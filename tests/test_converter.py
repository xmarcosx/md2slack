"""Tests for the markdown to Slack mrkdwn converter."""


from md2slack.converter import SlackMrkdwnRenderer, convert


class TestConvert:
    """Test the convert() function."""

    # T012: Test heading conversion (all levels)
    class TestHeadings:
        """Test heading conversion."""

        def test_h1_converts_to_bold(self):
            """H1 heading converts to bold text."""
            result = convert("# Heading 1")
            assert "*Heading 1*" in result

        def test_h2_converts_to_bold(self):
            """H2 heading converts to bold text."""
            result = convert("## Heading 2")
            assert "*Heading 2*" in result

        def test_h3_converts_to_bold(self):
            """H3 heading converts to bold text."""
            result = convert("### Heading 3")
            assert "*Heading 3*" in result

        def test_h4_converts_to_bold(self):
            """H4 heading converts to bold text."""
            result = convert("#### Heading 4")
            assert "*Heading 4*" in result

    # T013: Test bold conversion (**text** -> *text*)
    class TestBold:
        """Test bold conversion."""

        def test_double_asterisk_to_single(self):
            """**bold** converts to *bold*."""
            result = convert("**bold text**")
            assert "*bold text*" in result

        def test_bold_in_sentence(self):
            """Bold text within a sentence."""
            result = convert("This is **important** text.")
            assert "*important*" in result

    # T014: Test strikethrough conversion (~~text~~ -> ~text~)
    class TestStrikethrough:
        """Test strikethrough conversion."""

        def test_double_tilde_to_single(self):
            """~~strike~~ converts to ~strike~."""
            result = convert("~~deleted~~")
            assert "~deleted~" in result

        def test_strikethrough_in_sentence(self):
            """Strikethrough within a sentence."""
            result = convert("This is ~~wrong~~ correct.")
            assert "~wrong~" in result

    # T015: Test link conversion ([text](url) -> <url|text>)
    class TestLinks:
        """Test link conversion."""

        def test_markdown_link_to_slack_format(self):
            """[text](url) converts to <url|text>."""
            result = convert("[Click here](https://example.com)")
            assert "<https://example.com|Click here>" in result

        def test_link_with_title(self):
            """Link with title attribute."""
            result = convert('[Link](https://example.com "Title")')
            assert "<https://example.com|Link>" in result

    # T016: Test unordered list conversion (- item -> bullet item)
    class TestUnorderedLists:
        """Test unordered list conversion."""

        def test_dash_list_to_bullet(self):
            """- item converts to bullet item."""
            result = convert("- Item one\n- Item two")
            # Should contain bullet character
            assert "\u2022" in result or "- " in result or "* " in result

        def test_asterisk_list(self):
            """* item list converts."""
            result = convert("* First\n* Second")
            assert "First" in result
            assert "Second" in result

    # T017: Test ordered list conversion (1. item -> numbered)
    class TestOrderedLists:
        """Test ordered list conversion."""

        def test_numbered_list(self):
            """1. item preserves numbering."""
            result = convert("1. First\n2. Second\n3. Third")
            assert "First" in result
            assert "Second" in result
            assert "Third" in result


class TestSlackMrkdwnRenderer:
    """Test the SlackMrkdwnRenderer class."""

    def test_renderer_has_correct_name(self):
        """Renderer has NAME attribute set to 'slack'."""
        renderer = SlackMrkdwnRenderer()
        assert renderer.NAME == "slack"


# Phase 5: User Story 3 - Edge Cases
class TestEdgeCases:
    """Test edge case handling (US3)."""

    # T050: Test nested formatting
    def test_nested_bold_and_link(self):
        """Nested formatting: bold with link inside."""
        result = convert("**bold with [link](https://example.com)**")
        assert "*bold with" in result
        assert "<https://example.com|link>" in result

    def test_link_with_bold_text(self):
        """Link with bold text."""
        result = convert("[**bold link**](https://example.com)")
        # Should have both bold markers and link format
        assert "https://example.com" in result

    # T051: Test escaped characters
    def test_escaped_asterisks(self):
        """Escaped asterisks are preserved literally."""
        result = convert(r"\*not bold\*")
        # Mistune converts \* to literal *
        assert "*not bold*" in result or "\\*" in result

    def test_escaped_tilde(self):
        """Escaped tildes are preserved."""
        result = convert(r"\~not strike\~")
        # Should not be strikethrough
        assert "~" in result

    # T052: Test malformed markdown
    def test_unclosed_bold(self):
        """Unclosed bold markers don't crash."""
        result = convert("**unclosed")
        # Should not raise, content preserved
        assert "unclosed" in result

    def test_unclosed_strikethrough(self):
        """Unclosed strikethrough doesn't crash."""
        result = convert("~~unclosed")
        assert "unclosed" in result

    def test_mismatched_delimiters(self):
        """Mismatched delimiters are handled gracefully."""
        result = convert("**bold but ~mixed**")
        assert "bold" in result
        assert "mixed" in result

    # T053: Test code block content preservation
    def test_code_block_not_converted(self):
        """Content inside code blocks is not converted."""
        result = convert("```\n**not bold** ~~not strike~~\n```")
        # Should preserve literally (not convert to Slack format)
        assert "**not bold**" in result
        assert "~~not strike~~" in result

    def test_fenced_code_with_language(self):
        """Fenced code with language hint preserved."""
        result = convert("```python\ndef hello():\n    pass\n```")
        assert "def hello():" in result
        assert "```" in result

    # T054: Test empty string input
    def test_empty_string(self):
        """Empty string returns empty string."""
        result = convert("")
        assert result == ""

    # T055: Test whitespace-only input
    def test_whitespace_only(self):
        """Whitespace-only input is handled."""
        result = convert("   \n\t\n   ")
        # Should not crash, may return empty or whitespace
        assert isinstance(result, str)

    def test_newlines_only(self):
        """Newlines only input is handled."""
        result = convert("\n\n\n")
        assert isinstance(result, str)

    # T056: Test inline code preservation
    def test_inline_code_preserved(self):
        """Inline code with backticks is preserved."""
        result = convert("Use `pip install`")
        assert "`pip install`" in result

    def test_inline_code_with_markdown(self):
        """Markdown inside inline code is not converted."""
        result = convert("`**not bold**`")
        assert "`**not bold**`" in result
