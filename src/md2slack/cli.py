"""CLI entry point for md2slack."""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import click

from md2slack.chunker import DEFAULT_CHUNK_SIZE, MIN_CHUNK_SIZE, chunk_content
from md2slack.converter import convert as convert_markdown
from md2slack.slack import (
    SlackClient,
    SlackError,
    get_token,
    parse_thread_url,
)


def parse_line_range(
    ctx: click.Context, param: click.Parameter, value: str | None
) -> tuple[int, int] | None:
    """Parse --lines option value in START-END format.

    Args:
        ctx: Click context
        param: Click parameter
        value: String in "START-END" format (e.g., "10-50")

    Returns:
        Tuple of (start, end) line numbers (1-indexed), or None if value is None

    Raises:
        click.BadParameter: If format is invalid, start > end, or non-positive
    """
    if value is None:
        return None

    # Match START-END format (digits-digits)
    match = re.match(r"^(\d+)-(\d+)$", value)
    if not match:
        raise click.BadParameter(
            f"Invalid --lines format '{value}'. "
            "Expected START-END (e.g., --lines 10-50)."
        )

    start = int(match.group(1))
    end = int(match.group(2))

    # Validate positive values (1-indexed)
    if start <= 0 or end <= 0:
        raise click.BadParameter(
            f"Invalid line range '{value}'. Line numbers must be positive (1-indexed)."
        )

    # Validate start <= end
    if start > end:
        raise click.BadParameter(
            f"Invalid line range '{value}'. "
            "Start line must be less than or equal to end line."
        )

    return (start, end)


def extract_lines(content: str, start: int, end: int) -> str:
    """Extract a range of lines from content.

    Args:
        content: The full content string
        start: First line to include (1-indexed)
        end: Last line to include (1-indexed, inclusive)

    Returns:
        String containing only the specified lines
    """
    lines = content.splitlines(keepends=True)
    # Convert to 0-indexed, end is inclusive so we use end (not end-1)
    selected = lines[start - 1 : end]
    return "".join(selected)


def validate_line_range(
    start: int, end: int, total_lines: int, source: str = "File"
) -> None:
    """Validate that line range is within bounds of the content.

    Args:
        start: First line number (1-indexed)
        end: Last line number (1-indexed)
        total_lines: Total number of lines in the content
        source: Description of input source for error message (e.g., "File", "Input")

    Raises:
        click.ClickException: If range extends beyond total line count
    """
    if start > total_lines or end > total_lines:
        raise click.ClickException(
            f"Line range {start}-{end} is out of bounds. "
            f"{source} has {total_lines} lines (valid range: 1-{total_lines})."
        )


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """md2slack - Convert markdown to Slack mrkdwn and post to threads."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument(
    "file",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    required=False,
)
@click.option("--text", "-t", help="Markdown text to convert (alternative to file)")
@click.option(
    "--lines",
    "-l",
    callback=parse_line_range,
    help="Extract only specified line range (1-indexed, inclusive). Format: START-END",
)
def convert(
    file: str | None, text: str | None, lines: tuple[int, int] | None
) -> None:
    """Convert markdown to Slack mrkdwn format.

    Reads markdown from FILE or --text and outputs Slack mrkdwn.
    If no input is provided, reads from stdin.
    """
    # Validate --lines cannot be used with --text
    if lines and text:
        raise click.UsageError("--lines requires file or stdin input, not --text")

    if text:
        markdown = text
    elif file:
        markdown = Path(file).read_text(encoding="utf-8")
        input_source = "File"
    elif not sys.stdin.isatty():
        markdown = sys.stdin.read()
        input_source = "Input"
    else:
        raise click.UsageError("Provide FILE, --text, or pipe markdown to stdin")

    # Extract line range if specified
    if lines:
        start, end = lines
        total_lines = len(markdown.splitlines())
        validate_line_range(start, end, total_lines, input_source)
        markdown = extract_lines(markdown, start, end)

    result = convert_markdown(markdown)
    click.echo(result, nl=False)


@cli.command()
@click.argument(
    "file",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    required=False,
)
@click.option(
    "--thread",
    "-t",
    required=True,
    help="Slack thread URL (copy from Slack)",
)
@click.option(
    "--prefix",
    "-p",
    default=None,
    help="Text to prepend before converted content",
)
@click.option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="Preview output without posting to Slack",
)
@click.option(
    "--chunk-size",
    type=int,
    default=DEFAULT_CHUNK_SIZE,
    help=f"Max chars per chunk (min: {MIN_CHUNK_SIZE}, default: {DEFAULT_CHUNK_SIZE})",
)
@click.option(
    "--lines",
    "-l",
    callback=parse_line_range,
    help="Extract only specified line range (1-indexed, inclusive). Format: START-END",
)
def post(
    file: str | None,
    thread: str,
    prefix: str | None,
    dry_run: bool,
    chunk_size: int,
    lines: tuple[int, int] | None,
) -> None:
    """Post markdown content to a Slack thread.

    Reads markdown from FILE (or stdin), converts to Slack mrkdwn format,
    and posts to the specified thread. Long content is automatically split
    into multiple messages.

    Examples:

      md2slack post --thread "https://org.slack.com/archives/C.../p..." file.md

      cat update.md | md2slack post -t "https://..."

      md2slack post -t "https://..." -p "Weekly Update:" file.md --dry-run
    """
    # Validate chunk-size
    if chunk_size < MIN_CHUNK_SIZE:
        raise click.UsageError(
            f"--chunk-size must be at least {MIN_CHUNK_SIZE} characters"
        )
    # Cap chunk-size at Slack's limit
    chunk_size = min(chunk_size, DEFAULT_CHUNK_SIZE)

    # Read input
    if file:
        markdown = Path(file).read_text(encoding="utf-8")
        input_source = "File"
    elif not sys.stdin.isatty():
        markdown = sys.stdin.read()
        input_source = "Input"
    else:
        raise click.UsageError("Provide FILE or pipe markdown to stdin")

    # Extract line range if specified
    if lines:
        start, end = lines
        total_lines = len(markdown.splitlines())
        validate_line_range(start, end, total_lines, input_source)
        markdown = extract_lines(markdown, start, end)

    # Parse thread URL
    try:
        thread_ref = parse_thread_url(thread)
    except ValueError as e:
        raise click.ClickException(str(e)) from e

    # Convert markdown to mrkdwn
    mrkdwn = convert_markdown(markdown)

    # Apply prefix if provided
    if prefix:
        # Handle escaped newlines in prefix
        prefix_text = prefix.replace("\\n", "\n")
        mrkdwn = prefix_text + mrkdwn

    # Chunk content (always enabled - handles both long and short content)
    chunk_result = chunk_content(mrkdwn, max_size=chunk_size)

    # Display any warnings
    for warning in chunk_result.warnings:
        click.echo(f"Warning: {warning}", err=True)

    # Dry run: show chunks with break markers
    if dry_run:
        click.echo("--- DRY RUN (not posting) ---", err=True)
        for i, c in enumerate(chunk_result.chunks):
            click.echo(c.with_indicator)
            if i < len(chunk_result.chunks) - 1:
                click.echo("--- CHUNK BREAK ---", err=True)
        click.echo("--- END DRY RUN ---", err=True)
        return

    # Get token for posting
    try:
        token = get_token()
    except ValueError as e:
        raise click.ClickException(str(e)) from e

    # Post chunks sequentially
    chunks_posted = 0
    try:
        client = SlackClient(token)
        client.set_workspace(thread_ref.workspace or "slack")

        last_permalink = None

        for i, c in enumerate(chunk_result.chunks):
            if i > 0:
                # Rate limiting: 1 second delay between posts
                time.sleep(1)

            # Progress output to stderr
            if chunk_result.chunk_count > 1:
                click.echo(
                    f"Posting chunk {i + 1}/{chunk_result.chunk_count}...",
                    err=True,
                )

            result = client.post_message(
                channel_id=thread_ref.channel_id,
                thread_ts=thread_ref.thread_ts,
                text=c.with_indicator,
            )
            last_permalink = result["permalink"]
            chunks_posted += 1

        # Success summary
        if chunk_result.chunk_count > 1:
            click.echo(
                f"Posted {chunk_result.chunk_count} chunks to thread: "
                f"{last_permalink}"
            )
        else:
            click.echo(f"Posted to thread: {last_permalink}")

    except SlackError as e:
        # Report partial success on error
        if chunks_posted > 0:
            total = chunk_result.chunk_count
            click.echo(
                f"Error posting chunk {chunks_posted + 1}/{total}: {e.message}",
                err=True,
            )
            click.echo(
                f"Chunks 1-{chunks_posted} posted successfully.", err=True
            )
        raise click.ClickException(f"{e.message}\nHint: {e.hint}") from e
