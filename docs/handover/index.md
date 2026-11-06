# Share Telegram Evidence with Limited Disclosure

Canonical page: https://phishdestroy.github.io/TgWitness/docs/handover/

Share only what's needed, the original stays untouched.

A handover is a separate signed extract: pick chats and people, hide identities or text, choose files and team notes. The manifest records what was kept, trimmed and left out.

## Prepare the recipient's extract

1. **Exports → Handover extract**: write the purpose, pick chats and a period, **Load people of the chosen chats** if you need named people.
2. Everyone else: pseudonyms, left out, or as recorded. Text and files are separate switches; phones and emails can be masked.
3. Case Board: nothing, bookmarks and slices, or cards with comments. Team names can be swapped for aliases.
4. **Download handover extract**, open it, verify it, look through it before sending.

### One original, a deliberate sharing copy

Synthetic example · identity illustration only

1. **Select.** Include the case chat and identify the person the extract is about.
2. **Minimize.** Choose how another participant appears in the sharing copy.
3. **Inspect.** Open the generated archive's report and records before sending it.
4. **Share.** Deliver the checked copy and communicate its trusted fingerprint separately.

#### Original observation

Nora · user 71002

“I received the revised link.”

The source journal keeps this saved observation.

#### Recipient's copy

Show as recorded: Nora · user 71002 · “I received the revised link.”

Pseudonym: P01 · “I received the revised link.”

Omit: this participant's message is left out of the copy.

#### Inspect the actual files

Read report.html and records.jsonl.

Check identities, text, attachments and optional team comments.

#### Signed extract

Selection + file hashes + signed manifest

A separate package linked to its source journal boundary

## Use the controls together

| Control | Effect on the copy |
| --- | --- |
| People | Selected people stay named; others get pseudonyms or are left out. |
| Text | All text, only the selected people's and your account's, or none. |
| Files | Files of the selected people and your account, all shown files, or none. |
| Case Board | Nothing, bookmarks and slices, or cards with discussion. |

Read the text and files too: a pseudonym doesn't remove names written inside a message or attachment. If a selected file is missing, restore it or leave attachments out.

## Keep the copy independently checkable

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Keep the original archive and checkpoints yourself. The recipient can verify their copy without getting the whole workspace. Design: [Report studio](https://phishdestroy.github.io/TgWitness/docs/reports/). Trusted references: [export verification](https://phishdestroy.github.io/TgWitness/docs/exports/).
