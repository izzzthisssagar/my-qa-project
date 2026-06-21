# QA Mastery — Marketing

Everything for getting testers into QA Mastery, listening to them, and shipping what they want — so the product becomes what users actually need.

**Operating context:** live app · $0 organic · solo founder · global audience.
**North Star:** Weekly Activated Learners (signup + ≥1 graded lab).

---

## The one loop everything serves

```
 GET PEOPLE IN  →  THEY USE IT  →  THEY GIVE FEEDBACK  →  WE RANK IT  →  WE SHIP IT  →  WE TELL THEM
 (01 action plan    (the product)    (02 feedback loop)    (RICE)         (product)      ("you asked,
  + 03 content)                                                                            we built it")
                                          ▲                                                     │
                                          └─────────────────────────────────────────────────────┘
                                            users feel heard → tell others → more users in
```

## Folder map

| Folder | What's inside | Start here |
|---|---|---|
| `01-action-plan/` | 30/60/90-day plan, per-channel playbook, weekly metrics tracker | [`30-60-90-plan.md`](./01-action-plan/30-60-90-plan.md) |
| `02-feedback-loop/` | 3-channel feedback intake, RICE scoring, master CSV, Supabase schema, form spec | [`feedback-system.md`](./02-feedback-loop/feedback-system.md) |
| `03-content/` | 12-week calendar, post templates, reusable CMS workflow, design briefs | [`content-calendar.md`](./03-content/content-calendar.md) |
| `04-designs/` | HTML marketing visuals (launch post, "you asked we built it" template) → Express/Canva | [`README.md`](./04-designs/README.md) |
| `05-automation/` | Reusable Python tools: feedback triage, content scheduler, review aggregator | [`automation-overview.md`](./05-automation/automation-overview.md) |
| `QA Mastery Marketing Strategy.docx` | Original high-level GTM/growth essay (positioning, GEO, tax) — reference | — |

## Weekly operating rhythm

| Day | Do | Tool/file |
|---|---|---|
| **Mon** | Plan week, draft 3 posts | `content-calendar.md` + `content_scheduler.py --week` |
| **Tue–Fri** | 1 post/day, reply to comments, answer 2–3 community Qs | `post-templates.md` |
| **Daily** | "What to post today" | `content_scheduler.py --today <date>` |
| **Fri** | Fold in feedback → re-rank → pick 1 to ship | `review_aggregator.py` → `feedback_triage.py` |
| **Sun** | Update metrics, mark winners | `targets-and-metrics.md` |
| **Monthly** | "You asked, we built it" posts, update public roadmap | `04-designs/asset-3-you-asked.html` |

## First 7 days (do this now)
1. Set up the 3 feedback channels (in-app form, Tally form, community sheet) — [`02-feedback-loop`](./02-feedback-loop/feedback-system.md).
2. Post the launch design (exported to Adobe Express) + "we're live" post.
3. Start daily community presence (build karma, answer first).
4. Log every signup source in [`targets-and-metrics.md`](./01-action-plan/targets-and-metrics.md).
5. Friday: run the triage script, pick the #1 small thing to ship.

## Reusable for other projects
The whole system is project-agnostic. Copy this folder, swap `05-automation/config/project.example.yaml`, start fresh CSVs with the same headers, and the scripts run for any project. See [`content-management-system.md`](./03-content/content-management-system.md).

## Open items / decisions for you
- **Brand colors** ✅ now match the live app tokens (`globals.css`): zinc `#09090b`, teal accent `#2dd4a7`, amber "bug" `#f5b948`. All 5 designs rebuilt + re-exported.
- **Domain** ✅ set to the live platform URL `qa-mastery-platform.vercel.app` everywhere. Swap in a custom domain later (one find/replace) if you buy one.
- **Designs** currently exported to Adobe Express (editable + PNG/PDF export). Say the word if you want them pushed to Canva instead.
- **In-app feedback** ✅ live in the real app (`qa-mastery/apps/platform`) → Supabase `feedback` table → `export_supabase_feedback.py` → triage. Apply the migration (`supabase db push`) and set GitHub secrets to turn on the weekly auto-triage.
