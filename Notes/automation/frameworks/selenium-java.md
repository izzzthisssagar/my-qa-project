---
title: "Selenium with Java"
tags: ["automation", "selenium", "java"]
updated: "Fri Jul 03 2026 05:45:00 GMT+0545 (Nepal Time)"
---

# Selenium with Java

*The industry-standard browser automation library — its WebDriver architecture, core API, and where it fits in a Java test stack.*

**Selenium WebDriver** is the long-standing standard for browser automation, and
Java is its most common host language. It drives a real browser through the
browser's own automation interface.

## Architecture

Your test → **WebDriver API** → **browser driver** (ChromeDriver, GeckoDriver) →
the **browser**. The driver translates WebDriver commands into the browser's
native protocol. Selenium 4 adopted the **W3C WebDriver** standard, so behaviour
is consistent across browsers.

## Core API

```java
WebDriver driver = new ChromeDriver();
driver.get("https://example.com");

WebElement search = driver.findElement(By.name("q"));
search.sendKeys("qa mastery");
search.submit();

new WebDriverWait(driver, Duration.ofSeconds(10))
    .until(ExpectedConditions.titleContains("qa mastery"));

driver.quit();   // always quit — frees the driver process
```

## The wider stack

Selenium only drives the browser; a real suite adds:

- **Build/deps** — Maven or Gradle (Selenium Manager now auto-provisions drivers).
- **Runner** — [TestNG or JUnit](/notes/automation/frameworks/testng-junit) for
  structure, assertions, parallelism.
- **Design** — the [Page Object Model](/notes/automation/fundamentals/page-object-model)
  for maintainability.
- **Reporting** — ExtentReports or Allure.

## Selenium vs Playwright

Selenium is mature, multi-language, and ubiquitous in enterprise. [Playwright](/notes/automation/frameworks/playwright)
is newer, with built-in auto-waiting and richer tooling. Both are strong choices;
Selenium's edge is its ecosystem and the sheer number of jobs that ask for it.


---
_Source: `packages/curriculum/content/notes/automation/frameworks/selenium-java.mdx`_
