# Track A — Ready-to-Paste Posts (Notes v2, Modules 1–4)

**What actually shipped** (this is the ground truth — don't claim more than this):

| Module | Chapters | Notes |
|---|---|---|
| 1. How a computer works | 5 | 20 |
| 2. Operating systems & files | 5 | 20 |
| 3. The internet & the web | 5 | 20 |
| 4. The web platform for testers | 2 of 4 live (JS + rendering) | 8 |
| **Total live** | | **68** |

Every note carries the same 18 sections: a hook, an analogy, a real image with
tappable hotspots, a playable animated diagram, a **runnable** code playground, a
first-timer checklist, a "when it breaks" troubleshooter, a worked example, a quiz,
flashcards, and a challenge.

Module 4's HTML and CSS chapters are **not live yet.** Do not post about them.

> Same rules as `week-1-posts.md`: LinkedIn links go in the **first comment**.
> Reply to every comment inside two hours. Native upload video everywhere.

---

## MON — LinkedIn — Teach (the strongest post in this batch)

```
A junior tester writes: "the checkout button doesn't work."

A senior tester writes: "POST /api/charge fires twice on a single click — the
button's click handler and the form's submit handler both call the payment API.
POST isn't idempotent, so the customer is charged twice."

Same bug. Same thirty seconds of clicking. Same person, six months apart.

The difference isn't talent. It's that the second one knows a click doesn't stop
at the button — it bubbles up through every ancestor, and any of them can react.
One physical click can run five pieces of code written by five people who never
met.

You can learn that in an afternoon. Nobody teaches it, because it sits in the gap
between "learn to code" and "learn to test."

So I wrote it down. 68 free notes, and every one of them ends with you being able
to do something you couldn't do before.

What's the vaguest bug report you've ever received? I'll rewrite it in the
comments.
```

**First comment:** `The events & handlers note (free, no signup for module 1): [domain]/notes`

---

## WED — LinkedIn — Build-in-public (the honest one; this style outperforms)

```
I shipped 68 notes this week and found three bugs in my own platform while doing it.

One of them was embarrassing.

Every "Run code" and "Mark complete" button on the site had white text on a green
background. Looked fine to me. Measured 1.72:1 contrast — a hard accessibility
failure. It had been broken for weeks.

The cause: a CSS design token that was never defined. Not "defined wrong" —
never defined at all. So the utility class silently didn't exist, the text fell
back to the default colour, and nothing failed. No build error. No test. No lint
warning. It just quietly shipped.

We found it because a second pair of eyes ran an automated accessibility scan on
a page I'd never asked anyone to check.

Then we wrote a test that fails loudly if any design token is used without being
declared. That test is worth more than the fix.

The bug you can see is never the expensive one. The expensive one is the one your
tooling was structurally incapable of noticing.

What's the bug your test suite could never have caught?
```

**First comment:** `Both the fix and the guard test are in the repo. Happy to share the test if it's useful to anyone.`

---

## FRI — LinkedIn — Engage/CTA

```
Quick test. No signup, no link — just answer in your head.

A user clicks Submit. Nothing happens.
The browser console shows no errors.
The Network tab shows no request was sent.

Where's the bug?

...

It's not the server — you can't get a failed response from a request that was
never made. It's not a crashed script — that would show a red error.

So the click never reached code that calls the API. Three candidates:
→ no event handler is attached yet (the page looks done but its JavaScript is
  still loading)
→ the button is disabled
→ something invisible is sitting on top of it, eating the click

That third one is real and common. An element with opacity: 0 is invisible, takes
up space, and is still fully clickable. Your screenshot shows a button. The
browser delivers the click to a ghost.

If you got that, you can debug most front-end bugs you'll ever meet.
If you didn't — that's exactly what the free notes are for.

Which of the three would you have checked first?
```

**First comment:** `[domain]/notes — Module 1 is free, no card.`

---

## Community post (Reddit r/QualityAssurance, dev.to, Discord — no CTA, pure value)

```
The one browser skill that separates junior from senior QA (and nobody teaches it)

Open DevTools. Look at the Network tab. Click the failing request. Read the
Response body.

That's it. That's the whole skill.

Because it answers the only question that matters: what did the server ACTUALLY
send?

- Server sent the right data, screen shows the wrong thing → front-end bug.
- Server sent the wrong data → back-end bug.

Ten seconds. No source code. No architecture knowledge. You just assigned the
ticket to the right person with evidence attached, and you did it before anyone
opened an editor.

The corollary that took me longer to learn: the client is untrusted. A disabled
button can be re-enabled in DevTools in two seconds. A `min="1"` on an input is
decoration. curl never loads your page at all.

So: find a form with a client-side rule, break it in the Elements panel, submit,
and watch the status code. If the server says 400, the developers did their job.
If it says 200, you just found a real bug in under a minute.

I've been writing this stuff down as free notes while learning it myself. Not
linking here — it's not that kind of post. Ask if you want it.
```

---

## Reel / Shorts script — "The click that charged twice" (~40s, vertical)

| Beat | On screen | VO / caption |
|---|---|---|
| 0–4s | A "Pay" button. One click. | "One click. Watch the Network tab." |
| 4–10s | Network panel: **two** identical POSTs, both 201. | "Two requests. Two charges. The customer clicked once." |
| 10–18s | Elements → Event Listeners: `click` on the button, `submit` on the form. | "The button has a handler. So does the form it's inside." |
| 18–28s | Animated DOM tree: click travels down, back up, fires twice. | "A click doesn't stop where you clicked. It bubbles up through every ancestor. Both handlers fire." |
| 28–34s | Terminal-ish text: `POST is not idempotent`. | "And POST isn't idempotent. Twice sent, twice created." |
| 34–40s | Notes page, the FlowAnimation playing. | "Nobody teaches this. So I wrote it down. 68 free notes." |

**Caption (all platforms):**
```
Your customer clicked once. They were charged twice. Here's why.

A click doesn't stop at the button — it bubbles up through every parent element,
and each one can react. Button handler fires. Form's submit handler fires. Both
call the payment API. POST isn't idempotent, so two charges exist.

Every senior tester knows this. Almost no course teaches it.

68 free notes, no signup for the first module. Link in bio.
```

---

## Email — to the 5-day course list (send after Track A goes live)

**Subject:** The bug that was invisible to our own tests

```
Hey —

Short one, and it's a confession.

While writing this week's notes I found an accessibility bug on our own platform.
Every primary button — Run code, Mark complete — had white text on green. 1.72:1
contrast. A hard failure. Nobody had noticed, including me, because it looked
fine.

The cause was a CSS variable that was never defined. Not wrong. Missing. So the
class silently didn't exist and the text fell back to a default. The build passed.
The tests passed. Nothing anywhere reported a problem.

That's the whole lesson of testing, in one bug: **the absence of a failure is not
evidence of correctness.** Your tooling can only tell you about the things it was
built to notice.

We fixed it, measured it (4.62:1 and 10.50:1 in the two themes), and then wrote a
test that fails if any design token is used without being declared. The test
matters more than the fix.

68 free notes are live now — computers, operating systems, the internet, and the
web platform. Module 1 needs no account.

Reply and tell me the bug your tests could never have caught. I read every one.

— Sajan
```

---

## Posting order

1. **Community post first** (no CTA, pure value — builds the reputation the rest spends).
2. **Wed build-in-public**, 48h later. Highest trust-per-word of anything here.
3. **Mon teach**, the following week.
4. **Reel** once the video is cut.
5. **Fri engage** to close the loop.
6. **Email** last, after at least one post has landed.

**Do not** post the Mon teach post and the reel in the same week — they use the same
bubbling story and it reads as repetition.
