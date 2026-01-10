# Quickstart: Convert Command

**Feature**: 004-convert-command
**Date**: 2026-01-10

## Prerequisites

- Python 3.10+
- uv package manager
- Repository cloned locally

## Setup

```bash
# Install dependencies
uv sync --dev

# Verify installation
uv run md2slack --help
```

## Usage

### Convert a file

```bash
uv run md2slack convert notes.md
```

### Convert inline text

```bash
uv run md2slack convert --text "**bold** and _italic_"
```

### Convert from stdin (piping)

```bash
echo "# Heading" | uv run md2slack convert
cat update.md | uv run md2slack convert
```

## Expected Output

Input markdown:
```markdown
# Status Update

**Project**: md2slack
- Task 1 completed
- Task 2 in progress

See [docs](https://example.com) for details.
```

Output mrkdwn:
```
*Status Update*

*Project*: md2slack
• Task 1 completed
• Task 2 in progress

See <https://example.com|docs> for details.
```

## Error Handling

### File not found
```bash
$ uv run md2slack convert missing.md
Error: Invalid value for 'FILE': Path 'missing.md' does not exist.
$ echo $?
2
```

### No input provided
```bash
$ uv run md2slack convert
Error: Provide FILE, --text, or pipe markdown to stdin
$ echo $?
1
```

## Running Tests

```bash
# All tests
uv run pytest

# CLI tests only
uv run pytest tests/test_cli.py -v

# With coverage
uv run pytest --cov=md2slack
```

## Development Notes

- Converter module: `src/md2slack/converter.py`
- CLI module: `src/md2slack/cli.py`
- Tests: `tests/test_cli.py`
- The convert command calls `convert_markdown()` which uses mistune for parsing
