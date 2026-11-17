import hashlib
import json
import logging
import os
from pathlib import Path

from .security import private_write
from .store import utcnow

LOG = logging.getLogger("tgwitness.rollback")
MEANING = ("The journal is behind the last head this computer recorded for the same data directory and signing key. "
           "The data directory was restored from an older copy or replaced. Records after 'remembered' are missing "
           "here; archives exported before this point can hold records that this journal does not. Keep both and "
           "show this record with any archive exported from now on.")
UNWRITABLE = set()


def state_dir():
    configured = os.environ.get("TGWITNESS_STATE_DIR")
    if configured:
        return Path(configured)
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local") / "TgWitness" / "state"
    return Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local" / "state") / "tgwitness"


def marker(root):
    name = hashlib.sha256(str(Path(root).resolve()).encode("utf-8")).hexdigest()[:24] + ".json"
    return state_dir() / "journal-heads" / name


def remember(store, public_key):
    head = store.stats()["head"]
    if not head:
        return
    path = marker(store.root)
    try:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        private_write(path, json.dumps({"format": "tgwitness-journal-head-v1", "root": str(Path(store.root).resolve()),
                                        "public_key": public_key, "seq": head["seq"], "hash": head["hash"],
                                        "at": utcnow()}).encode("utf-8"))
    except OSError as exc:
        if path.parent not in UNWRITABLE:
            UNWRITABLE.add(path.parent)
            LOG.warning("Could not record the journal head in %s (%s); a restore from an older copy will not be "
                        "detected. Set TGWITNESS_STATE_DIR to a writable folder outside the data directory",
                        path.parent, type(exc).__name__)


def check(store, public_key):
    try:
        saved = json.loads(marker(store.root).read_bytes())
    except (OSError, ValueError):
        return None
    if not isinstance(saved, dict) or saved.get("public_key") != public_key or not isinstance(saved.get("seq"), int):
        return None
    head = store.stats()["head"] or {"seq": 0, "hash": None}
    with store.snapshot() as snapshot:
        found = snapshot.hash_at(saved["seq"]) if saved["seq"] <= head["seq"] else None
    if saved["seq"] <= head["seq"] and found == saved.get("hash"):
        return None
    return {"remembered": {"seq": saved["seq"], "hash": saved.get("hash"), "at": saved.get("at")},
            "journal_head": {"seq": head["seq"], "hash": head["hash"]},
            "reason": "shorter" if saved["seq"] > head["seq"] else "different_record",
            "meaning": MEANING}
