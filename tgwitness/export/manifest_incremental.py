import hashlib

from ..store import canonical, utcnow
from ..verify import fingerprint

FORMAT = "tgwitness-live-chat-export-v1"
START_FORMAT = "tgwitness-live-export-start-v1"
PAGE_FORMAT = "tgwitness-live-page-v1"
START_FILE = "live/export.json"
MEANING = ("Messages read so far by a chat export that was still running when this archive was sealed. Each page is "
           "signed with the workspace key as soon as it is written and names the page before it. Pages hold messages "
           "in reading order, newest first. The finished export adds attachments, the full report and its own "
           "signature.")


def page_name(number, suffix):
    return "live/pages/" + str(number).zfill(6) + suffix


def seal_name(number):
    return "live/seals/" + str(number).zfill(6) + ".json"


class SealChain:
    def __init__(self, vault, identity, producer):
        self.vault, self.identity, self.producer = vault, identity, producer
        self.started_at = None
        self.head = self.head_name = None
        self.pages = self.messages = 0
        self.low = self.high = None
        self.files = {}

    def envelope(self, statement):
        return canonical({"statement": statement, "public_key": self.vault.public_key,
                          "signature": self.vault.sign(canonical(statement))})

    def start(self, files, started_at):
        self.started_at, self.files = started_at, dict(files)
        data = self.envelope({"format": START_FORMAT, "archive_format": FORMAT, "page_format": PAGE_FORMAT,
                              **self.identity, "started_at": started_at, "files": self.files,
                              "producer": self.producer})
        self.head, self.head_name = hashlib.sha256(data).hexdigest(), START_FILE
        return data

    def page(self, number, files, facts):
        if number != self.pages + 1:
            raise ValueError("Live pages are sealed in order.")
        total = self.messages + facts["messages"]
        data = self.envelope({"format": PAGE_FORMAT, "export_id": self.identity["export_id"],
                              "chat_id": self.identity["chat"]["id"], "page": number,
                              "previous_sha256": self.head, "files": files, **facts,
                              "total_messages": total, "sealed_at": utcnow()})
        self.head, self.head_name, self.pages, self.messages = hashlib.sha256(data).hexdigest(), seal_name(number), number, total
        for value in (facts.get("low"), facts.get("high")):
            if type(value) is int:
                self.low = value if self.low is None else min(self.low, value)
                self.high = value if self.high is None else max(self.high, value)
        return data

    def manifest(self, state, stop=None):
        manifest = {"format": FORMAT, "public_key": self.vault.public_key,
                    "fingerprint": fingerprint(self.vault.public_key), **self.identity,
                    "started_at": self.started_at, "sealed_at": utcnow(), "state": state,
                    "pages": self.pages, "messages": self.messages, "low": self.low, "high": self.high,
                    "head": self.head_name, "head_sha256": self.head, "files": self.files,
                    "meaning": MEANING, "producer": self.producer}
        if stop:
            manifest["stop"] = stop
        data = canonical(manifest)
        return [("manifest.json", data), ("manifest.sig", self.vault.sign(data).encode("ascii"))]
