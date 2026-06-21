# Week 1 — Ready-to-Paste Posts

Copy these as-is, swap `[domain]` and any `[X]` placeholders, post. Schedule: Mon / Wed / Fri + 2 community posts. Reply to every comment in the first 2 hours.

> Reminder: on LinkedIn the **link goes in the FIRST COMMENT**, not the post body (the algorithm suppresses outbound links). Each post below gives you the first-comment text too.

---

## MON — LinkedIn — Launch (pair with `04-designs/asset-1-launch.html`)

```
QA Mastery is live. And I built it because I was tired of one thing.

You can watch 100 hours of Selenium tutorials and still freeze on day one of the job.

Watching someone test isn't testing. Nobody grades your bug reports. Nobody tells you what to test.

So I built a platform where you actually do the work:
→ A real (deliberately broken) shop called BuggyShop
→ You find the seeded bugs and file real bug reports
→ You get graded — like an actual QA job

No videos to passively watch. You learn by doing.

The first module of each track is free. I'd genuinely love your feedback — tell me what's missing and I'll build it.

You don't watch testing. You do it.
```
**First comment:** `Try the free first module here 👉 [domain] — and reply with what you'd want next.`

---

## WED — LinkedIn — The BuggyShop story (build-in-public)

```
I built a shop that's broken on purpose. Here's why.

Every junior tester asks the same thing in QA communities: "Where do I actually practice?"

The usual answers — saucedemo, the-internet — are fine, but they're disconnected. Nobody tells you WHAT to test, and nothing checks if you did it right.

So QA Mastery has BuggyShop: an e-commerce app with real, seeded bugs hidden inside it. Known bug IDs on the server. When you file a report, it gets graded against the real answer key — and the answer key never reaches your browser, so you can't cheat your way to a certificate.

That last part matters. A credential only means something if it can't be faked.

This is the difference between "I watched a course" and "here's a graded portfolio of bugs I found."

What would make a practice environment genuinely useful for you? I'm building from your answers.
```
**First comment:** `Free first module 👉 [domain]`

---

## FRI — LinkedIn — Engage / poll (feeds the feedback loop)

```
Quick one for anyone learning QA 👇

What's the ONE thing blocking you from your first QA job (or your next level)?

A) I don't know what to learn or in what order
B) I can't get hands-on practice
C) I freeze in interviews
D) Something else (tell me below)

I read every reply — and a lot of them turn into things I build next.
```
**First comment:** `If you want a structured, hands-on path: [domain] (first module free).`

(LinkedIn natively supports polls — use the poll feature for A–D, or post as text and let people reply.)

---

## Community post #1 — Reddit r/QualityAssurance or r/softwaretesting

> ⚠️ Read each sub's self-promo rules first. Spend a few days answering questions before you post this. Lead with the free value, not the signup.

**Title:** `Made a free practice app with seeded bugs that grades your bug reports`

```
A question that comes up here constantly is "where do I actually practice testing?" The usual practice sites are good but disconnected — nothing tells you what to test or checks your work.

I built a free practice environment to fix that: a deliberately buggy e-commerce app (BuggyShop) with real seeded bugs. You find them, write a proper bug report, and it gets graded against the known issues.

Sharing it because I genuinely want feedback from people learning QA — what's missing, what's confusing, what you'd want next. First module is free, no catch.

Also happy to just share my bug-report template separately if that's more useful — it works on any practice site.
```
*(Drop the link only if the sub allows it; otherwise offer it when people ask in comments.)*

---

## Community post #2 — Ministry of Testing / Discord / Telegram (#resources or #show-your-work)

```
Built something for people learning QA and would love this community's eyes on it.

It's a learning platform where every concept has a hands-on lab on a built-in buggy app, and your bug reports get graded server-side (answer key never ships to the client, so the grading actually means something).

Still early — I'm shipping based on feedback every week. If you have 10 minutes and brutal honesty, I'd really value it. What would make this credible/useful to you?
```

---

## After you post (every time)
1. Reply to every comment within ~2 hours.
2. Log new signups + their source in `01-action-plan/targets-and-metrics.md`.
3. Paste any feedback/requests into `02-feedback-loop/feedback-intake.csv`.
4. Friday: run `feedback_triage.py`, pick the #1 thing to ship next week.
