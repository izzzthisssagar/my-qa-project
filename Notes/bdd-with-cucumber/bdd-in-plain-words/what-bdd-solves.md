---
title: "What BDD solves"
tags: ["bdd-with-cucumber", "bdd-in-plain-words", "track-d"]
updated: "2026-07-16"
---

# What BDD solves

*A business stakeholder's description, a developer's build, and a tester's test case can all quietly diverge from the same original requirement. BDD fixes this by making one shared, structured document be all three at once.*

> A product owner says "users should be able to reset a forgotten password." A developer builds a reset
> flow. A tester writes a test case. Three people, three interpretations of one sentence - and by the
> time anyone notices they didn't all mean the same thing, code has already been written against the
> wrong understanding. BDD exists specifically to catch this before a single line of code is written,
> not after.

> **In real life**
>
> A bilingual road sign says the exact same thing in Welsh and English, stacked on top of each other -
> not a rough paraphrase in each language, the identical instruction, verified to mean the same thing to
> a Welsh speaker and an English speaker alike. Nobody reading either version is left guessing whether
> the other version says something slightly different. BDD's shared specification aims for exactly that:
> one statement of behavior that a business stakeholder, a developer, and a tester all read as saying
> the same thing.

**What BDD solves**: BDD (Behavior-Driven Development) solves the problem of requirements silently diverging as they pass between a business stakeholder's intent, a developer's implementation, and a tester's verification - three different people, often with three different mental models, working from what should be one shared understanding. It does this by writing specifications as concrete, structured examples of behavior (in a shared, natural-language format like Gherkin's Given/When/Then) that all three roles read, discuss, and agree on BEFORE code is written - and which then become the literal, automatable test that verifies the behavior was actually built correctly, closing the loop instead of leaving three separate, potentially drifting interpretations.

## The specific gap BDD closes

- **The traditional path**: a requirement is written in a ticket, a developer reads and interprets it,
  a tester separately reads and interprets it, and both interpretations only get compared once
  something is already built - often the most expensive point to discover a misunderstanding.
- **The concrete-example fix**: instead of a vague sentence, BDD asks the team to work through actual,
  specific examples together *before* building anything - "what happens when the reset link is used
  twice?" "what if the email doesn't exist in the system?" - surfacing disagreements about intent
  while they're still cheap to resolve.
- **One document, three jobs**: the resulting Gherkin scenario (covered in depth next chapter) serves
  as the requirement (readable by a business stakeholder), the specification (readable by a developer
  building the feature), and the test (executable by an automation framework) - the same artifact, not
  three separate ones that can drift apart.
- **BDD is a conversation practice before it's a testing tool** - the automation is real and valuable,
  but the actual gap it closes happens earlier, in the discussion that produces the shared examples.

> **Tip**
>
> When a scenario is hard to write in Given/When/Then terms, treat that difficulty itself as useful
> information - it's often a sign the team doesn't actually agree yet on what the feature is supposed to
> do, not a sign that Gherkin is the wrong tool for this particular case.

> **Common mistake**
>
> Adopting BDD's syntax (Given/When/Then, `.feature` files) without adopting the conversation it's meant
> to capture - a developer writing scenarios alone, after the fact, to satisfy a tooling requirement.
> This produces Gherkin-shaped test scripts with none of BDD's actual value, since the shared-
> understanding conversation that would have caught a misalignment never happened.

![A bilingual Welsh-English road sign in Caernarfon showing Parcio ar gyfer canol y dref in Welsh directly above Parking for town centre in English, with parking, castle, and tree pictogram icons below, and a separate brown sign below reading Yr Hwylfan / Fun Centre](what-bdd-solves.jpg)
*Welsh bilingual road sign in Caernarfon — Wikimedia Commons, public domain (Man vyi). [Source](https://commons.wikimedia.org/wiki/File:Welsh_bilingual_road_sign_in_Caernarfon.jpg)*
- **The Welsh text — the business stakeholder's language** — One reader's native framing of the same instruction - the way a product owner naturally describes a feature, in their own terms.
- **The English text, directly below — the same message, verified** — Not a rough gist, an intentionally identical statement - the way a well-written BDD scenario is meant to say exactly the same thing to a developer that it says to the business stakeholder who helped write it.
- **The pictogram row — a THIRD shared layer, understood by everyone regardless of language** — Parking, castle, tree - symbols nobody needs either language to read correctly. This is what Given/When/Then's structure adds on top of plain prose: a shared shape, not just shared words.
- **The second sign below — a related but SEPARATE piece of information** — Not merged into the first sign, kept distinct - the same discipline good BDD scenarios need: one scenario, one behavior, not several folded together until nobody can verify any of them cleanly.

**Where a requirement silently drifts, without BDD's shared examples**

1. **A ticket says: "users should be able to reset a forgotten password"** — One sentence, genuinely open to several different interpretations.
2. **A developer builds: a reset link, valid for 24 hours, single-use** — Reasonable defaults - never explicitly discussed or confirmed with anyone else.
3. **A tester writes: a test case assuming the link never expires** — An equally reasonable, but DIFFERENT, unstated assumption.
4. **The mismatch surfaces during testing** — Now it's a bug report, a re-discussion, and rework - after the code already exists.
5. **With BDD: the 24-hour expiry is a concrete example, agreed on BEFORE any code is written** — The same disagreement, caught at its cheapest possible moment.

Catching a misunderstanding by working through concrete examples together, before building anything,
is really just: state a specific case, check whether everyone agrees on the expected outcome, and
only proceed once they do. Here's that shape as a small, generic simulation.

*Run it - surface a disagreement about a concrete example before any code exists (Python)*

```python
business_expectation = {"reset_link_expires_after_hours": None}  # never stated explicitly
developer_assumption = {"reset_link_expires_after_hours": 24}
tester_assumption = {"reset_link_expires_after_hours": None}      # assumed it never expires

def check_agreement(business, developer, tester):
    if business["reset_link_expires_after_hours"] is None:
        return "UNRESOLVED: business hasn't stated an explicit expectation yet"
    if developer["reset_link_expires_after_hours"] != tester["reset_link_expires_after_hours"]:
        return f"MISMATCH: developer assumes {developer['reset_link_expires_after_hours']}h, tester assumes {tester['reset_link_expires_after_hours']}h"
    return "AGREED"

print(check_agreement(business_expectation, developer_assumption, tester_assumption))

# After a BDD conversation, the business stakeholder states a concrete example:
business_expectation["reset_link_expires_after_hours"] = 24
developer_assumption["reset_link_expires_after_hours"] = 24
tester_assumption["reset_link_expires_after_hours"] = 24
print(check_agreement(business_expectation, developer_assumption, tester_assumption))
```

Same agreement-check shape in Java.

*Run it - surface a disagreement about a concrete example before any code exists (Java)*

```java
import java.util.*;

public class Main {
    static String checkAgreement(Integer business, Integer developer, Integer tester) {
        if (business == null) return "UNRESOLVED: business hasn't stated an explicit expectation yet";
        if (!Objects.equals(developer, tester)) {
            return "MISMATCH: developer assumes " + developer + "h, tester assumes " + tester + "h";
        }
        return "AGREED";
    }

    public static void main(String[] args) {
        Integer businessExpectation = null; // never stated explicitly
        Integer developerAssumption = 24;
        Integer testerAssumption = null; // assumed it never expires

        System.out.println(checkAgreement(businessExpectation, developerAssumption, testerAssumption));

        // After a BDD conversation, the business stakeholder states a concrete example:
        businessExpectation = 24;
        developerAssumption = 24;
        testerAssumption = 24;
        System.out.println(checkAgreement(businessExpectation, developerAssumption, testerAssumption));
    }
}
```

### Your first time: Your mission: find a real, hidden disagreement in a vague requirement

- [ ] Pick a one-sentence feature description - your own project's, or invent one ("users can filter search results by price") — Write it down exactly as a product owner might phrase it.
- [ ] Independently, write down three specific example scenarios it should cover — Include at least one edge case (an empty result set, a negative price, a tie).
- [ ] If you can, ask someone else to do the same for the identical one-sentence description — Compare your examples to theirs.
- [ ] Identify at least one place where your specific examples genuinely differ — That difference is exactly the kind of gap BDD's upfront conversation is designed to surface.

You've now experienced directly how one plain sentence hides real, specific disagreements that only
concrete examples reveal.

- **A team adopts Gherkin syntax but scenarios still don't match what actually gets built.**
  Check whether scenarios are being written collaboratively (the actual point of BDD) or by one person alone after the fact - the syntax alone doesn't create shared understanding, the conversation does.
- **Writing scenarios feels like slow, unnecessary overhead for an obviously simple feature.**
  For a feature the whole team already deeply and demonstrably agrees on, lighter-weight BDD (or skipping it) can be reasonable - the value is proportional to how much genuine ambiguity or risk exists, not a mandatory step for everything.
- **A tester and developer discover, mid-sprint, that they built/tested against different assumptions.**
  This is precisely the failure BDD's upfront example-writing conversation is meant to prevent - worth treating as a signal to start that conversation earlier for the next feature, not just fixing this one instance.
- **Business stakeholders won't participate in writing or reviewing scenarios.**
  Without their input, the 'shared' understanding is really just developer/tester alignment, missing the actual source of the requirement - worth raising directly, since this is the specific gap BDD exists to close.

### Where to check

- **The original ticket or requirement**, compared against the eventual Gherkin scenario — reveals
  how much genuine translation/interpretation happened along the way.
- **Who actually attended the scenario-writing conversation** — the real signal for whether BDD's
  shared-understanding goal was met, more than whether `.feature` files exist at all.
- **Git blame / authorship on `.feature` files** — a single author on every scenario is a sign the
  collaborative conversation may not be happening.
- **Bug reports that trace back to a misunderstood requirement** — a recurring pattern here is direct
  evidence of the exact gap BDD is meant to close.

### Worked example: a concrete example that caught a real disagreement before any code was written

1. A ticket reads: "Show a warning when a user's cart total exceeds their available store credit."
2. In a scenario-writing conversation, someone asks the concrete question: "What if the total exactly
   EQUALS the available credit - is that a warning too, or is 'exceeds' meant strictly?"
3. The product owner, developer, and tester in the room discover they'd each silently assumed a
   different answer - strictly greater-than, greater-than-or-equal, and "not sure, hadn't thought
   about it," respectively.
4. The group agrees explicitly: exactly-equal is fine, no warning; only strictly-greater triggers one.
   This becomes a concrete Given/When/Then example in the resulting scenario.
5. The edge case that would likely have surfaced as a confusing bug report two weeks later was instead
   resolved in a five-minute conversation, before a single line of code existed to be wrong.

**Quiz.** A team has fully adopted Gherkin syntax - every feature has .feature files with Given/When/Then scenarios - but developers and testers still frequently discover, mid-sprint, that they built and tested against different assumptions. What does this pattern most likely indicate?

- [ ] Gherkin syntax is fundamentally unsuited to catching requirement misunderstandings
- [x] The scenarios are likely being written by one person after the fact rather than through a genuine collaborative conversation involving business, development, and testing - the syntax alone doesn't create shared understanding without the conversation BDD is actually built around
- [ ] The team needs a different BDD tool, since Cucumber specifically must be misconfigured
- [ ] This is normal and unavoidable regardless of how BDD is practiced

*The note is explicit that BDD's real value comes from the collaborative conversation that produces shared examples BEFORE code is written - adopting the syntax without the conversation produces Gherkin-shaped scripts with none of that actual benefit, which is exactly the pattern described. Option one blames the tool for what the note attributes to missing practice. Option three invents a tooling problem not indicated by the symptom described. Option four contradicts the note's entire premise - this specific gap is exactly what BDD, practiced correctly, is meant to prevent.*

- **The specific gap BDD is designed to close** — Requirements silently diverging as they pass between a business stakeholder's intent, a developer's build, and a tester's verification - three interpretations of what should be one shared understanding.
- **What makes BDD's specification different from a plain requirement doc?** — It's written as concrete, structured examples (Given/When/Then) discussed and agreed on collaboratively BEFORE code is written, and the same document becomes the executable test.
- **Is BDD primarily a testing tool or a conversation practice?** — A conversation practice first - the automation is real and valuable, but the actual gap it closes happens in the discussion that produces shared examples, not just in running the resulting tests.
- **The most common way teams get BDD's syntax without its value** — Writing Gherkin scenarios alone, after the fact, without the collaborative conversation - producing test scripts shaped like BDD with none of the shared-understanding benefit.
- **The bilingual-sign analogy for BDD's shared specification** — The same message, verified to say the identical thing in two different readers' languages - not a rough paraphrase each side interprets separately.

### Challenge

Take a real, currently-vague requirement from your own work (or invent a plausible one). Without
consulting anyone else, write down three concrete examples of behavior it implies, including at least
one genuinely ambiguous edge case. Then find one other person, describe only the original vague
requirement to them, and ask them to independently write their own three examples. Compare - and write
one sentence on what your two sets of examples reveal that the original sentence alone didn't.

### Ask the community

> My team keeps having disagreements about what a feature is actually supposed to do, discovered mid-development. Here's a recent example: `[describe the requirement and the mismatch]`.

Describing the specific mismatch (not just "we disagreed") usually reveals whether an earlier,
concrete-example conversation would have caught it - and gives others a real case to reason about
rather than an abstract complaint.

- [Cucumber.io — official BDD documentation](https://cucumber.io/docs/bdd/)
- [Inviqa — The beginner's guide to BDD](https://inviqa.com/blog/bdd-guide)

🎬 [Understanding Behaviour-Driven Development — BDD 101 Part 1 — Matt Wynne — ConformIQ](https://www.youtube.com/watch?v=_463WlWTcdM) (15 min)

- BDD solves requirements silently diverging between a business stakeholder's intent, a developer's build, and a tester's verification - three interpretations of what should be one shared understanding.
- The fix is working through concrete, specific examples collaboratively BEFORE code is written - surfacing disagreements while they're cheapest to resolve.
- The resulting Gherkin scenario serves as requirement, specification, and executable test all at once - one artifact, not three that can drift apart.
- BDD's real value is the conversation that produces shared examples, not just the resulting syntax - scenarios written alone, after the fact, lose most of that value.
- Difficulty writing a scenario in Given/When/Then terms is often a sign the team doesn't actually agree yet on the behavior, not a sign the format is wrong.


## Related notes

- [[Notes/bdd-with-cucumber/bdd-in-plain-words/given-when-then|Given / When / Then]]
- [[Notes/bdd-with-cucumber/bdd-in-plain-words/bdd-vs-test-scripts|BDD vs test scripts]]
- [[Notes/bdd-with-cucumber/bdd-in-plain-words/the-three-amigos|The three amigos]]


---
_Source: `packages/curriculum/content/notes/bdd-with-cucumber/bdd-in-plain-words/what-bdd-solves.mdx`_
