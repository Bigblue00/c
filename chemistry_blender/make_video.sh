#!/usr/bin/env bash
# Render every reaction with Blender and join them into one MP4.
#
#   ./make_video.sh                 # full quality (1280x720, slow on CPU)
#   ./make_video.sh --samples 6 --width 640 --height 360   # quick preview
#
# Needs either the `blender` executable or the `bpy` Python module
# (pip install bpy), plus ffmpeg.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
FRAMES="${FRAMES:-$HERE/frames}"
OUT="${OUT:-$HERE/chemistry_reactions.mp4}"
REACTIONS=(water methane ammonia salt neutralization)

if command -v blender >/dev/null 2>&1; then
  blender -b -P "$HERE/chemistry_reactions.py" -- --out "$FRAMES" --reaction all "$@"
else
  python3 "$HERE/chemistry_reactions.py" --out "$FRAMES" --reaction all "$@"
fi

LIST="$(mktemp)"
for r in "${REACTIONS[@]}"; do
  ffmpeg -y -loglevel error -framerate 24 -i "$FRAMES/$r/%04d.png" \
    -c:v libx264 -pix_fmt yuv420p -crf 20 "$FRAMES/$r.mp4"
  echo "file '$FRAMES/$r.mp4'" >> "$LIST"
done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" -c copy "$OUT"
rm -f "$LIST"
echo "Wrote $OUT"
