# TgWitness verifier sources SHA-256: 781f7205b40c9de2a7b270355cf23d98c44957a2db3c642f2f93b11958f2d319
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
        parser.exit(1, "Could not decrypt the export: " + type(exc).__name__ + "\n")
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
# Catalogue SHA-256: ad4f01a5dc6b4a91a0ba3c2702c7234febe07c42620716ab3c450f5e1dbe5379
VERIFIER_LANGUAGE_DATA = (
    "eNrkvetzHNd1L/qvdCEfLN87hI+cxFUX+ASRkMTiAwwB+Zzki6uBaQJtzExD0zOQQJVuSWIsWSVFtB2ZchxLsuKb6Dg5qgM+IIIkCFZ55O/gv+C/"
    "5K7nfvXueQADWfKpssXBTPfu3Xuvvd7rt16byTozc6/NdNJ2NjM3s9hZb+Xlxkxj5pWi2yzxl+V8vZN14Tf50Jg5u5GtbcJv+qExczHfzpJutgb3"
    "5J31JO00k2a2na9leNWQHxsz/z3vdbKyTH5c9LudtAWXh980Zq5kxVYrS7a6xbW8RUOG38A1/dVWvobfFNfwAvfPxsxylrayJkxiq+j28FW8vxsz"
    "L+Zlr+ju2AuCLxozP8yzV7JuUmatbK2XF7Bm1a8aM+d7WRvnx/82Zi6lnfxaVvaSEtYu7fW7uMaRL8062PeH785l5Vo3X4WJpt21DVhF+LX6nb2u"
    "dH7H+5dhBddw6a9l3ayzhrdXvoLdTLdwDrhDWb7Vo30Nv8JndPPtVN7c+QPeMe/k7byk5Vxjool815i5Sp+StY00xzG8PxszC2trRb/TS5p5udYq"
    "Sl6pyJcwE9gaeMN+D9dg7eV+XuY6rZpf8Nm4jbBVRGHuX0LNSJhmO8pGspGWG1lJtNrbUOo1c5/4lsZMp+gBNWZlBq/zTNFqAuFkr+I0vgvjDfmx"
    "MdNOe2s4MA6Kz4OXawsFwa3DfuWnlv2trVYO3z9z5gwcuyZuuz40/ltjxrwXzx8u6BXJDtBOAgcKHzviAncEfM4aLljWnEvSZjM5c6ZXpmfWUm+Y"
    "+qt4LFzttazby6/la2mPr+9m28Um7nWZFNeS13p5O3s9eea1kmj89e/K+Me5M/5Mc1dPbmkk6bUebBYuPn6RlL20vTV6CscYqDGDN63RoeOFSq6l"
    "wPtgtV7rZmlZdF6Hh42+xhvHWfTkmU6RLJ1dvvK9s1cvJnmHpiIs5rv+yGPf1ZjZyjrI8+eSbr+TFL0y6W+td9Nm1sAL+Ztt4CXXduAJ41/bmHku"
    "760V8Li01wNC52nJAZo395uRJ7m6MdPvbHaKV/yreztb2Ty8OF+FB0bHxN2izYLnHPfOxszlAhavmeESIA8wP5Vz/DlZK4AornWLNq3wWtFCmVN0"
    "vwO/tIq1zVl4+snHACm3ePX88+fPLqycX7qcPL9w/uLiORR0kW8bpA4w70tW4cFJmW7D263u9JAbFfCMvPQespntzIoWMfFtjRmYPEh8ODuv5HBJ"
    "R6Qu3FmuFVsoK0ZcALSYwgFMW4HMiH1L+1Gslll3W4gF9q5QWZY1ZbWHXtGYeSFFmsD/wnj99mrWLeno8G1ZEweJfY2yFrWjBBSxHglb+1djZqmb"
    "r+egFiW9bG2jA+ykBcpUD045it0hPzZmViI3rESue4mpGH7VT7ge9Mrw6e9Jy/h70i8uW0ZAP9u/+DeVLvKj+RP0xbSz3k/Xcd/Mx8bM80Cb8A39"
    "A/PFZ67gM8/1u0bz0I8o05GjkTinDyDJUVlA8Uz/qsZBzzcf8arOtbzbpq/tZ3zvNecX9y/U40jKkvLGn4D+hfCWhb6eF930edFIrxpt6KrRgS6B"
    "YgfvSgPpR6P7lFbjKWU8GQ5XY4ceRv/AX+Zw43f2D3w7YDS8suYj6nglfYP/0N7QFPhfpDelh3OGCpYdhXXZ0VNhXTZgxzxtr/od7HB2DWi6j9th"
    "PuK8e/RS/C/PKzl/TqaGnxozi6+m7ZwtDvMR6X4d1JrrSgfen6D9d4tmf434CCr/zl8wnug1jhJd+Qq1QBDGrHSRgmf/srqp+Tn4AuwH0PpwteGb"
    "XjddIwsi/Ere9rki7Tb1hfkPWO1eynYJ/Yu7yMyMdlE+8q7LfvOMcc15tvQJ3rXbLWjh6F+YOb9fsvziwpnv/+0PcOrBN/DslJkR/wt0RyoDUh5/"
    "MO9vX1zWq5SVYspu5imRNf4rWvUWyLme6sv8h1olxhbB3Yty5itRzrzkMN0SV4umGvsWx+2X9LN8wHUutrb4beUT2Gwd0Ly6/S0eyf2LbA1gAx0S"
    "JGxg2D9l14DMWIfT7bNf4BnugDXNq6kfYR/X1cYVpQC3LPIln0IYbwVkGehC7UR19OQP95PF5vf/9m+f/X/wo93eCW8AirFfbqetHGda+Yp5kRg4"
    "wpL0L5jjiwsw1PJLl5bx+faPxsxrndcTss+dRyZksMCVQ37kO4WX4M8bWQqLik98Xe6s+ZHvbAtrxV9hK4DV6G2xX/ielCn7mfK7akaBkpR39Y6k"
    "i0eslGHGvBhHTtGygKcB7QMTwE8tEXjJa/iJZzb6KtCAzCEqeZ3god2iv76hpuZr6etkzazimJNcDRS5QXoTkV+ZvmKuwXe1NspqtlOQdQsqGrM+"
    "0M9aadkz19OyvI760bRHbMwYBRotbM/sZat++O/u+iV/9VrHXyP+pjHzpzf+g24nWilI+FW+YnpBwgOSa1gXAF1F1rCjFI19qRnVXkTSA1+gULXO"
    "+BSC4Se4xz9bZPwWvbT1uhpv1g833nWoEcgZMI6w+STvZW3Q4oGXwtryXsC+rMMLw9Y6rgorkqcxiuGXVra6w2Wv4tnSV4qNZ6czpYEaM/KJKIC3"
    "XW0btGycrRzzQrLf8+wV5J0gqdSh2s2aKc3OXx/29tnXOv69jZkLMIt2Xir/9v4UCbFmVBLvT0ebdEeIfCnaSAIaUwf9mFs9VUzcr1BHzMHYKJqk"
    "zJnPpNs3SVMok2uwcCr9WNOP/sLyf72b93ZE+vNnoSVafOP7pj/w6bB6ZGaxQub/zdxUtxMYW9+ox2WOotizvpWG855yzePcyc9UVxPSS14GV+OX"
    "4pfMt3I8UV1U9jtszp7o9urTX0nBiO9mKSpDQFGw1nwsyDGSGdpGmuv2O7EJTDoCngtidKFLlvlsw3hFieSvefrMce9szJw5cw0mnHW3uihE0PMQ"
    "LJv7c3z54PnTGAXnUlJU44zrfqLBzC9bRStf26EDkCYv5L0X+6vJwhqfCljF+QTpv5WsnPsfc8nWTm8DBjjTTnrrIshn11pFv2n9al/3E0F2CdM1"
    "kqmRvEZKpOiSKLZGXeL6ppnPsoAx5DD0Z/RE6ba85uzL66gnkGcU7LUUWCovRGp2yN1EcledfJTGDClOyjDQ1Zispd1unqFLSUV04qiC87KUREXG"
    "NrAyf7rj6Zksk2f/9MY/vyYK6OsgP3M6w6s71nQa90qgAVYJrYOTo3yojBunLju/YVJtpUcOJoBaBJ/p1zOr7IdFkpnyiBh3QbPfCgUelVQnu8AU"
    "gxnnusZMs0uCGqbZRO+oOKZoWbpZK90pcQnHuMhQL/HNtGNc9spWXym6m9daxSvJa/rpdUusk9wEUvKH588tXj67OAfivZO3+20wj8i0kaht8pp8"
    "wCdMcDG+g75b6cro6NfoG8JYJWkjPWAGq+jsx4WicHTa3UnWYcm2wErZSFGB7mRq3p15BaVOh3y0cOpmk/NwLuH1V0FhyVKMRsIgnRbIqg2c4Ssb"
    "RSs7I/e68gl2ErVG2lI9Q8BN8EiVfTDM2Hc8S46rb8lUo6vaqMxTY6HyJLDtMDxijPBeuqmTLm1gokwx/pW93EdeAkZTQd/Ka7SRFXeyDCg8Zc++"
    "8bljMA+0pFafswxaLbRazIEt+uiuw1+zJk+6ZsG/dW8RO2koQuQAgW5dUljtNTSnyvhhG3Z9Y2YhrnShP7DmF/R+v9zPu/SLKt7kCa9+25i5dP7y"
    "+UsvXUqeX7qa6NySS4sr6E6s+6n+LnyJhZWVxeWVxXPJ2aWLFxfPUuDq6kuXhww47C77LLzwpSvJylJydfHs0tVziRVVS8+riew8ZbzrwQa5vLL4"
    "wtXzK3+fLF2++Pc4l+g8Ly+tyLpMeENj5jLImQS2aovjqyy2Z7d22OZjmfZasUVbgm8w2fW+X5a5RBn4ZfVb/9r1dCu8kL5qzJAbiJ1CJrIQVR3G"
    "vJCkco39YOLZG1lX5PJYV9ZJuf4WxjLVh2X23HGjkIsPQ/6q+CA7AG6AMVE4frUi8eQjN2ZEfof6WvIP56/MjVCVjn3ryKeOaUqMnsO4A9ncM/o5"
    "7zFfZ12i9ifkbKKKr7khjti3jZnl/haSJbJyY41Qsk/a7Qlj191FJ8MEVwNXRjENRIC/7qi+h2Z72hPzEQ6tjcm5J4IEVI9sazwbKAmnORrOrcyQ"
    "xZMpb2wXx29IXvvZ5L9vFAnoIk15kHgeyg1cbRl5rV/2imaedjgX4AzaY91C/ZoN+G6rZ7fJMY/4rb4J8zCxYDm9NJz1PbN7PjVTorVU707EG4AZ"
    "EcnKBswRtcBV1PdZucuvBd6BYlXeOO+BKghGeOYZFg0TE0iBzIChkceuk7VmbdD62zPlxoxnSrEqlgZkvc1uT3ymE2aA1z3+vUM9Am4cwvXi7BR9"
    "Nz3ipCMAhT1/NvnrZ3/wrG+dNpKlraxjEwT0V483N+BNNVSzVdCLpU3RZGfbmb2HFrphrtVEJmSrZUIeHhWO4ulxeDBS1Dd9inX+Cke4Gh4CXMFO"
    "KSJApjUSaS1DnjPsV/QJej+aPz2HI0wqJZbHBwo4YKd6fMndN7XBRmoDo580WhEYYwxcIYetUb4zpaNNwHloZU48yBi0p2FcjxMHjGQKgxDFOT86"
    "o9f8gP7/IX5DNxQN++8lJvq8FIUuC4e6rRUtiKxrdDaVW+laNpv8UL2QILxh93XLXcJEK97ynIC/sMYaEIwjDP+y349zieAj89ZmirmYr2RUAKBs"
    "1mSUwAw40i7ZwPi680kG1jyQPN5fkoxnJ3a/0+P40ik/YFxrcT55uZ+2OE0gO39uYdnNtqZpvIZ2aL42gWE5yZiNmZe29O0xllMYPlDCxrCYHHUF"
    "VrPQJ5NGrrpLiyKV9T82ZgoQtYlo9L7+U/cLWOvu00u8ppRstbpfzAxLzOSHOTT7pDk5CbN2okOusXozLHapaWPV72D38Vz6w1e+asxsmKKelLwT"
    "/t+YIYwkyrHwknKD3b+JL0pUvJWuEuMPv1Eujoyda2hsfNH9DuUfxTTTpJRSpD6b19VvMaqtstNXqOLfc0SbYmpAmQUlEYbfmGjpax0bfEk4B4au"
    "sMHQBt2CWwOMqpVuc1TsytkLksAixsFW3kFlhh+ENSB0SDWlbPpjmpoeOCypremhvygn7czfPvt9w06RLIWi58gRUnpGIKgkDXLu4DQ2Ckq7PvEQ"
    "1VmweeQE8NFqQl9w5HH115r9Pfscfdsv7Qbbr0Ammz8qFRs4LLqIYN7VSo/j3Tfh8zCUM/HD+CZ9f/f3suxj2iX/+3oD5Gra6pNHwiSbmUWa9D6u"
    "PShKJtKl5SRvp+vZWAHyY95oY5zBucWIpElzK65da+UdHpyVCrXTXVV7Xr6S/IkfXuIInr/c4vX8czzV5VZByRKXJLzusa+aS4g3V9le5Esvj3KO"
    "svqe+Sswurslmtv//FevofCjwq3xrnNy8ZNX0m6HfbfV7zifqFoI5pRmDv2dc2xsjBhTRkuy9mIFZiAbkaE8mzyDRvf3f/DXf5PI8GftVd+dx/A2"
    "PCBJ+0CR3byXZ+IAA+MU2Frknh9+X3J1vgkzeR3FWNrE9OnXQFnDbCnOxsJ8eyI8CnSixjybnCv6q63szForBwKiiqa/n11rNzHclzS76bqfNYlK"
    "dtEB0s57s8lSB8ymtaXl713MO/1XicuXGzpGuUHJR3BwOBlMQlxlcoWP+V/PPvvs/82ZJN2drV4BOu7Wxg49lmQcSK0UJmayvmeTywUWMK3jccFs"
    "PFDd8NzBLMGubxWplBfBSfqRnsogc4wjtug/yzrm5M6y0tHr9tdsNA6U7+WVhasrP3px8eribO9VeFlT24qze3Hl0kWpgYbHZ875ZfMFXrrL62tT"
    "Hd06JFzGrRSsjWfMEnMCFVD1d+dsKJ8qz4Enz5nB4eVp25a6+BSkDFGDdUi8m/0SmInoWkLGAC+zrbQLpNLaSZ6R4VsZahuSH9C3NT40mdW0+SMe"
    "8iVg2j/4G5jmq7Dca8C3MeslRbLKuuV8QlZZqVmapMNitlCrVbzCC40jXc+3SMtFrgiXsuFAKq6zOuzgT5NrXPULu+wsOY5USnXGDz2TyORCcvnc"
    "HJUtss7g5tJux2+aTeSMkIaxhWct9UtwZxPiYPS1hLSpLK+91YcVUPLTuZ0F267gqXAFq/Oks8WWJg6W/VbPGe0V0KGKV6i2LwUO12rpWPxZjF6d"
    "fTNvmsQoLIfB+4p+b6vPwRccm6fL9YSpFnSe4eee+b+QuuFEmExCfxdg4UHJ+H+/Z6owzrhrV34PlizttnKKqtlnoc9/lunwR32vfEzyRXnGto5s"
    "CwtRKO8A7XCiSZSfWNyesQc77wUpra28Dbz1R+EvyX+bw2oBzlblbSvhXJQlrtz359DRqSF2mPLLfcnUYcu/yzxKBTLGFck3ai/kYwj6QIuXHXMs"
    "k2fnfIpiMUzzlrojb8vs3auZ2bcmcmL6sofZnZ53zOyasKu0uY3UgOu50OR30fQzEMndasTNOn4pZ6PbLzUoxaIKbYjZBA/3mTMbWWtrNjE+6bRV"
    "FpKSgf7o5eWL88Z77L00xoWEr9D57MGjUuABGUcNKUWDWX9DghlxPu9yJw03yITZpJxNrrSAzZBkZZXxe8omhIytFMPtA8oy3l/7C/tGuJbkR3nH"
    "1PgwT6WqUniiqTbhPBYcDokMb6ZJCUtM7eyDKdMewKtTlCdZBb2wxcyFAmlb3QIdXU3KAwW63M46OWo1OP41VCIlY1x4+o9g43PSiV7InER/qQb2"
    "eH1lGhIAQAKzrEboi49qtiWs+QJ8rEp9k3M9myyTrNC8fyYqdMohE+9g7SRWNRqGkhmeyrs0aw6vOhCFBTYVokO5KiySmH06UVpF4xy0yTK0X5jE"
    "tbah8XxxpKlSzebnK+Q4ajYlZEwZPZgvRulCoqhowfGP4BRW0r2pInw+dsZKe8jU2YzPNAcJbg4COooiwvXertEMkzQrSJHj15EFbrUIZeO1OHoK"
    "roxWqDkoFBid45dw07Wtvx1PBqfwopWXdXdIEWnUBiulMtjGg6su19lKYdyiGdgL22l1GyWVy4kTthBAdsxTgArJjz1/MtgqsMpNfTsYd7YKp7KY"
    "rm04XmYNxSJyQk77K76n5ryTyyNiw8KVNIwebxOgif8wJ5JQDj5yVipC0EfDNs/0z2o802LBjUHAGE0GH1H9kKO1mUjra/mrWVkJ+LOjE/7TLtCl"
    "MpssSFwEI/5O0kPXi4HDOtJRYwCRdrHNajnoarg6TYbwAHuvWc5WIGdWaDT6RiMHoBIaOoaLNM9AZSHF0LCaC9dfk9DT4ADlDjfxaadnH+hQDz5o"
    "Nl4lToTJVyln0JQt81jMzAoOi0E8SKSg3aRCpquEZ2MyInXOqDjJIUh96IN5eBnQEXJVqN2cSP0Fb0DoqNmwCn6hMwYPCjd4SFYLLjsxJbaIknj0"
    "mpaGUqIN8gbIcyVx1Dca7P0ZHeOe9VCgFgyXRYllDrQXa7rmrSvWbxmlglyQlq6lisBmSJvSzDjB6zpoJjrI7bZGB/RWzfVxMA2ICWkRbLq1BacQ"
    "bVgm4X63i/SAfDrnJOP6+JcJfUlWjh5nubkUEDGfJCzdtoSBxKCpNHzAyT22wopcy+rlgjlf67dac1LXS4w7Z4FHJlBTj0TedYWQGk+V59ImGu4Y"
    "lGrS6PLiYdkmPqZDwUDcIiyKwq0E3bU5L49X1pC7Of9uIZ8BRtE1XpVAIj4XNGCZYUtQGhJOLW/tmOhacj4KK2O4ghLEmnmj8JHV8gnvKg6xzcax"
    "yAhQgJOe7dY7mABkhRCcjM8yOk1Tm12sZyQazJONjHkdXUh9B//u6LdPbzx98+mbRw+P9o8eRGHwjj49Ojy6d/TkaB8u2z16/PQtFxLv6NOnb8Dv"
    "d4724F8YZBQ43tEteNCdo92nN5Oj+zAcDfv0/eRoP6GZvEXDPcBPeFkUMe/oFlz6xtFjuP1RApO6A0Pegwm8dbR39OjpzSiCHs/z6T/CpY/gWXDd"
    "B3gPvXOApQeX3ji6jZc9fQcecni0l8Clh/B2uzhlecz7MsXDCNze0Uf0ZntwP14OiwbL9t7RgwRm8NbTd57+nNawAsJ39In+Chce3U5oad6Ce96A"
    "We/HQfmOfgED36ZrYH5wy9H95OgJveubRwf0vDeevgtfP6TFVMC+oy/g/fbggj3c0Kfv1WH3uZuPu3RAL7MP67hHc9v1mPjRZ8FevF+D6nf0iaUn"
    "XZpdmOhPkDgChD+9Fq4CgsCh41B/R5/RNY94HR7TYsj64TbCCsQP3NGvcdK8TU/fxpVGmuIl3Q2RAIXcYZVx6+FNHzMp33F3oYYTw+oAEeGoT999"
    "+nN58T3nGNAeB3ru0X/AQj6hd6D3shcz7UZxBI9+C894E5/19D14sX2mYFnrpz+BtYbBYDig88eyifUogzIY0tQeHZlHZvIPzEpVFEAgHCF/JBtD"
    "9vSsYyAQBmwGFuKJw5VgKRoJEM/e05/iZ2Imbzvrtl9dt6H4hDTfN4HJvMWHHNYJyC55Bt+Vzs1ewtRPmynbfxdW+wY8B2Y3GsYQ5oFv8wRmdY+J"
    "Gkb0X0qPxkH11B0eHYwAO4TL9xJiQbxrcP/EmIfubHATnzhbsMcHDNhiQtwc1/0u/vGQDgE8nc4HfoVLDkvzFs2f+JCQwXiQieEs+MXCqcwxi74N"
    "L3oHWDNwn+kAKsYm72/TvkzpkPblPvGox8x/ThVncayZ+ZPSwelcvImEjKSFvJqOyB1aTBIJ8OfEWIzeptARxaffZ7bNiwTnA0nxETKUp+9PAaXR"
    "PiJOGHBk7ziSBa94TIdNx5wUtBEG/5IkHJ3ZOT75T4grPCYhsuePYBSGg5MAOvKxpzOI+0t6B77hl8SPHxODlxHn66Y0BbxHOtYs+pgPiQxACfOk"
    "dm5Pb85XDyyqVQ9c6tPn8f5MCSLy6GN4GHL+O3wgjg5Y/PFjQRiHRM9PnzNfE28HAruJl9MbJiTUkDsfGOGn+lU9oiRIw9+CHvOLo1/Cv78++lkC"
    "M/tlIt/+y9GH8P3HRz87Psikp6OT/nLn6U09e08/IOkCM/0JyivYNUf5QI75ADVAkj8PUS+GNzzEt/snWiNh4ZUXHQlQaWjwkIn36QcJHkbSlHge"
    "RAUHyCd+QvMEUq3FreRlJ3b3TlX3GI1fSfoI6tFIo+8Rf0YdX6wAIlNhIVZTwKV6z0Jbig5yG1WgeoxLojlndHex6X1pHrsV2EvQDvmpSJZVU2gU"
    "FObRr+C6n7BKSg/D1YQvHtOC7YmFt8fm0p596RqgzKN/G/duC59Jb+6xBzKOCEsTf6NjzXiaQPG7FUBNvKbKKQ6r4Jpyoavc0GUOyubR/ybqf2hR"
    "No8+U4xNPCw+yiZM5xGzSrRZLMm6qJu0+7ga+7i7DvomnOdDMRb3HJvQAeMUc1CVusMAlJMPb4VxHlYwOvW96662qJ1kanjqpQPgCWamnDcHxfPo"
    "/0NGAK//ngfl6Ux93/d90SPgNABPsMTgIHse/cy1MWhYQfjUR1mUT6A2kCChh/PoNzW6ie/Qta8TPdUWDRR2GfZXCcp6BfbpTL4jOvZNDyBU9obP"
    "vdAFTWC51kiuAQ01p4Nt7lr7zwES5f2+Y7iy7rOiisLvu6rc4fH0AEbhR2E2CVttRLQO2OjRF2AgvsnHiEghgByFdX0DuD+PjWrM27I6Pvgo0cF9"
    "5xRG8EePfqYa2BBPSgWUlFwbjlWVqDslBlFauThi40ZQS+k2XvyHbNA8QkHg8BY88SGWKVDSob1D11ZBTXFbiJweyVE32KZEKJ5ItCinMBNROTys"
    "06NfKcmY7VfQU9ign8Ka3haXQxX7VONwjgK86wCg4s6pSmAGN2io8Ctauw88PFT/UDuwqEefk6n/noOMiscXVmcffvhHh7d4QKnEOx+LpGPWi/a0"
    "OG34vQx+Kok4350TR1KlydTqCnFEVTpLHutggb0rRHfo4qsK22BuQHQPS/vIrKFFXYUtil/ig7DSeEhxd8wpCpBY0TVY4QMVPFalPNJWY6CsxM5J"
    "cJDFLuwkBs8KuirpS47NDsuXmGuPA9YaepKVAdY7V8WhaR5xPFRXdvTKkK6Y361EtI/+nZxIoEILzeK+HR/01R2Fk2qdi3wfEGrpo5BgfS+WGdDs"
    "6D67HUZjw9KjHeHtDHZMmNiA3cKLNUJ31h2cIZhfpEQeolQn7kALcJ/4wHtJzcSOAS1Levr9xIpcHRB/FOPo4XHRZtHN5fMt1bnV4VjdXPGWOdKe"
    "xiQCPy1U2qpDPtEvjh75ARh8Cshn8Vn96Y0PPTeR+Ugub/Kxui/i2or/JGrFIXmndpNnZD7fHQfUtuLAqSyl4ys1DmaSo1W82+ouBdIl+dM/3hoK"
    "hItEuofeekOEkyLhslfaPwsS7nrb9+wHb07C8gQYuZUHWvuQfS/u/lUdqhMC5/qcSYhabkCt70sbsSM9dToguqRTV3zmkYjMPBPRPTGZUOPHsB7Q"
    "qhMFwwUQC1dtz2FOeatUsTt+ali8VTEZeSPiJmyXGx10PjiUqisdem8lrp5w+mMD9zJFe0olnRPRTirOojhlnwTVt+Jp5rAu+v0pIMNBPFwB9Q88"
    "JGWQb9pVbw95894k/feOioenH9Di7HvOlMhmB+DAoMfyy7ObO86w7vkeUB4YHdg2UvxQhg/QhdViTnwDsg5oOAzaxucUBx+WODl5R5FrVhyHARox"
    "afD3EvGyWsVSLO9afOKj35E8OSSN7GZUB/TsbRe1mGKij+RH11njQRjbPXkSJjCIKeyjGoPG+5iUv8cU4LMu4BMhHLum72MJuMAUbsLc3kRZ9GZC"
    "vEhZ0G4YwglOE1w5BfTj+NLsk9QnrvFW/XFuhDRLbvSHTDN0xMRjbG3LfaRc8gaDFHjHbvB0kJTrXoYoXhwTqPU8pnjuG8gZUGl4y8RS7xhf9F2j"
    "oKEDllmLSQU4GeZyGJnz5GUjVAZsLLtRif4SY/tJ3Ew5DXxmJNEIl4oQRjTGcBDZejxX3xwEZ3jB8HnqB/JpAc6wP4VTgHOumHh6SyMJjEm+cTS8"
    "c0TzNNRTVYrukktgOpjPPoVUh1LBZLV92Io6IooLymkDQrMhgwJbgpqelvNYA8hvcpJWxApE+5b1rj3ki67eu+vHQSVNwT5huG90fGhpTwn0L6ek"
    "lndtnIJ4H+XDPTxNwOn6F6uPxc6pHRtfNXYk2OdKXt/xoalrEgVYNRSt4EF9vsS4oNWkoN6AOzAKyXfEIzqopr8jB+P+iRGt9Sj62QFkYN+pl4cH"
    "04W6hrXaJ3XgAFbgoDqVP5jURdHnx0HB9gw2I8TVVbpbp/19i1Cyj/7VOLL3JAby9L1GQhuKgXtK9Dm6DbxHL5JAyBNYzffImBER/P7RfTj/H0h+"
    "6dN38Y8EFSONSlOM54NK7GQ2Ofrl05+zpvolGZRqiJCLGDNTiHLwCQ8pUYL1LBO6YkbuqQ2sYr+peWPBEzGNRb1KB4H7ICGP+kPd6ic2sC88+ulb"
    "fzmI3SM2vzFi61nE3xZ+v2d87qGfFZWdYAvIg4qDcWDVZC5IjrHjSXKdg4eayeFbcJJ0Jhv69IbRsCwd2SwMmMGXzJtMZkiD+JRrZRwEmRqcieiG"
    "SPZVTjCd4Qf1CZNC51Amy221Z+6cDGQ8ZHOPmdSrvI7UH019kYSycVDIwaaM8GvOonY0Vj+NOQ5QfvQJ0MBN3+pmArnh2ufDQcuPfnP0q6OP4f+/"
    "Ofrd0W+Sow+BaP83/vMJ5jodfQT//7ejX8KX/+voM/j0C8x/+sXRfx19Chf8K2ZCHX18bHzzKTyb9gIvwwvxIkzU+hn89jFc9y8JjfEpjP7Z0a8T"
    "+M/P4fffUrLWpCjp4VzDeeCs9XG/gif9yhkIvvjoJADq9Fq4Cr/GZ/wHLckn9LYfy7//i9YhmCKlqVX3alJ0dXgAsQeSPu9SFAZUqt2ju3MOxZKP"
    "DpU7OxzQIEdO0RAfA399jCyvOB673Ij87j08qwn7a8KQ8P4kOO1+0OTpTT9R/EtRWCqVMDU6+q6no48P7R5X7oYxi4S8JnvxdGv1XH1NUPCjVMZI"
    "TM0eGTcIIRER3Q9DiK4YgXc7UPHzWB3X+5xKKckIJ4CSB4rCenvfJBxi882NYdxMDWP+OJMby5UyHuy82P0VReXAS0mtLZGuZLLIsXo4RnbJRIj1"
    "R78QXZpdJaHQ9GNqd9Th61AwZ+pMFcn+6N+IcWEY9GZiCsYOhYIrpiXpGQ1QdihJBOYk+xvNRxvqMPDvVb3Os4q/Sdj4sHe6NA8893bgqMb3uUss"
    "5pDeOPTigDH0a04HN54z9Bf9U+A4l5AvrZAtXQtYvXmw1i4mUkNjyVbSkDDG4hyFhqsME1E7Q1FkAZ54IPu2Rz5cMbQifrRvKWK/m5sqgqB64A+5"
    "QMFLyziUA2Gqu2yGPB+fmxIK9De+EQkFK9V7ifNhtnwCutNjjbLvh6n5HAfyzOc7iRi+KK7YcX6010goEZsOXySY4n5JdCz7fY9yMkx6hufQdBxM"
    "mOQKB/quno5dfuuTthnw3Gf0/KDggn2tysHIx+byMLZw1Ugyi/aujuarWB/gnjkH7LR7FcSpiQO+ceaIdSNamOWcwqc3vmUtDTgvguof2SUqNnnt"
    "rOtvCF6kUs9tCq0b6h18R8t1pTobxqa3HPYMefHY6FLb4OyHU44k5eKx+qW9YeVYvHxTbbEQCObkWU5hiCu8fjTO9/x4K4CHsTG+Aja8O4M4zas1"
    "+TS6yfxjzjbG006pnwOpqbGhrN9YwtwWBECFp+tbDjn9lPo8sDJ+xg9HTKKZj3rP0+gD0XAF0J61MU8mf6bVJ2KiszNUSwj5+gOHq49QP/aG9ZoY"
    "nayoJbT2+bv/B7SiOPpiVETWj2KPF5cVtu4qI4+D2tC5JObA8TBLXP/ALhtcvrXAju662Kc9FF/ia7xB7iae4l2NohxKISBGriQnHvTJTysBUWN/"
    "+JzDJDAiFMi7XIR5CAO/TT44f5vIw1C3S8YF4fAWM9IejfV19tfAAkIOfj1RsBaKXfB7caxgV7klef4JGmQ/YFIUI3ELDFA+edW/fqrh/jxjWdTl"
    "FYoFXZ3Tvp5eVl587f+0+nlE6DfIzvbmPoErUmcD7ycOAQzZUvSwMqB3xvgrDaLvyksQ4U7WNQQDF15VDYaOYLY/lYPtCxSKM9IRGtVO5OgzvbIC"
    "6cClrY+Jjdc3FqG7FHnlMDFumCHp80Objhx9KO8h9bcyOyb9N0wqmSQp7Y3ZjMS+JllYBjtDFlPoODwMcXd6rGmJb5s/oYixX71FJk+kjwllIt1h"
    "9brqgN+LtDUhV5YT8PMxk8ImJ0Ex0E2FTBI1+RHdVO18oqFDJ/8jeCGSxrF2KMT5jQXLScl3+W5y3rxlYnTxJil+7uL9KrRUNHNxSB8VL34odZ0x"
    "XbbaYKCmVBkX3l78DF393bDpSlhtckqtV4J0N3pEw0EgqjyjWoqBT7SBhYe0YU8U9shmmBDQDawcT6SuyEwKqt3eLSi87CFzsJGSZ64uXlm6unJu"
    "YWXhu9Nt6+K7pj1KmQvwIthPqQ7Sig/MDRpxMiHpKMfs/xJ1qSk1w5w89l5Lom5rmKPPiKrfwinSL3TNCRrEVAacDGrGGZtmcuzeMRPMw6SKDp3F"
    "cfvKhGNJWI51BcQZMvfDbr1N22cw2abXZEbTnlA3vo8u1s++wa1m/o44nXlmI+JRYvMDc98e0eZR7VvFxJDLHpoDCiZGeC7c1Ek0he41vMApnioq"
    "Fn0ggQKM8P+mMSrsy5bwzfE62FTw2uw97tgPRIDsju5tI3T8sr+QE/S3GWkVyt1YE2juxz+Gdr7h0m0MKAtCnisTkY2pwrBXTRgd1SGnimg4BujX"
    "N6pzjoHw2A0d/+rHcESOeAcfjPOWrutorPkb/EIS85pqonQggRbYvNukD5vYmtGDUfdn6Eap5p2gQ48iKJIycQPhlnhQPmvU9gVUAlyGL23aypfo"
    "UqIrnbYHxh0t2Spv0YT4MrY0TJzFL2F7II/5hdfZJwIVVt/o5+hjk5fntfoBYeR2+knI7r1tMzP3OAvQOssiuAKzmGm0bz0fYisrdgIbJvtKKcy2"
    "9o335yGjdLg/RzoGVSqxAg4caRgkxXAab+CNCxsIVVgddrQ546l1NezUpwGvoxBi0DLim1+3i6uDXrZn3FzcCjWg6S4aANrwaD7txtoPSZm3M3+5"
    "2XEmzWLqGdvUgv0k5PZEZ2gNbZmdbVVEsBWVUjHrYo96jPHo3bMJpNLLiOeqkBt3ZKax7G4+BJXQjC0mCZofgfRzX+wHf4O5aYpgtQs3vs2eO8F/"
    "ErFBcHLEGdzKDgIHk5zse2zGioAxVY4m1w3R6PzmSQLmKxvBKKOOA8bJnosdb1hPQ2qk7D9E9yNzjIAm3U5LlYrP0OdVKckJ2i/Fq7B5L5+MGBuo"
    "y2GOoR8Nv3hivWf+CTLes8RC52jO8s81rP6mF3ugbAcY5X28l7OZw95OhLlkcCoPxQ3m5ogI3fkvNouZoTJdOg7MK1hCwZ9UnMxyDN0N7qRwhMeC"
    "qec0hqKj4wD/RBiNxatzK293vVZRsLzBDARlw2yoWUjUBGNNpIhd3ZN8hGptNOWNqT99aEspoyu9Rwl477JL642xJxhvPVXFJzeHIMIBnKZUBPlj"
    "xSxxGU2MQj3AmP/oyiMUY9qpQ6dx1fDqZ7+VlVz73+YiB+ztakGzjTo/0IIganTlJmZTUgjb40iNP3VC045+ZPpfNeK56FzO8cj6BZyxuELEmy8y"
    "lcfVQxLqEk/fpwZaVVTYmPrv9tSKnUBvgd0TaCdFKgRxTF9c28Qsp9AuYnxxGpTTggtBvnzlyM30C7ZwLlK3OF4OYiwnQcRHOMMH6nVCanjf01nr"
    "6+iIMx3Mmg5giHUIE7CZHFxM8yVpkEbDMz3BKvtnMiN8i9KoZYH0rvQMO/qlJDGJEhnH2vZ0A1U4xlYnqzoEO3nvVXI47kY80xxhk4IXm5VuU45U"
    "tmqXMp9Buuq6UYWDGiy1AfZMsXwlF+LB6KZmgeJii3TMeSbr36Adae0OzUUg79yWZwiwFptlKHYlgZ8A5jEmq1Itsr4PPCHOA+1R2IzyKEVg3kwq"
    "vjP2ezwiJdeAjVMiyQ2OVphoqNNTTXEyKn3VGHjPJabDIYppDLhKNv8RRbm0BorVw5+zHl5DS45WJmvkeTmdaHbQrs1Lat7XqteK1lcPdEWKkYWM"
    "UUQUDTLvq/JgQxq+2LWGqqtTyiBVla3mjUxLuKomwrvAx9mkrT5U5cgnHXfUZCLwkEoeLqoTDQ4Qa+aXl+e/H0GsEYSbXaQTGywTSfSYK98knMLn"
    "Y6+m8xxBbDCW8XsVx918LUzzKLyxRpi2XUnA4hcIO10YMSAcI8jai2esejEB8kW6WZ6xLPAx+twFoDUK3zc0s1a2lot2NHARwGXQ+XMTjYTnKgYC"
    "mZUP1feCfE0sZxKc0RQLJ3k8TK4Y0TAPOF71QTV4QQYD5MAgBmqosiZiUmnOMs99bm5zNDVkEHs2TMDuRSr2/Kn1xtlJyQ2RPnz6RpGOPm4g7j3f"
    "d8ORaxba+BZMjbNO5VfMW+KMTsnQP4+gqolKomKDjvcdP8C3V+3l962RDzX1L78erWRqHmgFOVv0VD9dwqki2WvYjWLb1riuBHMSD3yQnkjOajkt"
    "Dr4RnakKWUUrJUyJih+5vCfuQdz8O15Fl0RebaoNWxBYsOaQx2NH6jEOE/9YbWHodmNyMD8c2ME4kwoT1LB0I0x8dTBXOO2VYlneUdFf3IWF4Ucd"
    "6dDv6B9qd/az9TDa6lB8h1b9kZ6/J2NA6O8HnrBGWKZtspBDWKvEIlZzpCMAAvXd8hgEU4SOAB+g4SVJ4kxFcD+uQ+aft/ameZGgDYAOAhfekUL3"
    "A/dy7NflD8LVTz6iedBqyrXD6gTwsJOhhRHvuEk745ZvyRnybUU7HZ//PtAyIqcmkRfUa68hJRmBT/fAawtEX0SbAlFdU7AApC+9Obx3ZATl1FWc"
    "4wiOYyhVUa4Wmpb4MpICAZIlzt9s8ruP/hfLxZ+AGdbvroudIU9IpLTIj8JV9MSgw6UR74cR0AiPcxsMBuo8gfYxXaYmOtEHpk96quOQ3Nhxs2HD"
    "rZYgrIp++2xuMTj+6Y2GJ1ibeIOS5ywBVIseo/3fxukAUOPkTqrdVOYsn37TzSo1WpYCde7XRPID7Ulod3iDuohndgTSrKNs7yZu7PId68Yy6ZJ4"
    "9byCO8UAW9+svITq4I+U1QQCU3A+LfIIT0YdhiFGTeSNfWQbkn5vRtN4k1i/oaFNtmJH8H3HLMbGQ2oWWwpgEytIM6+lHGeBxGXmdUqAr2o6kZI7"
    "yANUkdxdH9WfYHMNUqXXPTEiRferIbv3qrWqHtwqty3tb7ptS38ndPoRMYL3JRss1rz06S1DmzdYWPrtS4Ul33l6a8wGpiazNUFiClgBfsXW/a1E"
    "4DzJPSndfJ5+NF5DU5r0Q/jvnaHNTOGCR/Agka78FHlJvTfe2hRe9h1BQ7c8eLxGpvucvIzrFW9i+hH/JuSYwGexJuDTB3VNTNFPijtgjZO7pHdy"
    "Aw6vc+kvPczm/frOpXbnxTSGB4hpTMnHvgJBVx9SV4mRHUv3Tb9SWeZYv9KaLqWfsruLkrweU/6oeje/lDeXtiGRA/mRBIf3FD2EAwyOTgnzeVDt"
    "WUqK4iE/gm+rE1EfIQemvFZ0yN8a1Zz0X+WpH8DIZCNbE50Xpq49KebTPJR8g7eQSd2Ccf6RHn2A7gDYqo+UgsiYAJIVZ+O+lz0/qnUpPoh59i0R"
    "7XtawrEvDpPH7EJkFeInQzqZagdWom8ioWN1Mg04DvEIy6RuYecEllFn4FmPVb1njLXdhAlH1txvCStrPry1KRE6B1zwRCTPmE6mtLB7bn3I6D6m"
    "cm5whfnT7tMPvfeR3icksWKHcHQT0zuefjl5E1M7l4bxZ/7pjX8xGZXKBLWRqZffvee1MrUuoAnal7psyOvKygRA8SxpX3rPRC2n3ryUjg8b965E"
    "NBFhEjhasiSY8aZzzcHX3M+0drKxedqupihqOEbEPRoJvwP5yAEeWNK/jtHVtHpcq7N4bLoH3nE6nN6cRofTYQ+LUJKTho7sAFk4OeXpYB6366m5"
    "1gXrIib4ftDuVGqd4McTdjz9WLL/JVvglpPJ4Ygxp+upW5YwzX6nqhgccNBTilDvE4ExL1Xr8OZ8EnJXRkcMN4kGsiTKaGh02A5g7OcMutPUWqDy"
    "7ht3zSO1kKnelc4GNZ1kxfXGnHwyrBfe5kOyOd8Ux1hCfuJ7BGz0WB14+MttKgDcZSe5EalD+6JiR9RfggL4ttcZFdH2PoXv/udJ+6I6kkhMD2X+"
    "XNDNySWeWoVnRtqiUk5M4hhBBwlI3vdtiYrzwuM1RQ0zhRCCiY2qL7lQ9Q6pwm8I52UIF3gJt03SjdFdUllViqk6E3RLhccesvP6iTq4QuVT3enM"
    "s4WgdzXxw++bihrYkL6pn7Oz2URDON36J6RZyFZJ/cGQxqmhuTVG49RPaH3uogaqlhwbb9QAlS0lJAm20PGKWyOaptbdE7RKtZzFaZNKF0qT1H9D"
    "j3Ndm9Qq669rlOopUEGb1N/whjltUj8ybVI/rLRJ/TfWnviFJmqRSpbq+2jSOrd5DVLJJ/ShaXt7p6ZValQSxFul1oiNoFPqR0SYd7kgQ0/pZ6Sj"
    "qgdDDFhxIJhjFLZOdSykEa1TPzXqsvVDPo42UFU03v1jtE/9XCUMUqJRgYKoz6fi8hNDzOmWiukad2W/3oj0THUGdPqlfuhR/HKNQT6sR+p9HJpj"
    "NVUD1O2O+oktOfPbon4UIrj5jVHflnxKT9WktDHkdNIPaD9olvrLcZulwoD3xYKNNUtlT71zZGvbpaL65nhnxLgLWqT+0jXXFB/6RrRBqn9pYFS7"
    "FcSsbNf1SyVKuXl0F032+0GnVGZ51pCuNk39qTZVkXV226Z+St5+CbdHGqfeIc6K5Oi2TSUq91umfmQpyG+Y+qnocY/GbJlKGvQNt2Vq6IHxW6ZW"
    "xreNUz8Z7sPw+6gKw3D7qKIKME731LreqR8G7qURnVPr9Qd/h2uaqX5WqzHQXO9LLkZdY9X7hGC+72yh01L1o8qPYTNVhfId0k71F2pVjWio6tHk"
    "1FqqekznhC1VfVcLn0ANqu2fvHMq2jCUbbtPjsVYt1TUlrTD762TdEvFH92RaAb3WT47Ux7aItVvRuiMEoJ6jtEllcZ6UpXVYDMcv1EqDRp4NFHv"
    "9+ccuNAeaaCI3BmBPWAMm3CWx+iaWn/VFFqk3vJi67KxEj9j4xJtIWchuEHq6bZHVb8/2XxcRujMgduiHvptUY2fyekA/di1Co0Q9axFz7UKv03Y"
    "GDXi62GHcNwFaxJ93iZNbLzuqEFv1GRoc1R6OupfU2iO6jhJq15uNuyiBs/JGqRWVzR01xLu7mHVQgyQwwWu8HgdU+nAkzZl8OeC8O6tKXdMDdzz"
    "5ID6R1LI7mpgbZ6CsqxvJZqb4jUpJP/AHcqho5W7n0QGPnA0qan3SXWjhmHEgfikKJz7jsI5b9qiBsZFA0n5MM6W8N3C1xi7XyoLSU+jFBo3ECuB"
    "4yxO6ifrmFrxYkv02PRMpYgbH2nNDb3rGrx1e07ii1a/Zr/DVqnW9WFZlir271tYC9Ykahuh3g90/Hgj1BHP8qILNf1QQ41/N7EZSKYARq29cTqj"
    "Ph7ZGZWSXe4g2b5LbtbDqhnot0PlPABU0xz/Sl0z1GpCRLwd6kfG5PqpuLLZuziFdqis4phU3Ptc4m82NWGgLZM1jOzwgWn3FJz0x1pk90gKi6Q9"
    "0HTbpHphKMpJfJtT6mInuIEVVw/VyLstrtS7iU1o0pWfegdUP1x2G6ttNJTnuB3kQuPnJxK1zIZztt4mx/4jVsk4WfdG4NQ/STtU3zHvCcNGVfxL"
    "0hb/GMSRhWv9JG6LnEpLVHJ9MDu5TckXEgEJ6XACUvjm9EOlkuGR/VApHHv6/VDtJb6w1utMFtr+6E6ohkTChAtVpFXhIWEwnR6oIUnUdEGNCFcm"
    "siA2xSK2Qnmn0AmVmmw/8FF3RXuRviaS2bWvcju0JvYtutJhBRd3PlBzuOomnhwsJ3k6HVBZTN4wudJ1aQ6n0wjVhrUP1RANXtSLDHsB2uiSPf1I"
    "nAcCLmJ60xxSNZom61Mu9Qm6o1pTljJ5avILyB9hdQa1fN10DP7CRLtJ9RircWo1hlSXF0B0Z9us4prSExrDbjhpg1WOI6EpYiSklb/k8X3IPXk0"
    "S74idA84nfRQst5lpTnr/W2SdLem1IWVku1ukRhVxwzNkAlnvzpdpzErb8I4jVnrFtvtvlOrjX6b2rN+qlFRyajTJhLapZNzyDlzkMKjhO6Hi669"
    "OvdJp5F0hKcfcmYFMVq3NSvmzxpJfIfSng2EzPBYzmxy9A7lQQlm1K7sN3GRm5zmgHVwP5XyFzw1DdVmuGqC6OWhBQy5HyH340xtnmszHwS8X9I0"
    "f0IsDWnlQwWq2Dc5NZye8BfU6nU0ITWGEpFqMZR9xj8+iUeaR++LS5FO91fOhzkUM/pDStLlGkx5yB1TogIUVOn2aqnug9Cz8BZt6G3p+0r4DjeP"
    "7jYoyf4mazniHa7mmoSdXynQhIKRMtVuOZ1f74hRY0satO8ryomT9n0dyVglRbDKXYO8sTH7wH5UyUIjV55YbnG7rb4VLDpLcOF/om6ShLjPoUTD"
    "hzeAfRtufxv+/Rk1GYXPCCqKbUQ/Ofrno19Ja1PblfXto1/wBb+Grz6mbqufnKQH7BQeT/uAOWcfUp9YzEv78OgWNjzlrqw/xxQ1HORn1CD134/X"
    "AFYnKg1g/RmEDWB/5zYoOWn717el/euvsP0r/vE2POFj+q9t/nqcdZQeseFeTtwj9mOOPRMzUz2BFKKH0cRTp0vsu9o+47740cdsFMsSRPzD8YB1"
    "XbtYmthdtiE4BHdnyCh07MZvHOuGlW5VsvIN3/OzCHzT5s5xesUStvRbQ5KLyRtzz0ecn9Rx9LV1jlVuLJ1jQxX8XijxnLMW9I2lnB6yaoKggRFd"
    "8P63bUJpUGXASVInaB0Lk8O2LtazVd9kBsXY3BiG39Q6xx5jbmP5nMZsHMueOFV52D3ipOvWQ2ZU/fojAqKTN4v9kEs6NJ2mJuAkya5UoEX1nu8L"
    "bVbUCT11j6U0+g3O9DqdbrKRXrKhPYd54TZstutVKwXnpOJ2USvEpqYSN3O8/iYf/RvVRNZ2Y3kQuP/FtauRjGFNZMki+3cu6L8jV91DfZqZp0/C"
    "jbAEKkySCOj2Ay+GFsxNwhMa6XR+sBn+LEkZ2YCOl4m9VPyOfxGdY3ePvqxvH8tBUZO0Us21EKNdBHalMLtRWw3nFhVUAwcI3uYl93xHC9Zwx9VY"
    "N51iubnovuBOPMTnotXEG12JNfhpfXfEiUid+px8FS9gbQG0iCv9VA/AtPrE3q+JNsqS+8zISbZxy2YNZfuOg6o65WZenmqD2HhuzmMB+qq2hfUO"
    "2LeuKaz0URq/KWz9DZGmsH6tVaQZLEaT+c2Gjes0gvVHTPQMSeU5u09cBDADfbrr49tbDXhorRrM6rS7woaxDrcfbDWUxCgbWmDIXcVHaVOj+79K"
    "LMAZeXf0sKfU6JXUypGNXnmenE/y2JN1HuibF+OfUqtX0Z79gMoo/XnU251Se1c/FdyUTR9XZJxKa9f6A1Avuy0/ZulQ386V5RKpA5JWOVE710oz"
    "V0+x+z+imeu0g8rs8o7VsA6R+lEYAPUIDDt8tmMrqXIH+ocbtfOxqthKIzzpSuSW4x7+8a8N5XKvVXqRIBcFV2BI31Z1ADhMQ8cCnf+DP0vfVgYr"
    "umFCELvyZqwWB31bbwg0vZX0ZFw6PVv9ZKYw1XHflGWbvEb1oHEqSDAPjGkMK0A9tW6tn0zP6zefVOAU9PZdWwu4a46L9mFloTdxJ1a3DysHdEiP"
    "Vyg6y/2P14c1hvoAK2BMhuH9WBVMiXuqHBoUPz9z/yCwqof3ZH0b3wgDJOZ9jEvDVjaxAj9ZN1YK8SkUyGOTqqTEPdRPPboP6/0K0BApX/VdWPeG"
    "P7HaidUo46RQu9BPH0V7sfJxc/uvqlit679qoDx8029471UyBt0aNFtqPLr/KuW7aZXjvuvbcnGxqj1YGSFoSA9W24EV04erCmas/2qtdTFB/9VT"
    "7b7q1E9o71VBTKqMz54MP9Gz0nsVxtO9C5F5nN6rWqZG1BPrtsqbJshNX0ufVcNQlBrmXE8O+k7jTVbJZ+SimSCfOWmT1Vh5hDZY3a+lvD9LW9UJ"
    "MW1Ovb1qbD5o3jgBj+GzmWKbVQKKFNgjr8mqrYWYdptVfL9vc5vVKvpO2GaVpSwZBN+xqGDqEa31AES6rLL30UQaVSkzpY3UZrU+yPr0pvXCj9tm"
    "1Vd24SHDG60ejtdoVah5qs1W3erPIffWtVklGa5S2KknNyUyVjNQrXacFqs1cIxjoJF9sxqtGvwJlwrF3ywrY7FJbwi2sQbsHH/dg3FenWIL472O"
    "poapFn+PqqHUBlTq5WIzrrS8KwbggYQwNItNZqVem8n6rzLmwPD+qwjbw9ycpiflVPgst6WT7/tlLAxzofRgtQ4xvzpOu7D+LujC6qQmPBjVhfXT"
    "IFfO78WKDi+/G+tuvBfrvtc8ywUkQBhjQjA6tL1YiYepnnuH4yo2XnjL60QoXTg5POwazdF+rE4pWBQo7fhdWSsVj9wD0yqBNRx4WFfW/4mhAUHp"
    "Mvsa68q6W6WQG5wJHPRl3R/Sl9V7g32+3TiN4BV/xlsrfVmFBNHupjmK2R3ryvoLJ8xU6ckacfMyRNAe4fu73VgZTG6fe/KxU+dWTTfWmlzwul6s"
    "8jLUi1XMSOnFSvnKmk/hdWHdt11YCewV5vNAu7ASWrS0ryL7+r7cRLkKYRdW6tpGoXFzqqVqQ45N5VBHe68iifpUN6Lvaui5ipX/PIh2X41UdEd6"
    "r4bjU/dVwxpdrxh13nJ8YeEpsd6whDFjEp2oWzTthgak9+p3RrReNQCah4o2qAtw1+mJGWu8iunx9W1XiTO687lDPC/WePUz4oUulF2Mmxyv+aqz"
    "pzHwi1j7VXEA3sB+U7diFdfUBE7Y/KgGrJ4WRTrZGxNMsa4Ba82pT4YgsLlNWANpq41Y36W2DOoHUBaj+zZOG9bH9W1YY9dyb9bKISTrSuqrNbc9"
    "7M16S3qzSr70rpjw99TlWufVD6PUu5FurV7i4q7ZanU0vGWq9HeTGFotx1W4Ixb502Ud/WGlWWvN7R6qbaVZa/XMes1aPU1P7RRp10rCCzuMmHat"
    "Ug3iRERiekG0WWuQa1fZybkqPx2Z9WczBTi+JPhKPpgru6RI4LptWTV3R9VsN0BFKidYnCMbsx5idlJYIOG0Z63smG3Qau1QF7/VEebV5qz/W3KG"
    "tDlrBc82UBAexFuz1muXvjJhmoYGOcS+b1cY10My0lQ1cBABKg1ZQ5ZZ1d+ps4VpmqAvwgtk0928jIWx27FarcG0Y5Ujy+1YDbwDBhWdZqyc6Wia"
    "sf6Ct8/MkcJQrvFSXVuWD6wo3ULfRt1y/loE5k1jLUqDgH0n/1QktualkdUooXKXnrQ0nBfcssjxGrN+UiWmO7XaaY2CGR7IAzeKyGktRl7XpSuE"
    "zVc/ZunOObiqV9QgAT3wMqBnE80tlnRQs2X7tgsB8hEfVGffgK9ILJnNqkMRyg8tM9m1IHpuA1aVJ6Tlwh9+81UJvEf60WvfuRvsBCBZhKv0gdUC"
    "P/CXCg1Yc+QpcorKrsi+MGTuJ69am/6+lx/v1MrWAl2R00GDY7JiVGX2rsnXsZxqWPtVgu4IEKwjKZjzUWTo4Y6tSB9W28vFwP54DTvEFW8L0e/R"
    "YnP3Lptbxyykpj9rBdI6LKQfXpqN5D9Wi1YnuGN6HwbJlhVwDtwhp/3qA68nlKkz5bbjeoYa9RpTnTt2WI6Fm6hdN+qhGLxYDjS6i2s44Ximp7aa"
    "UvDCRiVP3mSAjt0049Y8n5V7T98/Q4WRuxYMaTcJAhMqB3/Kp5sOdS0eUry7q76pnz7jOANdWeBnYpit1oJNya+Y9/q8Vv0v5kmNOO6PnCPzEycN"
    "vc350H5/FGbsQbPXb5LMGb+hq6eUBj1cd8XbIw5cmyrNFt6unHtq5cp7wfHHJx68aZj7ROPKCfKbuApotptFu29Ln4hf77mVIV77Vkk98hPrH4tx"
    "IkkjEugystKxeQJ0aObjphbB69xjWlEdBKCIJLGEg4lWI9olDewiXETyVcXN6+iJCpTHtOEso4v/c4exrRx5O+ooG2dlzVH23ifs5/o7VRPuSZuw"
    "P/xXiPb9h0f87twTUaGhXMHuldqzDKvvBmAbnjmlkY14zbZgnloGTutq0aXcbrB1+Ka6uNILVnf5TgCeWC2gQUUCVuNxNL9Fzemnt/7waD4gRcnj"
    "9pEb7YlyfDk3tWNftPpeGltVxh7RMZbSRJjFa6cspI3RSsKQwq2IOBindItYRoUvVCWwUxwwgQtEqhet/9htW6LYjq6GiF8FHZuQwVRDWW+rYcQ/"
    "G0ud+HWk9+xE0x7Ro9ZCzQalV1UZM1LRjDJr17ZmPJk3BQebHuYy7lsGrzPmlQ/qAibm81WauWP9GQeRQgvOS3SL/yr1GdXOtBxq2RtyzvRLTl/4"
    "0i9zu2EglRlS5NAigzpta1lhGYJMNTr9t5LW/KTihnWflhiI1cmYR5zT0uCJcGpC3wibVvp2QG1jwErhanVxHcRUSdcTcdYYEkHQ8K4B95+jejTN"
    "tpcmtk8MqLtNyTV7KY2nXOje2sQKsl6N++fQwQFxm5WqdIrVR8YwgqXDLQmxmJMgBg39llMB678Nr6+HHmXbEB/Ou+vjovRG+XzQuKnKyRzl1Ngr"
    "FTg6/O+BaflwaNWioNsusZgKpXh6nXkTksymkvGJpGjHMq5tY12RAV5HE5vFzG6CamWXZ6N+YM+gieg5bzE5ypoZKo7zXddd9xcBFM1j010X4d09"
    "HHzLELS7xH4VwrOKtOAluvrqyVth20nvV1sAXEE+5ma8Wek0410st9LB7aIVbcD7fN5tp51e5jbdxcYe3WI1XcsLkI6jGu6+0E3x0sHdTpJ1kmbe"
    "xcywZAdbim4V2LliuyijXXXP5Wk3LxLMGwOJnq/TZdVmuleyLnckgAv7ZR/vKaudc690+9lqmmwNHuLXaaRX7vnOtaJLaFGtVtosYr1x9RJ4EqdO"
    "52kr3hF3GT/zSzezVrKdl0XXaYK72KIUT5po1FVDy063EghrDr8Xnj6ywktS0+2WG6Pg2uFvvSJoccuft2h+8Ta3V+VzjpNIWmlyrZ8JFVSPAn9F"
    "V2J99yq9ltfClv/Q58UE1NVsHdvAFiUDMOTXYQvKqkPjbNrMOvIkuaGuS+25fLvfWk91E/Al1vAl0qEtZxea9JfcJZflzbRinMIOtwraoZyp4njt"
    "ZO1ZkmliWDZVIN4dmnX0nYd2ie0U+luWPMNfyxPwLMMJ6Y5uDYs68Bqm068VcHJdQuQ50hEZ1v4ViwDQ65Zk5RaQBQaym8XEDWDpWZhyTqvQTLEm"
    "vZ9008EX18du4sqnibKHebWbKVwzuA1DTqdTq7mjWZg9xOdxz1D4Eg5QBi+IP55qF9boRMwsYBd1KOAMW/3B70s5GW3gHTS7Xp61t4rJ+6xeS1ut"
    "wV0i15Ci+Xb6cwoNVZ3R/B2lGzfSHXtzRnTL9xbH6pmKB2guyX6crfV7qXtHsoPV+Qg9knf6PJvGSfqlmjRIs2p6v57jeZ7G2pR6o/byLaKQtfDB"
    "2GepgHNfzCMafIUwnJlpdgoxx2n0Or3M+0ePLJ1n6sC0HTBgC37dKLrwX9j6tayZsZDtZq3ix/JprdjKUYp363uXPr9w8eJSsng5ubiQ6BVnzw/+"
    "+fLx25VeTEvh3yDxO2v9VtpJQB7JjeugmzRRrBFHxZNCVTTwnojtFU56ZCtSaa+GW4IAOPTig8/aqyDu+WJUz5hLx5uNpq6og0vWWJsZ3V30sjJ2"
    "kUfIWpB9DR7q5UQnMgqNb7uJorYJM8PDuQrrs1bUtxS9PHjYzlAl6JgpNUW3cBuIXoR/iEQDjXJo21BsedhCrbE3+P0a/FiUpuMMqbQrY93jNQU9"
    "Z8+O9gO9XJhuoMuDLyqtQJedU9Sttv8063wNVqyV93gznfaf55t50U5t889zmTb/XPA7f+JH1b5Mu89LBa6U0+YTdC1UkAq/uedVs8lBM0/5zD/4"
    "7TvxxeRvejHbr/OsaBWoWpZOy87Bm0y5WL631VJ+5HTpFJW29Hp0XnUUIse3dCnrlOmPs9JvyHmWtL/SduKUIW0jzhVgiqEH91LAjXwv/dkCCBeV"
    "X9t481K6M3hY4uEvE+yc0tG/nB6c8G9aeo03lbaCppukudR027QqMzLqtRQWkBbC6bG51IbT0Cyc5porgy96/VbhddS8PPuHhyQLgDD8tpn8EVlS"
    "tWWm/qkb5XfKXGylqwVxhi26OdIm0xopwMfROisr/TEXXdW1yQDBseaY4XWurh/pgrnInwq5FPlntp6GDS9X0tVW1i10ZUqn1+V5OP154fe4VH5s"
    "e1u+WDBdmPY3l4qmKGdOV0v+d1gzy6bVYpxeli+IOHE7WD4PNMT7bVtXntWF0B6V/K9tUKknK2n3Wyir8dugU+UVGIoXgsHW3NaUz6tlGG9JuRCX"
    "MvHGk7yusi2u/HCbTC7iOP0y9dpKwvnJOvzqfjtJ+au9xT8GjSSZZ8NfvJCVBpI0IVbg8TzHGkg+jzKD7NW6xpE/VEWp6J6sWyQ7MUTHaDJXOmGH"
    "yO3BZ0Ixfo7Ei2y1NvXAMvkfvy+kjoK/uzJgkr6QxvzFn9EiXM1w2cdtBdkWqXDC5o/MWPBaxC8SCQhiu6TLClqzthVAx+vgWNBHEu/HbeB4Eaay"
    "hee2dA5uolZ9B7ca1CbSlnlZ6XY0UE+pW+NiSx15oB0X/pNxVOeENQiBhBwVCXCUwUNkTIW9nnXmNPFcGxP1Y7RnMtlJQlcHugCLaNPFrYARJh2U"
    "nUPbLO7wF4PPymP1WORL2ZDfUV+QsXqL8mRNFJdJv7TDkavP+B7Neus4E/ZItAeW/B58JVvlTXLuTq0vouNvRWWIFc/5hOq2OywZ6I0ycbyKYs1N"
    "gPC9ZeeFTemxnp1mv8PAJ9wL1At9ZjnvrBuND/++3M+co+tPdpJmhrTfHXfDsxbf5SgZ4nYU69Qzp0/Yx/Aq3FuaFcAhunwC8XnAM9GLnHV0W3it"
    "gp1xSDHoTIiivZttpSRWMmthV9sQqubZdvWxaAfCyJjXRCWPNBtc0T945mLwp0FjwbODu01kgk3E72qxb7m+nSD9wpEWVJ+YS1p92W0kKJ/hkWH7"
    "wLNmL6/ZeE7YMRDVVQXxOVGTwEW7W+SSA+F4rYsnUNdbXqeZlbAGSNo+kSUtPoCDu1NoAnjR8bOIL7msJW+dTBPlFFADBaCIT3TE/TCdjn/VSQFz"
    "gSEGdxFgCPeH7BJy+Dk2jc5UDobx9aYna+b3PLus3ABDw4k6sARy3P87yjFc3fAU+vQ11FG20ceYHMiM9bxHHpkJN+2b05sPXyh8IJ3qfifc76+x"
    "NZ+z7XqRs7MjuvKJw9MShZG4U2vCN3SUqCjH5QyoxpBDegrd9hbRg6s+dYf5UYQg62QRTbxptKB54wS0mpHjFZmdqHceqv1Wf4hcP/gCFIDAnJ1+"
    "p7wX0x3TIE/egwyjIJyg0Q1YYNJJ+oPfr6Y4NT4o+oQTdL5zgwrOg+Ve0kZx76wuNVY3u6sglfmN+HJ1duKXW0inJ2xHdzFk9kDkHIYCEcEa9LVW"
    "/8ecHYEJFvDRjf1No9Fce/BFB62utX57C30EdAclW4zTPs6XbyjR7Bp9uxrE4YmiacJ65RSCaHBUB+e8Qx/Xu/0tilPA67U42IUxl4wZEUw2s9ps"
    "m8IkyPN7RTO1rsrZZLloETfb6mfkQ2iiCwIlJIa6KuIfaS8VnuKPhBQ9+Ixw+pDdzWt8SYw57CezyschX9soNGTzl9OIbdiGNaL7xbsIRL2Vox9U"
    "HUWuJxnWGMg46WhMSuLmaCpgb4s+ebMadPhhF1ElwZ+zpng+O9laVoIcShB2rkV4BW74jK4v5FV3KMmhaKpnn16FXhNOYXmyJmcsL+lIk9Kkhxzu"
    "u5a2emlnvNZli56qUquX1jYrc60aWhqQeWTPDOlSdnXx7146v3x+ZWk5uTT4J7gMPpxbTK5cfWnxuYXk7EuXrlw8f25p+dhtyJYXeZDFZPGiPiG5"
    "snB1Ibm4sCyPWcYhrlxdOru4vIQPx35hV85f5MBxcnbx6grFkc8tHaO7mD5S3yR5cWF5ZQEnc3XxhfPLK1eXnDvh2SdoJ7a8dHEpkbvOLZzDOy4v"
    "JdEFMKuuSyErcYwOYWCS9imGD+yvLOaSbVDQEKZSEyy6zhAo/0e3AbuSdQdf0EEJ4s3xtl8X03Xgx6UY8sH1Y7f3Wow4JMURif4U0bFAmKxlx2ni"
    "tfByf/CFr9eKqwYNzqqdMNQo/Do6dck8VUtwmErExWweZj2C88T5rM5qXL8ZfgvcAzMRSZBKUoXu2Ak6ci16PiVEYGnGVO+54Tro1JpwTTCd8YzK"
    "4d23JHmUbiz7LPessyxe0hiGAH3zerLOWjZyzVkuKP8pb7dBghBoHzMqU1KTeqREMoVwXBElNBNYOfX2WS/BjmbdNfTLqrpqZLPjle2gUgBrSEnN"
    "xqgS/yAl+uE50UP4TWl+9VIHVRVgIU11P7GHcpXOqBNQs8Q3myy2vLCLtV55iJIulmkVvH9lZogj+TGRjRCab5E3ZJHgnnzw+w6e+wzjOjK5b2lv"
    "Kt/+Nhxwq3p8XG9+n8xQf+1NbDFIF/Pz24zVYDLOyrziDWthAlWvv11Q/m9pcs6E42AuI+ih25IPWuBeg4qatk7aFsp1KZtkPT7RffekdYHXbxWS"
    "4ReL+E2l0dOi7zasDOOFAatuRyRttBC9bKxvU38n16dSmSH/GEyw31FjyCnDSFrZ4AtO8aN56p0yTQqelu71Ts5oQXI8SDq1iaTW7znVHktuHLKV"
    "PIsEZgZsCDHqoFassSeH6HSYuBzeUUnzIoePcUrtk3hnYmPROxuWkiOr6GmpR13gbxr9kiZQdEa+xGm0SeICFlRjJ2OU02qG5EuPkdTaqAaFK4JG"
    "2RaSXNGVpODZYb2PTN6pd4tN8a0mg/2l9z06hnu/k1cS2edwf6qmIznryPFD5lPHM5jsmeBqsLxs4y2cQ22dv7IEFEIoM++AsTCDpd8Sf4u/LjvD"
    "ViU4hmg0S2z76207RIn1qFeL3w0zm1ZbNpKccZ49HUX4s8xY3QHLseh4SXK8uu2Ck0CY3+l86MXmxfKmbe2Ipo+8MfLQJioBHJ85jYZCk/sZ5qth"
    "DnqK4xQgu3ui/kC49ular09JjvLq1/q0slgS00WbotRKwmEtgZb5Mi1HMophW/JH63sApauwkz09GxHdsL7VzxI5z3GGNHFqGyG5u+N09lk2N2K1"
    "WE4xHxugDzxIsQY+Vx23RpeSV7JOvGWPO5hTKRtp04PSvt8VjuAWoob9edI1k2kBhxN/jPbmQSdz1stBULAOYGYZ68jDH+Xh68h9VDuI9d4xtSlh"
    "gJurbNMhHXYW6A+bL+UrI9W+B9w7oun3O/A66LjphqfUP8dLn5P+OfLJHdmt68QnsJmIIR6sa4QhfixHlR9TwpGSRN2y0h/nnASBTCHqKXbHaQai"
    "ic/SnNqevvbIWl0jyGTZoYwzHPZ4vXCYZzczeI7G1CSqWE8lbh+cRTaz8Ttd3xM0wXFGc4sRC1OMCHfLzWY3s1AHPnbLmxM//STtbc5GxuZyE6oz"
    "De5mzWZ6bW0yvodZw/LSN7injT7VPMtlUdb21WAf8OtX5aDIqcKf0lrDbD5JnYABJ1Fk7NFbk0RDyo/S5AEY54eXxutO83x9Ta+TjDSqH42Q4ssx"
    "9jxuO5qKej1xA5qFJqx0j0sOymK1G6t6HqPfjIOLgAlCkWrrb1RbmYtppIC3U2BNF3ohotXisNfFeHPCVAWYFsdnUD+G2RWUf5pxxnIz4xBfZ5Ju"
    "L1Scla9zBBzJmJplvJjCN81iFfN4EdcDxnRQoUFv7YJO0utmcoPNfOfNHvy+NZssdry+LXwksiHNWpYzE4Dy+7SgMeS1aaGJbjt1PiihB5/1cngs"
    "m9OYFJ0CzYFdWGZUZ5124ZU6EiMImqv4KbRsjdvhI01VLmZppYeKmoTdxFEOsJ+FrQ5f85fZ65Zytd9jmeqt5zOcnSLrzWPrVIkTxRqizNkyV/an"
    "0J4uYbELVg1eX2Plpy/6J2oXXseTF8UT6/inxFGTkl5dZpL794w8rpn9OKXSEZN9VLolqUHXkvN2Gj/4G3RdgAqdYfhxI3sV6HMtpywRJvisC0KO"
    "ssbIBsfckaaptPEbkSxrFTa5bLxVZNOwg+phR3yiaXcL9W+gj37H2y236chVR/ny7FZTXR60F6m/wdRJKIUa2cGHGSUMxsrxOA6+QDs3uRgrvOcN"
    "xWOyVYQtQS5LPhPsDM+v6zo3ZpOz8AzJ/saOGcKHqLRnG63uThp29zhLn/EMwGyCN7IisJX1OHnctPJgx5o8hDwEPCEytWJtOzhwlQbUT1rMsBYd"
    "yzb21ZGooXmoYq9kZbwRx/NRWnWabVzpt2Di3MCHMsiAgcMRdDppxGoL/P4ZlSuwa8aah+jEmr3WEqBnENQ8IoDvBwlERLicykMkhbFncoqI11Za"
    "YSQOF9sqmqQiaspHvxOqF3YUamoRemi4IJ4wmtxOFg6pCQXA4OG9ROq4P2CqdjOHo3pe3qA3hQ93laScuIQcYS4W1tPwQcP4/HfErGtKDmTauc6M"
    "lf0w7MgT2CkrqfF0dJB2MtNiwkRyeljsjTFTI55MR4nKcjnRl5JccujH8bhmpY3Eco77RXAKHdLZWPg10KuWddbTWmHnM2Ox+hk6ynt7fLdWQbHi"
    "vuF82v1BTp4v3/swOmI+aOykGN3PweHqfZO4B0Ot2RMgFZYsVxBOInVbOLyEz7xOd7tv678WvBAoJcSNiGOqJzdl9cg40PnAttMdGAFVLHQmNd0e"
    "C1KUVGmxsCRr7gQkgzCNkXESryI3qLfeJGWCWEbQMeESjIAUFYRnrB6FYDBe/c5swiXoJC0M4ghnU1IibU+c35KfjE5DM3nZcyNdvG4Hi5yvakUC"
    "Q5exYOBVdsrVWC6tORmF6iMWxzmnGXRAJR38Hvh3K11jH3FQCbeDlAG6L7v6usS9kUQ5L7KmIQH6gWugZzivKVaCayKMjSCxxMG6k5xUAVTDvA2M"
    "vRgOUITxWxP+t/E0phknBD9Wl4CL6sLSKnFJFvYhwHaCUBjWP3OhECeu4ty1hqQxIoNBgURs7oeIj6Eo/iuV51SDYVSSouXotJf5utQYRhHN5kGw"
    "pS1iqQ6xi0MWXWJyMsjnLjm+a241O3JYzP2ejULXpdZ5VppqtDAiQRyRfKzzyR/+y2RE/uGRb9zrSA28QcuDkTsWCrYgJZDkZayi6J8mW4lnkL1U"
    "DR0q9EaTKkG2c44FaFyBs7/QGcoGjIhKxwVJenimqwfaV263g+ur2cappnBZXSzhkBlPTdUU3JScoU/IYgOBkPcoPmeyE2mqVdD6RWtqgcq6TdKD"
    "UiLMeVrPOpkio/grruTFNisSgile3vGigmxcM1esp1nXJ4xUmZna9gBrnmSXANnAmlK5AjMvLg0oHfgl4e4tSaU1OexS+BKebdS73Zx5k1uviX50"
    "IDth2JMMZuba5I/4w395GFCI7I6zkE0Stl/alHq5LUXgTY7i65UCRuVh/LzUET5LpE3rRQeD6gNcntvMQrbbzNqYCdidLE3QI9qz5lhXH1mJuko2"
    "6g6pIBG10sNKa8B1kTSfIIxbi3n+kk1bYWMpIsy0aN3N42BeScot6kvelGaTlzoBz5T8NydDRhPfhi6uv56gGFDOaIWfCuhEu+jkRQBBThxZ85tS"
    "LEQErp5Rfg4cDQ5WcuRzflhMvhqNt3kBNA6bDZbh7NTQpXvKso467FBjr4P19tNFJPdS1qzjwkJRgqDosB15R0ohQS2UUrhNMv5a2kJFoksJmwxC"
    "6jmWVdzw2e7GcFtdE1i1CeZpLtpABV0iyXxVjQ3GgoMK8z4/LG09GRFQl0BG2WIXMlxTgDyCNEK5kpWsP4RTl0eUaHrq0L10lbT/DquXI0AJmT8r"
    "CbPG5KpiOhevzNEiAXo4Jmq+1gBPX0ylGKg0ym5aRXAS9ZGsY7nIBWLyWOWOiHonWdfRrgkwGuENDGD0FZhrf70/+M8yChnNQAqDzxjfw6BGqzdy"
    "8PlgbyzU6G289HewmogXA1IxGwcymh6rejSwj85GOgQ2mhZmC8Yo0ihmdLE9FDL6ataCF71LGbbpWrcGNdq5CoP1+IlQD2tgo/mlm/jSZV+QpVzs"
    "aPi3U4sbvYClXymjMRem5r8KHc0rU4seDZQyAj06o7zFOuTowX8ydDQy5RPDRtOCnBw2Op8INlp2gTFeR0BG0x9yg1yFJm0MMpo2tmsI4niY0c5J"
    "+h1npJldt/dmNPnoew+FjkZXowsbzQ9ppzmJsHw9HQc5WvO5Mzy8hgplnqOBo/GJIM07GWJpTowYbVdDYKNRzA9+C49DjSkfHzbaGYimZPOU59QL"
    "eDr40eGDcQAykrL21wof7cyjOgVMRQXTrkSKXgMh114tpCYZ1p3dDhOjSFvfpaFtfjD/eS1tbRT9KYFI66DB1ibPlPCK5l6s22N2eBwAacGPfpUD"
    "jYWHII2ZQW2qxwEdrCE/HhM+mnOlmkUNcPSr4mufMnZ0ap+KKIobmcBGI3iXTxDfI3KoAEcXUwKOXoYnek40lwid0dFjX1AIi9QE0Pdw70Hcb4NS"
    "yXocs+fB3fWcWDU8DrS2ISjS+u3gncGNJfj64otLLx0fQHqhdHm5+vTaicGQLtMW6nnAzYD5kdegJGQFM8uRsNGwUaA7SgEHJ+dh9AN+FdjoUajR"
    "jrSbCDQ662z02/gLVew6Bbs8li2Gt1jRF9O1PmFRjQSIxhFOBSJ6IwYRnQ9FiN4YgRDN58RARLNyIyDRebsCEn3Z409FBCbaE5fjIkRfSQmcNgCJ"
    "Vl2rHiT6LOpD61n75CDRNO8193cXJlpVCFYlXajoRSJWDxqaGPT40NDrrEG72NBFCA1NQw6Hhj7LTC7kOCMRos8yzvIIMOiNChi0Ve5HIkIjUffI"
    "y3gsROjz51iqHwcPWknIx4Omv67nw/Gg1eygug+78VFMaKMgrIIYOrOVbhVDgKHNxarNR0ChV2AdN0jlJ0w/Y8WEsNB/10+b7AQ6W0GFHnwRgYVW"
    "fjsEGHpBNiuAhR6OCm00EwcUehnlQ4AITXaegwddBHDQRQe9VKkLCX0J5htBgS7Ee+8paR4WdDEUCjoqOuJI0EuubMgZhTl1UaDxg4I2Kwg0Yz0X"
    "ivUcA4IuTgoEPfhtHAba3+dThYFetKdDTaqUNJevAQvacNoTYUHzKIwF7TP6Y+NBY/H64HM0ECbCg0ZRcFJA6ELwoHkvcP3LrF9SCg2QcMsJfIjg"
    "+bNhQlMZirrwfVPLMdqxSmvw+6T42pChFxxvHSi9fe/RMKxjczq40EUMF9pBheb3mggV2k0ISgI3BijHNZjQUbbIv9aiQmfsUuFrjosK7Xo61Nfj"
    "JJSfDBo69VyJVWe91/7nxKjQlG+kPuPpYUI7Jr5yyvmE4zPZ4GGTjB8a+VqRexCS7cSIV9dtNVUwaOPpDVSKZEEeGEJB94rSTrL0ZzkJCjSHYOwL"
    "ZmpNGoM3IKOTYD4HHp1UYJ/BhGAfJZzWfledMWTIt6zjX2dYj/p8vkMr0ssxXIOp59InJI77LBtq1a0o6nN0zNTVvoeAP/Pc0VAfCvwsHuIRwM8c"
    "LOHcMYz7eHpxHPs5q4A/696WXmDm1OCfl8yuYbJ0ivBujj3ioD5bapMzVvSnAPi8YFwjLgsDeZZWqZxnoVApHDuCsTJGnzk5znN8LsRrujmVrEkx"
    "acpOOifqgBFA9bCdEN/ZdSlVQZ5zA/KMQ1pnvX4X6H2ngPNMjCxN8ja6LEsOowjS8zhb9U1Cd27XoDu3vQ0GYffnRnc2+zkC3dmlHZcijASdJshz"
    "Fh+D1VNXNuN6RsgFRs5PBd4ZnuPiPzB3k3lh2my7Vq1uGr1GUZ6FkG2k2mfq4yM9D0V5zsEK8UzV6UM8W3jnYjuVwsao318jEXCNswhn0lIOjD6k"
    "fwKY5w67l6PP5wFgwyRPUfWlMZGem+mpQj0vKLNHsSChmiZ1j73W6r9q04rQsjURl2niO8Ognebk+M4RreJbC/H8nPoQXchgmnCmWMFAqv2OQXbO"
    "WxspsyHOluTDzg6U1EF3lvwBeIWyhKcO7mL9C5qbXcpKoqrol/spFzwIHSies9yLyW05Wm2pB+esDIRtm1XySCTEpzTE8pcD6Fy7PY1gd1DNgksG"
    "d7cQTtjx8GgiB+WfrMLDbE4qpgAyiPPLfWbDjOKc444xhLO4LFGTKWl/4IhJyCzAcKY3U/DmjLFo2tZFLZlb6CU8IY6zHl7efucEU7VCe0wU52E6"
    "53DsZjFMCLu5REo8DnozIQpfubr0w4VkYWXx8rkTwTdboGIPu9kfnjyj/2Px7Escrz23gOMsrtAFyysL5xZOgNu8sHL+8gv4jIWVwbvJ0vRRmxeu"
    "LF5eWHZwmxfxpqHvfRnfUl/+GJDNV+AsvYp0tgWKYOGmMthbOyD+OW8fxfnxQJs1khAFbV6jTHP8v72aUwjHxmwuRkIpgRm0MfjsOIDNHNn2Lbgs"
    "PE0k3Z0sEwyjf034zFbOwy8EbRd6dyOgzPiEOCSzsME280EDyqw7eAJQZptrw8iAdVry3AidcWqwzJ0xJjKeGTgaj1m833gvq1YqxuoRmeN+Z6zZ"
    "yacGypwpJjPnX10HaSagzIUhLDg/69J1drpgzG2GiM1DNGa/EKCN35U9ch+q6YOdqzAi/42EYW47MMy01bRluPuFG8ayZDeb/F0/wwNHpibqZXIj"
    "nGN5Q3S2tYoYVLN1iHKqnk4dy0OEVkzid5uSJKuW9bcUi3nJq/hirlcTrfHDX6zgcW6bPfwaBxB/VehNRKxsVPhAyae1c+B7yqrvCr5ltR5e0MUb"
    "dUxU1kPbGfMdUI2nBcu8EcAya/qbqLZ66Bqa2N3LYtG2qWAyLyW1fh83/jb4bczfg7xgu1gb/KekP2X9bx0ic3sYInM7gsjcTmlqFD/xyhwSMj1B"
    "ZAkoczsAZbblxXI9EJ2BZe7jvhvvghMGbRanC8jsjdUQArSIuR2uy6EKVHjzni8okVmpmDQxnxF4zKKs9UaI3FNDZG4PQWRuG6aS67lrVvnMlKCY"
    "J9G2Rk7/tLCYs9VJeeO0kJg92fEs7LNPpQ4Asys4auVLlFXVIjCLN7NmLDfX8y8fefm4nveOTUMvPX/wXFLUoTAbkY07GT8OpPhmisI8+Nxz0Crm"
    "FiHu4cwZgLlNpR9b4jPxVycbtjb94OylPMrviq8Zf3mhpOXD/xoUZPUACe5yTgFszFVHfSbIR+sUtiI3qPGYTypDKrAy73Opmy0FmaeIuLw0mZdg"
    "vq7uRZ5p1XJ+NPrtJ4JexnIAAV6WpeElJv8y8jzCXi4lCXME9nLpVBJNhL1M0MudYkLc5b4CL5dCJsBZND12TORlvlPxllzs5TT0G40JvdweCr3s"
    "lZtGcZdzCaIHlZwV3GXZLdx+VIhqYJcx2WVwF5OvDepyeyTqcoGgy9vjgi77bikuUh0NumxCl1bjqMVbLv6seMtpkKYmkMtFZWyubKdsB3wEGYNc"
    "DgjWyauUipEq2rIN5UThlslz6VZxnibgchHgLdMRsoDLjnYo4qrh55Kg4XkStGUDtSyHQ5LoosThwiwvM5YxwSynJ4ZZdkbzy/UKLtdzcI51F331"
    "9tgQyyd68pTgldMQXrnt3J3iUfAKM6cIr9zGff6WoSsXUXRl/Emfnlk9D7+2xXSGpucdmDgNyZMoR/BkJgTgHw4tiDt/PFDlDYR9reaJTIKpzPbB"
    "yzEWPDamclxvnhxZGbFMBN4jln4xLqqy5P+nRVJbhfyNwlZeqtP+OqDpEhRYv/5NJkBZJohlTP8MwJW7SKho5EyMrSyYvwWj8J4DmxRoqdnfAj1k"
    "rcW2S9tDX+wL3G+WFDFw5QzxDy8XLrhyw0QK69GVB+864eMiBFhuBwDL/aSoBVimAv/fK8Qyvlo/WU1RrBcRbOUl3470AnNxaOV8GLaypwkwurIr"
    "KNy19uCVz2IpHbv5fYBldhNQnggvOz3E5NQS7uvgswlglvsGBQx9JPJUdZp4OMvnIymYqmKINyZVfE+J+VrEZVhvnKibD8QSkiM3xF0C4OVz+JCs"
    "FnQ5L+fVyiZAiyIvzwjb4sptAmPWptgB8DLjLrfrcZdxBHKnUvMNPEn9driXcezlkHlTVXYt8HLlanQUGU4wm4CVB7ImAFt2bF8bNS5hM93y9e3B"
    "f7ZNCXh7i6RUt4LBrEQOgr0cfLGNGi4mp3edELAiMRc+6iYsy4/RtBmGwrwQul30cabQPPWAmJd8HGazfBTIiwExp2i3NKvnBM443DEMi3mpBn1Z"
    "y/4zrRePwzE7OEbG42RrlQ0mc5eNWQ+XmXpV1eIyS+r/EFxmvAJxmbc9zCQflxkhyzDzUoGZ+23BYhYqc7GYfc+RojKbrZL8oZTjABV6tSPRHVuD"
    "e5LCZrIVCaj5WlSz8TCaq6TIVJJjyMS/LdHycMFqdp2/Ab92sJp9kCnjO8gRqrnwsSczhwIabjwgY7PQwuoNPid7h1w34vBzRH9vHLBmclTa/DGD"
    "1hwBPNGYDAGgMaetAjQD5XuYzBQ7jkMy++xanAIEy8TvN/gM9sECMis/VDTmJvBSewazQC/oU2RT4iYuJnPihZG6NRDNwv/7bQvP3I/hM9eCM9O9"
    "IThz9P0WhMlyih4dMFhhdaUzIPYalkJ3ctZEfWxmors4NvNGWlO84BjnrlDkYJbAqdopikRidr6VrhWMLhpANMtWu5EbwxFtkc1sgoXglA1ZcqEZ"
    "+VXxb/QyOvzEpBajZzFp6u6Pj8ucbSsuMy+vLStjyeYkCzb9CiZJXUAzBr3HrXzd93I6co+qMTGFSc5zF9+Enew9AQbC41HUgDRLulMF1mW+NnhA"
    "lQSYZVrBZiYmgX4VRWa28KD9GkzmtpPvD8bmxIjMC67hYFGZOeXXxdfK/KgYVSFrYQ+npBJaMtd+NGrTGBS/w8004cjfGIDMzhMqsTEPjplOdJM8"
    "y1WEMPbbww53pVjPlAdinFqIH35exaWkWQZ15CMBmNH/p/kcTniCs4nwV3G54lzcbEej1xceBHPqF+NSZLpQsIOO+h5rYJhPl4PUoDHXhhcZk5lE"
    "AccYOOFL9ae2wN6/iksgDknPT9lJYQVbDsDtS+3q/tje70E6F3lmOY+dpqdgcCnq5u1im/IBKFS7SpjMlEs9EpV5yVXsUfvo57iCmBahJ6qRrAss"
    "M7p5zLqbeLOAMmd9p3o4c9MoiR+1MsMWa2i44xmMQsNcXh7AMi84qMx0WhKGZJbsWRctNiFI5rUqJDO+oDnYSxEsZkqPF9C/0ttHIkU5pSXz3z+9"
    "8ZsAaulPb3xMETxGJCXuXXpwTmlZgWLmS1k19HGY24rDPISpMmL/9ohMwB8PPnOzAQOK/KFTieUl47hqsqSYskIRUQldYLEGkUIkgceP2NZDLfsp"
    "Ke10eGxbOVfppm0wczSwy6a7R/z8aRmdlwij1Tu1p9MsaZO4LkMuD4nu8mGyz6hFYEZfs4Fg5sweRKXh6gZCYK4PyIMm91k3Sz11RrMDaJA9H385"
    "ixGjd5zarNUPxV5eCtZllRGE8T30tJvT4Hb5A2Ew+IKsuHSO2AlJRWB6MDRDLxNjCUSK625OxbSNIS8T5fwn0p1zM7Mukb9RMIfMKGPMx9BIs8DL"
    "Hs9D0WghusOCfd0jA77sKCSlgV9eiqMv0xhwhridhwn4g4GenI1lcvjYfhTjc8hZNCRX+7IwzLYMsdCD6sGGjABhXvA4HvJSQkxiRkyGMG20C5ZX"
    "YYuZA96DCbhOEYXVoQl9udd10JdXBgfdzcHnWRR7+avd9vW0le6kHRd6+QJbvK2sOwp2+WzaaX11O9lMd766jZkiyVq+kV5vUReqKtzyStr56vZm"
    "sj446LQGB199OjiIQi1fyP/4aS5fwBzyKtLyi2lrE1Zr8DkOt4mj9iJwy5cGBxvw8vAoYMcMI1YBW34BjJ02PI+v6Mdhll8YfNmFOfcGB61sBywK"
    "+HHwORwhB2V5cOurTzNesKhObr7MYcHLr277CMu0LnXoyvSWYAyn2E8EVmY7wFfWCwi3L4KwfCHd6aSb/FXa4WdHSPRSurnax62D/dxJN4EqQnhl"
    "pKSs185qGNyFwQFQ7kELl6k9OIA1ZbJgagiU6wtMMdcR1592OAqu/GJWplsJHOv1HAkBdOAkv/bHT2UB6yGWz6VffQrDI3X0gLp4aXwN72pKnAZI"
    "pEtkeAxcZTk8sGCdBrwrt3EGMujSXPE0bHpvidNvFl992sW+O215iaHgyjvFZvJMVm7mSfOr2/DeSbrZw+e1R4MqI53h0TQ4D2h7ZX/8tAX/z7sj"
    "EJVXs1aORatYzDgxnvLm4MtNOC2Dg+uZvHkr69AZwzmNjaaMFyeb2velyZNxSnmyTTyMnRPhKNMzSr5tEzdErwJCWsWF3gFtBM5HqjOg1zgdLOXa"
    "ucCO5xsouRrJ9RRh95tpex0v6GA7wrLodL05VmY4DpAy3y+rDfxyNQVqg/eHp1yfAn4yD9/sd/vtfmVPk2eYraGfU4cAwp8UP3kVCQLGy+Y82OTN"
    "ot3v9Tv9BKtk8BABV+ATm3absoZ2nNrLJ4ZYNkDIadnM4QC3s+21Plw43rOOD7aMOlCnne1klteg1g6se3Aw77AffJ4ZwKcrXP0pIS0/R4y4jWQU"
    "eQjwgDn52vB4ZtjANtdgJeB/SZliISI26cJFgq+GoCufW/rqk6svXVy4tJA8t/DHTxaunl8+/w/Hh1dWBo/cfaeJ9AqzWE13eiwlV/uVyYKU3iAO"
    "DcrcKrx7Kx0PZZkUChx9M93CWknQAfGdMRaQtmG7miQr4gjLm3BM2zmtTnssaGWWvSgcVvMuaGNfXm+hCYXSvcxlXyyo8nMFCI3+Zj2q8gs8ADJ5"
    "IrsSh2eh76Mqn0XdkP6A54xCU4Yffyw/bnbyzSTdwVXt6cgxNOWV6JUWTvk5Ohr5DmmCBKb8Ik61a+CUF7ezXgVP+ULArqqAysu00SDR23qIfVDl"
    "c3nLIiqzNjansMorhQ+qvIy74AIqX8a2uQ6e8jJOOUBTviDUSZNz0ZSXOumOoR4fTVl+kkl7YMqLrCW0RZ9VHOULRJoOjvK5otxJXe2utMRF33o4"
    "ymX6Y/7WgVEm/Y6/FSBlGtOBUYblCL0+/2D5CJ1D3wlmZingyc8NDnYGB5vf22TtdBN0uu41H01ZaVXpaMEnIBdSmThCDZryOdD9clw2EsGu7uvg"
    "KZ8jPQ7GbwKDAEpJN/ExHSFqgVh+DqRviy0Ci7F8Lt1Okwt5u5XDY3yY5XNZJ+sBx6iCLF8Akdvq0/76+Movptfh6WT5zcXhlS+QWSUmR16BVV4u"
    "NlaznqeXttMYpDLr8JXrIojKyC26aJG38nYCTCXr5SGY8g/BMEmupB0wEBwgZVov2I6vbg8+99GUV5B/WiBlIh0PSVk2rQfqOR8fxVN+MSXU4yqe"
    "8gItiIM7q1jK3ik0gMrPOZqUh6tM6+LgKvOCigmpuMpZc6cCq6wM6TIwajEiDKAyc5daROULvqiIQykLPycdsJUy7zAwysiqwNbEw8G/WDRl+Ak1"
    "vFazX8FSvgAMv9PLd7KkD/qHYTkBpvJzzEd76FCAG3ghK8jK7mZHkZVXPJkZhVa2X6pCxDJcVnNSgGXWE2Da5hb2ScA3x0NWXgd1AMzIvBIzI/ao"
    "LdHU1DwZunKThnR+zJT9k5AeiaosNi78tipsa3xAZZAJJwRT3sBT1JCh0i7uwiab5LD4ZAMLBU+KoVwSMRI0dhMRro4HoKy2TgfPKs2rgb98B10B"
    "eGGn3+ZJk4bJ9qYa6aynTB89WbxwYl2S+k12EI0ZTgjVw24TTQfQdnmrG/gx8EeQol505CYyqgyQMpuoTVHcR0EqGwsFH45YB+LEy4J1qeIqe2uN"
    "FsZwRGUYG7/ppdiyPN1IT4CrTKb7tno7PAO3mZ8MVblQNVhWVv2H8YeMA6n8AntfN3v0/t9Bw0qv5f2dGqAysUUy/dhfOg9CHXgWGjdABCB3eeWQ"
    "2FjLaKHHDD6hSqTWsIqZaQEpG17tqBLqz5238+hhaAPrWDaV7sg4szrd2ODJPKTLszF/2LUcrdVY3dWTIClvsuOXJ5DRSSbEsQz9JAyrzB+3MYew"
    "U9IxI/dugJm8wPNL+jugSrbT67B8aNZXAZNZPDVDnSoKmkwbERkyApV8wVrfsEB0A+IedfIAMHnwDjA2cmxsFqSF1KMli3a7CcZtv6VmhAuQDHZD"
    "T05KCJBsgyZ252IAyWkXYwXXRec8PkAya5wNj2Tgoek14bQs5pBh4hLSV4iE6O0DWyXwcQqIybxz5tUbpE9ad80miVycSpzIVRKcHC65MpFCjFqh"
    "gVa2WYK46BgHGzndkxLtLvafwhkHcuqh2trmDyeDThZlKNfAgNwoAQDnVkoWUV3uO6LFnQJW8pibs4VW2WaSX88pTrCag/K52fvzQCUHI7jOUd4/"
    "co7FobS2s3BapwqVbASCvahpnSIjoJJVa2BxuOlRwtQgkutGIUrAkKLd+Z2o+G2L/jxtiOTn+iKYxDeNBXrIEHNxSjLrTSpKHa1WO7s+LzaWG03u"
    "wDCOQdeZCB7Zv8LTg3mPY7Eh9ur3+qcKmJw2s17oPTcGpsYVVvsd9kqbMbczYC8hRATFHFo6fUfdmAQ82ewdAcFbKRdGEMYCTOaL4JioeSQ/eSLO"
    "ZeziYD0WeLL9g4dEggJRkZLWwBLBD8bAQx1BcgLwZLkYnUFETOak2Zeyo4wDqByEcljkhLL22wWrPLh1HauN1BFGk8W12sZ4LrCpFsH3Ersluz9Z"
    "zzpZiwMl2SYxDjm3pA1RG3k86Lj4wOh2kK2h8pE8128kwKXhCF2Hg1IZi1MGyAXZInerpJpsggI6+LJFWQ4ZBtq6ZBavW4tqdfDlDsvPpDn4EmvE"
    "bDjlLwNbuWaPGqxV4VmVPcJdw5VdRcVjEwO57KVhLgWmiWpieA9vG+kqvKYdDHvASspytxvEaAafA6PoIdHLDEB/a9MAG9lWibtM4qFJe6YxO3LH"
    "445IbA3kYLaJSnH3hJDK7pF2zzNKTLwbmcbmeMjKS67iqvSXo+FJWUZxYOUX8EVauTVihiMqX1i4fH4l+WoXrKTdy8nC8gsLV7/aTTBKunJx4Wpy"
    "YeHqHz85f3Hh8rnzx8ZUHv8ROI5Gay9fOv/HT5KVpSsUuP1q94+fXFy89NXuMaCVvScat8aFhb8/d/6yvWdWvlmAf89V3nximOXlhXOL8MVzg9+s"
    "DH5z+eLgNxfwpnGX4tICvv0xoJaX0au2CawJqA3xu/UncmYAL9tEVRKZkR3JJBwAt+zCCa3mHcQRmDUiwCxNVNQI9LKJHHDIWM3qsVGXw4QXcin6"
    "nkaSx2xkObrX+ODLz2GJRhrmQWwA20AOEZy8IFVFLOivCYY5LddhHYS7OB468gI6tCxfgTIHL+bqFcKFSqETq8ey/cTpCfCy68xGTobFXFXGBSUQ"
    "rCE2teeGa6bTxGEebzKR8VCPmQiJ+QLJNTfro0w38i30KnP8Nl5Ms6zWV2jeTIzCvMBUInsIRjvnHiIxww1wwFEbRyGJ3iqq9NmUHFbXmTldHObB"
    "b1Bkd9YwjwwPFerxoB8AcyD3Xdm3z0Za1mTDrMMnv5fJ0YZ5N/tffcoMaycHHtJrg+SGw9j9JuEzf7W7ie4delehhIZnlWpgjLxzqPXA7oP9BSP3"
    "URV13b857GyiaigyN3j9RmCjq3PG2vD0oZqFZKjLRGXQB0yFTy1ewm8hRvOF4MQYxldY0UD6aNT3SPmc7C5lzu85GzhB0Y3Bka3gjmqtBtevtmoN"
    "YrQQkHnhnm+monfi8iFgBfBlJgN8BtxEWW87GJDn2eBBxQPLE8ENYy6tWW8nAXFeNuE5VoSRIXBODJ1UOqUJhwzQLN7wvdcnR2529yMcoyHh1qY5"
    "JNcDoveDf98mzGaWKTUz5B+DCdI89BdG6txE/b5DGUmwJsVmv5N2hLlKScWXwDK6eZk39CudsAmgUtxpp6L74CjyBpKrOlXo5ufsJF2HjuFdfuwR"
    "3g9/9R+bkrcebf4uzpby6MmgRF9F3vNPt+O6Ho7svOmLbuYfMlN2X50OpnMNZ2I9l1Zn05MlyF+ij/6OJw2mhPKMehJV6fV0KhE3K+ZY2/GYUk8R"
    "5Pm5CndtjMFeKVs47STuFKYF9izXUvD82e9kNRKoytNCdS9I97Bq/TCw54pLvNT8U8l4+guHeB4eOaisDvG8wD2tQYQ5TVqhtBb2SdlYYZISzyUJ"
    "3wSlrOUdgkxls/HfzvpWBvni3bfeHobdLDaRf6iU/YtJ/9Wn6OJiWUCCwA12fC3AzhforKm00ZosUtvxj4Zbc+CGWfWx3yFnPogvibbO///kvetz"
    "Xdd1J/ivnHI+hJ6B4LHb4w/gJ5pSS4peHJHOjKe6ynUJXBFXeBAB7rVNuzwlwCQASXQrikU7bSmjUAQJECIJAnyC6oaqIid/A0B+kfov6b2ee619"
    "9jn3XABUJKcSiyRwzj77sfZ6r/UrxqBOaFoqhMzInEdusqqfVhvn/bkdjsYxjNpEX5PYgie7Rj2cIT0H+2Zh+rXlc2chTA32eqeLibG1DZxfw4d5"
    "FZhuPG2KhDAro7qHc7wUXamyrG3ebFMyuyAzwAHblhlzFnWDHs7iP7KUA/bqNNb6xLFy3Zsx8/XPH7c4zcVat5kOzqNUt8q1D5nezWekLjQQ65Tm"
    "maeNm+nf5C1it1i5bzOn4bS7nYnwP9Ytck2b2WEdtG6qv4zfzfdtnor1rT5ILuUjNY2bT7lcElH7yp1D058kLZv5Tjy9hs00Jie9lUfEzKXTkD1K"
    "/ING4QpEkcvwSc7AsJm1vk8z1YP+HHXop9Cg2WUtsz0OckUbJ1Nm2Eg0RqP6Bwv3B3yOciPDI0FdmQh6cLAhudxowMbNmg5nldLTQRZN5yeY794c"
    "f0SW6wFaN8dB6goFS12SuWBwXz2baz+J4lxbKpe/uN9+zaX35AUjh85hrQ+5cody6QeSAx4sGcm1O3ArZ8hIAYYWvibRUxjlzT9vfgvaOidfDdem"
    "/fPZzhTbVkWaXJy1xKR078+bRyEtMhwN3THQdOw1lDyqibNhFRRW8OTzq2YdnuMjlfW3fdo7p6smEdO0sXM5R33gns7/r1eve+d47g16OVMOn6t7"
    "dp0KvjkNnP0iOevbThw0/gbfl7zi1hinKWDMO/dRYbpB6YfQ2xjUBk4X59rdic4kF8u2Z0c744He2rMVLZwTk2SaSkppsqjZIckP+1aM/Dgkw3Te"
    "CBoiFlWAkUFmStCaQEyVzB1Q5WfhYs+hYUYF+sO2z7M8MuYbPaeRSN/42TV2BsPItX7GGXUxs2MaO8DMJkU9FBwBV+4LHOb714/b54pzOMHpcE1p"
    "iA4x0fDvTA9oLvoy3RvCwWV6P/u2z25zgiJ5rhd2A1s+U7eR6V7aEKKoO65oW/3Kt4b+4g/Z8wikcnayxyLsHBYsz7bCSuPpUBILJE78Kt8f+nSv"
    "dMgyCzD0z7WsgZL9/HQvGCzhxGPTaCyvjJ4bsEzEVyOBC5OOKv2iO5Jzbdk4G4dcSZk0i/7RD8EOm+yiVwjaxIRHIPaK0zkqQWqUd8FkQe4XyDPY"
    "QfCftnG5npZwSewYDV7NcCXmgq1B1GNONVxQvAQcxKq6LFhzMG0bRj9r6vV73dZ0i8SLlhUmHaNjecVY7sXhAtPh0XqVhOgZTE0NbGW63SXah86f"
    "rS5amhyOgMjArB4Km922QfQp/MRErIkHRSmMc3a6N9qDYWaAtc9CAo98UvwTtif0n28bc3S4sIvnAj69ZNoMGr7xxSosoWJXA81JNVOuNzRzXjyx"
    "6k7QZD61dYHAOr74Q5h5IJM5ncEEXuDZfC9oUyLgeYbpBP1Sa6bVRTLHeDy1g+72/vXjHmogc7xn3O+5VNvg20H7X0Mv6NOxgEEUCxQZolpMAon8"
    "YMT0d+5g3ctke6aQVgfoT4PkolJ6E7FM6I3ejlHsNHWSDhB6PRsKtaqNbfacIQAZQD1+nTR4MdE6HSYHceFzdJdMb+fn7LpHYsQh9RBqxAQquLwi"
    "M9751VRQhEHzC9QGvX6xBiWYl07wD3MTZ+unA/fgBEpWjQRhY4LRlnRzNoloRzVaEzdqDrPkTL2E6+jMIjBoenP10u8cujlo7p1ZZrvgkOjCFecZ"
    "Qf4vSOo/3ybHQSB06efMXI6Sq42SQPcMVN5zPVYLKKKSUySAjTE7na5o7fwyuvCY6KDiklIC1YOLZI2s23Z1fr5qZafLakCcQXGiNdHuipcEYhzA"
    "poYg0Rf9dhNS/Qla2hTEFcDYmgvX3VaJSLNnLHoqtXqOHMBG5KNgCzqdixpjsc7kUPmsrIhMGjxrj4ySjNbKnylmw7OkfJzEQjeOBVpX9/TZ7qQ6"
    "G9Dlhy5PPXwNT7WELU67Vs/hihJrHJKrilFx3FieVEv7lIUTQqIuylVY0h4E8j3Rpc8Hwbkivj6O/OHQUBoyLTH+ws9Nw0cn2Xk4yo5zTjSZzXd9"
    "Hsp3nhmD25nnHZywztzD5LTAlPTWI/UmYd+p2GvNpYrQLhMXgkyFyXCIEx2272cbNX+WKnJ1mUlOWzZKGlspn+sVUs0YK8vLUTWOwRaqU2IuwWyS"
    "x+LjHpR2iP6KJF7hi9tfaPO4sS5Up8ct3dvkDJZSdVtUabMEwpG5oJA4cc61Zoiw8Yd0SToTYSeAVrXuHZxpZ3/Vms30hIYpSriInLRSdgfODM0t"
    "QYtO8y6H2OE3JIcyTSRCPklkQOfIyovk3Z4t935+aiwln6T2bGu8VU5mwSC+i4vkom4Aqdei+LE6NEtZUOi3BdIJA+jmw5s4yrl8Yg8G42Bm1Phs"
    "jtpdRV6Q1J/GX0nq0+xwvhfgUKxLRtcQ7PJUrJbTZUQLlqOQkexdxYoWFvIWycXkloMstJUZHiXrwRKpJ+GEWmUYpdRSD5whCW/QnYnJu4nnC6kJ"
    "mXq3i6u36bty68IxmcLxoHT1pimnkDovSNkFvPFfvnPGdIQa6/yX74jeLTcYWSqcjQmdBGWyzT88Dbx9lsUUv2p08bQfUANO2xvi5H+ALBjvTIrY"
    "t0R1tjr7MJKOsvW/7sR01qj1wc6eNi3PePLpBXT6I6jdaV7QX9N2pDFi8yFgnLZ6y7eHjkk3SSai8NWyHJsWdROnCLrOaA/Am0DyQStwW6AQE49i"
    "/gKgRVH22pDfVxaPYpahmQlKyFjtRvvuUcB2idDOUHiUfRjhEgDb16xGSQ89WhHFz+ay4FYjnwP7jsYFgxhK5tuzYccnWCBTkhAdqLlYGaI9hz3c"
    "o6JT0THVd4yKY9NibMMB249ATaAw8khJYp8LhAbMf5xaa8FD6OKQimSnQgFF17RtHSq3n3BtDJQVTnTwA6gPBFWTKrbAJIsuRs1wlLMWbeyoFMBS"
    "AsHpnv9GSQOBndADlK4Gdk+Gi4omW2Y75wAxrM0pBlQSlu9UqPpc9joZ5xzpQaYOE+aZdElJKi4rekVj0ydT7jQVJwE0FX6jqqe2q1B9LvLJeOrk"
    "xIHG0C3bGHp3de/87vbu5u7a3ju717PtoeGRvQt7y3sLe+/vbtsW0bvb4efnw4uru+sFjrS+ezM8ttCvYzQ/e2f3xt47e+cL+sLuWhjn7u5msbeM"
    "v78Sfru0u4WzKreRDi8uh6+bb9/dWwpvbmS7SeM85+nZdVhveH2+4M/c3b0VfnOv3GEaf78BK+RJhjdX9y5kukzvru8twKAw+wthuHWYXK7VtHkQ"
    "B4QtOJ9vOB3mBAPBCjf16+Gk7puO0/TjvUWY/+5mVd9pnM5CGGm7CF9f3b0W5nidhoRjX8X3153woB0N/13CHc31pObd2wwbL5sJZLJ7L3xsPmlP"
    "Hb5yD3+YaU0dJrO5eyPMjcng3u7GbkV7aqIbXMMDmv9VGBn/Ritwvar553fCK4tIXQ8qeHA8CiUnnMijMLPrZQNg9w48Hv53vfBvVrWwxgF/GzYq"
    "bFM4LXrrZnhvdXettoc1Pwhbej7u8BZeQ6++Iq1cKHSHkMb219La3uRAzjJfJSJY6e5Fuabr4ey2dq/FH9ZsTm2f691HfH/CGDfgJhdHwpCBGujH"
    "C/CXvQv9m16Hl9Z3H8DW4vTrib6I3C0s7Hqfltg6RdyM+fDXQfti+50UStsMM14Dkl4Lm3k7nN1vG3fITgaE4Yrwt0gL5hz3lkaKcGPvBzLUEQ7S"
    "ORtYbtjEDdlXsy49y/PhEq3CAzfDr9/ODHOI3bN3r+y9Bx+E9RfVk9ub33uHRw0UG/Z8O9AaPoNUw8eyu4Vb9s7gfbQDYdwVgVG+Rld5Sy4fQkvt"
    "2tNOPlccgWtYgNwMRLYRh8Xt8Mx80LbbcMvCXBZ2r4+EywaTWQtTuQsnETbCvAz7/Wn4vXl70J7acJC4AHvAa7gJvw1H/E641x9WTEK/uP/O2oEi"
    "loFAzLeVJ4BaAVwhfN7tdCQrIanw8EqQBxsFMyOd+iF13Mbvx416AKzazSDMO8wBBOMCcOoRPn9kg8AVwy+v7N4Kr93GJ4GYQFht82UKv74BC65u"
    "wp25A/tvwR1G2CT+WJJDzNDDf8MuWuF9M5D18u5DIo4LYTrw25vA/jaIH8F7N0g8LO3e3ltq1KI7jPRbuG2wtPt6yQLJhSMO106+Hb6xUdmquyTT"
    "SYDuvdOob7e78kaFvgJkNY87hWe7CRMKG3M9NvEOvwa5er26i7dwAaACGP+RKqrIyW/SjpZ6eqfy1Wrutf29+TxBMb8XLYF5plAe6x6aGNcr+n3X"
    "DuE6f5cuqjQAh9ui7b/DWW6j6u4bgFdx2nIj8JKOgNMwncBxgsCUr8eG4EBK0g0cWPbe274jOBPWBmuj3Bac9as1VCKlNzhbCkSBpj843ncyNmx3"
    "cLuiK4ENvYPv+TbhcUnItVyfcJ4Z61us50m3cHs5TM9wISiyyFzn8JLKaBxA+LtNZETXcB2mibjVqPlNbiZOH4rdxGlOwMVTHyKpAJFXGiUA9904"
    "V3nDHoXH+XfUaJynAf+9bvqL4+0J7CfcHjFTqug36TXuOV5F0/GM+QKGIymDqA4/YmvANCHngwchgCpQkGYg00wHcjEuUdFfdH3I+RLNF8mCTT9y"
    "VW1XwbgrdyVnIljcfQiMo9SbnJjr1fB7YNw38u3JE/MTmDtPxPcpN3YE2fThtY2gGlzP9SpPH452WqZdeZjmApgbYQY0Y3GJiNYJphDYLWkT8/DT"
    "5TD0dbuDfHm4oALJcGP3im9mHi7gKnwi9jPHjQTBve6amtuLDSoQEYB0Ng/m4gMcutzbXOJqyKV0g02P8zhyELK7D22jcxL7rsV5sofS6dydg1x1"
    "anhOC6J7jia763we6HEhzP16SbeQIpDEjXBiYCGc74iOh3E5WmwsXm1fdPaSLSMxBF4ZjmTvXbxSsUE6y4UF3FHfIB1/BWvbLrdFN1IFBGKuJzpR"
    "i7VufEt0NHnX95ZQtmQ7onvlSGwJfXQ/XdHlSsZXvMG9z97o7PO5WQofpy6JIsoa5tQH6JLO44QjxTlEL0Ocdt9O6cSndQzHYpv2TCchiNu6/8bp"
    "ouPx1SyOWPH5XUz+BgMqWs0sx2lXVQwHerqwj87qwhZpCVEl2m+Pde/0WTQuwsCSwj0X/0MUlfg+8mwY4Wn0WA+bdEU+ya5U932gKOeKCHu9tLes"
    "HolPApPeZIKhJ8FSAcuOiFyklDZZb9JavcozBAbrctl1hk+iazHbbj3LjAswIMJXajuv7y0jhV2BNSJHGrzvep3bQ1jAdXVTRkKmH6ib8mC92Wsn"
    "Ef1h4B5x1GeNmwEatycshL6Fw+g70Z8j+v7hdHKHBSLFbRj3HkeFdj/EjUDPAd69zcAu0A69ibvwtnI6iFMUaLDnggcaYzq0Vu8uivIvnzq1K8z0"
    "PnoOVhOp9C+fwYKyQQExdK7TgkEXw4NIlaXGreGrCChScLJXGPdSf4bxxhywU3xU1uGbmdDePZKhcoFuhkfX3HnvvVt1sqqNJU3lgdGRjSJchw+C"
    "11fuLi+OD1ZpjXyv6jGf/4YzqjLt5oFSi+hHSprMh/Ve2N0S7rgJjrbaTvMQ1wwPPUjNFNtsXrnSKhtErt986czNZUmbzkeLQGYIccMbyGj234Fe"
    "XSDGLWTJEmy52+CIWizoHhHXe2dvqeQzPGDv+WQvLG8H+VlxPejZ28gckS0F2wWcgzo9cIeGPw+nLT3RKdivd9H7Xj1n1LlvgUgwtuM6zNmGiG5g"
    "XGzb6rTvoQbwPhA0b/Tu6sE61+d8q8oBs9E95VKkvnhHoLL/d+L7ed2cLcCn0Pue1Zi1wL0uJN7r6ChJCELlgZDEv0sL/OwXcd7pF/EcJNDhPxzk"
    "2FNsfV8iEHm0dLJ92uBnHPtZWhF14tC64zt6KA2kDjTgfFHQrQPPWFOastGGp9Akn4NJcpWsEcDRqKhxKjumPSOtM5pDQOKgC91NlUQTMitrIk5h"
    "FcnVvKd+okfhmN8vyMttOqSiY2uRHuAEANhb5804/Pb6GqSToTXf54gs9rvlAB6qu6n5hJYzeFNvAUcPm6lfhsBaptVp0077/aKJUb6XrUSrkjbq"
    "xC/6FccCYD+WUS9cL+j9wCCXcaFg9umL+2zFL18T5lV2n4oYJIK9EzWPbYrCiSj8FJwVdvB9d+k3jnG+SZfFSbsRb8FiIF7xXCCjEzv/Fvjxm/Tu"
    "r9TohNdJsOVb1Lwfj3IdElgiw4Yw+adRn8Bcu2hFgFq8hryemX5e3eEAxTvCEiBuQP6rdfQ2vAMcehnl+IbyPZLfan2KpytQClA3nNrSMGgtfL8u"
    "hB8uFiiCwunTnb5KoXQwXDfA3Cs4Vr9YIF1ugf/qU6tO2NyiyJdzn/6Xz+hbG0LqfAmAFy9zBD/8H4WZKUZdskmTqC8/KNJhAWazd/4vB3cA+FIg"
    "oNtFGj04LNJajo5Nf3Dhvs8DTRQxPG4cMBrpgf/ps6DwnsfTIOkNxjUfDJGYCEHNH0BOBsf7X4Nafx5eu0u0AifKnBA/C1wZP4wC51Okt8tEDjG4"
    "dTBkAx/xbsYNgaVBAGR3oxniQSPOX2PtVKIiMC+ONjd4btD3QyGbGoSE/OL4Ni0nihCmJWYkxsre0r7xE5rvODudNiQSwDZnUBM26S2zp5zqAqT/"
    "Kbiv9gGs0HxiGWd71PPQ5c6D7gNpwbtJQBoshDOWWEr9HlXSNJ3XoOgLzHQgZUCpdpU2PJcHF8dDV9t19X6TVRdHroJgYE5vzCEbhsxgMQS5+4hf"
    "UIU/easxLoMPR4jixjGIwBhJfzfaO/FHp783h2iozmxcAmYnjm9YU9ZrUs0wvg7YhsO/KUrgiUMa00rYHR1lDIkVSpo7GKQDKVuk4EKBeZSzQNtl"
    "y3Ckr9VzaAAP+5laQ49KPd5DDOa5zEL5NLKSfDVtRbgsyVgcGP8hl/8DTsVt4JCQchsTgkirvBt00LA54F25nKgxKYUeOjBEuJ6U+xo2AjOIPsXP"
    "fUqe43zQ5S4aR8jBq70Eidc7vHYbVPXdzW8STgQ6Q8XXaKkHdmFx73dAupth7++YnUAb5Z3Azx4Gqtt0/hggod8Cp4zc3buZ9T5Qfu8FSDJGLzkx"
    "zJuUTOSsBh2BXLrw4Zs0XeNX4KC08a2uUwrttxBNwkW9UwIk/py/uLR8zn5Lg7smx8XzCRsLidYniQzk2M7yvEoGBAlX75Vm5fMmRn+jjCtQUz2f"
    "dwMBN9gGGgP9ZJGSfVgLOSi2RGXUiblLet0lGhPWjnmUPuHhUOAm+nh33/GnbmMExC4X0OhfF1PjWwQ4wVKNpogXOZklP+BmSRce4nh3gW8WUdBx"
    "bH+BDAt0gOOh4uR1KJw8UBhIfiSrdfTRyCpsJow+FispeEXVGSqHiknRzC0NW1LOsbAyNR870q0Ts4uvf3xAak7rASoS36+Oep5OIK98PB3MCjnn"
    "3GBe8Gh2SEWWwmFgVOxH++u/kMNCq7AGwHkOBphh98mhDwu54qCkXy6wrNRrc3y0EtTC17ZAHi0Rko6u8av/AAgX+wr7lUJ+kv2IrDZXBzaSSUq7"
    "JbnGm+BdkdBL6Ur5O0deT3K6r8bMdrTOh324zN5bWVYaPKOxKW8LqTSJ6i+rnQl/9TvLlqe77nY8u9FfA14GhY9Fdl6nwrxVrNC+VURxGw2eBUoI"
    "1ggC3Dbw5C/EmVhFi7c2xg2ih+smlohh5EHKLfy3SISxM2cbS6zPSx7J04DZOLAXCUKvuXrKbdRRNgrkGguSkwd1qXTkNDVyqeh8mmBxQNwFY4uy"
    "1zhXDmixo+UG3iDHqGuBOXyhMlUi0gjxTrP6XIvRQSJWMhoxSFXSoqsRO/ijFEhiT6QMQvrwxu7lhqgdbqxgMd5HUYYDa3Si7HzMYXiUDbA7Sr6a"
    "RphB87BDF7GbCH4nBfbQy+iznDLgHtGbbnxutOFZnA+Q6+RjuYOeSJyKzDqH94GBhQfW2QFTeR8nk0f8iPli0bXsmo5UwX3IRYsuJ1HIBob88Gns"
    "Twn2I+2T8BZ3toeQnnZRSb/jUtTgg+JhxcYK/ClePuUMSC0JU6TFAyl1ijAfPnx4EBnCi2O8hSPA06kGOvXwsCdm2QeRY7jzvlRvDQAIYmbCO1BO"
    "nHMZqBk4EPWLwE+RreFDB0AF6dPtwH7vSFIBb8/RfCNOq6oLwr6wRL6eiZISdRD4EWJMQNoNPysDcrJnEGLvBFZ1gVLNQG5opOfACCTUSIjyGjTX"
    "w5H4NxiJpHzyMWC/TvyGVRGentnoiOCB5UDvFLE/TJ0rMXadIHWTwmQVhSlkaG5aXxfu6vuSa0AqCThmOMl9VWOP9zGNvAGkSWUbFJOQ2g/UxLs/"
    "ykKpKbxJpiJsYHwT1P1uUwLaWtguDVfkusY0AD2Jfa+qOtV8o5BPMBCASk1Nr5yajkA2QYey7teCRG8wYbJrgGDvIzmVzcQ7PB1v0rzH25tdTx4n"
    "RQcPbxY+e52cTGvcyWuVrdpVJKxNvqMYXGEL3HRAJ+Mbhr5JBTPOZ8U1YGRLvAMZaTyCRUyR2+kAUzxACqaOhXPwwCgorh12ijhnM5W+GojkaNsw"
    "mFCLptvIp9SthseArmpbsfsIcJXdyxnclAZdilTmZuBUUKnf3L1SeFyV4WzRlKpniMWhHLHC+ZCcp8NTYUfGZuWBHZGUQUh2pLO12aCc2oV8OI+r"
    "kkyLHCHhM8PmjG6Rcl+eCVp5EU8lKXBIRQRHjNBK9L5FvLjzsKTwD8FZCVYPNfO4XEpNta1Awk82ErwVnfSPflhQkVQYQMrCvCC/g2oDZmlBQrXw"
    "F5j0mk57lVPZWZ0lTyBfNGoHcgWTgvFHHp6FKv9qDlD76VEYGXUaSCRBJ9YNiqHD3JnYLWVZxBaiaw6RAs+4LynKfL4JZEt8Ru9dWk45LJH6oGGx"
    "A4+2787uLXOkxKjgnjZv32TdiL8FMxml6zpFyS3CC/qDwGTipWk+b5g6cb44m0X0yt6wOahSVrWIR3ibshEt9EtkB9qibFgStGKTJbONDgQG+buZ"
    "GLUJuQZsGxTVHO4LNteDaa9lSAHOGN+sRoQZJqESgz3Jh5mouTw0DwnT7zYZZBhQtSAwypgwmOtzNbwAutiCwYTJlyJ6YJjMM4AOg9WeVBsLv8Tr"
    "sqYOV59ohzAxdTmh4GuRFMQHaDgu5UoiBGeGb5XQ2DpwoTAyp/aauSTpm4gkk1EtLYpMHPYq0vhq+qwmwmzjVzbzkRjqtkG+VWAEFIZMAGbgfoKt"
    "AjwTionnOfsvxixisoBm+FApXIyEwj+i4kSeCk7VXMbkLjy3jRidNs0+WfUaLqR6l3Fohknw4VFEIAqQ1DjPdwWBBtWrsiiVmG2UDyX4GclNUKKg"
    "lpikf2CI1OYmvN1Q6UDlGvOT4qdFcJPBarYmrPo+RkKIX6PxIqA15r5nlbF12lIRD/YZF9dQb3gJrkaFHTc8MG0s6DN47SgnQ3vFaYmkhbBxE8rv"
    "U80WqGyIBY4YuSHvo7YhKzhLfSn2M74Cj1ocm6jBlMBsSscZ698qC1nKyobSNGXHr5aqFrwuaIButOPQKnBfKfGoEO1sbmud+LAVY7GTAesWvj+X"
    "qy9iN3y0tc+ze9yKYIeCQ5XyiRBU+eh+SkeWU4PJybkcqPuma1+bqyMvtNph1XZJfKeo7fUB9V1c0C+sKz9UTOpnmi2h5hTop8h2iCTuIv0bnRle"
    "4gAui4KrjX1SI7f4pt+51s+Owy0nKTmSrsFe1bXKTKVG4DoxX8lbuNKeyJaDiV9NEmsKYBckj0xxK5WKMMs7TykAqeSszCCjWj3MNIHx72EsKJvP"
    "lxPHLj0xbaZEAkQC/XF+JqIau1RIwyRtVbhJBD9PCQANGzATvaA5GXs8kMvzSkz4gBxSuMAagOMWDzQjnnEGucfmFnDDAEyEZcLg2Jd21Qy7yL4H"
    "aOp1wSTwZ+tknTdePwFBzWXsGwrOgiVbeStxijLKz78Lr83nLIOWRDmi9Uke2pGUGjtpEiPMnlP/KDJJFMHX744k4PE6jY8hTYPlnQND9rciaoFj"
    "X2dmqfmxpUYtucRijgqZ0WR5TskFj988rcUoDmt4f85L2S92a7oNI5VhhSCDw5gysfs/qnAx+ZpzOoSJuCrbNORTTvdgVxUolNrfKIaQOMvyHq4k"
    "e8HA9r4hAWDtVGRADZILF6j5jli5uJAEfAjv0CYwpeTma89M8cSu55IRKPNBRPK6dKeiN25wbkR8g/ohmbYNklz7jlREbZByXNjmtq6bKP3zEZpy"
    "axxMd0JDVFiWn9hJ6AJZ6DxPahoE9vQiVopmmvSWmuogeWUGD1O+y3APTK3huX/5rAR7ZNPCVR7WysKDp9nfjlcGL3Ga3BO/XpfTU5j8nZLFIw5i"
    "NQS0VTX3EDGfS5fX56MuU8gDJpnMfN+zbS3bQSHmd6fsP97K+9oah22oPqyKBKvJHeVSicyZ5Y8IlSetFL6Husp1z3LN0hKEpbBrNC+SirHLoJRc"
    "38HLrhGim1LtViJ8SVrrnzWWSxezTMi4maJzBdU/f0PMberLSXLVIvOUQF+F0lTvvs703tW9LJkiidd5BCyTd3Y/NdxqWzwBN03yVtoQzMZSlD2W"
    "3OGqhAQjtkBzb7Xi8t/CyCSaifNUS2bcXBWt7CqnVNHoji8vNKcupJreCFlSttIOFFa4kbRcQDo4X6q44B3N8IAo5uOc6/bDmk9ph2Skn1KCnfwm"
    "6BDIEI2JUNVS2jrnF+ieLVc1i7Tri81aTMu29XwPkqRVZBruyGDsZMSWdidOdiNp84O5d+SYKwk6eu8m7sTtRD/GQ5XdMRopgFW90TJgVfiZwJWe"
    "XKwCqroAhuzj62F/oV/DkgOrgsIqfPl/vnWRM5HrQarukwm8RWMVoP5twDIew9YuxVEy4FQXSCMpDIRSBpRqhwEjVp9c3DvP4z1BW3Uez3UjB0mF"
    "WUvc3QdE0AXcjRSQKsxxCzcLBRXy9GUSWRfCh8K0aHdK+FTmPdQ4N59c3L31eBEfzmJUoQP8Fje3COuIOy8YVSifYMiNSnwqPrgnF5Er7C2GceZh"
    "pz0kVR84qk9g1uHNZUqnuQeD2LVaPCryrYS13SxgA+GxDR67DqEKE2jXCAQtg07F+WRIZNpNPUGkUqcRNTXPolHdIYaBqdfoV99ActOVpHBUQKE3"
    "wic395b2PgjfDxdgmfe7Co4KxkVaa4RCBcz4Ahwube1W+Na2n5A1eUq0t08YKr2whRCIOIaWdu/ydcFbWbV+rTeoQZ1SsCmgWyLT4ogESYAgF3Y3"
    "wsqZSIK10h+Aymh068iRE6rW5RS6gbWgU3H3sZsg8KJ9wE7JDbO7pWfICjfc9rvItmDGg2BQ8XrikelUieRtXfgmylyOliwVwK7hvhwIiurxBikI"
    "hliQgcnDBP+GXgw3r6eERJWdDvjtY6/nHXRuQOAtbNrjRcpy3hJKiROumW4TMCp3izCJbJV2YRWlwTwZW9Sx5aBwVOYD1ZRQHNERcEdgoU8uokxd"
    "xKcDLYTHBoWgorFIHIEXf3OEpTVWMpqXlf4wr1upD3yud/BQDoRNtXvlyUUYDoXh7nq4YMCM6PJGYDsWAx+mU+RGgPkZDh8GcJUhTKIB6lgGKmX4"
    "2eNF0RYcJaYricukkwU2gsK7zEsPCdAKPG7SdcspM3aiUZUe0R+LmKCbRhGK9bAL2CPpE9h41u7gR2jbLxVmUfDLapArc9z2Qh0A6MrIOb4YuPOi"
    "GN7evVVi3Egra8RHzxPprdIpoRcMnrTr3NsBFQkd3UbzkXX2BcAK2u91FEbnC45DYihtGQf5oLD6oFUQKpCwzGBolKEq2wADi0iVWhPid5GOUTuM"
    "1MjqWMJ+HBzWKpqlS3WAWAiltAo6AGzwkvuSjq20UobGArt2k6R+1niox8fiXZEOPovExe/BQVfhYZVfcShY9tYLABZRlUJggW1Nm+IgsDIsPYN+"
    "VVZWEvSrLfQOLEbsK7iain0F31jFKRv0KwwnreuddhBYG7AXjGrFgDOovID66QGwiB4sVXocrMi65fcJCpY+YVYWgbCs1hePV5Gw0BzfI0NKcLAS"
    "088DYakR4H10cH9hqPiORcFibT7+UkCw+EsRBqsCAkt1EcN1lMN6H//eDuaw3I3oV/hHRL1CItzA63PX7smzWWItA18hK6yCvIo2ksoG8LrgAaVI"
    "V+wXlDNTfKs8tlWgn0VqAFmwhS4WrUW3AvVsC65DBtkKziDSqse1QsfH+Sg7yaK6g32acghXxqq9yz6wjTK+VbRXwumtZ1Gt4iP1iFYUoQ48Bvk5"
    "+mzkgln8KuTy68x81dxU7CrKU9j22FWR3xv0qrhRFrtKTrJAake5nKJXrWbRq8yGRVQeRa5SAYrU4JCrvAA3+FVl7CrY40jOCltF/vJFy90zyFW4"
    "ZaDTYefS8xa5yrgXKlCrMCvy8XUrLvNoVU5MhT15RAoQLdoAVgkYVbwdOagqeTHBq0KsqvhmAlklv17l8hWC3y7DVjGp5DGrjIZAU8gDV61yJh+6"
    "B8G+PSBqlV611FZHVzKqj+Bd3R94FVUrA6stZ1xEzwaI2ci194laVXYuKmzNvsCr1LVCGE5g0PaHrEpEVpzEPpGr5EYeodEIq8oqomYH+dMFZkNv"
    "iGXFR/r4evStifo2MJAVanXwxUX8Bg6Iv2BFZ7+IVhpzjLyCPBrmEOAFvNjhFfY0LWGukHVAbXDX+o3hp4NypdEKMy8CKXM+jwJ06PA70qKj9wOT"
    "QshgiQOICROFloJcGT2+P9ZVotMVhK61qmZkeaOQCKqArhLeTb+sgbhiFDXwqsEb+0K5Ct/8r+F140hKXJ7W14LLFELeP6aV9edBFusyDG1Ph0yQ"
    "0peXBkCyKhKGQnTMT4tteYMtkUNCsPLRCq3JpNWCD0RDjbCiT8D6ZlCEwipiiUgoU9GGehGYWg8X0cquYp1ioXhEVl1NZwnOJqMzb+wthLUs9Jm7"
    "X/ggqFZEtXbXwv+rhyLjf8kT8UHwrFhFx6AUClMQhHANw9dvU2gLr5JkDWCq/Ko0BmfX5Cb6NDfdQqKWlqBZsW0dN1QWXIaxEsFsjBYWR1UwVqXB"
    "jYWUw68C5W0R/H3z4HSAhXrlly2aiGkVPr9RNEazQt/Ug0IM9oJSPh+noFZPwGu4A7v9ePHxBoUqLQiCcVplgrclYCs2FjQtm9wg+4a0cpcahFF0"
    "JqKYytHpJyipcmoEpe2mtihlQyxobDPxRR0QCqu0f7sX666Z+sbIFc+LRKooLY/y5WVxNVMeHByrNGu+bzcwAkXtJsj7TdvGLftR/YZcBmBdxgUK"
    "pHiDEhLukppzAAgs44J1Um/Xh84wCLmbBqzRMb2E+Dqpa+dpYFsRg4aUAIp9PAanQt69XT7p7Pl+c5CucG3pF5XdGPr4WgGvVIQasKvyWfdBu/JW"
    "ntXrogJyaAhX9vpQEIf5a3nUCnKCv2ChGsrMeO8oEwvCdcYVHunosHGw2CbgQJZl3ZCfhPpPxmR6/I98CyjsScHFQCTu59be36TIsRgOJjo9AORV"
    "1LSebLqnYwiQ3aJScrD6NFGuYpsREtKZKF82OvmJCaBtckgqfgpYdamrodHjbOCyKdYVh3HJ+jM6V2VwUhWBiuhjM9ArjiThfWSYqyTGqX7ag2Ne"
    "VYk2WDqz7rvAl1epRrwk7w4F5OomRiQW4FKcJ3c1Hd0n6sPgr4EJ6hLVmmBb1ah1pZ39diFcGd8vkd89yjUD9WCTMvNMahJGlZetR4oyJ0mCbRUS"
    "qyLWHO0SqzYLaWAxyE2bFIzh7nm22TiaKxs9rLeo4hNYco032zABk1lLl2iLXwPFIdEbk/gyXfjzcX6QUi25IMDqNhBTGefkmG9Y4SLNlG+hphPo"
    "Pf7LQbBqTj6gyFdTD/DEkltVnJyGQraQlLjlKPlslB6UZFQtRAsGo1+sZ5F7JE8Ka0SYHNb0UXejJCxieG9L3WvsAFwCXp6VMGRAwUaxbW40fbHK"
    "w39oIkQb+0e5yvLBTMLdfsCtmpsw1ThW0dKW6fVBr4rrKZnmeQa/f5yqzKesIqWhm3h+6Fus3JVUKgyMT2XO0gfjYxCx7ELXsawDcj/AVIxElXo8"
    "cNF9tmoT7jV4GzNq9KCgVJisfJOyz7E08cnFEVu5usnwcRQtEy+fjpDPO8vjURmGLfEWE3asgKS6C5oNXur8OwMCUpUiB/cw6WBTtTYj4SQSUVLC"
    "B4KmshQsamkkZAgQaI6dUr5yx6jegseiJk3y60KqMpTZ6GYgObsMa4oDbJNSA0KBJM4aaieLxRH+7HdTUcAu3gOAU1GUQNRSbAKxQSWlpDXpDRup"
    "N1oOE5XKzwlS5fd26qbV0PPRGJGKLq4o31zVtQoqBqsHfcCp0hAXuYmspBoQm8oUM+zAXQszW+OeCKRGroVJ3lWF2PBwNtaZTg4XhYpoFLPgDCSN"
    "yeeM2rSoLG4lkPpERR5GO3G8BvG3zrOCpuHH1Pr3aabfFJSqSEGgjF3A3GhQHZBvbSS+E5AV3kXkd08sEXJBLqIzkuI84GuOn9J4MZEt8opNVRsR"
    "d4ItcEzx2HBeHhmFc1bOa7rmEvcFX6rybuEs8vPHm4rdRhbxhi3GCJl74tuKe+XYOJFvBRNYowrT+7vbqKV4p1o+20Bv92p93C/Nr6Ewg7cM1FRF"
    "8qC+wOukOnBrXHsg8evO4U2gK9TSzwRxgOk8QD1iAZ0uQtYbWJSwKUkkd/nRkmtqd4ODFvNoGItuzTbvgUG1yhEva9YlDIy2PK8X4TXllM1S0dvB"
    "obYO7GaWG8sl3deIT2xy1khVpsa3CZPLeU8DV8l0LsggcuFBQ74MLFzl/C1KXE0EEBAGzl3HEkgu8pyKuibDyFJQKbI1S7ZW1g5OCzxcHC5xGPDk"
    "nmyKOzyrfhKNqCQYQPFJmXw5db8PFBdXHfAnuUbLfFTUq6cEv8VnmhsMaSRO5BHFnWHbaljvIQFxuVQda9Umg1RP/7BAt9wgli0bBWyB3Zs5Vr57"
    "sb84ODQIrtSE6kP2JIHzwlkZplVF9YJQS468jK4F42LbtvE3RV//D4DNVRmKrNs0dOvH3EPrdldH90iV9N6gTiJqRUJufrxqqOUibtI8V/lS+MhU"
    "QTl9NRfgJM4qXbFLcFtWcKW7xTZ1ctO/Xogt6VXAojLKE3eJzb7bPcCrplOwwrXgwEU6KsSb2TV711y7u6iR0m1INNKni6i1DzcY5juWw8DaE5c+"
    "TVxoMMSsNWILkEi2JVUR2naDfERoUVFVnOrZXIBJfKkWPyu+TQXUqOVjeSiAai1LrUA1cBZRQn7n1qQdMvGyavwsmYUJwPBimNJiEUwTCK3McCC9"
    "tjSn3QVBHoCVm/pOs3haiZW3RqoBRIju2FzGPKSWjg4MZ0sVhxRQy1yZxXLjkBKoFnT0x8gRVSnuhMtyvgJOS/LpYpG8mXMOUIvatphNlH+7zMJK"
    "aK1NwWmJUYrq9ilVSFu2yrrKLtoX7JZLsX9asFuxVwQOT4FI6ehRxttK+28g6Bb5kqmdBJDOpxhTjJpY+BnjCl2wTbijuy8B4mK/i2HrcUpPD4nL"
    "sgW+zCOFdY5R/8KYjkZkEn4rxR9sdudqronN7QOVC/kdJR1yzTVlfsrGNiA5C9Rl/Drwc45OrFOR3n6hupIx0zBHcYQ1JTNK/HAh7FnVKtMUYn+I"
    "XIcwH3Xq29nsF3qr5jvyqspwyeC/SGr3FnpG1ySadJiQWzQXoN8bBTYxgvuIHG9bmtV9YzG3Kr5aiDbCXkPw/c2DGzDpZEGlQbaNQrVHy9xnVzIB"
    "aYXXXauAVSRgihCCWmEyV9m7VR8SdGp7M9gt8358Ot/vpR/4Fl2JMixZLs9uYCSuaBgNjMSFqdcbAonjNdhBgLcyXXq+UZBbIEXhPqKPCnMy4RB3"
    "+DRz0zdJQJqv2WCCPKJPEHNBHCqO4maDqKtTxAA90pCVtgHzECsyt544o90tdkatcqpaFRrXOh7qBV+WhRYqu+5NL7WYriAFaxbQQfMd+HqTu4zs"
    "XrReCUFAytpweC57w1DBWrisd3l0uK8Omyv28LHoXDVdfCJoF3IcD9iVBKwcdhdOFTWpLQqOGV7BqXtAKze5X7eE2zmk8hh+sEUy715QpGk0Oobz"
    "fKNLca0Ey0v4pm/aVJ3GkMHz8jBeShZsQfAmmyziqOghpheZjwDsnHwZsw8RUpzlcxnPC/2i7qiPaGe3+HkTvtfmOo5BCzFUwHrRFkU69RnRw+IF"
    "stOxRjA3c5VcOZySAfoqV3uoi5eyMuFE6WTYWNToVNKHS+dbk6Ibj3NNypcSxK8n95/cRU8YFQKgYwof3Ipmq/6T0rT92oC1aCse6rIJwpU8aCo5"
    "DT1FiC93lDaDneuzYp2kafNFXfh3CHNHQh+Oxiy6l22IaUoUfS1dgvBV8U5acKoXk3ocuzxPx9tsm768csBx9tqmV3J1yWtF5GG6XmXcVQ4OTFeM"
    "GU62w+MF2Nx462A5EL2/od2pjLcdbH3sNI+K1k5SJWDxwYwrx/OD69zll0jToYIRGhepr8CmczBgKM9WUz4gvHCzBgDMnnpp782nKciAjVYYFK60"
    "s1lksOpbmEkOU5gwzSeUhCvCCyM+gm0+yXW8JJvMmGBpuadHDHO/RaywtH1ukqX+WANiomeitYWX8Aa1YMCT/MEIQ4U9uWgyBAwuGKgGtxj8ILKs"
    "NbrXa9i+f5NUPyY4Pjtz0dwQVuVmkgEIsXLLEG2J59RkhytWTYVFhWD0AsAFaM5TUeiivQAGWCy34bGVwIiNMTiu8Ji5blqutWvivliZEJXH6KeR"
    "Vj60O2jAbGDuD7H3sro9TOKRIMeMimj6eg5bRIDwc8Ydo/PbKieIYzN5XZCEqFO5FumqpLJ4kLJVdMiyjiUmi3R8bKhK0TGmM4DJsy9SxE9p69Yk"
    "Xx55BAudsNEKUqaZKMqXjN6qtK7qtWiAW069vSV1W7oaXxtiSSyHYxZLAkgc4uV3LixabWxmV5LiCZqZJKiUG/MYh1/VLFUgJtowMzrQMgCmYt3m"
    "ipS0TkE0E2Uuh2dWpUnlmHGUZJvRtfsg/O8aGQh6zqJiuCCzYwsJsJnPYPVGSKaenK54EQl5OG27KNVH2QZsLjiI34gQZ3DGohhVqiBRCDqyUvgz"
    "iY2KEoD3TH5GxyqdXzSHiqxJ6dpdyh80/QZM0NNQYzlbE2iYxA7JReSJUNuyYSNRSfsSTQZBDgn7vEzaojcSitjSXKpLMl2NpTglg5dW14hUqy9z"
    "1awVpbjUvFabexg2b5uRh2UqJ8Z7niYguSzlaPpowFTjbJwUV9VHtAGImnFYcGesbC29z8dwddOgey65XGv1eMR7XCpRy2fADWdzUddIJRTjPim9"
    "L0fQh3PtvOwEuUETNEaRRl2RiJMAX0XL8MqWMyw4TduJDQqp2Amo01N6f6l+wn2jaE+2RE1N4dNQ9seYCJz3Y75l3Ptea9ldBu2HrgDFdlQwfivM"
    "w10GMSusEhopSMzetDtKjGrPLHJQav+ObD6fak85fdnMGvIcm1RVvIIMoKbhZW3LmPbs4VRtvcs2rfoTCpDfBGAaRlqjmqOE2xrMP8l7drellA5P"
    "0T7Ko2aznSpCaAXUYIc0FzncLVde55LgPZiAVIwak5rI3cRmFTSN7F3028VDNmLGtLOKPkV2OSjry/VIQQmUYEVgz2w6DL5zEpIpg2+Q9SF3IpJq"
    "pp1qUV9VZYsJCsQTXiWgwKTuUjPAciKGbMO8+Bz2FcNJIz212jYckfHtf4SMec1EcjX8or1W09WoaVuekFjMwNikElRTSPygWm2xaKwl7uzkMqBo"
    "O7Qdnm1+SxorC8x6UdnwYqDyCmbkA83BQX1fJGptPYgxm8q9F1C7w+mWbLfCWSCxKXquNQPiqZX0APO5Rs0dyhgtWeWllOpf1jfobhJ7dGF0b3v1"
    "KTcx8g1WIanyUpeaNHZoyuRsZ4q7VOru88mi2lVf5WO7OaN81iaVKLJZSYYTRVAym8AMn6JihGwhCiIKVCYJlnIDy35HdV2R7lV1pfIMqRRp3XJC"
    "FTfLZmLHDY9V/lk8nDRXNu6DvJ3MI9eEi554gKqcem9KHSL1oEaoj5MtQ0FX9AZLNZQfICHWovFpegM+uSgVQ6mNEStcylWUoG9IMf3dpDxmM+nH"
    "SNPLNWV0XkfRbbi7EBWMpL+jqiwND+1QuQ3RtLdJfINE42peUxUgam2xfZ5v+JDZ/TQ/tbQ3aScALQkyKZclf3gaP4XoqROrwhrJ0YwUzQ3UckVu"
    "GdtBxFO2U45ty309YtPlWGgOToo2/VOcgnQjMy2mOQ+1oGbYhoboUrBJIeX+i/Ir61IxqhELyeWsCs9mXbDrerMGj42uLTaGzKCxbbD/gGQAWt7z"
    "FpAN6A0qAfvhsGHjg2toy+IL4G5eBg4CU10mxfY8d5DPQLGBmgzAznewvRxnGpbB2CLoWpjuk38wPW8AHhYRClIotm1krRc4yRow7TJAbOH388R/"
    "UBvaRCLa3NvOga/FxEnKho2PZqDXcGHLu9eYnTkfkEFfC2d8Laz/Aq4gj2eOrS6gPWaQdttFPDcn2clfjCeYRV8DN949bdT9BNGeN/G0rnHvUIe/"
    "xils5CYBxejJ/JN/qERfg3Ke2wXBBwYeN19xYTZpCeGowxFe3Nt5vMhdNQPdPEqh2GTYKsBPRcSUMrR5R4C4nykQm/k9slNsa18BwYYProSN3ybb"
    "9DoyoPk+QGxBQN8Blqa7DDDhy0jTid2k5IOZXNTAfx8gbEoNe8uPH0E52jyKti29fOU14+6jqReWtdgXgO2CSSiC0R8/Ko7A7aO0fVS5gE3Icvrj"
    "rxnOw7sEbnpwpQiJ34EL7lwogVQf71hCrENkI07xZB5cJjJlWDNGkvGPgfHZPtnbIb6DXEenCHyLGv7bW9kQlc0w4EX2OOQma6HZ7rKUMpdm/5hs"
    "cQJPyCuxtw2HgHdzW7uCr1M7ukVUtW/FOT5B2/Yp4bM1mhqqIEHEbhOEOWpB+NwFPSzCfjfTz826CUxbHAIVA3N/MChJ6sMhQLT572TIAvwF1yAx"
    "xvNv1AbCIzq0vDQoThuGfx5A0p/FZAsK6Hn6FDKZwLp3HCTa4Ehsa+Ec8QBX0XNHW6qdl2yyCFz4oMLF1+1knnxwQNQ1VKe2EWv6gpkA2Vp3wu8+"
    "pGle8/MT9p4sI0+LchaHBLYW5/MJ+rE2+nwWU4iW0d5f1/y68MqmENTjncfv4z2DK/PJ7nr4g97E3a3EVtOz0gtwAGS1yAzBhkHHGYFbg3qEGgOZ"
    "vHc4aGCUVl6GOhQT1kwqjF9TXxw1fB/ms0amfFDj8EOcowgbRX3XIBIAjbRQgFfAqN2AIiEykkQZ6A+ipqdMxnzQUmEe69IvbN1L9hyPwJUSlhqB"
    "BlXjqMVvgDRe5D0Nq8SR/qGIOGslBLXHpOfCFpFeB53c58lR2Bc/TW3idTK2mA2IrspWQxZHrfaNEp4a33BBVDM3kjHVwAgM017lW2qB1Wqlcxli"
    "ra/20Rdw7Q5qOAi4RrbOeTgLj7lGXmgkQsIZUsg1tGjnDeDa4w0K9iZwa5Z8iJ2VIdc8u8tBriUM0WxsHnotwVxzFyuBXgPDjscyuGupjp9irz2S"
    "urUEes0o9GjTGuQ1+JBBXkO+nzqfsywWBzIxAnKKQFg9gq7h0d8xsGvgE+c5GKS1lIId1ppVLrNoa2vSUwASN+BAqMEO6qtxvzzs2uPFx0Flf/w+"
    "Ab8Y4uyDv0YLAkEB3Amuv4deQw0CxSEdbLDpgYaXCWc+A8cGgYiHsKEZMDZgXFLrv8k0mINhu0vWL3oHGBTDGbcej+0xWXXecMmislkzkFgN9Wi8"
    "gJwwA88G5B/UwmWSuctq/TNqG9vGBqhNthMcFHRG9SBtRtwwRBvK9vUUoI3pIF5dBWd7FKbyAE8tD89mtMoyRJuVzjKyA2lTTcBAtJldtDBtin1B"
    "upzBakNtdpnp0YG0CTPeEZ0LhzQQbeo1ONFYGNdBtLFMVBQ0MiASkDbUmB02G/bz1BuV4LJdoDAsnmwKymZ/V8JiE5usNBkDyWbpI4fFFn9INfKY"
    "woB8eF9IbGVbfpvYj4KwifNtn2hsmC1KukSSvMGcW10e+4dhQ4AyI3HsM4nwaoDBZgUUPIMScbkJEhvOwwmxA8Cw4WSc1CuQE4ehd4gl+y+RuCgp"
    "u+DqKZyzmJWRgZHYwDV+nlD5Dgq+luECYXmAssZ2MNkyVsVBLDZyZmQcS2oePBUMNnHO0gFIl9Od1D2HJwY5JDAlaDANFjAbPYmw4tPiDgl+mAjF"
    "Zp0gYEajRdAAlS21csmVKK7yBt65MkBb5sT6wLPxVxk8cItBHgYDaOPbR/hshlXR0Dl3qDWg9o/SRo2UMe/DWWmZu2QdsU2x2TJ8xjwucRS+C4cH"
    "z/ZIEtcSlm9DGxhso5AGaT6ci7mRe88rG00I6/BQ2kqzSRSxctSGlmZnTPcLVTtIZAGWdh6Dk4yJShfZ6L8JU0KZ1RizLfk4EbbSsvfrSMnZItdS"
    "Wpo+CGhbDPbU7sQNlCJb6ptZpH3Y26Za2GWCS9jEdkDUqrWM1vZ4UcroA/tKUDPzgG2oDRjVF9Wja1pzXIJsc04nEhvZT+Xh27waDD44MsfvoM2z"
    "g3qpxW+TzDr2GKKqX4fhZiwa9QFwqnXY2wcJkJuKV0gZTFHcsrFePJociJtLIxbb4mAgbvaWr+69B6rIMt1wlNPxyNLwQqCkNU/brMPAEFnNBGXc"
    "AVHbaFAI9OKwzoS1rsagQc9X3DzgVzD7O/Qimhp282kZtl6Kmd1qdgGDY7g1XUNVV3VWB8XLJMAT12IIImhTO+xlPACem4tPsgrKJ6rhTJbUu5RK"
    "5mOFrJtkjIGngOg2kj1LSUjgjk0SuPBkO4/5zaRPs9X6DUFyo12HkodwoKVPJx+FyVuO9JTx3JywTDDdjH+wD6BbWfVTrQSXYojmcEDdNEaReL+y"
    "zXZTFhDd7iWiSc6KV7GFrrZKZ/PhA72R+y+R/xIxE1kaw1Sij+atNg1qG96PccYPo+uAlq3jJMFCEw0fAAPO68/uBVuqvo4Hwi351hFA9SkCwGUD"
    "eboNPirKe7Sq+1aP/OZJRzVD2jrk4o1B4DIEUDp0p0XUxidFt28EBUcPsWubXBt4fmFbylFkeY+kLes7+wKF01+jcXAdbuZ5wA/XZ2QDzOgUpzZ3"
    "ETd5n4Bw4NTTlsEX6A5tol2EepJDgUNB2AAFLmPpVyiKCpP8LUKC45pxVB0CnyHsrGViOWyCbHOfHty4HXWz4OUqfArYGmY88CFjgjMwbsxyhF4j"
    "1yQPzQaakdyBUO9RedBq1HsxJ32HK24KtBnEyiWdlw4YVd00BCF6RTARFimnF4ngQwmPO+uf0HfvUNUdX01V6oIAn/fXEEn0LwPKTc4/RhkiBexe"
    "zB4+UUWy4dUeU0ct64R5AAkDqPMziaCaZKiCqtrviD2HZZoX0KK76w09ObZMnDbjpSUEMfyrWh5CAXjK2JqTgT0M6DilVUiFMQf9YzhRRDMQGAuJ"
    "/WO5VbGw1OYD59kjXOBaQyS3Eh/zV2QTI5gVCG73MZbCDeejbV2H4Xb3CZbEi17CJ5YsLw4sTVTpK7BIcIhcf3Ixupz3ifDWaCKwneU4vTbPwxeA"
    "PSxSMYnVVne3OZI0KNRbH2nlvd46xAHA3YTFGicILtwpkBUHpcceD8mTpEQnB4V6g4oo3EdopwvpgfENunfa9iycSER4SxW1JNstj/VWyhLCqptl"
    "TqvIAL2VX5AcoYER3kxQXDmUP2GXSmpVa1aKmqO7ATODLJ26rLzS7S/6pfB8HVBuKdndZBDGprcDn7UobxTXKWV50AeWJXluUYoxvIQ4ILKb3Ctr"
    "k/0DdXe7QDmHXx+iW5O5DOr26IPnRgoBKJfso07ubCzGqMByK7mPK/IaBsJyw8TAjccb7EtIXCcYTEyIkGIcNyEvJTW/8V4eLqgb60uoJt3hdg9Y"
    "yLxdtueRJaEqE7YW5dVtzq5K6zwKX6yC0o2dyxmGwyruNwXJDXn0HUVn5q4YTMecOCC3ueQqli168gFqdt4PuWwMN8qhvqia4CbWb9wRuWg7FIJP"
    "ZhMdnF7xRDvmIQqMTWJUYq+4ODVNoa/bSqnfjYQn8y0EasvFtpH2KnhzJlxA+1uOkAopqOOkrjrGmp501Mbw1LJfsWFjhjQdgr7NBmhl0CI6nHKO"
    "IJreThjzPKmWd8TkvIP2LLnyhUvv3kYNGbRQrNe9x+49loZIEQfCZ8tmSOCNInaSCY3k+ROxymxs7ODobAP4i7USyeQZR8ZXunlNgurfJpC2VGpX"
    "obWlz6WwbQTDRrT6+P3HOyasRVIqnO7f721TE0O62hBu0qX4D2CfBvO8dsXD0j7stqalciLq+YrzchPX5aFCuGn6EX1ElZfI9iu4c0VlZeWU+mK0"
    "lRUnpXTV522ylNjHTwmyLSWSzKi7F3MlM/gedV8gOUtczqZicCryYaG4lZRcZuPJIA1W9HTg3GKm2iGJA9TbSAKRXWQCzQcGd6umZogx8lAulbCW"
    "7WYVgCZiug7gLV6IzOhNikz+8lHeMmGofAgyH3mkRt/5wo7KsORIRdYl+vovSnwIB9tBWUCEbe8vMAckjrwiptowX6g1Sc/NBj3JPoL9Ra0m6YK3"
    "yq3x2BZPhVY2UJjAxfGwWbmHFPzU0eOUR6gYls3QdgxwT+3eoA6Fty7CxmWEPUVQof3RBVu1L99BMqBmW0mFHWa4reslfprAcQfyroXl6Zg23VTD"
    "FBe0ExjNKHsdcI0NgOVWgUkuU7wtw+uxc9dd7uQEO7mhrtVaODl9D/v3mRxkLetOWV8Nslz28mIqGXBnKVGqBJUL7z/iRqzUYS1dXFM0uVhd8g/l"
    "XKtY5++qMOMnckhympvJzm40qB6WU+HzYHLcv3eewurU5S0WwOQw5QyMnOqW8Bn0N2Zg5TDWpfkbNBuMkSDz5tLLMsacWRawa1Ct1gxbroKZszJ+"
    "0zQcwSyfPLxcqRfMoi/1rUGUyxtwnHTg9fp9oMr5GoGnhCtHY5KZa1Pw0qFZptAolPdzAT1T5Jqj9hjAjOD7nGIvRTwx4pXgx8VuKMw/Vp8CbJze"
    "3cQZwCA8YfSRJMlIVPndi0QOvHaU03c4kZfyvgOBJJnqAyDH1VFP1i1kPJ469zx6XPxRdCFh7el+oePSoepjK1V9Kkq4bC4LYd84coNOTrNlGk9r"
    "v4BypfcURo5o6Ab3/CNbB60QUyXEJSJWxB0YTo5p+bWTBXXJ2r3xbUSP+wTaHZ7n9huVpUv17Dnxwq7RZUYzDe0HSHINsyPvJ0dRlrGdkiZ4oRsg"
    "xiYTqhO9vhlCXHwk32OmDyycGj0lYLgoMZuiwWXtpsHx4PJZjVRas8aBsn6ocPUtgVzvsW8OQlzlyimfKJ9uV1ocKT4EKtcELa7kWfce30DNWQA4"
    "3MEd0txTl/gqmxM4MY0wW3w5toXyUHEa4ib8LyTl8xypsHgaolMXBg3OZKkqvMY9RmOIXWFUg8fye4oFFtLigL9kUeHweYcHV0q0iDBwDgHOu9jK"
    "+G+iybCe6nsKYY5mLI32MXmM48GcMd0wAYJ7vExJaQUknqYdXziREBtqfpBBhcska7sGPkm2C45RDwsnhjRuLAG/bdriVNsgS1IZ6cR87yxdBIV8"
    "8csu0zgeNffuxLKWeSO7kQhMXkieBjjJUp1vVeBwgZbK84xp0orAkti2uSmi1ntDX7YgcYGsN9wVvWMjYC6PRXpaSGxHQzsKEFeVtBuuBuXxBeEX"
    "zjpQILoO5pn36C5EsLgf/ZB25zrQNzZgwG6GMKWblF2cLgr8J7eES9x4bGQuTCDQqmRlrxJOHNkAFOqNQHHWbxGP3DRh0s9dxKbqYftQD4ezSIlP"
    "aAo/ofBoznGW5Ngk8Wjpu+dB4yigai+zd/+VGyH4vFrD9iTSBK0euOGAUJrNPbM+JtvCiwPt6Ji5iPms2U5ekkhKoyQ+ZwMcV7ETjinQ5VnFVRBu"
    "zJOYzwwZRsua9brA7QkLYfApbpz12iC7dxnyvgkctbKoYFAJrNzuNcLIiQzD8ukc1Jzmx4bv18DKqZ82yVqw4XbwLYD3CPdAZ2PTfMK9S48hgzJX"
    "WahZy68d3hxj7LAIt4mPjDy3QZlhOg2GlEMvyzqB2JJSvMy+Igs8V6piRfA5m3bpOKcwd7IwAOkxZlSGbfvBiIGW8wdmZCMB0tVkZypk5wMESl2L"
    "IRmrott7FQkasOZyvezwxJjSFGCuH23isPBSkS+SIqUp0zOrwF6DN0SiJlBzDFtk9nXEhWkzWrqJo0rJW14XRfA4UvpWFVrNYxRoz1Ovl4ZVMq6c"
    "NK3gU/XBeiY+gZVj1QaMWdxfUEd/HEuUfD4nyUm+bhej5KiDkMv0q4WW6APpZSyf78SQZcXOVElwozAwuw67K6ByRoIZ5Tch/03ZUFV675QnKj0K"
    "drAVr4Wco+bk21hnct6XeWUQ5mLLPh/1lDYtbIFwSQOrQHj7E3UAPxBx5hgpQhHlJPXhk6DJSog06UJUPfWkqeMqwpOGMeYZbc5Sm4vSRomrBGTR"
    "50CJLKPPVXPivFpmk90cxez9fT3NkJyUupBs+HzRCQ0FpisZQuU2cJKCZm5nolWxmwSrmFZ3L0ftjQmMpPpybMKZ0WMiPUvHGQrTJKkkkQIFjI4L"
    "kLxKkbVW5BIxJi1FWgFw6yaevOlS/kRQNaR5wkWX4s/kvcZwsOoLjLmmqLguFgIKrL5dkmWljhqYB0deJq5aiW7a9GVsMUJtHGKAh9tlxOtTBqSr"
    "6drKFn1tHXHWjeNERJJRS+upR6NjIB4RqeI1RzosZclVdWW9GPWhBqh0CiTlG3fkGgJoppE2RE+9IkShzoisaKLic7tj2mApVG9fcYLMR+XTAc3N"
    "8C3O/BRzfdMdNIDQNrJk6V8mbWKq01GUhsSqZedD4ht3vSW514EZjpWb2FHSCeykEz/F2UopmTGF2CWDshVj9NllAdazvT+ME0RWZGHtDIVftF8q"
    "9QaIaHaxhlJ627KJW/YO+CTmBOLumypL8sUJPk3RJzXdQEWqIpsryZfFCifPYqkIM5vfzvrNeZAZjO/B2Qm7N6VWga1Fd+0UjCochCaouxMhrk47"
    "kmSjpU3itGE8l/miyY+9lkh7th2RSamGR6QA1MjcGLXnja7CftDSUm2TJfzL1fJyFIgVSfJFeIwOucYXM1aHZUoMVUjUArUiwlQl+l1iC9a3Uqry"
    "R1aRYw18DnVMIds515jbrv0mqylc01bR9qqc6C0KDvuo0EXIOmss005LpsVrFi2JTKtEVYejky1OmEiL0KykT1H8pgLm4cLgdkB5Le+W/0VJA0vH"
    "TfrnJBoNNROyjYxrhTrvIEPs1RR9aFXOOrbWXsjpEKbLU0UhjrUUMcksl6Ymd1y63VP9gduESvZIhmtt54tdzdst7QXnvVU20cDNNeB6zDdVqXL1"
    "aJmGc9mkROaGDM8d7V8U8DteqU4CO5EfZmoiTQ64T/Y2GoFnn64AK3e6DLOn2Vz2C9LnYMdfJFOCZRp3k56jdywqb/FNZAL2c+F6UJtMamlgxALg"
    "oA2ehemEAr7/j0FQRxwdupaJX02upSmUZ32YS7bQBv37mFOlnhInHrKoejcSSC2sdMv1+TY7oeJJmw1gYFqdVY5zlGjEwEWwyS/Koy1U1ozInM5l"
    "1O/FEt1nGm2Kj1ud5H1hnbKNNU0Xp0xbuMryuVjxxLNGq9D+gg1CYqscSVIOy9130j6XpMlI57JSWrschecO2jrRZbGW9heueOzWULFBVPUFbf9z"
    "/v8+sCGxEUYsxLBz5mvDnifU0x9wo3fb5sI1JooD5NvY1jUlygCJxe7gRQTh4z4L8bpS7YCqcuLXFR0g17/S+J7LLU6Xc9LWETDbsb+BXEkDw/fl"
    "yvaXK59/ubL25dXffbly7curb2UB+fCxh/jMypcrO1+uXMK/P/hy5Tb8PfxXfmVR+r5c+dOXV5fCA/1g+r5c2cJRw7P3Chzzc/zE2zLyZfzJwpcr"
    "fwy//iD8tJCf3ZMXH2Yh/PCB8NjHuER4LLz5kQy7Fj6cRfSDCV19N3wO/7tQ4GyWwh/r+N5t/PGnX678d/l6BuMPNgx+S5+6h59do5WZgVZu4UNX"
    "MvB/uONv4d7cwMVf071ZxwnQyB/n4ABxUiv47DZ+4GHluxl8QKAEfuI+TfdPX65shOkbcMAvVxbxI2Fnb1XBA8Lqri7Lsj+lA6APFzUk5TSX8glW"
    "wAjigzTpK/jGSoFzpB9dUgJL4AT9a2sF0zNOCid5dTmPLSizJ2KAjz2kU5LhbuY5BI5OJ3sNF8TktSxE8Seib7pW8PsUfvDLlbdhfvDsuvwFzrpC"
    "Wsvt3vjy6gKeRXj2Vv6alb0h2ccKoAte+29x0X+gK1wFWYgP7OimKvFfgnOFnaA9v1KLYCiUsCJzgj2/8OXKKv7jjzLmNo3jzVq9S5XXYB8AhzUk"
    "PMSkEzYqcqxBdpJo4i3iVmHo+UAX/eAQkS7WZUpXdY/WcC5vAaUdwYXP41x28Dfwpfdk6g+TfekPmFgrGfj7dUzgIfHVW/hjOB1HKHz76gAV3fLw"
    "9n2OvApe/yP/bVBIReQb68r0b+PFMbP9CLfwMvH/PpysGeBizRg5SiiSVfMDYb3LprsJTvRdnqhwkv1jMtbPMRVohjfdluHwxUuF0MJtHS4h0qeC"
    "23gY0w+vvAtX+2ORJreUlpHGbxFTjvrCDXzwWn7J20hGi4MjPpZHs0w0pZR7fPFWtg4BBLLvp/vSKq16GVhRRjorL1iIs7ADDIoZidx0AQ8CuJGH"
    "jkRZS6pnYIHzcLKf0uoOgh8pH/tYeP0S6RUlEvMbF5Z9EW8sa3rA+46akdPZHghcEgXnRzih/58Ybv8JWqkNeu1RvhBwmCg6VljNgN+uK/fPb0b/"
    "GxTP/JCwKf1sWSlfQeqQiz7YvEZo2eHJDdLXtsjc4dcs6/5H4cJvRSmyiN9dUk1h4curK5WYlrkNXnOXe/8Al/Wc8SHObwnJZYmEzHvK2dAAQM2B"
    "iaEgY0y1YVXLdvArl+KWXEI+sIDjvuVkq4is7Pb0hcdUY0Up8Bp+fYP06cibb+Iprij/X6B5VmJl4oktoEnERlyl8tkfQtMS4wU8RrI4L9Gx0o9g"
    "8MJYFB/VyH3aHYLUxPcXaG3VwJqlD5fVRfnxe/Hc14Sd3i7BbZZtcjrWBXQEvNUPcRMv2QJpgSu0E8yBcJH3ZGw2FE5lh2jwYgTgLHNBAeFM2M9P"
    "2VQkW3q+BMMp8g5Xiiqh20TWQ8t4nIapEpGu5fff67MepBMIGV59QL9hoE66TwLVqTS/Rcfp8TotuVm0TuX0tG+C2Ynz+JwtSTxWA91ZZeVUrMNi"
    "eopp8kBtMo/oidNMH4lInsiIPxcJuWbAPB0HoE1SP49z4qiS/LoxnnPeKOR4Pk4QzX8Y5L5H+IxmDZ4J43uWXUgM81mWtWmkrK+g8iFMHOeeOBQ+"
    "igigIutvqf0uUKD4hc9lJuviVNnQG/CsuXXpFTvpnEB15lEOMpQPmnf+nnEvMofKey4MfuiXKx+qGKkwCg2YKNrgb8lQD8hhGUFF6fIQN1sETgsE"
    "8JYHFuX5MteJoyR4olEqrvwz0agHFUXy+Z1w0Ns0Yevs2ZHFrOTBRsXpKJNAfaEsjLdLsKPIopfJyhUNPyobKzkA0sRWz7+VgSGNAh3O5/d0woXI"
    "rPspCKnd/hvGOXHZwJHiCc6Tpe4hSaNkRw9fRCZV1c2Bk6Jku6YumEgrglCquiJ+72PimGWs0rxtU4YsdepV8kmFLsWteahaXgQvtSdgwEv1LA2f"
    "IuxSZA9viZzeMP56SbBRnz1uHOnrC8RqFcg08XxW4pkOoDDlYU4NUdmLdaVIzlvxTvFabYu+ec/BnsqZXXKb7OFPRa1d1TuWYKDiEtbkPm3gBnyk"
    "D1eAohJzcJOulogGLlVIdEe48Ep/4NScnXBpP+ipTRx7H5PXDk/HKvq3ijwf2h/KquwBe7FLmYiJGI2e14OBrmZ1A/twWeHoC8Ca145wjcQELjeF"
    "Yk3UjQNisVr95Ajy5IXvFhRwKUQa8z/8ZzVGQcYJ03m9L1M00EFBWnEifyC5Qf+Oiu9+wVqr2J3atLnzghFUo77FDINv3C2xZAHwtca9XTZsDx/a"
    "FdkKqRLbcprqylyvjkkQRdARw3yH2CyPtn1G1scdUdvz88o4k8GBzbhKL0XnP21NP1jYGu/TB+LEkOhPo4BDGSO2ilD6AMXyBGhHPyCVd2CYWGVo"
    "Q33uFi+WZrpW4Yxl/+uBAGStqZ639xpxgnJ8axCUWaYceaZqJi7aH93LhwY9KypBf3HJfqmjhY2dx414KJaYiFL8af9h8170as7zlglrHxZkbZN5"
    "VqjxfmMuIFf/XAQuTfqPZA5FXnFP+M+8WEyrmbWu6cM7NB5tMkecK+3IxqC3VVtfCvxWuoadAzRehOjVOyAkbjlH4SD7+1DMBz3cHdWSaEReXCZb"
    "50Mca128ZJdIYUpgdct7csFYzJzikIDrlrU/seDsJmYxduvZU/JptrEyeLuVNlwhisRtWfZD+cZt41v5OAHj1TQhTdwhV/HlWlDeKsvfO/6KJDsg"
    "8elY1F6rbsXlW4y25llhKbVnoH1FAdhWzhft8/0D/JY9H+RQeehCNw+tnlvpdYJrTdf0RuWdZpazpGM2YYvGDrwKT6k6eACY4L6i112ze7QxzfhU"
    "3IfPdZnrhs7X5aspCaypordGUUxiwX+oXPPgyMKDLbsc9P/cZnI5ormtGlXUca/RsLqgZWY4eJCBUeKi9o8/XKXRNMw6yicWDfVJyGF+XW1SPwXo"
    "4qFK2vtURQluxrphnpySc0nlepjs1cOmy28OEnJppX3AkFOKZQFw9GlCImcJNr5QFW3pg5DcyOapUp6Fag8HOzlPpqURKaMuw0co4tyIrpmAV5Bl"
    "bWmqXlX49ylgKau1n9dy0xCVydyxwe3U/Kowo8tJQuAZOVpUqTXpsJx7UOkHcNm0zZGY8yzYv1dO3bnqPC0r5IF9esjMTbJWUlFXkXDEe/62eFu3"
    "+URNTiFqKmntWZ4PS0ScPIQoDZviOPchvhylpfrjIKk80SQeAOk5G61zAWrK3yjlUJA8eptdmYoEXR5vv5DQWQ2mUtu5Z7YYOTT8HbJCLIa03XPJ"
    "Q8MT3SdodFVWekzEMRmS6HKqrL1ogiedHExxINvlW4Q0LWoea7wcGBwiJ8zb1tPtBOmqJn6o3b9AVMSSbZvGi+7sZ4COLOeVJC9Lcwua4ESf+SfZ"
    "X6q4SJzizpAi79E9TQ+6UcTYGA7Ctjea2NadG002jQQvpY74S/puemn+JM4jZhHvHo1e8ArPYvjb39MCHXu6xCNpCCMn8vBG/WVgXDekvKEGNMek"
    "mRxZ/9iUp1V002IEWIky6lkP2UaKFAw5toVoe542h4QyjVuFaTHncYnU4DL5XFKSktq2viaGjKGrG5J4taNi5SEt7oa8+YA5OVh9K4VN6+B5beiC"
    "b9Kr90V1/lxNvXdVXu8fUrsRg89khi9qrG9NfIbOZdUMd3tw474Shht1kHtiT28QTd2PIkK0yhpYbvzoDVz4So5C8juVflZEFVOmsrO3YlSnfib1"
    "kN2NPYi52eKZVWrf1Vs+KHp31V7FUPxQZSQIi08OBdI7EUepo1R3Y7+7WXX26annCiv2AQaOK/ijKTwD3nRrxOB+s4EVR8oo/FI6oTzVlSsQO8kD"
    "hNfk+bjM1AxUeP2rC1ItuEOpU43hw8tR7KqQd6bcrCKqntRAlY1G0aibI47jBzkp2Skb+/BsNsxg/jrgyAeyDap2O5rnfO91Hj7XgEv8KpJ8o2tB"
    "Cx4Wknp09sJU3lg2LA8AaZ6ID693QotF1RFG+lnqh4luPti0yuMOlXyYKVephzo32t9b+aDGjs3k5EyYyt5i7PS1RS7VuZADgZ9X0bMmurAi9ztV"
    "FOPlG5ISHFYWq+PWhwuIrtrzCqmSOJuNQupigc1WejtupwbYJfrV2xIkJun3B8uVOBS3IjVCkhWcc55kZHvOBUfc9JsCp64beg0n+VCFeCYPwJmV"
    "khloOVEaqDBpHWQ4v628y43NI1zC3Vozr+tpDRHjkDip3sh9RGJK14mEz22bIx/fc1N9RgTuhq3PI7meJ4CMK+6aUNmOCuaP0mQvopFvIbB7jSd9"
    "xe1rZT1Og1Bv4yB2SrNpksEAqZDRRE1dPjfV1LUZl1KjJBfg3XRM5wBqHA1cSl3gfTzSGnCE3dpSt1K00C+oFFCrPMYu6jJJs/NOdU9cONLyQSDp"
    "xWb7UJdQRT3MRgyXvp1PuCLB8VD9bk58PLSpn7nMj4PD1zcO2bmWD3nHflqpV5JNjcN69emn3ybQ+0xcumK6mSeTqeMM7VX6RGumOa2CRWimqRP1"
    "LZE8hogJnH51KPf6jzWMJS2XRPnfiB1SMjaSWHy8RfUl9E0gwlU/CRpHqw6tXqfkUrwzZFurIvcT2TG3Nvog8XTcAshk/cXhKOrRhk2S1005bhNg"
    "etjVFmpxJDqDUjddFtSYbcFvDzUWi9H3TP6NexmHrGP35QHQMstMu7991n/p/UyzeJrJkJkbmp8i31zSj7C3FTYaGECFwY03gwwqXYeernhtclel"
    "usQpiyXp0zd/YKj6lh2OUKrUExtpZHS5zQoT2Sq3tfIr+6xwP1WXzWKLfMJFdu1AvFIDNhyp4FXXSkBwITQG4e65mdZoe7j4W8mNCbYg+DL4ulkO"
    "AyG4KO3SlAj05CSX1envh5FdU7nrmn88aA4Eq88jDQt52EoUPq4recgVyyKemYTfE+F7WcrG6gOp1Phw1ei4ifHWLOdHXBDklELt1R8lxxiN86ys"
    "NVQkvmw4Xh6Hr1JASEs/zr9FHU3A67FRoKhrWqoZCNCifiG1Hy3aYx1w18D7c2hoUhpbb7pLCcD6ug1xZhrIxMndyvBOr1Wpr5No4qrNHs8pbDGD"
    "ayGpXk+Htn023804n2PUM1rwtJHNXPpHi7/rtSapiKz94rPHTto2Ybjdv4bQQme0ufe/rhtBI2f/0fjNeEgb0ncUJRlNtUmzh5/MCBFB1u1ZFbdz"
    "gSZNl491uXkfp/LTeqUctXjW80eq3TxJw2onNjE6J8/5crzbzrqLy7wt0uxatQQ4G8yHgn2XqZnajDWtS94A51DCqK/ZbZmD8efKTQTmqTuTW7lT"
    "MOIC42bMQVO/sBdjPbSuTQOg+jhVlO4XtS9j2rvP+dDil8VvFeh8rqI636mrFFF/qCIl70ieBJGbTt916M2v5TvQXFga0bY4spfpQ5vad0uRrmZa"
    "wBRbozH2vp6ocmpQb9hOaJD4RMVPk63T7cnsNpBif4NGcvYEp7kE5ZTatVY3fhFzwDVrJUBayOxqFXPcxLc3XdPBdy3XhAqre8Q08cZ2lV2S4egO"
    "xltgt9OfaFGC1LZWVAGHBwmeWzO0h3AEIO+gQ022fk4p2yeOv8Slq+w9BXyZsAv0XWiqiRJKavtpzNo6hvQrmgNE0j2j59K3bLNOZL0wtZoeq66z"
    "gFN6uX9s4Kots0WuO2qhzBSbjL7+3InXXj/17LFTx75LnQee+T+//wNVL4HJMAcbwaDnnItBBFt0CCO8sJ/jZ7mflrVMbuPUb9Z5dHcK/upIPkM6"
    "2qBDkRA/kErdkqSPUU/SwZKWyMkCyR9u6rDATQ45ZY3LQ3Mk7joLJauMtH78x/i53lwk9vCjshsa7Ap9ttT2EuYOIepwHOXGl/kBkzzntzKqS4NO"
    "lzRl8/lMauB3B507JMQefOJpHdCgUy4915mb60GLFPozWL/twBZ6GHrUNgd6iuY9eSGS5kfq+B8qtTXg8nTDHBe0xR03ETw7R8zrtZNFZ6p1pt2o"
    "NEde5Gvz2smC1TKs/mxWUcNZ+wlThjoA7XNw9o03JjvTND+yXiUsZZ1XR/lHXBb3t69QhrgnDs4UqfhqmP77csgq4deK/g0VBoofiRV3dekozDLr"
    "ydBkoVIyDVe/FkmyS22+yke2L1Jcc9JRlxoH/sZJSDtw2jxXnkd9oyxmo2Fe3mWnbxj3xQj2hjjyV79+ozM7B6GI3//Vr0HZ5ZbFdd1Jal413eKK"
    "X7RmGeutiTvgT5zuym7NNUp4P5ltwmx74e+7t3K2bf4p7uNMK4AOMHPoUs41gw66L8iD7wcB/J+PFz/40X/6YcHTPR6f+u5RKLIJEy5avXBDZzvd"
    "TpsD/bPtoNhMZ9752x803DOXg3yAjbikhIw9lBqtKnuXSkH9o9nlkU58UZaYi95ZBWRVqtJvY2DDG+z2wauSjhlzoK7FGqDfgPbZGoO+Vb8O1jsU"
    "c7s+beF5ctPYKvgtfd8iCSu7v0x6/TOy31vaccz5gDZE6aPeJcYbpAkT0WR8S5jLJe1g4Hqpw1ymWqOvnfzey53p3i/l3blxmWH4WzYHMmh5XPPO"
    "sND/afj73//fhbWOzp6b6Z49M9uaGT83FOfsFE9ryOS9Om+z31jUJpdbTm4z4tUfFhpXZ3+cfOJtGp+/f1lKltakYezlWkdu6qYJIulnIt6s9zOT"
    "jxiLMTILyyaM21QOaIYx21MD8uSpY6+f+tkLz73+3HD3l11ndfIZvnDqlZeLKv0+10DHlJEoBfVrz8/1LVwSbsvcUmLk0165mtO+nACspVFTCWO9"
    "+d8diSVSkHIJ3e9GJPhSvZp4iyRBoxzw8g6k8nKS6oc4JONbi19ni7IqB8+GyITYTHeS6qD8Ed2FwUrC3i3KHWkLaWq4pk6dJdn2062xn9E6f/RD"
    "TetS3I0dMSYfklOLDjxi01Tv31GN3Gyp1vU7zie2Fh4pJ1ui35HU4Pi04hRtpG3JYNYE6V32Ynra/RNuBIXUF4Zk7+mbxnuCtFN76eLdoSnM2WaZ"
    "GZ6Q9rQpKjuyjGDTfDJVNX26GGDc/mZsrqarLMxMSoPSozRjMZK1L5LCu8pWnA9fgy7keI+5p/270m/lubjjscDM46E02P6Sbq7saSfW+am2jQnW"
    "XM4tnkLa4CvaXvJS0sFjReo/PidjJaZJFlZ7AO7XCjrr5GQMz9Y7oqtiTGtNSpnoi2d73ZleN3YJ9ispaSO8YnSWktX4zGx7rjfZfeZ/Yxl2y2s0"
    "/9/3tP/nMzZSNPe9JKTsG/l/VJl/lyaBZWYdE0U+quxoGJjdz3pJC+/BWOxb+RTjirKXGWgDK62EFvRIY2JaUnuDfJ/46o1ER2v/stNNO7CK2/Zd"
    "8ZJPBZPkZ/rke6LGUN3ex8Zy/T9GckVCiaXJDX7hBH4ASRmzVIyWy9JRTz45t1eV+cSqtCaVQlGQVw7oZujG+JOqn5eYAX1/pI6TxuXB9mo35X1c"
    "rHcrmEdWlazvCrFmXcCRRbTGfg5MQtnbikDefC4Uu+IYMy2cYbWUpGN48A+pSyNv1g+lSU8fNMUkeSiZsjtR8yFeel+sw4eCirDhnOR1Jins7jPP"
    "jLcnZ0w7UNUCyxmAcq8g7+/kyZejZeGsj6Mm265W1Y+6YC7wD3pBtzU91po8O21sKXqVXliL3OvgFpTTdev2towKaJLF/tggqddp2m8rrbNv8XsV"
    "ipUzixMpouzamcExcSOzVps6GP7hRl8y2E9LQjlb6eQxNk/dfH/WmZbYjwUEySU8mZa+1iHCkCNFxilYoRXTDIIpONe16ZJ1J6e3chG3xKRI3cPf"
    "3BZfIJdtxxnSBnLsPnOKxJq2hDutpZqL8g+a3qqu0ZeKZrO9rC4Z78Yb4DUut0dkW+tngcN1Rtv7lMipqdU/67nZ5i/b8oEmV2SoYdpgalBMtNsz"
    "1qgpe4P6A1D8wZ4vNzB17nFnUq0haZSgklIXl8skz9hOl9J8+VSti1cPtRNr42SUuNq9u6ReoYcZco1Cph47Vek/Uwpta+i9zeN4xA0hzRXXf/CS"
    "TARLmZ6xRU0PbaFIWrGpZ5Drtyqd+3AyH2gj0Hwngv6fiOVWy1mAq6gEvsf8ihyDgtL0s1a3MtbijDdy8uYqrLT3cHUgoaR35APMuB1G6iMnLuX4"
    "Z8BtK3p1VVR9VEKBveXti9+Alj4ziVCsv87jDwuIQL1Xvq4bIk81UkLMYo+NFpsnGIuegWeR6bIY62qaZ6FHsyAtxyldw+qiwKyhlaZIXjJtfC4X"
    "pjOPl7kpOsN2VUfJwXBj2Wcbz8bpDswuuPsvdSyOQA3xrPq3xT6aKns3VcplI+EWMkY4p7E5120G3Ra1BGapWFuMaFCGK8mnT3FWDlI69pbZSac4"
    "YKva0uyPuvYQ2U6QSU1pg76ONZk7sv065Fv5PIdKh3Z566EfNeQuSbz0P6BuVFUb/54AwVdZrknf1UZlkK4YUI11EOML2tfrj6458pBjYzGJsm/R"
    "tCUMYZFq1pY45XuStmsAXmJhtJoc99M74GrdH1ZtR01lZexMEQl8W1wA70X7R5ucL2Uyd95zBfApEnre6e78hAsJQlOGsDNh5yV/EXMNWflWv53P"
    "+1/nHsaOlHjPqzRN5dtDcmxR6kfUDzK9XIWw5ff9tiQWXNwUWZkxDtasL0q+zOS34vHoykRXC9iXJiJnUDtjoxwbQ6jN1smXzDtj2lcSpR11atX2"
    "aznLtLbYo07RTlu7lfu1/d7lIzSCNjXo7utNFIrKfj9CR3pTlzPxnXumP9vH5VjPu/b96LC2+8qpIb/vO//MMWbnzG3XLbLkAAp+0mKhwjwbsJFH"
    "qTl/ZQUF8rfEDfmuLeFh4tdezBWQz3EDH1r0i36e074Nb4c0SzBTB/1u3xa6dDYc16ms+M3YVs06NvTBvWKCfE9x+5wrNirhEUbqD9VitElPXLeq"
    "0t5G9XkAEdyQwHJfjp7TJXGglm9Zdc8Zhwtbqb6nPM3lkVnBcksVkIcmR8dBx8eLr/dxOSdpjqbOKeOWWfLJaOYI+nXfjhNIQ4f5CfPNdDUlGmBw"
    "UqMJP+R+iGW9xQB3qH77CnRl6swlgLOusabTreyO9mVeLuS2omGoygI8P8ER6bztENCQNNY5t2LltzSFK0kX0CqbzKlca40Mr7y5ZH5W6jX0kLOr"
    "o8cpGiSV3Zpq0cMu2Wjy/WZwYvmuSL4PzAcaQ9hOHIv+uehb/J3u7YeSW5DLUaZ6PrPL1Sow85+4tnxZ94LN/Kng8nmYpiy3rTs/507+MF92Vn1O"
    "2qFHyjT7JBdUyuH+YU4+Psewpbi074a9m/WQ2fllO99XfeE9k7uVyRps0gv/OFWbUQOFme5cFqBX5YIKhI9cpCEPqesy15O+sfk4uZ9wxK/YyeTu"
    "fdDcYVRBd+zC/c3QdyAq+OvvQIp3WP6PW+OtuVbx4vTY2aD1dFphk35BPPrXDD0Fkd72NMR9u63pM61pwS+ew19MtWc7E3Mt/PHLUMVIPF5Q08ba"
    "EPWiR2fbE62p1jQijs71wgNjLWxJGv450eqaxoMREONvuP9Xa2KuA22622dnJtvS5h5Hxb+GUabPnOlNw+xP9E5PdkYJ6QHW15vodooZ+OEEFo5S"
    "sWCbEbVfboW/hGmca8F8gpA6054EDG0tqkyem+38onUOJ/u3nfYvsKyVm4XCZDqTnXFcU9jcmQ4M9CL0TYZqh/AniMKcz/wU7G1Bm6vgRE4RPcnr"
    "f7YNEGinHRjisdm5zozM/832ZGtuAg9DnoX3X2lPm98QqrSrJnid/j7XKeawgXn+qpzCk5qBri405XD2Uy38FvZPp12gf+B8c5L/eCCjbtzxcP7Q"
    "0JoIIPHDvt6a7rY6xSi9YQDRw0GNTp6do+0LxBmOnifWmuhNE4Z0Nyy+hzVODiH72AT8Iyw0TH6Mn8K5ep/NSSCEQKl46kLxQNQpqFQ79oWf9bN/"
    "pT1FqWETLficOeShYrozGRZGeKRwC2bTlWJnS8IoKY6cnRxDOHeYIBSpdDtjrYmiFcY70p6YCz8FN3D4xmS4XlCJ4vBaqUhQyQoKqkbPToSLaclN"
    "TqMbr3mHZyHNR4ojzzwjnTziJODKjHVagbD87y3EEG5IGwuqzgXSw+pUGMCSPX+f92GiTSWsx8ITbihTZjUCtd9qe6bjnW5P9qbCgPEERsKvpk63"
    "xmGq+haNnda3wFekzL7FqKhY7Hbk11TyjKVCc/RGoFy88LpxhezMaCsQIDC4zOv5D+tHI/pw640uI8Sa9gnN5qEzAEqR8eba3cAJxqHuuvhFa6Lb"
    "87OCGXDTi6Rya7bdmjuLxcszkenDF/EjLWgPfaY1aR50g6XFk68dP3nie8dffzlT9mmGlJ2coe8VRyLl6wBjnfByYIEw+/DqGHbHh7JegAjpzZyZ"
    "bY1hT6Q2/UTrCqfa0z0QGiPFm60gkYAs3BuTrcmefWPoO5JEZfv0Ko6QfFHHPxX4S2BJeCjBLm2BYOARjvpP6gd60xPT0MLLfgD68ByFBjxaqSjT"
    "0Gqt8LE329PQu8e+x1s3EUhi8mgRNy4evAyEd68L0W+5K9DQ/Gw4mrE27Cj2t7D9fuDvgN/VjjAXWiX51+E3k2dHJ7AhSuajcdAR/klgH1Ongwwf"
    "a812wsZM4Yb1pmZ6k8MgZiEN6sXjx7Br/n8+9uLLzz0bRqafvnTs5IvF88eeP/ayxRudw1rvArOli9PnoEUHlnJ25twsoWdoSfiGL+NFgtdUJ+hM"
    "gWQJPCnIltFOnF5YS2eYS1snw7XClkPY0A8+AnA4gOgRvjHZRvEUVhg4dNiLid6MEYCgNGAqbbjGrclEXLVEXM21T7fOdFA2hKM5W2rqrsAhfuPp"
    "l22cdJAOKnjDcaOwgfk/3wIS+pvWbAs0pFcZwQRurCRFgNyEJTyDCgCPgN8AKRqWLuoJKHvFZAflzLOBdbVmnYL3moBcd9uj49OBPYVTxwJPdIN2"
    "wu7CpW9PIDHPTcKYp/o+ibDSeHF05UD23dZ4jwhZfhz+8VNUh37awp93DbDwj1leMKfh35vGW6cScQfqLufaqRYNkfhwIXDtszh5+PZPprs9+Paz"
    "vVlVkcJfWekAXgnbG7QzUjRAwUHNdyqwadWJaA58aIRKqyne4ccT9E8a9CcuAVxW5h55hTSE8OuX2qgPkGLI9HqcKJQTC+ZwkNnAF2L7k6jHedfb"
    "ifacVdTmSOGSkexAp87hp/6mTSfoHOLHhVv4CE2cFqBnhx+80JvtvRFE/Vxr9nsT7VFUuMOxtf30nk3pxjKLhAPQ7jHUbYXOSoQf7kjvNB7Qy+03"
    "wk3BaoNnO+OdSaT2aVxTF9f8N72x3iTPungR2NeLzxYvteZ6cwjK25rqiJU1pdT32iyoYL8SgqF/ztHhBZtnrDeKzI2+GX48icJksg0Tek76raVG"
    "wmmwhagTljRwgpQdUiHPnp49O+m07PQJ1q1fCPuFsPXtX3ZnW6P8QPjrBHCZc+G0xvWQCOIc1obauSz6JPf/eaUX1GA8ZOKgYGgRr2SSCD/4v4UQ"
    "FH/62Q7v/HOc0/5SoIBJ/uox7l/HmSigynNOCmoJgidN14ZYO1Anajnhh8+DEhP3INIv7BmQwmu6Ta8AJ0A9fwzN5uM2eh/OvgP7Yc3jk9Iv6KTY"
    "WCeyPP9YhudbHA5sbIKzPRG5+lhnijfzBNRk0D692Ub9+WT37MwMM4PZoAghEUDB/Oxsb6YrmxEoLKhDZDwFBjKNMox+NdPrxnODVhLSM+JZ+qpV"
    "MfGuB1odx5dPBlk4h9PSghnRZGaJ7UmrNbSS9CEBvh6LTdm0jeC/PNCAc/hrPGgy9fX5jElT8erQd8wPJW269KM0zeoFgBQ+LfwsjBWGOvmTV04S"
    "yck/hr4DLQPQXWE+WQggOvySxoDfHremWZwdPCS9McNT0Dy/+DXM4zc8AtuN8Ms3gdnIb+lVRSgLvw5n1CVcQPjNDLBr+2N6gQHOoD8Gm49BxevM"
    "ykBgrRK7x4fD/SjIppiy5kcnTHka/spfmUL/D36hBcZQ+Gq4KoF/EE4JidLi1/A3mp48FWhvHP48TZ4qfsK1dNDGoNT4VFottah56Onf5C5kQXZw"
    "UNjOnGnpDsI7qIjCW9QVQdoMzrV+UcQmTtZGO90+dxZ9AJ05ZppBv7QdMbkVyLC4csJmgKeoGz8Lh5E30+gB6MgyMR7OgA3+cMOC4UbDfheUODUP"
    "wBvhHADk0KDhrEGMjoe59lwv3F8mOXF/md6jf0UNq7ql7fsr6lYFnbzhk0hoZ1Ggwo/GeFGQLDp9rsWEBcSLPo8EfxgbWUVlzD3qHSfGWSIriiob"
    "vxcHRzEFm3BWFE/10STfcs6DsONzuvOghxbl3UuupWlSyxZtdGLaG0q0xU8G0/VNegjUDr5q6lA8WgDomoIz05mOEaDUXNc6d6KcFw+kUVQ8BwyD"
    "hpPHgcc6eANAceDjb1lXYuIKYm4chbqdaPuXcI9lL3IzNVNsT/EkjU5AH302meqoU7vaYExXTDpW+BPSO6Fam8Y95sTpAVwqUFNq1GWPejYIn/Yv"
    "gI13qZE/ItYG6Uo4Ue5MyLsaFxy4Ymf6zVYPtaMWvI10gL6Tc9CYgpxGQTIHBjDDM1M3LORHTnXmRF681MZTpWsrsxfRNKoqEv5TVsLakuq8deN1"
    "vTKMulIRdLtpcCbPoGYD/5iYjYSiStRzv+x0sTcSjAtG50QwPVqzZK0wuB8itoskB3YYdqTVfWYO/1AFFXSTM7Od7jnuEwR/b6lOIG3EX5KTc7GJ"
    "5ywYg+iPwDbpx8zUhVoCx+6pwj/XAfXCN33iK9ZBQBlSo4H30t0CfwHY9DALNAeQh75JmnCcVQtYIGrn3rdxiq8wEBSD35Q6TiX4JdKtfji/frgP"
    "4GUYL5G1d2bIXNCBn5vKL4ADzraxSRh3WnQgyB4krXo2Y53TPby27PyYmT0baC3OK97u9NYNx56Jqc+dBMaQOrXxNr7hlDPHz5mPDInkIMHCb5NM"
    "GXfKnE/DzwDO2F/nDwi7rdvHRMR2gilevAlioNHh4GwaAoTh5WoJNMIx6sgC53M0tsdq1HMt+0VeQPrNHrg34H61J3pBtPiPD/bhIFJZhvwmYnz9"
    "GnVnVqFBmuojeqzyiJ5fol6wBM0Th57+BD5Wj4BCHZ/DKc0KEFErAkh4PICaUUQwn26hu9oIM0MdKXft1nVnl56WRieW2oBsC3bxvLC0STja9FgP"
    "1YdU5SNl5ag12OhHyrjzHfxzcI8i2/2T6LJ0tqR00Yu9yTCyC7aJ+t4pUqHgyH2g/dQxL0Pj5KOL+mgh4QY+lLMzYaE6Zph1LwPxFw7BwQDRXFEX"
    "jOfmYnfRJ67CiZmkHkoYl3DvZ6G2dK6ISOuwlQxiDzpVLxjmQEX4MFNOdPgRR9Hn94lwf8LwbODwEG6WMAbPe7IHMmv2zVYmpmAH2zeEPUSLUVUA"
    "g5JfDF8JzLI33omvN4GnnyjLKy+KnMP0W4Q/zx6qsBWBwYx1cLIk5M7M9maK0x2woqc4YWKC9NCzUzELYq411WKuHlT83mywvsHGHy5O6HPAL4Ku"
    "E5QauklBx5wIRx+YRNeJdiQTOwgEe8JleyN89qjwDst8wDSY6GjUYq49A8HNoH31hv9iUNrz5xPPZoiNA3SawH7QzoU9CDMMAmO2Q1wag2Z4ImRV"
    "hk3u2jMEJwJ7N/BMwgmhGybw88neBKpFFIiSWBC9OgXh1/CL8PZUD884jDrTEv+wcpf2KLT3D+MMHwiznDV/vcwSVYpXmlzqzTDITzRWLyuxx8ki"
    "MekpuFn1YOMnnnv95E+PvX7s1LFXCcf62MvFT1499ZOXih//5KVTLxannnv9xHOv/uSFF/eNFN74CzDMiddfO/ncySL84PmfvHLiJy+Hd3567NXn"
    "w0MvH3uhePbFU8+dOnbipWOv7gMMXJ6P33vhxVeff/5YcTxMDSYX33v22OsvHgTx+4Vjr/70WCGvHTuJ7lPcA33T7cCLzx57ye30oJjcL2PkZhwY"
    "Vmv6zV430L5JDoivT7bOqMcsvl+FtH2iFIHNw2q/BMrMmySH3LONEbRLvkKmYXYZgiQbz2hYzbGvTVi58p5ZiR/vEKlTHbCwO18TonW9qpC4fSfa"
    "z+gHnYsufFGeMWRhuegM5wy0pg+GOG1VP2iMYTXrkb7q56EhTPebRmPDsB5Imtzg/CapYuFwWL5V1sSWnfiplTQYSrTEdSEhJcjH6TNDsFDQzjDu"
    "RnI1Q0iHDv18ojMebtZEu9s5Q7pZ1N1Pt8Z/0fKu0LHOVNi+YDcHMoR/650mc0JzWU/3uiyfvymIzCfDnNQ5FThLD1d7jvwevOmtX4TpENkNFyc7"
    "QcEUxWSqDTFKSy6Q3hZEdy/cywmJgMdLzTOLrrD2ZFBhhhJ3C2iCoPJG2zvc8OFvJ0SxEDSzt25F0Eu8DQRswFc8Fy91FzT6LovjUdTQIZA1AM5x"
    "SJ96M/xXPVgaHJwKNwkOCJ4Mb2Feipq6QxATCwZkkBFgRmKaeAdp9yDoumX7Gi60vWxe501F6KHg4daM4I8jcf5A9itQZ4f0z28TRG3Oc1KaqX8o"
    "mTBME/OtUVAwbZ5ujbboDHHa6QA8e4xi8os/1g3oYgRmNhBftyXqHKkpvJRqQ+HwMGTzXi+ncWR8wXNtsLplL9ydBBExfeYZ+qMvKmx0PmWGisL3"
    "6YC9Rj0hNxzugUwErn7KdA4JppX0G065yCk4TWb7VPBYhf8S02zIIA8LNVVqc2oI0/Gqbl4TS1hWJYxpJMRupUoXEy3/0oFJq1zx7A0rbxEyM/Uf"
    "j5SzREQQE7VbEgcrbLaHalR01IL+w8sklmjuR9SzHLf1d3e6evFDYrIkF8tz7eGvBaATMtxak0a20EWygkU/MUNs0uWnHdVXnbCA72pQZxzU0TPD"
    "Twkn83i9jc/hVpz7TLBoJvUjJtqAH1GVGs1h9sLRfdfPNcG4PNGeOt0CggJR1AO1Cn7ZEeZUi1p5Eh6UKhX8NucLVONQhrfBQqMVZrS1aqzJkzIr"
    "OlTJlmyCJImvqnosRUQgpqZa3leTQ4eUI4Otnu11Y2pHBvTRpOlLlWQG4nEG9ny05coRUxjHQKVj5N2HX2TxGsmvi/+Kk8oBM3a17m+Gijgr4RfT"
    "OH9SVlmFtngM/xE2eSLoOxPh91lMxf8LgZ305ymmosmle0ooii5ujB8oDesy1GB4tsRwLBpW9yScMzoWObvUwx8+C6ETrj98CkCHMgTeOtk5vBMj"
    "sQqGNDCSHkMa4ueEibNYozoIJKH7plHF5dArMs8ygIMnyXCFn+FvDwAyaIaqqTYzQ9B0jJts3zCBB/o0SeiD4P0dLw0MumeQ2kCU8eUgW/D1uTTL"
    "+8CIfkBG+FZ4/VuA4/d3nv34XNq5dlBJW/r1MZJKVJQJu8YeL6b0o+FvY1pgpiGGMI2UEKLPvAGknqnGN/OUusw+UHqR4v6uxGeboueVNNWBAfNO"
    "oCcHudGoqQLqh4Zn6tcrqmHZkPimgNxpiRMmzU+16iaOcfZYE9B3Rr2wuhYVl57FxEl1cp0BxQGDtvl55YHipLpHAvnBKhguXoLANPhvJ8KAtlk9"
    "avthMW2ylTB9eqKNOdXgVy1OAIkZFLehGGKzQG7DDrbtlRhvcQhuvC0WwY0mIFcT7juIVVByhosYwJLQFFTdnaFXxjqBW/Twwwl0GldPlUrKh8vg"
    "Zz8GQ8IjoA0Xr8iFUIGOYExq5vEv7f46yLKXzyKP0e08gmY2pV5MYclVuysmG+jfgWHkUceEq8BIULxaHIOFo+IOWzsZvwOKckQJOxk9k8TIUl8F"
    "Mj+IrnXmgkUk8F6nO61ZDpHlavNjgk0C1vWKTOhHPwzkFUgPQn7jQf8IpDkXPjh5tAiWOVcwEM8BSkSueRo8Zhz1iEBamBcfN/AcR00k3PMGdVhA"
    "MrBHNGygsESNtwUU7KVLMK4yT5KqbfXH4eJkuDjTlHzYmUQf9Sw65RIRMFxQBnM430Cs7MKeCCK0B7vCJcgWHkpNRBqHE3RopvxV/iZVXEMx9mRL"
    "i5kNVtOzwS7utqC0MHEOwPnNUWXXsEVbeoGGFecl1q8F1paDVALBBk1SwkHosfA1rEFXGi7oE+wdo5hDF0qrZYFZEKQT/QjQQBmdagNFEFARZUGB"
    "4dbtzQxHkCKf3e5hiczvAIXIum06msoOp4lnMAzIQxOQfxJNzCmoi0rcJAJNlObHsFu75D2jMTwJCJ8dBtwgQ5yoIAwbjCBz1gkR0ZnjGH/DtTJg"
    "3sxY51U2k9vg+1gthaxp0BPKTq6u1GcOkbd6iAuWVEwGGQeerhlIXzoHvPUcppzPdSHSNEnidbh4GQutCFRnOPaufLN3xoXxGUHHJbdK+GOsM9ma"
    "wKeExQ2nWDin8IKTbBqi/ZowLMCKoRK7xGtIBnhcTph4IOwJw50EjAa9gqgTxCuUyl9J7TM/19fYzz+cR4tR3kuZZTgaKqtcfoeTHcPS/mGD9vI8"
    "f9AuuGJdwvfUDg7bgjmksZUM3buJ9lRvDKhj2KCrUAF5CVTlWdnxuVRUJcIndaLrxEQW4KyVnIc9dskJmOw4aSuYpqq8izi8loFA5Bp54AwXO43F"
    "OgT2vI6Ru0uO13sUSRoMW1gR4nxwxaZiOydYB+5mnHHBjReEq5DbF0OcYVun4CXKV4EKCHBxxnRdV1DHU55tkYrKXi9+lTRKzCjCvEJ0eGagNLga"
    "hVRdjeUcrXH785XXrBu6+kglru2UlC7qjUZSTUKMmChJFi07wVN3dhIhHm4CcuF6hkidsMaQpaXSGCxDyA0qDJ6ZPodJmd1Oa4bVtaHKCPuJYCWh"
    "op5mO1R54YdLBcon7Zd8+Cb2n9KK5NgWBKiEvQw17aGOmponNHH5O0hUM+BtmqB0U/RIT0ibibiSLteVD5cbf/HMtWjSJyWg/zawMPBEWgSEqEmP"
    "JukJvooUjwFzbM9CmT2lMcNqyW03XEIleJrMZdBEJ2ivgGTRJic/5jKQWzvqRFPYEg3mhyu0KTUmrgFZ1QWkHXLtH3ZE4kQan3Xk0kniAUrEozXT"
    "mxPlLWxDtyPly5pIY1urSSs9k8DDDXJ8HbLeLAn+Ax1hPJz2nrYRa3X1FKeTZBZhk+G3JXqdTOfBBBskGhq7MAX53bDvRMIcVhKoHW+V3HW5T+DO"
    "J0tlFPkrz4wyrn1NIPp+h4tXUfJSArhvtePuJq8UhpJvi8KtL+DHj+IX8JS4Kxh8Wp6FYEIblNLxHmcz8pPDaVuWU5b79mO7FZQUuQymmIN8j+lr"
    "kSpP8EWuTSjBTUUlUAqEWRNkBSu2mhL50TwBZdj3X3QJGDFjrVKK+SQqNLNS8dNBF3rUKO1NlGsQc1/KRSk1m6wfMfmB4jVGzQqUiLjj9Bnz0jQO"
    "xJfXdPdhtkyUiaGwGWo8Q4NTE0LwIbdme3jjXODZRp3jFuJLz9CrhoPReVXSpm9iJQcuIbPhZq0n4/wT5S1jw2ApSrC4MCdchLlGewvIgKZ+pomg"
    "sXZ8ZedLS1GlPgRU8GqbEYwRyznH+Z2FZkiOxfZDR5UnWpI5DaVvc+SU4bOR3mRWUYlsL52zji/lPxLuLo5nOryRwSZ3hq68/2ystcNkUOPp5IA2"
    "Pzecb0gKJWlUh4JbEqwHKulvo0lL7UCplY5wvbGyOiH5n64JQmT80DH35x3TMfdU56tHn4PN1fnqs6Vutl/uq2f+7fZXn/1T0BK++B+2Xe5L4ZXf"
    "TkE9fb9uuc8H2/6LT+DRrz7bHA2MJnxzpvj5F/8MuUXh793i9FefvZvtmfvq+FePbnbh00Gn+Oqz65gYCaNkG+i+8NVnvy/m/u1yMfrF5WJ6/ItP"
    "pjM9dL96tAnecR5t9Iu7cJHHOX7uG+r++IvLZ2Gss8Wf34dNuDIalM0v1qeKmWC8nsm11o1vTIYljY4Xc199djPfYPflsIwWzuN34arMfnFjerz4"
    "JTbWlT67x7+4PFpMffXZ1dGqbrvHw9sbuDunv3p0JRDLF+uylsjwj/NSZUNyjXdPheOfKSb/7XYPT2kjLnjqi7tFNwyeduGNP8604H31TC8cBUQI"
    "AyudCGd45Wye6GFuV2cKmPx4cTrsbVDn4cin00a8J8NuFWNfPfp0uvhl76tHV7sVbPHHuA9nAsXpCrrjveIM7HJZNz8+Hub5xw7vXnirqi/vKaLT"
    "cKj/LYyHNNOFCOgX/xzuxfhZeL22U++pMIcuLCxIHDiG8Obl6ZI2eRwKEMLiesVpoaP9teuNdxMJDEkkvPPFPwep+efwC7h7o5m113bqnaB1j35x"
    "pzhCL9FJFKP/er0Y/7fL0/3b9QYy38br9tVnHwYOEP7bSSg3HNsXV5jV1HXs5cnoIY+C5BoN05kZuHev7lAcbRIpcQLPnGYZCOj98JWvPlttwYzx"
    "8Jq18o3Dj47/2+1W/MiEHhJk9wFbOZRWvsrZwp9vm+8Cj8W7EH7++6DafHEzXLk/vw/8/+n29C1PKJnK5BePRmOzKLC88A4Aow9iB+soBu7rGzfX"
    "rnkc6RXOr3MIzX1pX7NfOmIui47QnT2LxH/WMNpBO/3++f0Wb+U/Fb8MsiVs3v8YgX8/unwO2NNSOFQ3BOxnuFN35JkDdAE+TqOwMAEuHZsAl2dw"
    "CJ2AJ8/CSSWSv+Ct/SVIx0C/n707PX60MPtdph4ZG3mL3j8cYKozPX5IHYJfqpsCTPS/BcYCImAk+Y0wnfDSuSBUP/sUn/59GAuIiZnOtKhhXRUl"
    "1S2F/58v5o9DYekLxakXvnq0cqoIYvGfX9x/Y+GoZ/wv8t6tOYoryx/9Khn/F9wRQjM9MTEP8CQkAWqEwEi4L/F/SUkpKUdVmaKySm30BLYxYHPz"
    "3RjcBhtssM2l224MCJuIrj7zcL5F96hK4qm/wlm3vffamVml0gW33SfCYUpVmfu67mvt39aScQoXkNCFaWGJqFlawm58E1ppSTrT6r+kee14T0jD"
    "c2nzWoJGBrAss84CEhloL9ESbDt1hBtWfYIRdblOr3/RG+iw2ktR77Peph1DHy5rXq/jdJR5iIZHBYnWYREfsO8Dv79FZmMHWGKy98BgfCvIazfX"
    "HYmw4yX4xMB18ADVxns2dVeY4sG5mM1xMLH/tvwIt4nsbdJ2HQCLO7zjIRcfKLKoQS/mnyx8MciUAn7xYCc9WUQyPtDRDPAxjcdm4TngISBjB2wM"
    "Ru9XBtj4r5egEx/YeMLtt0Y3HgUumE4VuvE47liFBkATUyDHf70EZGppIgd1TD/SElmT10c7zq2D/6hDPZ7QRpVCPj5suEVhH5Od70Ef71HmnwqP"
    "TMRsid/LISBP+BavICGbZgUIeTSV6Xoht6G8UPTjkHa4/oYLPPJEjcQfy8TPFhQ4MnqXU3PNxx46siPSHECylWSd0JFJplknQhgR/JjjRMjvxT5I"
    "8p6/LV9E7lQIyRMgIRv08Mk8TjIIx5swQVisKR8t2fnYeuo53GRY5PdYF04VgJP/esk4O7CIKfL+J3E5evIECUR0XpS3N+k5xQVU5d+Ind8gHQZG"
    "/J/QeziOur4MYlkezzlHJVDLQLl3QGKJG8Grzg2/miCFpHnk5T1GkuaJwYAwwwP36mTVftHwsZj3O23i8Jh9FneozMSa/qYbfOZRdJq6YjOz2qvn"
    "PGoF1kyt4y8arHlC2aYeZnOO4wx282D5ZhggZ3bowVoErfc/98E5Q4dVnvHAnf96iUnOozyL7iyOfEd454mOOrYc5PnFRvO6CXY4pUbafNLfOov8"
    "/NdLFB4l4TANEpvo06FA02La730g6D3oZ8zG4GpDu6l4bTlEaHofFAN2zmZNAvI8LgOI1sSlnRYfJTpHaGVI0YNsXKA0sEboFuGi/aiWfdF405sE"
    "iyb2IqO+kJDdg3GEusj9LQBGM5/Ajwc4KLABpGgnphH01ondXhGj61bHbRE2Wks6t+RkHjuTVfXGEgKt101ASMMvx9EGX/zb40cJf2Ftm80CSg+y"
    "oZaXBGWBGlxufJfn8LyQpccoSGbImZaULV89CoRkzocO3M+ord6Cf8g4soEbF7VCP2RjsNMd3EeKpnkrNWXieKXw0yXrTEZ/Vwxq7IO+wnAwmiXX"
    "pzaFQ83U6XrGcGCfCxLqyODWQKjzHbkuQPwD+bqNMs7GRiCo3dvsGYIUeQ8jpLSO8mL+mcTmErYNotqL4efDe83vd6MuuRwHBEHJO+fTUJaiAkQS"
    "IrqpF6Pw+mke+baBV3uDL7esrDDbLc6+MoyJ3sHwxjAi8YJx/VPf6ukZy3rSahS9BMxcGE5Q/nxuXbTpshV0a0WubKWj6js/JUwRgSkhLoxNAMAG"
    "lk0bhbTYTXnM6zlJONHy0cSKiNfGeCsYoaWw1y44M68bL0e83uPJx7wB6QI5OQjsgzSUFIy1rgjYZEyebNCOnOagF4hgqz58H0MDY08QGdXJdCLF"
    "VsDHJhJgDsijYisrPpikFNIsNBRvCR271E0ilbFISSggBd7m4xwPW36VI3fzsLIloToWfKS2MV6UNL/ZDsxssyagBkuYpApf2qFIvNYF6mgC24SW"
    "bcfh8yX7oix8jynDX2LFFBjMaHVLmNoP+m4NQHsqlyYF8u9z+S/SgLksFHE8CjX0Hmj33wwmtcX7PFC1mU84drxISULgffEmeeU2trs/HbhtdqxY"
    "pfAs891PgfxkD7KCDqShkR8RgVuRhnnIbPY6ENy+9eSyrE75/xhA3DnzI2da5KiqSCnbDcktuZu8XkQJanI1yOEhs1mJTezMtd2wpp8dVwa3+6mo"
    "VXpH7c6F+kh8/9JlRM2rda5koNmQ8PY9/+3H9MY0m4Xz9v16FTyVRfEs7OZjeEZesX2gW/rd1BZQvrvmtZS+Lc1v0o73Cv1NkfTF5p+gFZAC3y0I"
    "BnhZBJxDnFvGAV9XB6EQMhrsuBHDFWRxsRA7KKxtQQiH0VxfCLjZ4xjemKLQU52sKszzLL/akDAN1z31AhVOyjpRRV1laVGbZvgZYYUTP5datTVM"
    "WsLO/M99mgGJ6QTWoWpN+Tnj9lAAqUFlWxhVvEnMJ+7bZVJhp2mH3+KwBApYcjrZqWUDVoeD+oP9+hWSf1wIgfyEX7/qlv6vb6WcSPqY+MgUaSR/"
    "fZXGaHX/NDJWBemvUdJlwDUCttVJFJa7tdD0pHCnFGcCa4LG7p3j/zpw5T2TSF8n+qCqxXwkT7xgbxM4m8+0gZqF41BMRWJ69kFrX/MSY1XY7QUi"
    "gCmyf1w03SS8VYZZRCBa/ZNhigGUd6qSKIe3PzOaoMpeAU5AtDGK5K/KFwDz2FtDP7dJ696EFuepG71hoeu8Qcc4AEkuWx5ajoie81A56TBJC9Id"
    "Fv23zTeOBoN/e/z50QDc80sjwcT+kb8tv3I0wMzxK/D//7n3t+VPB4PB5rtj+4Kx/X97/PVYMNo8gZGV+/DNIMiBW2P7Ng2a/tdLTZAUl5onDwfU"
    "UNBxQC/9bTnfKzb94tHmyWDiSPMcVYUcpcqQrw8H0q4ZvTzP498EpnphmIXFevzDGI7u07Fg3/4R1czEkUPwOJgAl7YCtI4TOBMcwN4OQpMDwUTz"
    "PE74UPPEGKzM44djlGvYT7vU03Ly/sJOHixu5UZR2fcgpV6xJdAgrVJVvEUWpm2C7fb1MdknyspSOsCy50pRrGXj3uoZoL2k0FYC67MkwBLOZ65j"
    "PfeO166sUM9D9KRBURDk6nN0sR6NCSTIp8d/JBR3kVZOPFYxl5+TjOgIiw+iUh3OG6Ed8+LcCOvuuzKu5o9XCtfM1W1tDdrdxttPM6Z6R19sVw8u"
    "yLYhvW9oVCXNlgYluqO+27yuqnhjK6LjSchirl1V/2lnfIPI7/7uw0Q/IA7/rM/Vr7DK5+y8T3Hbjv9+kEwXcgyRB2+DjeJ5bjXZEPzKei7KBsYM"
    "7pRT7wUJIkaqCRnQQwkYGj8lbHheAxOSxUXg2vbCZtN8X6Xdo1TCaVNf4Ci4P7DlQQmYK1V5kRsnNldHHbCxObZtQKzrhA2vVoYxfK8+07qCxxps"
    "uOJRAX+k7MmzBdslSClR7Z8j1LzPQUoGr5cUh6V5TMU1c83rsRY7OmtnZFA+RN8fDLKlzh5h6fGDBI3k8kiv/WzOJqFHWRMTA91HFPw8q1xAps84"
    "Nkgj7GrMQ5dznFjeKlB9x/gQOh/VonToU16MTgs7M+J5Q9d7W5qjbfSi6MSHFB3rCtOfE4y90Gvz0XGT8+043rJHc4OfxA3961sUmchFvjxRfn6K"
    "t53mVN6uTNAWTeTbMzMWKyJ3AkEm3TUjvG2I9z1FjP/NtOsY03AvBQ7NBJwS6EOu0EexJCrjmRTd0fBVNMf2Zjqap0OeZW0+J3B8Y02Vtcaqoqr0"
    "I8kcz4xyEnKbgPLz5qHoq25GYg9zeS7I+aWS3ZPqBVleKsS3C0x/cGM070nSEuXZTZp2RNhXxF2WKPI8PK/Ff3Ww/VEJ6+WLZkrSbCULJwK1kNTZ"
    "1amKzgUhKfhJ1niGVekdOckESOWEAg2I7AI/hQKGY7Dfz/E5ZiUTd1I5Db4C8TLoQF2dF9O6oWZBtUX746L3j83iDon+nOTkGdl8xMBlR8Jsh+wJ"
    "5Zwgu26mUEupZ3tW6iwnK+6EhfNFlGd4XjD/LlL0sjtHYGmqW4Bod0nCkfsrZN1EYtJSbQz0f5BPpTEFixlBLAVEsTDHlrgI1K4XABzmZ/PHbHFA"
    "flFS5wsBppp/osj/J7IeeTbseifAIJcbuwHzSubK6nu5IkBmorxKPJxssruxFy8suyTAbTgGOFUtXMklAepkm0aHKLkoQKxJH1ehcFPAHHgSdauy"
    "ZplBMN5PwY6k9O4AbTvNNT9L1IjLbhAw51QIucArz+FTVOW3CfDyeaHLDqASnS4WGPTN4tLTlZu5a8CrqH5Otw24EpnyqwY8RAJsu65O3XObxJow"
    "yqrJ0XqHE3IXDqgEqYVSeI43D+jyclMd+0nMh37RnGR9Kal3qyv7fHLAJag2r7Nq+2KT9xEIPXJZ4iSGid15hO4Eo+8kmPCiGvgTv7zVCwoGCyfm"
    "Cx3pk/OqLdV/x3P0m7q4YDuHRDbLNl1joFtfmEMBOde8BjLGNSHlB1yhSPpi+64zQFpkUJY5jkmyFKUh/AyvN+h0cgN0MltTjePkz+C0xbZd7xz7"
    "buDVz8idgREJB+fNKkVVqNRNrqmH2w8UgIt7Ogdfsc4dCIpoN38JQofivA1fhTAoCD8ohhcxwD9dchh4vYsRJhBNaIrLBoICqshP6kqEoTIAiMff"
    "1bkGHOPLJTAtHBkxFWa9DY8EIJlrtFVT/3OdzTOUYp/xUm/gdoR9sLafxeA+3ja1TET1dEkCQnHdpJzM4wWNxSxe1XzzdkruGuvsRXbK0bGbIM/G"
    "uyVB+KXzHQmDpBi96xHkaJW+HUG6pjE6pp62irc/sFljcodoB/BARZ2m+XKDs+CTUjmzfFtC0rPNr0tuTihgZE2VnM/HEZRcpYBFBGC85i9TUGzu"
    "zBS6T0G4FxN2n8Vc369UlL813v0KfBIcS5UYLcttyQuu4ow2iz1ss1GfHi+/ZkF1S4lVRO8I9vPCJzrv7ndJHoi7dGHIj6krS4jzVOz3ShGWuXKB"
    "U2NeqSL5Rp6C5k1Q+cXc/QtjPEa8fQGPYCCMmJQLVOhAFsFx7VbVeNPklkokmhA1UCvw35jEQ9q9WfWvZBjkYAQH4dyKSyIO2u7LbSgWlMmJMKRH"
    "f/P1TQ32rLigo8kRRkNqudsa9pQ9oyv9rB3eH6jAXhamYl4r/u+szDAh5wSbilGQ9So1i4Lyoi9zEGak2bjqRDdkiQHhaKaoHI4zYJSXlCI6il5w"
    "yMnAyKg7Hmix0HgGEtUVY24pmFoUsox35cMB1Z+fASUuKbv6YQppcU7vObMGG4TdLn+g9fdmaIK8LsxGiV6LJ1O8C2IwT/wet6iLIEh4m5sgmK9Q"
    "ODO8qFz24J3x8u+BcD/hNRBaEuXPbSFXoplKuIp0IYT1wM2ZMJmcqg2U4J4f1zO3ROTpUBfQGN1TUk+hmrdFEHRKi71nZk26PeJYKaVoY0vfJ3FA"
    "N6Yhipz4DwqoNGmnGC0KduI8T3moCya0hkCyR0jYXWXBXHuio4+BHq2BwZ61NjaYULGKdYpqT9nwmObACmGUFKyz/uA3UbV48QQFrLjIyN05wUFd"
    "t5IOfUtVKdgtEKFfuIRijKw8JbrMfRR07KEiZ8E7KH5bzotCQ6I57C/Nunn3UzUi2mROGJt7KZTJbwqpkM2LZg9rC/W9VxFsG+hwQYUoJyrnkgar"
    "BEfhTvSzIJm2+E76oopxXaVehimhMu6dV2GP0gEoN25VS2EVWWow2lMiYCJkyVqRQ2uh77cgi6lwvcUo7d10mUWQq0jheJGxDuyQrTJVqqfk1Enu"
    "uot93olNl14gbugPRvFlsqEr+lw0eYSCMOQlLbzCBkdAeTXq3Xqh9QuxvwFXVXq4HD1G7C4F85UTq7m0C8W+KB/Ic6qBnJqVOueOuXJ76nFOQr7F"
    "V4nhpXK7wy0ZLNIK+HWF4u3dHU9+lZRJ9XnVOV4cFAetkWM56MxwIBhRfAy2jBVYwmS5egev3salsqRcobyapafLNdzRbAOqgpUuC2iiyBbbU6sw"
    "Da8qp/T0qa2zooqB86JV+jrXF/1GmQaqYEyeF7TGda7eOEhB2bqcSZdousry5gdpUF5UOZMlRpZmHSBfd4snNv+35W/0wXeT4VWHyXk09P3U/3Ob"
    "KmIff8/8WaU2MjT0ZZhGGOTAfw/mai68ii0SycksSaa4BN9P39VBfWtMDX3I2IK/mq0jgl2kLFGteUd9z2sjQfDixR0/ptgsL1/losZuDGvBu1Av"
    "+BWgyrqFudKSTXF4muAB1YoUCiDLU54cXHiJpbHstD4YhUMQzJipjuV9JW2aVaJE3su4vMakp8gBtPjUFlgXLwRxAOAJZ3id1fqNdSuNvStoi2A+"
    "X09I8eNuWkmheVrtESeKFbCIT1lq2eiIOHxttMwG+GtSIZ/LgTjDX7BiF7FXW65liKYUyw/lHRrY9YJKKj10VoJ4aY/iz+dPL1TpF2v2dDggZ/JG"
    "4kcFDmVTneNSdmYeLKZUjqGS+7//pyNM5//9P6LdVBeOnorSJJgm5qDaQwltEAniBuArhetL9mxN4XXmDX1q0FUk91aG/Y0X0LJDKPXu5GSArsAw"
    "Z+OKrkreZvXQdPsYIsZ1nJtrafdd7kdhKef7UF4VdCejJQfVUywyY87labpEn/FVJom6+oNxpbn0wiRFSKzSg9Hd9ja3jzmqI4lVKmvNVHIj+CZ3"
    "p4pYCo7m7QA5+07NvklBvIU5FaoST7DOinW9YqJOZUT5TfK68NWPlSl5Ris9Z8n8paSUwyQpvZmlA0d5a1AEFu2YpCJ9yE99sUvBS1hP83GhlMcc"
    "JhPXP4duryN5nQZbaz6u860JOgpVQPHKjyaH6mXdp1rzz7iay/eccKsbQG4SjHJAFT5f3F1UbvlJanq3EEyeyHZLpo1qN1wWV7nZ50eSr8vntc00"
    "3i/4ZF2xvr3wCzOQcgFcHL+AdlEEdtAofFJJpefZ4VoZmmIe1ss7Dsy2dA4mlMZdYX4uOWHnNBcJX2Mwa3Ged2H59pmlOXX7zOrdEyvfv7Py8E77"
    "/dOld8+s3vmhden82olT+uKZ9mcn2p/cfHb90Xr3zrTu/qH9wYPW9++1zjxYeXhh7e4PrRunS6+ZWfvi5Nq9k+0PbraeflB6s8zqu7faZ75b+/Nr"
    "7fcvF++UaZ36uvXkBLbw4YWSa2Ra915v3T/ZfuNm6603yi6NaV14vXXxT/b3krtiYL6rV99sXb717MTZ9pu31R0xsAyrV+52uh+m/fBU6/x7vIqe"
    "knNQo2W3wbQvXlx7en/1o9dadz5sX89f/bJ271uZZ/Hil/bHN9uPL7UuvrJ24tVyemyff2/twnftdx+0z9/NX/LSvnCrde9JB7Ha+u5Pq09ut05f"
    "hHGt3b0P21p06fj7Z+/80Okel7VvP4d9bL/x1bOrf+p6YUvrzOuth6+2nlx8dvr0syuvF+x83q3W+furX13b3B0tz748BxTDe/O/J0623jnTeniu"
    "deJJ6+1zehpdr2RZeXgetqh19dY/npxpf/DF6tkzsH6t04//8eTsunexAEdw50wkrXOPnp06v86tK+2rX7YvXlr54Qr0537h3ta9ZwU6bL9yC3av"
    "fe0RzHzl0ecww9UrD9ee/gG+tETa260qMBK9gP948tHave/a3y233ri2PdeotM98uXb6G/npH0/OiSiicUPna59+1br0xrN3T8BKmNfcOmzLvSm6"
    "x5XHF8woVc/n2pc/gl9AyD374Nv2mW8KY+nlphRujIVq68Yf1769CYu55btRkFK4SWp+9Y0H7RMnYXwsUVDk/+l6++pZ2wSPdyM3obR+ONW68drq"
    "pddx759eWrt+Tr+BO/bag9alC+qnTV57whzWvvfu6tlHrYcnWcz/48kVbnmbrjqB9Vr95Ca3vfrH5dYf3oQeLJHbzu1Wb9OdJe0Prq2++fXqV28q"
    "GvpIPn98c+30lyCoQfyB5kG+he/f/uR/T7zS8d4RHi1T0eZvG2HCb91/feXpx7D4pIc+WHvjFRQgd26wQOYRgWZ99vbN1eW3Wnc/4nGte6sIbCUo"
    "UXh+7dyrrSvftl4/1bp7rn3mUsdrRJ69eguUAeis1sX3e7o7BKUDCfC1L15p3fukfVWWjK8DgZV99tG7nS8BwbfpvdYZ1MDt9+7D5Av3fbAt0zrz"
    "wdr1W+td8tG68Enrizfbb5xoX723uvw6LGSHmz1yj7jrPJg4zQ0erUuf2+s72h/eK1zfYam2eF2H1R/+7Rxr9+6s3TrhLuZgKwIo0dzOAZLYv5uj"
    "fe7k6vIdJlR9OQfO9co1dTnH2t3rsIT+rRxgSVgDQl/IgRbG9btrd28UbuLABTC/uIs3WGWyIWou3WCqUjdugGm7svzAu3LDdq5c5/aDM+2T9/y7"
    "NthYcbds2Kbkmg2WE/nQkBYRKiS39vnrq1fet8OTazVaN75o3b/Yev2yulCj/c2tZ6ff8K7TWLv3OZDFytPrPEZ9oYbV22W3aeB+X/m2/e4jbbOp"
    "6zNWr55cfe+mujyjfe30s08/9O7NaF8/A7NeffJ+6+J3/q0ZomAu3yrelbG6/Noq1YX712SsvvvH8lsxUMaev2vNXf/6i7WTb7Ru3Obxs31VdusF"
    "75b9veS6i9Uvllce32i/9eHa5yfzN1vILK++2f74qbrPAtwK4F3/Jgsrr+QSC8sF7v4KoGRed3VxxbN3L6/du1d6c0Xr+7dh3g5531xUAc2wCNYX"
    "VVjp7q6osIRqLqfgFVPXUbS+fBs8vfzdE7yBq6880ldOMPN3vHEiJ47Lr5ngZWM5qu+SwHX56JXWyaveFRLwLXzVvvNp4QIJck3vFC+NwHbev4M+"
    "39M/tC/cLLssgofg7Db/kgjs0m5j2RUR9ktRqd/dbJ36bjM3QzB/uheY0jd5HwRYbO33zhQyhCyYrAezpQshVh5+yc2p361vst6VEO2PrzOb4q+t"
    "G98CsfR6GQS8yjJ4a3dBwPCNIHjUOvWAm2Spu/b0CtiLK49ftyJzo1c/IMm89y1+Yo252eseLN/xwoJ2lVXDp0BUP7drHTjOsvL4sfJnMLBx5j4u"
    "y9dfB7ITPBzn4Fz9muUqGkRXT4BVv/LwhHrsjHQBTgSbWuvd5ADsx3y18vBdsCrZjbdUVryywS4Yf9Hplgb4b2X5ZuviG2tPPwRWYYLc1DUNdoCW"
    "qf73hLi6rbfPcWRgC5czuObJNuR11E54r3cxcMgMxGTr1B/RnSvs34llsMDs+7wc23P3AtpkNFwYN1v0ZMs/Ar+Jg2L8J24v2HW8dKTnWLwwN4Jj"
    "BYy6nbcq2M5Yoz/7+FPQ6DzE9pu3YXA4IDWO1T/9AKYl0562knq+NsHtpWpVR5OsC8fe0hbvSGhfewT6A4N8ZCy1wL4Gv/Xp6fbyDeirdeYaOA/t"
    "V0+1Xv9z8fIDHgAGrQyr5S4+kMEr66X0xgNeYN1OyU0H1nghP/HR2r2P7drqmw2enTgBgmVl+bPVaye73m3AihMomG1wfXsBy+X2iS/ytxbY+LVd"
    "+vzdBa0b74OSsibc5i8s0L466x5ZpeWbYFEBK67du6kpBNindfGt1Xc/WVleXvn+PV5wlp5bvJZAeI1m3Dr/DYwKukOZ//Tj1fcuowj3CbK8041f"
    "QwAT1F2Dawq+/uryRSBO8NwwVGi65sgNfL96602QXbAIYInBrzySzd8zIHLUD+mCsIbPEmS9+EbRVnoOVwnAdgMBoFg+d6p16asuW9A+d3r18aN/"
    "yk0BsDv5VnhjYNwr3z9dffdWOVYfcHzr0pn8sECy2u7/8eSjbb4dQOs0ecgaqutfEGAVN6skvfnbcy2A3c5iK8DnoHHcxtN+55TfdmP/t+/cYO3A"
    "EQoS1ESHZC1YYwpjqPe+Y+Ul0tVk4HpH8RfL1X+QQ7ae87X9OP3ciYXqR3owoRcXI773nSVlaat95v0CMgnvh42a9YrMnxPpNqqulQoHgnqC3+eH"
    "ONBFXsAWwfVheEiVl84U5TD4syvfX23/+aR6A1bwDguAzSPmt5evrz34BnyEle8vrH1+sv3HV/AdNK2+vytuZQ8Y+TYQaE1ircJ/RpD4q1+gs8XR"
    "GFRCVx+DjIBv0Cq8fPfZiY9Wf7ixuvwaGO8rj78CnwpouHXqFjuw7LTiClDoDXQjKlj6vLJ8Crb07yeu2ofb791H9iUx9PcTH7fe+GTt1e8xBHLp"
    "HpBh++x5+HPt069Wlz8Bd4AyG19b1wEtERYPd26AwOCmWBX/a6DOwy7AFuj1x89q/cVpvHdTVv70l2uPv0JhTdEDFiCtS6AXT7QeX2yd+cBuCur5"
    "K9dg3dp/fvPZ6YvPrp4Aoud9ZLm48vAxr+3KQ3BK78N+YfxMHKN3MTx74e1nl2+wDch0gk4IbT1vwebx4LH1UnZcffK4deOPmGXsAfndujc5660j"
    "wnvr6SnsytjpXSDdRecUxrhpjHZuSprNTbrLPDaKsa6bRl+Jez39DQVQ7Cs6PgIMrn1wTrZuGFsd2d54OhwN/FLPmIMzehU3Co++8vBNDOzcwQy0"
    "qE37c9B6/Xz76+uSzrVNdYRFt8m3cih0/pmScZc3AnvO4ScbjZKkQNHc6B3YHI2lG6/ZfDmzYhe35UcCK98OIkOyv3RhdfmOFLSQeOJs7dZAyGG1"
    "tcFI57isDQTE083Y2k7Y8fXH0bP/0h1svHXqO7DrOFUvSe+PXnNFXOXnNZzRr/MsG4IWX/vhVOuN29b1QUv+j3+giKyjDptT3F4YcSC0lYdn2+9j"
    "rVDr7h+woOPKw9YpCVVjRcbZE6DS2MqFuWEU7e4fmBVZdf1UwMBxJo/Ptd94Q3buXRQVHJtiumndQGW7dv9k+xzYCGfRrJcn/4h7ePc6mAy22qF9"
    "4YvWmQe8Cu0Pf1i98ZiDO0bhX8C0A3l5aC+A1UAd8Yr8DKG5uQ4L5meJ2Ipd9GtJS+QCSjYszKvLtUdIPBQthJVoXfwSvaTv32lfuImViO8/QnIy"
    "TuvKozdbZ8+DcQYSGKMoy++3H157dvIdLBugtCMOhj3ZDx7g2j+9vPL4imzI2fMrTz4iS9fVpGwFS5urcCwvoOH44M+rV94vpkGQQPxg4tYhs7vE"
    "Fbiaj6s5bFzBxmN/BsDY7XfvAbu5YyqtRw/AW/Fc9Wcnzj67TmvOz+ZGr9/w/Xn74sryBR712r1loBwkXUqBtR6+DxrzGW6ibYAhR/lVymSdNFOS"
    "d+6fbJ2/j0mVM++zfWANSjNDW4K8fZjXkq8zqkTet1SH4VPwRr7++pfApbYnUv/n2vcuwodnr35vVRfmQd69uy6YNUcx2m/eLOo8m0HcbvRqG6Yx"
    "bbYuvgKuKHpYj1CeAjcjyfuSBvXhpXOuEA12ohNS9HbAWJeZG8bQMA1Y6+I5AlYXpSUskwjMi5+z//ns07dAZsJ6cXJX97td0NRoiv4y4Crd3gzS"
    "vNDy8+DdIKht5Zq2pf7V4aU7xnHNGoAk8gpHC0oJI2mkCYEKJIJBkb/WOfKeFDEDHVOIycVL1TRAFppJ0Ed/FmzkFxjAl6gmzHxTGemsnp872DOz"
    "Aoj81h3MMrUuvtV6+CrMGpxTTlJJke8HYGtcMH1ZhfGPJ1fo6MP7az+8hW9TM7AVa3evt07d5IgaT+R5gDeX+7tnrrSWsYbDVMdfYTPFvkgq4XPY"
    "Buqgfe106/TrUkBsItLrAzNjSvL9+7haP5wACWIlCxpY9z5eD46Zn8JieTaK3r7x7N0TXdGXUaoVCfjGayvL57HWYPmd9sefdEVg5pIvmCRuExmO"
    "+aF2hV22EQtcI5j4p3gswrZQBrTcPneWq+WYCnT5QAnUMh+HskVxeXxlPoXEZFeCrMyFDO13zgP3lqIotz+4xoOB7QYLvAN4sqzq5Vt8DqgjXDJs"
    "Bh+b4qBH6/VTXZCRrVa29k8RDtN9Q3DIeRBkUwD13BCQuU2bG863yCFglJJXHoO4lFbsSRm0LLDDZ+/80Pr4tC3D81GP+UwSx89B/Tm0Y473bQPe"
    "MVirrTduWX8jkCZB9LOUF3dW0vpm794Gub/cvvp4g5DGrpLGGl2f3cfjEa7jcvRi9xW7flsALLZhOdUcWhaUdXOnWPJ4v7zgm8Ij7tBjLsPXocfN"
    "4g4X3sOFv/gWRTTlVQoygDiSgMs2Yg1jMorEyuo3yyDInr13tfXqxR5T+P9UlGHQRfmeMcy/+vny6uOnUpP16IG1f3K+A2pNCv2CLucdX7v8UftN"
    "UACPmW9Q+puypB4gg90j+bNc6wAFexTlfugdJFgl9D/aIC6wy5jf+ZxPv64HAqxPxdlzpj8d4F87ITFje+gKfBOQ299jhYgp2uLpYbHgkw9bp85w"
    "7eDa03dbV/5Q2jEW7bY/frV1C1OM7T+81gHeF6xrTuCsffFZ68KbaAlTNOxc6/SywrDjEEPr/utcHcoG85vvo3K6++rKwzfAFMDXrt7SoL4ue+/B"
    "+kpJlQX25RyAj+wLAsDD9eX+V3542r70GE/gMiddxqgu8ApYRK27Z9c+O4XPPHxz7fvvOWXCWU3uL4fc27r/kTtKBzxH0pufzOH0Yj3Kh6fACMpB"
    "9cLD/Dqj88rp30cgkM+v3jkLclIaf+9bFAq8rh4sr1pKNNO+u9f64TVUJBfvwTpLRR4tMcsEEOd8/Mnh8YKxJ/iddiLYHC/W2g/vgDNgTeR8Px9Z"
    "IF720uXMH4U12UV34WUK5KHGsf2tPP0Yz1uZQgh7GMooJxmqw9yFVeQBIewu1hScP9k6BdRxpXXmQevOB+AaoFNz6uTa3Yertx+3rz2h0qi3ucrA"
    "A9bF/SDixwMTFNrHgdq1RKV0ArMS4EdJYd0NdEr1LnGTBoNW3EDjnHJwnMevcHTXnl7GFnWFsXrP0qGIbWImTHTB0M7CW1/DA94ZyqtfI1uq05Ma"
    "FRft5m/e44HY9pFTb5yH5cKaiC8/aF38TAJt4IX84aocdVTIt7g8F99vPzhjCRWrKuiECT9sMW65Be4OqwMUi39AocQSlFthSHoH2b4zrC0uDViy"
    "Z8/bscIycfCQx1HEsC3SlcKtdUTYOvXNsw/umIA6odLmSnd9yFr9Y/Dv/0ChIalrwY8gRoD2/oPCZwZtliN9JE6vc5UsZz55CXivWMxh+uned+0/"
    "vmIDSdDYL6ExfQhWxitHsPh13hZ+Srb6zacoBYxkWvviddwZUzAgosRhwkpSgvrEiV38HIsmC8k+NMApWorFS2BjGc3Uvnq+9cZ1CkTcwyN9xscg"
    "VfAKvCI4r/C3DY6vPf1QJLfgvAIDm+g0jxJj2effA8HCtWzCdRrRtfX5K0APYm2wAiCj8ruV5QsyFEaP4GYo1VKqBFAznXpgsVod47/7A1KnAmMF"
    "khba5Rqau68CO7a++yPSuXvMRE8K8KxWjvFBW2ZBPnrD9TfYMlEYN2FwWW0Ui/mfJ8cPth6/Y6UJz+bZRxefXX7Nyo6V5VOw+e33H8HU1/78He7g"
    "iXMceuRODLgqT7uArkoSkyOxtKQk43kxLacVhD2KUKwcWr7g4rqgzuktw7cWSJXVgRYc4pucb138kLdHn8dA2U4xv9Wv3wX5JlLkzH0Wm3bzMI58"
    "QzqzgKko/UiKMCLJyuPXcyWPWuTqAn27YfABxcDj17GGgTkDJROa5JRmOSeO9+evYBE84UdweZJ+THa3iHUKfazeeFw8I4+WWxd+5MwJdezyT6i2"
    "cgkmRklB0SAh0gs6w+dSjD0gkcohPiEBOgsMi8JV6byUnOmwaU9bpOwevnfR1jwjV509gSwleZDHxaJ+ywVeKBcs3ZXlGyzobaKbFzh3qFB19+zV"
    "73NwJXZrYYXNKUEz4tUrD9nEkKMNhlL4jAO2BULz3pO109/aIyQ6PW4RWjh/5eoNGLnmgwfcAiZ5BXvkii1HWjHi3ybk8RyAMeuR0GBlr9569s4P"
    "LExWvsfKVO7dh/t8TnxcXikCPkYLM9fXnp14e3X5MtuRIIO8HIkhw9aNbzlIRemomwixdGYZ9/vNm7yYoN1ab3yC9HTmMnBI+8MLXZL4ONBLFwRR"
    "5cy1Z5dvoJ698rR9/lMzYo27g22QWYdzZ/lCiwrUaFGLZJgfn249/BwziO/+kUWGKaqQ0x7CEhxmRIP03iPbNFPOytO7lmBWr33b+vgiUyw8L6kD"
    "d77+7yeu6iP2WARrRI+H58Ba+O6fmf113SzGL+1BPJBBFz8jO1KSI1YqcVEo6x9Ys/a10yhVHz6GAWjsCBgAzolXlMIruBumKBRrd+knrEH95CY8"
    "LKdwNJLA+qKJd7dYmsNkwXU51nLPpXckx85pVooRouci6V6ieQ8qiL0vMyQWVrYtPx/ETcob/rh5lg4Hyx1IfYLkzITfunifA5bg6+oyHVsNrkQ6"
    "Ur0cMTQV47ZNWQ7iCc0NumAEF0vAx2S9gDDggdUvzre+/xQMH13QpPEiSDYxLQClIzV9/w7a3WfPoLshdUFXumTbxAUAuf7B7fbVT/hF0YYqUyC+"
    "oSIWGUsJRBd3i8qggPuA1qyollvPPv6UNweNV6Vp8JnT59vv38dcxt0PLOjSyqNPUHtfewhvQeeCAnb2jFAzKVrU8Oosq9MFZs8kkf8NbgDyJEhv"
    "Ap+wcoRc0gdGptzj0SK/m6Zwm9mHoCXUZ2hg2Xj7kSBUy0bTn+KHGYwEnglsOYS1yhH2iwmBRILVutyllWpyZoaX0vzE6TnvXOu1hzAsEVJFEDaG"
    "Y3CKkYrA+dQmHi9mhB1yYPhLVndGerzJBwrRWvjoon8ABQvOTI7jFQL8m6kpwL+9tTBpfhHGWSnaH5/1DMEN03B/LzVvKw9zPcy/4aQWzSKqGxfx"
    "R0kwDe1Nwad6EC7gWSpENCnDAPyV5D2mMdDXvF0FSZKVYgEepo8ZPdiox5U4C+tRo5YVcQEP16IGjHUBvz3WiEqgAY+EC6zd0JNv3i5DBzSPTO/g"
    "jJ20VIISON68beqMpzEvFyzGmHRMIvSlHWRg8yz0hKuTdYINdIdupxv2vGPkCc4JXqEOAIIGYmS6eRt+o1c1giB/psLuchjBI83bM7DtVAMh2c5y"
    "cEv5CreiFjW/aGR5SMEhpB75q1xo+RQD7TRvTzfiela0BwfnwubdBHrbEfnvdEIbHIoXG5XZUHYED47MpLUqEzJuEWZAeHE64hAOuL+wbXqqeTsq"
    "2EXjU1HYwO2qMblsDpPQ4zUasn4X/54L4Vk8VgP8xEQ21WVVuoIXhpP8PX8j9fuVBg5uKo6AbH+xLoYhDB5aX8Aa31BRKj1J3NQNzDCB/maQ6WP/"
    "lx6gDN0DUcLzhz0JENc/rSOFhlPwVs9YhvopBF6lPcAG4UmQT/VoaXsgDd0buHV+r0D1i+kxIC1cyOLL2whr2GkUbgR4us80t1Br3sqCyt9PXJ5L"
    "aykmumcjf2C9YByCGIKfjFTMETn3LH+q1zYLfaiby23oC2FjqpG4l6fDhCdnX98YBmLEUINJHWklehmmSdTivbXQwPOCm4c/HFBPmTdhV25n1O1u"
    "220tqOzYJjBEKqWbxmVRr8YYNU4a0CMvoqIH04Zd6W1CRzwMvDTtkR7KcFBq2GqIymJXgEhGcxFhHILaXyTBlbBs5Dcr6SzpUekBHu3viJ/YPDu4"
    "f3gwGBoORgeCl5pn3TObR1Mc9aR4UKGKfBx1CoOp02lgDGjBhqIAQ4EO5gFppyg35nWxFeUBIWswfHA/qs1bKBMza5ywZC4HW1R/UW18jAmOnlAX"
    "B5AopEvM4uO+6VcSJKegeRtMu8AqKuDJfovM2Dw7FZLi7IDMODgXz8zUqLgzke9h0QrQjKNYb0e6UtubXREawUihj/IjGHiZwfBpvNwBrLHkHQ+z"
    "cYTZxYA2jpH9w6CNhxpxAbRxLM2zj1f+OmZ1pY/cSB8jh9wottwuA9zYPOHjNsJHY70IYuPBFLSBAmwcS6uTtcgHbBx2+5WDbJTP9L0P2YgjnlK/"
    "OtjGQWs0YEIlU+CNh8EO4eEZ9Ma9McjlqJZ5+I3DBTtH34FgPnpQjoNk6WUOy1EadmCO9E8uALPfyR0/2ASLBZ/JWrdQjvCPAnE8ElXDmhDFUIFo"
    "chiO7nM5jGPeRI75GaZ+Bed4CG3rTME5wr92iIzmCLwFVJaifJlOs4yXQGE68kdyqIqojvxnZqx5H9uR/orpIFs5xqN1StCbQ8csKyA9DitTFEcI"
    "xnyDy1FLAB9zD1tjvgT5cRg/wdimG4xRBJ5OPY8AORFOVsiGR91Ee2lAIGHXwDXwQSAnohqsE1G2wEDuj4QcLJrSwXTasLMBgYR/eWWLIJAGiw81"
    "1w6zag4L0udBiwYJQhNkiIcGOWgWwqBBDtllzBQk5EHws+Iwy2NCHqbKe1rPBDr7lsS/BYccN85gOTjkQAf1UY4SyevKE9alsgowchjbYffZ4UUO"
    "1GrNL+u0Dj5cJP8F028UISOhM/mTXizgRcLvwLGwuqiFyyAj9Y6XIUY63w12OLCPbAYzkuMWmXuD/SmGTdwEbCR9FRUyPPuNLzmN5Y9W0G4eO9K2"
    "gr/7Yl6NdT0QySDnx+JDUbKzDnse9YomWfbLxsEkRabgsyH4z0n9F7ITWH4evFDBqNMvwGc2i1h1umej0JK5p6LNQkuitSkPax4OnKeO5ud/N7Jj"
    "DTDI0OCEf/wFpwbh5ecFQjkamfgerOpio3QE0LplQ/BCGzunI7zyaxrFMxhBKNz9N8heNsoBHFTu7hf9PYBRWrMLYyp+RCPDqE4pIuVCQUwGyV/u"
    "B93QKbF5WrZGvSY0slFYSon+6KdxzBIBshPJtoZO6d4h0Zxf6R3cgOov2gBiZRmDZyAwzQvGdzFvbBdcpQrOov8gEhW82UokDTWM0whPcoA2MA4L"
    "w4CxblDhAtPKduJX6iCyLEVdWSZitGXSdYYBgNxqUm8ZYsNg+H3KF8NgTUzpKWwE6VL0hWehEP2Rw6o9bJ8UtwJ3mYuINqgVtMJVADRcjGHB8TvY"
    "JBOApa2yo7RB7BwiJngpO3MrhDzNqYAcOKa4DMDR1qwrRccc9wJ7QFu47WFSj8pxMifsHzhD7RrnkDIHya3GuaBh1RUrU/2CGGL1GK0J8GWV4a3x"
    "M+Fz8zb+YSdlobgGZW8znRvKg2iS6SvHv6ItoWiOOroCirB+Ds6b4mjgUTHDWkqDPTZs2L917MxRF35RIhaGYuMyHpnLcIAx67EsDx57NxGd0hFt"
    "HFizdFBWNAGl4AKFODCwR4wQk7CgS0aZYZsIsgxv82ibKqiFkiknhvpcYiKyWYs+lSOI6i6Z4RugzwGQs08E346oCiwQY+TU30m3ZyREcpv6T8Hn"
    "LO2RppHvcQFTIxh9U5ue6191HvTQ+8bQOTH4nd998/AuvbPr4HR6Vo0mDlHQ24bX2bWVxFP3tKyWaByZPAfYzkFpZVpZGAlPnoib4+4llieQsulu"
    "t1G90ZKyoohBRfb3bwjec7TI2cEv2Tb3XgtphNp13n7AT9MiTwQbmt6hshA2KYK/qHXYiQ6r8I1pvlGCStUr6udAPv0hio/tNfBC6s6A6RH5k4Ou"
    "uKl1luH4UubipxkJpa3igY4qJWBD8TMz8HeDVKyYmzMVMBRwKLVwMYwrTl/o1jaNEGoeRpOLgjHulV6gQacK9ohbpejnBQ6KrOUinMifMQoWGDUS"
    "LI084kwRjZlyEjiJmHJdYQ1pD/pGAZVwVFd0BIivKn5rvfssqk5WRONhQKM/GMTA3M6pGOXLQtQAzv0Sk0RA9JQgYMMmrWX0ryIbChsnHItCr628"
    "fbKY0LpfZBdLIWmQPGss1lDNZjT2Og7F5o36/2VQR9ff3r5OmyvbbicDbIEik208WmD4k/OcFIMy+58JD4dBtflllXJ+PFV0c0PeXVgVsBEQDqFO"
    "ezkVECQiijrSO5hyEm9L+SJAEDGNiVYBASMaGA5K9BR5DWgHNw9a6p7nxDXqOnjHuuToPid4zzslf3sBMB3uwRDuCGbqOVIY2ybfqQum6fBvRvbh"
    "n+MM5jkwCp8OHzp6BBPKh48MH31pODgyPH54eHCieXZ4fNNIp2XdDI8FBwcmRppnjgxjBpt7Gw/G4bvxvQMj0BSFZbmpYWkcRhEM790L3xyFj5sA"
    "QzXPY3MjYxPBr46Ov3h0R/NEMLpjeOzI8L6R8YkjwweH4RfXwDish2lhEzio8ELzLL7RPBscHRt58Si3T5MbGxrBZeqy/GO4iMMHD4+O0PpvFCO1"
    "ebYegmTIGiCjuO4DtTLwWE2/i9aGe6sTRuphEXoZBtW8BEgJYupoiAl2w+IoMNwz2UYgVIfKI6j8KpoEbM/51lzveKpSCFDCZV4NgKrKiafiHwlU"
    "1bRsJMs6cXDbnQ5QYn8lRnGjUscZsTi2Elb0cyUO4yxNtga6OmTsM4lD4dEvZfkrEz/YtY6pu20ArBscU48ObXcsVvMTvZmFoh1N0K78gE0xq+lc"
    "uQ2Dsg6lUw3edKAfqaWLZ/CVCIvfQC3WybrhDCjV8FqjF3XItkO1HsXyLTR0jNEsgSkMF5uhYhwSGB99Cd9hA42ISFBYWBVj+R8p8J8KdOtRih81"
    "Xo6bt6q8xSg+QTCQgJq2uxgZU1TShI4G+4NRqoOmKj1gY04U1aUxjjLyxF01YEluyfnakQ0EYiFaClyORlufoychTDSITNyg/+eJ/Vrm/JPI3AGW"
    "6EIZS+kkIwVPUNqHdS0TJIPK8biyqCq4XhWU4riEYOBiEoHoOYsLsVYM/sIEMXcTojr2ve8+8poRQQkzbujNATlsEQ/WC3VTxWGUhJQVa2BBHsGv"
    "WWZ0eQVJR+QIC/0eLLiuob4gXMatQ8aOetHxQisqv2mUng1u4SIvomEPe7Mk5WbRzwNM1g5RwrxsenUea/6x3KAb1pO0qepKw+QgaODFBmQGVLSP"
    "aeOXXWmtnGZBXYzWgFZ/Mhsvlbp94LHdI3d9ZNfAXE27qhRVOEeGTsF8jHqV69zuaLIctjTrmFBZFwFPYT4j39S2Ysq6xsTKKGsMOVdkOssJE/Mo"
    "CKZtQpHdoM20/hS2C1Y210jziw5SdTEOc1J1uxBl148292lbvC+nccq1UplY6++GNTvQKc5uK3D/1YFnbSZiR1keIonLFge+VTHxXayryz1NMroo"
    "5cznXcpIH61mCmJFNGcVkIbp2xTHlM9GnPOPp7n+W/zv3MKAU9llXRp5jivK+P4fA7OWoofU7rQcYFSHwmxgkEKwWK/KqVYMPddNYJ9LXim24MYC"
    "i5oam7ZwFGe3H3U0dQ7OFiOnpmbqSiiS/Jxgb9eLUSCV8SzkrNRuLyFD7bu8BSVPbOu9YN/i8lMxNZIUkicvQIiHRCMq++TgNctA8946kLj2R3PS"
    "yhRYvWxCB13xcbnmPAg71cB1xcYdoKIz9RO5L1jxihXtvQHkumfwVBwthBzEKRTwlqHl5qvYcVdsXU4JXq4+PWLPEZcA56J2lioEGId3SDcPoiuf"
    "ULgsIANTcV8RSpcC28BG2Eq9LkU3MtAyUF3zMV8vJyZDGb4u+Zq5lL0cQo66IO3qw2B526SILElIuy7xn8fcLRZdPifs3UqoawobPD7MfhQaj+r6"
    "SCt2o0N0oZzslH7A/YZ3ccWYO7nMOSvg8g6ZjJU7nhu84NB5f7E92LymCVN/U4ghOH5D7Rh7RqY03Jcv3cH1wGNszW+5fGwD8L16PCGdBK+ENSnB"
    "l+LHDhSksXzH8UOdvqNft4Dlq5ryjmXKqcxI3oavgU9ki8sOaG4K1nfznVsL4xdbAPgdLLYO1AAKhg7b2pdBMcDbUs61fQi/QEX0EiXOj2d1Cqb1"
    "VgX0TwX4tX257u3G4deg8vFA5WzCgkO+1acovRovqfWdtkJXTAN4GoaDyQm0TNHIceTBuYke4H/5IE6pXaUrr9YDA2Zn+VhBcPeKBVxW+9/lhXJU"
    "4AE0NIAoWXRJ5JjUvHcYtwe0YA0kYSpRKY1dfgj9JwUlPOomi9STpNUqKZpOg+8Ja3g31QHEQJyzXKKFphgaLHUOc8YwqGQxJT+rdFzlyMJ0wO04"
    "NFjHYgTYc/CG+oOhFByHaOcUoZ8skbegwBlTE8HmUjH0n+zRAFCjWSPrD8bRb1Yow33qlLuGGe73QIY9dGHyojS8MHZciRSP4OrSUT4sIkEWlPwZ"
    "hnj7gyOwFkGyg51GoAo0kdDZrFNNAJgKtdnm7f4i6LArJU52hMTV+cRjfxF/eDTG1fCxh52/SXWhxoIgiFt3CoILWvTye/jDg3NRNSabzVvnFygw"
    "sYCm/ZLZjZoODoH8+QUd53VAxMMJVYcDWy/acU3Jjh8CAR/GGfIubeqUdLvDxmuw+10WjnjYlcNKDIziPlQ6QiWQJAFecF1WQmybhqhKsBJ92JfH"
    "69CIx+2A/us/MU4CRnjzVo2O7b8col0Cuqnxsnif7O3bEhjM/ewUmcYe2NRUtIC80u/hFLtTEwn0A5P1VpkTXlgFzEVH5hQFklEj8Xa0X2EV80FK"
    "ZEg6d5ST6ro6ZpcPX9z9RXf8BHNTmCdYQInkHHbtbjtqzfjpcqwDPPvEBUQGLEBDHI+gGZDFVKOl3JMa60M31v5gEMdClIPFlI1KPay7jNlMlFCZ"
    "WH8O/HggSRoVmk1e8/mcB7QkMC11zOH1a1hknJrtUvZarbCUPZRgI2NzU2Aes7bX295HEg5f64yXzGuqOsYi0qnm7enIUpwLiveX4iePd2ADhaI8"
    "sLDQOC4C2LAS1WzP4DrU+h2kcuGMhw+q7P8c/DswpFXzGOiJ3UEOnBTWZQHZ/Ac8xiauFDMF2QKyHVdf5KNcBomZRS7uHrgwGBrl9IWXCq2GiMZh"
    "t3mhIXWE1r7qD34JnXeGf+lX6MwdqQeaDcGwrMe1/mCMU77xNFoVS/SzF52m4scoJ+QVdvOgWy6K+LKE47K7XeU5Tdn+PpvCAF4TP3Raqk/54FDD"
    "JgB1XTIyVYLkRTBCCOzc70BnVS1eiLtl4J25YM9fDpNOwm1BKKo4meIAnIfyPI4Ezwq4j3OjSHhamnfWvWGD4X44JSJBET3H/uBwBcTzEplBRoga"
    "HGjFiFHOzmCYNnlPEj7uif5y9GenN4DqpMLR0iDzgZyVZcJC/A9aDwMDfdT02khyM0aHy58lzA9WgEQYyWOT/qTVxhGnmZFdiKkAX4UUHupXiNBy"
    "QKwACX1IdsHPtk57AQClTCX1RokVb/VZfUkW0qP6fh8hGpiEg7fCIflkkznB2R+4mBzbog4lxqrgJJUotKkHx1hcRK4XajchAtFe/Ro9etDTIgxF"
    "Z4ovaI31QUKjC7sfXJNiDSRj+H+lQoA6VFulY99KafKZ3iqf5iQwLzSW6EU0tqmYNEpo3CX40rls+Y5SOCGxXMpPXRvd0VdaNDYdueSwLDfD6NGm"
    "p7VqZECBEvzDyQ1gA/g+l9SGFRNwIRuokgMsNeWG1YEE0xoVXUsZQ38vANajOoZnsAWklBua0ue6+oLZWvPTKeKWTGHWURYZs3FCjH1evsaDPpLF"
    "9VM9tmrHf82pLq94KI92MOj1nTvoLUO0oAYz8WyjRhkGiQHlse1g09HWN4xmkjNoZ5sekEBhG7FTxKRwpK+Pm/aXwhziOyVJM1M6o7M4WcgWP9Z4"
    "/+UrVYP6l2XnmuQrT/roNX3aChPxFcqzSQW5xGD7C8DYP440Ky/jO1qalqXjtHjcGfRXWOOUtRA++zxSiDcTv8xLUSgSI90VmVUlGxANp6NJfruM"
    "/LEFduXlUdwcDzXZYWx5Fk5odiAqF+bVYratwilTcoGR8kZsCsY0wOSo8zwp04aLSnUmlhnx18yFtAwvqUPQnMayx91x2ymBaJcBhg4C3ojqUhLn"
    "MUiI0oxosoahTAQLxRH1+2BJpFINXhKKogX4CBqIF3DB1kAbSC/n/VWk5Fkfis7M+UxdMIaqw52BcEAcAWNcZl79GW6HGwWuPNuMwD0eshhyEIt2"
    "2jKT/Mq7Jvg7OvEkrvkMxWJMo1Cv9eehpY4mUmFhBH1HOZ+vXOIq7I4E2LHOk1kMg1laqha77CRcpZ44MhUzZSawBucDBodnc6Pv1LiXhe/3kG6P"
    "utohU+zJhQIl+taAIujt5hIneg/LP8VwLmVucoUaXn/sywELJLY0qGTR1UoTLYi/TAurpHVDWgbhOEssrnDLROqbsjPCrgMJLBoIxDPmnIkBp+pk"
    "+XA4u7R0gqRcvmzC1W9UJIPNudzEJJ8jbfI5HzlHyR6bJmRNkAPNdRFlAL9lRT3hDGpJ3CrKtXoShnN5FkDCqGA029m9Bf8ABeku/tKo7ohz5WFl"
    "qlFhLBf62Wk55RMGZWMywMOWzBJKRnqZyzkFgVGS5EPMQwFHierKVp2KyNo0Zx9SVFa7eXxWGGeSwBQJbkSrKo8x8I4GhETYaMqery+fF/VGi9og"
    "nEIJ6oNFEk6ig4SRjWAI7bSOMJu0mIot0OqTdIC/J+UnkekEbm7UnOh0CG40ueYtVn0lUNM0MzxglhmitGBTVfAwUKEinJkhYQ45oCurIS2LYaWo"
    "boWGBEKsEYLo6Qi8YdHTh6JGPZuaK8VOP4rQY0sRDCkhSD0Ln3641nwy0wC7NFkPOh1/3DnQmOFW4JUAc2n7olrzhgb/VgfGfxc1oF3wTuvpPGjD"
    "crR0WKE0oafwqyJIevP9mRnYTPgKa0fGgJJ+H9EZhTxW+ksoMqLZCFFcgj1gZ07N1csA0+G5StiYySbtIyVY6QON7PfhHMst/jlTEOnDFaLSaD2A"
    "dHrdPJF5aoPWpgM8+h74bg5k3mSE1gVD8eUg0vmRKJ6slyOkv0gyOAmT2XCyAzj6iyBM6rTzQVSbCbMsSvLo6AOTlSjGZzqITv4uQnNvCBR3kgEp"
    "LEVFl4F/DOtL86h4OsGhH8KNrkSzSFqLwA0HgBtShYnO4+sIhf4SjgMxfIJhmg4P27dShSyyneNEKZtDQW9enUQvjvmGRmohdZK+YD+/2yDeqQWF"
    "qXfFPE9wdNBkbS7EktHgheYNJGd4ZlieWQ/yHMyHarUeVOn4CSPz0QYllg6D5hMYfySYAl3wz2ksCIwzi5S4YRB0syh9sMuYfQ9GgGCDI/DjTssf"
    "sxEtC+iirN4zHrp9m0c4G9Fe1NWhsrk4WWrMNJ+wVNs8IrrpaYnfnA/r0icexq/VGjO44eN1wlJ7npjoJeMIq6ZLPZYExCPt+++AbzM0fqLKxuHQ"
    "x8H3cAQ+E81VZlHcII5gsg0A6NS8qZDxtjB4YR7oUr1bFem3UeBz++ze5hOkOvU4BrJhzROcUBw1P4nwaNLm4c/l6Z0kkGHwsYgv4eDdQPD2cex6"
    "hgaUbAn//GgyGc2HCd17yRV3wOLQbQav7w5oCfn9JWL9mmlkp6KKbYJAPxChMdlIwsm55o1kNkZtonrZFQwB7+MXrIkIXhWjnSQ2UfYdnWMtyTIb"
    "1GwX9POre4aPHD7SvLr36Ni+YO/w/tF9w+OD+0cH9g1vAf/cyW56jSo5I6DIbCEikwNF5x5qJMQRg7AHwmk+gbFW8EkMIB7AVueh1awnGPSX4PGs"
    "Dss1Hc8GWJgItFKZZEjwRjYb/b55Y65C3aKYnprLOsKhT4C+Q2vIV3nrg6EPZ8HvG/AH08qeKJ0EuYF6PgPjDvwxPILcmJmNxGCsOxD00eYTYPHO"
    "IOi/A6MJ6yGIrdmsqBcg0MVmpITIetjnjG2OvBWY54SUOgCfqxcMsLXGPbe8Y5HPWRMy9PmvwiLyuSehSqDPfTXp45+PL9RgZRUA+gBdQUPY579r"
    "5LDPwwaZ5hb6fF8N8zYO+nwgWYLV9aHPB/Q25cDPQSQBldXj2XoB/RxXQf3owM/Jtomw6iRGkBZWoAb/fB/Y1kgkk0yXCgcdrZw4SjwYdN8iVKEE"
    "tOHJDIsSHwX9APmaDgSdWvUg0PNhKl+gqaDe0epMSMwg6Of7amnzk53/dqCCc2PL2TALA6LvjxPiJB8PPeoGh94BDf1osoj0DaKkaBcrMPQBZPWK"
    "MbsVIjpPxSKi7w0rlZ3wyYNBJ68t2igE+jBoXXAL0MBMyjHQ90S4CKHxOHz0c/xrJ9uhZXjnZK5H5ucSlHOY8VJjFmUcSX4iNeueKKRznDHZqJn4"
    "ZwbonP/1cM61LHVY50gWHtT5vkg2RGGd7wW7JloP69y4X5mCOt/ndIOGOt/r2Uke5DktjUI8538V1jn8S694UOfqDwVxzp5dR4jzcpVQDnCuBD8q"
    "PPq+ruHNB2D5QDcxUzqA8z0Rmgz1Ar45BRkmayksTVJEOAf/DBUsBw68Bwtg5/vMYIJGtRTsfGCSVzo17FOGeO6KaohdFmpY4FetbgbxfNy4Ufad"
    "ncwq4GdhEezmcM9nm08qdaJbPxVIcm8nO5JbAjzfKXJZ/bwzL+F7QTxXQgwfOJAuzPSKdK6E/dbAzncSE1FZNRmSMdr1qnVRSpF1eTeJcj5PT4ni"
    "3izM+aB6mhaarMssWAJ6thEBegXtYHhHO+XbD2k+hJUVGHCC9uaCYRgWqElq0PKX8h1BtC7hdpnnxMplyZ9tDLz8JeeHUEgkF57gMIyefBHK3K1l"
    "MFbr7w5h3pCvgDUxbLIpEPP99KgNMmCTByhfomzALaCXe7FBY9JOG5pAwDW/m15ByzWPElGZh6vBr7YZq5xNXhtaCiRYihiuqC3Yn6tIeJ8djZJ4"
    "FCvWIARRPkvR3WQ7ccpNABem//cTfyg0+/cTV6m9ed9E41iVGWxxhDybZCOo5NwISXOiJXt0bqdyJNWebwWN3I9MopG1l5oxwXroEZzL2hL+DQsD"
    "zDlbQaFJcokMC2v65YDI3VjDyd/jK6w5chDkpG5gMs7Y6opA7jVVAj2uDC2gqMMqj6Bxx/HzTqw87Qo5vifCgBCHu2eaTzBD4PR3EW+cPgNJ5PHG"
    "tfMPY/LSKlkJ9PiwILG4EMiW8MeHQmOQYsQU3nSuBkg36CPA3GladVRmOY5JdxswyFGZmB3M3HLgeJDisPfh6sIMhoPoUMvMZASciHJiHEM/FffO"
    "9sCPdxgPyx2g8iPhXDXig+mTwMdhYxKcXlRvxj7OFlP0mmZBj4qDtDXgcavgs1xaYCfpkT4XiUeezBl7zwFc3MqzvfRdODlda0zN04LgjoATRJe3"
    "cjxObZ2KgcHk6j8dkHGcT6FD5GkMRhrMmp3S685RIMGNdbtBdHFPf5jHXERkHVBxQ7o7iRpYg2aOHp47oDjzCQfscGFxDau5+KdPOIuoNozC3m6Q"
    "8SE0Nmsi5KC9ABZrDrNgFKuMjC2zc1A3SfYj6T2Mz2LlLkgRLeB3ymsbAxfXJlXJ02LHoF3/I6CKq1DXTpMFj3SiobgIuJTCLKYHZPHNQ4tjtN9U"
    "5da8HFOccHdVl67uCVmcHtp5pIFTQJ/GBCUR4QHskq1CimP2wcp5pxI8PfDr4pvc+2xEyZp6/+bRxA9iRgHPP8wQKIPNtoPjX6HXD/eMLO6iuaX6"
    "7ueFLW6GOshD3UP5ORgq1vrhEfR9tcbCApVvxZhOwEAgCaZgHoMA5N0FYw2wJmqc+eoPSG4EleaNjGox4PmkwYEEJKwsRT+eWELRA+kMFBUg7cIq"
    "NEkhhgCcgniRTCZg8t3yFPvAIkYQHmGWJRI2TZUpvzOZE2DJfx2U8JKN6ivsEtU64FkUTP/B3zrmM035MVhWtK44lig7l5hIMFAvBnTGaUZLu6kp"
    "TBfgFk3CkqJmmg5xjVm/S1oJPnGUv48MFywxD7HuMJ2jwupMRQhl/FaXbA0DvMjULt9lGRuz5vXeEMA9znZWKckgrFTqiP4Nz9IISBkHL6U1PKMV"
    "1ZdM3qYLDjj8NDQ8PjEwBr8NDR85OrZveCzY27x6JNgz/OvhkfGDAxPDR0YGRoPhI/Dt6OjEpqHAN9wTNrcHE7vD0N8++BF/GRgfhzfHXzp0ZN/A"
    "2L7N4YDnhuE63DMyHvwO2hqCoYyND0z8TjXyEkxkC1jgY0ePBOal5msT8kZvCzI2Mrh/Qm/ARrHAx5o3puYy0hfIkPW6qYdg+8C9j/q8weaffR9Z"
    "qL8jNHghZ9y80ahG5cjg+tkK5Y+TDeKBB0sNCkrK87riDOOozhpD4bsZUPD9eCBGpcSVgaBZErlR2Vn1HwkWvETgWFFTElW23ekwIEYrFzDrXvMC"
    "XtgQNZqwft3DGZqtIYGDhQVP7ZRABWoAbYtLQ9mudc3SbYMBlwFxeKrbeHpzNnvD/2ZnCjViVdWMdDw7pINdtcDP/W0I/nu4NgsO/BKm6AJdrot2"
    "EKpW1lVIM0JXDdKiYATNNR9wadL2wn8Pwz4OofiBeTkLvw8tr4xGNBnVa3jRD1XfaOLEQdrKCqksWmgk83XtgP2U8MBxqkucfNB1QpnsK0VZbBxz"
    "Pl2YgSFFYl16lUWwTjEIvD7clboYSpqM5nlULnHAlcpRDUNtaC1CfyAL2TRaamRcdIUkmbGD77v0LkoHU6tN/0zxwClh1bwBdr6Riip3ZNJwLsZh"
    "wmKlEXmVqBCjH1aRKj1NsqqflGiGpWboakzDMFClzifNJwszsHO/j5JCSE02GrWU5y5zo2Lfoj+POvoAnUm0VjMQ7FbRwYvRaOoyY/YMk8k4qnM0"
    "MGZazacCgV5gQbcHCRz1+mDnVnKZQtRlI3O8PE4g+FRsd+ZnBgquQzSFEfKPuQFSiSfWi+J4zBMM+RrhklSQzGB9TQHEHnJOwVOyX0hFqCRgSQGT"
    "AWAyUZEJo3qFrduK/u3Y1W9LmS1MifgFsyyfKOmgWj0pZvJ03bG/ydjjzHhHdf2cIL9518raYpY0UsCNBb6rZB0l1jahf490td1MHDXT7XWcyfMA"
    "/u6TJNMGBCiI35ACb0QU24UFTqHF9SnY0zudBRlXKJFpo6VYRwxwv4JXqTnbaP//D3DA10sW6DIcEnF+aTohTKGCU94TpjHBXdBEbw+wEewcB6sG"
    "apPYlBQdUdmZLZYOXBrei8Q7F4RpIQFRz+eacmvS6L4m7CzZCqH099DDj4v+jbQPe9t8YI/mUcAqrEsSkRhvksMCwBwsjMkgcxa8LQG19Qpo5Soo"
    "8EzU2G4QFyEtNxbV73GtRtQquzPQDkYWqGIUnIvniPu9mViE7cQcyKCe9HEMFhkbwgA3T8zGJNxC8eBZ+AHZURxwXcxvfky+VGeJukJ9w2YUy8TS"
    "GX6tC8i3NzRMnWE7pqq3F4jvXzdvYPiKj9bp8lU68UUJm9m66qET1LeV21T0ZktqS1C+6dSr6qkE4NscKA0nceVKYL0P4987B+btIcYipDcFrfOH"
    "NsuwvI9E8/QdnsRNqLKhI4a3O1rCFsWiOyCbBJgVz7ogeTsTQ58wKoXxpm92wjc7CdA7D+OtIlPPDcGbOt7pThy+KE0OS5MNbpILMMQ7RHg7IOo5"
    "xIepgdTBVeGp/BpP2lXYtXM1uj5otzlJykLvecJ1Z8whqkSQ24jqxjN1WcA+2lea7v6UTt5sDpK7pv1fRwrDtflK84ZPCBqNWyhhcM/Ocf5q82jc"
    "rpHSM4KCPrxzULWhDwtuCoR7E30m9pBvvBX87ULDnL/i0xp41NO+P4ln0bEyfkmXxm8agntQXkSK2RPV8dB5hhDcUXXnSI+N/LNRuHPiB3s1ndn9"
    "w/7k+F6H+svJBldR4HbKrkLvtA1cBQDWJA4Lw2PBHIOz5g6G9YDC7cZ6uOPx2nUQuDUlapnbKwL3YE/PlQNv/xo+4ZiNJeeOXq0HtI2RyYggsGYo"
    "41480fyTwtYeypW3kJOWcPC0ZOxk0Pc0HDbFp+lwJ4bbp8kKAksRrJc6RzvKhoTqCu1b8ew6gGwndXC75p3PYesarOeBmNsLMKF5sNnNg7glGg6T"
    "IsZxNKfaadQypPKEy750LiWswev9XAergbiDGZVo1EjcJq3o0Lj3REnzAdX8yMp48Ny4sj46N44PScjCgnqne/oDdI2RSYk/MwPKTfUc9O4cWjIw"
    "XDx9Nx0lJdDcqspWV8cZVi/D5eb4Pe5eDpsbXaXDriI7IxTnncZ6CEQ+cQflW+bhdB+eCdn49bckUXvyAg5jvvkAwZepSf4aZdac3dpfFDC7o9qu"
    "gp8qPmx/cIgWHfcG+0cJVLNRFvc4hR6BQB1+93iEMFF1G8T20iIzXvD2BRmDV1INglvVhPFpyV/48N37CJwC5/xf/xnsR8juaAn0X4WaiMgp2h2M"
    "RtKmVKswF5AjKiF8suEn6z5sN7obFWmdxK4tt+vME30cewDnvjaNMyCa05uuIbwN6Up8QVVd5iC7+eBGbCrh9VuIkkqMTwVMmEXxXWNLtt3P4nM0"
    "De0BBCHNQ3QjS9jEFVZhIaiiad+VCXPH/TyOmirGHAZ2m0xIAWSmr71gz0pXHlz3JDzKZwNz7KOZMdQnAD2obtNVZkMEGDYtg+ZOiHS6c1MqBkFn"
    "jG69AP3BXmgGDZRADQNRdCapcIm5oByo2yd8E9ZQp7QNXPdQjYsoaHGJa0ghj1tACwXYfYS0Buz2FB+Q8PG67dGJ4N93BerUQ7ZgUaFoCETy/cF/"
    "7EJn3yQcDBA3Rhy5hoDCM3LMggJpubIol2Xw3rH765GVMr0sWf1yVy5k5BtPGq3bIxy/YU05tmk0fkMuWbMRO6sF5MVK5ukABdv9az5vFjg0rV36"
    "5ENNxXf7JN+AYghBJ0GBAh/8vvmkNh3PsrNXrSrTAnWGMkXwoDB8zCj7OBcVIbsnrTpdalAaHUna4HZzcZ1J/tj1wSKQyiyaNySuC6DdhzA6IWp5"
    "MtLGQUc9bNoihmeFUZxtIiEPBIabNU1SyaaRnga8m1k1b6YsolVJVQPqTU7irI/f7RQHkSSf+EyoNNFRaiLfk0tiTq6PxgQkzCF6g+b9kjcWfted"
    "fiQTNJMsVtlCkFkOMoxFHnDYLKIlzxCDHGA0agFHhOdpS8lFoUzBTEgBWI31TcKrgPS9P63YtdKZpZ0lJ0NY3fCMdHKlbPAU7+1zjOvnZnLo33vk"
    "SPn61qU+3oSxQqB5EbT8spzxE50uIXkEh1xCod8AUeiQVQiGYE4iGkxcmYcGPiSnXI2imrQIa2IWyS44SIB+EJkBm/K5s2XEZPp8OApDQlRhgYbF"
    "AVg1bMqtzBKLNSjxcpzU72WNUNDxXuhIp1FwYu11QAmnk1nQhoHasR5wtts756HTJS5TrOtxONdgRM1OZhM/Xw1WDkO4KTyd0BVOh2ySRqoQoSd4"
    "b8q28cl5hx6GhUsZpTgy/0wVeLJCsyITBJQNv//vaJrYcymqJMY27lYJ0imd45XrsEbsiu/9K+yXu8uVNsTlMG2KXrAzOb5P50hNinA3i67ma4mU"
    "BUoSAOusQHpMEnNyn6JJp8Olhqq8yoMBmHNA0Rwe/2LcNyCfEhRwnI5Ct2OXa5LK61TFpJ3YbjyFawtO/37iqkfwru4LmurjEiX/BDZ/dTgVoEyJ"
    "0FA4twgB/s8Tc+WlfVQV1sB0UC5JgxAesGTUL0sKtBUOSG0X58kwMk3zEBYKE6rWW2qY3l1KDcmmn020wsaCYenV3Gm25ni4ae8wp+dCSo2IBZfU"
    "QRMlxoKrZZQAYzFVhAIfcvibAaVZqKRBsS/mIGgocspn2p4GV+c3Df8m5lQ5nTLAd8IaVeg6jEzlmWDOcFaGtpt5XXFH1Y5rkv/hUBSOJwcKzgEN"
    "oFlX/Cu5XqRd8hi5cpETQ1FdqhO5DtqeiMDDsELYdNBSnV0YFSNesXm/PjnBlojUbIKIcHNkXdCnvRsYqHEYzIBwnKpt8IGbDzKyE5yDiK/y13MC"
    "f2QGWAAEJ6oykKGwzNXmjeYnCgi8qAlQBkW91nkWiVlXeBZFsFc7xX37OOC4AywKFThdKVdrg3tJgPQo8m70XUlBltdjF3DwYVteZAqTHGqCx+Zs"
    "WJh8DsXk2FYUMxp1WMpKoROHu8JG5zVGiSmZ6sb/xcQ8v4THSRApxRzuqwV701o1X3urkL1Ix1kaZp0QM1RLDY9VcX4zeMlAhSeEXTYLxOkObHrV"
    "FoU6C1vgMWP8bGkMwxm0Wz49C/uA9IEBLdEBeSZwJb3KkG0HKplvftqx+ksnjLSoIf0U9uIuBD0l60NiklEDSxUiKhQhGiUYG6vqlFLsD8rRdeF9"
    "sZ9NsNi9SeYE9dYJXGSSzOppCWiTFAkxJD1rsMiM6IRxGcFLIw+TuZCFGlrJ2EemSprc7J2i0rgZ/YGCOytdQefXwDoTACJGlR2spBeON+C6ptQe"
    "i1LF0DTxUzeIjidjzZQIMsGbgUDddID6HsidLWP0LhoUY4qV2EEyS68SW0OMaBg/NnhETjDON0ZrLM73SB082DBJS4G+98a1asjQ1Bbjm91QxiHs"
    "CvF9hIHHwyVkKMqO4mU8WOiAt/EgWvMCWWCLcSne91AMqjmF9uKASgaqaRKXg37TR1wjlLILDAFehP6GxxbDYKExid+GJZDfRxiEPsXVijF3mpYB"
    "ftunpmppklbS2XgqLUf9HofPPPdpLMmJM6zaWVqCdglLKAf/HXeC/6Y9oCYMSkTqaYUJWZxO+N9MFLSS+GOdXtfo3/yZRloO/30Eeq3FOMgUD0WG"
    "wUwqNFFCzowfZ+eNlysCPSw26lEeD5z/MP2WyU3xEmrxdFqnBcpfHoScD2sTm2KiDljgQ/FiozIbukEhNL/g6XUDAfcnI4/F9bBgpI4TxaS0S3KX"
    "Qbo5OHDhrlDWjuK5WKUK0owRQ3gCYTBVnHt3MHAHPBwFL+A9ILW6rMgC7h+i9kbrI4LjJSIxXSKCB2QdSdJImWW6woDTfYzRFEe80w3DgFMvdO0L"
    "Tb8eMkHWGyGs+zTGpXrF/eaW6Hp0E4AP4aHZ2RiN2lrknt0K5rd7I8Wtcp0K2DUy1PNF+y4dge09rtimplMQzrCWVRAdoVychpJ6w4Dfi5qETV88"
    "6biRTcW4zluG/Vatuv2Dl+ikt3sxgSHIJRdxulHcbzqPD9SapbsCYJxZSlB474B4gOa2gvjN9XDCiOZVw6e7pVu8PEh3sXmw73q8QGQQ6m4RWDOF"
    "jWnUU2iBV9BVTphm7DKn24T2PZbvCddSWox2BSjxgAJrMV3/GyWzMEgwykh4pzXSvCxwqfE6atXOaN/m22AMj5KPHB0fHJkY2DzM96hIZv5tFsyn"
    "IKa3oIEKKjgWS0B2WC8I632sQUKyhloHJmYGuy66tzyQEiGj1qqCZ5jSc7h3vBnlcN6hVl7wyBI8EvUE6C0bw78QuaBtWhNdHciFMtC3Q/IeX8Af"
    "g8VGyuRRjucNX0ObIgoqEY6gAOcN5lAyxWafbyF2BfYeAgIIkWLgR/gttsiJcQdg7/wLHqz3uGMIC+ydWljv8ebXRVzvtMAgPq43/D6T1pKYflSY"
    "3qMY6w8dpPdQaBC9B3KA3vgx1IjeB1NYmVRBeuN1v+B7xamP6n3E7lcO0hs/R0Zr+5DeY3K5s/3ZgXoPOgsgIRhqA+g9QLSpcLz38hU8R3L2nO/l"
    "88fZ2AfvHrDWmaB3S1sGvBvEWD6mZP/wY2+D6QJdxhc6+O6DIeqhtBL9WzVO+JPC7h5L6wXcbiKVHHA32eUdULvFTsX0YC1mKldg3YcIEMTH6QZ5"
    "5gF1jwyxbIO99sG6hzP8aJyIUsBu8DGMVe1DdgPpiAcCgrQcs1t5CxV2sxajAnb3sLYexRxlTLcCjnfhUc/0LsH1HiZSrbNoh4+Z9T3yyN7jCNgZ"
    "kqSAZYoVtPdIgmLPx/aWj6nD9T7ENGHxJg+ae9lShetN/0br4HrzrGTlFLb3OCmD1MP1xuox+soBejti15DeCtGbcj988Rd+Q6TYA7j3XnHTyrG9"
    "Bzroh3J0b15SM1etDzTE9whoDfgcegDfDOudsuPpY3x7P+UQvs2fGXFAAdV7YHExZvsZ8bJKUL1lw3n9SyG9X7ICG+w6+8RmEL0xthCJC0T63r66"
    "OSxv+iotZP0kGBcHcrnZ5rG8GWQSfpvS0jxUA1wXxlscVwa6dsZkj0jeVRH7W4PxNg8HeEbN+qBBzNeuxzQyoNMKRodi2+cmsbxRKOFjpLE3i+U9"
    "oo9gusVPafQJuYPqNRg0vvY8ULxHKjashhSG8Sn2B3XTjrf6grSCl4JWdpAYsnA0xrYNAy+ksCFYb2c4BVGQCzBwLC4txfJW3yTrQHljWzh8fmjj"
    "MN78KDvPkYm9uMq9rYF4c7NZwz5h3oiUb7tBAG8DONuwj+EpMjHd020D73YxTjTqmf/C3eaez7pVGBEHOVMyKmspchN9DrTmVDGkbUPu9oKwYKdg"
    "PjOaclaD9Bnvtmc6M2B0cAswWgz/JgXl3jNWt0hr730kHnEKPc/Vp6WtoHbr6Au1UEORl9q4ITYjfhywGfaObG5jJOTt8a2uRdxuVMm1aCFETWHM"
    "PpxMEbubLRZtUJVid0ODKJyTKGTq4EZnxLIuAfGeAIPQBKvF1w5zCN6DKcYBcR4cbOoK5E2/YGsYRq3A6i8K7p8xfEuRvK/lgbwH3Z4KD9TitATA"
    "G0xOvPsWv9sScveoJqnmLdjKakjiWxwOtO/xlDAoliD26KySorAXRtsG/O5RHeVgQQbjUbEPn8zltmGM1U3zRc51dGZwubYHv7t8PBgkCwOs5KxR"
    "1+AOYhicJFMWTTW0hKAYTQWecpHTcGsQ3hwqQoljYJ9c8J4Viwuji1xRRt7zwPA2kjeuLpAwhpHMAqtUNrJfPx0E7ykqnPA7XKBajR1qd0EV+v0/"
    "Vxhvs9P6ifXhu+eMyjDxRSYbo07jHwPCO5HQj9bSjSTIkQ9TRfocMLslVGoj1UbMybjwVncPSWVa2TW7rR6FFY7d97loRu+g3bG1c8Pgl7Cc6ukM"
    "n14Mk7wLuv2g3ePoHci7sbHheTK4QrYjtruwCgg5eUoXMKVbwOkuZARYg6G2MXFtZR71BNQ9gE4/qF5S++Cb1YQbON6IJwG3DNZtxTinUOADGsAz"
    "lUaWEV1VwsW0ltoUSqrf3jRCN51iyTBCT68hMMP0dJzNGN+RX0p7QeieKjMp3BqFPy+I7lEeJSwADbkP0yUgrYBJYZCNhYVYYKBjxiQGqYA0DwK8"
    "gYF7HGpkCknCAIE1KNsemwn1B80zCDCTxZNkeMYwh7AGyjxL4TkxhLRu9xqhKEFqYwlgL6ALsBjutmkbI0ZYBi0g2lTItSaYIfnXAegu36Y+t0sy"
    "o5h2zsZw/Lguggojky1gIXRKqbGEEz/TlBWjn0OZ0lJos6iYe6aNM+4JsACWACKUBae9XOYJJShsoUwQCwDQacsohkUziDL4IYu2hs1dYGcqX/BZ"
    "Gkw3YJ163Bs693BHa9MIorAjQLf2VWht+MLbLrjcR4ZfPDoyPjIxwsDSI8Hh4SPB6HBw+Mihl4aD8UNDQyPjewcmJkY2jcfdcw/YzJGBQWhgYkDa"
    "G4BPw3v3Dk9MHB2gZOwmULhHDh5SvRwK9o6MHQoGRosvDo1sBXh7/NDoIYe8fYIm03XmmGb213ejcNuHayjOgOYWwswrQEga6SLpTY25jcrevd0J"
    "Z/swfYrzGd1yoO3RcKqBcR2ynNTj8Ubgtkdz4UIJEqKjI/ZTznrqHWWbs9RlHOQ8PlUaAhz1IwFsdzUC8kFe2xmGel1nsQvgTU0hlNWiYXpRjLbn"
    "LWFrJxwjomNyniGtDeZd3c3IbcPV7nkwvbmA3XG1bdUkvSrGFmcNwo5Hbw43Eq6iMnZ26rtCG4PWHkqnGsjHJjkaU8EAlg72kaIh3Zax3SqUZOR+"
    "uu2w2kcTrPmqgfrE9iJraJKiBYkhY42t0U9j9p2gkOCsqIzHBE1+KlDaOD0eiY0PmZ0DEUShEJ3E0tTXHwzOoYnDjuexhop7oqCR2VJpkqJYTSNM"
    "vvRKzAEWmgqYV456KLwF5hyvo8QiYS3zAZqfKZj2iJFnRv51zILhYZs0YJfMEwImuUexqw7xxf6AfGXUmFNYd8H2f0axAB27CqiaNkjrHFZBe7ca"
    "qjot48/2YfS5ivcDoRFawWFM4bG9aKvY2akLBEtdEDIPni7yuNDSAYboPU26LaDZI5WgSyN+Jq6yoyRYiKM14/+ZwWTr8EhhhFPFo1h9SAKMgRrb"
    "3onsaBn6q5F9S4bIqUv3MLxnRksa3IUeZKReAdn2IWN3iGD1qeSgkkQx06FKDgvDiXJ0KZ/uYNgmauQ1g/RdaOc5QWLzbpS1hamhROUJEMoyFOe0"
    "VKxsExp2zwbOulN4HljY5pxGunFpuF0o2CNBj7TqKQxPmWiRlHbDvBb6XCiadO7lf3XE6xc3GGpPmrfdPHcVakEwcCaaV3ycInnT59SEiDIuG7bh"
    "WJkyx+8rO3DOoJ6pZhEjeP7Uo24TL3DRj4loPRpRs5S7oU4SqjbAcmSwSMS8oQhXSEFDIFrXIxj7qc6Gm/53B9KYTavHcvyBS+OnpPoXvn9egNWd"
    "vfkaJvIjYlluVmULqFnvGEq4QXDqfbBuVMVQSyRjQKuImEJYao9xYhRHoXklWheoWp4zB2FY+u+QxEZXtOoQy4nTUoOsC1Y1FR/JLzEXXCxKrWgP"
    "QNXj9kU6noQUYzLYO3KBnDKAaqlGxpSoK+0oQaf2qvzRnVnk+vI8RDVqRUxhSgmIOQcZloBVc8SIGlsgpqukpYjVHLkFHwvYuE4mphpqGXK1Ot0Q"
    "a10aWn1dBmJNZmzC2SuyArwEsRz7DLsAWXvHdayRgA+WglkTnKpLM+fBrNUfzwfJ2hTT0FCpgz50hfItR4E7UIg9iJNWMYfqpPmZOMuQV4j5qIu4"
    "gGQ9RBYk7Qd9/TyxrCuqCJHYaRfim4Q571Da6gsqerORdea2AmpN4Q4Mx4QmYSFpuk5koaGtx0lo4lf04xaQrV1L3lG41B6FU2/zQApH4jaFbr2p"
    "fuXtzSNbD+YbjapkR+AxRvsqvln3jlZuBdPavIiwKfBSLHxPgS9gLDxdgi56+jPAtj7mSyNl2dhOI+Kg/Pk1TdC7uaCMxIKk1lPxnWAQSAxgBip6"
    "4Lh7D2jW9uSzezZ3ZnQdLGshvGMFmdsrmLV7bsNY1ngaIUtNvIZIr67OI60HaO2fsA/Kzuz+pBCtR3TFCLgyKR5JQsJg5z4tnQEZ4j0NKuOjnjI4"
    "THqhbQmuKRVfUki6hnGFeoPOiKTlw+yAa41GAp6olaw/+Bj9wd4QQ9wLCzhyxIwAb1OjQy4soLmDh5GmYJ5TaH4ugLVZobddtXZ/MN7wYKvl9K5G"
    "rPbRqptnQCxifoeCkh5UNaUlPKhqHgUs8qI+t8IWeIy90yFE8tkEphpXH0wt8KZ4J5IGfFcCUT26w3P9JH2Wqo5KUaox9Z9HqH7Jr78yYBkIWexp"
    "Cn8DfFTqqAZaPUvFVfSWOHhhoZHGditqGJCPsSfSLD4M9UhCJoHtUaIZtOGHZDEx6AU0RE0s2H5jF+DA+I4FoB6xEVCdBJC4SWjQlSQ5+4L0X8Gh"
    "ynqoSp7EO2GZg6EeseP6r//EmAMaoVh0kQE5TyEedSxMgvgv4BuwI43Vgo2IQhqxDz1tquA5uO6vKOdwEjQNEwnRTWHwGWdIcUpvEzXeNOz1JIWB"
    "Y7fIXJOd5gCny550BwZSRGzFuhrEcuTjf1HBta2x6u8P9pWfCzfbO9UBc3qk6uqDaJCWlyaJdQehexJhsO7g2NkaajrbMoNX3sDACujSCbEUzSD0"
    "p2Zz0FPmHFroAUuP2I5iO09zeNycts8hTIdTWGlClnl+E9PuqNL9ge7O4n3EeoXFEyyHk97biXAVkvThWlSNA6J68jWBPRoITKgApEtq830M6fwD"
    "CCVtdj82tVpcg4/BPLK9CEqayNYUyEQ2UcpKB7zkBQcxbXbHZuVDI1s94efIxZZeNBIVJrS5WEKStns/Qwc8Q40erUnPUEONfC7zFstu3AS8MovF"
    "mhd6zYliBRY9aFdHggPw+K6ysKbLNfapqHxkXDxkOlg+GiQZuBigkeAcQYLgGWoHC4IMkxBBFUGjbeUWjHEucmjRasI2E4LLLWKzABQ9TkEB1op9"
    "mKwD3RbnpGxHdWjSaYRVpGfXT8CfLA2xGq2h5J0BiLacVmIGYEoees0a6fqo0E6OA+lQEVzKMnXK0rkcJ+T4E2EfaBzooxL9ZOLzZ0rSL6ZV8Oc6"
    "MxNPhzxVPA7Bgk2KCWC9Tb6ReDTFaCJwk4Z7xsM7BbTnQ7L8/rGBKOcmKAXHaSROEAQ4IlPX4GS1oe4cpvNBDG0lEelnBKerCVKNzZ1oi0tEOUp1"
    "UXIxeTHoCEW60LdChmgjrcUWQUl2XXRO6CE4S2xcaQOCyVqMjE7gdc2d7xJNZgv1dOSbdhdLJSjkaqBDVDwzE2VgvbKIYVQUKBGVH8S26LADRjOe"
    "wNnRASMFw8he8t0I/j5XdDStINfosBctqMHxUjidxbyphUOpBByvrdAxToZ+k/hqTxjNoyZ0ZY5Fc91trDGnIpeRsue3zJGadBZlBTAXVgAg5fSt"
    "UzmgLFdKbrsykfXAmA9hVzMs3b2UORAGnegwB7CZAhjNpQidxbH4LMZTiSbGT8Ft0zZyXZXunMNZeAe3SzCVaVSyoewVmAqKQoqhppH6dquyQiuu"
    "Y1dnIzLTnIWVPxdSAyWQKHiyIpry8xYj5YVbRxNN8+g9SNwoscbQEq818jKlErgAg0Ke3euDpCLKrikhTebP1XOVkBRTeaUw/C7ray4vtpKgBgyI"
    "xj1Gy9nbZdtQoi5FrOQR5XHVIsKtNQeoDRv1mVNwaSHhreVYHw3Vspw7z+sfq4HB0DpaaMFyGtbDAiqmNmRcOaTkUfSieI3/8pWFbvnLsrAOpsCk"
    "hlWSFXWR9hWuVrVZAE5geHhLYAObOvRIFa8Timg99uu3aBektCtmKfyXr3B7bLd/Wd6N/Yo3IHkOek2NgcU3xobIeNUPRwVQZCQb60uihZ3WuB6M"
    "6AHMIqCZzqJ3GokFCdejsU7VegWatdG30t6MEc07Y8tBo4ALcI0tA+zZmIpDD8irL4jKqmt0a10gj4/mKkho8X0NJge4fZ7MGkj7GOA39mI5X8rh"
    "Nq8P8Ww6rGhhEck/xMMrnVO3FMsieUKgNqazHN4xCWxDliAZFhYotUwtoYhdFGxiNGaByaLdnU64OWaOQmUB2Yw+4wpwRlH5gsZqYnTXAr1a0s9j"
    "uXZCPR5x2sdCnwovWWAkySU5k4f9u7BSZRA4mGEFx05qlLUYxrIqoLgZLqIS8gM2wiiBgpBcXg8/NCAoW/Z3bWIMrDurplVGSYVHRAyQk5yFzj9M"
    "SYXstkN0MpLHqShJnbR3G2ah3YwJQ7adjEWNPuUIj40RpBU/1w9PlkLoxSyrNWmjuk2tNqulZecm+QiWHI1WiB7Gce0AYzwayZEbNnvFHtKYRTAc"
    "xFsjpzjms1sKgMhMzwpPfN6wtqqN1bY2gRk3lhSY8aH/d3lpMpoHE6gUznikupTCuxrNeCKaz+biWmOxEtbWAzT+VZrABI6nS43FYBEVdy2uVEN+"
    "sYhfbL+hL8qhi/emx6fxEobGIgxLfoD24iJ68aFqNVyMj6OWiisl4MUHG3M1dEBDvNMlSyfTehl48QS0/bJ6oAS1+EC6o8bDAS1QSQl6LwdVzDMu"
    "tdrtlzEsdRZ7stzhK5XBFE+Ei1k8I1MIay/HizmYYvPAcco6l8AUQ9+TIUiKRZAN1HUJmb4YTjYqwfwiXluXxcdx82LU2+ExeGcuj1B8IKrEk2gh"
    "HYvpxzIpR9+hdAvr2GBwLEaPHuZAdMJLlbPMf0sUtBQm/x3X4k6Yxftxk0Bk7ag0qmldxplmc/Npjfrg0XaELoadPoZxEBxJKk/7xiJSTBIbYnBt"
    "bgK0GPkKRtgXvBxlc/ABueO4nmSCDiUxGvfRFakYCP2/G6Boq2GGQMXzIAnmM/5xPXTimAZCy2++nQ1BKeOJgUpIhNMNnbgeHgOlj2UowNfYyEbh"
    "iUGaUSYurmAAIJmNl6B7XgMZFo6wZ4xifNguHA9pV3As3QF/QyfbAlBMXWT2grjYPDSHCjaG0c+DPAiDycjQXSIr81zAijuNZjrEtP4xcN3C6uwO"
    "4O7pkOqM6eoWO7LCuHpBK/bfr8TzZsEbi2AxNBbDmZnwGDA2cPfSNuAWd+zOkhzJPjAYbSPH0x3HNgpdPN+oV9Nj0+Eu/SBwIbDfLJ6WpR6TWTxO"
    "vCOBH7cCYWxxhsNsOj6GKiNgFt6tnptsHK81ZnfExTFsCc84SVlCms7RjAO2infbL4gqLIYx0FBMC7pNGMYHG/DKMQxCI3VORhVwajE1hV3soi9R"
    "HB6PZ3eQTiUuyVKY4TTL5QSE0nqoxQcGJsZHfjsQHDz60sDevQMDL8If8M3vgkM7JoZGNg9iLFKblR8t02R4HMebYPZlbrKB4/77iQ/dyOdBz5FQ"
    "mEzxB9LFPcEYoynBXUynMZAiqIdwvpGIzi3HLz6GMFFOea0PW3ygAToYdM50uAg7cAwG5yS5Qyreg+KzEh/rjFJM7Rh2rIXHwiprcR+n+Gg2T85v"
    "uuP4y4za1RWgeCDD719OgOGVTu8ATjzBD9bDmSyumAcdPPGYEL3BJv4t0/NvBSOyAE484UmYIjjxRE7t+QjFE2RvCjzxNP1K+MRHYT9zEMVgelXj"
    "4yDUNEzxeDgZTiqUYjJsfIRiMIjAzkJ2IBWtMYonFBsXUIrtj2bYDqX4oNb5BqF4CIlPAxSHxyvaQsuMcSYWrvPNfwOTqPG3CqWYpsLfGphiaFHB"
    "FDdq+SDPS06LiaGvol8vhlXw3x1Q8X5UwgqaeDiDv43H4QCKJzw60RjFI2xtlEEUH9oBtkmNiVyZqgqmeBDsXhjiJIpSsOp4bwxk8Tgux+Jc6IEW"
    "m08eYLH1sNjzyiEWwxbOzePgC2DFEymmH1BO1sPjx9OapYES1OIh9IrYa4gLaMXjjblJ/JuNyLgMpZiNbfVECTDxRLogBmyAoinOwxHTZsFYX677"
    "YMR7Ulw9Nq0dHPFEYxbDrzIlQSRG4vAgiXmT6si7MndJKf+GU+9FUOIBXAMF4+qgiB0TWTDig75544ESGzY1kMS8ioYxGJeY/81hEdv9DpLGMbMW"
    "phSdfLSOkMQv+iK/HInYiPnJ1FGlBSCeSHe8TPlf5nuLQczfT8cFBGL/hRwE8VElWgoAxPxhOjQDkbV1AMS4xcwzZeDD+S/nMasbbwZ8eMQ5PfYl"
    "ChOQJbI5AOI5IAogi0KqC+Ub/SWyZgsAxCx7vZ9ZZsP6xb0AEBupRXPETegVe/hlEeZbBR8m1/kFbOgXQbpjidsFLz5cCJfSRFx2dkmnNwM6PNlY"
    "MmYI/FXHIufNgQ5PWN+beZLmDj+BtEL5Cs/upMWcDUFP+O7y9gMP72sspnPOscOmuHdYrPkUzMraNJjvDTFBRSaT+Zm+HNdmJQBHisGiDIsvyKPu"
    "BXLY8w4WYc6NuVo+UlAEHE5gX/EWchFs/HVHzOFFmlsdbd0k3DDqsH2SfOJFE0Zw7uL0FlCH4ZUQDFKO0YALA6s5y6Ra0n6vkMOOHznkiXsrz0+L"
    "8bYdkMNK3HGEcncg6MLw/lK1YXnORRLBLapgSIh3dzreToBhNRzVmMROd3P/jrJoSEl8TJtcPQMK81wwxoaCBWNsxq8Uz0yF2XiWWwESrlI4lW0q"
    "EK87jscoHGxwhEse6jVyuZGDnFcDPx1LF8TmyUEIH8CBmtWoAhHGhMeehw9GNZOS8TMddwIPxpUH360K8mQGeJkbKsEMtqYPfz1PX+cwgznEC/LH"
    "OCAd8IKHRK8GDbz8lpD1xCbSQMF7GvVGwm6QBxNMtJKqDSuBCEaD+FhMoYMtQQSzIegoxPEF2t/ThPYHrJo6N2Ab0IBpS3hqdD36MQq3H4srPAaK"
    "NEwCcRAf5Kl3Oq5tDwawHoUn6OvpDiDLKkaggv8Oa+FxcjBAPtckVL41nF8Wp7zItZij4SYCrl5cDMn4McHy+Dlh/G5g/cFsqabHgngp/umA+i6G"
    "hf5yPXlxRFhpYsnnCuprNZx6iM3YeH1sX6PH5+UHtf3bg+lr97PQiI7wmZ0WnZiRs1XX0aHtBvQ9SoYcKy+MzYp54FSJM0oTEkgB1g/D1qYwpONo"
    "DBpvxuRSE83XG8LzNTuYe9SknKZtxoEixXRJ0vbj+RZbdO6aiZw3WI/aho6n83EB5YC30Kh8WopeQX3VpoAEhFbnQFgk0+FxivaIApKANmmszMbN"
    "e0L45YfqKoaj5LB5LgDmCdFf9vlgY0C/Rqh7PfgS3j0fVsMKUpaykTYJ9VvlvC/WioYYAwTWgg6xTfduLzi//rBLDISfEcrv+Fz4chYfh68lVkTD"
    "lYQwHreAwTZqDUoRAw2Da0QuNFmXqJiOh7MpFZRRzD2bS1A1zcHeUhISPLvgKJqd8DOQJtpY8j5KvriKBHqMM94L4fE6kHW6ozJFuht2dT6GObBP"
    "ad2TyQZRPCYMiLj/dYB8O+5EX34fFmUT2MM2UQySRZPgbr4c4yn8ejXcCf8Hk3ba5EQCimrANEDp4qtsENOKp4sivuDrSRQ54CtjpYESMjwuKq3Q"
    "IWYOdiAQYOgrArRZXUrHJpJIEZBJExvPf/Nov4ajp0Fu/Hdo+LkaMkcfh46zOVBIaZ3S8L2g/U50MD7FNSqH+Z0wE6LkIL6pvIwuYL9DA6Mjo8HR"
    "wf1Hxyyc7Z6BXw0cGRkd2jzAb9dW3aucohwdGNs3MBb8dmTfjpHx/ZtF9IXnTdxgYiD47aHfHX1pCFq1r+ykr/YNDO4f8Ca4YVTfvQMvDkwEvx34"
    "zejIxOjIAXyjy3QPDgxtBsf3AEamZpF4p8PqLvc8kK59jPU4hon+P+7erSuqM98X/irzrtNj0Izd611jXeiVidnd6STqjmZnJHcTqdaigKKpqqar"
    "LvbgqCggpuUooJigoqKgoKKiXnT8IguqCqxy5Cu8/9NzmnNWUUCRlfQY3RGq5nyO//PhR0RyPBrK1052ivaMwPA1sXJOesqTNcP3nuSImwThArVN"
    "jqkkoUNtR+0JyhdTzbHOsB0SZp5sBk39uF000fxL4fqqkdW7aSlyohCqJk4rkOpYBAmhA2WBchb9dxQ+ScQ6/cTBkHyDJjK+84c4FoBUNSHrid9b"
    "bQnhURpC7h1xQXXU3pOgE3QRAkK9nMNgcsW2DyvyE5WU2hNa75fa3utMxJuwMAqLU7Msobkmqw0v3Qrs1RmhF6swqC4TjWqOsAH1+xZNccwEbKWU"
    "Kv1D3oS1ovDpVNwJwoD0qeVFSR3HrwWt97NEgrdKd638RUzx6GLNLFmDZM7RQ5g8iLehgYfaE9xMshgyygYJOL2aLtS7KrLPVZCSYgBO+xvSsT5R"
    "MTF+g/i7n5yP8fpEMjEJaMKBLcJ6ErQejpvxQVmBdLkEXRdoUiVwDzgEm+WgBTuDYaeMXVMkLidmeZvRhYVL/Rswk08WeTuberS+lBKQqkbqQHi7"
    "VuqILMm2Th8rTmSBDmsRzVhecLwuWLsm2hYOz8Rzni49daM0wZzUbwlhl0mo4hrV14FF0lqIEn4nzhzJeFpyvD1uVsgDNMjXapVtVAdPFXgJy0zA"
    "cWS1JPPAX6wrxi4vIqnVU0jQtPhtGuAfd+dOqQOLu8LqJiM1oArNHA6UbkMwVE/ZA8W4JECpHDlqMqXU64GfGzQwwGAMvE5B418KL7e6MFPKQ8vC"
    "uFSI1AUp16IkPUY8LEhCZk+4Gr4CPK5jiQdH8dLhisF/d6zcUBS7+gmR+Pm7W+wXGd0+4pQ1YDiFgpf4XbKdy26DdK9dB6SoRtwtyUV7q8QIlXYq"
    "joDaqxHEAovrd8LZppUYBb+sLd7sW2HmXwRD93NiIvya1pHCX/EHq9BbYvR6pt9ptdFMBeDnO3XbhYzDoS46fGxkELP3MKBya/Kcm22P+ah5n/Qf"
    "1nkmqG+OJuPSdVRv8Zowc7+Fjcd1dF2JJlDi7Sl0XmJpTqxXR8mFh9kSgpPnlLHuXqDXK8Pk2kSNwTyM9FWFyOUySVwuuTT2eqXWrAagXCsqkiSi"
    "ZceM1L81VBRILneP6ToHy42LQMptoU7ABM8WgZCL0AX/IHaXzrEgLq783ua3Gq0fgMTl+gvKwJjcSxQULi2V0rtYii3jRePftpkuwWD2FKVSczXo"
    "22+1DaA+x363VDwS+Db4SQD4Vrjg0HBveUzuQQwPSNUq5xOYY6Cj4EG4Z4v9I5xOEvdWKaSLdPtnaZyzW/QOAe72s8A9sWtKekGNDqvDNtkjykdj"
    "+7AhdMWw73/AoJhVIfUhnZR7gL+1ip3s6oFsEtvGo9YUDX9rPmJ38gD4t2YQNyZo+qhCWLOqn2pfuLeV58NKgGrT7RfzNvSeesHjv2WEshkFXEOo"
    "da/JP5/UhckHBsAF6jl5BuQgwsT8BsBu035wYpgMaL7dLpGLKqJzrKujOBmpULKnE8lmTwerrfvPNtcIcmseqdpluAvSbXBjohz2jnMLMmvPULf/"
    "VxcGIDTNuSRq7TQJmHgNSLcsQUAY2V2eWusqWYptfb8qwFt302jER+wDBGsNS1COIeyxlctboub0ON8JCkOSgH/3E8jXBH6JnaMUUvP/mkN5z9nx"
    "CoC36AxxFScGfLHAujX+NzLIsCbAwrdDAUYV64kEQf6lqbUBz5kcBiwYxrHUY5L2TaXZmYljGp/rDGwI3DToVLLEbBBcj7tBYSlxSvFjmoTdCgON"
    "64Dh/t13sXBpQVQsfvZ8m1WUSlyMyZRG78/onrX7+Jd9qKi8nXv64MD57Wwm0eo3uY5AABaXSyjd/twIIFwXAlefD876NzoPAr+VPnu3FV6qGNwr"
    "4m/1okzNzjH3Buhi6DpZ+eBRkmxS9yG9FNiGLhUQAYTcT7EV5gj5nPbNmvU1et/iWYkxHjk3Bd6RkdrPGaDcY61JtCbpdHWY3Y7DfyRTm4IXu6bL"
    "LgP4G4ZWcC0BiNz/+k8U8bgGjL4gTGKCGVQv5yisG77GSqBkFkmICJscdDihzsw/UlhGAtet4voGL/eU35GQhJlzeQRK0KCctiBHSJerDZFrmqHI"
    "SkK5lpIMBnhQAZRcsa549+moNxu9YyriZGl+2FPqH+gdB1QScDeKLbzeBCjxLMLiBvqObYTcj9U87bpSlA6Q7JtG7wQwUAt9B+Mls+3UOiIz86Zt"
    "ZNyPbU+x0TPnkJbGtzZZgQbE5fFxF+pcpTw3CgpXlV02yy1Vhr71OvAuUySC6NhpMycxXncO8z5qUlMbqw8nDINrFXCng72nCgb322SHrkb1iMxx"
    "z21cA8MC1UbEdSvPA2i41peIhJv1/wF85GAUcNGgZUCggvhduplRcQ3orar2BE3RqmtKnBoXOkfzgF3oH3QkWJhQloZp449H7LhMwJ6hK5cUjrQv"
    "nrEGx2/TcZfWPpZIW3sghN8ca2JexNQnn6MFhft/mN05D2uf0BErEB/o4VH5AxAPOloHoyCX/iOea/PFrYFdJ0Gd4l8cRzfR1vqNAoArG4ALpIQr"
    "dopZmLhMDgKF61FNG+qpowbVwNiDvkhPuR05OwcaV7SjOrOU31BBHfLtydoppIBs69vymarqYI8K/FYYBt60jAPkRdwXTpLVNgH+luMTijIkyG4W"
    "eo9Ax/2KBvuHn6aIT5rw4v/mt8WVem+2lYuNivtZeEdK01jNlM4K4Jw74wnVSctyC6znVlxqQm7HimqLpteIuPBYCBE31M0RSDazPtYpAlYd5jKc"
    "LAFfhAuDK+r+D+2mSyMlSlHIGeQq9RlJHZ8OD0iw2VYRdKlSiCvhPD2KDXvLYW4WixLtprNKsYLTEEyNnm6FUeVpAV4VJ4rjj9Kv5NTQhZ6QYDrH"
    "7Kj6UzLvwgERSLfY5GAcOELWOGoxe0SJeYPOmKluNViYZlOivECi0kWLkiALmysqRax9RrLZakC3Va22HKLSvSF8TNJfq+sPzlO5bKcnRp7lGtu5"
    "RioIiSiLcBMDCodF1Y7rIqswrO2frWm9CGSlZt+pNZEu3j9gX4OTZjpKG5DL5SjJOUXSpE2SKeBB4pacU2Gh8aXUSjhsaJeBNvtqZTSRqcaTTH+D"
    "uCl8zny8HNiTRXS2WxavzO4i1h4Km0fXK5FV0gnDisFN5QhIWzHhqXCeKVAbg6zjS/kz7I9CQc2+AqYh6viSjpvrdi0GS9BZ6VqhcIUI1q/BheC7"
    "yd+dtRCL2DtELWT1kYTBaVW8FL1n1agJt5FBGvw7JmpEKsiOuCtVRFCA0H+XpeNQTERJkWByjQmP5+RqrbjURFnUmNT4CmS2ECCaocIQMgdH/MUU"
    "4cJLN4IkpCklLKrkEnGYGSZGruAvqgAdAzf6qLl9XAHOxNVkfMho+dh1SEfVJXB6R/+CZ8T+ElrynDqL/5UAhwzjyP4cYJLdRWDKqptxIe6kdhxJ"
    "D6WhSWtZpWaWKDfi1u5woS5sQVMKmltS6hFYVTv9RZRdu2JcRFlsP/+HFuIiGiqri3ZjjmFAXmlNukanvPscjasbjSuxmOYnfl6lMH3wp9rFU/td"
    "Z5zTYIFTDMDFKqHIZHM+maOEGwG7Ztnfcellt6wynSXSdmdck6SMphW4lfcSaMHKdGdX6lXATrQxaHjfEuzSp5SGhcT/ZtSUjwlz3VxADZaSaeBo"
    "mfIO8EEyiaQZ05gmRIC7gjaa9ngzkdMn3253U8pkNCbCffnaCnIp/6hZupKAeOU0umgI2bAS68EevXiTcxbgyPIF6A4KZxNckpdKKphHSXzzEVRA"
    "Lvu7KilyVmLXzFkbUQ+pNHcU60WgcBJujPLhyUwHuxD/MAJXX/7dZwgYOmyQmvBLgu7E6uUHyj9nSbR4U4NlCDAybCJpIcN+GJ99//RheWItEhi2"
    "3D9buj9QvnHVhoZ9/6S7fGfO+zD+sHT/3m7YsOWhhfLQ7PuVfq808OLD9JhXWhn13q+vwP8i0WHLs/0fLq+XhgbLlxe88nx3qf9qJEJsuXepfP0e"
    "rMz7MNZfujX7Ybw/DA77fvXp+5VZD1YLu4gAhy2tXSrPrZeuznql1bX3q/Ow3Sh02PLcWmn+tvNMBEBs6fkKHKNX7p//0DdngcPqc4o0eEt3F2Cz"
    "H65MwX5h4x6f+B7wYcv9C/AC7qE83l9+sYaLXR8OYMTyQ9HwsOVns+UnU155Zb18ayWaLstTPeXBKbz08stb8HAQD/bD8HCZ9hwlzMrPxssXhnGB"
    "cOelW3NhM7Y0P1h+PVa6Blt4AutfrwT9+n61vzw/DlQxDlfh8eVWBXstPesv9654uPa734cML32fHsxZvnF7fxivfGENwA5rQOiKvGGfshnvw/Q4"
    "76kquGt58kJ5btj76P3TpdIT2CbwS+8arBD+C8PtjvDKyyBSdimqPN0N+9sov5j6MH4PvigNLeyC9lqen4WzLV2FQ4NXxy/TuvYI+KrZszw35ZV+"
    "XMSFTF71ypMr75+sELEqOq8N8ZUfl7N0lmY1cpSfjb1f6T4Q7Kt8BkdeXuiWRRJ53JlDQvkwehVmDhzNoSC+BqeGjXkf+rrLN/rxWvuWQOrBl2sf"
    "ZvqRxnhcPGG1wsW9I77yq3LGHgjuD8OLdUB2lWHLk0ulZ2b08UGPFmkLLVy/HogZYq/4rvpZ67nS7Q3azcQlUHYenJj1iv3dVHnoIbBweWphz1Cv"
    "pReotUCI0d5I3XjlW2vlG0s21qvMdCBg1/L4MMozPJ7S5TE91+z8h6nxox6rZpIC9opChENnWyeo19LoQOnO6/J8T8RMtESY7PJTljyNHhsD5blu"
    "kcoiIvBjkO6TV5HLgNbL8+vlqUXYT1/5xoC8WxEOVgwSptj9476KsYNLm4dd3KZjXBlDLgOLBAllbk1WjfIBVv2hd8FINS1ea0J+ZTMBCbL0ZAyM"
    "HhT3sv3ydH/pR1CYixUhYIGRQLUZvbY7BiyrJFLCa93llRUywfAe1tz70XCw8OX7J/cqg8GGJTHe6AM2FV1EWLb2PDCCWPtXxYMtz1wtra6TAB6c"
    "BwG8jkKDNX4FUFh+FOhPP927BDaXgwxrcY0ifPq0Hw3N62MaJLY8NRhCiVU8Zcn8MFRshM500WLLE+tsZAtgLFtdRxRo7P9zEWPBYIJlCbPYoLFw"
    "YcDrFmosmECwMRc2Vl32YgAzVt3ZYggwtrS8rs0UgxXLZoMx9BVcLFOshReL9t/chgMXq209yzMv3RtD+Xq320WLZbPOYMXq0QQtloVbMC4TkDRu"
    "WArmAELy9EIFN7Y03I2m6NI6k6mCjwXTFwxBQzcGQbbc1wNEZejPxpDVFkwUimxptfv9k9cue+gjsbBkwWwu3XjKV6IgZIGW+LwNgCws7f3jtRCE"
    "LJMmbyaAHwu2fPluTwg8FsYu3/j+SDRaLIz1/vFK0I9wQWPLj/s/DA84xmkUcKyY6oHHItBjgebgWZZ+D4PQseWNbiR48ARxlGuzFnosEtKN713s"
    "WBacBjZWs48BjlX3smhhxoLCL92eikSNtY8iAjxW6YlFGzxWqyGDGaspXIHG8ilaiLHAgKWxMZYQDmosOBEfepY+jC7BQYEasjFjWYRUBI1lJUFy"
    "UemJaOBY0Qj6RDVoLPI/uDTlhe/ZpHSQY+HT0tAif+pCx9rfBIBjWVN6pZ7L7190R4HH8iLU7w5srK0Wd0GOZb5gmtszbKzxpD4MjIFr+v75eunG"
    "oifMsT/YWBRh1xdDmSSWdOI6Hgg2FsMcMpr1AAvwGjBj8XXjhcMTHyYXSiNjNQLHog5CN0+J94PBx8pozDNkoICJODTvzsCSnYwvuq4PE4OOEbNX"
    "SNnS0hoQZrn/MV6VbIFV9n6xZQOMi5YwfEG70AcNL7x/MUwqwvXQGw8FYRZ1BfiToIqMvyixChi1PNf/EVi5vxcXzTlRNH3JlofrsGU6befuIIqH"
    "u5dkLAM+K/6pbcDvhj+rTHnh9any5GB5dqN0b0ViNO9XNyKiGWFE2sDp74JIi0EbxQUjY3uGpCWGIR5uUCEDHNGJ/3haOe0TmpYoko1jTUB4gWDT"
    "oBfhBEjcyWrBqeVIK/HTjUGiVcPWJjq38L0agSNv9QGuVQLXtpXY5jwq/5J5cP0eCQMtnZ3IgRXkck3wuuHZWhMHrBIJ+R4Nr2h+HO7jw41BszY8"
    "Wm0H1gxw65ghVqBRO6PoiXq2eX8QgFt0PjD4bk2K3i/HxJAbb82ihv1wYR7W0v+hf6V0t4eW8+HKOixHLsvEPQNIt7jU0rNBrZsCELeixWxDLRLl"
    "VjGaNVIExq3lyQOfTFuHb8Pcln8YAHbxmMyr4tyyFUARi1srYJIHAG61Ggki3OpECt5UBLpteZpdV2Wx7h/flpjEvjoU2yrUglFEUZgoM0g+43Wq"
    "06aABz0UCAocEP9WSafeBbUcUOi8HIzCr7EIU6ukuIqtNQ4OfesuwITJyq+WSvOXygNTEpsDs2MDzQ6JxPTNwV2KGrKPY/9YuJY0dRMHrC0aguF7"
    "ZqyAnVgfWNyq14BCBdU6+Mpz/R4o0g/ji/jtH0LwAb80Km5gBLk3PMKotaDBEFgJbWh88f2rKY/TFIeKjasv3DykAxy7IOPatsTrqQ8DV8vr84YI"
    "6gOOW2UUIInyrTXiEiIE2/ZylWy9kXGDMkzi28CVJD7IVvECJh4lSIhMkV8xEXtjUC3SsmMlxMHmDhACiwI7+N+4J+Bc/W3pyaAoF1y9MbA5DRDy"
    "Tw4LPFeMtlDEn/IEdK68Hu1pmGFLU3S8wbKh8tRTkI94VswteFaTS8pLCBxcrTC7wRtWV8tqMLD6KIW0B7DdEtDsdTTUyK6Vb+lq5oCS16ykYkDK"
    "7wt2lzN2xDUzw0igY8OgYcvXV6zHlHpRyodOg+RYxCr2icNbfjoLhpxXvj6GkcPys3vlW4/JUVHlErWA8KqjUdrKGDC/IfTd0ot+VQhCYTfQsWsX"
    "WarObZRWpjyM8Pz4gkK0qsKgH9UxuseP18ursGew3HunyBt6Mvhhah2FDzxLZvHqU5ROhp/EVXaGEqVKAuLybbrujdny/DoJKeCs0vhw6S5c1vot"
    "9BnG5zlZcUN83wbOPAEZ3+0WRsEl31xChWwSObtKv38bFN/IG21wr5MrMeQSwhEkPMTS6DS8wjbPLBC4sCVfMd5taWUGb2C5GzimQW5HK6FZFFZX"
    "1RI4tbRGt39tge70/mLp+6uW6YTJTPGedDaO41iku0AaXh9zIkD7h+x1mb+0vG74vzTYX5ojU59969oQey2LmSlZp7KjwXpxN4OWk1QFn1epZBFU"
    "snJa777RedWYFWRg5d3sFZjXWa64yEesh1UpkImc7AeQV7uVKCS0m08RIefwMIswtLQPMF4gOCxlKQ0tAsdYYLzIBPo5DGmI3Vyiqj6rcqJ/HZbQ"
    "WBGVF1MM67dEVkVD8qq8tMo714zFKyU7yNbzFMHSAUnhNhWwXLfss2irrHZkXrCA8LJJYAQ8SpuiSCwHM+VwXLvr9/pC9EYxQoMVyxMClVkkJq3T"
    "yERoFCtQJ8gykIoj1ktjFJgLyK+DofY6Zjr1vKqwUO/akd0s1npi9+62kIiRUO8EB6oK3ovaCUwEjE1gkYkysqW8h2No0X0xlocWThPuCcVXCOT9"
    "0yXKgVwfwyDg5FXLpmDipWvHWVdMJK2+cL6gWP8/FZMAg3NolrZHzC10CTZ7aehFJDPPDZNzL66JpUp/LQi+aBGAfVG+u66DYUxamHADDwWNDonE"
    "aINS9iv0Afpb4jVkdk5R5QLF7MWqMc66EtY0INwhCSr46c6SVF1hKBYNGbAXNWPrU9dmpC2sfoMQv8E4ARERZRiFgLrdODqqDCvYL8GGvp4PfbMR"
    "tbSNbjQzHLmYW0MXAM91CO4PdNCT1zAD3uSHC0/J/XTJmcgXrowtxtfgOKK0Bb2vpW3pqkXYBwH/Rab/YcCeWWzVKbFwkRE9LjOgkHcgSH1w8F9z"
    "8MER8DDfP+9GAsdjpfIqstRDoSjrMH5DKMAfmapliq/I2f8+uNiPosMx5nFcnTguBqpSYjZs/5TnXhOR250V758MI5MvbTS4n6vtlMdWlHY1po1s"
    "SGJJ1AdRP6RglZxe0wLQEm3aVEHrBUwVZzoTefvo/UoP/M/Dsv7ZeU6K8Tntih/sKmGsQL3b75k16cLBuiIJOxkPonOsSBxWogLTIMB2Zko2LaJx"
    "fOsBJCzWjhh+wOphg6eWpdQFUnh3SQqOtwRxRZKyJEZKtVdQZ2hhZS3/8f/ZBIgK3RgkkYLLVUNRqqQa7nBEtDtUcxpwLP7dkYd3yRIE6m96p6LC"
    "yrtnDILlLShKrcDRje/LkwPci9RPOtJJMFgtL2FzKnAWzFGVzkK7Ouo8KoTl9QlZ3rpYGIaZKyc+Dh2+mJnW6B+QK/Plu5YPbTnyaioVLgc9NrGm"
    "2gLgyikyCjw/P06F7WpIUnZgVWBZ6XA3lvDK+xKys9jtMBCO6xSPsGCPVVxyZfb9OvWw8CI40+CFC6F3B0EGmi2NrHBnA3kTIlH71y2zYR500ZJU"
    "YFSDQ5a3cBdkIMpyMVGpykYr4yEH2cs6NwzeXhgBBlorzS9wpHy4KlSyFI9SdYy9oRpBklUdLAh37iTjvIeMEIWNzKZxabXfOMMRoMimBZZniMBF"
    "dopTkNC5djWIjvxheJGcERI6keDI0sz54ftZis8pqyUKHlkS0yNjpqkzGhzZdMlKrh0J+Fl3FUhkq4RAtd7uGQrZqpI8ZDhkVYgRHJATCPMiXngI"
    "bmU0PiROyJUbRP9U5mvHwFxoZNNxKtzXv1J/YGThAlMkCMuUYY/oaEPvQoO+TSwwmVrnchMyfqmXyd7FXqCQLdfZKiTpxxYds5Dd4I/Z3T4g/DEP"
    "Qp62zlXrqoVQ42EITtg0IO4bELn6CkQXV5+7bujIrD2s9z6MXiIrkuStqbg/MB4y0tPJ05QIW16H7f6KMZGDeMGmhoIisVMLmCxHc2ndlD2i0TSh"
    "i5LtwBHpLO4DjLL2/u+XJs1PpiNxJ3dImmRCmFLUCHsFUsa19i6ZPt49Yidr3VErenLA4N4zfnKwZOX9k9cgLGuATg51aWsog18PTnJUX2xg2Uhy"
    "NaxAGZEgY7GKc4qs4KhZKQe9MvVhWtUdi72ISTiwQ9BxuL5S7sfOSWXxiSOhDeTKwMlc1kBcMj5efjZO1t78rEkFWriHFLXmuLf3oWetdOchOseP"
    "V9Alk4p2GJJ8kufrGI6i/fUMIwuVLlyDxakxLQBlk3qzAZTddm6dlIxGT0YPyUFPFh8LfcL+ldL6mOkjikrQU7AGE7N9pVE4y/4FLoyTjWGG9Poa"
    "RnqvzUYwcwSqclThbqj3NODiV0Vc5pbl19b5EWavNkJY17MXuIZ7MBdL0Vc1Ny+kj9wqjE9Nm/mtgi59kRLh/oilGt6lcTqtW53r10UuakfRKMx4"
    "LjwsrqdR3ZJY+GZC2u6NgdL8bX33BngZbHTcoTyJ9LUyQ30GmAGhkLJCXtaFTkS2qi9WqXLkEmoQCqAu//G/yMaZ8v7rP/HVO0sRq2nEMEFp5TEF"
    "r1/DWPO29z4fOg4XevnD6BrY6kha7i1aYUN0NOZnAzylGs0tdlDAxuJwK6+DSuWR/4CQAwjMUS0aztumXNsVCGQH9i7BetQr2GQ7FVGYaXABkA9e"
    "rX24tghcaLAB6DrGVkp3BlwO0pvRWQzeiD5RF34AB195TemfJytwE5xxeyrL0kdkQzaXny8SgI1bmSf7Z7dXdStFc6mGcpYpURYbdilPXcDlRKE5"
    "C6lXBnGmAJO0ONgFaIgfY01GFOsEPsIQzqbAz24GV+DNpaEHqCTmF0r31hi8WXKRpdtr5tQEnjnYTuGCNzvfInqz6b0Tk+XDhaew8gBQs5vSuD5W"
    "fvKQiIsqjOgWqKrBuQWlZPTTPIGtJeYtXADCa3bAJGxsZnXf/XLfVQgs2DmjMyimBAyIioI5tFoMguhDtICbOQwhqz6iE7mhYHKDZCoawnW/cKsv"
    "8HdmpPnSDyuWqCE5Sh6tMUMUbDMdEhlSlgBT2SuJsQpsM0pWpR3RHtFZJHVkmK5G+UsbH5yig7eIMQLBWeVc0Mxei1645CXFag7rbOZsNS2X8ql9"
    "SERUITuLbIUXLLRm5EuM3n1/VchIj+xxsgiP1LVyTCRW32YEvDMDYdCFcIep1JQKt4tfEKE/LKTn6BMhqkDqm+lTUCpMzXAICCzlLFGHfXH+0jXO"
    "e0tKwRba2NU1NwX6z/o2iMui8KBZ04cQobVs0UUH0lnC0p7pWpsJa0afRWzSVeH6Sl2IaEu8qlG7pcnJYjlzAhYaCzWvkYrm0H5pQLXvhhQbk42J"
    "emrN48bUNYY0pYa0VBYadDMYfOp2W+cCndxAsIGBxJ5gqqiMx8RaaWIhUJVl1bZziUgD1cfeWcLkqqkFtV7ql+ineA2llXulJ9SHXbUwJIxBbRrP"
    "iGW0EgcaQA0jnkvFEqZAYlqMFAwu6Cy/MEwgu6/B6gTJR3KETvEC3e/kCuZxhmY/9D61HJ5aEaoNWlAYcE01dVlVHlgNfG3eMoWd3C9ZyaNL79f6"
    "ncYMJz0E9tf8C7xjh4uxE8OpD4ruy3BxBwKL6fYqo8chKfZOYQwevlS4Arw7p+mWkzFMgZqRS3MbqBs0GArJcnqD1NqLRTiBYG2RBtajRL4p0aEY"
    "denqPNbK6/XytKZc9bKJobOInu5mp1JCvIb0pTkb2F0sXvvsLN3kYl7/MoIsutjP5L9BFoN4AMaEX94/GdaZmhAP2WKG0yqodIIFZxzjdhhBbklA"
    "28j7VYIE7rCBz9SqybPLqdZU3z+utPchyUrtFQ93Y9jAsZS5Zk9JBbuax0FrVOdLTo+SeE5ftNC/1AKohjkkAcdZYrwoXeSk8rSKrznbQduY7wEm"
    "s+SdNGM4ozm0bd4N0raNTfRqofSkH4vwTDcH5YUEIlOJJyU6Zc1wtlQSRi6k1fWhuDMi4mgnoQktzsbPoB4H+Oy/u6fU9FZw+r+7p8VQ5VSSYjV1"
    "obNuJwV/DO8Ol+5sBJocbEiLSGDtGsS4S8RYl7pbDSjqlcml8sKIOgxtusJwgdorPG6DYif2eS22clgUK+ELBBKs5OKJD9BbZxBhDZCH0m9Tdsli"
    "QAhoO5iElsr0kGQPlZqafi+awmn5FKFVvr7SEHH+9Lx1Q2R9TI2roEnwenqnwFUp9Vk2pAUUhqLfoa8PU/3wusfIqNGEWakQw+6aEs+Yh6G9qdSs"
    "GtPs36HouTVNzpHWTxTubSQEmPb/1Oot3B1ugMSlIWSECf1ZUYcj6uCd7B6rYwoE3VjCrHkvMjNpOTFSKjU5egac111GEGhEzxKCHCHipQCDtgIE"
    "02xWw3b0i+0YLmp2ZlCPa34PWVGqm46ontgWFAp7qJpt7EiIWYm9u9LQYnlwlnA5qEyEqmvNW9UALcnmIVL/SDJZv2c2tNYllbSuMSdP2OA5ljGo"
    "tje3VtmEi8Bl1qhhUtui4VI0NojEMQRfTUK4DkiJ1Ahp8jZkY4luhA3Pnf/Dn320RDR2ePFFz86Dsa31h4WJi5Hw4cWV18XXT7a7B2z48ML9Hwo3"
    "b+/MDxRnHu2GHp4fWS1M9+4M92//+Hp78OL2j3PF148iccO37wxtP7xUmLy9fX84EjA83z209fJl4f5Y4dZgGCk8P7C0M0EjTF2JAArPL1/Ir/Tk"
    "5x/nv78chRBeePg8P/qkuNYNS9VPRWCEw96370zkpxd3etbhBCyUcH0ekU5HYX0gP/EIjjN/dWQP2OCFS92F0dHttyvF6/35h1Ow+QAu+Pb9+7Lh"
    "MC741psLhZdX86N929190eRXuAa7niiMPStcux6EBC9cWcyvXKkgGvPPnxTXHxXWZ2Bd24tTcGhh858/3xkdrIQGnl9fLQw+K1x+sDP7pCoKeH7w"
    "QmH8x/zGaHHkCaw3ZFnyheVHVooP5veHAc4kzdez2d2zMzNbeHE5372RH71sb6MqAPjW+ghcUX528eeNwe3By8VLg/nh5fzFlz9vXNoV/BtYgycX"
    "OplZLy7d2QXluzB7vzB6devNzJ6xvWG2Qu8iXF1h/kXhwvfANLC9wpXb8Imm0NpQvXEN1tH9vHF9+8FQ4fmr/OV589hB4LwLg/e3L67KVz9vDMsp"
    "0aJh8u0fHhT+ubBz+TmcuXqNz7tuON7OjBMbapXWzMOF6evwDcq5iWuFwVWgmNByaoHv5vH4PPMLjwvjk3CeB0bv1lfEwxeHugsDQ7A+FIckUVD8"
    "P/lnYfaSHoWXvBfU7vybge3p8eLVC7Di/M3n27eG7Tfw3vqf5d8MW1/pwpG94XQzhxWWx4qXXuRf/Mjy/ueNGR7ZGXj/EN1wZMWbt3nsnVs38jfg"
    "vGbgw517k/Ah8o2a377zOqFxF/tvFUcWi8BGDj1d519B/G1fvL+9erEwMQ1ye2fmAihnXBF8e3Vqs7u3IsY2L57pav8Q28wN+ZWL+f4ncBcw89br"
    "kfxAX/FpP0qVhwuFK7dgUaAg4audi9/vfL9SfNaTf3Sdl7YrqjZcLmhWeL643J+fhZHv5h8NFwavVkTS3ulbBPUAx5J/M1kTkDZKDRLpW69ebb0e"
    "377bnV++WZi9CYfLa2T4bPh1h3ClK8Bn4zD0an4QlXNhfD3/cDKEnM32Dgv13YCz81du5u8OFS53b9+6VlxbKS53V8DLDjxiQLKZbhU4dv7qHQ2L"
    "XZhaDsFia8EQBsPWqsWFwN6+f2N7sdtAYLOBAbSpQLBBVLsw2Nvdk0CZNv417nLGxr/eXhyEw3Pxr8G80FaFjX+NZscPL7fvj4Twr3Hr6huDf50f"
    "frEzMMJ2msK+3um5VxxbZPKyELC1XWkQsPUSLMd2e/FyoWfZhb9mO8bAX+uhBP6aRUgwehIQHVZ8qfDs6fa1Ib1Cgb7OL9zNr4zmlx9YuNf53unt"
    "xVcO4PX2vVWgDBAQsNIA3rXW7VF410jPjy4XZtZsi87CuS7O9hTHb1sg14XF6Z1bww7INex669Wz4vPF7embLs61CJ/pxTDONUiO4ouxEM51cexx"
    "NMY1iuVr17Ux7IJbb/dczi/cyz9aYNMrCtiab0t/H4FoXbz7auvlQuH7qe07PUFAa9zim6HC3FsLyRr8DmBcF8laSy1BsubbdpCskcjpxC0k653h"
    "5e37C5FI1kxVERjWMA4LYxvDWst5g2GtyVRhWOvDsmCs8/f/CR5hEMNaPL5XN2z0aub+iujVLJjZw6iIXM0iVB+gBq4uXH+Q75kFy8RBrMad9swW"
    "Hv4QQqwmF/Z5GK4a3oDPi8+vR0FVw5c8cyRatbnBqlDVQtnPb+cHnu8HrJqZ0rzA5L1PlGow4grjg6FsEZOOdmoOhFPtgRsupGg9wIK2Bpxqr/jw"
    "AosXWi/JkBpBqr38pYssfg8GT407ECEA9LQCNsYzHpYl7k73E7AktazcKw41ks34Gv7E2nK/6NOa5TBqwgeG3wOhg4DGZzztJNYfZ5pjMRhtMQ5P"
    "cXYITJ2tlxeKS0ue3CTHS4wHNLvEchUNotluMPi31rutxwZlCvAv2NTaDUwaOZT4a2t9DM6BPXy97zBotD606nDR8L+tV7fBt8+P3skvTNC3bCTs"
    "HTZaL1Gz12Z3j1jJo5c5bHAAwGg9PFuHTAm2n14rPjQH1oB88gOP0ddzeBEdtPXXYInp9+GrusFDo21Gy0WXAIz70QmOlYFTxT+Qlf8CLxjsOz46"
    "Uu/MiuBsAZfWEwmapym+fiIGyywq9PDi0KEhSVd88gaMS5ZxtnlUM/yzuUXelyIVnIGcOAwokrN0QOTnnYtzKNHYk2CpT2eYX76HQZrle7BFmHSn"
    "59H22Gv22MP4zrwSDGcpqR5AeOaRbfslEuCZr9IeJwLfWVsvGOFcGdm+95ilRQDgeae7G+TK1qsfiz9sVMV3Zv2JAuiHObjbALwzS+dC990gvLMO"
    "dOtrCAI8g6AAk0bbcfvHdwb/XV867fiJfVNyaK9ug3kFbKm/ZR5Bx2zmDR87i9AD4jrzdLzp/MhqsfclrA3ODU6icKl76+1ccXwaD1OFGvjJ6Kn3"
    "Dupszw4uKjj/mlOQHF5Pw2VxZGen50pxcQjF16uXxQdD8C2vYf84ziJK3ZAvyGv4mf11EN9hw6k+wM3OKHDLO7eWiwvm5APHDnRSGL5YXBv6H0Fr"
    "hksJjsJXAqyABPpgqHD1IbB3NJYWCJvgykCy6hX8vHG93nDNtlJTT2mbdXfIZiYI1EXEcPbd1wevWd9peBT0wQcvmtunSw8owXojNWPIjqmcohSw"
    "hPzwQP7qA7YXtEGF6vDBELMmi1idqasdalnsWPdBy8QEiuL47qHgK/PQyswlmrBCMDqSDNvcev22OLZohisMToQKP/ha+ED2AJsMxx2Iutt6RUeD"
    "agJHLj67pn/1OPqFvgG/i3k9EJ424e4NBhk0D9Lp1cEIwfz89tbr2cLTHhDJ1kvonLBogGf2j3uMPvurt9vPVsGF2Hp9ZftOT+FxLzlUiw/zj67D"
    "2dUCfKxDhWwsB5T7bwj8uHi3BxwxjtWgbrp3E2QHfALqCbyr7cGl4puF4tN+MOuBZvNXyeXCXxfZx+VoHChLoDz+Od83sN33Gq50s3tYP2ZnFDa7"
    "R/KXb8IzGB0Zv4mkyabJ08fgIlAqZEm5E3eK/bdgZBAe/K0dSP/3gCqudP7ws33+7FAC08B5wiFjkublA3IWMLTAEoVvJ/9yND84iWRJ1wFqKj8z"
    "j2J4fWnn4ujObDdQPD7Wrby93pcskrfWL2+/XYErw9AaaSdwi9EivPLPnekFSWeomB6OT/EMvov9IxHjBJHsWNx4mV94jCnKGuCHbfHBtGZbdxVR"
    "iPNvB3BCZcpXASEWpWStUcuRfYMQ6xHCgzu+ud6T6Ha1p71iEUdKPrSxiA4K4+vWi0AVBwEkBiEgiWblEXH88P5Oz1h+cMV4UdZK9gFLvLUONnt3"
    "4eFtzAtfGCks3ZIUsHkTZAgYOiDYrRcroRDbybpoEGJ+Aklz9Me9YBBzuEpHr+TEHdNk69WItk5qxxkGxgY/W+famEtBc4NmklyyRTOgT0E6/EKQ"
    "wrtSG5CCTXAPL2DVwMBjO0b088YlZIQ3w8WX8h7LL875HgxCGE7atjSpF4hNVbAzgJ6qmWf1RBDefR0RYwV9olpghPMDz/O905z8l9Q5urnD8gqo"
    "5YqtBcZnsDM1ewIQ3t4Yy1++p10nDNs8XqKgrqEOnZOsL2JwcWlpa/1SYeIFW2wYT77ULVlQUGNclDe7CB+C/mNLGXaIIbnlO8ySrOR+LRjB+dE7"
    "KPUuX5ZbHFuEc4QrQsufaGhn/iHocFj09v2VwnAPeAFobdPDaA6MLu90j+70XMFbfXQLbA1dS1G4cjcPxhpdUv7NZPHmbY4RCe91/wgmRn7gGXuO"
    "sIat1095Xj6g3yD4LxeAabLGANXDH7SExsD19QvoNJOBFQimst2PXEGnzqVPnD6A89jpnt56OSNn2TeABKYCMHz8cJBbrybgBnZ6riFNTmxwmYnx"
    "4V4M5S+NoKdBdYkYq7MngnlBy66CMTdEJD1SmO3b/uGBXQ9zEPDfrTcXwMrUvIO2KbGMnXnR+YJA9PLgwL9VwhhcXsgFJDqMobM2vyGIXyPFRdPk"
    "R/tAL8JJBxarn3NjBPrx/JsbvMLtR91AKEi+lGHbfrJRmLhovc3Yjfo9fip/Y0hvAav2RlBIgNIDK0Lbn2ojugC6fri+nAnUGsZW/1JIRTlJTAv+"
    "kT6kek3HbBguLI9iHvD6BQx4DDzLrwyCctHeeHVgXw6TFK6hmLRf1KcIq6s3rq8ZTF9OxHAoq5Wwza+MFC5e0oIarNqduRvh5E49QH53N0hqWXy9"
    "YH5ZboLPEBCLeDjgILEkJYW4M/8KJCk/fCgAv0yCIfpTqiLCeA2KKq1mTAF2BThfXSJnW1z/7oC9eMU/XsPK//tjHC+m7B7Fi9UxgGAKVq6GFBKq"
    "TNKCcFcSFKGQYn6kG7naIm6gaDSTrJisvZn86GW9GRCXwd2wYxBiBiVmQYFKQPveE4uJWDMfOo4ucwNrADZRwK/lWCuvCqPhoDdMZZDSHT9vzIDo"
    "x+jRxjIeFw0BF7G9CBR+G60WOrRDQsetwVNWbRAzbKKY1z3SE3fyVwdlosLidOHlhNQvW/Hv3QFwCzNrhYmVfO/qDqhXqkthIYPFPURLO9evFB49"
    "3Q361n52p+ehmElUKV8V9RalXoisOUiA5Q5PrxbmblaFuuXKM3gDjTMyNKOXXRXw1o6H4Gn8cENH5/U4UbC3W2/muHqPg7Z2TUME/C33cPFcEdC3"
    "3DrF1BkBebsz90Nh7m3h2ggsKhLxtth/ixcDxFB8vFAB7FYEx/SiriiMxrrFVAX3elFEJT9wtwrMrdbP2myqBqv4f6JQblVt1iFD3Oo8dXBEiTuD"
    "HJ15iUE0HkU39qDBhhPujA7m5y7q+kAX1Zb7pziECWrSANpyI0gdIG3z4zfzQ+PaG1EosqAcWA+IWyzFBXJ36Natvyrcu7lHAFtT3qOvt+cJXK81"
    "8W7wtezBHQC+Vgf8rOHQAgl03ARBXvnA9wVXW2FGbRhWnbFuILV48NMbpA7kVQpQjG9tSOCmjji15PbPFm4/LK6+AkFWmJrP943WWFHwP4JWa6We"
    "gzNTMmHmh+Lz66rg8Y62kAJeBCbgKKgMKp9vfHt6pnBtCTNTKvuKgeSNUa6V2hPmbLD7bBfMWYeobCTwWjFnrQKD63uEm3Wz93e4ZXc3qFm7m093"
    "xv56UGbtPaFkH3jmLPh7qqLsfVnLEpBMLl7K99/PDwzu9KxjdGy2Lz9zA0ymyNnRNitcGSwsXQZCKtwdqoAdC6Y4p4y27/7IvgCazphfHgbP/t7W"
    "+pAFqcZxCuwWo4pENrKHJgozq2Cy5R/1ba1fBvMAXsbCDAsb1lQSOOCwUvKlsWA51+DZkLBUcGRjwsoSRpcLY7PAEroRBcZC/oEjeXRp+8c5eAaW"
    "vr1xiRM0nF7l+QIor/mV67oVEP0h1UbJDwfwXLFmZuIx2Eaei+yK4UcagbFAWQHDeorUYyqDY/nGkJyuA9VqnSaabs+X82++R+UyugxHzQKfTxmF"
    "x8MFEPHco2WQWeGyGATS0xvB4fiwtjfW0Y9Q5nRwnusak5Wde05YcJiUA6QmXE2hEdRCer6tt3OF4R5dkaH7tpTCkqUaYFY4Ql6Q91//SaX7Iz35"
    "gYc73U+w8fDhZH6gD9s/B3q2Fx8X770szGPPdv7CP7nowQFgxcvoWS9cu1gcfQNSC01lfZCopbqHd+ZuSHJ64Q06j9bl8GAKq1TibpyZUBWsvHIL"
    "dHWnexocOi5/5kC0/Z6mQBHiip8wmwZLuwQvLiFfkUhgTwoLL+7dtHs9bQBVLMVYHZdqWjUFHt/Cxe0fX6POuDNRvD8p4TpwUW7MSlemhZWKuxmd"
    "KDwb1CSKJWHUC8MPayxUHkGm631ps/hkD9paEYCowo30DvJ8ZWBUFAoDg/lLI3qtcFIchOR1hAFQw0Rl4Z9aFD85uzNxScXf42orczd1dbELd2qX"
    "Hnv/CxPZKmUuyqv7OnABjPcfFHtTcKeYreKkmapF1pUUEr7l6+JaSvthGhXG+yOMZ3ftypKlVUxep5vhp/i280NvUQpYkgmvHe5HVSuINDEgpex+"
    "8rS4PWqKCGcUdTwaThhrYy1VVZgdyQ/hwyCCtt7e0t6HrGi0D4SgoJLCRzq8vtMr6WKFQwqcrALd0lQxP8jL4QokYUIbbXR76LYYIawGuCQ1/+YG"
    "L0VhYOAYLJwiVQGqqIFnGk7UCIGxN0imFqgo0DZfn5T0POoDvsw/f4wEbx5T4ZcQdKiWZlxjzLzInUJcDoQjE6nxEAouVEfAWBDYm9Nihbeyc31x"
    "Z7pfS5B83wAGKSdebL15yyPwwArwk9VFCPATZaWEbnEmR7orNguJeUwaw23C4dvkx28pptUIn7gj0gW24BBnZWT70WW+FW7JYHWMgp1iGxxwYSkC"
    "6lJLTn1tGIFemJBLUOCdWADHgoQQVbZeXoBPtl69lh4PS+RKAJKZlmvBBydRBry8gEUTDHgBYokMdNUuMiwtRXd6sQzrx9n8wABXSAWelHsNoW2C"
    "J//j9i2TwrSDYhhKq8KP0s6O0xtsTdRfwTQVAb1gYB4EBHncWOdsZQZNanIPOJpioVLuEQ+VDowPlUjijs6m6mJqPq1AUwFmUJZHdam23Q5RJQQM"
    "tLf1aoHFvU6i8xkHmiCtsfNzFwOIK2hw0h2rIAF2Ner1cjoAi4OHpIJHiGZ6ozh2k9sx8FgvXUSDcuXK9sU1/S5adZRvDiPkcFZMIluzEtmikOAF"
    "GMc+AJjaVEzhdypuzS9jyES5CkiDA88wDDbSnb+FHQ0sZMBcKr4W6nMxMQ+J16MrVVipY9y250bx6R0plZh4YVM2Clg8x4u6WoKDW5j4uvcEA8yD"
    "r5AkQPRTWTyztbqk4fzIKjASNlRQ7QC10FQsH8CzwijuHUaTKd59tTO9gDmMmbeF0Rm1ExttCGs8ySSkyK0STAPPbKwmXjgOP3exOPZYKJrJ/PI8"
    "M4pu8OV4ZWFxmtIlSGMCaESDB2nMehgDs3BOaByorIVBEdjsHt6+c0EDCWBRrxJiDnAFy5hHTyWQSCJ0+59Xpe8E7BLdckhFdWiRqswMWobAMaNv"
    "dJ2rVBiDNh2chLOGNdg4GbAGtNUH78MR61eoq1fVudJXYFAVyQCqCDhZUbYBBXMoF4gB7DzNWkw2kXVDEfX+nH+H02DXRtjCgkvSmSMtblnS6YGi"
    "6gDMS+7SeaMGEUw6by0G0P2emo617hPnC9ibIqXgUDNjSDOlqoDnMeWcQ3yi5QhnlvWT+shQJtGpAZGAU1NcfJR//QOYUHbxlQWSgaJW9WoDA8BL"
    "xfFnaMpfGkSL5PtBIBkkhMo5P3id65aQWjf6CpP38AzodaNprbQE03KYfKKwy7jZCiVBCPKCEtZozbOJz9eFJrGlu/CZiyOFiRVMnDyapIsfE9Gr"
    "XteGNnaOrtyChYuOJiVut/IaFaPumCkJE2NTV1AgEe6GFjXk6z5TzYB9LLepVcO0lIp/wrLT6h7CeyCCKDwEA/MlODBIK9YUuhYKPuRkYnH9NVWi"
    "9Hqa0Jyw2+BFMUG4/JlsAJ7eEoIzRsGorzh9aFp859dhfSLCwjB1DErBZe7SMQz+B2lL9ox0qRVWWKmuXS5/UyUqd1iVkW0Dxk1byoJB/NgHK8H3"
    "vsRWmkwkDuKpWDv6HOB4nPPbbSzE07E2P0EfVYVB/AoeavPbCTkglYGvm32qa/bb0/FINMS/SA2en0jFI9EQT9GPXhKRDcJoiB9nEum453f5bRFY"
    "iF/4HfgagvHFzsVao+AQ1SOpWIvf6Z+PxkI8FW+Nn6d9tPkdfqeFhYj//gG7AirBIZ4xp2lg8GwheFo2HgWKeKwzEW/ysj4eYxzTDu3n+ApsYMQv"
    "Y+3WNxHoiF9lWjIJ3CI1l0QT3hkaoMPH5HEqng5CJAJVZFpj52mGKEnzVSyRbFYLxUpb3D4vKGAJfgWE4MdpHnilEmDiKcQVa/bxzIGeMu1VQRNP"
    "xTqTtDgPj+hc/HzIkFGX3BbDJ+L7Q04kBvDS5j6lARcJvDO4q6r4iel4M4x03m+Od3ofxRIpWmprrCl+Htimzf/9riCKbXDlHXA3/JkmELO0+C6I"
    "irwCZIvONHL1noEVrbnU9PEEVRh3+M2+5HbhkZrxFe0B1eqwHSKR8o/Aobc1+efrg7OYireANImargk+aCVGieGhpCNeryPaYngd1groENVYKIk6"
    "sOPc74ALB/HtLKgWvMUUy26UXzSFj10k5/xW66H9gi5aQwauzfsoHcdt6Jeb4ak2eBdk2u/3iLoIBA+65FzmiNeCU+FenDcSsbYM1rAfBHARZA4Y"
    "dSRz1IvEokfdOeuAupiGI4K70NOpg0sA3Z3PxI96fHD6vtUYwmjwEovWeoAwnnGnaoo1+fA6/QwH2tYENNrsd8aJIFvg+nDZmbaOTGtjRfzFU5+e"
    "+NOnp4/9+dgJ70/H/nTsi/1jMDrKEyYmEdPkx9P6KOJtqLNE6iQy7WfjZoVwOPHGWqAY8YOUHxcCTSWSHahJOlDpV0RjxFnoeHw2DVJwcOdB+aiL"
    "2QWbkY8d7IaOJLbAtsU6z8OzJARIhcAFN2qERjCR2PapgNB4ItnWlOzkM7GYEEdU5oIN1XgaTDzQgpZVVhWt8eNMOt5JyjXRDuPBQaT81gqAjcFn"
    "HdBG3jNIotYMqDcF3ngGF6zhG7/1Q+iNZ1yxEsZwPBNQZi6UI5u8BsrxuFCzQnL8uj2dSbhYjmfoWmwsx9Nwu00WlOPH8VZlIFtgjsfjSv3bUI7H"
    "DcO6SI563eprA+d4ChbYzvac0OhpoEoLxBHh7xwIx69kZss5hR9jLS6A4zExpgS/UUYR9Ma/xNrjqWAk4hORDG7I5Yt4RybN/gFjNn4eS1lojfCv"
    "72A1Cl0EYBrPOJ5GFFajZVcyYQP5Z5rITLcQG8+AGjlH1NtJmtLCbjzjt9DtGujGz457vFgLtPEUMqAQVwC0kX9N+eycOMCNx4HxU3HS12h/RoM4"
    "sgnfhF5KCMPxUzH9UqhDicFDGI7qEWUFR4A4nooRm6Pcy8L9nNfXoqEcT5Fhz7tWUI5fZlp9F8jxixi5AAbJ8Uu5do2GdBx5EI+fplBIjl+B1ExH"
    "Ajny3sM4jsdFbtswjn9Ce8RBcVS0qkAcwcxvyqAmtkAc+d8AhiPcfTzh6Tu13CLkI+UERWM5Gl/CEejRmI6ntNSGIdv4QDWw45kYUk46Q/dqkB0/"
    "hndiLHVdYMcz5osAtCN8A9yWQci7tqaMcEsI4/F4HFeAhBCF8XiaVVwlkEdl+3j62/0gPLIvrp+PcEv2ifaYIo53sxx/Rt/rryzA9gnyiMTnCfyc"
    "SFxrSbsBPJKsx2/Q+mj1a8V2bEOpfDBcRxIG+GSbHayJey1AAGmZAIg/lvD3AesIlHYe/23iUNE+QR3TxIMdhgeBn1Dr4r/nSVyzq4xvafsSXz0M"
    "kEcKscCJoKWWVvPCcJFeFn+NcYLEeTh/5Z4DK4HfxWP+vrEGREel171ma/PNMbFlVRwijOwYPrmqCI80PH7UCrJqX7iO/KjjiNoRDbSr2shC2ye4"
    "I7xiD55APB59zmhLKkFhDLxaoR75ORzH0JA8y7Z8Cz9ZL3xHFQeErXT49q6OenDTzSSbedhmWg05jXLnPhsCaKPaVk/doB5B38nqtLqPksBHNYF3"
    "+NqNilzrXmAfSRjzDpF4go6YoaGDQD7CeH4HcFW7xJTB3GlPSfCW4xtpVMjNYLHyUnTAMwD7+HmMjMkOEfm02jD2I2kHY29GAj8GRgpcbRgD8gz+"
    "koBfXAc2AAH5eRIb+1szFGmuDAB5OgtuXNrLoAOjLUwbA1L9HA9iQH6u7sdZbxAHEu0/D1dB3+4fBpLNQBSgjg1PIfeERSWONmvP+o0HB33kjdri"
    "B0w+mDpIoG44AS1A/BIotC1yFXvHfwwvJB3DhTTHwaZNi7TqgI9AALaj0E/AIlBrOTGfxgPhQNqzkxBoMFKelYC8TPx13rKvDgELUokajDy1gPCu"
    "7TL+R3AhI2eU5QfnZGa0L9Kdf29z7xEQUi5VP8CXtwsMJMeh9Y1rPVY3GEhzsaFRTOSdQsGWBtJkEZST9UaFpKCH6AsjotpisGAQQXG7J5qNiaOe"
    "2HX8qxa8tYNDsgJ2n+vKtGSabYP0UIAh1Yi0ZhP0lTC3ituz62AoXEYE0ZGJQB+qFQ8yENNmvWLnBPD4awWEPJVBGDd8n552hCRLDP3wPkEhlfxt"
    "juvov6y1lSKciVhnix+Y2Bpg35iQ6uHmOByVHzcv1AIFmQjrdTu++BvCgtTBHvqsCQiU1ivWJUoTnD7OKYvORLL9HNxVCsQc7p7C4eRmdQKTwPjk"
    "MMOqkdSBq2EkJJHmeCaRARXR4WMY3yig0JuYCQGG+WsCDX1h+yhZIeH8VKwZbPFEnPX1vwc25GkOUbq30RC8imY6Ogw/8LnF4T5SmObrjFP+hvNJ"
    "fD/GZct0YiyZeQn25DeA5G8WgyCR4YuEC2nlIgbMzgjbqUwJXhfWL2Ta4sAI4Axk6JbZS5PgqnonETuLEABiTO0fLFI9b/It7ZnzxK7nKTdg3qoG"
    "FvkXJVsizb2KYJFi+Ru/mc6mOmyk+urrE2e+/tz7+OvPz3zmHf/s1Kcnvv7zZ/vGjYwaVF76y7Evjp3wPj/5xaefn+aZvjr2+def7QMs0n5erdg7"
    "/emfPzvxpz8dg3c/P2m/evzYV58dBC9SvQBTHPvzsb8cs1+xt3nms+PHPrdPcK+IkV9QyQ2KC9CemRRQrJXdNm+nQBe3xim8o1Ty7vCRZ0KJxWgQ"
    "Sc4sBp6rGUoyECoTclQRM8uk6QA+bjWGTe2Ykmw0tIKkqMQjjoKOozMa/4VQJbUEEEdOJEAwvqmnCYWoYDJ+RlcvWHKuQ9LdfvvBsCXtOJjYfe5b"
    "Fcy6uoFKVl5AzV5VdTBJju7Km2wBwQ2K2qlYnX8mFGYNehp7A5XkTGUqiaYIloY1sbbSSSRz/eqdemNLnoqfB02UiKXj53zStjHhEFxCl6JH2WVr"
    "nNy8uM2lZJfL9yCNKJfe+CsCmzwdA5NQxW5ASGRkmwmumUpjqlcIrdE7HQe7jneDXHUOf+A30SgBVZpph8e1uyCMCOfUascvW0B2NwQCEmiEgZWi"
    "XVSJVP0GESeFZpXASmCxWqW0jeIvuGnfOL9RKT6HE025kPclu5VsgWP0F4t5WuC/OrpDpjQnYPEZYJ5Ya8byDhswh+O3ZtDSbyXDENu2Gg+ILum6"
    "o8KkHTYzCRVpG9PVe3UBmawSJAncgBsZwYNHipRCn98S5GQgvhBapP4+sMxEHGmlnSvGFQU2+Wd9c3u0YOt9WbKk3eRNUx3oZ+xqPFl1KClVP5zJ"
    "qABQyDqIiIKmYlQEL+u3+YzZRWm86iiTbFOldtGahwQyqS8largmtHF5LakYsnZQiNQJVrKySVLLMusFJ+kMYmr8UQ7WKPnqhSZZEz0GxVBg7QFB"
    "VBFNUsKA5jvMDWJ8RZJM/96wkrtFm8P6l6STipoeCVYnSNV9BEF3ZsjiMVFKtFnALKImBtyaJnEnKeMI5ODmxFUIMYne4C8AJnkG6DJxHr/XrBCU"
    "/noGTAunfEu2H6X3lGRFdB2rYhb0ChlyhwElydemPGN9faGo/1HYqgTIeVCqF8i0xtHD1BypB64FPvJzPARQmu1U8IsCFoOGqbiSIFVBI0/HKASu"
    "+xJwDZ4kpitDRqYxeIt2HbWCBI2lykiRp9Wy1M1JTV0tAJH0rjZH2zi/LNdvBzeiQCLZDuYC80zalA1EIETapdqqxS0CKRIJ0mkqC2JFAuU1c0sG"
    "fhGJFqliH/CbWVIUYGRa925hRXeCOuGiISNZTkg4RbGBdMZVQo48Rr+kXC0cxkcjyEiT3AyCR+qiq0PCjrRz2zR+eFSnqgmHF7cHTqxThtVHAloT"
    "L8dvpmoBLj90kSSPwz9wktxX9pEBkvx9fWAk1RB8bh1cXuq3HzFtEGwascxvUHdKadxkao8wkurZRIzcfok+Ocn4QG9ZBKTkaYZxxM/o2wNASlpD"
    "Vegpsl7npQR6i/aFK7nvaTHR/vsDYEt+Eho2zuU/lFTULzeDDG/Fvg0nS3xgcEmkGRirBd6urSThfxRR8m+unLHjwKSYPNBUihNUkCGqOeioZ0XD"
    "TIMXulmwjuD9m8hyDRiT0iltLVI12+2CMclE9reQJK0VYjJkPVZ5Ohpp8lgbhUHOmqaP3WAmdXMxlZE4qWddNvbrQJxUnSxUZ8Y3FOrBpLozpoKa"
    "VpJJy0gcL8JUdEZHUSk4CZYIZRujVxWNPPlpIpXupPATuMGZzgy61WCyN3qfw1Aexj0pJWRhdZFlDnZKjN0WqqqVQlsMT1J1uw072WAyTTbsZKMD"
    "OvmlyUY4wJPKA7SwJ90gCthtzfBf7Ixr9LjrC8yTP2BAFmtNU+Qv4gvN8TasfoNby1AYLwBAKb0z5ArbJXAB6MmP0fp3UScx2tieJV9H6WhCOFT+"
    "lnwXPGAHe/ILFNXt5jw/YheXiINGwNNG9ieLGqTD7484yJOEwXeEa1NpFGxH9I7hvoEMOfbcauZAu/eIBpz8REX5WGwFwwPgFZO37UsZzEcyWVOc"
    "lYZbAuKeIC3ToE5+qdbyX//pYdFaJ1rMncgi8Bre1VHxJUmikoRBpwQTYlS+iM2Eci8GgJIKpc3R0fLJ2VGJkb9yTzxRgX1DjRb05Fdi++jInIqG"
    "HXHBJ0PPhcqzwe8FYmw3Rm9MOMz0wcMlAdFEtr0mQFFmMCko/aQ2EiXPLcP4WFKtFilzYkoDm3fs4HI6lqZqtw7doWrBUh7X3hawbbBHWDpVG210"
    "ys/NBCpaiGmnc2ApROBSkirD8JJv3Q8zI9kylXEqQfzomeA0gMMzrRkyVTgB0xgJVXmqCiVaoJVnYkgVDFvJNZTY8p3OdDQa7EqnLNpFrjRfef/r"
    "iBM/iasaaLAOWjOpRu8/gCWd8ok27IsxwQyFahko7BABF0oX8tsuASjZ2uj98YhNl2QGNFrIlqH71STE90xj/IWPzkdnpcOOHUne2chFC+lS2SDs"
    "CqMlwKxrVcozrTSoSLBWh+QPkelz1s9ymzB47s1teIfaMmj0vqBmGoa6bDRgfC0Zyj5qzSF4l0ftc1CR92YwZxOSJw1ItMYg+uUZ4mnWQw18TipN"
    "HlA5EeJRcx770dbuYB8I9mCJJIWMid0UCbQGLIYJatxzmXY6Tetz/ZqE0huj0TG11JViKBoORYm0XZkVc7N2o4WQ+SeZVe/dZK18U0ll7zEg/TTq"
    "h4m9CtNRJQLeUaMFnImNECHYzOPqBs66msrVPMGotVmUUgR67ZqwG130zI9FpZGm1RLL6STAbC/JvQ7pgGmmg037Ev9UroHcsKsDGm3kTCPhkMPa"
    "DLIO7oCO0CzTU330Ik447kpIFZJZ5voNaV/WVSLiUdDRdYo1iuEq+2muIWuMhs/kFgYHjOGoF84lKP7mEILhcgL4MQxLlBdIvekgQ4uKUJgCAc6U"
    "NtaCm2nDN6huTuzCgzOO270GJruBJejAPNiNB85QB116Q8WM8mn2/Ky0fkRMuzHUOXrajB3MaqQycJ+qTVRzC12zqQBWK4/srkLVKzVV0iqtiiva"
    "/T/gf3hen8sWwYps8ptoE04nUWMYOElWLe1ubspdlbDGkdYpBHjUqiBrU1rLxGJhlZl0uOkPiyqakS1J7tFmVcSsMQSmebgSILpq5zRW+KYrlu5g"
    "+3vC4IGwU0YBZUZXwvIO4uq036Geg2MTKmd56yOHpTONuiPY5minlCZcOBGn1YndAK+3KTcHO8HjrOi4yxRnqAhTxbIHhEKXr3PWin/I/eCD5vNS"
    "/ZS6cYPvLlSioSQZfF2ZSlutFQiJtoE2PZ8wTauafBojISGYqDXHSEm00UgCSqJWaFXm6mpe1fGj2FzgTbiwWLAgcLFO1svhU2X/hsFQjhKGWzNB"
    "1FlTqhdAacRT5pHGEC5nTbIzmlyClVesEQL1V+Stc5KuUqEEC3EMgAf0vDF8mvxUAz1WU0lFYxiPjm6RdWpFbnMkEKXubT46n0zZ5hy4MlQ1ZYla"
    "P1zLWens/uAKLjk0vn9wQNFyofyWVlI0eKMLhyICVNrjgYMyKn77dzSGJV10tHIa1ZwJv2A5QWxv2KQTQfJyPSpt1FgLll4H4g0mtH+gWif1iaVi"
    "5J9Q8bAoT0ll4n4yrUwtLsqYmCBgtDuofUAhLM/dorpw5zb1iVnt283C9Vwx6Om6O3KrmzJwaAmnQ5rXaK4cOy3gcTn3VoYhcUwCI3PcNZsoOVeV"
    "SRLX+8SBs2LfRsjaaRRQsR/V2RXdAWUQ+mhljdEIiuTLUW8B7ao57otKJa+Pwdc0uIglesj6CDCTVBiygDfyFuE8O1otOM9TydZUIh6N45ls7oin"
    "Mi0/DVD9rIHx7Oj0u5pzsXbCTakK5XnCP9eZ7YIFxTwwW95tZLuSXtzLdOZ+GtADhPE8j+fiMTAREt67mS4Q04l/rXZVgfWMeRkYOJ1IdsEr8qgL"
    "8Hk82fWvVZCQ9GmuPRsB8/md3xGPnc39NJ1OwnKzYLPQFxFon1/RNx6na+PxaLTPb7JN/1oFR7AzFzvXCnvFa7AgPz9tpbxZthLiJ5+8bsTNONL1"
    "3XU8lFiiAuDnSepvl2RYFxUJ21Cf+HU0xue7F51wSu96kxWIE/Zy9nxXNi332ZFMd8VBfOVi7/pDWJ/Js+eTdMGxChLqOyphBkrP4XnHvBy25WfD"
    "Juu7Hv9d/1ls7EJq72zm+40E/Py6xQcKwDmRIbLwSiLZziBSlXE/k7kskD/vqDOZA4pJ5TBaELSrTjF1/HRRKCOzPwDQb2Kd2b+CLDsLuqCDLhk2"
    "BK5KAo4+DT8Cc7zrlR37zparooE2YSDyI0wSp3JZJWx2xwDNnUs2tyffzcCucrIcODjtnTAkbTUMUJpXDvujZAfuao8goDwrTP6uF8QMHH3WHEAS"
    "hEXOO9OVjLfBVXYSObXVjAYqI+PF5pJwNO96vRQLLpjkiNecbPZbPFzzT9P1QQXFN+hy03KWGZw8A//v8t9ttMdxbyAEm0G4ves/XGDQiKW461BD"
    "dSS9VJZPMwd3lPNTyS4wbfaODqpVQsyaCQW8x7KiK55E0QJE+NN0HSBDnTli9iUnzS3HvI+IQPU4XVoo7hU8NHk2F0uQJowdwWZDIM422BUIfJrf"
    "eRu27KfSP013qG/2CSZ6sil2th3PjrXgWT5dGeOoXkWdAEVh7Fw7aj543J0T7Fk6xlwXCy8S2OeANdt9UKZYfI90k1Gj1glU9GOcEhcFehruGSWM"
    "mhDlJE15hP7JwnJJ3fw0AOICFC5ayNToBUP6lTFGv/n0q2//92efH/vkL8e8E599+vXxYyeO7R9nlFV21uuK/zTwbgOX4osibvJb0llYWaI1A+eJ"
    "zV5weM76dkUXTfADMFiX15WF20ApnfMTGIeLVcQXRYX1buZsHFgajgjfood3RxY9gezkd8Za4No68brhDZwrwy92gfqKG2jRLzIEElYBWPQLsLia"
    "sjaHZj3UOmRnxULAol/AP742EMmyqIoserIzS1/C0aRycLzn/rWKM8ijOZohCmX0dKWHDdboCeaImEIZPUGnxxijZwiJyAUZhe+N6AlDjH5sdKWL"
    "LvqXn6Zz2YRBF9V22BGFL3o86YKLfgJU76U70WrxbYjRU2TnWhijdPi+izD6nXOxAaDRU8qoS9JXLtgobLDDfB9z0Ea/E1OCUJAU4Oh3RKEW5Oip"
    "1ngi7mCOfqfsPsvL/gYkT7JNDWZBj34u9pxAj+JoBnoU/gmGWk6LassqzeaGm/TyBID0m3isNcHmUCsGuyw00q+7GBrteBQBBSBJWRJUQCNFompD"
    "pZW0jV4LiPRUEi1j9ENsCNJsOvOu18UgRdHKOh5L8ZDwsi4i6afncvgzfl8JkzSHhmgIlPQkDHaWzXJ0YHKVUElZlYIl1ZUUIzUamxQOn+zlisik"
    "yk6PQCb933BXhEMAlnk6CbfTm6FFJfycUL8DU3rGRxfP5/OwoErBIQGJkianycIr/QQNBrxwg1iKvOUgln4n15W08Eo/Rmu1ORKwVEX+LfdLYZZ+"
    "xxohaWOWEk91GV/JYJcisSct7FJYWNqCLSVWwupm1KjwUSsxpANiegqsAT7czmQre72qXNn29aJRTD+JVh7RKKZfgeeUZO/ZqIifpm0s029A4uSy"
    "bSxPDZbpd758nAyhmaLD2amUhAtnCvMpfyEZBWTqrCcSzBR4PwlehgwQCWh6wgctNI3mutel3LZsCzDFgQBOT4mbFWO+QcNAvezvE9oUaT2Ol0kC"
    "LpCoIs8STKRWFRvZJ9ApgV3yIPj1d8Z1rB3u1Di0+HW7f+5dL/wcS9SKe9plFMPB0E9Z4iiXl5yGrmRLTEyqrD3RPuBP0SnxOzMp8mbh9xZS8PuF"
    "QSUuzmo2BjsHjUs8fiQhOdIMvZM7NPhTFXOCYYEh0JfmeWnMpO1Ooo2XbgePnR9A7iGDV4ISmb0hoNo+B0YOc+f85pxPXiSGLDgocxZM7kgc1A5X"
    "AHrtnV5VHNS4B4YR6nV5bO9AqNoATEpMp0GIzA7s7B8HNTCFDJ3UNjB6ZahkMvsAQGW+zOkHuyhSgWHYTN3AT0nbSZgJ/D9W7UfBlI2RJIlxWDSj"
    "PAXkUDjErnbMeTsRKlu71gv9VGK2OS9NRkSWT9rM2xY/CgyXgGUx63WgScmBQ318wJDW0mrGPv3OIXOmHD0QkA65jsZnPCAIqh2swQHIE4j7XpwG"
    "OCe/daGbFkcHsz2esTfmvXspxkMXEFwYGhVNXKMdaOl+GBoV7RcdmFMmcbYSSKo7psS0ovFRxcry+dNEZ7aDbdwgOmpXtgXlu18VH/UbkOPtYGc1"
    "J9NZtCDPxmxzNwyUCkyo7EkXLZUusMNNqATBUsmty8W62sFu6eQ0xUEQU+W2OpI6MtZuOx/YrpZkdlOMBbcOEoRsfi/XBFaQTxGvc8l6wKhK9MM+"
    "gzaUt+kgdTd4iTQwIlhGPsaAkT6SzU3xZOfZegGphi5DE2JX9hwWbHEOCBQnGGWIKdeZPIvRj3QXR6F9K0AGR9nCa5egyP7BVTskhKTFSYPRGSZF"
    "YA0Bh5WTL2wL7zCgVrtwqhxcxNl4KhHHe/Rbz1phNnVZKJyZgOTOyAv4lQCuyiaCcza3+iqayiHrrl8acbWzOWse6ZAgyS6gq4pa4poCSI2SxVof"
    "1NVqo1BQX3QzZmms6w/QyCEArsJBUJhaaySKLvoYmUKgsPYEpdK03Qfco0wZ/yi4HRhQztrhbFAp6gFbvO8NjhXuMPAkPNcep4Bnc/IwIVklUYB+"
    "gRpc7SIYpD8q5uO7lx65O3CJbcmz8CImwuJmnlYg/v3jtHbB7RgbTbIHWq9F5A5qxmy1wo8oFeDI+T0WOQcFbP2uKa6y9iTq0cY2SsAW+aImO+By"
    "uzAg5YMYqRt0K0Wzu7Jt/jlSyamO2Lte1tl7QnK1YrVZ0bGWzmPT7TcE54rxL9h9tgvcyywtFWVfrisLFnkM1pnBMlU0WLyuVMe/Vlvb4SdYH4gE"
    "SvEmm2ItbbRz+Pysj++ggEg2el8m322AuYhvonXUmcuCPEhnWxNw+UArMNc5oLMuFXDy2Wj5K4gZzHfDAbX5XMuiMuE5Hp+yPO1pEDkor7SAoawg"
    "LyaGqKxxfJDTK/8+WK94WVl1WzG+rYbAZZH1Yod04Ij9VHtMgjNJCgzijfE1YqQsDbYWbqMFIS27YB8t8QZU3xRhAFEW9zuFcXT6jVxilbxSJICf"
    "wul3pXLZVBpuAMgWlpIlJknSHWLMGuTnwQBe8ao19yY1c+P4vMp3/fRnckA+AjHUBvfqiEDLaomJxW7osCL0q3JqRMTEagB9PfbFiU+9b7798tif"
    "jp347Jh3/OSZbz/57qd+eOj4yW9OHv/XtW+806c+fddz4rOTJz7dNxSsHuJbT836Lc76r2t/MlN+a6bEv7l08sw3n3361fHv8KVTX3336cefffon"
    "7zv471e80mMnvv3kzwdAjDXbgnkJKfar419bL313EKDYM99+8flJj1+DzZ58d/2nC/jaic8+9fZ4GPtAj/0cZHIL6obOZMKuasD8JxXs6fi3GSpX"
    "A3LsSQ6imlxxNHDsFxmkQfexmnFjJcwINCyBRSnb46iksry8JDi0zbnG/eDGMvPqWFs6k/ZbvHcbGPwhYRO2BoD/zmUiFMIvBCYblDSUmjPxYT18"
    "zh4dNOW7l7DVllROxbGyIhhQ8mLhzk8DKtV2AAzZLnJrMgwbpYxxbaYe2c3yrBuU7O7riBgrtzc0WR0sz4lKA2NYij8qdqV8p/wnryOctdsTiuzx"
    "ZCKD2pxqDDO5DFMFRXL8BlRJTcDU+Iun6kPQ8MG9giWr7U+yDusLLnsylWzCqFwudpYiKKLHYFHvNjCsxsvOqvAPem0UdZNALDxnHKouNGXJ2wTm"
    "wEXHfk0os8c7M+dU0Dbng21BiQqURx0qD22ID0zn9r8mO9vovpLoOeEJJNnKxH2msFMFY7BcOETx1Ab0oFqa0YSkXEgX2zvxmCIcmd4nDgaPDSZq"
    "ICGFZJZlR13CIS1kgLpO+28UjZarSVDsERdlTNaMtohnAWeJgg0bg+E3SwaoIGisLaNLtUyVlncaneT2mJGIsbCPoMKUwHbZVALvu4VLKJodh7iB"
    "He93M8A77fGz6S6YCZGp8Hb9dngtc1A82rOBSLKpkDuLq8S9tsWTmGixvfIGy0LOqkQeE1ZdAGqrjNABTkgL5TOJr2M6DP1JHNWqkGdGR5R+SyC1"
    "Oa4yHqi8TOuJwFK7ML8nXRA+nkIum0YlkeO1Oi/KenVSNGZeVGtH5WqVxwZKS3kbdYWp5QonJLk/chBMBmuwrBAdOqRIO166WndDtAatjk1L0Sa9"
    "88gBDgmYVoeXo4YTcSx83h5/txGR1asHMq1t4eS0fEPJbls5aiiLgn4pnNqkVPxk9yUa6wlY29kcSZopWgB2DMmADSyf4JQqCqiwvqmGYEs0agaK"
    "evffHcb2zJ5j+NjWFlECrvSUuH5kNsHVZKXKAG4sYOdT2pqNKdz0OSpZy/mdGa8z2YSF/ueSjZ7KyGdaKHqHLIXH0EC9Zl1kTeuYuSM1UAZUPhT2"
    "biKY75fEvz1OsTlshsNGJPTBmbcwym3VaLOuQSXjd6hH9cxdnDw+axfHtcRx7mxaSkdhJK77xsQEFhDiZ81epss/99P0YaHkntxPXOCol+iiKRL8"
    "tKIyaWzgWXN7BM09BjyN/W1wLjGsRfhrXDJBKM8wgJmiiMdu2LnoFDR3JeF2qAaGDLYBkKBV0XPBt8KKSOIDU5ElLkJV/NzP2tsJ27dFXsbPz9I7"
    "NSLokhXXLJdNdqgT4InCzhWrvSvWDPL9nC4v8aPhc/Vwvm4pjUDPZfLN2m2aQfxcLmSjgGmOMXQzkSC6GBuOpbOgQmE8e3FRQLod0iV5luI/Umnv"
    "a/Uehajbpa6ULsg0oTphpV3RdfE8bFNiX/C6nYeJryvVahWgda36OBq4OSlSHE6DUylSesGjo0xx616D2LqYIfSl5PBQsXUxukZjgDLi7p+YmHZa"
    "8TToi4R94hD+PuF1tZOKWsvu0Yq6+8OH1m23Wl6y0m0XArh1u+4OCqtb45RkA9cVULcrS1LNvJcEHicZVD8c3biHlfY5L5XF5tvMrxhLNyBMbK9S"
    "TRa3YyW5cEzliKpWYBxdlctKUuVVm5/KZdF46Ip3oh5FlYm/knmHfxKS5/MpQFoLoK5V82gej+xN3QVhlyhu/wC7HYFy7j3j657ERooYCBlqdDd1"
    "ieGSit1wd0/q+k6KvJim4YxVYfnrAd9V3Vy+dHMh7+XAFvdSXf9abfHCPc8cx2rxE8m9LIutV9QvGcp/qYA0nDA4+GcpergHIF5sRcH0LtUEZA0G"
    "b3u8xWvuyiQ6k2k8fwv+D30EMiOAd87hY+3URI0SXxV6yzjf2Hi8OoFXGY33G074ZpmLHEDenIvFq9aA1azIj2LiA9s2eifiZw0rYpWx38pnhg5a"
    "R5Kz0LFILF7b1VNFqU5bcQQ0L+FOoCvSEgLotdEUlK4njF4rd+frYgw4sj/4Lj7vu+tg277bwNCaXUNPT3oftSWBy1I56zJ+GsDqY/QFKR1YAa1X"
    "VVih40j39AWeJuENYLoFJ/xpWoU1aC4D2nuSAp0qWmRCJclUsgnEkQLplaLerkBFD9UxGGAOsAsCSL3fwMM5hOkFaZGIe6lcLIXN6nD4MSxuz3Ul"
    "ESuTqB/jAC0oxZlKOxJxF5/3myzedI59qpjEjB0CpVZ4rDFnuAqkKb6lEEyv6oyTLj/sqrTdygBYr9NFEP1Go8d8x4SZSHYISABvTFRHrNGjkmsJ"
    "jsepwIRMTQbr9YNIvdgXnWn2la6QGhMkCd2c2OidxtmA37uy6EHKkMlEux9E6T3WniHGSbqEbDGH72VUl5rv4PV+g2PHuROInCfaZlckWG+yKZmI"
    "Im+8jq6qWL2nkhSgIy3ME9K6qFBKYraxCoi9tgBud9qGsxZi7wn/bBzkC4g4Imuglyas+m5LEKMFYHtz0rEnqEFh8F5V0I/wvegSZQW4l2vyz8b1"
    "CJLGkabLNsLz7cKamFiCCrHezbSiERJRHamAfV1QEUm7s9TEr9q4oqwpi5RCdYKoVYDCgFQQG0DifrjIDAH8dln3r1aZxfsnMmu3e0TbbPDfIEEK"
    "uWABm8MM9BywfJffwvSoo26wyZAAtjCAj4PUIumgDBawV3KVUtUNEnaHY8TDzvwVn7HUMrf7wWeZFDr6FM1LSLcJqnS8iu+STWDGhDGBpaor7SfQ"
    "vdKIwPbBqSQH6aVkMzpfrcw3DgrwxyAiWfX5oq1yFVSdEro52QwenPb/G72v2+LctkQJ1AD0L3FdQKlj6LCFn5ZSN/jJPFMB5pdFNpXA0ShoK3NH"
    "IcYtEDYhayP7npDyZvSXwYvwCdvH2pRv5QKpOC56c8eTpt4RBRqQItwZDtyV5W/Iamz1sWUi2Zy1wX6xtScE9usqtoDaUvcgRNMmAclYWwOzmku0"
    "AXRfQqvgyv0WV9DpRAjQFbXFtcAMZCfHuN8JAX7TINck8Itq1ZebpFYVgoQSGs04KL8YvmYJn6SBwUgG/sOTgn/0Qj3TP8SBZxXhRhmKVwcPG2+W"
    "iozZY3rXz5FktoUSZ1tibgtSs89sw6WDKGbPnq8A9QueHmGiGMfrqBHfXtAdaRCFYkGv8Uocq0L1n+YoegK81dkM56WZFck0kOKUjXESRZXC5oTt"
    "7VR1W02wwAKQphFNVT2t0xqDvZecpCGekzYJMOf9dxvN3DDTwFFOJOyz8YyiTrf3yTttG3SqqiOkG6riBX9upmT5RAeIeVxeFZyBarhWhS1dYUQu"
    "sh6PIrFjMLiLqKqVOm6I0ElJ4Clwwb1G5IhAApb1ODkT7ieRzicd3W/hCloLMwQBgay/La/MbB6rgV/QnalAOW1YXXYWzRMd4cuEoYDrLB+iq6wC"
    "iAgGSQK2DPyPtkisRQXo4RmCs0IHh5KSvUnxuqWKB47cpJa6PL42dXCNdot8VwpmgZvhUqecrlKhZasuPAciR9flwfwZwgNh/yqH0FIDHdgNEAb/"
    "FWhCKRlSlQAwv/BJg5eRvgYy4TQJy6GbJKxTLA+Xj2o7yTcrvbr4119QzasD0E17Ig6P4vcgOVtBaCQMxZL9fzYeM7TKGA/4iapbCIACf4O13shi"
    "/9194zsfzZxz/909hwaB4HLAAjknwBItKdWnSHqtWGLqEK9AmtjFrRa34x3CzZ3genO7Nh1WmOQ2G6svmgxwvZAYhxpgmQRbZa0J1ntU3SMaqPia"
    "syZ6kauTVA9a0ryQCWEIn7KEcUwL46oC2CXBZFMLkZROC2Wd4rogKWsJaIpaKrYOxS3ULioqMvaFHWESY5Ce8EMFMeHRq8AN63pLVd+GdKUj5SEV"
    "ZzFtu68NxSz+rc9OMJRyLutami+JD4lexHqKSK62jxHbFTAN6mNzgxGpdtw+ADBMctk3lEfNzi1gM/iqzo+AKlo8P6GiorDkFGZeQx1s4bS2zq8b"
    "YYdlvzRCTKn5SkTo2UyG3g0GMoBpktVAiLmaGDccS7dqSnf6kImHPHaiXF/kiBfXja9KR0ltepKQXH30OZSysELCDPGLc+c6Y82ZhIIYZdqgsmbG"
    "hvSbjf51LEeV14mrS/5poME7mzRRqw4F0wSSDlcJJ+t3ppPiD9BSVX0rCr7cuVaQNmhT4j5xBkOEFrGnjZ2SMZswc9FhtcSaKTKe4yOIkXunGE6H"
    "geOSvI4bp0xLdYlFqiWYnsgWHTZDV5UcpGYMM6F4VgtXQB4VMIy/4S4a7pIWvBgbpQit3Ljj0vpk6mgc1oxqowpJybhlo8RUtZVR+ght3OJb0MaF"
    "yduF2aXt+zci0Y2Lr5/kr45sdw/Y0MaFhdntxY2d+YHizKPdsI03++5t9i5s9k3sDD8pjr3a7Fnc7Lu42XcVP+x9EQlsvNl7Z7P3x82+vs2+wc2+"
    "EXhss+/VZu/6Zh98uLHZd3mz70Ek0vFm3x18oPcZPTa52fdws2+chtqQV1zE4/zA0s7EEGylMHUlAu04v9KTH1nZ7IEhhjd7bm72LW32zdFYg1GQ"
    "x/nHtwsP1wJPRaAeb/Zd2+y7TQv9YbPn0U7PeuHyDQv2WJ9rpE2/2Xdjs2+I9nWXTmYQxuBbcsS9AV+Kgj/evr8Ee84vv9l+fAvex5Xgeh7wVQXA"
    "kPnhaDjk/MWX+YH1/GhvceBuNKnjgfQ+5wPZ7P3nZu9Duke4nR74IYiJnF+5AkNWkJWF2e78ymh+eMK5k95VGvxS2H63v8Xp4MTw59VK2Mh4DHgG"
    "QEWrfLBAHsWFl1XBkfODFwrjP+ZvDOVHJ/JvJkPmpk0QdNTPNTnuAxqZb3qzG85uFDkER7uNv/Zc3uyF8Vcr7RmmZrbdDSU5/3AqP7u42TO52XN/"
    "s6f/543B/OgC/LDZu7jZu0wkJ7v5eePSruDJvN6tV1ObPSNRpLu4td69fXGNpnuz2TO9C5RyYfhi/tF1Wtmk+10NKMpw6OoaHrhHI9Sk2ag27GS5"
    "i57h4g8vt++PqGHu4GHhZmY2e6/9vHFd23xA/dtvX+cvz9Nu4bHRzZ55fKun/0CQyvJZYbq3CKfac1dkNom1wsz6Zs9yfuFx/vILNa29ukE1EF9m"
    "3bCVw2vY7H1L0mUerx5+RhabRJrtvZx/A8f2SO0Nbsda7xv6783QSmvBW+Zh1O3gqIXxSXfU6wcGWVZrXa5KBYMBEQvLMYMCCW329MJBWC9c2iP2"
    "sn7Weg4pLv/o5vatYXX1Q5u9l0BamDfDjzhEuTcsZtJspLVBAuE2UerAmQAZwBYtwYKcvtnda16usgp47kCQzVvrI0CDKDLwBi6Q4LlAVwGi8y6u"
    "UQhz8ueNGRaRhXUQEW9RWIc3FEnFJI/qBOlcHFoqPhhi+qww23KAWuCIgPnzg6+Q1Uev7MxcAIMNBf507/YiSrv8zZebPbeJIjVdTvPBRqM+8zlE"
    "8sz+wZ+VvFzeejsHxGApcbIG+wbzg5NoIfRcg7XzPjb7+llboi4eeQoLKj69ClqOFMr39j52RYdmO4v3UFzuz888yV+AQ7qbfzS89fJCRXjonb5F"
    "0PDF63Bo97WG3x0cevvOamF9qTB7c2cCdrO8vTgF9m+kbODlM0j0Zu8jMo6A5CYrg0W7guY+cnXPj7CrwvhKvnshBBZt29uobe/c3Q0uOj/Qh9Rz"
    "uXv71jXY+fa91eLaSgWIaP0UrEQ/aOChmfsUOLRmFMaHJkruD0FEF2bv8xbD8NDwVWH06tabGRccenuxmx0YAYdmqxSku8KG3uxZd8GhC5fgIHqA"
    "QeB+bHDo4tULxbHHFji0bRC6ENF8pywrAgDRvHz9lQsQbW/PQEOzHWTBQu/03CuOLTKlWuDQZD7dIn554GBEB0xhK1yy2XeLTMVXJPXWXbTogM1r"
    "cKMDEwl+tBaWwWBbpKhyY5TsbugdCZ50fuFuYeJi/iE4BK/AuuefLVDpwuoinLSDKq3pzAaU1sZbFKB0fuFSYWYNJToZtYGzsoCli7M9xfHbFqi0"
    "2tegmOwaWnqz9zGd5wv4zUGUBtlZuPmKXeYAnnTxaX/xxVgISnrr9Wxh8Cq8wRQbASONSmloPuymuVDS7FKJxkJXI2ixR8FLh52eyPciUKfzG6Cf"
    "gcrBg5xUAg6kxmzxyVAQcVof1mbfrD52BTsNTlb+7pCLOa2lsgBOs35zIKf5TosURFCQ07j0vnswQyTqdMgGe2RQeRX8NOsmzboagpoVoYM9HWYd"
    "hUJtX4SFRk2MeBEDEr0/BGGolUPSh0cP587WBr2u8ahZrFUEo45UVdFQ1Kye9MFr/GmQQnjSPbOFhz9srT90QKj504Ap4IJRwyuFiYdhJOrCldvF"
    "Z9fRBhy8CA8o1WVZFEFsal5aJCi1IY0oPGr9oZgwyoDYDwq17byqt5gT94lBXZi9BL5CKO9pi1qyOo1rzwp9/2jU9tDWI1rb7AZGvfXqGa3IyEt8"
    "bLNvioi7Gz6qEZZaDeSoooPhU8uQQfk1HJiEFQ6ajmJ/OgS8V9hqoL78wCL+xEbHfgGrK/E72kTdPfBM4NjhZVr2XStgErTl649oDdS+9RJ8h2XL"
    "OWdRT6OCta6MUXOosBY04ZHBl9mWDysUVBSz3ez383jo4PO84PtaYYG7ene7oWC7vttd8ZG6e3TEzY02mcOLRMWudD/8fUVwbB2Hoy+AQvcFkB0I"
    "7llBv4iAntZVB4DLZovfiR2C77dMpNU7pBjnkXILh1kGh1ipNiztQCif3LBHkbIGiYJHge9AuXBYpD4o22pT92n9Eobn2DvQm/wAfuiFgfyjFxjk"
    "syOZQUNisThwN391MKDYmG7rBr3NKxACDxlUeg8/b8yE18diCy7V4oBg9LxmIO6wHeUQrA5F93I0mkJ/+PxD/G+IbA8C0r3Z+1qOIbRjTIvIpTwg"
    "eTKkkkEPaD33KZqzole78+qf+VuTKHYu3gEvEF9XXloAupsCEY/As9VaNIDa7erzYeV8hIyeKAxvzWv2+BEA3qEYyiAZvqt0Fsu0vUk2H21I7+LT"
    "XuRb69Iro3qLzwH3NXeLBZmN5F0YX4OzLXTfDYJ464whh2wiELzzCxNgqmqLfv/o3Uq7BK5+mYS+S3uKf1n0b726XZhDyepeTURc5oB43jwpEQyu"
    "Kj86ufX2Fp3NMFxgYbjHqCKgz2h+uevo94OBegfWw7FZJVH07CowCtKPgrIgedF8GrsJXmqkiNs/mrerch5Fp7dsrYdfhdJITv6roi19OKDf4LPv"
    "7VpxUSyIgFmXVKr6vph/vf/kHNf/CB64OwKR3iMVl4fTXI5aEYjawHL0HkAT6fnhmOqMCR42F9Bw5qfz3UPqnE0IaxeocCUgbO21SrmCVfQiQ7R0"
    "6PDhipQs4WSUWBTt9CwWlse2N/osHiVJhvcoOqfeIOPRIlgFCZlqAvYenWQl52c4f/UBLjxKHKsgmDsaEJtYpdGZo9rxyfW3xfH77GuFbOJhflin"
    "Wq2cll6tsobrjmAuIyq3NyLeyvnWyFybGpo+uEm87Iy/2UsWg5H9sPk5vIbeS66XF3HEtSKeV9DXDyhDjTZBhXxXRaKoFRGdHtJ24Nb6+mZvjzLz"
    "htVz8j2mUu64KRZzqfsCTI/SrCHt27dMh7KM/I11SxvWGB6lqVgMR2jffaKogwO+9frK9p0eJCjgopfdRBiOa8zOqK6kUoGkGnDVA2ZgqErCnOlv"
    "CF2djoLr2aYlkGGH3NE2mdU/73RfzwOlIcGvqNKTSWWdOjEr8My2XqOYzg88hrfQDhq/nx99Dh8WV19hbnzgcWH2UjjmY+IsFceURGrh3s3tvtdw"
    "CxyCJKa7z7TOeoXylODwvi2sL4Hqzo8u0/NkfPYMk4VFDwAloNNEch0EBO4O6Bf46L5KdlYT4f820O11oITQlW1fvL/98kE4Sori8Soc5pREstD1"
    "Jz+PyjmYVPDYLz1B7xUv/Q5J7WE0F7CIoAeFzeIg3KxcHCxpegFEruU+2pkjDok8EOqCoZAGXtCw/8TL7QVJseimtG+qKOtw/u0AyBTbbdk/NHwN"
    "IgoJi0LrS/PbV1/Xhg7vRAoruz0VoeHVFu9rz7gKMrxxo2uQt/sGhd/TLHReNZ/BXjHhnYidfgZ+pYAamlU1nsSegeI5yFXovsuSjIP0fC7aRntU"
    "I03tAym+sIS1tIVLQzvzF8Dd0c/DLPox7RvxjPkLI/mXd6oUYEVjx9vVJdGw8fwELof4Yi+g8Sow/yAqbB9RdwsChd/FkHFle7h2THnSNOy17CFI"
    "gQ/bbkVUTOcXwpivyAEVvAqQtAtcnFWDNUZW+dar2zvTI1EDLatqqlVJNUuU05HLB0Opj/bDeh7Bq7aVmL8wYFW/VvI76glbX2lhBM0ZtbSIoU0C"
    "Z09o9sWhJVDfYusij8NJL5ga/OhGS9fBv1mtBGBP4PYs4namr2J2jSmKnSxjmFEVDPDWj7Pbz1aleosUet0B7YtLS1vrl8gRYP8Lc3Kq82CR6jKH"
    "lC0xDD9sb1zSJ6L87Ad4K8QgIQFzk0TFYiX/gi2QXwvk/X8AUXBaSUKwIVLNDwzuzD/kSg6go2A00cmxzmly276/Eh16xNJAcg6qRo3wf729mBx6"
    "O1d8dCsYcUITlcKsqnaFxS5MDQ+DD61uz3KfF15a9yBm4G8QKb9ynErkuNp6VMpBhe9VXFFxuXvnxcvPCgND4UYI492h/R1MHkRGUkAp5C9Rofvg"
    "bQmy4UQjHCUjx3KKbpXjOv/kGiGbl/Lza5IwIwOquHZVCm3ZnbAu8yC4+8WZte2335vT004FnuFT1bryPf1wASmOy9aBOdzE0aFi7cud9oxxvamS"
    "NfPyQ1V+qlRl8BvC4/95Y9DqW3FCg5wCxyqN7h535fSSC+Vc5V1ct7zBUM4Vn6X7377/EEhy+82GUmE3w32ChcvjxcW3REfBr3i0j1WwU5WE4BWL"
    "YRKo/efjqdQ0UFf8f1VlEyHBjSlJLHlhs+cWrPmPP7++4dqVpoomf7VfC+T8zEuKGz1SwggMx6mt9SsBCc9lFdX/YECkgaMXTlR+n12WQ/q7AcEA"
    "te1IVRC+KBAXJqztP6qwGmswrHdhMVinvzRQxVpWZqjeomV7HuLfGaiQs6GSK9IfqGyqqhBQRaAVQH9w44G9qnr95YFaCX9YpLRcX0BKV1LfAW1r"
    "XNTov0RQJV+lJo72Nv/d/z5BJCnlX/+Q3xhV3miFk+vtr9TcVCV8rGsGA/EHJFiOkOo0Ckrs61IbhNIxkgkfhCwcJ7zuHJRmTu3RdvcEc2iWNtGn"
    "Vk1uwXQ8CB1oKAW3WHwKi3mLJlnvKB5Cz52Aj21q8sAJwBjIj5EJukP/YwlKUKyKrMA+AFTFhcnbfD2iXKfRy1Bz2XodZYkxMsXFKT5fxB4w7Q2y"
    "dke3ya73rVi7cxh/OeEwgmM/b8zoKbStS0sBfxYppUJrze5/XaEws1aYoOAPi3PMKPRZBPYg/5j96pu7/Y2F0KvDkrGl9dLtXS48M2dQ9Q8vBEp/"
    "dTYdO6OoQK3qH1/g1gAipUdbrybC+6rxzzBwiJRrm1RftvbRggNG/UUGXXzIp6vjJxF/jkGjYPCkEX+KQdAjsF9W88PliL/HQI4R8ljh2sjW69nI"
    "v8VgqiKxJHCaGFIa76L+GoNFr91SoBQCaYj+owwBhAwOxIJVU+XvMISroQpwmYNXNQpHGEs8+EngTzI4zQmH94cZeEy7Ri0wqF2FBoa3ZRXclDEt"
    "AAKJH9Ai3KruZZWhlUCt+xcbHDQJbOyEa34LVr/52w1szNfhrzcwnwUK9DwZGOzWgDZFvwDUMMfi///yvq2prutK96+sUj9EOg24nc7Jg3hy207H"
    "dezYZSk5lSpXqbCELaqxoLnEcavcJbBs5NvRhb3BCAQCITZs3TB2ZOhKpKrzJ/TKQ2wn/+LMcZtzzNtaa2+Q28mp6nbQ3nvNNS9jjvsYH3icFtlr"
    "NH0trtntENjBz3z2COjbW9uY8mJnlkZ2cB8pW+4xdaDpFuIhMRoeH5d3pov+I6SFXPF/VxAQNabkaQ8dzKdbiIjoue8X/suQiH0OvNBbzT8/WiUx"
    "cIg4EUaBggdxrasUSq+ZhfjfAhYhbyWTJ3x5gb1z2pgetCXNFVou9S0ygRPl8ikd10wJ6zlsBHLFU6xVKM6v9GEDpwaohPuJzam3jQWgAUcFkkS0"
    "DyLK6mJJ5EyQjjElMgbLnb/OrZHf4C/3Nr69+kkNTImoO8p920Hpx4MkkW0+AXLuhhWEbhXT1+pMB67lt1f/pCrxgAxTc6CGOQ3zAw4Bb63AVk9f"
    "+/Zi+9sPL6WzEdP4EuBsoYQo8/SXTSPakk+7NtNw20AbmkPPB9VTUFh5geMqRtZh0RRYZNC04gbWbHyCvYU+RsXrAwy8Jl6j8CjoanloFEFLFudz"
    "dxAVHigFsDkNS6GtUNYV4PRgJUFNbJytI01OKNyDvzGGutkINrfuWc6A0wstrgDKIlefIVwra7kF4BY+ogVywqlPSE8OdhYgE4KGW/Iy2GdNBurz"
    "z4PXu4xVd8TgczAcdA9EKDPFO54sBYLR527HXTDykwr7AxAM/M2sJSGVxmwDQHyMZGDoaWBS4O1vP1mMCYzeRe5TevD7P3z2l28eQH6h77ejQqaS"
    "WIZZrMzU5XOamYo+ga65R/h/d+zE7XIdoMbPf/bdqiGy+8/+/K8Xdr5rbpfMHsz+rf/6fuFPGJQkkjMzm/7znx5/39jU20pn5aA2cB1bqGOjGTN9"
    "MaYGTCkBAXIZ7i/b4+jyVXdZdYpJ+FIE5oKOy4awpB7Lay7lI3L4gcAN6zP3RpKbSFyKvV2wDw20lh74VBJ2/5EbR6ULDekzKJaW9APiOLzaRg3g"
    "Ea0pvCLylg2mG0P30xtIZ1e+W15CRcVOOL2JGuFDjM2v0Oq+E5QSy3ofqJLTBMewoB88B/N7d3U3yTn47c2vv/v4AuhWCQQQzTVL8D4KipKro4YN"
    "lMjrfft2FclxmxxDgKgs6Qe6L4xgf9DtMzfukz9iEubmX+c+Rhe8jsQOTSQr+3zsj+D74p8MedoaPj9x6g58ePOPZvifYnhC8DziEgHf+b1C6ZDg"
    "FOfspZDSSW5C450vp9NpL070EdG57kZmOs/CnBOdqTjLQ/A+rEdUSManX6mGUYQcREKu+aFAdtl99/GX6IalhbRiolaIIORPok4wZtKUVyGZ/hmP"
    "OOToYjgNVPlkrzyKjc+SS/vPj1f/elPkF9QFsW/B6WPgwAaAEFQoUL9MXkcJ+ZLDnkFDDMcNVAMJnTqJCmLprxcaShNgkvSQREhXQasSdk5SDECN"
    "DJZAkXa8t+gELdddzJrw9UaQfPdxWp0jpcyijUQC4prGHoHQ5vVb2CbiPo7zKXox+HU2N9t7xLBIFkvePU/gk1DjLdziaUx4gt4RNtHf6WvW9iqV"
    "kArJJCIDfZnWUG+7ZJ3K8R6q+YcvMUzzu7Uvo2QgJ4r+/Ojxt/eXjM4rKRLBL6dRPXB54IJ8otWmCAElrBspS7R44MoSQh3TCfpgg5wulKcbHznF"
    "CRLPdfJAaofncyyB9AhuIDB9Ebo83b6Hrog1zmxt3fp2RmUGafrEbBdf2CSmaZFWaBus+MlvjFYmnOUaHBaFy4Sd35EBt1BbTKeXpnJvV/gSiVf0"
    "z7uf/+XhV16CWnI01ycV5vbd3N53XzWj5MCw+UkM6iL3yfc2s6rEK62ZgplMKQlKT+0yHUPlW+1nyUj48hvXjFbSIqMApdTFuXlvlocs68DCcEMi"
    "244xXVNt62DF3PdKsr18MqkO8StuQQ/MZ8UBSZrDdypiLuwahU89lmUnR+NWVSoGfZdyM8c9qWpdfCdIVuXWSn4rjM1cux78+zo++Wn0+jvCWz6D"
    "W2CUDnA5bILEdKOhEQPZs5/ESZa2XfS3Vy4G0UhK+qNArGeQXJhyBQtwnQPavuFV57tqexe6oHaaoJn86XOQoWFvIJ6hD2jzI2H3mfxsP6Hy2z/N"
    "/vm/PqVMZux6V8U0lK/Mxjhx9umsX7tvEj1SBgafu5/kDG/f5ldw5FwnpX5GrzY25Lcff/LXhXXLj1DD+fy7y0ZkX/K5CAkySahOZ/F6zc25KFDb"
    "2Hf0uqV9jupO7n6JHP3xtoigMDkD+w/JLfdPnJzbVM7L7Ey1efrsu7k/JcVEMNHcLVNDPfj+4qqrl/TvmmptKdzsLlLBrt0EKcMRA4lLJDeTHUrk"
    "3MA4obIdzgMvFX2JffM7uIft0FjjNNP7zJ+etrU+dyVT5gIyx2M+IdRkyT+qVsQfGAHx/cptO06mBa60NtG9RDsVoA9KKgr863cnWz9guBWQe8im"
    "3VQe2LyfOE3HtWzeqDbLfAmmIzjhMqtq9HMjpTicQ4ZIKDKcvx6yJV8C5hK5rkmu4KKVjFJHEO6m7ourPEh6JpvoRidu59iIO87EI/fjMhHuIc2J"
    "aK1OT93vn4tCNKTx7y8/wiHvsxYDm8dekb+sbirWGTCgzvLT2E4W91L4rumLqLtRa/M7zmsw1fKLYVb8G/lZ+V1MQW8Iq6TS4E1/iWHGk202FrXk"
    "oz3QCtJn3370+V82L31/f97ylypcBaSk3fvfbl/OTIC3LdXULuhUFve4+8yzCMxksCGwfZHlyOYym11MH7In+R7kFGi8uFjTxNvVjs7ftpWbT/Wk"
    "gHdFddxRXuTnX6CkjDLmpj+lIg97LkWNzvObaeYRNPSTEMv3D3e+f/RhfL3UgqMkOslpySw+zdySsDOu1y7olrxPkp/DpS/3xYv4INYxdGGUd2Ec"
    "hfrKEUArTZxV0Er7exf3d+f3d9eS0Er7u0v7u3v7ex/v797e353Z313Y393Z313VSEv7u1P44a393Sb+t7W/e2l/t72/e29/93oV9pJ6+vr+7pf4"
    "BjOdh/D53hR+eH1/7wL+4A9mmjARnvLq/t5n+BsztW182+7+7iIOaH48a75NQjclXrS7jCObaSwkQZv296Zx5Fv46hWcw2dub/Y+2N/9xPwRozft"
    "797B6X2Jb7lCr8C9MX98IQufNfNPYDvhdzs4sxl5ch52Ye8Szubr/d0GTmKBlpECfEqNgQuBHWvhxMyhfZ1GgXJnAwdglvEN7vKU2o4p2e5VnMye"
    "wohSr+ZhcnhRODb+Et7z6f4eEdo0vm0GX7KKn3yNP1jBDWx651uJJuWdHIwyha+5Dq8B8r6H79jDqdhNvoeH9DX+bIfuiAadSv4gAUCFK0BCgEFn"
    "4DF45Q7/Dc/PpDlE6lJ8IDeijSdghrgUIlSpJZhF7WTkZeoi2OfmcDOm8FBgJ2K7HangU/w2HCcHXuUTlJAw/L2EdBIfBY38Odyv3T+UYlz5Y+dP"
    "1zIVJtxt5FZ8eL7lKAxtR92ZeZzQ9fhedYeVVc48kxejp9jfvYjbvoOLuW82p3B8sPRUSlG18IqsCtX8oTiqJtd2pMss4ALO9R5u+Gd4Pvgy3nyY"
    "3bFK5C1Z9Ay+CfbV9WFUtOiJHl4pnGqrAolLLYgOz+zIbseQXBnuJLODDz8B1sgMYxVPYE0vCl+/h48ITzMnCNJqtjaQV2YWa/iGGbdS+KOBu3NL"
    "Xl5GYccLHG8ZeSscvHvnQeC+mEu5OdySddvJ+IcaL8RyIDs/eHYOx1kw1DGbePEhgoN1voKy+eKHq5ZKZOpKPdADR8yGLxtQgL/cOghjVSxGs81o"
    "3nzTVvFbmmxLjd4tIFkp4XY8S8OpAtZlX43HuJAX/nM4rHnXrWMdgpkRRRz3f6aZk/55pyhltIwcDUrFdL//iu7xxxzJwebcRMKzRBPdALfX8yIG"
    "r/cXwRFomo0p2s5C8dHOGNchIZl1NGulD5DW1qYfMBO1z9klTeFPGni7V/ErUjWm/LV9icueUWJdj2bV4AsoNW4pWTNTrutkodOqtY7o0ncPqZaR"
    "XEvCLi/yzoIWYUV+rPZehFnCtKYUeeyCbgjbfEmJVtxRvNP43+vyB9kQfyBDrRKLLVCx8e+vcQILeEVoRR8oS4X49DROQGsHznDKIrilrltSGSab"
    "gbSxFmmd1UBvIZGXmNxgx9LQMz4VKk2QGTdSHqx1ytmxaJIRTpwMRWfSYspGQyeDGedOjndt2ucOJWJimTiCDyqndHStoKX9BKVgc2qk28Il74k/"
    "ooGz3JE9mcdbisYq/NEUkvlYdvt6BqWu65d4YHZJ7izYdgEhWJA78WBcinDuDq5hxgB5SbXcB8uTG7ZF1itD5ln2KZB5KL8fElEp4DwZd022kalY"
    "g+gJb2siNSwRtxRAPXzRV7jBfMkUpl4Jcwog9nAG3yg9fSEwXnzQvQ73Ohzbg+qjJYlyuQxuCo+/BnbXggL1i9mZgvbTmpQH7Zc0N1WAQvEz3Cxx"
    "IyqYv9jaZ5i/4KUM8xcrLWGMTv3Di4SmGHYFCTMQoGMaOD/B/0NKWlVSjgnLQwQsv98BUmBSaGaAA8v8ODnOz/6X20IPa0Kc9OGMjzio3EHEohvW"
    "EaBgCDWb9WAIceV38ME2Hn+Dtk8BEipHc/oAApRCZ0YDWU+Rc9FHLJQr8DUy4Wl861oaujBvHyTctxGkYambBEXq7nwK1bDsuegqJLANtR6grvZF"
    "OaHbMlasdNr3Nf3jEixE9Q+HgShuePYU+GCIJeqSQ0gMmLHDSaxDj4KfqDjJkjjBl+W+NJKgigI6p5Tput5gBbuYZHEWfFFdtSVRdhY8LMb4UAWL"
    "0VevaPwFdtwyLiN+oy6XzgHC/d7FjUhfHovOGHmiQz/xa4eunqbBHesrlAHVBRLUokListZkG9AbyZO4KIy35UFFeg/4g/qAkYr5TcvVuiQ+mzv4"
    "iu0YTlLJ8MhBqG5dBCoZLDcFLllx1VKIk2njkTxS8HeCbAo7UDewlEnO6Z73Ce8PSWnXJX4lfRSmUVpPeaBLdI9aWeiR9G+SylUVhmURMxcEnsSf"
    "FCI9W1UIlkVSzToYhGUR8C2llAaOeTKGlQWZmowy1JfxwynRwna6gLrM/6pTsMtyJhofqmbz8eHB0Hal8IKngXyp49asdrJzJaIlItiME/pT+JFT"
    "QNZQE7vkO6djFbMt2zUv0cw1dbYlqg07YYqjvJRjNYAzO7U6PUesShII400lIb4k5GY5lVQAb9p50K0Kw+NBJAb/2UQNZ7UrhM4ql3ocREyy4URo"
    "0ReXB8D0zPgGryeJOOlMOYgDuS4YaJo/W73aPigcsI3XjKgkoTIeDjZoRvvvyIXg8e9+YhALyCCIa9/xHNAxwdbZe9bsbfrOdXFgyT/tVewmQ6Ms"
    "NHxooKbZPBiYnI2AN7RzoM4U+4vSDIxY4FRulItmdQKV2imf6MKKUhw48NrbHCr9eOS49w/2IGisFeFFPkKbd2TnbC9MOT1eV5d+Jn1iGZdwAOCq"
    "zMmYELSUdZsZg7z679UB6gpbOwn7mmbW+XmmQWFTNJ+2fv0oihCH8rVq1Fjfx+ScU3nsWBx1RhlEtJZpHOArHMwys7QbSGPN+iouSYDruOEuxuBh"
    "0GZvQpRpGWLT+oEZCUXBA+KQ6xqtthMezGpcKnWjM1+jFwPdmxLzuCZnCIwRIVFn2yrbW9HOAUFzo9PLZYVcVNIiedpxkNIyE/0bmweSuAcHx9yt"
    "vRzrCiH/g81inEYTIhkcnVJhnpZ8Yp1JwdrzrLVMjwlTFA4E95vXST2u1YNWuQuWat0YpGRPTsMPFSytYKedFE8BEbhAS+OW2u3bio+QN6mlLpGV"
    "OIdJtz88eHDyjcFWRC9PCYSA9NhmCWbY2ew6QxYuUhQpvw7opwJUOCPXY6JMEO8PgTGcsmUCXaaGdVFB4BWqxmFjEicyrroQvV4gnVZT7sSy1zik"
    "HTD+JKk/+3SsuKX1ovpwxglPlf+Q6BLOLaVSP58KgrG8MVW4ofMw5c0xl+8vMvvXEKpbc3MQtgJUWMS4Y3Vhi8MESPfbWEOsyol0SVL1gYtrJvJF"
    "+RDOhyIDdglg3KFW0QCOzgzta08pqdZa5lEaRCU5nSgoeu5dgyOrdU2JgFrApU2LPr0gyvRXpdMz1/6ylLF8KU7HpgsexPPIYirXNGu6I5e/LSTm"
    "vF2rPXec81aIM2m+8B0Pt2E7+V7Pu7AmbNuirTxTxKr375JKBfgK/7DmrM5WwVQ7+KMhcrOlnA2x8jOvUla90FAQS2jLWdNs5qTirOEOHd76MSpg"
    "OyIMV5VJXq+kJz8hr85IxzZIS3DxG74uaZdcLG5JRORyJRvK/XNbXtL6u8GV7pquq8hZU3555DA+ZPLY2euQonCXB+NfhwzlF+ogFxRDtYtvqWyA"
    "h5JN83E0lXxycILUbJ6stqosbd/hOkubDC1pTfkMX/+EYFYNr7jPlnJJ/kD3SNh+7c5DldMxu797FV2QCcFEYaBpujj1sLFT5leJ9O/Sg5DG1c57"
    "De2pXhLdYtGm7ZVgb+cHTEnx2r7J7iC6D/LSVOii6W5uSlOhsz/8o+sUDlyfFkvWqqlndkoIPx/YKbRxE0QQuwEUzwZtSr3ROQFo48ZhJludq1yf"
    "OjuFLQ9fx8VpTeXXXTxelKj17g2SdDslCVGWu3peIPf2HMB5F7USaRz0XKWEMkWyw9VGTC8NNcY5GsHWJHM9Qss80N6sjV4fVT0vxsqDdofDONSG"
    "kMZ36QfCYu+Qxyg/q7u/NOks+0kwHTXTFHHMKVV9MRZqnrITnpbUdsHnX1JS7gGw3GN/BeIElnizkmzneG2ny6GBvR/izKv91oF/qQNgePkqysoM"
    "TPmEep/tS1jliazwt3YGJp9JT1uQC05/75JSryxU51j+QJiwXuMdbq3CzNEeWmyAJu7poYPU7+/ekPu+5vFuV0Ef+NasKClJWPBMVMVAtMUTMfrd"
    "S5yjrHW8ZAmsqvDSx/tjAbuPSFxva1xgGxAHVZnm77IsuFBeMN1gJRkY1ht/SeIvUkXMGkFJBsVFEYXUYGI1XyZrp9TAP4AQgtuRuJoRz6kZXplW"
    "kuJLXVI3zrI0QNqlfN0BSw54FyRXIREBhVrj4uRZQx/g9iOwK/TmDb0VRERH3mRqG5roCJS4zy89Sab+5EqWA+FczhkvZRJV25LftcAOkqwIyaSe"
    "KfnQXRpWkUrsuqAKSnZUVggtw3oabL7GBRlkJ5rQlyIs67gG4yBzrOol/f4J15w4i6acDZ52PboEO5fG7OthWpWfVz2eaN4LCIah4jnkwRsIBMXv"
    "KK0tRiX1maz4s8Kinijg44ilTIQUfhHZLWVK3hZmEhOb3UW2Ecojwjq1W6cjBMjaZdHgxNWoF9qVnjvIRe9wiwOqCuYOqn58sKfwm506bGmlLvaY"
    "w5OsfoQudnjFE33vDAZ41D32t9IAA9Q0hNYesMYQJxH4mKR2ihEHDormWajkV1F/gGCh6G1cts3XvOoD3TPNM0rQvYE70cl7ebNKG3C5t6tuIk6v"
    "zzZP4e09SOJ4JXq8VWmMkuLoI6F61wiAR1nmbq+D8o9QWJdZCKEE8LktWe1l8w4tdcuOYzW0G6MiAnTnf3o5TGbDB1AnJEFtVMRzsVqAWT/vWgun"
    "zGRKvSOXbKuZeqpNhTUouhG01TZo9e4kzc9urc+u9w+PUul12NsQ28Z0oHrhEapBKq6u50evyJOvI8Y96V159aXSzFNnA/HW1a2PxV49C9uKPb/b"
    "BmD0ugmm23PQha0oLj5Zlhqla/DMffR6NPnaDRh2pLfnSF9QmCHUCekT46MDpwf7it9IopUxEIG++UroSwwhVScPA8FGTqfgQnlKf/1UrQRhdbSd"
    "vgAr60V1vKhdk2d1cN1yqSWNa62f40vx9H4jc6nmDX4x5zdit1rS81NlsoHWytQzn4Xl1Xgt3y5KRIJizDMBTdhYcwllBH7CelxQmBb1NzB/kV54"
    "ZgD6ZL07iA1eRUW0BdGGdjWIH16U/mLwzBB4gOD5cTRsKaFy8tyEZKG3QiEb6GheTS4dlCWHhKamCrRng6ZmiWPpj1XCOgVh6K7gizGtrseC0tRY"
    "CtYLb/QX/z45MEz1o4MvvfDcCd3VEff5PARdhk7/t0ZC+pU6qxMJacbdhizEmW8X2HPk16NCa5AOPmKl6bih3aifwz0ccVHuZlP8/Wsq1vQpLls6"
    "vPry8AQNaptsinU7/J6Yq8HTpW0yXYpGoqxlxNgxBbtOA7PYm24q36cs5yJxpBCo03s2Du8d131QsnsSOiqC9hVS/eW2bhxavZqdOzOJRr/q5ZZ5"
    "l3adq3Jhlg93vBBiafBQPHDmIo3bDiHJsltXu1jWPGQYNIBg/iV9Plwn5jb5Dc7a7uUDZ8ZDMnW8Kt2/fHQAWO2ABWRWD+eTPT0XypI05vUcqKQq"
    "cR3h8MCbg8MpHWnRcYOqXeLUK6PdUr/vqi745Q0gUwXGXPMzUIxzR3nOmokLc4Ikmoru8s9bu8r3TZQyqGw3Ri6gw/IIw8BHsI1Q+Ikt5JHy+1Rn"
    "A/Mr/LWr9unBx+E6GQ1yeOB3VPnw2vP/i2vl2eEMGF9mf+il0O4Zhaw0FSlvS08TjF+kctja8jjXBuEEIm9w2BuapxOl0zyUiFXLq4BQcVjXwNwI"
    "gIGMvzrsW14cff3F1159/eQLz5187hh1ROn9n8/+1GrbwPSY0x7H6PW4F6cxFnYPhvJhg8+OYONFGaLU0tT+1QR/PF6oMPJFVho57yQ9ZBFTdNC7"
    "4L4GDgjXSaEFVRcJEQfInEwvCLXLPRJdt/17Hnjdpzu4Cc//C753clw6PjmPP34ZEAlYX/aRqP8yrAVSEMwpJTow1228HE8i6rasXhRRcWmtwbFO"
    "FwDJ5/+tsz9mz0pPbnx8Eno40f++32NM14HhSQze2s4u7NTOvcjrq697tPCYhW+FrpIg82thoNJqZJxY3asniqF3Bt4erFUVJw/6YCpfS7hmVeK9"
    "NsE8WS/Al69epRsXzwTsHsp2bCeYkbfeGh46R8shx4CECbV7r58/4hrX37xCNSM+MUl6UbJnSzCHQukldCgrSABYdmUBZ6ixTL4GSO+lZWPWcZPk"
    "Z1n20F/UJXdgchclpiv5hmZLUiLepTi5DQh6yFNv2uoe8moLcw3jZShUpmKxH97JWA1QjqTj2Ffn6D+cf2tobByCQrP/cB7sAezbX+93qlFo8e7A"
    "GAN9ClenvjvfqNb9U6p2vaXaOpR5aLjgP0YjUMAwnoIbQsJ0CkHAleCu9Au6ZI2j4z4Fi2C0fpBrzxoF4BfPFz/9+T//rOD5Pu9+dawf6ujMjIuB"
    "SXOrx4YmhgY5GWNs0Gha5xLP/Oan+Y5zQV6+DmVu+73Qddl+p1AMyh9Ta4kuIhg2eEHXGAcoUjhM8mByGwo/Ye6e3EFbeEBx8SkARAabB1r1nT8y"
    "PAANG6RnXVMcdn4CWaIqoPArGq4jEd2W8C0waI0L73kaJW+VB0+1WWK3QEto9Hoo1nUScZwIXLwzcPrVE8+8PHRu8vfBdtva3SlbNFGMn5W5jp8F"
    "G8BwWe59EaUdFq+RuPnnvmef/ceolvv02HujEyNvjw2Mnn0vCA8mMaxyrcSuS8iRwMJ2CknOKUlY/Vrcmfqk7JY3xGdJUmVauGVD+jleEhbQIJib"
    "UyIZu8HP6MRjTRbkxNiksqWd/V2cOPnc6ydP/fLF11/sm/j9RFGVpBvZG788+crLdSVantpdgyNphEeIaqJXZSkZYI0kTduj31XZiZ1kLrCd6LHj"
    "rvoR0nihWejxomz6LsSkCWBRqHQhO33nVYJ3SsS4PNshk9AWexX3pP6HMxZ3ZHuRExy167oofk+dfZSr6myp/JKgKUwYGMZ9fHPgzClZl96QexJo"
    "mBapqsHzvpZQyVTx858VqtbM1UPZ8qtcbv2UasNdKqdgC1v4TvKfXLR7yfP/j6FREXgqjSHPSsOAuK5tjwPIsKQVybRqqH5jmpaSlww6P2RbF0t3"
    "7LpNFO2sjyPSDJnLVe2cyjN/A9aZ7D0YctmckWf9ewH8Sig+g76QWgVJaWDOH31RvCjks26JlijHkSYjx1GBgVeeRsQUg9BY3NqbDtHOktSVjzlg"
    "4261wj0ZMKrn8LCTIlNCuF+LH9RuT8VBxiIo7kuc6II1Mjkxyl3l7ey3U+mTTndiw7F3bHB8cnii93+w4LF5hGXsPsoJWij+8xnb27hXR93Gn9Ec"
    "REvJJdGkdChIZwuqjVdpzoaznZqswnhIZMxkW4GNQrtrMRwaBfJoi+BmCY+9t5hrODRR0hxteOgdYx2cKvtV8U/HKwmhqtbMKyNTBPZTBk4qL6dU"
    "GeRefDebPjZGhZtFqjVdVUGiz1brMTKnb0qRgHtxXAJf0nlCLv2z1VueRmgalBb5ZRNIMnqtkFdcYcWcSHTx2dqEdpGyHWVJeNk3dYUSKIFnfgcc"
    "7Uw1qlW+u+7x4iDVKoWXiqgUi5zVeku4dQ5CUnbS6Wza6X1Le9sqwAIpud/cibODw6Mps0yllUaGFeSNnjjxcuHZ037CXqlXyMN4+6pc3wRdZWLg"
    "3JmB4ZFzg9I/3uroyjPE1p7K4bX67IEMuvLp5XOt655h4UyLjEbHftNnNEpFakkuBKTkX86ytxa194PS8XUFinRWwFQM6q9+auicC5BplT3ZciFQ"
    "Uq10cfBOSntJ4EUbK3R8QiFUfdwFksGhHF5Gx3QVp6vSX4Fk3DJyiSnxHl7yKyO+FNzjpvJ/qKMNJXogYbeRblp0b94C33jQu5PNxVOGOw6dtu1R"
    "6yTLV1YLBQZfZe1D/T1OJM9q9fu2asbxB9GvBkfF/OIFTjFVxS6zpFfLyj2tw5Y1Ky2qYpkaJt2GAEpspCBFzl7uuGtXzhDUdRxTATyTys0AVS+P"
    "DGapM4Q0V5Hq4A503gVaeUKSrTGTimAy7VArhdaqz9Yfc9+TQ8IQIGfAF9J5Rqfg5GfgTmlaegTdEW4JrlXgdeTiFETEUwMTheofS3t+Vwn/6G6W"
    "bn7/gZScniTdl+g9oSKpW4HOiOYrLcaUFqISLqO6lU+UJ95ucPJqxdGZKJ/sfbCORocRhv38kVekH+x4FQibQM1ka6Q053Fo5joc6DhmvrW6FErm"
    "3wML3g2jA7WK/OLCvqNeTPVY4HaIDdRg4IOn48aAPanlpZLgwy10MDxlNciJyvyOkOf7iw76W3sM8gNGCtjT1ugl0eC/UoptwJt0A3jLrW0WEImR"
    "2zZ98XVB3BjgHgpWsc1JJOtpq4UWEdVjzuUuZH+hm6/o6taK9qKVeCQwzFei1C1EZfqrUlFKR81JWNxqH1K/JOr796gaddOVwbAB++NjRSIr2tGm"
    "riPVua8XGVk36RlT4v+StDfU3U5sSX1ECUd1W4BjhVKTdNctWpgXh6zvuAovWXEUK3mOFT6Mt1U2khcoWeWtK/pj75+9N7ej+o8padymo82qwboC"
    "aHKpfwKYFMUEFNcgh3u2ttKJOK1a5tq9a3TJ1P2orR4G3SNz4jWFUVOmaWsxkNuQSOkVAuuMz5OW+ZEFAorfmGT0JUWu1Yzew7V1vpniDfvNG0cC"
    "Gs71rdKnHaRq26J8u9GZuFrcBb7CJCjrmpF0KSQ7Q1Zo14pKM4LP61QQmRY6FvHGEY1bDpvrucTKpxfc9hqhjzeOnBkcHsSiIPNeY82Pv3EkBDoO"
    "fI019em6fK1OYQomyzNruah8nWVtZBJFRh7vTkkotbJasQBp+OToNva+lmNXpQSz5/e24cI20U4MN+cvITJrai0k7FEl2JwaOtnLNlK22VHOwjxW"
    "+JexK10gl92cldmeuL4uqtj9VNFYaUZCqUJszYGKveiu73T9u1LSXySoELMSYg8nal3STkcKL0eSsybXWAZQX4XJHlkKSYa2qC7SZdGwabLWL2UL"
    "lhbxD6uj8ezSvZYPpcjUei9yM8qFbjXmxSVBJPLTQUMwsJpC87rMx7p7Kdw/j1sOcfFXoJ3Z0Hh9aPcUSXaNwdSpbyxkgReleGlOuNkCJQ9lHRxJ"
    "qRe0ErKyY06VgnzFzc1sJxc2jSzXTZbtaAT7iNmV6o1aZlNPxgVRMi5JBpHlqWUlQ6ntKNFLkg5rLcesmqISBhPTbgY+4Wqgx06OpjO4B8unk69o"
    "4oatJthiIrEr3ss08615uM3Icx7ohQvKrbgsl3gmvAh+jXtRniLutc1RKoQ6Zs3W6zdlSiRMZlFJBIXZ+kvSqIVxZbQmS3d4YJJQYSM1+xgNEe7D"
    "nuMa2V4tXEubRLZDWMRYjhKXsDuC043pUbMTrfFkGuDVNnOPvP9+z5Gzg+B1hgR9szlP1p5cfbL5ZOFJ22zeu8T6zzNaIHzdeDL/pPmk/eQG9hQw"
    "WhnsqHlk1jzSgm/M5y9D7S0JDkHEPDMIwb9xGqH1ZOnJF08ahRlqAf6n+WT5yeKTLfMPePEN1SDUgRSZL+BnK4V5fg3fBr97bXBkdHhQMEFw+HUz"
    "SNP8d8G8xPyoMOMuFU+uPLmJL8CHJt8cHjpN4Dw0oaZ5/TzMZMP85Kr5p2zACS5aRXcG/HbWfDkPE2+bP2CwX9o64eAnDTPEqlkmDQYJUL8ZGnwX"
    "y7i56zBt3Dwuuw0PbODE4acvQeN5Wc2CGYVmnowM4GQWzN7gGMtmoQvmMfNqTzNXm/bCIABgvukh+OIQV2CyMMgV89ZF3PEV9ftx73ewO1SIrKtI"
    "zMPrOAOzmUtmMi3+aeIamqHWzLewXWbmLbMVS7j2FwYRmYI36OaTa0/mYIMyWon5agspA0dZxj/mzMCbTIuB79n8eBP/HzdLPQuNQBlg5czQ+Onh"
    "kXG7u1u4oe0C/7wqm2LO3WzKJBbWnf73yaHxIZnyFTz55pNbMJ+rOJ/NyCfG14hPDWlGbhTcmRArcNBhcYwFK5K71y4sJZiRewqe+RbdgmbZyrGb"
    "LUFUFUdHhqEgnBpdQBWTOZYrcD4LONBR/F+gVPMhjL5SIKG0n2xCKZMHl05lrBLLoCM3z8F0ljShFshV5EbBZKQFUHG0t1d677i5rOI9aflfamg5"
    "3JtBLNJ7z9AollPrm9Kgm9LiXWnDfLbwpm4hv3hy3RtOle8dhwYJ1pYXhmhHxendxCNpPWkcL5C3rBpKsE/QuGH9E7xBulYMMAA4VFIWR89TtT/W"
    "k9kb0y4SrwVK+wLuEMxgEcjUfNEbj5OegX27FIn2FANvTTB2umphUm9Cai5Xe2U8c/LzwM4Kn/bnkK17E4TJcPOZoAxwbHBgfATL7zXdN8w/FpDX"
    "LtHi4Qwb6ufekGFp76vPn3jtmedffzlRmeyPrE/XXAS45yvuafO54puwjNFB7K9OuAIADjU5+vbYwBlsLjZIn9i6V/M0kGTbjE90s262FgVXm/7V"
    "wo1u+OPAvGhbC5ShK3rQniOS9aY7dVsoOpmUm8IVvNAoA2jV8E5Yo9z+fjWxRq/3qslz/3YOWvLpV0EDrn7ovGXraGVCti4QXgvX+Vqh375EzAW4"
    "4lp/wRutqYZoxvznCnKxNnyGct6bN4A7jJhTPTMIJ4EdaHTPL/gbICEHHXSRDT3/xHwzPHL63/pkX9T7m2oGa4YVLuMPzKfHhZxvEs+9aRbSQgF/"
    "A+baMFNco3uJc23g7A136APlAHLiXnr+OQRA+cVzL7384gtEf1eEo1vK1pjY49gGocBs/uLN96DVDlYmD417a4GWxD6zYqFLDBD/cUVuUpsmDNNd"
    "ZvWFObaRgqDa4OwXQb8qeIIs7mD1jT4u/x4enKCWo9hZFKYC+GyA+EQzgTt6o8D3NZ9ch4cbeJ9xnJuoGW1imrlhUgPDoZCli7ZFWuQSEmibznsk"
    "QsiwCFN9VoTcRAmIvKqN24ACvm1OEzTHNqzhXwdGSQNbw3n8imGutMMdvl82i1+XTdqS0WGcJiozoPcWw0Mk/zZRHFtVzVd6Xx0bensIm/EOnj57"
    "zrDl4YJKla0m+AW95Qvz4E2Wx6Jj0T/BGV//YejPRNfW7gtfOtxJ/tD8/VvS/Rb5Sln2qbYTmSJ/qxr4eQIbTAPO3CRVjJTdX5jbRzt5Bc/w5Ahd"
    "OiD0FybHrCq4bJ64jooUMHXiHKCuNzDyNIlBZTwM2NKG1f1oHiCI0e4gHHZbBIF3cAtP+NdedQTN3HIY1L5Rt6HR2uYLUZ9OOKJGAuYEEvwl6LUb"
    "vNmvJ7VW3w+KE51FPqF00nHRREGw3uTv4B30iqb5/Dbs3Hs0D+SoYWAmwb/8kB3eKHh0ARV2LO5A8qLdNCcrM3Tq9QsJGtP8ydO6aI8Z/z2nwvMV"
    "Av4AwhAu0cuDb5k7h3U6uD1wcb/Ab04OTQzz1FEFxTnB1IuXXqDZzwFfKfDAFpACX/z9wDtDbMzCbs7jNrw69rZRU/9jwOnwm8bwIFX/tbGRM5On"
    "kb/KDED7JDEIFwahyqRDpLKplDpQmD9ZSlAzPmklR6at1ag3fmJ+9oUyRpK/0obIL41dAGcI3c7GBk6zmr2MRMdsZtXeCNyafxkZGGMKZ0uVDpmP"
    "jjuL4ZbN4yV8nrk5XdolYjOUIOjoiI6VfgI0Cq97kWtAzEfX0G6ED5/j9pycHMUtbSBNyolFbX6e4Eo1tOCX8ab+AtVB+kxEIm+Yvig8L7o9tLNi"
    "SA+eGRogApll6/x5nZtixm2JYnuVPRtEXCekOZkybl/rSERp1CXsaCQMykofUqbJGn4NqqxY0ADlN/DTExMjo6OyA6CDbHLvjLGxydEJ+QKMqxbZ"
    "qoaznUMJTCMhC8HvTtAMXGcYPvcF1KZ6bUOXXxjb25ihZ9wdZDqQ6jVR8sboOirlgC62/SGzB/NO2+HRtlf9v98UkvBh/nQU4m6P+F7E4O+1g6Sf"
    "NUToPpRiAfURin/SFf2kP998RsrUvNyMb4Y/8etXThAByz96jkCjD/RGqWlQJ17ATDdfunFwAiJLwI7rddOGX0qDX/MzSDYqzsPs3pdhNNuEgSwP"
    "lN/RIBat0/zGHOcEQffiCErW6G/pOcb8hD44bMkbDXloTMaD3jYksnAoTzjRIZmZMZME+wk47QJpee6lZKjhhp4HByQiQJkraPgYoVaRtlCch79o"
    "2vIr1h/pL6NIyG+89iy2AzL1cpb+bQPUJfnN9/VVb4r+S2YlaoZNkfKF+XSTtFTZ9gaOg5QBI1HDE2nLOj7wbuG6xWmr+s3B90bQkzM0zszd6Oe6"
    "9zA38ukTUTtLsqPBGrp6Pex7yrzWc8Q7OI/y+iZZ5kqOGOFoDG963zHQea2hBs4mz5fDXivWhgokNfblXBGOJX5h1cv5H6hXXoafgn61+hNumweA"
    "CvBapNkRVB3gI1BH4VH+FXwL18EQeI/zkuGD1E7Pqab8U+uPaYLRSg/63orIN7bA27fAlInjuJehuIVdGRGN3frkcu9uBK8kExr/TauzDqlNVCf0"
    "7VcNvdlD4dziESNAaxjsKXkE97vJUvrXXCzvnND9BYCcAiDUxKBg3cD5A/bh+IT24ynFRrzW4noSltzop0uzSH56dl4XLDCAB9ATWi/Srj+WC05L"
    "0fMc/D1wBdmU1EQTM0TXHmo5Vsdx0yWPRrB7s+g7aAl7aiBVXyFmthSoJtJpHIiKSFCnrmsriQgvpeFQ+IMta/gGLJgVRbXkvBoafBekygShscC7"
    "xgbPUIdR/7DIJ+9thfKTgSp4U17bQC17ng5ymXxcwdk4JQcSld8ZGhdBBvK418ou3Dlcg8jR004fbIiFUijV0FoIpYNq0wH1wMLouOcgHDFqFd0l"
    "mjg7K1DDH5rALmxiHM0WyPJEAX3eYugWb5mTEuWDxruJigb6O7TGDrrV22NDE++JDmxtPw04rw/SscMXNciO1Zkp+rWBG7LA0kPoyYiGSWsojQ+B"
    "ZuQ3m+MrOTTRJ04idWqk3KEbDW/nFp/5Apmzc0TWltBgj28gR4IB+ngq4iNmmLOo112AZCUgI33RLiiPe5Ms6pjWt9Djs2zmsEIHuZmaxrsD48Xp"
    "sUHsZchtZfHWp/E8S2YCm7FBXk7wyi2BXN/Ew2gXvjvrJnKKm+IQWxZvAXmImOuHsRoSRD2uiANu61uhcqnccIoD9RRaFikVtKfwIyZN96WvmPqd"
    "5RPwZPrr9CEixoX+mTkY9BxdRXHVprPbMP9cUxwte5Y4qZpAlXgjBwQX5znq+gTH2e/68NXqI5l8I64jfCNqoOjUpnCF/+7O3msENwuo9x1W5Hm0"
    "BtgoAJltf+KfvPzOO85AxWExnSGkJh6ENllYGpcDYVEn/3dGB8YE0G7AoQb5MC7es+Hho7rG3htP4CvKUXTD9jzy5Iky4A4puFCKvRTyJNE5vKCC"
    "YoxzpEQjN6R4yQIFjJQB4GmnVnXqx1gnKQDL1lmuUhK0rEjDsqSAkD3dw/85+hKbEnnh81X2uLT7dB0WMZ8BrDUb4aHYmdmhd3wwsTS0rfcqGd4m"
    "R7BV50dg+gunWl/B71YoDAbuJ7Lw7DvhB4ncYXO8HggdrQX1XEcRiSCMC8EoMUpnFp65ecuZMdSYoDp9vLBeXjyLscHhgfcQ2JvdyaCqLBT0hDke"
    "4fhN7fBzj9mLhWIH2r2e86USoMO8NTzybnFe/npfZDaFhtmhuEbhqzYKpAUyNddwOrMSr+ap6JFyoNDG9uCkmOI8//G+h/OM9izZOai8LeD+weHf"
    "IBtCUwNYMiqvRg1pu88NkhxMqEKsCBVuAehThRwPVBMnDIt8E2KJsOGYMjQw9l7xtjmsUYBXhS7oI9B6l9wRve+C3D+HwRjDivqKlwzvMtv+plEk"
    "BwcgaYPBNt89C4t/9+zI8GAvP6s1BENcYFQgldmCrgFkN+OTp89y5KjP9xwW1slNEpnC3Jxf0cJ/bohIv4YZSPbakP8Pd2EN6ZOMXwgTgSYCNjra"
    "KovEUa0Ls68gwsZoPpsns0DW7Axogd/nCpJFieqyFYxKzqIlIOp1NLCX+hW3U5xyxcXHGvDQHGmIiePric5OElZ4939CmG3WHTUx8G9ykOMuAouI"
    "SuOD/z4JDN1Y+NRmmY8WWqAjePk4AApA1MWG9iBtwijKw5OUcjYsEE3E+kYmwZMO32IVopl03ZPtKUoOtuk7s7wNpshwkwzPq5KM5kULl5lpNmHY"
    "jSe3OJ6/KKbXLDKbRoGHDqKiXbgYKYkOVEvpLCVZgP51w6r/epFkz85TcKMvyT1AGWAOYiyzccxfOA8+gvGAgeDgazBNkgKKnTQChgL8Y96sfNMN"
    "1XPkubTeLklkoI/56riK9mMwDTtroU7E5lxgwd3ESUnW3ysv/eqlV379SvGLV18vZBXFKy+epPdlp78kbucl7YMOGGTJ8LD2506efPHEyRdfKJ5/"
    "9eWXX3weQ/yv//pXlCyY58L6jUY3IH+RfStuqkoO8C6/88/LvGAqv36tOPlq8fqLz7/6+guFUzVe/YU4i/y9aMQ7ESy9XYh/0voknQITOKLAiP7V"
    "yRf/9fWXTv62ePVXL/8WFpDctV+9elIOxlraBV4hQ2a47A5IL7Djf2WUjcJQ3Sgl5bhqcPShkJp0fmQUyel9l6dwlTzDV3RmDrzwKt05NwxaGG4A"
    "P9pDMoXJlJhq00s7CH7/9sDouE1BIJq+6v24HiQVLSPvEt7C3dkgH3MDj7YNf6pTvmr1TiMfMwZ32OE+SIYjObUCG3YrbW779zut1xBAt3jKU5iH"
    "GDaAxDVRw0FeGHEBeTJUZK94WBWx6xvXYGJfsuR2o4TckU49T7IscF7OckH8NMLe8dOWpEFVA2+WavNXndet0Qtdh0gJSNksxyu19IqJ1DTuu5hW"
    "TSNepYwnAGIx97nBXgyrly5T8CnbnyAbs/At1xOTo3D/QOuwFj/m0wJWDQO6MAVL/jR7/MkJfb2HrAy2Sm9i7HSJfFMeI2uIQAPZGYB0owrOvfDJ"
    "22NYkkuy0DyBgXTgX3CnSQ+C6Wwh0W+JmxA1ykU/nGQ57Cye4aZ8kLBU8Y81CWxsUEJeH059fBBENrr0rJdBw/hAqLOv+N9nRwqjvJ/hVbEfcvws"
    "HCsv4/Tk+MTImaGBc5Th1gvekbERicb0mM9GJxw9KM+F7xuE81xgX5UNsl0Bc78hdNmHKrFb/7z55wLo3lfdMHPiRV/HI8ZYm+MUSPib8jw+YiOg"
    "xJHXUeXcZLGw2kMnzrNaMD+frfLDkUonSGrEKgPwV4qHDti9RkoQd3LCWQiJg8XJs2bzwQ4j6BM0r4beCpyHI2/yUQ5NdASo2+eLp6ZVKpb0BczH"
    "ZZeQvK4qFgLnyU7tqwl3cx/8vUJuH5v8iIbUFblm7L1soT9gSfk2lqi6IfYr9dgAMeVG3eZwbB82vlX+DbJ0BoL7+zsK68RoggknR4EL9i8sJROu"
    "2iBxXtyXewJ1yFc7gAPMYOXvjYbQOf45Sl1FP3aL9Pi/Ibx7Fj2ZKfK3wRTpNoPLfk18jFtIe5sYDenFmdpHeaZ+rp56cMlOHiW1SprmmePgkox5"
    "eNjwZZ7KKOLsBKTvNIOF9GTEMPqoy3HexSGxZjlhMEjz6YG18wGlBiMOrqSJ8jCHvOeQwNQ71aKqV/FUsNHR3dAm90cXvPOwEM4D6VJFvZ50uUJ5"
    "92k55DOyLIi5X7SUTy38ewcvP5yYDLK9OJX5eHnaU4vruxqem7OhfTpbTtLjTDbN81cL54PvK7zgT3gB/bAHa3SkXyxwJMTjGs3e/EayFRZcW7uV"
    "PwCaN6ZggPbKFgD4LFedJXvVXVUWZbhnLhnT/GJO9tg6qfqLcJwtLjduFuziWHTkcMMaQ/JOm9vf95TguA/sJumVtyaLlUAPWCbXPzDDBZ6R2bfO"
    "ILO5BHpRpyZcI7syiGbTAtpV2NiYCeRC4K54bxkTqZpYXJCHvEYxh0lWV8v0zjyKtX0789x5UcuvShY6mdo1QKr9obYw1wOjLF62R8Nzo6Wwp32D"
    "hI5LZUMl4KV1/vY8J5WHKNKcg3bFGc5+iXgIHI1racpqaPpUKRzjQIu/v41xd/bVynxTQM8YaljQuiUnfMGF+yKL3ewqtsiJ11D5fyXAzLq+T+tD"
    "HeMu+xmwTwlv2Suq72V4Zf5LD+3ljsI7SDuVYmIaHbe1ifGgWUk4v2lrgjRIsova2arwp4iJTGcu29kuNBs4bqsDWd4pZZblZ0/h840mB6k3kUC7"
    "wTQWItxARtz28ooaHpUlMIrxKsFlWsXPcayDIhOHYyYrgNUI7qWJcuCu0IUPNgNWUg4JKViP3UAyRYXWSD07Bn6+Rtq8ylY5MByw1fduEi3aGLpH"
    "sj9atN/MWwsb8WDxhI4sLjxsIR9fodSCrWQhrr0eWJjNqa5b7A1itaXB4mATqeiKi2xY7q18z0RWFKmph8ar0ovdr70a/Aq4XSbh7lF2s7ZCx5i7"
    "kByLG4NKEGgO18BftRQpczXgdP1GKKpPgk5p/vFA5KZaMiAV3bQ+xVyvBzznenOTJDpp4WPTGBZC1zrpf8nJpgFqUUncIJcYJkEs6VIEMNH66CQ3"
    "KOllDU2QBc581pA0ZMtcM1PYpOGWKL6RtPpU1UYfcDwNLWvvWNPDkO3zQGQlqONDx6LF5+HF0qwSdXXosIaVzPaBH+Wq6p+ANX7EQewnm+Z3MYZr"
    "mEKOP2fe1BdjsDqTDzbFB2Ht87ISpBlSLyKtakNf29KU9ISH5GGpojq0ADyxZN9RCq6TprKE59a0SosqPVgirpZGTFVcDIefY3O/SbfB8keeDchB"
    "/B2aKg4PNZPo6rsHrUtM2AzYxLMW5BSvBzkRN8PaKpvTY3XpALhUzfbnP3OmwA3aiVWzyA0b3pbqFy7NoyQ265xy7QWoqND8o8/DGKUGDRT4oy3G"
    "HXHHgnJL8qnYMlngjxq8uUQeQBt9CiHUL4vyGmCgWzmA/dQ/Vz9ecrVJyKn6KKOyyQo4eh8oM29DPOnsdKCMBVhxeUMP285jmRK/Cml/oQE2RWOz"
    "OXxcqGLP1s6eJ0i71FTfW6/DMnI58Zv1BRCaYrj3BbumMrKX6BQt7KUaXm+wiFI6WUMySdBL3LnZ5JWk0xVDMY9x2VeEM2A1Jjhx+EdfEsTSvxzM"
    "tba4cwgBVFq2TxCV5p+r6C5hRxIjTqYqhXxMyugXgEepW985247DNuzauoomDczCEOFPjxeSpEb+CWL/Udq0IEfK8bVtCy7a3K2AsBqia8CBrRW+"
    "n1pS4cz7nz1eJLvK9CnMxohmGxxsdNWedoA+myi6xMQMserVqM5vjlKAlrVYUYCJ/j5arw021amRiNHDhndTqym2pdcy7s6y+PGWCu674iW1N5Xu"
    "01ewgCO0wj5xA2+6pt/u5K6ZbWF8wn7NgWykbpkTSNcUv+8LUQaZX5Ea0CMN8ZQ+kxf8WoxgC7wWMRhZNoW8b+LBNK02J7y4bcH+KIgm9zpSiagl"
    "B7A9oOle/T3b7TxLTn3tSyP1aYnK6bD8AmvArBOza9h+OXhRBX8vmIjTJbJLZ67vclE2Kd/MxmSWkOLmWWdaJC4pYHYi4CIgu+CMvGi33yxJMSnl"
    "OreT7LFGXyMswGQ+r9DlgtBqmWYUVQCyULMj2J5P8+4+NF2Dl6AGYZl8wWTQKFHu5Ch55gXeTYuuOTpuCiu4blPqZObs5fQ2oU+xy4afg6u6Gl2h"
    "pGyVPicS2xaoNHHEDUotob58aIFcoeksSY32qtN2EihoUsZoZb+2wfNRKxUS7ymiZBddQrCkPc6O28AFCfMNlnUGyxWbikXG21IidaSvDtKY7/qU"
    "VhlBgomjOl2WiAnsQSBMyhSbOGqTMpkXFeX2RLGzZM6OthfU9YrCbq5Tnhdw64sbfCx61ydoZ9Brm9I0XFIXcZtU38p+r8xWhecXUeNrAAHCU9do"
    "ENvzoy/RonRRe2WxXHVeTPOrxF7Ecd/GivtGr8o/psvaivOAepQxEdjuuHIbLuAGjtat3RehVP2AfK+L1MxlvMENq56qNCl66EYhRRZ0SmuWrrjx"
    "TXCTruoyDXOAfV7PlmXpzrFVkcUmTNCq46vCg5sFl2UsUaDKb+nYF/eOxdDAG0dgm2+iunvFlVnZC0u1Hl+QEVp2w9S+rzm3yU3imdyoQiXX2Tpu"
    "5OX9fJk96rezWxDprq3YvqDtWMM1HrNcXVk/KlF+SzrrWZJt6OT4LZw6Zkv5eUeaj9gKnCLsRGMtQJfEyYFnu/plqtcSqbP4xhGv4d8bR/pJSlpF"
    "dtlNidQ4753yUyR1v1mb9RAsc9pElSjIUaE4g1fLknUtgTv9VxV2ttXLc9WdzV6Mobm7LcOue20ye+TkwgWE43oJEX1RK+uCl7hZJnS9TlFbASFf"
    "lSJ7Uci9W71GjsFZVZVQvsmpXd2QlJM5UlTnVAPzvqDtH9f9EXHEicTXMG+iTTrKTa7JXcCUipJsllXcj6sJRY7TbGjYK64b6KwuJU9RqncJ7ZKu"
    "iEVX3aJbYqHXPC9N0KOCgyKSSb6EREM5Pg1KzeakQVFK0fsCf87Cl82ElNM9Vdp9RWnfcEtdnmoVt+9xc4myj1xbzjZ1eNlA2rhpI/mFa2XY73ju"
    "SkBwzYBqG7gbVyKGri6wmVK4vC3dNhG2YZXLeV1dVV+N/rZiG8yKA2wRdegbsfLJ03Qef5QJpJbYamC7NtuPih/ryzSM5+4wlBPUtn0SCuniRzr+"
    "lksYamDjwYZr92q9nKRRcRmOS633LQ9ER3jznEJH2N+4u7/xaH9jen9jx/yRhEjY39jdb30uv2zi39/sb2zD3/DJ9n7rggZP2N+4vt+awW939zfu"
    "77fM4HtVKAr0/v0N89y9AsekEbbxdav7G4/NJM0Xl3Ee8Bd9dk+e2g3eFiMu7G98jL9c2d/YxOF3zShLsoTP4VP4eycJwwCvhd88kB1YN683z7fx"
    "H+b5T/c37shcdmJQBnzTJs7R/KbFb924hRPZVgOZJcB3txJgDfi0WfNOwVuz8Qi3Cj5r4wxoHSspGAec2Dr+dg/fsKtfSl/cxdlsmImm0R3wO3rH"
    "QzOFAlf0WD4i+rhOTwvgw/7GR7zpMPT94JDSyNDwA9rqR/KGO3RgtLwiR5E+dBvvtXyNRJqCisBxaAm38GXrBc6aPmpasgyQI/Cxx/zwxi05k9ZM"
    "GkgCqK/1f2jbibrvCOnNIEGad+1m8F3gBXT0G4UmnhBcQt7Rxl/wOSahr2C4abV1j4UW1vHDD2gT4lvonV4Igxz9vhBWMENTSQJS7G98qI6btvtj"
    "2ZEVTaT03cNSsAo5lXW+Xmo1tOR5GW0vhnUFsrpA9yt9q7qAs8jRak8BF9Et/KHH3Ep3spBnrhNteuxgD39pnlkkUiyFwsCdbssUb1vq38Q3/LE4"
    "ilswhYObA/mU5kiL2A22pxotIy9I+LUV997ySrrYt82/6SFguW61OawNRUkb9Ipw42DN9OaOoTiQY7RFhmzTEU5lJ+0O06fQDFerB92RG6CKXtyy"
    "VeEsfAynO28Z2xRd4u7hPvgz3KdtOWq65/nV251jMmOygP82cROBRdBD61Y6Bmf5VLBCDjThFZEq9xV1W9qne9BWugEyBJ5cr7mEJWuGh+Dud45A"
    "EowpVHIrQT9WGaJF3j4EaJIO3p69tEm5DXth3yu630yneCaeHOI/HsvbUaUD0bF5XI9TyKRJt90Enr8u0hsO9SDoJiLpVnCt9ug3fbWOj4k3qUgy"
    "/H41cDjlAyGhgGhnDXuTzqtsZi0SM/14wMB6WOJ4p6/ZZXb9tW6XI4VDglVRDGHd8jVab+dzOl6wssUbNI/8d4d2JNRktCVGb/sCtbU/ko1ym5UJ"
    "lDwf4etn9m+vZ0FaElsuNzG8991Dt+SVgcRSt31Vdd2yvxk+f1zaZeIOwe484g0SZtq0m2R+uIC/mqfnH+CLm1YgsT5PW1WJAJMxhni6bWEYu6Lc"
    "baPuAnwDd7Q1IyfOvH/aGiVZ0Bg8zWk0xh6TPfYhXqPHPnHcqoUj427dxmwgo+8KAdEJ3Apok4hvJ622Zng1bSpB0hRiC8Hu55FpKueUEwtIGfeJ"
    "NRBxzNmrF0HaxI4Fy7R3WIjjU6XgNmIl7WiW55EXH5LiY3etTXcyOWLn4zgsnIARCxqO/ddv2aLVBslUBI1TWxDHsDmd6N4+qo6cxDc0U8bW0UxN"
    "EHaQo075GDvwutYlIZsvaHkacsexTtwygd3BPb1l90cB79QkctHCAnQeYRIP8VFmDxFUDx5X+ocOswdJmjQlftEJy4kst2nRfv7CerGcjyppzI8n"
    "Vxh6bRTKOTO6baHGRz7GT7lxH4zL+D+BI40xgKx+EEaW6irT5F1xYTqczj3lg1lyKEEiL3YVTBDpIzRrDygovngnPG9W1qpLYQfh0dvju6t29nEt"
    "n4yCFpJ3gs9oA5+atfqqghoS8bEt3B/2zEMdsrtRiDdvlchKQQ8Jc76g1tiMcYicdN64SWfpgxEpPrErCtSUL42R2unZBEZR7EhNKhG38Lt5Ov0I"
    "wEhcKERAKwXr60Lilk1FmEaVvqz0OAnII58Xb8pZz1qSDVwxK+KHVm+3XisNkqQP867y36wqqCRkO1Nk9PtwSSUqCgMoadXAg1EqIWuFrGRVZvae"
    "0D5HCEtJQ09h5AjGUk6B1JhLSa3WoS+Vn6lCZAqoJmKahNAkbHtVm48hXJMKobS1bWPfaVGbrFs5C9vUgZKYRnKq1Ls8YrH4Tvgea2c+kmVcsIoK"
    "hx089Cf8jpbZihCg5MEvJFrDJxnAQcnPxA0Kf9OQmyl8KOuVuhwuRUFECVU/svc3BxXlPkyZUS5c1jFkVKX3dIUdod7JAjNPRJe6BJfC479EZ+Mn"
    "n3mahZg3nn/7QBhTxAoK/Rb1S6sK1YCZsiNFahyubw8/Xa2JOGUHC7Wgg6FP2WHXOZAjGxq9JjAsy7yonvzsAp8K77MdcZ0+crp5t3BV5axOM1F4"
    "oBel3nbq+GDUnGvZixEcPqxVHGr0XbXxXM+9b5WyOXsoPcwynCsjoS7Q6h/iQ9+k9EGiFYuC5dzHZHJXIWKV+NtceIrjZLixn6L42K4RnIlhtMoP"
    "n36VBdJyE9JXBvWCjdmukLUCjtVTdp3cZtQPzIWWYZdAXDhT52DIUIC4ekuZQsfTrYnhxcfBP3G3NpFuQWMfDpBXXkbe5cwHdNJnExf6izBfQXHe"
    "xzgWaWx3tX1SVIrmdFQieV/YpOcHE6dwaJhilbPOGApVu1dvpXuoad2lPxIrr7BzayOVpS2Fsth709KlNaKc57jTO3MQpDOdMlK2r6JOw4ZukO5M"
    "e9z2LcIdPMXrNhhzh7ecl/hIzn464PXOhcJZJWSxBABqsiV3iQ9/qJWyAEHNU+PK3R2ZCxAhrZXwOG8mCdC1kiDDilKjN8XU1uG/trXINEhb5MW4"
    "rXyecAarpahtsbpuj/qh1v5wtTtkTmg8N1zyHD5GN4f9ch60W52sPqb5BOSbPGdvEZuWnu3fPQJcKsTF8r0s9lWp/ornhMWiFxir9Lv5hEja1AGR"
    "5To4BLoLOwWH71KRrr30Yw+C0CvasHhaLc4rEG47V7G6zgHrSg8EZDGeamYApzbcczldON11duojReT4LzE3XEj3wHZJd3/9jC6nG/YUdfIaHdv1"
    "OGRoSD8FTLzjCRLRkjvNILOykmSLhFdtyoPjnM6X9SPB0sNV7kXvDN5mpYGn09JiHjxVbL2YEt2vg5BJBcZeLaumQuENKfJw0Phywft40BKarEt6"
    "ab10nbMPREnKBykPG+LPWv1phTVIg2VO6GXKJKyrosLEtgkn/UUydJIeMqkCS4JgfbjABHP1HxIy3BBqu28VKebvxVMEEOQRrepRN4UnsY3JrCs8"
    "cJXtIrOhmxk10UXd+7E9w9JjILFXF4uwjPISZJZW/TpPuqoFYog/El5g4y6rotfIL4VGxEOKNzYRQq+y17oCP7Rf6xCr2so7+AeesXsOfYPqdUHi"
    "HW11YoZd4iNaIYUm9CZqUxwZmOb0LvQrpQta6iAk5va7EzvjbwhGMVkRZHNxvFBgD12aldCu9iqBCif24Aq3g0S4y3HssVdNgQJTF+wPZ4j878ve"
    "b+vkvbtSA7TtZbnRw8zsKBLWwv/e58RcyWVcR/Nyk95ijSYOj3k37IGN/NE/5myCKoXZMitL2DbqfqACclvoaabf+cvT7kUvAczjZOksNuZQxEP/"
    "PpAhuyDWnho06hF0aaaP6FrEIpYsV0gHtRwNW2fL/dBeD6mbTg3O0qVZp+jTTsXp7R6B0LtzQUJN3LvM34Gg2gUXxwlbs8S/npCgYXqJS9RhrTOU"
    "9JfjtNi7tLwPXaoxT/JekMbqbgpRdPcQmTVkSJh7KYHDTWFqng5UDz4Tl7uutozGf5wu66otSNOAm16iJTzwqVDKBcvIsl64EkzOKEbIGSchIVbt"
    "cNfQnJJ6/DnnWNCVQE6Z1llzmkGYu1//HLqA7+yI5GzpSyrkqoyKVJBYollk1ncD7lkuMxMu2WBbQ19vDbJwhFh6C7vACRW+qTyhqF2QLIBWxPLj"
    "XubIbkj2pKA5cddyQ58YkBOlsUS7yT1PA41WjuSlndcGH/XD71GEPqjODsNYHBjlpCO3lhrGbkdwpUjIc3L3IhHU4W22VLltJ1U/GfyHgD79wRjF"
    "UZ9ThFUcx+RWp25PTA0i1SWxI1RKmkGK0YxKBuVQXVpeHQxttbYvyIwFhqxXOPohyveUD+MwkVe7mWI8ek/k8CXuVQ7A6vRYXVXkGF+i80C68VeJ"
    "G7MqA7QjmNbc7fiQUkNVyXdQLLOnFK5mdVj+cHFcgxuwTplIWhNr230rd/dIfdcM+eJ22CEDv5nTPO++2utMgda0vGKHPeQutzt3ucVrVsrcSST+"
    "WNBklT/tcbDnTOppz7DkTyaT7kNvg4tkqmCgtqDor0VbubgoPno2kihoGXsa9Fv9yr9eIRMRUKpKk2aYSKfyE/M6CW9pjpC+5qF19jeIdlsZYkgn"
    "ZVbcl6o0nNBErkhm8jhJmnZ1m4nKZhPWX+ZN2vOMkfrLGTmkfdy1jvsNv3+Qiso7H1ypV55m95GtXv1Qaw5Zb8OmW4AwuEeOx+H6CnGSuL0NifQg"
    "CMClyasqGaPCq9HUyQB5sRCkTpfmqxwcR7iT+KXtF8JZLaIu4jOeOn2wgKaXgvs3BE7sAuxqObkZZ34cLADnGbgR21Ip/yhkEoluYdTwRtI17GJT"
    "b+9JjfAvNpTnOg0pbTmYQCYRm3etpJnCoSIlx9ps1pMbKcFpkUdJ4ythdnAY+g2ZQyWecuzc93PyrWff7m35Oj6yrsKnA8LcU0PKLeL3jkLzXJ61"
    "G9zK9AStZXMYkM11zS+4ZcG4NtPmh8JtPogk7Up4KpEuxWKHgvxclTDRE2fcexZMTyh3Huh2VLkSnJVyGaVqcl1/m4ouXRlk6aAHRYVaWSo0Qx/U"
    "3zsYdUX2kM3OaKfDUWX7zLKpiw42ZZqe03E51JdMndhVrbB2s80yy0K/nhZOWnuZo2BKnJvEtwq/ZQJOujfgqhICVS4wzzjpKfWJFfZjxx8Tr+Sj"
    "rpsFlMxvIeX9qWNtlzNNT4eyn66r+oO5/KIsZxGnuZ1qmVqXyAvuT1Y22GY9eoq+hef6glQ1t3kagN6HFnpwTeRKnVL97u3hDnN7QBaUNPWaTKIW"
    "KLhIqlXbNM+Ty8QMHtrgxrxXIlIGDq6f1X71bbF1PTIKVexHUe5MLpUsjy9eUb9ZYCb+p7Ylcx5nXBes20wDt02qbsXfsprY4+XxM21u3ldJPl7X"
    "SEmUcC9OgZPrSiebLPAg6BqQsAcSqOWiFjySPx5XNLNKoJpneiULR0ngmguleCyvUDluOvdmmxqsxIjnehuIYd61I7m0yRT0eeq2WxrVKWLMUrez"
    "aOjZJtN2XVFBRglIemU3tjIbtmMk9XSl9VNCVKcx88Ug4St0qlSb3DZqi+kltu9JxmkKUwwKjl1DBh95PdnCuLDsFN55+EDsPj/azhcn87uOZ32x"
    "YM32eOFmt3t7vnhuJvQ8vxt3B8jtlX7kjIPPNYEiZyTFc/nNaXx39xEyvbu6WPAAEO/pAQ+li2oEue51U+0KDv4wZut1HqmYZLeo8YlRw77kTCJu"
    "JFukH6WubaYSQCQB/YDI8u6mvAoKma1iX/rxw8mzhhqCyiN93FEIEZudGj5h4nVVf9CkOzlgMf2wJOtB4bpenef0OJ6ES2/1EnMqF1LYousaCPbu"
    "J7X6NlfA2XuugvhknFpSF96+fsOXjvHu6/sodlVkqekVSMe9wTWGwwFafpeBPpzkPuO0IGi5M46+7VSzcqM318KmH8WZFwOT5s6PDU0MDXKqwNig"
    "UYHOpaHoO+im6HUo2q5b5lGxTSzMa6yvyBX84BxVx2JWA/qTCy6kAnebhPuGjXsGNQMujesDL7qo4pWaobRsp1jamw0O091eB8BKMDOgV9j5I8MD"
    "UBQv9oOURJDbaU68DjPWYwUDKBjbXmvybUgzDU/n37FhTs+15QWcpI0MJUlFhzpra+VXhGRnCnH3rloXlFtf8c7A6VdPPPPy0LnJ36OPYfyszNj8"
    "lcwCNTokdxUgrODin/ueffYf4eXF6bH3RidG3h4bGD37XjhzKmLZDB0RJV3Xsrly5BVs4iIWqbxkhtF6mFB3nBt01ZU2cEeN1RKWLYV4E6dEfOZ6"
    "kqTDflVOJugeMjZp7dATJ597/eSpX774+ouIaO6sVqkKRGz6MuSf7AR2rEfEp9Pw16n161JDn+Iu24YMIGYDbU75iD156dHiR5zPJm4/x16PHXfF"
    "apArCs0Ej0swKD15r4IypDjlf0pO3mWU4QgMryznvSNOxkclkSP41PnBC91TpbPEo+KoXW41Y/bTLlK+cWJrvDDc1zcHzpzi1bUM9TiJsKf8K7sc"
    "vSTvvSvC2Qm6yW2He9fvJWcXFA5qilNss7yYLcgHIxKE+RLedInXU9FmIZdi0ePAPSQyPhWt3vlZkEhq3K5NPatx26c04FpeFuImFcyUxdRDjfc4"
    "AjeQqSvRIRvHq9ciq8aM6JIEksrvNKw9ejvskeAOlc6pXlcBlrRB5W+8bJ+wqsljZM8rihWUQyIkprynDwm4tzuossO4lSNB4dhuwh97udy4C96k"
    "rL1zx/ri2srDr6q8Tw8Y7XTY9bIth4WhSYQbnu7qmxY5I5MTo9xgOpxkCW9/6GpEescGxyeHJ3r/B8ioXu23Fl77n8/YNqq9OgA1/gzHLSrvwe11"
    "F9K3nNObq7C0+LwNWzs1GTRkr6Xdpnnnpk0wG4XeuEGXW0sxuAvItC3bb+tjHvz90ESyE62VDa63FCHWn7KP6E7Rj8kcEYP1n45nipNSHb3JmS87"
    "mCKtn0KixxhV1vFZ2etPReUt3VKyZgFTEcjg9GDp+SaKAVMX89njRQe4J9ng6qDtY137itVkGEmVsZlwIOgtcR2eNlU8YdNXzs78DjiI7dm8Lt2Z"
    "H+t8y8TmHi+6LF/oSWdnzRadGPC0HCV97dVzvWo8h3qV7Wk2u7f37ODwqG7NKqpgnJWoKnUgF/HEiZd7BTklZWP0q+S/kDQ87VCa6t6VPolaXZgY"
    "OHdmYHjknLKWbDBaknRFEme3xAWZPInTlUFVNvVERWioX++K3Y8sjPyTz2RULM/wjWVLoKSGyvt6PuHPDVzRJMExY2mUfGronMSDYpSYcINds2Q7"
    "kaA/AycViFHpqcT0YmPsjU8oJTZxvPbmfUR6UDiN8hxTdbY1toKOcEpm07K/WvIDz0AICXiltiB4eanwZQgxPrd9C7zPQUNJNrtOGbY2dHqwpvD2"
    "ci5r21hxhV72RBKx4TBfRRDiSvO4whYIWmsZHLUWjm/IJEzq6m6Hjzz+V45u5fXMTTRTXVKGA2OoBLVRzvvust4jFhAk87ucjbJaI3VpUSvSuXKe"
    "Tui3kM5kiV7WXRcCk8bxUYsmrPOERPdOJK+lGwokgKfK6iDYT58tFe3U5kpHT7K9HKLyHbhVnjwIU0PWrYS7a280ewIF9uvUwIRufFkf9q7/kHWT"
    "RCMQ2RNbU8EcPKilCNCbU3mKinJKa1TSBR6ZwDc7mwd/PzqMSMTn02jbgu5QEtuoguVVguWu7R4c4T/UzZpe1zJBc66mkHlndWEf2aC8fxHDLM7S"
    "7kj5YsWqXFIi6xAso2q1xSFgJddgH4K0kTuqTAp3BNHpR+AzomUzdCXft04K4q8L2phxgi2CGU9vXuKGusZF6Vy1ii1mPtjvtbaIm3CqWHEHWAH2"
    "ymwn8h9K/PDCKKH7NiQoSeTz/wsdJ1dEn6ndSATq9lwfU5ccuZ4tFK2sQBCecB/v1Z4y7Vm6VZdJOxmaasfm5uKuiyt81mmXip7cfqRLb62p+Ki6"
    "DrdtOSCtcVH8k4w29MhZLsHF1PTcLoV8lNPFBDYLRJJIYLMsPUE2fuJGIjp8uRaUgyfFVrwymaTsdhcjo/V5xqfD5FBn68ngC9Y96Slh/UXJhgSd"
    "XTLM1w3u8VsX9Ob6gDKMxPJk2riRgmqrV5WB4/bZRX4CWsy1Y4tTbGorznTRstUjWXU33bjOM+n15DUTrNg914ljT67RjNWha64rqcf35+9wsM/Z"
    "X7n7s4QvXNZe6PSMO4JL5b7zGt+zM/U6zxo7a92hYKeCqv4afTy0SZCPMOt6IY/pNJOhOgaYD2yqQB5T1nvowHM+0FIlt0fnDoa7XLqOuKCpvNOo"
    "666jurws2aYzofGVvp3laUc1TL1kh1XnjPoA73ozSjiu9DikhHeuNW6qsjqNCGS9ujCXG8n2qsn7FneOTL8yCqluI/23NZ1Vda/xkIHTanqCaa5r"
    "1mK/ca+gvZZum6LPBx5Deu5hrLw/tcJCHce5G/f6Ssw6FIIdlKk4q687xpz1haRxTV6BzlFD4wE0cVqz0DkDmv1upmV2TI+JsFhAffV9VccTqIkh"
    "KIeEVXn/meorCvsyqcQHxlWzKQ3T/tm06/bJqQEElzbua8DDaYAYdgjPBO5dpPUd1kHUsS9aa4VvuWq7hTSiczO1JdWJ0ygbUy2TGHfFZUtG8bpW"
    "rDbqAr7VbS1/e70ow+GuPt6ynqIVJHvb676+HnS76iDYGjYt94RzR2eginUsPO8jmxql6OFyLTYRgGCHtU6d4iU8TwV11HRilEMFCbhm70g913gC"
    "VzmRPSDU5po/doKcd5lT1rkPd0bHnq3t30JH8fvv/z9CtH2+"
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
