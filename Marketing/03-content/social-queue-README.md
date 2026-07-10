# Social Queue — the one sheet that drives all posting

`social-queue.csv` is the single source of truth for what goes out, where, and
when. Fill a row, set `status = ready`, and (once Zapier is wired) it posts
itself. This file is the artifact the reel's Zapier blueprint
(`notes-interactive-captions.md`) refers to — it now exists.

## Columns

| Column | What it holds | Notes |
|---|---|---|
| `date` | Target post date (YYYY-MM-DD) | Zapier can post on this date or you post manually; it's the schedule. |
| `platform` | `linkedin` · `x` · `instagram` · `youtube` · `tiktok` | One row **per platform** — never one row fanned out. Each platform wants a native upload. |
| `asset` | Video/image filename, or blank for text-only | `notes-interactive.mp4` for the reel; blank for a text/carousel post. |
| `caption_ref` | Pointer to the caption, as `file.md#anchor` | Keeps captions in their own doc (versioned, reviewable) instead of trapped in a spreadsheet cell. Copy the caption from there at post time. |
| `title` | For YouTube (Shorts need a title) | Blank for platforms that don't use one. |
| `link` | The CTA/first-comment URL | LinkedIn/X put it in the first comment, not the body. |
| `status` | `draft` → `ready` → `posted` | Only `ready` rows fire. Flip to `posted` (with `posted_at`) after — prevents double-posting. |
| `posted_at` | Timestamp when it went out | Written by the last Zapier step, or by hand. |

## Status lifecycle

```
draft  ── caption finalized, asset ready ──▶  ready  ── posted (auto or manual) ──▶  posted
   ▲                                             │
   └──────────── needs another pass ─────────────┘
```

Only ever set `ready` when the `caption_ref` anchor actually resolves and the
`asset` (if any) exists. A `ready` row is a promise the post is complete.

## How it maps to Zapier (from the reel blueprint)

1. **Trigger** — Google Sheets *New or Updated Row* on this sheet (import the CSV
   as a Google Sheet first; keep the header row exactly).
2. **Filter** — continue only when `status` is `ready`.
3. **Paths by `platform`** — LinkedIn / X / Instagram / YouTube each get their own
   action; TikTok routes to Buffer (Zapier can't upload to TikTok directly).
4. **Last step** — update the row: `status = posted`, `posted_at = now`. This is
   what stops a row from firing twice.

**Free-tier:** Paths need Zapier Starter. On free, make 5 single-step Zaps (one per
platform) all watching this sheet, each filtered to its own `platform`. Same
result, $0.

## What's queued right now

- **2026-07-16 — the "Notes That Fight Back" reel**, five platforms, all `ready`.
  This is the launch. (Native upload everywhere; the mp4 lives at
  `06-video/out/notes-interactive.mp4` — recover from git if needed, see the
  captions doc's note; do **not** re-add it to the app's `public/` folder.)
- **Week 5 LinkedIn posts** — queued as `draft` (captions in `weeks-5-8-posts.md`);
  flip to `ready` when you're happy with them.

## Adding a post (the whole workflow)

1. Write/lock the caption in the relevant `*-posts.md` or captions doc under a `##`
   heading (that heading is your `caption_ref` anchor).
2. Add one row per platform to `social-queue.csv`, `status = draft`.
3. When it's truly ready, flip to `ready`. Zapier (or you) does the rest.

That's the loop: **caption in a doc → row in the queue → status ready → posted.**
One sheet, every channel, no forgotten drafts.
