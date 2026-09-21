"""
CLI 인터페이스 및 파이프라인 통합 단위 테스트
"""

import io
import unittest
from unittest.mock import patch, MagicMock

from src.ai_client import AIClient, APIError, ConfigurationError
from src.cli import build_parser, main, run_commit_pipeline, run_pr_pipeline


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.parser = build_parser()

    def test_argument_parsing_commit_defaults(self):
        args = self.parser.parse_args(["commit"])
        self.assertEqual(args.command, "commit")
        self.assertEqual(args.model, "gpt-4o-mini")
        self.assertEqual(args.temperature, 0.2)
        self.assertEqual(args.max_tokens, 300)
        self.assertTrue(args.safe_mode)
        self.assertFalse(args.staged)

    def test_argument_parsing_commit_custom(self):
        args = self.parser.parse_args([
            "commit",
            "-m", "gpt-4o",
            "-t", "0.5",
            "--max-tokens", "400",
            "--no-safe-mode",
            "--staged"
        ])
        self.assertEqual(args.model, "gpt-4o")
        self.assertEqual(args.temperature, 0.5)
        self.assertEqual(args.max_tokens, 400)
        self.assertFalse(args.safe_mode)
        self.assertTrue(args.staged)

    def test_argument_parsing_pr_defaults(self):
        args = self.parser.parse_args(["pr"])
        self.assertEqual(args.command, "pr")
        self.assertEqual(args.max_tokens, 1000)
        self.assertTrue(args.safe_mode)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_main_no_command_returns_1(self, mock_stdout):
        exit_code = main([])
        self.assertEqual(exit_code, 1)

    @patch("src.cli.is_git_repository", return_value=False)
    @patch("sys.stderr", new_callable=io.StringIO)
    def test_run_commit_pipeline_not_git_repo(self, mock_stderr, mock_is_git):
        args = self.parser.parse_args(["commit"])
        exit_code = run_commit_pipeline(args)
        self.assertEqual(exit_code, 1)
        self.assertIn("Git 저장소가 아닙니다", mock_stderr.getvalue())

    @patch("src.cli.is_git_repository", return_value=True)
    @patch("src.cli.get_changed_files", return_value=[])
    @patch("src.cli.get_git_diff", return_value="")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_run_commit_pipeline_no_changes(self, mock_stdout, mock_diff, mock_files, mock_is_git):
        args = self.parser.parse_args(["commit"])
        exit_code = run_commit_pipeline(args)
        self.assertEqual(exit_code, 0)
        self.assertIn("변경 사항이 없습니다", mock_stdout.getvalue())

    @patch("src.cli.is_git_repository", return_value=True)
    @patch("src.cli.get_changed_files", return_value=["src/main.py"])
    @patch("src.cli.get_git_diff", return_value="+ def new_feat(): pass")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_run_commit_pipeline_success(self, mock_stdout, mock_diff, mock_files, mock_is_git):
        args = self.parser.parse_args(["commit"])
        mock_client = MagicMock()
        mock_client.generate_completion.return_value = (
            "feat: add new feature\n\n- added new_feat()", 1.25
        )
        mock_client.call_count = 1

        exit_code = run_commit_pipeline(args, client=mock_client)
        self.assertEqual(exit_code, 0)
        output = mock_stdout.getvalue()
        self.assertIn("[생성 결과: 커밋 메시지 초안]", output)
        self.assertIn("feat: add new feature", output)
        self.assertIn("AI API 호출 횟수 : 1회", output)

    @patch("src.cli.is_git_repository", return_value=True)
    @patch("src.cli.get_changed_files", return_value=["src/main.py"])
    @patch("src.cli.get_git_diff", return_value="+ new line")
    @patch("sys.stderr", new_callable=io.StringIO)
    def test_run_commit_pipeline_config_error(self, mock_stderr, mock_diff, mock_files, mock_is_git):
        args = self.parser.parse_args(["commit"])
        mock_client = MagicMock()
        mock_client.generate_completion.side_effect = ConfigurationError("API 키가 없습니다.")

        exit_code = run_commit_pipeline(args, client=mock_client)
        self.assertEqual(exit_code, 1)
        self.assertIn("API 키가 없습니다.", mock_stderr.getvalue())

    @patch("src.cli.is_git_repository", return_value=True)
    @patch("src.cli.get_changed_files", return_value=["src/main.py"])
    @patch("src.cli.get_git_diff", return_value="+ new line")
    @patch("sys.stderr", new_callable=io.StringIO)
    def test_run_commit_pipeline_api_error(self, mock_stderr, mock_diff, mock_files, mock_is_git):
        args = self.parser.parse_args(["commit"])
        mock_client = MagicMock()
        mock_client.generate_completion.side_effect = APIError("연결 오류")

        exit_code = run_commit_pipeline(args, client=mock_client)
        self.assertEqual(exit_code, 1)
        self.assertIn("연결 오류", mock_stderr.getvalue())

    @patch("src.cli.is_git_repository", return_value=True)
    @patch("src.cli.get_changed_files", return_value=["README.md"])
    @patch("src.cli.get_git_diff", return_value="+ # Docs")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_run_pr_pipeline_success(self, mock_stdout, mock_diff, mock_files, mock_is_git):
        args = self.parser.parse_args(["pr"])
        mock_client = MagicMock()
        mock_client.generate_completion.return_value = (
            "feat: update documentation\n\n### Why\n- 문서 갱신\n\n### What\n- README 보강\n\n### How to Test\n- 육안 확인", 0.95
        )
        mock_client.call_count = 1

        exit_code = run_pr_pipeline(args, client=mock_client)
        self.assertEqual(exit_code, 0)
        output = mock_stdout.getvalue()
        self.assertIn("[생성 결과: Pull Request 초안]", output)
        self.assertIn("### Why", output)
        self.assertIn("### What", output)
        self.assertIn("### How to Test", output)
        self.assertIn("AI API 호출 횟수 : 1회", output)

    def test_argument_parsing_repo_options(self):
        # --repo
        args1 = self.parser.parse_args(["commit", "--repo", "C:/test/repo"])
        self.assertEqual(args1.repo, "C:/test/repo")

        # -r
        args2 = self.parser.parse_args(["commit", "-r", "/custom/path"])
        self.assertEqual(args2.repo, "/custom/path")

        # -C
        args3 = self.parser.parse_args(["pr", "-C", "../other-project"])
        self.assertEqual(args3.repo, "../other-project")

    @patch("os.path.isdir", return_value=False)
    @patch("sys.stderr", new_callable=io.StringIO)
    def test_run_commit_pipeline_invalid_repo_directory(self, mock_stderr, mock_isdir):
        args = self.parser.parse_args(["commit", "--repo", "non_existent_folder_xyz"])
        exit_code = run_commit_pipeline(args)
        self.assertEqual(exit_code, 1)
        self.assertIn("지정한 저장소 경로가 존재하지 않거나 디렉토리가 아닙니다", mock_stderr.getvalue())

    @patch("os.path.isdir", return_value=True)
    @patch("src.cli.is_git_repository", return_value=False)
    @patch("sys.stderr", new_callable=io.StringIO)
    def test_run_commit_pipeline_repo_not_git(self, mock_stderr, mock_is_git, mock_isdir):
        args = self.parser.parse_args(["commit", "--repo", "some_regular_dir"])
        exit_code = run_commit_pipeline(args)
        self.assertEqual(exit_code, 1)
        self.assertIn("지정한 디렉토리가 Git 저장소가 아닙니다", mock_stderr.getvalue())

    @patch("os.path.isdir", return_value=True)
    @patch("src.cli.is_git_repository", return_value=True)
    @patch("src.cli.get_changed_files", return_value=["src/sample.py"])
    @patch("src.cli.get_git_diff", return_value="+ print('hello')")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_run_commit_pipeline_custom_repo_success(self, mock_stdout, mock_diff, mock_files, mock_is_git, mock_isdir):
        args = self.parser.parse_args(["commit", "--repo", "C:/valid/repo"])
        mock_client = MagicMock()
        mock_client.generate_completion.return_value = (
            "feat: external repo commit\n\n- updated sample.py", 0.8
        )
        mock_client.call_count = 1

        exit_code = run_commit_pipeline(args, client=mock_client)
        self.assertEqual(exit_code, 0)
        output = mock_stdout.getvalue()
        self.assertIn("feat: external repo commit", output)
        self.assertIn("대상 저장소", output)


if __name__ == "__main__":
    unittest.main()
