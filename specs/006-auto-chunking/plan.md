# Implementation Plan: Auto-Chunking for Long Content

**Branch**: `006-auto-chunking` | **Date**: 2026-01-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/006-auto-chunking/spec.md`

## Summary

When users post long markdown documents to Slack, they hit the 40,000 character limit. Currently md2slack truncates with a warning, losing content. This feature adds intelligent auto-chunking via a `--chunk` flag that splits long content into multiple sequential messages posted to the same thread, preserving code blocks and tables intact.

## Technical Context

**Language/Version**: Python 3.10+ (per pyproject.toml `requires-python = ">=3.10"`)
**Primary Dependencies**: Click 8.0+ (CLI), mistune 3.0+ (markdown), slack_sdk (Slack API)
**Storage**: N/A (stateless CLI operation)
**Testing**: pytest 7.0+ with pytest-cov
**Target Platform**: Cross-platform CLI (macOS, Linux, Windows)
**Project Type**: Single project - Python CLI tool
**Performance Goals**: Process documents of any size; 95%+ splits at natural boundaries
**Constraints**: Slack API rate limits (1 second between posts), 40,000 char/message limit
**Scale/Scope**: Single-user CLI tool for document posting

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle                   | Status | Notes                                                                                           |
| --------------------------- | ------ | ----------------------------------------------------------------------------------------------- |
| I. One-Command Workflow     | PASS   | `md2slack post --chunk --thread URL file.md` - single command, no intermediate steps            |
| II. Faithful Conversion     | PASS   | Chunking operates on converted mrkdwn; preserves code blocks and tables intact                  |
| III. Zero Friction          | PASS   | Single `--chunk` flag enables feature; optional `--chunk-size` for power users                  |
| IV. Preview Before Commit   | PASS   | `--dry-run` will show all chunks before posting                                                 |
| V. Professional Output      | PASS   | Intelligent split points (paragraph > sentence > hard); continuation indicators; warns on edge cases |

**Gate Result**: PASS - All principles satisfied. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/006-auto-chunking/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A - no API contracts for CLI feature)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/md2slack/
├── __init__.py
├── __main__.py
├── cli.py               # MODIFY: Add --chunk and --chunk-size flags to post command
├── converter.py         # NO CHANGE: Conversion happens before chunking
├── slack.py             # MODIFY: Add post_chunked_messages method to SlackClient
├── tables.py            # NO CHANGE
└── chunker.py           # NEW: Content chunking logic

tests/
├── conftest.py
├── test_cli.py          # MODIFY: Add chunking CLI tests
├── test_converter.py    # NO CHANGE
├── test_tables.py       # NO CHANGE
├── test_slack.py        # MODIFY: Add chunked posting tests
└── test_chunker.py      # NEW: Comprehensive chunker unit tests
```

**Structure Decision**: Single project structure. New `chunker.py` module contains self-contained chunking algorithm. Modifications to `cli.py` for flags and `slack.py` for multi-message posting.

## Complexity Tracking

> No Constitution violations requiring justification. Design follows existing patterns.

| Area            | Complexity | Rationale                                             |
| --------------- | ---------- | ----------------------------------------------------- |
| New module      | Low        | `chunker.py` is self-contained, pure function design  |
| CLI changes     | Low        | Two new flags on existing command                     |
| Slack changes   | Low        | Loop with delay over existing `post_message` method   |
| Testing         | Medium     | Requires comprehensive boundary detection tests       |
