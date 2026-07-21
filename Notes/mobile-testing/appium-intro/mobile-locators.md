---
title: "Mobile locators"
tags: ["mobile-testing", "appium-intro", "track-c"]
updated: "2026-07-21"
---

# Mobile locators

*Native screens have no DOM, so Appium defines its own locator strategies per platform -- accessibility id, Android's UiAutomator selector, iOS's predicate string and class chain -- and accessibility id is usually the most stable choice.*

> A tester used to `document.querySelector`-style thinking opens a mobile app's element tree for the first
> time looking for a class name or an id attribute to copy into a CSS selector, and finds neither — just a
> native view hierarchy with its own vocabulary, one that has nothing to do with HTML at all.

> **In real life**
>
> Finding a specific person in a building works differently depending on the building. In an office with name
> plates on every door, you read the plate — fast, unambiguous, exactly one answer. In a building with no name
> plates, you might describe someone by their badge number if you have it, or fall back to "third door on the
> left, past the plant" if you don't — a description that stops working the moment the furniture gets
> rearranged. Accessibility id is the name plate. Position- or text-based fallbacks are the "third door on the
> left" — they work today, and quietly stop working the next time the screen changes shape.

**A locator**: A locator, on a mobile screen, is a platform-specific expression that identifies one element in the native view or accessibility hierarchy the operating system exposes. There is no DOM to query, so Appium and each platform define their own selector vocabulary instead of reusing CSS selectors or DOM-shaped XPath.

## Why CSS and XPath don't carry over

A web page's DOM is one standard tree with one standard query language surface: tag names, classes, CSS
selectors, and XPath all assume that structure exists. A native app has no DOM. Android exposes its own
element tree through the accessibility and UI-testing frameworks; iOS exposes its own through XCUITest. Each
platform has its own attribute vocabulary — Android elements carry a `resource-id` and a `content-desc`;
iOS elements carry an accessibility identifier and a `label`. Appium's locator strategies exist specifically
to read those platform-native attributes, because there is no shared HTML-like structure underneath to fall
back on.

## The strategies

**Accessibility id** is the one cross-platform strategy: the same strategy name works on Android and iOS,
though the underlying value comes from a different attribute on each — `content-desc` on Android, the
accessibility identifier on iOS. It is usually close to a direct id lookup rather than a search through the
whole tree, which makes it fast as well as stable.

**UiAutomator selector** (`-android uiautomator`) is Android-only. It takes a `UiSelector`-style expression
string — for example matching on `resourceId` or visible `text` — and can chain conditions together. It is
powerful, but Android-only and slower than accessibility id, because the expression runs as a small program
against the device's UI hierarchy rather than resolving as a direct lookup.

**iOS predicate string** (`-ios predicate string`) is iOS-only: an `NSPredicate`-style expression evaluated
against an element's attributes, such as matching where `label` equals a given string. **iOS class chain**
(`-ios class chain`) is also iOS-only — a leaner, XPath-like syntax scoped to declared element types, more
expressive than a predicate string for structural queries while staying faster than full XPath.

> **Tip**
>
> Capture the exact identifier from a live inspector against the running app, not from guessing at the app's
> source code. Generated ids, localized display strings, and dynamically populated content can all differ
> between what's in the source and what actually renders on screen.

> **Common mistake**
>
> Do not reach for XPath first out of web habit. On both platforms it is the slowest and most brittle
> strategy — it walks the full element hierarchy and breaks on almost any structural change to the screen.
> Treat it as a last resort for the rare element with no accessibility id, resource id, or predicate-matchable
> attribute, not a default starting point.

![Android phone home screen showing a YouTube icon with a text label, a YT Music icon with a text label, and a dock row of Phone, Messages, and Camera icons with no visible text labels](mobile-locators.jpg)
*OnePlus Nord smartphone displaying Android home screen — Gannu03, Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:OnePlus_Nord_smartphone_displaying_Android_home_screen.jpg)*
- **An icon with a visible text label** — YouTube has both an icon and an on-screen label — exactly the kind of element accessibility id locators are built for, since that label is usually the same string exposed as content-desc.
- **A second labeled icon, same story** — YT Music is a different element with an equally stable label. A UiAutomator selector matching this exact text would work too, but accessibility id doesn't depend on the visible string matching pixel-for-pixel.
- **An icon with no visible text label** — The dock's phone icon has no on-screen label at all. A CSS-style find-by-visible-text approach has nothing to grab here — the element still carries a content-desc or resource-id underneath, which accessibility id and resource-id locators read directly.
- **Same shape, no distinguishing text** — Neighboring dock icons look visually identical in style. A locator built on position or a generic class name alone is fragile here; a stable identifier is what actually tells these elements apart reliably.

**Choosing a locator strategy for one element**

1. **Check for an accessibility id first** — Cross-platform, close to a direct lookup, and usually the most stable choice available.
2. **Fall back to a platform-native id** — resource-id on Android, or an iOS predicate matching a unique attribute, when no accessibility id exists.
3. **Use a structural strategy only when needed** — UiAutomator selector chaining on Android, class chain on iOS — for elements no simple id can isolate.
4. **Treat XPath as the last resort** — Slowest and most brittle on both platforms; reach for it only when nothing else can identify the element.

*Choosing a locator strategy by priority (Python)*

```python
elements = [
    {"name": "login_button", "accessibility_id": "login_button", "resource_id": "com.shop:id/login_button", "text": "Log in"},
    {"name": "promo_banner", "resource_id": "com.shop:id/promo_banner", "text": "50% off today"},
    {"name": "price_label", "text": "$19.99"},
]

priority = ["accessibility_id", "resource_id", "text"]

def choose_strategy(element):
    for key in priority:
        if element.get(key):
            return key, element[key]
    return "xpath_fallback", "//*[last()]"

chosen_strategies = []
for el in elements:
    strategy, value = choose_strategy(el)
    chosen_strategies.append(strategy)
    print(el["name"] + " -> strategy=" + strategy + " value=" + value)

print("STRATEGIES_USED=" + ",".join(chosen_strategies))
result = "PASS" if chosen_strategies == ["accessibility_id", "resource_id", "text"] else "FAIL"
assert result == "PASS", "expected strategy priority accessibility_id > resource_id > text for this fixture"
print("RESULT=" + result)
```

*Choosing a locator strategy by priority (Java)*

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        List<Map<String, String>> elements = new ArrayList<>();

        Map<String, String> loginButton = new LinkedHashMap<>();
        loginButton.put("name", "login_button");
        loginButton.put("accessibility_id", "login_button");
        loginButton.put("resource_id", "com.shop:id/login_button");
        loginButton.put("text", "Log in");
        elements.add(loginButton);

        Map<String, String> promoBanner = new LinkedHashMap<>();
        promoBanner.put("name", "promo_banner");
        promoBanner.put("resource_id", "com.shop:id/promo_banner");
        promoBanner.put("text", "50% off today");
        elements.add(promoBanner);

        Map<String, String> priceLabel = new LinkedHashMap<>();
        priceLabel.put("name", "price_label");
        priceLabel.put("text", "$19.99");
        elements.add(priceLabel);

        String[] priority = {"accessibility_id", "resource_id", "text"};

        List<String> chosenStrategies = new ArrayList<>();
        for (Map<String, String> el : elements) {
            String strategy = "xpath_fallback";
            String value = "//*[last()]";
            for (String key : priority) {
                if (el.get(key) != null) {
                    strategy = key;
                    value = el.get(key);
                    break;
                }
            }
            chosenStrategies.add(strategy);
            System.out.println(el.get("name") + " -> strategy=" + strategy + " value=" + value);
        }

        System.out.println("STRATEGIES_USED=" + String.join(",", chosenStrategies));
        boolean matches = chosenStrategies.equals(Arrays.asList("accessibility_id", "resource_id", "text"));
        String result = matches ? "PASS" : "FAIL";
        if (!result.equals("PASS")) throw new AssertionError("expected strategy priority accessibility_id > resource_id > text for this fixture");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Pick a locator for one real element

- [ ] Inspect the element live — Use an inspector against the running app rather than guessing an id from source code.
- [ ] Check for an accessibility id first — Cross-platform, close to a direct lookup, and the most stable choice when the app provides one.
- [ ] Fall back to a platform-native id — resource-id on Android, or a predicate matching a unique attribute on iOS.
- [ ] Reach for a structural strategy only if needed — UiAutomator selector chaining, or iOS class chain, for elements no simple id can isolate.
- [ ] Treat XPath as the last option — Confirm nothing else can identify the element before falling back to it.

- **A locator that worked yesterday finds nothing today, with no app functionality actually broken.**
  A structural or position-based locator broke because the screen's layout shifted slightly. Switch to accessibility id or a resource id, which don't depend on structural position.
- **The same accessibility id locator works on Android but not on iOS.**
  Accessibility id is cross-platform as a strategy name, but the underlying value is set independently per platform — confirm the iOS accessibility identifier was actually assigned to that element too.
- **An XPath-based locator times out or matches the wrong element after a minor UI change.**
  XPath walks the full hierarchy and is the most sensitive strategy to structural change. Replace it with accessibility id or resource id where possible.
- **A UiAutomator selector matching visible text fails after a localization change.**
  Text-based selectors break when the app's display language changes. Prefer resource-id or accessibility id, which don't depend on the visible string.

### Where to check

- An Appium inspector tool, for confirming the exact live value of an element's accessibility id, resource-id, or attributes.
- The Appium documentation's locator strategies reference for the current supported selector syntax per platform.
- [[mobile-testing/appium-intro/first-mobile-test]] for where a locator's value gets used inside a find-element call.
- [[mobile-testing/appium-intro/what-appium-is]] for why native screens have no DOM to query in the first place.
- [[mobile-testing/appium-intro/setup]] for getting a driver running against a real device or emulator to inspect against.

### Worked example: a locator that broke on a redesign it had nothing to do with

1. A test locates a checkout button using a UiAutomator selector chained on its position as the third
   button in a container.
2. A later release adds a promo banner above the button, shifting its position in the container without
   changing anything about the button itself.
3. The position-based locator now finds the wrong element, and the test fails on a change unrelated to
   checkout at all.
4. Replacing the locator with the button's accessibility id fixes it permanently — that identifier doesn't
   depend on where the button sits relative to its neighbors.

**Quiz.** Why is accessibility id usually the most stable locator strategy in Appium?

- [ ] It is the only strategy Appium supports on real devices
- [x] It is a cross-platform strategy that maps to a stable, developer-assigned identifier rather than an element's position or visible text, which both change more often
- [ ] It automatically updates itself whenever the app's UI changes
- [ ] It only works on iOS, so Android tests never need to worry about it

*Accessibility id reads an explicit identifier the app assigns for accessibility purposes. That identifier isn't tied to layout position or visible text, so it survives UI changes that break position- or text-based locators.*

- **Accessibility id** — A cross-platform Appium locator strategy reading content-desc on Android or the accessibility identifier on iOS — usually the fastest and most stable choice.
- **UiAutomator selector** — -android uiautomator — an Android-only strategy using a UiSelector-style expression string, capable of chaining conditions.
- **iOS predicate string vs class chain** — Predicate string is an NSPredicate-style attribute match; class chain is a leaner, XPath-like syntax scoped to declared element types. Both are iOS-only.
- **Why XPath is a last resort on mobile** — It walks the full element hierarchy on both platforms, making it the slowest and most brittle strategy to structural UI changes.

### Challenge

Pick one element in an app you know that currently has no visible text label, and write down which locator strategy you would actually need to find it reliably, and why a text-based approach can't work there.

- [Appium Documentation — Finding Elements](https://appium.readthedocs.io/en/latest/en/writing-running-appium/finding-elements/)
- [Appium Documentation — Capabilities](https://appium.io/docs/en/2.0/guides/caps/)
- [Appium Beginner Tutorial 8 — Using Appium Desktop Inspector to Find Object Locators](https://www.youtube.com/watch?v=P2lM4NY4CTU)

🎬 [Appium Beginner Tutorial 8 — Using Appium Desktop Inspector to Find Object Locators](https://www.youtube.com/watch?v=P2lM4NY4CTU) (11 min)

- Native screens have no DOM, so Appium defines its own locator strategies instead of reusing CSS selectors or DOM-shaped XPath.
- Accessibility id is cross-platform and usually the fastest, most stable choice, since it reads a developer-assigned identifier rather than layout or visible text.
- UiAutomator selector is Android-only; iOS predicate string and class chain are iOS-only — each platform still needs its own fallback strategies.
- XPath is the slowest and most brittle strategy on both platforms and belongs at the bottom of the priority list, not the top.


## Related notes

- [[Notes/mobile-testing/appium-intro/what-appium-is|What Appium is]]
- [[Notes/mobile-testing/appium-intro/first-mobile-test|First mobile test]]
- [[Notes/mobile-testing/appium-intro/setup|Setup]]


---
_Source: `packages/curriculum/content/notes/mobile-testing/appium-intro/mobile-locators.mdx`_
