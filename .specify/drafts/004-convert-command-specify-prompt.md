# Prompt: Convert Command

_For use with /speckit.specify_
_Source: .specify/features/004-convert-command.md_
_Generated: 2026-01-10_

---

The convert command is the preview mechanism for md2slack, allowing users to see exactly what their markdown will look like after conversion to Slack's mrkdwn format before posting to a thread. This directly supports Constitution Principle IV (Preview Before Commit) since posting to client threads is irreversible and users need confidence before committing.

The command should be invoked as `md2slack convert --file <path>` and simply read the markdown file, run it through the existing converter module (feature 003), and print the converted mrkdwn to stdout. This is intentionally a thin wrapper with no additional processing - what you see is exactly what would get posted.

For error handling, the command should exit 0 on success with converted content on stdout, and exit 1 with a clear error message on stderr for failure cases like file not found or permission denied. Per Principle V (Professional Output), error messages should be actionable - tell the user what went wrong and what they can do about it. The MVP keeps it minimal with just the --file option; stdin support and other conveniences can come later.
