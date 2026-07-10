# QA Mastery — Social Posts: Weeks 5, 6, 7 & 8

Same rules as weeks 2–4:
- LinkedIn links go in the **first comment**, never the body.
- Proof posts use `[bracketed placeholders]` — fill with real numbers/quotes only. **Do not invent testimonials.**
- Community variants give value first, soft CTA last.

---

## WEEK 5

### Monday — LinkedIn (TEACH)

**Hook:**
> Five bug-report mistakes that scream "junior" — and the one-line fix for each.

**Body:**
I grade bug reports every day. The same five mistakes show up in almost every rejected one:

1. **The rumor title.** "Login broken." Broken *how*? Fix: component + symptom in one line — "Login: valid password rejected after email with uppercase letters."
2. **Steps that start mid-air.** Step 1 assumes you're already logged in, mid-cart, on the right release. Fix: start from a clean state, every time.
3. **No expected result.** You described what happened but never what *should* have. The diff IS the bug. Fix: quote the rule you believe was violated.
4. **Evidence-free claims.** No screenshot, no console error, no response body. Fix: attach the one artifact a developer would ask for first.
5. **Severity theater.** Everything marked "critical" — so nothing is. Fix: money/user-blocking = high. Cosmetic = low. Be the person whose severity ratings can be trusted.

Every one of these is a habit, and habits form by repetition against feedback. That's the whole reason QA Mastery grades your reports against a hidden answer key instead of showing you a model answer to copy.

Which of the five do you catch yourself doing? I'll go first: early on, my titles were all rumors.

**First comment:**
File a graded report against a real seeded bug (first module free): https://qa-mastery-platform.vercel.app

---

### Wednesday — LinkedIn (DIFFERENTIATE)

**Hook:**
> Watching a testing course is like watching gym videos. The muscle doesn't know.

**Body:**
Course platforms measure the wrong thing. "87% watched" means 87% of a video played while someone made tea.

Here's what watching can't give you:

- The moment a bug report you wrote comes back **rejected** with the reason.
- The dead end where your locator matches nothing and *you* have to figure out why.
- The severity call you defended — wrongly — and the correction that sticks forever.

Those three moments teach more than ten hours of video, because they're *yours*. Failure you own is the only curriculum that transfers.

So we built QA Mastery backwards from that: a deliberately broken shop, a live API with seeded contract violations, and grading that reads your actual work — test cases, bug reports, code — the way a lead would.

You can't watch your way into a QA job. You can absolutely *practice* your way in.

**First comment:**
The first module of each track is free, no card: https://qa-mastery-platform.vercel.app

---

### Friday — LinkedIn (ENGAGE, poll)

**Body:**
Poll: If you're breaking into QA this year — which track are you starting with?

- 🖱️ Manual first (learn to see bugs, then automate)
- 🤖 Automation first (code from day one)
- 🤷 Honestly torn — convince me

Context for the torn: manual-first teaches you *what* to test; automation-first teaches you *how* to scale it. We built both tracks because the right answer depends on your background — but I have a strong opinion for career-switchers. Poll first, opinion in the comments Monday.

---

## WEEK 6

### Monday — LinkedIn (TEACH)

**Hook:**
> Everyone tests the happy path. Bugs live where nobody looks. Here's the map.

**Body:**
Want to find bugs other testers miss? Stop testing what the app is *supposed* to do and start interrogating what it *promises implicitly*:

1. **Boundaries.** Not "does quantity work" — what happens at 0, 1, 999, 1000, -1? The free-shipping rule that says "over $999" — does exactly $999 qualify? (In our practice shop, that exact bug is seeded. Learners walk past it for days.)
2. **State transitions.** Can you cancel an order that already shipped? Pause something twice? Go back after submitting?
3. **The second time.** Everything works once. Submit twice, apply the coupon twice, click save twice — fast.
4. **Interruptions.** Refresh mid-checkout. Lose network mid-upload. Come back tomorrow with the same tab open.
5. **Someone else's data.** Change the ID in the URL. Can you see order #1042 that isn't yours? (More common in production than anyone admits.)

The pattern: bugs cluster at *edges* — of ranges, of states, of sessions, of permissions. Test the edges and you'll out-find testers with twice your experience.

Which edge found you your best bug? Genuinely collecting these.

**First comment:**
Practice all five hunting grounds on BuggyShop (real seeded bugs, graded reports): https://qa-mastery-platform.vercel.app

---

### Wednesday — LinkedIn (PROOF — learner spotlight #1)

> ⚠️ Fill only with a real learner and their permission. Do not invent. If no
> testimonial exists yet, swap in the week-7 Wednesday post and run this when
> you have one.

**Hook:**
> [Learner first name] went from [starting point] to [result] in [timeframe]. Here's the actual work.

**Body:**
[2–3 sentences of their story, in their words if possible.]

What I want you to look at is not the outcome — it's the artifact: [describe one real graded deliverable — a bug report, a test plan, an automation script — and what made it good].

[Quote — verbatim, with permission.]

[Result — job / interview / first automation suite / portfolio — stated plainly, no inflation.]

**First comment:**
The same track [name] used starts free: https://qa-mastery-platform.vercel.app

---

### Friday — LinkedIn (ENGAGE)

**Body:**
Confession thread: what's the one QA concept everyone assumes you know, that you've quietly never fully understood?

Severity vs priority? What "regression" actually covers? Why POST isn't idempotent? When "flaky" is the test's fault vs the app's?

Drop it below — no judgment, real answers only. I'll answer every single one this weekend, and the best questions become next month's lessons. (That's not a gimmick — half our curriculum already comes from questions like these.)

---

## WEEK 7

### Monday — LinkedIn (TEACH)

**Hook:**
> Two techniques turn "I clicked around a bit" into "I tested it." Fifteen minutes to learn both.

**Body:**
**Equivalence Partitioning (EP):** you can't test every input, so split them into groups the code treats identically. An age field accepting 18–65: one valid partition (18–65), two invalid (under 18, over 65). Three tests cover what three hundred wouldn't.

**Boundary Value Analysis (BVA):** bugs love the fence lines between partitions. So test *at* the edges: 17, 18, 65, 66. Off-by-one errors — `>` written where `>=` belonged — live exactly there, and they're some of the most common bugs in real code.

Together: partition first (what groups exist?), then hit every boundary of every group. That's a *designed* test suite — defensible in a review, explainable in an interview.

Interview tip: when they ask "how would you test this field?", answering with EP + BVA by name, then walking the partitions out loud, is the difference between "clicked around" and "tested."

**First comment:**
Our test-design module has an interactive boundary widget — slide the input, watch the bug appear: https://qa-mastery-platform.vercel.app

---

### Wednesday — LinkedIn (BUILD-IN-PUBLIC)

**Hook:**
> One month of user feedback, ranked in a spreadsheet, decided our roadmap. Here's the actual list.

**Body:**
Every piece of feedback from the last month — [N] items from [in-app form / DMs / community] — went into one sheet and got RICE-scored (Reach × Impact × Confidence ÷ Effort). No vibes, no pet features.

What you asked for most:
1. [Real theme #1 — e.g. "more API testing practice"] — [count] requests
2. [Real theme #2] — [count]
3. [Real theme #3] — [count]

What we're shipping because of it:
- ✅ [Feature already shipped in response] — done
- 🔨 [Feature in progress] — building now
- 📋 [Feature planned] — next

What we're *not* doing (and why): [one honest cut + the reasoning — this line builds more trust than the whole list above].

If you told me something last month: this is where it went. If you haven't yet — the form takes 60 seconds, and apparently it steers the roadmap.

**First comment:**
Feedback form: [link] · The platform it improves: https://qa-mastery-platform.vercel.app

---

### Friday — LinkedIn (ENGAGE / CTA)

**Body:**
Free lab Friday. 🔓

BuggyShop's cart module has [N] seeded bugs. One of them involves free shipping and the number 999. That's your only hint.

Find it, file a report, get graded against the hidden answer key — no card, no trial timer, first module's just free.

Fastest correct report gets a shoutout here Monday (with permission). Go break something useful.

**First comment:**
Start here: https://qa-mastery-platform.vercel.app

---

## WEEK 8

### Monday — LinkedIn (TEACH)

**Hook:**
> Testers who can read an API response don't wait for the UI to tell them what broke.

**Body:**
The UI says "Something went wrong." Useless. The API response under it says exactly what:

**Read these four things, in order:**

1. **Status code — the genre.** 2xx worked · 4xx *you* (the client) got something wrong · 5xx *they* (the server) broke. A 400 vs 500 distinction alone tells you which team owns the bug.
2. **The error body — the plot.** Good APIs return a machine-readable envelope: `{"error": {"code": "unauthorized", "message": …}}`. Quote it verbatim in your bug report — it's the strongest evidence you can attach.
3. **Headers — the fine print.** `WWW-Authenticate` tells you which auth was expected. `Retry-After` tells you rate limiting is by design, not a bug.
4. **The contract.** Compare what came back against what the docs *promise*. A 200 with a wrong field is still a bug — arguably a worse one, because nothing alarmed.

This is exactly why our practice API (TaskFlight) ships with real Swagger docs and seeded *contract violations* — responses that look fine and lie. Spotting those is the skill.

What's the sneakiest API bug you've caught — one where the status code said "fine"?

**First comment:**
Explore TaskFlight with your own sandbox: https://qa-mastery-platform.vercel.app

---

### Wednesday — LinkedIn ("You asked, we built it" #2)

> ⚠️ Fill with the real shipped feature when this week arrives — candidates
> from the current build: the Notes wiki (searchable reference encyclopedia),
> the task board, or interactive notes with runnable code. Use real request
> quotes only.

**Hook:**
> You asked. We built it. Round two.

**Body:**
The ask: "[verbatim user request, with permission]" — and [N] variations of the same theme.

What shipped: **[feature name]** — [2–3 sentences: what it does, in learner-benefit terms, not feature terms].

The detail I'm proudest of: [one concrete craft decision — e.g. "every note's code block actually runs — real compiler, not a screenshot"].

It's live for every learner now. Keep telling me what's missing — this is round two because round one worked.

**First comment:**
See it live: https://qa-mastery-platform.vercel.app · Feedback form: [link]

---

### Friday — LinkedIn (ENGAGE — AMA)

**Body:**
AMA: breaking into QA, no gatekeeping. 🎤

I'll answer everything in the comments this weekend — how to start with zero experience, manual vs automation first, whether certifications matter, what a graded portfolio does in interviews, how I'd learn Selenium in 2026, what hiring managers actually skim for in bug reports.

No question too basic. The "too basic" questions are usually the ones half the lurkers also have.

One rule: real questions over hypotheticals. What's *actually* blocking you this week?

**First comment:**
If your question needs a longer answer, it becomes next week's post. Backlog of everything shipped so far: https://qa-mastery-platform.vercel.app

---

## Community variants (Reddit r/QualityAssurance · Ministry of Testing)

Reuse the week-5 Monday and week-8 Monday teach posts with these swaps:
- Strip all product mentions from the body; value only.
- Single soft CTA as a final line: "I practice these on a free seeded-bug app — link in my profile if useful."
- Reddit titles as questions ("What bug-report mistakes made you cringe as a junior?") — question titles outperform statements there.
