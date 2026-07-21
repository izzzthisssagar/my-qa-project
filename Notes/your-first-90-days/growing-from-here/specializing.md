---
title: "Specializing"
tags: ["your-first-90-days", "growing-from-here", "track-c"]
updated: "2026-07-21"
---

# Specializing

*A street watchmaker's entire table is tiny gears, loupes, and tweezers built for exactly one narrow trade - nothing there would help fix a car or a phone. Specializing in QA means the same trade-off: real depth in one direction, bought with less breadth everywhere else.*

> A generalist QA who can competently test a UI, poke at an API, and write a basic SQL check is
> genuinely valuable - and also directly interchangeable with a large pool of other generalists with the
> same broad-but-shallow profile. Specializing is a deliberate trade: less interchangeability, bought
> with real depth somewhere specific enough that fewer people can match it.

> **In real life**
>
> A street watchmaker's entire workspace is built around one narrow trade: a magnifying loupe headset,
> tweezers fine enough to place a gear a few millimeters wide, tiny brushes and oil for parts most people
> have never seen up close. None of it would help fix a car, rewire a lamp, or repair a phone - the whole
> setup exists because of a deliberate choice to go deep in one specific direction rather than own a
> general-purpose toolkit that does many things adequately. Specializing in QA is the same trade: real
> depth in one area - security, performance, mobile, accessibility - bought with less time spent getting
> broader everywhere else.

**Specializing**: Specializing, in a QA career, means deliberately investing disproportionate time in one specific testing domain - security, performance, accessibility, mobile, or another named area - to build depth that a generalist profile can't match, in exchange for spending comparatively less time broadening skills elsewhere.

## The timing question: specialize too early, and the depth has nothing to stand on

Specializing before building a solid generalist foundation risks depth in a narrow area with no
surrounding context to make it fully useful - a security-focused tester who's never really understood
how the broader QA process works has a harder time explaining findings in terms a team can act on, or
knowing when a security concern should actually block a release versus get logged and scheduled.
Waiting until basic testing competence, common tools, and the fundamentals of how software actually
breaks feel solid gives a specialization somewhere real to attach to - depth on top of a foundation,
not depth instead of one.

## Picking a direction: genuine interest matters as much as market demand

A specialization chosen purely for a market-demand signal, with no real curiosity behind it, is hard to
sustain the deliberate practice that real depth actually requires - staying current in a narrow field
takes ongoing effort, and effort is far easier to sustain in a direction that's genuinely interesting to
begin with. The strongest signal worth trusting: which kind of bug or problem consistently produces
real curiosity rather than just obligation - an accessibility issue that's fascinating to dig into, an
API auth flaw that's satisfying to trace end to end, a performance regression that's oddly compelling to
root-cause. That recurring pull is a better long-term compass than a job-posting keyword count alone.

> **Tip**
>
> Test a specialization direction with a small, real project before committing to it seriously - a
> focused audit of one real app's accessibility, or a small API security review against an
> authorized target. Real engagement with the actual work reveals genuine interest far faster than
> reading about the field in the abstract.

> **Common mistake**
>
> Specializing so narrowly that the broader generalist skills atrophy entirely. The strongest
> specialists usually keep enough breadth to understand how their narrow area connects to the rest of
> the testing process - a security specialist who can't explain a finding in terms the wider team can act
> on has traded away too much surrounding context for the depth gained.

![A street watchmaker wearing a magnifying loupe headset working on tiny watch parts on a folding table](specializing.jpg)
*Watchmaker — Yılmaz Kilim, CC0, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Watchmaker_(184539829).jpeg)*
- **The magnifying loupe headset** — A tool built for exactly one purpose - seeing detail invisible at a normal, generalist scale. Specialization works the same way: instruments and habits calibrated for one narrow domain's specific demands.
- **The scattered tiny watch parts** — Components so specific to one trade that a generalist toolkit has no equivalent use for them - the concrete shape real specialization depth eventually takes.
- **The tweezers and fine tools laid out** — Precision instruments most other trades would never need - deliberately chosen and kept ready because this one narrow domain specifically demands them.
- **The ordinary cars and street in the background** — The broader, general world still surrounding the narrow trade - a reminder that even a deep specialist usually still needs enough context outside their narrow focus to function within it.

**Choosing and testing a specialization direction deliberately**

1. **Build a solid generalist foundation first** — Fundamentals of testing and common tools solid enough that specialization has real context to attach to.
2. **Notice which problems produce genuine curiosity, not just obligation** — A recurring pull toward one kind of bug or domain is a better compass than market-demand keywords alone.
3. **Test the direction with a small, real project before committing** — A focused audit or authorized mini-review reveals genuine engagement faster than reading about the field abstractly.
4. **Keep enough surrounding breadth to stay connected to the wider process** — Depth traded for zero remaining context makes findings harder to communicate to the rest of the team.

*Weighing curiosity signal against market-demand signal for a specialization choice (Python)*

```python
candidates = [
    {"domain": "security testing", "curiosity_score": 9, "market_demand_score": 8},
    {"domain": "performance testing", "curiosity_score": 4, "market_demand_score": 9},
    {"domain": "accessibility testing", "curiosity_score": 8, "market_demand_score": 6},
]

for c in candidates:
    # weighted toward curiosity, since sustained depth needs sustained genuine interest
    weighted = c["curiosity_score"] * 1.5 + c["market_demand_score"]
    c["weighted_score"] = round(weighted, 1)

ranked = sorted(candidates, key=lambda c: c["weighted_score"], reverse=True)
print("Ranked by curiosity-weighted score:")
for c in ranked:
    print("  " + c["domain"] + " -> " + str(c["weighted_score"]))
```

*Weighing curiosity signal against market-demand signal for a specialization choice (Java)*

```java
import java.util.*;

public class Main {
    static class Candidate {
        String domain; double curiosity, marketDemand, weighted;
        Candidate(String domain, double curiosity, double marketDemand) {
            this.domain = domain; this.curiosity = curiosity; this.marketDemand = marketDemand;
            this.weighted = curiosity * 1.5 + marketDemand;
        }
    }

    public static void main(String[] args) {
        List<Candidate> candidates = new ArrayList<>();
        candidates.add(new Candidate("security testing", 9, 8));
        candidates.add(new Candidate("performance testing", 4, 9));
        candidates.add(new Candidate("accessibility testing", 8, 6));

        candidates.sort((a, b) -> Double.compare(b.weighted, a.weighted));

        System.out.println("Ranked by curiosity-weighted score:");
        for (Candidate c : candidates) {
            System.out.println("  " + c.domain + " -> " + c.weighted);
        }
    }
}
```

### Your first time: Test one specialization direction with a real, small project

- [ ] List two or three candidate specialization directions — Security, performance, accessibility, mobile, or another named QA domain.
- [ ] Pick the one that's produced genuine curiosity most consistently so far — Not just the one with the most job postings mentioning it.
- [ ] Run one small, real, authorized project in that direction — An accessibility audit of a real app, a focused API security review against a permitted target.
- [ ] Honestly assess whether the engagement felt sustained or like an obligation — This single signal is worth more than any amount of abstract research about the field.

- **A tester specializes early and struggles to explain findings in terms the rest of the team can act on.**
  A sign the specialization outpaced the generalist foundation underneath it - deliberately rebuild broader context on how the overall testing process and team communication work, alongside the narrow depth already built.
- **A chosen specialization feels like a chore to keep up with despite strong market demand.**
  Revisit the choice honestly - depth sustained purely by demand without real curiosity is hard to keep current; a direction with genuine pull, even with a smaller market, may hold up better long-term.
- **A deep specialist increasingly struggles to collaborate outside their narrow area.**
  Deliberately maintain some generalist breadth alongside the specialization - enough surrounding context to stay connected to the wider process, not depth that's completely isolated from it.

### Where to check

- Recent bugs or problems worked on, checked honestly for which ones produced real curiosity versus just task completion.
- A specific specialization direction, tested against one small real project before any larger commitment.
- [[your-first-90-days/growing-from-here/junior-to-mid-roadmap]] for the generalist foundation a specialization should sit on top of, not replace.
- [[your-first-90-days/growing-from-here/continued-learning]] for the ongoing practice a chosen specialization needs to actually stay current.
- [[a-portfolio-that-gets-interviews/the-3-repo-portfolio/repo-3-api-suite-and-ci]] for turning a real specialization direction into visible, portfolio-ready evidence.

### Worked example: a specialization direction chosen for demand, then honestly reconsidered

1. A tester picks performance testing to specialize in, largely because job postings in that direction
   consistently pay noticeably more in their market.
2. Six months in, staying current with load-testing tools and methodology increasingly feels like an
   obligation - reading documentation without much genuine pull to dig deeper on their own time.
3. Reflecting honestly, the tester notices a different, consistent pattern: accessibility issues
   specifically have repeatedly drawn real curiosity, in small side investigations never officially
   assigned.
4. A small real project - an unpaid, authorized accessibility audit of a friend's side-project app -
   confirms it: the engagement there feels sustained and genuinely interesting, not like a chore.
5. The tester shifts specialization direction toward accessibility, accepting a smaller immediate market
   compared to performance testing, on the reasoning that sustained depth requires sustained genuine
   interest that performance testing clearly wasn't providing.

**Quiz.** According to this note, why does genuine curiosity matter as much as market demand when choosing a specialization direction?

- [ ] Market demand is actually irrelevant and should be ignored entirely when choosing
- [x] Real depth requires sustained deliberate practice over time, and that ongoing effort is far easier to sustain in a direction that produces genuine curiosity than one chosen purely for a demand signal
- [ ] Curiosity guarantees higher pay regardless of the specific domain chosen
- [ ] Market demand for any given specialization never actually changes over time

*Building and maintaining real specialization depth requires ongoing, sustained effort - staying current in a narrow field doesn't happen from a single burst of study. That kind of sustained effort is far easier to keep up when the direction produces genuine curiosity, not just an external demand signal - a specialization chosen purely for market pay with no real interest behind it is much harder to sustain the deliberate practice for.*

- **Specializing (QA career)** — Deliberately investing disproportionate time in one specific testing domain to build depth a generalist profile can't match, trading away comparative breadth elsewhere.
- **Why specializing too early can backfire** — Depth with no generalist foundation underneath has less context to attach to - harder to explain findings in terms the wider team can act on, or judge how a narrow finding fits the bigger picture.
- **The strongest signal for choosing a direction** — Which kind of problem consistently produces genuine curiosity rather than just obligation - a better long-term compass than market-demand keywords alone.
- **Why keeping some generalist breadth still matters after specializing** — The strongest specialists retain enough surrounding context to connect their narrow area back to the wider testing process - depth with zero remaining breadth isolates a specialist from the team around them.

### Challenge

List two or three candidate specialization directions. Run one small, real, authorized project in whichever one has produced the most genuine curiosity so far, and honestly assess whether the engagement felt sustained or like an obligation.

- [Indeed — Generalist vs. Specialist: What's the Difference?](https://www.indeed.com/career-advice/finding-a-job/generalist-vs-specialist)
- [Test Automation University — Free Courses Across Testing Specialties](https://testautomationu.applitools.com/)
- [Specialize or Generalize - Niche or Broad - What to do when picking a field | The Futur](https://www.youtube.com/watch?v=TmPHqX2P3vM)

🎬 [Specialize or Generalize - Niche or Broad - What to do when picking a field | The Futur](https://www.youtube.com/watch?v=TmPHqX2P3vM) (8 min)

- Specializing is a deliberate trade-off: real depth in one direction, bought with less breadth everywhere else.
- Build a solid generalist foundation before specializing - depth with no surrounding context is harder to communicate and apply well.
- Genuine, recurring curiosity toward a specific kind of problem is a better long-term compass than market-demand keywords alone.
- Test a specialization direction with one small, real, authorized project before fully committing to it.
- Keep enough generalist breadth alongside a specialization to stay connected to the wider testing process, not isolated from it.


## Related notes

- [[Notes/your-first-90-days/growing-from-here/junior-to-mid-roadmap|Junior → mid roadmap]]
- [[Notes/your-first-90-days/growing-from-here/continued-learning|Continued learning]]
- [[Notes/a-portfolio-that-gets-interviews/the-3-repo-portfolio/repo-3-api-suite-and-ci|Repo 3: API suite + CI]]


---
_Source: `packages/curriculum/content/notes/your-first-90-days/growing-from-here/specializing.mdx`_
