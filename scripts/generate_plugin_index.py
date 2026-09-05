#!/usr/bin/env python3
"""Generate `.operator-plugin/plugin-index.json`, what each plugin provides, so a client can show
a plugin's contents before installing it.

    python3 scripts/generate_plugin_index.py           # fetch remotes at their SHA, write the index
    python3 scripts/generate_plugin_index.py --check   # regenerate in memory and fail if stale

Never hand-edit the output. For a remote source the index records the SHA it was read from; a
client must ignore index data whose SHA no longer matches the catalog entry.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plugin_catalog as pc  # noqa: E402

OUT = os.path.join(pc.ROOT, ".operator-plugin", "plugin-index.json")


def build():
    catalog = pc.load_marketplace()
    index = {"version": 1, "plugins": {}}
    failures = []
    warnings = []
    # What the committed index last knew, for the verdict carry-over when GitHub cannot be asked.
    try:
        with open(OUT, "r", encoding="utf-8") as fh:
            previous = (json.load(fh).get("plugins") or {})
    except (OSError, ValueError):
        previous = {}
    for entry in catalog.get("plugins", []):
        name = entry["name"]
        try:
            plugin_dir = pc.resolve_plugin_dir(entry, fetch=True)
            manifest = pc.plugin_manifest(plugin_dir)
            row = {}
            kind = pc.source_of(entry)
            facts = None
            if kind[0] == "url":
                row["sha"] = kind[2]
                facts = pc.repo_facts(kind[1])
            if facts is not None and "error" in facts:
                # A lookup that FAILED (rate limit, outage) is not a verdict. Keep what the committed
                # index last knew and say so; the validator is where a failed check fails the build.
                prev = previous.get(name, {})
                for key in ("stars", "vetted", "vettedBy"):
                    if key in prev:
                        row[key] = prev[key]
                warnings.append("%s: could not check GitHub (%s); kept the previous verdict" % (name, facts["error"]))
            else:
                if facts:
                    row["stars"] = facts["stars"]
                # Who vetted it and why, shown on the website, and the reason a listing exists at all.
                vetted, by, reason = pc.vet(entry, catalog, facts)
                row["vetted"] = vetted
                if by:
                    row["vettedBy"] = by
            if manifest.get("version"):
                row["version"] = manifest["version"]
            if manifest.get("license"):
                row["license"] = manifest["license"]
            row["components"] = pc.components(plugin_dir)
            index["plugins"][name] = row
        except Exception as exc:
            failures.append("%s: %s" % (name, getattr(exc, "stderr", None) or exc))
    return index, failures, warnings


def dumps(index):
    return json.dumps(index, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main():
    check = "--check" in sys.argv[1:]
    index, failures, warnings = build()
    for w in warnings:
        print("WARN: %s" % w)
    for f in failures:
        print("ERROR: %s" % f)
    if failures:
        return 1
    text = dumps(index)
    if check:
        try:
            with open(OUT, "r", encoding="utf-8") as fh:
                current = json.load(fh)
        except (OSError, ValueError):
            current = {}
        # Star counts drift daily; a stale check on them would fail every PR opened after lunch.
        def without_stars(doc):
            doc = json.loads(json.dumps(doc))
            for row in (doc.get("plugins") or {}).values():
                row.pop("stars", None)
            return doc
        if without_stars(current) != without_stars(index):
            print("ERROR: %s is stale, run scripts/generate_plugin_index.py and commit it" % os.path.relpath(OUT, pc.ROOT))
            return 1
        print("plugin-index.json is current (%d plugins)" % len(index["plugins"]))
        return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    n = {k: sum(len(v["components"].get(k, [])) for v in index["plugins"].values()) for k in ("skills", "mcpServers", "bots")}
    print("Wrote %s: %d plugins, %d skills, %d MCP servers, %d bots"
          % (os.path.relpath(OUT, pc.ROOT), len(index["plugins"]), n["skills"], n["mcpServers"], n["bots"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
