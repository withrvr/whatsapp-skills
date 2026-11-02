#!/usr/bin/env bash
# Rebuild the launch video: soundtrack, frames, poster and MP4.
# Needs: Node 22 + Playwright (Chromium), Python 3 + numpy, ffmpeg, and the
# Inter and Noto Color Emoji fonts installed. Run from anywhere.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p frames
python3 synth.py                                   # -> audio.wav (-14 LUFS)
node render.js full 30 22                          # -> frames/0000.png .. 0659.png
cp frames/0648.png poster.png                      # settled outro frame
ffmpeg -loglevel error -y -i poster.png -q:v 2 launch.jpg
cp poster.png frames/0000.png                      # poster as frame 0 = thumbnail
ffmpeg -loglevel error -y -framerate 30 -i frames/%04d.png -i audio.wav \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -profile:v high \
  -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart launch.mp4
rm -rf frames stills poster.png audio.wav
echo "Built launch.mp4 and launch.jpg"
