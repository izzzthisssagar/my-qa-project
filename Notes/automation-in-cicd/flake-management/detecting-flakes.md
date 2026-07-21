---
title: "Detecting flakes"
tags: ["ci", "flaky-tests", "reliability", "diagnostics", "track-d"]
updated: "2026-07-17"
---

# Detecting flakes

*A flaky test produces different outcomes without a relevant product change; detecting it requires attempt-level history, stable test identity, controlled repetition, failure fingerprints, and environment correlation.*

> The same test fails on SHA `abc123`, passes on rerun of SHA `abc123`, and nobody changed code,
> configuration, data, or environment intentionally. Calling the first result “just CI” throws away
> the most important evidence: the test or system is nondeterministic under the conditions you run.

> **In real life**
>
> Every snowflake is recognizable as snow but its detailed shape depends on tiny changes in temperature
> and humidity. A flaky test also has a repeatable family of influences—timing, order, data, resource,
> network, clock—even when the individual failure looks unique.

**Flaky test**: A flaky test has more than one possible outcome for materially equivalent code, configuration, data, and environment. Detection requires stable test identity and attempt-level results. A fail-then-pass sequence is strong evidence, but repeated passes do not prove absence: low-probability flakes need many observations and controlled stress dimensions.

## Preserve attempts; do not overwrite them

```text
test_id=checkout::creates_order sha=abc123 attempt=1 status=failed worker=7 seed=4812
test_id=checkout::creates_order sha=abc123 attempt=2 status=passed worker=2 seed=4812
fingerprint=Timeout waiting for POST /orders
```

Track code, test version, runner image, browser/runtime, seed, worker/shard, order, data namespace,
clock, dependency endpoints, duration, and failure fingerprint. Otherwise “same conditions” is guesswork.

> **Tip**
>
> Use repeated and randomized-order runs to amplify timing/order bugs, then segment failures by worker,
> browser, runtime, runner image, time, seed, and dependency. Correlation is a lead, not proof of cause.

> **Common mistake**
>
> Calling every intermittent failure a flaky test. The product, environment, network, data, or dependency
> may genuinely be unstable. The test can be the messenger; classify the failing system after evidence.

![Macro photograph of a detailed natural snow crystal](detecting-flakes.jpg)
*Snowflake macro photography 1 (cropped) — Alexey Kljatov, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Snowflake_macro_photography_1_(cropped).jpg)*
- **Stable identity** — The center anchors observations to the same logical test and revision.
- **Timing branch** — Scheduling and readiness differences create one family of intermittent outcomes.
- **Data and order** — Shared state, seeds, and execution order create another family.
- **Environment** — Runner, browser, network, clock, and dependency variation must be recorded.

**From intermittent result to classified evidence**

1. **Unexpected failure appears** — Preserve first-attempt logs, trace, seed, environment, and exact SHA.
2. **Identity is normalized** — Map renamed/parameterized cases to a stable test ID and configuration.
3. **Equivalent rerun executes** — Hold relevant variables constant before changing dimensions deliberately.
4. **Attempts are compared** — Fail-pass, error fingerprints, duration, worker, order, and dependencies.
5. **Stress isolates dimension** — Repeat, randomize, parallelize, throttle, or pin clock/data one variable at a time.
6. **Cause class is owned** — Test, product, environment, infrastructure, or dependency receives an issue.

*Run it — rank tests by observed flake rate (Python)*

```python
``attempts = {"login": [1, 1, 1, 1], "checkout": [0, 1, 1, 0], "search": [1, 1, 0, 1]}
for test, outcomes in attempts.items():
    failures = outcomes.count(0)
    mixed = 0 < failures < len(outcomes)
    print(f"{test}: failures={failures}/{len(outcomes)} candidate_flake={mixed}")``
```

*Run it — rank tests by observed flake rate (Java)*

```java
``import java.util.*;

public class Main {
    public static void main(String[] args) {
        var attempts = new LinkedHashMap<String, List<Integer>>();
        attempts.put("login", List.of(1,1,1,1)); attempts.put("checkout", List.of(0,1,1,0));
        attempts.put("search", List.of(1,1,0,1));
        attempts.forEach((test, out) -> {
            long failures = out.stream().filter(x -> x == 0).count();
            boolean mixed = failures > 0 && failures < out.size();
            System.out.printf("%s: failures=%d/%d candidate_flake=%s%n", test, failures, out.size(), mixed);
        });
    }
}``
```

### Your first time: Your mission: reproduce one intermittent result

- [ ] Freeze identity and first evidence — SHA, test version, seed, environment, order, trace, and fingerprint.
- [ ] Repeat equivalent conditions — Do not silently upgrade dependencies or change data between attempts.
- [ ] Vary one stress dimension — Parallelism, order, network, CPU, locale, timezone, or clock.
- [ ] Classify and file ownership — Test defect, product race, environment, infrastructure, or dependency.

You now have a reproducible instability investigation rather than a rerun anecdote.

- **A rerun passes but no first-attempt trace exists.**
  Capture evidence on first failure or first retry and retain each attempt separately.
- **Flake trends reset after test renames.**
  Use a stable test ID independent of display title/path and maintain alias history.
- **Failures cluster on one runner.**
  Compare image, CPU/memory, clock, network, browser/runtime, and cached state before blaming the test.
- **100 repeats pass locally.**
  Reproduce CI parallelism, resources, order, timezone, seed, services, and network; local equivalence was not established.

### Where to check

- **Attempt-level report** — first, retry, and final outcome.
- **Trace/log/artifact per attempt** — first causal divergence.
- **Test identity and revision** — same logical case and code.
- **Seed/order/worker/shard** — state and concurrency correlation.
- **Runner/dependency telemetry** — environment instability.

### Worked example: a checkout failure that follows worker seven

1. Checkout fails 8 of 200 runs and passes every automatic retry.
2. Attempt history shows all failures on worker seven after a long setup duration.
3. Runner metrics show disk pressure; browser launch occasionally exceeds the fixed timeout.
4. The team drains the runner, fixes cleanup/capacity, and keeps the test unchanged.
5. Controlled repeats across workers confirm the failure disappears: infrastructure was flaky, not the assertion.

**Quiz.** What is strongest evidence of a flaky outcome?

- [ ] A test failed once on CI
- [ ] A developer says it passes locally
- [x] The same test and revision fail then pass under materially equivalent recorded conditions
- [ ] The suite is large

*Different outcomes under equivalent conditions establish nondeterminism. One failure may be a deterministic product, test, or environment defect.*

- **Flake** — Different outcomes under materially equivalent conditions.
- **Attempt-level history** — Separate record of every initial run and retry, never collapsed into only final status.
- **Failure fingerprint** — Normalized error signature used to group likely instances of one failure mode.
- **Stress dimension** — One controlled variable such as order, parallelism, clock, or network used to amplify a cause.
- **Stable test ID** — Identity that survives display-name/path changes for reliable trends.

### Challenge

Run one suspected case 100 times under recorded seed/order/worker data, then change one dimension.
Calculate first-attempt failure rate and show whether a failure fingerprint correlates with that dimension.

### Ask the community

> Test [stable ID] on SHA [sha] failed attempts [numbers] and passed [numbers]. Seed/order/worker/runtime, fingerprint, and evidence links are [values]; changing [one dimension] produced [result].

This gives others an instability experiment they can reproduce.

- [Playwright Docs — retries and flaky classification](https://playwright.dev/docs/test-retries)
- [Playwright Docs — repeat and fail-on-flaky CLI options](https://playwright.dev/docs/test-cli)

🎬 [3 Reasons for Playwright Flaky Tests (and How To Fix It) — Artem Bondar](https://www.youtube.com/watch?v=CwfohDaRpig) (11 min)

- Flakiness means different outcomes under materially equivalent conditions.
- Preserve every attempt with stable identity and complete environment context.
- Fail-then-pass is evidence; repeated passes do not prove a low-rate flake absent.
- Vary one stress dimension at a time and correlate rather than guess.
- Classify ownership across test, product, environment, infrastructure, and dependency.


## Related notes

- [[Notes/automation-in-cicd/flake-management/retries|Retries]]
- [[Notes/automation-in-cicd/flake-management/quarantine|Quarantine]]
- [[Notes/automation-in-cicd/scheduling-and-reporting/dashboards|Dashboards]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/flake-management/detecting-flakes.mdx`_
