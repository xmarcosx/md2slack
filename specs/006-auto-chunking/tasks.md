# Tasks: Auto-Chunking for Long Content

**Input**: Design documents from `/specs/006-auto-chunking/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Included per constitution Quality Standards requirement for comprehensive test coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/md2slack/`, `tests/` at repository root (per plan.md)

---

## Phase 1: Setup

**Purpose**: Create new module structure for chunking functionality

- [X] T001 Create chunker module skeleton in src/md2slack/chunker.py with module docstring and imports
- [X] T002 [P] Create test file skeleton in tests/test_chunker.py with pytest imports and fixtures

---

## Phase 2: Foundational (Core Data Structures)

**Purpose**: Implement data structures that ALL user stories depend on

**⚠️ CRITICAL**: User story implementation requires these structures

- [X] T003 Implement Chunk dataclass in src/md2slack/chunker.py with fields: content, index, total, split_type
- [X] T004 Implement ChunkResult dataclass in src/md2slack/chunker.py with fields: chunks, warnings, original_length
- [X] T005 [P] Add Chunk.indicator property returning "(N/M)" format in src/md2slack/chunker.py
- [X] T006 [P] Add Chunk.with_indicator property returning content + indicator in src/md2slack/chunker.py
- [X] T007 Add tests for Chunk and ChunkResult dataclasses in tests/test_chunker.py

**Checkpoint**: Foundation ready - data structures tested and working

---

## Phase 3: User Story 1 - Post Long Document Successfully (Priority: P1) 🎯 MVP

**Goal**: Enable posting documents exceeding 40,000 characters by splitting into multiple messages

**Independent Test**: Create an 80,000 character markdown file, run `md2slack post --chunk --thread URL file.md`, verify all content appears in thread

### Tests for User Story 1

- [X] T008 [P] [US1] Add test for chunk_content with short content (no splitting needed) in tests/test_chunker.py
- [X] T009 [P] [US1] Add test for chunk_content with long content (requires splitting) in tests/test_chunker.py
- [X] T010 [P] [US1] Add test for continuation indicator format "(1/3)" in tests/test_chunker.py
- [X] T011 [P] [US1] Add test for no indicator when single chunk in tests/test_chunker.py

### Implementation for User Story 1

- [X] T012 [US1] Implement basic chunk_content(content, max_size) function in src/md2slack/chunker.py
- [X] T013 [US1] Add --chunk flag to post command in src/md2slack/cli.py
- [X] T014 [US1] Add --chunk-size flag with default 39000, min 1000 validation in src/md2slack/cli.py
- [X] T015 [US1] Implement chunked posting loop in post command in src/md2slack/cli.py
- [X] T016 [US1] Add continuation indicators to chunks before posting in src/md2slack/cli.py
- [X] T017 [P] [US1] Add CLI tests for --chunk flag in tests/test_cli.py
- [X] T018 [P] [US1] Add CLI tests for --chunk-size validation in tests/test_cli.py

**Checkpoint**: User Story 1 complete - can post long documents with basic splitting

---

## Phase 4: User Story 2 - Intelligent Split Points (Priority: P1)

**Goal**: Split at paragraph boundaries (preferred), sentence boundaries (fallback), hard splits (last resort)

**Independent Test**: Create document with clear paragraphs, verify splits only occur at `\n\n` boundaries

### Tests for User Story 2

- [X] T019 [P] [US2] Add test for split at paragraph boundary (\n\n) in tests/test_chunker.py
- [X] T020 [P] [US2] Add test for split at sentence boundary (. ) when paragraph too large in tests/test_chunker.py
- [X] T021 [P] [US2] Add test for hard split when no natural boundary found in tests/test_chunker.py
- [X] T022 [P] [US2] Add test for split_type tracking in Chunk objects in tests/test_chunker.py

### Implementation for User Story 2

- [X] T023 [US2] Implement find_paragraph_boundary helper in src/md2slack/chunker.py
- [X] T024 [US2] Implement find_sentence_boundary helper in src/md2slack/chunker.py
- [X] T025 [US2] Implement find_best_split_point with priority logic in src/md2slack/chunker.py
- [X] T026 [US2] Update chunk_content to use find_best_split_point in src/md2slack/chunker.py
- [X] T027 [US2] Track split_type for each chunk (paragraph/sentence/hard) in src/md2slack/chunker.py

**Checkpoint**: User Story 2 complete - splits occur at natural boundaries

---

## Phase 5: User Story 3 - Preserve Code Blocks and Tables (Priority: P1)

**Goal**: Never split inside fenced code blocks (```); warn if oversized block detected

**Independent Test**: Create document with code block spanning chunk boundary, verify block stays intact

### Tests for User Story 3

- [X] T028 [P] [US3] Add test for code block detection (```) in tests/test_chunker.py
- [X] T029 [P] [US3] Add test for no split inside code block in tests/test_chunker.py
- [X] T030 [P] [US3] Add test for warning on oversized code block in tests/test_chunker.py
- [X] T031 [P] [US3] Add test for table preservation (tables render as code blocks) in tests/test_chunker.py

### Implementation for User Story 3

- [X] T032 [US3] Implement is_inside_code_block state tracking in src/md2slack/chunker.py
- [X] T033 [US3] Implement find_code_block_boundaries helper in src/md2slack/chunker.py
- [X] T034 [US3] Update find_best_split_point to skip positions inside code blocks in src/md2slack/chunker.py
- [X] T035 [US3] Add oversized block detection and warning generation in src/md2slack/chunker.py
- [X] T036 [US3] Display warnings from ChunkResult in CLI output in src/md2slack/cli.py

**Checkpoint**: User Story 3 complete - code blocks and tables never split

---

## Phase 6: User Story 4 - Rate Limiting and Progress Feedback (Priority: P2)

**Goal**: Show progress during posting; add 1-second delay between posts; handle errors gracefully

**Independent Test**: Create document producing 5+ chunks, observe progress messages and timing

### Tests for User Story 4

- [X] T037 [P] [US4] Add test for progress output format "Posting chunk N/M..." in tests/test_cli.py
- [X] T038 [P] [US4] Add test for completion summary message in tests/test_cli.py
- [X] T039 [P] [US4] Add test for error handling mid-posting (partial success reporting) in tests/test_cli.py

### Implementation for User Story 4

- [X] T040 [US4] Add progress output to stderr during chunked posting in src/md2slack/cli.py
- [X] T041 [US4] Add 1-second delay between chunk posts using time.sleep in src/md2slack/cli.py
- [X] T042 [US4] Add completion summary showing total chunks posted in src/md2slack/cli.py
- [X] T043 [US4] Add error handling for partial posting failure in src/md2slack/cli.py
- [X] T044 [US4] Report which chunks succeeded on error in src/md2slack/cli.py

**Checkpoint**: User Story 4 complete - full UX with progress and error handling

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases, dry-run support, and final validation

- [X] T045 [P] Add test for empty chunk skipping in tests/test_chunker.py
- [X] T046 [P] Add test for content exactly at chunk limit (no indicator) in tests/test_chunker.py
- [X] T047 Implement empty chunk filtering in src/md2slack/chunker.py
- [X] T048 Update --dry-run to show chunk breaks and indicators in src/md2slack/cli.py
- [X] T049 Add dry-run test for chunked content preview in tests/test_cli.py
- [X] T050 Run full test suite with uv run pytest
- [X] T051 Run linting with uv run ruff check .
- [X] T052 Validate quickstart.md examples work correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - provides data structures for all stories
- **User Story 1 (Phase 3)**: Depends on Foundational - basic chunking and CLI
- **User Story 2 (Phase 4)**: Depends on US1 - refines split point selection
- **User Story 3 (Phase 5)**: Depends on US2 - adds block protection
- **User Story 4 (Phase 6)**: Depends on US1 (can parallelize with US2/US3) - adds UX
- **Polish (Phase 7)**: Depends on all user stories

### User Story Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (data structures)
    ↓
Phase 3: US1 - Basic Chunking ← MVP STOP POINT
    ↓
Phase 4: US2 - Smart Split Points
    ↓
Phase 5: US3 - Block Protection
    ↓
Phase 6: US4 - Progress/Rate Limiting (can start after US1)
    ↓
Phase 7: Polish
```

### Within Each User Story

- Tests written first (TDD approach)
- Helpers/utilities before main logic
- Core implementation before CLI integration
- Story complete before next priority

### Parallel Opportunities

**Phase 2 (Foundational)**:
- T005 and T006 can run in parallel (different properties on same class)

**Phase 3 (US1)**:
- T008, T009, T010, T011 tests can run in parallel
- T017, T018 CLI tests can run in parallel

**Phase 4 (US2)**:
- T019, T020, T021, T022 tests can run in parallel

**Phase 5 (US3)**:
- T028, T029, T030, T031 tests can run in parallel

**Phase 6 (US4)**:
- T037, T038, T039 tests can run in parallel

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task: "Add test for split at paragraph boundary in tests/test_chunker.py"
Task: "Add test for split at sentence boundary in tests/test_chunker.py"
Task: "Add test for hard split in tests/test_chunker.py"
Task: "Add test for split_type tracking in tests/test_chunker.py"

# Then implement sequentially:
Task: "Implement find_paragraph_boundary helper"
Task: "Implement find_sentence_boundary helper"
Task: "Implement find_best_split_point with priority logic"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T007)
3. Complete Phase 3: User Story 1 (T008-T018)
4. **STOP and VALIDATE**: Test with real long document
5. Deploy/demo if ready - basic chunking works!

### Incremental Delivery

1. Setup + Foundational → Data structures ready
2. Add User Story 1 → Basic chunking works (MVP!)
3. Add User Story 2 → Smarter splits
4. Add User Story 3 → Code blocks protected
5. Add User Story 4 → Full UX polish
6. Each story adds quality without breaking previous

### Single Developer Strategy

Follow phases sequentially:
1. Phase 1-2: ~30 min (setup)
2. Phase 3: ~1 hr (core chunking)
3. Phase 4: ~1 hr (split points)
4. Phase 5: ~1 hr (block protection)
5. Phase 6: ~45 min (UX)
6. Phase 7: ~30 min (polish)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Constitution requires test coverage - tests included
- Default chunk size is 39,000 (buffer for indicator)
- Tables render as code blocks (same protection logic)
- Progress to stderr, permalinks to stdout
