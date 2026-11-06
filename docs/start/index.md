# Start in minutes

Canonical page: https://phishdestroy.github.io/TgWitness/docs/start/

Poke around the demo first, then connect your own account.

## Look around without an account

Get the project, have **Python 3.11 or later**, run the demo. The launcher sets up everything else.

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

A workspace with made-up messages opens in the browser. Open a chat, compare an edit, look at an export. No Telegram involved.

![TgWitness conversation view with sample messages](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

A sample workspace. Your own journal starts separately.

## Start your own workspace

Close the demo, then:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Open the address the launcher shows and paste the **panel access token** from the file it names. That's for TgWitness, not Telegram.

## Capture your first message

1. [Connect a dedicated Telegram account.](https://phishdestroy.github.io/TgWitness/docs/accounts/)
2. Pick a group or channel and start observation.
3. Send a message in your test group and watch it appear in the journal.

For a server installation, follow [Keep it running](https://phishdestroy.github.io/TgWitness/docs/server/).
