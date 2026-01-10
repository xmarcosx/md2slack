"""Content chunking for Slack message length limits.

This module provides intelligent content splitting for messages that exceed
Slack's 40,000 character limit. It splits at natural boundaries (paragraphs,
sentences) while preserving code blocks and tables intact.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["Chunk", "ChunkResult", "chunk_content"]

# Slack silently splits messages over ~4046 characters server-side.
# Use 3900 as default to leave buffer for continuation indicators.
# See: https://github.com/slackapi/java-slack-sdk/issues/704
DEFAULT_CHUNK_SIZE = 3900
MIN_CHUNK_SIZE = 500


@dataclass
class Chunk:
    """A segment of content that fits within Slack's message limit.

    Attributes:
        content: The text content of this chunk
        index: 0-based position in the sequence
        total: Total number of chunks in the sequence
        split_type: How this chunk was split: "paragraph", "sentence", "hard", or "none"
    """

    content: str
    index: int
    total: int
    split_type: str

    @property
    def indicator(self) -> str:
        """Return the continuation indicator in (N/M) format."""
        return f"({self.index + 1}/{self.total})"

    @property
    def with_indicator(self) -> str:
        """Return content with continuation indicator appended.

        Only adds indicator if there are multiple chunks.
        """
        if self.total <= 1:
            return self.content
        return f"{self.content}\n{self.indicator}"


@dataclass
class ChunkResult:
    """Result of the chunking operation.

    Attributes:
        chunks: Ordered list of content chunks
        warnings: Warning messages (e.g., oversized blocks)
        original_length: Length of input content
    """

    chunks: list[Chunk]
    warnings: list[str]
    original_length: int

    @property
    def chunk_count(self) -> int:
        """Return the number of chunks produced."""
        return len(self.chunks)


def chunk_content(content: str, max_size: int = DEFAULT_CHUNK_SIZE) -> ChunkResult:
    """Split content into chunks that fit within the size limit.

    Args:
        content: The mrkdwn content to split
        max_size: Maximum characters per chunk (default: 39000)

    Returns:
        ChunkResult containing the chunks and any warnings
    """
    if max_size < MIN_CHUNK_SIZE:
        max_size = MIN_CHUNK_SIZE

    original_length = len(content)
    warnings: list[str] = []

    # If content fits in one chunk, return as-is
    if len(content) <= max_size:
        return ChunkResult(
            chunks=[Chunk(content=content, index=0, total=1, split_type="none")],
            warnings=warnings,
            original_length=original_length,
        )

    # Find all code block boundaries
    code_block_ranges = find_code_block_boundaries(content)

    # Check for oversized code blocks
    for start, end in code_block_ranges:
        block_size = end - start
        if block_size > max_size:
            # Find line number for warning
            line_num = content[:start].count("\n") + 1
            warnings.append(
                f"Code block at line {line_num} exceeds chunk size "
                f"({block_size:,} chars). Block will be posted as-is; "
                "Slack may truncate."
            )

    chunks: list[Chunk] = []
    remaining = content
    position = 0

    while remaining:
        if len(remaining) <= max_size:
            # Last chunk - fits entirely
            chunks.append(
                Chunk(
                    content=remaining,
                    index=len(chunks),
                    total=0,  # Will be updated
                    split_type="none" if len(chunks) == 0 else "end",
                )
            )
            break

        # Find the best split point
        split_pos, split_type = find_best_split_point(
            remaining, max_size, code_block_ranges, position
        )

        # Create chunk from content up to split point
        chunk_content_str = remaining[:split_pos].rstrip()
        if chunk_content_str:  # Skip empty chunks
            chunks.append(
                Chunk(
                    content=chunk_content_str,
                    index=len(chunks),
                    total=0,  # Will be updated
                    split_type=split_type,
                )
            )

        # Move to remaining content
        remaining = remaining[split_pos:].lstrip()
        position += split_pos

    # Update total count in all chunks
    total = len(chunks)
    for chunk in chunks:
        chunk.total = total

    # Filter out empty chunks
    chunks = [c for c in chunks if c.content.strip()]

    # Re-index after filtering
    for i, chunk in enumerate(chunks):
        chunk.index = i
        chunk.total = len(chunks)

    return ChunkResult(
        chunks=chunks,
        warnings=warnings,
        original_length=original_length,
    )


def find_code_block_boundaries(content: str) -> list[tuple[int, int]]:
    """Find all code block start/end positions in the content.

    Code blocks are delimited by triple backticks (```) on their own lines.

    Args:
        content: The content to scan

    Returns:
        List of (start, end) tuples for each code block
    """
    boundaries: list[tuple[int, int]] = []
    in_block = False
    block_start = 0

    lines = content.split("\n")
    pos = 0

    for line in lines:
        line_stripped = line.strip()
        if line_stripped.startswith("```"):
            if not in_block:
                # Starting a code block
                in_block = True
                block_start = pos
            else:
                # Ending a code block
                in_block = False
                block_end = pos + len(line)
                boundaries.append((block_start, block_end))

        pos += len(line) + 1  # +1 for newline

    # Handle unclosed code block
    if in_block:
        boundaries.append((block_start, len(content)))

    return boundaries


def is_inside_code_block(
    position: int, code_block_ranges: list[tuple[int, int]]
) -> bool:
    """Check if a position is inside a code block.

    Args:
        position: Character position to check
        code_block_ranges: List of (start, end) tuples for code blocks

    Returns:
        True if position is inside a code block
    """
    for start, end in code_block_ranges:
        if start <= position < end:
            return True
    return False


def find_paragraph_boundary(
    content: str, max_pos: int, code_block_ranges: list[tuple[int, int]], offset: int
) -> int | None:
    """Find the last paragraph boundary (\\n\\n) before max_pos.

    Only considers boundaries that are not inside code blocks.
    Prefers boundaries in the last 50% of the search range but will search
    further back if needed to find a valid split point.

    Args:
        content: Content to search
        max_pos: Maximum position to search up to
        code_block_ranges: Code block ranges to avoid
        offset: Offset of content in original document

    Returns:
        Position after the paragraph boundary (for splitting), or None if not found
    """
    # Search the entire range for \n\n, starting from the end
    pos = content.rfind("\n\n", 0, max_pos)

    while pos >= 0:
        # Check if this position is inside a code block
        if not is_inside_code_block(pos + offset, code_block_ranges):
            return pos + 2  # Split after the newlines
        # Keep searching backward
        pos = content.rfind("\n\n", 0, pos)

    return None


def find_sentence_boundary(
    content: str, max_pos: int, code_block_ranges: list[tuple[int, int]], offset: int
) -> int | None:
    """Find the last sentence boundary before max_pos.

    Sentence boundaries are: ". ", "! ", "? "
    Only considers boundaries that are not inside code blocks.

    Args:
        content: Content to search
        max_pos: Maximum position to search up to
        code_block_ranges: Code block ranges to avoid
        offset: Offset of content in original document

    Returns:
        Position after the sentence boundary, or None if not found
    """
    # Find best sentence ending in the entire range
    best_pos = None

    for ending in [". ", "! ", "? "]:
        pos = content.rfind(ending, 0, max_pos)
        while pos >= 0:
            if not is_inside_code_block(pos + offset, code_block_ranges):
                if best_pos is None or pos > best_pos:
                    best_pos = pos + 2  # Split after the ending
                break
            # Keep searching backward
            pos = content.rfind(ending, 0, pos)

    return best_pos


def find_best_split_point(
    content: str,
    max_size: int,
    code_block_ranges: list[tuple[int, int]],
    offset: int,
) -> tuple[int, str]:
    """Find the best position to split content.

    Priority:
    1. Paragraph boundary (\\n\\n)
    2. Sentence boundary (. ! ?)
    3. Hard split at max_size

    Args:
        content: Content to split
        max_size: Maximum chunk size
        code_block_ranges: Code block ranges to avoid splitting
        offset: Offset of content in original document

    Returns:
        Tuple of (split_position, split_type)
    """
    # Try paragraph boundary first
    para_pos = find_paragraph_boundary(content, max_size, code_block_ranges, offset)
    if para_pos is not None and para_pos > 0:
        return para_pos, "paragraph"

    # Try sentence boundary
    sent_pos = find_sentence_boundary(content, max_size, code_block_ranges, offset)
    if sent_pos is not None and sent_pos > 0:
        return sent_pos, "sentence"

    # Last resort: hard split
    # Try to avoid splitting inside a code block
    split_pos = max_size

    # If we're about to split inside a code block, try to find the block start
    if is_inside_code_block(split_pos + offset, code_block_ranges):
        # Find which block we're in and split before it
        for start, end in code_block_ranges:
            if start <= split_pos + offset < end:
                # Split just before the code block if possible
                if start - offset > MIN_CHUNK_SIZE // 2:
                    return start - offset, "hard"
                # Otherwise we have to split inside (oversized block case)
                break

    return split_pos, "hard"
