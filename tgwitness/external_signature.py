import base64
import hashlib
import json
import re
import shutil
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from cryptography import x509
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed448, ed25519, padding, rsa

from . import asic
from .pdf_report import _int, _seq, _tlv
from .replica import filesystem_link
from .security import private_write
from .store import utcnow

try:
    from .verifier import national
except ImportError:
    national = None

ATTACHED, VERIFIED, UNSUPPORTED = "attached_not_checked", "verified", "algorithm_not_supported"
INVALID, MISMATCH, UNTRUSTED = "signature_invalid", "bytes_mismatch", "trust_not_established"
REQUESTED = "requested"
RANK = (INVALID, MISMATCH, UNSUPPORTED, ATTACHED, UNTRUSTED, VERIFIED)
DIRECTORY = "external-signatures"
MAX_SIGNATURE_BYTES, MAX_CERTIFICATE_BYTES = 16 * 1024 * 1024, 1024 * 1024
SIGNED_DATA, DATA = "1.2.840.113549.1.7.2", "1.2.840.113549.1.7.1"
CONTENT_TYPE, MESSAGE_DIGEST, SIGNING_TIME = "1.2.840.113549.1.9.3", "1.2.840.113549.1.9.4", "1.2.840.113549.1.9.5"
SIGNING_CERTIFICATE, SIGNING_CERTIFICATE_V2 = "1.2.840.113549.1.9.16.2.12", "1.2.840.113549.1.9.16.2.47"
SIGNATURE_TIME_STAMP = "1.2.840.113549.1.9.16.2.14"
DIGESTS = {"2.16.840.1.101.3.4.2.1": hashes.SHA256, "2.16.840.1.101.3.4.2.2": hashes.SHA384,
           "2.16.840.1.101.3.4.2.3": hashes.SHA512, "2.16.840.1.101.3.4.2.4": hashes.SHA224,
           "2.16.840.1.101.3.4.2.8": hashes.SHA3_256, "2.16.840.1.101.3.4.2.9": hashes.SHA3_384,
           "2.16.840.1.101.3.4.2.10": hashes.SHA3_512}
RSA_PKCS1 = {"1.2.840.113549.1.1.1": None, "1.2.840.113549.1.1.11": hashes.SHA256,
             "1.2.840.113549.1.1.12": hashes.SHA384, "1.2.840.113549.1.1.13": hashes.SHA512,
             "1.2.840.113549.1.1.14": hashes.SHA224}
RSA_PSS, MGF1 = "1.2.840.113549.1.1.10", "1.2.840.113549.1.1.8"
ECDSA = {"1.2.840.10045.2.1": None, "1.2.840.10045.4.3.1": hashes.SHA224, "1.2.840.10045.4.3.2": hashes.SHA256,
         "1.2.840.10045.4.3.3": hashes.SHA384, "1.2.840.10045.4.3.4": hashes.SHA512}
ED25519, ED448 = "1.3.101.112", "1.3.101.113"
NAMES = {"2.16.840.1.101.3.4.2.1": "SHA-256", "2.16.840.1.101.3.4.2.2": "SHA-384", "2.16.840.1.101.3.4.2.3": "SHA-512",
         "2.16.840.1.101.3.4.2.4": "SHA-224", "2.16.840.1.101.3.4.2.8": "SHA3-256", "2.16.840.1.101.3.4.2.9": "SHA3-384",
         "2.16.840.1.101.3.4.2.10": "SHA3-512", "1.3.14.3.2.26": "SHA-1", "1.2.840.113549.1.1.1": "RSA PKCS#1 v1.5",
         "1.2.840.113549.1.1.11": "RSA PKCS#1 v1.5 with SHA-256", "1.2.840.113549.1.1.12": "RSA PKCS#1 v1.5 with SHA-384",
         "1.2.840.113549.1.1.13": "RSA PKCS#1 v1.5 with SHA-512", "1.2.840.113549.1.1.14": "RSA PKCS#1 v1.5 with SHA-224",
         RSA_PSS: "RSASSA-PSS", "1.2.840.10045.2.1": "ECDSA", "1.2.840.10045.4.3.1": "ECDSA with SHA-224",
         "1.2.840.10045.4.3.2": "ECDSA with SHA-256", "1.2.840.10045.4.3.3": "ECDSA with SHA-384",
         "1.2.840.10045.4.3.4": "ECDSA with SHA-512", ED25519: "Ed25519", ED448: "Ed448",
         "1.2.804.2.1.1.1.1.2.1": "GOST 34.311 (DSTU)", "1.2.804.2.1.1.1.1.3.1.1": "DSTU 4145",
         "1.2.804.2.1.1.1.1.3.1.1.2.6": "DSTU 4145"}
INSTRUCTIONS = {
    "asice": "Sign this file exactly as downloaded, without opening or saving it again, as a CMS (CAdES) signature in "
             "a .p7s file, detached or with the content embedded, using SHA-256 or stronger. The file is an ASiC "
             "manifest that lists every file of the export with its SHA-256, so the signature covers the export as it "
             "is now. Upload the .p7s here; TgWitness adds it and this manifest to the container under META-INF "
             "without changing any other file.",
    "zip": "Sign this file exactly as downloaded, without opening or saving it again, as a CMS (CAdES) signature in a "
           ".p7s file, detached or with the content embedded, using SHA-256 or stronger. The file is the manifest.json "
           "of the export, which lists every other file of the export with its SHA-256, so the signature covers the "
           "export as it is now. Upload the .p7s here; TgWitness keeps it next to the export and includes it when you "
           "download the export with signatures."}


def told(text, **values):
    return {"text": text, "values": values} if values else text


def plain(reason):
    return reason["text"].format(**reason["values"]) if isinstance(reason, dict) else reason


class Unsupported(Exception):
    def __init__(self, text, **values):
        self.reason = told(text, **values)
        super().__init__(plain(self.reason))


def read(data, offset, end):
    if offset + 2 > end:
        raise ValueError("Truncated ASN.1 data")
    tag, first, at = data[offset], data[offset + 1], offset + 2
    if tag & 0x1F == 0x1F:
        raise ValueError("Unsupported ASN.1 tag")
    if first == 0x80:
        if not tag & 0x20:
            raise ValueError("Malformed ASN.1 length")
        start = at
        while True:
            if at + 2 > end:
                raise ValueError("Truncated ASN.1 data")
            if data[at] == 0 and data[at + 1] == 0:
                return tag, offset, start, at, at + 2
            at = read(data, at, end)[4]
    if first & 0x80:
        count = first & 0x7F
        if not 1 <= count <= 4 or at + count > end:
            raise ValueError("Unsupported ASN.1 length")
        length, at = int.from_bytes(data[at:at + count], "big"), at + count
    else:
        length = first
    if at + length > end:
        raise ValueError("Truncated ASN.1 data")
    return tag, offset, at, at + length, at + length


def items(data, node):
    found, at = [], node[2]
    while at < node[3]:
        child = read(data, at, node[3])
        found.append(child)
        at = child[4]
    return found


def raw(data, node):
    return data[node[1]:node[4]]


def value(data, node):
    return data[node[2]:node[3]]


def object_id(data, node):
    from .verifier.timestamps import oid
    if node[0] != 0x06:
        raise ValueError("Expected an object identifier")
    return oid(data, node[2], node[3])


def octets(data, node):
    if node[0] == 0x04:
        return value(data, node)
    if node[0] == 0x24:
        return b"".join(octets(data, child) for child in items(data, node))
    raise ValueError("Expected an octet string")


def algorithm(data, node):
    parts = items(data, node) if node[0] == 0x30 else []
    if not parts:
        raise ValueError("Malformed algorithm identifier")
    return object_id(data, parts[0]), raw(data, parts[1]) if len(parts) > 1 else b""


def attributes(data, node):
    found = {}
    for item in items(data, node):
        parts = items(data, item)
        if len(parts) != 2 or parts[1][0] != 0x31:
            raise ValueError("Malformed attribute")
        name = object_id(data, parts[0])
        if name in found:
            raise ValueError("Repeated attribute " + name)
        found[name] = [raw(data, child) for child in items(data, parts[1])]
    return found


def signer_info(data, node):
    parts = items(data, node)
    if len(parts) < 5 or parts[0][0] != 0x02:
        raise ValueError("Malformed signer information")
    sid = parts[1]
    if sid[0] == 0x30:
        issuer, serial = items(data, sid)
        identifier = ("issuer", raw(data, issuer), int.from_bytes(value(data, serial), "big", signed=True))
    elif sid[0] == 0x80:
        identifier = ("key", value(data, sid))
    else:
        raise ValueError("Unsupported signer identifier")
    rest, signed = parts[3:], None
    if rest and rest[0][0] == 0xA0:
        signed, rest = rest[0], rest[1:]
    if len(rest) < 2 or rest[0][0] != 0x30 or rest[1][0] != 0x04:
        raise ValueError("Malformed signer information")
    unsigned = rest[2] if len(rest) > 2 and rest[2][0] == 0xA1 else None
    return {"sid": identifier, "digest_algorithm": algorithm(data, parts[2]),
            "signed_bytes": _tlv(0x31, value(data, signed)) if signed else None,
            "attributes": attributes(data, signed) if signed else None,
            "signature_algorithm": algorithm(data, rest[0]), "signature": value(data, rest[1]),
            "unsigned": attributes(data, unsigned) if unsigned else {}}


def structure(data):
    top = read(data, 0, len(data))
    if top[0] != 0x30 or top[4] != len(data):
        raise ValueError("The file is not a CMS structure")
    parts = items(data, top)
    if len(parts) != 2 or object_id(data, parts[0]) != SIGNED_DATA or parts[1][0] != 0xA0:
        raise ValueError("The file is not CMS SignedData")
    inner = items(data, parts[1])
    if len(inner) != 1 or inner[0][0] != 0x30:
        raise ValueError("The file is not CMS SignedData")
    fields = items(data, inner[0])
    if len(fields) < 4 or fields[0][0] != 0x02 or fields[1][0] != 0x31 or fields[2][0] != 0x30 or fields[-1][0] != 0x31:
        raise ValueError("The file is not CMS SignedData")
    return parts, fields


def parse(data):
    parts, fields = structure(data)
    encapsulated = items(data, fields[2])
    if not encapsulated:
        raise ValueError("The signature has no content type")
    content = None
    if len(encapsulated) > 1:
        wrapped = items(data, encapsulated[1]) if encapsulated[1][0] == 0xA0 else []
        if len(wrapped) != 1:
            raise ValueError("Malformed embedded content")
        content = octets(data, wrapped[0])
    certificates = []
    for field in fields[3:-1]:
        if field[0] == 0xA0:
            certificates += [raw(data, child) for child in items(data, field) if child[0] == 0x30]
    signers = [signer_info(data, node) for node in items(data, fields[-1])]
    if not signers:
        raise ValueError("The signature has no signer")
    return {"content_type": object_id(data, encapsulated[0]), "content": content, "certificates": certificates,
            "signers": signers}


def detached(data):
    parts, fields = structure(data)
    encapsulated = items(data, fields[2])
    if len(encapsulated) < 2:
        return data
    body = b"".join(_seq(raw(data, encapsulated[0])) if field is fields[2] else raw(data, field) for field in fields)
    return _seq(raw(data, parts[0]), _tlv(0xA0, _seq(body)))


def digest(oid, data):
    if oid not in DIGESTS and national is not None:
        try:
            return national.digest(oid, data)
        except national.Unsupported:
            pass
    if oid not in DIGESTS:
        raise Unsupported("Digest algorithm {name} is not supported", name=NAMES.get(oid, oid))
    hasher = hashes.Hash(DIGESTS[oid]())
    hasher.update(data)
    return hasher.finalize()


def hash_for(oid):
    if oid not in DIGESTS:
        raise Unsupported("Digest algorithm {name} is not supported", name=NAMES.get(oid, oid))
    return DIGESTS[oid]()


def pss_parameters(parameters):
    chosen, mask, salt = None, None, 20
    if parameters:
        node = read(parameters, 0, len(parameters))
        for part in items(parameters, node):
            inner = items(parameters, part)
            if part[0] == 0xA0:
                chosen = hash_for(algorithm(parameters, inner[0])[0])
            elif part[0] == 0xA1:
                kind, nested = algorithm(parameters, inner[0])
                if kind != MGF1:
                    raise Unsupported("RSASSA-PSS mask generation {name} is not supported", name=kind)
                mask = hash_for(algorithm(nested, read(nested, 0, len(nested)))[0])
            elif part[0] == 0xA2:
                salt = int.from_bytes(value(parameters, inner[0]), "big")
            elif part[0] == 0xA3 and int.from_bytes(value(parameters, inner[0]), "big") != 1:
                raise Unsupported("RSASSA-PSS trailer field is not supported")
    if chosen is None or mask is None:
        raise Unsupported("RSASSA-PSS with the SHA-1 defaults is not supported")
    return chosen, mask, salt


def verify_signature(spki, signature_algorithm, parameters, signature, message, digest_algorithm):
    if signature_algorithm not in RSA_PKCS1 and signature_algorithm not in ECDSA \
            and signature_algorithm not in (RSA_PSS, ED25519, ED448):
        if national is not None:
            try:
                if national.verify(spki, signature_algorithm, signature, message):
                    return None
            except national.Unsupported:
                pass
            else:
                raise InvalidSignature()
        raise Unsupported("Signature algorithm {name} is not supported",
                          name=NAMES.get(signature_algorithm, signature_algorithm))
    try:
        key = serialization.load_der_public_key(spki)
    except (ValueError, UnsupportedAlgorithm):
        raise Unsupported("The signer key type is not supported") from None
    if signature_algorithm in RSA_PKCS1 and isinstance(key, rsa.RSAPublicKey):
        chosen = RSA_PKCS1[signature_algorithm]
        return key.verify(signature, message, padding.PKCS1v15(), chosen() if chosen else hash_for(digest_algorithm))
    if signature_algorithm == RSA_PSS and isinstance(key, rsa.RSAPublicKey):
        chosen, mask, salt = pss_parameters(parameters)
        return key.verify(signature, message, padding.PSS(mgf=padding.MGF1(mask), salt_length=salt), chosen)
    if signature_algorithm in ECDSA and isinstance(key, ec.EllipticCurvePublicKey):
        chosen = ECDSA[signature_algorithm]
        return key.verify(signature, message, ec.ECDSA(chosen() if chosen else hash_for(digest_algorithm)))
    if signature_algorithm == ED25519 and isinstance(key, ed25519.Ed25519PublicKey) \
            or signature_algorithm == ED448 and isinstance(key, ed448.Ed448PublicKey):
        return key.verify(signature, message)
    raise ValueError("The signature algorithm does not match the signer key")


def certificate_fields(der):
    certificate = read(der, 0, len(der))
    tbs = items(der, items(der, certificate)[0])
    if tbs and tbs[0][0] == 0xA0:
        tbs = tbs[1:]
    if len(tbs) < 6:
        raise ValueError("Malformed certificate")
    return {"serial": int.from_bytes(value(der, tbs[0]), "big", signed=True), "issuer": raw(der, tbs[2]),
            "spki": raw(der, tbs[5])}


def load_certificates(data):
    data = data or b""
    if not data.strip():
        return []
    if len(data) > MAX_CERTIFICATE_BYTES:
        raise ValueError("The certificate file is too large")
    try:
        found = x509.load_pem_x509_certificates(data) if b"-----BEGIN" in data else [x509.load_der_x509_certificate(data)]
    except ValueError:
        raise ValueError("The certificate file is not PEM or DER X.509") from None
    if not found:
        raise ValueError("The certificate file holds no certificate")
    return found


def signature_bytes(data):
    if len(data) > MAX_SIGNATURE_BYTES:
        raise ValueError("The signature file is too large")
    if data[:1] == b"\x30":
        return data
    found = re.search(rb"-----BEGIN [A-Z0-9 ]+-----(.*?)-----END [A-Z0-9 ]+-----", data, re.S)
    try:
        decoded = base64.b64decode(b"".join((found.group(1) if found else data).split()), validate=True)
    except ValueError:
        decoded = b""
    if decoded[:1] != b"\x30":
        raise ValueError("The file is not a DER, PEM or Base64 CMS signature")
    return decoded


def describe(certificate, der):
    return {"subject": certificate.subject.rfc4514_string(), "issuer": certificate.issuer.rfc4514_string(),
            "serial": format(certificate.serial_number, "x"), "sha256": hashlib.sha256(der).hexdigest(),
            "not_before": certificate.not_valid_before_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "not_after": certificate.not_valid_after_utc.strftime("%Y-%m-%dT%H:%M:%SZ")}


def find_signer(identifier, pool):
    for der in pool:
        try:
            fields = certificate_fields(der)
            if identifier[0] == "issuer" and fields["issuer"] == identifier[1] and fields["serial"] == identifier[2]:
                return der
            if identifier[0] == "key":
                extension = x509.load_der_x509_certificate(der).extensions.get_extension_for_class(x509.SubjectKeyIdentifier)
                if extension.value.digest == identifier[1]:
                    return der
        except (ValueError, x509.ExtensionNotFound):
            continue
    return None


def certificate_reference(attributes, der):
    if SIGNING_CERTIFICATE_V2 in attributes:
        name, chosen = SIGNING_CERTIFICATE_V2, "2.16.840.1.101.3.4.2.1"
    elif SIGNING_CERTIFICATE in attributes:
        name, chosen = SIGNING_CERTIFICATE, None
    else:
        return "absent"
    data = attributes[name][0]
    certificates = items(data, read(data, 0, len(data)))
    first = items(data, items(data, certificates[0])[0])
    if first[0][0] == 0x30:
        chosen, first = algorithm(data, first[0])[0], first[1:]
    expected = digest(chosen, der) if chosen else hashlib.sha1(der).digest()
    if not first or first[0][0] != 0x04 or value(data, first[0]) != expected:
        raise ValueError("The signing-certificate attribute names a different certificate")
    return "matches" if chosen else "matches_sha1"


def attribute_time(data):
    node = read(data, 0, len(data))
    text = value(data, node).decode("ascii")
    if node[0] == 0x17:
        when = datetime.strptime(text, "%y%m%d%H%M%SZ")
    elif node[0] == 0x18:
        when = datetime.strptime(text.split(".")[0].rstrip("Z"), "%Y%m%d%H%M%S")
    else:
        raise ValueError("Malformed signing time")
    return when.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def timestamp_check(token, signature, roots):
    from .verifier.timestamps import timestamp_signature, timestamp_token, tst_info
    try:
        reply = _seq(_seq(_int(0)), token)
        info = tst_info(timestamp_token(reply)["tst"])
        found = {"time": info["time"].strftime("%Y-%m-%dT%H:%M:%SZ"), "verified": False}
        if digest(info["algorithm"], signature) != info["hash"]:
            return {**found, "error": "The timestamp covers other bytes than this signature value"}
        signed = timestamp_signature(reply, roots)
        return {**found, "verified": True, "authority": signed["signer"], "root": signed["root"]}
    except Exception as exc:
        return {"verified": False, "error": str(exc)[:300] or type(exc).__name__}


def issued(child, parent):
    try:
        child.verify_directly_issued_by(parent)
        return True
    except (ValueError, TypeError, InvalidSignature, UnsupportedAlgorithm):
        return False


def chain_check(signer, pool, roots, when):
    if not roots:
        return False, "No trusted root certificate was supplied, so the certificate chain was not checked.", []
    trusted = {root.fingerprint(hashes.SHA256()): root for root in roots}
    chain, current = [signer], signer
    while current.fingerprint(hashes.SHA256()) not in trusted:
        if len(chain) > 8:
            return False, "The certificate chain is too long.", []
        issuer = next((candidate for candidate in [*roots, *pool] if candidate not in chain
                       and candidate.subject == current.issuer and issued(current, candidate)), None)
        if issuer is None:
            return False, "The certificate chain does not reach a supplied root certificate.", []
        try:
            authority = issuer.extensions.get_extension_for_class(x509.BasicConstraints).value.ca
        except x509.ExtensionNotFound:
            authority = False
        if not authority:
            return False, "A certificate in the chain is not a certificate authority.", []
        chain.append(issuer)
        current = issuer
    for certificate in chain:
        if not certificate.not_valid_before_utc <= when <= certificate.not_valid_after_utc:
            return False, told("A certificate in the chain was not valid at {time}.",
                               time=when.strftime("%Y-%m-%dT%H:%M:%SZ")), []
    try:
        usage = signer.extensions.get_extension_for_class(x509.KeyUsage).value
        if not usage.digital_signature and not usage.content_commitment:
            return False, "The signer certificate does not allow signatures.", []
    except x509.ExtensionNotFound:
        pass
    return True, "", [certificate.subject.rfc4514_string() for certificate in chain]


def check_signer(cms, signer, expected, pool, roots, timestamp_roots):
    found = {"state": ATTACHED, "reasons": [], "binding": False, "signature": False,
             "digest_algorithm": NAMES.get(signer["digest_algorithm"][0], signer["digest_algorithm"][0]),
             "signature_algorithm": NAMES.get(signer["signature_algorithm"][0], signer["signature_algorithm"][0]),
             "signature_algorithm_oid": signer["signature_algorithm"][0]}
    der = find_signer(signer["sid"], pool)
    if der is None:
        found["reasons"].append("The signer certificate is neither in the signature nor among the supplied certificates.")
        return found
    try:
        certificate = x509.load_der_x509_certificate(der)
        found["certificate"] = describe(certificate, der)
    except ValueError:
        found["reasons"].append("The signer certificate could not be read.")
        return found
    attributes = signer["attributes"]
    try:
        spki = certificate_fields(der)["spki"]
        if attributes is not None:
            content_type, message_digest = attributes.get(CONTENT_TYPE), attributes.get(MESSAGE_DIGEST)
            if not content_type or not message_digest:
                raise ValueError("The signed attributes lack the content type or the message digest")
            if object_id(content_type[0], read(content_type[0], 0, len(content_type[0]))) != cms["content_type"]:
                raise ValueError("The signed content type differs from the content type of the signature")
            verify_signature(spki, *signer["signature_algorithm"], signer["signature"], signer["signed_bytes"],
                             signer["digest_algorithm"][0])
            found["signing_certificate_attribute"] = certificate_reference(attributes, der)
            if SIGNING_TIME in attributes:
                found["claimed_signing_time"] = attribute_time(attributes[SIGNING_TIME][0])
            stated = octets(message_digest[0], read(message_digest[0], 0, len(message_digest[0])))
            found["signature"] = True
            if digest(signer["digest_algorithm"][0], expected) != stated:
                found.update(state=MISMATCH)
                found["reasons"].append("The signature is valid but covers other bytes than this export asked to sign.")
                return found
        else:
            verify_signature(spki, *signer["signature_algorithm"], signer["signature"], expected,
                             signer["digest_algorithm"][0])
            found["signature"] = True
    except Unsupported as exc:
        found.update(state=UNSUPPORTED, signature=False)
        found["reasons"].append(exc.reason)
        return found
    except (InvalidSignature, ValueError, IndexError) as exc:
        found.update(state=INVALID, signature=False)
        found["reasons"].append(str(exc) or "The signature value does not verify with the signer certificate.")
        return found
    found["binding"] = True
    when = datetime.now(timezone.utc)
    found["validation_time_basis"] = "time of this check"
    tokens = signer["unsigned"].get(SIGNATURE_TIME_STAMP) or []
    if tokens:
        found["timestamp"] = timestamp_check(tokens[0], signer["signature"], timestamp_roots)
        if found["timestamp"]["verified"]:
            when = datetime.strptime(found["timestamp"]["time"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            found["validation_time_basis"] = "verified timestamp"
    found["validation_time"] = when.strftime("%Y-%m-%dT%H:%M:%SZ")
    others = []
    for item in pool:
        try:
            others.append(x509.load_der_x509_certificate(item))
        except ValueError:
            continue
    trusted, reason, chain = chain_check(certificate, others, roots, when)
    if trusted:
        found.update(state=VERIFIED, chain=chain)
    else:
        found["state"] = UNTRUSTED
        found["reasons"].append(reason)
    return found


def verify(data, expected, roots=(), certificates=()):
    from .tsa_roots import trusted_roots
    result = {"state": ATTACHED, "reasons": [], "signers": [], "checked_at": utcnow(),
              "revocation": "not checked", "trust_list": "not checked"}
    try:
        cms = parse(data)
    except (ValueError, IndexError) as exc:
        result.update(state=INVALID)
        result["reasons"].append(told("The file is not a readable CMS signature: {reason}", reason=str(exc)))
        return result
    result["embedded"] = cms["content"] is not None
    pool = cms["certificates"] + [item.public_bytes(serialization.Encoding.DER) for item in certificates]
    timestamp_roots = list(roots) + list(trusted_roots())
    for signer in cms["signers"]:
        result["signers"].append(check_signer(cms, signer, expected, pool, list(roots), timestamp_roots))
    result["state"] = min((item["state"] for item in result["signers"]), key=RANK.index)
    if cms["content"] is not None and cms["content"] != expected:
        result["state"] = min(result["state"], MISMATCH, key=RANK.index)
        result["reasons"].append("The content embedded in the signature differs from the bytes this export asked to sign.")
    return result


def valid_id(ident):
    return isinstance(ident, str) and len(ident) == 32 and all(c in "0123456789abcdef" for c in ident)


def folder(store, export_id, create=False):
    if not valid_id(export_id):
        raise ValueError("This prepared export is unavailable.")
    base = store.root / DIRECTORY
    if filesystem_link(base):
        raise ValueError("The external signature directory must not be a filesystem link.")
    if create:
        base.mkdir(mode=0o700, exist_ok=True)
    target = base / export_id
    if filesystem_link(target) or target.exists() and target.resolve().parent != base.resolve():
        raise ValueError("The external signature directory must not be a filesystem link.")
    if create:
        target.mkdir(mode=0o700, exist_ok=True)
    return target


def tag(number):
    return str(number).zfill(3)


def records(directory):
    found = []
    for item in sorted(directory.glob("[0-9][0-9][0-9].json")) if directory.is_dir() else []:
        if not filesystem_link(item):
            found.append(json.loads(item.read_bytes()))
    return found


def record(directory, number):
    if not isinstance(number, str) or not re.fullmatch(r"[0-9]{1,3}", number) or not 1 <= int(number) <= 999:
        raise ValueError("Unknown signature request.")
    path = directory / (tag(int(number)) + ".json")
    if not path.is_file() or filesystem_link(path):
        raise ValueError("Unknown signature request.")
    return json.loads(path.read_bytes())


def inspect(path):
    with open(path, "rb") as stream:
        whole = hashlib.file_digest(stream, "sha256").hexdigest()
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(names) != len(set(names)):
            raise ValueError("The export has duplicate members.")
        container = asic.is_container(archive)
        try:
            inventory = archive.read("manifest.json")
            files = json.loads(inventory).get("files")
        except (KeyError, ValueError, AttributeError):
            files = None
        if not isinstance(files, dict):
            raise ValueError("This export has no inventory file that lists every member.")
        listed = [name for name in names if asic.data_object(name)] if container else names
        if set(listed) != set(files) | {"manifest.json", "manifest.sig"}:
            raise ValueError("The inventory of this export does not list exactly its members.")
        objects = asic.archive_objects(archive)
        computed = dict(objects)
        if any(computed.get(name) != digest for name, digest in files.items()):
            raise ValueError("A member of this export differs from its inventory.")
        return {"kind": "asice" if container else "zip", "objects": objects, "inventory": inventory, "sha256": whole,
                "meta": [name for name in names if name.startswith("META-INF/")],
                "program": {name: archive.read(name) for name in (asic.MANIFEST, asic.SIGNATURE) if container and name in names}}


def expected_content(found, item):
    if found["kind"] == "asice":
        return asic.manifest_xml(found["objects"], item["signature_name"])
    return found["inventory"]


def request(store, export_id, path, entry):
    if entry.get("encrypted"):
        raise ValueError("Password-protected exports cannot be signed here: their inventory is not readable without the password.")
    found = inspect(path)
    if found["sha256"] != entry["sha256"]:
        raise ValueError("The saved export changed. Prepare a new export.")
    directory = folder(store, export_id, True)
    taken = {item["number"] for item in records(directory)}
    taken |= {int(match[1]) for name in found["meta"] if (match := re.fullmatch(r"META-INF/(?:ASiCManifest|signature)([0-9]{3})\.(?:xml|p7s)", name))}
    number = next((n for n in range(1, 1000) if n not in taken), None)
    if number is None:
        raise ValueError("This export already has the maximum number of signature requests.")
    if found["kind"] == "asice":
        names = {"signed_name": "META-INF/ASiCManifest" + tag(number) + ".xml",
                 "signature_name": "META-INF/signature" + tag(number) + ".p7s"}
    else:
        names = {"signed_name": "manifest.json", "signature_name": "signature-" + tag(number) + ".p7s"}
    item = {"number": number, "export_id": export_id, "export_sha256": entry["sha256"], "export_format": entry["format"],
            "kind": found["kind"], **names, "requested_at": utcnow()}
    content = expected_content(found, item)
    item.update(content_sha256=hashlib.sha256(content).hexdigest(), content_bytes=len(content))
    private_write(directory / (tag(number) + ".content"), content)
    private_write(directory / (tag(number) + ".json"), json.dumps(item, indent=1).encode())
    return {**item, "state": REQUESTED, "instruction": INSTRUCTIONS[found["kind"]],
            "content_base64": base64.b64encode(content).decode(), "filename": filename(item)}


def filename(item):
    if item["kind"] == "asice":
        return "tgwitness-" + item["export_id"][:8] + "-" + item["signed_name"].rsplit("/", 1)[-1]
    return "tgwitness-" + item["export_id"][:8] + "-manifest.json"


def attach(store, export_id, number, signature, roots=b"", certificates=b""):
    directory = folder(store, export_id)
    item = record(directory, number)
    if item.get("attached_at"):
        raise ValueError("A signature is already attached to this request. Prepare a new request for another signature.")
    data = signature_bytes(signature)
    load_certificates(roots)
    load_certificates(certificates)
    name = tag(item["number"])
    private_write(directory / (name + ".p7s"), data)
    private_write(directory / (name + ".roots.pem"), roots or b"")
    private_write(directory / (name + ".certificates.pem"), certificates or b"")
    item.update(attached_at=utcnow(), signature_sha256=hashlib.sha256(data).hexdigest(), signature_bytes=len(data))
    private_write(directory / (name + ".json"), json.dumps(item, indent=1).encode())
    return item


def supply(store, export_id, number, roots=None, certificates=None):
    directory = folder(store, export_id)
    item = record(directory, number)
    if not item.get("attached_at"):
        raise ValueError("Attach a signature first.")
    for suffix, data in ((".roots.pem", roots), (".certificates.pem", certificates)):
        if data is not None:
            load_certificates(data)
            private_write(directory / (tag(item["number"]) + suffix), data)
    return item


def stored(directory, item, suffix):
    path = directory / (tag(item["number"]) + suffix)
    return path.read_bytes() if path.is_file() and not filesystem_link(path) else b""


def evaluate(directory, item, found, problem):
    content = stored(directory, item, ".content")
    public = {key: item.get(key) for key in ("number", "kind", "signed_name", "signature_name", "content_sha256",
                                             "content_bytes", "requested_at", "attached_at", "signature_sha256",
                                             "export_sha256")}
    public.update(instruction=INSTRUCTIONS.get(item.get("kind"), ""), reasons=[])
    if hashlib.sha256(content).hexdigest() != item.get("content_sha256"):
        public.update(state=MISMATCH, reasons=["The stored bytes to sign changed after the request."])
        return public
    if not item.get("attached_at"):
        public["state"] = REQUESTED
        if problem is not None:
            public["reasons"].append(problem)
        elif found is None or found.get("error") or expected_content(found, item) != content:
            public.update(state=MISMATCH, reasons=["This export changed after the bytes were prepared. Prepare a new "
                                                   "request; do not sign the earlier bytes."])
        else:
            public.update(content_base64=base64.b64encode(content).decode(), filename=filename(item))
        return public
    data = stored(directory, item, ".p7s")
    try:
        roots = load_certificates(stored(directory, item, ".roots.pem"))
        extra = load_certificates(stored(directory, item, ".certificates.pem"))
    except ValueError:
        roots, extra = [], []
    public["roots"] = [{"subject": root.subject.rfc4514_string(), "sha256": root.fingerprint(hashes.SHA256()).hex()}
                       for root in roots]
    if hashlib.sha256(data).hexdigest() != item.get("signature_sha256"):
        public.update(state=INVALID, reasons=["The stored signature file changed after it was attached."])
        return public
    try:
        result = verify(data, content, roots, extra)
    except Exception as exc:
        public.update(state=ATTACHED, reasons=[told("The signature could not be checked: {reason}",
                                                    reason=str(exc)[:200] or type(exc).__name__)])
        return public
    public.update(result)
    public["reasons"] = list(result["reasons"])
    if problem is not None:
        public["state"] = min(public["state"], ATTACHED, key=RANK.index)
        public["reasons"].insert(0, problem)
    elif found is None or found.get("error"):
        reason = (found or {}).get("error") or "The export could not be read."
        public["state"] = min(public["state"], MISMATCH, key=RANK.index)
        public["reasons"].insert(0, told("This export changed after the bytes were prepared: {reason}", reason=reason))
    elif expected_content(found, item) != content:
        public["state"] = min(public["state"], MISMATCH, key=RANK.index)
        public["reasons"].insert(0, "This export changed after the bytes were prepared; the signature no longer matches it.")
    public["export_binding"] = "checked" if problem is None else "not checked"
    return public


def status(store, export_id, path, entry, problem=None):
    directory = folder(store, export_id)
    found, eligible = None, None
    if entry.get("encrypted"):
        eligible = "Password-protected exports cannot be signed here: their inventory is not readable without the password."
    elif problem is None:
        try:
            found = inspect(path)
        except (ValueError, RuntimeError, NotImplementedError, zipfile.BadZipFile, OSError) as exc:
            found, eligible = {"error": str(exc)}, str(exc)
    signatures = []
    for item in records(directory):
        frozen = found
        if found is not None and not found.get("error") and found["sha256"] != item.get("export_sha256"):
            frozen = {"error": "The export file is no longer the one whose bytes were prepared for signing."}
        signatures.append(evaluate(directory, item, frozen, problem))
    result = {"export_id": export_id, "kind": found.get("kind") if found else None,
              "eligible": problem is None and eligible is None, "reason": problem or eligible, "signatures": signatures}
    if found and found.get("program"):
        result["program_signature"] = program_signature(found)
    return result


def program_signature(found):
    manifest, signature = found["program"].get(asic.MANIFEST), found["program"].get(asic.SIGNATURE)
    if manifest is None or signature is None:
        return {"state": ATTACHED, "reasons": ["The container has no program signature."]}
    result = verify(signature, manifest)
    result["note"] = ("CAdES signature made with this workspace's own self-issued certificate. The certificate is not "
                      "qualified and is not on any trusted list. The Ed25519 seal (manifest.sig) is a separate check.")
    if asic.manifest_xml(found["objects"], asic.SIGNATURE) != manifest:
        result["state"] = min(result["state"], MISMATCH, key=RANK.index)
        result["reasons"].insert(0, "The ASiC manifest does not list exactly the files of this container.")
    return result


def includable(item):
    return item.get("attached_at") and item.get("state") not in (INVALID, MISMATCH, REQUESTED)


def signed_copy(store, export_id, path, entry):
    directory = folder(store, export_id)
    report = status(store, export_id, path, entry)
    chosen = [item for item in report["signatures"] if includable(item)]
    if not chosen:
        raise ValueError("No signature can be included: none is attached, or every attached one is invalid or "
                         "covers other bytes.")
    target = store.root / "temporary-exports"
    if filesystem_link(target) or target.resolve().parent != store.root.resolve():
        raise ValueError("Temporary export directory must belong to this workspace.")
    target.mkdir(mode=0o700, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix="tgwitness-export-signed-", suffix=".zip", dir=target, delete=False) as handle:
        output = Path(handle.name)
    try:
        if report["kind"] == "asice":
            shutil.copyfile(path, output)
            with zipfile.ZipFile(output, "a", compression=zipfile.ZIP_DEFLATED) as archive:
                for item in chosen:
                    data = detached(stored(directory, item, ".p7s"))
                    content = stored(directory, item, ".content")
                    archive.writestr(item["signed_name"], content)
                    archive.writestr(item["signature_name"], data)
        else:
            inner = "tgwitness-" + entry["format"] + ".zip"
            lines = ["External signatures for " + inner + " (SHA-256 " + entry["sha256"] + ").", ""]
            with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.write(path, inner, compress_type=zipfile.ZIP_STORED)
                for item in chosen:
                    name = tag(item["number"])
                    archive.writestr(item["signature_name"], stored(directory, item, ".p7s"))
                    archive.writestr("signed-bytes-" + name + ".json", stored(directory, item, ".content"))
                    lines += [item["signature_name"] + ": CMS signature over manifest.json inside " + inner
                              + "; signed-bytes-" + name + ".json is an identical copy of those bytes (SHA-256 "
                              + item["content_sha256"] + "). State in TgWitness when downloaded: " + item["state"] + "."]
                lines += ["", "manifest.json lists every other file of the export with its SHA-256. Check the signature "
                          "with your own tools; TgWitness did not check revocation or trusted lists."]
                archive.writestr("SIGNATURES.txt", "\n".join(lines) + "\n")
        return output, report["kind"], [item["number"] for item in chosen]
    except BaseException:
        output.unlink(missing_ok=True)
        raise
