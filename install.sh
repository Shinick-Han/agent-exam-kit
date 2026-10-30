#!/usr/bin/env bash
set -euo pipefail
if command -v python3 >/dev/null 2>&1; then py=python3
elif command -v python >/dev/null 2>&1; then py=python
else echo 'Python 3.9+ is required.' >&2; exit 1; fi
"$py" - "$@" <<'PYBOOT'
import hashlib, sys, urllib.request
BASE = "https://raw.githubusercontent.com/Shinick-Han/agent-exam-kit/v0.1.0"
EXPECTED = "0b960f1158cd5169ae5c0575ff020c1cd03df579450a03405f5775e11c9430a9"
if sys.version_info < (3, 9):
    raise SystemExit("Python 3.9+ is required")
with urllib.request.urlopen(BASE + "/install.py", timeout=60) as response:
    data = response.read(1024 * 1024)
if hashlib.sha256(data).hexdigest() != EXPECTED:
    raise SystemExit("Installer SHA-256 mismatch")
exec(compile(data, "agent-exam-kit/install.py", "exec"), {"__name__": "__main__"})
PYBOOT
