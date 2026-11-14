from .chain import canonical, fingerprint
from .common import (
    Ed25519PublicKey,
    InvalidSignature,
    MAX_MEMBERS,
    MAX_RECORD_BYTES,
    MAX_SMALL_MEMBER_BYTES,
    MAX_UNCOMPRESSED_GIB,
    Path,
    VerifierTooOld,
    base64,
    hashlib,
    open_archive,
    read_manifest,
    read_member,
    strict_json,
    struct,
    zipfile,
    zlib,
)
LIVE_FORMAT = "tgwitness-live-chat-export-v1"
LIVE_START_FORMAT = "tgwitness-live-export-start-v1"
LIVE_PAGE_FORMAT = "tgwitness-live-page-v1"
LIVE_START = "live/export.json"
LIVE_TAIL = ("manifest.json", "manifest.sig")
LIVE_STATES = ("reading", "complete", "stopped")
LIVE_PAGE_LIMIT = 64 * 1024**2
LIVE_MEANING = ("Messages a chat export had read while it was still running, sealed page by page with the workspace "
                "key. It is not the finished export: attachments, reports and messages read later are not included.")


def live_archive(path):
    try:
        with open(path, "rb") as handle:
            header = handle.read(30)
            if len(header) != 30 or header[:4] != b"PK\x03\x04":
                return False
            return handle.read(struct.unpack("<H", header[26:28])[0]) == LIVE_START.encode("ascii")
    except OSError:
        return False


def live_zip64(extra):
    at = 0
    while at + 4 <= len(extra):
        field, length = struct.unpack("<HH", extra[at:at + 4])
        body = extra[at + 4:at + 4 + length]
        if field == 1:
            return list(struct.unpack("<" + "Q" * (len(body) // 8), body[:len(body) // 8 * 8]))
        at += 4 + length
    return []


class LiveSalvage:
    def __init__(self, path):
        self.path, self.members, self.ends, position = Path(path), {}, {}, 0
        with open(self.path, "rb") as handle:
            self.size = handle.seek(0, 2)
            while position + 30 <= self.size and len(self.members) < MAX_MEMBERS:
                handle.seek(position)
                (signature, _, flags, method, _, _, crc, packed, plain, name_length,
                 extra_length) = struct.unpack("<4sHHHHHIIIHH", handle.read(30))
                name, extra = handle.read(name_length), handle.read(extra_length)
                if signature != b"PK\x03\x04" or flags & 9 or len(name) != name_length or len(extra) != extra_length:
                    break
                if 0xFFFFFFFF in (packed, plain):
                    wide = live_zip64(extra)
                    if plain == 0xFFFFFFFF:
                        plain, wide = (wide[0], wide[1:]) if wide else (None, [])
                    if packed == 0xFFFFFFFF:
                        packed = wide[0] if wide else None
                    if plain is None or packed is None:
                        break
                start = position + 30 + name_length + extra_length
                try:
                    text = name.decode("utf-8")
                except UnicodeDecodeError:
                    break
                if start + packed > self.size or text in self.members:
                    break
                self.members[text] = (start, packed, plain, method, crc)
                position = self.ends[text] = start + packed

    def read(self, name, limit=MAX_SMALL_MEMBER_BYTES):
        start, packed, plain, method, crc = self.members[name]
        if plain > limit:
            raise ValueError(name + " exceeds the verifier's size limit for this member")
        with open(self.path, "rb") as handle:
            handle.seek(start)
            data = handle.read(packed)
        if method == 8:
            inflater = zlib.decompressobj(-15)
            data = inflater.decompress(data, plain + 1)
            if not inflater.eof:
                raise ValueError("Damaged archive member: " + name)
        elif method != 0:
            raise ValueError("Unsupported compression in archive member: " + name)
        if len(data) != plain or zlib.crc32(data) != crc:
            raise ValueError("Damaged archive member: " + name)
        return data


def live_signed(data, public=None):
    envelope = strict_json(data)
    if (not isinstance(envelope, dict) or set(envelope) != {"statement", "public_key", "signature"}
            or not isinstance(envelope["statement"], dict) or not isinstance(envelope["public_key"], str)):
        raise ValueError("Invalid signed record in the live archive")
    if public is not None and envelope["public_key"] != public:
        raise ValueError("A live archive record is signed by another key")
    Ed25519PublicKey.from_public_bytes(base64.b64decode(envelope["public_key"], validate=True)).verify(
        base64.b64decode(envelope["signature"], validate=True), canonical(envelope["statement"]))
    return envelope["statement"], envelope["public_key"]


def live_name(number, suffix):
    return ("live/seals/" if suffix == ".seal" else "live/pages/") + str(number).zfill(6) + (
        ".json" if suffix == ".seal" else suffix)


def live_page(data, statement, seen):
    ids = []
    lines = data.split(b"\n")
    if lines[-1]:
        raise ValueError("A live page ends inside a record")
    for line in lines[:-1]:
        if len(line) > MAX_RECORD_BYTES:
            raise ValueError("A record exceeds the verifier's size limit")
        record = strict_json(line)
        if not isinstance(record, dict):
            raise ValueError("A live page holds a value that is not a message record")
        number = record.get("id")
        if type(number) is int:
            if number in seen:
                raise ValueError("Duplicate message ID in the live archive: " + str(number))
            seen.add(number)
            ids.append(number)
    found = {"messages": len(lines) - 1, "first_id": ids[0] if ids else None, "last_id": ids[-1] if ids else None,
             "low": min(ids) if ids else None, "high": max(ids) if ids else None}
    if any(statement.get(key) != value for key, value in found.items()):
        raise ValueError("A live page differs from its seal")
    return found


def verify_live_export(path, expected_fingerprint=None, max_gib=None):
    limit = MAX_UNCOMPRESSED_GIB if max_gib is None else max_gib
    archive = salvage = reason = None
    try:
        archive = open_archive(path, max_gib)
    except (zipfile.BadZipFile, ValueError, OSError, EOFError, struct.error) as exc:
        if "size limit" in str(exc):
            raise
        salvage, reason = LiveSalvage(path), type(exc).__name__ + ": " + str(exc)
    try:
        if archive is not None:
            names = set(archive.namelist())

            def read(name, most=MAX_SMALL_MEMBER_BYTES):
                try:
                    return read_member(archive, name, most)
                except (zipfile.BadZipFile, zlib.error, EOFError):
                    raise ValueError("Damaged archive member: " + name) from None
        else:
            names = set(salvage.members)
            if sum(member[2] for member in salvage.members.values()) > limit * 1024**3:
                raise ValueError("Bundle exceeds the verifier's size limit; raise it with --max-gib")
            read = salvage.read
        if LIVE_START not in names:
            raise ValueError("This is not a live chat export: live/export.json is missing")
        opening = read(LIVE_START)
        start, public = live_signed(opening)
        if (start.get("format") != LIVE_START_FORMAT or start.get("archive_format") != LIVE_FORMAT
                or start.get("page_format") != LIVE_PAGE_FORMAT):
            raise VerifierTooOld("Unsupported live chat export format")
        fp = fingerprint(public)
        if expected_fingerprint and fp != expected_fingerprint:
            raise ValueError("Public key differs from the independently trusted fingerprint")
        files, chat = start.get("files"), start.get("chat")
        if (not isinstance(files, dict) or not isinstance(chat, dict) or type(chat.get("id")) is not int
                or not isinstance(start.get("export_id"), str) or LIVE_START in files or set(LIVE_TAIL) & set(files)):
            raise ValueError("Invalid live export start record")
        for name, digest in files.items():
            if name not in names or hashlib.sha256(read(name)).hexdigest() != digest:
                raise ValueError("File hash mismatch: " + name)
        head, covered, seen = hashlib.sha256(opening).hexdigest(), {LIVE_START, *files}, set()
        pages = messages = 0
        low = high = last = stopped = None
        while live_name(pages + 1, ".seal") in names:
            number, seal = pages + 1, live_name(pages + 1, ".seal")
            try:
                data = read(seal)
                statement, _ = live_signed(data, public)
                listed = statement.get("files")
                if (statement.get("format") != LIVE_PAGE_FORMAT or statement.get("page") != number
                        or statement.get("previous_sha256") != head or statement.get("export_id") != start["export_id"]
                        or statement.get("chat_id") != chat["id"] or not isinstance(listed, dict)
                        or set(listed) != {live_name(number, ".jsonl"), live_name(number, ".html")}):
                    raise ValueError("Live page seal " + str(number) + " does not follow the page before it")
                for name, digest in listed.items():
                    content = read(name, LIVE_PAGE_LIMIT) if name in names else None
                    if content is None or hashlib.sha256(content).hexdigest() != digest:
                        raise ValueError("File hash mismatch: " + name)
                    if name.endswith(".jsonl"):
                        found = live_page(content, statement, seen)
                if statement.get("total_messages") != messages + found["messages"]:
                    raise ValueError("Live page seal " + str(number) + " counts a different total")
            except (ValueError, InvalidSignature, KeyError, zlib.error) as exc:
                if archive is not None:
                    raise
                stopped = type(exc).__name__ + ": " + str(exc)
                break
            covered.update((seal, *listed))
            head, pages, messages, last = hashlib.sha256(data).hexdigest(), number, statement["total_messages"], statement
            low = found["low"] if low is None or found["low"] is not None and found["low"] < low else low
            high = found["high"] if high is None or found["high"] is not None and found["high"] > high else high
        if archive is not None:
            manifest = read_manifest(archive)
            if (manifest.get("format") != LIVE_FORMAT or manifest.get("public_key") != public
                    or manifest.get("head_sha256") != head or manifest.get("pages") != pages
                    or manifest.get("messages") != messages or manifest.get("export_id") != start["export_id"]
                    or manifest.get("chat") != chat or manifest.get("files") != files
                    or manifest.get("state") not in LIVE_STATES):
                raise ValueError("manifest.json differs from the sealed pages")
            if names != covered | set(LIVE_TAIL):
                raise ValueError("Unexpected or missing bundle members")
            state, stop, sealed_at, salvaged = manifest["state"], manifest.get("stop"), manifest.get("sealed_at"), None
        else:
            end = max(salvage.ends[name] for name in covered)
            state, stop, sealed_at = "interrupted", None, (last or start).get("sealed_at", start.get("started_at"))
            salvaged = {"reason": reason, "unsealed_members": len(names - covered - set(LIVE_TAIL)),
                        "unsealed_bytes": salvage.size - end, "stopped_at": stopped}
        return {"format": LIVE_FORMAT, "fingerprint": fp, "key_pinned": bool(expected_fingerprint),
                "export_id": start["export_id"], "chat": chat, "started_at": start.get("started_at"),
                "sealed_at": sealed_at, "state": state, "stop": stop, "pages": pages, "message_count": messages,
                "low": low, "high": high, "files_checked": len(covered) + (len(LIVE_TAIL) if archive else 0),
                "salvaged": salvaged, "producer": start.get("producer"), "meaning": LIVE_MEANING}
    finally:
        if archive is not None:
            archive.close()
