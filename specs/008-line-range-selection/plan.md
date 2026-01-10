# Implementation Plan: Line Range Selection

**Branch**: `008-line-range-selection` | **Date**: 2026-01-10 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/008-line-range-selection/spec.md`

## Summary

Add a `--lines START-END` option to both `post` and `convert` commands that extracts a subset of lines from the input file before conversion. This enables users to post specific sections from large markdown files in a single command, maintaining the one-command workflow principle.

## Technical Context

**Language/Version**: Python 3.10+ (per pyproject.toml `requires-python = ">=3.10"`)
**Primary Dependencies**: Click 8.0+ (CLI framework), existing md2slack modules
**Storage**: N/A (stateless transformation)
**Testing**: pytest 7.0+ (existing test infrastructure)
**Target Platform**: Cross-platform CLI (macOS, Linux, Windows)
**Project Type**: Single CLI application
**Performance Goals**: Line extraction < 100ms for files up to 10,000 lines
**Constraints**: Must work with both file and stdin input
**Scale/Scope**: Single feature addition to existing CLI

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle                   | Status | Notes                                                                                   |
| :-------------------------- | :----- | :-------------------------------------------------------------------------------------- |
| I. One-Command Workflow     | PASS   | Feature enables single-command posting of file sections (no temp files needed)          |
| II. Faithful Conversion     | PASS   | Line extraction happens before conversion; converter unchanged                          |
| III. Zero Friction          | PASS   | `--lines` is optional with short flag `-l`; omitting it preserves existing behavior     |
| IV. Preview Before Commit   | PASS   | `--lines` works with `convert` command for preview; `--dry-run` still available         |
| V. Professional Output      | PASS   | Error messages include valid range to guide users; no output degradation                |

**Gate Result**: PASS - No violations, proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/008-line-range-selection/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI interface contract)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/md2slack/
├── __init__.py
├── __main__.py
├── cli.py               # MODIFIED: Add --lines option to convert and post commands
├── converter.py         # UNCHANGED
├── slack.py             # UNCHANGED
├── chunker.py           # UNCHANGED
└── tables.py            # UNCHANGED

tests/
├── __init__.py
├── conftest.py          # May add fixtures for multi-line test files
├── test_cli.py          # MODIFIED: Add tests for --lines option
├── test_converter.py    # UNCHANGED
├── test_slack.py        # UNCHANGED
├── test_chunker.py      # UNCHANGED
└── test_tables.py       # UNCHANGED
```

**Structure Decision**: Single project structure. Only `cli.py` requires modification; all line extraction logic is self-contained within CLI command handlers. No new modules needed.

## Complexity Tracking

> No violations - table not required.
