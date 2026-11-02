# Using the skills

## The one habit that matters

Say everything you know, once, in whatever order it comes to you. Typos,
lowercase, half-sentences and Hinglish are all fine. The skill sorts it out.

> *team group. all hands moved from fri 6 nov 4pm to thu 5 nov 11am because ceo travelling. same zoom link https://zoom.us/j/8812345678 passcode 4421. questions in the form before wed eod https://forms.gle/q7XyZ. from Anita HR*

What makes a brief good:

- **Who it's for**: "my manager", "class 7B parents group", "my broadcast list", "my status".
- **Every fact**: dates, times, places, amounts, names, links, phone numbers. Paste links as they are.
- **What you want them to do**: confirm, pay, come, reply, nothing.
- **Anything about tone** you care about: "not too formal", "funny", "she's upset".

You don't need to say which skill to use, or how to format it.

## Dials

Add any of these in plain words, anywhere in the brief.

| Dial | Say | Default |
|---|---|---|
| Length | one line · short · on point · mid · detailed · everything | depends on the message type |
| Tone | casual · warm · professional · formal · funny · urgent · respectful · apologetic | from who it's for |
| Formatting | no formatting · simple · proper · full formatting | light (bold on the key details) |
| Emoji | no emoji · few · more emoji | a few, as labels |
| Language | Hinglish · Hindi · Marathi · Tamil · Arabic · bilingual English + Gujarati · … | the language of your brief |

Mix freely: *"short, funny but respectful, Hinglish, no emoji"*.

## After the first draft

Reply with one word and you get the full revised message:

`shorter` · `longer` · `more formal` · `more casual` · `funnier` · `serious` · `add emoji` ·
`no emoji` · `more formatting` · `plain` · `in Hindi` · `in Hinglish` · `3 options` · `split it` ·
`make it a caption` · `make it a status`

## Standing preferences

Tell the AI once, and it applies to every message:

> *I'm Priya Nair, class teacher of 7B at St. Mary's. I write to parents in English, polite, no emoji. Sign group notices "– Mrs. Nair".*

Where to put it so it sticks:

- **claude.ai**: in a Project's instructions, or in your profile preferences.
- **Claude Code**: in your `CLAUDE.md` (project or `~/.claude/CLAUDE.md`).
- **ChatGPT**: in Custom Instructions or a Project.

## Replies

Paste their message (or a screenshot) and add what you want to say:

> *reply to this: "Can you also take the Q3 vendor review this week?" — can't, I'm on the audit till Friday, can do next Tuesday*

If you haven't decided, say "give me both" and you get a yes and a no version.
If the message looks like a scam (OTP, KYC link, "Hi Mom, new number", a stranger
asking for money), the skill tells you so instead of drafting a reply.

## Attachments, links and @mentions

- Mention what you'll attach ("poster attached", "sending the PDF"). The text is written as its caption, and the notes tell you the order to send things.
- Paste links exactly. They're labeled and put on their own lines; the most important one goes first so WhatsApp builds a preview for it.
- Write `@Name` for people to tag. After pasting, retype the `@` in WhatsApp and pick the contact. Pasted @names are plain text.

## Polls, events and pins

When a native WhatsApp feature would beat a text message (headcount, choosing a
date, an event people should RSVP to, a notice people must find again), the notes
suggest it and give you the exact poll question and options to type in.

## Checking your own text

Paste anything and say *"check this"* (report only), *"fix typos, keep my style"*
(minimal edits) or *"make this WhatsApp-ready"* (formatting only). See `whatsapp-formatter`.

With Python you can also run the checker yourself:

```bash
python3 shared/scripts/wa_lint.py message.txt
```

```bash
python3 shared/scripts/wa_lint.py --fix chatgpt_answer.md > message.txt
```

```bash
python3 shared/scripts/wa_lint.py --kind status status.txt
```
