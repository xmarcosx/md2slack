# Prompt: Slack Integration

_For use with /speckit.specify_
_Source: .specify/features/005-slack-integration.md_
_Generated: 2026-01-10_

---

The final piece of md2slack is the ability to post converted content directly to Slack threads. Right now users have to run `md2slack convert`, copy the output, navigate to Slack, find the thread, and paste. The `post` command eliminates all of that by taking a thread URL and a markdown file and handling everything in one invocation.

Users will copy a thread URL directly from Slack (right-click → "Copy link" on any message). These URLs look like `https://yourorg.slack.com/archives/C0123ABCD/p1234567890123456` and encode both the channel ID and thread timestamp. The CLI should parse this URL format transparently so users never need to understand Slack's internal identifiers. The command should also support a `--dry-run` flag that shows exactly what would be posted without actually sending it, since posting to client threads is irreversible.

Authentication uses the `SLACK_BOT_TOKEN` environment variable, which is already set up to work with 1Password via `op run`. The bot needs `chat:write` scope to post, and optionally `chat:write.public` for channels the bot hasn't been invited to. Slack imposes a 40,000 character limit on messages, so the CLI should warn and truncate if the converted content exceeds this. Error messages should be clear and actionable: invalid URL format, missing token, expired token, channel not found, permission denied, and rate limiting all need distinct, helpful feedback. An optional `--prefix` flag lets users prepend text (like "Status Update" headers) before the converted content.
