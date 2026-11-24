# TgWitness verifier sources SHA-256: 4509b0a80308ee5ad1c67142c7e7a797e5e624b9bcef6c02ddbec5c09ec132e5
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
    # Claim the name first, so an existing file is refused before any work. Plaintext goes to a private
    # file beside it and replaces the claim only after every record has authenticated: one copy on disk.
    _pw_output(destination).close()
    temporary = None
    try:
        with source.open("rb") as encrypted:
            if _pw_read(encrypted, len(PW_MAGIC)) != PW_MAGIC:
                raise ValueError("Not a TgWitness password-encrypted file")
            salt, prefix = _pw_read(encrypted, 16), _pw_read(encrypted, 8)
            cipher = AESGCM(_pw_key(password, salt))
            name = cipher.decrypt(_pw_nonce(prefix, 0), _pw_record(encrypted, PW_NAME_LIMIT), PW_CONTEXT + b"name")
            try:
                _pw_name(name.decode("utf-8"))
            except UnicodeDecodeError as exc:
                raise ValueError("Invalid encrypted filename") from exc
            handle, temporary = tempfile.mkstemp(dir=destination.parent, prefix=".tgwitness-", suffix=".part")
            with os.fdopen(handle, "wb") as plain:
                counter = 1
                while True:
                    record = _pw_record(encrypted, PW_CHUNK)
                    last = len(record) < PW_CHUNK + 16
                    aad = PW_CONTEXT + name + (b"|last" if last else b"|more")
                    plain.write(cipher.decrypt(_pw_nonce(prefix, counter), record, aad))
                    if last:
                        if encrypted.read(1):
                            raise ValueError("Trailing data after password-encrypted content")
                        break
                    counter += 1
        os.replace(temporary, destination)
        temporary = None
    except BaseException:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)
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
    if len(signature) % 2 or 16 * len(signature) < 4 * size or key is None or not bin_on_curve(curve, key):
        return False
    whole, half = int.from_bytes(signature, order), 4 * len(signature)
    r, s = whole & ((1 << half) - 1), whole >> half
    if not (0 < r < n and 0 < s < n):
        return False
    if bin_combination(curve, n, key, 0, key) is not None:
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
    if offset < 0 or offset + 2 > len(data):
        raise ValueError("Truncated DER")
    tag, length, start = data[offset], data[offset + 1], offset + 2
    if length & 0x80:
        count = length & 0x7F
        if not 1 <= count <= 4:
            raise ValueError("Unsupported DER length")
        if start + count > len(data):
            raise ValueError("Truncated DER")
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


def pss_algorithm(data, item):
    parts = children(data, *item[2:])
    if item[0] != 0x30 or len(parts) not in (1, 2) or parts[0][0] != 0x06:
        raise ValueError("Malformed timestamp AlgorithmIdentifier")
    encoded = data[parts[0][2]:parts[0][3]]
    if not encoded or encoded[-1] & 128 or any(b == 128 and (i == 0 or not encoded[i-1] & 128)
                                               for i, b in enumerate(encoded)):
        raise ValueError("Malformed timestamp algorithm OID")
    return oid(data, *parts[0][2:]), parts[1] if len(parts) == 2 else None


def timestamp_pss_parameters(data, params):
    if params is None or params[0] != 0x30:
        raise ValueError("Missing timestamp RSASSA-PSS parameters")
    sha1 = "1.3.14.3.2.26"
    digest_oid = mask_oid = sha1
    salt, previous = 20, 0x9F
    for tag, _, start, end in children(data, *params[2:]):
        inner = children(data, start, end)
        if not previous < tag <= 0xA3 or len(inner) != 1:
            raise ValueError("Malformed timestamp RSASSA-PSS parameters")
        previous = tag
        if tag in (0xA0, 0xA1):
            alg, param = pss_algorithm(data, inner[0])
            if tag == 0xA1:
                if alg != "1.2.840.113549.1.1.8" or param is None:
                    raise ValueError("Unsupported timestamp RSASSA-PSS mask generation algorithm")
                alg, param = pss_algorithm(data, param)
            if param is not None and data[param[1]:param[3]] != b"\x05\x00":
                raise ValueError("Malformed timestamp RSASSA-PSS hash parameters")
            if tag == 0xA0:
                digest_oid = alg
            else:
                mask_oid = alg
        else:
            value = data[inner[0][2]:inner[0][3]]
            if (inner[0][0] != 0x02 or not value or value[0] & 128
                    or len(value) > 1 and value[0] == 0 and value[1] < 128):
                raise ValueError("Malformed timestamp RSASSA-PSS integer")
            number = int.from_bytes(value, "big")
            if tag == 0xA2:
                salt = number
            elif number != 1:
                raise ValueError("Unsupported timestamp RSASSA-PSS trailer")
    return digest_oid, mask_oid, salt


def verify_timestamp_pss(reply, algorithm, signer, key, signature, signed, content_digest):
    _, params = pss_algorithm(reply, algorithm)
    digest_oid, mask_oid, salt = timestamp_pss_parameters(reply, params)
    if digest_oid != content_digest or digest_oid not in DIGESTS or mask_oid not in DIGESTS:
        raise ValueError("Unsupported or mismatched timestamp RSASSA-PSS hash")
    spki = tbs_key(signer.tbs_certificate_bytes)
    _, start, end = der(spki, 0)
    key_oid, key_params = pss_algorithm(spki, children(spki, start, end)[0])
    if key_oid == "1.2.840.113549.1.1.10" and key_params is not None:
        required_hash, required_mask, minimum_salt = timestamp_pss_parameters(spki, key_params)
        if (digest_oid, mask_oid) != (required_hash, required_mask) or salt < minimum_salt:
            raise ValueError("Timestamp signature violates RSASSA-PSS public key restrictions")
    algorithm_hash = DIGESTS[digest_oid]()
    if salt > padding.calculate_max_pss_salt_length(key, algorithm_hash):
        raise ValueError("Invalid timestamp RSASSA-PSS salt length")
    key.verify(signature, signed, padding.PSS(padding.MGF1(DIGESTS[mask_oid]()), salt), algorithm_hash)


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
            elif isinstance(key, rsa.RSAPublicKey) and method == "1.2.840.113549.1.1.10":
                verify_timestamp_pss(reply, items[4], signer, key, signature, signed, content_digest)
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
# Catalogue SHA-256: bb9327a793285b885ddd2e27c9c00b095215526002c3f099b20effe622a10c8b
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
