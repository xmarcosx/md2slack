# md2slack

<p align="center">
  <img src="logo.png" alt="md2slack logo" width="500">
</p>

A CLI tool for posting formatted markdown updates to Slack threads.

## The Problem

You keep detailed markdown notes while working on client issues—headers, lists, tables, code blocks. When it's time to update the client in a Slack thread, you have two bad options:

1. Paste raw markdown → looks unprofessional
2. Manually reformat for Slack → tedious and error-prone

md2slack handles the conversion and posting in one command.

## Installation

```bash
uv pip install md2slack
```

Or install from source:

```bash
git clone https://github.com/yourusername/md2slack.git
cd md2slack
uv sync
```

## Slack App Setup

1. Create a Slack app at https://api.slack.com/apps
2. Add the following OAuth scopes under **OAuth & Permissions**:
   - `chat:write` — post messages to channels (required)
   - `chat:write.public` — post to channels the bot isn't a member of (optional)
3. Install the app to your workspace
4. Copy the **Bot User OAuth Token** (starts with `xoxb-`)
5. Set the token as an environment variable:

   ```bash
   export SLACK_BOT_TOKEN="xoxb-your-token-here"
   ```

6. Invite the bot to channels where you want to post: `/invite @your-bot-name`

### Using 1Password

If you use 1Password, you can run commands with token injection:

```bash
op run -- md2slack post -t "https://..." update.md
```

## Usage

### Post an update to a thread

```bash
# Copy the thread URL from Slack (right-click on a message → Copy link)
md2slack post --thread "https://yourorg.slack.com/archives/C0123ABCD/p1234567890123456" update.md
```

### Add a prefix to your message

```bash
md2slack post -t "..." update.md --prefix "📋 *Status Update*\n\n"
```

### Post a specific section from a large file

```bash
# Post only lines 45-78 from your notes
md2slack post -t "..." notes.md --lines 45-78

# Preview what will be posted first
md2slack post -t "..." notes.md --lines 45-78 --dry-run
```

### CLI Options

```
md2slack post [OPTIONS] [FILE]

Options:
  -t, --thread TEXT       Slack thread URL (required)
  -p, --prefix TEXT       Text to prepend before content
  -l, --lines START-END   Extract only specified lines (e.g., --lines 10-50)
  -n, --dry-run           Preview without posting
  --help                  Show this message
```

## Markdown Conversion

md2slack converts standard markdown to Slack's mrkdwn format:

| Markdown | Slack mrkdwn |
|----------|--------------|
| `# Heading` | `*Heading*` (bold) |
| `## Heading` | `*Heading*` (bold) |
| `**bold**` | `*bold*` |
| `_italic_` | `_italic_` |
| `~~strike~~` | `~strike~` |
| `[link](url)` | `<url\|link>` |
| `` `code` `` | `` `code` `` |
| ```code block``` | ```code block``` |
| `- list item` | `• list item` |
| `1. numbered` | `1. numbered` |

### Table Handling

Slack doesn't support tables natively. md2slack converts markdown tables to monospace code blocks with aligned columns:

**Input:**

```markdown
| Client | Status | ETA |
|--------|--------|-----|
| DC Prep | In Progress | Friday |
| Ascend | Blocked | TBD |
```

**Output in Slack:**

```
┌──────────┬─────────────┬─────────┐
│ Client   │ Status      │ ETA     │
├──────────┼─────────────┼─────────┤
│ DC Prep  │ In Progress │ Friday  │
│ Ascend   │ Blocked     │ TBD     │
└──────────┴─────────────┴─────────┘
```

## Development

```bash
# Clone and install in development mode
git clone https://github.com/yourusername/md2slack.git
cd md2slack
uv sync --dev

# Run tests
uv run pytest

# Run linting
uv run ruff check .
```

## Project Structure

```
md2slack/
├── src/
│   └── md2slack/
│       ├── __init__.py
│       ├── cli.py          # Click CLI definitions
│       ├── converter.py    # Markdown → mrkdwn conversion
│       ├── slack.py        # Slack API interactions
│       └── tables.py       # Table rendering logic
├── tests/
├── pyproject.toml
└── README.md
```
