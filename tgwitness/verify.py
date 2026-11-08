# TgWitness verifier sources SHA-256: 2dfbfc01a4674262466ac86cd1c25544b33598911a18c99c2d1bf07e399ea285
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
        super().__init__("The archive format is newer than this verifier; use the current verify.py" +
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
    """Validate claimed range coverage, not Telegram origin or absent payloads."""
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
                            pass  # Unsupported hash never produces a verified commitment.
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
    """TLS explorer consensus, explicitly not independent Bitcoin chain validation."""
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


# Channels have separate ID sequences; private chats, bots and basic groups share the account sequence.
GAP_DEFAULTS = {"gap_analysis": True, "gap_account_sequence": True, "gap_cluster_min": 1, "gap_clusters_listed": 20,
            "gap_service_estimate": False}
WIDE_TYPES = ("private", "groups", "bots")
GAP_MEANING = ("A gap is a message number between two observed messages that this collector never saw. Telegram assigns "
           "these numbers; a gap does not say who removed a message or why, and it may be a message Telegram never "
           "showed to this account.")
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
    """times maps each observed message number to the time it was first observed; notices are numbers known
    only from a deletion or recheck record, without saved content."""
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
    """Whether a collection scope records every message that takes a number from the account sequence."""
    if not isinstance(scope, dict) or scope.get("mode") != "account":
        return False
    types = scope.get("types") if isinstance(scope.get("types"), dict) else {}
    excluded = [chat for chat in scope.get("exclude") or scope.get("excluded") or [] if account_numbered(chat)]
    return all(types.get(kind) is True for kind in WIDE_TYPES) and scope.get("own_actions") is True and not excluded


def scope_reason(scope):
    if not isinstance(scope, dict) or scope.get("mode") != "account":
        return ("Private chats, bots and ordinary groups share one account-wide numbering. It can be measured only "
                "while whole-account collection is on; this journal has no such period.")
    return ("The scope does not confirm that private chats, bots, ordinary groups and the account's own messages "
            "were all included without excluded chats; those messages take numbers from the same sequence.")


class Sequences:
    """Collects observed numbers from journal records in order and measures their gaps."""

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
            # Account-level deletions name numbers without an attribution to an observed chat.
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
                    # Only messages that arrived during whole-account collection bound the measured range.
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
                         + " ID(s) not observed in " + str(chat["ranges_total"]) + " range(s) (not evidence of deletion)")
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
                          "meaning": "Records after a drand round were written after the round's time: nobody "
                                     "knows a round's value earlier. Rounds are compared with drand relays only "
                                     "with --check-drand."},
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
            lines.append("Rounds not compared with drand relays: run with --check-drand")
        elif checked["relays"]:
            lines.append("Confirmed by drand relays: " + str(checked["confirmed"]) + " of " + str(checked["asked"])
                         + " round(s) asked (" + ", ".join(checked["relays"]) + ")"
                         + ("" if len(checked["relays"]) > 1 else "; only one operator answered"))
        else:
            lines.append("Rounds could not be compared: no drand relay answered")
        if drand["clock_behind_seconds"] > 1:
            lines.append("The collector's clock was up to " + str(drand["clock_behind_seconds"])
                         + " s behind drand time")
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
                                 "signatures, but chronological claims require independent time evidence. "
                                 "An ordered journal does not prove its timestamps are accurate.")
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
        seal = check_seal(read_json_seal(json.loads(read_member(archive, "report.json", MAX_JSON_BYTES))), public)
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
            event = json.loads(line)
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
                    event = json.loads(line)
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
        records = [json.loads(line) for line in bounded_lines(incoming)]
    replay = board_replay(records, public)
    signed = json.loads(read_member(archive, "case-board.json", MAX_JSON_BYTES))
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
            retained_heads.append(json.loads(read_member(archive, name)).get("statement", {}).get("annotations_head"))
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
                    event = json.loads(line)
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
                if name not in files or json.loads(read_member(archive, name, MAX_JSON_BYTES)) != expected:
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
    signed = json.loads(read_member(archive, "case-board.json", MAX_JSON_BYTES))
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
            record = json.loads(line)
            if record["hash"] in wanted:
                for card in cards:
                    if card.get("target", {}).get("event_hash") == record["hash"] and card.get("observation") != record:
                        raise ValueError("Board exposes content outside the handover record")
                matched.add(record["hash"])
    if matched != set(wanted):
        raise ValueError("Board refers to a record not disclosed in the handover")
    if "report.json" in manifest["files"]:
        report = json.loads(read_member(archive, "report.json", MAX_JSON_BYTES))
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
                row = json.loads(line)
                if row["seq"] > count:
                    break
                prefix.append(row)
        if board_replay(prefix, public) != statement["state"]:
            raise ValueError("Case Board state differs from its signed annotations prefix")
        boundary = statement["journal_head"]
        source_head = {"seq": 0, "hash": "0" * 64}
        with open_archive(evidence) as archive, archive.open("events.jsonl") as incoming:
            for line in bounded_lines(incoming):
                row = json.loads(line)
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
            saved_coverage = json.loads(read_member(archive, "coverage.json", MAX_JSON_BYTES))
            saved_gaps = saved_coverage.get("gap_summary") if isinstance(saved_coverage, dict) else None
            if isinstance(saved_gaps, dict):
                gap_settings = saved_gaps.get("parameters")
        observed, outside = Coverage(gap_settings), OutsideRecords()
        hash_files, account_exports = set(), []

        def measured(lines):
            for line in lines:
                event = json.loads(line)
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
                    event = json.loads(line)
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
    """Check a local acquisition prefix; unsigned trailing bytes are not observations.

    Pages group decoded messages, not raw RPC responses. The final filtered ZIP
    keeps its existing per-account signatures and does not disclose excluded pages.
    """
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
            record = json.loads(line)
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
    """Read-only inspection of a stopped distributed job; never opens its vault."""
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
    # Preview shortening must never define equality. Include future fields too;
    # canonical JSON preserves value types and array order, unlike dict equality.
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
        print("Matched: " + str(result["matched"]) + " (possible correspondence, not proof of message identity)")
    if not (first["key_pinned"] and second["key_pinned"]):
        print("Signer identity is unpinned for at least one archive: compare the fingerprints with copies kept elsewhere.")


def message_id_summary(chat_id, ids):
    holes = missing_ranges(ids)
    return {"chat_id": chat_id, "numbered_per_chat": numbered_per_chat(chat_id),
            "first_id": ids[0] if ids else None, "last_id": ids[-1] if ids else None, "present": len(ids),
            "missing": sum(high - low + 1 for low, high in holes) if numbered_per_chat(chat_id) else None,
            "missing_ranges": [[low, high] for low, high in holes] if numbered_per_chat(chat_id) else []}


def check_message_ids(archive, manifest):
    claimed = json.loads(read_member(archive, "message-ids.json", MAX_JSON_BYTES))
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
                record = json.loads(line)
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
                    # The export wire format places one complete message on each line.
                    # Reject other layouts instead of authenticating bytes but silently skipping records.
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
            message = json.loads(line.removesuffix(","))
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
        envelope = json.loads(read_member(self.archive, name))
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
        record = json.loads(line)
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
        # Version 2 keeps records the selection left out as content-free markers, and replies say what they answer.
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
                    row = json.loads(line)
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
            # A reply to a disclosed or withheld message must point at that record; only not_in_source points nowhere.
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
            event = json.loads(line)
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
            event = json.loads(line)
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


def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def unb64url(text):
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


class DailyJournal:
    """One prefix boundary per UTC date; no full journal retained in memory."""
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
        # Every credited anchor is checked; sampling must not certify unchecked rounds.
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
CONDITION_LABELS = {"integrity": "Integrity", "signer": "Signer key", "head_binding": "Independent binding of the last record",
                    "external_time": "External time", "environment": "Attested collection run"}
CONDITION_ROLE = {"integrity": "required", "signer": "required", "head_binding": "one_of", "external_time": "one_of",
                  "environment": "optional"}
ROLE_LABELS = {"required": "Required conditions", "one_of": "At least one of these", "optional": "Optional condition"}
CONDITION_SCOPE = {"integrity": "The archive is unchanged since the collector signed it.",
                   "signer": "The signing key is the collector key the recipient retained.",
                   "head_binding": "Records up to the bound record were not removed or replaced after the binding.",
                   "external_time": "The covered records existed by the stated time.",
                   "environment": "The signing key was created inside the attested collection run."}
MINIMUM_NAMES = {"signer": "confirmed signer key", "head_binding or external_time": "independent binding of the last record or external time"}
UNPINNED_NOTE = "Signer key is not pinned: pass --fingerprint with the fingerprint you retained."


def assurance(result):
    """Credit only checks performed by this verifier, with coverage of the export head."""
    witness = result.get("witness") or {}
    anchors = result.get("anchors") or []
    stamps = [a for a in anchors if a.get("event_count") == result.get("events") and (
        a.get("kind") == "rfc3161" and a.get("signature", "").startswith("checked against") or
        a.get("kind") == "opentimestamps" and a.get("status") == "confirmed")]
    times = [a["time"] for a in stamps]
    if witness.get("head_bitcoin_block_time"):
        times.append(witness["head_bitcoin_block_time"])
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
                    + "; witness clock " + str(witness.get("head_witnessed_at"))) if independent else "no pinned independent witness at the export head"},
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
                      "collector {fingerprint}… matches the trusted fingerprint" if result.get("key_pinned")
                      else "collector {fingerprint}… not compared with a retained fingerprint", fingerprint=fp[:16])]
    independent = bool(witness.get("witness_key_pinned") and witness.get("witness_fingerprint") not in (None, fp)
                       and not witness.get("conflicts"))
    retained = result.get("checkpoint_event_count")
    through = max(retained or 0, (witness.get("verified_through_event") or 0) if independent else 0)
    at_head = journal and (retained == events or independent and bool(witness.get("export_head_witnessed")))
    if journal and through:
        text, values = "records 1–{through} of {total} held by an independent party", {"through": through, "total": events}
    elif journal:
        text, values = "no retained checkpoint or confirmed witness", {}
    else:
        text, values = "this archive type carries no journal checkpoints; verify the evidence journal", {}
    rows.append(condition("head_binding", "met" if at_head else "partial" if journal and through else "missing",
                          "--checkpoint kept outside the collector, or --witness with --witness-fingerprint" if journal
                          else "in the evidence journal ZIP: --checkpoint, or --witness with --witness-fingerprint", text, **values))
    checked = [a for a in anchors if a.get("kind") == "rfc3161" and str(a.get("signature", "")).startswith("checked against")
               or a.get("kind") == "opentimestamps" and a.get("status") == "confirmed"]
    times = [a["time"] for a in checked if a.get("event_count") == events and a.get("time")]
    if independent and witness.get("export_head_witnessed") and witness.get("head_bitcoin_block_time"):
        times.append(witness["head_bitcoin_block_time"])
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
                          "RFC 3161 with --tsa-ca, OpenTimestamps with --check-bitcoin, witness Bitcoin seals or a checked GitHub attestation"
                          if journal else "in the evidence journal ZIP: --tsa-ca or --check-bitcoin", text, **values))
    drand = ((result.get("outside") or {}).get("drand") or {}).get("checked") or {}
    if drand.get("confirmed"):
        rows[-1]["drand"] = ", ".join(drand.get("relays") or [])
        rows[-1]["detail"] += " · drand rounds confirmed by " + rows[-1]["drand"]
    rows.append(condition("environment", "met" if attested else "missing",
                          "--sealed-attestation with --sealed-policy for a GitHub Actions run; Intel TDX: python -m tgwitness.cloud verify"
                          if journal else "in the evidence journal ZIP: --sealed-attestation with --sealed-policy",
                          "collection ran in the attested workflow {workflow}" if attested
                          else "no attested collection run checked here",
                          **({"workflow": runtime.get("workflow")} if attested else {})))
    met = {row["id"] for row in rows if row["status"] == "met"}
    missing = ([] if "signer" in met else ["signer"]) + \
              ([] if {"head_binding", "external_time"} & met else ["head_binding or external_time"])
    minimum = not missing
    bound = events if minimum else max(through if journal else 0, stamped)
    options = [] if "signer" in met else ["--fingerprint FINGERPRINT"]
    if journal and "head_binding or external_time" in missing:
        options += sorted({"--tsa-ca TSA-ROOT.pem" if a.get("kind") == "rfc3161" else "--check-bitcoin" for a in unchecked
                           if a.get("event_count") == events and (a.get("kind") == "rfc3161" or a.get("status") == "bitcoin-unverified")}) \
            or ["--checkpoint CHECKPOINT.json"]
    return {"profile": "attested" if minimum and "environment" in met else "evidence" if minimum else "integrity",
            "minimum_met": minimum, "missing": missing, "records": events,
            "bound_through": bound if "signer" in met else 0, "conditions": rows,
            "next_options": options, "journal_needed": not journal and "head_binding or external_time" in missing,
            "minimum": "integrity, confirmed signer key, and an independent checkpoint, confirmed witness or verified "
                       "external timestamp covering the last exported record"}


def next_lines(evidence, t=None):
    t = t or english
    lines = [t("Next step: run verify.py again with {options}", options=" ".join(evidence["next_options"]))] \
        if evidence.get("next_options") else []
    if evidence.get("journal_needed"):
        lines.append(t("This archive type carries no checkpoints or timestamps: the last record is bound in the evidence "
                       "journal of the same workspace. Verify that ZIP with --fingerprint and --checkpoint."))
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
            page = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "TgWitness-verify"}),
                                          timeout=30).read(MAX_SMALL_MEMBER_BYTES).decode("utf-8", "replace")
            ids = [int(n) for n in re.findall(r'data-post="[^"/]+/(\d+)"', page)]
            posts += [(None, None, block) for block in re.split(r'data-post="', page)[1:]]
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
            found.append((message.get("id"), message.get("date"), body))
        return found
    return [(None, None, text)]


def check_channel(witness, source):
    key = Ed25519PublicKey.from_public_bytes(base64.b64decode(witness["public_key"], validate=True))
    matching, invalid, differing, foreign, dates = set(), [], [], 0, {}
    for message_id, date, text in channel_texts(source):
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
                if date:
                    dates[statement["seq"]] = date
    posted = set(witness["posted"])
    return {"matching": len(matching), "matching_records": sorted(matching),
            "invalid_signatures": invalid, "differ_from_journal": differing,
            "other_witnesses": foreign,
            "posted_but_not_found": sorted(posted - matching),
            "never_posted": sorted(set(witness["statements"]) - posted),
            "telegram_post_dates": dates,
            "post_date_verification": "not-performed"}


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
                          "Other progress fields are signed statements only. No proof of Telegram origin "
                          "or historical completeness."}


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
# Source: verifier_languages.json; update with tools/sync_verifier_languages.py
# Catalogue SHA-256: 4b6bf161b3f375df5d706dd2fc3c303ecf2d8c1c43e78f45ba269fbb6290677f
VERIFIER_LANGUAGE_DATA = (
    "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"
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
    # Windows locale.getlocale() may use English language names instead of tags.
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
        # Only formatting produced here may become terminal control sequences.
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
        # Separate lines avoid broken columns for CJK and right-to-left scripts.
        self.say("  " + self.paint(self.glyph[mark[0]], mark[1]) + " " + self.t(label))
        if detail:
            self.say("    " + (self.paint(detail, "dim") if state == "none" else detail))
        if state != "none":
            self.explain(label)

    def explain(self, label):
        meanings = VERIFIER_LANGUAGES[self.lang]["explain"]
        if self.explain_enabled and label in meanings:
            import textwrap
            # Preserve shaping clusters and bidirectional paragraphs; let the terminal wrap these scripts.
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
        import unicodedata
        text = " " + self.glyph[state] + "  " + label + " "
        width = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)
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
        # Preserve the exact diagnostic for experts; do not translate source data or error identifiers.
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
        # Keep arbitrary source/operator reasons verbatim; known software reasons use translated labels.
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
            self.check("none", "Derivation", "filtering and redaction correctness are not established")
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
        met = {row["id"] for row in evidence["conditions"] if row["status"] == "met"}
        needed = {"required": True, "one_of": not {"head_binding", "external_time"} & met, "optional": False}
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
            self.explain({"signer": "Key pinning", "head_binding": "Retained checkpoint"}.get(row["id"], ""))
        self.say()
        self.say("  " + self.paint(evidence_line(evidence, self.t), "ok" if evidence["minimum_met"] else "warn"))
        for line in next_lines(evidence, self.t):
            self.say("  " + line)

    def localized_note(self, note):
        if note == UNPINNED_NOTE:
            return reader_message("key_unconfirmed", self.lang)
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
        # Protocol diagnostics, user-entered data and unknown future notes stay verbatim.
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
    """Find by manifest, never by a guessed filename, key, or self-declared trust."""
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
    """Keep terminal colours on screen and plain UTF-8 in the saved copy."""
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
    """No shell commands, installations, key auto-pinning, or archive mutation."""
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
    parser.add_argument("--channel", help="Witness channel posts: Telegram Desktop result.json, saved page or t.me/s URL")
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
    compared['assurance']['scope'] = 'two authenticated chat exports; comparison does not prove event history'
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
    if check and check["telegram_post_dates"]:
        notes.append("Channel dates are supplied metadata; witness signatures do not authenticate publication times.")
    if args.require_witness:
        witnessed = result.get("witness")
        if not witnessed:
            raise ValueError("--require-witness requires a full evidence ZIP and its witness journal")
        if not witnessed["witness_key_pinned"] or not witnessed["export_head_witnessed"]:
            raise ValueError("No pinned witness checkpoint matches the exported journal head; "
                             "retain a witness checkpoint at the export boundary")
        if witnessed["witness_fingerprint"] == result["fingerprint"]:
            raise ValueError("Collector and independent witness must use different trusted signing keys")
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
