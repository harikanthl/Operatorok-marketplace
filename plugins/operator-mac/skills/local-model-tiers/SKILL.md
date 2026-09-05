---
name: local-model-tiers
description: The tier table for Apple silicon: which Ollama model a Mac can run well, from its unified memory and free disk.
---

HARD RULE, applies to every character you output including tables and headings: NEVER write an em dash or an en dash. Use a comma, a colon, a period, or parentheses instead.

You are choosing a local model for THIS Mac from measured facts, not from taste. Read the facts file first. It is at $HOME/Library/Application Support/Operator/LocalModels/fit.json and carries memoryBytes (unified memory), chip, freeKB (free disk on /), macOS, ollamaInstalled, brew, and ollama (the answer from GET /api/tags when Ollama is running, else null: it lists what is already pulled with each model's size).

THE TABLE (read 2026-09-04; sizes are approximate download sizes):

| Unified memory | Class | Pick (Ollama tag) | Download | Note |
|---|---|---|---|---|
| 8 GB | 3 to 4B, 8-bit | gemma4:4b-it-q8_0 | ~4.5 GB | sub-3B models suffer at 4-bit; Apple's on-device model is the alternative that needs nothing installed |
| 16 GB | 7 to 9B, Q4 | gemma4:9b | ~5.4 GB | the everyday sweet spot |
| 24 to 32 GB | 30B-A3B MoE Q4, or 13 to 14B dense | qwen3.8:30b-a3b | ~19 GB | ~100 tok/s on M-series |
| 32 GB and up, and the bot WORKS (tool calls) | 31B dense | gemma4:31b | ~19 GB | the only tier with reliable tool calling |
| 64 GB | 70B Q4 | llama4:70b | ~40 GB | production-viable |
| 96 to 128 GB | bf16 70B or a large MoE | your call, state it | | |

THE RULE: pick the largest tier whose weights plus an 8k KV cache fit in 60% of unified memory while the person keeps using the Mac. Weights at Q4 are roughly 0.6 GB per billion parameters; at 8-bit roughly 1.1 GB per billion; add 1 GB for the KV cache at 8k. Report the fit as one of three words: fits (comfortably inside 60%), tight (inside memory but over 60%, name the trade), too-big (does not fit, do not offer it).

DISK IS CHECKED HERE, NOT LATER. Compare freeKB against the download size plus 10 GB of headroom. If it does not fit, the recommendation is to free space first (Mac Housekeeping can), stated with the exact shortfall in GB, and no pull is offered. A download that dies at 90% is the failure this skill exists to prevent.

IF OLLAMA IS ALREADY RUNNING, recommend FROM what is pulled when something suitable is there: a model already on disk costs nothing to use, and re-downloading a near-equivalent is waste. Say which existing model you would use and why, or why none of them fit.

WRITE TWO FILES. First, pick.json to BOTH $HOME/Library/Application Support/Operator/LocalModels/pick.json and ./outbox/pick.json, exactly this shape: {"tag": "<ollama tag>", "fit": "fits|tight|too-big", "downloadGB": <number>, "freeGB": <number>, "memoryGB": <number>, "why": "<one sentence>", "alreadyPulled": true|false}. Second, ./outbox/recommendation.md: the sentence a person reads, with the numbers in it, for example: gemma4:9b fits this 16 GB Mac (5.4 GB to download, 41 GB free). If the verdict is too-big, say what it needs, what is free, and that Housekeeping can help.

NEVER download anything yourself. Never run ollama pull. Your job ends at the pick; the person taps the pull.
