"""Table rendering with Unicode box-drawing characters.

This module provides data structures and functions for rendering markdown
tables as monospace code blocks using Unicode box-drawing characters.
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from typing import Literal

__all__ = [
    "BoxChars",
    "LIGHT_BOX",
    "TableCell",
    "TableRow",
    "Table",
    "render_table",
    "wrap_cell",
]


@dataclass(frozen=True)
class BoxChars:
    """Unicode box-drawing character set."""

    horizontal: str = "\u2500"  # ─
    vertical: str = "\u2502"  # │
    top_left: str = "\u250c"  # ┌
    top_right: str = "\u2510"  # ┐
    bottom_left: str = "\u2514"  # └
    bottom_right: str = "\u2518"  # ┘
    left_t: str = "\u251c"  # ├
    right_t: str = "\u2524"  # ┤
    top_t: str = "\u252c"  # ┬
    bottom_t: str = "\u2534"  # ┴
    cross: str = "\u253c"  # ┼


# Default character set using light lines
LIGHT_BOX = BoxChars()


# T039: TableCell dataclass
@dataclass
class TableCell:
    """A single cell in a table."""

    content: str
    alignment: Literal["left", "center", "right"] | None = None
    is_header: bool = False

    @property
    def lines(self) -> list[str]:
        """Split content into lines for multi-line cell rendering."""
        return self.content.split("\n")

    @property
    def width(self) -> int:
        """Maximum line width in the cell."""
        return max((len(line) for line in self.lines), default=0)


# T040: TableRow dataclass
@dataclass
class TableRow:
    """A row of cells in a table."""

    cells: list[TableCell]

    @property
    def height(self) -> int:
        """Number of lines in the tallest cell."""
        return max((len(cell.lines) for cell in self.cells), default=1)


# T041: Table dataclass
@dataclass
class Table:
    """Parsed table structure for rendering."""

    headers: TableRow
    rows: list[TableRow] = field(default_factory=list)

    @property
    def column_count(self) -> int:
        """Number of columns in the table."""
        return len(self.headers.cells)

    def column_widths(self) -> list[int]:
        """Calculate width of each column based on content."""
        widths = [cell.width for cell in self.headers.cells]
        for row in self.rows:
            for i, cell in enumerate(row.cells):
                if i < len(widths):
                    widths[i] = max(widths[i], cell.width)
        return widths


# T045: wrap_cell function
def wrap_cell(content: str, width: int) -> list[str]:
    """Wrap text within a cell to fit specified width.

    Args:
        content: The cell content to wrap.
        width: Maximum width for each line.

    Returns:
        List of lines after wrapping.
    """
    if not content:
        return [""]
    if width <= 0:
        return [content]
    return textwrap.wrap(content, width=width) or [""]


# T042: render_row_line helper
def _render_row_line(
    cells: list[str],
    widths: list[int],
    box: BoxChars = LIGHT_BOX,
) -> str:
    """Render a single line of a row with vertical bars.

    Args:
        cells: Cell contents for this line.
        widths: Column widths.
        box: Box-drawing character set.

    Returns:
        Rendered line string.
    """
    parts = []
    for cell, width in zip(cells, widths):
        parts.append(f" {cell.ljust(width)} ")
    return box.vertical + box.vertical.join(parts) + box.vertical


# T043: render_separator helper
def _render_separator(
    widths: list[int],
    left: str,
    mid: str,
    right: str,
    box: BoxChars = LIGHT_BOX,
) -> str:
    """Render a horizontal separator line.

    Args:
        widths: Column widths.
        left: Left corner/junction character.
        mid: Middle junction character.
        right: Right corner/junction character.
        box: Box-drawing character set.

    Returns:
        Rendered separator string.
    """
    segments = [box.horizontal * (width + 2) for width in widths]
    return left + mid.join(segments) + right


# T044: render_table function
def render_table(table: Table, box: BoxChars = LIGHT_BOX) -> str:
    """Render a table with box-drawing characters.

    Args:
        table: The table to render.
        box: Box-drawing character set to use.

    Returns:
        Rendered table as a string.
    """
    widths = table.column_widths()
    lines: list[str] = []

    # Top border
    lines.append(_render_separator(widths, box.top_left, box.top_t, box.top_right, box))

    # Header row
    header_contents = [cell.content for cell in table.headers.cells]
    lines.append(_render_row_line(header_contents, widths, box))

    # Header separator
    lines.append(_render_separator(widths, box.left_t, box.cross, box.right_t, box))

    # Data rows
    for row in table.rows:
        row_contents = [cell.content for cell in row.cells]
        # Pad with empty strings if row has fewer cells
        while len(row_contents) < len(widths):
            row_contents.append("")
        lines.append(_render_row_line(row_contents, widths, box))

    # Bottom border
    lines.append(
        _render_separator(widths, box.bottom_left, box.bottom_t, box.bottom_right, box)
    )

    return "\n".join(lines)
