# Sample Lesson 3 — Your First Selenium Test (B2.1)

**Type:** Automation lab lesson · **Time:** ~40 min · **Free-tier:** Yes during validation
**Prereq stated upfront:** assumes B0 Java basics (variables, methods, classes). For the validation sample, a "Java in 90 seconds" refresher card is bolted on top.
**Pattern:** See it → Try it → Do it → Prove it

---

## Hook

> You're about to write a program that opens a browser, logs into a shop, and checks the result — in 12 lines of Java.
> No installation. No environment setup. The runner is ours; the code is yours.
> *(Honest note shown in-lesson: in a real job you'll set up Maven + ChromeDriver yourself — that's lesson B2.0, and we make you do it locally too. Today we remove setup so your first test runs in minutes, not hours.)*

---

## Part 1 — SEE IT: What Selenium actually does (8 min)

**Widget: `driver-pipeline` (animated diagram)**

Four boxes, animated left to right as a sample test runs in a side panel:
**Your Java code** → **WebDriver API** → **ChromeDriver (the translator)** → **Real Chrome browser**

- Each step lights up as the side-panel test executes line by line: `driver.get(...)` lights the pipeline and the embedded browser visibly navigates; `findElement` highlights the actual element in the page; `click()` clicks it live.
- Caption beats: Selenium doesn't "record" anything — it sends commands. ChromeDriver speaks the browser's protocol. The browser doesn't know a human isn't driving.

**Widget: `locator-xray`**
- BuggyShop login page with "X-ray mode" toggle: hovering any element shows its HTML + the best locator, ranked (`data-testid` → `id` → CSS → XPath last).
- One rule taught hard: **stable locators first.** `data-testid="login-submit"` survives redesigns; `/html/body/div[3]/div/button[2]` dies tomorrow. (Sets up the Deals-page locator gym later.)

## Part 2 — TRY IT: Read a test before writing one (7 min)

A complete 12-line test shown with every line annotated on hover; learner must predict, before running it: "Will this pass or fail?" Then they hit ▶ Run and watch the embedded browser execute.

```java
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import static org.testng.Assert.assertEquals;

public class LoginTest {
    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        driver.get("https://buggyshop.app/login");
        driver.findElement(By.cssSelector("[data-testid='login-email']")).sendKeys("asha@test.io");
        driver.findElement(By.cssSelector("[data-testid='login-password']")).sendKeys("Pass@123");
        driver.findElement(By.cssSelector("[data-testid='login-submit']")).click();
        String heading = driver.findElement(By.cssSelector("[data-testid='home-greeting']")).getText();
        assertEquals(heading, "Welcome back, Asha!");
        driver.quit();
    }
}
```

Concept callouts: a test = **navigate → act → assert** (+ always `quit()`); an automated test without an assertion is just a robot clicking; `main()` today, TestNG `@Test` in B3 (flagged explicitly so nobody thinks `main` is the real-world pattern).

## Part 3 — DO IT: Write your own (20 min, auto-graded)

**Task:** Write a test that searches BuggyShop for "mug", opens the first result, and asserts the product title contains "Mug".

- Embedded editor pre-loaded with imports + skeleton; learner writes ~8 lines.
- ▶ Run → code executes server-side in the containerized runner against BuggyShop; learner gets back: pass/fail, console output, **screenshot at the failure line** if it fails, and execution video.
- **Grading:** test passes (60%) · used stable locators, no absolute XPath (25%, static check) · assertion present and meaningful (15%, static check). Pass ≥ 70.
- **Designed stumble:** the search results take ~1.5 s to render. A naive `findElement` immediately after submitting the search intermittently throws `NoSuchElementException`. The error panel catches this specific failure and says: *"Your code was faster than the page. This is the #1 real-world automation failure — and it's exactly what Waits (next lesson, B2.4) solve. For now, re-run; sometimes it passes. Annoying? That's the point."*
- Hints ladder: locator inventory link → skeleton of the search interaction → full solution with explanation (using solution caps score at 70).

## Part 4 — PROVE IT (quiz, 6 questions)

1. Order the pipeline: Chrome, your code, ChromeDriver, WebDriver API.
2. Which locator survives a page redesign best: `data-testid`, absolute XPath, text-based, nth-child CSS?
3. What's wrong with a test that has no assertion?
4. Why did your test fail intermittently in the lab? *(timing/race — page slower than code)*
5. What does `driver.quit()` do and what leaks if you skip it?
6. `findElement` throws `NoSuchElementException` — name two distinct causes. *(bad locator vs not-yet-rendered)*

**Flashcards:** navigate/act/assert, locator ranking, NoSuchElement causes, quit().

---

## Production notes
- **Infra dependency (the big one):** this lesson requires the server-side Java runner (judge0-style + headless Chrome containers) — the plan's highest-risk build item. For **validation week**, ship this lesson as a *non-executable* annotated walkthrough (Parts 1–2 interactive, Part 3 shown as a demo video of the runner) — measure interest before building the runner.
- `driver-pipeline` and `locator-xray` widgets are reused across B1–B4.
- Marketing cut: 60-sec reel — "12 lines of Java just logged into a shop and checked the result. No setup. Write yours →".
