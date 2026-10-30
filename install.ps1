$ErrorActionPreference = 'Stop'
$kitArgs = @($args)
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) { throw 'Python 3.9+ is required.' }
$bootstrap = @'
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
'@
& $python.Source -c $bootstrap @kitArgs
if ($LASTEXITCODE -ne 0) { throw "Agent exam kit failed (exit $LASTEXITCODE)." }
