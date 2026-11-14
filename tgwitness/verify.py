# TgWitness verifier sources SHA-256: 0a2b754ff16b67048f066c20ce406332d35f497a0c84187a61582a26bb545ce6
"""Standalone verifier"""
import argparse
import base64
import bisect
import hashlib
import heapq
import io
import json
import math
import os
import re
import shutil
import sqlite3
import struct
import sys
import tempfile
import unicodedata
import zipfile
from array import array
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography import x509
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.x509 import ocsp

FIELDS = ("seq", "observed_at", "source_at", "kind", "chat_id", "message_id",
          "actor_id", "payload", "previous_hash")


OTS_MAGIC = b"\x00OpenTimestamps\x00\x00Proof\x00\xbf\x89\xe2\xe8\x84\xe8\x92\x94"
MAX_UNCOMPRESSED_GIB = 4


MAX_MEMBERS = 500_000
MAX_MANIFEST_BYTES = 64 * 1024**2
MAX_SMALL_MEMBER_BYTES = 16 * 1024**2
MAX_RECORD_BYTES = 64 * 1024**2
MAX_JSON_BYTES = 256 * 1024**2
OTS_PENDING, OTS_BITCOIN = bytes.fromhex("83dfe30d2ef90c8e"), bytes.fromhex("0588960d73d71901")
SEAL_OPEN = b'<script type="application/tgwitness-seal+json" id="tgwitness-seal">'
SEAL_CLOSE = b"</script></body></html>\n"
SEAL_WINDOW = 1024 * 1024
DRAND_CHAIN = "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971"
DRAND_GENESIS, DRAND_PERIOD = 1692803367, 3
DRAND_RELAYS = ("https://drand.cloudflare.com", "https://api.drand.sh", "https://api2.drand.sh", "https://api3.drand.sh")
DRAND_CHECK_LIMIT = 100
GATEWAY_FIELDS = ("at", "name", "type", "rcode", "decision", "colo")


class VerifierTooOld(ValueError):
    def __init__(self, detail=""):
        super().__init__("The archive signature is valid, but this verifier is older than the archive format" +
                         (": " + detail if detail else ""))


class CheckUnavailable(Exception):
    pass


def safe_text(value):
    text = str(value)
    text = re.sub(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07\x1b]*(?:\x07|\x1b\\))", "", text)
    text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f-\x9f]", "", text)
    return re.sub("[\u061c\u200e\u200f\u2028\u2029\u202a-\u202e\u2066-\u2069]",
                  lambda match: "\\u%04x" % ord(match.group()), text)


def authenticate_statement(value, key_field="public_key"):
    statement = value["statement"]
    Ed25519PublicKey.from_public_bytes(base64.b64decode(statement[key_field], validate=True)).verify(
        base64.b64decode(value["signature"], validate=True), canonical(statement))
    return statement


def validate_server_hashes(value):
    if (not isinstance(value, dict) or value.get("format") != "telegram-file-hashes-v1"
            or value.get("algorithm") != "sha256"
            or value.get("status") not in ("complete", "partial", "unavailable")
            or type(value.get("downloaded_bytes")) is not int or value["downloaded_bytes"] != 0):
        raise ValueError("Invalid Telegram file-hash manifest")
    ranges, size, covered = value.get("ranges"), value.get("expected_bytes"), value.get("covered_bytes")
    if (not isinstance(ranges, list) or len(ranges) > 65536 or type(covered) is not int or covered < 0
            or size is not None and (type(size) is not int or size <= 0)):
        raise ValueError("Invalid file-hash coverage")
    info = value.get("representation")
    if info is not None and (not isinstance(info, dict) or info.get("kind") not in ("photo", "document")
            or type(info.get("id")) is not int or not isinstance(info.get("variant"), str)
            or info.get("bytes") != size or any(key in info for key in ("access_hash", "file_reference"))):
        raise ValueError("Invalid file-hash representation")
    offset = 0
    for part in ranges:
        if (not isinstance(part, dict) or type(part.get("offset")) is not int
                or type(part.get("length")) is not int or part["offset"] != offset
                or not 0 < part["length"] < 2**31 or not isinstance(part.get("sha256"), str)
                or not re.fullmatch(r"[a-f0-9]{64}", part["sha256"])
                or size is None or offset >= size):
            raise ValueError("Invalid, overlapping or discontinuous file-hash range")
        offset = min(size, offset + part["length"])
    if covered != offset:
        raise ValueError("File-hash coverage differs from recorded ranges")
    if value["status"] == "complete" and (not info or size is None or offset != size or not ranges):
        raise ValueError("Incomplete file hashes claim complete coverage")
    if value["status"] == "partial" and (not info or size is None or not 0 < offset < size):
        raise ValueError("Invalid partial file-hash coverage")
    if value["status"] == "unavailable" and (offset or ranges):
        raise ValueError("Unavailable file hashes claim covered bytes")
    return value


def ends_at_directory(archive):
    handle, position = archive.fp, archive.fp.tell()
    try:
        handle.seek(0, 2)
        end = handle.tell()
        if end < 22:
            return False
        handle.seek(end - 22)
        return handle.read(4) == b"PK\x05\x06"
    finally:
        handle.seek(position)


def contiguous(archive, infos):
    handle, start = archive.fp, archive.fp.tell()
    try:
        position = 0
        for info in sorted(infos, key=lambda item: item.header_offset):
            if info.header_offset != position:
                raise ValueError("Archive has bytes between its members")
            handle.seek(position)
            header = handle.read(30)
            if len(header) != 30 or header[:4] != b"PK\x03\x04":
                raise ValueError("Archive member header is damaged")
            name_length, extra_length = struct.unpack("<HH", header[26:30])
            extra = handle.read(name_length + extra_length)[name_length:]
            wide, at = False, 0
            while at + 4 <= len(extra):
                field, length = struct.unpack("<HH", extra[at:at + 4])
                wide, at = wide or field == 1, at + 4 + length
            position += 30 + name_length + extra_length + info.compress_size
            if info.flag_bits & 8:
                handle.seek(position)
                signed = handle.read(4) == b"PK\x07\x08"
                position += (4 if signed else 0) + (20 if wide else 12)
        if position != archive.start_dir:
            raise ValueError("Archive has bytes between its members")
    finally:
        handle.seek(start)


def open_archive(path, max_gib=None):
    limit = MAX_UNCOMPRESSED_GIB if max_gib is None else max_gib
    if type(limit) not in (int, float) or not math.isfinite(limit) or limit <= 0:
        raise ValueError("Archive size limit must be a positive finite number of GiB")
    archive = zipfile.ZipFile(path)
    try:
        infos = archive.infolist()
        if len(infos) > MAX_MEMBERS:
            raise ValueError("Archive has more members than the verifier accepts")
        names = [info.filename for info in infos]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate ZIP members")
        if infos and min(info.header_offset for info in infos) != 0:
            raise ValueError("Archive has data before its first member")
        contiguous(archive, infos)
        if archive.comment:
            raise ValueError("Archive carries bytes in its trailing comment")
        if not ends_at_directory(archive):
            raise ValueError("Archive has data after its central directory")
        if sum(info.file_size for info in infos) > limit * 1024**3:
            raise ValueError("Bundle exceeds the verifier's size limit; raise it with --max-gib")
    except BaseException:
        archive.close()
        raise
    return archive


def read_member(archive, name, limit=MAX_SMALL_MEMBER_BYTES):
    if archive.getinfo(name).file_size > limit:
        raise ValueError(name + " exceeds the verifier's size limit for this member")
    with archive.open(name) as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError(name + " exceeds the verifier's size limit for this member")
    return data


def unique_keys(pairs):
    value = dict(pairs)
    if len(value) != len(pairs):
        raise ValueError("Signed JSON contains a duplicate key")
    return value


def strict_json(data):
    return json.loads(data, object_pairs_hook=unique_keys)


def read_manifest(archive):
    manifest = strict_json(read_member(archive, "manifest.json", MAX_MANIFEST_BYTES))
    if not isinstance(manifest, dict) or not isinstance(manifest.get("public_key"), str):
        raise ValueError("manifest.json is not a signed bundle manifest")
    Ed25519PublicKey.from_public_bytes(base64.b64decode(manifest["public_key"], validate=True)).verify(
        base64.b64decode(read_member(archive, "manifest.sig"), validate=True), canonical(manifest))
    return manifest


def member_digest(archive, name):
    digest = hashlib.sha256()
    with archive.open(name) as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bounded_lines(stream):
    for line in iter(lambda: stream.readline(MAX_RECORD_BYTES + 1), stream.read(0)):
        if len(line) > MAX_RECORD_BYTES:
            raise ValueError("A record exceeds the verifier's size limit")
        yield line


def read_json_file(path):
    path = Path(path)
    if path.stat().st_size > MAX_JSON_BYTES:
        raise ValueError(path.name + " exceeds the verifier's size limit")
    return strict_json(path.read_text(encoding="utf-8"))


import getpass


from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


PW_MAGIC = b"TGWPW1\n"
PW_CHUNK = 1024 * 1024
PW_CONTEXT = b"tgwitness-password-v1|"
PW_NAME_LIMIT = 1024


def _pw_key(password, salt):
    return Scrypt(salt=salt, length=32, n=2**17, r=8, p=1).derive(password.encode("utf-8"))


def _pw_read(stream, size):
    value = stream.read(size)
    if len(value) != size:
        raise ValueError("Truncated password-encrypted file")
    return value


def _pw_record(stream, limit):
    size = int.from_bytes(_pw_read(stream, 4), "big")
    if not 16 <= size <= limit + 16:
        raise ValueError("Invalid password-encrypted record length")
    return _pw_read(stream, size)


def _pw_nonce(prefix, counter):
    if counter >= 2**32:
        raise ValueError("Password-encrypted file exceeds the chunk limit")
    return prefix + counter.to_bytes(4, "big")


def _pw_name(value):
    name = value.encode("utf-8")
    if (not name or len(name) > PW_NAME_LIMIT or value in (".", "..")
            or any(ord(char) < 32 or ord(char) == 127 or char in "/\\" for char in value)):
        raise ValueError("Use a plain filename for the password-encrypted content")
    return name


def _pw_output(path):
    return os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb")


def encrypt_password_file(source, destination, password, inner_name=None):
    source, destination = Path(source), Path(destination)
    if not 12 <= len(password) <= 256:
        raise ValueError("Use a password of 12 to 256 characters")
    name = _pw_name(inner_name or source.name)
    salt, prefix = os.urandom(16), os.urandom(8)
    cipher = AESGCM(_pw_key(password, salt))
    created = False
    try:
        with source.open("rb") as plain, _pw_output(destination) as output:
            created = True
            output.write(PW_MAGIC + salt + prefix)
            metadata = cipher.encrypt(_pw_nonce(prefix, 0), name, PW_CONTEXT + b"name")
            output.write(len(metadata).to_bytes(4, "big") + metadata)
            counter = 1
            while True:
                data = plain.read(PW_CHUNK)
                last = len(data) < PW_CHUNK
                aad = PW_CONTEXT + name + (b"|last" if last else b"|more")
                record = cipher.encrypt(_pw_nonce(prefix, counter), data, aad)
                output.write(len(record).to_bytes(4, "big") + record)
                if last:
                    break
                counter += 1
        return destination
    except BaseException:
        if created:
            destination.unlink(missing_ok=True)
        raise


def decrypt_password_file(source, destination, password):
    source, destination = Path(source), Path(destination)
    with source.open("rb") as encrypted, tempfile.TemporaryFile(dir=destination.parent) as plain:
        if _pw_read(encrypted, len(PW_MAGIC)) != PW_MAGIC:
            raise ValueError("Not a TgWitness password-encrypted file")
        salt, prefix = _pw_read(encrypted, 16), _pw_read(encrypted, 8)
        cipher = AESGCM(_pw_key(password, salt))
        name = cipher.decrypt(_pw_nonce(prefix, 0), _pw_record(encrypted, PW_NAME_LIMIT), PW_CONTEXT + b"name")
        try:
            _pw_name(name.decode("utf-8"))
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid encrypted filename") from exc
        counter = 1
        while True:
            record = _pw_record(encrypted, PW_CHUNK)
            last = len(record) < PW_CHUNK + 16
            aad = PW_CONTEXT + name + (b"|last" if last else b"|more")
            data = cipher.decrypt(_pw_nonce(prefix, counter), record, aad)
            plain.write(data)
            if last:
                if encrypted.read(1):
                    raise ValueError("Trailing data after password-encrypted content")
                break
            counter += 1
        plain.seek(0)
        created = False
        try:
            with _pw_output(destination) as output:
                created = True
                shutil.copyfileobj(plain, output, PW_CHUNK)
        except BaseException:
            if created:
                destination.unlink(missing_ok=True)
            raise
    return destination


def password_command(argv):
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog="verify.py unseal-password", description="Open a .tgwpw export; verify the decrypted evidence separately.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, required=True, help="New output file; existing files are never overwritten.")
    parser.add_argument("--password-stdin", action="store_true", help="Read one UTF-8 password line from standard input instead of prompting.")
    args = parser.parse_args(argv)
    password = sys.stdin.readline().rstrip("\r\n") if args.password_stdin else getpass.getpass("Export password: ")
    try:
        decrypt_password_file(args.source, args.out, password)
    except Exception as exc:
        reason = ("the password is wrong or the file was changed" if type(exc).__name__ == "InvalidTag"
                  else str(exc) if isinstance(exc, (ValueError, OSError)) and str(exc) else type(exc).__name__)
        parser.exit(1, "Could not decrypt the export: " + reason + "\n")
    print("Export decrypted. Run verification on the resulting evidence separately.")
QUALIFIED_TSU = {
    "8751fca3d49938f02aaea3d69983adf3d9f324447b4c00b817c3900198c0fbfd": "EC1 TSU 2021",
    "3917e4995093954bc162568c7188c00a222023166824480e8f84a4e1f3441dc1": "EC2 TSU 2021",
    "61726c187889a606dda86821a1faf3c5ff5f4a116254a2325893655c7e45f64f": "TSU 202301",
    "e69a32ea707c71c1633f7c9cbfc60f902c50081d97473163ebf7098d5df36f30": "TSU 202302",
}
QUALIFIED_PROVIDER = "FPS Policy and Support - BOSA, Kingdom of Belgium"
QUALIFIED_LIST = "https://tsl.belgium.be/tsl-be.xml"
QC_STATEMENTS, QC_COMPLIANCE = "1.3.6.1.5.5.7.1.3", bytes.fromhex("0604008e460101")


def der(data, offset):
    tag, length, start = data[offset], data[offset + 1], offset + 2
    if length & 0x80:
        count = length & 0x7F
        if not 1 <= count <= 4:
            raise ValueError("Unsupported DER length")
        length, start = int.from_bytes(data[start:start + count], "big"), start + count
    if start + length > len(data):
        raise ValueError("Truncated DER")
    return tag, start, start + length


def children(data, start, end):
    found, offset = [], start
    while offset < end:
        tag, value_start, value_end = der(data, offset)
        if value_end > end:
            raise ValueError("Truncated DER")
        found.append((tag, offset, value_start, value_end))
        offset = value_end
    return found


def oid(data, start, end):
    parts, value = [], 0
    for byte in data[start:end]:
        value = (value << 7) | (byte & 0x7F)
        if not byte & 0x80:
            parts.append(value)
            value = 0
    if not parts:
        raise ValueError("Empty object identifier")
    first = min(parts[0] // 40, 2)
    return ".".join(map(str, [first, parts[0] - 40 * first] + parts[1:]))


SIGNED_DATA, TST_INFO = "1.2.840.113549.1.7.2", "1.2.840.113549.1.9.16.1.4"
CONTENT_TYPE, MESSAGE_DIGEST = "1.2.840.113549.1.9.3", "1.2.840.113549.1.9.4"
SIGNING_CERTIFICATE, SIGNING_CERTIFICATE_V2 = "1.2.840.113549.1.9.16.2.12", "1.2.840.113549.1.9.16.2.47"
DIGESTS = {"2.16.840.1.101.3.4.2.1": hashes.SHA256, "2.16.840.1.101.3.4.2.2": hashes.SHA384,
           "2.16.840.1.101.3.4.2.3": hashes.SHA512}
RSA_SIGNATURES = {"1.2.840.113549.1.1.1": None, "1.2.840.113549.1.1.11": hashes.SHA256,
                  "1.2.840.113549.1.1.12": hashes.SHA384, "1.2.840.113549.1.1.13": hashes.SHA512}
ECDSA_SIGNATURES = {"1.2.840.10045.4.3.2": hashes.SHA256, "1.2.840.10045.4.3.3": hashes.SHA384,
                    "1.2.840.10045.4.3.4": hashes.SHA512}


def timestamp_token(reply):
    tag, start, end = der(reply, 0)
    if tag != 0x30 or end != len(reply):
        raise ValueError("Not an RFC 3161 timestamp reply")
    parts = children(reply, start, end)
    status_info = children(reply, parts[0][2], parts[0][3]) if parts and parts[0][0] == 0x30 else []
    if not status_info or status_info[0][0] != 0x02:
        raise ValueError("Not an RFC 3161 timestamp reply")
    status = int.from_bytes(reply[status_info[0][2]:status_info[0][3]], "big")
    if status not in (0, 1):
        raise ValueError("The timestamp authority refused the request (status " + str(status) + ")")
    if len(parts) != 2 or parts[1][0] != 0x30:
        raise ValueError("The timestamp reply carries no token")
    content = children(reply, parts[1][2], parts[1][3])
    if len(content) != 2 or content[0][0] != 0x06 or oid(reply, *content[0][2:]) != SIGNED_DATA or content[1][0] != 0xA0:
        raise ValueError("The timestamp token is not signed data")
    signed_tag, signed_start, signed_end = der(reply, content[1][2])
    signed = children(reply, signed_start, signed_end) if signed_tag == 0x30 else []
    if len(signed) < 4 or signed[2][0] != 0x30 or signed[-1][0] != 0x31:
        raise ValueError("The timestamp token is not signed data")
    encapsulated = children(reply, signed[2][2], signed[2][3])
    if len(encapsulated) != 2 or oid(reply, *encapsulated[0][2:]) != TST_INFO or encapsulated[1][0] != 0xA0:
        raise ValueError("The timestamp token does not hold a TSTInfo")
    info_tag, info_start, info_end = der(reply, encapsulated[1][2])
    if info_tag != 0x04:
        raise ValueError("The timestamp token does not hold a TSTInfo")
    certificates = []
    for tag, _, value_start, value_end in signed[3:-1]:
        if tag == 0xA0:
            certificates += [reply[offset:stop] for _, offset, _, stop in children(reply, value_start, value_end)]
    signers = children(reply, signed[-1][2], signed[-1][3])
    if len(signers) != 1:
        raise ValueError("The timestamp token must have exactly one signer")
    return {"status": status, "tst": reply[info_start:info_end], "certificates": certificates,
            "signer": signers[0], "reply": reply}


def generalized_time(raw):
    found = re.fullmatch(rb"(\d{14})(?:\.\d{1,6})?Z", raw)
    if not found:
        raise ValueError("The timestamp time is not a UTC GeneralizedTime")
    return datetime.strptime(found[1].decode(), "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)


def tst_info(tst):
    tag, start, end = der(tst, 0)
    items = children(tst, start, end) if tag == 0x30 and end == len(tst) else []
    if len(items) < 5 or [t for t, *_ in items[:5]] != [0x02, 0x06, 0x30, 0x02, 0x18]:
        raise ValueError("Malformed TSTInfo")
    imprint = children(tst, items[2][2], items[2][3])
    algorithm = children(tst, imprint[0][2], imprint[0][3])
    if len(imprint) != 2 or imprint[1][0] != 0x04 or not algorithm or algorithm[0][0] != 0x06:
        raise ValueError("Malformed TSTInfo")
    nonce = next((int.from_bytes(tst[s:e], "big", signed=True) for t, _, s, e in items[5:] if t == 0x02), None)
    return {"algorithm": oid(tst, *algorithm[0][2:]), "hash": tst[imprint[1][2]:imprint[1][3]],
            "time": generalized_time(tst[items[4][2]:items[4][3]]), "nonce": nonce}


def query_nonce(query):
    _, start, end = der(query, 0)
    return next((int.from_bytes(query[s:e], "big", signed=True) for t, _, s, e in children(query, start, end)[2:]
                 if t == 0x02), None)


def timestamp_reply_summary(reply, digest, query=None):
    token = timestamp_token(reply)
    info = tst_info(token["tst"])
    if info["algorithm"] != "2.16.840.1.101.3.4.2.1" or info["hash"] != digest:
        raise ValueError("The timestamp does not cover this checkpoint")
    if query is not None and info["nonce"] != query_nonce(query):
        raise ValueError("The timestamp nonce differs from the request")
    return {"status": token["status"], "time": info["time"].strftime("%Y-%m-%dT%H:%M:%SZ")}


def signed_attributes(reply, start, end):
    found = {}
    for _, _, s, e in children(reply, start, end):
        parts = children(reply, s, e)
        if len(parts) != 2 or parts[0][0] != 0x06 or parts[1][0] != 0x31:
            raise ValueError("Malformed signed attribute")
        kind, values = parts
        name = oid(reply, *kind[2:])
        if name in found:
            raise ValueError("Repeated signed attribute")
        found[name] = children(reply, values[2], values[3])
    return found


def signing_certificate_hash(reply, attributes):
    if SIGNING_CERTIFICATE_V2 in attributes:
        name, default = SIGNING_CERTIFICATE_V2, hashes.SHA256
    elif SIGNING_CERTIFICATE in attributes:
        name, default = SIGNING_CERTIFICATE, hashes.SHA1
    else:
        raise ValueError("The timestamp does not name its signing certificate")
    value = attributes[name][0]
    certificates = children(reply, value[2], value[3])
    first = children(reply, certificates[0][2], certificates[0][3])[0]
    identifiers = children(reply, first[2], first[3])
    algorithm = default
    if identifiers[0][0] == 0x30:
        algorithm = DIGESTS.get(oid(reply, *children(reply, identifiers[0][2], identifiers[0][3])[0][2:]))
        identifiers = identifiers[1:]
    if algorithm is None or identifiers[0][0] != 0x04:
        raise ValueError("Unsupported signing certificate reference")
    return algorithm, reply[identifiers[0][2]:identifiers[0][3]], algorithm().name


def certificate_reference_details(algorithm):
    warning = ("The timestamp names its signing certificate by SHA-1 (RFC 2634 SigningCertificate); "
               "prefer authorities that return SigningCertificateV2")
    return {"certificate_reference": algorithm, "warnings": [warning] if algorithm == "sha1" else []}


def timestamp_certificate_reference(reply):
    token = timestamp_token(reply)
    _, _, start, end = token["signer"]
    items = children(reply, start, end)
    attributes = signed_attributes(reply, items[3][2], items[3][3])
    _, _, algorithm = signing_certificate_hash(reply, attributes)
    return certificate_reference_details(algorithm)


def timestamp_signature(reply, roots, *, include_reference=False, intermediates=()):
    token = timestamp_token(reply)
    when = tst_info(token["tst"])["time"]
    _, _, start, end = token["signer"]
    items = children(reply, start, end)
    if len(items) < 6 or items[3][0] != 0xA0 or items[4][0] != 0x30 or items[5][0] != 0x04:
        raise ValueError("The timestamp signer has no signed attributes")
    digest = DIGESTS.get(oid(reply, *children(reply, items[2][2], items[2][3])[0][2:]))
    if digest is None:
        raise ValueError("Unsupported timestamp digest algorithm")
    attributes = signed_attributes(reply, items[3][2], items[3][3])
    content_type, message_digest = attributes.get(CONTENT_TYPE), attributes.get(MESSAGE_DIGEST)
    if not content_type or oid(reply, *content_type[0][2:]) != TST_INFO:
        raise ValueError("The signed attributes do not describe a TSTInfo")
    hasher = hashes.Hash(digest())
    hasher.update(token["tst"])
    if not message_digest or reply[message_digest[0][2]:message_digest[0][3]] != hasher.finalize():
        raise ValueError("The signature does not cover this TSTInfo")
    algorithm, named, reference = signing_certificate_hash(reply, attributes)
    raw = {}
    for data in token["certificates"]:
        raw[data] = x509.load_der_x509_certificate(data)
    signer_data = None
    for data in raw:
        hasher = hashes.Hash(algorithm())
        hasher.update(data)
        if hasher.finalize() == named:
            signer_data = data
    if signer_data is None:
        raise ValueError("The reply does not carry the certificate the signature names")
    signer = raw[signer_data]
    try:
        usage = signer.extensions.get_extension_for_class(x509.ExtendedKeyUsage)
    except x509.ExtensionNotFound:
        usage = None
    if not usage or not usage.critical or list(usage.value) != [x509.oid.ExtendedKeyUsageOID.TIME_STAMPING]:
        raise ValueError("The signing certificate is not for time stamping only")
    signed = b"\x31" + reply[items[3][1] + 1:items[3][3]]
    signature = reply[items[5][2]:items[5][3]]
    method = oid(reply, *children(reply, items[4][2], items[4][3])[0][2:])
    key = signer.public_key()
    try:
        if isinstance(key, rsa.RSAPublicKey) and method in RSA_SIGNATURES:
            key.verify(signature, signed, padding.PKCS1v15(), (RSA_SIGNATURES[method] or digest)())
        elif isinstance(key, ec.EllipticCurvePublicKey) and method in ECDSA_SIGNATURES:
            key.verify(signature, signed, ec.ECDSA(ECDSA_SIGNATURES[method]()))
        else:
            raise ValueError("Unsupported timestamp signature algorithm " + method)
    except InvalidSignature:
        raise ValueError("The timestamp signature is invalid") from None
    trusted = {root.fingerprint(hashes.SHA256()): root for root in roots}
    chain, current = [signer], signer
    while not (len(chain) > 1 and chain[-1].fingerprint(hashes.SHA256()) in trusted):
        if len(chain) > 8:
            raise ValueError("The timestamp certificate chain is too long")
        candidates = list(trusted.values()) + [c for c in [*raw.values(), *intermediates] if c not in chain]
        issuer = None
        for candidate in candidates:
            if candidate.subject != current.issuer:
                continue
            try:
                current.verify_directly_issued_by(candidate)
            except (ValueError, TypeError, InvalidSignature):
                continue
            issuer = candidate
            break
        if issuer is None:
            raise ValueError("The timestamp certificate does not chain to a trusted root")
        try:
            constraints = issuer.extensions.get_extension_for_class(x509.BasicConstraints).value
        except x509.ExtensionNotFound:
            constraints = None
        if not constraints or not constraints.ca:
            raise ValueError("A certificate in the timestamp chain is not a certificate authority")
        chain.append(issuer)
        current = issuer
    for certificate in chain:
        if not certificate.not_valid_before_utc <= when <= certificate.not_valid_after_utc:
            raise ValueError("A certificate in the timestamp chain was not valid at the stamped time")
        for extension in certificate.extensions:
            if extension.critical and not isinstance(extension.value, (
                    x509.BasicConstraints, x509.KeyUsage, x509.ExtendedKeyUsage)):
                raise ValueError("Unsupported critical timestamp certificate extension: " + extension.oid.dotted_string)
    for index, certificate in enumerate(chain[1:], 1):
        try:
            usage = certificate.extensions.get_extension_for_class(x509.KeyUsage).value
        except x509.ExtensionNotFound:
            usage = None
        if usage is not None and not usage.key_cert_sign:
            raise ValueError("A timestamp CA certificate does not permit signing certificates")
        constraints = certificate.extensions.get_extension_for_class(x509.BasicConstraints).value
        below = sum(child.subject != child.issuer for child in chain[1:index])
        if constraints.path_length is not None and below > constraints.path_length:
            raise ValueError("The timestamp certificate chain exceeds a CA path length constraint")
    root = chain[-1]
    return {"signer": signer.subject.rfc4514_string(), "root": root.subject.rfc4514_string(),
            "root_sha256": root.fingerprint(hashes.SHA256()).hex(),
            "signer_sha256": signer.fingerprint(hashes.SHA256()).hex(),
            **(certificate_reference_details(reference) if include_reference else {})}


def ots_summary(proof, digest, *, commitments=False):
    head = OTS_MAGIC + b"\x01\x08"
    if len(digest) != 32 or proof[:len(head)] != head or proof[len(head):len(head) + 32] != digest:
        raise ValueError("The OpenTimestamps proof is not for this checkpoint")
    if len(proof) > 1024 * 1024:
        raise ValueError("The OpenTimestamps proof exceeds the size limit")

    class Reader:
        def __init__(self, data):
            self.data, self.pos = data, 0

        def take(self, size):
            end = self.pos + size
            if end > len(self.data):
                raise ValueError("Truncated OpenTimestamps proof")
            value, self.pos = self.data[self.pos:end], end
            return value

        def integer(self):
            value = 0
            for shift in range(0, 35, 7):
                byte = self.take(1)[0]
                value |= (byte & 127) << shift
                if not byte & 128:
                    if value > 0xffffffff:
                        break
                    return value
            raise ValueError("OpenTimestamps integer exceeds the limit")

        def blob(self, maximum):
            size = self.integer()
            if size > maximum:
                raise ValueError("OpenTimestamps field exceeds the limit")
            return self.take(size)

        def finish(self):
            if self.pos != len(self.data):
                raise ValueError("Trailing bytes in OpenTimestamps proof")

    reader = Reader(proof[len(head) + 32:])
    kinds, remaining = set(), 10000
    bitcoin = []

    def node(message_size, depth=0, message=None):
        nonlocal remaining
        if depth >= 256:
            raise ValueError("OpenTimestamps tree exceeds the depth limit")
        operations = set()
        while True:
            remaining -= 1
            if remaining < 0:
                raise ValueError("OpenTimestamps tree exceeds the operation limit")
            tag = reader.take(1)[0]
            more = tag == 255
            if more:
                tag = reader.take(1)[0]
            if tag == 0:
                kind = reader.take(8)
                payload = Reader(reader.blob(8192))
                if kind == OTS_BITCOIN:
                    height = payload.integer()
                    payload.finish()
                    if message_size != 32:
                        raise ValueError("OpenTimestamps Bitcoin commitment must be 32 bytes")
                    kinds.add("bitcoin-unverified")
                    if message is not None:
                        bitcoin.append({"height": height, "merkle_root": message.hex()})
                elif kind == OTS_PENDING:
                    uri = payload.blob(1000)
                    payload.finish()
                    if not re.fullmatch(rb"[A-Za-z0-9._/:-]*", uri):
                        raise ValueError("Invalid OpenTimestamps calendar URI")
                    kinds.add("pending")
                else:
                    kinds.add("unknown")
            else:
                argument = b""
                size = message_size
                if tag in (0xf0, 0xf1):
                    argument = reader.blob(4096)
                    if not argument:
                        raise ValueError("Empty OpenTimestamps operation argument")
                    size += len(argument)
                elif tag == 0xf3:
                    size *= 2
                elif tag in (0x02, 0x03, 0x08, 0x67):
                    size = 20 if tag in (0x02, 0x03) else 32
                elif tag != 0xf2:
                    raise ValueError("Unknown OpenTimestamps operation")
                if size > 4096:
                    raise ValueError("OpenTimestamps operation result exceeds the limit")
                operation = (tag, argument)
                if operation in operations:
                    raise ValueError("Repeated OpenTimestamps operation")
                operations.add(operation)
                calculated = None
                if message is not None:
                    if tag == 0xf0:
                        calculated = message + argument
                    elif tag == 0xf1:
                        calculated = argument + message
                    elif tag == 0xf2:
                        calculated = message[::-1]
                    elif tag == 0xf3:
                        calculated = message.hex().encode("ascii")
                    elif tag in (0x02, 0x03, 0x08):
                        try:
                            calculated = hashlib.new({0x02: "sha1", 0x03: "ripemd160", 0x08: "sha256"}[tag], message).digest()
                        except ValueError:
                            pass
                node(size, depth + 1, calculated)
            if not more:
                return

    node(32, message=digest if commitments else None)
    reader.finish()
    status = next(kind for kind in ("bitcoin-unverified", "pending", "unknown") if kind in kinds)
    return {"status": status, "verification": "structure only; run ots verify",
            **({"commitments": bitcoin} if commitments else {})}


PUBLIC_BITCOIN_SOURCES = ("https://blockstream.info/api", "https://mempool.space/api")
BITCOIN_SOURCES = PUBLIC_BITCOIN_SOURCES


def use_bitcoin_sources(urls):
    from urllib.parse import urlsplit
    global BITCOIN_SOURCES
    clean = []
    for url in urls:
        parts = urlsplit(url.strip())
        if parts.scheme not in ("http", "https") or not parts.hostname or parts.username or parts.password \
                or parts.query or parts.fragment:
            raise ValueError("--bitcoin-source needs an http(s) Esplora API address without credentials: " + url)
        clean.append(url.strip().rstrip("/"))
    BITCOIN_SOURCES = tuple(dict.fromkeys(clean)) or PUBLIC_BITCOIN_SOURCES


def bitcoin_fetcher():
    import urllib.request
    cache = {}

    def get(url):
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "TgWitness verify"}), timeout=15) as reply:
            body = reply.read(1025)
        if len(body) > 1024:
            raise ValueError("Excessive Bitcoin header response")
        return body.decode("ascii").strip()

    def fetch(height):
        if height in cache:
            return cache[height]
        found = []
        for source in BITCOIN_SOURCES:
            try:
                tip = int(get(source + "/blocks/tip/height"))
                if tip - height + 1 < 6:
                    return None
                block_hash = get(source + "/block-height/" + str(height))
                hash_bytes(block_hash)
                header = bytes.fromhex(get(source + "/block/" + block_hash + "/header"))
                if len(header) != 80 or hashlib.sha256(hashlib.sha256(header).digest()).digest()[::-1].hex() != block_hash:
                    raise ValueError("Bitcoin header hash mismatch")
                bits = int.from_bytes(header[72:76], "little")
                exponent, mantissa = bits >> 24, bits & 0x7fffff
                if bits & 0x800000 or not 3 <= exponent <= 29 or not mantissa:
                    raise ValueError("Invalid Bitcoin proof-of-work target")
                target = mantissa << (8 * (exponent - 3))
                if target > 0xffff << 208 or int(block_hash, 16) > target:
                    raise ValueError("Invalid Bitcoin header proof of work")
                found.append(header)
            except (OSError, UnicodeError):
                raise CheckUnavailable("Bitcoin header sources are unreachable") from None
        if len(set(found)) != 1:
            raise ValueError("Bitcoin header sources disagree")
        cache[height] = found[0]
        return found[0]
    return fetch


def confirm_ots(proof, digest, fetch=None):
    summary = ots_summary(proof, digest, commitments=True)
    fetch = fetch or bitcoin_fetcher()
    confirmed, unreachable = [], False
    for item in summary.pop("commitments"):
        try:
            header = fetch(item["height"])
        except CheckUnavailable:
            unreachable = True
            continue
        if header is None:
            continue
        if len(header) != 80 or header[36:68].hex() != item["merkle_root"]:
            raise ValueError("OpenTimestamps commitment differs from the Bitcoin block Merkle root")
        confirmed.append({"height": item["height"],
                          "time": datetime.fromtimestamp(int.from_bytes(header[68:72], "little"), timezone.utc).isoformat()})
    if confirmed:
        agreed = ("two HTTPS explorers" if BITCOIN_SOURCES == PUBLIC_BITCOIN_SOURCES
                  else "the supplied source" if len(BITCOIN_SOURCES) == 1 else str(len(BITCOIN_SOURCES)) + " supplied sources")
        summary.update(status="confirmed", time=min(c["time"] for c in confirmed), blocks=confirmed,
                       verification="proof evaluated; headers with 6 confirmations agreed by " + agreed,
                       sources=list(BITCOIN_SOURCES))
    elif unreachable:
        summary["check"] = "unavailable"
    return summary


def tsa_roots(path):
    data = Path(path).read_bytes()
    try:
        roots = x509.load_pem_x509_certificates(data)
    except ValueError:
        roots = [x509.load_der_x509_certificate(data)]
    if not roots:
        raise ValueError("The --tsa-ca file holds no certificate")
    return roots


def qualified_timestamp(reply):
    for data in timestamp_token(reply)["certificates"]:
        certificate = x509.load_der_x509_certificate(data)
        service = QUALIFIED_TSU.get(certificate.fingerprint(hashes.SHA256()).hex())
        if not service:
            continue
        try:
            statements = certificate.extensions.get_extension_for_oid(x509.ObjectIdentifier(QC_STATEMENTS)).value.value
        except x509.ExtensionNotFound:
            continue
        if QC_COMPLIANCE in statements:
            return {"qualified": {"service": service, "provider": QUALIFIED_PROVIDER, "trusted_list": QUALIFIED_LIST}}
    return {}


def stamp_time(value):
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def revocation_subject(reply, extra=()):
    token = timestamp_token(reply)
    _, _, start, end = token["signer"]
    items = children(reply, start, end)
    if len(items) < 6 or items[3][0] != 0xA0:
        raise ValueError("The timestamp signer has no signed attributes")
    algorithm, named, _ = signing_certificate_hash(reply, signed_attributes(reply, items[3][2], items[3][3]))
    loaded, signer = {}, None
    for data in token["certificates"]:
        loaded[data] = x509.load_der_x509_certificate(data)
    for data in loaded:
        hasher = hashes.Hash(algorithm())
        hasher.update(data)
        if hasher.finalize() == named:
            signer = loaded[data]
    certificates = list(loaded.values())
    if signer is None:
        raise ValueError("The reply does not carry the certificate the signature names")
    for candidate in certificates + list(extra):
        if candidate.subject != signer.issuer:
            continue
        try:
            signer.verify_directly_issued_by(candidate)
        except (ValueError, TypeError, InvalidSignature):
            continue
        return {"signer": signer, "issuer": candidate, "time": tst_info(token["tst"])["time"]}
    raise ValueError("The issuer of the signing certificate is neither in the reply nor in the given root file")


def ocsp_responder(response, issuer):
    for candidate in [issuer] + list(response.certificates):
        if response.responder_name is not None:
            named = candidate.subject == response.responder_name
        else:
            named = x509.SubjectKeyIdentifier.from_public_key(candidate.public_key()).digest == response.responder_key_hash
        if not named:
            continue
        if candidate.fingerprint(hashes.SHA256()) != issuer.fingerprint(hashes.SHA256()):
            try:
                candidate.verify_directly_issued_by(issuer)
                usage = candidate.extensions.get_extension_for_class(x509.ExtendedKeyUsage).value
            except (ValueError, TypeError, InvalidSignature, x509.ExtensionNotFound):
                continue
            if (x509.oid.ExtendedKeyUsageOID.OCSP_SIGNING not in usage
                    or not candidate.not_valid_before_utc <= response.produced_at_utc <= candidate.not_valid_after_utc):
                continue
        key = candidate.public_key()
        try:
            if isinstance(key, rsa.RSAPublicKey):
                key.verify(response.signature, response.tbs_response_bytes, padding.PKCS1v15(),
                           response.signature_hash_algorithm)
            elif isinstance(key, ec.EllipticCurvePublicKey):
                key.verify(response.signature, response.tbs_response_bytes, ec.ECDSA(response.signature_hash_algorithm))
            else:
                continue
        except InvalidSignature:
            continue
        return candidate
    raise ValueError("The OCSP response is not signed by the issuer or by a responder it authorised for OCSP signing")


def revocation_status(kind, data, subject):
    signer, issuer, when, source = subject["signer"], subject["issuer"], subject["time"], kind.upper()
    if kind == "ocsp":
        response = ocsp.load_der_ocsp_response(data)
        if response.response_status != ocsp.OCSPResponseStatus.SUCCESSFUL:
            raise ValueError("The OCSP responder answered " + response.response_status.name)
        found = None
        for single in response.responses:
            query = ocsp.OCSPRequestBuilder().add_certificate(signer, issuer, single.hash_algorithm).build()
            if (single.serial_number, single.issuer_name_hash, single.issuer_key_hash) == (
                    query.serial_number, query.issuer_name_hash, query.issuer_key_hash):
                found = single
        if found is None:
            raise ValueError("The OCSP response does not name this signing certificate")
        ocsp_responder(response, issuer)
        if found.certificate_status == ocsp.OCSPCertStatus.UNKNOWN:
            raise ValueError("The OCSP responder does not know this signing certificate")
        revoked = found.revocation_time_utc if found.certificate_status == ocsp.OCSPCertStatus.REVOKED else None
        reason, issued, until = found.revocation_reason, found.this_update_utc, found.next_update_utc
    elif kind == "crl":
        try:
            crl = x509.load_der_x509_crl(data)
        except ValueError:
            crl = x509.load_pem_x509_crl(data)
        if crl.issuer != issuer.subject or not crl.is_signature_valid(issuer.public_key()):
            raise ValueError("The CRL is not signed by the issuer of the signing certificate")
        entry = crl.get_revoked_certificate_by_serial_number(signer.serial_number)
        revoked = entry.revocation_date_utc if entry else None
        reason = next((e.value.reason for e in entry.extensions if isinstance(e.value, x509.CRLReason)), None) if entry else None
        issued, until = crl.last_update_utc, crl.next_update_utc
    else:
        raise ValueError("Unknown revocation evidence: " + kind)
    if revoked is not None:
        compromised = reason in (x509.ReasonFlags.key_compromise, x509.ReasonFlags.ca_compromise)
        state = "revoked" if revoked <= when or compromised else "revoked_after"
        return {"status": state, "source": source, "revoked_at": stamp_time(revoked),
                "reason": reason.value if reason else None,
                "detail": "signing certificate revoked at " + stamp_time(revoked)
                          + (", before" if revoked <= when else ", after") + " the time stamp"
                          + (", for key compromise" if compromised else "") + " (" + source + ")"}
    if issued < when and (until is None or until < when):
        raise ValueError("The " + source + " answer of " + stamp_time(issued) + " expired before the stamped time")
    if issued > signer.not_valid_after_utc:
        raise ValueError("The " + source + " answer was issued after the signing certificate expired")
    return {"status": "good", "source": source, "as_of": stamp_time(issued),
            "detail": "signing certificate not revoked as of " + stamp_time(issued) + " (" + source + ")"}


def timestamp_revocation(archive, names, base, reply, tsa_ca=None):
    found = [kind for kind in ("ocsp", "crl") if base + "." + kind in names]
    if not found:
        return {"status": "not checked", "detail": "revocation not checked (no OCSP/CRL in the archive)"}
    try:
        extra = x509.load_pem_x509_certificates(Path(tsa_ca).read_bytes()) if tsa_ca else []
    except (OSError, ValueError):
        extra = []
    problems = []
    for kind in found:
        try:
            return revocation_status(kind, read_member(archive, base + "." + kind), revocation_subject(reply, extra))
        except (ValueError, TypeError, IndexError, InvalidSignature, UnsupportedAlgorithm) as exc:
            problems.append(kind.upper() + ": " + str(exc))
    return {"status": "failed", "error": "; ".join(problems), "detail": "revocation check failed: " + "; ".join(problems)}


def verify_anchors(archive, names, public_key, event_count, hash_at, tsa_ca=None, check_bitcoin=False):
    results = []
    for name in sorted(n for n in names if n.startswith("anchors/") and n.endswith(".json")):
        data = read_member(archive, name)
        retained_checkpoint = strict_json(data)
        verify_checkpoint(retained_checkpoint, public_key, event_count, hash_at)
        digest, stem = hashlib.sha256(data).digest(), name[:-len(".json")] + "."
        for proof_name in sorted(n for n in names if n.startswith(stem) and n != name):
            service = proof_name[len(stem):].rsplit(".", 1)[0]
            entry = {"checkpoint": name[len("anchors/"):], "service": service,
                     "event_count": retained_checkpoint["statement"]["event_count"]}
            if proof_name.endswith(".tsr"):
                reply = read_member(archive, proof_name)
                query_name = proof_name[:-4] + ".tsq"
                query = read_member(archive, query_name) if query_name in names else None
                entry.update(kind="rfc3161", **timestamp_reply_summary(reply, digest, query))
                if tsa_ca:
                    timestamp_signature(reply, tsa_roots(tsa_ca))
                entry["signature"] = "checked against the given root" if tsa_ca else "not checked (use --tsa-ca)"
                if tsa_ca:
                    entry.update(qualified_timestamp(reply))
                try:
                    entry.update(timestamp_certificate_reference(reply))
                except (ValueError, IndexError, TypeError):
                    entry["certificate_reference"] = "unavailable"
                entry["revocation"] = timestamp_revocation(archive, names, proof_name[:-4], reply, tsa_ca)
                if entry["revocation"]["status"] == "revoked":
                    raise ValueError("The " + service + " timestamp is invalid: its " + entry["revocation"]["detail"]
                                     + ("; reason " + entry["revocation"]["reason"] if entry["revocation"]["reason"] else ""))
            elif proof_name.endswith(".ots"):
                proof = read_member(archive, proof_name)
                entry.update(kind="opentimestamps", **(confirm_ots(proof, digest) if check_bitcoin else ots_summary(proof, digest)))
            else:
                continue
            results.append(entry)
    return results


INTEL_SGX_ROOT = base64.b64decode(
    "MIICjzCCAjSgAwIBAgIUImUM1lqdNInzg7SVUr9QGzknBqwwCgYIKoZIzj0EAwIwaDEaMBgGA1UEAwwRSW50ZWwgU0dYIFJvb3Qg"
    "Q0ExGjAYBgNVBAoMEUludGVsIENvcnBvcmF0aW9uMRQwEgYDVQQHDAtTYW50YSBDbGFyYTELMAkGA1UECAwCQ0ExCzAJBgNVBAYT"
    "AlVTMB4XDTE4MDUyMTEwNDUxMFoXDTQ5MTIzMTIzNTk1OVowaDEaMBgGA1UEAwwRSW50ZWwgU0dYIFJvb3QgQ0ExGjAYBgNVBAoM"
    "EUludGVsIENvcnBvcmF0aW9uMRQwEgYDVQQHDAtTYW50YSBDbGFyYTELMAkGA1UECAwCQ0ExCzAJBgNVBAYTAlVTMFkwEwYHKoZI"
    "zj0CAQYIKoZIzj0DAQcDQgAEC6nEwMDIYZOj/iPWsCzaEKi71OiOSLRFhWGjbnBVJfVnkY4u3IjkDYYL0MxO4mqsyYjlBalTVYxF"
    "P2sJBK5zlKOBuzCBuDAfBgNVHSMEGDAWgBQiZQzWWp00ifODtJVSv1AbOScGrDBSBgNVHR8ESzBJMEegRaBDhkFodHRwczovL2Nl"
    "cnRpZmljYXRlcy50cnVzdGVkc2VydmljZXMuaW50ZWwuY29tL0ludGVsU0dYUm9vdENBLmRlcjAdBgNVHQ4EFgQUImUM1lqdNInz"
    "g7SVUr9QGzknBqwwDgYDVR0PAQH/BAQDAgEGMBIGA1UdEwEB/wQIMAYBAf8CAQEwCgYIKoZIzj0EAwIDSQAwRgIhAOW/5QkR+S9C"
    "iSDcNoowLuPRLsWGf/Yi7GSX94BgwTwgAiEA4J0lrHoMs+Xo5o/sX6O9QWxHRAvZUGOdRQ7cvqRXaqI=")
INTEL_SGX_ROOT_SHA256 = "44a0196b2b99f889b8e149e95b807a350e7424964399e885a7cbb8ccfab674d3"
INTEL_QE_VENDOR = bytes.fromhex("939a7233f79c4ca9940a0db3957f0607")
INTEL_TD_QE_SIGNER = bytes.fromhex("dc9e2a7c6f948f17474e34a7fc43ed030f7c1563f1babddf6340c82e0e54a8c5")
INTEL_PCK_CAS = ("Intel SGX PCK Platform CA", "Intel SGX PCK Processor CA")
SGX_PCK_EXTENSION = "1.2.840.113741.1.13.1"
TDX_BODIES = {2: 584, 3: 648, 4: 885}
TDX_REPORT_FIELDS = (("tee_tcb_svn", 16), ("mr_seam", 48), ("mr_signer_seam", 48), ("seam_attributes", 8),
                     ("td_attributes", 8), ("xfam", 8), ("mrtd", 48), ("mr_config_id", 48), ("mr_owner", 48),
                     ("mr_owner_config", 48), ("rtmr0", 48), ("rtmr1", 48), ("rtmr2", 48), ("rtmr3", 48),
                     ("report_data", 64))
TDX_MEASUREMENTS = ("mrtd", "rtmr0", "rtmr1", "rtmr2", "rtmr3", "report_data")
TDX_STATUSES = ("UpToDate", "SWHardeningNeeded", "ConfigurationNeeded", "ConfigurationAndSWHardeningNeeded",
                "OutOfDate", "OutOfDateConfigurationNeeded", "Revoked")
TDX_QE_STATUSES = ("UpToDate", "OutOfDate", "Revoked")
TDX_RESERVED_ATTRIBUTES = sum(1 << bit for bit in (*range(1, 4), *range(7, 16), *range(23, 27), *range(32, 62)))
TDX_NOT_CHECKED = ("the code the VM ran: the compose RTMR3 measures and the OS image behind MRTD and RTMR0-2; "
                   "python -m tgwitness.cloud verify compares them")
ATTESTATION_RECORDS = ("tgwitness-attestation-record-v1", "tgwitness-deployment-v1")


class QuoteInvalid(ValueError):
    pass


def tdx_root():
    root = x509.load_der_x509_certificate(INTEL_SGX_ROOT)
    if root.fingerprint(hashes.SHA256()).hex() != INTEL_SGX_ROOT_SHA256:
        raise QuoteInvalid("The pinned Intel SGX Root CA is damaged")
    return root


def tdx_quote(raw):
    if len(raw) < 48:
        raise QuoteInvalid("The quote is truncated")
    version, key_type, tee = struct.unpack_from("<HHI", raw, 0)
    if tee != 0x81:
        raise QuoteInvalid("Not an Intel TDX quote")
    if key_type != 2:
        raise QuoteInvalid("Unsupported attestation key type " + str(key_type))
    if raw[12:28] != INTEL_QE_VENDOR:
        raise QuoteInvalid("The quote was not produced by Intel's quoting enclave")
    if version == 4:
        kind, offset = 2, 48
    elif version == 5:
        if len(raw) < 54:
            raise QuoteInvalid("The quote is truncated")
        kind, size = struct.unpack_from("<HI", raw, 48)
        if TDX_BODIES.get(kind) != size:
            raise QuoteInvalid("Unsupported TD report body " + str(kind) + " of " + str(size) + " bytes")
        offset = 54
    else:
        raise QuoteInvalid("Unsupported quote version " + str(version))
    signed = offset + TDX_BODIES[kind]
    if len(raw) < signed + 4:
        raise QuoteInvalid("The quote is truncated")
    length = struct.unpack_from("<I", raw, signed)[0]
    auth = raw[signed + 4:signed + 4 + length]
    if len(auth) != length or len(auth) < 134 or raw[signed + 4 + length:].strip(b"\0"):
        raise QuoteInvalid("The quote's signature data has the wrong length")
    cert_type, cert_size = struct.unpack_from("<HI", auth, 128)
    cert = auth[134:134 + cert_size]
    if cert_type != 6 or len(cert) != cert_size or len(cert) < 456:
        raise QuoteInvalid("The quote carries no quoting enclave report")
    inner = 450 + struct.unpack_from("<H", cert, 448)[0]
    if len(cert) < inner + 6:
        raise QuoteInvalid("The quote's certification data is truncated")
    chain_type, chain_size = struct.unpack_from("<HI", cert, inner)
    chain = cert[inner + 6:inner + 6 + chain_size]
    if chain_type != 5 or len(chain) != chain_size:
        raise QuoteInvalid("The quote carries no PCK certificate chain")
    fields = TDX_REPORT_FIELDS + ((("tee_tcb_svn2", 16), ("mr_service_td", 48)) if kind in (3, 4) else ())
    report, at = {}, offset
    for name, size in fields:
        report[name], at = raw[at:at + size], at + size
    return {"version": version, "signed": raw[:signed], "report": report, "signature": auth[0:64],
            "attestation_key": auth[64:128], "qe_report": cert[0:384], "qe_signature": cert[384:448],
            "qe_auth": cert[450:inner], "pck_chain": chain.rstrip(b"\0")}


def tdx_signature(key, signature, data, what):
    if len(signature) != 64:
        raise QuoteInvalid(what + ": expected a 64-byte ECDSA P-256 signature")
    try:
        key.verify(encode_dss_signature(int.from_bytes(signature[:32], "big"), int.from_bytes(signature[32:], "big")),
                   data, ec.ECDSA(hashes.SHA256()))
    except (InvalidSignature, ValueError, TypeError):
        raise QuoteInvalid(what + ": the signature is invalid") from None


def tdx_certificates(text):
    data = text.encode() if isinstance(text, str) else bytes(text)
    try:
        return x509.load_pem_x509_certificates(data.rstrip(b"\0"))
    except ValueError:
        raise QuoteInvalid("Unreadable certificate chain") from None


def tdx_time(value):
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        raise QuoteInvalid("Unreadable time " + str(value)[:40]) from None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def tdx_crl(data, issuer, at, what):
    try:
        crl = x509.load_der_x509_crl(data)
    except ValueError:
        raise QuoteInvalid(what + " is unreadable") from None
    if crl.issuer != issuer.subject or not crl.is_signature_valid(issuer.public_key()):
        raise QuoteInvalid(what + " is not signed by " + issuer.subject.rfc4514_string())
    if crl.last_update_utc > at or crl.next_update_utc is not None and at > crl.next_update_utc:
        raise QuoteInvalid(what + " is not current at " + at.isoformat())
    return crl


def tdx_chain(chain, root, at, what, crls=None):
    chain = list(chain)
    if chain and chain[-1].fingerprint(hashes.SHA256()) == root.fingerprint(hashes.SHA256()):
        chain = chain[:-1]
    if not chain:
        raise QuoteInvalid(what + ": no certificates")
    for index, certificate in enumerate(chain):
        issuer = chain[index + 1] if index + 1 < len(chain) else root
        try:
            certificate.verify_directly_issued_by(issuer)
        except (ValueError, TypeError, InvalidSignature):
            raise QuoteInvalid(what + ": " + certificate.subject.rfc4514_string() + " is not issued by "
                               + issuer.subject.rfc4514_string()) from None
        try:
            constraints = issuer.extensions.get_extension_for_class(x509.BasicConstraints).value
        except x509.ExtensionNotFound:
            constraints = None
        if not constraints or not constraints.ca:
            raise QuoteInvalid(what + ": " + issuer.subject.rfc4514_string() + " is not a certificate authority")
        for checked in (certificate, issuer):
            if not checked.not_valid_before_utc <= at <= checked.not_valid_after_utc:
                raise QuoteInvalid(what + ": " + checked.subject.rfc4514_string() + " is not valid at " + at.isoformat())
        if crls is not None:
            crl = crls.get(issuer.subject.public_bytes())
            if crl is None:
                raise QuoteInvalid(what + ": no revocation list from " + issuer.subject.rfc4514_string())
            if crl.get_revoked_certificate_by_serial_number(certificate.serial_number) is not None:
                raise QuoteInvalid(what + ": " + certificate.subject.rfc4514_string() + " is revoked")
    return chain


def tdx_pck(certificate):
    try:
        data = certificate.extensions.get_extension_for_oid(x509.ObjectIdentifier(SGX_PCK_EXTENSION)).value.value
    except x509.ExtensionNotFound:
        raise QuoteInvalid("The PCK certificate has no Intel SGX extension") from None
    found = {}
    try:
        _, start, end = der(data, 0)
        for _, _, item_start, item_end in children(data, start, end):
            parts = children(data, item_start, item_end)
            if len(parts) != 2 or parts[0][0] != 0x06:
                continue
            name, (_, _, value_start, value_end) = oid(data, *parts[0][2:]), parts[1]
            if name == SGX_PCK_EXTENSION + ".2":
                for _, _, c_start, c_end in children(data, value_start, value_end):
                    sub = children(data, c_start, c_end)
                    component, (s_tag, _, s_start, s_end) = oid(data, *sub[0][2:]), sub[1]
                    value = data[s_start:s_end]
                    found["tcb." + component.rsplit(".", 1)[1]] = value if s_tag == 0x04 else int.from_bytes(value, "big")
            else:
                found[name] = data[value_start:value_end]
        return {"cpu_svn": bytes(found["tcb." + str(i)] for i in range(1, 17)), "pce_svn": found["tcb.17"],
                "fmspc": found[SGX_PCK_EXTENSION + ".4"]}
    except (KeyError, TypeError, ValueError, IndexError):
        raise QuoteInvalid("The PCK certificate's Intel SGX extension is incomplete") from None


def tdx_current(document, at, what):
    if not tdx_time(document["issueDate"]) <= at <= tdx_time(document["nextUpdate"]):
        raise QuoteInvalid(what + " is not current at " + at.isoformat() + " (issued " + str(document["issueDate"])
                           + ", next update " + str(document["nextUpdate"]) + ")")


def tdx_document(collateral, name, root, crls, at, what):
    chain = tdx_chain(tdx_certificates(collateral[name + "_issuer_chain"]), root, at, what, crls)
    if len(chain) != 1:
        raise QuoteInvalid(what + " must be signed by a certificate the root issued directly")
    text = collateral[name]
    tdx_signature(chain[0].public_key(), bytes.fromhex(collateral[name + "_signature"]), text.encode(), what)
    return json.loads(text)


def tdx_converge(platform, component):
    if platform not in TDX_STATUSES or component not in TDX_QE_STATUSES:
        raise QuoteInvalid("Unsupported TCB status convergence: " + str(platform) + ", " + str(component))
    if component == "Revoked":
        return "Revoked"
    if component == "OutOfDate" and platform in ("UpToDate", "SWHardeningNeeded"):
        return "OutOfDate"
    if component == "OutOfDate" and platform in ("ConfigurationNeeded", "ConfigurationAndSWHardeningNeeded"):
        return "OutOfDateConfigurationNeeded"
    return platform


def tdx_relaunch(launch, current):
    configuration = ("ConfigurationNeeded", "OutOfDateConfigurationNeeded", "ConfigurationAndSWHardeningNeeded",
                     "TDRelaunchAdvisedConfigurationNeeded")
    if launch in ("OutOfDate", "OutOfDateConfigurationNeeded") and current in (
            "UpToDate", "SWHardeningNeeded", "ConfigurationNeeded", "ConfigurationAndSWHardeningNeeded"):
        return "TDRelaunchAdvisedConfigurationNeeded" if launch in configuration or current in configuration \
            else "TDRelaunchAdvised"
    return launch


def tdx_components(level, key):
    return [c["svn"] for c in level["tcb"].get(key) or []]


def tdx_module_identity(tcb_info, svn):
    if svn[1] == 0:
        return None
    wanted = "TDX_%02X" % svn[1]
    for identity in tcb_info.get("tdxModuleIdentities") or []:
        if identity["id"].upper() == wanted:
            return identity
    raise QuoteInvalid("TCB Info has no TDX module identity " + wanted)


def tdx_platform_level(tcb_info, cpu_svn, pce_svn, svn):
    skip = 2 if svn[1] > 0 else 0
    levels = sorted(tcb_info["tcbLevels"], reverse=True, key=lambda level: (
        tdx_components(level, "sgxtcbcomponents"), level["tcb"]["pcesvn"], tdx_components(level, "tdxtcbcomponents")))
    for level in levels:
        sgx, td = tdx_components(level, "sgxtcbcomponents"), tdx_components(level, "tdxtcbcomponents")
        if len(sgx) != 16 or len(td) != 16:
            raise QuoteInvalid("TCB Info has a level without 16 SGX and 16 TDX components")
        if all(have >= need for have, need in zip(cpu_svn, sgx)) and pce_svn >= level["tcb"]["pcesvn"] and \
                all(have >= need for have, need in list(zip(svn, td))[skip:]):
            if level["tcbStatus"] not in TDX_STATUSES:
                raise QuoteInvalid("Unrecognized TCB status " + str(level["tcbStatus"]))
            status, advisories, date = level["tcbStatus"], list(level.get("advisoryIDs") or []), level["tcbDate"]
            identity = tdx_module_identity(tcb_info, svn)
            if identity:
                module = next((m for m in identity["tcbLevels"] if svn[0] >= m["tcb"]["isvsvn"]), None)
                if module is None:
                    raise QuoteInvalid("The TDX module ISVSVN " + str(svn[0]) + " is below every module TCB level")
                if module["tcbStatus"] not in TDX_QE_STATUSES:
                    raise QuoteInvalid("Unrecognized TDX module TCB status " + str(module["tcbStatus"]))
                status = tdx_converge(status, module["tcbStatus"])
                advisories += [a for a in module.get("advisoryIDs") or [] if a not in advisories]
                date = min(date, module["tcbDate"], key=tdx_time)
            return status, advisories, date
    raise QuoteInvalid("No TCB level of this platform is listed in Intel's TCB Info")


def tdx_check_module(tcb_info, report):
    base = tcb_info.get("tdxModule")
    if not base:
        raise QuoteInvalid("TDX TCB Info has no tdxModule")
    expected = tdx_module_identity(tcb_info, report["tee_tcb_svn"]) or base
    if bytes.fromhex(expected["mrsigner"]) != report["mr_signer_seam"]:
        raise QuoteInvalid("The TDX module is not signed by the signer Intel lists")
    attributes, mask = bytes.fromhex(expected["attributes"]), bytes.fromhex(expected["attributesMask"])
    for want, bits, have in zip(attributes, mask, report["seam_attributes"]):
        if want & bits != have & bits or have & ~bits & 0xFF:
            raise QuoteInvalid("The TDX module attributes differ from Intel's")


def tdx_check_qe(qe_report, identity):
    if qe_report[128:160] != bytes.fromhex(identity["mrsigner"]):
        raise QuoteInvalid("The quoting enclave is not signed by Intel")
    if qe_report[48] & 0x02:
        raise QuoteInvalid("The quoting enclave runs in debug mode")
    if struct.unpack_from("<H", qe_report, 256)[0] != identity["isvprodid"]:
        raise QuoteInvalid("The quoting enclave has the wrong product ID")
    mask = int.from_bytes(bytes.fromhex(identity["miscselectMask"]), "little")
    if struct.unpack_from("<I", qe_report, 16)[0] & mask != int.from_bytes(bytes.fromhex(identity["miscselect"]),
                                                                           "little") & mask:
        raise QuoteInvalid("The quoting enclave's MISCSELECT differs from Intel's")
    for want, bits, have in zip(bytes.fromhex(identity["attributes"]), bytes.fromhex(identity["attributesMask"]),
                                qe_report[48:64]):
        if want & bits != have & bits:
            raise QuoteInvalid("The quoting enclave's attributes differ from Intel's")
    svn = struct.unpack_from("<H", qe_report, 258)[0]
    for level in identity["tcbLevels"]:
        if svn >= level["tcb"]["isvsvn"]:
            if level["tcbStatus"] not in TDX_QE_STATUSES:
                raise QuoteInvalid("Unrecognized QE TCB status " + str(level["tcbStatus"]))
            return level["tcbStatus"], list(level.get("advisoryIDs") or [])
    raise QuoteInvalid("The quoting enclave's SVN is below every level Intel lists")


def tdx_problems(report):
    attributes, problems = int.from_bytes(report["td_attributes"], "little"), []
    if attributes & 0x01:
        problems.append("the TD runs in debug mode: the host can read its memory and registers")
    if attributes & 0x70:
        problems.append("TD profiling is enabled")
    if attributes & TDX_RESERVED_ATTRIBUTES:
        problems.append("reserved TD attribute bits are set")
    if attributes & (1 << 29):
        problems.append("the TD can be migrated to another machine")
    if attributes & (1 << 17):
        problems.append("service TD extensions are enabled")
    if not attributes & (1 << 28):
        problems.append("SEPT_VE_DISABLE is off")
    if report.get("mr_service_td", bytes(48)) != bytes(48):
        problems.append("a service TD is bound to this TD")
    return problems


def tdx_tcb(quote, chain, collateral, root, at):
    crl_data = [bytes.fromhex(collateral[name]) for name in ("root_ca_crl", "pck_crl")]
    moments = [tdx_time(json.loads(collateral[name])["issueDate"]) for name in ("tcb_info", "qe_identity")]
    at = max([at] + moments + [x509.load_der_x509_crl(data).last_update_utc for data in crl_data])
    crls = {root.subject.public_bytes(): tdx_crl(crl_data[0], root, at, "Intel's root revocation list")}
    pck_ca = tdx_chain(tdx_certificates(collateral["pck_crl_issuer_chain"]), root, at,
                       "The PCK revocation list issuer", crls)[0]
    crls[pck_ca.subject.public_bytes()] = tdx_crl(crl_data[1], pck_ca, at, "The PCK revocation list")
    tcb_info = tdx_document(collateral, "tcb_info", root, crls, at, "Intel's TCB Info")
    identity = tdx_document(collateral, "qe_identity", root, crls, at, "Intel's QE Identity")
    tdx_current(tcb_info, at, "Intel's TCB Info")
    tdx_current(identity, at, "Intel's QE Identity")
    if tcb_info.get("id") != "TDX" or tcb_info.get("version", 0) < 3:
        raise QuoteInvalid("The collateral's TCB Info is not for TDX")
    if identity.get("id") != "TD_QE" or identity.get("version") not in (2, 3):
        raise QuoteInvalid("The collateral's QE Identity is not for the TDX quoting enclave")
    chain = tdx_chain(chain, root, at, "The PCK certificate chain", crls)
    if chain[-1].subject != pck_ca.subject:
        raise QuoteInvalid("The PCK certificate and the revocation list come from different Intel CAs")
    qe_status, qe_advisories = tdx_check_qe(quote["qe_report"], identity)
    platform, report = tdx_pck(chain[0]), quote["report"]
    if bytes.fromhex(tcb_info["fmspc"]) != platform["fmspc"]:
        raise QuoteInvalid("Intel's TCB Info is for another platform (FMSPC)")
    status, advisories, date = tdx_platform_level(tcb_info, platform["cpu_svn"], platform["pce_svn"],
                                                  report["tee_tcb_svn"])
    tdx_check_module(tcb_info, report)
    current = None
    if "tee_tcb_svn2" in report:
        current = tdx_converge(tdx_platform_level(tcb_info, platform["cpu_svn"], platform["pce_svn"],
                                                  report["tee_tcb_svn2"])[0], qe_status)
    status = tdx_converge(status, qe_status)
    advisories += [a for a in qe_advisories if a not in advisories]
    if status == "Revoked" or current == "Revoked":
        raise QuoteInvalid("Intel has revoked this platform's TCB")
    if current:
        status = tdx_relaunch(status, current)
    return {"status": status, "advisory_ids": advisories, "tcb_date": date, "qe_status": qe_status,
            "collateral_issued": tcb_info["issueDate"], "evaluated_at": at.isoformat(),
            "revocation": "PCK chain checked against Intel's revocation lists",
            "detail": "Intel TCB status " + status + (" with " + ", ".join(advisories[:12]) if advisories else "")
                      + "; TCB level of " + str(date) + ", quoting enclave " + qe_status + "; Intel collateral issued "
                      + str(tcb_info["issueDate"]) + ", evaluated at " + at.isoformat()}


def tdx_verify(raw, binding, at, collateral=None):
    root, quote, at = tdx_root(), tdx_quote(raw), tdx_time(at)
    chain = tdx_chain(tdx_certificates(quote["pck_chain"]), root, at, "The PCK certificate chain")
    names = [", ".join(a.value for a in c.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)) for c in chain]
    if len(chain) != 2 or names[0] != "Intel SGX PCK Certificate" or names[1] not in INTEL_PCK_CAS:
        raise QuoteInvalid("The quote's certificates are not a PCK certificate under an Intel SGX PCK CA")
    pck, qe = chain[0], quote["qe_report"]
    tdx_signature(pck.public_key(), quote["qe_signature"], qe, "The quoting enclave report")
    if len(quote["qe_auth"]) != 32 or \
            qe[320:384] != hashlib.sha256(quote["attestation_key"] + quote["qe_auth"]).digest() + bytes(32):
        raise QuoteInvalid("The quoting enclave report does not name the key that signed the quote")
    if qe[128:160] != INTEL_TD_QE_SIGNER or struct.unpack_from("<H", qe, 256)[0] != 2 or qe[48] & 0x02:
        raise QuoteInvalid("The quoting enclave report is not from Intel's TDX quoting enclave in production mode")
    try:
        key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), b"\x04" + quote["attestation_key"])
    except ValueError:
        raise QuoteInvalid("The quote's attestation key is not a P-256 point") from None
    tdx_signature(key, quote["signature"], quote["signed"], "The TD report")
    report = quote["report"]
    problems = tdx_problems(report)
    if problems:
        raise QuoteInvalid("; ".join(problems))
    if report["report_data"] != hashlib.sha512(canonical(binding)).digest():
        raise QuoteInvalid("The quote's report data is not SHA-512 of this record: it vouches for something else")
    platform, tcb = tdx_pck(pck), None
    if collateral:
        try:
            tcb = tdx_tcb(quote, chain, collateral, root, at)
        except QuoteInvalid:
            raise
        except (KeyError, TypeError, ValueError, IndexError, AttributeError) as exc:
            raise QuoteInvalid("Intel's collateral is incomplete or unreadable: " + type(exc).__name__) from None
    return {"quote_version": quote["version"], "pck_ca": names[1], "fmspc": platform["fmspc"].hex(),
            "pck_sha256": pck.fingerprint(hashes.SHA256()).hex(), "qe_svn": struct.unpack_from("<H", qe, 258)[0],
            **{name: report[name].hex() for name in TDX_MEASUREMENTS}, "td_attributes": report["td_attributes"].hex(),
            "tcb": tcb}


def tdx_check(evidence, binding, at, source, binds):
    if evidence.get("error") or not evidence.get("quote"):
        return {"status": "missing", "detail": "no Intel TDX quote",
                **({"error": str(evidence["error"])[:200]} if evidence.get("error") else {})}
    try:
        found = tdx_verify(bytes.fromhex(evidence["quote"]), binding, at, evidence.get("collateral"))
    except (ValueError, KeyError, TypeError, IndexError, struct.error) as exc:
        return {"status": "fail", "detail": str(exc) or type(exc).__name__}
    if found["tcb"] is None:
        found["tcb"] = {"status": "not checked", "detail": "TCB status not checked (no collateral in the " + source + ")",
                        "revocation": "not checked",
                        **({"collector_error": str(evidence["collateral_error"])[:200]}
                           if evidence.get("collateral_error") else {})}
    return {"status": "pass", **found, "binds": binds}


def tdx_summary(quotes):
    return {"status": "pass" if all(q["status"] == "pass" for q in quotes) else "fail", "checked": "offline",
            "root": "Intel SGX Root CA pinned in this verifier", "root_sha256": INTEL_SGX_ROOT_SHA256,
            "quotes": quotes, "not_checked": TDX_NOT_CHECKED}


def tdx_start_binding(run):
    value = {"format": "tgwitness-tdx-start-v1", "public_key": run.get("public_key"), "run_id": run.get("run_id"),
             "source_tree_sha256": run.get("source_tree_sha256"), "host": run.get("host")}
    if "source_policy" in run:
        value["source_policy"] = run["source_policy"]
    return value


def verify_tdx_starts(starts, public_key):
    runs = [(event, event["payload"]["run"] if isinstance(event["payload"].get("run"), dict) else {}) for event in starts]
    if not any(run.get("tdx_start") for _, run in runs):
        return None
    quotes = []
    for event, run in runs:
        evidence = run["tdx_start"] if isinstance(run.get("tdx_start"), dict) else {}
        if evidence.get("quote") and run.get("public_key") != public_key:
            entry = {"status": "fail", "detail": "the quoted start names another key than this journal's"}
        else:
            entry = tdx_check(evidence, tdx_start_binding(run), event["observed_at"], "archive",
                              "the start record: journal key, run, source tree and host")
        quotes.append({"record": event["seq"], "at": event["observed_at"], **entry})
    return tdx_summary(quotes)


def verify_collector_attestation(data, expected_fingerprint=None):
    record = data.get("format") in ATTESTATION_RECORDS
    answer = (data.get("collector") or {}).get("statement") if record else data
    if not isinstance(answer, dict) or "statement" not in answer or "signature" not in answer:
        raise ValueError("The record carries no signed collector statement")
    statement = authenticate_statement(answer)
    if statement.get("format") != "tgwitness-assurance-v1":
        raise VerifierTooOld("Unsupported collector statement format")
    fp = fingerprint(statement["public_key"])
    if statement.get("fingerprint") != fp:
        raise ValueError("The statement's fingerprint does not belong to its key")
    if record and data["collector"].get("fingerprint") not in (None, fp):
        raise ValueError("The record names another collector key than its signed statement")
    if expected_fingerprint and fp != expected_fingerprint:
        raise ValueError("Public key differs from the independently trusted fingerprint")
    result = {"format": statement["format"], "fingerprint": fp, "key_pinned": bool(expected_fingerprint),
              **{name: statement.get(name) for name in ("created_at", "run_id", "run_event_seq", "version",
                                                        "source_tree_sha256", "challenge")}}
    if isinstance(answer.get("tdx"), dict):
        entry = tdx_check(answer["tdx"], statement, statement.get("created_at"), "file",
                          "the signed collector statement: key, challenge, run and host")
        result["tdx"] = tdx_summary([{"at": statement.get("created_at"), **entry}])
    return result


def tdx_lines(tdx):
    if not tdx:
        return []
    lines = []
    for quote in tdx["quotes"]:
        where = "Intel TDX quote" + (" at record " + str(quote["record"]) if "record" in quote else "")
        if quote["status"] != "pass":
            lines.append(where + ": " + quote["status"] + " · " + quote["detail"]
                         + (" (" + quote["error"] + ")" if quote.get("error") else ""))
            continue
        lines.append(where + ": verified offline; signature, quoting enclave and PCK chain to the pinned Intel SGX "
                     "Root CA are valid (quote v" + str(quote["quote_version"]) + ", " + quote["pck_ca"] + ", FMSPC "
                     + quote["fmspc"] + ")")
        lines += [{"report_data": "REPORTDATA"}.get(name, name.upper()) + ": " + quote[name] for name in TDX_MEASUREMENTS]
        lines.append("REPORTDATA is SHA-512 of " + quote["binds"])
        lines.append(quote["tcb"]["detail"])
    lines.append("Not checked offline: " + tdx["not_checked"])
    return lines


def is_format(value, name):
    return value in ("tgwitness-" + name, "tgwatch-" + name)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def fingerprint(public_key):
    return hashlib.sha256(base64.b64decode(public_key, validate=True)).hexdigest()


MERKLE_EMPTY = hashlib.sha256(b"").digest()


def merkle_leaf(event_hash):
    return hashlib.sha256(b"\x00" + bytes.fromhex(event_hash)).digest()


def merkle_node(left, right):
    return hashlib.sha256(b"\x01" + left + right).digest()


def hash_bytes(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("Malformed SHA-256 commitment")
    return bytes.fromhex(value)


class MerkleFrontier:
    def __init__(self):
        self.nodes = []
        self.count = 0

    def append(self, event_hash):
        node, level, count = merkle_leaf(event_hash), 0, self.count
        while count & 1:
            node = merkle_node(self.nodes[level], node)
            self.nodes[level] = None
            count >>= 1
            level += 1
        if level == len(self.nodes):
            self.nodes.append(node)
        else:
            self.nodes[level] = node
        self.count += 1

    def root(self):
        result = None
        for node in self.nodes:
            if node is not None:
                result = node if result is None else merkle_node(node, result)
        return result if result is not None else MERKLE_EMPTY


def merkle_path(value):
    if not isinstance(value, list) or len(value) > 64:
        raise ValueError("Malformed or excessive Merkle proof")
    return [hash_bytes(node) for node in value]


def verify_inclusion(event_hash, index, size, root, path):
    if not 0 <= index < size:
        raise ValueError("Merkle leaf outside tree")
    fn, sn, calculated = index, size - 1, merkle_leaf(event_hash)
    for node in merkle_path(path):
        if sn == 0:
            raise ValueError("Excess Merkle inclusion nodes")
        if fn & 1 or fn == sn:
            calculated = merkle_node(node, calculated)
            while fn and not fn & 1:
                fn >>= 1
                sn >>= 1
        else:
            calculated = merkle_node(calculated, node)
        fn >>= 1
        sn >>= 1
    if sn != 0 or calculated != root:
        raise ValueError("Event is not included in committed tree")


def verify_consistency(first, second, first_root, second_root, path):
    nodes = merkle_path(path)
    if not 0 <= first <= second:
        raise ValueError("Invalid Merkle tree sizes")
    if first == 0:
        if nodes or first_root != MERKLE_EMPTY or (second == 0 and second_root != MERKLE_EMPTY):
            raise ValueError("Invalid empty-tree consistency proof")
        return
    if first == second:
        if nodes or first_root != second_root:
            raise ValueError("Equal-size Merkle trees differ")
        return
    if not nodes:
        raise ValueError("Missing Merkle consistency proof")
    if first & (first - 1) == 0:
        nodes.insert(0, first_root)
    fn, sn = first - 1, second - 1
    while fn & 1:
        fn >>= 1
        sn >>= 1
    fr = sr = nodes[0]
    for node in nodes[1:]:
        if sn == 0:
            raise ValueError("Excess Merkle consistency nodes")
        if fn & 1 or fn == sn:
            fr, sr = merkle_node(node, fr), merkle_node(node, sr)
            while fn and not fn & 1:
                fn >>= 1
                sn >>= 1
        else:
            sr = merkle_node(sr, node)
        fn >>= 1
        sn >>= 1
    if sn != 0 or fr != first_root or sr != second_root:
        raise ValueError("Journal does not extend the previously committed tree")


def verify_continuity(value, checkpoint, previous=None, challenge=None):
    statement, proof = value["statement"], value["proof"]
    if (set(value) != {"statement", "signature", "proof"}
            or set(statement) != {"format", "public_key", "event_count", "head_hash", "root", "challenge"}
            or set(proof) != {"from_count", "consistency", "head_path", "previous_head_path"}
            or statement["format"] != "tgwitness-continuity-v1"):
        raise ValueError("Unexpected continuity proof fields")
    count, start = statement["event_count"], proof["from_count"]
    if any(type(n) is not int or not 0 <= n < 2**63 for n in (count, start)) or start > count:
        raise ValueError("Invalid continuity boundary")
    root = hash_bytes(statement["root"])
    hash_bytes(statement["head_hash"])
    if not isinstance(statement["challenge"], str) or not re.fullmatch(r"[0-9a-f]{32}", statement["challenge"]):
        raise ValueError("Missing continuity challenge")
    if statement["challenge"] != challenge:
        raise ValueError("Continuity challenge differs from this check")
    for field in ("public_key", "event_count", "head_hash"):
        if statement[field] != checkpoint[field]:
            raise ValueError("Continuity proof differs from checkpoint: " + field)
    Ed25519PublicKey.from_public_bytes(base64.b64decode(statement["public_key"], validate=True)).verify(
        base64.b64decode(value["signature"], validate=True), canonical(statement))
    if count:
        verify_inclusion(statement["head_hash"], count - 1, count, root, proof["head_path"])
    elif root != MERKLE_EMPTY or statement["head_hash"] != "0" * 64 or proof["head_path"]:
        raise ValueError("Invalid empty journal commitment")
    expected = previous["event_count"] if previous else 0
    if start != expected:
        raise ValueError("Continuity proof starts at a different retained boundary")
    if start:
        verify_inclusion(previous["head_hash"], start - 1, count, root, proof["previous_head_path"])
    elif proof["previous_head_path"]:
        raise ValueError("Unexpected previous-head proof for empty journal")
    if previous and previous.get("root"):
        verify_consistency(start, count, hash_bytes(previous["root"]), root, proof["consistency"])
    elif start == 0:
        verify_consistency(0, count, MERKLE_EMPTY, root, proof["consistency"])
    else:


        merkle_path(proof["consistency"])
    return statement


LIVENESS_GAP_SECONDS = 180
CHANNEL_IDS_BELOW = -1000000000000
MESSAGE_KINDS = ("message.new", "message.snapshot", "message.edited", "message.recovered",
                 "message.deleted", "message.missing_on_recheck")
INTERRUPTIONS = {"transport_disconnected": "connection to Telegram lost",
                 "authorization_required": "Telegram signed the account out",
                 "resume_failed": "observation could not resume after a restart"}
SESSION_NOTES = {"updates_diverted": "Telegram's update counter grew while no update reached this session",
                 "session_revoked_externally": "this session left Telegram's session list while its connection kept working",
                 "concurrent_sessions_at_start": "other sessions were signed in when observation started",
                 "probe_ack_missed_live": "the witness answered a probe, but the answer reached this session only "
                                          "from history, not live"}
SESSION_WINDOWS = ("updates_diverted", "session_revoked_externally", "probe_ack_missed_live")
PROBE_KINDS = {"probe.sent": "sent", "probe.acked": "answered live", "probe.unanswered": "unanswered",
               "probe.inconclusive": "inconclusive"}
WITNESS_PROBE_KINDS = {"probe.seen": "seen", "probe.ack_sent": "answered", "probe.ack_failed": "answer failed"}
SOURCE_KINDS = ("message.new", "message.snapshot", "message.recovered", "message.edited")
SOURCE_GROUPS = (("live observation", ("live_update", "update_recovery")),
                 ("history reads", ("history_snapshot", "baseline_snapshot", "new_chat_snapshot", "history_acquisition",
                                    "recheck")),
                 ("panel actions", ("panel_action", "panel_button_check")))
KEY_ORIGINS = {"created": "created by signing in from this workspace", "imported": "imported from an existing session"}
LOGIN_METHODS = {"qr": "QR code", "phone_code": "phone code", "session_import": "session import"}
ACCOUNT_LOSS = {"account_banned": "account banned", "account_deleted": "account deleted",
                "account_frozen": "account frozen", "session_duplicated": "session used in two places",
                "session_revoked": "session revoked", "session_expired": "session expired",
                "session_ended": "session no longer recognised", "not_authorized": "no reason given"}


def missing_ranges(ordered):
    return [(a + 1, b - 1) for a, b in zip(ordered, ordered[1:]) if b - a > 1]


def numbered_per_chat(chat_id):
    return isinstance(chat_id, int) and chat_id < CHANNEL_IDS_BELOW


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class Coverage:
    def __init__(self, gap_settings=None, *, chats_selected=False, senders_selected=False):
        self.sequences = Sequences(gap_settings, chats_selected=chats_selected, senders_selected=senders_selected)
        self.periods, self.gaps, self.notes = [], [], []
        self.start = self.alive = self.closed_at = self.close_reason = None
        self.observing = self.active = False
        self.run_id = None
        self.ids, self.titles = {}, {}
        self.first = self.last = None
        self.allowed = LIVENESS_GAP_SECONDS
        self.session = {}
        self.held, self.windows, self.sources, self.sealed_run = {}, [], {}, False

    def open(self, at):
        if self.held:
            self.alive = at
            return
        if self.closed_at is not None:
            self.gaps.append({"from": self.closed_at, "to": at, "reason": self.close_reason})
            self.closed_at = None
        self.start, self.alive, self.observing = at, at, True

    def close(self, at, reason):
        if self.observing:
            self.periods.append({"from": self.start, "to": at})
            self.observing, self.closed_at, self.close_reason = False, at, reason

    def hold(self, reason, at):
        self.close(at, SESSION_NOTES[reason])
        self.held.setdefault(reason, at)

    def release(self, reason, at, resume=False):
        since = self.held.pop(reason, None)
        if since is not None:
            self.windows.append({"from": since, "to": at, "reason": reason})
            if resume and self.active:
                self.open(at)

    def add(self, event):
        at, kind, payload, chat_id = event["observed_at"], event["kind"], event["payload"], event["chat_id"]
        self.first, self.last = self.first or at, at
        if self.observing and kind not in ("observation.started", "process.started"):
            silent = (parse_time(at) - parse_time(self.alive)).total_seconds()
            if silent > self.allowed:
                self.close(self.alive, "no capture heartbeat for " + str(round(silent / 60)) + " min while observing: "
                           "the process stopped, froze or the computer slept")
        heartbeat = (kind == "collector.heartbeat" and self.active
                     and (self.run_id is None or payload.get("run_id") == self.run_id))
        interval = payload.get("interval_seconds") if heartbeat else \
            (payload.get("parameters") or {}).get("heartbeat_seconds") if kind == "observation.started" else None
        if type(interval) is int and interval > 0:
            self.allowed = max(LIVENESS_GAP_SECONDS, 3 * interval)
        changed = (payload.get("after") or {}).get("heartbeat_seconds") if kind == "parameters.changed" else None
        if type(changed) is int and changed > 0:

            self.allowed = max(self.allowed, 3 * changed)
        if kind == "observation.started":
            self.close(self.alive, "observation restarted")
            self.release("updates_diverted", at)
            self.release("probe_ack_missed_live", at)
            self.open(at)
            self.active, self.run_id = True, payload.get("run_id")
        elif kind == "observation.stopped":
            self.close(at, "observation paused by the operator" if payload.get("reason") == "operator"
                       else "observation stopped: " + str(payload.get("reason") or "unknown"))
            self.release("updates_diverted", at)
            self.release("probe_ack_missed_live", at)
            self.active = False
        elif kind == "process.stopped":
            self.close(at, "collector process stopped")
            self.release("updates_diverted", at)
            self.release("probe_ack_missed_live", at)
            self.active = False
        elif kind == "process.started":
            self.close(self.alive, "collector process ended without an orderly stop")
            self.release("updates_diverted", at)
            self.release("probe_ack_missed_live", at)
            self.active = False
        elif kind == "collector.error":
            self.close(self.alive, "collector error: capture may be incomplete")
            self.notes.append({"at": at, "chat_id": chat_id, "reason": "collector_error",
                               "operation": payload.get("operation"), "error_type": payload.get("error_type")})
            if payload.get("observation_stopped") is True:
                self.active = False
        elif kind == "connection.closed" and payload.get("role") in (None, "current"):
            self.close(at, "connection to Telegram closed")
        elif kind == "connection.restored" and payload.get("reason") == "updates_resumed":
            self.release("updates_diverted", at, resume=True)
        elif kind == "connection.restored" and payload.get("reason") == "probe_ack_live":
            self.release("probe_ack_missed_live", at, resume=True)
        elif kind == "account.authorized":
            self.release("session_revoked_externally", at, resume=True)
        elif kind == "coverage.gap":
            reason = payload.get("reason")
            if chat_id is None and reason in INTERRUPTIONS:
                cause = ACCOUNT_LOSS.get(payload.get("cause")) if reason == "authorization_required" else None
                self.close(at, INTERRUPTIONS[reason] + (": " + cause if cause else ""))
                if reason != "transport_disconnected":
                    self.active = False
            elif chat_id is None and reason in SESSION_WINDOWS:
                self.hold(reason, at)
            else:
                self.notes.append({"at": at, "chat_id": chat_id, "reason": reason})
        elif heartbeat:
            if payload.get("connected") is True:
                if not self.observing:
                    self.open(at)
                self.alive = at
            elif payload.get("connected") is False:
                self.close(at, "collector heartbeat reports Telegram disconnected")
        if chat_id is not None and isinstance(payload.get("title"), str) and kind in (
                "target.changed", "source.discovered", "target.removed"):
            self.titles[chat_id] = payload["title"]
        if kind == "scope.applied":
            for added in payload.get("added") or []:
                self.titles[added.get("chat_id")] = added.get("title")
        if kind in MESSAGE_KINDS and numbered_per_chat(chat_id) and isinstance(event["message_id"], int):
            self.ids.setdefault(chat_id, set()).add(event["message_id"])
        self.session_event(at, kind, payload)
        if kind in SOURCE_KINDS or kind == "capture.opened":
            source = "recorder_capture" if kind == "capture.opened" else payload.get("source")
            source = source if isinstance(source, str) else "unlabelled"
            self.sources[source] = self.sources.get(source, 0) + 1
            if self.sealed_run and kind in SOURCE_KINDS:
                self.sources["inside_sealed_run"] = self.sources.get("inside_sealed_run", 0) + 1
        elif kind in ("sealed.started", "sealed.finished"):
            self.sealed_run = kind == "sealed.started"
        self.sequences.add(event, MESSAGE_KINDS)

    def session_event(self, at, kind, payload):
        s = self.session
        if kind == "account.authorized":
            s["key_origin"], s["login_method"], s["authorized_at"] = (payload.get("key_origin"),
                                                                       payload.get("login_method"), at)
        elif kind == "session.import_warning":
            s.setdefault("import_warning_at", at)
        elif kind == "account.security_event":
            counts = s.setdefault("security_events", {})
            name = str(payload.get("event_kind") or "security_notice")
            counts[name] = counts.get(name, 0) + 1
        elif kind == "account.all_other_sessions_terminated":
            s.setdefault("other_sessions_ended", []).append({"at": at, "ended": payload.get("sessions_before")})
        elif kind == "account.password_changed":
            s.setdefault("password_changes", []).append({"at": at, "operation": payload.get("operation")})
        elif kind == "account.phone_call":
            s["phone_calls"] = s.get("phone_calls", 0) + 1
        elif kind in PROBE_KINDS or kind == "coverage.gap" and payload.get("reason") == "probe_ack_missed_live":
            probes = s.setdefault("probes", {})
            name = PROBE_KINDS.get(kind, "answer missed live")
            probes[name] = probes.get(name, 0) + 1
            delay = payload.get("delay_seconds")
            if kind == "probe.acked" and isinstance(delay, (int, float)):
                s["probe_delay_max"] = max(s.get("probe_delay_max", 0), delay)
        elif kind in WITNESS_PROBE_KINDS:
            answers = s.setdefault("probe_answers", {})
            for name in (WITNESS_PROBE_KINDS[kind], "seen live" if kind == "probe.seen" and payload.get("via") == "push"
                         else None):
                if name:
                    answers[name] = answers.get(name, 0) + 1
        elif kind == "session.exclusive_from":
            s.setdefault("only_session", []).append({"from": at, "ended": payload.get("other_sessions_ended"),
                                                    "two_step": payload.get("two_step")})
        elif kind == "session.exclusive_automatic":
            s["only_session_automatic"] = {"at": at, "enabled": payload.get("enabled") is True}
        elif kind == "session.exclusive_postponed":
            s["only_session_postponed"] = s.get("only_session_postponed", 0) + 1
        elif kind == "session.exclusive_ended" and s.get("only_session"):
            s["only_session"][-1]["until"] = at
        elif kind == "session.security_baseline" and payload.get("trigger") == "observation_start" \
                and payload.get("other_sessions") == 0 and type(payload.get("other_sessions")) is int:
            s.setdefault("sessions_at_start", []).append({"at": at, "others": 0})
        elif (kind == "session.concurrent_at_start"
              or kind == "coverage.gap" and payload.get("reason") == "concurrent_sessions_at_start"):
            count = payload.get("concurrent_sessions")
            if type(count) is not int:
                count = len(payload["sessions"]) if isinstance(payload.get("sessions"), list) else None
            s.setdefault("sessions_at_start", []).append({"at": at, "others": count})
        elif kind == "account.sessions" and self.active and isinstance(payload.get("added"), list) and payload["added"]:
            s.setdefault("sessions_added", []).append({"at": at, "added": len(payload["added"])})

    def result(self, ranges_per_chat=50):
        periods = [dict(p) for p in self.periods]
        if self.observing:
            periods.append({"from": self.start, "to": self.alive, "still_observing": True})
        for period in periods:
            period["seconds"] = round((parse_time(period["to"]) - parse_time(period["from"])).total_seconds())
        gaps = [dict(g) for g in self.gaps]
        if not self.observing and self.closed_at is not None:
            gaps.append({"from": self.closed_at, "to": self.last, "reason": self.close_reason,
                         "not_resumed_by_last_record": True})
        windows = [dict(w) for w in self.windows] + [
            {"from": since, "to": self.last, "reason": reason, "not_resumed_by_last_record": True}
            for reason, since in self.held.items()]
        unobserved = []
        for chat_id, ids in sorted(self.ids.items()):
            ordered = sorted(ids)
            holes = missing_ranges(ordered)
            unobserved.append({"chat_id": chat_id, "title": self.titles.get(chat_id),
                               "observed_from": ordered[0], "observed_to": ordered[-1], "observed": len(ordered),
                               "not_observed": sum(high - low + 1 for low, high in holes),
                               "ranges": [{"low": low, "high": high} for low, high in holes[:ranges_per_chat]],
                               "ranges_total": len(holes)})
        return {"continuous": periods, "gaps": gaps, "session_windows": sorted(windows, key=lambda w: w["from"]),
                "record_sources": dict(sorted(self.sources.items())),
                "notes": self.notes[:200], "notes_total": len(self.notes),
                "unobserved_ids": unobserved, "gap_summary": self.sequences.result(self.titles), "first_record": self.first, "last_record": self.last,
                "meaning": "Observation intervals follow connected capture heartbeats from the same run, within three "
                           "heartbeat intervals (at least three minutes). Each interval ends at its last capture "
                           "confirmation or recorded stop. Session windows, while Telegram's update counter grew "
                           "without updates reaching this session or while Telegram no longer listed it, are gaps. "
                           "Message-number gaps describe the observed numbering range.",
                **({"session": self.session} if self.session else {})}


GAP_DEFAULTS = {"gap_analysis": True, "gap_account_sequence": True, "gap_cluster_min": 1, "gap_clusters_listed": 20,
            "gap_service_estimate": False}
WIDE_TYPES = ("private", "groups", "bots")
GAP_MEANING = ("A gap is a message number between two observed messages that this collector never saw. Telegram assigns "
           "these numbers; a gap may be a message Telegram never showed to this account.")
ESTIMATE_MEANING = ("Estimate from the share of service messages among observed numbers. It describes the range "
                    "as a whole; the missing count stays as observed.")


def account_numbered(chat_id):
    return isinstance(chat_id, int) and chat_id > CHANNEL_IDS_BELOW


def gap_parameters(values=None):
    if values is not None and not isinstance(values, dict):
        raise ValueError("Gap parameters must be an object")
    values = {**GAP_DEFAULTS, **(values or {})}
    for key in ("gap_analysis", "gap_account_sequence", "gap_service_estimate"):
        if type(values[key]) is not bool:
            raise ValueError("Invalid gap parameter: " + key)
    for key, maximum in (("gap_cluster_min", 100000), ("gap_clusters_listed", 200)):
        if type(values[key]) is not int or not 1 <= values[key] <= maximum:
            raise ValueError("Invalid gap parameter: " + key)
    return {key: values[key] for key in GAP_DEFAULTS}


def not_applicable(reason):
    return {"status": "not_applicable", "reason": reason}


NOTICE_KINDS = ("message.deleted", "message.missing_on_recheck")


def summarize_gaps(times, settings, service=0, notices=()):
    ordered = sorted(times)
    if len(ordered) < 2:
        return not_applicable("Fewer than two observed messages; there is no range to measure.")
    holes = [(low + 1, high - 1) for low, high in zip(ordered, ordered[1:]) if high - low > 1]
    span = ordered[-1] - ordered[0] + 1
    missing = sum(high - low + 1 for low, high in holes)
    listed = [hole for hole in holes if hole[1] - hole[0] + 1 >= settings["gap_cluster_min"]]
    largest = sorted(listed, key=lambda hole: (hole[0] - hole[1], hole[0]))[:settings["gap_clusters_listed"]]
    result = {"status": "applicable", "observed_from": ordered[0], "observed_to": ordered[-1], "span": span,
              "observed": len(ordered), "observed_without_content": len(notices),
              "missing": missing, "density": round(missing / span, 6),
              "gap_ranges": len(holes), "largest_gap": max((high - low + 1 for low, high in holes), default=0),
              "clusters_total": len(listed),
              "clusters": [{"low": low, "high": high, "missing": high - low + 1,
                            "after": {"message_id": low - 1, "observed_at": times[low - 1]},
                            "before": {"message_id": high + 1, "observed_at": times[high + 1]}}
                           for low, high in sorted(largest)]}
    if settings["gap_service_estimate"]:
        share = service / len(ordered)
        result["service_estimate"] = {"service_share": round(share, 4),
                                      "expected_service_in_missing": round(missing * share),
                                      "meaning": ESTIMATE_MEANING}
    return result


def wide(scope):
    if not isinstance(scope, dict) or scope.get("mode") != "account":
        return False
    types = scope.get("types") if isinstance(scope.get("types"), dict) else {}
    excluded = [chat for chat in scope.get("exclude") or scope.get("excluded") or [] if account_numbered(chat)]
    return all(types.get(kind) is True for kind in WIDE_TYPES) and scope.get("own_actions") is True and not excluded


def scope_reason(scope):
    if not isinstance(scope, dict) or scope.get("mode") != "account":
        return ("Private chats, bots and ordinary groups share one account-wide numbering. It can be measured only "
                "while whole-account collection is on; this journal has no such period.")
    return ("Private chats, bots, ordinary groups and the account's own messages take numbers from the same "
            "sequence, so the measurement needs a scope recorded as including all of them without excluded chats.")


class Sequences:

    def __init__(self, settings=None, *, chats_selected=False, senders_selected=False):
        self.settings = gap_parameters(settings)
        self.chats_selected, self.senders_selected = chats_selected, senders_selected
        self.channels, self.services, self.content = {}, {}, {}
        self.account, self.account_service, self.account_content, self.window = {}, set(), set(), None
        self.scope, self.wide_since, self.wide_periods = None, None, 0
        self.paused, self.disabled, self.monitoring = False, set(), {}

    def add(self, event, message_kinds):
        if not self.settings["gap_analysis"]:
            return
        kind, chat_id, message_id = event["kind"], event["chat_id"], event["message_id"]
        payload = event["payload"] if isinstance(event["payload"], dict) else {}
        if kind == "scope.changed" and isinstance(payload.get("after"), dict):
            self.set_scope(payload["after"], event["observed_at"])
        elif kind == "scope.applied":
            self.set_scope({**(self.scope or {}), "mode": payload.get("mode"), "types": payload.get("types"),
                            "own_actions": payload.get("own_actions", (self.scope or {}).get("own_actions")),
                            "exclude": payload.get("excluded") or []}, event["observed_at"])
        elif kind in ("observation.stopped", "process.stopped", "process.started"):
            self.paused = True
        elif kind == "observation.started":
            if self.paused and self.wide_since is not None:
                self.wide_periods += 1
            self.paused = False
            if isinstance(payload.get("scope"), dict):
                self.set_scope(payload["scope"], event["observed_at"])
        elif kind == "target.changed" and account_numbered(chat_id):
            if payload.get("enabled") is False:
                self.disabled.add(chat_id)
            else:
                self.disabled.discard(chat_id)
            self.set_scope(self.scope, event["observed_at"])
        elif kind == "monitoring.changed" and isinstance(payload.get("after"), dict):
            self.monitoring = payload["after"]
            self.set_scope(self.scope, event["observed_at"])
        elif kind == "deletion.unscoped":
            for number in payload.get("message_ids") or []:
                if type(number) is int and number > 0:
                    self.account.setdefault(number, event["observed_at"])
        if type(message_id) is not int or message_id <= 0:
            return
        service = kind in ("chat.service", "membership.service")
        if numbered_per_chat(chat_id):
            if kind in message_kinds or service:
                self.channels.setdefault(chat_id, {}).setdefault(message_id, event["observed_at"])
                if kind not in NOTICE_KINDS:
                    self.content.setdefault(chat_id, set()).add(message_id)
            if service:
                self.services.setdefault(chat_id, set()).add(message_id)
        elif account_numbered(chat_id):
            if kind in message_kinds or service:
                self.account.setdefault(message_id, event["observed_at"])
                if kind not in NOTICE_KINDS:
                    self.account_content.add(message_id)
                if kind == "message.new" and self.wide_since is not None and not self.paused:
                    low, high = self.window or (message_id, message_id)
                    self.window = (min(low, message_id), max(high, message_id))
            if service:
                self.account_service.add(message_id)

    def set_scope(self, scope, at):
        self.scope = scope
        recorded = all(self.monitoring.get(kind, True) is not False for kind in ("messages", "membership"))
        if wide(scope) and not self.disabled and recorded:
            if self.wide_since is None:
                self.wide_since, self.wide_periods = at, self.wide_periods + 1
        else:
            self.wide_since = None

    def result(self, titles=None, chat_limit=None):
        titles = titles or {}
        settings = self.settings
        summary = {"parameters": settings, "meaning": GAP_MEANING, "chats": [], "account": None}
        if not settings["gap_analysis"]:
            summary["status"] = "off"
            return summary
        summary["status"] = "on"
        for chat_id in sorted(self.channels)[:chat_limit]:
            entry = {"chat_id": chat_id, "title": titles.get(chat_id), "numbering": "per chat"}
            if self.senders_selected:
                entry.update(not_applicable("Records were selected by sender, so other senders' numbers are absent."))
            else:
                times = self.channels[chat_id]
                entry.update(summarize_gaps(times, settings, len(self.services.get(chat_id, ())),
                                       [n for n in times if n not in self.content.get(chat_id, ())]))
            summary["chats"].append(entry)
        if chat_limit is not None and len(self.channels) > chat_limit:
            summary["chats_truncated"] = len(self.channels) - chat_limit
        summary["account"] = {"numbering": "account-wide: private chats, bots and ordinary groups",
                              **self.account_result()}
        return summary

    def account_result(self):
        if not self.settings["gap_account_sequence"]:
            return not_applicable("Turned off in Parameters → Gap analysis.")
        if self.chats_selected or self.senders_selected:
            return not_applicable("Records were selected by chat or sender; other chats take numbers from the "
                                  "same account-wide sequence.")
        if not self.wide_periods or self.window is None:
            return not_applicable(scope_reason(self.scope))
        low, high = self.window
        inside = {number: at for number, at in self.account.items() if low <= number <= high}
        result = summarize_gaps(inside, self.settings, len(self.account_service.intersection(inside)),
                           [n for n in inside if n not in self.account_content])
        result["window"] = "from the first to the last message that arrived while whole-account collection was on"
        if self.wide_periods > 1:
            result["note"] = ("Whole-account collection was switched off and on again; numbers used while it was off "
                              "appear as gaps.")
        return result


def session_lines(coverage):
    s, lines = coverage.get("session") or {}, []
    if s.get("key_origin"):
        lines.append("Telegram session key: " + KEY_ORIGINS.get(s["key_origin"], str(s["key_origin"]))
                     + (" by " + LOGIN_METHODS.get(s["login_method"], str(s["login_method"])) if s.get("login_method") else "")
                     + " at " + str(s.get("authorized_at")))
    windows = coverage.get("session_windows")
    for reason, label in SESSION_NOTES.items():
        if (windows is not None and reason in SESSION_WINDOWS
                or reason == "concurrent_sessions_at_start" and s.get("sessions_at_start")):
            continue
        found = [n["at"] for n in coverage.get("notes") or [] if n.get("reason") == reason and n.get("chat_id") is None]
        if found:
            lines.append("Session: " + label + " (" + str(len(found)) + "x, first " + found[0] + ")")
    for window in windows or []:
        lines.append("Session window from " + window["from"] + " to " + window["to"] + ": "
                     + SESSION_NOTES.get(window["reason"], str(window["reason"]))
                     + (", not resumed by the last record" if window.get("not_resumed_by_last_record") else ""))
    for item in s.get("sessions_at_start") or []:
        lines.append("Other sessions signed in at observation start: "
                     + ("count not recorded" if item.get("others") is None else str(item["others"])) + " (" + item["at"] + ")")
    added = s.get("sessions_added") or []
    if added:
        lines.append("Sessions added to Telegram's session list during observation: "
                     + str(sum(item["added"] for item in added)) + " in " + str(len(added)) + " record(s), first "
                     + added[0]["at"])
    if s.get("security_events"):
        lines.append("Telegram security notices (777000): " + ", ".join(
            name + " " + str(count) for name, count in sorted(s["security_events"].items())))
    for item in s.get("other_sessions_ended") or []:
        lines.append("All other sessions ended from this workspace at " + item["at"]
                     + (" (" + str(item["ended"]) + " signed in before)" if isinstance(item.get("ended"), int) else ""))
    for item in s.get("password_changes") or []:
        lines.append("Two-step password " + str(item.get("operation") or "set or changed") + " from this workspace at " + item["at"])
    for item in s.get("only_session") or []:
        lines.append("Only session of the account from " + item["from"]
                     + (" until another session appeared at " + item["until"] if item.get("until") else "")
                     + ": other sessions ended" + (" (" + str(item["ended"]) + ")" if isinstance(item.get("ended"), int) else "")
                     + ", two-step password " + ("set from this workspace" if item.get("two_step") == "set_now"
                                                  else "already on"))
    if s.get("only_session_automatic"):
        item = s["only_session_automatic"]
        lines.append("Automatic only-session " + ("on" if item["enabled"] else "off") + " from " + item["at"]
                     + (", postponed by Telegram " + str(s["only_session_postponed"]) + " time(s)"
                        if s.get("only_session_postponed") else ""))
    if s.get("probes"):
        lines.append("Witness probes: " + ", ".join(name + " " + str(count) for name, count in s["probes"].items())
                     + ("; slowest live answer " + str(round(s["probe_delay_max"], 1)) + " s"
                        if s.get("probe_delay_max") is not None else ""))
    if s.get("probe_answers"):
        lines.append("Probes of another workspace answered as its witness: "
                     + ", ".join(name + " " + str(count) for name, count in s["probe_answers"].items()))
    if s.get("phone_calls"):
        lines.append("Phone call updates delivered to this session: " + str(s["phone_calls"]))
    return lines


def source_counts(coverage):
    sources = dict(coverage.get("record_sources") or {})
    groups = [(label, [(name, sources.pop(name)) for name in names if name in sources]) for label, names in SOURCE_GROUPS]
    captures, unlabelled = sources.pop("recorder_capture", 0), sources.pop("unlabelled", 0)
    sealed = sources.pop("inside_sealed_run", 0)
    return [(label, found) for label, found in groups if found], sorted(sources.items()), unlabelled, captures, sealed


def source_lines(coverage):
    groups, other, unlabelled, captures, sealed = source_counts(coverage)
    parts = [label + " " + str(sum(count for _, count in found)) + " ("
             + ", ".join(name + " " + str(count) for name, count in found) + ")" for label, found in groups]
    parts += ["source " + name + " " + str(count) for name, count in other]
    if unlabelled:
        parts.append("no source label " + str(unlabelled))
    lines = ["Message records by source: " + "; ".join(parts)] if parts else []
    if sealed:
        lines.append("Message records between sealed.started and sealed.finished (sealed run): " + str(sealed))
    if captures:
        lines.append("Recorder captures linked into this journal: " + str(captures))
    return lines


def coverage_lines(coverage):
    def span(seconds):
        hours, rest = divmod(int(seconds), 3600)
        return (str(hours) + " h " if hours else "") + str(rest // 60) + " min"
    lines = ["Continuously observed from " + p["from"] + " to " + p["to"] + " (" + span(p["seconds"]) + ")"
             + (", observing at the last capture confirmation" if p.get("still_observing") else "")
             for p in coverage["continuous"]]
    lines += ["Gap from " + g["from"] + " to " + g["to"] + ": " + str(g["reason"]) for g in coverage["gaps"]]
    lines += session_lines(coverage)
    lines += source_lines(coverage)
    for chat in coverage["unobserved_ids"]:
        if chat["not_observed"]:
            lines.append("Chat " + (chat["title"] or str(chat["chat_id"])) + ": IDs " + str(chat["observed_from"])
                         + "-" + str(chat["observed_to"]) + ", " + str(chat["not_observed"])
                         + " ID(s) not observed in " + str(chat["ranges_total"]) + " range(s)")
    gaps, extra = coverage.get("gap_summary") or {}, []
    account = gaps.get("account") if gaps.get("status") == "on" else None
    if account and account.get("status") == "applicable":
        extra.append("Account-wide sequence (private chats, bots, ordinary groups): IDs " + str(account["observed_from"])
                     + "-" + str(account["observed_to"]) + ", " + str(account["missing"]) + " ID(s) not observed in "
                     + str(account["gap_ranges"]) + " range(s)")
    elif account:
        extra.append("Account-wide sequence not measured: " + str(account.get("reason")))
    return (lines or ["No observation period recorded."]) + extra


def drand_time(number):
    return datetime.fromtimestamp(DRAND_GENESIS + (number - 1) * DRAND_PERIOD, timezone.utc).isoformat(
        timespec="milliseconds")


def drand_beacon(value):
    if not isinstance(value, dict) or type(value.get("round")) is not int or value["round"] < 1:
        raise ValueError("drand value without a round number")
    signature, randomness = value.get("signature"), value.get("randomness")
    if not (isinstance(signature, str) and re.fullmatch(r"[0-9a-f]{96}", signature) and isinstance(randomness, str)
            and hashlib.sha256(bytes.fromhex(signature)).hexdigest() == randomness):
        raise ValueError("drand randomness is not the hash of its signature")
    return {"round": value["round"], "randomness": randomness, "signature": signature}


class OutsideRecords:
    def __init__(self):
        self.rounds, self.checks, self.changes = [], [], []
        self.devices, self.largest_gap, self.clock_behind = {}, 0, 0
        self.windows, self.names, self.gaps, self.queries, self.truncated = [], {}, [], 0, 0

    def add(self, event):
        at, kind, payload = event["observed_at"], event["kind"], event["payload"]
        if kind == "beacon.drand":
            beacon = drand_beacon(payload)
            if payload.get("chain") != DRAND_CHAIN or payload.get("round_time") != drand_time(beacon["round"]):
                raise ValueError("drand value from another chain or with a wrong round time at record "
                                 + str(event["seq"]))
            self.clock_behind = max(self.clock_behind,
                                    (parse_time(payload["round_time"]) - parse_time(at)).total_seconds())
            if self.rounds:
                self.largest_gap = max(self.largest_gap,
                                       (parse_time(at) - parse_time(self.rounds[-1]["at"])).total_seconds())
            self.rounds.append({"seq": event["seq"], "at": at, **beacon, "round_time": payload["round_time"]})
        elif kind == "cloudflare.gateway_dns":
            queries, fields = payload.get("queries"), payload.get("fields")
            try:
                window = parse_time(payload["from"]) < parse_time(payload["until"])
            except (KeyError, AttributeError, TypeError, ValueError):
                window = False
            if not (window and isinstance(queries, list) and fields == list(GATEWAY_FIELDS)
                    and payload.get("count") == len(queries)
                    and all(isinstance(q, list) and len(q) == len(GATEWAY_FIELDS) for q in queries)):
                raise ValueError("Cloudflare Gateway log record " + str(event["seq"]) + " is malformed")
            previous = self.windows[-1] if self.windows else None
            if previous and previous["location_id"] == payload.get("location_id") \
                    and previous["address"] == payload.get("address") and payload["from"] != previous["until"]:
                self.gaps.append({"from": previous["until"], "until": payload["from"], "at": at})
            self.windows.append({"seq": event["seq"], "at": at, "from": payload["from"], "until": payload["until"],
                                 "count": len(queries), "location_id": payload.get("location_id"),
                                 "address": payload.get("address")})
            self.queries += len(queries)
            self.truncated += payload.get("truncated") is True
            for query in queries:
                self.names[str(query[1])] = self.names.get(str(query[1]), 0) + 1
        elif kind == "account.devices" and type(payload.get("count")) is int:
            self.checks.append(at)
            listed = payload.get("devices")
            if isinstance(listed, list):
                current = {str(d.get("hash")): d for d in listed if isinstance(d, dict)}
                self.changes.append({"at": at, "count": payload["count"], "devices": list(current.values()),
                                     "added": [current.get(h, {"hash": h}) for h in payload.get("added") or []],
                                     "removed": [self.devices.get(h, {"hash": h}) for h in payload.get("removed") or []]})
                self.devices = current

    def result(self):
        return {"drand": {"rounds": len(self.rounds), "chain": DRAND_CHAIN,
                          "first": self.rounds[0] if self.rounds else None,
                          "last": self.rounds[-1] if self.rounds else None,
                          "largest_gap_seconds": round(self.largest_gap),
                          "clock_behind_seconds": round(self.clock_behind, 1) if self.clock_behind > 0 else 0,
                          "meaning": "Offline checks confirm the recorded beacon's self-consistency. --check-drand "
                                     "compares selected rounds with HTTPS relays; authenticated rounds give a lower "
                                     "time bound for subsequent records."},
                "devices": {"checks": len(self.checks), "first_check": self.checks[0] if self.checks else None,
                            "last_check": self.checks[-1] if self.checks else None, "changes": self.changes[:200],
                            "changes_total": len(self.changes),
                            "meaning": "Telegram's list of sessions of this account (Settings, Devices) as the "
                                       "collector received it; IP addresses are not recorded."},
                "gateway": {"windows": len(self.windows), "queries": self.queries,
                            "first": self.windows[0]["from"] if self.windows else None,
                            "last": self.windows[-1]["until"] if self.windows else None,
                            "locations": sorted({w["location_id"] for w in self.windows if w["location_id"]}),
                            "addresses": sorted({w["address"] for w in self.windows if w["address"]}),
                            "names": sorted(self.names.items(), key=lambda item: (-item[1], item[0]))[:100],
                            "names_total": len(self.names), "gaps": self.gaps[:50], "gaps_total": len(self.gaps),
                            "truncated_windows": self.truncated,
                            "meaning": "DNS queries as Cloudflare Gateway logged them and its API returned them to "
                                       "the collector, window after window; a gap is time no copy covers. Cloudflare "
                                       "keeps its own copy 24 hours on the free plan."}}


def device_name(device, active=False):
    if set(device) == {"hash"}:
        return "session " + str(device["hash"])
    parts = [" ".join(str(device.get(k) or "") for k in ("device_model", "platform", "system_version")).strip(),
             " ".join(str(device.get(k) or "") for k in ("app_name", "app_version")).strip(),
             str(device.get("country") or "")]
    if device.get("current"):
        parts.append("this collector")
    elif active and device.get("active_at"):
        parts.append("active " + str(device["active_at"]))
    return ", ".join(p for p in parts if p)


def outside_lines(outside):
    lines, drand, devices = [], outside["drand"], outside["devices"]
    if drand["rounds"]:
        lines.append(str(drand["rounds"]) + " drand round(s) recorded from " + drand["first"]["at"] + " to "
                     + drand["last"]["at"] + "; the longest stretch without a new round is "
                     + str(round(drand["largest_gap_seconds"] / 60)) + " min")
        checked = drand.get("checked")
        if not checked:
            lines.append("drand beacons checked offline: each randomness is the SHA-256 of its signature. Run with "
                         "--check-drand to compare rounds with HTTPS relays and get a lower time bound.")
        elif checked["relays"]:
            lines.append("Confirmed by drand relays: " + str(checked["confirmed"]) + " of " + str(checked["asked"])
                         + " round(s) asked (" + ", ".join(checked["relays"]) + ")"
                         + ("" if len(checked["relays"]) > 1 else "; only one operator answered"))
        else:
            lines.append("Rounds could not be compared: no drand relay answered")
        if drand["clock_behind_seconds"] > 1:
            lines.append("Recorded observation times trail recorded drand round times by up to "
                         + str(drand["clock_behind_seconds"])
                         + " s.")
    gateway = outside.get("gateway") or {}
    if gateway.get("windows"):
        lines.append("Cloudflare Gateway DNS log copied in " + str(gateway["windows"]) + " window(s) from "
                     + gateway["first"] + " to " + gateway["last"] + ": " + str(gateway["queries"]) + " quer(ies), "
                     + str(gateway["names_total"]) + " name(s)"
                     + (" from " + ", ".join(gateway["addresses"]) if gateway["addresses"] else ""))
        if gateway["names"]:
            lines.append("Names looked up most: " + ", ".join(name + " (" + str(count) + ")"
                                                               for name, count in gateway["names"][:15]))
        lines += ["Gateway log not copied from " + gap["from"] + " to " + gap["until"] for gap in gateway["gaps"][:10]]
        if gateway.get("truncated_windows"):
            lines.append(str(gateway["truncated_windows"]) + " window(s) held more queries in one second than one "
                         "page of Cloudflare's log: the rest of that second is not in the copy")
    if devices["checks"]:
        lines.append("Telegram device list recorded " + str(devices["checks"]) + " time(s) from "
                     + devices["first_check"] + " to " + devices["last_check"] + "; it changed "
                     + str(max(0, devices["changes_total"] - 1)) + " time(s) after the first list")
        for change in devices["changes"][:20]:
            lines += [change["at"] + ": new session: " + device_name(d) for d in change["added"]]
            lines += [change["at"] + ": session ended: " + device_name(d) for d in change["removed"]]
            if not (change["added"] or change["removed"]):
                lines.append(change["at"] + ": " + str(change["count"]) + " session(s): "
                             + "; ".join(device_name(d, True) for d in change["devices"]))
    return lines


def confirm_drand(rounds, relays=DRAND_RELAYS, limit=DRAND_CHECK_LIMIT, fetch=None):
    import random
    chosen = rounds if len(rounds) <= limit else \
        [rounds[0], rounds[-1]] + random.SystemRandom().sample(rounds[1:-1], limit - 2)
    fetch = fetch or drand_fetcher()
    used = []
    for group in (relays[:1], relays[1:]):
        for relay in group:
            try:
                answers = [(item, drand_beacon(fetch(relay, item["round"]))) for item in chosen]
            except (OSError, ValueError):
                continue
            for item, answer in answers:
                if answer["round"] != item["round"] or answer["randomness"] != item["randomness"]:
                    raise ValueError("drand round " + str(item["round"]) + " at record " + str(item["seq"])
                                     + " differs from " + relay + ": the recorded value is not drand's")
            used.append(relay)
            break
    return {"asked": len(chosen), "confirmed": len(chosen) if used else 0, "relays": used,
            "unavailable": bool(chosen) and not used}


def drand_fetcher():
    import http.client
    from urllib.parse import urlsplit
    connections = {}

    def fetch(relay, number):
        host = urlsplit(relay).hostname
        for attempt in (0, 1):
            connection = connections.get(host) or http.client.HTTPSConnection(host, timeout=20)
            connections[host] = connection
            try:
                connection.request("GET", "/" + DRAND_CHAIN + "/public/" + str(number),
                                   headers={"Accept": "application/json", "User-Agent": "TgWitness verify"})
                reply = connection.getresponse()
                body = reply.read(4096)
                if reply.status != 200:
                    raise OSError(relay + " answered HTTP " + str(reply.status))
                return json.loads(body)
            except (http.client.HTTPException, ConnectionError):
                connection.close()
                connections.pop(host, None)
                if attempt:
                    raise OSError(relay + " closed the connection")
    return fetch


def verify_events(events, public_key):
    key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key, validate=True))
    previous, count = "0" * 64, 0
    previous_time, previous_at = None, None
    chronology = {"regressions": 0, "unparseable": 0, "samples": []}
    for count, event in enumerate(events, 1):
        if set(event) != set(FIELDS) | {"hash", "signature"}:
            raise ValueError("Unexpected or missing fields at event " + str(count))
        if event["seq"] != count or event["previous_hash"] != previous:
            raise ValueError("Broken sequence or hash chain at event " + str(count))
        calculated = hashlib.sha256(canonical({k: event[k] for k in FIELDS})).hexdigest()
        if event["hash"] != calculated:
            raise ValueError("Changed content at event " + str(count))
        key.verify(base64.b64decode(event["signature"], validate=True), bytes.fromhex(calculated))
        anomaly = None
        try:
            observed = parse_time(event["observed_at"])
            if observed.utcoffset() is None:
                raise ValueError("Observation time has no UTC offset")
        except (AttributeError, TypeError, ValueError, OverflowError):
            observed = None
            chronology["unparseable"] += 1
            anomaly = {"seq": count, "observed_at": event["observed_at"], "reason": "unparseable"}
        if observed is not None and previous_time is not None and observed < previous_time:
            chronology["regressions"] += 1
            anomaly = {"seq": count, "observed_at": event["observed_at"], "previous_at": previous_at,
                       "backwards_seconds": (previous_time - observed).total_seconds(), "reason": "regression"}
        if anomaly is not None and len(chronology["samples"]) < 100:
            chronology["samples"].append(anomaly)
        if observed is not None:
            previous_time, previous_at = observed, event["observed_at"]
        if event["kind"] == "media.hashed":
            payload = event["payload"]
            validate_server_hashes(payload.get("server_hashes"))
            if (payload["server_hashes"]["status"] != "complete" or payload.get("downloaded_bytes") != 0
                    or payload.get("media_sha256") is not None):
                raise ValueError("A hash-only record incorrectly claims downloaded file content")
        previous = calculated
    result = {"events": count, "head_hash": previous, "fingerprint": fingerprint(public_key)}
    if chronology["regressions"] or chronology["unparseable"]:
        chronology["meaning"] = ("Observation times come from the collector's clock; the hash chain fixes the order of "
                                 "the records, and timestamps, drand rounds and witness records fix them in time. "
                                 "These entries do not affect the signatures.")
        result["chronology"] = chronology
    return result


def media_reference(event):
    if event["kind"] not in ("media.saved", "actor.avatar_saved", "secret_chat.file"):
        return None
    payload = event["payload"]
    digest, size = payload.get("media_sha256"), payload.get("size")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("Invalid media reference in the signed journal")
    if size is not None and (type(size) is not int or size < 0):
        raise ValueError("Invalid media size in the signed journal")
    return digest, size


def verify_checkpoint(checkpoint, public_key, event_count, hash_at, check_drand=False):
    statement = checkpoint["statement"]
    if not is_format(statement["format"], "checkpoint-v1") or statement["public_key"] != public_key:
        raise ValueError("Checkpoint format or signing key mismatch")
    if type(statement["event_count"]) is not int or statement["event_count"] < 0:
        raise ValueError("Invalid checkpoint event count")
    Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key, validate=True)).verify(
        base64.b64decode(checkpoint["signature"], validate=True), canonical(statement))
    if statement["event_count"] > event_count:
        raise ValueError("Journal is shorter than the retained checkpoint")
    if hash_at(statement["event_count"]) != statement["head_hash"]:
        raise ValueError("Journal disagrees with the retained checkpoint")
    anchor = statement.get("drand_anchor")
    if check_drand and anchor and isinstance(anchor.get("round"), int) and isinstance(anchor.get("randomness"), str):
        try:
            confirmed = confirm_drand([{"round": anchor["round"], "randomness": anchor["randomness"],
                                        "seq": statement["event_count"]}])
        except ValueError as exc:
            raise ValueError("Checkpoint drand anchor: " + str(exc)) from exc
        if confirmed["confirmed"] == 0:
            raise ValueError("Checkpoint drand anchor round " + str(anchor["round"])
                             + " could not be confirmed against any drand relay")
    return anchor if anchor else None


def read_sealed(stream):
    digest, window, start = hashlib.sha256(), b"", None
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        start = chunk[:16] if start is None else start
        window += chunk
        if len(window) > 2 * SEAL_WINDOW:
            digest.update(window[:-SEAL_WINDOW])
            window = window[-SEAL_WINDOW:]
    at = window.rfind(SEAL_OPEN)
    if at < 0:
        return None
    if not start.lower().startswith(b"<!doctype html"):
        raise ValueError("This seal belongs to an HTML report, but the file is not one")
    digest.update(window[:at])
    block = window[at + len(SEAL_OPEN):]
    if not block.endswith(SEAL_CLOSE):
        raise ValueError("The report seal is not at the end of the file")
    raw = block[:-len(SEAL_CLOSE)]
    if b"<" in raw:
        raise ValueError("The report seal contains markup")
    return digest.hexdigest(), strict_json(raw)


def check_seal(sealed, public_key=None, expected_fingerprint=None):
    content, seal = sealed
    statement = authenticate_statement(seal)
    if not is_format(statement.get("format"), "report-seal-v1"):
        raise VerifierTooOld("Unsupported report seal")
    key = statement["public_key"]
    if public_key is not None and key != public_key:
        raise ValueError("The report was sealed with a different key than the archive")
    fp = fingerprint(key)
    if expected_fingerprint and fp != expected_fingerprint:
        raise ValueError("Public key differs from the independently trusted fingerprint")
    Ed25519PublicKey.from_public_bytes(base64.b64decode(key, validate=True)).verify(
        base64.b64decode(seal["signature"], validate=True), canonical(statement))
    if statement.get("content_sha256") != content:
        raise ValueError("The report was changed after it was sealed")
    return {"report_id": statement.get("report_id"), "created_at": statement.get("created_at"),
            "language": statement.get("language"), "case": statement.get("case") or {},
            "subject": statement.get("subject") or {}, "producer": statement.get("producer"), "fingerprint": fp}


def archive_seal(archive, name, public_key):
    with archive.open(name) as stream:
        sealed = read_sealed(stream)
    return check_seal(sealed, public_key) if sealed else None


REPORT_JSON = "report-json-v1"
PDF_SEAL = "2.25.240684792623320047764573196045913242332"
SIGNING_TIME = "1.2.840.113549.1.9.5"


def read_pdf_seal(data):
    ranges = re.findall(rb"/ByteRange\s*\[\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\]", data)
    if len(ranges) != 1:
        raise ValueError("Not a PDF signed by TgWitness: exactly one signature is expected")
    a, b, c, d = map(int, ranges[0])
    if a != 0 or not 0 < b < c or c + d != len(data) or data[b:b + 1] != b"<" or data[c - 1:c] != b">":
        raise ValueError("The PDF signature does not cover the whole file")
    raw = bytes.fromhex(data[b + 1:c - 1].decode("ascii"))
    content = hashlib.sha256(data[:b] + data[c:]).digest()
    _, start, end = der(raw, 0)
    info = children(raw, start, end)
    if oid(raw, info[0][2], info[0][3]) != SIGNED_DATA:
        raise ValueError("The PDF signature is not CMS signed data")
    _, start, end = der(raw, info[1][2])
    signed = children(raw, start, end)
    certificates = next(item for item in signed if item[0] == 0xA0)
    tag, offset, _, value_end = children(raw, certificates[2], certificates[3])[0]
    der_certificate = raw[offset:value_end]
    certificate = x509.load_der_x509_certificate(der_certificate)
    signer = children(raw, signed[-1][2], signed[-1][3])[0]
    parts = children(raw, signer[2], signer[3])
    attributes = next(item for item in parts if item[0] == 0xA0)
    unsigned = next((item for item in parts if item[0] == 0xA1), None)
    signature = next(item for item in parts if item[0] == 0x04)

    def values(item):
        found = {}
        for _, _, s, e in children(raw, item[2], item[3]):
            kind = children(raw, s, e)
            found[oid(raw, kind[0][2], kind[0][3])] = children(raw, kind[1][2], kind[1][3])[0]
        return found
    signed_attributes = values(attributes)
    digest = signed_attributes.get(MESSAGE_DIGEST)
    if digest is None or raw[digest[2]:digest[3]] != content:
        raise ValueError("The PDF was changed after it was signed")
    certificate.public_key().verify(raw[signature[2]:signature[3]], b"\x31" + raw[attributes[1] + 1:attributes[3]],
                                    ec.ECDSA(hashes.SHA256()))
    seal = values(unsigned).get(PDF_SEAL) if unsigned else None
    if seal is None:
        raise ValueError("The PDF signature carries no TgWitness seal")
    seal = strict_json(raw[seal[2]:seal[3]].decode("utf-8"))
    certificate_sha256 = hashlib.sha256(der_certificate).hexdigest()
    if seal["statement"].get("document_certificate_sha256") != certificate_sha256 \
            or seal["statement"].get("content") != "pdf-byte-range":
        raise ValueError("The seal does not vouch for the certificate that signed this PDF")
    when = signed_attributes.get(SIGNING_TIME)
    names = certificate.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
    return content.hex(), seal, {"certificate": names[0].value if names else certificate.subject.rfc4514_string(),
                                 "certificate_subject": certificate.subject.rfc4514_string(),
                                 "certificate_sha256": certificate_sha256,
                                 "signing_time": raw[when[2]:when[3]].decode("ascii") if when else None}


def read_json_seal(data):
    if not isinstance(data, dict) or set(data) != {"format", "report", "seal"} \
            or not is_format(data.get("format"), REPORT_JSON):
        raise ValueError("Not a TgWitness JSON report")
    return hashlib.sha256(canonical(data["report"])).hexdigest(), data["seal"]


def report_companions(archive, manifest, public, describes):
    files, report = manifest["files"], manifest.get("report") or {}
    checked = {"json": None, "parts": 0, "pdf": None}
    if "report.json" in files:
        seal = check_seal(read_json_seal(strict_json(read_member(archive, "report.json", MAX_JSON_BYTES))), public)
        if not describes(seal["subject"]):
            raise ValueError("report.json describes a different export")
        checked["json"] = seal
    for name in ("report.pdf", "chat.pdf"):
        if name in files:
            content, seal, signature = read_pdf_seal(read_member(archive, name, MAX_JSON_BYTES))
            seal = check_seal((content, seal), public)
            if not describes(seal["subject"]):
                raise ValueError(name + " describes a different export")
            checked["pdf"] = {**seal, "file": name, "pdf_signature": signature}
    parts = report.get("parts") or []
    for number, part in enumerate(parts, 1):
        name = part.get("file") if isinstance(part, dict) else None
        if name not in files:
            raise ValueError("A report part named in the manifest is missing: " + str(name))
        seal = archive_seal(archive, name, public)
        subject = (seal or {}).get("subject") or {}
        if not seal or not describes(subject) or subject.get("part") != number or subject.get("parts") != len(parts):
            raise ValueError("Report part " + name + " does not belong to this export")
        checked["parts"] += 1
    return checked


def check_sums(archive, manifest):
    if "SHA256SUMS" not in manifest["files"]:
        return None
    listed = {}
    for line in read_member(archive, "SHA256SUMS", MAX_MANIFEST_BYTES).decode("utf-8").splitlines():
        digest, _, name = line.partition("  ")
        listed[name] = digest
    if listed != {name: digest for name, digest in manifest["files"].items() if name != "SHA256SUMS"}:
        raise ValueError("SHA256SUMS disagrees with the signed manifest")
    return len(listed)


def verify_report(path, expected_fingerprint=None, evidence=None):
    signature = None
    if Path(path).suffix.lower() == ".json":
        sealed = read_json_seal(read_json_file(path))
    elif Path(path).suffix.lower() == ".pdf":
        if Path(path).stat().st_size > MAX_JSON_BYTES:
            raise ValueError(Path(path).name + " exceeds the verifier's size limit")
        content, seal, signature = read_pdf_seal(Path(path).read_bytes())
        sealed = content, seal
    else:
        with open(path, "rb") as stream:
            sealed = read_sealed(stream)
    if not sealed:
        raise ValueError("This report has no seal: it was made before seals or not by TgWitness")
    seal = check_seal(sealed, None, expected_fingerprint)
    subject = seal["subject"]
    result = {"format": "tgwitness-report-seal-v1", "fingerprint": seal["fingerprint"], "report_seal": seal,
              "producer": seal["producer"], "key_pinned": bool(expected_fingerprint), "evidence_checked": False,
              **({"pdf_signature": signature} if signature else {})}
    if evidence:
        if is_format(bundle_format(evidence), "chat-export-v1"):
            checked = verify_chat_export(evidence, expected_fingerprint)
            matches = checked["chat_json_sha256"] == subject.get("chat_json_sha256")
        elif is_format(bundle_format(evidence), "handover-v1"):
            checked = verify_handover(evidence, expected_fingerprint)
            with open_archive(evidence) as archive:
                matches = read_manifest(archive)["files"].get("records.jsonl") == subject.get("records_sha256") \
                    and checked["head_hash"] == subject.get("head_hash")
        else:
            checked = verify_bundle(evidence, expected_fingerprint)
            count = subject.get("event_count")
            matches = type(count) is int and 0 <= count <= checked["events"] \
                and ("0" * 64 if count == 0 else bundle_hashes(evidence, [count]).get(count)) == subject.get("head_hash")
        if checked["fingerprint"] != seal["fingerprint"] or not matches:
            raise ValueError("The report describes a different archive")
        result["evidence_checked"] = True
    return result


def verify_selection(path, expected_fingerprint=None, evidence=None):
    data = read_json_file(path)
    if isinstance(data.get("statement"), dict) and "signature" in data:
        return verify_board_selection(data, expected_fingerprint, evidence)
    if not isinstance(data, dict) or data.get("format") != "tgwitness-selection-v1":
        raise ValueError("Unsupported selection format")
    if not evidence:
        raise ValueError("A viewer selection requires --evidence with its signed source archive")
    source, items = data.get("source"), data.get("items")
    if not isinstance(source, dict) or not isinstance(items, list) or not items:
        raise ValueError("A selection must contain a source and at least one item")
    kind = source.get("kind")
    if kind == "journal":
        archive_format = bundle_format(evidence)
        kind = "handover" if is_format(archive_format, "handover-v1") else "evidence" if is_format(archive_format, "evidence-v1") else None
    verifier = {"chat": verify_chat_export, "evidence": verify_bundle, "handover": verify_handover}.get(kind)
    if verifier is None:
        raise ValueError("Unsupported selection source kind")
    checked = verifier(evidence, expected_fingerprint)
    seal = checked.get("report_seal") or {}
    if source.get("fingerprint") != checked["fingerprint"] or source.get("report_id") != seal.get("report_id"):
        raise ValueError("Selection describes a different report or signing key")
    subject = seal.get("subject") or {}
    boundary = ("chat_id", "chat_json_sha256") if kind == "chat" else ("head_hash",) if kind == "handover" else ("head_hash", "event_count")
    if canonical({k: source.get(k) for k in boundary}) != canonical({k: subject.get(k) for k in boundary}):
        raise ValueError("Selection describes a different archive boundary")
    if kind == "handover" and (type(source.get("event_count")) is not int or source["event_count"] != checked["journal_events"]):
        raise ValueError("Selection describes a different archive boundary")
    identity = "id" if kind == "chat" else "seq"
    wanted = {}
    for item in items:
        if not isinstance(item, dict) or type(item.get(identity)) is not int or item[identity] < 1:
            raise ValueError("Selection item has an invalid identifier")
        if item[identity] in wanted:
            raise ValueError("Selection contains duplicate identifiers")
        wanted[item[identity]] = item
    member = "chat.json" if kind == "chat" else "records.jsonl" if kind == "handover" else "events.jsonl"
    digest_key = "chat_json_sha256" if kind == "chat" else "records_sha256" if kind == "handover" else "events_sha256"
    matched = set()
    with open_archive(evidence) as archive:
        if member_digest(archive, member) != subject.get(digest_key):
            raise ValueError("Source data changed after archive verification")

        def records():
            with archive.open(member) as stream:
                for line in bounded_lines(stream):
                    yield json.loads(line)

        for record in chat_messages(archive) if kind == "chat" else records():
            number = record.get(identity)
            if number not in wanted:
                continue
            if number in matched:
                raise ValueError("Source has duplicate identifiers for a selected item")
            expected = record
            if kind != "chat":
                payload = record.get("payload") if isinstance(record.get("payload"), dict) else {}
                sender = payload.get("sender_observation") if isinstance(payload.get("sender_observation"), dict) else {}
                text = payload.get("text")
                expected = {"seq": number, "hash": record.get("hash"), "kind": record.get("kind"),
                            "observed_at": record.get("observed_at"), "chat_id": record.get("chat_id"),
                            "message_id": record.get("message_id"),
                            "sender_id": payload.get("sender_id", sender.get("id")),
                            "text": text if isinstance(text, str) and text else None}
            if canonical(wanted[number]) != canonical(expected):
                raise ValueError("Selection item differs from signed source: " + str(number))
            matched.add(number)
    if matched != set(wanted):
        raise ValueError("Selection contains items absent from its source archive")
    return {"format": "tgwitness-selection-v1", "fingerprint": checked["fingerprint"],
            "key_pinned": bool(expected_fingerprint), "source_kind": kind, "report_id": source["report_id"],
            "items_checked": len(matched), "evidence_checked": True, "selection_signed": False,
            "producer": checked.get("producer"), "case": checked.get("case") or {}}


ANNOTATION_FIELDS = ("seq", "at", "access_id", "access_label", "kind", "payload", "previous_hash")
ANNOTATION_FORMAT = "tgwitness-annotations-v1"
BOARD_KINDS = {"board." + kind for kind in ("bookmark", "highlight", "slice", "collection", "comment", "status", "move", "remove")}


def verify_board_selection(data, expected_fingerprint=None, evidence=None):
    statement = authenticate_statement(data)
    if statement.get("format") != "tgwitness-board-selection-v1":
        raise VerifierTooOld("Unsupported board selection")
    public = statement["public_key"]
    fp = fingerprint(public)
    if expected_fingerprint and fp != expected_fingerprint:
        raise ValueError("Selection key differs from trusted fingerprint")
    Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True)).verify(
        base64.b64decode(data["signature"], validate=True), canonical(statement))
    if not evidence:
        raise ValueError("A board selection requires --evidence with its signed source archive")
    checked = verify_bundle(evidence, expected_fingerprint)
    if checked["fingerprint"] != fp:
        raise ValueError("Selection belongs to a different workspace key")
    items = statement["items"]
    wanted = {item["seq"]: item for item in items}
    if len(wanted) != len(items):
        raise ValueError("Duplicate selection records")
    boundary, matched, at_boundary = statement["journal_head"], set(), "0" * 64
    with open_archive(evidence) as archive, archive.open("events.jsonl") as incoming:
        for line in bounded_lines(incoming):
            event = strict_json(line)
            if event["seq"] == boundary["seq"]:
                at_boundary = event["hash"]
            if event["seq"] in wanted:
                if event["seq"] > boundary["seq"] or event != wanted[event["seq"]]:
                    raise ValueError("Selection item differs from signed source")
                matched.add(event["seq"])
    if matched != set(wanted) or boundary["hash"] != at_boundary or boundary["seq"] > checked["events"]:
        raise ValueError("Selection source boundary or records missing")
    with tempfile.TemporaryDirectory(prefix="tgwitness-selection-") as temporary:
        db = sqlite3.connect(str(Path(temporary) / "query.sqlite3"))
        try:
            db.execute("CREATE TABLE events(seq INTEGER PRIMARY KEY,hash TEXT,observed_at TEXT,chat_id INTEGER,message_id INTEGER,kind TEXT,actor_id INTEGER,payload TEXT)")
            with open_archive(evidence) as archive, archive.open("events.jsonl") as incoming:
                for line in bounded_lines(incoming):
                    event = strict_json(line)
                    if event["seq"] > boundary["seq"]:
                        break
                    db.execute("INSERT INTO events VALUES(?,?,?,?,?,?,?,?)", tuple(event[key] for key in
                        ("seq", "hash", "observed_at", "chat_id", "message_id", "kind", "actor_id")) + (canonical(event["payload"]).decode(),))
            board_prepare(db)
            where, args = board_where(statement["query"], boundary["seq"])
            selected = {row[0] for row in db.execute("SELECT seq FROM events WHERE " + where, args)}
            if selected != set(wanted):
                raise ValueError("Selection does not contain the complete signed slice query")
        finally:
            db.close()
    return {"format": statement["format"], "fingerprint": fp, "key_pinned": bool(expected_fingerprint),
            "items_checked": len(matched), "evidence_checked": True, "selection_signed": True,
            "source_kind": "evidence", "report_id": None, "producer": checked.get("producer"), "case": checked.get("case") or {}}


def annotation_hash(record):
    return hashlib.sha256(canonical({"format": ANNOTATION_FORMAT,
        **{key: record[key] for key in ANNOTATION_FIELDS}})).hexdigest()


def board_replay(records, public_key=None):
    key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key, validate=True)) if public_key else None
    items, history, previous, count, action_ids = {}, [], "0" * 64, 0, set()
    for count, record in enumerate(records, 1):
        if set(record) != set(ANNOTATION_FIELDS) | {"hash", "signature"}:
            raise ValueError("Unexpected annotation fields")
        if type(record["seq"]) is not int or record["seq"] != count or record["previous_hash"] != previous or record["hash"] != annotation_hash(record):
            raise ValueError("Broken annotations chain at " + str(count))
        if (not re.fullmatch(r"admin|[a-f0-9]{16}", record["access_id"]) or
            not isinstance(record["access_label"], str) or not 1 <= len(record["access_label"]) <= 240 or
            datetime.fromisoformat(record["at"]).tzinfo is None):
            raise ValueError("Invalid annotation author or timestamp")
        if key:
            key.verify(base64.b64decode(record["signature"], validate=True), bytes.fromhex(record["hash"]))
        kind, payload = record["kind"], record["payload"]
        if kind not in BOARD_KINDS or not isinstance(payload, dict) or not re.fullmatch(r"[a-f0-9]{32}", payload.get("id", "")):
            raise ValueError("Invalid board annotation")
        previous = record["hash"]
        identifier = payload["id"]
        metadata = {"annotation_seq": count, "annotation_hash": previous, "at": record["at"],
                    "access_id": record["access_id"], "access_label": record["access_label"], "kind": kind}
        if kind in {"board.status", "board.move", "board.remove"}:
            if identifier in action_ids or identifier in items:
                raise ValueError("Duplicate board action identifier")
            action_ids.add(identifier)
            card = items.get(payload.get("card_id"))
            if not card or card.get("removed"):
                raise ValueError("Board action refers to a missing card")
            if kind == "board.status":
                if payload.get("state") not in {"open", "review", "confirmed", "dismissed"}:
                    raise ValueError("Invalid board status")
                card["state"] = payload["state"]
                history.append({**payload, **metadata})
            elif kind == "board.move":
                collection = items.get(payload.get("collection_id"))
                if payload.get("collection_id") and (not collection or collection["kind"] != "board.collection" or collection.get("removed")):
                    raise ValueError("Board move refers to a missing collection")
                card["collection_id"] = payload.get("collection_id")
            else:
                card["removed"] = True
                if card["kind"] == "board.collection":
                    for member in items.values():
                        if member.get("collection_id") == card["id"]:
                            member["collection_id"] = None
            continue
        if identifier in action_ids:
            raise ValueError("Duplicate board action identifier")
        old = items.get(identifier)
        if old:
            if old.get("removed") or payload.get("supersedes") != old["annotation_hash"] or old["kind"] != kind:
                raise ValueError("Invalid board revision")
        elif payload.get("supersedes"):
            raise ValueError("Board revision has no predecessor")
        if kind == "board.comment" and payload.get("parent_id") not in items:
            raise ValueError("Board comment has no parent")
        item = {**payload, **metadata, "state": old.get("state", "open") if old else "open",
                "collection_id": old.get("collection_id") if old else None, "removed": False,
                "created_access_id": old["created_access_id"] if old else record["access_id"],
                "created_access_label": old["created_access_label"] if old else record["access_label"],
                "created_at": old["created_at"] if old else record["at"]}
        items[identifier] = item
        if kind == "board.collection":
            for card_id in payload.get("card_ids", []):
                card = items.get(card_id)
                if not card or card["kind"] not in {"board.bookmark", "board.highlight", "board.slice"} or card.get("removed"):
                    raise ValueError("Collection refers to a missing card")
                card["collection_id"] = identifier
    return {"annotations_head": {"seq": count, "hash": previous}, "items": list(items.values()), "status_history": history}


def board_scope(item, lookup, trail=None):
    trail = set() if trail is None else trail
    while True:
        identifier = item.get("id")
        if identifier in trail:
            raise ValueError("Cyclic board reference")
        trail.add(identifier)
        kind = item["kind"]
        if kind in {"board.bookmark", "board.highlight"}:
            chat = item["target"].get("chat_id")
            return {chat} if chat is not None else None
        if kind == "board.slice":
            query = item["query"]
            if query.get("include_unscoped"):
                return None
            return set(query.get("chat_ids") or [query["chat_id"]])
        if kind == "board.collection":
            return set(item.get("chat_ids", [])) or None
        item = lookup.get(item.get("parent_id") or item.get("card_id"))
        if not item:
            return None


def board_where(query, boundary=None):
    chats = query.get("chat_ids") or [query.get("chat_id")]
    if not chats or any(type(chat) is not int for chat in chats) or len(chats) > 1000:
        raise ValueError("Invalid slice chat scope")
    parts, args = [], list(chats)
    chat_clause = "chat_id IN (" + ",".join("?" * len(chats)) + ")"
    if query.get("include_unscoped"):
        chat_clause = "(" + chat_clause + " OR (chat_id IS NULL AND kind='deletion.unscoped'))"
    parts.append(chat_clause)
    for field, op, name in (("observed_at", ">=", "from"), ("observed_at", "<=", "to")):
        if query.get(name):
            value = query[name]
            if datetime.fromisoformat(value).tzinfo is None:
                raise ValueError("Slice timestamps need a timezone")
            parts.append("julianday(" + field + ") " + op + " julianday(?)")
            args.append(value)
    for name, op in (("from_message_id", ">="), ("to_message_id", "<=")):
        if query.get(name) is not None:
            parts.append("message_id " + op + " ?")
            args.append(query[name])
    kinds = query.get("kinds", "all")
    if kinds != "all":
        if not isinstance(kinds, list) or not 1 <= len(kinds) <= 40:
            raise ValueError("Invalid slice kinds")
        clauses = []
        for kind in kinds:
            if not isinstance(kind, str) or not re.fullmatch(r"[a-z][a-z0-9_]*(?:\.[a-z0-9_*]+)+", kind):
                raise ValueError("Invalid slice kind")
            clauses.append("kind GLOB ?")
            args.append(kind)
        parts.append("(" + " OR ".join(clauses) + ")")
    if actors := query.get("actors"):
        parts.append("actor_id IN (" + ",".join("?" * len(actors)) + ")")
        args.extend(actors)
    if query.get("search"):
        parts.append("instr(board_search(payload),?)>0")
        args.append(board_search(query["search"]))
    if query.get("hide_system"):
        parts.append("kind NOT IN ('collector.heartbeat','host.state') AND NOT (kind='media.skipped' AND COALESCE(json_extract(payload,'$.reason'),'')='media download disabled')")
    if boundary is not None:
        parts.append("seq <= ?")
        args.append(boundary)
    return " AND ".join(parts), args


def board_search(value):
    return unicodedata.normalize("NFC", str(value or "").casefold())


def board_prepare(connection):
    connection.create_function("board_search", 1, board_search, deterministic=True)


def board_slice_summary(connection, query, boundary=None):
    board_prepare(connection)
    where, args = board_where(query, boundary)
    digest, count, first, last = hashlib.sha256(b"["), 0, None, None
    for seq, value in connection.execute("SELECT seq,hash FROM events WHERE " + where + " ORDER BY hash", args):
        digest.update((b"," if count else b"") + canonical(value))
        count += 1
        first, last = min(first or seq, seq), max(last or seq, seq)
    digest.update(b"]")
    counts = dict(connection.execute("SELECT kind,count(*) FROM events WHERE " + where + " GROUP BY kind", args))
    start, end, placed = connection.execute("SELECT min(julianday(observed_at)),max(julianday(observed_at)),count(julianday(observed_at)) FROM events WHERE " + where, args).fetchone()
    bins = [0] * 24
    if start is not None:
        span = max(end-start, 1 / 86400)
        for bucket, total in connection.execute("SELECT min(23,cast((julianday(observed_at)-?)/?*24 AS INTEGER)),count(*) FROM events WHERE " + where + " AND julianday(observed_at) IS NOT NULL GROUP BY 1", (start, span, *args)):
            bins[bucket] = total
    def iso(day):
        return datetime.fromtimestamp((day-2440587.5)*86400, timezone.utc).isoformat(timespec="seconds") if day is not None else None
    return {"record_count": count, "result_hash": digest.hexdigest(), "first_seq": first, "last_seq": last, "counts": counts,
            "timeline": {"from": iso(start), "to": iso(end), "bins": bins, "unplaced": count-placed, "basis": "observed_at UTC"}}


def verify_board(archive, manifest, checkpoint=None):
    files = manifest["files"]
    if not {"annotations.jsonl", "case-board.json"} & set(files):
        if manifest.get("annotations_head") or (checkpoint or {}).get("statement", {}).get("annotations_head"):
            raise ValueError("Missing retained annotations")
        return None
    if not {"annotations.jsonl", "case-board.json"} <= set(files):
        raise ValueError("Incomplete Case Board export")
    public = manifest["public_key"]
    if archive.getinfo("annotations.jsonl").file_size > MAX_JSON_BYTES:
        raise ValueError("Annotations exceed the verifier's 256 MiB replay limit")
    with archive.open("annotations.jsonl") as incoming:
        records = [strict_json(line) for line in bounded_lines(incoming)]
    replay = board_replay(records, public)
    signed = strict_json(read_member(archive, "case-board.json", MAX_JSON_BYTES))
    statement = signed["statement"]
    Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True)).verify(
        base64.b64decode(signed["signature"], validate=True), canonical(statement))
    if statement.get("format") != "tgwitness-case-board-v1" or statement.get("public_key") != public:
        raise ValueError("Case Board format or key mismatch")
    if statement.get("state") != replay or manifest.get("annotations_head") != replay["annotations_head"]:
        raise ValueError("Case Board state differs from annotations")
    if statement.get("journal_head") != {"seq": manifest["event_count"], "hash": manifest["head_hash"]}:
        raise ValueError("Case Board journal boundary mismatch")
    retained_heads = [(checkpoint or {}).get("statement", {}).get("annotations_head")]
    for name in files:
        if name.startswith("anchors/") and name.endswith(".json"):
            retained_heads.append(strict_json(read_member(archive, name)).get("statement", {}).get("annotations_head"))
    for retained in (head for head in retained_heads if head):
        seq = retained.get("seq")
        if type(seq) is not int or seq < 0 or seq > len(records) or retained.get("hash") != (records[seq-1]["hash"] if seq else "0" * 64):
            raise ValueError("Annotations disagree with retained checkpoint")
    dangling, changed, slices = [], [], {}
    with tempfile.TemporaryDirectory(prefix="tgwitness-board-verify-") as temporary:
        db = sqlite3.connect(str(Path(temporary) / "journal.sqlite3"))
        try:
            db.execute("CREATE TABLE events(seq INTEGER PRIMARY KEY,hash TEXT UNIQUE,observed_at TEXT,chat_id INTEGER,message_id INTEGER,kind TEXT,actor_id INTEGER,payload TEXT)")
            with archive.open("events.jsonl") as incoming:
                for line in bounded_lines(incoming):
                    event = strict_json(line)
                    db.execute("INSERT INTO events VALUES(?,?,?,?,?,?,?,?)", tuple(event[key] for key in
                        ("seq", "hash", "observed_at", "chat_id", "message_id", "kind", "actor_id")) + (canonical(event["payload"]).decode(),))
            for record in records:
                payload = record["payload"]
                if target := payload.get("target"):
                    row = db.execute("SELECT seq,chat_id,message_id,kind,payload FROM events WHERE hash=?", (target["event_hash"],)).fetchone()
                    if row is None:
                        dangling.append({"id": payload["id"], "event_hash": target["event_hash"]})
                    else:
                        if any(target.get(k) != row[i] for i, k in enumerate(("seq", "chat_id", "message_id", "kind"))):
                            raise ValueError("Board target metadata differs from journal")
                        if record["kind"] == "board.highlight":
                            selection, text = payload["range"], json.loads(row[4]).get(payload["range"]["field"])
                            if (not isinstance(text, str) or selection.get("version") != target["event_hash"] or
                                type(selection.get("start")) is not int or type(selection.get("length")) is not int or
                                selection["start"] < 0 or selection["length"] < 1 or
                                text[selection["start"]:selection["start"]+selection["length"]] != selection["quote"]):
                                raise ValueError("Highlight differs from the exact saved version")
                if record["kind"] == "board.slice":
                    snapshot = payload["snapshot"]
                    boundary = snapshot["journal_head"]
                    row = db.execute("SELECT hash FROM events WHERE seq=?", (boundary["seq"],)).fetchone()
                    if boundary["hash"] != (row[0] if row else "0" * 64 if boundary["seq"] == 0 else None):
                        raise ValueError("Slice creation boundary differs from journal")
                    original = board_slice_summary(db, payload["query"], boundary["seq"])
                    if any(snapshot.get(k) != original[k] for k in ("record_count", "result_hash", "first_seq", "last_seq")):
                        raise ValueError("Slice bookmark snapshot differs from its original journal prefix")
            for item in replay["items"]:
                if item["kind"] != "board.slice" or item["removed"]:
                    continue
                query, snapshot = item["query"], item["snapshot"]
                where, args = board_where(query)
                hashes = [row[0] for row in db.execute("SELECT hash FROM events WHERE " + where + " ORDER BY hash", args)]
                added = [row[0] for row in db.execute("SELECT seq FROM events WHERE " + where + " AND seq>? ORDER BY seq", (*args, snapshot["journal_head"]["seq"]))]
                current = board_slice_summary(db, query)
                expected = {"id": item["id"], "query": query, "snapshot": snapshot, "current": current,
                            "event_hashes": hashes, "added_seq": added, "removed_seq": []}
                name = "board/slices/" + item["id"] + ".json"
                if name not in files or strict_json(read_member(archive, name, MAX_JSON_BYTES)) != expected:
                    raise ValueError("Exported slice differs from journal: " + item["id"])
                slices[item["id"]] = name
                if added:
                    changed.append({"id": item["id"], "added": len(added), "removed": 0,
                                    "message": "slice changed since bookmark: +" + str(len(added)) + "/−0 records"})
        finally:
            db.close()
    if {name for name in files if name.startswith("board/slices/")} != set(slices.values()):
        raise ValueError("Unexpected board slice files")
    return {"annotations_head": replay["annotations_head"], "dangling": dangling, "slice_changes": changed,
            "collections": [{"id": item["id"], "title": item["title"]} for item in replay["items"]
                            if item["kind"] == "board.collection" and not item["removed"]]}


def verify_board_disclosure(archive, manifest):
    if "case-board.json" not in manifest["files"]:
        return None
    signed = strict_json(read_member(archive, "case-board.json", MAX_JSON_BYTES))
    statement, public = authenticate_statement(signed), manifest["public_key"]
    if statement.get("format") != "tgwitness-case-board-handover-v1" or statement.get("public_key") != public:
        raise ValueError("Invalid handover board format or signing key")
    Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True)).verify(
        base64.b64decode(signed["signature"], validate=True), canonical(statement))
    cards = statement["material"]["cards"]
    wanted = {card["target"]["event_hash"]: card for card in cards if card.get("target")}
    matched = set()
    with archive.open("records.jsonl") as incoming:
        for line in bounded_lines(incoming):
            record = strict_json(line)
            if record["hash"] in wanted:
                for card in cards:
                    if card.get("target", {}).get("event_hash") == record["hash"] and card.get("observation") != record:
                        raise ValueError("Board exposes content outside the handover record")
                matched.add(record["hash"])
    if matched != set(wanted):
        raise ValueError("Board refers to a record not disclosed in the handover")
    if "report.json" in manifest["files"]:
        report = strict_json(read_member(archive, "report.json", MAX_JSON_BYTES))
        if report["report"].get("case_board") != statement["material"]:
            raise ValueError("Readable report and board disclosure differ")
    return {"cards": len(cards), "meaning": "Minimised copy of the team notes, signed by the collector"}


def verify_board_document(path, expected_fingerprint=None, evidence=None):
    signed = read_json_file(path)
    statement = authenticate_statement(signed)
    if statement.get("format") not in ("tgwitness-case-board-v1", "tgwitness-case-board-disclosure-v1", "tgwitness-case-board-handover-v1"):
        raise VerifierTooOld("Unsupported Case Board document")
    public = statement["public_key"]
    fp = fingerprint(public)
    if expected_fingerprint and fp != expected_fingerprint:
        raise ValueError("Case Board key differs from trusted fingerprint")
    Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True)).verify(
        base64.b64decode(signed["signature"], validate=True), canonical(statement))
    if statement["format"] == "tgwitness-case-board-v1" and evidence:
        checked = verify_bundle(evidence, expected_fingerprint)
        if checked["fingerprint"] != fp:
            raise ValueError("Case Board belongs to another workspace key")
        count = statement["state"]["annotations_head"]["seq"]
        with open_archive(evidence) as archive, archive.open("annotations.jsonl") as incoming:
            prefix = []
            for line in bounded_lines(incoming):
                row = strict_json(line)
                if row["seq"] > count:
                    break
                prefix.append(row)
        if board_replay(prefix, public) != statement["state"]:
            raise ValueError("Case Board state differs from its signed annotations prefix")
        boundary = statement["journal_head"]
        source_head = {"seq": 0, "hash": "0" * 64}
        with open_archive(evidence) as archive, archive.open("events.jsonl") as incoming:
            for line in bounded_lines(incoming):
                row = strict_json(line)
                if row["seq"] > boundary["seq"]:
                    break
                source_head = {"seq": row["seq"], "hash": row["hash"]}
        if source_head != boundary:
            raise ValueError("Case Board journal boundary differs from its evidence source")
    elif evidence:
        raise ValueError("Verify a minimized board with its containing handover ZIP")
    return {"format": statement["format"], "fingerprint": fp, "key_pinned": bool(expected_fingerprint),
            "annotations_checked": bool(evidence), "meaning": "Team opinions; the signature authenticates the document as the team signed it"}


def verify_bundle(path, expected_fingerprint=None, checkpoint=None, tsa_ca=None, check_drand=False, max_gib=None,
                  check_bitcoin=False):
    with open_archive(path, max_gib=max_gib) as archive:
        names = archive.namelist()
        manifest = read_manifest(archive)
        if not is_format(manifest["format"], "evidence-v1"):
            raise VerifierTooOld("Unsupported evidence format")
        public = manifest["public_key"]
        fp = fingerprint(public)
        if expected_fingerprint and fp != expected_fingerprint:
            raise ValueError("Public key differs from the independently trusted fingerprint")
        Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True)).verify(
            base64.b64decode(read_member(archive, "manifest.sig"), validate=True), canonical(manifest))
        if set(names) != set(manifest["files"]) | {"manifest.json", "manifest.sig"}:
            raise ValueError("Unexpected or missing bundle members")
        for name, digest in manifest["files"].items():
            if member_digest(archive, name) != digest:
                raise ValueError("File hash mismatch: " + name)
        sums = check_sums(archive, manifest)

        def describes(subject):
            return (subject.get("event_count") == manifest["event_count"]
                    and subject.get("head_hash") == manifest["head_hash"]
                    and subject.get("events_sha256") == manifest["files"].get("events.jsonl"))
        seal = archive_seal(archive, "report.html", public) if "report.html" in manifest["files"] else None
        if seal and not describes(seal["subject"]):
            raise ValueError("The report seal describes a different journal")
        companions = report_companions(archive, manifest, public, describes)
        gap_settings = None
        if "coverage.json" in manifest["files"]:
            saved_coverage = strict_json(read_member(archive, "coverage.json", MAX_JSON_BYTES))
            saved_gaps = saved_coverage.get("gap_summary") if isinstance(saved_coverage, dict) else None
            if isinstance(saved_gaps, dict):
                gap_settings = saved_gaps.get("parameters")
        observed, outside = Coverage(gap_settings), OutsideRecords()
        hash_files, account_exports, starts = set(), [], []

        def measured(lines):
            for line in lines:
                event = strict_json(line)
                if event["kind"] == "process.started":
                    starts.append(event)
                if event["kind"] == "sealed.account_export":
                    item = event["payload"]
                    if (account_exports or item.get("file") != "account-export.zip"
                            or manifest["files"].get(item["file"]) != item.get("sha256")
                            or archive.getinfo(item["file"]).file_size != item.get("bytes")):
                        raise ValueError("Sealed account export differs from its journal binding")
                    account_exports.append(item)
                if event["kind"] == "media.hashed":
                    digest = hashlib.sha256(canonical(event["payload"].get("server_hashes"))).hexdigest()
                    name = "hashes/" + digest + ".json"
                    if manifest["files"].get(name) != digest:
                        raise ValueError("File-hash manifest differs from the signed journal")
                    hash_files.add(name)
                media = media_reference(event)
                if media:
                    digest, size = media
                    name = "media/" + digest
                    if manifest["files"].get(name) != digest:
                        raise ValueError("Preserved media is missing or differs from the signed journal: " + digest)
                    if size is not None and archive.getinfo(name).file_size != size:
                        raise ValueError("Preserved media size differs from the signed journal: " + digest)
                observed.add(event)
                outside.add(event)
                yield event
        with archive.open("events.jsonl") as stream:
            result = verify_events(measured(bounded_lines(stream)), public)
        if {name for name in manifest["files"] if name.startswith("hashes/")} != hash_files:
            raise ValueError("Unreferenced journal file-hash manifest")
        if ("account-export.zip" in manifest["files"]) != bool(account_exports):
            raise ValueError("Unbound sealed account export")
        if account_exports:
            with archive.open("account-export.zip") as incoming:
                account = verify_account_export(incoming, fp, max_gib=max_gib)
            binding = account_exports[0]
            if account["job_id"] != binding["job_id"] or account["complete_within_scope"] != binding["complete_within_scope"]:
                raise ValueError("Account export coverage differs from its journal binding")
            result["account_export"] = account
        if result["events"] != manifest["event_count"] or result["head_hash"] != manifest["head_hash"]:
            raise ValueError("Manifest does not match journal")
        result["coverage"] = observed.result()
        result["outside"] = outside.result()
        if check_drand and outside.rounds:
            result["outside"]["drand"]["checked"] = confirm_drand(outside.rounds)
        result["producer"] = manifest.get("producer")
        result.update(format=manifest["format"], files_checked=len(manifest["files"]), sha256sums=sums,
                      report_seal=seal, report_json=companions["json"], report_parts=companions["parts"],
                      report_pdf=companions["pdf"], case=manifest.get("case") or {})

        def hash_at(seq):
            if seq == 0:
                return "0" * 64
            with archive.open("events.jsonl") as stream:
                for line in bounded_lines(stream):
                    event = strict_json(line)
                    if event["seq"] == seq:
                        return event["hash"]
            return None
        if checkpoint:
            checkpoint_anchor = verify_checkpoint(checkpoint, public, result["events"], hash_at,
                                                  check_drand=check_drand)
            result["checkpoint_event_count"] = checkpoint["statement"]["event_count"]
            if checkpoint_anchor:
                result["checkpoint_drand_anchor"] = {**checkpoint_anchor, "confirmed_by_relays": bool(check_drand)}
        result["anchors"] = verify_anchors(archive, names, public, result["events"], hash_at, tsa_ca, check_bitcoin)
        result["board"] = verify_board(archive, manifest, checkpoint)
        tdx = verify_tdx_starts(starts, public)
        if tdx:
            result["tdx"] = tdx
        result["key_pinned"] = bool(expected_fingerprint)
        result["checkpoint_checked"] = checkpoint is not None
        result["assurance"] = assurance(result)
        return result


def verify_distributed_pages(stream, envelopes, job, task):
    format_name = "tgwitness-distributed-pages-v1"
    if job.get("checkpoint_format") != format_name:
        raise ValueError("Unsupported distributed checkpoint format.")
    low, high = task["low"], task["high"]
    if type(low) is not int or type(high) is not int or not 0 < low <= high:
        raise ValueError("Invalid checkpoint range.")
    workers = {w["profile_id"]: w for w in job["workers"]}
    eligible = {p for s in job["segments"] if s["low"] <= low <= high <= s["high"] for p in s["profiles"]}
    state = {"pages": 0, "count": 0, "cursor": high + 1, "byte_end": 0, "head_sha256": "0" * 64,
             "terminal": False, "profile_id": None, "transport_generation": None}
    plan_hash = hashlib.sha256(canonical(job)).hexdigest()
    for envelope in envelopes:
        value = envelope["statement"]
        profile = value["profile_id"]
        worker = workers.get(profile)
        if (not worker or profile not in eligible or envelope["public_key"] != worker["public_key"]
                or state["profile_id"] not in (None, profile)):
            raise ValueError("Checkpoint observer differs from the signed plan or preceding pages.")
        Ed25519PublicKey.from_public_bytes(base64.b64decode(worker["public_key"], validate=True)).verify(
            base64.b64decode(envelope["signature"], validate=True), canonical(value))
        if (value.get("format") != format_name or value.get("plan_sha256") != plan_hash
                or value.get("job_id") != job["id"] or value.get("chat_id") != job["chat_id"]
                or value.get("account_id") != worker["account_id"] or value.get("low") != low or value.get("high") != high):
            raise ValueError("Checkpoint scope differs from its signed plan.")
        fields = ("seq", "cursor_before", "cursor_after", "byte_start", "byte_end", "count")
        if any(type(value.get(k)) is not int for k in fields) or type(value.get("terminal")) is not bool:
            raise ValueError("Invalid checkpoint cursor, size or sequence.")
        if (state["terminal"] or value["seq"] != state["pages"] + 1
                or value.get("previous_receipt_sha256") != state["head_sha256"]
                or value["byte_start"] != state["byte_end"] or value["byte_end"] < value["byte_start"]
                or value["cursor_before"] != state["cursor"] or not 0 <= value["count"] <= 100
                or not value["count"] and not value["terminal"]):
            raise ValueError("Broken checkpoint receipt chain.")
        generation = value.get("transport_generation")
        if (value.get("transport") != job.get("transport", "regular")
                or value["transport"] == "takeout" and (type(generation) is not int or generation < 1
                    or state["transport_generation"] is not None and generation < state["transport_generation"])
                or value["transport"] == "regular" and generation is not None):
            raise ValueError("Checkpoint transport differs from the plan or preceding pages.")
        for name in ("captured_from", "captured_until"):
            try:
                if datetime.fromisoformat(value[name]).tzinfo is None:
                    raise ValueError
            except (KeyError, TypeError, ValueError):
                raise ValueError("Invalid checkpoint observation time.") from None
        digest, cursor, count, end = hashlib.sha256(), state["cursor"], 0, state["byte_end"]
        while end < value["byte_end"]:
            line = stream.readline(MAX_RECORD_BYTES + 1)
            end += len(line)
            if not line or len(line) > MAX_RECORD_BYTES or not line.endswith(b"\n") or end > value["byte_end"]:
                raise ValueError("Checkpoint data differs: truncated or oversized.")
            record = strict_json(line)
            mid = record["id"]
            if type(mid) is not int or not low <= mid < cursor:
                raise ValueError("Checkpoint messages are outside their range or repeated.")
            digest.update(line)
            count, cursor = count + 1, mid
        if digest.hexdigest() != value.get("sha256") or count != value["count"] or cursor != value["cursor_after"]:
            raise ValueError("Checkpoint data differs from its signed receipt.")
        state.update(pages=value["seq"], count=state["count"] + count, cursor=cursor,
                     byte_end=end, head_sha256=hashlib.sha256(canonical(envelope)).hexdigest(),
                     terminal=value["terminal"], profile_id=profile, transport_generation=generation)
    return state


def verify_distributed_work(directory, expected_fingerprint=None, max_gib=None):
    directory = Path(directory)
    def checked(path):
        if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
            raise ValueError("Distributed acquisition paths must not be links.")
        return path

    def signed(path, public=None):
        envelope = read_json_file(checked(path))
        if public is not None and envelope["public_key"] != public:
            raise ValueError("Distributed acquisition signing identity changed.")
        Ed25519PublicKey.from_public_bytes(base64.b64decode(envelope["public_key"], validate=True)).verify(
            base64.b64decode(envelope["signature"], validate=True), canonical(envelope["statement"]))
        return envelope

    checked(directory)
    for name in ("chunks", "pages", "receipts"):
        checked(directory / name)
    plan = signed(directory / "job.json")
    job, public = plan["statement"], plan["public_key"]
    fp = fingerprint(public)
    if expected_fingerprint and fp != expected_fingerprint:
        raise ValueError("Public key differs from the independently trusted fingerprint")
    if (job.get("format") != "tgwitness-distributed-job-v1"
            or job.get("checkpoint_format") != "tgwitness-distributed-pages-v1"
            or type(job.get("chunk_size")) is not int or job["chunk_size"] < 1):
        raise ValueError("This directory does not use the supported distributed checkpoint format.")
    workers = {w["profile_id"]: w for w in job["workers"]}
    if workers[job["lead"]]["public_key"] != public:
        raise ValueError("Acquisition plan was not signed by its lead observer.")
    tasks, previous_high = {}, 0
    for segment in job["segments"]:
        low, high = segment["low"], segment["high"]
        if type(low) is not int or type(high) is not int or not previous_high < low <= high:
            raise ValueError("Invalid or overlapping planned acquisition ranges.")
        previous_high = high
        if (high - low) // job["chunk_size"] + 1 + len(tasks) > MAX_MEMBERS:
            raise ValueError("Too many acquisition ranges to verify.")
        for start in range(low, high + 1, job["chunk_size"]):
            tasks[str(start)] = {"low": start, "high": min(high, start + job["chunk_size"] - 1)}
    states, total_bytes, tails = {}, 0, 0
    for folder in checked(directory / "pages").iterdir():
        if folder.name not in tasks or not checked(folder).is_dir():
            raise ValueError("Checkpoint directory is outside the signed plan.")
        paths = sorted(folder.glob("*.json"), key=lambda p: int(p.stem) if p.stem.isdigit() else -1)
        if len(paths) > MAX_MEMBERS or any(p.name != str(i) + ".json" for i, p in enumerate(paths, 1)):
            raise ValueError("Checkpoint receipt sequence is incomplete.")
        data_path = checked(directory / "chunks" / (folder.name + ".jsonl"))
        size = data_path.stat().st_size if data_path.exists() else 0
        total_bytes += size
        if total_bytes > (max_gib or MAX_UNCOMPRESSED_GIB) * 1024**3:
            raise ValueError("Distributed acquisition exceeds the verification size limit.")
        with data_path.open("rb") if data_path.exists() else io.BytesIO() as stream:
            state = verify_distributed_pages(stream, (read_json_file(checked(p)) for p in paths), job, tasks[folder.name])
        states[folder.name] = state
        tails += size - state["byte_end"]
    completed = 0
    for path in (directory / "receipts").glob("*.json"):
        state = states.get(path.stem)
        if not state or not state["terminal"]:
            raise ValueError("A completed chunk has no terminal checkpoint.")
        value = signed(path, workers[state["profile_id"]]["public_key"])["statement"]
        task = tasks[path.stem]
        summary = {"format": job["checkpoint_format"], **{k: state[k] for k in ("pages", "head_sha256", "count", "byte_end")}}
        if (value.get("checkpoint") != summary or value.get("job_id") != job["id"]
                or value.get("profile_id") != state["profile_id"] or value.get("count") != state["count"]
                or value.get("low") != task["low"] or value.get("high") != task["high"]
                or value.get("transport", "regular") != job.get("transport", "regular")
                or value.get("transport_generation") != state["transport_generation"]):
            raise ValueError("Chunk receipt differs from its signed checkpoints.")
        data_path = checked(directory / "chunks" / (path.stem + ".jsonl"))
        with data_path.open("rb") as stream:
            if data_path.stat().st_size != state["byte_end"] or hashlib.file_digest(stream, "sha256").hexdigest() != value["sha256"]:
                raise ValueError("Completed chunk differs from its signed receipt.")
        completed += 1
    captured = sum(s["count"] for s in states.values())
    status = signed(directory / "status.json", public)["statement"]
    if status["id"] != job["id"] or status["captured"] > captured or status["ranges_done"] > completed:
        raise ValueError("Saved acquisition progress is missing.")
    return {"format": job["checkpoint_format"], "fingerprint": fp, "job_id": job["id"],
            "chat_id": job["chat_id"], "captured": captured, "pages": sum(s["pages"] for s in states.values()),
            "ranges_done": completed, "ranges_total": len(tasks), "unsigned_tail_bytes": tails,
            "complete_within_plan": completed == len(tasks),
            "meaning": "Verified local acquisition prefix of the pages Telegram returned, signed per range. "
                       "Unsigned tails are excluded. Keep receipt heads independently to detect removal of a suffix."}


JOURNAL_KINDS = ("message.new", "message.snapshot", "message.recovered", "message.edited", "message.deleted",
                 "message.missing_on_recheck")


def check_journal_changes(archive, manifest, public):
    summary = manifest.get("journal") if isinstance(manifest.get("journal"), dict) else {}
    key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True))
    chat_id = (manifest.get("chat") or {}).get("id")
    count, first, previous, messages = 0, None, 0, set()
    with archive.open("journal-changes.jsonl") as stream:
        for line in bounded_lines(stream):
            event = strict_json(line)
            if not isinstance(event, dict) or set(event) != set(FIELDS) | {"hash", "signature"}:
                raise ValueError("Unexpected record in journal-changes.jsonl")
            if type(event["seq"]) is not int or event["seq"] <= previous:
                raise ValueError("journal-changes.jsonl is not in journal order")
            if event["chat_id"] != chat_id or event["kind"] not in JOURNAL_KINDS or type(event["message_id"]) is not int:
                raise ValueError("journal-changes.jsonl holds a record outside this chat's messages")
            calculated = hashlib.sha256(canonical({k: event[k] for k in FIELDS})).hexdigest()
            if event["hash"] != calculated:
                raise ValueError("Changed journal record " + str(event["seq"]) + " in journal-changes.jsonl")
            if not isinstance(event["signature"], str):
                raise ValueError("Unsigned journal record " + str(event["seq"]) + " in journal-changes.jsonl")
            key.verify(base64.b64decode(event["signature"], validate=True), bytes.fromhex(calculated))
            first = event["seq"] if first is None else first
            previous, count = event["seq"], count + 1
            messages.add(event["message_id"])
    if summary.get("records") != count or summary.get("messages") != len(messages):
        raise ValueError("The signed journal summary disagrees with journal-changes.jsonl")
    return {"records": count, "messages": len(messages), "first_seq": first, "last_seq": previous or None}


def verify_chat_export(path, expected_fingerprint=None, max_gib=None):
    with open_archive(path, max_gib=max_gib) as archive:
        names = archive.namelist()
        manifest = read_manifest(archive)
        if not is_format(manifest["format"], "chat-export-v1"):
            raise VerifierTooOld("Unsupported chat export format")
        public = manifest["public_key"]
        fp = fingerprint(public)
        if expected_fingerprint and fp != expected_fingerprint:
            raise ValueError("Public key differs from the independently trusted fingerprint")
        Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True)).verify(
            base64.b64decode(read_member(archive, "manifest.sig"), validate=True), canonical(manifest))
        if set(names) != set(manifest["files"]) | {"manifest.json", "manifest.sig"}:
            raise ValueError("Unexpected or missing bundle members")
        for name, digest in manifest["files"].items():
            if member_digest(archive, name) != digest:
                raise ValueError("File hash mismatch: " + name)
        parts = verify_parts(archive, manifest) if manifest.get("parts") else None
        attachments = check_attachments(archive, manifest)
        sums = check_sums(archive, manifest)

        def describes(subject):
            return (subject.get("chat_id") == (manifest.get("chat") or {}).get("id")
                    and subject.get("message_count") == manifest.get("message_count")
                    and subject.get("chat_json_sha256") == manifest["files"].get("chat.json"))
        seal = archive_seal(archive, "chat.html", public) if "chat.html" in manifest["files"] else None
        if seal and not describes(seal["subject"]):
            raise ValueError("The report seal describes a different chat export")
        companions = report_companions(archive, manifest, public, describes)
        ids = check_message_ids(archive, manifest) if "message-ids.json" in manifest["files"] else None
        journal = check_journal_changes(archive, manifest, public) if "journal-changes.jsonl" in manifest["files"] else None
        return {"format": manifest["format"], "fingerprint": fp,
                "message_count": manifest.get("message_count"), "producer": manifest.get("producer"),
                "chat": manifest.get("chat"), "key_pinned": bool(expected_fingerprint), "parts": parts,
                "files_checked": len(manifest["files"]), "chat_json_sha256": manifest["files"].get("chat.json"),
                "attachments": attachments, "sha256sums": sums, "report_seal": seal,
                "report_parts": companions["parts"], "report_pdf": companions["pdf"], "message_ids": ids,
                "journal_changes": journal,
                "case": manifest.get("case") or {}}


COMPARE_MEANING = {
    "number": "Both archives record the same chat and account, so messages are matched by their number. "
              "Unchanged means equality of the complete saved message record. A difference shows that the saved "
              "records differ, in content or in observation metadata.",
    "content": "The archives come from different chats or accounts (for example both sides of a private chat), "
               "or their scope identity is missing. Possible matches use time, sender, full text and file hash. "
               "Unchanged counts identical saved records among these pairs; differences describe the paired records.",
}


CLOCK_SLACK = 5


def unix_time(row):
    if row.get("date_unixtime") is not None:
        return int(row["date_unixtime"])
    try:
        return int(datetime.fromisoformat(str(row.get("date")).replace("Z", "+00:00")).timestamp())
    except ValueError:
        return 0


def chat_rows(path, max_gib=None):
    with open_archive(path, max_gib=max_gib) as archive:
        manifest = read_manifest(archive)
        return manifest, list(chat_messages(archive))


def row_text(row):
    text = row.get("text")
    if isinstance(text, list):
        text = "".join(part if isinstance(part, str) else str(part.get("text", "")) for part in text)
    return text or ""


def row_brief(row):
    return {"id": row.get("id"), "date": row.get("date"), "from": row.get("from"), "from_id": row.get("from_id"),
            "text": row_text(row)[:300], "file_sha256": row.get("file_sha256"), "edited": row.get("edited"),
            "reply_to_message_id": row.get("reply_to_message_id")}


def row_content(row):
    return canonical(row)


def compare_chat_exports(first, second, first_fingerprint=None, second_fingerprint=None, max_gib=None):
    checked = [verify_chat_export(first, first_fingerprint, max_gib),
               verify_chat_export(second, second_fingerprint, max_gib)]
    (first_manifest, first_rows), (second_manifest, second_rows) = (chat_rows(first, max_gib), chat_rows(second, max_gib))
    def same_identity(name):
        value = (first_manifest.get(name) or {}).get("id")
        other = (second_manifest.get(name) or {}).get("id")
        return type(value) is int and type(other) is int and value != 0 and value == other
    same_chat, same_account = same_identity("chat"), same_identity("account")
    method = "number" if same_chat and same_account else "content"
    order = lambda rows: sorted(rows, key=lambda row: (str(row.get("date")), str(row.get("id"))))
    if method == "number":
        def by_number(rows):
            found = {}
            for row in rows:
                number = row.get("id")
                if type(number) is not int or number <= 0:
                    raise ValueError("Invalid message ID in chat comparison")
                if number in found:
                    raise ValueError("Duplicate message ID in chat comparison")
                found[number] = row
            return found
        left, right = by_number(first_rows), by_number(second_rows)
        pairs = [(left[k], right[k]) for k in left.keys() & right.keys()]
        only_first = [left[k] for k in left.keys() - right.keys()]
        only_second = [right[k] for k in right.keys() - left.keys()]
    else:
        def content_key(row):
            return row.get("from_id"), row_text(row), row.get("file_sha256"), row.get("media_type")

        waiting, pairs, only_first = {}, [], []
        only_second = []
        for row in order(second_rows):
            if row.get("type") == "unparsed":
                only_second.append(row)
            else:
                waiting.setdefault(content_key(row), []).append(row)
        for row in order(first_rows):
            if row.get("type") == "unparsed":
                only_first.append(row)
                continue
            candidates = waiting.get(content_key(row), [])
            match = next((c for c in candidates if abs(unix_time(c) - unix_time(row)) <= CLOCK_SLACK), None)
            if match is None:
                only_first.append(row)
            else:
                candidates.remove(match)
                pairs.append((row, match))
        only_second.extend(row for rows in waiting.values() for row in rows)
    changed = []
    for a, b in pairs:
        if row_content(a) != row_content(b):
            fields = sorted(k for k in a.keys() | b.keys()
                            if (k in a) != (k in b) or canonical(a.get(k)) != canonical(b.get(k)))
            changed.append({"first": row_brief(a), "second": row_brief(b), "changed_fields": fields})
    return {"format": "tgwitness-chat-comparison-v1", "method": method, "meaning": COMPARE_MEANING[method],
            "first": {"file": str(first), "fingerprint": checked[0]["fingerprint"], "exported_at": first_manifest.get("exported_at"),
                      "chat_id": (first_manifest.get("chat") or {}).get("id"), "messages": len(first_rows),
                      "key_pinned": checked[0]["key_pinned"]},
            "second": {"file": str(second), "fingerprint": checked[1]["fingerprint"], "exported_at": second_manifest.get("exported_at"),
                       "chat_id": (second_manifest.get("chat") or {}).get("id"), "messages": len(second_rows),
                       "key_pinned": checked[1]["key_pinned"]},
            "only_first": [row_brief(row) for row in order(only_first)],
            "only_second": [row_brief(row) for row in order(only_second)],
            "changed": sorted(changed, key=lambda item: (str(item["first"]["date"]), str(item["first"]["id"]))),
            "matched": len(pairs), "unchanged": len(pairs) - len(changed)}


def print_comparison(result, limit=50):
    import builtins

    def print(*values, **kwargs):
        builtins.print(*(safe_text(v) if isinstance(v, str) else v for v in values), **kwargs)

    first, second = result["first"], result["second"]
    print("Both archives verified. First " + str(first["exported_at"]) + " (" + str(first["messages"]) + " messages, key "
          + first["fingerprint"][:16] + "), second " + str(second["exported_at"]) + " (" + str(second["messages"])
          + " messages, key " + second["fingerprint"][:16] + ").")
    print(result["meaning"])
    for title, name in (("Only in the first archive", "only_first"), ("Only in the second archive", "only_second")):
        rows = result[name]
        print(title + ": " + str(len(rows)))
        for row in rows[:limit]:
            shown = row["text"] or ("file " + str(row["file_sha256"])[:16] if row["file_sha256"] else "")
            print("  #" + str(row["id"]) + " " + str(row["date"]) + " " + str(row["from"] or row["from_id"]) + ": "
                  + " ".join(shown.split())[:120])
    print("Changed: " + str(len(result["changed"])))
    for item in result["changed"][:limit]:
        print("  #" + str(item["first"]["id"]) + ": " + " ".join(item["first"]["text"].split())[:80] + "  ->  "
              + " ".join(item["second"]["text"].split())[:80])
        print("    Fields: " + ", ".join(item["changed_fields"]))
    if result["method"] == "number":
        print("Unchanged: " + str(result["unchanged"]))
    else:
        print("Matched: " + str(result["matched"]) + " (possible correspondence between the two exports)")
    if not (first["key_pinned"] and second["key_pinned"]):
        print("Signer identity is unpinned for at least one archive: compare the fingerprints with copies kept elsewhere.")


def message_id_summary(chat_id, ids):
    holes = missing_ranges(ids)
    return {"chat_id": chat_id, "numbered_per_chat": numbered_per_chat(chat_id),
            "first_id": ids[0] if ids else None, "last_id": ids[-1] if ids else None, "present": len(ids),
            "missing": sum(high - low + 1 for low, high in holes) if numbered_per_chat(chat_id) else None,
            "missing_ranges": [[low, high] for low, high in holes] if numbered_per_chat(chat_id) else []}


def check_message_ids(archive, manifest):
    claimed = strict_json(read_member(archive, "message-ids.json", MAX_JSON_BYTES))
    ids = sorted({m["id"] for m in chat_messages(archive) if type(m.get("id")) is int})
    counted = message_id_summary((manifest.get("chat") or {}).get("id"), ids)
    if {k: claimed.get(k) for k in counted} != counted:
        raise ValueError("message-ids.json disagrees with the messages in chat.json")
    return {k: counted[k] for k in ("first_id", "last_id", "present", "missing")} | {
        "missing_ranges": len(counted["missing_ranges"]), "numbered_per_chat": counted["numbered_per_chat"]}


def verify_handover(path, expected_fingerprint=None):
    with open_archive(path) as archive:
        names = archive.namelist()
        manifest = read_manifest(archive)
        if not is_format(manifest["format"], "handover-v1"):
            raise VerifierTooOld("Unsupported handover format")
        public = manifest["public_key"]
        fp = fingerprint(public)
        if expected_fingerprint and fp != expected_fingerprint:
            raise ValueError("Public key differs from the independently trusted fingerprint")
        key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True))
        key.verify(base64.b64decode(read_member(archive, "manifest.sig"), validate=True), canonical(manifest))
        files = manifest["files"]
        if set(names) != set(files) | {"manifest.json", "manifest.sig"}:
            raise ValueError("Unexpected or missing bundle members")
        for name, digest in files.items():
            if member_digest(archive, name) != digest:
                raise ValueError("File hash mismatch: " + name)
            if name.startswith("media/") and name[len("media/"):] != digest:
                raise ValueError("Attachment name differs from its SHA-256: " + name)
        sums = check_sums(archive, manifest)
        journal = manifest["journal"]
        count, head = journal["event_count"], journal["head_hash"]
        if type(count) is not int or count < 1 or not re.fullmatch(r"[0-9a-f]{64}", str(head)):
            raise ValueError("Malformed journal boundary")
        key.verify(base64.b64decode(journal["head_signature"], validate=True), bytes.fromhex(head))
        counts, previous, referenced = {"unchanged": 0, "minimised": 0}, None, set()
        with archive.open("records.jsonl") as stream:
            for line in bounded_lines(stream):
                record = strict_json(line)
                minimised = record.get("minimised")
                if set(record) != set(FIELDS) | {"hash", "signature"} | ({"minimised"} if "minimised" in record else set()):
                    raise ValueError("Unexpected or missing fields at record " + str(record.get("seq")))
                seq = record["seq"]
                if type(seq) is not int or not 1 <= seq <= count or (previous and seq <= previous["seq"]):
                    raise ValueError("Records out of journal order at record " + str(seq))
                if not re.fullmatch(r"[0-9a-f]{64}", str(record["hash"])):
                    raise ValueError("Malformed hash at record " + str(seq))
                if minimised is None:
                    if hashlib.sha256(canonical({k: record[k] for k in FIELDS})).hexdigest() != record["hash"]:
                        raise ValueError("Changed content at record " + str(seq))
                    if previous and previous["seq"] == seq - 1 and record["previous_hash"] != previous["hash"]:
                        raise ValueError("Broken hash chain at record " + str(seq))
                    counts["unchanged"] += 1
                else:
                    if not isinstance(minimised, list) or not minimised or not all(isinstance(x, str) for x in minimised):
                        raise ValueError("A minimised record must name what was withheld: record " + str(seq))
                    counts["minimised"] += 1
                key.verify(base64.b64decode(record["signature"], validate=True), bytes.fromhex(record["hash"]))
                if seq == count and record["hash"] != head:
                    raise ValueError("The last record differs from the journal head")
                if record["kind"] in ("media.saved", "actor.avatar_saved", "secret_chat.file"):
                    digest = (record["payload"] or {}).get("media_sha256")
                    if "media/" + str(digest) in files:
                        referenced.add("media/" + digest)
                previous = record
        if counts != {k: manifest["counts"].get(k) for k in counts}:
            raise ValueError("Record counts differ from the signed manifest")
        if {name for name in files if name.startswith("media/")} - referenced:
            raise ValueError("The extract carries an attachment no record refers to")
        def describes(subject):
            return subject.get("records_sha256") == files.get("records.jsonl") and subject.get("head_hash") == head
        seal = archive_seal(archive, "report.html", public) if "report.html" in files else None
        if seal and not describes(seal["subject"]):
            raise ValueError("The report seal describes a different extract")
        companions = report_companions(archive, manifest, public, describes)
        board_disclosure = verify_board_disclosure(archive, manifest)
    return {"format": manifest["format"], "fingerprint": fp, "key_pinned": bool(expected_fingerprint),
            "board_disclosure": board_disclosure,
            "purpose": manifest.get("purpose"), "records_unchanged": counts["unchanged"],
            "records_minimised": counts["minimised"], "records_left_out": manifest["counts"].get("left_out"),
            "journal_events": count, "head_hash": head, "attachments": len(referenced),
            "files_checked": len(files), "sha256sums": sums, "report_seal": seal,
            "report_json": companions["json"], "report_parts": companions["parts"], "report_pdf": companions["pdf"],
            "case": manifest.get("case") or {}, "producer": manifest.get("producer")}


GAP_FORMAT = "tgwitness-message-gaps-v1"
SHARED_KINDS = ("private", "bot", "group")
NUMBERED_KINDS = ("supergroup", "channel")
GAP_BANDWIDTH = 900
GAP_NEIGHBORS = 120
GAP_HORIZON = 6 * 3600
GAP_UNKNOWN_SHARE = 0.05
GAP_OUT_OF_SCOPE_SHARE = 1.0
GAP_UNKNOWN_FLOOR = 0.05
GAP_PROVEN_WEIGHT = 1.0
GAP_HIGH, GAP_MEDIUM = 0.85, 0.65
GAP_EXAMPLES = 100
GAP_TOLERANCE = 0.011
CHANNEL_BASE = -1000000000000
GAP_MEANING = ("Private chats, bots and basic groups share one message number sequence for the account; a number absent "
               "between two exported messages belonged to a message this export does not hold. Its chat is proven when an "
               "exported reply or pin names it, otherwise estimated from which chats were active in the time between its "
               "neighbours. Channels and supergroups number their messages per chat.")


def gap_time(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return None if parsed.tzinfo is None else int(parsed.timestamp())


def gap_peer(value):
    if not isinstance(value, dict):
        return None
    for name, field, sign, base in (("PeerUser", "user_id", 1, 0), ("PeerChat", "chat_id", -1, 0),
                                    ("PeerChannel", "channel_id", -1, CHANNEL_BASE)):
        if value.get("_") == name and type(value.get(field)) is int and value[field] > 0:
            return base + sign * value[field]
    return None


def gap_shared(chat_id):
    return type(chat_id) is int and chat_id != 0 and chat_id > CHANNEL_BASE


def gap_scope(options, inventory):
    reasons = set()
    kinds = options.get("chat_kinds")
    if isinstance(kinds, list) and not set(SHARED_KINDS) <= set(kinds):
        reasons.add("chat_kinds")
    for key, reason in (("chat_ids", "chat_ids"), ("sender_ids", "sender_filter"), ("text_contains", "text_filter"),
                        ("own_messages_only", "own_messages_only")):
        if options.get(key):
            reasons.add(reason)
    if options.get("include_archived") is False:
        reasons.add("archived_excluded")
    chats = inventory.get("chats") if isinstance(inventory.get("chats"), list) else []
    if any(isinstance(chat, dict) and chat.get("kind") in SHARED_KINDS and chat.get("selected") is not True for chat in chats):
        reasons.add("unselected_chats")
    if inventory.get("discovery_complete") is not True:
        reasons.add("inventory_incomplete")
    return {"complete": not reasons, "reasons": sorted(reasons), "from_utc": options.get("from_utc"),
            "to_utc": options.get("to_utc")}


def gap_kernel(at, start, end):
    width = GAP_BANDWIDTH
    if end - start < 1:
        return math.exp(-abs(at - start) / width)
    if at <= start:
        total = width * (math.exp(-(start - at) / width) - math.exp(-(end - at) / width))
    elif at >= end:
        total = width * (math.exp(-(at - end) / width) - math.exp(-(at - start) / width))
    else:
        total = width * (2 - math.exp(-(at - start) / width) - math.exp(-(end - at) / width))
    return total / (end - start)


class MessageGaps:
    def __init__(self, scope):
        self.scope = scope
        self.kinds, self.ids, self.times = {}, {}, {}
        self.references = array("q")
        self.undated = 0
        self.borderline = set()

    def add(self, chat_id, kind, record):
        number = record.get("id")
        if (type(chat_id) is not int or type(number) is not int or number < 1
                or kind not in SHARED_KINDS and kind not in NUMBERED_KINDS):
            return
        at = gap_time(record.get("date"))
        if at is None:
            self.undated += 1
        self.kinds.setdefault(chat_id, kind)
        self.ids.setdefault(chat_id, array("q")).append(number)
        self.times.setdefault(chat_id, array("q")).append(-1 if at is None else at)
        reply = record.get("reply_to")
        if kind not in SHARED_KINDS or not isinstance(reply, dict):
            return
        target = reply.get("reply_to_msg_id")
        if type(target) is not int or target < 1:
            return
        owner = chat_id if reply.get("reply_to_peer_id") is None else gap_peer(reply.get("reply_to_peer_id"))
        if gap_shared(owner):
            self.references.extend((target, owner, chat_id, number, 1 if record.get("_") == "MessageService" else 0))

    def ordered(self, chat_id):
        ids, times = self.ids[chat_id], self.times[chat_id]
        if all(ids[i] > ids[i + 1] for i in range(len(ids) - 1)):
            for i in range(len(ids) - 1, -1, -1):
                yield ids[i], times[i]
        else:
            yield from sorted(zip(ids, times))

    def tagged(self, chat_id):
        for number, at in self.ordered(chat_id):
            yield number, at, chat_id

    def result(self):
        shared = sorted(chat for chat, kind in self.kinds.items() if kind in SHARED_KINDS)
        ids, times, owners = array("q"), array("q"), array("q")
        conflicts, inversions = {"count": 0, "examples": []}, {"count": 0, "examples": []}
        dated = -1
        for number, at, chat in heapq.merge(*(self.tagged(chat) for chat in shared)):
            if ids and number == ids[-1]:
                conflicts["count"] += 1
                if len(conflicts["examples"]) < GAP_EXAMPLES:
                    conflicts["examples"].append([number, owners[-1], chat])
                continue
            if at >= 0:
                if dated >= 0 and at < dated - 60:
                    inversions["count"] += 1
                    if len(inversions["examples"]) < GAP_EXAMPLES:
                        inversions["examples"].append([number, at, dated])
                dated = max(dated, at)
            ids.append(number)
            times.append(at)
            owners.append(chat)
        proven, claims = self.proven(ids)
        conflicts["count"] += claims["count"]
        conflicts["examples"] = (conflicts["examples"] + claims["examples"])[:GAP_EXAMPLES]
        gaps, by_chat, outside = self.attribute(ids, times, owners, proven)
        for chat in shared:
            by_chat.setdefault(chat, {"messages": 0, "proven": 0, "expected": 0.0, "high": 0})["messages"] = len(self.ids[chat])
        first = ids[0] if ids else None
        below = [list(item) for target, item in sorted(proven.items()) if first is not None and target < first]
        dated_times = [at for at in times if at >= 0]
        return {
            "format": GAP_FORMAT,
            "method": {"bandwidth_seconds": GAP_BANDWIDTH, "neighbors": GAP_NEIGHBORS, "horizon_seconds": GAP_HORIZON,
                       "unknown_share": GAP_UNKNOWN_SHARE, "out_of_scope_share": GAP_OUT_OF_SCOPE_SHARE,
                       "unknown_floor": GAP_UNKNOWN_FLOOR, "unknown_floor_run_factor": "1+log2(count)",
                       "proven_weight": GAP_PROVEN_WEIGHT,
                       "high": GAP_HIGH, "medium": GAP_MEDIUM},
            "meaning": GAP_MEANING,
            "scope": self.scope,
            "shared": {
                "chats": len(shared), "messages": len(ids), "undated": self.undated,
                "first_id": first, "last_id": ids[-1] if ids else None,
                "first_at": min(dated_times) if dated_times else None, "last_at": max(dated_times) if dated_times else None,
                "absent": sum(gap["count"] for gap in gaps), "runs": len(gaps), "below_first": first - 1 if first else 0,
                "proven": sum(len(gap["proven"]) for gap in gaps), "below_first_proven": below,
                "conflicts": conflicts, "time_inversions": inversions,
                "by_chat": [[chat, item["messages"], item["proven"], round(item["expected"], 2), item["high"]]
                            for chat, item in sorted(by_chat.items())],
                "not_in_export": {"expected": round(outside, 2)},
                "gaps": gaps,
            },
            "chats": self.numbered(),
        }

    def proven(self, ids):
        refs, found, claims = self.references, {}, {"count": 0, "examples": []}
        entries = sorted(tuple(refs[i:i + 5]) for i in range(0, len(refs), 5))
        for target, owner, source_chat, source_id, relation in entries:
            position = bisect.bisect_left(ids, target)
            if position < len(ids) and ids[position] == target or ids and target > ids[-1]:
                continue
            if target in found:
                if found[target][1] != owner:
                    claims["count"] += 1
                    if len(claims["examples"]) < GAP_EXAMPLES:
                        claims["examples"].append([target, found[target][1], owner])
                continue
            found[target] = (target, owner, source_chat, source_id, relation)
        return found, claims

    def attribute(self, ids, times, owners, proven):
        gaps, by_chat, outside = [], {}, 0.0
        share = GAP_UNKNOWN_SHARE if self.scope.get("complete") else GAP_OUT_OF_SCOPE_SHARE
        targets = sorted(proven)
        for right in range(1, len(ids)):
            left = right - 1
            if ids[right] - ids[left] < 2:
                continue
            low, high = ids[left] + 1, ids[right] - 1
            start, end = self.edge(times, left, -1), self.edge(times, right, 1)
            if start is None:
                start = end
            if end is None:
                end = start
            if start is None:
                start = end = 0
            if end < start:
                start, end = end, start
            scores = {}
            for index in range(left, max(-1, left - GAP_NEIGHBORS), -1):
                at = times[index]
                if at < 0:
                    continue
                if at < start - GAP_HORIZON:
                    break
                scores[owners[index]] = scores.get(owners[index], 0.0) + gap_kernel(at, start, end)
            for index in range(right, min(len(ids), right + GAP_NEIGHBORS)):
                at = times[index]
                if at < 0:
                    continue
                if at > end + GAP_HORIZON:
                    break
                scores[owners[index]] = scores.get(owners[index], 0.0) + gap_kernel(at, start, end)
            inside = [list(proven[target]) for target in
                      targets[bisect.bisect_left(targets, low):bisect.bisect_right(targets, high)]]
            for item in inside:
                scores[item[1]] = scores.get(item[1], 0.0) + GAP_PROVEN_WEIGHT
                by_chat.setdefault(item[1], {"messages": 0, "proven": 0, "expected": 0.0, "high": 0})["proven"] += 1
            count = high - low + 1
            unproven = count - len(inside)
            known = sum(scores.values())
            other = share * known + GAP_UNKNOWN_FLOOR * (1 + math.log2(count))
            whole = known + other
            ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
            best_chat, best = (ranked[0][0], ranked[0][1] / whole) if ranked else (None, 0.0)
            top, level = (best_chat, best) if best >= other / whole else (None, other / whole)
            confidence = ("proven" if unproven == 0 else "high" if level >= GAP_HIGH else
                          "medium" if level >= GAP_MEDIUM else "low")
            second = ranked[1][1] / whole if len(ranked) > 1 else 0.0
            if (unproven and (min(abs(level - GAP_HIGH), abs(level - GAP_MEDIUM)) <= GAP_TOLERANCE
                              or abs(best - other / whole) <= GAP_TOLERANCE or best - second <= GAP_TOLERANCE)):
                self.borderline.add(len(gaps))
            for chat, score in ranked:
                item = by_chat.setdefault(chat, {"messages": 0, "proven": 0, "expected": 0.0, "high": 0})
                item["expected"] += unproven * score / whole
            outside += unproven * other / whole
            if top is not None and confidence in ("high", "proven"):
                by_chat[top]["high"] += 1
            gaps.append({"from": low, "to": high, "count": count,
                         "after": [ids[left], owners[left], times[left]], "before": [ids[right], owners[right], times[right]],
                         "proven": inside, "likely": [[chat, round(score / whole, 3)] for chat, score in ranked[:3]
                                                      if score / whole >= 0.0005],
                         "other": round(other / whole, 3), "top": top, "confidence": confidence})
        return gaps, by_chat, outside

    @staticmethod
    def edge(times, index, step):
        while 0 <= index < len(times):
            if times[index] >= 0:
                return times[index]
            index += step
        return None

    def numbered(self):
        result = []
        for chat in sorted(chat for chat, kind in self.kinds.items() if kind in NUMBERED_KINDS):
            pairs, ranges, absent, repeated = [], [], 0, 0
            for number, at in self.ordered(chat):
                if pairs and number == pairs[-1][0]:
                    repeated += 1
                    continue
                if pairs and number - pairs[-1][0] > 1:
                    ranges.append([pairs[-1][0] + 1, number - 1, pairs[-1][1], at])
                    absent += number - pairs[-1][0] - 1
                pairs.append((number, at))
            result.append({"chat": chat, "kind": self.kinds[chat], "first": pairs[0][0], "last": pairs[-1][0],
                           "present": len(pairs), "absent": absent, "below_first": pairs[0][0] - 1,
                           "repeated": repeated, "ranges": ranges})
        return result


def gap_values_match(declared, computed):
    if isinstance(computed, dict):
        return isinstance(declared, dict) and declared.keys() == computed.keys() and all(
            gap_values_match(declared[key], computed[key]) for key in computed)
    if isinstance(computed, list):
        return isinstance(declared, list) and len(declared) == len(computed) and all(
            gap_values_match(a, b) for a, b in zip(declared, computed))
    if type(computed) is float or type(declared) is float:
        return (type(declared) in (int, float) and type(computed) in (int, float)
                and abs(declared - computed) <= max(GAP_TOLERANCE, abs(computed) * 0.001))
    return type(declared) is type(computed) and declared == computed


def gap_entry_matches(declared, computed, borderline):
    if not isinstance(declared, dict) or declared.keys() != computed.keys():
        return False
    for key in computed:
        if key == "likely":
            if not isinstance(declared[key], list) or any(not isinstance(item, list) or len(item) != 2 for item in declared[key]):
                return False
            ours, theirs = dict((chat, value) for chat, value in computed[key]), dict(
                (chat, value) for chat, value in declared[key])
            for chat in set(ours) | set(theirs):
                if chat not in ours or chat not in theirs:
                    if not borderline or max(ours.get(chat, 0.0), theirs.get(chat, 0.0)) > 2 * GAP_TOLERANCE:
                        return False
                elif not gap_values_match(theirs[chat], ours[chat]):
                    return False
        elif key in ("top", "confidence"):
            if declared[key] != computed[key] and not borderline:
                return False
        elif not gap_values_match(declared[key], computed[key]):
            return False
    return True


def gaps_match(declared, computed, borderline):
    if not isinstance(declared, dict) or declared.keys() != computed.keys():
        return False
    for key in computed:
        if key == "shared":
            ours, theirs = computed[key], declared[key]
            if not isinstance(theirs, dict) or theirs.keys() != ours.keys():
                return False
            for field in ours:
                if field == "gaps":
                    if (not isinstance(theirs[field], list) or len(theirs[field]) != len(ours[field])
                            or not all(gap_entry_matches(a, b, index in borderline)
                                       for index, (a, b) in enumerate(zip(theirs[field], ours[field])))):
                        return False
                elif field == "by_chat":
                    if (not isinstance(theirs[field], list) or len(theirs[field]) != len(ours[field])
                            or not all(isinstance(a, list) and len(a) == 5 and a[:3] == b[:3]
                                       and gap_values_match(a[3], b[3]) and (a[4] == b[4] or borderline)
                                       for a, b in zip(theirs[field], ours[field]))):
                        return False
                elif not gap_values_match(theirs[field], ours[field]):
                    return False
        elif not gap_values_match(declared[key], computed[key]):
            return False
    return True


def gap_lines(result):
    shared = result["shared"]
    lines = []
    if shared["messages"]:
        counts = {}
        for gap in shared["gaps"]:
            counts[gap["confidence"]] = counts.get(gap["confidence"], 0) + 1
        lines.append("Private chats, bots and basic groups: " + str(shared["absent"]) + " message number(s) absent in "
                     + str(shared["runs"]) + " run(s) between " + str(shared["first_id"]) + " and " + str(shared["last_id"])
                     + "; chat proven by a reply or pin for " + str(shared["proven"]) + ", estimated for the rest ("
                     + ", ".join(key + " " + str(counts[key]) for key in ("proven", "high", "medium", "low") if key in counts)
                     + ").")
        if shared["conflicts"]["count"] or shared["time_inversions"]["count"]:
            lines.append("Number sequence anomalies: " + str(shared["conflicts"]["count"]) + " conflicting claim(s), "
                         + str(shared["time_inversions"]["count"]) + " time inversion(s).")
    numbered = [chat for chat in result["chats"] if chat["absent"]]
    if result["chats"]:
        lines.append("Channels and supergroups: " + str(sum(chat["absent"] for chat in result["chats"]))
                     + " message number(s) absent in " + str(len(numbered)) + " of " + str(len(result["chats"])) + " chat(s).")
    if not result["scope"]["complete"]:
        lines.append("The export scope is limited (" + ", ".join(result["scope"]["reasons"])
                     + "); absent numbers include messages outside it.")
    return lines
def check_attachments(archive, manifest):
    files = manifest["files"]
    for name, digest in files.items():
        if name.startswith("media/") and name[len("media/"):] != digest:
            raise ValueError("Attachment name differs from its SHA-256: " + name)
    referenced, hash_files, count, numbers = 0, set(), 0, set()
    for message in chat_messages(archive):
        count += 1
        number = message.get("id")
        if type(number) is int:
            if number in numbers:
                raise ValueError("Duplicate message ID in chat.json: " + str(number))
            numbers.add(number)
        if message.get("server_hashes") is not None:
            hashes = message["server_hashes"]
            validate_server_hashes(hashes)
            digest = hashlib.sha256(canonical(hashes)).hexdigest()
            name = "hashes/" + digest + ".json"
            if (message.get("file_hash_sha256") != digest or files.get(name) != digest or message.get("file")
                    or message.get("file_status") == "hashes_only" and hashes["status"] != "complete"):
                raise ValueError("Chat file-hash reference or completeness mismatch")
            hash_files.add(name)
        name = message.get("file")
        if name is None:
            continue
        if not isinstance(name, str) or files.get(name) is None or files[name] != message.get("file_sha256"):
            raise ValueError("Message #" + str(message.get("id")) + " names an attachment missing from the archive")
        referenced += 1
    if {name for name in files if name.startswith("hashes/")} != hash_files:
        raise ValueError("Unreferenced chat file-hash manifest")
    if type(manifest.get("message_count")) is not int or manifest["message_count"] != count:
        raise ValueError("Chat message count differs from the signed manifest")
    return referenced


def chat_messages(archive):
    with archive.open("chat.json") as stream:
        inside, header, header_bytes, separator = False, [], 0, None
        lines = iter(bounded_lines(io.TextIOWrapper(stream, encoding="utf-8")))
        for raw in lines:
            line = raw.strip()
            if not inside:
                if line == '"messages": [':
                    json.loads("".join(header) + '"messages": []}')
                    inside = True
                else:
                    header_bytes += len(raw.encode("utf-8"))
                    if header_bytes > MAX_JSON_BYTES:
                        raise ValueError("Chat header exceeds the verification limit")
                    header.append(raw)
                continue
            if line.startswith("]"):
                if separator:
                    raise ValueError("Trailing comma after chat message")
                tail = "".join(line.split())
                for rest in lines:
                    tail += "".join(rest.split())
                    if len(tail) > 2:
                        raise ValueError("Unexpected data after chat messages")
                if tail != "]}":
                    raise ValueError("Invalid chat messages terminator")
                return
            if not line:
                continue
            if separator is False:
                raise ValueError("Missing comma between chat messages")
            separator = line.endswith(",")
            message = strict_json(line.removesuffix(","))
            if not isinstance(message, dict):
                raise ValueError("Chat message must be an object")
            yield message
        raise ValueError("Missing or unsupported chat messages array")


def verify_parts(archive, manifest):
    ranges = []
    for part in manifest["parts"]:
        statement = part["statement"]
        if not is_format(statement.get("format"), "chat-part-v1") or statement["chat_id"] != manifest["chat"]["id"]:
            raise ValueError("Part statement does not belong to this chat export")
        Ed25519PublicKey.from_public_bytes(base64.b64decode(statement["fetched_by_public_key"], validate=True)).verify(
            base64.b64decode(part["signature"], validate=True), canonical(statement))
        for item in statement["ranges"]:
            ranges.append((item["low"], item["high"], item, statement))
    ranges.sort(key=lambda r: r[0])
    for before, after in zip(ranges, ranges[1:]):
        if after[0] <= before[1]:
            raise ValueError("Signed ranges overlap")
    lows = [r[0] for r in ranges]
    hashes, counts = [hashlib.sha256() for _ in ranges], [0] * len(ranges)
    for message in chat_messages(archive):
        i = bisect.bisect_right(lows, message["id"]) - 1
        if i < 0 or message["id"] > ranges[i][1]:
            raise ValueError("Message #" + str(message["id"]) + " is outside every signed range")
        hashes[i].update(canonical(message) + b"\n")
        counts[i] += 1
    accounts = {}
    for (low, high, item, statement), digest, count in zip(ranges, hashes, counts):
        if count != item["count"] or digest.hexdigest() != item["sha256"]:
            raise ValueError("Messages " + str(low) + "-" + str(high) + " differ from what the account signed")
        key = statement["fetched_by_public_key"]
        summary = accounts.setdefault(key, {"account_id": statement["account_id"], "fingerprint": fingerprint(key),
                                            "ranges": 0, "messages": 0})
        summary["ranges"] += 1
        summary["messages"] += count
    return list(accounts.values())


def account_export_integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError("Invalid account export " + name)
    return value

def account_export_digest(value, name):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("Invalid account export " + name)
    return value

def account_export_timestamp(value, name):
    if not isinstance(value, str):
        raise ValueError("Invalid account export " + name)
    parsed = parse_time(value)
    if parsed.tzinfo is None or parsed.utcoffset().total_seconds() != 0:
        raise ValueError("Account export times must have an explicit UTC offset: " + name)
    return parsed

class AccountExportCheck:
    def __init__(self, archive, expected_fingerprint):
        self.archive = archive
        self.expected_fingerprint = expected_fingerprint

    def verify_manifest(self):
        names = self.archive.namelist()
        self.manifest = read_manifest(self.archive)
        if self.manifest.get("format") != "tgwitness-account-export-v1":
            raise VerifierTooOld("Unsupported account export format")
        self.public = self.manifest["public_key"]
        self.fp = fingerprint(self.public)
        if self.manifest.get("fingerprint") != self.fp:
            raise ValueError("Account export fingerprint does not match the signing key")
        if self.expected_fingerprint and self.fp != self.expected_fingerprint:
            raise ValueError("Public key differs from the independently trusted fingerprint")
        self.key = Ed25519PublicKey.from_public_bytes(base64.b64decode(self.public, validate=True))
        self.key.verify(base64.b64decode(read_member(self.archive, "manifest.sig"), validate=True), canonical(self.manifest))
        self.files = self.manifest["files"]
        if not isinstance(self.files, dict) or set(names) != set(self.files) | {"manifest.json", "manifest.sig"}:
            raise ValueError("Unexpected or missing account export members")
        for name, checksum in self.files.items():
            if (not name or "\\" in name or ":" in name or name.startswith("/")
                    or any(part in ("", ".", "..") for part in name.split("/"))):
                raise ValueError("Unsafe account export member name")
            if member_digest(self.archive, name) != account_export_digest(checksum, "file hash"):
                raise ValueError("File hash mismatch: " + name)
        for required in ("job.json", "inventory.json", "SHA256SUMS", "verify.py", "README.txt"):
            if required not in self.files:
                raise ValueError("Missing account export member: " + required)
        self.sums = check_sums(self.archive, self.manifest)
        self.account_id = account_export_integer(self.manifest["account_id"], "account ID", 1)
        self.job_id = self.manifest["job_id"]
        if not isinstance(self.job_id, str) or not self.job_id:
            raise ValueError("Invalid account export job ID")
        self.options = self.manifest["options"]
        if not isinstance(self.options, dict):
            raise ValueError("Invalid account export options")
        self.options_hash = hashlib.sha256(canonical(self.options)).hexdigest()
        if account_export_digest(self.manifest["options_sha256"], "options hash") != self.options_hash:
            raise ValueError("Account export options hash mismatch")


    def signed(self, name, kind):
        envelope = strict_json(read_member(self.archive, name))
        statement = envelope["statement"]
        if (statement.get("format") != "tgwitness-account-export-" + kind + "-v1"
                or statement.get("public_key") != self.public or statement.get("job_id") != self.job_id
                or type(statement.get("account_id")) is not int or statement["account_id"] != self.account_id
                or statement.get("options_sha256") != self.options_hash):
            raise ValueError("Account export signed identity/options mismatch: " + name)
        self.key.verify(base64.b64decode(envelope["signature"], validate=True), canonical(statement))
        return statement, hashlib.sha256(canonical(envelope)).hexdigest()


    def verify_inventory(self):
        job, _ = self.signed("job.json", "job")
        if job.get("options") != self.options or job.get("created_at") != self.manifest.get("created_at"):
            raise ValueError("Account export job does not match the manifest")
        account_export_timestamp(job["created_at"], "created_at")
        account_export_timestamp(self.manifest["completed_at"], "completed_at")
        self.inventory, self.inventory_hash = self.signed("inventory.json", "inventory")
        if self.inventory_hash != account_export_digest(self.manifest["inventory_sha256"], "inventory hash"):
            raise ValueError("Account export inventory hash mismatch")
        account_export_timestamp(self.inventory["observed_at"], "inventory observed_at")
        if (type(self.inventory.get("discovery_complete")) is not bool or not isinstance(self.inventory.get("gaps"), list)
                or any(not isinstance(gap, str) for gap in self.inventory["gaps"])):
            raise ValueError("Invalid account export discovery coverage")
        if not isinstance(self.inventory.get("chats"), list) or not isinstance(self.inventory.get("tasks"), list):
            raise ValueError("Invalid account export task inventory")
        self.tasks = {}
        self.chats = {}
        for chat in self.inventory["chats"]:
            cid = chat.get("id")
            if type(cid) is not int or not cid or cid in self.chats or type(chat.get("selected")) is not bool:
                raise ValueError("Invalid or duplicate account export inventory chat")
            if chat["selected"]:
                if self.options.get("chat_ids") and cid not in self.options["chat_ids"]:
                    raise ValueError("Account export selected a chat outside its frozen options")
                if self.options.get("chat_kinds") is not None and chat.get("kind") not in self.options["chat_kinds"]:
                    raise ValueError("Account export selected a chat kind outside its frozen options")
                if self.options.get("include_archived") is False and chat.get("archived"):
                    raise ValueError("Account export selected an excluded archived chat")
            self.chats[cid] = chat
        metadata_categories = {"profile", "contacts", "sessions", "profile_photos", "stories", "other_data"}
        for task in self.inventory["tasks"]:
            task_id, category = task["id"], task["category"]
            if not isinstance(task_id, str) or not task_id or task_id in self.tasks:
                raise ValueError("Duplicate or invalid account export task ID")
            account_export_integer(task["cursor_start"], "initial cursor")
            if category == "messages":
                if type(task.get("chat_id")) is not int or task["chat_id"] == 0:
                    raise ValueError("Invalid message task chat ID")
                if task["chat_id"] not in self.chats or not self.chats[task["chat_id"]]["selected"]:
                    raise ValueError("Account export message task is outside the selected inventory")
                newest = account_export_integer(task["newest_message_id"], "newest message ID")
                if task["cursor_start"] != newest + 1 or type(task.get("own_only")) is not bool:
                    raise ValueError("Invalid message task boundary")
            elif category not in metadata_categories or task.get("chat_id") is not None:
                raise ValueError("Invalid account export task category")
            self.tasks[task_id] = {"statement": task, "cursor": task["cursor_start"], "terminal": False, "ok": True}

        self.inventory_omissions = ["Selected chat has no history task: " + str(cid) for cid, chat in self.chats.items()
                               if chat["selected"] and not any(t["statement"].get("chat_id") == cid for t in self.tasks.values())]
        category_options = {"profile": "include_profile", "contacts": "include_contacts",
                            "sessions": "include_session_metadata", "profile_photos": "include_profile_photos",
                            "stories": "include_stories", "other_data": "include_other_data"}
        for category, option in category_options.items():
            present = any(t["statement"]["category"] == category for t in self.tasks.values())
            if self.options.get(option) is True and not present:
                self.inventory_omissions.append("Selected category has no acquisition task: " + category)
            if self.options.get(option) is False and present:
                raise ValueError("Account export task is excluded by its frozen options")


    def verify_pages(self, temporary):
        self.receipts = []
        for name in self.files:
            if name.startswith("receipts/"):
                found = re.fullmatch(r"receipts/(\d+)\.json", name)
                if not found:
                    raise ValueError("Unexpected account export receipt name")
                self.receipts.append((int(found[1]), name))
        self.receipts.sort()
        self.counts = dict.fromkeys(("records", "messages", "media_saved", "media_skipped", "bytes_saved"), 0)
        self.media_hashed = 0
        self.hash_manifests, self.hash_index = set(), hashlib.sha256()
        seen = sqlite3.connect(Path(temporary) / "seen.sqlite3")
        seen.execute("CREATE TABLE messages (chat INTEGER, id INTEGER, PRIMARY KEY (chat, id)) WITHOUT ROWID")
        self.data_files, self.media_files, self.failed_attachments, self.failed_pages, self.messages_seen = set(), set(), 0, 0, 0
        self.previous = "0" * 64
        self.gaps = MessageGaps(gap_scope(self.options, self.inventory))
        self.since = account_export_timestamp(self.options["from_utc"], "from_utc") if self.options.get("from_utc") else None
        self.until = account_export_timestamp(self.options["to_utc"], "to_utc") if self.options.get("to_utc") else None
        try:
            for seq, (number, name) in enumerate(self.receipts, 1):
                self.verify_page(seq, number, name, seen)
        finally:
            seen.close()

    def verify_page(self, seq, number, name, seen):
        receipt, receipt_hash = self.signed(name, "page")
        if (number != seq or type(receipt.get("seq")) is not int or receipt["seq"] != seq
                or receipt.get("previous_receipt_sha256") != self.previous
                or receipt.get("inventory_sha256") != self.inventory_hash):
            raise ValueError("Broken account export receipt chain at " + str(seq))
        self.previous = receipt_hash
        state = self.tasks.get(receipt.get("task_id"))
        if state is None or state["terminal"]:
            raise ValueError("Unknown or already terminal account export task")
        task = state["statement"]
        if (receipt.get("category") != task["category"] or receipt.get("chat_id") != task.get("chat_id")
                or type(receipt.get("chat_id")) is not type(task.get("chat_id"))):
            raise ValueError("Account export receipt task scope mismatch")
        before = account_export_integer(receipt["cursor_before"], "page cursor before")
        after = account_export_integer(receipt["cursor_after"], "page cursor after")
        if before != state["cursor"] or type(receipt.get("terminal")) is not bool:
            raise ValueError("Broken account export task cursor continuity")
        if receipt.get("outcome") not in ("ok", "failed"):
            raise ValueError("Invalid account export receipt outcome")
        account_export_timestamp(receipt["captured_from"], "captured_from")
        account_export_timestamp(receipt["captured_until"], "captured_until")
        count = account_export_integer(receipt["count"], "page record count")
        page_seen = account_export_integer(receipt["seen_count"], "page seen count")
        if page_seen < count:
            raise ValueError("Account export seen count is shorter than the saved page")
        if task["category"] == "messages":
            self.messages_seen += page_seen
        if task["category"] == "messages" and (after > before or (after == before and not receipt["terminal"])):
            raise ValueError("Invalid account export message pagination boundary")
        data_name = receipt["data_file"]
        matched = re.fullmatch(r"data/(\d+)\.jsonl", data_name) if isinstance(data_name, str) else None
        if not matched or int(matched[1]) != seq or data_name in self.data_files or data_name not in self.files:
            raise ValueError("Missing, reused or mismatched account export page data")
        self.data_files.add(data_name)
        if self.files[data_name] != account_export_digest(receipt["data_sha256"], "page data hash"):
            raise ValueError("Account export receipt data hash mismatch")
        actual, last_id = 0, before
        with self.archive.open(data_name) as stream:
            for line in bounded_lines(stream):
                last_id = self.verify_record(line, task, after, last_id, seen)
                actual += 1
        if actual != count:
            raise ValueError("Account export page record count mismatch")
        self.counts["records"] += actual
        state.update(cursor=after, terminal=receipt["terminal"], ok=state["ok"] and receipt["outcome"] == "ok")
        self.failed_pages += receipt["outcome"] == "failed"

    def verify_record(self, line, task, after, last_id, seen):
        record = strict_json(line)
        if not isinstance(record, dict) or line != canonical(record) + b"\n":
            raise ValueError("Account export records must be canonical JSONL")
        if record.get("category") != task["category"]:
            raise ValueError("Account export record category mismatch")
        if task["category"] == "messages":
            message_id = account_export_integer(record["id"], "message ID", 1)
            if (type(record.get("chat_id")) is not int or record["chat_id"] != task["chat_id"]
                    or message_id > task["newest_message_id"]
                    or not after <= message_id < last_id):
                raise ValueError("Account export message outside the signed pagination boundary")
            last_id = message_id
            if (task["own_only"] or self.options.get("own_messages_only")) and record.get("outgoing") is not True:
                raise ValueError("Account export own-message scope mismatch")
            at = account_export_timestamp(record["date"], "message date")
            if (self.since and at < self.since) or (self.until and at >= self.until):
                raise ValueError("Account export message outside the selected date range")
            if self.options.get("sender_ids") and record.get("from_id") not in self.options["sender_ids"]:
                raise ValueError("Account export sender selection mismatch")
            if self.options.get("text_contains") and not any(term.casefold() in (record.get("text") or "").casefold()
                                                         for term in self.options["text_contains"]):
                raise ValueError("Account export text selection mismatch")
            try:
                seen.execute("INSERT INTO messages VALUES (?, ?)", (task["chat_id"], message_id))
            except sqlite3.IntegrityError:
                raise ValueError("Duplicate account export message") from None
            self.counts["messages"] += 1
            self.gaps.add(task["chat_id"], self.chats[task["chat_id"]].get("kind"), record)
        self.verify_attachments(record)
        return last_id

    def verify_attachments(self, record):
        attachments = record.get("attachments", [])
        if not isinstance(attachments, list):
            raise ValueError("Invalid account export attachments")
        for attachment_index, attachment in enumerate(attachments):
            outcome = attachment.get("outcome")
            server_hashes = attachment.get("server_hashes")
            if server_hashes is not None:
                validate_server_hashes(server_hashes)
                manifest_digest = hashlib.sha256(canonical(server_hashes)).hexdigest()
                hash_file = "hashes/" + manifest_digest + ".json"
                if self.files.get(hash_file) != manifest_digest:
                    raise ValueError("File-hash manifest differs from its signed message record")
                self.hash_manifests.add(hash_file)
                self.hash_index.update(canonical({"category": record["category"], "chat_id": record.get("chat_id"),
                    "message_id": record.get("id"), "attachment_index": attachment_index, "manifest": hash_file}) + b"\n")
            if outcome == "saved":
                checksum = account_export_digest(attachment["sha256"], "attachment hash")
                media_name = "media/" + checksum
                size = account_export_integer(attachment["bytes"], "attachment byte count")
                if (attachment.get("file") != media_name or self.files.get(media_name) != checksum
                        or self.archive.getinfo(media_name).file_size != size):
                    raise ValueError("Account export attachment bytes/hash mismatch")
                expected = attachment.get("expected_bytes")
                if expected is not None and account_export_integer(expected, "expected attachment bytes") != size:
                    raise ValueError("Account export attachment size differs from observation")
                representation = attachment.get("representation")
                if representation is not None and (not isinstance(representation, dict)
                        or account_export_integer(representation.get("bytes"), "attachment representation bytes") != size):
                    raise ValueError("Account export attachment size differs from its representation")
                self.media_files.add(media_name)
                self.counts["media_saved"] += 1
                self.counts["bytes_saved"] += size
            elif outcome == "hashed":
                if (attachment.get("file") or attachment.get("sha256") or not server_hashes
                        or server_hashes["status"] != "complete"):
                    raise ValueError("Hash-only attachment claims saved bytes or incomplete coverage")
                self.media_hashed += 1
            elif outcome in ("excluded", "failed"):
                if attachment.get("file") or attachment.get("sha256"):
                    raise ValueError("Unsaved account export attachment claims saved bytes")
                self.counts["media_skipped"] += 1
                self.failed_attachments += outcome == "failed"
            else:
                raise ValueError("Invalid account export attachment outcome")

    def finish(self):
        if {name for name in self.files if name.startswith("data/")} != self.data_files:
            raise ValueError("Unreceipted account export page data")
        if {name for name in self.files if name.startswith("media/")} != self.media_files:
            raise ValueError("Unreferenced account export media")
        if self.hash_manifests:
            if self.files.get("hashes/index.jsonl") != self.hash_index.hexdigest():
                raise ValueError("File-hash index differs from signed message references")
            self.hash_manifests.add("hashes/index.jsonl")
        if {name for name in self.files if name.startswith("hashes/")} != self.hash_manifests:
            raise ValueError("Unreferenced account export file-hash manifest")
        if (account_export_integer(self.manifest["receipt_count"], "receipt count") != len(self.receipts)
                or account_export_digest(self.manifest["receipt_head_sha256"], "receipt head") != self.previous):
            raise ValueError("Account export manifest receipt boundary mismatch")
        declared_counts = self.manifest["counts"]
        if "unique_media_bytes" in declared_counts:
            self.counts["unique_media_bytes"] = sum(self.archive.getinfo(name).file_size for name in self.media_files)
        if declared_counts.get("media_hashed", 0) != self.media_hashed:
            raise ValueError("Account export hash-only attachment count mismatch")
        if any(type(declared_counts.get(name)) is not int or declared_counts[name] != count for name, count in self.counts.items()):
            raise ValueError("Account export manifest counts mismatch")
        if "messages_exported" in declared_counts and declared_counts["messages_exported"] != self.counts["messages"]:
            raise ValueError("Account export message summary mismatch")
        if "messages_seen" in declared_counts and declared_counts["messages_seen"] != self.messages_seen:
            raise ValueError("Account export seen-message summary mismatch")
        if "media_hashed" in declared_counts:
            self.counts["media_hashed"] = self.media_hashed
        gaps = None
        if "message-gaps.json" in self.files:
            computed = self.gaps.result()
            if not gaps_match(strict_json(read_member(self.archive, "message-gaps.json", MAX_JSON_BYTES)), computed,
                              self.gaps.borderline):
                raise ValueError("message-gaps.json differs from the message numbers in the signed pages")
            shared = computed["shared"]
            gaps = {"scope": computed["scope"], "lines": gap_lines(computed),
                    "shared": {key: shared[key] for key in ("messages", "absent", "runs", "proven", "below_first")},
                    "anomalies": shared["conflicts"]["count"] + shared["time_inversions"]["count"],
                    "channels_absent": sum(chat["absent"] for chat in computed["chats"])}
        done = sum(state["terminal"] and state["ok"] for state in self.tasks.values())
        failed_tasks = [name for name, state in self.tasks.items() if not state["ok"]]
        coverage = self.manifest["coverage"]
        if (type(coverage.get("inventory_complete")) is not bool
                or coverage["inventory_complete"] != self.inventory["discovery_complete"]
                or type(coverage.get("tasks_total")) is not int or coverage["tasks_total"] != len(self.tasks)
                or type(coverage.get("tasks_done")) is not int or coverage["tasks_done"] != done
                or type(coverage.get("failures")) is not int
                or coverage["failures"] != len(failed_tasks) + self.failed_attachments + len(self.inventory["gaps"])):
            raise ValueError("Account export coverage summary mismatch")
        complete = (self.inventory["discovery_complete"] and done == len(self.tasks)
                    and not self.inventory["gaps"] and not self.inventory_omissions and not self.failed_attachments and not self.failed_pages)
        if type(self.manifest.get("complete_within_scope")) is not bool or self.manifest["complete_within_scope"] != complete:
            raise ValueError("Account export completeness claim disagrees with acquisition receipts")
        if not isinstance(self.manifest.get("status"), str) or (self.manifest["status"] in ("done", "complete") and not complete):
            raise ValueError("Account export status contradicts its partial acquisition coverage")
        return {"format": self.manifest["format"], "fingerprint": self.fp, "key_pinned": bool(self.expected_fingerprint),
                "job_id": self.job_id, "account_id": self.account_id, "status": self.manifest["status"], "counts": self.counts,
                "options": self.options, "options_sha256": self.manifest["options_sha256"],
                "receipt_count": len(self.receipts), "receipt_head_sha256": self.previous, "files_checked": len(self.files),
                "sha256sums": self.sums, "producer": self.manifest.get("producer"), "coverage": {
                    "inventory_complete": self.inventory["discovery_complete"], "tasks_total": len(self.tasks), "tasks_done": done,
                    "unfinished_tasks": [name for name, state in self.tasks.items() if not state["terminal"]],
                    "failed_tasks": failed_tasks,
                    "failed_pages": self.failed_pages, "failed_attachments": self.failed_attachments,
                    "gaps": self.inventory["gaps"] + self.inventory_omissions},
                "complete_within_scope": complete, "source_completeness_established": False,
                "html_index_signed_by_manifest": "index.html" in self.files, "message_gaps": gaps,
                "meaning": "Integrity is checked relative to the signing key. Completion covers the frozen selected "
                           "tasks and their observed outcomes."}




LOSS_PREFIXES = ("connection.", "network.", "account.", "session.", "coverage.gap", "process.", "telegram.", "clock.",
                 "collector.")
LOSS_FIELDS = ("seq", "observed_at", "source_at", "kind", "chat_id", "message_id", "actor_id", "payload",
               "previous_hash")


def verify_account_loss(data, expected_fingerprint=None):
    statement = data["statement"]
    public = statement["public_key"]
    fp = fingerprint(public)
    if expected_fingerprint and fp != expected_fingerprint:
        raise ValueError("Public key differs from the independently trusted fingerprint")
    key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True))
    if not isinstance(data.get("signature"), str):
        raise ValueError("Unsigned account loss report")
    key.verify(base64.b64decode(data["signature"], validate=True), canonical(statement))
    records = statement.get("records")
    if not isinstance(records, list) or not isinstance(statement.get("loss"), dict):
        raise ValueError("Malformed account loss report")
    previous = 0
    for event in records:
        if not isinstance(event, dict) or set(event) != set(LOSS_FIELDS) | {"hash", "signature"}:
            raise ValueError("Unexpected record in the account loss report")
        if type(event["seq"]) is not int or event["seq"] <= previous:
            raise ValueError("Account loss report records are not in journal order")
        if not isinstance(event["kind"], str) or not event["kind"].startswith(LOSS_PREFIXES):
            raise ValueError("Account loss report holds a record of another kind")
        calculated = hashlib.sha256(canonical({k: event[k] for k in LOSS_FIELDS})).hexdigest()
        if event["hash"] != calculated:
            raise ValueError("Changed journal record " + str(event["seq"]) + " in the account loss report")
        if not isinstance(event["signature"], str):
            raise ValueError("Unsigned journal record " + str(event["seq"]) + " in the account loss report")
        key.verify(base64.b64decode(event["signature"], validate=True), bytes.fromhex(calculated))
        previous = event["seq"]
    loss = statement["loss"]
    return {"format": statement["format"], "fingerprint": fp, "key_pinned": bool(expected_fingerprint),
            "records": len(records), "truncated": bool(statement.get("truncated")), "window": statement.get("window"),
            "generated_at": statement.get("generated_at"), "account": statement.get("account"),
            "producer": statement.get("producer"), "loss": {key: loss.get(key) for key in ("cause", "at", "telegram_error", "dc_id")},
            "route": (loss.get("route") or {}).get("kind") if isinstance(loss.get("route"), dict) else None,
            "journal_head": statement.get("journal_head"), "meaning": statement.get("meaning")}


def verify_account_export(path, expected_fingerprint=None, max_gib=None):
    with open_archive(path, max_gib=max_gib) as archive, tempfile.TemporaryDirectory() as temporary:
        checked = AccountExportCheck(archive, expected_fingerprint)
        checked.verify_manifest()
        checked.verify_inventory()
        checked.verify_pages(temporary)
        return checked.finish()


def account_export_lines(result):
    coverage = result["coverage"]
    lines = ["Account " + str(result["account_id"]) + ": " + str(result["counts"]["messages"])
             + " message(s), " + str(result["receipt_count"]) + " signed capture receipt(s).",
             "Selected acquisition tasks finished: " + str(coverage["tasks_done"]) + " of " + str(coverage["tasks_total"]) + ".",
             "Complete within selected scope." if result["complete_within_scope"] else "Partial acquisition: selected scope is not complete.",
             result["meaning"]]
    if coverage["failed_pages"] or coverage["failed_attachments"]:
        lines.append("Failed pages: " + str(coverage["failed_pages"]) + "; failed attachments: "
                     + str(coverage["failed_attachments"]) + ".")
    lines += ["Inventory gap: " + str(gap) for gap in coverage["gaps"]]
    if result.get("message_gaps"):
        lines += ["Message numbers: " + line for line in result["message_gaps"]["lines"]]
    if result["html_index_signed_by_manifest"]:
        lines.append("The HTML index is protected by the signed archive manifest; a separate browser printout is not signed.")
    return lines


DISCLOSURE_FORMATS = ("tgwitness-account-disclosure-v1", "tgwitness-account-disclosure-v2")
WITHHELD_RULES = ("sender", "text", "period")
WITHHELD_FIELDS = {"id", "state", "rules", "count", "text", "attachments", "redacted_fields"}
REPLY_STATES = ("disclosed", "withheld", "not_in_source")


class AccountDisclosureCheck:
    def __init__(self, archive, expected_fingerprint, source, max_gib):
        self.archive = archive
        self.expected_fingerprint = expected_fingerprint
        self.source = source
        self.max_gib = max_gib

    def verify_manifest(self):
        self.manifest = read_manifest(self.archive)
        if self.manifest.get("format") not in DISCLOSURE_FORMATS:
            raise VerifierTooOld("Unsupported account disclosure format")
        self.marked = self.manifest["format"] == "tgwitness-account-disclosure-v2"
        self.public = self.manifest["public_key"]
        self.fp = fingerprint(self.public)
        if self.manifest.get("fingerprint") != self.fp:
            raise ValueError("Disclosure fingerprint does not match its signing key")
        if self.expected_fingerprint and self.fp != self.expected_fingerprint:
            raise ValueError("Public key differs from the independently trusted fingerprint")
        self.key = Ed25519PublicKey.from_public_bytes(base64.b64decode(self.public, validate=True))
        self.key.verify(base64.b64decode(read_member(self.archive, "manifest.sig"), validate=True), canonical(self.manifest))
        self.files = self.manifest["files"]
        if not isinstance(self.files, dict) or set(self.archive.namelist()) != set(self.files) | {"manifest.json", "manifest.sig"}:
            raise ValueError("Unexpected or missing disclosure archive members")
        allowed = {"messages.jsonl", "index.html", "analytics.json", "README.txt", "verify.py", "SHA256SUMS",
                   "VERIFY.cmd", "VERIFY.sh", "START_HERE.txt"}
        for name, checksum in self.files.items():
            if name not in allowed and not re.fullmatch(r"media/[0-9a-f]{64}", name):
                raise ValueError("Unexpected disclosure content: " + name)
            if not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-f]{64}", checksum):
                raise ValueError("Invalid disclosure file hash")
            if member_digest(self.archive, name) != checksum:
                raise ValueError("File hash mismatch: " + name)
        if "messages.jsonl" not in self.files or "index.html" not in self.files:
            raise ValueError("Missing authoritative disclosure messages or readable index")
        self.sums = check_sums(self.archive, self.manifest)
        for field in ("source_archive_sha256", "source_collector_fingerprint"):
            if not isinstance(self.manifest.get(field), str) or not re.fullmatch(r"[0-9a-f]{64}", self.manifest[field]):
                raise ValueError("Invalid disclosure source reference")
        if not isinstance(self.manifest.get("policy"), dict):
            raise ValueError("Disclosure must record its applied policy")

    def verify_messages(self, temporary):
        seen = sqlite3.connect(Path(temporary) / "disclosure.sqlite3")
        seen.execute("CREATE TABLE messages (chat TEXT, id TEXT, state TEXT, PRIMARY KEY(chat,id)) WITHOUT ROWID")
        seen.execute("CREATE TABLE replies (chat TEXT, id TEXT, state TEXT)")
        self.media, self.messages, self.withheld = set(), 0, 0
        try:
            with self.archive.open("messages.jsonl") as stream:
                for line in bounded_lines(stream):
                    row = strict_json(line)
                    if not isinstance(row, dict) or set(row) != {"chat", "message"}:
                        raise ValueError("Invalid disclosure message envelope")
                    chat, message = row["chat"], row["message"]
                    if not isinstance(chat, dict) or not isinstance(message, dict):
                        raise ValueError("Invalid disclosure chat/message")
                    for value in (chat.get("id"), message.get("id")):
                        if type(value) not in (str, int) or not value:
                            raise ValueError("Invalid disclosure chat/message ID")
                    state = message.get("state", "disclosed") if self.marked else "disclosed"
                    if self.marked and state not in ("disclosed", "withheld"):
                        raise ValueError("Invalid disclosure record state")
                    try:
                        seen.execute("INSERT INTO messages VALUES (?,?,?)",
                                     (canonical(chat["id"]).decode(), canonical(message["id"]).decode(), state))
                    except sqlite3.IntegrityError:
                        raise ValueError("Duplicate disclosure message") from None
                    if state == "withheld":
                        rules, count = message.get("rules"), message.get("count")
                        if (set(message) != WITHHELD_FIELDS or message.get("attachments") != []
                                or message.get("redacted_fields") != []
                                or not isinstance(rules, list) or not rules
                                or any(not isinstance(rule, str) or rule not in WITHHELD_RULES for rule in rules)
                                or rules != [rule for rule in WITHHELD_RULES if rule in rules]
                                or message.get("text") != "[withheld by selection \u2014 rule: " + ", ".join(rules) + "]"
                                or type(count) is not int or count < 1):
                            raise ValueError("Invalid withheld-by-selection marker")
                        self.withheld += count
                        continue
                    reply = message.get("reply_to") if self.marked else None
                    if reply is not None:
                        if (not isinstance(reply, dict) or set(reply) != {"id", "state"}
                                or type(reply.get("id")) not in (str, int) or not reply["id"]
                                or reply.get("state") not in REPLY_STATES):
                            raise ValueError("Invalid disclosure reply reference")
                        seen.execute("INSERT INTO replies VALUES (?,?,?)",
                                     (canonical(chat["id"]).decode(), canonical(reply["id"]).decode(), reply["state"]))
                    attachments = message.get("attachments", [])
                    if not isinstance(attachments, list):
                        raise ValueError("Invalid disclosure attachments")
                    for item in attachments:
                        if not isinstance(item, dict):
                            raise ValueError("Invalid disclosure attachment")
                        if item.get("outcome") != "saved":
                            if item.get("file") or item.get("sha256"):
                                raise ValueError("Unsaved disclosure attachment claims saved bytes")
                            continue
                        checksum = item.get("sha256")
                        if not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-f]{64}", checksum):
                            raise ValueError("Invalid disclosure media hash")
                        name = "media/" + checksum
                        size = item.get("bytes")
                        if (type(size) is not int or size < 0 or item.get("file") != name
                                or self.files.get(name) != checksum or self.archive.getinfo(name).file_size != size):
                            raise ValueError("Disclosure attachment bytes/hash mismatch")
                        self.media.add(name)
                    self.messages += 1
            self.chats = seen.execute("SELECT COUNT(DISTINCT chat) FROM messages WHERE state='disclosed'").fetchone()[0]
            dangling = seen.execute("SELECT count(*) FROM replies r LEFT JOIN messages m ON m.chat=r.chat AND m.id=r.id "
                                    "WHERE (r.state!='not_in_source' AND (m.id IS NULL OR m.state!=r.state)) "
                                    "OR (r.state='not_in_source' AND m.id IS NOT NULL)").fetchone()[0]
            if dangling:
                raise ValueError("A disclosed reply points at a record that is not in this disclosure")
        finally:
            seen.close()

    def finish(self):
        if {name for name in self.files if name.startswith("media/")} != self.media:
            raise ValueError("Unreferenced disclosure media")
        counts = {"messages": self.messages, "chats": self.chats, "media": len(self.media)}
        if self.marked:
            counts["withheld"] = self.withheld
        if (not isinstance(self.manifest.get("counts"), dict) or set(self.manifest["counts"]) != set(counts)
                or any(type(self.manifest["counts"][name]) is not int or self.manifest["counts"][name] != count
                       for name, count in counts.items())):
            raise ValueError("Disclosure manifest counts mismatch")
        source_checked = False
        if self.source is not None:
            with open(self.source, "rb") as stream:
                checksum = hashlib.file_digest(stream, "sha256").hexdigest()
            if checksum != self.manifest["source_archive_sha256"]:
                raise ValueError("Disclosure source archive hash mismatch")
            if self.fp != self.manifest["source_collector_fingerprint"]:
                raise ValueError("The disclosure is signed by a different key than its source archive")
            verify_account_export(self.source, self.manifest["source_collector_fingerprint"], max_gib=self.max_gib)
            source_checked = True
        return {"format": self.manifest["format"], "fingerprint": self.fp, "key_pinned": bool(self.expected_fingerprint),
                "disclosure_id": self.manifest.get("disclosure_id"), "created_at": self.manifest.get("created_at"),
                "counts": counts, "policy": self.manifest["policy"], "files_checked": len(self.files), "sha256sums": self.sums,
                "source_archive_sha256": self.manifest["source_archive_sha256"],
                "source_collector_fingerprint": self.manifest["source_collector_fingerprint"],
                "source_reference_checked": source_checked, "derivation_correctness_established": False,
                "html_index_signed_by_manifest": True, "producer": self.manifest.get("producer"),
                "meaning": "The signature protects this disclosure's bytes and policy statement. "
                           "Source linkage names the original archive and collector key; review filtering and redaction "
                           "against that archive."}





def verify_account_disclosure(path, expected_fingerprint=None, source=None, max_gib=None):
    with open_archive(path, max_gib=max_gib) as archive, tempfile.TemporaryDirectory() as temporary:
        checked = AccountDisclosureCheck(archive, expected_fingerprint, source, max_gib)
        checked.verify_manifest()
        checked.verify_messages(temporary)
        return checked.finish()
def bundle_format(path):
    with open_archive(path) as archive:
        return read_manifest(archive).get("format")


def bundle_hashes(path, seqs):
    wanted, found = set(seqs), {}
    if not wanted:
        return found
    with open_archive(path) as archive, archive.open("events.jsonl") as stream:
        for line in bounded_lines(stream):
            event = strict_json(line)
            if event["seq"] in wanted:
                found[event["seq"]] = event["hash"]
    return found


CAPTURE_KINDS = ("message.new", "message.edited", "message.deleted", "message.recovered",
                 "message.snapshot", "media.saved", "coverage.gap")


def verify_capture(value, checkpoint):
    statement = authenticate_statement(value)
    if not is_format(statement.get("format"), "capture-v1"):
        raise VerifierTooOld("Unsupported capture proof")
    fields = {"format", "created_at", "public_key", "event_count", "head_hash", "challenge", "counts", "last_message_at", "health"}
    if set(value) != {"statement", "signature"} or set(statement) not in (fields, fields | {"keys"}):
        raise ValueError("Unexpected capture proof fields")
    if set(checkpoint) != {"format", "created_at", "public_key", "event_count", "head_hash"}:
        raise ValueError("Unexpected checkpoint fields")
    if not is_format(statement.get("format"), "capture-v1"):
        raise ValueError("Unsupported capture proof")
    if (type(statement["event_count"]) is not int or statement["event_count"] < 0
            or not isinstance(statement["head_hash"], str) or not re.fullmatch(r"[0-9a-f]{64}", statement["head_hash"])):
        raise ValueError("Malformed capture boundary")
    for field in ("public_key", "event_count", "head_hash", "created_at"):
        if statement.get(field) != checkpoint.get(field):
            raise ValueError("Capture proof differs from checkpoint: " + field)
    Ed25519PublicKey.from_public_bytes(base64.b64decode(statement["public_key"], validate=True)).verify(
        base64.b64decode(value["signature"], validate=True), canonical(statement))
    counts = statement.get("counts")
    if not isinstance(counts, dict) or set(counts) != set(CAPTURE_KINDS):
        raise ValueError("Unexpected capture counters")
    if any(type(n) is not int or n < 0 for n in counts.values()) or sum(counts.values()) > statement["event_count"]:
        raise ValueError("Invalid capture counters")
    if statement.get("last_message_at") is not None:
        parse_time(statement["last_message_at"])
    parse_time(statement["created_at"])
    challenge = statement["challenge"]
    if challenge is not None and (not isinstance(challenge, str) or not re.fullmatch(r"[0-9a-f]{32}", challenge)):
        raise ValueError("Malformed capture challenge")
    health = statement["health"]
    if not isinstance(health, dict) or set(health) != {"running", "connected", "last_heartbeat", "media_pending", "media_failed", "backoff_until"}:
        raise ValueError("Unexpected capture health fields")
    if any(type(health[k]) is not bool for k in ("running", "connected")):
        raise ValueError("Invalid capture health flags")
    if any(type(health[k]) is not int or health[k] < 0 for k in ("media_pending", "media_failed")):
        raise ValueError("Invalid capture queue counts")
    if type(health["backoff_until"]) not in (int, float) or not 0 <= health["backoff_until"] < 1e12:
        raise ValueError("Invalid capture backoff")
    if health["last_heartbeat"] is not None:
        parse_time(health["last_heartbeat"])
    if "keys" in statement:
        keys = statement["keys"]
        if (not isinstance(keys, dict) or set(keys) != {"count", "origin", "authorized_seq"}
                or type(keys["count"]) is not int or not 0 <= keys["count"] <= statement["event_count"]
                or keys["origin"] not in ("created", "imported", "unknown")
                or (keys["count"] == 0 and (keys["authorized_seq"] is not None or keys["origin"] != "unknown"))
                or (keys["count"] > 0 and (type(keys["authorized_seq"]) is not int
                                          or not keys["count"] <= keys["authorized_seq"] <= statement["event_count"]))):
            raise ValueError("Malformed collector key history")
    return statement


def bundle_capture_prefixes(bundle_path, boundaries):
    wanted, result = set(boundaries), {}
    tree = MerkleFrontier()
    counts, last = dict.fromkeys(CAPTURE_KINDS, 0), None
    keys = {"count": 0, "origin": "unknown", "authorized_seq": None}
    if 0 in wanted:
        result[0] = {"head_hash": "0" * 64, "counts": dict(counts), "last_message_at": None,
                     "root": tree.root().hex(), "keys": dict(keys)}
    if not wanted:
        return result
    limit = max(wanted)
    with open_archive(bundle_path) as archive, archive.open("events.jsonl") as stream:
        for line in bounded_lines(stream):
            event = strict_json(line)
            if event["seq"] > limit:
                break
            tree.append(event["hash"])
            if event["kind"] == "account.authorized":
                origin = event["payload"].get("key_origin")
                keys = {"count": keys["count"] + 1, "authorized_seq": event["seq"],
                        "origin": origin if origin in ("created", "imported") else "unknown"}
            if event["kind"] in counts:
                counts[event["kind"]] += 1
                if event["kind"].startswith("message."):
                    last = max(last or event["observed_at"], event["observed_at"])
            if event["seq"] in wanted:
                result[event["seq"]] = {"head_hash": event["hash"], "counts": dict(counts), "last_message_at": last,
                                        "root": tree.root().hex(), "keys": dict(keys)}
    return result


def check_capture_prefix(value, bundle_path):
    statement = value["statement"]
    prefix = bundle_capture_prefixes(bundle_path, [statement["event_count"]]).get(statement["event_count"])
    if prefix is None or prefix["head_hash"] != statement["head_hash"]:
        raise ValueError("Capture proof head is absent from the evidence")
    if prefix["counts"] != statement["counts"] or prefix["last_message_at"] != statement.get("last_message_at"):
        raise ValueError("Capture counters differ from the evidence records")
    if "keys" in statement and prefix["keys"] != statement["keys"]:
        raise ValueError("Capture key history differs from the evidence records")
    return prefix["counts"]


WITNESS_TOKEN = re.compile(r"TGW1\.([A-Za-z0-9_-]{20,})\.([A-Za-z0-9_-]{40,})")
CHANNEL_POST = re.compile(r'[^"/]+/(\d+)"')
CHANNEL_TEXT = re.compile(r'class="tgme_widget_message_text js-message_text"[^>]*>(.*?)</div>', re.S)
CHANNEL_META = re.compile(r'class="tgme_widget_message_meta"[^>]*>(.*?)</time>', re.S)
CHANNEL_TIME = re.compile(r'<time datetime="([^"]+)"')
TELEGRAM_PAGES = ("t.me", "telegram.me")


def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def unb64url(text):
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


class DailyJournal:
    def __init__(self):
        self.tree, self.dates = MerkleFrontier(), {}
        self.previous, self.last_date, self.latest = None, None, None

    def payload(self, date):
        if not isinstance(date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            raise ValueError("Invalid daily seal date")
        datetime.strptime(date, "%Y-%m-%d")
        if self.last_date is not None and date <= self.last_date:
            raise ValueError("Repeated or reversed daily seal")
        before = max((v for k, v in self.dates.items() if k <= date), key=lambda v: v["to_seq"], default=None)
        boundary = before or {"to_seq": 0, "head_hash": "0" * 64, "root": MERKLE_EMPTY.hex()}
        day = self.dates.get(date, {})
        return {"date": date, "from_seq": day.get("from_seq", boundary["to_seq"] + 1),
                **{k: boundary[k] for k in ("to_seq", "head_hash", "root")},
                "checks": dict(day.get("checks", {"no_response": 0})),
                "previous_daily_sha256": self.previous, "drand_round": day.get("drand_round")}

    def add(self, event):
        moment = parse_time(event["observed_at"])
        if moment.tzinfo is None:
            raise ValueError("Witness date has no time zone")
        self.latest = moment if self.latest is None else max(moment, self.latest)
        date = moment.astimezone(timezone.utc).date().isoformat()
        if self.last_date is not None and date <= self.last_date:
            date = self.latest.astimezone(timezone.utc).date().isoformat()
        self.tree.append(event["hash"])
        day = self.dates.setdefault(date, {"from_seq": event["seq"], "checks": {"no_response": 0}})
        day.update(to_seq=event["seq"], head_hash=event["hash"], root=self.tree.root().hex())
        kind, payload = event["kind"], event["payload"]
        if kind in ("witness.anchor", "witness.no_response"):
            status = payload.get("status", "invalid") if kind == "witness.anchor" else "no_response"
            if status not in ("ok", "invalid", "key_changed", "rollback", "fork", "no_response"):
                raise ValueError("Unknown witness check status")
            day["checks"][status] = day["checks"].get(status, 0) + 1
            if payload.get("freshness"):
                day["drand_round"] = payload["freshness"]["drand_round"]
        elif kind == "witness.daily":
            if payload["date"] >= date:
                raise ValueError("Witness sealed an unfinished UTC day")
            self.previous = hashlib.sha256(canonical(event)).hexdigest()
            self.last_date = payload["date"]


def daily_payload(events, date):
    journal = DailyJournal()
    for event in events:
        journal.add(event)
    return journal.payload(date)


def witness_challenge(freshness):
    if not isinstance(freshness, dict):
        raise ValueError("Invalid witness freshness")
    beacon = drand_beacon({"round": freshness.get("drand_round"),
                          "randomness": freshness.get("drand_randomness"),
                          "signature": freshness.get("drand_signature")})
    nonce = freshness.get("nonce")
    if not isinstance(nonce, str) or not re.fullmatch(r"[0-9a-f]{32}", nonce):
        raise ValueError("Invalid witness freshness nonce")
    return hashlib.sha256(bytes.fromhex(beacon["signature"]) + bytes.fromhex(nonce)).hexdigest()[:32]


def post_statement(event, witness_fingerprint):
    payload = event["payload"]
    statement = {"format": "tgwitness-witness-post-v1", "witness": witness_fingerprint, "seq": event["seq"],
            "at": event["observed_at"], "record_hash": event["hash"],
            "status": payload.get("status") or ("no_response" if event["kind"] == "witness.no_response" else None),
            "collector": payload.get("collector_fingerprint"), "events": payload.get("event_count"),
            "head": payload.get("head_hash")}
    if payload.get("capture"):
        statement.update(capture_sha256=hashlib.sha256(canonical(payload["capture"])).hexdigest(),
                         counts=payload["capture"]["statement"]["counts"], delta=payload.get("capture_delta"))
    if payload.get("freshness") is not None:
        statement["drand_round"] = payload["freshness"]["drand_round"]
    if event["kind"] == "witness.daily":
        statement.update(kind="witness.daily", date=payload["date"], root=payload["root"],
                         drand_round=payload.get("drand_round"), previous_daily_sha256=payload["previous_daily_sha256"])
    return statement


def post_token(statement, signature_b64):
    return "TGW1." + b64url(canonical(statement)) + "." + b64url(base64.b64decode(signature_b64))


def verify_witness(path, expected_fingerprint=None, check_drand=False, check_bitcoin=False):
    with open_archive(path) as archive:
        names = archive.namelist()
        manifest = read_manifest(archive)
        if not is_format(manifest["format"], "witness-v1"):
            raise VerifierTooOld("Unsupported witness format")
        public = manifest["public_key"]
        fp = fingerprint(public)
        if expected_fingerprint and fp != expected_fingerprint:
            raise ValueError("Witness key differs from the independently trusted witness fingerprint")
        Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True)).verify(
            base64.b64decode(read_member(archive, "manifest.sig"), validate=True), canonical(manifest))
        if set(names) != set(manifest["files"]) | {"manifest.json", "manifest.sig"}:
            raise ValueError("Unexpected or missing witness bundle members")
        for name, digest in manifest["files"].items():
            if member_digest(archive, name) != digest:
                raise ValueError("File hash mismatch: " + name)
        anchors, silent, posted, failures, statements, interval = [], [], {}, [], {}, None
        retained, collector_keys = {}, {}
        journal, days, seals = DailyJournal(), [], {}

        def observed(stream):
            nonlocal interval
            for line in bounded_lines(stream):
                if not line.strip():
                    continue
                event = json.loads(line)
                yield event
                payload, kind = event["payload"], event["kind"]
                if kind == "witness.daily":
                    expected = journal.payload(payload.get("date"))
                    if canonical(payload) != canonical(expected):
                        raise ValueError("Witness daily root, counts, range or previous seal differs from the journal")
                    checks = payload["checks"]
                    status = "fail" if any(v for k, v in checks.items() if k not in ("ok", "no_response")) else \
                        "ok" if checks.get("ok") else "no_response_only"
                    day = {**payload, "seq": event["seq"], "status": status, "bitcoin": "none", "proofs": []}
                    seals[event["seq"]] = event
                    days.append(day)
                    statements[event["seq"]] = post_statement(event, fp)
                elif kind == "witness.anchored":
                    if payload.get("record") not in seals or not isinstance(payload.get("results"), list):
                        raise ValueError("Witness timestamp record has no preceding daily seal")
                journal.add(event)
                if kind == "witness.started":
                    interval = payload.get("interval_minutes")
                elif kind == "witness.anchor":
                    anchors.append({"seq": event["seq"], "at": event["observed_at"], "status": payload.get("status"),
                                    "collector_fingerprint": payload.get("collector_fingerprint"),
                                    "event_count": payload.get("event_count"), "head_hash": payload.get("head_hash")})
                    if payload.get("capture"):
                        captured = verify_capture(payload["capture"], payload["checkpoint"]["statement"])
                        if (fingerprint(captured["public_key"]) != payload["collector_fingerprint"]
                                or captured["event_count"] != payload["event_count"]
                                or captured["head_hash"] != payload["head_hash"]):
                            raise ValueError("Witness capture proof differs from its anchor")
                        anchors[-1]["capture"] = payload["capture"]
                        if captured.get("keys") is not None:
                            if payload.get("keys") != captured["keys"]:
                                raise ValueError("Witness key history differs from its signed capture")
                            anchors[-1]["keys"] = captured["keys"]
                            collector_keys[payload["collector_fingerprint"]] = key_history_summary(captured["keys"])
                    if "keys" in payload and not payload.get("capture"):
                        raise ValueError("Witness key history has no signed capture")
                    if payload.get("freshness") is not None:
                        fresh = payload["freshness"]
                        challenge = witness_challenge(fresh)
                        if not payload.get("capture") or captured.get("challenge") != challenge:
                            raise ValueError("Witness freshness challenge differs from the signed capture")
                        anchors[-1]["freshness"] = {**fresh, "verified": False, "not_before": None}
                    collector_key = payload.get("collector_fingerprint")
                    changed = payload.get("status") == "key_changed" and "previous_keys" in payload
                    if payload.get("status") == "ok" or changed:
                        prior = retained.get(collector_key)
                        if changed and (not prior or prior.get("keys") is None or prior["keys"] != payload["previous_keys"]
                                        or anchors[-1].get("keys") in (None, prior["keys"])
                                        or payload.get("pinned_fingerprint") != collector_key):
                            raise ValueError("Witness recorded a collector key change that differs from its key history")
                        if not changed and prior and prior.get("keys") is not None and prior["keys"] != anchors[-1].get("keys"):
                            raise ValueError("Witness accepted a changed or removed collector key history")
                        if changed:
                            anchors[-1]["previous_keys"] = payload["previous_keys"]
                        if payload.get("continuity") is not None:
                            if not payload.get("capture"):
                                raise ValueError("Continuity proof has no matching capture proof")
                            committed = verify_continuity(payload["continuity"], payload["checkpoint"]["statement"],
                                                          prior, captured["challenge"])
                            anchors[-1]["continuity"] = payload["continuity"]
                            anchors[-1]["root"] = committed["root"]
                        elif prior and prior.get("root"):
                            raise ValueError("Witness accepted a continuity downgrade")
                        retained[collector_key] = {k: anchors[-1][k] for k in ("event_count", "head_hash", "root", "keys")
                                                  if k in anchors[-1]}
                    statements[event["seq"]] = post_statement(event, fp)
                elif kind == "witness.no_response":
                    silent.append({"seq": event["seq"], "at": event["observed_at"], "error": payload.get("error")})
                    statements[event["seq"]] = post_statement(event, fp)
                elif kind == "witness.posted":
                    posted[payload.get("record")] = payload.get("message_id")
                elif kind == "witness.post_failed":
                    failures.append({"record": payload.get("record"), "error": payload.get("error")})
        with archive.open("events.jsonl") as stream:
            result = verify_events(observed(stream), public)
        proof_files = set()
        for day in days:
            event = seals[day["seq"]]
            digest = hashlib.sha256(canonical(event)).digest()
            stem = "anchors/daily-" + day["date"]
            if stem + ".json" in names:
                proof_files.add(stem + ".json")
                if read_member(archive, stem + ".json") != canonical(event):
                    raise ValueError("Retained witness daily seal differs from its journal record")
            for name in sorted(n for n in names if n.startswith(stem + ".") and n.endswith(".ots")):
                proof_files.add(name)
                proof = read_member(archive, name)
                summary = ots_summary(proof, digest)
                if check_bitcoin:
                    summary = confirm_ots(proof, digest)
                day["proofs"].append({"file": name, **summary})
            if any(p["status"] == "confirmed" for p in day["proofs"]):
                day["bitcoin"] = "confirmed"
                day["bitcoin_block_time"] = min(p["time"] for p in day["proofs"] if p["status"] == "confirmed")
            elif day["proofs"]:
                day["bitcoin"] = "pending"
        if any(n.startswith("anchors/") and n not in proof_files for n in names):
            raise ValueError("Witness timestamp file has no matching daily seal")
        missing_days = []
        if days:
            first, last = (datetime.strptime(d["date"], "%Y-%m-%d").date() for d in (days[0], days[-1]))
            if (last - first).days > 36600:
                raise ValueError("Witness daily range exceeds 100 years")
            dates = {d["date"] for d in days}
            missing_days = [(first + timedelta(days=i)).isoformat() for i in range((last - first).days + 1)
                            if (first + timedelta(days=i)).isoformat() not in dates]
    if result["events"] != manifest["event_count"] or result["head_hash"] != manifest["head_hash"]:
        raise ValueError("Witness manifest does not match its journal")
    bound = [a for a in anchors if a.get("freshness")]
    confirmation = {"asked": 0, "confirmed": 0, "relays": []}
    if check_drand and bound:
        rounds = [{"round": a["freshness"]["drand_round"], "randomness": a["freshness"]["drand_randomness"],
                   "seq": a["seq"]} for a in bound]
        confirmation = confirm_drand(rounds, limit=len(rounds))
        if confirmation["confirmed"] == len(rounds):
            for anchor in bound:
                anchor["freshness"].update(verified=True, not_before=drand_time(anchor["freshness"]["drand_round"]))
    freshness = {"anchors": len(anchors), "drand_bound": len(bound), "confirmed": confirmation["confirmed"],
                 "earliest_not_before": min((a["freshness"]["not_before"] for a in bound
                                              if a["freshness"]["verified"]), default=None),
                 "verification": "relay-confirmed" if confirmation["confirmed"] else "not-performed",
                 "relays": confirmation["relays"], "unavailable": bool(confirmation.get("unavailable"))}
    return {"format": manifest["format"], "fingerprint": fp, "public_key": public, "events": result["events"],
            "head_hash": result["head_hash"], "interval_minutes": interval, "channel": manifest.get("channel"),
            "producer": manifest.get("producer"), "anchors": anchors, "no_response": silent, "posted": posted,
            "post_failures": failures, "statements": statements, "key_pinned": bool(expected_fingerprint),
            "freshness": freshness, "days": days, "missing_days": missing_days, "collector_keys": collector_keys,
            **({"chronology": result["chronology"]} if "chronology" in result else {})}


def key_history_summary(keys):
    return {**keys, "meaning": "Telegram authorizations of the account as the collector recorded them",
            "note": "Imported session: the acquisition starts from an authorization created outside this collector"
            if keys["origin"] == "imported" else None}


def witnessed_periods(witness, key=None):
    limit = (witness.get("interval_minutes") or 10) * 60 * 2.5
    timeline = sorted([(a["at"], a["status"] == "ok" and key in (None, a["collector_fingerprint"]))
                       for a in witness["anchors"]]
                      + [(s["at"], False) for s in witness["no_response"]])
    periods, gaps, start, previous = [], [], None, None
    for at, ok in timeline:
        if ok and start is not None and (parse_time(at) - parse_time(previous)).total_seconds() > limit:
            periods.append({"from": start, "to": previous})
            gaps.append({"from": previous, "to": at, "reason": "no witness record (witness offline)"})
            start = None
        if ok:
            start, previous = start or at, at
        else:
            if start is not None:
                periods.append({"from": start, "to": previous})
                start = None
            gaps.append({"from": at, "to": at, "reason": "the collector did not answer or answered inconsistently"})
    if start is not None:
        periods.append({"from": start, "to": previous})
    return periods, gaps


def witness_moment(value):
    parsed = parse_time(value)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def cross_check_witness(witness, bundle_path, bundle_result):
    count, key = bundle_result["events"], bundle_result["fingerprint"]
    mine = [a for a in witness["anchors"] if a["collector_fingerprint"] == key]
    explained = {a["seq"] for a in witness["anchors"] if a["status"] == "key_changed" and a.get("previous_keys")}
    comparable = {a["seq"] for a in mine if a["status"] == "ok" or a["seq"] in explained}
    hashes = bundle_hashes(bundle_path, {a["event_count"] for a in mine
                                         if a["seq"] in comparable and 0 < (a["event_count"] or 0) <= count})
    prefixes = bundle_capture_prefixes(bundle_path, {a["event_count"] for a in mine
                                                    if a.get("capture") and a["seq"] in comparable
                                                    and a["event_count"] <= count})
    with open_archive(bundle_path) as archive:
        manifest = read_manifest(archive)
    created = manifest.get("snapshot_at") if isinstance(manifest.get("snapshot_at"), str) else manifest.get("created_at")
    created_at = witness_moment(created) if isinstance(created, str) else None
    consistent, conflicts, later, anomalies, matched, beyond = 0, [], 0, [], [], []
    for anchor in mine:
        if (anchor["event_count"] or 0) > count:
            beyond.append(anchor)
            if created_at and witness_moment(anchor["at"]) < created_at:
                conflicts.append(anchor)
            else:
                later += 1
        elif anchor["status"] != "ok" and anchor["seq"] not in explained:
            anomalies.append(anchor)
        elif ("0" * 64 if anchor["event_count"] == 0 else hashes.get(anchor["event_count"])) == anchor["head_hash"]:
            capture = anchor.get("capture", {}).get("statement")
            prefix = prefixes.get(anchor["event_count"])
            if (capture and (not prefix or any(prefix[k] != capture[k] for k in ("counts", "last_message_at"))
                             or "keys" in capture and prefix["keys"] != capture["keys"])
                    or anchor.get("root") and (not prefix or prefix["root"] != anchor["root"])):
                conflicts.append(anchor)
            else:
                consistent += 1
                matched.append(anchor)
        else:
            conflicts.append(anchor)


    matching_sequences = {a["seq"] for a in matched}
    timeline = []
    for anchor in witness["anchors"]:
        if anchor["collector_fingerprint"] == key and anchor["status"] == "ok":
            if anchor["event_count"] > count:
                continue
            if anchor["seq"] not in matching_sequences:
                anchor = {**anchor, "status": "conflict"}
        timeline.append(anchor)
    periods, gaps = witnessed_periods({**witness, "anchors": timeline}, key)
    verified_through = max((a["event_count"] for a in matched), default=0)
    continuity_through = max((a["event_count"] for a in matched if a.get("root")), default=0)
    invalid = sum(1 for a in witness["anchors"] if a["status"] == "invalid")
    exact = [a for a in matched if a["event_count"] == count]
    fresh = [a for a in exact if a.get("freshness", {}).get("verified")]
    sealed_days = [d for d in witness.get("days", []) if d["bitcoin"] == "confirmed"
                   and any(a["seq"] <= d["to_seq"] for a in exact)]
    late = {a["seq"] for a in beyond if a["status"] != "ok"}
    problems = sorted(a["seq"] for a in witness["anchors"]
                      if a["status"] != "ok" and a["seq"] not in late and a["seq"] not in explained)
    days = []
    for day in witness.get("days", []):
        index = bisect.bisect_left(problems, day["from_seq"])
        if (late or explained) and day["status"] == "fail" and (index == len(problems) or problems[index] > day["to_seq"]):
            day = {**day, "status": "ok" if day["checks"].get("ok") else "no_response_only"}
        days.append(day)
    highest = max((a["event_count"] for a in beyond), default=None)
    return {"witness_fingerprint": witness["fingerprint"], "anchors_for_this_key": len(mine),
            "other_keys": len(witness["anchors"]) - len(mine) - invalid, "invalid_answers": invalid,
            "consistent": consistent, "conflicts": conflicts, "export_created_at": created,
            "after_export": later, "anomalies": anomalies, "no_response": len(witness["no_response"]),
            "seen_after_export": {"event_count": highest, "at": next(a["at"] for a in beyond if a["event_count"] == highest)}
            if beyond else None,
            "witnessed": periods, "witness_gaps": gaps,
            "verified_through_event": verified_through, "unwitnessed_events": count - verified_through,
            "continuity_verified_through_event": continuity_through,
            "export_head_witnessed": any(a["event_count"] == count for a in matched),
            "export_head_witness_records": [a["seq"] for a in matched if a["event_count"] == count],
            "witness_key_pinned": bool(witness.get("key_pinned")),
            "collector_keys": witness.get("collector_keys", {}).get(key),
            "days": days, "missing_days": witness.get("missing_days", []),
            "head_not_before": min((a["freshness"]["not_before"] for a in fresh), default=None),
            "head_bitcoin_block_time": min((d["bitcoin_block_time"] for d in sealed_days), default=None),
            "head_witnessed_at": min((a["at"] for a in exact), default=None),
            "head_witness_record": min((a["seq"] for a in exact), default=None)}


ASSURANCE_TIERS = ("self_attested", "timestamped", "witnessed", "fresh", "witness_anchored", "sealed")
EVIDENCE_PROFILES = ("integrity", "evidence", "attested")
CONDITION_LABELS = {"integrity": "Integrity", "signer": "Signer key", "external_time": "External time",
                    "head_binding": "Witness with its own key", "checkpoint": "Retained checkpoint",
                    "environment": "Attested collection run"}
CONDITION_ROLE = {"integrity": "required", "signer": "required", "external_time": "required",
                  "head_binding": "supporting", "checkpoint": "supporting", "environment": "supporting"}
ROLE_LABELS = {"required": "Required conditions", "supporting": "Supporting records, not part of the minimum"}
CONDITION_SCOPE = {"integrity": "The archive is unchanged since the collector signed it.",
                   "signer": "The signing key is the collector key the recipient retained.",
                   "external_time": "A third party confirms that the covered records existed by the stated time.",
                   "head_binding": "A second key retained the journal head. Who holds that key is shown by the custodian's key-control record, kept with its fingerprint.",
                   "checkpoint": "Records up to the checkpoint match a journal state signed with the collector key. "
                                 "They are bound only if the recipient obtained it before this archive, through another channel.",
                   "environment": "The signing key was created inside the attested collection run."}
MINIMUM_NAMES = {"signer": "confirmed signer key", "external_time": "external time from a third party covering the last record"}


def assurance(result):
    witness = result.get("witness") or {}
    anchors = result.get("anchors") or []
    stamps = [a for a in anchors if a.get("event_count") == result.get("events") and (
        a.get("kind") == "rfc3161" and a.get("signature", "").startswith("checked against") or
        a.get("kind") == "opentimestamps" and a.get("status") == "confirmed")]
    times = [a["time"] for a in stamps]
    times += [witness[name] for name in ("head_bitcoin_block_time", "head_telegram_post_time") if witness.get(name)]
    independent = bool(witness.get("witness_key_pinned") and witness.get("export_head_witnessed")
                       and witness.get("witness_fingerprint") != result.get("fingerprint"))
    days = witness.get("days", result.get("days", []))
    missing = witness.get("missing_days", result.get("missing_days", []))
    bad_witness = bool(witness.get("conflicts") or witness.get("anomalies") or any(d["status"] == "fail" for d in days))
    complete_days = bool(days and not missing and all(d["bitcoin"] == "confirmed" for d in days)
                         and witness.get("head_bitcoin_block_time"))
    runtime = result.get("runtime_attestation") or {}
    tdx = tdx_condition(result["tdx"]) if result.get("tdx") else None
    ladder = [
        {"tier": "self_attested", "status": "pass", "detail": "signature, hashes and applicable chain/manifest checks"},
        {"tier": "timestamped", "status": "pass" if times else "absent",
         "detail": ("external timestamp covering the export head: " + min(times)
                    + "; Bitcoin dates are block-header times; TSA dates depend on the trusted authority")
                   if times else "no authenticated external time covering the export head"},
        {"tier": "witnessed", "status": "fail" if bad_witness else "pass" if independent else "absent",
         "detail": ("witness " + str(witness.get("witness_fingerprint")) + "; records 1.." + str(result.get("events"))
                    + "; witness clock " + str(witness.get("head_witnessed_at"))) if independent else "no pinned witness with its own key at the export head"},
        {"tier": "fresh", "status": "pass" if independent and witness.get("head_not_before") else "absent",
         "detail": "relay-confirmed drand challenge; not before " + str(witness.get("head_not_before"))
                   if witness.get("head_not_before") else "no independently checked drand binding for the export head"},
        {"tier": "witness_anchored", "status": "fail" if bad_witness else "pass" if independent and complete_days else "absent",
         "detail": "Bitcoin-confirmed daily seals: " + str(sum(d["bitcoin"] == "confirmed" for d in days))
                   + "; missing days: " + str(len(missing))},
        {"tier": "sealed", "status": "pass" if runtime.get("verified") is True and runtime.get("key_origin") == "created" else "absent",
         "detail": runtime.get("limitation") or (english(tdx[1], **tdx[2]) if tdx else
                                                 "no independently checked runtime attestation bound to this export and a created key")},
    ]
    tier = "self_attested"
    for row in ladder:
        if row["status"] != "pass":
            break
        tier = row["tier"]
    return {"tier": tier, "ladder": ladder, "scope": "complete exported head; coverage reports observation continuity"}


def assurance_line(result):
    value = result["assurance"]
    if value["tier"] == "self_attested":
        return "ASSURANCE: self_attested · signatures, hashes and record chain"
    witness = result.get("witness") or {}
    detail = (" since #" + str(witness["head_witness_record"]) + " (" + str(witness["head_witnessed_at"]) + ")"
              if witness.get("head_witness_record") else "")
    absent = {row["tier"] for row in value["ladder"] if row["status"] != "pass"}
    limits = [text for tier, text in (("fresh", "not fresh"), ("witness_anchored", "witness not anchored"),
                                    ("sealed", "not sealed")) if tier in absent]
    return "ASSURANCE: " + value["tier"] + detail + (" · " + " · ".join(limits) if limits else "")


def forgery_lines(result):
    lines, anchors = [], result.get("anchors") or []
    tsa = [a for a in anchors if a.get("kind") == "rfc3161" and a.get("time")
           and str(a.get("signature", "")).startswith("checked against")]
    if tsa:
        top = max(a["event_count"] for a in tsa)
        names = sorted({(a.get("qualified") or {}).get("service") or str(a.get("service")) for a in tsa if a["event_count"] == top})
        lines.append("Records 1-" + str(top) + " existed by " + min(a["time"] for a in tsa if a["event_count"] == top)
                     + ": changing them needs a new time stamp signed by " + ", ".join(names) + ".")
    ots = [a for a in anchors if a.get("kind") == "opentimestamps" and a.get("status") == "confirmed" and a.get("blocks")]
    if ots:
        top = max(a["event_count"] for a in ots)
        block = min((b for a in ots if a["event_count"] == top for b in a["blocks"]), key=lambda b: b["height"])
        lines.append("Records 1-" + str(top) + " are committed in Bitcoin block " + str(block["height"]) + " ("
                     + str(block["time"]) + "): changing them means rewriting Bitcoin from that block.")
    ladder = {row["tier"]: row for row in (result.get("assurance") or {}).get("ladder", [])}
    if ladder.get("witnessed", {}).get("status") == "pass":
        lines.append("A separate witness key retained the head (" + ladder["witnessed"]["detail"]
                     + "): changing those records also needs that key.")
    if ladder.get("sealed", {}).get("status") == "pass":
        lines.append("The collector key was created inside an attested Intel TDX VM: signing elsewhere needs a break of Intel TDX.")
    if not lines:
        lines.append("No external time was checked in this run: use --tsa-ca or --check-bitcoin for the archive's "
                     "timestamps, or add a witness.")
    cp = result.get("checkpoint_drand_anchor") or {}
    if isinstance(cp.get("round"), int):
        lines.append("The checkpoint at record " + str(result.get("checkpoint_event_count")) + " was signed no earlier than "
                     + drand_time(cp["round"]) + " (drand round " + str(cp["round"]) + ", "
                     + ("confirmed by relays" if cp.get("confirmed_by_relays") else "run with --check-drand to confirm") + ").")
    return ["Any change to a record breaks the hash chain and the Ed25519 signatures."] + lines


def english(text, **values):
    for name, value in values.items():
        text = text.replace("{" + name + "}", str(value))
    return text


def tdx_condition(tdx):
    failed = next((q for q in tdx["quotes"] if q["status"] != "pass"), None)
    if failed:
        return "missing", "Intel TDX check failed: {detail}", {"detail": (
            "record " + str(failed["record"]) + ": " if "record" in failed else "") + failed["detail"]
            + (" (" + failed["error"] + ")" if failed.get("error") else "")}
    return ("partial", "{count} Intel TDX quote(s) verified offline and bound to the collector key; the code the VM ran "
                       "is not checked here", {"count": len(tdx["quotes"])})


def condition(cid, status, how, text, **values):
    return {"id": cid, "role": CONDITION_ROLE[cid], "status": status, "scope": CONDITION_SCOPE[cid], "how": how,
            "detail": english(text, **values), "text": text, "values": values}


def evidence_conditions(result, kind="evidence"):
    events, fp = result.get("events"), result.get("fingerprint") or ""
    witness, anchors = result.get("witness") or {}, result.get("anchors") or []
    journal = kind == "evidence"
    integrity = (("{records} records, {files} files", {"records": events, "files": result.get("files_checked")})
                 if events is not None and result.get("files_checked") is not None else ("signature and content hashes", {}))
    rows = [condition("integrity", "met", "record signatures, hash chain, manifest and file hashes", integrity[0], **integrity[1]),
            condition("signer", "met" if result.get("key_pinned") else "missing",
                      "--fingerprint with the collector fingerprint the recipient retained",
                      "collector {fingerprint}… matches the fingerprint you supplied" if result.get("key_pinned")
                      else "collector {fingerprint}… not compared with a retained fingerprint", fingerprint=fp[:16])]
    checked = [a for a in anchors if a.get("kind") == "rfc3161" and str(a.get("signature", "")).startswith("checked against")
               or a.get("kind") == "opentimestamps" and a.get("status") == "confirmed"]
    times = [a["time"] for a in checked if a.get("event_count") == events and a.get("time")]
    if witness.get("export_head_witnessed") and not witness.get("conflicts"):
        times += [witness[name] for name in ("head_bitcoin_block_time", "head_telegram_post_time") if witness.get(name)]
    runtime = result.get("runtime_attestation") or {}
    attested = runtime.get("verified") is True and runtime.get("key_origin") == "created"
    if attested and runtime.get("attested_at"):
        times.append(runtime["attested_at"])
    unchecked = [a for a in anchors if a not in checked]
    stamped = max((a.get("event_count") or 0 for a in checked), default=0)
    qualified = next((a["qualified"] for a in checked if a.get("event_count") == events and a.get("qualified")), None)
    if times and qualified:
        status, text, values = ("met", "last exported record existed by {time}; qualified eIDAS time stamp from {service}",
                                {"time": min(times), "service": qualified["service"]})
    elif times:
        status, text, values = "met", "last exported record existed by {time}", {"time": min(times)}
    elif checked:
        status, text, values = "partial", "records 1–{through} existed by {time}", {
            "through": stamped, "time": min(a.get("time") or "?" for a in checked if (a.get("event_count") or 0) == stamped)}
    elif unchecked:
        status, text, values = ("unchecked", "{count} timestamp proof(s) present; check them with --tsa-ca or --check-bitcoin",
                                {"count": len(unchecked)})
    else:
        status, text, values = "missing", "no external timestamp in this archive", {}
    rows.append(condition("external_time", status,
                          "RFC 3161 with --tsa-ca, OpenTimestamps with --check-bitcoin, a witness post read from t.me with --channel, "
                          "witness Bitcoin seals or a checked GitHub attestation"
                          if journal else "in the evidence journal ZIP: --tsa-ca or --check-bitcoin", text, **values))
    drand = ((result.get("outside") or {}).get("drand") or {}).get("checked") or {}
    if drand.get("confirmed"):
        rows[-1]["drand"] = ", ".join(drand.get("relays") or [])
        rows[-1]["detail"] += " · drand rounds confirmed by " + rows[-1]["drand"]
    own_key = bool(witness.get("witness_key_pinned") and witness.get("witness_fingerprint") not in (None, fp)
                   and not witness.get("conflicts"))
    through = (witness.get("verified_through_event") or 0) if own_key else 0
    if journal and through:
        text, values = "records 1–{through} of {total} retained by a witness with its own key", {"through": through, "total": events}
    elif journal:
        text, values = "no witness with its own key", {}
    else:
        text, values = "this archive type carries no journal checkpoints; verify the evidence journal", {}
    rows.append(condition("head_binding", "met" if journal and own_key and witness.get("export_head_witnessed")
                          else "partial" if journal and through else "missing",
                          "--witness with --witness-fingerprint of a key other than the collector key" if journal
                          else "in the evidence journal ZIP: --witness with --witness-fingerprint", text, **values))
    if journal:
        retained = result.get("checkpoint_event_count")
        rows.append(condition("checkpoint", "met" if retained and retained == events else "partial" if retained else "missing",
                              "--checkpoint received before this archive, through another channel",
                              "records 1–{through} of {total} match the checkpoint you supplied" if retained
                              else "no checkpoint supplied", **({"through": retained, "total": events} if retained else {})))
    if result.get("tdx") and not attested:
        status, text, values = tdx_condition(result["tdx"])
        rows.append(condition("environment", status, "compose and OS image: python -m tgwitness.cloud verify", text, **values))
    else:
        rows.append(condition("environment", "met" if attested else "missing",
                              "--sealed-attestation with --sealed-policy for a GitHub Actions run; Intel TDX: python -m tgwitness.cloud verify"
                              if journal else "in the evidence journal ZIP: --sealed-attestation with --sealed-policy",
                              "collection ran in the attested workflow {workflow}" if attested
                              else "no attested collection run checked here",
                              **({"workflow": runtime.get("workflow")} if attested else {})))
    met = {row["id"] for row in rows if row["status"] == "met"}
    missing = [item for item in ("signer", "external_time") if item not in met]
    minimum = not missing
    bound = events if minimum else stamped
    options = [] if "signer" in met else ["--fingerprint FINGERPRINT"]
    if journal and "external_time" in missing:
        options += sorted({"--tsa-ca TSA-ROOT.pem" if a.get("kind") == "rfc3161" else "--check-bitcoin" for a in unchecked
                           if a.get("event_count") == events and (a.get("kind") == "rfc3161" or a.get("status") == "bitcoin-unverified")}) \
            or ["--witness WITNESS.zip", "--channel https://t.me/s/WITNESS_CHANNEL"]
    return {"profile": "attested" if minimum and "environment" in met else "evidence" if minimum else "integrity",
            "minimum_met": minimum, "missing": missing, "records": events,
            "bound_through": bound if "signer" in met else 0, "conditions": rows,
            "next_options": options, "journal_needed": not journal and "external_time" in missing,
            "minimum": "integrity, confirmed signer key, and external time from a third party covering the last exported "
                       "record: RFC 3161, Bitcoin, a witness post read from t.me or an attested collection run"}


def next_lines(evidence, t=None):
    t = t or english
    lines = [t("Next step: run verify.py again with {options}", options=" ".join(evidence["next_options"]))] \
        if evidence.get("next_options") else []
    if evidence.get("journal_needed"):
        lines.append(t("This archive type carries no checkpoints or timestamps: the last record is bound in the evidence "
                       "journal of the same workspace. Verify that ZIP with --fingerprint and --tsa-ca, --check-bitcoin "
                       "or --witness with --channel."))
    return lines


def evidence_line(evidence, t=None):
    t = t or english
    if evidence["minimum_met"]:
        return t("EVIDENCE: minimum met · profile {profile}", profile=evidence["profile"])
    if evidence.get("bound_through"):
        return t("EVIDENCE: minimum met up to record {through} of {total} · later records need a binding",
                 through=evidence["bound_through"], total=evidence.get("records"))
    return t("EVIDENCE: minimum not met · missing: {items}",
             items="; ".join(t(MINIMUM_NAMES.get(item, item)) for item in evidence["missing"]))


def requested_checks_unavailable(args, result):
    missing = []
    witness = result.get("witness") or {}
    if getattr(args, "check_drand", False):
        drand = ((result.get("outside") or {}).get("drand") or {}).get("checked") or {}
        if drand.get("unavailable") or (result.get("freshness") or {}).get("unavailable") \
                or (witness.get("freshness") or {}).get("unavailable"):
            missing.append("--check-drand: no drand relay answered")
    if getattr(args, "check_bitcoin", False):
        proofs = [a for a in result.get("anchors") or [] if a.get("kind") == "opentimestamps"]
        proofs += [p for d in (witness.get("days") or result.get("days") or []) for p in d.get("proofs", [])]
        if any(p.get("check") == "unavailable" for p in proofs):
            missing.append("--check-bitcoin: Bitcoin header sources unreachable")
    return missing


def channel_texts(source):
    source = str(source)
    if source.startswith(("http://", "https://")):
        import urllib.parse
        import urllib.request
        posts, before = [], None
        for _ in range(200):
            url = source + (("&" if "?" in source else "?") + "before=" + str(before) if before else "")
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "TgWitness-verify",
                                                                             "Accept-Language": "en"}),
                                        timeout=30) as response:
                live = all(telegram_page(address) for address in (url, response.geturl()))
                page = response.read(MAX_SMALL_MEMBER_BYTES).decode("utf-8", "replace")
            ids = [int(n) for n in re.findall(r'data-post="[^"/]+/(\d+)"', page)]
            for block in re.split(r'data-post="', page)[1:]:
                number, text, meta = CHANNEL_POST.match(block), CHANNEL_TEXT.search(block), CHANNEL_META.search(block)
                stamp = CHANNEL_TIME.search(meta.group(1)) if live and meta else None
                posts.append((int(number.group(1)) if number else None, stamp.group(1) if stamp else None,
                              (text.group(1) if text else "") if live else block,
                              ("edited" if post_edited(meta.group(1)) else "telegram") if stamp else None))
            if not ids or (before is not None and min(ids) >= before):
                break
            before = min(ids)
        return posts
    if Path(source).stat().st_size > MAX_JSON_BYTES:
        raise ValueError(Path(source).name + " exceeds the verifier's size limit")
    text = Path(source).read_text(encoding="utf-8", errors="replace")
    if source.lower().endswith(".json"):
        data = json.loads(text)
        found = []
        for message in data.get("messages", []):
            body = message.get("text", "")
            if isinstance(body, list):
                body = "".join(part if isinstance(part, str) else part.get("text", "") for part in body)
            found.append((message.get("id"), message.get("date"), body, "supplied"))
        return found
    return [(None, None, text, None)]


def check_channel(witness, source):
    key = Ed25519PublicKey.from_public_bytes(base64.b64decode(witness["public_key"], validate=True))
    matching, invalid, differing, foreign, dates, live, edited = set(), [], [], 0, {}, {}, set()
    for message_id, date, text, origin in channel_texts(source):
        for body, signature in WITNESS_TOKEN.findall(text):
            try:
                raw = unb64url(body)
                key.verify(unb64url(signature), raw)
                statement = json.loads(raw)
            except Exception:
                invalid.append(message_id)
                continue
            if statement.get("witness") != witness["fingerprint"]:
                foreign += 1
                continue
            expected = witness["statements"].get(statement.get("seq"))
            if expected != statement:
                differing.append(statement.get("seq"))
            else:
                matching.add(statement["seq"])
                if origin == "edited":
                    edited.add(statement["seq"])
                elif date:
                    dates[statement["seq"]] = date
                    moment = telegram_time(date) if origin == "telegram" else None
                    if moment:
                        live[statement["seq"]] = min(live.get(statement["seq"]) or "~", moment)
    posted = set(witness["posted"])
    return {"matching": len(matching), "matching_records": sorted(matching),
            "invalid_signatures": invalid, "differ_from_journal": differing,
            "other_witnesses": foreign,
            "posted_but_not_found": sorted(posted - matching),
            "never_posted": sorted(set(witness["statements"]) - posted),
            "telegram_post_dates": dates, "telegram_live_dates": live, "edited_posts": sorted(edited),
            "post_date_verification": "read-from-telegram" if live else "supplied" if dates else "not-performed"}


def post_edited(meta):
    head = re.sub(r'<span class="tgme_widget_message_from_author".*?</span>', "",
                  meta.split('<a class="tgme_widget_message_date"')[0], flags=re.S)
    return bool(re.sub(r"<[^>]+>|&nbsp;|[\s,]", "", head))


def telegram_page(address):
    import urllib.parse
    parts = urllib.parse.urlsplit(address)
    return parts.scheme == "https" and parts.hostname in TELEGRAM_PAGES and parts.path.startswith("/s/")


def telegram_time(value):
    try:
        moment = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    return moment.astimezone(timezone.utc).isoformat() if moment.tzinfo else None


def channel_head_time(witnessed, check):
    live = (check or {}).get("telegram_live_dates") or {}
    floor = witnessed.get("head_not_before")
    return min((live[seq] for seq in witnessed.get("export_head_witness_records") or []
                if seq in live and not (floor and witness_moment(live[seq]) < witness_moment(floor))), default=None)


def verify_dossier(path, expected_fingerprint=None, bundle=None):
    value = read_json_file(path)
    statement = authenticate_statement(value)
    if not is_format(statement.get("format"), "dossier-v1"):
        raise VerifierTooOld("Unsupported profile format")
    fp = fingerprint(statement["public_key"])
    if expected_fingerprint and fp != expected_fingerprint:
        raise ValueError("Public key differs from the independently trusted fingerprint")
    Ed25519PublicKey.from_public_bytes(base64.b64decode(statement["public_key"], validate=True)).verify(
        base64.b64decode(value["signature"], validate=True), canonical(statement))
    result = {"format": statement["format"], "fingerprint": fp, "chat": statement.get("chat"),
              "people": len(statement.get("people", [])), "built_at": statement.get("built_at"),
              "producer": statement.get("producer"), "key_pinned": bool(expected_fingerprint), "records_checked": 0}
    if bundle:
        with open_archive(bundle) as archive:
            if read_manifest(archive)["public_key"] != statement["public_key"]:
                raise ValueError("The evidence export was signed by another workspace key")
        verify_bundle(bundle, fp)
        wanted = {int(seq): digest for seq, digest in statement.get("record_hashes", {}).items()}
        found = bundle_hashes(bundle, wanted)
        for seq, digest in wanted.items():
            if found.get(seq) != digest:
                raise ValueError("Profile fact refers to record " + str(seq) + ", which the export does not contain")
        result["records_checked"] = len(wanted)
    return result


def verify_public_proof(path, collector_fingerprint=None, witness_fingerprint=None, bundle=None):
    value = read_json_file(path)
    statement = authenticate_statement(value, "witness_public_key")
    if not is_format(statement.get("format"), "public-proof-v1"):
        raise VerifierTooOld("Unsupported public proof")
    public = statement["witness_public_key"]
    fp = fingerprint(public)
    if witness_fingerprint and fp != witness_fingerprint:
        raise ValueError("Public proof witness differs from the trusted fingerprint")
    Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True)).verify(
        base64.b64decode(value["signature"], validate=True), canonical(statement))
    pin = statement["collector_fingerprint"]
    if collector_fingerprint and pin != collector_fingerprint:
        raise ValueError("Public proof collector differs from the trusted fingerprint")
    capture, checkpoint = statement.get("capture"), statement.get("checkpoint")
    result = {"format": statement["format"], "alias": statement["alias"], "observed_at": statement["observed_at"],
              "status": statement["status"], "collector_fingerprint": pin, "witness_fingerprint": fp,
              "keys_pinned": bool(collector_fingerprint and witness_fingerprint),
              "capture_signature_verified": False, "evidence_counters_checked": False}
    if capture is not None:
        captured = verify_capture(capture, checkpoint["statement"])
        Ed25519PublicKey.from_public_bytes(base64.b64decode(captured["public_key"], validate=True)).verify(
            base64.b64decode(checkpoint["signature"], validate=True), canonical(checkpoint["statement"]))
        if statement["status"] == "ok" and fingerprint(captured["public_key"]) != pin:
            raise ValueError("Capture proof was signed by another collector")
        result.update(capture_signature_verified=True, counts=captured["counts"], event_count=captured["event_count"],
                      head_hash=captured["head_hash"], last_message_at=captured.get("last_message_at"))
        if bundle:
            verify_bundle(bundle, pin)
            check_capture_prefix(capture, bundle)
            result["evidence_counters_checked"] = True
    elif statement["status"] == "ok" or bundle:
        raise ValueError("Proof contains no signed capture counters")
    return result


def verify_history_report(path, expected_fingerprint=None, bundle=None):
    value = read_json_file(path)
    statement = authenticate_statement(value)
    if not is_format(statement.get("format"), "history-report-v1"):
        raise VerifierTooOld("Unsupported history progress report")
    public = statement["public_key"]
    fp = fingerprint(public)
    if expected_fingerprint and fp != expected_fingerprint:
        raise ValueError("Public key differs from the independently trusted fingerprint")
    Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True)).verify(
        base64.b64decode(value["signature"], validate=True), canonical(statement))
    sources = statement["sources"]
    ids = [s["chat_id"] for s in sources]
    if (any(type(cid) is not int for cid in ids) or len(set(ids)) != len(ids)
            or type(statement["sources_total"]) is not int or len(ids) != statement["sources_total"]):
        raise ValueError("History report source list is inconsistent")
    for key in ("captured", "unavailable"):
        if (type(statement[key]) is not int or any(type(s[key]) is not int or s[key] < 0 for s in sources)
                or sum(s[key] for s in sources) != statement[key]):
            raise ValueError("History report counts are inconsistent")
    checkpoint = statement["checkpoint"]
    boundary = checkpoint["statement"]["event_count"]
    if type(boundary) is not int or boundary < 0:
        raise ValueError("Invalid history report checkpoint")
    verify_checkpoint(checkpoint, public, boundary, lambda seq: checkpoint["statement"]["head_hash"])
    checked = False
    if bundle:
        verify_bundle(bundle, fp, checkpoint)
        counts = {cid: {"captured": 0, "unavailable": 0} for cid in ids}
        observed_sources = None
        cursors, cursor_format = {}, None
        with open_archive(bundle) as archive, archive.open("events.jsonl") as stream:
            for line in bounded_lines(stream):
                event = json.loads(line)
                if event["seq"] > boundary:
                    break
                payload = event["payload"]
                if payload.get("history_run_id") != statement["id"]:
                    continue
                if event["kind"] == "history.started":
                    observed_sources = payload["sources"]
                    cursor_format = payload.get("cursor_format")
                    if payload["account_id"] != statement["account_id"]:
                        raise ValueError("History report account differs from the journal")
                    if cursor_format and payload["options"] != statement.get("options"):
                        raise ValueError("History report options differ from the journal")
                elif event["kind"] == "history.cursor":
                    cursors[event["chat_id"]] = event
                elif event["kind"] in ("message.snapshot", "history.message.unavailable"):
                    if event["chat_id"] not in counts:
                        raise ValueError("History report omits an acquired source")
                    key = "captured" if event["kind"] == "message.snapshot" else "unavailable"
                    counts[event["chat_id"]][key] += 1
        if observed_sources is None or set(observed_sources) != set(ids):
            raise ValueError("History report source plan differs from the journal")
        if any(counts[s["chat_id"]] != {key: s[key] for key in ("captured", "unavailable")} for s in sources):
            raise ValueError("History report counts differ from the journal")
        if cursor_format:
            for source in sources:
                cursor = cursors.get(source["chat_id"])
                state = {key: source[key] for key in ("run_id", "chat_id", "title", "position", "phase",
                    "upper_id", "offset_id", "captured", "unavailable", "error", "metadata")}
                state["metadata"] = json.loads(state["metadata"])
                if (cursor is None or source.get("cursor_seq") != cursor["seq"]
                        or source.get("cursor_hash") != cursor["hash"]
                        or canonical(state) != canonical(cursor["payload"]["state"])):
                    raise ValueError("History report cursor differs from the journal")
        checked = True
    return {"format": statement["format"], "fingerprint": fp, "key_pinned": bool(expected_fingerprint),
            "history_run_id": statement["id"], "phase": statement["phase"], "captured": statement["captured"],
            "unavailable": statement["unavailable"], "sources_total": statement["sources_total"],
            "evidence_counts_checked": checked, "checkpoint_event_count": boundary,
            "limitation": "Journal comparison checks the source plan, account, message counters and available signed cursors. "
                          "Other progress fields are retained as signed collector statements. Review source attribution "
                          "and coverage with the acquisition record."}


def producer_line(producer):
    if not producer:
        return "Producer: not named in this (older) archive."
    return ("Producer (signed): " + str(producer.get("software")) + " " + str(producer.get("version")) + " - "
            + str(producer.get("project")) + " - " + str(producer.get("homepage"))
            + (" - commit " + str(producer["commit"]) if producer.get("commit") else "")
            + (" - source files SHA-256 " + str(producer["source_tree_sha256"]) if producer.get("source_tree_sha256") else ""))


def fingerprint_colors(value):
    data = bytes.fromhex(value)
    return [(data[i] * 360 // 256, 68, 40 + data[i + 1] % 24) for i in range(0, 32, 2)]


# BEGIN GENERATED VERIFIER LANGUAGES
# Catalogue SHA-256: ee50b4f4aef5ff6c0709954737a4569a4a8e1b68b1cdabb1d1ed97ce522dab6e
VERIFIER_LANGUAGE_DATA = (
    "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"
)
# END GENERATED VERIFIER LANGUAGES
import zlib
VERIFIER_LANGUAGES = json.loads(zlib.decompress(base64.b64decode(VERIFIER_LANGUAGE_DATA)))
SAY = {code: entry["words"] for code, entry in VERIFIER_LANGUAGES.items()}


WINDOW_WORDS = {"updates_diverted": "Updates went to another session",
                "session_revoked_externally": "Session revoked externally"}
KINDS = {"evidence": "Evidence archive", "chat": "Chat export", "account": "Account export",
         "account_disclosure": "Account disclosure", "witness": "Witness journal",
         "dossier": "People profiles", "proof": "Public proof", "report": "Sealed report",
         "history": "History report", "handover": "Handover extract", "selection": "Viewer selection",
         "distributed": "Distributed acquisition", "board": "Case Board", "attestation": "Collector attestation"}
CONSOLE_LIST_LIMIT = 10


def utc_stamp(value):
    match = re.fullmatch(r"(\d{4}-\d\d-\d\d)T(\d\d:\d\d:\d\d)(?:\.\d+)?(?:Z|\+00:00)", str(value))
    return match[1] + " " + match[2] + " UTC" if match else str(value)


def duration_text(seconds):
    seconds = int(seconds)
    return "%d:%02d:%02d" % (seconds // 3600, seconds % 3600 // 60, seconds % 60)


def verifier_language(value):
    value = (value or "").strip().lower().replace("_", "-").split(".")[0]
    known = {code.lower(): code for code in VERIFIER_LANGUAGES}
    if value in known:
        return known[value]
    if value.startswith("zh-") and any(part in ("hant", "tw", "hk", "mo") for part in value.split("-")[1:]):
        return "zh-Hant"
    windows = dict(zip(("english", "russian", "ukrainian", "spanish", "portuguese", "turkish", "arabic", "persian",
                        "urdu", "hindi", "indonesian", "vietnamese", "chinese", "french", "german", "italian",
                        "uzbek", "korean", "chinese (traditional)", "malay", "polish", "japanese", "thai", "hebrew", "bengali"),
                       VERIFIER_LANGUAGES))
    base = value.split("-")[0]
    return known.get(base) or windows.get(base)


def console_language(choice=None):
    if choice and choice != "auto":
        selected = verifier_language(choice)
        if selected is None:
            raise ValueError("Unsupported verifier language: " + str(choice))
        return selected
    value = next((os.environ[name] for name in ("LC_ALL", "LC_MESSAGES", "LANG") if os.environ.get(name)), "")
    if not value:
        import locale
        value = locale.getlocale()[0] or ""
    return verifier_language(value) or "en"


def choose_verifier_language(default):
    codes = tuple(VERIFIER_LANGUAGES)
    print("\n" + " / ".join(VERIFIER_LANGUAGES[c]["words"]["Language"] for c in ("en", "ru", "zh", "ar")))
    for index, code in enumerate(codes, 1):
        print(str(index).rjust(2) + ". " + VERIFIER_LANGUAGES[code]["name"] + " [" + code + "]")
    while True:
        entered = input("[" + VERIFIER_LANGUAGES[default]["name"] + "] > ").strip()
        if not entered:
            return default
        if entered.isascii() and entered.isdigit() and 1 <= int(entered) <= len(codes):
            return codes[int(entered) - 1]
        selected = verifier_language(entered)
        if selected:
            return selected
        print(reader_message("language_invalid", default))


def enable_ansi(stream):
    if os.name != "nt":
        return True
    try:
        import ctypes
        import msvcrt
        kernel = ctypes.windll.kernel32
        handle, mode = msvcrt.get_osfhandle(stream.fileno()), ctypes.c_uint32()
        return bool(kernel.GetConsoleMode(handle, ctypes.byref(mode))
                    and kernel.SetConsoleMode(handle, mode.value | 0x0004))
    except Exception:
        return False


def reader_message(key, lang):
    return VERIFIER_LANGUAGES[lang]["reader"][key]


class Console:
    WIDTH = 66
    STYLES = {"ok": "1;32", "bad": "1;31", "warn": "1;33", "dim": "2", "bold": "1", "accent": "1;38;5;75",
              "okbar": "1;97;42", "badbar": "1;97;41", "warnbar": "1;30;43"}

    def __init__(self, stream, lang="en", color=True, explain=False):
        self.stream, self.words, self.lang = stream, SAY[lang], lang
        self.explain_enabled = explain
        try:
            "✔✘⚠◷•─│╭╮╰╯█⠋".encode(stream.encoding or "ascii")
            self.glyph = dict(ok="✔", bad="✘", warn="!", wait="◷", dot="•", h="─", v="│", tl="╭", tr="╮",
                              bl="╰", br="╯", block="██", spin="⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
        except (LookupError, UnicodeEncodeError):
            self.glyph = dict(ok="+", bad="x", warn="!", wait="~", dot="*", h="-", v="|", tl="+", tr="+",
                              bl="+", br="+", block="##", spin="|/-\\")
        self.color = color and enable_ansi(stream)

    def t(self, text, **values):
        text = self.words.get(text, text)
        for name, value in values.items():
            text = text.replace("{" + name + "}", str(value))
        return text

    def paint(self, text, style):
        text = safe_text(text)
        if not self.color or not style:
            return text
        if not hasattr(self, "_paints"):
            self._paints = {}
        token = "TGWSTYLE" + os.urandom(16).hex()
        self._paints[token + "B"] = "\033[" + self.STYLES[style] + "m"
        self._paints[token + "E"] = "\033[0m"
        return token + "B" + text + token + "E"

    def say(self, text=""):
        text = safe_text(text)
        for token, sequence in getattr(self, "_paints", {}).items():
            text = text.replace(token, sequence)
        self.stream.write(text + "\n")

    def number(self, value):
        return format(value, ",").replace(",", " " if self.lang != "en" else ",") if type(value) is int else str(value)

    def banner(self, title=None, tagline=None):
        g, inner = self.glyph, self.WIDTH - 4
        title, brand = title or self.t("TgWitness verifier"), "PhishDestroy"
        tagline = tagline or self.t("Signed Telegram evidence · Ed25519 · SHA-256")
        self.say()
        self.say("  " + self.paint(g["tl"] + g["h"] * inner + g["tr"], "accent"))
        self.say("  " + self.paint(g["v"], "accent") + "  " + self.paint(title, "bold")
                 + " " * max(1, inner - 4 - len(title) - len(brand)) + self.paint(brand, "dim") + "  "
                 + self.paint(g["v"], "accent"))
        self.say("  " + self.paint(g["v"], "accent") + "  " + self.paint(tagline[:inner - 4], "dim")
                 + " " * max(0, inner - 2 - len(tagline[:inner - 4])) + self.paint(g["v"], "accent"))
        self.say("  " + self.paint(g["bl"] + g["h"] * inner + g["br"], "accent"))
        self.say()

    def field(self, label, value):
        self.say("  " + self.paint(self.t(label).ljust(10), "dim") + " " + value)

    def heading(self, label):
        text = self.t(label).upper()
        self.say()
        self.say("  " + self.paint(text, "accent") + " " + self.paint(self.glyph["h"] * (self.WIDTH - 3 - len(text)), "dim"))

    def check(self, state, label, detail=""):
        mark = {"ok": ("ok", "ok"), "bad": ("bad", "bad"), "warn": ("warn", "warn"), "wait": ("wait", "warn"),
                "none": ("dot", "dim")}[state]
        detail = self.t(detail)
        self.say("  " + self.paint(self.glyph[mark[0]], mark[1]) + " " + self.t(label))
        if detail:
            self.say("    " + (self.paint(detail, "dim") if state == "none" else detail))
        if state != "none":
            self.explain(label)

    def explain(self, label):
        meanings = VERIFIER_LANGUAGES[self.lang]["explain"]
        if self.explain_enabled and label in meanings:
            import textwrap
            lines = ([meanings[label]] if self.lang in ("zh", "zh-Hant", "ja", "th", "hi", "bn", "ar", "fa", "ur", "he")
                     else textwrap.wrap(meanings[label], self.WIDTH - 4))
            for line in lines:
                self.say("    " + self.paint(line, "dim"))

    def signer(self, value):
        if not value:
            return
        groups = [value[i:i + 4] for i in range(0, 64, 4)]
        self.field("Signer", self.paint(" ".join(groups[:8]), "bold"))
        self.say("  " + " " * 11 + self.paint(" ".join(groups[8:]), "bold"))
        if self.color:
            import colorsys
            blocks = ""
            for hue, saturation, lightness in fingerprint_colors(value):
                r, g, b = colorsys.hls_to_rgb(hue / 360, lightness / 100, saturation / 100)
                code = 16 + 36 * round(r * 5) + 6 * round(g * 5) + round(b * 5)
                blocks += "\033[38;5;" + str(code) + "m" + self.glyph["block"]
            self.say("  " + " " * 11 + blocks + "\033[0m")

    def verdict(self, ok, reason="", evidence=None):
        evidence = evidence or {}
        state = "bad" if not ok else "ok" if evidence.get("minimum_met") else "warn"
        if not ok:
            label = self.t("VERIFICATION FAILED")
        elif evidence.get("minimum_met"):
            label = self.t("MINIMUM FOR EVIDENCE MET · ATTESTED COLLECTION RUN" if evidence["profile"] == "attested"
                           else "MINIMUM FOR EVIDENCE MET")
        elif evidence.get("bound_through"):
            label = self.t("MINIMUM MET UP TO RECORD {through} OF {total}", through=self.number(evidence["bound_through"]),
                           total=self.number(evidence["records"]))
        else:
            label = self.t("INTEGRITY ONLY · MINIMUM FOR EVIDENCE NOT MET")
        text = " " + self.glyph[state] + "  " + label + " "
        width = sum(0 if unicodedata.category(c) in ("Mn", "Me", "Cf") else 2 if unicodedata.east_asian_width(c) in "WF" else 1
                    for c in text)
        inner = max(self.WIDTH - 4, width)
        self.say()
        if self.color:
            self.say("  " + self.paint(text + " " * (inner + 2 - width), state + "bar"))
        else:
            self.say("  " + self.glyph["tl"] + self.glyph["h"] * inner + self.glyph["tr"])
            self.say("  " + self.glyph["v"] + text + " " * (inner - width) + self.glyph["v"])
            self.say("  " + self.glyph["bl"] + self.glyph["h"] * inner + self.glyph["br"])
        if reason:
            self.say("  " + self.paint(reason, "bad"))

    def spinner(self):
        return Spinner(sys.stderr, self.t("Checking signatures, hashes and the record chain"), self.glyph["spin"])

    def failure(self, path, exc):
        self.field("File", safe_text(path))
        message = safe_text(exc)
        label = ("Key mismatch" if "fingerprint" in message.lower() else
                 "File changed" if "File hash mismatch" in message or "ZIP changed during" in message else
                 "Signature mismatch" if isinstance(exc, InvalidSignature) else None)
        self.verdict(False, self.t(label) if label else reader_message("error", self.lang))
        self.field("Technical details", type(exc).__name__ + ": " + message)
        self.say()

    def case(self, case):
        shown = [(label, case.get(key)) for label, key in (("Title", "title"), ("Case ID", "id"),
                 ("Examiner", "examiner"), ("Organization", "organization")) if case.get(key)]
        if shown:
            self.heading("Case")
            for label, value in shown:
                self.say("  " + self.paint(self.t(label).ljust(14), "dim") + " " + str(value))

    def seal(self, result, name):
        seal = result.get("report_seal")
        if seal:
            self.check("ok", "Report seal", self.t("{name} · intact · language {lang}", name=name, lang=seal["language"]))
        else:
            self.check("none", "Report seal", self.t("not present (older export)"))
        if result.get("sha256sums"):
            self.check("ok", "SHA256SUMS", self.t("matches the signed manifest"))
        else:
            self.check("none", "SHA256SUMS", self.t("not present (older export)"))

    def timestamps(self, anchors):
        self.heading("Timestamps")
        self.explain("Timestamps")
        if not anchors:
            self.say("  " + self.paint(self.t("No independent timestamps: times come from the collector's clock."), "dim"))
            return
        # One entry for each service: a long journal carries a proof from every service at every checkpoint.
        groups = {}
        for anchor in anchors:
            groups.setdefault((anchor.get("kind") == "rfc3161", anchor["service"]), []).append(anchor)
        shown = lambda value: value.replace("T", " ").replace("Z", " UTC").replace("+00:00", " UTC")
        note = lambda text: self.say("    " + self.paint(text, "dim"))
        for (rfc, service), items in groups.items():
            numbers = sorted(int(item["checkpoint"][11:-5]) for item in items if item["checkpoint"][11:-5].isdigit())
            if len(numbers) != len(items):
                point = ", ".join(sorted({item["checkpoint"] for item in items})[:3])
            elif len(items) == 1:
                point = self.t("checkpoint #{n}", n=self.number(numbers[0]))
            else:
                point = self.t("checkpoints: {n} (#{first}–#{last})", n=self.number(len(items)),
                               first=self.number(numbers[0]), last=self.number(numbers[-1]))
            if rfc:
                checked = sum(item.get("signature", "").startswith("checked") for item in items)
                times = sorted(item["time"] for item in items if item.get("time"))
                span = "?" if not times else shown(times[0]) + (" – " + shown(times[-1]) if times[-1] != times[0] else "")
                self.check("ok" if checked == len(items) else "warn", "RFC 3161 · " + service, point + " · " + span)
                if checked in (0, len(items)):
                    note(self.t("signature chained to your root" if checked else "signature not checked: add --tsa-ca"))
                else:
                    note(self.t("signature chained to your root") + ": " + self.number(checked) + " / " + self.number(len(items)))
                found = [item.get("revocation") or {} for item in items]
                good = [item for item in found if item.get("status") == "good"]
                if good:
                    latest = max(good, key=lambda item: item["as_of"])
                    note(self.t("signing certificate not revoked as of {time} ({source})", source=latest["source"],
                                time=shown(latest["as_of"])))
                if any(item.get("status") not in (None, "good", "revoked_after", "failed") for item in found):
                    note(self.t("revocation not checked (no OCSP/CRL in the archive)"))
                references = sorted({item["certificate_reference"] for item in items if item.get("certificate_reference")})
                if references:
                    note(self.t("Signing certificate reference") + ": " + ", ".join(references))
                warnings = [self.t("signing certificate revoked at {time}, after the time stamp ({source})",
                                   source=item["source"], time=shown(item["revoked_at"]))
                            for item in found if item.get("status") == "revoked_after"]
                warnings += [self.t("revocation check failed: {reason}", reason=item["error"])
                             for item in found if item.get("status") == "failed"]
                warnings += [self.t(warning) for item in items for warning in item.get("warnings") or []]
                for warning in dict.fromkeys(warnings):
                    self.check("warn", "Timestamp warning", warning)
            else:
                states = {}
                for item in items:
                    states.setdefault(item.get("status"), []).append(item)
                state = "ok" if set(states) == {"confirmed"} else "wait" if set(states) == {"pending"} else "warn"
                self.check(state, "OpenTimestamps · " + service, point)
                for status, members in states.items():
                    detail = self.t({"pending": "pending: run ots upgrade, then ots verify", "confirmed": "Confirmed",
                                     "bitcoin-unverified": "Bitcoin attestation present; run ots verify"}.get(
                                         status, "unknown attestation type; no verified Bitcoin timestamp"))
                    if status == "confirmed":
                        times = sorted(item["time"] for item in members if item.get("time"))
                        detail += " · Bitcoin" + (" · " + shown(times[0]) + (" – " + shown(times[-1]) if times[-1] != times[0] else "")
                                                  if times else "")
                    note(detail + (": " + self.number(len(members)) if len(items) > 1 else ""))

    def lines(self, label, lines, limit=8):
        if not lines:
            return
        self.heading(label)
        self.explain(label)
        for line in lines[:limit]:
            self.say("  " + self.paint(self.glyph["dot"], "dim") + " " + self.t(line))
        if len(lines) > limit:
            self.say("  " + self.paint(self.t("… and {n} more", n=len(lines) - limit), "dim"))

    def coverage(self, coverage):
        self.heading("Coverage")
        self.explain("Coverage")
        periods, gaps = coverage["continuous"], coverage["gaps"]
        self.check("none", "Observation periods", self.number(len(periods)) if periods else "No observation period recorded.")
        # The full lists are in coverage.json and in the JSON answer; a long journal would bury the verdict here.
        for period in periods[:CONSOLE_LIST_LIMIT]:
            self.say("    " + utc_stamp(period["from"]) + " → " + utc_stamp(period["to"]) + " · "
                     + self.t("Duration") + ": " + duration_text(period["seconds"]))
        if len(periods) > CONSOLE_LIST_LIMIT:
            self.say("    " + self.paint(self.t("… and {n} more", n=len(periods) - CONSOLE_LIST_LIMIT), "dim"))
        self.check("warn" if gaps else "none", "Observation gaps", self.number(len(gaps)))
        for gap in gaps[:CONSOLE_LIST_LIMIT]:
            self.say("    " + utc_stamp(gap["from"]) + " → " + utc_stamp(gap["to"]) + " · "
                     + self.t("Reason") + ": " + self.coverage_reason(str(gap["reason"])))
        if len(gaps) > CONSOLE_LIST_LIMIT:
            self.say("    " + self.paint(self.t("… and {n} more", n=len(gaps) - CONSOLE_LIST_LIMIT), "dim"))
        for window in coverage.get("session_windows") or []:
            self.check("warn", WINDOW_WORDS.get(window["reason"], str(window["reason"])),
                       utc_stamp(window["from"]) + " → " + utc_stamp(window["to"])
                       + (" · " + self.t("open at the last record") if window.get("not_resumed_by_last_record") else ""))
        session = coverage.get("session") or {}
        starts = {}
        for item in session.get("sessions_at_start") or []:
            starts.setdefault(item.get("others"), []).append(str(item["at"]))
        for others, times in starts.items():
            self.check("warn" if others else "none", "Other sessions at start",
                       ("?" if others is None else self.number(others)) + " · " + utc_stamp(times[0])
                       + (" → " + utc_stamp(times[-1]) + " · ×" + self.number(len(times)) if len(times) > 1 else ""))
        if session.get("sessions_added"):
            self.check("warn", "Sessions added during observation",
                       self.number(sum(item["added"] for item in session["sessions_added"]))
                       + " · " + utc_stamp(session["sessions_added"][0]["at"]))
        groups, other, unlabelled, captures, sealed = source_counts(coverage)
        parts = [self.t(label) + " " + self.number(sum(count for _, count in found)) for label, found in groups]
        parts += [name + " " + self.number(count) for name, count in other]
        parts += [self.t("no source label") + " " + self.number(unlabelled)] if unlabelled else []
        parts += [self.t("inside a sealed run") + " " + self.number(sealed)] if sealed else []
        parts += [self.t("recorder captures") + " " + self.number(captures)] if captures else []
        if parts:
            self.check("none", "Records by source", " · ".join(parts))
        for chat in coverage["unobserved_ids"]:
            if chat["not_observed"]:
                self.check("warn", "Numbers not observed", str(chat.get("title") or chat["chat_id"]) + ": "
                           + str(chat["not_observed"]) + " · ID " + str(chat["observed_from"]) + "–" + str(chat["observed_to"]))
        summary = coverage.get("gap_summary") or {}
        account = summary.get("account") if summary.get("status") == "on" else None
        if account:
            if account.get("status") == "applicable":
                self.check("warn" if account["missing"] else "none", "Account", self.t("Numbers not observed")
                           + ": " + str(account["missing"]) + " · ID " + str(account["observed_from"]) + "–" + str(account["observed_to"]))
            else:
                self.check("none", "Account", self.t("Not checked") + " · " + self.t(str(account.get("reason") or "")))

    def coverage_reason(self, text):
        mapping = {"observation restarted": "Observation started", "observation paused by the operator": "Paused",
                   "collector process stopped": "Stopped", "collector process ended without an orderly stop": "Interrupted",
                   "collector error: capture may be incomplete": "Error", "connection to Telegram closed": "Disconnected",
                   "connection to Telegram lost": "Disconnected", "observation could not resume after a restart": "Interrupted",
                   **{SESSION_NOTES[reason]: word for reason, word in WINDOW_WORDS.items()}}
        if text in mapping:
            return self.t(mapping[text])
        if text.startswith("no capture heartbeat for "):
            minutes = re.search(r"for (\d+) min", text)
            return self.t("Interrupted") + (" · " + minutes[1] + " min" if minutes else "")
        if text.startswith("observation stopped: "):
            cause = text.partition(": ")[2]
            return self.t("Stopped") + ("" if cause == "shutdown" else ": " + cause)
        return text

    def outside(self, outside):
        drand, gateway, devices = outside["drand"], outside.get("gateway") or {}, outside["devices"]
        if not (drand["rounds"] or gateway.get("windows") or devices["checks"]):
            return
        self.heading("Live recording and devices")
        if drand["rounds"]:
            self.check("none", "drand", self.t("Recorded") + ": " + str(drand["rounds"]) + " · "
                       + utc_stamp(drand["first"]["at"]) + " → " + utc_stamp(drand["last"]["at"]))
            self.field("Gap", duration_text(drand["largest_gap_seconds"]))
            checked = drand.get("checked")
            self.check("ok" if checked and checked.get("relays") else "warn", "drand",
                       (self.t("Matches") + ": " + str(checked["confirmed"]) + "/" + str(checked["asked"])
                        + " · " + ", ".join(checked["relays"])) if checked and checked.get("relays")
                       else self.t("Not checked") + " · --check-drand")
            if drand["clock_behind_seconds"] > 1:
                self.check("warn", "Time", "drand: +" + str(drand["clock_behind_seconds"]) + " s")
        if gateway.get("windows"):
            self.check("none", "Cloudflare Gateway DNS", self.t("Count") + ": " + str(gateway["queries"]) + " · "
                       + str(gateway["first"]) + " → " + str(gateway["last"]))
            self.field("Source", ", ".join(gateway["addresses"]))
            for gap in gateway["gaps"]:
                self.check("warn", "Gap", str(gap["from"]) + " → " + str(gap["until"]))
            if gateway.get("truncated_windows"):
                self.check("warn", "Partial acquisition", str(gateway["truncated_windows"]))
            for name, count in gateway["names"][:15]:
                self.say("    " + name + ": " + str(count))
        if devices["checks"]:
            self.check("none", "Device list", self.t("Count") + ": " + str(devices["checks"]) + " · "
                       + str(devices["first_check"]) + " → " + str(devices["last_check"]))
            self.field("Changed", str(max(0, devices["changes_total"] - 1)))
            for change in devices["changes"][:20]:
                self.say("    " + str(change["at"]) + " +" + str(len(change["added"])) + " −" + str(len(change["removed"])))

    def account_coverage(self, result):
        coverage = result["coverage"]
        self.heading("Coverage")
        self.explain("Coverage")
        self.field("Account", str(result["account_id"]))
        self.field("Messages", self.number(result["counts"]["messages"]))
        self.field("Scope", str(coverage["tasks_done"]) + "/" + str(coverage["tasks_total"]))
        for field in ("failed_pages", "failed_attachments"):
            if coverage[field]:
                self.check("warn", "Failed", field + ": " + str(coverage[field]))
        for gap in coverage["gaps"]:
            self.check("warn", "Gap", str(gap))

    def tdx(self, tdx):
        self.heading("Intel TDX")
        for quote in tdx["quotes"]:
            where = self.t("record {n}", n=self.number(quote["record"])) + " · " if "record" in quote else ""
            if quote["status"] != "pass":
                self.check("bad", "Intel TDX quote", where + self.t(quote["detail"])
                           + (" · " + quote["error"] if quote.get("error") else ""))
                continue
            self.check("ok", "Intel TDX quote",
                       where + self.t("quote signature, quoting enclave and PCK chain to the pinned Intel root are valid"))
            self.say("    " + self.paint(quote["pck_ca"] + " · FMSPC " + quote["fmspc"] + " · v"
                                         + str(quote["quote_version"]), "dim"))
            for name in TDX_MEASUREMENTS:
                self.field({"report_data": "REPORTDATA"}.get(name, name.upper()), quote[name])
            self.check("ok", "Report data", self.t("SHA-512 of the start record: binds the journal key, run and host"
                                                   if "record" in quote else "SHA-512 of the signed collector statement"))
            tcb = quote["tcb"]
            if tcb["status"] == "not checked":
                self.check("warn", "Intel TCB status", self.t(tcb["detail"]))
            else:
                self.check("ok" if tcb["status"] == "UpToDate" else "warn", "Intel TCB status", tcb["status"] + " · "
                           + self.t("Intel collateral issued {issued}, evaluated at {time}",
                                    issued=tcb["collateral_issued"], time=tcb["evaluated_at"]))
        self.check("warn", "Not checked", self.t("compose and OS image: python -m tgwitness.cloud verify"))

    def show(self, shown, path, result, notes):
        self.say(evidence_line(result["evidence"], self.t) if result.get("evidence") else assurance_line(result))
        self.banner()
        self.field("File", str(path))
        self.field("Type", self.t(KINDS[shown]) + self.paint("  " + str(result.get("format") or ""), "dim"))
        self.signer(result.get("fingerprint"))
        self.heading("Checks")
        if shown == "evidence":
            self.check("ok", "Manifest signature", self.t("Ed25519 · valid"))
            self.check("ok", "File hashes", self.t("{n} files · SHA-256 match", n=self.number(result["files_checked"])))
            head = result["head_hash"]
            self.check("ok", "Record chain", self.t("{n} records · head {hash}", n=self.number(result["events"]),
                                                    hash=head[:8] + "…" + head[-8:]))
            self.seal(result, "report.html")
            if result.get("witness"):
                witness = result["witness"]
                self.check("ok" if witness["consistent"] else "warn", "Witness",
                           self.t("checkpoints match through record {a} of {b}",
                                  a=self.number(witness["verified_through_event"]), b=self.number(result["events"])))
        elif shown == "account_disclosure":
            self.check("ok", "Manifest signature", self.t("Ed25519 · valid"))
            self.check("ok", "File hashes", self.t("{n} files · SHA-256 match", n=self.number(result["files_checked"])))
            self.check("ok" if result["source_reference_checked"] else "warn", "Source reference",
                       "archive hash and collector key checked" if result["source_reference_checked"] else "not supplied (--evidence)")
            self.check("none", "Derivation", "review filtering and redaction against the source archive")
        elif shown == "account":
            self.check("ok", "Manifest signature", self.t("Ed25519 · valid"))
            self.check("ok", "File hashes", self.t("{n} files · SHA-256 match", n=self.number(result["files_checked"])))
            self.check("ok", "Capture receipts", str(result["receipt_count"]) + " · " + result["receipt_head_sha256"][:16] + "…")
            self.check("ok" if result["complete_within_scope"] else "warn", "Coverage",
                       "complete within selected scope" if result["complete_within_scope"] else "partial acquisition")
        elif shown == "chat":
            self.check("ok", "Manifest signature", self.t("Ed25519 · valid"))
            self.check("ok", "File hashes", self.t("{n} files · SHA-256 match", n=self.number(result["files_checked"])))
            self.check("ok", "Messages", self.t("{n} messages · {title}", n=self.number(result.get("message_count")),
                                                title=(result.get("chat") or {}).get("title") or "?"))
            if result.get("parts"):
                self.check("ok", "Accounts", self.t("{n} account(s) signed their message ranges", n=len(result["parts"])))
            self.seal(result, "chat.html")
        elif shown == "handover":
            self.check("ok", "Manifest signature", self.t("Ed25519 · valid"))
            self.check("ok", "File hashes", self.t("{n} files · SHA-256 match", n=self.number(result["files_checked"])))
            self.check("ok", "Unchanged records", self.t("{n} · hash, signature and chain checked",
                                                         n=self.number(result["records_unchanged"])))
            self.check("warn" if result["records_minimised"] else "ok", "Minimised records",
                       self.t("{n} · signature over the original record checked",
                              n=self.number(result["records_minimised"])))
            self.check("none", "Left out", self.t("{n} records of {total} in the journal",
                                                  n=self.number(result["records_left_out"]),
                                                  total=self.number(result["journal_events"])))
            self.seal(result, "report.html")
        elif shown == "selection":
            self.check("ok", "Described archive", self.t("verified and matches the seal"))
            self.check("ok", "Items", str(result["items_checked"]))
            self.check("ok" if result.get("selection_signed") else "none", "Signature",
                       "Signed Case Board selection; exact records matched against the archive" if result.get("selection_signed")
                       else self.t("Unsigned selection; item content matched against the signed archive"))
        elif shown == "report":
            seal = result["report_seal"]
            subject = seal["subject"]
            self.check("ok", "Report seal", self.t("{name} · intact · language {lang}", name=path.name, lang=seal["language"]))
            described = (self.t("{n} records · head {hash}", n=self.number(subject.get("event_count",
                                                                                     subject.get("record_count"))),
                                hash=str(subject.get("head_hash"))[:8] + "…")
                         if "event_count" in subject or "record_count" in subject else
                         self.t("{n} messages · {title}", n=self.number(subject.get("message_count")),
                                title=subject.get("chat_title") or subject.get("chat_id")))
            self.check("none", "Describes", described)
            if result["evidence_checked"]:
                self.check("ok", "Described archive", self.t("verified and matches the seal"))
            else:
                self.check("warn", "Described archive", self.t("not supplied (--evidence)"))
        else:
            self.check("ok", "Signature", self.t("Ed25519 · valid"))
        if shown == "evidence":
            self.timestamps(result.get("anchors") or [])
            self.coverage(result["coverage"])
            self.outside(result["outside"])
            notes = [n for n in notes if n not in coverage_lines(result["coverage"])
                     and n not in outside_lines(result["outside"]) and not n.startswith("No retained checkpoint")]
        elif shown == "account":
            self.account_coverage(result)
            notes = [note for note in notes if note not in account_export_lines(result)]
        elif shown == "account_disclosure":
            self.heading("Details")
            for label, field in (("Messages", "messages"), ("Chats", "chats"), ("Media", "media")):
                self.field(label, self.number(result["counts"][field]))
            self.explain("Minimised records")
        elif shown not in ("chat", "report", "handover"):
            facts = [key + ": " + json.dumps(value, ensure_ascii=False) for key, value in result.items()
                     if isinstance(value, (str, int, bool)) and key != "fingerprint"]
            self.lines("Technical details", facts, limit=12)
        if result.get("tdx"):
            self.tdx(result["tdx"])
            notes = [note for note in notes if note not in tdx_lines(result["tdx"])]
        self.lines("Notes", [self.localized_note(note) for note in notes])
        self.case(result.get("case") or (result.get("report_seal") or {}).get("case") or {})
        self.conditions(result.get("evidence"))
        self.verdict(True, evidence=result.get("evidence"))
        producer = result.get("producer")
        if producer:
            self.say("  " + self.paint(self.t("Produced by") + ": " + str(producer.get("software")) + " "
                                       + str(producer.get("version")) + " · " + str(producer.get("project")) + " · "
                                       + str(producer.get("homepage")), "dim"))
        self.say()

    def conditions(self, evidence):
        if not evidence:
            return
        self.heading("Conditions for evidence")
        needed = {"required": True, "supporting": False}
        role = None
        for row in evidence["conditions"]:
            if row["role"] != role:
                role = row["role"]
                self.say("  " + self.paint(self.t(ROLE_LABELS[role]), "bold"))
            mark = "ok" if row["status"] == "met" else "warn" if row["status"] != "missing" or needed[role] else "dot"
            detail = self.t(row["text"], **row["values"])
            if row.get("drand"):
                detail += " · " + self.t("drand rounds confirmed by {relays}", relays=row["drand"])
            self.say("  " + self.paint(self.glyph[mark], "dim" if mark == "dot" else mark) + " "
                     + self.t(CONDITION_LABELS[row["id"]]) + self.paint(" · " + self.t(row["scope"]), "dim"))
            self.say("    " + detail)
            if row["status"] != "met":
                self.say("    " + self.paint("→ " + self.t(row["how"]), "dim"))
            self.explain({"signer": "Key pinning", "head_binding": "Witness", "checkpoint": "Retained checkpoint"}.get(row["id"], ""))
        self.say()
        self.say("  " + self.paint(evidence_line(evidence, self.t), "ok" if evidence["minimum_met"] else "warn"))
        for line in next_lines(evidence, self.t):
            self.say("  " + line)

    def localized_note(self, note):
        if note in self.words:
            return self.t(note)
        if note.startswith("OpenTimestamps structure only:"):
            return "OpenTimestamps: " + self.t("Not checked") + " · ots verify"
        if note.startswith("The witness key is not pinned:") or note.startswith("A public proof is signed by its witness:"):
            return self.t("Witness") + ": " + reader_message("key_unconfirmed", self.lang) + " · --witness-fingerprint"
        if note.startswith("Witnessed from "):
            return self.t("Witness") + ": " + note.removeprefix("Witnessed from ").replace(" to ", " → ")
        if match := re.fullmatch(r"Witness checkpoints match through record (\d+) of (\d+)\.", note):
            return self.t("checkpoints match through record {a} of {b}", a=match[1], b=match[2])
        if match := re.fullmatch(r"The witness saw record (\d+) at (.+), beyond this export's last record (\d+)\.", note):
            return self.t("The witness saw record {n} at {time}, beyond this export's last record {count}.",
                          n=match[1], time=match[2], count=match[3])
        if match := re.fullmatch(r"(\d+) trailing record\(s\) have no matching witness checkpoint\.", note):
            return self.t("Witness") + ": " + self.t("Not supplied") + " · " + self.t("Records") + ": " + match[1]
        if note.startswith("The witness has no answer signed by this export's key:"):
            return self.t("Witness") + ": " + self.t("Not supplied")
        if note.startswith("Channel dates are supplied metadata;"):
            return self.t("Time") + ": " + self.t("Not checked") + " · Telegram"
        if note.startswith("Minimised records are authenticated"):
            return VERIFIER_LANGUAGES[self.lang]["explain"]["Minimised records"]
        if note.startswith(("Source reference not checked:", "History report signature only:")):
            return self.t("Described archive") + ": " + self.t("not supplied (--evidence)")
        return self.t("Technical details") + ": " + note if self.lang != "en" else note


class Spinner:
    def __init__(self, stream, text, frames):
        import threading
        self.stream, self.text, self.frames = stream, text, frames
        self.done = threading.Event()
        self.thread = threading.Thread(target=self.run, daemon=True)

    def run(self):
        index = 0
        while not self.done.wait(0.09):
            self.stream.write("\r  " + self.frames[index % len(self.frames)] + " " + self.text + "…")
            self.stream.flush()
            index += 1

    def __enter__(self):
        if getattr(self.stream, "isatty", lambda: False)():
            self.thread.start()
        return self

    def __exit__(self, *exc):
        self.done.set()
        if self.thread.is_alive():
            self.thread.join()
            self.stream.write("\r" + " " * (len(self.text) + 6) + "\r")
            self.stream.flush()



def matching_archives(directory):
    directory = Path(directory)
    try:
        manifest = directory / "manifest.json"
        if manifest.stat().st_size > MAX_MANIFEST_BYTES:
            return []
        wanted = manifest.read_bytes()
    except OSError:
        return []
    found, scanned = [], 0
    for parent in dict.fromkeys((directory, directory.parent)):
        try:
            for path in parent.iterdir():
                if path.suffix.lower() != ".zip" or not path.is_file():
                    continue
                scanned += 1
                if scanned > 100:
                    return found
                try:
                    with open_archive(path) as archive:
                        if read_member(archive, "manifest.json", MAX_MANIFEST_BYTES) == wanted:
                            found.append(path.resolve())
                except (OSError, ValueError, KeyError, RuntimeError, zipfile.BadZipFile):
                    continue
        except OSError:
            continue
    return sorted(set(found))


def entered_fingerprint(value):
    value = re.sub(r"[\s:]", "", value).lower()
    if value and not re.fullmatch(r"[a-f0-9]{64}", value):
        raise ValueError("Expected a SHA-256 fingerprint")
    return value


def file_sha256(path):
    with Path(path).open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


class Transcript:
    def __init__(self, stream):
        self.stream, self.text = stream, io.StringIO()

    def __getattr__(self, name):
        return getattr(self.stream, name)

    def write(self, value):
        self.text.write(re.sub(r"\x1b\[[0-9;]*m", "", value))
        return self.stream.write(value)


def save_transcript(path, text):
    for directory in (path.parent, Path.home() / "TgWitness-verifications"):
        try:
            directory.mkdir(parents=True, exist_ok=True)
            prefix = "verify-result-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-")
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", prefix=prefix,
                                             suffix=".txt", dir=directory, delete=False) as output:
                output.write(text)
                return Path(output.name)
        except OSError:
            continue
    return None


def interactive_verify(args):
    from contextlib import redirect_stdout
    lang = console_language(args.lang)
    if args.choose_language:
        lang = choose_verifier_language(lang)
    args.lang = lang
    say = lambda key: reader_message(key, lang)
    words = SAY[lang]
    print(say("trust"))
    path = Path(args.bundle).expanduser() if args.bundle else None
    if path is None:
        matches = matching_archives(Path(__file__).resolve().parent)
        if len(matches) == 1:
            print(say("found") + safe_text(matches[0]))
            chosen = input(say("confirm") + " ").strip().strip('"')
            path = Path(chosen).expanduser() if chosen else matches[0]
        else:
            chosen = input(say("archive") + " ").strip().strip('"')
            if not chosen:
                print(say("cancelled"))
                return 2
            path = Path(chosen).expanduser()
    path = path.resolve()
    if not path.is_file() or not zipfile.is_zipfile(path):
        print(say("bad_zip"))
        return 2
    fp = args.fingerprint
    while fp is None:
        try:
            fp = entered_fingerprint(input(say("key") + " "))
        except ValueError:
            print(say("bad_key"))
    command = [str(path), "--pretty", "--explain", "--lang", lang, "--max-gib", str(args.max_gib)]
    if fp:
        command += ["--fingerprint", fp]
    for name in ("checkpoint", "tsa_ca", "witness", "witness_fingerprint", "channel", "evidence",
                 "require_tier", "sealed_attestation", "sealed_policy", "sealed_repo"):
        if getattr(args, name):
            command += ["--" + name.replace("_", "-"), str(getattr(args, name))]
    for name in ("require_witness", "check_drand", "check_bitcoin", "strict", "board", "no_color"):
        if getattr(args, name):
            command.append("--" + name.replace("_", "-"))
    for url in args.bitcoin_source or ():
        command += ["--bitcoin-source", url]
    transcript, code = Transcript(sys.stdout), 0
    with redirect_stdout(transcript):
        print(say("unsigned"))
        print(say("trust"))
        print(words["Started {time}"].replace("{time}", datetime.now(timezone.utc).isoformat()))
        print("ZIP: " + safe_text(path))
        print(words["TgWitness verifier"] + ": " + safe_text(Path(__file__).resolve()))
        print("TgWitness SHA-256: " + file_sha256(__file__))
        print("Python: " + sys.version.split()[0])
        try:
            digest = file_sha256(path)
            print("ZIP SHA-256: " + digest)
            try:
                main(command)
            except SystemExit as exc:
                code = int(exc.code or 0)
            if file_sha256(path) != digest:
                raise ValueError("ZIP changed during verification; disregard any earlier success result")
        except Exception as exc:
            Console(sys.stdout, lang, not args.no_color).failure(path, exc)
            code = 1
        print(words["Finished"] + " (UTC): " + datetime.now(timezone.utc).isoformat())
        print(say("exit") + ": " + str(code))
    saved = save_transcript(path, transcript.text.getvalue())
    if saved:
        print(say("saved") + " " + safe_text(saved))
    else:
        print(say("not_saved"))
        code = code or 2
    return code


class CheckResult:
    def __init__(self, kind, details, signer_pinned, notes=None):
        self.kind = kind
        self.details = details
        self.signer_pinned = signer_pinned
        self.notes = notes if notes is not None else []


def verification_print(*values, **kwargs):
    import builtins
    builtins.print(*(safe_text(value) if isinstance(value, str) else value for value in values), **kwargs)


def verification_parser():
    parser = argparse.ArgumentParser(description=__doc__, epilog=
        "For a .tgwpw export: verify.py unseal-password SOURCE --out DESTINATION")
    parser.add_argument("bundle", nargs="?",
                        help="Evidence/chat/account/disclosure/witness ZIP, report JSON/HTML, or a stopped distributed acquisition directory")
    parser.add_argument("--fingerprint", help="Public key fingerprint retained independently")
    parser.add_argument("--checkpoint", type=Path, help="Previously retained signed checkpoint JSON")
    parser.add_argument("--tsa-ca", type=Path, help="Root certificate of the timestamp authority (PEM)")
    parser.add_argument("--witness", type=Path, help="Witness journal export to cross-check an evidence ZIP against")
    parser.add_argument("--witness-fingerprint", help="Witness key fingerprint retained independently")
    parser.add_argument("--require-witness", action="store_true",
                        help="Require a pinned witness checkpoint matching the full evidence ZIP's final record")
    parser.add_argument("--channel", help="Witness channel posts: Telegram Desktop result.json, saved page or t.me/s URL; post dates count as external time only from a live https://t.me/s/ page")
    parser.add_argument("--evidence", type=Path,
                        help="With a profile/proof/history JSON, sealed report or disclosure: verify the referenced original archive")
    parser.add_argument("--check-drand", action="store_true",
                        help="Compare the drand rounds in the journal with drand relays (needs internet)")
    parser.add_argument("--check-bitcoin", action="store_true",
                        help="Evaluate OTS proofs against block headers agreed by two HTTPS explorers (needs internet)")
    parser.add_argument("--bitcoin-source", action="append", metavar="URL",
                        help="Esplora API of your own Bitcoin node or explorer, used instead of the two public explorers; "
                             "repeat to require agreement. Implies --check-bitcoin")
    parser.add_argument("--require", choices=EVIDENCE_PROFILES[1:],
                        help="Exit 2 unless the minimum evidence conditions (evidence), or the minimum and an "
                             "attested collection run (attested), are met")
    parser.add_argument("--require-tier", choices=ASSURANCE_TIERS, help="Exit 2 if the complete export does not reach this tier")
    parser.add_argument("--strict", action="store_true", help="Exit 2 for an unpinned signer, 3 for an authenticated newer format")
    parser.add_argument("--sealed-attestation", type=Path, help="GitHub attestation bundle; checked with the existing gh verifier")
    parser.add_argument("--sealed-policy", type=Path, help="Independently trusted policy listing reviewed workflow and collector commits")
    parser.add_argument("--sealed-repo", default="phishdestroy/TgWitness", help="Repository identity expected in GitHub attestation")
    parser.add_argument("--board", action="store_true", help="Print Case Board collections, dangling references and slice changes")
    parser.add_argument("--compare", type=Path, metavar="SECOND_ZIP",
                        help="Compare two chat exports: messages present in only one of them and changed messages")
    parser.add_argument("--compare-fingerprint", help="Trusted fingerprint of the second archive's signer")
    parser.add_argument("--max-gib", type=int, default=MAX_UNCOMPRESSED_GIB,
                        help="Largest uncompressed archive to read, in GiB (default 4)")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--pretty", action="store_true", help="Readable, coloured answer (default at a terminal)")
    output.add_argument("--plain", action="store_true", help="Plain text answer (default when piped)")
    output.add_argument("--json", action="store_true", help="Only a JSON answer, for scripts")
    parser.add_argument("--no-color", action="store_true", help="No colours (also with the NO_COLOR variable)")
    parser.add_argument("--lang", type=lambda value: verifier_language(value) or value,
                        choices=("auto", *VERIFIER_LANGUAGES), help="Language of the readable answer")
    parser.add_argument("--choose-language", action="store_true", help="Show all languages before interactive verification")
    parser.add_argument("--pause", action="store_true", help="Wait for Enter after an interactive check (for launchers)")
    parser.add_argument("--explain", action="store_true", help="Explain what each readable check establishes")
    parser.add_argument("--interactive", action="store_true", help="Ask for the original ZIP and trusted key; save a readable transcript")
    return parser


def verification_arguments(parser, argv):
    args = parser.parse_args(argv)
    if bool(args.sealed_attestation) != bool(args.sealed_policy):
        parser.error("--sealed-attestation and --sealed-policy must be supplied together")
    args.implied_checks = set()
    if args.bitcoin_source:
        try:
            use_bitcoin_sources(args.bitcoin_source)
        except ValueError as exc:
            parser.error(str(exc))
        args.check_bitcoin = True
    if args.require_tier and ASSURANCE_TIERS.index(args.require_tier) >= ASSURANCE_TIERS.index("fresh") and not args.check_drand:
        args.check_drand = True
        args.implied_checks.add("check_drand")
    if args.require_tier and ASSURANCE_TIERS.index(args.require_tier) >= ASSURANCE_TIERS.index("timestamped") and not args.check_bitcoin:
        args.check_bitcoin = True
        args.implied_checks.add("check_bitcoin")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    if args.choose_language and not args.interactive:
        parser.error("--choose-language requires --interactive")
    return args


def verification_interactive(args, parser):
    if args.compare or args.compare_fingerprint or args.json or args.plain:
        parser.error("--interactive produces a readable single-archive check; comparison/JSON/plain options do not apply")
    if args.require_witness and (not args.witness or not args.witness_fingerprint):
        parser.error("--require-witness requires --witness and --witness-fingerprint")
    try:
        code = interactive_verify(args)
    except (EOFError, KeyboardInterrupt):
        verification_print(reader_message("cancelled", console_language(args.lang)))
        code = 2
    if args.pause and not os.environ.get("TGWITNESS_VERIFY_NO_PAUSE"):
        try:
            input(reader_message("pause", console_language(args.lang)) + " ")
        except (EOFError, KeyboardInterrupt):
            pass
    raise SystemExit(code)


def verification_comparison(args, parser, mode):
    unsupported = ["--" + name.replace("_", "-") for name in
                   ("checkpoint", "tsa_ca", "witness", "witness_fingerprint", "require_witness", "channel",
                    "evidence", "check_drand", "check_bitcoin", "bitcoin_source", "require_tier", "sealed_attestation", "board")
                   if getattr(args, name)]
    if unsupported:
        parser.error(", ".join(unsupported) + " cannot be used with --compare; verify the evidence archive separately")
    try:
        compared = compare_chat_exports(args.bundle, args.compare, args.fingerprint, args.compare_fingerprint, args.max_gib)
    except Exception as exc:
        code = 3 if args.strict and isinstance(exc, VerifierTooOld) else 1
        if mode == "json":
            verification_print(json.dumps({"verified": False, "error": type(exc).__name__ + ": " + str(exc)}, indent=2))
            raise SystemExit(code)
        verification_print("ASSURANCE: fail")
        parser.exit(code, "VERIFICATION FAILED: " + type(exc).__name__ + ": " + safe_text(exc) + "\n")
    pinned = bool(compared['first']['key_pinned'] and compared['second']['key_pinned'])
    compared['assurance'] = assurance(compared)
    compared['assurance']['scope'] = 'two authenticated chat exports; the comparison covers their contents'
    if mode == "json":
        verification_print(json.dumps({"verified": True, "kind": "comparison", "result": compared,
                          "signer_pinned": pinned, "requirements_met": not args.strict or pinned},
                         indent=2, ensure_ascii=True))
    else:
        verification_print(assurance_line(compared))
        print_comparison(compared)
    if args.strict and not pinned:
        raise SystemExit(2)
    return


def verification_json(args):
    notes = []
    data = read_json_file(args.bundle)
    kind = data.get("statement", {}).get("format")
    if data.get("format") in ATTESTATION_RECORDS or kind == "tgwitness-assurance-v1":
        result = verify_collector_attestation(data, args.fingerprint)
        return CheckResult("attestation", result, bool(args.fingerprint), tdx_lines(result.get("tdx")))
    if "statement" in data and "signature" in data:
        authenticate_statement(data, "public_key" if "public_key" in data["statement"] else "witness_public_key")
        known = {"tgwitness-board-selection-v1", "tgwitness-case-board-v1", "tgwitness-case-board-disclosure-v1",
                 "tgwitness-case-board-handover-v1", "tgwitness-account-loss-v1"}
        if kind not in known and not any(is_format(kind, name) for name in (
                "public-proof-v1", "history-report-v1", "dossier-v1")):
            raise VerifierTooOld("Unsupported signed JSON format")
    if kind == "tgwitness-account-loss-v1":
        shown, result = "account_loss", verify_account_loss(data, args.fingerprint)
        pinned = bool(args.fingerprint)
        notes.append("Account loss report: " + str(result["records"]) + " signed journal record(s) from "
                     + str((result["window"] or {}).get("from")) + "; Telegram ended the session at "
                     + str(result["loss"]["at"]) + " (" + str(result["loss"]["cause"]) + ")."
                     + (" The report reached its record limit." if result["truncated"] else ""))
    elif kind == "tgwitness-board-selection-v1":
        shown, result = "selection", verify_selection(args.bundle, args.fingerprint, args.evidence)
        pinned = bool(args.fingerprint)
        notes.append("Signed Case Board selection; exact records matched against the signed journal archive.")
    elif kind in {"tgwitness-case-board-v1", "tgwitness-case-board-disclosure-v1", "tgwitness-case-board-handover-v1"}:
        shown, result = "board", verify_board_document(args.bundle, args.fingerprint, args.evidence)
        pinned = bool(args.fingerprint)
        notes.append(result["meaning"])
    elif data.get("format") == "tgwitness-selection-v1":
        shown, result = "selection", verify_selection(args.bundle, args.fingerprint, args.evidence)
        pinned = bool(args.fingerprint)
        notes.append("The selection is unsigned. Its items match the verified archive; selection time and notes are not authenticated.")
    elif is_format(data.get("format"), REPORT_JSON):
        shown, result = "report", verify_report(args.bundle, args.fingerprint, args.evidence)
        pinned = bool(args.fingerprint)
    elif is_format(kind, "public-proof-v1"):
        shown = "proof"
        result = verify_public_proof(args.bundle, args.fingerprint, args.witness_fingerprint, args.evidence)
        pinned = bool(args.witness_fingerprint)
        if not pinned:
            notes.append("A public proof is signed by its witness: pass --witness-fingerprint to pin that key.")
    elif is_format(kind, "history-report-v1"):
        shown = "history"
        result = verify_history_report(args.bundle, args.fingerprint, args.evidence)
        pinned = bool(args.fingerprint)
        if not args.evidence:
            notes.append("History report signature only: pass --evidence to cross-check the journal and counts.")
    else:
        shown = "dossier"
        result = verify_dossier(args.bundle, args.fingerprint, args.evidence)
        pinned = bool(args.fingerprint)
    return CheckResult(shown, result, pinned, notes)


def verification_archive(args):
    notes = []
    pinned = bool(args.fingerprint or args.witness_fingerprint)
    if (archive_format := bundle_format(args.bundle)) in DISCLOSURE_FORMATS:
        if args.checkpoint or args.witness or args.tsa_ca or args.channel:
            raise ValueError("Journal checkpoint/witness/timestamp options do not apply to disclosure archives")
        shown = "account_disclosure"
        result = verify_account_disclosure(args.bundle, args.fingerprint, args.evidence)
        pinned = bool(args.fingerprint)
        notes.append(result["meaning"])
        if not result["source_reference_checked"]:
            notes.append("Source reference not checked: supply the original account archive with --evidence.")
    elif archive_format == "tgwitness-account-export-v1":
        if args.checkpoint or args.witness or args.tsa_ca or args.channel or args.evidence:
            raise ValueError("Journal checkpoint/witness/timestamp options do not apply to account export receipts")
        shown = "account"
        result = verify_account_export(args.bundle, args.fingerprint)
        pinned = bool(args.fingerprint)
        notes += account_export_lines(result)
    elif is_format(archive_format, "chat-export-v1"):
        shown = "chat"
        result = verify_chat_export(args.bundle, args.fingerprint)
        pinned = bool(args.fingerprint)
    elif is_format(archive_format, "handover-v1"):
        shown = "handover"
        result = verify_handover(args.bundle, args.fingerprint)
        pinned = bool(args.fingerprint)
        notes.append("Minimised records are authenticated by the signature over the original record's hash; "
                     "confirm their content against the complete journal by that hash.")
    elif is_format(archive_format, "witness-v1"):
        shown = "witness"
        result = verify_witness(args.bundle, args.witness_fingerprint or args.fingerprint, args.check_drand, args.check_bitcoin)
        if args.channel:
            result["channel_check"] = check_channel(result, args.channel)
        result.pop("statements")
    else:
        return verification_evidence(args)
    return CheckResult(shown, result, pinned, notes)


def verification_evidence(args):
    notes = []
    result = verify_bundle(args.bundle, args.fingerprint,
                           read_json_file(args.checkpoint) if args.checkpoint else None, args.tsa_ca,
                           args.check_drand, check_bitcoin=args.check_bitcoin)
    notes += coverage_lines(result["coverage"]) + outside_lines(result["outside"]) + tdx_lines(result.get("tdx"))
    pinned = bool(args.fingerprint)
    if any(a.get("kind") == "opentimestamps" and a.get("status") != "confirmed" for a in result.get("anchors", [])):
        notes.append("OpenTimestamps structure only: run ots verify to authenticate the Bitcoin timestamp.")
    if args.witness and not args.witness_fingerprint:
        notes.append("The witness key is not pinned: the witness journal is checked only against itself.")
    if args.witness:
        witness = verify_witness(args.witness, args.witness_fingerprint, args.check_drand, args.check_bitcoin)
        result["witness"] = cross_check_witness(witness, args.bundle, result)
        if args.channel:
            result["witness"]["channel_check"] = check_channel(witness, args.channel)
            result["witness"]["head_telegram_post_time"] = channel_head_time(result["witness"], result["witness"]["channel_check"])
        conflict = (result["witness"]["conflicts"] or [None])[0]
        if conflict and conflict["event_count"] > result["events"]:
            raise ValueError("The witness saw record " + str(conflict["event_count"]) + " at " + conflict["at"]
                             + ", before this export was created at " + str(result["witness"]["export_created_at"])
                             + ", but the export ends at record " + str(result["events"]))
        if conflict:
            raise ValueError("The journal differs from what the witness saw at " + conflict["at"] + " (record "
                             + str(conflict["event_count"]) + ")")
        broken = [a for a in result["witness"]["anomalies"] if a["status"] in ("fork", "rollback", "key_changed")]
        if broken:
            raise ValueError("The witness saw this journal " + broken[0]["status"].replace("_", " ") + " at "
                             + str(broken[0].get("at")) + " (record " + str(broken[0].get("event_count")) + ")")
        if result["witness"]["seen_after_export"]:
            notes.append("The witness saw record " + str(result["witness"]["seen_after_export"]["event_count"]) + " at "
                         + result["witness"]["seen_after_export"]["at"] + ", beyond this export's last record "
                         + str(result["events"]) + ".")
        notes += ["Witnessed from " + p["from"] + " to " + p["to"] for p in result["witness"]["witnessed"]]
        if not result["witness"]["consistent"]:
            notes.append("The witness has no answer signed by this export's key: nothing here is witnessed.")
        notes.append("Witness checkpoints match through record "
                     + str(result["witness"]["verified_through_event"]) + " of " + str(result["events"]) + ".")
        if result["witness"]["unwitnessed_events"]:
            notes.append(str(result["witness"]["unwitnessed_events"])
                         + " trailing record(s) have no matching witness checkpoint.")

        pinned = pinned or bool(args.witness_fingerprint and result["witness"]["consistent"])
    return CheckResult("evidence", result, pinned, notes)


REQUESTED_CHECKS = (("checkpoint", "--checkpoint"), ("witness", "--witness"), ("tsa_ca", "--tsa-ca"),
                    ("require_witness", "--require-witness"), ("sealed_attestation", "--sealed-attestation"),
                    ("channel", "--channel"), ("check_drand", "--check-drand"), ("check_bitcoin", "--check-bitcoin"))
APPLICABLE_CHECKS = {"evidence": {name for name, _ in REQUESTED_CHECKS},
                     "witness": {"channel", "check_drand", "check_bitcoin"}}


def refuse_inapplicable(args, kind):
    implied = getattr(args, "implied_checks", set())
    refused = [flag for name, flag in REQUESTED_CHECKS
               if getattr(args, name, None) and name not in implied and name not in APPLICABLE_CHECKS.get(kind, ())]
    if getattr(args, "evidence", None) and kind in ("evidence", "chat", "handover", "witness", "account", "distributed",
                                                    "attestation"):
        refused.append("--evidence")
    if getattr(args, "compare_fingerprint", None):
        refused.append("--compare-fingerprint without --compare")
    if getattr(args, "witness_fingerprint", None) and kind not in ("evidence", "witness", "proof"):
        refused.append("--witness-fingerprint")
    if kind == "evidence" and not getattr(args, "witness", None):
        refused += [flag + " without --witness" for name, flag in (("witness_fingerprint", "--witness-fingerprint"),
                                                                  ("channel", "--channel")) if getattr(args, name, None)]
    if refused:
        raise ValueError(", ".join(refused) + " cannot be checked against this " + kind
                         + " input; supply the archive and options that check it")


def verification_requirements(args, checked):
    result, notes, shown = checked.details, checked.notes, checked.kind
    refuse_inapplicable(args, shown)
    chronology = result.get("chronology")
    if chronology:
        notes.append("Observation time anomalies: " + str(chronology["regressions"]) + " backward step(s), "
                     + str(chronology["unparseable"]) + " unparseable timestamp(s). " + chronology["meaning"])
    if args.board and result.get("board"):
        notes.append("Case Board annotations: " + str(result["board"]["annotations_head"]["seq"]))
        notes.extend("Collection: " + item["title"] for item in result["board"]["collections"])
        notes.extend(item["message"] for item in result["board"]["slice_changes"])
        notes.extend("Dangling board target: " + item["id"] + " / " + item["event_hash"] for item in result["board"]["dangling"])
    check = result.get("channel_check") or (result.get("witness") or {}).get("channel_check")
    if check and (check["invalid_signatures"] or check["differ_from_journal"]):
        raise ValueError("Channel posts do not match the witness journal")
    if check and check["telegram_live_dates"]:
        notes.append("Channel post dates were read from Telegram at verification time; edited posts are not counted.")
    elif check and check["telegram_post_dates"]:
        notes.append("Channel dates are supplied metadata; witness signatures cover the post content.")
    if args.require_witness:
        witnessed = result.get("witness")
        if not witnessed:
            raise ValueError("--require-witness requires a full evidence ZIP and its witness journal")
        if not witnessed["witness_key_pinned"] or not witnessed["export_head_witnessed"]:
            raise ValueError("No pinned witness checkpoint matches the exported journal head; "
                             "retain a witness checkpoint at the export boundary")
        if witnessed["witness_fingerprint"] == result["fingerprint"]:
            raise ValueError("The collector and the witness must use different trusted signing keys")
        if check and (check["posted_but_not_found"] or not
                      set(check["matching_records"]).intersection(witnessed["export_head_witness_records"])):
            raise ValueError("Requested channel evidence is missing signed witness posts at the export boundary")
        result["witness_required"] = True
    if args.sealed_attestation:
        if shown != "evidence":
            raise ValueError("Runtime attestation requires a full evidence ZIP")
        try:
            from tgwitness.sealed_verify import verify as verify_runtime
        except ImportError:
            raise ValueError("Runtime verification needs the installed TgWitness sealed verifier and gh") from None
        checked_runtime = verify_runtime(args.bundle, args.sealed_attestation, args.sealed_repo,
                                         policy=args.sealed_policy, max_gib=args.max_gib)
        if checked_runtime["journal"]["fingerprint"] != result["fingerprint"]:
            raise ValueError("Runtime attestation names another collector key")
        result["runtime_attestation"] = {k: checked_runtime.get(k) for k in ("verified", "sha256", "workflow", "limitation", "attested_at")}
        result["runtime_attestation"]["key_origin"] = "created"
    result["assurance"] = assurance(result)
    if any(row["status"] == "fail" for row in result["assurance"]["ladder"]):
        raise ValueError("Assurance checks found contradictory witness evidence")
    result["evidence"] = evidence_conditions(result, shown)
    result["requested_checks_unavailable"] = requested_checks_unavailable(args, result)
    return checked


def verify_input(path, policy):
    args = argparse.Namespace(**{**vars(policy), "bundle": Path(path)})
    if args.bundle.is_dir():
        if (args.bundle / "manifest.sig").is_file() and (args.bundle / "verify.py").is_file():
            raise ValueError("This folder is an unpacked archive, and an unpacked copy is not checked. "
                             "Give the verifier the original ZIP file.")
        if args.checkpoint or args.witness or args.tsa_ca or args.channel or args.evidence:
            raise ValueError("Journal/report options do not apply to a distributed acquisition directory")
        result = verify_distributed_work(args.bundle, args.fingerprint, args.max_gib)
        checked = CheckResult("distributed", result, bool(args.fingerprint), [result["meaning"]])
    elif args.bundle.suffix.lower() in (".html", ".htm", ".pdf"):
        result = verify_report(args.bundle, args.fingerprint, args.evidence)
        checked = CheckResult("report", result, bool(args.fingerprint))
    elif args.bundle.suffix.lower() == ".json":
        checked = verification_json(args)
    else:
        checked = verification_archive(args)
    return verification_requirements(args, checked)


def verification_failure(args, parser, mode, console, exc):
    code = 3 if args.strict and isinstance(exc, VerifierTooOld) else 1
    if console:
        console.say("ASSURANCE: fail")
        console.failure(args.bundle, exc)
        raise SystemExit(code)
    if mode == "json":
        verification_print(json.dumps({"verified": False, "error": type(exc).__name__ + ": " + str(exc)}, indent=2))
        raise SystemExit(code)
    verification_print("ASSURANCE: fail")
    parser.exit(code, "VERIFICATION FAILED: " + type(exc).__name__ + ": " + safe_text(exc) + "\n")


def verification_output(args, checked, console, mode):
    shown, result, pinned, notes = checked.kind, checked.details, checked.signer_pinned, checked.notes
    evidence = result.setdefault("evidence", evidence_conditions(result, shown))
    unmet = bool(args.require_tier and ASSURANCE_TIERS.index(result["assurance"]["tier"]) < ASSURANCE_TIERS.index(args.require_tier))
    unpinned = args.strict and not pinned
    required = getattr(args, "require", None)
    profile_unmet = bool(required and EVIDENCE_PROFILES.index(evidence["profile"]) < EVIDENCE_PROFILES.index(required))
    unavailable = result.get("requested_checks_unavailable") or []
    if unmet:
        notes.append("Required assurance tier was not reached: " + args.require_tier)
    if profile_unmet:
        notes.append("Required evidence profile was not reached: " + required)
    notes += ["Requested check not performed: " + item for item in unavailable]
    failed = unmet or unpinned or profile_unmet or bool(unavailable)
    if console:
        console.show(shown, args.bundle, result, notes)
        if failed:
            raise SystemExit(2)
        return
    if mode == "json":
        verification_print(json.dumps({"verified": True, "kind": shown, "signer_pinned": pinned, "notes": notes, "result": result,
                          "evidence_profile": evidence["profile"], "requirements_met": not failed},
                         indent=2, ensure_ascii=True))
        if failed:
            raise SystemExit(2)
        return
    verification_print(evidence_line(evidence))
    for row in evidence["conditions"]:
        verification_print("  [" + row["status"] + "] " + CONDITION_LABELS[row["id"]] + " (" + row["role"].replace("_", " ")
                           + "): " + row["detail"] + ("" if row["status"] == "met" else " · " + row["how"]))
    for line in next_lines(evidence):
        verification_print(line)
    if shown == "evidence":
        verification_print("What changing this archive would take:")
        for line in forgery_lines(result):
            verification_print("  - " + line)
    verification_print(json.dumps(result, indent=2))
    verification_print(producer_line(result.get("producer")))
    seal = result.get("report_seal")
    if seal:
        verification_print("Report seal verified: " + ("chat.html" if shown == "chat" else "report.html" if shown == "evidence"
                                          else args.bundle.name) + ", language " + str(seal["language"]) + ".")
    if result.get("report_json"):
        verification_print("JSON report seal verified: report.json.")
    pdf = result.get("report_pdf") or (result if result.get("pdf_signature") else None)
    if pdf:
        verification_print("PDF signature and Ed25519 seal verified: " + str(pdf.get("file") or args.bundle.name)
              + " (certificate " + pdf["pdf_signature"]["certificate"] + ").")
    if result.get("report_parts"):
        verification_print("Report parts verified: " + str(result["report_parts"]) + ", each sealed over this export.")
    ids = result.get("message_ids")
    if ids and ids["numbered_per_chat"]:
        verification_print("Message IDs " + str(ids["first_id"]) + "-" + str(ids["last_id"]) + ": " + str(ids["present"])
              + " present, " + str(ids["missing"]) + " absent in " + str(ids["missing_ranges"])
              + " range(s); message-ids.json matches chat.json.")
    changes = result.get("journal_changes")
    if changes:
        verification_print("Journal records of deletions and earlier versions: " + str(changes["records"]) + " for "
                           + str(changes["messages"]) + " message(s); each hash and signature checked.")
    if result.get("sha256sums"):
        verification_print("SHA256SUMS matches the signed manifest.")
    for line in notes:
        verification_print(line)
    verification_print("Integrity verified. " + evidence_line(evidence)[len("EVIDENCE: "):].capitalize() + ".")
    if failed:
        raise SystemExit(2)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "unseal-password":
        return password_command(argv[1:])
    parser = verification_parser()
    args = verification_arguments(parser, argv)
    if args.interactive:
        verification_interactive(args, parser)
    if not args.bundle:
        parser.error("bundle is required (or use --interactive)")
    args.bundle = Path(args.bundle)
    if args.require_witness and (not args.witness or not args.witness_fingerprint):
        parser.error("--require-witness requires --witness and --witness-fingerprint")
    globals()["MAX_UNCOMPRESSED_GIB"] = max(1, args.max_gib)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    mode = "json" if args.json else "pretty" if args.pretty or (not args.plain and sys.stdout.isatty()) else "plain"
    if args.compare:
        return verification_comparison(args, parser, mode)
    console = Console(sys.stdout, console_language(args.lang),
                      mode == "pretty" and not args.no_color and not os.environ.get("NO_COLOR"), args.explain) \
        if mode == "pretty" or args.explain and mode == "plain" else None
    spinner = console.spinner() if console else None
    if spinner:
        spinner.__enter__()
    try:
        checked = verify_input(args.bundle, args)
    except Exception as exc:
        if spinner:
            spinner.__exit__(None, None, None)
        verification_failure(args, parser, mode, console, exc)
    if spinner:
        spinner.__exit__(None, None, None)
    return verification_output(args, checked, console, mode)


if __name__ == "__main__":
    main()
