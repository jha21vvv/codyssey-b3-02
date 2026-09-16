"""
생성된 커밋 메시지 및 PR 초안의 형식을 검증하고 실무 규칙에 맞게 자동 보정(후처리)하는 모듈
"""

import re
from typing import List, Optional, Tuple


def strip_markdown_fences(text: str) -> str:
    """텍스트 앞뒤를 감싸고 있는 마크다운 코드 블록(```)을 제거합니다."""
    text = text.strip()
    if text.startswith("```"):
        # 첫 번째 라인 제거 (``` 또는 ```markdown 등)
        lines = text.splitlines()
        if len(lines) >= 2:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def clean_title(title: str, max_length: int) -> str:
    """제목에서 불필요한 마크다운 기호를 제거하고 최대 길이를 초과할 경우 안전하게 자릅니다."""
    title = title.strip()
    # '# ', '## ' 등 마크다운 헤더 기호 제거
    title = re.sub(r"^#+\s*", "", title)

    if len(title) > max_length:
        title = title[: max_length - 3] + "..."
    return title


def validate_and_fix_commit(
    raw_text: str,
    changed_files: Optional[List[str]] = None
) -> str:
    """
    커밋 메시지 형식 검증 및 후처리:
    - 1줄 제목: 최대 72자 이내로 보정 (50자 권장)
    - 제목과 본문 사이 1줄 공백 보장
    - 본문 요약: 파일 언급 또는 불릿('- ') 1개 이상 포함 보장
    """
    text = strip_markdown_fences(raw_text)
    lines = text.splitlines()

    if not lines:
        title = "chore: 변경 사항 적용"
        body_lines = []
    else:
        title = clean_title(lines[0], max_length=72)
        body_lines = lines[1:]

    # 제목 바로 뒤 빈 줄 처리
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)

    body_text = "\n".join(body_lines).strip()

    # 본문 검증: 불릿('- ' or '* ') 또는 파일 언급 확인
    has_bullet = any(line.strip().startswith(("- ", "* ")) for line in body_lines)
    files = changed_files or []
    mentions_file = any(f in body_text for f in files) if files else False

    # 본문이 비어있거나 품질 기준(불릿 또는 파일 언급)을 충족하지 못할 경우 보충
    if not has_bullet and not mentions_file:
        supplementary = []
        if files:
            target_files = ", ".join(files[:3])
            supplementary.append(f"- 변경된 파일: {target_files}")
        supplementary.append("- 핵심 변경 사항 구현 및 반영")

        if body_text:
            body_text = body_text + "\n" + "\n".join(supplementary)
        else:
            body_text = "\n".join(supplementary)

    return f"{title}\n\n{body_text}"


def validate_and_fix_pr(
    raw_text: str,
    changed_files: Optional[List[str]] = None
) -> str:
    """
    PR 제목 및 본문 템플릿 검증 및 후처리:
    - 1줄 제목: 최대 80자 이내 보정
    - 제목과 본문 사이 공백 보장
    - 필수 3대 섹션 헤더(Why, What, How to Test) 존재 검증 및 자동 보충
    - 각 섹션별 최소 1개 이상의 불릿('- ') 보장
    """
    text = strip_markdown_fences(raw_text)
    lines = text.splitlines()

    if not lines:
        title = "PR: 코드 변경 사항 반영"
        body_lines = []
    else:
        title = clean_title(lines[0], max_length=80)
        body_lines = lines[1:]
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)

    section_patterns = {
        "Why": re.compile(r"(?i)^#*\s*Why\b"),
        "What": re.compile(r"(?i)^#*\s*What\b"),
        "How to Test": re.compile(r"(?i)^#*\s*How to Test\b"),
    }

    sections_content = {sec: [] for sec in section_patterns}
    intro_lines: List[str] = []
    current_sec = None

    for line in body_lines:
        matched_sec = None
        for sec_name, pattern in section_patterns.items():
            if pattern.match(line.strip()):
                matched_sec = sec_name
                break

        if matched_sec:
            current_sec = matched_sec
        elif current_sec:
            sections_content[current_sec].append(line)
        else:
            intro_lines.append(line)

    files = changed_files or []
    default_bullets = {
        "Why": "- 기능 개선 및 요구사항 충족을 위한 코드 변경",
        "What": f"- 주요 파일 변경: {', '.join(files[:3])}" if files else "- 주요 코드 로직 구현 및 리팩토링",
        "How to Test": "- 관련 단위 테스트 실행 및 변경 기능 동작 검증"
    }

    reconstructed: List[str] = []
    if intro_lines and any(l.strip() for l in intro_lines):
        reconstructed.extend([l for l in intro_lines if l.strip()])
        reconstructed.append("")

    for sec in ["Why", "What", "How to Test"]:
        reconstructed.append(f"### {sec}")
        content = sections_content[sec]
        non_empty = [c.strip() for c in content if c.strip()]

        bullets = [c for c in non_empty if c.startswith(("- ", "* "))]
        if bullets:
            for c in non_empty:
                reconstructed.append(c)
        elif non_empty:
            for c in non_empty:
                reconstructed.append(f"- {c}")
        else:
            reconstructed.append(default_bullets[sec])

        reconstructed.append("")

    final_body = "\n".join(reconstructed).strip()
    return f"{title}\n\n{final_body}"

