import base64
import hashlib
import html
import json
import re
import sqlite3
import struct
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .format import ZERO, canonical, decode, digest, utcnow

FORMAT = "tgwitness-capture-ayugram-v1"
REPORT_FORMAT = "tgwitness-capture-ayugram-reconciliation-v1"
DESKTOP = "AyuGram/AyuGramDesktop 0f2a31bb420de98f331990432265b131b8d836b5"
ANDROID = "AyuGram/AyuGram4A 7013145676d36d82ee13c02a89f72097b7490dcd, Room schema 21"
ANDROID_IDENTITY = "75ee43cc23a4c250996ef1dd53c63ed0"
REFERENCE_SCHEMAS = {"17a35fc698bbb19edb99e9ef84a9181fa75348b8f7bdc066ebf27532c1f1ae43":
                     "AyuGram Desktop 0f2a31b storage definition after sync_schema"}
TABLES = ("DeletedMessage", "EditedMessage", "DeletedDialog", "SpyMessageRead", "SpyMessageContentsRead")
MESSAGE_TABLES = ("DeletedMessage", "EditedMessage")
SERVICE_TABLES = {"SchemaVersion", "RegexFilter", "RegexFilterGlobalExclusion", "sqlite_sequence",
                  "room_master_table", "android_metadata"}
MESSAGE_COLUMNS = ("fakeId", "userId", "dialogId", "groupedId", "peerId", "fromId", "topicId", "messageId", "date",
                   "flags", "editDate", "views", "fwdFlags", "fwdFromId", "fwdName", "fwdDate", "fwdPostAuthor",
                   "replyFlags", "replyMessageId", "replyPeerId", "replyTopId", "replyForumTopic", "replySerialized",
                   "entityCreateDate", "text", "textEntities", "mediaPath", "hqThumbPath", "documentType",
                   "documentSerialized", "thumbsSerialized", "documentAttributesSerialized", "mimeType")
SPY_COLUMNS = ("fakeId", "userId", "dialogId", "messageId", "entityCreateDate")
COLUMNS = {"DeletedMessage": MESSAGE_COLUMNS, "EditedMessage": MESSAGE_COLUMNS,
           "DeletedDialog": ("fakeId", "userId", "dialogId", "peerId", "folderId", "topMessage", "lastMessageDate",
                             "flags", "entityCreateDate"),
           "SpyMessageRead": SPY_COLUMNS, "SpyMessageContentsRead": SPY_COLUMNS}
CHANNEL_BASE = 1000000000000
SIDECARS = ("-wal", "-shm", "-journal")
ROTATED = re.compile(r"ayudata_(\d+)\.db\Z")
LOCAL = "clock of the computer running AyuGram when it wrote this row"
DATES = {
    "DeletedMessage": {
        "date": "message date supplied by Telegram",
        "editDate": "last edit date supplied by Telegram; for a message never edited, the clock of the computer "
                    "running AyuGram when the deletion was saved",
        "entityCreateDate": LOCAL},
    "EditedMessage": {
        "date": "message date supplied by Telegram",
        "editDate": "date of this earlier version: Telegram's edit date when the version was itself an edit; "
                    "otherwise the clock of the computer running AyuGram when the next edit arrived",
        "entityCreateDate": LOCAL},
    "DeletedDialog": {"lastMessageDate": "date of the last message supplied by Telegram", "entityCreateDate": LOCAL},
    "SpyMessageRead": {"entityCreateDate": LOCAL},
    "SpyMessageContentsRead": {"entityCreateDate": LOCAL},
}
TABLE_MEANING = {
    "DeletedMessage": "message kept by AyuGram after a deletion notice; text as it was in the client's memory",
    "EditedMessage": "earlier version of a message, saved by AyuGram before it applied an edit",
    "DeletedDialog": "deleted chat (not written by AyuGram Desktop at the reference commit)",
    "SpyMessageRead": "read receipt (not written by AyuGram Desktop at the reference commit)",
    "SpyMessageContentsRead": "contents-read receipt (not written by AyuGram Desktop at the reference commit)",
}
LIMITS = [
    "AyuGram's database is a local file that the AyuGram user and other programs can change; rows can be removed "
    "in the client (one message or a whole chat) and the file can be replaced.",
    "Dates written by AyuGram itself (entityCreateDate, and editDate of a version that was never edited) come from "
    "the clock of the computer running AyuGram.",
    "AyuGram rows carry no hash or signature made at the time of the event; the recorder signs only the copy it made "
    "later.",
    "AyuGram Desktop keeps no media of deleted messages, skips messages without text and records a deletion only for "
    "messages that were loaded in its memory during that run.",
    "A negative AyuGram chat ID is shared by a basic group and a channel with the same number.",
    "An AyuGram row is not proof on its own; it is a second, unsigned observation to compare with the signed journal.",
]
STANDING = "second observer without a signature at the time of the event; corroboration only, not proof on its own"
INTERPRETED_MEANING = ("Database copy interpreted: file hash, schema and row counts per table. Rows are AyuGram's own "
                       "local records; they were not signed when AyuGram wrote them.")
REMOVED_MEANING = ("These fakeId values were present in the earlier copy and are absent from this one. AyuGram assigns "
                   "fakeId by AUTOINCREMENT and never reuses it in one file, so the rows were removed inside AyuGram "
                   "(single message or whole chat) or by another program. Changed rows kept their fakeId but not "
                   "their content.")
ROTATION_MEANING = ("The AUTOINCREMENT counters went down, so the database file was replaced. AyuGram renames its "
                    "database to ayudata_<unixtime>.db when a schema migration fails and starts a new one; the "
                    "unixtime comes from the clock of the computer running AyuGram. Rows of the earlier copy are "
                    "compared with the rotated file when the recorder copied it.")
OUTCOMES = ("matched", "ayugram_only", "tgwitness_only", "conflict", "ambiguous")
LABELS = {
    "matched": "Both observers agree on the deletion or on the text of that version",
    "ayugram_only": "Only AyuGram has it: observer without a signature at the time of the event",
    "tgwitness_only": "Only the TgWitness journal has it",
    "conflict": "Same message, different text for the same version; both values are shown",
    "ambiguous": "Chat not resolved: the negative AyuGram ID fits a basic group and a channel, and the journal does "
                 "not single out one of them",
}
REASONS = {
    "own": "own message: AyuGram Desktop does not save earlier versions of messages sent by this account",
    "same_text": "the edit did not change the text: AyuGram Desktop saves a version only when the text changes",
    "no_text": "no text in the journal's version: AyuGram Desktop skips messages without text, including media only",
    "memory": "AyuGram Desktop records a deletion only for a message loaded in its memory during that run",
    "removed": "the row may have been removed inside AyuGram before the copy was made",
}
JOURNAL_FIELDS = ("seq", "observed_at", "source_at", "kind", "chat_id", "message_id", "actor_id", "payload",
                  "previous_hash")
VERSION_KINDS = ("message.new", "message.snapshot", "message.recovered", "message.edited")
PLAIN_ENTITIES = {0xbb92ba95: "unknown", 0xfa04579d: "mention", 0x6f635b0d: "hashtag", 0x6cef8ac7: "bot_command",
                  0x6ed02538: "url", 0x64e475c2: "email", 0xbd610bc9: "bold", 0x826f8b60: "italic",
                  0x28a20571: "code", 0x9b69e34b: "phone", 0x4c4e743f: "cashtag", 0x9c4e7e8b: "underline",
                  0xbf0693d4: "strike", 0x761e6af4: "bank_card", 0x32ca960f: "spoiler", 0x71777116: "diff_insert",
                  0x0652c1c5: "diff_delete"}
VALUE_ENTITIES = {0x73924be0: ("pre", "language", "string"), 0x76a6d327: ("text_url", "url", "string"),
                  0xdc7b1140: ("mention_name", "user_id", "long"), 0xc8cf05f8: ("custom_emoji", "document_id", "long"),
                  0xc6c1e5a7: ("diff_replace", "old_text", "string"),
                  0x208e68c9: ("input_mention_name", "user", "input_user")}


class Reader:
    def __init__(self, data):
        self.data, self.pos = data, 0

    def take(self, size):
        if self.pos + size > len(self.data):
            raise ValueError("Truncated TL data")
        value = self.data[self.pos:self.pos + size]
        self.pos += size
        return value

    def int(self):
        return struct.unpack("<i", self.take(4))[0]

    def uint(self):
        return struct.unpack("<I", self.take(4))[0]

    def long(self):
        return struct.unpack("<q", self.take(8))[0]

    def string(self):
        size, head = self.take(1)[0], 1
        if size == 254:
            size, head = int.from_bytes(self.take(3), "little"), 4
        elif size == 255:
            raise ValueError("Invalid TL string")
        raw = self.take(size)
        self.take(-(head + size) % 4)
        return raw.decode("utf-8", "replace")


def input_peer(reader, depth=0):
    code = reader.uint()
    if code == 0x7f3b18ea:
        return {"type": "empty"}
    if code == 0x7da07ec9:
        return {"type": "self"}
    if code == 0x35a95cb9:
        return {"type": "chat", "chat_id": reader.long()}
    if code in (0xdde8a54c, 0x27bcbbfc):
        ident = reader.long()
        reader.long()
        return {"type": "user", "user_id": ident} if code == 0xdde8a54c else {"type": "channel", "channel_id": ident}
    if code in (0xa87b0a1c, 0xbd2a0840) and depth < 4:
        peer, message = input_peer(reader, depth + 1), reader.int()
        name = "user_id" if code == 0xa87b0a1c else "channel_id"
        return {"type": name[:-3] + "_from_message", "peer": peer, "msg_id": message, name: reader.long()}
    raise ValueError(f"Unknown InputPeer constructor 0x{code:08x}")


def input_user(reader):
    code = reader.uint()
    if code == 0xb98886cf:
        return {"type": "empty"}
    if code == 0xf7c1b13f:
        return {"type": "self"}
    if code == 0xf21158c6:
        ident = reader.long()
        reader.long()
        return {"type": "user", "user_id": ident}
    if code == 0x1da448e2:
        peer, message = input_peer(reader), reader.int()
        return {"type": "user_from_message", "peer": peer, "msg_id": message, "user_id": reader.long()}
    raise ValueError(f"Unknown InputUser constructor 0x{code:08x}")


def entity(reader):
    code = reader.uint()
    if code in PLAIN_ENTITIES:
        return {"type": PLAIN_ENTITIES[code], "offset": reader.int(), "length": reader.int()}
    if code in (0xf1ccaaac, 0x904ac7c7):
        flags = reader.uint()
        item = {"type": "blockquote" if code == 0xf1ccaaac else "formatted_date",
                "offset": reader.int(), "length": reader.int()}
        if code == 0xf1ccaaac:
            item["collapsed"] = bool(flags & 1)
        else:
            item.update(flags=flags, date=reader.int())
        return item
    if code not in VALUE_ENTITIES:
        raise ValueError(f"Unknown MessageEntity constructor 0x{code:08x}")
    name, field, kind = VALUE_ENTITIES[code]
    item = {"type": name, "offset": reader.int(), "length": reader.int()}
    item[field] = reader.string() if kind == "string" else reader.long() if kind == "long" else input_user(reader)
    return item


def decode_entities(blob):
    blob = bytes(blob)
    result = {"items": [], "complete": not blob, "error": None, "raw_hex": blob.hex(),
              "offsets": "UTF-16 code units, as in Telegram; access hashes are left in the raw bytes"}
    if not blob:
        return result
    reader = Reader(blob)
    try:
        if reader.uint() != 0x1cb5c415:
            raise ValueError("Not a TL vector")
        count = reader.int()
        if not 0 <= count <= 100000:
            raise ValueError("Invalid TL vector length")
        for _ in range(count):
            result["items"].append(entity(reader))
        if reader.pos != len(blob):
            raise ValueError("Unexpected bytes after the TL vector")
        result["complete"] = True
    except (ValueError, struct.error) as exc:
        result["error"] = str(exc)
    return result


def chat_candidates(dialog_id):
    if type(dialog_id) is not int or dialog_id == 0:
        return []
    return [dialog_id] if dialog_id > 0 else [dialog_id - CHANNEL_BASE, dialog_id]


def utc(value):
    if type(value) is not int or not 0 < value < 2**32:
        return None
    return datetime.fromtimestamp(value, timezone.utc).isoformat()


def unix(value):
    try:
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return int(moment.timestamp()) if moment.utcoffset() is not None else None
    except (AttributeError, TypeError, ValueError, OverflowError):
        return None


def text_value(raw):
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return bytes(raw)


def plain(value):
    return {"hex": bytes(value).hex()} if isinstance(value, (bytes, bytearray, memoryview)) else value


def quote(name):
    return '"' + name.replace('"', '""') + '"'


def file_sha256(path):
    with open(path, "rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def open_copy(path):
    path = Path(path).resolve(strict=True)
    if not path.is_file():
        raise ValueError("The AyuGram database copy is not a file")
    if any(Path(str(path) + suffix).exists() for suffix in SIDECARS):
        raise ValueError("A -wal, -shm or -journal file lies next to this database, so it is live or in use; "
                         "interpret a copy made by the recorder")
    connection = None
    try:
        connection = sqlite3.connect(path.as_uri() + "?mode=ro&immutable=1", uri=True)
        connection.text_factory = text_value
        if connection.execute("PRAGMA quick_check").fetchall() != [("ok",)]:
            raise ValueError("SQLite integrity check failed")
        return connection
    except sqlite3.DatabaseError as exc:
        if connection is not None:
            connection.close()
        raise ValueError("Not a readable SQLite database copy: " + str(exc)) from None
    except ValueError:
        connection.close()
        raise


def inspect(connection):
    master = [list(row) for row in connection.execute(
        "SELECT type, name, tbl_name, sql FROM sqlite_master ORDER BY type, name")]
    tables = {row[1]: [column[1] for column in connection.execute("PRAGMA table_info(" + quote(row[1]) + ")")]
              for row in master if row[0] == "table"}
    if not set(MESSAGE_TABLES) & set(tables):
        raise ValueError("Not an AyuGram database: it has neither a DeletedMessage nor an EditedMessage table")
    user_version = connection.execute("PRAGMA user_version").fetchone()[0]
    version, reference = None, None
    if "SchemaVersion" in tables:
        flavor, reference = "desktop", DESKTOP
        try:
            row = connection.execute('SELECT "version" FROM "SchemaVersion" WHERE "id" = 1').fetchone()
        except sqlite3.DatabaseError:
            row = None
        version = row[0] if row and type(row[0]) is int else None
        status = ("no_version_row" if version is None else "known" if version in (0, 1)
                  else "newer_than_parser" if version > 1 else "unknown")
    elif "room_master_table" in tables:
        flavor, reference, version = "android", ANDROID, user_version
        try:
            identity = connection.execute("SELECT identity_hash FROM room_master_table LIMIT 1").fetchone()
        except sqlite3.DatabaseError:
            identity = None
        status = ("newer_than_parser" if version > 21 else "older_than_reference" if version < 21
                  else "known_derived" if identity and identity[0] == ANDROID_IDENTITY else "differs_from_reference")
    else:
        flavor, status = "unrecognized", "unrecognized"
    schema_sha256 = digest(canonical(master))
    sequences = {}
    if "sqlite_sequence" in tables:
        sequences = {name: seq for name, seq in connection.execute("SELECT name, seq FROM sqlite_sequence")
                     if isinstance(name, str) and type(seq) is int}
    info = {"flavor": flavor, "version": version, "status": status, "user_version": user_version,
            "reference": reference, "schema_sha256": schema_sha256,
            "matches_reference_schema": REFERENCE_SCHEMAS.get(schema_sha256),
            "missing_tables": [name for name in TABLES if name not in tables],
            "other_tables": sorted(set(tables) - set(TABLES) - SERVICE_TABLES),
            "unknown_columns": {name: [c for c in tables[name] if c not in COLUMNS[name]]
                                for name in TABLES if name in tables and set(tables[name]) - set(COLUMNS[name])},
            "missing_columns": {name: [c for c in COLUMNS[name] if c not in tables[name]]
                                for name in TABLES if name in tables and set(COLUMNS[name]) - set(tables[name])},
            "date_meanings": "AyuGram Desktop source" + ("" if flavor == "desktop" else "; not checked for this flavor")}
    return info, tables, sequences


def normalize(table, raw):
    dialog = raw.get("dialogId")
    row = {"table": table, "meaning": TABLE_MEANING[table], "fake_id": raw.get("fakeId"),
           "account_id": raw.get("userId"), "dialog_id": dialog, "chat_candidates": chat_candidates(dialog),
           "message_id": raw.get("messageId"),
           "dates": {name: {"value": raw[name], "utc": utc(raw[name]), "meaning": meaning}
                     for name, meaning in DATES[table].items() if name in raw},
           "raw": {key: plain(value) for key, value in raw.items()}}
    if table == "DeletedDialog":
        row["top_message"] = raw.get("topMessage")
    if table not in MESSAGE_TABLES:
        return row
    text, flags, blob = raw.get("text"), raw.get("flags"), raw.get("textEntities")
    encoded = text.encode("utf-8") if isinstance(text, str) else bytes(text) if isinstance(text, bytes) else b""
    row.update(topic_id=raw.get("topicId"), sender_bare_id=raw.get("fromId"), grouped_id=raw.get("groupedId"),
               outgoing=bool(flags & 2) if type(flags) is int else None,
               text=text if isinstance(text, str) else None,
               text_hex=bytes(text).hex() if isinstance(text, bytes) else None,
               text_sha256=digest(encoded),
               entities=decode_entities(blob) if isinstance(blob, (bytes, memoryview)) else None,
               media_path=raw.get("mediaPath"))
    return row


def interpret(path):
    path = Path(path)
    connection = open_copy(path)
    try:
        info, tables, sequences = inspect(connection)
        rows = []
        for table in TABLES:
            if table not in tables or "fakeId" not in tables[table]:
                continue
            cursor = connection.execute("SELECT * FROM " + quote(table) + ' ORDER BY "fakeId"')
            names = [column[0] for column in cursor.description]
            rows.extend(normalize(table, dict(zip(names, values))) for values in cursor)
    finally:
        connection.close()
    counts = {table: sum(row["table"] == table for row in rows) for table in TABLES if table in tables}
    return {"format": FORMAT, "file": {"name": path.name, "sha256": file_sha256(path), "size": path.stat().st_size},
            "schema": info, "row_counts": counts, "sequences": sequences, "rows": rows, "limits": LIMITS}


def ranges(ids):
    result = []
    for value in sorted(ids):
        if result and result[-1][1] + 1 == value:
            result[-1][1] = value
        else:
            result.append([value, value])
    return result


def compare(earlier, later):
    def states(copy):
        result = {table: {} for table in TABLES}
        for row in copy["rows"]:
            result[row["table"]][row["fake_id"]] = digest(canonical(row["raw"]))
        return result
    before, after = states(earlier), states(later)
    return {table: {"added": sorted(set(after[table]) - set(before[table])),
                    "removed": sorted(set(before[table]) - set(after[table])),
                    "changed": sorted(key for key in set(before[table]) & set(after[table])
                                      if before[table][key] != after[table][key])} for table in TABLES}


def sequence_drop(earlier, later):
    return {table: {"before": value, "after": later["sequences"].get(table, 0)}
            for table, value in earlier["sequences"].items() if later["sequences"].get(table, 0) < value}


def diff(earlier, later, rotated=None):
    drop = sequence_drop(earlier, later)
    result = {"earlier": earlier["file"], "later": later["file"], "rotation": drop or None,
              "basis": "fakeId is assigned by AUTOINCREMENT and is never reused within one database file"}
    if not drop:
        result["tables"] = compare(earlier, later)
        return result
    result["tables"] = None
    result["rotated_copy"] = rotated["file"] if rotated else None
    result["before_rotation"] = None
    if rotated is not None:
        if sequence_drop(earlier, rotated):
            result["rotated_copy_note"] = "the rotated copy does not continue the earlier copy"
        else:
            result["before_rotation"] = compare(earlier, rotated)
    return result


def summary(tables):
    return {kind: {table: len(values[kind]) for table, values in tables.items() if values[kind]}
            for kind in ("added", "removed", "changed")}


def listed(tables, kind):
    return {table: ranges(values[kind]) for table, values in tables.items() if values[kind]}


def capture_copies(events):
    main, rotated = [], []
    for event in events:
        payload = event["payload"]
        if event["kind"] not in ("capture.saved", "capture.partial") or payload.get("source") != "ayugram":
            continue
        names = {item.get("sha256"): item.get("source_filename") for item in payload.get("rotated_databases") or []
                 if isinstance(item, dict)}
        for artifact in event["artifacts"]:
            if artifact["role"] == "ayugram_database":
                main.append({"seq": event["seq"], "sha256": artifact["sha256"], "name": payload.get("source_filename"),
                             "rotated_present": payload.get("rotated_present")})
            elif artifact["role"] == "ayugram_database_rotated":
                rotated.append({"seq": event["seq"], "sha256": artifact["sha256"],
                                "name": names.get(artifact["sha256"])})
    return main, rotated


def stored(journal, sha256):
    copy = interpret(journal.objects / sha256)
    if copy["file"]["sha256"] != sha256:
        raise ValueError("A stored database copy differs from its journal hash")
    return copy


def record(journal):
    with journal.lock:
        events = journal.events()
    done = {event["payload"].get("capture_seq") for event in events if event["kind"] == "ayugram.interpreted"}
    main, rotated = capture_copies(events)
    appended, previous, before = [], None, None
    for copy in main:
        if before is not None and copy["sha256"] == before["sha256"]:
            continue
        current = stored(journal, copy["sha256"])
        if copy["seq"] not in done:
            appended.extend(record_copy(journal, copy, current, before, previous, rotated))
        previous, before = current, copy
    return appended


def record_copy(journal, copy, current, before, previous, rotated):
    change, follow, candidates = None, None, []
    if previous is not None:
        if sequence_drop(previous, current):
            seen = before.get("rotated_present")
            candidates = list({item["sha256"]: item for item in rotated if item["seq"] > before["seq"]
                               and (not isinstance(seen, list) or item["name"] not in seen)}.values())
            if len(candidates) == 1:
                follow = candidates[0]
        change = diff(previous, current, stored(journal, follow["sha256"]) if follow else None)
    info = current["schema"]
    payload = {"format": FORMAT, "capture_seq": copy["seq"], "copy_sha256": copy["sha256"],
               "source_filename": copy["name"], "size": current["file"]["size"],
               "schema": {key: info[key] for key in ("flavor", "version", "status", "user_version", "reference",
                                                       "schema_sha256", "matches_reference_schema", "missing_tables",
                                                       "other_tables", "unknown_columns", "missing_columns")},
               "row_counts": current["row_counts"], "sequences": current["sequences"],
               "previous_capture_seq": before["seq"] if before else None,
               "since_previous": None if change is None else (
                   {"rotation": True} if change["rotation"] else summary(change["tables"])),
               "meaning": INTERPRETED_MEANING}
    events = [journal.append("ayugram.interpreted", payload)]
    if change and change["tables"] and (listed(change["tables"], "removed") or listed(change["tables"], "changed")):
        events.append(journal.append("ayugram.rows_removed", {
            "format": FORMAT, "capture_seq": copy["seq"], "previous_capture_seq": before["seq"],
            "copy_sha256": copy["sha256"], "previous_copy_sha256": before["sha256"],
            "removed": listed(change["tables"], "removed"), "changed": listed(change["tables"], "changed"),
            "id_format": "inclusive fakeId ranges", "meaning": REMOVED_MEANING}))
    if change and change["rotation"]:
        moment = ROTATED.fullmatch(follow["name"] or "") if follow else None
        prior = change.get("before_rotation")
        events.append(journal.append("ayugram.rotation_detected", {
            "format": FORMAT, "capture_seq": copy["seq"], "previous_capture_seq": before["seq"],
            "sequence_drop": change["rotation"], "rotated_candidates": len(candidates),
            "rotated_copy": None if not follow else {
                "capture_seq": follow["seq"], "sha256": follow["sha256"], "source_filename": follow["name"],
                "renamed_at_ayugram_clock": utc(int(moment.group(1))) if moment else None},
            "followed": prior is not None,
            "removed_before_rotation": listed(prior, "removed") if prior else None,
            "changed_before_rotation": listed(prior, "changed") if prior else None,
            "id_format": "inclusive fakeId ranges", "meaning": ROTATION_MEANING}))
    return events


def read_journal(path, expected_fingerprint=None):
    path = Path(path)
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            if not {"manifest.json", "manifest.sig", "events.jsonl"} <= names:
                raise ValueError("Choose a TgWitness evidence ZIP with manifest.json, manifest.sig and events.jsonl")
            manifest = decode(archive.read("manifest.json"))
            if not isinstance(manifest, dict) or manifest.get("format") not in ("tgwitness-evidence-v1",
                                                                                "tgwatch-evidence-v1"):
                raise ValueError("Choose a TgWitness evidence ZIP")
            raw_key = base64.b64decode(manifest["public_key"], validate=True)
            fingerprint = hashlib.sha256(raw_key).hexdigest()
            if expected_fingerprint and expected_fingerprint != fingerprint:
                raise ValueError("The journal key differs from the trusted fingerprint")
            key = Ed25519PublicKey.from_public_bytes(raw_key)
            key.verify(base64.b64decode(archive.read("manifest.sig"), validate=True), canonical(manifest))
            hasher, events, previous = hashlib.sha256(), [], ZERO
            with archive.open("events.jsonl") as stream:
                for line in stream:
                    hasher.update(line)
                    event = decode(line)
                    if not isinstance(event, dict) or set(event) != set(JOURNAL_FIELDS) | {"hash", "signature"}:
                        raise ValueError("Unexpected journal record fields")
                    if event["seq"] != len(events) + 1 or event["previous_hash"] != previous:
                        raise ValueError("Broken journal sequence or hash chain")
                    previous = digest(canonical({name: event[name] for name in JOURNAL_FIELDS}))
                    if event["hash"] != previous:
                        raise ValueError("Changed journal record")
                    key.verify(base64.b64decode(event["signature"], validate=True), bytes.fromhex(previous))
                    events.append(slim(event))
            if hasher.hexdigest() != manifest["files"].get("events.jsonl"):
                raise ValueError("events.jsonl differs from the signed manifest")
            if len(events) != manifest.get("event_count") or previous != manifest.get("head_hash"):
                raise ValueError("The signed manifest does not match the journal")
    except InvalidSignature:
        raise ValueError("Invalid signature in the journal export") from None
    except (zipfile.BadZipFile, KeyError, TypeError, AttributeError, json.JSONDecodeError) as exc:
        raise ValueError("Unreadable journal export: " + (str(exc) or type(exc).__name__)) from None
    return {"file": {"name": path.name, "sha256": file_sha256(path), "size": path.stat().st_size},
            "format": manifest["format"], "fingerprint": fingerprint, "key_pinned": bool(expected_fingerprint),
            "events": len(events), "head_hash": previous,
            "checked": "manifest signature, events.jsonl hash, hash chain and the signature of every record",
            "not_checked": "attachments, report seals, external time and coverage; run python -m tgwitness.verify "
                           "for the complete check"}, events


def slim(event):
    payload = event["payload"] if isinstance(event["payload"], dict) else {}
    text = payload.get("text")
    return {"seq": event["seq"], "hash": event["hash"], "kind": event["kind"], "observed_at": event["observed_at"],
            "source_at": event["source_at"], "chat_id": event["chat_id"], "message_id": event["message_id"],
            "text": text if isinstance(text, str) else None,
            "text_sha256": digest(text.encode("utf-8")) if isinstance(text, str) else None,
            "outgoing": payload.get("outgoing") is True or payload.get("deleted_message_was_outgoing") is True,
            "has_media": payload.get("has_media") is True, "account_id": payload.get("collector_account_id"),
            "message_ids": payload.get("message_ids") if event["kind"] == "deletion.unscoped" else None}


def journal_index(events):
    versions, deleted, known, unscoped, accounts = {}, {}, set(), {}, set()
    for event in events:
        if type(event["account_id"]) is int:
            accounts.add(event["account_id"])
        if isinstance(event["message_ids"], list):
            for ident in event["message_ids"]:
                if type(ident) is int:
                    unscoped.setdefault(ident, event["seq"])
        key = (event["chat_id"], event["message_id"])
        if type(key[0]) is not int or type(key[1]) is not int:
            continue
        known.add(key)
        if event["kind"] in VERSION_KINDS:
            versions.setdefault(key, []).append(event)
        elif event["kind"] == "message.deleted":
            deleted.setdefault(key, event)
    return {"versions": versions, "deleted": deleted, "known": known, "unscoped": unscoped, "accounts": accounts}


def shown(event):
    if event is None:
        return None
    return {"seq": event["seq"], "hash": event["hash"], "kind": event["kind"], "observed_at": event["observed_at"],
            "source_at": event["source_at"], "text": event["text"], "text_sha256": event["text_sha256"]}


def ayugram_part(row):
    return {"table": row["table"], "fake_id": row["fake_id"], "account_id": row["account_id"],
            "dialog_id": row["dialog_id"], "chat_candidates": row["chat_candidates"], "message_id": row["message_id"],
            "text": row["text"], "text_sha256": row["text_sha256"], "outgoing": row["outgoing"],
            "dates": row["dates"], "standing": STANDING}


def outcome(kind, chat_id, message_id, row=None, **extra):
    return {"outcome": kind, "label": LABELS[kind], "chat_id": chat_id, "message_id": message_id,
            **({"ayugram": ayugram_part(row)} if row else {}), **extra}


def deleted_outcome(row, key, index):
    notice = index["deleted"].get(key)
    history = [event for event in index["versions"].get(key, []) if notice is None or event["seq"] < notice["seq"]]
    last = history[-1] if history else None
    if notice is None:
        return outcome("ayugram_only", *key, row, journal_versions=[shown(event) for event in history],
                       journal_unscoped_notice_seq=index["unscoped"].get(key[1]),
                       basis="the journal has no deletion notice for this message")
    journal = {"deletion": shown(notice), "last_version": shown(last)}
    if last is not None and last["text_sha256"] != row["text_sha256"]:
        return outcome("conflict", *key, row, journal=journal,
                       basis="both record the deletion; the journal's last saved text before the notice differs")
    return outcome("matched", *key, row, journal=journal,
                   basis="deletion and text" if last else "deletion; the journal saved no text of this message")


def when(row, name):
    return row["dates"].get(name, {}).get("value")


def edited_outcome(row, key, index, first):
    history = index["versions"].get(key, [])
    if not history:
        return outcome("ayugram_only", *key, row, basis="the journal saved no version of this message")
    edit_date, date = when(row, "editDate"), when(row, "date")
    same, basis = [event for event in history if event["source_unix"] == edit_date], "same version date"
    if not same and first:
        same = [event for event in history if event["kind"] != "message.edited" and event["source_unix"] == date]
        basis = "first saved version: message date"
    if same:
        equal = [event for event in same if event["text_sha256"] == row["text_sha256"]]
        if equal:
            return outcome("matched", *key, row, journal={"version": shown(equal[0])}, basis=basis)
        return outcome("conflict", *key, row, journal={"version": shown(same[0])}, basis=basis)
    equal = [event for event in history if event["text_sha256"] == row["text_sha256"]]
    if equal:
        return outcome("matched", *key, row, journal={"version": shown(equal[0])}, basis="same text in a saved version")
    return outcome("ayugram_only", *key, row, journal_versions=[shown(event) for event in history],
                   basis="the journal saved other versions of this message, not this one")


def resolve(row, known):
    candidates = row["chat_candidates"]
    present = [chat for chat in candidates if (chat, row["message_id"]) in known]
    if len(candidates) == 1:
        return candidates[0], present
    return (present[0] if len(present) == 1 else None), present


def reconcile(copy, events):
    index = journal_index(events)
    for history in index["versions"].values():
        for event in history:
            event["source_unix"] = unix(event["source_at"])
    rows = [row for row in copy["rows"] if row["table"] in MESSAGE_TABLES]
    compared = [row for row in rows if not index["accounts"] or row["account_id"] in index["accounts"]]
    first = {}
    for row in compared:
        if row["table"] == "EditedMessage":
            group = (row["account_id"], row["dialog_id"], row["message_id"])
            first[group] = min(first.get(group, row["fake_id"]), row["fake_id"])
    items, claimed, edits, unresolved = [], set(), {}, set()
    for row in compared:
        chat, present = resolve(row, index["known"])
        if chat is None:
            unresolved.update((candidate, row["message_id"]) for candidate in row["chat_candidates"])
            items.append(outcome("ambiguous", None, row["message_id"], row, journal_candidates_with_message=present,
                                 basis="resolved only when exactly one candidate chat has this message ID in the "
                                       "journal"))
            continue
        key = (chat, row["message_id"])
        if row["table"] == "DeletedMessage":
            claimed.add(key)
            items.append(deleted_outcome(row, key, index))
        else:
            edits.setdefault(key, []).append(row)
            group = (row["account_id"], row["dialog_id"], row["message_id"])
            items.append(edited_outcome(row, key, index, first[group] == row["fake_id"]))
    for key, notice in index["deleted"].items():
        if key in claimed or key in unresolved:
            continue
        history = [event for event in index["versions"].get(key, []) if event["seq"] < notice["seq"]]
        reasons = ["memory", "removed"] + (["no_text"] if history and not history[-1]["text"] else [])
        items.append(outcome("tgwitness_only", *key, journal={"deletion": shown(notice),
                             "last_version": shown(history[-1] if history else None)},
                             expected_reasons=[REASONS[name] for name in reasons]))
    for key, history in index["versions"].items():
        if key in unresolved:
            continue
        for position, event in enumerate(history):
            if event["kind"] != "message.edited":
                continue
            prior = history[position - 1] if position else None
            saved = edits.get(key, [])
            if (prior is None and saved) or (prior is not None and any(
                    row["text_sha256"] == prior["text_sha256"] or when(row, "editDate") == prior["source_unix"]
                    for row in saved)):
                continue
            reasons = (["own"] if event["outgoing"] else []) + (
                ["same_text"] if prior and prior["text_sha256"] == event["text_sha256"] else []) + (
                ["no_text"] if prior and not prior["text"] else []) + ["removed"]
            items.append(outcome("tgwitness_only", *key, journal={"edit": shown(event), "previous_version": shown(prior)},
                                 expected_reasons=[REASONS[name] for name in reasons]))
    order = {name: position for position, name in enumerate(OUTCOMES)}
    items.sort(key=lambda item: (order[item["outcome"]], str(item["chat_id"]), item["message_id"] or 0))
    accounts = {"journal": sorted(index["accounts"]),
                "ayugram": sorted({row["account_id"] for row in rows if type(row["account_id"]) is int})}
    return items, accounts, len(rows) - len(compared)


def build_report(copy, journal_info, events, source=None):
    items, accounts, excluded = reconcile(copy, events)
    return {"format": REPORT_FORMAT, "created_at": utcnow(),
            "ayugram": {"file": copy["file"], "source": source, "schema": copy["schema"],
                        "row_counts": copy["row_counts"], "standing": STANDING},
            "journal": journal_info, "accounts": accounts, "excluded_other_account": excluded,
            "counts": {name: sum(item["outcome"] == name for item in items) for name in OUTCOMES},
            "labels": LABELS, "limits": LIMITS, "items": items}


STYLE = ('body{font:16px system-ui;max-width:1100px;margin:32px auto;padding:0 20px;background:#f5f7fa;color:#16243a}'
         'section,article{padding:16px 20px;background:white;border:1px solid #cdd6e2;border-radius:12px;margin:14px 0}'
         'pre{white-space:pre-wrap;overflow-wrap:anywhere}table{border-collapse:collapse}td,th{padding:4px 12px;'
         'text-align:left;border-bottom:1px solid #e1e7ef}.conflict{border-left:4px solid #c0392b}'
         '.ayugram_only,.ambiguous{border-left:4px solid #d39e00}.matched{border-left:4px solid #2e7d32}')


def render(report):
    escape = lambda value: html.escape(str(value), quote=True)
    counts = "".join(f"<tr><th>{escape(LABELS[name])}</th><td>{report['counts'][name]}</td></tr>" for name in OUTCOMES)
    journal, ayugram = report["journal"], report["ayugram"]
    articles = []
    for item in report["items"]:
        side = item.get("ayugram")
        body = (f'<h3>{escape(item["label"])}</h3><p>Chat {escape(item["chat_id"])} · message '
                f'{escape(item["message_id"])}</p>')
        if side:
            body += (f'<p>AyuGram {escape(side["table"])} #{escape(side["fake_id"])}, dialog {escape(side["dialog_id"])}: '
                     f'{escape(side["standing"])}</p><pre>{escape(side["text"] or "")}</pre>')
        for name, value in (item.get("journal") or {}).items():
            if value:
                body += (f'<p>Journal {escape(name)}: #{escape(value["seq"])} {escape(value["kind"])} · '
                         f'{escape(value["observed_at"])}</p><pre>{escape(value["text"] or "")}</pre>')
        for reason in item.get("expected_reasons", []):
            body += f'<p>Possible reason: {escape(reason)}</p>'
        if item.get("basis"):
            body += f'<p>Basis: {escape(item["basis"])}</p>'
        articles.append(f'<article class="{escape(item["outcome"])}">{body}</article>')
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
            '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; '
            'base-uri \'none\'; form-action \'none\'"><title>AyuGram and TgWitness journal comparison</title>'
            f'<style>{STYLE}</style><h1>AyuGram and TgWitness journal comparison</h1>'
            f'<section><p>AyuGram database copy {escape(ayugram["file"]["name"])} · SHA-256 '
            f'{escape(ayugram["file"]["sha256"])} · schema {escape(ayugram["schema"]["flavor"])} '
            f'{escape(ayugram["schema"]["version"])} ({escape(ayugram["schema"]["status"])})</p>'
            f'<p>Journal export {escape(journal["file"]["name"])} · SHA-256 {escape(journal["file"]["sha256"])} · '
            f'key SHA-256 {escape(journal["fingerprint"])} · key pinned: {escape(journal["key_pinned"])}</p>'
            f'<p>Checked: {escape(journal["checked"])}. Not checked: {escape(journal["not_checked"])}.</p>'
            f'<p>Rows of other accounts not compared: {escape(report["excluded_other_account"])}</p></section>'
            f'<section><h2>Outcomes</h2><table>{counts}</table></section>'
            '<section><h2>Limits of this observer</h2><ul>'
            + "".join(f"<li>{escape(limit)}</li>" for limit in report["limits"]) + '</ul></section>'
            + "".join(articles) + '</html>').encode()


def copy_from_export(path, fingerprint, directory):
    from .verify import verify_zip
    verified = verify_zip(path, fingerprint)
    with zipfile.ZipFile(path) as archive:
        events = [decode(line) for line in archive.read("events.jsonl").splitlines()]
        main, _ = capture_copies(events)
        if not main:
            raise ValueError("The capture export holds no AyuGram database copy")
        target = Path(directory) / "ayudata-copy.db"
        target.write_bytes(archive.read("objects/" + main[-1]["sha256"]))
    copy = interpret(target)
    if copy["file"]["sha256"] != main[-1]["sha256"]:
        raise ValueError("The database copy differs from its journal hash")
    return copy, {"capture_export": Path(path).name, "capture_export_sha256": file_sha256(path),
                  "capture_seq": main[-1]["seq"], "capture_fingerprint": verified["fingerprint"],
                  "capture_key_pinned": verified["key_pinned"]}


def write_json(value, output):
    raw = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if output is None:
        print(raw, end="")
    else:
        Path(output).write_text(raw, encoding="utf-8")


def command(args):
    if args.ayugram_command == "interpret":
        if args.data:
            from .journal import Journal
            journal = Journal(args.data)
            try:
                events = record(journal)
            finally:
                journal.close()
            write_json({"appended": [{"seq": event["seq"], "kind": event["kind"]} for event in events]}, args.output)
            return
        result = interpret(args.db)
        if args.previous:
            result["diff"] = diff(interpret(args.previous), result, interpret(args.rotated) if args.rotated else None)
        write_json(result, args.output)
        return
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    if any((output / name).exists() for name in ("report.json", "report.html")):
        raise ValueError("The output directory already holds a report")
    with tempfile.TemporaryDirectory() as directory:
        if args.capture_export:
            copy, source = copy_from_export(args.capture_export, args.capture_fingerprint, directory)
        else:
            copy, source = interpret(args.db), {"database_copy": Path(args.db).name}
    journal_info, events = read_journal(args.journal, args.journal_fingerprint)
    report = build_report(copy, journal_info, events, source)
    write_json(report, output / "report.json")
    (output / "report.html").write_bytes(render(report))
    write_json({"report": str(output / "report.json"), "html": str(output / "report.html"), "counts": report["counts"]},
               None)
