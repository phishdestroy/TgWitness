# Evidence assurance review · 30 October 2026

This review uses disposable journals, keys, simulated cloud APIs and synthetic
transport responses. It does not operate a live Telegram account or deploy a server.
Its purpose is to identify what the verifier actually establishes and prevent a
successful integrity check from being presented as proof of source truth.

## Tested boundaries

| Scenario | Expected result / boundary |
| --- | --- |
| A replacement journal is signed using the original collector key | Its signatures can verify; comparison with a previously retained original checkpoint or witness prefix rejects the replacement. |
| A valid export grows beyond the last witnessed record | Ordinary verification reports the exact unwitnessed tail. `--require-witness` rejects the handover. |
| A witness includes checkpoints later than the supplied export | They are reported separately and do not extend that export's verified witness period. |
| A requested channel file contains none of the claimed signed posts | Strict witness handover fails. |
| A signed archive contains no process-start measurement | Cloud host-binding verification fails, even when its signatures are valid. |
| Host measurements or the expected collector identity are absent | Missing measurements produce an incomplete result; no expected key produces failure. Neither becomes a successful host-binding check. |
| An unchanged collector reports modified bootstrap data | Installer binding fails against the retained original deployment record. |
| A compromised collector reports the original bootstrap measurements | Configuration comparisons can pass. The report explicitly identifies these measurements as self-reported and does not establish runtime attestation or key non-exportability. |
| A redirected endpoint advertises an unknown Telegram server key | The pinned Telethon dependency refuses the authorization handshake. |
| A redirected endpoint supplies arbitrary encrypted message bytes | Telethon refuses the message authentication check. |
| Someone edits the date in a Telegram Desktop JSON export | The witness token can still match. Publication-time verification is explicitly not performed. |

These scenarios are covered by `tests/test_evidence_assurance.py`,
`tests/test_telegram_server_auth.py` and the cloud bootstrap regression in
`tests/test_cloud.py`. Existing witness, checkpoint, export and assurance tests
remain part of the validation run.

## Handover procedure

1. Retain the collector and witness key fingerprints through independent channels.
2. Preserve the original evidence ZIP and witness journal separately. Record the
   collection scope, interruptions, software version and transfer history.
3. Require the exact export boundary to match the pinned witness when handing over
   a fully witnessed archive; use the procedure in [WITNESS.md](../WITNESS.md#require-a-witnessed-export-boundary).
4. Keep missing observations, disputed records, failures and unwitnessed intervals
   visible. A successful signature check does not turn an observation into a factual conclusion.
5. Treat dates in supplied files as metadata unless separately authenticated.
   Use independently verified timestamp evidence when trusted time is required.

Separate custody of integrity values follows the preservation approach described
in [NIST IR 8387](https://doi.org/10.6028/NIST.IR.8387). This review does not certify
legal admissibility, completeness of Telegram delivery or the identity of a human sender.

## Remaining architectural boundary

The cloud deployment mode does not independently attest the code running inside
the host. A malicious initial installer could change the collector, access its
secrets or cause it to present fabricated records before an independent witness
first observes them. Provider logs and a signed self-report do not close this gap.

The witness fixes the journal state it observes; it does not fetch each original
message from Telegram independently. A witness on the same host or controlled by
the same operator does not establish independent custody merely by having another key.

Closing the bootstrap boundary requires a separately trusted deployment process
or a reviewed attested execution design. Neither is added by this patch. Key
rotation, container encryption and network restrictions may reduce particular risks
but do not independently establish which code generated the first records.

The proposed `/etc/hosts`-only counterfeit Telegram scenario does not demonstrate
that boundary: the collector uses MTProto server authentication, and a hosts entry
does not implement IP-to-IP packet redirection. Changing the client or its session
secrets is a different prerequisite from redirecting an unchanged client's network path.

Protocol references: [Telegram server authentication](https://core.telegram.org/mtproto/auth_key)
and [MTProto message checks](https://core.telegram.org/mtproto/description).
