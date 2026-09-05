---
name: browser-fill-form
description: Prepare the answers for a captured web form (application, registration, quote request, government portal) from the person's own profile and documents, field by field, as a checklist they paste in. Never submits. Use when a browser capture is a form page.
metadata:
  operator:
    capture: browser
    integrations: []
    mcp: [filesystem]
    skills: [docx, pdf, clear-replies]
---

# Fill this form (on paper first)

Form filling is what people want automated most and trust least. So the work product is the filled
form as a checklist: every field, the answer, and where the answer came from. The person pastes and
submits. You do not touch the page.

## What you receive

- `page-<epoch>.md` and `page-<epoch>.html` in `/app/inbox`: read the HTML for the form's fields
  (labels, names, types, required marks, options in selects, character limits).
- The job prompt: URL, title, the **note** (context: "for the London flat", "use my work address")
  and any **selection**.
- The person's profile and documents when attached in `/app/inbox` (a profile Markdown, a CV, a
  passport scan). Read them with the `filesystem` MCP server or directly. A field with no source
  in those files has no answer; it is left for the person, not invented.

## Do

1. List every field in page order: label, type, required, options or limit.
2. For each field, the answer and its source ("profile.md: address", "cv.pdf: employer 2023"). Long
   answers (cover letters, "why do you want this") are drafted from the person's documents and the
   page's own description, and marked DRAFT.
3. Fields you cannot answer are listed under "You need to fill", with what kind of answer they want.
4. Consistency check: dates in the page's format, phone in the country's format, names spelled as in
   the documents, character limits respected with the count shown.
5. Anything that is a declaration, a signature, a payment or a legal consent goes under "Read before
   you tick", with the text quoted.

## Deliver

Reply with the checklist, then one fenced `operator-result` block:

```operator-result
{"url": "https://…", "form": "…", "fields": 23, "answered": 19, "needsYou": ["National insurance number"], "declarations": 2, "checklist": "form-answers.md"}
```

## Works with (optional)

- `filesystem` MCP server: the person's profile and documents.
- `pdf` / `docx` skills: read a CV or a scanned document for answers.
- `clear-replies` skill: keep the chat reply to the counts; the checklist is the artifact.

## Never

Never submit, click, or type into the page. Never invent an answer for a field with no source. Never
tick a consent on the person's behalf, in prose or in fact.
