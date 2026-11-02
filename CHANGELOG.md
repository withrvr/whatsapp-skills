# Changelog

All notable changes to this project. Versions follow [semver](https://semver.org).

## 1.0.0 (2026-11-02)

First release.

- 8 skills: `whatsapp-message`, `whatsapp-reply`, `whatsapp-announcement`,
  `whatsapp-invitation`, `whatsapp-promotion`, `whatsapp-status`,
  `whatsapp-channel`, `whatsapp-formatter`.
- Shared references: WhatsApp formatting, message dials, writing rules,
  links/media/mentions.
- `wa_lint.py`: pre-send checker and Markdown-to-WhatsApp converter (standard library only).
- Plugin manifests for Claude (claude.ai, Desktop, Claude Code) and OpenAI (Codex, ChatGPT).
- 131-scenario catalog, install and usage docs.
- 24 evals in the Agent Skills format with a runner that compares with and without skills.
- Voice rules: no em or en dashes anywhere in a message (lint error, `--fix` removes
  them), names capitalised as given, AI and email vocabulary list, specific over vague,
  one point per message, name-only sign-offs.
- English is the main focus; other languages are written on request.
- Pull-request-only workflow: each PR bumps the version (CI-checked) and merging
  it to `main` tags and publishes the release automatically.
