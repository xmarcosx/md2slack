# Implementation Plan: Testing Foundation

**Branch**: `002-testing-foundation` | **Date**: 2026-01-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-testing-foundation/spec.md`

## Summary

Set up test fixtures and infrastructure to support TDD workflow for upcoming features. The basic pytest configuration already exists from feature 001 - this feature adds shared fixtures for markdown conversion testing and file-based input scenarios.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: Click 8.0+, pytest 7.0+
**Storage**: N/A (no data storage)
**Testing**: pytest (already configured in pyproject.toml)
**Target Platform**: CLI tool (Linux, macOS, Windows)
**Project Type**: Single Python package
**Performance Goals**: N/A for test infrastructure
**Constraints**: Fixtures should be minimal - only what's needed for next feature (003-core-converter)
**Scale/Scope**: Small CLI tool, ~5-10 test modules expected

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. One-Command Workflow | N/A | Testing infrastructure, not user-facing |
| II. Faithful Conversion | SUPPORTS | Fixtures enable comprehensive conversion tests |
| III. Zero Friction | N/A | Testing infrastructure, not user-facing |
| IV. Preview Before Commit | N/A | Testing infrastructure, not user-facing |
| V. Professional Output | N/A | Testing infrastructure, not user-facing |
| Quality Standards - Test Coverage | SUPPORTS | This feature enables test coverage |
| Development Workflow | COMPLIANT | Uses `uv run pytest` as specified |

**Gate Status**: PASS - No violations. Feature supports constitution's Quality Standards.

## Project Structure

### Documentation (this feature)

```text
specs/002-testing-foundation/
├── plan.md              # This file
├── research.md          # Phase 0 output (minimal - no unknowns)
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
# Existing structure (from feature 001)
src/
└── md2slack/
    ├── __init__.py
    ├── __main__.py
    └── cli.py

# Test structure (to be created/enhanced)
tests/
├── __init__.py          # Exists
├── conftest.py          # NEW: Shared fixtures
└── test_cli.py          # Exists (3 smoke tests)
```

**Structure Decision**: Single project structure. Tests mirror source - currently only `test_cli.py` exists. As more source modules are added (converter.py, tables.py, slack.py), corresponding test files will be added.

## Complexity Tracking

No violations - no complexity tracking needed.

## Existing State Analysis

Feature 001 already established:
- pytest>=7.0 in dev dependencies
- `[tool.pytest.ini_options]` in pyproject.toml with `testpaths = ["tests"]`
- `tests/` directory with `__init__.py` and `test_cli.py`
- `uv run pytest` works and collects 3 tests

**Remaining work for feature 002**:
1. Create `tests/conftest.py` with shared fixtures
2. Add markdown sample fixtures for conversion testing
3. Optionally add pytest-cov for coverage reporting

## Design Decisions

### Fixture Strategy

**Decision**: Use pytest's built-in `tmp_path` fixture rather than custom implementation.

**Rationale**: pytest provides `tmp_path` out of the box, which handles:
- Automatic cleanup after tests
- Isolated paths per test
- Cross-platform compatibility

**Markdown Fixtures**: Provide dictionaries mapping element types to sample strings, allowing tests to access specific markdown patterns (headings, bold, links, lists, tables).

### Coverage

**Decision**: Add pytest-cov to dev dependencies but don't enforce coverage thresholds.

**Rationale**: Coverage is useful for visibility but premature to enforce. The constitution requires comprehensive tests for conversion logic, not arbitrary percentage targets.
