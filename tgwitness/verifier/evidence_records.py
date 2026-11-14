from .common import (
    MAX_JSON_BYTES,
    datetime,
    hashes,
    re,
    read_member,
    strict_json,
    timezone,
    x509,
)
from .national import DIGEST_NAMES
from .timestamps import (
    DIGESTS,
    children,
    der,
    hashed,
    oid,
    qualified_timestamp,
    signed_attributes,
    signing_certificate_hash,
    stamp_time,
    timestamp_signature,
    timestamp_token,
    tsa_roots,
    tst_info,
)
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
