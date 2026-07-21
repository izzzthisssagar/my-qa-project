---
title: "Writing for developers"
tags: ["test-management-and-reporting", "docs-and-communication", "track-c"]
updated: "2026-07-21"
---

# Writing for developers

*'Drive me around' and 'take me to 140 Elm Street' are both instructions - only one is usable. Writing for developers means the address version: exact function names, exact error text copied not retyped, never a vague gesture at the general area of the problem.*

> "The search is kind of slow sometimes" and "search-by-name returns in 4.2s at p95 with more than 500
> results, versus 0.3s below that threshold" describe the exact same real observation - only one of them
> gives a developer anything to act on. "Kind of slow" could mean a UI animation lag, a network issue, or
> a database query problem, and a developer reading it has to do all the investigative work the original
> report should have already done. Writing for developers means handing over the second version, every
> time, not the first.

> **In real life**
>
> An engineering drawing is drafted with a set square marked to the millimeter, a compass that traces
> one exact arc every time, and pencils kept sharp on purpose - nothing about it is approximate, because
> the entire point is that someone else can build the described object from the drawing alone, without
> ever meeting the person who drew it. A drawing labeled "pipe, roughly here, about this big" would be
> useless no matter how carefully it was sketched. Writing for developers needs that same discipline:
> exact values, exact names, exact conditions - precision is not a nice-to-have layered on top of the
> content, it is the content.

**Writing for developers**: Writing for developers means using the precise vocabulary, exact values, and structural conventions a technical reader already expects - naming the actual function, file, or component involved, quoting exact error text rather than paraphrasing it, and stating measurable conditions instead of vague qualifiers - so the reader can act without first having to reconstruct what actually happened.

## Precision is the content, not decoration on top of it

Vague qualifiers - "sometimes," "seems slow," "kind of broken," "occasionally fails" - are the single
most common failure in writing meant for a technical reader, because each one hides an actual,
discoverable condition behind an adjective. "Sometimes" almost always means something specific:
happens under load, happens for a particular input shape, happens after a particular sequence of
actions. Finding and stating that specific condition is not extra polish on a report or a doc - it is
the entire value the writer was supposed to add before handing it off. Error text, log lines, and
stack traces should be copied exactly, not retyped from memory - a single transcription error can send
a developer chasing the wrong symptom entirely.

## Use the vocabulary the reader already has

A developer thinks in terms of functions, files, classes, and exact parameter values - not "the thing
that handles logins" or "that page with the form on it." Referencing the actual `AuthService.login()`
or the exact file and line number, when known, closes the gap between what a reader has to guess and
what they can act on immediately. This is the direct opposite of writing for a non-technical
stakeholder, where the same underlying fact gets deliberately translated away from exactly this kind
of code-level vocabulary - writing for developers goes the other direction, toward more precision and
more of the reader's own technical language, not less.

> **Tip**
>
> Before finalizing anything meant for a developer - a bug report, a PR description, a technical doc -
> read it back and flag every adjective describing severity, frequency, or degree ("slow," "often,"
> "broken"). Replace each one with the specific, measurable condition it was standing in for.

> **Common mistake**
>
> Writing a developer-facing report in the same business-impact style used for a stakeholder update.
> The two audiences need opposite treatment - a stakeholder report translates technical detail away;
> a developer-facing one needs that exact technical detail restored and made as precise as possible.

![Precision drafting tools including a marked set square, protractor, compass, and sharpened pencils on top of a labeled technical engineering drawing](writing-for-developers.jpg)
*Engineering design drawings — Dinesh Cyanam, CC BY-SA 2.0, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Engineering_design_drawings.jpg)*
- **The labeled drawing itself** — Every part named exactly - 'Gland,' not 'the thingy near the end.' Writing for developers needs the same precision: name the actual function, file, or component, never a vague gesture at where the problem roughly is.
- **The ruler, marked to the millimeter** — No approximate measurements in a drawing meant to be built from. Developer-facing writing needs the same exactness: exact steps, exact values, exact error text - never 'sometimes' or 'kind of slow.'
- **Freshly sharpened pencils** — Precision tools, kept precise on purpose. Clear, specific language is the writing equivalent - the tool has to actually be sharp before the result can be exact.
- **The compass - built for one exact task** — Draws one specific kind of line, exactly, every time. Developer-facing writing benefits from the same discipline: the vocabulary and structure developers already expect, not an improvised version borrowed from a different audience.

**Turning a vague observation into developer-usable writing**

1. **Start with the vague version** — "Search is kind of slow sometimes" - a real observation, hiding a specific, discoverable condition behind an adjective.
2. **Find the exact condition the adjective was standing in for** — Slow under what load, for what input, after what sequence - reproduce it and measure it.
3. **Replace every adjective with the measured specific** — "4.2s at p95 with 500+ results, 0.3s below that" - now a developer has an actual target.
4. **Reference the actual code, file, or component involved** — Where known, name it directly - closing the gap between what the reader has to guess and what they can act on.

*Auditing writing for vague qualifiers (Python)*

```python
VAGUE_QUALIFIERS = ["sometimes", "kind of", "seems", "occasionally", "often", "a bit", "slow"]

drafts = [
    "The search page seems kind of slow sometimes when there are a lot of results.",
    "search-by-name (SearchController.byName) returns in 4.2s at p95 when results exceed 500; "
    "0.3s below that threshold.",
]

for draft in drafts:
    lower = draft.lower()
    found = [q for q in VAGUE_QUALIFIERS if q in lower]
    print("Draft: " + draft[:70] + ("..." if len(draft) > 70 else ""))
    if found:
        print("  Vague qualifiers found: " + ", ".join(found) + " -> needs a specific, measured replacement")
    else:
        print("  No vague qualifiers found - specific and actionable")
    print("")
```

*Auditing writing for vague qualifiers (Java)*

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> vagueQualifiers = Arrays.asList(
                "sometimes", "kind of", "seems", "occasionally", "often", "a bit", "slow");

        List<String> drafts = Arrays.asList(
                "The search page seems kind of slow sometimes when there are a lot of results.",
                "search-by-name (SearchController.byName) returns in 4.2s at p95 when results exceed 500; " +
                "0.3s below that threshold."
        );

        for (String draft : drafts) {
            String lower = draft.toLowerCase();
            List<String> found = new ArrayList<>();
            for (String q : vagueQualifiers) {
                if (lower.contains(q)) found.add(q);
            }

            String preview = draft.length() > 70 ? draft.substring(0, 70) + "..." : draft;
            System.out.println("Draft: " + preview);
            if (!found.isEmpty()) {
                System.out.println("  Vague qualifiers found: " + String.join(", ", found) +
                        " -> needs a specific, measured replacement");
            } else {
                System.out.println("  No vague qualifiers found - specific and actionable");
            }
            System.out.println();
        }
    }
}
```

### Your first time: Rewrite one vague observation precisely

- [ ] Find one recent bug report, PR description, or doc entry you wrote quickly — Something written in the moment, without much revision.
- [ ] Circle every adjective describing severity, frequency, or degree — 'Slow,' 'sometimes,' 'often,' 'broken' - anything standing in for a specific condition.
- [ ] Reproduce the issue and find the actual measurable condition behind each one — What load, what input, what exact sequence actually triggers it.
- [ ] Rewrite the sentence with the specific condition in place of the adjective — Confirm a developer reading only the rewritten version would know exactly what to check.

- **A developer asks a clarifying question before starting work on almost every bug report you file.**
  A strong signal of vague qualifiers or missing specifics - audit recent reports for adjectives standing in for measurable conditions and replace them before filing.
- **A PR description reads well but a reviewer still has to read the entire diff to understand what changed and why.**
  The description likely describes intent narratively rather than naming the specific functions, files, or behaviors changed - developers need the precise, code-referencing version, not a summary.
- **A copy-pasted error message in a report doesn't match what actually appears in the logs.**
  Likely retyped from memory rather than copied exactly - always paste the exact text; a single transcription error can send a developer chasing the wrong symptom entirely.

### Where to check

- Any bug report, PR description, or technical doc about to be filed for a developer audience, scanned specifically for vague severity/frequency adjectives before submission.
- Error text and log lines in any report - confirm they were copied exactly, never retyped from memory.
- [[test-management-and-reporting/docs-and-communication/confluence-and-wikis]] for applying this same precision standard to durable documentation, not just one-off reports.
- [[test-management-and-reporting/metrics-and-reporting/reporting-to-stakeholders]] for the opposite discipline - translating the same fact away from this level of technical detail for a non-technical audience.
- [[accessibility-testing/reporting-and-fixing/writing-a11y-findings-devs-act-on]] for this exact same precision principle applied specifically to accessibility findings.

### Worked example: a report rewritten from vague to actionable, same underlying bug

1. A tester notices the search page "feels slow sometimes" during exploratory testing and files it as
   observed, with that exact phrasing.
2. A developer, given no specific condition to reproduce, spends an hour trying to notice slowness
   manually, cannot reliably trigger it, and marks the ticket "cannot reproduce."
3. The tester revisits the issue with a stopwatch and a script varying result-set size, finds the
   pattern precisely: response time is 0.3s for result sets under 500, climbing to 4.2s at 500+ due to
   an unindexed query in `SearchController.byName()`.
4. The ticket is rewritten: "search-by-name (SearchController.byName) takes 4.2s at p95 when results
   exceed 500, versus 0.3s below that threshold - likely a missing index on the results table."
5. The same developer picks the rewritten ticket up and identifies the exact missing index within
   twenty minutes - the underlying bug never changed, only how precisely it was described.

**Quiz.** What does this note identify as the single most common failure in writing meant for a developer audience?

- [ ] Using too much technical jargon and code references
- [x] Vague qualifiers like 'sometimes' or 'kind of slow' that hide a specific, discoverable condition behind an adjective, leaving the developer to do the investigative work themselves
- [ ] Writing reports that are too short
- [ ] Including exact error text and log lines

*A vague qualifier is a real observation with the actual, useful information stripped out of it. 'Sometimes' almost always corresponds to a specific, findable condition - a particular load, input, or sequence - and finding that condition before writing the report is exactly the work the report was supposed to have already done for the developer reading it.*

- **Writing for developers** — Using the precise vocabulary, exact values, and structural conventions a technical reader already expects - naming the actual function or file, quoting exact error text, stating measurable conditions instead of vague qualifiers.
- **Why vague qualifiers are the most common failure** — Words like 'sometimes' or 'kind of slow' hide a specific, discoverable condition behind an adjective - finding that condition is the value the writer was supposed to add before handing the report off.
- **Why error text should be copied, never retyped** — A single transcription error in retyped log text or an error message can send a developer chasing an entirely wrong symptom - exact copy-paste removes that risk.
- **Writing for developers vs. reporting to stakeholders** — Opposite directions on the same underlying fact - a stakeholder report translates technical detail away; developer-facing writing restores and sharpens that same detail.

### Challenge

Find one bug report, PR description, or doc entry you wrote recently. Circle every vague adjective describing severity or frequency, then rewrite it with the specific, measured condition each one was standing in for.

- [Mintlify — How to Write Technical Documentation That Developers Actually Use](https://www.mintlify.com/library/how-to-write-technical-documentation)
- [getDX — How to Write Excellent Technical Documentation](https://getdx.com/blog/tech-documentation/)
- [How to Write Technical Documentation That Actually Works](https://www.youtube.com/watch?v=HyhfaZoaaiA)

🎬 [How to Write Technical Documentation That Actually Works](https://www.youtube.com/watch?v=HyhfaZoaaiA) (8 min)

- Precision is the content of developer-facing writing, not decoration on top of it - exact values, exact names, exact conditions.
- Vague qualifiers ('sometimes,' 'kind of slow') hide a specific, discoverable condition - finding and stating that condition is the actual work of the report.
- Reference the exact function, file, or component when known - closing the gap between what a reader has to guess and what they can act on.
- Copy error text and log lines exactly rather than retyping from memory - a transcription error can send a developer chasing the wrong symptom entirely.
- Writing for developers is the mirror image of reporting to stakeholders - one restores and sharpens technical detail, the other translates it away.


## Related notes

- [[Notes/test-management-and-reporting/docs-and-communication/confluence-and-wikis|Confluence / wikis]]
- [[Notes/test-management-and-reporting/metrics-and-reporting/reporting-to-stakeholders|Reporting to stakeholders]]
- [[Notes/accessibility-testing/reporting-and-fixing/writing-a11y-findings-devs-act-on|Writing a11y findings devs act on]]


---
_Source: `packages/curriculum/content/notes/test-management-and-reporting/docs-and-communication/writing-for-developers.mdx`_
