# Choose a proxy

Canonical page: https://phishdestroy.github.io/TgWitness/docs/proxies/

Keep the account connected. Decide explicitly when its route may use the server's address.

## Choose the IP mode first

01**Hide IP**

Use a proxy. When none works, wait without a direct Telegram connection.

02**Allow fallback**

Permit Direct after the configured delay; return to a working proxy when one answers.

03**Tunnel / VPN**

Allow direct routes through the host's network. This option does not install or verify a VPN.

The route chooses the connection. The IP mode determines whether a direct connection is permitted.

## Let the pool maintain the route

1. Open **Account → Settings → Connection settings**.
2. Choose the IP mode and **Automatic MTProxy**, or enter a fixed route.
3. Save and run **Test Telegram connection**. It also works before sign-in.
4. After starting collection, check that a controlled message reaches the journal.

New workspaces use automatic MTProxy with Hide IP behavior. The pool combines four public sources, probes entries, retains working routes and replaces failing proxies. Failed downloads retain the previous snapshots.

## Use your own proxy

Enter SOCKS5 or HTTP CONNECT details, paste a supported Telegram proxy link, or provide an operator catalog. Pause observation before changing an active route. Fake TLS MTProxy secrets beginning with `ee` remain unsupported.

**Rotation, sharing and retry settings**

Under **Parameters → Automatic MTProxy**, set failure thresholds, cooldowns, planned rotation and accounts per proxy. A sharing limit of one makes an account wait when no exclusive entry is available. List refresh and probe intervals follow the main workspace's values. Separate proxies do not guarantee separate exit IPs.

## Separate Telegram from external requests

MTProxy carries Telegram traffic only. Timestamps, notifications, copies and source checks use a separate SOCKS5/HTTP proxy, the account's SOCKS5/HTTP route, or Direct where the IP mode permits it. Those external requests can be disabled.

An explicit `TGWITNESS_PROXY_FEED_PROXY` configures the feed downloader's route. The [independent witness](https://phishdestroy.github.io/TgWitness/docs/witness/) keeps its own settings. These controls do not install a system VPN or route browser traffic.

See [all modes, defaults and source lists](https://phishdestroy.github.io/TgWitness/docs/reference/connection/#ip-modes), or [choose who may change an account's route](https://phishdestroy.github.io/TgWitness/docs/access/).
