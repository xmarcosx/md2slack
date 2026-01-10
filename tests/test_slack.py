"""Tests for Slack API client and URL parsing."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from slack_sdk.errors import SlackApiError

from md2slack.slack import (
    MAX_MESSAGE_LENGTH,
    TRUNCATION_INDICATOR,
    SlackClient,
    SlackError,
    ThreadReference,
    format_slack_error,
    get_token,
    parse_thread_url,
    truncate_content,
)

# =============================================================================
# parse_thread_url Tests (T005, T006)
# =============================================================================


class TestParseThreadUrl:
    """Tests for parse_thread_url function."""

    def test_valid_url_public_channel(self):
        """Parse valid URL with public channel (C prefix)."""
        url = "https://myorg.slack.com/archives/C0123ABCD/p1234567890123456"
        result = parse_thread_url(url)

        assert isinstance(result, ThreadReference)
        assert result.channel_id == "C0123ABCD"
        assert result.thread_ts == "1234567890.123456"
        assert result.workspace == "myorg"

    def test_valid_url_private_channel(self):
        """Parse valid URL with private channel (G prefix)."""
        url = "https://company.slack.com/archives/G9876ZYXW/p9876543210654321"
        result = parse_thread_url(url)

        assert result.channel_id == "G9876ZYXW"
        assert result.thread_ts == "9876543210.654321"
        assert result.workspace == "company"

    def test_valid_url_direct_message(self):
        """Parse valid URL with DM channel (D prefix)."""
        url = "https://team.slack.com/archives/D1111AAAA/p1111111111222222"
        result = parse_thread_url(url)

        assert result.channel_id == "D1111AAAA"
        assert result.thread_ts == "1111111111.222222"

    def test_valid_url_http(self):
        """Parse URL with http (not https)."""
        url = "http://myorg.slack.com/archives/C0123ABCD/p1234567890123456"
        result = parse_thread_url(url)

        assert result.channel_id == "C0123ABCD"
        assert result.thread_ts == "1234567890.123456"

    def test_invalid_url_missing_protocol(self):
        """Reject URL without protocol."""
        with pytest.raises(ValueError, match="Invalid thread URL format"):
            parse_thread_url("myorg.slack.com/archives/C0123ABCD/p1234567890123456")

    def test_invalid_url_wrong_domain(self):
        """Reject URL with wrong domain."""
        with pytest.raises(ValueError, match="Invalid thread URL format"):
            parse_thread_url("https://example.com/archives/C0123ABCD/p1234567890123456")

    def test_invalid_url_missing_archives(self):
        """Reject URL without /archives/ path."""
        with pytest.raises(ValueError, match="Invalid thread URL format"):
            parse_thread_url("https://myorg.slack.com/messages/C0123ABCD/p1234567890123456")

    def test_invalid_url_missing_timestamp(self):
        """Reject URL without timestamp."""
        with pytest.raises(ValueError, match="Invalid thread URL format"):
            parse_thread_url("https://myorg.slack.com/archives/C0123ABCD")

    def test_invalid_url_short_timestamp(self):
        """Reject URL with too-short timestamp."""
        with pytest.raises(ValueError, match="Invalid timestamp"):
            parse_thread_url("https://myorg.slack.com/archives/C0123ABCD/p123")

    def test_invalid_url_empty_string(self):
        """Reject empty URL."""
        with pytest.raises(ValueError, match="Invalid thread URL format"):
            parse_thread_url("")

    def test_url_with_query_params(self):
        """Parse URL with query parameters (should fail - not a clean URL)."""
        # Slack URLs with query params aren't in standard format
        url = "https://myorg.slack.com/archives/C0123ABCD/p1234567890123456?foo=bar"
        # This should actually still work because regex matches up to timestamp
        result = parse_thread_url(url)
        assert result.channel_id == "C0123ABCD"


# =============================================================================
# get_token Tests (T017)
# =============================================================================


class TestGetToken:
    """Tests for get_token function."""

    def test_token_from_environment(self, monkeypatch):
        """Get token from SLACK_BOT_TOKEN environment variable."""
        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-token-123")
        token = get_token()
        assert token == "xoxb-test-token-123"

    def test_missing_token_raises_error(self, monkeypatch):
        """Raise ValueError when SLACK_BOT_TOKEN is not set."""
        monkeypatch.delenv("SLACK_BOT_TOKEN", raising=False)
        with pytest.raises(ValueError, match="SLACK_BOT_TOKEN not set"):
            get_token()

    def test_empty_token_raises_error(self, monkeypatch):
        """Raise ValueError when SLACK_BOT_TOKEN is empty."""
        monkeypatch.setenv("SLACK_BOT_TOKEN", "")
        with pytest.raises(ValueError, match="SLACK_BOT_TOKEN not set"):
            get_token()


# =============================================================================
# Error Mapping Tests (T009, T010, T011)
# =============================================================================


class TestFormatSlackError:
    """Tests for format_slack_error function."""

    def _make_slack_error(self, error_code: str) -> SlackApiError:
        """Create a mock SlackApiError with given error code."""
        response = MagicMock()
        response.get.return_value = error_code
        response.__getitem__ = lambda self, key: error_code if key == "error" else None
        error = SlackApiError(message=f"Error: {error_code}", response=response)
        return error

    def test_invalid_auth_error(self):
        """Map invalid_auth to authentication failed message."""
        error = self._make_slack_error("invalid_auth")
        result = format_slack_error(error)

        assert isinstance(result, SlackError)
        assert result.code == "invalid_auth"
        assert "Authentication failed" in result.message
        assert "SLACK_BOT_TOKEN" in result.message

    def test_channel_not_found_error(self):
        """Map channel_not_found to channel not found message."""
        error = self._make_slack_error("channel_not_found")
        result = format_slack_error(error)

        assert result.code == "channel_not_found"
        assert "Channel not found" in result.message

    def test_not_in_channel_error(self):
        """Map not_in_channel to bot not in channel message."""
        error = self._make_slack_error("not_in_channel")
        result = format_slack_error(error)

        assert result.code == "not_in_channel"
        assert "Bot not in channel" in result.message
        assert "/invite" in result.message

    def test_token_revoked_error(self):
        """Map token_revoked to token revoked message."""
        error = self._make_slack_error("token_revoked")
        result = format_slack_error(error)

        assert result.code == "token_revoked"
        assert "revoked" in result.message.lower()

    def test_ratelimited_error(self):
        """Map ratelimited to rate limit message."""
        error = self._make_slack_error("ratelimited")
        result = format_slack_error(error)

        assert result.code == "ratelimited"
        assert "Rate limited" in result.message

    def test_msg_too_long_error(self):
        """Map msg_too_long to message too long error."""
        error = self._make_slack_error("msg_too_long")
        result = format_slack_error(error)

        assert result.code == "msg_too_long"
        assert "40,000" in result.message

    def test_missing_scope_error(self):
        """Map missing_scope to missing scope message."""
        error = self._make_slack_error("missing_scope")
        result = format_slack_error(error)

        assert result.code == "missing_scope"
        assert "chat:write" in result.message

    def test_unknown_error_code(self):
        """Handle unknown error codes gracefully."""
        error = self._make_slack_error("some_unknown_error")
        result = format_slack_error(error)

        assert result.code == "some_unknown_error"
        assert "some_unknown_error" in result.message
        assert "documentation" in result.hint.lower()


# =============================================================================
# Content Truncation Tests (T021, T022)
# =============================================================================


class TestTruncateContent:
    """Tests for truncate_content function."""

    def test_short_content_not_truncated(self):
        """Short content should not be truncated."""
        content = "Hello, world!"
        result, was_truncated = truncate_content(content)

        assert result == content
        assert was_truncated is False

    def test_exact_limit_not_truncated(self):
        """Content at exactly MAX_MESSAGE_LENGTH should not be truncated."""
        content = "x" * MAX_MESSAGE_LENGTH
        result, was_truncated = truncate_content(content)

        assert result == content
        assert was_truncated is False

    def test_over_limit_truncated(self):
        """Content over limit should be truncated with indicator."""
        content = "x" * (MAX_MESSAGE_LENGTH + 100)
        result, was_truncated = truncate_content(content)

        assert was_truncated is True
        assert len(result) == MAX_MESSAGE_LENGTH + len(TRUNCATION_INDICATOR)
        assert result.endswith(TRUNCATION_INDICATOR)

    def test_truncation_preserves_beginning(self):
        """Truncation should preserve the beginning of content."""
        prefix = "IMPORTANT: "
        content = prefix + "x" * (MAX_MESSAGE_LENGTH + 100)
        result, was_truncated = truncate_content(content)

        assert was_truncated is True
        assert result.startswith(prefix)


# =============================================================================
# SlackClient Tests (T007, T008)
# =============================================================================


class TestSlackClient:
    """Tests for SlackClient class."""

    def test_client_initialization(self):
        """Client initializes with token."""
        client = SlackClient("xoxb-test-token")
        assert client.client is not None

    def test_set_workspace(self):
        """Setting workspace updates internal state."""
        client = SlackClient("xoxb-test-token")
        client.set_workspace("myorg")
        assert client._workspace == "myorg"

    @patch("md2slack.slack.WebClient")
    def test_post_message_success(self, mock_webclient_class):
        """Post message returns ts and permalink on success."""
        # Setup mock
        mock_client = MagicMock()
        mock_webclient_class.return_value = mock_client
        mock_client.chat_postMessage.return_value = {
            "ok": True,
            "ts": "1234567891.000001",
            "channel": "C0123ABCD",
        }

        client = SlackClient("xoxb-test-token")
        client.set_workspace("myorg")

        result = client.post_message(
            channel_id="C0123ABCD",
            thread_ts="1234567890.123456",
            text="Hello, thread!",
        )

        assert result["ts"] == "1234567891.000001"
        assert "myorg.slack.com" in result["permalink"]
        assert "C0123ABCD" in result["permalink"]

        mock_client.chat_postMessage.assert_called_once_with(
            channel="C0123ABCD",
            text="Hello, thread!",
            thread_ts="1234567890.123456",
        )

    @patch("md2slack.slack.WebClient")
    def test_post_message_api_error(self, mock_webclient_class):
        """Post message raises SlackError on API error."""
        # Setup mock to raise SlackApiError
        mock_client = MagicMock()
        mock_webclient_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.get.return_value = "channel_not_found"
        mock_client.chat_postMessage.side_effect = SlackApiError(
            message="Error", response=mock_response
        )

        client = SlackClient("xoxb-test-token")

        with pytest.raises(SlackError) as exc_info:
            client.post_message(
                channel_id="C0123ABCD",
                thread_ts="1234567890.123456",
                text="Hello!",
            )

        assert exc_info.value.code == "channel_not_found"
        assert "Channel not found" in exc_info.value.message
