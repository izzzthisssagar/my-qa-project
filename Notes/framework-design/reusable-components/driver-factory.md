---
title: "Driver factory"
tags: ["framework-design", "reusable-components", "track-d"]
updated: "2026-07-17"
---

# Driver factory

*A DriverFactory centralizes WebDriver creation - browser choice, options, headless flag, local vs Grid - behind one method, so no test ever constructs its own driver inline, and moving the whole suite to headless Chrome on a grid is one config change instead of a find-and-replace.*

> The CI pipeline needs the suite headless on a Selenium Grid tonight. Simple question: where does
> the suite decide which browser it runs on? If the answer is "in forty test files, each with its own
> new ChromeDriver()" - including the one where someone hard-coded Firefox during an experiment and
> never changed it back - tonight just became a long night. A driver factory makes the answer one
> method, in one class, reading one config.

> **In real life**
>
> Nobody at a car plant builds their own car in the parking lot. An order comes in as a spec sheet -
> model, color, engine, trim - and the assembly line turns that spec into a finished car, the same
> way every time. The line owns the how: which parts, which sequence, which safety checks. Change the
> spec and the same line produces a different variant; retool the line once and every car after that
> carries the change. The buyers never touch a wrench - they just say what they need.

**Driver factory**: A driver factory is a class - usually DriverFactory with a static create() method - that is the single place in a framework where WebDriver instances are constructed. It reads the run's requirements from configuration (which browser, headless or headed, browser options and capabilities, local driver or RemoteWebDriver against a Selenium Grid URL) and returns a ready-to-use driver, so no test, page object, or base class ever contains new ChromeDriver() inline. Centralizing construction means the whole suite's browser setup is one readable method, switching browsers or environments is a config change rather than a code hunt, and options added once - a download directory, a language flag, a headless argument - apply to every driver the suite ever creates.

## One place that knows how drivers are born

Without a factory, driver construction is scattered - and each copy quietly makes its own
decisions:

```java
// LoginTest.java
WebDriver driver = new ChromeDriver();

// CheckoutTest.java - someone needed headless once, and hard-coded it here
ChromeOptions options = new ChromeOptions();
options.addArguments("--headless=new");
WebDriver driver = new ChromeDriver(options);

// SearchTest.java - left over from an experiment, never changed back
WebDriver driver = new FirefoxDriver();
```

With a factory, construction happens in exactly one place, driven by config:

```java
public final class DriverFactory {
    private DriverFactory() {}

    public static WebDriver create() throws MalformedURLException {
        String browser = System.getProperty("browser", "chrome");
        boolean headless = Boolean.getBoolean("headless");
        String gridUrl = System.getProperty("gridUrl", "");

        switch (browser) {
            case "firefox":
                FirefoxOptions firefox = new FirefoxOptions();
                if (headless) firefox.addArguments("-headless");
                return gridUrl.isEmpty()
                        ? new FirefoxDriver(firefox)
                        : new RemoteWebDriver(new URL(gridUrl), firefox);
            default:
                ChromeOptions chrome = new ChromeOptions();
                if (headless) chrome.addArguments("--headless=new");
                return gridUrl.isEmpty()
                        ? new ChromeDriver(chrome)
                        : new RemoteWebDriver(new URL(gridUrl), chrome);
        }
    }
}

// the only line anyone else ever writes - usually inside BaseTest's setup:
WebDriver driver = DriverFactory.create();
```

- **Tests never construct drivers** - they receive one, usually via the base class calling the
  factory in its setup hook. A test file that mentions ChromeDriver is a design smell.
- **The run is described by config, not code** - `-Dbrowser=firefox -Dheadless=true
  -DgridUrl=http://grid:4444` changes what the whole suite runs on with zero edits.
- **Options land once, apply everywhere** - a download directory, a window size, a language flag
  added in the factory reaches every driver the suite will ever create.
- **Local versus Grid is the factory's secret** - callers can't tell whether they got a local
  ChromeDriver or a RemoteWebDriver pointed at a grid, which is exactly why switching is painless.

> **Tip**
>
> Keep the factory honest by making it the only file allowed to import browser-specific classes -
> ChromeDriver, FirefoxOptions, RemoteWebDriver. That rule is greppable in review: any other file
> importing from org.openqa.selenium.chrome is routing around the factory, and it's the first place
> to look when "works locally, breaks in CI" appears.

> **Common mistake**
>
> Building the factory but letting it read nothing - create('chrome') hard-coded at the call site, or
> a BROWSER constant compiled into the code. If changing browsers requires editing and recommitting
> Java, the factory has centralized the construction but not the decision, and CI still can't flip
> the suite to headless Firefox without a code change. The factory's inputs must come from outside
> the code: system properties, environment variables, or a config file.

![Car assembly line inside the Opel factory in Gliwice, Poland - a white Opel Astra with open trunk and doors mid-assembly, a grey car with a green protective cover in the foreground, a blue car further down the line, overhead rails and equipment, and a yellow STREFA 2 hazard sign](driver-factory.jpg)
*Opel Astra assembly line, General Motors Manufacturing Poland, Gliwice — Wikimedia Commons, CC BY 3.0 (Marek Ślusarczyk / Tupungato). [Source](https://commons.wikimedia.org/wiki/File:002_Production_line_-_car_assembly_line_in_General_Motors_Manufacturing_Poland_-_Gliwice,_Poland.jpg)*
- **A car mid-assembly — a driver being built to spec** — Doors open, trunk open, options going in. The factory method does this for every driver: options, capabilities, and flags are applied during construction, before any caller touches it.
- **A different variant, same line** — Grey car, white car, blue car - different specs rolling off one process. Chrome, Firefox, headless, headed: one create() method produces every variant from the same code path.
- **The overhead infrastructure — shared by every car built** — Rails, power, and tooling serve the whole line from above. Config - browser name, headless flag, grid URL - plays that role for the factory: one supply feeding every driver's construction.
- **The STREFA 2 hazard sign — rules posted once for the whole line** — Safety policy is declared at the line, not negotiated per car. Browser policy works the same way: allowed browsers, default options, and environment rules are enforced in the factory, not left to each test's judgment.

**From forty private constructors to one factory**

1. **Every test news up its own driver** — new ChromeDriver() sprinkled through the suite - each copy a private decision about browser and options.
2. **The copies start to disagree** — CI needs headless, one test hard-codes Firefox, another pins an old options flag. Drift, file by file.
3. **The suite can't answer 'what browser do we test on?'** — The true answer lives in forty files and depends on which test you ask.
4. **Construction moves behind DriverFactory.create()** — Browser, options, headless, local-vs-grid: decided in one method, read from config.
5. **Tonight: headless Chrome on the grid. Tomorrow: local Firefox.** — A property flip per run - zero edits to any test file, and the whole suite always agrees.

The organizational core is simple: does each test decide how its driver is built, or does one
factory decide for everyone? Here's that difference as a small, generic simulation.

*Run it - flip one config and watch every driver follow (Python)*

```python
# Where does the suite decide WHICH browser it runs on? Two answers.

def create_driver(config):
    if config["remote"]:
        kind = "RemoteWebDriver -> " + config["grid_url"]
    else:
        kind = "local " + config["browser"].capitalize() + "Driver"
    mode = "headless" if config["headless"] else "headed"
    return f"{kind} ({mode})"

tests = ["LoginTest", "CheckoutTest", "SearchTest"]

print("--- every test builds its own driver inline ---")
inline = {
    "LoginTest":    "local ChromeDriver (headed)",
    "CheckoutTest": "local ChromeDriver (headed)",
    "SearchTest":   "local FirefoxDriver (headed)",  # someone experimented and left it
}
for test, driver in inline.items():
    print(f"{test:13} -> {driver}")
print("CI wants headless Chrome on the grid tonight: 3 files to edit, 1 already drifted")

print()
print("--- every test asks the factory ---")
config = {"browser": "chrome", "headless": False, "remote": False,
          "grid_url": "http://grid.internal:4444"}
for test in tests:
    print(f"{test:13} -> {create_driver(config)}")

print()
print("one config change: headless=True, remote=True")
config["headless"] = True
config["remote"] = True
for test in tests:
    print(f"{test:13} -> {create_driver(config)}")
print("edits to test files: 0")
```

Same single-point-of-decision shape in Java.

*Run it - flip one config and watch every driver follow (Java)*

```java
public class Main {
    // The one place that decides how a driver is built
    static String createDriver(String browser, boolean headless, boolean remote, String gridUrl) {
        String kind = remote
                ? "RemoteWebDriver -> " + gridUrl
                : "local " + browser.substring(0, 1).toUpperCase() + browser.substring(1) + "Driver";
        String mode = headless ? "headless" : "headed";
        return kind + " (" + mode + ")";
    }

    public static void main(String[] args) {
        String[] tests = {"LoginTest", "CheckoutTest", "SearchTest"};

        System.out.println("--- every test builds its own driver inline ---");
        System.out.println("LoginTest     -> local ChromeDriver (headed)");
        System.out.println("CheckoutTest  -> local ChromeDriver (headed)");
        System.out.println("SearchTest    -> local FirefoxDriver (headed)"); // someone experimented and left it
        System.out.println("CI wants headless Chrome on the grid tonight: 3 files to edit, 1 already drifted");

        System.out.println();
        System.out.println("--- every test asks the factory ---");
        for (String test : tests) {
            System.out.println(pad(test) + " -> " + createDriver("chrome", false, false, ""));
        }

        System.out.println();
        System.out.println("one config change: headless=true, remote=true");
        for (String test : tests) {
            System.out.println(pad(test) + " -> "
                    + createDriver("chrome", true, true, "http://grid.internal:4444"));
        }
        System.out.println("edits to test files: 0");
    }

    static String pad(String name) {
        return (name + "             ").substring(0, 13);
    }
}
```

### Your first time: Your mission: centralize driver creation, then flip the suite from the command line

- [ ] Find every place your suite (or a tutorial project) constructs a driver — Grep for 'new ChromeDriver' and 'new FirefoxDriver' - each hit is a private construction decision.
- [ ] Write DriverFactory.create() reading browser and headless from system properties — A switch on the browser name, options built per branch, sensible defaults when no property is set.
- [ ] Route all construction through the factory - usually one call in BaseTest's setup — Delete the inline constructions. Test files should no longer compile if they mention a concrete driver class.
- [ ] Run the suite twice without editing code: once plain, once with -Dbrowser=firefox -Dheadless=true — Watching the whole suite change browser from the command line is the payoff, live.

You've now moved the biggest environmental decision a suite makes - what it runs on - out of the
code and into configuration.

- **Tests pass locally but CI runs the wrong browser - or ignores the headless flag entirely.**
  Some construction still bypasses the factory. Grep for 'new ChromeDriver' and browser-specific imports outside DriverFactory; every hit is a private decision CI can't reach. Route them through the factory, then make the check a review rule.
- **Parallel test runs collide - two tests end up sharing (or quitting) the same driver.**
  The factory returns a shared static driver instead of a fresh one per request. A factory should construct on every create() call, and per-thread ownership belongs to the lifecycle code that calls it (base class or listener) - commonly with a ThreadLocal per test thread.
- **The factory works locally but throws when gridUrl is set - or silently runs local when you expected the grid.**
  Treat the config as input worth validating: fail loudly on a malformed grid URL, and log one line at creation time saying what was built ('chrome, headless, remote via http://grid:4444'). That one log line turns every 'what did CI actually run?' mystery into a lookup.
- **The factory has sprouted a dozen parameters and callers are passing options through it call by call.**
  The factory's contract is create() reads config - when callers hand it per-call options, the decision has moved back to the call sites. Fold recurring needs into named config (a profile: 'ci', 'local-debug') instead of parameters, so the factory stays the single decision point.

### Where to check

- **A grep for `new ChromeDriver` and friends** — exactly one file (the factory) should hit;
  every other hit is construction that config can't reach.
- **The factory method itself** — one screenful should answer what browsers are supported, which
  options each gets, and when the suite goes remote.
- **Your CI pipeline definition** — the browser/headless/grid values CI passes are the factory's
  real-world inputs; if CI passes nothing, the factory is only half wired.
- **Selenium's official documentation on browser options and Grid** — the capabilities and
  RemoteWebDriver mechanics the factory encapsulates.

### Worked example: the grid migration that touched one file

1. A team of four runs 80 UI tests locally in headed Chrome. Every test class builds its own
   driver; a few have private ChromeOptions tweaks that nobody remembers adding.
2. The company stands up a Selenium Grid and CI time-slots demand headless. Estimate under the
   current layout: edit 80 files, reconcile the scattered options, and hope nothing drifts back.
3. Instead, one engineer spends an afternoon on DriverFactory.create(): browser, headless, and
   gridUrl read from system properties; ChromeOptions and FirefoxOptions built in one place; the
   scattered per-test tweaks reviewed - two were obsolete, one (a download directory) became a
   factory default for everyone.
4. BaseTest's setup becomes driver = DriverFactory.create(). The 80 test files lose their
   construction lines entirely and never learn what they now run on.
5. CI's pipeline adds -Dheadless=true -DgridUrl=http://grid:4444 to the run command. Local
   developers change nothing. The migration's total code diff: one new class, one changed line in
   the base class, 80 deletions.

**Quiz.** CI must run the suite headless on a Selenium Grid, while developers keep running headed Chrome locally. With a proper driver factory in place, what changes to make that happen?

- [ ] Each test file gets an if-statement checking an IS_CI flag before constructing its driver
- [x] Nothing but configuration: CI passes properties like -Dheadless=true -DgridUrl=..., the factory reads them, and no test or factory code is edited
- [ ] The team maintains two branches of the suite - one constructing local drivers, one constructing remote drivers
- [ ] Selenium detects the CI environment automatically and switches to RemoteWebDriver on its own

*The factory's entire purpose is that the construction decision reads from outside the code - so different environments are different property sets against identical code. Option one re-scatters the decision into every test file, which is the exact disease the factory cures. Option three creates a permanent merge burden to represent what one if-statement in one factory expresses. Option four imagines machinery Selenium doesn't have: nothing switches to a grid unless your code constructs a RemoteWebDriver, and the factory is precisely the one place that knows when to do that.*

- **What does a driver factory centralize?** — All WebDriver construction: browser choice, options/capabilities, headless flag, and local versus RemoteWebDriver-on-Grid - one create() method reading config, used by the whole suite.
- **Where do tests get their driver under this pattern?** — They receive it - typically the base class calls DriverFactory.create() in its setup hook. Test files never mention ChromeDriver or FirefoxDriver at all.
- **Why must the factory read config instead of constants in code?** — So changing browser, headless mode, or grid target is a run-time flag (-Dbrowser=firefox) rather than an edit-and-recommit - which is what lets CI and local runs differ with identical code.
- **The greppable health check for this pattern** — Search for 'new ChromeDriver' and browser-specific imports: exactly one file - the factory - should hit. Every other hit is construction that config can't reach.
- **The assembly-line analogy for the driver factory** — Orders are spec sheets, the line owns how cars get built, and retooling the line once changes every car after it. Config is the spec, create() is the line, and no test ever builds its own car in the parking lot.

### Challenge

Take any suite with inline driver construction and stage the migration yourself: write
DriverFactory.create() reading browser, headless, and gridUrl from system properties, convert the
suite to use it (ideally via the base class), and then prove the payoff - run the same tests twice
from the command line with different -Dbrowser values and capture both runs' output. Bonus: add one
shared ChromeOptions default (like a download directory) and confirm every test inherits it.

### Ask the community

> My suite constructs drivers in `[N]` places and CI needs headless-on-grid while local stays headed. Here's my draft DriverFactory: `[paste it]`. What would you change about how it reads config and handles the local-versus-grid split?

Factory drafts attract precise feedback because the whole design fits in one method - reviewers
will quickly flag missing option defaults, unvalidated grid URLs, and the parallel-run pitfalls
that only show up at 2 a.m. in CI.

- [Selenium — official docs: browser options and capabilities](https://www.selenium.dev/documentation/webdriver/drivers/options/)
- [Refactoring Guru — Factory Method (the design pattern behind DriverFactory)](https://refactoring.guru/design-patterns/factory-method)

🎬 [Factory Pattern With Selenium WebDriver + Java + TestNG — Naveen AutomationLabs](https://www.youtube.com/watch?v=mVIWw59tj84) (21 min)

- A driver factory makes one method - DriverFactory.create() - the only place WebDriver instances are constructed, for the entire suite.
- The factory reads its decisions from config (browser, headless, grid URL), so what the suite runs on is a run-time flag, not a code edit.
- Tests never construct drivers - they receive one via the base class - and a test file mentioning ChromeDriver is a design smell you can grep for.
- Options and capabilities added in the factory apply to every driver the suite ever creates: one download-directory line reaches all eighty tests.
- Local versus Grid stays the factory's secret: callers cannot tell which they got, which is exactly why migrating environments touches one file.


## Related notes

- [[Notes/framework-design/reusable-components/base-classes|Base classes]]
- [[Notes/framework-design/reusable-components/waits-wrapper|Waits wrapper]]
- [[Notes/framework-design/page-object-model/the-pom-pattern|The POM pattern]]


---
_Source: `packages/curriculum/content/notes/framework-design/reusable-components/driver-factory.mdx`_
