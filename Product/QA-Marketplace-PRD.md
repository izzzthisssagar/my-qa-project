# QA Mastery Talent — Product Requirement Document

> A niche freelance & job marketplace for QA Engineers / Testers and the developers/companies who need testing done. Built as a module of QA Mastery.

**Status:** PRD v1.0 (locked for MVP planning) · **Surface:** web-first, inside `apps/platform` · **Launch model:** free both sides

---

## Context

QA Mastery is a live, Phase-1 learning platform (Next.js 16 App Router + React 19 + Supabase + Paddle, Turborepo monorepo on Vercel). This PRD adds a **two-sided marketplace module** where Clients/Developers post QA/testing work and QA Professionals showcase testing-specific portfolios and get hired.

**Key decisions (confirmed with founder):**
- **Integration:** A new module *inside* QA Mastery (`apps/platform`), reusing existing Supabase auth, accounts, Paddle billing, design system, and CI. The talent pool is **not** limited to QA Mastery graduates — **anyone with real, verifiable QA experience** can join. Graduates get a fast-track ("learn → certified → hired" funnel); external experienced testers join via an experience-verification path.
- **Monetization:** **Free at launch** (build two-sided liquidity first, matching the $0-organic / solo-founder constraint). Paid tiers / commission planned for V1.0, not gated in MVP.
- **Platform:** **Web-first**, responsive Next.js — same stack as the live app.

**Why now:** QA Mastery already produces job-ready testers and has the audience funnel (LinkedIn/Reddit). A marketplace closes the loop — turning learners into earners and giving the platform a second, defensible value prop ("the place QA careers happen") without rebuilding auth, billing, or UI.

---

## 0. Product summary

| | |
|---|---|
| **Name** | QA Mastery Talent (working title) |
| **One-liner** | The hiring layer for QA — testers showcase real testing portfolios (bug reports, automation scripts, device matrices); developers/companies find, vet, and contact the right tester. |
| **Surface** | Web-first, `/talent` routes inside `apps/platform` |
| **Two sides** | **Testers** (supply) · **Clients/Developers** (demand) |
| **Launch model** | Free for both sides; directory + profiles + projects + secure messaging |
| **North Star (marketplace)** | **Weekly Connected Pairs** = a client and tester who exchange ≥2 messages (real intent), not raw signups |
| **Differentiator** | QA-native profiles: testing-type taxonomy, device matrix, bug-report & automation-script artifacts, and platform-verified skills (graded labs from the learning side) |

---

## 1. Core user personas & tailored features

### 1A. Persona: "Priya" — the QA Tester (supply)

Two sub-types, **one profile model**, different trust signals:
- **Graduate** — came through QA Mastery learning; skills evidenced by graded labs.
- **Experienced pro** — joins directly; skills evidenced by verified work history + portfolio.

**Profile requirements (the QA-native bits are the moat):**

| Field group | Detail |
|---|---|
| **Identity** | Display name, headline, avatar, location/timezone, languages, availability (open / busy / not looking), hourly rate or "contact for rate" |
| **Testing skills (typed taxonomy, not free text)** | • **Discipline:** Manual, Automation, Both • **Specialties (multi-select):** Functional, Regression, Exploratory, API, Performance/Load, Security, Accessibility, Usability, Localization, Mobile, Web, Game, Embedded/IoT • **Automation stack:** Selenium, Playwright, Cypress, Appium, TestNG/JUnit, Postman/REST Assured, k6/JMeter, etc. • **Languages:** Java, JS/TS, Python, etc. |
| **Device & environment matrix** | Structured rows: real devices owned (e.g. *iPhone 13 / iOS 17*, *Samsung A54 / Android 13*), desktop OS/browsers, network conditions. **This is a top filter for clients** and rare on generic marketplaces. |
| **Portfolio artifacts** | First-class, QA-specific (see §3B): bug-report sheets, test plans/cases, automation script repos/snippets, coverage reports, before/after defect findings. |
| **Verified skills** | Auto-imported badges from the learning platform's graded labs (e.g. "API Testing — 94%"). Strongest trust signal; only graduates have these. |
| **Work history & verification** | Roles, durations, optional LinkedIn/GitHub links. Experience-verification path for non-graduates (§5). |
| **Reviews** | Client ratings post-engagement (V1.0). |

**Tester features:** create/edit profile, upload & organize portfolio items, set availability, browse/apply to projects, receive & reply to contact requests, get "verified" badges, share public profile URL (`/talent/u/[handle]`).

### 1B. Persona: "Devon" — the Client / Developer / Company (demand)

**Profile requirements:**

| Field group | Detail |
|---|---|
| **Identity** | Name / company, role, logo, website, location/timezone |
| **Project context (per posting)** | **Project type:** Web app / Mobile app / API / Game / Desktop / Embedded • **Codebase / tech stack:** React, Node, iOS/Swift, Android/Kotlin, etc. • **Required testing types:** (same taxonomy as tester specialties — enables matching) • **Engagement:** one-off project, ongoing, full-time role • **Bug-tracking / tooling used:** Jira, Linear, GitHub Issues, TestRail, etc. • **Budget / rate range** (optional) • **Timeline & NDA-required flag** |
| **Trust** | Verified email / domain; company verification badge (V1.0) |

**Client features:** post/edit/close a project, browse & filter testers, view portfolios, save/shortlist testers, initiate contact, manage applicants per project, leave reviews (V1.0).

### Tailored feature: **QA-native matching & filters**
Because both sides share one **testing-type taxonomy + device matrix + stack vocabulary**, search/filter is precise: *"Find a tester with a real iPhone 13 who does Playwright API automation, available now, ≤ $40/hr."* This precision is the product's reason to exist over Upwork/Fiverr.

---

## 2. App architecture & system design

### 2A. Tech stack (reuse the live stack — do **not** introduce new infra)

| Layer | Choice | Why / reuse |
|---|---|---|
| **Frontend** | Next.js 16 App Router, React 19, TypeScript, Tailwind 4, Motion | Same as `apps/platform`; ship in existing app |
| **Backend** | Next.js Server Actions + Route Handlers; Zod validation | Mirrors existing `feedback/actions.ts` + `zod` pattern |
| **Database** | Supabase Postgres + **RLS** + SQL migrations | Reuse `packages/db`, migration workflow, service-role triage pattern |
| **Auth** | Supabase Auth (`@supabase/ssr`) | Already live; one account, add a `role`/profile-type |
| **Realtime messaging** | **Supabase Realtime** (Postgres changes / broadcast) on a `messages` table | No new service; RLS-secured; fits "fast, real-time" requirement |
| **File/artifact storage** | **Supabase Storage** buckets (avatars, portfolio files, bug-report sheets) | RLS-scoped; signed URLs |
| **Payments (later)** | **Paddle** (already integrated) | For V1.0 paid tiers / featured listings |
| **Search/filter** | Postgres indexes + `tsvector` / trigram; GIN on array/`jsonb` skill columns | Scales fine to 6-figure rows before needing external search |
| **Hosting / CI** | Vercel + Turborepo + GitHub Actions | Unchanged |
| **Design system** | `packages/ui`; brand zinc `#09090b` / teal `#2dd4a7` / amber `#f5b948`; Bricolage Grotesque + Geist | Consistent with platform |

### 2B. Core entities & relationships

```
auth.users (Supabase)
  └── profiles (1:1)  role: tester | client | both
        ├── tester_profiles (1:1, if tester)
        │     ├── tester_skills        (taxonomy: discipline, specialties[], stack[])
        │     ├── tester_devices       (device matrix rows)
        │     ├── portfolio_items (1:N) type: bug_report | test_plan | automation | coverage | other
        │     │     └── portfolio_assets (Supabase Storage refs / links)
        │     └── verified_skills      (imported from learning-side graded labs)
        ├── client_profiles (1:1, if client)
        └── reviews (received)   ← V1.0

projects (posted by client)
  ├── owner_id → profiles
  ├── required_testing_types[], stack[], engagement, budget, tooling[], nda_required
  └── applications (1:N)  tester_id → profiles, status: applied|shortlisted|declined|hired

conversations  (client_id, tester_id, project_id?)  ← created on first contact
  └── messages (1:N)  sender_id, body, attachments[], read_at   ← Supabase Realtime

reviews (V1.0)   reviewer_id, subject_id, project_id, rating, body
saved_testers / shortlists   client_id → tester_id
reports (moderation)   reporter_id, target_type, target_id, reason
```

**Relationship notes**
- One `auth.users` → one `profiles`; a profile may be `tester`, `client`, or `both` (a graduate can also hire).
- `verified_skills` bridges the learning platform and the marketplace — the unique trust graph.
- `conversations` are the contact boundary: messaging only opens after an explicit contact/connection action (anti-spam + future paywall point).
- Every table ships with **RLS**: read-own / read-public-profile / write-own; service-role for moderation & triage (mirrors the existing feedback migration).

### 2C. Key non-functional requirements
- **Security:** RLS on every table; signed URLs for private artifacts; NDA-gated portfolio items hidden until access granted.
- **Performance:** directory list p95 < 300ms; indexed filters; paginated/virtualized lists.
- **Privacy:** testers control public vs. private profile fields; email never exposed (in-app messaging only).
- **Accessibility:** WCAG AA (fitting for a product that *sells* a11y testing).

---

## 3. Key workflows & user journeys

### 3A. Client posts a project & filters for the right tester
1. Client signs in → `/talent/post` → guided form (project type → stack → **required testing types** → engagement → budget → tooling → NDA flag).
2. Zod-validated Server Action inserts into `projects` (RLS: owner-only write). Project goes live in the directory.
3. Client opens **Find Testers** (`/talent/testers`) → filters by **specialty, automation stack, device matrix (real-device toggle), availability, rate, location/timezone, verified-skill badges**.
4. Results ranked: verified-skill match > specialty match > recent activity. Client opens profiles, **shortlists** promising testers.
5. Client either waits for applicants on the posted project or **initiates contact** with a shortlisted tester (§3C).

### 3B. Tester showcases an automation-script portfolio / bug-report sheet
1. Tester → `/talent/profile` → completes skills taxonomy + **device matrix**.
2. Tester → **Add portfolio item** → picks a **type**:
   - **Bug-report sheet:** structured template (title, severity, steps, expected/actual, environment, evidence screenshots) or upload an existing sheet (CSV/Sheets export → Supabase Storage).
   - **Automation script:** paste snippet (syntax-highlighted) or link a public GitHub repo; tag framework + language; optional short "what this proves" note.
   - **Coverage / test plan:** upload PDF/MD or link.
3. Graduates: **verified-skill badges** auto-appear from graded labs (read from the learning schema) — no extra work.
4. Tester sets availability → profile is public at `/talent/u/[handle]`, shareable on LinkedIn (feeds the existing $0-organic motion).

### 3C. Secure connection & messaging flow
1. Trigger: client clicks **Contact** on a profile, *or* tester **applies** to a project.
2. System creates a `conversations` row (client + tester [+ project]) — the explicit consent boundary.
3. **In-app messaging only** (Supabase Realtime): no emails/phone exposed; attachments via signed Storage URLs; typing/read receipts.
4. **Anti-bypass nudges** even in free phase: contact info masking in early messages, "keep it on-platform" microcopy (sets up V1.0 monetization).
5. After an engagement, both parties prompted to **review** (V1.0) — builds the reputation graph.

---

## 4. Phased development roadmap (MVP → V1.0)

### Phase 1 — MVP (must-have to launch, free)
**Goal: two-sided liquidity + the QA-native profile that can't be copied elsewhere.**

- **Auth/role:** extend `profiles` with role (`tester|client|both`) + onboarding chooser. *(reuse existing Supabase auth)*
- **Tester profile:** skills taxonomy, device matrix, availability, public profile page.
- **Portfolio:** the 3 core artifact types (bug-report sheet, automation script, test plan/coverage) + Storage upload.
- **Verified-skill import:** read graded-lab results → `verified_skills` badges (graduates).
- **Experience-verification path** for non-graduates (lightweight: LinkedIn/GitHub link + manual/queued review).
- **Client profile + project posting** with the typed fields.
- **Directory + filters** for testers and projects (the QA-native filters are the wow moment).
- **Contact + Realtime 1:1 messaging** with consent boundary + on-platform nudges.
- **Moderation basics:** report button, admin/service-role review queue, rate limits on signup/posting.
- **Schema & RLS migration** (one `..._talent.sql` migration; applied via Supabase, recorded in `schema_migrations`).

**Explicitly NOT in MVP:** payments/escrow, reviews/ratings, native mobile, AI matching, automated skill assessments, integrated issue tracking.

### Phase 2 — Post-MVP / scaling (V1.0)
- **Reviews & reputation** (ratings post-engagement) — the trust flywheel.
- **Monetization (Paddle):** featured tester/project listings, pro subscription (advanced filters / more active projects), and/or **commission via escrow** for managed engagements.
- **Escrow / milestone payments** (Paddle) — directly counters platform-bypass once there's money to protect.
- **Automated skill assessments:** spin up timed labs from the learning engine as on-demand, marketplace-graded tests → stronger verified badges.
- **Integrated issue tracking / handoff:** light bug-tracker or Jira/Linear/GitHub export so testers deliver inside the platform (raises switching cost, reduces bypass).
- **Smarter matching:** recommendations from skill/device/stack vectors + activity.
- **Native mobile** (React Native/Expo) reusing `packages/shared` + `db`.
- **Company verification & team accounts.**

---

## 5. Risk analysis & security

| Risk | Type | Mitigation |
|---|---|---|
| **Platform bypass** ("let's take it off-platform") | Business — existential for marketplaces | Free phase: contact-masking + on-platform nudges. V1.0: make on-platform *worth it* — escrow protection, reviews that only count on-platform, dispute support, integrated delivery/issue-tracking. Don't fight bypass with walls; out-value it. |
| **Spam / fake tester accounts** | Trust | Email/domain verification; **experience-verification gate** for non-graduates; rate limits on signup/posting (reuse existing patterns); report queue; verified-skill badges make real testers visibly outrank fakes. |
| **Low liquidity (cold-start, chicken-and-egg)** | Business | **Seed the supply side** from existing QA Mastery graduates (built-in advantage); manually concierge the first client matches; "you asked, we built it" + tester-spotlight content via the live $0-organic motion. |
| **Data privacy (PII, NDAs, client codebases)** | Security/legal | RLS on every table; in-app messaging only (no email/phone exposure); NDA-gated portfolio items hidden until granted; signed Storage URLs; never store client source — links/descriptions only. |
| **Quality / mis-hire** | Trust | Verified-skill badges, device-matrix transparency, real artifacts over claims; reviews in V1.0; clear specialty taxonomy reduces mismatch. |
| **Moderation load on a solo founder** | Ops | Service-role admin queue + report-driven (not proactive) moderation; automate triage like the existing `feedback_triage.py`; start invite-light. |
| **Scope creep diluting the learning product** | Product | Ship as a contained `/talent` module behind a flag; MVP scope is fixed above; reuse — don't fork — auth/billing/UI. |
| **Security of file uploads** | Security | Validate MIME/size, store in private buckets, signed URLs, no public listing of private artifacts, virus-scan hook in V1.0. |

---

## 6. Open questions / next step

This PRD is locked enough to plan the MVP build. The **next engagement** is an implementation plan for §4 Phase 1:
- the `..._talent.sql` migration (entities in §2B + RLS),
- `/talent` route tree and Server Actions,
- profile/portfolio/directory UI in `packages/ui`,
- Supabase Realtime messaging.

To decide before build: final module name, whether `/talent` launches behind a feature flag vs. soft-public, and the exact graded-lab fields to map into `verified_skills`.
