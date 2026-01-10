---
name: roadmap
description: Manages the product roadmap for md2slack CLI tool. Use when the user wants to add features to the roadmap, see what's planned, sequence work, break down goals into features, or decide what to build next. Triggers on phrases like "add to roadmap", "what's next", "show roadmap", "break down this goal", "sequence features", or "roadmap".
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roadmap Management

You manage the product roadmap for md2slack, helping translate high-level goals into actionable, sequenced features.

## When to Activate

Activate this skill when the user:
- Wants to see the current roadmap status
- Wants to add a feature idea to the backlog
- Asks what to work on next
- Wants to break down a high-level goal into features
- Asks about feature sequencing or dependencies

## Context Loading

Before any action, read:
1. `ROADMAP.md` at repository root (create if missing)
2. `.specify/memory/constitution.md` (if exists) for project principles
3. `.specify/templates/feature-brief-template.md` for brief format
4. `.specify/specs/` to see what features already have specifications
5. `.specify/drafts/` to see what's being actively planned

## ROADMAP.md Structure

Always maintain this structure:

```markdown
# md2slack Roadmap

## Vision
[One paragraph: what this CLI tool does and who it's for]

## Current Focus
[The feature currently being worked on, if any]

## Up Next
Features ready to be specified (in order):
- [ ] NNN - [One sentence description]

## Backlog
Features identified but not yet sequenced:
- [ ] [One sentence description]

---

## Feature Briefs

Feature briefs are stored as separate files in `.specify/features/`.

See individual files: [001-feature-name.md](.specify/features/001-feature-name.md), etc.

---

## Shipped
- [x] NNN - [One sentence description] (shipped [date])

## Parking Lot
Ideas captured but not committed to:
- [Vague or distant ideas]

---

## Dependencies Map
[feature] → [depends on]

## Goals Decomposition Log
### [Goal name]
Broken down on [date]:
- Feature A
- Feature B
```

## Feature Brief Format

When a feature moves to "Current Focus" or "Up Next", write a detailed brief.

**Load the template**: Read `.specify/templates/feature-brief-template.md` for the required format.

**Write briefs to**: `.specify/features/NNN-feature-name.md`

**Key principle**: Briefs capture WHAT and WHY, never HOW. Keep them short.

## Feature Breakdown Principles

When breaking down goals:
1. **ONE SENTENCE per feature** — Details belong in briefs, not the roadmap
2. **Identify dependencies explicitly** — What must exist before this can be built?
3. **Prefer smaller over larger** — Bias toward shippable increments
4. **Group related features** but avoid artificial phases

## Sequencing Priorities (CLI Development)

1. Core CLI structure (Click commands, arguments, options)
2. Data transformation (markdown → mrkdwn conversion)
3. External integrations (Slack API client)
4. Configuration management (tokens, defaults)
5. Error handling and user feedback
6. Testing and reliability
7. Documentation and help text

## Numbering Convention

- Features in "Up Next" get three-digit numbers (001, 002, etc.)
- Backlog items do NOT get numbers until they're sequenced into "Up Next"
- Numbers persist even after shipping (for reference)

## Quality Checks

Before finalizing any roadmap update:
1. Verify every feature in "Up Next" has its dependencies already shipped or sequenced earlier
2. Confirm feature descriptions are truly one sentence
3. Check that the dependencies map is current
4. Ensure "Current Focus" matches what's actually being worked on

## After Any Roadmap Change

1. Show the user the specific changes made
2. Highlight any new dependencies identified
3. Note if the change affects current sequencing
4. Offer relevant follow-up actions (e.g., "Want me to create a brief for this?")

## Interaction Style

- Be collaborative, not prescriptive—offer recommendations with rationale
- Ask clarifying questions when goals are ambiguous
- Proactively surface dependency conflicts or sequencing issues
- When adding features, always show where they fit and why
- Keep responses focused—the roadmap is about direction, not implementation details

## Project Context

- **Tech Stack**: Python 3, Click CLI framework, uv for package management
- **Key Features**: Markdown to Slack mrkdwn conversion, table rendering, thread posting
- **Architecture**: CLI commands in `cli.py`, conversion in `converter.py`, Slack API in `slack.py`
- **Secrets**: Uses 1Password for `SLACK_BOT_TOKEN`
