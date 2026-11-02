# Changelog

All notable changes to this project. Versions follow [semver](https://semver.org).

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
- Launch video for LinkedIn (`media/launch/`, 22 s square, with sound) and a silent
  README demo loop (`media/demo/`), both rebuilt from source with their `build.sh`.
- Pull-request-only workflow: each PR bumps the version (CI-checked) and merging
  it to `main` tags and publishes the release automatically.
