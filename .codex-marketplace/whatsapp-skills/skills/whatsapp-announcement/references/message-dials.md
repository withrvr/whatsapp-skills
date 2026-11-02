<!-- GENERATED from shared/references/message-dials.md by scripts/sync.py. Edit the source, not this copy. -->
# Message dials

Every message is set by a few dials. The user can set any of them in plain words,
in any order, anywhere in the brief: *"short, funny, no emoji, Hinglish"*.
Explicit dials win. Missing dials are inferred from the audience and the
situation. Anything still unknown takes the skill's default.

## The dials

### Length

| Setting | Also understood as | Size | Use for |
|---|---|---|---|
| `one-liner` | "one line", "tiny" | ≤ 120 characters | Quick confirms, status, nudges |
| `short` | "on point", "crisp", "brief", "quick" | ≤ 350 characters, 1-4 lines | Most 1:1 messages, reminders |
| `medium` | "mid", "normal" | 350-900 characters | Announcements, invites, promos |
| `long` | "high", "detailed", "full", "everything" | 900+ characters | Notices with many details, schedules, multi-part info |

Length never drops a fact the user gave. If everything doesn't fit the chosen
length, keep the facts and cut the words, or split into two messages and say so.

### Tone

| Setting | What changes |
|---|---|
| `casual` | Contractions, lowercase is fine, slang the user uses, no sign-off |
| `warm` | Friendly greeting, a line of personal touch, "thanks" / "see you" |
| `friendly-professional` | Clear and polite, contractions ok, no slang, minimal emoji. Default for work. |
| `formal` | Full sentences, "Dear …" / "Good morning Sir", no slang, no emoji, name + role sign-off |
| `funny` | One joke or playful line built on the situation, never at someone's expense. Facts stay exact. |
| `urgent` | Lead with the alert word and the action, no greeting, no jokes, no emoji except ⚠️ |
| `celebratory` | Upbeat opener, 🎉-style emoji allowed, exclamation once |
| `respectful` | For elders, teachers, religious or family occasions: honorifics (ji, Sir, Ma'am), no slang |
| `apologetic` | Own it in line 1, state the fix, no over-explaining |
| `persuasive` | Benefit first, one proof point, one clear call to action |

Tone mixes are fine: "funny but respectful", "formal but warm".

### Formatting

`plain` · `light` · `full`. Defined in `whatsapp-formatting.md`.
"No formatting", "simple" → `plain`. "Proper", "neat", "structured" → `full`.

### Emoji

| Setting | Means |
|---|---|
| `none` | Zero. Also forced for condolences, layoffs, serious alerts, formal notes. |
| `few` | 0-3, as line labels or one at the end. Default. |
| `rich` | Allowed as labels on most lines plus a couple in prose. Still not after every sentence. |

### Language and script

1. Explicit request wins: "in Hindi", "Hinglish", "in Tamil", "bilingual English + Marathi".
2. Otherwise write in the language the brief is in. Exception: a brief in mixed
   Hinglish for an office or formal audience gets clear English unless the user
   asks for Hinglish.
3. **Hinglish** means Hindi words in Roman script, spelled the way people type on
   WhatsApp: *kal, aaj, hai, bhi, kar do, pls, sab log*. No Devanagari unless asked.
4. **Other scripts** (Devanagari, Tamil, Bengali, Arabic, …): write natively and
   naturally, not a word-by-word translation of English.
5. **Bilingual**: the whole message in the first language, a blank line, then the
   whole message in the second. Don't interleave line by line.
6. Never translate names, links, phone numbers, codes or amounts. Keep dates and
   times in the form the audience reads (e.g. "Sat, 14 Nov" or "14 नवंबर, शनिवार").

### Audience and relationship

Inferred from who the message goes to. It sets the defaults for tone and greeting.

| Audience | Default tone | Greeting |
|---|---|---|
| Friend, sibling, close colleague | casual | "Hey", or none mid-chat |
| Team or office group | friendly-professional | "Hi team", "Hi all" |
| Boss, senior, client | friendly-professional or formal | "Hi Priya", "Good morning Sir" |
| Elder relative, teacher, guest of honour | respectful | "Namaste Mama ji", "Respected Ma'am" |
| Parents group (school), residents (society) | friendly-professional | "Dear Parents", "Dear Residents" |
| Customers | warm | "Hi [first name]" or "Hello!" |
| Stranger / new contact | friendly-professional | "Hi [name], I'm …" (introduce yourself in line 1) |
| Community or channel followers | the creator's voice | none or a signature opener |

### Voice

- `I` for a personal message, `we` for a business, team or family as hosts.
- **Sign-off**: none in casual chats. A name + role in group notices when the
  sender's authority matters ("– Priya, Class Rep"). Name + role + organisation
  on a first message to a stranger.

## Standing preferences

If the user has already told you their defaults (in this conversation, in
project or custom instructions, `CLAUDE.md`, or memory), they act as explicit
dials for every message: their name and role, default language, emoji habit,
sign-off, how they address their boss. Once the user sets a dial in a
conversation ("Hinglish, no emoji"), keep it for the next messages until they
change it.

## Quick adjustments after a draft

The user will often reply with one word. Apply it to the last message and send
the full revised message (not a diff):

`shorter` · `longer` · `more formal` · `more casual` · `funnier` · `serious` ·
`add emoji` · `no emoji` · `more formatting` · `plain` · `in Hindi` / `in Hinglish` /
`in <language>` · `3 options` · `split it` · `make it a caption` · `make it a status`
