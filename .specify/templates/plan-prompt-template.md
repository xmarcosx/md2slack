# Plan Prompt Template

This template guides the creation of natural language prompts for `/speckit.plan`.

---

## Format

```markdown
# Prompt: [Feature Name] Implementation

_For use with /speckit.plan_
_Source: .specify/specs/NNN-feature-name/spec.md_
_Generated: [DATE]_

---

[1-3 paragraphs of natural language prose about implementation approach]
```

## Guidelines

### DO

- Reference the completed spec from `/speckit.specify`
- Describe the implementation approach at a high level
- Mention which modules/files will be affected
- Note any architectural decisions or patterns to follow
- Include testing considerations

### DON'T

- Repeat the full spec content
- Create structured task lists (that's Spec Kit's job)
- Go into line-by-line implementation details
- Use `[NEEDS CLARIFICATION]` markers

## Example

```markdown
# Prompt: Thread URL Parsing Implementation

_For use with /speckit.plan_
_Source: .specify/specs/002-thread-url-parsing/spec.md_
_Generated: 2026-01-09_

---

The thread URL parsing spec is complete and ready for implementation. The parser
should live in a dedicated module since it's a self-contained piece of functionality
that the CLI will call when processing the --thread argument.

For the implementation approach, start with the URL parsing logic itself - a function
that takes a Slack thread URL string and returns a tuple of (channel_id, thread_ts).
The regex patterns should handle both the web format and slack:// protocol. Error
handling should provide actionable messages that help users understand what went wrong.

Testing should cover the various URL formats from the spec, including edge cases like
malformed URLs and URLs from different Slack workspace domains. Since this is pure
string parsing with no external dependencies, unit tests will be straightforward.
```

## Quality Checks

Before finalizing:
- [ ] Does it reference the completed spec?
- [ ] Does it describe the implementation approach (not detailed steps)?
- [ ] Does it mention affected modules/files?
- [ ] Is it natural language prose (not a task list)?
