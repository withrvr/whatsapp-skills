# How it works

What the skills do differently, how the output is checked, and how they're tested.
For installing see [INSTALL.md](INSTALL.md); for everyday use see [USAGE.md](USAGE.md).

## Why the output is right

- **WhatsApp formatting, not Markdown.** `*bold*`, `_italic_`, `~strike~`, lists and quotes that render. Never `**bold**`, `# headings`, `[links](…)` or tables, the habits that show up as junk in a chat.
- **Facts are copied, never invented.** Links character for character, numbers, names and amounts exact. If something essential is missing you get a `[placeholder]` and a note, not a guess.
- **Weekday ↔ date checking.** "Friday, 7 Nov" when 7 Nov is a Saturday gets caught and flagged.
- **Built for the chat bubble.** The point in the first two lines, short blocks, labeled logistics (📅 ⏰ 📍), links that get a preview, captions that work with media, notes on re-tagging `@mentions`.
- **A checker in every skill.** [`wa_lint.py`](../shared/scripts/wa_lint.py) (Python standard library only) checks each draft before it's handed over: Markdown leaks, markers that won't render, broken links, any em or en dash, weekday/date mismatches, the 700-character status limit, placeholders, chain-message patterns, card/Aadhaar/PAN/OTP numbers. `--fix` converts Markdown to WhatsApp; `--redact` masks sensitive values.

## Voice rules

Every skill follows a short list of voice rules, and the built-in checker
enforces the mechanical ones before a message reaches you: no em or en dashes,
names capitalised as given, no AI or email vocabulary, specific beats vague, one
point per message, emoji as labels, name-only sign-offs, and more.

The full, current list lives in one place, the file the skills themselves read:
[`shared/references/writing-rules.md`](../shared/references/writing-rules.md#voice-rules).

## Languages

The skills are written and tested in **English**, which is the main focus. Ask
for any other language and the model writes it natively: Hinglish, Hindi,
Marathi, Tamil, Telugu, Bengali, Gujarati, Urdu, Arabic, Spanish, Portuguese,
Indonesian and more. The same rules apply in every language: exact facts,
WhatsApp formatting, no dashes. Examples in other languages are especially
welcome as contributions ([CONTRIBUTING.md](../CONTRIBUTING.md)).

## Tested against a real model

Every skill ships evals in the [Agent Skills format](https://agentskills.io/skill-creation/evaluating-skills)
(`skills/*/evals/evals.json`): 33 realistic prompts, including traps like a
weekday that doesn't match its date, a request for fake "only 2 hours left"
urgency, a "Hi Mom, new number" scam, a venue that changes halfway through a
chat, a suggestion that must not be reported as a decision, Devanagari output,
Markdown input, and phone numbers that must be masked. `scripts/run_evals.py`
runs each prompt through Claude Code with and without the skills and grades the
output with deterministic checks.

| Out of 33 test requests | Plain AI | With the skills |
|---|---|---|
| Messages with `**stars**` showing instead of bold | 25 | **0** |
| Messages with em or en dashes | 10 | **0** |
| All automated checks passed (formatting, dates, facts, safety) | 60% | **99%** |

Same model and same requests both times; only the skills changed. Without them
the model also left a phone number visible when asked to hide them, and answered
"write my status" with 240 to 880 characters of options instead of one status.
With the skills, a matching skill picked itself up in 32 of 33 runs without being
named; the other was a one-line typo fix the model did directly.

## Repository layout

```
skills/<name>/            one folder per skill, self-contained (spec-compliant)
  SKILL.md                instructions + shared core rules
  references/             playbooks, examples, shared formatting/dials/rules
  scripts/wa_lint.py      the pre-send checker and sensitive-data masker
  evals/evals.json        test prompts, assertions and checks
skills/whatsapp-catchup/scripts/wa_chat.py   chat-export parser
shared/                   single source for everything copied into skills
scripts/                  sync, validate, evals, zip builder
docs/                     install, usage, scenario catalog, how it works
media/demo/               README demo loop: demo.html, render.js, build.sh
.claude-plugin/           Claude plugin + marketplace manifests
.codex-plugin/, .agents/  OpenAI (Codex / ChatGPT) plugin + marketplace
.claude/skills/           symlinks so Claude Code finds the skills on clone
tests/                    offline test suite
```

## Development

```bash
pip install -r requirements-dev.txt
```

```bash
python3 scripts/sync.py && python3 scripts/validate.py && python3 -m unittest discover -s tests
```

```bash
python3 scripts/run_evals.py --baseline
```

Edit shared content in `shared/`, never the generated copies in `skills/*/references/`.
Contributions, especially new scenarios and languages, are welcome:
**[CONTRIBUTING.md](../CONTRIBUTING.md)**.

## Privacy

The skills are instructions and a local script. They make no network calls and
store nothing. Your messages go only where your AI app already sends your chats.
