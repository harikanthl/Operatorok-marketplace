---
name: browser-study-pack
description: Turn a captured page, a paper, an article, a chapter or a whole book into a study pack, a summary you can trust, key concepts, notes by section, flashcards, questions at three depths and a quiz with an answer key, in Markdown plus files Anki and Quizlet import directly. Use when a browser capture's note says study, learn, quiz me, flashcards, or exam, or when a document is staged with that ask.
metadata:
  operator:
    capture: browser
    integrations: []
    mcp: [fetch]
    skills: [grounded-citations, clear-replies]
    derivedFrom: MuseDrop's study pack (summary, notes by section, key concepts, flashcards, mock test, exported as one Markdown document and a portable bundle), rewritten for a box that receives a page or a file and returns files.
---

# Study pack

A study pack is not a summary with questions stapled on. It is the set of things a person needs to
learn the source well enough to explain it: what it says, the words it uses, the structure of the
argument, the facts to recall, the questions that test whether they understood, and the ones that
test whether they can use it.

## What you receive

- The source, one of: a browser capture, `page-<epoch>.md` in `/app/inbox` beside the `.html`, with
  the person's note; a URL in the prompt (fetch it with the `fetch` MCP server); or a staged file
  (`.pdf`, `.epub`, `.md`, `.txt`, `.html`). A PDF is read with `pdftotext -layout`; an EPUB is
  unzipped and its XHTML read in spine order. A book is worked chapter by chapter, and the pack has
  one section per chapter.
- Optional in the note: a level (`intro`, `course`, `exam`; default `course`), a focus ("just the
  proofs", "chapters three to five"), and a deck name for the flashcards.

## Do

1. **Read all of it.** Then write the one-paragraph summary a good student would give: the claim,
   how it is supported, what it leaves open. Every later part is built from the source, never from
   what you already know about the topic; where you add outside context, mark it "(context)".
2. **Key concepts.** Ten to thirty terms the source depends on, each defined in one sentence in
   the source's own sense, with where it first appears (page, section or heading).
3. **Notes by section.** Follow the source's own structure. Per section: the point in one line,
   then three to six bullets of what it establishes, with numbers and names kept exact. Cite the
   passage each bullet rests on (`grounded-citations`).
4. **Flashcards.** Thirty to sixty for an article, up to a hundred and fifty for a book. Each is
   ONE fact, term, or relation, front under fifteen words, back under forty, no "and" that hides
   two cards. Cloze cards for definitions and numbers; question cards for mechanisms and causes.
   Tag each with its section.
5. **Questions at three depths**, with model answers: *recall* (what did it say), *apply* (use it
   on a new case you write), *critique* (where is it weak, what would change the conclusion).
   Eight of each for an article, twelve per chapter for a book.
6. **A quiz**: ten multiple-choice questions with four options, one correct, plausible wrong
   options drawn from the source's own near-misses, and an answer key that says why each wrong
   option is wrong.
7. **Misconceptions**: the five things a reader is most likely to get wrong about this source, and
   the sentence that corrects each.
8. **Write the files** to `/app/outbox/`:
   - `study-pack.md`: everything above, in that order, with a title and the source citation.
   - `flashcards-anki.txt`: importable as-is by Anki 2.1.54 or newer, with these header lines
     first: `#separator:tab`, `#html:false`, `#notetype:Basic`, `#deck:<deck name>`,
     `#tags column:3`; then one card per line, `front<TAB>back<TAB>tags`. Cloze cards go in a
     second file, `flashcards-anki-cloze.txt`, with `#notetype:Cloze` and `{{c1::…}}` syntax.
   - `flashcards-quizlet.tsv`: `term<TAB>definition`, one per line, no header.
   - `study-pack.json`: `{"title","source":{…},"summary","concepts":[{"term","definition","where"}],"sections":[{"heading","point","bullets":[…]}],"flashcards":[{"front","back","tags":[…],"kind":"basic|cloze"}],"questions":[{"depth":"recall|apply|critique","q","answer"}],"quiz":[{"q","options":[…],"answer":0,"why":[…]}],"misconceptions":[{"wrong","right"}]}`.

## Deliver

The summary paragraph and the counts in the reply, then:

```operator-result
{"source": {"title": "…", "kind": "paper", "url": "…"}, "level": "course", "concepts": 18, "sections": 7, "flashcards": 48, "questions": 24, "quiz": 10, "files": ["study-pack.md", "flashcards-anki.txt", "flashcards-anki-cloze.txt", "flashcards-quizlet.tsv", "study-pack.json"]}
```

## Works with (optional)

- `article-to-podcast`: the same source as an episode to listen to before drilling the cards.
- `browser-clip-to-notes`: file the pack's summary where the person's notes live.
- `dev-meeting-prep`: a pack on a paper before a reading group.

## Never

Never test a fact the source does not state. Never write a flashcard with two facts on it. Never
mark a quiz option correct because it sounds right; every answer points at a passage. Never skip a
chapter of a book because it was long; say the chapter was skipped and why, if you must.
