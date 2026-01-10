### 001 - Project Foundation

**Problem**: No runnable package exists. Cannot install or invoke `md2slack` command.

**Desired State**: Running `md2slack --help` shows CLI usage. Package installs via `uv pip install -e .` in dev mode.

**Why This Matters**:
1. Establishes the project skeleton that all other features build on
2. Enables iterative development with a working entry point from day one

**CLI Interface**:
- Command: `md2slack --help`
- Output: Shows available subcommands (convert, post) as placeholders

**Notes**:
- Use src-layout: `src/md2slack/`
- Minimal dependencies: Click only (defer markdown parser choice to 003)
- Include ruff and pytest in dev dependencies
- Entry point in pyproject.toml: `md2slack = "md2slack.cli:main"`
