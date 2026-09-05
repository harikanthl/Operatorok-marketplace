---
name: reproduce-paper
description: Run somebody else's code and report honestly what came out, judged by a reviewer that did not do the work.
---

HARD RULE, applies to every character you output including tables, headings, and chart labels: NEVER write an em dash or an en dash. Not one. Use a comma, a colon, a period, or parentheses instead. If you catch yourself reaching for one, rewrite the sentence.

Reproducing a paper means running somebody else's code and reporting honestly what came out. The failure mode is not that the code breaks. It is that you spend an hour patching around it, watch a number finally appear, and call it a reproduction because you want to be finished. Everything below exists to stop that.

WHAT A NORMAL RESULT LOOKS LIKE. In the ICML 2026 reproduction challenge, more than 1,200 people pointed coding agents at 2,226 papers. 51 percent of papers had at least one claim independently verified. 23 percent had at least one claim falsified or contested. Only 266, about 12 percent, reproduced in full. Those people had GPUs and nineteen days. You have a CPU and minutes. A partial, well-evidenced result is the expected outcome here, not a disappointment, and you should not be steering toward a clean yes.

WRITE THE CLAIMS TABLE BEFORE YOU RUN ANYTHING.

Read the paper first. The `literature-search` skill's GET /research/papers/{arxiv_id}/read returns it as Markdown, which is faster and more reliable than parsing the PDF. Pull every quantitative claim you intend to check into a table saved to disk: the claim, the table or figure number it came from, the dataset and split, the metric, and the value the paper states. Write it before the environment exists. A number you record after seeing your own output is not a prediction, it is a rationalization, and by then you cannot tell the two apart.

Two more columns, both filled in before the first command runs. TOLERANCE: what gap would still count as a match. Use the variance the paper states; if it states none, pick a number and say why you picked it. A tolerance chosen after you see your output is not a tolerance. SCALE DEPENDENCE: whether the claim could plausibly change with sequence length, dataset size, model size, or number of steps. Mark those claims now, because a scale-dependent claim CANNOT be settled at reduced scale and you need to know that before you spend the budget rather than after.

SET UP THE LOGBOOK BEFORE THE FIRST COMMAND.

Run `pip install --upgrade trackio`, then `trackio logbook open --title "Reproduction: <paper title>"`. Make one page per claim with `trackio logbook page "Claim 1: ..."`, and run EVERY experiment through the wrapper rather than invoking it directly:

  trackio logbook run --page "Claim 1" -- python eval.py --config small

The wrapper records the exact command, the scripts and config files it touched, the output, the exit code, the duration and the files produced. That is the difference between a deviation log you maintain by remembering to and one that exists because you ran the command. `trackio logbook read --json` reads it back, which is how the reviewer later sees what actually happened instead of what you say happened.

Keep the logbook LOCAL. Do not run `trackio logbook publish`: it uploads to a Hugging Face Space, and an attached trace can still carry prompts, paths, tool inputs and command output even after scrubbing. Copy what belongs in the deliverable into /app/outbox instead.

SCOPE TO THE BOX YOU ARE IN, AND PUT THE SCOPE IN A TABLE.

This worker has CPU, a few gigabytes and minutes. Most published training runs need GPUs and days. Prose hides that gap; a table shows it. Open the report with this one, filled honestly:

| | This reproduction | Full replication |
| --- | --- | --- |
| Scope | what you actually ran | what the paper did |
| Hardware | CPU, no GPU | what the paper used |
| Compute time | your wall clock | theirs, if stated |
| Cost | your approximate spend | theirs, if estimable |
| Outcome | your verdict summary | the paper's claim |

What is checkable here is usually: the repository's own test suite, the small or CPU configuration the authors shipped, one seed instead of five, a subset of the benchmark, an evaluation against released weights rather than training from scratch. Reproduce that. A narrow reproduction, honestly bounded, is a real result. A full one claimed from a partial run is a fabrication.

Find the code with GET /papers/{arxiv_id}/repositories. If the paper has no code, say so and stop. There is nothing to reproduce, and reimplementing the method section from scratch is a different job that needs a different name and a different estimate.

KEEP THE DEVIATION LOG WHILE YOU WORK, NOT AFTERWARDS.

The wrapper captures the mechanical half. You still write the judgement half as it happens: the pin you had to change, the import you patched, the batch size you cut, the seed you fixed, the missing data file you substituted, and WHY. The deviations are a finding in their own right. A number that matched only after nine undocumented changes has told the reader something important about the paper, and it is exactly what disappears when the log is written from memory at the end.

Every verdict must name the file that backs it. A claim's row carries the artifact path the number came from: the log, the eval record, the result file. If you cannot point at a file, you do not have evidence, you have a recollection, and the row is inconclusive.

FOUR WAYS THIS GOES WRONG THAT ARE NOT THE OBVIOUS ONE.

These are from real reproductions, not imagined ones. Check for each before you write a verdict.

1. You stopped looking too early. A result can hold at the scale you ran and break at the scale the paper used. One challenge paper looked correct until the analysis reached k=1024, where growth the shorter runs could not show appeared. This is why you marked scale dependence in advance.
2. The code does not implement the paper. One paper's theory analysed reverse KL while the released code defaulted to forward KL, so every published number came from a different objective than the one described. Read enough of the implementation to confirm it matches the method section before you trust either.
3. The evaluation set is not what it looks like. In one case about 66 percent of scored positions were padding tokens training to near-zero loss, deflating perplexity roughly threefold. Look at what is actually being scored.
4. Your own arithmetic is wrong. One participant compared per-trajectory time against per-batch time and reported a 2x slowdown when the same data confirmed the paper's 8x speedup. Recheck the units and the denominators of any number you are about to call a discrepancy.

THE REVIEW IS TWO QUESTIONS, ASKED BY SOMEBODY WHO DID NOT DO THE WORK.

When the run is finished you are the worst available judge of it. You have watched yourself work around every failure and you have stopped seeing them. So before writing the report, spawn a subagent as the reviewer. Its fresh context is the entire point, so give it PATHS, not a narrative: the repository, the logbook (`trackio logbook read --json`), the deviation log, the claims table, the paper's Markdown. Do not tell it what you concluded and do not summarize what happened.

It answers two separate questions, and they fail differently:

- FAITHFUL: does the implementation and the protocol you ran actually test the paper's claim, or does it test something adjacent?
- SUFFICIENT: is the evidence on disk enough to support the verdict, and what is missing?

A run can be perfectly faithful and badly under-evidenced, or richly evidenced and measuring the wrong thing. One question cannot catch both.

When the reviewer does not pass a claim, that is work, not a sentence in the report. Take one of three actions and record which: DIAGNOSE (find out why the evidence is short), REVISE (fix the protocol and say what changed), RERUN (re-execute and compare). Only when the budget is genuinely gone do you write the claim up as inconclusive with the reviewer's objection intact.

The reviewer's verdict is the one that ships. Yours is a draft it is checking. Quote it verbatim, including every place it disagrees with you. A reviewer that agreed with everything was either handed a summary instead of files, or told the answer.

VERDICTS ARE PER CLAIM, AND THERE ARE FOUR WORDS.

Use these four, which are the vocabulary the reproduction community judges with. Do not invent your own.

- VERIFIED: you ran it at a scale that can settle the claim, and the observed value is inside the tolerance you set in advance. Give the number.
- TOY: it held, but only at reduced scale, on synthetic data, on a subset, or against released weights instead of a real training run. State exactly what was reduced. This is the honest verdict for most of what a CPU box can do, and rounding it up to VERIFIED is the single most common way this job produces a lie.
- FALSIFIED: the evidence contradicts the paper's claim. See the bar below.
- INCONCLUSIVE: you ran it and the evidence does not settle it, or it could not be run here at all. Say which of those two, and why.

One overall "yes" across a paper with eleven claims is not a result, it is a mood.

FALSIFIED CARRIES A HIGHER BAR THAN VERIFIED. Saying a published paper is wrong is a bigger claim than saying it is right, you are making it from a short run on modest hardware, and reproducers get this wrong in practice: a challenge participant's own unit error produced a confident falsification that the same data disproved. Before you write FALSIFIED: recheck your units and denominators, confirm the code implements the method as described, confirm the claim is not scale dependent, and have the reviewer specifically try to refute your refutation. If any of those is unsettled, the verdict is INCONCLUSIVE, not FALSIFIED.

Report the observed number even when it is worse, especially when it is worse. A reproduction that fails cleanly, with a logbook that explains why, is worth more to the reader than one that succeeds and cannot be audited. A negative result, well evidenced, is a finished piece of work.
