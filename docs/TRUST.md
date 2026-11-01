# Independent verification

[Русская версия](ru/TRUST.md) · [Security policy](../.github/SECURITY.md)

You can check artifact bytes against a public workflow and commit without access
to our infrastructure or trust in our self-hosted runner. This still requires
trust in the code you approve, GitHub's hosted runners and OIDC, Sigstore, and
your verification tools. An attestation is a signed claim, not proof that code
is harmless.

## Release source archive

Use a recent [GitHub CLI](https://cli.github.com/manual/gh_attestation_verify).
From a release produced after `provenance.yml` was introduced, download
`TgWitness-<ver>.zip`, its `.zip.sha256` file, `sbom.spdx.json`, and
`provenance.sigstore.json`. This ZIP is built with `tools/build_source.py` on
GitHub-hosted Ubuntu. It has a separate name to avoid the existing release
workflow's `*-source.zip` upload. Manual runs retain files in the
`attested-source` Actions artifact; they do not attach release assets.

Choose the release version and the full commit SHA you have independently
reviewed. Inspect `.github/workflows/provenance.yml`, its pinned actions and
`tools/build_source.py` at that commit. Do not copy an expected SHA from an
untrusted archive or assume a tag can never move. Then run:

```sh
VERSION='<ver>'
COMMIT='<reviewed-release-commit>'
gh attestation verify "TgWitness-${VERSION}.zip" \
  --repo phishdestroy/TgWitness \
  --signer-workflow phishdestroy/TgWitness/.github/workflows/provenance.yml \
  --signer-digest "$COMMIT" --source-digest "$COMMIT" \
  --source-ref "refs/tags/v${VERSION}" --deny-self-hosted-runners
```

Success verifies the file digest, SLSA provenance signature, repository,
workflow revision, source revision/ref and hosted runner identity. The workflow
path alone does **not** pin its revision. A checksum alone establishes no
builder identity. Missing or failed verification means this guarantee is absent.
Repeat the command with the `.zip.sha256` file to authenticate it as well.
For saved bundles, add `--bundle provenance.sigstore.json`; obtain trusted roots
in advance if verification must be offline.

## Sealed evidence

After decrypting the handoff described in [SEALED-ACTIONS](SEALED-ACTIONS.md),
verify `evidence.zip` against the actual caller fork (`OWNER/TgWitness`):

```sh
gh attestation verify evidence.zip --bundle attestation.jsonl \
  --repo OWNER/TgWitness \
  --signer-workflow phishdestroy/TgWitness/.github/workflows/sealed-collector.yml \
  --signer-digest eab5169e400ff3010d8853f42c8e430fe23ffe6b \
  --deny-self-hosted-runners
```

Review the [pinned collector workflow](https://github.com/phishdestroy/TgWitness/blob/eab5169e400ff3010d8853f42c8e430fe23ffe6b/.github/workflows/sealed-collector.yml),
which checks out collector commit `68fc80c3f4ca6764ffb178ce1a21f74dbd5dd6bf`.
For journal, attachment, collector-policy and capture-coverage checks, also run
the verifier from an independently trusted installation:

```sh
python -m tgwitness.sealed_verify evidence.zip --bundle attestation.jsonl --repo OWNER/TgWitness
```

## Public records and SBOM

- **Transparency:** open the Rekor link in the attestation step's public Actions
  summary. The downloaded bundle's `verificationMaterial.tlogEntries` records
  the log ID, index and inclusion proof; `gh attestation verify` verifies the
  signed bundle and log evidence. Use [Sigstore search](https://search.sigstore.dev/)
  to inspect the linked entry. A log entry timestamps a commitment, not Telegram
  messages. See [Rekor's role](https://docs.sigstore.dev/logging/overview/).
- **Repository checks:** open the [OpenSSF Scorecard report](https://securityscorecards.dev/viewer/?uri=github.com/phishdestroy/TgWitness).
  Check its date, commit and individual findings, not just its score. The
  workflow requests a scan every Monday at 04:32 UTC and on pushes to `main`;
  publication makes results available through OpenSSF's public dataset and
  signed Rekor records. This is automated analysis, not an independent human
  audit. A missing or stale report is not evidence of a successful check.
- **Workflow checks:** [workflow-audit.yml](../.github/workflows/workflow-audit.yml)
  runs zizmor on workflow changes and Mondays at 07:00 UTC. Read its
  `workflow-audit-sarif` artifact for injection, permission and pinning findings.
  Code-scanning findings are also uploaded; dashboard access may be restricted.
- **Dependencies:** `sbom.spdx.json` is a repository inventory, signed as a
  build output and bound to the ZIP by an SPDX attestation. Authenticate it
  using the release verification command above with `sbom.spdx.json` as the
  filename and the same commit/ref constraints, then scan locally:

  ```sh
  grype sbom:sbom.spdx.json
  ```

## What this does not guarantee

- Absence of application bugs, malicious behavior, vulnerable dependencies, or
  compromise of GitHub, Sigstore, approved actions or your verification tools.
- Authenticity, truth or completeness of Telegram content; recovery of unseen
  deletions; message timestamps; or secrecy from the capture host.
- Coverage of portable ZIPs, wheels, containers, GitHub's automatic source
  downloads, legacy `*-source.zip` files or releases without this attestation.
- Bit-for-bit reproducible rebuilds: the current ZIP builder records timestamps.
  The guarantee concerns the exact published and attested bytes.
- An exhaustive installed-runtime SBOM or a vulnerability-free result. The SBOM
  describes what the scanner detects in the source repository.
