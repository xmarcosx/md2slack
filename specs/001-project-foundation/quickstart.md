# Quickstart: Project Foundation

**Feature**: 001-project-foundation
**Date**: 2026-01-09

## Goal

Get `md2slack --help` working from a fresh clone.

## Prerequisites

- Python 3.10 or higher
- uv package manager installed

## Steps

### 1. Clone and Install

```bash
git clone <repository-url>
cd md2slack
uv pip install -e .
```

### 2. Verify Installation

```bash
md2slack --help
```

Expected output:
```
Usage: md2slack [OPTIONS] COMMAND [ARGS]...

  md2slack - Convert markdown to Slack mrkdwn and post to threads.

Options:
  --help  Show this message and exit.

Commands:
  convert  Convert markdown to Slack mrkdwn format.
  post     Post content to a Slack thread.
```

### 3. Try Subcommands

```bash
md2slack convert
# Output: Convert command is not implemented yet.

md2slack post
# Output: Post command is not implemented yet.
```

### 4. Run Development Tools

```bash
# Install dev dependencies
uv sync --dev

# Run linter
uv run ruff check .

# Run tests
uv run pytest
```

## Troubleshooting

### Command not found

If `md2slack` is not found after installation:
1. Ensure you installed with `-e .` flag
2. Check that your Python environment's bin directory is in PATH
3. Try `python -m md2slack` as an alternative

### Import errors

If you see import errors:
1. Verify Click is installed: `uv pip list | grep click`
2. Reinstall: `uv pip install -e .`

## Next Steps

This feature provides the foundation. Future features will implement:
- `convert`: Markdown to mrkdwn conversion
- `post`: Slack API integration
