---
title: "Waits wrapper"
tags: ["framework-design", "reusable-components", "track-d"]
updated: "2026-07-17"
---

# Waits wrapper

*Selenium waiting means three lines of WebDriverWait + ExpectedConditions boilerplate at every call site. A small Waits wrapper owns those lines once - timeout, polling, ignored exceptions - so every wait in the suite becomes one readable line and the wait policy has exactly one home.*

> Open any test in the suite and you'll find the same three lines: construct a WebDriverWait, pick a
> timeout, call until with an ExpectedCondition. A hundred and twenty call sites, a hundred and twenty
> copies - some with 10 seconds, some with 5, a quarter missing the ignored-exception clause someone
> added after last month's flaky week. A waits wrapper exists so those three lines are written once,
> and the suite's entire waiting policy lives behind one method name.

> **In real life**
>
> A crosswalk signal is one sealed box that owns the decision "is it safe to cross yet?" Pedestrians
> don't each time the traffic gaps, estimate car speeds, and make a private judgment call - they read
> one symbol produced by one box whose timing rules were engineered once. Everyone at the corner
> crosses by the same rule, and when the city retimes the intersection, it reprograms that one signal
> - not the pedestrians. The box is not the traffic rule itself; it's the one agreed place the rule
> lives.

**Waits wrapper**: A waits wrapper is a small helper class - often called Waits or SmartWait - that packages Selenium's explicit-wait boilerplate (constructing a WebDriverWait, setting the timeout and polling interval, attaching ignored exceptions, and calling until with an ExpectedCondition) behind short, intention-revealing static methods like Waits.untilVisible(driver, locator) or Waits.untilClickable(driver, locator). It changes none of the waiting strategy - the same explicit waits run underneath - it changes where that strategy is written: once, in one class, instead of re-typed at every call site. The payoff is one-line call sites that read as intent, a single home for the suite's wait policy (default timeout, polling, ignored exceptions), and the structural guarantee that no call site can quietly forget part of that policy.

## From three lines everywhere to one line anywhere

This note is about code organization, not wait strategy - explicit waits and their conditions are
covered elsewhere. The question here is purely: where do those lines live?

Without the wrapper, every call site re-types the ceremony:

```java
// The same ceremony, before nearly every interaction in the suite
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
wait.ignoring(StaleElementReferenceException.class);
wait.until(ExpectedConditions.elementToBeClickable(By.id("place-order")));
driver.findElement(By.id("place-order")).click();
```

With the wrapper, the ceremony is written once, and call sites shrink to a sentence:

```java
public final class Waits {
    private static final Duration DEFAULT_TIMEOUT = Duration.ofSeconds(10);

    private Waits() {}

    public static WebElement untilClickable(WebDriver driver, By locator) {
        return new WebDriverWait(driver, DEFAULT_TIMEOUT)
                .ignoring(StaleElementReferenceException.class)
                .until(ExpectedConditions.elementToBeClickable(locator));
    }

    public static WebElement untilVisible(WebDriver driver, By locator) {
        return new WebDriverWait(driver, DEFAULT_TIMEOUT)
                .ignoring(StaleElementReferenceException.class)
                .until(ExpectedConditions.visibilityOfElementLocated(locator));
    }

    // the escape hatch for genuinely slower pages - explicit, not sneaky
    public static WebElement untilVisible(WebDriver driver, By locator, Duration timeout) {
        return new WebDriverWait(driver, timeout)
                .ignoring(StaleElementReferenceException.class)
                .until(ExpectedConditions.visibilityOfElementLocated(locator));
    }
}

// every call site in the suite, from now on:
Waits.untilClickable(driver, By.id("place-order")).click();
```

- **The wrapper owns the policy** - default timeout, polling interval, ignored exceptions - and the
  policy exists in exactly one file, so it cannot be half-applied.
- **Call sites read as intent** - `untilClickable`, `untilVisible`, `untilGone` - the reader learns
  what the test is waiting for, not how Selenium waits are constructed.
- **Overloads are the escape hatch** - a slow report page gets an explicit longer timeout at its
  call site, visibly, instead of someone editing the shared default for everyone.
- **Nothing about the strategy changes** - the same WebDriverWait runs underneath. This is the same
  move as a utility class, applied to the most-repeated boilerplate a Selenium suite has.

> **Tip**
>
> Name wrapper methods after the condition, not the mechanism: untilVisible, untilClickable,
> untilTextPresent. If the method names mirror ExpectedConditions closely, any Selenium reader can
> guess the implementation without opening the class - and page objects that use the wrapper read
> almost like prose: return Waits.untilVisible(driver, successBanner).getText().

> **Common mistake**
>
> Letting per-call-site timeouts sneak back in as copy-paste: a teammate needs 30 seconds once, writes
> raw WebDriverWait boilerplate inline "just here," and three months later the suite has two waiting
> systems again - the wrapper for most calls, and a scattering of hand-rolled waits nobody tracks. The
> wrapper must be the only door: slow cases go through an explicit timeout overload, so even the
> exceptions to the default are visible, greppable, and consistent.

![A New York City pedestrian signal in a yellow-framed housing on a black pole, showing a red LED raised-hand symbol with the unlit walking-person section beside it and tall office buildings blurred in the background](waits-wrapper.jpg)
*Pedestrian LED traffic light, Financial District, New York — Wikimedia Commons, CC0 (Freier Denker). [Source](https://commons.wikimedia.org/wiki/File:Pedestrian_LED_Traffic_Light_NYC.jpg)*
- **The red hand — the condition, rendered for everyone** — Pedestrians read one symbol instead of each judging traffic themselves. A wrapper call site reads one method name - untilClickable - instead of re-deriving the wait construction every time.
- **The unlit WALK half — the other condition, same box** — Walk and don't-walk both come from one housing. untilVisible, untilClickable, untilGone - different conditions, one Waits class, so every kind of waiting shares one policy.
- **The sealed yellow housing — where the timing rules live** — The intersection's timing is engineered inside this one box. The wrapper is the same: default timeout, polling and ignored exceptions live inside the class, invisible at the call sites that rely on them.
- **The pole at the corner — one signal serving every crosser** — Every pedestrian at this corner obeys the same box, so the city retimes the intersection by reprogramming one signal. Change the wrapper's default once, and every wait in the suite follows.

**How wait boilerplate spreads - and how a wrapper pulls it back**

1. **One test needs to wait for the order button** — Three lines of WebDriverWait ceremony, written inline. Reasonable.
2. **120 call sites later, the ceremony is everywhere** — Copied, tweaked, occasionally missing the ignored-exception clause that stops stale-element flake.
3. **Staging slows down: the default timeout must change** — The policy lives in 120 places - that's 120 edits, or a regex-replace and a prayer.
4. **The ceremony moves into one Waits class** — Waits.untilClickable(driver, locator) - every call site becomes one intention-revealing line.
5. **The wait policy now has one home** — Timeout, polling, ignored exceptions change in one file, and every wait in the suite follows at once.

The wrapper's payoff is countable: boilerplate lines in the suite, call sites that forgot part of
the policy, and edits needed when the policy changes. Here's that bookkeeping as a small simulation.

*Run it - the cost of 120 inline waits versus one wrapper (Python)*

```python
# Every wait in the suite, organized two ways: inline boilerplate vs one wrapper.

BOILERPLATE_LINES = 3   # new WebDriverWait(...) + .ignoring(...) + .until(...)
CALL_SITES = 120        # places in the suite that wait for something

# Inline: every call site owns its own copy of the wait policy -
# and a quarter of them forgot the .ignoring(StaleElementReferenceException) part
inline = {f"site_{i}": {"timeout": 10, "ignores_stale": i % 4 != 0}
          for i in range(1, CALL_SITES + 1)}
forgot = [s for s, policy in inline.items() if not policy["ignores_stale"]]

print("--- inline WebDriverWait at every call site ---")
print(f"boilerplate lines in the suite: {BOILERPLATE_LINES * CALL_SITES}")
print(f"call sites missing part of the policy: {len(forgot)}")
print(f"changing the default timeout: {CALL_SITES} edits")

print()

# Wrapper: ONE function owns the policy; every call site is one line
wrapper = {"timeout": 10, "ignores_stale": True}
print("--- one Waits.until() wrapper ---")
print(f"boilerplate lines in the suite: {BOILERPLATE_LINES} (inside the wrapper)")
print("call sites missing part of the policy: 0")
wrapper["timeout"] = 15
print(f"changing the default timeout: 1 edit -> every wait now uses {wrapper['timeout']}s")
```

Same bookkeeping in Java.

*Run it - the cost of 120 inline waits versus one wrapper (Java)*

```java
public class Main {
    static final int BOILERPLATE_LINES = 3; // new WebDriverWait(...) + .ignoring(...) + .until(...)
    static final int CALL_SITES = 120;      // places in the suite that wait for something

    public static void main(String[] args) {
        // Inline: every call site owns its own copy of the wait policy -
        // and a quarter of them forgot the .ignoring(StaleElementReferenceException) part
        int forgot = 0;
        for (int site = 1; site <= CALL_SITES; site++) {
            boolean ignoresStale = site % 4 != 0;
            if (!ignoresStale) forgot++;
        }

        System.out.println("--- inline WebDriverWait at every call site ---");
        System.out.println("boilerplate lines in the suite: " + (BOILERPLATE_LINES * CALL_SITES));
        System.out.println("call sites missing part of the policy: " + forgot);
        System.out.println("changing the default timeout: " + CALL_SITES + " edits");

        System.out.println();

        // Wrapper: ONE method owns the policy; every call site is one line
        int wrapperTimeout = 10;
        System.out.println("--- one Waits.until() wrapper ---");
        System.out.println("boilerplate lines in the suite: " + BOILERPLATE_LINES + " (inside the wrapper)");
        System.out.println("call sites missing part of the policy: 0");
        wrapperTimeout = 15;
        System.out.println("changing the default timeout: 1 edit -> every wait now uses " + wrapperTimeout + "s");
    }
}
```

### Your first time: Your mission: wrap your suite's wait boilerplate and retire the copies

- [ ] Count the ceremony: grep your suite (or a tutorial project) for 'new WebDriverWait' — Each hit outside a wrapper class is one copy of the policy. Note how many use different timeouts - that inconsistency is unplanned.
- [ ] Create a Waits class with two static methods: untilVisible and untilClickable — Default timeout as a private constant, ignored exceptions attached, ExpectedConditions underneath - the exact lines you found, written once.
- [ ] Convert five call sites to one-line wrapper calls and rerun those tests — Same green results, five fewer copies of the ceremony - behavior unchanged, organization changed.
- [ ] Change the default timeout in the wrapper and rerun — Every converted call site follows instantly; every unconverted one keeps its stale private policy. That contrast is the whole argument.

You've now moved a policy from a hundred homes into one - without touching what the suite actually
waits for.

- **Raw WebDriverWait boilerplate keeps reappearing in new tests even though the wrapper exists.**
  The wrapper isn't covering a condition people need (waiting for text, for an element count, for invisibility), so they route around it. Audit the raw waits, add the missing untilX methods, and make 'no inline WebDriverWait outside Waits' a review rule you can grep for.
- **One slow page needed a longer wait, and someone raised the wrapper's default timeout for the entire suite.**
  The default is the policy for the common case; exceptions must be local. Add a timeout-parameter overload and use it at that one call site - the slow page's cost stays visible at the slow page, and the other hundred call sites keep failing fast.
- **A wait fails and the stack trace points into the wrapper, not the test - and triage got slower.**
  Make the wrapper tell the story: pass a message into the wait or wrap the TimeoutException with the locator and condition ('waited 10s for visibility of #order-total'). One good failure message in one place upgrades diagnostics for every wait in the suite at once - the same leverage, applied to debugging.
- **The wrapper has started growing click(), type(), and select() methods that take locators, and tests call it directly.**
  That's scope creep from wait wrapper toward a driver wrapper - and locators are scattering back into tests. Keep Waits about waiting; interaction methods belong in page classes, which call Waits internally. If a test passes a By to the wrapper, ask why that locator isn't inside a page object.

### Where to check

- **A grep for `new WebDriverWait` across the suite** — one hit inside the wrapper class is the
  goal; every other hit is a call site holding its own copy of the policy.
- **The Waits class itself** — the default timeout, polling interval, and ignored exceptions
  should all be visible in one screenful; that's the suite's entire waiting policy.
- **Timeout values across call sites** — if converted call sites pass explicit timeouts routinely,
  the default is wrong or the overload is being abused; both are one-file conversations.
- **Selenium's official waits documentation** — the strategy the wrapper packages: explicit waits,
  ExpectedConditions, and why implicit and explicit waits must not be mixed.

### Worked example: the timeout change that was one line instead of a hundred and twenty

1. A team's suite has around 120 explicit waits, written inline over two years. Timeouts vary from
   5 to 20 seconds with no recorded reason; roughly a quarter predate the day someone started adding
   ignoring(StaleElementReferenceException) and never got it.
2. The staging environment moves to a shared cluster and gets slower. The de facto 10-second default
   starts timing out on page loads - dozens of red tests, none of them real product bugs.
3. Before touching timeouts, an engineer spends a morning extracting a Waits class: untilVisible,
   untilClickable, untilGone, plus a timeout overload. A scripted pass converts the inline
   ceremonies to one-liners; tests stay green because the underlying strategy is unchanged.
4. Then the actual fix: the wrapper's DEFAULT_TIMEOUT goes from 10 to 15 seconds. One line, one
   file. The suite reruns green against the slower staging cluster the same afternoon.
5. Weeks later, stale-element flake in the checkout area vanishes too - the quarter of call sites
   that had been missing the ignoring clause inherited it silently during conversion. Nobody had to
   find them; the wrapper made their omission structurally impossible.

**Quiz.** A team has a Waits wrapper with a 10-second default. One report page legitimately takes 25 seconds to render its table. What does this note recommend?

- [ ] Raise the wrapper's default timeout to 25 seconds so the report tests pass
- [ ] Write inline WebDriverWait boilerplate just for the report page, since the wrapper doesn't fit
- [x] Call a timeout overload at that call site - Waits.untilVisible(driver, table, Duration.ofSeconds(25)) - so the exception is explicit and local while the suite default stays fast
- [ ] Replace the wait with Thread.sleep(25000) since the delay is known and constant

*The default encodes the policy for the common case, and exceptions should be visible exactly where they apply - the overload keeps the slow page's cost at the slow page's call site, greppable and reviewed. Option one makes every timeout in the suite 2.5x slower to fail, hiding real hangs behind a default chosen for one page. Option two restarts the boilerplate scatter the wrapper exists to end - the next reader finds two waiting systems. Option four is worse than both: a fixed sleep always pays the full 25 seconds even when the table renders in 8, and still fails on the day it takes 26.*

- **What does a waits wrapper actually change?** — Where the wait code lives, not how waiting works. The same WebDriverWait + ExpectedConditions run underneath - but the boilerplate is written once, in one class, instead of at every call site.
- **What policy does the wrapper class own?** — The suite's waiting defaults: timeout, polling interval, and ignored exceptions (like StaleElementReferenceException) - defined once, applied to every wait automatically.
- **How should wrapper methods be named?** — After the condition, not the mechanism: untilVisible, untilClickable, untilGone. Call sites then read as intent, and any Selenium reader can guess the implementation.
- **How do you handle one genuinely slow page?** — A timeout-parameter overload at that call site - explicit and local - never by raising the shared default, and never by writing inline boilerplate around the wrapper.
- **The crosswalk-signal analogy for the waits wrapper** — One sealed box owns 'safe to cross yet?' and everyone reads its symbol; retiming the intersection reprograms one signal. The wrapper owns 'ready to interact yet?' - and changing the policy is one edit, not one per pedestrian.

### Challenge

In any suite you can access, run a grep for `new WebDriverWait` and build a one-page census: how
many call sites, which timeouts appear, and how many attach ignored exceptions. Then write the
Waits class that would replace them (methods, default, overloads), convert the three most-repeated
call sites, and rerun those tests to prove behavior is unchanged while the copies are gone.

### Ask the community

> My suite has `[N]` inline WebDriverWait call sites with timeouts ranging from `[min]` to `[max]` seconds. Here's a typical one: `[paste it]`. What would you put in a Waits wrapper first, and what default timeout reasoning would you use?

Sharing one real call site plus your timeout spread gets much sharper advice than asking in the
abstract - reviewers can tell you which variations are real requirements worth an overload, and
which are just drift that conversion should erase.

- [Selenium — official docs: Waiting strategies](https://www.selenium.dev/documentation/webdriver/waits/)
- [Selenium — official docs: Expected conditions](https://www.selenium.dev/documentation/webdriver/support_features/expected_conditions/)

🎬 [Selenium Class 50: How To Use Explicit Wait in Selenium 4 — Testing Tutorialspoint](https://www.youtube.com/watch?v=07NCR1ml0O4) (7 min)

- A waits wrapper moves the WebDriverWait + ExpectedConditions ceremony into one class, turning three lines at every call site into one intention-revealing line.
- It changes code organization, not wait strategy - the same explicit waits run underneath, so converting call sites leaves behavior untouched.
- The wrapper is the single home of the wait policy: default timeout, polling, and ignored exceptions live in one file and cannot be half-applied.
- Handle slow pages with explicit timeout overloads at their call sites - never by raising the shared default or writing inline boilerplate around the wrapper.
- Keep the wrapper about waiting: interaction methods that take locators belong in page classes, which call the wrapper internally.


## Related notes

- [[Notes/framework-design/reusable-components/utilities|Utilities]]
- [[Notes/framework-design/reusable-components/driver-factory|Driver factory]]
- [[Notes/framework-design/page-object-model/the-pom-pattern|The POM pattern]]


---
_Source: `packages/curriculum/content/notes/framework-design/reusable-components/waits-wrapper.mdx`_
