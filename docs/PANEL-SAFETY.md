# Panel safeguards

[Documentation](README.md) · [Accounts](ACCOUNTS.md) · [Storage](STORAGE.md)

The panel checks the account context before acting. Imported files are inspected
before Telegram sign-in. Chat actions are off until enabled for the current chat.
These controls reduce accidental actions; the server still checks access permissions.

## File check

```text
!  No session found
   Only application settings. Add .session / TData,
   or sign in by phone or QR.

   [Choose files]  [Phone]  [QR]       [Connect — disabled]
```

```text
✓  Session found — Telegram will validate it on connect
   Device       Synthetic desktop
   Platform     Windows 11
   Version      5.13.1 x64
   Language     en

   [Connect]   or, when another account is connected:
   [Create workspace and connect]
```

The green result means a usable session was decoded, not that Telegram has
accepted it. Conflicting application IDs, damaged ZIPs and incomplete credentials
have separate errors. A settings-only JSON never produces a success message.

Additional workspaces can be deleted after typing their name. Their journal,
attachments and signing key are deleted. The main workspace owns installation
settings and cannot be deleted through this control; the panel explains this.

## Account context

```text
Workspace [Case A ▾]   / Exports       [avatar] @account_a

! You are viewing @account_a, but @account_b is selected.
  Actions are paused until the account is confirmed.
  Account in this link: @account_a.
  [Switch to the account in this link]
```

The URL determines the workspace. Loaded server status carries its workspace ID;
late responses from an earlier selection are ignored. The mismatch notice blocks
content interaction and workspace API requests until resolved. Export confirmation
names the account, and checks the context again after confirmation.

## Read-only chat

```text
[✓] Read only              [✓] Mask secrets
Sending and bot actions are hidden.

Password: B4X••••• [Show]
```

Enabling chat actions exposes the composer and bot buttons. Sending and pressing
a bot button require account-named confirmation. Remembered consent lasts ten
minutes and is cleared when the chat or workspace changes. Explicitly opening or
joining a Telegram link has its own confirmation and does not enable chat actions.

Secret detection is heuristic: it recognizes common password, token, key, OTP,
session and payment-card patterns. It cannot identify every secret. List previews
always mask detected values. Revealing a value, or disabling masking, records
metadata in the journal before display; it does not journal the secret again.
Captured bytes, hashes and signed exports are unchanged. Use a disclosure export
when the recipient should receive less information.

## Downloads

File-picker denial and `createWritable()` failure fall back to the browser's
ordinary download. If a streamed write fails, a prepared journal export can be
retried through a short-lived, single-use HttpOnly download cookie. Tokens are not
put in URLs. Authorization is checked again after hashing the retained file.

Prepared journal exports include the file's size, SHA-256 and **Download again**.
The cache retains at most 20 entries within 2 GiB, plus the latest file. Existing
account-export jobs retain their own download list. Preparation or dispatch to a
browser does not establish receipt. Check the browser's Downloads list.

## English and Russian copy

| English | Русский |
| --- | --- |
| No session found | Сессия не найдена |
| No session — only application settings. Add a .session or TData file, or sign in by phone or QR. | Нет сессии — только настройки приложения. Добавьте .session или TData либо войдите по телефону или QR. |
| Export records from {account}? | Выгрузить записи аккаунта {account}? |
| Confirm the workspace above before continuing. | Сначала подтвердите пространство в плашке выше. |
| Download again | Скачать снова |
| No data | Нет данных |
| Telegram does not report who deleted the message | Кто удалил — Telegram не сообщает |
| Technical sequence (seq) | Технический номер (seq) |

## Checks and visual artifacts

Run from the repository with the `dev` dependencies and Playwright Chromium:

```sh
python tools/check_import_preflight.py
python tools/check_chat_safety_browser.py
python tools/check_workspace_downloads_browser.py
python tools/check_prepared_export_access.py
python tools/check_services_browser.py
python tools/check_storage_services.py
node tools/check_privacy_js.cjs
```

The browser checks generate real desktop/mobile screenshots under
`test-results/import-preflight/`, `test-results/chat-safety/`,
`build/ux-review/account-safety/` and `build/ux-review/services/`. These are local
review artifacts, excluded from source archives. Telegram clients and remote
storage in these checks are synthetic; they do not log in to real accounts or
send messages to external services.
