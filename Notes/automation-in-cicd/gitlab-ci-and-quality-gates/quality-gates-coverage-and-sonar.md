---
title: "Quality gates (coverage, Sonar)"
tags: ["quality-gates", "coverage", "sonarqube", "track-d"]
updated: "2026-07-17"
---

# Quality gates (coverage, Sonar)

*A quality gate converts a small set of measurable risk policies into a pass/fail decision; coverage and static analysis are useful signals only when scoped, explainable, and resistant to gaming.*

> Coverage can rise while confidence falls. A test that executes every line without asserting the
> outcome may produce a beautiful percentage and prove nothing. A gate is valuable when it blocks a
> specific unacceptable risk, not when it turns a convenient number into a superstition.

> **In real life**
>
> A caliper is precise, but it measures only the dimension between its jaws. It cannot tell whether the
> part is strong, correctly assembled, or safe. Coverage and static analysis are the same: exact within
> their definitions, incomplete as a verdict on overall quality.

**quality gate**: A quality gate is an automated policy that evaluates selected measurable conditions and returns pass or fail for a change or codebase. Examples include no new blocker findings, coverage on changed code above a threshold, successful tests, or bounded duplication. SonarQube/SonarCloud can compute a Quality Gate from analysis; GitLab can ingest coverage and code-quality reports. A gate should focus on new-code risk, declare ownership and exceptions, and remain only one part of the release decision.

## Gate behavior, not vanity

Good policies are small and actionable:

- all required automated tests pass;
- no new critical/blocker security or reliability findings;
- changed-code coverage does not fall below an agreed risk threshold;
- analysis completed for the exact revision;
- any exception has an owner, reason, expiry, and review.

Repository-wide coverage targets punish legacy code unrelated to a small change and encourage shallow
tests. New-code policies create a ratchet without pretending the existing system became safe overnight.

> **Tip**
>
> Publish the report and a short failure summary. A red gate that says only "quality failed" creates
> work; one that links new findings, rules, files, and remediation makes work finish.

> **Common mistake**
>
> Failing on every analyzer warning from day one. Teams drown in old findings, mark the job allowed to
> fail, and teach everyone that the gate is ceremonial.

![A metal vernier caliper measuring a small black circular object against a millimetre scale](quality-gates-coverage-and-sonar.jpg)
*Caliper full view — Simon A. Eugster, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:Caliper_full_view.jpeg)*
- **Measured scope** — A metric covers a defined property, not the entire product.
- **Threshold** — The gate compares an observed value or severity with an agreed boundary.
- **Calibration** — Rules, exclusions, versions, and baselines must be governed so results remain comparable.
- **Limit of claim** — Precision does not expand scope: unmeasured risks still require tests and review.

**From analysis to merge signal**

1. **Exact revision checked out** — Analysis and tests bind to the candidate commit.
2. **Evidence generated** — Tests, coverage, and analyzers produce machine-readable reports.
3. **Reports parsed** — GitLab or Sonar maps findings to changed code and configured rules.
4. **Policy evaluated** — New-code thresholds and prohibited severities produce pass/fail.
5. **Evidence displayed** — Merge-request annotations explain what crossed the boundary.
6. **Exception governed** — Any override is rare, owned, reasoned, time-bounded, and auditable.

*Run it — evaluate a new-code gate (Python)*

```python
``evidence = {"tests_pass": True, "new_coverage": 84, "new_blockers": 0}
policy = {"minimum_coverage": 80, "maximum_blockers": 0}
checks = {
    "tests": evidence["tests_pass"],
    "coverage": evidence["new_coverage"] >= policy["minimum_coverage"],
    "blockers": evidence["new_blockers"] <= policy["maximum_blockers"],
}
print(checks)
print("gate:", "PASS" if all(checks.values()) else "FAIL")``
```

*Run it — evaluate a new-code gate (Java)*

```java
``import java.util.*;

public class Main {
    public static void main(String[] args) {
        boolean testsPass = true;
        int newCoverage = 84, newBlockers = 0;
        var checks = new LinkedHashMap<String, Boolean>();
        checks.put("tests", testsPass);
        checks.put("coverage", newCoverage >= 80);
        checks.put("blockers", newBlockers <= 0);
        System.out.println(checks);
        System.out.println("gate: " + (checks.values().stream().allMatch(Boolean::booleanValue) ? "PASS" : "FAIL"));
    }
}``
```

### Your first time: Your mission: design one defensible gate

- [ ] Name the risk and evidence source — For example: untested new branches, measured by changed-code branch coverage.
- [ ] Choose a threshold from history and consequence — Do not copy an industry number without examining current variance and criticality.
- [ ] Make one change fail on purpose — Confirm report, annotation, status, and remediation path are understandable.
- [ ] Document exception governance — Specify authorized role, required reason, owner, expiry, and follow-up.

A gate is ready when failure teaches the author exactly what policy was violated and why it matters.

- **Coverage is missing or zero in GitLab.**
  Separate log regex percentage from coverage_report format/path; verify the tool generated the expected Cobertura or JaCoCo file.
- **Sonar reports analysis but the pipeline passes a failed gate.**
  Ensure the scanner waits for and propagates Quality Gate status with a bounded timeout.
- **Developers add assertions-free tests to raise coverage.**
  Review test strength, mutation results or defect detection, and focus policy on risk—not percentage alone.
- **Old findings block every change.**
  Baseline legacy debt and gate new code while separately owning debt reduction.

### Where to check

- **Exact analyzed SHA and branch/MR context** — evidence must match the candidate.
- **Raw report path/format** — generation versus ingestion failure.
- **Quality profile/gate version** — rule or threshold drift.
- **New-code definition and exclusions** — actual scope of the metric.
- **Merge-request annotations and analyzer task log** — actionable failure reason.

### Worked example: 80% coverage that missed the refund bug

1. A service has 86% line coverage and a passing global threshold.
2. Refund tests execute the handler but never assert the amount sent to the payment provider.
3. A sign error ships despite green coverage.
4. The team adds outcome assertions and reviews changed-code branch coverage for money paths.
5. Coverage remains a useful gap detector, but risk-focused assertions become the actual confidence.

**Quiz.** What does 90% line coverage prove?

- [ ] The product is 90% correct
- [x] Tests executed 90% of instrumented lines under that measurement; assertion strength and other risks remain unknown
- [ ] No security defects exist
- [ ] Every branch and input was tested

*Coverage measures execution, not correctness, assertion quality, branch completeness, realistic data, or operational risk.*

- **Quality gate** — Automated pass/fail policy over selected evidence, not a total quality verdict.
- **New-code gate** — Applies policy to changed code, creating a ratchet without blocking all work on legacy debt.
- **Line coverage claim** — Which instrumented lines executed; it says nothing direct about assertion strength.
- **Actionable gate failure** — Names policy, evidence, changed location, remediation, and report link.
- **Governed override** — Authorized, reasoned, owned, time-bounded, auditable, and followed up.

### Challenge

Take one current gate and write its exact claim, blind spots, baseline, threshold rationale, owner,
failure remediation, false-positive rate, and override history. Replace one vanity rule with a risk rule.

### Ask the community

> Gate [name/version] failed on SHA [sha] because [policy]. Raw evidence is [value/report], new-code scope is [scope], and expected remediation is [action].

Share evidence and configuration, not confidential source or tokens.

- [GitLab Docs — CI/CD artifact report types](https://docs.gitlab.com/ci/yaml/artifacts_reports/)
- [SonarQube Docs — Quality gates](https://docs.sonarsource.com/sonarqube-server/latest/user-guide/quality-gates/)

🎬 [How to Create Quality Gates in SonarQube — Engineerhoon](https://www.youtube.com/watch?v=8_Xt9vchlpY) (7 min)

- A quality gate blocks a defined unacceptable risk; it does not certify the entire product.
- Coverage measures executed code, not assertion strength or correctness.
- Prefer actionable new-code policies over overwhelming legacy-wide thresholds.
- Bind analysis to the exact revision and publish understandable report evidence.
- Keep overrides rare, authorized, owned, time-bounded, and auditable.


## Related notes

- [[Notes/automation-in-cicd/gitlab-ci-and-quality-gates/blocking-a-merge-on-failure|Blocking a merge on failure]]
- [[Notes/automation-in-cicd/gitlab-ci-and-quality-gates/gitlab-ci-yml|.gitlab-ci.yml]]
- [[Notes/automation-in-cicd/scheduling-and-reporting/dashboards|Dashboards]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/gitlab-ci-and-quality-gates/quality-gates-coverage-and-sonar.mdx`_
