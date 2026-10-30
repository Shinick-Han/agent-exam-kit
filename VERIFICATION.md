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
