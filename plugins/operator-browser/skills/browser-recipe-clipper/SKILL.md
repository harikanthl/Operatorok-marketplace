---
name: browser-recipe-clipper
description: Extract the recipe from a captured page (ingredients with quantities, steps, times, yield) without the life story, scale it, convert units, and file it with a shopping list. Use when a browser capture is a recipe page.
metadata:
  operator:
    capture: browser
    integrations: []
    skills: [apple-notes, apple-reminders, obsidian, notion, clear-replies]
---

# Recipe clipper

Recipe clippers are a top extension category for one reason: the recipe is a fifth of the page. Keep
the fifth, exactly, and make it cook-ready.

## What you receive

- `page-<epoch>.md` and `page-<epoch>.html` in `/app/inbox`. Recipe pages often carry structured data
  (`application/ld+json` with `@type: Recipe`) in the HTML; use it when present, it is the author's
  own ingredient list. Otherwise read the Markdown.
- The job prompt: URL, title, the **note** ("for 6", "metric", "no dairy") and any **selection**.

## Do

1. Extract: title, yield, prep and cook time, ingredients as `quantity unit item (prep)`, steps as
   numbered imperative sentences, oven temperature, and the author's notes that change the result
   (rest time, substitutions). Nothing else from the page.
2. Scale to the note's servings, rounding to sensible kitchen amounts and saying where you rounded.
3. Convert units when the note asks (cups to grams uses per-ingredient densities; say the source
   table). Temperatures in both scales.
4. Substitutions the note asks for ("no dairy") are listed as options, not silently applied.
5. Shopping list = ingredients grouped by aisle, quantities summed.

## Deliver

Write the recipe as `recipe-<slug>.md` (frontmatter: title, url, yield, times, tags), then one fenced
`operator-result` block:

```operator-result
{"title": "…", "url": "https://…", "yield": "6", "scaledFrom": "4", "ingredients": 12, "steps": 8, "converted": "metric", "file": "recipe-….md", "shoppingList": ["…"]}
```

## Works with (optional)

- `apple-notes`, `obsidian` or `notion` skills: file the recipe in the person's recipe folder.
- `apple-reminders` skill: the shopping list as a reminders list.
- `clear-replies` skill: the chat reply is title, time and servings; the recipe is the artifact.

## Never

Never paraphrase a quantity. Never drop an ingredient that appears only in the steps; add it to the
list and say so. Never apply a substitution the person did not confirm.
