# Changelog

All notable changes to this project. Versions follow [semver](https://semver.org).

## 1.0.1 (2026-11-02)

- README: a silent 15-second demo loop at the top (`media/demo/`): notes become a
  message, AI formatting gets fixed, private details get masked. Rebuilt from
  source with `media/demo/build.sh`.
- README: test results now lead with plain counts anyone can read (out of 33 test
  requests, `**stars**` instead of bold: 25 without the skills, 0 with; em dashes:
  10 vs 0). The automated-check percentage stays as a labeled third row.
- Tests: the mention check covers more names and file types and looks only at
  files git tracks.

## 1.0.0 (2026-11-02)

First release.

- 11 skills: `whatsapp-message`, `whatsapp-reply`, `whatsapp-announcement`,
  `whatsapp-invitation`, `whatsapp-promotion`, `whatsapp-status`,
  `whatsapp-channel`, `whatsapp-formatter`, `whatsapp-redact`, `whatsapp-setup`,
  `whatsapp-catchup`.
- Shared references: WhatsApp formatting, message dials, writing rules,
  links/media/mentions.
- `wa_lint.py`: pre-send checker, Markdown-to-WhatsApp converter, and sensitive-data
  finder and masker with Luhn, Verhoeff and IBAN checksums (standard library only).
- `wa_chat.py`: WhatsApp chat-export parser for Android and iPhone formats.
- New scenarios: order, delivery and payment messages, cart reminders, broadcast
  welcomes, job openings, urgent help requests, minutes, stand-ups, buy-sell-rent
  posts, event recaps, voice-note scripts.
- Plugin manifests for Claude (claude.ai, Desktop, Claude Code) and OpenAI (Codex, ChatGPT).
- 170-scenario catalog, install and usage docs.
- 33 evals in the Agent Skills format with a runner that compares with and without skills.
- Voice rules: no em or en dashes anywhere in a message (lint error, `--fix` removes
  them), names capitalised as given, AI and email vocabulary list, specific over vague,
  one point per message, name-only sign-offs.
- English is the main focus; other languages are written on request.
- Pull-request-only workflow: each PR bumps the version (CI-checked) and merging
  it to `main` tags and publishes the release automatically.
