import time
from pathlib import Path

from starlette.responses import FileResponse

from .workers import complete_in_thread

DELIVERY_HEADER = "X-TgWitness-Delivery"
HOLD_SECONDS = 6 * 3600
HOLD_LIMIT = 200


def delivery(app, request, export_id, mark):
    """Return the mark to run after a complete response, or hold it for the panel's receipt.

    The operating system buffers several megabytes of a response, so a server cannot tell whether a client kept the
    whole file. The panel asks to confirm the download itself; the mark then waits for that receipt."""
    if mark is None or request is None or not export_id or request.headers.get(DELIVERY_HEADER) != "confirm":
        return mark, {}
    held, now = getattr(app.state, "held_deliveries", None), time.monotonic()
    if held is None:
        held = app.state.held_deliveries = {}
    for key, (until, _) in list(held.items()):
        if until < now:
            held.pop(key, None)
    while len(held) >= HOLD_LIMIT:
        held.pop(next(iter(held)))
    held[export_id] = (now + HOLD_SECONDS, mark)
    return None, {DELIVERY_HEADER: "held"}


def confirm_delivery(app, export_id):
    held = getattr(app.state, "held_deliveries", None) or {}
    until, mark = held.pop(export_id, (0, None))
    if mark is None or until < time.monotonic():
        return False
    mark()
    return True


async def build_file(function):
    path = None

    def build():
        nonlocal path
        path = function()
        return path

    try:
        return await complete_in_thread(build)
    except BaseException:
        if path is not None:
            Path(path).unlink(missing_ok=True)
        raise


class TemporaryDownload(FileResponse):
    def __init__(self, path, *, delivered=None, **kwargs):
        super().__init__(path, **kwargs)
        self.delivered = delivered

    async def __call__(self, scope, receive, send):
        state = {"status": None, "sent": False, "gone": False}

        async def watched_send(message):
            if message["type"] == "http.response.start":
                state["status"] = message.get("status")
            await send(message)
            if message["type"] == "http.response.pathsend" or (
                    message["type"] == "http.response.body" and not message.get("more_body", False)):
                state["sent"] = True

        async def watched_receive():
            message = await receive()
            if message["type"] == "http.disconnect" and not state["sent"]:
                state["gone"] = True
            return message

        try:
            await super().__call__(scope, watched_receive, watched_send)
        finally:
            Path(self.path).unlink(missing_ok=True)
        if self.delivered is not None and state["sent"] and not state["gone"] and state["status"] == 200 \
                and scope.get("method") != "HEAD":
            self.delivered()


class RetainedDownload(FileResponse):
    def __init__(self, path, *, release, **kwargs):
        super().__init__(path, **kwargs)
        self.release = release

    async def __call__(self, scope, receive, send):
        try:
            await super().__call__(scope, receive, send)
        finally:
            self.release()
