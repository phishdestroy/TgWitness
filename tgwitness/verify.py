# TgWitness verifier sources SHA-256: 0d92c1173cd3e91c5fb9488cd3d414abfb6618850047dcf92a20df6a22a0e6b2
"""Standalone verifier"""
import argparse
import base64 as _base64
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
    problems = []
    for kind in found:
        try:
            return revocation_status(kind, read_member(archive, base + "." + kind), revocation_subject(reply, extra))
        except (ValueError, TypeError, IndexError, InvalidSignature, UnsupportedAlgorithm) as exc:
            problems.append(kind.upper() + ": " + str(exc))
    return {"status": "failed", "error": "; ".join(problems), "detail": "revocation check failed: " + "; ".join(problems)}


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
# Catalogue SHA-256: 25e57ac9db2fb893867a1219e446434647fe6606f04400c320c2d323d69d957d
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
        parser.exit(code, "VERIFICATION FAILED: " + type(exc).__name__ + ": " + failure_detail(exc) + "\n")
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
    parser.exit(code, "VERIFICATION FAILED: " + type(exc).__name__ + ": " + failure_detail(exc) + "\n")


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
