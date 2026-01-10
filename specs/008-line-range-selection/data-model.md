# Data Model: Line Range Selection

**Feature**: 008-line-range-selection
**Date**: 2026-01-10

## Overview

This feature is stateless and does not introduce persistent data structures. The only data involved is the transient line range value passed via CLI option.

## Entities

### LineRange (transient)

Represents a validated range of line numbers for extraction.

| Field | Type    | Description                              | Constraints            |
| :---- | :------ | :--------------------------------------- | :--------------------- |
| start | integer | First line to include (1-indexed)        | >= 1                   |
| end   | integer | Last line to include (1-indexed)         | >= start               |

**Validation Rules**:
- Both `start` and `end` must be positive integers
- `start` must be less than or equal to `end`
- Both values must be within the file's actual line count (1 to total_lines)

**Source**: Parsed from `--lines START-END` CLI option string.

## State Transitions

N/A - No state changes. Line extraction is a pure function that takes content and range, returns extracted content.

## Data Flow

```text
User Input                Processing                   Output
-----------              -----------                  ------
--lines "45-78"  →  parse to (45, 78)  →  validate against file  →  extract lines 45-78
                                             ↓
                                        Error if invalid
```

## Relationships

- **LineRange → Content**: Applied to raw markdown content (file or stdin)
- **Content → Converter**: Extracted content passed to existing converter (unchanged)
- **Converter → Chunker → Slack**: Downstream pipeline unchanged
