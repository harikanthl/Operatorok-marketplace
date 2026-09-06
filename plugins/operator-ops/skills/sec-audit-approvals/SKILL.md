---
name: sec-audit-approvals
description: Audit every path by which work runs without a tap in this workspace, the risk ladder in policy.md, standing "always allow" pins, automations that run unattended, and report the drift. Use monthly, after choosing "always allow", or before trusting a new automation.
metadata:
  operator:
    integrations: []
    mcp: []
    skills: [structured-report, clear-replies]
    derivedFrom: OnlyTerp/hermes-optimization-guide skills/security/audit-approval-bypass (MIT)
---

# Approval audit

A tap is how work starts and money is spent in Operator. Every standing exception to that is a
place an attacker would love, and this audit lists them so the person can see the whole set.

## What you receive

- The workspace under `/app/work`: its `policy.md` (the risk-class ladder and what each class
  needs), any `.operator/` pins, and the automations staged in `/app/inbox/_automations.json`
  when the job stages them. The job prompt may name an automation to focus on.

## Do

1. Read `policy.md`. Record for each risk class what it requires (auto, tap, Face ID) and any
   class that is auto-approved.
2. List standing pins: every "always allow" a person granted and what it matches. Each is a
   permanent yes; say what it covers today, in plain words.
3. For each unattended automation: its schedule, which risk classes its jobs can hit, and whether
   a gated command would park (waiting for a phone) or be refused. An automation that could
   reach a red class with nobody present is the finding this audit exists for.
4. Flag:
   - **RED** a red-class action with no tap on any path; an always-allow pin whose match is broad
     (`rm -r`, `git push`, a wildcard);
   - **AMBER** an amber class auto-approved for an unattended automation; a pin older than
     ninety days;
   - **GREEN** the rest, listed so the person sees the audit covered them.
5. Write `/app/outbox/approval-audit-<date>.md`.

## Deliver

The red and amber lines in the reply, then:

```operator-result
{"policyFound": true, "pins": 3, "automations": 4, "red": 1, "amber": 2, "findings": [{"flag": "RED", "where": "pin: 'git push origin main'", "why": "…", "proposal": "remove the pin; approve pushes per run"}], "report": "approval-audit-2026-09-06.md"}
```

## Never

Never change `policy.md`, a pin, or an automation. Never test a gated action to see whether it
gates. Never call an approval posture fine because the file was missing; a missing `policy.md`
is a RED finding.
