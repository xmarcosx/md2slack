# Prompt: Auto-Chunking for Long Content

_For use with /speckit.specify_
_Source: .specify/features/006-auto-chunking.md_
_Generated: 2026-01-10_

---

When users post long markdown documents to Slack, they hit the 40,000 character limit. Currently md2slack truncates with a warning, which means content gets lost. This violates Constitution Principle V (Professional Output)—users trust us not to silently drop their content.

The solution is auto-chunking: when enabled via `--chunk` flag, the tool splits long content into multiple sequential messages posted to the same thread. The chunking needs to be intelligent about where it splits. Splitting mid-paragraph or mid-sentence looks unprofessional. Splitting mid-code-block or mid-table breaks formatting entirely. The ideal split points are paragraph boundaries (double newlines), with fallback to sentence boundaries, and hard splits only as a last resort. Each chunk should include a continuation indicator like `(1/3)` so readers understand they're seeing part of a larger document.

Real-world example: a document like `temp_files/ny.md` with multiple tables and code blocks is about 7,500 characters. Combine five similar reports into a single status update and you're over the limit. The chunker needs to keep tables and code blocks intact—never split mid-block—and warn if a single block exceeds the chunk size since there's no good solution for that case. Rate limiting (1 second between posts) prevents Slack throttling, and progress output like `Posting chunk 2/5...` keeps users informed during longer uploads.
