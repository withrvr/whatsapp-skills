#!/usr/bin/env bash
# Rebuild the README demo GIF (silent 15 s loop, 800 px wide, 12 fps).
# Needs: Node 22 + Playwright (Chromium), ffmpeg, Inter and Noto Color Emoji fonts.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p frames
HTML="$PWD/demo.html" W=1280 H=720 OUT="$PWD" node ../launch/render.js full 30 15
ffmpeg -loglevel error -y -framerate 30 -i frames/%04d.png \
  -vf "fps=12,scale=800:-1:flags=lanczos,palettegen=max_colors=128:stats_mode=diff" palette.png
ffmpeg -loglevel error -y -framerate 30 -i frames/%04d.png -i palette.png \
  -lavfi "fps=12,scale=800:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle" \
  -loop 0 demo.gif
rm -rf frames stills palette.png
echo "Built demo.gif"
