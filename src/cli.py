# [1차]: CLI 진입점 모듈의 역할을 기술하는 다중 라인 모듈 독스트링의 시작입니다.
# [2차]: "이 파일은 사용자가 터미널에서 명령을 내렸을 때 가장 먼저 출동하는 총사령탑 본부입니다"라는 현판입니다.
"""
# [1차]: AI 기반 Git 커밋 및 PR 자동 생성기 CLI 인터페이스 모듈임을 명시합니다.
# [2차]: 터미널에서 사용자의 입력을 받아 모든 부품(Git, 보안, AI, 검증, 포매터)을 한 줄로 엮어 실행하는 지휘관입니다.
AI 기반 Git 커밋 및 PR 자동 생성기 CLI 인터페이스
# [1차]: 모듈 독스트링을 닫는 삼중 따옴표입니다.
# [2차]: 현판 닫기.
"""

# [1차]: 터미널 명령어 및 옵션 플래그 파싱을 위해 argparse 표준 라이브러리를 임포트합니다.
# [2차]: 사용자가 터미널에 친 복잡한 옵션들(--model, --safe-mode 등)을 파이썬이 알아먹기 좋게 숟가락으로 떠먹여 주는 번역기입니다.
import argparse
# [1차]: 경로 검증 및 파일 시스템 확인을 위해 os 표준 라이브러리를 임포트합니다.
# [2차]: 폴더가 실제로 있는지, 파일이 존재하는지 컴퓨터 지도를 확인하는 내비게이션 도구입니다.
import os
# [1차]: 표준 입출력 스트림(stdout, stderr) 제어 및 종료 코드(sys.exit) 반환을 위해 sys 모듈을 임포트합니다.
# [2차]: 컴퓨터 화면에 글자를 띄우거나 프로그램을 정상/비정상 종료시키는 운영체제 소통 창구입니다.
import sys
# [1차]: 타입 어노테이션을 위해 typing 모듈에서 List와 Optional을 임포트합니다.
# [2차]: 매개변수와 반환값의 형태를 명확히 적어두기 위한 라벨표입니다.
from typing import List, Optional

# [1차]: AI 호출 클라이언트 및 커스텀 예외 클래스들을 ai_client 모듈에서 임포트합니다.
# [2차]: AI에게 전화를 걸어줄 비서와 에러 안내원들을 불러옵니다.
from src.ai_client import AIClient, APIError, ConfigurationError
# [1차]: 최종 결과를 규격화된 박스로 꾸며줄 format_output 함수를 formatter 모듈에서 임포트합니다.
# [2차]: 글자를 예쁜 액자 상자로 포장해 주는 선물 디자이너를 데려옵니다.
from src.formatter import format_output
# [1차]: Git 저장소 검사 및 diff 수집 함수들을 git_client 모듈에서 임포트합니다.
# [2차]: Git 저장소인지 확인하고 코드 변경점을 수집해 올 Git 일꾼들을 부릅니다.
from src.git_client import get_changed_files, get_git_diff, has_changes, is_git_repository
# [1차]: 커밋 및 PR용 프롬프트 생성 함수들을 prompts 모듈에서 임포트합니다.
# [2차]: AI에게 건넬 질문지를 전문적으로 써주는 작가들을 모셔옵니다.
from src.prompts import build_commit_prompt, build_pr_prompt
# [1차]: 민감정보 마스킹 및 diff 길이 절삭 함수를 security 모듈에서 임포트합니다.
# [2차]: 비밀번호를 먹칠하고 너무 긴 글을 가위로 잘라줄 보안 요원을 배치합니다.
from src.security import apply_safe_mode
# [1차]: 커밋 및 PR 응답 품질 검증 및 자동 보정 함수들을 validator 모듈에서 임포트합니다.
# [2차]: AI가 써온 글의 맞춤법과 양식을 칼같이 교정해 주는 검사관들을 배치합니다.
from src.validator import validate_and_fix_commit, validate_and_fix_pr

# [1차]: 윈도우 환경 콘솔에서 한글 출력이 깨지는 현상을 방지하기 위한 조건문입니다.
# [2차]: 윈도우 컴퓨터에서 한글이 외계어로 깨져 나오는 고질병을 고치기 위한 백신 주사입니다.
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    # [1차]: 표준 출력 스트림 인코딩 재설정 중 예외를 대비하는 try 블록입니다.
    # [2차]: 인코딩 바꾸다가 문제 생겨도 프로그램이 멈추지 않게 감싸는 안전장치입니다.
    try:
        # [1차]: 표준 출력(stdout)의 인코딩을 UTF-8로 재구성합니다.
        # [2차]: 일반 안내 화면 통로를 한글 안 깨지는 UTF-8 모드로 전환합니다.
        sys.stdout.reconfigure(encoding="utf-8")
        # [1차]: 표준 에러(stderr)의 인코딩을 UTF-8로 재구성합니다.
        # [2차]: 빨간색 에러 화면 통로도 한글 안 깨지게 UTF-8로 맞춥니다.
        sys.stderr.reconfigure(encoding="utf-8")
    # [1차]: 인코딩 재설정 실패 시 조용히 넘어갑니다.
    # [2차]: 실패해도 그냥 넘어갑니다.
    except Exception:
        pass


# [1차]: CLI 명령어 파서 구조를 정의하고 생성하는 build_parser 함수 선언부입니다.
# [2차]: "터미널 명령 규칙판 만들기" 작업을 시작하는 설계 함수입니다.
def build_parser() -> argparse.ArgumentParser:
    # [1차]: 함수의 목적을 명시한 한 줄 독스트링입니다.
    # [2차]: 함수 설명서입니다.
    """CLI 명령어 파서를 구성합니다."""
    # [1차]: 프로그램 이름(prog)과 전체 설명을 지정하여 메인 ArgumentParser 객체를 생성합니다.
    # [2차]: "codyssey-ai-git"이라는 이름의 메인 명령 접수 창구를 터미널에 개설합니다.
    parser = argparse.ArgumentParser(
        prog="codyssey-ai-git",
        description="Git 변경 사항을 기반으로 AI 커밋 메시지 및 PR 초안을 자동 생성하는 CLI 도구"
    )

    # [1차]: 서브커맨드(commit, pr) 분기를 위한 서브파서 관리 객체를 추가합니다.
    # [2차]: 손님이 'commit'을 할지 'pr'을 할지 골라 탈 수 있는 2갈래 선택 길(분기점)을 만듭니다.
    subparsers = parser.add_subparsers(
        dest="command",
        title="명령어 목록",
        description="실행할 작업을 선택하세요"
    )

    # [1차]: commit 서브커맨드를 위한 전용 서브파서를 등록합니다.
    # [2차]: 1번 창구: "커밋 메시지 만들어주세요" 전용 신청 데스크를 엽니다.
    commit_parser = subparsers.add_parser(
        "commit",
        help="Git 변경 사항을 분석하여 커밋 메시지를 자동 생성합니다."
    )
    # [1차]: 커밋 서브파서에 공통 옵션들을 부여하며 최대 토큰 기본값을 300으로 설정합니다.
    # [2차]: 커밋 창구에 공통 옵션들을 붙여주고, 글자 수는 300토큰(짧은 요약)으로 맞춥니다.
    _add_common_options(commit_parser, default_max_tokens=300)

    # [1차]: pr 서브커맨드를 위한 전용 서브파서를 등록합니다.
    # [2차]: 2번 창구: "Pull Request 초안 써주세요" 전용 신청 데스크를 엽니다.
    pr_parser = subparsers.add_parser(
        "pr",
        help="Git 변경 사항을 분석하여 Pull Request(PR) 제목 및 본문 초안을 자동 생성합니다."
    )
    # [1차]: PR 서브파서에 공통 옵션을 부여하며 본문이 길므로 최대 토큰 기본값을 1000으로 설정합니다.
    # [2차]: PR 창구에 공통 옵션들을 붙여주고, PR은 긴 글이어야 하니 1000토큰으로 넉넉히 줍니다.
    _add_common_options(pr_parser, default_max_tokens=1000)

    # [1차]: 구성 완료된 최상위 파서 객체를 반환합니다.
    # [2차]: 완성된 명령 규칙판을 출하합니다.
    return parser


# [1차]: 각 서브커맨드에 공통으로 필요한 옵션 플래그들을 주입하는 헬퍼 함수 선언부입니다.
# [2차]: 각 창구마다 공통 양식 스티커(--model, --temperature 등)를 찰떡같이 붙여주는 도우미입니다.
def _add_common_options(parser: argparse.ArgumentParser, default_max_tokens: int) -> None:
    # [1차]: 함수의 목적을 명시한 한 줄 독스트링입니다.
    # [2차]: 설명서입니다.
    """서브커맨드 공통 옵션을 추가합니다."""
    # [1차]: 모델명 옵션을 등록하며 단축(-m), 표준(--model), 단일 대시(-model) 별칭을 모두 지원합니다.
    # [2차]: "AI 모델 뭐 쓸래?" 옵션을 붙입니다. -m, --model, -model 모두 찰떡같이 알아듣습니다.
    parser.add_argument(
        "-m", "--model", "-model",
        type=str,
        default="gpt-4o-mini",
        help="사용할 AI 모델명 (기본값: gpt-4o-mini)"
    )
    # [1차]: 생성 창의성/다양성(temperature) 옵션을 부동소수점 타입(float)으로 등록합니다.
    # [2차]: "AI가 얼마나 차분하게 쓸지(0.0) 아니면 톡톡 튈지(1.0)"를 조절하는 온도계 옵션입니다.
    parser.add_argument(
        "-t", "--temperature", "-temperature",
        type=float,
        default=0.2,
        help="텍스트 생성 다양성 파라미터 (기본값: 0.2)"
    )
    # [1차]: 최대 생성 토큰 수(max-tokens) 옵션을 정수형(int)으로 등록합니다.
    # [2차]: "최대 몇 글자(토큰)까지 쓸래?" 한도 옵션입니다.
    parser.add_argument(
        "--max-tokens", "-max-tokens",
        type=int,
        default=default_max_tokens,
        help=f"생성할 최대 토큰 수 (기본값: {default_max_tokens})"
    )
    # [1차]: 스테이징된 변경사항만 수집할지 여부를 지정하는 불리언 플래그(--staged)를 등록합니다.
    # [2차]: "git add 해둔 것만 골라서 커밋할래?" 스위치입니다.
    parser.add_argument(
        "--staged", "-staged",
        action="store_true",
        default=False,
        help="스테이징된(staged) 변경 사항만 수집합니다."
    )
    # [1차]: 보안 마스킹 및 크기 절삭을 활성화하는 --safe-mode 플래그를 등록합니다 (기본값 True).
    # [2차]: "비밀번호 먹칠 검사 켜기!" 안전 스위치입니다 (기본으로 켜져 있어 안전합니다).
    parser.add_argument(
        "--safe-mode", "-safe-mode",
        dest="safe_mode",
        action="store_true",
        default=True,
        help="민감정보 마스킹 및 diff 길이 제한 활성화 (기본값: True)"
    )
    # [1차]: 안전 모드를 비활성화할 수 있는 --no-safe-mode 반대 플래그를 등록합니다.
    # [2차]: "난 보안 검사 끄고 날것 그대로 보낼래" 스위치입니다.
    parser.add_argument(
        "--no-safe-mode", "-no-safe-mode",
        dest="safe_mode",
        action="store_false",
        help="안전 모드 비활성화"
    )
    # [1차]: 대상 Git 저장소 경로를 지정하는 -r, --repo, -C 옵션을 등록합니다 (기본값: None, 현재 디렉토리).
    # [2차]: "어느 프로젝트 폴더의 변경점을 읽어올까?" 원격 조준 스위치를 달아줍니다.
    parser.add_argument(
        "-r", "--repo", "-C",
        dest="repo",
        type=str,
        default=None,
        help="분석할 대상 Git 저장소 디렉토리 경로 (기본값: 현재 디렉토리)"
    )


# [1차]: 커밋 메시지 자동 생성 파이프라인 전체를 1~7단계로 순차 지휘하는 함수 선언부입니다.
# [2차]: 공장의 컨베이어 벨트 총책임자로서, 재료 수집부터 완제품 출력까지 1번~7번 일꾼을 차례로 지휘합니다.
def run_commit_pipeline(args: argparse.Namespace, client: Optional[AIClient] = None) -> int:
    # [1차]: 함수의 목적을 명시한 한 줄 독스트링입니다.
    # [2차]: 설명서입니다.
    """커밋 메시지 자동 생성 파이프라인을 실행합니다."""
    # [1차]: 대상 Git 저장소 경로를 확인하고 정규화합니다.
    # [2차]: 사용자가 옵션으로 지정한 폴더가 있는지 확인하고 절대 경로로 바꿉니다.
    target_repo = os.path.abspath(args.repo) if getattr(args, "repo", None) else None

    # [1차]: 대상 디렉토리가 실제로 존재하는지 유효성을 검사합니다.
    # [2차]: 손님이 지정한 폴더가 컴퓨터에 진짜 있는지 확인합니다.
    if target_repo and not os.path.isdir(target_repo):
        print(f"[오류] 지정한 저장소 경로가 존재하지 않거나 디렉토리가 아닙니다: {args.repo}", file=sys.stderr)
        return 1

    # [1차]: 1단계: 대상 폴더가 유효한 Git 저장소인지 검증합니다.
    # [2차]: 1단계 문지기 일꾼: "여기가 Git 작업실 맞나요?" 확인합니다.
    if not is_git_repository(cwd=target_repo):
        # [1차]: Git 저장소가 아닌 경우 표준 에러(sys.stderr)로 에러 메시지를 출력합니다.
        # [2차]: Git 폴더가 아니면 빨간색 경고등을 켜고 안내문을 출력합니다.
        if target_repo:
            print(f"[오류] 지정한 디렉토리가 Git 저장소가 아닙니다: {target_repo}", file=sys.stderr)
        else:
            print("[오류] 현재 디렉토리가 Git 저장소가 아닙니다. Git 초기화된 리포지토리에서 실행해주세요.", file=sys.stderr)
        # [1차]: 비정상 종료 코드 1을 반환합니다.
        # [2차]: 컴퓨터에게 "에러로 끝났음(1)"을 알리고 멈춥니다.
        return 1

    # [1차]: 2단계: 변경된 파일 목록을 수집합니다.
    # [2차]: 2단계 수집 일꾼: 오늘 수정한 파일 목록을 받아옵니다.
    changed_files = get_changed_files(cwd=target_repo)
    # [1차]: args.staged 설정에 맞추어 코드 변경 diff 문자열을 수집합니다.
    # [2차]: 구체적으로 몇 번째 줄이 바뀌었는지 코드 영수증을 긁어옵니다.
    raw_diff = get_git_diff(staged_only=args.staged, cwd=target_repo)

    # [1차]: 변경된 파일도 없고 diff 내용도 공백인 경우를 검사합니다.
    # [2차]: 고친 게 하나도 없는데 실수로 프로그램을 켰는지 확인합니다.
    if not changed_files and not raw_diff.strip():
        # [1차]: 변경 사항이 없음을 표준 출력으로 안내합니다.
        # [2차]: "고친 게 없으니 코드 먼저 고치고 오세요"라고 친절히 안내합니다.
        print("[안내] 변경 사항이 없습니다. 코드를 수정하거나 git add 후 다시 실행해주세요.")
        # [1차]: AI 호출 비용을 낭비하지 않고 정상 종료 코드 0으로 안전하게 종료합니다.
        # [2차]: 비싼 AI에게 전화 걸지 않고 0원 지출로 기분 좋게 끝냅니다.
        return 0

    # [1차]: 3단계: 안전 모드 설정에 따라 민감정보 마스킹 및 크기 제한을 적용합니다.
    # [2차]: 3단계 보안 일꾼: 비밀번호와 API 키에 먹칠하고 너무 긴 글을 자릅니다.
    diff_text = apply_safe_mode(raw_diff, enabled=args.safe_mode)

    # [1차]: 4단계: 수집된 파일과 diff를 바탕으로 커밋 생성용 OpenAI 메시지 목록을 조립합니다.
    # [2차]: 4단계 작가 일꾼: AI에게 보낼 "커밋 메시지 주문서" 질문지를 작성합니다.
    # 마이: 이 부분이 깃에서 git add . 치면 추가되는 변한 내용들 모으는것
    #마이: 새로 만든 파일(새파일.py)은 diff에 아예 안 나와서 파일명을 따로 받아가는거임.
    #마이: ai의 이해를 돕기위해 바뀐 파일들을 줘서 커밋 메시니의 윤곽을 잡으려고
    messages = build_commit_prompt(changed_files, diff_text)

    # [1차]: 5단계: 주입받은 client가 있으면 사용하고, 없으면 기본 AIClient 인스턴스를 생성합니다.
    # [2차]: 5단계 통신 일꾼: 테스트용 가짜 AI가 있으면 그걸 쓰고, 없으면 진짜 OpenAI 통신 비서를 부릅니다.
    ai_client = client or AIClient()
    # [1차]: AI API 호출 중 발생 가능한 예외를 포착하는 try 블록입니다.
    # [2차]: 국제전화 거는 동안 통신 장애가 생길까 봐 대비하는 그물망입니다.
    try:
        # [1차]: generate_completion을 호출하여 AI로부터 (응답본문, 소요시간)을 수신합니다.
        # [2차]: 미국 서버로 전화를 걸어 1회 호출 원칙으로 멋진 답변을 받아 적고 스톱워치를 끕니다.
        # 마이: elapsed는 걸린 시간 기록
        raw_response, elapsed = ai_client.generate_completion(
            messages=messages,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
    # [1차]: API 키 누락 등 설정 오류 발생 시의 예외 처리입니다.
    # [2차]: API 키 안 넣었을 때 친절한 해결책을 띄우고 종료합니다.
    except ConfigurationError as e:
        print(f"[설정 오류] {str(e)}", file=sys.stderr)
        return 1
    # [1차]: HTTP 401, 429 등 네트워크/API 통신 오류 발생 시의 예외 처리입니다.
    # [2차]: 인증 실패나 크레딧 부족 등 구체적 원인을 짚어주고 종료합니다.
    except APIError as e:
        print(f"[API 오류] {str(e)}", file=sys.stderr)
        return 1
    # [1차]: 기타 예상치 못한 모든 런타임 오류를 가로챕니다.
    # [2차]: 돌발 에러가 나도 터미널이 흉하게 깨지지 않게 예쁘게 에러를 찍고 종료합니다.
    except Exception as e:
        print(f"[실행 오류] 처리 중 예외가 발생했습니다: {str(e)}", file=sys.stderr)
        return 1

    # [1차]: 6단계: AI 응답의 첫 줄을 72자 이내 제목으로 다듬고 본문 불릿 품질을 보증합니다.
    # [2차]: 6단계 검사관 일꾼: AI가 써온 글에서 불필요한 백틱(```)을 떼고, 글자 수와 불릿을 완벽히 맞춤 교정합니다.
    fixed_commit = validate_and_fix_commit(raw_response, changed_files=changed_files)

    # [1차]: 7단계: 출력 박스 하단에 표시할 실행 통계 메타데이터 딕셔너리를 구성합니다.
    # [2차]: 7단계 포장 일꾼: 호출 횟수, 걸린 시간, 모델명 영수증을 챙깁니다.
    meta = {
        "call_count": ai_client.call_count,
        "elapsed": elapsed,
        "model": args.model,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "safe_mode": args.safe_mode,
        "repo": target_repo or os.getcwd()
    }
    # [1차]: format_output을 호출하여 터미널용 액자 박스 문자열을 생성합니다.
    # [2차]: 예쁜 테두리 액자에 결과물과 영수증을 담아 포장합니다.
    formatted = format_output(title="커밋 메시지 초안", content=fixed_commit, meta=meta)
    # [1차]: 완성된 결과물을 콘솔 화면에 출력합니다.
    # [2차]: 손님(개발자) 앞에 완성된 멋진 결과물을 딱 내려놓습니다.
    print(formatted)
    # [1차]: 전체 파이프라인이 성공적으로 완수되었음을 알리는 종료 코드 0을 반환합니다.
    # [2차]: "성공적으로 완벽하게 끝났습니다(0)!" 도장을 찍습니다.
    return 0


# [1차]: Pull Request 초안 자동 생성 파이프라인 전체를 지휘하는 함수 선언부입니다.
# [2차]: PR 생성 공장의 컨베이어 벨트 총책임자입니다.
def run_pr_pipeline(args: argparse.Namespace, client: Optional[AIClient] = None) -> int:
    # [1차]: 함수의 목적을 명시한 한 줄 독스트링입니다.
    # [2차]: 설명서입니다.
    """Pull Request 초안 자동 생성 파이프라인을 실행합니다."""
    # [1차]: 대상 Git 저장소 경로를 확인하고 정규화합니다.
    # [2차]: 사용자가 옵션으로 지정한 폴더가 있는지 확인하고 절대 경로로 바꿉니다.
    target_repo = os.path.abspath(args.repo) if getattr(args, "repo", None) else None

    # [1차]: 대상 디렉토리가 실제로 존재하는지 유효성을 검사합니다.
    # [2차]: 손님이 지정한 폴더가 컴퓨터에 진짜 있는지 확인합니다.
    if target_repo and not os.path.isdir(target_repo):
        print(f"[오류] 지정한 저장소 경로가 존재하지 않거나 디렉토리가 아닙니다: {args.repo}", file=sys.stderr)
        return 1

    # [1차]: 1단계: 현재 폴더 또는 지정된 대상의 Git 저장소 유효성을 검사합니다.
    # [2차]: 1단계: Git 폴더인지 확인합니다.
    if not is_git_repository(cwd=target_repo):
        # [1차]: 비저장소일 경우 표준 에러 출력 후 종료합니다.
        # [2차]: 에러 경고문을 띄우고 중단합니다.
        if target_repo:
            print(f"[오류] 지정한 디렉토리가 Git 저장소가 아닙니다: {target_repo}", file=sys.stderr)
        else:
            print("[오류] 현재 디렉토리가 Git 저장소가 아닙니다. Git 초기화된 리포지토리에서 실행해주세요.", file=sys.stderr)
        return 1

    # [1차]: 2단계: 변경 파일 목록과 코드 diff를 수집합니다.
    # [2차]: 2단계: 고친 파일과 코드 영수증을 모아옵니다.
    changed_files = get_changed_files(cwd=target_repo)
    raw_diff = get_git_diff(staged_only=args.staged, cwd=target_repo)

    # [1차]: 변경 사항이 전무한 경우를 검사합니다.
    # [2차]: 고친 게 없는지 확인합니다.
    if not changed_files and not raw_diff.strip():
        # [1차]: 사용자에게 안내 메시지를 출력하고 비용 지출 없이 종료합니다.
        # [2차]: 헛걸음하지 않게 안내하고 0원 지출로 끝냅니다.
        print("[안내] 변경 사항이 없습니다. 코드를 수정하거나 git add 후 다시 실행해주세요.")
        return 0

    # [1차]: 3단계: 안전 모드를 통해 민감정보 마스킹 및 크기를 절삭합니다.
    # [2차]: 3단계: 비밀번호 먹칠 및 서류 크기 다이어트를 합니다.
    diff_text = apply_safe_mode(raw_diff, enabled=args.safe_mode)

    # [1차]: 4단계: PR 초안 생성을 위한 질문지(messages)를 조립합니다.
    # [2차]: 4단계: Why/What/How to Test를 포함하라는 질문 편지를 작성합니다.
    messages = build_pr_prompt(changed_files, diff_text)

    # [1차]: 5단계: AIClient 인스턴스를 준비합니다.
    # [2차]: 5단계: AI 비서를 호출합니다.
    ai_client = client or AIClient()
    # [1차]: API 호출 예외를 포착하는 try 블록입니다.
    # [2차]: 통신 안전망입니다.
    try:
        # [1차]: AI API를 단 1회 호출하여 PR 본문과 소요 시간을 수신합니다.
        # [2차]: 1회 호출 원칙으로 미국 서버에 전화 걸어 PR 초안을 받아 적습니다.
        raw_response, elapsed = ai_client.generate_completion(
            messages=messages,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
    # [1차]: 설정 누락 예외 처리입니다.
    # [2차]: API 키 누락 안내입니다.
    except ConfigurationError as e:
        print(f"[설정 오류] {str(e)}", file=sys.stderr)
        return 1
    # [1차]: HTTP 및 API 에러 처리입니다.
    # [2차]: API 오류 안내입니다.
    except APIError as e:
        print(f"[API 오류] {str(e)}", file=sys.stderr)
        return 1
    # [1차]: 기타 모든 예외 처리입니다.
    # [2차]: 기타 오류 안내입니다.
    except Exception as e:
        print(f"[실행 오류] 처리 중 예외가 발생했습니다: {str(e)}", file=sys.stderr)
        return 1

    # [1차]: 6단계: 80자 제목 및 Why, What, How to Test 3대 헤더와 불릿을 검증 및 자동 보충합니다.
    # [2차]: 6단계: 사내 표준 PR 양식에 부합하도록 누락된 헤더나 불릿을 완벽히 AS 교정합니다.
    fixed_pr = validate_and_fix_pr(raw_response, changed_files=changed_files)

    # [1차]: 7단계: 실행 메타데이터 딕셔너리를 구성합니다.
    # [2차]: 7단계: 작업 영수증을 작성합니다.
    meta = {
        "call_count": ai_client.call_count,
        "elapsed": elapsed,
        "model": args.model,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "safe_mode": args.safe_mode,
        "repo": target_repo or os.getcwd()
    }
    # [1차]: format_output으로 완성된 액자형 출력 문자열을 생성합니다.
    # [2차]: 예쁜 상자에 PR 초안과 영수증을 담습니다.
    formatted = format_output(title="Pull Request 초안", content=fixed_pr, meta=meta)
    # [1차]: 콘솔 화면에 출력합니다.
    # [2차]: 개발자에게 결과물을 선보입니다.
    print(formatted)
    # [1차]: 정상 종료 코드 0을 반환합니다.
    # [2차]: 성공 종료(0) 도장을 찍습니다.
    return 0


# [1차]: CLI 실행의 최상위 진입점인 main 함수 선언부입니다. argv 인자로 커스텀 입력을 받을 수 있습니다.
# [2차]: 프로그램이 시작될 때 문을 열고 들어오는 현관문 함수입니다.
def main(argv: Optional[List[str]] = None) -> int:
    # [1차]: 함수의 역할을 설명하는 한 줄 독스트링입니다.
    # [2차]: 설명서입니다.
    """CLI 메인 함수"""
    # [1차]: build_parser를 호출하여 명령 파서를 준비합니다.
    # [2차]: 명령 규칙판을 세웁니다.
    parser = build_parser()
    # [1차]: 명령줄 인자들을 파싱하여 Namespace 객체(args)에 바인딩합니다.
    # [2차]: 손님이 친 명령어 글자들을 가방(args)에 착착 정리해 담습니다.
    args = parser.parse_args(argv)

    # [1차]: 서브커맨드(commit 또는 pr)를 입력하지 않은 경우를 검사합니다.
    # [2차]: 아무 명령도 안 치고 프로그램 이름만 쳤는지 봅니다.
    if not args.command:
        # [1차]: 도움말을 출력합니다.
        # [2차]: "사용법 안내 책자"를 보여줍니다.
        parser.print_help()
        # [1차]: 사용법 미숙지로 종료 코드 1을 반환합니다.
        # [2차]: 1을 반환하며 멈춥니다.
        return 1

    # [1차]: 사용자가 'commit' 서브커맨드를 선택한 경우의 분기입니다.
    # [2차]: 손님이 "커밋 메시지 만들어줘"를 선택했을 때입니다.
    if args.command == "commit":
        # [1차]: 커밋 파이프라인을 실행하고 그 반환 코드를 그대로 돌려줍니다.
        # [2차]: 커밋 공장을 가동합니다.
        return run_commit_pipeline(args)
    # [1차]: 사용자가 'pr' 서브커맨드를 선택한 경우의 분기입니다.
    # [2차]: 손님이 "PR 초안 써줘"를 선택했을 때입니다.
    elif args.command == "pr":
        # [1차]: PR 파이프라인을 실행하고 그 반환 코드를 돌려줍니다.
        # [2차]: PR 공장을 가동합니다.
        return run_pr_pipeline(args)
    # [1차]: 기타 알 수 없는 서브커맨드가 들어온 경우입니다.
    # [2차]: 엉뚱한 명령을 입력했을 때입니다.
    else:
        # [1차]: 도움말을 출력합니다.
        # [2차]: 사용법을 보여줍니다.
        parser.print_help()
        # [1차]: 종료 코드 1을 반환합니다.
        # [2차]: 1을 돌려줍니다.
        return 1


# [1차]: 파이썬 스크립트가 모듈로 임포트되지 않고 직접 터미널에서 실행되었을 때만 main()을 수행하도록 하는 진입 가드 구문입니다.
# [2차]: "이 파이썬 파일을 터미널에서 직접 실행했을 때만 대장 함수(main)를 실행해라!"라는 출발 신호등입니다.
if __name__ == "__main__":
    # [1차]: main() 함수의 반환 코드를 전달하여 시스템 프로세스를 종료합니다.
    # [2차]: 대장 함수의 성공(0) 또는 실패(1) 결과를 운영체제에 전하며 깔끔하게 퇴근합니다.
    sys.exit(main())
