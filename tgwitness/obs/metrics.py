import math

from ..swarm.dashboard import SWARM, meter

CONTENT_TYPE = "text/plain; version=0.0.4; charset=utf-8"
STATES = ("busy", "idle", "waiting", "blocked", "offline")
JOURNAL_FILES = ("journal.sqlite3", "journal.sqlite3-wal", "journal.sqlite3-shm")


def escape(value):
    return str(value).replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


def number(value):
    if isinstance(value, bool):
        return str(int(value))
    if isinstance(value, int):
        return str(value)
    return repr(float(value)) if math.isfinite(value) else ("+Inf" if value > 0 else "-Inf" if value < 0 else "NaN")


class Families:
    def __init__(self):
        self.families = {}

    def add(self, name, kind, text, labels, value):
        if value is None:
            return
        self.families.setdefault(name, (kind, text, []))[2].append((labels, value))

    def text(self):
        lines = []
        for name, (kind, text, samples) in self.families.items():
            lines += ["# HELP " + name + " " + text, "# TYPE " + name + " " + kind]
            for labels, value in samples:
                tags = ",".join(key + '="' + escape(item) + '"' for key, item in labels.items())
                lines.append(name + ("{" + tags + "}" if tags else "") + " " + number(value))
        return "\n".join(lines) + "\n"


def journal_bytes(root):
    total = 0
    for name in JOURNAL_FILES:
        try:
            total += (root / name).stat().st_size
        except OSError:
            pass
    return total


def head(store):
    with store.reading() as db:
        row = db.execute("SELECT seq FROM events ORDER BY seq DESC LIMIT 1").fetchone()
    return row[0] if row else 0


def account(families, row, state):
    labels = {"workspace": row["id"], "label": row["label"]}
    add = families.add
    add("tgw_workspace_up", "gauge", "1 while the workspace runs in this process.", labels,
        int(row["state"] != "unavailable"))
    if row["state"] == "unavailable" or state is None:
        return
    add("tgw_observing", "gauge", "1 while the account observes its sources.", labels, int(row["observing"]))
    add("tgw_connected", "gauge", "1 while the account is connected to Telegram.", labels, int(row["connected"]))
    for name in STATES:
        add("tgw_account_state", "gauge", "Current state of the account; one series is 1.", {**labels, "state": name},
            int(row["state"] == name))
    rates = row["rates"]
    for lane, value in (("all", rates["records"]), ("text", rates["text"]), ("media", rates["media"])):
        add("tgw_records_per_sec", "gauge", "Journal records per second over the last 10 seconds.",
            {**labels, "lane": lane}, value)
    add("tgw_floodwait_remaining_seconds", "gauge", "Seconds left in the longest Telegram wait of the account.",
        labels, row["flood"]["remaining"] if row["flood"] else 0)
    for queue, value in row["queue"].items():
        add("tgw_queue_depth", "gauge", "Attachments in the file queue by state.", {**labels, "queue": "files",
                                                                                   "state": queue}, value)
    downloads = row["downloads"]
    add("tgw_downloads_active", "gauge", "Files downloading now.", labels, downloads["active"])
    add("tgw_media_connections", "gauge", "File connections open to Telegram data centers.", labels,
        downloads["connections"])
    for lane, slots in sorted((getattr(state.collector, "media_slots", None) or {}).items()):
        add("tgw_download_slots", "gauge", "Attachments the account may download at once now, by queue.",
            {**labels, "lane": lane}, slots.limit)
    found = meter(state.store)
    for lane, value in found.totals.items():
        add("tgw_records_total", "counter", "Journal records written since the process started.",
            {**labels, "lane": lane}, value)
    add("tgw_floodwait_seconds_total", "counter",
        "Seconds Telegram asked the account to wait since the process started.", labels, found.flood_seconds)
    add("tgw_media_bytes_total", "counter", "Bytes of attachments saved since the process started.", labels,
        found.media_bytes)
    for kind, value in sorted(found.problems.items()):
        add("tgw_problems_total", "counter", "Problem records written since the process started, by kind.",
            {**labels, "kind": kind}, value)
    add("tgw_journal_bytes", "gauge", "Size of the journal database files.", labels, journal_bytes(state.store.root))
    add("tgw_journal_records", "gauge", "Records in the signed journal.", labels, head(state.store))


def collect(app_state, profile_id="default"):
    snapshot = SWARM.snapshot(app_state, profile_id)
    registry = getattr(app_state, "profiles", None)
    entries = registry.entries if registry else {}
    families = Families()
    for row in snapshot["accounts"]:
        entry = entries.get(row["id"])
        state = app_state if entry is None or entry.get("self") else getattr(entry.get("app"), "state", None)
        try:
            account(families, row, state)
        except Exception:
            families.add("tgw_workspace_up", "gauge", "1 while the workspace runs in this process.",
                         {"workspace": row["id"], "label": row["label"]}, 0)
    gates = snapshot["gates"]
    for gate in ("handshakes", "registrations"):
        value = gates.get(gate) or {}
        labels = {"gate": gate}
        families.add("tgw_gate_active", "gauge", "Connection setups running now.", labels, value.get("active"))
        families.add("tgw_gate_waiting", "gauge", "Connection setups waiting for a turn.", labels, value.get("waiting"))
        families.add("tgw_gate_started_total", "counter", "Connection setups started since the process started.",
                     labels, value.get("started"))
        families.add("tgw_gate_timeouts_total", "counter", "Connection setups that timed out.", labels,
                     value.get("timeouts"))
    families.add("tgw_downloads_joined_total", "counter",
                 "File requests answered by a download that was already running.", {},
                 (snapshot.get("files") or {}).get("joined"))
    return families.text()
