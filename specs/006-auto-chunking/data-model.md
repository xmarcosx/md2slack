# Data Model: Auto-Chunking for Long Content

**Feature**: 006-auto-chunking
**Date**: 2026-01-10

## Overview

The auto-chunking feature introduces three key data structures for managing content splitting. All structures are internal to the chunking module and not persisted.

## Entities

### Chunk

A segment of content that fits within Slack's message limit.

| Field       | Type   | Description                                              |
| ----------- | ------ | -------------------------------------------------------- |
| content     | str    | The text content of this chunk                           |
| index       | int    | 0-based position in the sequence                         |
| total       | int    | Total number of chunks in the sequence                   |
| split_type  | str    | How this chunk was split: "paragraph", "sentence", "hard" |

**Derived Properties**:
- `indicator` → `(index+1/total)` string, e.g., "(2/5)"
- `with_indicator` → content + newline + indicator (if total > 1)

**Validation Rules**:
- `len(content) <= max_chunk_size`
- `0 <= index < total`
- `total >= 1`

### SplitPoint

A location in the document where content can be divided.

| Field    | Type   | Description                                      |
| -------- | ------ | ------------------------------------------------ |
| position | int    | Character position in the original content       |
| quality  | str    | Split quality: "paragraph", "sentence", "hard"   |

**Quality Priority** (highest to lowest):
1. `"paragraph"` - Double newline (`\n\n`)
2. `"sentence"` - Period followed by space (`. `)
3. `"hard"` - Character limit (last resort)

### ChunkResult

Result of the chunking operation.

| Field             | Type        | Description                                      |
| ----------------- | ----------- | ------------------------------------------------ |
| chunks            | list[Chunk] | Ordered list of content chunks                   |
| warnings          | list[str]   | Warning messages (e.g., oversized blocks)        |
| original_length   | int         | Length of input content                          |
| chunk_count       | int         | Number of chunks produced                        |

**Validation Rules**:
- `sum(len(c.content) for c in chunks) == original_length` (no content lost)
- `all(c.index == i for i, c in enumerate(chunks))` (indices are sequential)

## State Transitions

The chunker uses a simple state machine for code block detection:

```
                    ┌─────────────────────┐
                    │                     │
     ┌──────────────▼──────────────┐      │
     │        NORMAL               │      │
     │   (can split here)          │      │
     └──────────────┬──────────────┘      │
                    │                      │
                    │ encounter ```       │ encounter ```
                    │                      │
     ┌──────────────▼──────────────┐      │
     │       IN_CODE_BLOCK         │      │
     │   (cannot split here)       ├──────┘
     └─────────────────────────────┘
```

**State Rules**:
- In NORMAL state: All split types are valid
- In IN_CODE_BLOCK state: No splits allowed (accumulate until block ends)
- Tables render as code blocks, so same rules apply

## Relationships

```
ChunkResult
    │
    ├── chunks: list[Chunk]
    │       │
    │       └── Each chunk references its position in sequence
    │
    └── warnings: list[str]
            │
            └── Generated when oversized blocks detected
```

## Usage Flow

```
Input: mrkdwn content (str), max_size (int)
                │
                ▼
        ┌───────────────┐
        │ chunk_content │
        └───────┬───────┘
                │
                ▼
    ┌───────────────────────┐
    │ Scan for code blocks  │
    │ Find split points     │
    │ Create Chunk objects  │
    └───────────┬───────────┘
                │
                ▼
        ┌───────────────┐
        │ ChunkResult   │
        └───────────────┘
                │
                ▼
    ┌───────────────────────┐
    │ CLI adds indicators   │
    │ Posts sequentially    │
    └───────────────────────┘
```
