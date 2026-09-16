"""
터미널 포매터 단위 테스트
"""

import unittest
from src.formatter import format_output


class TestFormatter(unittest.TestCase):

    def test_format_output_contains_required_sections(self):
        title = "커밋 메시지 초안"
        content = "feat: add feature\n\n- detail bullet"
        meta = {
            "call_count": 1,
            "elapsed": 1.23,
            "model": "gpt-4o-mini",
            "temperature": 0.2,
            "max_tokens": 300,
            "safe_mode": True
        }

        output = format_output(title, content, meta)

        self.assertIn("[생성 결과: 커밋 메시지 초안]", output)
        self.assertIn("feat: add feature", output)
        self.assertIn("AI API 호출 횟수 : 1회", output)
        self.assertIn("gpt-4o-mini", output)
        self.assertIn("보안 안전 모드   : 적용됨 (ON)", output)
        self.assertIn("검토 후 적용하세요", output)


if __name__ == "__main__":
    unittest.main()
