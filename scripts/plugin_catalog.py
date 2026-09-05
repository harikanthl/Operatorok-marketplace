"""Shared reader for the Operator plugin marketplace. Stdlib only.

One index file (`.operator-plugin/marketplace.json`) lists plugins; each plugin is a directory that
bundles skills (`skills/*/SKILL.md`), MCP servers (`.mcp.json`), bots (`bots/*.json`) and, optionally,
commands, agents and hooks. The directory comes from a `source`: a path inside this repo, or a git
URL pinned to a full commit SHA.

The same layout as the Claude Code / Grok Build plugin format, so a vendor's existing plugin repo
installs unchanged. Index folders are read in this order: `.operator-plugin`, `.claude-plugin`,
`.grok-plugin` — ours first, the others so a foreign repo can be pointed at directly.
"""

import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_DIRS = (".operator-plugin", ".claude-plugin", ".grok-plugin")
CACHE = os.path.join(ROOT, ".cache", "sources")

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
# A helper file beside a SKILL.md: relative, forward slashes, no dot-segments, no hidden files.
SAFE_PATH_RE = re.compile(r"^(?!SKILL\.md$)[A-Za-z0-9_][A-Za-z0-9_.\-]*(/[A-Za-z0-9_][A-Za-z0-9_.\-]*)*$")


class CatalogError(Exception):
    pass


# ── index ───────────────────────────────────────────────────────────────────────────────────────

def index_path(root=ROOT):
    for d in INDEX_DIRS:
        p = os.path.join(root, d, "marketplace.json")
        if os.path.isfile(p):
            return p
    raise CatalogError("no marketplace.json under %s" % ", ".join(INDEX_DIRS))


def load_marketplace(root=ROOT):
    with open(index_path(root), "r", encoding="utf-8") as fh:
        return json.load(fh)


def source_of(entry):
    """Normalise the two spellings in the wild: `{"source": "url", ...}` / `{"type": "local", ...}`.

    Returns ("local", path) or ("url", url, sha, subpath)."""
    src = entry.get("source")
    if not isinstance(src, dict):
        raise CatalogError("source must be an object")
    kind = src.get("source") or src.get("type")
    if kind == "local":
        return ("local", src.get("path"))
    if kind in ("url", "git", "github"):
        return ("url", src.get("url"), src.get("sha"), src.get("path"))
    raise CatalogError("unknown source kind %r" % (kind,))


# ── resolving a plugin directory ────────────────────────────────────────────────────────────────

def _git(args, cwd):
    env = {"PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", ""),
           "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_NOSYSTEM": "1"}
    return subprocess.run(["git"] + args, cwd=cwd, env=env, check=True,
                          capture_output=True, text=True).stdout.strip()


def resolve_plugin_dir(entry, root=ROOT, fetch=True, cache=CACHE):
    """The directory holding the plugin's files. Remote sources are fetched at their pinned SHA into
    `.cache/sources/<name>-<sha>` and the checkout is verified to BE that SHA before use."""
    kind = source_of(entry)
    if kind[0] == "local":
        path = kind[1]
        full = os.path.normpath(os.path.join(root, path))
        if not full.startswith(root + os.sep):
            raise CatalogError("local path %r escapes the repo" % path)
        if not os.path.isdir(full):
            raise CatalogError("local path %r does not exist" % path)
        return full
    _, url, sha, subpath = kind
    if not fetch:
        return None
    os.makedirs(cache, exist_ok=True)
    dest = os.path.join(cache, "%s-%s" % (entry["name"], sha))
    if not os.path.isdir(os.path.join(dest, ".git")):
        os.makedirs(dest, exist_ok=True)
        _git(["init", "--quiet"], dest)
        _git(["remote", "add", "origin", url], dest)
        # Fetch exactly the pinned commit — never a branch tip.
        _git(["fetch", "--quiet", "--depth", "1", "origin", sha], dest)
        _git(["checkout", "--quiet", "--detach", "FETCH_HEAD"], dest)
    head = _git(["rev-parse", "HEAD"], dest)
    if head != sha:
        raise CatalogError("%s: checkout is %s, not the pinned %s" % (entry["name"], head, sha))
    plugin_dir = os.path.normpath(os.path.join(dest, subpath)) if subpath else dest
    if not plugin_dir.startswith(dest):
        raise CatalogError("%s: source.path escapes the checkout" % entry["name"])
    if not os.path.isdir(plugin_dir):
        raise CatalogError("%s: source.path %r not found at %s" % (entry["name"], subpath, sha[:8]))
    return plugin_dir


# ── a plugin's contents ─────────────────────────────────────────────────────────────────────────

def parse_frontmatter(text):
    """(attrs, body) from a `---` fenced block. Folded (`>-`) and continuation lines are joined; a
    nested object is kept as its raw lines under the key. Good enough to read name/description."""
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    block, body = text[4:end], text[end + 4:].lstrip("\n")
    attrs, key = {}, None
    for line in block.split("\n"):
        if line[:1] in (" ", "\t") and key:
            attrs[key] = (attrs[key] + " " + line.strip()).strip()
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip().strip("\"'"), value.strip()
        if value in (">", ">-", "|", "|-"):
            value = ""
        attrs[key] = value.strip("\"'")
    return attrs, body


def plugin_manifest(plugin_dir):
    for d in INDEX_DIRS + ("",):
        p = os.path.join(plugin_dir, d, "plugin.json") if d else os.path.join(plugin_dir, "plugin.json")
        if os.path.isfile(p):
            with open(p, "r", encoding="utf-8") as fh:
                return json.load(fh)
    return {}


def _shorten(s, n=120):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def components(plugin_dir):
    """What a plugin provides, in the shape `plugin-index.json` records."""
    out = {}
    skills = []
    skills_root = os.path.join(plugin_dir, "skills")
    walk_root = skills_root if os.path.isdir(skills_root) else plugin_dir
    for dirpath, dirnames, filenames in os.walk(walk_root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d != "node_modules")
        if "SKILL.md" in filenames:
            # A skill's own subfolders are its files, never further skills — a nested SKILL.md
            # (Vercel vendors upstream skills under `skills/flags-sdk/upstream/`) rides along as a
            # reference. The same rule the app's reader applies, so the count shown before install
            # is the count that arrives.
            dirnames[:] = []
            with open(os.path.join(dirpath, "SKILL.md"), "r", encoding="utf-8") as fh:
                attrs, body = parse_frontmatter(fh.read())
            rel = os.path.relpath(dirpath, walk_root).replace(os.sep, "/")
            skills.append({
                "name": attrs.get("name") or os.path.basename(dirpath),
                "description": _shorten(attrs.get("description")),
                "path": rel if rel != "." else "",
                "hasBody": bool(body.strip()),
                "files": sorted(
                    os.path.relpath(os.path.join(dp, f), dirpath).replace(os.sep, "/")
                    for dp, dn, fn in os.walk(dirpath)
                    for f in fn if f != "SKILL.md" and not f.startswith(".")
                ),
            })
    if skills:
        out["skills"] = sorted(skills, key=lambda s: s["name"])

    mcp = os.path.join(plugin_dir, ".mcp.json")
    if os.path.isfile(mcp):
        with open(mcp, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
        servers = doc.get("mcpServers", doc) if isinstance(doc, dict) else {}
        rows = []
        for name, cfg in sorted(servers.items()):
            if not isinstance(cfg, dict):
                continue
            transport = cfg.get("type") or ("http" if cfg.get("url") else "stdio")
            rows.append({"name": name, "transport": transport,
                         **({"url": cfg["url"]} if cfg.get("url") else {}),
                         **({"command": cfg["command"]} if cfg.get("command") else {})})
        if rows:
            out["mcpServers"] = rows

    bots_dir = os.path.join(plugin_dir, "bots")
    if os.path.isdir(bots_dir):
        rows = []
        for f in sorted(os.listdir(bots_dir)):
            if not f.endswith(".json"):
                continue
            with open(os.path.join(bots_dir, f), "r", encoding="utf-8") as fh:
                bot = json.load(fh)
            profile = bot.get("bot") or {}
            rows.append({"id": bot.get("id"), "name": bot.get("name"),
                         "tagline": _shorten(bot.get("tagline")),
                         "agent": profile.get("agent"),
                         # The bot's colour, so a browser can draw its face before install.
                         "color": profile.get("color"),
                         "helpsWith": _shorten(profile.get("helpsWith"), 160),
                         "skills": bot.get("skillIDs", [])})
        if rows:
            out["bots"] = rows

    for kind in ("commands", "agents"):
        d = os.path.join(plugin_dir, kind)
        if os.path.isdir(d):
            names = sorted(os.path.splitext(f)[0] for f in os.listdir(d) if f.endswith(".md"))
            if names:
                out[kind] = names
    if os.path.isfile(os.path.join(plugin_dir, "hooks", "hooks.json")):
        out["hooks"] = True
    return out


# ── vetting ─────────────────────────────────────────────────────────────────────────────────────
#
# Anyone can open a pull request; not everything can be listed. A remote plugin is vetted when its
# repo has at least `vetting.minStars` GitHub stars, OR its owner is a trusted org the index names
# with a reason. A local (first-party) plugin is vetted by code-owner review. Archived repos are
# refused. Stars are a floor, not a proof of safety — SHA pinning, the install receipt and review are
# the rest of it — but they keep a two-day-old repo nobody has looked at off the site.

GITHUB_REPO_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$")


def github_repo(url):
    m = GITHUB_REPO_RE.match(url or "")
    return (m.group(1), m.group(2)) if m else None


def repo_facts(url, cache={}):
    """{'stars', 'archived', 'owner', 'ownerType'} from the GitHub API, or None when the repo is not
    on GitHub or the API is unreachable. Uses GITHUB_TOKEN when set (CI always has one)."""
    import json as _json
    import urllib.request
    repo = github_repo(url)
    if not repo:
        return None
    key = "/".join(repo)
    if key in cache:
        return cache[key]
    headers = {"User-Agent": "operatorok-marketplace", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    try:
        req = urllib.request.Request("https://api.github.com/repos/%s" % key, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            d = _json.load(resp)
        facts = {"stars": int(d.get("stargazers_count") or 0), "archived": bool(d.get("archived")),
                 "owner": (d.get("owner") or {}).get("login") or repo[0],
                 "ownerType": (d.get("owner") or {}).get("type")}
    except Exception as exc:  # noqa: BLE001 — any failure is "could not check", reported by the caller
        facts = {"error": str(exc)}
    cache[key] = facts
    return facts


def vet(entry, catalog, facts=None):
    """(vetted: bool, vettedBy: str, reason: str) for one catalog entry."""
    policy = catalog.get("vetting") or {}
    min_stars = int(policy.get("minStars") or 0)
    trusted = policy.get("trustedOwners") or {}
    kind = source_of(entry)
    if kind[0] == "local":
        return True, "first-party", "vendored in this repo; code-owner review"
    url = kind[1]
    repo = github_repo(url)
    if not repo:
        return False, "", "not a GitHub repo; only GitHub sources can be vetted today"
    owner = repo[0]
    if facts is None:
        facts = repo_facts(url)
    if facts is None or "error" in facts:
        return False, "", "could not check the repo (%s)" % ((facts or {}).get("error") or "no facts")
    if facts.get("archived"):
        return False, "", "the repo is archived"
    for name, why in trusted.items():
        if name.lower() == owner.lower():
            return True, "trusted-owner", "%s (%s)" % (name, why)
    if facts.get("stars", 0) >= min_stars:
        return True, "stars", "%d stars (floor %d)" % (facts["stars"], min_stars)
    return False, "", "%d stars, below the floor of %d, and %s is not a trusted owner" % (facts.get("stars", 0), min_stars, owner)
