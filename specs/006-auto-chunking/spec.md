# Feature Specification: Auto-Chunking for Long Content

**Feature Branch**: `006-auto-chunking`
**Created**: 2026-01-10
**Status**: Draft
**Input**: User description: "When users post long markdown documents to Slack, they hit the 40,000 character limit. Currently md2slack truncates with a warning, which means content gets lost. The solution is auto-chunking: when enabled via `--chunk` flag, the tool splits long content into multiple sequential messages posted to the same thread. The chunking needs to be intelligent about where it splits—paragraph boundaries preferred, sentence boundaries as fallback, hard splits as last resort. Each chunk should include a continuation indicator like `(1/3)`. Tables and code blocks must never be split mid-block. Rate limiting (1 second between posts) prevents Slack throttling, and progress output keeps users informed."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Post Long Document Successfully (Priority: P1)

A user has a lengthy status report or documentation that exceeds Slack's 40,000 character limit. They want to post the entire document to a Slack thread without losing any content.

**Why this priority**: This is the core problem the feature solves. Without this, users lose content when posting long documents—a violation of professional output standards.

**Independent Test**: Can be fully tested by creating a markdown file exceeding 40,000 characters, running the post command with `--chunk`, and verifying all content appears in the thread as sequential messages.

**Acceptance Scenarios**:

1. **Given** a markdown file with 80,000 characters, **When** the user runs `md2slack post --chunk --channel C123 --thread-ts 1234.5678 file.md`, **Then** the content is split into multiple messages and all messages are posted to the same thread in order.
2. **Given** a markdown file with 80,000 characters, **When** chunking is enabled, **Then** each message includes a continuation indicator showing position (e.g., `(1/3)`, `(2/3)`, `(3/3)`).
3. **Given** a markdown file under 40,000 characters, **When** the user runs the command with `--chunk`, **Then** the content is posted as a single message without a continuation indicator.

---

### User Story 2 - Intelligent Split Points (Priority: P1)

A user posts a long document and expects the splits to occur at natural boundaries—between paragraphs or sentences—rather than cutting off mid-sentence or mid-word.

**Why this priority**: Poor split points make output look unprofessional and hard to read. This directly impacts the quality of the feature's core functionality.

**Independent Test**: Can be tested by posting a document with clear paragraph structure and verifying splits occur only at paragraph boundaries (double newlines).

**Acceptance Scenarios**:

1. **Given** a document with multiple paragraphs, **When** the content is chunked, **Then** splits occur at paragraph boundaries (double newlines) whenever possible.
2. **Given** a document where a paragraph exceeds the chunk size, **When** the content is chunked, **Then** the split occurs at a sentence boundary within that paragraph.
3. **Given** a document where a sentence exceeds the chunk size, **When** the content is chunked, **Then** a hard split occurs at the character limit with appropriate handling.

---

### User Story 3 - Preserve Code Blocks and Tables (Priority: P1)

A user posts a technical document containing code blocks and tables. They expect these elements to remain intact and properly formatted—never split in the middle.

**Why this priority**: Splitting code blocks or tables mid-element breaks formatting and renders the output useless for technical content. This is critical for the target audience.

**Independent Test**: Can be tested by posting a document with a large table and verifying the table appears complete in a single chunk.

**Acceptance Scenarios**:

1. **Given** a document with a code block, **When** the content is chunked, **Then** the code block is never split—it appears complete in one chunk.
2. **Given** a document with a markdown table, **When** the content is chunked, **Then** the table is never split—it appears complete in one chunk.
3. **Given** a code block or table that exceeds the chunk size limit, **When** processing occurs, **Then** a warning is displayed to the user indicating the block cannot be safely split.

---

### User Story 4 - Rate Limiting and Progress Feedback (Priority: P2)

A user posts a very long document that results in many chunks. They want to see progress as chunks are posted and expect the tool to respect Slack's rate limits.

**Why this priority**: Important for user experience and API compliance, but the core chunking functionality must work first.

**Independent Test**: Can be tested by posting a document that produces 5+ chunks and observing progress messages and timing between posts.

**Acceptance Scenarios**:

1. **Given** a document that produces multiple chunks, **When** posting occurs, **Then** progress output is displayed (e.g., `Posting chunk 2/5...`).
2. **Given** multiple chunks to post, **When** each chunk is sent, **Then** at least 1 second delay occurs between posts to prevent Slack API throttling.
3. **Given** posting is in progress, **When** all chunks complete, **Then** a summary message confirms successful completion with total chunks posted.

---

### Edge Cases

- What happens when a single code block or table exceeds the entire chunk size limit? → Display a warning and include the block as-is (Slack will truncate but user is informed)
- What happens when the document is exactly at the chunk size limit? → Post as single message without indicator
- What happens if a chunk ends up being empty after splitting? → Skip empty chunks, do not post them
- What happens if posting a chunk fails mid-way through? → Stop posting, display error with chunk number that failed, indicate which chunks succeeded
- What happens when `--chunk` is used but chunking isn't needed? → Proceed normally with single message, no indicator

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a `--chunk` flag on the post command to enable auto-chunking behavior
- **FR-002**: System MUST split content into chunks that do not exceed 40,000 characters each
- **FR-003**: System MUST prioritize split points in this order: paragraph boundaries (double newlines), sentence boundaries (period followed by space), hard character limit
- **FR-004**: System MUST never split content in the middle of a fenced code block (``` delimited)
- **FR-005**: System MUST never split content in the middle of a markdown table
- **FR-006**: System MUST include a continuation indicator in the format `(N/M)` at the end of each chunk when multiple chunks are posted
- **FR-007**: System MUST post all chunks to the same Slack thread in sequential order
- **FR-008**: System MUST wait at least 1 second between posting each chunk to respect rate limits
- **FR-009**: System MUST display progress output showing which chunk is being posted (e.g., `Posting chunk 2/5...`)
- **FR-010**: System MUST display a warning when a code block or table exceeds the chunk size limit
- **FR-011**: System MUST skip empty chunks and not attempt to post them
- **FR-012**: System MUST stop posting and report an error if any chunk fails to post, indicating which chunks succeeded

### Key Entities

- **Chunk**: A segment of the original content sized to fit within Slack's message limit, with split point and position metadata
- **Split Point**: A location in the document where content can be divided, categorized by quality (paragraph > sentence > hard)
- **Continuation Indicator**: A marker appended to chunks showing position in sequence (e.g., `(2/5)`)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can post documents of any length without losing content (100% content preservation when chunking is enabled)
- **SC-002**: 95% of splits occur at paragraph or sentence boundaries (not hard character splits)
- **SC-003**: Zero instances of code blocks or tables being split mid-element
- **SC-004**: All chunks post successfully to the same thread in correct order
- **SC-005**: Users see progress feedback within 2 seconds of each chunk being posted
- **SC-006**: No Slack API rate limit errors occur during normal operation (1 second delay between posts)

## Assumptions

- Slack's current character limit per message is 40,000 characters (will use this as default, could be configurable)
- Paragraph boundaries are identified by double newlines (`\n\n`)
- Sentence boundaries are identified by period followed by space (`. `)
- Code blocks are delimited by triple backticks (```)
- The existing `post` command infrastructure handles authentication and thread targeting
- Rate limit of 1 second between posts is sufficient to avoid Slack throttling under normal conditions
