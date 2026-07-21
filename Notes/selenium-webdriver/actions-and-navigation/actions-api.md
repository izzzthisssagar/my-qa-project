---
title: "Actions API: sequences, device state, and cleanup"
tags: ["selenium", "webdriver", "interactions", "navigation", "track-d"]
updated: "2026-07-18"
---

# Actions API: sequences, device state, and cleanup

*Build low-level pointer and keyboard sequences only when high-level element commands are insufficient, then release state and assert the outcome.*

> A held Shift key is session state, not a one-line detail. If an action sequence fails before key-up, later tests can inherit a modifier you forgot was still pressed.

> **In real life**
>
> A mouse has distinct pointer movement, buttons, and a wheel; the browser remembers their state across a sequence. The Actions API is the control surface for those devices, not a stronger version of every ordinary click.

**Actions API**: The Actions API is WebDriver's low-level interface for composing synchronized virtual keyboard, pointer, pen, touch, and wheel input sources.

## Act inside the right boundary

Use high-level WebElement click and sendKeys for ordinary controls. Use Actions when behavior depends on hover, drag, chorded keys, pointer offsets, click-and-hold, or wheel input. Java `Actions` and Python `ActionChains` build sequences and send them with `perform`.

Input sources are stateful across the session. Keep key-down and key-up balanced, release held pointer buttons, and clear input state after interrupted or intentionally incomplete sequences. Synchronize on the application outcome after `perform`; execution of the input sequence is not the business oracle.

> **Tip**
>
> Keep action chains short and name the user gesture they model; long chains make the failing device transition hard to locate.

> **Common mistake**
>
> Replacing every intercepted click with an Actions chain. A center-point obstruction may be a product defect, not a need for lower-level input.

![Three-button computer mouse with left and right buttons, wheel, body, and cable](actions-api.jpg)
*3-button Microsoft mouse — Darkone, CC BY-SA 2.5. [Source](https://commons.wikimedia.org/wiki/File:3-Tasten-Maus_Microsoft.jpg)*
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
ActionChains(driver).move_to_element(card).key_down(Keys.SHIFT).send_keys("a").key_up(Keys.SHIFT).click().perform()
assert card.get_attribute("value") == "A"
~~~

~~~java
new Actions(driver).moveToElement(card).keyDown(Keys.SHIFT).sendKeys("a").keyUp(Keys.SHIFT).click().perform();
assertEquals("A", card.getAttribute("value"));
~~~

*Run it — verify an ordered interaction (Python)*

```python
EXPECTED = "move:card>key-down:SHIFT>type:a>key-up:SHIFT>click:card"
EVENTS = ["move:card","key-down:SHIFT","type:a","key-up:SHIFT","click:card"]

def execute(events):
    trace = ">".join(events)
    if trace != EXPECTED:
        raise AssertionError(f"unexpected sequence={trace}")
    return trace, "pointer=card keys=released value=A clicked=true"

trace, state = execute(EVENTS)
sequence_accepted = trace == EXPECTED
assert sequence_accepted, "the intended interaction sequence must be accepted"
assert state == "pointer=card keys=released value=A clicked=true", "the final application/context state is the oracle"
print(f"TRACE {trace}")
print(f"STATE {state}")
print("RESULT sequence_accepted=true final_state_verified=true")
```

*Run it — verify an ordered interaction (Java)*

```java
import java.util.List;

public class Main {
    static final String EXPECTED = "move:card>key-down:SHIFT>type:a>key-up:SHIFT>click:card";
    record Result(String trace, String state) {}
    static Result execute(List<String> events) {
        String trace = String.join(">", events);
        if (!trace.equals(EXPECTED)) throw new AssertionError("unexpected sequence=" + trace);
        return new Result(trace, "pointer=card keys=released value=A clicked=true");
    }
    public static void main(String[] args) {
        Result result = execute(List.of("move:card", "key-down:SHIFT", "type:a", "key-up:SHIFT", "click:card"));
        boolean sequenceAccepted = result.trace().equals(EXPECTED);
        if (!sequenceAccepted) throw new AssertionError("the intended interaction sequence must be accepted");
        if (!result.state().equals("pointer=card keys=released value=A clicked=true")) throw new AssertionError("the final state is the oracle");
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

- [Selenium — Actions API](https://www.selenium.dev/documentation/webdriver/actions_api/)
- [Selenium — Mouse actions](https://www.selenium.dev/documentation/webdriver/actions_api/mouse/)
- [Selenium — Keyboard actions](https://www.selenium.dev/documentation/webdriver/actions_api/keyboard/)

🎬 [JavaScript Course for Beginners – Your First Step to Web Development](https://www.youtube.com/watch?v=W6NZfCO5SIk) (48 min)

- Choose the API that matches the browser boundary.
- Command completion is not the application outcome.
- Frames and windows require explicit context management.
- Low-level input state must be balanced and restored.
- Real Selenium stays fenced; playgrounds model sequence deterministically.


## Related notes

- [[Notes/selenium-webdriver/actions-and-navigation/clicks-and-input|Clicks & input]]
- [[Notes/selenium-webdriver/actions-and-navigation/dropdowns-and-alerts|Dropdowns & alerts]]
- [[Notes/selenium-webdriver/actions-and-navigation/frames-and-windows|Frames & windows]]


---
_Source: `packages/curriculum/content/notes/selenium-webdriver/actions-and-navigation/actions-api.mdx`_
