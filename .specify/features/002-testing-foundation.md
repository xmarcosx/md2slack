### 002 - Testing Foundation

**Problem**: No test infrastructure exists. Cannot write or run tests for upcoming features.

**Desired State**: `uv run pytest` runs successfully (even with zero tests). Test fixtures ready for conversion testing.

**Why This Matters**:
1. Enables TDD workflow for Core Converter (003) and beyond
2. Catches regressions as features are added

**Example**:
- Current: No tests/ directory, pytest not configured
- Desired: `uv run pytest` exits 0, basic fixtures available

**Notes**:
- Structure: `tests/` at repo root, organized by module
- Basic fixtures: temp file creation, sample markdown strings
- Keep fixtures minimal—only add what's needed for next feature
- Configure pytest in pyproject.toml (not pytest.ini)
