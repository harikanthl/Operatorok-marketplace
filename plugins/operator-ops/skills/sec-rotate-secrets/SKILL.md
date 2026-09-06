---
name: sec-rotate-secrets
description: Rotate the secrets a workspace owns (webhook HMACs, signing secrets) atomically, and hand the person a checklist for the ones only they can rotate (API keys, tokens), logging fingerprints and never values. Use on a schedule, after a suspected leak, or when the person says "rotate".
metadata:
  operator:
    integrations: [github]
    mcp: []
    skills: [clear-replies]
    derivedFrom: OnlyTerp/hermes-optimization-guide skills/security/rotate-secrets (MIT)
---

# Rotate secrets

In Operator, provider keys live in the phone's Keychain and reach a box as environment variables
at spawn. A box cannot rotate those, and must not try. What a box CAN rotate is a secret the
workspace itself owns: a webhook HMAC in a config file, a signing secret in `.env`, a token the
workspace mints for its own services.

## What you receive

- A pattern in the job prompt (`WEBHOOK_*`, `*_HMAC*`, or `all`) and the workspace under
  `/app/work`. Secret files: `.env`, `.env.*`, `config/*.yaml`, `wrangler.jsonc`, whatever the
  prompt names.

## Do

1. List the keys that match. For each decide the kind by name: an HMAC or webhook secret is
   generated here (`openssl rand -hex 32`); an API key, PAT or OAuth token is the person's to
   rotate at the provider, and goes on the checklist with the provider's URL.
2. Back up each file you will touch as `<file>.bak.<timestamp>` before any write.
3. Rewrite atomically, never with `sed s///` (secret values contain `/`, `&` and `\`): read the
   file into memory, replace the exact `KEY=` line, write to a temp file, `chmod 600`, then move.
   THE SAFE-WRITE LAW: never open a file for writing before its read has finished.
4. Propagate a rotated webhook secret to the remote side when an integration can: GitHub hooks
   via the `github` integration (`PATCH /repos/{owner}/{repo}/hooks/{id}`), proposed first,
   applied after the person's tap.
5. Log every rotation as `key · sha256 fingerprint of the OLD value · sha256 of the NEW value ·
   time` to `/app/outbox/rotation-log.md`. Values never appear anywhere.
6. Write the checklist for the person-only kinds to `/app/outbox/rotate-checklist.md`, one line
   per key with where to rotate it and where in Operator's Settings to paste the new value.

## Deliver

What rotated and what is on the checklist, then:

```operator-result
{"pattern": "WEBHOOK_*", "rotated": [{"key": "…", "file": ".env", "oldFingerprint": "…", "newFingerprint": "…"}], "checklist": [{"key": "…", "rotateAt": "https://…", "pasteIn": "Settings → Integrations → …"}], "propagated": [], "log": "rotation-log.md"}
```

## Never

Never print, log, or echo a secret value. Never rotate a key you cannot propagate and leave a
service broken; propose, then apply after approval. Never touch a file the pattern did not match.
