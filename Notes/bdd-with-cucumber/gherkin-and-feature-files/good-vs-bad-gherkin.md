---
title: "Good vs bad Gherkin"
tags: ["bdd-with-cucumber", "gherkin-and-feature-files", "track-d"]
updated: "2026-07-16"
---

# Good vs bad Gherkin

*Bad Gherkin is imperative click-by-click scripting, leaked implementation detail, 15-step scenarios, and vague Then assertions. Good Gherkin states behavior declaratively: plain-language intent, one behavior, a specific checkable outcome - readable by anyone who understands the feature.*

> Two scenarios verify the same login behavior. One is five lines a product owner can confirm at a
> glance. The other is nineteen lines of "When I click the #login-btn element" that breaks every time
> a CSS class is renamed - without a single actual behavior change. Both are syntactically valid
> Gherkin. Only one of them is a specification; the other is a test script that moved into a .feature
> file and brought all its furniture.

> **In real life**
>
> A cluttered workbench holds every tool the job needs - and that's exactly the problem. The pliers
> exist, somewhere under the offcuts; the right screw is in the bowl with three hundred wrong ones;
> the surface is dominated by whatever was put down last, not what matters most. Nothing is missing,
> but nothing is findable, and every job starts with archaeology. A bad Gherkin scenario reads the
> same way: the behavior is in there, buried under UI clicks, field IDs, and steps that state
> everything except what's actually being verified.

**Good vs bad Gherkin**: Good Gherkin is declarative: each step states intent and behavior in the language of the user and the business ('When the user signs in with valid credentials'), keeps one behavior per scenario, and ends in a Then naming a specific, observable outcome. Bad Gherkin is imperative and leaky: steps script UI mechanics click-by-click ('When I click the Submit button', 'When I type into the password field'), expose implementation details (element selectors, database fields, endpoint paths), sprawl to 15 or more steps because they transcribe a manual test script, and assert vaguely ('Then it works correctly') so a pass proves nothing and a failure explains nothing. The difference is not syntax - both parse - it's whether the scenario specifies WHAT the system does or scripts HOW one particular build of the UI is operated.

## The anti-patterns, each next to what good looks like

- **Imperative click-by-click vs declarative behavior.** Bad: "When I click the login link, And I
  type 'sam@example.com' into the email field, And I type 'hunter2' into the password field, And I
  click the Submit button." Good: "When Sam signs in with valid credentials." The imperative version
  scripts one build of the UI - rename a button and it breaks with zero behavior change. The
  declarative version survives any redesign that keeps the behavior, because the *how* lives in the
  step definitions, where it belongs.
- **Implementation details leaking in.** Bad: "Given user_table contains a row with status_flag=3,
  When POST /api/v2/sessions returns 200." Good: "Given a registered user with a locked account,
  When they attempt to sign in." Field names, selectors, and endpoints belong one layer down; the
  moment they appear in the scenario, the one document meant for everyone becomes readable only by
  engineers - and lies dormant when the schema changes.
- **Test-script-length scenarios.** A scenario with 15 or more steps is almost always a manual test
  script transcribed line by line - three or four behaviors folded together with all their setup
  inline. Good Gherkin pushes shared setup into a Background or a single summarizing Given ("Given
  Sam has a paid order awaiting dispatch") and gives each behavior its own scenario. Most good
  scenarios fit in three to six steps.
- **Vague Then assertions.** Bad: "Then the page should load correctly," "Then it should work as
  expected." Correctly according to what? A Then that can't fail informatively can't pass
  meaningfully either. Good: "Then the order status should be 'Dispatched'," "Then Sam should see 1
  item in the cart" - a specific, observable fact someone could check by eye.

> **Tip**
>
> Apply the redesign test to every step: if the UI were rebuilt tomorrow - same behavior, different
> buttons - which steps would survive? Steps that describe intent ("signs in", "adds the mug to the
> cart") survive; steps that describe mechanics ("clicks #submit-btn", "scrolls to the footer") die in
> the redesign. Write the survivors into the scenario and push the mechanics down into step
> definitions.

> **Common mistake**
>
> Reviewing Gherkin for syntax instead of audience. A scenario can parse perfectly, follow
> Given/When/Then order, and still be bad Gherkin because a product owner couldn't confirm it matches
> their intent - the review question isn't "is this valid?" but "could the least technical person who
> understands this feature read it and say 'yes, that's what it should do'?" Valid-but-unreadable
> scenarios are how feature files quietly stop being specifications.

![A cluttered workbench in a dim rustic workshop with a bowl full of mixed bolts and fasteners at the center, hand tools buried under offcuts and containers, a red power tool lying on top of the pile on the right, and a bright window above the bench](good-vs-bad-gherkin.jpg)
*Cluttered workbench in a rustic workshop — Wikimedia Commons, CC BY 2.0 (Shixart1985). [Source](https://commons.wikimedia.org/wiki/File:Cluttered_workbench_in_a_rustic_workshop_filled_with_tools_and_materials.jpg)*
- **The bowl of mixed fasteners — an 18-step scenario** — Every screw the job needs is in there, along with hundreds that aren't - the way a transcribed test script contains the behavior somewhere among its click-by-click steps, at the cost of finding it.
- **The power tool sprawled on top — implementation detail dominating** — The loudest thing on the bench is a tool, not the work - like a scenario whose most prominent lines are selectors, field names, and endpoints instead of the behavior they serve.
- **The pliers buried in the pile — the actual behavior, in there somewhere** — What you came for exists but takes archaeology to reach - a vague 'Then it works correctly' leaves the real expected outcome exactly this findable.
- **The window — the light was never the problem** — There's plenty of light to work by; the bench is unusable anyway. Valid syntax is that light: a scenario can parse perfectly and still be this bench.

**A transcribed test script becoming a specification**

1. **A 19-step scenario arrives in review** — Clicks, field IDs, scrolls - a manual test script pasted into Gherkin.
2. **The reviewer asks: what behavior is this verifying?** — The answer takes three read-throughs: successful login, and maybe cart persistence.
3. **Mechanics get pushed down into step definitions** — 'Click, type, type, click' becomes 'When Sam signs in with valid credentials'.
4. **The second behavior gets its own scenario** — Cart persistence was hiding in steps 12 through 19 - now it's independently named and reported.
5. **Two five-line scenarios replace the script** — A product owner confirms both at a glance - and a UI redesign no longer breaks either.

Telling good Gherkin from bad is a reviewable, almost mechanical judgment: count the steps, spot the
mechanics words, catch the vague assertions. Here's that reviewer's eye as a small, generic
simulation.

*Run it - a reviewer's checklist over two versions of the same scenario (Python)*

```python
IMPERATIVE_WORDS = ["click", "type", "scroll", "navigate", "press"]
VAGUE_ASSERTIONS = ["correctly", "properly", "as expected", "works"]

scenarios = {
    "Login works": [
        "I click the login link",
        "I type sam@example.com into the email field",
        "I type the password into the password field",
        "I click the Submit button",
        "the page should load correctly",
    ],
    "Registered user signs in successfully": [
        "Sam is a registered user",
        "Sam signs in with valid credentials",
        "Sam should see her account dashboard",
    ],
}

def review(name, steps):
    findings = []
    if len(steps) > 8:
        findings.append(f"{len(steps)} steps - likely a transcribed test script")
    for step in steps:
        lowered = step.lower()
        if any(w in lowered for w in IMPERATIVE_WORDS):
            findings.append(f"imperative mechanics: '{step}'")
        if any(v in lowered for v in VAGUE_ASSERTIONS):
            findings.append(f"vague assertion: '{step}'")
    verdict = "NEEDS REWRITE" if findings else "READS AS A SPECIFICATION"
    print(f"Scenario: {name} -> {verdict}")
    for f in findings:
        print(f"  - {f}")

for name, steps in scenarios.items():
    review(name, steps)
```

Same reviewer's checklist in Java.

*Run it - a reviewer's checklist over two versions of the same scenario (Java)*

```java
import java.util.*;

public class Main {
    static final List<String> IMPERATIVE = List.of("click", "type", "scroll", "navigate", "press");
    static final List<String> VAGUE = List.of("correctly", "properly", "as expected", "works");

    static void review(String name, List<String> steps) {
        List<String> findings = new ArrayList<>();
        if (steps.size() > 8) {
            findings.add(steps.size() + " steps - likely a transcribed test script");
        }
        for (String step : steps) {
            String lowered = step.toLowerCase();
            if (IMPERATIVE.stream().anyMatch(lowered::contains)) {
                findings.add("imperative mechanics: '" + step + "'");
            }
            if (VAGUE.stream().anyMatch(lowered::contains)) {
                findings.add("vague assertion: '" + step + "'");
            }
        }
        System.out.println("Scenario: " + name + " -> "
            + (findings.isEmpty() ? "READS AS A SPECIFICATION" : "NEEDS REWRITE"));
        for (String f : findings) {
            System.out.println("  - " + f);
        }
    }

    public static void main(String[] args) {
        review("Login works", List.of(
            "I click the login link",
            "I type sam@example.com into the email field",
            "I type the password into the password field",
            "I click the Submit button",
            "the page should load correctly"));

        review("Registered user signs in successfully", List.of(
            "Sam is a registered user",
            "Sam signs in with valid credentials",
            "Sam should see her account dashboard"));
    }
}
```

### Your first time: Your mission: take one bad scenario through a full declarative rewrite

- [ ] Write (or find) a deliberately bad scenario: 12 or more steps, clicks and field names, ending in 'Then it should work correctly' — Transcribing how you'd manually test a login or checkout produces one naturally.
- [ ] Underline every step that would survive a full UI redesign with identical behavior — Expect two or three survivors - those are the intent; everything else is mechanics.
- [ ] Rewrite using only the survivors, in plain language, with a Then naming one specific observable outcome — Aim for three to six steps; push every click and selector down to where step definitions would live.
- [ ] Show both versions to someone else and ask which one they could confirm matches the feature's intent — If they still can't confirm the rewrite, the leak isn't gone yet - iterate once more.

You've now performed the exact transformation that separates a specification from a transcribed test
script - and you have a before/after pair to show for it.

- **Scenarios break en masse after every UI change, even when behavior didn't change.**
  That's the signature of imperative Gherkin - steps script the old UI's mechanics. Rewrite steps to state intent and move selectors/clicks into step definitions, so only real behavior changes touch the .feature files.
- **A scenario passes but the feature is visibly broken.**
  Look at the Then: vague assertions ('loads correctly', 'works as expected') pass as long as nothing throws. Replace them with a specific observable fact - a value, a status, a visible message - that would actually have caught this.
- **Product owners stopped reading the feature files months ago.**
  Sample a few scenarios and count implementation words (selectors, field names, endpoints) - once those leak in, non-technical readers rationally give up. De-leak the language before trying to re-engage the readers.
- **Nobody can tell what a 20-step scenario actually verifies, including its author.**
  List the distinct actions it performs - each one is probably a folded-in behavior. Split by behavior, compress each one's setup into a summarizing Given, and let the scenario names carry what the steps used to hide.

### Where to check

- **Step wording for mechanics verbs** — click, type, scroll, navigate, press are the fastest grep
  for imperative Gherkin in a feature directory.
- **Then steps for vague adverbs** — "correctly," "properly," "as expected" mark assertions that
  can't fail informatively.
- **Step counts per scenario** — anything at 15 or more steps is a transcribed script until proven
  otherwise; most good scenarios fit in three to six.
- **The git history of .feature files after UI redesigns** — mass scenario edits with no behavior
  change are hard evidence the scenarios script mechanics rather than specify behavior.

### Worked example: a checkout scenario rescued from nineteen steps of click-by-click scripting

1. A reviewer opens a scenario called "Checkout test": nineteen steps, beginning "When I click the
   cart icon, And I click the checkout button, And I type '4111...' into the card number field" and
   ending "Then everything should work correctly."
2. She applies the redesign test - which steps survive a UI rebuild? Three do: a user with an item
   in the cart, paying with a valid card, and an order confirmation appearing. Everything else is
   mechanics scripting the current build.
3. She also finds a second behavior hiding in steps 14 through 19: the confirmation email. It's been
   silently untested for months, because the scenario always failed earlier, on a renamed button,
   before reaching those steps.
4. The rewrite: "Given Sam has a Blue Mug in her cart, When she pays with a valid card, Then her
   order should be confirmed with order status 'Paid'" - plus a second, separate scenario for the
   confirmation email. The clicks and selectors move into step definitions.
5. The next UI redesign changes dozens of selectors and zero .feature files. The email scenario -
   now actually reachable - fails the following week and catches a real regression the old
   nineteen-step version would have masked.

**Quiz.** A scenario reads: 'When I click the #promo-input field, And I type SAVE10, And I click Apply, Then the page updates correctly.' Which rewrite best fixes BOTH anti-patterns it contains, according to this note?

- [ ] When I click the #promo-input field, And I type SAVE10, And I click Apply, Then the total should be $90 - keep the steps, sharpen the assertion
- [ ] When the user applies the promo code SAVE10, Then the page updates correctly - declarative action, same assertion
- [x] When the user applies the promo code SAVE10, Then the order total should be reduced to $90 - declarative action AND a specific observable outcome
- [ ] Then applying promo code SAVE10 should work as expected on all pages - one step is simpler than four

*The scenario has two distinct problems - imperative click-by-click mechanics and a vague Then - and option three fixes both: intent-level action wording that survives a redesign, plus an assertion naming a specific checkable fact. Option one keeps the mechanics, so every UI rename still breaks the scenario despite the better assertion. Option two fixes the action but keeps 'updates correctly', which can't fail informatively. Option four makes things worse: it collapses action and assertion into one vaguer step and adds an untestable 'all pages' claim.*

- **Imperative vs declarative Gherkin** — Imperative scripts UI mechanics ('click the Submit button') and breaks on any redesign; declarative states intent ('signs in with valid credentials') and survives any rebuild that keeps the behavior. Mechanics belong in step definitions.
- **The redesign test for a Gherkin step** — If the UI were rebuilt tomorrow with identical behavior, would this step still make sense? Intent-level steps survive; mechanics-level steps die - write the survivors, push the rest down a layer.
- **Why is a 15-step scenario a red flag?** — It's almost always a transcribed manual test script: several behaviors folded together with inline setup. Split by behavior, compress setup into a summarizing Given - good scenarios usually run three to six steps.
- **What's wrong with 'Then it should work correctly'?** — It can't fail informatively, so it can't pass meaningfully - nothing observable is named. A good Then states a specific checkable fact: a value, a status, a visible message.
- **The real review question for a Gherkin scenario** — Not 'is the syntax valid?' but 'could the least technical person who understands this feature read it and confirm that's what it should do?' - valid-but-unreadable is still bad Gherkin.

### Challenge

Run a mechanics audit on a real feature directory (yours or an open-source project's): grep the
.feature files for click, type, scroll, press, and the vague trio "correctly", "properly", "as
expected", and count steps per scenario. Pick the single worst offender, rewrite it declaratively
using the redesign test, and record the before/after step counts plus one sentence on what the
rewrite revealed - a hidden second behavior, an untestable assertion, or a leak that had locked
non-technical readers out.

### Ask the community

> Is this scenario too imperative, or is this level of UI detail justified here? `[paste the scenario]` - context: `[what the feature does and who reads the file]`.

Pasting the actual scenario matters - the imperative/declarative boundary is obvious to a second
reader within seconds, and the interesting discussion is usually about which layer the mechanics
should move down to.

- [Cucumber — Writing better Gherkin](https://cucumber.io/docs/bdd/better-gherkin/)
- [Automation Panda — BDD 101: Writing Good Gherkin](https://automationpanda.com/2017/01/30/bdd-101-writing-good-gherkin/)

🎬 [Cucumber BDD Best Practices — The-Ohayo-Dev](https://www.youtube.com/watch?v=nrggIRWK6qo) (35 min)

- Good Gherkin is declarative: steps state user-level intent, and the click-by-click mechanics live in step definitions, so redesigns don't break specifications.
- Implementation details (selectors, field names, endpoints) leaking into scenarios lock out non-technical readers and break the file when internals change.
- A 15-plus-step scenario is a transcribed test script: split it by behavior and compress setup into a summarizing Given - three to six steps is the healthy range.
- A Then must name a specific observable outcome; 'works correctly' can't fail informatively and therefore can't pass meaningfully.
- Review scenarios for audience, not syntax: the test is whether the least technical person who understands the feature could read it and confirm the intent.


## Related notes

- [[Notes/bdd-with-cucumber/gherkin-and-feature-files/writing-scenarios|Writing scenarios]]
- [[Notes/bdd-with-cucumber/gherkin-and-feature-files/scenario-outlines-and-examples|Scenario outlines & examples]]
- [[Notes/bdd-with-cucumber/gherkin-and-feature-files/backgrounds-and-tags|Backgrounds & tags]]


---
_Source: `packages/curriculum/content/notes/bdd-with-cucumber/gherkin-and-feature-files/good-vs-bad-gherkin.mdx`_
