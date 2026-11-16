import hashlib
import re
from typing import Literal

import qrcode
from pydantic import BaseModel, ConfigDict, Field

from .store import canonical, utcnow
from .verify import fingerprint

FORMAT = "tgwitness-image-attestation-v1"
MEANING = ("TgWitness rendered each listed PNG page from the listed signed journal records and signed this "
           "statement with the workspace key. It binds every page's SHA-256 to the records the page shows. "
           "It does not show what Telegram displayed to anyone and does not replace the evidence archive.")
THEMES = ("light", "dark", "classic")
MAX_PAGES = 200
MAX_RECORDS = 20000
DIGEST = re.compile(r"[0-9a-f]{64}")


class ImagePage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    records: list[int] = Field(min_length=1, max_length=MAX_RECORDS)


class ImageAttestation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    style: Literal["light", "dark", "classic"]
    pages: list[ImagePage] = Field(min_length=1, max_length=MAX_PAGES)


class QrText(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=1, max_length=300)


def qr_rows(text):
    code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    code.add_data(text)
    code.make(fit=True)
    return ["".join("1" if cell else "0" for cell in row) for row in code.get_matrix()]


def attest(store, vault, chat_id, pages, theme, account_id=None):
    if theme not in THEMES:
        raise ValueError("Choose the light, dark or classic style.")
    if not 1 <= len(pages) <= MAX_PAGES:
        raise ValueError("Sign between 1 and %d pages at once." % MAX_PAGES)
    wanted = sorted({seq for page in pages for seq in page["records"]})
    if not wanted or len(wanted) > MAX_RECORDS:
        raise ValueError("Each image needs saved records; at most %d records can be signed at once." % MAX_RECORDS)
    if any(not DIGEST.fullmatch(page["sha256"]) for page in pages):
        raise ValueError("Every page needs its SHA-256.")
    found = {}
    with store.reading() as db:
        for start in range(0, len(wanted), 500):
            part = wanted[start:start + 500]
            for row in db.execute("SELECT seq, hash, kind, message_id FROM events WHERE chat_id=? AND seq IN (%s)"
                                  % ",".join("?" * len(part)), (chat_id, *part)):
                found[row[0]] = {"seq": row[0], "hash": row[1], "kind": row[2], "message_id": row[3]}
        head = db.execute("SELECT seq, hash FROM events ORDER BY seq DESC LIMIT 1").fetchone()
    if len(found) != len(wanted):
        raise ValueError("Some records do not belong to this chat. Refresh the chat and create the image again.")
    title = next((t["title"] for t in store.targets() if t["chat_id"] == chat_id), None)
    statement = {"format": FORMAT, "meaning": MEANING, "created_at": utcnow(),
                 "chat": {"id": chat_id, "title": title}, "account_id": account_id, "style": theme,
                 "journal_head": {"seq": head[0], "hash": head[1]} if head else None,
                 "pages": [{"page": index, "png_sha256": page["sha256"],
                            "records": [found[seq] for seq in sorted(set(page["records"]))]}
                           for index, page in enumerate(pages, 1)]}
    digest = hashlib.sha256(canonical(statement)).hexdigest()
    event = store.append("export.image_attested", {"statement_sha256": digest, "pages": len(pages),
                                                    "records": len(wanted), "style": theme}, chat_id=chat_id)
    return {"statement": statement, "signature": vault.sign(canonical(statement)), "public_key": vault.public_key,
            "fingerprint": fingerprint(vault.public_key), "recorded_as": {"seq": event["seq"], "hash": event["hash"]}}
