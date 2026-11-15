import asyncio
import logging
import time

from ..media.cas import DIGEST, linked

log = logging.getLogger(__name__)

MEANING = ("Removes shared media files that have no reference in the journal. "
           "Only files whose nlink count has dropped to 1 (no hardlinks from workspace copies) are removed.")


def _has_ref(store, sha256):
    with store.reading() as db:
        row = db.execute(
            "SELECT 1 FROM events WHERE kind IN ('media.saved','media.attachment')"
            " AND json_extract(payload,'$.media_sha256')=? LIMIT 1",
            (sha256,)
        ).fetchone()
    return row is not None


async def run_gc(store, library, *, dry_run=False):
    removed = skipped = bytes_freed = 0
    root = library.root
    if not root.is_dir() or linked(root):
        return {"removed": 0, "skipped": 0, "bytes_freed": 0, "dry_run": dry_run}
    for folder in root.iterdir():
        if linked(folder) or not folder.is_dir():
            continue
        for path in folder.iterdir():
            await asyncio.sleep(0)
            try:
                info = path.stat(follow_symlinks=False)
                if not DIGEST.fullmatch(path.name) or linked(path):
                    skipped += 1
                    continue
                if info.st_nlink > 1:
                    skipped += 1
                    continue
                if _has_ref(store, path.name):
                    skipped += 1
                    continue
                if not dry_run:
                    path.unlink(missing_ok=True)
                removed += 1
                bytes_freed += info.st_size
            except OSError:
                skipped += 1
    log.info("Media GC: removed=%s skipped=%s bytes_freed=%s dry_run=%s",
             removed, skipped, bytes_freed, dry_run)
    return {"removed": removed, "skipped": skipped, "bytes_freed": bytes_freed, "dry_run": dry_run}


class MediaGC:
    def __init__(self, store, library):
        self.store = store
        self.library = library
        self._last: dict | None = None
        self._last_at: float | None = None

    async def run(self, *, dry_run=False):
        result = await run_gc(self.store, self.library, dry_run=dry_run)
        self._last = result
        self._last_at = time.monotonic()
        return result

    def public(self):
        return {
            "last": self._last,
            "last_at": self._last_at,
        }
