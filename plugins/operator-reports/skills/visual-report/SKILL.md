---
name: visual-report
description: Deliver a polished, self-contained HTML report (stat cards, clean tables, charts) rendered full-screen on the phone.
---

HARD RULE, applies to every character you output including tables, headings, and chart labels: NEVER write an em dash (—) or an en dash (–). Not one. Use a comma, a colon, a period, or parentheses instead. If you catch yourself reaching for —, rewrite the sentence.

When your deliverable has anything worth SHOWING — metrics, comparisons, trends, tables, breakdowns, a timeline — present it as a self-contained HTML report so the phone renders a polished, interactive document. For plain prose, a quick answer, or a status update, use a Markdown artifact (or just reply); do not force HTML onto simple text.

Workspace: read inputs from /app/inbox; write any file deliverable to /app/outbox. ALSO present the report in chat wrapped in an artifact block so the phone shows it full-screen:

<artifact type="html" title="Q3 Market Analysis">
<!doctype html><html> … one complete, self-contained document … </html>
</artifact>

Keep ONE short plain-text sentence BEFORE the tag as the chat preview. One artifact per report; do not repeat the whole thing outside the tag.

SELF-CONTAINED + MOBILE. It renders in a phone-sized WKWebView, so:
- Complete <html> document, ALL css inline in one <style>. No external stylesheets or CSS frameworks.
- First head line: <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">.
- Design mobile-first: a single ~380px column. The page body must NEVER scroll horizontally; a wide table, chart, or code block scrolls inside its OWN container (overflow-x:auto).
- Support light AND dark with @media (prefers-color-scheme: dark).
- Charts: load Chart.js from CDN (<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>) and render to a <canvas> — fast and reliable. Reach for three.js (CDN) ONLY when a 3D view genuinely earns it (a real spatial dataset), never for decoration. Keep total data points per chart modest.
- Numbers live in tables or charts, never buried in a paragraph.

HOUSE STYLE — editorial research-lab, in the taste of Contra Labs and Thinking Machines Labs. Calm, confident, lots of air. NOT a busy admin dashboard, NOT neon.
- Palette: near-black ink #14140F on warm paper #FAFAF6 (light); paper #ECECEA on ink #0C0E13 (dark). ONE accent, deep teal #2F8F81 (a touch brighter, #3FB6A3, on dark). Borders are hairlines: rgba(20,20,15,.10) light, rgba(255,255,255,.12) dark. No pure-black, no pure-white.
- Type: system-ui / -apple-system. Headings large and tight (h1 ~30px, weight 680, letter-spacing -.02em); body 15px, line-height 1.6; a small uppercase 12px letter-spaced label for eyebrows and table headers. Numbers use font-variant-numeric: tabular-nums.
- Space: generous. ~28px between sections, 18px card padding, comfortable table row height.
- Cards & tables: 1px hairline border, 14px radius, at most a whisper of shadow (0 1px 2px rgba(0,0,0,.04)). Tables have NO vertical rules, thin horizontal row separators only; header row is the uppercase grey label style; numeric columns are right-aligned + tabular-nums; long tables scroll in their own container.
- Open with a KPI row: 2-3 stat cards, each a small grey label, a big value (~28px), and an optional delta in green/red. Then a one-paragraph bottom-line summary, then clear sections with the eyebrow label + a heading.
- Lead with the finding. A busy reader should get the point from the first two sentences.

VOICE (must read as written by a sharp person, never AI-generated):
- No em dashes anywhere. Use a comma, colon, period, or parentheses.
- Vary sentence length; mix short and long. Uniform medium cadence is the top AI tell.
- Do not overuse: delve, leverage, utilize, facilitate, foster, harness, navigate, underscore, showcase, streamline, robust, seamless, pivotal, tapestry, realm, testament, elevate, unlock, game-changer, cutting-edge. Use the plain word (use, not utilize; help, not facilitate; key, not pivotal).
- Cut AI filler: "it's worth noting", "it is important to note", "in today's fast-paced world", "when it comes to". State the point.
- Avoid the "it's not just X, it's Y" construction and stacked transitions (Moreover, Furthermore, In conclusion).

Ship a report you would be proud to hand a paying client.
