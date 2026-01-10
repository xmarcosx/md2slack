# Research: Default Chunking Implementation

**Feature**: 007-default-chunking
**Date**: 2026-01-10

## Research Questions

### RQ1: Does the chunker already handle short content correctly?

**Finding**: Yes, the chunker handles short content gracefully.

**Evidence** (from `chunker.py:87-93`):
```python
# If content fits in one chunk, return as-is
if len(content) <= max_size:
    return ChunkResult(
        chunks=[Chunk(content=content, index=0, total=1, split_type="none")],
        warnings=warnings,
        original_length=original_length,
    )
```

**Behavior**:
- Content under `max_size` (default 39,000) returns a single chunk with `total=1`
- The `with_indicator` property returns plain content when `total <= 1` (no indicator added)
- Confirmed by test `test_chunk_with_indicator_single_chunk` in `test_chunker.py:45-47`

**Conclusion**: Always using the chunked path will produce identical behavior for short content as the current non-chunked path.

---

### RQ2: What happens to the truncation warning in the non-chunked path?

**Finding**: The truncation warning is no longer needed.

**Current behavior** (from `cli.py:220-225`):
```python
mrkdwn, was_truncated = truncate_content(mrkdwn)
if was_truncated:
    click.echo(
        "Warning: Content exceeds Slack's 40,000 character limit. Truncating.",
        err=True,
    )
```

**With default chunking**:
- Long content will be split into chunks instead of truncated
- All content is preserved (no warning needed)
- The chunker already provides warnings for oversized code blocks that can't be split

**Conclusion**: Remove truncation path entirely. Content preservation is the goal; truncation works against it.

---

### RQ3: What tests will break when --chunk flag is removed?

**Finding**: Several tests in `test_cli.py` explicitly use `--chunk` flag.

**Affected tests**:
| Test Name                          | Current Behavior                    | Required Change               |
| :--------------------------------- | :---------------------------------- | :---------------------------- |
| `test_chunk_flag_in_help`          | Asserts `--chunk` is in help output | Assert `--chunk` is NOT there |
| `test_chunk_size_validation`       | Uses `--chunk` with `--chunk-size`  | Remove `--chunk` flag usage   |
| `test_chunk_dry_run_short_content` | Uses `--chunk` flag                 | Remove `--chunk` flag usage   |
| `test_chunk_dry_run_long_content`  | Uses `--chunk` flag                 | Remove `--chunk` flag usage   |
| `test_chunk_posts_multiple_messages` | Uses `--chunk` flag              | Remove `--chunk` flag usage   |
| `test_chunk_progress_output`       | Uses `--chunk` flag                 | Remove `--chunk` flag usage   |
| `test_chunk_completion_summary`    | Uses `--chunk` flag                 | Remove `--chunk` flag usage   |
| `test_chunk_error_mid_posting`     | Uses `--chunk` flag                 | Remove `--chunk` flag usage   |
| `test_chunk_single_message_no_indicator` | Uses `--chunk` flag            | Remove `--chunk` flag usage   |

**Conclusion**: All tests using `--chunk` need modification. The behavior they test remains valid; only the flag usage changes.

---

### RQ4: What is Slack's actual message limit?

**Finding**: Slack's message limit is 40,000 characters for `chat.postMessage`.

**Evidence**:
- Error mapping in `slack.py:68-71` references 40,000
- `MAX_MESSAGE_LENGTH` constant is 39,900 (leaves buffer)
- `DEFAULT_CHUNK_SIZE` is 39,000 (leaves buffer for indicator)

**Implication**: The 39,000 default chunk size is appropriate. It leaves 1,000 characters of headroom for chunk indicators (~15 chars) and potential API overhead.

**Conclusion**: Keep `DEFAULT_CHUNK_SIZE = 39000` as the maximum allowed value for `--chunk-size`.

---

### RQ5: Should we show a warning when capping user-provided --chunk-size?

**Finding**: A warning would be user-friendly but is not strictly necessary.

**Options**:
1. Silent cap: `chunk_size = min(chunk_size, DEFAULT_CHUNK_SIZE)` - simple, no noise
2. Warning cap: Show warning when user value exceeds limit - transparent but verbose

**Recommendation**: Option 1 (silent cap). Users specifying large chunk sizes probably want "don't split unnecessarily," which capping achieves. A warning adds noise for a non-error condition.

**Conclusion**: Silently cap `--chunk-size` at `DEFAULT_CHUNK_SIZE`.

---

## Best Practices Applied

### Click CLI Flag Removal

**Best practice**: When removing a flag, update docstrings and examples.

**Applied to** `cli.py:post()`:
- Update docstring to remove `--chunk` example
- Keep `--chunk-size` documentation (still valid)
- Update Examples section to show simpler usage

### Test Migration for Removed Features

**Best practice**: Don't delete tests for behavior that still exists; update them.

**Applied to** `test_cli.py`:
- `test_chunk_flag_in_help` → `test_chunk_flag_not_in_help`
- Other chunk tests → Remove flag, verify same behavior works by default

---

## Decisions Made

| Decision                           | Choice                          | Rationale                                       |
| :--------------------------------- | :------------------------------ | :---------------------------------------------- |
| Always use chunked path            | Yes                             | Chunker handles all cases correctly             |
| Remove truncate_content usage      | Yes                             | Content preservation > truncation               |
| Cap chunk-size silently            | Yes                             | Reduces noise, achieves user intent             |
| Keep truncate_content in slack.py  | Yes                             | Future-proofing, minimal change                 |
| Add content preservation tests     | Yes                             | Close gap identified in bug 001                 |
