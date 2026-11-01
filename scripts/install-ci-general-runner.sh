#!/usr/bin/env bash
# Add one unprivileged runner to an existing TgWitness Ubuntu CI host.
# Registration and service startup are separate, after capacity/isolation checks.
set -euo pipefail
umask 077

if [[ ${EUID} -ne 0 ]]; then
  echo 'Run as root on the existing dedicated CI host.' >&2
  exit 1
fi
. /etc/os-release
if [[ ${ID} != ubuntu || ${VERSION_ID} != 24.04 || $(uname -m) != x86_64 ]]; then
  echo 'This installer requires Ubuntu 24.04 x86_64.' >&2
  exit 1
fi
if [[ ! -f /opt/actions-runner/.runner ]]; then
  echo 'Prepare and register the primary runner before adding capacity.' >&2
  exit 1
fi

runner_user=tgwitness-ci-general
runner_root=/opt/actions-runner-general
runner_cache=/opt/hostedtoolcache-general
runner_version=2.338.2
runner_sha256=baebf204307bac6193480852732f0aba2ae97b6c5597c244f4d5558390147c40

# Two browser workers in each of two jobs need headroom. Do not infer capacity
# from the runner process being idle; inspect actual load before enabling routing.
memory_kib=$(awk '/^MemTotal:/ {print $2}' /proc/meminfo)
free_kib=$(df --output=avail -k /opt | tail -n 1 | tr -d ' ')
if (( $(nproc) < 4 || memory_kib < 7 * 1024 * 1024 || free_kib < 15 * 1024 * 1024 )); then
  echo 'At least 4 CPUs, 7 GiB total RAM and 15 GiB free /opt space are required.' >&2
  exit 1
fi

if ! id "$runner_user" >/dev/null 2>&1; then
  useradd --create-home --user-group --shell /bin/bash "$runner_user"
fi
# Never add this account to docker, sudo or another privileged group. Refuse an
# existing account that has been repurposed; do not silently remove its access.
if [[ $(id -Gn "$runner_user") != "$runner_user" ]]; then
  echo 'The general runner account must belong only to its own group.' >&2
  exit 1
fi
if sudo -n -l -U "$runner_user" >/dev/null 2>&1; then
  echo 'The general runner account has sudo access; review it before continuing.' >&2
  exit 1
fi
if runuser -u "$runner_user" -- test -w /var/run/docker.sock; then
  echo 'The general runner account can write the Docker socket.' >&2
  exit 1
fi
if runuser -u "$runner_user" -- test -r /opt/actions-runner/.credentials \
    || runuser -u "$runner_user" -- test -w /opt/actions-runner; then
  echo 'Restrict the primary runner directory to its owner before adding a service.' >&2
  exit 1
fi
for directory in "$runner_root" "$runner_cache"; do
  if [[ -L "$directory" ]]; then
    echo 'Refusing a symlink in a runner installation path.' >&2
    exit 1
  fi
  install -d -m 700 -o "$runner_user" -g "$runner_user" "$directory"
done

if [[ ! -f "$runner_root/config.sh" ]]; then
  archive=$(mktemp /tmp/tgwitness-general-runner.XXXXXX.tar.gz)
  trap 'rm -f -- "$archive"' EXIT
  curl --fail --location --retry 3 \
    "https://github.com/actions/runner/releases/download/v${runner_version}/actions-runner-linux-x64-${runner_version}.tar.gz" \
    --output "$archive"
  printf '%s  %s\n' "$runner_sha256" "$archive" | sha256sum --check --status
  tar -xzf "$archive" -C "$runner_root"
  chown -R "$runner_user:$runner_user" "$runner_root"
fi

# The primary host installer already provides Python and browser OS libraries.
# Keep tool installations, pip/Playwright caches, workspaces and credentials
# separate. No Docker daemon or system-wide package installation is needed here.
if [[ ! -f "$runner_root/.env" ]]; then
  printf 'AGENT_TOOLSDIRECTORY=%s\n' "$runner_cache" > "$runner_root/.env"
  chown "$runner_user:$runner_user" "$runner_root/.env"
  chmod 600 "$runner_root/.env"
elif ! grep -Fxq "AGENT_TOOLSDIRECTORY=$runner_cache" "$runner_root/.env"; then
  echo 'The existing runner has a different tool cache; refusing to overwrite it.' >&2
  exit 1
fi

echo 'General runner prepared without Docker or sudo access.'
echo 'Register it with only the tgwitness-general custom label; do not start it yet.'
echo 'Follow docs/internal/CI-PARALLELISM.md for service limits and activation.'
