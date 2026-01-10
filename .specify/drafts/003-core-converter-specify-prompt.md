# Prompt: Core Converter

_For use with /speckit.specify_
_Source: .specify/features/003-core-converter.md_
_Generated: 2026-01-09_

---

The core converter is the heart of md2slack—a pure function that transforms markdown into Slack's mrkdwn format. When a user passes markdown content, the converter should return a string that renders correctly in Slack while preserving the original document's structure and intent.

The conversion needs to handle the standard markdown elements: headings become bold text (since Slack has no native heading support), double-asterisk bold becomes single-asterisk bold, strikethrough tildes stay as tildes but with Slack's single-tilde syntax, and markdown links transform into Slack's angle-bracket format. Lists should convert to bullet points using the bullet character. The trickiest part is tables—since Slack doesn't support tables natively, these need to render as monospace code blocks using Unicode box-drawing characters to preserve the tabular structure with proper column alignment.

Edge cases matter here: nested formatting (bold inside a link, code inside a table cell), escaped characters that shouldn't be converted, and malformed markdown that should degrade gracefully rather than break. The function should be pure with no side effects—it takes a string, returns a string, and does nothing else.
