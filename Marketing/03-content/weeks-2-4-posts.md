# QA Mastery — Launch Social Posts: Weeks 2, 3 & 4

A quick note on how to use this:
- LinkedIn links always go in the **first comment** (the body never contains the link, so the algorithm doesn't suppress reach).
- Replace `qa-mastery-platform.vercel.app` with your final domain if it changes.
- Proof posts use `[bracketed placeholders]` — fill them with real numbers/quotes only. Do not invent testimonials.
- Community posts (Reddit / Ministry of Testing) are written to give value first and lead with the soft CTA at the end, since those communities punish drive-by promotion.

---

## WEEK 2

### Monday — LinkedIn (TEACH)

**Hook:**
> "Found a bug" is not a bug report. It's a rumor.

**Body:**
Most people learning QA write bug reports like this:

"The checkout is broken."

That's a rumor. A developer can't act on it, a hiring manager won't respect it, and you can't reproduce it next week.

Here's the skeleton every report needs:

1. **Title** — component + what's wrong, in one line. "Checkout: order total ignores quantity > 1"
2. **Steps to reproduce** — numbered, from a clean state. If you can't list the steps, you didn't actually find it.
3. **Expected result** — what the spec/logic says should happen.
4. **Actual result** — what really happened.
5. **Evidence** — screenshot, console error, network response.
6. **Severity** — does it block money/users, or is it cosmetic?

The gap between "the checkout is broken" and the version above IS the job. That's literally what you get paid to do.

This week in BuggyShop, the deliberately broken e-commerce app inside QA Mastery, learners are filing reports against the cart module and getting graded on exactly these fields. Not graded by a quiz. Graded against a real answer key.

What's the one field beginners skip most? My vote: "Expected result." They describe the bug but never say what *should* have happened. Yours?

**First comment:**
Try the cart module yourself, free, here: https://qa-mastery-platform.vercel.app
The first module of every track is free, no card.

---

### Wednesday — LinkedIn (BUILD-IN-PUBLIC / PROOF)

**Hook:**
> I built a course that can't be cheated. Here's the trick.

**Body:**
Every "do the work" course has the same hole: the answer key lives in the browser. Open DevTools, read the JSON, fake the credential. Done.

So when I built BuggyShop's grading for QA Mastery, I made one rule: **the answer key never touches the browser.**

How it works:
- BuggyShop ships with real seeded bugs — known, intentional, documented on the server.
- You explore the app, find a bug, file a real bug report.
- Your report gets sent to the server and graded against the answer key *there*.
- The browser only ever sees pass/fail + feedback. Never the key.

You can't inspect-element your way to a passing grade. The only way through is to actually find the bug and write it up well — which is, conveniently, the actual skill employers pay for.

This was the hardest part to get right, and the part I'm proudest of. A QA cert means nothing if the assessment itself has a security hole. (A little ironic to ship a QA product with a faked-grade vulnerability, no?)

Solo founder, building this in the open. Ask me anything about the architecture below.

**First comment:**
Poke at BuggyShop and the grader here: https://qa-mastery-platform.vercel.app — and yes, you're welcome to try to break the grading. That's kind of the point.

---

### Friday — LinkedIn (ENGAGE / CTA)

**Hook:**
> Reply with the worst bug you've ever found in the wild. I'll go first.

**Body:**
Best way to learn QA is to study real bugs. So let's build a thread of them.

Mine: an e-commerce site where applying a coupon recalculated the subtotal but not the tax line, so the final charge was *lower* than the displayed total. Nobody complained — customers were getting undercharged. Finance found it three months later.

That's the kind of bug that doesn't throw an error, doesn't crash anything, and slips past "click around and see if it works" testing. You only catch it if you check the *math*, not just the screen.

That class of bug — silent, logic-level, money-related — is exactly what I seed into BuggyShop. No red error banners. Just wrong behavior that looks fine until you verify it.

Your turn. Drop the gnarliest bug you've found (or shipped, no judgment) in the comments. The weirder, the better — and the more useful for everyone learning.

**First comment:**
If hunting that kind of bug sounds fun rather than stressful, you might like this: https://qa-mastery-platform.vercel.app
First module of each track is free.

---

### Community — Reddit r/QualityAssurance (TEACH / soft CTA)

**Title / Hook:**
> The skill that got me hired wasn't testing. It was writing the report afterward.

**Body:**
I've been mentoring a few career switchers and noticed the same blind spot every time: they get good at *finding* bugs way before they get good at *reporting* them. And in interviews, the report is what gets judged — because anyone can say "it's broken," but a clean repro proves you can think.

A few things I drill that consistently move people from "junior who found a bug" to "junior I'd actually hire":

- **Always reproduce from a clean state** before filing. Half of "bugs" vanish on a fresh session — that's data too, write it down.
- **Separate Expected from Actual.** If you can't articulate Expected, you don't understand the feature yet.
- **Attach evidence that survives.** Console error text > a screenshot of a console error. Network response body > "it didn't load."
- **Severity ≠ priority.** A typo on the legal page can be high priority before an audit. Learn to argue both.
- **One bug per report.** Bundling three issues into one ticket is how two of them never get fixed.

For practice, I ended up building a deliberately broken shop app with seeded bugs that grades your reports server-side (so you find out if your repro actually holds up, instead of guessing). But honestly even without any tool, just rewriting your last five bug reports against the checklist above will make a visible difference.

What's a bug-report habit that you wish someone had taught you on day one? Genuinely want to add to my list.

*(Mods — happy to drop the tool link only if it's welcome here; left it out of the post to keep it value-first.)*

---

## WEEK 3

### Monday — LinkedIn (TEACH)

**Hook:**
> Severity and priority are not the same word. Mixing them up gets bugs ignored.

**Body:**
This trips up almost every new tester, and it shows in interviews.

**Severity** = how badly the bug breaks the product. A technical judgment.
**Priority** = how soon we should fix it. A business judgment.

They move independently. Four real combinations:

- **High severity, high priority:** checkout charges the wrong amount. Drop everything.
- **High severity, low priority:** a crash in an admin tool only two internal users touch, with a known workaround. Bad, but not urgent.
- **Low severity, high priority:** the CEO's name is misspelled on the homepage the day before a press launch. Trivial bug, fix it now.
- **Low severity, low priority:** padding is 2px off on a settings page nobody screenshots. Backlog it.

As a tester you *assign severity* (you know the product impact) and you *argue for priority* (you give the business the context to decide). Good testers do both. Great testers know which one is theirs to own.

In BuggyShop, the seeded bugs span all four quadrants on purpose — so you practice the judgment call, not just the find. A cosmetic bug and a money bug should not get the same writeup, and the grader knows the difference.

Which quadrant do you think gets mishandled most in real teams? I'd argue "high severity, low priority" — because "high severity" makes everyone panic and reprioritize badly.

**First comment:**
Practice classifying real seeded bugs (free first module): https://qa-mastery-platform.vercel.app

---

### Wednesday — LinkedIn (BUILD-IN-PUBLIC)

**Hook:**
> A learner found a bug in BuggyShop I didn't put there. Here's what I did.

**Body:**
The whole premise of BuggyShop is *deliberate* bugs — a known set of seeded defects, graded against an answer key on the server.

This week someone reported a bug that wasn't on my list.

First reaction: mild panic. Second reaction: this is the most QA thing that could possibly happen. I built a broken app on purpose and still shipped an *accidental* bug into it. The app is so on-brand it's testing me.

What I'm doing about it:
- Reproduced it from a clean state (practice what I preach).
- Decided severity/priority — it's low severity, but I'm treating it as high priority because trust in the grader is the whole product.
- Adding it to the seeded set with a proper answer-key entry, so the next person who finds it gets credit instead of confusion.
- Crediting the learner who found it.

This is the part of building in public I actually like: the product's flaws become content, and the people using it make it better. A QA platform whose author refuses to admit bugs would be a bad joke.

Solo-building this. If you've ever shipped a bug into your own bug-finding tool, tell me I'm not alone.

**First comment:**
See BuggyShop (and try to find one I *didn't* mean to ship): https://qa-mastery-platform.vercel.app

---

### Friday — LinkedIn (DIFFERENTIATE / CTA)

**Hook:**
> You can't learn to swim by watching swimming. You're not learning QA by watching QA.

**Body:**
The internet is full of QA "courses" that are really just video playlists. You watch someone else test for six hours, take a quiz, get a certificate, and then freeze the first time a real app is in front of you — because you've never actually done it.

QA Mastery's entire bet is the opposite: **you don't watch testing, you do it.**

What that means concretely:
- A real, deliberately broken e-commerce app (BuggyShop) — not slides about one.
- You find real bugs and file real bug reports, in the format real teams use.
- Server-side grading against a real answer key, so feedback is honest — you can't fool it, and it can't flatter you.
- Free first module of every track, so you can find out today whether you actually like this work before paying anything.

The career switchers who succeed aren't the ones who watched the most content. They're the ones who can walk into an interview and say "here are five bugs I found and the reports I wrote." That's a portfolio. A certificate of completion is not.

If you've been collecting tutorials and still don't feel ready: that feeling is the problem this is built to fix. Go do one.

**First comment:**
Free first module, no card: https://qa-mastery-platform.vercel.app
Pick a track — first QA job, or manual-to-automation — and start with an actual bug.

---

### Community — Ministry of Testing (DIFFERENTIATE / discussion, soft CTA)

**Title / Hook:**
> Does "practice on a deliberately broken app" actually beat "test a real app" for learning?

**Body:**
Genuine question for this community, because I've gone back and forth on it.

When people learn manual testing, the usual advice is "go test a real website." And it works to a point — but real sites have two problems for a learner: (1) you never know if the weird thing you found is a real bug or intended behavior, so you get no clean feedback signal, and (2) the most instructive bugs (silent logic/data bugs) are rare and hard to stumble onto.

The alternative is a deliberately broken practice app with a *known* set of seeded bugs, where your bug report can be checked against an answer key. You trade realism ("it's a sandbox") for feedback quality ("you find out if your repro actually holds").

I've been building in that second direction — a broken shop app, grading reports server-side so the answer key can't be read from the browser — and I keep wondering if I'm over-indexing on the feedback loop at the expense of messy real-world realism.

So I'll put it to people who've trained testers:
- For a true beginner, which gives a better foundation — sandbox-with-answer-key, or real-app-with-ambiguity?
- Is there a point where the seeded sandbox stops helping and you *have* to throw someone at a real, undocumented app?

Not trying to pitch — genuinely want the pushback, because it shapes what I build next.

*(Happy to share the project link in a comment if folks are curious, but keeping the post about the question.)*

---

## WEEK 4

### Monday — LinkedIn (TEACH — automation track)

**Hook:**
> Your first Selenium test should fail. On purpose.

**Body:**
For the manual testers moving into automation: the scariest part is writing the very first script. So let's demystify it with the one thing manual testers already understand — a test case.

A Selenium/Java test is just your manual steps, written for a robot:

1. **Arrange** — open the browser, go to the page (your "clean state").
2. **Act** — drive the app: click, type, submit (your "steps to reproduce").
3. **Assert** — check the result against expected (your "Expected vs Actual").

The mistake beginners make: they write a test, it passes, and they trust it. But a test that has *never failed* is not proven — it might be asserting nothing useful.

So before you trust any automated check, make it fail once. Change the expected value to something wrong and confirm it goes red. If it stays green, your assertion is fake and your test is decoration.

That's the whole mental bridge from manual to automation: you already know what to check. Selenium is just the hands. Java is just the grammar.

In the automation track, you point Selenium at BuggyShop — the same broken app you tested by hand — and write checks that catch the seeded bugs automatically. Manual skills don't get thrown away. They get amplified.

Manual testers moving to automation: what's the one thing that's been stopping you from starting?

**First comment:**
The manual-to-automation track (Java/Selenium against BuggyShop) starts free: https://qa-mastery-platform.vercel.app

---

### Wednesday — LinkedIn (PROOF — template, fill before posting)

**Hook:**
> [Number] people have filed bug reports in BuggyShop this month. Here's what the data says about how beginners think.

> ⚠️ FOUNDER: only post this once the numbers are real. Replace every bracket. If you don't have the data yet, skip to the alt version below.

**Body:**
Since launch, learners have filed `[NUMBER]` graded bug reports against BuggyShop. Because grading happens server-side against an answer key, I get something most courses never see: data on *how* beginners actually test.

A few patterns from the graded reports:

- The most-missed bug so far is `[BUG NAME / MODULE]` — `[X]%` of people walked right past it. My read on why: `[ONE-SENTENCE REASON]`.
- The field people most often leave weak is `[FIELD, e.g. "Expected result"]`. `[SHORT OBSERVATION]`.
- The bug people find *fastest* is `[BUG NAME]`, usually within `[TIME / ATTEMPTS]`.

What's striking: the bugs people miss aren't the hard ones. They're the *quiet* ones — the logic and data bugs that don't throw an error. That matches what I see in hiring: juniors catch crashes, seniors catch silent wrong behavior.

I'll keep sharing this as the dataset grows. Building in public means showing the numbers, not just the wins.

**Alt version (use if you don't have numbers yet):**
> Hook: "I'm about to have data no QA course usually has — and I want to tell you up front what I expect to be wrong about."
> Body: Because BuggyShop grades reports server-side, I'll soon be able to see which seeded bugs beginners miss most. My prediction before the data comes in: the most-missed bug will be the silent pricing/logic one, not any crash — because beginners test the screen, not the math. I'm posting this prediction *now* so I can be publicly right or wrong later. Builder's accountability. I'll report back with real percentages once `[N]` reports are in.

**First comment:**
Add your report to the dataset (free first module): https://qa-mastery-platform.vercel.app

---

### Friday — LinkedIn (ENGAGE / CTA — challenge)

**Hook:**
> A 20-minute challenge: find one real bug today and write the report. I'll review the first 10 in the comments.

**Body:**
Enough scrolling. Let's do the actual work, together, today.

The challenge:
1. Open BuggyShop (the free first module — no card).
2. Find one bug. Any severity counts.
3. Write the report: Title, Steps to reproduce, Expected, Actual, Evidence, Severity.
4. Post your report (or a screenshot of it) in the comments.

I'll personally review the first 10 — same way I'd review a junior's first ticket. Honest, specific, kind. You'll find out fast whether your repro holds and your Expected/Actual are clear.

Why bother? Because "I did a QA course" is forgettable in an interview. "Here's a bug report I wrote, walk you through my reasoning?" is not. This is how you start a portfolio with zero experience — one real report at a time.

Career switchers especially: this is your low-risk first rep. Twenty minutes. Worst case you learn the format. Best case you start a portfolio today.

Drop yours below. Let's see them.

**First comment:**
Here's BuggyShop to do the challenge: https://qa-mastery-platform.vercel.app
Post your report here and tag me — I'll review the first 10.

---

### Community — Reddit r/QualityAssurance (BUILD-IN-PUBLIC / PROOF, soft CTA)

**Title / Hook:**
> I built a bug-reporting trainer that grades you server-side so the answer key can't be cheated. One month in — what I got wrong.

**Body:**
A month ago I started building a QA learning tool because I was tired of "courses" that are just video playlists with a quiz. The idea: a deliberately broken e-commerce app with seeded bugs, where you file real bug reports and they get graded *on the server* against an answer key — so the key never reaches the browser and you can't inspect-element a passing grade.

What's working better than expected:
- Server-side grading creates an actual feedback loop. People find out if their repro holds, not just whether they "found something."
- The silent logic/data bugs are the best teachers. People breeze past the crashes and miss the quiet money bugs — which is exactly the gap I see when interviewing juniors.

What I got wrong:
- I underestimated how much beginners struggle with *Expected vs Actual* specifically. Finding the bug isn't the hard part; articulating what *should* have happened is.
- I shipped an accidental, unseeded bug into my own bug-training app (yes, I know). A learner found it. Most on-brand failure possible.
- Grading bug reports is genuinely hard — free-text repro steps don't map cleanly to an answer key, and I'm still tuning how forgiving to be.

Posting partly to be accountable in public, partly because this sub has trained more testers than I ever will and I want the criticism: **for those of you who mentor juniors — is "graded practice on a sandbox" a real substitute for messy real-app experience, or just a better on-ramp before the real thing?**

Solo founder, QA background, building in the open. Happy to share the link in a comment if it's allowed here — kept the post focused on the lessons since that's the useful part.

---

## Quick reference: pillar rotation used

| Week | Mon (teach) | Wed (build/proof) | Fri (engage/CTA) | Community |
|------|-------------|-------------------|------------------|-----------|
| 2 | Teach (report anatomy) | Build-in-public + proof (uncheatable grading) | Engage (worst-bug thread) | Teach (report habits) |
| 3 | Teach (severity vs priority) | Build-in-public (accidental bug) | Differentiate (do, don't watch) | Differentiate (discussion) |
| 4 | Teach (first Selenium test) | Proof (graded-report data — template) | Engage (20-min challenge) | Build-in-public + proof (1-month retro) |

All five pillars (teach, differentiate, build-in-public, proof, engage) appear across the three weeks. The only post containing invented-looking specifics is the Week 4 Wednesday proof post, which is intentionally a fill-in template with an alt no-data version so nothing fake gets published.
