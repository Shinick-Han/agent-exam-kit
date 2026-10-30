#!/bin/sh
# agent-exam-kit 0.3.0: POSIX shell only; no Python/Node/jq runtime.
set -eu
root=${AGENT_EXAM_KIT_HOME:-"$HOME/.agent-exam-kit"}
skills=${AGENT_EXAM_KIT_SKILLS:-"$HOME/.agents/skills"}
cache=
only=all
dry=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --root|--skills-dir|--cache)
      [ "$#" -ge 2 ] || { echo "Missing value: $1" >&2; exit 1; }
      case "$1" in --root) root=$2;; --skills-dir) skills=$2;; --cache) cache=$2;; esac
      shift 2;;
    --skills-only) only=skills; shift;;
    --herdr-only) only=herdr; shift;;
    --dry-run) dry=1; shift;;
    *) echo "Unknown option: $1" >&2; exit 1;;
  esac
done
case "$root" in ''|/) echo 'Choose a user installation directory.' >&2; exit 1;; esac
for tool in curl tar gzip mktemp uname mkdir mv chmod cmp rm cp cut; do
  command -v "$tool" >/dev/null 2>&1 || { echo "Missing command: $tool" >&2; exit 1; }
done
if command -v sha256sum >/dev/null 2>&1; then
  checksum() { sha256sum "$1" | cut -d ' ' -f 1; }
elif command -v shasum >/dev/null 2>&1; then
  checksum() { shasum -a 256 "$1" | cut -d ' ' -f 1; }
else
  echo 'Need sha256sum or shasum.' >&2; exit 1
fi
case "$(uname -s):$(uname -m)" in
  Linux:x86_64) asset=herdr-linux-x86_64; digest=14d9e8bc8b4a9e0118d77c32266f76d461f09b40342eb23752960bd89f59929d;;
  Linux:aarch64|Linux:arm64) asset=herdr-linux-aarch64; digest=17d7536f2da50859523680ef279dffcac8e4a235f4e46fe8da6c2ec44141897c;;
  Darwin:arm64|Darwin:aarch64) asset=herdr-macos-aarch64; digest=fb77c2232a05a8035421382c894392f4174e4e38a18e48af3dd0290157c3a7e2;;
  Darwin:x86_64) asset=herdr-macos-x86_64; digest=5fb0a908ec7f6745e3e245738b06bfad56c46391c391ab3c0955fbead01f1369;;
  *) echo 'Supported: Linux/macOS x64 or ARM64.' >&2; exit 1;;
esac
bundle_url=https://github.com/Shinick-Han/agent-exam-kit/releases/download/v0.3.0/writing-skills.tar.gz
bundle_sha=55cb53f11d7087fa8aa5d6109761b8c78a9e91543a55bf76e8e10f50a906bc0d
echo "Agent exam kit 0.3.0 ($asset)"
echo "Herdr: $root/bin/herdr; skills: $skills"
[ "$dry" -eq 0 ] || exit 0
stage=$(mktemp -d "${TMPDIR:-/tmp}/agent-exam-kit.XXXXXXXX")
cleanup() { [ -z "$stage" ] || rm -rf "$stage"; }
trap cleanup 0
trap 'exit 1' 1 2 3 15
fetch_verified() {
  url=$1; expected=$2; output=$3
  if [ -n "$cache" ] && [ -f "$cache/$expected" ]; then
    cp "$cache/$expected" "$output"
  else
    curl --fail --silent --show-error --location --proto '=https' --connect-timeout 15 --max-time 180 "$url" -o "$output"
  fi
  actual=$(checksum "$output")
  [ "$actual" = "$expected" ] || { echo 'SHA-256 mismatch; installation stopped.' >&2; exit 1; }
}
if [ "$only" != skills ]; then
  fetch_verified "https://github.com/herdrdev/herdr/releases/download/v0.9.5/$asset" "$digest" "$stage/herdr"
  chmod 755 "$stage/herdr"
fi
if [ "$only" != herdr ]; then
  fetch_verified "$bundle_url" "$bundle_sha" "$stage/skills.tar.gz"
  # This archive is produced by build_unix_bundle.py from hash-checked public sources.
  tar -xzf "$stage/skills.tar.gz" -C "$stage"
  for name in anti-defensive-writing avoid-ai-writing stop-slop-ko search-first-exam; do
    [ -f "$stage/skills/$name/SKILL.md" ] || { echo "Missing skill: $name" >&2; exit 1; }
  done
fi
mkdir -p "$root"
receipt="$stage/receipt.txt"
printf 'agent-exam-kit 0.3.0\n' > "$receipt"
if [ "$only" != skills ]; then
  mkdir -p "$root/bin"
  if [ -e "$root/bin/herdr" ] || [ -L "$root/bin/herdr" ]; then
    if [ ! -L "$root/bin/herdr" ] && cmp -s "$stage/herdr" "$root/bin/herdr"; then
      echo 'Herdr: already installed'
      printf 'herdr already_installed\n' >> "$receipt"
    else
      echo 'Herdr: kept existing executable (not replaced)'
      printf 'herdr kept_existing_not_verified\n' >> "$receipt"
    fi
  else
    mv "$stage/herdr" "$root/bin/herdr"
    printf 'herdr installed %s\n' "$digest" >> "$receipt"
    echo 'Herdr: installed'
  fi
fi
if [ "$only" != herdr ]; then
  mkdir -p "$skills"
  for name in anti-defensive-writing avoid-ai-writing stop-slop-ko search-first-exam; do
    if [ -e "$skills/$name" ] || [ -L "$skills/$name" ]; then
      echo "$name: kept existing directory"
      printf '%s kept_existing_not_verified\n' "$name" >> "$receipt"
    else
      mv "$stage/skills/$name" "$skills/$name"
      echo "$name: installed"
      printf '%s installed\n' "$name" >> "$receipt"
    fi
  done
fi
mv "$receipt" "$root/receipt-unix.txt"
printf '\nStart: %s/bin/herdr\n' "$root"
printf 'Receipt: %s/receipt-unix.txt\n' "$root"
echo 'Python is not needed to install. Python scanners are optional; writing rules work without them.'
