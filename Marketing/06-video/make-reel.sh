#!/usr/bin/env bash
# make-reel.sh — turn brand slide PNGs into a 9:16 reel (TikTok / IG Reels / Shorts).
# All-free: ffmpeg (slideshow + encode) + optional edge-tts voiceover (no API key).
#
# The QA Mastery short-form video STANDARD:
#   - 1080x1920, 30fps, H.264 + AAC, slides padded on brand black (#09090b)
#   - hook on slide 1, one idea per slide, CTA on the last slide
#   - burned text already lives in the slides (sound-off friendly)
#   - optional AI voiceover (edge-tts, en-US-AriaNeural) for retention
#
# Usage:
#   ./make-reel.sh --prefix bugreport --count 9 --out bug-report-reel.mp4
#   ./make-reel.sh --prefix bugreport --count 9 --out bug-report-reel.mp4 \
#       --vo "Seven fields every bug report needs. Title. Steps to reproduce. Expected. Actual. Severity. Environment. Evidence. Practice on a real buggy app and get graded."
#
# Slides are read from the platform public dir (already deployed/hosted there):
SLIDES_DIR="${SLIDES_DIR:-/Users/sajanathapa/Desktop/1/My Qa Projecct/qa-mastery/apps/platform/public/marketing}"
OUT_DIR="${OUT_DIR:-$SLIDES_DIR/video}"
BG="0x09090b"
PER=2.8        # seconds per slide (silent mode)
FIRST=3.2
LAST=4.0

PREFIX=""; COUNT=0; OUT="reel.mp4"; VO=""
while [ $# -gt 0 ]; do
  case "$1" in
    --prefix) PREFIX="$2"; shift 2;;
    --count)  COUNT="$2"; shift 2;;
    --out)    OUT="$2"; shift 2;;
    --vo)     VO="$2"; shift 2;;
    *) echo "unknown arg $1"; exit 1;;
  esac
done
[ -z "$PREFIX" ] && { echo "need --prefix"; exit 1; }
mkdir -p "$OUT_DIR"

VOFILE=""
if [ -n "$VO" ]; then
  VOFILE="$OUT_DIR/${PREFIX}-vo.mp3"
  echo "[vo] edge-tts -> $VOFILE"
  python3 -m edge_tts --voice en-US-AriaNeural --text "$VO" --write-media "$VOFILE"
  # spread slide time evenly across the voiceover length
  VODUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VOFILE")
  PER=$(python3 -c "print(max(1.5, ${VODUR}/${COUNT}))")
  FIRST=$PER; LAST=$PER
fi

LIST=$(mktemp)
for n in $(seq 1 "$COUNT"); do
  d=$PER; [ "$n" -eq 1 ] && d=$FIRST; [ "$n" -eq "$COUNT" ] && d=$LAST
  printf "file '%s/%s-%s.png'\nduration %s\n" "$SLIDES_DIR" "$PREFIX" "$n" "$d" >> "$LIST"
done
printf "file '%s/%s-%s.png'\n" "$SLIDES_DIR" "$PREFIX" "$COUNT" >> "$LIST"

VF="scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=${BG},setsar=1,format=yuv420p,fps=30"

if [ -n "$VOFILE" ]; then
  ffmpeg -y -f concat -safe 0 -i "$LIST" -i "$VOFILE" \
    -vf "$VF" -map 0:v -map 1:a -c:v libx264 -preset medium -crf 20 \
    -c:a aac -b:a 128k -shortest "$OUT_DIR/$OUT"
else
  ffmpeg -y -f concat -safe 0 -i "$LIST" -f lavfi -i anullsrc=r=44100:cl=stereo \
    -vf "$VF" -map 0:v -map 1:a -c:v libx264 -preset medium -crf 20 \
    -c:a aac -b:a 128k -shortest "$OUT_DIR/$OUT"
fi

echo "[done] $OUT_DIR/$OUT"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT_DIR/$OUT"
