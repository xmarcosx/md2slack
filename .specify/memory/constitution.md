<!--
  Sync Impact Report
  ==================
  Version change: (new) → 1.0.0

  Modified principles: N/A (initial creation)

  Added sections:
  - Core Principles (5 principles)
  - Quality Standards
  - Development Workflow
  - Governance

  Removed sections: N/A (initial creation)

  Templates requiring updates:
  - .specify/templates/plan-template.md ✅ (compatible - uses generic constitution reference)
  - .specify/templates/spec-template.md ✅ (compatible - no constitution-specific references)
  - .specify/templates/tasks-template.md ✅ (compatible - no constitution-specific references)

  Follow-up TODOs: None
-->

# md2slack Constitution

## Core Principles

### I. One-Command Workflow

Every operation MUST be completable in a single command invocation. The tool MUST NOT
require intermediate steps, temporary files, or manual file juggling between conversion
and posting.

**Rationale**: The tool exists to eliminate friction. Multi-step workflows recreate the
problem we're solving.

### II. Faithful Conversion

The converter MUST preserve the structure and intent of markdown content when
transforming to Slack's mrkdwn format. This includes:

- Headings MUST remain visually distinct (rendered as bold)
- Lists MUST maintain hierarchy and bullet styling
- Tables MUST be readable (box-drawing characters in code blocks)
- Code blocks MUST be preserved with proper formatting
- Links MUST be functional in Slack

**Rationale**: Users write structured markdown for a reason. Losing that structure
defeats the purpose of using markdown in the first place.

### III. Zero Friction

The CLI MUST have sensible defaults and minimal required arguments:

- Thread URL MUST be the primary identifier (no separate channel/timestamp args)
- Token MUST be configurable via environment variable or config file
- Common options MUST have short flags

**Rationale**: Every required argument is friction. Optimize for the common case of
"post this file to that thread."

### IV. Preview Before Commit

The tool MUST always provide a way to see output before posting:

- `convert` subcommand MUST show formatted output without posting
- Dry-run mode MUST be available for the `post` command
- Output preview MUST exactly match what will be posted

**Rationale**: Posting to a client thread is not reversible. Users need confidence
before committing.

### V. Professional Output

All output MUST look intentional and polished:

- Tables MUST use box-drawing characters for clean alignment
- Formatting MUST be consistent (no mixing of styles)
- Edge cases (nested lists, code in tables) MUST degrade gracefully, not break
- Error messages MUST be clear and actionable

**Rationale**: This tool exists to make users look professional. Broken or ugly
output is worse than manual reformatting.

## Quality Standards

The codebase MUST meet these quality requirements:

- **Test Coverage**: Conversion logic MUST have comprehensive tests covering:
  - All supported markdown elements
  - Edge cases (nested structures, special characters)
  - Table rendering accuracy
- **Error Handling**: CLI MUST fail fast with clear error messages
  - Invalid thread URLs MUST be caught before API calls
  - Missing tokens MUST produce actionable error messages
  - API errors MUST include relevant context
- **Code Style**: All code MUST pass `ruff check` with no warnings

## Development Workflow

- **Package Management**: Use `uv` for all dependency management
- **Testing**: Run `uv run pytest` before committing changes
- **Linting**: Run `uv run ruff check .` to verify code style
- **Secrets**: Use 1Password for storing `SLACK_BOT_TOKEN` (see `op-env-refs`)

## Governance

This constitution defines the non-negotiable principles for md2slack development.
All feature implementations MUST align with these principles.

**Amendment Process**:

1. Propose changes via pull request to this file
2. Document rationale for any principle changes
3. Update version number according to semantic versioning:
   - MAJOR: Removing or fundamentally redefining a principle
   - MINOR: Adding new principles or expanding existing ones
   - PATCH: Clarifications and wording improvements
4. Update `LAST_AMENDED_DATE` on any change

**Compliance Review**:

- Feature specifications MUST reference relevant principles
- Implementation plans MUST include a Constitution Check section
- Code reviews SHOULD verify principle alignment

**Version**: 1.0.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-09
