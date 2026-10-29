![Straight to the answer — Accounts, capture, evidence and everyday operation.](../assets/presentation/wiki-faq.svg)

# Frequently asked questions

[Project](../../README.md) · [Documentation](../README.md) · [Wiki](Home.md) · [Support](../../SUPPORT.md)


## Does TgWitness recover messages deleted before it started?

No. A deletion notice may be recorded without prior content. History acquisition returns what is currently visible to the account, not a reconstruction of all earlier versions.

## Does a valid signature prove Telegram sent the message?

No. It verifies integrity relative to a signing key. An operator controlling the collector and key can fabricate a journal. Separately retained checkpoints and independent witnesses constrain later rewriting, but do not establish Telegram origin by themselves.


![Section divider](../assets/presentation/divider.svg)

## Is every Telegram event guaranteed to arrive?

No. Account permissions, connection failures, service behavior and process interruptions affect visibility. Rechecks and saved update state help recovery, but coverage reports and controlled delivery tests still matter.

## Can I use a bot token instead of a user account?

The collector uses a Telegram user authorization through MTProto. A bot token is used separately by the optional witness or Proof broadcaster.


![Section divider](../assets/presentation/divider.svg)

## Do I need my own API ID and API hash?

They are optional in the normal sign-in flow. The workspace can reuse saved/imported credentials or use the built-in pool. They identify an application; they do not provide account access without authorization.

## Can several people have separate access permissions?

Not in the current single-operator model. The panel token controls every workspace. A witness token has a separate, read-only capability; it is not a general user role.


![Section divider](../assets/presentation/divider.svg)

## Are messages and attachments encrypted on disk?

The vault encrypts sessions, credentials and signing secrets. The local journal and attachments are not encrypted by TgWitness. Use disk encryption and restrictive permissions. Exports can optionally be wrapped in a password-protected ZIP.

## Does Lock stop collection?

No. Lock clears browser access; the running collector continues. Pause observation stops collection. Closing the tab also leaves the process running.


![Section divider](../assets/presentation/divider.svg)

## Why can two accounts show different histories?

They may have different access, membership dates and visibility. Each workspace preserves its own observations and signing identity. Compare records with their original workspace attached.

## Does a public proxy failure switch me to a direct connection?

No automatic direct fallback is configured. Other network functions, such as witness HTTP requests or feed downloads, have separate route settings.


![Section divider](../assets/presentation/divider.svg)

## Are an evidence export and a backup interchangeable?

No. An evidence export deliberately excludes login and signing secrets. A service backup must preserve the entire stopped data directory and any external master key.

## Is a witness on my server independent?

It has a separate process and key, but the same operator still controls that server. Independent custody requires a separate operator or system outside that control.


![Section divider](../assets/presentation/divider.svg)

## Is Linux, macOS or Docker support already fully qualified?

Consult the current [verification record](../VERIFICATION.md). Implemented launchers and CI definitions are not evidence that every platform and live-service scenario has been executed.

## How do I report a problem or contribute?

Use [Support](../../SUPPORT.md) for help and bug reports, [Contributing](../../CONTRIBUTING.md) for development, and [Security](../../SECURITY.md) for vulnerabilities.
