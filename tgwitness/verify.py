# TgWitness verifier sources SHA-256: eaadde1c664a2354f3fa586ae274bd021609c570a650ff3f6c8748ee6322cc04
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
import zlib
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


PARALLEL = {"jobs": 1, "executor": None}
PARALLEL_JOBS_LIMIT = 16
PARALLEL_EVENTS_AFTER = 5000
PARALLEL_EVENT_BATCH = 2000
PARALLEL_HASH_BYTES = 64 * 1024**2


def parallel_jobs(value=None):
    if value is not None:
        jobs = (os.cpu_count() or 1) if value == "auto" else int(value)
        if jobs < 1:
            raise ValueError("--jobs needs a positive number or auto")
        PARALLEL["jobs"] = min(jobs, PARALLEL_JOBS_LIMIT)
    return PARALLEL["jobs"]


def parallel_pool():
    if PARALLEL["jobs"] < 2:
        return None
    if PARALLEL["executor"] is None:
        import concurrent.futures
        import multiprocessing
        PARALLEL["executor"] = concurrent.futures.ProcessPoolExecutor(
            PARALLEL["jobs"], mp_context=multiprocessing.get_context("spawn"))
    return PARALLEL["executor"]


def parallel_shutdown():
    executor, PARALLEL["executor"] = PARALLEL["executor"], None
    if executor is not None:
        executor.shutdown(wait=True, cancel_futures=True)


def journal_batch(public_key, first, lines):
    key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key, validate=True))
    for seq, line in enumerate(lines, first):
        try:
            event = strict_json(line)
            calculated = hashlib.sha256(canonical({k: event[k] for k in FIELDS})).hexdigest()
        except (ValueError, KeyError, TypeError):
            return seq, "content"
        if event["hash"] != calculated:
            return seq, "content"
        try:
            key.verify(base64.b64decode(event["signature"], validate=True), bytes.fromhex(calculated))
        except (InvalidSignature, ValueError, TypeError):
            return seq, "signature"
    return None


def journal_failure(found):
    seq, reason = found
    if reason == "signature":
        raise InvalidSignature("Invalid signature at event " + str(seq))
    raise ValueError("Changed content at event " + str(seq))


class JournalChecks:
    def __init__(self, public_key):
        self.public_key, self.pending, self.first, self.lines = public_key, [], None, []
        self.pool = parallel_pool()

    def add(self, seq, line):
        if not self.lines:
            self.first = seq
        self.lines.append(line)
        if len(self.lines) >= PARALLEL_EVENT_BATCH:
            self.submit()

    def submit(self):
        if self.lines:
            self.pending.append(self.pool.submit(journal_batch, self.public_key, self.first, self.lines))
            self.lines = []
        while len(self.pending) > 3 * PARALLEL["jobs"]:
            found = self.pending.pop(0).result()
            if found:
                self.abandon()
                journal_failure(found)

    def settle(self):
        self.submit()
        pending, self.pending = self.pending, []
        for index, future in enumerate(pending):
            found = future.result()
            if found:
                for rest in pending[index + 1:]:
                    rest.cancel()
                journal_failure(found)

    def abandon(self):
        for future in self.pending:
            future.cancel()
        self.pending, self.lines = [], []


def member_hashes(path, names):
    found = {}
    with zipfile.ZipFile(path) as archive:
        for name in names:
            digest = hashlib.sha256()
            with archive.open(name) as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            found[name] = digest.hexdigest()
    return found


class MemberHashes:
    def __init__(self, archive, path, names):
        self.archive, self.names, self.futures = archive, list(names), []
        sizes = {info.filename: info.compress_size for info in archive.infolist()}
        pool = parallel_pool() if isinstance(path, (str, os.PathLike)) else None
        if pool is None or len(self.names) < 2 or sum(sizes.get(n, 0) for n in self.names) < PARALLEL_HASH_BYTES:
            return
        buckets = [[0, []] for _ in range(2 * PARALLEL["jobs"])]
        for name in sorted(self.names, key=lambda n: -sizes.get(n, 0)):
            bucket = min(buckets, key=lambda b: b[0])
            bucket[0] += sizes.get(name, 0) + 4096
            bucket[1].append(name)
        self.futures = [pool.submit(member_hashes, os.fspath(path), names) for _, names in buckets if names]

    def result(self):
        if not self.futures:
            return {name: member_digest(self.archive, name) for name in self.names}
        found = {}
        for future in self.futures:
            found.update(future.result())
        self.futures = []
        return found

    def cancel(self):
        for future in self.futures:
            future.cancel()
        self.futures = []
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


class EventChain:
    def __init__(self, public_key, remember=None):
        self.public_key, self.remember, self.checks = public_key, remember, None
        self.key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key, validate=True))
        self.previous, self.count = "0" * 64, 0
        self.previous_time = self.previous_at = None
        self.chronology = {"regressions": 0, "unparseable": 0, "samples": []}

    def structure(self, event):
        count = self.count + 1
        if set(event) != set(FIELDS) | {"hash", "signature"}:
            raise ValueError("Unexpected or missing fields at event " + str(count))
        if event["seq"] != count or event["previous_hash"] != self.previous:
            raise ValueError("Broken sequence or hash chain at event " + str(count))

    def content(self, event):
        calculated = hashlib.sha256(canonical({k: event[k] for k in FIELDS})).hexdigest()
        if event["hash"] != calculated:
            raise ValueError("Changed content at event " + str(self.count + 1))
        self.key.verify(base64.b64decode(event["signature"], validate=True), bytes.fromhex(calculated))
        return calculated

    def settle(self, event, digest):
        count, chronology, anomaly = self.count + 1, self.chronology, None
        try:
            observed = parse_time(event["observed_at"])
            if observed.utcoffset() is None:
                raise ValueError("Observation time has no UTC offset")
        except (AttributeError, TypeError, ValueError, OverflowError):
            observed = None
            chronology["unparseable"] += 1
            anomaly = {"seq": count, "observed_at": event["observed_at"], "reason": "unparseable"}
        if observed is not None and self.previous_time is not None and observed < self.previous_time:
            chronology["regressions"] += 1
            anomaly = {"seq": count, "observed_at": event["observed_at"], "previous_at": self.previous_at,
                       "backwards_seconds": (self.previous_time - observed).total_seconds(), "reason": "regression"}
        if anomaly is not None and len(chronology["samples"]) < 100:
            chronology["samples"].append(anomaly)
        if observed is not None:
            self.previous_time, self.previous_at = observed, event["observed_at"]
        if event["kind"] == "media.hashed":
            payload = event["payload"]
            validate_server_hashes(payload.get("server_hashes"))
            if (payload["server_hashes"]["status"] != "complete" or payload.get("downloaded_bytes") != 0
                    or payload.get("media_sha256") is not None):
                raise ValueError("A hash-only record incorrectly claims downloaded file content")
        self.previous, self.count = digest, count
        if self.remember is not None and count in self.remember:
            self.remember[count] = digest

    def run(self, events):
        for event in events:
            self.structure(event)
            self.settle(event, self.content(event))
        return self.result()

    def run_lines(self, lines, take=None):
        for line in lines:
            event = strict_json(line)
            try:
                if take is not None:
                    take(event)
                if self.checks is None and self.count >= PARALLEL_EVENTS_AFTER and parallel_pool() is not None:
                    self.checks = JournalChecks(self.public_key)
                self.structure(event)
                if self.checks is None:
                    digest = self.content(event)
                else:
                    self.checks.add(self.count + 1, line)
                    digest = event["hash"]
                self.settle(event, digest)
            except Exception:
                if self.checks is not None:
                    self.checks.settle()
                raise
        if self.checks is not None:
            self.checks.settle()
        return self.result()

    def result(self):
        result = {"events": self.count, "head_hash": self.previous, "fingerprint": fingerprint(self.public_key)}
        if self.chronology["regressions"] or self.chronology["unparseable"]:
            self.chronology["meaning"] = ("Observation times come from the collector's clock; the hash chain fixes the "
                                          "order of the records, and timestamps, drand rounds and witness records fix "
                                          "them in time. These entries do not affect the signatures.")
            result["chronology"] = self.chronology
        return result


def verify_events(events, public_key, remember=None):
    return EventChain(public_key, remember).run(events)


def verify_event_lines(lines, public_key, take=None, remember=None):
    return EventChain(public_key, remember).run_lines(lines, take)


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
        hashing = MemberHashes(archive, path, manifest["files"])

        def hashes_match():
            found = hashing.result()
            for name, digest in manifest["files"].items():
                if found[name] != digest:
                    raise ValueError("File hash mismatch: " + name)
        if not hashing.futures:
            hashes_match()
        try:
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

            def take(event):
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
            known = anchored_counts(archive, checkpoint)
            with archive.open("events.jsonl") as stream:
                result = verify_event_lines(bounded_lines(io.BufferedReader(stream, 1024 * 1024)), public, take, known)
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
        except Exception:
            if hashing.futures:
                hashes_match()
            raise
        except BaseException:
            hashing.cancel()
            raise
        if hashing.futures:
            hashes_match()
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
            if known.get(seq):
                return known[seq]
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


def anchored_counts(archive, checkpoint):
    statements, wanted = [checkpoint] if isinstance(checkpoint, dict) else [], {}
    for name in archive.namelist():
        if name.startswith("anchors/") and name.endswith(".json"):
            try:
                statements.append(strict_json(read_member(archive, name)))
            except ValueError:
                continue
    for value in statements:
        statement = value.get("statement") if isinstance(value, dict) else None
        count = statement.get("event_count") if isinstance(statement, dict) else None
        if type(count) is int and count > 0:
            wanted[count] = None
    return wanted
DISTRIBUTED_PAGE_FORMATS = ("tgwitness-distributed-pages-v1", "tgwitness-distributed-pages-v2")


def verify_distributed_pages(stream, envelopes, job, task):
    format_name = job.get("checkpoint_format")
    if format_name not in DISTRIBUTED_PAGE_FORMATS:
        raise ValueError("Unsupported distributed checkpoint format.")
    handovers = format_name == DISTRIBUTED_PAGE_FORMATS[1]
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
        changed = state["profile_id"] not in (None, profile)
        handover = value.get("handover_from") if handovers else None
        if (not worker or profile not in eligible or envelope["public_key"] != worker["public_key"]
                or (handover != state["profile_id"] if changed else handover is not None)
                or not handovers and "handover_from" in value):
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
                    or not changed and state["transport_generation"] is not None
                    and generation < state["transport_generation"])
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
            or job.get("checkpoint_format") not in DISTRIBUTED_PAGE_FORMATS
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
        hashing = MemberHashes(archive, path, manifest["files"])

        def hashes_match():
            found = hashing.result()
            for name, digest in manifest["files"].items():
                if found[name] != digest:
                    raise ValueError("File hash mismatch: " + name)
        if not hashing.futures:
            hashes_match()
        try:
            parts = verify_parts(archive, manifest) if manifest.get("parts") else None
            numbers = set()
            attachments = check_attachments(archive, manifest, numbers)
            sums = check_sums(archive, manifest)

            def describes(subject):
                return (subject.get("chat_id") == (manifest.get("chat") or {}).get("id")
                        and subject.get("message_count") == manifest.get("message_count")
                        and subject.get("chat_json_sha256") == manifest["files"].get("chat.json"))
            seal = archive_seal(archive, "chat.html", public) if "chat.html" in manifest["files"] else None
            if seal and not describes(seal["subject"]):
                raise ValueError("The report seal describes a different chat export")
            companions = report_companions(archive, manifest, public, describes)
            ids = check_message_ids(archive, manifest, numbers) if "message-ids.json" in manifest["files"] else None
            journal = (check_journal_changes(archive, manifest, public) if "journal-changes.jsonl" in manifest["files"]
                       else None)
        except Exception:
            if hashing.futures:
                hashes_match()
            raise
        except BaseException:
            hashing.cancel()
            raise
        if hashing.futures:
            hashes_match()
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


def check_message_ids(archive, manifest, numbers=None):
    claimed = strict_json(read_member(archive, "message-ids.json", MAX_JSON_BYTES))
    ids = sorted(numbers if numbers is not None else {m["id"] for m in chat_messages(archive) if type(m.get("id")) is int})
    counted = message_id_summary((manifest.get("chat") or {}).get("id"), ids)
    if {k: claimed.get(k) for k in counted} != counted:
        raise ValueError("message-ids.json disagrees with the messages in chat.json")
    return {k: counted[k] for k in ("first_id", "last_id", "present", "missing")} | {
        "missing_ranges": len(counted["missing_ranges"]), "numbered_per_chat": counted["numbered_per_chat"]}


def handover_proofs(archive, journal, hashes, count, head):
    root, proven, head_proven = hash_bytes(journal.get("merkle_root")), set(), False
    with archive.open("proofs.jsonl") as stream:
        for line in bounded_lines(stream):
            proof = strict_json(line)
            seq = proof.get("seq") if isinstance(proof, dict) else None
            if type(seq) is not int or not 1 <= seq <= count or seq in proven and not proof.get("head"):
                raise ValueError("Malformed Merkle proof in proofs.jsonl")
            if proof.get("head") is True:
                if seq != count:
                    raise ValueError("The journal head proof names another record")
                verify_inclusion(head, count - 1, count, root, proof.get("path"))
                head_proven = True
                continue
            if seq not in hashes:
                raise ValueError("A Merkle proof names a record that is not in this extract: " + str(seq))
            verify_inclusion(hashes[seq], seq - 1, count, root, proof.get("path"))
            proven.add(seq)
    if proven != set(hashes) or not head_proven:
        raise ValueError("Every record and the journal head need a Merkle proof")
    return len(proven)


def handover_range(records, chosen):
    if not chosen:
        return None
    chat, low, high = chosen
    numbers = sorted({r["message_id"] for r in records if r["chat_id"] == chat and type(r["message_id"]) is int
                      and low <= r["message_id"] <= high})
    if not numbers:
        raise ValueError("No record of chat " + str(chat) + " with message numbers " + str(low) + "-" + str(high)
                         + " is in this extract")
    return {"chat_id": chat, "from": low, "to": high, "messages": len(numbers), "message_ids": numbers[:1000],
            "records": sum(1 for r in records if r["chat_id"] == chat and type(r["message_id"]) is int
                           and low <= r["message_id"] <= high)}


def verify_handover(path, expected_fingerprint=None, chosen=None):
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
        counts, previous, referenced, hashes, located = {"unchanged": 0, "minimised": 0}, None, set(), {}, []
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
                hashes[seq] = record["hash"]
                located.append({"chat_id": record["chat_id"], "message_id": record["message_id"]})
                previous = record
        if counts != {k: manifest["counts"].get(k) for k in counts}:
            raise ValueError("Record counts differ from the signed manifest")
        if {name for name in files if name.startswith("media/")} - referenced:
            raise ValueError("The extract carries an attachment no record refers to")
        if "proofs.jsonl" in files:
            proven = handover_proofs(archive, journal, hashes, count, head)
        elif "merkle_root" in journal:
            raise ValueError("The extract names a Merkle root but carries no proofs")
        else:
            proven = None
        selected = handover_range(located, chosen)
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
            "records_proven": proven, "merkle_root": journal.get("merkle_root") if proven is not None else None,
            "range": selected,
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
def check_attachments(archive, manifest, numbers=None):
    files = manifest["files"]
    for name, digest in files.items():
        if name.startswith("media/") and name[len("media/"):] != digest:
            raise ValueError("Attachment name differs from its SHA-256: " + name)
    referenced, hash_files, count, numbers = 0, set(), 0, set() if numbers is None else numbers
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
# Catalogue SHA-256: fcfb094c7a71eb7314ddcc51ab814a93cb7d9040769011fbb6e960769a8a1c5e
VERIFIER_LANGUAGE_DATA = (
    "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"
)
# END GENERATED VERIFIER LANGUAGES
VERIFIER_LANGUAGES = json.loads(zlib.decompress(base64.b64decode(VERIFIER_LANGUAGE_DATA)))
SAY = {code: entry["words"] for code, entry in VERIFIER_LANGUAGES.items()}


WINDOW_WORDS = {"updates_diverted": "Updates went to another session",
                "session_revoked_externally": "Session revoked externally"}
KINDS = {"evidence": "Evidence archive", "chat": "Chat export", "account": "Account export",
         "account_disclosure": "Account disclosure", "witness": "Witness journal",
         "dossier": "People profiles", "proof": "Public proof", "report": "Sealed report",
         "history": "History report", "handover": "Handover extract", "selection": "Viewer selection",
         "distributed": "Distributed acquisition", "board": "Case Board", "attestation": "Collector attestation",
         "live": "Live chat export"}
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
        elif shown == "live":
            salvaged = result.get("salvaged")
            self.check("warn" if salvaged else "ok", "Manifest signature",
                       self.t("not used: the archive was not closed") if salvaged else self.t("Ed25519 · valid"))
            self.check("ok", "File hashes", self.t("{n} files · SHA-256 match", n=self.number(result["files_checked"])))
            self.check("ok", "Messages", self.t("{n} messages · {title}", n=self.number(result.get("message_count")),
                                                title=(result.get("chat") or {}).get("title") or "?"))
            self.check("ok", "Page seals", self.t("{n} pages signed in order", n=self.number(result["pages"])))
            if salvaged:
                self.check("warn", "Unsealed tail", self.t("{n} bytes after the last seal were not checked",
                                                          n=self.number(salvaged["unsealed_bytes"])))
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
            if result.get("records_proven") is not None:
                root = str(result.get("merkle_root") or "")
                self.check("ok", "Record chain", self.t("{n} records · head {hash}", n=self.number(result["records_proven"]),
                                                        hash=root[:8] + "…" + root[-8:]))
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
    command = [str(path), "--pretty", "--explain", "--lang", lang, "--max-gib", str(args.max_gib), "--jobs", str(args.jobs)]
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
    parser.add_argument("--range", metavar="CHAT:FROM-TO",
                        help="With a handover extract: confirm that messages FROM to TO of chat CHAT are in it, "
                             "each checked (write --range=-100123:10-20 for a negative chat ID)")
    parser.add_argument("--jobs", default="auto",
                        help="Processes that check a large archive together: a number, or auto for one per CPU "
                             "(at most 16). 1 checks everything in this process.")
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
        result = verify_handover(args.bundle, args.fingerprint, chosen_range(args.range))
        pinned = bool(args.fingerprint)
        notes.append("Minimised records are authenticated by the signature over the original record's hash; "
                     "confirm their content against the complete journal by that hash.")
        if result["records_proven"] is not None:
            notes.append("Merkle proofs: each of the " + str(result["records_proven"]) + " records belongs to the journal of "
                         + str(result["journal_events"]) + " records with root " + str(result["merkle_root"])[:16] + "…")
        if result["range"]:
            notes.append("Range " + str(result["range"]["chat_id"]) + ":" + str(result["range"]["from"]) + "-"
                         + str(result["range"]["to"]) + ": " + str(result["range"]["records"]) + " record(s) for "
                         + str(result["range"]["messages"]) + " message(s) in this extract, each checked.")
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
                                                    "attestation", "live"):
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


def chosen_range(value):
    if not value:
        return None
    match = re.fullmatch(r"(-?\d{1,20}):(\d{1,12})-(\d{1,12})", value.strip())
    if not match or int(match[2]) > int(match[3]):
        raise ValueError("--range needs CHAT:FROM-TO, for example --range=-1001234567890:100-200")
    return int(match[1]), int(match[2]), int(match[3])


def verification_requirements(args, checked):
    result, notes, shown = checked.details, checked.notes, checked.kind
    refuse_inapplicable(args, shown)
    if getattr(args, "range", None) and shown != "handover":
        raise ValueError("--range checks messages in a handover extract; give the extract instead")
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
    elif live_archive(args.bundle):
        if args.checkpoint or args.witness or args.tsa_ca or args.channel or args.evidence:
            raise ValueError("Journal/report options do not apply to a live chat export")
        result = verify_live_export(args.bundle, args.fingerprint, args.max_gib)
        notes = [result["meaning"]]
        if result["salvaged"]:
            notes.append("This archive was not closed: pages up to its last seal were checked; "
                         + str(result["salvaged"]["unsealed_bytes"]) + " bytes after that seal were not.")
        checked = CheckResult("live", result, bool(args.fingerprint), notes)
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
    try:
        parallel_jobs(args.jobs)
    except ValueError:
        parser.error("--jobs needs a positive number or auto")
    try:
        return verification_main(args, parser)
    finally:
        parallel_shutdown()


def verification_main(args, parser):
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
