---
name: sec-audit-mcp
description: Audit every MCP server a workspace or a bot is wired to, with a risk flag per server, what it can reach, what credentials it holds, and how stale it is. Use weekly, after adding a server, or before widening a server's tools. Read-only; changes are proposed, never made.
metadata:
  operator:
    integrations: []
    mcp: [fetch]
    skills: [structured-report, clear-replies]
    derivedFrom: OnlyTerp/hermes-optimization-guide skills/security/audit-mcp (MIT)
---

# MCP audit

## What you receive

- The servers to audit, in one of three places: the job prompt's list; a `.mcp.json` in the
  workspace (the Claude Code plugin format); or the servers attached to this bot, which Operator
  lists in `/app/inbox/_mcp.json` when the job stages them.

## Do

1. For each server record: name; transport (`stdio` with a command, or `http` with a URL);
   enabled; tool filters (an include list, an exclude list, or none); the env var names it is
   given (names only, never values); its source (npm package, git URL, or HTTP origin); and how
   stale it is: `npm view <pkg> time.modified`, `git log -1 --format=%cI`, or a `HEAD` request's
   `Last-Modified` through the `fetch` MCP server.
2. Flag:
   - **HIGH** the server ingests untrusted content (tool names matching `scrape|fetch|email|rss|
     crawl|browse`) and has no tool filter;
   - **HIGH** it holds a credential env var whose name suggests write scope (`*_ADMIN_*`,
     `*_WRITE_*`, a PAT) while its tools include reads only;
   - **MEDIUM** no update in ninety days; a `latest` tag with no pin; an HTTP server without TLS;
   - **LOW** everything else, stated as such.
3. For each HIGH, one proposed change: the exact include list, or the narrower credential. A
   proposal is text in the report; nothing is edited.
4. Write `/app/outbox/mcp-audit.md`.

## Deliver

The flagged servers in the reply, then:

```operator-result
{"servers": 6, "high": 1, "medium": 2, "low": 3, "findings": [{"server": "…", "flag": "HIGH", "why": "…", "proposal": "…"}], "report": "mcp-audit.md"}
```

## Never

Never read or print a credential value. Never change a server's config. Never call a server's
tools to "test" it; the audit is of its configuration, not its behaviour.
