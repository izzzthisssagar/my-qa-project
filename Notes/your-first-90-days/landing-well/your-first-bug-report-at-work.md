---
title: "Your first bug report at work"
tags: ["your-first-90-days", "landing-well", "track-c"]
updated: "2026-07-20"
---

# Your first bug report at work

*Why the first bug report at a new job is a credibility moment: over-index on clarity, reproduction steps, and calibrated severity rather than volume, and learn the team's existing bug-report conventions before deviating from them.*

> Nobody remembers your fiftieth bug report. Several people remember your first one, and quietly form
> an opinion about whether your name on a ticket means "read this carefully" or "double-check this
> first." That opinion is expensive to change later and nearly free to get right now.

> **In real life**
>
> A cub reporter's first byline gets fact-checked line by line before it runs, not because the editor
> distrusts them personally, but because nobody yet knows whether this new name means careful work.
> One clean, accurate, well-sourced story earns looser editing on the second one. One sloppy story
> earns scrutiny for months.

**Report credibility**: Report credibility is the reputation effect created by a new team member's first few pieces of written work. It is earned through demonstrated clarity and accuracy rather than assumed from a job title, and it directly determines how closely a person's future reports get double-checked.

## Clarity beats volume on report one

A new QA who files ten vague bug reports in their first week teaches the team to skim their tickets.
A new QA who files two reports with an exact title, precise reproduction steps, and a clearly stated
expected-versus-actual result teaches the team to trust the next one without re-verifying it first.
Volume is not the signal that matters yet — clarity is.

## Calibrate severity before you assign it

An inflated severity on your first bug reads as either inexperience or an attempt to force priority
through drama; both cost credibility. Look at how the team has historically rated similar issues, ask
if you are unsure, and pick the severity you can defend line by line if someone questions it.

> **Tip**
>
> Before filing your first bug, find three existing tickets this team closed as "good examples" — ask
> a teammate directly which ones they would want to see repeated. Match that format exactly for your
> first few reports, then adapt once you understand why it looks that way.

> **Common mistake**
>
> Do not assume your last team's bug-report template, severity scale, or tone is the correct one here.
> A report that looks perfectly professional by your old standards can still read as ignoring this
> team's conventions — and a new hire's very first artifact is the worst moment to look like they did
> not bother to check first.

![A black-and-white 1940s newsroom with several men reading wire copy and paper strips, one typing at a desk, a wall clock, world maps, and a rack of rolled newspapers](your-first-bug-report-at-work.jpg)
*Journalists in the Radio-Canada/CBC newsroom, Montreal — Conrad Poirier, Wikimedia Commons, public domain. [Source](https://commons.wikimedia.org/wiki/File:CBC_journalists_in_Montreal.jpg)*
- **The clock everyone can check against** — Precise timing turns a vague complaint into evidence. Exact timestamps, versions, and environments do for a bug report what the clock does here — they let anyone verify the account independently.
- **Rolled copy in an established house format** — Every one of these newspapers already follows its own house style before a new writer ever touches it. A team's existing bug-report format is the same kind of precedent — learn it before you deviate from it.
- **The first draft, still being typed** — This is the moment before anyone else has seen the work — every word of it is about to be read closely. A first bug report gets exactly this level of attention, whether the author expects it or not.
- **The room that will read it before it ships** — Several people here are checking copy before it goes out, not just one editor. A new report gets cross-checked by more eyes than a veteran's does, which is exactly why clarity matters most on the first one.

**Filing a credible first bug report**

1. **Learn this team's existing conventions first** — Find and match a few reports the team already considers good examples before you file your own.
2. **Write an exact, specific title** — Name what failed and under what condition, not a vague symptom.
3. **Give precise, numbered reproduction steps** — Anyone on the team should be able to follow them without asking a clarifying question.
4. **Calibrate severity against real precedent** — Rate it the way similar issues have historically been rated here, and be ready to defend the choice.

*A bug-report quality checker (Python)*

```python
report = {
    "clear_title": True,
    "numbered_repro_steps": True,
    "expected_vs_actual": True,
    "environment_details": True,
    "calibrated_severity": True,
    "matches_team_conventions": True,
}
missing = []
for field, present in report.items():
    print(field + "=" + ("PASS" if present else "FAIL"))
    if not present:
        missing.append(field)
result = "CREDIBLE" if not missing else "NEEDS_REVISION"
assert result == "CREDIBLE", "bug report missing: " + ", ".join(missing)
print("RESULT=" + result)
```

*A bug-report quality checker (Java)*

```java
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
public class Main {
    public static void main(String[] args) {
        Map<String, Boolean> report = new LinkedHashMap<>();
        report.put("clear_title", true);
        report.put("numbered_repro_steps", true);
        report.put("expected_vs_actual", true);
        report.put("environment_details", true);
        report.put("calibrated_severity", true);
        report.put("matches_team_conventions", true);
        List<String> missing = new ArrayList<>();
        for (var e : report.entrySet()) {
            System.out.println(e.getKey() + "=" + (e.getValue() ? "PASS" : "FAIL"));
            if (!e.getValue()) missing.add(e.getKey());
        }
        String result = missing.isEmpty() ? "CREDIBLE" : "NEEDS_REVISION";
        if (!result.equals("CREDIBLE")) throw new AssertionError("bug report missing: " + String.join(", ", missing));
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: File your first bug report on a new team

- [ ] Find two or three reports this team already considers good — Ask a teammate directly, rather than guessing from the template alone.
- [ ] Match their format for title, steps, and severity — Save your own preferred format for once you understand why theirs looks the way it does.
- [ ] Reproduce the issue at least twice before filing — A first report that turns out to be unreproducible costs more credibility than a slightly late one.
- [ ] State expected versus actual result explicitly — Do not make the reader infer what should have happened instead.

- **Your first bug report gets reassigned as 'not a bug' or 'works as intended'.**
  Ask directly what the expected behavior actually is here before filing the next one, rather than guessing again from your own assumptions.
- **A teammate quietly rewrites your report before triage.**
  Ask to see the rewritten version and what specifically changed. This is free, direct feedback on the team's real conventions.
- **You are unsure whether an issue is Critical or Minor.**
  Look up how the last two similar-looking issues were rated on this team, and match that precedent rather than guessing from a general rubric.

### Where to check

- The bug tracker's recently closed tickets, read specifically for format and tone rather than content.
- A direct question to a teammate about which past reports they consider good examples.
- The team's severity or priority definitions, if documented, and how they were actually applied recently.
- [[your-first-90-days/landing-well/building-trust]] for how early reports compound into a broader pattern of trust over time.

### Worked example: the report that matched the room

1. A new QA finds a checkout bug on day four and drafts a report using her old team's template.
2. Before filing, she checks two recently closed tickets and notices this team always states the exact
   order ID and timestamp in the first line, not the last.
3. She rewrites her draft to match that convention, keeps her precise repro steps, and rates it against
   a similar ticket from last month rather than her own instinct.
4. It is triaged and confirmed within the hour, with no follow-up questions.

**Quiz.** What should a new QA prioritize most in their very first bug report on a new team?

- [ ] Filing as many bugs as possible in the first week
- [x] Clarity, precise reproduction steps, and severity calibrated to this team's precedent
- [ ] Using the exact template from their previous employer
- [ ] Marking every issue as high severity to ensure it gets attention

*The first report is judged on trustworthiness, not volume. Clarity and calibrated severity build the credibility that makes every later report easier to trust.*

- **Why the first report matters more** — It sets a team's expectation for how closely to double-check everything with that person's name on it, before any other evidence exists.
- **Calibrated severity** — A severity rating matched to how the team has historically rated similar issues, defensible line by line, rather than inflated to force attention.
- **Match before you deviate** — Learn a team's existing bug-report conventions and follow them first; propose changes only once you understand why they exist.

### Challenge

Find a bug report your current or most recent team considers a good example. List the three specific things about its format you would copy exactly in your own first report.

- [BrowserStack — How to Write an Effective Bug Report](https://www.browserstack.com/guide/how-to-write-a-bug-report)
- [Marker.io — How to Write a Bug Report (Step-By-Step Guide)](https://marker.io/blog/how-to-write-bug-report)
- [How to Write a Good Bug Report (Step-by-Step Guide + Real Examples)](https://www.youtube.com/watch?v=QlSJCCctsnw)

🎬 [How to Write a Good Bug Report (Step-by-Step Guide + Real Examples)](https://www.youtube.com/watch?v=QlSJCCctsnw) (4 min)

- The first bug report is a credibility moment, judged more on clarity than volume.
- Calibrate severity against this team's actual precedent, not instinct or a previous employer's scale.
- Learn a team's existing bug-report conventions before deviating from them.
- Trustworthy early reports earn looser scrutiny on every report that follows.


## Related notes

- [[Notes/your-first-90-days/landing-well/onboarding-as-a-qa|Onboarding as a QA]]
- [[Notes/your-first-90-days/landing-well/learning-the-product-fast|Learning the product fast]]
- [[Notes/your-first-90-days/landing-well/building-trust|Building trust]]


---
_Source: `packages/curriculum/content/notes/your-first-90-days/landing-well/your-first-bug-report-at-work.mdx`_
