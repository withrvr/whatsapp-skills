---
name: whatsapp-status
description: "Write WhatsApp Status updates: text status (700-character limit), captions for photo and video status, and sets of 2-5 status slides for offers, milestones, festival wishes, quotes, availability, back-in-stock or countdowns. Use whenever someone wants to put something on their WhatsApp status, personal or business. One idea per status, reply-to-status calls to action. Not for messages to a chat or group (use whatsapp-message or whatsapp-announcement)."
license: MIT
metadata:
  author: withrvr
  version: "1.0.0"
---

# WhatsApp Status

Status is a 24-hour full-screen story seen by the user's contacts. People tap
through fast: a text status gets a glance, a photo caption gets a second. You
write status text that lands in that glance, and that invites a reply (replies
to a status arrive in the user's private chat).

## When to use

- "Status for Diwali / my birthday / my new job / exam results"
- "Business status: offer today, new stock, open on Sunday"
- "Caption for my photo / video status"
- "Make 3 status slides about the workshop"
- "Out of office / not available status"

**Not for:** messages to a person or group (`whatsapp-message`, `whatsapp-announcement`),
full promo blasts (`whatsapp-promotion`), channel posts (`whatsapp-channel`).

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

## Workflow

1. **Identify the format**: text status, caption on the user's photo/video, or a set of slides.
2. **Find the one idea.** A status carries one thing. If the brief has three, make three slides.
3. **Set the dials.** Defaults: length `one-liner` (text status ≤ 140 characters
   reads in one glance; hard limit 700), tone from the voice (personal or
   business), formatting `plain` (text status fonts are chosen in the app; markers
   work in captions), emoji `few`.
4. **Write it**, with a reply hook when the user wants a response ("Reply 🙋 to book a slot").
5. **Check length** with `scripts/wa_lint.py --kind status`, and deliver. For slides, label each block `Status 1 of 3`.

## Rules for status

- **One idea per status.** Short lines. Text status shows in big type: 1-3 short lines is ideal.
- **Text status: no Markdown, keep markers minimal.** The user picks the background
  colour and font in the app; suggest one in Notes if it helps (e.g. "dark background, serif font").
- **Captions** sit over the photo: first line strongest, under ~200 characters.
- **Calls to action use replies**, since status replies go to the user's chat:
  "Reply *YES* for the menu", "Reply 🎂 to order".
- **Links**: put a link alone on the last line. One link at most.
- **Privacy:** the user's contacts see it (subject to their status privacy
  setting). Don't put phone numbers of other people, addresses, or private news in a status unless the user says so.
- **Business status** can carry an offer; still one offer per slide, with the validity.
- **Festivals and occasions:** a sincere one-liner beats a forwarded poem.

## Example

**Brief:** *status for my cake business, new flavour biscoff cheesecake, ₹650 for 500g, weekend orders only, reply to order*

```text
New: Biscoff cheesecake 🍰
₹650 for 500 g · weekend orders only
Reply 🍰 to order!
```

## References

- `references/status-patterns.md`: patterns for personal, business, festival, milestone, availability and slide sets. Load at step 4.
- `references/examples.md`: worked status texts and captions.
- `references/message-dials.md`, `references/writing-rules.md`, `references/whatsapp-formatting.md`.
- `references/links-media-mentions.md`: when the status has a link or is a caption on media.
- `scripts/wa_lint.py`: `--kind status` enforces the 700-character limit.

## Related skills

`whatsapp-promotion` (the full offer message) · `whatsapp-channel` (posts to followers) ·
`whatsapp-invitation` (the actual invite)
