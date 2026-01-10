# Feature Specification: Default Chunking with Content Preservation

**Feature Branch**: `007-default-chunking`
**Created**: 2026-01-10
**Status**: Draft
**Input**: User description: "Make chunking automatic by default, remove --chunk flag, ensure all content reaches Slack reliably"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Post Long Document Without Flags (Priority: P1)

A user has a lengthy markdown document (e.g., meeting notes, report) that exceeds Slack's message size limit. They want to post it to a thread without needing to know about Slack's internal limits or remember any special flags. The tool should automatically split the content across multiple messages, preserving all content in the correct order.

**Why this priority**: This is the core value proposition - zero friction posting. Users shouldn't need to understand Slack's technical constraints.

**Independent Test**: Post a markdown file exceeding 40,000 characters and verify all content appears in Slack across multiple messages in correct order.

**Acceptance Scenarios**:

1. **Given** a markdown file with 50,000 characters, **When** user runs `md2slack post -t <url> large-doc.md`, **Then** all content is posted across multiple messages with chunk indicators (1/N, 2/N, etc.)
2. **Given** a markdown file with 50,000 characters, **When** user runs `md2slack post -t <url> large-doc.md`, **Then** the first message contains the beginning of the document (title, first section)
3. **Given** a markdown file with 50,000 characters, **When** user runs `md2slack post -t <url> large-doc.md`, **Then** the last message contains the end of the document

---

### User Story 2 - Post Short Document Seamlessly (Priority: P1)

A user posts a small markdown file that fits within a single Slack message. The tool should post it as a single message without any chunk indicators, maintaining the same simple experience they had before.

**Why this priority**: Short content is the common case. The change to default chunking must not degrade this experience.

**Independent Test**: Post a markdown file under 3,000 characters and verify it appears as a single message without any indicators.

**Acceptance Scenarios**:

1. **Given** a markdown file with 1,000 characters, **When** user runs `md2slack post -t <url> small-doc.md`, **Then** content is posted as a single message without chunk indicators
2. **Given** a markdown file with 1,000 characters, **When** user runs `md2slack post -t <url> small-doc.md`, **Then** the post completes with a single API call

---

### User Story 3 - Customize Chunk Size (Priority: P2)

A power user wants to control where their content splits (perhaps to align with section breaks or to work around a specific Slack workspace configuration). They can use `--chunk-size` to specify a different threshold than the default.

**Why this priority**: Power user feature. Most users won't need this, but it provides an escape hatch for edge cases.

**Independent Test**: Post a document with `--chunk-size 5000` and verify it splits at the specified threshold rather than the default.

**Acceptance Scenarios**:

1. **Given** a 15,000 character document, **When** user runs `md2slack post -t <url> doc.md --chunk-size 5000`, **Then** content is split into 3 messages instead of 1
2. **Given** a 3,000 character document and `--chunk-size 1000`, **When** posting, **Then** content is split into 3 messages

---

### User Story 4 - Simplified CLI (Priority: P2)

A user who previously used `--chunk` flag finds that the flag no longer exists. The tool's help text reflects this change, showing only `--chunk-size` as an optional parameter. The user experience is simpler with one fewer flag to remember.

**Why this priority**: Supports the "zero friction" principle. Fewer flags = less cognitive load.

**Independent Test**: Run `md2slack post --help` and verify `--chunk`/`-c` flag is not listed while `--chunk-size` remains.

**Acceptance Scenarios**:

1. **Given** the post command, **When** user runs `md2slack post --help`, **Then** output shows `--chunk-size` option but NOT `--chunk` or `-c`
2. **Given** a user tries `md2slack post -t <url> --chunk file.md`, **When** command executes, **Then** CLI reports an error about unknown option `--chunk`

---

### Edge Cases

- What happens when content is exactly at the chunk boundary (e.g., 39,999 characters)? → Should post as single message without indicators
- What happens when content is 1 character over the limit? → Should split into 2 messages with indicators
- What happens when `--chunk-size` is set to a value larger than Slack's limit? → Should use Slack's limit as the maximum
- What happens when content contains only whitespace? → Should handle gracefully (empty or minimal post)
- What happens when the markdown conversion expands content beyond the limit? → Should chunk based on converted size, not original

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST automatically split content exceeding Slack's message limit across multiple messages
- **FR-002**: System MUST post content under the limit as a single message without chunk indicators
- **FR-003**: System MUST preserve all original content across chunks with no data loss
- **FR-004**: System MUST post chunks in correct sequential order (beginning of document first)
- **FR-005**: System MUST add chunk indicators (1/N, 2/N, etc.) when content is split into multiple messages
- **FR-006**: System MUST NOT add chunk indicators when content fits in a single message
- **FR-007**: System MUST remove the `--chunk` and `-c` CLI flags from the post command
- **FR-008**: System MUST retain the `--chunk-size` flag for customizing the split threshold
- **FR-009**: System MUST use the converted mrkdwn size (not original markdown size) to determine chunking needs
- **FR-010**: System MUST cap `--chunk-size` at Slack's maximum message size if user specifies a larger value

### Key Entities

- **Chunk**: A portion of converted content sized to fit within Slack's message limit, with optional indicator prefix
- **Chunk Indicator**: A prefix like "(1/3)" added to multi-message posts to show sequence and total count

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of posted content reaches Slack - no truncation or data loss regardless of document size
- **SC-002**: First chunk of any multi-message post contains the beginning of the original document
- **SC-003**: Users can post documents of any size without specifying any chunking-related flags
- **SC-004**: Short documents (under limit) post as single messages with zero chunk indicators
- **SC-005**: CLI help output shows one fewer required/optional flag compared to previous version

## Assumptions

- Slack's message limit is approximately 40,000 characters (existing behavior)
- The chunker already handles short content gracefully by returning a single chunk without indicators
- Removing the non-chunked code path will simplify maintenance and potentially resolve the reported "missing content" bug
- Users who previously used `--chunk` will see an error message guiding them that the flag is no longer needed
