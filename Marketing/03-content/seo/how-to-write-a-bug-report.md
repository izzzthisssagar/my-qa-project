---
title: "How to Write a Bug Report That Gets Fixed (With a Real Example)"
meta_description: "Learn how to write a clear bug report that developers actually fix. Includes a full real-world example, a reusable template, and a quality checklist."
slug: how-to-write-a-bug-report
status: draft
---

# How to Write a Bug Report That Gets Fixed (With a Real Example)

A bug report is a written record that tells a developer exactly what went wrong, how to reproduce it, and what should have happened instead. To write a good one, give it a specific title, numbered reproduction steps, the expected result, the actual result, and the environment you tested on — so a stranger can trigger the same bug without asking you a single question.

That last part is the whole game. The test of a bug report is not how detailed it looks; it's whether someone who has never seen the bug can reproduce it from your words alone. Everything below serves that single goal.

## What a bug report actually is

A bug report is a communication tool, not a complaint. Its job is to transfer the bug from your head into the developer's head with zero loss. A vague report ("checkout is broken") forces the developer to become a detective, and detective work is expensive — most "cannot reproduce" closures come from reports that skipped steps, not from bugs that don't exist.

### The 7 things every good bug report has

A good bug report contains these seven elements:

1. **Title** — a one-line summary that names the *what*, *where*, and *impact*.
2. **Steps to reproduce** — numbered, exact, starting from a known state.
3. **Expected result** — what *should* happen, per the spec or reasonable behavior.
4. **Actual result** — what *actually* happens, described literally.
5. **Environment** — browser/OS/device, app version or URL, account or test data used.
6. **Severity and priority** — how badly it breaks things, and how soon it needs fixing.
7. **Evidence** — screenshot, screen recording, console error, or network log.

If a report is missing steps or the expected/actual split, it isn't a bug report yet — it's a hint.

## How to write a bug report, step by step

Follow this order every time. It keeps you from filing duplicates and from filing "bugs" that are actually your own setup mistakes.

1. **Reproduce it twice.** Before writing anything, trigger the bug a second time from a clean state (new tab, logged out, fresh cart). If it only happens once, note that — intermittent bugs are real, but you must say so.
2. **Find the smallest path.** Strip out unrelated clicks. If the bug appears with 3 steps, don't file 9. The shortest reliable repro is the most valuable thing in the report.
3. **Write the title last-ish, but make it specific.** "Discount code field accepts expired codes and applies the discount" beats "coupon bug."
4. **Number the steps from a known starting point.** Start at "logged in as a standard user on the cart page," not "so I was checking out."
5. **Split expected vs actual explicitly.** Two labeled lines. This is where the developer instantly sees the gap.
6. **Capture evidence as you go.** Screenshot the broken state; open DevTools and copy any red console error or failing network request.
7. **Set severity honestly.** Don't mark everything Critical. Reserve it for data loss, security, crashes, or blocked core flows.
8. **Read it back as a stranger.** Could someone reproduce this with no access to you? If not, fix the gap before submitting.

## Bug report template you can copy

```
Title: [Where] [What happens] — [impact]

Environment:
- App / URL + version:
- Browser / OS / device:
- Account / test data:

Preconditions:
- (logged-in state, cart contents, feature flags, etc.)

Steps to reproduce:
1.
2.
3.

Expected result:
-

Actual result:
-

Severity: Critical / High / Medium / Low
Priority: P1 / P2 / P3

Evidence:
- Screenshot / recording link
- Console error / network log
```

## A real example: a working bug report

Here is the same template filled in for a realistic e-commerce bug — the kind you'd hit in a deliberately broken practice app like QA Mastery's BuggyShop.

```
Title: Cart total ignores quantity — subtotal stays at single-item
price when quantity is increased

Environment:
- App / URL: buggyshop (BuggyShop lab) — Cart module
- Browser / OS: Chrome 126 / macOS 14.5
- Account: standard test user (test-buyer-01)

Preconditions:
- Logged in as standard user
- Cart contains 1x "Aurora Desk Lamp" at $40.00

Steps to reproduce:
1. Open the Cart page with 1x Aurora Desk Lamp ($40.00) in the cart.
2. Click the "+" stepper next to the lamp to set quantity to 3.
3. Observe the line item and the order subtotal.

Expected result:
- Line item shows 3 x $40.00 = $120.00
- Subtotal updates to $120.00

Actual result:
- Quantity field correctly shows "3"
- Line item still shows $40.00
- Subtotal remains $40.00 (quantity is not multiplied into the total)

Severity: High
Priority: P1
Evidence:
- Screenshot: cart-qty3-subtotal-40.png
- Console: no errors; network shows POST /api/cart returns
  qty:3 but unitPrice not multiplied in `lineTotal` field
```

Notice what makes this work: a developer can drop a lamp in the cart, click "+" twice, and see the wrong number in under 30 seconds. The expected/actual split shows the exact dollar gap. The evidence even points at the likely culprit (`lineTotal` in the API response), which shortens the fix without overstepping into "here's how to code it."

## Common mistakes that get bugs rejected

| Mistake | Why it fails | Fix |
|---|---|---|
| Vague title ("it's broken") | Can't be triaged or searched for duplicates | Name the where, what, and impact |
| No steps, just a description | Developer can't reproduce | Add numbered steps from a known state |
| Expected and actual merged | Reader can't see the gap | Two separate labeled lines |
| Missing environment | "Works on my machine" standoff | Browser, OS, version, account |
| Everything marked Critical | Severity becomes meaningless | Reserve Critical for data loss/crash/blocked flow |
| Opinions instead of facts | Sounds like a feature request | Report behavior, not preferences |
| Multiple bugs in one report | Half get lost in tracking | One bug per report |

## Severity vs priority (they're not the same)

These two get confused constantly, so define them cleanly:

- **Severity** measures *technical impact* — how badly the bug damages the product (crash, data loss, cosmetic typo).
- **Priority** measures *business urgency* — how soon it should be fixed relative to everything else.

A typo in the footer is low severity. But if that typo is in your company name on the homepage, it can be high priority. Conversely, a rare crash in an admin tool used once a year may be high severity but low priority. State both, and don't assume they move together.

## How to know your bug report is good

Run it through this quick check before you submit:

- A stranger can reproduce it from the steps alone, with no access to you.
- The title would help you find this bug later in a list of 200.
- Expected and actual are separate, specific, and factual.
- Severity is honest, not inflated.
- There is at least one piece of evidence.
- It describes one bug, not three.

If all six are true, you've written a report a developer can act on immediately — which is the only metric that matters.

## Practice on real bugs, not hypotheticals

Reading about bug reports is like reading about swimming. The skill only sticks when you find a real, reproducible bug and write it up under realistic conditions — including the discipline of *not* knowing in advance what the bug is.

That's exactly what BuggyShop is for: a deliberately broken e-commerce app seeded with real bugs. You hunt them, file actual bug reports, and get graded server-side against a hidden answer key — so the feedback is real, not self-assessed. The first module of each track is free.

If you want to turn the template above into muscle memory, try the free BuggyShop lab on [QA Mastery](https://qa-mastery-platform.vercel.app) and file your first real bug report today. You don't watch testing. You do it.