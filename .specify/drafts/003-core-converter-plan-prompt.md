# Prompt: Core Converter Implementation

_For use with /speckit.plan_
_Source: .specify/specs/003-core-converter/spec.md_
_Generated: 2026-01-09_

---

The core converter spec defines the transformation from markdown to Slack mrkdwn. For implementation, this should live in `src/md2slack/converter.py` as the main conversion module, with table-specific logic in `src/md2slack/tables.py` since table rendering is complex enough to warrant separation.

The implementation approach should use an existing markdown parser (mistune is lightweight and extensible) rather than hand-rolling regex patterns. Parse the markdown into an AST, then walk the tree and render each node type to its Slack equivalent. This is cleaner than string manipulation and handles nested structures correctly. The table renderer will need to calculate column widths from content, then draw the box-drawing frame around properly padded cells.

Testing should be thorough since this is the core value of the tool. Each conversion rule needs tests with simple cases and edge cases. Table tests should verify alignment and box-drawing output. The constitution requires comprehensive coverage of all supported elements, so the test file will be substantial—but that's appropriate for the feature that matters most.
