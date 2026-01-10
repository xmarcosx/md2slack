# Tasks: Slack Post Command

**Input**: Design documents from `/specs/005-slack-post/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included as requested in Quality Standards (plan.md specifies "URL parsing and error handling will have unit tests").

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/md2slack/`, `tests/` at repository root
- Per plan.md: New `slack.py` module, updates to existing `cli.py`

---

## Phase 1: Setup

**Purpose**: Add slack_sdk dependency and prepare project for Slack integration

- [X] T001 Add `slack_sdk>=3.0` to dependencies in pyproject.toml
- [X] T002 Run `uv sync` to install new dependency

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Slack functionality that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 [P] Create src/md2slack/slack.py with module docstring and imports
- [X] T004 [P] Create tests/test_slack.py with pytest imports and fixtures
- [X] T005 Implement `parse_thread_url()` function in src/md2slack/slack.py per research.md regex pattern
- [X] T006 [P] Add unit tests for `parse_thread_url()` in tests/test_slack.py covering valid URLs, invalid URLs, and edge cases
- [X] T007 Implement `SlackClient` class with `__init__(token)` in src/md2slack/slack.py
- [X] T008 Implement `SlackClient.post_message(channel_id, thread_ts, text)` method in src/md2slack/slack.py
- [X] T009 [P] Add error mapping dictionary for Slack API errors in src/md2slack/slack.py per research.md error codes
- [X] T010 Implement `format_slack_error()` function to convert API errors to user-friendly messages in src/md2slack/slack.py
- [X] T011 [P] Add unit tests for error mapping in tests/test_slack.py with mocked SlackApiError responses
- [X] T012 Run `uv run pytest tests/test_slack.py` to verify all foundational tests pass
- [X] T013 Run `uv run ruff check src/md2slack/slack.py` to verify code style

**Checkpoint**: Foundation ready - Slack module with URL parsing, API client, and error handling complete

---

## Phase 3: User Story 1 - Post Markdown to Thread (Priority: P1) 🎯 MVP

**Goal**: User can post converted markdown to a Slack thread with a single command

**Independent Test**: Run `md2slack post --thread <url> --file <path>` with valid inputs and verify message appears in Slack thread

### Tests for User Story 1

- [X] T014 [P] [US1] Add CLI integration test for `post` command happy path in tests/test_cli.py with mocked Slack API
- [X] T015 [P] [US1] Add CLI test for stdin input in tests/test_cli.py

### Implementation for User Story 1

- [X] T016 [US1] Implement `post` command in src/md2slack/cli.py with `--thread` and file arguments
- [X] T017 [US1] Add `get_token()` helper to read SLACK_BOT_TOKEN from environment in src/md2slack/slack.py
- [X] T018 [US1] Wire up post command: parse URL → read file → convert → post in src/md2slack/cli.py
- [X] T019 [US1] Add success message with permalink output in src/md2slack/cli.py
- [X] T020 [US1] Add stdin support (read from stdin when no file provided) in src/md2slack/cli.py
- [X] T021 [US1] Implement content length validation and truncation (40k limit) in src/md2slack/slack.py
- [X] T022 [P] [US1] Add unit test for truncation logic in tests/test_slack.py
- [X] T023 [US1] Add error handling for missing token, invalid URL, API errors in src/md2slack/cli.py
- [X] T024 [P] [US1] Add CLI tests for error scenarios in tests/test_cli.py
- [X] T025 [US1] Run full test suite `uv run pytest` to verify User Story 1 is complete

**Checkpoint**: User Story 1 complete - `md2slack post --thread <url> --file <path>` works end-to-end

---

## Phase 4: User Story 2 - Preview Before Posting (Priority: P2)

**Goal**: User can preview what will be posted without actually posting

**Independent Test**: Run `md2slack post --thread <url> --file <path> --dry-run` and verify output shown but no Slack API call made

### Tests for User Story 2

- [X] T026 [P] [US2] Add CLI test for `--dry-run` flag in tests/test_cli.py verifying no API call and output to stdout

### Implementation for User Story 2

- [X] T027 [US2] Add `--dry-run` / `-n` option to post command in src/md2slack/cli.py
- [X] T028 [US2] Implement dry-run logic: skip API call, output preview to stdout with indicator in src/md2slack/cli.py
- [X] T029 [US2] Run `uv run pytest tests/test_cli.py -k dry_run` to verify dry-run tests pass

**Checkpoint**: User Story 2 complete - `--dry-run` shows preview without posting

---

## Phase 5: User Story 3 - Add Prefix Text (Priority: P3)

**Goal**: User can prepend custom text before converted content

**Independent Test**: Run `md2slack post --thread <url> --file <path> --prefix "Header"` and verify prefix appears before content

### Tests for User Story 3

- [X] T030 [P] [US3] Add CLI test for `--prefix` option in tests/test_cli.py verifying prefix is prepended

### Implementation for User Story 3

- [X] T031 [US3] Add `--prefix` / `-p` option to post command in src/md2slack/cli.py
- [X] T032 [US3] Implement prefix prepending logic (handle newlines in prefix) in src/md2slack/cli.py
- [X] T033 [US3] Run `uv run pytest tests/test_cli.py -k prefix` to verify prefix tests pass

**Checkpoint**: User Story 3 complete - `--prefix` prepends text before converted content

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation

- [X] T034 Run full test suite `uv run pytest` and verify all tests pass
- [X] T035 Run `uv run ruff check .` and fix any style issues
- [X] T036 [P] Add short flags documentation to `--help` output in src/md2slack/cli.py
- [X] T037 Validate quickstart.md examples work correctly (manual test)
- [X] T038 Update README.md with Slack setup instructions (OAuth scopes, token)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 (uses same infrastructure)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD approach)
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 2 (Foundational)**:
- T003, T004 can run in parallel (create files)
- T006, T009, T011 can run in parallel (independent tests)

**Phase 3 (US1)**:
- T014, T015 can run in parallel (independent tests)
- T022, T024 can run in parallel (independent tests)

**Phase 4-5 (US2, US3)**:
- T026 and T030 can run in parallel if stories run in parallel

---

## Parallel Example: Phase 2 Foundational

```bash
# Launch file creation in parallel:
Task: "Create src/md2slack/slack.py with module docstring and imports"
Task: "Create tests/test_slack.py with pytest imports and fixtures"

# After T005, launch tests in parallel:
Task: "Add unit tests for parse_thread_url() in tests/test_slack.py"
Task: "Add error mapping dictionary in src/md2slack/slack.py"
Task: "Add unit tests for error mapping in tests/test_slack.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (2 tasks)
2. Complete Phase 2: Foundational (11 tasks) - CRITICAL
3. Complete Phase 3: User Story 1 (12 tasks)
4. **STOP and VALIDATE**: Test `md2slack post --thread <url> --file <path>`
5. Deploy/demo if ready - core feature works!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP ready
3. Add User Story 2 → `--dry-run` support added
4. Add User Story 3 → `--prefix` support added
5. Polish → Documentation complete

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Slack API calls are mocked in tests - no real Slack workspace needed for development
