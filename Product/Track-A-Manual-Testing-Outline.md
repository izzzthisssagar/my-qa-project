# Track A — Manual Testing Foundation: Lesson-Level Outline

**Status:** Draft v1 · Week 1 deliverable · Owner: Sagar
**Format per lesson:** See it (visual widget) → Try it (guided) → Do it (lab) → Prove it (quiz)
**Total:** 5 modules · 28 lessons · ~40 hours learner effort
**Practice target:** BuggyShop (see `BuggyShop-Spec.md`). Bug IDs referenced as `BS-###`.

---

## Module A1 — How Software Is Built (and Breaks) · 5 lessons · ~5 h

### A1.1 What Is Software Testing, Really?
- **Objective:** Define testing as risk-information gathering, not "clicking around." Distinguish testing from QA from QC.
- **Visual:** Interactive "ship or don't ship" simulator — learner sees a release dashboard with partial test info and must decide; reveals consequences.
- **Lab:** None (first lesson stays frictionless).
- **Quiz:** 5 Qs.

### A1.2 SDLC — How Software Gets Built
- **Objective:** Name SDLC phases and what QA does in each. Waterfall vs Agile vs DevOps at a glance.
- **Visual:** Interactive pipeline — drag a "requirement" card through phases; toggle Waterfall/Agile/DevOps and watch the flow change shape.
- **Lab:** Match 10 QA activities to the right phase (drag-and-drop, auto-checked).
- **Quiz:** 6 Qs.

### A1.3 STLC — The Tester's Own Lifecycle
- **Objective:** Requirement analysis → planning → case design → env setup → execution → closure; entry/exit criteria.
- **Visual:** STLC wheel; click each phase to see its artifacts (test plan, RTM, cases, reports) with real examples.
- **Lab:** Given a mini feature spec ("BuggyShop wishlist"), order the STLC activities and pick the correct exit criteria.
- **Quiz:** 6 Qs.

### A1.4 What Is a Bug? (Defect, Error, Failure)
- **Objective:** Error vs defect vs failure chain; bug lifecycle states; why bugs cluster.
- **Visual:** Animated chain: developer mistake → defect in code → failure at runtime. Bug lifecycle as a clickable state machine (New → Assigned → Fixed → Retest → Closed/Reopened).
- **Lab:** First contact with BuggyShop: free-explore 15 minutes, submit 3 "observations" (not formal reports yet). Graded for: is it actually unexpected behavior?
- **Quiz:** 5 Qs.

### A1.5 The Cost of Bugs & Where QA Sits in Agile
- **Objective:** Cost-of-defect curve; shift-left; QA's seat in Scrum ceremonies.
- **Visual:** "Catch the bug" cost game — same bug caught at requirements/dev/staging/production, watch cost multiply; interactive sprint board showing where testers plug in.
- **Lab:** Scenario quiz: 5 sprint situations, choose what a good QA does.
- **Quiz:** 5 Qs.
- **Milestone:** Module A1 badge. *(A1 is the free-tier hook — keep production quality highest here.)*

---

## Module A2 — Testing Fundamentals · 5 lessons · ~6 h

### A2.1 Verification vs Validation
- **Objective:** Build the right thing vs build the thing right; static vs dynamic testing.
- **Visual:** Split-screen widget — same feature, one side reviews the spec (verification), other side tests the build (validation).
- **Lab:** Sort 12 activities into verification/validation buckets.
- **Quiz:** 5 Qs.

### A2.2 Testing Levels — Unit → Integration → System → UAT
- **Objective:** What each level catches, who owns it, what it costs.
- **Visual:** Interactive pyramid; click a level to inject a bug and see which level catches it (and which miss it).
- **Lab:** Given 8 BuggyShop bugs (described), assign the level that should have caught each.
- **Quiz:** 6 Qs.

### A2.3 Testing Types — Functional vs Non-Functional
- **Objective:** Functional, usability, performance, security, compatibility — the map, not the depth (depth comes in later tracks).
- **Visual:** Card explorer — each type is a flip-card with a 60-second interactive micro-demo on BuggyShop (e.g., usability card shows a confusing checkout flow).
- **Lab:** Tag 10 test scenarios with the correct type.
- **Quiz:** 6 Qs.

### A2.4 Black / White / Grey Box
- **Objective:** Approaches by knowledge-of-internals; where manual testers live.
- **Visual:** A literal box widget — slide transparency from black to white; the same login feature shows what you can see/test at each setting.
- **Lab:** 8 scenarios → classify approach.
- **Quiz:** 5 Qs.

### A2.5 The 7 Testing Principles (Live)
- **Objective:** All 7 ISTQB principles, demonstrated rather than recited.
- **Visual:** Principle playground — e.g., pesticide paradox: rerun the same 5 tests on BuggyShop v1.1 while a new seeded bug ships untouched; defect clustering: heatmap of where BuggyShop's bugs actually live.
- **Lab:** Match principles to 7 real-world mini-stories.
- **Quiz:** 7 Qs.
- **Milestone:** Module A2 badge.

---

## Module A3 — Test Design Techniques · 6 lessons · ~9 h *(the heart of the track)*

### A3.1 Why Design Tests? (vs Random Clicking)
- **Objective:** Coverage thinking; you can't test everything — choose intelligently.
- **Visual:** "Infinite inputs" visualizer — an input field's possible-value space rendered as a huge grid; watch techniques carve it into a handful of smart picks.
- **Lab:** Free-test BuggyShop signup for 10 min, count what you covered; then see a designed suite cover 3× with fewer steps (humbling on purpose).
- **Quiz:** 4 Qs.

### A3.2 Equivalence Partitioning
- **Objective:** Partition valid/invalid classes; one test per class.
- **Visual:** Interactive partitioner — drag boundaries onto an input range (e.g., BuggyShop discount code length 5–10 chars), classes auto-color.
- **Lab:** Partition BuggyShop's "quantity" field (1–99) and pick minimal test set; auto-checked against expected classes. Finds seeded bug BS-007 if done right.
- **Quiz:** 5 Qs.

### A3.3 Boundary Value Analysis
- **Objective:** Bugs live at the edges; 2-value and 3-value BVA.
- **Visual:** BVA slider on a real BuggyShop field — drag across the boundary and watch pass/fail flip exactly at the edge (seeded off-by-one bug BS-008 revealed live).
- **Lab:** Design BVA cases for price filter (min 0, max 100000) and age field; auto-checked. Should catch BS-008.
- **Quiz:** 6 Qs.

### A3.4 Decision Tables
- **Objective:** Combinatorial conditions → complete rule coverage.
- **Visual:** Decision-table builder — conditions for BuggyShop free-shipping (cart > ₹999, member, promo code) auto-generate columns; collapse impossible rules.
- **Lab:** Build the table for BuggyShop's payment-method availability logic; execute the 6 derived tests; one rule exposes BS-011.
- **Quiz:** 5 Qs.

### A3.5 State Transition Testing
- **Objective:** Model states/events; valid vs invalid transitions.
- **Visual:** Order-status state machine (Placed → Paid → Shipped → Delivered / Cancelled) — learner drags transitions; invalid ones flash red.
- **Lab:** Draw the state diagram for BuggyShop order flow, derive transition tests, execute; invalid-transition test exposes BS-014 (cancel after shipped).
- **Quiz:** 5 Qs.

### A3.6 Error Guessing & Technique Choice
- **Objective:** Experience-based testing; choosing which technique fits which problem.
- **Visual:** "Tester instincts" checklist explorer (empty inputs, special chars, paste, double-click, back-button…), each instantly try-able on a BuggyShop form.
- **Lab (mini-capstone):** Signup + cart + checkout: design a full test-case set using ALL techniques. Auto-scored against an expected-coverage rubric (technique used, classes covered, boundaries hit). Should surface BS-003, BS-007, BS-008, BS-016.
- **Quiz:** 6 Qs.
- **Milestone:** Module A3 badge + "Test Designer" portfolio artifact (their case set, exportable).

---

## Module A4 — Test Cases, Bug Reports & Tools · 6 lessons · ~9 h

### A4.1 Writing Test Cases That Don't Embarrass You
- **Objective:** Anatomy: ID, title, precondition, steps, data, expected result; atomic vs bloated cases.
- **Visual:** "Fix this test case" editor — a terrible case, learner repairs it field by field, live score.
- **Lab:** Write 5 cases for BuggyShop login in the platform's case editor; rubric-graded (clarity, atomicity, expected results).
- **Quiz:** 5 Qs.

### A4.2 Test Data & Preconditions
- **Objective:** Designing data deliberately; data dependency traps; idempotent tests.
- **Visual:** Data-matrix widget — pair test cases with data variants; watch a case fail purely from stale data.
- **Lab:** Build a data sheet for checkout testing (cards, addresses, coupons); auto-checked for coverage.
- **Quiz:** 4 Qs.

### A4.3 Priority vs Severity (Triage)
- **Objective:** Severity = impact, priority = order; they diverge.
- **Visual:** **Triage game** — 12 incoming BuggyShop bugs, drag onto a severity×priority grid; instant feedback with reasoning (e.g., logo typo on homepage: low sev, high pri before a demo).
- **Lab:** Triage 8 more bugs, justify 2 in free text (rubric-graded).
- **Quiz:** 5 Qs.

### A4.4 The Bug Report That Gets Fixed
- **Objective:** Title, env, steps, expected vs actual, evidence; reproducibility; one bug per report.
- **Visual:** Side-by-side: a vague report vs a great report for the same bug; toggle to see dev reaction time.
- **Lab:** BS-002 is reproduced in front of the learner (guided); they file the report in the platform's bug tool; graded on completeness + repro clarity.
- **Quiz:** 5 Qs.

### A4.5 Tools of the Trade — Jira & Test Management
- **Objective:** Jira workflow (epic/story/bug), boards; test-management basics (suites, runs, RTM).
- **Visual:** Simulated Jira board + simulated TestRail-style run screen inside the platform (no external accounts needed in v1).
- **Lab:** Execute a provided 10-case run against BuggyShop, mark pass/fail, link failures to bug reports.
- **Quiz:** 5 Qs.

### A4.6 🐞 BUG HUNT I (graded milestone)
- **Objective:** Apply everything: find and report real bugs.
- **Format:** Timed-ish (suggested 90 min) hunt on BuggyShop v1.0 signup→checkout. **10 of 18 reachable seeded bugs** to pass; reports auto-graded on: correct bug identified (manifest match), repro steps work, severity within tolerance, no duplicates.
- **Output:** Portfolio artifact: "Found X bugs, sample reports."
- **Milestone:** Module A4 badge.

---

## Module A5 — Real-World Manual QA · 6 lessons · ~10 h

### A5.1 Exploratory Testing & Session-Based Test Management
- **Objective:** Charters, time-boxes, note-taking; exploratory ≠ random.
- **Visual:** Charter builder + live session timer with note pane integrated over BuggyShop.
- **Lab:** Run a 30-min charter ("Explore profile & order history for data-integrity issues"); session notes rubric-graded. Area contains BS-019, BS-020.
- **Quiz:** 4 Qs.

### A5.2 Smoke, Sanity, Retest & Regression
- **Objective:** What each is, when each runs, how regression suites grow.
- **Visual:** Release-train widget — a new BuggyShop build arrives; learner picks which suite to run at each stage and sees what escapes if they skip.
- **Lab:** BuggyShop **v1.1 ships** (new wishlist feature + 2 regressions seeded: BS-021, BS-022). Run the regression suite, catch the regressions.
- **Quiz:** 5 Qs.

### A5.3 Cross-Browser, Responsive & Compatibility Basics
- **Objective:** Why rendering differs; viewport testing; a sane compatibility matrix.
- **Visual:** Viewport switcher on BuggyShop (mobile/tablet/desktop) — BS-023 (mobile-only overlap) visible live.
- **Lab:** Test checkout at 3 viewports, file what breaks.
- **Quiz:** 4 Qs.

### A5.4 UAT, Test Reporting & Sign-off
- **Objective:** UAT vs system test; test summary reports; go/no-go input.
- **Visual:** Report builder — metrics auto-pulled from the learner's own v1.0/v1.1 runs (their real pass rates, bug counts).
- **Lab:** Write the v1.1 test summary + recommendation email to a fake PM; rubric-graded (clarity, data-backed, honest risk statement).
- **Quiz:** 4 Qs.

### A5.5 Working With Developers (Without Wars)
- **Objective:** "Not a bug" disputes, async communication, evidence discipline, when to escalate.
- **Visual:** Branching conversation sim — a dev rejects your bug; choose responses; see outcomes.
- **Lab:** Rewrite 2 hostile bug comments into professional ones (rubric).
- **Quiz:** 4 Qs.

### A5.6 🏆 CAPSTONE — Full Test Cycle on BuggyShop v2.0
- **Format:** v2.0 ships with a new feature (coupons) + **12 fresh seeded bugs** (BS-026…BS-037, defined in manifest v2). Learner delivers: mini test plan (scope/risks/approach) → designed test cases (techniques required) → execution run → bug reports → summary report with ship/no-ship recommendation.
- **Grading:** Hybrid — auto (bug matches, case coverage, run completeness) + rubric (plan quality, report quality). Rubric graded by you initially; collect these to train AI-assisted grading later.
- **Output:** The flagship portfolio artifact + **Track A certificate**.

---

## Production Notes

- **Build order:** A1 → A3 → A4 → A2 → A5. (A1 is the free hook; A3+A4 are the value core; A2 is mostly widgets reusable from A1; A5 depends on BuggyShop v1.1/v2.0 existing.)
- **Widget reuse:** 28 lessons need only ~12 distinct widget *types* (drag-sort, slider-boundary, state-machine, flip-cards, triage-grid, editor-with-rubric, session-timer, viewport-switcher, sim-Jira, report-builder, branching-dialog, pipeline). Spec each once, skin per lesson.
- **Quiz bank:** ~140 questions total. Draft with AI, expert-review every one.
- **Dependency:** A1.4 onward requires BuggyShop v1.0 live. A5.2 requires v1.1. A5.6 requires v2.0.
