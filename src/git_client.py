"""
Git 상태 및 변경 사항(diff)을 수집하는 클라이언트 모듈
"""

import os
import subprocess
from typing import List, Optional


def run_git_command(args: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
    """Git 명령을 실행하고 완료된 프로세스 객체를 반환합니다."""
    working_dir = cwd or os.getcwd()
    return subprocess.run(
        ["git", "-c", "core.quotepath=false"] + args,
        cwd=working_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )


def is_git_repository(cwd: Optional[str] = None) -> bool:
    """현재 디렉토리가 Git 저장소 루트 또는 내부에 위치하는지 확인합니다."""
    result = run_git_command(["rev-parse", "--is-inside-work-tree"], cwd=cwd)
    return result.returncode == 0 and result.stdout.strip() == "true"


def get_git_root(cwd: Optional[str] = None) -> Optional[str]:
    """Git 저장소의 최상위 루트 디렉토리 경로를 반환합니다."""
    result = run_git_command(["rev-parse", "--show-toplevel"], cwd=cwd)
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def get_changed_files(cwd: Optional[str] = None) -> List[str]:
    """
    git status --porcelain 결과를 파싱하여 변경, 추가, 삭제된 파일 목록을 반환합니다.
    """
    result = run_git_command(["status", "--porcelain"], cwd=cwd)
    if result.returncode != 0:
        return []

    changed_files = []
    for line in result.stdout.splitlines():
        trimmed = line.strip()
        if not trimmed:
            continue
        # status 포맷: XY PATH 또는 XY ORIG_PATH -> NEW_PATH
        # 첫 2자는 상태 코드(X: index, Y: work tree), 3번째 자리는 공백
        parts = line[3:].strip()
        if " -> " in parts:
            # 파일 이름 변경(rename)의 경우 변경된 대상 파일 추출
            parts = parts.split(" -> ")[1].strip()
        if parts.startswith('"') and parts.endswith('"'):
            parts = parts[1:-1]
        if parts:
            changed_files.append(parts)

    return changed_files


def get_git_diff(staged_only: bool = False, cwd: Optional[str] = None) -> str:
    """
    git diff 결과를 수집합니다.
    - staged_only=True: git diff --cached (스테이징된 변경사항)
    - staged_only=False: staged 및 unstaged 변경사항을 모두 수집 (staged 우선 및 결합)
    """
    if staged_only:
        res_staged = run_git_command(["diff", "--cached"], cwd=cwd)
        return res_staged.stdout if res_staged.returncode == 0 else ""

    # staged 변경사항 확인
    res_staged = run_git_command(["diff", "--cached"], cwd=cwd)
    staged_diff = res_staged.stdout if res_staged.returncode == 0 else ""

    # unstaged 변경사항 확인
    res_unstaged = run_git_command(["diff"], cwd=cwd)
    unstaged_diff = res_unstaged.stdout if res_unstaged.returncode == 0 else ""

    diffs = []
    if staged_diff.strip():
        diffs.append(staged_diff.strip())
    if unstaged_diff.strip():
        diffs.append(unstaged_diff.strip())

    return "\n\n".join(diffs)


def has_changes(cwd: Optional[str] = None) -> bool:
    """
    변경 사항(수정된 파일 또는 diff 내용)이 존재하는지 확인합니다.
    """
    files = get_changed_files(cwd=cwd)
    diff = get_git_diff(cwd=cwd)
    return bool(files or diff.strip())
