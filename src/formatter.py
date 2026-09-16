"""
터미널 출력용 구분선, 헤더, 메타데이터 포맷팅 모듈
"""

from typing import Any, Dict, Optional

DIVIDER_DOUBLE = "=" * 68
DIVIDER_SINGLE = "-" * 68


def format_output(
    title: str,
    content: str,
    meta: Optional[Dict[str, Any]] = None
) -> str:
    """
    최종 결과물을 구분선, 헤더, 실행 메타정보와 함께 터미널에 정돈된 형태로 출력할 문자열을 생성합니다.
    """
    meta_info = meta or {}
    call_count = meta_info.get("call_count", 1)
    elapsed = meta_info.get("elapsed", 0.0)
    model = meta_info.get("model", "gpt-4o-mini")
    temperature = meta_info.get("temperature", 0.2)
    max_tokens = meta_info.get("max_tokens", 300)
    safe_mode = meta_info.get("safe_mode", True)

    lines = [
        DIVIDER_DOUBLE,
        f"  [생성 결과: {title}]",
        DIVIDER_SINGLE,
        content.strip(),
        DIVIDER_SINGLE,
        "  [실행 메타정보]",
        f"  * AI API 호출 횟수 : {call_count}회",
        f"  * 소요 시간        : {elapsed:.2f}초",
        f"  * 사용 모델        : {model} (temp={temperature}, max_tokens={max_tokens})",
        f"  * 보안 안전 모드   : {'적용됨 (ON)' if safe_mode else '미적용 (OFF)'}",
        DIVIDER_DOUBLE,
        "  [안내] 위 결과물은 AI가 생성한 초안입니다. 반드시 검토 후 적용하세요.",
        DIVIDER_DOUBLE,
    ]

    return "\n".join(lines)
