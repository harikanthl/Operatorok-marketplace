---
name: literature-search
description: Find papers, benchmarks and their code through the Papers with Code catalog.
---

HARD RULE, applies to every character you output including tables, headings, and chart labels: NEVER write an em dash or an en dash. Not one. Use a comma, a colon, a period, or parentheses instead. If you catch yourself reaching for one, rewrite the sentence.

When the question is about research, machine learning, or the state of the art, search the curated literature BEFORE searching the open web. A web search returns what is written about a paper. This returns the paper, its benchmark numbers, and the code that implements it.

Use the public Papers with Code API at https://paperswithcode.co/api/v1. Reads are anonymous: no key, no account, no login. Call it with the tools you already have (curl, or httpx in Python). Send a User-Agent header, because requests without one are refused by the CDN.

The endpoints worth knowing:

- GET /papers/search?q=<query>&limit=10 finds papers by title, abstract or author.
- GET /papers/{arxiv_id} returns one paper's metadata. The id is the bare arXiv number, for example 2501.09136.
- GET /research/papers/{arxiv_id}/read returns the paper already converted to Markdown. Prefer this over downloading and parsing a PDF yourself: it is somebody else's careful parse, and it is the same bytes every time you ask.
- GET /research/papers/{arxiv_id}/lineage returns what a paper built on and what has since built on it. This is how you find out whether a result was superseded, which a search alone will not tell you.
- GET /papers/{arxiv_id}/repositories returns the code that implements the paper.
- GET /tasks/{task_id}/trending-benchmarks and GET /evaluations/ return leaderboards with real numbers, so you can say what is state of the art instead of guessing.
- GET /papers/trending and GET /papers/recent are for "what is new in X", not for answering a specific question.

How to use it well:

Search, then READ. A title and abstract are not evidence. Pull the Markdown for any paper you intend to cite and quote from what it actually says.

Check the lineage before you call anything current. A paper from eighteen months ago with four follow-ups that beat it is a historical note, not a recommendation, and reporting it as the state of the art is the most common way this work goes wrong.

When you name a number, name where it came from: the benchmark, the dataset split, and the paper. An accuracy figure with no benchmark attached is not a fact a reader can check.

Cite by arXiv id and title, so the reader can open the same page you read.

If the catalog returns nothing useful, say so and fall back to the open web. It covers machine learning and adjacent fields well and other subjects barely at all. Reporting an empty result honestly is correct; inventing a paper to fill the gap is not.
