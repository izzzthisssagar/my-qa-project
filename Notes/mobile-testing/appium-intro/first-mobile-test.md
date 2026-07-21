---
title: "First mobile test"
tags: ["mobile-testing", "appium-intro", "track-c"]
updated: "2026-07-21"
---

# First mobile test

*Every first Appium script follows the same five-step shape: start a session with capabilities, find one element, interact with it, assert an outcome, and end the session — the last step matters more than it looks.*

> A first Appium script looks intimidating until it's broken into its actual shape: five steps, most of them
> one line each. The part that quietly determines whether tomorrow's test suite runs at all isn't the tap or
> the assertion — it's whether the very last step ever gets a chance to run.

> **In real life**
>
> Borrowing a shared meeting room follows the same shape every time: book it (start a session), find the
> right room (find an element), use it for what you came to do (interact), confirm you got what you needed
> (assert), and check out so the next person can book it (end the session). Skipping checkout doesn't undo
> the meeting that already happened — it just leaves the room looking occupied to everyone who tries to book
> it next, for a problem that has nothing to do with their meeting.

**A first mobile test**: A first mobile test, in Appium, is a script that follows five steps in order: start a session by sending a capabilities object, find one element on screen, interact with it (tap or type), assert that the interaction produced the expected outcome, and end the session so the device or emulator is released.

## The five-step shape

Every Appium script, no matter the language or app, follows the same shape underneath. First, a session
starts by sending a capabilities object — the same object covered in setup — and the driver blocks until the
app is installed and launched on the target device or emulator. Second, the script finds exactly one
element it needs, using a locator strategy such as accessibility id. Third, it interacts with that element:
`click()`/`tap()` for a button, `send_keys()`/`sendKeys()` for a text field — the same method names Selenium
testers already use, since Appium's client libraries mirror that shape on purpose. Fourth, it asserts that
the interaction produced the expected result, usually by reading text or an attribute back from another
element. Fifth, the session ends.

That fifth step is easy to treat as an afterthought, but it isn't optional. A session is a real, held
resource — a specific device or emulator instance that no other test can use while it's active. A script
that only calls `driver.quit()` at the bottom of its happy path, after the assertion, never reaches that
line when the assertion fails first. The session stays open, and the device it was holding looks busy to
every test that runs after it, for a failure that has nothing to do with those later tests.

## Where the language-specific detail actually lives

The five steps above are the same in Python and Java; what differs is syntax, not shape. A Python script
typically starts a session in a `setUp` method and ends it in `tearDown`, so the framework itself guarantees
the session closes even when a test fails partway through. A Java script using JUnit or TestNG uses the
equivalent `@Before`/`@After` (or `@BeforeMethod`/`@AfterMethod`) hooks for the same reason. Neither language
makes the mistake harder to make — a `driver.quit()` call placed at the end of a test method's body instead
of in a teardown hook has exactly the same leak risk in both.

> **Tip**
>
> Put the session-ending call in a teardown hook or a `finally` block, never at the bottom of the happy path.
> That one placement decision is the difference between a failing assertion costing one test and a failing
> assertion costing every test that runs after it in the same suite.

> **Common mistake**
>
> Do not assume a passing test proves the whole script is safe. A script that passes every time in isolation
> can still leak sessions the moment an assertion starts failing — verify the cleanup step specifically, by
> deliberately breaking an assertion once and confirming the session still ends.

![A woman seated at a desk with two computer monitors, holding a black smartphone connected to the computer by a cable and tapping its screen](first-mobile-test.jpg)
*Developers working on the Talk. They Hear You. mobile app — SAMHSA, Wikimedia Commons, Public domain. [Source](https://commons.wikimedia.org/wiki/File:Developers_working_on_the_%E2%80%9CTalk._They_Hear_You.%E2%80%9D_mobile_app._(14649388733).jpg)*
- **Where the script lives and runs** — The desktop side is where the test code sits — the process that will send the capabilities object and every command afterward, none of which touch this screen directly.
- **Where the next command gets written, not where it runs** — The keyboard is for editing the script and reading results back. The actual tap and type happen on the device beside it, not here.
- **The device a session actually holds** — This is the real target of every find-element, tap, and assert call in the script — a specific physical device, held for the whole session.
- **The literal link the commands travel over** — For a real Android device this cable carries the same USB/ADB connection UiAutomator2 uses — sever it mid-session and every remaining step in the script fails.

**One script, five steps**

1. **Start a session** — Send the capabilities object; the driver blocks until the app is installed and launched on the target.
2. **Find one element** — Locate it by accessibility id or another platform-specific strategy before interacting with it.
3. **Interact with it** — tap()/click() for a button, send_keys()/sendKeys() for a text field.
4. **Assert the outcome** — Read text or an attribute back and compare it to what the interaction should have produced.
5. **End the session — always** — In a teardown hook or finally block, so a failed assertion still releases the device for the next test.

*The five-step shape, simulated locally (Python)*

```python
class FakeAppiumSession:
    def __init__(self):
        self.active = False
        self.screen = {"login_button": "LOGIN", "welcome_label": None}

    def start_session(self, caps):
        self.active = True
        print("SESSION_START platform=" + caps["platformName"] + " automation=" + caps["appium:automationName"])

    def find_element(self, accessibility_id):
        if not self.active:
            raise RuntimeError("no active session")
        if accessibility_id not in self.screen:
            raise RuntimeError("element not found: " + accessibility_id)
        print("FIND_ELEMENT accessibility_id=" + accessibility_id)
        return accessibility_id

    def tap(self, element_id):
        print("TAP element=" + element_id)
        if element_id == "login_button":
            self.screen["welcome_label"] = "Welcome back"

    def assert_text(self, element_id, expected):
        actual = self.screen.get(element_id)
        print("ASSERT element=" + element_id + " expected=" + str(expected) + " actual=" + str(actual))
        assert actual == expected, "assertion failed for " + element_id

    def end_session(self):
        self.active = False
        print("SESSION_END")

caps = {"platformName": "Android", "appium:automationName": "UiAutomator2", "appium:deviceName": "Pixel8", "appium:app": "/apps/shop-debug.apk"}

session = FakeAppiumSession()
session.start_session(caps)
login_button = session.find_element("login_button")
session.tap(login_button)
session.assert_text("welcome_label", "Welcome back")
session.end_session()

print("RESULT=PASS")
```

*The five-step shape, simulated locally (Java)*

```java
import java.util.HashMap;
import java.util.Map;

public class Main {
    static class FakeAppiumSession {
        boolean active = false;
        Map<String, String> screen = new HashMap<>();

        FakeAppiumSession() {
            screen.put("login_button", "LOGIN");
            screen.put("welcome_label", null);
        }

        void startSession(Map<String, String> caps) {
            active = true;
            System.out.println("SESSION_START platform=" + caps.get("platformName") + " automation=" + caps.get("appium:automationName"));
        }

        String findElement(String accessibilityId) {
            if (!active) throw new RuntimeException("no active session");
            if (!screen.containsKey(accessibilityId)) throw new RuntimeException("element not found: " + accessibilityId);
            System.out.println("FIND_ELEMENT accessibility_id=" + accessibilityId);
            return accessibilityId;
        }

        void tap(String elementId) {
            System.out.println("TAP element=" + elementId);
            if (elementId.equals("login_button")) {
                screen.put("welcome_label", "Welcome back");
            }
        }

        void assertText(String elementId, String expected) {
            String actual = screen.get(elementId);
            System.out.println("ASSERT element=" + elementId + " expected=" + expected + " actual=" + actual);
            if (!expected.equals(actual)) throw new AssertionError("assertion failed for " + elementId);
        }

        void endSession() {
            active = false;
            System.out.println("SESSION_END");
        }
    }

    public static void main(String[] args) {
        Map<String, String> caps = new HashMap<>();
        caps.put("platformName", "Android");
        caps.put("appium:automationName", "UiAutomator2");
        caps.put("appium:deviceName", "Pixel8");
        caps.put("appium:app", "/apps/shop-debug.apk");

        FakeAppiumSession session = new FakeAppiumSession();
        session.startSession(caps);
        String loginButton = session.findElement("login_button");
        session.tap(loginButton);
        session.assertText("welcome_label", "Welcome back");
        session.endSession();

        System.out.println("RESULT=PASS");
    }
}
```

### Your first time: Write and run one first Appium script

- [ ] Start a session with a capabilities object — platformName, appium:automationName, appium:deviceName, appium:app — the call blocks until the app launches.
- [ ] Find exactly one element — Capture its accessibility id or resource id from an inspector first, rather than guessing it from the app's source.
- [ ] Interact with it once — tap()/click() for a button, send_keys()/sendKeys() for a text field — one interaction per script while it's new.
- [ ] Assert one concrete outcome — Read text or an attribute back and compare it to the exact value the interaction should have produced.
- [ ] End the session in a teardown hook — setUp/tearDown in Python, @Before/@After in Java — never only at the bottom of the happy path.

- **The script hangs indefinitely right after starting the session.**
  The app under test never actually launched. Confirm the appium:app path or bundle id is correct by launching it manually first.
- **find_element raises a no-such-element error even though the button is visible on screen.**
  The locator strategy or identifier is wrong. Confirm the real accessibility id with an inspector rather than assuming it from the app's source.
- **The test passes locally but the device is unusable for the very next test.**
  The session was never ended, usually because the quit()/end-session call lives only at the end of the happy path instead of a teardown hook.
- **An assertion fails even though the tap clearly worked on screen a moment later.**
  The assertion read the element before the UI finished updating. Wait for the expected state instead of asserting immediately after the interaction.

### Where to check

- The Appium documentation's quickstart guide for the exact driver-construction syntax in your client language.
- Your test framework's setup/teardown hooks, to guarantee the session always ends even when a test fails.
- [[mobile-testing/appium-intro/setup]] for the capabilities object the first step depends on.
- [[mobile-testing/appium-intro/mobile-locators]] for choosing and confirming the identifier a find-element call uses.
- [[mobile-testing/appium-intro/what-appium-is]] for why this five-step shape mirrors a Selenium test almost exactly.

### Worked example: a script that passes today and blocks tomorrow's suite

1. A first script starts a session, finds the login button, taps it, and asserts a welcome message — every
   step passes.
2. The very next test in the same suite fails immediately at session start with a device-busy-style error.
3. The cause: an earlier version of the script called quit() only after the assertion line, so a run where
   the assertion had failed never reached it, and that session stayed open holding the device.
4. Moving the session-ending call into a teardown hook fixes both today's script and every future test's
   cleanup, regardless of whether the assertion passes or fails.

**Quiz.** Which step in a first Appium script is most commonly forgotten in a way that affects tests beyond the current one?

- [ ] Starting the session, since no test can run at all without it
- [x] Ending the session, since a session left open still holds the device or emulator and can block every test that runs after it
- [ ] Finding an element, since Appium locates elements automatically without being asked
- [ ] Asserting an outcome, since a failed assertion has no effect on other tests

*A session is a held resource. If the ending call only sits at the bottom of the happy path, a failed assertion skips it entirely and the device stays locked for whatever test runs next.*

- **Five-step shape of a first Appium script** — Start a session with capabilities, find an element, interact with it, assert an outcome, end the session.
- **Why end the session in a teardown, not the happy path** — A session left open after a failed assertion still holds the device or emulator, which can block the next test from starting.
- **Python's guarantee for session cleanup** — A tearDown method (or equivalent fixture) runs even when the test method fails, so quit() belongs there, not at the end of the test body.
- **What stays the same across platforms in this shape** — The five steps themselves; only the capabilities and the exact locator values used to find elements change per platform.

### Challenge

Write out the five steps of a first Appium script for one screen in an app you know, including the exact locator you'd need for the element you interact with, then mark which of the five steps a rushed first draft is most likely to get wrong.

- [Appium Documentation — Write a Test (Python)](https://appium.io/docs/en/2.0/quickstart/test-py/)
- [Appium Documentation — Capabilities](https://appium.io/docs/en/2.0/guides/caps/)
- [Appium Beginner Tutorial 7 — First Appium Project with Java](https://www.youtube.com/watch?v=N7vY3cPSo8g)

🎬 [Appium Beginner Tutorial 7 — First Appium Project with Java](https://www.youtube.com/watch?v=N7vY3cPSo8g) (22 min)

- Every first Appium script follows the same five-step shape: start a session, find an element, interact, assert, end the session.
- The session-ending call belongs in a teardown hook or finally block, not at the bottom of the happy path.
- A session left open after a failed assertion still holds its device or emulator, which can block the next test in the suite.
- Python and Java differ in syntax, not in shape — setUp/tearDown and @Before/@After exist for the same reason.


## Related notes

- [[Notes/mobile-testing/appium-intro/setup|Setup]]
- [[Notes/mobile-testing/appium-intro/mobile-locators|Mobile locators]]
- [[Notes/mobile-testing/appium-intro/what-appium-is|What Appium is]]


---
_Source: `packages/curriculum/content/notes/mobile-testing/appium-intro/first-mobile-test.mdx`_
