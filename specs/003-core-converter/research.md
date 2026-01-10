# Research: Core Converter

**Feature**: 003-core-converter
**Date**: 2026-01-09

## Decisions Summary

| Topic | Decision | Rationale |
|-------|----------|-----------|
| Markdown Parser | mistune 3.x | Lightweight, AST-based, extensible custom renderer |
| Renderer Approach | Subclass `HTMLRenderer` | Simpler API, children pre-rendered, methods receive text |
| Table Rendering | Custom box-drawing in code block | Slack lacks native tables; monospace preserves alignment |
| Box Style | Light lines (U+2500 block) | Universal font support, clean appearance |

## Research Findings

### 1. Markdown Parser: mistune

**Decision**: Use mistune 3.2.0 with custom renderer

**Rationale**:
- Lightweight pure Python implementation
- AST-based parsing enables clean separation of parsing and rendering
- Extensible via custom renderers and plugins
- Built-in plugins for `strikethrough` and `table`
- Python 3.8+ compatible (project requires 3.10+)

**Alternatives Considered**:
- `markdown-it-py`: Heavier, CommonMark compliant but more complex
- `commonmark`: Strict CommonMark, less extensible
- Regex-based: Fragile, doesn't handle nested structures

**Implementation Pattern**:
```python
from mistune import HTMLRenderer
import mistune

class SlackMrkdwnRenderer(HTMLRenderer):
    def __init__(self):
        super().__init__(escape=False)  # No HTML escaping needed

    def strong(self, text: str) -> str:
        return f'*{text}*'  # **bold** -> *bold*

    def strikethrough(self, text: str) -> str:
        return f'~{text}~'  # ~~strike~~ -> ~strike~

    # ... other methods

markdown = mistune.create_markdown(
    renderer=SlackMrkdwnRenderer(),
    plugins=['strikethrough', 'table']
)
```

### 2. Slack mrkdwn Format

**Conversion Rules**:

| Markdown | Slack mrkdwn | Implementation |
|----------|--------------|----------------|
| `# Heading` | `*Heading*` | `heading()` method |
| `**bold**` | `*bold*` | `strong()` method |
| `_italic_` or `*italic*` | `_italic_` | `emphasis()` method |
| `~~strike~~` | `~strike~` | `strikethrough()` method (plugin) |
| `[text](url)` | `<url\|text>` | `link()` method |
| `` `code` `` | `` `code` `` | `codespan()` method (passthrough) |
| `- item` | `• item` | `list_item()` method |
| `1. item` | `1. item` | `list_item()` method with counter |
| `> quote` | `>quote` | `block_quote()` method |
| ` ```code``` ` | ` ```code``` ` | `block_code()` method (passthrough) |

**Special Characters to Escape**:
- `&` -> `&amp;`
- `<` -> `&lt;`
- `>` -> `&gt;` (but NOT in block quotes)

### 3. Table Rendering

**Decision**: Render markdown tables as monospace code blocks with Unicode box-drawing characters

**Rationale**:
- Slack doesn't support native tables
- Code blocks use monospace font, preserving alignment
- Box-drawing characters create professional appearance (Constitution Principle V)

**Box-Drawing Characters (Light Style)**:
```python
BOX = {
    'h': '─',        # U+2500 horizontal
    'v': '│',        # U+2502 vertical
    'tl': '┌',       # U+250C top-left corner
    'tr': '┐',       # U+2510 top-right corner
    'bl': '└',       # U+2514 bottom-left corner
    'br': '┘',       # U+2518 bottom-right corner
    'lt': '├',       # U+251C left T-junction
    'rt': '┤',       # U+2524 right T-junction
    'tt': '┬',       # U+252C top T-junction
    'bt': '┴',       # U+2534 bottom T-junction
    'x': '┼',        # U+253C cross
}
```

**Rendering Algorithm**:
1. Parse table tokens (headers + rows)
2. Calculate column widths from max content length
3. For long content: wrap text into multi-line cells
4. Render top border
5. Render header row(s)
6. Render header separator
7. Render data rows with row separators
8. Render bottom border
9. Wrap in code block (` ``` `)

**Example Output**:
```
┌────────┬───────┬─────────┐
│ Name   │ Role  │ Status  │
├────────┼───────┼─────────┤
│ Alice  │ Admin │ Active  │
│ Bob    │ User  │ Pending │
└────────┴───────┴─────────┘
```

**Multi-line Cell Handling**:
- Use `textwrap.wrap()` with configurable width
- Track maximum height per row
- Pad shorter cells with empty lines
- Default max cell width: 40 characters (configurable)

### 4. Nested Formatting

**Decision**: Let mistune handle nesting via recursive rendering

**Pattern**: When rendering a container element (e.g., link), the `text` parameter already contains rendered children:

```python
def link(self, text: str, url: str, title: str = None) -> str:
    # text is already rendered (may contain *bold*, etc.)
    return f'<{url}|{text}>'
```

**Edge Cases**:
- Bold inside link: `**[text](url)**` works naturally
- Link inside bold: `**[text](url)**` -> `*<url|text>*`
- Code inside anything: preserved literally (mistune handles)

### 5. Escaping and Edge Cases

**Escaped Characters**:
- Mistune parses `\*` as literal `*` (not bold delimiter)
- Renderer receives plain text, no special handling needed

**Malformed Markdown**:
- Mistune is lenient by design
- Unclosed delimiters treated as literal text
- No crashes, content preserved (meets FR-011)

**Code Block Content**:
- Content inside ` ``` ` or `` ` `` is NOT parsed
- Renderer receives raw text, passes through unchanged

## Dependencies

**Required Additions to pyproject.toml**:
```toml
dependencies = [
    "click>=8.0",
    "mistune>=3.0,<4.0",
]
```

## Performance Considerations

- mistune is synchronous, single-pass parsing
- Rendering is O(n) where n is document length
- Table width calculation requires two passes over table content
- Spec target: <100ms for 10,000 chars (easily achievable)

## Sources

- [mistune documentation](https://mistune.lepture.com/en/latest/)
- [mistune GitHub](https://github.com/lepture/mistune)
- [Slack mrkdwn reference](https://api.slack.com/reference/surfaces/formatting)
- [Unicode Box Drawing (U+2500)](https://www.unicode.org/charts/PDF/U2500.pdf)
- [Python textwrap docs](https://docs.python.org/3/library/textwrap.html)
