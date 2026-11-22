# TgWitness verifier sources SHA-256: 67e6cd46f8a9aad0c20ed29ed85b71fbd0444539a3feabfd1bc6688ce82eee81
"""Standalone verifier"""
import argparse
import base64 as _base64
import binascii
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

class StrictBase64:
    def b64decode(self, value, altchars=None, validate=False):
        data = _base64.b64decode(value, altchars, validate)
        if validate:
            raw = value.encode("ascii") if isinstance(value, str) else bytes(value)
            if _base64.b64encode(data, altchars) != raw:
                raise ValueError("Non-canonical base64 encoding")
        return data

    def __getattr__(self, name):
        return getattr(_base64, name)


base64 = StrictBase64()

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


def utc_time(item, name):
    if hasattr(item, name + "_utc"):
        return getattr(item, name + "_utc")
    value = getattr(item, name)
    return value.replace(tzinfo=timezone.utc) if value is not None else None


def safe_text(value):
    text = str(value)
    text = re.sub(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07\x1b]*(?:\x07|\x1b\\))", "", text)
    text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f-\x9f]", "", text)
    return re.sub("[\u061c\u200e\u200f\u2028\u2029\u202a-\u202e\u2066-\u2069]",
                  lambda match: "\\u%04x" % ord(match.group()), text)


def failure_detail(exc):
    text = safe_text(exc)
    if not text and isinstance(exc, InvalidSignature):
        return "the signature does not match the signed content: the file was changed, or it was signed by another key"
    return text


def plain_failure(exc):
    detail = failure_detail(exc)
    if isinstance(exc, zipfile.BadZipFile):
        return "this file is not a ZIP archive, or it is damaged [" + type(exc).__name__ + "]"
    if isinstance(exc, (FileNotFoundError, NotADirectoryError, IsADirectoryError)):
        name = getattr(exc, "filename", None)
        return "cannot read " + (safe_text(name) if name else "the file") + ": it does not exist or is not a file [" + type(exc).__name__ + "]"
    if isinstance(exc, KeyError) and "manifest.json" in detail:
        return "the archive has no manifest.json, so it is not a signed TgWitness archive [" + type(exc).__name__ + "]"
    if isinstance(exc, KeyError) and "manifest.sig" in detail:
        return "the archive has no manifest.sig, so its signature cannot be checked [" + type(exc).__name__ + "]"
    if isinstance(exc, json.JSONDecodeError):
        return ("a record or manifest is not valid JSON (character " + str(exc.pos) + "): the file is damaged or was not produced by TgWitness ["
                + type(exc).__name__ + "]")
    if isinstance(exc, InvalidSignature):
        return detail
    if isinstance(exc, UnicodeError):
        return "a file in the archive is not valid text: the file is damaged or was not produced by TgWitness [" + type(exc).__name__ + "]"
    if isinstance(exc, binascii.Error):
        return "a signature or key field is not valid base64: the file is damaged or was altered [" + type(exc).__name__ + "]"
    if type(exc) is ValueError and detail:
        return detail
    return type(exc).__name__ + ": " + detail


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



def fingerprint_argument(value):
    text = re.sub(r"[\s:]", "", value).lower()
    if not re.fullmatch(r"[a-f0-9]{64}", text):
        raise argparse.ArgumentTypeError("expected a SHA-256 fingerprint of 64 hexadecimal digits; upper case, spaces and colons are accepted")
    return text


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
STREEBOG_PI = bytes.fromhex(
    "fceedd11cf6e3116fbc4fada23c5044de977f0db932e99ba1736f1bb14cd5fc1f918655ae25cef21811c3c428b018e4f058402aee36a8fa0"
    "060bed987fd4d31feb342c51eac848abf22a68a2fd3aceccb5700e56080c7612bf7213479cb75d8715a19629107b9ac7f391786f9d9eb2b1"
    "3275193dff358a7e6d54c680c3bd0d57dff524a93ea843c9d779d6f67c22b903e00fecde7a94b0bcdce828504e330a4aa79760731e006244"
    "1ab83882649f2641ad454692275e552f8ca3a57d69d5953b0758b34086ac1df730376be488d9e789e11b83494c3ff8fe8d53aa90cad88561"
    "207167a42d2b095bcb9b25d0bee56c5259a674d2e6f4b4c0d166afc2394b63b6")
STREEBOG_A = bytes.fromhex(
    "8e20faa72ba0b47047107ddd9b505a38ad08b0e0c3282d1cd8045870ef14980e6c022c38f90a4c073601161cf205268d1b8e0b0e798c13c8"
    "83478b07b2468764a011d380818e8f405086e740ce47c9202843fd2067adea1014aff010bdd875080ad97808d06cb40405e23c0468365a02"
    "8c711e02341b2d0146b60f011a83988e90dab52a387ae76f486dd4151c3dfdb924b86a840e90f0d2125c354207487869092e94218d243cba"
    "8a174a9ec8121e5d4585254f64090fa0accc9ca9328a89509d4df05d5f661451c0a878a0a1330aa660543c50de970553302a1e286fc58ca7"
    "18150f14b9ec46dd0c84890ad27623e00642ca05693b9f700321658cba93c13886275df09ce8aaa8439da0784e745554afc0503c273aa42a"
    "d960281e9d1d5215e230140fc080298471180a8960409a42b60c05ca30204d215b068c651810a89e456c34887a3805b9ac361a443d1c8cd2"
    "561b0d22900e46692b838811480723ba9bcf4486248d9f5dc3e9224312c8c1a0effa11af0964ee50f97d86d98a327728e4fa2054a80b329c"
    "727d102a548b194e39b008152acb82279258048415eb419d492c024284fbaec0aa16012142f35760550b8e9e21f7a530a48b474f9ef5dc18"
    "70a6a56e2440598e3853dc371220a2471ca76e95091051ad0edd37c48a08a6d807e095624504536c8d70c431ac02a736c83862965601dd1b"
    "641c314b2b8ee083")
STREEBOG_C = bytes.fromhex(
    "b1085bda1ecadae9ebcb2f81c0657c1f2f6a76432e45d016714eb88d7585c4fc4b7ce09192676901a2422a08a460d31505767436cc744d23"
    "dd806559f2a645076fa3b58aa99d2f1a4fe39d460f70b5d7f3feea720a232b9861d55e0f16b501319ab5176b12d699585cb561c2db0aa7ca"
    "55dda21bd7cbcd56e679047021b19bb7f574dcac2bce2fc70a39fc286a3d843506f15e5f529c1f8bf2ea7514b1297b7bd3e20fe490359eb1"
    "c1c93a376062db09c2b6f443867adb31991e96f50aba0ab2ef1fdfb3e81566d2f948e1a05d71e4dd488e857e335c3c7d9d721cad685e353f"
    "a9d72c82ed03d675d8b71333935203be3453eaa193e837f1220cbebc84e3d12e4bea6bacad4747999a3f410c6ca923637f151c1f1686104a"
    "359e35d7800fffbdbfcd1747253af5a3dfff00b723271a167a56a27ea9ea63f5601758fd7c6cfe57ae4faeae1d3ad3d96fa4c33b7a3039c0"
    "2d66c4f95142a46c187f9ab49af08ec6cffaa6b71c9ab7b40af21f66c2bec6b6bf71c57236904f35fa68407a46647d6ef4c70e16eeaac5ec"
    "51ac86febf240954399ec6c7e6bf87c9d3473e33197a93c90992abc52d822c3706476983284a05043517454ca23c4af38886564d3a14d493"
    "9b1f5b424d93c9a703e7aa020c6e41414eb7f8719c36de1e89b4443b4ddbc49af4892bcb929b069069d18d2bd1a5c42f36acc2355951a8d9"
    "a47f0dd4bf02e71e378f5a541631229b944c9ad8ec165fde3a7d3a1b258942243cd955b7e00d0984800a440bdbb2ceb17b2b8a9aa6079c54"
    "0e38dc92cb1f2a607261445183235adbabbedea680056f52382ae548b2e4f3f38941e71cff8a78db1fffe18a1b3361039fe76702af69334b"
    "7a1e6c303b7652f43698fad1153bb6c374b4c7fb98459ced7bcd9ed0efc889fb3002c6cd635afe94d8fa6bbbebab07612001802114846679"
    "8a1d71efea48b9caefbacd1d7d476e98dea2594ac06fd85d6bcaa4cd81f32d1b378ee767f11631bad21380b00449b17acda43c32bcdf1d77"
    "f82012d430219f9b5d80ef9d1891cc86e71da4aa88e12852faf417d5d9b21b9948bc924af11bd720")
KUPYNA_S0 = bytes.fromhex(
    "a8435f066b756c5971df879517f0d8096df31dcbc94d2caf79e097fd6f4b45393edda34fb4b69a0e1fbf15e149d293c692729e61d163faee"
    "f419d5ad58a4bba1dcf2833742e47a329cccab4a8f6e04272ee7e25a9616232bc265660fbca947413448fcb76a88a55386f95bdb387bc31e"
    "2233242836c7b23b8e77baf5149f08559b4cfe605cda1846cd7d21b03f1b89ffeb84693a9dd7d3706740b5de5d3091b1781101e5006898a0"
    "c502a6742d0ba276b3becebdaee98a311cecf19994aaf6262fefe88c3503d47ffb05c15e90203d82f7ea0a0d7ef8501ac40757b83c62e3c8"
    "ac526410d0d9130c122951b9cfd6738d8154c0ed4e44a72a8525e6ca7c8b5680")
KUPYNA_S1 = bytes.fromhex(
    "cebbeb92eacb13c1e93ad6b2d29017f8421556b4651c8843c55c36baf557678d31f664589ef422aa750f02b1df6d734d7c262ef7085d443e"
    "9f14c8ae5410d8bc1a6b69f3bd33abfad19b684e169591ee4c638e5bcc3c19a181497bd96f3760cae72b48fd9645fc41120d79e5898ce320"
    "30dcb76c4ab53f97d4622d06a4a5835f2adac9007ea255bf11d59ccf0e0a3d517d931bfec44709860b8f9d6a07b9b0981832714bef3b70a0"
    "e440ffc3a9e678f98b46801e38e1b8a8e00c23761d252405f16e94289a84e8a34f77d385e252f282507a2f7453b361af3935decd1f99acad"
    "722cddd087be5ea6ec04c60334fbdb59b6c201f05aeda766217f8a27c7c029d7")
KUPYNA_S2 = bytes.fromhex(
    "93d99ab5982245fcba6adf029fdc51594a172bc294f4bba362e471d4cd7016e1493cc0d85c9bad8553a17ac82de0d172a62cc4e37678b7b4"
    "093b0e414cdeb29025a5d7031100c32e92ef4e129d7dcb3510d54f9e4da955c6d07b1897d336e64856818f77cc9cb9e2acb82f15a47cda38"
    "1e0b05d6146e6c7e66fdb1e560af5e3387c9f05d6d3f888dc7f71de9eced802927cf99a8500f3724283095d23e5b4083b369571f071c8abc"
    "20ebce8eabee31a273f9ca3a1afb0dc1fefaf26fbd96dd4352b608f3aebe19893226b0ea4b6484826bf579bf015f75631b233d682a65e891"
    "f6ff1358f1470a7fc5a7e7615a0646444204a0db398654aa8c34218bf80c7467")
KUPYNA_S3 = bytes.fromhex(
    "688dca4d734b4e2ad45226b3541e191f2203463d2d4a5383138ab7d52579f5bd582f0d02ed519e11f23e555ed1163c66705df34540cce894"
    "5608ce1a3ad2e1dfb5386e0ee5f4f986e94fd68523cf32993114aeeec848d330a19241b118c42c71724415fd37be5faa9b88d8ab899cfa60"
    "eabc620c24a6a8ec6720db7c28ddac5b347e10f17b8f63a0059a437721bf2709c39fb6d729c2ebc0a48b8c1dfbffc1b2972ef865f6750704"
    "4933e4d9b9d042c76c90008e6f5001c5da473fcd69a2e27aa7c6930f0a06e62b96a31caf6a128439e7b082f7fe9d875c8135deb4a5fc80ef"
    "cbbb6b76ba5a7d780b95e3ad74983b36646ddcf059a94c177f91b8c9571be061")
DSTU_DKE = bytes.fromhex("a9d6eb45f13c708280c4967b231f5eadf658eba4c037291d38d96bf025ca4e17"
                         "f8e9720dc615b43a28975f0bc1dea36438b564ea2c179fd0123e6db8fac57904")
GOST34311 = "1.2.804.2.1.1.1.1.2.1"
KUPYNA = {"1.2.804.2.1.1.1.1.2.2.1": 256, "1.2.804.2.1.1.1.1.2.2.2": 384, "1.2.804.2.1.1.1.1.2.2.3": 512}
STREEBOG = {"1.2.643.7.1.1.2.2": 256, "1.2.643.7.1.1.2.3": 512}
SM3 = "1.2.156.10197.1.401"
DIGEST_NAMES = {GOST34311: "gost34311", SM3: "sm3", **{k: "kupyna-" + str(v) for k, v in KUPYNA.items()},
                **{k: "streebog-" + str(v) for k, v in STREEBOG.items()}}
DSTU_KEYS = {"1.2.804.2.1.1.1.1.3.1.1": "little", "1.2.804.2.1.1.1.1.3.1.1.1.1": "big"}
DSTU_SIGNATURES = {"1.2.804.2.1.1.1.1.3.1.1": ("little", GOST34311), "1.2.804.2.1.1.1.1.3.1.1.1.1": ("big", GOST34311),
                   **{"1.2.804.2.1.1.1.1.3.6.%d.1" % i: ("little", h) for i, h in enumerate(KUPYNA, 1)},
                   **{"1.2.804.2.1.1.1.1.3.6.%d.1.1.1" % i: ("big", h) for i, h in enumerate(KUPYNA, 1)}}
GOST_KEYS = {"1.2.643.7.1.1.1.1": 32, "1.2.643.7.1.1.1.2": 64}
GOST_SIGNATURES = {"1.2.643.7.1.1.3.2": (32, "1.2.643.7.1.1.2.2"), "1.2.643.7.1.1.3.3": (64, "1.2.643.7.1.1.2.3"),
                   "1.2.643.7.1.1.1.1": (32, "1.2.643.7.1.1.2.2"), "1.2.643.7.1.1.1.2": (64, "1.2.643.7.1.1.2.3")}
SM2_SIGNATURE, SM2_CURVE, EC_PUBLIC_KEY = "1.2.156.10197.1.501", "1.2.156.10197.1.301", "1.2.840.10045.2.1"
SM2_DEFAULT_ID = b"1234567812345678"
NATIONAL_SIGNATURES = {*DSTU_SIGNATURES, *GOST_SIGNATURES, SM2_SIGNATURE}
NATIONAL_TABLES = {}


class Unsupported(ValueError):
    pass


def gost_curve(*values):
    return tuple(int(value, 16) for value in values)


GOST_CURVE_CPA = gost_curve(
    "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd97",
    "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd94", "a6",
    "ffffffffffffffffffffffffffffffff6c611070995ad10045841b09b761b893", "1",
    "8d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14")
GOST_CURVE_CPB = gost_curve(
    "8000000000000000000000000000000000000000000000000000000000000c99",
    "8000000000000000000000000000000000000000000000000000000000000c96",
    "3e1af419a269a5f866a7d3c25c3df80ae979259373ff2b182f49d4ce7e1bbc8b",
    "800000000000000000000000000000015f700cfff1a624e5e497161bcc8a198f", "1",
    "3fa8124359f96680b83d1c3eb2c070e5c545c9858d03ecfb744bf8d717717efc")
GOST_CURVE_CPC = gost_curve(
    "9b9f605f5a858107ab1ec85e6b41c8aacf846e86789051d37998f7b9022d759b",
    "9b9f605f5a858107ab1ec85e6b41c8aacf846e86789051d37998f7b9022d7598", "805a",
    "9b9f605f5a858107ab1ec85e6b41c8aa582ca3511eddfb74f02f3a6598980bb9", "0",
    "41ece55743711a8c3cbf3783cd08c0ee4d4dc440d4641a8f366e550dfdb3bb67")
GOST_CURVES = {
    "1.2.643.7.1.2.1.1.1": gost_curve(
        "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd97",
        "c2173f1513981673af4892c23035a27ce25e2013bf95aa33b22c656f277e7335",
        "295f9bae7428ed9ccc20e7c359a9d41a22fccd9108e17bf7ba9337a6f8ae9513",
        "400000000000000000000000000000000fd8cddfc87b6635c115af556c360c67",
        "91e38443a5e82c0d880923425712b2bb658b9196932e02c78b2582fe742daa28",
        "32879423ab1a0375895786c4bb46e9565fde0b5344766740af268adb32322e5c"),
    "1.2.643.7.1.2.1.1.2": GOST_CURVE_CPA, "1.2.643.7.1.2.1.1.3": GOST_CURVE_CPB, "1.2.643.7.1.2.1.1.4": GOST_CURVE_CPC,
    "1.2.643.2.2.35.1": GOST_CURVE_CPA, "1.2.643.2.2.35.2": GOST_CURVE_CPB, "1.2.643.2.2.35.3": GOST_CURVE_CPC,
    "1.2.643.2.2.36.0": GOST_CURVE_CPA, "1.2.643.2.2.36.1": GOST_CURVE_CPC,
    "1.2.643.7.1.2.1.2.1": gost_curve(
        "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffdc7",
        "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffdc4",
        "e8c2505dedfc86ddc1bd0b2b6667f1da34b82574761cb0e879bd081cfd0b6265"
        "ee3cb090f30d27614cb4574010da90dd862ef9d4ebee4761503190785a71c760",
        "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        "27e69532f48d89116ff22b8d4e0560609b4b38abfad2b85dcacdb1411f10b275", "3",
        "7503cfe87a836ae3a61b8816e25450e6ce5e1c93acf1abc1778064fdcbefa921"
        "df1626be4fd036e93d75e6a50e3a41e98028fe5fc235f5b889a589cb5215f2a4"),
    "1.2.643.7.1.2.1.2.2": gost_curve(
        "8000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000006f",
        "8000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000006c",
        "687d1b459dc841457e3e06cf6f5e2517b97c7d614af138bcbf85dc806c4b289f"
        "3e965d2db1416d217f8b276fad1ab69c50f78bee1fa3106efb8ccbc7c5140116",
        "8000000000000000000000000000000000000000000000000000000000000001"
        "49a1ec142565a545acfdb77bd9d40cfa8b996712101bea0ec6346c54374f25bd", "2",
        "1a8f7eda389b094c2c071e3647a8940f3c123b697578c213be6dd9e6c8ec7335"
        "dcb228fd1edf4a39152cbcaaf8c0398828041055f94ceeec7e21340780fe41bd"),
    "1.2.643.7.1.2.1.2.3": gost_curve(
        "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffdc7",
        "dc9203e514a721875485a529d2c722fb187bc8980eb866644de41c68e1430645"
        "46e861c0e2c9edd92ade71f46fcf50ff2ad97f951fda9f2a2eb6546f39689bd3",
        "b4c4ee28cebc6c2c8ac12952cf37f16ac7efb6a9f69f4b57ffda2e4f0de5ade0"
        "38cbc2fff719d2c18de0284b8bfef3b52b8cc7a5f5bf0a3c8d2319a5312557e1",
        "3fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        "c98cdba46506ab004c33a9ff5147502cc8eda9e7a769a12694623cef47f023ed",
        "e2e31edfc23de7bdebe241ce593ef5de2295b7a9cbaef021d385f7074cea043a"
        "a27272a7ae602bf2a7b9033db9ed3610c6fb85487eae97aac5bc7928c1950148",
        "f5ce40d95b5eb899abbccff5911cb8577939804d6527378b8c108c3d2090ff9b"
        "e18e2d33e3021ed2ef32d85822423b6304f726aa854bae07d0396e9a9addc40f"),
}
SM2_CURVE_PARAMS = gost_curve(
    "fffffffeffffffffffffffffffffffffffffffff00000000ffffffffffffffff",
    "fffffffeffffffffffffffffffffffffffffffff00000000fffffffffffffffc",
    "28e9fa9e9d9f5e344d5a9e4bcf6509a7f39789f515ab8f92ddbcbd414d940e93",
    "fffffffeffffffffffffffffffffffff7203df6b21c6052b53bbf40939d54123",
    "32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7",
    "bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0")
DSTU_CURVES = [
    (163, (7, 6, 3, 0), 1, "5ff6108462a2dc8210ab403925e638a19c1455d21", "400000000000000000002bec12be2262d39bcf14d", 2,
     "2e2f85f5dd74ce983a5c4237229daf8a3f35823be", "3826f008a8c51d7b95284d9d03ff0e00ce2cd723a"),
    (167, (6, 0), 1, "6ee3ceeb230811759f20518a0930f1a4315a827dac", "3fffffffffffffffffffffb12ebcc7d7f29ff7701f", 2,
     "7a1f6653786a68192803910a3d30b2a2018b21cd54", "5f49eb26781c0ec6b8909156d98ed435e45fd59918"),
    (173, (10, 2, 1, 0), 0, "108576c80499db2fc16eddf6853bbb278f6b6fb437d9", "800000000000000000000189b4e67606e3825bb2831",
     4, "4d41a619bcc6eadf0448fa22fad567a9181d37389ca", "10b51cc12849b234c75e6dd2028bf7ff5c1ce0d991a1"),
    (179, (4, 2, 1, 0), 1, "4a6e0856526436f2f88dd07a341e32d04184572beb710", "3ffffffffffffffffffffffb981960435fe5ab64236ef",
     2, "6ba06fe51464b2bd26dc57f48819ba9954667022c7d03", "25fbc363582dcec065080ca8287aaff09788a66dc3a9e"),
    (191, (9, 0), 1, "7bc86e2102902ec4d5890e8b6b4981ff27e0482750fefc03", "40000000000000000000000069a779cac1dabc6788f7474f",
     2, "714114b762f2ff4a7912a6d2ac58b9b5c2fcfe76daeb7129", "29c41e568b77c617efe5902f11db96fa9613cd8d03db08da"),
    (233, (9, 4, 1, 0), 1, "06973b15095675534c7cf7e64a21bd54ef5dd3b8a0326aa936ece454d2c",
     "1000000000000000000000000000013e974e72f8a6922031d2603cfe0d7", 2,
     "3fcda526b6cdf83ba1118df35b3c31761d3545f32728d003eeb25efe96",
     "9ca8b57a934c54deeda9e54a7bbad95e3b2e91c54d32be0b9df96d8d35"),
    (257, (12, 0), 0, "1cef494720115657e18f938d7a7942394ff9425c1458c57861f9eea6adbe3be10",
     "800000000000000000000000000000006759213af182e987d3e17714907d470d", 4,
     "02a29ef207d0e9b6c55cd260b306c7e007ac491ca1b10c62334a9e8dcd8d20fb7",
     "10686d41ff744d4449fccf6d8eea03102e6812c93a9d60b978b702cf156d814ef"),
    (307, (8, 4, 2, 0), 1, "393c7f7d53666b5054b5e6c6d3de94f4296c0c599e2e2e241050df18b6090bdc90186904968bb",
     "3ffffffffffffffffffffffffffffffffffffffc079c2f3825da70d390fbba588d4604022b7b7", 2,
     "216ee8b189d291a0224984c1e92f1d16bf75ccd825a087a239b276d3167743c52c02d6e7232aa",
     "5d9306bacd22b7faeb09d2e049c6e2866c5d1677762a8f2f2dc9a11c7f7be8340ab2237c7f2a0"),
    (367, (21, 0), 1, "43fc8ad242b0b7a6f3d1627ad5654447556b47bf6aa4a64b0c2afe42cadab8f93d92394c79a79755437b56995136",
     "40000000000000000000000000000000000000000000009c300b75a3fa824f22428fd28ce8812245ef44049b2d49", 2,
     "324a6eddd512f08c49a99ae0d3f961197a76413e7be81a400ca681e09639b5fe12e59a109f78bf4a373541b3b9a1",
     "1ab597a5b4477f59e39539007c7f977d1a567b92b043a49c6b61984c3fe3481aaf454cd41ba1f051626442b3c10"),
    (431, (5, 3, 1, 0), 1,
     "03ce10490f6a708fc26dfe8c3d27c4f94e690134d5bff988d8d28aaeaede975936c66bac536b18ae2dc312ca493117daa469c640caf3",
     "3fffffffffffffffffffffffffffffffffffffffffffffffffffffba3175458009a8c0a724f02f81aa8a1fcbaf80d90c7a95110504cf", 2,
     "1a62ba79d98133a16bbae7ed9a8e03c32e0824d57aef72f88986874e5aae49c27bed49a2a95058068426c2171e99fd3b43c5947c857d",
     "70b5e1e14031c1f70bbefe96bdde66f451754b4ca5f48da241f331aa396b8d1839a855c1769b1ea14ba53308b5e2723724e090e02db9"),
]
DSTU_NAMED = {"1.2.804.2.1.1.1.1.3.1.1.2." + str(index): index for index in range(len(DSTU_CURVES))}
EVEN_HEX = str.maketrans("0123456789abcdef", "0101010101010101")


def streebog_tables():
    if "streebog" not in NATIONAL_TABLES:
        rows = [int.from_bytes(STREEBOG_A[8 * i:8 * i + 8], "big") for i in range(64)]

        def linear(value):
            out = 0
            for bit in range(64):
                if value >> bit & 1:
                    out ^= rows[63 - bit]
            return out
        NATIONAL_TABLES["streebog"] = (
            [[linear(STREEBOG_PI[byte] << 8 * k) for byte in range(256)] for k in range(8)],
            [int.from_bytes(STREEBOG_C[64 * i:64 * i + 64], "big") for i in range(12)])
    return NATIONAL_TABLES["streebog"]


def streebog_lps(value, tables):
    data = value.to_bytes(64, "little")
    out = 0
    for j in range(8):
        word = 0
        for k in range(8):
            word ^= tables[k][data[8 * k + j]]
        out |= word << 64 * j
    return out


def streebog_g(tables, constants, counter, state, block):
    key = streebog_lps(state ^ counter, tables)
    value = block
    for constant in constants:
        value = streebog_lps(value ^ key, tables)
        key = streebog_lps(key ^ constant, tables)
    return value ^ key ^ state ^ block


def streebog(data, bits):
    tables, constants = streebog_tables()
    mask = (1 << 512) - 1
    state, counter, total = (0 if bits == 512 else int.from_bytes(b"\x01" * 64, "big")), 0, 0
    data = bytes(data)
    full = len(data) // 64 * 64
    for offset in range(0, full, 64):
        block = int.from_bytes(data[offset:offset + 64], "little")
        state = streebog_g(tables, constants, counter, state, block)
        counter, total = (counter + 512) & mask, (total + block) & mask
    rest = data[full:]
    block = int.from_bytes(rest + b"\x01", "little")
    state = streebog_g(tables, constants, counter, state, block)
    counter, total = (counter + 8 * len(rest)) & mask, (total + block) & mask
    state = streebog_g(tables, constants, 0, state, counter)
    state = streebog_g(tables, constants, 0, state, total)
    return state.to_bytes(64, "little") if bits == 512 else (state >> 256).to_bytes(32, "little")


def gost28147_tables(sbox):
    rows = [[sbox[8 * row + j // 2] >> 4 if j % 2 == 0 else sbox[8 * row + j // 2] & 15 for j in range(16)]
            for row in range(8)]
    tables = []
    for k in range(4):
        table = []
        for byte in range(256):
            value = (rows[2 * k][byte & 15] | rows[2 * k + 1][byte >> 4] << 4) << 8 * k
            table.append((value << 11 | value >> 21) & 0xFFFFFFFF)
        tables.append(table)
    return tables


def gost28147_encrypt(tables, key, block):
    keys = [key >> 32 * i & 0xFFFFFFFF for i in range(8)]
    t0, t1, t2, t3 = tables
    low, high = block & 0xFFFFFFFF, block >> 32
    for subkey in keys * 3 + keys[::-1]:
        value = (low + subkey) & 0xFFFFFFFF
        low, high = high ^ t0[value & 255] ^ t1[value >> 8 & 255] ^ t2[value >> 16 & 255] ^ t3[value >> 24], low
    return high | low << 32


def gost94_permute(value):
    data = value.to_bytes(32, "little")
    return int.from_bytes(bytes(data[8 * (o % 4) + o // 4] for o in range(32)), "little")


def gost94_step(tables, state, block):
    mask64 = (1 << 64) - 1
    shift = lambda x: x >> 64 | ((x ^ x >> 64) & mask64) << 192
    u, v = state, block
    keys = [gost94_permute(u ^ v)]
    for constant in (0, 0xFF00FFFF000000FFFF0000FF00FFFF0000FF00FF00FF00FFFF00FF00FF00FF00, 0):
        u, v = shift(u) ^ constant, shift(shift(v))
        keys.append(gost94_permute(u ^ v))
    mixed = 0
    for i, key in enumerate(keys):
        mixed |= gost28147_encrypt(tables, key, state >> 64 * i & mask64) << 64 * i

    def psi(x, times):
        for _ in range(times):
            feedback = x ^ x >> 16 ^ x >> 32 ^ x >> 48 ^ x >> 192 ^ x >> 240
            x = x >> 16 | (feedback & 0xFFFF) << 240
        return x
    return psi(state ^ psi(block ^ psi(mixed, 12), 1), 61)


def gost34311(data, sbox=DSTU_DKE):
    key = "gost28147:" + bytes(sbox).hex()
    if key not in NATIONAL_TABLES:
        NATIONAL_TABLES[key] = gost28147_tables(bytes(sbox))
    tables, mask = NATIONAL_TABLES[key], (1 << 256) - 1
    data = bytes(data)
    state, total, offset = 0, 0, 0
    while len(data) - offset > 32:
        block = int.from_bytes(data[offset:offset + 32], "little")
        state, total, offset = gost94_step(tables, state, block), (total + block) & mask, offset + 32
    block = int.from_bytes(data[offset:], "little")
    total = (total + block) & mask
    state = gost94_step(tables, state, block)
    state = gost94_step(tables, state, 8 * len(data) & mask)
    return gost94_step(tables, state, total).to_bytes(32, "little")


def gf256_mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        a, b = (a << 1) ^ (0x11D if a & 0x80 else 0), b >> 1
    return out


def kupyna_tables():
    if "kupyna" not in NATIONAL_TABLES:
        boxes, row = (KUPYNA_S0, KUPYNA_S1, KUPYNA_S2, KUPYNA_S3), (1, 1, 5, 1, 8, 6, 7, 4)
        NATIONAL_TABLES["kupyna"] = [[sum(gf256_mul(row[(i - r) % 8], boxes[i % 4][byte]) << 8 * r for r in range(8))
                                      for byte in range(256)] for i in range(8)]
    return NATIONAL_TABLES["kupyna"]


def kupyna_mix(columns, tables, shifts):
    count = len(columns)
    return [tables[0][columns[j] & 255] ^ tables[1][columns[(j - shifts[1]) % count] >> 8 & 255]
            ^ tables[2][columns[(j - shifts[2]) % count] >> 16 & 255] ^ tables[3][columns[(j - shifts[3]) % count] >> 24 & 255]
            ^ tables[4][columns[(j - shifts[4]) % count] >> 32 & 255] ^ tables[5][columns[(j - shifts[5]) % count] >> 40 & 255]
            ^ tables[6][columns[(j - shifts[6]) % count] >> 48 & 255] ^ tables[7][columns[(j - shifts[7]) % count] >> 56]
            for j in range(count)]


def kupyna_xor(columns, rounds, tables, shifts):
    for step in range(rounds):
        columns = kupyna_mix([value ^ (j << 4 ^ step) for j, value in enumerate(columns)], tables, shifts)
    return columns


def kupyna_add(columns, rounds, tables, shifts):
    count = len(columns)
    for step in range(rounds):
        columns = kupyna_mix([(value + (0x00F0F0F0F0F0F0F3 ^ ((count - 1 - j) << 4 ^ step) << 56)) & 0xFFFFFFFFFFFFFFFF
                              for j, value in enumerate(columns)], tables, shifts)
    return columns


def kupyna(data, bits):
    tables = kupyna_tables()
    count, rounds = (8, 10) if bits <= 256 else (16, 14)
    shifts, size = (0, 1, 2, 3, 4, 5, 6, 7 if count == 8 else 11), 8 * count
    data = bytes(data)
    data += b"\x80" + bytes((-len(data) - 13) % size) + (8 * (len(data))).to_bytes(12, "little")
    state = [size] + [0] * (count - 1)
    for offset in range(0, len(data), size):
        block = [int.from_bytes(data[offset + 8 * j:offset + 8 * j + 8], "little") for j in range(count)]
        mixed = kupyna_xor([a ^ b for a, b in zip(state, block)], rounds, tables, shifts)
        state = [a ^ b ^ c for a, b, c in zip(mixed, kupyna_add(block, rounds, tables, shifts), state)]
    state = [a ^ b for a, b in zip(kupyna_xor(state, rounds, tables, shifts), state)]
    return b"".join(value.to_bytes(8, "little") for value in state)[-bits // 8:]


def sm3(data):
    rotate = lambda x, n: (x << n | x >> 32 - n) & 0xFFFFFFFF if n % 32 else x
    data = bytes(data)
    length = 8 * len(data)
    data += b"\x80" + bytes((55 - len(data)) % 64) + length.to_bytes(8, "big")
    state = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600, 0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]
    for offset in range(0, len(data), 64):
        words = [int.from_bytes(data[offset + 4 * i:offset + 4 * i + 4], "big") for i in range(16)]
        for j in range(16, 68):
            x = words[j - 16] ^ words[j - 9] ^ rotate(words[j - 3], 15)
            words.append(x ^ rotate(x, 15) ^ rotate(x, 23) ^ rotate(words[j - 13], 7) ^ words[j - 6])
        a, b, c, d, e, f, g, h = state
        for j in range(64):
            ss1 = rotate((rotate(a, 12) + e + rotate(0x79CC4519 if j < 16 else 0x7A879D8A, j % 32)) & 0xFFFFFFFF, 7)
            ss2 = ss1 ^ rotate(a, 12)
            ff = a ^ b ^ c if j < 16 else (a & b) | (a & c) | (b & c)
            gg = e ^ f ^ g if j < 16 else (e & f) | (~e & g)
            tt1 = (ff + d + ss2 + (words[j] ^ words[j + 4])) & 0xFFFFFFFF
            tt2 = (gg + h + ss1 + words[j]) & 0xFFFFFFFF
            a, b, c, d = tt1, a, rotate(b, 9), c
            e, f, g, h = tt2 ^ rotate(tt2, 9) ^ rotate(tt2, 17), e, rotate(f, 19), g
        state = [x ^ y for x, y in zip(state, (a, b, c, d, e, f, g, h))]
    return b"".join(value.to_bytes(4, "big") for value in state)


def digest(oid, data):
    if oid == GOST34311:
        return gost34311(data)
    if oid in KUPYNA:
        return kupyna(data, KUPYNA[oid])
    if oid in STREEBOG:
        return streebog(data, STREEBOG[oid])
    if oid == SM3:
        return sm3(data)
    raise Unsupported("Unsupported digest algorithm " + str(oid))


def prime_on_curve(curve, point):
    p, a, b = curve[:3]
    x, y = point
    return 0 <= x < p and 0 <= y < p and (y * y - x * x * x - a * x - b) % p == 0


def prime_affine_add(curve, first, second):
    p, a = curve[:2]
    if first is None or second is None:
        return first or second
    (x1, y1), (x2, y2) = first, second
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    slope = ((3 * x1 * x1 + a) * pow(2 * y1, -1, p) if first == second else (y2 - y1) * pow(x2 - x1, -1, p)) % p
    x3 = (slope * slope - x1 - x2) % p
    return x3, (slope * (x1 - x3) - y1) % p


def prime_double(curve, point):
    p, a = curve[:2]
    x, y, z = point
    if not y:
        return None
    yy, zz = y * y % p, z * z % p
    s, m = 4 * x * yy % p, (3 * x * x + a * zz * zz) % p
    x3 = (m * m - 2 * s) % p
    return x3, (m * (s - x3) - 8 * yy * yy) % p, 2 * y * z % p


def prime_add(curve, point, other):
    p = curve[0]
    if point is None:
        return other[0], other[1], 1
    x1, y1, z1 = point
    zz = z1 * z1 % p
    h, r = (other[0] * zz - x1) % p, (other[1] * zz * z1 - y1) % p
    if not h:
        return prime_double(curve, (other[0], other[1], 1)) if not r else None
    hh = h * h % p
    hhh, v = h * hh % p, x1 * hh % p
    x3 = (r * r - hhh - 2 * v) % p
    return x3, (r * (v - x3) - y1 * hhh) % p, z1 * h % p


def prime_combination(curve, k1, first, k2, second):
    p = curve[0]
    both = prime_affine_add(curve, first, second)
    point = None
    for bit in range(max(k1.bit_length(), k2.bit_length()) - 1, -1, -1):
        if point is not None:
            point = prime_double(curve, point)
        pick = (k1 >> bit & 1, k2 >> bit & 1)
        other = {(1, 0): first, (0, 1): second, (1, 1): both}.get(pick)
        if other is not None:
            point = prime_add(curve, point, other)
    if point is None or not point[2]:
        return None
    inverse = pow(point[2], -1, p)
    return point[0] * inverse * inverse % p, point[1] * inverse * inverse * inverse % p


def gost_verify(curve, key, digest_value, signature):
    p, a, b, q, gx, gy = curve
    half = len(signature) // 2
    s, r = int.from_bytes(signature[:half], "big"), int.from_bytes(signature[half:], "big")
    if len(signature) % 2 or not (0 < r < q and 0 < s < q) or not prime_on_curve(curve, key):
        return False
    e = int.from_bytes(digest_value, "little") % q or 1
    v = pow(e, -1, q)
    point = prime_combination(curve, s * v % q, (gx, gy), -r * v % q, key)
    return point is not None and point[0] % q == r


def sm2_verify(curve, key, message, signature, identity=SM2_DEFAULT_ID):
    p, a, b, n, gx, gy = curve
    r, s = signature
    if not (0 < r < n and 0 < s < n) or not prime_on_curve(curve, key) or len(identity) >= 8192:
        return False
    size = (p.bit_length() + 7) // 8
    z = sm3((8 * len(identity)).to_bytes(2, "big") + identity
            + b"".join(value.to_bytes(size, "big") for value in (a, b, gx, gy, key[0], key[1])))
    e = int.from_bytes(sm3(z + bytes(message)), "big")
    t = (r + s) % n
    if not t:
        return False
    point = prime_combination(curve, s, (gx, gy), t, key)
    return point is not None and (e + point[0]) % n == r


def bin_mul(a, b, field):
    if not a or not b:
        return 0
    spread = lambda x: int("00000000000".join(format(x, "b")), 2)
    lanes = a.bit_length() + b.bit_length() - 1
    product = format(spread(a) * spread(b), "x").zfill(3 * lanes)
    return bin_reduce(int(product[2::3].translate(EVEN_HEX), 2), field)


def bin_square(a, field):
    return bin_reduce(int("0".join(format(a, "b")), 2), field) if a else 0


def bin_reduce(value, field):
    m, low = field
    while value >> m:
        top = value >> m
        value &= (1 << m) - 1
        for exponent in low:
            value ^= top << exponent
    return value


def bin_inverse(a, field):
    m, low = field
    u, v, g1, g2 = a, (1 << m) | sum(1 << e for e in low), 1, 0
    while u != 1:
        shift = u.bit_length() - v.bit_length()
        if shift < 0:
            u, v, g1, g2, shift = v, u, g2, g1, -shift
        u, g1 = u ^ v << shift, g1 ^ g2 << shift
    return bin_reduce(g1, field)


def bin_trace(a, field):
    total, value = 0, a
    for _ in range(field[0]):
        total ^= value
        value = bin_square(value, field)
    return total & 1


def bin_half_trace(a, field):
    total, value = 0, a
    for _ in range((field[0] - 1) // 2 + 1):
        total ^= value
        value = bin_square(bin_square(value, field), field)
    return total


def bin_affine_add(curve, first, second):
    field, a = curve[:2]
    if first is None or second is None:
        return first or second
    (x1, y1), (x2, y2) = first, second
    if x1 == x2:
        if y1 != y2 or not x1:
            return None
        slope = x1 ^ bin_mul(y1, bin_inverse(x1, field), field)
        x3 = bin_square(slope, field) ^ slope ^ a
        return x3, bin_square(x1, field) ^ bin_mul(slope ^ 1, x3, field)
    slope = bin_mul(y1 ^ y2, bin_inverse(x1 ^ x2, field), field)
    x3 = bin_square(slope, field) ^ slope ^ x1 ^ x2 ^ a
    return x3, bin_mul(slope, x1 ^ x3, field) ^ x3 ^ y1


def bin_double(curve, point):
    field, a, b = curve[:3]
    x, y, z = point
    if not x or not z:
        return None
    xx, zz = bin_square(x, field), bin_square(z, field)
    z3 = bin_mul(xx, zz, field)
    bz4 = bin_mul(b, bin_square(zz, field), field)
    x3 = bin_square(xx, field) ^ bz4
    return x3, bin_mul(bz4, z3, field) ^ bin_mul(x3, bin_mul(a, z3, field) ^ bin_square(y, field) ^ bz4, field), z3


def bin_add(curve, point, other):
    field, a = curve[:2]
    x2, y2 = other
    if point is None:
        return x2, y2, 1
    x1, y1, z1 = point
    zz = bin_square(z1, field)
    p = bin_mul(y2, zz, field) ^ y1
    q = bin_mul(x2, z1, field) ^ x1
    if not q:
        return bin_double(curve, (x2, y2, 1)) if not p else None
    c = bin_mul(z1, q, field)
    d = bin_mul(bin_square(q, field), c ^ bin_mul(a, zz, field), field)
    z3 = bin_square(c, field)
    e = bin_mul(p, c, field)
    x3 = bin_square(p, field) ^ d ^ e
    f = x3 ^ bin_mul(x2, z3, field)
    return x3, bin_mul(e ^ z3, f, field) ^ bin_mul(x2 ^ y2, bin_square(z3, field), field), z3


def bin_combination(curve, k1, first, k2, second):
    field = curve[0]
    both = bin_affine_add(curve, first, second)
    point = None
    for bit in range(max(k1.bit_length(), k2.bit_length()) - 1, -1, -1):
        if point is not None:
            point = bin_double(curve, point)
        other = {(1, 0): first, (0, 1): second, (1, 1): both}.get((k1 >> bit & 1, k2 >> bit & 1))
        if other is not None:
            point = bin_add(curve, point, other)
    if point is None or not point[2]:
        return None
    inverse = bin_inverse(point[2], field)
    return bin_mul(point[0], inverse, field), bin_mul(point[1], bin_square(inverse, field), field)


def bin_on_curve(curve, point):
    field, a, b = curve[:3]
    x, y = point
    xx = bin_square(x, field)
    return (x >> field[0] == 0 and y >> field[0] == 0
            and bin_square(y, field) ^ bin_mul(x, y, field) == bin_mul(xx, x ^ a, field) ^ b)


def bin_decompress(curve, value):
    field, a, b = curve[:3]
    if not value or value >> field[0]:
        return None
    x = value & ~1
    if bin_trace(x, field) != bin_trace(a, field):
        x ^= 1
    if not x:
        return None
    w = bin_mul(x, bin_square(x, field), field) ^ bin_mul(a, bin_square(x, field), field) ^ b
    v = bin_mul(w, bin_inverse(bin_square(x, field), field), field)
    z = bin_half_trace(v, field)
    if bin_square(z, field) ^ z != v:
        return None
    if bin_trace(z, field) != value & 1:
        z ^= 1
    return x, bin_mul(z, x, field)


def dstu_curve(index):
    m, low, a, b, n, cofactor, x, y = DSTU_CURVES[index]
    return (m, low), a, int(b, 16), int(n, 16), (int(x, 16), int(y, 16)), cofactor


def dstu_verify(curve, key, digest_value, signature, order="little"):
    field, a, b, n, base = curve[:5]
    size = n.bit_length()
    if len(signature) % 2 or 16 * len(signature) < 4 * size or not bin_on_curve(curve, key):
        return False
    whole, half = int.from_bytes(signature, order), 4 * len(signature)
    r, s = whole & ((1 << half) - 1), whole >> half
    if not (0 < r < n and 0 < s < n):
        return False
    h = int.from_bytes(digest_value, "little") & ((1 << field[0]) - 1) or 1
    point = bin_combination(curve, s, base, r, key)
    return point is not None and bin_mul(h, point[0], field) & ((1 << size - 1) - 1) == r


def dstu_parameters(data, start, end, order):
    items = children(data, start, end)
    if not 1 <= len(items) <= 2 or len(items) == 2 and (items[1][0] != 0x04 or items[1][3] - items[1][2] != 64):
        raise ValueError("Malformed DSTU 4145 parameters")
    sbox = data[items[1][2]:items[1][3]] if len(items) == 2 else DSTU_DKE
    if items[0][0] == 0x06:
        name = oid(data, *items[0][2:])
        if name not in DSTU_NAMED:
            raise Unsupported("Unsupported DSTU 4145 curve " + name)
        return dstu_curve(DSTU_NAMED[name]), sbox
    if items[0][0] != 0x30:
        raise ValueError("Malformed DSTU 4145 parameters")
    fields = children(data, items[0][2], items[0][3])
    if fields and fields[0][0] == 0xA0:
        if data[fields[0][2]:fields[0][3]] != b"\x02\x01\x00":
            raise Unsupported("Unsupported DSTU 4145 parameter version")
        fields = fields[1:]
    if [tag for tag, *_ in fields] != [0x30, 0x02, 0x04, 0x02, 0x04]:
        raise ValueError("Malformed DSTU 4145 parameters")
    number = lambda item: int.from_bytes(data[item[2]:item[3]], "big", signed=True)
    basis = children(data, fields[0][2], fields[0][3])
    if len(basis) != 2 or basis[0][0] != 0x02 or basis[1][0] not in (0x02, 0x30):
        raise ValueError("Malformed DSTU 4145 parameters")
    exponents = [basis[1]] if basis[1][0] == 0x02 else children(data, basis[1][2], basis[1][3])
    field = number(basis[0]), tuple(sorted((number(item) for item in exponents), reverse=True)) + (0,)
    a, b, n = number(fields[1]), int.from_bytes(data[fields[2][2]:fields[2][3]], order), number(fields[3])
    for index, known in enumerate(DSTU_CURVES):
        curve = dstu_curve(index)
        if curve[:4] == (field, a, b, n):
            base = bin_decompress(curve, int.from_bytes(data[fields[4][2]:fields[4][3]], order))
            if base is None or base != curve[4] and bin_combination(curve, n, base, 0, base) is not None:
                raise ValueError("The DSTU 4145 base point is not a point of the curve's prime order")
            return (field, a, b, n, base, curve[5]), sbox
    raise Unsupported("Unsupported DSTU 4145 curve parameters")


def public_key(spki):
    tag, start, end = der(spki, 0)
    parts = children(spki, start, end) if tag == 0x30 and end == len(spki) else []
    if len(parts) != 2 or parts[0][0] != 0x30 or parts[1][0] != 0x03 or spki[parts[1][2]] != 0:
        raise ValueError("Malformed public key")
    algorithm = children(spki, parts[0][2], parts[0][3])
    if not algorithm or algorithm[0][0] != 0x06:
        raise ValueError("Malformed public key")
    name, bits = oid(spki, *algorithm[0][2:]), spki[parts[1][2] + 1:parts[1][3]]
    params = algorithm[1] if len(algorithm) == 2 else None
    if name in DSTU_KEYS or name in GOST_KEYS:
        if params is None or params[0] != 0x30:
            raise ValueError("Malformed public key parameters")
        inner = der(bits, 0)
        if inner[0] != 0x04 or inner[2] != len(bits):
            raise ValueError("Malformed public key")
        value = bits[inner[1]:]
    if name in DSTU_KEYS:
        order = DSTU_KEYS[name]
        curve, sbox = dstu_parameters(spki, params[2], params[3], order)
        point = bin_decompress(curve, int.from_bytes(value, order))
        if point is None:
            raise ValueError("The DSTU 4145 public key is not a point of the curve")
        return "dstu", curve, point, sbox
    if name in GOST_KEYS:
        size, sets = GOST_KEYS[name], children(spki, params[2], params[3])
        if not sets or sets[0][0] != 0x06:
            raise ValueError("Malformed public key parameters")
        curve = GOST_CURVES.get(oid(spki, *sets[0][2:]))
        if curve is None:
            raise Unsupported("Unsupported GOST R 34.10-2012 parameter set " + oid(spki, *sets[0][2:]))
        if len(value) != 2 * size or (curve[0].bit_length() + 7) // 8 != size:
            raise ValueError("The GOST R 34.10-2012 key length does not match its parameters")
        return "gost", curve, (int.from_bytes(value[:size], "little"), int.from_bytes(value[size:], "little")), size
    if name == EC_PUBLIC_KEY and params is not None and params[0] == 0x06 and oid(spki, *params[2:]) == SM2_CURVE:
        if len(bits) != 65 or bits[0] != 4:
            raise Unsupported("Only uncompressed SM2 public keys are supported")
        return "sm2", SM2_CURVE_PARAMS, (int.from_bytes(bits[1:33], "big"), int.from_bytes(bits[33:], "big"))
    raise Unsupported("Unsupported public key algorithm " + name)


def sm2_signature(signature):
    tag, start, end = der(signature, 0)
    values = children(signature, start, end) if tag == 0x30 and end == len(signature) else []
    if len(values) != 2 or any(item[0] != 0x02 or signature[item[2]] & 0x80 for item in values):
        raise ValueError("Malformed SM2 signature")
    return tuple(int.from_bytes(signature[item[2]:item[3]], "big") for item in values)


def verify(spki_der, signature_algorithm_oid, signature, message):
    if signature_algorithm_oid not in NATIONAL_SIGNATURES:
        raise Unsupported("Unsupported signature algorithm " + str(signature_algorithm_oid))
    try:
        key, signature, message = public_key(bytes(spki_der)), bytes(signature), bytes(message)
        if signature_algorithm_oid in DSTU_SIGNATURES:
            order, hashing = DSTU_SIGNATURES[signature_algorithm_oid]
            if key[0] != "dstu":
                return False
            value = gost34311(message, key[3]) if hashing == GOST34311 else digest(hashing, message)
            return dstu_verify(key[1], key[2], value, signature, order)
        if signature_algorithm_oid in GOST_SIGNATURES:
            size, hashing = GOST_SIGNATURES[signature_algorithm_oid]
            if key[0] != "gost" or key[3] != size or len(signature) != 2 * size:
                return False
            return gost_verify(key[1], key[2], digest(hashing, message), signature)
        return key[0] == "sm2" and sm2_verify(key[1], key[2], message, sm2_signature(signature))
    except Unsupported:
        raise
    except (ValueError, IndexError, TypeError, ZeroDivisionError):
        return False


def certificate_fields(data):
    tag, start, end = der(data, 0)
    parts = children(data, start, end) if tag == 0x30 and end == len(data) else []
    if len(parts) != 3 or parts[0][0] != 0x30 or parts[1][0] != 0x30 or parts[2][0] != 0x03:
        raise ValueError("Malformed signed structure")
    algorithm = children(data, parts[1][2], parts[1][3])
    if not algorithm or algorithm[0][0] != 0x06 or data[parts[2][2]] != 0:
        raise ValueError("Malformed signed structure")
    return data[parts[0][1]:parts[0][3]], oid(data, *algorithm[0][2:]), data[parts[2][2] + 1:parts[2][3]]


def tbs_key(tbs):
    _, start, end = der(tbs, 0)
    items = children(tbs, start, end)
    index = 6 if items and items[0][0] == 0xA0 else 5
    if len(items) <= index or items[index][0] != 0x30:
        raise ValueError("Malformed certificate")
    return tbs[items[index][1]:items[index][3]]


def signed_value(spki, algorithm, value, tbs):
    if algorithm not in NATIONAL_SIGNATURES:
        raise Unsupported("Unsupported signature algorithm " + str(algorithm))
    if algorithm in DSTU_SIGNATURES:
        try:
            tag, start, end = der(value, 0)
        except (ValueError, IndexError):
            return False
        if tag != 0x04 or end != len(value):
            return False
        value = value[start:end]
    return verify(spki, algorithm, value, tbs)


def signed_by(data, issuer):
    try:
        tbs, algorithm, value = certificate_fields(bytes(data))
        key = tbs_key(certificate_fields(bytes(issuer))[0])
    except Unsupported:
        raise
    except (ValueError, IndexError):
        return False
    return signed_value(key, algorithm, value, tbs)
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


def timestamp_reply_summary(reply, digest, query=None, data=None):
    token = timestamp_token(reply)
    info = tst_info(token["tst"])
    expected = digest if info["algorithm"] == "2.16.840.1.101.3.4.2.1" else (
        hashed(info["algorithm"], data) if data is not None and info["algorithm"] in DIGEST_NAMES else None)
    if expected is None or info["hash"] != expected:
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


def hashed(algorithm, data):
    if isinstance(algorithm, str):
        if algorithm in DIGEST_NAMES:
            return digest(algorithm, data)
        algorithm = DIGESTS[algorithm]
    hasher = hashes.Hash(algorithm())
    hasher.update(data)
    return hasher.finalize()


def certificate_fingerprint(algorithm, data):
    if isinstance(algorithm, str):
        return digest(algorithm, data)
    return x509.load_der_x509_certificate(data).fingerprint(algorithm())


def issued_by(certificate, issuer):
    method = certificate.signature_algorithm_oid.dotted_string
    if method not in NATIONAL_SIGNATURES:
        return certificate.verify_directly_issued_by(issuer)
    if certificate.issuer != issuer.subject:
        raise ValueError("The certificate names a different issuer")
    if not signed_value(tbs_key(issuer.tbs_certificate_bytes), method, certificate.signature,
                        certificate.tbs_certificate_bytes):
        raise InvalidSignature()


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
        algorithm = oid(reply, *children(reply, identifiers[0][2], identifiers[0][3])[0][2:])
        algorithm = DIGESTS.get(algorithm) or (algorithm if algorithm in DIGEST_NAMES else None)
        identifiers = identifiers[1:]
    if algorithm is None or identifiers[0][0] != 0x04:
        raise ValueError("Unsupported signing certificate reference")
    reference = DIGEST_NAMES[algorithm] if isinstance(algorithm, str) else algorithm().name
    return algorithm, reply[identifiers[0][2]:identifiers[0][3]], reference


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
    content_digest = oid(reply, *children(reply, items[2][2], items[2][3])[0][2:])
    if content_digest not in DIGESTS and content_digest not in DIGEST_NAMES:
        raise ValueError("Unsupported timestamp digest algorithm")
    attributes = signed_attributes(reply, items[3][2], items[3][3])
    content_type, message_digest = attributes.get(CONTENT_TYPE), attributes.get(MESSAGE_DIGEST)
    if not content_type or oid(reply, *content_type[0][2:]) != TST_INFO:
        raise ValueError("The signed attributes do not describe a TSTInfo")
    if not message_digest or reply[message_digest[0][2]:message_digest[0][3]] != hashed(content_digest, token["tst"]):
        raise ValueError("The signature does not cover this TSTInfo")
    algorithm, named, reference = signing_certificate_hash(reply, attributes)
    raw = {}
    for data in token["certificates"]:
        raw[data] = x509.load_der_x509_certificate(data)
    signer_data = None
    for data in raw:
        if certificate_fingerprint(algorithm, data) == named:
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
    if method in NATIONAL_SIGNATURES:
        if not verify(tbs_key(signer.tbs_certificate_bytes), method, signature, signed):
            raise ValueError("The timestamp signature is invalid")
    else:
        try:
            key = signer.public_key()
        except UnsupportedAlgorithm:
            raise ValueError("Unsupported timestamp signature algorithm " + method) from None
        try:
            if isinstance(key, rsa.RSAPublicKey) and method in RSA_SIGNATURES and (
                    RSA_SIGNATURES[method] or content_digest in DIGESTS):
                key.verify(signature, signed, padding.PKCS1v15(), (RSA_SIGNATURES[method] or DIGESTS[content_digest])())
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
        issuer, unsupported = None, None
        for candidate in candidates:
            if candidate.subject != current.issuer:
                continue
            try:
                issued_by(current, candidate)
            except (Unsupported, UnsupportedAlgorithm):
                unsupported = current.signature_algorithm_oid.dotted_string
                continue
            except (ValueError, TypeError, InvalidSignature):
                continue
            issuer = candidate
            break
        if issuer is None and unsupported:
            raise ValueError("Unsupported signature algorithm or parameters in the timestamp certificate chain: "
                             + unsupported)
        if issuer is None:
            raise ValueError(TSA_UNTRUSTED)
        try:
            constraints = issuer.extensions.get_extension_for_class(x509.BasicConstraints).value
        except x509.ExtensionNotFound:
            constraints = None
        if not constraints or not constraints.ca:
            raise ValueError("A certificate in the timestamp chain is not a certificate authority")
        chain.append(issuer)
        current = issuer
    for certificate in chain:
        if not utc_time(certificate, "not_valid_before") <= when <= utc_time(certificate, "not_valid_after"):
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


def tsa_paths(tsa_ca):
    return [tsa_ca] if isinstance(tsa_ca, (str, Path)) else list(tsa_ca or ())


def tsa_roots(tsa_ca):
    roots = []
    for path in tsa_paths(tsa_ca):
        data = Path(path).read_bytes()
        try:
            found = x509.load_pem_x509_certificates(data)
        except ValueError:
            found = [x509.load_der_x509_certificate(data)]
        if not found:
            raise ValueError("The --tsa-ca file " + str(path) + " holds no certificate")
        roots += found
    if not roots:
        raise ValueError("The --tsa-ca file holds no certificate")
    return roots


TSA_CHECKED = "checked against the given root"
TSA_NO_MATCHING_ROOT = "no matching root in --tsa-ca"
TSA_UNTRUSTED = "The timestamp certificate does not chain to a trusted root"


def tsa_signature_check(reply, roots):
    try:
        checked = timestamp_signature(reply, roots)
    except ValueError as exc:
        if str(exc) == TSA_UNTRUSTED:
            return TSA_NO_MATCHING_ROOT, None
        raise
    return TSA_CHECKED, checked["signer_sha256"]


def qualified_timestamp(reply, signer_sha256):
    service = QUALIFIED_TSU.get(signer_sha256 or "")
    if not service:
        return {}
    for data in timestamp_token(reply)["certificates"]:
        certificate = x509.load_der_x509_certificate(data)
        if certificate.fingerprint(hashes.SHA256()).hex() != signer_sha256:
            continue
        try:
            statements = certificate.extensions.get_extension_for_oid(x509.ObjectIdentifier(QC_STATEMENTS)).value.value
        except x509.ExtensionNotFound:
            return {}
        if QC_COMPLIANCE in statements:
            return {"qualified": {"service": service, "provider": QUALIFIED_PROVIDER, "trusted_list": QUALIFIED_LIST,
                                  "signer_sha256": signer_sha256}}
        return {}
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
        if certificate_fingerprint(algorithm, data) == named:
            signer = loaded[data]
    certificates = list(loaded.values())
    if signer is None:
        raise ValueError("The reply does not carry the certificate the signature names")
    for candidate in certificates + list(extra):
        if candidate.subject != signer.issuer:
            continue
        try:
            issued_by(signer, candidate)
        except (ValueError, TypeError, InvalidSignature, UnsupportedAlgorithm):
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
                    or not utc_time(candidate, "not_valid_before") <= utc_time(response, "produced_at") <= utc_time(candidate, "not_valid_after")):
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
        revoked = utc_time(found, "revocation_time") if found.certificate_status == ocsp.OCSPCertStatus.REVOKED else None
        reason, issued, until = found.revocation_reason, utc_time(found, "this_update"), utc_time(found, "next_update")
    elif kind == "crl":
        try:
            crl = x509.load_der_x509_crl(data)
        except ValueError:
            crl = x509.load_pem_x509_crl(data)
        if crl.issuer != issuer.subject or not crl.is_signature_valid(issuer.public_key()):
            raise ValueError("The CRL is not signed by the issuer of the signing certificate")
        entry = crl.get_revoked_certificate_by_serial_number(signer.serial_number)
        revoked = utc_time(entry, "revocation_date") if entry else None
        reason = next((e.value.reason for e in entry.extensions if isinstance(e.value, x509.CRLReason)), None) if entry else None
        issued, until = utc_time(crl, "last_update"), utc_time(crl, "next_update")
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
    if issued > utc_time(signer, "not_valid_after"):
        raise ValueError("The " + source + " answer was issued after the signing certificate expired")
    return {"status": "good", "source": source, "as_of": stamp_time(issued),
            "detail": "signing certificate not revoked as of " + stamp_time(issued) + " (" + source + ")"}


def timestamp_revocation(archive, names, base, reply, tsa_ca=None):
    found = [kind for kind in ("ocsp", "crl") if base + "." + kind in names]
    if not found:
        return {"status": "not checked", "detail": "revocation not checked (no OCSP/CRL in the archive)"}
    extra = []
    for path in tsa_paths(tsa_ca):
        try:
            extra += x509.load_pem_x509_certificates(Path(path).read_bytes())
        except (OSError, ValueError):
            pass
    try:
        subject = revocation_subject(reply, extra)
    except (ValueError, TypeError, IndexError, InvalidSignature, UnsupportedAlgorithm) as exc:
        return {"status": "failed", "error": str(exc), "detail": "revocation check failed: " + str(exc)}
    states, problems = [], []
    for kind in found:
        try:
            states.append(revocation_status(kind, read_member(archive, base + "." + kind), subject))
        except (ValueError, TypeError, IndexError, InvalidSignature, UnsupportedAlgorithm) as exc:
            problems.append(kind.upper() + ": " + str(exc))
    revoked = [state for state in states if state["status"] == "revoked"]
    if revoked:
        return revoked[0]
    if problems:
        return {"status": "invalid", "error": "; ".join(problems),
                "detail": "revocation data present but not valid for this time stamp: " + "; ".join(problems)}
    return next((state for state in states if state["status"] == "revoked_after"), None) \
        or max(states, key=lambda state: state["as_of"])


def verify_anchors(archive, names, public_key, event_count, hash_at, tsa_ca=None, check_bitcoin=False):
    results = []
    roots = tsa_roots(tsa_ca) if tsa_paths(tsa_ca) else None
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
                entry.update(kind="rfc3161", **timestamp_reply_summary(reply, digest, query, data))
                entry["signature"], signer = tsa_signature_check(reply, roots) if roots else ("not checked (use --tsa-ca)", None)
                if entry["signature"] == TSA_CHECKED:
                    entry.update(qualified_timestamp(reply, signer))
                try:
                    entry.update(timestamp_certificate_reference(reply))
                except (ValueError, IndexError, TypeError):
                    entry["certificate_reference"] = "unavailable"
                entry["revocation"] = timestamp_revocation(archive, names, proof_name[:-4], reply, tsa_ca)
                if entry["revocation"]["status"] == "revoked":
                    raise ValueError("The " + service + " timestamp is invalid: its " + entry["revocation"]["detail"]
                                     + ("; reason " + entry["revocation"]["reason"] if entry["revocation"]["reason"] else ""))
                if entry["revocation"]["status"] == "invalid":
                    raise ValueError("The revocation data stored with the " + service + " timestamp is not valid for it: "
                                     + entry["revocation"]["error"])
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
    if utc_time(crl, "last_update") > at or utc_time(crl, "next_update") is not None and at > utc_time(crl, "next_update"):
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
            if not utc_time(checked, "not_valid_before") <= at <= utc_time(checked, "not_valid_after"):
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
    at = max([at] + moments + [utc_time(x509.load_der_x509_crl(data), "last_update") for data in crl_data])
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
    status = "pass"
    if found["tcb"] is None:
        status, found["tcb"] = "partial", {
            "status": "not checked", "detail": "TCB status not checked (no collateral in the " + source + ")",
            "revocation": "not checked",
            **({"collector_error": str(evidence["collateral_error"])[:200]} if evidence.get("collateral_error") else {})}
    return {"status": status, **found, "binds": binds}


def tdx_summary(quotes):
    states = {q["status"] for q in quotes}
    return {"status": "pass" if states == {"pass"} else "partial" if states <= {"pass", "partial"} else "fail",
            "checked": "offline",
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
        if quote["status"] not in ("pass", "partial"):
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


ERS_RECORD = re.compile(r"anchors/(checkpoint-\d{12,})(?:\.renewal-(\d{1,6}))?\.ers")
ERS_CONTAINER = "META-INF/evidencerecord.ers"
ERS_SHA2 = {"2.16.840.1.101.3.4.2.1": "SHA-256", "2.16.840.1.101.3.4.2.2": "SHA-384",
            "2.16.840.1.101.3.4.2.3": "SHA-512"}


def ers_algorithm_name(algorithm):
    return ERS_SHA2.get(algorithm) or DIGEST_NAMES.get(algorithm) or algorithm


def ers_tlv(tag, body):
    size = len(body)
    if size < 0x80:
        return bytes([tag, size]) + body
    length = size.to_bytes((size.bit_length() + 7) // 8, "big")
    return bytes([tag, 0x80 | len(length)]) + length + body


def ers_reply(token):
    return ers_tlv(0x30, ers_tlv(0x30, b"\x02\x01\x00") + token)


def ers_algorithm(data, start, end):
    items = children(data, start, end)
    if not items or items[0][0] != 0x06:
        raise ValueError("Malformed hash algorithm in the evidence record")
    found = oid(data, *items[0][2:])
    if found not in DIGESTS and found not in DIGEST_NAMES:
        raise ValueError("Unsupported hash algorithm in the evidence record: " + found)
    return found


def ers_signer(reply, token):
    try:
        items = children(reply, token["signer"][2], token["signer"][3])
        if len(items) < 4 or items[3][0] != 0xA0:
            return None
        algorithm, named, _ = signing_certificate_hash(reply, signed_attributes(reply, items[3][2], items[3][3]))
        for data in token["certificates"]:
            if certificate_fingerprint(algorithm, data) == named:
                return x509.load_der_x509_certificate(data)
    except (ValueError, TypeError, IndexError, KeyError):
        return None
    return None


def ers_stamp(data, start, value_start, end):
    fields = children(data, value_start, end)
    tags = [tag for tag, *_ in fields[:-1]]
    if not fields or fields[-1][0] != 0x30 or tags != sorted(set(tags)) or not set(tags) <= {0xA0, 0xA1, 0xA2}:
        raise ValueError("Malformed ArchiveTimeStamp")
    token = data[fields[-1][1]:fields[-1][3]]
    reply = ers_reply(token)
    found = timestamp_token(reply)
    info = tst_info(found["tst"])
    algorithm, partials = None, []
    for tag, _, field_start, field_end in fields[:-1]:
        if tag == 0xA0:
            algorithm = ers_algorithm(data, field_start, field_end)
        elif tag == 0xA2:
            for kind, _, list_start, list_end in children(data, field_start, field_end):
                values = children(data, list_start, list_end)
                if kind != 0x30 or not values or any(value[0] != 0x04 for value in values):
                    raise ValueError("Malformed reduced hash tree")
                partials.append([data[s:e] for _, _, s, e in values])
    if algorithm is None:
        if info["algorithm"] not in DIGESTS and info["algorithm"] not in DIGEST_NAMES:
            raise ValueError("Unsupported hash algorithm in the evidence record: " + info["algorithm"])
        algorithm = info["algorithm"]
    if info["algorithm"] != algorithm:
        raise ValueError("A time stamp in the evidence record uses a different hash algorithm than its hash tree")
    return {"raw": data[start:end], "token": token, "reply": reply, "partials": partials, "algorithm": algorithm,
            "hash": info["hash"], "time": info["time"], "signer": ers_signer(reply, found)}


def ers_parse(data):
    tag, start, end = der(data, 0)
    if tag != 0x30 or end != len(data):
        raise ValueError("Not an RFC 4998 evidence record")
    items = children(data, start, end)
    if (len(items) < 3 or items[0][0] != 0x02 or data[items[0][2]:items[0][3]] != b"\x01" or items[1][0] != 0x30
            or items[-1][0] != 0x30 or [tag for tag, *_ in items[2:-1]] not in ([], [0xA0])):
        raise ValueError("Not an RFC 4998 evidence record version 1, or an encrypted one")
    declared = [ers_algorithm(data, s, e) for _, _, s, e in children(data, items[1][2], items[1][3])]
    chains = []
    for kind, chain_start, value_start, value_end in children(data, items[-1][2], items[-1][3]):
        if kind != 0x30:
            raise ValueError("Malformed ArchiveTimeStampChain")
        stamps = []
        for stamp_kind, stamp_start, stamp_value, stamp_end in children(data, value_start, value_end):
            if stamp_kind != 0x30:
                raise ValueError("Malformed ArchiveTimeStamp")
            stamps.append(ers_stamp(data, stamp_start, stamp_value, stamp_end))
        if not stamps:
            raise ValueError("Empty ArchiveTimeStampChain")
        chains.append({"raw": data[chain_start:value_end], "algorithm": stamps[0]["algorithm"], "stamps": stamps})
    if not chains:
        raise ValueError("Empty ArchiveTimeStampSequence")
    return {"algorithms": declared, "chains": chains}


def ers_node(algorithm, values):
    return values[0] if len(values) == 1 else hashed(algorithm, b"".join(sorted(values)))


def ers_root(algorithm, values, partials):
    if not partials:
        if len(values) != 1:
            raise ValueError("A data group needs a reduced hash tree")
        return values[0]
    if any(value not in partials[0] for value in values):
        raise ValueError("A data object is not in the first hash list of the reduced hash tree")
    current = ers_node(algorithm, partials[0])
    for siblings in partials[1:]:
        current = ers_node(algorithm, [current, *siblings])
    return current


def ers_check(data, measure, roots=None, now=None):
    record = ers_parse(data)
    previous, stamps, other, signatures = [], [], 0, []
    for index, chain in enumerate(record["chains"]):
        algorithm, where = chain["algorithm"], " of chain " + str(index + 1)
        if algorithm not in record["algorithms"]:
            raise ValueError("Chain " + str(index + 1) + " uses a hash algorithm the evidence record does not declare")
        sequence = hashed(algorithm, ers_tlv(0x30, b"".join(previous)))
        for position, stamp in enumerate(chain["stamps"]):
            if stamp["algorithm"] != algorithm:
                raise ValueError("Chain " + str(index + 1) + " mixes hash algorithms")
            if position:
                values = [hashed(algorithm, chain["stamps"][position - 1]["token"])]
            elif index:
                values = [hashed(algorithm, value + sequence) for value in measure(algorithm)]
            else:
                values = measure(algorithm)
            if ers_root(algorithm, values, stamp["partials"]) != stamp["hash"]:
                raise ValueError("ArchiveTimeStamp " + str(position + 1) + where + " does not cover its data")
            if not index and not position and stamp["partials"]:
                other = len([value for value in stamp["partials"][0] if value not in values])
            if roots is not None:
                status, last_signer = tsa_signature_check(stamp["reply"], roots)
                signatures.append(status)
            if stamps and stamp["time"] < stamps[-1]["time"]:
                raise ValueError("ArchiveTimeStamp " + str(position + 1) + where + " is older than the one it renews")
            stamps.append(stamp)
        previous.append(chain["raw"])
    late, proven = [], 0
    for position in range(1, len(stamps)):
        signer = stamps[position - 1]["signer"]
        if signer is not None and stamps[position]["time"] > utc_time(signer, "not_valid_after"):
            late.append({"time": stamp_time(stamps[position]["time"]),
                         "previous_expired": stamp_time(utc_time(signer, "not_valid_after"))})
            proven = position
    newest, now = stamps[-1], now or datetime.now(timezone.utc)
    expires = utc_time(newest["signer"], "not_valid_after") if newest["signer"] is not None else None
    protection = {"time": stamp_time(newest["time"]), "algorithm": ers_algorithm_name(newest["algorithm"]),
                  "signer": newest["signer"].subject.rfc4514_string() if newest["signer"] is not None else None,
                  "expires": stamp_time(expires) if expires else None,
                  "state": "unknown" if expires is None else "in force" if now <= expires else "expired"}
    if signatures and signatures[-1] == TSA_CHECKED:
        protection.update(qualified_timestamp(newest["reply"], last_signer))
    chains = record["chains"]
    signature = ("not checked (use --tsa-ca)" if roots is None else TSA_CHECKED if set(signatures) == {TSA_CHECKED}
                 else TSA_NO_MATCHING_ROOT)
    return {"record": record, "signature": signature, "chains": len(chains), "stamps": len(stamps),
            "timestamp_renewals": len(stamps) - len(chains), "hash_tree_renewals": len(chains) - 1,
            "algorithms": [ers_algorithm_name(chain["algorithm"]) for chain in chains],
            "earliest": stamp_time(stamps[0]["time"]), "proven_from": stamp_time(stamps[proven]["time"]),
            "late_renewals": late, "newest": protection, "other_hashes": other}


def ers_extends(before, after):
    old, new = before["chains"], after["chains"]
    if len(new) < len(old) or any(
            [s["raw"] for s in new[i]["stamps"][:len(chain["stamps"])]] != [s["raw"] for s in chain["stamps"]]
            or (i < len(old) - 1 and new[i]["raw"] != chain["raw"]) for i, chain in enumerate(old)):
        raise ValueError("A renewal changes the earlier evidence")


def ers_stream(archive, name, algorithm):
    if algorithm not in DIGESTS:
        return hashed(algorithm, read_member(archive, name, MAX_JSON_BYTES))
    hasher = hashes.Hash(DIGESTS[algorithm]())
    with archive.open(name) as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.finalize()


def ers_entry(summary, roots):
    return {**{key: value for key, value in summary.items() if key != "record"},
            "signature": summary.get("signature") or ("not checked (use --tsa-ca)" if roots is None else TSA_CHECKED)}


def verify_evidence_records(archive, names, container=(), tsa_ca=None, now=None):
    roots = tsa_roots(tsa_ca) if tsa_ca else None
    found = {}
    for name in names:
        match = ERS_RECORD.fullmatch(name)
        if match:
            found.setdefault(match[1], []).append((int(match[2] or 0), name))
    entries = []
    for stem, files in sorted(found.items()):
        checkpoint = "anchors/" + stem + ".json"
        if checkpoint not in names:
            raise ValueError("Evidence record without its checkpoint: " + files[0][1])
        data = read_member(archive, checkpoint)
        measure = lambda algorithm, data=data: [hashed(algorithm, data)]
        summary = before = None
        for _, name in sorted(files):
            try:
                summary = ers_check(read_member(archive, name), measure, roots, now)
                if before is not None:
                    ers_extends(before, summary["record"])
            except (ValueError, TypeError, IndexError, KeyError) as exc:
                raise ValueError("Evidence record " + name + " is invalid: " + str(exc)) from None
            before = summary["record"]
        statement = strict_json(data).get("statement") or {}
        entries.append({"subject": "checkpoint", "checkpoint": stem + ".json", "event_count": statement.get("event_count"),
                        "files": [name for _, name in sorted(files)], **ers_entry(summary, roots)})
    if ERS_CONTAINER in container:
        objects = sorted(name for name in names if name != "mimetype" and not name.startswith("META-INF/"))
        measured = {}

        def measure(algorithm):
            if algorithm not in measured:
                measured[algorithm] = [ers_stream(archive, name, algorithm) for name in objects]
            return measured[algorithm]
        try:
            summary = ers_check(read_member(archive, ERS_CONTAINER), measure, roots, now)
        except (ValueError, TypeError, IndexError, KeyError) as exc:
            raise ValueError("Evidence record " + ERS_CONTAINER + " is invalid: " + str(exc)) from None
        entries.append({"subject": "export", "file": ERS_CONTAINER, "files_covered": len(objects),
                        **ers_entry(summary, roots)})
    if not entries:
        return None
    earliest = min(entries, key=lambda entry: entry["proven_from"])
    weakest = min(entries, key=lambda entry: (entry["newest"]["state"] == "in force",
                                              entry["newest"]["expires"] or "", entry["newest"]["time"]))
    return {"records": entries,
            "earliest": {"time": earliest["proven_from"], "subject": earliest["subject"],
                         "event_count": earliest.get("event_count")},
            "newest": weakest["newest"],
            "signature": "not checked (use --tsa-ca)" if roots is None else TSA_CHECKED if all(
                entry["signature"] == TSA_CHECKED for entry in entries) else TSA_NO_MATCHING_ROOT}


def ers_lines(records, t):
    rows, checked = [], records["signature"].startswith("checked")
    shown = lambda value: str(value).replace("T", " ").replace("Z", " UTC")
    points = [entry for entry in records["records"] if entry["subject"] == "checkpoint"]
    if points:
        numbers = sorted(int(item["checkpoint"][11:-5]) for item in points)
        rows.append((points, t("checkpoints: {n} (#{first}–#{last})", n=len(points), first=numbers[0],
                                 last=numbers[-1]) if len(points) > 1 else t("checkpoint #{n}", n=numbers[0])))
    rows += [([entry], t("{n} export files", n=entry["files_covered"]))
             for entry in records["records"] if entry["subject"] == "export"]
    lines = []
    for group, subject in rows:
        late = [item for entry in group for item in entry["late_renewals"]]
        states = {entry["newest"]["state"] for entry in group}
        state = "ok" if checked and not late and states == {"in force"} else "warn"
        detail = subject + " · " + t("{chains} chain(s), {stamps} time stamp(s) · renewals: {timestamp} time stamp, "
                                     "{tree} hash tree", chains=sum(e["chains"] for e in group),
                                     stamps=sum(e["stamps"] for e in group),
                                     timestamp=sum(e["timestamp_renewals"] for e in group),
                                     tree=sum(e["hash_tree_renewals"] for e in group))
        notes = [t("hash trees, renewals and order checked; data objects covered")]
        notes.append(t("signature chained to your root" if checked else "signature not checked: add --tsa-ca"))
        notes.append(t("revocation not checked (no OCSP/CRL in the archive)"))
        first = min(group, key=lambda entry: entry["proven_from"])
        when = shown(first["proven_from"]) + (" (" + t("records 1–{n}", n=first["event_count"]) + ")"
                                              if first.get("event_count") else "")
        notes.append(t("earliest proven time: {time}", time=when) if checked
                     else t("earliest time stated by the time stamps: {time}", time=when))
        newest = min((entry["newest"] for entry in group),
                     key=lambda item: (item["state"] == "in force", item["expires"] or "", item["time"]))
        text = t("newest protection: {algorithm} · time stamp of {time}", algorithm=newest["algorithm"],
                 time=shown(newest["time"]))
        if newest["state"] == "in force":
            text += " · " + t("signing certificate valid until {time}", time=shown(newest["expires"]))
        elif newest["state"] == "expired":
            text += " · " + t("signing certificate expired {time}: renew with a new time stamp",
                              time=shown(newest["expires"]))
        else:
            text += " · " + t("the token does not carry its signing certificate")
        notes.append(text)
        lines.append((state, "Evidence records (RFC 4998)", detail, notes))
        lines += [("warn", "Timestamp warning",
                   t("renewed at {time}, after the previous signing certificate expired ({expired}): earlier times "
                     "are not proven", time=shown(item["time"]), expired=shown(item["previous_expired"])), [])
                  for item in late]
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
        elif kind == "session.takeover_risk" and isinstance(payload.get("risks"), list):
            names = [r["kind"] for r in payload["risks"] if isinstance(r, dict) and isinstance(r.get("kind"), str)]
            if names:
                s.setdefault("takeover_risks", []).append({"at": at, "risks": names})
        elif kind == "account.security_event":
            counts = s.setdefault("security_events", {})
            name = str(payload.get("event_kind") or "security_notice")
            counts[name] = counts.get(name, 0) + 1
        elif kind == "account.all_other_sessions_terminated":
            s.setdefault("other_sessions_ended", []).append({
                "at": at, "ended": payload.get("sessions_before"), "count": payload.get("sessions_ended"),
                "kept_approver": payload.get("kept_approving_session") is True,
                "interrupted": payload.get("interrupted_by") if isinstance(payload.get("interrupted_by"), str) else None})
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


SCOPE_REASONS = ("Private chats, bots and ordinary groups share one account-wide numbering. It can be measured only "
                 "while whole-account collection is on; this journal has no such period.",
                 "Private chats, bots, ordinary groups and the account's own messages take numbers from the same "
                 "sequence, so the measurement needs a scope recorded as including all of them without excluded chats.")


def scope_reason(scope):
    return SCOPE_REASONS[0] if not isinstance(scope, dict) or scope.get("mode") != "account" else SCOPE_REASONS[1]


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
        if item.get("kept_approver") or item.get("interrupted"):
            lines.append("Other sessions ended from this workspace at " + item["at"]
                         + (": " + str(item["count"]) + " of " + str(item["ended"])
                            if isinstance(item.get("count"), int) and isinstance(item.get("ended"), int) else "")
                         + ("; the session that approved this workspace's sign-in was kept" if item.get("kept_approver") else "")
                         + ("; stopped by " + item["interrupted"] if item.get("interrupted") else ""))
            continue
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
             for p in coverage["continuous"]] or ["No observation period recorded."]
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
    return lines + extra


COMPLETENESS_FORMAT = "tgwitness-sequence-continuity-v1"
COMPLETENESS_KINDS = ("coverage.sequence", "coverage.gap", "coverage.gap_closed")
COMPLETENESS_METHODS = ("push", "getDifference", "getChannelDifference")
COMPLETENESS_CHANNEL_BASE = -1000000000000
COMPLETENESS_LISTED = 20
COMPLETENESS_PROVES = ("Telegram numbers message-related updates with pts: one sequence for the account (private chats "
                       "and basic groups together) and one per channel or supergroup. An unbroken stretch proves that "
                       "every update Telegram numbered in that sequence between its first and last pts reached this "
                       "collector's Telegram client, pushed live or returned by getDifference or getChannelDifference.")
COMPLETENESS_LIMITS = ("It says nothing about content Telegram never sent to this account, about intervals before the "
                       "first recorded pts, or about stretches the collector did not write down. Any pts advance not "
                       "covered by a recorded segment or difference is shown as a break. Times are when the collector "
                       "accepted the updates; pts bounds are those of whole recorded segments.")
COMPLETENESS_CHANNELS = ("Channels and supergroups: a getChannelDifference that is not final covers the pts it returned "
                         "and the next request continues from there; updateChannelTooLong starts such a recovery and is "
                         "not a break by itself; a too-long channel difference is a break; leaving a channel or losing "
                         "access to it ends its chain, and a later rejoin starts a new one.")
COMPLETENESS_REASONS = {
    "difference_too_long": "Telegram answered that the difference was too long to deliver",
    "state_dropped:banned": "the account lost access to the channel",
    "state_dropped:no_access_hash": "the channel's access hash was missing, so its position was dropped",
    "unclaimed:observation_paused": "updates arrived while observation was paused and were not recorded",
    "unclaimed:startup_buffer_full": "updates arrived while the startup buffer was full",
    "collector_restarted": "the collector restarted between the two stretches",
    "unaccounted": "pts advanced without a recorded segment or difference",
}


def completeness_int(value):
    return value if type(value) is int else None


def completeness_time(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else None


def completeness_key(scope, chat_id):
    if scope == "account":
        return "account"
    if scope == "channel" and completeness_int(chat_id) is not None and chat_id < COMPLETENESS_CHANNEL_BASE:
        return chat_id
    return None


def completeness_segment(item, record, run):
    if not isinstance(item, dict):
        return None
    start, end, count = (completeness_int(item.get(name)) for name in ("from", "to", "updates"))
    first, last = completeness_time(item.get("first_at")), completeness_time(item.get("last_at"))
    if (start is None or end is None or count is None or end < start or count < 0 or first is None or last is None
            or last < first or item.get("method") not in COMPLETENESS_METHODS):
        return None
    return {"from": start, "to": end, "updates": count, "first_at": first, "last_at": last, "method": item["method"],
            "record": record, "run": run, "differences": completeness_int(item.get("differences_total")) or 0,
            "empty": completeness_int(item.get("empty_differences")) or 0}


def completeness_collect(events):
    found = {}

    def entry(key):
        return found.setdefault(key, {"segments": [], "gaps": [], "drops": [], "unclaimed": [], "events": {},
                                      "invalid": 0})
    closures = {}
    for event in events:
        kind, payload, record = event.get("kind"), event.get("payload"), event.get("seq")
        if kind not in COMPLETENESS_KINDS or not isinstance(payload, dict):
            continue
        if kind == "coverage.sequence":
            for item in payload.get("sequences") if isinstance(payload.get("sequences"), list) else []:
                key = completeness_key(item.get("scope"), item.get("chat_id")) if isinstance(item, dict) else None
                if key is None:
                    continue
                target = entry(key)
                for segment in item.get("segments") if isinstance(item.get("segments"), list) else []:
                    parsed = completeness_segment(segment, record, payload.get("run_id"))
                    if parsed is None:
                        target["invalid"] += 1
                    else:
                        target["segments"].append(parsed)
                for note in item.get("events") if isinstance(item.get("events"), list) else []:
                    name = note.get("event") if isinstance(note, dict) else None
                    if not isinstance(name, str):
                        continue
                    target["events"][name] = target["events"].get(name, 0) + 1
                    if name == "state_dropped":
                        target["drops"].append({"reason": str(note.get("reason")), "pts": completeness_int(note.get("pts")),
                                                "at": completeness_time(note.get("at")), "record": record})
                for lost in item.get("unclaimed") if isinstance(item.get("unclaimed"), list) else []:
                    low, high = (completeness_int(lost.get(n)) if isinstance(lost, dict) else None for n in ("from", "to"))
                    if low is not None and high is not None and high >= low:
                        target["unclaimed"].append({"from": low, "to": high, "reason": str(lost.get("reason")),
                                                    "record": record})
        elif kind == "coverage.gap":
            key = completeness_key(payload.get("scope"), event.get("chat_id"))
            low, high = completeness_int(payload.get("pts_before")), completeness_int(payload.get("pts_after"))
            if key is not None and low is not None and high is not None and high > low:
                entry(key)["gaps"].append({"from": low, "to": high, "record": record,
                                           "at": completeness_time(event.get("observed_at"))})
        elif completeness_int(payload.get("gap_record")) is not None:
            key = completeness_key(payload.get("scope"), event.get("chat_id"))
            closures[(payload["gap_record"], key)] = {"record": record, "at": payload.get("at"),
                                                      "whole_from_pts": completeness_int(payload.get("whole_from_pts"))}
    return found, closures


def completeness_stretches(segments):
    stretches = []
    for segment in sorted(segments, key=lambda s: (s["from"], -s["to"], s["record"] or 0)):
        last = stretches[-1] if stretches else None
        if last is None or segment["from"] > last["pts_to"]:
            last = {"pts_from": segment["from"], "pts_to": segment["from"], "updates": 0, "pushed": 0, "recovered": 0,
                    "from_at": segment["first_at"], "to_at": segment["last_at"], "differences": {},
                    "empty_differences": 0, "overlapping": 0, "partly_overlapping": 0, "segments": []}
            stretches.append(last)
        segment["counted"] = segment["to"] > last["pts_to"] or segment["from"] == segment["to"] == last["pts_to"]
        if segment["to"] > segment["from"] and segment["from"] < last["pts_to"]:
            last["overlapping"] += 1
            if segment["to"] > last["pts_to"]:
                last["partly_overlapping"] += 1
        if segment["counted"]:
            last["updates"] += segment["updates"]
            last["pushed" if segment["method"] == "push" else "recovered"] += segment["updates"]
            last["pts_to"] = max(last["pts_to"], segment["to"])
        if segment["method"] != "push" and segment["differences"]:
            last["differences"][segment["method"]] = last["differences"].get(segment["method"], 0) + segment["differences"]
        last["empty_differences"] += segment["empty"]
        last["from_at"], last["to_at"] = min(last["from_at"], segment["first_at"]), max(last["to_at"], segment["last_at"])
        last["segments"].append(segment)
    return stretches


def completeness_reasons(found, low, high, after, before, previous, following, closures):
    reasons, records, closed = [], [], None
    for gap in found["gaps"]:
        if gap["from"] < high and gap["to"] > low:
            reasons.append("difference_too_long")
            records.append(gap["record"])
            closed = closed or closures.get(gap["record"])
    for drop in found["drops"]:
        inside = drop["pts"] is not None and low <= drop["pts"] <= high
        timed = drop["at"] is not None and after is not None and before is not None and after <= drop["at"] <= before
        if inside or timed:
            reasons.append("state_dropped:" + drop["reason"])
            records.append(drop["record"])
            closed = closed or closures.get(drop["record"])
    for lost in found["unclaimed"]:
        if lost["from"] < high and lost["to"] > low:
            reasons.append("unclaimed:" + lost["reason"])
            records.append(lost["record"])
    if previous is not None and following is not None and previous["run"] != following["run"]:
        reasons.append("collector_restarted")
    return list(dict.fromkeys(reasons)) or ["unaccounted"], sorted({r for r in records if r is not None}), closed


def completeness_breaks(found, stretches, closures):
    breaks, used = [], set()
    for previous, following in zip(stretches, stretches[1:]):
        low, high = previous["pts_to"], following["pts_from"]
        last = max(previous["segments"], key=lambda s: s["to"])
        first = min(following["segments"], key=lambda s: s["from"])
        reasons, records, closed = completeness_reasons(found, low, high, previous["to_at"], following["from_at"],
                                                        last, first, closures)
        used.update(g["record"] for g in found["gaps"] if g["from"] < high and g["to"] > low)
        breaks.append({"pts_from": low, "pts_to": high, "after_at": previous["to_at"], "before_at": following["from_at"],
                       "reasons": reasons, "records": records, "closed_by": closed})
    for gap in found["gaps"]:
        if gap["record"] in used:
            continue
        inside = any(s["pts_from"] <= gap["from"] and gap["to"] <= s["pts_to"] for s in stretches)
        if inside:
            continue
        breaks.append({"pts_from": gap["from"], "pts_to": gap["to"], "after_at": gap["at"], "before_at": gap["at"],
                       "reasons": ["difference_too_long"], "records": [gap["record"]],
                       "closed_by": closures.get(gap["record"])})
    return sorted(breaks, key=lambda b: (b["pts_from"], b["pts_to"]))


def completeness_within(start, end, since, until):
    return (since is None or end is None or end >= since) and (until is None or start is None or start <= until)


def completeness_stamp(value):
    return value.isoformat(timespec="milliseconds") if value is not None else None


def completeness_view(key, found, closures, since, until):
    found = found or {"segments": [], "gaps": [], "drops": [], "unclaimed": [], "events": {}, "invalid": 0}
    stretches = completeness_stretches(found["segments"])
    breaks = completeness_breaks(found, stretches, {record: item for (record, owner), item in closures.items()
                                                    if owner == key})
    result = {"scope": "account" if key == "account" else "channel", "chat_id": None if key == "account" else key,
              "channel_id": None if key == "account" else COMPLETENESS_CHANNEL_BASE - key,
              "events": found["events"], "invalid_segments": found["invalid"]}
    first = min(found["segments"], key=lambda s: (s["first_at"], s["from"])) if found["segments"] else None
    result["not_recorded_before"] = completeness_stamp(first["first_at"]) if first else None
    result["first_recorded_pts"] = first["from"] if first else None
    shown = [s for s in stretches if completeness_within(s["from_at"], s["to_at"], since, until)]
    gaps = [b for b in breaks if completeness_within(b["after_at"], b["before_at"], since, until)]
    listed, records, differences = [], set(), {}
    for stretch in shown:
        inside = [s for s in stretch["segments"] if completeness_within(s["first_at"], s["last_at"], since, until)]
        if inside:
            low, high = min(s["from"] for s in inside), max(s["to"] for s in inside)
            counted = [s for s in inside if s["counted"]]
        else:
            low = high = max([s["to"] for s in stretch["segments"] if since is not None and s["last_at"] < since]
                            or [stretch["pts_from"]])
            counted = []
        for segment in inside:
            records.add(segment["record"])
            if segment["method"] != "push" and segment["differences"]:
                differences.setdefault(segment["method"], {"count": 0, "records": set()})
                differences[segment["method"]]["count"] += segment["differences"]
                differences[segment["method"]]["records"].add(segment["record"])
        listed.append({"pts_from": low, "pts_to": high, "pts_advance": high - low,
                       "updates": sum(s["updates"] for s in counted),
                       "pushed": sum(s["updates"] for s in counted if s["method"] == "push"),
                       "recovered": sum(s["updates"] for s in counted if s["method"] != "push"),
                       "from_at": completeness_stamp(stretch["from_at"]), "to_at": completeness_stamp(stretch["to_at"]),
                       "whole_stretch": {"pts_from": stretch["pts_from"], "pts_to": stretch["pts_to"]},
                       "empty_differences": sum(s["empty"] for s in inside),
                       "overlapping_segments": stretch["overlapping"],
                       "partly_overlapping_segments": stretch["partly_overlapping"]})
    records.discard(None)
    if not listed and not gaps:
        status = "not_recorded"
    elif gaps:
        status = "breaks"
    elif len(listed) == 1 and (since is None or shown[0]["from_at"] <= since) and (until is None or shown[0]["to_at"] >= until):
        status = "unbroken"
    else:
        status = "partial"
    ordered = sorted(records)
    result.update({
        "status": status, "stretches": listed,
        "pts_from": listed[0]["pts_from"] if listed else None, "pts_to": listed[-1]["pts_to"] if listed else None,
        "from_at": listed[0]["from_at"] if listed else None, "to_at": listed[-1]["to_at"] if listed else None,
        "updates": sum(s["updates"] for s in listed),
        "breaks": [{**b, "after_at": completeness_stamp(b["after_at"]), "before_at": completeness_stamp(b["before_at"])}
                   for b in gaps],
        "differences": {method: {"count": item["count"], "records": sorted(item["records"])[:COMPLETENESS_LISTED],
                                 "records_total": len(item["records"])} for method, item in differences.items()},
        "records": {"first": ordered[0], "last": ordered[-1], "count": len(ordered)} if ordered else None})
    return result


def completeness_certificate(events, since=None, until=None, chats=None, account=True):
    found, closures = completeness_collect(events)
    start, end = completeness_time(since), completeness_time(until)
    if chats is None:
        keys = [key for key in found if key != "account"]
    else:
        keys = [chat for chat in chats if completeness_key("channel", chat) is not None]
        account = account and any(completeness_key("channel", chat) is None for chat in chats)
    keys = (["account"] if account else []) + sorted(dict.fromkeys(keys), reverse=True)
    return {"format": COMPLETENESS_FORMAT, "since": since, "until": until, "proves": COMPLETENESS_PROVES,
            "does_not_prove": COMPLETENESS_LIMITS, "channels": COMPLETENESS_CHANNELS,
            "sequences": [completeness_view(key, found.get(key), closures, start, end) for key in keys]}


def completeness_when(value):
    return value[:16].replace("T", " ") + " UTC" if isinstance(value, str) else "?"


def completeness_lines(certificate, t, titles=None):
    lines = []
    for item in certificate["sequences"]:
        if item["scope"] == "account":
            name = t("Account sequence (private chats and basic groups)")
        else:
            name = t("Channel {name}", name=(titles or {}).get(item["chat_id"]) or str(item["chat_id"]))
        if item["status"] == "not_recorded":
            lines.append(t("{name}: no update sequence records in this interval; continuity is not claimed.", name=name)
                         + (" " + t("Not recorded before {at}.", at=completeness_when(item["not_recorded_before"]))
                            if item["not_recorded_before"] else ""))
            continue
        text = t("{name}, {start} – {end}: pts {first} → {last}, breaks {breaks}", name=name,
                 start=completeness_when(certificate.get("since") or item["from_at"]),
                 end=completeness_when(certificate.get("until") or item["to_at"]),
                 first=item["pts_from"] if item["pts_from"] is not None else "?",
                 last=item["pts_to"] if item["pts_to"] is not None else "?", breaks=len(item["breaks"]))
        for method, recovered in item["differences"].items():
            text += ", " + t("recovered through {method}: {count} (records {records})", method=method,
                             count=recovered["count"], records=", ".join("#" + str(r) for r in recovered["records"]))
        text += ". " + {"unbroken": t("Unbroken."), "partial": t("Recorded for part of the interval only."),
                        "breaks": t("Not unbroken.")}[item["status"]]
        if item["not_recorded_before"]:
            text += " " + t("Not recorded before {at}.", at=completeness_when(item["not_recorded_before"]))
        lines.append(text)
        for gap in item["breaks"]:
            closed = gap.get("closed_by")
            lines.append("  " + t("Break: pts {low} → {high}, {after} – {before}: {reason}", low=gap["pts_from"],
                                  high=gap["pts_to"], after=completeness_when(gap["after_at"]),
                                  before=completeness_when(gap["before_at"]),
                                  reason="; ".join(t(COMPLETENESS_REASONS.get(r, r)) for r in gap["reasons"]))
                         + (" (" + ", ".join("#" + str(r) for r in gap["records"]) + ")" if gap["records"] else "")
                         + ". " + (t("Whole again from pts {pts} (record #{record}).", pts=closed["whole_from_pts"],
                                     record=closed["record"]) if closed else t("No closing record.")))
    return lines
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
        if type(event["seq"]) is not int or event["seq"] != count or event["previous_hash"] != self.previous:
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
    if event["kind"] not in ("media.saved", "actor.avatar_saved", "secret_chat.file", "webapp.file"):
        return None
    payload = event["payload"]
    digest, size = payload.get("media_sha256"), payload.get("size")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("Invalid media reference in the signed journal")
    if size is not None and (type(size) is not int or size < 0):
        raise ValueError("Invalid media size in the signed journal")
    return digest, size


def verify_checkpoint(checkpoint, public_key, event_count, hash_at, check_drand=False):
    statement = checkpoint.get("statement") if isinstance(checkpoint, dict) else None
    if (not isinstance(statement, dict) or not isinstance(checkpoint.get("signature"), str)
            or any(key not in statement for key in ("format", "public_key", "event_count", "head_hash"))):
        raise ValueError("The --checkpoint file is not a signed TgWitness checkpoint: it needs a statement "
                         "(format, public_key, event_count, head_hash) and a signature")
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
PDF_SIGNATURE_TIMESTAMP = "1.2.840.113549.1.9.16.2.14"
PDF_DATA, PDF_SHA256, PDF_ECDSA_SHA256 = "1.2.840.113549.1.7.1", "2.16.840.1.101.3.4.2.1", "1.2.840.10045.4.3.2"


def read_pdf_seal(data):
    ranges = re.findall(rb"/ByteRange\s*\[\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\]", data)
    if len(ranges) != 1:
        raise ValueError("Not a PDF signed by TgWitness: exactly one signature is expected")
    a, b, c, d = map(int, ranges[0])
    if a != 0 or not 0 < b < c or c + d != len(data) or data[b:b + 1] != b"<" or data[c - 1:c] != b">":
        raise ValueError("The PDF signature does not cover the whole file")
    raw = bytes.fromhex(data[b + 1:c - 1].decode("ascii"))
    content = hashlib.sha256(data[:b] + data[c:]).digest()
    tag, start, end = der(raw, 0)
    if tag != 0x30 or any(raw[end:]):
        raise ValueError("The PDF signature carries data after its CMS structure")
    info = children(raw, start, end)
    if len(info) != 2 or info[0][0] != 0x06 or oid(raw, info[0][2], info[0][3]) != SIGNED_DATA or info[1][0] != 0xA0:
        raise ValueError("The PDF signature is not CMS signed data")
    tag, start, end = der(raw, info[1][2])
    signed = children(raw, start, end) if tag == 0x30 and end == info[1][3] else []
    if [item[0] for item in signed] != [0x02, 0x31, 0x30, 0xA0, 0x31] or raw[signed[0][2]:signed[0][3]] != b"\x01":
        raise ValueError("The PDF signature carries CMS fields TgWitness does not write")
    certificates, signers = children(raw, signed[3][2], signed[3][3]), children(raw, signed[4][2], signed[4][3])
    if len(certificates) != 1 or len(signers) != 1:
        raise ValueError("The PDF signature must carry exactly one certificate and one signer")
    encapsulated = children(raw, signed[2][2], signed[2][3])
    if len(encapsulated) != 1 or encapsulated[0][0] != 0x06 or oid(raw, *encapsulated[0][2:]) != PDF_DATA:
        raise ValueError("The PDF signature is not detached")
    der_certificate = raw[certificates[0][1]:certificates[0][3]]
    certificate = x509.load_der_x509_certificate(der_certificate)
    parts = children(raw, signers[0][2], signers[0][3])
    if [item[0] for item in parts] not in ([0x02, 0x30, 0x30, 0xA0, 0x30, 0x04], [0x02, 0x30, 0x30, 0xA0, 0x30, 0x04, 0xA1]) \
            or raw[parts[0][2]:parts[0][3]] != b"\x01":
        raise ValueError("The PDF signer carries fields TgWitness does not write")
    attributes, signature = parts[3], parts[5]
    unsigned = parts[6] if len(parts) == 7 else None

    def algorithm(item, expected):
        found = children(raw, item[2], item[3]) if item[0] == 0x30 else []
        if not found or found[0][0] != 0x06 or oid(raw, *found[0][2:]) != expected or len(found) > 2 \
                or len(found) == 2 and raw[found[1][1]:found[1][3]] != b"\x05\x00":
            raise ValueError("The PDF signature names an algorithm TgWitness does not use")
    digests = children(raw, signed[1][2], signed[1][3])
    if len(digests) != 1:
        raise ValueError("The PDF signature names an algorithm TgWitness does not use")
    algorithm(digests[0], PDF_SHA256)
    algorithm(parts[2], PDF_SHA256)
    algorithm(parts[4], PDF_ECDSA_SHA256)
    sid = children(raw, parts[1][2], parts[1][3])
    if len(sid) != 2 or raw[sid[0][1]:sid[0][3]] != certificate.issuer.public_bytes() or sid[1][0] != 0x02 \
            or int.from_bytes(raw[sid[1][2]:sid[1][3]], "big", signed=True) != certificate.serial_number:
        raise ValueError("The PDF signer does not name the certificate in the signature")

    def values(item):
        found = {}
        for kind_tag, _, s, e in children(raw, item[2], item[3]):
            kind = children(raw, s, e) if kind_tag == 0x30 else []
            if len(kind) != 2 or kind[0][0] != 0x06 or kind[1][0] != 0x31:
                raise ValueError("Malformed PDF signature attribute")
            name, value = oid(raw, kind[0][2], kind[0][3]), children(raw, kind[1][2], kind[1][3])
            if name in found or len(value) != 1:
                raise ValueError("A PDF signature attribute is repeated or holds more than one value")
            found[name] = value[0]
        return found
    signed_attributes = values(attributes)
    digest = signed_attributes.get(MESSAGE_DIGEST)
    if digest is None or raw[digest[2]:digest[3]] != content:
        raise ValueError("The PDF was changed after it was signed")
    certificate.public_key().verify(raw[signature[2]:signature[3]], b"\x31" + raw[attributes[1] + 1:attributes[3]],
                                    ec.ECDSA(hashes.SHA256()))
    extra = values(unsigned) if unsigned else {}
    seal = extra.get(PDF_SEAL)
    if seal is None or seal[0] != 0x0C:
        raise ValueError("The PDF signature carries no TgWitness seal")
    if set(extra) - {PDF_SEAL, PDF_SIGNATURE_TIMESTAMP}:
        raise ValueError("The PDF signature carries unsigned attributes TgWitness does not write")
    stamped = None
    if PDF_SIGNATURE_TIMESTAMP in extra:
        token = extra[PDF_SIGNATURE_TIMESTAMP]
        reply = ers_reply(raw[token[1]:token[3]])
        try:
            found = tst_info(timestamp_token(reply)["tst"])
            if found["hash"] != hashed(found["algorithm"], raw[signature[2]:signature[3]]):
                raise ValueError("it covers other data than this signature")
            tsa_signature_check(reply, ())
        except (ValueError, TypeError, IndexError, KeyError) as exc:
            raise ValueError("The time stamp on the PDF signature is invalid: " + str(exc)) from None
        stamped = stamp_time(found["time"])
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
                                 "signing_time": raw[when[2]:when[3]].decode("ascii") if when else None,
                                 **({"signature_timestamp": stamped} if stamped else {})}


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
                    yield strict_json(line)

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


IMAGE_FORMAT = "tgwitness-image-attestation-v1"


def manifest_digest(manifest, name):
    files = manifest.get("files")
    if isinstance(files, dict):
        value = files.get(name)
        return value.get("sha256") if isinstance(value, dict) else value
    if isinstance(files, list):
        return next((item.get("sha256") for item in files if isinstance(item, dict) and item.get("name") == name), None)
    return None


def verify_image(images, signature_file, trusted=None, evidence=None):
    attested = read_json_file(signature_file)
    statement = attested.get("statement") if isinstance(attested, dict) else None
    if not isinstance(statement, dict) or statement.get("format") != IMAGE_FORMAT:
        raise ValueError(signature_file.name + " is not a TgWitness image signature")
    public = attested.get("public_key")
    Ed25519PublicKey.from_public_bytes(base64.b64decode(public, validate=True)).verify(
        base64.b64decode(attested.get("signature") or "", validate=True), canonical(statement))
    signer = fingerprint(public)
    if trusted and signer != trusted.strip().lower():
        raise ValueError("The image signer key differs from the trusted fingerprint")
    pages = {page["png_sha256"]: page for page in statement.get("pages") or []}
    checked = []
    for path in images:
        digest = hashlib.sha256()
        with open(path, "rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        page = pages.get(digest.hexdigest())
        if page is None:
            raise ValueError(path.name + " is not a signed page of this statement: the image was changed or belongs to another signature")
        checked.append({"file": path.name, "page": page["page"], "records": len(page["records"])})
    matched = None
    if evidence:
        archive = open_archive(evidence)
        try:
            manifest = read_manifest(archive)
            if manifest.get("fingerprint") != signer and fingerprint(manifest["public_key"]) != signer:
                raise ValueError("The evidence archive was signed by another key")
            expected = manifest_digest(manifest, "events.jsonl")
            if expected and member_digest(archive, "events.jsonl") != expected:
                raise ValueError("events.jsonl differs from the signed archive manifest")
            wanted = {record["seq"]: record["hash"] for page in pages.values() for record in page["records"]}
            found = {}
            with archive.open("events.jsonl") as stream:
                for line in bounded_lines(stream):
                    if line.strip():
                        record = strict_json(line)
                        if record.get("seq") in wanted:
                            found[record["seq"]] = record.get("hash")
        finally:
            archive.close()
        missing = sum(1 for seq, value in wanted.items() if found.get(seq) != value)
        if missing:
            raise ValueError(str(missing) + " signed records of the image are not in the evidence archive")
        matched = len(wanted)
    return {"verified": True, "format": IMAGE_FORMAT, "fingerprint": signer, "key_pinned": bool(trusted),
            "chat": statement.get("chat"), "created_at": statement.get("created_at"), "style": statement.get("style"),
            "pages_total": len(pages), "checked": checked, "evidence_records_matched": matched,
            "recorded_as": attested.get("recorded_as"), "meaning": statement.get("meaning")}


def image_command(argv):
    import argparse

    parser = argparse.ArgumentParser(prog="verify.py IMAGE.png [IMAGE.png ...] IMAGES.sig.json",
                                     description="Check TgWitness chat images against their signature file.")
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--fingerprint", type=fingerprint_argument, help="Collector key fingerprint retained independently")
    parser.add_argument("--evidence", type=Path, help="Evidence ZIP that must contain every signed record of the images")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    signatures = [path for path in args.files if path.name.lower().endswith(".json")]
    images = [path for path in args.files if not path.name.lower().endswith(".json")]
    if len(signatures) != 1 or not images:
        parser.error("give the PNG pages and one .sig.json file")
    try:
        result = verify_image(images, signatures[0], args.fingerprint, args.evidence)
    except Exception as exc:
        reason = ("the signature does not match the statement" if type(exc).__name__ == "InvalidSignature"
                  else str(exc) or type(exc).__name__)
        print(json.dumps({"verified": False, "error": reason}) if args.json
              else "IMAGE: fail\nVERIFICATION FAILED: " + reason)
        raise SystemExit(1)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0
    chat = result["chat"] or {}
    records = sum(item["records"] for item in result["checked"])
    print("IMAGE: signed rendering of saved records · " + str(len(result["checked"])) + " of "
          + str(result["pages_total"]) + " pages · " + str(records) + " records")
    print("  Chat: " + str(chat.get("title") or "") + " (" + str(chat.get("id")) + ")")
    for item in result["checked"]:
        print("  " + item["file"] + ": page " + str(item["page"]) + ", " + str(item["records"]) + " records")
    print("  Signer key: " + result["fingerprint"] + (" (matches the trusted fingerprint)" if result["key_pinned"]
          else " (not compared with a retained fingerprint · --fingerprint)"))
    print("  Evidence archive: " + (str(result["evidence_records_matched"]) + " records found in the signed archive"
          if result["evidence_records_matched"] is not None else "not checked · --evidence archive.zip"))
    print("  " + result["meaning"])
    return 0
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
ASIC_NAMESPACE = "http://uri.etsi.org/02918/v1.2.1#"
ASIC_DIGEST_NAMESPACE = "http://www.w3.org/2000/09/xmldsig#"
ASIC_SHA256 = "http://www.w3.org/2001/04/xmlenc#sha256"
ASIC_MANIFEST, ASIC_SIGNATURE = "META-INF/ASiCManifest.xml", "META-INF/signature.p7s"
ASIC_RECORD_MANIFEST, ASIC_RECORD = "META-INF/ASiCEvidenceRecordManifest.xml", "META-INF/evidencerecord.ers"
ASIC_ADDED_MANIFEST = re.compile(r"META-INF/ASiCManifest([0-9]{3})\.xml")
CHAT_EXPORT_MEMBER = re.compile(r"chat-export-[0-9]{3}\.zip")


def container_members(archive, names, listed):
    if "mimetype" in listed or "mimetype" not in names \
            or archive.getinfo("mimetype").file_size != len(ASIC_MIMETYPE) \
            or read_member(archive, "mimetype") != ASIC_MIMETYPE:
        return []
    return sorted(name for name in names if name not in listed
                  and (name == "mimetype" or name.startswith("META-INF/")))


def asic_references(archive, name, signature):
    """Data objects and their SHA-256 listed by one ASiC manifest whose only SigReference names signature; None when
    the manifest cannot be read that way. A DTD or entity declaration is refused."""
    from urllib.parse import unquote
    from xml.parsers import expat
    references, signatures, digest = [], [], None
    parser = expat.ParserCreate(namespace_separator=" ")

    def refuse(*_):
        raise ValueError("declaration")

    def start(tag, attributes):
        nonlocal digest
        if tag == ASIC_NAMESPACE + " SigReference":
            signatures.append(attributes.get("URI"))
        elif tag == ASIC_NAMESPACE + " DataObjectReference":
            references.append({"uri": attributes.get("URI") or "", "method": None, "value": None})
        elif references and tag == ASIC_DIGEST_NAMESPACE + " DigestMethod" and references[-1]["method"] is None:
            references[-1]["method"] = attributes.get("Algorithm")
        elif references and tag == ASIC_DIGEST_NAMESPACE + " DigestValue" and references[-1]["value"] is None:
            digest = []

    def text(data):
        if digest is not None:
            digest.append(data)

    def end(tag):
        nonlocal digest
        if digest is not None and tag == ASIC_DIGEST_NAMESPACE + " DigestValue":
            references[-1]["value"], digest = "".join(digest).strip(), None
    parser.StartDoctypeDeclHandler = parser.EntityDeclHandler = refuse
    parser.StartElementHandler, parser.CharacterDataHandler, parser.EndElementHandler = start, text, end
    try:
        parser.Parse(read_member(archive, name, MAX_MANIFEST_BYTES), True)
    except (expat.ExpatError, ValueError):
        return None
    if not references or signatures != [signature]:
        return None
    listed = {}
    for item in references:
        try:
            uri = unquote(item["uri"], errors="strict")
        except UnicodeDecodeError:
            return None
        if not uri or uri == "mimetype" or uri.startswith("META-INF/") or uri in listed \
                or item["method"] != ASIC_SHA256 or not item["value"]:
            return None
        try:
            listed[uri] = base64.b64decode(item["value"], validate=True).hex()
        except ValueError:
            listed[uri] = ""
    return listed


def verify_container(archive, names, container, digests):
    """The ASiC-E layer as the report's Check tab reads it: META-INF/ASiCManifest.xml must list every data object with
    its SHA-256, an added ASiCManifestNNN.xml or ASiCEvidenceRecordManifest.xml must match the files it lists, and no
    other entry may sit under META-INF/. The CAdES signatures themselves are not checked here."""
    objects = [name for name in names if name != "mimetype" and not name.startswith("META-INF/")]
    present = set(objects)

    def actual(name):
        if name in digests:
            return digests[name]
        if name in present:
            return hashlib.sha256(read_member(archive, name, MAX_MANIFEST_BYTES)).hexdigest()
        return None
    if ASIC_MANIFEST not in container or ASIC_SIGNATURE not in container:
        raise ValueError("ASiC-E container damaged: " + ASIC_MANIFEST + " or " + ASIC_SIGNATURE + " is missing")
    main = asic_references(archive, ASIC_MANIFEST, ASIC_SIGNATURE)
    if main is None:
        raise ValueError("ASiC-E container damaged: " + ASIC_MANIFEST + " cannot be read")
    problems, covered, checked = [], {"mimetype", ASIC_MANIFEST, ASIC_SIGNATURE}, [ASIC_MANIFEST]
    changed = [name for name, value in main.items() if actual(name) != value]
    unlisted = [name for name in objects if name not in main]
    if changed:
        problems.append("SHA-256 differs from " + ASIC_MANIFEST + ": " + ", ".join(changed[:30]))
    if unlisted:
        problems.append("not listed in " + ASIC_MANIFEST + ": " + ", ".join(unlisted[:30]))
    for name in container:
        added = ASIC_ADDED_MANIFEST.fullmatch(name)
        if not added and name != ASIC_RECORD_MANIFEST:
            continue
        target = ASIC_RECORD if not added else "META-INF/signature" + added[1] + ".p7s"
        other = asic_references(archive, name, target) if target in container else None
        if other is None or any(item not in present or actual(item) != value for item, value in other.items()):
            problems.append(name + " does not match the files it lists")
            continue
        covered.update((name, target))
        checked.append(name)
    outside = [name for name in container if name not in covered]
    if outside:
        problems.append("not covered by any container manifest: " + ", ".join(outside[:30]))
    if problems:
        raise ValueError("ASiC-E container damaged: " + " · ".join(problems))
    return {"manifest_files": len(main), "manifests_checked": checked}


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
            sequence_events = []
            hash_files, account_exports, starts, chat_exports = set(), [], [], []

            def take(event):
                if event["kind"] == "process.started":
                    starts.append(event)
                if event["kind"] == "sealed.chat_export" and event["payload"].get("file") is not None:
                    item = event["payload"]
                    name = item["file"]
                    if (not isinstance(name, str) or not CHAT_EXPORT_MEMBER.fullmatch(name)
                            or any(bound["file"] == name for bound in chat_exports)
                            or type(item.get("chat_id")) is not int or type(item.get("complete")) is not bool
                            or manifest["files"].get(name) != item.get("sha256")
                            or archive.getinfo(name).file_size != item.get("bytes")):
                        raise ValueError("Sealed chat export differs from its journal binding")
                    chat_exports.append(item)
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
                if event["kind"] in COMPLETENESS_KINDS:
                    sequence_events.append(event)
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
            if {name for name in manifest["files"] if CHAT_EXPORT_MEMBER.fullmatch(name)} != {c["file"] for c in chat_exports}:
                raise ValueError("Unbound sealed chat export")
            checked_chats = []
            for binding in chat_exports:
                with archive.open(binding["file"]) as incoming:
                    partial = incoming.read(30 + len(LIVE_START))
                    incoming.seek(0)
                    if partial[:4] == b"PK\x03\x04" and partial[30:] == LIVE_START.encode("ascii"):
                        if binding["complete"]:
                            raise ValueError("A partial chat snapshot is bound as a complete chat export")
                        chat = verify_live_export(incoming, fp, max_gib=max_gib)
                        chat_id = (chat.get("chat") or {}).get("id")
                    else:
                        chat = verify_chat_export(incoming, fp, max_gib=max_gib)
                        chat_id = (chat.get("chat") or {}).get("id")
                if chat_id != binding["chat_id"]:
                    raise ValueError("A sealed chat export contains a different chat than its journal binding")
                checked_chats.append({"chat_id": binding["chat_id"], "file": binding["file"], "complete": binding["complete"],
                                      "format": chat.get("format"), "message_count": chat.get("message_count")})
            result["chat_exports"] = checked_chats
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
        result["sequence_continuity"] = completeness_certificate(sequence_events)
        if check_drand and outside.rounds:
            result["outside"]["drand"]["checked"] = confirm_drand(outside.rounds)
        result["producer"] = manifest.get("producer")
        if container:
            result["container"] = {"format": "ASiC-E", "unchecked_members": container,
                                   **verify_container(archive, names, container, manifest["files"])}
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
        records = verify_evidence_records(archive, names, container, tsa_ca)
        if records:
            result["evidence_records"] = records
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
                 "message.missing_on_recheck", "message.deletion_attributed")


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
    return {"chat_id": chat, "from": low, "to": high, "messages": len(numbers), "absent": high - low + 1 - len(numbers),
            "message_ids": numbers[:1000],
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
                if record["kind"] in ("media.saved", "actor.avatar_saved", "secret_chat.file", "webapp.file"):
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


def gap_scope(options, inventory, done=None):
    reasons = set()
    kinds = options.get("chat_kinds")
    if isinstance(kinds, list) and not set(SHARED_KINDS) <= set(kinds):
        reasons.add("chat_kinds")
    categories = options.get("chat_categories")
    if isinstance(categories, list) and not {"personal", "bots", "private_groups"} <= set(categories):
        reasons.add("chat_kinds")
    if options.get("own_only_categories"):
        reasons.add("own_messages_only")
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
    if done is not None:
        tasks = [task for task in inventory.get("tasks", ()) if isinstance(task, dict) and task.get("category") == "messages"]
        for chat in chats:
            if isinstance(chat, dict) and chat.get("kind") in SHARED_KINDS and chat.get("selected") is True:
                pages = [task for task in tasks if task.get("chat_id") == chat.get("id")]
                if not pages or any(task.get("id") not in done for task in pages):
                    reasons.add("shared_history_incomplete")
        if any(task.get("own_only") is True and not (isinstance(task.get("chat_id"), int) and task["chat_id"] <= CHANNEL_BASE)
               for task in tasks):
            reasons.add("own_messages_only")
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

    def result(self, legacy=False):
        self.borderline = set()
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
        proven, claims = self.proven(ids, legacy)
        conflicts["count"] += claims["count"]
        conflicts["examples"] = (conflicts["examples"] + claims["examples"])[:GAP_EXAMPLES]
        gaps, by_chat, outside = self.attribute(ids, times, owners, proven, legacy)
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

    def proven(self, ids, legacy=False):
        refs, found, claims = self.references, {}, {"count": 0, "examples": []}
        disputed = set()
        entries = sorted(tuple(refs[i:i + 5]) for i in range(0, len(refs), 5))
        for target, owner, source_chat, source_id, relation in entries:
            position = bisect.bisect_left(ids, target)
            if position < len(ids) and ids[position] == target or ids and target > ids[-1]:
                continue
            if target in found:
                if found[target][1] != owner:
                    disputed.add(target)
                    claims["count"] += 1
                    if len(claims["examples"]) < GAP_EXAMPLES:
                        claims["examples"].append([target, found[target][1], owner])
                continue
            found[target] = (target, owner, source_chat, source_id, relation)
        if not legacy:
            for target in disputed:
                del found[target]
        return found, claims

    def attribute(self, ids, times, owners, proven, legacy=False):
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
            if not legacy and unproven == 0 and len({item[1] for item in inside}) > 1:
                top = None
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
    borderline = borderline and computed.get("confidence") != "proven"
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


def export_category(kind, username):
    if kind == "private":
        return "personal"
    if kind == "bot":
        return "bots"
    if kind in ("group", "supergroup"):
        return "public_groups" if username else "private_groups"
    return "public_channels" if username else "private_channels"


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
                categories = self.options.get("chat_categories")
                if categories is not None and export_category(chat.get("kind"), chat.get("username")) not in categories:
                    raise ValueError("Account export selected a chat category outside its frozen options")
                if self.options.get("include_archived") is False and chat.get("archived"):
                    raise ValueError("Account export selected an excluded archived chat")
            self.chats[cid] = chat
        metadata_categories = {"profile", "contacts", "sessions", "profile_photos", "stories", "other_data", "avatars"}
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
                chat = self.chats[task["chat_id"]]
                if (export_category(chat.get("kind"), chat.get("username")) in (self.options.get("own_only_categories") or ())
                        and task["own_only"] is not True):
                    raise ValueError("Account export read all messages in a category limited to own messages")
            elif category not in metadata_categories or task.get("chat_id") is not None:
                raise ValueError("Invalid account export task category")
            self.tasks[task_id] = {"statement": task, "cursor": task["cursor_start"], "terminal": False, "ok": True}

        self.inventory_omissions = ["Selected chat has no history task: " + str(cid) for cid, chat in self.chats.items()
                               if chat["selected"] and not any(t["statement"].get("chat_id") == cid for t in self.tasks.values())]
        category_options = {"profile": "include_profile", "contacts": "include_contacts",
                            "sessions": "include_session_metadata", "profile_photos": "include_profile_photos",
                            "stories": "include_stories", "other_data": "include_other_data", "avatars": "include_avatars"}
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
            declared = strict_json(read_member(self.archive, "message-gaps.json", MAX_JSON_BYTES))
            self.gaps.scope = gap_scope(self.options, self.inventory,
                                        {name for name, state in self.tasks.items() if state["terminal"] and state["ok"]})
            computed = self.gaps.result()
            if not gaps_match(declared, computed, self.gaps.borderline):
                self.gaps.scope = gap_scope(self.options, self.inventory)
                computed = self.gaps.result(legacy=True)
                if not gaps_match(declared, computed, self.gaps.borderline):
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
                event = strict_json(line)
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
    held = []
    with open_archive(bundle_path) as archive:
        manifest = read_manifest(archive)
        for name in archive.namelist():
            if name.startswith("anchors/") and name.endswith(".json"):
                try:
                    statement = json.loads(read_member(archive, name, MAX_JSON_BYTES)).get("statement")
                except (ValueError, AttributeError):
                    continue
                if (isinstance(statement, dict) and statement.get("event_count") == count
                        and isinstance(statement.get("created_at"), str)):
                    held.append(statement["created_at"])
    boundary = manifest.get("boundary") if isinstance(manifest.get("boundary"), dict) else {}
    if boundary.get("event_count") == count and isinstance(boundary.get("chosen_at"), str):
        created = boundary["chosen_at"]
    elif held:
        created = min(held, key=witness_moment)
    else:
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
    times += [e["proven_from"] for e in (result.get("evidence_records") or {}).get("records", [])
              if str(e.get("signature", "")).startswith("checked against")
              and (e.get("subject") == "export" or e.get("event_count") == result.get("events"))]
    times += [witness[name] for name in ("head_bitcoin_block_time", "head_telegram_post_time") if witness.get(name)]
    runtime = result.get("runtime_attestation") or {}
    if runtime.get("verified") is True and runtime.get("key_origin") == "created" and runtime.get("attested_at"):
        times.append(runtime["attested_at"])
    independent = bool(witness.get("witness_key_pinned") and witness.get("export_head_witnessed")
                       and witness.get("witness_fingerprint") != result.get("fingerprint"))
    days = witness.get("days", result.get("days", []))
    missing = witness.get("missing_days", result.get("missing_days", []))
    bad_witness = bool(witness.get("conflicts") or witness.get("anomalies") or any(d["status"] == "fail" for d in days))
    complete_days = bool(days and not missing and all(d["bitcoin"] == "confirmed" for d in days)
                         and witness.get("head_bitcoin_block_time"))
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
        lines.append("GitHub's signed build provenance (Sigstore, issued to the run's GitHub OIDC identity) binds this archive "
                     "to a run of the approved workflow " + str((result.get("runtime_attestation") or {}).get("workflow"))
                     + " on a GitHub-hosted runner, where the approved code creates the collector key and a new Telegram "
                     "session: changing the archive needs a new attestation from a run of that workflow, or a break of "
                     "GitHub Actions or Sigstore. The runner's hardware isolation is not attested.")
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
    failed = next((q for q in tdx["quotes"] if q["status"] not in ("pass", "partial")), None)
    if failed:
        return "missing", "Intel TDX check failed: {detail}", {"detail": (
            "record " + str(failed["record"]) + ": " if "record" in failed else "") + failed["detail"]
            + (" (" + failed["error"] + ")" if failed.get("error") else "")}
    unchecked = sum(q["status"] == "partial" for q in tdx["quotes"])
    if unchecked:
        return ("partial", "{count} Intel TDX quote(s) verified offline and bound to the collector key; {missing} without "
                           "Intel's collateral, so their TCB status, Intel's revocation lists, QE Identity and TDX module "
                           "are not checked; the code the VM ran is not checked here",
                {"count": len(tdx["quotes"]), "missing": unchecked})
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
    records = (result.get("evidence_records") or {}).get("records", [])
    proven = [e for e in records if str(e.get("signature", "")).startswith("checked against")]
    covered = [(events if e.get("subject") == "export" else e.get("event_count") or 0, e["proven_from"]) for e in proven]
    times += [at for count, at in covered if count == events]
    if witness.get("export_head_witnessed") and not witness.get("conflicts"):
        times += [witness[name] for name in ("head_bitcoin_block_time", "head_telegram_post_time") if witness.get(name)]
    runtime = result.get("runtime_attestation") or {}
    attested = runtime.get("verified") is True and runtime.get("key_origin") == "created"
    if attested and runtime.get("attested_at"):
        times.append(runtime["attested_at"])
    unchecked = [a for a in anchors if a not in checked] + [e for e in records if e not in proven]
    stamped = max([a.get("event_count") or 0 for a in checked] + [count for count, _ in covered], default=0)
    qualified = next((a for a in checked if a.get("event_count") == events and a.get("qualified") and a.get("time")), None)
    if qualified:
        status, text, values = ("met", "last exported record existed by {time}; qualified eIDAS time stamp from {service}",
                                {"time": qualified["time"], "service": qualified["qualified"]["service"]})
    elif times:
        status, text, values = "met", "last exported record existed by {time}", {"time": min(times)}
    elif checked or covered:
        status, text, values = "partial", "records 1–{through} existed by {time}", {
            "through": stamped, "time": min([a.get("time") or "?" for a in checked if (a.get("event_count") or 0) == stamped]
                                            + [at for count, at in covered if count == stamped])}
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
                statement = strict_json(raw)
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
                event = strict_json(line)
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
# Catalogue SHA-256: 0206ff557642169aa8cb1c96af97f28c692ab179c70371a9b8a4a95b21a6e451
VERIFIER_LANGUAGE_DATA = (
    "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"
    "v0xKqBeQaKi4ZY5qkl2uASml6N1ZlBjSfELK6XSEtbIpbJjlqCtQrbK4tX4umbIb349ijVLNlpE2brsUduMx/Ic8z70VEdx8RLVzuBuXMgxdXWA7"
    "pXh593S/AGpot+S9SGjalvto7CK2wRUfjr4TOB3iafqsJZQJpJY4GCy3NgfEzK+VczqlMSwqFcOsqRgEw9eTjn/PV8rMIeL+nO9z4ryopFFxUNTX"
    "lIeWBzZvPDGtmjf+vHz/5+Wtn5fP/7y8YX/o0cHx5+Wv8bnv8Z1VA/9e+fPPy3/Df9+y/7748/I8/mrz5+W1n1c+/3l5Hf95K27uiH/++OflR/jn"
    "2zjAusH3Xthv9G7waMe0j5rsOEamsO4m+vPKORx5C6dzAT8DT9Da6elH+IL99lKiIaSbF75jf3j888pZ2oGHdkB8m3bx4av0iXSj+A3Af6/j8nDO"
    "8A8YVyZ9gfabdv5r+hWuHFYBe/AY//gMVr/8ov8ekjA+H+l9XKbd26V4uEH7i0/laOdlPt+5I7mPe27/tlI4Jdd9Mv885uXQzuq+lEh3F/Cvm3DI"
    "K3bjH/dqUEkUTjM1sqnzsoo7uO3niYTv00/0u+/krc3oa9lmlj8vf0Yng+uHV+woC7KEP+PCt4i6sx0u1c7TDiw5+kZihsv0V5nLRrbfJX5pVeh8"
    "hb+6/I2ipOBWfJPog+nILzg3uhfxdc50yMSJLfH1gC9s6o/SH+7jbJbtRNONM/Fv9I2HdgqGaEV+dV+ofVX10kRSxE2Hob+PDinpEcAHHN+iL/yV"
    "DoyWl8shAr1N9lr+jESa6sKJ49ASviEek75AUVNOYTb36SDlTFYupHt0AvWt/IW2naj7r47lyYXczGlwDB+go182mnjivp3yjTV8gs8x2fsdhjuv"
    "tu6F0MIS/pLZSvYWBqcXeRKyzxthBRdoKslenz8vf6KOm7b7M9mRW5pI6W8PC/uAyqks8fVSq6ElX5PRHmcMXSSrs3S/0rfqFTqF5tFqCVmuX/jD"
    "gLkV7mQvyUJi/waRYmGXUdzpNZnit476V0kWmN24BedwcHsgnxfpEL0bkRYLdtPz3jteSRf7W1IWvsdfb/jV5rUxVZS07FSkHPm34y6nyDHWRIas"
    "0xGey520P8yQQnO4Wn9dUfMG6F8TUZhk8Gs43WuOsZ2jS/zqnVT5d6I10VHTPc9fvVG64Z9Jh0HW+QIfYkWLXlpy0jE6y/+VNqy/aMK3RKp8r6jb"
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
        message = failure_detail(exc)
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

    def timestamps(self, anchors, records=None):
        self.heading("Timestamps")
        self.explain("Timestamps")
        if records:
            for state, label, detail, notes in ers_lines(records, self.t):
                self.check(state, label, detail)
                for text in notes:
                    self.say("    " + self.paint(text, "dim"))
        if not anchors and records:
            return
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
                unmatched = sum(item.get("signature", "").startswith("no matching root") for item in items)
                if unmatched == len(items):
                    note(self.t("signature not checked: no matching root in --tsa-ca"))
                elif checked in (0, len(items)):
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
            if quote["status"] not in ("pass", "partial"):
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
                if result["container"].get("manifest_files") is not None:
                    self.check("ok", "ASiC-E manifest", self.t("{n} files · SHA-256 match",
                                                               n=self.number(result["container"]["manifest_files"])))
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
            self.timestamps(result.get("anchors") or [], result.get("evidence_records"))
            self.coverage(result["coverage"])
            self.outside(result["outside"])
            if result.get("sequence_continuity"):
                self.heading("Sequence continuity")
                for line in completeness_lines(result["sequence_continuity"], self.t):
                    self.say("    " + line)
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
                 "require", "require_tier", "sealed_attestation", "sealed_policy", "sealed_repo"):
        value = getattr(args, name)
        for item in value if isinstance(value, list) else [value] if value else ():
            command += ["--" + name.replace("_", "-"), str(item)]
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
    parser.add_argument("--fingerprint", type=fingerprint_argument, help="Public key fingerprint retained independently")
    parser.add_argument("--checkpoint", type=Path, help="Previously retained signed checkpoint JSON")
    parser.add_argument("--tsa-ca", type=Path, action="append",
                        help="Root certificate(s) of a timestamp authority (PEM); repeat for several authorities. "
                             "Tokens from an authority without a root here are reported as not checked")
    parser.add_argument("--witness", type=Path, help="Witness journal export to cross-check an evidence ZIP against")
    parser.add_argument("--witness-fingerprint", type=fingerprint_argument, help="Witness key fingerprint retained independently")
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
    parser.add_argument("--compare-fingerprint", type=fingerprint_argument, help="Trusted fingerprint of the second archive's signer")
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


def archive_kind(path):
    try:
        with zipfile.ZipFile(path) as archive:
            manifest = json.loads(archive.read("manifest.json"))
    except (OSError, KeyError, ValueError, zipfile.BadZipFile):
        return None
    value = str(manifest.get("format", "")) if isinstance(manifest, dict) else ""
    if is_format(value, "chat-export-v1"):
        return "chat"
    if value == "tgwitness-account-export-v1" or value in DISCLOSURE_FORMATS:
        return "account"
    for kind in ("evidence", "witness"):
        if is_format(value, kind + "-v1"):
            return kind
    return None


def verification_comparison(args, parser, mode):
    unsupported = ["--" + name.replace("_", "-") for name in
                   ("checkpoint", "tsa_ca", "witness", "witness_fingerprint", "require_witness", "channel",
                    "evidence", "check_drand", "check_bitcoin", "bitcoin_source", "require", "require_tier", "sealed_attestation",
                    "board")
                   if getattr(args, name)]
    if unsupported:
        parser.error(", ".join(unsupported) + " cannot be used with --compare; verify the evidence archive separately")
    try:
        for path in (args.bundle, args.compare):
            kind = archive_kind(path)
            if kind and kind != "chat":
                raise ValueError("--compare compares two chat exports; " + str(path) + " is not one (" + kind + " archive)"
                                 + ". Verify each archive on its own")
        compared = compare_chat_exports(args.bundle, args.compare, args.fingerprint, args.compare_fingerprint, args.max_gib)
    except Exception as exc:
        code = 3 if args.strict and isinstance(exc, VerifierTooOld) else 1
        if mode == "json":
            verification_print(json.dumps({"verified": False, "error": type(exc).__name__ + ": " + failure_detail(exc)}, indent=2))
            raise SystemExit(code)
        verification_print("ASSURANCE: fail")
        parser.exit(code, "VERIFICATION FAILED: " + plain_failure(exc) + "\n")
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
        if "statement" not in data:
            if {"document", "signed"} <= set(data):
                raise ValueError("This is a case documentation file, not an evidence archive. Check it with: "
                                 "python -m tgwitness.documentation_verify FILE --fingerprint FINGERPRINT")
            raise ValueError("Unrecognised JSON file: it is not a TgWitness signed report, proof, dossier, "
                             "selection or board document.")
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
                         + str(result["range"]["messages"]) + " message(s) in this extract, each checked."
                         + (" " + str(result["range"]["absent"]) + " of the " + str(result["range"]["to"] - result["range"]["from"] + 1)
                            + " numbers in the range have no record in this extract: left out by its rules, deleted or never used."
                            if result["range"]["absent"] else ""))
    elif is_format(archive_format, "witness-v1"):
        shown = "witness"
        result = verify_witness(args.bundle, args.witness_fingerprint or args.fingerprint, args.check_drand, args.check_bitcoin)
        if args.channel:
            result["channel_check"] = check_channel(result, args.channel)
        result.pop("statements")
        flagged = {}
        for anchor in result["anchors"]:
            if anchor["status"] != "ok":
                flagged.setdefault(anchor["status"], []).append(anchor)
        for status, items in sorted(flagged.items()):
            notes.append("The witness recorded " + str(len(items)) + " check(s) with status " + status.replace("_", " ")
                         + ", the first at " + str(items[0].get("at")) + " (record " + str(items[0].get("event_count")) + ").")
        if result.get("no_response"):
            notes.append("The witness recorded " + str(len(result["no_response"])) + " check(s) the collector did not answer.")
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
        verification_print(json.dumps({"verified": False, "error": type(exc).__name__ + ": " + failure_detail(exc)}, indent=2))
        raise SystemExit(code)
    verification_print("ASSURANCE: fail")
    parser.exit(code, "VERIFICATION FAILED: " + plain_failure(exc) + "\n")


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
    verification_print(assurance_line(result))
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
        if result["container"].get("manifest_files") is not None:
            others = result["container"]["manifests_checked"][1:]
            verification_print("ASiC-E container: META-INF/ASiCManifest.xml lists "
                               + str(result["container"]["manifest_files"]) + " files and their SHA-256 match"
                               + ("; also matching the files they list: " + ", ".join(others) if others else "") + ".")
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
    if argv and argv[0].lower().endswith(".png"):
        return image_command(argv)
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
