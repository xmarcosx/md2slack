# Data Model: Default Chunking

**Feature**: 007-default-chunking
**Date**: 2026-01-10

## Overview

This feature does not introduce new data entities. It modifies the behavior of existing components without changing their structure.

## Existing Entities (Unchanged)

### Chunk

Defined in `src/md2slack/chunker.py`.

```python
@dataclass
class Chunk:
    content: str      # Text content of this chunk
    index: int        # 0-based position in sequence
    total: int        # Total number of chunks
    split_type: str   # How chunk was split: "paragraph", "sentence", "hard", "none"
```

**Properties**:
- `indicator`: Returns `(N/M)` format string
- `with_indicator`: Returns content with indicator appended (only if `total > 1`)

### ChunkResult

Defined in `src/md2slack/chunker.py`.

```python
@dataclass
class ChunkResult:
    chunks: list[Chunk]    # Ordered list of content chunks
    warnings: list[str]    # Warning messages (e.g., oversized blocks)
    original_length: int   # Length of input content
```

**Properties**:
- `chunk_count`: Returns `len(self.chunks)`

## Behavioral Changes

### CLI Parameter Change

**Before**:
```
post [OPTIONS] [FILE]
  --chunk, -c        Enable auto-chunking for long content
  --chunk-size INT   Max chars per chunk (default: 39000)
```

**After**:
```
post [OPTIONS] [FILE]
  --chunk-size INT   Max chars per chunk (default: 39000)
```

The `--chunk` flag is removed; chunking is always enabled.

### Validation Change

**New validation**: `--chunk-size` is capped at `DEFAULT_CHUNK_SIZE` (39000).

```python
# In cli.py, after existing min validation
chunk_size = min(chunk_size, DEFAULT_CHUNK_SIZE)
```

This ensures user-specified values larger than Slack's limit are silently capped.

## State Diagram

The feature does not introduce new states. Content flows through the existing pipeline:

```
Markdown Input
    ↓
convert_markdown()
    ↓
Optional: Apply prefix
    ↓
chunk_content()  ← NOW ALWAYS CALLED (previously conditional)
    ↓
┌─────────────────────────────────────┐
│ If dry_run:                         │
│   Display chunks with break markers │
│   EXIT                              │
└─────────────────────────────────────┘
    ↓
For each chunk:
    ↓
SlackClient.post_message()
    ↓
Success: Display permalink
```

## No API Contracts

This feature does not introduce or modify API endpoints. All changes are internal to the CLI.
