# TgWitness verifier sources SHA-256: 6600795d8082a548698533d64fde080135ac179baa93776516b1c102bc9f761a
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
        if signer is not None and stamps[position]["time"] > signer.not_valid_after_utc:
            late.append({"time": stamp_time(stamps[position]["time"]),
                         "previous_expired": stamp_time(signer.not_valid_after_utc)})
            proven = position
    newest, now = stamps[-1], now or datetime.now(timezone.utc)
    expires = newest["signer"].not_valid_after_utc if newest["signer"] is not None else None
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
# Catalogue SHA-256: 022f383950713b7dba3744c32f9d2a059c8c61b35215a78e284a472fdba710a0
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
