# Optional independent browser and AyuGram capture

[Project](../README.md) · [Installation and controls](../addons/capture/README.md)

The optional `tgwitness-capture` package provides independently operated recorders.
It does not change the main collector's defaults or existing signed formats.

- Separate control panels, data volumes, Ed25519 keys, sessions and exports.
- Capture disabled at every service start; video separately enabled and off by default.
- Chromium: selected-tab PNG, MHTML and rendered-text snapshots, change polling.
- AyuGram: consistent copies of a configured local SQLite database, including WAL.
- Signed event chain, downloadable checkpoints, separately operated witness receipts.
- Signed ZIP with originals and an HTML report; standalone verification CLI.

Use the `capture-browser` and `capture-ayugram` profiles in
[`addons/capture/compose.yaml`](../addons/capture/compose.yaml), or install the package
in its own Python environment. Ordinary `docker compose up` for TgWitness starts
neither recorder. Each recorder's own panel controls capture; there is no implicit
shared key, automatic account login or runtime dependency on the main panel.

The browser profile includes an optional Neko/Chromium environment and dedicated
upstream HTTP proxy forwarding. AyuGram's GUI, login and separate proxy/WARP route
must already be configured; its profile starts the database recorder only.

This is a preview with explicit coverage limits. See the installation guide for
the deployed isolation assumptions, unfinished video handling, key pinning,
independent checkpoints, storage limits and Linux acceptance procedure. Database
schema interpretation, WACZ/rrweb, native signed PDF and main-panel import are not
implemented in this version.
