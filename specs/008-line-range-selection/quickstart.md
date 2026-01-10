# Quickstart: Line Range Selection

**Feature**: 008-line-range-selection
**Date**: 2026-01-10

## What This Feature Does

Adds a `--lines` option to `md2slack convert` and `md2slack post` commands, allowing you to extract and process only specific lines from a markdown file.

## Usage Examples

### Preview a section before posting

```bash
# Check what lines 45-78 look like after conversion
md2slack convert notes.md --lines 45-78
```

### Post a specific section to Slack

```bash
# Post only lines 45-78 to a thread
md2slack post notes.md --thread "https://org.slack.com/archives/C.../p..." --lines 45-78
```

### Combine with dry-run for safety

```bash
# Preview the chunked output before posting
md2slack post notes.md -t "https://..." --lines 120-180 --dry-run
```

### Works with stdin too

```bash
# Pipe content and extract lines
cat large-doc.md | md2slack convert --lines 10-50
```

## Line Number Reference

- **1-indexed**: Line 1 is the first line (matches your editor)
- **Inclusive**: `--lines 5-10` includes both line 5 and line 10
- **Single line**: Use same number for start and end (`--lines 42-42`)

## Error Handling

Invalid ranges produce clear error messages:

```bash
$ md2slack convert file.md --lines 150-200
Error: Line range 150-200 is out of bounds. File has 100 lines (valid range: 1-100).
```

## When to Use This

- Share a specific table or section from a large reference document
- Post meeting notes without the full agenda
- Extract a code block or example from comprehensive docs
- Preview just the part you care about before posting
