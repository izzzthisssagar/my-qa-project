# Week 4 — Promotion Kit

**Goal:** 50–100 genuine waitlist signups in ~2 weeks. Below: ready-to-paste posts. Replace `https://verdant-chebakia-94a514.netlify.app` with your Netlify URL everywhere before posting.

**Posting rule that matters more than the copy:** in every community, lead with the *challenge*, not the product. "Can you find the bug?" gets engagement; "check out my course" gets ignored or removed as self-promo.

---

## 1. LinkedIn — launch post (your main channel)

> **Can you find the bug? 🐞**
>
> I built a signup form with 3 real bugs hidden in it — the same bugs that ship to production every day.
>
> One hides in the email field. One in the password pair. One in how the form submits.
>
> Most people find 0. Testers find 1–2. Good testers find all 3.
>
> Try it (no signup, 2 minutes): https://verdant-chebakia-94a514.netlify.app
>
> Why I built this: I'm creating an interactive QA learning platform — where you don't *watch* testing, you *do* it. Real bug hunts, graded bug reports, Selenium + Java you run in the browser. This page is the first tiny piece.
>
> If you find all 3, comment "3/3" — and tell me how long it took. 👇

**Follow-up posts (every 2–3 days, rotate):**
- Boundary Hunter angle: "A quantity field accepts 1–99. Where's the bug? Hint: it's not in the middle." + 45-sec screen recording of the slider.
- Stats post after ~1 week: "X people tried the bug hunt. Y found the email bug, only Z found the double-click bug. Here's what that says about how we test forms…"
- Story post: why you're building this (manual tester → automation → teaching). People follow people, not products.

## 2. Reddit — r/QualityAssurance & r/softwaretesting

**Title:** I made a free "find the bug" challenge — a signup form with 3 seeded bugs. How many can you find?

> Hey all — I'm a QA learning automation, and I'm building an interactive way to practice testing. As a first experiment I put up a page with two free exercises:
>
> 1. A boundary-value slider on a quantity field (find the off-by-one)
> 2. A signup form with 3 hidden bugs (validation, paste handling, race condition)
>
> No signup needed to play: https://verdant-chebakia-94a514.netlify.app
>
> Honest ask: I want to know if this "learn by hunting bugs" format is actually useful, or if videos/blogs already cover it. Brutal feedback welcome — especially from folks who interview junior testers.

**Reddit rules:** read each sub's self-promo policy first; post as discussion, reply to every comment, never argue. If a mod removes it, message them politely asking what format is acceptable.

## 3. Ministry of Testing (The Club forum) / QA Discord & Telegram groups

> Built a small free interactive bug-hunt exercise (boundary analysis + a 3-bug signup form) as a pilot for a hands-on QA learning platform. Would love feedback from experienced testers on whether the seeded bugs feel realistic: https://verdant-chebakia-94a514.netlify.app

Framing for pro communities = "review my seeded bugs," not "learn from me." Senior testers will critique it — that critique is free expert content review.

## 4. WhatsApp/Telegram (personal network, India QA groups)

> 🐞 Quick challenge: this signup form has 3 hidden bugs. Most people find 0. Can you find all 3? Takes 2 min, no signup: https://verdant-chebakia-94a514.netlify.app

## 5. Posting schedule (2 weeks)

| Day | Action |
|---|---|
| 1 | LinkedIn launch post + personal WhatsApp/Telegram groups |
| 2 | r/QualityAssurance |
| 3 | Reply to every comment everywhere (this is half the work) |
| 4 | r/softwaretesting + Ministry of Testing |
| 5–6 | LinkedIn follow-up #1 (Boundary Hunter clip) |
| 8 | QA Discords/Telegram communities |
| 9–10 | LinkedIn stats post (real numbers from the hunt) |
| 12 | LinkedIn story post (why I'm building this) |
| 14 | Count signups → kill/continue decision |

## 6. Measure (write numbers down daily)

- Visitors (Netlify Analytics or PostHog)
- % who interacted with a widget
- Waitlist signups (Formspree dashboard)
- Comments saying "I'd pay for this" / "where's the full course" (strongest signal of all)

**Gate (from the plan):** ≥50 genuine signups → green-light Phase 1 build. 20–50 → fix the pitch, retry 2 weeks. <20 after honest effort → rework the concept before building anything.

## 7. Pre-flight checklist (before Day 1)

- [ ] Formspree ID replaced in index.html (test with your own email)
- [ ] Site deployed, live URL works on your phone
- [ ] You personally passed the README testing checklist
- [ ] Analytics snippet added
- [ ] `https://verdant-chebakia-94a514.netlify.app` replaced in every post above
