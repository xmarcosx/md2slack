# CLI Interface Contract: Line Range Selection

**Feature**: 008-line-range-selection
**Date**: 2026-01-10

## Option Specification

### --lines / -l

| Attribute     | Value                                           |
| :------------ | :---------------------------------------------- |
| Long form     | `--lines`                                       |
| Short form    | `-l`                                            |
| Type          | String (format: `START-END`)                    |
| Required      | No                                              |
| Default       | None (process entire file)                      |
| Commands      | `convert`, `post`                               |

**Format**: `START-END` where both are positive integers (1-indexed, inclusive).

**Examples**:
- `--lines 10-50` - Extract lines 10 through 50
- `-l 1-1` - Extract only line 1
- `-l 100-200` - Extract lines 100 through 200

## Command Signatures

### convert

```text
md2slack convert [FILE] [OPTIONS]

Options:
  -t, --text TEXT      Markdown text to convert (alternative to file)
  -l, --lines START-END  Extract only specified line range (1-indexed, inclusive)
  --help               Show this message and exit
```

### post

```text
md2slack post [FILE] [OPTIONS]

Options:
  -t, --thread TEXT    Slack thread URL (required)
  -p, --prefix TEXT    Text to prepend before converted content
  -n, --dry-run        Preview output without posting to Slack
  --chunk-size INT     Max chars per chunk
  -l, --lines START-END  Extract only specified line range (1-indexed, inclusive)
  --help               Show this message and exit
```

## Error Responses

### Invalid Format

**Trigger**: `--lines` value doesn't match `START-END` pattern.

```text
Error: Invalid --lines format 'abc'. Expected START-END (e.g., --lines 10-50).
```

### Start Greater Than End

**Trigger**: START > END (e.g., `--lines 50-30`).

```text
Error: Invalid line range '50-30'. Start line must be less than or equal to end line.
```

### Out of Bounds

**Trigger**: Range extends beyond file's actual line count.

```text
Error: Line range 150-200 is out of bounds. File has 100 lines (valid range: 1-100).
```

### Zero or Negative Values

**Trigger**: START or END is 0 or negative.

```text
Error: Invalid line range '0-10'. Line numbers must be positive (1-indexed).
```

## Behavior Contract

| Scenario                          | Expected Behavior                                         |
| :-------------------------------- | :-------------------------------------------------------- |
| `--lines` omitted                 | Process entire file (existing behavior)                   |
| `--lines 5-10` with file          | Extract lines 5-10 from file, process extracted content   |
| `--lines 5-10` with stdin         | Read stdin, extract lines 5-10, process extracted content |
| `--lines 5-5`                     | Extract single line 5                                     |
| `--lines 1-N` where N=total lines | Extract entire file (same as omitting option)             |
| `--lines` with `--text`           | Error: `--lines` requires file or stdin input             |
