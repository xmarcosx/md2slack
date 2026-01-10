# Research: Auto-Chunking for Long Content

**Feature**: 006-auto-chunking
**Date**: 2026-01-10
**Status**: Complete

## Research Questions

### 1. Chunking Algorithm Approach

**Decision**: State machine with block tracking

**Rationale**: The chunker needs to track whether it's inside a code block or table to avoid splitting mid-element. A simple state machine approach:
- Track `in_code_block` state (toggle on triple backticks)
- Tables in mrkdwn are rendered as code blocks, so same tracking applies
- When seeking split point, skip if inside a protected block

**Alternatives Considered**:
- **Regex-based detection**: Rejected. Fragile with nested structures and edge cases (backticks in strings, escaped characters).
- **AST-based parsing**: Rejected. Overkill for this use case since we're operating on already-converted mrkdwn, not raw markdown. The mrkdwn format is simpler.
- **Line-by-line streaming**: Rejected. Need to look ahead/behind for paragraph boundaries.

### 2. Split Point Priority Implementation

**Decision**: Greedy backward search from chunk boundary

**Rationale**: Given a maximum chunk size:
1. Start at position `max_size` in the remaining content
2. Search backward for paragraph boundary (`\n\n`)
3. If not found within reasonable range (50% of chunk), search for sentence boundary (`. `)
4. If still not found, hard split at `max_size`

This ensures we always make progress while preferring natural boundaries.

**Alternatives Considered**:
- **Forward search from start**: Rejected. Would require reprocessing and could produce very small chunks if boundaries are sparse.
- **Optimal splitting (dynamic programming)**: Rejected. Unnecessary complexity for a CLI tool; greedy approach is good enough.

### 3. Code Block Detection in mrkdwn

**Decision**: Track triple backtick delimiters

**Rationale**: In Slack mrkdwn format:
- Code blocks are delimited by triple backticks on their own lines
- Tables are rendered as code blocks by the converter (see `converter.py:200`)
- No nested code blocks in mrkdwn

Detection approach:
```python
if line.strip().startswith("```"):
    in_code_block = not in_code_block
```

**Alternatives Considered**:
- **Count backticks**: Rejected. Triple backticks are the only fence style in mrkdwn.
- **Parse original markdown**: Rejected. Chunking operates post-conversion on mrkdwn.

### 4. Continuation Indicator Format

**Decision**: `(N/M)` suffix on each chunk

**Rationale**:
- Format: `(1/3)`, `(2/3)`, `(3/3)`
- Appended at the end of each chunk after a newline
- Only added when total chunks > 1
- Takes ~8 characters maximum (e.g., `(10/10)`) - negligible overhead

**Alternatives Considered**:
- **Header prefix**: Rejected. Would change how content appears at the top of messages.
- **Part N of M**: Rejected. Longer, takes more character budget.
- **Unicode indicators**: Rejected. May not render consistently in all Slack clients.

### 5. Rate Limiting Strategy

**Decision**: Fixed 1-second delay between posts

**Rationale**:
- Slack's rate limits are complex (tier-based per method)
- `chat.postMessage` is Tier 2 (approximately 1 request per second)
- Fixed 1-second delay is simple and sufficient for typical use cases
- For very long documents (10+ chunks), this adds reasonable wait time

**Alternatives Considered**:
- **Exponential backoff on 429**: Could be added later, but fixed delay should prevent hitting limits.
- **No delay**: Rejected. Would hit rate limits on documents with 3+ chunks.
- **Configurable delay**: Rejected. Adds complexity without clear benefit.

### 6. Error Handling for Oversized Blocks

**Decision**: Warn and post as-is, let Slack truncate

**Rationale**:
- If a single code block or table exceeds 40,000 characters, there's no good way to split it
- Splitting breaks the formatting (code block wouldn't render correctly)
- Better to warn the user and let them see partial content than fail entirely
- Slack will truncate but at least some content is visible

**Alternatives Considered**:
- **Fail with error**: Rejected. Too harsh; partial content is better than none.
- **Force split**: Rejected. Would produce broken output (unclosed code blocks).
- **Compress/summarize**: Rejected. Out of scope; tool should be transparent about content.

### 7. Chunk Size Configuration

**Decision**: Default 39,000 with `--chunk-size` override

**Rationale**:
- Slack limit is 40,000 characters
- Default to 39,000 to leave buffer for continuation indicator and formatting
- Allow override via `--chunk-size` for testing or future-proofing
- Minimum enforced at 1,000 (smaller chunks would be impractical)

**Alternatives Considered**:
- **No configuration**: Rejected. Testing would require full 40K documents.
- **Config file setting**: Could be added later; flag is sufficient for MVP.

### 8. Progress Output Location

**Decision**: stderr for progress, stdout for final result

**Rationale**:
- Progress messages (`Posting chunk 2/5...`) go to stderr
- Final permalink output goes to stdout
- Follows Unix convention: data to stdout, metadata to stderr
- Allows piping permalink to other tools while seeing progress

**Alternatives Considered**:
- **All to stdout**: Rejected. Would mix data with progress, breaking scripts.
- **Verbose flag for progress**: Rejected. Progress should always show for multi-chunk posts.

## Dependencies

No new dependencies required. The feature uses:
- **click**: Already used for CLI (flags, echo to stderr)
- **time.sleep**: Standard library for rate limiting
- **re**: Standard library for boundary detection (already in converter.py)

## Risks and Mitigations

| Risk                           | Probability | Impact | Mitigation                                       |
| ------------------------------ | ----------- | ------ | ------------------------------------------------ |
| Slack changes rate limits      | Low         | Medium | Configurable delay could be added if needed      |
| Slack changes message limit    | Low         | Medium | `--chunk-size` flag allows user override         |
| Edge case in block detection   | Medium      | Low    | Comprehensive test coverage for edge cases       |
| Performance on huge documents  | Low         | Low    | Linear algorithm; 1M chars < 1 second            |
