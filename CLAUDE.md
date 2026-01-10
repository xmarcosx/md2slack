# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

md2slack is a CLI tool for converting markdown to Slack's mrkdwn format and posting to Slack threads. The project uses Python with uv for package management.

## Development Commands

```bash
# Install dependencies (dev mode)
uv sync --dev

# Run tests
uv run pytest

# Run linting
uv run ruff check .
```

## Architecture

Planned structure (from README):
- `src/md2slack/cli.py` - Click CLI definitions
- `src/md2slack/converter.py` - Markdown → mrkdwn conversion
- `src/md2slack/slack.py` - Slack API interactions
- `src/md2slack/tables.py` - Table rendering (converts markdown tables to monospace box-drawing format)
- `src/md2slack/config.py` - Config file handling

## Key Functionality

The converter transforms:
- Headings → bold text
- `**bold**` → `*bold*`
- `~~strike~~` → `~strike~`
- `[link](url)` → `<url|link>`
- Lists → bullet points (•)
- Tables → monospace code blocks with box-drawing characters

## Environment

Uses 1Password for secrets. The `SLACK_BOT_TOKEN` is stored in 1Password (see `op-env-refs`).

## Speckit Integration

This repo uses speckit for feature planning. Use `/specify`, `/plan`, `/tasks`, and `/implement` commands for the feature development workflow.

## Active Technologies
- Python 3.10+ + Click (CLI framework) (001-project-foundation)
- N/A (no data storage in this feature) (001-project-foundation)
- Python 3.10+ + Click 8.0+, pytest 7.0+ (002-testing-foundation)
- N/A (no data storage) (002-testing-foundation)
- Python 3.10+ (matches pyproject.toml requires-python) + Click 8.0+ (CLI), mistune (markdown parsing) (003-core-converter)
- N/A (pure function, no persistence) (003-core-converter)
- Python 3.10+ (per pyproject.toml `requires-python = ">=3.10"`) + Click 8.0+ (CLI framework), mistune 3.0+ (markdown parsing) (004-convert-command)
- N/A (stateless transformation) (004-convert-command)
- Python 3.10+ (per pyproject.toml `requires-python = ">=3.10"`) + Click 8.0+ (CLI), mistune 3.0+ (markdown), slack_sdk (new - Slack API) (005-slack-post)
- N/A (stateless CLI operation) (005-slack-post)
- Python 3.10+ (per pyproject.toml `requires-python = ">=3.10"`) + Click 8.0+ (CLI), mistune 3.0+ (markdown), slack_sdk (Slack API) (006-auto-chunking)
- Python 3.10+ (per pyproject.toml `requires-python = ">=3.10"`) + Click 8.0+ (CLI framework), existing md2slack modules (008-line-range-selection)

## Recent Changes
- 001-project-foundation: Added Python 3.10+ + Click (CLI framework)

## Subagent Configuration

Always use `model: "opus"` when spawning Task subagents. Do not use haiku or sonnet for any subagent tasks.
