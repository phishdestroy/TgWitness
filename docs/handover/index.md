# Prepare a sharing copy

Canonical page: https://phishdestroy.github.io/TgWitness/docs/handover/

Share the relevant observations while keeping the original workspace intact.

A handover is a separate signed extract. Choose the chats and people, reduce identities or text, and decide which files and team notes belong in the recipient's copy. Its manifest records the selection and the number of unchanged, minimized and omitted records.

## Prepare the recipient's extract

1. Open **Exports → Handover extract**. Write its purpose, choose the chats and optional UTC period, then select **Load people of the chosen chats** if you need named subjects.
2. Choose how to handle everyone else: pseudonyms, omit their messages, or show as recorded. Set message text and attachments independently; optionally mask phone numbers and email addresses.
3. Choose whether to include Case Board bookmarks and slices, or cards with comments. Investigator aliases can replace team names in this copy.
4. Select **Download handover extract**. Open the generated report and selected records locally, verify the archive, and inspect the copy before sending it.

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
| People | Keep selected subjects identifiable; pseudonymize or omit other participants as chosen. |
| Text | Include all text, only the selected people's and observing account's text, or omit message text and its text-bearing detail fields. |
| Files | Choose files of the selected people and observing account, all shown messages' files, or no files. |
| Case Board | Choose no board material, bookmarks and slices, or cards with team discussion. |

Review free-form text and file contents as well as identities: a pseudonym does not automatically remove every name written in a message or attachment. If a selected preserved file is unavailable, restore it or explicitly omit attachments before generating the extract.

## Keep the copy independently checkable

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Retain the original signed evidence archive and checkpoints separately. The handover records its own projection, so a recipient can check the delivered copy without receiving the entire workspace. [Report studio](https://phishdestroy.github.io/TgWitness/docs/reports/) supplies its reading design; [export verification](https://phishdestroy.github.io/TgWitness/docs/exports/) explains the trusted references.
