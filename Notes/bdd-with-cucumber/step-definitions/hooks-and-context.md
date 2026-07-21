---
title: "Hooks & context"
tags: ["bdd-with-cucumber", "step-definitions", "track-d"]
updated: "2026-07-16"
---

# Hooks & context

*@Before/@After hooks run setup and teardown around every scenario (or a tagged subset like @Before('@browser')), while scenario state travels between steps via an injected shared object (Java), behave's context, or pytest-bdd fixtures - and never, by discipline, between scenarios.*

> Every scenario in the suite starts a browser, and every scenario must close it - but no `.feature`
> file says a word about browsers, because launching Chrome is plumbing, not behavior. Hooks are where
> that plumbing lives: code that runs automatically before and after every scenario (or only the tagged
> ones), invisible to the Gherkin. And between those bookends sits a second question every BDD suite
> must answer deliberately: how does the Given step's cart reach the Then step's assertion - without
> also leaking into the next scenario?

> **In real life**
>
> A level crossing barrier comes down before every train and lifts after it has passed - automatically,
> every single time. No train's timetable contains a "lower the barrier" entry; the crossing equipment
> isn't part of any train's journey, it's the machinery that makes every journey safe, triggered by the
> approach itself. And critically, the barrier resets completely between trains: no train inherits a
> half-lowered barrier from the one before it. Hooks are that crossing equipment - setup and teardown
> wrapped around every scenario without appearing in any of them - and the full reset between trains is
> exactly the isolation discipline scenario state demands.

**Hooks &amp; context**: Hooks are blocks of glue code that Cucumber runs automatically around every scenario: @Before methods before the first step, @After methods after the last (running even when the scenario failed - which makes them the reliable home for cleanup like driver.quit()). A tagged hook such as @Before('@browser') runs only for scenarios carrying that tag, so expensive setup is paid only where needed. Context is the companion problem: steps within one scenario live in separate methods (often separate classes) yet must share state. Java solves it with a shared object injected by a DI container (PicoContainer or Spring) into each step class's constructor; behave passes every step a per-scenario context object; pytest-bdd shares state through pytest fixtures. The governing discipline for both: state is scoped to ONE scenario - created fresh in setup, torn down after, never leaking into the next scenario, so every scenario passes or fails on its own.

## Around every scenario, and between its steps

```java
public class Hooks {

    private final TestContext context;   // one instance per scenario, injected

    public Hooks(TestContext context) { this.context = context; }

    @Before("@browser")                  // tagged: only scenarios tagged @browser
    public void openBrowser() {
        context.driver = new ChromeDriver();
    }

    @After("@browser")                   // runs even if the scenario failed
    public void closeBrowser(Scenario scenario) {
        if (scenario.isFailed()) {
            // capture a screenshot before quitting - the classic @After job
        }
        context.driver.quit();
    }
}
```

- **`@Before` / `@After` wrap the scenario, not the suite** - they fire around *every* scenario
  (each hook once per scenario), which is what makes them the isolation mechanism: fresh setup in,
  guaranteed cleanup out. `@After` runs even on failure, so resources can't stay leaked behind a red
  scenario. (These are `io.cucumber.java` annotations - not JUnit's identically-named ones; mixing
  the imports is a classic silent bug.)
- **Tagged hooks scope the cost** - `@Before("@browser")` runs only for scenarios tagged
  `@browser`, so API-only scenarios never pay for Chrome. Tag expressions compose
  (`@Before("@browser and not @headless")`).
- **Sharing state within a scenario - Java** - step definitions are stateless matchers, so a shared
  `TestContext` object (the "world") carries the scenario's state. A DI container - PicoContainer
  is the lightweight default, Spring for teams already on it - creates ONE instance per scenario
  and injects it into every step class and hook class that declares it in its constructor. New
  scenario, new instance, automatically.
- **Sharing state - Python** - behave hands every step the same per-scenario `context` object
  (attributes set in a Given are readable in the Then, and behave resets scenario-level attributes
  between scenarios), with `environment.py` defining `before_scenario` / `after_scenario` hooks.
  pytest-bdd uses fixtures: state is whatever fixtures the steps declare, and teardown is the
  fixture's own finalization - hooks and context collapse into one mechanism.
- **The isolation discipline** - the same rule as everywhere else in test automation: a scenario
  must not depend on, or be able to see, anything another scenario created. Scenario order can
  change, subsets run under tags, and parallel runners interleave everything - state that outlives
  its scenario turns all of that into flaking.

> **Tip**
>
> Put cleanup in `@After` hooks (or fixture finalizers), never in a scenario's final Then steps - a
> failed scenario stops at the failing step and skips everything after it, so trailing "cleanup steps"
> silently don't run exactly when things went wrong. Hooks run regardless of outcome; that guarantee
> is the whole reason they exist.

> **Common mistake**
>
> Sharing state through static fields (Java) or module-level globals (Python) because "it was easier
> than setting up dependency injection." It works - until the day two scenarios run in a different
> order, or in parallel, and one scenario reads the cart, user, or driver the previous scenario left
> behind. The resulting failures are order-dependent, unreproducible in isolation, and land on
> whichever innocent scenario ran second. Scenario state belongs in the per-scenario container the
> framework resets for you: the injected world object, behave's context, or a pytest fixture.

![A level crossing with its red-and-white barrier lowered across an empty road, a warning light on a pole at the left, white road markings in the foreground, and the fenced railway line and bare trees beyond](hooks-and-context.jpg)
*Barrier down, train imminent at St Fagans level crossing — Wikimedia Commons, CC BY-SA 2.0 (Jaggery). [Source](https://commons.wikimedia.org/wiki/File:Barrier_down,_train_imminent_at_St_Fagans_level_crossing_-_geograph.org.uk_-_3911086.jpg)*
- **The lowered barrier — the @Before hook, already run** — Down before the train arrives, every time, triggered automatically by the approach - setup that no train's own schedule mentions, exactly as no scenario's Gherkin mentions the browser starting.
- **The warning light — the trigger deciding when the equipment activates** — The crossing acts on a signal, not on every event everywhere - the way a tagged hook like @Before('@browser') fires only for the scenarios that carry its tag.
- **The empty road, cleanly held back** — Everything outside the crossing waits in a known, safe state while one train passes - one scenario running with exclusive, isolated use of its resources.
- **The railway beyond — where the actual journey happens** — The train's journey is the scenario itself: the steps. The crossing gear (hooks) makes the passage safe but is never part of the route - and it fully resets before the next train.

**One scenario's life inside its hooks**

1. **@Before('@browser') fires: a fresh driver and a fresh TestContext are created** — New scenario, new world - nothing inherited from the previous scenario.
2. **Given a logged-in user: the step stores the user on the shared context** — State starts its journey between steps - inside this one scenario only.
3. **When/Then steps read the same context and assert against it** — Different step classes, same injected per-scenario instance - that's the DI container's job.
4. **@After fires - even though the Then failed** — Screenshot captured, driver.quit() runs. Failure never leaks a browser or dirty state.
5. **The next scenario begins with its own new context** — Isolation achieved: any scenario can run first, alone, or in parallel and behave identically.

Underneath the annotations, a hook system is just a runner that wraps every scenario in the same
before/after calls and hands each one a fresh state container. Here's that machine - including the
leak the discipline exists to prevent - as a small, generic simulation.

*Run it - wrap scenarios in before/after hooks and see why fresh context matters (Python)*

```python
def before_scenario(name):
    print(f"  [hook] before: fresh context for '{name}'")
    return {}  # a brand-new, empty state container

def after_scenario(name, context):
    context.clear()
    print(f"  [hook] after: torn down '{name}' (even on failure)")

def run(scenarios, isolate=True):
    print(f"--- run with isolate={isolate} ---")
    shared = {}  # only used to demonstrate the leak
    for name, steps in scenarios:
        context = before_scenario(name) if isolate else shared
        for step in steps:
            step(context)
        status = "PASS" if context.get("ok", True) else "FAIL (leaked state!)"
        print(f"  {name}: {status}")
        if isolate:
            after_scenario(name, context)

def add_item(ctx): ctx.setdefault("cart", []).append("mug")
def assert_one_item(ctx): ctx["ok"] = len(ctx["cart"]) == 1

scenarios = [
    ("adding one item", [add_item, assert_one_item]),
    ("adding one item again", [add_item, assert_one_item]),
]

run(scenarios, isolate=True)   # each scenario gets a fresh context: both pass
run(scenarios, isolate=False)  # shared state leaks: the SECOND scenario fails
```

The same wrap-and-isolate runner in Java.

*Run it - wrap scenarios in before/after hooks and see why fresh context matters (Java)*

```java
import java.util.*;
import java.util.function.Consumer;

public class Main {
    record ScenarioDef(String name, List<Consumer<Map<String, Object>>> steps) {}

    @SuppressWarnings("unchecked")
    static List<String> cart(Map<String, Object> ctx) {
        return (List<String>) ctx.computeIfAbsent("cart", k -> new ArrayList<String>());
    }

    static void run(List<ScenarioDef> scenarios, boolean isolate) {
        System.out.println("--- run with isolate=" + isolate + " ---");
        Map<String, Object> shared = new HashMap<>(); // demonstrates the leak
        for (ScenarioDef s : scenarios) {
            Map<String, Object> ctx = isolate ? new HashMap<>() : shared;
            if (isolate) System.out.println("  [hook] before: fresh context for '" + s.name() + "'");
            for (Consumer<Map<String, Object>> step : s.steps()) step.accept(ctx);
            boolean ok = (boolean) ctx.getOrDefault("ok", true);
            System.out.println("  " + s.name() + ": " + (ok ? "PASS" : "FAIL (leaked state!)"));
            if (isolate) System.out.println("  [hook] after: torn down (even on failure)");
        }
    }

    public static void main(String[] args) {
        Consumer<Map<String, Object>> addItem = ctx -> cart(ctx).add("mug");
        Consumer<Map<String, Object>> assertOne = ctx -> ctx.put("ok", cart(ctx).size() == 1);

        List<ScenarioDef> scenarios = List.of(
            new ScenarioDef("adding one item", List.of(addItem, assertOne)),
            new ScenarioDef("adding one item again", List.of(addItem, assertOne))
        );

        run(scenarios, true);  // fresh context each time: both pass
        run(scenarios, false); // shared state leaks: the SECOND scenario fails
    }
}
```

### Your first time: Your mission: move plumbing into hooks and prove your scenarios are isolated

- [ ] Find (or imagine) a suite where every scenario's first Given is 'the browser is open' — That's plumbing in the Gherkin - the tell that a @Before hook is missing.
- [ ] Move the setup into a @Before hook and the teardown into @After, leaving the Gherkin about behavior only — Tag browser-dependent scenarios @browser and make both hooks tagged, so API scenarios skip the cost.
- [ ] Run one scenario completely alone (by tag or by line number) — A scenario that only passes as part of the full run is depending on a sibling's leftover state.
- [ ] Run the suite twice with scenario order shuffled (or in parallel if your runner supports it) — Identical results both times is the observable proof of isolation this note's discipline exists for.

You've now separated plumbing from behavior and verified - not assumed - that no scenario leans on
another's leftovers.

- **A scenario passes when run alone but fails in the full suite (or vice versa).**
  That's leaked state - some scenario's leftovers (a static field, a global, an uncleaned database row) are visible to the next. Move the state into the per-scenario container and reset the external world in @Before/@After.
- **Java hooks simply never fire, with no error at all.**
  Check the imports first - JUnit's @Before/@After compile fine but mean something else entirely; Cucumber hooks come from io.cucumber.java. Then confirm the hooks class lives inside a package the runner's glue configuration scans.
- **Browsers pile up after failed runs, even though the last step quits the driver.**
  Quitting in a step means quitting only on success - a failing scenario never reaches it. Move driver.quit() into an @After hook (or fixture finalizer), which runs regardless of the scenario's outcome.
- **Two step definition classes each see a different, half-empty version of the scenario's state.**
  Each class is holding its own private fields instead of the shared world object. Give both classes the same constructor-injected TestContext (PicoContainer/Spring) so the container hands them one instance per scenario.

### Where to check

- **The hook annotations' import lines** — `io.cucumber.java.Before` versus JUnit's `@Before` is the
  first check whenever Java hooks silently don't run.
- **Tag spelling on both sides** — the scenario's tag and the hook's tag expression
  (`@Before("@browser")`) must match exactly; a typo just means the hook quietly never fires.
- **A solo run of the failing scenario** — running it alone immediately separates "this scenario is
  broken" from "this scenario inherits another's state."
- **The DI wiring** (`cucumber-picocontainer` on the classpath, shared object in constructors) — when
  state set in one step class never appears in another, the container setup is the usual culprit.

### Worked example: the flaky suite that only failed on Tuesdays - or rather, in one specific order

1. A checkout suite is green for weeks, then a new scenario is added alphabetically before the
   others - and suddenly 'guest checkout shows an empty cart' fails in CI, but passes every time a
   developer runs it alone.
2. Investigation finds the cart page object cached in a static field: the new scenario logs a user
   in and puts two items in the cart; the guest scenario, running next, sees that same cart instance
   still holding both items.
3. The fix has two halves. First, the static field becomes a field on a TestContext object, with
   cucumber-picocontainer injecting a fresh instance into every step class per scenario.
4. Second, browser start/quit moves out of the step definitions into tagged @Before/@After hooks, so
   even a failing scenario tears its browser and state down completely.
5. The team adds a CI job that runs the suite with a shuffled scenario order - the leak that cost a
   day of debugging is now caught mechanically the moment anyone reintroduces one.

**Quiz.** A team's last step in every scenario is 'Then the browser is closed', implemented with driver.quit(). Scenarios that fail leave orphaned browsers running all over CI. Why - and what's the correct fix per this note?

- [ ] The browsers crash on their own; upgrading ChromeDriver will resolve it
- [x] A failing scenario stops at the failing step, so the trailing quit step never executes - cleanup belongs in an @After hook, which Cucumber runs whether the scenario passed or failed
- [ ] driver.quit() only works inside @Before hooks, so the call is a no-op in a Then step
- [ ] The scenarios need a second, backup quit step added after the first one

*Execution stops at a failing step and skips everything after it - so cleanup written as a final step runs only on success, which is precisely backwards. @After hooks exist because they run regardless of outcome (the note's tip makes exactly this point). Option one blames tooling for a structural sequencing problem. Option three invents a restriction that doesn't exist - quit() is an ordinary method call wherever it appears; the issue is whether the line is ever reached. Option four doubles the broken approach: a second trailing step is skipped by a failure just as reliably as the first.*

- **What do @Before and @After hooks do?** — Run setup/teardown automatically around EVERY scenario - @After even when the scenario failed - keeping plumbing (browsers, data seeding, cleanup) out of the Gherkin entirely.
- **What is a tagged hook?** — A hook with a tag expression - @Before('@browser') - that runs only for scenarios carrying that tag, so expensive setup is paid only by the scenarios that need it. Expressions compose: '@browser and not @headless'.
- **How do steps share state within one scenario in Java?** — A shared TestContext ('world') object, created once per scenario by a DI container (PicoContainer or Spring) and constructor-injected into every step and hook class.
- **How do behave and pytest-bdd share state between steps?** — behave: the per-scenario context object passed to every step. pytest-bdd: ordinary pytest fixtures declared as step parameters, with teardown via fixture finalization.
- **The scenario-isolation rule** — State lives and dies with ONE scenario: fresh in @Before, gone by @After, never in statics or globals - so any scenario can run first, alone, or in parallel with identical results.

### Challenge

Take a small BDD suite (yours or a tutorial project) and audit it for the two failure modes in this
note: (1) plumbing in the Gherkin - Given steps about browsers, databases, or test users that no
stakeholder cares about - and (2) leak paths - static fields, globals, or cleanup living in final
Then steps. Fix one of each: move the plumbing into a tagged hook, and move the leaking state into
the framework's per-scenario container. Then prove the fix by running the affected scenarios alone
and in shuffled order.

### Ask the community

> My scenario `[name]` passes alone but fails in the full run (or only fails in parallel). The state it reads is stored in `[static field / global / context / fixture]` and my hooks look like: `[describe your @Before/@After setup]`.

Naming where the state actually lives is the key detail - order-dependent failures are almost always
traced in one step once someone sees whether the container is per-scenario or accidentally shared.

- [Cucumber — official API reference (hooks and tagged hooks)](https://cucumber.io/docs/cucumber/api/)
- [Baeldung — Cucumber hooks in Java](https://www.baeldung.com/java-cucumber-hooks)

🎬 [#8 - Hooks in #Cucumber (Before/After Hooks in Cucumber) — Naveen AutomationLabs](https://www.youtube.com/watch?v=PzOZggL6ewo) (19 min)

- @Before/@After hooks wrap every scenario with automatic setup and teardown - @After runs even on failure, which is why cleanup belongs there and never in a scenario's final steps.
- Tagged hooks (@Before('@browser')) scope expensive setup to only the scenarios that carry the tag.
- Within a scenario, steps share state through a per-scenario container: a DI-injected world object in Java (PicoContainer/Spring), behave's context, or pytest-bdd fixtures.
- State must never outlive its scenario - statics and globals create order-dependent failures that land on innocent scenarios and vanish when run alone.
- The observable test of isolation: every scenario produces identical results run first, run alone, or run in parallel - and a shuffled-order CI run enforces it mechanically.


## Related notes

- [[Notes/bdd-with-cucumber/step-definitions/glue-code-java|Glue code (Java)]]
- [[Notes/bdd-with-cucumber/step-definitions/behave-and-pytest-bdd-python|behave / pytest-bdd (Python)]]
- [[Notes/bdd-with-cucumber/step-definitions/data-tables|Data tables]]


---
_Source: `packages/curriculum/content/notes/bdd-with-cucumber/step-definitions/hooks-and-context.mdx`_
