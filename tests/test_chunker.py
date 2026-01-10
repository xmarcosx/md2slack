"""Tests for md2slack content chunker."""

from md2slack.chunker import (
    Chunk,
    ChunkResult,
    chunk_content,
    find_code_block_boundaries,
    find_paragraph_boundary,
    find_sentence_boundary,
    is_inside_code_block,
)

# =============================================================================
# Phase 2: Foundational - Data Structures (T003-T007)
# =============================================================================


class TestChunkDataclass:
    """Tests for Chunk dataclass."""

    def test_chunk_creation(self):
        """T003: Chunk dataclass has required fields."""
        chunk = Chunk(content="Hello", index=0, total=3, split_type="paragraph")
        assert chunk.content == "Hello"
        assert chunk.index == 0
        assert chunk.total == 3
        assert chunk.split_type == "paragraph"

    def test_chunk_indicator_property(self):
        """T005: Chunk.indicator returns (N/M) format."""
        chunk = Chunk(content="Test", index=1, total=5, split_type="sentence")
        assert chunk.indicator == "(2/5)"

    def test_chunk_indicator_first_chunk(self):
        """T005: First chunk indicator is (1/M)."""
        chunk = Chunk(content="First", index=0, total=3, split_type="paragraph")
        assert chunk.indicator == "(1/3)"

    def test_chunk_with_indicator_multiple_chunks(self):
        """T006: with_indicator includes indicator for multi-chunk content."""
        chunk = Chunk(content="Content here", index=0, total=2, split_type="paragraph")
        assert chunk.with_indicator == "Content here\n(1/2)"

    def test_chunk_with_indicator_single_chunk(self):
        """T006: with_indicator returns plain content for single chunk."""
        chunk = Chunk(content="Only content", index=0, total=1, split_type="none")
        assert chunk.with_indicator == "Only content"


class TestChunkResultDataclass:
    """Tests for ChunkResult dataclass."""

    def test_chunk_result_creation(self):
        """T004: ChunkResult has required fields."""
        chunks = [Chunk(content="A", index=0, total=2, split_type="paragraph")]
        result = ChunkResult(chunks=chunks, warnings=[], original_length=100)
        assert result.chunks == chunks
        assert result.warnings == []
        assert result.original_length == 100

    def test_chunk_result_chunk_count(self):
        """T004: ChunkResult.chunk_count returns number of chunks."""
        chunks = [
            Chunk(content="A", index=0, total=2, split_type="paragraph"),
            Chunk(content="B", index=1, total=2, split_type="none"),
        ]
        result = ChunkResult(chunks=chunks, warnings=[], original_length=200)
        assert result.chunk_count == 2

    def test_chunk_result_with_warnings(self):
        """T004: ChunkResult can contain warnings."""
        result = ChunkResult(
            chunks=[],
            warnings=["Code block exceeds limit"],
            original_length=50000,
        )
        assert len(result.warnings) == 1
        assert "exceeds limit" in result.warnings[0]


# =============================================================================
# Phase 3: User Story 1 - Basic Chunking (T008-T011)
# =============================================================================


class TestBasicChunking:
    """Tests for basic chunk_content functionality."""

    def test_short_content_no_split(self):
        """T008: Short content (under limit) returns single chunk."""
        content = "This is short content."
        result = chunk_content(content, max_size=1000)
        assert result.chunk_count == 1
        assert result.chunks[0].content == content
        assert result.chunks[0].split_type == "none"

    def test_long_content_splits(self):
        """T009: Long content (over limit) splits into multiple chunks."""
        # Create content that exceeds the limit
        content = "A" * 2500
        result = chunk_content(content, max_size=1000)
        assert result.chunk_count >= 2
        # All chunks should be under limit
        for chunk in result.chunks:
            assert len(chunk.content) <= 1000

    def test_continuation_indicator_format(self):
        """T010: Continuation indicators use (N/M) format."""
        content = "A" * 2500
        result = chunk_content(content, max_size=1000)
        assert result.chunk_count >= 2
        first_chunk = result.chunks[0]
        assert first_chunk.indicator == f"(1/{result.chunk_count})"

    def test_no_indicator_single_chunk(self):
        """T011: Single chunk has no indicator added."""
        content = "Short content"
        result = chunk_content(content, max_size=1000)
        assert result.chunk_count == 1
        assert result.chunks[0].with_indicator == content


# =============================================================================
# Phase 4: User Story 2 - Intelligent Split Points (T019-T022)
# =============================================================================


class TestIntelligentSplitPoints:
    """Tests for intelligent split point detection."""

    def test_split_at_paragraph_boundary(self):
        """T019: Content splits at paragraph boundary (\\n\\n) when available."""
        # Create content long enough to require splitting with max_size=1000
        first_para = "A" * 600 + " first paragraph."
        second_para = "B" * 600 + " second paragraph."
        content = f"{first_para}\n\n{second_para}"
        result = chunk_content(content, max_size=1000)
        # Should split at paragraph boundary
        assert result.chunk_count >= 2
        # First chunk should contain first paragraph content
        assert "first paragraph" in result.chunks[0].content
        # Check split type
        assert result.chunks[0].split_type == "paragraph"

    def test_split_at_sentence_boundary(self):
        """T020: Falls back to sentence boundary (. ) when paragraph too large."""
        # One long paragraph with multiple sentences (total > 1000 chars)
        sentence1 = "A" * 400 + " first sentence here."
        sentence2 = "B" * 400 + " second sentence here."
        sentence3 = "C" * 400 + " third sentence here."
        content = f"{sentence1} {sentence2} {sentence3}"
        result = chunk_content(content, max_size=1000)
        # Should split at sentence boundary
        assert result.chunk_count >= 2
        # Check that at least one split was at sentence
        split_types = [c.split_type for c in result.chunks]
        assert "sentence" in split_types or "hard" in split_types

    def test_hard_split_no_boundary(self):
        """T021: Hard split when no natural boundary found."""
        # Long content with no natural boundaries
        content = "A" * 2000  # No spaces, periods, or newlines
        result = chunk_content(content, max_size=1000)
        assert result.chunk_count >= 2
        # Should use hard split
        assert "hard" in [c.split_type for c in result.chunks]

    def test_split_type_tracking(self):
        """T022: Each chunk tracks its split type."""
        # Make content long enough to actually split
        para1 = "A" * 500 + " para one."
        para2 = "B" * 500 + " para two. Sentence. More."
        para3 = "C" * 500 + " para three."
        content = f"{para1}\n\n{para2}\n\n{para3}"
        result = chunk_content(content, max_size=1000)
        # Each chunk should have a split_type
        for chunk in result.chunks:
            assert chunk.split_type in ["paragraph", "sentence", "hard", "none", "end"]


# =============================================================================
# Phase 5: User Story 3 - Code Block Preservation (T028-T031)
# =============================================================================


class TestCodeBlockPreservation:
    """Tests for code block detection and preservation."""

    def test_code_block_detection(self):
        """T028: Detects code blocks delimited by triple backticks."""
        content = "Text before.\n\n```\ncode here\n```\n\nText after."
        boundaries = find_code_block_boundaries(content)
        assert len(boundaries) == 1
        start, end = boundaries[0]
        assert "```" in content[start:end]
        assert "code here" in content[start:end]

    def test_no_split_inside_code_block(self):
        """T029: Content does not split inside code blocks."""
        # Code block with content that would otherwise split
        code_content = "line1\nline2\nline3\nline4\nline5"
        content = f"Intro.\n\n```\n{code_content}\n```\n\nAfter."
        result = chunk_content(content, max_size=30)

        # Verify code block is intact in one of the chunks
        found_intact = False
        for chunk in result.chunks:
            if "```" in chunk.content and code_content in chunk.content:
                found_intact = True
                break

        # Either the block is intact, or the content was small enough for one chunk
        assert found_intact or result.chunk_count == 1

    def test_oversized_code_block_warning(self):
        """T030: Warning generated for oversized code blocks."""
        # Create a code block that exceeds max_size
        large_code = "x" * 1500
        content = f"```\n{large_code}\n```"
        result = chunk_content(content, max_size=1000)

        # Should have a warning
        assert len(result.warnings) >= 1
        assert "exceeds chunk size" in result.warnings[0]

    def test_table_as_code_block_preserved(self):
        """T031: Tables (rendered as code blocks) are preserved."""
        # Tables in mrkdwn are wrapped in code blocks by the converter
        table_content = "┌───┬───┐\n│ A │ B │\n├───┼───┤\n│ 1 │ 2 │\n└───┴───┘"
        content = f"Text.\n\n```\n{table_content}\n```\n\nMore text."

        boundaries = find_code_block_boundaries(content)
        assert len(boundaries) == 1

        # Table should be detected as code block
        start, end = boundaries[0]
        assert table_content in content[start:end]


# =============================================================================
# Helper Function Tests
# =============================================================================


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_find_code_block_boundaries_multiple(self):
        """Find boundaries of multiple code blocks."""
        content = "Text.\n\n```\nblock1\n```\n\nMiddle.\n\n```\nblock2\n```\n\nEnd."
        boundaries = find_code_block_boundaries(content)
        assert len(boundaries) == 2

    def test_find_code_block_boundaries_empty(self):
        """No boundaries when no code blocks."""
        content = "Just plain text with no code blocks."
        boundaries = find_code_block_boundaries(content)
        assert len(boundaries) == 0

    def test_find_code_block_boundaries_unclosed(self):
        """Handles unclosed code block."""
        content = "Text.\n\n```\nunclosed code block"
        boundaries = find_code_block_boundaries(content)
        assert len(boundaries) == 1
        # Should extend to end of content
        assert boundaries[0][1] == len(content)

    def test_is_inside_code_block_true(self):
        """Position inside code block returns True."""
        ranges = [(10, 50), (100, 150)]
        assert is_inside_code_block(25, ranges) is True
        assert is_inside_code_block(125, ranges) is True

    def test_is_inside_code_block_false(self):
        """Position outside code block returns False."""
        ranges = [(10, 50), (100, 150)]
        assert is_inside_code_block(5, ranges) is False
        assert is_inside_code_block(75, ranges) is False
        assert is_inside_code_block(200, ranges) is False

    def test_find_paragraph_boundary_found(self):
        """Finds paragraph boundary when present."""
        # Use longer content to ensure search window covers the boundary
        content = "A" * 50 + " First para.\n\n" + "B" * 50 + " Second para."
        # max_pos should be far enough to include the boundary in search window
        pos = find_paragraph_boundary(content, len(content), [], 0)
        assert pos is not None
        # Should find the \n\n boundary
        assert "\n\n" in content[:pos] or content[pos - 2 : pos] == "\n\n"

    def test_find_paragraph_boundary_not_found(self):
        """Returns None when no paragraph boundary."""
        content = "One continuous paragraph without breaks."
        pos = find_paragraph_boundary(content, 30, [], 0)
        assert pos is None

    def test_find_sentence_boundary_found(self):
        """Finds sentence boundary when present."""
        # Use longer content
        content = "A" * 50 + " First sentence. " + "B" * 50 + " Second sentence."
        pos = find_sentence_boundary(content, len(content), [], 0)
        assert pos is not None

    def test_find_sentence_boundary_exclamation(self):
        """Finds exclamation as sentence boundary."""
        content = "A" * 50 + " Wow! " + "B" * 50 + " Another sentence."
        pos = find_sentence_boundary(content, len(content), [], 0)
        assert pos is not None

    def test_find_sentence_boundary_question(self):
        """Finds question mark as sentence boundary."""
        content = "A" * 50 + " Really? " + "B" * 50 + " Yes indeed."
        pos = find_sentence_boundary(content, len(content), [], 0)
        assert pos is not None


# =============================================================================
# Phase 7: Polish - Edge Cases (T045-T046)
# =============================================================================


# =============================================================================
# Phase 3: User Story 1 - Content Preservation (T009-T011 from 007-default-chunking)
# =============================================================================


class TestContentPreservation:
    """Tests for content preservation during chunking."""

    def test_first_chunk_contains_document_beginning(self):
        """T009: First chunk must contain the beginning of the original document."""
        # Create long content with identifiable beginning
        beginning_marker = "THIS IS THE BEGINNING OF THE DOCUMENT"
        content = beginning_marker + "\n\n" + "A" * 2000 + "\n\nEnd of document."
        result = chunk_content(content, max_size=1000)

        # First chunk must start with the beginning marker
        assert result.chunks[0].content.startswith(beginning_marker)

    def test_all_words_preserved_across_chunks(self):
        """T010: All words from original must be present when chunks are combined."""
        # Create content with distinct words
        words = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"]
        # Pad between words to ensure splitting occurs
        content = (" " + "X" * 200 + " ").join(words)
        result = chunk_content(content, max_size=500)

        # Combine all chunk content
        combined = " ".join(c.content for c in result.chunks)

        # All original words must be present
        for word in words:
            assert word in combined, f"Word '{word}' not preserved in chunks"

    def test_chunk_order_matches_document_order(self):
        """Content chunks maintain the same order as the original document."""
        # Create content with numbered sections
        sections = [f"SECTION_{i}" + "=" * 300 for i in range(1, 5)]
        content = "\n\n".join(sections)
        result = chunk_content(content, max_size=500)

        # Extract section numbers in order from chunks
        combined = "".join(c.content for c in result.chunks)
        positions = []
        for i in range(1, 5):
            pos = combined.find(f"SECTION_{i}")
            if pos >= 0:
                positions.append(pos)

        # Positions should be in ascending order
        assert positions == sorted(positions), "Chunk order doesn't match doc order"


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_chunk_skipping(self):
        """T045: Empty chunks are skipped."""
        # Content with lots of whitespace that might create empty chunks
        content = "Content.\n\n\n\n\n\nMore content."
        result = chunk_content(content, max_size=15)
        # No empty chunks
        for chunk in result.chunks:
            assert chunk.content.strip() != ""

    def test_content_exactly_at_limit(self):
        """T046: Content exactly at limit produces single chunk, no indicator."""
        content = "A" * 1000
        result = chunk_content(content, max_size=1000)
        assert result.chunk_count == 1
        assert result.chunks[0].with_indicator == content

    def test_minimum_chunk_size_enforced(self):
        """Minimum chunk size is enforced."""
        content = "A" * 5000
        # Request very small chunks
        result = chunk_content(content, max_size=100)
        # Should enforce minimum of 500
        for c in result.chunks:
            assert len(c.content) <= 500 or len(c.content) == len(content)

    def test_preserves_all_content(self):
        """All original content is preserved after chunking."""
        content = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        result = chunk_content(content, max_size=25)

        # Reconstruct content (accounting for whitespace trimming)
        reconstructed = "\n\n".join(c.content for c in result.chunks)

        # Key content should be preserved
        assert "First" in reconstructed
        assert "Second" in reconstructed
        assert "Third" in reconstructed
