# Research: Line Range Selection

**Feature**: 008-line-range-selection
**Date**: 2026-01-10

## Research Tasks

### 1. Click Option Patterns for Range Values

**Question**: How should the `--lines` option parse `START-END` format?

**Decision**: Use Click's string option with custom validation callback.

**Rationale**: Click doesn't have a built-in range type. A string option with a validation callback provides:
- Clear error messages for invalid formats
- Flexibility to validate START <= END
- Ability to return a tuple (start, end) for downstream use

**Alternatives Considered**:
- Two separate options (`--start-line`, `--end-line`): Rejected - more verbose, violates zero-friction principle
- Click's `nargs=2` with type=int: Rejected - requires space-separated values, less intuitive than `START-END`

**Implementation Pattern**:
```python
def parse_line_range(ctx, param, value):
    if value is None:
        return None
    # Parse "START-END" format, validate, return tuple
```

### 2. Line Extraction from Content

**Question**: Where should line extraction occur in the command flow?

**Decision**: Extract lines immediately after reading file/stdin content, before any conversion.

**Rationale**:
- Keeps converter unchanged (receives markdown string, doesn't know about lines)
- Chunking operates on converted output (unaffected)
- Slack posting operates on chunks (unaffected)
- Single point of extraction for both `post` and `convert` commands

**Implementation Pattern**:
```python
# After reading content:
if lines:
    start, end = lines
    content = extract_lines(content, start, end)
# Then proceed with conversion...
```

### 3. Error Message Format

**Question**: What should error messages include for invalid ranges?

**Decision**: Include the file's actual line count to enable immediate correction.

**Rationale**: Constitution Principle V requires "clear and actionable" error messages. Showing valid range eliminates guesswork.

**Examples**:
- `Error: Line range 150-200 is out of bounds. File has 100 lines (valid range: 1-100).`
- `Error: Invalid line range '50-30'. Start line must be less than or equal to end line.`
- `Error: Invalid --lines format 'abc'. Expected START-END (e.g., --lines 10-50).`

### 4. stdin Line Counting

**Question**: How to handle `--lines` with stdin input?

**Decision**: Read stdin into memory first, then apply line extraction.

**Rationale**:
- stdin must be fully read before line count is known
- Memory usage is acceptable (typical markdown files are small)
- Consistent behavior whether input is file or stdin

**Implementation Note**: Current code already reads stdin fully with `sys.stdin.read()`.

### 5. Existing CLI Patterns

**Question**: How do existing options work in `cli.py`?

**Findings from code review**:
- `convert` command: Takes `file` (optional) and `--text` (optional), reads stdin if neither
- `post` command: Takes `file` (optional), requires `--thread`, has `--prefix`, `--dry-run`, `--chunk-size`
- Both commands read file content early, then process

**Integration Point**: Add `--lines` option to both commands after file/stdin reading, before conversion.

## Summary

| Topic                     | Decision                                             |
| :------------------------ | :--------------------------------------------------- |
| Option format             | `--lines START-END` with `-l` short flag             |
| Parsing                   | Custom Click callback returning `(start, end)` tuple |
| Extraction point          | After reading content, before conversion             |
| Error messages            | Include file's actual line count                     |
| stdin handling            | Read fully, then extract lines                       |
| Module changes            | `cli.py` only                                        |
