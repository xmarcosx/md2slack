### 005 - Slack Integration

**Problem**: No way to post converted content to Slack threads. Users must copy/paste manually.

**Desired State**: `md2slack post --thread <url> --file <path>` posts converted markdown to specified thread.

**Why This Matters**:
1. Constitution Principle I (One-Command Workflow)—convert and post in single command
2. Constitution Principle III (Zero Friction)—thread URL as primary identifier
3. Eliminates the copy/paste step that makes manual formatting tedious

**CLI Interface**:
- Command: `md2slack post --thread <url> --file <path> [--prefix <text>] [--dry-run]`
- Input: Slack thread URL, markdown file
- Output: Success message with link, or error details

**Example**:
- `md2slack post --thread "https://org.slack.com/archives/C0123/p1234567890" --file update.md`
- `--dry-run` shows what would be posted without sending
- `--prefix "Status Update\n\n"` prepends text before converted content

**Notes**:
- Parse thread URL to extract channel ID and thread timestamp
- Token via `SLACK_BOT_TOKEN` env var (1Password integration via `op run`)
- Slack message limit: 40,000 chars. Warn and truncate if exceeded.
- Required OAuth scopes: `chat:write`, optionally `chat:write.public`
- Clear error messages for: invalid URL, missing token, API errors
