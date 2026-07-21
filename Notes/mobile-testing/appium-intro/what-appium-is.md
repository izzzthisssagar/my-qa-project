---
title: "What Appium is"
tags: ["mobile-testing", "appium-intro", "track-c"]
updated: "2026-07-21"
---

# What Appium is

*Appium extends the WebDriver protocol Selenium popularized for browsers onto native iOS and Android apps, routing the same client commands through a platform driver instead of ChromeDriver or GeckoDriver.*

> A tester who has spent a year writing `driver.find_element(...).click()` in Selenium opens their first
> Appium project expecting to relearn everything for mobile. Instead the test code looks almost identical —
> same client, same session object, same method names. What actually changed is invisible: there is no
> browser and no DOM anywhere underneath it.

> **In real life**
>
> Think of a translation agency that takes requests in one standard format and routes each one to whichever
> specialist translator the job needs. Selenium is a small agency with one translator on staff, fluent only
> in "browser." Appium is the same agency grown larger: it still accepts requests in the exact same
> standard format, but now routes each one to whichever specialist the target platform requires — one
> translator for Android, a completely different one for iOS. The client never has to learn a new way to
> phrase the request.

**Appium**: Appium is an open-source, cross-platform automation framework that drives native, hybrid, and mobile-web apps on Android and iOS through a single WebDriver-based client API, by routing each command through a platform-specific driver instead of talking to a browser or the OS directly.

## The same protocol, a different driver underneath

Selenium and Appium share the same foundation: the WebDriver protocol, a standard way for a test client to
send JSON commands over HTTP to a server and get structured results back. Selenium's server forwards those
commands to a browser driver — ChromeDriver, GeckoDriver, and so on — which speaks directly to a browser's
rendering engine and DOM. Appium's server forwards the exact same shape of command to a platform driver
instead: UiAutomator2 for Android, XCUITest for iOS. Neither of those drivers has any concept of a DOM,
because there isn't one — a native app's UI is a view hierarchy the operating system's own instrumentation
framework exposes, not HTML.

This is why the client-side code barely changes when a tester moves from Selenium to Appium. `find_element`,
`click`, session start, and session end all exist on the Appium side because Appium's client libraries are
built to speak the same protocol shape Selenium's are. What changes is what sits behind the server: a
browser-specific driver becomes a platform-specific one, and the thing being automated becomes a real
operating system's accessibility layer instead of a rendering engine.

## Where the Selenium mental model stops applying

The similarity breaks down exactly at the boundary of "how do I find things." CSS selectors and most XPath
habits assume an HTML document; a native screen has no such document to query. Elements are described by
properties the platform's own accessibility and UI-testing frameworks expose — a resource id on Android, an
accessibility identifier on iOS — which is why Appium defines its own locator strategies instead of reusing
CSS selectors wholesale. A hybrid app's webview portion is the one place CSS and XPath still work, because
that piece really is rendered by a browser engine embedded inside the native shell.

Appium 2 also decoupled the server from any specific driver: the core server is a thin router, and
UiAutomator2, XCUITest, and every other platform driver are installed and versioned separately. A session's
capabilities tell that router which driver to hand the session to before a single command is sent.

> **Tip**
>
> When a mobile test behaves unexpectedly, check the driver before the test code. Confirm which driver the
> session actually started with (UiAutomator2, XCUITest, or something else) and that its version matches what
> the app and OS version require — a driver/OS mismatch produces failures that look like broken test logic
> but aren't.

> **Common mistake**
>
> Do not treat Appium as "Selenium, but somehow for phones" in the literal sense of expecting a DOM. Porting a
> CSS selector or a DOM-shaped XPath expression straight into a native-app test is a common first mistake —
> there is no document to query, only a platform-specific view hierarchy with its own locator strategies.

![Four smartphones lying face down on a dark wooden table: a black Samsung Galaxy S22 Ultra, a silver LG G6, a white iPhone SE third generation, and a silver Samsung Galaxy S10 5G](what-appium-is.jpg)
*SAMSUNG Galaxy S22 Ultra, LG G6, iPhone SE3, SAMSUNG Galaxy S10 5G — Dinkun Chen, Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:SAMSUNG_Galaxy_S22_Ultra,_LG_G6,_iPhone_SE3,_SAMSUNG_Galaxy_S10_5G_(2).jpg)*
- **Another Android OEM entirely** — The LG G6 is Android too, but a different manufacturer's build — the same UiAutomator2 driver still applies, because it talks to Android's own instrumentation layer, not to LG's skin specifically.
- **Android device, UiAutomator2 driver** — A session against this phone is driven by UiAutomator2 — it reads Android's accessibility tree, the same interface regardless of which app or manufacturer skin sits on top.
- **A different Android phone, same driver** — Pointing a session at this device instead of the one on the left changes nothing about which driver runs the test — only the capabilities object naming the target device changes.
- **A completely separate driver** — This iPhone is automated by XCUITest, not UiAutomator2 — an entirely different technology under the hood, reached through the exact same find_element-style client call.

**How one Appium command reaches a real screen**

1. **Test code calls a WebDriver-style command** — find_element, click, and session start/end — the same API shape a Selenium tester already knows.
2. **The Appium server receives it over HTTP** — The command arrives as a JSON payload, the same transport Selenium's server used.
3. **The server hands it to the session's driver** — UiAutomator2 for an Android session, XCUITest for an iOS session — chosen by the capabilities the session started with.
4. **The driver runs it against the real OS automation layer** — UiAutomator2 talks to Android's own instrumentation framework; XCUITest talks to Apple's — neither one touches a browser DOM.

*Routing one client command to the right driver (Python)*

```python
sessions = [
    {"name": "android_settings_session", "platformName": "Android", "automationName": "UiAutomator2"},
    {"name": "ios_settings_session", "platformName": "iOS", "automationName": "XCUITest"},
    {"name": "android_webview_session", "platformName": "Android", "automationName": "UiAutomator2"},
]

driver_for = {
    ("Android", "UiAutomator2"): "UiAutomator2Driver",
    ("iOS", "XCUITest"): "XCUITestDriver",
}

command = "find_element(accessibility_id=login_button)"

distinct_drivers = set()
for s in sessions:
    key = (s["platformName"], s["automationName"])
    driver = driver_for.get(key, "UNKNOWN_DRIVER")
    print(s["name"] + "=" + driver)
    print("  command=" + command + " -> routed_to=" + driver)
    distinct_drivers.add(driver)

print("DISTINCT_DRIVERS=" + str(len(distinct_drivers)))
result = "PASS" if len(distinct_drivers) == 2 else "FAIL"
assert result == "PASS", "expected exactly 2 distinct native drivers behind one client API"
print("RESULT=" + result)
```

*Routing one client command to the right driver (Java)*

```java
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.TreeSet;

public class Main {
    public static void main(String[] args) {
        String[][] sessions = {
            {"android_settings_session", "Android", "UiAutomator2"},
            {"ios_settings_session", "iOS", "XCUITest"},
            {"android_webview_session", "Android", "UiAutomator2"},
        };

        Map<String, String> driverFor = new LinkedHashMap<>();
        driverFor.put("Android|UiAutomator2", "UiAutomator2Driver");
        driverFor.put("iOS|XCUITest", "XCUITestDriver");

        String command = "find_element(accessibility_id=login_button)";

        TreeSet<String> distinctDrivers = new TreeSet<>();
        for (String[] s : sessions) {
            String key = s[1] + "|" + s[2];
            String driver = driverFor.getOrDefault(key, "UNKNOWN_DRIVER");
            System.out.println(s[0] + "=" + driver);
            System.out.println("  command=" + command + " -> routed_to=" + driver);
            distinctDrivers.add(driver);
        }

        System.out.println("DISTINCT_DRIVERS=" + distinctDrivers.size());
        String result = distinctDrivers.size() == 2 ? "PASS" : "FAIL";
        if (!result.equals("PASS")) throw new AssertionError("expected exactly 2 distinct native drivers behind one client API");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Recognize Appium's shape before writing any code

- [ ] Confirm the platform and driver — Android sessions use the UiAutomator2 driver, iOS sessions use the XCUITest driver — know which one the target app needs before writing anything.
- [ ] Confirm the app type — Native, hybrid, or mobile web changes which locator strategies apply — a hybrid app's webview portion still accepts CSS and XPath.
- [ ] Find the WebDriver-style client library for your language — Appium's client libraries mirror Selenium's find_element/click API shape closely on purpose.
- [ ] Expect a view hierarchy, not a DOM — What you inspect on a native screen is the platform's own accessibility tree, not HTML.

- **A test written for a browser fails immediately against a native app, with no obvious error about a missing element.**
  Confirm platformName and the automation driver in the session's capabilities match a driver that is actually installed — a missing or mismatched driver is a common first-session failure.
- **A CSS selector or DOM-shaped XPath throws an invalid-selector error against a native screen.**
  Native apps have no DOM. Switch to accessibility id, a resource id, or a platform-specific selector — CSS and XPath only work against a webview's rendered HTML.
- **The exact same test code passes on Android and fails immediately on iOS.**
  Different OS, different driver, often different capabilities and locator values — expect platform-specific adjustments even when the calling code's shape stays identical.

### Where to check

- The Appium documentation's list of supported drivers, for platforms beyond UiAutomator2 and XCUITest.
- The W3C WebDriver specification, the base protocol Appium and Selenium both implement.
- [[mobile-testing/appium-intro/setup]] for installing the Appium server and a platform driver.
- [[mobile-testing/appium-intro/mobile-locators]] for the locator strategies that replace CSS and XPath on native screens.
- [[mobile-testing/device-and-os-matrix/fragmentation]] for why "Android" is not one uniform automation target either.

### Worked example: porting a login test from a browser to a native app

1. A Selenium test finds a login button with a CSS selector, clicks it, and asserts a welcome message
   appears.
2. Porting it straight to Appium, the CSS selector fails immediately — there is no DOM for a native login
   screen to query.
3. The tester captures the button's accessibility id from the native app instead and swaps it into the
   exact same find-then-click-then-assert shape the Selenium test already used.
4. The driver behind the session, not the shape of the test code, is what actually changed: UiAutomator2 in
   place of ChromeDriver.

**Quiz.** Why can a tester reuse Selenium's find_element/click pattern almost unchanged in Appium?

- [ ] Appium renders every native app as an HTML DOM behind the scenes
- [x] Both are built on the WebDriver protocol; Appium just routes the same commands to a platform driver (UiAutomator2, XCUITest) instead of a browser driver
- [ ] Appium automatically converts native apps into hybrid webviews before testing them
- [ ] Selenium and Appium share no real API, they only look similar by coincidence

*Appium adopts the same WebDriver client/server protocol Selenium uses. Only the driver behind the server, and therefore what is actually being automated, changes.*

- **What protocol does Appium share with Selenium?** — The WebDriver protocol — the same client/server command structure, routed to a different kind of driver.
- **Android driver** — UiAutomator2 — drives native Android apps through Android's own instrumentation framework.
- **iOS driver** — XCUITest — drives native iOS apps through Apple's own UI-testing framework.
- **Biggest mental-model shift from Selenium** — No DOM and no CSS selectors on native screens — elements come from the platform's own accessibility or view hierarchy instead.

### Challenge

Take one CSS selector or XPath expression from a Selenium test you know well, and write down what native-app locator strategy you would need instead, and specifically why the DOM-based version cannot work on a native screen.

- [Appium Documentation — Introduction](https://appium.io/docs/en/2.0/intro/)
- [Appium Documentation — Capabilities](https://appium.io/docs/en/2.0/guides/caps/)
- [Appium Beginner Tutorial 1 — What is Appium](https://www.youtube.com/watch?v=mAylNVddfJc)

🎬 [Appium Beginner Tutorial 1 — What is Appium](https://www.youtube.com/watch?v=mAylNVddfJc) (8 min)

- Appium and Selenium share the same WebDriver protocol — the same client command shape, sent to a different kind of driver.
- Android sessions run through the UiAutomator2 driver; iOS sessions run through XCUITest — neither talks to a browser DOM.
- Native screens have no DOM, so CSS selectors and DOM-shaped XPath do not carry over; a hybrid app's webview portion is the exception.
- Appium 2 decoupled the server from any one driver, so drivers are installed and versioned separately from the core server.


## Related notes

- [[Notes/mobile-testing/appium-intro/setup|Setup]]
- [[Notes/mobile-testing/appium-intro/first-mobile-test|First mobile test]]
- [[Notes/mobile-testing/appium-intro/mobile-locators|Mobile locators]]


---
_Source: `packages/curriculum/content/notes/mobile-testing/appium-intro/what-appium-is.mdx`_
