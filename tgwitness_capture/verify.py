import hashlib
import io
import re
import struct
import zipfile

from .format import FORMAT, HEX, ZERO, check_checkpoint, check_events, check_seal, decode, fingerprint

MAX_TOTAL = 8 * 1024 ** 3
MAX_FILE = 512 * 1024 ** 2
MAX_ENTRIES = 100000
MAX_MANIFEST = 16 * 1024 ** 2
CHUNK = 1024 * 1024


class Member(io.RawIOBase):
    def __init__(self, budget, source, name, size):
        super().__init__()
        self.budget, self.source, self.name, self.left = budget, source, name, size

    def readable(self):
        return True

    def readinto(self, buffer):
        if not len(buffer):
            return 0
        data = self.source.read(min(len(buffer), self.left + 1))
        self.left -= len(data)
        self.budget.left -= len(data)
        if self.left < 0:
            raise ValueError("Archive member exceeds verification limit: " + self.name)
        if self.budget.left < 0:
            raise ValueError("Archive exceeds verification limit")
        if not data and self.left:
            raise ValueError("Archive member is shorter than its header: " + self.name)
        buffer[:len(data)] = data
        return len(data)

    def close(self):
        if not self.closed:
            self.source.close()
        super().close()


class Budget:
    def __init__(self, archive, total=MAX_TOTAL):
        self.archive, self.left = archive, total

    def open(self, name, limit=MAX_FILE):
        info = self.archive.getinfo(name)
        if info.file_size > limit:
            raise ValueError("Archive member exceeds verification limit: " + name)
        return io.BufferedReader(Member(self, self.archive.open(info), name, info.file_size), CHUNK)

    def read(self, name, limit=MAX_FILE):
        with self.open(name, limit) as source:
            return b"".join(iter(lambda: source.read(CHUNK), b""))


def check_layout(archive, infos):
    handle = archive.fp
    if archive.comment:
        raise ValueError("Archive carries bytes in its trailing comment")
    handle.seek(-22, 2)
    if handle.read(4) != b"PK\x05\x06":
        raise ValueError("Archive has data after its central directory")
    position = 0
    for item in sorted(infos, key=lambda value: value.header_offset):
        if item.header_offset != position:
            raise ValueError("Archive members overlap or have bytes between them" if position
                             else "Archive has data before its first member")
        handle.seek(position)
        header = handle.read(30)
        if len(header) != 30 or header[:4] != b"PK\x03\x04":
            raise ValueError("Archive member header is damaged")
        name_length, extra_length = struct.unpack("<HH", header[26:30])
        extra, wide = handle.read(name_length + extra_length)[name_length:], False
        while len(extra) >= 4:
            field, length = struct.unpack("<HH", extra[:4])
            wide, extra = wide or field == 1, extra[4 + length:]
        position += 30 + name_length + extra_length + item.compress_size
        if item.flag_bits & 8:
            handle.seek(position)
            position += (4 if handle.read(4) == b"PK\x07\x08" else 0) + (20 if wide else 12)
    if position != archive.start_dir:
        raise ValueError("Archive members overlap or have bytes between them")


def verify_zip(path, expected_fingerprint=None, checkpoint=None, receipt=None,
               witness_fingerprint=None, require_final_anchor=False, expected_settings=None, *, check_drand=False):
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = [item.filename for item in infos]
        if len(names) != len(set(names)) or len(names) > MAX_ENTRIES:
            raise ValueError("Duplicate or excessive archive entries")
        if any(item.file_size > MAX_FILE or item.flag_bits & 1 or item.is_dir()
               or item.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)
               or (item.external_attr >> 16) & 0o170000 not in {0, 0o100000} for item in infos):
            raise ValueError("Unsupported archive member")
        if sum(item.file_size for item in infos) > MAX_TOTAL:
            raise ValueError("Archive exceeds verification limit")
        check_layout(archive, infos)
        reads, rereads = Budget(archive), Budget(archive)
        if not {"manifest.json", "manifest.sig", "events.jsonl", "report.html"} <= set(names):
            raise ValueError("Incomplete capture export")
        if archive.getinfo("manifest.json").file_size > MAX_MANIFEST or archive.getinfo("manifest.sig").file_size != 128:
            raise ValueError("Invalid manifest size")
        manifest = decode(reads.read("manifest.json", MAX_MANIFEST))
        if (set(manifest) != {"format", "observer_id", "public_key", "created_at", "seq", "head_hash", "files"}
                or manifest["format"] != FORMAT or not isinstance(manifest["files"], dict)):
            raise ValueError("Unsupported manifest")
        public_key = manifest["public_key"]
        actual_fingerprint = fingerprint(public_key)
        if expected_fingerprint is not None and expected_fingerprint != actual_fingerprint:
            raise ValueError("Untrusted observer key")
        check_seal(public_key, "manifest", manifest, reads.read("manifest.sig", 128).decode("ascii"))
        if set(names) != set(manifest["files"]) | {"manifest.json", "manifest.sig"}:
            raise ValueError("Archive inventory does not match manifest")
        for name, descriptor in manifest["files"].items():
            if name not in {"events.jsonl", "report.html"} and not re.fullmatch(r"objects/[0-9a-f]{64}", name):
                raise ValueError("Unsafe or unknown archive path")
            if (set(descriptor) != {"sha256", "size"} or not HEX.fullmatch(descriptor["sha256"])
                    or type(descriptor["size"]) is not int or descriptor["size"] != archive.getinfo(name).file_size):
                raise ValueError("Invalid file descriptor")
            with reads.open(name) as source:
                if hashlib.file_digest(source, "sha256").hexdigest() != descriptor["sha256"]:
                    raise ValueError("File hash mismatch: " + name)
        events = []
        with rereads.open("events.jsonl") as source:
            while line := source.readline(2 * 1024 ** 2 + 1):
                if len(line) > 2 * 1024 ** 2 or not line.endswith(b"\n"):
                    raise ValueError("Invalid journal line")
                events.append(decode(line))
        head = check_events(events, public_key, manifest["observer_id"])
        if type(manifest["seq"]) is not int or manifest["seq"] != len(events) or manifest["head_hash"] != head:
            raise ValueError("Manifest boundary does not match journal")
        referenced = {"events.jsonl", "report.html"}
        for event in events:
            for artifact in event["artifacts"]:
                name = "objects/" + artifact["sha256"]
                if manifest["files"].get(name) != {"sha256": artifact["sha256"], "size": artifact["size"]}:
                    raise ValueError("Missing or altered event artifact")
                referenced.add(name)
        if referenced != set(manifest["files"]):
            raise ValueError("Unreferenced export files")
        from .trusted_verify import verify_analysis
        report_count = int(verify_analysis(events, rereads.read))
    from .trusted_anchor import confirm
    drand = confirm(events, check_drand)
    anchored_seq = 0
    independently_witnessed = False
    checkpoints = [checkpoint] if checkpoint is not None else []
    if receipt is not None:
        if not witness_fingerprint:
            raise ValueError("A trusted witness fingerprint is required for a receipt")
        receipt_body = receipt["body"]
        if receipt_body.get("format") != FORMAT or receipt_body.get("kind") != "witness.receipt":
            raise ValueError("Invalid witness receipt")
        witness_key = receipt_body["public_key"]
        if fingerprint(witness_key) != witness_fingerprint or witness_key == public_key:
            raise ValueError("Untrusted or shared witness key")
        check_seal(witness_key, "receipt", receipt_body, receipt["signature"])
        checkpoints.append(receipt_body["checkpoint"])
        independently_witnessed = True
    for retained in checkpoints:
        body = check_checkpoint(retained, public_key, manifest["observer_id"])
        if body["seq"] > len(events):
            raise ValueError("Export is shorter than retained checkpoint")
        expected_head = events[body["seq"] - 1]["hash"] if body["seq"] else ZERO
        if expected_head != body["head_hash"]:
            raise ValueError("Export disagrees with retained checkpoint")
        anchored_seq = max(anchored_seq, body["seq"])
    if require_final_anchor and (not checkpoints or anchored_seq != len(events)):
        raise ValueError("Export has an unanchored tail")
    from .official_proof import official_report
    official = official_report(events, expected_settings)
    return {"valid": True, "format": FORMAT, "observer_id": manifest["observer_id"],
            "fingerprint": actual_fingerprint, "key_pinned": expected_fingerprint is not None,
            "events": len(events), "head_hash": head, "checkpoint_checked": bool(checkpoints),
            "independently_witnessed": independently_witnessed, "anchored_seq": anchored_seq,
            "unanchored_events": len(events) - anchored_seq,
            "trusted_reports_checked": report_count, "drand": drand,
            **({"official": official} if official is not None else {})}
