import time
import weakref
from collections import deque

from ..media.dedup_queue import DOWNLOADS
from ..store import utcnow
from ..transport import burst

SCHEMA = "tgwitness-swarm-v1"
WINDOW = 10
SLOW_SECONDS = 5
PROBLEMS = frozenset({"coverage.gap", "collector.error", "network.connection_failed", "network.route_unavailable",
                      "network.slow_route", "media.failed", "account.authorization_error", "storage.low",
                      "history.source.failed", "telegram.backoff"})
BLOCKING_ROUTE = frozenset({"down"})
_meters = weakref.WeakKeyDictionary()


class Meter:
    def __init__(self, clock=time.monotonic, wall=time.time):
        self.clock, self.wall, self.events, self.problem = clock, wall, deque(), None
        self.totals, self.flood_seconds, self.media_bytes, self.problems = {"text": 0, "media": 0, "other": 0}, 0, 0, {}

    def __call__(self, event):
        now, kind = self.clock(), event.get("kind") or ""
        lane = "text" if kind.startswith("message.") else "media" if kind.startswith("media.") else "other"
        self.events.append((now, lane))
        self.totals[lane] += 1
        self.trim(now)
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        if kind == "telegram.backoff":
            seconds = next((payload[key] for key in ("retry_after_seconds", "seconds")
                            if type(payload.get(key)) in (int, float) and payload[key] > 0), 0)
            self.flood_seconds += seconds
        elif kind == "media.saved" and type(payload.get("size")) is int and payload["size"] > 0:
            self.media_bytes += payload["size"]
        if kind in PROBLEMS:
            self.problems[kind] = self.problems.get(kind, 0) + 1
            reason = next((payload.get(key) for key in ("reason", "failed_method", "error_type", "status", "method")
                           if isinstance(payload.get(key), str) and payload.get(key)), None)
            self.problem = {"kind": kind, "reason": reason, "at": self.wall(), "seq": event.get("seq")}

    def trim(self, now):
        while self.events and now - self.events[0][0] > WINDOW:
            self.events.popleft()

    def rates(self):
        self.trim(self.clock())
        counts = {"text": 0, "media": 0, "other": 0}
        for _, lane in self.events:
            counts[lane] += 1
        return {"records": round(len(self.events) / WINDOW, 1), "text": round(counts["text"] / WINDOW, 1),
                "media": round(counts["media"] / WINDOW, 1)}


def meter(store):
    found = _meters.get(store)
    if found is None:
        found = _meters[store] = Meter()
        store.listeners.append(found)
    return found


def slow_facts(state, task):
    collector, store = state.collector, state.store
    account = store.get_setting("account", None) or {}
    media = store.media_stats()
    route = collector.route_status()
    health = store.get_setting("route_health", None) or {}
    try:
        session = bool(state.vault.read("credentials").get("session"))
    except Exception:
        session = bool(account.get("id"))
    facts = {"account": {"id": account.get("id"), "username": account.get("username")} if account.get("id") else None,
             "has_session": session, "account_loss": bool(store.get_setting("account_loss", None)),
             "media": {"queued": media.get("queued", 0) + media.get("retry", 0), "running": media.get("running", 0),
                       "failed": media.get("failed", 0)},
             "route": {"kind": route.get("kind"), "managed": route.get("managed"),
                       "status": health.get("status") if health.get("format") else None, "ema_ms": health.get("ema_ms"),
                       "fallback": bool(route.get("fallback_to_direct"))},
             "history": None}
    if task == "history":
        status = collector.history.status()
        if status.get("phase") not in (None, "none"):
            phases = status.get("sources_by_phase") or {}
            finished = sum(phases.get(key, 0) for key in ("complete", "failed", "skipped"))
            facts["history"] = {"phase": status.get("phase"), "sources": status.get("sources_total", 0),
                                "finished": finished, "captured": status.get("captured", 0),
                                "media_pending": status.get("media_pending", 0)}
    return facts


def classify(row):
    if row["authorization_required"] or row["account_loss"]:
        return "blocked", "sign_in"
    if (row["route"] or {}).get("status") in BLOCKING_ROUTE:
        return "blocked", "route_down"
    if row["flood"] and row["flood"]["remaining"] >= 3 and not row["observing"]:
        return "waiting", "flood_wait"
    if row["task"] or row["downloads"]["active"] or row["downloads"]["busy"]:
        return "busy", None
    if row["connected"] or row["has_session"]:
        return "idle", None
    return "offline", None


def account_row(identifier, entry, registry, groups, cache, now, wall):
    group = registry.group_of(identifier) if registry else None
    base = {"id": identifier, "label": entry.get("label") or identifier,
            "group": {"id": group, "label": groups.get(group, "")} if group else None}
    app = entry.get("app")
    if app is None:
        return {**base, "state": "unavailable", "reason": entry.get("error_type") or "unavailable"}
    collector, store = app.state.collector, app.state.store
    activity = collector.activity()
    task = activity.get("task")
    slow = cache.get(identifier)
    if slow is None or now - slow["at"] >= SLOW_SECONDS or slow.get("task") != task:
        slow = cache[identifier] = {"at": now, "task": task, **slow_facts(app.state, task)}
    client = collector.client
    floods = {key: until for key, until in collector.flood_waits().items() if until > wall}
    flood = max(floods.items(), key=lambda item: item[1]) if floods else None
    pool = client._media_pool.snapshot() if getattr(client, "_media_pool", None) is not None else None
    dcs = (pool or {}).get("dcs", [])
    row = {
        **base,
        "account": slow["account"], "phase": collector.phase, "observing": bool(collector.running),
        "connected": bool(client and client.is_connected()), "has_session": slow["has_session"],
        "authorization_required": bool(collector.authorization_required), "account_loss": slow["account_loss"],
        "task": task, "detail": activity.get("detail"), "history": slow["history"],
        "rates": meter(store).rates(),
        "flood": {"method": flood[0], "remaining": round(flood[1] - wall), "methods": len(floods)} if flood else None,
        "queue": slow["media"],
        "downloads": {"active": DOWNLOADS.active(store.root), "connections": sum(dc["connections"] for dc in dcs),
                      "busy": sum(dc["busy"] for dc in dcs), "waiting": sum(dc["waiting"] for dc in dcs),
                      "limit": (pool or {}).get("limit"), "floods": sum(dc["floods"] for dc in dcs)},
        "route": slow["route"],
        "problem": meter(store).problem, "last_error": collector.last_error,
    }
    row["state"], row["reason"] = classify(row)
    return row


class Swarm:
    def __init__(self, clock=time.monotonic, wall=time.time):
        self.clock, self.wall, self.cache = clock, wall, {}

    def snapshot(self, app_state, profile_id="default"):
        registry = getattr(app_state, "profiles", None)
        entries = registry.entries if registry else {
            profile_id: {"label": app_state.store.get_setting("profile_label", "Main workspace"), "app": None,
                         "self": True}}
        groups = {item["id"]: item["label"] for item in (registry.groups() if registry else [])}
        now, wall, rows = self.clock(), self.wall(), []
        for identifier, entry in list(entries.items()):
            if entry.get("self"):
                entry = {**entry, "app": _Self(app_state)}
            try:
                rows.append(account_row(identifier, entry, registry, groups, self.cache, now, wall))
            except Exception as exc:
                rows.append({"id": identifier, "label": entry.get("label") or identifier, "state": "unavailable",
                             "reason": type(exc).__name__})
        for stale in set(self.cache) - set(entries):
            del self.cache[stale]
        totals = {state: sum(1 for row in rows if row["state"] == state)
                  for state in ("busy", "idle", "waiting", "blocked", "offline", "unavailable")}
        live = [row for row in rows if "rates" in row]
        totals.update(accounts=len(rows), records_per_second=round(sum(row["rates"]["records"] for row in live), 1),
                      downloads=sum(row["downloads"]["active"] for row in live),
                      connections=sum(row["downloads"]["connections"] for row in live),
                      queued_files=sum(row["queue"]["queued"] for row in live),
                      flood_waits=sum(1 for row in live if row["flood"]))
        return {"schema": SCHEMA, "generated_at": utcnow(), "accounts": rows, "totals": totals,
                "gates": burst.snapshot(), "files": DOWNLOADS.snapshot(limit=8)}


class _Self:
    def __init__(self, state):
        self.state = state


SWARM = Swarm()
