---
name: whatsapp-message
description: "Turn a brain-dump of context into one ready-to-send WhatsApp message to a person or small chat: favours, follow-ups, updates to your boss, HR or recruiters, first messages to new contacts, apologies, congratulations, payment nudges, bookings, complaints, voice-note scripts. Use whenever someone wants to message, text or WhatsApp someone and gives the situation, even casually. Dials for length, tone, formatting, emoji and language. Not for group notices (use whatsapp-announcement), invites (whatsapp-invitation) or answering a message you got (whatsapp-reply)."
license: MIT
metadata:
  author: withrvr
  version: "1.0.1"
---

# WhatsApp Message

The user has the whole situation in their head. They give it to you once, messy
and out of order. You return the one message they'll paste into WhatsApp: right
tone for the person, right length, nothing invented, nothing missing.

## When to use

- "Write a WhatsApp message to my manager that I'll be late / on leave / done with X"
- "Message the landlord / plumber / school / clinic about …"
- "I got this number from Ankit, write my first message to her about …"
- "Remind him about the money, nicely"
- "Congratulate / thank / apologise to …"
- "What should I say in a voice note to Nani about …" (a speakable script)
- Any 1:1 or small-chat message where the user is starting the conversation.

**Not for:** a reply to a message they received (`whatsapp-reply`), a notice to a
group (`whatsapp-announcement`), an invitation (`whatsapp-invitation`), a sales
message (`whatsapp-promotion`), or fixing text they already wrote (`whatsapp-formatter`).

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

1. **Pull the facts out of the brief.** Who it's to and their relationship to the
   user, what happened, what the user wants from them, by when, what's attached.
   Note anything the user said in their own words that should survive (a nickname, a phrase).
2. **Find the situation** in `references/message-playbook.md` and use its shape.
3. **Set the dials.** Defaults for this skill: length `short`, formatting `plain`
   (`light` when there are 3+ details like date, time, amount), emoji `few` for
   casual and `none` for formal, tone from the relationship. Explicit words in
   the brief override all of these.
4. **Draft** the message in the shape, in the user's voice, with every fact exact.
5. **Check** with the core rules above.
6. **Deliver** the block, then Notes only if something needs doing.

## Rules for 1:1 messages

- **Greeting and point in the same message.** Never a lone "Hi" that waits for a
  reply. "Hi Ma'am, …" then the reason, in one bubble.
- **The ask is specific and easy to answer.** "Can we move our call to 4 pm today?"
  beats "Let me know when you're free". For favours, give an easy out.
- **To a boss, senior or client:** reason first, one apology at most, what's
  covered and what they need to do (if anything). No "Sorry to disturb".
- **To a new contact:** line 1 says who you are and how you got the number
  ("Hi Meera, I'm Rohan, Ankit's colleague, he shared your number"). Then why,
  then one ask.
- **Money:** amount, what it's for, how to pay (UPI ID or link copied exactly), by
  when. Friendly, never accusing. Second reminders are shorter than the first.
- **Leave and absence:** dates, reason at the level the user wants to share,
  handover, reachable or not. Formal leave still goes through the HR system; say so in Notes if relevant.
- **Sensitive** (condolence, illness, breakup, conflict): load
  `references/writing-rules.md` §Respect and sensitivity before drafting.

## Example

**Brief:** *msg to my manager Kavita, fever since last night, won't come today,
the client deck is 90% done, Rahul can present at 3 if needed, I'll be on phone
for urgent stuff. not too formal*

```text
Hi Kavita, I've had a fever since last night so I won't make it in today.

The client deck is 90% done and in the shared folder. Rahul can present it at 3 if needed, I've briefed him.

I'm on my phone for anything urgent.
```

## References

- `references/message-playbook.md`: shapes for ~30 common 1:1 situations and voice-note scripts. Load at step 2.
- `references/examples.md`: worked briefs with finished messages. Load when the tone is unclear.
- `references/message-dials.md`: full dial definitions and audience defaults.
- `references/writing-rules.md`: output contract, fact rules, won't-write list.
- `references/whatsapp-formatting.md`: what renders and the pre-send checklist.
- `references/links-media-mentions.md`: load when the brief has links, attachments, @mentions or phone numbers.
- `scripts/wa_lint.py`: pre-send check (`python3 scripts/wa_lint.py --kind message draft.txt`).

## Related skills

`whatsapp-reply` (answering a message you got) · `whatsapp-announcement` (groups) ·
`whatsapp-formatter` (fix text you already wrote)
