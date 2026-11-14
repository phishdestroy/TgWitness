import asyncio

from telethon.errors import TypeNotFoundError

WINDOW = 0.05
LIMIT = 100


class MessageBatcher:
    def __init__(self, window=WINDOW, limit=LIMIT):
        self.window, self.limit = window, limit
        self.batches, self.tasks = {}, set()
        self.asked = self.calls = 0

    async def get(self, client, peer, number):
        loop = asyncio.get_running_loop()
        key = (id(client), peer)
        batch = self.batches.get(key)
        if batch is None:
            batch = self.batches[key] = {"client": client, "peer": peer, "waiters": [], "numbers": set()}
            batch["timer"] = loop.call_later(self.window, self.send, key, batch)
        future = loop.create_future()
        batch["waiters"].append((number, future))
        batch["numbers"].add(number)
        self.asked += 1
        if len(batch["numbers"]) >= self.limit:
            batch["timer"].cancel()
            self.send(key, batch)
        return await future

    def send(self, key, batch):
        if self.batches.get(key) is batch:
            del self.batches[key]
        task = asyncio.get_running_loop().create_task(self.run(batch))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    async def run(self, batch):
        numbers = sorted(batch["numbers"])
        try:
            try:
                found = dict(zip(numbers, await self.ask(batch, numbers)))
            except TypeNotFoundError:
                if len(numbers) == 1:
                    raise
                found = {}
                for number in numbers:
                    try:
                        found[number] = (await self.ask(batch, [number]))[0]
                    except Exception as exc:
                        found[number] = exc
        except Exception as exc:
            for _, future in batch["waiters"]:
                if not future.done():
                    future.set_exception(exc)
            return
        except BaseException:
            for _, future in batch["waiters"]:
                future.cancel()
            raise
        for number, future in batch["waiters"]:
            if future.done():
                continue
            value = found.get(number)
            if isinstance(value, Exception):
                future.set_exception(value)
            else:
                future.set_result(value)

    async def ask(self, batch, numbers):
        self.calls += 1
        answer = await batch["client"].get_messages(batch["peer"], ids=list(numbers))
        return list(answer) if isinstance(answer, (list, tuple)) else [answer]
