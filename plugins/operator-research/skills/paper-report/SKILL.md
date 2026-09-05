---
name: paper-report
description: Deliver longform research as a self-contained HTML paper: masthead, abstract, numbered figures, references.
---

HARD RULE, applies to every character you output including tables, headings, figure captions and chart labels: NEVER write an em dash or an en dash. Not one. Use a comma, a colon, a period, or parentheses instead. If you catch yourself reaching for one, rewrite the sentence.

Use this when the deliverable is meant to be READ start to finish: a research report, a reproduction write-up, a literature review, an analysis someone will sit with. It is a paper, not a dashboard. If the deliverable is really a metrics summary or a status update, do not force this shape onto it.

DELIVERY, BOTH WAYS. Read inputs from /app/inbox. Write the file to /app/outbox, which is the only writable output dir, AND present the same document in chat wrapped in an artifact block so the phone renders it full screen:

<artifact type="html" title="Reproducing Sparse Attention at Scale">
<!doctype html><html> ... one complete, self-contained document ... </html>
</artifact>

Keep ONE short plain-text sentence before the tag as the chat preview. Do not repeat the document outside the tag. One artifact per deliverable.

SELF-CONTAINED AND MOBILE. It renders in a phone-sized WKWebView.

- A complete <html> document with ALL css inline in one <style>. No external stylesheets, no CSS frameworks, no web fonts.
- First line in head: <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">.
- The body must NEVER scroll horizontally. A wide table, code block or figure scrolls inside its OWN container with overflow-x:auto.
- Support light AND dark with @media (prefers-color-scheme: dark).
- Prefer a table or hand-written inline SVG over a charting library. If a trend genuinely needs a chart, Chart.js from CDN is allowed, but the same numbers must ALSO appear in a table, because the phone may render this with no network and a blank canvas is not a result.

THE SHAPE OF THE PAGE, in order.

1. Masthead. A small uppercase eyebrow (the job, for example REPRODUCTION or RESEARCH REPORT), then the title, then a one-line deck saying what the reader is about to learn. Under a hairline rule, a metadata line in small grey caps: the source (paper title and arXiv id, or the topic), the date, and where it ran (hardware, wall clock, approximate cost).
2. The bottom line, in one paragraph, set slightly larger than body text. Outcome first. A reader who stops here should still have the answer.
3. The scope table when the work was bounded, immediately after the bottom line, so the reader learns the limits before the findings rather than after.
4. Sections. Each opens with a small uppercase eyebrow and an h2. Longform prose, not bullet soup: use paragraphs for reasoning and reserve lists for things that are genuinely enumerable.
5. Figures and tables are NUMBERED and CAPTIONED (Figure 1, Table 2), captions below figures and above tables, and every one is referred to by number from the prose. An uncaptioned figure is decoration.
6. Conclusion, stating what would change the answer.
7. References, numbered, each with title and arXiv id or URL, matching superscript markers in the text.

HOUSE STYLE, an editorial research paper: warm paper, dark ink, one accent, lots of air.

- Palette: ink #14140F on paper #FAFAF6 in light; paper #ECECEA on ink #0C0E13 in dark. ONE accent, deep teal #2F8F81 (#3FB6A3 on dark), used for links, the eyebrow rules and nothing else. Hairline borders rgba(20,20,15,.10) light, rgba(255,255,255,.12) dark. No pure black, no pure white, no second accent.
- Measure: one column, max-width 34rem, centred, with 20px side padding. Long reading lines are the point; do not stretch to full width.
- Type: body in a serif stack (Iowan Old Style, Palatino, Georgia, serif) at 17px with line-height 1.65, because this is a document you read rather than scan. Headings and all UI furniture in system-ui, tight and heavy (h1 ~31px weight 660 letter-spacing -.02em, h2 ~21px weight 640). Eyebrows and table headers 11px uppercase letter-spacing .08em in grey. Numbers everywhere use font-variant-numeric: tabular-nums.
- Space: ~34px between sections, 1.1em between paragraphs, no double rules and no boxes around prose.
- Tables: hairline border, 12px radius, NO vertical rules, thin horizontal separators only, header row in the uppercase grey label style, numeric columns right-aligned, long tables scroll in their own container.
- Verdict words (VERIFIED, TOY, FALSIFIED, INCONCLUSIVE and the like) render as small uppercase pills with a hairline border, not as coloured blocks. Colour at most the accent and a muted red; never a traffic-light row.
- Code and commands in a mono stack at 13px on a faintly tinted panel, in their own scroll container.
- At most one pull quote, for the single finding the whole document exists to deliver. If nothing deserves it, use none.

VOICE, must read as written by a sharp person and never as generated text.

- No em dashes anywhere. Use a comma, a colon, a period, or parentheses.
- Lead with the finding. A busy reader should have the point inside two sentences.
- Vary sentence length, mixing short and long. A run of similar medium-length sentences is the top tell.
- Do not use: delve, leverage, utilize, facilitate, foster, harness, navigate, underscore, showcase, streamline, robust, seamless, pivotal, tapestry, realm, testament, elevate, unlock, game-changer, cutting-edge. Use the plain word.
- Cut filler: "it's worth noting", "it is important to note", "when it comes to", "in today's fast-paced world". State the point.
- Avoid the "not just X, it's Y" construction and stacked transitions (Moreover, Furthermore, In conclusion).
- Never describe a number without saying where it came from.

Ship something a reader would finish on a train and forward to a colleague.
