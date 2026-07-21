---
title: "Auto-waiting explained"
tags: ["playwright", "setup-and-auto-waiting", "track-d"]
updated: "2026-07-16"
---

# Auto-waiting explained

*Before every action, Playwright checks a fixed list of conditions on the target element - attached, visible, stable, enabled, receives events - and only acts once all of them hold, with no explicit sleep ever required.*

> Older automation code is full of `sleep(2000)` calls sprinkled in wherever a test flaked once - a
> guess at how long "probably long enough" is, wrong half the time in both directions. Playwright never
> asks you to guess. Before every action it runs a fixed checklist against the actual element, and only
> acts the moment every item on that checklist is true - not a fixed millisecond earlier, not a
> millisecond later than necessary.

> **In real life**
>
> A spacecraft's master caution panel doesn't have one light. It has a whole grid of individually
> labeled indicators - pressure, temperature, bus voltage, pump status - and mission control doesn't
> proceed on a fixed clock. It watches every specific light and moves the moment the full board reads
> clear. Playwright's actionability checks work the same way: several distinct, named conditions, all
> of them, before a single click happens.

**Auto-waiting**: Auto-waiting in Playwright is the automatic actionability check the framework runs on an element immediately before performing an action on it - confirming the element is Attached to the DOM, Visible, Stable (not mid-animation), Enabled, and able to Receive Events (not covered by another element) - retrying the whole check until every condition holds or the action's timeout is reached. No explicit sleep or manual wait call is required; the check runs automatically before click(), fill(), and every other action method.

## The checklist Playwright runs before every action

Before `click()`, `fill()`, or almost any other action method executes, Playwright confirms all of
the following about the target element:

- **Attached** — it exists in the DOM at all.
- **Visible** — it has a non-empty bounding box and isn't hidden by CSS.
- **Stable** — it's not mid-animation; its position has stopped changing across two consecutive
  frames.
- **Enabled** — it's not disabled (relevant for form controls).
- **Receives Events** — it isn't obscured by another element sitting on top of it at the click point
  (a loading spinner or modal overlay, for example).

If any check fails, Playwright doesn't error immediately - it **retries the whole checklist** until
every condition holds or the action's timeout (30 seconds by default) is reached. Only then does it
throw, and the error names exactly which check was still failing.

> **Tip**
>
> When a test times out on an action, read the error message fully before adding a manual wait - it
> names the specific actionability check that never passed ("element is not visible," "element is
> outside of the viewport"), which usually points straight at the real bug in the page rather than a
> timing problem to paper over.

> **Common mistake**
>
> Adding `page.waitForTimeout(3000)` before an action "just to be safe." This reintroduces exactly the
> guessing game auto-waiting exists to remove - too short and it's still flaky, too long and every test
> run gets slower for no benefit. If an action is genuinely failing its actionability check, the fix is
> almost always locating what's actually covering, disabling, or hiding the element - not a longer
> sleep.

![A grid of 24 individually labeled mechanical indicator switches on an Apollo command module master caution and event annunciator panel - labels including F/C-BUS DISCONNECT, H2 PRESS, O2 PRESS, MN BUS A UNDERVOLT, and AC BUS 1 FAIL - all currently unlit, mounted in a metal frame](auto-waiting-explained.jpg)
*Apollo Command Module Master Caution & Event Annunciator Panel — Wikimedia Commons, CC BY 2.0 (Steve Jurvetson). [Source](https://commons.wikimedia.org/wiki/File:Apollo_Command_Module_Master_Caution_%26_Event_Annunciator_Panel_%E2%80%94_with_the_Infamous_%22Main_Bus_B_Undervolt%22_Alarm_of_Apollo_13_(53839889630).jpg)*
- **H2O SEP PUMP FAIL — one named, specific check** — Not a generic 'something's wrong' light - a precisely named condition. Playwright's checklist is the same: 'Attached', 'Visible', 'Stable' are specific, individually named checks, not one vague readiness flag.
- **F/C 1, F/C 2, F/C 3 — several checks, evaluated together** — Three related indicators sit side by side, each independently either clear or not. An action only proceeds once every relevant indicator on the whole board reads clear, the same way every actionability check must pass, not just most of them.
- **AC BUS 1 FAIL / AC BUS 1 OVERLOAD — different failure MODES, same slot** — Two adjacent but distinct conditions about the same system - just as 'not Visible' and 'not Enabled' are two different, specifically diagnosable reasons the same click could still be blocked.
- **The whole panel, currently unlit — every light on it is why** — A clear panel isn't the absence of information, it's confirmation that every specific check was run and passed. Playwright's silent, successful click carries the same weight - five checks quietly passed, not skipped.

**One click, actionability-checked**

1. **click() is called** — The test code requests an action on a locator.
2. **Attached?** — Is the element even in the DOM yet? If not, wait and recheck.
3. **Visible? Stable?** — Non-zero size, not hidden, not still mid-animation.
4. **Enabled? Receives Events?** — Not disabled, and nothing else sitting on top of it at the click point.
5. **All clear — click happens** — The instant every check passes, not a fixed delay before or after.

An actionability check is really just: evaluate a list of named conditions, retry until all of them
are true or time runs out, and report which one is still false if it doesn't. Here's that shape as a
small, generic simulation.

*Run it - retry a checklist of named conditions until all pass or time runs out (Python)*

```python
import time

def check_attached(t): return t >= 0
def check_visible(t): return t >= 1
def check_stable(t): return t >= 2
def check_enabled(t): return t >= 2

checks = {
    "Attached": check_attached,
    "Visible": check_visible,
    "Stable": check_stable,
    "Enabled": check_enabled,
}

def wait_for_actionable(elapsed_ticks, timeout_ticks=5):
    for tick in range(timeout_ticks + 1):
        failing = [name for name, fn in checks.items() if not fn(tick)]
        if not failing:
            print(f"tick {tick}: all checks passed - action proceeds")
            return True
        print(f"tick {tick}: still waiting on {failing}")
    print(f"timed out after {timeout_ticks} ticks - still failing: {failing}")
    return False

wait_for_actionable(elapsed_ticks=0)
```

Same retry-until-all-pass shape in Java.

*Run it - retry a checklist of named conditions until all pass or time runs out (Java)*

```java
import java.util.*;
import java.util.function.*;

public class Main {
    public static void main(String[] args) {
        Map<String, IntPredicate> checks = new LinkedHashMap<>();
        checks.put("Attached", t -> t >= 0);
        checks.put("Visible", t -> t >= 1);
        checks.put("Stable", t -> t >= 2);
        checks.put("Enabled", t -> t >= 2);

        int timeoutTicks = 5;
        for (int tick = 0; tick <= timeoutTicks; tick++) {
            List<String> failing = new ArrayList<>();
            for (var entry : checks.entrySet()) {
                if (!entry.getValue().test(tick)) failing.add(entry.getKey());
            }
            if (failing.isEmpty()) {
                System.out.println("tick " + tick + ": all checks passed - action proceeds");
                return;
            }
            System.out.println("tick " + tick + ": still waiting on " + failing);
        }
        System.out.println("timed out after " + timeoutTicks + " ticks");
    }
}
```

### Your first time: Your mission: watch a real actionability failure name itself

- [ ] Write a test that clicks a locator you know will be covered by something else — A common trigger: a cookie-consent banner or loading spinner still on top of the real button when the click is attempted.
- [ ] Run it and read the timeout error message in full — Look for which specific check Playwright reports as still failing, not just "timeout exceeded".
- [ ] Fix the actual cause named in the error, not the symptom — Dismiss the covering element first, or wait for the specific condition the error named - not a blanket sleep.
- [ ] Re-run and confirm it passes with no added wait calls — The fix should be addressing what was actually blocking the action, which auto-waiting was correctly reporting the whole time.

You've now seen auto-waiting do its real job: turning a vague flaky click into a specific, named,
fixable failure.

- **"element is not visible" even though it clearly appears on screen in a screenshot.**
  Check for zero-opacity or off-screen CSS during a transition, or whether the screenshot was taken after the animation finished while the actual click attempt happened mid-transition.
- **"element is outside of the viewport" on an element that exists but hasn't been scrolled to.**
  Playwright auto-scrolls elements into view as part of actionability, but a fixed-position overlay or an unusual scroll container can defeat that - try scrollIntoViewIfNeeded() explicitly as a diagnostic step.
- **An action times out with "element does not receive events" and nothing visibly covers it.**
  Check for an invisible full-page overlay (a modal backdrop with zero opacity, or a loading spinner container that didn't unmount) sitting at a higher z-index - invisible does not mean absent from the click point.
- **A teammate added page.waitForTimeout() calls throughout a suite and flakiness came back anyway.**
  A fixed sleep doesn't fix a genuinely unstable page - it just makes the test slower while leaving the same race condition intact. Replace it with the actionability check doing its job, and fix whatever the underlying error names.

### Where to check

- **The full timeout error message** — always names the specific actionability check still failing,
  not just a generic timeout.
- **Playwright's trace viewer** (covered later in this module) — shows a timeline of exactly which
  actionability checks passed and when, for any recorded run.
- **`playwright.config.ts`'s `actionTimeout`** — the default per-action timeout auto-waiting retries
  within, if a legitimately slow page needs more than 30 seconds.
- **DevTools' Elements panel**, mid-failure — inspecting the actual computed style and z-index stack
  at the click coordinates often reveals the covering element immediately.

### Worked example: a flaky click that auto-waiting actually solved by naming the real cause

1. A checkout test intermittently fails to click "Place Order," maybe one run in five.
2. A teammate's first fix is `await page.waitForTimeout(1000);` before the click - it "mostly" works,
   but the failure still recurs occasionally, and every test run is now a full second slower.
3. Reading the actual timeout error from a failed run (rather than guessing) shows: "element is
   outside of the viewport." The page has a sticky promo banner that occasionally loads late and
   pushes the button down before the click coordinates are calculated.
4. The real fix: `await page.getByRole('button', { name: 'Place Order' }).scrollIntoViewIfNeeded();`
   before the click, addressing the actual layout shift auto-waiting had been correctly reporting the
   whole time.
5. The flakiness disappears completely - not reduced by a guessed delay, eliminated by fixing the
   condition the error named.

**Quiz.** A Playwright action times out with the error 'element is not visible.' What is the most effective next step?

- [ ] Add page.waitForTimeout(5000) before the action and hope the extra delay covers it
- [x] Read what the actionability check is reporting literally - the element genuinely fails the Visible check - and investigate why (CSS, an unfinished animation, a covering element) rather than guessing at a fixed delay
- [ ] Increase the global test timeout so the check has more time to eventually pass on its own
- [ ] Switch to a different locator strategy, since the error must mean the locator is wrong

*The note is explicit that Playwright already retries the actionability checklist automatically until timeout, and the error names the specific check still failing - a manual sleep (option one) reintroduces the exact guessing game auto-waiting exists to remove, and doesn't address why the element isn't visible. Option three might occasionally 'fix' a slow-loading page by accident, but treats a specific, diagnosable condition as a generic timing problem. Option four is a non-sequitur - 'not visible' means the located element was found but isn't currently visible, which is a different problem from having located the wrong element entirely.*

- **The five actionability checks Playwright runs before an action** — Attached, Visible, Stable, Enabled, Receives Events - all must hold before an action like click() executes.
- **What happens if a check fails when an action is first attempted?** — Playwright retries the entire checklist automatically until every condition holds or the action's timeout (30s by default) is reached - it doesn't fail on the first failed check.
- **Why is page.waitForTimeout() before an action usually a mistake?** — It reintroduces the guessing game auto-waiting exists to remove - too short stays flaky, too long slows every run, and it doesn't fix whatever is actually failing the real actionability check.
- **What does a timeout error from a failed action actually tell you?** — The specific actionability check that never passed (e.g. "not visible," "outside of the viewport") - almost always a direct pointer at the real cause in the page.
- **"Receives Events" check — what does it actually catch?** — Something else (a modal backdrop, a loading spinner, an invisible overlay) sitting on top of the target element at the exact click point, even if the target itself looks fine.

### Challenge

Find or construct a page with a genuinely covering element (a cookie banner, a loading spinner that
lingers, or a fixed header that overlaps content on scroll). Write a test that clicks something behind
it, let the test fail naturally, and read the exact actionability check named in the error. Then fix
the real cause - not with a sleep - and confirm the test passes reliably across several runs.

### Ask the community

> My Playwright action keeps timing out with `[exact error text, e.g. element is not visible]` on an element I can see is on the page. Here's the relevant markup/screenshot: `[describe or paste it]`.

The exact wording of the actionability error, plus what's actually at that spot in the DOM (including
anything with a higher z-index), is usually enough for someone to spot the covering or hidden element
immediately.

- [Playwright — official Auto-waiting / actionability docs](https://playwright.dev/docs/actionability)
- [CircleCI — Mastering waits and timeouts in Playwright](https://circleci.com/blog/mastering-waits-and-timeouts-in-playwright/)

🎬 [Auto Wait In Playwright — How Playwright Waits Automatically Using Actionability Checks (Java) — Mukesh Otwani](https://www.youtube.com/watch?v=srkXpc7Ehbs) (9 min)

- Before most actions, Playwright checks five named conditions on the target element - Attached, Visible, Stable, Enabled, Receives Events - and retries automatically until all hold or the timeout is reached.
- No explicit sleep is required for this - and adding one anyway (page.waitForTimeout) reintroduces the exact guessing game auto-waiting exists to eliminate.
- A timeout error names the specific check still failing - that name is almost always a direct pointer at the real cause in the page, not a generic timing problem.
- "Receives Events" failures usually mean something else is covering the target at the click point, even when the target itself looks fine.
- Fixing the condition the error actually names (a covering overlay, a layout shift, a disabled state) eliminates flakiness; a longer sleep only slows the test while leaving the real race condition intact.


## Related notes

- [[Notes/playwright/setup-and-auto-waiting/installing-playwright|Installing Playwright]]
- [[Notes/playwright/setup-and-auto-waiting/typescript-setup|TypeScript setup]]
- [[Notes/playwright/setup-and-auto-waiting/first-test|First test]]


---
_Source: `packages/curriculum/content/notes/playwright/setup-and-auto-waiting/auto-waiting-explained.mdx`_
