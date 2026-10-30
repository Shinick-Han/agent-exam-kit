# Verification

Date: 2026-10-30

| Check | Result |
|---|---|
| Windows Python unit tests | 6 passed |
| WSL Ubuntu Python unit tests | 6 passed |
| Windows x64 installation | Herdr and all three skills installed under isolated test paths |
| Linux x64 installation | Herdr and all three skills installed under isolated test paths |
| Herdr version on both systems | 0.9.5 |
| Windows repeated installation | All four components reported `already_installed` |
| Existing customized skill | Preserved; reported `kept_existing_not_verified` |
| Modified cached download | SHA-256 mismatch rejected |
| Archive parent traversal / absolute path / symlink | Rejected |
| Dry run | No installation directories created |
| Mock Codex auth sentinel | Unchanged after installation |
| Published v0.1.0 PowerShell entry point | Downloaded from public raw URL; all four components installed in isolated Windows paths and Herdr 0.9.5 executed |
| Published v0.1.0 curl-to-bash entry point | Public bootstrap and manifest fetched in WSL; hash-checked cached components installed in isolated Linux paths and Herdr 0.9.5 executed |
| Korean README style scanner | stop-slop-ko PASS, WARN 0, INFO 0 |

The traversal fixture originally used a harmless backslash separator, which Python's
ZIP implementation normalizes on Windows. The fixture was corrected to test an actual
backslash parent traversal. Both platform test suites then passed.

The Herdr release digests came from the upstream GitHub release API. Both x64
downloads were independently hashed and matched. Skill archives were downloaded
at the manifest's exact commits and hashed locally.

macOS and Linux ARM64 downloads are listed using upstream release digests. They
have not been executed on native hardware. Actual Cofa sandbox installation,
child Codex authorization and platform activity capture remain to be checked there.

No user Codex settings or installed skills were modified during testing. The test
installations use explicit isolated paths. The installer does not start agents.

Local checkout: `C:/Users/user/source/agent-exam-kit`. No verified WorkBite Task
binding was available, so this existing checkout was not enrolled in StorageGuardian.

## Unix 0.2.0

- Replaced the Unix Python bootstrap with a POSIX `sh` installer.
- WSL Ubuntu x64: installation passed with a restricted PATH that contains no
  Python, Node, Git, jq, unzip, Bash or sudo. Herdr 0.9.5 executed successfully.
- Checked dry run, required skill references/scanner presence, repeated installation,
  preservation of a customized skill and refusal of a corrupted cached executable.
- Legacy Python tests: all 6 passed. Worker deployment dry run passed.
- Skills are redistributed in a reproducible 397,294-byte archive with upstream
  licenses and source commit metadata. Installer pins its SHA-256.
- macOS and ARM64 remain unexecuted. Actual Cofa host OS is not explicitly named
  in the provided guides; use `uname -s` inside the actual workspace to verify.
- Deployed the dedicated Worker and `kit.shinick.dev` hostname. The exact hostname
  route takes precedence over the existing gateway wildcard; no gateway code changed.
- Public short-URL smoke test passed using fresh network downloads with Python,
  Node, Git and jq absent from PATH. The served script matched `install.sh` exactly,
  all three skills installed, and Herdr 0.9.5 executed.
- curl HEAD checks on custom domain and workers.dev endpoint returned HTTP 200
  with `X-Kit-Version: 0.2.0`. A separate Python urllib probe received Cloudflare
  error 1010; curl, which is the documented installer transport, succeeded.
