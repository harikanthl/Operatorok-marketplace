---
name: dev-release-notes
description: Build human-readable release notes from a git range or a milestone, grouped into What's New, Improvements, Fixes, Security, Breaking, Docs and Acknowledgements, ready to paste into a release. Use when the person names a range like v1.2.0..HEAD or a milestone.
metadata:
  operator:
    integrations: [github]
    mcp: []
    skills: [clear-replies]
    derivedFrom: OnlyTerp/hermes-optimization-guide skills/dev/release-notes (MIT)
---

# Release notes

## What you receive

- A repository under `/app/work` and, in the job prompt, a git range (`X..Y`) or a GitHub milestone
  name. A range is read with `git log --pretty='%H%x00%s%x00%b%x00%an' X..Y`; a milestone needs the
  `github` integration and its closed PRs.

## Do

1. For each commit or PR take the type from its Conventional Commits prefix (`feat`, `fix`,
   `perf`, `refactor`, `docs`, `security`, `chore`), the scope in parentheses, the summary, the
   body, and the author.
2. Group: **What's New** (`feat`, scope not `ci|deps|docs`), **Improvements** (`perf`,
   `refactor`), **Fixes** (`fix`), **Security** (`security` or a `security` label),
   **Breaking** (a `!` marker or a `breaking` label), **Docs** (`docs`),
   **Acknowledgements** (authors who are not repo members, when the integration can tell).
3. Rewrite every summary as a sentence a user reads, not a commit message:
   `feat(mcp): add http transport with reconnect backoff` becomes
   `HTTP MCP servers now reconnect automatically with exponential backoff.`
4. Link PRs `([#1234](https://github.com/owner/repo/pull/1234))` when the number is known.
5. Write `/app/outbox/release-notes-<range>.md`. Empty groups are omitted.

## Deliver

The notes in the reply, then:

```operator-result
{"range": "v1.2.0..HEAD", "commits": 48, "groups": {"new": 9, "improvements": 6, "fixes": 20, "security": 1, "breaking": 0, "docs": 5}, "file": "release-notes-v1.2.0..HEAD.md"}
```

## Works with (optional)

- `github` integration: read a milestone's PRs; publish the release after the person approves it.

## Never

Never publish a release or tag anything. Never describe a change the commit does not describe.
Never drop a `!` breaking marker into Improvements because the sentence read better there.
