# Tasks: Core Converter

**Input**: Design documents from `/specs/003-core-converter/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Included per constitution quality standards requiring "comprehensive test coverage"

**Organization**: Tasks grouped by user story for independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Add mistune dependency and create module files

- [x] T001 Add mistune dependency to pyproject.toml (add `"mistune>=3.0,<4.0"` to dependencies list)
- [x] T002 [P] Create src/md2slack/converter.py with module docstring and imports
- [x] T003 [P] Create src/md2slack/tables.py with module docstring and imports
- [x] T004 [P] Create tests/test_converter.py with imports and test class structure
- [x] T005 [P] Create tests/test_tables.py with imports and test class structure
- [x] T006 Run `uv sync --dev` to install new dependencies

---

## Phase 2: Foundational

**Purpose**: Core infrastructure that all user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Implement BoxChars dataclass in src/md2slack/tables.py (frozen dataclass with all 11 box-drawing characters)
- [x] T008 Implement SlackMrkdwnRenderer base class in src/md2slack/converter.py (subclass HTMLRenderer, set escape=False)
- [x] T009 Implement convert() function shell in src/md2slack/converter.py (create mistune markdown with renderer and plugins)
- [x] T010 Add `__all__` exports to src/md2slack/converter.py (convert, SlackMrkdwnRenderer)
- [x] T011 Add `__all__` exports to src/md2slack/tables.py (BoxChars, LIGHT_BOX, and placeholder for future exports)

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - Convert Basic Markdown Text (Priority: P1)

**Goal**: Convert headings, bold, strikethrough, links, and lists to Slack mrkdwn format

**Independent Test**: Pass markdown strings with these elements and verify output matches Slack syntax

### Tests for User Story 1

- [x] T012 [P] [US1] Test heading conversion (all levels) in tests/test_converter.py
- [x] T013 [P] [US1] Test bold conversion (**text** -> *text*) in tests/test_converter.py
- [x] T014 [P] [US1] Test strikethrough conversion (~~text~~ -> ~text~) in tests/test_converter.py
- [x] T015 [P] [US1] Test link conversion ([text](url) -> <url|text>) in tests/test_converter.py
- [x] T016 [P] [US1] Test unordered list conversion (- item -> bullet item) in tests/test_converter.py
- [x] T017 [P] [US1] Test ordered list conversion (1. item -> numbered) in tests/test_converter.py

### Implementation for User Story 1

- [x] T018 [US1] Implement text() method in SlackMrkdwnRenderer (escape &, <, > characters)
- [x] T019 [US1] Implement heading() method in SlackMrkdwnRenderer (convert to bold format)
- [x] T020 [US1] Implement strong() method in SlackMrkdwnRenderer (**text** -> *text*)
- [x] T021 [US1] Implement emphasis() method in SlackMrkdwnRenderer (*text* -> _text_)
- [x] T022 [US1] Implement strikethrough() method in SlackMrkdwnRenderer (~~text~~ -> ~text~)
- [x] T023 [US1] Implement link() method in SlackMrkdwnRenderer ([text](url) -> <url|text>)
- [x] T024 [US1] Implement list() and list_item() methods in SlackMrkdwnRenderer (unordered with bullet)
- [x] T025 [US1] Extend list_item() for ordered lists (preserve numbering)
- [x] T026 [US1] Implement paragraph() method in SlackMrkdwnRenderer (add double newline)
- [x] T027 [US1] Implement codespan() method in SlackMrkdwnRenderer (passthrough backticks)
- [x] T028 [US1] Implement block_code() method in SlackMrkdwnRenderer (preserve code blocks)
- [x] T029 [US1] Implement block_quote() method in SlackMrkdwnRenderer (> prefix each line)
- [x] T030 [US1] Implement linebreak() and softbreak() methods in SlackMrkdwnRenderer
- [x] T031 [US1] Run tests/test_converter.py and verify all US1 tests pass

**Checkpoint**: Basic markdown conversion fully functional and tested

---

## Phase 4: User Story 2 - Convert Markdown Tables (Priority: P2)

**Goal**: Render markdown tables as monospace code blocks with Unicode box-drawing characters

**Independent Test**: Pass markdown tables and verify output contains aligned box-drawing code blocks

### Tests for User Story 2

- [x] T032 [P] [US2] Test TableCell dataclass (content, alignment, is_header, lines, width properties) in tests/test_tables.py
- [x] T033 [P] [US2] Test TableRow dataclass (cells, height property) in tests/test_tables.py
- [x] T034 [P] [US2] Test Table dataclass (headers, rows, column_count, column_widths) in tests/test_tables.py
- [x] T035 [P] [US2] Test render_table() with simple 2x2 table in tests/test_tables.py
- [x] T036 [P] [US2] Test render_table() with varying column widths in tests/test_tables.py
- [x] T037 [P] [US2] Test render_table() with empty cells in tests/test_tables.py
- [x] T038 [P] [US2] Test full table conversion via convert() in tests/test_converter.py

### Implementation for User Story 2

- [x] T039 [US2] Implement TableCell dataclass in src/md2slack/tables.py (content, alignment, is_header, lines, width)
- [x] T040 [US2] Implement TableRow dataclass in src/md2slack/tables.py (cells, height property)
- [x] T041 [US2] Implement Table dataclass in src/md2slack/tables.py (headers, rows, column_count, column_widths)
- [x] T042 [US2] Implement render_row_line() helper in src/md2slack/tables.py (render single line of cells with vertical bars)
- [x] T043 [US2] Implement render_separator() helper in src/md2slack/tables.py (horizontal border with appropriate T-junctions)
- [x] T044 [US2] Implement render_table() function in src/md2slack/tables.py (full table with borders)
- [x] T045 [US2] Implement wrap_cell() function in src/md2slack/tables.py (use textwrap.wrap for long content)
- [x] T046 [US2] Implement table() method in SlackMrkdwnRenderer that builds Table from mistune tokens
- [x] T047 [US2] Implement table_head(), table_body(), table_row(), table_cell() methods in SlackMrkdwnRenderer
- [x] T048 [US2] Update __all__ exports in src/md2slack/tables.py (add TableCell, TableRow, Table, render_table, wrap_cell)
- [x] T049 [US2] Run tests/test_tables.py and tests/test_converter.py table tests, verify all US2 tests pass

**Checkpoint**: Table conversion fully functional with box-drawing output

---

## Phase 5: User Story 3 - Handle Edge Cases Gracefully (Priority: P3)

**Goal**: Handle nested formatting, escaped characters, malformed markdown, and code block preservation

**Independent Test**: Pass edge case inputs and verify no crashes, content preserved, formatting applied where possible

### Tests for User Story 3

- [x] T050 [P] [US3] Test nested formatting (**bold with [link](url)**) in tests/test_converter.py
- [x] T051 [P] [US3] Test escaped characters (\*not bold\*) in tests/test_converter.py
- [x] T052 [P] [US3] Test malformed markdown (**unclosed) in tests/test_converter.py
- [x] T053 [P] [US3] Test code block content preservation in tests/test_converter.py
- [x] T054 [P] [US3] Test empty string input in tests/test_converter.py
- [x] T055 [P] [US3] Test whitespace-only input in tests/test_converter.py
- [x] T056 [P] [US3] Test inline code preservation in tests/test_converter.py

### Implementation for User Story 3

- [x] T057 [US3] Verify nested formatting works via mistune recursive rendering (add test assertions)
- [x] T058 [US3] Verify escaped character handling via mistune (add test assertions)
- [x] T059 [US3] Verify malformed markdown graceful degradation (add test assertions, ensure no exceptions)
- [x] T060 [US3] Verify code block content is not converted (already implemented, add assertions)
- [x] T061 [US3] Verify empty string returns empty string (add edge case handling if needed)
- [x] T062 [US3] Verify whitespace preservation (add edge case handling if needed)
- [x] T063 [US3] Run full test suite and verify all US3 tests pass

**Checkpoint**: All edge cases handled gracefully, no crashes on any input

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, cleanup, and integration

- [x] T064 Run `uv run ruff check .` and fix any linting issues
- [x] T065 Run `uv run pytest` and verify all tests pass
- [x] T066 [P] Add type hints to all public functions in src/md2slack/converter.py
- [x] T067 [P] Add type hints to all public functions in src/md2slack/tables.py
- [x] T068 Run `uv run ruff check .` again after type hint additions
- [x] T069 Validate quickstart.md examples work with implemented code
- [x] T070 Update convert CLI command in src/md2slack/cli.py to use converter.convert()

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion
- **User Story 2 (Phase 4)**: Depends on Foundational; can run parallel to US1 but uses converter
- **User Story 3 (Phase 5)**: Depends on US1 (uses same renderer methods)
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: Foundational only - can start immediately after Phase 2
- **US2 (P2)**: Foundational + needs converter.py base from US1 for table() integration
- **US3 (P3)**: Depends on US1 implementation (tests edge cases of existing methods)

### Within Each User Story

1. Tests written first (ensure they FAIL)
2. Implementation tasks in order
3. Run tests to verify pass

### Parallel Opportunities

**Phase 1 (Setup)**:
```
T002, T003, T004, T005 can run in parallel (different files)
```

**Phase 3 (US1 Tests)**:
```
T012, T013, T014, T015, T016, T017 can all run in parallel (same file but independent tests)
```

**Phase 4 (US2 Tests)**:
```
T032, T033, T034, T035, T036, T037, T038 can all run in parallel
```

**Phase 5 (US3 Tests)**:
```
T050, T051, T052, T053, T054, T055, T056 can all run in parallel
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T011)
3. Complete Phase 3: User Story 1 (T012-T031)
4. **STOP and VALIDATE**: Run `uv run pytest tests/test_converter.py`
5. Basic markdown conversion works - can preview in CLI

### Incremental Delivery

1. **Setup + Foundational** -> Foundation ready
2. **Add US1** -> Test independently -> Basic conversion works (MVP!)
3. **Add US2** -> Test independently -> Tables render with box-drawing
4. **Add US3** -> Test independently -> Edge cases handled gracefully
5. **Polish** -> Linting, type hints, CLI integration

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story independently testable after completion
- Commit after each task or logical group
- mistune handles most edge cases automatically (lenient parser)
- Table rendering is the most complex part (separate module justified)

---

## Summary

| Metric | Count |
|--------|-------|
| **Total Tasks** | 70 |
| **Setup Tasks** | 6 |
| **Foundational Tasks** | 5 |
| **US1 Tasks** | 20 (6 tests + 14 impl) |
| **US2 Tasks** | 18 (7 tests + 11 impl) |
| **US3 Tasks** | 14 (7 tests + 7 impl) |
| **Polish Tasks** | 7 |
| **Parallel Opportunities** | 28 tasks marked [P] |
