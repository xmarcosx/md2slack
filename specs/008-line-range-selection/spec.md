# Feature Specification: Line Range Selection

**Feature Branch**: `008-line-range-selection`
**Created**: 2026-01-10
**Status**: Draft
**Input**: User description: "Add --lines option to extract and post specific line ranges from markdown files"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Post Section from Large Document (Priority: P1)

A user maintains a comprehensive markdown file (e.g., meeting notes, reference documentation) and needs to share only a specific section with their Slack thread. They identify the relevant lines in their editor (e.g., lines 45-78), then use the `--lines` flag to post just that section without creating a temporary file or copy-pasting.

**Why this priority**: This is the core use case that motivated the feature. Without it, users must manually extract content, defeating the one-command workflow principle.

**Independent Test**: Can be fully tested by running `md2slack post file.md --thread URL --lines 45-78` and verifying only lines 45-78 appear in Slack.

**Acceptance Scenarios**:

1. **Given** a 200-line markdown file, **When** user runs `md2slack post file.md --thread URL --lines 45-78`, **Then** only lines 45 through 78 (inclusive) are converted and posted to Slack
2. **Given** a markdown file with a table spanning lines 120-145, **When** user runs `md2slack post file.md --thread URL --lines 120-145`, **Then** the complete table is converted to box-drawing format and posted

---

### User Story 2 - Preview Section Before Posting (Priority: P2)

A user wants to verify the converted output of a specific section before posting it to Slack. They use the `convert` command with the `--lines` flag to preview the mrkdwn output for just that section.

**Why this priority**: Aligns with the "Preview Before Commit" constitution principle. Users need confidence before posting to client threads.

**Independent Test**: Can be fully tested by running `md2slack convert file.md --lines 10-25` and verifying only those lines appear in stdout.

**Acceptance Scenarios**:

1. **Given** a markdown file, **When** user runs `md2slack convert file.md --lines 10-25`, **Then** only lines 10-25 are converted and displayed to stdout
2. **Given** the same file and range, **When** user later runs `md2slack post file.md --thread URL --lines 10-25`, **Then** the posted content matches the preview exactly

---

### User Story 3 - Handle Invalid Range Gracefully (Priority: P3)

A user specifies a line range that doesn't exist in the file (e.g., requesting lines 150-200 in a 100-line file). The CLI provides a clear error message indicating the valid range.

**Why this priority**: Error handling supports user experience but is secondary to core functionality.

**Independent Test**: Can be fully tested by running with an out-of-bounds range and verifying the error message is clear and actionable.

**Acceptance Scenarios**:

1. **Given** a 100-line file, **When** user runs `md2slack post file.md --thread URL --lines 150-200`, **Then** CLI displays an error message indicating the file has only 100 lines
2. **Given** any file, **When** user runs with `--lines 50-30` (start > end), **Then** CLI displays an error message explaining the range format

---

### Edge Cases

- What happens when the range includes only a single line (e.g., `--lines 5-5`)? **Expected**: Extract and process that one line.
- What happens when the range starts at line 1? **Expected**: Works normally, line 1 is valid.
- What happens when the range ends exactly at the last line? **Expected**: Works normally, includes the last line.
- What happens when the range partially overlaps file bounds (e.g., `--lines 90-150` in a 100-line file)? **Expected**: Error message indicating valid range is 1-100.
- What happens when `--lines` is used with stdin input instead of a file? **Expected**: Works the same way—stdin content is read, lines are counted and extracted.
- What happens when the file has trailing empty lines? **Expected**: Empty lines count toward line numbers and are included if within range.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a `--lines` option in format `START-END` where START and END are positive integers
- **FR-002**: System MUST use 1-indexed line numbers matching editor conventions (line 1 is the first line)
- **FR-003**: System MUST treat the range as inclusive on both ends (e.g., `--lines 5-10` includes lines 5, 6, 7, 8, 9, and 10)
- **FR-004**: System MUST support `--lines` option on both `post` and `convert` commands
- **FR-005**: System MUST extract the specified lines before any conversion or processing occurs
- **FR-006**: System MUST display a clear error message when START is greater than END
- **FR-007**: System MUST display a clear error message when the range extends beyond the file's actual line count, including the valid range in the message
- **FR-008**: System MUST support single-line ranges where START equals END (e.g., `--lines 5-5`)
- **FR-009**: System MUST work with stdin input when no file is specified, applying line extraction to the piped content
- **FR-010**: System MUST preserve the original line content exactly, including any leading/trailing whitespace within lines

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can extract and post a section from a 500-line file in a single command without creating intermediate files
- **SC-002**: The `--lines` option works identically on both `post` and `convert` commands
- **SC-003**: Error messages for invalid ranges include the valid line range, enabling users to correct their command on the first retry
- **SC-004**: Line extraction completes instantly (< 100ms) for files up to 10,000 lines
- **SC-005**: 100% of edge cases (single-line range, first line, last line, stdin) behave as documented

## Assumptions

- Users know their editor's line numbers and can identify the range they want to extract
- File encoding is UTF-8 (consistent with existing markdown handling)
- Line endings follow Unix (LF) or Windows (CRLF) conventions and both are supported
- The `--lines` option is optional; omitting it processes the entire file (existing behavior)
