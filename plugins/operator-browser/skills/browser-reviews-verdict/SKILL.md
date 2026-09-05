---
name: browser-reviews-verdict
description: Read the reviews on a captured product, app, restaurant or service page, separate the recurring complaints from the praise, weigh review quality, and give a buy or skip verdict with the deciding reasons. Use when a browser capture is a page with reviews and the note asks "should I".
metadata:
  operator:
    capture: browser
    integrations: [firecrawl, tavily]
    mcp: [fetch]
    skills: [clear-replies]
---

# Reviews verdict

"Should I buy this" from a page of two hundred reviews. The answer is what keeps coming up, how much
to trust it, and a verdict the person can disagree with because the reasons are on the table.

## What you receive

- `page-<epoch>.md` in `/app/inbox`: the page, including whatever reviews were loaded when captured.
- The job prompt: URL, title, the **note** (what the person cares about: "for a small kitchen",
  "for a 6-year-old", "battery life") and any **selection**.

## Do

1. Count what you actually have: reviews visible, rating distribution if shown, date range. A page
   with six reviews loaded gets a verdict marked "thin evidence".
2. Themes: the recurring complaints and the recurring praise, each with a count and one representative
   quote. A theme mentioned once is not a theme.
3. Trust: flag signs of low-quality reviews (identical phrasing, all five stars in one week,
   unverified purchases where the page marks them) and say how much weight you removed.
4. Match to the note: which themes bear on what the person cares about. A great product for the
   wrong reason is a skip.
5. If the note asks, or the evidence is thin, use the `fetch` MCP server (or `FIRECRAWL_API_KEY` /
   `TAVILY_API_KEY` search) for one independent review or test, and say whose.
6. Verdict: `buy`, `skip`, or `depends` with the one condition that decides it.

## Deliver

Reply with the themes table and the verdict, then one fenced `operator-result` block:

```operator-result
{"url": "https://…", "item": "…", "reviewsRead": 48, "rating": 4.3, "complaints": [{"theme": "strap breaks", "count": 9}], "praise": [{"theme": "battery", "count": 21}], "trust": "moderate", "verdict": "depends", "condition": "if you will not carry it daily", "independent": "https://…"}
```

## Works with (optional)

- `fetch` MCP server: one independent review when the page's are thin.
- `firecrawl` / `tavily` integrations: find that review quickly.
- `clear-replies` skill: verdict and the deciding reason in the chat; the table is the artifact.

## Never

Never give a confident verdict on a handful of reviews. Never count a one-off as a theme. Never
buy or add to cart.
