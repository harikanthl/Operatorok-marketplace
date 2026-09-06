---
name: audio-brief
description: Deliver a finished piece of work as a chaptered audio episode the person listens to in Operator. Use when they asked for a podcast, a briefing, a deep dive, a recap, or "read this to me", and whenever a job's own contract names an audio deliverable. You produce the words in one artifact block; the phone produces the voices.
metadata:
  operator:
    integrations: []
    mcp: []
    skills: []
    derivedFrom: Operator's own BriefManifest contract (brief-manifest@1); the caps below are the phone decoder's and are not negotiable.
---

# Audio brief (`brief-manifest@1`)

Operator's phone can SPEAK any artifact that follows this shape. It writes a one-narrator or
two-host script from your chapters, renders it in the voices the person chose (their phone, or
their own OpenAI, ElevenLabs or Gemini key), and gives them a chapter list, a synced transcript, and
an "ask about this line" button. You do not produce audio. You produce the words.

## Emit exactly one block

Finish your turn with:

```
<artifact type="brief-manifest@1" title="A short name for the episode">
{
  "title": "A short name for the episode",
  "headline": "One sentence saying what this is about.",
  "chapters": [
    {
      "title": "What this chapter covers",
      "summary": "One or two sentences leading the chapter.",
      "items": ["One point per line, as a complete spoken sentence."]
    }
  ]
}
</artifact>
```

`title`, `headline` and `summary` are optional; `chapters` is not, and a manifest with no chapter
that has any text in it is discarded.

## Rules

- **It is read aloud.** Plain sentences only. No markdown, no bullet characters, no headings inside
  the text, no code, no URLs spoken out, no emoji.
- **Length.** At most 16 chapters, at most 16 items per chapter, at most 90 words per item, at most
  6,000 words in total (about forty minutes). Anything past a cap is dropped silently, so write
  inside the caps rather than discovering where they are. Four to eight chapters is a good episode;
  a ten-minute episode is about 1,500 words.
- **Numbers as spoken.** "four dollars forty", not "$4.40". "twenty twenty-six", not "2026".
- **No `#xxxxxxxx` tags.** Those are Operator's own citation tokens for the person's sessions and
  workers. They are stripped from anything you write, and a tag you invent can never become a link.
- **Valid JSON**, under 256 KB, with nothing after the closing tag. No comments, no trailing commas,
  no prose inside the block.
- **One block per turn.** A second manifest in the same message is a second episode; emit it in a
  second turn if you mean it.

## Chapters

`kind` is optional and defaults to a plain topic chapter. Set it only when the chapter really is one
of Operator's own brief chapters (`needsAttention`, `yourDay`, `overnight`, `openWork`, `progress`,
`intelligence`, `recommendedAction`); anything else is read as a topic, which is the right answer
for research and for anything made from a document.

## Never

Never put a fact in the manifest that is not in the work it is made from; an episode is the same
work arranged for the ear. Never pad to a length; a shorter honest episode beats a longer one that
repeats itself.
