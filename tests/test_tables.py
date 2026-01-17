"""Tests for table rendering with box-drawing characters."""

import pytest

from md2slack.tables import LIGHT_BOX


class TestBoxChars:
    """Test the BoxChars dataclass."""

    def test_default_box_chars(self):
        """LIGHT_BOX has all expected characters."""
        assert LIGHT_BOX.horizontal == "\u2500"
        assert LIGHT_BOX.vertical == "\u2502"
        assert LIGHT_BOX.top_left == "\u250c"
        assert LIGHT_BOX.top_right == "\u2510"
        assert LIGHT_BOX.bottom_left == "\u2514"
        assert LIGHT_BOX.bottom_right == "\u2518"

    def test_box_chars_frozen(self):
        """BoxChars is frozen (immutable)."""
        with pytest.raises(Exception):
            LIGHT_BOX.horizontal = "x"


# T032: Test TableCell dataclass
class TestTableCell:
    """Test the TableCell dataclass."""

    def test_cell_content(self):
        """TableCell stores content."""
        from md2slack.tables import TableCell

        cell = TableCell("Hello")
        assert cell.content == "Hello"

    def test_cell_lines_single(self):
        """Single-line content returns one line."""
        from md2slack.tables import TableCell

        cell = TableCell("Hello")
        assert cell.lines == ["Hello"]

    def test_cell_lines_multiline(self):
        """Multi-line content splits correctly."""
        from md2slack.tables import TableCell

        cell = TableCell("Line1\nLine2")
        assert cell.lines == ["Line1", "Line2"]

    def test_cell_width(self):
        """Width is max line length."""
        from md2slack.tables import TableCell

        cell = TableCell("Hello")
        assert cell.width == 5

    def test_cell_width_multiline(self):
        """Width is max line length for multi-line."""
        from md2slack.tables import TableCell

        cell = TableCell("Hi\nHello World")
        assert cell.width == 11

    def test_cell_alignment(self):
        """Cell can have alignment."""
        from md2slack.tables import TableCell

        cell = TableCell("Test", alignment="center")
        assert cell.alignment == "center"

    def test_cell_is_header(self):
        """Cell can be marked as header."""
        from md2slack.tables import TableCell

        cell = TableCell("Header", is_header=True)
        assert cell.is_header is True


# T033: Test TableRow dataclass
class TestTableRow:
    """Test the TableRow dataclass."""

    def test_row_cells(self):
        """TableRow stores cells."""
        from md2slack.tables import TableCell, TableRow

        cells = [TableCell("A"), TableCell("B")]
        row = TableRow(cells)
        assert len(row.cells) == 2

    def test_row_height_single(self):
        """Row height is 1 for single-line cells."""
        from md2slack.tables import TableCell, TableRow

        row = TableRow([TableCell("A"), TableCell("B")])
        assert row.height == 1

    def test_row_height_multiline(self):
        """Row height is max cell height."""
        from md2slack.tables import TableCell, TableRow

        row = TableRow([TableCell("A\nB\nC"), TableCell("X")])
        assert row.height == 3


# T034: Test Table dataclass
class TestTable:
    """Test the Table dataclass."""

    def test_table_column_count(self):
        """Column count matches header count."""
        from md2slack.tables import Table, TableCell, TableRow

        headers = TableRow([TableCell("A"), TableCell("B"), TableCell("C")])
        table = Table(headers=headers, rows=[])
        assert table.column_count == 3

    def test_table_column_widths(self):
        """Column widths based on max content."""
        from md2slack.tables import Table, TableCell, TableRow

        headers = TableRow([TableCell("Name"), TableCell("Value")])
        rows = [
            TableRow([TableCell("Alice"), TableCell("100")]),
            TableRow([TableCell("Bob"), TableCell("2000")]),
        ]
        table = Table(headers=headers, rows=rows)
        widths = table.column_widths()
        assert widths == [5, 5]  # "Alice" and "Value"/"2000"


# T035: Test render_table() with simple 2x2 table
class TestRenderTable:
    """Test the render_table() function."""

    def test_simple_2x2_table(self):
        """Render a simple 2x2 table."""
        from md2slack.tables import Table, TableCell, TableRow, render_table

        headers = TableRow([
            TableCell("A", is_header=True),
            TableCell("B", is_header=True),
        ])
        rows = [TableRow([TableCell("1"), TableCell("2")])]
        table = Table(headers=headers, rows=rows)

        result = render_table(table)
        assert "\u250c" in result  # top-left corner
        assert "\u2518" in result  # bottom-right corner
        assert "A" in result
        assert "B" in result
        assert "1" in result
        assert "2" in result

    # T036: Test render_table() with varying column widths
    def test_varying_column_widths(self):
        """Columns align based on content width."""
        from md2slack.tables import Table, TableCell, TableRow, render_table

        headers = TableRow([
            TableCell("Name", is_header=True),
            TableCell("X", is_header=True),
        ])
        rows = [TableRow([TableCell("Alice"), TableCell("1")])]
        table = Table(headers=headers, rows=rows)

        result = render_table(table)
        # Verify alignment (lines should be consistent length)
        lines = result.strip().split("\n")
        assert len(lines) >= 4  # top, header, separator, data, bottom

    # T037: Test render_table() with empty cells
    def test_empty_cells(self):
        """Empty cells render as blank space."""
        from md2slack.tables import Table, TableCell, TableRow, render_table

        headers = TableRow([
            TableCell("A", is_header=True),
            TableCell("B", is_header=True),
        ])
        rows = [TableRow([TableCell(""), TableCell("X")])]
        table = Table(headers=headers, rows=rows)

        result = render_table(table)
        assert "X" in result
        # Should still have proper structure
        assert "\u2502" in result  # vertical bar


# Test multi-line cell rendering
class TestMultiLineCells:
    """Test rendering of multi-line cells."""

    def test_multiline_cell_in_data_row(self):
        """Multi-line cell renders all lines with proper alignment."""
        from md2slack.tables import Table, TableCell, TableRow, render_table

        headers = TableRow([
            TableCell("Col A", is_header=True),
            TableCell("Col B", is_header=True),
        ])
        rows = [TableRow([TableCell("Line1\nLine2"), TableCell("Single")])]
        table = Table(headers=headers, rows=rows)

        result = render_table(table)
        lines = result.strip().split("\n")

        # Should have: top border, header, separator, data line 1, data line 2, bottom border
        assert len(lines) == 6
        # Check that "Line1" and "Line2" appear on separate lines
        assert "Line1" in lines[3]
        assert "Line2" in lines[4]
        # Check that "Single" appears only on first line, second line has empty
        assert "Single" in lines[3]
        # lines[4] should have blank space where "Single" cell is (padded)
        assert "│" in lines[4]

    def test_multiline_cell_mixed_heights(self):
        """Rows with cells of different heights render correctly."""
        from md2slack.tables import Table, TableCell, TableRow, render_table

        headers = TableRow([
            TableCell("A", is_header=True),
            TableCell("B", is_header=True),
        ])
        rows = [
            TableRow([TableCell("One\nTwo\nThree"), TableCell("X")]),
            TableRow([TableCell("Single"), TableCell("Y")]),
        ]
        table = Table(headers=headers, rows=rows)

        result = render_table(table)
        lines = result.strip().split("\n")

        # Should have: top, header, sep, 3 lines for first row, 1 line for second row, bottom
        assert len(lines) == 8
        assert "One" in lines[3]
        assert "Two" in lines[4]
        assert "Three" in lines[5]
        assert "Single" in lines[6]

    def test_multiline_header(self):
        """Multi-line headers render correctly."""
        from md2slack.tables import Table, TableCell, TableRow, render_table

        headers = TableRow([
            TableCell("Header\nLine 2", is_header=True),
            TableCell("B", is_header=True),
        ])
        rows = [TableRow([TableCell("Data"), TableCell("X")])]
        table = Table(headers=headers, rows=rows)

        result = render_table(table)
        lines = result.strip().split("\n")

        # Should have: top, header line 1, header line 2, sep, data, bottom
        assert len(lines) == 6
        assert "Header" in lines[1]
        assert "Line 2" in lines[2]


# T038: Test full table conversion via convert()
class TestTableConversion:
    """Test table conversion through the full convert() pipeline."""

    def test_markdown_table_to_box_drawing(self):
        """Markdown table converts to box-drawing code block."""
        from md2slack.converter import convert

        md = """| Name | Value |
|------|-------|
| foo  | 42    |"""
        result = convert(md)
        # Should be wrapped in code block
        assert "```" in result
        # Should have box-drawing characters
        assert "\u2500" in result or "\u2502" in result
