---
name: glasses-site-inspection
description: Turn a hands-free site walk (glasses photos and clips of rooms, equipment, defects, meters) into a structured inspection report with findings, severities, locations and the photo for each. Use when a capture collection is a walkthrough of a property, plant, vehicle or job site.
metadata:
  operator:
    capture: glasses
    integrations: [airtable, resend]
    skills: [visual-report, structured-report, docx]
---

# Site inspection from a walk

A person walks the site with glasses on, looks at what matters, says a word or two about each thing.
What comes back is the report they would have typed up that evening, with the evidence already
attached.

## What you receive

- Photos and clips in `/app/inbox`, in capture order, with the `_collection.json` sidecar (ids, files,
  times, gps). The order IS the route through the site; keep it.
- Read the pixels via `OPERATOR_CAPABILITY_URL` (`vision.semantic`, `mediaPaths`, bearer
  `$OPERATOR_INGEST_TOKEN`). Ask per photo: what is this, where is it (room or area cues), what is wrong
  if anything, any readable numbers (meter, serial, label).
- The job prompt names the site, the kind of inspection, and any checklist to follow. A checklist in
  `/app/inbox` (PDF, CSV, Markdown) is the frame the findings go into.

## Do

1. Group photos into locations in walk order. Name locations as the person would ("Unit 2 kitchen",
   "Roof, north corner"), never by file name.
2. For each finding: what, where, severity (`info`, `minor`, `major`, `critical`), the photo id, and
   what should happen next. A photo with nothing wrong is still recorded as "inspected, no finding".
3. Read every number you can: meter readings, serials, model plates, dates on labels. Put them in a
   readings table with the photo id.
4. If a checklist was given, mark every item pass, fail, or not seen, and say which photos cover it.
   Items not seen are listed, not silently passed.
5. Write the report: summary of counts by severity, then findings by location, then readings, then
   the checklist, then a "not inspected" list.

## Deliver

Produce the report as an artifact (Markdown; use the `visual-report` skill for an HTML version when
asked), then one fenced `operator-result` block:

```operator-result
{"site": "14 Oak St", "walkStart": "2026-09-05T09:10:00Z", "findings": [{"where": "Unit 2 kitchen", "what": "water staining under sink", "severity": "major", "photo": "IMG_0801.jpg", "next": "plumber to check trap"}], "readings": [{"what": "gas meter", "value": "018432", "photo": "IMG_0790.jpg"}], "checklist": {"pass": 12, "fail": 2, "notSeen": 1}, "report": "inspection.md"}
```

## Speaking to the glasses

During the walk, a guidance card is one line: `{"title": "Kitchen: water staining noted", "detail": "Major. Get a photo of the trap", "speak": true, "action": "none"}`.
Ask for one more photo when one would settle a finding; never more than one at a time.

## Works with (optional)

- `visual-report` / `structured-report` skills: the polished report.
- `docx` skill: a Word version for the client.
- `airtable` integration (`AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`): one row per finding in the team's tracker.
- `resend` integration (`RESEND_API_KEY`, `RESEND_FROM`): send the report, only when the person asks.

## Never

Never assign a severity you cannot justify from the photo; say "needs a closer look". Never mark a
checklist item passed because nothing contradicted it. Never send the report without being asked.
