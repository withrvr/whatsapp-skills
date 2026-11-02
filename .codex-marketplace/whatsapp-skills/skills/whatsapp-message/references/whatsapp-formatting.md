<!-- GENERATED from shared/references/whatsapp-formatting.md by scripts/sync.py. Edit the source, not this copy. -->
# WhatsApp formatting: what renders, what breaks

WhatsApp has its own small formatting language. It is **not Markdown**. Anything
outside this page shows up in the chat as literal symbols.

## Syntax that renders

| Effect | Type this | Notes |
|---|---|---|
| Bold | `*text*` | One asterisk each side. |
| Italic | `_text_` | |
| Strikethrough | `~text~` | Good for "~₹999~ ₹699" price cuts. |
| Monospace block | ` ```text``` ` | For codes, IDs, passcodes. Not for emphasis. |
| Inline code | `` `text` `` | Short IDs, coupon codes. |
| Bulleted list | `- item` or `* item` at the start of a line | Space after the symbol. |
| Numbered list | `1. item` at the start of a line | |
| Quote | `> text` at the start of a line | For one important note or a quoted rule. |
| Combined | `*_bold italic_*` | Nest cleanly, close in reverse order. |

Lists, quotes and inline code are newer. On an old app they show as the plain
characters (`- item`, `> text`), which still reads fine, so they are safe to use.
`•` bullets also work everywhere as plain text.

## Markdown that does NOT render

These are the habits an AI writer brings from Markdown. Every one of them looks broken in a chat.

| Don't write | Shows as | Write instead |
|---|---|---|
| `**bold**` or `__bold__` | stray asterisks | `*bold*` |
| `# Heading` | a literal `#` | `*Heading*` on its own line |
| `[Register here](https://…)` | raw brackets | `Register: https://…` |
| A table with pipes | a wall of pipe characters | one row per line: `*Mon* · 10 am · Room 4` |
| `---` divider | three dashes | a blank line |
| Indented sub-bullets | flat, uneven lines | one flat list, or split into two lists with bold labels |
| `<b>`, `<br>`, HTML | the tags | WhatsApp markers and real line breaks |

## Rules that make markers render

1. **Hug the text.** `*Venue:*` works, `* Venue *` and `*Venue *` don't.
2. **Space or punctuation outside.** `abc*def*` often fails. `(*optional*)` and `*Note:*` work.
3. **One line at a time.** A marker can't span a line break. Bold each line separately.
4. **Never wrap links, phone numbers or emails.** `*https://…*` can break tap-to-open. Bold the label instead: `*Register:* https://…`
5. **Labels carry their colon inside:** `*Date:* Sat, 14 Nov`.
6. **Underscores inside words are safe.** `file_name.pdf` and `@my_handle` don't italicise.
7. **A lone asterisk with spaces around it is literal** (`5 * 3`). A trailing `*` for "T&C apply*" shows as a plain asterisk, which is usually what was meant.

## Formatting levels

Pick one with the `formatting` dial (see `message-dials.md`).

- **plain**: no markers, no lists. Line breaks only. Default for 1:1 chats and replies.
- **light**: 1-3 bold anchors (date, time, deadline, the one action), short paragraphs, a list only if there are 3+ parallel items. Default for most group messages.
- **full**: bold title line, labeled detail lines, lists, emoji as line labels, one `>` quote for the critical note. Default for invitations and structured notices.

Bold is a highlighter: if more than about a fifth of the message is bold, nothing stands out.

## Layout that works in a chat bubble

- **The first two lines carry the point.** Long messages collapse behind "Read more", and the notification preview shows only the start. Lead with what + when, or with the ask.
- **Short blocks.** 1-3 lines per paragraph, one blank line between blocks, never two.
- **Logistics as labeled lines**, not a sentence:

  ```
  📅 *Sat, 14 Nov*
  ⏰ 7:00 pm onwards
  📍 Green Park Banquet, Sector 5
  ```

- **Emoji as line labels** (📅 ⏰ 📍 🔗 📞 ✅ ⚠️ 📝) scan better than emoji scattered inside sentences.
- **No decorative dividers** (`━━━━━`, `✦✦✦`) unless the user asks: they wrap badly on narrow phones. A blank line is the divider.
- **Mobile width is about 30-35 characters per line.** Long labeled lines wrap; keep each one short.

## Pre-send checklist

Run `scripts/wa_lint.py` when you can execute Python. Otherwise check by hand:

- [ ] No `**`, `#` headings, `[label](url)`, tables, `---`, HTML
- [ ] Every marker hugs its text and opens and closes on the same line
- [ ] No marker touching a link, phone number or email
- [ ] Links start with `https://`
- [ ] Every weekday matches its date
- [ ] What + when (or the ask) sits in the first two lines
- [ ] Every `[placeholder]` is listed in Notes
- [ ] Length fits: status ≤ 700 characters, caption ideally ≤ 1,024
