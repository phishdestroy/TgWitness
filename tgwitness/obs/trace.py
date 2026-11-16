import contextvars
import re
import secrets
import time
from collections import deque
from contextlib import asynccontextmanager, contextmanager

MEANING = ("Per-request spans for the panel API: method, route template, status and duration. "
           "Spans stay in memory and are available to the main administrator via /api/trace.")
SKIPPED = ("stream", "events", "trace")
_span_id: contextvars.ContextVar = contextvars.ContextVar("tgwitness_span_id", default=None)
_trace_id: contextvars.ContextVar = contextvars.ContextVar("tgwitness_trace_id", default=None)


def _new_id(bits=64):
    return secrets.token_hex(bits // 8)


class Span:
    __slots__ = ("trace_id", "span_id", "parent_id", "name", "start_ns", "end_ns", "attributes", "status")

    def __init__(self, name, trace_id, span_id, parent_id):
        self.trace_id, self.span_id, self.parent_id, self.name = trace_id, span_id, parent_id, name
        self.start_ns, self.end_ns = time.time_ns(), None
        self.attributes, self.status = {}, "OK"

    def set(self, key, value):
        self.attributes[str(key)] = value
        return self

    def finish(self, *, error=None):
        self.end_ns = time.time_ns()
        if error is not None:
            self.status = "ERROR"
            self.attributes["error"] = error if isinstance(error, str) else type(error).__name__

    def duration_ms(self):
        return None if self.end_ns is None else round((self.end_ns - self.start_ns) / 1_000_000, 2)

    def to_dict(self):
        return {"trace_id": self.trace_id, "span_id": self.span_id, "parent_id": self.parent_id, "name": self.name,
                "start_ns": self.start_ns, "duration_ms": self.duration_ms(), "attributes": dict(self.attributes),
                "status": self.status}


class Tracer:
    def __init__(self, *, max_spans=4096):
        self._spans = deque(maxlen=max_spans)

    def start_span(self, name, *, attributes=None):
        span = Span(name, _trace_id.get() or _new_id(128), _new_id(64), _span_id.get())
        if attributes:
            span.attributes.update(attributes)
        return span

    def finish_span(self, span, *, error=None):
        span.finish(error=error)
        self._spans.append(span)

    def _enter(self, span):
        return _trace_id.set(span.trace_id), _span_id.set(span.span_id)

    def _leave(self, tokens):
        _span_id.reset(tokens[1])
        _trace_id.reset(tokens[0])

    @asynccontextmanager
    async def span(self, name, **attributes):
        current = self.start_span(name, attributes=attributes)
        tokens = self._enter(current)
        try:
            yield current
        except BaseException as exc:
            self.finish_span(current, error=exc)
            raise
        else:
            self.finish_span(current)
        finally:
            self._leave(tokens)

    @contextmanager
    def sync_span(self, name, **attributes):
        current = self.start_span(name, attributes=attributes)
        tokens = self._enter(current)
        try:
            yield current
        except BaseException as exc:
            self.finish_span(current, error=exc)
            raise
        else:
            self.finish_span(current)
        finally:
            self._leave(tokens)

    def spans(self, profile=None):
        return [span for span in list(self._spans) if profile is None or span.attributes.get("profile") == profile]

    def public(self, profile=None, limit=50):
        spans = self.spans(profile)
        routes = {}
        for span in spans:
            if span.end_ns is not None:
                routes.setdefault(span.name, []).append(span.duration_ms())
        summary = []
        for name, values in routes.items():
            values.sort()
            summary.append({"name": name, "count": len(values), "p50_ms": values[len(values) // 2],
                            "p95_ms": values[min(len(values) - 1, int(len(values) * .95))], "max_ms": values[-1],
                            "errors": sum(1 for span in spans if span.name == name and span.status == "ERROR")})
        summary.sort(key=lambda row: -row["p95_ms"])
        return {"meaning": MEANING, "total_spans": len(spans), "routes": summary,
                "recent": [span.to_dict() for span in spans[-limit:]][::-1]}


TRACER = Tracer()


async def traced(request, call_next, profile):
    path = request.url.path
    workspace = re.match("^/profiles/([a-f0-9]{32})/", path)
    if ("/api/" not in path or path.rsplit("/api/", 1)[1].split("/", 1)[0] in SKIPPED
            or workspace and workspace[1] != profile):
        return await call_next(request)
    current = TRACER.start_span("http " + request.method, attributes={"profile": profile})
    tokens = TRACER._enter(current)
    try:
        response = await call_next(request)
    except BaseException as exc:
        route = getattr(request.scope.get("route"), "path", None) or "unmatched"
        current.name = request.method + " " + route
        current.set("http.route", route)
        TRACER.finish_span(current, error=exc)
        raise
    finally:
        TRACER._leave(tokens)
    route = getattr(request.scope.get("route"), "path", None) or "unmatched"
    current.name = request.method + " " + route
    current.set("http.route", route).set("http.status_code", response.status_code)
    TRACER.finish_span(current, error="HTTP " + str(response.status_code) if response.status_code >= 500 else None)
    return response
