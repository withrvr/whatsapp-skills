# Conversion rules

## Markdown → WhatsApp

| Source | WhatsApp | Script (`--fix`) handles it |
|---|---|---|
| `**bold**`, `__bold__` | `*bold*` | yes |
| `***bold italic***` | `*_bold italic_*` | yes |
| `*italic*` (single, Markdown source) | `_italic_` | **no**: decide by source. In Markdown it's italic; on WhatsApp it would turn bold. |
| `_italic_` | `_italic_` | unchanged |
| `~~strike~~` | `~strike~` | no: replace by hand |
| `# Heading` … `###### Heading` | `*Heading*` on its own line | yes |
| `[label](https://url)` | `label: https://url` | yes |
| `[https://url](https://url)` | `https://url` | yes |
| `www.site.com` | `https://www.site.com` | yes |
| Table | header row bold, one line per row, cells joined with ` · ` | yes |
| `---`, `***`, `___` rules | blank line | yes |
| `+ item` | `- item` | yes |
| Indented sub-bullets | flattened | yes (indent removed; regroup by hand if meaning depends on nesting) |
| `> quote` | `> quote` | unchanged (renders) |
| `` `code` `` | `` `code` `` | unchanged (renders) |
| ```` ```python ```` fenced code | ```` ``` ```` (language tag dropped) | yes |
| `![image](url)` | the URL on its own line, or "image attached" | no |
| Footnotes `[^1]` | inline "(source: …)" | no |
| Emoji shortcodes `:tada:` | the emoji 🎉 | no |

## Dashes (all modes, even convert)

Em dashes (—) and en dashes (–) are removed in every mode, because they mark text as
AI-written. `--fix` does it: `2–4` → `2-4`, `10 am – 6 pm` → `10 am to 6 pm`,
a dash starting a sign-off line is dropped, any other dash becomes a comma.
Re-read the sentence after: sometimes a full stop or colon reads better than the comma.

## HTML → WhatsApp

`<b>`/`<strong>` → `*x*` · `<i>`/`<em>` → `_x_` · `<s>`/`<del>` → `~x~` ·
`<br>` → line break · `<li>` → `- ` · `<a href="u">t</a>` → `t: u` · other tags removed. All handled by `--fix`.

## Email → WhatsApp (polish mode only)

| Email habit | WhatsApp |
|---|---|
| "Dear Sir/Madam," | Greeting for the actual audience, or none in a group with a headline |
| "I hope this email finds you well." | Remove |
| "I am writing to inform you that…" | Start with the information |
| "Please find attached…" | "Attached: [what]" |
| "Kindly revert at the earliest." | "Please reply by [time]." |
| "Thanks & Regards, Name, Title, Company, phone…" | The name on its own last line (+ role if it matters) |
| Long paragraphs | 1-3 line blocks |
| Subject line | Bold headline line |

In `convert` mode keep the words and only fix the layout.

## Broken WhatsApp formatting

| Problem | Fix |
|---|---|
| `* bold *`, `*bold *` | `*bold*` (script tightens one-sided loose markers) |
| Bold spanning two lines | Close and reopen on each line |
| `*https://link*` | `https://link` (script removes the markers) |
| `abc*def*` | Add a space: `abc *def*` |
| Three+ blank lines | One blank line (script) |
| Whole lines in CAPS | Normal case, bold the key word |

## Polish rules

- Fix spelling, grammar, punctuation, capitalisation of names and brands.
- Keep the user's slang, Hinglish spellings ("kal", "pls"), emoji and sign-off.
  "pls" is not a typo; "recieve" is.
- Don't add or remove facts. Don't upgrade the tone (casual stays casual).
- Length within ±10% of the original unless the user asks to shorten.
- List every non-trivial change in Notes (max 3 bullets; group small fixes as "fixed 4 typos").

## Check-mode report format

A plain numbered list in chat, not a code block (it's not a message to paste):

Problems:
1. Line 3: `Friday, 14 Nov`: 14 Nov 2026 is a Saturday.
2. Line 5: `**Venue**` shows asterisks on WhatsApp → use `*Venue*`.
3. Line 7: the link has no https:// → `https://www.example.com`.

No problems → "Looks good to send." plus any warnings worth knowing (length, @mentions to re-tag).
