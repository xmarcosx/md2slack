# CLI Contract: Convert Command

**Feature**: 004-convert-command
**Date**: 2026-01-10

## Command Signature

```
md2slack convert [OPTIONS] [FILE]
```

## Arguments

| Argument | Type | Required | Description                      |
| -------- | ---- | -------- | -------------------------------- |
| FILE     | path | No       | Path to markdown file to convert |

## Options

| Option         | Short | Type   | Default | Description                    |
| -------------- | ----- | ------ | ------- | ------------------------------ |
| --text         | -t    | string | None    | Markdown text to convert       |
| --help         |       | flag   |         | Show help message and exit     |

## Input Precedence

1. `--text` value (if provided)
2. `FILE` contents (if path provided)
3. stdin (if not a TTY)
4. Error (if none of the above)

## Output Streams

| Stream | Content                              | When                       |
| ------ | ------------------------------------ | -------------------------- |
| stdout | Converted mrkdwn text (no newline)   | Success                    |
| stderr | Error message                        | Failure                    |

## Exit Codes

| Code | Meaning            | Scenario                            |
| ---- | ------------------ | ----------------------------------- |
| 0    | Success            | Conversion completed                |
| 1    | Usage error        | No input provided                   |
| 2    | Invalid argument   | File does not exist (Click default) |

## Examples

### Success Cases

```bash
# File input
$ md2slack convert notes.md
*Heading*

Content here.
$ echo $?
0

# Text option
$ md2slack convert --text "**bold**"
*bold*
$ echo $?
0

# Stdin
$ echo "# Title" | md2slack convert
*Title*
$ echo $?
0
```

### Error Cases

```bash
# Missing file
$ md2slack convert missing.md
Error: Invalid value for 'FILE': Path 'missing.md' does not exist.
$ echo $?
2

# No input
$ md2slack convert
Error: Provide FILE, --text, or pipe markdown to stdin
$ echo $?
1
```

## Compatibility Notes

- Click framework handles argument parsing and validation
- `exists=True` on FILE argument provides automatic existence check
- No trailing newline on output (for clean piping)
