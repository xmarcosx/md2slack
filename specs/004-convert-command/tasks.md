# Tasks: Convert Command

**Input**: Design documents from `/specs/004-convert-command/`
**Prerequisites**: plan.md, spec.md, research.md, contracts/cli-interface.md

**Implementation Note**: Research revealed that the convert command is **already implemented** in `src/md2slack/cli.py`. The remaining work is validation, test completion, and documentation.

**Tests**: Included as this feature requires validation of existing implementation.

**Organization**: Tasks are grouped by user story to enable independent validation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Verification)

**Purpose**: Verify existing implementation and test infrastructure

- [X] T001 Verify convert command exists and responds to `--help` via `uv run md2slack convert --help`
- [X] T002 [P] Verify pytest and test fixtures are working via `uv run pytest tests/test_cli.py -v`
- [X] T003 [P] Review existing error messages in `src/md2slack/cli.py` for actionability per Constitution Principle V

---

## Phase 2: Foundational (No changes needed)

**Purpose**: Core infrastructure is already complete from feature 003

**⚠️ NOTE**: No foundational tasks required - the convert command and converter module already exist.

**Checkpoint**: Foundation verified - user story validation can proceed

---

## Phase 3: User Story 1 - Preview Markdown Conversion (Priority: P1)

**Goal**: Validate that users can preview markdown conversion output

**Independent Test**: Run `uv run md2slack convert notes.md` with a sample markdown file and verify output matches expected mrkdwn format

### Tests for User Story 1

- [X] T004 [P] [US1] Add test for file input with various markdown elements in `tests/test_cli.py`
- [X] T005 [P] [US1] Add test for empty file handling (should output empty string, exit 0) in `tests/test_cli.py`
- [X] T006 [P] [US1] Add test for whitespace-only file in `tests/test_cli.py`

### Implementation for User Story 1

- [X] T007 [US1] Verify existing implementation handles all markdown elements (headings, bold, links, tables) via manual test with sample file
- [X] T008 [US1] Run full test suite to confirm US1 acceptance scenarios pass via `uv run pytest tests/test_cli.py -v`

**Checkpoint**: User Story 1 validated - basic conversion works as specified

---

## Phase 4: User Story 2 - Handle Missing File Gracefully (Priority: P2)

**Goal**: Validate that missing file errors are clear and actionable

**Independent Test**: Run `uv run md2slack convert nonexistent.md` and verify error message and exit code

### Tests for User Story 2

- [X] T009 [P] [US2] Add test for file not found error message and exit code in `tests/test_cli.py`
- [X] T010 [P] [US2] Add test for directory-instead-of-file error in `tests/test_cli.py`

### Implementation for User Story 2

- [X] T011 [US2] Verify Click's `exists=True` error message meets "actionable" standard per FR-008
- [X] T012 [US2] If error message needs improvement, update error handling in `src/md2slack/cli.py`

**Checkpoint**: User Story 2 validated - missing file errors are handled gracefully

---

## Phase 5: User Story 3 - Handle Permission Errors (Priority: P3)

**Goal**: Validate that permission errors are clear and actionable

**Independent Test**: Create a file with no read permission, run convert command, verify error message

### Tests for User Story 3

- [X] T013 [US3] Add test for permission denied error with unreadable file in `tests/test_cli.py`

### Implementation for User Story 3

- [X] T014 [US3] Review if Click handles PermissionError or if custom handling is needed in `src/md2slack/cli.py`
- [X] T015 [US3] If permission error handling is missing, add try/except in convert command in `src/md2slack/cli.py`

**Checkpoint**: User Story 3 validated - permission errors are handled gracefully

---

## Phase 6: Polish & Documentation

**Purpose**: Final validation and documentation updates

- [X] T016 [P] Update spec.md to reflect actual CLI interface (positional FILE vs --file option)
- [X] T017 [P] Run `uv run ruff check .` to verify code style compliance
- [X] T018 Run complete test suite via `uv run pytest --cov=md2slack` and verify all tests pass
- [X] T019 Validate quickstart.md examples work correctly via manual testing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - verification can start immediately
- **Foundational (Phase 2)**: N/A - already complete from feature 003
- **User Stories (Phase 3-5)**: Can proceed after Setup verification
  - Stories can proceed in parallel (they test different scenarios)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all user story validations being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies - tests core functionality
- **User Story 2 (P2)**: No dependencies on US1 - tests missing file scenario
- **User Story 3 (P3)**: No dependencies on US1/US2 - tests permission scenario

### Parallel Opportunities

- T002, T003 can run in parallel (different concerns)
- T004, T005, T006 can run in parallel (different test scenarios, same file)
- T009, T010 can run in parallel (different test scenarios)
- T016, T017 can run in parallel (different files)

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all US1 tests together:
Task: "Add test for file input with various markdown elements in tests/test_cli.py"
Task: "Add test for empty file handling in tests/test_cli.py"
Task: "Add test for whitespace-only file in tests/test_cli.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup verification
2. Skip Phase 2 (already done)
3. Complete Phase 3: User Story 1 validation
4. **STOP and VALIDATE**: All basic conversion tests pass
5. Feature is functionally complete for MVP

### Incremental Delivery

1. Verify Setup → Foundation confirmed
2. Validate User Story 1 → Core conversion works
3. Validate User Story 2 → Missing file errors handled
4. Validate User Story 3 → Permission errors handled
5. Polish → Documentation updated, all tests pass

### Expected Outcome

Since the convert command is already implemented, most tasks are **validation and testing** rather than new code. The primary deliverables are:
- Expanded test coverage in `tests/test_cli.py`
- Verification that error messages meet Constitution Principle V
- Updated spec.md reflecting actual implementation
- Possible minor error handling improvements in `src/md2slack/cli.py`

---

## Notes

- [P] tasks = can run in parallel
- [Story] label maps task to specific user story for traceability
- Most "implementation" is actually validation of existing code
- Focus is on test coverage and error message quality
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
