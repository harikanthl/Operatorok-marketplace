---
name: glasses-whiteboard-to-notes
description: Turn glasses photos of whiteboards, flip charts, sticky-note walls, slides and business cards into clean notes, diagrams as text, tasks, and contacts. Use when a capture shows writing on a surface that will be erased or walked away from.
metadata:
  operator:
    capture: glasses
    integrations: [airtable]
    skills: [apple-notes, obsidian, notion, apple-reminders, architecture-diagram]
---

# Whiteboard to notes

A glance at the board before it is wiped. What comes back is the board as notes a person can search,
the boxes and arrows as a diagram they can edit, and the "@Sam by Friday" as a task.

## What you receive

- Photos in `/app/inbox` with the `_collection.json` sidecar. Read them via `OPERATOR_CAPABILITY_URL`
  (`vision.semantic`, `mediaPaths`, bearer `$OPERATOR_INGEST_TOKEN`). Ask for: all text verbatim in
  reading order, region by region; boxes and their labels; arrows and what they connect; colours
  when they carry meaning (red = blocked); and, for a card, name, title, company, phone, email.
- Several photos of one board (left half, right half) are one board: stitch by overlapping text.
- The job prompt may name the meeting or project the board belongs to.

## Do

1. Transcribe every region as it is written, then reorganise into headings and bullets only where the
   board's own structure implies it. Keep abbreviations; expand them in brackets when obvious.
2. Diagrams: rewrite as a Mermaid block (`flowchart`, `sequence`, or `mindmap`) so the arrows survive
   as edits, plus a one-line prose reading of what it says.
3. Tasks: any line with a person, a verb and a date or a checkbox becomes an action item
   (`owner, action, due`). Unowned ones go under "Open".
4. Business cards: one contact record each, fields exactly as printed.
5. Say which regions were unreadable and what a better photo would fix (angle, glare, distance).

## Deliver

Reply with the notes, the diagram block, tasks and contacts, then one fenced `operator-result` block:

```operator-result
{"title": "Launch planning board", "notes": "board.md", "diagrams": 1, "actions": [{"owner": "Sam", "action": "vendor shortlist", "due": "2026-09-12"}], "contacts": [{"name": "Priya Nair", "company": "Acme", "email": "priya@acme.example"}], "unreadable": ["bottom right, glare"], "photos": ["IMG_1102.jpg", "IMG_1103.jpg"]}
```

## Speaking to the glasses

Guidance card: `{"title": "Board captured: 14 lines, 3 tasks", "detail": "Bottom right has glare, retake", "speak": true, "action": "none"}`.

## Works with (optional)

- `apple-notes`, `obsidian`, `notion` skills: the notes kept where the person keeps notes.
- `apple-reminders` skill: the person's own actions as reminders.
- `architecture-diagram` skill: a drawn version of the diagram when asked.
- `airtable` integration (`AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`): contacts or tasks into a shared base.

## Never

Never "improve" what the board says. Never assign a task to someone whose name is not on the board.
Never fill an unreadable region with a guess.
