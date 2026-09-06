---
name: score-my-setup
description: Score what can be verified from inside a worker's box about how this Operator setup is run, out of fifty, with one fix per miss. Use from Operator Diagnostics, after changing policy, or when something feels loose. Scores values, never the presence of a setting.
metadata:
  operator:
    integrations: []
    mcp: []
    skills: [clear-replies]
    derivedFrom: OnlyTerp/hermes-optimization-guide scripts/score-your-setup.py (MIT), the idea of scoring values not presence
---

# Score my setup

Six checks, each verifiable from where you stand. A check you cannot run scores zero and says why;
a guessed score is worse than a missing one.

## What you receive

- The box you are in: `/app/work` (the workspace), `/app/inbox`, `/app/outbox`, your environment.

## Do

Run every check and record the evidence line for each (the command and what it printed). After
each one, `operator-watch <pct> "<check name>"` puts the person's progress bar where you are; it is
on PATH in every Operator box and harmless anywhere else.

1. **Policy (10).** `policy.md` exists in the workspace and names a risk ladder. Full marks when
   red-class actions require a tap and nothing red is auto-approved; half when the file exists
   but a class is unstated; zero when it is missing.
2. **No keys in files (10).** Search the workspace (`git ls-files` plus untracked, skipping
   `node_modules`, `.git`) for key shapes: `sk-ant-`, `sk-or-`, `ghp_`, `github_pat_`, `AKIA`,
   `xoxb-`, `-----BEGIN`. Full marks at zero hits. Report file and line, never the value.
3. **Egress (10).** `curl -m 3 http://169.254.169.254/` and `curl -m 3 http://metadata.google.internal/`
   must fail. Full marks when both are refused; zero when either answers.
4. **Mounts (8).** `/app/inbox` refuses a write (`touch /app/inbox/.probe` fails); `/app/outbox`
   accepts one (and you remove it). Half marks for one of the two.
5. **Skill budget (6).** Count the skill files staged for you and their total bytes. Full marks
   under 64 KiB total; half between 64 and 96; zero above.
6. **Identity (6).** `OPERATOR_WORKER_NAME` and `OPERATOR_RUNTIME` are set; `OPERATOR_INGEST_TOKEN`
   is set and is not printed by any process listing (`ps -eo args` does not contain it). Full
   marks when all three hold.

Total out of fifty. Write `/app/outbox/setup-score.md` with the table, the evidence lines, and
one fix per miss in the person's terms (which screen, which file).

## Deliver

The total and the misses in the reply, then:

```operator-result
{"total": 42, "outOf": 50, "checks": [{"name": "policy", "score": 10, "of": 10, "evidence": "…"}, {"name": "keys-in-files", "score": 5, "of": 10, "evidence": "1 hit: config/dev.env:3"}], "fixFirst": "Remove the key at config/dev.env:3 and add it under Settings → Integrations", "report": "setup-score.md"}
```

## Never

Never print a key you found; the file and line is the finding. Never score a check you could
not run. Never change policy, mounts, or files to make a check pass.
