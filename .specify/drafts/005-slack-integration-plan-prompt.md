# Prompt: Slack Integration Implementation

_For use with /speckit.plan_
_Source: .specify/specs/005-slack-integration/spec.md_
_Generated: 2026-01-10_

---

The Slack integration builds on the existing `convert` command infrastructure and adds a new `slack.py` module for API interactions. The `post` command in `cli.py` is already stubbed out and needs to be wired up. The implementation naturally splits into three pieces: URL parsing to extract channel ID and thread timestamp, the Slack API client for posting messages, and the CLI glue that ties them together.

For the Slack client, use the official `slack_sdk` package since it handles authentication, rate limiting, and error responses properly. The client should be a thin wrapper that takes the bot token, channel ID, thread_ts, and message text, then calls `chat.postMessage`. Keep it simple and let the SDK handle retries. URL parsing is pure string manipulation with regex to extract the channel ID (starts with C, D, or G) and convert the timestamp from Slack's `p1234567890123456` format to the `1234567890.123456` format the API expects.

Testing should mock the Slack API calls to avoid hitting real endpoints. The URL parsing logic is pure and can be unit tested directly with various URL formats. Integration testing with a real Slack workspace is optional but valuable for verifying the end-to-end flow works correctly. Error handling tests should cover the common failure modes: malformed URLs, missing or invalid tokens, and API errors like channel_not_found or not_in_channel.
