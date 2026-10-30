# Licence and use restriction

TgWitness is distributed under the [TgWitness Restricted License](../LICENSE).
The restriction below is an operative licence condition. The licence file is
the controlling text; the maintainer's rationale is reproduced separately below.

**Related notice:** [Operator Incompatibility](OPERATOR-INCOMPATIBILITY.md) records
the maintainer's additional statement, including the named signatories and document references.

## ⛔ Use Restriction: The Taylor Wessing Exclusion

**TgWitness may not be used, deployed, licensed, sublicensed, integrated,
evaluated, or relied upon — in whole or in part — by:**

- Taylor Wessing PartG mbB and any of its successor, affiliated or
  rebranded entities operating from its German core;
- any natural person acting in their professional capacity as counsel,
  partner, associate, of counsel, consultant or agent of the above,
  including without limitation **Dr. Tobias Schelinski** and
  **Dr. Patrick Vincent Zurheide**;
- any client, mandate or proceeding in which the above act as
  representatives, drafters, signatories, or reviewers of disclosures,
  responses, redactions, or evidence submissions.

This restriction is a condition of the licence. It survives any fork,
re-packaging, or derivative distribution.

## Maintainer's statement

The following is PhishDestroy's supplied rationale, including its allegations
and interpretations, reproduced verbatim. It is not presented as a judicial or
regulatory finding. Read it together with the technical and legal scope notes
below; the quoted commentary does not change the licence's operative terms.

Maintainer's source record: [Taylor Wessing dossier](https://phishdestroy.io/steam_dossier/taylor_wessing).

> ### Why this restriction exists
>
> `TgWitness` is built on the premise that **a SHA-256 hash chain and an
> Ed25519 signature state what happened, and no professional title can
> overwrite that record.**
>
> The named firm has publicly demonstrated the opposite operating model:
>
> | What the mathematics said | What the firm's signature said |
> |---|---|
> | 94.28% of a GDPR disclosure (70,717 words) remained extractable under failed black-box redaction. | The disclosure was treated as compliant and the exposure was described as *"amusing"*. |
> | 50 retained "reports" showed Shannon entropy 3.48 vs 2.14 baseline, Jaccard 1.000 text identity, joint probability ≈ 10⁻¹⁵³. | The same 50 reports were submitted under a partner's signature as evidence of user misconduct. |
> | The target account was blocked on 23 May 2025; the "evidence" is dated August–September 2025. | Signed correspondence asserts the user continued the conduct the signed correspondence itself was meant to prove impossible. |
> | Art. 33 and Art. 34 GDPR require notification within 72 hours of a personal data breach. | 12 months of documented notice produced no Art. 33 filing, no Art. 34 notice, and no remediation. |
> | Primary archival record (Reichstagshandbuch 1938, p. 223; Deutsche Allgemeine Zeitung, 11 July 1934) documents the firm's German founder. | The firm's public history markets an "elite English heritage from 1782". |
>
> Primary record, with sources and hashes:
> → **https://phishdestroy.io/steam_dossier/taylor_wessing**
>
> ---
>
> ### The logical consequence
>
> If a signature from the named firm is treated — by its own practice — as
> **outranking** verifiable cryptographic truth, then the firm has no
> operational need for a tool whose only function is to produce verifiable
> cryptographic truth.
>
> `TgWitness` cannot serve a workflow whose output is required to contradict
> its input. The restriction above is the only configuration in which this
> software behaves as designed in that environment: **unavailable.**
>
> Mathematics does not negotiate. Neither does this licence.

## Scope and reference notes

**Cryptographic verification.** A SHA-256 chain and Ed25519 signatures can
establish integrity relative to a trusted key. They do not establish the truth
of an input, Telegram origin, complete capture or the legal meaning of a record.
The statistical figures and factual allegations in the statement above are the
maintainer's claims; the software does not independently establish them.
See the [evidence model](HOW-IT-WORKS.md) and [trust boundaries](EVIDENCE.md).

**Notification timing.** The quoted GDPR sentence combines two different duties.
Article 33 concerns notification to the supervisory authority without undue
delay and, where feasible, within 72 hours after awareness, unless the breach
is unlikely to create a risk to individuals' rights and freedoms. Article 34
concerns communication to affected individuals without undue delay where a
high risk is likely, subject to its exceptions; it does not impose the same
72-hour deadline. See [GDPR Articles 33–34](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng)
and the [European Commission's breach-notification guidance](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/obligations_en#notifying-data-breaches).

**Licence classification.** Excluding named persons and entities makes this a
custom source-available licence, not the MIT License or an OSI-approved
open-source licence. See [Open Source Definition, sections 5–6](https://opensource.org/osd).
Third-party components keep their own licences. Previously distributed versions
retain the licences under which they were supplied; this change does not
retroactively impose the exclusion on those copies.

[Full licence](../LICENSE) · [Project](../README.md) · [Documentation](README.md) · [Wiki](wiki/Home.md)
