---
title: "Selenium With Java Tutorial for Beginners: Write Your First Test Step by Step"
meta_description: "Learn Selenium with Java from scratch. Set up the project, write your first browser test, understand locators and waits, and avoid common beginner mistakes."
slug: selenium-java-beginners
status: draft
---

# Selenium With Java Tutorial for Beginners: Write Your First Test Step by Step

To write your first Selenium test in Java, you install a JDK and an IDE, add the `selenium-java` dependency through Maven, then write a class that launches a browser with `new ChromeDriver()`, navigates with `driver.get(url)`, finds an element with `driver.findElement(By.id(...))`, and asserts on the result. That's the entire loop: open a browser, do something, check what happened. This guide walks you through it end to end, then shows you the locators, waits, and habits that separate a working test from a flaky one.

Selenium is the most widely used open-source tool for automating web browsers, and Java is its most common language pairing in the job market. If your goal is your first automation role, this is the stack hiring managers expect you to know.

## What You Need Before You Start

A Selenium-with-Java setup has four moving parts. Get these installed first so the code below actually runs.

1. **JDK 17 or newer** — the Java runtime and compiler. Verify with `java -version`.
2. **An IDE** — IntelliJ IDEA Community Edition or Eclipse. IntelliJ is the more common choice today.
3. **A build tool** — Maven (or Gradle). Maven downloads Selenium and your test libraries for you, so you never hand-manage JAR files.
4. **A browser** — Chrome, Firefox, or Edge. Selenium 4.6+ includes **Selenium Manager**, which auto-downloads the matching driver binary. You no longer need to install ChromeDriver manually.

That last point trips up people following older tutorials. If a guide tells you to download `chromedriver.exe` and set a system property, it predates Selenium Manager. On modern Selenium you can skip it entirely.

## Step 1: Create the Maven Project and Add Selenium

Create a new Maven project in your IDE, then open `pom.xml` and add Selenium plus a test framework. JUnit 5 and TestNG are both fine; this guide uses JUnit 5.

```xml
<dependencies>
  <dependency>
    <groupId>org.seleniumhq.selenium</groupId>
    <artifactId>selenium-java</artifactId>
    <version>4.27.0</version>
  </dependency>
  <dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.11.3</version>
    <scope>test</scope>
  </dependency>
</dependencies>
```

Save the file and let Maven download the dependencies. Use the latest stable Selenium version when you do this — check the official releases rather than copying a version number blindly.

## Step 2: Write Your First Test

Create a class in `src/test/java`. This test opens a page, types a search term, submits it, and checks the page title changed.

```java
import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import java.time.Duration;
import static org.junit.jupiter.api.Assertions.*;

public class FirstTest {

    WebDriver driver;

    @BeforeEach
    void setUp() {
        driver = new ChromeDriver();
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(5));
    }

    @Test
    void searchReturnsResults() {
        driver.get("https://www.selenium.dev/selenium/web/web-form.html");

        WebElement textBox = driver.findElement(By.name("my-text"));
        WebElement submit = driver.findElement(By.cssSelector("button"));

        textBox.sendKeys("hello world");
        submit.click();

        assertTrue(driver.getCurrentUrl().contains("submitted-form"));
    }

    @AfterEach
    void tearDown() {
        driver.quit();
    }
}
```

Run it. A real Chrome window opens, fills the form, submits, and the test passes green. The four anatomy pieces to remember:

- **`@BeforeEach` / `@AfterEach`** — set up a fresh browser per test and always close it with `driver.quit()`. Forgetting `quit()` leaves zombie browser processes running.
- **`driver.get(url)`** — navigate to a page.
- **`findElement(By...)`** — locate an element on the page.
- **assertion** — verify the outcome. A test with no assertion isn't a test; it's a script that can't fail.

## Step 3: Understand Locators

A **locator** is how you tell Selenium which element to act on. Choosing stable locators is the single biggest skill in UI automation, because brittle locators are the number-one cause of flaky tests.

| Locator | Example | When to use | Stability |
|---|---|---|---|
| `By.id` | `By.id("login")` | Element has a unique, stable id | Highest |
| `By.name` | `By.name("email")` | Form fields | High |
| `By.cssSelector` | `By.cssSelector("button.primary")` | Most general-purpose cases | High |
| `By.linkText` | `By.linkText("Sign out")` | Anchor links by visible text | Medium |
| `By.xpath` | `By.xpath("//button[text()='Buy']")` | When you must match by text or traverse the DOM | Medium/Low |
| `By.className` | `By.className("btn")` | Rarely, classes are often shared | Low |

**A good locator has three qualities:** it is unique on the page, it targets something meaningful (an id or `data-testid`, not a styling class), and it survives minor layout changes. Prefer `id` and `cssSelector`. Reach for XPath only when you need to match by visible text or walk up the DOM tree — capabilities CSS selectors lack.

## Step 4: Replace Sleeps With Explicit Waits

Modern web apps load content asynchronously, so an element may not exist the instant the page "loads." Beginners reach for `Thread.sleep(3000)`. Don't. It's slow when the page is fast and fails when the page is slow.

Use an **explicit wait** instead, which polls until a condition is true or a timeout expires:

```java
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
WebElement banner = wait.until(
    ExpectedConditions.visibilityOfElementLocated(By.id("confirmation"))
);
```

Quick reference on the three wait types:

- **Implicit wait** — a global "wait up to N seconds for any element to appear." Set it once.
- **Explicit wait** — wait for a *specific condition* on a *specific element*. The right tool most of the time.
- **`Thread.sleep`** — a hard pause. Avoid it in real tests.

## Common Beginner Mistakes (and the Fixes)

- **Hard-coded sleeps everywhere** → switch to explicit waits.
- **Not calling `driver.quit()`** → orphaned browsers eat memory; always quit in teardown.
- **`NoSuchElementException`** → usually a wrong locator or acting before the element renders; verify the selector in DevTools and add a wait.
- **`StaleElementReferenceException`** → you held a reference to an element after the DOM re-rendered; re-find the element instead of reusing the old variable.
- **Tests with no assertions** → if it can't fail, it isn't testing anything.
- **Mixing implicit and explicit waits aggressively** → can produce unpredictable timeouts; prefer explicit waits and keep implicit waits short.

## How Selenium Fits a Real QA Workflow

Selenium drives the browser, but on its own it isn't a test suite. A production-grade setup layers a few things on top:

1. **A test runner** (JUnit 5 or TestNG) to organize, group, and report on tests.
2. **The Page Object Model**, where each page's locators and actions live in their own class. This keeps tests readable and means a UI change touches one file, not fifty.
3. **Assertions** that express business expectations, not just "the element exists."
4. **CI integration** so tests run automatically on every code change.

You don't need all of this on day one. Master a single reliable test first, then grow into Page Objects and CI.

## Selenium vs. Other Browser-Automation Tools

| Tool | Language fit | Best for | Notes |
|---|---|---|---|
| **Selenium + Java** | Java | Enterprise teams, broad job demand | Most requested combo in QA job posts |
| Selenium + Python | Python | Fast scripting, data-heavy teams | Same API, lighter syntax |
| Playwright | JS/TS, Java, Python, .NET | Modern apps, built-in waits | Newer, less entrenched in legacy shops |
| Cypress | JavaScript | Front-end devs | Runs in-browser, JS-only |

For someone targeting a first QA-automation job, **Selenium with Java remains the safest bet** because it appears in the most listings and transfers cleanly to other stacks once you understand the core concepts.

## Your Next Step: Practice on a Real Broken App

Reading code is not the same as testing software. The fastest way to internalize locators, waits, and assertions is to point your shiny new test at an app that actually has bugs — then watch your assertions catch them.

That's exactly what **BuggyShop** on QA Mastery is for: a deliberately broken e-commerce app with real seeded bugs, where you don't watch testing, you do it. Write Selenium-with-Java tests against it, find the bugs, and file real bug reports that get graded against a server-side answer key. The first module of each track is free.

Spin up the free lab on QA Mastery and run your first test against a real, broken app today.