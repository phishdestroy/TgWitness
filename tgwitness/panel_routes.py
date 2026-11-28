import html
import re
from difflib import get_close_matches

from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse, RedirectResponse

ALIASES = {"/network-topology": "/topology", "/case-board": "/board", "/home": "/start", "/dashboard": "/start",
           "/overview": "/start", "/map": "/system-map", "/logs": "/system-log", "/log": "/system-log",
           "/fleet": "/swarm", "/swarm-dashboard": "/swarm"}


DOCUMENTS = (
    "/home", "/case-board", "/pseudo-secret", "/network-topology",
    "/settings", "/first-run", "/board", "/system-map", "/secret-chats",
    "/topology", "/swarm", "/start", "/chats", "/journal", "/sources", "/parameters", "/account", "/accounts",
    "/access", "/system-log", "/integrations", "/exports", "/extras", "/analysis", "/sealed",
    *("/extras/" + card for card in ("alerts", "evidence", "cloud", "bot", "github", "setup", "storage", "capture")),
    *("/first-run/" + str(step) for step in range(1, 6)),
    *("/settings/" + section for section in ("appearance", "level", "goal", "connection", "telegram", "chats", "collection",
                                             "protection", "notifications", "group")),
)


def missing_page(suggestions):
    links = "".join('<li><a href="' + html.escape(path, quote=True) + '">' + html.escape(path) + "</a></li>" for path in suggestions)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            "<title>Page not found · TgWitness</title><style>:root{color-scheme:light dark}"
            "body{font:16px/1.5 system-ui,sans-serif;max-width:32rem;margin:12vh auto;padding:0 20px}"
            "a{color:#2a4fd6}@media(prefers-color-scheme:dark){a{color:#8fa8ff}}</style></head><body>"
            "<h1>This page does not exist</h1><p>The address is not part of the TgWitness panel.</p>"
            + ("<p>Did you mean:</p><ul>" + links + "</ul>" if links else "")
            + '<p><a href="/start">Open the panel</a></p></body></html>')


def register(app, static):
    async def document(request):
        for name, value in request.path_params.items():
            if (not re.fullmatch(r"-?[0-9]{1,19}", value)
                    or not -(2**63) <= int(value) < 2**63
                    or int(value) == 0 or name == "seq" and int(value) < 0):
                raise HTTPException(404)
        return await static.get_response("index.html", request.scope)

    async def group_document(request):
        if not re.fullmatch(r"[a-f0-9]{32}", request.path_params["group_id"]):
            raise HTTPException(404)
        return await static.get_response("index.html", request.scope)

    async def missing(request, error):
        if (error.status_code == 404 and request.method in ("GET", "HEAD")
                and "text/html" in request.headers.get("accept", "")
                and not request.url.path.startswith(("/api/", "/profiles/"))):
            return HTMLResponse(missing_page(get_close_matches(request.url.path, DOCUMENTS, n=3, cutoff=0.4)), status_code=404,
                                headers={"Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'",
                                         "Cache-Control": "no-store"})
        return await http_exception_handler(request, error)

    app.add_exception_handler(HTTPException, missing)

    async def alias(request):
        query = request.url.query
        return RedirectResponse(ALIASES[request.url.path] + ("?" + query if query else ""), status_code=307)

    for path in ALIASES:
        app.add_route(path, alias, methods=["GET", "HEAD"], name="panel-alias")
    for path in (*DOCUMENTS, "/chats/{chat_id}", "/journal/event/{seq}"):
        if path in ALIASES:
            continue
        app.add_route(path, document, methods=["GET", "HEAD"], name="panel-document")
    app.add_route("/groups/{group_id}", group_document, methods=["GET", "HEAD"], name="panel-group-document")
