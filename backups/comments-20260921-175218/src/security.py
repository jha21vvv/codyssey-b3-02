# [1차]: 보안 마스킹 모듈의 성격과 역할을 기술하는 다중 라인 모듈 독스트링의 시작입니다.
# [2차]: "이 파일은 코드가 인터넷 세상 밖으로 나가기 전에 위험한 비밀이 묻어있는지 몸수색하는 보안 검색대입니다"라고 알리는 팻말입니다.
"""
# [1차]: 민감 정보 마스킹 및 diff 길이/파일 수 제한을 처리하는 모듈(--safe-mode)임을 명시합니다.
# [2차]: API 키 유출로 몇 백만 원 요금 폭탄을 맞지 않도록 사전에 지켜주는 안전 금고 역할을 설명합니다.
민감 정보 마스킹 및 diff 길이/파일 수 제한을 처리하는 보안 모듈 (--safe-mode)
# [1차]: 모듈 독스트링을 닫는 삼중 따옴표입니다.
# [2차]: 팻말 닫기.
"""

# [1차]: 문자열 패턴 매칭 및 치환을 위해 파이썬 내장 정규표현식(re) 모듈을 임포트합니다.
# [2차]: "sk-..."로 시작하는 비밀 키나 이메일 주소처럼 특정한 규칙을 가진 글자들을 귀신같이 찾아내는 돋보기를 챙깁니다.
import re
# [1차]: 정적 타입 검사를 위해 typing 모듈에서 List와 Tuple을 임포트합니다.
# [2차]: (정규식 패턴, 바꿀 문자열) 쌍들의 목록임을 표기하기 위한 라벨 도구입니다.
from typing import List, Tuple

# [1차]: 민감정보 정규식 패턴과 이를 대체할 마스킹 텍스트 튜플 목록을 전역 상수로 선언합니다.
# [2차]: 공항 검색대에 붙어있는 "기내 반입 금지 물품 도감(칼, 폭발물, 가위...)" 목록입니다.
SENSITIVE_PATTERNS = [
    # [1차]: RSA, SSH 등 Private Key 블록(BEGIN/END)을 감지하여 [REDACTED_PRIVATE_KEY]로 치환하는 정규식 패턴입니다.
    # [2차]: 서버의 최고 비밀 인증서가 코드에 적혀 있으면 그 문단 전체를 새까만 마커펜으로 칠해버립니다.
    # 마이: 나중에 검색하기 좋도록 문자열 형식을 다듬어둬서 그에 맞는 문자열을 빠르게 찾으려는것
    (re.compile(r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----[\s\S]*?-----END (?:[A-Z ]+)?PRIVATE KEY-----"), "[REDACTED_PRIVATE_KEY]"),
    # [1차]: sk- 접두어로 시작하는 20자 이상의 OpenAI API 키 형식을 감지하여 [REDACTED_API_KEY]로 치환합니다.
    # [2차]: OpenAI 유료 비밀 키("sk-abc1234...")가 발견되면 즉시 "[REDACTED_API_KEY]" 스티커를 딱 붙여 가립니다.
    (re.compile(r"\bsk-[a-zA-Z0-9]{20,}\b"), "[REDACTED_API_KEY]"),
    # [1차]: sk-ant- 접두어로 시작하는 Anthropic Claude API 키 형식을 감지하여 [REDACTED_API_KEY]로 치환합니다.
    # [2차]: Claude AI 서비스의 비밀 키도 발견 즉시 가려줍니다.
    (re.compile(r"\bsk-ant-[a-zA-Z0-9_\-]{20,}\b"), "[REDACTED_API_KEY]"),
    # [1차]: ghp_, gho_ 등 36자 이상의 GitHub Personal Access Token 형식을 감지하여 [REDACTED_GITHUB_TOKEN]으로 치환합니다.
    # [2차]: 깃허브 계정을 털어갈 수 있는 깃허브 출입증(토큰)을 발견하면 모자이크 처리합니다.
    (re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,}\b"), "[REDACTED_GITHUB_TOKEN]"),
    # [1차]: AKIA 접두어로 시작하는 16자리 영숫자의 AWS Access Key ID를 감지하여 [REDACTED_AWS_KEY]로 치환합니다.
    # [2차]: 아마존 클라우드 열쇠가 노출되어 채굴 서버로 악용당하지 않게 마스킹합니다.
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED_AWS_KEY]"),
    # [1차]: 일반적인 이메일 주소(user@domain.com) 패턴을 감지하여 [REDACTED_EMAIL]로 치환합니다.
    # [2차]: 개인정보인 개발자의 이메일 주소("dev@gmail.com")를 가려줍니다.
    (re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"), "[REDACTED_EMAIL]"),
    # [1차]: key, secret, password 등의 할당문에서 실제 값만 [REDACTED_SECRET]으로 치환하되 기 마스킹된 값은 건너뛰는 전방부정 정규식입니다.
    # [2차]: 코드에서 `password = "123456"` 처럼 적어둔 줄이 있으면, 변수명은 두고 실제 암호값("123456")만 쏙 빼서 `[REDACTED_SECRET]`으로 덮어씁니다.
    (re.compile(r'(?i)(["\']?(?:api[_\-]?key|secret|token|password|auth[_\-]?token)["\']?\s*[:=]\s*["\'])(?!\[REDACTED_)([^"\']{4,})(["\'])'), r"\1[REDACTED_SECRET]\3"),
# [1차]: SENSITIVE_PATTERNS 리스트 정의를 닫습니다.
# [2차]: 금지 물품 도감 완성.
]


# [1차]: 텍스트 내 민감 정보를 마스킹 치환하는 mask_sensitive_data 함수의 선언부입니다.
# [2차]: 서류를 검색대에 집어넣으면 위험한 단어들에 먹칠을 싹 해주는 '자동 검열 롤러기'입니다.
def mask_sensitive_data(text: str) -> str:
    # [1차]: 함수의 목적을 설명하는 Docstring의 시작입니다.
    # [2차]: 설명서 시작.
    """
    # [1차]: 텍스트 내 API 키, 비밀번호 등을 감지하여 안전하게 치환함을 기술합니다.
    # [2차]: 설명입니다.
    텍스트 내에 포함된 민감 정보(API 키, 토큰, 비밀번호, 이메일 등)를 감지하여 마스킹합니다.
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 끝.
    """
    # [1차]: 입력 텍스트가 None이거나 빈 문자열인 경우 처리 없이 그대로 반환합니다.
    # [2차]: 빈 종이가 들어오면 검열할 것도 없으니 그냥 돌려보냅니다.
    if not text:
        return text

    # [1차]: 원본 문자열을 보존하고 치환 결과를 누적하기 위해 masked 변수에 복사합니다.
    # [2차]: 원본 서류의 복사본을 작업대에 올려놓습니다.
    masked = text
    # [1차]: SENSITIVE_PATTERNS 목록의 (패턴, 대체문자열) 튜플을 차례로 순회합니다.
    # [2차]: 1번 위험물(개인키)부터 7번 위험물(비밀번호)까지 차례차례 도장을 쥐고 서류를 훑어봅니다.
    for pattern, replacement in SENSITIVE_PATTERNS:
        # [1차]: 정규표현식 sub 메소드로 일치하는 모든 위험 텍스트를 마스킹 텍스트로 치환합니다.
        # [2차]: 위험한 글자를 발견할 때마다 먹칠 도장을 쾅쾅 찍어 바꿉니다.
        # 마이: 패턴에 해당되는 형식이 마스크에서 발견되면 리플레이스로 바꾸는 구조.
        masked = pattern.sub(replacement, masked)

    # [1차]: 모든 패턴 마스킹이 완료된 안전한 텍스트를 반환합니다.
    # [2차]: 먹칠이 완벽하게 끝난 안전한 서류를 돌려줍니다.
    return masked


# [1차]: diff 텍스트의 파일 수 및 라인 수를 제한하여 초과분을 잘라내는 truncate_diff 함수 선언부입니다.
# [2차]: diff가 너무 두꺼우면 책이 무거워서 날아가지 못하니, 딱 읽을 수 있는 만큼만 남기고 잘라내는 '종이 절단기'입니다.
def truncate_diff(diff_text: str, max_files: int = 10, max_lines: int = 200) -> str:
    # [1차]: 함수의 목적과 절삭 정책을 설명하는 Docstring의 시작입니다.
    # [2차]: 설명서 시작.
    """
    # [1차]: 파일 수(기본 10개) 및 줄 수(기본 200줄) 제한 규칙을 기술합니다.
    # [2차]: 자르는 기준 한도 설명입니다.
    diff 텍스트의 크기를 제한합니다.
    - 최대 파일 수(max_files, 기본 10개) 초과 시 절삭
    - 최대 라인 수(max_lines, 기본 200줄) 초과 시 절삭
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 끝.
    """
    # [1차]: 빈 텍스트인 경우 빈 문자열을 반환합니다.
    # [2차]: 자를 종이가 없으면 빈 종이로 끝냅니다.
    if not diff_text:
        return ""

    # [1차]: 텍스트를 줄 단위로 분할하여 문자열 리스트로 변환합니다.
    # [2차]: 여러 장의 서류를 한 줄씩 낱장으로 분리합니다.
    lines = diff_text.splitlines()

    # [1차]: 각 파일의 diff 시작 헤더("diff --git ")가 위치한 라인 인덱스들을 저장할 리스트입니다.
    # [2차]: "어디서부터 새로운 파일이 시작되는지 페이지 번호를 체크하자"라는 뜻입니다.
    file_indices: List[int] = []
    # [1차]: 전체 줄을 라인 번호(idx)와 함께 순회합니다.
    # [2차]: 서류 1줄부터 끝 줄까지 줄 번호를 매기며 읽어 내려갑니다.
    for idx, line in enumerate(lines):
        # [1차]: 해당 줄이 "diff --git "으로 시작하는지(새 파일의 diff 시작점인지) 검사합니다.
        # [2차]: "새로운 파일 등장!" 깃발을 발견하면 그 줄 번호를 메모장에 적어둡니다.
        if line.startswith("diff --git "):
            # [1차]: 파일 시작 라인 인덱스를 리스트에 추가합니다.
            # [2차]: 줄 번호를 메모장에 추가합니다.
            file_indices.append(idx)

    # [1차]: diff에 포함된 총 파일 개수를 산출합니다.
    # [2차]: 총 몇 개의 파일을 건드렸는지 깃발 개수를 셉니다.
    total_files = len(file_indices)
    # [1차]: 파일 단위 절삭 발생 여부 플래그를 False로 초기화합니다.
    # [2차]: "파일 수가 너무 많아서 잘라냈는가?" 체크용 스티커입니다.
    file_truncated = False
    # [1차]: 한도 초과로 생략된 파일 개수를 0으로 초기화합니다.
    # [2차]: 버려진 파일이 몇 개인지 기록할 숫자입니다.
    files_omitted = 0

    # [1차]: 발견된 파일 수가 허용 최대 파일 수(max_files)를 초과하는지 검사합니다.
    # [2차]: "고친 파일이 10개가 넘어?" 하고 묻는 조건문입니다.
    if total_files > max_files:
        # [1차]: 허용 한도 다음 파일의 시작 라인 인덱스를 절삭 기준점(cutoff_line)으로 지정합니다.
        # [2차]: 딱 10번째 파일까지만 살리고, 11번째 파일이 시작되는 줄에 작두 칼을 댑니다.
        cutoff_line = file_indices[max_files]
        # [1차]: 생략된 파일 개수를 계산합니다.
        # [2차]: "13개 중 10개만 살렸으니 3개는 생략되었네"라고 뺄셈합니다.
        files_omitted = total_files - max_files
        # [1차]: cutoff_line 이전까지만 슬라이싱하여 lines 리스트를 자릅니다.
        # [2차]: 칼로 싹둑 잘라서 10개 파일 내용만 손에 남깁니다.
        lines = lines[:cutoff_line]
        # [1차]: 파일 절삭 플래그를 True로 설정합니다.
        # [2차]: "파일 수 잘라냈음!" 스티커를 붙입니다.
        file_truncated = True

    # [1차]: 1단계 절삭 후 남아있는 총 라인 수를 계산합니다.
    # [2차]: 파일 수를 줄였으니, 이제 전체 줄 수가 200줄을 넘는지 검사하러 갑니다.
    total_lines = len(lines)
    # [1차]: 라인 절삭 플래그를 False로 초기화합니다.
    # [2차]: 라인 절삭 체크 스티커입니다.
    line_truncated = False
    # [1차]: 현재 라인 수가 최대 허용 라인 수(max_lines)를 초과하는지 검사합니다.
    # [2차]: 10개 파일만 남겼는데도 200줄이 넘는지 봅니다.
    if total_lines > max_lines:
        # [1차]: 정확히 max_lines 번째 줄까지만 슬라이싱하여 자릅니다.
        # [2차]: 200줄 뒤는 과감하게 칼로 잘라냅니다.
        lines = lines[:max_lines]
        # [1차]: 라인 절삭 플래그를 True로 설정합니다.
        # [2차]: "줄 수 잘라냈음!" 스티커를 붙입니다.
        line_truncated = True

    # [1차]: 남아있는 라인들을 개행 문자로 합쳐 문자열로 재구성합니다.
    # [2차]: 자르고 남은 종이들을 다시 테이프로 붙여 하나로 만듭니다.
    result = "\n".join(lines)

    # [1차]: 절삭 안내 문구들을 담을 리스트를 초기화합니다.
    # [2차]: "주의: 내용이 너무 길어서 일부 생략되었습니다"라는 안내문을 담을 바구니입니다.
    notices = []
    # [1차]: 파일 단위 절삭이 발생한 경우 안내 메시지를 작성합니다.
    # [2차]: "최대 10개 파일을 초과해서 나머지 파일은 생략했습니다"라는 안내 쪽지를 작성합니다.
    if file_truncated:
        notices.append(f"... [diff truncated by safe-mode: 최대 {max_files}개 파일 초과 (외 {files_omitted}개 파일 생략)]")
    # [1차]: 라인 단위 절삭이 발생한 경우 안내 메시지를 작성합니다.
    # [2차]: "최대 200줄을 넘어서 200줄까지만 AI에게 보냅니다"라는 안내 쪽지를 작성합니다.
    if line_truncated:
        notices.append(f"... [diff truncated by safe-mode: 최대 {max_lines}줄 초과 (전체 {total_lines}줄 중 {max_lines}줄만 전송)]")

    # [1차]: 안내 메시지가 존재하는 경우 결과 텍스트 맨 뒤에 결합합니다.
    # [2차]: 서류 맨 밑에 주의사항 쪽지를 딱 풀로 붙입니다.
    if notices:
        result += "\n\n" + "\n".join(notices)

    # [1차]: 크기 제한 처리가 완료된 diff 텍스트를 반환합니다.
    # [2차]: 적당한 크기로 다이어트가 끝난 건강한 diff 종이를 돌려줍니다.
    return result


# [1차]: 보안 안전 모드의 전체 파이프라인(마스킹 및 절삭)을 순차 실행하는 apply_safe_mode 함수 선언부입니다.
# [2차]: "보안팀 총출동!" 버튼을 누르면 먹칠(마스킹)과 절단(크기제한)을 한 번에 원스톱으로 처리해 주는 메인 게이트웨이입니다.
def apply_safe_mode(
    diff_text: str,
    enabled: bool = True,
    max_files: int = 10,
    max_lines: int = 200
) -> str:
    # [1차]: 함수의 기능과 흐름을 설명하는 Docstring의 시작입니다.
    # [2차]: 설명서 시작.
    """
    # [1차]: enabled가 True일 때 마스킹과 크기 절삭을 차례로 적용함을 기술합니다.
    # [2차]: 원스톱 보안 처리 안내입니다.
    --safe-mode 파이프라인을 실행합니다.
    enabled가 True일 때 민감정보 마스킹 및 파일/라인 절삭을 차례로 적용합니다.
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 끝.
    """
    # [1차]: 안전 모드가 비활성화되어 있거나 diff 내용이 없는 경우 원본 텍스트를 즉시 반환합니다.
    # [2차]: "보안 검사 안 할래요"라고 했거나 검사할 서류가 아예 없으면 그냥 하이패스로 통과시킵니다.
    if not enabled or not diff_text:
        return diff_text

    # [1차]: 1단계: 민감 정보 마스킹 함수를 호출하여 API 키와 비밀번호를 치환합니다.
    # [2차]: 1단계: 비밀번호와 API 키에 새까만 마커칠을 먼저 합니다.
    masked = mask_sensitive_data(diff_text)
    # [1차]: 2단계: 크기 절삭 함수를 호출하여 최대 파일 수 및 라인 수를 제한합니다.
    # [2차]: 2단계: 먹칠 끝난 서류가 10개 파일이나 200줄을 넘지 않게 자릅니다.
    truncated = truncate_diff(masked, max_files=max_files, max_lines=max_lines)

    # [1차]: 두 단계 보안 조치가 완료된 안전한 텍스트를 반환합니다.
    # [2차]: 100% 안심하고 인터넷으로 쏴도 되는 완벽히 무해해진 코드를 돌려줍니다.
    return truncated
