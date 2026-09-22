#!/usr/bin/env bash
# Render every clip at 720p30, copy the mp4 into out/ and a poster frame into frames/.
set -euo pipefail
cd "$(dirname "$0")"
MANIM="${MANIM:-$HOME/.venvs/sbd-animations/bin/manim}"
MEDIA=/Users/niccolo/.cache/ese-ai-manim/videos

render () {  # render <module> <Scene> <output-name>
  PYTHONPATH=src "$MANIM" -qm --disable_caching "src/$1.py" "$2" -o "$3.mp4" >/dev/null 2>&1
  cp "$MEDIA/$1/720p30/$3.mp4" "out/$3.mp4"
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "out/$3.mp4")
  ffmpeg -v error -y -ss "$(echo "$dur * 0.78" | bc -l)" -i "out/$3.mp4" -frames:v 1 "frames/$3.png"
  printf '%-20s %5.1fs  %s\n' "$3" "$dur" "$(du -h "out/$3.mp4" | cut -f1)"
}

only="${1:-all}"
[ "$only" = all ] || [ "$only" = w01 ] && render w01_tokens     TwoTokenizers   w01_tokens
[ "$only" = all ] || [ "$only" = w02 ] && render w02_calendars  Calendars       w02_calendars
[ "$only" = all ] || [ "$only" = w03 ] && render w03_splits     Splits          w03_splits
[ "$only" = all ] || [ "$only" = w04 ] && render w04_retrieval  MeaningIsAPlace w04_retrieval
[ "$only" = all ] || [ "$only" = w05 ] && render w05_agentloop  AgentLoop       w05_agentloop
[ "$only" = all ] || [ "$only" = w07 ] && render w07_lookahead  LookAhead       w07_lookahead
[ "$only" = all ] || [ "$only" = w08 ] && render w08_amm        ConstantProduct w08_amm
echo done
