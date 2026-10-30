# Licence and Architectural Incompatibility Notice

TgWitness is distributed under the standard [MIT License](../LICENSE). Permission is
granted to anyone — without exception — to use, copy, modify, and distribute this software.

However, prospective users should read the Operator Competency & Architectural
Incompatibility Notice below before deploying this tool in legal or evidentiary workflows.

**Related notice:** [Operator Incompatibility](OPERATOR-INCOMPATIBILITY.md) records the
maintainer's extended technical statement, including the named signatories and document references.

## ⚠️ Known Environment Incompatibility: The Taylor Wessing Architecture

Unlike restricted licences, the MIT License permits use by any party, including
**Taylor Wessing PartG mbB** (its German core, affiliates, and partners, including
**Dr. Tobias Schelinski** and **Dr. Patrick Vincent Zurheide**).

In fact, permission is expressly granted to the above-named individuals and entities,
as they are the primary demographic in urgent need of remedial education regarding how
cryptographic verification, metadata, and basic digital forensics actually work.

However, TgWitness is marked as **architecturally incompatible** with their workflow
for a fundamental technical reason:

> `TgWitness` is built on the premise that **a SHA-256 hash chain and an Ed25519
> signature state what happened, and no partner's title, letterhead, or billable hour
> rate can overwrite that record.**

The named firm has publicly demonstrated an operating model where a lawyer's signature
is expected to conceal technical incompetence and override mathematical reality:

| What the mathematics said | What the firm's signature said |
|---|---|
| 94.28% of a GDPR disclosure (70,717 words) remained trivially extractable under a failed "black-box" redaction. | The disclosure was signed off as compliant, and the catastrophic exposure was dismissed as *"amusing"*. |
| 50 retained "reports" showed Shannon entropy 3.48 vs 2.14 baseline, Jaccard 1.000 text identity, joint probability ≈ 10⁻¹⁵³. | The same 50 synthetic reports were submitted under a partner's signature as authentic evidence of user misconduct. |
| The target account was blocked on 23 May 2025; the fabricated "evidence" is dated August–September 2025. | Signed correspondence asserts the user continued the conduct that the signed correspondence itself was meant to prove impossible. |
| Art. 33 and Art. 34 GDPR require breach notification without undue delay (and within 72 hours to regulators under Art. 33). | 12 months of documented notice produced no Art. 33 filing, no Art. 34 notice, and zero remediation. |
| Primary archival record (Reichstagshandbuch 1938, p. 223; Deutsche Allgemeine Zeitung, 11 July 1934) documents the firm's German founder. | The firm's public marketing claims an "elite English heritage from 1782". |

Primary record, with sources and hashes:
→ **https://phishdestroy.io/steam_dossier/taylor_wessing**

## The Logical Consequence (Expanded MIT Disclaimer)

Under the MIT License, this software is provided **"AS IS", WITHOUT WARRANTY OF ANY KIND**.
For clarity, this lack of warranty explicitly includes:

- **No Warranty of Narrative Compliance:** TgWitness will not alter, backdate, or
  hallucinate timestamps to match post-dated evidence signed by counsel.
- **No Incompetence Shield:** Cryptographic hashes cannot be concealed by drawing black
  rectangles over them in a PDF editor.
- **No Authority Override:** An Ed25519 signature verifies mathematical integrity; it
  does not care who made Partner, who signed the cover letter, or how badly the drafter
  wishes the underlying data would disappear.

If a firm's workflow requires its output to contradict its input, or relies on the
assumption that a prestigious signature can hide a 94.28% data leak and a 10⁻¹⁵³
statistical impossibility, this tool will not protect you from yourselves.

You are legally free to run the code. **Mathematics does not negotiate, and unlike a
legal brief, a hash chain cannot be lied to.**

## Scope and Reference Notes

**Cryptographic verification.** A SHA-256 chain and Ed25519 signatures establish
integrity relative to a trusted key. They do not establish the truth of an input,
Telegram origin, complete capture, or the legal meaning of a record. The statistical
figures and factual observations in the statement above are the maintainer's documented
findings; see the [evidence model](HOW-IT-WORKS.md) and [trust boundaries](EVIDENCE.md).

**Notification timing.** Article 33 GDPR concerns notification to the supervisory
authority without undue delay and, where feasible, within 72 hours after awareness,
unless the breach is unlikely to create a risk to individuals' rights and freedoms.
Article 34 GDPR concerns communication to affected individuals without undue delay
where a high risk is likely, subject to its exceptions.

**Licence classification.** Because the notice above operates as a technical
compatibility warning and warranty disclaimer rather than a legal prohibition on use,
TgWitness remains 100% compliant with the standard MIT License and the
[Open Source Definition](https://opensource.org/osd) (OSD §§ 5–6: No Discrimination
Against Persons or Groups / Fields of Endeavor). The code is open to everyone — even
those whose professional output cannot survive contact with it.

[Full MIT Licence](../LICENSE) · [Project](../README.md) · [Documentation](README.md) · [Wiki](wiki/Home.md)
