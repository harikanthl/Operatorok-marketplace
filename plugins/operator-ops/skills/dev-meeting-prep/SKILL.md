---
name: dev-meeting-prep
description: Write a one-page brief for an upcoming meeting from the event, recent threads with the attendees and the notes the person keeps, so they walk in knowing the open asks on both sides. Use when the person names a meeting, an attendee, or says "prep me".
metadata:
  operator:
    integrations: [operator-mail]
    mcp: [memory]
    skills: [himalaya, apple-notes, meeting-action-items, clear-replies]
    derivedFrom: OnlyTerp/hermes-optimization-guide skills/dev/meeting-prep (MIT)
---

# Meeting prep

## What you receive

- The event: an `.ics` in `/app/inbox`, or the title, time, place and attendees in the job prompt.
- Threads: mail with the attendees from the last ninety days when the `operator-mail` integration
  or the `himalaya` skill is attached; notes and previous meeting notes from the `memory` MCP
  server or `apple-notes` when attached. With none of these, the brief is the event alone, and
  it says so.

## Do

1. Resolve the meeting: a name matches the next event with that attendee; "next" is the next one.
2. Gather in parallel: the last ten threads per attendee, mentions of the title in notes, and the
   previous meeting's notes if any.
3. One or two lines per thread. Extract the open asks in each direction: what they asked of the
   person, what the person asked of them.
4. Write the brief, under 400 words, in this shape:

   ```
   ## Meeting: {title}
   **When:** … · **Where:** … · **Attendees:** …
   ### Context      last topic, open asks from them, open asks from me
   ### Likely agenda
   ### My notes     from memory, if any
   ### Watch for    anything recent that reads as a hard topic
   ### Links        the threads and docs you used
   ```
5. Save it to `/app/outbox/meeting-prep-<date>.md`.

## Deliver

The brief in the reply (it is short by design), then:

```operator-result
{"meeting": "…", "at": "2026-09-08T14:00Z", "attendees": 3, "threadsRead": 12, "openAsksFromThem": 2, "openAsksFromMe": 1, "sources": ["mail", "memory"], "file": "meeting-prep-2026-09-08.md"}
```

## Works with (optional)

- `meeting-action-items` skill: after the meeting, the same attendees' actions from the notes.

## Never

Never forward or send the brief anywhere. Never invent a position for the person; "no notes" is
the honest line. Never quote a thread you did not read in full.
