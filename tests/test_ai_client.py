"""
AI API 클라이언트 모듈 단위 테스트 (Mock 기반)
"""

import io
import json
import unittest
import urllib.error
from unittest.mock import patch, MagicMock

from src.ai_client import (
    AIClient,
    ConfigurationError,
    AuthenticationError,
    QuotaExceededError,
    APIError
)


class TestAIClient(unittest.TestCase):

    def test_missing_api_key_raises_configuration_error(self):
        client = AIClient(api_key="")
        with self.assertRaises(ConfigurationError):
            client.generate_completion([{"role": "user", "content": "hi"}])

    @patch("urllib.request.urlopen")
    def test_generate_completion_success(self, mock_urlopen):
        mock_resp_data = {
            "choices": [
                {
                    "message": {
                        "content": "feat: test commit\n\n- test bullet"
                    }
                }
            ]
        }
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(mock_resp_data).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        client = AIClient(api_key="test-key")
        content, elapsed = client.generate_completion(
            [{"role": "user", "content": "test"}],
            model="gpt-4o-mini",
            temperature=0.2,
            max_tokens=300
        )

        self.assertEqual(content, "feat: test commit\n\n- test bullet")
        self.assertGreaterEqual(elapsed, 0.0)
        self.assertEqual(client.call_count, 1)

    @patch("urllib.request.urlopen")
    def test_generate_completion_http_401(self, mock_urlopen):
        error_body = json.dumps({"error": {"message": "Invalid API key"}}).encode("utf-8")
        http_error = urllib.error.HTTPError(
            url="http://api.com",
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=io.BytesIO(error_body)
        )
        mock_urlopen.side_effect = http_error

        client = AIClient(api_key="wrong-key")
        with self.assertRaises(AuthenticationError) as ctx:
            client.generate_completion([{"role": "user", "content": "test"}])
        self.assertIn("HTTP 401", str(ctx.exception))

    @patch("urllib.request.urlopen")
    def test_generate_completion_http_429(self, mock_urlopen):
        error_body = json.dumps({"error": {"message": "Quota exceeded"}}).encode("utf-8")
        http_error = urllib.error.HTTPError(
            url="http://api.com",
            code=429,
            msg="Too Many Requests",
            hdrs={},
            fp=io.BytesIO(error_body)
        )
        mock_urlopen.side_effect = http_error

        client = AIClient(api_key="test-key")
        with self.assertRaises(QuotaExceededError) as ctx:
            client.generate_completion([{"role": "user", "content": "test"}])
        self.assertIn("HTTP 429", str(ctx.exception))

    @patch("urllib.request.urlopen")
    def test_generate_completion_http_500(self, mock_urlopen):
        http_error = urllib.error.HTTPError(
            url="http://api.com",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=io.BytesIO(b"{}")
        )
        mock_urlopen.side_effect = http_error

        client = AIClient(api_key="test-key")
        with self.assertRaises(APIError) as ctx:
            client.generate_completion([{"role": "user", "content": "test"}])
        self.assertIn("HTTP 500", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
