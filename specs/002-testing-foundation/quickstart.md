# Quickstart: Testing Foundation

**Feature**: 002-testing-foundation
**Date**: 2026-01-09

## What This Feature Does

Provides shared test fixtures for the md2slack project, enabling TDD workflow for upcoming features like the core markdown converter.

## Running Tests

```bash
# Install dependencies (if not already done)
uv sync --dev

# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run tests with coverage
uv run pytest --cov=md2slack
```

## Using Fixtures

### Markdown Samples

Access pre-defined markdown patterns in your tests:

```python
def test_heading_conversion(markdown_samples):
    heading = markdown_samples["heading"]
    # heading == "# Hello World"
    result = convert(heading)
    assert result == "*Hello World*"
```

Available samples:
- `heading` - H1 heading
- `bold` - Bold text
- `italic` - Italic text
- `link` - Markdown link
- `list` - Bullet list
- `code_inline` - Inline code
- `code_block` - Fenced code block
- `table` - Markdown table

### Temporary Files

Use pytest's built-in `tmp_path` fixture:

```python
def test_file_input(tmp_path):
    # Create a temporary markdown file
    md_file = tmp_path / "test.md"
    md_file.write_text("# Test Content")

    # Use the file in your test
    result = process_file(md_file)
    assert result is not None
```

### Markdown File Fixture

Create temporary markdown files with custom content:

```python
def test_convert_file(markdown_file):
    # Creates a temp file with "# Sample Heading" content
    result = convert_file(markdown_file)
    assert "*Sample Heading*" in result
```

## Test Organization

Tests mirror the source structure:

```
tests/
├── conftest.py       # Shared fixtures (markdown_samples, etc.)
├── test_cli.py       # CLI command tests
├── test_converter.py # Converter tests (feature 003)
├── test_tables.py    # Table rendering tests (future)
└── test_slack.py     # Slack API tests (future)
```

## Adding New Fixtures

Add shared fixtures to `tests/conftest.py`:

```python
@pytest.fixture
def my_fixture():
    # Setup
    resource = create_resource()
    yield resource
    # Teardown (optional)
    resource.cleanup()
```

Fixtures are automatically available to all test files without import.
