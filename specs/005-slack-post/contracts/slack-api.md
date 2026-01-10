# Slack API Contract

**Feature**: 005-slack-post
**Date**: 2026-01-10

## Overview

This document defines the contract between md2slack and the Slack Web API. We use the official `slack_sdk` Python package which wraps these endpoints.

## Endpoint: chat.postMessage

Posts a message to a channel or thread.

**SDK Method**: `WebClient.chat_postMessage()`

### Request Parameters

| Parameter    | Type   | Required | Description                                      |
| ------------ | ------ | -------- | ------------------------------------------------ |
| `channel`    | string | Yes      | Channel ID (e.g., `C0123ABCD`)                   |
| `text`       | string | Yes      | Message content in mrkdwn format                 |
| `thread_ts`  | string | Yes*     | Parent message timestamp to reply to             |
| `mrkdwn`     | bool   | No       | Enable mrkdwn formatting (default: true)         |

*`thread_ts` is required for our use case (posting to threads).

### Request Example

```python
response = client.chat_postMessage(
    channel="C0123ABCD",
    text="*Status Update*\n\nProject is on track.",
    thread_ts="1234567890.123456"
)
```

### Success Response

```json
{
    "ok": true,
    "channel": "C0123ABCD",
    "ts": "1234567891.000001",
    "message": {
        "type": "message",
        "text": "*Status Update*\n\nProject is on track.",
        "user": "U0123WXYZ",
        "ts": "1234567891.000001",
        "team": "T0123TEAM"
    }
}
```

**Fields we use**:
- `ok`: Boolean success indicator
- `ts`: Timestamp of posted message (used to construct permalink)
- `channel`: Channel where message was posted

### Error Response

```json
{
    "ok": false,
    "error": "channel_not_found"
}
```

**Error codes we handle**:

| Code               | HTTP Status | Description                           |
| ------------------ | ----------- | ------------------------------------- |
| `invalid_auth`     | 401         | Token is invalid or expired           |
| `channel_not_found`| 404         | Channel doesn't exist or inaccessible |
| `not_in_channel`   | 403         | Bot not a member of the channel       |
| `token_revoked`    | 401         | Token has been revoked                |
| `ratelimited`      | 429         | Too many requests                     |
| `msg_too_long`     | 400         | Message exceeds 40,000 characters     |
| `missing_scope`    | 403         | Token lacks required OAuth scope      |

## Authentication

**Method**: Bearer token via `SLACK_BOT_TOKEN` environment variable.

**Token format**: `xoxb-...` (bot token)

**Required scopes**:
- `chat:write` - Post to channels bot is a member of
- `chat:write.public` (optional) - Post to public channels without membership

## Rate Limits

Slack uses a tiered rate limiting system. The `slack_sdk` handles retries automatically.

- **Tier 3**: ~50 requests per minute (chat.postMessage is Tier 3)
- **Response header**: `Retry-After` indicates seconds to wait

## Permalink Construction

After successful posting, construct permalink from response:

```
https://{workspace}.slack.com/archives/{channel}/p{ts_without_dot}
```

Example:
- Response `ts`: `1234567891.000001`
- Channel: `C0123ABCD`
- Permalink: `https://myorg.slack.com/archives/C0123ABCD/p1234567891000001`

Note: Workspace subdomain must be known from original URL or configured.
