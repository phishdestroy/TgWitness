# Chromium sandbox policy

`official-seccomp.json` is the unmodified profile distributed with Playwright 1.64.1．
It keeps a deny-by-default syscall policy and permits the user namespaces needed
by Chromium's own sandbox，without adding host administration capabilities．

Source：<https://github.com/microsoft/playwright/blob/v1.64.1/utils/docker/seccomp_profile.json>

SHA-256：`cc3e61cabda6bbc1e53e54d27ba4d55a9d3be829b6dd1a596f4a7b31b1cc7849`

Copyright Microsoft Corporation，licensed under Apache License 2．0，see
[PLAYWRIGHT-LICENSE.txt](PLAYWRIGHT-LICENSE.txt)．
