#!/bin/sh
set -eu
repo=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
testroot=$(mktemp -d /tmp/kit-public.XXXXXXXX)
cleanup() { rm -rf "$testroot"; }
trap cleanup 0
trap 'exit 1' 1 2 3 15
mkdir "$testroot/path"
for tool in curl tar gzip mktemp uname mkdir mv chmod cmp rm cp cut sha256sum cat; do
  ln -s "$(command -v "$tool")" "$testroot/path/$tool"
done
export PATH="$testroot/path"
if command -v python3 >/dev/null 2>&1 || command -v node >/dev/null 2>&1; then
  echo 'Unexpected runtime in test PATH.' >&2; exit 1
fi
curl -fsSL https://kit.shinick.dev -o "$testroot/install.sh"
cmp "$repo/install.sh" "$testroot/install.sh"
curl -fsSL https://kit.shinick.dev | /bin/sh -s -- --root "$testroot/root" --skills-dir "$testroot/skills"
"$testroot/root/bin/herdr" --version
for name in anti-defensive-writing avoid-ai-writing stop-slop-ko search-first-exam; do
  test -f "$testroot/skills/$name/SKILL.md"
done
test -f "$testroot/skills/avoid-ai-writing/references/patterns.md"
echo 'PASS: public short URL, fresh network downloads, no Python/Node/Git/jq.'
