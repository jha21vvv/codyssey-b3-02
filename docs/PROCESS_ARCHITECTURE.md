# AI 기반 Git 커밋 및 PR 자동 생성기 - 아키텍처 및 업무 흐름 가이드

본 문서는 파이썬 기반으로 자동 생성된 **시스템 전체 아키텍처 다이어그램** 및 **업무별 파일/함수 상세 흐름도**를 정리한 문서입니다.

---

## 1. 전체 시스템 아키텍처 (System Architecture Overview)

Python 3.10+ 표준 라이브러리만을 사용하여 구현된 7단계 계층형 아키텍처입니다.

![시스템 전체 아키텍처](diagrams/architecture_overview.png)

### 7개 계층 및 담당 모듈 요약
| 계층 (Layer) | 담당 소스 파일 | 핵심 함수 및 역할 |
|---|---|---|
| **1. Presentation Layer** | `src/cli.py` | `main()`, `build_parser()`, `run_commit_pipeline()`, `run_pr_pipeline()`<br>CLI 명령어(`commit`, `pr`) 파싱 및 파라미터 제어 |
| **2. Git Integration Layer** | `src/git_client.py` | `is_git_repository()`, `get_changed_files()`, `get_git_diff()`, `run_git_command()`<br>Git 저장소 유효성 검사, 변경 파일 목록 파싱, 코드 diff 수집 |
| **3. Security Layer** | `src/security.py` | `apply_safe_mode()`, `mask_sensitive_data()`, `truncate_diff()`<br>API Key, 비밀번호, Email 정규식 마스킹 및 10개 파일 / 200줄 크기 절단 |
| **4. Prompt Engineering Layer** | `src/prompts.py` | `build_commit_prompt()`, `build_pr_prompt()`<br>Conventional Commits 및 PR 3대 헤더(Why/What/How to Test) 템플릿 조립 |
| **5. AI REST Client Layer** | `src/ai_client.py` | `AIClient.generate_completion()`, `load_dotenv_file()`<br>표준 `urllib` 기반 HTTP POST 통신, 1회 단일 호출 보장, 401/429 예외 처리 |
| **6. Validation Layer** | `src/validator.py` | `validate_and_fix_commit()`, `validate_and_fix_pr()`, `clean_title()`<br>로컬 후처리: 제목 글자 수(72/80자) 절단, 누락 헤더/불릿 자동 보완 |
| **7. Output Formatting Layer** | `src/formatter.py` | `format_output()`<br>이중 구분선(=, -) 박스 렌더링, API 호출 횟수/시간/토큰 메타정보 로깅 |

---

## 2. 업무 프로세스 1: 커밋 메시지 자동 생성 흐름 (`commit`)

사용자가 터미널에서 `python -m src.cli commit`을 실행했을 때 파일과 함수가 순차적으로 호출되는 전체 흐름입니다.

![커밋 메시지 자동 생성 흐름](diagrams/process_flow_commit.png)

### 단계별 실행 순서 (Step-by-step)
1. **[STEP 1] CLI 인자 파싱** (`src/cli.py` ➡️ `main()`, `build_parser()`)
   - 명령어 `commit`과 옵션(`-model`, `-temperature`, `-max-tokens`, `-safe-mode`, `-staged`) 파싱
2. **[STEP 2] Git 저장소 유효성 검사** (`src/git_client.py` ➡️ `is_git_repository()`)
   - `git rev-parse --is-inside-work-tree` 실행 (Git 폴더가 아니면 `exit code 1` 종료)
3. **[STEP 3] Git 변경 사항 수집** (`src/git_client.py` ➡️ `get_changed_files()`, `get_git_diff()`)
   - `git status --porcelain`으로 파일 목록 추출 및 `git diff` 수집 (변경 사항 없으면 안내 후 정상 종료)
4. **[STEP 4] 보안 안전 모드 필터링** (`src/security.py` ➡️ `apply_safe_mode()`)
   - 정규식 마스킹(`[REDACTED_...]`) + 최대 10개 파일 / 최대 200줄 절단
5. **[STEP 5] 프롬프트 조립** (`src/prompts.py` ➡️ `build_commit_prompt()`)
   - Conventional Commits 규칙 시스템 프롬프트 + [수정 파일] + [Diff] 결합
6. **[STEP 6] AI REST API 1회 호출** (`src/ai_client.py` ➡️ `AIClient.generate_completion()`)
   - OpenAI 호환 엔드포인트 단 1회 호출 (`call_count=1`), 소요 시간 및 생성 텍스트 획득
7. **[STEP 7] 서식 검증 및 후처리** (`src/validator.py` ➡️ `validate_and_fix_commit()`)
   - 첫 줄 제목 72자 이내 절단, 본문에 파일 언급이나 불릿(`- `) 누락 시 자동 보완
8. **[STEP 8] 최종 출력 렌더링** (`src/formatter.py` ➡️ `format_output()`)
   - 구분선 상자에 담아 터미널 출력 및 메타정보(호출 1회, 소요시간) 표시

---

## 3. 업무 프로세스 2: PR 초안 자동 생성 흐름 (`pr`)

사용자가 터미널에서 `python -m src.cli pr`을 실행했을 때 3대 필수 헤더(Why/What/How to Test)를 완성하는 흐름입니다.

![PR 초안 자동 생성 흐름](diagrams/process_flow_pr.png)

### 단계별 실행 순서 (Step-by-step)
1. **[STEP 1] CLI 인자 파싱** (`src/cli.py` ➡️ `run_pr_pipeline()`)
   - 기본 `max_tokens=1000` 설정, `--safe-mode` 기본 활성화
2. **[STEP 2] Git 저장소 검증** (`src/git_client.py` ➡️ `is_git_repository()`)
3. **[STEP 3] Git 변경 사항 수집** (`src/git_client.py` ➡️ `get_changed_files()`, `get_git_diff()`)
4. **[STEP 4] 보안 안전 필터링** (`src/security.py` ➡️ `apply_safe_mode()`)
5. **[STEP 5] PR 프롬프트 조립** (`src/prompts.py` ➡️ `build_pr_prompt()`)
   - 1줄 제목(80자) 및 3대 헤더(`### Why`, `### What`, `### How to Test`) 필수 지침 주입
6. **[STEP 6] AI API 단일 호출** (`src/ai_client.py` ➡️ `AIClient.generate_completion()`)
7. **[STEP 7] PR 서식 검증 및 헤더 복구** (`src/validator.py` ➡️ `validate_and_fix_pr()`)
   - 정규식으로 3대 섹션 검사, 누락 섹션 자동 생성 및 불릿(`- `) 자동 주입
8. **[STEP 8] PR 박스 터미널 출력** (`src/formatter.py` ➡️ `format_output()`)

---

## 4. 업무 프로세스 3 & 4: 보안 안전 모드 및 AI 통신/예외 분기

![보안 및 AI 통신 상세 흐름](diagrams/process_flow_security_and_ai.png)

### 보안 안전 모드 (`src/security.py`)
1. **정규식(Regex) 마스킹**: OpenAI 키, GitHub 토큰, AWS 키, 이메일, 패스워드 패턴을 `[REDACTED_...]`로 즉시 치환
2. **파일 수 절단**: `diff --git ` 헤더 기준 최대 10개 파일 초과분 절단
3. **라인 수 절단**: 전체 라인 200줄 초과분 절단 및 `... [diff truncated]` 안내 주석 삽입

### AI 통신 및 예외 분기 (`src/ai_client.py`)
1. **설정 검증**: `os.environ` 또는 `.env` 키 확인 (누락 시 OS별 설정법 안내)
2. **HTTP POST 전송**: `urllib.request.urlopen` (타임아웃 45초, `call_count=1`)
3. **HTTP 응답 분기**:
   - `HTTP 200`: 정상 JSON 파싱 후 응답 반환
   - `HTTP 401`: `AuthenticationError` (API Key 인증 실패 안내)
   - `HTTP 429`: `QuotaExceededError` (한도/크레딧 초과 안내)
   - `HTTP 5xx / URLError`: `APIError` (서버 장애 또는 인터넷 연결 끊김 안내)
