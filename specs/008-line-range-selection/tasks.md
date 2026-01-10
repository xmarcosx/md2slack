# Tasks: Line Range Selection

**Input**: Design documents from `/specs/008-line-range-selection/`
**Prerequisites**: plan.md, spec.md, research.md, contracts/cli-interface.md

**Tests**: Tests are included (existing test infrastructure in pytest).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: No new project setup needed - adding to existing CLI

This phase is empty because we're extending an existing CLI. All infrastructure (pytest, Click, module structure) already exists.

**Checkpoint**: Setup complete - proceed to Foundational phase

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core line range parsing and extraction logic that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T001 Implement `parse_line_range` callback function in src/md2slack/cli.py that parses "START-END" format and returns tuple
- [X] T002 Implement `extract_lines` helper function in src/md2slack/cli.py that extracts line range from content string
- [X] T003 Implement `validate_line_range` helper function in src/md2slack/cli.py that checks range against total line count

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Post Section from Large Document (Priority: P1) 🎯 MVP

**Goal**: Enable `md2slack post file.md --thread URL --lines 45-78` to post only specified lines

**Independent Test**: Run `md2slack post file.md --thread URL --lines 45-78 --dry-run` and verify only lines 45-78 appear in output

### Tests for User Story 1

- [X] T004 [P] [US1] Add test for `--lines` option on post command with valid range in tests/test_cli.py
- [X] T005 [P] [US1] Add test for `--lines` option on post command with stdin input in tests/test_cli.py

### Implementation for User Story 1

- [X] T006 [US1] Add `--lines/-l` option decorator to `post` command in src/md2slack/cli.py
- [X] T007 [US1] Integrate line extraction into `post` command flow after reading file content in src/md2slack/cli.py
- [X] T008 [US1] Add line extraction for stdin input path in `post` command in src/md2slack/cli.py

**Checkpoint**: At this point, `md2slack post --lines` should be fully functional

---

## Phase 4: User Story 2 - Preview Section Before Posting (Priority: P2)

**Goal**: Enable `md2slack convert file.md --lines 10-25` to preview only specified lines

**Independent Test**: Run `md2slack convert file.md --lines 10-25` and verify only lines 10-25 appear in stdout

### Tests for User Story 2

- [X] T009 [P] [US2] Add test for `--lines` option on convert command with valid range in tests/test_cli.py
- [X] T010 [P] [US2] Add test for `--lines` option on convert command with stdin input in tests/test_cli.py
- [X] T011 [P] [US2] Add test that `--lines` with `--text` produces error in tests/test_cli.py

### Implementation for User Story 2

- [X] T012 [US2] Add `--lines/-l` option decorator to `convert` command in src/md2slack/cli.py
- [X] T013 [US2] Integrate line extraction into `convert` command flow after reading file content in src/md2slack/cli.py
- [X] T014 [US2] Add validation that `--lines` cannot be used with `--text` option in src/md2slack/cli.py

**Checkpoint**: At this point, `md2slack convert --lines` should be fully functional

---

## Phase 5: User Story 3 - Handle Invalid Range Gracefully (Priority: P3)

**Goal**: Provide clear, actionable error messages for all invalid range scenarios

**Independent Test**: Run with invalid ranges and verify error messages include valid range

### Tests for User Story 3

- [X] T015 [P] [US3] Add test for invalid format error (e.g., "abc") in tests/test_cli.py
- [X] T016 [P] [US3] Add test for start > end error (e.g., "50-30") in tests/test_cli.py
- [X] T017 [P] [US3] Add test for out-of-bounds error with correct message format in tests/test_cli.py
- [X] T018 [P] [US3] Add test for zero/negative line numbers error in tests/test_cli.py

### Implementation for User Story 3

- [X] T019 [US3] Add invalid format error handling to `parse_line_range` in src/md2slack/cli.py
- [X] T020 [US3] Add start > end validation error to `parse_line_range` in src/md2slack/cli.py
- [X] T021 [US3] Add zero/negative validation error to `parse_line_range` in src/md2slack/cli.py
- [X] T022 [US3] Add out-of-bounds error with file line count to `validate_line_range` in src/md2slack/cli.py

**Checkpoint**: All error scenarios should produce clear, actionable messages

---

## Phase 6: Edge Cases & Polish

**Purpose**: Handle edge cases documented in spec.md

### Tests for Edge Cases

- [X] T023 [P] Add test for single-line range (e.g., `--lines 5-5`) in tests/test_cli.py
- [X] T024 [P] Add test for range starting at line 1 in tests/test_cli.py
- [X] T025 [P] Add test for range ending at last line in tests/test_cli.py
- [X] T026 [P] Add test for file with trailing empty lines in tests/test_cli.py

### Polish

- [X] T027 Run `uv run pytest` to verify all tests pass
- [X] T028 Run `uv run ruff check .` to verify code style
- [X] T029 Manual test: Run quickstart.md examples to validate user experience

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Empty - existing project
- **Foundational (Phase 2)**: No dependencies - can start immediately
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on T001-T003 (Foundational)
- **User Story 2 (P2)**: Depends on T001-T003 (Foundational) - Can run in parallel with US1
- **User Story 3 (P3)**: Depends on T001-T003 (Foundational) - Can run in parallel with US1/US2

### Within Each User Story

- Tests written first (if included)
- Implementation follows tests
- Story complete before checkpoint

### Parallel Opportunities

**Foundational Phase**:
- T001, T002, T003 are sequential (T002 depends on T001's format, T003 depends on T002)

**User Story 1**:
- T004, T005 can run in parallel (different test cases)

**User Story 2**:
- T009, T010, T011 can run in parallel (different test cases)

**User Story 3**:
- T015, T016, T017, T018 can run in parallel (different error scenarios)

**Edge Cases**:
- T023, T024, T025, T026 can run in parallel (different edge cases)

---

## Parallel Example: User Story 3 Tests

```bash
# Launch all error scenario tests together:
Task: "Add test for invalid format error (e.g., 'abc') in tests/test_cli.py"
Task: "Add test for start > end error (e.g., '50-30') in tests/test_cli.py"
Task: "Add test for out-of-bounds error with correct message format in tests/test_cli.py"
Task: "Add test for zero/negative line numbers error in tests/test_cli.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (T001-T003)
2. Complete Phase 3: User Story 1 (T004-T008)
3. **STOP and VALIDATE**: Test with `md2slack post file.md --thread URL --lines 10-20 --dry-run`
4. MVP complete - `post` command supports `--lines`

### Incremental Delivery

1. Foundational → Foundation ready
2. Add User Story 1 → `post --lines` works → MVP!
3. Add User Story 2 → `convert --lines` works
4. Add User Story 3 → Error messages polished
5. Add Edge Cases → All scenarios covered

### Total Task Count

| Phase         | Tasks |
| :------------ | :---- |
| Foundational  | 3     |
| User Story 1  | 5     |
| User Story 2  | 6     |
| User Story 3  | 8     |
| Edge Cases    | 7     |
| **Total**     | **29**|

---

## Notes

- [P] tasks = different test cases or implementations that don't conflict
- All code changes are in src/md2slack/cli.py (single file)
- All tests are in tests/test_cli.py (single file)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
