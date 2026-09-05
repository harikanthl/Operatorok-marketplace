---
name: browser-lead-to-crm
description: Turn a captured profile, company page or listing (LinkedIn, a team page, a directory, a property listing) into a clean CRM record with the fields the person's pipeline uses, deduplicated against what they already have, plus a first-touch draft. Use when a browser capture's note says lead, contact, add to CRM, or save this person.
metadata:
  operator:
    capture: browser
    integrations: [airtable, postgres, supabase]
    mcp: [fetch, postgres]
    skills: [notion, google-workspace, clear-replies]
---

# Lead to CRM

Saving a person or a company from a page into the pipeline is what sales and recruiting extensions
do all day. Do it with the fields the person's CRM actually has, and never twice for the same lead.

## What you receive

- `page-<epoch>.md` in `/app/inbox`: the profile, company page or listing.
- The job prompt: URL, title, the **note** (stage, owner, why: "warm, met at the expo", "pipeline:
  Q4 enterprise") and any **selection**.
- The pipeline's field list when attached (`fields.md` or a CSV header), or the CRM reachable through
  an integration. No field list: use a sensible default (name, title, company, email, phone, location,
  source URL, stage, owner, notes, captured).

## Do

1. Extract only what the page states: name, title, company, location, contact details that are
   PUBLIC on the page, company size and industry when shown. Quote the line each came from.
2. Never infer an email from a name pattern. A missing email is a missing email.
3. Dedupe: if a CRM is reachable (Airtable base, a Postgres or Supabase database through
   `DATABASE_URL` / the `postgres` MCP server, a Notion database), search by name and company and by
   URL. A match becomes an UPDATE proposal showing the diff, not a new row.
4. Stage, owner and tags from the note. Enrich from the company site with the `fetch` MCP server
   only when the note asks, and mark enriched fields as such.
5. First-touch draft: three sentences, referencing one specific thing from the page, ending with
   one small ask. A draft. The person sends.

## Deliver

Reply with the record and the draft, then one fenced `operator-result` block:

```operator-result
{"url": "https://…", "record": {"name": "…", "title": "…", "company": "…", "email": null, "location": "…", "stage": "warm", "owner": "me", "source": "https://…"}, "duplicateOf": null, "enriched": [], "written": false, "draft": "first-touch.md"}
```

`written` is true only after the row was actually created or updated in a reachable CRM, and only
when the note said to write it.

## Works with (optional)

- `airtable` integration (`AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`): the pipeline as a base.
- `postgres` / `supabase` integrations and the `postgres` MCP server: a database-backed CRM.
- `notion` or `google-workspace` skills: a Notion database or a Google Sheet as the pipeline.
- `fetch` MCP server: company-site enrichment when asked.

## Never

Never scrape beyond the captured page unless asked. Never guess an email or a phone. Never write a
row the note did not ask to write, and never overwrite a field without showing the diff.
