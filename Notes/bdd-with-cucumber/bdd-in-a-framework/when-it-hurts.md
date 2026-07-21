---
title: "When it hurts"
tags: ["bdd-with-cucumber", "bdd-in-a-framework", "track-d"]
updated: "2026-07-16"
---

# When it hurts

*The honest counter-case: for a solo developer, purely technical logic, a throwaway prototype, or a team doing syntax without collaboration, BDD's scenario meetings, glue layer, and indirection are pure cost - a plain test would be faster to write, read, and debug.*

> This module has spent three chapters building up Cucumber - so here's the note that would get cut
> from a sales deck. There are common, ordinary situations where BDD makes a team strictly worse off:
> slower to write tests, slower to debug them, with a glue layer to maintain that translates between
> two audiences who turn out to be the same person. Knowing these situations is not disloyalty to
> BDD - it's the difference between an engineer who chose a tool and one who inherited a habit.

> **In real life**
>
> On a riverside walking path stands a properly-built wooden kissing gate - good timber, correct
> construction, real craftsmanship. And it's pointless: the main gate beside it is missing, so the
> fence line is just open, and every walker strolls straight past the carefully-made mechanism
> without touching it. Nothing is wrong with the gate itself. It's wrong for the spot: all the cost
> of building and maintaining a gate, in a place where nothing needed gating. BDD in the wrong
> conditions is exactly this - well-constructed Gherkin, glue code, and reports, standing beside a
> wide-open path where no communication gap ever needed closing.

**When BDD hurts**: BDD hurts - meaning its overhead is paid in full while its benefits never arrive - in identifiable situations that are the mirror image of the previous note's conditions. A solo developer or tiny co-located team has no communication gap for a shared specification to close: they'd be writing plain-language translations for themselves. Pure technical or internal logic (parsers, caches, retry policies) has no business reader: no stakeholder will ever review those scenarios, so the natural-language layer serves nobody. Throwaway prototypes and short-lived code cancel the living-documentation dividend, which only compounds over time the code doesn't have. And a team that adopts Gherkin syntax without the collaborative practice - scenarios written by one engineer, after the code, reviewed by no stakeholder - pays the steepest version: full glue-code and indirection cost, zero shared-understanding benefit. In all four cases the same test coverage was available from a plain test framework at a fraction of the writing, reading, and debugging cost.

## The four situations where the overhead buys nothing

- **A solo developer or tiny team** — BDD's core product is shared understanding across different
  roles. One person (or three people at one whiteboard, shipping daily) already has it. Writing
  "Given a logged-in user" so that a step definition can call the code you wrote an hour ago is
  translating for an audience of yourself - the meeting BDD replaces never needed to happen.
- **Pure technical / internal logic** — no product owner will ever read "Given the LRU cache
  contains 512 entries, When entry 513 is inserted..." - and per Chapter 1's bdd-vs-test-scripts
  note, they shouldn't have to. Behavior with no non-technical audience gains nothing from a
  natural-language layer; a well-named unit test states it more precisely for the only readers it
  will ever have.
- **Throwaway prototypes and short-lived code** — living documentation is an annuity, and
  short-lived code dies before the first payment. A hackathon demo or an A/B-test variant that
  ships and gets deleted in six weeks collects the full setup cost (feature files, glue, runner
  config) and none of the compounding return.
- **Syntax without the collaborative practice** — the most expensive failure mode, because it looks
  like success. Scenarios written alone, after the code, reviewed by no stakeholder (the pattern
  Chapter 1 dissected) keep every cost - Gherkin's indirection, regex/expression matching, a glue
  layer between a failure and its cause - while the one benefit that justifies those costs, the
  alignment conversation, never happens. The team ends up debugging through three files to fix
  what a ten-line JUnit test would have shown in one.

> **Tip**
>
> A fast litmus test before writing a `.feature` file: name the specific non-engineer who will read
> these scenarios, and the specific decision they'll make from them. A name and a decision - not a
> role that theoretically could. If you can't produce both, write a plain test; you can always
> promote the behavior to a scenario later, the day a real reader appears.

> **Common mistake**
>
> Concluding "we tried BDD and it doesn't work" after paying its costs in exactly these no-payoff
> conditions - a solo-maintained internal service, scenarios nobody non-technical ever saw. That
> verdict then blocks BDD later, on the rule-dense cross-team feature where it would have earned its
> keep. The honest conclusion is narrower and more useful: BDD was the wrong tool for THAT spot -
> misdiagnosing "wrong conditions" as "bad tool" is itself a costly error, in both directions.

![A well-built wooden kissing gate standing beside a riverside footpath where the main gate is missing, so the worn path simply runs straight past the carefully-constructed gate mechanism](when-it-hurts.jpg)
*A somewhat pointless 'kissing gate' on the Stour Valley Walk — Wikimedia Commons, CC BY-SA 2.0 (Nick Smith). [Source](https://commons.wikimedia.org/wiki/File:A_somewhat_pointless_%27kissing_gate%27_on_the_Stour_Valley_Walk_-_geograph.org.uk_-_783043.jpg)*
- **The kissing gate itself — genuinely well-made, and serving nothing** — Nothing is wrong with the construction. Well-formatted Gherkin and clean glue code can be equally well-made and equally functionless - quality of execution can't rescue a tool from the wrong conditions.
- **The worn path running straight past it — the route everyone actually takes** — Walkers don't use the mechanism because nothing requires them to. A solo developer 'walks straight past' their own scenarios the same way: the shared-understanding gate was never needed on this path.
- **The gap where the main gate should be — the missing piece that made this pointless** — A kissing gate only works as part of a fence line; alone, it's furniture. Gherkin syntax only works as part of the collaborative practice - without the conversation, the .feature files are the same furniture.
- **The fence posts trailing off into the bushes — the maintenance that continues anyway** — Someone still owns this structure - it weathers, it's checked, it's repaired. Unread scenarios and their glue code age the same way: the maintenance bill arrives on schedule whether or not anyone benefits.

**The same bug, found through two different test stacks**

1. **A solo developer's internal parser has an off-by-one bug** — Purely technical logic, one maintainer, no business reader anywhere in sight.
2. **Path A - the plain unit test fails** — The IDE points at the assertion and the input that broke. One file. Fix takes minutes.
3. **Path B - the Cucumber scenario fails** — Read the Gherkin step, find the matching step-definition expression, follow the glue into the helper - three files before reaching the same assertion.
4. **Both paths find the identical bug** — Coverage was never the difference. The difference was the indirection tax - paid on every single failure, forever.
5. **What Path B bought for that tax: nothing** — No stakeholder read the scenario; no conversation was held; no ambiguity existed. Full cost, zero benefit - the definition of the wrong conditions.

Weighing a tool's fixed overhead against benefits that may be absent - instead of assuming benefits
always arrive - is really just: count what each path costs, count who actually collects the
benefit, and subtract. Here's that shape as a small, generic simulation.

*Run it - the indirection tax with and without a reader who benefits (Python)*

```python
# Cost model: files touched to diagnose one failure, and who reads the spec layer
test_stacks = [
    {"name": "plain unit test",       "files_per_failure": 1, "spec_layer_readers": 0},
    {"name": "cucumber + glue layer", "files_per_failure": 3, "spec_layer_readers": 0},  # solo dev: no reader
    {"name": "cucumber + glue layer", "files_per_failure": 3, "spec_layer_readers": 4},  # cross-team feature
]

def verdict(stack):
    indirection_tax = stack["files_per_failure"] - 1  # every file past the first is pure overhead
    benefit = stack["spec_layer_readers"] * 2          # value scales with real readers
    net = benefit - indirection_tax
    label = "worth it" if net > 0 else "pure cost - a plain test was strictly better"
    return f"tax={indirection_tax} benefit={benefit} net={net:+} -> {label}"

for stack in test_stacks:
    print(f"{stack['name']:<24} readers={stack['spec_layer_readers']}  {verdict(stack)}")
```

Same cost-benefit subtraction in Java.

*Run it - the indirection tax with and without a reader who benefits (Java)*

```java
import java.util.*;

public class Main {
    record Stack(String name, int filesPerFailure, int specLayerReaders) {}

    static String verdict(Stack s) {
        int indirectionTax = s.filesPerFailure() - 1; // every file past the first is pure overhead
        int benefit = s.specLayerReaders() * 2;       // value scales with real readers
        int net = benefit - indirectionTax;
        String label = net > 0 ? "worth it" : "pure cost - a plain test was strictly better";
        return "tax=" + indirectionTax + " benefit=" + benefit + " net=" + net + " -> " + label;
    }

    public static void main(String[] args) {
        List<Stack> stacks = List.of(
            new Stack("plain unit test", 1, 0),
            new Stack("cucumber + glue layer (solo dev)", 3, 0),
            new Stack("cucumber + glue layer (cross-team)", 3, 4)
        );
        for (Stack s : stacks) {
            System.out.println(s.name() + " readers=" + s.specLayerReaders() + "  " + verdict(s));
        }
    }
}
```

### Your first time: Your mission: feel the indirection tax on a failure you cause yourself

- [ ] Take any working Cucumber project (an example repo is fine) and break one assertion deliberately — Change an expected value in a step definition or the code under test - anywhere downstream of the Gherkin.
- [ ] Starting ONLY from the failed scenario output, time how long it takes to reach the broken line — Count every file you open on the way: feature file, step definitions, page object or helper, the code itself.
- [ ] Now write the equivalent check as a plain unit test, break it the same way, and time the diagnosis again — Note the file count this time - typically one.
- [ ] Write one sentence: what would have to be true for the extra files and minutes to be worth paying on every future failure? — Your answer should sound like the previous note's four conditions - if it doesn't, you've just derived this note's thesis yourself.

The indirection tax is easy to dismiss in the abstract and impossible to dismiss after you've paid
it with a stopwatch running.

- **Test-writing velocity dropped sharply after mandating Cucumber for all new tests.**
  Audit which tests actually have a non-technical audience. Migrating the purely-technical majority back to plain unit/integration tests typically recovers most of the loss - and makes the remaining, genuinely-shared scenarios more credible, not less.
- **Debugging any failure means bouncing between feature files, step definitions, and helpers before reaching real code.**
  That's the indirection tax, and it's only justified if someone non-technical is collecting the readable-spec benefit. If no such reader exists, the honest fix is removing the layer, not getting faster at traversing it.
- **A repo's .feature files were all written by one engineer, all after the code, and no stakeholder has ever opened them.**
  This is syntax-without-practice - full Gherkin cost for zero collaborative benefit. Either start the actual practice (invite stakeholders, write scenarios before code, per Chapter 1) or drop to plain tests; the current middle state is the worst of both.
- **A prototype's test setup (runner config, glue scaffolding, feature files) took longer than the prototype.**
  Match the harness to the code's life expectancy: throwaway code earns a handful of plain tests around whatever must not break during the demo. If the prototype graduates to a real product, that's the moment BDD's conditions may appear - decide again then.

### Where to check

- **Feature-file authorship and access logs** — one engineer writing every scenario, and zero
  non-engineer views of reports, are the two most direct signals the shared layer serves nobody.
- **Time-to-diagnose on recent failures** — how many files sit between a red scenario and its cause,
  versus the same measurement on the team's plain tests.
- **The scenarios' actual vocabulary** — cache sizes, byte sequences, and internal flags in Gherkin
  mean the content never had a business audience, whatever the format claims.
- **The code's expected lifetime** — a deprecation date, an A/B-test end date, or a 'prototype'
  label next to a full BDD harness is the mismatch this note describes.

### Worked example: the team that un-adopted Cucumber and got faster - honestly

1. A two-person platform team maintains internal build tooling: config parsers, artifact caching,
   retry logic. A year earlier, a company-wide mandate put all their tests in Cucumber.
2. Their reality check: 140 scenarios, every one written by whichever of the two wrote the code,
   after writing it. The published reports have no views from outside the team. Steps read like
   "Given the manifest cache contains 3 stale entries" - because that IS the domain; there is no
   business-language version of a manifest cache.
3. They measure a sprint of failures: median four file-hops from red scenario to broken line, and
   two genuine bugs where the failure was in step-definition glue, not in the tooling itself -
   tests failing on translation, not on behavior.
4. They migrate to plain JUnit over three weeks: the 140 scenarios become 90 tighter unit tests
   plus a dozen integration tests. Test-suite maintenance time drops by roughly a third; the glue
   package is deleted outright.
5. The postmortem's key sentence, worth quoting: "Nothing was wrong with Cucumber. There was no
   conversation to capture, so we were maintaining a translation layer between us and ourselves."

**Quiz.** A solo developer maintains an internal log-parsing service nobody else touches. Their tests are Cucumber scenarios they write themselves after each change; no one else has ever read them. They ask whether to keep the BDD setup. Per this note, what's the honest recommendation?

- [ ] Keep it - BDD scenarios always improve quality regardless of team size or audience
- [x] Drop to plain unit tests - with no communication gap to close, no business reader, and no collaborative conversation, the Gherkin layer is pure indirection cost; identical coverage is available with faster writing and one-file debugging
- [ ] Keep it, but hire a business analyst so someone can read the scenarios
- [ ] Drop all automated testing, since the BDD suite was wasted effort anyway

*This case hits three of the note's four no-payoff situations at once: solo maintainer, purely technical domain, syntax without any collaborative practice - so every BDD cost is being paid while the sole benefit (shared understanding across roles) has no one to accrue to. Option one is exactly the unconditional cheerleading this note exists to correct; BDD's value is conditional on audience and ambiguity. Option three inverts the reasoning absurdly - hiring a reader to justify a format serves the tool, not the product. Option four confuses the layer being questioned: the TESTS are valuable and stay; it's the natural-language translation layer on top of them that isn't earning its cost.*

- **The four situations where BDD's overhead buys nothing** — A solo dev or tiny team (no communication gap); pure technical/internal logic (no business reader); throwaway or short-lived code (no time for living docs to compound); syntax adopted without the collaborative practice (all cost, no conversation).
- **What is the 'indirection tax'?** — The extra hops every failure costs in a Cucumber stack - Gherkin step to step-definition expression to glue to real code - paid on every diagnosis, justified only when someone actually collects the readable-spec benefit.
- **Why is 'syntax without the practice' the most expensive failure mode?** — It keeps every cost (glue layer, expression matching, indirection) while skipping the one benefit that justifies them - the alignment conversation - and it looks like success, so it persists.
- **What's wrong with concluding 'BDD doesn't work' after a bad fit?** — It misdiagnoses wrong CONDITIONS as a bad TOOL - blocking BDD later on the ambiguous, cross-team, long-lived feature where it would genuinely pay off.
- **The pointless-kissing-gate analogy for BDD in the wrong conditions** — A well-built gate beside a missing fence: nothing wrong with the construction, everything wrong with the placement - everyone walks straight past it while the maintenance bill continues.

### Challenge

Audit a real Cucumber suite (yours, your team's, or an open-source project's) against this note's
four situations: check feature-file authorship, look for technical vocabulary in the Gherkin, find
any evidence a non-engineer reads the scenarios or reports, and note the code's expected lifetime.
Write a three-sentence verdict: which scenarios are earning their indirection cost, which would be
better as plain tests, and - the hard part - what specifically would have to change for the second
group to justify staying as Gherkin.

### Ask the community

> I think my team is paying BDD's costs without its benefits: `[describe your situation - team size, who reads the scenarios, what the code is]`. Before I propose dropping it, what am I missing?

Asking "what am I missing?" before proposing removal matters - responders who've un-adopted
Cucumber can flag the real costs of migrating back (rewriting suites, retraining, political
capital), which are part of the honest math too.

- [Cucumber — official blog: Cucumber anti-patterns (part one)](https://cucumber.io/blog/bdd/cucumber-antipatterns-part-one/)
- [ThinkCode — Cucumber anti-patterns (Malmqvist's field notes)](https://www.thinkcode.se/blog/2016/06/22/cucumber-antipatterns)

🎬 [The TRUTH About Cucumber & Behavior Driven Development (BDD) — Modern Software Engineering](https://www.youtube.com/watch?v=YUkk2lGLxjA) (13 min)

- BDD makes teams strictly worse off in ordinary, common situations: solo devs, purely technical logic, throwaway code, and syntax adopted without the collaborative practice.
- The indirection tax is paid on every failure - multiple file-hops from red scenario to broken line - and is only justified when someone real collects the readable-spec benefit.
- No communication gap means nothing to close: a solo developer writing Gherkin is maintaining a translation layer between themselves and themselves.
- Living documentation is an annuity that short-lived code never collects on - match the harness to the code's life expectancy.
- The honest verdict after a bad fit is 'wrong conditions,' not 'bad tool' - misdiagnosing that blocks BDD where it would genuinely pay, and cheerleading blocks plain tests where THEY would.


## Related notes

- [[Notes/bdd-with-cucumber/bdd-in-a-framework/cucumber-and-selenium|Cucumber + Selenium]]
- [[Notes/bdd-with-cucumber/bdd-in-a-framework/reports-and-living-documentation|Reports & living documentation]]
- [[Notes/bdd-with-cucumber/bdd-in-a-framework/when-bdd-helps|When BDD helps]]


---
_Source: `packages/curriculum/content/notes/bdd-with-cucumber/bdd-in-a-framework/when-it-hurts.mdx`_
