# Contributing

Thanks for adding to the Operator Marketplace. A contribution is one entry in
`.operator-plugin/marketplace.json`, and for a first-party plugin, the files under `plugins/`.

## Listing your plugin (most contributions)

Your plugin lives in your own repo, in the standard layout (`skills/<name>/SKILL.md`, an optional
`.mcp.json`, optional `bots/<id>.json`, optional `plugin.json`). If it already installs into Claude
Code or Grok Build, it is ready.

1. Pin the commit: `git ls-remote https://github.com/you/your-plugin.git HEAD`.
2. Append an entry to `plugins` in `.operator-plugin/marketplace.json` with `name`, `description`,
   `category`, a remote `source` (`url`, `sha`, optional `path`), and `homepage`. Add `keywords`
   and `domains` so the app can suggest your plugin when someone mentions your product or pastes
   your URL.
3. Run
   ```bash
   python3 scripts/generate_plugin_index.py
   python3 scripts/validate_catalog.py --fetch
   ```
   and commit the regenerated `.operator-plugin/plugin-index.json` with your entry.
4. Open a pull request. Say what the plugin does, what it reaches (which hosts, which
   credentials), and its license.

To ship an update later, bump the `sha` and regenerate the index.

## Writing a bot

A bot is a JSON file under `bots/` in your plugin: an Operator Solution with a `bot` profile.
Copy one from `plugins/operator-mac-bots/bots/` and change:

- `id`, `name`, `tagline`, `blurb`, `symbol`, how it appears.
- `bot.helpsWith`, one or two sentences on what it is for; this is the soul of the teammate.
- `bot.agent`, `claude`, `hermes`, `pi`, `grok`, or another agent Operator knows.
- `jobs`, the first job is what installs; a conversational bot's first job uses the `bot-chat@1`
  contract. Further jobs are the things it can do when asked.
- `skillIDs`, skills from your plugin or from Operator's catalog, by id.
- `connectorIDs`, integrations the bot needs (`gmail`, `github`, …), so the app asks for them.

Keep bots honest: a bot that claims a capability it does not have is the one failure people do not
forgive. Every job should name its contract or its prompt.

## Ground rules

- **Pin, never float.** A remote source without a full SHA is rejected by CI.
- **Text only in skills.** Helper files beside a `SKILL.md` are text; paths are relative, no hidden
  files, no `..`.
- **Say what it reaches.** MCP servers and skills that call out to a service must say so in the
  plugin description, and the credentials they need must be named in the PR.
- **Your license, stated.** Put it in `plugin.json` (`license`) or your repo. Vendored third-party
  plugins under `external_plugins/` must carry their upstream license file.
- **No secrets in the repo.** Ever. A `.mcp.json` names an env var; it never holds a value.

Code-owner review is required to merge.
