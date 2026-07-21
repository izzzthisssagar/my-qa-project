---
title: "WCAG 2.2 A / AA / AAA"
tags: ["accessibility-testing", "why-accessibility-matters", "track-c"]
updated: "2026-07-20"
---

# WCAG 2.2 A / AA / AAA

*WCAG 2.2, the current W3C accessibility standard, defines three conformance levels - A, AA, and AAA - each stricter than and inclusive of the one before it. AA is the common legal and contractual bar; AAA is a genuine stretch goal, rarely required site-wide.*

> "Is it accessible" is not a yes-or-no question with one right answer - WCAG 2.2 answers it with three
> ordered levels instead, because a product can genuinely clear a real bar without clearing every bar
> that exists.

> **In real life**
>
> A gold, silver, and bronze medal from the same event are not three different competitions - they are
> three genuine, ordered results in the identical event, each one a real accomplishment, each one stricter
> than the last. Nobody hands out a bronze medal for showing up. WCAG's three conformance levels work the
> same way: Level A is not a participation ribbon, it is a real, checkable bar - AA and AAA simply raise
> that same bar further, on the same criteria, for the same underlying goal.

**WCAG conformance levels**: WCAG 2.2 is the current W3C Web Content Accessibility Guidelines standard. It organizes testable success criteria into three conformance levels - A, AA, and AAA - where each level is cumulative: meeting Level AA requires meeting every Level A criterion as well, and meeting Level AAA requires meeting every Level A and Level AA criterion too. Level AA is the level most commonly cited in law, contracts, and procurement policy.

## Three levels, each one cumulative

- **Level A** - the floor. Criteria at this level address barriers so severe that some users cannot
  access content at all without them being met - this is not an optional starting point, it is the
  minimum real bar.
- **Level AA** - the common target. Everything in Level A, plus additional criteria that address
  barriers affecting a wider range of users under ordinary conditions. This is the level most laws,
  contracts, and internal policies actually require.
- **Level AAA** - the stretch goal. Everything in Level A and AA, plus the strictest additional
  criteria. The W3C itself notes it is not recommended as a general site-wide requirement, because some
  AAA criteria cannot be satisfied for all content types no matter how well a team executes.
- **Cumulative by design.** A product cannot claim Level AA while failing a Level A criterion - AA is
  defined as including A, not sitting beside it.

## Level AA is the practical answer to "which one do we target"

Nearly every legal and contractual reference to WCAG - policy language, procurement requirements,
audit contracts - points to Level AA specifically. That makes it the default, evidence-based target for
most products, with AAA reserved for content types or user populations where a team has a specific,
deliberate reason to go further.

> **Tip**
>
> When someone asks "are we WCAG compliant," ask back "at which level, and is that a false claim if even
> one Level A criterion is failing somewhere on the site." Conformance is normally scoped to a defined set
> of pages or flows, not asserted as a blanket, unqualified claim about an entire product.

> **Common mistake**
>
> Assuming Level AAA is always the "best practice" target to aim for everywhere. The W3C's own guidance
> is that AAA is not recommended as a general requirement for entire sites, since some AAA criteria are
> not achievable for every kind of content - treating it as a default target can create false promises
> instead of genuine improvement.

![A Paralympic athlete wearing gold, silver, and bronze medals from the Sydney 2000 Games, holding a small open box with a diamond pin](wcag-2-2-a-aa-aaa.jpg)
*291000 - Paralympic gold silver bronze medals - 2000 Sydney medal photo — Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:291000_-_Paralympic_gold_silver_bronze_medals_BHP_diamond_pin_-_3b_-_2000_Sydney_medal_photo.jpg)*
- **Gold - the highest tier, still the same event** — AAA raises the bar further on the identical underlying criteria as A and AA - it is not a separate, unrelated standard.
- **Silver - a real, ordered result beneath gold** — AA sits between the floor and the stretch goal - a genuine, meaningfully stricter bar than Level A, and the level most commonly required in practice.
- **Bronze - a real accomplishment, not a token** — Level A is the floor, not a participation ribbon - it addresses the most severe access barriers and is a genuine, checkable bar on its own.
- **An extra honor beyond the medal tiers** — The diamond pin is an additional recognition layered on top of a real result - much like an organization choosing to exceed AA for one specific, deliberate reason, rather than by default.

**Deciding which conformance level to target**

1. **Start from Level A as the non-negotiable floor** — These criteria address the most severe access barriers; nothing ships without them.
2. **Target Level AA as the default** — It is cumulative with A, and it is what law, contracts, and policy actually reference in practice.
3. **Treat AAA as a deliberate, scoped exception** — Apply it only where a team has a specific reason and content type that can actually achieve it.
4. **Re-verify the whole chain, not just the newest criteria** — A regression in an old Level A check breaks the AA claim just as much as a new failure would.

*A WCAG conformance-level checker (Python)*

```python
checklist = [
    {"criterion": "Non-text content has a text alternative", "level": "A", "met": True},
    {"criterion": "Keyboard operable, no traps", "level": "A", "met": True},
    {"criterion": "Page has a descriptive title", "level": "A", "met": True},
    {"criterion": "Text contrast at least 4.5:1", "level": "AA", "met": True},
    {"criterion": "Text can resize to 200 percent without loss of content", "level": "AA", "met": True},
    {"criterion": "Consistent navigation across pages", "level": "AA", "met": False},
    {"criterion": "Sign language interpretation for prerecorded audio", "level": "AAA", "met": False},
    {"criterion": "Text contrast at least 7:1", "level": "AAA", "met": False},
]

order = ["A", "AA", "AAA"]

def summarize(checklist):
    by_level = {lvl: [] for lvl in order}
    for item in checklist:
        by_level[item["level"]].append(item)
    return by_level

def level_status(by_level):
    results = {}
    for lvl in order:
        items = by_level[lvl]
        failed = [i for i in items if not i["met"]]
        results[lvl] = (len(failed) == 0, failed)
    return results

by_level = summarize(checklist)
status = level_status(by_level)

print("WCAG conformance-level checklist:")
print()
for lvl in order:
    items = by_level[lvl]
    passed_count = sum(1 for i in items if i["met"])
    print("Level " + lvl + ": " + str(passed_count) + "/" + str(len(items)) + " criteria met")
    for i in items:
        mark = "PASS" if i["met"] else "FAIL"
        print("  [" + mark + "] " + i["criterion"])
print()

achieved = None
cumulative_ok = True
for lvl in order:
    ok, failed = status[lvl]
    cumulative_ok = cumulative_ok and ok
    if cumulative_ok:
        achieved = lvl

print("Highest conformance level actually achieved: " + (achieved if achieved else "None"))
if achieved != "AAA":
    next_level = order[order.index(achieved) + 1] if achieved else "A"
    blockers = [i["criterion"] for i in by_level[next_level] if not i["met"]]
    print("Blocking " + next_level + ": " + "; ".join(blockers))
```

*A WCAG conformance-level checker (Java)*

```java
import java.util.*;

public class Main {
    static class Item {
        String criterion;
        String level;
        boolean met;

        Item(String criterion, String level, boolean met) {
            this.criterion = criterion;
            this.level = level;
            this.met = met;
        }
    }

    public static void main(String[] args) {
        List<Item> checklist = new ArrayList<>();
        checklist.add(new Item("Non-text content has a text alternative", "A", true));
        checklist.add(new Item("Keyboard operable, no traps", "A", true));
        checklist.add(new Item("Page has a descriptive title", "A", true));
        checklist.add(new Item("Text contrast at least 4.5:1", "AA", true));
        checklist.add(new Item("Text can resize to 200 percent without loss of content", "AA", true));
        checklist.add(new Item("Consistent navigation across pages", "AA", false));
        checklist.add(new Item("Sign language interpretation for prerecorded audio", "AAA", false));
        checklist.add(new Item("Text contrast at least 7:1", "AAA", false));

        String[] order = {"A", "AA", "AAA"};

        Map<String, List<Item>> byLevel = new LinkedHashMap<>();
        for (String lvl : order) byLevel.put(lvl, new ArrayList<>());
        for (Item i : checklist) byLevel.get(i.level).add(i);

        Map<String, Boolean> levelOk = new LinkedHashMap<>();
        Map<String, List<String>> levelFailed = new LinkedHashMap<>();
        for (String lvl : order) {
            List<Item> items = byLevel.get(lvl);
            List<String> failed = new ArrayList<>();
            for (Item i : items) if (!i.met) failed.add(i.criterion);
            levelOk.put(lvl, failed.isEmpty());
            levelFailed.put(lvl, failed);
        }

        System.out.println("WCAG conformance-level checklist:");
        System.out.println();
        for (String lvl : order) {
            List<Item> items = byLevel.get(lvl);
            long passedCount = items.stream().filter(i -> i.met).count();
            System.out.println("Level " + lvl + ": " + passedCount + "/" + items.size() + " criteria met");
            for (Item i : items) {
                String mark = i.met ? "PASS" : "FAIL";
                System.out.println("  [" + mark + "] " + i.criterion);
            }
        }
        System.out.println();

        String achieved = null;
        boolean cumulativeOk = true;
        for (String lvl : order) {
            boolean ok = levelOk.get(lvl);
            cumulativeOk = cumulativeOk && ok;
            if (cumulativeOk) achieved = lvl;
        }

        System.out.println("Highest conformance level actually achieved: " + (achieved != null ? achieved : "None"));
        if (!"AAA".equals(achieved)) {
            String nextLevel = order[Arrays.asList(order).indexOf(achieved) + 1];
            List<String> blockers = levelFailed.get(nextLevel);
            System.out.println("Blocking " + nextLevel + ": " + String.join("; ", blockers));
        }
    }
}
```

### Your first time: Score one real page against all three levels

- [ ] List a handful of criteria spanning A, AA, and AAA — Use this note's checklist as a starting shape, then swap in real findings.
- [ ] Mark each as met or not met from actual testing — Not from assumption - check contrast, keyboard operation, and text alternatives directly.
- [ ] Compute the achieved level using the cumulative rule — A single failed Level A criterion caps the result at 'not even A', regardless of how many AA or AAA criteria pass.
- [ ] Report the achieved level and the specific blockers to the next one — Not just a percentage - name exactly what is failing and at which level.

- **A team claims 'AA compliant' but one Level A criterion is failing somewhere in scope.**
  Explain the cumulative rule: AA conformance requires every Level A criterion to also be met, so the claim is not accurate until that gap closes, regardless of how many AA-specific criteria pass.
- **Stakeholders want to target AAA everywhere by default.**
  Point to the W3C's own guidance that AAA is not recommended as a blanket site-wide requirement, since some AAA criteria cannot be met for every content type - suggest scoping AAA to specific, deliberate cases instead.
- **A conformance claim covers 'the whole site' but testing only covered a few pages.**
  Scope the claim honestly to the pages and flows actually tested - conformance is normally asserted per defined scope, not as an unqualified blanket statement.

### Where to check

- The W3C's own WCAG 2.2 standard and its Understanding documents for authoritative level definitions.
- Whether a "compliant" claim is scoped to specific pages/flows or asserted as an unqualified blanket statement.
- Whether every Level A criterion in scope truly passes before accepting an AA claim.
- [[accessibility-testing/why-accessibility-matters/pour-principles]] for the four principles that organize the criteria within each level.

### Worked example: an AA claim that was not actually true yet

1. A team reports "we are WCAG 2.2 AA compliant" ahead of a compliance review.
2. An independent audit checks a sample of Level A criteria first, as the cumulative rule requires.
3. One Level A criterion fails: an icon-only search button has no accessible name anywhere it appears.
4. Because AA conformance requires every Level A criterion to hold, the accurate status is "not yet
   conformant at any level," not "AA except for one AA-specific item."
5. Report: "Level A gap found (icon-only search button lacks an accessible name); this blocks any AA
   conformance claim until resolved, per WCAG's cumulative level definition." The team fixes the one
   component-level issue and the claim becomes accurate again.

**Quiz.** A product passes every Level AA-specific criterion the team checked, but one Level A criterion is failing on a page in scope. What is the accurate conformance status?

- [ ] Level AA, since all the AA-specific criteria pass
- [x] Not conformant at Level AA (or any level) yet, because AA conformance requires every Level A criterion to also be met, and one is failing
- [ ] Level AAA, since AA and A are both close to passing
- [ ] The failing Level A criterion does not matter since it is a lower level than AA

*This note defines the levels as cumulative: meeting Level AA requires meeting every Level A criterion too. A single failing Level A item caps the real status below AA, regardless of how many AA-specific criteria separately pass.*

- **Level A** — The floor - addresses the most severe access barriers. A genuine, checkable minimum bar, not a participation ribbon.
- **Level AA** — Includes all of Level A, plus more. The level most commonly required by law, contracts, and policy in practice.
- **Level AAA** — Includes all of Level A and AA, plus the strictest additional criteria. Not recommended by the W3C as a blanket site-wide requirement.
- **The cumulative rule** — Each level includes every criterion from the level(s) below it - a single failing Level A criterion blocks any accurate AA or AAA claim.

### Challenge

Take one real page. List at least two criteria you can actually verify at each of Level A, AA, and AAA (contrast, keyboard operation, and text alternatives are good starting points). Mark each met or not met from real testing, then compute the honestly achieved conformance level using the cumulative rule.

- [W3C WAI — WCAG Overview (current standard, WCAG 2.2)](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [W3C WAI — Understanding Conformance](https://www.w3.org/WAI/WCAG22/Understanding/conformance)
- [The Ultimate Accessibility Checklist: WCAG 2.2 A/AA/AAA](https://www.youtube.com/watch?v=njN4xEMC-PM)

🎬 [The Ultimate Accessibility Checklist: WCAG 2.2 A/AA/AAA](https://www.youtube.com/watch?v=njN4xEMC-PM) (23 min)

- WCAG 2.2 defines three conformance levels - A, AA, AAA - each one cumulative with the level(s) before it.
- Level A is a genuine floor addressing the most severe barriers, not an optional starting point.
- Level AA is the practical default target most law, contracts, and policy actually reference.
- Level AAA is a deliberate stretch goal, not a recommended blanket requirement for an entire site.
- A single failing Level A criterion blocks any accurate AA or AAA conformance claim, no matter how many higher-level criteria separately pass.


## Related notes

- [[Notes/accessibility-testing/why-accessibility-matters/pour-principles|POUR principles]]
- [[Notes/accessibility-testing/why-accessibility-matters/the-business-and-legal-case-ada-eaa|The business & legal case (ADA/EAA)]]
- [[Notes/accessibility-testing/why-accessibility-matters/disabilities-and-assistive-tech|Disabilities & assistive tech]]


---
_Source: `packages/curriculum/content/notes/accessibility-testing/why-accessibility-matters/wcag-2-2-a-aa-aaa.mdx`_
