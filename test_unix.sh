#!/bin/sh
set -eu
repo=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
testroot=$(mktemp -d /tmp/agent-exam-kit-test.XXXXXXXX)
cleanup() { rm -rf "$testroot"; }
trap cleanup 0
trap 'exit 1' 1 2 3 15
mkdir "$testroot/path"
# Deliberately exclude Python, Node, Git, jq, unzip, Bash and sudo.
for tool in curl tar gzip mktemp uname mkdir mv chmod cmp rm cp cut sha256sum cat; do
  ln -s "$(command -v "$tool")" "$testroot/path/$tool"
done
export PATH="$testroot/path"
if command -v python3 >/dev/null 2>&1 || command -v node >/dev/null 2>&1; then
  echo 'Test PATH unexpectedly contains a runtime.' >&2; exit 1
fi
run_install() {
  /bin/sh "$repo/install.sh" --root "$testroot/root" --skills-dir "$testroot/skills" --cache "$repo/.cache" "$@"
}
run_install --dry-run
[ ! -e "$testroot/root" ]
run_install
"$testroot/root/bin/herdr" --version
for name in anti-defensive-writing avoid-ai-writing stop-slop-ko search-first-exam; do
  [ -f "$testroot/skills/$name/SKILL.md" ]
done
[ -f "$testroot/skills/avoid-ai-writing/references/patterns.md" ]
[ -f "$testroot/skills/stop-slop-ko/scripts/slop_scan.py" ]
[ -s "$testroot/skills/search-first-exam/UPSTREAM-LICENSE" ]
cmp "$repo/skills/search-first-exam/SKILL.md" "$testroot/skills/search-first-exam/SKILL.md"
printf 'customized' > "$testroot/skills/anti-defensive-writing/SKILL.md"
run_install
[ "$(cat "$testroot/skills/anti-defensive-writing/SKILL.md")" = customized ]
mkdir "$testroot/bad-cache"
printf 'corrupt' > "$testroot/bad-cache/14d9e8bc8b4a9e0118d77c32266f76d461f09b40342eb23752960bd89f59929d"
if /bin/sh "$repo/install.sh" --herdr-only --root "$testroot/bad-root" --cache "$testroot/bad-cache"; then
  echo 'FAIL: accepted a corrupt executable' >&2; exit 1
fi
[ ! -e "$testroot/bad-root" ]
echo 'PASS: POSIX installation without Python/Node; dry run, references, repeat, preservation.'
