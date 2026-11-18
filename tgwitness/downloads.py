from pathlib import Path

from starlette.responses import FileResponse

from .workers import complete_in_thread


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
