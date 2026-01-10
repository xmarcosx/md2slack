# Research: Testing Foundation

**Feature**: 002-testing-foundation
**Date**: 2026-01-09

## Summary

Minimal research needed - pytest infrastructure already exists from feature 001. This document captures decisions for the remaining fixture work.

## Findings

### 1. Pytest Fixture Best Practices

**Decision**: Use `conftest.py` at test root for shared fixtures.

**Rationale**: This is pytest's standard pattern. Fixtures in conftest.py are automatically available to all test modules without imports.

**Alternatives considered**:
- Fixtures in each test file: Rejected - leads to duplication
- Fixtures in a separate module with explicit imports: Rejected - unnecessary complexity

### 2. Temporary File Handling

**Decision**: Use pytest's built-in `tmp_path` fixture.

**Rationale**:
- Built into pytest, no additional dependencies
- Provides `pathlib.Path` object (modern Python file handling)
- Automatic cleanup after test
- Unique directory per test invocation

**Alternatives considered**:
- Custom `tempfile.TemporaryDirectory`: Rejected - reinvents the wheel
- Shared temp directory with manual cleanup: Rejected - test isolation issues

### 3. Markdown Sample Data Structure

**Decision**: Provide fixtures as dictionaries with named samples.

**Rationale**: Tests can request specific markdown patterns by name (e.g., `markdown_samples["heading"]`), making tests self-documenting.

**Structure**:
```python
@pytest.fixture
def markdown_samples():
    return {
        "heading": "# Hello World",
        "bold": "This is **bold** text",
        "italic": "This is *italic* text",
        "link": "[Click here](https://example.com)",
        "list": "- Item 1\n- Item 2\n- Item 3",
        "code_inline": "Use `code` here",
        "code_block": "```python\nprint('hello')\n```",
        "table": "| A | B |\n|---|---|\n| 1 | 2 |",
    }
```

### 4. Coverage Tooling

**Decision**: Add pytest-cov to dev dependencies.

**Rationale**: Coverage visibility is valuable even without enforcement. Developers can run `uv run pytest --cov=md2slack` to see coverage.

**Alternatives considered**:
- No coverage tooling: Rejected - harder to assess test completeness later
- Enforce minimum coverage: Rejected - premature for foundation feature

## No Unknowns Remaining

All technical decisions resolved. Ready for implementation.
