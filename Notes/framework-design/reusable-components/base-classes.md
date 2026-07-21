---
title: "Base classes"
tags: ["framework-design", "reusable-components", "track-d"]
updated: "2026-07-17"
---

# Base classes

*A shared parent class (BaseTest, BasePage) that every test or page class extends - setup, teardown, the driver field, and common helpers live in ONE place instead of being copy-pasted everywhere. DRY and consistent, until it grows into a god class nobody wants to touch.*

> Forty test classes, each opening with the same ten copy-pasted lines: create the driver, maximize the
> window, set the timeout, navigate to the app. Then the timeout needs to change. Someone edits it in
> twenty-eight files, misses twelve, and the suite spends the next month failing in ways that depend on
> which file a test happens to live in. A base class exists so that change is one edit, in one file,
> inherited by everyone.

> **In real life**
>
> An apartment block under construction is dozens of different homes - different layouts, different
> kitchens, different owners - all standing on one shared concrete skeleton. No floor pours its own
> private foundation, and no apartment gets its own personal structural design; the frame is engineered
> once and every unit inherits it. When the structural spec changes, it changes in the frame drawings -
> one place - and every floor built after that carries the change. What each apartment does differently
> (its interior) stays out of the frame's job entirely.

**Base class (BaseTest / BasePage)**: A base class in a test framework is a shared parent class that every test class or every page class extends, so behavior common to all of them is written exactly once. A BaseTest typically owns the lifecycle: it holds the WebDriver field, creates the driver in a setup hook (@BeforeMethod / @BeforeEach), and quits it in a teardown hook (@AfterMethod / @AfterEach), so no individual test class contains any of that plumbing. A BasePage typically owns what every page object needs: the driver reference passed in through its constructor, plus shared interaction helpers (a safe click, a text getter, a wait call). Subclasses inherit all of it automatically and add only what is unique to them. The payoff is DRY (one edit propagates everywhere) and consistency (every test starts and ends the same way). The cost appears when the base class accumulates responsibilities that do not belong to ALL subclasses - Excel readers, email senders, screenshot logic, date formatting - and becomes a god class: a bloated parent that everything depends on, everyone fears editing, and every change to it risks breaking the entire suite at once.

## What lives in the parent, and what must not

- **BaseTest owns the lifecycle** — the driver field, the setup hook that creates it, the teardown
  hook that quits it. A test class that extends it contains only tests; it never mentions
  ChromeDriver, timeouts, or window sizing at all.
- **BasePage owns what every page needs** — the driver reference (assigned once in the base
  constructor), plus genuinely universal helpers: a click that waits first, a safe text read. Each
  page object extends it and adds only its own locators and actions.
- **One edit propagates everywhere** — change the default timeout, the starting URL, or the browser
  options in the base class, and every subclass picks it up on the next run. No search-and-replace
  across forty files, no stragglers.
- **The membership test** — before adding anything to a base class, ask: does EVERY subclass need
  this? If only some do, it belongs in a utility class or a smaller intermediate class instead.
  A base class is for the universal minimum, not for "somewhere convenient to put things."

```java
public class BaseTest {
    protected WebDriver driver;                 // shared field - every test class inherits it

    @BeforeMethod
    public void setUp() {
        driver = DriverFactory.createDriver();  // one place decides how drivers are built
        driver.manage().window().maximize();
        driver.get(Config.baseUrl());
    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) driver.quit();      // guaranteed cleanup for every test class
    }
}

public class LoginTest extends BaseTest {       // no setup code anywhere in this file
    @Test
    public void rejectsWrongPassword() {
        new LoginPage(driver).loginAs("standard_user", "wrong_pass");
        // assertions only - the lifecycle is inherited
    }
}
```

> **Tip**
>
> Keep the base class down to what every single subclass needs, and push everything else outward: helpers
> only some classes use become utility classes, and setup only one product area needs becomes a small
> intermediate class (a CheckoutBaseTest extending BaseTest) rather than another field on the shared
> parent. A BaseTest that stays under a screenful is a BaseTest people trust enough to actually edit.

> **Common mistake**
>
> Treating the base class as the junk drawer - Excel reading, email reporting, screenshot naming, date
> formatting, and retry logic all bolted onto BaseTest "because everything can reach it there." That's
> the god class: every test in the suite now depends on code most of them never use, any edit to it can
> break everything at once, and new team members inherit hundreds of lines of unrelated plumbing before
> writing their first test. The DRY win came from centralizing the UNIVERSAL parts, not from centralizing
> everything.

![A multi-story apartment building under construction showing the bare repeated concrete structural skeleton across several floors, formwork panels being set on the top storey, a red concrete pump boom overhead, and workers preparing materials at ground level](base-classes.jpg)
*Multi-story concrete construction in Chile — Wikimedia Commons, CC BY-SA 3.0 (WTF Formwork). [Source](https://commons.wikimedia.org/wiki/File:Concrete_construction.JPG)*
- **The same concrete frame, repeated on every floor** — One structural design that every unit inherits identically - the base class itself. No apartment negotiates its own private skeleton, and no test class writes its own private setup.
- **Formwork panels being set for the next storey** — The frame's design is defined once and stamped onto each new floor as it's built - change the form, and every floor poured after that carries the change. One edit, inherited by everything built on top.
- **The concrete pump boom feeding every floor from one point** — One central supply line serving the whole structure - the same shape as a base class's setup hook: every test class draws its driver, its timeouts, and its starting state from the same single source.
- **Ground-level benches where unit-specific work is prepared** — What makes each apartment different is prepared OUTSIDE the shared frame - exactly where subclass-specific behavior belongs: in the subclass, not bolted onto the parent everyone depends on.

**From forty copies to one parent - and the line not to cross**

1. **40 test classes, each with copy-pasted setup** — Same ten lines everywhere - and a timeout change means forty edits.
2. **BaseTest extracted: driver, setUp, tearDown in one file** — Every test class now extends it and shrinks to just its tests.
3. **A config change lands once, in the base class** — All forty classes inherit the new behavior on the next run - zero stragglers.
4. **Unrelated helpers start accumulating on BaseTest** — Excel readers, email senders, screenshot naming - things only SOME classes need.
5. **God class alert: split it before everything depends on everything** — Universal minimum stays in the base; the rest moves to utilities or smaller intermediate classes.

Strip away the framework and the pattern is just: shared behavior defined once in a parent, inherited
by every child, so one change lands everywhere. Here's that shape as a small, generic simulation -
including the copy-paste version it replaces.

*Run it - one parent class versus forty copies of the same setup (Python)*

```python
class BaseTest:
    TIMEOUT = 10  # the shared default - ONE place to change it

    def set_up(self):
        return f"driver created, timeout={self.TIMEOUT}s"

class LoginTest(BaseTest):
    def run(self):
        return f"[LoginTest]    {self.set_up()} -> testing login"

class CheckoutTest(BaseTest):
    def run(self):
        return f"[CheckoutTest] {self.set_up()} -> testing checkout"

print("--- both classes inherit the same setup ---")
print(LoginTest().run())
print(CheckoutTest().run())

print("--- one edit in the base propagates to every subclass ---")
BaseTest.TIMEOUT = 30
print(LoginTest().run())
print(CheckoutTest().run())

print("--- the copy-paste world this replaces ---")
copies = {"LoginTest": 10, "CheckoutTest": 10, "CartTest": 30}  # someone missed two files
stale = [name for name, t in copies.items() if t != 30]
print(f"after a manual timeout change across files, still stale: {stale}")
```

Same inheritance shape in Java.

*Run it - one parent class versus forty copies of the same setup (Java)*

```java
public class Main {
    static int TIMEOUT = 10; // the shared default - ONE place to change it

    static class BaseTest {
        String setUp() {
            return "driver created, timeout=" + TIMEOUT + "s";
        }
    }

    static class LoginTest extends BaseTest {
        String run() { return "[LoginTest]    " + setUp() + " -> testing login"; }
    }

    static class CheckoutTest extends BaseTest {
        String run() { return "[CheckoutTest] " + setUp() + " -> testing checkout"; }
    }

    public static void main(String[] args) {
        System.out.println("--- both classes inherit the same setup ---");
        System.out.println(new LoginTest().run());
        System.out.println(new CheckoutTest().run());

        System.out.println("--- one edit in the base propagates to every subclass ---");
        TIMEOUT = 30;
        System.out.println(new LoginTest().run());
        System.out.println(new CheckoutTest().run());

        System.out.println("--- the copy-paste world this replaces ---");
        int[] copiedTimeouts = {30, 30, 10}; // someone missed a file
        int stale = 0;
        for (int t : copiedTimeouts) if (t != 30) stale++;
        System.out.println("after a manual change across files, stale copies remaining: " + stale);
    }
}
```

### Your first time: Your mission: extract a base class from two duplicated test classes

- [ ] Write (or find) two test classes that each contain their own identical setup and teardown — Driver creation, a timeout, a starting URL - the same lines twice. Run both and confirm they pass.
- [ ] Create a BaseTest holding the driver field, a setup hook, and a teardown hook — Move the duplicated lines into it, make both test classes extend it, and delete their local copies.
- [ ] Change one shared value (the timeout or the URL) in BaseTest only — Run both classes and confirm both picked up the change with zero edits to the test files themselves.
- [ ] Now try to add a CSV-parsing helper to BaseTest - then stop and say out loud why it doesn't belong — Only some future tests would use it: that's the membership test failing, and the god-class slope starting.

You've now felt both halves of the tradeoff: the one-edit payoff, and the pull toward dumping
everything into the parent.

- **A one-line change to the base class broke dozens of seemingly unrelated tests at once.**
  That blast radius is the cost of centralization - and it's acceptable only when the base class holds genuinely universal behavior. If the broken tests never used the thing you changed, the base class is carrying non-universal code: move it out to a utility or an intermediate class so its blast radius matches its actual audience.
- **One test class needs a slightly different setup (a different URL, no login) and fights the inherited hook.**
  Don't pile conditionals into the base setup ('if this is the payments suite, then...'). Either expose a small overridable method the subclass can customize (a protected startUrl() it overrides), or create a thin intermediate base class for that family of tests.
- **The base class has grown to hundreds of lines and new teammates can't say what it actually does.**
  Audit each member with the membership test: does every subclass use this? Screenshot naming, data readers, report hooks used by a subset all move out to focused utility classes. What remains - lifecycle, driver field, universal helpers - is usually a screenful.
- **A test fails during setup and it's unclear which class in the chain (BaseTest, WebBaseTest, CheckoutBaseTest) actually ran what.**
  Deep inheritance chains hide execution order. Keep the hierarchy shallow (one, at most two levels), and check the framework's rule for parent-class hook ordering - in TestNG and JUnit, parent setup hooks run before child ones, which is usually the behavior you want but rarely the one people guess.

### Where to check

- **The base class file itself** — its length and its import list are the fastest god-class detector:
  imports for Excel, mail, or JSON parsing in a BaseTest are things that don't belong to a lifecycle.
- **What each subclass actually uses** — an IDE's "find usages" on a base-class helper shows instantly
  whether it's universal (every subclass) or a squatter (two subclasses, and it should move out).
- **The framework's hook-ordering rules** — JUnit and TestNG both run parent setup hooks before child
  ones and child teardown before parent; the official docs are the authority when a chain misbehaves.
- **Version history of the base class** — a file that changes in every second pull request is carrying
  too many responsibilities; a healthy base class changes rarely, because the universal minimum rarely
  changes.

### Worked example: the 900-line BaseTest that a timeout change finally exposed

1. A team's suite has 35 test classes, each with its own copy of driver creation, window sizing, an
   implicit wait, and a login call. A tester extracts a BaseTest; every class shrinks by a dozen lines
   and the next timeout change takes thirty seconds instead of an afternoon.
2. Six months later, BaseTest is 900 lines. It reads Excel test data, names screenshots, sends failure
   emails, formats dates, and holds retry logic - each added "because everything extends BaseTest
   anyway, so everything can reach it."
3. A developer tweaks the screenshot-naming logic inside BaseTest. The change accidentally touches a
   shared field used by teardown - and 35 test classes fail overnight, including suites that never
   take screenshots at all.
4. The team audits BaseTest with one question per member: does EVERY test class need this? The
   lifecycle (driver field, setup, teardown) stays. Excel reading, screenshot naming, emailing, and
   date formatting move into four small utility classes that only the classes needing them import.
5. BaseTest lands at 40 lines. The next screenshot-naming change touches ScreenshotUtils and its
   three actual consumers - the other 32 test classes are structurally incapable of noticing.

**Quiz.** A teammate wants to add a parseCsvTestData() method to BaseTest, arguing 'every test class extends BaseTest, so putting it there means every test can reach it.' Only the 4 data-driven test classes (of 35) would ever call it. Based on this note, what's the right call?

- [ ] Add it to BaseTest - maximum reachability is exactly what a base class is for
- [x] Decline: reachability isn't the criterion, universality is - a method only 4 of 35 subclasses use fails the membership test and starts the god-class slide, so it belongs in a small utility class those 4 classes import
- [ ] Add it to BaseTest but mark it deprecated so people know not to use it too much
- [ ] Create a second BaseTest2 parent containing only parseCsvTestData() and have the 4 classes extend both

*The note's membership test says a base class holds only what EVERY subclass needs - the payoff of centralization is bought with blast radius, so anything non-universal inflates risk for classes that never use it. Option one repeats the exact reasoning ('everything can reach it') that the mistake callout identifies as the god-class trap. Option three doesn't solve anything - deprecated-but-present code still couples all 35 classes to it and still breaks everything when edited. Option four isn't even possible in Java (a class cannot extend two parents), and splitting parents per-helper would recreate the same problem as a hierarchy tangle instead of a single junk drawer.*

- **What does a BaseTest typically own?** — The lifecycle: the WebDriver field, the setup hook that creates the driver, and the teardown hook that quits it - so no individual test class contains any lifecycle plumbing.
- **What does a BasePage typically own?** — The driver reference (assigned in the base constructor) plus interaction helpers every page object needs - a safe click, a text getter. Each page class adds only its own locators and actions.
- **The membership test before adding anything to a base class** — Does EVERY subclass need this? If only some do, it belongs in a utility class or a small intermediate class - not on the shared parent.
- **What is a god class, in base-class terms?** — A base class that accumulated responsibilities beyond the universal minimum - everything depends on it, most subclasses use only a fraction of it, and any edit risks breaking the whole suite at once.
- **The apartment-block analogy for base classes** — Many different homes on one shared concrete skeleton: the frame is designed once and every unit inherits it (the base class), while each apartment's unique interior stays out of the frame's job (subclass-specific code).

### Challenge

Open a real test framework (yours, a tutorial repo, or an open-source suite) and audit its BaseTest or
BasePage with the membership test: for each field and method, count how many subclasses actually use
it. Produce two lists - "universal, stays" and "partial, should move out" - and for one item on the
second list, actually perform the extraction into a utility class and confirm the suite still passes.

### Ask the community

> My BaseTest has grown to `[N]` lines and includes `[list the main things it does]`. Which of these belong in the base class versus a utility, and how would you split it?

Listing what the base class actually contains usually gets a fast, concrete split proposal - the
universal-versus-partial boundary is much easier for someone else to see in a real member list than in
the abstract.

- [Selenium — official docs: Page Object Models (shared page-class design)](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [Refactoring Guru — Large Class (the god-class smell and its fixes)](https://refactoring.guru/smells/large-class)

🎬 [Selenium Framework Tutorial #5 - Move Common Details to Base Class — Software Testing Mentor](https://www.youtube.com/watch?v=j3o6r1BB2hI) (19 min)

- A base class centralizes what every test or page class shares - the driver field, setup, teardown, universal helpers - so one edit propagates everywhere instead of being copy-pasted into every file.
- BaseTest owns the lifecycle; BasePage owns the driver reference and universal page helpers; subclasses add only what is unique to them.
- The membership test guards the design: only what EVERY subclass needs belongs in the parent - partial-use helpers move to utility classes.
- The god class is the failure mode: a base class that became the junk drawer couples the whole suite to code most of it never uses, and every edit risks breaking everything at once.
- Blast radius is the price of centralization - acceptable for genuinely universal behavior, unacceptable for anything else, which is exactly the line between DRY and god class.


## Related notes

- [[Notes/framework-design/reusable-components/utilities|Utilities]]
- [[Notes/framework-design/reusable-components/waits-wrapper|Waits wrapper]]
- [[Notes/framework-design/reusable-components/driver-factory|Driver factory]]


---
_Source: `packages/curriculum/content/notes/framework-design/reusable-components/base-classes.mdx`_
