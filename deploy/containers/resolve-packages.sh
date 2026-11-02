#!/bin/sh
# Maintainer command: run inside the pinned Wolfi base; inspect results before updating locks.
set -eu
profile=${1:?Usage: resolve-packages.sh runtime|media|build [output-directory]}
case "$profile" in runtime|media|build) ;; *) echo "Unknown profile" >&2; exit 2 ;; esac
root=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
arch=$(apk --print-arch)
case "$arch" in x86_64|aarch64) ;; *) echo "Unsupported architecture" >&2; exit 2 ;; esac
out=${2:-/out}
mkdir -p "$out"
cache=$(mktemp -d)
trap 'rm -rf "$cache"' EXIT HUP INT TERM

# Repository signatures are checked by apk; no caller-supplied repository or key is used.
apk update
awk 'NF && $1 !~ /^#/ {print $1}' "$root/$profile.packages" > "$cache/roots"
apk add --no-cache $(cat "$cache/roots")
cp /lib/apk/db/installed "$out/$profile-$arch.installed"
cp "$root/$profile.packages" "$out/$profile-$arch.packages"
awk '/^P:/ {name=substr($0,3)} /^V:/ {print name "=" substr($0,3)}' \
    /lib/apk/db/installed | sort > "$out/$profile-$arch.versions"
mkdir "$cache/apks"
apk fetch --recursive --output "$cache/apks" $(cat "$out/$profile-$arch.versions")
for package in "$cache"/apks/*.apk; do apk verify "$package"; done
(
    cd "$cache/apks"
    sha256sum ./*.apk | sed 's|  ./|  |' | sort -k2
) > "$out/$profile-$arch.lock"
printf 'Resolved %s/%s: %s signed APKs\n' "$profile" "$arch" "$(wc -l < "$out/$profile-$arch.lock")"
