# Quickstart: Core Converter

**Feature**: 003-core-converter

## Basic Usage

```python
from md2slack.converter import convert

# Convert markdown to Slack mrkdwn
slack_text = convert("# Hello **World**")
print(slack_text)
# Output: *Hello *World**
#
```

## Conversion Examples

### Text Formatting

```python
# Headings become bold
convert("# Main Title")      # -> "*Main Title*\n\n"
convert("## Subtitle")       # -> "*Subtitle*\n\n"

# Bold: double asterisk -> single asterisk
convert("**important**")     # -> "*important*"

# Italic stays as underscore
convert("_emphasis_")        # -> "_emphasis_"

# Strikethrough: double tilde -> single tilde
convert("~~deleted~~")       # -> "~deleted~"

# Links use Slack format
convert("[Click here](https://example.com)")
# -> "<https://example.com|Click here>"
```

### Lists

```python
# Unordered lists use bullet character
convert("""
- Item one
- Item two
- Item three
""")
# Output:
# • Item one
# • Item two
# • Item three

# Ordered lists preserve numbering
convert("""
1. First
2. Second
3. Third
""")
# Output:
# 1. First
# 2. Second
# 3. Third
```

### Tables

```python
convert("""
| Name  | Role   |
|-------|--------|
| Alice | Admin  |
| Bob   | User   |
""")
# Output (wrapped in code block):
# ```
# ┌───────┬────────┐
# │ Name  │ Role   │
# ├───────┼────────┤
# │ Alice │ Admin  │
# │ Bob   │ User   │
# └───────┴────────┘
# ```
```

### Code Blocks

```python
# Inline code: backticks preserved (Slack supports them)
convert("Use `pip install`")  # -> "Use `pip install`"

# Fenced code blocks preserved
convert("""
```python
def hello():
    print("world")
```
""")
# Output:
# ```
# def hello():
#     print("world")
# ```
```

## Edge Cases

```python
# Empty input returns empty output
convert("")           # -> ""

# Whitespace preserved
convert("   ")        # -> "   "

# Malformed markdown degrades gracefully
convert("**unclosed") # -> "**unclosed" (no crash)

# Escaped characters preserved
convert(r"\*not bold\*")  # -> "*not bold*"
```

## Integration with CLI

```bash
# Via convert command (once CLI is integrated)
md2slack convert input.md

# Via post command with preview
md2slack post --dry-run input.md https://slack.com/thread/...
```

## Direct Import

```python
# For advanced use cases, access the renderer directly
from md2slack.converter import SlackMrkdwnRenderer
import mistune

renderer = SlackMrkdwnRenderer()
md = mistune.create_markdown(
    renderer=renderer,
    plugins=['strikethrough', 'table']
)

result = md("Your **markdown** here")
```

## Table Rendering Module

```python
from md2slack.tables import Table, TableRow, TableCell, render_table

# Build table programmatically
table = Table(
    headers=TableRow([
        TableCell("Name", is_header=True),
        TableCell("Value", is_header=True)
    ]),
    rows=[
        TableRow([TableCell("foo"), TableCell("42")]),
        TableRow([TableCell("bar"), TableCell("17")])
    ]
)

print(render_table(table))
# ┌──────┬───────┐
# │ Name │ Value │
# ├──────┼───────┤
# │ foo  │ 42    │
# │ bar  │ 17    │
# └──────┴───────┘
```
