"""Markdown to Slack mrkdwn converter.

This module provides the core conversion functionality for transforming
standard CommonMark markdown into Slack's mrkdwn format.
"""

from __future__ import annotations

import re

import mistune
from mistune import HTMLRenderer

__all__ = ["convert", "SlackMrkdwnRenderer"]


def _strip_mrkdwn_formatting(text: str) -> str:
    """Strip Slack mrkdwn inline formatting for use in code blocks.

    Removes: backticks, bold asterisks, italic underscores,
    strikethrough tildes, and converts links to plain text.
    """
    # Remove backticks (inline code)
    text = text.replace("`", "")

    # Convert Slack links <url|text> to just text (or url if no text)
    text = re.sub(r"<([^|>]+)\|([^>]+)>", r"\2", text)
    text = re.sub(r"<([^>]+)>", r"\1", text)

    # Remove bold asterisks (but not the content)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)

    # Remove italic underscores (only at word boundaries, not in identifiers)
    text = re.sub(r"(?<![a-zA-Z0-9])_([^_]+)_(?![a-zA-Z0-9])", r"\1", text)

    # Remove strikethrough tildes
    text = re.sub(r"~([^~]+)~", r"\1", text)

    return text


class SlackMrkdwnRenderer(HTMLRenderer):
    """Custom renderer for converting Markdown to Slack's mrkdwn format."""

    NAME = "slack"

    def __init__(self) -> None:
        super().__init__(escape=False)
        self._list_depth = 0
        self._ordered_list_counter = 0
        self._in_ordered_list = False

    # T018: text() - escape &, <, > characters
    def text(self, text: str) -> str:
        """Render plain text, escaping Slack control characters."""
        return (
            text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )

    # T019: heading() - convert to bold format
    def heading(self, text: str, level: int, **attrs) -> str:
        """Render heading as bold text."""
        return f"*{text}*\n\n"

    # T020: strong() - **text** -> *text*
    def strong(self, text: str) -> str:
        """Render bold text with Slack single asterisk."""
        return f"*{text}*"

    # T021: emphasis() - *text* -> _text_
    def emphasis(self, text: str) -> str:
        """Render italic text with Slack underscore."""
        return f"_{text}_"

    # T022: strikethrough() - ~~text~~ -> ~text~
    def strikethrough(self, text: str) -> str:
        """Render strikethrough with Slack single tilde."""
        return f"~{text}~"

    # T023: link() - [text](url) -> <url|text>
    def link(self, text: str, url: str, title: str | None = None) -> str:
        """Render link in Slack format."""
        if text and text != url:
            return f"<{url}|{text}>"
        return f"<{url}>"

    # T024: list() and list_item() - unordered with bullet
    def list(self, text: str, ordered: bool, **attrs) -> str:
        """Render a list."""
        self._in_ordered_list = ordered
        if ordered:
            self._ordered_list_counter = 0
        return f"{text}\n"

    def list_item(self, text: str, **attrs) -> str:
        """Render a list item with bullet or number."""
        text = text.strip()
        if self._in_ordered_list:
            # T025: ordered lists preserve numbering
            self._ordered_list_counter += 1
            return f"{self._ordered_list_counter}. {text}\n"
        else:
            # Unordered list with bullet character
            return f"\u2022 {text}\n"

    # T026: paragraph() - add double newline
    def paragraph(self, text: str) -> str:
        """Render paragraph with trailing newlines."""
        return f"{text}\n\n"

    # T027: codespan() - passthrough backticks
    def codespan(self, text: str) -> str:
        """Render inline code with backticks."""
        return f"`{text}`"

    # T028: block_code() - preserve code blocks
    def block_code(self, code: str, info: str | None = None) -> str:
        """Render code block with triple backticks."""
        return f"```\n{code.rstrip()}\n```\n\n"

    # T029: block_quote() - > prefix each line
    def block_quote(self, text: str) -> str:
        """Render block quote with > prefix."""
        lines = text.strip().split("\n")
        quoted = "\n".join(f">{line}" for line in lines)
        return f"{quoted}\n\n"

    # T030: linebreak() and softbreak()
    def linebreak(self) -> str:
        """Render hard line break."""
        return "\n"

    def softbreak(self) -> str:
        """Render soft line break as space."""
        return " "

    def thematic_break(self) -> str:
        """Render horizontal rule."""
        return "---\n\n"

    def inline_html(self, html: str) -> str:
        """Pass through inline HTML."""
        return html

    def block_html(self, html: str) -> str:
        """Pass through block HTML."""
        return html

    def image(self, alt: str, url: str, title: str | None = None) -> str:
        """Render image as link (Slack doesn't support inline images)."""
        return f"<{url}|{alt or 'image'}>"

    # T046-T047: Table rendering methods
    def table(self, text: str) -> str:
        """Render table as code block with box-drawing characters.

        The text parameter contains the pre-rendered table content from
        table_head and table_body methods.
        """
        from md2slack.tables import (
            Table,
            TableCell,
            TableRow,
            render_table,
        )

        # Parse the pre-rendered content to extract cells
        # Format: HEADER:cell1\x00cell2\n for header, ROW:cell1\x00cell2\n for data
        rows_data = []
        header_data = []

        for line in text.strip().split("\n"):
            if not line:
                continue
            if line.startswith("HEADER:"):
                cells = line[7:].split("\x00")
                header_data = [
                    TableCell(_strip_mrkdwn_formatting(c.strip()), is_header=True)
                    for c in cells
                    if c.strip()
                ]
            elif line.startswith("ROW:"):
                cells = line[4:].split("\x00")
                rows_data.append(
                    TableRow(
                        [
                            TableCell(_strip_mrkdwn_formatting(c.strip()))
                            for c in cells
                            if c.strip()
                        ]
                    )
                )

        if not header_data:
            # Fallback: just return as-is in code block
            return f"```\n{text}\n```\n\n"

        table = Table(headers=TableRow(header_data), rows=rows_data)
        rendered = render_table(table)
        return f"```\n{rendered}\n```\n\n"

    def table_head(self, text: str) -> str:
        """Render table header section.

        Cells come directly here (not through table_row for headers).
        """
        # The text contains cells with \x00 delimiter
        return f"HEADER:{text}\n"

    def table_body(self, text: str) -> str:
        """Render table body section."""
        return text

    def table_row(self, text: str, **attrs) -> str:
        """Render a table row."""
        return f"ROW:{text}\n"

    def table_cell(self, text: str, **attrs) -> str:
        """Render a table cell."""
        # Use null byte as delimiter (won't appear in normal text)
        return f"{text}\x00"


def convert(markdown: str) -> str:
    """Convert markdown to Slack mrkdwn format.

    Args:
        markdown: The markdown string to convert.

    Returns:
        The converted Slack mrkdwn string.
    """
    md = mistune.create_markdown(
        renderer=SlackMrkdwnRenderer(),
        plugins=["strikethrough", "table"],
    )
    return md(markdown)
