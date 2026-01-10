# Prompt: Default Chunking with Content Preservation

_For use with /speckit.specify_
_Source: .specify/features/007-default-chunking.md_
_Generated: 2026-01-10_

---

The current `post` command has a friction point: the `--chunk` flag requires explicit opt-in, which means users who forget it risk silent truncation of their content. There's also a reported bug where content appears missing from the beginning of posts (documented in `.specify/bugs/001.md`). Both issues undermine trust that all content will make it to Slack.

The fix is straightforward: make chunking automatic. When a user runs `md2slack post -t <url> file.md`, the tool should intelligently split long content across multiple messages without any flags. Short content would still result in a single message. The `--chunk` flag becomes redundant and should be removed entirely, though `--chunk-size` stays available for power users who need to customize the split threshold.

This change aligns with Constitution Principle III (Zero Friction) by eliminating a flag that shouldn't exist, and Principle II (Faithful Conversion) by ensuring all content reaches Slack. As part of this work, we need to investigate whether the "missing content" bug is a real code issue or user confusion about thread replies, add tests that verify the first chunk contains the beginning of content, and clean up the now-dead non-chunked code path.
