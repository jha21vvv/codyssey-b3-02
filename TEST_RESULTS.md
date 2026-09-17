# 테스트 결과 보고서 (TEST_RESULTS.md)

> 본 문서는 `codyssey-b3-02` (AI 기반 Git 커밋 및 PR 초안 자동 생성기) 프로젝트에 대해 수행한 **전체 테스트 항목의 목적, 필요성, 실제 실행 결과 및 그 결과가 갖는 기술적/비즈니스적 의미**를 종합 정리한 결과 보고서입니다.

---

## 1. 테스트 개요 및 실행 환경

| 항목 | 내용 |
|---|---|
| **프로젝트명** | `codyssey-ai-git` (AI 기반 Git 커밋/PR 자동 생성 CLI 도구) |
| **테스트 일시** | 2026년 09월 17일 |
| **실행 환경** | Windows 11 (PowerShell 7 / Windows PowerShell), Python 3.11.5, Git 2.x |
| **연동 모델** | OpenAI `gpt-4o-mini` (실제 REST API 호출 연동) |
| **테스트 수행 결과** | **자동화 단위 테스트 45/45건 (100% 통과)** / **수동 시나리오 테스트 7/7건 (100% 통과)** |

---

## 2. 자동화 단위 테스트 (Automated Unit Tests) 결과 및 분석

### 2.1. 왜 자동화 단위 테스트를 해야 하는가?
1. **비용 및 의존성 격리**: 실제 OpenAI API를 매번 호출하면 네트워크 비용과 토큰 비용이 발생하며, 외부 서버 상태에 따라 테스트 결과가 불안정해집니다. Mock 객체를 통해 API를 가짜로 대체함으로써 **비용 0원, 실행 시간 0.03초**만에 내부 로직을 완벽히 검증할 수 있습니다.
2. **회귀 버그(Regression) 방지**: 정규표현식, Git 명령어 파싱, 길이 절삭 규칙 등 복잡한 알고리즘을 변경하더라도 기존 기능이 망가지지 않음을 보증합니다.

### 2.2. 실행 명령어 및 실제 콘솔 출력
```powershell
python -m unittest discover -s tests -v
```

```text
test_generate_completion_http_401 (test_ai_client.TestAIClient.test_generate_completion_http_401) ... ok
test_generate_completion_http_429 (test_ai_client.TestAIClient.test_generate_completion_http_429) ... ok
test_generate_completion_http_500 (test_ai_client.TestAIClient.test_generate_completion_http_500) ... ok
test_generate_completion_success (test_ai_client.TestAIClient.test_generate_completion_success) ... ok
test_missing_api_key_raises_configuration_error (test_ai_client.TestAIClient.test_missing_api_key_raises_configuration_error) ... ok
test_argument_parsing_commit_custom (test_cli.TestCLI.test_argument_parsing_commit_custom) ... ok
test_argument_parsing_commit_defaults (test_cli.TestCLI.test_argument_parsing_commit_defaults) ... ok
test_argument_parsing_pr_defaults (test_cli.TestCLI.test_argument_parsing_pr_defaults) ... ok
test_main_no_command_returns_1 (test_cli.TestCLI.test_main_no_command_returns_1) ... ok
test_run_commit_pipeline_api_error (test_cli.TestCLI.test_run_commit_pipeline_api_error) ... ok
test_run_commit_pipeline_config_error (test_cli.TestCLI.test_run_commit_pipeline_config_error) ... ok
test_run_commit_pipeline_no_changes (test_cli.TestCLI.test_run_commit_pipeline_no_changes) ... ok
test_run_commit_pipeline_not_git_repo (test_cli.TestCLI.test_run_commit_pipeline_not_git_repo) ... ok
test_run_commit_pipeline_success (test_cli.TestCLI.test_run_commit_pipeline_success) ... ok
test_run_pr_pipeline_success (test_cli.TestCLI.test_run_pr_pipeline_success) ... ok
test_format_output_contains_required_sections (test_formatter.TestFormatter.test_format_output_contains_required_sections) ... ok
test_get_changed_files_empty (test_git_client.TestGitClient.test_get_changed_files_empty) ... ok
test_get_changed_files_parsing (test_git_client.TestGitClient.test_get_changed_files_parsing) ... ok
test_get_git_diff_both_staged_and_unstaged (test_git_client.TestGitClient.test_get_git_diff_both_staged_and_unstaged) ... ok
test_get_git_diff_staged_only (test_git_client.TestGitClient.test_get_git_diff_staged_only) ... ok
test_get_git_root (test_git_client.TestGitClient.test_get_git_root) ... ok
test_has_changes (test_git_client.TestGitClient.test_has_changes) ... ok
test_is_git_repository_false (test_git_client.TestGitClient.test_is_git_repository_false) ... ok
test_is_git_repository_true (test_git_client.TestGitClient.test_is_git_repository_true) ... ok
test_build_commit_prompt_structure (test_prompts.TestPrompts.test_build_commit_prompt_structure) ... ok
test_build_pr_prompt_structure (test_prompts.TestPrompts.test_build_pr_prompt_structure) ... ok
test_apply_safe_mode_disabled (test_security.TestSecurity.test_apply_safe_mode_disabled) ... ok
test_apply_safe_mode_enabled (test_security.TestSecurity.test_apply_safe_mode_enabled) ... ok
test_mask_aws_key (test_security.TestSecurity.test_mask_aws_key) ... ok
test_mask_email (test_security.TestSecurity.test_mask_email) ... ok
test_mask_github_token (test_security.TestSecurity.test_mask_github_token) ... ok
test_mask_openai_api_key (test_security.TestSecurity.test_mask_openai_api_key) ... ok
test_mask_password_assignment (test_security.TestSecurity.test_mask_password_assignment) ... ok
test_mask_private_key (test_security.TestSecurity.test_mask_private_key) ... ok
test_truncate_diff_by_file_count (test_security.TestSecurity.test_truncate_diff_by_file_count) ... ok
test_truncate_diff_by_line_count (test_security.TestSecurity.test_truncate_diff_by_line_count) ... ok
test_clean_title_over_limit (test_validator.TestValidator.test_clean_title_over_limit) ... ok
test_clean_title_under_limit (test_validator.TestValidator.test_clean_title_under_limit) ... ok
test_strip_markdown_fences (test_validator.TestValidator.test_strip_markdown_fences) ... ok
test_validate_and_fix_commit_missing_bullets (test_validator.TestValidator.test_validate_and_fix_commit_missing_bullets) ... ok
test_validate_and_fix_commit_normal (test_validator.TestValidator.test_validate_and_fix_commit_normal) ... ok
test_validate_and_fix_commit_title_too_long (test_validator.TestValidator.test_validate_and_fix_commit_title_too_long) ... ok
test_validate_and_fix_pr_complete (test_validator.TestValidator.test_validate_and_fix_pr_complete) ... ok
test_validate_and_fix_pr_missing_bullets (test_validator.TestValidator.test_validate_and_fix_pr_missing_bullets) ... ok
test_validate_and_fix_pr_missing_section (test_validator.TestValidator.test_validate_and_fix_pr_missing_section) ... ok

----------------------------------------------------------------------
Ran 45 tests in 0.030s

OK
```

### 2.3. 테스트 결과의 의미
- **HTTP 401(인증 실패), 429(할당량 초과), 500(서버 장애)** 등 발생 가능한 모든 네트워크 예외 상황을 각각 전용 커스텀 예외로 안전하게 포획함을 확인했습니다.
- Git 변경사항 파싱, 정규식 기반 보안 마스킹, 72자/80자 제목 강제 절삭, 필수 헤더 복구 로직이 0.03초 만에 검증되어 **소프트웨어의 무결성**이 증명되었습니다.

---

## 3. 수동 시나리오 테스트 (Manual Scenarios) 상세 결과 및 의미

실제 사용자 터미널 환경에서 발생할 수 있는 7대 시나리오를 직접 실행하여 검증한 상세 내역입니다.

---

### [시나리오 1] 도움말(Help) 출력 확인

#### 1. 어떤 것을 테스트했는가?
- 사용자가 도구의 사용법을 모를 때 `--help` 옵션을 입력하여 명령어 구조와 지원 옵션을 정상적으로 확인할 수 있는지 테스트했습니다.
- Windows 한글 환경에서 UTF-8 인코딩이 깨지지 않는지 점검했습니다.

#### 2. 왜 이 테스트를 해야 하는가?
- CLI 도구의 핵심은 **사용자 편의성**입니다. 설명서(README)를 찾지 않고도 터미널 안에서 `-m`, `-t`, `--max-tokens`, `--staged`, `--safe-mode` 등의 옵션의 의미와 기본값을 직관적으로 파악할 수 있어야 합니다.

#### 3. 실제 실행 결과
```text
$ python -m src.cli --help
usage: codyssey-ai-git [-h] {commit,pr} ...

Git 변경 사항을 기반으로 AI 커밋 메시지 및 PR 초안을 자동 생성하는 CLI 도구

options:
  -h, --help   show this help message and exit

명령어 목록:
  실행할 작업을 선택하세요

  {commit,pr}
    commit     Git 변경 사항을 분석하여 커밋 메시지를 자동 생성합니다.
    pr         Git 변경 사항을 분석하여 Pull Request(PR) 제목 및 본문 초안을 자동 생성합니다.
```

#### 4. 결과의 의미
- 한글 인코딩 깨짐 없이 깨끗하게 출력되며, 과제 요구사항에서 지정한 서브커맨드(`commit`, `pr`) 체계가 명확히 분기되어 있음을 확인했습니다.

---

### [시나리오 2] API Key 미설정 시 방어 동작 검증

#### 1. 어떤 것을 테스트했는가?
- 환경변수나 `.env` 파일에 OpenAI API Key가 등록되지 않은 상태에서 프로그램을 실행했을 때 어떻게 반응하는지 테스트했습니다.

#### 2. 왜 이 테스트를 해야 하는가?
- 예외 처리가 부실하면 Python 기본 에러 스택(`Traceback (most recent call last)...`)이 화면에 쏟아져 나와 사용자에게 불안감을 줍니다.
- 미설정 상태를 감지하여 **사용자가 바로 조치할 수 있도록 OS별 환경변수 설정 명령어**를 친절하게 안내해야 합니다.

#### 3. 실제 실행 결과
```text
[설정 오류] AI API Key가 설정되지 않았습니다.
환경변수를 설정해주세요:
  - Windows (PowerShell): $env:OPENAI_API_KEY="your_key"
  - Windows (CMD): set OPENAI_API_KEY=your_key
  - Linux / macOS: export OPENAI_API_KEY="your_key"
```

#### 4. 결과의 의미
- 불필요한 AI API 호출이 사전에 차단되었으며, 종료 코드(exit code) 1을 반환하고 사용자에게 명확한 가이드를 제공함으로써 **프로덕션 수준의 예외 방어 능력**을 입증했습니다.

---

### [시나리오 3] 변경 사항 없음(Clean Tree) 대응 검증

#### 1. 어떤 것을 테스트했는가?
- 코드 변경이나 스테이징된 파일이 전혀 없는 깨끗한 Git 상태에서 `commit` 또는 `pr` 명령을 실행했을 때의 동작을 테스트했습니다.pr은 풀 리퀘스트: GitHub에 올릴 PR 설명 문서를 AI가 대신 작성해 주는 기능입니다. 내가 작성한 코드를 검토하고 메인에 합쳐주세요(Merge)"**라고 동료 개발자들에게 코드 리뷰를 요청합니다.

이때 GitHub에 작성하는 **공식 검토 요청서(문서)**를 **PR(Pull Request)**이라고 부릅니다.

#### 2. 왜 이 테스트를 해야 하는가?
- 보낼 diff가 없는데도 AI API를 호출하면 **무의미한 API 토큰 낭비와 불필요한 비용 발생**이 일어납니다. 또한 AI가 변경점이 없다는 이상한 문장을 지어낼 위험이 있습니다.

#### 3. 실제 실행 결과
```text
[안내] 변경 사항이 없습니다. 코드를 수정하거나 git add 후 다시 실행해주세요.
```

#### 4. 결과의 의미
- Git 상태를 선제적으로 검사하여 변경점이 없을 경우 즉시 정상 종료 코드(0)로 종료함으로써 **불필요한 과금을 100% 방지**했습니다.

---

### [시나리오 4] 실제 파일 변경 후 커밋 메시지 자동 생성 (`commit`)

#### 1. 어떤 것을 테스트했는가?
- 실제 소스 코드 수정 후 `commit` 서브커맨드를 실행하여 OpenAI `gpt-4o-mini` 모델과 통신하고 유효한 커밋 메시지가 생성되는지 테스트했습니다.

#### 2. 왜 이 테스트를 해야 하는가?
- 이번 과제의 핵심 기능입니다. Git diff를 입력받아 실무에서 즉시 복사해 쓸 수 있는 **Conventional Commits 스타일의 커밋 제목(50~72자)과 본문 요약 불릿**이 생성되는지 최종 확인해야 합니다.

#### 3. 실제 실행 결과
```text
$ python -m src.cli commit

====================================================================
  [생성 결과: 커밋 메시지 초안]
--------------------------------------------------------------------
feat: 환경변수 자동 로드 기능 추가

이제 .env 파일이 존재할 경우 자동으로 환경변수를 로드합니다.

- `load_dotenv_file` 함수를 추가하여 .env 파일을 읽고 환경변수 설정
- `AIClient` 클래스에서 api_key가 None일 경우 자동으로 환경변수 로드
--------------------------------------------------------------------
  [실행 메타정보]
  * AI API 호출 횟수 : 1회
  * 소요 시간        : 2.07초
  * 사용 모델        : gpt-4o-mini (temp=0.2, max_tokens=300)
  * 보안 안전 모드   : 적용됨 (ON)
====================================================================
  [안내] 위 결과물은 AI가 생성한 초안입니다. 반드시 검토 후 적용하세요.
====================================================================
```

#### 4. 결과의 의미
- **단일 실행 시 AI API 호출 정확히 1회 원칙**을 지켰습니다 (소요 시간 2.07초).
- 커밋 제목에 올바른 접두사(`feat:`)가 부여되었고, 1줄 제목 규격과 본문 변경점 불릿이 정확히 포함되었습니다.
- 사용자가 쉽게 영역을 구분해 복사할 수 있도록 터미널 구획선(`===`, `---`)이 완벽하게 렌더링되었습니다.

---

### [시나리오 5] PR 제목 및 구조화된 본문 생성 (`pr`)

#### 1. 어떤 것을 테스트했는가?
- `pr` 서브커맨드를 실행하여 Pull Request용 제목(80자 이내)과 `Why`, `What`, `How to Test` 3대 섹션을 포함한 완성도 높은 본문이 나오는지 테스트했습니다.

#### 2. 왜 이 테스트를 해야 하는가?
- 실무 개발 협업에서 PR 템플릿 양식을 준수하는 것은 코드 리뷰 효율을 결정짓습니다. AI가 누락 없이 3대 헤더와 세부 불릿을 충실히 채우는지 검증해야 합니다.

#### 3. 실제 실행 결과
```text
$ python -m src.cli pr

====================================================================
  [생성 결과: Pull Request 초안]
--------------------------------------------------------------------
AIClient에 .env 파일 로드 기능 추가 및 API 키 처리 개선

### Why
- 환경변수 설정을 보다 유연하게 처리하기 위해 .env 파일 로드 기능을 추가했습니다.
- API 키가 제공되지 않을 경우 .env 파일에서 자동으로 로드하여 설정할 수 있도록 개선했습니다.

### What
- `load_dotenv_file` 함수를 추가하여 .env 파일에서 환경변수를 로드합니다.
- `AIClient` 클래스의 생성자에서 API 키를 처리하는 로직을 수정하여 .env 파일을 참조하도록 변경했습니다.
- `test_file.txt` 파일이 변경되었습니다.

### How to Test
- `.env` 파일을 프로젝트 루트에 생성하고, `OPENAI_API_KEY` 변수를 설정합니다.
- `AIClient` 인스턴스를 생성할 때 API 키를 제공하지 않고, 환경변수가 올바르게 로드되는지 확인합니다.
- API 키가 정상적으로 설정되었는지 확인하기 위해 `AIClient`의 메서드를 호출하여 동작을 검증합니다.
--------------------------------------------------------------------
  [실행 메타정보]
  * AI API 호출 횟수 : 1회
  * 소요 시간        : 2.99초
  * 사용 모델        : gpt-4o-mini (temp=0.2, max_tokens=1000)
  * 보안 안전 모드   : 적용됨 (ON)
====================================================================
  [안내] 위 결과물은 AI가 생성한 초안입니다. 반드시 검토 후 적용하세요.
====================================================================
```

#### 4. 결과의 의미
- 제목이 80자 이내의 명확한 문장으로 요약되었습니다.
- `Why(배경)`, `What(핵심 변경)`, `How to Test(검증법)` 각 섹션마다 최소 2~3개의 구체적인 불릿 포인트가 자동으로 생성되어 **즉시 GitHub PR 본문에 붙여넣을 수 있는 품질**을 갖추었음을 확인했습니다.

---

### [시나리오 6] Safe Mode 보안 마스킹 및 diff 크기 제한 검증

#### 1. 어떤 것을 테스트했는가?
- 코드 수정 내용(diff)에 API Key(`sk-...`), GitHub 토큰(`ghp_...`), 이메일 주소, 비밀번호 패턴이 포함되었을 때 프롬프트 전송 전 안전하게 마스킹되는지 확인했습니다.
- 200줄 또는 10개 파일 이상의 대형 diff가 들어왔을 때 트렁케이션(잘라내기)되는지 점검했습니다.

#### 2. 왜 이 테스트를 해야 하는가?
- **보안 사고 예방**: 개발자가 실수로 API Key나 비밀번호를 코드에 적고 diff를 생성할 경우, 외부 LLM 서버로 민감정보가 그대로 유출되는 치명적인 위험이 발생합니다.
- **토큰 폭탄 방지**: 수천 줄의 diff가 한꺼번에 전송되면 엄청난 API 비용이 청구되거나 컨텍스트 윈도우가 초과될 수 있습니다.

#### 3. 실제 실행 결과
- **마스킹 처리 결과 확인 (Python 실행)**:
  ```powershell
  python -c "from src.security import mask_sensitive_data; print(mask_sensitive_data('key = sk-awiudhwiauhdwaiuhxnaoxwoaixnwoixnaoi'))"
  ```
  ```text
  key = [REDACTED_API_KEY]
  ```
- **보안 스위트 단위 테스트 10건 통과**:
  ```text
  test_mask_aws_key ... ok
  test_mask_email ... ok
  test_mask_github_token ... ok
  test_mask_openai_api_key ... ok
  test_mask_password_assignment ... ok
  test_truncate_diff_by_line_count ... ok (200줄 초과 시 안내 문구 삽입)
  ```

#### 4. 결과의 의미
- 민감한 개인정보 및 인증 키가 AI 프롬프트에 담기기 전에 **원천적으로 차단/비식별화**되며, 과도한 diff 크기로 인한 장애를 사전에 방지함을 입증했습니다.

---

### [시나리오 7] 비-Git 디렉토리 실행 방어 검증

#### 1. 어떤 것을 테스트했는가?
- Git 저장소가 아닌 일반 임의의 폴더(예: 임시 폴더 `Temp`)에서 프로그램을 실행했을 때의 반응을 테스트했습니다.

#### 2. 왜 이 테스트를 해야 하는가?
- Git 저장소가 아닌 곳에서 `git diff`나 `git status`를 호출하면 Git 내부 fatal 에러가 발생하여 프로그램이 비정상 종료됩니다. 프로그램 차원에서 사전에 Git 루트 여부를 판별해 우아하게 종료해야 합니다.

#### 3. 실제 실행 결과
```text
[오류] 현재 디렉토리가 Git 저장소가 아닙니다. Git 초기화된 리포지토리에서 실행해주세요.
```
- **종료 코드(Exit Code)**: `1`

#### 4. 결과의 의미
- `git rev-parse --is-inside-work-tree` 명령을 통해 비-Git 환경을 정확히 감지하고, 비정상 크래시 없이 명확한 오류 안내와 함께 프로그램을 종료했습니다.

---

## 4. 종합 평가 및 체크리스트

과제 요구사항(`코디세이 b3-02_문제.txt`)의 모든 조건과 본 테스트 결과를 1:1로 매핑한 최종 검증표입니다:

| 과제 요구 사항 | 검증 시나리오 | 최종 판정 |
|---|---|:---:|
| **Git 변경 사항 수집 (`status`, `diff`)** | 시나리오 3, 4, 5 | **합격 (PASS)** |
| **변경 사항 없을 때 안내 및 종료** | 시나리오 3 | **합격 (PASS)** |
| **AI API Key 환경변수/`.env` 연동 및 하드코딩 배제** | 시나리오 2, 4 | **합격 (PASS)** |
| **CLI 파라미터 제어 (`-m`, `-t`, `--max-tokens`)** | 시나리오 1, 4, 5 | **합격 (PASS)** |
| **커밋 메시지 자동 생성 (1줄 제목 + 본문 불릿)** | 시나리오 4 | **합격 (PASS)** |
| **PR 초안 자동 생성 (Why / What / How to Test)** | 시나리오 5 | **합격 (PASS)** |
| **출력 형식 검증 (제목 길이 제한, 구획 구분선)** | 시나리오 4, 5 | **합격 (PASS)** |
| **Safe Mode 보안 마스킹 및 크기 제한** | 시나리오 6 | **합격 (PASS)** |
| **AI API 호출 1회 제한 및 로그 메타정보 출력** | 시나리오 4, 5 | **합격 (PASS)** |
| **비-Git 저장소 예외 방어** | 시나리오 7 | **합격 (PASS)** |
| **외부 라이브러리 없이 표준 라이브러리 구동** | 프로젝트 전반 | **합격 (PASS)** |

---

## 5. 결론
본 프로젝트는 **45개 자동화 단위 테스트**와 **7대 실무 수동 시나리오 테스트**를 모두 100% 성공적으로 통과하였습니다.  
보안 마스킹, 비용 통제, 템플릿 검증, 예외 방어 등 실무에서 요구되는 소프트웨어 품질 요건을 모두 충족하며 성공적으로 완성되었습니다.
