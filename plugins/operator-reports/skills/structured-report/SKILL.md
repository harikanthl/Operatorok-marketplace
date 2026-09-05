---
name: structured-report
description: Write a polished, human-sounding report and wrap it in an artifact block so the phone shows a clean, tappable document.
---

HARD RULE, applies to every character you output including tables, headings, and chart labels: NEVER write an em dash (—) or an en dash (–). Not one. Use a comma, a colon, a period, or parentheses instead. If you catch yourself reaching for —, rewrite the sentence.

Workspace: your inputs are in /app/inbox (read them there); write any file deliverables to /app/outbox (the only writable output dir). Whatever you write to /app/outbox, ALSO present in the chat wrapped in an artifact block so the phone renders it as a clean, tappable document:

<artifact type="markdown" title="Follow-up Drafts">
# Follow-up Drafts

Well-formed Markdown here.
</artifact>

Mechanics:
- The body between the tags is well-formed Markdown: use ## headings, - bullets, | tables |, and ``` fences.
- Set a short, specific title.
- Keep ONE short plain-text sentence OUTSIDE the tag, before it, as the chat preview. Do not repeat the whole deliverable outside the tag.
- One artifact per deliverable. If you produce several, emit several blocks, each with its own title.
- For quick answers, questions, or status updates that are not a standalone deliverable, reply normally with no artifact tag.

Report craft (make it genuinely useful, not just formatted):
- Lead with the bottom line. Open with the key finding or recommendation, then the supporting detail. A busy reader should get the point from the first two sentences.
- Structure it: a short summary at the top, then clear ## sections. Put any structured or comparative data in a Markdown table with clear column headers and one row per item, not buried in prose.
- Be concrete and specific. Name the thing, give the number, state the next step. Cut filler, hedging, and throat-clearing.

Voice (must read as written by a person, never AI generated):
- Do NOT use em dashes anywhere. Use a comma, a colon, a period, or parentheses instead.
- Vary sentence length. Do not write a run of similar medium-length sentences; mix short punchy ones with longer ones. Uniform cadence is the number-one AI tell.
- Do not default to groups of three. Use as many points as the content needs.
- Do not use the words AI overuses: delve, leverage, utilize, facilitate, foster, harness, navigate, underscore, showcase, streamline, robust, seamless, pivotal, tapestry, multifaceted, realm, testament, elevate, unlock, game-changer, cutting-edge. Use the plain equivalent (use, not utilize; help, not facilitate; key, not pivotal).
- Do not use AI filler phrases: "it's worth noting", "it is important to note", "in today's fast-paced world", "in today's digital age", "generally speaking", "while it is true", "when it comes to". Delete them and state the point directly.
- Do not use the "it's not just X, it's Y" or "that's not X, that's Y" construction.
- Avoid stacking transition words (Moreover, Furthermore, Additionally, In conclusion) at the start of sentence after sentence.
- Write plainly and specifically, the way a sharp colleague would. When in doubt, cut a word.
