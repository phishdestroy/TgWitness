import asyncio
import hashlib
import hmac
import json
import secrets
import time
from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, model_validator

from . import netclient
from .store import utcnow

EVENTS = {"collector.error": "collector", "coverage.gap": "collector", "connection.restored": "collector",
          "observation.started": "collector", "media.failed": "media", "media.recovered": "media",
          "media.missing_after_restart": "media",
          "chat_export.completed": "export", "export.completed": "export",
          "message.new": "changes", "message.edited": "changes", "message.deleted": "changes",
          "message.missing_on_recheck": "changes", "message.recovered": "changes"}
MAX_PENDING = 1000
MAX_DEFERRED = 100


class HookSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=80)
    url: str = Field(max_length=2048)
    events: list[Literal["collector", "media", "export", "changes"]] = Field(default_factory=lambda: ["collector", "media", "export"], min_length=1, max_length=4)
    chats: list[int] = Field(default_factory=list, max_length=1000)
    include_text: bool = False

    @model_validator(mode="after")
    def valid(self):
        parsed = urlsplit(self.url)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query
                or parsed.fragment or any(ord(c) < 33 or ord(c) > 126 for c in self.url)):
            raise ValueError("Use an HTTPS webhook URL without credentials, query or fragment.")
        if "changes" in self.events and not self.chats:
            raise ValueError("Choose the chats whose changes may be sent.")
        self.events, self.chats = sorted(set(self.events)), sorted(set(self.chats))
        return self


def lock(store):
    if not hasattr(store, "webhook_lock"):
        store.webhook_lock = asyncio.Lock()
    return store.webhook_lock


def state(store):
    return store.get_setting("webhook_delivery", {"cursor": (store.stats()["head"] or {}).get("seq", 0),
                                                 "pending": [], "history": [], "last_error": None})


def public(entry):
    return {k: v for k, v in entry.items() if k != "secret"}


def lost_completions(data):
    count = data.get("lost_completions", 0)
    return (str(count) + " export completion notice(s) were never queued because the delivery queue was full."
            if count else None)


def completion_jobs(hooks, workspace, completion):
    jobs = []
    for hook in hooks:
        event = {"event_id": hashlib.sha256((workspace + ":" + hook["id"] + ":export.completed:"
                                             + completion["id"]).encode()).hexdigest(),
                 "kind": "export.completed", "observed_at": completion["observed_at"], "payload": {}}
        jobs.append(queued(hook, envelope(event, workspace, hook)))
    return jobs


def release_deferred(data, hooks, workspace):
    targets = [hook for hook in hooks if "export" in hook["events"]]
    while data.get("deferred") and len(data["pending"]) + len(targets) <= MAX_PENDING:
        data["pending"] += completion_jobs(targets, workspace, data["deferred"].pop(0))


def create(store, vault, body):
    entries = vault.read("webhooks").get("entries", [])
    if len(entries) >= 10:
        raise ValueError("At most ten webhook destinations are supported per workspace.")
    item = {**body.model_dump(), "id": secrets.token_hex(16), "secret": secrets.token_urlsafe(32),
            "start_seq": (store.stats()["head"] or {}).get("seq", 0), "created_at": utcnow()}
    entries.append(item)
    vault.save("webhooks", {"entries": entries})
    store.set_setting("webhook_delivery", state(store))
    return {"connection": public(item), "secret": item["secret"]}


def envelope(event, workspace, hook):
    kind = event["kind"]
    payload = {"schema": "tgwitness.webhook/1", "event_id": event.get("event_id") or hashlib.sha256(
        (workspace + ":" + hook["id"] + ":" + str(event["seq"]) + ":" + event["hash"]).encode()).hexdigest(),
        "timestamp": event["observed_at"], "workspace": workspace, "type": kind, "synthetic": False,
        "source": {"chat_id": event.get("chat_id"), "message_id": event.get("message_id"),
                   "event_seq": event.get("seq"), "hash": event.get("hash")}, "counts": {"events": 1}}
    if kind == "message.deleted":
        payload["deletion_notice"] = True
    if kind == "message.missing_on_recheck":
        payload["missing_on_recheck"] = True
    if hook["include_text"] and EVENTS.get(kind) == "changes" and isinstance(event["payload"].get("text"), str):
        payload["text"] = event["payload"]["text"][:1000]
        payload["text_truncated"] = len(event["payload"]["text"]) > 1000
    return payload


def queued(hook, payload):
    return {"destination": hook["id"], "event_id": payload["event_id"], "payload": payload,
            "attempts": 0, "next_attempt": 0, "created_at": utcnow()}


def signature(secret, body, timestamp):
    digest = hmac.new(secret.encode(), str(timestamp).encode() + b"." + body, hashlib.sha256).hexdigest()
    return "t=" + str(timestamp) + ",v1=" + digest


async def send(hook, payload, network):
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    async with asyncio.timeout(12):
        await netclient.request("POST", hook["url"], network, headers={"Content-Type": "application/json",
            "X-TgWitness-Signature": signature(hook["secret"], body, int(time.time())),
            "X-TgWitness-Event-ID": payload["event_id"]}, body=body, timeout=10, limit=4096)


async def pump(store, vault, network, workspace):
    async with lock(store):
        hooks = vault.read("webhooks").get("entries", [])
        data = state(store)
        if not hooks:
            data["cursor"] = (store.stats()["head"] or {}).get("seq", 0)
            data["pending"] = []
            data["deferred"] = []
            store.set_setting("webhook_delivery", data)
            return
        release_deferred(data, hooks, workspace)
        for event in store.events_after(data["cursor"], 200):
            targets = [hook for hook in hooks if event["seq"] > hook["start_seq"]
                       and EVENTS.get(event["kind"]) in hook["events"]
                       and (EVENTS[event["kind"]] != "changes" or event["chat_id"] in hook["chats"])]
            if len(data["pending"]) + len(targets) > MAX_PENDING:
                data["last_error"] = "Delivery queue is full; journal scanning will resume after delivery."
                break
            data["pending"] += [queued(hook, envelope(event, workspace, hook)) for hook in targets]
            data["cursor"] = event["seq"]
        destinations = {h["id"]: h for h in hooks}
        due = []
        for job in [job for job in data["pending"] if job["next_attempt"] <= time.time()][:5]:
            hook = destinations.get(job["destination"])
            if not hook:
                data["pending"].remove(job)
                continue
            # The attempt is counted before sending, so a crash mid-delivery still backs off.
            job["attempts"] += 1
            job["next_attempt"] = time.time() + min(3600, 15 * 2 ** (job["attempts"] - 1))
            due.append((hook, dict(job)))
        store.set_setting("webhook_delivery", data)
    # Deliveries run outside the lock: a slow receiver must not block editing or removing destinations.
    results = []
    for hook, job in due:
        error = None
        try:
            await send(hook, job["payload"], network)
        except Exception as exc:
            error = str(exc)[:300] if isinstance(exc, netclient.RouteError) else type(exc).__name__
            if isinstance(exc, netclient.HTTPError):
                error = "HTTP " + str(exc.status)
        results.append((job, error))
    if not results:
        return
    async with lock(store):
        data = state(store)
        for job, error in results:
            final = error is None or job["attempts"] >= 8
            data["history"].append({"destination": job["destination"], "event_id": job["event_id"],
                "timestamp": utcnow(), "attempt": job["attempts"], "status": "delivered" if error is None else
                "exhausted" if final else "retrying", "error": error})
            data["last_error"] = error or lost_completions(data)
            if final:
                data["pending"] = [item for item in data["pending"] if not (
                    item["destination"] == job["destination"] and item["event_id"] == job["event_id"])]
        data["history"] = data["history"][-100:]
        store.set_setting("webhook_delivery", data)


async def enqueue_test(store, vault, workspace, ident):
    async with lock(store):
        hook = next((h for h in vault.read("webhooks").get("entries", []) if h["id"] == ident), None)
        if not hook:
            raise ValueError("Webhook destination not found.")
        data = state(store)
        if len(data["pending"]) >= MAX_PENDING:
            raise ValueError("The webhook queue is full.")
        payload = {"schema": "tgwitness.webhook/1", "event_id": secrets.token_hex(32), "timestamp": utcnow(),
                   "workspace": workspace, "type": "test", "synthetic": True, "counts": {"events": 0}}
        data["pending"].append(queued(hook, payload))
        store.set_setting("webhook_delivery", data)
        return {"queued": True, "event_id": payload["event_id"], "synthetic": True}


async def export_completed(store, vault, workspace, export_id=None):
    async with lock(store):
        hooks = [h for h in vault.read("webhooks").get("entries", []) if "export" in h["events"]]
        if not hooks:
            return
        data = state(store)
        completion = {"id": export_id or secrets.token_hex(16), "observed_at": utcnow()}
        data.setdefault("deferred", [])
        if not data["deferred"] and len(data["pending"]) + len(hooks) <= MAX_PENDING:
            data["pending"] += completion_jobs(hooks, workspace, completion)
        elif len(data["deferred"]) < MAX_DEFERRED:
            data["deferred"].append(completion)
            data["last_error"] = "The delivery queue is full; export completion will be sent when it drains."
        else:
            data["lost_completions"] = data.get("lost_completions", 0) + 1
            data["last_error"] = lost_completions(data)
        store.set_setting("webhook_delivery", data)
