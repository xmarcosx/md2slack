# Feature Specification: Slack Post Command

**Feature Branch**: `005-slack-post`
**Created**: 2026-01-10
**Status**: Draft
**Input**: User description: "Post converted markdown content directly to Slack threads via a single CLI command"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Post Markdown to Thread (Priority: P1)

A user has a markdown file containing a status update and wants to post it to an existing Slack thread. They copy the thread URL from Slack, run a single command with the file path and thread URL, and the converted content appears in the thread.

**Why this priority**: This is the core value proposition—eliminating the manual copy/paste workflow between markdown conversion and Slack posting.

**Independent Test**: Can be fully tested by providing a valid thread URL and markdown file, then verifying the message appears in the Slack thread with correct mrkdwn formatting.

**Acceptance Scenarios**:

1. **Given** a valid Slack thread URL and a readable markdown file, **When** the user runs `md2slack post --thread <url> --file <path>`, **Then** the converted content is posted to the thread and a success message with permalink is displayed.
2. **Given** a valid thread URL, **When** the user provides markdown via stdin instead of a file, **Then** the converted content is posted to the thread.
3. **Given** successful posting, **When** the command completes, **Then** the exit code is 0.

---

### User Story 2 - Preview Before Posting (Priority: P2)

A user wants to verify what will be posted before committing to an irreversible action. They run the command with a dry-run flag to see the exact output that would be sent to Slack.

**Why this priority**: Posting to client threads is irreversible. Users need confidence before committing, making preview essential for professional use.

**Independent Test**: Can be fully tested by running with --dry-run flag and verifying output matches what would be posted, without any actual Slack API calls.

**Acceptance Scenarios**:

1. **Given** a valid thread URL and markdown file, **When** the user runs with `--dry-run`, **Then** the converted content is displayed to stdout without posting to Slack.
2. **Given** dry-run mode, **When** the command completes, **Then** no Slack API calls are made and the user sees a clear indicator that this was a preview.

---

### User Story 3 - Add Prefix Text (Priority: P3)

A user wants to prepend a header or label (like "Status Update" or "Weekly Report") before their converted markdown content.

**Why this priority**: Adds flexibility for common formatting patterns without requiring users to modify their source files.

**Independent Test**: Can be fully tested by providing --prefix flag and verifying the prefix appears before the converted content in the posted message.

**Acceptance Scenarios**:

1. **Given** a `--prefix "Status Update\n\n"` option, **When** posting, **Then** the prefix text appears before the converted markdown content.
2. **Given** a prefix with newlines, **When** combined with converted content, **Then** formatting is preserved correctly.

---

### Edge Cases

- What happens when the thread URL format is invalid or unrecognized? → Clear error message explaining expected URL format.
- What happens when the SLACK_BOT_TOKEN environment variable is missing? → Error message directing user to set the token.
- What happens when the token is expired or invalid? → Error message indicating authentication failure with remediation steps.
- What happens when the bot lacks permission to post to the channel? → Error message explaining the bot needs to be invited to the channel.
- What happens when the channel or thread no longer exists? → Error message indicating the thread was not found.
- What happens when the converted content exceeds Slack's 40,000 character limit? → Warning displayed, content truncated with indicator.
- What happens when the Slack API rate limits the request? → Error message with retry guidance.
- What happens when the markdown file is empty? → Post empty content (valid use case for clearing or minimal updates).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST parse Slack thread URLs in the format `https://<workspace>.slack.com/archives/<channel_id>/p<timestamp>` to extract channel ID and thread timestamp.
- **FR-002**: System MUST read the bot token from the `SLACK_BOT_TOKEN` environment variable.
- **FR-003**: System MUST convert markdown content using the existing converter before posting.
- **FR-004**: System MUST post the converted content as a reply to the specified thread.
- **FR-005**: System MUST support `--dry-run` flag to preview without posting.
- **FR-006**: System MUST support `--prefix` option to prepend text before converted content.
- **FR-007**: System MUST accept markdown input from either a file path argument or stdin.
- **FR-008**: System MUST display a success message with the posted message permalink on successful posting.
- **FR-009**: System MUST warn and truncate content that exceeds 40,000 characters.
- **FR-010**: System MUST provide clear, actionable error messages for all failure modes:
  - Invalid URL format
  - Missing token
  - Invalid/expired token
  - Channel not found
  - Permission denied (not in channel)
  - Rate limiting

### Key Entities

- **Thread URL**: The Slack permalink containing workspace, channel ID, and message timestamp; used as the primary identifier for where to post.
- **Bot Token**: OAuth token with `chat:write` scope; required for authentication with Slack API.
- **Converted Content**: The markdown input transformed to Slack mrkdwn format; the payload to be posted.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can post markdown to a Slack thread in a single command invocation (no intermediate steps).
- **SC-002**: Users can preview exact output before posting using dry-run mode.
- **SC-003**: 100% of supported error conditions produce distinct, actionable error messages.
- **SC-004**: Content exceeding Slack's character limit is handled gracefully with warning and truncation.
- **SC-005**: Posted messages preserve all formatting from the markdown source (headings, lists, links, tables, code blocks).

## Assumptions

- Users have access to copy thread URLs from Slack (standard Slack functionality).
- Users have already set up the `SLACK_BOT_TOKEN` environment variable (documented in README, uses 1Password).
- The bot has been invited to channels where it needs to post (required for `chat:write` scope).
- Thread URLs follow Slack's standard permalink format.
- The existing `md2slack convert` functionality correctly handles all markdown-to-mrkdwn transformations.
