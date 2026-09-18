# [1차]: Git 클라이언트 모듈의 성격과 역할을 기술하는 다중 라인 모듈 독스트링의 시작입니다.
# [2차]: "이 파일은 Git과 대화하는 전담 통역사입니다"라는 팻말을 겁니다.
"""
# [1차]: Git 상태 및 변경 사항(diff)을 수집하는 클라이언트 모듈임을 정의합니다.
# [2차]: 개발자가 코드를 고치고 나면 "어디를 얼마나 고쳤니?" 하고 Git에게 물어봐 주는 척척박사입니다.
Git 상태 및 변경 사항(diff)을 수집하는 클라이언트 모듈
# [1차]: 모듈 독스트링을 닫는 삼중 따옴표입니다.
# [2차]: 설명 팻말을 닫습니다.
"""

# [1차]: 운영체제 환경 및 현재 작업 디렉토리 경로 조회를 위해 os 모듈을 임포트합니다.
# [2차]: 내가 지금 컴퓨터의 어느 폴더에 서 있는지 확인하기 위한 나침반을 꺼냅니다.
import os
# [1차]: 외부 시스템 프로세스(git CLI)를 파이썬 하위 프로세스로 실행하기 위해 subprocess 모듈을 임포트합니다.
# [2차]: 파이썬이 까만색 터미널 창을 몰래 하나 열어서 대신 키보드를 두드릴 수 있는 손가락 로봇을 가져옵니다.
import subprocess
# [1차]: 정적 타입 힌팅을 위해 typing 표준 모듈에서 List와 Optional을 임포트합니다.
# [2차]: "결과물은 파일 이름들의 목록(List)이야"라고 자료형을 표기하기 위한 라벨 도구입니다.
from typing import List, Optional


# [1차]: 임의의 Git 명령 인자(args)를 받아 서브프로세스로 실행하고 완료 객체를 반환하는 래퍼 함수 선언부입니다.
# [2차]: "Git 심부름꾼 나와라!" 하고 부르는 핵심 심부름꾼 함수입니다.
def run_git_command(args: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
    # [1차]: 함수의 기능과 목적을 설명하는 한 줄 독스트링입니다.
    # [2차]: 함수 설명서입니다.
    """Git 명령을 실행하고 완료된 프로세스 객체를 반환합니다."""
    # [1차]: 호출자가 디렉토리(cwd)를 전달하지 않았으면 현재 작업 디렉토리(os.getcwd())를 기본 작업 폴더로 지정합니다.
    # [2차]: "어느 폴더에서 git 명령 칠까?" 물어봤는데 아무 말도 안 했으면(None), 그냥 지금 내가 서 있는 폴더에서 실행합니다.
    working_dir = cwd or os.getcwd()
    # [1차]: subprocess.run을 호출하여 git 프로세스를 동기 실행하고 CompletedProcess 객체를 반환합니다.
    # [2차]: 파이썬 손가락 로봇이 실제로 터미널에 글자를 탁탁탁 치고 엔터를 누르는 순간입니다.
    return subprocess.run(
        # [1차]: 명령어 목록 맨 앞에 한글 파일명 깨짐을 방지하는 Git 설정 옵션("-c core.quotepath=false")을 강제 주입하고 세부 인자를 결합합니다.
        # [2차]: Git은 기본적으로 한글 파일명을 외계어로 바꿔 출력하는데, "한글 그대로 똑바로 읽어라!"라는 특수 안경을 씌워주는 필수 옵션입니다.
        # 마이: -c"이번 한 번만 임시로 설정 바꿔줘!"  core Git의 설정 카테고리 중 '기본 시스템' 영역  
        # quotepath-false 터미널이 깨질까 봐 글자 모양을 지우고, 컴퓨터 부품 번호표(바이트 코드)를 대신 적어두는 옵션을 끈다는 말
        ["git", "-c", "core.quotepath=false"] + args,
        # [1차]: 프로세스가 실행될 기준 작업 디렉토리를 지정합니다.
        # [2차]: "이 폴더 안으로 직접 걸어 들어가서 실행해라" 하고 일터 주소를 알려줍니다.
        cwd=working_dir,
        # [1차]: 프로세스의 표준 출력(stdout)과 표준 에러(stderr)를 파이썬 메모리로 캡처하도록 설정합니다.
        # [2차]: 터미널 화면에 결과 글자가 그냥 날아가지 않도록 파이썬 바구니로 낚아챕니다.
        capture_output=True,
        # [1차]: 캡처된 바이트(bytes) 출력을 문자열(str)로 자동 디코딩하도록 지시합니다.
        # [2차]: 0과 1 컴퓨터 이진수 데이터를 우리가 읽을 수 있는 사람의 글자로 자동 번역해 달라는 옵션입니다.
        text=True,
        # [1차]: 표준 인코딩을 UTF-8로 강제하여 한글 및 다국어 텍스트의 손실 없는 처리를 보장합니다.
        # [2차]: 한국어 글자가 깨져서 네모(□)나 물음표(?)로 나오지 않도록 UTF-8 한글 폰트 규격을 지정합니다.
        encoding="utf-8",
        # [1차]: 인코딩 변환 불가능한 특이 바이트 발생 시 프로세스 중단 없이 대체 문자('?')로 치환하도록 설정합니다.
        # [2차]: 도중에 이상한 외계 글자가 한 글자 섞여 있어도 프로그램이 에러를 내며 뻗지 않고 유연하게 넘어가게 해주는 방패입니다.
        errors="replace"
    # [1차]: subprocess.run 호출 괄호를 닫습니다.
    # [2차]: 명령어 발송 완료.
    )


# [1차]: 현재 디렉토리가 Git 워크트리 내부인지 불리언(True/False)으로 판별하는 함수 선언부입니다.
# [2차]: "여기가 Git 프로젝트 폴더 맞나요?" 하고 입구에서 확인해 주는 문지기 검사관 함수입니다.
def is_git_repository(cwd: Optional[str] = None) -> bool:
    # [1차]: 함수의 목적을 명시한 Docstring입니다.
    # [2차]: 함수 설명서입니다.
    """현재 디렉토리가 Git 저장소 루트 또는 내부에 위치하는지 확인합니다."""
    # [1차]: git rev-parse --is-inside-work-tree 명령을 실행하여 현재 위치가 작업 트리 내부인지 질의합니다.
    # [2차]: Git에게 "지금 너 일하는 작업실(Work-tree) 안에 들어와 있는 거 맞니?"라고 공식 질문을 던집니다.
    result = run_git_command(["rev-parse", "--is-inside-work-tree"], cwd=cwd)
    # [1차]: 반환 코드가 0(정상 종료)이고 표준 출력이 "true"인 경우에만 True를 반환합니다.
    # [2차]: Git이 에러 없이(returncode == 0) "응, 맞아!(true)"라고 확실히 대답했을 때만 진짜 Git 폴더로 인정해 줍니다.
    return result.returncode == 0 and result.stdout.strip() == "true"


# [1차]: Git 저장소의 최상위 루트 디렉토리 절대경로를 반환하는 함수 선언부입니다.
# [2차]: "이 Git 건물의 1층 로비(루트 폴더)가 어디야?" 하고 건물 주소를 물어보는 함수입니다.
def get_git_root(cwd: Optional[str] = None) -> Optional[str]:
    # [1차]: 함수의 목적을 명시한 Docstring입니다.
    # [2차]: 함수 설명서입니다.
    """Git 저장소의 최상위 루트 디렉토리 경로를 반환합니다."""
    # [1차]: git rev-parse --show-toplevel 명령을 실행하여 최상위 루트 경로를 조회합니다.
    # [2차]: Git에게 "너의 가장 꼭대기 보금자리 폴더 경로를 보여줘"라고 조회합니다.
    # 마이: 깃에서 변동사항등을 체크할때 제일위에서해야 전부 반영되니 만든것
    result = run_git_command(["rev-parse", "--show-toplevel"], cwd=cwd)
    # [1차]: 프로세스가 성공적으로 완료된 경우(returncode == 0)를 검사합니다.
    # [2차]: 주소를 정상적으로 알아왔는지 체크합니다.
    if result.returncode == 0:
        # [1차]: 공백 및 줄바꿈을 제거한 순수 절대경로 문자열을 반환합니다.
        # [2차]: 알아온 주소 뒤에 붙은 쓸데없는 줄바꿈을 털어내고 깨끗한 폴더 주소를 건넵니다.
        #마이: stdout 터미널 까만 화면에 정상적으로 찍힌 글자 텍스트
        return result.stdout.strip()
    # [1차]: Git 저장소가 아니거나 실행 실패 시 None을 반환합니다.
    # [2차]: Git 폴더가 아니라서 주소를 못 찾았으면 "없어요(None)"라고 알려줍니다.
    return None


# [1차]: 변경, 추가, 삭제된 파일 목록을 문자열 리스트로 반환하는 get_changed_files 함수의 선언부입니다.
# [2차]: "오늘 내가 어떤 파일들을 건드렸지?" 하고 수정한 파일 이름 목록을 받아오는 함수입니다.
def get_changed_files(cwd: Optional[str] = None) -> List[str]:
    # [1차]: 함수의 동작을 설명하는 Docstring의 시작입니다.
    # [2차]: 설명서 엽니다.
    """
    # [1차]: git status --porcelain 결과를 기계적으로 파싱하여 변경된 파일 목록을 추출함을 기술합니다.
    # [2차]: 사람이 보기 좋은 문구 대신 컴퓨터가 읽기 좋게 규격화된 상태 표를 읽어온다고 설명합니다.
    git status --porcelain 결과를 파싱하여 변경, 추가, 삭제된 파일 목록을 반환합니다.
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 닫기.
    """
    # [1차]: git status --porcelain 명령을 실행합니다.
    # [2차]: Git에게 "사람 보라고 꾸미지 말고, 군더더기 싹 뺀 날것의 상태 목록을 줘!"라고 요청합니다.
    result = run_git_command(["status", "--porcelain"], cwd=cwd)
    # [1차]: 명령 실행에 실패한 경우 안전하게 빈 리스트([])를 반환하여 에러 전파를 차단합니다.
    # [2차]: 조회가 실패했으면 프로그램이 죽지 않고 조용히 "아무 파일도 없어요([])" 하고 빈 바구니를 줍니다.
    if result.returncode != 0:
        return []

    # [1차]: 파싱 완료된 파일 경로들을 순서대로 담을 빈 리스트를 생성합니다.
    # [2차]: 고친 파일 이름들을 적어둘 메모지를 한 장 꺼냅니다.
    changed_files = []
    # [1차]: status 출력 문자열을 줄 단위로 쪼개어(splitlines) 한 라인씩 반복 순회합니다.
    # [2차]: 상태 표에 적힌 변경 목록을 위에서부터 한 줄씩 눈으로 읽어 내려갑니다.
    for line in result.stdout.splitlines():
        # [1차]: 한 라인의 좌우 공백 문자를 제거합니다.
        # [2차]: 글자 양옆의 여백을 털어냅니다.
        trimmed = line.strip()
        # [1차]: 빈 줄인 경우 파싱할 내용이 없으므로 다음 라인으로 건너뜁니다.
        # [2차]: 아무 글자도 없는 빈 줄이면 무시하고 다음 줄을 봅니다.
        if not trimmed:
            continue
        # [1차]: 상태 코드 2자리와 공백 1자리를 건너뛰고 순수 파일 경로 문자열(line[3:])만 슬라이싱합니다.
        # [2차]: "M  src/cli.py"에서 앞의 상태 딱지("M  ")를 칼로 떼어내고 순수 파일 이름("src/cli.py")만 챙깁니다.
        parts = line[3:].strip()
        # [1차]: 파일 이름 변경(rename) 표기인 화살표(" -> ")의 포함 여부를 검사합니다.
        # [2차]: 파일 이름 변경(개명)인지 확인합니다.
        if " -> " in parts:
            # [1차]: 화살표를 기준으로 분할하여 변경 후의 최종 대상 파일 경로([1])만 추출합니다.
            # [2차]: 개명 전 옛날 이름은 버리고, 지금 살아있는 "새 이름"만 골라냅니다.
            parts = parts.split(" -> ")[1].strip()
        # [1차]: 공백이 포함된 파일명에 붙는 앞뒤 큰따옴표의 존재 여부를 검사합니다.
        # [2차]: 파일 이름에 공백이 있어서 따옴표로 포장되어 있는지 확인합니다.
        if parts.startswith('"') and parts.endswith('"'):
            # [1차]: 슬라이싱(parts[1:-1])을 통해 앞뒤 큰따옴표를 벗겨냅니다.
            # [2차]: 포장용 따옴표 껍질을 훌러덩 벗겨냅니다.
            parts = parts[1:-1]
        # [1차]: 정제된 파일 경로 문자열이 유효하게 존재하는지 검사합니다.
        # [2차]: 정상적인 파일 이름이 맞는지 확인합니다.
        if parts:
            # [1차]: 최종 파일 경로를 changed_files 결과 리스트에 추가합니다.
            # [2차]: 메모지에 고친 파일 이름을 꾹 눌러 적습니다.
            changed_files.append(parts)

    # [1차]: 수집된 변경 파일 경로 리스트를 호출자에게 반환합니다.
    # [2차]: 완성된 변경 파일 목록 메모지를 건넵니다.
    return changed_files


# [1차]: Git diff 텍스트를 수집하는 get_git_diff 함수의 선언부입니다.
# [2차]: "어떤 코드가 추가되고 지워졌는지 구체적인 코드 영수증을 싹 긁어와라!"라고 시키는 함수입니다.
def get_git_diff(staged_only: bool = False, cwd: Optional[str] = None) -> str:
    # [1차]: 함수의 동작 및 옵션별(staged_only) 동작 모드를 설명하는 Docstring의 시작입니다.
    # [2차]: 설명서 시작.
    """
    # [1차]: diff 수집 규칙(staged 우선 조회 및 unstaged 결합)을 기술합니다.
    # [2차]: staged만 볼 것인지, 파일 수정한 것 전체를 다 볼 것인지 옵션 안내입니다.
    git diff 결과를 수집합니다.
    - staged_only=True: git diff --cached (스테이징된 변경사항)
    - staged_only=False: staged 및 unstaged 변경사항을 모두 수집 (staged 우선 및 결합)
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 끝.
    """
    # [1차]: 호출자가 staged_only=True로 지정한 경우의 조건문입니다.
    # [2차]: "난 `git add` 해둔 장바구니 품목만 커밋할 거야!"라고 지정했을 때입니다.
    if staged_only:
        # [1차]: git diff --cached 명령을 실행하여 스테이징된 변경사항만 조회합니다.
        # [2차]: 장바구니(`git add`)에 들어있는 변경 내용만 Git에게 물어봅니다.
        res_staged = run_git_command(["diff", "--cached"], cwd=cwd)
        # [1차]: 명령 성공 시 diff 출력을, 실패 시 빈 문자열을 반환합니다.
        # [2차]: 성공했으면 그 diff 영수증을 돌려주고 실패했으면 빈손으로 돌아갑니다.
        return res_staged.stdout if res_staged.returncode == 0 else ""

    # [1차]: staged_only가 False일 때, 우선 staged 변경사항을 먼저 조회합니다.
    # [2차]: 전체 조회의 경우: 1단계로 장바구니에 담긴 변경점부터 먼저 확인합니다.
    res_staged = run_git_command(["diff", "--cached"], cwd=cwd)
    # [1차]: 명령 성공 시 스테이징 diff를 취하고, 실패 시 빈 문자열을 취합니다.
    # [2차]: 장바구니 영수증을 챙깁니다.
    staged_diff = res_staged.stdout if res_staged.returncode == 0 else ""

    # [1차]: 2단계로 작업 트리 내 unstaged 변경사항(git diff)을 조회합니다.
    # [2차]: 2단계로 아직 장바구니에 안 담고 책상 위에 꺼내둔(unstaged) 변경점도 확인합니다.
    res_unstaged = run_git_command(["diff"], cwd=cwd)
    # [1차]: 명령 성공 시 unstaged diff를 취하고, 실패 시 빈 문자열을 취합니다.
    # [2차]: 책상 위 영수증을 챙깁니다.
    unstaged_diff = res_unstaged.stdout if res_unstaged.returncode == 0 else ""

    # [1차]: 수집된 diff 토막들을 순서대로 담을 리스트를 초기화합니다.
    # [2차]: 두 영수증을 합치기 위한 편지 봉투입니다.
    diffs = []
    # [1차]: 스테이징된 diff에 유효한 텍스트가 존재하는지 검사합니다.
    # [2차]: 장바구니 영수증 내용이 있으면 봉투에 쏙 넣습니다.
    if staged_diff.strip():
        # [1차]: 양쪽 여백을 정돈한 staged diff를 리스트에 추가합니다.
        # [2차]: 장바구니 내용을 봉투에 넣습니다.
        diffs.append(staged_diff.strip())
    # [1차]: 작업 트리의 unstaged diff에 유효한 텍스트가 존재하는지 검사합니다.
    # [2차]: 책상 위 영수증 내용도 있으면 봉투에 이어 넣습니다.
    if unstaged_diff.strip():
        # [1차]: 양쪽 여백을 정돈한 unstaged diff를 리스트에 추가합니다.
        # [2차]: 책상 위 내용을 봉투에 넣습니다.
        diffs.append(unstaged_diff.strip())

    # [1차]: 두 diff 블록을 2개의 줄바꿈("\n\n")으로 연결하여 통합 문자열을 반환합니다.
    # [2차]: 두 영수증 사이에 줄바꿈 두 칸을 띄워서 보기 좋게 붙인 뒤 AI에게 넘겨줄 거대한 코드 diff 종이를 건넵니다.
    return "\n\n".join(diffs)


# [1차]: 작업 트리에 커밋 대상 변경사항이 존재하는지 불리언으로 반환하는 has_changes 함수 선언부입니다.
# [2차]: "고친 거 진짜 있어? 헛걸음하는 거 아니지?" 하고 최종 점검해 주는 확인 도장 함수입니다.
def has_changes(cwd: Optional[str] = None) -> bool:
    # [1차]: 함수의 역할을 설명하는 Docstring입니다.
    # [2차]: 설명서입니다.
    """
    # [1차]: 변경 사항(수정된 파일 또는 diff 내용)이 존재하는지 확인함을 기술합니다.
    # [2차]: 변경점이 하나라도 있는지 체크한다는 설명입니다.
    변경 사항(수정된 파일 또는 diff 내용)이 존재하는지 확인합니다.
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 닫기.
    """
    # [1차]: 변경된 파일 목록을 조회합니다.
    # [2차]: 고친 파일 목록을 받아옵니다.
    files = get_changed_files(cwd=cwd)
    # [1차]: 코드 변경 diff 문자열을 조회합니다.
    # [2차]: 고친 코드 내용물을 받아옵니다.
    diff = get_git_diff(cwd=cwd)
    # [1차]: 파일 목록이 비어있지 않거나, diff 텍스트에 공백이 아닌 문자가 존재하면 True를 반환합니다.
    # [2차]: 파일 이름이 적혀 있거나, 코드 영수증 글자가 단 한 글자라도 적혀 있으면 "일거리 있음(True)"을 반환하고, 둘 다 텅 비었으면 "일거리 없음(False)"을 반환합니다.
    return bool(files or diff.strip())
