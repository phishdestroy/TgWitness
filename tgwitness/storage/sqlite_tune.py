import sqlite3

SETTING = "sqlite_tune"
MEANING = ("SQLite WAL mode and cache settings applied to every workspace connection. "
           "Overrides can be stored per account in the sqlite_tune workspace setting.")

PRAGMAS = {
    "journal_mode": "WAL",
    "synchronous": "NORMAL",
    "wal_autocheckpoint": 2000,
    "cache_size": -32768,
    "mmap_size": 268435456,
}

_SKIP_COMPARE = {"journal_mode"}


def apply(conn, overrides=None):
    merged = dict(PRAGMAS)
    if overrides:
        for key, value in overrides.items():
            if key in PRAGMAS:
                merged[key] = value
    for key, value in merged.items():
        try:
            conn.execute(f"PRAGMA {key} = {value!r}")
        except sqlite3.OperationalError:
            pass
    return merged


def from_store(store):
    value = store.get_setting(SETTING, {})
    return value if isinstance(value, dict) else {}


def apply_from_store(conn, store):
    return apply(conn, from_store(store))


def public(overrides=None):
    merged = dict(PRAGMAS)
    if overrides:
        for key, value in overrides.items():
            if key in PRAGMAS:
                merged[key] = value
    return {"pragmas": merged}
