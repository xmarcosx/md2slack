### 008 - Line Range Selection

**Problem**: Users maintain comprehensive markdown notes but often need to post only a specific section to Slack. Currently, they must either manually copy the desired lines to a separate file or copy-paste directly—defeating the purpose of the one-command workflow.

**Desired State**: Users can specify a line range (e.g., `--lines 123-147`) to extract and post only those lines from a larger markdown file, preserving the single-command workflow.

**Why This Matters**:
1. Eliminates manual extraction when sharing a specific section from a larger document
2. Maintains the "one-command workflow" principle even for partial content

**CLI Interface**:
- Command: `md2slack post FILE --thread URL --lines START-END`
- Also works with: `md2slack convert FILE --lines START-END`
- Input: File path with optional line range (1-indexed, inclusive)
- Output: Only the specified lines are converted/posted

**Example**:
- Current: Copy lines 123-147 to a temp file, then `md2slack post temp.md --thread URL`
- Desired: `md2slack post notes.md --thread URL --lines 123-147`

**Notes**:
- Line numbers should be 1-indexed (matching editor conventions)
- Range is inclusive on both ends (123-147 includes both lines 123 and 147)
- Should validate that range exists within file bounds
- Should work with both `post` and `convert` commands for consistency
