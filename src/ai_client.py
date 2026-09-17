"""
AI REST API 클라이언트 모듈 (OpenAI 호환 규격, urllib 기반 경량 연동)
"""

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple


class APIError(Exception):
    """AI API 관련 기본 예외 클래스"""
    pass


class ConfigurationError(APIError):
    """API 키 등 필수 설정 누락 시 발생하는 예외"""
    pass


class AuthenticationError(APIError):
    """API 인증 실패(HTTP 401) 시 발생하는 예외"""
    pass


class QuotaExceededError(APIError):
    """API 할당량 초과 또는 Rate Limit(HTTP 429) 시 발생하는 예외"""
    pass


def load_dotenv_file(env_path: str = ".env") -> None:
    """루트 경로의 .env 파일이 존재하는 경우 환경변수로 자동 로드합니다."""
    if os.path.isfile(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass


class AIClient:
    """
    OpenAI 호환 REST API 클라이언트
    - urllib.request를 활용하여 외부 패키지 의존성 없이 동작
    - 단일 실행 시 1회 호출 원칙 및 호출 횟수 추적
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 45.0
    ):
        if api_key is None:
            load_dotenv_file()
            self.api_key = os.environ.get("OPENAI_API_KEY")
        else:
            self.api_key = api_key
        self.base_url = (
            base_url
            or os.environ.get("OPENAI_BASE_URL")
            or "https://api.openai.com/v1"
        ).rstrip("/")
        self.timeout = timeout
        self.call_count = 0

    def validate_configuration(self) -> None:
        """API 키 설정 여부를 검증합니다."""
        if not self.api_key:
            raise ConfigurationError(
                "AI API Key가 설정되지 않았습니다.\n"
                "환경변수를 설정해주세요:\n"
                "  - Windows (PowerShell): $env:OPENAI_API_KEY=\"your_key\"\n"
                "  - Windows (CMD): set OPENAI_API_KEY=your_key\n"
                "  - Linux / macOS: export OPENAI_API_KEY=\"your_key\""
            )

    def generate_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
        max_tokens: int = 500
    ) -> Tuple[str, float]:
        """
        AI API를 호출하여 텍스트 응답을 생성합니다.
        
        반환값: (생성된 텍스트, 소요 시간(초))
        """
        self.validate_configuration()

        endpoint = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        req_body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "codyssey-b3-02/1.0"
        }

        req = urllib.request.Request(endpoint, data=req_body, headers=headers, method="POST")

        start_time = time.perf_counter()
        self.call_count += 1

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                elapsed = time.perf_counter() - start_time
                resp_data = json.loads(response.read().decode("utf-8"))
                content = resp_data["choices"][0]["message"]["content"]
                return content.strip(), elapsed

        except urllib.error.HTTPError as e:
            error_msg = ""
            try:
                err_json = json.loads(e.read().decode("utf-8"))
                error_msg = err_json.get("error", {}).get("message", "")
            except Exception:
                pass

            if e.code == 401:
                raise AuthenticationError(
                    f"AI API 인증에 실패했습니다 (HTTP 401).\n"
                    f"API 키가 올바른지 확인해주세요. (원인: {error_msg or 'Invalid API Key'})"
                )
            elif e.code == 429:
                raise QuotaExceededError(
                    f"AI API 요청 한도 또는 크레딧이 초과되었습니다 (HTTP 429).\n"
                    f"잠시 후 다시 시도하거나 잔여 크레딧을 확인해주세요. (원인: {error_msg or 'Rate limit reached'})"
                )
            elif 500 <= e.code < 600:
                raise APIError(
                    f"AI API 제공업체 서버 오류가 발생했습니다 (HTTP {e.code}).\n"
                    f"잠시 후 다시 시도해주세요."
                )
            else:
                raise APIError(
                    f"AI API 호출 오류 (HTTP {e.code}): {error_msg or e.reason}"
                )

        except urllib.error.URLError as e:
            raise APIError(
                f"AI API 서버에 연결할 수 없습니다. 네트워크 상태를 확인해주세요.\n"
                f"원인: {e.reason}"
            )
        except json.JSONDecodeError:
            raise APIError("AI API 응답(JSON)을 파싱하는 중 오류가 발생했습니다.")
        except (KeyError, IndexError):
            raise APIError("AI API 응답 데이터 형식이 올바르지 않습니다.")
        except Exception as e:
            raise APIError(f"예상치 못한 오류가 발생했습니다: {str(e)}")
