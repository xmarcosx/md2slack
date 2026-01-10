# Prompt: Project Foundation Implementation

_For use with /speckit.plan_
_Source: .specify/specs/001-project-foundation/spec.md_
_Generated: 2026-01-09_

---

The project foundation spec establishes the package structure and CLI skeleton. Implementation should create the directory structure first, then the pyproject.toml with all metadata and dependencies, followed by the minimal Python modules needed for the CLI entry point.

The CLI module at `src/md2slack/cli.py` will define the Click group and placeholder subcommands. Keep it minimal—just enough to make `md2slack --help` show the tool description and list convert/post as available commands. Each subcommand can be a stub that exits with a "not implemented" message.

Since this is pure infrastructure, testing is limited to verifying the package installs and the CLI invokes without errors. A single smoke test that runs `md2slack --help` and checks for a zero exit code is sufficient. The testing foundation feature (002) will set up proper test infrastructure.
