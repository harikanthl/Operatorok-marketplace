# Operator Marketplace

The open catalog of plugins for [Operator](https://operatorok.com), skills, MCP servers and **bots**
that an Operator app can browse and install. This repo is an index that points at plugin sources;
the app reads the index, shows what a plugin contains, and installs it on your Mac.

It uses the same plugin layout as Claude Code and Grok Build, on purpose: a plugin repo written for
either of those installs into Operator unchanged, and a plugin written for Operator works there too.
What Operator adds is **bots**, a plugin can ship ready-to-talk-to teammates, not only know-how.

> [!WARNING]
> Third-party plugins listed here are developed and provided by their respective authors, not by
> Operator. They are listed as-is, without warranty; a plugin may run code and reach data on your
> machine, and each is governed by its own license and terms. Read what a plugin contains before
> you install it, the app shows you, and `.operator-plugin/plugin-index.json` is the same list.

## Repo layout

| Path | Purpose |
|---|---|
| `.operator-plugin/marketplace.json` | The catalog index, the source of truth |
| `.operator-plugin/plugin-index.json` | Generated component index, never hand-edit |
| `plugins/` | First-party plugins, maintained here |
| `external_plugins/` | Third-party plugins vendored here (most third parties are referenced remotely instead) |
| `scripts/` | Validator and index generator, stdlib Python |

## What a plugin is

A directory bundling any combination of:

| Component | Location | Purpose |
|---|---|---|
| Skills | `skills/<name>/SKILL.md` | Packaged know-how the agent loads on demand; helper files may sit beside it |
| MCP servers | `.mcp.json` | Tools the agent can call: `{"mcpServers": {name: {url…} or {command, args, env}}}` |
| **Bots** | `bots/<id>.json` | An Operator Solution with a `bot` profile: a named teammate with its jobs, skills and connectors |
| Commands | `commands/*.md` | Slash commands (carried for compatibility) |
| Agents | `agents/*.md` | Subagent definitions (carried for compatibility) |
| Hooks | `hooks/hooks.json` | Lifecycle hooks (carried for compatibility) |

An optional `plugin.json` (at the plugin root or under `.operator-plugin/`) adds `version`,
`author`, `license`, `homepage` and `keywords`.

A bot file is the JSON of an Operator Solution, `id`, `name`, `tagline`, `symbol`, `jobs`, and a
`bot` block with `helpsWith`, `agent` and `color`. Its `skillIDs` may name skills from any installed
plugin or from Operator's own catalog. See `plugins/operator-mac-bots/bots/` for the shape.

## Catalog format

`.operator-plugin/marketplace.json`:

```json
{
  "name": "operatorok",
  "description": "Short description of this marketplace",
  "owner": { "name": "Operator" },
  "plugins": []
}
```

Each entry in `plugins`:

| Field | Required | Description |
|---|---|---|
| `name` | yes | kebab-case plugin id, unique in the index |
| `source` | yes | Where the plugin's files come from (below) |
| `description` | yes | Shown when browsing |
| `category` | no | A lowercase slug: `development`, `deployment`, `database`, `research`, `writing`, `mac`, `bots`, … |
| `homepage` | no | Project URL |
| `keywords` | no | Terms that suggest this plugin for a request |
| `domains` | no | Hosts that suggest this plugin when a link is pasted |
| `version`, `author`, `tags` | no | Display metadata |

### Source types

**Remote**, an upstream git repo pinned to a full commit SHA, optionally a subdirectory of it.
Nothing is vendored here; the files are fetched at install time and the checkout is verified to be
that SHA:

```json
{
  "name": "my-plugin",
  "description": "What the plugin does.",
  "category": "development",
  "source": {
    "source": "url",
    "url": "https://github.com/my-org/my-plugin.git",
    "sha": "0000000000000000000000000000000000000000",
    "path": "optional/subdir"
  },
  "homepage": "https://github.com/my-org/my-plugin"
}
```

**Local**, the files live in this repo under `plugins/<name>/` or `external_plugins/<name>/`:

```json
{ "name": "my-plugin", "source": { "source": "local", "path": "./plugins/my-plugin" } }
```

A local plugin installs from this repo itself: the index carries a top-level `repository`, and the
publish step stamps the commit it publishes from as `publishedSha` on the copy it serves
(`scripts/stamp_published.py`). An installer fetches `repository` at `publishedSha` with `path` as
the subdirectory, so a local plugin is pinned exactly like a remote one. The file in the repo never
carries the stamp, because a commit cannot pin itself before it exists.

### SHA pinning

Every remote source pins a 40-character lowercase commit SHA. Without it, a force-push or a
compromised upstream would silently ship new code to everyone who installs or updates. Find it with:

```bash
git ls-remote https://github.com/my-org/my-plugin.git HEAD
```

To roll out an update, bump the SHA (remote) or commit the change (local).

## Vetting, what gets listed

Anyone can open a pull request. Not everything can be listed. The index's `vetting` block is the
rule, and CI enforces it on every pull request:

- A remote plugin is listed when its repo has at least `vetting.minStars` GitHub stars (50), **or**
  its owner is one of `vetting.trustedOwners`, official vendor orgs a maintainer added with the
  reason they are trusted. An archived repo is refused either way.
- A first-party plugin under `plugins/` is vetted by code-owner review.
- The generated index records each plugin's `stars`, `vetted` and `vettedBy`, and the website shows
  them. Star counts are refreshed by the generator and ignored by the staleness check.

Stars are a floor, not a proof of safety. SHA pinning, code-owner review, and the install receipt
(the app shows every skill, tool and bot a plugin brings before anything is kept) are the rest of it.
To list a young official repo, add its org to `trustedOwners` with a reason in the same pull request.

## Add or update a plugin

1. Reference your repo with a remote source, or vendor a first-party plugin under `plugins/`.
2. Add or edit the entry in `.operator-plugin/marketplace.json`.
3. Regenerate the component index and validate:
   ```bash
   python3 scripts/generate_plugin_index.py
   python3 scripts/validate_catalog.py --fetch
   ```
4. Open a pull request. CI runs the same two commands and fails on a bad SHA, a SKILL.md without
   `name`/`description`, an unsafe helper-file path, or a stale index.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Status

The index, validator and generator are what this repo is. The Operator app installs from it:
*Bots → New Bot → Skills → + → Add from marketplace* browses this index, shows a plugin's contents
before anything is fetched, has your paired Mac fetch it at the pinned commit, and offers *Make a
bot* for every bot template it ships. That installer is built and not yet in a released build; until
it ships, a plugin's skills can be added by pasting its `SKILL.md` into the same `+` sheet, and the
Mac's Skill Packs card installs any plugin repo by URL.

What the app keeps from a plugin: every `SKILL.md` with its helper files up to 48 KiB per file and
96 KiB per skill (a worker receives its skills over a bounded channel), every `.mcp.json` server,
and every `bots/*.json`. Larger reference files are listed as skipped on the install receipt, by
name, so a plugin never arrives quietly smaller than it looks here.

## License

The index and scripts are MIT ([LICENSE](LICENSE)). Each plugin carries its own license; the
Hermes skills referenced here are MIT, © 2025 Nous Research.
