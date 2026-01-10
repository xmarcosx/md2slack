### 007 - Reliable Posting: Default Chunking with Content Preservation

**Problem**: Two related issues affect posting reliability: (1) The `--chunk` flag requires explicit opt-in, causing silent truncation when users forget it, and (2) a reported bug where content is missing from the beginning of posts. Both undermine trust that all content will be posted.

**Desired State**: Chunking is automatic by default, and all content from the original markdown appears in Slack in correct order—no flags required, no silent data loss.

**Why This Matters**:
1. Users posting long documents shouldn't need to know about Slack's limits or remember flags
2. Content disappearing (from end via truncation OR beginning via bug) destroys trust in the tool
3. Simplifies CLI by removing the `--chunk` flag entirely

**CLI Interface**:
- Command: `md2slack post -t <url> file.md` (unchanged)
- Removed: `--chunk` / `-c` flag
- Kept: `--chunk-size` for customization (power users)
- Output: All content posted, split across multiple messages if needed

**Example**:
- Current: `md2slack post -t <url> large-doc.md` → may truncate or lose beginning content
- Desired: `md2slack post -t <url> large-doc.md` → all content posted reliably

**Scope**:
1. **Make chunking default**: Remove `--chunk` flag, always use chunked path
2. **Investigate content bug**: Verify if bug exists or is display/UX confusion (see `.specify/bugs/001.md`)
3. **Add content preservation tests**: Assert first chunk contains beginning of content, all content preserved across chunks
4. **Remove dead code**: Delete truncate_content usage from non-chunked path (path no longer exists)

**Notes**:
- The chunker already handles short content gracefully (returns single chunk, no indicator)
- Bug may resolve naturally when non-chunked code path is eliminated
- Investigation should confirm whether bug is real data loss or Slack thread display confusion
