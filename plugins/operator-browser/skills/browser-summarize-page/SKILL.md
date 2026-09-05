---
name: browser-summarize-page
description: Summarize a captured web page in the shape the person needs (the gist, the argument, the numbers, the steps), answer the note they sent with it, and keep the source. Use when a browser capture arrives with a page and a note that asks what it says.
metadata:
  operator:
    capture: browser
    integrations: []
    mcp: [fetch]
    skills: [clear-replies, grounded-citations]
---

# Summarize this page

The most-used thing a browser assistant does. The bar: a person who reads only your summary would not
be surprised by anything in the page, and could say where each claim came from.

## What you receive

- The page in `/app/inbox` as `page-<epoch>.md` (Markdown, scripts stripped) beside the original
  `page-<epoch>.html`. Read the Markdown.
- The job prompt carries the URL, the title, the person's **note** (their question or what they want)
  and any **selection** they highlighted. The selection is what they cared about; start there.

## Do

1. Decide the shape from the note. No note: a five-line gist plus the three most useful specifics.
   "What are the numbers": a table. "How do I": numbered steps. "Is this true": say so and use the
   `grounded-citations` discipline.
2. Read the whole Markdown before writing. Long pages: read to the end; a summary of the first screen
   is a guess.
3. Every specific claim carries a short quote or a section heading from the page in brackets so it
   can be found again. Never cite a section that is not in the file.
4. If the selection is present, answer about the selection first, then the page around it.
5. Note what the page does NOT say when the note asked for it.
6. Do not follow links unless the note asks. If it does, use the `fetch` MCP server and say which
   pages you read.

## Deliver

The summary in the reply (under 250 words unless the note asks for more), then one fenced
`operator-result` block:

```operator-result
{"url": "https://…", "title": "…", "shape": "gist", "keyPoints": ["…"], "answeredNote": true, "notCovered": [], "readWhole": true}
```

## Works with (optional)

- `fetch` MCP server: follow a link the note points at.
- `grounded-citations` skill: strict page-cited answers.
- `clear-replies` skill: keep chat replies short; the long version goes in an artifact.

## Never

Never summarize from the title and the first paragraph. Never add facts the page does not contain.
Never state a paywalled or truncated page as complete; say the file ends mid-way.
