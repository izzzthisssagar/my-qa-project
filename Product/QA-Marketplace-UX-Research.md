# QA Mastery Talent — UX Research & Design Pack

> Companion to `QA-Marketplace-PRD.md`. Proto-personas, journey maps, a usability-test plan, and a validation research plan for the QA freelance/job marketplace module.

**Status:** v0.1 — **PROVISIONAL / assumption-based** · **Owner:** founder (solo) · **Confidence:** Low (exploratory)

---

## ⚠️ Methodology note — read first

This module is **pre-launch**: there are no analytics, surveys, support tickets, or user interviews *for the marketplace itself* yet. Per the persona methodology (`persona-methodology.md`), artifacts built without data are **assumption-based and therefore not yet valid** — they sit on the left of the validity spectrum.

So everything here is deliberately framed as **proto-personas and hypothesis journey maps**: a starting set of testable assumptions, *not* findings. Each persona states its **confidence = Low** and lists **"what would confirm / refute"** it. Section 4 is the **research plan that turns these into data-backed (Medium→High) artifacts** — and it's the most important part to act on.

What we *can* lean on honestly:
- The founder is QA-domain-expert (the supply side is well-understood from the inside).
- QA Mastery already has a learner audience + a feedback loop (3 channels) — the fastest recruitment pool.
- No fabricated numbers. Where a score needs data we mark it **[needs data]**; where it's a design-judgment estimate we mark it **[est.]**.

---

## 1. Proto-personas

Two primary personas (the two sides of the marketplace) + one secondary. All **Low confidence** until §4 runs.

### 1A. Priya — The QA Tester (supply) · PRIMARY

> *"I can do the work — I just need somewhere my real testing proof outranks a flashy résumé."*

| | |
|---|---|
| **Archetype** | Specialist professional / portfolio-builder (maps loosely to "power_user" — frequent, depth-seeking) |
| **Sub-types** | (a) **Graduate** — came through QA Mastery, has verified-skill badges; (b) **Experienced pro** — joins directly, has work history |
| **Demographics [est.]** | 22–35, global (India / Nepal / SEA / LatAm / EE over-indexed for freelance QA), graduate or self-taught, tech proficiency 6–9/10 |
| **Context** | Job-seeking or freelancing alongside a role; works evenings/weekends across timezones; web on desktop, checks messages on mobile |

**Goals**
- Get *contacted* by real clients without paying to apply or fighting 100-bid races (the Upwork pain).
- Show **proof of skill** — bug-report sheets, automation scripts, device matrix — not just claims.
- Convert a QA Mastery learning streak into actual paid work / a job.

**Frustrations (hypotheses to validate)** — *[needs data on frequency]*
- "On generic marketplaces my testing skills look identical to everyone else's — no way to stand out." [est. High severity]
- "Clients don't understand QA, so they filter on the wrong things (or just price)."
- "I own real devices (iPhone 13, Pixel 7) but nowhere shows it as an asset."

**Behaviors [est.]** — checks for new projects daily when actively looking; spends real effort on a profile *if* it visibly pays off; will abandon a long onboarding.

**Design implications**
→ Make the **portfolio artifact** (bug report / automation script) the hero of the profile, above the fold.
→ Surface **verified-skill badges** and **device matrix** as first-class, filterable signals.
→ Keep profile creation incremental — usable after 5 minutes, richer over time.
→ Notify fast on inbound contact (the dopamine that drives return visits).

**What would CONFIRM this persona:** ≥40% of surveyed testers rank "proof of skill / standing out" above "more job volume"; portfolio-completion correlates with contact rate.
**What would REFUTE it:** testers mostly want *volume* and treat profiles as throwaway → re-think toward application/bidding model.

---

### 1B. Devon — The Client / Developer / Founder (demand) · PRIMARY

> *"I ship features faster than I can test them. I need someone who'll actually find the bugs my users will."*

| | |
|---|---|
| **Archetype** | Time-poor builder / hiring manager (maps to "business_user" — outcome & ROI focused) |
| **Demographics [est.]** | 25–45, indie dev / startup founder / small-team eng lead, global, high tech proficiency, low QA-process proficiency |
| **Context** | Posts work in short bursts under deadline pressure; evaluates on trust signals fast; web desktop primarily |

**Goals**
- Find a tester who matches the **actual stack & surface** (e.g. real iPhone + Playwright + API testing) — fast.
- Vet competence **before** spending money or a hiring slot (proof > promises).
- Hand off testing and get back clear, actionable bug reports.

**Frustrations (hypotheses)** — *[needs data]*
- "I can't tell a good tester from a good profile-writer." [est. Critical severity — this is the core trust problem]
- "Generic marketplaces make me wade through irrelevant generalists."
- "I don't even know what testing types I need — help me scope it."

**Behaviors [est.]** — low patience, high skepticism; bounces if the directory isn't instantly relevant; trusts artifacts/badges over bios.

**Design implications**
→ **QA-native filters** (specialty, device matrix, stack, verified badges) must be the first thing on the Find-Testers page.
→ Show **proof artifacts in the directory card**, not buried in profiles.
→ Provide a **guided "what testing do I need?"** posting flow (Devon often can't self-scope).
→ Default to relevance: never show an empty/irrelevant directory at cold-start (see §3 cold-start risk).

**What would CONFIRM:** clients filter primarily on specialty + proof signals and value the device matrix; guided posting raises completion.
**What would REFUTE:** clients only care about price/availability and ignore proof → de-emphasize portfolio, compete on liquidity/price.

---

### 1C. Maya — The Career-Switcher Graduate (supply) · SECONDARY

QA Mastery learner, **not yet experienced**, hungry for a first paid gig. Strong verified badges, thin work history. Matters because she's the **easiest supply to seed** (already in the funnel) and the "learn → earn" story. Design implication: let **verified badges substitute for work history** for newcomers, and consider a "first gig / open to junior work" flag. Lower priority than 1A/1B for MVP polish, but the **liquidity engine**.

> **Persona generator:** `scripts/persona_generator.py` is ready to *replace these estimates with data* once §4 collects it. Feed it the JSON schema in §4.5 → run `python scripts/persona_generator.py json`. Do **not** run it on invented data — that manufactures false confidence.

---

## 2. Journey maps (hypothesis / future-state)

Future-state maps for the two critical MVP journeys. Emotion 1–5 (1 angry → 5 delighted). All emotion values are **[est.]** — to be corrected by §4 usability sessions.

### 2A. Priya (Tester) — "Turn my skills into an inbound contact"

**Scope:** Persona Priya · Goal: get a real client to contact her · Start: hears about Talent (LinkedIn/in-app) · End: first inbound message · Timeframe: 20 min setup + days to first contact.

| Stage | 1. Discover | 2. Sign up / choose role | 3. Build profile | 4. Add proof artifact | 5. Go live & wait | 6. Get contacted |
|---|---|---|---|---|---|---|
| **Actions** | Sees a tester-spotlight post / in-app banner | Logs in (existing QA Mastery acct), picks "Tester" | Fills skills taxonomy + device matrix | Uploads a bug-report sheet / pastes automation script | Sets availability, shares public URL on LinkedIn | Opens app to a new message |
| **Touchpoints** | LinkedIn/Reddit, in-app | Supabase auth | `/talent/profile` | Portfolio editor + Storage upload | `/talent/u/[handle]` | Realtime inbox |
| **Emotion [est.]** | 3 🙂 curious | 4 🙂 "no new signup, nice" | 2 😕 "lots of fields" | 4 🙂 "my work looks legit" | 3 😐 "now what?" | 5 😄 "it worked!" |
| **Pain points** | "Is this just another Upwork?" | — (reuse of account is a win) | Taxonomy/device matrix feels long; unclear payoff | Unsure which artifact best proves skill | Silence = doubt; no feedback the profile is good | — |
| **Opportunities** | Lead with proof/outcomes in marketing | Pre-fill from existing profile + verified badges | Progressive profile; live "profile strength" meter; explain *why* each field helps matching | Artifact templates + "this is a strong example" hints; auto-pull badges | Profile-strength nudges, "X clients viewed you", first-gig seeding | Push notification + fast reply UX |

**Emotion curve (the risk is the "Valley of Death" at stages 3 & 5):**
```
5 😄                                              ╱
4 🙂        ╱╲          ╱                         ╱
3 😐 ──╱───╱──╲────────╱──╲──────────────────────
2 😕            ╲────╱      ╲(silence)
1 😠
     Discover  Signup  Profile  Artifact  Wait   Contacted
```
**Critical drop-off:** Stage 3 (profile effort vs. unclear payoff) and Stage 5 (post-publish silence). These are where testers churn.

**Prioritized opportunities** — `Priority = (Frequency + Severity + Breadth) × Solvability`, 1–5 each. Frequency/Breadth **[needs data]**; shown as estimates:

| Opportunity | Freq | Sev | Breadth | Solv | Priority [est.] | Verdict |
|---|---|---|---|---|---|---|
| Profile-strength meter + "why this field" microcopy (Stage 3) | 4 | 4 | 5 | 5 | **65** | Quick win |
| Artifact templates + strong-example hints (Stage 4) | 3 | 4 | 4 | 4 | 44 | Quick win |
| Post-publish "you're being viewed" / first-gig seeding (Stage 5) | 4 | 4 | 4 | 3 | 36 | Strategic |
| Auto-pull verified badges to cut profile effort (Stage 3) | 5 | 3 | 3 | 4 | 44 | Quick win (graduates only) |

### 2B. Devon (Client) — "Find and contact the right tester"

**Scope:** Persona Devon · Goal: contact a well-matched tester · Start: realizes he needs testing · End: sends first message · Timeframe: one sitting (~15 min).

| Stage | 1. Realize need | 2. Post project (or skip) | 3. Browse + filter testers | 4. Vet profiles | 5. Shortlist | 6. Contact |
|---|---|---|---|---|---|---|
| **Actions** | "I can't test this myself" | Guided post: type→stack→testing types→NDA | Applies QA-native filters | Reads bug-report/script artifacts + badges | Saves 2–3 candidates | Sends first message |
| **Touchpoints** | in-app/marketing | `/talent/post` | `/talent/testers` | profile pages | shortlist | Realtime chat |
| **Emotion [est.]** | 2 😕 stressed | 3 😐 "what do I even need?" | 4 🙂 "this is relevant!" | 4 🙂 "I can see real proof" | 3 😐 "are these the best?" | 4 🙂 "easy" |
| **Pain points** | Doesn't know QA scope | Posting feels like work under deadline | Empty/irrelevant results at cold-start kill trust | Hard to compare candidates | No reputation signal yet (no reviews in MVP) | Worry about being ghosted |
| **Opportunities** | "Not sure what you need?" entry point | Guided/templated posting; let him browse *before* posting | Relevance-first ranking; never-empty state; verified-badge prominence | Side-by-side compare; proof on the card | Lightweight signals (badges, recency, response rate) pre-reviews | Set response-time expectations; nudge testers to reply |

**Emotion curve (the "Aha" is Stage 3 — relevant filters):**
```
5 😄
4 🙂                    ╱────╲      ╱──╲   ╱
3 😐 ──────────╱──────╱       ╲────╱    ╲─╱
2 😕 ──╲──────╱
1 😠
     Realize  Post   Filter(aha) Vet  Short  Contact
```
**Critical risk:** Stage 3 cold-start — if the directory is empty/irrelevant on Devon's first visit, he never returns. (Mitigation = seed supply first; see §4 sequencing + PRD §5 cold-start.)

| Opportunity | Freq | Sev | Breadth | Solv | Priority [est.] | Verdict |
|---|---|---|---|---|---|---|
| Relevance-first ranking + never-empty directory (Stage 3) | 5 | 5 | 5 | 3 | **45** | Strategic — gate launch on it |
| Guided "what testing do I need?" posting (Stage 2) | 4 | 4 | 4 | 4 | 48 | Quick win |
| Proof artifact on the directory card (Stage 4) | 4 | 4 | 5 | 4 | 52 | Quick win |
| Pre-review trust signals: badges + response rate (Stage 5) | 4 | 4 | 4 | 3 | 36 | Strategic |

---

## 3. Empathy snapshot (for design workshops)

| | **Priya (Tester)** | **Devon (Client)** |
|---|---|---|
| **Thinks** | "Will anyone actually see my work?" | "Can I trust this person before I pay?" |
| **Feels** | Under-recognized, hopeful | Pressed for time, skeptical |
| **Says** | "I'm good but invisible." | "Just show me who can actually do this." |
| **Does** | Polishes profile *if* it pays off; abandons long forms | Filters hard, bounces on irrelevance, vets via proof |
| **Pain** | Standing out; post-publish silence | Telling skill from self-promotion; cold-start emptiness |
| **Gain** | An inbound message from a real client | A vetted, relevant tester in one sitting |

---

## 4. Validation research plan (turns proto → data-backed)

Lean, $0-budget, solo-runnable. Goal: move personas from **Low → Medium confidence** and de-risk the two journeys **before** building the full MVP.

### 4.1 Research questions
1. **(Primary)** Do testers value *proof-of-skill / standing out* over *job volume*? (decides whether portfolio-first or bidding-first)
2. **(Primary)** Do clients filter on QA-native signals (specialty, device matrix, proof) — and can they self-scope testing needs, or do they need guidance?
3. Which profile fields do testers actually complete vs. abandon? Where's the Valley-of-Death?
4. What trust signals do clients need *pre-reviews* to send a first message?
5. *(Exploratory)* Is the "learn → earn" badge story a real motivator or a nice-to-have?

### 4.2 Methods (match question → method, per the skill's selection table)
| Question | Method | Sample | Why |
|---|---|---|---|
| Q1, Q5 (tester attitudes) | **Survey** to QA Mastery learners + LinkedIn/Reddit QA communities | 30–50 | Cheap, segments supply, feeds `persona_generator.py` |
| Q2, Q4 (client attitudes/trust) | **5 moderated remote interviews** with indie devs/founders | 5–8 | "Why" depth; small N finds most issues |
| Q2, Q3 (can they *do* the flows) | **Usability test** on a clickable prototype (§5) | 5 testers + 5 clients | 5 users ≈ 80% of usability issues |
| Liquidity sanity | **Guerrilla** posts ("would you use this?") in 2–3 QA subreddits/Discords | 5–10 reactions | Rapid demand signal |

**Approach:** remote, mostly unmoderated survey + moderated calls over Zoom/Meet. **Tools:** Tally/Google Form (already in the feedback stack), Zoom, a Figma/click-through prototype.

### 4.3 Recruitment (reuse existing channels — $0)
| Channel | Side | Target | Incentive |
|---|---|---|---|
| In-app + email to QA Mastery learners | Testers | 30–50 survey, 5 interviews | Early access + "first 50 founding testers" badge |
| LinkedIn (founder's network) + r/QualityAssurance, r/softwaretesting | Both | top-up | Shout-out / early access |
| Indie/startup Discords, r/startups, IndieHackers | Clients | 5–8 | Free testing match at launch |

### 4.4 Success criteria (decision gates before full build)
- **Persona confidence → Medium:** ≥20 testers + ≥5 clients with aligned patterns.
- **Go portfolio-first** if ≥40% of testers rank proof/standing-out #1 (else reconsider bidding model).
- **Guided posting required** if ≥3/5 clients can't self-scope testing needs unaided.
- **Launch gate:** clients in the usability test reach a relevant tester in <3 min with >80% task success.

### 4.5 Data schema for `persona_generator.py`
Collect the survey into this shape so the script produces data-backed personas (replaces the §1 estimates):
```json
[
  {
    "user_id": "tester_01",
    "age": 27,
    "usage_frequency": "daily",
    "features_used": ["portfolio", "device_matrix", "messages", "badges"],
    "primary_device": "desktop",
    "usage_context": "work",
    "tech_proficiency": 8,
    "pain_points": ["invisible on generic marketplaces", "too many bids per job"]
  }
]
```
Then: `python scripts/persona_generator.py json` → archetype, frequency-counted frustrations, stated confidence.

---

## 5. Usability test plan (prototype → pre-build validation)

**Study:** "QA Talent — core flows" · Moderated remote · 45–60 min · 5 testers + 5 clients · clickable prototype.

### Research questions (testable)
- Can a **tester** build a profile + add one proof artifact in <10 min, unaided?
- Can a **client** filter to a relevant tester and send a first message in <3 min, >80% success?
- Where do users hesitate, error, or give up? (severity-rated)

### Tasks (scenarios, not instructions)
**Tester:**
1. *Warm-up:* "Tell me how you currently show clients you're good at testing."
2. *Core:* "You just heard about QA Talent. Set yourself up so a client would want to hire you." (observe taxonomy, device matrix, artifact)
3. *Secondary:* "Add proof that you can do API automation."
4. *Reflection:* "What would make you trust this enough to put real effort in?"

**Client:**
1. *Warm-up:* "Walk me through the last time you needed testing done."
2. *Core:* "Find someone who can test your React web app on a real iPhone and do API checks, then contact them."
3. *Edge:* "You're not sure what testing you need — show me what you'd do."
4. *Reflection:* "Would you trust these testers without star ratings? What's missing?"

### Metrics & severity
| Metric | Target |
|---|---|
| Task completion | >80% |
| Time-to-contact (client) | <3 min |
| Time-to-first-artifact (tester) | <10 min |
| Error rate | <15% |
| Post-task satisfaction | >4/5 |

Rate every issue **4 Critical / 3 Major / 2 Minor / 1 Cosmetic**; fix Critical+Major before MVP launch. Use the moderator guide in `assets/research_plan_template.md`.

---

## 6. How this feeds the build

| Finding type | Feeds into (PRD ref) |
|---|---|
| Tester values proof vs volume (Q1) | Profile layout & whether MVP is portfolio-first vs application-first (PRD §1A, §4) |
| Client filter behavior (Q2) | Find-Testers ranking & filter order (PRD §3A) |
| Valley-of-Death fields (Q3) | Progressive profile + strength meter (PRD §4 MVP) |
| Pre-review trust signals (Q4) | What ships before reviews in V1.0 (PRD §4, §5) |
| Cold-start usability | Launch sequencing: seed supply before opening demand (PRD §5) |

---

## Validation checklist (current state)

- [ ] Based on 20+ users — **NO (0 — provisional)** → run §4
- [ ] 2+ data sources — **NO** → survey + interviews (§4.2)
- [x] Specific, actionable goals & design implications
- [x] Confidence level stated (**Low**)
- [ ] Frustrations include frequency counts → after §4 survey
- [x] Journey layers filled (actions, touchpoints, emotions, pain, opportunities)
- [x] Opportunities prioritized (scores marked [est.]/[needs data])
- [x] Usability tasks are realistic scenarios, not instructions
- [x] Usability sample ≥5 per side; success metrics + severity defined

**Bottom line:** This pack is a rigorous set of *assumptions and a plan to test them* — not validated research. The single highest-value next action is running §4 (lean, $0, ~2 weeks) to earn the right to call these personas real before investing build effort.
