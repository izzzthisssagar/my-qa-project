---
title: "Projects & browsers"
tags: ["playwright", "parallel-and-cross-browser", "track-d"]
updated: "2026-07-16"
---

# Projects & browsers

*One playwright.config.ts projects array runs the same test suite against Chromium, Firefox, and WebKit in a single command - one script, three real rendering engines, not three separate test suites.*

> A bug that only shows up in Safari never gets caught by a suite that only ever runs in Chrome - and
> WebKit, Playwright's Safari-equivalent engine, catches exactly that category of bug locally, before a
> real Safari user ever finds it. Writing the test once and running it against three real engines is a
> config setting, not three separate test suites to maintain.

> **In real life**
>
> The Rosetta Stone carries one royal decree carved three times - in hieroglyphic, in Demotic, and in
> Greek - the same content, rendered through three completely different writing systems on the same
> stone. Nobody wrote three different decrees. One message, three independent systems capable of
> misrendering it in three different ways, which is exactly why having all three mattered enough to
> carve.

**Projects**: Playwright projects are named configurations in the projects array of playwright.config.ts, each specifying a browser (or device) to run the exact same test suite against. The default scaffolded config already defines three projects - chromium, firefox, and webkit - so a single npx playwright test command runs every test file against all three real rendering engines without duplicating a single line of test code. A specific project can be targeted alone with --project=<name>, and projects can also represent device emulation (a specific mobile viewport/UA) rather than just a different browser engine.

## What a project actually is, and why three exist by default

```
export default defineConfig({
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
```

- **The same test files run against every project** — nothing in the test code itself names a
  browser; the project config supplies that.
- **Chromium, Firefox, and WebKit are three genuinely different rendering engines** — not three
  builds of the same engine. WebKit specifically is the closest local equivalent to real Safari,
  which has no other easy way to test cross-platform.
- **A project can represent a device, not just a browser** — `{ ...devices['iPhone 14'] }` runs the
  same suite with a mobile viewport and touch emulation, still against a real engine underneath.
- **`--project=<name>`** runs just one project when you don't need all three (fast local iteration,
  for example), without touching the config file itself.

> **Tip**
>
> When a test fails on only one project, resist the urge to immediately assume that project's engine is
> "buggy." Read the actual failure - a real, engine-specific rendering or behavior difference is
> sometimes the correct catch (the entire reason WebKit is included), not a false positive to skip past.

> **Common mistake**
>
> Writing engine-specific workarounds directly into test code (`if (browserName === 'webkit') { ... }`)
> to make a failing assertion pass everywhere. This usually papers over a real cross-browser bug in the
> app instead of surfacing it - the point of running three projects is to catch exactly this kind of
> difference, not to write around it in the test.

![The Rosetta Stone showing its three distinct horizontal bands of inscription - Egyptian hieroglyphic script at the top, Demotic script in the middle, and ancient Greek script at the bottom - the dark stone surface densely covered with the three carved scripts](projects-and-browsers.jpg)
*Rosetta Stone — Wikimedia Commons, CC BY-SA 4.0 (Hans Hillewaert). [Source](https://commons.wikimedia.org/wiki/File:Rosetta_Stone.JPG)*
- **Hieroglyphic band — one engine, one rendering system** — A complete, independent rendering of the same content - the same relationship a chromium project has to the underlying test: the full suite, expressed through one specific engine.
- **Demotic band — a second, unrelated system, same content** — Not a variant of the hieroglyphic text - a genuinely different script with its own rules. Firefox's Gecko engine is the same kind of independent system, not a re-skinned Chromium.
- **Greek band — the third independent rendering** — WebKit's role exactly: the closest available local stand-in for real Safari, an engine with its own real behavior, not a formality.
- **One stone, one decree, carved once per system** — The content itself was never rewritten between bands - only re-expressed. This is the whole point of a Playwright project: one test file, unmodified, run through each engine in turn.

**One test file, three engines, one command**

1. **npx playwright test is run** — No browser specified anywhere in the command or the test file itself.
2. **The chromium project runs the full suite** — Every test file, against Chromium.
3. **The firefox project runs the full suite** — The exact same test files, unmodified, against Firefox.
4. **The webkit project runs the full suite** — Again, the same files, against WebKit - Safari's closest local equivalent.
5. **One report, three engines' results** — A single run surfaces exactly which engine (if any) disagreed.

Running the same instructions against several independent interpreters and comparing results is
really just: apply one procedure multiple times, once per interpreter, and report where they
disagree. Here's that shape as a small, generic simulation.

*Run it - the same check, run against three independent interpreters (Python)*

```python
def check_button_color(engine, rendered_color):
    expected = "blue"
    return rendered_color == expected

engines = {
    "chromium": "blue",
    "firefox": "blue",
    "webkit": "blue-ish",  # a real rendering difference
}

results = {name: check_button_color(name, color) for name, color in engines.items()}

for engine, passed in results.items():
    print(f"{engine}: {'PASS' if passed else 'FAIL'}")

failing = [e for e, ok in results.items() if not ok]
print(f"\\nEngines disagreeing with the rest: {failing}")
```

Same run-against-each-engine, compare-results shape in Java.

*Run it - the same check, run against three independent interpreters (Java)*

```java
import java.util.*;

public class Main {
    static boolean checkButtonColor(String renderedColor) {
        return renderedColor.equals("blue");
    }

    public static void main(String[] args) {
        Map<String, String> engines = new LinkedHashMap<>();
        engines.put("chromium", "blue");
        engines.put("firefox", "blue");
        engines.put("webkit", "blue-ish"); // a real rendering difference

        List<String> failing = new ArrayList<>();
        for (var entry : engines.entrySet()) {
            boolean passed = checkButtonColor(entry.getValue());
            System.out.println(entry.getKey() + ": " + (passed ? "PASS" : "FAIL"));
            if (!passed) failing.add(entry.getKey());
        }

        System.out.println("\\nEngines disagreeing with the rest: " + failing);
    }
}
```

### Your first time: Your mission: run one suite against all three engines and find (or rule out) a real difference

- [ ] Confirm your scratch project's playwright.config.ts still has all three default projects — chromium, firefox, webkit - untouched from npm init playwright@latest.
- [ ] Run npx playwright test with no --project flag — Confirm the report shows results broken out per project, not just one combined pass/fail.
- [ ] Run npx playwright test --project=webkit alone — Confirm it runs faster and reports only WebKit's results.
- [ ] Pick one real visual or interactive element in your test target and compare it by eye across all three engines — Even without a failing test, get in the habit of noticing real rendering differences, not just trusting they don't exist.

You've now run one suite across three genuinely independent engines and practiced noticing where they
might actually differ.

- **A test passes on chromium and firefox but consistently fails only on webkit.**
  Treat this as a real signal first, not noise - check whether the feature actually behaves differently in Safari-family engines (a CSS property, a form control default, a timing quirk) before assuming the test itself is wrong.
- **webkit tests are noticeably slower or flakier than chromium/firefox on the same suite.**
  WebKit's browser automation surface is genuinely less mature in some edge cases than Chromium's - check Playwright's own release notes/issues for known WebKit-specific timing quirks before assuming your test is at fault.
- **A teammate wants to just delete the webkit project to make CI faster and greener.**
  This trades away the one project most likely to catch a real Safari-only bug before a real Safari user does - if speed is the actual concern, look at parallelism and sharding (next notes) before removing engine coverage entirely.
- **Device-emulation projects (like 'Mobile Safari') behave differently from what a real device shows.**
  Emulation approximates a device's viewport, UA, and touch behavior on top of a desktop engine - it's a strong first signal, not a perfect substitute for testing on an actual physical device for anything touch- or performance-sensitive.

### Where to check

- **`playwright.config.ts`'s `projects` array** — the definitive list of what actually gets tested,
  and under what name.
- **The HTML report, filtered by project** — confirms at a glance which specific engine(s) a failure
  is isolated to.
- **`playwright.dev`'s own browser support notes** — documents known engine-specific behavior
  differences worth checking before assuming a failure is a test bug.
- **`--project=<name>`** on any local run — the fastest way to isolate investigation to just the
  engine actually showing a problem.

### Worked example: a real WebKit-only bug that projects caught before Safari users did

1. A date picker component passes cleanly on chromium and firefox in every CI run.
2. It fails consistently on webkit with a timeout on a specific animation-dependent interaction.
3. Rather than adding a webkit-specific skip, the team opens the same page manually in real Safari on
   a Mac and reproduces the exact same stuck interaction - it's a genuine bug in how the component
   handles a CSS transition, specific to WebKit's animation timing.
4. The fix addresses the actual CSS issue in the component. Re-running all three projects afterward
   shows webkit now passing too, with no change needed to the test itself.
5. The bug never reached a real Safari user, because the webkit project caught it in exactly the same
   engine family Safari actually uses, days before any release.

**Quiz.** A test fails only on the webkit project, passing cleanly on chromium and firefox. What's the most appropriate first response?

- [ ] Add a browserName === 'webkit' check in the test to skip the failing assertion on WebKit specifically
- [x] Investigate whether the app genuinely behaves differently in WebKit - this is precisely the kind of real, engine-specific bug running three projects exists to catch, since WebKit is the closest local equivalent to real Safari
- [ ] Delete the webkit project since it's clearly less reliable than the other two
- [ ] Assume it's a flaky test and re-run until it passes

*The note's worked example demonstrates exactly this: a webkit-only failure often IS a real, catchable difference, and the correct response is to investigate the app's actual behavior in that engine family before touching the test. Option one is the specific mistake the note's Callout warns against - papering over a real difference instead of surfacing it. Option three throws away the entire value proposition of cross-browser projects to avoid dealing with a real finding. Option four assumes flakiness without evidence, when a CONSISTENT single-project failure is a strong signal of a genuine, reproducible difference, not randomness.*

- **What are Playwright's three default projects?** — chromium, firefox, webkit - three genuinely independent rendering engines, not three builds of one engine.
- **What makes webkit specifically valuable to include?** — It's the closest local equivalent to real Safari, which has no easy separate way to test cross-platform.
- **How do you run just one project locally?** — npx playwright test --project=<name>, without editing the config file.
- **Why is a browserName === 'webkit' skip in test code usually a mistake?** — It papers over a real cross-browser difference instead of surfacing it - defeating the actual purpose of running multiple engine projects.
- **The Rosetta Stone analogy for projects** — One decree (test suite), carved three times through three independent systems (hieroglyphic/Demotic/Greek = chromium/firefox/webkit) - same content, three real, independently-capable-of-differing renderings.

### Challenge

Pick a real interactive component (a dropdown, a date picker, a custom form control) on a site you
use. Write one Playwright test against it and run it across all three default projects. If all three
pass identically, deliberately inspect the component's CSS for anything vendor-specific or
animation-dependent that COULD plausibly differ in WebKit, and explain in one sentence why it either
does or doesn't actually cause a difference in practice.

### Ask the community

> My test passes on chromium/firefox but fails only on webkit with `[describe the failure]`. Here's the relevant markup/CSS: `[paste it]`.

Pasting the actual failure alongside the relevant markup or CSS usually reveals quickly whether this
is a known WebKit-specific behavior difference or something else entirely.

- [Playwright — official Projects docs](https://playwright.dev/docs/test-projects)
- [Playwright — official Browsers docs](https://playwright.dev/docs/browsers)

🎬 [Playwright Cross-Browser Testing Tutorial — Chromium, Firefox & WebKit Setup — Test Automation 101](https://www.youtube.com/watch?v=Tpzvq0mxdgc) (10 min)

- Playwright projects (chromium, firefox, webkit by default) run the exact same test suite against three genuinely independent rendering engines with one command.
- WebKit specifically matters because it's the closest local equivalent to real Safari, which has no other easy cross-platform testing path.
- A test that fails on only one project is often a real, valuable finding - not noise to skip past with a browser-specific workaround in test code.
- --project=<name> runs a single engine locally without touching the config, useful for fast iteration.
- Projects can also represent device emulation (a mobile viewport/UA on top of a real engine), a strong first signal though not a full substitute for real-device testing.


## Related notes

- [[Notes/playwright/parallel-and-cross-browser/parallelism-and-sharding|Parallelism & sharding]]
- [[Notes/playwright/parallel-and-cross-browser/retries|Retries]]
- [[Notes/playwright/parallel-and-cross-browser/config|Config]]


---
_Source: `packages/curriculum/content/notes/playwright/parallel-and-cross-browser/projects-and-browsers.mdx`_
