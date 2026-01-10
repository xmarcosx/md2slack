# Quickstart: Slack Post Command

**Feature**: 005-slack-post
**Date**: 2026-01-10

## Prerequisites

1. **Slack Bot Token**: Create a Slack app with `chat:write` scope
2. **1Password**: Store token as `SLACK_BOT_TOKEN` (see `op-env-refs`)
3. **Bot Membership**: Invite bot to target channels with `/invite @botname`

## Installation

```bash
# Install with slack_sdk dependency
uv sync
```

## Basic Usage

### Post to a Thread

```bash
# Copy thread URL from Slack (right-click → Copy link)
md2slack post --thread "https://myorg.slack.com/archives/C0123ABCD/p1234567890123456" --file update.md
```

### Preview Before Posting (Dry Run)

```bash
md2slack post --thread "https://..." --file update.md --dry-run
```

### Add a Prefix

```bash
md2slack post --thread "https://..." --file update.md --prefix "📊 Weekly Report\n\n"
```

### Pipe from stdin

```bash
cat update.md | md2slack post --thread "https://..."
```

## CLI Reference

```
md2slack post [OPTIONS] [FILE]

Options:
  --thread, -t TEXT   Slack thread URL (required)
  --prefix, -p TEXT   Text to prepend before content
  --dry-run, -n       Preview without posting
  --help              Show this message and exit
```

## Environment Variables

| Variable          | Description                    | Required |
| ----------------- | ------------------------------ | -------- |
| `SLACK_BOT_TOKEN` | Bot token with `chat:write`    | Yes      |

## Example Workflow

```bash
# 1. Write your update in markdown
echo "## Status Update

- ✅ Completed feature X
- 🚧 Working on feature Y
- ⏳ Blocked on review for Z" > update.md

# 2. Preview the conversion
md2slack convert update.md

# 3. Preview what will be posted (dry-run)
md2slack post -t "https://..." -f update.md --dry-run

# 4. Post to the thread
md2slack post -t "https://..." -f update.md
# Output: ✓ Posted to thread: https://myorg.slack.com/archives/C.../p...
```

## Error Messages

| Error                                  | Solution                                           |
| -------------------------------------- | -------------------------------------------------- |
| "SLACK_BOT_TOKEN not set"              | Set env var or use `op run`                        |
| "Invalid thread URL format"            | Use URL from Slack's "Copy link" menu              |
| "Bot not in channel"                   | Run `/invite @botname` in the channel              |
| "Authentication failed"                | Check token is valid, has correct scopes           |
| "Content exceeds 40,000 characters"    | Content will be truncated with warning             |

## Running with 1Password

```bash
# Using op run to inject token
op run -- md2slack post -t "https://..." -f update.md
```
