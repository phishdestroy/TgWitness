# TgWitness verifier sources SHA-256: bb7a211b448801272bfabcbd63858b1a3952f497d6eb13f5e793d4d2bdf66619
"""Standalone verifier"""
import argparse
import base64
import bisect
import hashlib
import io
import json
import math
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unicodedata
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

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
    return re.sub(r"[\x00-\x08\x0b-\x1f\x7f-\x9f]", "", text)


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


def timestamp_signature(reply, roots, *, include_reference=False):
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
        candidates = list(trusted.values()) + [c for c in raw.values() if c not in chain]
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


BITCOIN_SOURCES = ("https://blockstream.info/api", "https://mempool.space/api")


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
            raise ValueError("Independent Bitcoin header sources disagree")
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
        summary.update(status="confirmed", time=min(c["time"] for c in confirmed), blocks=confirmed,
                       verification="proof evaluated; headers with 6 confirmations agreed by two HTTPS explorers",
                       sources=list(BITCOIN_SOURCES))
    elif unreachable:
        summary["check"] = "unavailable"
    return summary


def find_openssl():
    found = shutil.which("openssl")
    if not found and os.name == "nt":
        for base in (os.environ.get("ProgramFiles", r"C:\Program Files"),):
            for sub in ("Git/usr/bin/openssl.exe", "Git/ucrt64/bin/openssl.exe", "Git/mingw64/bin/openssl.exe"):
                if os.path.isfile(os.path.join(base, sub)):
                    return os.path.join(base, sub)
    if not found:
        raise ValueError("OpenSSL is required to check timestamp signatures (--tsa-ca)")
    return found


def openssl_verify_timestamp(data, reply, query, ca_path):
    binary = find_openssl()
    with tempfile.TemporaryDirectory() as tmp:
        paths = {}
        for name, content in (("data", data), ("reply.tsr", reply), ("query.tsq", query)):
            if content is not None:
                paths[name] = os.path.join(tmp, name)
                with open(paths[name], "wb") as handle:
                    handle.write(content)
        common = [binary, "ts", "-verify", "-in", paths["reply.tsr"], "-CAfile", str(ca_path)]
        selectors = [["-data", paths["data"]]] + ([["-queryfile", paths["query.tsq"]]] if query is not None else [])
        for selector in selectors:
            done = subprocess.run(common + selector, capture_output=True, timeout=30, check=False)
            if done.returncode:
                raise ValueError("Timestamp signature check failed: " + done.stderr.decode(errors="replace")[-500:])


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
                    openssl_verify_timestamp(data, reply, query, tsa_ca)
                entry["signature"] = "checked against the given root" if tsa_ca else "not checked (use --tsa-ca)"
                try:
                    entry.update(timestamp_certificate_reference(reply))
                except (ValueError, IndexError, TypeError):
                    entry["certificate_reference"] = "unavailable"
            elif proof_name.endswith(".ots"):
                proof = read_member(archive, proof_name)
                entry.update(kind="opentimestamps", **(confirm_ots(proof, digest) if check_bitcoin else ots_summary(proof, digest)))
            else:
                continue
            results.append(entry)
    return results


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

    def open(self, at):
        if self.closed_at is not None:
            self.gaps.append({"from": self.closed_at, "to": at, "reason": self.close_reason})
            self.closed_at = None
        self.start, self.alive, self.observing = at, at, True

    def close(self, at, reason):
        if self.observing:
            self.periods.append({"from": self.start, "to": at})
            self.observing, self.closed_at, self.close_reason = False, at, reason

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
            self.open(at)
            self.active, self.run_id = True, payload.get("run_id")
        elif kind == "observation.stopped":
            self.close(at, "observation paused by the operator" if payload.get("reason") == "operator"
                       else "observation stopped: " + str(payload.get("reason") or "unknown"))
            self.active = False
        elif kind == "process.stopped":
            self.close(at, "collector process stopped")
            self.active = False
        elif kind == "process.started":
            self.close(self.alive, "collector process ended without an orderly stop")
            self.active = False
        elif kind == "collector.error":
            self.close(self.alive, "collector error: capture may be incomplete")
            self.notes.append({"at": at, "chat_id": chat_id, "reason": "collector_error",
                               "operation": payload.get("operation"), "error_type": payload.get("error_type")})
            if payload.get("observation_stopped") is True:
                self.active = False
        elif kind == "connection.closed" and payload.get("role") in (None, "current"):
            self.close(at, "connection to Telegram closed")
        elif kind == "coverage.gap":
            reason = payload.get("reason")
            if chat_id is None and reason in INTERRUPTIONS:
                cause = ACCOUNT_LOSS.get(payload.get("cause")) if reason == "authorization_required" else None
                self.close(at, INTERRUPTIONS[reason] + (": " + cause if cause else ""))
                if reason != "transport_disconnected":
                    self.active = False
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
        self.sequences.add(event, MESSAGE_KINDS)

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
        unobserved = []
        for chat_id, ids in sorted(self.ids.items()):
            ordered = sorted(ids)
            holes = missing_ranges(ordered)
            unobserved.append({"chat_id": chat_id, "title": self.titles.get(chat_id),
                               "observed_from": ordered[0], "observed_to": ordered[-1], "observed": len(ordered),
                               "not_observed": sum(high - low + 1 for low, high in holes),
                               "ranges": [{"low": low, "high": high} for low, high in holes[:ranges_per_chat]],
                               "ranges_total": len(holes)})
        return {"continuous": periods, "gaps": gaps, "notes": self.notes[:200], "notes_total": len(self.notes),
                "unobserved_ids": unobserved, "gap_summary": self.sequences.result(self.titles), "first_record": self.first, "last_record": self.last,
                "meaning": "Observation intervals follow connected capture heartbeats from the same run, within three "
                           "heartbeat intervals (at least three minutes). Each interval ends at its last capture "
                           "confirmation or recorded stop. Message-number gaps describe the observed numbering range."}


GAP_DEFAULTS = {"gap_analysis": True, "gap_account_sequence": True, "gap_cluster_min": 1, "gap_clusters_listed": 20,
            "gap_service_estimate": False}
WIDE_TYPES = ("private", "groups", "bots")
GAP_MEANING = ("A gap is a message number between two observed messages that this collector never saw. Telegram assigns "
           "these numbers; a gap may be a message Telegram never showed to this account.")
ESTIMATE_MEANING = ("Estimate from the share of service messages among observed numbers. It does not explain any "
                    "particular gap and is never subtracted from the missing count.")


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
        self.paused = False

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
        if wide(scope):
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


def coverage_lines(coverage):
    def span(seconds):
        hours, rest = divmod(int(seconds), 3600)
        return (str(hours) + " h " if hours else "") + str(rest // 60) + " min"
    lines = ["Continuously observed from " + p["from"] + " to " + p["to"] + " (" + span(p["seconds"]) + ")"
             + (", observing at the last capture confirmation" if p.get("still_observing") else "")
             for p in coverage["continuous"]]
    lines += ["Gap from " + g["from"] + " to " + g["to"] + ": " + str(g["reason"]) for g in coverage["gaps"]]
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
                          "meaning": "Offline checks establish only the recorded beacon's self-consistency, "
                                     "not its BLS signature or a lower time bound. --check-drand compares "
                                     "selected rounds with HTTPS relays. Only authenticated rounds can support "
                                     "a lower time bound for subsequent records; unchecked rounds cannot."},
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
            lines.append("drand beacons are self-consistent only: no BLS signature or lower time bound verified. "
                         "Run with --check-drand to compare rounds with HTTPS relays.")
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
        chronology["meaning"] = ("Observation times are collector-supplied. These anomalies do not invalidate "
                                 "signatures; chronological claims rest on independent time evidence such as a "
                                 "timestamp or a witness record.")
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


def verify_checkpoint(checkpoint, public_key, event_count, hash_at):
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


def read_sealed(stream):
    digest, window = hashlib.sha256(), b""
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        window += chunk
        if len(window) > 2 * SEAL_WINDOW:
            digest.update(window[:-SEAL_WINDOW])
            window = window[-SEAL_WINDOW:]
    at = window.rfind(SEAL_OPEN)
    if at < 0:
        return None
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
    parent = lookup.get(item.get("parent_id") or item.get("card_id"))
    return board_scope(parent, lookup, trail) if parent else None


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
    return {"cards": len(cards), "meaning": "Minimised team notes, signed by the collector; not the original annotations chain"}


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
            "annotations_checked": bool(evidence), "meaning": "Team opinions; signature authenticates the signed document, not the truth of a conclusion"}


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
        hash_files, account_exports = set(), []

        def measured(lines):
            for line in lines:
                event = strict_json(line)
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
            verify_checkpoint(checkpoint, public, result["events"], hash_at)
            result["checkpoint_event_count"] = checkpoint["statement"]["event_count"]
        result["anchors"] = verify_anchors(archive, names, public, result["events"], hash_at, tsa_ca, check_bitcoin)
        result["board"] = verify_board(archive, manifest, checkpoint)
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
        return {"format": manifest["format"], "fingerprint": fp,
                "message_count": manifest.get("message_count"), "producer": manifest.get("producer"),
                "chat": manifest.get("chat"), "key_pinned": bool(expected_fingerprint), "parts": parts,
                "files_checked": len(manifest["files"]), "chat_json_sha256": manifest["files"].get("chat.json"),
                "attachments": attachments, "sha256sums": sums, "report_seal": seal,
                "report_parts": companions["parts"], "report_pdf": companions["pdf"], "message_ids": ids,
                "case": manifest.get("case") or {}}


COMPARE_MEANING = {
    "number": "Both archives record the same chat and account, so messages are matched by their number. "
              "Unchanged means equality of the complete saved message record. Differences may include "
              "observation metadata and do not by themselves prove a Telegram edit.",
    "content": "The archives come from different chats or accounts (for example both sides of a private chat), "
               "or their scope identity is missing. Possible matches use time, sender, full text and file hash. "
               "Unchanged counts identical saved records among these pairs, not proven message identity. "
               "Differences describe the paired records, not necessarily edits of the same Telegram message.",
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
                "html_index_signed_by_manifest": "index.html" in self.files,
                "meaning": "Integrity is checked relative to the signing key. Completion covers the frozen selected "
                           "tasks and observed outcomes, not all Telegram data, a simultaneous snapshot or trusted time."}




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
                           "Source linkage names the original archive and collector key; filtering and redaction follow the stated policy."}





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
                   "head_binding": "A second key retained the journal head. Who controls that key is a custody fact this verifier cannot check.",
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
         "detail": runtime.get("limitation") or "no independently checked runtime attestation bound to this export and a created key"},
    ]
    tier = "self_attested"
    for row in ladder:
        if row["status"] != "pass":
            break
        tier = row["tier"]
    return {"tier": tier, "ladder": ladder, "scope": "complete exported head; no claim of continuous or complete Telegram observation"}


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


def english(text, **values):
    for name, value in values.items():
        text = text.replace("{" + name + "}", str(value))
    return text


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
    if times:
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
# Catalogue SHA-256: 1b70a391239d15a9ccf526c76d9862aa112fc79ddc882fa10662b98283e1a762
VERIFIER_LANGUAGE_DATA = (
    "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"
    "RPFPP/0XzDMcMA=="
)
# END GENERATED VERIFIER LANGUAGES
import zlib
VERIFIER_LANGUAGES = json.loads(zlib.decompress(base64.b64decode(VERIFIER_LANGUAGE_DATA)))
SAY = {code: entry["words"] for code, entry in VERIFIER_LANGUAGES.items()}


KINDS = {"evidence": "Evidence archive", "chat": "Chat export", "account": "Account export",
         "account_disclosure": "Account disclosure", "witness": "Witness journal",
         "dossier": "People profiles", "proof": "Public proof", "report": "Sealed report",
         "history": "History report", "handover": "Handover extract", "selection": "Viewer selection",
         "distributed": "Distributed acquisition", "board": "Case Board"}


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
        for anchor in anchors:
            point = self.t("checkpoint #{n}", n=self.number(int(anchor["checkpoint"][11:-5]))) \
                if anchor["checkpoint"][11:-5].isdigit() else anchor["checkpoint"]
            if anchor.get("kind") == "rfc3161":
                checked = anchor.get("signature", "").startswith("checked")
                self.check("ok" if checked else "warn", "RFC 3161 · " + anchor["service"],
                           point + " · " + anchor.get("time", "?").replace("T", " ").replace("Z", " UTC"))
                self.say("  " + " " * 27 + self.paint(self.t("signature chained to your root" if checked
                                                               else "signature not checked: add --tsa-ca"), "dim"))
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
                   "connection to Telegram lost": "Disconnected", "observation could not resume after a restart": "Interrupted"}
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
    parser.add_argument("--explain", action="store_true", help="Explain what the readable checks mean and do not mean")
    parser.add_argument("--interactive", action="store_true", help="Ask for the original ZIP and trusted key; save a readable transcript")
    return parser


def verification_arguments(parser, argv):
    args = parser.parse_args(argv)
    if bool(args.sealed_attestation) != bool(args.sealed_policy):
        parser.error("--sealed-attestation and --sealed-policy must be supplied together")
    args.implied_checks = set()
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
                    "evidence", "check_drand", "check_bitcoin", "require_tier", "sealed_attestation", "board") if getattr(args, name)]
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
    if "statement" in data and "signature" in data:
        authenticate_statement(data, "public_key" if "public_key" in data["statement"] else "witness_public_key")
        known = {"tgwitness-board-selection-v1", "tgwitness-case-board-v1", "tgwitness-case-board-disclosure-v1",
                 "tgwitness-case-board-handover-v1"}
        if kind not in known and not any(is_format(kind, name) for name in (
                "public-proof-v1", "history-report-v1", "dossier-v1")):
            raise VerifierTooOld("Unsupported signed JSON format")
    if kind == "tgwitness-board-selection-v1":
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
    notes += coverage_lines(result["coverage"]) + outside_lines(result["outside"])
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
    if getattr(args, "evidence", None) and kind in ("evidence", "chat", "handover", "witness", "account", "distributed"):
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
