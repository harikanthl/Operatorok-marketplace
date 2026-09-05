---
name: browser-price-watch
description: From a captured product page, extract the product and price, compare it across other retailers, say whether to buy now, and set up a watch that reports when the price drops. Use when a browser capture is a shop or listing page and the note asks about price, deal, or "track this".
metadata:
  operator:
    capture: browser
    integrations: [firecrawl, tavily, exa, resend, twilio]
    mcp: [fetch]
    skills: [product-price-monitor, clear-replies]
---

# Price watch

Price tracking is the shopping use people install extensions for. Read the price from the page the
person is on, check it elsewhere, and if asked, keep watching.

## What you receive

- `page-<epoch>.md` (and `.html`) in `/app/inbox`: the product page.
- The job prompt: URL, title, the **note** ("is this a good price", "track", "under 40") and any
  **selection** (often the price or the variant).

## Do

1. Extract: product name, brand, variant (size, colour), listed price, currency, sale vs list price,
   stock, seller, shipping line. Every field from the page file, quoted.
2. Compare: with `FIRECRAWL_API_KEY`, `TAVILY_API_KEY` or `EXA_API_KEY` present, search for the exact
   product; otherwise use the `fetch` MCP server on two or three retailers for that country. Record
   price, URL and date for each. Normalise variants before comparing.
3. Verdict: buy here, buy there, or wait. Mention the price history only if a page states it.
4. If the note asks to track, or names a target price: write the watch as a small spec the
   `product-price-monitor` skill (or an automation) can run: URL, selector or price text, target,
   check interval, and where to notify.

## Deliver

Reply with the extraction, the comparison table and the verdict, then one fenced `operator-result`
block:

```operator-result
{"product": "…", "variant": "…", "here": {"price": 129.0, "currency": "USD", "seller": "…", "url": "https://…"}, "elsewhere": [{"seller": "…", "price": 119.0, "url": "https://…", "seen": "2026-09-05"}], "verdict": "elsewhere", "watch": {"url": "https://…", "target": 100.0, "every": "6h", "notify": "phone"}}
```

## Works with (optional)

- `fetch` MCP server: read retailer pages.
- `firecrawl` / `tavily` / `exa` integrations: product search across the web.
- `product-price-monitor` skill: run the watch.
- `resend` (`RESEND_API_KEY`) or `twilio` (`TWILIO_*`) integrations: the drop notification, when the person wants email or SMS instead of the phone.

## Never

Never purchase, add to cart, or apply a coupon. Never quote a price without a URL. Never compare
different variants as if they were the same.
