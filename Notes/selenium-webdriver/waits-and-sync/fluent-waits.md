---
title: "Fluent waits and observable polling"
tags: ["selenium", "webdriver", "waits", "synchronization", "track-d"]
updated: "2026-07-18"
---

# Fluent waits and observable polling

*Configure timeout, polling cadence, and narrowly ignored transient exceptions while preserving the final cause of failure.*

> Polling faster does not make an application ready sooner. It only changes how often the test observes state—and how much load and log noise the test creates.

> **In real life**
>
> Several darts show separate attempts while the bullseye defines success. A fluent wait needs the same discipline: bounded attempts, one explicit target, and a record of misses. Hiding every thrown exception would be like erasing the dartboard between throws.

**fluent wait**: A fluent wait is a configurable wait with a maximum duration, polling interval, condition, and optional set of ignored transient exceptions.

## Wait for evidence, not elapsed time

Java's `FluentWait` lets you set the timeout, polling interval, message supplier, and exceptions to ignore. `WebDriverWait` is a specialization for WebDriver and ignores `NotFoundException` by default. Python `WebDriverWait` accepts a timeout, poll frequency, and ignored exceptions.

Ignore only exceptions that mean try again in this condition, such as a temporarily missing element. Do not ignore assertion failures, invalid selectors, or unrelated driver errors. A useful timeout report preserves elapsed time, condition, locator, poll count, last observed value, and last transient exception.

> **Tip**
>
> Match polling cadence to meaningful state change; a 10 ms poll rarely helps a UI that updates every few hundred milliseconds.

> **Common mistake**
>
> Ignoring broad exception types until the wait times out. That replaces the real defect with a generic timeout and destroys causal evidence.

![Three darts embedded at different positions around a dartboard bullseye](fluent-waits.jpg)
*Darts in a dartboard — David A. Tyo, public domain. [Source](https://commons.wikimedia.org/wiki/File:Darts_in_a_dartboard.jpg)*
- **Initial state** — The first visible state is evidence, not yet success.
- **Repeated observation** — Polling samples state without assuming when it changes.
- **Decisive condition** — The named target state releases the next action.
- **Deadline** — A bounded wait rejects missing readiness with evidence.

**A condition-based wait**

1. **Trigger** — Perform the action that starts asynchronous work.
2. **Observe** — Evaluate one named condition.
3. **Poll** — Retry only while the deadline and transient policy allow.
4. **Return or reject** — Continue on decisive state or fail with the last observation.

## Real Selenium examples

These fenced samples require Selenium; the playground pair is a dependency-free timing model.

~~~python
from selenium.webdriver.support.ui import WebDriverWait

wait = WebDriverWait(driver, 10, poll_frequency=0.25)
message = wait.until(lambda d: d.find_element(By.ID, "status").text == "Ready")
~~~

~~~java
Wait wait = new FluentWait<>(driver)
    .withTimeout(Duration.ofSeconds(10))
    .pollingEvery(Duration.ofMillis(250))
    .ignoring(NoSuchElementException.class);
~~~

*Run it — wait for one decisive state (Python)*

```python
EXPECTED = "ready"
OBSERVATIONS = [[0,"loading"],[2,"loading"],[4,"ready"]]

def wait_until(observations, expected, deadline):
    for timestamp, state in observations:
        if timestamp > deadline:
            break
        if state == expected:
            return timestamp, state
    raise AssertionError(f"timeout deadline={deadline} expected={expected}")

ready = wait_until(OBSERVATIONS, EXPECTED, 5)
accepted = ready == (4, EXPECTED)
assert accepted, "the wait must return the first decisive observation"

try:
    wait_until(OBSERVATIONS, EXPECTED, 3)
    raise AssertionError("the short deadline must reject readiness")
except AssertionError as error:
    timeout_rejected = str(error).startswith("timeout deadline=")
assert timeout_rejected, "timeout evidence must be preserved"

print(f"READY t={ready[0]} state={ready[1]}")
print("REJECT timeout deadline=3")
print("RESULT ready=true timeout_rejected=true")
```

*Run it — wait for one decisive state (Java)*

```java
import java.util.List;

public class Main {
    static final String EXPECTED = "ready";
    record Observation(int time, String state) {}
    static Observation waitUntil(List<Observation> observations, String expected, int deadline) {
        for (Observation item : observations) {
            if (item.time() > deadline) break;
            if (item.state().equals(expected)) return item;
        }
        throw new AssertionError("timeout deadline=" + deadline + " expected=" + expected);
    }
    public static void main(String[] args) {
        List<Observation> observations = List.of(new Observation(0, "loading"), new Observation(2, "loading"), new Observation(4, "ready"));
        Observation ready = waitUntil(observations, EXPECTED, 5);
        boolean accepted = ready.equals(new Observation(4, EXPECTED));
        if (!accepted) throw new AssertionError("the wait must return the first decisive observation");
        boolean timeoutRejected = false;
        try { waitUntil(observations, EXPECTED, 3); }
        catch (AssertionError error) { timeoutRejected = error.getMessage().startsWith("timeout deadline="); }
        if (!timeoutRejected) throw new AssertionError("timeout evidence must be preserved");
        System.out.println("READY t=" + ready.time() + " state=" + ready.state());
        System.out.println("REJECT timeout deadline=3");
        System.out.println("RESULT ready=true timeout_rejected=true");
    }
}
```

### Your first time: Your mission: replace one sleep

- [ ] Name the transition — Write the state before and the decisive state after the async work.
- [ ] Choose an observation — Use visible UI or protocol evidence required by the next action.
- [ ] Bound the wait — Set timeout and polling cadence appropriate to the system.
- [ ] Capture failure — Preserve last state, condition, locator, elapsed time, and relevant logs.

You now have a synchronization oracle rather than a delay guess.

- **The wait times out although the page looks ready.**
  Compare the named condition with the actual next-action requirement and last observed state.
- **The wait is much longer than configured.**
  Check for mixed implicit and explicit waits or slow work inside the condition.
- **A stale element repeats until timeout.**
  Relocate by a stable locator after rerender instead of polling an old reference.
- **CI fails but local runs pass.**
  Capture timings, network, console, and the exact transition instead of enlarging a sleep.

### Where to check

- **Wait diagnostics** — condition, locator, timeout, poll count, and last observed value.
- **Browser console and network** — async errors, rejected requests, and completion timing.
- **DOM snapshots** — node replacement, visibility, enabledness, and text changes.
- **Timeout configuration** — implicit, explicit, script, and page-load timeouts kept distinct.

### Worked example: the spinner that outlived the sleep

A test clicks Search, sleeps two seconds, and reads an empty results panel. On a busy runner the response takes three seconds. The repair waits for the spinner to disappear and results to become visible, returns early on fast runs, and reports the last state plus network failure when readiness never occurs.

**Quiz.** What should release an explicit wait?

- [ ] The average historical delay
- [x] A named state required by the next action
- [ ] The longest sleep the suite can tolerate
- [ ] Any ignored exception

*A wait is useful when its condition proves the next action can proceed; elapsed time alone does not.*

- **Implicit wait** — A session-wide timeout applied to element location.
- **Explicit wait** — A bounded polling loop for one named condition.
- **Polling interval** — How often a wait reevaluates its condition.
- **Last observation** — The state or exception that makes a timeout diagnosable.

### Challenge

Mutate EXPECTED in both playgrounds. The original state observations must make each program exit nonzero. Then add an observation exactly at the deadline and prove the boundary policy is inclusive.

### Ask the community

> After [trigger], I waited [timeout] for [condition] at [locator]. The last state was [state], poll count was [count], and network/console evidence was [summary]. Which boundary should I inspect next?

Remove credentials, private URLs, cookies, and customer data.

- [Selenium — Waiting strategies](https://www.selenium.dev/documentation/webdriver/waits/)
- [Selenium Java API — FluentWait](https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/support/ui/FluentWait.html)
- [Selenium Python API — waits](https://www.selenium.dev/selenium/docs/api/py/selenium_webdriver_support/selenium.webdriver.support.wait.html)

🎬 [Retries and Test Flakiness in Playwright](https://www.youtube.com/watch?v=B2xvEk-EEvk) (10 min)

- Readiness is a condition, not a duration.
- Implicit waits affect lookup; explicit waits can name richer state.
- Do not mix implicit and explicit waits.
- Bounded polling should preserve the last observation and cause.
- Real Selenium stays fenced; playgrounds model timing deterministically.


## Related notes

- [[Notes/selenium-webdriver/waits-and-sync/implicit-vs-explicit|Implicit vs explicit]]
- [[Notes/selenium-webdriver/waits-and-sync/avoiding-sleeps|Avoiding sleeps]]
- [[Notes/selenium-webdriver/waits-and-sync/handling-async|Handling async]]


---
_Source: `packages/curriculum/content/notes/selenium-webdriver/waits-and-sync/fluent-waits.mdx`_
