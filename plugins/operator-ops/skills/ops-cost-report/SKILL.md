---
name: ops-cost-report
description: Turn a usage export into a cost report by Solution, model and day, with anomalies flagged by a median rule rather than a hunch. Use when the person asks what they are spending, after a spike, or on a weekly schedule with a usage export staged in the inbox.
metadata:
  operator:
    integrations: [airtable, resend]
    mcp: []
    skills: [xlsx, structured-report, clear-replies]
    derivedFrom: OnlyTerp/hermes-optimization-guide skills/ops/cost-report (MIT)
---

# Cost report

A bill that arrives as one number is a bill nobody can act on. Split it three ways and say which
day and which job moved it.

## What you receive

- A usage export in `/app/inbox`: `usage-*.json` or `usage-*.csv`, one row per run, with at least
  `at`, `solution`, `job`, `model`, `tokensIn`, `tokensOut`, `costUSD`. Operator's own export
  (Sessions → Usage → Export) has exactly these columns. Cache columns (`cacheRead`,
  `cacheWrite`) are optional and, when present, are reported.
- The job prompt may name a window (`7d`, `30d`) and a format (markdown, csv, xlsx). Default:
  seven days, markdown.

## Do

1. Read every row. Drop rows outside the window and say how many you dropped.
2. Three tables: **by Solution**, **by model**, **by day**. Cost, tokens in, tokens out, run count;
   each sorted by cost. When cache columns exist, add the cached share per model: a model that
   should be caching and is not is the cheapest fix on the page.
3. **Anomalies.** Daily spend that exceeds three times the median absolute deviation of the window
   is flagged, with the Solution and job that drove it named from the rows, not guessed.
4. **The three cheapest changes**, each a sentence with the number it would save: a job on a
   frontier model that never uses tools, a run count that doubled, a model with no cache reads.
5. Write the report to `/app/outbox/cost-report-<window>.md` (and `.csv`/`.xlsx` if asked, via the
   `xlsx` skill).

## Deliver

The four tables and the anomalies in the reply, under 300 words of prose around them, then:

```operator-result
{"window": "7d", "totalUSD": 25.53, "rows": 412, "dropped": 3, "bySolution": [{"id": "…", "usd": 0}], "anomalies": [{"day": "2026-09-03", "usd": 9.8, "driver": "weekly-dep-audit"}], "report": "cost-report-7d.md"}
```

## Works with (optional)

- `resend` integration: mail the report on a schedule, only when the job prompt says to.
- `airtable` integration: append the by-day rows to a base the person names.
- `structured-report` skill: the same numbers as a printable PDF.

## Never

Never state a cost that is not the sum of rows you read. Never invent a driver for a spike; if the
rows do not say, say the day is unexplained. Never mail or post anything the prompt did not ask for.
