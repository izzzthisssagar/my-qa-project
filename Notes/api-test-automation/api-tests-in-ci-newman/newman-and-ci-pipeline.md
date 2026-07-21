---
title: "Newman and the CI pipeline"
tags: ["api-test-automation", "api-tests-in-ci-newman", "track-d"]
updated: "2026-07-17"
---

# Newman and the CI pipeline

*Wire a versioned Postman collection into CI as a deterministic gate, with pinned tooling, protected secrets, useful timeouts, and failure propagation.*

> A local command is a promising audition. A CI gate is the job: clean machine, known inputs, every pull request, and no human allowed to click “ignore.”

> **In real life**
>
> A 1913 assembly line moved every car through the same stations. CI does the same to changes: checkout, install, start the service, run the API suite, publish evidence.

**CI API-test gate**: A CI API-test gate is a pipeline job whose reproducible setup runs an API suite and fails the workflow when the runner exits non-zero. It must control tool versions, target availability, secrets, timeouts, and artifacts rather than relying on a developer machine's state.

## A gate, not a background decoration

A robust job checks out the same collection reviewed with the code, installs a pinned Node and dependency lockfile, starts or reaches the intended test target, then runs `npx newman run`. Use request and overall timeouts so a dead service does not occupy a runner forever. Newman returns a status CI can use; the shell step must propagate it.

> **Tip**
>
> Put the fast, deterministic smoke collection on pull requests. Keep broader regression in a later or scheduled lane so feedback stays useful without shrinking coverage to nothing.

> **Common mistake**
>
> Fetching an unversioned collection from a mutable workspace during CI means the tested artifact may differ from the pull request. Either version the export or pin the remote revision through a controlled workflow.

![Workers along an early Ford automobile assembly line](newman-and-ci-pipeline.jpg)
*Ford assembly line, 1913 — unknown author, public domain, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:AssemblyLine.jpg)*
- **First station** — Checkout and dependency installation prepare a known starting state.
- **Work moves forward** — The API target must be ready before the suite reaches its execution stage.
- **Final inspection** — Assertions and exit status decide whether this change proceeds.

**Pull request to API gate**

1. **Checkout + pinned Node** — Recreate the reviewed repository state.
2. **Install with lockfile** — Resolve the exact Newman dependency.
3. **Provision target + secrets** — Wait for health; inject protected values.
4. **Run Newman** — Apply explicit request and run timeouts.
5. **Publish report; propagate exit** — Evidence survives while failures still block.

*Run it - decide a pipeline gate from stages (Python)*

```python
stages = {"checkout": True, "service_ready": True, "newman": False, "report_uploaded": True}
for name, ok in stages.items():
    print(f"{name}={'ok' if ok else 'failed'}")
gate = stages["checkout"] and stages["service_ready"] and stages["newman"]
print(f"gate={'PASS' if gate else 'BLOCK'}")
```

*Run it - decide the same pipeline gate (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    Map<String, Boolean> stages = new LinkedHashMap<>();
    stages.put("checkout", true); stages.put("service_ready", true);
    stages.put("newman", false); stages.put("report_uploaded", true);
    stages.forEach((n, ok) -> System.out.println(n + "=" + (ok ? "ok" : "failed")));
    boolean gate = stages.get("checkout") && stages.get("service_ready") && stages.get("newman");
    System.out.println("gate=" + (gate ? "PASS" : "BLOCK"));
  }
}
```

### Your first time: Your mission: add a truthful API gate

- [ ] Use a pinned Node version and frozen lockfile install — The runner should not improvise dependencies.
- [ ] Wait on the target health endpoint — A retrying readiness check separates startup delay from product failure.
- [ ] Inject the API key from CI secrets — Never echo it or commit it in an environment export.
- [ ] Upload JUnit even on failure — Use the CI platform's always-run condition for evidence, not for the gate itself.

- **The suite starts before the API is ready.**
  Add a bounded readiness loop against /api/health before Newman.
- **A failed run has no report artifact.**
  Keep the Newman failure status, but place artifact upload in an always-run step.
- **CI and local results disagree.**
  Compare Node/Newman versions, collection revision, base URL, and environment inputs.

### Where to check

- CI logs for the exact collection SHA, Newman version, and target URL.
- Secret masking and environment-variable names.
- Health-check timing, Newman timeouts, and the original process status.

### Worked example: a pull-request smoke gate

The job installs from the lockfile, waits up to 60 seconds for BuggyAPI `/api/health`, then runs a read-only smoke collection with `--timeout-request 5000`. JUnit upload runs even if Newman fails, while the Newman step remains red. Reviewers get both a blocked merge and the failing assertion name.

**Quiz.** How should a CI job preserve a report when Newman fails?

- [ ] Suppress Newman's exit code
- [x] Upload artifacts in an always-run step while preserving the failure
- [ ] Retry forever
- [ ] Commit the report

*Evidence collection and gate outcome are separate concerns. Always-run upload preserves evidence without lying about the test result.*

- **What makes a CI test a gate?** — Its non-zero result blocks the workflow or merge path.
- **Why pin Newman?** — To keep local and CI behavior reproducible across runner updates.
- **Readiness versus assertion failure?** — Readiness proves the target can accept tests; assertions evaluate its behavior.

### Challenge

Sketch a CI job with checkout, locked install, bounded health wait, Newman execution, and always-run report upload. Mark exactly which step owns the gate status.

### Ask the community

> My Newman CI gate differs from local at `[stage]`; versions, target, and redacted inputs are `[details]`.

Bring comparable facts, not a screenshot of one red icon.

- [Postman Docs — Newman in continuous integration](https://learning.postman.com/docs/reference/newman-cli/continuous-integration/)
- [Postman Docs — Newman options and exit status](https://learning.postman.com/docs/reference/newman-cli/newman-options)

🎬 [Building Quality Gates in DevOps CI/CD Pipelines — DheerajTechInsight](https://www.youtube.com/watch?v=90auAVyZswc) (31 min)

- Pin tools and version the collection so CI tests the reviewed artifact.
- Wait for target readiness and bound network waits with explicit timeouts.
- Inject secrets at runtime and keep logs/reporters from exposing them.
- Upload evidence independently while preserving Newman's failure status as the gate.


## Related notes

- [[Notes/api-test-automation/api-tests-in-ci-newman/running-postman-collections-headlessly|Running Postman collections headlessly]]
- [[Notes/api-test-automation/api-tests-in-ci-newman/reporting-api-results|Reporting API results]]
- [[Notes/automation-in-cicd/running-tests-in-ci/what-ci-is|What CI is]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/api-tests-in-ci-newman/newman-and-ci-pipeline.mdx`_
