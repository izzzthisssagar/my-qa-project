# Sample Lesson 2 — Your First Real Bug Report (A4.4, lab-led)

**Type:** Manual lab lesson · **Time:** ~35 min · **Free-tier:** Yes for validation phase (moves behind paywall at launch; the public teaser keeps only the hunt, not the graded report)
**Pattern:** See it (briefly) → Try it (guided repro) → Do it (hunt + report) → Prove it

---

## Hook

> A developer reads your bug report for 30 seconds and decides: fix it now, or throw it in the backlog swamp.
> The difference is rarely the bug. It's the report.
> Today you find a real bug and write a report a developer would actually fix.

---

## Part 1 — SEE IT: Anatomy of a report that gets fixed (5 min)

**Widget: `report-comparison`** — the same bug (BS-002) reported twice, side by side:

❌ *"signup broken. password not working. pls check"*
✅ Structured report with: **Title** ("Signup: error message blames 'username' when password fails validation"), **Environment**, **Steps to reproduce** (numbered, exact data), **Expected result**, **Actual result**, **Evidence** (screenshot), **Severity: Minor / Priority: Medium**.

Toggle button: "Dev's reaction" — shows time-to-fix estimate for each (left: bounced back "cannot reproduce"; right: fixed same sprint). Six anatomy parts become clickable callouts, each with a one-line rule:

1. **Title = location + trigger + wrong outcome** in ≤ 12 words.
2. **Steps:** exact data, numbered, from a clean state. A stranger must reproduce it.
3. **Expected vs actual:** expected comes from the spec, not your opinion.
4. **One bug per report.** Two bugs in one report = one bug gets lost.
5. **Evidence:** screenshot with the failure visible; console/network only if you have it.
6. **Severity ≠ priority** (15-second recap card; full lesson is A4.3).

## Part 2 — TRY IT: Guided reproduction (10 min)

Learner opens BuggyShop signup (embedded). Guided script walks them into **BS-002**:

1. Go to Signup. Enter name `Asha Verma`, email `asha@test.io`.
2. Enter password `abc` (too short on purpose). Submit.
3. **Observe:** error appears only now (no inline hint existed), and it reads *"Username is invalid."*
4. Prompted questions (checkboxes/free text): What did you expect? What actually happened? Which field is the message blaming? Is this one bug or two? *(Discussion reveal: arguably two — late validation timing AND wrong message; we report the wrong message as the defect, note the timing as a usability observation. Judgment calls like this are the job.)*

## Part 3 — DO IT: The hunt + the report (15 min, graded)

**Hunt scope:** Signup page only. Seeded & reachable here: BS-001 (email regex), BS-003 (paste bypasses confirm-match), BS-004 (double-click bypasses terms). Learner must find **one** of these on their own — hints unlock after 7 minutes ("Try being rude to the email field"; "What if the two password fields disagree?"; "What can a fast double-click skip?").

**Report form (structured, per locked decision #2):**
- Page (dropdown) · Feature (dropdown) · Title (text) · Steps (numbered list) · Expected (text) · Actual (text) · Severity (dropdown) · Evidence (auto-screenshot button).

**Grading (auto + rubric hybrid):**
| Criterion | Weight | Auto-checkable? |
|---|---|---|
| Bug matches a manifest entry (page+feature+category) | 30% | Yes |
| Steps reproduce from clean state (step-count + required data present) | 25% | Partially (heuristics); rubric fallback |
| Title ≤ 12 words, contains location + wrong outcome | 15% | Yes (pattern) |
| Expected/actual filled, distinct, spec-grounded | 15% | Rubric |
| Severity within ±1 of manifest | 10% | Yes |
| One bug per report | 5% | Rubric |

Pass ≥ 70. Feedback shows the manifest's model report for the bug they found, diffed against theirs.

## Part 4 — PROVE IT (quiz, 5 questions)

1. Best title for BS-003? *(multiple choice, picks location+trigger+outcome form)*
2. A report says "login sometimes fails." What's the single biggest missing element?
3. Severity vs priority: homepage logo typo the day before a press demo — rate both.
4. Why one bug per report?
5. Your repro steps work on your machine but not the dev's. List two likely differences to document. *(env/browser, data/state)*

**Portfolio:** the graded report becomes the learner's first portfolio artifact.

---

## Production notes
- Public teaser version (`/play/find-the-bug`): signup page + "Can you find one of the 3 bugs hidden here?" with a counter of how many visitors found each. No grading, ends at the report form with signup wall. This is the validation-week traffic driver.
- The model-report diff view is the single highest-effort UI piece here; fallback v0 = show model report side-by-side without diffing.
