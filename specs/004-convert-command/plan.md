# Implementation Plan: Convert Command

**Branch**: `004-convert-command` | **Date**: 2026-01-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-convert-command/spec.md`

## Summary

The convert command provides a preview mechanism for md2slack, allowing users to see converted mrkdwn output before posting to Slack. **Research revealed that this command is already implemented** in feature 003's work, with functionality exceeding the MVP spec (supports file, `--text`, and stdin input). The remaining work is primarily validation, testing, and documentation.

## Technical Context

**Language/Version**: Python 3.10+ (per pyproject.toml `requires-python = ">=3.10"`)
**Primary Dependencies**: Click 8.0+ (CLI framework), mistune 3.0+ (markdown parsing)
**Storage**: N/A (stateless transformation)
**Testing**: pytest 7.0+ with subprocess-based CLI tests
**Target Platform**: macOS, Linux (any platform with Python 3.10+)
**Project Type**: Single project CLI tool
**Performance Goals**: < 1 second for typical files (< 100KB)
**Constraints**: None specific to this feature
**Scale/Scope**: Single-user CLI tool, processes one file at a time

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle                    | Status | Evidence                                                              |
| ---------------------------- | ------ | --------------------------------------------------------------------- |
| I. One-Command Workflow      | PASS   | `md2slack convert file.md` is single command                          |
| II. Faithful Conversion      | PASS   | Delegates to proven converter module from feature 003                 |
| III. Zero Friction           | PASS   | Positional FILE arg simpler than --file; supports stdin/--text too    |
| IV. Preview Before Commit    | PASS   | This IS the preview mechanism                                         |
| V. Professional Output       | REVIEW | Error messages need verification for actionability                    |

**Post-Design Re-Check**: All principles satisfied. Error message wording to be verified in testing phase.

## Project Structure

### Documentation (this feature)

```text
specs/004-convert-command/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Research findings (existing impl discovered)
├── data-model.md        # Data flow documentation
├── quickstart.md        # Usage guide
├── contracts/
│   └── cli-interface.md # CLI contract specification
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # (created by /speckit.tasks)
```

### Source Code (repository root)

```text
src/md2slack/
├── __init__.py
├── __main__.py          # Entry point
├── cli.py               # CLI commands including convert (ALREADY EXISTS)
├── converter.py         # Markdown→mrkdwn conversion (feature 003)
└── tables.py            # Table rendering (feature 003)

tests/
├── __init__.py
├── conftest.py          # pytest fixtures
├── test_cli.py          # CLI tests (NEEDS EXPANSION)
├── test_converter.py    # Converter unit tests
└── test_tables.py       # Table rendering tests
```

**Structure Decision**: Existing single-project structure. No new directories needed. Primary changes will be in `tests/test_cli.py` to expand test coverage.

## Implementation Status

| Component         | Status           | Notes                                              |
| ----------------- | ---------------- | -------------------------------------------------- |
| CLI command       | COMPLETE         | `src/md2slack/cli.py:21-40`                        |
| File input        | COMPLETE         | Positional `FILE` argument                         |
| Text option       | COMPLETE         | `--text`/`-t` option                               |
| Stdin support     | COMPLETE         | Reads when not TTY                                 |
| Error handling    | PARTIAL          | Click defaults, may need custom messages           |
| Test coverage     | PARTIAL          | Basic tests exist, need error scenario tests       |

## Remaining Work

1. **Verify error message quality** - Check that Click's default messages are "actionable" per Constitution Principle V
2. **Add permission denied test** - Currently untested scenario
3. **Add empty file test** - Edge case from spec
4. **Document variance** - Spec says `--file`, impl uses positional `FILE`

## Complexity Tracking

No complexity violations. Implementation is simpler than spec anticipated.
