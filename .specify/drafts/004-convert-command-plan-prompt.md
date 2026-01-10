# Prompt: Convert Command Implementation

_For use with /speckit.plan_
_Source: .specify/specs/004-convert-command/spec.md_
_Generated: 2026-01-10_

---

The convert command spec is complete and implementation should be straightforward since it's a thin wrapper around the already-implemented converter module from feature 003. The command implementation belongs in `src/md2slack/cli.py` as a new Click command alongside the existing CLI structure.

The implementation flow is: read file contents, pass to the `convert_markdown()` function from `converter.py`, and print the result to stdout. Error handling should catch file I/O exceptions (FileNotFoundError, PermissionError) and translate them into user-friendly messages on stderr with appropriate exit codes. The Click framework handles argument parsing and help text.

Testing should cover the happy path (valid file produces converted output), file not found, permission denied, and empty file edge cases. Since the converter itself is already tested in feature 003, these tests focus on the CLI integration layer - file reading, output routing, and exit codes. Tests can use Click's CliRunner for invoking the command in isolation.
