# Data Model: Slack Post Command

**Feature**: 005-slack-post
**Date**: 2026-01-10

## Overview

This feature is stateless—no persistent data storage. The data model describes the transient entities used during command execution.

## Entities

### ThreadReference

Parsed representation of a Slack thread URL.

| Field        | Type   | Description                                      | Example               |
| ------------ | ------ | ------------------------------------------------ | --------------------- |
| `channel_id` | string | Slack channel identifier (C, G, or D prefix)     | `C0123ABCD`           |
| `thread_ts`  | string | Parent message timestamp in API format (with .)  | `1234567890.123456`   |
| `workspace`  | string | Slack workspace subdomain (optional, for errors) | `myorg`               |

**Validation rules**:
- `channel_id` must match pattern `^[CGD][A-Z0-9]+$`
- `thread_ts` must match pattern `^\d{10}\.\d{6}$`

**State transitions**: N/A (immutable value object)

---

### PostRequest

Input parameters for posting a message.

| Field     | Type             | Description                                 | Required |
| --------- | ---------------- | ------------------------------------------- | -------- |
| `thread`  | ThreadReference  | Parsed thread URL                           | Yes      |
| `content` | string           | Converted mrkdwn content to post            | Yes      |
| `prefix`  | string \| None   | Optional text to prepend                    | No       |
| `dry_run` | bool             | If true, preview only (no API call)         | No       |

**Validation rules**:
- `content` length must be <= 40,000 characters after prefix applied
- `prefix` is prepended before `content` if provided

---

### PostResult

Result of a successful post operation.

| Field       | Type   | Description                              | Example                                        |
| ----------- | ------ | ---------------------------------------- | ---------------------------------------------- |
| `ts`        | string | Timestamp of the posted message          | `1234567891.000001`                            |
| `permalink` | string | HTTP URL to the posted message           | `https://myorg.slack.com/archives/C.../p...`   |
| `truncated` | bool   | Whether content was truncated            | `false`                                        |

---

### SlackError

Structured error from Slack API.

| Field     | Type   | Description                                   |
| --------- | ------ | --------------------------------------------- |
| `code`    | string | Slack error code (e.g., `channel_not_found`)  |
| `message` | string | User-friendly error message                   |
| `hint`    | string | Remediation suggestion                        |

**Known error codes** (see research.md):
- `invalid_auth`
- `channel_not_found`
- `not_in_channel`
- `token_revoked`
- `ratelimited`
- `message_too_long`
- `missing_scope`

## Relationships

```
ThreadReference <-- parsed from --> Thread URL (string)
PostRequest --> ThreadReference
PostRequest --> content (from converter)
PostResult <-- returned by --> Slack API
SlackError <-- thrown by --> Slack API
```

## Data Flow

```
1. User provides: thread URL + file path (or stdin)
2. Parse thread URL → ThreadReference
3. Read file → markdown string
4. Convert markdown → mrkdwn (existing converter)
5. Apply prefix if provided
6. Validate length, truncate if needed
7. If dry_run: output to stdout, exit
8. Post to Slack API → PostResult or SlackError
9. Display success message with permalink
```
