"""
Git 클라이언트 모듈 단위 테스트
"""

import subprocess
import unittest
from unittest.mock import patch, MagicMock

from src.git_client import (
    is_git_repository,
    get_git_root,
    get_changed_files,
    get_git_diff,
    has_changes
)


class TestGitClient(unittest.TestCase):

    @patch("src.git_client.run_git_command")
    def test_is_git_repository_true(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="true\n")
        self.assertTrue(is_git_repository())
        mock_run.assert_called_once_with(["rev-parse", "--is-inside-work-tree"], cwd=None)

    @patch("src.git_client.run_git_command")
    def test_is_git_repository_false(self, mock_run):
        mock_run.return_value = MagicMock(returncode=128, stdout="", stderr="fatal: not a git repository")
        self.assertFalse(is_git_repository())

    @patch("src.git_client.run_git_command")
    def test_get_git_root(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="/path/to/repo\n")
        self.assertEqual(get_git_root(), "/path/to/repo")

    @patch("src.git_client.run_git_command")
    def test_get_changed_files_parsing(self, mock_run):
        porcelain_output = (
            " M src/main.py\n"
            "M  src/utils.py\n"
            "?? tests/test_new.py\n"
            "A  README.md\n"
            '?? "테스트_파일.txt"\n'
            "R  old_name.py -> new_name.py\n"
        )
        mock_run.return_value = MagicMock(returncode=0, stdout=porcelain_output)
        files = get_changed_files()
        expected = [
            "src/main.py",
            "src/utils.py",
            "tests/test_new.py",
            "README.md",
            "테스트_파일.txt",
            "new_name.py"
        ]
        self.assertEqual(files, expected)

    @patch("src.git_client.run_git_command")
    def test_get_changed_files_empty(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        self.assertEqual(get_changed_files(), [])

    @patch("src.git_client.run_git_command")
    def test_get_git_diff_staged_only(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="diff --git a/a.py b/a.py\n+new line")
        diff = get_git_diff(staged_only=True)
        self.assertIn("+new line", diff)
        mock_run.assert_called_once_with(["diff", "--cached"], cwd=None)

    @patch("src.git_client.run_git_command")
    def test_get_git_diff_both_staged_and_unstaged(self, mock_run):
        def side_effect(args, cwd=None):
            if args == ["diff", "--cached"]:
                return MagicMock(returncode=0, stdout="staged changes")
            elif args == ["diff"]:
                return MagicMock(returncode=0, stdout="unstaged changes")
            return MagicMock(returncode=0, stdout="")

        mock_run.side_effect = side_effect
        diff = get_git_diff(staged_only=False)
        self.assertIn("staged changes", diff)
        self.assertIn("unstaged changes", diff)

    @patch("src.git_client.get_changed_files")
    @patch("src.git_client.get_git_diff")
    def test_has_changes(self, mock_diff, mock_files):
        # Case 1: 변경 사항 있음
        mock_files.return_value = ["file.py"]
        mock_diff.return_value = ""
        self.assertTrue(has_changes())

        mock_files.return_value = []
        mock_diff.return_value = "+some diff"
        self.assertTrue(has_changes())

        # Case 2: 변경 사항 없음
        mock_files.return_value = []
        mock_diff.return_value = ""
        self.assertFalse(has_changes())


if __name__ == "__main__":
    unittest.main()
