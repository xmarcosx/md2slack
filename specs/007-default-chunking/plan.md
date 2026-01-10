# Implementation Plan: Default Chunking with Content Preservation

**Branch**: `007-default-chunking` | **Date**: 2026-01-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-default-chunking/spec.md`

## Summary

Make auto-chunking the default behavior for the `post` command by removing the `--chunk` flag and always using the chunked code path. This simplifies the CLI while ensuring all content is reliably posted to Slack without truncation. The change involves removing the `--chunk`/`-c` flag, eliminating the non-chunked code path, and adding tests to verify content preservation.

## Technical Context

**Language/Version**: Python 3.10+ (per pyproject.toml `requires-python = ">=3.10"`)
**Primary Dependencies**: Click 8.0+ (CLI), mistune 3.0+ (markdown), slack_sdk (Slack API)
**Storage**: N/A (stateless CLI operation)
**Testing**: pytest 7.0+ with CliRunner for CLI testing
**Target Platform**: Cross-platform CLI (macOS, Linux, Windows)
**Project Type**: Single package (src/md2slack/)
**Performance Goals**: N/A (network-bound, single-user CLI)
**Constraints**: Slack's 40,000 character message limit
**Scale/Scope**: Single-user CLI tool

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle               | Status | Evidence                                                                               |
| :---------------------- | :----- | :------------------------------------------------------------------------------------- |
| I. One-Command Workflow | ✅ PASS | No additional flags required; chunking happens automatically                           |
| II. Faithful Conversion | ✅ PASS | All content preserved across chunks; no truncation                                     |
| III. Zero Friction      | ✅ PASS | Removing `--chunk` flag reduces cognitive load; one fewer option to remember           |
| IV. Preview Before Commit | ✅ PASS | `--dry-run` continues to work, shows chunk breaks for multi-chunk content            |
| V. Professional Output  | ✅ PASS | Chunk indicators (1/N, 2/N) provide clear sequence; no broken or partial content      |

**Gate Result**: PASS - All principles satisfied. This feature directly supports Zero Friction (III) and Faithful Conversion (II).

## Project Structure

### Documentation (this feature)

```text
specs/007-default-chunking/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/md2slack/
├── __init__.py
├── cli.py               # PRIMARY: Remove --chunk flag, always use chunked path
├── chunker.py           # UNCHANGED: Already handles short content gracefully
├── converter.py         # UNCHANGED: Markdown conversion
├── slack.py             # SECONDARY: Remove truncate_content (dead code after change)
└── tables.py            # UNCHANGED: Table rendering

tests/
├── __init__.py
├── conftest.py
├── test_chunker.py      # ADD: Content preservation tests
├── test_cli.py          # MODIFY: Update tests for removed --chunk flag
├── test_converter.py    # UNCHANGED
├── test_slack.py        # UNCHANGED (truncate_content tests can remain)
└── test_tables.py       # UNCHANGED
```

**Structure Decision**: Single package structure; changes confined to `cli.py` (main), `slack.py` (cleanup), and test files.

## Complexity Tracking

No constitution violations. This feature reduces complexity by:
1. Removing a CLI flag (`--chunk`)
2. Eliminating a code path (non-chunked posting)
3. Removing dead code (`truncate_content` import in cli.py)

## Design Decisions

### D1: Always-Chunked Code Path

**Decision**: Remove the conditional branch in `cli.py` that checks `if chunk:` and always execute the chunked code path.

**Rationale**: The chunker already handles short content gracefully by returning a single chunk without indicators. This means:
- Short content (< 39,000 chars): Single message, no indicators, identical behavior to current non-chunked path
- Long content: Automatically chunked with indicators, no user action needed

**Alternative Rejected**: Auto-chunk only above a threshold (e.g., 20K characters). This adds complexity without benefit since the chunker already handles all cases.

### D2: Remove truncate_content Import

**Decision**: Remove the `truncate_content` import from `cli.py` as it becomes dead code.

**Rationale**: The non-chunked path is the only user of `truncate_content`. Once removed, the import is unnecessary. The function remains in `slack.py` for potential future use.

### D3: Cap --chunk-size at Slack Limit

**Decision**: If user specifies `--chunk-size` > 39,000 (our default), use 39,000 as maximum.

**Rationale**: Per FR-010, the system must cap chunk-size at Slack's maximum. This prevents users from accidentally creating messages that Slack will reject.

**Implementation**: Add validation in `cli.py` before calling `chunk_content()`:
```python
chunk_size = min(chunk_size, DEFAULT_CHUNK_SIZE)
```

### D4: Test Content Preservation

**Decision**: Add tests that verify the first chunk contains the beginning of the original content and that all content is accounted for across chunks.

**Rationale**: Per the bug investigation (001.md), existing tests only verify the presence of indicators, not that content is preserved. This gap could mask content loss issues.

**Tests to Add**:
1. First chunk starts with beginning of original content
2. All content words present across chunks (accounting for whitespace normalization)
3. Chunk order matches document order

## Files to Modify

| File                    | Action  | Changes                                                        |
| :---------------------- | :------ | :------------------------------------------------------------- |
| `src/md2slack/cli.py`   | MODIFY  | Remove `--chunk`/`-c` flag, remove conditional, cap chunk-size |
| `tests/test_cli.py`     | MODIFY  | Update tests for removed flag, add content preservation tests  |
| `tests/test_chunker.py` | MODIFY  | Add content preservation tests                                 |

## Implementation Notes

### cli.py Changes (Lines 80-85, 145-251)

**Remove:**
```python
@click.option(
    "--chunk",
    "-c",
    is_flag=True,
    help="Enable auto-chunking for long content",
)
```

**Modify:**
- Remove `chunk` parameter from `post()` function signature
- Remove `if chunk:` conditional branch (lines 145-217)
- Remove the entire `else:` branch (lines 218-251) - this is the non-chunked path
- Keep the chunked path logic but make it unconditional
- Remove `truncate_content` from imports (line 18)

**Add:**
```python
# Cap chunk-size at Slack's limit (after validation, before chunk_content)
chunk_size = min(chunk_size, DEFAULT_CHUNK_SIZE)
```

### test_cli.py Changes

**Modify:**
- `test_chunk_flag_in_help`: Change to verify `--chunk` is NOT in help output
- Update all tests that use `--chunk` flag to work without it
- Add test: `test_post_without_chunk_flag_still_works` (documents new behavior)

**Add:**
```python
def test_first_chunk_contains_document_beginning(self, tmp_path, monkeypatch):
    """First chunk must contain the beginning of the original document."""
    ...

def test_all_content_preserved_across_chunks(self, tmp_path, monkeypatch):
    """All content from original document must be present in chunks."""
    ...
```

### test_chunker.py Changes

**Add:**
```python
def test_first_chunk_starts_with_original_content_beginning():
    """First chunk must start with the beginning of the original content."""
    ...

def test_content_reassembly_preserves_all_words():
    """All words from original content must be present when chunks are joined."""
    ...
```
