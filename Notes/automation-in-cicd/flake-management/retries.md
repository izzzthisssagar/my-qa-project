---
title: "Retries"
tags: ["ci", "retries", "flaky-tests", "reliability", "track-d"]
updated: "2026-07-17"
---

# Retries

*Retries are a bounded diagnostic and resilience mechanism, not a flake fix; preserve every attempt, classify fail-then-pass separately, avoid retrying destructive work blindly, and cap the confidence cost.*

> A suite with one retry reports 99% green. Its first-attempt success is 73%. The dashboard celebrates
> reliability while developers wait for reruns and learn that red means “click again.” Retries did not
> restore trust; they made instability cheaper to ignore.

> **In real life**
>
> A RESET button can recover a machine from a transient state, but pressing it erases clues and may
> repeat half-completed work. A test retry is the same: useful when bounded and instrumented, dangerous
> when it repeats side effects or overwrites the first failure.

**Test retry**: A test retry is another attempt of the same logical test after an unexpected result. It should have a small explicit budget, isolated state, preserved attempt evidence, and separate outcome classification: passed first attempt, flaky (failed then passed), or failed all attempts. Retrying changes observed pipeline behavior; it does not remove the underlying nondeterminism.

## Treat the first failure as data

```ts
export default defineConfig({
  retries: process.env.CI ? 1 : 0,
  use: { trace: "on-first-retry" },
});
```

One retry may capture richer evidence and distinguish persistent from intermittent failure. Report
both attempts, fail CI on flaky results when policy requires, and never call fail-pass simply “passed.”

> **Tip**
>
> Retry at the narrowest safe layer. A retrying assertion that polls a read-only condition is different
> from replaying an entire checkout that may create a second order.

> **Common mistake**
>
> Increasing retries until the pipeline looks green. If each independent attempt fails with probability
> 20%, three total attempts hide the failure 99.2% of the time while tripling worst-case cost.

![A dusty black industrial push button labeled RESET](retries.jpg)
*RESET — Lukas Large, CC BY-SA 2.0. [Source](https://commons.wikimedia.org/wiki/File:RESET_(5628279223).jpg)*
- **Explicit action** — A retry should be intentional, bounded, and visible—not an invisible loop.
- **Old state** — Dust and residue represent state that must be isolated or cleaned before another attempt.
- **Side effects** — Resetting can replay destructive work; use idempotency and unique data.
- **First evidence** — Preserve the original failure before recovery changes the environment.

**A safe bounded retry**

1. **Attempt one fails** — Capture error, trace, logs, seed, state, and environment before cleanup.
2. **Policy evaluates** — Is this error retryable, budget available, and operation safe to repeat?
3. **State is isolated** — New context/data or verified idempotency prevents duplicate side effects.
4. **Retry executes** — Record a new attempt ID under the same logical test.
5. **Outcome is classified** — Pass-first, flaky fail-pass, or persistent failure—not one collapsed boolean.
6. **Debt is routed** — Flaky outcome creates owned evidence even when the pipeline continues.

*Run it — show how retries hide a failure probability (Python)*

```python
``p_fail = 0.20
for total_attempts in (1, 2, 3):
    visible_failure = p_fail ** total_attempts
    print(f"attempts={total_attempts} visible_failure={visible_failure:.1%} hidden_by_recovery={1-visible_failure:.1%}")``
```

*Run it — show how retries hide a failure probability (Java)*

```java
``public class Main {
    public static void main(String[] args) {
        double pFail = 0.20;
        for (int attempts = 1; attempts <= 3; attempts++) {
            double visible = Math.pow(pFail, attempts);
            System.out.printf("attempts=%d visible_failure=%.1f%% hidden_by_recovery=%.1f%%%n",
                attempts, 100 * visible, 100 * (1 - visible));
        }
    }
}``
```

### Your first time: Your mission: audit one retry policy

- [ ] Find every retry layer — Assertion, test, job, workflow, client, proxy, and manual rerun can multiply.
- [ ] Classify safety — Check side effects, idempotency, fresh data/context, and cleanup.
- [ ] Preserve all attempts — Prove the first error and each later trace remain available.
- [ ] Expose confidence cost — Report first-pass, flaky, final failure, added time, and retry budget.

You now know whether retries diagnose instability or merely conceal it.

- **Only the final green result appears.**
  Configure attempt-aware reporting and store first-attempt evidence separately.
- **A retried test creates duplicate records.**
  Use idempotency keys, unique attempt data, verified cleanup, or do not retry the whole operation.
- **One failure triggers many more than configured retries.**
  Inventory nested framework, job, workflow, HTTP-client, and manual retry layers; define one total budget.
- **Retry cost makes CI much slower.**
  Measure added wall time by fingerprint, cap attempts, fail fast for deterministic errors, and fix/quarantine the cause.

### Where to check

- **Framework and CI config** — every retry layer and total attempt budget.
- **Attempt report** — first, retry, and final classifications.
- **Artifacts per attempt** — original evidence not overwritten.
- **Data/idempotency records** — duplicate side effects.
- **Dashboard** — first-pass gap, retry rate, and lost time.

### Worked example: a retry that creates two orders

1. Checkout submits an order, but the UI response times out before the confirmation appears.
2. Whole-test retry uses the same user but no idempotency key and submits again.
3. Attempt two passes; CI reports green while two orders exist.
4. The team stops whole-flow retry, adds an idempotency key, and polls the first order's status.
5. A single diagnostic retry remains for safe read-only assertions, with both attempts visible.

**Quiz.** When is a retry most defensible?

- [ ] Whenever it makes CI green
- [x] For a bounded, safe-to-repeat attempt that preserves evidence and remains classified as flaky after fail-pass
- [ ] For every destructive end-to-end flow
- [ ] Instead of investigating flakes

*A retry can aid diagnosis or tolerate a known transient boundary only when bounded, observable, and safe. It never converts instability into a clean pass.*

- **Retry budget** — Maximum attempts across all nested retry layers.
- **Flaky outcome** — At least one failed and one passed attempt for the same logical test execution.
- **Idempotency** — Repeating an operation has no additional unintended effect.
- **First-pass rate** — Share of cases successful without any retry.
- **Retry amplification** — Nested retry layers multiplying attempts, cost, and side effects.

### Challenge

Map every retry layer in one pipeline and compute maximum attempts. Force a fail-pass case and a
destructive timeout; prove first evidence survives and that repeated execution cannot duplicate state.

### Ask the community

> Test [ID] uses retry layers [list] with total budget [n]. Attempt statuses/evidence are [values], operation safety/idempotency is [evidence], and first-pass/final rates are [values].

This exposes hidden amplification and whether recovery is trustworthy.

- [Playwright Docs — test retries](https://playwright.dev/docs/test-retries)
- [Playwright Docs — traces on first retry](https://playwright.dev/docs/trace-viewer-intro)

🎬 [How To Retry Failed Test Cases: Retries and Test Flakiness — SDET-QA](https://www.youtube.com/watch?v=DUZN6j0W0UU) (14 min)

- Retries recover or diagnose; they do not fix nondeterminism.
- Preserve each attempt and classify fail-pass as flaky, never simply passed.
- Audit nested retry layers and enforce one small total budget.
- Retry only safe/idempotent work with isolated state.
- Measure first-pass gap, added time, and side effects so green cannot hide confidence loss.


## Related notes

- [[Notes/automation-in-cicd/flake-management/detecting-flakes|Detecting flakes]]
- [[Notes/automation-in-cicd/flake-management/quarantine|Quarantine]]
- [[Notes/automation-in-cicd/scheduling-and-reporting/publishing-reports|Publishing reports]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/flake-management/retries.mdx`_
