---
title: "Continuous testing"
tags: ["agile-and-devops-for-testers", "shift-left-and-cicd", "continuous-testing"]
updated: "2026-07-20"
---

# Continuous testing

*Testing continuously across the whole pipeline instead of as one late phase - fast smoke tests on every commit, a fuller nightly regression run, and production monitoring treated as testing that never stops.*

> Ask an old-school QA team when testing happens and they'll point at a phase near the end of a release
> calendar - a block of weeks with "Testing" written on it, after development is done. Ask a team practicing
> continuous testing the same question and they'll struggle to answer, because for them testing isn't a phase
> at all. It's running on every commit, again every night, and again quietly against production while nobody's
> watching - all at once, all the time, none of it waiting for a calendar block that says it's now allowed to
> start.

> **In real life**
>
> A hospital doesn't check a patient's vital signs once at admission and call the checking done. A bedside
> monitor reads heart rate, oxygen, and blood pressure continuously, second by second, for as long as the
> patient is connected to it - not because any single reading matters that much on its own, but because a
> sudden change is only visible if something was watching a moment ago too. A quick pulse check at the door is
> still useful on its own - it catches an obvious emergency fast - but it's not a substitute for the monitor
> that keeps watching afterward. Continuous testing works the same way: a fast check on every commit catches
> the obvious break immediately, a deeper nightly run catches what the fast check can't afford to check every
> time, and monitoring the running system in production is the bedside monitor that never gets unplugged,
> watching for the change that only shows up once real traffic hits it.

**Continuous testing**: Continuous testing is the practice of running automated tests at every stage of the software delivery pipeline - on every commit, on a recurring schedule, and even after release via production monitoring - rather than treating testing as one dedicated phase that happens only after development is complete.

## Three cadences, not one big phase

Continuous testing typically runs at three different speeds, each catching something the others can't
afford to. **Smoke tests on every commit** are a small, fast subset of checks - can the application start,
can a user log in, does the core happy path still work - that run automatically on every single push,
finishing in minutes so a developer gets feedback before they've mentally moved on to something else.
**Nightly regression** is the fuller suite: hundreds or thousands of tests covering edge cases, older
features, and cross-feature interactions that would be far too slow to run on every commit, scheduled to run
on a recurring cadence instead - often overnight, when the extra time doesn't block anyone. **Production
monitoring** is testing that never technically ends: synthetic checks that repeatedly exercise real user
flows against the live system, canary deployments that watch a small slice of real traffic before a full
rollout, and alerting on real error rates or latency - all of it functioning as a continuous, automated
verification that the system still actually works, running against reality itself instead of a staging copy
of it.

## Why production monitoring counts as testing

It's tempting to draw a hard line between "testing" (something QA does before release) and "monitoring"
(something ops does after release), but continuous testing treats that line as mostly artificial. A synthetic
check that logs in and completes a checkout flow against production every five minutes is functionally a
test - it has a fixed set of steps, an expected outcome, and it fails loudly when reality doesn't match the
expectation. The only real difference from a pre-release test is what it's running against: a synthetic
staging environment versus the actual system real users depend on right now. Treating production monitoring
as a genuine form of testing - not a separate discipline owned entirely by a different team - is what closes
the loop: staging can never perfectly predict what real user behavior, real data volume, and real third-party
services will do, so the verification has to keep running after release too, not stop the moment a deploy
succeeds.

> **Tip**
>
> When deciding which cadence a new test belongs in, ask how expensive it is versus how urgently a failure
> needs to be known. A check that takes under a second and covers a critical path belongs in the on-commit
> smoke suite. A check that takes minutes and covers an edge case belongs in nightly regression. A check that
> can only be meaningfully verified against real traffic or real data belongs in production monitoring - it
> was never going to be caught earlier no matter how much pre-release testing ran.

> **Common mistake**
>
> Treating continuous testing as "run the full regression suite on every single commit." That's not
> continuous testing, it's just slow testing running more often - developers wait longer for feedback on every
> push, the pipeline backs up, and people start pushing several commits before checking results, which quietly
> defeats the entire point of fast, frequent feedback. The speed difference between cadences is the whole
> mechanism, not an afterthought.

![A Philips IntelliVue hospital patient monitor mounted on a wall arm, showing its main display screen, a row of modular measurement bays below it with several plugged-in modules, a small red warning tag on a cable connector, and coiled cables hanging on hooks underneath](continuous-testing.jpg)
*ICU Monitor (front) - Quinn Dombrowski, Wikimedia Commons, CC BY-SA 2.0. [Source](https://commons.wikimedia.org/wiki/File:ICU_Monitor_(front).jpg)*
- **The always-on display** — Even powered down between patients here, this is the one screen a clinician glances at continuously - not a report compiled once a shift. A continuous testing dashboard works the same way: checked constantly, not read once per sprint.
- **Several modules plugged in and running together** — Multiple separate measurement modules sit side by side, each checking something different, all live at once - like a pipeline running smoke tests, nightly regression, and production monitoring simultaneously instead of one at a time.
- **A warning tag hanging right on the equipment** — A physical do-not-discard tag on a cable is how this system forces a human to notice something before it gets lost - the same job as an alert that pages someone the moment a production canary check fails, not a report read next week.
- **Cables coiled and ready before they're needed** — These leads are already plugged in and hung on hooks, ready for whichever patient needs them next - not stored away and fetched on request. Continuous testing keeps its checks similarly always-armed, running whether or not anyone asked for a test run today.

**One change, tested at every cadence - press Play**

1. **Commit pushed** — A fast smoke suite runs immediately - core happy paths only, finishing in minutes so the developer gets feedback before moving on to something else.
2. **That night, regression runs** — A much fuller suite runs on a schedule, covering edge cases and older features too slow to check on every single commit.
3. **Release goes out** — The build that survived both cadences ships - but continuous testing doesn't stop here, it changes shape instead of ending.
4. **Production, continuously** — Synthetic checks and real traffic monitoring keep verifying the system against reality itself, catching what no staging environment could have predicted.

Here is a small continuous testing status check: it evaluates each cadence and reports the first one that's
unhealthy - notice production monitoring is checked here exactly the same way the earlier cadences are, not
treated as a separate concern outside of testing.

*A continuous testing status check (Python)*

```python
checks = [
    ("smoke_test", "every_commit", True),
    ("regression_suite", "nightly", True),
    ("production_monitor", "continuous", False),
]

def check(name, cadence, healthy):
    print(name.upper() + "=" + ("HEALTHY" if healthy else "ALERT") + " cadence=" + cadence)
    return healthy

results = [check(name, cadence, healthy) for name, cadence, healthy in checks]
result = "PASS" if all(results) else "FAIL"
assert result == "FAIL", "expected the production monitor to raise an alert"
print("RESULT=" + result)
```

*A continuous testing status check (Java)*

```java
import java.util.*;

public class Main {
    static class Check {
        String name;
        String cadence;
        boolean healthy;
        Check(String name, String cadence, boolean healthy) {
            this.name = name;
            this.cadence = cadence;
            this.healthy = healthy;
        }
    }

    static boolean check(Check c) {
        System.out.println(c.name.toUpperCase() + "=" + (c.healthy ? "HEALTHY" : "ALERT") + " cadence=" + c.cadence);
        return c.healthy;
    }

    public static void main(String[] args) {
        List<Check> checks = new ArrayList<>();
        checks.add(new Check("smoke_test", "every_commit", true));
        checks.add(new Check("regression_suite", "nightly", true));
        checks.add(new Check("production_monitor", "continuous", false));

        boolean allHealthy = true;
        for (Check c : checks) {
            allHealthy &= check(c);
        }
        String result = allHealthy ? "PASS" : "FAIL";
        if (!result.equals("FAIL")) throw new AssertionError("expected the production monitor to raise an alert");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Mapping a team's continuous testing setup for the first time

- [ ] Find what runs on every commit — Ask specifically for the smoke or fast-check suite name and its typical run time - if nothing runs on every commit, that's your first finding.
- [ ] Find what runs on a schedule instead — Look for a nightly or recurring job separate from the on-commit pipeline, and how long it actually takes to finish.
- [ ] Find out whether production is monitored as testing — Ask whether synthetic checks or canary monitoring exist against the live system, and who gets paged when they fail - if the answer is 'that's an ops thing,' the two disciplines aren't connected yet.
- [ ] Check whether cadences are actually separated — Confirm the full regression suite doesn't also run on every commit - if it does, the team likely has one slow phase wearing continuous testing's name, not three real cadences.

- **Developers stopped waiting for pipeline results because every commit triggers the full, slow test suite.**
  Split the suite: a small, fast smoke subset on every commit, and the full suite moved to a nightly or scheduled run instead. Feedback speed is what makes on-commit testing worth having at all.
- **A production incident happened that no test ever would have caught, and nobody was watching for it either.**
  This is a gap in the third cadence, not a reason to write more pre-release tests. Add a synthetic check or monitoring alert for that specific failure mode against the live system - some things only manifest under real traffic.
- **QA owns pre-release testing and a separate ops team owns production monitoring, with no shared visibility into either.**
  Treat production monitoring as a genuine testing cadence, not a separate discipline - get testers visibility into what's monitored and why, and get whoever owns monitoring involved when new features ship with new failure modes to watch for.

### Where to check

- The pipeline configuration for what actually runs on every commit versus what's scheduled separately - the real cadences, not a description of intended process.
- Whatever synthetic monitoring or canary checks exist against production, and whether a tester has ever seen what they check.
- The last production incident that no pre-release test caught - was it a gap that could only ever be caught by monitoring, or a gap a nightly regression run should have caught first?
- [[agile-and-devops-for-testers/shift-left-and-cicd/quality-gates]] for what actually decides pass or fail within any one of these cadences.
- [[agile-and-devops-for-testers/shift-left-and-cicd/the-cicd-pipeline]] for where the on-commit and scheduled cadences physically run.

### Worked example: the outage a synthetic check would have caught in minutes

1. **The setup:** A third-party payment provider starts silently rejecting a specific card type. All
   pre-release tests use test-mode credentials that never touch this code path, so nothing in the pipeline
   ever exercises it.
2. **What actually happens:** Real customers start failing checkout for two hours before a support ticket
   volume spike gets anyone's attention - no test, smoke or regression, was ever going to catch a live
   third-party behavior change.
3. **The root cause:** The team had smoke tests and nightly regression, both genuinely useful, but no
   synthetic check running continuously against the real payment flow in production - the third cadence
   simply didn't exist.
4. **The fix:** The team adds a synthetic check that completes a real (low-value, refunded) checkout against
   production every few minutes, alerting immediately on failure - the exact failure mode that caused the
   two-hour outage would now surface in minutes.
5. **The lesson:** Pre-release testing, no matter how thorough, can't verify behavior that only exists in the
   live system talking to live third parties - that gap is exactly what production monitoring as testing
   exists to close.

**Quiz.** Why does continuous testing treat production monitoring as a form of testing, rather than a separate concern owned only by an operations team?

- [ ] Because monitoring tools are cheaper than dedicated test automation tools
- [x] Because a synthetic check against the live system has the same shape as a test - fixed steps, an expected outcome, and a loud failure - and can catch real-world behavior no staging environment can fully replicate
- [ ] Because pre-release testing is unreliable and should be replaced by monitoring entirely
- [ ] Because operations teams are responsible for writing all automated tests

*A synthetic check running against production is functionally a test - it just runs against reality instead of a staging copy of it. Continuous testing treats it as testing because staging can never perfectly predict real user behavior, real data, and real third-party services, so verification has to keep running after release too.*

- **Continuous testing, in one line** — Running automated tests at every stage of delivery - on every commit, on a schedule, and continuously in production - rather than treating testing as one phase after development is done.
- **The three typical cadences** — Fast smoke tests on every commit, a fuller regression suite on a nightly or scheduled cadence, and production monitoring that verifies the live system continuously.
- **Why production monitoring counts as testing** — A synthetic check against the live system has the same shape as a pre-release test - fixed steps, an expected result, a loud failure - and it catches real-world behavior no staging environment can fully replicate.

### Challenge

Map your own team's (or a team you've studied) continuous testing setup against the three cadences: what runs on every commit, what runs on a schedule, and what runs continuously against production. Name the gap - the cadence that's weakest or missing entirely.

- [AWS - What is Continuous Testing?](https://aws.amazon.com/what-is/continuous-testing/)
- [Atlassian - Software Testing in Continuous Delivery](https://www.atlassian.com/continuous-delivery/software-testing)
- [What is Continuous Testing?](https://www.youtube.com/watch?v=RYQbmjLgubM)

🎬 [What is Continuous Testing?](https://www.youtube.com/watch?v=RYQbmjLgubM) (7 min)

- Continuous testing runs at three cadences - fast smoke tests on every commit, a fuller regression suite on a schedule, and continuous production monitoring - not as one late testing phase.
- Each cadence exists because of a real speed-versus-coverage tradeoff: cheap and fast checks run most often, expensive and thorough checks run less often.
- Production monitoring counts as a genuine form of testing - a synthetic check against the live system has the same shape as a pre-release test, just running against reality instead of staging.
- Running the full regression suite on every commit isn't continuous testing - it's slow testing running more often, and it defeats the fast-feedback point of the on-commit cadence.


## Related notes

- [[Notes/agile-and-devops-for-testers/shift-left-and-cicd/the-cicd-pipeline|The CI/CD pipeline]]
- [[Notes/agile-and-devops-for-testers/shift-left-and-cicd/quality-gates|Quality gates]]
- [[Notes/agile-and-devops-for-testers/shift-left-and-cicd/shift-left|Shift-left]]


---
_Source: `packages/curriculum/content/notes/agile-and-devops-for-testers/shift-left-and-cicd/continuous-testing.mdx`_
