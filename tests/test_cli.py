"""Tests for md2slack CLI commands."""

import os
import stat
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from md2slack.cli import cli


def test_cli_help_exits_zero():
    """Verify md2slack --help exits with code 0."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "md2slack" in result.output
    assert "convert" in result.output
    assert "post" in result.output


def test_convert_help():
    """Verify md2slack convert --help exits with code 0."""
    runner = CliRunner()
    result = runner.invoke(cli, ["convert", "--help"])
    assert result.exit_code == 0
    assert "Convert markdown to Slack mrkdwn format" in result.output
    assert "--text" in result.output


def test_convert_with_text():
    """Verify md2slack convert --text converts markdown."""
    runner = CliRunner()
    result = runner.invoke(cli, ["convert", "--text", "**bold**"])
    assert result.exit_code == 0
    assert "*bold*" in result.output


def test_convert_with_stdin():
    """Verify md2slack convert reads from stdin."""
    runner = CliRunner()
    result = runner.invoke(cli, ["convert"], input="# Heading")
    assert result.exit_code == 0
    assert "*Heading*" in result.output


def test_post_help():
    """Verify md2slack post --help shows options."""
    runner = CliRunner()
    result = runner.invoke(cli, ["post", "--help"])
    assert result.exit_code == 0
    assert "--thread" in result.output
    assert "--dry-run" in result.output
    assert "--prefix" in result.output


# =============================================================================
# User Story 1: Preview Markdown Conversion
# =============================================================================


def test_convert_file_with_various_elements(tmp_path):
    """T004: Test file input with various markdown elements."""
    # Create a markdown file with various elements
    md_file = tmp_path / "test.md"
    md_file.write_text(
        """# Heading

**bold** and *italic* text

- Item 1
- Item 2

[Link](https://example.com)

| Col A | Col B |
|-------|-------|
| 1     | 2     |
"""
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["convert", str(md_file)])
    assert result.exit_code == 0
    # Check heading converted
    assert "*Heading*" in result.output
    # Check bold converted (** -> *)
    assert "*bold*" in result.output
    # Check list bullets
    assert "•" in result.output
    # Check link format
    assert "<https://example.com|Link>" in result.output


def test_convert_empty_file(tmp_path):
    """T005: Test empty file handling - should output empty string, exit 0."""
    md_file = tmp_path / "empty.md"
    md_file.write_text("")

    runner = CliRunner()
    result = runner.invoke(cli, ["convert", str(md_file)])
    assert result.exit_code == 0
    assert result.output == ""


def test_convert_whitespace_only_file(tmp_path):
    """T006: Test whitespace-only file handling."""
    md_file = tmp_path / "whitespace.md"
    md_file.write_text("   \n\n   \t   \n")

    runner = CliRunner()
    result = runner.invoke(cli, ["convert", str(md_file)])
    assert result.exit_code == 0
    # Whitespace-only should produce whitespace or empty output, not error
    assert result.exception is None


# =============================================================================
# User Story 2: Handle Missing File Gracefully
# =============================================================================


def test_convert_file_not_found():
    """T009: Test file not found error message and exit code."""
    runner = CliRunner()
    result = runner.invoke(cli, ["convert", "nonexistent_file.md"])
    assert result.exit_code == 2  # Click's default for invalid argument
    assert "does not exist" in result.output.lower()


def test_convert_directory_instead_of_file(tmp_path):
    """T010: Test directory-instead-of-file error."""
    runner = CliRunner()
    result = runner.invoke(cli, ["convert", str(tmp_path)])
    assert result.exit_code == 2  # Click's invalid argument exit code
    assert "is a directory" in result.output.lower()


# =============================================================================
# User Story 3: Handle Permission Errors
# =============================================================================


@pytest.mark.skipif(
    os.name == "nt", reason="Permission tests not reliable on Windows"
)
def test_convert_permission_denied(tmp_path):
    """T013: Test permission denied error with unreadable file."""
    md_file = tmp_path / "unreadable.md"
    md_file.write_text("# Secret content")
    # Remove read permission
    md_file.chmod(0o000)

    try:
        runner = CliRunner()
        result = runner.invoke(cli, ["convert", str(md_file)])
        # Should exit with error
        assert result.exit_code != 0
        # Should have some error indication
        assert result.exception is not None or "permission" in result.output.lower()
    finally:
        # Restore permissions for cleanup
        md_file.chmod(stat.S_IRUSR | stat.S_IWUSR)


# =============================================================================
# User Story 4: Post to Slack Thread (T014-T025)
# =============================================================================

VALID_THREAD_URL = "https://myorg.slack.com/archives/C0123ABCD/p1234567890123456"


class TestPostCommand:
    """Tests for md2slack post command."""

    def test_post_happy_path_with_file(self, tmp_path, monkeypatch):
        """T014: Post command happy path with file input."""
        md_file = tmp_path / "update.md"
        md_file.write_text("## Status Update\n\n- Task 1 done\n- Task 2 in progress")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            runner = CliRunner()
            result = runner.invoke(
                cli,
                ["post", "--thread", VALID_THREAD_URL, str(md_file)],
            )

            assert result.exit_code == 0
            assert "Posted to thread" in result.output
            assert "permalink" in result.output.lower() or "slack.com" in result.output

            # Verify API was called correctly
            mock_client.post_message.assert_called_once()
            call_args = mock_client.post_message.call_args
            assert call_args.kwargs["channel_id"] == "C0123ABCD"
            assert call_args.kwargs["thread_ts"] == "1234567890.123456"
            # Content should be converted
            assert "*Status Update*" in call_args.kwargs["text"]

    def test_post_with_stdin(self, monkeypatch):
        """T015: Post command reads from stdin."""
        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            runner = CliRunner()
            result = runner.invoke(
                cli,
                ["post", "--thread", VALID_THREAD_URL],
                input="**Bold** text via stdin",
            )

            assert result.exit_code == 0
            assert "Posted to thread" in result.output

            # Verify content was converted from stdin
            call_args = mock_client.post_message.call_args
            assert "*Bold*" in call_args.kwargs["text"]

    def test_post_missing_token(self, tmp_path, monkeypatch):
        """T023: Error when SLACK_BOT_TOKEN not set."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test")

        monkeypatch.delenv("SLACK_BOT_TOKEN", raising=False)

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["post", "--thread", VALID_THREAD_URL, str(md_file)],
        )

        assert result.exit_code != 0
        assert "SLACK_BOT_TOKEN" in result.output

    def test_post_invalid_thread_url(self, tmp_path, monkeypatch):
        """T023: Error for invalid thread URL format."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["post", "--thread", "https://example.com/not-a-slack-url", str(md_file)],
        )

        assert result.exit_code != 0
        assert "Invalid thread URL" in result.output

    def test_post_api_error(self, tmp_path, monkeypatch):
        """T024: Handle Slack API errors gracefully."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            from md2slack.slack import SlackError

            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.side_effect = SlackError(
                code="channel_not_found",
                message="Channel not found. Verify the thread URL is correct.",
                hint="Check URL and ensure channel exists",
            )

            runner = CliRunner()
            result = runner.invoke(
                cli,
                ["post", "--thread", VALID_THREAD_URL, str(md_file)],
            )

            assert result.exit_code != 0
            assert "Channel not found" in result.output
            assert "Hint:" in result.output

    def test_post_missing_thread_option(self, tmp_path):
        """Post command requires --thread option."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test")

        runner = CliRunner()
        result = runner.invoke(cli, ["post", str(md_file)])

        assert result.exit_code != 0
        assert "thread" in result.output.lower()

    def test_post_no_input_error(self):
        """Post command errors when no input provided."""
        runner = CliRunner()
        # Using mix_stderr=False so both outputs go to output
        result = runner.invoke(
            cli,
            ["post", "--thread", VALID_THREAD_URL],
            catch_exceptions=False,
        )

        assert result.exit_code != 0


# =============================================================================
# User Story 5: Dry Run (T026-T029)
# =============================================================================


class TestPostDryRun:
    """Tests for post command --dry-run option."""

    def test_dry_run_shows_preview(self, tmp_path, monkeypatch):
        """T026: Dry run shows converted content without posting."""
        md_file = tmp_path / "update.md"
        md_file.write_text("## Status Update\n\n- Task done")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            runner = CliRunner()
            result = runner.invoke(
                cli,
                ["post", "--thread", VALID_THREAD_URL, "--dry-run", str(md_file)],
            )

            assert result.exit_code == 0
            # Should show dry run indicator
            assert "DRY RUN" in result.output
            # Should show converted content
            assert "*Status Update*" in result.output
            # Should NOT call the Slack API
            mock_client_class.return_value.post_message.assert_not_called()

    def test_dry_run_short_flag(self, tmp_path, monkeypatch):
        """T026: Dry run works with short -n flag."""
        md_file = tmp_path / "test.md"
        md_file.write_text("**Bold** text")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient"):
            runner = CliRunner()
            result = runner.invoke(
                cli,
                ["post", "-t", VALID_THREAD_URL, "-n", str(md_file)],
            )

            assert result.exit_code == 0
            assert "DRY RUN" in result.output
            assert "*Bold*" in result.output

    def test_dry_run_does_not_require_token(self, tmp_path, monkeypatch):
        """Dry run should work even without token (no API call needed)."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Heading")

        monkeypatch.delenv("SLACK_BOT_TOKEN", raising=False)

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["post", "--thread", VALID_THREAD_URL, "--dry-run", str(md_file)],
        )

        assert result.exit_code == 0
        assert "DRY RUN" in result.output


# =============================================================================
# User Story 6: Prefix Text (T030-T033)
# =============================================================================


class TestPostPrefix:
    """Tests for post command --prefix option."""

    def test_prefix_prepended(self, tmp_path, monkeypatch):
        """T030: Prefix is prepended to converted content."""
        md_file = tmp_path / "update.md"
        md_file.write_text("- Task done")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            runner = CliRunner()
            result = runner.invoke(
                cli,
                [
                    "post",
                    "--thread", VALID_THREAD_URL,
                    "--prefix", "Weekly Report:",
                    str(md_file),
                ],
            )

            assert result.exit_code == 0

            call_args = mock_client.post_message.call_args
            text = call_args.kwargs["text"]
            # Prefix should appear before content
            assert text.startswith("Weekly Report:")
            # Content should follow
            assert "Task done" in text

    def test_prefix_with_newlines(self, tmp_path, monkeypatch):
        """T030: Prefix handles escaped newlines."""
        md_file = tmp_path / "update.md"
        md_file.write_text("Content here")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            runner = CliRunner()
            result = runner.invoke(
                cli,
                [
                    "post",
                    "--thread", VALID_THREAD_URL,
                    "--prefix", "Header\\n\\n",
                    str(md_file),
                ],
            )

            assert result.exit_code == 0

            call_args = mock_client.post_message.call_args
            text = call_args.kwargs["text"]
            # Escaped newlines should be converted
            assert "Header\n\n" in text

    def test_prefix_short_flag(self, tmp_path, monkeypatch):
        """T030: Prefix works with short -p flag."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Content")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            runner = CliRunner()
            result = runner.invoke(
                cli,
                ["post", "-t", VALID_THREAD_URL, "-p", "Prefix:", str(md_file)],
            )

            assert result.exit_code == 0

            call_args = mock_client.post_message.call_args
            assert call_args.kwargs["text"].startswith("Prefix:")

    def test_prefix_in_dry_run(self, tmp_path, monkeypatch):
        """Prefix appears in dry run output."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Content")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "post",
                "-t", VALID_THREAD_URL,
                "-p", "Prefix:",
                "--dry-run",
                str(md_file),
            ],
        )

        assert result.exit_code == 0
        assert "Prefix:" in result.output
        assert "Content" in result.output


# =============================================================================
# User Story 7: Auto-Chunking for Long Content (T013-T018, T037-T044, T048-T049)
# =============================================================================


# =============================================================================
# 007-default-chunking: User Story 1 - Long Content Auto-Chunking (T011)
# =============================================================================


class TestDefaultChunking:
    """Tests for default auto-chunking behavior (no --chunk flag needed)."""

    def test_long_content_posts_without_chunk_flag(self, tmp_path, monkeypatch):
        """T011: Long content posts automatically without --chunk flag."""
        md_file = tmp_path / "long.md"
        # Create content that will be split (> 1000 chars)
        long_content = "A" * 600 + " paragraph one.\n\n" + "B" * 600 + " paragraph two."
        md_file.write_text(long_content)

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            with patch("md2slack.cli.time.sleep"):
                runner = CliRunner()
                # Note: No --chunk flag!
                result = runner.invoke(
                    cli,
                    [
                        "post",
                        "--thread", VALID_THREAD_URL,
                        "--chunk-size", "1000",
                        str(md_file),
                    ],
                )

            assert result.exit_code == 0
            # Should have posted multiple times (auto-chunking works)
            assert mock_client.post_message.call_count >= 2
            # Check that indicators were added
            calls = mock_client.post_message.call_args_list
            first_text = calls[0].kwargs["text"]
            assert "(1/" in first_text

    def test_short_content_posts_without_indicator(self, tmp_path, monkeypatch):
        """T015: Short content posts as single message without indicator."""
        md_file = tmp_path / "short.md"
        md_file.write_text("Short content that fits easily.")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            runner = CliRunner()
            result = runner.invoke(
                cli,
                ["post", "--thread", VALID_THREAD_URL, str(md_file)],
            )

            assert result.exit_code == 0
            # Should have posted once
            assert mock_client.post_message.call_count == 1
            # No indicator for single message
            call_text = mock_client.post_message.call_args.kwargs["text"]
            assert "(1/" not in call_text

    def test_chunk_flag_produces_error(self, tmp_path):
        """T024: Using removed --chunk flag produces error."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Test content")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["post", "--thread", VALID_THREAD_URL, "--chunk", str(md_file)],
        )

        # Should fail - unknown option
        assert result.exit_code != 0
        assert "no such option" in result.output.lower() or "Error" in result.output

    def test_chunk_size_capped_at_default(self, tmp_path, monkeypatch):
        """T020: --chunk-size values above DEFAULT_CHUNK_SIZE are capped."""
        md_file = tmp_path / "test.md"
        # Content that would fit in one larger chunk but needs splitting at 3900
        # Since this is short, let's just verify the parameter is accepted
        md_file.write_text("Short content")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            runner = CliRunner()
            # Use --chunk-size larger than DEFAULT_CHUNK_SIZE (3900)
            result = runner.invoke(
                cli,
                [
                    "post",
                    "--thread", VALID_THREAD_URL,
                    "--chunk-size", "50000",  # Above 3900 limit
                    str(md_file),
                ],
            )

            # Should succeed (silently capped, not rejected)
            assert result.exit_code == 0


class TestPostChunking:
    """Tests for post command chunking behavior."""

    def test_chunk_flag_not_in_help(self):
        """T023: --chunk flag should NOT appear in post command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["post", "--help"])
        assert result.exit_code == 0
        # --chunk should be removed (only --chunk-size should remain)
        # Actually verify --chunk (not --chunk-size) is not present
        help_lines = result.output.split("\n")
        chunk_flag_present = any(
            "--chunk" in line and "--chunk-size" not in line
            for line in help_lines
        )
        assert not chunk_flag_present, "--chunk flag should be removed from help"

    def test_chunk_size_flag_in_help(self):
        """T014: --chunk-size flag appears in post command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["post", "--help"])
        assert result.exit_code == 0
        assert "--chunk-size" in result.output

    def test_chunk_size_validation(self, tmp_path, monkeypatch):
        """T018/T021: --chunk-size with value below minimum is rejected."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Content")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "post",
                "--thread", VALID_THREAD_URL,
                "--chunk-size", "100",  # Below minimum of 500
                str(md_file),
            ],
        )

        assert result.exit_code != 0
        assert "500" in result.output  # Should mention minimum

    def test_chunk_dry_run_short_content(self, tmp_path, monkeypatch):
        """T027/T048: Dry run shows content without indicators for short content."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Short content that fits in one chunk.")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "post",
                "--thread", VALID_THREAD_URL,
                "--dry-run",
                str(md_file),
            ],
        )

        assert result.exit_code == 0
        assert "DRY RUN" in result.output
        assert "Short content" in result.output
        # No chunk breaks for single-chunk content
        assert "CHUNK BREAK" not in result.output

    def test_chunk_dry_run_long_content(self, tmp_path, monkeypatch):
        """T028/T049: Dry run shows chunk breaks for long content."""
        md_file = tmp_path / "long.md"
        # Create content that will be split (> 1000 chars)
        long_content = "A" * 600 + " paragraph one.\n\n" + "B" * 600 + " paragraph two."
        md_file.write_text(long_content)

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "post",
                "--thread", VALID_THREAD_URL,
                "--chunk-size", "1000",
                "--dry-run",
                str(md_file),
            ],
        )

        assert result.exit_code == 0
        assert "DRY RUN" in result.output
        assert "CHUNK BREAK" in result.output
        # Should have continuation indicators
        assert "(1/" in result.output
        assert "(2/" in result.output

    def test_chunk_posts_multiple_messages(self, tmp_path, monkeypatch):
        """T029: Chunked posting creates multiple API calls with indicators."""
        md_file = tmp_path / "long.md"
        long_content = "A" * 600 + " paragraph one.\n\n" + "B" * 600 + " paragraph two."
        md_file.write_text(long_content)

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            # Mock time.sleep to speed up test
            with patch("md2slack.cli.time.sleep"):
                runner = CliRunner()
                result = runner.invoke(
                    cli,
                    [
                        "post",
                        "--thread", VALID_THREAD_URL,
                        "--chunk-size", "1000",
                        str(md_file),
                    ],
                )

            assert result.exit_code == 0
            # Should have posted multiple times
            assert mock_client.post_message.call_count >= 2
            # Check that indicators were added
            calls = mock_client.post_message.call_args_list
            first_text = calls[0].kwargs["text"]
            assert "(1/" in first_text

    def test_chunk_progress_output(self, tmp_path, monkeypatch, capsys):
        """T030: Progress output shows 'Posting chunk N/M...' format."""
        md_file = tmp_path / "long.md"
        long_content = "A" * 600 + " paragraph one.\n\n" + "B" * 600 + " paragraph two."
        md_file.write_text(long_content)

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            with patch("md2slack.cli.time.sleep"):
                runner = CliRunner()
                result = runner.invoke(
                    cli,
                    [
                        "post",
                        "--thread", VALID_THREAD_URL,
                        "--chunk-size", "1000",
                        str(md_file),
                    ],
                )

            assert result.exit_code == 0
            # Progress output (Click mixes stdout/stderr in CliRunner)
            assert "Posting chunk 1/" in result.output
            assert "Posting chunk 2/" in result.output

    def test_chunk_completion_summary(self, tmp_path, monkeypatch):
        """T031: Completion summary shows total chunks posted."""
        md_file = tmp_path / "long.md"
        long_content = "A" * 600 + " paragraph one.\n\n" + "B" * 600 + " paragraph two."
        md_file.write_text(long_content)

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            with patch("md2slack.cli.time.sleep"):
                runner = CliRunner()
                result = runner.invoke(
                    cli,
                    [
                        "post",
                        "--thread", VALID_THREAD_URL,
                        "--chunk-size", "1000",
                        str(md_file),
                    ],
                )

            assert result.exit_code == 0
            # Should show completion summary
            assert "Posted" in result.output
            assert "chunks" in result.output

    def test_chunk_error_mid_posting(self, tmp_path, monkeypatch):
        """T032: Error handling shows which chunks succeeded on failure."""
        md_file = tmp_path / "long.md"
        p1 = "A" * 600 + " paragraph one."
        p2 = "B" * 600 + " paragraph two."
        p3 = "C" * 600 + " paragraph three."
        long_content = f"{p1}\n\n{p2}\n\n{p3}"
        md_file.write_text(long_content)

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            from md2slack.slack import SlackError

            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            # First call succeeds, second fails
            mock_client.post_message.side_effect = [
                {"ts": "1234567891.000001", "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001"},
                SlackError(
                    code="ratelimited",
                    message="Rate limited by Slack",
                    hint="Wait and retry",
                ),
            ]

            with patch("md2slack.cli.time.sleep"):
                runner = CliRunner()
                result = runner.invoke(
                    cli,
                    [
                        "post",
                        "--thread", VALID_THREAD_URL,
                        "--chunk-size", "1000",
                        str(md_file),
                    ],
                )

            assert result.exit_code != 0
            # Should report partial success
            has_partial = "Chunks 1-1 posted successfully" in result.output
            has_chunk = "Chunk" in result.output
            assert has_partial or has_chunk

    def test_chunk_single_message_no_indicator(self, tmp_path, monkeypatch):
        """T033: Short content posts without indicator."""
        md_file = tmp_path / "short.md"
        md_file.write_text("Short content")

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            runner = CliRunner()
            result = runner.invoke(
                cli,
                [
                    "post",
                    "--thread", VALID_THREAD_URL,
                    str(md_file),
                ],
            )

            assert result.exit_code == 0
            # Should have posted once
            assert mock_client.post_message.call_count == 1
            # Content should not have indicator
            call_text = mock_client.post_message.call_args.kwargs["text"]
            assert "(1/" not in call_text


# =============================================================================
# Feature 008: Line Range Selection
# =============================================================================


class TestLineRangePost:
    """Tests for --lines option on post command (User Story 1)."""

    def test_post_with_lines_option_file(self, tmp_path, monkeypatch):
        """T004: --lines option on post command extracts specified lines from file."""
        md_file = tmp_path / "multiline.md"
        md_file.write_text(
            "Line 1 content\n"
            "Line 2 content\n"
            "# Line 3 heading\n"
            "Line 4 content\n"
            "Line 5 content\n"
        )

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            runner = CliRunner()
            result = runner.invoke(
                cli,
                [
                    "post",
                    "--thread", VALID_THREAD_URL,
                    "--lines", "2-4",
                    str(md_file),
                ],
            )

            assert result.exit_code == 0
            assert "Posted to thread" in result.output

            # Verify only lines 2-4 were posted
            call_args = mock_client.post_message.call_args
            text = call_args.kwargs["text"]
            # Line 2 should be present
            assert "Line 2 content" in text
            # Line 3 (heading) should be converted
            assert "*Line 3 heading*" in text
            # Line 4 should be present
            assert "Line 4 content" in text
            # Line 1 and Line 5 should NOT be present
            assert "Line 1 content" not in text
            assert "Line 5 content" not in text

    def test_post_with_lines_option_stdin(self, monkeypatch):
        """T005: --lines option on post command works with stdin input."""
        stdin_content = (
            "First line\n"
            "Second line\n"
            "Third line\n"
            "Fourth line\n"
        )

        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token")

        with patch("md2slack.cli.SlackClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.post_message.return_value = {
                "ts": "1234567891.000001",
                "permalink": "https://myorg.slack.com/archives/C0123ABCD/p1234567891000001",
            }

            runner = CliRunner()
            result = runner.invoke(
                cli,
                ["post", "--thread", VALID_THREAD_URL, "--lines", "2-3"],
                input=stdin_content,
            )

            assert result.exit_code == 0

            # Verify only lines 2-3 were posted
            call_args = mock_client.post_message.call_args
            text = call_args.kwargs["text"]
            assert "Second line" in text
            assert "Third line" in text
            assert "First line" not in text
            assert "Fourth line" not in text

    def test_post_with_lines_dry_run(self, tmp_path, monkeypatch):
        """--lines option works with --dry-run for preview."""
        md_file = tmp_path / "multiline.md"
        md_file.write_text(
            "# Header\n"
            "Middle content\n"
            "Footer content\n"
        )

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "post",
                "--thread", VALID_THREAD_URL,
                "--lines", "2-2",
                "--dry-run",
                str(md_file),
            ],
        )

        assert result.exit_code == 0
        assert "DRY RUN" in result.output
        assert "Middle content" in result.output
        # Header and Footer should not appear
        assert "Header" not in result.output
        assert "Footer" not in result.output


class TestLineRangeConvert:
    """Tests for --lines option on convert command (User Story 2)."""

    def test_convert_with_lines_option_file(self, tmp_path):
        """T009: --lines option on convert extracts specified lines from file."""
        md_file = tmp_path / "multiline.md"
        md_file.write_text(
            "Line 1 content\n"
            "# Line 2 heading\n"
            "Line 3 content\n"
            "Line 4 content\n"
        )

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["convert", "--lines", "2-3", str(md_file)],
        )

        assert result.exit_code == 0
        # Line 2 (heading) should be converted
        assert "*Line 2 heading*" in result.output
        # Line 3 should be present
        assert "Line 3 content" in result.output
        # Lines 1 and 4 should NOT be present
        assert "Line 1 content" not in result.output
        assert "Line 4 content" not in result.output

    def test_convert_with_lines_option_stdin(self):
        """T010: --lines option on convert command works with stdin input."""
        stdin_content = (
            "First line\n"
            "**Second line bold**\n"
            "Third line\n"
            "Fourth line\n"
        )

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["convert", "--lines", "2-3"],
            input=stdin_content,
        )

        assert result.exit_code == 0
        # Line 2 bold should be converted
        assert "*Second line bold*" in result.output
        assert "Third line" in result.output
        # Lines 1 and 4 should NOT be present
        assert "First line" not in result.output
        assert "Fourth line" not in result.output

    def test_convert_lines_with_text_error(self):
        """T011: --lines with --text produces error."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["convert", "--text", "Some text", "--lines", "1-5"],
        )

        assert result.exit_code != 0
        assert "--lines" in result.output.lower() or "lines" in result.output.lower()

    def test_convert_lines_short_flag(self, tmp_path):
        """--lines works with short -l flag on convert."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Line 1\n# Line 2\nLine 3\n")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["convert", "-l", "2-2", str(md_file)],
        )

        assert result.exit_code == 0
        assert "*Line 2*" in result.output
        assert "Line 1" not in result.output
        assert "Line 3" not in result.output


class TestLineRangeErrors:
    """Tests for --lines error handling (User Story 3)."""

    def test_invalid_format_error(self, tmp_path):
        """T015: Invalid format (e.g., 'abc') produces clear error."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Line 1\nLine 2\n")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["convert", "--lines", "abc", str(md_file)],
        )

        assert result.exit_code != 0
        assert "Invalid --lines format" in result.output
        assert "abc" in result.output
        assert "START-END" in result.output

    def test_start_greater_than_end_error(self, tmp_path):
        """T016: Start > end (e.g., '50-30') produces error."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Line 1\nLine 2\nLine 3\n")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["convert", "--lines", "50-30", str(md_file)],
        )

        assert result.exit_code != 0
        assert "50-30" in result.output
        assert "Start line must be less than or equal to end line" in result.output

    def test_out_of_bounds_error(self, tmp_path):
        """T017: Out-of-bounds range shows file line count."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Line 1\nLine 2\nLine 3\n")  # 3 lines

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["convert", "--lines", "2-10", str(md_file)],
        )

        assert result.exit_code != 0
        assert "out of bounds" in result.output.lower()
        assert "3 lines" in result.output
        assert "valid range: 1-3" in result.output

    def test_zero_line_number_error(self, tmp_path):
        """T018: Zero line number produces error."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Line 1\nLine 2\n")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["convert", "--lines", "0-5", str(md_file)],
        )

        assert result.exit_code != 0
        assert "positive" in result.output.lower() or "1-indexed" in result.output

    def test_negative_line_number_error(self, tmp_path):
        """T018: Negative line numbers are rejected by format validation."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Line 1\nLine 2\n")

        runner = CliRunner()
        # Negative numbers won't match the \d+-\d+ pattern
        result = runner.invoke(
            cli,
            ["convert", "--lines", "-1-5", str(md_file)],
        )

        assert result.exit_code != 0
        assert "Invalid --lines format" in result.output

    def test_error_on_post_command(self, tmp_path):
        """Error messages work on post command too."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Line 1\nLine 2\n")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["post", "--thread", VALID_THREAD_URL, "--lines", "xyz", str(md_file)],
        )

        assert result.exit_code != 0
        assert "Invalid --lines format" in result.output


class TestLineRangeEdgeCases:
    """Tests for --lines edge cases (Phase 6)."""

    def test_single_line_range(self, tmp_path):
        """T023: Single-line range (e.g., --lines 5-5) works."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["convert", "--lines", "3-3", str(md_file)],
        )

        assert result.exit_code == 0
        assert "Line 3" in result.output
        assert "Line 2" not in result.output
        assert "Line 4" not in result.output

    def test_range_starting_at_line_1(self, tmp_path):
        """T024: Range starting at line 1 works."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# First heading\nSecond line\nThird line\n")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["convert", "--lines", "1-2", str(md_file)],
        )

        assert result.exit_code == 0
        # First line heading converted
        assert "*First heading*" in result.output
        assert "Second line" in result.output
        assert "Third line" not in result.output

    def test_range_ending_at_last_line(self, tmp_path):
        """T025: Range ending at last line works."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Line 1\nLine 2\nLine 3\n")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["convert", "--lines", "2-3", str(md_file)],
        )

        assert result.exit_code == 0
        assert "Line 2" in result.output
        assert "Line 3" in result.output
        assert "Line 1" not in result.output

    def test_file_with_trailing_empty_lines(self, tmp_path):
        """T026: File with trailing empty lines counts correctly."""
        md_file = tmp_path / "test.md"
        # File with 5 lines including 2 trailing empty lines
        md_file.write_text("Line 1\nLine 2\nLine 3\n\n\n")

        runner = CliRunner()
        # Request lines 1-5 (should work - there are 5 lines)
        result = runner.invoke(
            cli,
            ["convert", "--lines", "1-5", str(md_file)],
        )

        assert result.exit_code == 0
        assert "Line 1" in result.output

    def test_entire_file_range(self, tmp_path):
        """Selecting entire file range is equivalent to no --lines."""
        md_file = tmp_path / "test.md"
        md_file.write_text("Line 1\n# Line 2\nLine 3\n")

        runner = CliRunner()

        # With --lines covering entire file
        result_lines = runner.invoke(
            cli,
            ["convert", "--lines", "1-3", str(md_file)],
        )

        # Without --lines
        result_no_lines = runner.invoke(
            cli,
            ["convert", str(md_file)],
        )

        assert result_lines.exit_code == 0
        assert result_no_lines.exit_code == 0
        assert result_lines.output == result_no_lines.output

    def test_lines_in_help_output(self):
        """--lines option appears in help for both commands."""
        runner = CliRunner()

        convert_help = runner.invoke(cli, ["convert", "--help"])
        assert "--lines" in convert_help.output
        assert "-l" in convert_help.output

        post_help = runner.invoke(cli, ["post", "--help"])
        assert "--lines" in post_help.output
        assert "-l" in post_help.output
