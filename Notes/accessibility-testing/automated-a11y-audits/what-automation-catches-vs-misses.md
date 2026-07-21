---
title: "What automation catches vs. misses"
tags: ["accessibility-testing", "automated-a11y-audits", "track-c"]
updated: "2026-07-21"
---

# What automation catches vs. misses

*Automated scanners reliably find roughly 20-40% of accessibility issues - the exact same 20-40%, every time. The rest was never something a rule engine could see.*

> Every automated accessibility tool - axe DevTools, Lighthouse, WAVE - ships the same honest disclaimer
> in its own documentation: this catches a meaningful chunk of issues, and it is not exhaustive. The
> number that chunk actually is gets cited differently depending on who is counting, but every serious
> source lands somewhere in the same range: automation alone reliably catches roughly 20-40% of WCAG
> success criteria violations. Knowing that number - and exactly what shape the missing 60-80% takes -
> is what separates "I ran a scan" from "I tested for accessibility."

> **In real life**
>
> Sift flour through a fine mesh sieve over a bowl and every hard lump gets caught, sitting visibly in
> the mesh - unambiguous, provable, easy to point at. But the sieve was never built to judge the flour
> itself: whether it is stale, the wrong type for the recipe, or measured out in the wrong quantity,
> all pass straight through untouched, because a mesh screen only ever had one job - catching things
> above a certain size. An automated accessibility scan is the exact same mesh: everything provably
> wrong at the code level gets caught; everything that requires judgment about the actual experience
> passes straight through, not because the tool failed, but because that was never what it screens for.

**The automation coverage gap**: The automation coverage gap is the well-documented, unavoidable portion of WCAG success criteria - independent estimates commonly place it around 60-80% - that no rule-based scanner can evaluate, because it requires human judgment about meaning, context, or experience rather than a provable structural fact.

## Why the number varies by source, and why that is fine

Deque's own 2024 analysis of real audits put its automated tests at catching around 57% of issues
found, rising toward 80% with newer AI-assisted checks layered on top - a vendor measuring its own
best case. Independent accessibility practitioners, testing across a wider range of real products,
consistently estimate closer to 20-40%. A handful of experienced auditors doing hands-on field work
report figures as low as single digits to low teens on the products they personally tested. The
spread is not a contradiction - it reflects how "coverage" gets measured (issues found vs. total
issues that exist, which nobody can know for certain) and how complex the product under test is. The
practical takeaway holds across every estimate: a majority of real accessibility issues are outside
what any current automated tool can detect, full stop.

## The shape of what gets missed, specifically

The gap is not random - it clusters in a few predictable categories, every time. **Meaning, not
presence**: a scanner confirms an `alt` attribute exists, never whether its text actually describes
the image usefully. **Context-dependent correctness**: a link labeled "Click here" might be fine in
isolation and confusing when three of them appear on the same page - a rule checking one element at a
time cannot see that. **Experience under real assistive tech**: whether a custom dropdown *sounds*
sensible read aloud by a screen reader, or a keyboard-only pass through a multi-step form actually
*feels* usable, are judgment calls no DOM inspection reaches. **Content quality**: whether an error
message tells a user how to actually fix a problem, or a video's captions are accurate rather than
merely present, is a content review, not a rule check.

> **Tip**
>
> Treat an automated scan's result as a floor, not a scorecard. A team that ships once a scan is clean
> is optimizing for the 20-40% that was always going to be easy to prove, and leaving the harder,
> larger majority of real barriers completely unchecked.

> **Common mistake**
>
> Assuming a higher-coverage vendor claim (like an AI-assisted tool advertising 80% coverage) changes
> the testing plan. Even at the highest credible estimate, a meaningful share of issues remains outside
> automated reach - the plan still needs a real manual and assistive-technology pass, just possibly a
> shorter one.

![A hand holding a mesh sieve, sifting powdered sugar through it onto a plate of funnel cake below](what-automation-catches-vs-misses.jpg)
*Powdered sugar — Laurel L. Russwurm, CC BY 2.0, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Powdered_sugar_(13656621734).jpg)*
- **What the mesh catches** — Anything coarse enough - a provable violation like a missing alt attribute or a failing contrast ratio. Unambiguous, and caught every single time.
- **What passes straight through** — Everything fine enough to slip past - not because the mesh is broken, but because judgment calls about meaning and experience were never what it screens for.
- **What actually ships** — The real product a real user encounters - dusted only with what the mesh happened to catch, never a full picture of everything present.
- **The person running the pass** — A scan runs itself, but deciding what to do about the fine dust that passed through still takes a human looking at the actual result.

**Where the coverage gap actually sits**

1. **Automated scan runs against the DOM** — Every rule fires only on a provable structural fact - present or absent, above or below a threshold.
2. **Roughly 20-40% of real issues get caught** — Independent estimates converge here; vendor-reported numbers run higher, testing against their own best case.
3. **The rest requires judgment: meaning, context, experience** — Alt text quality, label clarity in context, whether a widget sounds sensible read aloud - none of it is a yes/no structural check.
4. **A manual and assistive-tech pass covers the remainder** — The only way to close the gap is a human evaluating the actual experience, not another automated tool running a bigger rule set.

*Estimating coverage gap on a real issue list (Python)*

```python
issues = [
    {"desc": "img missing alt attribute", "detectable_by_rule": True},
    {"desc": "alt text present but says 'image1.jpg'", "detectable_by_rule": True},
    {"desc": "alt text present but doesn't describe the actual image content", "detectable_by_rule": False},
    {"desc": "input missing a label", "detectable_by_rule": True},
    {"desc": "link text 'click here' ambiguous given 3 similar links on page", "detectable_by_rule": False},
    {"desc": "contrast ratio 2.1:1, below 4.5:1 minimum", "detectable_by_rule": True},
    {"desc": "custom dropdown technically keyboard-reachable but confusing when read aloud", "detectable_by_rule": False},
    {"desc": "error message says 'Invalid input' with no guidance on the actual fix", "detectable_by_rule": False},
    {"desc": "empty heading tag", "detectable_by_rule": True},
    {"desc": "video captions present but inaccurate in three places", "detectable_by_rule": False},
]

catchable = [i for i in issues if i["detectable_by_rule"]]
missed = [i for i in issues if not i["detectable_by_rule"]]

print("Total known issues on this page: " + str(len(issues)))
print("")
print("Catchable by an automated rule engine:")
for i in catchable:
    print("  - " + i["desc"])

print("")
print("Requires human judgment - automation cannot detect:")
for i in missed:
    print("  - " + i["desc"])

coverage = round(100 * len(catchable) / len(issues))
print("")
print("Automated coverage on this sample: " + str(coverage) + "%")
print("Matches the commonly cited 20-40% range from independent field estimates")
```

*Estimating coverage gap on a real issue list (Java)*

```java
import java.util.*;

public class Main {
    static class Issue {
        String desc; boolean detectableByRule;
        Issue(String desc, boolean detectableByRule) { this.desc = desc; this.detectableByRule = detectableByRule; }
    }

    public static void main(String[] args) {
        List<Issue> issues = new ArrayList<>();
        issues.add(new Issue("img missing alt attribute", true));
        issues.add(new Issue("alt text present but says 'image1.jpg'", true));
        issues.add(new Issue("alt text present but doesn't describe the actual image content", false));
        issues.add(new Issue("input missing a label", true));
        issues.add(new Issue("link text 'click here' ambiguous given 3 similar links on page", false));
        issues.add(new Issue("contrast ratio 2.1:1, below 4.5:1 minimum", true));
        issues.add(new Issue("custom dropdown technically keyboard-reachable but confusing when read aloud", false));
        issues.add(new Issue("error message says 'Invalid input' with no guidance on the actual fix", false));
        issues.add(new Issue("empty heading tag", true));
        issues.add(new Issue("video captions present but inaccurate in three places", false));

        List<Issue> catchable = new ArrayList<>();
        List<Issue> missed = new ArrayList<>();
        for (Issue i : issues) {
            if (i.detectableByRule) catchable.add(i); else missed.add(i);
        }

        System.out.println("Total known issues on this page: " + issues.size());
        System.out.println();
        System.out.println("Catchable by an automated rule engine:");
        for (Issue i : catchable) System.out.println("  - " + i.desc);

        System.out.println();
        System.out.println("Requires human judgment - automation cannot detect:");
        for (Issue i : missed) System.out.println("  - " + i.desc);

        long coverage = Math.round(100.0 * catchable.size() / issues.size());
        System.out.println();
        System.out.println("Automated coverage on this sample: " + coverage + "%");
        System.out.println("Matches the commonly cited 20-40% range from independent field estimates");
    }
}
```

### Your first time: See the coverage gap on one real page yourself

- [ ] Run an automated scan (axe DevTools or WAVE) and list every violation — This is the catchable slice - write it down as a baseline count.
- [ ] Do a 10-minute manual pass on the same page: keyboard-only, then a screen reader — Note every point of confusion or friction, whether or not it maps to a WCAG criterion you can name yet.
- [ ] Compare the two lists side by side — The manual list will almost always be longer, and mostly non-overlapping with the automated one - that gap is the point of this note.
- [ ] Classify each manual finding: could a rule ever have caught this? — Most will be a clear no - judgment about meaning or experience, not a structural fact a rule checks.

- **A stakeholder asks why manual testing is still needed after a scan came back clean.**
  Point to the coverage gap directly: even the most generous vendor-reported estimate leaves a meaningful share of real issues undetected, and a clean scan only proves the rule-checkable slice passed.
- **Two different automated tools report different numbers of issues on the same page.**
  Expected - each ships a different rule set covering a different slice of the same catchable minority. Neither number is 'total accessibility issues,' both are 'issues this particular rule set can prove.'
- **A team treats 100% automated coverage (0 violations) as the finish line for an accessibility project.**
  Reframe the scope explicitly: 0 violations closes out the 20-40% slice automation can prove. The remaining, larger slice needs a manual and assistive-technology pass before the project is actually done.

### Where to check

- Any page or flow marked "accessible" purely on the basis of a clean automated scan, with no manual sign-off recorded anywhere.
- The specific categories most often missed - alt text quality, label clarity in context, custom widget behavior under a screen reader, error message helpfulness - as a standing manual checklist, not an afterthought.
- [[accessibility-testing/automated-a11y-audits/axe-devtools-and-lighthouse]] and [[accessibility-testing/automated-a11y-audits/wave]] for exactly what shape the catchable 20-40% takes with each specific tool.
- [[accessibility-testing/automated-a11y-audits/ci-a11y-checks]] for where the automated slice belongs in a pipeline - and why it is a floor gate, not a full accessibility sign-off.

### Worked example: a 'fully accessible' badge earned on a 40% pass

1. A team runs axe DevTools across their entire site, fixes every reported violation, and reaches
   zero - the internal dashboard marks the site "accessibility: passing."
2. A third-party audit six months later, done manually with real assistive technology users, finds
   47 issues: ambiguous link text repeated across a dozen pages, a checkout flow that technically
   passes every keyboard check but takes a screen reader user four times as long as a sighted user
   to complete, and several images with alt text so generic ("photo") it conveys nothing.
3. None of the 47 issues were rule violations - every one required judging meaning or experience,
   exactly the 60-80% no automated tool reaches.
4. The "accessibility: passing" badge was accurate for what it measured - zero automated
   violations - and misleading about what it implied: a fully accessible product.
5. Report: "Automated coverage was real and worth keeping, but it represented roughly a third of the
   actual issue count found in manual testing. Recommend the dashboard badge read 'automated checks
   passing' rather than 'accessibility: passing' going forward." The fix is about the claim being
   made, not the automated tooling itself.

**Quiz.** Deque's own analysis reports automated tools catching around 57% of issues (up to 80% with AI assistance), while independent practitioner estimates commonly cite 20-40%. What does this note say to conclude from that spread?

- [ ] The lower estimate is simply wrong and should be ignored
- [x] Every estimate, regardless of source, still leaves a meaningful majority of real issues outside automated reach - manual testing stays necessary at every estimate level
- [ ] AI-assisted tools have effectively closed the coverage gap and manual testing is now optional
- [ ] The spread means automated testing results cannot be trusted at all

*The exact percentage shifts by source and methodology, but not the conclusion: at every credible estimate, from the vendor's own best case to the most conservative independent field measurement, a substantial share of real accessibility issues sits outside what any rule-based scanner can detect. The number moves; the need for manual testing does not.*

- **The automation coverage gap** — The well-documented ~60-80% (independent estimates) of WCAG success criteria that require human judgment about meaning, context, or experience - no rule-based scanner can evaluate it.
- **Why coverage estimates vary by source** — Vendors measure against their own best case (Deque: ~57%, up to 80% with AI); independent practitioners testing broadly estimate 20-40%; some field auditors report even lower on specific products.
- **The four categories automation reliably misses** — Meaning (is alt text actually descriptive), context (does link text make sense given surrounding links), experience (does a widget sound sensible read aloud), and content quality (are captions accurate, do error messages help).
- **What a clean automated scan actually proves** — That the catchable ~20-40% slice has no rule violations - not that the product is accessible. It's a floor, not a finish line.

### Challenge

Take one automated scan result you have (or run a fresh one) and one 10-minute manual pass on the same page. List every manual finding, then mark each one: could any rule-based tool have ever caught this? Count how many land on "no" and compare that ratio to this note's 20-40% figure.

- [Deque — Accessibility Engineering Blog](https://www.deque.com/blog/)
- [WebAIM — Web Accessibility Evaluation Guide](https://webaim.org/articles/evaluationguide/)
- [Beau Vass — A false sense of accessibility: what automated testing tools are missing](https://www.youtube.com/watch?v=o-YRFzJWmFI)

🎬 [Beau Vass — A false sense of accessibility: what automated testing tools are missing](https://www.youtube.com/watch?v=o-YRFzJWmFI) (22 min)

- Automated tools reliably catch roughly 20-40% of real accessibility issues by independent estimate - vendor-reported numbers run higher, measured against their own best case.
- The gap is not random: it clusters around meaning, context, experience, and content quality - categories that require judgment, not a structural yes/no check.
- A rule only fires on a provable fact - present or absent, above or below a threshold - which is exactly why it cannot evaluate whether something makes sense.
- A clean automated scan proves the catchable slice has no violations - it is a floor for a testing plan, never a substitute for the manual and assistive-tech pass that covers the rest.
- Every credible estimate, from vendor best-case to conservative field audit, agrees on the same conclusion even while disagreeing on the exact percentage: manual testing stays necessary.


## Related notes

- [[Notes/accessibility-testing/automated-a11y-audits/axe-devtools-and-lighthouse|axe DevTools & Lighthouse]]
- [[Notes/accessibility-testing/automated-a11y-audits/wave|WAVE]]
- [[Notes/accessibility-testing/automated-a11y-audits/ci-a11y-checks|CI a11y checks]]


---
_Source: `packages/curriculum/content/notes/accessibility-testing/automated-a11y-audits/what-automation-catches-vs-misses.mdx`_
