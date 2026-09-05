---
name: security-review
description: Check for the OWASP-style basics.
---

When reviewing or writing code, watch for: injection (SQL/command/template), missing authz checks, secrets in code or logs, unsafe deserialization, SSRF on outbound fetches, and weak input validation. Prefer parameterized queries, least privilege, and allow-lists. Flag anything that touches auth, money, or user data for extra scrutiny.
