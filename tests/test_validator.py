"""
출력 검증 및 후처리기 단위 테스트
"""

import unittest
from src.validator import (
    clean_title,
    strip_markdown_fences,
    validate_and_fix_commit,
    validate_and_fix_pr
)


class TestValidator(unittest.TestCase):

    def test_strip_markdown_fences(self):
        raw = "```markdown\nfeat: add feature\n\n- detail 1\n```"
        cleaned = strip_markdown_fences(raw)
        self.assertEqual(cleaned, "feat: add feature\n\n- detail 1")

    def test_clean_title_under_limit(self):
        title = "### feat: short title"
        cleaned = clean_title(title, max_length=72)
        self.assertEqual(cleaned, "feat: short title")

    def test_clean_title_over_limit(self):
        long_title = "feat: " + "a" * 80
        cleaned = clean_title(long_title, max_length=72)
        self.assertLessEqual(len(cleaned), 72)
        self.assertTrue(cleaned.endswith("..."))

    def test_validate_and_fix_commit_normal(self):
        raw = "feat(auth): add login token support\n\n- token auth logic\n- updated src/auth.py"
        fixed = validate_and_fix_commit(raw, ["src/auth.py"])
        lines = fixed.splitlines()
        self.assertEqual(lines[0], "feat(auth): add login token support")
        self.assertEqual(lines[1], "")
        self.assertIn("- token auth logic", fixed)

    def test_validate_and_fix_commit_missing_bullets(self):
        # 본문이 아예 없거나 불릿/파일 언급이 없는 경우
        raw = "fix: resolve critical null pointer bug"
        fixed = validate_and_fix_commit(raw, ["src/app.py"])
        lines = fixed.splitlines()
        self.assertEqual(lines[0], "fix: resolve critical null pointer bug")
        self.assertEqual(lines[1], "")
        self.assertIn("- 변경된 파일: src/app.py", fixed)
        self.assertIn("- 핵심 변경 사항 구현 및 반영", fixed)

    def test_validate_and_fix_commit_title_too_long(self):
        raw = "feat: " + ("super " * 15) + "long title here\n\n- bullet point"
        fixed = validate_and_fix_commit(raw, ["src/app.py"])
        title_line = fixed.splitlines()[0]
        self.assertLessEqual(len(title_line), 72)
        self.assertTrue(title_line.endswith("..."))

    def test_validate_and_fix_pr_complete(self):
        raw = (
            "feat: implement user authentication flow\n\n"
            "### Why\n- 사용자 인증 기능 추가 필요\n\n"
            "### What\n- JWT 토큰 생성 및 검증\n\n"
            "### How to Test\n- pytest tests/test_auth.py 실행"
        )
        fixed = validate_and_fix_pr(raw, ["src/auth.py"])
        self.assertIn("### Why", fixed)
        self.assertIn("### What", fixed)
        self.assertIn("### How to Test", fixed)
        self.assertIn("- 사용자 인증 기능 추가 필요", fixed)

    def test_validate_and_fix_pr_missing_section(self):
        # How to Test 섹션이 누락된 경우 자동 보충 확인
        raw = (
            "feat: implement user profile\n\n"
            "### Why\n- 프로필 확인 기능 필요\n\n"
            "### What\n- 프로필 조회 API 추가"
        )
        fixed = validate_and_fix_pr(raw, ["src/profile.py"])
        self.assertIn("### Why", fixed)
        self.assertIn("### What", fixed)
        self.assertIn("### How to Test", fixed)
        self.assertIn("- 관련 단위 테스트 실행", fixed)

    def test_validate_and_fix_pr_missing_bullets(self):
        # 섹션 헤더만 있고 불릿이 없는 경우
        raw = (
            "feat: add feature\n\n"
            "### Why\n"
            "설명만 있고 불릿이 없는 경우\n\n"
            "### What\n\n"
            "### How to Test\n"
        )
        fixed = validate_and_fix_pr(raw)
        self.assertIn("### Why", fixed)
        self.assertIn("### What", fixed)
        self.assertIn("### How to Test", fixed)
        # 모든 섹션에 최소 1개 불릿 확인
        for sec in ["Why", "What", "How to Test"]:
            idx = fixed.find(f"### {sec}")
            next_lines = fixed[idx:].splitlines()[1:3]
            has_bullet = any(l.strip().startswith("- ") for l in next_lines)
            self.assertTrue(has_bullet, f"{sec} 섹션에 불릿이 생성되어야 합니다.")


if __name__ == "__main__":
    unittest.main()
