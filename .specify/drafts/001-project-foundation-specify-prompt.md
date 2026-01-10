# Prompt: Project Foundation

_For use with /speckit.specify_
_Source: .specify/features/001-project-foundation.md_
_Generated: 2026-01-09_

---

We need to bootstrap md2slack as an installable Python package with a working CLI entry point. Right now there's no code at all—just documentation describing what the tool should eventually do. The goal is to get `md2slack --help` working so we have a foundation to build on.

The package should use the standard src-layout with source code under `src/md2slack/`. The CLI will be built with Click, and the entry point should expose placeholder subcommands for `convert` and `post` that just print "not implemented yet" messages. This gives us the command structure from day one even though the functionality comes later.

For dependencies, we only need Click for now—the markdown parsing library will be chosen when we implement the converter. Dev dependencies should include ruff for linting and pytest for testing, matching the workflow described in CLAUDE.md. The package should be installable in dev mode via `uv pip install -e .` so we can iterate quickly.
