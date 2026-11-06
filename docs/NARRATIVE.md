# Evidence narratives

`python -m tgwitness.narrative` produces a source-linked account from a **verified full evidence ZIP**. It first authenticates the archive, then creates PDF, HTML, JSON and four SVG diagrams. It never takes a supplied verdict JSON as proof. A failed signature, inconsistent manifest or contradictory witness evidence stops generation.

```sh
python -m tgwitness.narrative evidence.zip --lang de --jurisdiction DE --out narrative-de/
python -m tgwitness.narrative evidence.zip --lang ru --fingerprint COLLECTOR_FP --witness witness.zip --witness-fingerprint WITNESS_FP --check-drand --check-bitcoin --out narrative-ru/
python tools/check_narrative_texts.py
```

Obtain fingerprints independently. An unpinned package can be described, but its missing pin is visible as a limitation. Instructions in the report use `TRUSTED_COLLECTOR_FP` and `TRUSTED_WITNESS_FP`; they never turn an embedded key into an independent trust decision. `--tsa-ca ROOT.pem` enables the existing RFC 3161 root check. External checks use the verifier's existing trust model; see [FOR-THE-RECORD.md](FOR-THE-RECORD.md).

The destination must be empty. Generation stages all outputs before publishing them into that directory. It does not overwrite another report, contact Telegram, submit timestamps, send mail or publish anything. Network checks run only when requested. The input ZIP remains unchanged. The output is a derived report, not a new independently witnessed evidence package.

## Reading the report

Read the introduction, chronology, assurance checks, limitations and verification commands in that order. Jurisdiction terms are optional. The appendix identifies every cited record by journal, sequence number and full SHA-256. The source package SHA-256 appears at the front. Collector and witness sequence numbers have separate namespaces.

A recorded claim is described as a recorded claim. A document event containing `signature_claimed: qualified` and `signature_objects: 0` does **not** become a finding that the PDF is unsigned, forged or legally invalid. The renderer does not independently inspect PDF signatures, validate QES or DKIM, or reconstruct an earlier receipt date. External anchor files receive credit only when the verifier actually checks them. A pending OTS submission remains unconfirmed.

Counts describe event kinds. New messages, edits, deletion notices and absence on recheck remain distinct. Counts do not establish continuous coverage. Unknown events retain their source references and an interpretation limitation. Dates in scenes come from signed event metadata, not an authenticated wall clock. Bitcoin dates are block-header dates, not exact receipt times.

The HTML timeline has keyboard-focusable and hoverable event references. Every SVG has a title and description. The PDF uses selectable text and the same drawing geometry; it does not depend on a browser or an SVG conversion service. Japanese PDF generation uses the project's existing CJK font discovery; a suitable installed font is required. No new package dependency was added.

## Templates and jurisdictions

There are 25 complete phrase catalogs and matching glossaries. Supported languages: en, de, fr, es, it, pt, nl, pl, cs, sk, uk, ru, ro, bg, hu, el, sv, da, fi, no, lt, lv, et, tr, ja. `no` uses Bokmål wording. `pt` uses the generic CLDR Portuguese cardinal rule. Templates support the bounded ICU **plural subset** used in these catalogs, including nested placeholders and exact-number branches; this is not a general implementation of every ICU formatter. Cardinal rules follow [Unicode CLDR](https://www.unicode.org/cldr/charts/48/supplemental/language_plural_rules.html).

The checker compares keys and placeholders, renders plural cases, checks phrase lengths and applies any supplied forbidden-word lists. Every language, including English and German, is visibly marked **machine-assisted, not reviewed**. Passing mechanical tests is not legal or native-language review.

Jurisdiction catalogs contain terminology and official source references checked on 2026-11-06. They cover DE, AT, CH, UK, IE, FR, ES, IT, PL, CZ, UA, NL, BE and US-federal. `UK` is explicitly scoped to **England and Wales civil proceedings**; it does not represent Scotland or Northern Ireland. CH currently supplies electronic-signature terminology, not a complete Swiss procedure guide. Missing local terms remain null. A regional data-protection authority is not guessed. GDPR access periods are not encoded as a universal 30-day deadline; [EDPB guidance](https://www.edpb.europa.eu/system/files/2023-04/edpb_guidelines_202201_data_subject_rights_access_v2_en.pdf) distinguishes the applicable one-month rule. An OTS proof is not automatically classified as a qualified timestamp under eIDAS.

Changing jurisdiction affects only the jurisdiction section and its source references. Changing language does not change the machine scene model. The section is a reference table, not a legal opinion or a procedural checklist.

## Release requirements still outstanding

The T7 forbidden-word lists and T13 custody/spec schema have not been supplied. Existing `custody.*` events receive source-linked generic descriptions; compatibility with an absent schema is not asserted. The narrative glossary is ready for reuse, but a shared T7/T14 interface cannot be tested without those specifications.

`python tools/check_narrative_texts.py --for-release` intentionally fails until T7 and T13 integration and native legal review of en/de/fr/uk/ru are documented. No human read-aloud test or ten-minute comprehension study has been performed. The feature is a review draft, not a release-complete implementation of those dependencies.

The requested sample includes six distinct scene kinds and collection on both sides of an interruption. Preserving that catalog produces seven chronological scenes, not five. The golden fixture records this explicitly instead of merging unrelated events to force an arbitrary count. Recorded stop/start pairs extend the gap scene to the next recorded start; their dates remain computer-clock claims, not independently proved downtime.

Tests cover the golden model, all 25 PDF/HTML outputs, unchanged scene counts across languages, plural edge cases, exact record references, independent DE/AT/CH sections, escaped markup, unverified claims, and the pre-existing signed legacy archive. Output narratives preserve hashes and mask contacts with the handover detectors; they are not a general anonymisation service for arbitrary names embedded in filenames or payload strings.
