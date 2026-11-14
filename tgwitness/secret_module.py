"""Fetch, check and load the Secret Chat protocol library"""
import asyncio
import hashlib
import importlib.abc
import importlib.util
import io
import sys
import zipfile

from . import netclient
from .security import owner_only
from .security import private_write
from .workers import complete_in_thread

PACKAGE = "telethon_secret_chat"
INFO = {"name": "kiaro-telethon-secret-chat", "version": "0.2.0", "author": "KiaroSama", "license": "GPL-3.0-or-later",
        "source": "https://github.com/KiaroSama/Telethon-Secret-Chat",
        "commit": "d87bf037b90060383c7b704d8a06ebb98c621c6f",
        "sha256": "c80feb9b5bc28201677c140d20930fbd730d7efdebb8ca789a19040c3f00ce5c"}
ARCHIVE = "https://codeload.github.com/KiaroSama/Telethon-Secret-Chat/zip/" + INFO["commit"]
FILE = "telethon-secret-chat-" + INFO["commit"] + ".zip"
LIMIT = 16 * 1024 * 1024
MISMATCH = ("The pseudo-secret module differs from the version pinned by this TgWitness release, "
            "so it was not loaded. Install it again.")
BROKEN = "The pseudo-secret module passed its check but could not start. Update TgWitness and install it again."
home = None
problem = None
lock = asyncio.Lock()


class Refused(ValueError):
    pass


class Verified(importlib.abc.MetaPathFinder, importlib.abc.InspectLoader):
    def __init__(self, files):
        self.files = files

    def located(self, name):
        base = name.replace(".", "/")
        return next((path for path in (base + "/__init__.py", base + ".py") if path in self.files), None)

    def find_spec(self, name, path=None, target=None):
        found = self.located(name) if name == PACKAGE or name.startswith(PACKAGE + ".") else None
        if not found:
            return None
        spec = importlib.util.spec_from_loader(name, self, origin=FILE + "/" + found,
                                               is_package=found.endswith("/__init__.py"))
        spec.has_location = True
        return spec

    def is_package(self, name):
        return (self.located(name) or "").endswith("/__init__.py")

    def get_source(self, name):
        return importlib.util.decode_source(self.files[self.located(name)])

    def get_code(self, name):
        found = self.located(name)
        return compile(self.files[found], FILE + "/" + found, "exec", dont_inherit=True)


def checked(data):
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            wanted = [(item, item.filename.partition("/")[2]) for item in archive.infolist() if not item.is_dir()]
            wanted = [(item, name) for item, name in wanted
                      if name in ("LICENSE", "NOTICE") or name.startswith(PACKAGE + "/")]
            if sum(item.file_size for item, _ in wanted) > LIMIT or len({name for _, name in wanted}) != len(wanted):
                raise Refused(MISMATCH)
            files = {name: archive.read(item) for item, name in wanted}
    except Exception:
        raise Refused(MISMATCH) from None
    listing = "".join(hashlib.sha256(files[name]).hexdigest() + "  " + name + "\n" for name in sorted(files))
    if hashlib.sha256(listing.encode()).hexdigest() != INFO["sha256"]:
        raise Refused(MISMATCH)
    return files


def start(files):
    from . import secret_chats
    finder = Verified(files)
    sys.meta_path.append(finder)
    try:
        if secret_chats.bind():
            return
    except Exception:
        secret_chats.LOG.exception("The checked Secret Chat module could not start")
    sys.meta_path.remove(finder)
    for name in [name for name in sys.modules if name == PACKAGE or name.startswith(PACKAGE + ".")]:
        del sys.modules[name]
    raise Refused(BROKEN)


def restore(root):
    global home, problem
    from . import secret_chats
    home = root / "modules"
    path = home / FILE
    if secret_chats.available() or not path.is_file():
        return
    try:
        if path.stat().st_size > LIMIT:
            raise Refused(MISMATCH)
        start(checked(path.read_bytes()))
    except OSError:
        problem = MISMATCH
    except Refused as exc:
        problem = str(exc)


def save(data):
    files = checked(data)
    home.mkdir(parents=True, exist_ok=True)
    owner_only(home)
    private_write(home / FILE, data)
    return files


async def install(network):
    global problem
    from . import secret_chats
    async with lock:
        if secret_chats.available():
            return
        if home is None:
            raise RuntimeError("The module folder is not set")
        _, _, data = await netclient.request("GET", ARCHIVE, network, timeout=60, limit=LIMIT)
        start(await complete_in_thread(save, data))
        problem = None


def describe():
    from . import secret_chats
    library = secret_chats.library
    if library is None:
        return {**INFO, "state": None, "problem": problem}
    if isinstance(getattr(library, "__loader__", None), Verified):
        return {**INFO, "state": "checked", "problem": None}
    return {**INFO, "version": getattr(library, "__version__", None), "commit": None, "sha256": None,
            "state": "environment", "problem": None}
