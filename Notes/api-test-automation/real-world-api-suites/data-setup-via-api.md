---
title: "Data setup via API"
tags: ["api-test-automation", "real-world-api-suites", "track-d"]
updated: "2026-07-17"
---

# Data setup via API

*Create test prerequisites through fast supported interfaces, isolate every run, and clean up only what the test owns.*

> Five minutes of clicking to create one prerequisite is not realistic setup. It is a hostage negotiation with the UI.

> **In real life**
>
> A laboratory labels each sample before the experiment. API setup should do the same: known recipe, unique identity, controlled inputs, scoped disposal.

**API-based test-data setup**: API-based test-data setup creates prerequisites through supported service endpoints rather than UI flows or direct database edits. Good setup is deterministic, uniquely namespaced, minimal, observable, and paired with cleanup that deletes only resources created by that run.

## Arrange quickly without cheating invisibly

Use authenticated create endpoints to arrange only the records a scenario needs. Generate a run id and carry it in names or metadata. Capture returned resource ids immediately; cleanup should use those ids, not a broad “delete all test data” query. Direct database setup can be valid for lower-level tests, but an API suite should not silently depend on schema internals unless that dependency is explicit.

> **Tip**
>
> Prefer create-and-capture over search-and-guess. The POST response gives the authoritative id; use it for action, assertion, and cleanup.

> **Common mistake**
>
> Shared fixtures named `Test Project` guarantee collisions under parallel execution. Namespacing is not polish—it is isolation.

![A researcher preparing labeled samples and equipment in a laboratory](data-setup-via-api.jpg)
*Sample preparation laboratory — Sofiia Baletska, CC BY 4.0, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Sample_preparation_laboratory.jpg)*
- **Prepared sample tools** — Each scenario receives the minimum prerequisite data it needs.
- **Separate white sample containers** — Unique run identities prevent parallel tests from sharing state accidentally.
- **Labeled bottle on the workspace** — Captured resource ids make teardown scoped and auditable.

**Arrange, use, and clean one resource**

1. **Generate run id** — Create a collision-resistant namespace.
2. **POST prerequisite** — Use the public create endpoint with valid auth.
3. **Capture returned id** — Store the server-assigned identity immediately.
4. **Exercise scenario** — Act on that exact resource.
5. **Delete owned ids** — Cleanup only what this run created.

*Run it - create deterministic names and cleanup ids (Python)*

```python
run_id = "run-2042"
created = []
for index in range(1, 4):
    server_id = 700 + index
    name = f"{run_id}-project-{index}"
    created.append(server_id)
    print(f"create {name} -> id={server_id}")
print("cleanup ids=" + ",".join(map(str, reversed(created))))
```

*Run it - create the same setup ledger (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    String runId = "run-2042"; List<Integer> created = new ArrayList<>();
    for (int i = 1; i <= 3; i++) {
      int id = 700 + i; created.add(id);
      System.out.println("create " + runId + "-project-" + i + " -> id=" + id);
    }
    Collections.reverse(created);
    System.out.println("cleanup ids=" + created.toString().replace("[", "").replace("]", "").replace(" ", ""));
  }
}
```

### Your first time: Your mission: build an isolated setup helper

- [ ] Generate one run id per suite execution — Use it consistently in created names.
- [ ] Create a project through POST /api/v1/projects — Use your sandbox's public credentials; do not copy anyone else's.
- [ ] Capture the returned project id — Never discover it later by an ambiguous name search.
- [ ] Delete only that id in teardown — Keep cleanup safe even when another run is active.

- **Parallel runs modify each other's records.**
  Add a per-run namespace and stop selecting records by shared display names.
- **Cleanup deletes another test's data.**
  Maintain an owned-id ledger and delete only ids created by this run.
- **Setup failure causes dozens of assertion failures.**
  Fail fast during arrange with the setup response status and body, before executing dependent checks.

### Where to check

- Setup request payload, auth scope, response status, and returned id.
- Run-id propagation through names, logs, and report metadata.
- Owned-id ledger and teardown order, including partial setup failure.

### Worked example: isolated BuggyAPI project setup

The suite creates `reg-2042-project` through `POST /api/v1/projects`, records its returned id, then creates scenario data beneath that project. Tests never search for “the test project.” Teardown deletes child resources then the captured project id. No database table or private implementation detail is required.

**Quiz.** What is the safest cleanup selector?

- [ ] All names containing test
- [ ] Everything created today
- [x] The exact resource ids recorded by this run
- [ ] The first list result

*An ownership ledger is explicit and collision-safe; broad text or time queries can delete unrelated data.*

- **Why setup via API?** — It is faster than UI setup while exercising supported service behavior.
- **What should a create helper return?** — The authoritative server-assigned resource id plus any data the scenario needs.
- **Cleanup rule** — Delete only resources recorded as owned by this run.

### Challenge

Design setup for five parallel workers. Show the run/worker namespace, returned-id ledger, teardown order, and behavior if the third create call fails.

### Ask the community

> Our setup collides on `[resource]`; naming rule, captured ids, and teardown selector are `[details]`.

Do not post live credentials or another learner's sandbox data.

- [Postman Docs — Write post-response test scripts](https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-scripts)
- [Postman Docs — Variables and scopes](https://learning.postman.com/docs/use/send-requests/variables/variables)

🎬 [Postman Beginner Tutorial 9: Environments — Automation Step by Step](https://www.youtube.com/watch?v=sUJjHU9oFzI) (12 min)

- Use supported create endpoints for fast setup without UI dependence.
- Give every run a unique namespace and capture every returned id.
- Fail during arrange when setup fails instead of producing misleading downstream failures.
- Cleanup must delete only resources explicitly owned by the current run.


## Related notes

- [[Notes/api-test-automation/real-world-api-suites/chaining-and-state|Chaining & state]]
- [[Notes/api-test-automation/real-world-api-suites/full-api-suite-on-buggyapi|Full API suite on BuggyAPI]]
- [[Notes/api-test-automation/real-world-api-suites/test-pyramids-for-apis|Test pyramids for APIs]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/real-world-api-suites/data-setup-via-api.mdx`_
