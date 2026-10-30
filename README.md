# Agent exam kit

공개 도구를 한 명령으로 설치하는 작은 번들. Herdr TUI와 글쓰기 Skill 3개를 설치한다.

## 설치

Python 3.9 이상이 필요하다. Codex는 실행 환경에서 제공하는 버전을 그대로 사용한다.

Linux / macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/Shinick-Han/agent-exam-kit/v0.1.0/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/Shinick-Han/agent-exam-kit/v0.1.0/install.ps1 | iex
```

설치 후 출력되는 `Start Herdr`의 경로로 실행한다. 셸 프로필과 PATH는 수정하지 않는다.

```bash
~/.agent-exam-kit/bin/herdr
```

Windows:

```powershell
& "$HOME\.agent-exam-kit\bin\herdr.exe"
```

## 포함 항목

| 항목 | 공개 원본 | 설치 위치 |
|---|---|---|
| Herdr TUI 0.9.5 | https://github.com/herdrdev/herdr | `~/.agent-exam-kit/bin` |
| anti-defensive-writing | https://github.com/Kiterlin/anti-defensive-writing | `~/.agents/skills/anti-defensive-writing` |
| avoid-ai-writing | https://github.com/conorbronsdon/avoid-ai-writing | `~/.agents/skills/avoid-ai-writing` |
| stop-slop-ko | https://github.com/leeandev/stop-slop-ko | `~/.agents/skills/stop-slop-ko` |

Herdr의 GUI 앱이 아닌 터미널 버전을 설치한다. 각 Skill의 참조 문서와 스크립트도 함께 받는다.
각 원본의 정확한 커밋, 다운로드 URL과 SHA-256은 `manifest.json`에 있다.
원본 도구는 각 저장소의 라이선스를 따른다. 이 저장소에는 설치기만 포함한다.

## 설치 동작

- 사용자 권한으로 지정 디렉터리에 설치한다. `sudo`와 관리자 권한을 요구하지 않는다.
- 설치기는 GitHub에서 내려받는 GET 요청만 보낸다. 작업 파일, 프롬프트, 인증 파일은 읽거나 전송하지 않는다.
- Codex 설치·업데이트, 인증·모델·권한 설정 변경, Herdr 통합 훅 설치를 수행하지 않는다.
- Skill 파일이 모두 같으면 재설치를 생략한다. 다른 내용이 있는 기존 디렉터리는 보존하고 `kept_existing_not_verified`로 보고한다.
- 각 다운로드의 SHA-256을 검증한다. 검증 실패 시 설치를 중단한다.
- 설치 결과는 `~/.agent-exam-kit/receipt.json`에 남긴다.
- 설치는 에이전트를 실행하거나 Skill을 자동 호출하지 않는다. 새 Codex 세션에서 필요한 Skill을 명시해 사용한다.

현재 Codex 세션에서 새 Skill을 찾지 못하면 `~/.agents/skills/<이름>/SKILL.md`를 읽도록 요청한다.
스캐너와 참조 파일의 경로는 설치된 Skill 디렉터리를 기준으로 잡는다.

## 미리 확인 / 일부 설치

```bash
curl -fsSL https://raw.githubusercontent.com/Shinick-Han/agent-exam-kit/v0.1.0/install.sh | bash -s -- --dry-run
curl -fsSL https://raw.githubusercontent.com/Shinick-Han/agent-exam-kit/v0.1.0/install.sh | bash -s -- --skills-only
```

PowerShell에서 옵션을 전달하려면 파일로 내려받는다.

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/Shinick-Han/agent-exam-kit/v0.1.0/install.ps1 -OutFile install-kit.ps1
./install-kit.ps1 --dry-run
```

개발자용 옵션: `--root PATH`, `--skills-dir PATH`, `--manifest FILE`, `--cache DIR`, `--herdr-only`.
다른 내용의 기존 파일을 자동 덮어쓰는 옵션은 없다.

## 시험에서 사용

공개 하네스와 Skill을 가져오는 데 쓴다. 시험에서 제공하는 Codex와 허용된 모델·인증을 그대로 사용한다.
Herdr는 제공 작업 공간 안에서 터미널 관리에 사용하고, 외부 AI·원격 접속·브라우저 자동 조작을 연결하지 않는다.
과제 내용과 결과물은 외부로 전송하지 않는다. AI 사용이 금지된 후속 서술형에는 적용하지 않는다.
실제 시험 규칙과 제공 환경의 제한을 따른다. 이 저장소는 시험 운영사와 관계없는 개인 설치 번들이다.

글쓰기 Skill은 제출 문서 검토 때 적용한다. 숫자, 실패 기록, 미확인 조건과 기술 용어를 유지한다.
한국어 문서에서는 `stop-slop-ko`를 마지막에 적용한다.

## 확인 범위

테스트 결과는 `VERIFICATION.md`에 기록한다. 실제 Cofa 환경에서의 설치·인증 계승·기록 수집은 사전 체험에서 확인한다.
사전 체험에서 설치한 파일이 본 응시에 유지되는지는 제공 화면에서 확인한다. 같은 명령으로 다시 설치할 수 있다.
