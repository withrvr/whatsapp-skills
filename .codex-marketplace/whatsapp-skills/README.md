<p align="center">
  <img src="assets/icon.svg" alt="" width="84" height="84">
</p>

<h1 align="center">WhatsApp Skills</h1>

<p align="center">
  <b>Tell your AI the situation once. Get the WhatsApp message, ready to paste.</b><br>
  11 open-source Agent Skills for Claude, ChatGPT and Codex.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude-plugin-D97757" alt="Claude plugin">
  <img src="https://img.shields.io/badge/ChatGPT%20%2F%20Codex-plugin-111827" alt="ChatGPT and Codex plugin">
  <img src="https://img.shields.io/badge/Agent_Skills-open_standard-6E56CF" alt="Agent Skills">
  <img src="https://img.shields.io/badge/license-MIT-22C55E" alt="MIT license">
</p>

<p align="center">
  <img src="media/demo/demo.gif" alt="Demo: messy notes become a WhatsApp message, AI formatting gets fixed, private details get masked" width="800">
</p>

## You type this

```
msg for the team group: all hands moved from fri 4pm to thu 11am, ceo travelling.
same zoom link https://zoom.us/j/8812345678. questions by wed eod. from anita hr
```

## You paste this

```text
📢 *All-hands moved to Thu, 5 Nov, 11 am*

It was on ~Fri, 6 Nov, 4 pm~. Moved because our CEO is travelling.

🔗 *Zoom:* https://zoom.us/j/8812345678
📝 *Questions:* send them by Wed end of day

Anita, HR
```

Bold that actually shows as bold, the old time struck through, your link untouched,
weekday checked against the date. No `**stars**`, no em dashes, nothing invented.

## Install

**Claude (web and desktop):** Customize → Plugins → Add marketplace → `withrvr/whatsapp-skills`, then add it from Discover.

**Claude Code:**

```
/plugin marketplace add withrvr/whatsapp-skills
/plugin install whatsapp-skills@whatsapp-skills
```

**Codex, Cursor, Gemini CLI and other agents:**

```bash
npx skills add withrvr/whatsapp-skills
```

ChatGPT and every other option: **[docs/INSTALL.md](docs/INSTALL.md)**

## 11 skills, one for every message

| Skill | Writes |
|---|---|
| `whatsapp-message` | 1:1 messages: your boss, HR, clients, landlords, new contacts, family |
| `whatsapp-reply` | The reply to a message you got. Spots scams instead of answering them |
| `whatsapp-announcement` | Group notices: meetings, alerts, PTMs, fee dues, study material |
| `whatsapp-invitation` | Weddings, birthdays, poojas, parties, plus reminders and thank-yous |
| `whatsapp-promotion` | Offers, launches, order and payment updates for your customers |
| `whatsapp-status` | Status updates and photo captions within the 700-character limit |
| `whatsapp-channel` | Channel posts and daily or weekly series |
| `whatsapp-formatter` | Fixes ChatGPT or Claude Markdown so it renders in WhatsApp |
| `whatsapp-redact` | Hides phone numbers, UPI IDs, Aadhaar and names before you share a chat |
| `whatsapp-setup` | Business description, greeting and away messages, group rules |
| `whatsapp-catchup` | "What did I miss?" from a busy group, plus minutes to post back |

You never pick one. Describe the situation and the right skill steps in.
See all **[170 everyday scenarios](docs/SCENARIOS.md)**.

## Why it's better than asking AI directly

- **Real WhatsApp formatting.** `*bold*`, `_italic_`, `~strike~` and lists that render, instead of Markdown junk.
- **Your facts, exactly.** Dates, links, numbers and names are copied, never made up.
- **Checked before you see it.** Wrong weekdays, em dashes, status length and sensitive numbers get caught.
- **Your tone, your language.** Short or detailed, formal or funny, English, Hinglish, Hindi and more.

In 33 test requests, plain AI showed `**stars**` instead of bold **25 times**. With the skills: **0**.
How we test: **[docs/HOW-IT-WORKS.md](docs/HOW-IT-WORKS.md)**

## More

[Usage guide](docs/USAGE.md) · [All scenarios](docs/SCENARIOS.md) · [How it works](docs/HOW-IT-WORKS.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md)

Draft-only by design: nothing is sent for you. No WhatsApp API, no accounts, no network calls.

If it saves you a rewrite, a ⭐ helps others find it.

<sub>MIT licensed. Not affiliated with, endorsed by or sponsored by WhatsApp or Meta. WhatsApp is a trademark of WhatsApp LLC.</sub>
