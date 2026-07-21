---
title: "Reporting API results"
tags: ["api-test-automation", "api-tests-in-ci-newman", "track-d"]
updated: "2026-07-17"
---

# Reporting API results

*Produce console feedback for humans, JUnit for CI, JSON for deeper diagnosis, and artifacts that survive long enough to answer what actually failed.*

> A red pipeline square says a test was unhappy. A useful report says which request, which assertion, which environment, and what the next investigator should inspect.

> **In real life**
>
> Punch cards turned machine state into a durable record another system could sort. Newman reporters do the same run in several shapes: terminal for people, JUnit for CI, JSON for tools.

**API test result report**: A test result report is a structured, retained account of run identity, requests, assertions, errors, timings, and outcome. Newman has built-in CLI, JSON, JUnit, progress, and emojitrain reporters; selecting a non-CLI reporter disables the default CLI output unless cli is explicitly included.

## One run, several consumers

Use `-r cli,junit,json` when humans need immediate logs, CI needs test cases, and diagnosis needs machine-readable detail. Set explicit export paths such as `--reporter-junit-export reports/newman.xml` and `--reporter-json-export reports/newman.json`. Report artifacts should include run metadata but exclude secrets and unnecessary sensitive bodies.

> **Tip**
>
> Name artifacts with suite, environment, commit, and run id. “newman.json” downloaded from five jobs is a tiny distributed-systems incident.

> **Common mistake**
>
> Turning on `-r junit` alone disables the default CLI reporter. If you still want terminal output, request `-r cli,junit` explicitly.

![A wide IBM punch card with rows of rectangular holes and printed columns](reporting-api-results.png)
*IBM punch card — MdeVicente, CC0 1.0, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Ibm_punch_card.png)*
- **Structured columns** — Machine-readable reports use stable fields so CI can count tests and failures.
- **Individual marks** — Each assertion needs its own identity; one red suite total is not enough.
- **Durable record** — An artifact remains available after the ephemeral runner disappears.

**Turn one run into useful evidence**

1. **Newman execution** — Requests, assertions, errors, and timings are collected.
2. **CLI reporter** — Fast feedback appears in the job log.
3. **JUnit reporter** — CI renders named test cases and failures.
4. **JSON reporter** — Detailed execution data supports diagnosis or trend extraction.
5. **Retained artifact** — Evidence survives the runner under a traceable name.

*Run it - summarize assertion records (Python)*

```python
records = [("status is 200", True, 81), ("schema matches", False, 81), ("under 500ms", True, 81)]
passed = sum(ok for _, ok, _ in records)
failed = len(records) - passed
print(f"tests={len(records)} passed={passed} failed={failed}")
for name, ok, ms in records:
    print(f"{'PASS' if ok else 'FAIL'} | {name} | {ms}ms")
```

*Run it - summarize the same records (Java)*

```java
import java.util.*;
public class Main {
  record Result(String name, boolean ok, int ms) {}
  public static void main(String[] args) {
    List<Result> rows = List.of(new Result("status is 200", true, 81), new Result("schema matches", false, 81), new Result("under 500ms", true, 81));
    long passed = rows.stream().filter(Result::ok).count();
    System.out.println("tests=" + rows.size() + " passed=" + passed + " failed=" + (rows.size() - passed));
    rows.forEach(r -> System.out.println((r.ok() ? "PASS" : "FAIL") + " | " + r.name() + " | " + r.ms() + "ms"));
  }
}
```

### Your first time: Your mission: publish two report formats

- [ ] Run with cli and junit reporters — Confirm the terminal remains readable and XML is created.
- [ ] Add a JSON export — Inspect it for useful request and assertion detail.
- [ ] Force one named failure — Verify CI surfaces the assertion name rather than only a job failure.
- [ ] Audit for secrets — Check console and artifacts before increasing retention or sharing.

- **The terminal summary vanished.**
  Include cli explicitly when enabling other reporters: -r cli,junit.
- **CI shows zero test cases.**
  Confirm the JUnit export path exists, is uploaded, and is registered with the CI test-report feature.
- **Reports expose tokens or sensitive bodies.**
  Remove script logging, restrict reporter detail, redact at source, and rotate any exposed credential.

### Where to check

- The `-r` list and reporter-specific export paths.
- Artifact upload conditions and retention settings.
- Assertion names, first failure, request URL, revision, environment, and secret leakage.

### Worked example: a report reviewers can act on

The job runs `-r cli,junit,json`; JUnit feeds the CI Tests tab, JSON is retained seven days for failed runs, and the console keeps the concise summary. Artifact names contain `smoke-staging-{commit}-{runId}`. A schema assertion failure appears by name and links back to the exact job.

**Quiz.** Why did CLI output disappear after adding -r junit?

- [ ] JUnit is broken
- [x] Selecting another reporter disables default CLI unless cli is included
- [ ] Newman only supports one reporter
- [ ] The collection has no tests

*Postman documents that the default CLI reporter is turned off when other reporters are explicitly selected; use -r cli,junit for both.*

- **CLI reporter** — Human-readable live terminal output.
- **JUnit reporter** — XML suited to CI test-result rendering.
- **JSON reporter** — Machine-readable execution detail for diagnosis and custom processing.

### Challenge

Define a reporting contract with required metadata, file names, retention, upload-on-failure behavior, and redaction rules. Test it with one intentional assertion failure.

### Ask the community

> Our report loses `[field/test cases]`; Newman command, artifact path, and redacted sample are `[details]`.

A tiny redacted sample beats a screenshot of the CI sidebar.

- [Postman Docs — Newman built-in reporters](https://learning.postman.com/docs/reference/newman-cli/newman-built-in-reporters)
- [Postman Docs — Newman command reference](https://learning.postman.com/docs/reference/newman-cli/newman-options)

🎬 [Postman Newman Tutorial | Postman API Testing — SDET Unicorns](https://www.youtube.com/watch?v=ee-T6skoMjM) (12 min)

- Choose report formats by consumer: CLI for humans, JUnit for CI, JSON for tools and diagnosis.
- Explicitly include cli when selecting other reporters if terminal output should remain.
- Use traceable artifact names and retention that matches investigation needs.
- Treat reports as sensitive data and audit them for tokens and response bodies.


## Related notes

- [[Notes/api-test-automation/api-tests-in-ci-newman/running-postman-collections-headlessly|Running Postman collections headlessly]]
- [[Notes/api-test-automation/api-tests-in-ci-newman/newman-and-ci-pipeline|Newman + CI pipeline]]
- [[Notes/framework-design/logging-and-reporting/allure|Allure]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/api-tests-in-ci-newman/reporting-api-results.mdx`_
