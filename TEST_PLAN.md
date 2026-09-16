# 테스트 계획 및 실행 가이드 (TEST_PLAN.md)

> 본 문서는 `codyssey-b3-02` 프로젝트의 기능과 제약 사항을 검증하기 위한 **자동화 단위 테스트 실행법** 및 **수동 시나리오 테스트 절차**를 상세히 안내합니다.

---

## 1. 테스트 개요 및 환경

### 1.1. 테스트 분류
1. **자동화 단위 테스트 (Automated Unit Tests)**:
   - 외부 AI API Key 없이도 실행 가능 (Mock 객체 기반 격리 테스트).
   - Git 수집, 보안 마스킹, 프롬프트 생성, 출력 검증/후처리, CLI 파이프라인 등 총 45개 테스트 케이스 100% 자동 검증.
2. **수동 시나리오 테스트 (Manual Scenario Tests)**:
   - 실제 터미널(PowerShell / CMD) 환경에서 사용자가 직접 명령어를 입력하여 각 기능과 예외 처리의 정상 동작을 확인하는 검증.

### 1.2. 사전 요구사항
* Python 3.10 이상
* Git 설치 및 환경변수 등록

---

## 2. 자동화 단위 테스트 (Automated Tests)

외부 AI 호출 비용이나 인터넷 연결 없이, 프로젝트의 모든 로직과 예외 처리가 정상 동작하는지 1초 이내로 일괄 검증합니다.

### 2.1. 전체 테스트 실행 명령어
프로젝트 루트 디렉토리에서 아래 명령어를 실행합니다:

```powershell
python -m unittest discover -s tests -v
```

### 2.2. 테스트 스위트 구성 및 검증 범위
| 테스트 파일 | 테스트 수 | 주요 검증 내용 |
|---|---|---|
| `test_git_client.py` | 8개 | Git 작업 트리 검증, `git status` 변경 파일 파싱 (한글/공백 경로 포함), staged/unstaged diff 계층적 수집 |
| `test_security.py` | 10개 | OpenAI/Anthropic/AWS/GitHub 키, 이메일, 패스워드 정규식 마스킹, diff 10개 파일 및 200줄 초과 트렁케이션 |
| `test_ai_client.py` | 5개 | API 키 누락 방어(`ConfigurationError`), HTTP 401(인증 실패), HTTP 429(할당량 초과), HTTP 500(서버 오류) |
| `test_prompts.py` | 2개 | Commit(Conventional Commits, 50자) 및 PR(Why/What/How to Test) 프롬프트 구조 검증 |
| `test_validator.py` | 9개 | 제목 72자/80자 절삭, 마크다운 코드블록(```) 제거, 누락된 헤더 및 불릿 자동 복구/보충 |
| `test_formatter.py` | 1개 | 터미널 구획선(`===`, `---`), AI API 호출 횟수(1회) 및 메타정보 출력 검증 |
| `test_cli.py` | 10개 | CLI 인자 파싱(기본값 및 커스텀), 비-Git 디렉토리 방어, 변경 부재 시 종료, 엔드투엔드 파이프라인 |

### 2.3. 기대 결과
터미널 마지막 줄에 아래와 같이 표시되어야 합니다:
```text
Ran 45 tests in 0.0XXs

OK
```

---

## 3. 수동 시나리오 테스트 절차 (Manual Scenarios)

터미널에서 사용자의 입출력 흐름과 예외 상황을 직접 검증하는 7대 시나리오입니다.

---

### [시나리오 1] 도움말(Help) 출력 확인
* **목적**: CLI 명령어 구조 및 옵션 설명이 한글 깨짐 없이 정상 출력되는지 확인.
* **실행 명령**:
  ```powershell
  python -m src.cli --help
  python -m src.cli commit --help
  python -m src.cli pr --help
  ```
* **성공 기준**:
  - `commit`, `pr` 서브커맨드 목록이 나타남.
  - `-m/--model`, `-t/--temperature`, `--max-tokens`, `--staged`, `--safe-mode` 옵션 설명이 출력됨.

---

### [시나리오 2] API Key 미설정 시 방어 동작 검증
* **목적**: 환경변수에 API Key가 등록되지 않은 상태에서 친절한 가이드가 제공되는지 확인.
* **실행 절차**:
  1. 현재 터미널 세션에서 API Key 환경변수를 일시 해제:
     ```powershell
     # PowerShell인 경우
     $env:OPENAI_API_KEY=""
     ```
  2. 커밋 생성 명령 실행:
     ```powershell
     python -m src.cli commit
     ```
* **성공 기준**:
  - 지저분한 Traceback(에러 스택) 없이 아래 안내문 출력:
    ```text
    [설정 오류] AI API Key가 설정되지 않았습니다.
    환경변수를 설정해주세요:
      - Windows (PowerShell): $env:OPENAI_API_KEY="your_key"
      - Windows (CMD): set OPENAI_API_KEY=your_key
      - Linux / macOS: export OPENAI_API_KEY="your_key"
    ```
  - 종료 코드(exit code) 1 반환.

---

### [시나리오 3] 변경 사항 없음(Clean Tree) 대응 검증
* **목적**: Git 작업 트리에 수정된 내용이 없을 때 불필요한 AI 호출을 하지 않고 안전하게 종료하는지 확인.
* **실행 절차**:
  1. 임의의 빈 임시 Git 리포지토리 생성 후 테스트 (코드 블록 안의 내용만 복사):
     ```powershell
     $env:PYTHONPATH = (Get-Location).Path
     mkdir test_clean_repo
     cd test_clean_repo
     git init
     python -m src.cli commit
     cd ..
     Remove-Item -Recurse -Force test_clean_repo
     ```
* **성공 기준**:
  - `[안내] 변경 사항이 없습니다. 코드를 수정하거나 git add 후 다시 실행해주세요.` 출력.
  - AI API 호출 없이 종료 코드 0으로 정상 종료.

---

### [시나리오 4] 실제 파일 변경 후 커밋 메시지 생성 검증 (`commit`)
* **목적**: 실제 코드 변경 사항을 수집하여 Conventional Commits 스타일의 1줄 제목과 본문 불릿을 생성하는지 확인.
* **실행 절차**:
  1. API Key 등록:
     ```powershell
     $env:OPENAI_API_KEY="your-real-openai-api-key"
     ```
  2. 임의 파일 수정 또는 신규 파일 생성:
     ```powershell
     echo "# test note" >> test_file.txt
     ```
  3. 커밋 생성 명령어 실행:
     ```powershell
     python -m src.cli commit
     ```
  4. 테스트 파일 정리:
     ```powershell
     del test_file.txt
     ```
* **성공 기준**:
  - 상단/하단에 이중 구분선(`===`) 및 싱글 구분선(`---`) 구획 표시.
  - 1줄 커밋 제목 (50~72자 이내, `feat:`, `fix:` 등 접두어 포함).
  - 본문에 변경된 파일명 언급 또는 1~2개 불릿(`- `) 포함.
  - `[실행 메타정보]`에 `AI API 호출 횟수 : 1회` 정확히 표시.

---

### [시나리오 5] PR 제목 및 구조화된 본문 생성 검증 (`pr`)
* **목적**: PR 초안 생성 시 80자 제목 및 `Why`, `What`, `How to Test` 3대 섹션 헤더와 불릿이 포함되는지 확인.
* **실행 절차**:
  1. 임의 파일 수정 후 PR 명령어 실행:
     ```powershell
     python -m src.cli pr
     ```
* **성공 기준**:
  - 1줄 PR 제목 (최대 80자).
  - 본문에 아래 3가지 섹션 헤더 및 각 섹션당 1개 이상의 불릿(`- `) 필수 포함:
    - `### Why`
    - `### What`
    - `### How to Test`
  - `[실행 메타정보]`에 `AI API 호출 횟수 : 1회` 표시.

---

### [시나리오 6] Safe Mode 보안 마스킹 및 크기 제한 검증
* **목적**: 코드에 API Key 패턴이나 긴 줄이 포함되었을 때 마스킹 및 트렁케이션이 적용되어 AI로 안전하게 전달되는지 확인.
* **단위 테스트 기반 즉시 검증**:
  ```powershell
  python -m unittest tests/test_security.py -v
  ```
* **수동 diff 확인 검증 (Python 인터프리터)**:
  ```powershell
  python -c "from src.security import mask_sensitive_data; print(mask_sensitive_data('key = \"sk-1234567890abcdefghijklmnopqrstuvwxyz\"'))"
  ```
* **성공 기준**:
  - `key = "[REDACTED_API_KEY]"` 로 마스킹되어 출력됨.
  - 200줄 초과 diff 입력 시 `... [diff truncated by safe-mode: 최대 200줄 초과]` 문구 추가.

---

### [시나리오 7] 비-Git 디렉토리 실행 방어 검증
* **목적**: Git이 초기화되지 않은 폴더에서 실행 시 오류를 정상 안내하는지 확인.
* **실행 절차**:
  ```powershell
  cd ..
  python -m codyssey-b3-02.src.cli commit
  cd codyssey-b3-02
  ```
* **성공 기준**:
  - `[오류] 현재 디렉토리가 Git 저장소가 아닙니다. Git 초기화된 리포지토리에서 실행해주세요.` 출력.
  - 종료 코드 1 반환.

---

## 4. 최종 테스트 검증 체크리스트

| 검증 항목 | 검증 방법 | 확인 여부 |
|---|---|:---:|
| 45개 자동화 단위 테스트 통과 | `python -m unittest discover -s tests -v` | [x] |
| CLI `--help` 옵션 및 한글 출력 정상 | `python -m src.cli --help` | [x] |
| API Key 미설정 시 친절한 가이드 제공 | `python -m src.cli commit` (키 미등록 상태) | [x] |
| 변경 사항 없을 때 안전 종료 (exit 0) | `test_cli.py::test_run_commit_pipeline_no_changes` | [x] |
| 민감정보 마스킹 (`sk-...`, `ghp_...`, 이메일 등) | `test_security.py` | [x] |
| diff 크기 제한 (10개 파일, 200줄 제한) | `test_security.py` | [x] |
| 커밋 제목 72자 이내 및 본문 불릿 보증 | `test_validator.py` | [x] |
| PR 제목 80자 이내 및 Why/What/How to Test 헤더/불릿 보증 | `test_validator.py` | [x] |
| AI API 호출 횟수 정확히 1회 로깅 | `test_formatter.py`, `test_cli.py` | [x] |
| 원격 저장소(`git push`, PR 생성) 자동 반영 배제 | 코드 검토 (로컬 텍스트 출력 한정) | [x] |

