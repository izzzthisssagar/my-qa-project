---
title: "The POM pattern"
tags: ["framework-design", "page-object-model", "track-d"]
updated: "2026-07-17"
---

# The POM pattern

*The Page Object Model gives each real page in the app one class that owns its locators and actions, so tests read as page-level intent - and when the UI changes, you fix one page class instead of every test that touches that page.*

> Forty tests each contain their own copy of `driver.findElement(By.id("login-btn")).click()`. One
> Tuesday a developer renames that id, and forty tests go red for the same one-line reason. The Page
> Object Model exists so that Tuesday costs you one edit in one class - not an afternoon of
> find-and-replace across a test suite.

> **In real life**
>
> A universal remote control is one object that encapsulates everything you can do to one specific
> system. Its buttons are named by intent - GUIDE, VOL, MUTE, DVR - not by the infrared pulse codes
> they actually transmit. The household presses the same labeled buttons every day without knowing a
> single code. When the cable box is swapped for a new model, someone reprograms the remote once, and
> every person who uses it keeps pressing exactly the same buttons. Nobody re-learns anything, because
> nobody ever depended on the codes - only on the labels.

**Page Object Model**: The Page Object Model (POM) is a test-code design pattern in which each real page (or major screen) of the application under test gets one class that encapsulates two things: the locators that find that page's elements, and public methods representing the actions a user can perform there. Tests interact with pages only through those methods - loginPage.enterCredentials(...), loginPage.submit() - never through raw driver calls. Because every locator lives in exactly one class, a UI change is absorbed by editing that one page class, while the tests that use it remain untouched.

## From scattered driver calls to page-level intent

Without the pattern, every test speaks raw Selenium and owns its own copies of every locator:

```java
// Test knows HOW the page is built - and so does every other test
driver.findElement(By.id("username")).sendKeys("standard_user");
driver.findElement(By.id("password")).sendKeys("secret_sauce");
driver.findElement(By.id("login-btn")).click();
```

With the pattern, the page's knowledge moves into one class, and the test speaks user intent:

```java
public class LoginPage {
    private final WebDriver driver;
    private final By username = By.id("username");
    private final By password = By.id("password");
    private final By loginButton = By.id("login-btn");

    public LoginPage(WebDriver driver) {
        this.driver = driver;
    }

    public void enterCredentials(String user, String pass) {
        driver.findElement(username).sendKeys(user);
        driver.findElement(password).sendKeys(pass);
    }

    public void submit() {
        driver.findElement(loginButton).click();
    }
}

// The test now reads as a sequence of page-level actions
LoginPage loginPage = new LoginPage(driver);
loginPage.enterCredentials("standard_user", "secret_sauce");
loginPage.submit();
```

- **One class per real page** (or major screen) - LoginPage, CartPage, CheckoutPage - mirroring how
  a user actually experiences the app.
- **Locators live only inside the page class** - a test that never sees a `By` can never break when
  one changes.
- **Methods are user actions**, named by intent - the pattern is framework-agnostic and works the
  same way in Playwright, Cypress, or WebDriverIO; only the driver calls inside the class differ.
- **The payoff is a single point of change** - when the login form is redesigned, LoginPage is the
  only file that knows, and the forty tests that log in stay exactly as they are.

> **Tip**
>
> Build page objects for the pages your tests actually touch, as they touch them - don't map the whole
> application up front. A LoginPage with two methods that three real tests use today beats twenty
> speculative page classes nobody calls yet, and the pattern grows naturally one page at a time.

> **Common mistake**
>
> Writing a "page object" that is really just a thin wrapper around the driver - methods like
> `click(By locator)` and `type(By locator, String text)` that still make every test supply its own
> locators. That keeps all the ceremony of the pattern while giving up its entire payoff: the locators
> are still scattered through the tests, so a UI change still means editing every test that touches
> the page.

![A silver Cablevision universal remote control lying on a wooden floor, showing TV and CBL device buttons at the top, a SEL button with arrow keys, labeled GUIDE, INFO and FAV buttons, VOL and CH rockers, a green DVR button, a numeric keypad, and the model number UR2-CBL-CV04 printed at the bottom](the-pom-pattern.jpg)
*Cablevision UR2-CBL-CV04 universal remote — Wikimedia Commons, CC BY-SA 4.0 (Jonathan Schilling). [Source](https://commons.wikimedia.org/wiki/File:Cablevision_UR2-CBL-CV04_universal_remote.jpg)*
- **TV / CBL device buttons — one object per system it drives** — The remote dedicates a mode to each specific device it controls, the way POM dedicates one class to each real page of the app under test.
- **GUIDE, INFO, FAV — buttons named by intent** — Nobody presses 'transmit pulse code 0x2F' - they press GUIDE. Page object methods are named the same way: submitOrder(), not clickButton3().
- **The keypad — low-level inputs hidden behind the shell** — The raw signals live inside the device, out of sight - like locators and driver calls living privately inside the page class instead of inside every test.
- **The model number — the one thing to reprogram when hardware changes** — Swap the cable box and one person reprograms this one remote once; every user keeps pressing the same buttons. Change the UI and one person edits one page class; every test keeps calling the same methods.

**The same UI change, with and without page objects**

1. **A developer renames the login button's id** — 'login-btn' becomes 'signin-button' - a routine front-end refactor, no behavior change.
2. **Without POM: forty tests each own a copy of the old locator** — Every test that logs in goes red at once, each for the identical one-line reason.
3. **With POM: one LoginPage class owns that locator, once** — The same forty tests call loginPage.submit() - none of them ever saw the id.
4. **One edit in one file** — Update the By.id inside LoginPage. Nothing else in the suite mentions it.
5. **Forty tests green again, untouched** — The change was absorbed exactly where the knowledge lived - the whole point of the pattern.

The heart of the pattern is a bookkeeping fact: how many places know each locator. Here's that
maintenance math as a small, generic simulation.

*Run it - count the edits a locator rename costs, with and without page objects (Python)*

```python
# Forty tests all need the login button. Two ways to organize that knowledge.

tests = [f"test_{i}" for i in range(1, 41)]

# Without POM: every test carries its own copy of the locator
scattered = {test: {"login_button": "id=login-btn"} for test in tests}

# With POM: one page class owns it; tests only hold a reference to the page
page_objects = {"LoginPage": {"login_button": "id=login-btn"}}

def edits_needed(owners, old, new):
    places = [name for name, locs in owners.items()
              if old in locs.values()]
    return places

renamed_from, renamed_to = "id=login-btn", "id=signin-button"

print("UI change: login button id renamed")
print(f"Without POM: {len(edits_needed(scattered, renamed_from, renamed_to))} files to edit")
print(f"With POM:    {len(edits_needed(page_objects, renamed_from, renamed_to))} file to edit")
print()
print("Same suite, same change - the difference is only WHERE the knowledge lives.")
```

Same maintenance math in Java.

*Run it - count the edits a locator rename costs, with and without page objects (Java)*

```java
import java.util.*;

public class Main {
    static List<String> editsNeeded(Map<String, String> owners, String oldLocator) {
        List<String> places = new ArrayList<>();
        for (Map.Entry<String, String> e : owners.entrySet()) {
            if (e.getValue().equals(oldLocator)) {
                places.add(e.getKey());
            }
        }
        return places;
    }

    public static void main(String[] args) {
        String locator = "id=login-btn";

        // Without POM: every test carries its own copy of the locator
        Map<String, String> scattered = new LinkedHashMap<>();
        for (int i = 1; i <= 40; i++) {
            scattered.put("test_" + i, locator);
        }

        // With POM: one page class owns it
        Map<String, String> pageObjects = Map.of("LoginPage", locator);

        System.out.println("UI change: login button id renamed");
        System.out.println("Without POM: " + editsNeeded(scattered, locator).size() + " files to edit");
        System.out.println("With POM:    " + editsNeeded(pageObjects, locator).size() + " file to edit");
        System.out.println();
        System.out.println("Same suite, same change - the difference is only WHERE the knowledge lives.");
    }
}
```

### Your first time: Your mission: refactor one raw test into a page object and break the UI on purpose

- [ ] Write (or find) one test that logs in using raw driver calls — Direct findElement + sendKeys + click against a practice site like SauceDemo - the 'before' state.
- [ ] Extract a LoginPage class: locators as private fields, enterCredentials() and submit() as public methods — The test should end up with zero By locators and zero findElement calls of its own.
- [ ] Simulate a UI change: alter one locator so it no longer matches — Change By.id('login-btn') to a wrong value inside the page class only.
- [ ] Run the test, then fix the locator in the page class and run again — Notice the failure pointed at one class, the fix touched one class, and the test file was never edited.

You've now performed the exact maintenance event the pattern exists for - and felt it cost one edit.

- **A locator changed and you still had to edit a dozen files.**
  The locator was duplicated - some tests bypass the page object and call the driver directly. Hunt down raw findElement calls in test code and route them through the page class, so the next change really does cost one edit.
- **Page classes have ballooned into thousand-line god objects that everyone is afraid to touch.**
  The class is probably modeling more than one real page, or absorbing reusable widgets that belong in component objects. Split by what a user would call a distinct screen, and pull shared UI (nav bar, modals) into composed components.
- **Tests are green but unreadable - a wall of page method calls with no visible intent.**
  Method naming has drifted toward mechanics (clickFirstRow, typeInBox) instead of user intent (openOldestOrder, applyCoupon). Rename methods after what the user is trying to accomplish and the test becomes its own documentation.
- **Two teammates wrote two different page objects for the same page.**
  There's no shared map of which pages already have classes. Agree on one package per app area, one class per real page, named after the page - and make a quick search of that package part of the habit before writing a new one.

### Where to check

- **Your test files, for raw `findElement`/locator literals** — every one found in a test (rather
  than a page class) is a future multi-file edit waiting to happen.
- **The page-objects package structure** — one class per real page, named after the page, is the
  quickest health check on whether the pattern is actually being followed.
- **The diff of your last UI-driven test fix** — if it touched many test files for one UI change,
  the locators are still scattered regardless of what the classes are called.
- **Selenium's official Page Object Models documentation** — the canonical description of the
  pattern, its motivations, and the conventions this chapter's other notes build on.

### Worked example: the checkout redesign that cost one afternoon instead of one sprint

1. An e-commerce team has 60 UI tests; 25 of them pass through checkout. The checkout flow is built
   as three page classes: CartPage, PaymentPage, ConfirmationPage.
2. A redesign ships: the payment form is rebuilt with a new component library, and every field id,
   button, and error banner on that page changes.
3. The nightly run goes red - all 25 checkout tests fail. Triage takes minutes, because every
   failure's stack trace points into the same file: PaymentPage.
4. One engineer updates PaymentPage's locators against the new markup - about 15 lines - and reruns
   the suite. All 25 tests pass. Not one test file was opened, let alone edited.
5. The team's estimate history tells the real story: the same class of redesign, before the POM
   refactor, took a full sprint of test fixing. The pattern turned a suite-wide event into a
   single-file event.

**Quiz.** A team adopts POM and writes a LoginPage class - but tests still do driver.findElement(By.id('login-btn')).click() directly whenever it feels quicker. What is the actual consequence?

- [ ] None - as long as the page class exists, the pattern's benefit is secured
- [ ] The tests run measurably slower because the page class adds an extra layer of calls
- [x] The single-point-of-change payoff is lost for every locator that also lives in a test: the next UI rename still breaks and requires editing every one of those tests, exactly as if POM had never been adopted
- [ ] Selenium will throw an exception when a locator is used outside a page class

*The pattern's entire payoff comes from each locator having exactly one owner - any test that carries its own copy re-creates the scattered-knowledge problem for that locator, so the next rename is once again a multi-file edit. Option one confuses having the class with using it; the benefit comes from routing all interaction through it. Option two is backwards - a method call's overhead is negligible and speed was never the pattern's point. Option four invents an enforcement mechanism that doesn't exist: Selenium neither knows nor cares about page objects, which is precisely why the discipline has to come from the team.*

- **What two things does a page object encapsulate?** — That page's locators (how to find its elements) and the actions a user can perform on it (public methods named by intent).
- **The core payoff of POM in one sentence** — When the UI changes, you fix one page class - not every test that touches that page - because each locator has exactly one owner.
- **What should a test look like under POM?** — A sequence of page-level actions - loginPage.enterCredentials(...), loginPage.submit() - with zero raw driver calls or locators of its own.
- **Is POM specific to Selenium?** — No - it's a framework-agnostic design pattern. The same one-class-per-page structure works in Playwright, Cypress, or WebDriverIO; only the driver calls inside the class differ.
- **The universal-remote analogy for POM** — Buttons named by intent (GUIDE, VOL) = page methods; the infrared codes inside = locators; reprogramming the remote once for a new cable box = editing one page class for a UI change while every user/test keeps the same interface.

### Challenge

Take any suite you have access to (yours, a teammate's, or an open-source example) and audit five UI
tests: count how many raw locator literals appear inside test code versus inside page classes. Pick
the locator that appears in the most places, imagine it renamed tomorrow, and write down the exact
list of files you'd have to edit. Then refactor just that one locator behind a page object and
compare the two lists.

### Ask the community

> I'm introducing page objects into an existing suite of `[N]` tests. Here's a representative test: `[paste it]`. Which pages would you extract first, and what would you leave alone for now?

Sharing one real test usually gets better guidance than describing the suite in the abstract -
experienced reviewers can point at the exact lines that should become page methods, and just as
importantly, at the parts not worth abstracting yet.

- [Selenium — official Page Object Models documentation](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [Martin Fowler — PageObject](https://martinfowler.com/bliki/PageObject.html)

🎬 [Selenium Page Object Model Explained In 5 Minutes — Automation by Rain the Dog](https://www.youtube.com/watch?v=GKDJk4s_T-s) (6 min)

- POM gives each real page of the app one class owning that page's locators and the user actions it supports.
- Tests interact only through page methods and read as page-level intent - loginPage.submit() - never raw driver calls.
- The payoff is single-point-of-change: a UI change is absorbed by editing one page class while every test using it stays untouched.
- The pattern only pays off if it's followed everywhere - one locator copied into test code re-creates the scattered-knowledge problem for that locator.
- POM is framework-agnostic: the same structure works in Selenium, Playwright, Cypress, or WebDriverIO.


## Related notes

- [[Notes/framework-design/page-object-model/page-classes|Page classes]]
- [[Notes/framework-design/page-object-model/returning-pages|Returning pages]]
- [[Notes/framework-design/page-object-model/component-objects|Component objects]]


---
_Source: `packages/curriculum/content/notes/framework-design/page-object-model/the-pom-pattern.mdx`_
