<!-- GENERATED from shared/references/links-media-mentions.md by scripts/sync.py. Edit the source, not this copy. -->
# Links, media, mentions and native features

Load this when the brief has links, an attachment (image, video, PDF, poster),
@mentions, a phone number, or when a poll, event or pin would serve the message
better than text.

## Links

- **WhatsApp builds a preview card from the first link** in a text message. Put
  the most important link first, or alone on its own line at the end.
- **No preview when the message has media.** If a poster and a link both matter,
  send the poster with the link in its caption (still tappable, just no card).
- **Always `https://`.** A bare `example.com` is not reliably tappable.
- **Label every link on the line before it or in front of it**, never with Markdown:

  ```
  📝 *Register:* https://forms.gle/AbC123
  📍 *Location:* https://maps.app.goo.gl/XyZ789
  ```

- **Never bold or italicise a URL**, and don't glue punctuation to it.
- **Never shorten, "clean" or guess a link.** Copy it exactly. If a venue has no map link, say so in Notes instead of inventing one.
- More than ~5 links is a sign the content belongs in a document or a second message.

### Links WhatsApp users use

| Link | Shape | Notes |
|---|---|---|
| Click-to-chat | `https://wa.me/919876543210` | Digits only: country code + number, no `+`, spaces or dashes. Add `?text=Hi%20there` to prefill (URL-encoded). |
| Group invite | `https://chat.whatsapp.com/…` | Anyone with it can join. Warn before posting it publicly. |
| Channel | `https://whatsapp.com/channel/…` | |
| Maps | `https://maps.app.goo.gl/…` | Use the share link the user gives. |
| Meeting | Meet / Zoom / Teams URL | Meeting ID and passcode on their own lines, in `` `inline code` ``. |
| Payment | UPI ID, payment link | Copy exactly. Never ask anyone for an OTP or PIN. |

## Phone numbers and emails

- `+91 98765 43210` style (with country code) is tappable everywhere.
- Never wrap a number or email in formatting markers.
- Label it: `📞 Rahul: +91 98765 43210`.

## Media and captions

When the user will attach something, the text you write is its **caption**.

- **Line 1 must make sense next to the image** in the chat list and in the notification.
- **Keep the key facts in text even if the poster shows them.** Captions are
  searchable, readable when the image fails to load, and survive forwarding.
- **Keep captions under ~1,000 characters.** (The Business API caps captions at
  1,024; long ones collapse anyway.) If there's more, send the media with a short
  caption and the details as a second message.
- **Albums**: the caption goes on the first item. Or send the text first and the album after.
- **Documents (PDF, DOCX, PPT):** everyone sees the file name. Suggest a clean one
  in Notes: `Class10_Physics_Ch3_Notes.pdf`, not `scan0042_final(2).pdf`. Caption
  = what it is + what to do with it + by when.
- **Video / voice note**: a one-line text lead-in helps people who can't play it now.

## Mentions

- `@Name` in the drafted text is **plain text**. To create a real tag the user
  deletes it and types `@`, then picks the contact. Always say this in Notes when
  the message has @mentions.
- Tags notify people even in a muted group. Tag the people who must act, not the whole group.
- Write `@Name` with the name as the user gave it, so it's easy to re-tag.

## Native features that beat text

Suggest one in Notes when it fits, and write its content so the user can create it in seconds.

| Situation | Feature | What to give the user |
|---|---|---|
| Headcount, choosing a date, menu, T-shirt size | **Poll** (up to 12 options, single or multiple answers) | `Poll question:` + `Options:` list |
| Meetup, class, call, party in a group or community | **Event** (name, date and time, location or call link; members can RSVP) | Event name, description line, date/time, location |
| A notice people must find again | **Pin** the message in the group | Say "Pin this" in Notes |
| One-way notices to many groups | **Community announcement group** | Same message, no change |
| Same message to many 1:1 chats | **Broadcast list** (only people who saved your number receive it) | Message written to read well 1:1, no "Hi all" |
| Typo spotted after sending | **Edit** (within 15 minutes) | Nothing, just fix it |

Format a poll suggestion like this in Notes or as its own block:

```text
Poll question: Which Saturday works for the offsite?
Options:
- 14 Nov
- 21 Nov
- 28 Nov
- Can't make any
```
