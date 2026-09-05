---
name: browser-reply-draft
description: Draft a reply to what is on the captured page (an email thread, a message, a comment, a review, a support ticket, a post) in the person's voice, from their note, with the facts taken from the page. Never sends. Use when a browser capture's note says reply, respond, answer, or draft.
metadata:
  operator:
    capture: browser
    integrations: [operator-mail, resend]
    skills: [humanizer, clear-replies, himalaya]
---

# Draft the reply

AI writing help inside the browser is the most-installed productivity extension there is. The
difference here: the draft is built from the actual thread on the page and the person's own words,
and it stays a draft until they send it.

## What you receive

- `page-<epoch>.md` in `/app/inbox`: the thread, post, ticket or review as the page shows it.
- The job prompt: URL, title, the **note** (what the person wants to say: "decline politely",
  "yes, Tuesday works, ask about parking") and any **selection** (the message to answer).

## Do

1. Find what to answer: the selection, or the latest message addressed to the person. Quote it back
   in one line so a wrong target is caught.
2. Facts only from the page and the note: names, dates, amounts, what was asked. Nothing the person
   did not say or the page does not show.
3. Voice: match the person's own earlier messages in the thread when there are any (length, warmth,
   formality, sign-off). Otherwise plain and brief.
4. Structure: answer the ask in the first sentence, then the one or two things that need saying,
   then the next step. Under 120 words unless the note wants more.
5. Offer two variants only when the note is ambiguous about tone; otherwise one draft.
6. Say what the draft does NOT address, if the thread asked more than the note answered.

## Deliver

The draft in the reply, ready to paste, then one fenced `operator-result` block:

```operator-result
{"url": "https://…", "answering": "Ana, 2026-09-04: can you do Tuesday?", "draft": "reply.md", "words": 84, "unaddressed": ["the invoice question"], "sent": false}
```

## Works with (optional)

- `humanizer` skill: make the draft read like a person wrote it.
- `himalaya` skill or `operator-mail` / `resend` integrations: send it, only when the person says send.
- `clear-replies` skill: short, scannable.

## Never

Never send, post, or submit. Never commit the person to a date, price or promise the note did not give.
Never invent a detail to sound complete.
