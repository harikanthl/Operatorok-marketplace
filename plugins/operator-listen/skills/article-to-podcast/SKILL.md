---
name: article-to-podcast
description: Turn a paper, a blog post, an article or a long page into a finished episode, an mp3 with chapters and a synced transcript rendered in the box with the person's own ElevenLabs, Gemini or OpenAI voice, plus the same episode as a brief the phone can read aloud itself, and show notes. Use when they send a link or a file and say podcast, listen, episode, "read this to me", or "walk me through it". Faithful to the source; never adds a claim the source did not make.
metadata:
  operator:
    capture: browser
    integrations: [elevenlabs, openai, gemini]
    mcp: [fetch]
    skills: [audio-brief, grounded-citations, clear-replies]
    derivedFrom: MuseDrop's Podcast composer (script stage decoupled from voice stage, two hosts or one narrator, canonical PCM concatenated and encoded once, timed transcript beside the audio), rebuilt for a box with the operator.media pack (ffmpeg + episode-render) and Operator's brief-manifest contract.
---

# Article to podcast

The best explainer of a paper is a colleague who read it properly and tells you what it says, what
it does not say, and why it matters, in the order you would ask. That is the show. Not a summary
read aloud, and not two hosts vamping.

## What you receive

- A source, one of: a URL in the job prompt (fetch it with the `fetch` MCP server); a browser
  capture, `page-<epoch>.md` in `/app/inbox` beside the `.html`, with the person's note; or a staged
  file (`.pdf`, `.md`, `.txt`, `.html`, `.epub`). A PDF is read with `pdftotext -layout` first;
  figures and tables are described from their captions and numbers, never invented.
- Optional in the prompt: a length (`5`, `10`, `20` minutes; default ten), a style (`show` for two
  hosts, `anchor` for one narrator; the phone applies the person's own default when you say
  nothing), and a note ("focus on the method", "I am not a statistician").

## Do

1. **Read the whole source.** Then write, in your own words and before any script, the one
   paragraph a careful reader would give: the claim, the evidence, the limits. If you cannot write
   that paragraph, you have not read it yet.
2. **Decide the spine.** Four to eight chapters in the order a curious listener asks: what this is
   and why now; the core idea in one picture; how they showed it; what the numbers say; what it
   does not show, and what the authors admit; who it changes things for; what to read next. Cut any
   chapter with nothing in it.
3. **Write for the ear.** Every item is a complete spoken sentence a person can follow without the
   page: short, concrete, one idea. Say numbers as words. Name the authors once, then "they".
   Explain every term the first time. No headings, bullets, code or URLs inside the text. For a
   `show` the phone assigns the two voices; you write the sentences so that alternating them reads
   as a conversation: a question or a "so what", then the answer.
4. **Stay faithful.** A claim in the episode is a claim in the source. Where you add context from
   outside it, say so in the sentence ("outside this paper, …"). Disagreements and caveats get their
   own chapter, not a clause.
5. **Write the show notes** to `/app/outbox/show-notes.md`: title, the one paragraph from step 1,
   the chapter list with one line each, the source citation (title, authors, venue or site, date,
   URL), and three questions the listener could ask you next.
6. **Write the script** to `/app/work/episode.script.json`, the same words as the chapters, as
   turns: `{"title", "style": "show"|"anchor", "speakers": ["Alex", "Sam"], "chapters": [{"title",
   "turns": [{"speaker": "Alex", "text": "…"}]}]}`. For a show, alternate the two speakers so the
   lines read as a conversation; for an anchor, every turn is the one narrator.
7. **Render the audio**: `episode-render /app/work/episode.script.json --out /app/outbox`. It is
   on PATH in the Listen box (`operator.media` pack). It picks the person's voice provider from the
   key they attached (ElevenLabs, then Gemini, then OpenAI), concatenates canonical PCM, encodes
   once with ffmpeg, and writes `episode.mp3` (ID3 title and chapter markers) and
   `episode.transcript.json` (speaker, text, start time per line) into the outbox; the phone lists
   the mp3 under the session's Documents and plays it. Exit 3 means no voice key was attached: say
   so in one sentence and carry on, because step 8 still gives them the episode. Its stderr shows
   a progress bar on the phone; do not silence it.
8. **Emit the episode** exactly as `audio-brief` says: finish the turn with ONE
   `brief-manifest@1` artifact block, within its caps. About 1,500 words for ten minutes. This is
   the same episode the phone can read in its own voices, and the one that has "ask about this
   line"; the mp3 is the one they can keep and share.

## Deliver

Two lines of reply (what the episode is, how long, whether the mp3 rendered and with which voice),
the artifact block last, and before it:

```operator-result
{"source": {"title": "…", "authors": ["…"], "url": "…", "kind": "paper"}, "minutes": 10, "words": 1480, "chapters": 6, "style": "show", "showNotes": "show-notes.md", "audio": {"file": "episode.mp3", "provider": "elevenlabs", "durationSeconds": 612, "transcript": "episode.transcript.json"}}
```

`audio` is `null` when no voice key was attached.

## Works with (optional)

- `grounded-citations`: the show notes quote the source's own lines for each chapter.
- `browser-summarize-page`: when the person only wants the gist, not an episode.
- `browser-study-pack`: the same source as flashcards and questions instead of, or beside, the episode.

## Never

Never invent a finding, a number or a quote. Never read a URL aloud. Never pad to the requested
length; say it is a six-minute paper and make six minutes. Never write the manifest before the
paragraph in step 1 exists. Never print or log a voice key; `episode-render` never does either.
Never call the mp3 "rendered" when `episode-render` did not exit 0.
