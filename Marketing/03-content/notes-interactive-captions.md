# "Notes That Fight Back" — launch captions (NotesInteractive reel)

**Asset:** `06-video/out/notes-interactive.mp4` (1080×1920, ~52s, VO + captions
baked in — sound-off friendly).

> ⚠️ **The hosted copy is gone.** The 28 MB mp4 was removed from the platform's
> `public/` folder on 2026-07-10 — everything in `public/` is bundled into every
> Vercel build, and nothing in the app referenced it. It is preserved in git
> (`git show eb30574:apps/platform/public/marketing/video/notes-interactive.mp4 > notes-interactive.mp4`).
> **Every platform below takes a native upload anyway**, so this changes nothing
> about posting. If you ever need a URL, host it on Vercel Blob / S3 / YouTube —
> do not put it back in `public/`.

One reel, five platforms. Post in this order (native upload everywhere — never
paste a link to another platform's video).

---

## TikTok / IG Reels / YT Shorts (same caption)

Your course notes: a PDF you never opened again.
Our notes: you tap the hardware, play the diagrams, run real code, and get quizzed before you can scroll past. Then they pay you XP.

Notes that fight back → link in bio, first module free.

#QA #SoftwareTesting #LearnToCode #TechEducation #StudyTok #CareerSwitch #EdTech

**YT Shorts title:** Notes you tap, run and get quizzed by — QA Mastery
**Cover text (choose frame ~2s):** NOBODY READS NOTES.

---

## LinkedIn

**Hook (first line, before "…see more"):**
> Nobody reads course notes. So we made notes that fight back.

**Body:**
We rebuilt the humble "lesson notes" from zero, and this 50-second screen capture shows the result better than I can describe it:

- Tap any part of a real machine — it explains itself
- Diagrams have a Play button — watch the power actually flow
- There's a real compiler inside the note — edit, run, get output
- The note quizzes you back before you can scroll past
- Finish → XP → streak

The principle behind all of it: reading is watching. Recall + doing is learning. Every one of our 100+ note pages is built on this same interactive skeleton.

Would you have stayed in tech education longer if your notes worked like this? Genuinely asking.

**First comment:**
Try the notes yourself (first module free, no card): https://qa-mastery-platform.vercel.app

---

## X / Twitter

nobody reads course notes.

so we made notes you TAP, diagrams you PLAY, code that RUNS inside the page, and a quiz that catches you before you scroll past.

notes that fight back 👇
[native video]

first module free: qa-mastery-platform.vercel.app

---

## Community (Reddit r/QualityAssurance · Ministry of Testing) — value-first

Title: We rebuilt "course notes" as interactive pages — tap the hardware, run the code, get quizzed. What would you add?

Body: give the design reasoning (recall > recognition, doing > reading), embed/attach the video, invite critique. Soft CTA only in a reply if asked.

---

## Zapier: post everywhere from one row

**The wiring (one-time, ~15 min in zapier.com):**

1. **Trigger — Google Sheets: "New/updated row"** in sheet `Social Queue`
   with columns: `date · platform · video_url · caption · title · status`.
   (The sheet IS the content pipeline — `content-pipeline.csv` can be imported
   as a second tab to keep planning and posting in one place.)
2. **Filter:** only continue when `status = ready`.
3. **Paths by `platform`:**
   - `linkedin` → LinkedIn "Create Share Update" (caption; video via URL)
   - `x` → Twitter "Create Tweet with media"
   - `instagram` → Instagram for Business "Publish Reel" (needs IG Business +
     FB page link; takes `video_url` — this is why we host the mp4 on the
     platform's public URL)
   - `youtube` → YouTube "Upload Video" (Short: 9:16 + <60s is auto-detected)
   - `tiktok` → no direct Zapier upload; route to Buffer ("Add to Queue",
     attachment = video_url) which pushes a TikTok reminder to your phone
4. **Last step — update the row:** `status = posted` + timestamp (prevents
   double-fires).

**Free-tier note:** multi-step Zaps with Paths need the Starter plan; on the
free tier, make 5 single-step Zaps (one per platform) all watching the same
sheet, each with its own `platform` filter — same result, $0.

**Fill the sheet for this launch (one row per platform, same video_url):**

| date | platform | video_url | caption | status |
|---|---|---|---|---|
| [pick Wed] | linkedin | …/marketing/video/notes-interactive.mp4 | (LinkedIn body above) | ready |
| same day | x | 〃 | (X caption) | ready |
| same day | instagram | 〃 | (short caption) | ready |
| same day | youtube | 〃 | (title + caption) | ready |
| same day | tiktok | 〃 | (short caption) | ready |

Calendar note: this IS a "Differentiate"-pillar post — slot it as the Wednesday
proof post of whichever week you launch it, and shift that week's planned Wed
post one week right.
