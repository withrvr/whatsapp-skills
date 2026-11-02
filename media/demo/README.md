# README demo

The silent loop at the top of the main README: three things the skills do, five
seconds each, landscape so it fits the GitHub page.

1. Messy notes in, WhatsApp message out (`whatsapp-announcement`)
2. Fixes what AI gets wrong for WhatsApp: Markdown stars, em dashes, a wrong weekday (`whatsapp-formatter`)
3. Hides private details before you share a chat (`whatsapp-redact`)

| File | What it is |
|---|---|
| `demo.gif` | The loop, 800 px wide, 12 fps |
| `demo.html` | The composition: every frame is a pure function of time |
| `render.js` | Captures each frame with Playwright |
| `build.sh` | Rebuilds `demo.gif` in one command |

All names, numbers and links are the repo's own fictional example data.

## Rebuild after a change

```bash
./media/demo/build.sh
```

Needs Node 22 with Playwright (Chromium), ffmpeg, and the Inter and Noto Color
Emoji fonts.
