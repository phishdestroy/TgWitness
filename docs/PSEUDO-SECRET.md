[TgWitness](../README.md) / [Documentation](README.md)

# Secret Chats: installation and recording

The published application includes the Secret Chat backend, collector integration,
API routes and **Pseudo-secret** interface. The protocol library is a separate module:
open **Pseudo-secret** and press **Install and turn on**. Automatic incoming acceptance
stays off until you turn it on.

## Protocol module

| | |
| --- | --- |
| Module | `kiaro-telethon-secret-chat` 0.2.0 |
| Author | KiaroSama |
| License | GPL-3.0-or-later; its `LICENSE` and `NOTICE` stay inside the saved archive |
| Source | [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat) at commit `d87bf037b90060383c7b704d8a06ebb98c621c6f` |
| Check | SHA-256 `c80feb9b5bc28201677c140d20930fbd730d7efdebb8ca789a19040c3f00ce5c` over the list of package files and their own SHA-256 values |

**Install and turn on** is available to the main administrator. TgWitness downloads the
source archive of that commit from GitHub through the workspace's route for requests
outside Telegram, compares every file of the package with the value fixed in the
TgWitness release, saves the archive as `modules/telethon-secret-chat-<commit>.zip` in
the data directory and loads the code from memory. No restart is needed. The check runs
again at every start; an archive that differs is not loaded and the page says so.
A changed, missing or added package file fails the check.

The module is a separate work under its own license. TgWitness does not ship it: each
installation downloads it from its author's repository. **Details** on the page shows
the loaded module, its author, license, commit and SHA-256.

A host without access to GitHub can install the same commit into the Python
environment instead; the panel then uses that copy:

```sh
python -m pip install ".[secret-chats]"
```

TgWitness becomes an endpoint for the chats it creates or accepts. It records
messages, available attachments, timer changes and deletion notices in the signed
journal. Previously saved content remains available after a later deletion notice.

## Package availability

On 8 November 2026, the published installer package was checked at source
[`b35f8e18f3d1`](https://github.com/phishdestroy/TgWitness/commit/b35f8e18f3d13c329af12e0036f50e0c8f340a2c),
release `b35f8e18f3d1-1ff85ec98bb2`, version 0.9.1 preview.
The [immutable wheel](https://get.destroy.tools/releases/b35f8e18f3d1-1ff85ec98bb2/tgwitness-0.9.1-py3-none-any.whl)
and its dependency lock passed SHA-256 and RSA release-signature verification.
The packaged backend and interface matched that source revision byte for byte.
The package also contains the API registration and collector hooks.

That package did not contain the protocol library, and it is not in the dependency
lock. The `secret-chats` extra in [pyproject.toml](../pyproject.toml) pins the same
commit as the panel button.

This package inspection establishes which files and dependency declarations ship.
The [validation record](VERIFICATION.md) identifies the separate runtime checks.
The earlier 6 November guide described a development snapshot; it no longer
describes the package above.

## Use the interface

Open **Pseudo-secret**, install the module if the page offers it, turn it on for the account and connect it.
Incoming requests wait for acceptance unless automatic acceptance is enabled.
Starting, accepting, sending and closing use the account's interaction permissions
and read-only protection.

| Action | Preserved result |
| --- | --- |
| Start a chat by username or user ID | Outgoing request; the peer accepts it on their device. |
| Accept a request | TgWitness becomes the receiving endpoint. |
| Send or receive a message | `secret_chat.message` with its direction, content and supplied timer. |
| Receive a file | Decrypted bytes stored by SHA-256 and a `secret_chat.file` receipt; included in the evidence export. |
| Receive a timer or deletion notice | A separate action record alongside retained messages and files. |
| Review the chat | Conversation, file receipts, notices and key visualization. |

Existing Secret Chats on another device retain their device-specific keys. An
imported cloud session does not transfer those keys. Secret-chat key material and
counters use the workspace vault; preserved messages and decrypted files use the
normal workspace storage protections.

## Persistence and interaction controls

The integrated implementation uses durable journal lookup for duplicate detection,
keeps attachment jobs pending after a failed download, and routes closing through
the same interaction guard as other remote actions. These replace the three paths
reported in the historical 6 November development-snapshot audit.

Decrypted messages whose journal write fails are held in the vault for retry.
Attachment size and free-disk checks defer downloads while keeping their jobs.
The module reuses the account's existing connection. Read and typing notices are sent
only as chosen under
[What the other side sees](INVESTIGATION-MODE.md#what-the-other-side-sees); screenshot
notifications are never sent. See [secret_chats.py](../tgwitness/secret_chats.py),
[API routes](../tgwitness/api/secret_chats.py) and
[access policy](../tgwitness/access.py).

The [historical audit](../website/validation/audit/REPORT.md) retains its original
snapshot findings. Current availability and implementation should be read from
the package revision above and the [current capabilities](STATUS.md).

## Interface demonstration

The website scenario uses fictional requests, messages and files to demonstrate
the panel workflow. It is an interface example; protocol and acquisition checks
have their own dated results in the validation record.
