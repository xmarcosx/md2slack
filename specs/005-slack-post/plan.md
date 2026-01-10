# Implementation Plan: Slack Post Command

**Branch**: `005-slack-post` | **Date**: 2026-01-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-slack-post/spec.md`

## Summary

Add a `post` command to md2slack that posts converted markdown content directly to Slack threads. The command takes a thread URL (copied from Slack) and a markdown file, parses the URL to extract channel ID and thread timestamp, converts the markdown to mrkdwn, and posts via the Slack API. Supports `--dry-run` for preview and `--prefix` for prepending text.

## Technical Context

**Language/Version**: Python 3.10+ (per pyproject.toml `requires-python = ">=3.10"`)
**Primary Dependencies**: Click 8.0+ (CLI), mistune 3.0+ (markdown), slack_sdk (new - Slack API)
**Storage**: N/A (stateless CLI operation)
**Testing**: pytest 7.0+ (existing infrastructure)
**Target Platform**: macOS/Linux command line
**Project Type**: single (CLI tool)
**Performance Goals**: N/A (single-operation CLI, not performance-critical)
**Constraints**: Slack message limit 40,000 characters; requires `chat:write` OAuth scope
**Scale/Scope**: Single-user CLI tool, one message per invocation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle                    | Status | Evidence                                                                 |
| ---------------------------- | ------ | ------------------------------------------------------------------------ |
| I. One-Command Workflow      | ✅      | `md2slack post --thread <url> --file <path>` is a single command         |
| II. Faithful Conversion      | ✅      | Reuses existing converter; no changes to conversion logic                |
| III. Zero Friction           | ✅      | Thread URL is primary identifier; token via env var; short flags planned |
| IV. Preview Before Commit    | ✅      | `--dry-run` flag shows output without posting                            |
| V. Professional Output       | ✅      | Clear error messages for all failure modes; graceful truncation          |

**Quality Standards**:
- Test coverage: URL parsing and error handling will have unit tests; API calls mocked
- Error handling: All failure modes produce distinct, actionable messages (FR-010)
- Code style: Will pass `ruff check` (existing CI requirement)

## Project Structure

### Documentation (this feature)

```text
specs/005-slack-post/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (Slack API contract)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/md2slack/
├── __init__.py          # Existing
├── __main__.py          # Existing
├── cli.py               # Existing - add post command implementation
├── converter.py         # Existing - no changes
├── tables.py            # Existing - no changes
└── slack.py             # NEW - Slack API client and URL parsing

tests/
├── test_cli.py          # Existing - add post command tests
├── test_converter.py    # Existing - no changes
├── test_tables.py       # Existing - no changes
└── test_slack.py        # NEW - URL parsing and API client tests
```

**Structure Decision**: Single project structure. New `slack.py` module handles Slack-specific logic (URL parsing, API client). CLI integration in existing `cli.py`. Follows established pattern from converter/tables modules.

## Complexity Tracking

> No violations - design follows all Constitution principles without exceptions.
