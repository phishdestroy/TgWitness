from .common import (
    Ed25519PublicKey,
    MAX_JSON_BYTES,
    MAX_MANIFEST_BYTES,
    VerifierTooOld,
    base64,
    bounded_lines,
    hashlib,
    io,
    open_archive,
    re,
    read_manifest,
    read_member,
    strict_json,
)
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
    from .account import verify_account_export
    from .chat import verify_chat_export
    from .live import LIVE_START, verify_live_export
    from .board import verify_board
    from .chain import canonical, fingerprint, is_format
    from .completeness import COMPLETENESS_KINDS, completeness_certificate
    from .coverage import Coverage
    from .journal import media_reference, verify_checkpoint, verify_event_lines
    from .outside import OutsideRecords, confirm_drand
    from .parallel import MemberHashes
    from .reports import archive_seal, check_sums, report_companions
    from .timestamps import verify_anchors, verify_tdx_starts
    from .witness import assurance
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
        from .evidence_records import verify_evidence_records
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
