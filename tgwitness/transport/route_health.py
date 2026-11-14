import asyncio
import os
import time

from telethon.network import MTProtoPlainSender
from telethon.tl.functions import ReqPqMultiRequest
from telethon.tl.types import ResPQ

from ..proxy_catalog import PROBE_DC, _Loggers
from .burst import HANDSHAKES

FORMAT = "tgwitness-route-health-v1"
METHOD = "req_pq_multi"
SLOW_MS = 5000
RECOVER_MS = 4000
ALPHA = 0.4
SAMPLES = 5
CONSECUTIVE = 3
DOWN_AFTER = 2
TIMEOUT = 10
AUTO_REROLL_SECONDS = 1800
MEANING = ("Time to open a Telegram transport connection through this route plus one unauthenticated MTProto "
           "round trip. The check creates no authorization key and uses no account.")
RULE = ("A route is slow when the moving average of these checks exceeds the threshold or three consecutive checks "
        "exceed it, and unavailable after two failed checks in a row.")


def home_dc(client):
    session = getattr(client, "session", None)
    dc_id, host, port = (getattr(session, name, None) for name in ("dc_id", "server_address", "port"))
    if type(dc_id) is int and 0 < dc_id < 1000 and isinstance(host, str) and host and type(port) is int:
        return dc_id, host, port
    return PROBE_DC


async def handshake(route, dc=None, timeout=TIMEOUT):
    async with HANDSHAKES.turn("route_check"):
        return await _handshake(route, dc, timeout)


async def _handshake(route, dc, timeout):
    dc_id, host, port = dc or PROBE_DC
    options = route.client_options()
    connection = options["connection"](host, port, dc_id, loggers=_Loggers(), proxy=options.get("proxy"))
    started = time.monotonic()
    try:
        await asyncio.wait_for(connection.connect(timeout=timeout), timeout + 3)
        opened = time.monotonic()
        nonce = int.from_bytes(os.urandom(16), "big", signed=True)
        answer = await asyncio.wait_for(MTProtoPlainSender(connection, loggers=_Loggers()).send(
            ReqPqMultiRequest(nonce)), timeout)
        answered = time.monotonic()
    finally:
        await connection.disconnect()
    if not isinstance(answer, ResPQ) or answer.nonce != nonce:
        raise ConnectionError("unexpected handshake answer")
    connect_ms = max(1, round((opened - started) * 1000))
    rtt_ms = max(1, round((answered - opened) * 1000))
    return {"latency_ms": connect_ms + rtt_ms, "connect_ms": connect_ms, "rtt_ms": rtt_ms, "dc": dc_id,
            "method": METHOD}


class RouteHealth:
    def __init__(self, store, clock=time.time):
        self.store, self.clock = store, clock

    @staticmethod
    def blank(revision=None, reroll=None):
        return {"format": FORMAT, "revision": revision, "status": "unknown", "since": None, "samples": [],
                "ema_ms": None, "consecutive_slow": 0, "consecutive_failures": 0,
                "reroll": reroll or {"at": None, "count": 0, "confirm": False, "trigger": None}}

    def state(self):
        value = self.store.get_setting("route_health", None)
        if not isinstance(value, dict) or value.get("format") != FORMAT:
            return self.blank()
        return value

    def record(self, result, revision):
        state = self.state()
        if state.get("revision") != revision:
            state = self.blank(revision, state.get("reroll"))
        before, now = state["status"], self.clock()
        if result.get("telegram_connected"):
            latency = int(result["latency_ms"])
            state["samples"] = [*state["samples"], {"at": now, "ms": latency, "connect_ms": result.get("connect_ms"),
                                                    "rtt_ms": result.get("rtt_ms")}][-SAMPLES:]
            ema = state["ema_ms"]
            state["ema_ms"] = round(latency if ema is None else ALPHA * latency + (1 - ALPHA) * ema)
            state["consecutive_slow"] = state["consecutive_slow"] + 1 if latency > SLOW_MS else 0
            state["consecutive_failures"] = 0
            if state["ema_ms"] > SLOW_MS or state["consecutive_slow"] >= CONSECUTIVE:
                status = "slow"
            elif before in ("slow", "down") and state["ema_ms"] > RECOVER_MS:
                status = "slow"
            else:
                status = "ok"
        else:
            state["samples"] = [*state["samples"], {"at": now, "ms": None,
                                                    "error": result.get("error_type")}][-SAMPLES:]
            state["consecutive_failures"] += 1
            status = "down" if state["consecutive_failures"] >= DOWN_AFTER else before
        state["status"] = status
        if status != before:
            state["since"] = now
            if status == "ok":
                state["reroll"] = {**state["reroll"], "confirm": False}
        self.store.set_setting("route_health", state)
        return before, status, state

    def reroll_due(self, mode):
        state = self.state()
        reroll = state["reroll"]
        return (mode == "warp" and state["status"] in ("slow", "down") and not reroll.get("confirm")
                and (reroll.get("at") is None or self.clock() - reroll["at"] >= AUTO_REROLL_SECONDS))

    def rerolled(self, trigger):
        state = self.state()
        reroll = state["reroll"]
        state.update(samples=[], ema_ms=None, consecutive_slow=0, consecutive_failures=0,
                     reroll={"at": self.clock(), "count": reroll.get("count", 0) + 1, "trigger": trigger,
                             "confirm": trigger == "automatic"})
        self.store.set_setting("route_health", state)

    def transition(self, mode, before, status, state):
        samples = [sample.get("ms") for sample in state["samples"]]
        last = state["samples"][-1] if state["samples"] else {}
        if status in ("slow", "down") and status != before:
            return "network.slow_route", {
                "mode": mode, "status": status, "ema_ms": state["ema_ms"], "threshold_ms": SLOW_MS,
                "samples_ms": samples, "connect_ms": last.get("connect_ms"), "rtt_ms": last.get("rtt_ms"),
                "method": METHOD, "meaning": MEANING + " " + RULE}
        if status == "ok" and before in ("slow", "down"):
            return "network.route_recovered", {
                "mode": mode, "previous_status": before, "ema_ms": state["ema_ms"], "threshold_ms": SLOW_MS,
                "samples_ms": samples, "method": METHOD, "meaning": MEANING}
        return None

    def public(self, mode):
        state = self.state()
        measured = [sample for sample in state["samples"] if sample.get("ms") is not None]
        last = measured[-1] if measured else {}
        reroll = state["reroll"]
        automatic = None
        if mode == "warp" and not reroll.get("confirm"):
            automatic = reroll["at"] + AUTO_REROLL_SECONDS if reroll.get("at") else 0
        return {"status": state["status"], "since": state["since"], "ema_ms": state["ema_ms"],
                "last_ms": last.get("ms"), "connect_ms": last.get("connect_ms"), "rtt_ms": last.get("rtt_ms"),
                "samples": [sample.get("ms") for sample in state["samples"]], "threshold_ms": SLOW_MS,
                "method": METHOD, "reroll": {"at": reroll.get("at"), "count": reroll.get("count", 0),
                                             "trigger": reroll.get("trigger"),
                                             "confirm_needed": bool(reroll.get("confirm")),
                                             "next_automatic_at": automatic}}
