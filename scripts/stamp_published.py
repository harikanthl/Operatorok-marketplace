#!/usr/bin/env python3
"""Stamp the index with the commit it is being published from, so LOCAL plugins install.

    python3 scripts/stamp_published.py --sha <40 hex> [--out PATH]

A `local` source lives inside this repo, so the only thing an installer needs that the index cannot
know at authoring time is which commit of THIS repo to fetch, the index cannot pin its own commit
before that commit exists. The publish step knows it (`GITHUB_SHA`, or `git rev-parse HEAD` after a
push), and writes a copy of `marketplace.json` with `publishedSha` set. That copy is what goes to KV;
the file in the repo never carries the stamp. A client then installs a local plugin from
`repository` at `publishedSha` with `path` as the subdirectory, the same fetch as any vendor plugin.

The stamp is only honest for a commit that exists on the remote: run it after the push, never before.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plugin_catalog as pc  # noqa: E402


def main():
    args = sys.argv[1:]
    sha = out = None
    for i, a in enumerate(args):
        if a == "--sha" and i + 1 < len(args):
            sha = args[i + 1]
        elif a.startswith("--sha="):
            sha = a.split("=", 1)[1]
        elif a == "--out" and i + 1 < len(args):
            out = args[i + 1]
        elif a.startswith("--out="):
            out = a.split("=", 1)[1]
    if not sha or not pc.SHA_RE.match(sha):
        print("usage: stamp_published.py --sha <40 hex lowercase> [--out PATH]")
        return 2
    catalog = pc.load_marketplace()
    if not catalog.get("repository"):
        print("ERROR: marketplace.json has no top-level `repository`; local plugins cannot be installed without it")
        return 1
    catalog["publishedSha"] = sha
    out = out or os.path.join(pc.ROOT, ".cache", "marketplace.published.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    n_local = sum(1 for p in catalog.get("plugins", []) if pc.source_of(p)[0] == "local")
    print("stamped %s → %s (%d local plugins now installable)" % (sha[:8], os.path.relpath(out, pc.ROOT), n_local))
    return 0


if __name__ == "__main__":
    sys.exit(main())
