# Feature Specification: Convert Command

**Feature Branch**: `004-convert-command`
**Created**: 2026-01-10
**Status**: Implemented
**Input**: User description: "The convert command is the preview mechanism for md2slack, allowing users to see exactly what their markdown will look like after conversion to Slack's mrkdwn format before posting to a thread."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Preview Markdown Conversion (Priority: P1)

A developer has written a status update in markdown and wants to verify how it will appear in Slack before posting. They run the convert command with their file to preview the converted output without any side effects.

**Why this priority**: This is the core and only functionality of this feature. Users need confidence that their content will look correct before posting to irreversible Slack threads (Constitution Principle IV: Preview Before Commit).

**Independent Test**: Can be fully tested by running the command with a markdown file and verifying the converted mrkdwn output matches expected format. Delivers immediate value by showing users exactly what would be posted.

**Acceptance Scenarios**:

1. **Given** a valid markdown file exists at the specified path, **When** the user runs `md2slack convert notes.md`, **Then** the converted mrkdwn content is printed to stdout and the command exits with code 0
2. **Given** a markdown file with headings, bold text, links, and tables, **When** the user runs the convert command, **Then** all elements are converted to Slack mrkdwn format (headings to bold, tables to box-drawing code blocks, etc.)

---

### User Story 2 - Handle Missing File Gracefully (Priority: P2)

A developer accidentally specifies a file path that doesn't exist. The CLI provides a clear, actionable error message so they can correct their command.

**Why this priority**: Error handling is essential for usability but secondary to the core conversion functionality. Per Constitution Principle V (Professional Output), errors must be clear and actionable.

**Independent Test**: Can be tested by running the command with a non-existent file path and verifying the error message and exit code.

**Acceptance Scenarios**:

1. **Given** no file exists at the specified path, **When** the user runs `md2slack convert missing.md`, **Then** an error message is printed to stderr indicating the file was not found, and the command exits with code 2
2. **Given** the file path is a directory instead of a file, **When** the user runs the convert command, **Then** an appropriate error message is displayed and the command exits with code 2

---

### User Story 3 - Handle Permission Errors (Priority: P3)

A developer specifies a file they don't have permission to read. The CLI provides an actionable error message explaining the permission issue.

**Why this priority**: Permission errors are less common than missing files but still need graceful handling for a professional tool.

**Independent Test**: Can be tested by running the command with a file that has restricted read permissions and verifying the error message.

**Acceptance Scenarios**:

1. **Given** a file exists but the user lacks read permission, **When** the user runs `md2slack convert restricted.md`, **Then** an error message about permission denied is printed to stderr, and the command exits with code 2

---

### Edge Cases

- What happens when the file is empty? The command outputs nothing (empty string) and exits with code 0.
- What happens when the file contains only whitespace? The command outputs the whitespace as-is (after conversion) and exits with code 0.
- What happens when no input is provided? The CLI displays an error message explaining the three input options: FILE, --text, or stdin piping.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a `convert` subcommand accessible as `md2slack convert`
- **FR-002**: System MUST accept a positional `FILE` argument specifying the path to a markdown file
- **FR-002a**: System SHOULD also support `--text` option for inline markdown input
- **FR-002b**: System SHOULD also support stdin piping for flexible input
- **FR-003**: System MUST read the contents of the specified input and convert it using the existing converter module
- **FR-004**: System MUST print the converted mrkdwn content to stdout on success
- **FR-005**: System MUST exit with code 0 on successful conversion
- **FR-006**: System MUST print error messages to stderr (not stdout) when errors occur
- **FR-007**: System MUST exit with code 2 for invalid arguments (file not found, permission denied, directory)
- **FR-007a**: System MUST exit with code 1 for usage errors (no input provided)
- **FR-008**: Error messages MUST be actionable, indicating what went wrong and suggesting how to fix it
- **FR-009**: At least one input method (FILE, --text, or stdin) MUST be provided

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can preview converted markdown output in under 1 second for typical files (< 100KB)
- **SC-002**: 100% of file system errors (not found, permission denied) produce user-friendly error messages
- **SC-003**: Output from the convert command exactly matches what would be posted via the future post command
- **SC-004**: Users can verify their markdown content looks correct before posting, eliminating surprise formatting issues in Slack threads

## Assumptions

- The converter module from feature 003 is complete and available for import
- Standard CLI conventions apply: stdout for output, stderr for errors, exit 0 for success, non-zero for failure
- Implementation exceeds MVP scope: supports FILE, --text, and stdin input methods

## Implementation Notes

The actual implementation differs from the original spec in ways that improve user experience:

1. **Positional FILE argument** instead of `--file` option - simpler syntax: `md2slack convert notes.md`
2. **Multiple input methods** - FILE, `--text`, and stdin piping are all supported
3. **Exit code 2** for invalid arguments (Click's default for bad arguments)
4. **Exit code 1** for usage errors (no input provided)

These changes align with Constitution Principle III (Zero Friction) while maintaining professional error handling (Principle V).
