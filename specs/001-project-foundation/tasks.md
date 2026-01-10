# Tasks: Project Foundation

**Input**: Design documents from `/specs/001-project-foundation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: A single smoke test is included as specified in the plan (minimal testing for infrastructure feature).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths follow src-layout: `src/md2slack/` for package code

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and package configuration

- [x] T001 Create src-layout directory structure: `src/md2slack/`
- [x] T002 Create package init file with version in `src/md2slack/__init__.py`
- [x] T003 Create `pyproject.toml` with package metadata, Click dependency, entry point configuration
- [x] T004 [P] Create tests directory structure: `tests/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core CLI infrastructure that MUST be complete before subcommands can be added

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create CLI module with Click group in `src/md2slack/cli.py`
- [x] T006 Configure Click group to show help when invoked without subcommand in `src/md2slack/cli.py`

**Checkpoint**: Foundation ready - `md2slack --help` should work after installation

---

## Phase 3: User Story 1 - Install and Verify CLI (Priority: P1) 🎯 MVP

**Goal**: Developer can install package and run `md2slack --help` successfully

**Independent Test**: Run `uv pip install -e .` followed by `md2slack --help` and verify output appears

### Implementation for User Story 1

- [x] T007 [US1] Install package in dev mode and verify CLI entry point works
- [x] T008 [US1] Verify `md2slack` without arguments shows help message
- [x] T009 [US1] Verify `md2slack --help` displays available commands (convert, post)

**Checkpoint**: User Story 1 complete - package installs and help works

---

## Phase 4: User Story 2 - View Convert Subcommand (Priority: P2)

**Goal**: Developer can run `md2slack convert` and see placeholder functionality

**Independent Test**: Run `md2slack convert --help` and `md2slack convert` to verify output

### Implementation for User Story 2

- [x] T010 [US2] Add `convert` subcommand to CLI group in `src/md2slack/cli.py`
- [x] T011 [US2] Implement placeholder message "Convert command is not implemented yet." in `src/md2slack/cli.py`
- [x] T012 [US2] Add help text describing future convert functionality in `src/md2slack/cli.py`

**Checkpoint**: User Story 2 complete - convert subcommand shows placeholder

---

## Phase 5: User Story 3 - View Post Subcommand (Priority: P2)

**Goal**: Developer can run `md2slack post` and see placeholder functionality

**Independent Test**: Run `md2slack post --help` and `md2slack post` to verify output

### Implementation for User Story 3

- [x] T013 [P] [US3] Add `post` subcommand to CLI group in `src/md2slack/cli.py`
- [x] T014 [US3] Implement placeholder message "Post command is not implemented yet." in `src/md2slack/cli.py`
- [x] T015 [US3] Add help text describing future post functionality in `src/md2slack/cli.py`

**Checkpoint**: User Story 3 complete - post subcommand shows placeholder

---

## Phase 6: User Story 4 - Run Development Tools (Priority: P3)

**Goal**: Developer can run linting and tests using uv

**Independent Test**: Run `uv run ruff check .` and `uv run pytest` to verify they execute

### Implementation for User Story 4

- [x] T016 [US4] Add ruff and pytest as dev dependencies in `pyproject.toml`
- [x] T017 [P] [US4] Create smoke test file `tests/test_cli.py` with basic CLI invocation test
- [x] T018 [US4] Run `uv sync --dev` to install dev dependencies
- [x] T019 [US4] Verify `uv run ruff check .` executes without configuration errors
- [x] T020 [US4] Verify `uv run pytest` runs and passes smoke test

**Checkpoint**: User Story 4 complete - dev tools work

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [x] T021 Run all CLI commands and verify output matches contracts/cli-interface.md
- [x] T022 Run quickstart.md validation steps end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 must complete before US2/US3 (verifies installation works)
  - US2 and US3 can proceed in parallel (different subcommands)
  - US4 should be last (tests require all code to exist)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 completion (need working CLI first)
- **User Story 3 (P2)**: Depends on US1 completion, can run parallel with US2
- **User Story 4 (P3)**: Depends on US1-US3 (tests the complete CLI)

### Within Each User Story

- Core CLI structure before subcommands
- Subcommand definition before placeholder implementation
- Implementation before verification

### Parallel Opportunities

- T001 and T004 can run in parallel (different directories)
- T013 can run in parallel with T010-T012 (different subcommands in same file, but logically separate)
- T017 can run in parallel with T016 (different files)

---

## Parallel Example: Setup Phase

```bash
# Launch directory creation in parallel:
Task: "Create src-layout directory structure: src/md2slack/"
Task: "Create tests directory structure: tests/"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (directory structure, pyproject.toml)
2. Complete Phase 2: Foundational (CLI module with Click group)
3. Complete Phase 3: User Story 1 (verify installation and help)
4. **STOP and VALIDATE**: Run `md2slack --help` independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test `md2slack --help` → MVP complete!
3. Add User Story 2 → Test `md2slack convert` → Convert placeholder works
4. Add User Story 3 → Test `md2slack post` → Post placeholder works
5. Add User Story 4 → Run ruff + pytest → Dev workflow complete

### Single Developer Strategy

Since this is a small infrastructure feature:
1. Work through phases sequentially
2. Verify each checkpoint before proceeding
3. Total: ~22 small tasks, should complete quickly

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each phase completion
- Stop at any checkpoint to validate story independently
- This is a foundation feature - minimal code, maximum structure
