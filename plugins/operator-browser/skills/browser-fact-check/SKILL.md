---
name: browser-fact-check
description: Check the claims in a captured page or a highlighted passage against primary sources, and report each as supported, contradicted, or unverified, with the evidence. Use when a browser capture's note asks "is this true", "verify", or "fact check".
metadata:
  operator:
    capture: browser
    integrations: [tavily, exa, firecrawl]
    mcp: [fetch]
    skills: [cited-sources, grounded-citations, clear-replies]
---

# Fact-check this

People send a page with "is this true?" more than any other question. The answer is a verdict per
claim, with the source that decides it, and an honest "could not verify" where nothing does.

## What you receive

- `page-<epoch>.md` in `/app/inbox`: the page.
- The job prompt: URL, title, the **selection** (the passage to check, when highlighted) and the
  **note**.

## Do

1. Extract the checkable claims: statements of fact with a number, a date, a name, a cause, a quote.
   Opinions and predictions are listed as "not checkable". With a selection, check only that.
2. For each claim, find a primary source: the original report, the dataset, the statute, the
   transcript, the company's own page. Search with `TAVILY_API_KEY`, `EXA_API_KEY` or
   `FIRECRAWL_API_KEY` when present; otherwise the `fetch` MCP server on the sources the claim itself
   names. Secondary coverage supports a verdict only when the primary is unreachable, and is marked so.
3. Verdict per claim: `supported`, `contradicted`, `partly` (number or date off; say by how much),
   `unverified`. Quote the deciding sentence from the source with its URL.
4. Note the page's own sourcing: does it link to what it claims, and does the link say that?
5. Overall: one line on how much of the page holds up, without a percentage unless every claim was
   checked.

## Deliver

Reply with the claims table, then one fenced `operator-result` block:

```operator-result
{"url": "https://…", "claims": [{"claim": "…", "verdict": "supported", "source": "https://…", "quote": "…"}], "counts": {"supported": 3, "contradicted": 1, "partly": 1, "unverified": 2}, "notCheckable": 2}
```

## Works with (optional)

- `fetch` MCP server: read the sources.
- `tavily` / `exa` / `firecrawl` integrations: find primary sources fast.
- `cited-sources` / `grounded-citations` skills: the citation discipline.
- `clear-replies` skill: the chat reply is the counts and the worst finding; the table is the artifact.

## Never

Never mark a claim supported because it sounds plausible or appears on several sites. Never treat the
page as its own source. Never hide an unverified claim in a "mostly true".
