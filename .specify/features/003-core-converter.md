### 003 - Core Converter

**Problem**: No way to transform markdown to Slack's mrkdwn format. Users must manually reformat.

**Desired State**: A pure function converts markdown string → mrkdwn string, handling all elements including tables.

**Why This Matters**:
1. Core value proposition of the tool—this is the main feature
2. Constitution Principle II (Faithful Conversion) requires complete, accurate transformation

**Example**:
- Input: `# Heading\n**bold** and [link](url)`
- Output: `*Heading*\n*bold* and <url|link>`

**Notes**:
- Conversion rules (from README):
  - `# Heading` → `*Heading*` (bold)
  - `**bold**` → `*bold*`
  - `~~strike~~` → `~strike~`
  - `[text](url)` → `<url|text>`
  - `- item` → `• item`
  - Tables → monospace code blocks with box-drawing characters
- Edge cases to handle: nested formatting, escaped characters, code in tables
- Use existing markdown parser (mistune or similar), transform AST
- Pure function: no file I/O, no side effects
