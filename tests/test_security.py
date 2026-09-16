"""
보안 및 Safe Mode 모듈 단위 테스트
"""

import unittest

from src.security import (
    mask_sensitive_data,
    truncate_diff,
    apply_safe_mode
)


class TestSecurity(unittest.TestCase):

    def test_mask_openai_api_key(self):
        raw = 'export OPENAI_API_KEY="sk-1234567890abcdefghijklmnopqrstuvwxyz"'
        masked = mask_sensitive_data(raw)
        self.assertNotIn("sk-1234567890abcdefghijklmnopqrstuvwxyz", masked)
        self.assertIn("[REDACTED_API_KEY]", masked)

    def test_mask_github_token(self):
        raw = 'git_token = "ghp_1234567890abcdefghijklmnopqrstuvwxyz12"'
        masked = mask_sensitive_data(raw)
        self.assertNotIn("ghp_1234567890abcdefghijklmnopqrstuvwxyz12", masked)
        self.assertIn("[REDACTED_GITHUB_TOKEN]", masked)

    def test_mask_aws_key(self):
        raw = 'aws_access_key = "AKIAIOSFODNN7EXAMPLE"'
        masked = mask_sensitive_data(raw)
        self.assertNotIn("AKIAIOSFODNN7EXAMPLE", masked)
        self.assertIn("[REDACTED_AWS_KEY]", masked)

    def test_mask_email(self):
        raw = "Author: dev.team_12@example-company.com"
        masked = mask_sensitive_data(raw)
        self.assertNotIn("dev.team_12@example-company.com", masked)
        self.assertIn("[REDACTED_EMAIL]", masked)

    def test_mask_password_assignment(self):
        raw = 'DB_PASSWORD = "super_secret_password_1234"'
        masked = mask_sensitive_data(raw)
        self.assertNotIn("super_secret_password_1234", masked)
        self.assertIn("[REDACTED_SECRET]", masked)

    def test_mask_private_key(self):
        raw = (
            "-----BEGIN RSA PRIVATE KEY-----\n"
            "MIIEowIBAAKCAQEA0Y123...\n"
            "-----END RSA PRIVATE KEY-----"
        )
        masked = mask_sensitive_data(raw)
        self.assertNotIn("MIIEowIBAAKCAQEA0Y123...", masked)
        self.assertIn("[REDACTED_PRIVATE_KEY]", masked)

    def test_truncate_diff_by_file_count(self):
        # 12개의 diff --git 블록 생성
        diff_blocks = []
        for i in range(12):
            diff_blocks.append(f"diff --git a/file{i}.py b/file{i}.py\n+line in file {i}")
        diff_text = "\n".join(diff_blocks)

        truncated = truncate_diff(diff_text, max_files=10, max_lines=500)
        self.assertIn("file0.py", truncated)
        self.assertIn("file9.py", truncated)
        self.assertNotIn("file10.py", truncated)
        self.assertNotIn("file11.py", truncated)
        self.assertIn("최대 10개 파일 초과 (외 2개 파일 생략)", truncated)

    def test_truncate_diff_by_line_count(self):
        # 250줄의 diff 텍스트 생성
        lines = [f"+line {i}" for i in range(250)]
        diff_text = "\n".join(lines)

        truncated = truncate_diff(diff_text, max_files=10, max_lines=200)
        line_count = len(truncated.splitlines())
        # 200줄 + 빈 줄 + 안내문구
        self.assertIn("최대 200줄 초과", truncated)
        self.assertIn("+line 199", truncated)
        self.assertNotIn("+line 200", truncated)

    def test_apply_safe_mode_disabled(self):
        raw = 'key = "sk-1234567890abcdefghijklmnopqrstuvwxyz"'
        result = apply_safe_mode(raw, enabled=False)
        self.assertEqual(result, raw)

    def test_apply_safe_mode_enabled(self):
        raw = 'key = "sk-1234567890abcdefghijklmnopqrstuvwxyz"'
        result = apply_safe_mode(raw, enabled=True)
        self.assertIn("[REDACTED_API_KEY]", result)


if __name__ == "__main__":
    unittest.main()
