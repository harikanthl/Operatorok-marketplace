---
name: glasses-remember-where
description: Turn "remember where I parked / put this" photos from smart glasses into a findable memory, and answer "where did I leave it" from what was captured. Use when a capture collection holds a photo taken to remember a place or an object's location.
metadata:
  operator:
    capture: glasses
    integrations: [airtable]
    mcp: [memory]
    skills: [apple-notes, apple-reminders, maps]
---

# Remember where

The single most common thing people do with camera glasses is take a photo so they will not have to
remember: the parking spot, the locker, where the passport went, which shelf the part is on. Your job
is to make that photo answer the question later, in one sentence, without the person scrolling.

## What you receive

- Photos and clips in `/app/inbox`, one file per asset, with a `_collection.json` sidecar listing each
  asset's `id`, `file`, `kind`, captured time, `camera`, and `gps` when the glasses had a fix.
- The job prompt says whether this is a **store** ("remember this") or a **recall** ("where is my…").
- If `OPERATOR_CAPABILITY_URL` is set you can look at the pixels: POST `{"capability": "vision.semantic",
  "policy": "balanced", "prompt": "...", "mediaPaths": ["/app/inbox/<file>"]}` with header
  `Authorization: Bearer $OPERATOR_INGEST_TOKEN`; the response's `text` is the answer.

## Store

1. For each photo, describe what fixes the location: signage, level or row markers, landmarks, the
   colour and kind of the container, anything with a number on it. Read text in the frame verbatim.
2. Write one memory line per photo: `<what> — <where, as a person would say it> — <when> — <gps if any>`.
   Example: `car — P3, row F, near the blue elevator door — Tue 14:02 — 37.78,-122.41`.
3. Keep the memory somewhere the next run can read it. In order of preference: the `memory` MCP server
   if attached; otherwise `/app/work/remember.md`, appended, newest last.

## Recall

1. Read the memory store. Match the question against the `what` column loosely (car, bike, bag, keys).
2. Answer with the most recent match, in one sentence a person can act on while walking. Say the time
   so they can judge staleness. If there is a photo, name its file so the phone can show it.
3. No match: say so plainly. Never guess a location.

## Deliver

End with one fenced `operator-result` block:

```operator-result
{"mode": "store", "remembered": [{"what": "car", "where": "P3 row F by the blue elevator", "at": "2026-09-05T14:02:00Z", "photo": "IMG_0412.jpg"}]}
```

or for recall: `{"mode": "recall", "answer": "Your car is on P3, row F, by the blue elevator, parked at 14:02.", "photo": "IMG_0412.jpg", "confidence": 0.9}`.

## Speaking to the glasses

Mentra Live has a speaker and no display. When asked for a guidance card, answer with
`{"title": "P3 row F", "detail": "By the blue elevator door, parked 14:02", "speak": true, "action": "none"}`
and keep `detail` under fifteen words: it is read aloud.

## Works with (optional)

- `memory` MCP server: durable recall across runs.
- `apple-reminders` skill: a timed reminder ("meter runs out at 16:00") when the person says so.
- `apple-notes` skill: mirror the memory line into a note.
- `maps` skill: turn a gps fix into a walking direction.
- `airtable` integration (`AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`): a shared "where things are" table for a team.

## Never

Never invent a location, never round a time to make it sound fresher, and never delete a memory the
person did not ask to forget.
