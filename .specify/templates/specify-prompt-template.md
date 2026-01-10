# Specify Prompt Template

This template guides the creation of natural language prompts for `/speckit.specify`.

---

## Format

```markdown
# Prompt: [Feature Name]

_For use with /speckit.specify_
_Source: .specify/features/NNN-feature-name.md_
_Generated: [DATE]_

---

[1-3 paragraphs of natural language prose describing the feature]
```

## Guidelines

### DO

- Write in natural, conversational prose
- Describe the user problem and desired outcome
- Include relevant context about the CLI tool
- Mention constraints or edge cases worth considering
- Reference the feature brief if one exists

### DON'T

- Create structured sections (User Stories, Requirements, Acceptance Criteria)
- Write bullet lists of requirements
- Use `[NEEDS CLARIFICATION]` markers
- Include implementation details
- Mimic Spec Kit's output format

## Example

```markdown
# Prompt: Thread URL Parsing

_For use with /speckit.specify_
_Source: .specify/features/002-thread-url-parsing.md_
_Generated: 2026-01-09_

---

When users want to post to a Slack thread, they'll copy the thread URL from
Slack. These URLs look like "https://yourorg.slack.com/archives/C0123ABCD/p1234567890123456"
and contain both the channel ID and the thread timestamp encoded in a specific format.

The CLI needs to parse these URLs to extract the channel ID and thread_ts values
that the Slack API requires. Users shouldn't need to understand Slack's internal
ID formats - they just paste the URL they copied.

The parser should handle both the web URL format and the newer slack:// protocol
links, and provide clear error messages if the URL format is unrecognized.
```

## Quality Checks

Before finalizing:
- [ ] Is this natural language prose (not structured requirements)?
- [ ] Does it explain the problem and desired outcome?
- [ ] Does it provide enough context for Spec Kit?
- [ ] Is it free of implementation details?
