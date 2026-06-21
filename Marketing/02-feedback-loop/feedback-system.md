# Feedback & Review Loop — The Heart of "Build What Users Want"

This is the system that makes the product become what users actually want. Three intake channels → one master list → scored → ranked → shipped → told back to users.

```
  IN-APP FORM ─┐
  (Supabase)   │
               │
  EXTERNAL  ───┼──►  MASTER LIST  ──►  RICE SCORE  ──►  RANKED BACKLOG  ──►  SHIP  ──►  "YOU ASKED, WE BUILT IT"
  FORM (Tally) │     (feedback-       (rice-scoring     (public roadmap)              (close the loop publicly)
               │      intake.csv)      .md)
  COMMUNITY ───┘
  + DMs (manual)
```

The loop only works if the **last step happens**. Collecting feedback and never telling users you acted on it kills trust. Always close the loop.

---

## The three intake channels (you chose all)

### 1. In-app form → Supabase (best data)
A "Feedback" button inside the platform. Captures the user, what they were doing, and their request — automatically tied to real usage data. See [`supabase-feedback-schema.sql`](./supabase-feedback-schema.sql).
- **Pro:** highest quality — you know who, when, where in the app.
- **Use for:** bug reports, feature requests from active users, lab-specific friction.

### 2. External form (Tally / Google Form) → zero dev, instant
A public link you drop in posts, bios, and community comments. See [`forms/feedback-form-spec.md`](./forms/feedback-form-spec.md).
- **Pro:** works for non-signups, prospects, anyone. No login wall.
- **Use for:** "what's stopping you from signing up?", early-access interest, cold feedback.

### 3. Community + DMs → manual capture
Comments on Reddit/LinkedIn, Discord messages, DMs. You read them and paste into the master CSV.
- **Pro:** richest *unprompted* signal — people complaining/praising in the wild.
- **Use for:** spotting themes, quotes for testimonials, competitor gaps.

---

## The master list

Everything lands in [`feedback-intake.csv`](./feedback-intake.csv) — one row per item, regardless of channel. Columns are designed to feed the [automation triage script](../05-automation/automation-overview.md) directly.

Columns: `id, date, source, user_segment, type, raw_text, theme, reach, impact, confidence, effort, status`

- **source:** in_app | tally | reddit | linkedin | discord | dm | email
- **type:** bug | feature | ux | content | pricing | praise
- **theme:** the grouped problem (e.g., "lab grading too strict", "want API track"). 3+ items sharing a theme = a pattern worth acting on.
- **status:** new → triaged → planned → shipped → announced

---

## Scoring & ranking

Don't build by loudest voice. Score every feature/UX/content request with **RICE** — see [`rice-scoring.md`](./rice-scoring.md). The [`feedback_triage.py`](../05-automation/scripts/feedback_triage.py) script reads the CSV and prints the ranked backlog automatically.

Bugs skip RICE — they go straight to a severity triage (Critical/High/Med/Low) and Critical/High get fixed before any feature work.

---

## The weekly ritual (15 min, every Friday)

1. Paste the week's community/DM feedback into `feedback-intake.csv`.
2. Export in-app + Tally submissions, append to the CSV.
3. Run `python feedback_triage.py feedback-intake.csv` → ranked backlog.
4. Group by `theme`. Any theme with 3+ items = strong signal.
5. Pick **one** thing to ship next week (small enough to actually ship).
6. Mark it `planned` in the CSV and add it to the public roadmap.

## The monthly ritual

- Move shipped items to `announced` and write one "You asked, we built it" post.
- Review themes: what do users keep asking for that you keep deprioritizing? Maybe they're right.
- Update the public roadmap so users *see* their influence.

---

## Closing the loop (do not skip)

For every shipped request:
1. Reply to the original person ("you asked for X — it's live").
2. Post publicly: "You asked, we built it: X." (Best-performing post type — see [content calendar](../03-content/content-calendar.md).)
3. Mark `announced` in the CSV.

This is the entire marketing flywheel: **users feel heard → they tell others → more users → more feedback → better product.**
