# Working on this repository

Instructions for any coding agent (Codex, Claude Code, others) changing this
repo. If you're here to **write a WhatsApp message**, ignore this file and use
the skills in `skills/`: describe the situation and the matching skill applies.

## What this repo is

Eight [Agent Skills](https://agentskills.io/specification) that turn a user's
context into a ready-to-paste WhatsApp message. Draft-only: no sending, no
WhatsApp API, no automation, no network calls. Keep it that way.

## Golden rules

1. **Shared content has one source.** Edit `shared/references/*.md`,
   `shared/scripts/wa_lint.py` and `shared/snippets/core-rules.md`, then run
   `python3 scripts/sync.py`. Never edit the generated copies in
   `skills/*/references/` (they start with a `GENERATED` comment), the
   `skills/*/scripts/wa_lint.py` copies, the text between the
   `<!-- BEGIN/END shared:core-rules -->` markers in a SKILL.md, or anything in
   `.codex-marketplace/`.
2. **Version lives in `.claude-plugin/plugin.json` only.** `sync.py` copies it
   into the other manifests and every SKILL.md `metadata.version`.
3. **Run the checks before every commit:**

   ```bash
   python3 scripts/sync.py --check && python3 scripts/validate.py && python3 -m unittest discover -s tests
   ```

4. **Examples are part of the product.** Every ```` ```text ```` block in
   `skills/*/references/examples.md` must pass `wa_lint.py` with no errors and no
   warnings (tests enforce it with today = 2026-11-02). Check weekdays against a
   calendar; the linter will catch a mismatch if you don't.

## Skill invariants

- Directory name = `name` = `whatsapp-<what>`. Lowercase, hyphens, ≤ 64 chars.
- Frontmatter fields only from the spec: `name`, `description`, `license`,
  `metadata` (string values), optionally `compatibility`, `allowed-tools`.
- `description` ≤ 600 chars, no em or en dashes, includes a "Use whenever …"
  trigger and a "Not for … (use whatsapp-…)" sentence pointing at real siblings.
- `SKILL.md` body under 500 lines and ~5,000 tokens. Detail goes in `references/`,
  each file mentioned from SKILL.md with when to load it (no orphans).
- Every skill ships `references/examples.md` (≥ 4 worked examples) and
  `evals/evals.json` (≥ 3 cases).
- Renaming or adding a skill: update the README skill table, `docs/SCENARIOS.md`,
  sibling "Not for" / "Related skills" lines, the skill count in the manifests'
  descriptions, then sync.

## Evals

`skills/*/evals/evals.json` follows the spec's eval format (`prompt`,
`expected_output`, `assertions`) plus `checks`, which `scripts/run_evals.py`
grades mechanically. Run them after any change to instructions:

```bash
python3 scripts/run_evals.py --baseline
```

Results land in `evals-workspace/` (git-ignored). Read failing transcripts
(`transcript.jsonl`) before changing a skill: fix the instruction that caused
the behaviour, in general terms, not a patch for one prompt.

## Releases

1. Bump `version` in `.claude-plugin/plugin.json` (semver), run `python3 scripts/sync.py`.
2. Add a `CHANGELOG.md` entry.
3. Commit, tag `vX.Y.Z`, push the tag. The release workflow builds the skill zips and publishes them.

## Style for skill text

- Write what the model wouldn't know without the skill: WhatsApp rendering
  rules, chat-bubble layout, the user's real situations. Skip generic writing advice.
- Give defaults, not menus. Explain the why in one clause when a rule seems arbitrary.
- No mention of other skill bundles or their authors.
