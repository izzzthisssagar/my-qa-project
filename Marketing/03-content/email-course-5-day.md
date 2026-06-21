# 5 Days to Your First Graded Bug Report

A free email course from QA Mastery. *You don't watch testing. You do it.*

---

## Signup-Page Blurb

**5 Days to Your First Graded Bug Report.** Most people "learn QA" by watching someone else click around in a video. Five days later, they still can't do the one thing every QA job requires: find a real bug and write it up so a developer can fix it. This free 5-day email course is the opposite. Each day you take one small, concrete action — and by Day 5 you'll have filed a real bug report on QA Mastery and had it graded server-side against a real answer key (not a quiz, not a checkbox — actual QA work). No experience needed. No fluff. Just you, doing the job. Drop your email and start tomorrow.

---

## Opt-In Confirmation Email

**Subject:** Confirm your spot — Day 1 lands the moment you click

**Preview text:** One click and you're in. Here's what the next 5 days look like.

**Body:**

Almost there.

To make sure this is really you (and to keep your inbox clean), tap the button below to confirm. Day 1 arrives the second you do.

**[Yes — start my 5-day course]**

Here's the deal you just signed up for. Over the next five days, you won't watch a single video. Instead:

- **Day 1** — What a bug actually is (and why most beginners get this wrong)
- **Day 2** — The anatomy of a bug report a developer will thank you for
- **Day 3** — Find your first real bug on a practice app
- **Day 4** — Write it up and self-check it like a pro
- **Day 5** — File it on QA Mastery and get it graded for real

One email a day. One small action a day. By Friday you'll have done something most "QA students" never do: filed a real, graded bug report.

If you didn't sign up for this, just ignore this email — nothing happens until you confirm.

See you in Day 1.

— The QA Mastery team
qa-mastery-platform.vercel.app

*Didn't sign up? No action needed; you won't hear from us again.*

---

## Day 1 — Mindset + What a Bug Really Is

**Subject:** Day 1: A bug is not "the app is broken"

**Preview text:** The one sentence that separates testers from button-clickers.

**Body:**

Welcome to Day 1. Let's kill the biggest myth first.

A bug is not "something went wrong." A bug is **a gap between what the software actually does and what it's supposed to do.** That second half — "supposed to do" — is the whole job. Anyone can notice a page looks weird. A tester can say *exactly* what the correct behavior was and prove the software didn't deliver it.

Here's the mindset shift that changes everything: you are not trying to use the app. You are trying to *catch* the app. Every screen is making a promise — "click this and you'll get that." Your job is to find the promises it quietly breaks.

This is why testing is a skill you do, not watch. You can't absorb suspicion from a video. You build it by poking at real things and noticing when reality and expectation drift apart.

Good testers aren't negative people. They're precise people. "It's broken" gets ignored. "I expected the cart total to update when I removed an item; it stayed at $40" gets fixed.

You don't need any tools today. You don't need to know code. You just need to start seeing software as a set of promises waiting to be checked.

**Your action today (5 minutes):** Open any app or website you used this week. Find one thing that surprised you — a button that did nothing, a number that looked off, a confusing message. Write one sentence: *"I expected X, but it did Y."* That's your first bug observation. That's the whole foundation.

Tomorrow: how to turn that one sentence into a bug report a developer actually respects.

**Soft CTA:** Curious where you'll practice this for real? Peek at BuggyShop, our deliberately broken store, at qa-mastery-platform.vercel.app — no pressure, just look around.

---

## Day 2 — Anatomy of a Great Bug Report

**Subject:** Day 2: The 6 parts of a bug report devs don't hate

**Preview text:** Steal this exact structure. It works in real jobs.

**Body:**

Yesterday you wrote "I expected X, but it did Y." Today we turn that into a real bug report — the document that is, quite literally, the deliverable of a QA job.

A great report does one thing: it lets a developer reproduce the bug **without talking to you.** If they have to ask "what did you click?", you've added a day of delay. Here's the structure that prevents that:

1. **Title** — Short and specific. Not "checkout broken." Try: *"Cart total doesn't update after removing an item."*
2. **Steps to reproduce** — Numbered. Start from a known point ("Log in as test user"). Each step is one action.
3. **Expected result** — What *should* happen. This is where beginners go quiet — don't. Be exact.
4. **Actual result** — What *did* happen. Just the facts.
5. **Environment** — Browser, device, account used. Bugs hide in specifics.
6. **Evidence** — A screenshot, a recording, an error message. Show, don't tell.

Notice what's *not* here: opinions, blame, guesses about the cause. Your job is to report symptoms precisely, not diagnose the code. "I think the database is wrong" makes you look junior. Clean repro steps make you look hireable.

The magic test for any report: hand it to a stranger. Can they reproduce the bug using only your words? If yes, you've done the job.

**Your action today (10 minutes):** Take the bug observation from Day 1 and rewrite it using all six parts above. Even if it's a tiny bug. Get the muscle memory now, before it counts.

Tomorrow: you go hunting for a real bug on purpose.

**Soft CTA:** Want a real one to practice on tomorrow? BuggyShop on qa-mastery-platform.vercel.app is seeded with genuine bugs waiting to be caught. Have a look before Day 3.

---

## Day 3 — Find Your First Bug on a Practice App

**Subject:** Day 3: Go break something (on purpose)

**Preview text:** A repeatable method for finding bugs, not just stumbling on them.

**Body:**

Today you stop waiting for bugs to appear and start hunting them. There's a difference between *noticing* a bug and *finding* one — and finding is a method you can repeat on any app, in any job.

Here's the beginner-friendly hunt:

**1. Pick one feature.** Not the whole app — one thing. A login form. A cart. A search box. Focus beats wandering.

**2. Use it the "right" way first.** Establish what normal looks like. You can't spot wrong until you know right.

**3. Then misbehave.** This is where bugs live:
- Leave required fields empty and submit.
- Type a negative number, or a huge one, where a quantity goes.
- Add an item, remove it, add it again. Watch the totals.
- Click the same button twice fast.
- Paste emoji or spaces into a name field.

**4. Watch for the gap.** Every time reality drifts from what you expected — that's a catch. Note it immediately, before you forget the exact steps.

The mistake beginners make is exploring randomly and hoping. Pros pick a target and apply pressure. You're not looking for *every* bug today. You're looking for **one** you can fully reproduce.

If you've got a QA Mastery account, BuggyShop is built exactly for this — real seeded bugs, no risk of breaking anything that matters. If not, any e-commerce demo or todo app will do for practice.

**Your action today (15 minutes):** Pick one feature on BuggyShop (or any practice app). Apply the four steps above. Find one bug and reproduce it twice from scratch. If you can trigger it on demand, you've got it.

Tomorrow: we write it up and self-check it like an interviewer would.

**Soft CTA:** BuggyShop's first module is free — start hunting now at qa-mastery-platform.vercel.app and bring your catch to Day 4.

---

## Day 4 — Write + Self-Check the Report

**Subject:** Day 4: Make your bug report bulletproof

**Preview text:** The 60-second self-check that catches your own mistakes.

**Body:**

You've got a bug. Now let's write it up so well that it would pass in a real sprint — and then we'll stress-test it before anyone else does.

First, write the full report using Day 2's six parts: **Title, Steps to reproduce, Expected, Actual, Environment, Evidence.** Don't rush the steps. The single most common reason a report gets bounced back is steps that "skip a beat" — they assume the reader already did something you forgot to mention.

Now the part that makes you look senior: **the self-check.** Before you submit anything, run this:

- **The cold-start test.** Do your steps begin from a known state (logged in? on the home page?), or do they assume context? Add the missing first step.
- **The stranger test.** Read only your steps — not your memory. Could someone reproduce it with zero help? If a step makes you mentally fill a gap, write that gap in.
- **Expected vs. Actual clarity.** Are these two genuinely *different* and *specific*? "It should work / it didn't work" fails. "Total should drop to $20 / total stayed $40" passes.
- **One bug per report.** Found two issues? That's two reports. Mixing them gets both ignored.
- **Evidence attached.** A screenshot with the wrong value circled beats a paragraph.

Tighten the title last, once you know exactly what the bug is. A precise title is the first thing that signals you know what you're doing.

This self-check *is* the professional habit. It's what separates a report that gets fixed from one that gets a "can't reproduce" and quietly dies.

**Your action today (15 minutes):** Finalize your bug report and run all five self-checks above. Fix every weak spot. When it survives the stranger test, it's ready.

Tomorrow: the real thing — you file it and get it graded.

**Soft CTA:** Tomorrow you'll submit on QA Mastery and get scored against a real answer key. Make sure you can log in at qa-mastery-platform.vercel.app tonight so Day 5 is smooth.

---

## Day 5 — Get It Graded on QA Mastery

**Subject:** Day 5: File it for real and get graded

**Preview text:** No quiz. No checkbox. A real bug report, scored against a real answer key.

**Body:**

This is the day. Everything so far was practice. Today you do the actual job: file a real bug report and have it **graded server-side against a real answer key** — the same kind of feedback loop that builds genuine QA skill.

Here's why this matters and why QA Mastery is built the way it is: the answer key never reaches your browser. You can't peek at it, and you can't fake the result. When your report gets graded, that grade *means something* — it reflects whether a real bug was caught and described well enough to act on. That's the difference between "I watched a QA course" and "I can do QA."

The first module of each track is free, so you can do this today at no cost. Here's the flow:

1. **Log in** to QA Mastery and open BuggyShop.
2. **Hunt** using your Day 3 method — pick a feature, establish normal, apply pressure.
3. **Write the report** with Day 2's six parts.
4. **Self-check** it with Day 4's five tests.
5. **Submit it** for grading and read the feedback closely. The feedback is the lesson.

Don't aim for perfect. Aim for *filed.* Your first graded report is a milestone most people who say they "want to get into QA" never reach. After it, you're not someone learning about testing. You're someone who tests.

When you get your grade, sit with the feedback. Then find another bug. The loop you just ran — hunt, write, check, submit, learn — is the entire craft. Everything else is reps.

**Your action today (20 minutes):** File one real bug report on BuggyShop and get it graded. That's it. That's the whole goal of these five days, done.

**Soft CTA:** Ready to make it count? Log in and file your first graded report now at qa-mastery-platform.vercel.app — then keep the streak going with the next bug.

---

*You don't watch testing. You do it. — QA Mastery, qa-mastery-platform.vercel.app*