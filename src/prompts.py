"""
커밋 메시지 및 Pull Request(PR) 초안 생성을 위한 프롬프트 엔지니어링 모듈
"""

from typing import Dict, List

COMMIT_SYSTEM_PROMPT = """당신은 실무 표준을 철저히 준수하는 전문 소프트웨어 엔지니어입니다.
제공된 Git diff와 변경된 파일 목록을 분석하여 명확하고 실용적인 Git 커밋 메시지를 작성하세요.

[작성 규칙]
1. 첫 번째 줄은 1줄 커밋 제목으로 작성하세요.
   - 50자 이내를 권장하며, 절대 72자를 초과하지 마세요.
   - Conventional Commits 접두어(feat:, fix:, refactor:, docs:, test:, chore:, style: 중 택1)를 사용하세요.
2. 제목 바로 다음 줄은 반드시 빈 줄(공백 라인)이어야 합니다.
3. 본문은 다음 중 최소 1개 이상을 반드시 충족해야 합니다:
   - 변경된 주요 파일 또는 모듈 1~3개 언급
   - 핵심 변경 사항 1~2개를 불릿('- ')으로 요약
4. 결과물 전체를 마크다운 코드 블록(```)으로 감싸지 말고, 순수한 커밋 메시지 텍스트만 출력하세요.
"""

PR_SYSTEM_PROMPT = """당신은 협업과 코드 리뷰를 위한 완성도 높은 Pull Request(PR) 설명을 작성하는 전문 소프트웨어 엔지니어입니다.
제공된 Git diff와 변경된 파일 목록을 분석하여 PR 제목과 구조화된 본문을 작성하세요.

[작성 규칙]
1. 첫 번째 줄은 1줄 PR 제목으로 작성하세요.
   - 절대 80자를 초과하지 마세요.
   - 간결하고 명확하게 변경 사항을 요약하세요.
2. 제목 바로 다음 줄은 빈 줄이어야 합니다.
3. 본문은 반드시 다음 3가지 섹션 헤더를 정확히 포함해야 합니다:
   ### Why
   ### What
   ### How to Test
4. 각 섹션 아래에는 반드시 최소 1개 이상의 불릿('- ') 항목을 작성하세요:
   - Why: 변경 배경 및 목적
   - What: 핵심 변경 사항 목록
   - How to Test: 동작 확인 및 테스트 방법
5. 결과물 전체를 마크다운 코드 블록(```)으로 감싸지 말고, 마크다운 형식의 순수 텍스트로 출력하세요.
"""


def format_changed_files_summary(changed_files: List[str]) -> str:
    """변경된 파일 목록을 프롬프트용 텍스트로 변환합니다."""
    if not changed_files:
        return "- (변경된 파일 없음)"
    return "\n".join(f"- {f}" for f in changed_files)


def build_commit_prompt(changed_files: List[str], diff_text: str) -> List[Dict[str, str]]:
    """
    커밋 메시지 생성을 위한 OpenAI Chat Completion 메시지 목록을 생성합니다.
    """
    files_summary = format_changed_files_summary(changed_files)
    user_content = (
        f"[변경된 파일 목록]\n{files_summary}\n\n"
        f"[Git Diff 변경 내용]\n{diff_text}\n\n"
        "위 변경 사항을 바탕으로 작성 규칙에 맞추어 1줄 제목과 본문 요약을 포함한 커밋 메시지를 작성해주세요."
    )

    return [
        {"role": "system", "content": COMMIT_SYSTEM_PROMPT.strip()},
        {"role": "user", "content": user_content.strip()}
    ]


def build_pr_prompt(changed_files: List[str], diff_text: str) -> List[Dict[str, str]]:
    """
    PR 제목 및 본문 초안 생성을 위한 OpenAI Chat Completion 메시지 목록을 생성합니다.
    """
    files_summary = format_changed_files_summary(changed_files)
    user_content = (
        f"[변경된 파일 목록]\n{files_summary}\n\n"
        f"[Git Diff 변경 내용]\n{diff_text}\n\n"
        "위 변경 사항을 바탕으로 작성 규칙에 맞추어 80자 이내의 1줄 PR 제목과 Why/What/How to Test 헤더 및 불릿을 포함한 PR 본문을 작성해주세요."
    )

    return [
        {"role": "system", "content": PR_SYSTEM_PROMPT.strip()},
        {"role": "user", "content": user_content.strip()}
    ]
