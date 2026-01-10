# Prompt: Testing Foundation Implementation

_For use with /speckit.plan_
_Source: .specify/specs/002-testing-foundation/spec.md_
_Generated: 2026-01-09_

---

The testing foundation spec is complete and ready for implementation. This is
infrastructure work that sets up pytest for the project - no application logic
involved, just configuration and fixture scaffolding.

The implementation should start with adding pytest and pytest-cov as dev dependencies
in pyproject.toml, along with the pytest configuration section. Then create the tests
directory structure mirroring the source layout (tests/test_converter.py, etc). The
conftest.py file at the tests root will hold shared fixtures - start with a fixture
for sample markdown strings and one using tmp_path for file-based test scenarios.

Since this is pure infrastructure, verification is straightforward: `uv run pytest`
should exit 0 and show the test collection working (even if there are zero actual
tests yet). The fixtures should be importable and functional so the next feature
can immediately start writing tests against them.
