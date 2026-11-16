# TgWitness verifier sources SHA-256: 6d996f97d8ee08ba76b2f860aad5de63f7963c3d53ba95b9af99ecb0565e2c90
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
                if record["kind"] in ("media.saved", "actor.avatar_saved", "secret_chat.file"):
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
# Catalogue SHA-256: 8bfddf08068abe53ddd7e39b7308539533c8e5141fcbdaeb90d7ac90271c821e
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
