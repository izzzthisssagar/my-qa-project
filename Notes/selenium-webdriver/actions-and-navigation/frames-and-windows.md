---
title: "Frames, windows, and explicit context switching"
tags: ["selenium", "webdriver", "interactions", "navigation", "track-d"]
updated: "2026-07-18"
---

# Frames, windows, and explicit context switching

*Track the active document and window handle, switch deliberately, and return to the parent context before locating the next element.*

> The element can be visible on screen and still be unreachable because WebDriver is searching a different document or window. Location always happens inside the current browsing context.

> **In real life**
>
> A bank hall has several labelled teller windows. Seeing all stations does not mean the clerk at one station can operate another. A WebDriver window handle selects the station; switching into an iframe selects a document inside it.

**browsing context**: A browsing context is the active document environment—top-level window or nested frame—against which WebDriver resolves subsequent commands.

## Act inside the right boundary

Frames and iframes contain separate documents. Switch by a located frame element when possible, interact inside it, then return with `parent_frame` or `default_content`. Index-based switching is fragile when frame order changes.

Tabs and windows share the window-handle model. Record the original handle, wait for the expected handle set after opening, identify the new handle deliberately, switch to it, and verify title or URL. Closing a window does not automatically prove the driver is focused on a valid remaining handle; switch back explicitly.

> **Tip**
>
> Log current handle, all handles, frame path, title, and URL when a context-sensitive locator fails.

> **Common mistake**
>
> Selecting the first handle that is not the original without waiting for the expected handle count or verifying the destination.

![Bank hall with separate labelled accountant and teller service windows](frames-and-windows.jpg)
*Tellers windows, Commonwealth Bank Hurstville — Sam Hood, public domain. [Source](https://commons.wikimedia.org/wiki/File:SLNSW_11353_Tellers_windows_Commonwealth_Bank_Hurstville.jpg)*
- **Target** — The visible target must belong to the active context and intended interaction.
- **Input boundary** — Element, prompt, frame, window, and device APIs are not interchangeable.
- **Transition** — The ordered command changes browser or application state.
- **Outcome oracle** — Observed final state proves the interaction achieved its purpose.

**A verified browser interaction**

1. **Identify boundary** — Choose element, prompt, frame, window, or input device.
2. **Establish context** — Locate or switch to the exact target.
3. **Perform sequence** — Send the smallest ordered interaction.
4. **Verify outcome** — Assert application state, not command completion alone.
5. **Restore context** — Release input and switch back when required.

## Real Selenium examples

These fenced samples require Selenium. The playground pair models ordering without a browser.

~~~python
original = driver.current_window_handle
driver.switch_to.frame(driver.find_element(By.ID, "payment-frame"))
assert driver.find_element(By.ID, "card").is_displayed()
driver.switch_to.default_content()
driver.switch_to.window(original)
~~~

~~~java
String original = driver.getWindowHandle();
driver.switchTo().frame(driver.findElement(By.id("payment-frame")));
assertTrue(driver.findElement(By.id("card")).isDisplayed());
driver.switchTo().defaultContent();
driver.switchTo().window(original);
~~~

*Run it — verify an ordered interaction (Python)*

```python
EXPECTED = "frame:payment>default-content>window:child>window:original"
EVENTS = ["frame:payment","default-content","window:child","window:original"]

def execute(events):
    trace = ">".join(events)
    if trace != EXPECTED:
        raise AssertionError(f"unexpected sequence={trace}")
    return trace, "frame=top window=original"

trace, state = execute(EVENTS)
sequence_accepted = trace == EXPECTED
assert sequence_accepted, "the intended interaction sequence must be accepted"
assert state == "frame=top window=original", "the final application/context state is the oracle"
print(f"TRACE {trace}")
print(f"STATE {state}")
print("RESULT sequence_accepted=true final_state_verified=true")
```

*Run it — verify an ordered interaction (Java)*

```java
import java.util.List;

public class Main {
    static final String EXPECTED = "frame:payment>default-content>window:child>window:original";
    record Result(String trace, String state) {}
    static Result execute(List<String> events) {
        String trace = String.join(">", events);
        if (!trace.equals(EXPECTED)) throw new AssertionError("unexpected sequence=" + trace);
        return new Result(trace, "frame=top window=original");
    }
    public static void main(String[] args) {
        Result result = execute(List.of("frame:payment", "default-content", "window:child", "window:original"));
        boolean sequenceAccepted = result.trace().equals(EXPECTED);
        if (!sequenceAccepted) throw new AssertionError("the intended interaction sequence must be accepted");
        if (!result.state().equals("frame=top window=original")) throw new AssertionError("the final state is the oracle");
        System.out.println("TRACE " + result.trace());
        System.out.println("STATE " + result.state());
        System.out.println("RESULT sequence_accepted=true final_state_verified=true");
    }
}
```

### Your first time: Your mission: prove one interaction

- [ ] Name the boundary — Identify element, select, alert, frame, window, or input device.
- [ ] Capture starting context — Record handle, frame path, target identity, and relevant state.
- [ ] Perform the minimum sequence — Keep input ordered and balance held device state.
- [ ] Assert the outcome — Verify visible, navigational, or persisted application state.

You now have a user-meaningful interaction oracle, not just a completed command.

- **The element is visible but not found.**
  Check the active window and frame before changing the locator.
- **Click is intercepted.**
  Inspect the center point, overlay, scrolling, and viewport rather than bypassing interactability.
- **A later test types uppercase unexpectedly.**
  Release held modifier keys or reset the session input state.
- **The command succeeds but behavior is wrong.**
  Strengthen the post-action oracle and verify the target identity.

### Where to check

- **Current context** — window handle, handle set, frame path, title, and URL.
- **Element evidence** — tag, enabled/displayed state, center-point obstruction, current value.
- **Prompt state** — alert text and chosen accept/dismiss response.
- **Input state** — focused element, pointer location, held keys/buttons, and action sequence.

### Worked example: the click that saved the wrong panel

A page contains two Save buttons. The command completes, but the test checks only that no exception was thrown. After a redesign, the first match belongs to a notification panel. The repaired test scopes the target, verifies identity, performs the interaction in the correct context, and asserts the profile confirmation and persisted value.

**Quiz.** What proves a WebDriver interaction succeeded?

- [ ] The command returned
- [ ] The element was found once
- [x] The intended application outcome was observed
- [ ] No screenshot was taken

*Command completion is transport evidence; the application outcome is the behavioral oracle.*

- **Interactability** — Whether WebDriver can perform the requested user-like element action.
- **Window handle** — A session-persistent identifier for one top-level browsing context.
- **Alert** — A browser prompt addressed outside the page DOM.
- **Input state** — Remembered pointer, button, and key state across action sequences.

### Challenge

Mutate EXPECTED in both playgrounds. The unchanged event sequence must make each program exit nonzero. Then remove the final restoration or key-release event and require the state oracle to reject the sequence.

### Ask the community

> Interaction [sequence] ran in window/frame [context] against [target]. The command result was [result], final state was [state], and logs showed [evidence]. Which boundary should I inspect?

Remove secrets, cookies, customer data, and private URLs.

- [Selenium — Frames](https://www.selenium.dev/documentation/webdriver/interactions/frames/)
- [Selenium — Windows and tabs](https://www.selenium.dev/documentation/webdriver/interactions/windows/)
- [Selenium Java API — TargetLocator](https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebDriver.TargetLocator.html)

🎬 [#5 - BrowserContext in Playwright || Handle Two different user sessions with BrowserContext](https://www.youtube.com/watch?v=0mfLHPLZ7_k) (18 min)

- Choose the API that matches the browser boundary.
- Command completion is not the application outcome.
- Frames and windows require explicit context management.
- Low-level input state must be balanced and restored.
- Real Selenium stays fenced; playgrounds model sequence deterministically.


## Related notes

- [[Notes/selenium-webdriver/actions-and-navigation/clicks-and-input|Clicks & input]]
- [[Notes/selenium-webdriver/actions-and-navigation/dropdowns-and-alerts|Dropdowns & alerts]]
- [[Notes/selenium-webdriver/actions-and-navigation/actions-api|Actions API]]


---
_Source: `packages/curriculum/content/notes/selenium-webdriver/actions-and-navigation/frames-and-windows.mdx`_
