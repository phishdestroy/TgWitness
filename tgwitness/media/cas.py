import hashlib
import logging
import os
import re
from contextlib import suppress
from pathlib import Path

DIGEST = re.compile(r"[0-9a-f]{64}")
log = logging.getLogger(__name__)


def digest_of(path):
    with open(path, "rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def linked(path):
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())


class MediaLibrary:
    def __init__(self, root):
        self.root = Path(root)

    def shared(self, digest):
        return self.root / digest[:2] / digest

    def adopt(self, path, digest):
        path = Path(path)
        if not DIGEST.fullmatch(digest) or linked(path) or not path.is_file() or linked(self.root):
            return "skipped"
        shared = self.shared(digest)
        for _ in range(2):
            try:
                if shared.exists():
                    if linked(shared) or os.path.samefile(shared, path):
                        return "kept"
                    if shared.stat().st_size != path.stat().st_size or digest_of(shared) != digest:
                        return "kept"
                    temporary = path.with_name(path.name + ".shared")
                    temporary.unlink(missing_ok=True)
                    os.link(shared, temporary)
                    os.replace(temporary, path)
                    return "joined"
                shared.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                os.link(path, shared)
                return "shared"
            except FileExistsError:
                continue
            except OSError as exc:
                log.info("Attachment kept as a separate copy: %s", type(exc).__name__)
                return "kept"
        return "kept"

    def sweep(self):
        removed = freed = 0
        if not self.root.is_dir() or linked(self.root):
            return removed, freed
        for folder in self.root.iterdir():
            if linked(folder) or not folder.is_dir():
                continue
            for path in folder.iterdir():
                with suppress(OSError):
                    info = path.stat(follow_symlinks=False)
                    if DIGEST.fullmatch(path.name) and info.st_nlink == 1 and not linked(path):
                        path.unlink()
                        removed, freed = removed + 1, freed + info.st_size
        if removed:
            log.info("Shared attachment library: %s unused copies removed, %s bytes freed", removed, freed)
        return removed, freed
