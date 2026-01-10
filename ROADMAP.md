# md2slack Roadmap

## Vision

A CLI tool for developers who maintain markdown notes and need to post
structured updates to Slack threads without manual reformatting.

## Current Focus

None — ready for next feature.

## Up Next

Features ready to be specified (in order):
- [ ] 008 - Line range selection flag to parse and post only specific lines from a file

## Backlog

Features identified but not yet sequenced:
(none)

---

## Feature Briefs

See individual files in `.specify/features/`:
- [001-project-foundation.md](.specify/features/001-project-foundation.md)
- [002-testing-foundation.md](.specify/features/002-testing-foundation.md)
- [003-core-converter.md](.specify/features/003-core-converter.md)
- [004-convert-command.md](.specify/features/004-convert-command.md)
- [005-slack-integration.md](.specify/features/005-slack-integration.md)
- [006-auto-chunking.md](.specify/features/006-auto-chunking.md)
- [007-default-chunking.md](.specify/features/007-default-chunking.md)
- [008-line-range-selection.md](.specify/features/008-line-range-selection.md)

---

## Shipped

- [x] 007 - Default chunking with content preservation (shipped 2026-01-10)
- [x] 006 - Auto-chunking for long content (shipped 2026-01-10)
- [x] 005 - Slack integration with post command (shipped 2026-01-10)
- [x] 004 - Convert command for preview mode (shipped 2026-01-10)
- [x] 003 - Core converter for markdown→mrkdwn (shipped 2026-01-10)
- [x] 002 - Testing foundation with pytest infrastructure (shipped 2026-01-09)
- [x] 001 - Project foundation with pyproject.toml and Click skeleton

## Parking Lot

Ideas captured but not committed to:
- Thread discovery (list recent threads in channel)
- Message templates (reusable prefixes/headers)
- Clipboard output support

---

## Dependencies Map

```
008-line-range-selection → 005-slack-integration
007-default-chunking → 006-auto-chunking
006-auto-chunking → 005-slack-integration
005-slack-integration → 003-core-converter
004-convert-command → 003-core-converter
003-core-converter → 002-testing-foundation
002-testing-foundation → 001-project-foundation
```
