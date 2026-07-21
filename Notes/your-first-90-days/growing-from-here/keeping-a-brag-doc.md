---
title: "Keeping a brag doc"
tags: ["your-first-90-days", "growing-from-here", "track-c"]
updated: "2026-07-21"
---

# Keeping a brag doc

*A notebook filled in the moment, entry by entry, holds real numbers a memory reconstructed six months later never quite recovers. A brag doc is that same notebook kept for one purpose - so a performance review or resume update draws from actual evidence, not a strained after-the-fact guess.*

> Asked in a performance review to list this year's biggest contributions, a tester with no running
> record spends the first ten minutes just trying to remember what happened in February - and the
> specific bug that saved a release, or the process improvement that quietly reduced flaky test time by
> half, has usually faded into a vague "I did a lot of testing" by the time memory alone is asked to
> reconstruct it months later.

> **In real life**
>
> A notebook filled in daily, right in the moment something happens, holds the actual figures - a
> specific amount, a specific date, a specific note about what it was for - in a way memory alone rarely
> preserves with the same precision months later. Trying to reconstruct those same details from scratch
> after the fact means guessing, rounding, and often missing entries that felt unremarkable at the time
> but would have mattered in the full picture. A brag doc is that same discipline applied to work
> accomplishments: captured close to when they happened, in specific enough detail that six months later
> it holds real evidence, not a strained and incomplete memory.

**A brag doc**: A brag doc is a running, personal record of work accomplishments - bugs found, process improvements made, positive feedback received - written down close to when each one happens, specifically so a performance review, resume update, or promotion case can draw from real, specific evidence instead of an unreliable memory reconstructed under pressure months later.

## Specificity is what makes an entry actually useful later

"Found some good bugs this quarter" as a brag doc entry provides almost nothing to work with later - it
could describe anything from a minor cosmetic issue to a release-blocking discovery. "Found a checkout
total calculation bug affecting all users with stacked discount codes, caught before release" is usable
months later in a review, a resume line, or a promotion case, because the specific, concrete detail is
already there rather than needing to be reconstructed from a vague memory of "some good bugs." The habit
of writing the specific version in the moment, even briefly, is what separates a genuinely useful brag
doc from a list of vague entries that don't actually help later.

## Small, unremarkable-feeling wins belong in it too, not just the dramatic ones

A single release-blocking bug catch is an easy, obvious brag doc entry - it feels significant the moment
it happens. A quieter but genuinely valuable contribution, like writing a test data setup script that
saved the team a recurring ten minutes per test run, often gets skipped because it doesn't feel dramatic
in the moment. Over a full year, these smaller, easy-to-forget contributions frequently add up to a
larger and more well-rounded case than the handful of dramatic catches alone - and they're exactly the
entries most likely to be lost entirely without a running record capturing them close to when they
happened.

> **Tip**
>
> Set a recurring, low-effort reminder - weekly or biweekly - to add anything worth logging since the
> last entry, rather than relying on remembering to do it spontaneously. A two-minute weekly habit
> produces a far more complete record than sporadic entries only when something feels obviously
> brag-worthy.

> **Common mistake**
>
> Starting a brag doc only right before a performance review, then trying to backfill months of
> accomplishments from memory. This defeats the entire purpose - the whole value of the habit comes from
> capturing specific detail close to when it happened, not compressing a backward-looking memory exercise
> into the same rushed, imprecise conditions the document exists to avoid.

![A close-up of a hand writing in an open notebook filled with handwritten notes, with a laptop nearby](keeping-a-brag-doc.jpg)
*Person writing in a notebook — Shixart1985, CC BY 2.0, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Person_writing_in_a_notebook_while_sitting_at_a_desk.jpg)*
- **The notebook, already filled with entries** — A running record built entry by entry over time - not a single after-the-fact reconstruction attempt, which is exactly the difference a brag doc is built around.
- **The pen, actively writing a new line** — Capturing something close to when it happened - the specific habit that makes each entry actually useful months later, versus a vague memory reconstructed under pressure.
- **The laptop, positioned nearby but not the focus** — The actual work happening alongside the record of it - the brag doc runs in parallel with the work itself, not as a separate task saved for review season.
- **Numbers visible in the handwritten notes** — Specific figures captured in the moment - the same precision a brag doc entry needs: a specific bug, a specific date, a specific measurable impact, not a vague general impression.

**Building a brag doc that's actually useful months later**

1. **Log an entry close to when it happens, not after the fact** — Specific detail captured in the moment - what happened, when, and its concrete impact.
2. **Include small wins alongside the dramatic ones** — A quiet process improvement often adds up to as much as a single obvious catch, but gets forgotten without a record.
3. **Set a recurring reminder rather than relying on spontaneous memory** — A weekly or biweekly habit produces a far more complete record than sporadic, only-when-obvious entries.
4. **Pull from it directly at review, resume, or promotion time** — Real evidence already captured, not a rushed reconstruction attempt under review-season pressure.

*Flagging brag doc entries too vague to be useful later (Python)*

```python
entries = [
    "Found some good bugs this quarter",
    "Found checkout total bug affecting all users with stacked discount codes, caught before release",
    "Helped with testing",
    "Wrote a test data setup script, saved ~10 min per test run across the team",
]

VAGUE_MARKERS = ["some", "a lot of", "helped with", "various"]

for e in entries:
    lower = e.lower()
    is_vague = any(m in lower for m in VAGUE_MARKERS)
    verdict = "VAGUE - won't hold up months later, rewrite with specifics" if is_vague \\
        else "SPECIFIC - usable as real evidence later"
    print(e + " -> " + verdict)
```

*Flagging brag doc entries too vague to be useful later (Java)*

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> entries = Arrays.asList(
                "Found some good bugs this quarter",
                "Found checkout total bug affecting all users with stacked discount codes, caught before release",
                "Helped with testing",
                "Wrote a test data setup script, saved ~10 min per test run across the team"
        );

        List<String> vagueMarkers = Arrays.asList("some", "a lot of", "helped with", "various");

        for (String e : entries) {
            String lower = e.toLowerCase();
            boolean isVague = vagueMarkers.stream().anyMatch(lower::contains);
            String verdict = isVague
                    ? "VAGUE - won't hold up months later, rewrite with specifics"
                    : "SPECIFIC - usable as real evidence later";
            System.out.println(e + " -> " + verdict);
        }
    }
}
```

### Your first time: Start a real brag doc this week

- [ ] Create one simple running document - a notes app, a plain text file, anything low-friction — The tool matters far less than actually using it consistently.
- [ ] Add three entries right now from the last two weeks — Even if they feel small - a test data fix, a caught edge case, positive feedback received.
- [ ] Set a recurring weekly or biweekly reminder to add anything new — A calendar reminder or recurring task, not reliance on remembering spontaneously.
- [ ] Rewrite any vague entry with a specific detail: what, when, and the concrete impact — Confirm each entry would still make sense read cold, six months from now.

- **A performance review or promotion case feels thinner than the actual year's work deserved.**
  Almost always a missing running record, not a genuinely thin year - start a brag doc now going forward, even without being able to recover everything from the past.
- **Brag doc entries exist but read too vague to actually use in a review or resume.**
  Rewrite each one with the specific what, when, and measurable impact - a vague entry provides almost nothing to draw from later, however well-intentioned the original note was.
- **The habit of logging entries quietly stops after the first few weeks.**
  Attach it to an existing recurring habit (end of each Friday, or a standing weekly reminder) rather than relying on remembering spontaneously - the habit needs a fixed trigger to actually stick.

### Where to check

- The last two weeks of real work, mined for at least two or three entries worth logging right now.
- Existing brag doc entries, reviewed for vague language that would need reconstruction rather than usable specifics.
- [[your-first-90-days/growing-from-here/junior-to-mid-roadmap]] for the concrete capabilities a brag doc's entries can serve as direct evidence for.
- [[resume-and-applications/the-qa-resume/numbers-and-impact]] for turning a brag doc's specific entries into resume-ready, quantified lines.
- [[your-first-90-days/landing-well/building-trust]] for the kind of early, quieter contributions worth logging even before they feel dramatic enough to seem brag-worthy.

### Worked example: a brag doc that turned a vague review into a specific, well-supported case

1. A tester's first attempt at year-end self-review notes reads: "Found several important bugs, helped
   improve the test process, generally had a strong year."
2. Realizing none of it is specific enough to actually cite in a review, the tester starts a brag doc
   from that point forward, logging entries weekly.
3. Three months later, entries include: "caught a checkout total bug affecting all users with stacked
   discounts, pre-release," "wrote a shared test data setup script, cut ~10 min per run across 4
   teammates," and "onboarded a new hire's first week, they were running tests independently by day 3."
4. At the next review, instead of a vague general impression, the tester presents three specific,
   dated entries with concrete impact each.
5. The manager references two of the specific entries directly in the written review - evidence that
   would have been effectively lost to memory without the running record capturing it close to when it
   actually happened.

**Quiz.** According to this note, what's the core reason a brag doc entry needs specific detail rather than a general impression?

- [ ] Specific entries are simply required by most company review templates
- [x] A vague entry like 'found some good bugs' provides almost nothing to draw from months later, while a specific one with what, when, and concrete impact remains genuinely usable evidence at review or resume time
- [ ] Specific entries take less time to write than general ones
- [ ] Vague entries are considered unprofessional regardless of their later usefulness

*The entire value of a brag doc comes from capturing real, usable evidence close to when it happens - a vague entry like 'found some good bugs' could describe almost anything and provides nothing concrete to draw from later. A specific entry with what happened, when, and its measurable impact remains genuinely useful months later, in a way a vague one, or a memory reconstructed from scratch, generally doesn't.*

- **A brag doc** — A running, personal record of work accomplishments logged close to when they happen, so a review, resume update, or promotion case can draw from real evidence instead of an unreliable after-the-fact memory.
- **Why specificity matters in each entry** — A vague entry ('found some good bugs') gives nothing concrete to work with later - a specific one (what, when, measurable impact) stays genuinely usable months later.
- **Why small, unremarkable-feeling wins belong in a brag doc too** — Over a year, quieter contributions often add up to as much as a handful of dramatic catches, but are the most likely entries to be forgotten entirely without a running record.
- **Why starting a brag doc only right before a review defeats its purpose** — The value comes from capturing detail close to when it happened - backfilling months of accomplishments from memory right before a review recreates the exact imprecise conditions the habit exists to avoid.

### Challenge

Start a brag doc today. Add three real entries from the last two weeks, written with specific detail - what happened, when, and the concrete impact - not a general impression.

- [Julia Evans — Get Your Work Recognized: Write a Brag Document](https://jvns.ca/blog/brag-documents/)
- [Workhuman — What Is a Brag Sheet and Why You Need One](https://www.workhuman.com/blog/brag-sheet/)
- [Brag Document Guide: The Career Hack Your Manager Won't Tell You About](https://www.youtube.com/watch?v=wBqiv9A_Vq4)

🎬 [Brag Document Guide: The Career Hack Your Manager Won't Tell You About](https://www.youtube.com/watch?v=wBqiv9A_Vq4) (10 min)

- A brag doc is a running record kept close to when accomplishments happen, so reviews and resumes draw from real evidence instead of a reconstructed memory.
- Specific detail - what, when, concrete impact - is what makes an entry actually usable months later; vague entries give almost nothing to work with.
- Small, quieter wins belong in it too - over a full year they often add up to as much as the dramatic, obvious catches.
- Set a recurring reminder rather than relying on spontaneous memory - a two-minute weekly habit produces a far more complete record.
- Starting a brag doc only right before a review defeats its purpose - the value comes entirely from capturing detail close to when it happened.


## Related notes

- [[Notes/your-first-90-days/growing-from-here/junior-to-mid-roadmap|Junior → mid roadmap]]
- [[Notes/resume-and-applications/the-qa-resume/numbers-and-impact|Numbers & impact]]
- [[Notes/your-first-90-days/landing-well/building-trust|Building trust]]


---
_Source: `packages/curriculum/content/notes/your-first-90-days/growing-from-here/keeping-a-brag-doc.mdx`_
