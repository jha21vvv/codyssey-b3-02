"""
AI 기반 Git 커밋 및 PR 자동 생성기 - 아키텍처 및 업무 흐름 다이어그램 생성 스크립트
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager, rc

# 1. 한글 폰트 설정 (Windows Malgun Gothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "docs", "diagrams")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_architecture_overview():
    """1. 전체 시스템 계층형 아키텍처 다이어그램"""
    fig, ax = plt.subplots(figsize=(15, 11), dpi=200)
    ax.set_facecolor("#F8F9FA")
    fig.patch.set_facecolor("#FFFFFF")

    # 타이틀
    ax.text(7.5, 10.4, "AI 기반 Git 커밋 & PR 자동 생성기 - 시스템 아키텍처", 
            fontsize=20, fontweight="bold", ha="center", va="center", color="#1A202C")
    ax.text(7.5, 9.9, "Python 3.10+ 표준 라이브러리 기반 | 무의존성 경량 아키텍처 | 1회 호출 및 보안 안전 모드", 
            fontsize=12, ha="center", va="center", color="#4A5568")

    layers = [
        {
            "name": "1. CLI 프레젠테이션 계층 (Presentation Layer)",
            "file": "src/cli.py",
            "desc": "명령어 파싱 (commit, pr) | 옵션 제어 (-model, -temperature, -max-tokens, -safe-mode) | 파이프라인 총괄",
            "y": 8.5, "color": "#EBF8FF", "edge": "#3182CE", "badge": "#2B6CB0"
        },
        {
            "name": "2. Git 연동 및 형상 수집 계층 (Git Integration Layer)",
            "file": "src/git_client.py",
            "desc": "is_git_repository() [루트 검사] | get_changed_files() [status --porcelain] | get_git_diff() [staged/unstaged]",
            "y": 7.1, "color": "#F0FFF4", "edge": "#38A169", "badge": "#2F855A"
        },
        {
            "name": "3. 보안 및 데이터 정제 계층 (Security & Sanitization Layer)",
            "file": "src/security.py",
            "desc": "apply_safe_mode() | mask_sensitive_data() [정규식 API키/PW/Email 마스킹] | truncate_diff() [10파일/200줄 제한]",
            "y": 5.7, "color": "#FEFCBF", "edge": "#D69E2E", "badge": "#B7791F"
        },
        {
            "name": "4. 프롬프트 엔지니어링 계층 (Prompt Engineering Layer)",
            "file": "src/prompts.py",
            "desc": "COMMIT_SYSTEM_PROMPT (Conventional Commits) | PR_SYSTEM_PROMPT (Why/What/How to Test) | build_prompt()",
            "y": 4.3, "color": "#FAF5FF", "edge": "#805AD5", "badge": "#6B46C1"
        },
        {
            "name": "5. AI REST 클라이언트 계층 (AI Client Layer)",
            "file": "src/ai_client.py",
            "desc": "AIClient.generate_completion() | urllib.request (HTTP POST) | 1회 호출(call_count=1) | 401/429 예외 처리",
            "y": 2.9, "color": "#FFF5F5", "edge": "#E53E3E", "badge": "#C53030"
        },
        {
            "name": "6. 서식 검증 및 후처리 계층 (Validation & Post-processing)",
            "file": "src/validator.py",
            "desc": "validate_and_fix_commit() [제목 72자 자르기, 불릿/파일 보완] | validate_and_fix_pr() [제목 80자, 3대 헤더 복구]",
            "y": 1.5, "color": "#EDFDFD", "edge": "#319795", "badge": "#285E61"
        },
        {
            "name": "7. 결과 포맷팅 및 출력 계층 (Output Formatting Layer)",
            "file": "src/formatter.py",
            "desc": "format_output() | 이중 구분선(=, -) 박스 렌더링 | 실행 메타정보(호출수, 시간, 토큰) | 사용자 검토 안내",
            "y": 0.1, "color": "#F7FAFC", "edge": "#718096", "badge": "#4A5568"
        }
    ]

    for layer in layers:
        y = layer["y"]
        # 계층 박스
        rect = patches.FancyBboxPatch(
            (0.8, y), 13.4, 1.05,
            boxstyle="round,pad=0.1,rounding_size=0.15",
            facecolor=layer["color"], edgecolor=layer["edge"], linewidth=2
        )
        ax.add_patch(rect)

        # 뱃지 (파일명)
        badge = patches.FancyBboxPatch(
            (1.0, y + 0.65), 2.2, 0.32,
            boxstyle="round,pad=0.05,rounding_size=0.08",
            facecolor=layer["badge"], edgecolor="none"
        )
        ax.add_patch(badge)
        ax.text(2.1, y + 0.81, layer["file"], fontsize=9.5, fontweight="bold", color="#FFFFFF", ha="center", va="center")

        # 계층명
        ax.text(3.4, y + 0.81, layer["name"], fontsize=12.5, fontweight="bold", color="#2D3748", va="center")

        # 설명
        ax.text(1.1, y + 0.28, layer["desc"], fontsize=10, color="#4A5568", va="center")

        # 아래로 향하는 연결 화살표 (마지막 계층 제외)
        if y > 0.5:
            ax.annotate('', xy=(7.5, y - 0.32), xytext=(7.5, y),
                        arrowprops=dict(facecolor='#718096', edgecolor='none', width=2.5, headwidth=8, headlength=7))

    ax.set_xlim(0, 15)
    ax.set_ylim(-0.2, 10.8)
    ax.axis("off")

    output_path = os.path.join(OUTPUT_DIR, "architecture_overview.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[생성 완료] {output_path}")


def create_commit_process_flow():
    """2. 커밋 메시지 자동 생성 상세 프로세스 흐름도"""
    fig, ax = plt.subplots(figsize=(15, 12), dpi=200)
    ax.set_facecolor("#F8F9FA")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(7.5, 11.5, "업무 프로세스 1: 커밋 메시지 자동 생성 흐름 (commit)", 
            fontsize=18, fontweight="bold", ha="center", va="center", color="#1A202C")
    ax.text(7.5, 11.05, "명령어: python -m src.cli commit [옵션] | 파일 및 함수 호출 흐름", 
            fontsize=11.5, ha="center", va="center", color="#4A5568")

    steps = [
        {"num": "STEP 1", "file": "src/cli.py", "func": "main() -> build_parser() -> parse_args()",
         "action": "사용자 입력 파싱 (-model, -temperature, -max-tokens, -safe-mode, -staged)", "color": "#EBF8FF", "edge": "#3182CE"},
        {"num": "STEP 2", "file": "src/git_client.py", "func": "is_git_repository()",
         "action": "git rev-parse --is-inside-work-tree 실행 (저장소 아니면 sys.exit(1))", "color": "#F0FFF4", "edge": "#38A169"},
        {"num": "STEP 3", "file": "src/git_client.py", "func": "get_changed_files() & get_git_diff()",
         "action": "git status --porcelain 및 git diff 수집 (변경 사항 없으면 안내 후 정상 종료 0)", "color": "#F0FFF4", "edge": "#38A169"},
        {"num": "STEP 4", "file": "src/security.py", "func": "apply_safe_mode()",
         "action": "mask_sensitive_data() (키/토큰/PW 마스킹) + truncate_diff() (최대 10파일, 200줄 절단)", "color": "#FEFCBF", "edge": "#D69E2E"},
        {"num": "STEP 5", "file": "src/prompts.py", "func": "build_commit_prompt()",
         "action": "COMMIT_SYSTEM_PROMPT (50자/72자 제목, 파일/불릿 요약) + [수정된 파일] + [Diff] 조립", "color": "#FAF5FF", "edge": "#805AD5"},
        {"num": "STEP 6", "file": "src/ai_client.py", "func": "AIClient.generate_completion()",
         "action": "OpenAI REST API 1회 호출 (urllib.request POST) | 응답 텍스트 & 소요시간 측정", "color": "#FFF5F5", "edge": "#E53E3E"},
        {"num": "STEP 7", "file": "src/validator.py", "func": "validate_and_fix_commit()",
         "action": "로컬 후처리: 제목 길이(72자) 자르기, 불릿('- ') 또는 파일 언급 누락 시 자동 보완", "color": "#EDFDFD", "edge": "#319795"},
        {"num": "STEP 8", "file": "src/formatter.py", "func": "format_output()",
         "action": "이중 구분선(=, -) 박스 렌더링 + [실행 메타정보] (호출 1회, 시간, 토큰) 터미널 출력", "color": "#F7FAFC", "edge": "#718096"},
    ]

    y_start = 9.8
    y_gap = 1.3
    for i, step in enumerate(steps):
        y = y_start - (i * y_gap)

        # 박스
        rect = patches.FancyBboxPatch(
            (1.0, y), 13.0, 0.95,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            facecolor=step["color"], edgecolor=step["edge"], linewidth=2
        )
        ax.add_patch(rect)

        # 번호 뱃지
        badge = patches.FancyBboxPatch(
            (1.2, y + 0.55), 1.6, 0.28,
            boxstyle="round,pad=0.04,rounding_size=0.06",
            facecolor=step["edge"], edgecolor="none"
        )
        ax.add_patch(badge)
        ax.text(2.0, y + 0.69, step["num"], fontsize=9.5, fontweight="bold", color="#FFFFFF", ha="center", va="center")

        # 파일::함수명
        ax.text(3.1, y + 0.69, f"{step['file']} :: {step['func']}", fontsize=11.5, fontweight="bold", color="#2D3748", va="center")

        # 세부 동작
        ax.text(1.4, y + 0.25, step["action"], fontsize=10, color="#4A5568", va="center")

        # 화살표
        if i < len(steps) - 1:
            ax.annotate('', xy=(7.5, y - 0.35), xytext=(7.5, y),
                        arrowprops=dict(facecolor='#4A5568', edgecolor='none', width=2.5, headwidth=8, headlength=7))

    ax.set_xlim(0, 15)
    ax.set_ylim(-0.5, 12.0)
    ax.axis("off")

    output_path = os.path.join(OUTPUT_DIR, "process_flow_commit.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[생성 완료] {output_path}")


def create_pr_process_flow():
    """3. PR 초안 자동 생성 상세 프로세스 흐름도"""
    fig, ax = plt.subplots(figsize=(15, 12), dpi=200)
    ax.set_facecolor("#F8F9FA")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(7.5, 11.5, "업무 프로세스 2: Pull Request(PR) 초안 자동 생성 흐름 (pr)", 
            fontsize=18, fontweight="bold", ha="center", va="center", color="#1A202C")
    ax.text(7.5, 11.05, "명령어: python -m src.cli pr [옵션] | 3대 필수 헤더(Why/What/How to Test) 보장", 
            fontsize=11.5, ha="center", va="center", color="#4A5568")

    steps = [
        {"num": "STEP 1", "file": "src/cli.py", "func": "main() -> run_pr_pipeline()",
         "action": "PR 명령어 및 옵션 파싱 (기본 max-tokens=1000 설정, safe-mode 기본 ON)", "color": "#EBF8FF", "edge": "#3182CE"},
        {"num": "STEP 2", "file": "src/git_client.py", "func": "is_git_repository()",
         "action": "Git 저장소 유효성 검사 (Git 환경 아니면 에러 출력 후 종료 1)", "color": "#F0FFF4", "edge": "#38A169"},
        {"num": "STEP 3", "file": "src/git_client.py", "func": "get_changed_files() & get_git_diff()",
         "action": "전체 작업 트리 및 스테이징 변경사항 diff 수집 (변경 없으면 0 종료)", "color": "#F0FFF4", "edge": "#38A169"},
        {"num": "STEP 4", "file": "src/security.py", "func": "apply_safe_mode()",
         "action": "민감정보(API Key, Email 등) 마스킹 및 최대 10개 파일 / 200줄 절단 필터링", "color": "#FEFCBF", "edge": "#D69E2E"},
        {"num": "STEP 5", "file": "src/prompts.py", "func": "build_pr_prompt()",
         "action": "PR_SYSTEM_PROMPT (1줄 제목 80자 이내, Why/What/How to Test 헤더 및 불릿 강제) 조립", "color": "#FAF5FF", "edge": "#805AD5"},
        {"num": "STEP 6", "file": "src/ai_client.py", "func": "AIClient.generate_completion()",
         "action": "OpenAI 호환 REST API 1회 호출 (max_tokens=1000) 및 응답 획득", "color": "#FFF5F5", "edge": "#E53E3E"},
        {"num": "STEP 7", "file": "src/validator.py", "func": "validate_and_fix_pr()",
         "action": "로컬 정규식 검증: 제목 80자 자르기, Why/What/How to Test 누락 헤더 자동 복구, 불릿 자동 주입", "color": "#EDFDFD", "edge": "#319795"},
        {"num": "STEP 8", "file": "src/formatter.py", "func": "format_output()",
         "action": "[생성 결과: PR 초안] 박스 출력 + 호출 횟수, 토큰, 소요시간 메타정보 출력", "color": "#F7FAFC", "edge": "#718096"},
    ]

    y_start = 9.8
    y_gap = 1.3
    for i, step in enumerate(steps):
        y = y_start - (i * y_gap)

        rect = patches.FancyBboxPatch(
            (1.0, y), 13.0, 0.95,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            facecolor=step["color"], edgecolor=step["edge"], linewidth=2
        )
        ax.add_patch(rect)

        badge = patches.FancyBboxPatch(
            (1.2, y + 0.55), 1.6, 0.28,
            boxstyle="round,pad=0.04,rounding_size=0.06",
            facecolor=step["edge"], edgecolor="none"
        )
        ax.add_patch(badge)
        ax.text(2.0, y + 0.69, step["num"], fontsize=9.5, fontweight="bold", color="#FFFFFF", ha="center", va="center")

        ax.text(3.1, y + 0.69, f"{step['file']} :: {step['func']}", fontsize=11.5, fontweight="bold", color="#2D3748", va="center")
        ax.text(1.4, y + 0.25, step["action"], fontsize=10, color="#4A5568", va="center")

        if i < len(steps) - 1:
            ax.annotate('', xy=(7.5, y - 0.35), xytext=(7.5, y),
                        arrowprops=dict(facecolor='#4A5568', edgecolor='none', width=2.5, headwidth=8, headlength=7))

    ax.set_xlim(0, 15)
    ax.set_ylim(-0.5, 12.0)
    ax.axis("off")

    output_path = os.path.join(OUTPUT_DIR, "process_flow_pr.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[생성 완료] {output_path}")


def create_security_and_ai_flow():
    """4. 보안 마스킹 및 AI REST 통신 상세 처리 흐름도 (2단 구성)"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10), dpi=200)
    fig.patch.set_facecolor("#FFFFFF")

    # 왼쪽: 보안 모듈 흐름
    ax1.set_facecolor("#F8F9FA")
    ax1.text(4.5, 9.5, "업무 프로세스 3: 보안 안전 모드 (--safe-mode)", fontsize=14, fontweight="bold", ha="center", color="#1A202C")
    ax1.text(4.5, 9.05, "src/security.py 동작 메커니즘", fontsize=10.5, ha="center", color="#718096")

    sec_steps = [
        ("입력 데이터", "원시 Git Diff 텍스트 (raw_diff)", "#EBF8FF", "#3182CE"),
        ("1차 정규식 마스킹", "OpenAI Key -> [REDACTED_API_KEY]\nGitHub Token -> [REDACTED_GITHUB_TOKEN]\nAWS Key -> [REDACTED_AWS_KEY]\n이메일 -> [REDACTED_EMAIL]\npassword = '..' -> [REDACTED_SECRET]", "#FEFCBF", "#D69E2E"),
        ("2차 파일 수 절단", "diff --git 헤더 기준 최대 10개 파일 검사\n11번째 파일부터 절단 후 생략 안내 부착", "#FEEBC8", "#DD6B20"),
        ("3차 라인 수 절단", "전체 라인 수 검사 (최대 200줄)\n200줄 초과 시 절단 및 [diff truncated] 주석", "#FED7D7", "#E53E3E"),
        ("안전 diff 출력", "마스킹 & 크기 제한 완료된 안전 텍스트 반환", "#F0FFF4", "#38A169"),
    ]

    for i, (title, desc, bg, border) in enumerate(sec_steps):
        y = 7.3 - (i * 1.7)
        rect = patches.FancyBboxPatch((0.5, y), 8.0, 1.25, boxstyle="round,pad=0.08,rounding_size=0.1", facecolor=bg, edgecolor=border, linewidth=2)
        ax1.add_patch(rect)
        ax1.text(0.8, y + 0.95, title, fontsize=11, fontweight="bold", color="#2D3748")
        ax1.text(0.8, y + 0.45, desc, fontsize=8.5, color="#4A5568", va="center")
        if i < len(sec_steps) - 1:
            ax1.annotate('', xy=(4.5, y - 0.45), xytext=(4.5, y),
                         arrowprops=dict(facecolor='#718096', edgecolor='none', width=2, headwidth=6, headlength=6))

    ax1.set_xlim(0, 9)
    ax1.set_ylim(-1.5, 10.0)
    ax1.axis("off")

    # 오른쪽: AI 통신 및 예외 처리 흐름
    ax2.set_facecolor("#F8F9FA")
    ax2.text(4.5, 9.5, "업무 프로세스 4: AI 통신 및 예외 처리", fontsize=14, fontweight="bold", ha="center", color="#1A202C")
    ax2.text(4.5, 9.05, "src/ai_client.py 동작 메커니즘", fontsize=10.5, ha="center", color="#718096")

    ai_steps = [
        ("API 키 검증", "os.environ['OPENAI_API_KEY'] 검사\n누락 시 ConfigurationError (OS별 설정법 안내)", "#EBF8FF", "#3182CE"),
        ("HTTP 패킷 구성", "endpoint: /v1/chat/completions\nheaders: Bearer <KEY>, Content-Type: json\nbody: json.dumps(payload).encode('utf-8')", "#FAF5FF", "#805AD5"),
        ("urllib 전송 & 카운트", "urllib.request.urlopen(req, timeout=45)\n* 1회 호출 보장 (self.call_count += 1)\n* time.perf_counter()로 소요시간 측정", "#FEFCBF", "#D69E2E"),
        ("상태코드별 분기", "200 OK -> JSON 파싱 (choices[0].message)\n401 Unauthorized -> AuthenticationError\n429 Rate Limit -> QuotaExceededError\n5xx / URLError -> APIError (네트워크 오류)", "#FED7D7", "#E53E3E"),
        ("최종 결과 반환", "(생성된 텍스트, 소요 시간(초)) 튜플 반환", "#F0FFF4", "#38A169"),
    ]

    for i, (title, desc, bg, border) in enumerate(ai_steps):
        y = 7.3 - (i * 1.7)
        rect = patches.FancyBboxPatch((0.5, y), 8.0, 1.25, boxstyle="round,pad=0.08,rounding_size=0.1", facecolor=bg, edgecolor=border, linewidth=2)
        ax2.add_patch(rect)
        ax2.text(0.8, y + 0.95, title, fontsize=11, fontweight="bold", color="#2D3748")
        ax2.text(0.8, y + 0.45, desc, fontsize=8.5, color="#4A5568", va="center")
        if i < len(ai_steps) - 1:
            ax2.annotate('', xy=(4.5, y - 0.45), xytext=(4.5, y),
                         arrowprops=dict(facecolor='#718096', edgecolor='none', width=2, headwidth=6, headlength=6))

    ax2.set_xlim(0, 9)
    ax2.set_ylim(-1.5, 10.0)
    ax2.axis("off")

    output_path = os.path.join(OUTPUT_DIR, "process_flow_security_and_ai.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[생성 완료] {output_path}")


if __name__ == "__main__":
    print("=== 다이어그램 이미지 생성 시작 ===")
    create_architecture_overview()
    create_commit_process_flow()
    create_pr_process_flow()
    create_security_and_ai_flow()
    print("=== 모든 다이어그램 생성 완료 ===")
