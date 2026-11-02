# Channel formats

## How channels behave (design around this)

- One-way. Followers **react** (emoji), **vote** in polls, **forward**, and tap links. They can't reply in the channel.
- Followers don't see each other, and admins don't see followers' phone numbers. Never address a follower by name.
- Posts get forwarded into chats, out of context. Each post must stand alone.
- Channels support text, images, videos, documents, voice and polls.

## Header patterns

Pick one per channel and keep it.

| Channel kind | Header pattern |
|---|---|
| Daily tip series | `📌 *Day 4/30 · [Topic]*` |
| Numbered tips | `💡 *Tip #12: [Topic]*` |
| News / updates | `🗞️ *[Headline]*` |
| Weekly roundup | `📬 *This week in [topic] · [Date]*` |
| Deals | `🔥 *[Product] at [price]*` |
| School / coaching | `🏫 *[Class/Batch]: [What]*` |
| Creator updates | `[Signature emoji] *[What's new]*` |

## Post skeletons

### Tip / lesson

```text
[Header]

[The tip in 1-2 lines, with one bold anchor.]

[Why or how, 1-3 lines. One example if it helps.]

[Reaction or poll CTA.]
[Series footer, if a series.]
```

### News / update

```text
[Header]

[What happened, 1-2 lines.]
[Why it matters to this audience, 1 line.]

🔗 [Source link, only if given]
```

### Roundup (3-5 items)

```text
[Header]

*1. [Item]*
[One line + link]

*2. [Item]*
[One line + link]

*3. [Item]*
[One line + link]

[Footer: next roundup day]
```

### Resource drop

```text
📚 *[Resource name]*

[What it is + who it's for, 1 line.]
[Link or "PDF below".]

Forward it to someone preparing for [X].
```

### Countdown / launch

```text
⏳ *[N] days to [launch/event]*

[One teaser line.]
[Date + time.]
[What followers should do now: turn on notifications, save the date.]
```

### Poll post

Write the poll for the user to create in the app (up to 12 options):

```text
Poll question: [Question]
Options:
- [Option]
- [Option]
- [Option]
```
Optionally a one-line text post above it: "Help me pick next week's topic 👇"

### Welcome / pinned intro post

```text
👋 *Welcome to [Channel name]!*

[What followers get, and how often: "One money tip every morning at 8."]

[What to do: turn on notifications / react to tell me what you want more of.]
[Who runs it: one line.]
```

## Series footers

- `*Tomorrow:* [next topic]`
- `*Next Monday:* [next topic]`
- `*Part 2 drops if this gets 100 🔥*` (only if the user wants engagement gating)

## Cadence suggestions

- Daily series: same time every day (morning commutes or 8-9 pm work well for most audiences).
- Tips/updates: 3-5 posts a week beats 5 posts in one day.
- Big news: post once, then a follow-up only when there's something new.
