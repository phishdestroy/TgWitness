import asyncio
import hashlib
import re
import threading
import zlib
from datetime import datetime, timezone

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509 import ocsp

from .anchor import timestamp_request
from .anchoring import REVOCATION_LIMITS, problem, revocation_sources
from .pdf_report import BYTE_RANGE_PLACEHOLDER, CONTENTS_HEX, ECDSA_SHA256, RSA_SHA256, signed_data
from .tsa_roots import trusted_roots
from .verify import children, der, revocation_status, timestamp_reply_summary, timestamp_signature, timestamp_token

LEVELS = ("B-B", "B-T", "B-LT", "B-LTA")
SIGNATURE_TIMESTAMP = "1.2.840.113549.1.9.16.2.14"
DER = serialization.Encoding.DER
WHITESPACE, DELIMITERS = b"\x00\t\n\x0c\r ", b"()<>[]{}/%"
REFERENCE = re.compile(rb"(\d+)\s+(\d+)\s+R(?![^\s()<>\[\]{}/%])")
WORD = re.compile(rb"[^\s()<>\[\]{}/%]+")
SUBSECTION = re.compile(rb"\s*(\d+)\s+(\d+)[ \t]*\r?\n")


class KeySigner:
    def __init__(self, key, certificate, chain=()):
        if not isinstance(key, (ec.EllipticCurvePrivateKey, rsa.RSAPrivateKey)):
            raise ValueError("Only RSA and ECDSA keys can sign PDF reports")
        self.key, self.certificate, self.chain = key, certificate, list(chain)
        self.algorithm = ECDSA_SHA256 if isinstance(key, ec.EllipticCurvePrivateKey) else RSA_SHA256

    def sign(self, data):
        if self.algorithm == ECDSA_SHA256:
            return self.key.sign(data, ec.ECDSA(hashes.SHA256()))
        return self.key.sign(data, padding.PKCS1v15(), hashes.SHA256())


def pkcs12_signer(data, password=None):
    key, certificate, extra = pkcs12.load_key_and_certificates(data, password)
    if key is None or certificate is None:
        raise ValueError("The PKCS#12 file holds no private key with its certificate")
    path = chain(certificate, list(extra), [])
    return KeySigner(key, certificate, path[1:] + [item for item in extra if item not in path])


def issued_by(certificate, issuer):
    if certificate.issuer != issuer.subject:
        return False
    try:
        certificate.verify_directly_issued_by(issuer)
    except (ValueError, TypeError, InvalidSignature):
        return False
    return True


def chain(leaf, pool, roots):
    anchors = {root.fingerprint(hashes.SHA256()) for root in roots}
    path = [leaf]
    while path[-1].fingerprint(hashes.SHA256()) not in anchors and not issued_by(path[-1], path[-1]):
        issuer = next((item for item in pool if item not in path and issued_by(path[-1], item)), None)
        if issuer is None or len(path) > 8:
            return path
        path.append(issuer)
    return path


def complete(path, roots):
    anchors = {root.fingerprint(hashes.SHA256()) for root in roots}
    if path[-1].fingerprint(hashes.SHA256()) not in anchors and not issued_by(path[-1], path[-1]):
        raise ValueError("The issuer of " + path[-1].subject.rfc4514_string() + " is not available")
    return path


def network_fetch(network):
    from .netclient import request

    def fetch(method, url, headers, body, limit, timeout):
        found = {}

        def run():
            try:
                found["value"] = asyncio.run(request(method, url, network, headers, body, timeout=timeout,
                                                     limit=limit))[2]
            except Exception as exc:
                found["error"] = exc
        worker = threading.Thread(target=run, name="pades-fetch", daemon=True)
        worker.start()
        worker.join(timeout + 15)
        if "error" in found:
            raise found["error"]
        if "value" not in found:
            raise TimeoutError(url)
        return found["value"]
    return fetch


def stamp(data, urls, fetch, roots):
    errors = []
    for url in urls:
        try:
            query = timestamp_request(data)
            reply = fetch("POST", url, {"Content-Type": "application/timestamp-query",
                                        "Accept": "application/timestamp-reply"}, query, 256 * 1024, 15)
            summary = timestamp_reply_summary(reply, hashlib.sha256(data).digest(), query)
            signed = timestamp_signature(reply, roots)
            _, start, end = der(reply, 0)
            token = children(reply, start, end)[1]
            certificates = [x509.load_der_x509_certificate(item) for item in timestamp_token(reply)["certificates"]]
            signer = next(item for item in certificates
                          if item.fingerprint(hashes.SHA256()).hex() == signed["signer_sha256"])
            return {"url": url, "time": summary["time"], "token": reply[token[1]:token[3]], "signer": signer,
                    "certificates": certificates}
        except Exception as exc:
            errors.append(url + ": " + problem(exc))
    raise ValueError("; ".join(errors) if errors else "No timestamp authority is configured")


def revocation(subject, issuer, fetch, when):
    errors = []
    for kind, url in revocation_sources(subject):
        try:
            if kind == "ocsp":
                query = ocsp.OCSPRequestBuilder().add_certificate(subject, issuer, hashes.SHA1()).build().public_bytes(DER)
                answer = fetch("POST", url, {"Content-Type": "application/ocsp-request",
                                             "Accept": "application/ocsp-response"}, query, REVOCATION_LIMITS[kind], 15)
            else:
                answer = fetch("GET", url, {"Accept": "application/pkix-crl"}, b"", REVOCATION_LIMITS[kind], 20)
            state = revocation_status(kind, answer, {"signer": subject, "issuer": issuer, "time": when})
            if state["status"] != "good":
                raise ValueError(state["detail"])
            if kind == "ocsp":
                return kind, answer, list(ocsp.load_der_ocsp_response(answer).certificates)
            if not answer.lstrip().startswith(b"-----"):
                return kind, answer, []
            return kind, x509.load_pem_x509_crl(answer).public_bytes(DER), []
        except Exception as exc:
            errors.append(kind.upper() + " " + url + ": " + problem(exc))
    raise ValueError("No revocation data for " + subject.subject.rfc4514_string() + ": "
                     + ("; ".join(errors) if errors else "the certificate names no OCSP or CRL address"))


def validation_data(signer, stamped, fetch, roots, when):
    pool = [signer.certificate, *signer.chain, *stamped["certificates"], *roots]
    certificates, answers = [], {"ocsp": [], "crl": []}
    for leaf in (signer.certificate, stamped["signer"]):
        path = complete(chain(leaf, pool, roots), roots)
        certificates += path
        for subject, issuer in zip(path, path[1:]):
            kind, answer, extra = revocation(subject, issuer, fetch, when)
            answers[kind].append(answer)
            certificates += extra
    unique = list(dict.fromkeys(item.public_bytes(DER) for item in certificates))
    return unique, list(dict.fromkeys(answers["ocsp"])), list(dict.fromkeys(answers["crl"]))


class Name(str):
    pass


class Ref(tuple):
    pass


class Raw(bytes):
    pass


def skip(data, pos):
    while pos < len(data):
        if data[pos] in WHITESPACE:
            pos += 1
        elif data[pos] == 0x25:
            while pos < len(data) and data[pos] not in b"\r\n":
                pos += 1
        else:
            break
    return pos


def parse(data, pos):
    pos = skip(data, pos)
    if data.startswith(b"<<", pos):
        found, pos = {}, pos + 2
        while not data.startswith(b">>", skip(data, pos)):
            key, pos = parse(data, pos)
            if not isinstance(key, Name):
                raise ValueError("Malformed PDF dictionary")
            found[key], pos = parse(data, pos)
        return found, skip(data, pos) + 2
    if data.startswith(b"[", pos):
        items, pos = [], pos + 1
        while not data.startswith(b"]", skip(data, pos)):
            item, pos = parse(data, pos)
            items.append(item)
        return items, skip(data, pos) + 1
    if data.startswith(b"/", pos):
        end = pos + 1
        while end < len(data) and data[end] not in WHITESPACE + DELIMITERS:
            end += 1
        return Name(data[pos + 1:end].decode("latin-1")), end
    if data.startswith(b"(", pos):
        depth, end = 0, pos
        while True:
            if data[end] == 0x5C:
                end += 2
                continue
            depth += (data[end] == 0x28) - (data[end] == 0x29)
            end += 1
            if depth == 0:
                return Raw(data[pos:end]), end
    if data.startswith(b"<", pos):
        end = data.index(b">", pos) + 1
        return Raw(data[pos:end]), end
    found = REFERENCE.match(data, pos) or WORD.match(data, pos)
    if not found:
        raise ValueError("Malformed PDF object")
    return (Ref((int(found[1]), int(found[2]))) if found.re is REFERENCE else Raw(found[0])), found.end()


def dump(value):
    if isinstance(value, dict):
        return b"<<" + b" ".join(b"/" + key.encode("latin-1") + b" " + dump(item) for key, item in value.items()) + b">>"
    if isinstance(value, list):
        return b"[" + b" ".join(dump(item) for item in value) + b"]"
    if isinstance(value, Name):
        return b"/" + value.encode("latin-1")
    if isinstance(value, Ref):
        return b"%d %d R" % value
    return bytes(value)


class Document:
    def __init__(self, data):
        self.data = bytes(data)
        found = re.search(rb"startxref\s+(\d+)\s+%%EOF\s*$", self.data)
        if not found:
            raise ValueError("The PDF does not end with a cross-reference table")
        self.startxref, self.offsets, self.trailer = int(found[1]), {}, None
        at, seen = self.startxref, set()
        try:
            while at is not None and at not in seen:
                seen.add(at)
                if not self.data.startswith(b"xref", at):
                    raise ValueError("PDF files with cross-reference streams are not supported")
                pos = at + 4
                while (section := SUBSECTION.match(self.data, pos)):
                    first, count, pos = int(section[1]), int(section[2]), section.end()
                    for index in range(count):
                        entry = self.data[pos + 20 * index:pos + 20 * index + 20]
                        self.offsets.setdefault(first + index, int(entry[:10]) if entry[17:18] == b"n" else None)
                    pos += 20 * count
                head = re.compile(rb"\s*trailer").match(self.data, pos)
                if not head:
                    raise ValueError("The PDF cross-reference table has no trailer")
                trailer = parse(self.data, head.end())[0]
                self.trailer = self.trailer or trailer
                at = int(trailer["Prev"]) if "Prev" in trailer else None
        except (IndexError, KeyError, TypeError) as exc:
            raise ValueError("Unreadable PDF cross-reference table") from exc
        self.size = int(self.trailer["Size"])

    def get(self, ref):
        at = self.offsets.get(ref[0])
        head = re.compile(rb"%d\s+%d\s+obj" % tuple(ref)).match(self.data, at) if at is not None else None
        if not head:
            raise ValueError("PDF object " + str(ref[0]) + " is missing")
        try:
            value, end = parse(self.data, head.end())
        except (IndexError, ValueError) as exc:
            raise ValueError("PDF object " + str(ref[0]) + " is unreadable") from exc
        if self.data.startswith(b"stream", skip(self.data, end)):
            raise ValueError("PDF object " + str(ref[0]) + " is a stream")
        return value

    def resolve(self, value):
        return self.get(value) if isinstance(value, Ref) else value

    def allocate(self):
        self.size += 1
        return Ref((self.size - 1, 0))

    def update(self, objects):
        body = self.data if self.data.endswith(b"\n") else self.data + b"\n"
        offsets = {}
        for ref, value in sorted(objects.items()):
            offsets[ref] = len(body)
            body += b"%d %d obj\n" % ref + value + b"\nendobj\n"
        table, refs = b"xref\n", sorted(offsets)
        while refs:
            group = [refs.pop(0)]
            while refs and refs[0][0] == group[-1][0] + 1:
                group.append(refs.pop(0))
            table += b"%d %d\n" % (group[0][0], len(group)) + b"".join(
                b"%010d %05d n \n" % (offsets[ref], ref[1]) for ref in group)
        trailer = {Name("Size"): Raw(b"%d" % max(self.size, max(ref[0] for ref in offsets) + 1)),
                   **{Name(key): self.trailer[key] for key in ("Root", "Info", "ID") if key in self.trailer},
                   Name("Prev"): Raw(b"%d" % self.startxref)}
        return body + table + b"trailer\n" + dump(trailer) + b"\nstartxref\n%d\n%%%%EOF\n" % len(body)


def catalog_for_validation(doc, catalog):
    extensions = dict(doc.resolve(catalog.get("Extensions")) or {})
    extensions[Name("ESIC")] = {Name("BaseVersion"): Name("1.7"), Name("ExtensionLevel"): Raw(b"1")}
    catalog[Name("Extensions")] = extensions
    header = re.match(rb"%PDF-(\d\.\d)", doc.data)
    current = str(catalog.get("Version") or (header[1].decode() if header else "1.7"))
    if current < "1.7":
        catalog[Name("Version")] = Name("1.7")
    return catalog


def with_field(data, signature, name, for_validation=False):
    doc = Document(data)
    root = doc.trailer["Root"]
    catalog = doc.get(root)
    objects, sig, field = {}, doc.allocate(), doc.allocate()
    page_ref = catalog["Pages"]
    while "Kids" in (page := doc.get(page_ref)):
        page_ref = doc.resolve(page["Kids"])[0]
    annots = page.get("Annots")
    if isinstance(annots, Ref):
        objects[annots] = dump(doc.get(annots) + [field])
    else:
        page[Name("Annots")] = list(annots or []) + [field]
        objects[page_ref] = dump(page)
    form = catalog.get("AcroForm")
    form_ref = form if isinstance(form, Ref) else None
    form = doc.get(form_ref) if form_ref else dict(form or {})
    fields = form.get("Fields")
    if isinstance(fields, Ref):
        objects[fields] = dump(doc.get(fields) + [field])
    else:
        form[Name("Fields")] = list(fields or []) + [field]
    form[Name("SigFlags")] = Raw(b"3")
    if form_ref:
        objects[form_ref] = dump(form)
    else:
        catalog[Name("AcroForm")] = form
    objects[root] = dump(catalog_for_validation(doc, catalog) if for_validation else catalog)
    objects[field] = dump({Name("Type"): Name("Annot"), Name("Subtype"): Name("Widget"), Name("FT"): Name("Sig"),
                           Name("F"): Raw(b"132"), Name("Rect"): [Raw(b"0")] * 4, Name("P"): page_ref,
                           Name("T"): Raw(b"(" + name.encode("ascii") + b")"), Name("V"): sig})
    objects[sig] = dump({**signature, Name("ByteRange"): Raw(BYTE_RANGE_PLACEHOLDER),
                         Name("Contents"): Raw(b"<" + b"0" * CONTENTS_HEX + b">")})
    updated = doc.update(objects)
    return updated, updated.index(b"%d 0 obj\n" % sig[0], len(doc.data))


def placeholder(data, kind):
    marker = b"/ByteRange " + BYTE_RANGE_PLACEHOLDER
    at = data.find(marker)
    if at < 0 or data.find(marker, at + 1) >= 0:
        return None
    start, end = data.rfind(b" obj", 0, at), data.find(b"endobj", at)
    if start < 0 or end < 0 or b"/SubFilter /" + kind not in data[start:end]:
        raise ValueError("The signature field of this PDF is not prepared for " + kind.decode())
    return start


def fill(data, at, value_for):
    buffer = bytearray(data)
    marker = buffer.find(b"/ByteRange " + BYTE_RANGE_PLACEHOLDER, at) + len(b"/ByteRange ")
    start = buffer.find(b"/Contents <", marker) + len(b"/Contents ")
    end = buffer.find(b">", start) + 1
    if marker < at or start < marker or buffer.find(b"endobj", at, end) >= 0 or set(buffer[start + 1:end - 1]) != {0x30}:
        raise ValueError("The PDF has no signature placeholder")
    buffer[marker:marker + len(BYTE_RANGE_PLACEHOLDER)] = b"[%010d %010d %010d %010d]" % (0, start, end, len(buffer) - end)
    value = value_for(bytes(buffer[:start]) + bytes(buffer[end:])).hex().encode()
    if len(value) > end - start - 2:
        raise ValueError("The PDF signature does not fit its placeholder")
    buffer[start + 1:end - 1] = value + b"0" * (end - start - 2 - len(value))
    return bytes(buffer), bytes.fromhex(buffer[start + 1:end - 1].decode("ascii"))


def with_dss(data, certificates, ocsps, crls, contents):
    doc = Document(data)
    root = doc.trailer["Root"]
    catalog = doc.get(root)
    if "DSS" in catalog:
        raise ValueError("The PDF already has a document security store")
    objects = {}

    def streams(items):
        refs = []
        for item in items:
            packed, ref = zlib.compress(item), doc.allocate()
            objects[ref] = (dump({Name("Length"): Raw(b"%d" % len(packed)), Name("Filter"): Name("FlateDecode")})
                            + b"\nstream\n" + packed + b"\nendstream")
            refs.append(ref)
        return refs
    found = {"Cert": streams(certificates), "OCSP": streams(ocsps), "CRL": streams(crls)}
    store = {Name("Type"): Name("DSS"), **{Name(key + "s"): refs for key, refs in found.items() if refs},
             Name("VRI"): {Name(hashlib.sha1(contents).hexdigest().upper()): {
                 Name(key): refs for key, refs in found.items() if refs}}}
    reference = doc.allocate()
    objects[reference] = dump(store)
    catalog[Name("DSS")] = reference
    objects[root] = dump(catalog_for_validation(doc, catalog))
    return doc.update(objects)


def pdf_date(when):
    return Raw(when.strftime("(D:%Y%m%d%H%M%S+00'00')").encode())


def sign_pdf(data, signer, level="B-B", *, tsa_urls=(), fetch=None, roots=None, attributes=None, reason=None,
             when=None):
    if level not in LEVELS:
        raise ValueError("Unknown PAdES level " + str(level))
    wanted, roots = LEVELS.index(level), list(trusted_roots() if roots is None else roots)
    when = when or datetime.now(timezone.utc)
    outcome = {"requested": level, "level": "B-B", "not_reached": None, "timestamp_authority": None}
    data = bytes(data)
    at = placeholder(data, b"ETSI.CAdES.detached")
    if at is None:
        fields = {Name("Type"): Name("Sig"), Name("Filter"): Name("Adobe.PPKLite"),
                  Name("SubFilter"): Name("ETSI.CAdES.detached"), Name("M"): pdf_date(when)}
        if reason:
            fields[Name("Reason")] = Raw(b"(" + re.sub(rb"([()\\])", rb"\\\1", reason.encode("latin-1", "replace")) + b")")
        data, at = with_field(data, fields, "TgWitness signature")
    stamps = {}

    def missing(next_level, why):
        outcome["not_reached"] = {"level": next_level, "reason": why}

    def value_for(content):
        digest = hashlib.sha256(content).digest()

        def unsigned(signature):
            extra = list(attributes(digest, signer.certificate.public_bytes(DER)) if attributes else [])
            if wanted >= 1:
                try:
                    if fetch is None:
                        raise ValueError("No network route was given for the timestamp authority")
                    stamps["signature"] = stamp(signature, tsa_urls, fetch, roots)
                    extra.append((SIGNATURE_TIMESTAMP, stamps["signature"]["token"]))
                except ValueError as exc:
                    missing("B-T", str(exc))
            return extra
        return signed_data(digest, signer, unsigned)
    data, contents = fill(data, at, value_for)
    if "signature" not in stamps:
        return data, outcome
    outcome.update(level="B-T", timestamp_authority=stamps["signature"]["url"])
    if wanted < 2:
        return data, outcome
    try:
        data = with_dss(data, *validation_data(signer, stamps["signature"], fetch, roots, when), contents)
    except ValueError as exc:
        missing("B-LT", str(exc))
        return data, outcome
    outcome["level"] = "B-LT"
    if wanted < 3:
        return data, outcome
    try:
        prepared, at = with_field(data, {Name("Type"): Name("DocTimeStamp"), Name("Filter"): Name("Adobe.PPKLite"),
                                         Name("SubFilter"): Name("ETSI.RFC3161")}, "TgWitness document time stamp", True)
        data = fill(prepared, at, lambda content: stamp(content, tsa_urls, fetch, roots)["token"])[0]
    except ValueError as exc:
        missing("B-LTA", str(exc))
        return data, outcome
    outcome["level"] = "B-LTA"
    return data, outcome
