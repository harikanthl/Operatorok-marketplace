---
name: browser-clip-to-notes
description: Clip a captured web page or selection into the person's notes as a clean, cited entry with source, date, tags and the passage that mattered, and file it where their notes live. Use when a browser capture's note says clip, save, keep, or file this.
metadata:
  operator:
    capture: browser
    integrations: [airtable]
    skills: [apple-notes, obsidian, notion, llm-wiki, cited-sources]
---

# Clip to notes

Note clippers are among the oldest and stickiest extensions. The difference here is that the clip is
readable later without opening the page, and it says where it came from.

## What you receive

- `page-<epoch>.md` in `/app/inbox` (the page as Markdown) beside `page-<epoch>.html`.
- The job prompt: URL, title, the **selection** (the passage the person highlighted) and the **note**
  (their tag, folder, or why it matters).

## Do

1. The clip body is the selection when there is one, quoted verbatim in a block quote. Without a
   selection, it is the page's main content trimmed of navigation, comments and boilerplate.
2. Above the body: a one-line summary in your words, the source (title, site, URL), the capture date,
   the author and published date when the page states them.
3. Tags: from the note first; then two or three from the content. Lowercase, hyphenated.
4. Below the body: a "Why I clipped this" line built from the note, and a "Key facts" list of up to
   five items, each with the sentence it came from.
5. Never alter the quoted passage. Mark elisions with `[…]`.

## Deliver

Write the clip as `clip-<slug>.md` in the reply's artifacts (frontmatter: title, url, captured,
tags), then one fenced `operator-result` block:

```operator-result
{"title": "…", "url": "https://…", "captured": "2026-09-05T11:00:00Z", "tags": ["pricing", "saas"], "hasSelection": true, "file": "clip-….md", "destination": "notes"}
```

## Works with (optional)

- `apple-notes`, `obsidian` or `notion` skills: file the clip where the person keeps notes, in the
  folder the note names.
- `llm-wiki` skill: fold the clip into a personal wiki page on the topic.
- `cited-sources` skill: the citation discipline for the key facts.
- `airtable` integration (`AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`): a reading log row per clip.

## Never

Never rewrite the passage. Never drop the URL. Never file into a destination the note did not name
without saying where it went.
