# TgWitness verifier sources SHA-256: f2335662a88c72969f7e05fad9f40a5421871be2978d4ad1523263a2fa202cdc
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
    parser.add_argument("--fingerprint", help="Collector key fingerprint retained independently")
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
            result["container"] = {"format": "ASiC-E", "unchecked_members": container}
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
# Catalogue SHA-256: 503e373ea8e6a5d3d18d08ff641d193c62afdc0064e0da31d0d99c8f1048abe2
VERIFIER_LANGUAGE_DATA = (
    "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"
    "H0+d+t/6i/8j"
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
    parser.add_argument("--fingerprint", help="Public key fingerprint retained independently")
    parser.add_argument("--checkpoint", type=Path, help="Previously retained signed checkpoint JSON")
    parser.add_argument("--tsa-ca", type=Path, action="append",
                        help="Root certificate(s) of a timestamp authority (PEM); repeat for several authorities. "
                             "Tokens from an authority without a root here are reported as not checked")
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
