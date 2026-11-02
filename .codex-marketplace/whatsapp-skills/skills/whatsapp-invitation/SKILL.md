---
name: whatsapp-invitation
description: "Create WhatsApp invitations and follow-ups: weddings (haldi, mehendi, sangeet, wedding, reception), engagements, birthdays, housewarmings and griha pravesh, baby showers, naming ceremonies, poojas, anniversaries, farewells, reunions, office parties, launches, meetups. Use whenever someone wants to invite people on WhatsApp or needs the e-card caption, venue and map lines, RSVP ask, save-the-date, reminder or thank-you message. English, Hinglish, Hindi or bilingual. Not for general notices (use whatsapp-announcement)."
license: MIT
metadata:
  author: withrvr
  version: "1.0.0"
---

# WhatsApp Invitation

Most invitations now travel on WhatsApp: an e-card or video plus a message, sent
to family groups, friends and colleagues, then a reminder and a thank-you. The
user gives you the event details and who's inviting. You write each message in
the sequence, warm and complete, with every name, date and venue exactly right.

## When to use

- "Make a WhatsApp invite for my sister's wedding / son's birthday / housewarming"
- "Caption for the e-invite card", "save the date message"
- "Remind everyone about the sangeet tomorrow", "send the venue location"
- "Thank everyone for coming"
- Office parties, farewells, reunions, launches, community meetups and religious events.

**Not for:** notices that aren't invitations (`whatsapp-announcement`), ticketed
or paid events being sold (`whatsapp-promotion`), the user's 24-hour status (`whatsapp-status`).

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

1. **Collect the event facts**: occasion, whose (names exactly, with relations),
   hosts ("Sharma family", "Rohit & Ananya"), each function's date, day, time,
   venue + map link, dress code or theme, RSVP (by when, to whom, how), extras
   (parking, kids, gifts, food), and who it's going to (family group, friends, office).
2. **Pick the message in the sequence** (`references/invitation-types.md`):
   save-the-date · invite · e-card caption · personal invite to elders ·
   reminder · day-of (location + contact) · thank-you. Default is the invite.
3. **Set the dials.** Defaults: length `medium`, tone `warm` (family or religious:
   `respectful`; friends: `celebratory`; office: `friendly-professional`),
   formatting `full`, emoji `few` (rich for kids' birthdays and friends).
   Language: as asked; family weddings are often bilingual or Hindi/regional.
4. **Write it**: opener that names the occasion and the people → the
   details block (one function per block for multi-day events) → RSVP / action →
   a warm close from the hosts.
5. **Check every fact** against the brief, especially weekday ↔ date for each
   function and am/pm. Then deliver.

## Rules for invitations

- **Names are sacred.** Spell them exactly as given, with the honorifics and
  family names the user uses. Never shorten "Ananya" to "Anu" unless the user did.
- **One function = one block** with its own date, time and venue. Order by date.
- **Venue line + map link** on separate lines. No map link given → don't invent one; suggest in Notes that they add the Google Maps share link.
- **RSVP only if the user wants it**, with a date and a person. For big family
  weddings, invitations usually don't ask for RSVP.
- **Gifts:** say nothing unless the user says ("No gifts please, your blessings are enough").
- **The e-card caption** doesn't repeat the card word for word, but keeps the key
  date, time and venue in text (searchable, forwards without the image).
- **Religious and cultural wording** only as the user's tradition uses it ("With
  the blessings of Shri Ganesh", "Insha'Allah", "With joy and God's grace"). Don't add religious lines the user didn't signal.
- **Reminders** are short: the function, the time, the venue link, a contact.
- **Thank-you** messages name the occasion and thank warmly; mention photos if the user is sharing them.

## Example

**Brief:** *housewarming. Mehta family (Nikhil & Pooja). sun 22 nov, pooja 10am, lunch from 12:30. flat 1803, Tower C, Lodha Amara, Thane. map https://maps.app.goo.gl/Tq9wE. friends + family group. warm, few emoji*

```text
🏡 *You're invited to our Griha Pravesh!*

We've moved into our new home and would love to celebrate with you.

📅 *Sun, 22 Nov*
🪔 Pooja at 10 am
🍽️ Lunch from 12:30 pm

📍 Flat 1803, Tower C, Lodha Amara, Thane
https://maps.app.goo.gl/Tq9wE

Do come with family! 🙏
Nikhil & Pooja Mehta
```

## References

- `references/invitation-types.md`: structures for each occasion and every message in the invite sequence, with timing. Load at step 2.
- `references/examples.md`: complete wedding (multi-function), birthday, office party, Hindi and bilingual examples.
- `references/links-media-mentions.md`: e-card captions, map links, albums and video invites.
- `references/message-dials.md`, `references/writing-rules.md`, `references/whatsapp-formatting.md`.
- `scripts/wa_lint.py`: pre-send check (`--kind invitation`, or `--kind caption` for an e-card caption).

## Related skills

`whatsapp-announcement` (notices and reminders that aren't invitations) ·
`whatsapp-status` (a status about the event) · `whatsapp-message` (a personal 1:1 invite note)
