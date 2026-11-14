import base64
import hashlib
import zipfile
from datetime import datetime, timezone
from urllib.parse import quote
from xml.sax.saxutils import escape, quoteattr

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa

from .pdf_report import (CONTENT_TYPE, DATA, MESSAGE_DIGEST, SHA256, SIGNED_DATA, SIGNING_CERTIFICATE_V2,
                         SIGNING_TIME, _int, _oid, _seq, _set, _tlv)

MIMETYPE_NAME, MIMETYPE = "mimetype", b"application/vnd.etsi.asic-e+zip"
MANIFEST, SIGNATURE = "META-INF/ASiCManifest.xml", "META-INF/signature.p7s"
NAMESPACE = "http://uri.etsi.org/02918/v1.2.1#"
SIGNATURE_TIME_STAMP = "1.2.840.113549.1.9.16.2.14"
ECDSA_SHA256, RSA_SHA256 = "1.2.840.10045.4.3.2", "1.2.840.113549.1.1.11"
MEDIA_TYPES = {".json": "application/json", ".jsonl": "application/x-ndjson", ".html": "text/html",
               ".csv": "text/csv", ".txt": "text/plain", ".pdf": "application/pdf", ".py": "text/x-python",
               ".zip": "application/zip", ".xml": "application/xml", ".cmd": "text/plain", ".sh": "text/plain",
               ".js": "text/javascript", ".css": "text/css"}


class LocalSigner:
    def __init__(self, key, certificate):
        self.key, self.chain = key, [certificate.public_bytes(serialization.Encoding.DER)]
        if isinstance(key, ec.EllipticCurvePrivateKey):
            self.algorithm = ECDSA_SHA256
        elif isinstance(key, rsa.RSAPrivateKey):
            self.algorithm = RSA_SHA256
        else:
            raise ValueError("Unsupported signing key")

    def certificates(self):
        return list(self.chain)

    def sign(self, signed_attributes):
        if self.algorithm == ECDSA_SHA256:
            value = self.key.sign(signed_attributes, ec.ECDSA(hashes.SHA256()))
        else:
            value = self.key.sign(signed_attributes, padding.PKCS1v15(), hashes.SHA256())
        return value, list(self.chain)


def workspace_signer(vault):
    from .pdf_report import identity
    return LocalSigner(*identity(vault))


def data_object(name):
    return name != MIMETYPE_NAME and not name.startswith("META-INF/")


def write_mimetype(archive):
    if archive.infolist():
        raise ValueError("The mimetype entry must be the first entry of an ASiC-E container")
    info = zipfile.ZipInfo(MIMETYPE_NAME, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_STORED
    archive.writestr(info, MIMETYPE)


def is_container(archive):
    infos = archive.infolist()
    if not infos:
        return False
    first = min(infos, key=lambda info: info.header_offset)
    if first.filename != MIMETYPE_NAME or first.header_offset or first.compress_type != zipfile.ZIP_STORED \
            or first.extra or first.file_size != len(MIMETYPE):
        return False
    return archive.read(first) == MIMETYPE


def manifest_xml(objects, signature_name):
    lines = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
             '<asic:ASiCManifest xmlns:asic=' + quoteattr(NAMESPACE)
             + ' xmlns:ds="http://www.w3.org/2000/09/xmldsig#">',
             '<asic:SigReference URI=' + quoteattr(signature_name) + ' MimeType="application/x-pkcs7-signature"/>']
    for name, digest in objects:
        suffix = "." + name.rsplit(".", 1)[-1].lower() if "." in name.rsplit("/", 1)[-1] else ""
        lines += ['<asic:DataObjectReference URI=' + quoteattr(quote(name, safe="/-._~"))
                  + ' MimeType=' + quoteattr(MEDIA_TYPES.get(suffix, "application/octet-stream")) + '>',
                  '<ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>',
                  '<ds:DigestValue>' + escape(base64.b64encode(bytes.fromhex(digest)).decode())
                  + '</ds:DigestValue>',
                  '</asic:DataObjectReference>']
    lines.append('</asic:ASiCManifest>')
    return ("\n".join(lines) + "\n").encode("utf-8")


def archive_objects(archive, digests=None):
    found = []
    for info in sorted(archive.infolist(), key=lambda item: item.header_offset):
        if not data_object(info.filename) or info.is_dir():
            continue
        if digests is not None:
            if info.filename not in digests:
                raise ValueError("Missing digest for " + info.filename)
            found.append((info.filename, digests[info.filename]))
            continue
        digest = hashlib.sha256()
        with archive.open(info) as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        found.append((info.filename, digest.hexdigest()))
    return found


def attribute(kind, value):
    return _seq(_oid(kind), _set(value))


def cades(content, signer, timestamp=None, when=None):
    chain = signer.certificates()
    certificate = x509.load_der_x509_certificate(chain[0])
    issuer, serial = certificate.issuer.public_bytes(), certificate.serial_number
    when = when or datetime.now(timezone.utc)
    reference = _seq(_tlv(0x04, hashlib.sha256(chain[0]).digest()), _seq(_seq(_tlv(0xA4, issuer)), _int(serial)))
    signed = _set(attribute(CONTENT_TYPE, _oid(DATA)),
                  attribute(SIGNING_TIME, _tlv(0x17, when.strftime("%y%m%d%H%M%SZ").encode())),
                  attribute(MESSAGE_DIGEST, _tlv(0x04, hashlib.sha256(content).digest())),
                  attribute(SIGNING_CERTIFICATE_V2, _seq(_seq(reference))))
    value, returned = signer.sign(signed)
    if not returned or returned[0] != chain[0]:
        raise ValueError("The signer returned a different certificate")
    details = {"format": "CAdES", "level": "B-B", "signing_time": when.strftime("%Y-%m-%dT%H:%M:%SZ"),
               "certificate_sha256": hashlib.sha256(chain[0]).hexdigest(), "signer": certificate.subject.rfc4514_string()}
    unsigned = []
    if timestamp is not None:
        try:
            token, stamped = timestamp(value)
            unsigned.append(b"\xa1" + _set(attribute(SIGNATURE_TIME_STAMP, token))[1:])
            details.update(level="B-T", timestamp=stamped)
        except Exception as exc:
            details["timestamp_error"] = str(exc)[:500] or type(exc).__name__
    info = _seq(_int(1), _seq(issuer, _int(serial)), _seq(_oid(SHA256)), b"\xa0" + signed[1:],
                _seq(_oid(signer.algorithm)), _tlv(0x04, value), *unsigned)
    body = _seq(_int(1), _set(_seq(_oid(SHA256))), _seq(_oid(DATA)), _tlv(0xA0, b"".join(sorted(returned))),
                _set(info))
    return _seq(_oid(SIGNED_DATA), _tlv(0xA0, body)), details


def seal(archive, digests, signer, timestamp=None):
    manifest = manifest_xml(archive_objects(archive, digests), SIGNATURE)
    signature, details = cades(manifest, signer, timestamp)
    archive.writestr(MANIFEST, manifest)
    archive.writestr(SIGNATURE, signature)
    return {"container": "ASiC-E", "manifest": MANIFEST, "signature": SIGNATURE,
            "manifest_sha256": hashlib.sha256(manifest).hexdigest(), **details}


def reply_token(reply):
    from .verifier.timestamps import children, der
    tag, start, end = der(reply, 0)
    parts = children(reply, start, end) if tag == 0x30 else []
    if len(parts) != 2 or parts[1][0] != 0x30:
        raise ValueError("The timestamp reply carries no token")
    return reply[parts[1][1]:parts[1][3]]


def tsa_timestamp(urls, post):
    from .anchor import timestamp_request
    from .tsa_roots import trusted_roots
    from .verifier.timestamps import timestamp_reply_summary, timestamp_signature

    def stamp(value):
        problems = []
        for url in urls:
            try:
                query = timestamp_request(value)
                reply = post(url, query)
                summary = timestamp_reply_summary(reply, hashlib.sha256(value).digest(), query)
                signed = timestamp_signature(reply, trusted_roots())
                return reply_token(reply), {"service": url, "time": summary["time"], "authority": signed["signer"]}
            except Exception as exc:
                problems.append(url + ": " + (str(exc)[:200] or type(exc).__name__))
        raise ValueError("; ".join(problems) or "No timestamp authority is configured")
    return stamp
