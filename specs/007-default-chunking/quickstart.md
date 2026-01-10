# Quickstart: Default Chunking

**Feature**: 007-default-chunking
**Date**: 2026-01-10

## What Changed

Chunking is now automatic. You no longer need to use `--chunk` or `-c` when posting long documents.

### Before

```bash
# Long documents required --chunk flag
md2slack post -t "https://org.slack.com/archives/C.../p..." --chunk long-document.md

# Without it, content was truncated with a warning
md2slack post -t "https://org.slack.com/archives/C.../p..." long-document.md
# Warning: Content exceeds Slack's 40,000 character limit. Truncating.
```

### After

```bash
# Just post - chunking happens automatically
md2slack post -t "https://org.slack.com/archives/C.../p..." long-document.md

# Short documents still post as single messages (no indicators)
md2slack post -t "https://org.slack.com/archives/C.../p..." short-note.md
```

## Usage Examples

### Post a long document

```bash
md2slack post -t "https://myorg.slack.com/archives/C0123ABC/p1234567890123456" report.md
# Output:
# Posting chunk 1/3...
# Posting chunk 2/3...
# Posting chunk 3/3...
# Posted 3 chunks to thread: https://myorg.slack.com/...
```

### Preview chunking with dry-run

```bash
md2slack post -t "https://..." -n long-document.md
# Output:
# --- DRY RUN (not posting) ---
# [First chunk content]
# (1/2)
# --- CHUNK BREAK ---
# [Second chunk content]
# (2/2)
# --- END DRY RUN ---
```

### Custom chunk size (power users)

```bash
# Split at 20,000 characters instead of 39,000
md2slack post -t "https://..." --chunk-size 20000 document.md
```

## Removed Options

| Option        | Status  | Migration                        |
| :------------ | :------ | :------------------------------- |
| `--chunk, -c` | Removed | No action needed; now automatic  |

## Behavioral Notes

1. **Short content**: Posts as single message without any indicators (same as before)
2. **Long content**: Automatically split with `(1/N)`, `(2/N)` indicators
3. **--chunk-size**: Still available for power users; capped at 39,000 (Slack's limit)
4. **--dry-run**: Shows chunk breaks and indicators for preview
