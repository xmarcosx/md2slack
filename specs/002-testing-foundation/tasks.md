# Tasks: Testing Foundation

**Input**: Design documents from `/specs/002-testing-foundation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md

**Tests**: No explicit test tasks included - this feature IS the testing infrastructure.

**Organization**: Tasks are grouped by user story to enable independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add pytest-cov dependency and create conftest.py structure

- [x] T001 Add pytest-cov>=4.0 to dev dependencies in pyproject.toml
- [x] T002 Create tests/conftest.py with standard pytest docstring and imports

---

## Phase 2: User Story 1 - Run Test Suite (Priority: P1)

**Goal**: Verify `uv run pytest` executes successfully with the new conftest.py

**Independent Test**: Run `uv run pytest` from repo root and verify exit code 0

### Implementation for User Story 1

- [x] T003 [US1] Verify pytest runs successfully after conftest.py creation via `uv run pytest`
- [x] T004 [US1] Verify pytest discovers existing tests in tests/test_cli.py

**Checkpoint**: `uv run pytest` should exit 0 and show test collection output

---

## Phase 3: User Story 2 - Write Conversion Tests (Priority: P2)

**Goal**: Provide markdown sample fixtures for conversion testing

**Independent Test**: Import `markdown_samples` fixture in a test and verify it returns a dict with markdown patterns

### Implementation for User Story 2

- [x] T005 [US2] Add `markdown_samples` fixture to tests/conftest.py returning dict with heading, bold, italic, link, list, code_inline, code_block, table samples
- [x] T006 [US2] Add docstring to `markdown_samples` fixture explaining available keys

**Checkpoint**: A test can use `markdown_samples["heading"]` to get `"# Hello World"`

---

## Phase 4: User Story 3 - Test File-Based Input (Priority: P3)

**Goal**: Provide fixture for creating temporary markdown files

**Independent Test**: Use `markdown_file` fixture in a test and verify it creates a readable file

### Implementation for User Story 3

- [x] T007 [US3] Add `markdown_file` fixture to tests/conftest.py that creates a temp markdown file using tmp_path
- [x] T008 [US3] Add docstring to `markdown_file` fixture explaining usage and automatic cleanup

**Checkpoint**: A test using `markdown_file` fixture gets a Path to a readable markdown file that is cleaned up after test

---

## Phase 5: Polish & Validation

**Purpose**: Verify all fixtures work together and document usage

- [x] T009 Run `uv run pytest -v` and verify all 3 existing tests still pass
- [x] T010 Run `uv run pytest --cov=md2slack` to verify coverage reporting works
- [x] T011 Verify fixtures are documented in quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup - verify pytest still works
- **User Story 2 (Phase 3)**: Can start after Setup, adds fixtures to conftest.py
- **User Story 3 (Phase 4)**: Can start after Setup, adds fixtures to conftest.py
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories - just verifies pytest works
- **User Story 2 (P2)**: No dependencies on other stories - adds markdown_samples fixture
- **User Story 3 (P3)**: No dependencies on other stories - adds markdown_file fixture

### Within Each User Story

- US1: Just verification tasks
- US2: Single fixture implementation in conftest.py
- US3: Single fixture implementation in conftest.py

### Parallel Opportunities

- US2 and US3 both add to the same file (conftest.py), so should be done sequentially
- T005 and T007 modify the same file - NOT parallelizable
- Setup (T001-T002) should complete before user stories

---

## Parallel Example: Setup

```bash
# T001 and T002 can run in sequence (T001 first for dependency install):
Task: "Add pytest-cov>=4.0 to dev dependencies in pyproject.toml"
Task: "Create tests/conftest.py with standard pytest docstring and imports"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: User Story 1 (T003-T004)
3. **STOP and VALIDATE**: Run `uv run pytest` and verify it works
4. This gives a working test infrastructure

### Incremental Delivery

1. Complete Setup → pytest-cov added, conftest.py created
2. Add User Story 1 → Verify pytest still works
3. Add User Story 2 → markdown_samples fixture available
4. Add User Story 3 → markdown_file fixture available
5. Each story adds value without breaking previous stories

---

## Notes

- This is a small feature - only 11 tasks total
- All work is in 2 files: pyproject.toml and tests/conftest.py
- No test tasks needed since this feature IS the test infrastructure
- Feature 001 already set up pytest basics - we're just adding fixtures
- Avoid: modifying tests/test_cli.py or other existing files unnecessarily
