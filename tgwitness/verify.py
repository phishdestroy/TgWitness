# TgWitness verifier sources SHA-256: ef6bdd447926f4a1855e2a14160b16173986da914bb8463e096555123d5beb93
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


ASIC_MIMETYPE = b"application/vnd.etsi.asic-e+zip"


def container_members(archive, names, listed):
    if "mimetype" in listed or "mimetype" not in names \
            or archive.getinfo("mimetype").file_size != len(ASIC_MIMETYPE) \
            or read_member(archive, "mimetype") != ASIC_MIMETYPE:
        return []
    return sorted(name for name in names if name not in listed
                  and (name == "mimetype" or name.startswith("META-INF/")))


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
        container = container_members(archive, names, manifest["files"])
        if set(names) - set(container) != set(manifest["files"]) | {"manifest.json", "manifest.sig"}:
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
        if container:
            result["container"] = {"format": "ASiC-E", "unchecked_members": container}
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
# Catalogue SHA-256: 8ba3e8e8777d4db823abe54dc0e5a8f5da03af4d7f6683af90055391b6a73dbe
VERIFIER_LANGUAGE_DATA = (
    "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"
    "6Tm07BBKrTspsNCJLKbEsGiq5HVWD5S4n5F2XMe5uZZ23+WaGeZyvg3lJZN3UlpyiEfFXD0+uTxNFy81tsoEUddgMKYkl16YpIgsVlpf3m1vc/uY"
    "ozriWKW81kwlN4Ivc1fTiKbgaN4OkJMYqNlT5MSbm1GuKrEEGyxYV8vJ6pSNld8krwtf/Fiekj9opeWqfL4Ul3LQLqUX3HQ4Ud4aFPFZO8b6SB7y"
    "U59uUSgdXhDAz4gyNXli+ucuCdCevE6DrS89avDlE9oLVQBDy48mB45mzaf60l9wNR/fdcytYXDNiTFKnS98Pre1KNzyk9T0bpGsPJbtlkwr1W64"
    "zK5ys8+PJF/ewGubadhksMm6QqZ77hc+QMoEcH78AmhIER9DgxlKQpqeZ4fbeWiKeXQ0r6qadekc2iqNu8rnuaRQ0UkuYr5GYdbsPG/C8iU+CzPq"
    "Ep/lO4vPvnn32YMv2peOlV7hs/zFt63zZ1YWj+r7e9p/WGx/dPP5xw9Xu76ndefD9nv3W99cbB2//+zB2ZU737ZuHCu9rWfl0zdX7r7Zfu9m6+l7"
    "pRf0LF+41T7+9cpfjrQvXS5ezdM6+nnrySK28P7Zktt4Wnffad17s33yZuu3J8vu3mmdfad17s/295Ird2C+y1dPtS7fer54on3qtrpqB5Zh+cqd"
    "TtfstB8cbZ25yKvoCTmH2Fp2qU773LmVp/eWPzjS+uL99sf5G3RW7n4l8yzen9O+drP96Hzr3Fsri2+X02P7zMWVs1+3L9xvn7mTvyunffZW6+6T"
    "Dmy19fWfl5/cbh07B+NauXMPtrVo0vH3z9/9ttN1OCtffQL72D75x+dX/9z13pvW8XdaD95uPTn3/Nix51feKej5vFutM/eW/3h9fVfdPP/sNFAM"
    "783/LL7Zevd468Hp1uKT1u9O62l0vdnm2YMzsEWtq7f+8eR4+71Pl08ch/VrHXv0jycnVr3SBk4Ed85E0jr98PnRM6tcXtO++ln73Pln316B/twv"
    "3Nuq19VAh+23bsHuta8/hJk/e/gJzHD5yoOVpx/Cl5ZIe7ucBkaiF/AfTz5Yuft1++vHrZPXN+c2mvbxz1aOfSk//ePJaWFFNG7ofOX3f2ydP/n8"
    "wiKshHnNrcOmXD+je3z26KwZper5dPvyB/ALMLnn733VPv5lYSy9XDjDjTFTbd3408pXN2ExN3zFDFIKN0nNL5+83158E8bHHAVZ/p8/bl89YZvg"
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
            if result.get("container"):
                self.check("none", "ASiC-E container",
                           self.t("Entries outside the signed manifest (mimetype, META-INF): {n} · their CAdES "
                                  "signatures are not checked by this verifier",
                                  n=self.number(len(result["container"]["unchecked_members"]))))
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
    if result.get("container"):
        verification_print("ASiC-E container: entries outside the signed manifest (mimetype, META-INF): "
                           + str(len(result["container"]["unchecked_members"]))
                           + "; their CAdES signatures are not checked by this verifier.")
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
