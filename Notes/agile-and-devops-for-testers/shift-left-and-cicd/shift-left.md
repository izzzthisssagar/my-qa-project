---
title: "Shift left"
tags: ["agile-and-devops-for-testers", "shift-left-and-cicd", "shift-left"]
updated: "2026-07-20"
---

# Shift left

*Moving testing into requirements and design review, before code exists, because a defect caught on paper costs far less than one caught after it ships - and what that actually changes about a tester's day.*

> A story lands on the sprint board already broken - not because anyone wrote bad code, but because the
> acceptance criteria were vague, an edge case never came up in conversation, and the design quietly assumed
> something the backend can't actually do. A tester who first sees this story the day a pull request opens
> finds the problem the hard way, after two developers already built against the wrong assumption. A tester
> who read the same ticket a week earlier, before a single line of code existed, catches it with one
> five-minute question instead of a week of rework. That gap is the entire idea behind shifting left.

> **In real life**
>
> A city doesn't send its most important building inspector in only after the walls are painted and tenants
> have moved in. The inspection that actually prevents disasters happens on the architect's drawings, before
> the foundation is poured - checking that the plumbing plan and the electrical plan don't route through the
> same wall cavity, that a stairwell meets code width, that the load calculations hold before a single truck
> of concrete arrives. Catching a bad assumption on paper costs an eraser and twenty minutes. Catching the
> same assumption after the third floor is framed costs a demolition crew. Testing runs on the identical
> curve: the earlier in a design's life a problem gets caught, the cheaper it is to fix, and a tester's most
> valuable move is often the one made before there's anything built yet to run a test against.

**Shift left**: Shift-left testing is the practice of moving testing activities earlier in the software development lifecycle - reviewing requirements and designs, writing acceptance criteria and tests alongside or before code - so defects are found and fixed at the cheapest, earliest point possible, instead of waiting until code is complete to begin testing.

## Why earlier is so much cheaper

The reason shift left is worth the effort isn't philosophical, it's economic. A vague requirement caught
during backlog refinement costs one clarifying question. The same ambiguity caught during code review costs
a developer's rework. Left uncaught until a formal test phase, it costs a bug report, a triage meeting, and
a second round of development. Left uncaught until production, it costs an incident, a hotfix under
pressure, and possibly real damage to users who hit it first. This "cost grows by roughly an order of
magnitude at each later phase" idea is a widely cited - and admittedly imprecise - industry rule of thumb,
but the direction of the curve is not in dispute anywhere: a defect is cheapest the moment it's still just an
idea on a page, and gets more expensive every phase it survives undetected. Shift left is simply the
practice of putting a tester's judgment in front of that curve as early as the curve exists at all - which
means before requirements are finalized, not just before code merges.

## What actually changes about a tester's day

This is the part teams get wrong most often: shift left is not "run the same tests a little sooner in the
week." Running your regression suite one day earlier in the pipeline is a CI/CD optimization - useful, but
it's shifting *execution* left, not shifting *testing* left, and the two get conflated constantly. Real
shift left changes which meetings a tester is in and what they're doing there. It means sitting in backlog
refinement and asking what a requirement actually means before the team commits to a story point estimate
for it. It means reading a technical design doc and asking "how would we even verify this" before a single
API contract gets finalized between two teams. It means co-writing acceptance criteria with the Product
Owner while a story is still being shaped, not translating a finished feature into criteria after the fact.
None of that touches a keyboard running a test script - it's judgment applied to a document, a whiteboard
sketch, or a conversation, days or weeks before there's an application to click on.

> **Tip**
>
> The single highest-leverage shift-left habit is asking one question out loud in design review: "how would
> we know this actually works?" If nobody in the room can answer that in a sentence, the design isn't ready to
> build yet - and you just found that out for the cost of one question, not for the cost of a failed
> acceptance test three weeks later.

> **Common mistake**
>
> Treating "shift left" as a synonym for "automate more and run it earlier in CI." Test automation that runs
> sooner in a pipeline is a real, separate improvement - see [[agile-and-devops-for-testers/shift-left-and-cicd/the-cicd-pipeline]]
> - but it still only catches problems in code that already exists. If a tester never reviews a requirement or
> a design before code is written, moving the same post-code test suite an hour earlier changes nothing about
> how expensive the defects it finds already were to create.

![A printed page covered in handwritten pen edits, with crossed-out lines, insertions written above the text, a large circled passage in the left margin, a pen resting across the page, and a stack of other marked-up pages underneath](shift-left.jpg)
*Example of copyedited manuscript - Phoebe, Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:Example_of_copyedited_manuscript.jpg)*
- **A reviewer's pen, mid-document** — A human is catching problems on paper before this document is ever considered finished - the same instinct as reviewing a requirement or a design before a single line of code exists to test.
- **A sentence rewritten before it ever prints** — Crossing out a phrase and writing a replacement above it here costs nothing but a minute of the reviewer's time. Catching the same wording problem after the page is typeset and printed means reprinting - the cost curve shift left exists to stay ahead of.
- **A whole passage circled for a bigger rework** — This isn't a word-level fix - it's a structural flag on an entire section, the same way a design review can flag 'this whole approach won't work' before any code has been committed to it.
- **Every page in the stack gets this pass** — The markup happens page by page, systematically, before the manuscript goes anywhere - shift left isn't a one-time gate either, it's review built into every draft, not sampled occasionally after the fact.

**Where a tester's day starts now - press Play**

1. **Requirements review** — Before a ticket is even pulled into a sprint, a tester reads the ask and flags what's ambiguous, untestable as written, or missing an edge case entirely.
2. **Design review** — Before code exists, a tester sits in on the technical design and asks how a claim like 'this will scale' or 'this handles retries' would actually be verified.
3. **Code exists, tests get written alongside it** — The defect classes that would have come from a vague requirement or a broken design are already filtered out - unit and integration tests now target what's genuinely left to check.
4. **Late-stage testing shrinks to confirmation** — By the time a build reaches formal test, most of what used to surface here for the first time was already caught one or two phases earlier.

Here is a small shift-left checkpoint gate: it checks whether a tester was actually engaged at each SDLC
checkpoint, in order, and reports the first checkpoint that got skipped - because that's exactly where an
undetected defect keeps traveling until something finally catches it.

*A shift-left checkpoint gate (Python)*

```python
checkpoints = [
    ("requirements_review", True, 1),
    ("design_review", True, 5),
    ("code_review", False, 10),
    ("staging_test_phase", True, 50),
]

def check(name, engaged, cost_multiplier):
    label = name.upper()
    status = "ENGAGED" if engaged else "SKIPPED"
    print(label + "=" + status + " cost_if_missed_here=" + str(cost_multiplier) + "x")
    return engaged

results = [check(name, engaged, mult) for name, engaged, mult in checkpoints]
first_gap = next(name for name, engaged, mult in checkpoints if not engaged)
result = "PASS" if all(results) else "FAIL"
assert result == "FAIL", "expected a shift-left gap at " + first_gap
print("RESULT=" + result)
```

*A shift-left checkpoint gate (Java)*

```java
import java.util.*;

public class Main {
    static class Checkpoint {
        String name;
        boolean engaged;
        int costMultiplier;
        Checkpoint(String name, boolean engaged, int costMultiplier) {
            this.name = name;
            this.engaged = engaged;
            this.costMultiplier = costMultiplier;
        }
    }

    static boolean check(Checkpoint c) {
        String label = c.name.toUpperCase();
        String status = c.engaged ? "ENGAGED" : "SKIPPED";
        System.out.println(label + "=" + status + " cost_if_missed_here=" + c.costMultiplier + "x");
        return c.engaged;
    }

    public static void main(String[] args) {
        List<Checkpoint> checkpoints = new ArrayList<>();
        checkpoints.add(new Checkpoint("requirements_review", true, 1));
        checkpoints.add(new Checkpoint("design_review", true, 5));
        checkpoints.add(new Checkpoint("code_review", false, 10));
        checkpoints.add(new Checkpoint("staging_test_phase", true, 50));

        boolean allEngaged = true;
        String firstGap = null;
        for (Checkpoint c : checkpoints) {
            boolean ok = check(c);
            allEngaged &= ok;
            if (!ok && firstGap == null) firstGap = c.name;
        }
        String result = allEngaged ? "PASS" : "FAIL";
        if (!result.equals("FAIL")) throw new AssertionError("expected a shift-left gap at " + firstGap);
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: First time shifting left on a new team

- [ ] Ask to be added to backlog refinement, not just sprint planning — Refinement is where requirements are still soft enough to change cheaply. By sprint planning, the team is usually already committing to them.
- [ ] Read a ticket like a skeptic before it's estimated — Look for acceptance criteria that describe the happy path only, unstated assumptions, and anything that can't be verified as written.
- [ ] Ask 'how would we test this' out loud during design discussion — If the room can't answer in a sentence, the design has a testability gap worth naming before anyone starts building against it.
- [ ] Co-write acceptance criteria before code starts, not after — Criteria written to match what already shipped only confirm the build - they never had the chance to catch anything.

- **Testers only see a ticket the day a pull request opens for review.**
  That's the exact opposite of shift left - the tester's first contact with the work is already at the most expensive phase to catch anything. Push for an invite to backlog refinement and design discussions, even as a silent observer at first.
- **Acceptance criteria get written after a feature is already built, to describe what shipped.**
  Criteria written retroactively can only confirm behavior, never catch a wrong assumption before it's coded. Get criteria written and agreed while the story is still in refinement, before development starts.
- **The team says they've 'shifted left' because tests now run one stage earlier in the pipeline.**
  That's a real pipeline improvement, but it's shifting test execution left, not shifting testing left - see [[agile-and-devops-for-testers/shift-left-and-cicd/the-cicd-pipeline]]. Name the difference explicitly so the team doesn't stop there and call requirements review solved.

### Where to check

- The backlog refinement meeting - is a tester actually in the room asking questions, or only informed of decisions afterward?
- The most recent defect that took real rework to fix - trace it back and ask whether a requirements or design review question could have caught it first.
- Whether acceptance criteria exist before development starts on a story, or only get written to match what already shipped.
- [[agile-and-devops-for-testers/tester-in-a-sprint/acceptance-criteria]] for what a testable, story-specific acceptance criterion actually looks like.
- [[agile-and-devops-for-testers/shift-left-and-cicd/quality-gates]] for how the earliest-caught defects still get backed up by automated checkpoints later in the pipeline.

### Worked example: the API contract that broke two teams at once

1. **The setup:** A mobile team and a backend team agree on an API contract during a quick chat, with no
   written design doc and no tester in the conversation. Both teams start building against their own
   understanding of the same endpoint.
2. **The gap surfaces late:** Integration testing, three weeks later, reveals the mobile team expected a
   paginated response while the backend built a single full list - a mismatch that was never actually
   agreed on, just assumed identically by nobody.
3. **The root cause:** No design review happened where a tester - or anyone - could have asked "what does
   this response look like for a user with ten thousand records" before either team wrote a line of code.
4. **The fix that would have caught it for free:** A tester in that original conversation, asking one
   pagination question, would have forced both teams to write down the actual contract before building
   against two different guesses of it.
5. **The lesson:** The defect wasn't a coding mistake by either team - it was a requirements gap that had
   three weeks to compound before anyone could see it, precisely because no one reviewed the design while it
   was still just a conversation.

**Quiz.** A team says they've adopted shift-left testing because their automated test suite now runs one stage earlier in the CI pipeline. What's the most accurate read of this claim?

- [ ] This is exactly what shift-left testing means - running tests earlier is the whole practice
- [x] This is a real improvement to test execution timing, but it's not shift-left testing unless testers are also engaging with requirements and design before code exists
- [ ] This claim is meaningless - CI pipeline changes have nothing to do with testing quality
- [ ] This only counts as shift-left testing if the tests also run faster, not just earlier

*Running the same post-code tests earlier in a pipeline is a genuine, useful change - but it only ever catches problems in code that already exists. Shift-left testing specifically means moving a tester's involvement earlier in the SDLC, into requirements and design review, before any code has been written.*

- **Shift left, in one line** — Moving testing activities - especially requirements and design review - earlier in the SDLC, so defects are caught at the cheapest possible point, before code exists rather than after.
- **The most common shift-left mistake** — Confusing it with running the same post-code test suite earlier in a CI pipeline. That's a real improvement, but it's shifting execution left, not shifting testing left - it still only catches problems in code that already exists.
- **The highest-leverage shift-left habit** — Asking 'how would we know this actually works' out loud during design review, before a single line of code is written against the design.

### Challenge

Pick one story currently in your backlog that hasn't started development yet. Read only the requirement or design behind it and write down every question you'd need answered before you'd trust it's ready to build - then check how many of those questions the team can actually answer right now.

- [BrowserStack - Shift Left Testing: What it Means and Why it Matters](https://www.browserstack.com/guide/what-is-shift-left-testing)
- [Atlassian - 5 tips for shifting left in continuous testing](https://www.atlassian.com/blog/software-teams/5-tips-for-shifting-left-in-continuous-testing)
- [Shift Left Testing - What does it mean really?](https://www.youtube.com/watch?v=swZ12ZZmXjo)

🎬 [Shift Left Testing - What does it mean really?](https://www.youtube.com/watch?v=swZ12ZZmXjo) (6 min)

- Shift left means moving testing activities earlier in the SDLC, into requirements and design review - not just running the same post-code tests sooner.
- The economic case is a widely cited cost curve: the earlier a defect is caught, the cheaper it is to fix, and requirements or design review is the earliest a tester can catch anything at all.
- What actually changes is which meetings a tester is in and what they do there - backlog refinement, design review, and co-writing acceptance criteria before code starts.
- Running tests earlier in a CI/CD pipeline is a real, separate improvement to test execution - it still only catches problems in code that already exists.


## Related notes

- [[Notes/agile-and-devops-for-testers/shift-left-and-cicd/the-cicd-pipeline|The CI/CD pipeline]]
- [[Notes/agile-and-devops-for-testers/shift-left-and-cicd/quality-gates|Quality gates]]
- [[Notes/agile-and-devops-for-testers/tester-in-a-sprint/acceptance-criteria|Acceptance criteria]]


---
_Source: `packages/curriculum/content/notes/agile-and-devops-for-testers/shift-left-and-cicd/shift-left.mdx`_
