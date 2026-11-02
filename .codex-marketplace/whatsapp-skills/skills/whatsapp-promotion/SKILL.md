---
name: whatsapp-promotion
description: "Write WhatsApp business and marketing messages for a shop, small business, freelancer, coach or creator: sales and offers, festive campaigns, launches, new arrivals, course promos, service reminders, review and referral asks, catalog shares, listings, order confirmed, shipped and delivered, payment received or due, cart reminders, broadcast welcome. Use whenever someone wants to promote or sell on WhatsApp or message customers. Real terms, one call to action, opt-out line. Not for invitations (use whatsapp-invitation) or profile text (use whatsapp-setup)."
license: MIT
metadata:
  author: withrvr
  version: "1.0.1"
---

# WhatsApp Promotion

A shop owner, tutor, salon, baker, real-estate agent, coach or creator wants to
tell their customers about an offer or a launch. WhatsApp is personal: a promo
that reads like spam gets the sender muted, blocked or reported. You write the
message that customers are glad to get: the benefit up front, honest terms, one
easy way to act.

## When to use

- "Diwali sale message for my customers", "new collection arrived"
- "Promote my webinar / course / workshop / coaching batch"
- "Remind clients their service is due", "follow up on an enquiry"
- "Ask happy customers for a Google review / referral"
- "Share my price list / catalog", "property listing for my broadcast list"
- "Order confirmed / shipped / delivered message", "payment received", "payment due reminder", "cart reminder", "welcome message for my broadcast list"

**Not for:** inviting people to a celebration (`whatsapp-invitation`), a notice
with nothing to sell (`whatsapp-announcement`), status text (`whatsapp-status`),
channel posts and series (`whatsapp-channel`).

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

1. **Collect the offer facts**: what's offered, price / discount (exact), validity
   (start, end), conditions, how to buy or book (wa.me link, website, store
   address, "reply YES"), the business name, who receives it (broadcast list,
   customer group, community), attachments (catalog, poster, reel).
2. **Pick the type** in `references/promo-types.md`.
3. **Set the dials.** Defaults: length `short` (medium for launches and courses),
   tone `warm` (upbeat for sales), formatting `light`, emoji `few`.
4. **Line 1 is the benefit** in the customer's words, not the business's
   ("Your Diwali sweets, delivered fresh" beats "We are pleased to announce").
5. **Then proof or detail** (what's included, price, a strikethrough old price),
   **validity**, **one call to action**, **business name**, **opt-out** for broadcasts.
6. **Check and deliver.** Notes for: attach the poster/catalog, broadcast-list reach, timing.

## Rules for promotions

- **Never invent an offer, price, discount, validity date, stock level, review or testimonial.**
  No "only 3 left" or "ends tonight" unless it's true and the user said it.
- **Prices exact and readable:** ₹1,499, not 1499/-. Old price struck through: `~₹1,999~ *₹1,499*`.
- **One call to action.** Reply with a word, tap a wa.me link, or visit a link. Not three.
- **Terms in one line** when they exist ("Valid till Sun, 15 Nov. Not valid on sale items.").
- **Opt-out for broadcast lists:** end with "Reply STOP to stop these messages."
  (For a group the customer joined, not needed.)
- **Festive messages:** greeting first and genuine; the offer after a line break, never in the same sentence as the blessing.
- **No promos into groups that aren't the user's** (school groups, society groups)
  unless the group allows it. Say so in Notes if the brief implies it.
- **Claims:** no medical, financial-return or "guaranteed" claims the user can't back.
  Regulated goods (alcohol, tobacco, weapons, drugs, adult content, gambling) aren't allowed under WhatsApp's commerce policy: decline.
- **Frequency:** if the user plans daily blasts, suggest a status or channel in Notes instead.

## Example

**Brief:** *home bakery Sweet Crumbs. diwali hampers: 12 cookies + 4 brownies + diya, ₹899 (usually 1,199). order by thu 5 nov, delivery 6-8 nov in pune. order on https://wa.me/919822012345?text=Diwali%20hamper. broadcast list*

```text
🪔 *Diwali hampers are here!*

12 handmade cookies, 4 fudgy brownies and a diya, packed and ready to gift.

~₹1,199~ *₹899*
📅 Order by *Thu, 5 Nov* · Delivery 6 to 8 Nov in Pune

👉 Order here: https://wa.me/919822012345?text=Diwali%20hamper

Sweet Crumbs
Reply STOP to stop these messages.
```

## References

- `references/promo-types.md`: skeletons for 14 promotion types plus 7 order, payment and broadcast-welcome messages. Load at step 2.
- `references/examples.md`: worked promos (sale, launch, course, service reminder, review ask, listing).
- `references/links-media-mentions.md`: wa.me links with prefilled text, catalog links, posters and captions.
- `references/message-dials.md`, `references/writing-rules.md`, `references/whatsapp-formatting.md`.
- `scripts/wa_lint.py`: pre-send check (`--kind promotion`, or `--kind caption` with a poster).

## Related skills

`whatsapp-status` (offer as a 24-hour status) · `whatsapp-channel` (regular
posts to followers) · `whatsapp-reply` (answering customer enquiries) ·
`whatsapp-setup` (business description, greeting, away message, quick replies)
