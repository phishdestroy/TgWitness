import asyncio
import contextvars
import logging
import secrets
import time
from contextlib import asynccontextmanager, contextmanager

MEANING = ("OpenTelemetry-compatible per-task spans. When OTEL_EXPORTER_OTLP_ENDPOINT is set, spans are "
           "exported to that collector. Otherwise they are recorded in memory and available via /api/trace. "
           "A local Jaeger-compatible endpoint on loopback is used when TGWITNESS_JAEGER_HOST is set.")
SERVICE_NAME = "tgwitness"
_span_id: contextvars.ContextVar = contextvars.ContextVar("tgwitness_span_id", default=None)
_trace_id: contextvars.ContextVar = contextvars.ContextVar("tgwitness_trace_id", default=None)
log = logging.getLogger(__name__)


def _new_id(bits=64):
    return secrets.token_hex(bits // 8)


def _now_ns():
    return time.time_ns()


class Span:
    __slots__ = ("trace_id", "span_id", "parent_id", "name", "start_ns", "end_ns",
                 "attributes", "status", "events")

    def __init__(self, name, trace_id, span_id, parent_id):
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_id = parent_id
        self.name = name
        self.start_ns = _now_ns()
        self.end_ns = None
        self.attributes: dict = {}
        self.status = "OK"
        self.events: list = []

    def set(self, key, value):
        self.attributes[str(key)] = value
        return self

    def add_event(self, name, attributes=None):
        self.events.append({"name": name, "time_ns": _now_ns(), "attributes": attributes or {}})

    def finish(self, *, error=None):
        self.end_ns = _now_ns()
        if error is not None:
            self.status = "ERROR"
            self.attributes["error"] = str(error)[:200]

    def duration_ms(self):
        if self.end_ns is None:
            return None
        return round((self.end_ns - self.start_ns) / 1_000_000, 2)

    def to_dict(self):
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "start_ns": self.start_ns,
            "end_ns": self.end_ns,
            "duration_ms": self.duration_ms(),
            "attributes": dict(self.attributes),
            "status": self.status,
            "events": list(self.events),
        }


class Tracer:
    def __init__(self, *, max_spans=4096, exporter=None):
        self._spans: list[Span] = []
        self._max = max_spans
        self._exporter = exporter
        self._lock = None
        self._loop = None

    def _safe_lock(self):
        loop = asyncio.get_running_loop() if asyncio.get_event_loop().is_running() else None
        if loop is not self._loop:
            self._loop, self._lock = loop, asyncio.Lock() if loop else None
        return self._lock

    def start_span(self, name, *, trace_id=None, parent_id=None, attributes=None):
        parent = _span_id.get()
        tid = trace_id or _trace_id.get() or _new_id(128)
        sid = _new_id(64)
        span = Span(name, tid, sid, parent_id or parent)
        if attributes:
            span.attributes.update(attributes)
        return span

    def finish_span(self, span: Span, *, error=None):
        span.finish(error=error)
        self._store(span)
        if self._exporter:
            try:
                self._exporter(span)
            except Exception:
                pass

    def _store(self, span):
        while len(self._spans) >= self._max:
            self._spans.pop(0)
        self._spans.append(span)

    @asynccontextmanager
    async def span(self, name, **attributes):
        s = self.start_span(name, attributes=attributes or None)
        token_tid = _trace_id.set(s.trace_id)
        token_sid = _span_id.set(s.span_id)
        try:
            yield s
        except Exception as exc:
            self.finish_span(s, error=exc)
            raise
        else:
            self.finish_span(s)
        finally:
            _span_id.reset(token_sid)
            _trace_id.reset(token_tid)

    @contextmanager
    def sync_span(self, name, **attributes):
        s = self.start_span(name, attributes=attributes or None)
        token_tid = _trace_id.set(s.trace_id)
        token_sid = _span_id.set(s.span_id)
        try:
            yield s
        except Exception as exc:
            self.finish_span(s, error=exc)
            raise
        else:
            self.finish_span(s)
        finally:
            _span_id.reset(token_sid)
            _trace_id.reset(token_tid)

    def recent(self, limit=100):
        return [s.to_dict() for s in self._spans[-limit:]]

    def by_trace(self, trace_id):
        return [s.to_dict() for s in self._spans if s.trace_id == trace_id]

    def public(self, limit=20):
        traces: dict[str, list] = {}
        for s in self._spans[-500:]:
            traces.setdefault(s.trace_id, []).append(s)
        result = []
        for tid, spans in sorted(traces.items(),
                                 key=lambda kv: max(s.start_ns for s in kv[1]), reverse=True)[:limit]:
            result.append({
                "trace_id": tid,
                "spans": len(spans),
                "root_name": next((s.name for s in spans if s.parent_id is None), spans[0].name),
                "start_ms": spans[0].start_ns // 1_000_000,
                "duration_ms": max(s.duration_ms() or 0 for s in spans),
                "status": "ERROR" if any(s.status == "ERROR" for s in spans) else "OK",
            })
        return {"traces": result, "total_spans": len(self._spans)}


TRACER = Tracer()
