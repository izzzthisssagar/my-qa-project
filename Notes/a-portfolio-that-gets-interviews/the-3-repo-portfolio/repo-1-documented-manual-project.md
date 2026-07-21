---
title: "Repo 1: documented manual project"
tags: ["a-portfolio-that-gets-interviews", "the-3-repo-portfolio", "track-e"]
updated: "2026-07-20"
---

# Repo 1: documented manual project

*Turn one manual-testing effort into portfolio evidence: a short test plan, a handful of well-written test cases, and one real bug report with reproduction steps and proof, organized so a stranger can follow your thinking unassisted.*

> A hiring manager opens a GitHub profile and gives it roughly nine seconds before deciding whether to
> keep reading. A folder of test cases scattered across a personal notes app, a spreadsheet, and three
> screenshots buried in Downloads proves nothing in nine seconds. One small, deliberately organized
> repository - a short plan, a handful of well-written cases, one real bug reported end to end - proves
> structured manual thinking in exactly the time available.

> **In real life**
>
> A certified weather station never reports "kind of windy today." It follows a fixed instrument
> standard, in a specific enclosure, at a specific height, on a fixed schedule, so a climatologist
> decades later - someone who was never there - can trust the number and compare it against a reading
> taken on the other side of the world. A manual-testing portfolio project earns the same trust the
> same way: the format is fixed and a little boring on purpose, so a reviewer who has never met you can
> believe what it says without asking a single clarifying question.

**Documented manual project**: A documented manual project is a small, self-contained repository that demonstrates manual QA thinking end to end: a short test plan naming scope and risk, a handful of well-structured test cases, and at least one real, fully evidenced bug report - organized so a reviewer can verify the work without a live walkthrough or any extra explanation from you.

## Pick a target worth testing

Choose a small, stable public target: one of this platform's own practice apps (BuggyShop for a
shopping flow, or TaskFlight through its UI rather than its API), or another public demo site built
for practice. Scope down hard. One flow - checkout, account creation, search and filter - tested well
beats an entire application tested shallowly. Write the scope down in one short paragraph before
writing a single case, so a reader knows what you did NOT cover, and why that boundary was a decision
and not an oversight.

## What actually goes in the repo

A README that orients a stranger in thirty seconds (its own topic later in this chapter), a short test
plan naming what is in scope, what is out, and the two or three biggest risks, five to fifteen test
cases covering the happy path plus the edge cases that actually matter, and folders that make sense on
first glance - `test-plan/`, `test-cases/`, `bug-reports/` reads clearer than one unlabeled folder
called `docs`. Consistency across every artifact - the same fields, the same format, every time - reads
as competence. A different layout for every case reads as improvisation.

## Write the one bug report that counts

Pick a real defect: a seeded bug in a practice app, or a genuine one found by exploring on your own.
Report it completely - exact steps to reproduce, expected result, actual result, environment, and
evidence such as a screenshot, a short screen recording, or a copied response body. One report at this
level of completeness demonstrates more than twenty one-line complaints ever could. Reviewers read a
bug report as a proxy for how someone will actually behave on a real team, under a real deadline, when
nobody is checking their work line by line.

> **Tip**
>
> Match the fields of your bug report to a format reviewers already recognize - Summary, Steps to
> Reproduce, Expected, Actual, Environment, Evidence - instead of inventing your own structure. A
> recognizable format lets a reviewer skim it in seconds rather than decoding your personal system first.

> **Common mistake**
>
> Do not pad the repository with dozens of trivial test cases to look thorough. A reviewer skims; forty
> near-duplicate cases for the same field read as busywork, not rigor. Fifteen well-chosen cases with a
> visible risk-based rationale beat eighty generated from a template nobody thought about.

![A white louvered Stevenson screen instrument shelter on a metal stand in front of a Victorian-era weather station building with an octagonal observation tower topped by a weather vane](repo-1-documented-manual-project.jpg)
*Stevenson screen for South Shields Weather Station - Wikimedia Commons, CC BY-SA 2.0. [Source](https://commons.wikimedia.org/wiki/File:Stevenson_screen_for_South_Shields_Weather_Station_-_geograph.org.uk_-_2937031.jpg)*
- **One fixed enclosure design, used everywhere** — The louvered box is a shared standard, not a personal preference - the same reason a bug report should use the same six fields every single time instead of a fresh layout per report.
- **The station behind it - one documented process** — A real station runs the identical procedure on every visit. A portfolio project earns the same trust by keeping its test-plan and test-case format identical across every artifact in the repo.
- **The weather vane - a second, different measurement** — Temperature alone is not a weather report; wind direction is recorded too. A bug report with only a screenshot and no reproduction steps is the temperature without the wind - one data point standing in for a full account.
- **The fence and gate - a controlled record** — Access to the station and its readings is controlled and traceable. A portfolio repo's commit history is the same kind of evidence: it shows the work happened over real time, not all at once the night before an interview.

**Building one documented manual project**

1. **Pick one small, stable target and scope it in writing** — Name what is in scope, what is out, and why - before writing a single case.
2. **Write a short plan and well-structured cases** — Same fields every time; a handful of well-chosen cases beats dozens of near-duplicates.
3. **File one real bug report, completely** — Steps, expected, actual, environment, and evidence - the artifact reviewers read closest.
4. **Organize the repo so a stranger can verify it** — Clear folders, an orienting README, and commit history that shows real work over time.

*A documented-project completeness checker (Python)*

```python
required_folders = ["readme", "test-plan", "test-cases", "bug-reports"]
repo = {
    "readme": True,
    "test-plan": True,
    "test-cases": True,
    "bug-reports": True,
}
missing_folders = [f for f in required_folders if not repo.get(f)]

bug_report = {
    "summary": "Checkout button stays disabled after a valid coupon is applied",
    "steps_to_reproduce": "1. Add item 2. Apply coupon SAVE10 3. Observe Checkout button",
    "expected": "Checkout button becomes enabled once the coupon is accepted",
    "actual": "Checkout button remains disabled",
    "environment": "Chrome 126, BuggyShop staging, desktop",
    "evidence": "screenshot-checkout-disabled.png",
}
required_fields = ["summary", "steps_to_reproduce", "expected", "actual", "environment", "evidence"]
missing_fields = [f for f in required_fields if not bug_report.get(f)]

checks = {
    "repo_structure_complete": len(missing_folders) == 0,
    "bug_report_complete": len(missing_fields) == 0,
}
for name, passed in checks.items():
    print(name + "=" + ("PASS" if passed else "FAIL"))
result = "PASS" if all(checks.values()) else "FAIL"
assert result == "PASS", "documented manual project rejected"
print("RESULT=" + result)
```

*A documented-project completeness checker (Java)*

```java
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Arrays;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<String> requiredFolders = Arrays.asList("readme", "test-plan", "test-cases", "bug-reports");
        Map<String, Boolean> repo = new LinkedHashMap<>();
        repo.put("readme", true);
        repo.put("test-plan", true);
        repo.put("test-cases", true);
        repo.put("bug-reports", true);
        boolean repoComplete = true;
        for (String f : requiredFolders) {
            if (!repo.getOrDefault(f, false)) repoComplete = false;
        }

        Map<String, String> bugReport = new LinkedHashMap<>();
        bugReport.put("summary", "Checkout button stays disabled after a valid coupon is applied");
        bugReport.put("steps_to_reproduce", "1. Add item 2. Apply coupon SAVE10 3. Observe Checkout button");
        bugReport.put("expected", "Checkout button becomes enabled once the coupon is accepted");
        bugReport.put("actual", "Checkout button remains disabled");
        bugReport.put("environment", "Chrome 126, BuggyShop staging, desktop");
        bugReport.put("evidence", "screenshot-checkout-disabled.png");
        List<String> requiredFields = Arrays.asList("summary", "steps_to_reproduce", "expected", "actual", "environment", "evidence");
        boolean bugComplete = true;
        for (String f : requiredFields) {
            String v = bugReport.get(f);
            if (v == null || v.isEmpty()) bugComplete = false;
        }

        Map<String, Boolean> checks = new LinkedHashMap<>();
        checks.put("repo_structure_complete", repoComplete);
        checks.put("bug_report_complete", bugComplete);
        boolean ok = true;
        for (Map.Entry<String, Boolean> e : checks.entrySet()) {
            System.out.println(e.getKey() + "=" + (e.getValue() ? "PASS" : "FAIL"));
            ok &= e.getValue();
        }
        String result = ok ? "PASS" : "FAIL";
        if (!result.equals("PASS")) throw new AssertionError("documented manual project rejected");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Ship your first documented manual project

- [ ] Pick one small, stable flow and write the scope down first — Name what's in scope, what's out, and the top risks in a single short paragraph.
- [ ] Write five to fifteen test cases in one consistent format — Same fields every time: ID, title, steps, expected result, priority.
- [ ] File one bug completely, with evidence attached — Steps to reproduce, expected, actual, environment, and a screenshot or recording.
- [ ] Organize the repo and commit the work over real time — Clear folders, an orienting README, and more than one commit dated across more than one day.

- **The repo has forty test cases and a reviewer's eyes glaze over by case six.**
  Cut to the fifteen that actually matter and add one paragraph explaining the risk-based reasoning behind the selection - reviewers reward visible judgment over volume.
- **The single bug report has a screenshot but no reproduction steps.**
  Add exact numbered steps, expected result, and actual result. A screenshot alone forces the reader to guess what you did; it does not prove you could reproduce it on demand.
- **Every commit is dated the same night, hours before you started applying.**
  This is a signal reviewers notice. Build the project over several real sessions and commit as you go - the history is itself evidence of sustained, structured work.

### Where to check

- The repo's own folder structure, viewed exactly as a stranger would land on it from the profile page.
- The commit history (`git log --oneline`) for evidence of real work spread over time, not one dump.
- [[a-portfolio-that-gets-interviews/the-3-repo-portfolio/readmes-that-sell]] for how the README should introduce this exact repo in the first screen.
- [[defect-management/writing-bug-reports/anatomy-of-a-report]] for the full six-field bug report anatomy this project should follow.

### Worked example: one seeded bug, reported completely

1. Exploring BuggyShop's checkout, a tester notices the Checkout button stays disabled after a valid
   coupon is applied - the discount shows in the order summary, but the button never re-enables.
2. They reproduce it twice more, varying only the coupon code, to rule out a fluke.
3. The bug report names exact steps, expected behavior, actual behavior, browser and app version, and
   attaches a short screen recording showing the disabled button after the discount appears.
4. The report sits in `bug-reports/` next to two others, all in the identical six-field format, so a
   reviewer can compare all three in under a minute.

**Quiz.** What single change most increases a documented manual project's credibility to a reviewer?

- [ ] Adding as many test cases as possible
- [ ] Using a unique, personalized format for each artifact
- [x] Consistent structure across artifacts plus one fully evidenced bug report
- [ ] Removing the bug report so nothing looks unfinished

*Reviewers skim. A consistent, recognizable format across every artifact plus one bug report that is genuinely complete - steps, expected, actual, environment, evidence - proves more in less reading time than volume or novelty ever could.*

- **What belongs in a documented manual project repo** — An orienting README, a short scoped test plan, five to fifteen consistent test cases, and at least one fully evidenced bug report.
- **Why format consistency matters here** — A reviewer skims in seconds; the same fields every time let them verify quality without first decoding a personal system.
- **The weather-station standard** — A trustworthy record follows a fixed, boring-on-purpose format so a stranger who was never there can trust it without asking you anything.

### Challenge

Scope one small flow in a practice app, write a plan and ten test cases in one consistent format, then file one bug report with full reproduction steps and attached evidence.

- [Software Testing Help - How to write a good bug report](https://www.softwaretestinghelp.com/how-to-write-good-bug-report/)
- [Guru99 - How to write a test case (with template)](https://www.guru99.com/test-case.html)
- [How To Create Automation Tester Portfolio (To Fetch Job Easily)](https://www.youtube.com/watch?v=wgPg6AqI6u8)

🎬 [How To Create Automation Tester Portfolio (To Fetch Job Easily)](https://www.youtube.com/watch?v=wgPg6AqI6u8) (10 min)

- One small, well-scoped manual project beats a sprawling, half-finished one.
- Consistent structure across every artifact reads as competence; a fresh format each time reads as improvisation.
- One bug report with complete reproduction steps and real evidence outweighs a pile of one-line complaints.
- Commit history spread over real time is itself evidence the work is genuine.


## Related notes

- [[Notes/a-portfolio-that-gets-interviews/the-3-repo-portfolio/repo-2-ui-automation-suite|Repo 2: UI automation suite]]
- [[Notes/test-artifacts/test-plans-and-strategy/whats-in-a-plan|What's in a plan]]
- [[Notes/defect-management/writing-bug-reports/anatomy-of-a-report|Anatomy of a report]]
- [[Notes/version-control-with-git/why-version-control/repositories|Repositories]]


---
_Source: `packages/curriculum/content/notes/a-portfolio-that-gets-interviews/the-3-repo-portfolio/repo-1-documented-manual-project.mdx`_
