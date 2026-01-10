"""Shared pytest fixtures for md2slack tests.

This module provides fixtures for:
- markdown_samples: Dictionary of sample markdown patterns for conversion testing
- markdown_file: Temporary markdown file for file-based input testing
"""

from pathlib import Path

import pytest


@pytest.fixture
def markdown_samples():
    """Provide sample markdown strings for conversion testing.

    Returns a dictionary mapping element types to markdown examples.

    Available keys:
        - heading: H1 heading (# Hello World)
        - bold: Bold text (**bold**)
        - italic: Italic text (*italic*)
        - link: Markdown link ([text](url))
        - list: Bullet list (- items)
        - code_inline: Inline code (`code`)
        - code_block: Fenced code block (```...```)
        - table: Markdown table (| A | B |)

    Example:
        def test_heading(markdown_samples):
            heading = markdown_samples["heading"]
            result = convert(heading)
            assert "*Hello World*" in result
    """
    return {
        "heading": "# Hello World",
        "bold": "This is **bold** text",
        "italic": "This is *italic* text",
        "link": "[Click here](https://example.com)",
        "list": "- Item 1\n- Item 2\n- Item 3",
        "code_inline": "Use `code` here",
        "code_block": "```python\nprint('hello')\n```",
        "table": "| A | B |\n|---|---|\n| 1 | 2 |",
    }


@pytest.fixture
def markdown_file(tmp_path: Path) -> Path:
    """Create a temporary markdown file for file-based input testing.

    Uses pytest's built-in tmp_path fixture for automatic cleanup.
    The file is created with sample heading content.

    Args:
        tmp_path: Pytest fixture providing a temporary directory unique to each test.

    Returns:
        Path to the created markdown file.

    Note:
        The temporary file is automatically cleaned up after the test completes.
        Each test invocation gets an isolated temporary directory.

    Example:
        def test_file_input(markdown_file):
            content = markdown_file.read_text()
            assert "# Sample Heading" in content

        def test_custom_content(tmp_path):
            # For custom content, use tmp_path directly
            md_file = tmp_path / "custom.md"
            md_file.write_text("# Custom Content")
    """
    md_file = tmp_path / "test.md"
    md_file.write_text("# Sample Heading\n\nThis is sample content.")
    return md_file
