# Prompt: Testing Foundation

_For use with /speckit.specify_
_Source: .specify/features/002-testing-foundation.md_
_Generated: 2026-01-09_

---

The md2slack CLI needs a testing foundation before we can build the core converter
and other features. Right now there's no tests directory and pytest isn't configured,
so running `uv run pytest` would fail. We need the infrastructure in place so that
developers can write tests as they build features.

The test setup should be minimal but ready for what's coming next. The core converter
(003) will need to test markdown-to-mrkdwn transformations, so we'll want fixtures
that provide sample markdown strings and a way to create temporary files for
file-based input testing. Keep the fixtures lean though - only add what's actually
needed for the next feature, not a kitchen-sink fixture library.

Configuration should live in pyproject.toml rather than a separate pytest.ini file,
keeping the repo's configuration consolidated. The tests directory should be at the
repo root with a structure that mirrors the source modules, making it easy to find
the tests for any given piece of functionality.
