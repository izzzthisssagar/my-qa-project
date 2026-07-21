---
title: "Dashboards"
tags: ["ci", "dashboards", "metrics", "analytics", "track-d"]
updated: "2026-07-17"
---

# Dashboards

*CI dashboards support decisions when they show trends and distributions for failure, duration, queueing, reruns, flakes, and coverage with clear scope, freshness, ownership, and drill-down.*

> A dashboard says the pipeline is 96% successful. It mixes feature branches, canceled experiments,
> nightly retries, and release builds. The number is precise, attractive, and useless for deciding
> whether main is safe to ship.

> **In real life**
>
> An aircraft panel does not show one giant “plane score.” Separate instruments expose speed, altitude,
> heading, fuel, and engine state because each supports a different decision. A CI dashboard needs
> separable measures, healthy ranges, trend context, and a route from a bad gauge to the underlying run.

**CI dashboard**: A CI dashboard is a time-scoped, filterable view of pipeline health derived from run, job, test, and deployment records. Useful measures include first-attempt success, final success, failure and cancellation rate, queue and execution duration distributions, flake/rerun rate, change-to-feedback latency, and evidence freshness. Every tile needs scope, denominator, time window, last updated time, owner, and drill-down.

## Start with a decision, then choose a metric

| Decision | Better measure | Dangerous shortcut |
| --- | --- | --- |
| Can main ship? | latest required-gate result on current SHA | all-branch success rate |
| Is feedback slowing? | p50/p95 queue + execution duration | average total duration |
| Is the suite trustworthy? | first-attempt pass and rerun/flake rate | final green after retries |
| Where to invest? | top failure fingerprints × lost time | raw failure count |

Segment by pipeline source, branch, suite, environment, and period before comparing.

> **Tip**
>
> Show first-attempt and final outcomes side by side. The gap reveals hidden retries that a final-green
> dashboard would otherwise erase.

> **Common mistake**
>
> Treating coverage percentage or test count as quality. Both can rise while assertions weaken, risk
> scope changes, or failures become less diagnosable. Pair activity/coverage measures with outcomes.

![A Curtiss C-46 aircraft cockpit with many gauges, controls, and two crew members](dashboards.jpg)
*C-46 cockpit — Bzuk, public domain. [Source](https://commons.wikimedia.org/wiki/File:C-46_cockpit.jpg)*
- **Different gauges** — Queue, duration, success, and flakes answer different questions; do not collapse them into one score.
- **Healthy ranges** — A measure becomes actionable when the team defines expected bounds and ownership.
- **Controls** — Filters for branch, source, environment, and time window change the interpretation.
- **Human decision** — Dashboards assist an accountable operator; they do not replace context or investigation.

**From CI events to an honest dashboard**

1. **Events are emitted** — Runs, jobs, attempts, tests, queues, and deployments get stable IDs.
2. **Data is normalized** — Status meanings, timestamps, branches, suites, and fingerprints align.
3. **Scope is selected** — Filter source, branch, environment, and time window.
4. **Measures are calculated** — Use explicit denominators and distributions, not ambiguous averages.
5. **Freshness is shown** — Last-updated and missing-data indicators prevent stale confidence.
6. **Tile drills down** — Every anomaly links to the exact runs, jobs, tests, and artifacts.

*Run it — expose retries hidden by final success (Python)*

```python
``runs = [("r1", "failed", "passed"), ("r2", "passed", "passed"), ("r3", "failed", "passed")]
first_pass = sum(first == "passed" for _, first, _ in runs) / len(runs)
final_pass = sum(final == "passed" for _, _, final in runs) / len(runs)
print(f"first-attempt success: {first_pass:.0%}")
print(f"final success: {final_pass:.0%}")
print(f"retry-hidden gap: {final_pass - first_pass:.0%}")``
```

*Run it — expose retries hidden by final success (Java)*

```java
``import java.util.*;

public class Main {
    record Run(String id, String first, String last) {}
    public static void main(String[] args) {
        var runs = List.of(new Run("r1", "failed", "passed"),
            new Run("r2", "passed", "passed"), new Run("r3", "failed", "passed"));
        long first = runs.stream().filter(r -> r.first().equals("passed")).count();
        long last = runs.stream().filter(r -> r.last().equals("passed")).count();
        System.out.printf("first-attempt success: %.0f%%%n", 100.0 * first / runs.size());
        System.out.printf("final success: %.0f%%%n", 100.0 * last / runs.size());
        System.out.printf("retry-hidden gap: %.0f%%%n", 100.0 * (last - first) / runs.size());
    }
}``
```

### Your first time: Your mission: build one decision-driven view

- [ ] Write the decision first — Name the user, decision, cadence, and action when the measure changes.
- [ ] Define numerator and denominator — Specify included statuses, retries, branches, sources, and time window.
- [ ] Add segmentation and freshness — Filter meaningful populations and expose stale/missing data.
- [ ] Prove drill-down — Open the exact run and evidence behind one chart point.

You now have a decision surface rather than a wall of vanity numbers.

- **Dashboard success disagrees with the release gate.**
  Compare SHA, branch, source, required-job scope, attempts, skipped/canceled treatment, and refresh time.
- **Average duration looks stable while developers complain.**
  Plot p50/p95 queue and execution separately; a few long waits disappear inside an average.
- **Flakes vanish after retries.**
  Store attempt-level outcomes and display first-attempt success, rerun rate, and final status together.
- **A chart changed after a taxonomy rename.**
  Version metric definitions, map old/new suite identifiers, and annotate breaks in historical series.

### Where to check

- **Tile definition** — decision, formula, denominator, window, and owner.
- **Filters** — branch, source, environment, suite, and attempt.
- **Ingestion lag/freshness** — last event and missing-data state.
- **Raw run/job/test IDs** — trace a point back to evidence.
- **Metric-version history** — schema, status, or taxonomy changes.

### Worked example: 100% green hiding a 33% first-pass rate

1. Three main-branch pipelines all finish green after automatic retries.
2. The dashboard counts only final status and reports 100% success.
3. Two runs failed first because of the same checkout timeout, costing 24 minutes each.
4. The team adds first-attempt success, rerun rate, failure fingerprint, and lost-time tiles.
5. The dashboard now exposes 33% first-pass success and points directly to the unstable dependency.

**Quiz.** Which dashboard comparison best reveals hidden flakiness?

- [ ] Total tests this month versus last month
- [ ] Final success rate alone
- [x] First-attempt success versus final success after retries, segmented by suite
- [ ] Lines of test code versus product code

*Retry recovery creates a measurable gap between first and final outcome. Segmenting identifies where the instability lives.*

- **Denominator** — The population included in a rate; changing it changes the meaning.
- **p95 duration** — The value at or below which 95% of observations fall, exposing tail latency better than an average.
- **First-attempt success** — Share of runs green before retry; a trust signal for suite stability.
- **Freshness** — How recently the dashboard successfully incorporated source events.
- **Drill-down** — Path from aggregate metric to exact run, job, test, log, and artifact.

### Challenge

Take one existing CI success chart. Document its denominator, retries, skipped/canceled handling,
scope, freshness, and owner. Add first-attempt status and p95 latency, then trace one anomaly to raw evidence.

### Ask the community

> Dashboard metric [name] shows [value] but raw CI shows [difference]. Formula, denominator, filters, attempt handling, freshness, and example run IDs are [values].

This makes a data-definition defect reproducible instead of debating screenshots.

- [GitLab Docs — CI/CD analytics](https://docs.gitlab.com/user/analytics/ci_cd_analytics/)
- [GitHub Docs — workflow runs API](https://docs.github.com/en/rest/actions/workflow-runs)

🎬 [GitLab CI/CD Tutorial for Beginners — TechWorld with Nana](https://www.youtube.com/watch?v=qP8kir2GUgo) (69 min)

- Begin with a decision and accountable user, then select measures.
- Expose scope, denominator, time window, attempt handling, freshness, and owner.
- Use distributions and segment meaningful populations instead of relying on averages.
- Compare first-attempt and final success to reveal retry-hidden instability.
- Every aggregate must drill down to exact runs and durable evidence.


## Related notes

- [[Notes/automation-in-cicd/scheduling-and-reporting/publishing-reports|Publishing reports]]
- [[Notes/automation-in-cicd/flake-management/detecting-flakes|Detecting flakes]]
- [[Notes/automation-in-cicd/scheduling-and-reporting/notifications|Notifications]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/scheduling-and-reporting/dashboards.mdx`_
