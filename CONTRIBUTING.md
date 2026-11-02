# Contributing

Thanks for helping. The most valuable contributions are real-world ones: a
situation the skills handle badly, a language or culture they get wrong, a
WhatsApp behaviour that changed.

## Easy ways to help

- **Report a bad message.** Open an issue with your brief (remove private
  details), what you got, and what you expected.
- **Request a scenario.** Something you send often that isn't in
  [docs/SCENARIOS.md](docs/SCENARIOS.md).
- **Add an example** to a skill's `references/examples.md`: a realistic brief and
  the message you'd actually send. Especially welcome: Hindi, Marathi, Tamil,
  Telugu, Bengali, Gujarati, Urdu, Arabic, Spanish, Portuguese, Indonesian.
- **Correct a WhatsApp fact** (a limit, a formatting rule, a feature) with a source.

## Setup

```bash
git clone https://github.com/withrvr/whatsapp-skills.git
```

```bash
cd whatsapp-skills && pip install -r requirements-dev.txt
```

## Where things live

| You want to change | Edit | Then |
|---|---|---|
| Formatting rules, dials, writing rules, links/media | `shared/references/*.md` | `python3 scripts/sync.py` |
| The checker | `shared/scripts/wa_lint.py` (+ tests in `tests/test_wa_lint.py`) | `python3 scripts/sync.py` |
| Rules every skill shows up front | `shared/snippets/core-rules.md` | `python3 scripts/sync.py` |
| One skill's workflow or playbook | `skills/<name>/SKILL.md`, `skills/<name>/references/<playbook>.md` | — |
| Examples | `skills/<name>/references/examples.md` | tests lint them |
| Eval cases | `skills/<name>/evals/evals.json` | `python3 scripts/run_evals.py --skill <name>` |

Never edit files that start with a `GENERATED` comment; edit their source in `shared/`.

## Before you open a PR

```bash
python3 scripts/sync.py --check && python3 scripts/validate.py && python3 -m unittest discover -s tests
```

If you changed skill instructions and have Claude Code installed, also run the
evals for that skill and mention the result in the PR:

```bash
python3 scripts/run_evals.py --skill whatsapp-announcement --baseline
```

## Writing examples

- Briefs look like real typing: lowercase, out of order, abbreviations.
- Outputs are what you'd actually send. Exact facts, no invented details.
- Check every weekday against a calendar (the tests use 2026-11-02 as "today").
- No real people's phone numbers, addresses or names you don't have permission to use.

## Ground rules

- Draft-only. No features that send messages, call WhatsApp APIs or automate accounts.
- Nothing that helps write scams, impersonation, chain messages or spam.
