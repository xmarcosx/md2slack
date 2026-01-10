# Research: Convert Command

**Feature**: 004-convert-command
**Date**: 2026-01-10

## Executive Summary

Research reveals that the convert command is **already implemented** in `src/md2slack/cli.py`. The existing implementation exceeds the MVP specification requirements by supporting three input methods: file path, `--text` option, and stdin piping.

## Findings

### Existing Implementation Analysis

**Location**: `src/md2slack/cli.py:21-40`

The convert command already exists with:
- File argument support (`FILE` positional argument with `click.Path(exists=True)`)
- Text option (`--text`/`-t` for direct markdown input)
- Stdin support (reads from stdin when not a TTY)
- Calls `convert_markdown()` from converter module
- Outputs to stdout with no trailing newline

**Current Behavior vs Spec Requirements**:

| Requirement | Spec Says        | Current Implementation  | Status            |
| ----------- | ---------------- | ----------------------- | ----------------- |
| FR-001      | `convert` subcommand | `@cli.command()` convert | PASS              |
| FR-002      | `--file` option  | Positional `FILE` arg   | DIFFERS (simpler) |
| FR-003      | Read + convert   | `Path(file).read_text()` + `convert_markdown()` | PASS |
| FR-004      | Print to stdout  | `click.echo(result, nl=False)` | PASS             |
| FR-005      | Exit 0 on success | Click default behavior | PASS              |
| FR-006      | Errors to stderr | Click raises `UsageError` | PARTIAL          |
| FR-007      | Exit 1 on error  | Click handles this     | PASS              |
| FR-008      | Actionable errors | Click's default messages | NEEDS REVIEW    |
| FR-009      | `--file` required | FILE is optional (has --text and stdin fallbacks) | DIFFERS |

### Gap Analysis

1. **Input mechanism**: Spec calls for `--file <path>` option, implementation uses positional `FILE` argument. The positional argument is actually more ergonomic (`md2slack convert notes.md` vs `md2slack convert --file notes.md`).

2. **Error messages**: Current implementation relies on Click's built-in error handling. For file not found, Click's `exists=True` validation produces: `Error: Invalid value for 'FILE': Path 'missing.md' does not exist.` This is clear but could be more actionable.

3. **Additional features**: Stdin and `--text` support already implemented, exceeding MVP scope.

### Decision

**Recommendation**: The existing implementation satisfies the spirit of the spec and provides a better UX than the literal spec requirements. Rather than regressing to `--file` only:

1. Keep the current implementation as-is
2. Update the spec to reflect the actual CLI interface
3. Add tests for file error scenarios (permission denied)
4. Verify error messages meet "actionable" standard

### Technology Confirmation

- **Framework**: Click 8.0+ (per pyproject.toml)
- **Converter**: `md2slack.converter.convert()` function from feature 003
- **Testing**: pytest with subprocess for CLI tests, Click's CliRunner available

## Alternatives Considered

| Alternative                          | Rejected Because                                |
| ------------------------------------ | ----------------------------------------------- |
| Rewrite to match spec exactly        | Existing impl is superior, would regress UX     |
| Add `--file` as alias to `FILE` arg  | Unnecessary complexity, no user benefit         |
| Remove stdin/--text support          | Violates "Zero Friction" principle, loses value |

## Next Steps

1. Review existing error message wording for actionability
2. Add test coverage for permission denied scenario
3. Update spec to match actual implementation (or accept variance)
4. No new code needed for core functionality
