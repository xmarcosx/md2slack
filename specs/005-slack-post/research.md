# Research: Slack Post Command

**Feature**: 005-slack-post
**Date**: 2026-01-10

## 1. Slack SDK Usage

**Decision**: Use `slack_sdk` Python package with `WebClient` for API calls.

**Rationale**: Official Slack SDK handles authentication, rate limiting, retries, and error parsing. Well-maintained and documented.

**Alternatives considered**:
- Raw HTTP requests: More control but requires implementing auth, rate limiting, error handling manually.
- `slackclient` (legacy): Deprecated in favor of `slack_sdk`.

**Key findings**:
- Use `WebClient.chat_postMessage()` with `channel`, `text`, and `thread_ts` parameters
- `thread_ts` MUST be a string, not a float (float causes silent failure)
- Response includes `ts` (timestamp) and `permalink` for the posted message

**Sources**:
- [Slack chat.postMessage reference](https://docs.slack.dev/reference/methods/chat.postMessage/)
- [Python Slack SDK documentation](https://docs.slack.dev/tools/python-slack-sdk/web/)

---

## 2. Thread URL Parsing

**Decision**: Parse URLs with regex pattern `r"archives/([^/]+)/p(\d+)"` to extract channel ID and timestamp.

**Rationale**: Slack permalink format is stable and well-documented. Regex is simple and handles the standard format.

**URL Format**:
```
https://{workspace}.slack.com/archives/{channel_id}/p{timestamp_without_dot}
```

**Example**:
- URL: `https://myorg.slack.com/archives/C0123ABCD/p1234567890123456`
- Channel ID: `C0123ABCD`
- Raw timestamp: `1234567890123456`
- API timestamp: `1234567890.123456` (insert dot at position 10)

**Conversion logic**:
```python
ts = f"{raw_ts[:10]}.{raw_ts[10:]}"
```

**Channel ID prefixes**:
- `C` - Public channels
- `G` - Private channels (groups)
- `D` - Direct messages

**Sources**:
- [Slack chat.getPermalink](https://api.slack.com/methods/chat.getPermalink)
- [Slack Thread Reader implementation](https://openwebui.com/t/peterlyoo/slack_thread_reader)

---

## 3. Error Handling

**Decision**: Map Slack API errors to user-friendly messages with remediation steps.

**Key error codes and handling**:

| Error Code           | User Message                                                      | Remediation                          |
| -------------------- | ----------------------------------------------------------------- | ------------------------------------ |
| `invalid_auth`       | "Authentication failed. Check your SLACK_BOT_TOKEN."              | Re-generate token, verify scopes     |
| `channel_not_found`  | "Channel not found. Verify the thread URL is correct."            | Check URL, ensure channel exists     |
| `not_in_channel`     | "Bot not in channel. Invite the bot with /invite @botname"        | Invite bot to channel                |
| `token_revoked`      | "Token has been revoked. Generate a new SLACK_BOT_TOKEN."         | Create new token                     |
| `ratelimited`        | "Rate limited by Slack. Try again in {retry_after} seconds."      | Wait and retry                       |
| `message_too_long`   | "Message exceeds Slack's 40,000 character limit."                 | Truncate (handled by FR-009)         |
| `missing_scope`      | "Bot lacks required scope. Ensure chat:write is enabled."         | Add scope in Slack app config        |

**Token validation**:
- Check `SLACK_BOT_TOKEN` environment variable before any API call
- Validate token format starts with `xoxb-` (bot tokens)

**Sources**:
- [Slack error troubleshooting](https://api.slack.com/automation/cli/errors)
- [channel_not_found troubleshooting](https://knock.app/blog/troubleshooting-channel-not-found-in-slack-incoming-webhooks)

---

## 4. Character Limit Handling

**Decision**: Warn user and truncate at 39,900 characters (leaving buffer) with truncation indicator.

**Rationale**: Slack enforces 40,000 character limit. Better to truncate gracefully with warning than fail silently or error out.

**Implementation**:
```python
MAX_LENGTH = 39900  # Leave buffer for truncation indicator
TRUNCATION_INDICATOR = "\n\n[Message truncated due to Slack's 40,000 character limit]"

if len(content) > MAX_LENGTH:
    click.echo("Warning: Content exceeds Slack's 40,000 character limit. Truncating.", err=True)
    content = content[:MAX_LENGTH] + TRUNCATION_INDICATOR
```

---

## 5. Required OAuth Scopes

**Decision**: Require `chat:write` scope; recommend `chat:write.public` for posting to channels without joining.

**Scopes**:
- `chat:write` - Required. Post messages to channels the bot is a member of.
- `chat:write.public` - Optional. Post to public channels without being a member.

**Documentation note**: Update README to specify required scopes when setting up Slack app.

---

## 6. Dependency Addition

**Decision**: Add `slack_sdk>=3.0` to `pyproject.toml` dependencies.

**Version rationale**: 3.x is the current stable line with async support and maintained actively.

```toml
dependencies = [
    "click>=8.0",
    "mistune>=3.0,<4.0",
    "slack_sdk>=3.0",
]
```
