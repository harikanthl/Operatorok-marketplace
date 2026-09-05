---
name: browser-translate-page
description: Translate a captured page or a highlighted passage faithfully into the person's language, keeping structure, numbers, names and terms of art, with the source kept beside hard passages. Use when a browser capture is in another language or the note says translate.
metadata:
  operator:
    capture: browser
    integrations: []
    skills: [clear-replies, grounded-citations]
---

# Translate this page

Page translation is one of the most-used browser features anywhere. The machine version is fine for
gist and wrong for contracts, forms, prices and instructions. This one is for when the wrong kind
of wrong would cost something.

## What you receive

- `page-<epoch>.md` in `/app/inbox`: the page as Markdown (headings, lists, tables preserved).
- The job prompt: URL, title, the **selection** (translate only this, when present), and the
  **note** (target language, register, or a domain: "legal", "medical", "it's a rental contract").

## Do

1. Target language from the note; otherwise the language the person writes in. Say which you chose.
2. Translate the selection when there is one; otherwise the main content, skipping navigation,
   cookie banners and comments unless the note asks for them.
3. Keep the structure: headings stay headings, tables stay tables, numbered steps stay numbered.
   Numbers, dates, currencies, units, proper nouns, product names and code stay exactly as written;
   dates get the target locale's format in brackets when the order could mislead.
4. Terms of art (legal, medical, technical) are translated with the standard term and the original
   in brackets on first use.
5. Passages that carry obligations or risk (deadlines, fees, penalties, consent, dosage) are marked
   with `!` and shown source-beside-translation so a person can check them.
6. Ambiguity is stated, not resolved silently: "(could also mean …)".

## Deliver

The translation in the reply (or as `translation-<slug>.md` when over a screen), then one fenced
`operator-result` block:

```operator-result
{"url": "https://…", "sourceLanguage": "de", "targetLanguage": "en", "scope": "selection", "words": 640, "flagged": 3, "ambiguous": 1, "file": "translation-….md"}
```

## Works with (optional)

- `grounded-citations` skill: when the person then asks questions about the translated page, answer
  only from it.
- `clear-replies` skill: keep the chat reply to the summary line; the translation is the artifact.

## Never

Never smooth a clause into a friendlier meaning. Never change a number or a date. Never translate a
name. Never drop a sentence because it was hard.
