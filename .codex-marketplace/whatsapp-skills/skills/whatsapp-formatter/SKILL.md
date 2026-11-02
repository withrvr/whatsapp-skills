---
name: whatsapp-formatter
description: "Convert or clean text for WhatsApp without rewriting it: ChatGPT or Claude Markdown, emails, docs or notes into WhatsApp formatting (*bold*, _italic_, lists, working links); fix broken markers, weekday-date mistakes, status or caption length, typos and grammar while keeping the sender's words and voice. Modes: convert, polish, check. Use whenever someone pastes text and asks to format, fix, check or make it WhatsApp-ready. Not for writing a message from scratch (use whatsapp-message)."
license: MIT
metadata:
  author: withrvr
  version: "1.0.0"
---

# WhatsApp Formatter

The user already has the text: something an AI wrote in Markdown, an email they
want to send on WhatsApp instead, a notice copied from a PDF, or their own draft
full of typos. They want it to look right in WhatsApp and be correct, **not**
rewritten into something else.

## When to use

- "Format this for WhatsApp", "make this WhatsApp-ready", "convert to WhatsApp"
- "Why are there stars in my message?", "fix the bold"
- "Check this before I send it", "any mistakes?"
- "Fix grammar but keep it mine"
- Pasted Markdown, email text, HTML, or a doc excerpt.

**Not for:** writing from a brief (`whatsapp-message`, `whatsapp-announcement` and
siblings). If the user's text needs a real rewrite (wrong tone, too long by half),
say so in one line and offer to hand it to the matching writer skill.

<!-- BEGIN shared:core-rules -->
## Core rules (every WhatsApp skill)

- **Deliver the final message first**, in a ` ```text ` block, with no preamble. One message unless asked for options. Then `Notes:` (max 3 bullets) only when there's something to act on, never just to confirm a check passed.
- **Never invent facts, never drop them.** Dates, times, venues, prices, names, numbers and links come from the user, copied exactly. Short messages cut words, not facts. Missing and essential → `[placeholder]`, listed in Notes.
- **WhatsApp is not Markdown.** Bold is `*one asterisk*`, italic `_x_`, strike `~x~`. Never `**x**`, `# heading`, `[label](url)`, tables or `---`. Markers hug the text and can't span lines. Never put markers on a link.
- **No em dashes (—) or en dashes (–), ever.** Comma, full stop, colon, "to" or a new line instead. Capitalise names exactly as given. No AI vocabulary (leverage, streamline, delve, foster…). Full list: `references/writing-rules.md` §Voice rules.
- **First two lines carry the point** (what + when, or the ask). Short blocks, one blank line between them.
- **Check weekday ↔ date**, am/pm, time zone and deadlines. Flag anything off in the user's brief.
- **Dials:** length, tone, formatting, emoji, language. Explicit words from the user win, then the audience, then this skill's defaults (`references/message-dials.md`).
- **Before delivering**, if you can run code: save the draft to a temp file with your file-writing tool (not a shell heredoc), then run `python3 <this skill's folder>/scripts/wa_lint.py --kind <kind> <file>` as one standalone command: absolute paths, no `cd`, no `&&`, no shell variables, so it doesn't trip permission checks. Fix every error; weigh the warnings. If you can't run code, use the checklist in `references/whatsapp-formatting.md`. Don't mention the check in your reply unless it found a problem in the user's own brief.
<!-- END shared:core-rules -->

## Modes

Infer the mode from the request; default is **convert**.

| Mode | Triggered by | Changes | Never changes |
|---|---|---|---|
| `convert` | "format", "convert", "WhatsApp-ready" | Formatting, layout, link style, blank lines, em/en dashes (always removed) | Words, order, tone, length |
| `polish` | "fix", "correct", "grammar", "typos", "clean up" | Convert + spelling, grammar, punctuation, obvious clarity fixes | Voice, slang the user chose, facts, length (±10%) |
| `check` | "check", "review", "any mistakes", "is this okay" | Nothing. Reports problems. | The text |

## Workflow

1. **Identify the source**: Markdown (AI output), email, HTML, plain notes, or WhatsApp text that's broken.
2. **Run the converter first if you can execute code**: write the text to a file,
   then `python3 scripts/wa_lint.py --fix input.txt > fixed.txt`. It converts
   `**bold**`, `# headings`, `[label](url)`, tables, `---`, HTML and loose markers,
   and prints remaining problems on stderr. Then review by hand (step 3).
   Without code execution, apply `references/conversion-rules.md` by hand.
3. **Fix what a script can't:**
   - Markdown `*single asterisk*` meant *italic* in the source, but it's **bold** on WhatsApp. If the source is Markdown, change those to `_italic_` (or drop them).
   - Email-isms in `polish` mode only: "Please find attached" → "Attached:"; "Dear Sir/Madam" in a casual group → the audience's greeting. In `convert` mode leave the words.
   - Over-formatting: more than ~20% bold → keep 1-3 anchors.
   - Lead: if the key point is buried in paragraph 3 in `polish` mode, flag it in Notes; don't reorder unless asked.
4. **Check facts and limits**: weekday ↔ date, link intact, status ≤ 700 characters, caption ≤ ~1,024.
5. **Deliver**: the fixed message in a `text` block, then Notes listing what you changed
   in 1-3 bullets (and anything you deliberately didn't change). In `check` mode:
   a short numbered list of problems with the fix for each (plain text, not a code
   block, since it isn't a message to paste), and no rewritten message unless asked.
   Report **every** error and warning the checker (or the checklist) finds, including
   a link without `https://`: a bare `www.` link isn't reliably tappable on every
   phone. Don't overrule a finding by calling it fine; the user decides.

## Example

**Input (from an AI chat):**

```markdown
## Team Lunch 🍕
**When:** Friday, 13 Nov at 1 PM
**Where:** [Toit](https://maps.app.goo.gl/T01t)
- Please *confirm* by Wednesday
```

**Output:**

```text
*Team Lunch 🍕*

*When:* Friday, 13 Nov at 1 PM
*Where:* Toit: https://maps.app.goo.gl/T01t

- Please _confirm_ by Wednesday
```

Notes:
- Converted the heading, bold labels and map link; the single-asterisk *confirm* was Markdown italic, so it's `_confirm_` now.

## References

- `references/conversion-rules.md`: every Markdown/HTML/email pattern and its WhatsApp form, plus polish rules. Load at step 3.
- `references/examples.md`: before/after conversions and a check-mode report.
- `references/whatsapp-formatting.md`: what renders, the full checklist.
- `references/message-dials.md`, `references/writing-rules.md`, `references/links-media-mentions.md`.
- `scripts/wa_lint.py`: `--fix` converts, plain run checks, `--kind status|caption` checks limits.

## Related skills

`whatsapp-message` and siblings (write from a brief) · `whatsapp-reply` (answer a message you got) ·
`whatsapp-redact` (mask sensitive details instead of formatting)
