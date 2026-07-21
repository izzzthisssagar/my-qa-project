---
title: "Avoiding fixed sleeps"
tags: ["selenium", "webdriver", "waits", "synchronization", "track-d"]
updated: "2026-07-18"
---

# Avoiding fixed sleeps

*Replace unconditional delays with bounded condition waits that return early on success and fail with the last observed state.*

> A sleep has only two modes: waste time after the app is ready, or wake up before it is ready. Making the number larger merely shifts which failure you see.

> **In real life**
>
> A wall of live camera feeds is useful because an operator can react when the relevant scene changes. Closing your eyes for five seconds is not monitoring. Condition polling observes the right feed until its state is decisive or the deadline expires.

**fixed sleep**: A fixed sleep pauses the test for a predetermined duration without observing whether the application became ready earlier or never became ready.

## Wait for evidence, not elapsed time

`time.sleep` and `Thread.sleep` are appropriate only when the delay itself is the behavior under test or a protocol requires a minimum interval. They are poor synchronization tools because they observe nothing. Fast runs pay the whole delay; slow runs can still fail after it.

Replace sleeps with a condition tied to user-visible or protocol state: a spinner disappears, text changes, a button becomes enabled, a URL reaches the expected value, or a request-backed result appears. Bound the wait and log the last observation. Do not wait for a vague page loaded concept when the next action needs one specific control.

> **Tip**
>
> Before deleting a sleep, write the state transition it was trying to cover; that sentence becomes the explicit wait condition.

> **Common mistake**
>
> Replacing a two-second sleep with a ten-second sleep after CI fails. The test becomes slower without gaining a truthful readiness oracle.

![CCTV control room wall showing many live camera feeds](avoiding-sleeps.jpg)
*CCTV control room monitor wall — Mark Yeomans, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:CCTV_control_room_monitor_wall.jpg)*
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
wait = WebDriverWait(driver, 10)
result = wait.until(EC.visibility_of_element_located((By.ID, "result")))
~~~

~~~java
WebElement result = new WebDriverWait(driver, Duration.ofSeconds(10))
    .until(ExpectedConditions.visibilityOfElementLocated(By.id("result")));
~~~

*Run it — wait for one decisive state (Python)*

```python
EXPECTED = "spinner-gone"
OBSERVATIONS = [[0,"spinner-visible"],[1,"spinner-visible"],[2,"spinner-gone"]]

def wait_until(observations, expected, deadline):
    for timestamp, state in observations:
        if timestamp > deadline:
            break
        if state == expected:
            return timestamp, state
    raise AssertionError(f"timeout deadline={deadline} expected={expected}")

ready = wait_until(OBSERVATIONS, EXPECTED, 4)
accepted = ready == (2, EXPECTED)
assert accepted, "the wait must return the first decisive observation"

try:
    wait_until(OBSERVATIONS, EXPECTED, 1)
    raise AssertionError("the short deadline must reject readiness")
except AssertionError as error:
    timeout_rejected = str(error).startswith("timeout deadline=")
assert timeout_rejected, "timeout evidence must be preserved"

print(f"READY t={ready[0]} state={ready[1]}")
print("REJECT timeout deadline=1")
print("RESULT ready=true timeout_rejected=true")
```

*Run it — wait for one decisive state (Java)*

```java
import java.util.List;

public class Main {
    static final String EXPECTED = "spinner-gone";
    record Observation(int time, String state) {}
    static Observation waitUntil(List<Observation> observations, String expected, int deadline) {
        for (Observation item : observations) {
            if (item.time() > deadline) break;
            if (item.state().equals(expected)) return item;
        }
        throw new AssertionError("timeout deadline=" + deadline + " expected=" + expected);
    }
    public static void main(String[] args) {
        List<Observation> observations = List.of(new Observation(0, "spinner-visible"), new Observation(1, "spinner-visible"), new Observation(2, "spinner-gone"));
        Observation ready = waitUntil(observations, EXPECTED, 4);
        boolean accepted = ready.equals(new Observation(2, EXPECTED));
        if (!accepted) throw new AssertionError("the wait must return the first decisive observation");
        boolean timeoutRejected = false;
        try { waitUntil(observations, EXPECTED, 1); }
        catch (AssertionError error) { timeoutRejected = error.getMessage().startsWith("timeout deadline="); }
        if (!timeoutRejected) throw new AssertionError("timeout evidence must be preserved");
        System.out.println("READY t=" + ready.time() + " state=" + ready.state());
        System.out.println("REJECT timeout deadline=1");
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

🎬 [Auto Wait In Playwright | How Playwright Waits Automatically Using Actionability Check  With Java](https://www.youtube.com/watch?v=srkXpc7Ehbs) (9 min)

- Readiness is a condition, not a duration.
- Implicit waits affect lookup; explicit waits can name richer state.
- Do not mix implicit and explicit waits.
- Bounded polling should preserve the last observation and cause.
- Real Selenium stays fenced; playgrounds model timing deterministically.


## Related notes

- [[Notes/selenium-webdriver/waits-and-sync/implicit-vs-explicit|Implicit vs explicit]]
- [[Notes/selenium-webdriver/waits-and-sync/fluent-waits|Fluent waits]]
- [[Notes/selenium-webdriver/waits-and-sync/handling-async|Handling async]]


---
_Source: `packages/curriculum/content/notes/selenium-webdriver/waits-and-sync/avoiding-sleeps.mdx`_
