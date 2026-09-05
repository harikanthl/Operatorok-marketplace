#!/usr/bin/env python3
"""Validate `.operator-plugin/marketplace.json` and every local plugin it lists.

    python3 scripts/validate_catalog.py            # index + local plugins
    python3 scripts/validate_catalog.py --fetch    # also fetch every remote source at its SHA

Exit 1 on any error. Remote sources are only fetched with --fetch (CI does); without it the
entry's shape is still checked — a missing or short SHA fails either way.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plugin_catalog as pc  # noqa: E402

errors = []
warnings = []


def error(where, msg):
    errors.append("%s: %s" % (where, msg))


def warn(where, msg):
    warnings.append("%s: %s" % (where, msg))


def report(strict):
    """Local plugins are ours to fix, so their findings are errors. A remote plugin's are facts
    about someone else's repo: the installer skips what it cannot take, so they are warnings."""
    return error if strict else warn


def check_entry(entry, seen):
    name = entry.get("name")
    loc = "plugins[%s]" % (name or "?")
    if not isinstance(name, str) or not pc.NAME_RE.match(name):
        error(loc, "name must be a kebab-case slug")
        return None
    if name in seen:
        error(loc, "duplicate plugin name")
    seen.add(name)
    if not isinstance(entry.get("description"), str) or not entry["description"].strip():
        error(loc, "description is required (it is what people browse)")
    cat = entry.get("category")
    if cat is not None and (not isinstance(cat, str) or not pc.NAME_RE.match(cat)):
        error(loc, "category must be a lowercase slug")
    for key in ("keywords", "domains", "tags"):
        v = entry.get(key)
        if v is not None and (not isinstance(v, list) or not all(isinstance(x, str) for x in v)):
            error(loc, "%s must be a list of strings" % key)
    try:
        kind = pc.source_of(entry)
    except pc.CatalogError as exc:
        error(loc, str(exc))
        return None
    if kind[0] == "local":
        path = kind[1]
        if not isinstance(path, str) or not path.startswith("./"):
            error(loc, "local source.path must start with './'")
    else:
        _, url, sha, subpath = kind
        if not isinstance(url, str) or not re.match(r"^https://[^\s]+\.git$", url):
            error(loc, "source.url must be an https git URL ending in .git")
        if not isinstance(sha, str) or not pc.SHA_RE.match(sha):
            error(loc, "source.sha must be a full 40-character lowercase commit SHA (git ls-remote <url> HEAD)")
        if subpath is not None and (not isinstance(subpath, str) or subpath.startswith("/") or ".." in subpath.split("/")):
            error(loc, "source.path must be a relative path inside the repo")
    return name


def check_skill_dir(loc, dirpath, strict=True):
    with open(os.path.join(dirpath, "SKILL.md"), "r", encoding="utf-8") as fh:
        attrs, body = pc.parse_frontmatter(fh.read())
    if not attrs:
        error(loc, "SKILL.md has no frontmatter")
        return
    for key in ("name", "description"):
        if not attrs.get(key):
            error(loc, "SKILL.md frontmatter is missing `%s`" % key)
    if not body.strip():
        error(loc, "SKILL.md has an empty body")
    for dp, dn, fn in os.walk(dirpath):
        dn[:] = [d for d in dn if not d.startswith(".")]
        for f in fn:
            if f == "SKILL.md" and dp == dirpath:
                continue
            rel = os.path.relpath(os.path.join(dp, f), dirpath).replace(os.sep, "/")
            if not pc.SAFE_PATH_RE.match(rel):
                report(strict)(loc, "helper file path %r is not safe (no hidden files, dot-segments or SKILL.md)"
                                    "%s" % (rel, "" if strict else " — the installer will skip this file"))


def check_bot(loc, path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            bot = json.load(fh)
    except ValueError as exc:
        error(loc, "not valid JSON (%s)" % exc)
        return
    for key in ("id", "name", "tagline", "symbol", "jobs"):
        if key not in bot:
            error(loc, "bot is missing `%s`" % key)
    if bot.get("id") and bot["id"] != os.path.splitext(os.path.basename(path))[0]:
        error(loc, "file is named %s but the bot's id is %r" % (os.path.basename(path), bot["id"]))
    if not isinstance(bot.get("bot"), dict):
        error(loc, "a bot needs a `bot` profile block (helpsWith, agent, color)")
    if not isinstance(bot.get("jobs"), list) or not bot["jobs"]:
        error(loc, "a bot needs at least one job (the first is what installs)")


def check_plugin_dir(name, plugin_dir, strict=True):
    loc = "plugins[%s]" % name
    manifest = pc.plugin_manifest(plugin_dir)
    if manifest and manifest.get("name") not in (None, name):
        report(strict)(loc, "plugin.json name %r differs from the catalog entry" % manifest.get("name"))
    comps = pc.components(plugin_dir)
    if not comps:
        error(loc, "plugin provides nothing (no skills/, .mcp.json, bots/, commands/, agents/ or hooks/)")
    skills_root = os.path.join(plugin_dir, "skills")
    walk_root = skills_root if os.path.isdir(skills_root) else plugin_dir
    for dirpath, dirnames, filenames in os.walk(walk_root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        if "SKILL.md" in filenames:
            check_skill_dir("%s/%s" % (loc, os.path.relpath(dirpath, plugin_dir)), dirpath, strict)
    bots_dir = os.path.join(plugin_dir, "bots")
    if os.path.isdir(bots_dir):
        for f in sorted(os.listdir(bots_dir)):
            if f.endswith(".json"):
                check_bot("%s/bots/%s" % (loc, f), os.path.join(bots_dir, f))
    mcp = os.path.join(plugin_dir, ".mcp.json")
    if os.path.isfile(mcp):
        try:
            with open(mcp, "r", encoding="utf-8") as fh:
                doc = json.load(fh)
            servers = doc.get("mcpServers") if isinstance(doc, dict) else None
            if not isinstance(servers, dict) or not servers:
                error(loc, ".mcp.json must be {\"mcpServers\": {name: config}}")
            else:
                for sname, cfg in servers.items():
                    if not isinstance(cfg, dict) or not (cfg.get("url") or cfg.get("command")):
                        error(loc, ".mcp.json server %r needs a url (http) or a command (stdio)" % sname)
        except ValueError as exc:
            error(loc, ".mcp.json is not valid JSON (%s)" % exc)


def main():
    fetch = "--fetch" in sys.argv[1:]
    try:
        catalog = pc.load_marketplace()
    except (pc.CatalogError, ValueError) as exc:
        print("ERROR: %s" % exc)
        return 1
    for key in ("name", "description", "owner"):
        if key not in catalog:
            error("marketplace", "missing top-level `%s`" % key)
    plugins = catalog.get("plugins")
    if not isinstance(plugins, list):
        error("marketplace", "`plugins` must be a list")
        plugins = []
    seen = set()
    for entry in plugins:
        if not isinstance(entry, dict):
            error("plugins[]", "entry is not an object")
            continue
        name = check_entry(entry, seen)
        if not name:
            continue
        kind = pc.source_of(entry)[0]
        if kind == "url" and not fetch:
            continue
        try:
            plugin_dir = pc.resolve_plugin_dir(entry, fetch=fetch)
        except (pc.CatalogError, OSError) as exc:
            error("plugins[%s]" % name, str(exc))
            continue
        except Exception as exc:  # git failures carry their stderr
            error("plugins[%s]" % name, "fetch failed: %s" % getattr(exc, "stderr", exc))
            continue
        if plugin_dir:
            check_plugin_dir(name, plugin_dir, strict=(kind == "local"))
    # Local plugin directories that nothing lists are a gap, not an oversight to leave silent.
    listed_local = set()
    for entry in plugins:
        if isinstance(entry, dict):
            try:
                k = pc.source_of(entry)
                if k[0] == "local":
                    listed_local.add(os.path.normpath(os.path.join(pc.ROOT, k[1])))
            except pc.CatalogError:
                pass
    for tree in ("plugins", "external_plugins"):
        base = os.path.join(pc.ROOT, tree)
        if os.path.isdir(base):
            for d in sorted(os.listdir(base)):
                full = os.path.join(base, d)
                if os.path.isdir(full) and full not in listed_local:
                    error("%s/%s" % (tree, d), "directory exists but no catalog entry points at it")

    for w in warnings:
        print("WARN: %s" % w)
    for e in errors:
        print("ERROR: %s" % e)
    n_remote = sum(1 for p in plugins if isinstance(p, dict) and (p.get("source") or {}).get("source") == "url")
    print("Validated %d plugin(s), %d remote%s — %s" % (
        len(plugins), n_remote, " (fetched)" if fetch else " (shape only; --fetch to resolve)",
        "%d error(s)" % len(errors) if errors else "OK"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
