# [1차]: AI REST API 클라이언트 모듈의 성격과 역할을 설명하는 다중 라인 모듈 독스트링의 시작입니다.
# [2차]: "이 파일은 태평양 건너 미국에 있는 OpenAI 인공지능 본사로 직접 전화를 걸어 대화를 나누는 전담 국제전화 부스입니다"라는 간판입니다.
"""
# [1차]: AI REST API 클라이언트 모듈(OpenAI 호환 규격, urllib 기반 경량 연동)임을 명시합니다.
# [2차]: 외부 패키지 설치 없이 파이썬 순정 부품(urllib)만으로 가볍고 빠르게 동작하는 스마트 전화기입니다.
AI REST API 클라이언트 모듈 (OpenAI 호환 규격, urllib 기반 경량 연동)
# [1차]: 모듈 독스트링을 닫는 삼중 따옴표입니다.
# [2차]: 간판 닫기.
"""

# [1차]: 파이썬 딕셔너리와 JSON 문자열 간의 상호 변환(직렬화/역직렬화)을 위해 json 표준 모듈을 임포트합니다.
# [2차]: 파이썬 언어로 된 요청서를 인터넷 전송용 국제 표준 데이터 규격(JSON 상자)으로 포장해 주는 택배 포장기입니다.
import json
# [1차]: 환경변수(OPENAI_API_KEY) 및 파일 경로 조회를 위해 os 모듈을 임포트합니다.
# [2차]: 컴퓨터 운영체제의 환경설정 금고를 뒤져서 비밀 API 키를 꺼내오기 위한 마스터키입니다.
import os
# [1차]: API 호출 소요 시간(초)을 정밀하게 측정하기 위해 time 모듈을 임포트합니다.
# [2차]: AI에게 전화를 걸고 끊을 때까지 몇 초 걸렸는지 0.001초 단위로 재는 고성능 스톱워치입니다.
import time
# [1차]: HTTP 상태 코드 오류(HTTPError, URLError)를 처리하기 위해 urllib.error 모듈을 임포트합니다.
# [2차]: 상대방 전화가 통화 중이거나 결번일 때 "어떤 문제가 생겼는지" 파악하는 에러 감지기입니다.
import urllib.error
# [1차]: HTTP POST 네트워크 요청을 전송하기 위해 urllib.request 모듈을 임포트합니다.
# [2차]: 전파를 쏴서 인터넷 통신 패킷을 미국 서버로 날려 보내는 무전기 송신기입니다.
import urllib.request
# [1차]: 타입 어노테이션을 위해 typing 모듈에서 제네릭 타입들을 임포트합니다.
# [2차]: 코드 곳곳에 "여긴 텍스트, 여긴 숫자"라고 표기해 주는 문법 라벨들입니다.
from typing import Any, Dict, List, Optional, Tuple


# [1차]: AI API 통신 중 발생하는 모든 오류의 최상위 기본 커스텀 예외 클래스를 선언합니다.
# [2차]: "AI 통신과 관련된 모든 사고"를 통틀어 지칭하는 가장 큰 에러 집안의 할아버지 클래스입니다.
class APIError(Exception):
    # [1차]: 예외 클래스 목적을 명시한 한 줄 독스트링입니다.
    # [2차]: 설명서입니다.
    """AI API 관련 기본 예외 클래스"""
    # [1차]: 추가 구현 없이 상속받은 표준 기능을 유지합니다.
    # [2차]: 기본 에러 기능을 그대로 물려받아 씁니다.
    pass


# [1차]: 필수 설정(API 키 등)이 누락되었을 때 발생하는 ConfigurationError 클래스를 선언합니다.
# [2차]: "야! 너 전화 걸기 전에 API 키(동전)도 안 넣었잖아!" 하고 혼내는 설정 불량 에러입니다.
class ConfigurationError(APIError):
    # [1차]: 클래스 독스트링입니다.
    # [2차]: 설명서입니다.
    """API 키 등 필수 설정 누락 시 발생하는 예외"""
    # [1차]: 상속 기능을 유지합니다.
    # [2차]: 에러 기능을 그대로 씁니다.
    pass


# [1차]: HTTP 401 인증 실패 시 발생하는 AuthenticationError 클래스를 선언합니다.
# [2차]: "네가 준 비밀번호(API 키)가 가짜이거나 오타가 났대!" 하고 알려주는 출입 거절 에러입니다.
class AuthenticationError(APIError):
    # [1차]: 클래스 독스트링입니다.
    # [2차]: 설명서입니다.
    """API 인증 실패(HTTP 401) 시 발생하는 예외"""
    # [1차]: 상속 기능을 유지합니다.
    # [2차]: 에러 기능을 그대로 씁니다.
    pass


# [1차]: HTTP 429 요청 한도 및 크레딧 소진 시 발생하는 QuotaExceededError 클래스를 선언합니다.
# [2차]: "계정에 충전해 둔 크레딧(달러)이 다 떨어졌거나, 1초에 너무 많이 전화해서 쫓겨났어!"를 알리는 잔액 부족 에러입니다.
class QuotaExceededError(APIError):
    # [1차]: 클래스 독스트링입니다.
    # [2차]: 설명서입니다.
    """API 할당량 초과 또는 Rate Limit(HTTP 429) 시 발생하는 예외"""
    # [1차]: 상속 기능을 유지합니다.
    # [2차]: 에러 기능을 그대로 씁니다.
    pass


# [1차]: 외부 라이브러리 없이 .env 파일을 읽어 시스템 환경변수로 등록하는 load_dotenv_file 함수 선언부입니다.
# [2차]: 비밀 금고 메모지(`.env`)를 발견하면 거기에 적힌 비밀 키들을 컴퓨터의 머릿속(`os.environ`)에 쏙쏙 입력해 주는 심부름꾼입니다.
def load_dotenv_file(env_path: str = ".env") -> None:
    # [1차]: 함수의 목적을 명시한 한 줄 독스트링입니다.
    # [2차]: 설명서입니다.
    """루트 경로의 .env 파일이 존재하는 경우 환경변수로 자동 로드합니다."""
    # [1차]: 지정된 경로에 .env 파일이 실제로 존재하는지 검사합니다.
    # [2차]: "프로젝트 폴더에 진짜 .env 파일이 놓여 있나?" 하고 확인합니다.
    if os.path.isfile(env_path):
        # [1차]: 파일 I/O 오류를 포착하기 위한 try 블록입니다.
        # [2차]: 파일 읽다가 문제 생겨도 프로그램이 죽지 않도록 감싸는 안전장치입니다.
        try:
            # [1차]: .env 파일을 UTF-8 읽기 모드로 오픈합니다.
            # [2차]: 한글이나 특수문자가 안 깨지도록 .env 파일을 펼칩니다.
            with open(env_path, "r", encoding="utf-8") as f:
                # [1차]: 파일 내용을 한 라인씩 순회합니다.
                # [2차]: 메모지에 적힌 줄들을 위에서부터 한 줄씩 읽습니다.
                for line in f:
                    # [1차]: 줄 좌우 공백을 제거합니다.
                    # [2차]: 줄 양쪽의 여백을 털어냅니다.
                    line = line.strip()
                    # [1차]: 빈 줄이 아니고, 주석(#)이 아니며, 등호(=)를 포함하는 유효 데이터 라인인지 검사합니다.
                    # [2차]: 빈 줄이나 주석(# 메모)은 건너뛰고, "이름 = 값" 형태로 적힌 진짜 데이터 줄만 골라냅니다.
                    if line and not line.startswith("#") and "=" in line:
                        # [1차]: 첫 번째 등호를 기준으로 키(k)와 값(v)을 분리합니다.
                        # [2차]: 등호를 칼로 똑 잘라서 왼쪽은 명찰(Key), 오른쪽은 내용물(Value)로 나눕니다.
                        # 마이: 한번만 자르라는것. 코드에서 첫번쨰 등장에 유의미해서 쓴것.
                        k, v = line.split("=", 1)
                        # [1차]: 키의 양쪽 공백을 제거합니다.
                        # [2차]: 명찰의 공백을 지웁니다.
                        k = k.strip()
                        # [1차]: 값의 공백 및 따옴표(' 또는 ")를 벗겨냅니다.
                        # [2차]: 따옴표("...")로 포장되어 있다면 껍질을 벗겨 순수 알맹이 글자만 남깁니다.
                        v = v.strip().strip("'\"")
                        # [1차]: 유효한 키이고 아직 시스템 환경변수에 등록되지 않은 경우에만 등록합니다.
                        # [2차]: 이미 컴퓨터 터미널에서 export/set으로 준 우선순위 높은 키가 있다면 덮어쓰지 않고,
                        #  없을 때만 채워 넣는 매너 있는 동작입니다.
                        if k and k not in os.environ:
                            # [1차]: os.environ 딕셔너리에 키-값을 저장합니다.
                            # [2차]: 컴퓨터 환경변수 저장소에 값을 쏙 집어넣습니다.
                            os.environ[k] = v
        # [1차]: 모든 예외를 무시하고 통과합니다.
        # [2차]: .env를 못 읽더라도 터미널 환경변수가 있을 수 있으므로 조용히 넘어갑니다.
        except Exception:
            pass


# [1차]: OpenAI 호환 REST API 호출 및 통신을 전담하는 AIClient 클래스 선언부입니다.
# [2차]: "AI 통신 전담 비서"를 찍어내는 설계도(Class)입니다.
class AIClient:
    # [1차]: 클래스의 설계 원칙(외부 의존성 없음, 1회 호출 원칙)을 기술한 Docstring의 시작입니다.
    # [2차]: 설명서 시작.
    """
    # [1차]: urllib 기반 동작 및 호출 횟수 추적 특징을 설명합니다.
    # [2차]: 이 비서가 왜 가볍고 돈을 아껴주는지 설명하는 소개글입니다.
    OpenAI 호환 REST API 클라이언트
    - urllib.request를 활용하여 외부 패키지 의존성 없이 동작
    - 단일 실행 시 1회 호출 원칙 및 호출 횟수 추적
    # [1차]: Docstring을 닫습니다.
    # [2차]: 설명서 끝.
    """

    # [1차]: AIClient 인스턴스를 초기화하는 생성자 메서드입니다.
    # [2차]: 비서를 처음 채용할 때 기본 세팅(출입증, 본사 주소, 최대 대기시간)을 해주는 입사식입니다.
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 45.0
    ):
        # [1차]: api_key가 직접 전달되지 않은 경우 .env 로드 후 환경변수에서 키를 가져옵니다.
        # [2차]: 손에 키를 안 쥐어주고 출근시켰으면, 비서가 알아서 .env 메모지와 컴퓨터 금고를 뒤져 키를 찾아냅니다.
        if api_key is None:
            # [1차]: load_dotenv_file을 호출하여 .env 환경변수를 주입합니다.
            # [2차]: 메모지를 열어 환경변수에 키를 채웁니다.
            load_dotenv_file()
            # [1차]: os.environ에서 OPENAI_API_KEY 값을 취해 인스턴스 변수에 저장합니다.
            # [2차]: 컴퓨터 금고에서 키를 꺼내 주머니에 넣습니다.
            self.api_key = os.environ.get("OPENAI_API_KEY")
        # [1차]: 생성자 인자로 API 키를 직접 넘겨준 경우의 분기입니다.
        # [2차]: 테스트할 때 "이 가짜 키 써봐" 하고 직접 건네준 키를 챙깁니다.
        else:
            # [1차]: 전달받은 키를 직접 인스턴스 변수에 저장합니다.
            # [2차]: 전달받은 키를 주머니에 넣습니다.
            self.api_key = api_key
        # [1차]: base_url 인자 -> 환경변수 OPENAI_BASE_URL -> 공식 기본값 순서로 URL을 결정하고 우측 슬래시를 제거합니다.
        # [2차]: 통신할 OpenAI 본사 서버 주소를 세팅하고 끝에 붙은 주소 슬래시('/')를 깔끔하게 다듬습니다.
        self.base_url = (
            base_url
            or os.environ.get("OPENAI_BASE_URL")
            or "https://api.openai.com/v1"
        ).rstrip("/")
        # [1차]: 네트워크 요청 타임아웃 제한 시간(기본 45.0초)을 설정합니다.
        # [2차]: "전화 걸고 45초 동안 아무 대답 없으면 전화 끊어버려!"라는 인내심 타이머입니다.
        self.timeout = timeout
        # [1차]: API 호출 횟수를 추적하는 카운터 변수를 0으로 초기화합니다.
        # [2차]: "AI한테 전화 몇 번 걸었는지 셀 계수기"를 0으로 맞춥니다. 비용 통제를 위한 핵심 장치입니다.
        self.call_count = 0

    # [1차]: API 키가 유효하게 설정되어 있는지 검증하는 메서드 선언부입니다.
    # [2차]: "전화 걸기 전에 동전(API 키) 주머니에 진짜 있는지 만져봐!" 하는 안전 점검입니다.
    def validate_configuration(self) -> None:
        # [1차]: 메서드 역할을 기술한 한 줄 독스트링입니다.
        # [2차]: 설명서입니다.
        """API 키 설정 여부를 검증합니다."""
        # [1차]: api_key가 None이거나 빈 문자열인 경우를 검사합니다.
        # [2차]: 키가 없으면 통신을 시도조차 하지 않고 멈춥니다.
        if not self.api_key:
            # [1차]: OS별 환경변수 설정 명령어가 포함된 상세한 ConfigurationError 예외를 발생시킵니다.
            # [2차]: 초보 개발자가 당황하지 않도록 "윈도우는 이렇게 치고, 맥은 이렇게 치세요"라는 친절한 과외 선생님 같은 에러 안내문을 던집니다.
            raise ConfigurationError(
                "AI API Key가 설정되지 않았습니다.\n"
                "환경변수를 설정해주세요:\n"
                "  - Windows (PowerShell): $env:OPENAI_API_KEY=\"your_key\"\n"
                "  - Windows (CMD): set OPENAI_API_KEY=your_key\n"
                "  - Linux / macOS: export OPENAI_API_KEY=\"your_key\""
            )

    # [1차]: AI API에 완성 요청을 보내고 (답변텍스트, 소요시간) 튜플을 반환하는 핵심 메서드입니다.
    # [2차]: "진짜로 전화 걸어서 물어보고, 대답 받아 적고 스톱워치 끄기!"를 수행하는 메인 엔진입니다.
    def generate_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
        max_tokens: int = 500
    ) -> Tuple[str, float]:
        # [1차]: 메서드의 목적과 반환 규격을 기술하는 Docstring의 시작입니다.
        # [2차]: 설명서 시작.
        """
        # [1차]: 텍스트 응답 생성 및 반환값 규격을 설명합니다.
        # [2차]: 설명입니다.
        AI API를 호출하여 텍스트 응답을 생성합니다.
        
        반환값: (생성된 텍스트, 소요 시간(초))
        # [1차]: Docstring을 닫습니다.
        # [2차]: 설명서 끝.
        """
        # [1차]: 통신 시도 전 API 키 설정 유효성을 먼저 검증합니다.
        # [2차]: 전화 수화기 들기 전에 동전 확인부터 합니다.
        self.validate_configuration()

        # [1차]: 목적지 REST 엔드포인트 URL(/chat/completions)을 조립합니다.
        # [2차]: OpenAI 건물의 '채팅 답변 창구 번호판' 주소를 완성합니다.
        endpoint = f"{self.base_url}/chat/completions"
        # [1차]: 요청 페이로드 파라미터(모델, 메시지, 온도, 최대토큰) 딕셔너리를 구성합니다.
        # [2차]: 모델명, 질문지(messages), 온도(temperature), 글자수(max_tokens)를 규격 용지에 적습니다.
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        # [1차]: 페이로드 딕셔너리를 JSON 문자열로 변환 후 UTF-8 바이트로 인코딩합니다.
        # [2차]: 적어둔 용지를 통신 케이블을 타고 날아갈 수 있게 전기 신호(바이트)로 압축 포장합니다.
        req_body = json.dumps(payload).encode("utf-8")
        # [1차]: HTTP 요청 헤더(Content-Type, Bearer 토큰 인증, User-Agent)를 설정합니다.
        # [2차]: 편지 봉투 겉면에 "이건 JSON 문서고, 내 API 키는 이거며, 내 프로그램 이름은 codyssey야"라고 도장을 찍습니다.
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "codyssey-b3-02/1.0"
        }

        # [1차]: urllib.request.Request 객체를 POST 메서드로 생성합니다.
        # [2차]: 보낼 편지 상자(URL + 데이터 + 헤더)를 우체통 투입구에 장전합니다.
        req = urllib.request.Request(endpoint, data=req_body, headers=headers, method="POST")

        # [1차]: 통신 시작 시간을 고정밀 타이머로 측정합니다.
        # [2차]: 전화 걸기 직전 스톱워치 스타트 버튼을 찰칵 누릅니다.
        start_time = time.perf_counter()
        # [1차]: 단일 실행 1회 호출 원칙에 따라 호출 카운터를 1 증가시킵니다.
        # [2차]: 계수기 숫자를 +1 올립니다.
        self.call_count += 1

        # [1차]: 네트워크 통신 오류를 포착하기 위한 try 블록입니다.
        # [2차]: 통신 중에 생길 수 있는 온갖 돌발 상황에 대비하는 그물망입니다.
        try:
            # [1차]: urlopen으로 HTTP 요청을 전송하고 컨텍스트 매니저로 응답 스트림을 관리합니다.
            # [2차]: 신호가 미국으로 날아가서 서버의 답변 문이 열리는 순간입니다.
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                # [1차]: 응답 수신 즉시 경과 시간(초)을 계산합니다.
                # [2차]: 대답을 듣자마자 스톱워치를 멈추고 몇 초 걸렸는지 잽니다.
                elapsed = time.perf_counter() - start_time
                # [1차]: 응답 바이트를 UTF-8로 디코딩하고 JSON 딕셔너리로 역직렬화합니다.
                # [2차]: 미국에서 날아온 암호 전기 신호를 다시 사람이 읽을 수 있는 글자로 번역합니다.
                resp_data = json.loads(response.read().decode("utf-8"))
                # [1차]: OpenAI 응답 구조(choices[0].message.content)에서 답변 텍스트를 추출합니다.
                # [2차]: 거대한 답변 보고서 상자 속에서 알맹이 편지 내용(AI의 실제 답변)만 쏙 빼냅니다.
                content = resp_data["choices"][0]["message"]["content"]
                # [1차]: 양쪽 여백을 정돈한 텍스트와 소요 시간(초)을 튜플로 반환합니다.
                # [2차]: 완성된 답변 텍스트와 소요 시간(예: ("feat: 로그인 기능 구현", 1.45))을 손에 쥐여줍니다.
                return content.strip(), elapsed

        # [1차]: HTTP 응답 에러(4xx, 5xx) 발생 시의 예외 분기입니다.
        # [2차]: 상대방 서버가 거절 응답(HTTP 에러 코드)을 보냈을 때의 비상 대책반입니다.
        except urllib.error.HTTPError as e:
            # [1차]: 에러 상세 사유 메시지를 저장할 변수를 초기화합니다.
            # [2차]: 서버가 왜 화가 났는지 구체적인 이유 쪽지를 읽을 준비를 합니다.
            error_msg = ""
            # [1차]: 서버가 보낸 에러 JSON 본문에서 메시지를 추출하기 위한 내부 try 블록입니다.
            # [2차]: 에러 쪽지 열어보기 시도입니다.
            try:
                # [1차]: 에러 응답 바이트를 파싱하여 JSON 딕셔너리로 변환합니다.
                # [2차]: 에러 JSON 쪽지를 해석합니다.
                err_json = json.loads(e.read().decode("utf-8"))
                # [1차]: error.message 필드의 상세 에러 텍스트를 추출합니다.
                # [2차]: 쪽지에 적힌 구체적인 이유 문장을 꺼냅니다.
                error_msg = err_json.get("error", {}).get("message", "")
            # [1차]: JSON 파싱 실패 시 예외를 조용히 무시합니다.
            # [2차]: 쪽지 해석이 안 되면 기본 에러 이유를 쓸 수 있게 넘어갑니다.
            except Exception:
                pass

            # [1차]: HTTP 401(Unauthorized)인 경우 AuthenticationError를 발생시킵니다.
            # [2차]: 401 에러면 "API 키가 틀렸어요!"라고 직관적으로 짚어줍니다.
            if e.code == 401:
                raise AuthenticationError(
                    f"AI API 인증에 실패했습니다 (HTTP 401).\n"
                    f"API 키가 올바른지 확인해주세요. (원인: {error_msg or 'Invalid API Key'})"
                )
            # [1차]: HTTP 429(Rate Limit/Quota Exceeded)인 경우 QuotaExceededError를 발생시킵니다.
            # [2차]: 429 에러면 "요청 한도 초과 또는 잔여 달러가 부족해요!"라고 알려줍니다.
            elif e.code == 429:
                raise QuotaExceededError(
                    f"AI API 요청 한도 또는 크레딧이 초과되었습니다 (HTTP 429).\n"
                    f"잠시 후 다시 시도하거나 잔여 크레딧을 확인해주세요. (원인: {error_msg or 'Rate limit reached'})"
                )
            # [1차]: HTTP 500~599(서버 장애)인 경우 APIError를 발생시킵니다.
            # [2차]: 우리 잘못이 아니라 OpenAI 회사 서버가 다운되었을 때입니다.
            elif 500 <= e.code < 600:
                raise APIError(
                    f"AI API 제공업체 서버 오류가 발생했습니다 (HTTP {e.code}).\n"
                    f"잠시 후 다시 시도해주세요."
                )
            # [1차]: 그 외 기타 HTTP 상태 코드 에러의 처리입니다.
            # [2차]: 기타 웹 오류에 대한 범용 안내입니다.
            else:
                raise APIError(
                    f"AI API 호출 오류 (HTTP {e.code}): {error_msg or e.reason}"
                )

        # [1차]: DNS 오류, 네트워크 단절 등 연결 자체 실패 시 URLError를 포착합니다.
        # [2차]: 랜선이 뽑혔거나 와이파이가 끊겨서 아예 서버를 찾을 수 없을 때입니다.
        except urllib.error.URLError as e:
            raise APIError(
                f"AI API 서버에 연결할 수 없습니다. 네트워크 상태를 확인해주세요.\n"
                f"원인: {e.reason}"
            )
        # [1차]: 응답 본문이 깨져서 JSON 디코딩에 실패한 경우의 예외 처리입니다.
        # [2차]: 서버가 준 글자가 깨져서 읽을 수 없을 때입니다.
        except json.JSONDecodeError:
            raise APIError("AI API 응답(JSON)을 파싱하는 중 오류가 발생했습니다.")
        # [1차]: 응답 JSON 구조에서 choices나 content 키가 누락된 경우의 예외 처리입니다.
        # [2차]: 상자를 열었는데 있어야 할 알맹이 봉투가 안 들어있을 때입니다.
        except (KeyError, IndexError):
            raise APIError("AI API 응답 데이터 형식이 올바르지 않습니다.")
        # [1차]: 기타 예상치 못한 모든 런타임 예외를 가로채어 APIError로 래핑합니다.
        # [2차]: 상상치 못한 돌발 버그가 생겨도 원인을 친절하게 알려주며 마무리하는 최종 안전망입니다.
        except Exception as e:
            raise APIError(f"예상치 못한 오류가 발생했습니다: {str(e)}")
