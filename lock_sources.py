"""Maintainer helper: pin downloads and generate hash-bound entry points."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".cache"
CACHE.mkdir(exist_ok=True)


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "agent-exam-kit-build"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def store(data):
    digest = hashlib.sha256(data).hexdigest()
    (CACHE / digest).write_bytes(data)
    return digest


skills = []
for name, repo, commit, sub, includes in [
    ("anti-defensive-writing", "Kiterlin/anti-defensive-writing", "f516147d017a3fe43ae99192cb89d8261b0c8679", "skill/anti-defensive-writing/", None),
    ("avoid-ai-writing", "conorbronsdon/avoid-ai-writing", "9cd07215982eca9736e14caaa63241c0264856f3", "", ["SKILL.md", "references", "scripts", "detector", "examples", "agents", "LICENSE", "NOTICE.md"]),
    ("stop-slop-ko", "leeandev/stop-slop-ko", "553be0525c28f593f103fbebae4c1f15684a81e5", "plugins/stop-slop-ko/skills/stop-slop-ko/", None),
]:
    url = f"https://codeload.github.com/{repo}/zip/{commit}"
    data = get(url)
    prefix = repo.split("/")[1] + "-" + commit + "/" + sub
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        assert prefix + "SKILL.md" in archive.namelist()
    item = {"name": name, "repo": repo, "commit": commit, "url": url,
            "sha256": store(data), "prefix": prefix}
    if includes:
        item["includes"] = includes
    skills.append(item)
    print(name, len(data), flush=True)

release = json.loads(subprocess.check_output(
    ["gh", "api", "repos/herdrdev/herdr/releases/tags/v0.9.5"], text=True, encoding="utf-8"))
herdr = {}
for asset in release["assets"]:
    key = asset["name"].removeprefix("herdr-").removesuffix(".zip")
    item = {"name": "herdr-" + key, "version": release["tag_name"],
            "url": asset["browser_download_url"], "sha256": asset["digest"].split(":")[1]}
    if key in ("windows-x86_64", "linux-x86_64"):
        data = get(item["url"])
        assert store(data) == item["sha256"]
        if key == "windows-x86_64":
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                item["zip_member"] = next(x for x in archive.namelist() if x.endswith("herdr.exe"))
        print(item["name"], len(data), flush=True)
    herdr[key] = item

(ROOT / "manifest.json").write_text(json.dumps(
    {"version": "0.1.0", "herdr": herdr, "skills": skills}, ensure_ascii=False, indent=2) + "\n", "utf-8")
engine_sha = hashlib.sha256((ROOT / "install.py").read_bytes()).hexdigest()
bootstrap = '''import hashlib, sys, urllib.request
BASE = "https://raw.githubusercontent.com/Shinick-Han/agent-exam-kit/v0.1.0"
EXPECTED = "ENGINE_SHA"
if sys.version_info < (3, 9):
    raise SystemExit("Python 3.9+ is required")
with urllib.request.urlopen(BASE + "/install.py", timeout=60) as response:
    data = response.read(1024 * 1024)
if hashlib.sha256(data).hexdigest() != EXPECTED:
    raise SystemExit("Installer SHA-256 mismatch")
exec(compile(data, "agent-exam-kit/install.py", "exec"), {"__name__": "__main__"})
'''.replace("ENGINE_SHA", engine_sha)
shell = '''#!/usr/bin/env bash
set -euo pipefail
if command -v python3 >/dev/null 2>&1; then py=python3
elif command -v python >/dev/null 2>&1; then py=python
else echo 'Python 3.9+ is required.' >&2; exit 1; fi
"$py" - "$@" <<'PYBOOT'
''' + bootstrap + "PYBOOT\n"
powershell = '''$ErrorActionPreference = 'Stop'
$kitArgs = @($args)
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) { throw 'Python 3.9+ is required.' }
$bootstrap = @'
''' + bootstrap + "'@\n" + '''& $python.Source -c $bootstrap @kitArgs
if ($LASTEXITCODE -ne 0) { throw "Agent exam kit failed (exit $LASTEXITCODE)." }
'''
# Unix installation is generated separately without a Python runtime.
(ROOT / "install-python.sh").write_text(shell, "utf-8", newline="\n")
(ROOT / "install.ps1").write_text(powershell, "utf-8", newline="\n")
print("Locked engine:", engine_sha)
