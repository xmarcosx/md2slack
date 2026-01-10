### 006 - Auto-Chunking for Long Content

**Problem**: Long markdown documents exceed Slack's 40,000 character limit. Current behavior truncates with a warning, losing content.

**Desired State**: Automatically split long content into multiple sequential messages, preserving readability and context.

**Why This Matters**:
1. Constitution Principle V (Professional Output)—no content loss
2. Large status updates, documentation, or reports can be posted without manual splitting
3. Maintains formatting integrity across chunk boundaries

**CLI Interface**:
- Flag: `--chunk` / `-c` enables auto-chunking (default: truncate with warning)
- Flag: `--chunk-size <n>` sets max characters per chunk (default: 39000)
- Output: Posts multiple messages in sequence, reports count

**Example**:
- `md2slack post -t <url> large-doc.md --chunk`
- Output: `Posted 3 messages to thread: <permalink>`

**Chunking Strategy**:
1. Split at paragraph boundaries (double newline) when possible
2. Fallback to sentence boundaries (`. `) if paragraphs too large
3. Hard split at chunk size if no natural boundary found
4. Add continuation indicator: `(1/3)`, `(2/3)`, `(3/3)` to each chunk
5. Preserve code blocks—never split mid-block

**Notes**:
- Rate limiting: 1 second delay between posts to avoid Slack throttling
- Tables: Keep entire table in one chunk if possible; warn if table exceeds limit
- Code blocks: Never split; warn if single code block exceeds chunk size
- Progress indicator for large documents: `Posting chunk 2/5...`
