"""
프롬프트 생성 모듈 단위 테스트
"""

import unittest
from src.prompts import build_commit_prompt, build_pr_prompt


class TestPrompts(unittest.TestCase):

    def test_build_commit_prompt_structure(self):
        changed_files = ["src/main.py", "tests/test_main.py"]
        diff_text = "+ def hello():\n+     return 'world'"

        messages = build_commit_prompt(changed_files, diff_text)

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")

        # 시스템 프롬프트 검증
        sys_content = messages[0]["content"]
        self.assertIn("Conventional Commits", sys_content)
        self.assertIn("72자", sys_content)
        self.assertIn("불릿", sys_content)

        # 유저 프롬프트 검증
        user_content = messages[1]["content"]
        self.assertIn("src/main.py", user_content)
        self.assertIn("tests/test_main.py", user_content)
        self.assertIn("+ def hello():", user_content)

    def test_build_pr_prompt_structure(self):
        changed_files = ["README.md"]
        diff_text = "+ # New Docs"

        messages = build_pr_prompt(changed_files, diff_text)

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")

        # 시스템 프롬프트 필수 섹션 검증
        sys_content = messages[0]["content"]
        self.assertIn("Why", sys_content)
        self.assertIn("What", sys_content)
        self.assertIn("How to Test", sys_content)
        self.assertIn("80자", sys_content)

        # 유저 프롬프트 검증
        user_content = messages[1]["content"]
        self.assertIn("README.md", user_content)
        self.assertIn("+ # New Docs", user_content)


if __name__ == "__main__":
    unittest.main()
