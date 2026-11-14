# TgWitness verifier sources SHA-256: 815af69e17a282e4921cd3b49f9414b16fa0e36e31d6607f127abb95ad5435ca
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
        if hashed(algorithm, data) == named:
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
        if hashed(algorithm, data) == named:
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
                entry.update(kind="rfc3161", **timestamp_reply_summary(reply, digest, query, data))
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
            if hashed(algorithm, data) == named:
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
    previous, stamps, other = [], [], 0
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
                timestamp_signature(stamp["reply"], roots)
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
    if roots is not None:
        protection.update(qualified_timestamp(newest["reply"]))
    chains = record["chains"]
    return {"record": record, "chains": len(chains), "stamps": len(stamps),
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
            "signature": "checked against the given root" if roots is not None else "not checked (use --tsa-ca)"}


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
            "signature": "checked against the given root" if roots is not None else "not checked (use --tsa-ca)"}


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
        sequence_events = []
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
                if event["kind"] in COMPLETENESS_KINDS:
                    sequence_events.append(event)
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
    times += [e["proven_from"] for e in (result.get("evidence_records") or {}).get("records", [])
              if str(e.get("signature", "")).startswith("checked against")
              and (e.get("subject") == "export" or e.get("event_count") == result.get("events"))]
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
    qualified = next((a["qualified"] for a in checked if a.get("event_count") == events and a.get("qualified")), None)
    if times and qualified:
        status, text, values = ("met", "last exported record existed by {time}; qualified eIDAS time stamp from {service}",
                                {"time": min(times), "service": qualified["service"]})
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
# Catalogue SHA-256: b1ef03110810d075e7d6a793246895701ae854be1a99711e0571885bf75b0c12
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
