# Prompt: Line Range Selection

_For use with /speckit.specify_
_Source: .specify/features/008-line-range-selection.md_
_Generated: 2026-01-10_

---

Users often maintain comprehensive markdown notes in a single file—meeting notes, reference documentation, runbooks—but need to post just a specific section to a Slack thread. Right now they have to manually copy those lines to a temp file or paste directly into Slack, which defeats the purpose of a one-command workflow. We need a `--lines` option that lets users specify a range of lines to extract from the source file before conversion and posting.

The flag should accept a range in the format `--lines START-END` where both values are 1-indexed line numbers (matching what users see in their editors) and the range is inclusive on both ends. So `--lines 123-147` would include lines 123, 124, ... 146, 147. The option should work with both the `post` and `convert` commands since users might want to preview a section before posting it. If the specified range extends beyond the file's actual line count, the CLI should fail with a clear error message indicating the valid range.

The typical workflow would be: user has a 200-line notes file, checks their editor to see lines 45-78 contain the relevant section, then runs `md2slack post notes.md --thread URL --lines 45-78` to post just that section. This preserves the single-command principle while giving users surgical control over what gets shared.
