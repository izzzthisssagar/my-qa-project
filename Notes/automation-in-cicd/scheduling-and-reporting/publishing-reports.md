---
title: "Publishing reports"
tags: ["ci", "test-reporting", "artifacts", "junit", "track-d"]
updated: "2026-07-17"
---

# Publishing reports

*A CI report turns raw runner output into durable evidence only when it preserves machine-readable results, human diagnosis, revision and environment identity, artifacts, and retention.*

> CI says “27 tests failed.” The runner is already gone, the console log is truncated, and the only
> screenshot lived in its temporary workspace. Execution happened; evidence did not survive. For the
> person debugging tomorrow, that is nearly the same as never running the suite.

> **In real life**
>
> A printing press does not create the investigation—it makes the result portable, repeatable, and
> readable by people who were not in the room. A test reporter packages transient execution into a
> record that reviewers, dashboards, and later jobs can consume.

**Published CI test report**: A published test report is durable, attributable CI evidence produced from a test run. It commonly combines a machine-readable format such as JUnit XML with a human-readable HTML or platform summary, plus failure artifacts. A useful report states the exact commit, attempt, environment, suite/shard, timestamps, outcome counts, and retention location.

## Publish evidence, not decoration

```yaml
- name: Run tests
  run: pytest --junitxml=results/junit.xml
- name: Upload evidence
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: tests-${{ github.sha }}-${{ github.run_attempt }}
    path: results/
    retention-days: 14
```

`if: always()` matters because failure is when evidence is most valuable. A unique name prevents a
rerun, matrix cell, or shard from disguising which result produced the files.

> **Tip**
>
> Keep the raw machine-readable file even when a plugin renders a beautiful summary. XML/JSON supports
> reprocessing, trend extraction, and migration when the UI or publisher changes.

> **Common mistake**
>
> Publishing only an HTML report with “latest” in its path. It is easy to read but hard to aggregate,
> and a new run can overwrite the evidence needed to explain the previous failure.

![A historical wooden printing press beside examples of printed pages](publishing-reports.jpg)
*The Printing Press — RF National Scenic Byway / J. Pitts, CC BY-SA 2.0. [Source](https://commons.wikimedia.org/wiki/File:The_Printing_Press.jpg)*
- **Reporter** — Transforms runner output into a standard, portable record.
- **Human-readable pages** — Summaries help reviewers understand failures without parsing raw logs.
- **Durable copies** — Retention and immutable naming preserve evidence after the runner disappears.
- **Operator** — A report still needs an owner who can interpret and act on it.

**From test process to reviewable evidence**

1. **Tests execute** — Framework records case IDs, duration, status, and failure details.
2. **Machine report is written** — JUnit XML or structured JSON preserves individual results.
3. **Failure context is collected** — Logs, screenshots, traces, dumps, and environment metadata.
4. **Publisher runs even on failure** — Conditional logic must not skip the evidence step when tests are red.
5. **Artifacts become durable** — Immutable names, access control, and retention apply.
6. **Platform renders summary** — Checks, merge requests, and dashboards link back to raw evidence.

*Run it — summarize JUnit-style cases (Python)*

```python
``cases = [("login", "passed", 1.2), ("checkout", "failed", 4.8), ("search", "passed", 0.7)]
counts = {state: sum(1 for _, s, _ in cases if s == state) for state in ("passed", "failed")}
duration = sum(seconds for _, _, seconds in cases)
print(f"total={len(cases)} passed={counts['passed']} failed={counts['failed']}")
print(f"duration={duration:.1f}s")
print("publish even on failure:", True)``
```

*Run it — summarize JUnit-style cases (Java)*

```java
``import java.util.*;

public class Main {
    record Case(String name, String state, double seconds) {}
    public static void main(String[] args) {
        var cases = List.of(new Case("login", "passed", 1.2),
            new Case("checkout", "failed", 4.8), new Case("search", "passed", 0.7));
        long passed = cases.stream().filter(c -> c.state().equals("passed")).count();
        long failed = cases.size() - passed;
        double duration = cases.stream().mapToDouble(Case::seconds).sum();
        System.out.printf("total=%d passed=%d failed=%d%n", cases.size(), passed, failed);
        System.out.printf("duration=%.1fs%n", duration);
        System.out.println("publish even on failure: true");
    }
}``
```

### Your first time: Your mission: publish one failure-proof report

- [ ] Generate a structured result — Use JUnit XML or another platform-supported machine format.
- [ ] Collect diagnosis artifacts — Attach logs, traces, screenshots, environment, and seed/test-data identity.
- [ ] Publish under failure — Break a test intentionally and prove the publishing step still executes.
- [ ] Verify identity and retention — Find SHA, attempt, shard, access policy, download link, and expiry.

The run now leaves an auditable record instead of a disappearing console.

- **The report step is skipped when tests fail.**
  Use the platform's always/finally condition and ensure the test command does not terminate the entire job before cleanup.
- **Matrix reports overwrite one another.**
  Include OS, runtime, browser, shard, SHA, and attempt in artifact/report identity, then aggregate explicitly.
- **The platform shows zero tests although XML exists.**
  Validate the report schema, path/glob, working directory, XML encoding, and publisher support.
- **A historical failure can no longer be opened.**
  Check retention, expiry, deletion policy, permissions, and whether a latest alias overwrote immutable evidence.

### Where to check

- **Test command options** — result format and output directory.
- **Publisher condition** — whether it runs after failure/cancellation.
- **Artifact manifest** — exact matched paths, size, name, and retention.
- **Report parser logs** — malformed files and unsupported schemas.
- **Run metadata** — SHA, attempt, environment, shard, and timestamps.

### Worked example: four shards, one misleading report

1. Four browser shards each write `results.xml` and upload artifact `test-results`.
2. Only the last upload is visible; it contains 250 of 1,000 cases and happens to be green.
3. The merge request appears healthy while another shard failed.
4. The team names artifacts by SHA, attempt, browser, and shard, then adds an aggregation job.
5. The summary now reports all 1,000 cases and links each failure to its trace.

**Quiz.** Why retain both machine-readable and human-readable test output?

- [ ] They are identical backups
- [x] Structured output supports parsing and trends; rendered output speeds human diagnosis
- [ ] HTML is required to fail CI
- [ ] JUnit XML contains screenshots automatically

*The formats serve different consumers. Structured data enables automation and aggregation; rendered summaries make review faster. Failure artifacts remain separate evidence.*

- **JUnit XML** — A widely supported structured exchange format for suites, cases, status, duration, and failure text.
- **Publish-on-failure** — A finalization condition that preserves evidence even when the test command exits nonzero.
- **Immutable artifact identity** — A name/path tied to revision, attempt, environment, and shard rather than only latest.
- **Retention** — How long evidence remains downloadable before expiry or deletion.
- **Aggregation** — Combining distinct shard/matrix result files without overwriting their identities.

### Challenge

Force one failure in a two-shard run. Publish both raw results and diagnosis artifacts, aggregate the
case totals, rerun the failed job, and prove a reviewer can distinguish both attempts one week later.

### Ask the community

> CI report [name] shows [missing/incorrect] results. Test output path, publisher condition, artifact manifest, SHA/attempt/shard, parser log, and retention are [values].

This evidence separates generation, path matching, parsing, overwriting, and expiry failures.

- [GitHub Docs — workflow artifacts](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts)
- [GitLab Docs — artifact report types](https://docs.gitlab.com/ci/yaml/artifacts_reports/)

🎬 [Capture Screenshots and Record Videos After Test Execution — CommitQuality](https://www.youtube.com/watch?v=HUzCg0o0ScM) (9 min)

- Runner output is temporary; published evidence must survive the job.
- Keep machine-readable results, human summaries, and diagnosis artifacts.
- Run publishers on failure and cancellation paths where possible.
- Make revision, attempt, environment, matrix cell, and shard identity explicit.
- Test parsing, access, aggregation, and retention—not merely artifact upload success.


## Related notes

- [[Notes/automation-in-cicd/running-tests-in-ci/artifacts|Artifacts]]
- [[Notes/automation-in-cicd/scheduling-and-reporting/dashboards|Dashboards]]
- [[Notes/automation-in-cicd/scheduling-and-reporting/notifications|Notifications]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/scheduling-and-reporting/publishing-reports.mdx`_
