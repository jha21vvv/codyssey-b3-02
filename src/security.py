"""
민감 정보 마스킹 및 diff 길이/파일 수 제한을 처리하는 보안 모듈 (--safe-mode)
"""

import re
from typing import List, Tuple

# 민감정보 정규식 패턴 및 대체 텍스트 목록
SENSITIVE_PATTERNS = [
    # 1. Private Key 블록
    (re.compile(r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----[\s\S]*?-----END (?:[A-Z ]+)?PRIVATE KEY-----"), "[REDACTED_PRIVATE_KEY]"),
    # 2. OpenAI API Key (sk-...)
    (re.compile(r"\bsk-[a-zA-Z0-9]{20,}\b"), "[REDACTED_API_KEY]"),
    # 3. Anthropic API Key (sk-ant-...)
    (re.compile(r"\bsk-ant-[a-zA-Z0-9_\-]{20,}\b"), "[REDACTED_API_KEY]"),
    # 4. GitHub Personal Access Token (ghp_..., gho_..., 등)
    (re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,}\b"), "[REDACTED_GITHUB_TOKEN]"),
    # 5. AWS Access Key ID (AKIA...)
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED_AWS_KEY]"),
    # 6. 이메일 주소
    (re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"), "[REDACTED_EMAIL]"),
    # 7. 설정값/할당문 내 secret, password, api_key, token 값 마스킹 (이미 마스킹된 [REDACTED_...]는 건너뜀)
    (re.compile(r'(?i)(["\']?(?:api[_\-]?key|secret|token|password|auth[_\-]?token)["\']?\s*[:=]\s*["\'])(?!\[REDACTED_)([^"\']{4,})(["\'])'), r"\1[REDACTED_SECRET]\3"),
]


def mask_sensitive_data(text: str) -> str:
    """
    텍스트 내에 포함된 민감 정보(API 키, 토큰, 비밀번호, 이메일 등)를 감지하여 마스킹합니다.
    """
    if not text:
        return text

    masked = text
    for pattern, replacement in SENSITIVE_PATTERNS:
        masked = pattern.sub(replacement, masked)

    return masked


def truncate_diff(diff_text: str, max_files: int = 10, max_lines: int = 200) -> str:
    """
    diff 텍스트의 크기를 제한합니다.
    - 최대 파일 수(max_files, 기본 10개) 초과 시 절삭
    - 최대 라인 수(max_lines, 기본 200줄) 초과 시 절삭
    """
    if not diff_text:
        return ""

    lines = diff_text.splitlines()

    # 1. 파일 단위 절삭 (diff --git 헤더 기준)
    file_indices: List[int] = []
    for idx, line in enumerate(lines):
        if line.startswith("diff --git "):
            file_indices.append(idx)

    total_files = len(file_indices)
    file_truncated = False
    files_omitted = 0

    if total_files > max_files:
        cutoff_line = file_indices[max_files]
        files_omitted = total_files - max_files
        lines = lines[:cutoff_line]
        file_truncated = True

    # 2. 라인 수 단위 절삭
    total_lines = len(lines)
    line_truncated = False
    if total_lines > max_lines:
        lines = lines[:max_lines]
        line_truncated = True

    result = "\n".join(lines)

    # 절삭 안내 메시지 추가
    notices = []
    if file_truncated:
        notices.append(f"... [diff truncated by safe-mode: 최대 {max_files}개 파일 초과 (외 {files_omitted}개 파일 생략)]")
    if line_truncated:
        notices.append(f"... [diff truncated by safe-mode: 최대 {max_lines}줄 초과 (전체 {total_lines}줄 중 {max_lines}줄만 전송)]")

    if notices:
        result += "\n\n" + "\n".join(notices)

    return result


def apply_safe_mode(
    diff_text: str,
    enabled: bool = True,
    max_files: int = 10,
    max_lines: int = 200
) -> str:
    """
    --safe-mode 파이프라인을 실행합니다.
    enabled가 True일 때 민감정보 마스킹 및 파일/라인 절삭을 차례로 적용합니다.
    """
    if not enabled or not diff_text:
        return diff_text

    # 1단계: 민감 정보 마스킹
    masked = mask_sensitive_data(diff_text)

    # 2단계: 파일 및 라인 수 절삭
    truncated = truncate_diff(masked, max_files=max_files, max_lines=max_lines)

    return truncated
