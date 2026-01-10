# Implementation Plan: Core Converter

**Branch**: `003-core-converter` | **Date**: 2026-01-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-core-converter/spec.md`

## Summary

Implement a pure-function markdown-to-Slack-mrkdwn converter. The converter parses CommonMark markdown into an AST using mistune, then walks the tree to render each node to Slack's mrkdwn equivalent. Table rendering uses Unicode box-drawing characters in code blocks.

## Technical Context

**Language/Version**: Python 3.10+ (matches pyproject.toml requires-python)
**Primary Dependencies**: Click 8.0+ (CLI), mistune (markdown parsing)
**Storage**: N/A (pure function, no persistence)
**Testing**: pytest 7.0+ with pytest-cov
**Target Platform**: Linux/macOS/Windows CLI
**Project Type**: Single project (CLI tool)
**Performance Goals**: <100ms for 10,000 character documents (from spec SC-005)
**Constraints**: Pure function, no side effects (FR-010); graceful degradation on malformed input (FR-011)
**Scale/Scope**: Single-file input, typical markdown document sizes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. One-Command Workflow | ✅ PASS | Converter is a building block; full workflow comes from CLI integration |
| II. Faithful Conversion | ✅ PASS | All requirements (FR-001 to FR-015) preserve markdown structure/intent |
| III. Zero Friction | N/A | Applies to CLI layer, not converter module |
| IV. Preview Before Commit | ✅ PASS | Pure function enables `convert` subcommand preview |
| V. Professional Output | ✅ PASS | Box-drawing tables, consistent formatting, graceful degradation |

**Quality Standards**:
- Test Coverage: Comprehensive tests for all markdown elements ✅ (required by spec)
- Error Handling: Graceful degradation, no crashes ✅ (FR-011)
- Code Style: ruff check compliance ✅ (will enforce)

## Project Structure

### Documentation (this feature)

```text
specs/003-core-converter/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
src/md2slack/
├── __init__.py          # Package init
├── __main__.py          # Module entry point
├── cli.py               # Click CLI definitions (exists)
├── converter.py         # Main conversion function (NEW)
└── tables.py            # Table rendering logic (NEW)

tests/
├── __init__.py          # Test package init (exists)
├── conftest.py          # Pytest fixtures (exists)
├── test_cli.py          # CLI smoke tests (exists)
├── test_converter.py    # Converter unit tests (NEW)
└── test_tables.py       # Table rendering tests (NEW)
```

**Structure Decision**: Single project structure following existing layout. The converter module (`converter.py`) contains the main `convert()` function. Table rendering is separated to `tables.py` due to complexity of box-drawing logic.

## Constitution Check (Post-Design Re-evaluation)

*Re-evaluated after Phase 1 design completion.*

| Principle | Status | Design Verification |
|-----------|--------|---------------------|
| I. One-Command Workflow | ✅ PASS | `convert()` is a single-call function; integrates with CLI `convert` command |
| II. Faithful Conversion | ✅ PASS | Design preserves: headings (bold), lists (bullets), tables (box-drawing), links (Slack format), code blocks (literal) |
| III. Zero Friction | N/A | Module layer, not CLI layer |
| IV. Preview Before Commit | ✅ PASS | Pure function with no side effects enables safe preview |
| V. Professional Output | ✅ PASS | Box-drawing characters (U+2500 block), consistent escaping, graceful degradation |

**Quality Standards Re-check**:
- Test Coverage: data-model.md defines testable structures; quickstart.md shows expected behaviors ✅
- Error Handling: Empty string, whitespace, malformed markdown all handled gracefully ✅
- Code Style: Will enforce via ruff on implementation ✅

## Complexity Tracking

> No constitution violations. Separate `tables.py` module is justified by the distinct complexity of box-drawing table rendering versus inline element conversion.
