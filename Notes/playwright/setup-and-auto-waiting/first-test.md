---
title: "First test"
tags: ["playwright", "setup-and-auto-waiting", "track-d"]
updated: "2026-07-16"
---

# First test

*A Playwright test is three parts - navigate, act, assert - and the terminal report after npx playwright test tells you immediately, per browser, whether the assertion actually held.*

> The scaffolded example test that ships with every new Playwright project already passes the moment
> it's installed - which is exactly the problem if you never look at what it's actually doing. A first
> test worth writing yourself is small enough to read in one glance and specific enough that watching it
> fail on purpose teaches you more than watching it pass ever could.

> **In real life**
>
> A receptacle tester is a small yellow plug with a chart printed on its side: plug it into an outlet,
> read which lights come on, match the pattern against the chart, and you know immediately - correctly
> wired, reversed polarity, or no ground - without opening the wall. A Playwright test does the same
> job for a web page: navigate, act, assert, and the terminal reports the exact pattern back before you
> ever have to dig deeper.

**first test**: A first Playwright test is the minimal shape every test in the framework follows: import test and expect from @playwright/test, call test(name, async ({ page }) => {...}) with a descriptive name, navigate with page.goto(url), perform an action or read a value, and finish with an expect(...) assertion. Running it with npx playwright test executes it once per configured browser project and prints a pass/fail report naming exactly which assertion held or failed, and where.

## The three parts every test has

```
import { test, expect } from '@playwright/test';

test('homepage has the expected title', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  await expect(page).toHaveTitle(/Playwright/);
});
```

- **Navigate** — `page.goto(url)` loads the page the test runs against. Playwright waits for
  navigation to actually complete before the next line runs.
- **Act** (optional for a read-only check like this one) — click, fill, or otherwise interact with
  the page the way a real user would.
- **Assert** — `expect(...)` states what should be true. If it isn't, the test fails and the report
  says exactly which assertion and which line.

The `{ page }` argument is a **fixture** - Playwright hands your test a fresh, isolated browser page
automatically; you never construct or tear one down by hand (the next chapter covers fixtures in
depth).

> **Tip**
>
> Name tests as a plain-English statement of what should be true ("homepage has the expected title"),
> not as a description of the steps ("test 1" or "click button and check page"). When a test fails, that
> name is the first thing anyone reads in the report - make it carry the actual expectation.

> **Common mistake**
>
> Writing a test with actions but no `expect(...)` at all. It will always report as passed, because
> nothing in it can fail - clicking a button that silently does nothing looks identical, in the report,
> to clicking a button that works correctly. A test without an assertion isn't testing anything.

![A yellow plug-in receptacle tester inserted into a wall outlet with two amber LED lights illuminated, a small printed reference chart visible on its side decoding the light patterns into wiring conditions](first-test.jpg)
*Receptacle tester demonstration — Wikimedia Commons, CC BY-SA 4.0 (AndrewBuck). [Source](https://commons.wikimedia.org/wiki/File:Receptacle_tester_demonstration.jpg)*
- **Plugging in — page.goto()** — The tester makes contact with the outlet the same way a test navigates to a URL - the first, necessary step before anything can be checked.
- **The lit LEDs — the assertion's result** — Two specific lights, in a specific pattern - this is the report. Not a vague 'something happened,' a precise, readable signal.
- **The printed chart — what the pattern means** — The tester doesn't just light up, it tells you exactly what the pattern MEANS, correct wiring vs reversed vs no ground - the same job a well-named expect() assertion and its failure message do in a test report.
- **No chart, no lights — a test with no assertion** — A tester with the reference chart peeled off would still plug in and 'work,' but it couldn't tell you anything. A test with actions but no expect() is exactly this: activity with no verifiable result.

**One test, start to report**

1. **test() declares intent** — A descriptive name states what should be true, before any code runs.
2. **page.goto() navigates** — Playwright waits for the page to actually finish loading before continuing.
3. **An action runs (if any)** — Click, fill, or otherwise interact - optional for a pure read-only check.
4. **expect() asserts** — States the expected outcome; Playwright's matchers retry automatically until it holds or times out.
5. **The report prints** — Pass or fail, per browser project, naming exactly which assertion and which line if it failed.

A test is really just: do a thing, then check a condition, then report which one happened. Here's
that shape as a small, generic simulation - not real Playwright code, just the pattern underneath it.

*Run it - navigate, act, assert, report (Python)*

```python
def run_test(name, steps, assertion):
    print(f"Running: {name}")
    state = {}
    for step in steps:
        state = step(state)
    passed = assertion(state)
    status = "PASSED" if passed else "FAILED"
    print(f"  {status}")
    return passed

def goto(state):
    state["url"] = "https://example-shop.test/"
    state["title"] = "Example Shop - Home"
    return state

def check_title(state):
    return "Shop" in state.get("title", "")

result = run_test("homepage has the expected title", [goto], check_title)
print(f"Overall: {'1 passed' if result else '1 failed'}")
```

Same shape in Java - the structure (navigate, act, assert, report) is identical, only the syntax
changes.

*Run it - navigate, act, assert, report (Java)*

```java
import java.util.*;
import java.util.function.*;

public class Main {
    record PageState(String url, String title) {}

    public static void main(String[] args) {
        String testName = "homepage has the expected title";
        System.out.println("Running: " + testName);

        PageState state = goTo();
        boolean passed = checkTitle(state);

        System.out.println("  " + (passed ? "PASSED" : "FAILED"));
        System.out.println("Overall: " + (passed ? "1 passed" : "1 failed"));
    }

    static PageState goTo() {
        return new PageState("https://example-shop.test/", "Example Shop - Home");
    }

    static boolean checkTitle(PageState state) {
        return state.title().contains("Shop");
    }
}
```

### Your first time: Your mission: write and break your own first test

- [ ] In your scratch Playwright project, write a new test that navigates to a real page and asserts something true about it — Try expect(page).toHaveTitle(...) or expect(page.getByRole('heading')).toBeVisible() against a site you know.
- [ ] Run it with npx playwright test and read the full terminal report — Note which browsers it ran against and how long each took.
- [ ] Now break the assertion on purpose — Change the expected title to something wrong, or point the locator at an element that doesn't exist.
- [ ] Run it again and read the failure output closely — Note exactly what Playwright reports: the expected value, the actual value, and which line failed.

You've now seen both a clean pass and a real, informative failure - the two states every test you'll
ever write reports back.

- **The test passes even though you're sure the feature is broken.**
  Check whether there's actually an expect() call in the test at all, and whether it's asserting the specific thing you think it is - a missing or misdirected assertion passes silently no matter what the page does.
- **npx playwright test runs zero tests.**
  Confirm the file matches Playwright's default test file pattern (usually *.spec.ts) and lives under the configured testDir in playwright.config.ts.
- **The failure report shows the expected and actual values, but they look identical to the eye.**
  Look for whitespace, case sensitivity, or a regex vs exact-string mismatch - toHaveTitle(/Playwright/) and toHaveTitle('Playwright') behave differently on a title with extra surrounding text.
- **A test passes locally but fails immediately in CI with no browser window ever visible.**
  This is expected - CI runs headless by default. Confirm the failure is a real assertion mismatch (read the reported expected vs actual) rather than assuming headless mode itself is the cause.

### Where to check

- **The terminal summary line** after a run (e.g. "3 passed, 1 failed") — the fastest overall signal.
- **The per-test failure block** — names the exact assertion, expected value, actual value, and file
  and line number.
- **`playwright.config.ts`'s `testDir` and `testMatch`** — confirms which files Playwright is actually
  discovering as tests.
- **The HTML report** (`npx playwright show-report` after a run) — a browsable, per-test view
  including any screenshots Playwright captured on failure.

### Worked example: a first test that fails usefully on the first try

1. A tester writes `await expect(page).toHaveTitle('Playwright');` against the real Playwright docs
   homepage, whose actual title is "Fast and reliable end-to-end testing for modern web apps |
   Playwright".
2. Running `npx playwright test` reports a failure: expected `"Playwright"` exactly, received the
   full real title string - an exact-string match failed against a title that merely contains the
   word.
3. The tester rewrites it as `await expect(page).toHaveTitle(/Playwright/);` - a regex that checks the
   title merely contains the word, matching the intent more honestly.
4. Running it again reports 1 passed. The failure wasn't a bug in the page - it was the assertion
   being stricter than the actual intent, and the report's expected-vs-actual output made that obvious
   in one read.

**Quiz.** A test performs a click action but has no expect() call anywhere in it. What does the test report show when run?

- [ ] It always fails, because Playwright requires at least one assertion per test
- [x] It always reports as passed, because nothing in the test can actually fail without an assertion to check - the click happening (or silently doing nothing) looks identical in the report either way
- [ ] Playwright refuses to run the file at all
- [ ] It reports as 'skipped' since there's nothing to verify

*The note is explicit that a test without an assertion isn't testing anything - it will report as passed regardless of whether the action actually had the intended effect, because there's no expect() to fail. Option one is false; Playwright does not require an assertion to run a test, which is exactly why this mistake is possible and worth watching for. Option three is false - the file runs fine syntactically. Option four is also false - 'skipped' is a distinct, deliberate status a test gets from test.skip(), not an automatic consequence of missing assertions.*

- **The three parts of a Playwright test** — Navigate (page.goto), act (optional - click/fill/etc.), assert (expect(...)) - assert is the only part that actually makes the test verify anything.
- **Why does a test with actions but no expect() always pass?** — Nothing in it can fail - there's no assertion to check the outcome against, so success and silent failure look identical in the report.
- **toHaveTitle('Playwright') vs toHaveTitle(/Playwright/)** — The first requires an exact match; the second (a regex) matches if the title merely contains the word - picking the wrong one produces a misleading failure against a real, correct page.
- **Where does a failed assertion's detail actually show up?** — The per-test failure block in the terminal report - expected value, actual value, and the exact file and line.

### Challenge

Write three small tests against a real site of your choice: one that asserts something true (should
pass), one where you deliberately assert something false (should fail, on purpose, so you can read the
failure report), and one that performs an action with no assertion at all. Run all three and confirm
the third one - the assertion-free one - reports as passed regardless of what the action actually did.

### Ask the community

> My Playwright test reports `[passed/failed]` but I expected the opposite. Here's the test: `[paste the test code]`. Here's the terminal output: `[paste the report]`.

Pasting both the test code and the exact terminal output (not a paraphrase) lets someone spot in
seconds whether the assertion itself, the locator, or the expected value is the actual problem.

- [Playwright — official Writing tests docs](https://playwright.dev/docs/writing-tests)
- [Playwright — official Assertions reference](https://playwright.dev/docs/test-assertions)

🎬 [How to Create and Run Your First Test — Playwright JavaScript Tutorial Part 1 — TestMu AI (LambdaTest)](https://www.youtube.com/watch?v=1crAeA3ZPAM) (48 min)

- Every Playwright test has the same shape: navigate (page.goto), optionally act, then assert (expect(...)) - assert is the only part that makes it actually verify anything.
- The { page } fixture is handed to every test automatically - a fresh, isolated browser page with no manual setup or teardown.
- A test with actions but no expect() call always reports as passed, because there's nothing in it that can fail - this is the single most common reason a 'passing' test proves nothing.
- The terminal failure report names the exact expected value, actual value, and line - read it fully before assuming the page (rather than the assertion) is wrong.
- Naming a test as a plain statement of what should be true, not a list of steps, makes that report readable at a glance months later.


## Related notes

- [[Notes/playwright/setup-and-auto-waiting/installing-playwright|Installing Playwright]]
- [[Notes/playwright/setup-and-auto-waiting/typescript-setup|TypeScript setup]]
- [[Notes/playwright/setup-and-auto-waiting/auto-waiting-explained|Auto-waiting explained]]


---
_Source: `packages/curriculum/content/notes/playwright/setup-and-auto-waiting/first-test.mdx`_
