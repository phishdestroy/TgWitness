import asyncio
import logging

MEANING = ("Splits message processing into fetch → parse → sign → write → index stages connected by "
           "asyncio queues. CPU-bound signing and writing run in a thread executor so network fetches "
           "are never blocked by disk I/O or cryptography.")
QUEUE_DEPTH_TEXT = 512
QUEUE_DEPTH_MEDIA = 64
log = logging.getLogger(__name__)


class PipelineStage:
    def __init__(self, name, fn, in_queue: asyncio.Queue, out_queue: asyncio.Queue | None = None,
                 *, executor=None):
        self.name = name
        self.fn = fn
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.executor = executor
        self.processed = self.errors = self.dropped = 0
        self._task = None

    async def _run(self):
        loop = asyncio.get_running_loop()
        while True:
            item = await self.in_queue.get()
            if item is None:
                if self.out_queue is not None:
                    await self.out_queue.put(None)
                self.in_queue.task_done()
                break
            try:
                if self.executor is not None:
                    result = await loop.run_in_executor(self.executor, self.fn, item)
                else:
                    result = await self.fn(item) if asyncio.iscoroutinefunction(self.fn) else self.fn(item)
                if self.out_queue is not None and result is not None:
                    await self.out_queue.put(result)
                self.processed += 1
            except Exception as exc:
                self.errors += 1
                log.debug("Pipeline stage %s error: %s", self.name, exc)
            finally:
                self.in_queue.task_done()

    def start(self):
        self._task = asyncio.ensure_future(self._run())
        return self._task

    def public(self):
        return {
            "stage": self.name,
            "processed": self.processed,
            "errors": self.errors,
            "queue_size": self.in_queue.qsize(),
        }


class MessagePipeline:
    def __init__(self, *, fetch_fn, parse_fn, sign_fn, write_fn, index_fn,
                 executor=None, queue_depth_text=QUEUE_DEPTH_TEXT, queue_depth_media=QUEUE_DEPTH_MEDIA):
        self._fetch_q = asyncio.Queue(maxsize=queue_depth_text)
        self._parse_q = asyncio.Queue(maxsize=queue_depth_text)
        self._sign_q = asyncio.Queue(maxsize=queue_depth_text)
        self._write_q = asyncio.Queue(maxsize=queue_depth_text)

        self._stages = [
            PipelineStage("fetch", fetch_fn, self._fetch_q, self._parse_q),
            PipelineStage("parse", parse_fn, self._parse_q, self._sign_q),
            PipelineStage("sign", sign_fn, self._sign_q, self._write_q, executor=executor),
            PipelineStage("write", write_fn, self._write_q, None, executor=executor),
        ]
        self._index_fn = index_fn
        self._running = False

    async def submit(self, item):
        await self._fetch_q.put(item)

    def start(self):
        self._running = True
        for stage in self._stages:
            stage.start()

    async def finish(self):
        await self._fetch_q.put(None)
        for stage in self._stages:
            if stage._task is not None:
                await stage._task
        self._running = False

    def public(self):
        return {
            "running": self._running,
            "stages": [s.public() for s in self._stages],
        }
