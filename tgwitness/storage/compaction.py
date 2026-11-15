import asyncio
import logging
import time
from pathlib import Path

import zstandard

MEANING = ("Repackages old closed journal export segments (.jsonl) as compressed .jsonl.zst files "
           "in the background without blocking the active writer. The hash chain is preserved.")
COMPRESSED_SUFFIX = ".jsonl.zst"
SEGMENT_GLOB = "*.jsonl"
MIN_AGE_SECONDS = 3600
COMPRESSION_LEVEL = 3
log = logging.getLogger(__name__)


def _is_active(path, store):
    try:
        active = getattr(store, "_active_export_path", None)
        if active and Path(active) == path:
            return True
    except Exception:
        pass
    return False


async def compact_file(path: Path) -> dict:
    out = path.with_suffix("").with_suffix(COMPRESSED_SUFFIX)
    if out.exists():
        return {"path": str(path), "skipped": "already_compressed"}
    original_bytes = path.stat().st_size

    def _do():
        cctx = zstandard.ZstdCompressor(level=COMPRESSION_LEVEL)
        with open(path, "rb") as src, open(out, "wb") as dst:
            cctx.copy_stream(src, dst)
        return out.stat().st_size

    compressed_bytes = await asyncio.get_running_loop().run_in_executor(None, _do)
    path.unlink()
    log.info("Compacted %s: %s → %s bytes", path.name, original_bytes, compressed_bytes)
    return {"path": str(path), "original_bytes": original_bytes, "compressed_bytes": compressed_bytes}


class JournalCompactor:
    def __init__(self, store, root: Path, *, loop_interval=300, clock=time.monotonic):
        self.store = store
        self.root = root
        self.loop_interval = loop_interval
        self.clock = clock
        self._running = False
        self._last: dict | None = None
        self._last_at: float | None = None
        self._total = self._errors = 0

    def _candidate_dirs(self):
        candidates = []
        for folder in ("data", "export", "."):
            p = self.root / folder
            if p.is_dir():
                candidates.append(p)
        return candidates

    def _find_segments(self):
        now = time.time()
        segments = []
        for folder in self._candidate_dirs():
            for path in sorted(folder.glob(SEGMENT_GLOB)):
                try:
                    age = now - path.stat().st_mtime
                    if age >= MIN_AGE_SECONDS and not _is_active(path, self.store):
                        segments.append(path)
                except OSError:
                    pass
        return segments

    async def run_once(self):
        segments = self._find_segments()
        results = []
        for path in segments:
            await asyncio.sleep(0)
            try:
                r = await compact_file(path)
                results.append(r)
                self._total += 1
            except Exception as exc:
                self._errors += 1
                results.append({"path": str(path), "error": str(exc)})
        self._last = {"segments": len(segments), "results": results}
        self._last_at = self.clock()
        return self._last

    async def loop(self):
        self._running = True
        while self._running:
            await asyncio.sleep(self.loop_interval)
            try:
                await self.run_once()
            except Exception as exc:
                log.warning("Compaction error: %s", exc)

    def stop(self):
        self._running = False

    def public(self):
        return {
            "total": self._total,
            "errors": self._errors,
            "last": self._last,
            "last_at": self._last_at,
        }
