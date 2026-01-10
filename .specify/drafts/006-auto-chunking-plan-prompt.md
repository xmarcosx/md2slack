# Prompt: Auto-Chunking Implementation

_For use with /speckit.plan_
_Source: specs/006-auto-chunking/spec.md_
_Generated: 2026-01-10_

---

The auto-chunking feature builds on the existing `post` command in `cli.py` and the Slack integration in `slack.py`. The core chunking logic should live in a new module—perhaps `chunker.py`—since it's a self-contained algorithm that takes converted mrkdwn content and returns a list of appropriately-sized chunks.

The chunker needs awareness of markdown structure to find good split points. It should scan for paragraph boundaries first, then sentence boundaries if paragraphs are too large. Code blocks and tables (which render as code blocks) need special handling: the chunker must track when it's inside a fenced block and never split there. If a single block exceeds the chunk size, the chunker should keep it intact and emit a warning rather than produce broken output.

The CLI changes are straightforward: add `--chunk` and `--chunk-size` flags to the `post` command, then loop through chunks with a 1-second delay between posts. Progress output goes to stderr so it doesn't interfere with the final permalink output. Testing should cover the boundary detection logic extensively—paragraph splits, sentence fallback, code block preservation, and the edge case of oversized single blocks.
