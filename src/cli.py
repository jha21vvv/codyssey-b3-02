"""
AI 기반 Git 커밋 및 PR 자동 생성기 CLI 인터페이스
"""

import argparse
import sys
from typing import List, Optional

from src.ai_client import AIClient, APIError, ConfigurationError
from src.formatter import format_output
from src.git_client import get_changed_files, get_git_diff, has_changes, is_git_repository
from src.prompts import build_commit_prompt, build_pr_prompt
from src.security import apply_safe_mode
from src.validator import validate_and_fix_commit, validate_and_fix_pr

# Windows 콘솔 한글 깨짐 방지
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def build_parser() -> argparse.ArgumentParser:
    """CLI 명령어 파서를 구성합니다."""
    parser = argparse.ArgumentParser(
        prog="codyssey-ai-git",
        description="Git 변경 사항을 기반으로 AI 커밋 메시지 및 PR 초안을 자동 생성하는 CLI 도구"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="명령어 목록",
        description="실행할 작업을 선택하세요"
    )

    # 1. commit 서브커맨드
    commit_parser = subparsers.add_parser(
        "commit",
        help="Git 변경 사항을 분석하여 커밋 메시지를 자동 생성합니다."
    )
    _add_common_options(commit_parser, default_max_tokens=300)

    # 2. pr 서브커맨드
    pr_parser = subparsers.add_parser(
        "pr",
        help="Git 변경 사항을 분석하여 Pull Request(PR) 제목 및 본문 초안을 자동 생성합니다."
    )
    _add_common_options(pr_parser, default_max_tokens=1000)

    return parser


def _add_common_options(parser: argparse.ArgumentParser, default_max_tokens: int) -> None:
    """서브커맨드 공통 옵션을 추가합니다."""
    parser.add_argument(
        "-m", "--model", "-model",
        type=str,
        default="gpt-4o-mini",
        help="사용할 AI 모델명 (기본값: gpt-4o-mini)"
    )
    parser.add_argument(
        "-t", "--temperature", "-temperature",
        type=float,
        default=0.2,
        help="텍스트 생성 다양성 파라미터 (기본값: 0.2)"
    )
    parser.add_argument(
        "--max-tokens", "-max-tokens",
        type=int,
        default=default_max_tokens,
        help=f"생성할 최대 토큰 수 (기본값: {default_max_tokens})"
    )
    parser.add_argument(
        "--staged", "-staged",
        action="store_true",
        default=False,
        help="스테이징된(staged) 변경 사항만 수집합니다."
    )
    parser.add_argument(
        "--safe-mode", "-safe-mode",
        dest="safe_mode",
        action="store_true",
        default=True,
        help="민감정보 마스킹 및 diff 길이 제한 활성화 (기본값: True)"
    )
    parser.add_argument(
        "--no-safe-mode", "-no-safe-mode",
        dest="safe_mode",
        action="store_false",
        help="안전 모드 비활성화"
    )



def run_commit_pipeline(args: argparse.Namespace, client: Optional[AIClient] = None) -> int:
    """커밋 메시지 자동 생성 파이프라인을 실행합니다."""
    # 1. Git 저장소 유효성 검증
    if not is_git_repository():
        print("[오류] 현재 디렉토리가 Git 저장소가 아닙니다. Git 초기화된 리포지토리에서 실행해주세요.", file=sys.stderr)
        return 1

    # 2. Git 변경 사항 수집
    changed_files = get_changed_files()
    raw_diff = get_git_diff(staged_only=args.staged)

    if not changed_files and not raw_diff.strip():
        print("[안내] 변경 사항이 없습니다. 코드를 수정하거나 git add 후 다시 실행해주세요.")
        return 0

    # 3. 안전 모드(--safe-mode) 필터링
    diff_text = apply_safe_mode(raw_diff, enabled=args.safe_mode)

    # 4. 프롬프트 구성
    messages = build_commit_prompt(changed_files, diff_text)

    # 5. AI API 호출 (단일 호출 원칙)
    ai_client = client or AIClient()
    try:
        raw_response, elapsed = ai_client.generate_completion(
            messages=messages,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
    except ConfigurationError as e:
        print(f"[설정 오류] {str(e)}", file=sys.stderr)
        return 1
    except APIError as e:
        print(f"[API 오류] {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[실행 오류] 처리 중 예외가 발생했습니다: {str(e)}", file=sys.stderr)
        return 1

    # 6. 형식 검증 및 후처리
    fixed_commit = validate_and_fix_commit(raw_response, changed_files=changed_files)

    # 7. 출력 포맷팅
    meta = {
        "call_count": ai_client.call_count,
        "elapsed": elapsed,
        "model": args.model,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "safe_mode": args.safe_mode
    }
    formatted = format_output(title="커밋 메시지 초안", content=fixed_commit, meta=meta)
    print(formatted)
    return 0


def run_pr_pipeline(args: argparse.Namespace, client: Optional[AIClient] = None) -> int:
    """Pull Request 초안 자동 생성 파이프라인을 실행합니다."""
    # 1. Git 저장소 유효성 검증
    if not is_git_repository():
        print("[오류] 현재 디렉토리가 Git 저장소가 아닙니다. Git 초기화된 리포지토리에서 실행해주세요.", file=sys.stderr)
        return 1

    # 2. Git 변경 사항 수집
    changed_files = get_changed_files()
    raw_diff = get_git_diff(staged_only=args.staged)

    if not changed_files and not raw_diff.strip():
        print("[안내] 변경 사항이 없습니다. 코드를 수정하거나 git add 후 다시 실행해주세요.")
        return 0

    # 3. 안전 모드(--safe-mode) 필터링
    diff_text = apply_safe_mode(raw_diff, enabled=args.safe_mode)

    # 4. 프롬프트 구성
    messages = build_pr_prompt(changed_files, diff_text)

    # 5. AI API 호출 (단일 호출 원칙)
    ai_client = client or AIClient()
    try:
        raw_response, elapsed = ai_client.generate_completion(
            messages=messages,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
    except ConfigurationError as e:
        print(f"[설정 오류] {str(e)}", file=sys.stderr)
        return 1
    except APIError as e:
        print(f"[API 오류] {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[실행 오류] 처리 중 예외가 발생했습니다: {str(e)}", file=sys.stderr)
        return 1

    # 6. 형식 검증 및 후처리
    fixed_pr = validate_and_fix_pr(raw_response, changed_files=changed_files)

    # 7. 출력 포맷팅
    meta = {
        "call_count": ai_client.call_count,
        "elapsed": elapsed,
        "model": args.model,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "safe_mode": args.safe_mode
    }
    formatted = format_output(title="Pull Request 초안", content=fixed_pr, meta=meta)
    print(formatted)
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """CLI 메인 함수"""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "commit":
        return run_commit_pipeline(args)
    elif args.command == "pr":
        return run_pr_pipeline(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
