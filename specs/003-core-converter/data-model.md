# Data Model: Core Converter

**Feature**: 003-core-converter
**Date**: 2026-01-09

## Overview

The core converter is a pure function with no persistence. This document describes the internal data structures used during markdown-to-mrkdwn conversion.

## Core Types

### ConverterResult

The main converter returns a simple string result. No wrapper type needed for the primary function:

```python
def convert(markdown: str) -> str:
    """Convert markdown to Slack mrkdwn format."""
    ...
```

### Table Data Structures

Table rendering requires intermediate structures to calculate widths and handle multi-line cells.

```python
@dataclass
class TableCell:
    """A single cell in a table."""
    content: str
    alignment: Literal['left', 'center', 'right'] | None = None
    is_header: bool = False

    @property
    def lines(self) -> list[str]:
        """Split content into lines for multi-line cell rendering."""
        return self.content.split('\n')

    @property
    def width(self) -> int:
        """Maximum line width in the cell."""
        return max((len(line) for line in self.lines), default=0)

@dataclass
class TableRow:
    """A row of cells in a table."""
    cells: list[TableCell]

    @property
    def height(self) -> int:
        """Number of lines in the tallest cell."""
        return max((len(cell.lines) for cell in self.cells), default=1)

@dataclass
class Table:
    """Parsed table structure for rendering."""
    headers: TableRow
    rows: list[TableRow]

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
```

### Box-Drawing Character Set

```python
@dataclass(frozen=True)
class BoxChars:
    """Unicode box-drawing character set."""
    horizontal: str = '─'      # U+2500
    vertical: str = '│'        # U+2502
    top_left: str = '┌'        # U+250C
    top_right: str = '┐'       # U+2510
    bottom_left: str = '└'     # U+2514
    bottom_right: str = '┘'    # U+2518
    left_t: str = '├'          # U+251C
    right_t: str = '┤'         # U+2524
    top_t: str = '┬'           # U+252C
    bottom_t: str = '┴'        # U+2534
    cross: str = '┼'           # U+253C

# Default character set
LIGHT_BOX = BoxChars()
```

## Renderer State

The mistune renderer may need to track state for ordered lists:

```python
@dataclass
class ListState:
    """Track list context during rendering."""
    ordered: bool = False
    counter: int = 0
    depth: int = 0
```

## Conversion Flow

```
Input (str)          Mistune Parser        AST Tokens         SlackRenderer        Output (str)
────────────────────────────────────────────────────────────────────────────────────────────────

"# Heading"    -->   parse()        -->   [{type: 'heading',  -->  heading()   -->  "*Heading*\n\n"
                                           level: 1,
                                           children: [...]}]

"**bold**"     -->   parse()        -->   [{type: 'strong',   -->  strong()    -->  "*bold*"
                                           children: [...]}]

"| A | B |"    -->   parse()        -->   [{type: 'table',    -->  table()     -->  "```\n┌───┬───┐\n..."
                                           children: [...]}]       (with tables.py)
```

## Validation Rules

Since this is a pure function converter, validation is minimal:

| Input | Behavior |
|-------|----------|
| Empty string | Return empty string |
| Whitespace only | Preserve whitespace |
| Invalid UTF-8 | Python handles (raises UnicodeDecodeError at caller) |
| Malformed markdown | Degrade gracefully (mistune is lenient) |
| Very long input | Process as-is (no length limit) |

## Module Structure

```
src/md2slack/
├── converter.py      # Main convert() function, SlackMrkdwnRenderer
└── tables.py         # Table dataclasses, render_table() function
```

### converter.py Exports

```python
# Primary API
def convert(markdown: str) -> str: ...

# For testing/advanced use
class SlackMrkdwnRenderer(HTMLRenderer): ...
```

### tables.py Exports

```python
# Data structures
class TableCell: ...
class TableRow: ...
class Table: ...
class BoxChars: ...

# Constants
LIGHT_BOX: BoxChars

# Rendering
def render_table(table: Table, box: BoxChars = LIGHT_BOX) -> str: ...
def wrap_cell(content: str, width: int) -> list[str]: ...
```
