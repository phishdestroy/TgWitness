# Telegram Proxies: MTProxy, SOCKS5 & Routing

Canonical page: https://phishdestroy.github.io/TgWitness/docs/proxies/

Keep the account online, and decide yourself whether it may ever show your server's IP.

## Choose the IP mode first

01**Hide the address**

Proxy only. If none works, it waits.

02**Direct as a last resort**

Goes direct after a delay, back to a proxy once one works.

03**Server behind a tunnel or VPN**

Direct is fine. It doesn't set up or check the VPN for you.

The route chooses the connection. The IP mode determines whether a direct connection is permitted.

## Let the pool maintain the route

1. **Account → Settings → Connection settings**.
2. Pick the IP mode and **Automatic MTProxy**, or a fixed route.
3. Save, **Test Telegram connection** (works before sign-in too).
4. Start collecting and send yourself a test message.

New workspaces start on automatic MTProxy with **Hide the address**. The pool pulls four public lists, checks servers, keeps the good ones and swaps out dead ones.

## Use your own proxy

SOCKS5, HTTP CONNECT, a Telegram proxy link or an operator catalog. Pause observation before switching. Fake TLS secrets (`ee`…) don't work.

**Rotation, sharing and retry settings**

**Parameters → Automatic MTProxy**: failure thresholds, cooldowns, rotation, accounts per proxy. Limit 1 means an account waits rather than share. Different proxies can still share an exit IP.

## Separate Telegram from external requests

MTProxy only carries Telegram. Timestamps, notifications, copies and code checks go through a separate SOCKS5/HTTP proxy, the account's SOCKS5/HTTP route, or direct if the mode allows. Or turn them off.

`TGWITNESS_PROXY_FEED_PROXY` sets the route for list downloads. The [witness](https://phishdestroy.github.io/TgWitness/docs/witness/) has its own settings. None of this touches your browser or system network.

More: [modes and defaults](https://phishdestroy.github.io/TgWitness/docs/reference/connection/#ip-modes), [who may change routes](https://phishdestroy.github.io/TgWitness/docs/access/).
