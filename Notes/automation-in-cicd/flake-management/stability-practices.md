---
title: "Stability practices"
tags: ["ci", "test-stability", "isolation", "determinism", "track-d"]
updated: "2026-07-17"
---

# Stability practices

*Stable automation controls state, time, data, dependencies, selectors, resources, order, and observability so a failure reflects the product contract rather than accidental test conditions.*

> A team keeps adding waits to a flaky suite: two seconds after login, five after checkout, ten before
> asserting email. The suite becomes slower and still fails when CI is busy. They did not synchronize
> with product state; they synchronized with hope.

> **In real life**
>
> A gyroscope preserves orientation while the frame around it moves. Stable tests need similar anchors:
> observable business states, isolated contexts, controlled clocks/data, explicit dependency contracts,
> and evidence. Fixed sleeps anchor only to elapsed wall time, which is the part most likely to vary.

**Stable automated test**: Test stability is the property that materially equivalent conditions produce the same meaningful outcome. It is engineered through isolation, deterministic data and clocks, state-based synchronization, resilient user-facing or contract selectors, controlled dependencies, bounded resources, order independence, idempotent setup/cleanup, and enough telemetry to explain divergence.

## Remove uncontrolled variables systematically

```ts
await page.getByRole("button", { name: "Place order" }).click();
await expect(page.getByTestId("order-status")).toHaveText("Confirmed");
```

The assertion repeatedly observes the state that matters. `waitForTimeout(5000)` merely assumes the
state will exist by an arbitrary deadline and wastes all five seconds when it appears immediately.

> **Tip**
>
> Make each test able to run alone, in any order, and in parallel. Generate unique data, create state
> through supported APIs/fixtures, and start from a fresh browser/session/database namespace.

> **Common mistake**
>
> Mocking every dependency to obtain determinism. Mocks reduce variability but can drift from reality.
> Keep contract checks and a smaller number of controlled real integration paths.

![Foucault's brass gyroscope displayed beside an optical instrument](stability-practices.jpg)
*Foucault's gyroscope — Stéphane Magnenat, public domain. [Source](https://commons.wikimedia.org/wiki/File:Foucault%27s_gyroscope.jpg)*
- **Stable reference** — Assertions anchor to observable contract state rather than arbitrary elapsed time.
- **Isolation rings** — Fresh context, unique data, and cleanup prevent surrounding tests from changing the result.
- **Observation** — Logs, traces, metrics, and clocks let investigators see the first divergence.
- **Controlled base** — Pinned runtime, dependencies, resources, locale, timezone, and seed create comparable conditions.

**Engineering a stable test**

1. **Name the contract** — State the user/business behavior and authoritative observable outcome.
2. **Build isolated state** — Fresh context, unique data, idempotent setup, and scoped cleanup.
3. **Control boundaries** — Clock, random seed, dependencies, runtime image, locale, timezone, and resources.
4. **Synchronize by condition** — Wait for meaningful UI/API/event/database state, not fixed sleeps.
5. **Exercise hostile order** — Run alone, randomized, parallel, repeated, and under representative load.
6. **Retain evidence** — Trace the first divergence and trend stability continuously.

*Run it — poll a condition instead of sleeping blindly (Python)*

```python
``states = ["processing", "processing", "confirmed"]
for attempt, state in enumerate(states, start=1):
    print(f"poll {attempt}: {state}")
    if state == "confirmed":
        print("assertion passed on observed state")
        break
else:
    raise AssertionError("order never confirmed")``
```

*Run it — poll a condition instead of sleeping blindly (Java)*

```java
``import java.util.*;

public class Main {
    public static void main(String[] args) {
        var states = List.of("processing", "processing", "confirmed");
        boolean confirmed = false;
        for (int i = 0; i < states.size(); i++) {
            System.out.println("poll " + (i + 1) + ": " + states.get(i));
            if (states.get(i).equals("confirmed")) { confirmed = true; break; }
        }
        if (!confirmed) throw new AssertionError("order never confirmed");
        System.out.println("assertion passed on observed state");
    }
}``
```

### Your first time: Your mission: harden one unstable test

- [ ] Delete fixed sleeps — Replace each with the authoritative state or event it was guessing about.
- [ ] Isolate identity and data — Fresh context, unique records, deterministic clock/seed, and scoped cleanup.
- [ ] Stabilize boundaries — Pin/runtime-record dependencies, locale, timezone, and runner resources.
- [ ] Stress and observe — Run alone, random order, parallel, repeated, and retain first-failure evidence.

The test now fails on contract divergence, not on incidental timing.

- **A longer timeout reduces but does not remove failures.**
  Identify the missing readiness condition or overloaded dependency; wait on state and measure duration rather than extending blindly.
- **Tests pass alone but fail together.**
  Find shared users/data/files/ports/clock/global state, order dependence, and cleanup collisions; namespace or isolate them.
- **A selector breaks on harmless layout changes.**
  Use role/name, label, or an explicit test contract instead of deep CSS/XPath structure.
- **A mock-based test is stable but production integration fails.**
  Validate mocks against provider contracts and retain representative controlled integration tests.

### Where to check

- **Readiness condition** — authoritative UI/API/event/database state.
- **Fixture lifecycle** — setup, unique data, isolation, and cleanup.
- **Order/parallel runs** — shared state and resource collision.
- **Runtime manifest** — browser, image, dependency, locale, timezone, clock, and seed.
- **First-divergence evidence** — trace, logs, network, console, metrics, and screenshots.

### Worked example: replacing a sleep with the actual order contract

1. After Place order, the test sleeps five seconds and checks for “Confirmed.”
2. Under load, confirmation takes six seconds; locally it takes 300 ms.
3. The team asserts the status element with bounded auto-retry and captures API/event timing.
4. The test finishes quickly when healthy and fails only when confirmation exceeds the real SLA.
5. Unique order IDs and fresh contexts make parallel execution independent.

**Quiz.** Which change most directly improves timing stability?

- [ ] Double every fixed sleep
- [ ] Retry the entire suite five times
- [x] Wait with a bounded assertion on the authoritative state the user contract requires
- [ ] Run all tests sequentially forever

*State-based synchronization adapts to normal speed variation and fails at a meaningful boundary. Sleeps only guess, and broad retries hide causes.*

- **State-based wait** — Bounded polling of a meaningful observable condition rather than fixed elapsed time.
- **Isolation** — Each test owns fresh context and state so other tests cannot change its outcome.
- **Deterministic input** — Recorded or controlled data, seed, clock, locale, timezone, and dependency behavior.
- **Resilient selector** — User-facing role/name or explicit contract that survives incidental DOM layout changes.
- **Order independence** — A test succeeds alone and in arbitrary suite order because it owns prerequisites.

### Challenge

Choose one test containing sleeps or shared fixtures. Replace guesses with state conditions, unique
data, and fresh context; run it 100 times alone, random-order, and parallel while retaining evidence.

### Ask the community

> Test [ID] is unstable under [condition]. Its state wait, fixture/data isolation, clock/seed, runtime/dependencies, order/parallel result, and first-divergence evidence are [values].

These dimensions lead to an engineering fix rather than a timeout increase.

- [Playwright Docs — auto-retrying assertions](https://playwright.dev/docs/test-assertions)
- [Playwright Docs — test isolation](https://playwright.dev/docs/browser-contexts)

🎬 [Avoid Flaky End-to-End Tests with Playwright toPass — Checkly](https://www.youtube.com/watch?v=8g7FvoRToGo) (8 min)

- Synchronize on authoritative state, not arbitrary time.
- Make tests isolated, order-independent, parallel-safe, and deterministic in inputs.
- Control and record clocks, seeds, dependencies, runtime, locale, timezone, and resources.
- Prefer resilient user-facing or explicit-contract selectors.
- Use repeated hostile execution and first-divergence evidence to maintain stability continuously.


## Related notes

- [[Notes/automation-in-cicd/flake-management/detecting-flakes|Detecting flakes]]
- [[Notes/playwright/setup-and-auto-waiting/auto-waiting-explained|Auto-waiting explained]]
- [[Notes/automation-in-cicd/running-tests-in-ci/artifacts|Artifacts]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/flake-management/stability-practices.mdx`_
