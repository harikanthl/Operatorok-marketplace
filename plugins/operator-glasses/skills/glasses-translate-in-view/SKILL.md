---
name: glasses-translate-in-view
description: Translate the text in front of the person's eyes, from a glasses photo of a sign, menu, label, form or page, into their language, read back in order and kept as a note. Use when a capture holds foreign-language text.
metadata:
  operator:
    capture: glasses
    integrations: [elevenlabs]
    skills: [apple-notes, clear-replies]
---

# Translate what is in view

Live translation is the glasses feature people say changed their daily behaviour. Here it is a photo
of the thing, translated faithfully, spoken or shown back in the order the eye reads it, and kept.

## What you receive

- Photos in `/app/inbox` with the `_collection.json` sidecar (ids, files, times, gps).
- The job prompt may name the target language. If it does not, use the language the person writes in.
- Look at the pixels through `OPERATOR_CAPABILITY_URL` (`vision.semantic`, `mediaPaths`) with
  `Authorization: Bearer $OPERATOR_INGEST_TOKEN`. Ask it to transcribe the text EXACTLY as printed,
  in reading order, keeping line breaks and prices, before you translate anything.

## Do

1. Transcribe first, translate second. Keep the source line beside each translated line so a person
   can point at the sign and match it.
2. Menus and labels: keep numbers, currencies, units and allergen words exactly. Translate dish names
   and add a two-word gloss when the name alone would not tell a stranger what it is.
3. Forms and notices: translate the field labels and the instruction sentences; flag anything that
   is a deadline, a fee or a legal condition with `!` at the start of the line.
4. If a region of text is unreadable (glare, angle, cut off), say which lines and suggest a second
   photo, closer and straight on. Do not fill the gap.

## Deliver

A short Markdown table (source | translation) in the reply, then one fenced `operator-result` block:

```operator-result
{"sourceLanguage": "ja", "targetLanguage": "en", "lines": [{"source": "本日のおすすめ", "translation": "Today's special"}], "unreadable": [], "photo": "IMG_0501.jpg"}
```

## Speaking to the glasses

When asked for a guidance card, `speak: true` and put only the lines that matter in `detail`,
shortest first, under twenty words. A menu is read as "three items: …", not in full.

## Works with (optional)

- `elevenlabs` integration (`ELEVENLABS_API_KEY`): natural speech in the target language for the phone
  to play, when the built-in voice is not good enough for the script.
- `apple-notes` skill: keep the translated menu or notice as a note titled by place and date.
- `clear-replies` skill: keep the spoken answer short.

## Never

Never translate from memory of what a sign "usually says". Never drop a number. Never mark a line as
read when it was not.
