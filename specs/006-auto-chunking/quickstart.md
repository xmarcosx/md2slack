# Quickstart: Auto-Chunking for Long Content

**Feature**: 006-auto-chunking
**Date**: 2026-01-10

## Overview

The auto-chunking feature allows posting markdown documents of any length to Slack threads by automatically splitting content into multiple messages when it exceeds the 40,000 character limit.

## Basic Usage

### Post a long document with auto-chunking

```bash
md2slack post --chunk --thread "https://workspace.slack.com/archives/C123/p456" long-document.md
```

Output:
```
Posting chunk 1/3...
Posting chunk 2/3...
Posting chunk 3/3...
Posted 3 chunks to thread: https://workspace.slack.com/archives/C123/p456000001
```

### Preview chunks without posting (dry run)

```bash
md2slack post --chunk --thread "https://..." --dry-run long-document.md
```

Output:
```
--- DRY RUN (not posting) ---
[Chunk 1 content]
(1/3)
--- CHUNK BREAK ---
[Chunk 2 content]
(2/3)
--- CHUNK BREAK ---
[Chunk 3 content]
(3/3)
--- END DRY RUN ---
```

### Custom chunk size (for testing)

```bash
md2slack post --chunk --chunk-size 10000 --thread "https://..." document.md
```

## How It Works

1. **Content is converted** from markdown to Slack mrkdwn format
2. **Chunking is applied** if content exceeds the size limit:
   - Splits at paragraph boundaries (`\n\n`) when possible
   - Falls back to sentence boundaries (`. `) for large paragraphs
   - Hard splits at character limit as last resort
3. **Code blocks and tables are preserved** - never split mid-element
4. **Chunks are posted sequentially** with 1-second delay between posts
5. **Each chunk includes a continuation indicator** like `(2/5)`

## Examples

### Document that fits in one message

```bash
md2slack post --chunk --thread "https://..." short-doc.md
```

Output:
```
Posted to thread: https://workspace.slack.com/archives/C123/p456000001
```

No chunking indicator added - posted as a single message.

### Document with large code block

If a code block exceeds the chunk size limit:

```bash
md2slack post --chunk --thread "https://..." doc-with-huge-codeblock.md
```

Output:
```
Warning: Code block at line 45 exceeds chunk size (52,000 chars).
         Block will be posted as-is; Slack may truncate.
Posting chunk 1/2...
Posting chunk 2/2...
Posted 2 chunks to thread: https://...
```

### Pipe input with chunking

```bash
cat report.md | md2slack post --chunk --thread "https://..."
```

## CLI Reference

### New options on `post` command

| Option           | Short | Default | Description                                       |
| ---------------- | ----- | ------- | ------------------------------------------------- |
| `--chunk`        | `-c`  | false   | Enable auto-chunking for long content             |
| `--chunk-size`   |       | 39000   | Maximum characters per chunk (min: 1000)          |

### Behavior notes

- `--chunk` without long content: Posts normally, no indicator
- `--dry-run` with `--chunk`: Shows all chunks with break markers
- Progress output goes to stderr; permalink goes to stdout
- On posting failure: Stops immediately, reports which chunks succeeded

## Error Handling

### Oversized block warning

```
Warning: Code block at line N exceeds chunk size (X chars).
         Block will be posted as-is; Slack may truncate.
```

Action: Consider breaking up the code block in your source document.

### Posting failure mid-sequence

```
Error posting chunk 3/5: channel_not_found
Chunks 1-2 posted successfully.
```

Action: Fix the issue and manually post remaining content, or use `--dry-run` to get the remaining chunks.
