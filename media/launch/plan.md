# Launch video plan: whatsapp-skills

## Inspect

- **What it is:** 11 open-source Agent Skills that turn the messy context in your head into a ready-to-paste WhatsApp message.
- **Who it's for:** anyone who writes WhatsApp messages with an AI and then fixes them by hand: team leads, teachers, society secretaries, small shops, creators.
- **What sets it apart:** WhatsApp-native output. Real `*bold*` instead of Markdown `**stars**`, no em dashes, weekdays checked against dates, a built-in linter (`wa_lint.py`) in every skill. Works in Claude, ChatGPT/Codex and any agent that reads SKILL.md.
- **Most impressive claim (real, from the eval run):** 33 prompts, 99% of checks pass with the skills vs 60% for the same model without them.
- **Visual hook:** lowercase notes typing in fast → snapping into a clean WhatsApp message.
- **Real UI / flow shown:** the brief and output from `skills/whatsapp-announcement/SKILL.md`'s worked example; real `wa_lint.py` error codes (MD_BOLD, EM_DASH, WEEKDAY_MISMATCH); the real skill names; the real install command.
- **Tone:** `default`, punchy, playful, clean.
- **Share caption:** see `share-copy.txt`.
- **Privacy:** every name, number and link on screen is the repo's own fictional example data (Anita from HR, zoom.us/j/8812345678). No real people.

## Format

Square 1080×1080, 30 fps, 22 s, for the LinkedIn feed (square holds the most screen on mobile).
Music: 120 BPM (1 beat = 0.5 s = 15 frames, 1 bar = 2 s), C major, I–V–vi–IV. Every cut lands on a beat.

## Storyboard

| # | Time | Beats | Scene | On screen |
|---|---|---|---|---|
| 1 | 0.0–3.0 | 6 | **Hook** | "You know exactly what to say." Lowercase notes type in fast underneath: `all hands moved fri 4pm → thu 11am…` |
| 2 | 3.0–7.0 | 8 | **Reveal** | "Get the WhatsApp message." A chat bubble builds line by line with the finished announcement, bold and strikethrough rendered. Chip: `/whatsapp-announcement` |
| 3 | 7.0–11.0 | 8 | **Highlight: it's WhatsApp, not Markdown** | "Formatting that actually renders." Typical AI bubble with literal `**stars**`, an em dash and "Friday, 7 Nov"; the checker flags MD_BOLD, EM_DASH, WEEKDAY_MISMATCH; the fixed bubble lands with "✓ ready to paste." |
| 4 | 11.0–15.0 | 8 | **Highlight: 11 skills** | "11 skills. One for every message." Cards pop on half-beats: message, reply, announcement, invitation, promotion, status, channel, formatter, redact, setup, catchup, + 170 scenarios |
| 5 | 15.0–18.0 | 6 | **Highlight: proof** | "Tested on 33 real prompts." Bars fill: with skills 99%, same model without 60% |
| 6 | 18.0–22.0 | 8 | **Punchline / outro** | Icon, "whatsapp-skills", "Give the context once. Get the message to paste.", typed install command, "Free & open source · Claude · ChatGPT · Codex" |

Poster: settled outro frame (name, tagline and install line all visible).

## Sound

Synthesised in one pass on the 120 BPM grid: four-on-the-floor kick (soft first bar), clap on 2 and 4, off-beat hats, eighth-note bass, plucked arpeggio and a pad on C–G–Am–F. Effects are pitched into the key and sit under the music: quiet key ticks while typing, soft filtered whooshes on cuts, pentatonic pops for each skill card, a rising tone under the bar fill. Drums drop for the last bar so the outro breathes; final chord rings and fades.
