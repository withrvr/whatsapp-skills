# Summary rules

## The five things to extract

| Thing | Signals in a chat | How to write it |
|---|---|---|
| **Decisions** | "final", "confirmed", "done", "let's go with", admin/organiser stating it, several 👍 on a proposal | What + who decided + when it applies |
| **Dates and deadlines** | weekdays, dates, "tomorrow", "by Friday", times | `Day, Date, time · what`, resolved against the message's own date |
| **Asks of the user** | @mentions, their name, "can you", replies quoting them | What, who asked, by when |
| **Links and files** | URLs, "PDF attached", `document omitted` | `Label: link` (label from the surrounding message) |
| **Open questions** | questions with no answer, disagreements | Question + who asked |

Everything else (greetings, thanks, jokes, forwards, "ok", stickers) is noise
unless the user asked for the full picture.

## Resolving relative dates

"Tomorrow" in a message sent on Sun, 1 Nov means Mon, 2 Nov. Always convert
relative dates using the **message's timestamp**, not today's date, and write the
weekday with the date.

## Long chats

- Up to a few hundred messages: read everything.
- Larger: use `wa_chat.py --since` for the user's window, or `--last 300`.
  For a month or more, summarise per week: `Week of 2 Nov: …`.
- Always use `--mentions <user's name>` once, so nothing addressed to them is missed.

## Export formats you'll see

- iPhone: `[02/11/26, 10:15:32 AM] Name: text`
- Android: `02/11/2026, 10:15 - Name: text` or `2/11/26, 10:15 pm - Name: text`
- Dates can be day-first or month-first depending on the phone's region;
  `wa_chat.py` guesses from the dates in the file (`--date-order` overrides).
- System lines (joins, leaves, "Messages and calls are end-to-end encrypted")
  are not messages. `<Media omitted>`, `image omitted` and `This message was deleted` can't be read.

## Minutes (MoM) to post

```text
📝 *Minutes: [meeting or topic], [Day, Date]*

*Decided*
1. [Decision]
2. [Decision]

*Action items*
- [Owner]: [task] by *[Day, Date]*
- [Owner]: [task] by *[Day, Date]*

*Still open:* [question]
*Next:* [next meeting / date]
```

- Owners by name as they appear in the group; the user retypes them as @mentions to tag.
- Only decisions that were actually agreed. Proposals go under "Still open".

## Recap to post (informal)

```text
Quick recap of today's discussion 👇

- [Point]
- [Point]
- [Point]

[What happens next + date]
```

## Catch-up for the user (not posted)

Plain chat text, sections in this order, empty ones dropped:
`In short` · `Decided` · `Dates` · `For you` · `Links and files` · `Still open`.
