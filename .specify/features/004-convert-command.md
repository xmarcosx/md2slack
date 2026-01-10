### 004 - Convert Command

**Problem**: No CLI to preview conversion before posting to Slack. Users can't verify output.

**Desired State**: `md2slack convert --file update.md` outputs converted mrkdwn to stdout.

**Why This Matters**:
1. Constitution Principle IV (Preview Before Commit)—posting to client threads is irreversible
2. Enables verification workflow before committing to Slack

**CLI Interface**:
- Command: `md2slack convert --file <path>`
- Input: Markdown file path
- Output: Converted mrkdwn to stdout

**Example**:
- `md2slack convert --file notes.md` prints converted content
- Exit 0 on success, exit 1 with error message for missing/unreadable file

**Notes**:
- Thin wrapper: read file → call converter → print to stdout
- Clear error messages for file not found, permission denied
- No options beyond --file for MVP (keep it simple)
