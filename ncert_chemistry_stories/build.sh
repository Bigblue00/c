#!/usr/bin/env bash
# Render story episodes and assemble the videos.
#
#   ./build.sh                       # every episode, then one video per class
#   ./build.sh c10_ch3_salt          # just these episodes
#   WIDTH=1280 HEIGHT=720 SAMPLES=16 ./build.sh   # higher quality (slower)
#
# Steps: prepare.py (plans + audio mix) -> render_story.py (frames) ->
# ffmpeg (episode MP4 with narration) -> one MP4 per class.
# Run narrate.py first if you want the spoken narration.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
FRAMES="${FRAMES:-$HERE/frames}"
VIDEOS="${VIDEOS:-$HERE/videos}"
WIDTH="${WIDTH:-960}"
HEIGHT="${HEIGHT:-540}"
SAMPLES="${SAMPLES:-8}"
FPS="${FPS:-12}"
mkdir -p "$VIDEOS/episodes"

cd "$HERE"
python3 prepare.py "$@"

if [ $# -gt 0 ]; then
  IDS=("$@")
else
  mapfile -t IDS < <(python3 -c "from episodes import EPISODES; print('\n'.join(e['id'] for e in EPISODES))")
fi

render() {
  if command -v blender >/dev/null 2>&1; then
    blender -b -P "$HERE/render_story.py" -- "$@"
  else
    python3 "$HERE/render_story.py" "$@"
  fi
}

for id in "${IDS[@]}"; do
  out="$VIDEOS/episodes/$id.mp4"
  if [ -f "$out" ]; then echo "skip $id (done)"; continue; fi
  render "plans/$id.json" --out "$FRAMES" --width "$WIDTH" --height "$HEIGHT" \
    --samples "$SAMPLES" --fps "$FPS" | grep --line-buffered -E "frame [0-9]+/[0-9]+ \(rendered" | awk 'NR%60==0' || true
  audio="audio/$id/episode.wav"
  if [ -f "$audio" ]; then
    ffmpeg -y -loglevel error -framerate "$FPS" -i "$FRAMES/$id/%05d.png" -i "$audio" \
      -r 24 -c:v libx264 -pix_fmt yuv420p -crf 22 -c:a aac -b:a 128k -shortest "$out"
  else
    ffmpeg -y -loglevel error -framerate "$FPS" -i "$FRAMES/$id/%05d.png" \
      -r 24 -c:v libx264 -pix_fmt yuv420p -crf 22 "$out"
  fi
  echo "done $id"
done

# One video per class, episodes in syllabus order.
for cls in 10 11 12; do
  list="$(mktemp)"
  for id in $(python3 -c "from episodes import EPISODES; print(' '.join(e['id'] for e in EPISODES if e['class']==$cls))"); do
    [ -f "$VIDEOS/episodes/$id.mp4" ] && echo "file '$VIDEOS/episodes/$id.mp4'" >> "$list"
  done
  if [ -s "$list" ]; then
    ffmpeg -y -loglevel error -f concat -safe 0 -i "$list" -c copy "$VIDEOS/class_${cls}_chemistry_stories.mp4"
    echo "wrote $VIDEOS/class_${cls}_chemistry_stories.mp4"
  fi
  rm -f "$list"
done
