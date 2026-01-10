# Implementation Plan: Project Foundation

**Branch**: `001-project-foundation` | **Date**: 2026-01-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-project-foundation/spec.md`

## Summary

Bootstrap md2slack as an installable Python package with a working CLI entry point. Create the src-layout directory structure, pyproject.toml with dependencies (Click for runtime, ruff/pytest for dev), and a minimal CLI module with placeholder subcommands for `convert` and `post`.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: Click (CLI framework)
**Storage**: N/A (no data storage in this feature)
**Testing**: pytest (smoke test only for this feature)
**Target Platform**: Linux/macOS/Windows (cross-platform CLI)
**Project Type**: Single Python package with src-layout
**Performance Goals**: N/A (infrastructure feature)
**Constraints**: Must work with uv package manager
**Scale/Scope**: Single CLI entry point with 2 placeholder subcommands

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. One-Command Workflow | PASS | CLI will be single command; subcommands are natural CLI structure |
| II. Faithful Conversion | N/A | No conversion logic in this feature |
| III. Zero Friction | PASS | Default behavior shows help; minimal required args |
| IV. Preview Before Commit | N/A | No posting logic in this feature |
| V. Professional Output | PASS | Help text will be clear and well-formatted |

**Quality Standards Check**:
- Code Style: Will configure ruff as dev dependency
- Error Handling: Placeholder commands exit with clear messages
- Test Coverage: Smoke test for CLI invocation

**Verdict**: All applicable principles satisfied. No violations.

## Project Structure

### Documentation (this feature)

```text
specs/001-project-foundation/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (minimal for CLI tool)
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output (CLI interface contract)
```

### Source Code (repository root)

```text
src/
└── md2slack/
    ├── __init__.py      # Package init with version
    └── cli.py           # Click CLI definitions

tests/
└── test_cli.py          # Smoke test for CLI invocation

pyproject.toml           # Package metadata, dependencies, entry points
```

**Structure Decision**: Single Python package using src-layout as specified in requirements. The `src/md2slack/` directory contains the package code with CLI module. Tests are at the root level in `tests/` directory. This matches the architecture described in CLAUDE.md.

## Complexity Tracking

No violations requiring justification. This is a minimal infrastructure feature.
