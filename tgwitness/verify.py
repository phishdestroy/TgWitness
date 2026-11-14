# TgWitness verifier sources SHA-256: 1b24dc88fae592bc3718c259c0417e39ab7255fe96af904d1280c4c8b3243b24
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
# Catalogue SHA-256: e2246ee877684d8d65768a7dd719a3e34fab923e72e777dbf347669cb64933c2
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
    windows = {"english": "en", "russian": "ru", "ukrainian": "uk", "spanish": "es",
               "portuguese": "pt", "turkish": "tr", "arabic": "ar", "persian": "fa", "urdu": "ur",
               "hindi": "hi", "indonesian": "id", "vietnamese": "vi", "chinese": "zh", "french": "fr",
               "german": "de", "italian": "it", "uzbek": "uz", "korean": "ko", "chinese (traditional)": "zh-Hant",
               "malay": "ms", "polish": "pl", "japanese": "ja", "thai": "th", "hebrew": "he", "bengali": "bn"}
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
    print("\n" + " / ".join(VERIFIER_LANGUAGES[c]["words"]["Language"] for c in ("en", "zh", "ar", "ru")))
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
