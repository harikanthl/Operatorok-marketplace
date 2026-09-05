---
name: glasses-fridge-to-recipe
description: From glasses photos of a fridge, pantry or shopping basket, list what is there, propose meals that use it, and produce a shopping list for what is missing. Use when a capture shows food or a kitchen and the person asks what to cook or what to buy.
metadata:
  operator:
    capture: glasses
    integrations: []
    skills: [apple-reminders, apple-notes, clear-replies]
---

# Fridge to recipe

"What can I cook with what I have" is the question people ask their glasses in the kitchen, hands
full. Answer it from the photos, and turn the gap into a shopping list.

## What you receive

- Photos in `/app/inbox` (fridge shelves, pantry, a basket, a receipt) with the `_collection.json`
  sidecar. Use `OPERATOR_CAPABILITY_URL` (`vision.semantic`, `mediaPaths`, bearer
  `$OPERATOR_INGEST_TOKEN`) to read the shelves: ask for every visible food item with a rough quantity
  and any visible date.
- The job prompt may carry constraints: people count, diet, time available, cuisine, a dish they want.

## Do

1. Inventory first. One line per item, with quantity as seen ("half a lemon", "2 eggs", "milk, open").
   Mark items whose date is visible and past.
2. Propose three meals, ranked by how much of the inventory each uses and how little it needs bought.
   For each: name, time, the inventory items it uses, the items missing.
3. Write the recipe for the top pick only, in numbered steps a person can follow with wet hands:
   short lines, quantities, temperatures, timings. Others get one line each.
4. Shopping list = the union of missing items for the top pick, grouped by aisle.

## Deliver

Reply with the inventory, the three options and the top recipe, then one fenced `operator-result`
block:

```operator-result
{"inventory": [{"item": "eggs", "qty": "6"}, {"item": "spinach", "qty": "1 bag", "note": "wilting"}], "meals": [{"name": "Spinach omelette", "minutes": 15, "uses": ["eggs", "spinach"], "missing": ["feta"]}], "shoppingList": ["feta"], "expired": []}
```

## Speaking to the glasses

Guidance card: `{"title": "Spinach omelette, 15 min", "detail": "You have eggs and spinach; buy feta", "speak": true, "action": "none"}`.
One meal per card. Steps are read one at a time when the person says "next".

## Works with (optional)

- `apple-reminders` skill: the shopping list as a reminders list named "Groceries".
- `apple-notes` skill: the recipe kept as a note.
- `clear-replies` skill: keep spoken steps short.

## Never

Never claim an item is safe to eat past a visible date. Never invent items you did not see; say
"I could not see the door shelves" instead.
