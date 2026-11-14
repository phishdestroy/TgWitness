import base64
import hashlib
import os
import re
from datetime import datetime, timedelta, timezone
from typing import Literal
from urllib.parse import quote
from xml.sax.saxutils import escape, quoteattr

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from pydantic import BaseModel, ConfigDict, Field

from .anchor import der
from .security import private_write
from .verifier.timestamps import (DIGESTS, children, der as element, oid, query_nonce, signed_attributes,
                                  signing_certificate_hash, timestamp_signature, timestamp_token, tst_info)

ALGORITHMS = {"sha256": "2.16.840.1.101.3.4.2.1", "sha384": "2.16.840.1.101.3.4.2.2",
              "sha512": "2.16.840.1.101.3.4.2.3"}
NAMES = {value: name for name, value in ALGORITHMS.items()}
STRENGTH = ("sha256", "sha384", "sha512")
OID_BYTES = {"sha256": bytes.fromhex("0609608648016503040201"), "sha384": bytes.fromhex("0609608648016503040202"),
             "sha512": bytes.fromhex("0609608648016503040203")}
SIGNATURE_DIGESTS = {"1.3.14.3.2.26": "sha1", **{key: value.name for key, value in DIGESTS.items()}}
RECORD_FILE = re.compile(r"(checkpoint-\d{12,})(?:\.renewal-(\d{1,6}))?\.ers")
CHECKPOINT_FILE = re.compile(r"checkpoint-\d{12,}\.json")
CONTAINER_RECORD, CONTAINER_MANIFEST = "META-INF/evidencerecord.ers", "META-INF/ASiCEvidenceRecordManifest.xml"
RECORD_MEDIA_TYPE = "application/vnd.etsi.timestamp-token"
RECORD_LIMIT = 16 * 1024 * 1024
DAY = 86400


class RenewalPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")
    months_before_expiry: int = Field(default=6, ge=1, le=60)
    weak_algorithms: list[Literal["sha1", "sha256", "sha384", "sha512"]] = Field(default_factory=list, max_length=4)
    algorithm: Literal["sha256", "sha384", "sha512"] = "sha256"
    stronger_algorithm: Literal["sha384", "sha512"] = "sha512"


def policy(store):
    return RenewalPolicy.model_validate(store.get_setting("evidence_record_policy", {}) or {})


def demand_renewal(store, kind):
    if kind not in ("timestamp", "hashtree"):
        raise ValueError("Unknown renewal kind")
    from .store import utcnow
    store.set_setting("evidence_record_demand", {"kind": kind, "at": utcnow()})


def digest(name, data):
    return hashlib.new(name, data).digest()


def node(name, values):
    return values[0] if len(values) == 1 else digest(name, b"".join(sorted(values)))


def tree(name, leaves):
    level = sorted(set(leaves))
    if not level:
        raise ValueError("No data objects")
    under, paths = {value: [value] for value in level}, {value: [] for value in level}
    while len(level) > 1:
        groups = [level[i:i + 2] for i in range(0, len(level), 2)]
        if len(groups[-1]) == 1:
            single = groups.pop()
            groups[-1] = groups[-1] + single
        joined, level = {}, []
        for group in groups:
            parent = node(name, group)
            for value in group:
                for leaf in under[value]:
                    paths[leaf].append(sorted(group) if not paths[leaf] else sorted(v for v in group if v != value))
                joined.setdefault(parent, []).extend(under[value])
            level.append(parent)
        under = joined
    return level[0], paths


def root_hash(name, values, partials):
    if not partials:
        if len(values) != 1:
            raise ValueError("A data group needs a reduced hash tree")
        return values[0]
    if any(value not in partials[0] for value in values):
        raise ValueError("A data object is not in the first hash list of the reduced hash tree")
    current = node(name, partials[0])
    for siblings in partials[1:]:
        current = node(name, [current, *siblings])
    return current


def chained(name, value, sequence):
    return digest(name, value + digest(name, sequence))


def algorithm_identifier(name):
    return der(0x30, OID_BYTES[name])


def archive_timestamp(partials, token):
    reduced = der(0xA2, b"".join(der(0x30, b"".join(der(0x04, value) for value in partial))
                                 for partial in partials)) if partials else b""
    return der(0x30, reduced + token)


def encode(chains):
    names = sorted({chain["algorithm"] for chain in chains}, key=STRENGTH.index)
    return der(0x30, der(0x02, b"\x01") + der(0x30, b"".join(algorithm_identifier(n) for n in names))
               + der(0x30, b"".join(der(0x30, b"".join(chain["stamps"])) for chain in chains)))


def token_reply(token):
    return der(0x30, der(0x30, der(0x02, b"\x00")) + token)


def token_details(token):
    reply = token_reply(token)
    found = timestamp_token(reply)
    info = tst_info(found["tst"])
    if info["algorithm"] not in NAMES:
        raise ValueError("Unsupported timestamp hash algorithm " + info["algorithm"])
    items = children(reply, found["signer"][2], found["signer"][3])
    if len(items) < 6 or items[3][0] != 0xA0:
        raise ValueError("The timestamp signer has no signed attributes")
    method = oid(reply, *children(reply, items[2][2], items[2][3])[0][2:])
    algorithm, named, _ = signing_certificate_hash(reply, signed_attributes(reply, items[3][2], items[3][3]))
    signer = None
    for data in found["certificates"]:
        hasher = hashes.Hash(algorithm())
        hasher.update(data)
        if hasher.finalize() == named:
            signer = x509.load_der_x509_certificate(data)
    return {"algorithm": NAMES[info["algorithm"]], "hash": info["hash"], "time": info["time"], "signer": signer,
            "signature_digest": SIGNATURE_DIGESTS.get(method, method)}


def parse(data):
    if len(data) > RECORD_LIMIT:
        raise ValueError("Evidence record size limit exceeded")
    tag, start, end = element(data, 0)
    if tag != 0x30 or end != len(data):
        raise ValueError("Not an RFC 4998 evidence record")
    items = children(data, start, end)
    if len(items) < 3 or items[0][0] != 0x02 or data[items[0][2]:items[0][3]] != b"\x01" or items[1][0] != 0x30:
        raise ValueError("Not an RFC 4998 evidence record version 1")
    if any(tag == 0xA1 for tag, *_ in items[2:-1]):
        raise ValueError("Encrypted evidence records are not supported")
    if items[-1][0] != 0x30:
        raise ValueError("Not an RFC 4998 evidence record")
    declared = [NAMES.get(oid(data, *children(data, s, e)[0][2:]), "unsupported")
                for _, _, s, e in children(data, items[1][2], items[1][3])]
    chains = []
    for _, chain_start, value_start, value_end in children(data, items[-1][2], items[-1][3]):
        stamps = []
        for _, stamp_start, stamp_value, stamp_end in children(data, value_start, value_end):
            fields = children(data, stamp_value, stamp_end)
            tags = [t for t, *_ in fields[:-1]]
            if not fields or fields[-1][0] != 0x30 or tags != sorted(set(tags)) or not set(tags) <= {0xA0, 0xA1, 0xA2}:
                raise ValueError("Malformed ArchiveTimeStamp")
            token = data[fields[-1][1]:fields[-1][3]]
            details = token_details(token)
            name, partials = details["algorithm"], []
            for tag, _, s, e in fields[:-1]:
                if tag == 0xA0:
                    name = NAMES.get(oid(data, *children(data, s, e)[0][2:]))
                    if name is None:
                        raise ValueError("Unsupported hash tree algorithm")
                elif tag == 0xA2:
                    for kind, _, ps, pe in children(data, s, e):
                        values = children(data, ps, pe)
                        if kind != 0x30 or not values or any(v[0] != 0x04 for v in values):
                            raise ValueError("Malformed reduced hash tree")
                        partials.append([data[vs:ve] for _, _, vs, ve in values])
            stamps.append({"raw": data[stamp_start:stamp_end], "token": token, "partials": partials,
                           "algorithm": name, **{k: v for k, v in details.items() if k != "algorithm"}})
        if not stamps:
            raise ValueError("Empty ArchiveTimeStampChain")
        chains.append({"raw": data[chain_start:value_end], "algorithm": stamps[0]["algorithm"], "stamps": stamps})
    if not chains:
        raise ValueError("Empty ArchiveTimeStampSequence")
    return {"algorithms": declared, "chains": chains}


def check(data, objects, roots=None):
    record = parse(data)
    previous, times = [], []
    for index, chain in enumerate(record["chains"]):
        name = chain["algorithm"]
        if name not in record["algorithms"]:
            raise ValueError("Chain " + str(index + 1) + " uses a hash algorithm the record does not declare")
        sequence = der(0x30, b"".join(previous))
        for position, stamp in enumerate(chain["stamps"]):
            if stamp["algorithm"] != name:
                raise ValueError("Chain " + str(index + 1) + " mixes hash algorithms")
            if position:
                values = [digest(name, chain["stamps"][position - 1]["token"])]
            elif index:
                values = [chained(name, digest(name, item), sequence) for item in objects]
            else:
                values = [digest(name, item) for item in objects]
            if root_hash(name, values, stamp["partials"]) != stamp["hash"]:
                raise ValueError("ArchiveTimeStamp " + str(position + 1) + " of chain " + str(index + 1)
                                 + " does not cover its data")
            if roots is not None:
                timestamp_signature(token_reply(stamp["token"]), roots)
            if times and stamp["time"] < times[-1]:
                raise ValueError("ArchiveTimeStamp " + str(position + 1) + " of chain " + str(index + 1)
                                 + " is older than the one it renews")
            times.append(stamp["time"])
        previous.append(chain["raw"])
    newest = record["chains"][-1]["stamps"][-1]
    return {"chains": len(record["chains"]), "stamps": len(times), "earliest": times[0], "newest": times[-1],
            "algorithm": record["chains"][-1]["algorithm"], "signer_expires": newest["signer"].not_valid_after_utc
            if newest["signer"] else None}


def query(name, value):
    nonce = os.urandom(16).lstrip(b"\0") or b"\0"
    if nonce[0] & 0x80:
        nonce = b"\0" + nonce
    imprint = der(0x30, der(0x30, OID_BYTES[name] + b"\x05\x00") + der(0x04, value))
    return der(0x30, der(0x02, b"\x01") + imprint + der(0x02, nonce) + der(0x01, b"\xff"))


def accept(reply, name, value, request, roots):
    found = timestamp_token(reply)
    info = tst_info(found["tst"])
    if info["algorithm"] != ALGORITHMS[name] or info["hash"] != value:
        raise ValueError("The timestamp does not cover the evidence record hash")
    if info["nonce"] != query_nonce(request):
        raise ValueError("The timestamp nonce differs from the request")
    signed = timestamp_signature(reply, roots)
    _, start, end = element(reply, 0)
    parts = children(reply, start, end)
    return reply[parts[1][1]:parts[1][3]], {"time": info["time"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                                            "authority": signed["signer"]}


def record_name(stem, generation):
    return stem + (".renewal-" + str(generation) if generation else "") + ".ers"


def newest_records(folder):
    found = {}
    for path in folder.glob("checkpoint-*.ers") if folder.is_dir() else []:
        match = RECORD_FILE.fullmatch(path.name)
        if match and not path.is_symlink():
            generation = int(match[2] or 0)
            if generation >= found.get(match[1], (-1, None))[0]:
                found[match[1]] = (generation, path)
    return found


def missing_checkpoints(root):
    folder = root / "checkpoints"
    covered = newest_records(folder / "anchors")
    return [path for path in sorted(folder.glob("checkpoint-*.json")) if CHECKPOINT_FILE.fullmatch(path.name)
            and not path.is_symlink() and path.name[:-5] not in covered]


def write_record(folder, stem, generation, data):
    target = folder / record_name(stem, generation)
    if target.exists():
        raise ValueError("Evidence record already exists: " + target.name)
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    private_write(target, data)
    return target


def renewal_due(record, rules, now, demand=None):
    newest = record["chains"][-1]["stamps"][-1]
    if record["chains"][-1]["algorithm"] in rules.weak_algorithms:
        return "hashtree", "the hash algorithm " + record["chains"][-1]["algorithm"] + " is marked weak"
    if demand == "hashtree":
        return "hashtree", "requested"
    if newest["signature_digest"] in rules.weak_algorithms:
        return "timestamp", "the timestamp signature uses " + newest["signature_digest"] + ", marked weak"
    if newest["signer"] is not None:
        expires = newest["signer"].not_valid_after_utc
        if expires - now <= timedelta(days=round(rules.months_before_expiry * 30.4375)):
            return "timestamp", "the signing certificate of the newest timestamp expires " + expires.strftime(
                "%Y-%m-%dT%H:%M:%SZ")
    if demand == "timestamp":
        return "timestamp", "requested"
    if newest["signer"] is None:
        raise ValueError("The newest timestamp does not carry its signing certificate; its expiry cannot be checked")
    return None


def stronger(name, rules):
    choices = [n for n in STRENGTH if STRENGTH.index(n) > STRENGTH.index(name) and n not in rules.weak_algorithms]
    preferred = rules.stronger_algorithm
    if preferred in choices:
        return preferred
    if not choices:
        raise ValueError("No hash algorithm stronger than " + name + " is available")
    return choices[-1]


def plan(root, rules, now=None, demand=None):
    now = now or datetime.now(timezone.utc)
    folder = root / "checkpoints"
    jobs, problems = {}, []
    for stem, (generation, path) in sorted(newest_records(folder / "anchors").items()):
        try:
            data = path.read_bytes()
            record = parse(data)
            due = renewal_due(record, rules, now, demand)
            if not due:
                continue
            kind, reason = due
            source = folder / (stem + ".json")
            item = source.read_bytes() if source.is_file() and not source.is_symlink() else None
            if item is None:
                raise ValueError("The checkpoint this record covers is missing")
            check(data, [item])
            if kind == "timestamp":
                name = record["chains"][-1]["algorithm"]
                leaf = digest(name, record["chains"][-1]["stamps"][-1]["token"])
            else:
                name = stronger(record["chains"][-1]["algorithm"], rules)
                leaf = chained(name, digest(name, item), der(0x30, b"".join(c["raw"] for c in record["chains"])))
            jobs.setdefault((kind, name), []).append({"stem": stem, "generation": generation, "data": data,
                                                      "record": record, "item": item, "leaf": leaf,
                                                      "reason": reason})
        except Exception as exc:
            problems.append({"file": path.name, "error": str(exc)[:200] or type(exc).__name__})
    return jobs, problems


def kept(before, after):
    old, new = before["chains"], after["chains"]
    if len(new) < len(old):
        raise ValueError("A renewal must keep the earlier evidence unchanged")
    for index, chain in enumerate(old):
        raws = [s["raw"] for s in chain["stamps"]]
        if [s["raw"] for s in new[index]["stamps"][:len(raws)]] != raws or (
                index < len(old) - 1 and new[index]["raw"] != chain["raw"]):
            raise ValueError("A renewal must keep the earlier evidence unchanged")


def renew(folder, kind, name, entries, token, paths):
    written, problems = [], []
    for entry in entries:
        try:
            chains = [{"algorithm": c["algorithm"], "stamps": [s["raw"] for s in c["stamps"]]}
                      for c in entry["record"]["chains"]]
            stamp = archive_timestamp(paths[entry["leaf"]], token)
            if kind == "timestamp":
                chains[-1]["stamps"].append(stamp)
            else:
                chains.append({"algorithm": name, "stamps": [stamp]})
            data = encode(chains)
            check(data, [entry["item"]])
            kept(entry["record"], parse(data))
            written.append(write_record(folder, entry["stem"], entry["generation"] + 1, data).name)
        except Exception as exc:
            problems.append({"file": record_name(entry["stem"], entry["generation"]),
                             "error": str(exc)[:200] or type(exc).__name__})
    return written, problems


def create(folder, name, items, token, paths):
    written, problems = [], []
    for stem, item in items:
        try:
            data = encode([{"algorithm": name, "stamps": [archive_timestamp(paths[digest(name, item)], token)]}])
            check(data, [item])
            written.append(write_record(folder, stem, 0, data).name)
        except Exception as exc:
            problems.append({"file": stem + ".json", "error": str(exc)[:200] or type(exc).__name__})
    return written, problems


def manifest_xml(objects, record_name):
    from .asic import MEDIA_TYPES, NAMESPACE
    lines = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
             '<asic:ASiCManifest xmlns:asic=' + quoteattr(NAMESPACE)
             + ' xmlns:ds="http://www.w3.org/2000/09/xmldsig#">',
             '<asic:SigReference URI=' + quoteattr(record_name) + ' MimeType=' + quoteattr(RECORD_MEDIA_TYPE) + '/>']
    for name, value in objects:
        suffix = "." + name.rsplit(".", 1)[-1].lower() if "." in name.rsplit("/", 1)[-1] else ""
        lines += ['<asic:DataObjectReference URI=' + quoteattr(quote(name, safe="/-._~"))
                  + ' MimeType=' + quoteattr(MEDIA_TYPES.get(suffix, "application/octet-stream")) + '>',
                  '<ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>',
                  '<ds:DigestValue>' + escape(base64.b64encode(bytes.fromhex(value)).decode()) + '</ds:DigestValue>',
                  '</asic:DataObjectReference>']
    lines.append('</asic:ASiCManifest>')
    return ("\n".join(lines) + "\n").encode("utf-8")


def seal_container(archive, digests, stamp):
    from .asic import data_object
    objects = [(name, value) for name, value in digests.items() if data_object(name)]
    values = sorted(bytes.fromhex(value) for _, value in objects)
    if len(values) < 2:
        raise ValueError("An export evidence record needs at least two files")
    token, stamped = stamp(b"".join(values))
    data = encode([{"algorithm": "sha256", "stamps": [archive_timestamp([values], token)]}])
    record = parse(data)["chains"][0]["stamps"][0]
    if root_hash("sha256", values, record["partials"]) != record["hash"]:
        raise ValueError("The export timestamp does not cover the file hash list")
    manifest = manifest_xml(objects, CONTAINER_RECORD)
    archive.writestr(CONTAINER_MANIFEST, manifest)
    archive.writestr(CONTAINER_RECORD, data)
    return {"record": CONTAINER_RECORD, "manifest": CONTAINER_MANIFEST, "files": len(objects),
            "record_sha256": hashlib.sha256(data).hexdigest(), **stamped}
