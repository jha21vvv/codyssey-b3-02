# codyssey-ai-git: AI 기반 Git 커밋 및 PR 자동 생성 도구

> Git의 변경 사항(`git status`, `git diff`)을 분석하여 실무 표준에 부합하는 **커밋 메시지**와 **Pull Request(PR) 초안**을 자동으로 생성해 주는 경량 Python CLI 도구입니다.

---

## 1. 주요 특징

* **원스톱 자동화**: 프로젝트 루트에서 단일 명령어로 Git 변경 사항 수집부터 AI 분석, 형식 검증, 터미널 출력까지 한 번에 완료됩니다.
* **표준 라이브러리 기반 (Zero Dependency)**: Python 3.10+ 내장 라이브러리(`urllib`, `argparse`, `json`, `subprocess`, `re`)만을 사용하여 별도 패키지 설치 없이 즉시 실행할 수 있습니다.
* **보안 안전 모드 (`--safe-mode`) 기본 탑재**:
  * **민감정보 마스킹**: diff 내 API Key, GitHub 토큰, AWS 키, 이메일, 패스워드 등을 정규식으로 감지하여 `[REDACTED_...]` 처리 후 AI로 전송합니다.
  * **diff 크기 제한**: 최대 10개 파일, 최대 200줄 이내로 절삭하여 불필요한 토큰 낭비와 의도치 않은 데이터 유출을 방지합니다.
* **비용 최적화 (1회 호출 원칙)**:
  * 1회 실행 당 정확히 1회의 AI API 호출만 수행하며, 터미널 로그에 실제 호출 횟수가 명시됩니다.
  * 규격(길이 제한, 템플릿 헤더, 불릿 요약) 미달 시 LLM 재생성이 아닌 로컬 후처리기(`Validator`)로 완벽하게 보정합니다.
* **안전한 Git 연동**: `git status`와 `git diff` 수집 및 텍스트 초안 출력까지만 수행하며, `git commit`, `git push`, 원격 PR 생성 등 위험한 자동 반영은 일체 실행하지 않습니다.

---

## 2. 개발 및 실행 환경

* **Python 버전**: Python 3.10 이상 권장 (Python 3.11 호환 검증 완료)
* **운영체제**: Windows, macOS, Linux
* **사전 요구사항**: Git CLI 설치 및 환경변수 PATH 등록

---

## 3. 설치 및 환경 설정

### 3.1. 저장소 클론 및 이동
```bash
git clone https://github.com/jha21vvv/codyssey-b3-02.git
cd codyssey-b3-02
```

### 3.2. AI API Key 환경변수 설정
본 도구는 보안을 위해 API 키를 소스 코드에 절대 저장하지 않으며 환경변수를 통해 주입받습니다. OpenAI 호환 REST API를 지원합니다.

#### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY="sk-your-openai-api-key-here"

# (선택) 프록시 또는 OpenAI 호환 타사 API(Gemini, Groq, Ollama 등)를 사용하는 경우
$env:OPENAI_BASE_URL="https://api.openai.com/v1"
```

#### Windows (CMD)
```cmd
set OPENAI_API_KEY=sk-your-openai-api-key-here
```

#### macOS / Linux (Bash or Zsh)
```bash
export OPENAI_API_KEY="sk-your-openai-api-key-here"
```

---

## 4. 명령어 사용법 (CLI)

프로젝트 루트 디렉토리에서 `python -m src.cli <command> [options]` 형식으로 실행합니다.

### 4.1. 커밋 메시지 자동 생성 (`commit`)
현재 작업 트리의 변경 사항을 요약하여 1줄 제목(50~72자)과 본문 불릿을 포함한 커밋 메시지를 생성합니다.

```powershell
# 기본 실행 (staged + unstaged 변경사항 분석, 안전모드 적용)
python -m src.cli commit

# 스테이징된(git add) 변경사항만 대상으로 지정
python -m src.cli commit --staged

# AI 모델 및 파라미터 직접 지정
python -m src.cli commit -m gpt-4o-mini -t 0.2 --max-tokens 300
```

### 4.2. Pull Request 초안 자동 생성 (`pr`)
80자 이내의 PR 제목과 `Why`, `What`, `How to Test` 3대 필수 섹션 헤더 및 각 섹션별 불릿 항목을 포함한 PR 본문을 생성합니다.

```powershell
# 기본 실행
python -m src.cli pr

# 스테이징된 변경사항만 분석
python -m src.cli pr --staged

# 더 풍부한 설명을 위해 max-tokens 확장
python -m src.cli pr --max-tokens 1500
```

### 4.3. CLI 옵션 상세 안내

| 옵션 | 단축 옵션 | 기본값 | 설명 |
|---|---|---|---|
| `--model` | `-m` | `gpt-4o-mini` | 사용할 AI 모델 이름 (예: `gpt-4o`, `gpt-4o-mini` 등) |
| `--temperature` | `-t` | `0.2` | 생성 다양성 제어 (0.0에 가까울수록 일관되고 정형화된 출력) |
| `--max-tokens` | - | `commit`: 300<br>`pr`: 1000 | 생성할 최대 토큰 수 |
| `--staged` | - | `False` | `git diff --cached` 결과(스테이징된 변경)만 분석 |
| `--safe-mode` | - | `True` | 민감정보 마스킹 및 diff 줄/파일 수 제한 활성화 |
| `--no-safe-mode` | - | - | 안전 모드 비활성화 |

---

## 5. 실행 및 출력 예시

### 5.1. 커밋 메시지 생성 예시 (`python -m src.cli commit`)
```text
====================================================================
  [생성 결과: 커밋 메시지 초안]
--------------------------------------------------------------------
feat(core): implement git collection and safe mode filter

- 변경된 파일: src/git_client.py, src/security.py
- git status 및 git diff 수집 로직 구현
- 정규식 기반 민감정보 마스킹 및 diff 200줄 절삭 안전 모드 추가
--------------------------------------------------------------------
  [실행 메타정보]
  * AI API 호출 횟수 : 1회
  * 소요 시간        : 1.18초
  * 사용 모델        : gpt-4o-mini (temp=0.2, max_tokens=300)
  * 보안 안전 모드   : 적용됨 (ON)
====================================================================
  [안내] 위 결과물은 AI가 생성한 초안입니다. 반드시 검토 후 적용하세요.
====================================================================
```

### 5.2. Pull Request 초안 생성 예시 (`python -m src.cli pr`)
```text
====================================================================
  [생성 결과: Pull Request 초안]
--------------------------------------------------------------------
feat: add automated git commit and PR generator CLI

### Why
- 수동 커밋 메시지 및 PR 작성 시간을 절약하고 협업 표준 형식을 정착시키기 위함

### What
- git status 및 git diff 변경 내용을 수집하는 git_client 모듈 추가
- 민감정보(API 키, 토큰, 이메일) 마스킹 및 diff 길이 제한 보안 모듈 추가
- 커밋(50자/불릿) 및 PR(Why/What/How to Test) 템플릿 검증기 구현
- 단일 실행 CLI 엔트리포인트(src/cli.py) 제공

### How to Test
- python -m unittest discover -s tests 명령으로 45개 단위 테스트 전체 통과 확인
- 파일 수정 후 python -m src.cli commit 및 python -m src.cli pr 동작 확인
--------------------------------------------------------------------
  [실행 메타정보]
  * AI API 호출 횟수 : 1회
  * 소요 시간        : 1.84초
  * 사용 모델        : gpt-4o-mini (temp=0.2, max_tokens=1000)
  * 보안 안전 모드   : 적용됨 (ON)
====================================================================
  [안내] 위 결과물은 AI가 생성한 초안입니다. 반드시 검토 후 적용하세요.
====================================================================
```

---

## 6. 운영 및 보안 가이드

### 6.1. 민감정보 보호 및 안전 모드 (`--safe-mode`)
* **마스킹 패턴**: OpenAI 키(`sk-...`), Anthropic 키(`sk-ant-...`), GitHub PAT(`ghp_...`), AWS 키(`AKIA...`), 이메일 주소(`user@domain.com`), 패스워드 할당문(`password = "..."`) 등을 자동으로 감지하여 치환합니다.
* **Diff 크기 제한**: 대규모 리팩토링 시 지나치게 큰 diff가 전송되어 토큰이 과다 청구되거나 민감 파일이 유출되는 것을 막기 위해 **최대 10개 파일, 최대 200줄**까지만 선별하여 전송합니다.

### 6.2. 비용 및 할당량(Quota) 관리
* **단일 호출 원칙**: 1회 명령어 실행 당 AI API 요청을 **정확히 1회**만 수행합니다.
* **로컬 후처리 검증**: AI가 템플릿 헤더(`Why/What/How to Test`)나 불릿(`- `)을 빠뜨리거나 제목 길이가 초과될 경우, AI를 재호출하지 않고 로컬 `validator.py`가 정규식 및 파서 기반으로 자동 보정하여 추가 비용 발생을 0으로 억제합니다.
* **가성비 모델 권장**: 기본 모델로 가성비가 우수한 `gpt-4o-mini`를 사용하여 1회 실행 비용을 $0.001 미만으로 유지합니다.

### 6.3. 운영 시 주의사항
* AI가 생성한 커밋 메시지와 PR 설명은 **작성을 돕기 위한 초안**입니다.
* 생성된 문구를 터미널에서 복사한 후, 실제 변경 의도와 일치하는지 최종 검토한 뒤 `git commit -m "..."` 또는 GitHub PR에 등록하세요.

---

## 7. 테스트 실행

저장소 내 모든 모듈의 기능과 예외 처리는 `unittest`로 100% 검증할 수 있습니다.

```powershell
python -m unittest discover -s tests -v
```
