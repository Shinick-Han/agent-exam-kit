# Agent exam kit

시험과 실습에서 반복되는 환경 설정 시간을 줄이기 위해 만든 개인 설치 번들이다. Herdr TUI, 글쓰기 Skill 3개, 구현 전 조사 Skill인 `search-first-exam`을 한 명령으로 설치한다.

## 만든 목적

환경 설정을 자동화해 요구사항 파악, 구현, 검증에 쓸 시간을 확보하려고 준비했다. Herdr TUI는 코딩 에이전트의 터미널 세션을 관리하고, 글쓰기 Skill은 계획 문서와 작업 기록의 표현을 다듬는 데 사용한다. `search-first-exam`은 구현 전에 기존 코드와 허용된 공개 자료를 찾아 재사용 여부를 판단한다.

이 저장소의 역할은 공개 도구를 내려받고 버전을 확인해 지정된 경로에 설치하는 것이다. 개별 시험 과제의 문제, 답안이나 완성된 풀이를 제공하지 않는다. 실제 과제의 해석과 구현, 결과 검증은 사용자가 제공된 작업 환경에서 수행한다.

설치 과정과 출처를 확인할 수 있도록 다음 내용을 공개한다.

- [install.sh](install.sh): Unix 설치기가 내려받는 파일, 검증 절차와 설치 경로.
- [manifest.json](manifest.json): 원본 저장소, 고정한 커밋과 Herdr 버전, 원본 다운로드의 SHA-256.
- [build_unix_bundle.py](build_unix_bundle.py): 공개 원본에서 필요한 Skill 파일을 모으는 과정.
- [공개 릴리스](https://github.com/Shinick-Han/agent-exam-kit/releases/tag/v0.3.0): Skill 묶음과 해당 파일의 SHA-256.
- [VERIFICATION.md](VERIFICATION.md): 설치 테스트 결과와 확인 범위.

설치 결과는 설치 디렉터리의 기록 파일에 남긴다. `kit.shinick.dev`는 이 저장소의 공개 설치 스크립트를 제공하는 짧은 주소다.

## 설치

Linux/macOS 설치는 Python, Node, Git, jq 없이 실행한다. `sh`, `curl`, `tar`, `gzip`, SHA-256 도구와 기본 셸 명령을 사용한다. Codex는 실행 환경에서 제공하는 버전을 그대로 사용한다.

Linux / macOS:

```bash
curl -fsSL https://kit.shinick.dev | sh
```

고정된 공개 원본 주소:

```bash
curl -fsSL https://raw.githubusercontent.com/Shinick-Han/agent-exam-kit/v0.3.0/install.sh | sh
```

Windows PowerShell용 기존 v0.1.0 설치기는 Python 3.9 이상을 사용하며 Herdr와 글쓰기 Skill 3개를 설치한다. `search-first-exam`은 Unix v0.3.0 번들에 포함되어 있다.

```powershell
irm https://raw.githubusercontent.com/Shinick-Han/agent-exam-kit/v0.1.0/install.ps1 | iex
```

설치 후 출력되는 실행 경로를 사용한다. 셸 프로필과 PATH는 수정하지 않는다.

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
| search-first-exam | [이 저장소의 시험용 수정본](skills/search-first-exam/SKILL.md) | `~/.agents/skills/search-first-exam` |

Herdr의 GUI 앱이 아닌 터미널 버전을 설치한다. 각 Skill의 참조 문서와 스크립트도 함께 받는다.
글쓰기 Skill 원본의 정확한 커밋, 다운로드 URL과 SHA-256은 `manifest.json`에 있다. `search-first-exam`의 원본 커밋과 변경 범위는 해당 `SKILL.md`에 기록한다. 전체 묶음에는 `sources.json`도 포함한다.
원본 도구는 각 저장소의 라이선스를 따른다. 저장소에는 설치 코드를 공개하고, 릴리스에는 공개 Skill 파일을 원본 라이선스와 출처 정보와 함께 묶어 배포한다.

## search-first-exam

[원본 search-first](https://github.com/affaan-m/everything-claude-code/blob/6f1881aeafa3c48f7b603cc4be4b2e4e70daad59/skills/search-first/SKILL.md)는 OSS 전용 검색기가 아니다. 패키지, MCP, 서비스와 공개 저장소까지 검토하는 워크플로다. 이 번들은 원본을 수정한 `search-first-exam`을 설치하며, 기존 `search-first`는 보존한다.

- 제공된 프로젝트 코드와 표준 라이브러리를 먼저 확인한다.
- 외부 조사가 필요하면 일반적인 기술 용어로 공개 문서와 OSS를 찾는다. 과제 내용과 코드를 검색어로 전송하지 않는다.
- 공개 코드의 라이선스와 버전, 실제 검증 결과를 확인한다. GitHub 공개 여부만으로 OSS라고 판단하지 않는다.
- 제공된 Codex를 사용한다. Claude 전용 호출, Aside 자동 조작, 개인 인증 설정 조회와 외부 서비스 설정 지시는 포함하지 않는다.
- 근거가 충분하면 구현으로 넘어간다. 조사 자체를 늘리는 데 시간을 쓰지 않는다.

원본의 MIT 라이선스를 함께 배포한다. 이 수정본은 알려진 응시 조건에 맞춰 범위를 좁힌 것으로, 운영사의 사용 승인을 뜻하지 않는다.

## 설치 동작

- 사용자 권한으로 지정 디렉터리에 설치한다. `sudo`와 관리자 권한을 요구하지 않는다.
- 설치기는 GitHub에서 내려받는 GET 요청만 보낸다. 작업 파일, 프롬프트, 인증 파일은 읽거나 전송하지 않는다.
- Codex 설치·업데이트, 인증·모델·권한 설정 변경, Herdr 통합 훅 설치를 수행하지 않는다.
- Unix 설치기는 기존 Skill 디렉터리를 보존하고 검증하지 않은 기존 설치로 기록한다. Windows 설치기는 파일이 모두 같으면 재설치를 생략하고, 다르면 기존 내용을 보존한다.
- 각 다운로드의 SHA-256을 검증한다. 검증 실패 시 설치를 중단한다.
- Unix 설치 결과는 `~/.agent-exam-kit/receipt-unix.txt`, Windows 결과는 `~/.agent-exam-kit/receipt.json`에 남긴다.
- 설치는 에이전트를 실행하거나 Skill을 자동 호출하지 않는다. 새 Codex 세션에서 필요한 Skill을 명시해 사용한다.

현재 Codex 세션에서 새 Skill을 찾지 못하면 `~/.agents/skills/<이름>/SKILL.md`를 읽도록 요청한다.
스캐너와 참조 파일의 경로는 설치된 Skill 디렉터리를 기준으로 잡는다.

## 미리 확인 / 일부 설치

```bash
curl -fsSL https://kit.shinick.dev | sh -s -- --dry-run
curl -fsSL https://kit.shinick.dev | sh -s -- --skills-only
```

PowerShell에서 옵션을 전달하려면 파일로 내려받는다.

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/Shinick-Han/agent-exam-kit/v0.1.0/install.ps1 -OutFile install-kit.ps1
./install-kit.ps1 --dry-run
```

Unix 옵션: `--root PATH`, `--skills-dir PATH`, `--cache DIR`, `--herdr-only`. Windows Python 설치기는 `--manifest FILE`도 지원한다.
다른 내용의 기존 파일을 자동 덮어쓰는 옵션은 없다.

## Python이 없는 환경

설치와 Herdr 실행, Skill 문체 규칙 사용에는 Python이 필요 없다.
`stop-slop-ko`의 기계적 스캐너는 Python을 사용하므로 Python이 없으면 수동 문체 검토를 진행하고 스캔은 `NOT_RUN`으로 기록한다.
`avoid-ai-writing`의 Node 검사기도 Node가 있을 때만 실행한다.
설치기는 Python이나 Node를 추가 설치하지 않는다.

실제 응시 서버의 OS는 공식 안내에 명시되지 않았다. 터미널에서 `uname -s`로 확인할 수 있다.
Unix 설치기는 Linux/macOS와 x64/ARM64를 감지하며 지원하지 않는 조합에서는 중단한다.

## 번들 재생성

`python build_unix_bundle.py`는 개발자 PC에서만 실행한다. 고정한 공개 원본으로 검증된 Skill 압축 파일과 Python 없는 `install.sh`를 생성한다.
`release/writing-skills.tar.gz`와 `release/SHA256SUMS`는 공개 v0.3.0 릴리스에 첨부한다. 압축 파일 이름은 이전 버전과 같지만 조사 Skill도 포함한다.
`lock_sources.py`는 기존 Python 진입점을 `install-python.sh`로 생성하며 Unix 진입점을 덮어쓰지 않는다.

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
