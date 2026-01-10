# Prompt: Line Range Selection Implementation

_For use with /speckit.plan_
_Source: .specify/specs/008-line-range-selection/spec.md_
_Generated: 2026-01-10_

---

The line range selection spec is complete and ready for implementation. This feature adds a `--lines` option to both the `post` and `convert` commands that extracts a subset of lines from the input file before processing. The change is localized to the CLI layer—the converter and Slack posting logic remain unchanged since they just receive markdown content.

The implementation should add the `--lines` option to both commands in `cli.py`, with a helper function to parse the range string and validate it against the file's line count. The line extraction should happen early in the command flow, right after reading the file content, so the rest of the pipeline (conversion, chunking, posting) works with the extracted content as if it were the entire file. Error handling should catch invalid range formats (not matching `N-M` pattern) and out-of-bounds ranges (start or end beyond file length, or start > end).

Testing should cover the option parsing, range validation, and line extraction logic. Include edge cases like single-line ranges (`--lines 5-5`), ranges at file boundaries, and various error conditions. Since this touches both commands, tests should verify the option works consistently across `post` and `convert`.
