# Tasks: Default Chunking with Content Preservation

**Status**: ✅ COMPLETE (2026-01-10)
**Input**: Design documents from `/specs/007-default-chunking/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Test tasks are included as this feature modifies existing behavior and the plan explicitly calls for content preservation tests (D4).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (No changes needed)

**Purpose**: This feature modifies existing code; no new project setup required.

**Status**: ✅ Project already initialized with Python 3.10+, Click, pytest

---

## Phase 2: Foundational (CLI Flag Removal)

**Purpose**: Core changes that MUST be complete before user story validation - remove the `--chunk` flag and eliminate the non-chunked code path.

**⚠️ CRITICAL**: These changes affect all user stories and must be done first.

- [X] T001 Remove `--chunk`/`-c` flag definition from post command in src/md2slack/cli.py (lines 80-85)
- [X] T002 Remove `chunk` parameter from `post()` function signature in src/md2slack/cli.py (line 98)
- [X] T003 Remove `truncate_content` from imports in src/md2slack/cli.py (line 18)
- [X] T004 Add chunk-size cap: `chunk_size = min(chunk_size, DEFAULT_CHUNK_SIZE)` after validation in src/md2slack/cli.py
- [X] T005 Remove `if chunk:` conditional branch and keep chunked path logic in src/md2slack/cli.py (lines 145-217)
- [X] T006 Remove `else:` branch (non-chunked path) in src/md2slack/cli.py (lines 218-251)
- [X] T007 Update `post()` docstring to remove `--chunk` example in src/md2slack/cli.py (line 113)
- [X] T008 Run `uv run ruff check .` to verify code style compliance

**Checkpoint**: CLI refactoring complete - `--chunk` flag removed, chunking is now always-on

---

## Phase 3: User Story 1 - Post Long Document Without Flags (Priority: P1) 🎯 MVP

**Goal**: Users can post documents exceeding Slack's limit without any flags; content is automatically chunked.

**Independent Test**: Post a markdown file exceeding 40,000 characters and verify all content appears across multiple messages in correct order.

### Tests for User Story 1

- [X] T009 [P] [US1] Add content preservation test: first chunk contains document beginning in tests/test_chunker.py
- [X] T010 [P] [US1] Add content preservation test: all words preserved across chunks in tests/test_chunker.py
- [X] T011 [P] [US1] Add CLI test: long content posts without --chunk flag in tests/test_cli.py

### Implementation for User Story 1

- [X] T012 [US1] Verify chunker produces multiple chunks for long content (already works, validate)
- [X] T013 [US1] Verify chunks have correct indicators (1/N, 2/N format) (already works, validate)
- [X] T014 [US1] Run tests to confirm FR-001, FR-003, FR-004, FR-005 satisfied

**Checkpoint**: Long documents post automatically with chunking; first chunk contains beginning of content

---

## Phase 4: User Story 2 - Post Short Document Seamlessly (Priority: P1)

**Goal**: Short documents post as single messages without chunk indicators.

**Independent Test**: Post a markdown file under 3,000 characters and verify it appears as a single message without indicators.

### Tests for User Story 2

- [X] T015 [P] [US2] Add CLI test: short content posts as single message without indicator in tests/test_cli.py

### Implementation for User Story 2

- [X] T016 [US2] Verify chunker returns single chunk for short content (already works, validate)
- [X] T017 [US2] Verify `with_indicator` returns plain content for single chunk (already works, validate)
- [X] T018 [US2] Run tests to confirm FR-002, FR-006 satisfied

**Checkpoint**: Short documents post as single messages without any indicators

---

## Phase 5: User Story 3 - Customize Chunk Size (Priority: P2)

**Goal**: Power users can specify `--chunk-size` to control split threshold.

**Independent Test**: Post a document with `--chunk-size 5000` and verify it splits at the specified threshold.

### Tests for User Story 3

- [X] T019 [P] [US3] Add test: --chunk-size still works without --chunk flag in tests/test_cli.py
- [X] T020 [P] [US3] Add test: --chunk-size capped at DEFAULT_CHUNK_SIZE in tests/test_cli.py

### Implementation for User Story 3

- [X] T021 [US3] Update existing test_chunk_size_validation to not use --chunk flag in tests/test_cli.py
- [X] T022 [US3] Run tests to confirm FR-008, FR-010 satisfied

**Checkpoint**: --chunk-size works independently and is capped at Slack's limit

---

## Phase 6: User Story 4 - Simplified CLI (Priority: P2)

**Goal**: CLI help shows one fewer flag; `--chunk` is rejected as unknown option.

**Independent Test**: Run `md2slack post --help` and verify `--chunk`/`-c` is not listed.

### Tests for User Story 4

- [X] T023 [P] [US4] Rename test_chunk_flag_in_help → test_chunk_flag_not_in_help in tests/test_cli.py
- [X] T024 [P] [US4] Add test: --chunk flag produces error in tests/test_cli.py

### Implementation for User Story 4

- [X] T025 [US4] Verify --chunk-size still appears in help output (no change needed)
- [X] T026 [US4] Run tests to confirm FR-007 satisfied

**Checkpoint**: CLI is simpler with one fewer flag

---

## Phase 7: Test Migration (Existing Tests)

**Purpose**: Update all existing tests that use `--chunk` flag to work with new default behavior.

- [X] T027 Remove `--chunk` flag from test_chunk_dry_run_short_content in tests/test_cli.py
- [X] T028 Remove `--chunk` flag from test_chunk_dry_run_long_content in tests/test_cli.py
- [X] T029 Remove `--chunk` flag from test_chunk_posts_multiple_messages in tests/test_cli.py
- [X] T030 Remove `--chunk` flag from test_chunk_progress_output in tests/test_cli.py
- [X] T031 Remove `--chunk` flag from test_chunk_completion_summary in tests/test_cli.py
- [X] T032 Remove `--chunk` flag from test_chunk_error_mid_posting in tests/test_cli.py
- [X] T033 Remove `--chunk` flag from test_chunk_single_message_no_indicator in tests/test_cli.py

**Checkpoint**: All existing tests pass with new default-chunking behavior

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [X] T034 Run full test suite: `uv run pytest` and verify all tests pass
- [X] T035 Run linting: `uv run ruff check .` and fix any issues
- [X] T036 [P] Validate quickstart.md examples work correctly
- [X] T037 [P] Update bug 001.md to mark as resolved (content preservation verified)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: N/A - already complete
- **Phase 2 (Foundational)**: No dependencies - start here - BLOCKS all user stories
- **Phase 3-6 (User Stories)**: All depend on Phase 2 completion
  - US1 and US2 are both P1 priority but can proceed in parallel
  - US3 and US4 are P2 priority and can proceed in parallel after P1 stories
- **Phase 7 (Test Migration)**: Depends on Phase 2 (need CLI changes before updating tests)
- **Phase 8 (Polish)**: Depends on all previous phases

### User Story Dependencies

| Story | Priority | Dependencies          | Can Parallel With |
| :---- | :------- | :-------------------- | :---------------- |
| US1   | P1       | Phase 2 (Foundational)| US2               |
| US2   | P1       | Phase 2 (Foundational)| US1               |
| US3   | P2       | Phase 2 (Foundational)| US4               |
| US4   | P2       | Phase 2 (Foundational)| US3               |

### Within Each User Story

- Tests FIRST (write and verify they exercise the right behavior)
- Implementation/validation second
- Confirm functional requirements satisfied

### Parallel Opportunities

**Phase 2**: T001-T007 modify the same file (cli.py) - execute sequentially
**Phase 3 (US1)**: T009, T010, T011 can run in parallel (different files)
**Phase 4 (US2)**: T015 can run parallel with US1 tests
**Phase 5 (US3)**: T019, T020 can run in parallel
**Phase 6 (US4)**: T023, T024 can run in parallel
**Phase 7**: All test migration tasks (T027-T033) modify same file - execute sequentially
**Phase 8**: T036, T037 can run in parallel

---

## Parallel Example: User Story 1 & 2 Tests

```bash
# Launch all P1 user story tests together:
Task: "Add content preservation test: first chunk contains document beginning in tests/test_chunker.py" [T009]
Task: "Add content preservation test: all words preserved across chunks in tests/test_chunker.py" [T010]
Task: "Add CLI test: long content posts without --chunk flag in tests/test_cli.py" [T011]
Task: "Add CLI test: short content posts as single message without indicator in tests/test_cli.py" [T015]
```

---

## Implementation Strategy

### MVP First (Phase 2 + User Story 1)

1. Complete Phase 2: Foundational (CLI refactoring) - T001-T008
2. Complete Phase 3: User Story 1 - T009-T014
3. **STOP and VALIDATE**: Run `uv run pytest` - long documents should chunk automatically
4. This is the MVP - core value delivered

### Incremental Delivery

1. Phase 2 → CLI refactoring complete
2. Add US1 (long docs) → Test → Validate (**MVP!**)
3. Add US2 (short docs) → Test → Validate
4. Add US3 (custom size) → Test → Validate
5. Add US4 (CLI cleanup) → Test → Validate
6. Phase 7 → Migrate existing tests
7. Phase 8 → Final polish

### Single Developer Strategy (Recommended)

Execute in order: Phase 2 → Phase 3 → Phase 4 → Phase 7 → Phase 5 → Phase 6 → Phase 8

This prioritizes:
1. Core functionality (chunking by default)
2. Both P1 stories (most common use cases)
3. Test migration (ensure CI passes)
4. P2 stories (power user features)
5. Final validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Many tasks are "validate existing behavior" since chunker already works
- Primary code changes are in cli.py (flag removal, path simplification)
- Test changes are in test_cli.py (remove flag usage, add preservation tests)
- Avoid modifying chunker.py unless bugs are found
