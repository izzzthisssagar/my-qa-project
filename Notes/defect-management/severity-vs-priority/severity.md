---
title: "Severity"
tags: ["defect-management", "severity-vs-priority", "track-c"]
updated: "2026-07-16"
---

# Severity

*How bad a defect's technical impact is - a fixed, technical judgment about the defect itself, independent of who's asking for it fixed or when the release ships.*

> A typo in a footer link and a checkout flow that charges customers twice are both "bugs," but calling
> them the same size of problem would be absurd. Severity is the answer to one specific question: if
> nobody touches this, how bad is the actual damage? Not how soon someone should fix it — that's the
> next note's question — just how bad the thing itself is, judged on its own technical merits.

> **In real life**
>
> A rust-swollen support wall shows every degree of severity in one glance: a faint stain here is
> cosmetic, a hairline crack there means the cladding is starting to separate, and one corner has
> already sheared off a visible chunk of concrete — a structural failure, not a blemish. Nobody needs
> to know the building's maintenance schedule or budget to rank these; the wall itself, examined
> directly, tells you how bad each spot already is. Severity works the same way — it's a property of
> the defect itself, readable independent of anyone's calendar.

**severity**: Severity is a technical judgment of how much damage a defect causes to the system if left unfixed - crash vs cosmetic, data-loss vs display-only, blocking every user vs affecting an edge case - independent of business timing, deadlines, or who is asking for a fix. A common scale: Critical (system unusable, data loss, security exposure), Major/High (a core feature broken with no workaround), Minor (a feature degraded but usable, or a workaround exists), Trivial/Low (cosmetic, no functional impact). Severity is decided from the defect's own observed impact - it does not become more severe because a VIP customer reported it, which is a priority question, not a severity one.

## The four-level scale, read off the defect itself

- **Critical** — the system crashes, data is lost or corrupted, or there's a real security exposure.
  No workaround exists. Example: a checkout bug that charges a customer's card twice with no way to
  reverse it automatically.
- **Major / High** — a core feature is broken with no reasonable workaround, but the system as a
  whole survives. Example: search returns zero results for any query, but the rest of the app works.
- **Minor** — a feature is degraded or annoying but a workaround exists, or the impact is contained
  to a non-core path. Example: a filter resets unexpectedly, but re-applying it takes one extra click.
- **Trivial / Low** — cosmetic only, no functional impact at all. Example: a misaligned icon, a typo
  in a tooltip nobody reads twice.

> **Tip**
>
> The fastest severity gut-check: ask "does a workaround exist, and does the system stay usable?" A
> crash or unrecoverable data loss with zero workaround is close to automatically Critical. A cosmetic
> issue that never blocks any actual task is close to automatically Trivial. Most real disagreement
> happens in the Major/Minor middle — which is exactly where naming the workaround explicitly (or its
> absence) resolves more arguments than debating adjectives does.

> **Common mistake**
>
> Letting severity drift upward because of WHO reported it, or how loudly. A VIP customer's cosmetic
> complaint is still cosmetic — Trivial severity, however urgently the business wants it addressed. That
> urgency is a real, legitimate signal, but it belongs in the next note's field (priority), not in an
> inflated severity rating. Mixing the two makes severity meaningless as a technical signal, because it
> stops describing the defect and starts describing the org chart.

![A close-up photograph of a tiled retaining wall with rust-stained cladding panels showing different stages of damage - some panels with only faint rust streaks, one panel visibly cracked with a chunk broken off, and a small hand-painted 'PARKING AT OWN RISK' warning sign mounted on the wall](severity.jpg)
*Retaining wall cracking from rust-swollen reinforcing — Wikimedia Commons, CC BY-SA 3.0 (JonRichfield). [Source](https://commons.wikimedia.org/wiki/File:Concrete_wall_cracking_as_steel_reinforcing_corrodes_and_swells_9058.jpg)*
- **A clean, undamaged panel — the baseline** — Same wall, same underlying cause present everywhere, but this specific spot shows nothing yet. Not every defect in the same system is automatically severe just because a related one is.
- **A faint rust streak, no cracking — Trivial** — Cosmetic discoloration only, structurally sound. Severity reads this exactly as it appears: no functional impact, regardless of how it looks.
- **A visible crack with cladding starting to separate — Minor to Major** — Real, visible, worsening damage - but the wall is still standing and doing its job. This is the genuinely debatable middle severity range, where naming the specific observed extent matters more than an adjective.
- **The detached, broken corner — Critical** — A visible structural failure - a chunk of the actual load-bearing material has already sheared off. No workaround restores it; this is damage, not appearance.
- **The warning sign — severity has a real, physical consequence** — 'PARKING AT OWN RISK' exists because the wall's actual condition, examined directly, poses a real risk to whatever sits near it - the same reason a Critical bug gets flagged loudly regardless of anyone's calendar or deadline.

**The same underlying bug, read at four different severities**

1. **Trivial** — A tooltip has a typo. Cosmetic, no functional impact, no workaround needed because nothing is actually broken.
2. **Minor** — A saved filter resets after navigating away. Annoying, but re-applying it costs one extra click - a real workaround exists.
3. **Major** — Search returns zero results for every query. A core feature is fully broken, no workaround - but the rest of the app still works.
4. **Critical** — Checkout charges a customer's card twice with no automatic reversal. Real financial harm, no workaround, the system did the wrong thing with real consequences.
5. **Same wall, four different spots** — All four are real defects in the same product - severity describes how bad EACH ONE is on its own, not how the product is doing overall.

Severity is really just a function from an observed impact (crashes? data loss? workaround exists?)
to one of four levels. Here's a small script that applies exactly that rule, so the same inputs
always produce the same rating instead of relying on a gut call that drifts from person to person.

*Run it - classify defects into severity levels from their observed impact (Python)*

```python
defects = [
    {"id": "BUG-601", "crashes_or_data_loss": True, "workaround_exists": False, "core_feature_broken": True},
    {"id": "BUG-602", "crashes_or_data_loss": False, "workaround_exists": False, "core_feature_broken": True},
    {"id": "BUG-603", "crashes_or_data_loss": False, "workaround_exists": True, "core_feature_broken": False},
    {"id": "BUG-604", "crashes_or_data_loss": False, "workaround_exists": True, "core_feature_broken": False, "cosmetic_only": True},
]

def classify_severity(d):
    if d["crashes_or_data_loss"] and not d["workaround_exists"]:
        return "Critical"
    if d["core_feature_broken"] and not d["workaround_exists"]:
        return "Major"
    if d.get("cosmetic_only"):
        return "Trivial"
    return "Minor"

for d in defects:
    print(f"{d['id']}: {classify_severity(d)}")

# BUG-601: Critical
# BUG-602: Major
# BUG-603: Minor
# BUG-604: Trivial
```

Same classification rule in Java, the kind of deterministic check a tracker's own automation could
apply consistently instead of leaving every rating to individual judgment:

*Run it - classify defects into severity levels from their observed impact (Java)*

```java
import java.util.*;

public class Main {
    record Defect(String id, boolean crashesOrDataLoss, boolean workaroundExists,
                  boolean coreFeatureBroken, boolean cosmeticOnly) {}

    static String classifySeverity(Defect d) {
        if (d.crashesOrDataLoss() && !d.workaroundExists()) return "Critical";
        if (d.coreFeatureBroken() && !d.workaroundExists()) return "Major";
        if (d.cosmeticOnly()) return "Trivial";
        return "Minor";
    }

    public static void main(String[] args) {
        List<Defect> defects = List.of(
            new Defect("BUG-601", true, false, true, false),
            new Defect("BUG-602", false, false, true, false),
            new Defect("BUG-603", false, true, false, false),
            new Defect("BUG-604", false, true, false, true)
        );

        for (Defect d : defects) {
            System.out.println(d.id() + ": " + classifySeverity(d));
        }
    }
}

/* BUG-601: Critical
   BUG-602: Major
   BUG-603: Minor
   BUG-604: Trivial */
```

### Your first time: Your mission: rate five real (or realistic) bugs by severity alone

- [ ] Gather or invent five bugs spanning a real range — Try to genuinely cover all four levels - one obvious Critical, one obvious Trivial, and a couple of debatable Minor/Major cases.
- [ ] For each, answer only three questions — Does it crash or lose data? Does a workaround exist? Is a core feature broken? Resist the urge to factor in who reported it or how urgent it feels.
- [ ] Write the one-line reasoning, not just the label — 'Critical - no workaround, real financial harm' beats a bare 'Critical' - the reasoning is what a stranger actually needs to agree or disagree with your call.
- [ ] Run the Python playground with your own five bugs — Structure them with the same three fields and confirm the script's classification matches your own read.

You now have five real severity ratings you can defend with reasoning, not just a gut adjective.

- **Two people rate the exact same bug at two different severities.**
  Ask each person to state which of the three questions (crashes/data loss? workaround exists? core feature broken?) they answered differently - severity disagreements are almost always a disagreement about one specific fact, not a difference in values.
- **A bug's severity keeps getting bumped up every time a manager asks about it.**
  This is the priority signal leaking into the severity field - the bug's actual technical impact hasn't changed just because attention increased. Keep severity fixed to the defect's own impact and let urgency show up in priority instead (next note).
- **You're not sure whether a workaround 'counts' - it exists but it's clunky and easy to miss.**
  A workaround that a normal user is unlikely to discover or tolerate barely counts - lean toward the higher severity and name the workaround's real limitation explicitly in the ticket ('a workaround exists but requires the user to already know to check the settings menu').
- **A Critical-severity bug sits unfixed for weeks while lower-severity bugs get worked first.**
  This is not automatically wrong - it's exactly what happens when priority (business scheduling) diverges from severity (technical impact), which the next two notes cover directly. Check whether that divergence was a deliberate, documented decision or simply neglect.

### Where to check

- **Your tracker's severity field definitions**, if documented — many teams write down what each level means locally; check it before assuming the generic four-level scale above maps exactly.
- **Past tickets at each severity level** — reading a handful of real Critical vs Major tickets from your own project calibrates your gut faster than any abstract definition.
- **The defect's own reproduction** (see repro-steps and evidence from the previous chapter) — severity should be rated against what you actually observed, not a description of what you assume it implies.
- **Whether a workaround is documented anywhere for users**, if one exists — a workaround that exists but isn't communicated to users functions closer to "no workaround" in practice.

### Worked example: a severity call that resisted social pressure to inflate

1. The CEO personally emails about a typo on the marketing homepage footer, asking that it be treated
   as urgent.
2. The tester rates it: **Trivial severity** — cosmetic only, no functional impact, no workaround
   needed because nothing is broken. The reasoning is written on the ticket plainly.
3. Separately, in the priority field: **High priority** — because the CEO specifically flagged it and
   it's on the public marketing homepage, a real (if non-technical) business reason to fix it soon.
4. Both ratings are honest and defensible at the same time: technically trivial, urgently prioritized.
   Keeping them separate means the severity statistics for the release stay accurate (this wasn't a
   crash), while the ticket still gets worked quickly because of its real, stated priority.
5. If severity had been inflated to "Critical" to match the urgency, the release's severity
   statistics would now falsely suggest a crash-level defect shipped — a genuinely different, wrong
   signal for anyone reading the numbers later without the full story.

**Quiz.** A bug crashes the app for exactly one specific, rarely-used account configuration that affects an estimated 0.1% of users. How should severity be rated?

- [ ] Trivial, since it only affects 0.1% of users
- [x] Critical for the technical impact (a crash, likely no workaround) - severity rates the defect's own impact when it occurs, independent of how many users encounter it; how RARE it is belongs in the priority/scheduling conversation, not the severity rating
- [ ] Minor, as a compromise between the crash and the small affected population
- [ ] It cannot be rated without knowing the business priority first

*This note is explicit that severity is a technical judgment of impact WHEN the defect occurs, independent of business timing or how many people are affected - a crash is a crash for whoever hits it, and severity's job is to describe how bad the defect itself is, not how common the triggering condition is. Option one wrongly imports population size (a priority-shaped concern) into the severity rating. Option three invents an unsupported 'compromise' that isn't how the four-level scale works - severity isn't averaged against likelihood. Option four has severity and priority backwards; severity can and should be rated from the defect's own observed impact alone, and doing so is exactly what lets priority be decided separately and explicitly afterward, which the next two notes cover.*

- **Severity — definition** — A technical judgment of how much damage a defect causes if left unfixed (crash vs cosmetic, workaround or none) - independent of business timing, deadlines, or who reported it.
- **The four-level severity scale** — Critical (crash/data loss/security, no workaround), Major (core feature broken, no workaround), Minor (degraded but a workaround exists), Trivial (cosmetic, no functional impact).
- **The fastest severity gut-check** — Does a workaround exist, and does the system stay usable? No workaround + unusable/lost data trends Critical; cosmetic-only with zero functional impact trends Trivial.
- **Why severity shouldn't rise just because a VIP reported it** — That's a real, legitimate signal - but it belongs in priority (the next note), not severity. Mixing the two makes severity stop describing the defect and start describing the org chart.
- **How to rate severity for a rare-but-crashing bug** — Rate the impact AS IT OCCURS (likely Critical for a crash with no workaround) - how rarely the triggering condition happens is a scheduling/priority question, not a severity one.
- **The debatable middle of the severity scale** — Most real disagreement happens between Minor and Major - resolved faster by naming the SPECIFIC workaround (or its absence) explicitly than by debating adjectives.

### Challenge

Rate the five bugs from your FirstTime exercise above using the fastest gut-check (workaround exists?
system stays usable?) instead of the three-question classifier, and compare your two sets of ratings.
Where they disagree, figure out honestly which method was actually more accurate for that specific
bug. Then open the Python playground, add your five bugs with the three boolean fields, and confirm
the classifier's output matches your considered final rating for each one.

### Ask the community

> I rated this bug as `[your severity]`: `[brief description, crashes/data-loss? workaround? core feature broken?]`. A colleague thinks it should be `[their severity]` instead. Whose read is more defensible, and what's the deciding factor?

Naming the exact three-question answers you each gave (not just the final label) usually resolves
this fast - severity disagreements are almost always a disagreement about one specific observed fact.

- [Guru99 — severity within the defect life cycle](https://www.guru99.com/defect-life-cycle.html)
- [Software Testing Help — severity's role in triage](https://www.softwaretestinghelp.com/defect-triage-process-meeting/)
- [Test IO Community — Bug Severity Levels Explained: Critical vs High vs Low](https://www.youtube.com/watch?v=FvRp0zRRNwI)

🎬 [Bug Severity Levels Explained: Critical vs High vs Low — Test IO Community](https://www.youtube.com/watch?v=FvRp0zRRNwI) (2 min)

- Severity is a technical judgment of a defect's own impact (crash vs cosmetic, workaround or none) - independent of business timing or who reported it.
- Four levels: Critical (unusable/data loss, no workaround), Major (core feature broken, no workaround), Minor (degraded, workaround exists), Trivial (cosmetic only).
- The fastest gut-check: does a workaround exist, does the system stay usable? Most real disagreement lives in the Minor/Major middle, resolved by naming the specific workaround.
- Severity should not inflate because of who reported it or how loudly - that urgency is real, but it belongs in priority, covered next.
- A rare-but-crashing bug still rates by its impact WHEN it occurs - how rarely it triggers is a priority/scheduling question, not a severity one.


## Related notes

- [[Notes/defect-management/severity-vs-priority/priority|Priority]]
- [[Notes/defect-management/severity-vs-priority/combinations|Combinations]]
- [[Notes/defect-management/severity-vs-priority/who-sets-what|Who sets what]]


---
_Source: `packages/curriculum/content/notes/defect-management/severity-vs-priority/severity.mdx`_
