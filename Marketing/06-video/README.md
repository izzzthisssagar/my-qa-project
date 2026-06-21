# Video — short-form pipeline (TikTok / IG Reels / Shorts)

All-free, repeatable. Turns brand slides into a 9:16 reel and posts via Buffer.

## The standard
- **Format:** 1080×1920, 30fps, H.264 + AAC; slides padded on brand black `#09090b`.
- **Structure:** hook on slide 1 · one idea per slide · CTA on the last slide.
- **Captions:** baked into the slides (sound-off friendly — the TikTok default).
- **Voiceover (optional, free):** `edge-tts` (`en-US-AriaNeural`), no API key.
- **Brand:** zinc/teal/amber, Bebas + Roboto (same as the image designs).

## Pipeline (reuses the image pipeline)
```
HTML design slides → PNG (Playwright, /04-designs)  →  make-reel.sh (ffmpeg [+ edge-tts])
  →  apps/platform/public/marketing/video/*.mp4  →  commit + deploy (public URL)
  →  Buffer "Add to Queue" attachment=video  →  TikTok (reminder) + IG Reels (direct)
```

## Make a reel
```bash
# silent (slides carry the text)
./make-reel.sh --prefix bugreport --count 9 --out bug-report-reel.mp4

# with free AI voiceover
./make-reel.sh --prefix bugreport --count 9 --out bug-report-reel.mp4 \
  --vo "Seven fields every bug report needs. Title. Steps. Expected. Actual. Severity. Environment. Evidence. Practice on a real buggy app and get graded."
```
PNGs are rendered from the HTML designs via Playwright (see `../04-designs` + the
`shoot.cjs` approach used to make `launch.png`, `bugreport-*.png`, etc.).

## Posting (Buffer, via Zapier MCP)
- **TikTok:** `scheduling_type: "reminder"` (Notification publishing — free plan; Buffer pings the phone to tap-publish). Direct auto-publish needs a Buffer paid plan.
- **IG Reels:** `scheduling_type: "direct"`, `ig_post_type: "reels"`, `ig_share_to_feed: true`.
- **Always pass `image: ""`** on video posts (and `video: ""` on image posts) — the Buffer resolver otherwise auto-duplicates the media. See the marketing memory.
- MP4 must be on a public URL first (host in `public/marketing/video/`, deploy).

## Shipped with this pipeline
- `bug-report-reel.mp4` — 9-slide "7 fields" reel → queued to TikTok (`6a3744a1`) + IG Reel (`6a374478`).

## Optional upgrade (not built)
Remotion (`package.json` here) is installed for fully code-driven motion shorts
(animated scenes, word-synced captions). The ffmpeg-slideshow standard above is
simpler and already covers TikTok/Reels/Shorts; switch to Remotion when you want
real animation rather than slide transitions.
