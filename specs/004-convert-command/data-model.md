# Data Model: Convert Command

**Feature**: 004-convert-command
**Date**: 2026-01-10

## Overview

The convert command is a stateless transformation with no persistent data storage. It operates as a pure function: markdown text in, mrkdwn text out.

## Entities

### Input

| Field    | Type   | Description                        | Source                  |
| -------- | ------ | ---------------------------------- | ----------------------- |
| markdown | string | Raw markdown content to convert    | File, --text, or stdin  |

### Output

| Field   | Type   | Description                        | Destination |
| ------- | ------ | ---------------------------------- | ----------- |
| mrkdwn  | string | Converted Slack mrkdwn content     | stdout      |
| error   | string | Error message (on failure only)    | stderr      |
| code    | int    | Exit code (0=success, 1=failure)   | process     |

## State Transitions

```
[No File] --read--> [Markdown String] --convert--> [Mrkdwn String] --echo--> [stdout]
                                                          |
[File Error] -----------------------------------------> [stderr + exit 1]
```

## Validation Rules

1. **Input source precedence**: `--text` > `FILE` > stdin
2. **File validation**: Must exist and be readable (Click's `exists=True` handles existence)
3. **Empty input**: Valid - produces empty output with exit 0

## Relationships

```
convert command
    └── depends on: md2slack.converter.convert()
                        └── depends on: md2slack.tables (for table rendering)
```

## Notes

- No database or file storage
- No configuration state
- No user sessions or authentication
- Pure functional transformation
