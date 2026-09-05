---
name: glasses-describe-scene
description: Describe what is in front of a person who cannot see it well, from a glasses photo, in the order that matters for acting, and read any text aloud. Use for accessibility, low light, or "what am I looking at" questions from the glasses.
metadata:
  operator:
    capture: glasses
    integrations: [elevenlabs]
    skills: [clear-replies]
---

# Describe the scene

For a person with low vision, camera glasses with a speaker are the use case, not a use case. The
description has to be useful before it is complete: what is in the way, what is written, what is
about to matter.

## What you receive

- One or more photos in `/app/inbox` with the `_collection.json` sidecar. Read them via
  `OPERATOR_CAPABILITY_URL` (`vision.semantic`, `mediaPaths`, bearer `$OPERATOR_INGEST_TOKEN`). Ask
  for: obstacles and their position (left, ahead, right, distance in steps if judgeable), people and
  what they are doing, any text exactly as printed, signs and their meaning, and the general place.
- The job prompt may carry the question ("is this the right bus", "read this to me", "who is here").

## Do

1. Answer the question first if there is one, in one sentence.
2. Then the scene in this order: hazards and obstacles, then things that need action (a door, a
   counter, a queue), then people, then the rest. Positions as clock directions or left/ahead/right,
   distances in steps or metres, never "nearby".
3. Text: read it verbatim, most important first (a platform number before an advert). Say when text
   is partly unreadable.
4. Keep every sentence short. This will be spoken.
5. If the photo is too dark, blurred, or aimed at the floor, say exactly that and what to do: "tilt up",
   "step back", "try again with the light on".

## Deliver

The spoken description is the reply. Then one fenced `operator-result` block:

```operator-result
{"answer": "Yes, this is the 42 to Kings Cross.", "hazards": [{"what": "step down", "where": "ahead, one pace"}], "text": ["42 Kings Cross", "Exit"], "people": 3, "quality": "ok", "photo": "IMG_0905.jpg"}
```

## Speaking to the glasses

Guidance card: `{"title": "Step down ahead", "detail": "One pace. Bus 42 to Kings Cross on your right", "speak": true, "action": "none"}`.
`speak` is always true for this skill.

## Works with (optional)

- `elevenlabs` integration (`ELEVENLABS_API_KEY`): a clearer voice for long readings.
- `clear-replies` skill: short sentences.

## Never

Never guess at text you cannot read. Never say a path is clear when part of the frame is not visible.
Never describe a person's appearance beyond what helps the question (a uniform, a raised hand).
