# TgWitness verifier sources SHA-256: 4342292a54b97281bd9e23f5d12aeaf6a7b041eac540f63999d0c26562ef38d2
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
# Catalogue SHA-256: a293616b8a59b08fe0e7796c939bde13f22cdd729854e8e2400ff1b733af4d8c
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
        for anchor in anchors:
            point = self.t("checkpoint #{n}", n=self.number(int(anchor["checkpoint"][11:-5]))) \
                if anchor["checkpoint"][11:-5].isdigit() else anchor["checkpoint"]
            if anchor.get("kind") == "rfc3161":
                checked = anchor.get("signature", "").startswith("checked")
                self.check("ok" if checked else "warn", "RFC 3161 · " + anchor["service"],
                           point + " · " + anchor.get("time", "?").replace("T", " ").replace("Z", " UTC"))
                self.say("  " + " " * 27 + self.paint(self.t("signature chained to your root" if checked
                                                               else "signature not checked: add --tsa-ca"), "dim"))
                revocation = anchor.get("revocation") or {}
                status = revocation.get("status")
                if status == "good":
                    self.say("  " + " " * 27 + self.paint(self.t(
                        "signing certificate not revoked as of {time} ({source})", source=revocation["source"],
                        time=revocation["as_of"].replace("T", " ").replace("Z", " UTC")), "dim"))
                elif status == "revoked_after":
                    self.check("warn", "Timestamp warning", self.t(
                        "signing certificate revoked at {time}, after the time stamp ({source})", source=revocation["source"],
                        time=revocation["revoked_at"].replace("T", " ").replace("Z", " UTC")))
                elif status == "failed":
                    self.check("warn", "Timestamp warning", self.t("revocation check failed: {reason}", reason=revocation["error"]))
                elif status:
                    self.say("  " + " " * 27 + self.paint(self.t("revocation not checked (no OCSP/CRL in the archive)"), "dim"))
                if anchor.get("certificate_reference"):
                    self.say("  " + self.t("Signing certificate reference") + ": " + anchor["certificate_reference"])
                for warning in anchor.get("warnings") or []:
                    self.check("warn", "Timestamp warning", self.t(warning))
            else:
                status = anchor.get("status")
                detail = {"pending": "pending: run ots upgrade, then ots verify",
                          "bitcoin-unverified": "Bitcoin attestation present; run ots verify"}.get(
                              status, "unknown attestation type; no verified Bitcoin timestamp")
                self.check("wait" if status == "pending" else "warn", "OpenTimestamps · " + anchor["service"][:10],
                           point + " · " + self.t(detail))

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
        for period in periods:
            self.say("    " + str(period["from"]) + " → " + str(period["to"]) + " · "
                     + self.t("Duration") + ": " + str(int(period["seconds"])) + " s")
        self.check("warn" if gaps else "none", "Observation gaps", self.number(len(gaps)))
        for gap in gaps:
            self.say("    " + str(gap["from"]) + " → " + str(gap["to"]))
            self.say("    " + self.t("Reason") + ": " + self.coverage_reason(str(gap["reason"])))
        for window in coverage.get("session_windows") or []:
            self.check("warn", WINDOW_WORDS.get(window["reason"], str(window["reason"])),
                       str(window["from"]) + " → " + str(window["to"])
                       + (" · " + self.t("open at the last record") if window.get("not_resumed_by_last_record") else ""))
        session = coverage.get("session") or {}
        for item in session.get("sessions_at_start") or []:
            self.check("warn" if item.get("others") else "none", "Other sessions at start",
                       ("?" if item.get("others") is None else self.number(item["others"])) + " · " + str(item["at"]))
        if session.get("sessions_added"):
            self.check("warn", "Sessions added during observation",
                       self.number(sum(item["added"] for item in session["sessions_added"]))
                       + " · " + str(session["sessions_added"][0]["at"]))
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
            return self.t("Stopped") + ": " + text.partition(": ")[2]
        return text

    def outside(self, outside):
        drand, gateway, devices = outside["drand"], outside.get("gateway") or {}, outside["devices"]
        if not (drand["rounds"] or gateway.get("windows") or devices["checks"]):
            return
        self.heading("Live recording and devices")
        if drand["rounds"]:
            self.check("none", "drand", self.t("Recorded") + ": " + str(drand["rounds"]) + " · "
                       + str(drand["first"]["at"]) + " → " + str(drand["last"]["at"]))
            self.field("Gap", str(drand["largest_gap_seconds"]) + " s")
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
            return self.t("signature not checked: add --tsa-ca").replace("--tsa-ca", "ots verify")
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
