---
title: "Native dropdowns and browser alerts"
tags: ["selenium", "webdriver", "interactions", "navigation", "track-d"]
updated: "2026-07-18"
---

# Native dropdowns and browser alerts

*Distinguish HTML select controls from custom widgets and switch explicitly to browser alerts before reading, accepting, dismissing, or typing.*

> A native select, a styled menu, and a JavaScript alert can look like choices on screen, but they cross three different automation interfaces. Using the wrong interface fails for the right reason.

> **In real life**
>
> Nesting dolls look like one family but each shell opens at a different boundary. A native select opens through Selenium's Select helper; a custom dropdown is ordinary DOM interaction; a browser alert requires switching to the prompt boundary.

**user prompt**: A user prompt is a browser-level alert, confirm, or prompt dialog that WebDriver addresses through the active alert interface rather than the page DOM.

## Act inside the right boundary

Selenium support classes wrap real HTML `select` elements and expose selection by visible text, value, or index plus selected-option inspection. They do not work for custom div-based comboboxes; those must be tested through their actual DOM and keyboard behavior.

JavaScript alerts, confirms, and prompts are not DOM elements. Switch to the active alert, inspect its text, then accept, dismiss, or send text where supported. Wait for the alert when its appearance is asynchronous. After resolution, assert the page state produced by the chosen response.

> **Tip**
>
> Inspect the element tag first. Use Select only for a real select; preserve user-facing tests for custom widgets.

> **Common mistake**
>
> Trying to locate an alert message with a CSS selector. Browser prompts live outside the document DOM.

![Seven decorated matryoshka dolls arranged from smallest to largest](dropdowns-and-alerts.jpg)
*7 piece Matryoshka dolls, Queensland, 2021 — Kgbo, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:7_piece_Matryoshka_dolls,_Queensland,_2021.jpg)*
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
Select(driver.find_element(By.ID, "country")).select_by_value("CA")
alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
assert alert.text == "Continue?"
alert.accept()
~~~

~~~java
new Select(driver.findElement(By.id("country"))).selectByValue("CA");
Alert alert = new WebDriverWait(driver, Duration.ofSeconds(5)).until(ExpectedConditions.alertIsPresent());
assertEquals("Continue?", alert.getText());
alert.accept();
~~~

*Run it — verify an ordered interaction (Python)*

```python
EXPECTED = "select:CA>alert-text:Continue?>alert:accept"
EVENTS = ["select:CA","alert-text:Continue?","alert:accept"]

def execute(events):
    trace = ">".join(events)
    if trace != EXPECTED:
        raise AssertionError(f"unexpected sequence={trace}")
    return trace, "option=CA alert=accepted"

trace, state = execute(EVENTS)
sequence_accepted = trace == EXPECTED
assert sequence_accepted, "the intended interaction sequence must be accepted"
assert state == "option=CA alert=accepted", "the final application/context state is the oracle"
print(f"TRACE {trace}")
print(f"STATE {state}")
print("RESULT sequence_accepted=true final_state_verified=true")
```

*Run it — verify an ordered interaction (Java)*

```java
import java.util.List;

public class Main {
    static final String EXPECTED = "select:CA>alert-text:Continue?>alert:accept";
    record Result(String trace, String state) {}
    static Result execute(List<String> events) {
        String trace = String.join(">", events);
        if (!trace.equals(EXPECTED)) throw new AssertionError("unexpected sequence=" + trace);
        return new Result(trace, "option=CA alert=accepted");
    }
    public static void main(String[] args) {
        Result result = execute(List.of("select:CA", "alert-text:Continue?", "alert:accept"));
        boolean sequenceAccepted = result.trace().equals(EXPECTED);
        if (!sequenceAccepted) throw new AssertionError("the intended interaction sequence must be accepted");
        if (!result.state().equals("option=CA alert=accepted")) throw new AssertionError("the final state is the oracle");
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

- [Selenium — Select lists](https://www.selenium.dev/documentation/webdriver/support_features/select_lists/)
- [Selenium — Alerts](https://www.selenium.dev/documentation/webdriver/interactions/alerts/)
- [Selenium Java API — Alert](https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/Alert.html)

🎬 [Selenium Tutorial for Beginners using Python | Selenium for Web Scraping (With Project)](https://www.youtube.com/watch?v=XI5_nsClCYI) (37 min)

- Choose the API that matches the browser boundary.
- Command completion is not the application outcome.
- Frames and windows require explicit context management.
- Low-level input state must be balanced and restored.
- Real Selenium stays fenced; playgrounds model sequence deterministically.


## Related notes

- [[Notes/selenium-webdriver/actions-and-navigation/clicks-and-input|Clicks & input]]
- [[Notes/selenium-webdriver/actions-and-navigation/frames-and-windows|Frames & windows]]
- [[Notes/selenium-webdriver/actions-and-navigation/actions-api|Actions API]]


---
_Source: `packages/curriculum/content/notes/selenium-webdriver/actions-and-navigation/dropdowns-and-alerts.mdx`_
