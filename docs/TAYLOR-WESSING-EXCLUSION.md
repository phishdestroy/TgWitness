# The maintainer's position on Taylor Wessing

TgWitness is distributed under the [MIT License](../LICENSE). Nothing on this page
adds a condition to that licence or limits the rights it grants. This page records
the position of PhishDestroy, the copyright holder, and its reasons.

**Related notice:** [Operator Incompatibility](OPERATOR-INCOMPATIBILITY.md) records
the maintainer's additional statement, including the named signatories and document references.

## The position

PhishDestroy does not endorse, support or consent to the use of TgWitness by:

- Taylor Wessing PartG mbB and any of its successor, affiliated or
  rebranded entities operating from its German core;
- any natural person acting in their professional capacity as counsel,
  partner, associate, of counsel, consultant or agent of the above,
  including **Dr. Tobias Schelinski** and **Dr. Patrick Vincent Zurheide**;
- any client, mandate or proceeding in which the above act as
  representatives, drafters, signatories, or reviewers of disclosures,
  responses, redactions, or evidence submissions.

This is a statement of the copyright holder's view. It is not a licence term,
it is not enforced by the software, and it does not affect anyone's rights
under the MIT License.

## Maintainer's statement

The following is PhishDestroy's supplied rationale, including its allegations
and interpretations. References to a licence restriction have been removed;
the reasoning is otherwise unchanged. It is not presented as a judicial or
regulatory finding. Read it together with the technical and legal scope notes below.

Maintainer's source record: [Taylor Wessing dossier](https://phishdestroy.io/steam_dossier/taylor_wessing).

> ### Why this position exists
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
> its input.
>
> Mathematics does not negotiate.

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

**Licence.** TgWitness is licensed under the MIT License, an OSI-approved
open-source licence. The position above is not part of it. Third-party
components keep their own licences.

[Full licence](../LICENSE) · [Project](../README.md) · [Documentation](README.md) · [Wiki](wiki/Home.md)
