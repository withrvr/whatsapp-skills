# Install

Pick the app you use. Every route installs the same 11 skills.

- [claude.ai and Claude Desktop (plugin)](#claudeai-and-claude-desktop-plugin)
- [claude.ai: upload one skill as a zip](#claudeai-upload-one-skill-as-a-zip)
- [Claude Code](#claude-code)
- [ChatGPT](#chatgpt)
- [Codex CLI](#codex-cli)
- [Any agent: `npx skills`](#any-agent-npx-skills)
- [Apps without skills support](#apps-without-skills-support)
- [Updating and removing](#updating-and-removing)

## claude.ai and Claude Desktop (plugin)

1. Open **Customize** in the sidebar, then the **Plugins** tab.
2. Click **Add** → **Add marketplace** → **Add from a repository**.
3. Paste `withrvr/whatsapp-skills` and sync.
4. Switch to **Discover**, find **whatsapp-skills**, click **+** on its card.
5. Switch to **Yours**: it's listed and enabled.
6. Start a new chat: *"WhatsApp message to my manager that I'm on leave tomorrow."*

> Syncing a marketplace only adds the plugin to **Discover**. It isn't installed until you click **+**.
> Skills need a plan that includes them and code execution turned on in Settings.
> If code execution is off, the skills still work; they check drafts by checklist instead of running `wa_lint.py`.

## claude.ai: upload one skill as a zip

If you only want one or two skills, or your workspace can't add a marketplace:

1. Download a zip from [Releases](https://github.com/withrvr/whatsapp-skills/releases)
   (`whatsapp-announcement.zip`, …), or build them: `python3 scripts/build_zips.py` → `dist/`.
2. **Settings** → **Capabilities** → **Skills** → **Upload skill**, and choose the zip.
3. Turn the skill on.

Each zip has one folder with `SKILL.md` at its top, the layout the upload expects.
`whatsapp-skills-all.zip` has all 11 folders, for agents that take a folder of skills.

## Claude Code

### As a plugin (recommended)

```
/plugin marketplace add withrvr/whatsapp-skills
/plugin install whatsapp-skills@whatsapp-skills
```

Skills are then available everywhere. Call one directly with
`/whatsapp-skills:whatsapp-message <notes>`, or just describe the situation.

### Clone and open

```bash
git clone https://github.com/withrvr/whatsapp-skills.git
```

```bash
cd whatsapp-skills && claude
```

The repo ships `.claude/skills/` (symlinks to `skills/`), so Claude Code finds all
11 skills with no install. Call them as `/whatsapp-message`, `/whatsapp-reply`, and so on.

**Windows:** symlinks need Developer Mode (or an elevated shell) plus
`git config --global core.symlinks true` before cloning. Without that, use the
plugin route, or copy the skills as shown next.

### Personal skills (all projects, no plugin)

```bash
mkdir -p ~/.claude/skills && cp -R skills/whatsapp-* ~/.claude/skills/
```

## ChatGPT

The repo carries OpenAI's plugin manifest (`.codex-plugin/plugin.json`) and
marketplace file (`.agents/plugins/marketplace.json`, pointing at the packaged
plugin in `.codex-marketplace/whatsapp-skills/`).

- **Plugins** ([chatgpt.com/plugins](https://chatgpt.com/plugins)): where your
  workspace lets you add a plugin marketplace from GitHub, add
  `withrvr/whatsapp-skills`, then install **WhatsApp Skills**.
- **Skill upload**: where ChatGPT offers uploading a skill, upload a zip from
  [Releases](https://github.com/withrvr/whatsapp-skills/releases), one per skill.
- **Neither available**: use a Project or custom GPT, as described in
  [Apps without skills support](#apps-without-skills-support).

ChatGPT's plugin and skill screens change often and differ by plan; the files
above are the standard formats those screens read.

## Codex CLI

```bash
codex plugin marketplace add withrvr/whatsapp-skills
```

```bash
codex plugin add whatsapp-skills@whatsapp-skills
```

To test a local clone: `codex plugin marketplace add .` from the repo root.

## Any agent: `npx skills`

One command that installs into whichever agents you have (Claude Code, Codex,
Cursor, Gemini CLI, and more):

```bash
npx skills add withrvr/whatsapp-skills
```

Agents that follow the [Agent Skills](https://agentskills.io) standard can also
load the folders in `skills/` directly: copy them into the agent's skills folder.

## Apps without skills support

For a chat app with Projects, custom GPTs, Gems or custom instructions:

1. Pick the skill you use most (usually `whatsapp-message` or `whatsapp-announcement`).
2. Add its `SKILL.md` and the files in its `references/` folder as project knowledge / files.
3. Paste this as the instructions:

   ```
   You write WhatsApp messages. Follow SKILL.md exactly, and read the files in
   references/ when SKILL.md says to. Reply with the final message in a text code
   block first, then at most 3 short notes.
   ```

## Updating and removing

| Where | Update | Remove |
|---|---|---|
| claude.ai / Desktop | Customize → Plugins → sync the marketplace | Customize → Plugins → Yours → remove |
| Claude Code plugin | `/plugin marketplace update whatsapp-skills` | `/plugin uninstall whatsapp-skills@whatsapp-skills` |
| Clone | `git pull` | delete the folder |
| Uploaded zip | upload the new zip | delete the skill in Settings |
| `npx skills` | `npx skills add withrvr/whatsapp-skills` again | delete the `whatsapp-*` skill folders it installed |
