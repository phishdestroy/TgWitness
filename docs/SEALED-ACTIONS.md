# Sealed capture from a personal fork

**Unreleased preview.** A fork launches a pinned reusable workflow from
`phishdestroy/TgWitness`. The workflow reads one selected chat using a newly
created Telegram session, attests the resulting evidence ZIP, and uploads only
recipient-encrypted handoffs. The normal administration panel is not exposed.

This is an ordinary GitHub-hosted runner, not confidential hardware. GitHub,
the approved collector and dependencies, the helper page, the browser, and the
HTTPS tunnel remain in the trust boundary. A GitHub attestation binds bytes to
an approved workflow; it does not give the messages a Telegram signature,
establish historical completeness, or certify that nobody accessed the host.

## User flow

1. Obtain a trusted TgWitness checkout. Open `website/sealed.html` locally in a
   modern browser, or use the official site's `/TgWitness/sealed.html` page once
   that version is published. The helper makes no network requests for key or
   file processing. It is available in English and Russian.
2. Generate a key and save **sealed-key.json**. This is the only private
   decryption key. Copy the separate public **recipient** value. Losing the
   private key loses access to both the connection and the archive.
3. Fork TgWitness, enable Actions in the fork, and run **Sealed chat capture**.
   Paste the public recipient and choose 30, 60, or 120 minutes. Never put a
   phone number, login code, Telegram password, private key, or session in
   workflow inputs, commits, issues, or logs.
4. During the run, download **sealed-connection** from Artifacts and unzip it.
   Load `connection.tgwsealed` in the helper, using the saved private key.
   The resulting link contains a random access secret in its URL fragment.
   Keep this link private. The panel removes the fragment and keeps the secret
   in this tab's session storage; it is not placed in HTTP access logs.
5. Enter your Telegram `api_id` and `api_hash`, then authorize by QR or phone
   code and, if required, Telegram's two-step verification password. Use
   [my.telegram.org/apps](https://my.telegram.org/apps) for your API credentials.
   Existing session files cannot be imported into this mode.
6. Load the dialogs and select one chat. Capture starts immediately. The
   selected source cannot be changed after starting. You can resume a paused
   history read, finish with the data already collected, or cancel without
   producing an archive. History reading and attachment downloading finish
   separately. Deadline expiry after starting produces an explicitly partial
   archive; expiry before starting produces no archive.
7. Wait for **sealed-result**, download and unzip it, and decrypt
   `delivery.tgwsealed` in the helper. You receive `delivery.zip`, containing
   `evidence.zip`, `attestation.jsonl`, and instructions. Browser decryption is
   limited to 256 MiB; larger packages use the streaming local command below.
8. End the temporary session in Telegram Settings → Devices if revocation was
   not confirmed or the runner was killed. Normal completion attempts logout;
   network failures and forced runner termination prevent an absolute guarantee.

The repository must contain the published pinned source and reusable-workflow
commits. A local branch alone cannot be invoked by another GitHub repository.

## Local decryption and verification

Use tools from an independently trusted installation, not executable files
supplied by an unknown evidence archive:

```sh
python -m tgwitness.sealed_crypto decrypt delivery.tgwsealed --key sealed-key.json --out delivery.zip
# Unzip delivery.zip using your archive manager, then:
python -m tgwitness.sealed_verify evidence.zip --bundle attestation.jsonl --repo OWNER/TgWitness
```

Python 3.11+, the project's dependencies, and a recent GitHub CLI supporting
`--signer-digest` and `--deny-self-hosted-runners` are required. A CLI key generator
is also available: `python -m tgwitness.sealed_crypto keygen sealed-key.json`.

The verifier uses `tgwitness/sealed_policy.json` from the trusted installation.
It checks the caller repository, upstream signer workflow, approved signer
commit, hosted runner requirement, complete ZIP digest, internal journal and
attachment integrity, fresh account-key origin, and expected collector commit.
It displays history and media outcomes instead of implying all data was saved.
An empty approved-release list fails closed. Updating the policy is an explicit
trust decision; never accept an archive's own proposed policy automatically.

For offline use, obtain trusted roots ahead of time from a trusted environment:

```sh
gh attestation trusted-root > trusted_root.jsonl
python -m tgwitness.sealed_verify evidence.zip --bundle attestation.jsonl --repo OWNER/TgWitness --trusted-root trusted_root.jsonl
```

The timestamp of the attestation concerns the archive's commitment. It does not
authenticate message timestamps or the collector's wall clock. See
[GitHub's verification options](https://cli.github.com/manual/gh_attestation_verify).

## How the fork is kept outside the capture process

The caller contains a job-level reference to the upstream reusable workflow at
a full commit SHA. That workflow explicitly checks out **the upstream repository
at a fixed collector SHA**. A default `actions/checkout` in a reusable workflow
would check out the caller and is intentionally not used.

The workflow does not restore caller caches, consume caller artifacts, execute
caller files, or accept source/image URLs, shell commands, prepared ZIP files,
or hashes to sign. It accepts a bounded public recipient and session duration.
Actions, the Python base image, and cloudflared are pinned by immutable digests;
Python dependencies use the existing hash-locked requirements. The image is
built from the trusted source without a cache.

The collector runs as a non-root user with a read-only image, dropped Linux
capabilities, resource limits, and no Docker socket or GitHub-token environment.
Its only mounts are fresh configuration, workspace, and output directories.
The restricted FastAPI application exposes login, dialogs, one-chat collection,
status, resume, finish, and cancellation. There is no plaintext download route,
general administration route, import route, or signing endpoint.

The supervisor stops the network-facing containers before the attest action
reads the final fixed `evidence.zip`. The packaging container has no network.
The upload steps name only `connection.tgwsealed` and `delivery.tgwsealed`;
neither plaintext evidence nor Telegram credentials are uploaded as artifacts.
Cleanup removes the private directories and containers, with no claim of
physical disk erasure. Artifact retention is one day; download before expiry.

A fork owner can replace the caller or create a different signed file. The
strict verifier must reject the resulting **different signer workflow/digest**.
This construction still depends on the absence of exploitable bugs in approved
code and on the integrity of GitHub's runner and signing infrastructure.

## Cryptographic handoff

Each recipient key is RSA-3072 (RSA-4096 imports also accepted), exponent 65537.
Each envelope has a fresh random AES-256 key and 96-bit nonce. RSA-OAEP with
SHA-256/MGF1-SHA256 wraps the AES key. AES-GCM with a 128-bit tag authenticates
the complete prefix and payload. The public recipient is DER SPKI in base64;
the private key file contains DER PKCS8 in base64.

Envelope bytes are `TGWSEAL1\n`, a big-endian uint32 JSON-header length, the
header, ciphertext, and a 16-byte GCM tag. The header has exactly `algorithm`,
`key`, and `nonce`; algorithm is `RSA-OAEP-256+A256GCM`. The complete prefix
through the header is GCM additional authenticated data. Header size is bounded
at 8192 bytes. The CLI streams payloads up to 8 GiB and authenticates before
installing the requested output; it refuses overwriting an existing destination.
This is a project-specific envelope around standard cryptographic primitives,
not an independently audited encryption format.

The original evidence bytes are attested **before** placing the evidence and
attestation in the encrypted outer package. This avoids a circular dependency
between the archive's hash and a certificate included inside that same archive.
For public repositories, attestation metadata (repository, workflow, commit,
artifact name and digest) is public. Never put chat names in public metadata.

## Limits and validation

This mode uses the existing signed journal, resumable history reader, and media
queue. It collects one visible chat, not Secret Chats, deleted history from
before collection, or all account dialogs. Dialog enumeration is capped at
20,000. Existing attachment type/size limits and a 4 GiB export limit apply.
Live updates for the selected chat can also be observed during the read; the
history is not an atomic Telegram snapshot. Generated screenshots and screen
recordings are not part of this mode.

Tests cover synthetic fresh login, scope isolation, media, cancellation,
partial deadline completion, failed logout, forbidden API paths and fields,
preloaded workspace rejection, wrong-key and tamper rejection, required verifier
flags, and browser/Python encryption interoperability. The browser acceptance
test uses a plainly labelled mock attestation; it is not a real Sigstore test.
Real hosted-runner, Docker, GitHub attestation, and live Telegram acceptance
must be reported separately from local synthetic checks.

[GitHub Actions terms](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features#actions)
restrict use of hosted runners to the software project's lifecycle. A fork does
not remove these restrictions; this preview must not be marketed as unrestricted
free production hosting. [Cloudflare Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/)
are also intended for testing and development. The helper/workflows are suitable
for evaluating this feature; production service eligibility remains a separate
deployment requirement.

## Maintainer release sequence

1. Commit and review the collector, supervisor, container definition and tests.
2. Pin that collector commit in `sealed-collector.yml`, then commit/review the
   reusable workflow. Never silently derive the checkout from the caller SHA.
3. Pin the reusable workflow commit in `sealed-witness.yml` and add its
   workflow/collector SHA pair to `sealed_policy.json` in a trusted release.
4. Publish all referenced commits and the helper, then test an independent fork
   and the real GitHub certificate. Do not squash away commits referenced by
   these pins unless the references are regenerated and published again.

See [reusable workflows and attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/increase-security-rating)
for the distinction between the caller repository and the upstream signer.
