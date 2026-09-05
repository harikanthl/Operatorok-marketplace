---
name: glasses-meeting-notes
description: Turn audio and clips captured by glasses during a conversation, site meeting or lecture into notes, decisions, action items with owners, and a follow-up draft. Use when a capture holds speech and the person wants what was said kept.
metadata:
  operator:
    capture: glasses
    integrations: [resend, operator-mail]
    skills: [meeting-action-items, apple-notes, apple-reminders, himalaya, clear-replies]
---

# Meeting notes from the glasses

The mic is the glasses feature people forget they have. A walking conversation, a stand-up on the
floor, a client on site: the notes get written by nobody. Write them.

## What you receive

- Clips (video with audio) or audio files in `/app/inbox` with the `_collection.json` sidecar. If a
  transcript file (`.txt`, `.srt`, `.json`) is beside a clip, use it. Otherwise ask the host to
  transcribe: POST to `OPERATOR_CAPABILITY_URL` with header `Authorization: Bearer $OPERATOR_INGEST_TOKEN`
  and body `{"capability": "speech.stt", "policy": "balanced", "prompt": "Transcribe this clip and say
  who said what", "mediaPaths": ["/app/inbox/<clip>"]}`, one clip per call. The reply's `text` is JSON:
  `{"text", "language", "segments": [{"start", "end", "speaker", "text"}], "diarized", "provider", "model"}`.
  The host transcribes on the Mac itself unless the person's policy and keys allow a cloud model; the
  `provider` field says which, and you name it in the notes. If the capability is absent and the
  `transcribe-audio` skill's local tools are not in this worker either, say so and stop: notes from
  guessed speech are worse than none.
- The job prompt may name the people present, the purpose, and the person's own name so "I will"
  can be attributed.
- Video frames matter when a person points at something: read them via `OPERATOR_CAPABILITY_URL`
  (`vision.semantic`) only for moments the transcript refers to ("this one here").

## Do

1. Transcript first, cleaned: remove fillers, keep every number, name, date and commitment verbatim.
   Mark unclear stretches `[unclear 00:04:12]` rather than smoothing them over.
2. Notes: five to ten bullets of what was discussed, in order.
3. Decisions: what was agreed, by whom, stated as facts.
4. Action items: `owner — action — due`, only where the transcript has all three or the owner is the
   person themself. Anything with a missing owner goes under "Open".
5. Follow-up draft: a short message to the other people confirming decisions and actions. A DRAFT,
   never sent by you.

## Deliver

Reply with notes, decisions and actions, then one fenced `operator-result` block:

```operator-result
{"title": "Site meeting, 14 Oak St", "at": "2026-09-05T10:30:00Z", "people": ["Ana", "me"], "decisions": ["Replace the trap this week"], "actions": [{"owner": "Ana", "action": "send plumber quote", "due": "2026-09-08"}], "open": ["who signs off the roof work"], "unclear": ["00:04:12"], "draft": "followup.md"}
```

## Speaking to the glasses

At the end of a conversation a guidance card is the action count: `{"title": "3 actions, 1 open", "detail": "Ana sends the quote by Monday", "speak": true, "action": "none"}`.

## Works with (optional)

- `meeting-action-items` skill: the same extraction discipline for a longer recording.
- `apple-notes` skill: the notes kept; `apple-reminders` skill: the person's own actions as reminders.
- `himalaya` skill or `operator-mail` / `resend` integration: send the follow-up, only when told to.
- `clear-replies` skill: keep the spoken summary short.

## Never

Never record an action for someone who did not commit to it. Never send the follow-up. Never fill an
unclear stretch with what was probably said.
