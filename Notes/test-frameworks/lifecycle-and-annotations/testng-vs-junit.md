---
title: "TestNG vs JUnit"
tags: ["test-frameworks", "lifecycle-and-annotations", "track-d"]
updated: "2026-07-17"
---

# TestNG vs JUnit

*JUnit 5 is the default for plain unit testing and the safer starting choice for a new project, while TestNG's built-in parallel execution, grouping, and dependsOnMethods ordering still make it a common pick specifically for larger Selenium suites.*

> Both frameworks discover a method, run it, and report pass or fail - from a distance, TestNG and
> JUnit look like two names for the same thing. Try to run 500 Selenium tests across four browsers in
> parallel, or make one test depend on another finishing first, and the distance closes fast: one of
> them does that out of the box, and the other needs an extra library bolted on to get there.

> **In real life**
>
> At Wallaroo, South Australia, a stretch of railway carries two different track gauges down the same
> corridor - narrower and broader rails, sharing one common rail between them, both leading the same
> direction. A narrow-gauge train and a broad-gauge train solve the exact same problem (getting people
> and freight from one end of the line to the other) but they are built to genuinely different
> standards, and a wheelset built for one physically cannot run on the other. Picking a gauge isn't
> picking a "wrong" answer - it's picking which specific, incompatible standard the rest of your
> rolling stock has to match.

**TestNG vs JUnit**: TestNG and JUnit are the two dominant Java test frameworks, solving the same core problem (discovering and running test methods, reporting results) with different feature sets and defaults. JUnit - specifically JUnit 5 (Jupiter) today - is the ecosystem default: the most widely used Java testing library overall, deeply integrated into Maven, Gradle, Spring Boot, and most IDEs out of the box, with lifecycle hooks named @BeforeEach/@AfterEach (per-test) and @BeforeAll/@AfterAll (per-class). TestNG, built afterward and explicitly designed to address gaps JUnit had at the time, ships built-in parallel test execution (no extra plugin required), flexible grouping via @Test(groups = {...}), explicit dependency ordering via dependsOnMethods, and native data providers via @DataProvider for parameterized tests. Neither framework is simply 'better' - JUnit 5 has since closed much of the original gap (parameterized tests, tags roughly comparable to groups, extensions), and the honest 2026 guidance is: JUnit 5 is the safer default for a new project's general unit testing, while TestNG remains a common, often-preferred choice specifically for larger Selenium/UI automation suites that lean hard on its native parallelism, grouping, and method-dependency features.

## Where the two actually diverge

```java
// TestNG: native grouping and explicit method dependencies, no extra library
import org.testng.annotations.Test;

public class CheckoutTests {

    @Test(groups = "smoke")
    public void userCanLogIn() {
        // ...
    }

    @Test(groups = "smoke", dependsOnMethods = "userCanLogIn")
    public void loggedInUserCanAddToCart() {
        // only runs if userCanLogIn passed first - and is skipped, not failed, otherwise
    }

    @Test(groups = "regression", dependsOnMethods = "loggedInUserCanAddToCart")
    public void cartTotalReflectsDiscountCode() {
        // ...
    }
}
```

- **Parallel execution** — TestNG supports parallel execution at the method, class, or suite level
  directly through its XML suite configuration, no extra dependency. JUnit 5 supports it too, but it's
  opt-in via a separate configuration property and, historically, needed extra setup to feel as
  turnkey - for a large Selenium suite needing to fan out across multiple browser sessions, TestNG's
  version has traditionally been the path of less resistance.
- **Grouping** — `@Test(groups = {"smoke", "regression"})` lets one method belong to multiple named
  groups, and a run can include or exclude by group directly from the command line or XML suite file.
  JUnit 5's closest equivalent is `@Tag`, which covers similar ground but arrived later and is less
  commonly the reason a team specifically reaches for JUnit.
- **`dependsOnMethods`** — TestNG can declare that one test should only run after another specific
  test has passed, and will report a dependent test as SKIPPED (not failed) if its dependency didn't
  pass. JUnit has no direct built-in equivalent - the JUnit philosophy generally discourages
  inter-test dependencies in favor of fully independent tests, which is a genuine design difference,
  not just a missing feature.
- **`@DataProvider`** — TestNG's native way to run the same test method against many different input
  rows, returning a 2D array or iterator of argument sets. JUnit 5 has its own comparable mechanism
  (`@ParameterizedTest` with `@CsvSource`, `@MethodSource`, and others) that arrived in JUnit 5 and is
  now considered on par - this used to be a clearer TestNG advantage than it is today.
- **Ecosystem and defaults** — JUnit 5 ships as the default test dependency in a fresh Spring Boot
  project and most Java tutorials; it has the larger overall download share and IDE support. TestNG's
  strongest, most durable use case in 2026 is specifically Selenium and other large UI-automation
  suites where its native parallelism, grouping, and dependency ordering solve real, common problems
  those suites hit - not a general claim that it's "better" outside that context.

> **Tip**
>
> Don't treat this as a permanent, ideological choice. A team already standardized on JUnit 5 for unit
> tests can still reach for TestNG specifically for its Selenium/E2E suite if the parallel-execution and
> grouping features solve a real, current pain point - the two frameworks aren't mutually exclusive
> across a single codebase's different test types, even though mixing them within ONE module adds real
> build-configuration complexity worth weighing against the benefit.

> **Common mistake**
>
> Choosing TestNG (or JUnit) for a new project based on outdated advice or a tutorial written years
> earlier, without checking what each framework's current version actually supports. JUnit 5 closed a
> real gap with parameterized tests and tags; TestNG's parallel execution and dependsOnMethods are still
> genuinely native advantages JUnit hasn't fully matched. The comparison shifts over time - re-verify
> against each framework's current documentation rather than repeating a comparison that was accurate
> in 2018.

![A rural railway track at Wallaroo, South Australia, receding toward the horizon, showing dual-gauge rail infrastructure with an additional inner rail running alongside the main pair on wooden sleepers, dry grass fields on either side](testng-vs-junit.jpg)
*Wallaroo dual-gauge railway — Wikimedia Commons, CC BY-SA 4.0 (Vmenkov). [Source](https://commons.wikimedia.org/wiki/File:Wallaroo-dual-gauge-railway-0855.jpg)*
- **The outer rail on one side — one gauge's own boundary** — Belongs to one specific standard; a wheelset built for it never runs on the other gauge's spacing. Neither framework's specific feature set 'fits' the other's use case by accident - each is built to its own standard.
- **The extra rail running alongside the main pair** — One rail shared between two different gauges at once - the physical point where both standards overlap, the way TestNG and JUnit both ultimately solve the exact same underlying problem (discover a method, run it, report the result) even while diverging sharply on how.
- **The two rail sets, laid down the same corridor** — Two genuinely different standards sharing the same ground, built for the same kind of traffic - a Java project still has to commit to one framework (or deliberately run both, at real configuration cost) the same way a train has to commit to one gauge.
- **The track continuing on, unchanged, toward the horizon** — Whichever gauge a given line commits to, the destination is identical: a test that ran and reported a result. The frameworks just get there by two different, not fully interchangeable standards.

**Same test suite, two different engines under it**

1. **Both engines discover the same @Test-annotated methods** — Discovery itself looks nearly identical between the two frameworks.
2. **JUnit 5's engine runs each test independently, in isolation by default** — No built-in concept of one test depending on another - by design philosophy, not oversight.
3. **TestNG's engine checks dependsOnMethods and groups before running each test** — A test whose dependency failed is marked SKIPPED, never even attempted.
4. **TestNG's suite XML fans tests out across parallel threads natively** — JUnit 5 can do this too, but via an opt-in configuration property, not the out-of-the-box default.
5. **Both report pass/fail/skipped back to the build tool identically** — From Maven or Gradle's perspective, the final report format converges - the divergence is entirely in HOW each engine got there.

Strip away the annotations and this comparison is really just: two different engines given the exact
same list of test definitions, with different rules for how they decide execution order and whether
they run things at once. Here's that shape as a small, generic simulation.

*Run it - two engines, same test definitions, different execution rules (Python)*

```python
tests = [
    {"name": "user_can_log_in", "group": "smoke", "depends_on": None},
    {"name": "logged_in_user_can_add_to_cart", "group": "smoke", "depends_on": "user_can_log_in"},
    {"name": "cart_total_reflects_discount", "group": "regression", "depends_on": "logged_in_user_can_add_to_cart"},
]

def simple_engine(tests):
    print("--- simple engine (JUnit-style: independent, no dependency awareness) ---")
    for t in tests:
        print(f"  running {t['name']}: PASS")

def dependency_aware_engine(tests):
    print("--- dependency-aware engine (TestNG-style: groups + dependsOnMethods) ---")
    results = {}
    for t in tests:
        dep = t["depends_on"]
        if dep and results.get(dep) != "PASS":
            results[t["name"]] = "SKIPPED"
            print(f"  {t['name']} [{t['group']}]: SKIPPED (dependency '{dep}' did not pass)")
            continue
        results[t["name"]] = "PASS"
        print(f"  {t['name']} [{t['group']}]: PASS")

simple_engine(tests)
dependency_aware_engine(tests)

# now simulate the dependency actually failing
tests[0] = {**tests[0], "will_fail": True}
print("--- dependency-aware engine, with the first test now failing ---")
results = {}
for t in tests:
    dep = t["depends_on"]
    if t.get("will_fail"):
        results[t["name"]] = "FAIL"
        print(f"  {t['name']}: FAIL")
        continue
    if dep and results.get(dep) != "PASS":
        results[t["name"]] = "SKIPPED"
        print(f"  {t['name']}: SKIPPED (dependency '{dep}' did not pass)")
        continue
    results[t["name"]] = "PASS"
    print(f"  {t['name']}: PASS")
```

Same two-engines comparison in Java.

*Run it - two engines, same test definitions, different execution rules (Java)*

```java
import java.util.*;

public class Main {
    record TestDef(String name, String group, String dependsOn, boolean willFail) {}

    static void simpleEngine(List<TestDef> tests) {
        System.out.println("--- simple engine (JUnit-style: independent, no dependency awareness) ---");
        for (TestDef t : tests) {
            System.out.println("  running " + t.name() + ": PASS");
        }
    }

    static void dependencyAwareEngine(List<TestDef> tests) {
        System.out.println("--- dependency-aware engine (TestNG-style: groups + dependsOnMethods) ---");
        Map<String, String> results = new HashMap<>();
        for (TestDef t : tests) {
            if (t.willFail()) {
                results.put(t.name(), "FAIL");
                System.out.println("  " + t.name() + ": FAIL");
                continue;
            }
            String dep = t.dependsOn();
            if (dep != null && !"PASS".equals(results.get(dep))) {
                results.put(t.name(), "SKIPPED");
                System.out.println("  " + t.name() + " [" + t.group() + "]: SKIPPED (dependency '" + dep + "' did not pass)");
                continue;
            }
            results.put(t.name(), "PASS");
            System.out.println("  " + t.name() + " [" + t.group() + "]: PASS");
        }
    }

    public static void main(String[] args) {
        List<TestDef> tests = List.of(
            new TestDef("userCanLogIn", "smoke", null, false),
            new TestDef("loggedInUserCanAddToCart", "smoke", "userCanLogIn", false),
            new TestDef("cartTotalReflectsDiscount", "regression", "loggedInUserCanAddToCart", false)
        );

        simpleEngine(tests);
        dependencyAwareEngine(tests);

        List<TestDef> withFailure = List.of(
            new TestDef("userCanLogIn", "smoke", null, true),
            new TestDef("loggedInUserCanAddToCart", "smoke", "userCanLogIn", false),
            new TestDef("cartTotalReflectsDiscount", "regression", "loggedInUserCanAddToCart", false)
        );
        System.out.println("--- dependency-aware engine, with the first test now failing ---");
        dependencyAwareEngine(withFailure);
    }
}
```

### Your first time: Your mission: run the same three tests under both frameworks and compare what you actually see

- [ ] Create two tiny scratch projects: one with JUnit 5, one with TestNG, each with the same three test methods (login, add-to-cart, checkout) — Keep the logic trivial - the point is comparing the frameworks' behavior, not the test logic.
- [ ] In the TestNG project, make the second test dependsOnMethods the first, and make the first test deliberately fail — Run it - confirm the second and third tests report SKIPPED, not just absent or failed.
- [ ] In the JUnit 5 project, try to express the same 'only run this if that one passed' relationship — Notice there's no direct built-in equivalent - you'd need to build it yourself (a shared boolean flag, a JUnit extension), which is the actual design difference, not a missing checkbox.

You've now seen the two frameworks' actual divergence directly, not just read a comparison table
about it.

- **A TestNG test depending on another via dependsOnMethods is reported SKIPPED and it's unclear why.**
  Check whether the method it depends on actually passed in this specific run - dependsOnMethods marks a test SKIPPED (not run at all) whenever its dependency didn't pass, which is by design, not a bug.
- **Tests that pass individually start failing intermittently only when run in TestNG's parallel mode.**
  That's almost always shared mutable state between tests that parallel execution now runs at the same time - the fix is the same isolation discipline covered in setup/teardown hooks, not a TestNG configuration setting.
- **A team tries to mix JUnit 5 and TestNG test classes in the same Maven/Gradle module and the build gets confusing fast.**
  Both frameworks can technically coexist in one module with the right plugin configuration (the Surefire/Failsafe or Gradle test task needs to know about both), but it's real ongoing complexity - usually better to pick one per module, even if different modules in a larger project use different frameworks.
- **A migration from TestNG to JUnit 5 (or vice versa) stalls specifically on tests using groups or dependsOnMethods.**
  There's no 1:1 automatic translation for dependsOnMethods - JUnit 5's philosophy discourages inter-test dependencies, so migrating those specific tests usually means restructuring them to be independent (often via shared setup) rather than finding an equivalent annotation.

### Where to check

- **`pom.xml` / `build.gradle`** — which framework (and which major version - JUnit 4 vs 5 matters a
  lot) is actually on the classpath is the first fact to confirm before assuming either framework's
  behavior applies.
- **The suite's XML config (TestNG) or `junit-platform.properties` (JUnit 5)** — where parallel
  execution settings actually live for each framework; a suite that "isn't running in parallel" is
  often just not configured to, rather than incapable of it.
- **Each framework's own current documentation, not a blog post's comparison table** — this
  comparison shifts as both frameworks release new versions; treat any specific claim ("JUnit can't do
  X") as worth re-verifying against the current docs rather than assumed permanent.
- **Whether inter-test dependencies are actually necessary** — before reaching for
  `dependsOnMethods` specifically, check whether the same effect is achievable with shared setup
  instead, which keeps tests independently runnable and easier to parallelize later.

### Worked example: a Selenium team picking a framework for a new 300-test regression suite

1. A QA team starts a new Selenium project from scratch and needs cross-browser regression tests
   (Chrome, Firefox, Edge) to finish in a reasonable CI window - sequential execution of 300 UI tests
   would take hours.
2. They evaluate JUnit 5: parallel execution is available but needs explicit configuration
   (`junit.jupiter.execution.parallel.enabled=true` plus careful thread-safety review of shared
   fixtures) to behave the way they want out of the box.
3. They evaluate TestNG: the same parallel fan-out is a native suite-XML setting
   (`parallel="methods" thread-count="4"`), and grouping smoke tests separately from the full
   regression pass is a one-line `groups` attribute away.
4. Given the team's specific need - large-scale UI automation leaning hard on exactly the features
   TestNG ships natively - they choose TestNG for this suite, while a separate, smaller internal-tools
   project on the same team stays on JUnit 5 for its plain unit tests.
5. Eighteen months later, JUnit 5's parallel support and tagging have matured further, but the
   original tradeoff that drove the decision - TestNG's more turnkey parallelism for this specific
   suite's scale - is still judged accurate on review, so the suite stays on TestNG rather than being
   migrated for its own sake.

**Quiz.** A team is starting a brand-new Selenium regression suite in 2026 and needs to decide between TestNG and JUnit 5. Based on this note, which statement best reflects honest, current guidance?

- [ ] JUnit is strictly obsolete for test automation now and TestNG should always be used instead
- [ ] TestNG is strictly obsolete now that JUnit 5 exists and should never be chosen for new projects
- [x] JUnit 5 is the safer general default, but TestNG remains a common, often-preferred choice specifically for larger Selenium suites that lean on its native parallel execution, grouping, and dependsOnMethods ordering
- [ ] The two frameworks are functionally identical in every respect, so the choice never matters

*The note's Term definition and comparison table are explicit that neither framework is simply better - JUnit 5 is the broader ecosystem default and safer general starting point, while TestNG's native parallelism, grouping, and dependsOnMethods remain genuine, still-current reasons it's commonly chosen specifically for larger Selenium/UI automation suites. Option one and option two each declare one framework categorically obsolete, which the note explicitly avoids doing for either. Option four ignores the entire comparison section detailing real, current feature differences (parallel execution defaults, dependsOnMethods, groups vs tags) that make the choice genuinely matter for a suite with TestNG's specific use case in mind.*

- **What's JUnit 5's general ecosystem position?** — The default, most widely used Java test framework - deeply integrated with Maven, Gradle, Spring Boot, and most IDEs; the safer starting choice for a new project's general unit testing.
- **What does dependsOnMethods actually do on failure?** — If the method a test depends on didn't pass, TestNG reports the dependent test as SKIPPED, not FAILED and not run at all - a deliberate distinction from an ordinary failure.
- **Has JUnit 5 closed every original gap with TestNG?** — Mostly, but not completely - @ParameterizedTest now rivals @DataProvider and @Tag rivals groups, but there's still no direct JUnit 5 equivalent to dependsOnMethods, by design philosophy rather than oversight.
- **The dual-gauge railway analogy for TestNG vs JUnit** — Two genuinely different rail gauges sharing the same corridor, solving the same transport problem with incompatible standards - picking one framework isn't picking a 'wrong' answer, it's committing to a specific standard the rest of the suite has to match.

### Challenge

Pick one real feature difference from this note - parallel execution, groups, or dependsOnMethods -
and implement the same behavior in both a scratch JUnit 5 project and a scratch TestNG project. Time
how long each takes to set up (not run), and write down, in your own words, whether the framework that
needed less configuration for that specific feature matches this note's guidance about which framework
suits which use case.

### Ask the community

> I'm choosing between TestNG and JUnit 5 for [describe your project - new Selenium suite, existing unit tests, mixed]. The specific feature I keep coming back to is [parallel execution / groups / dependsOnMethods / something else].

Naming the ONE specific feature actually driving the decision usually gets a much sharper answer than
asking "which is better" in the abstract - the honest answer nearly always depends on exactly that
kind of specific, current need.

- [TestNG — official documentation: annotations, groups, and dependencies](https://testng.org/annotations.html)
- [BrowserStack — JUnit vs TestNG: core differences](https://www.browserstack.com/guide/junit-vs-testng)

🎬 [TestNG Class 2: Differences between TestNG And Junit — Testing Tutorialspoint](https://www.youtube.com/watch?v=hWHUH4EnId0) (5 min)

- TestNG and JUnit solve the same core problem - discovering and running test methods - with different feature sets, not a strictly better-or-worse relationship.
- JUnit 5 is the broader ecosystem default and the safer general starting choice, with deep build-tool and IDE integration.
- TestNG's most durable, still-current advantages are native parallel execution, flexible grouping, and explicit dependsOnMethods ordering - all genuinely useful for large Selenium/UI automation suites.
- JUnit 5 has closed much of the original gap (parameterized tests via @ParameterizedTest, tags via @Tag), but has no direct equivalent to dependsOnMethods by design philosophy.
- This comparison shifts as both frameworks evolve - verify specific claims against each framework's current documentation rather than repeating older, possibly stale guidance.


## Related notes

- [[Notes/test-frameworks/lifecycle-and-annotations/setup-and-teardown-hooks|Setup / teardown hooks]]
- [[Notes/test-frameworks/lifecycle-and-annotations/test-annotation|@Test]]
- [[Notes/test-frameworks/lifecycle-and-annotations/pytest-fixtures|pytest fixtures]]


---
_Source: `packages/curriculum/content/notes/test-frameworks/lifecycle-and-annotations/testng-vs-junit.mdx`_
