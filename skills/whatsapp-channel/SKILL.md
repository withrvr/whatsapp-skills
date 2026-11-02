---
name: whatsapp-channel
description: "Write WhatsApp Channel posts in a consistent creator, brand, school or community voice: updates, tips, news roundups, daily or weekly series (Day 3 of 30, Tip #12), countdowns, resource drops, welcome and poll posts. Use whenever someone posts to or plans content for a WhatsApp Channel. Plans short series and keeps numbering, header and footer consistent. Not for two-way group chats (use whatsapp-announcement) or 24-hour status (use whatsapp-status)."
license: MIT
metadata:
  author: withrvr
  version: "1.0.1"
---

# WhatsApp Channel

A Channel is one-way: the admin posts, followers read, react with an emoji, vote
in polls and forward posts into their chats. They can't reply in the channel.
People follow for a reason (tips, news, deals, a creator's updates) and unfollow
when posts get noisy. You write posts that deliver that reason in seconds and
are worth forwarding.

## When to use

- "Post for my channel about …", "today's tip for the channel"
- "Start a 30-day series on …", "plan 7 posts for next week", "write Day 4"
- "Welcome post for my new channel", "weekly roundup"
- School, college, coaching, community, news, deals and creator channels.

**Not for:** groups where members reply (`whatsapp-announcement`), status
(`whatsapp-status`), one-off sales blasts to a broadcast list (`whatsapp-promotion`).

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

1. **Know the channel**: name, topic, audience, voice, and any existing format
   (header style, numbering, sign-off). If the user pasted earlier posts, copy
   their format exactly. Otherwise set one from `references/channel-formats.md`.
2. **Pick the post type** (update, tip, series entry, roundup, resource drop,
   countdown, poll post, welcome).
3. **Set the dials.** Defaults: length `short` to `medium`, tone = the channel's voice,
   formatting `light`, emoji `few`.
4. **Write the post**: header line → the value (the tip, the news, the resource) →
   the one action (react, vote, tap link, forward) → series footer if it's a series.
5. **Check and deliver.**

## Rules for channel posts

- **Lead with the value.** The header plus the first line should be worth it alone.
- **Series stay consistent**: same header pattern (`📌 *Day 4/30 · Excel shortcuts*`),
  same structure, same footer ("Tomorrow: …"). Never skip or repeat a number; ask
  for the last number if you don't know it.
- **Calls to action that work in a channel**: react with an emoji ("React 🔥 if
  you want part 2"), vote in a poll, tap a link, forward to a friend. Never "reply
  below" or "comment" (followers can't).
- **Forward-friendly**: posts get forwarded into chats out of context, so each one
  stands alone. Put the channel link at the end only if the user gave it.
- **No follower data**: followers are private. Don't write "Hi Rahul" style posts.
- **Frequency**: suggest a rhythm in Notes when the user asks to plan (a series is
  better at a fixed time daily or 2-3 times a week than in bursts).

## Planning a series

When asked to plan: give the plan as a short numbered list in chat (title + one
line each), then **fully write post 1** in a `text` block. Write the rest when
asked ("write day 2", "write all"). Keep the format identical across posts.

## Example

**Brief:** *my channel 'Money Mornings' (personal finance tips for 20-somethings). day 3 of 21 day series. topic: emergency fund = 6 months expenses, keep in liquid fund or sweep FD, not stocks. tomorrow: credit score*

```text
📌 *Day 3/21 · Your emergency fund*

Before investing, build a cushion of *6 months of expenses*.

Keep it somewhere you can withdraw in a day or two: a liquid fund or a sweep-in FD. Not in stocks, because emergencies don't wait for the market to recover.

React 💰 if you've started yours.

*Tomorrow:* what your credit score really is
```

## References

- `references/channel-formats.md`: header, series and footer formats, post types, welcome post, poll posts, cadence. Load at step 1.
- `references/examples.md`: worked posts for creator, coaching, news-roundup and deals channels.
- `references/message-dials.md`, `references/writing-rules.md`, `references/whatsapp-formatting.md`.
- `references/links-media-mentions.md`: when posts carry links, images or polls.
- `scripts/wa_lint.py`: pre-send check (`--kind channel`).

## Related skills

`whatsapp-status` (24-hour updates) · `whatsapp-announcement` (groups) · `whatsapp-promotion` (offers) ·
`whatsapp-setup` (channel name and description)
