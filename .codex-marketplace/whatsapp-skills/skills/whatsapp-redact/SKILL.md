---
name: whatsapp-redact
description: "Mask or remove sensitive details before you forward, post or share WhatsApp text: phone numbers, emails, UPI and bank details, card numbers, OTPs, Aadhaar, PAN and other IDs, names, addresses, flat and vehicle numbers, in a message, chat export or screenshot text. Use whenever someone wants to hide, mask, blur, anonymise or redact details before sending, posting a chat in a group, warning others about a scam, or pasting into an AI. Consistent stand-ins (Person A, [phone 1]) and a private key. Not for writing a new message (use whatsapp-message)."
license: MIT
metadata:
  author: withrvr
  version: "1.0.1"
---

# WhatsApp Redact

People forward chats, post screenshots in groups, warn others about scams and
paste conversations into AI apps, and the text is full of other people's phone
numbers, names, addresses, UPI IDs and sometimes an OTP. You return the same
text with the sensitive parts masked: consistently, so it still reads, and
without removing what the purpose needs.

## When to use

- "Hide the numbers and names before I post this in the group"
- "Mask my details, I want to share this chat with the builder's other buyers"
- "Warn our society about this scam message, but remove my info"
- "Remove personal info from this chat before I paste it into ChatGPT"
- "Blur / hide the account number in this payment message"

**Not for:** writing a new message (`whatsapp-message`), replying
(`whatsapp-reply`), summarising a chat (`whatsapp-catchup`; it can hand you its
summary to redact afterwards).

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

1. **Ask yourself who will see it and why.** The purpose decides what stays:
   | Purpose | Mask | Keep |
   |---|---|---|
   | Post in a group / public | everything below at `standard` | what the point needs (the date, the amount, the business name) |
   | Scam warning | the victim's details | **the scammer's number, UPI ID and link**, labeled as the scammer's, so people can block them |
   | Complaint to a company | other customers, family members | your own order ID, dates, amounts |
   | Paste into an AI or send to a helper | numbers and IDs (`light`) | names, if the user is fine with that |
   | Evidence for police, a lawyer, HR or a bank | **nothing.** Tell the user to share the original export unedited; a redacted copy can weaken evidence | everything |
2. **Pick the level** (default `standard`, the user can say "light" or "full"):
   - `light`: numbers and IDs only: phone, email, UPI ID, card, account, Aadhaar, PAN, IBAN, OTP, passwords.
   - `standard`: light + names of private people (→ Person A, Person B), exact
     addresses (→ the area or city), flat, house and vehicle numbers, children's
     school and class, health details, photos of people mentioned by name.
   - `full`: standard + company and place names, exact dates (→ "Day 1", "Day 2"), job titles and any detail that identifies someone in context.
3. **Mask numbers mechanically.** If you can run code, save the text to a temp
   file with your file-writing tool, then run `python3 <this skill's folder>/scripts/wa_lint.py --redact <file>`
   as one standalone command (absolute paths, no `cd` or `&&`)
   (`--style partial` keeps the last 4 digits; `--keep phone,email` leaves those
   kinds visible; `--pii` lists what it found without changing anything). It
   validates card (Luhn), Aadhaar (Verhoeff) and IBAN checksums, so it catches
   what eyes miss. Without code execution, go through
   `references/redaction-rules.md` §What counts as sensitive line by line.
4. **Then mask what a script can't:** names, nicknames ("Bittu"), addresses,
   relationships that identify someone ("the secretary's son"), sender names in
   chat-export lines, and @mentions.
5. **Keep it readable.** The same person or number gets the same stand-in every
   time. Keep timestamps, amounts and dates unless the level says otherwise.
6. **Deliver**: the redacted text in a `text` block, then Notes with:
   - `Key (keep private):` which stand-in is who, so the user can check it. This line is never part of the block.
   - what was deliberately left visible and why (the scammer's number)
   - for screenshots: what to cover in the image (see below)

## Rules

- **Never guess a hidden value, never un-mask** someone else's redaction, never
  help work out who an anonymised person is.
- **Over-mask rather than under-mask** when unsure; say what you masked.
- **Don't change the meaning.** No rewording, no tidying. Only the sensitive parts change.
- **OTPs, PINs, passwords and CVVs are always masked**, at every level, even if the user says keep everything.
- **Your own details:** ask once if unclear whether the user wants their own name and number kept.

## Screenshots

This skill works on text. For an image, tell the user what to cover, in order:
the contact name and photo in the chat header, phone numbers, profile photos
of people, UPI IDs and account numbers, addresses, and any QR code. Cover them
with **solid boxes**, not blur or pixelation (those can sometimes be reversed),
and crop out what isn't needed. If they paste the screenshot, list exactly what
you see that needs covering.

## Example

**Brief:** *mask this before I post it in the building group, keep the scammer's number*

> *+91 70123 45678: Dear customer your electricity will be cut tonight. Call 70123 45678 or pay ₹10 at https://bit.ly/eb-pay*
> *Me: my consumer no is 1102345678, my name is Sunita Rao, flat C-703*

```text
⚠️ Scam alert: this message came to me today.

Scammer: "Dear customer your electricity will be cut tonight. Call 70123 45678 or pay ₹10 at https://bit.ly/eb-pay"

The scammer's number is +91 70123 45678. Please block and report it. Don't click the link.
```

Notes:
- I removed your reply completely (consumer number, name, flat): the group doesn't need it.
- Left the scammer's number and link visible on purpose, so people can recognise and block them.

## References

- `references/redaction-rules.md`: what counts as sensitive, stand-in styles, chat-export handling, edge cases. Load at step 3.
- `references/examples.md`: worked redactions (group post, scam warning, AI paste, partial masking, chat export).
- `references/writing-rules.md`, `references/whatsapp-formatting.md`, `references/message-dials.md`, `references/links-media-mentions.md`.
- `scripts/wa_lint.py`: `--redact`, `--pii`, `--style partial`, `--keep`.

## Related skills

`whatsapp-catchup` (summarise a chat, then redact the summary) · `whatsapp-reply`
(answering a suspicious message) · `whatsapp-announcement` (a full scam alert notice)
