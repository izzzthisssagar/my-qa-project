# QA Mastery Platform — Detailed Product & Execution Plan

**Working name:** QA Mastery (placeholder — decide later)
**Author:** Sagar | **Date:** June 11, 2026
**Decisions locked:** Web-first → Android later · V1 = Manual + Automation testing · **Java is the primary teaching language** (Selenium + Java + TestNG leads; Playwright/JS becomes a secondary path later) · Founder is QA-strong / dev-light (AI-assisted build)

---

## 1. Executive Summary

A web platform (Android app in a later phase) where aspiring testers learn QA **visually and practically** — not by watching videos, but by *doing*: writing test cases against a real practice application, running real automation scripts in the browser, filing real bug reports that get graded. The long-term arc takes a complete beginner to QA-lead readiness across manual, automation, API, performance, security, DB, CI/CD, and Git. V1 ships only Manual + Automation, done deeply.

**Core differentiator:** Every concept has (a) a visual explanation (interactive diagram/animation), (b) a hands-on lab on a built-in practice app, and (c) graded feedback. Competitors (Test Automation University, Udemy courses, Guru99, BrowserStack Academy) deliver passive content; almost none grade your actual work.

**The honest constraint:** You can't code much yourself. The plan therefore assumes AI-assisted development (Claude/Cowork building the app with you), managed infrastructure (no servers to run), and your time going mostly into **content and curriculum**, which is where your QA expertise is the real asset. Content is 70% of this product; code is 30%.

---

## 2. Problem & Positioning

### The gap
- New testers learn from scattered YouTube videos, blogs, and outdated Udemy courses. No structured path from zero → job-ready → lead.
- Existing content is passive. Watching someone use Selenium ≠ being able to use Selenium.
- "Practice sites" (the-internet, saucedemo) exist but are disconnected from any curriculum — no one tells you *what* to test or grades what you did.
- Nothing credible bridges senior tester → QA Lead (test strategy, estimation, team management, metrics, stakeholder communication).

### Positioning statement
> "The only QA learning platform where you don't watch testing — you do it. Learn every concept visually, practice it on a real app, and get graded like you would in a real job."

### Competitors (study these before building)
| Competitor | Strength | Weakness you exploit |
|---|---|---|
| Test Automation University (Applitools) | Free, credible instructors | Video-only, no hands-on grading, automation-only |
| Udemy QA courses | Cheap, huge catalog | Outdated, passive, no path, no practice env |
| Guru99 / Software Testing Help | Free articles, SEO giants | Text walls, zero interactivity, ad-ridden |
| BrowserStack/LambdaTest academies | Real tooling | Marketing funnels for their product |
| Codecademy/Exercism model | Interactive in-browser practice | Don't cover QA at all — this is the model to copy for QA |

**[Likely]** Your real competition is "free YouTube + ChatGPT." Your answer to that: structure, hands-on grading, a practice environment, and a credential — none of which YouTube provides.

---

## 3. Target Users (Personas)

**P1 — Career Switcher Sana (primary, v1):** 22–30, non-CS or fresh graduate, wants first QA job. Needs zero-assumption explanations, visual learning, a portfolio to show employers. Will pay if she believes it leads to a job.

**P2 — Manual Tester Manish (primary, v1):** 1–3 yrs manual testing, stuck; needs automation to grow salary. Knows SDLC already; wants to skip basics and go straight to Selenium/Playwright + Git + CI. Highest willingness to pay.

**P3 — Future Lead Priya (later phase):** 4–8 yrs experience, targeting lead roles at product companies. Needs test strategy, metrics, interviews, people skills. Served in Phase 4 — don't build for her yet, but design the brand so she isn't excluded.

---

## 4. Product Strategy — Phased Roadmap

### Phase 0 — Validate before building (Weeks 1–4)
- Write the full curriculum outline (this doc's Section 5 is the start).
- Create 3 sample lessons (1 visual concept, 1 manual lab, 1 automation lab) as simple web pages.
- Share in QA communities (LinkedIn, Reddit r/QualityAssurance, r/softwaretesting, Ministry of Testing, Telegram/Discord QA groups). Goal: 100 email signups for "early access."
- **Kill/continue gate:** If <50 people care after 4 weeks of honest promotion, rework the angle before spending months building.

### Phase 1 — Web MVP: Manual + Automation (Months 2–6)
> **✅ Built — June 2026.** Code-complete and green; publishing is now a config
> step (Vercel + Supabase). The platform lives in `qa-mastery/` (its own repo);
> a full plan-vs-shipped report is in [`PHASE-1-REPORT.md`](./PHASE-1-REPORT.md).

Ship a responsive web app with:
1. **Two complete tracks** (Section 5): Manual Testing (Foundation) and Automation Testing (Selenium + Playwright basics).
2. **The Practice App** ("BuggyShop") — a deliberately flawed e-commerce demo app embedded in the platform. Every lab targets it. It has seeded bugs with known IDs so submissions can be auto-graded.
3. **Lesson engine:** concept page (visual/interactive) → guided demo → lab task → quiz → graded submission.
4. Progress tracking, streaks, completion certificates (non-accredited, honest about it).
5. Free tier (first module of each track) + paid tier.

### Phase 2 — Depth + breadth (Months 7–12)
- Add tracks: API testing (Postman/REST), Git & GitHub for testers, SQL/DB testing, CI/CD basics (GitHub Actions running learners' actual test repos).
- Add portfolio feature: learner's graded projects become a shareable public page (their job-application asset).
- Community: discussion per lesson, peer review of bug reports.

### Phase 3 — Android app (Months 12–18)
- Wrap or rebuild with a cross-platform approach (Capacitor wrap of the web app first — cheapest; React Native/Flutter only if the wrap underperforms).
- Mobile is for **consuming** lessons, quizzes, flashcards, interview prep. Labs (real IDE/browser automation) stay web-only — be honest in the app about this. This split is standard (DataCamp/Codecademy do the same).

### Phase 4 — QA Lead track + careers layer (Months 18+)
- Security testing (OWASP basics), performance (JMeter/k6), test strategy & planning, metrics, estimation, leadership/communication, mock interviews, resume review.
- Mentor marketplace or cohort-based "Lead Bootcamp" (highest revenue per user).

---

## 5. V1 Curriculum (Detailed)

### Track A — Manual Testing Foundation (~40 hours of learner effort)

**Module A1: How Software Is Built (and Breaks)**
- SDLC & STLC visualized as an interactive pipeline diagram; where QA sits in Agile/Scrum.
- What is a bug — cost of bugs (interactive: "find the cheapest place to catch this bug").
- Lab: explore BuggyShop, write your first 3 observations.

**Module A2: Testing Fundamentals**
- Verification vs validation, levels (unit/integration/system/UAT), types (functional/non-functional), black/white/grey box — each as a visual card with a 60-second interactive example.
- 7 testing principles with live demos (e.g., pesticide paradox shown by re-running the same tests on BuggyShop while a new bug ships).

**Module A3: Test Design Techniques (the heart of manual QA)**
- Equivalence partitioning, boundary value analysis, decision tables, state transition, error guessing — each taught with an interactive widget (e.g., a BVA slider on a real input field).
- Lab series: design test cases for BuggyShop's signup, cart, checkout. Auto-checked against expected coverage.

**Module A4: Test Cases, Bug Reports & Tools**
- Writing test cases that don't embarrass you; test data; priority vs severity (interactive triage game).
- Bug report anatomy; reproducing intermittent bugs; evidence (screenshots/video/logs).
- Tools: intro to Jira & TestRail-style workflows (simulated in-platform).
- Lab: find 10 of the 25 seeded bugs in BuggyShop checkout, file reports; graded on reproducibility, clarity, severity accuracy.

**Module A5: Real-World Manual QA**
- Exploratory testing & session-based test management; regression vs retest; smoke/sanity; UAT; cross-browser/responsive basics.
- Capstone: full test cycle on a new BuggyShop release — plan, design, execute, report, summary email to a fake PM. Manually-rubric-graded (by you at first; AI-assisted grading later).

### Track B — Automation Foundation (~60 hours)

**Module B0: Just Enough Java (expanded — Java is the primary language)**
- Variables, types, loops, methods, classes/objects, collections, exceptions — the OOP subset automation actually uses. Maps directly to your existing "PHASE 1 — JAVA ESSENTIALS" notes.
- Exercises run against a server-side code runner (judge0-style), since Java doesn't run in-browser. Budget B0 at ~12–15 hours of learner effort — Java's beginner curve is steeper than JS, and rushing it is where most Selenium courses lose people.

**Module B1: How Automation Actually Works**
- DOM visualized interactively (click an element on BuggyShop → see its HTML highlight). Locators: CSS & XPath taught as a game ("hit the target element in fewest characters").
- What Selenium/Playwright do under the hood (animated diagram of driver ↔ browser protocol).

**Module B2: Selenium WebDriver Core (Java)**
- Setup (Maven, ChromeDriver), locators, actions, assertions, waits (the #1 beginner killer — taught with a visual race-condition simulator), handling alerts/frames/windows.
- Every lesson: write the test in the embedded editor, the runner executes it against BuggyShop server-side, learner gets pass/fail + screenshots/logs back.

**Module B3: TestNG + Framework Structure**
- TestNG annotations, suites, assertions, data providers; Maven project layout; Page Object Model done right.

**Module B4: Good Practices & Capstone**
- Data-driven tests, ExtentReports/Allure reporting, Log4j2 basics, flaky-test debugging.
- Capstone: build a 15-test Selenium+TestNG suite for BuggyShop from a requirements doc; graded on coverage, stability, structure.
- *(Playwright/JS offered later as a secondary "modern stack" mini-track in Phase 2 — demand for it is growing, but it's an add-on, not the spine.)*

**Module B5: Git + GitHub for Testers (bridge module)**
- Clone, branch, commit, PR, review — done on real GitHub with a template repo. This seeds the Phase 2 CI/CD track.

**Interview Prep mini-track (both personas want this):** 200+ real interview Q&A, scenario questions, flashcards. Cheap to produce, high perceived value, great free-tier hook.

---

## 6. Learning Experience Design ("visual + practical" made concrete)

Every lesson follows one repeatable pattern — build the engine once, reuse forever:

1. **See it** — interactive visual (animated diagram, clickable simulation). Not a video by default; videos are expensive to update and passive. Short screencasts only where motion genuinely helps.
2. **Try it (guided)** — a sandboxed walkthrough with hints on BuggyShop or the embedded code runner.
3. **Do it (lab)** — an ungated task with auto-grading (seeded bugs, expected test coverage, passing test runs).
4. **Prove it** — quiz + spaced-repetition flashcards feeding a review queue.
5. **Show it** — graded artifacts (bug reports, test suites) accumulate in a public portfolio page.

**The Practice App (BuggyShop) is the moat.** Spec it carefully:
- E-commerce demo: signup/login, product list/search, cart, checkout, orders, profile.
- ~25 seeded, versioned bugs per "release," each with a hidden ID, category, severity, and repro path → enables auto-grading of bug hunts.
- Multiple "releases" so regression testing can be taught honestly.
- Stable selectors + an intentionally messy area (to teach locator strategy on bad DOMs).
- Same app used by manual and automation tracks — learners feel continuity.

**Gamification (light, not childish):** XP, streaks, module badges, a "bugs found" counter. No leaderboards in v1 — small user base makes them demotivating.

---

## 7. Technical Plan (built for a dev-light founder)

### Recommended stack
| Layer | Choice | Why |
|---|---|---|
| Web app | **Next.js (React) + Tailwind** | Largest ecosystem, best AI-assistance support, one framework for site + app |
| Backend/DB/Auth | **Supabase** (Postgres, auth, storage) | Managed, generous free tier, no server ops; you already have Supabase MCP access |
| Payments | Merchant-of-record (Paddle / Lemon Squeezy) | One integration serves India + global with localized pricing; provider handles GST/VAT. Verify India support at build time |
| Code-runner for labs | **Server-side Java runner from day one** (judge0 self-hosted or hosted API; Selenium jobs run headless in a containerized runner) | Java can't execute in-browser — this is the project's one real piece of infrastructure. Fallback if it stalls: "run locally in IntelliJ, submit repo + report" with auto-checks on the repo |
| BuggyShop | Separate small Next.js app, versioned releases, bug manifest JSON for grading | Isolated from main platform |
| Interactive visuals | React components (custom) + Excalidraw/Mermaid-style diagrams | Reusable lesson widgets |
| Hosting | Vercel + Supabase cloud | Push-to-deploy, no DevOps |
| Android (Phase 3) | **Capacitor wrap** of the web app first | 90% cheaper than native; revisit only if reviews complain |
| Analytics | PostHog (free tier) | Funnel + lesson drop-off tracking |

### Build approach
- You + AI pair-build (Claude/Cowork writes the code, you act as the QA — which you're actually qualified to do; *your platform becomes its own test subject*).
- Hard rule: **no custom feature that a managed service already provides** (auth, payments, email, video hosting).
- Realistic v1 engineering scope: lesson engine, ~10 reusable interactive widget types, BuggyShop, grading service, auth/payments, progress tracking. That is genuinely buildable AI-assisted in 3–4 months part-time; the curriculum content will take you longer than the code.

### Data model (core tables)
`users`, `tracks`, `modules`, `lessons`, `lesson_blocks` (concept/widget/lab/quiz), `lab_submissions` (+ score, feedback), `quiz_attempts`, `progress`, `subscriptions`, `bug_manifest` (BuggyShop seeded bugs), `portfolio_items`.

---

## 8. Content Production Pipeline (your main job)

- **Write order:** outline → scripts for all of Track A → build A-widgets → Track A labs → Track B. Content before polish.
- **Per-lesson budget:** concept script (you, 2–3 h) → widget spec (you + AI, 1 h) → widget build (AI-assisted, 2–4 h) → lab + grading rules (2 h) → quiz (30 min). ≈ 1 lesson/day part-time; ~70 lessons in v1 → **~4 months of content work running parallel to the build.**
- Use AI to draft, but every lesson must pass your expert review — your credibility is the product. Wrong content in a QA course is fatal irony.
- Maintain a content versioning habit from day one (tools change: Playwright releases monthly).

---

## 9. Monetization

- **Free tier:** Module A1 + B0/B1 + interview flashcards (the hook; also your SEO/social funnel).
- **Pro subscription:** everything + grading + certificate + portfolio. **Geography decision (locked June 12, 2026): both markets from day one, implemented via a merchant-of-record provider** (Paddle / Lemon Squeezy — verify current India support during build week) — one integration, localized pricing (**₹999–1,499/mo or ₹6,999–9,999/yr** in India; **~$15/mo / ~$99/yr** elsewhere), tax compliance handled by the provider. Hard rule: no dual payment-rail builds (Razorpay + Stripe separately) in v1.
- **Later:** cohort-based Lead Bootcamp (Phase 4, premium ₹25–50k), B2B team licenses for service companies training freshers (real money in India's IT-services market), placement partnerships.
- **Do NOT promise jobs.** Promise skills + portfolio + interview readiness. Job guarantees create legal and reputational debt.

---

## 10. Go-to-Market

1. **Build in public** from week 1: post BuggyShop bug-hunt challenges on LinkedIn ("Can you find the bug in this checkout?") — these are inherently shareable and demonstrate the product.
2. **SEO:** free interactive widgets as standalone pages (e.g., "Interactive BVA calculator," "XPath practice game") — link magnets Guru99 can't match.
3. **Communities:** Ministry of Testing, Reddit, Discord/Telegram QA groups, college tie-ups for P1 learners.
4. **YouTube shorts/reels:** 60-second visual concept clips cut from your widgets, funneling to free tier.
5. Launch milestones: 100 waitlist (Phase 0) → 500 free users (Month 7) → first 50 paying (Month 8–9).

---

## 11. Costs (cash, not time)

| Item | Monthly est. |
|---|---|
| Vercel + Supabase + PostHog | $0–45 (free tiers initially) |
| Domain, email | ~$5 |
| Claude/AI tooling | $20–100 |
| Stripe/Razorpay fees | % of revenue |
| Optional: designer for brand + widget polish (one-time) | $300–800 |
| **Total burn before revenue** | **< $150/mo** |

The real cost is your time: realistically 20–25 h/week for 6 months to reach Phase 1 launch.

---

## 12. Success Metrics

- **Phase 0:** 100 waitlist signups; >40% open rate on update emails.
- **Phase 1:** activation = % of signups completing 3 lessons (target 40%); week-4 retention (target 25%); free→paid conversion (target 3–5%); lesson drop-off heatmap (find and fix the worst lesson monthly).
- **North star:** number of learners who complete a capstone (skin-in-the-game proxy for "this actually teaches").

---

## 13. Risks & Mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Scope creep back to "teach everything" | High — it's already in your head | This document. Phase gates. Nothing outside Phase 1 until capstone completions exist. |
| Content takes 3× longer than code | High | Start content in week 1, parallel to build; ship Track A before B is finished. |
| Java code-runner/labs too hard to build | **High (raised — Java needs server-side execution)** | Fallback ladder: hosted judge0 API → "run locally in IntelliJ, submit GitHub repo + Allure report" with automated repo checks → manual review. Labs degrade gracefully, never block launch. |
| Nobody pays (free alternatives) | Medium | Phase 0 validation gate; portfolio + grading are the paid value, keep them paid. |
| Solo-founder burnout | Medium | Phase gates double as stop/continue decisions; build-in-public creates accountability. |
| Tool churn (Playwright/Selenium updates) | Certain over time | Version-pin labs; quarterly content review; teach concepts > syntax. |

---

## 14. Next 30 Days (concrete)

- **Week 1:** Name + domain. Write full Track A outline to lesson level. Open LinkedIn build-in-public thread.
- **Week 2:** Spec BuggyShop (pages + 25 seeded bugs with manifest). Draft 3 sample lessons.
- **Week 3:** Build the 3 sample lessons as a simple landing site (AI-assisted) with waitlist email capture.
- **Week 4:** Promote in 5 communities; collect feedback + signups. Evaluate kill/continue gate.
- **Decision point:** ≥50–100 genuine signups → green-light Phase 1 build (and I can start building the platform with you in the next session).

---

*End of plan. Java confirmed as primary language (decision locked June 11, 2026). Sections most likely to change after Phase 0 feedback: pricing (§9) and lab grading depth (§6).*
