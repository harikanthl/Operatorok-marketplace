---
name: job-contract
description: Read /app/inbox/_contract.json and deliver exactly the declared outputs as artifact blocks.
---

HARD RULE, applies to every character you output including tables, headings, and chart labels: NEVER write an em dash (—) or an en dash (–). Not one. Use a comma, a colon, a period, or parentheses instead. If you catch yourself reaching for —, rewrite the sentence.

At the very start of the task, check whether /app/inbox/_contract.json exists. If it is absent, there is no contract to honor: proceed normally and ignore everything below.

If it is present, it is your invocation contract, the exact agreement for what you were handed and what you must return. Read it first, before anything else. It is an envelope shaped {"contract":"job-contract@1","job":…,"solution":…,"definition":{id,name,inputs,outputs,…}}. Two fields decide your work:
- definition.inputs lists what you were given. A slot with kind "file" is sitting in /app/inbox. A slot with kind "connector" is wired in as an environment variable. A slot with kind "text" arrived in the first message. Slots of kind "knowledge" or "document" are reference material, also in /app/inbox. A slot of kind "knowledge" arrives specifically at /app/inbox/knowledge/ when the solution has accumulated knowledge, and is simply absent otherwise, so treat it as optional reference material.
- definition.outputs lists EXACTLY what to deliver. Not a suggestion, the whole job. Deliver every output slot, deliver nothing beyond them.

Deliver each output slot as ONE artifact block, and write the same content to a durable file:

<artifact type="X" title="LABEL">
… the deliverable …
</artifact>

- type comes from the slot's artifactType, mapped: html → html, markdown → markdown, table → markdown (render the content as a proper Markdown table with a header row), json → markdown (put the JSON inside a ```json fence).
- title is the slot's label, verbatim. Use the label EXACTLY as written, including its capitalisation: the label is how the deliverable is identified everywhere it appears, and a retitled artifact is read as a different deliverable and shown twice.
- An html deliverable is read on a PHONE, in a WKWebView about 380px wide. Write a complete self-contained document with all css in one inline <style>, `<meta name="viewport" content="width=device-width, initial-scale=1">` as the first head line, and a single-column mobile-first layout. Never set a fixed pixel width. A wide table must sit in its own horizontally scrolling container (`<div style="overflow-x:auto"><table>…</table></div>`) and keep to about five columns, with cell padding, because an unpadded table on a phone runs its labels together and is unreadable. Put the full detail in the file copy if it does not fit the card.
- Put ONE short plain sentence before each artifact as the chat preview. Do not repeat the deliverable outside the tag.
- The artifact block must contain the COMPLETE deliverable itself, even when it is long HTML. NEVER make the block a pointer or summary such as "see /app/outbox/report.html": the phone renders ONLY what is inside the block; the outbox file is the durable copy, not the display copy.
- ALSO write each artifact to /app/outbox/<slot-id>.<ext>, the durable file copy: .md for markdown and table, .html for html, .json for json, .csv when a table is genuinely tabular data you also want as a spreadsheet. Same content in both places.

Discipline that keeps the contract honest:
- One artifact per output slot. If there are three output slots, emit three blocks, each with its own title, each also written to /app/outbox.
- Do not invent outputs the contract did not ask for. Quick clarifications, questions, and status updates are just normal replies, no artifact tag.
- If a REQUIRED input slot's material is genuinely missing, for example the slot expects a file and nothing in /app/inbox matches it, do NOT fabricate data to fill the gap. Ask ONE specific question, on its own line, as the very last line of your reply, and stop there.

Voice, when the deliverable is prose (must read as written by a person, never AI-generated):
- No em dashes anywhere. Use a comma, a colon, a period, or parentheses.
- Vary sentence length; mix short and long. Uniform medium cadence is the top AI tell.
- Lead with the finding. A busy reader should get the point from the first two sentences.
- Do not overuse: delve, leverage, utilize, facilitate, foster, harness, navigate, underscore, showcase, streamline, robust, seamless, pivotal. Use the plain word.
- Cut AI filler: "it's worth noting", "it is important to note", "when it comes to". State the point.

Machine copies: when an output slot declares a schemaID, ALSO write /app/outbox/<slot-id>.json, a strict JSON document conforming to that schema (for email-drafts@1: an array of {"to","subject","body"}; for sms-drafts@1: an array of {"to","body"}). This file is what one-tap Send actions execute, exactly as written, so put final, send-ready text in it: real recipient addresses or numbers from the input data, no placeholders. If a recipient is unknown, omit that record rather than inventing contact details. Keep the human-readable artifact and the JSON file consistent. knowledge-metrics.json is a RESERVED outbox filename for usage receipts (see the grounded-citations skill) and is never a deliverable slot file.
