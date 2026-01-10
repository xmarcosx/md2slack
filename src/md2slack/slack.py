"""Slack API client and URL parsing for md2slack.

This module provides:
- Thread URL parsing to extract channel ID and thread timestamp
- Slack API client for posting messages to threads
- Error mapping for user-friendly error messages
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


@dataclass
class ThreadReference:
    """Parsed representation of a Slack thread URL."""

    channel_id: str
    thread_ts: str
    workspace: str | None = None


class SlackError(Exception):
    """Structured error from Slack API with user-friendly message."""

    def __init__(self, code: str, message: str, hint: str) -> None:
        self.code = code
        self.message = message
        self.hint = hint
        super().__init__(message)


# Thread URL regex pattern
# Matches: https://{workspace}.slack.com/archives/{channel_id}/p{timestamp}
THREAD_URL_PATTERN = re.compile(
    r"https?://([^/]+)\.slack\.com/archives/([^/]+)/p(\d+)"
)

# Slack API error mapping (code -> (message, hint))
ERROR_MAPPING: dict[str, tuple[str, str]] = {
    "invalid_auth": (
        "Authentication failed. Check your SLACK_BOT_TOKEN.",
        "Re-generate token and verify scopes",
    ),
    "channel_not_found": (
        "Channel not found. This can happen if: (1) the URL is incorrect, "
        "(2) the channel is private (requires /invite @botname), "
        "or (3) the token is for a different workspace.",
        "For private channels, invite the bot first",
    ),
    "not_in_channel": (
        "Bot not in channel. Invite the bot with /invite @botname",
        "Invite bot to channel",
    ),
    "token_revoked": (
        "Token has been revoked. Generate a new SLACK_BOT_TOKEN.",
        "Create new token",
    ),
    "ratelimited": (
        "Rate limited by Slack. Try again later.",
        "Wait and retry",
    ),
    "msg_too_long": (
        "Message exceeds Slack's 40,000 character limit.",
        "Content will be truncated",
    ),
    "missing_scope": (
        "Bot lacks required scope. Ensure chat:write is enabled.",
        "Add scope in Slack app config",
    ),
}

# Message length limits
MAX_MESSAGE_LENGTH = 39900  # Leave buffer for truncation indicator
TRUNCATION_INDICATOR = "\n\n[Message truncated due to Slack's 40,000 character limit]"


def parse_thread_url(url: str) -> ThreadReference:
    """Parse a Slack thread URL to extract channel ID and thread timestamp.

    Args:
        url: Slack thread URL (e.g., https://org.slack.com/archives/C0123/p1234567890123456)

    Returns:
        ThreadReference with channel_id, thread_ts, and workspace

    Raises:
        ValueError: If URL format is invalid
    """
    match = THREAD_URL_PATTERN.match(url)
    if not match:
        raise ValueError(
            f"Invalid thread URL format: {url}\n"
            "Expected format: https://workspace.slack.com/archives/CHANNEL/pTIMESTAMP"
        )

    workspace, channel_id, raw_ts = match.groups()

    # Convert raw timestamp (16 digits) to API format (10.6)
    # p1234567890123456 -> 1234567890.123456
    if len(raw_ts) < 11:
        raise ValueError(f"Invalid timestamp in URL: {raw_ts}")

    thread_ts = f"{raw_ts[:10]}.{raw_ts[10:]}"

    return ThreadReference(
        channel_id=channel_id,
        thread_ts=thread_ts,
        workspace=workspace,
    )


def get_token() -> str:
    """Get Slack bot token from environment.

    Returns:
        Slack bot token

    Raises:
        ValueError: If SLACK_BOT_TOKEN is not set
    """
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        raise ValueError(
            "SLACK_BOT_TOKEN not set. "
            "Set this environment variable with your Slack bot token."
        )
    return token


def format_slack_error(error: SlackApiError) -> SlackError:
    """Convert Slack API error to user-friendly SlackError.

    Args:
        error: SlackApiError from the Slack SDK

    Returns:
        SlackError with user-friendly message and hint
    """
    error_code = error.response.get("error", "unknown_error")

    if error_code in ERROR_MAPPING:
        message, hint = ERROR_MAPPING[error_code]
    else:
        message = f"Slack API error: {error_code}"
        hint = "Check the Slack API documentation for this error"

    return SlackError(code=error_code, message=message, hint=hint)


def truncate_content(content: str) -> tuple[str, bool]:
    """Truncate content if it exceeds Slack's message limit.

    Args:
        content: Message content to potentially truncate

    Returns:
        Tuple of (content, was_truncated)
    """
    if len(content) <= MAX_MESSAGE_LENGTH:
        return content, False

    truncated = content[:MAX_MESSAGE_LENGTH] + TRUNCATION_INDICATOR
    return truncated, True


class SlackClient:
    """Client for posting messages to Slack threads."""

    def __init__(self, token: str) -> None:
        """Initialize Slack client with bot token.

        Args:
            token: Slack bot token (xoxb-...)
        """
        self.client = WebClient(token=token)
        self._workspace: str | None = None

    def set_workspace(self, workspace: str) -> None:
        """Set the workspace for permalink construction.

        Args:
            workspace: Slack workspace subdomain
        """
        self._workspace = workspace

    def post_message(
        self, channel_id: str, thread_ts: str, text: str
    ) -> dict[str, str]:
        """Post a message to a Slack thread.

        Args:
            channel_id: Slack channel ID (e.g., C0123ABCD)
            thread_ts: Parent message timestamp (e.g., 1234567890.123456)
            text: Message content in mrkdwn format

        Returns:
            Dict with 'ts' (message timestamp) and 'permalink'

        Raises:
            SlackError: If the API call fails
        """
        try:
            response = self.client.chat_postMessage(
                channel=channel_id,
                text=text,
                thread_ts=thread_ts,
            )

            ts = response.get("ts", "")
            # Construct permalink from response
            ts_no_dot = ts.replace(".", "")
            workspace = self._workspace or "workspace"
            permalink = f"https://{workspace}.slack.com/archives/{channel_id}/p{ts_no_dot}"

            return {
                "ts": ts,
                "permalink": permalink,
            }

        except SlackApiError as e:
            raise format_slack_error(e) from e
