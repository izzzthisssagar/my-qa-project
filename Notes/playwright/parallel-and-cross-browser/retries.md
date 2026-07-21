---
title: "Retries"
tags: ["playwright", "parallel-and-cross-browser", "track-d"]
updated: "2026-07-16"
---

# Retries

*retries: 2 re-runs a failing test up to twice more before calling it truly failed - and a test that only passes on a retry is reported as 'flaky,' not silently counted the same as a clean first-try pass.*

> A test that fails once in fifty CI runs due to a genuine one-off network blip isn't the same problem
> as a test that's actually broken. Retries let Playwright tell the two apart automatically - re-running
> a failure before giving up on it, and labeling the result "flaky" rather than quietly filing it next
> to a clean pass as if nothing happened.

> **In real life**
>
> A dartboard doesn't erase a missed throw when the next one lands in the bullseye - all three darts
> stay stuck in the board, visible, telling the truth about how many attempts it actually took. A player
> who hits the bullseye on the third throw did land it, but that's a genuinely different, worse result
> than landing it on the first throw, and a good scorer records both facts, not just the final outcome.

**Retries**: Retries in Playwright (the retries config option) automatically re-run a failed test up to a set number of additional times before marking it as truly failed. A test that fails on its first attempt but passes on a retry is reported with a distinct status - flaky - not simply counted as a normal pass, keeping the fact that something needed a second attempt visible instead of hidden. A test that fails on its first attempt AND every retry is reported as failed. The common convention is retries: 0 locally (so flakiness is seen immediately) and retries: 1 or 2 in CI (to absorb genuine transient infrastructure noise without masking it).

## What actually happens, attempt by attempt

```
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
  use: { trace: 'on-first-retry' },
});
```

- **Attempt 1 fails** — Playwright doesn't report a failure yet if retries remain; it re-runs the same
  test in a completely fresh context.
- **A later attempt passes** — the test is reported as **flaky**, a distinct status from a clean pass,
  specifically so the fact that it needed extra attempts stays visible in the report rather than
  disappearing.
- **Every attempt fails** — only then is the test reported as genuinely **failed**.
- **`trace: 'on-first-retry'`** pairs naturally with retries - the first retry attempt gets a full
  trace recorded, giving you real evidence for exactly the runs worth investigating.

> **Tip**
>
> Keep `retries: 0` locally even if CI uses 2. Seeing a failure immediately, once, while developing is
> far more useful than watching it quietly disappear on a local retry - the whole point of catching
> flakiness is catching it, not papering over it during the exact moment you're best positioned to
> investigate.

> **Common mistake**
>
> Treating a growing "flaky" count in CI reports as background noise to ignore rather than a queue of
> real problems to work through. Retries are explicitly a diagnostic signal, not a fix - a test that
> regularly needs its second or third attempt to pass has a real, findable cause (a race condition, a
> missing wait, a genuinely unreliable dependency) worth investigating, not silencing.

![Three darts stuck in a dartboard - one landed dead center in the bullseye, one landed just off-center near the bull's edge, and one landed further out on an outer scoring wedge, all three visibly still in the board at once](retries.jpg)
*Darts in a dartboard — Wikimedia Commons, public domain (David A. Tyo). [Source](https://commons.wikimedia.org/wiki/File:Darts_in_a_dartboard.jpg)*
- **The outer dart — attempt 1, a real miss** — This throw genuinely didn't land the target - the equivalent of a test's first attempt actually failing. Nothing hides that this happened.
- **The near-bull dart — attempt 2, closer but still not it** — Better, but still not the actual target - if this were the LAST attempt allowed, the test would report as genuinely failed, not flaky.
- **The bullseye dart — the attempt that actually succeeded** — This is what makes the difference between 'flaky' (eventually passed) and 'failed' (never passed) - one successful attempt, within the allowed retry count.
- **All three darts, still visibly stuck in the board** — Nothing about hitting the bullseye erased the two prior throws - the same reason a flaky-labeled test still shows its earlier failed attempt in the report, not just the final passing one.

**A test with retries: 2, from first failure to final status**

1. **Attempt 1 runs and fails** — A genuine, one-off network timeout, say.
2. **Retries remain (2 configured) - re-run automatically** — A completely fresh browser context, same test.
3. **Attempt 2 passes** — The underlying transient condition cleared on its own.
4. **Reported status: FLAKY, not passed** — The fact that attempt 1 failed stays visible in the report.
5. **If attempt 2 had also failed** — Attempt 3 (the last allowed retry) would run before a final FAILED status.

Retrying a failed attempt up to a limit, and honestly labeling whether the eventual success took more
than one try, is really just: attempt, check, retry if attempts remain, and report which kind of
outcome actually happened. Here's that shape as a small, generic simulation.

*Run it - retry a flaky operation up to a limit, and honestly label the outcome (Python)*

```python
import random

def flaky_operation(attempt):
    # succeeds on attempt 2 for this simulation, deterministically
    return attempt >= 2

def run_with_retries(max_retries):
    for attempt in range(1, max_retries + 2):  # attempt 1 + up to max_retries more
        print(f"attempt {attempt}...")
        if flaky_operation(attempt):
            status = "PASSED" if attempt == 1 else "FLAKY"
            print(f"  succeeded on attempt {attempt} -> status: {status}")
            return status
    print("  failed on every attempt -> status: FAILED")
    return "FAILED"

run_with_retries(max_retries=2)
```

Same retry-and-label logic in Java.

*Run it - retry a flaky operation up to a limit, and honestly label the outcome (Java)*

```java
public class Main {
    static boolean flakyOperation(int attempt) {
        return attempt >= 2; // succeeds on attempt 2, deterministically, for this simulation
    }

    static String runWithRetries(int maxRetries) {
        for (int attempt = 1; attempt <= maxRetries + 1; attempt++) {
            System.out.println("attempt " + attempt + "...");
            if (flakyOperation(attempt)) {
                String status = (attempt == 1) ? "PASSED" : "FLAKY";
                System.out.println("  succeeded on attempt " + attempt + " -> status: " + status);
                return status;
            }
        }
        System.out.println("  failed on every attempt -> status: FAILED");
        return "FAILED";
    }

    public static void main(String[] args) {
        runWithRetries(2);
    }
}
```

### Your first time: Your mission: watch a test earn a genuinely different status at each retry outcome

- [ ] Set retries: 2 in a scratch project's config, with trace: 'on-first-retry' — Also confirm your local retries stays 0 for regular development, only bumping to 2 for this exercise.
- [ ] Write a test that fails deterministically on its first run but passes after (e.g. checking a value from a counter file that increments each run) — Or simpler: use test.info().retry to branch behavior for this exercise only.
- [ ] Run it and read the report's status for that test — Confirm it says FLAKY, not PASSED.
- [ ] Open the trace captured on the first retry — Confirm it exists specifically because of on-first-retry, capturing exactly the attempt that failed.

You've now seen the three real statuses (passed, flaky, failed) produced directly instead of assumed.

- **A test's flaky rate keeps climbing week over week and nobody's investigating it.**
  Treat rising flaky counts as a backlog of real bugs, not ambient noise - each one has an actual, findable cause (race condition, timing assumption, real external dependency) worth triaging like any other defect.
- **retries is set high (4 or 5) 'just to be safe' in CI.**
  This is widely considered a smell, not a safety margin - it means paying (in CI time) for nondeterminism instead of fixing it. 1-2 retries is the common convention; anything higher usually means a genuinely broken test is being masked rather than absorbed.
- **A test passes locally every time but shows up as flaky only in CI.**
  This pattern often points to environment-specific timing (CI machines can be slower or more resource-constrained than a dev laptop) - check the trace from the first CI retry rather than assuming it can't be reproduced.
- **A teammate wants to just delete a test that keeps showing up as flaky instead of fixing it.**
  Deleting removes real coverage along with the annoyance - investigating the trace from its most recent flaky run (on-first-retry should have captured one) usually finds the actual cause faster than it seems.

### Where to check

- **The HTML report's status column** — distinguishes passed, flaky, and failed at a glance across an
  entire run.
- **`playwright.config.ts`'s `retries` value**, and whether it differs between local and CI
  (`process.env.CI ? 2 : 0` is the common pattern) — confirms exactly what's configured where.
- **The trace from a flaky test's first failed attempt** (via `trace: 'on-first-retry'`) — the direct
  evidence for what actually went wrong, not just that something did.
- **A dashboard or CI history of flaky-rate over time**, if the project tracks one — reveals whether a
  specific test's flakiness is worsening, stable, or already fixed.

### Worked example: a rising flaky count traced back to one real, fixable race condition

1. Over several weeks, the same "add to cart" test shows up as flaky roughly one run in eight -
   annoying, but each individual CI run still goes green after its retry, so it's easy to ignore.
2. A team lead finally opens the trace captured on the first-retry attempt for the most recent flaky
   occurrence.
3. The trace's network tab shows the cart count API response arriving about 200ms after the UI already
   rendered the (stale) old count - a genuine race condition between an optimistic UI update and the
   real server confirmation, not a Playwright timing issue.
4. The fix addresses the actual race in the app: the UI now waits for the real confirmation before
   updating the visible count.
5. The test's flaky rate drops to zero over the following weeks - the retries didn't fix anything by
   themselves, but they kept the evidence around (via the paired trace) that made finding the real fix
   possible.

**Quiz.** A test has been passing every CI run for months, but always as 'flaky' rather than a clean pass - it needs its retry roughly one time in ten. Is this something worth investigating, or is it fine to leave as-is since the suite is technically green every time?

- [ ] It's fine to leave as-is - a flaky status still counts as an overall pass, so there's no real problem
- [x] Worth investigating - 'flaky' is a distinct, deliberate status specifically because it represents a real, findable underlying cause (the note's examples: a race condition, a timing assumption, a genuine external dependency issue) that retries absorb but do not fix
- [ ] The retries count should simply be lowered to 0 to force the real failure to show clearly every time
- [ ] This is expected and unavoidable - all Playwright tests are flaky roughly one time in ten by design

*The note is explicit that retries are diagnostic, not curative - a persistently flaky (not just occasionally, but consistently needing a retry) test has a real cause worth finding, illustrated directly in the worked example's race condition. Option one treats the retry mechanism as if it were the fix rather than a safety net masking a real issue. Option three would make CI red intermittently without investigating anything, which doesn't help find the cause either - it just removes the safety net. Option four is false; flakiness is not an inherent, expected property of Playwright tests - it's a signal of a specific, fixable underlying issue.*

- **The three possible test outcomes with retries enabled** — Passed (succeeded on attempt 1), Flaky (failed at least once, then eventually passed within the retry limit), Failed (failed on every attempt including all retries).
- **Why keep retries: 0 locally even with retries: 2 in CI?** — Seeing a failure immediately during development is more useful than watching it silently disappear on a local retry - you're best positioned to investigate right when it happens.
- **Why is retries: 5 (or higher) considered a smell?** — It means paying CI time for nondeterminism instead of fixing it - the common convention is 1-2 retries; higher usually masks a genuinely broken test rather than absorbing real transient noise.
- **What pairs naturally with retries for diagnosing flakiness?** — trace: 'on-first-retry' - captures full evidence (DOM, network, console) from exactly the attempt that failed, without paying tracing cost on every clean pass.
- **The dartboard analogy for retries** — All three throws stay visibly stuck in the board - hitting the bullseye on the third throw is a real, different (worse) outcome than hitting it on the first, and a flaky status keeps that fact visible instead of erasing it.

### Challenge

Find (or create) a test with a real, fixable source of occasional flakiness (a race condition, a
missing wait). Run it enough times locally with retries: 0 to see it fail on its own. Then enable
retries: 2 with trace: 'on-first-retry' and run it until it shows up as flaky. Open that trace and
identify the actual root cause from the evidence alone - then fix the real issue and confirm the flaky
status disappears over several subsequent runs.

### Ask the community

> A specific test has been showing up as flaky roughly `[X]` times out of `[Y]` CI runs for a while now. Here's what the trace from its most recent flaky run shows: `[describe it]`.

Sharing the actual trace evidence from a real flaky occurrence (not just "it's flaky sometimes")
usually gets a much faster, more specific answer than describing the symptom alone.

- [Playwright — official Retries docs](https://playwright.dev/docs/test-retries)
- [Better Stack — Avoiding Flaky Tests in Playwright](https://betterstack.com/community/guides/testing/avoid-flaky-playwright-tests/)

🎬 [Retries and Test Flakiness in Playwright — SDET Adda For QA Automation](https://www.youtube.com/watch?v=B2xvEk-EEvk) (10 min)

- retries: N re-runs a failing test up to N more times before reporting it as genuinely failed.
- A test that fails then eventually passes is reported as FLAKY - a distinct status from a clean pass, keeping the extra-attempt fact visible rather than hidden.
- The common convention: retries: 0 locally (see flakiness immediately), 1-2 in CI (absorb real transient noise); higher counts are a smell, not a safety margin.
- trace: 'on-first-retry' pairs naturally with retries, capturing real evidence from exactly the attempt that failed, at low ongoing cost.
- Retries are diagnostic, not curative - a persistently flaky test has a real, findable cause worth investigating, not background noise to tolerate.


## Related notes

- [[Notes/playwright/parallel-and-cross-browser/projects-and-browsers|Projects & browsers]]
- [[Notes/playwright/parallel-and-cross-browser/parallelism-and-sharding|Parallelism & sharding]]
- [[Notes/playwright/parallel-and-cross-browser/config|Config]]


---
_Source: `packages/curriculum/content/notes/playwright/parallel-and-cross-browser/retries.mdx`_
