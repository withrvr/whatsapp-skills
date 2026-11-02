---
name: whatsapp-reply
description: "Draft the reply to a WhatsApp message you received. Use whenever the user pastes or describes a message, chat or screenshot and asks what to reply, how to respond or what to say, including awkward or suspicious ones (saying no, pushing back on a boss, clients, recruiters, angry customers, family, strangers, possible scams). Answers every question asked, mirrors their tone and language, sounds like the user. Not for starting a new conversation (use whatsapp-message)."
license: MIT
metadata:
  author: withrvr
  version: "1.0.0"
---

# WhatsApp Reply

Someone messaged the user. The user pastes it (or a screenshot) and says what
they want to get across, often in three words: *"say no politely"*, *"ask for
more time"*, *"yes but only after 6"*. You return the reply they'll send.

## When to use

- "Reply to this: …", "what do I say to this", "how do I respond"
- A screenshot of a chat with "help me reply"
- An HR, recruiter, client, landlord or family message that needs a careful answer
- Group messages where the user was asked something directly

**Not for:** starting a conversation (`whatsapp-message`), a group notice
(`whatsapp-announcement`), polishing a reply the user already wrote (`whatsapp-formatter`).

<!-- BEGIN shared:core-rules -->
## Core rules (every WhatsApp skill)

- **Deliver the final message first**, in a ` ```text ` block, with no preamble. One message unless asked for options. Then `Notes:` (max 3 bullets) only when there's something to act on, never just to confirm a check passed.
- **Never invent facts, never drop them.** Dates, times, venues, prices, names, numbers and links come from the user, copied exactly. Short messages cut words, not facts. Missing and essential → `[placeholder]`, listed in Notes.
- **WhatsApp is not Markdown.** Bold is `*one asterisk*`, italic `_x_`, strike `~x~`. Never `**x**`, `# heading`, `[label](url)`, tables or `---`. Markers hug the text and can't span lines. Never put markers on a link.
- **No em dashes (—) or en dashes (–), ever.** Comma, full stop, colon, "to" or a new line instead. Capitalise names exactly as given. No AI vocabulary (leverage, streamline, delve, foster…). Full list: `references/writing-rules.md` §Voice rules.
- **First two lines carry the point** (what + when, or the ask). Short blocks, one blank line between them.
- **Check weekday ↔ date**, am/pm, time zone and deadlines. Flag anything off in the user's brief.
- **Dials:** length, tone, formatting, emoji, language. Explicit words from the user win, then the audience, then this skill's defaults (`references/message-dials.md`).
- **Before delivering**, if you can run code: save the draft to a temp file with your file tool, then run `python3 <this skill's folder>/scripts/wa_lint.py --kind <kind> <file>` (absolute path, no shell variables). Fix every error; weigh the warnings. If you can't run code, use the checklist in `references/whatsapp-formatting.md`. Don't mention the check in your reply unless it found a problem in the user's own brief.
<!-- END shared:core-rules -->

## Workflow

1. **Read the incoming message closely.**
   - Who sent it and their relationship to the user.
   - Their language, formality, length and emoji habit.
   - **Every question and request in it.** List them to yourself; the reply must answer each one, in their order.
   - In a screenshot, the user's own messages are the bubbles on the **right**
     (green in light mode), the other person's are on the **left**. Read names,
     times and quoted messages from the image. In a group, the sender's name sits above their bubble.
2. **Read the user's intent.** Yes / no / not now / counter-offer / need info / just acknowledge.
   If the user gave no intent and the answer could go either way, give two
   variants labeled by intent (`Accept`, `Decline`). This is the one case where
   variants are the default.
3. **Check for a scam before replying.** See "Suspicious messages" below.
4. **Mirror the sender, within reason.** Same language and script, similar formality and length.
   Never more casual than a formal sender, never more emoji than them in a work chat.
5. **Draft** with the shape from `references/reply-situations.md`.
6. **Check and deliver.** Add Notes if they should reply to a specific message (swipe to quote) or tag someone.

## Rules for replies

- **Answer first.** The yes/no/answer goes in line 1. Context after.
- **Every question gets an answer**, even if it's "I'll confirm by Friday".
- **Saying no:** thanks or acknowledgement → the no, clearly → one short reason
  (optional) → an alternative if the user has one. Never a fake excuse the user didn't give.
- **Counter-offers:** restate what you can do as a concrete offer ("I can do ₹40,000 with delivery by the 20th").
- **Angry or upset sender:** acknowledge the feeling and the specific issue, give the fix or next step with a time. Don't argue in text; offer a call if it's escalating.
- **In a group**, answer only the part addressed to the user. Suggest replying to the specific message (swipe right on it) so the context shows.
- **Don't over-apologise** for replying late. One "Sorry for the late reply" at most, or none.

## Suspicious messages

If the incoming message asks for an OTP, PIN, password, card number, KYC update
by link, a "refundable registration fee", gift cards, or comes from an unknown
number claiming to be a bank, courier, police, government, a boss or a relative
in trouble: **don't draft a reply that engages.** Tell the user plainly that it
looks like a scam, why, and what to do (don't click, don't share codes, verify by
calling the official number they already have, block and report in WhatsApp). If
they still want a reply, a one-line "I'll contact the bank directly" is the most you write.

## Example

**Incoming (from recruiter Neha, formal):** *"Hi Arjun, thanks for your time yesterday. The panel would like to move you to the final round. Could you share your availability for Thursday or Friday this week, and your expected CTC?"*
**User:** *thu after 2 works, fri anytime. expected 28 LPA*

```text
Hi Neha, thank you, that's great to hear!

For the final round, Thursday after 2 pm works, and Friday I'm available any time.

My expected CTC is 28 LPA.
```

## References

- `references/reply-situations.md`: shapes for common replies (decline, delay, negotiate, angry sender, family, recruiters). Load at step 5.
- `references/examples.md`: worked incoming messages with finished replies.
- `references/message-dials.md`, `references/writing-rules.md`, `references/whatsapp-formatting.md`.
- `references/links-media-mentions.md`: when the reply carries links, files or tags.
- `scripts/wa_lint.py`: pre-send check (`--kind reply`).

## Related skills

`whatsapp-message` (start a conversation) · `whatsapp-formatter` (fix a reply you wrote)
