---
name: glasses-receipts-to-expenses
description: Turn glasses photos of receipts, invoices and price tags into expense lines with vendor, date, total, tax and category, checked against the photo, ready for a spreadsheet or accounting system. Use when a capture holds a receipt or a bill.
metadata:
  operator:
    capture: glasses
    integrations: [quickbooks, airtable]
    skills: [xlsx, document-pipeline, clear-replies]
---

# Receipts to expenses

Glance at the receipt, it is filed. The trick is that an expense line with one wrong digit is worse
than no line, so every field carries the photo it came from and a confidence.

## What you receive

- Photos in `/app/inbox` with the `_collection.json` sidecar (time and gps tell you when and roughly
  where the purchase was). Read them via `OPERATOR_CAPABILITY_URL` (`vision.semantic`, `mediaPaths`,
  bearer `$OPERATOR_INGEST_TOKEN`): ask for vendor name, address line, date and time, line items,
  subtotal, tax lines, total, currency, payment method and last four digits, exactly as printed.
- If the `docpipe` harness is present (`/usr/local/bin/docpipe`), use the `document-pipeline` skill
  instead of free reading; it gives provenance per field.
- The job prompt may name the expense categories in use and the person's default currency.

## Do

1. One expense per receipt. Fields: vendor, date, currency, total, tax, category, payment, photo id,
   and a confidence per field (0 to 1) from how clearly it was printed and read.
2. Check the arithmetic: line items plus tax should equal the total. A mismatch is reported, not
   silently corrected; the total as printed wins.
3. Category from the vendor and items, using the person's list when given, else a short default list
   (meals, travel, supplies, fuel, lodging, other).
4. A receipt that is cut off, faded or folded gets `needsReview: true` and a one-line reason.
5. Same vendor, same total, same day twice: flag the second as a possible duplicate.

## Deliver

Reply with a table of the expenses, then one fenced `operator-result` block:

```operator-result
{"expenses": [{"vendor": "Shell Kings Rd", "date": "2026-09-05", "currency": "GBP", "total": 62.40, "tax": 10.40, "category": "fuel", "payment": "card 4421", "photo": "IMG_1001.jpg", "confidence": {"total": 0.98, "date": 0.9}, "needsReview": false}], "duplicates": [], "arithmeticMismatches": []}
```

Also write `expenses.csv` beside the reply with the same rows, one per line.

## Speaking to the glasses

Guidance card: `{"title": "£62.40 fuel, filed", "detail": "Shell, card 4421", "speak": true, "action": "none"}`.
A receipt that needs review says so: `{"title": "Receipt unclear", "detail": "Retake, flat and in light", …}`.

## Works with (optional)

- `xlsx` skill: an expenses workbook instead of CSV.
- `airtable` integration (`AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`): one row per expense in a shared base.
- `quickbooks` integration (`QUICKBOOKS_CLIENT_ID`, `QUICKBOOKS_CLIENT_SECRET`): create the expense there, only when the person asks.
- `document-pipeline` skill: provenance-tagged extraction when the harness is available.

## Never

Never invent a digit. Never change a printed total to make the arithmetic work. Never post to an
accounting system without being told to.
