---
name: whatsapp-setup
description: "Write the standing text of a WhatsApp account, business, group, community or channel: personal About line (139 characters), WhatsApp Business description, greeting message, away message, quick replies, labels, catalog item names and descriptions, group and community names, descriptions and rules, channel name and description. Use whenever someone is setting up or improving their WhatsApp Business profile, auto-replies, saved replies, catalog, or a group, community or channel. Not for one-off messages (use whatsapp-message) or channel posts (use whatsapp-channel)."
license: MIT
metadata:
  author: withrvr
  version: "1.0.1"
---

# WhatsApp Setup

Some WhatsApp text is written once and read thousands of times: the business
description customers see, the greeting a new customer gets, the away message
at night, the quick replies a shop owner taps fifty times a day, the rules in a
group's description. You write that text, field by field, so the user can paste
each piece into the right box.

## When to use

- "Set up my WhatsApp Business: description, greeting and away message"
- "Write quick replies for price, location, timings and payment"
- "Catalog descriptions for these 10 products"
- "Group description and rules for our new residents group"
- "Community / channel description", "my About line"

**Not for:** a one-off message (`whatsapp-message`), a welcome post inside a
group (`whatsapp-announcement`), channel posts (`whatsapp-channel`), offers
(`whatsapp-promotion`).

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

1. **List the fields the user needs.** If they say "set up my business", the
   default set is: description, greeting message, away message, 5-8 quick
   replies, labels. For a group: name, description with rules. For a channel:
   name, description. Field-by-field guidance is in `references/setup-fields.md`.
2. **Collect the facts** once: business name, what they sell, area, hours, how
   to order and pay, delivery, website, typical questions customers ask. Never
   invent hours, prices, delivery areas or policies; use a `[placeholder]`.
3. **Write each field to its own limit and job.** Defaults: tone `warm`,
   formatting `plain` (most of these fields show plain text; bold works in
   greeting, away and quick-reply messages), emoji `few`.
4. **Check lengths**: `python3 <this skill's folder>/scripts/wa_lint.py --kind about|business-description|group-description|quick-reply <file>`.
5. **Deliver one labeled block per field**, in the order the user will fill them
   in. Put the label line above each block, not inside it:
   `Greeting message (sent to new customers)`, then the block.
   For quick replies, label each with its shortcut: `Quick reply /price`.

## Rules for standing text

- **Write for the stranger.** A description or greeting is read by someone who
  doesn't know the business yet: what you are, where, and how to get what they came for.
- **Greeting message:** short, says who they reached and what to send to get
  served fastest ("Send the item photo or name and your pincode").
  WhatsApp Business sends it when someone messages for the first time, or after 14 days of no messages.
- **Away message:** when they'll hear back (the real hours), and what to do if urgent. No fake "we'll reply in 5 minutes".
- **Quick replies:** one question each, complete on its own, with the
  shortcut a person would remember (`/price`, `/loc`, `/pay`, `/hours`,
  `/delivery`, `/thanks`). They're typed with `/` in a chat.
- **Catalog items:** name = what it is + key variant ("Cotton kurta, indigo, S to XXL");
  description = material/size/what's included, care or usage, delivery time if fixed.
  Price is its own field in the app; don't repeat it unless asked.
- **Group descriptions** carry the purpose, 3-5 rules and who the admins are.
  They're shown when people join and stay findable, unlike a message that scrolls away.
- **Names:** groups and channels are found by name; put the place or topic in it
  ("Sunrise Towers B Wing Residents", "Pune Weekend Plans").
- **Labels** (WhatsApp Business): suggest a short set that matches the user's
  flow, e.g. New enquiry · Payment pending · Paid · Order complete · Follow up.

## Example

**Brief:** *home bakery Sweet Crumbs, pune, cakes cookies hampers, order 2 days ahead, delivery in Baner Aundh Wakad, open 10am to 8pm, upi payment. greeting + away*

Greeting message (sent to new customers)

```text
Hi! Welcome to Sweet Crumbs 🍰

Tell us what you'd like (cake, cookies or a hamper), the date you need it and your area. We deliver in Baner, Aundh and Wakad.

Please order at least 2 days ahead.
```

Away message (outside 10 am to 8 pm)

```text
Thanks for your message! We're closed right now and will reply after 10 am.

Our hours are 10 am to 8 pm, every day.
```

## References

- `references/setup-fields.md`: every field, its limit, what it's for, and a template. Load at step 1.
- `references/examples.md`: complete setups (shop, tutor, residents group, channel, personal About).
- `references/message-dials.md`, `references/writing-rules.md`, `references/whatsapp-formatting.md`, `references/links-media-mentions.md`.
- `scripts/wa_lint.py`: `--kind about` (139), `business-description` (512), `group-description` (2,048), `quick-reply`.

## Related skills

`whatsapp-promotion` (offers to customers) · `whatsapp-announcement` (welcome and rules posts) ·
`whatsapp-channel` (channel posts) · `whatsapp-reply` (answering customers)
