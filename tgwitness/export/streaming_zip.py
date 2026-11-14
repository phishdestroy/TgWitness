import base64
import hashlib
import json
import os
import struct
import threading
import zipfile
from contextlib import suppress
from pathlib import Path

from ..account_export import durable_write, linked
from ..store import canonical

TAIL = ("manifest.json", "manifest.sig")
COPY = 1024 * 1024
SEALED_LIMIT = 64 * 1024**2


def digest(data):
    return hashlib.sha256(data).hexdigest()


class LiveZip:
    def __init__(self, path):
        self.path = Path(path)
        self.sealed = self.path.with_name(self.path.name + ".sealed")
        self.lock = threading.Lock()
        self.offset, self.tail, self.size, self.members = None, b"", 0, 0

    def append(self, members, finish):
        with self.lock:
            if linked(self.path) or linked(self.sealed) or linked(self.path.parent):
                raise ValueError("Live archive paths must not be links.")
            fresh = self.offset is None
            if not fresh and self.path.stat().st_size != self.size:
                self.restore((self.offset, self.tail, self.size))
            try:
                written, offset, tail, size, count = self.write(fresh, members, finish)
            except BaseException:
                if fresh:
                    with suppress(OSError):
                        self.path.unlink(missing_ok=True)
                else:
                    with suppress(Exception):
                        self.restore((self.offset, self.tail, self.size))
                raise
            self.offset, self.tail, self.size, self.members = offset, tail, size, count
            self.remember(offset, tail, size)
            return written

    def write(self, fresh, members, finish):
        with open(self.path, "w+b" if fresh else "r+b") as handle:
            with zipfile.ZipFile(handle, "w" if fresh else "a", zipfile.ZIP_DEFLATED, allowZip64=True) as archive:
                if not fresh:
                    self.reopen(archive)
                written = {}
                for name, data in members:
                    if name in TAIL or name in archive.NameToInfo:
                        raise ValueError("Live archive member already exists: " + name)
                    archive.writestr(name, data)
                    written[name] = digest(data)
                offset = archive.start_dir
                closing = list(finish(written))
                if [name for name, _ in closing] != list(TAIL):
                    raise ValueError("A live archive seal ends with its manifest and signature.")
                for name, data in closing:
                    archive.writestr(name, data)
                count = len(archive.filelist)
            handle.flush()
            os.fsync(handle.fileno())
            size = handle.seek(0, os.SEEK_END)
            handle.seek(offset)
            return written, offset, handle.read(), size, count

    @staticmethod
    def reopen(archive):
        stale = [info for info in archive.filelist if info.filename in TAIL]
        if sorted(info.filename for info in stale) != sorted(TAIL):
            raise ValueError("The live archive has no manifest at its end.")
        start = min(info.header_offset for info in stale)
        if any(info.header_offset >= start for info in archive.filelist if info.filename not in TAIL):
            raise ValueError("The live archive manifest is not at its end.")
        archive.filelist = [info for info in archive.filelist if info.filename not in TAIL]
        for name in TAIL:
            del archive.NameToInfo[name]
        archive.start_dir = start

    def remember(self, offset, tail, size):
        durable_write(self.sealed, canonical({"offset": offset, "size": size, "sha256": digest(tail),
                                              "tail": base64.b64encode(tail).decode("ascii")}))

    def saved(self):
        if linked(self.sealed) or self.sealed.stat().st_size > SEALED_LIMIT:
            raise ValueError("The live archive seal record is invalid.")
        state = json.loads(self.sealed.read_bytes())
        tail = base64.b64decode(state["tail"], validate=True)
        if (digest(tail) != state["sha256"] or type(state["offset"]) is not int or type(state["size"]) is not int
                or state["offset"] < 0 or state["offset"] + len(tail) != state["size"]):
            raise ValueError("The live archive seal record is damaged.")
        return state["offset"], tail, state["size"]

    def restore(self, sealed=None):
        offset, tail, size = sealed or self.saved()
        with open(self.path, "r+b") as handle:
            if handle.seek(0, os.SEEK_END) < offset:
                raise ValueError("The live archive is shorter than its last seal.")
            handle.seek(offset)
            handle.truncate()
            handle.write(tail)
            handle.flush()
            os.fsync(handle.fileno())
        self.offset, self.tail, self.size = offset, tail, size

    def intact(self):
        try:
            with zipfile.ZipFile(self.path) as archive:
                infos = sorted(archive.infolist(), key=lambda info: info.header_offset)
                if [info.filename for info in infos[-2:]] != list(TAIL):
                    return None
                offset, count = infos[-2].header_offset, len(infos)
            with open(self.path, "rb") as handle:
                size = handle.seek(0, os.SEEK_END)
                handle.seek(size - 22)
                end = handle.read(22)
                if end[:4] != b"PK\x05\x06" or struct.unpack("<H", end[20:22])[0]:
                    return None
                handle.seek(offset)
                return offset, handle.read(), size, count
        except (OSError, zipfile.BadZipFile, ValueError, EOFError, struct.error):
            return None

    def recover(self):
        with self.lock:
            if linked(self.path) or linked(self.sealed):
                raise ValueError("Live archive paths must not be links.")
            found = self.intact()
            if found is None:
                self.restore()
                found = self.intact()
                if found is None:
                    raise ValueError("The live archive could not be restored to its last seal.")
                self.members = found[3]
                return True
            self.offset, self.tail, self.size, self.members = found
            try:
                current = self.saved()[1]
            except (OSError, ValueError, KeyError, TypeError):
                current = None
            if current != found[1]:
                self.remember(found[0], found[1], found[2])
            return False

    def snapshot(self, target):
        with self.lock:
            offset, tail = self.offset, self.tail
        if offset is None:
            raise ValueError("No sealed page yet.")
        with open(self.path, "rb") as source, open(target, "xb") as out:
            left = offset
            while left:
                chunk = source.read(min(left, COPY))
                if not chunk:
                    raise ValueError("The live archive is shorter than its last seal.")
                out.write(chunk)
                left -= len(chunk)
            out.write(tail)
        return Path(target)
