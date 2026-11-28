# Private regression tests

Regression tests are kept out of the public source (see [Contributing](../.github/CONTRIBUTING.md#validation)).
This folder holds an encrypted copy of them together with the run that checked a revision,
so the result can be confirmed later without publishing the tests.

| | |
|---|---|
| Revision | `4e43cf89cdde6e14839897207b9e121408064ce7` (main) |
| Run | 26 November 2026, Linux x86_64 (Ubuntu 24.04), Python 3.12.3, Telethon 1.45.0 |
| Result | 293 passed, 1 skipped: the OpenTimestamps Keccak-256 test runs only where OpenSSL provides Keccak |
| Archive | `private-tests-4e43cf8.7z`, 7-Zip AES-256 with encrypted file names |

The archive holds the 44 test modules, the full pytest log of the run and a report of
the audit fixes and live tests (in Russian) with their coverage maps. The maintainer holds the password.

## What this receipt covers

The result above applies only to revision `4e43cf89cdde6e14839897207b9e121408064ce7`
(26 November 2026). Commits made after it, including the current `main`, are not covered by
this receipt: no run of these tests on a later revision is recorded here. Until a new archive
and result are added, the public check anyone can run on any revision is the synthetic
round trip, which exports a synthetic journal, verifies it with its fingerprint and refuses
changed, added and removed files and another fingerprint:

```sh
python tools/evidence_roundtrip.py
```

Check that the archive is the one listed here:

```sh
sha256sum -c SHA256SUMS.txt
```

With the password, run the tests on that revision in an environment with the project's
dependencies and pytest:

```sh
mkdir check
git archive 4e43cf89cdde6e14839897207b9e121408064ce7 | tar -x -C check
7z x -ocheck validation/private-tests-4e43cf8.7z tests
cd check && python -m pytest tests
```
