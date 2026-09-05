---
name: glasses-price-check
description: Identify a product from a glasses photo (shelf tag, box, barcode, label), find its price elsewhere, and say whether to buy it here. Use when a capture shows a product in a shop and the person asks "is this a good price" or "what is this".
metadata:
  operator:
    capture: glasses
    integrations: [firecrawl, tavily, exa]
    mcp: [fetch]
    skills: [product-price-monitor, clear-replies]
---

# Price check in the aisle

Hands-free shopping help: the person looks at a product, and wants to know what it is, what it costs
elsewhere, and whether to pick it up now.

## What you receive

- Photos in `/app/inbox` with the `_collection.json` sidecar. Read the pixels via
  `OPERATOR_CAPABILITY_URL` (`vision.semantic`, `mediaPaths`, bearer `$OPERATOR_INGEST_TOKEN`): ask for
  brand, product name, size or count, any barcode digits, and the shelf price with currency.
- The job prompt may name the shop and the country, which decide the comparison sites.

## Do

1. Identify the product from the photo. If the barcode digits are readable, use them as the key.
2. Look up the price elsewhere. Use the `fetch` MCP server on two or three retailers the person would
   actually buy from in that country; with `FIRECRAWL_API_KEY`, `TAVILY_API_KEY` or `EXA_API_KEY`
   present, use that search first to find the product pages. Record each price with its URL and date.
3. Normalise to the same size or count before comparing. Say the per-unit price.
4. Verdict in one line: buy here, buy elsewhere (where, how much less, delivery caveat), or wait.

## Deliver

Reply with the identification, a three-row comparison, and the verdict, then one fenced
`operator-result` block:

```operator-result
{"product": "Brand X coffee beans 1 kg", "barcode": "5011234567890", "here": {"price": 14.99, "currency": "GBP", "shop": "Tesco"}, "elsewhere": [{"shop": "Amazon", "price": 12.49, "url": "https://…", "seen": "2026-09-05"}], "verdict": "elsewhere", "saving": 2.5, "photo": "IMG_0610.jpg"}
```

## Speaking to the glasses

Guidance card: `{"title": "£14.99 here, £12.49 online", "detail": "Amazon, delivery two days", "speak": true, "action": "none"}`.
Numbers first, source second, under fifteen words.

## Works with (optional)

- `fetch` MCP server: read retailer pages.
- `firecrawl` / `tavily` / `exa` integrations: search that finds the product page in one call.
- `product-price-monitor` skill: keep watching the price after the person leaves the shop.
- `clear-replies` skill: keep the spoken verdict short.

## Never

Never buy anything or add to a cart. Never quote a price you did not see on a page; say "no price found"
instead. Never compare different sizes without saying so.
