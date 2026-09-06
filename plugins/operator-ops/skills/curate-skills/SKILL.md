---
name: curate-skills
description: Keep a skill library honest, find duplicates, stale command flags, one-off task notes and overlong descriptions, and propose what to archive, merge or trim, without changing anything. Use monthly, after a batch of new skills, or when the picker has become noise.
metadata:
  operator:
    integrations: []
    mcp: []
    skills: [clear-replies]
    derivedFrom: OnlyTerp/hermes-optimization-guide part22 §1 (Curator) and part26 §3 (the haircut), MIT
---

# Curate skills

A skill library grows until half of it is two versions of the same thing, a note somebody wrote
for one afternoon, and a command whose flags changed last spring. The curator reads all of it and
proposes; the person decides.

## What you receive

- A directory of skills: `/app/inbox/skills/` when the job stages the person's own library, or a
  marketplace clone under `/app/work` (`plugins/*/skills/*/SKILL.md`). The prompt may name one
  plugin to keep to.

## Do

1. Read every `SKILL.md`: name, description, the body, helper files. Count words in each
   description; over 160 characters is a **haircut** finding (every description loads into
   context on every session).
2. **Duplicates.** Two skills whose descriptions share the trigger and whose bodies share the
   procedure are one skill. Name the pair and which to keep (the newer, or the one with tests).
3. **Stale.** A command flag or a URL in a body that the workspace's own tools or docs contradict
   (`--help` disagrees, a 404 through the `fetch` MCP server if attached) is a stale finding
   with the line quoted.
4. **One-off.** A body that names a specific date, ticket or file as its whole purpose is a task
   note, not a skill; propose archiving it.
5. **Pinned** skills (the prompt names them) are never proposed for archive.
6. Write `/app/outbox/skill-curation.md`: a table of proposals (`archive`, `merge into X`,
   `trim description`, `fix flag`), each with the evidence line, and a patch under
   `/app/outbox/skill-curation.patch` for the trims and flag fixes the person can apply as one.

## Deliver

The proposal counts and the top five in the reply, then:

```operator-result
{"skills": 58, "proposals": {"archive": 4, "merge": 2, "trim": 11, "fix": 3}, "pinned": 6, "items": [{"skill": "…", "action": "merge", "into": "…", "why": "…"}], "report": "skill-curation.md", "patch": "skill-curation.patch"}
```

## Never

Never delete, move or edit a skill. Never propose archiving a pinned skill. Never call a skill
a duplicate on its name alone; the procedure has to match.
