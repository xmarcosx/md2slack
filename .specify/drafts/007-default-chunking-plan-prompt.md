# Prompt: Default Chunking Implementation

_For use with /speckit.plan_
_Source: .specify/specs/007-default-chunking/spec.md_
_Generated: 2026-01-10_

---

The spec for default chunking should be complete before planning, but the implementation approach is relatively contained. The main change happens in `cli.py` where the `post` command currently has two code paths: one for chunked posting and one for direct posting. We'll collapse this to always use the chunked path, which already handles short content gracefully by returning a single chunk without indicators.

The CLI changes involve removing the `--chunk` / `-c` flag definition, removing the conditional logic that checks for the flag, and ensuring the chunked code path is always taken. The `--chunk-size` option stays since power users may want to tune the threshold. We should also clean up any dead code related to truncation in the non-chunked path.

Testing is the critical piece. The existing chunker tests verify behavior but don't assert that content is preserved correctly. We need tests that verify: (1) the first chunk contains the beginning of the original content, (2) all content is accounted for across chunks when reassembled, and (3) short content still works as a single message. The bug investigation may resolve naturally once the non-chunked path is eliminated, but we should confirm either way.
