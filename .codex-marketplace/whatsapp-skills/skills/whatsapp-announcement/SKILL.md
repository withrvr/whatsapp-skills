---
name: whatsapp-announcement
description: "Write a WhatsApp group, community or broadcast announcement from notes: office notices, meetings and changes, reminders, deadlines, fee dues, alerts, society and school notices, study material, holidays, rules, results, fundraisers, job openings, urgent blood or help requests, minutes, stand-ups, buy-sell-rent posts, event recaps. Use whenever someone needs to inform, remind or alert a WhatsApp group. Packs dates, times, links and @mentions. Not for invitations (use whatsapp-invitation), offers (whatsapp-promotion) or channel posts (whatsapp-channel)."
license: MIT
metadata:
  author: withrvr
  version: "1.0.0"
---

# WhatsApp Announcement

A group admin, team lead, teacher, class rep, society secretary or organiser has
information many people need. They dump it on you: dates, times, three links, who
to contact, what changed. You return the notice people will actually read in the
group, with nothing lost and nothing invented.

## When to use

- "Announce in the team group that …", "notice for the society group"
- "Tell the class/parents group about the test / PTM / holiday / syllabus"
- "Share these study materials with the batch", "post the schedule"
- "Alert: water cut tomorrow", "server down", "rain holiday", "road closed"
- "Reminder for tomorrow's meeting", "fees due Friday"
- Community announcement groups and broadcast lists with the same purpose.

**Not for:** invitations to a celebration or event (`whatsapp-invitation`),
anything selling (`whatsapp-promotion`), one-way channel posts or series
(`whatsapp-channel`), a 1:1 message (`whatsapp-message`).

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

1. **Make a fact sheet from the brief** (in your head, not in the output): what,
   who it's for, when (date, day, time, time zone), where (place or link), what
   people must do, deadline, links, files, contacts, who's announcing.
2. **Pick the type** in `references/announcement-types.md` (meeting, change,
   reminder, deadline, alert, info share, study material, results, fundraiser,
   welcome, rules, digest, job opening, urgent help request, minutes, stand-up,
   buy-sell-rent post, event recap). Use its skeleton.
3. **Set the dials.** Defaults: length `medium`, tone `friendly-professional`,
   formatting `light` (`full` when there are 4+ details), emoji `few` as line
   labels. Alerts: tone `urgent`, emoji only ⚠️ or 🚨, no greeting.
4. **Write the headline line**: emoji label + bold title that says what it is.
   `📢 *Team meeting moved to Thu, 5 Nov*`. Someone who reads only this line must get the point.
5. **Then the core in 1-2 lines** (what + when), **then labeled details**, **then
   the action + deadline**, then contact and sign-off.
6. **Check and deliver.** Suggest a poll, event or pin in Notes when it fits.

## Rules for group announcements

- **Changes lead with the change.** "*Changed:* Exam moved from ~Mon, 9 Nov~ to
  *Wed, 11 Nov*". Old value struck through, new value bold.
- **Every action has a deadline** and a way to do it (link, reply in DM, form).
- **Ask for replies carefully.** "Reply 👍 when you've read" floods big groups.
  For 30+ people prefer a poll, a form, or "reply only if you can't make it".
- **Links**: each one labeled on its own line; the most important first (it gets the preview).
- **Files**: say what's attached and suggest a clean file name in Notes.
- **@mentions** only for people who must act. Remind the user to re-type them.
- **Sign-off** with name and role when authority matters: "Rakesh, Secretary" alone on the last line.
- **Big groups and communities:** no "Hi all, hope everyone is doing well" opener.
  The headline is the opener.
- **Repeat posts** (reminders): shorter than the first post, same headline style, the delta first.

## Example

**Brief:** *team group. all hands moved from fri 6 nov 4pm to thu 5 nov 11am because ceo travelling. same zoom link https://zoom.us/j/8812345678 passcode 4421. send questions in the form before wed eod https://forms.gle/q7XyZ. from Anita HR*

```text
📢 *All-hands moved to Thu, 5 Nov, 11 am*

It was on ~Fri, 6 Nov, 4 pm~. Moved because our CEO is travelling on Friday.

🔗 *Zoom:* https://zoom.us/j/8812345678
🔑 *Passcode:* `4421`

📝 *Questions for the CEO:* send them by Wed end of day
https://forms.gle/q7XyZ

Anita, HR
```

Notes:
- Pin this in the group till Thursday.

## References

- `references/announcement-types.md`: skeletons for 21 announcement types. Load at step 2.
- `references/examples.md`: full worked announcements (office, school, society, alert, study material, Hinglish).
- `references/links-media-mentions.md`: load whenever the brief has links, files, posters, @mentions, or a poll/event would fit.
- `references/message-dials.md`, `references/writing-rules.md`, `references/whatsapp-formatting.md`.
- `scripts/wa_lint.py`: pre-send check (`--kind announcement`).

## Related skills

`whatsapp-invitation` (celebrations and events) · `whatsapp-promotion` (offers) ·
`whatsapp-channel` (one-way channel posts) · `whatsapp-status` (24-hour status) ·
`whatsapp-catchup` (minutes from a chat discussion) · `whatsapp-setup` (group description and rules)
