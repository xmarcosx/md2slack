# Feature Specification: Core Converter

**Feature Branch**: `003-core-converter`
**Created**: 2026-01-09
**Status**: Draft
**Input**: User description: "Core converter: pure function transforming markdown to Slack mrkdwn format"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Convert Basic Markdown Text (Priority: P1)

A user has a markdown document with headings, bold text, links, and lists. They want to convert it to Slack's mrkdwn format so it renders correctly when posted to Slack. The converter takes their markdown string and returns a properly formatted mrkdwn string.

**Why this priority**: This is the core value proposition—without basic markdown conversion, the tool has no purpose. Every other feature depends on this working correctly.

**Independent Test**: Can be fully tested by passing markdown strings with headings, bold, links, and lists, then verifying the output matches Slack mrkdwn syntax. Delivers immediate value as users can preview converted content.

**Acceptance Scenarios**:

1. **Given** markdown with `# Heading`, **When** converted, **Then** output contains `*Heading*` (bold format)
2. **Given** markdown with `**bold text**`, **When** converted, **Then** output contains `*bold text*`
3. **Given** markdown with `~~strikethrough~~`, **When** converted, **Then** output contains `~strikethrough~`
4. **Given** markdown with `[link text](https://example.com)`, **When** converted, **Then** output contains `<https://example.com|link text>`
5. **Given** markdown with `- item`, **When** converted, **Then** output contains bullet character followed by item text
6. **Given** markdown with `1. item`, **When** converted, **Then** output contains numbered format (`1.`) followed by item text

---

### User Story 2 - Convert Markdown Tables (Priority: P2)

A user has a markdown document containing tables. Since Slack doesn't support native tables, the converter renders tables as monospace code blocks using Unicode box-drawing characters to preserve the tabular structure.

**Why this priority**: Tables are explicitly mentioned in the feature brief and constitution as a key differentiator. However, basic text conversion must work first.

**Independent Test**: Can be fully tested by passing markdown tables and verifying the output contains properly aligned monospace code blocks with box-drawing characters.

**Acceptance Scenarios**:

1. **Given** a markdown table with headers and rows, **When** converted, **Then** output contains a code block with box-drawing borders
2. **Given** a table with varying column widths, **When** converted, **Then** columns are aligned based on content width
3. **Given** a table with empty cells, **When** converted, **Then** empty cells are rendered as blank space within the table structure
4. **Given** a table with header row, **When** converted, **Then** header row is visually separated from data rows

---

### User Story 3 - Handle Edge Cases Gracefully (Priority: P3)

A user has markdown with nested formatting, escaped characters, or malformed syntax. The converter handles these edge cases gracefully, converting what it can and preserving content that cannot be converted.

**Why this priority**: Edge cases matter for real-world usage but the primary conversion rules must work first. Graceful degradation ensures the tool doesn't break on unexpected input.

**Independent Test**: Can be fully tested by passing edge case inputs and verifying output is reasonable (no crashes, no data loss, formatting preserved where possible).

**Acceptance Scenarios**:

1. **Given** markdown with nested formatting like `**bold with [link](url)**`, **When** converted, **Then** both bold and link formatting are applied
2. **Given** markdown with escaped characters like `\*not bold\*`, **When** converted, **Then** escaped characters are preserved literally
3. **Given** malformed markdown like unclosed bold `**broken`, **When** converted, **Then** content is preserved without crashing
4. **Given** code blocks containing markdown-like syntax, **When** converted, **Then** code block content is not converted (preserved literally)

---

### Edge Cases

- What happens when input is an empty string? (Return empty string)
- What happens when input contains only whitespace? (Preserve whitespace)
- How does the converter handle very long lines in tables? (Wrap text within cells to create multi-line cells, preserving all content)
- What happens with deeply nested lists? (Convert with appropriate indentation up to reasonable depth)
- How are inline code spans handled? (Preserve with backticks, which Slack supports)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Converter MUST transform markdown headings (`#`, `##`, etc.) to bold text (`*heading*`)
- **FR-002**: Converter MUST transform double-asterisk bold (`**text**`) to single-asterisk bold (`*text*`)
- **FR-003**: Converter MUST transform double-tilde strikethrough (`~~text~~`) to single-tilde (`~text~`)
- **FR-004**: Converter MUST transform markdown links (`[text](url)`) to Slack format (`<url|text>`)
- **FR-005**: Converter MUST transform unordered list items (`- item`, `* item`) to bullet points using the bullet character
- **FR-006**: Converter MUST render markdown tables as monospace code blocks with Unicode box-drawing characters
- **FR-007**: Converter MUST preserve code blocks and inline code without modification (backticks supported by Slack)
- **FR-008**: Converter MUST handle nested formatting (e.g., bold inside links) correctly
- **FR-009**: Converter MUST preserve escaped characters literally without converting them
- **FR-010**: Converter MUST be a pure function with no side effects (input string in, output string out)
- **FR-011**: Converter MUST degrade gracefully on malformed markdown (no crashes, preserve content)
- **FR-012**: Converter MUST align table columns based on content width
- **FR-013**: Converter MUST visually separate table header rows from data rows using box-drawing characters
- **FR-014**: Converter MUST wrap long table cell content into multi-line cells, preserving all content
- **FR-015**: Converter MUST transform ordered list items (`1. item`) to numbered format, preserving the numbering

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All standard markdown elements (headings, bold, strikethrough, links, lists) convert correctly 100% of the time for well-formed input
- **SC-002**: Converted tables display readable tabular data with aligned columns when viewed in Slack
- **SC-003**: Converter handles malformed input without crashing in 100% of cases
- **SC-004**: Round-trip preservation: content meaning is preserved through conversion (no data loss)
- **SC-005**: Conversion completes in under 100ms for documents up to 10,000 characters

## Clarifications

### Session 2026-01-09

- Q: How should the converter handle table cells that exceed a reasonable display width? → A: Wrap text within cells (multi-line cells, preserves all content)
- Q: Should the converter handle ordered lists (`1. item`, `2. item`)? → A: Yes, convert to numbered format (preserve numbering)

## Assumptions

- Slack's mrkdwn format is the target output (not Slack Block Kit or other formats)
- Standard CommonMark markdown is the expected input format
- Unicode box-drawing characters are supported in Slack's monospace code blocks
- The bullet character (U+2022) renders correctly in Slack
- Performance target of 100ms is sufficient for typical CLI usage
- Table column width is determined by longest content in each column (no max-width truncation by default)
