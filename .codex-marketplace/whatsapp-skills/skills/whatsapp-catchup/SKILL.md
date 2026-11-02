---
name: whatsapp-catchup
description: "Catch up on a long WhatsApp group chat or exported chat: what you missed, what was decided, dates and deadlines, links and files, and what is asked of you, in a short summary. Then, if wanted, the recap or meeting minutes to post back to the group with decisions and action items, owners and deadlines. Use whenever someone pastes or attaches a chat or export and asks what happened, what they missed, what they need to do, or to post a summary or MoM. Not for replying to one message (use whatsapp-reply)."
license: MIT
metadata:
  author: withrvr
  version: "1.0.0"
---

# WhatsApp Catch-up

The user was away from a busy group for a day, or a week. Three hundred
messages later, they want to know what matters to them without scrolling. Or
a discussion in the group needs to be turned into minutes everyone can see.
You read the chat and give them exactly that.

## When to use

- "What did I miss in this group?" with a pasted chat or an exported `.txt`
- "Anything I need to do?", "was anything decided about the AGM?"
- "Summarise yesterday's discussion", "only messages since Monday"
- "Write the minutes / MoM / recap of this discussion to post in the group"

**Not for:** answering one message (`whatsapp-reply`), writing a notice from
your own notes (`whatsapp-announcement`), masking details in a chat before
sharing it (`whatsapp-redact`).

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

## Getting the chat

If the user hasn't shared it, tell them in one line: open the chat → tap the
group name (iPhone) or ⋮ → More (Android) → **Export chat** → **Without media**,
then attach the `.txt` (inside the zip on iPhone). A copy-pasted stretch of
messages works too.

## Workflow

1. **Know who the user is in the chat** (their name as it appears) and what
   window they care about ("since Friday", "today"). Ask only if it's needed and not obvious.
2. **Parse the export** when you can run code (pasted text: save it to a file with
   your file-writing tool first; run the script as one standalone command):
   `python3 <this skill's folder>/scripts/wa_chat.py <file> --since YYYY-MM-DD --messages`
   gives the messages, people, links and media counts. `--mentions <name>` finds
   what's addressed to the user; `--last 300` caps a huge chat. Without code,
   read the pasted text directly.
3. **Read for the five things** (see `references/summary-rules.md`): decisions,
   dates and deadlines, asks of the user, links and files, open questions.
4. **Write the catch-up for the user** (plain chat text, not a code block; it's for them to read):

   ```
   In short: [2 lines: what happened that matters]

   Decided: [bullet per decision, who decided]
   Dates: [Day, Date, time · what]
   For you: [what's asked of the user, by whom, by when]
   Links and files: [label: link]
   Still open: [unresolved questions]
   ```
   Drop any section that's empty. Keep it shorter than the chat by far: a week of chat in about 10-15 lines.
5. **Recap or minutes to post** (when asked, or offer it in one line): a
   WhatsApp-ready block in the shape in `references/summary-rules.md` §Minutes,
   checked with `wa_lint.py --kind announcement`.

## Rules

- **Decided means decided.** A suggestion with no agreement is "proposed by
  Meera", not a decision. If people disagreed, say so.
- **Latest wins.** When a time or place changed during the chat, report the
  final one and mention it changed ("moved from 10 am to 11 am on Sat").
- **Attribute.** Who said what, by their display name as it appears in the chat.
- **Don't fill gaps.** Deleted messages, `<Media omitted>` and images can't be
  read: say "Rakesh shared an image" instead of guessing what it showed.
- **Check dates.** Weekdays against dates, "tomorrow" against the message's own date.
- **No mood reading.** Don't characterise people ("Rahul was rude"); report what was said if it matters.
- **Privacy.** The chat contains other people's messages. Summarise for the user;
  if they want to share the summary outside the group, offer `whatsapp-redact` first.

## Example

**Input (export, user is Priya):**

```chat
[01/11/26, 9:05:40 PM] Rakesh Secretary: Dear all, AGM is on Sun, 15 Nov at 11 am in the clubhouse. Agenda: maintenance hike, parking.
[01/11/26, 9:07:02 PM] Meera B-1204: Can we also discuss the lift?
[02/11/26, 8:15:00 AM] Rakesh Secretary: Yes added. @Priya please share last year accounts by Fri https://docs.google.com/x
[02/11/26, 8:16:10 AM] Priya: image omitted
```

**Output:**

In short: The AGM is set and you've been asked for last year's accounts.

Decided: AGM on *Sun, 15 Nov, 11 am* in the clubhouse (Rakesh). Agenda: maintenance hike, parking, and the lift (added at Meera's request).
For you: Rakesh asked you to share last year's accounts by Fri, 6 Nov.
Links and files: Rakesh's doc: https://docs.google.com/x

## References

- `references/summary-rules.md`: the five things to extract, how to handle long chats, minutes and recap templates. Load at step 3.
- `references/examples.md`: catch-ups and minutes from real-looking chats.
- `references/writing-rules.md`, `references/whatsapp-formatting.md`, `references/message-dials.md`, `references/links-media-mentions.md`.
- `scripts/wa_chat.py`: parses Android and iPhone exports (`--since`, `--last`, `--from`, `--mentions`, `--messages`, `--json`).
- `scripts/wa_lint.py`: check the recap before posting (`--kind announcement`).

## Related skills

`whatsapp-reply` (answer what's asked of you) · `whatsapp-announcement` (post a
notice from your notes) · `whatsapp-redact` (mask the chat or summary before sharing)
