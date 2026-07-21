---
title: "Chaining and state"
tags: ["api-test-automation", "real-world-api-suites", "track-d"]
updated: "2026-07-17"
---

# Chaining and state

*Carry server-issued values between requests without hiding dependencies, leaking state across scenarios, or making one early failure poison the entire suite.*

> Create returns an id. Update needs that id. Delete needs it again. Hard-code `42` and the suite is not chained—it is haunted.

> **In real life**
>
> Each chain link transfers force to the next. A request chain transfers a validated token or id; one broken link should stop that scenario, not quietly feed garbage downstream.

**Request chaining**: Request chaining captures a value from one response—such as a token, project id, or ticket id—and supplies it to a later request. Scenario state should be explicit, narrowly scoped, validated before use, and reset between independent scenarios.

## State is useful when ownership is visible

After a create response, assert success and schema before storing `id`. In Postman, prefer a scope whose lifetime matches the scenario; clear temporary values when done. Collection-wide mutable variables can make cases order-dependent. A chain is appropriate for one business lifecycle, not as a way to make every test depend on the previous test's leftovers.

> **Tip**
>
> Name variables by meaning and owner—`createdTicketId` beats `id`. Validate before storing, and log the run id rather than the secret token.

> **Common mistake**
>
> A 401 login response followed by `pm.response.json().token` can overwrite good state with undefined. Assert the prerequisite response first and stop the scenario on failure.

![A close view of connected metal chain links](chaining-and-state.jpg)
*Chains — Bernard Spragg, CC0 1.0, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Chains._(50630851101).jpg)*
- **Producer link** — A create or login response produces a server-issued value.
- **Validated handoff** — Assertions prove the value is safe before state is stored.
- **Consumer link** — A later request uses the exact captured id or token.

**A safe project lifecycle chain**

1. **Create project** — POST with a unique run name.
2. **Assert + capture projectId** — Store only after status and shape pass.
3. **Read and patch same id** — Consumers reference explicit scenario state.
4. **Delete same id** — Teardown closes the lifecycle.
5. **Unset temporary state** — The next scenario starts clean.

*Run it - validate a state handoff (Python)*

```python
responses = [{"status": 201, "id": 314}, {"status": 200, "id": 314}, {"status": 204}]
state = {}
if responses[0]["status"] == 201 and isinstance(responses[0].get("id"), int):
    state["createdProjectId"] = responses[0]["id"]
print(f"captured={state['createdProjectId']}")
print(f"same_resource={responses[1]['id'] == state['createdProjectId']}")
state.clear()
print(f"state_after_cleanup={state}")
```

*Run it - validate the same handoff (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    int createStatus = 201, createdId = 314, fetchedId = 314;
    Map<String,Integer> state = new HashMap<>();
    if (createStatus == 201) state.put("createdProjectId", createdId);
    System.out.println("captured=" + state.get("createdProjectId"));
    System.out.println("same_resource=" + (fetchedId == state.get("createdProjectId")));
    state.clear();
    System.out.println("state_after_cleanup=" + state);
  }
}
```

### Your first time: Your mission: chain one resource lifecycle

- [ ] Create a uniquely named project — Assert success and an integer id before capture.
- [ ] Store createdProjectId — Use scenario-level state rather than a mysterious global id.
- [ ] GET and PATCH that exact id — Prove each response refers to the captured resource.
- [ ] Delete and clear state — Leave no id for the next independent run.

- **A later request sends /undefined.**
  Fail the producer step before capture and guard that the expected field has the right type.
- **Tests pass only in collection order.**
  Split independent scenarios and give each its own setup; keep chains only inside genuine lifecycles.
- **Parallel workers reuse one id.**
  Use per-run/per-worker variable scopes and unique data instead of shared mutable collection state.

### Where to check

- Producer response status and body before variable assignment.
- Variable scope, current value, and accidental overwrites.
- Collection order, cleanup, and parallel-run namespaces.

### Worked example: create, read, patch, delete without magic ids

`POST /api/v1/projects` returns the project id. The scenario validates and stores it as `createdProjectId`, then uses that value in GET, PATCH, and DELETE URLs. If create fails, consumers do not run. Cleanup unsets the variable, so a future run cannot accidentally act on an old project.

**Quiz.** When should a response value be stored for later requests?

- [ ] Before checking the response
- [x] After validating the producer response and value type
- [ ] Only in a global variable
- [ ] By hard-coding it into the collection

*A validated handoff prevents a failed producer from contaminating later requests with missing or stale state.*

- **Producer** — The request that returns a value needed later.
- **Consumer** — A later request that reads explicitly captured scenario state.
- **Order dependence warning** — Independent tests should create their own prerequisites rather than inherit previous test state.

### Challenge

Model login → create project → create ticket → update ticket → delete ticket → delete project. Mark every produced value, assertion gate, scope, and cleanup action.

### Ask the community

> Our chain loses `[variable]` after `[producer]`; response status, scope, and redacted script are `[details]`.

Never paste bearer tokens, API keys, or sandbox credentials.

- [Postman Docs — Post-response scripts](https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-scripts)
- [Postman Docs — Variables and scopes](https://learning.postman.com/docs/use/send-requests/variables/variables)

🎬 [Postman — How to Write and Automate API Tests in Postman](https://www.youtube.com/watch?v=oXW-C2bM0wE) (13 min)

- Capture server-issued values instead of hard-coding ids and tokens.
- Validate the producer response before storing or consuming state.
- Scope variables to the real scenario lifetime and clear temporary state.
- Use chains for coherent lifecycles, not to make independent tests order-dependent.


## Related notes

- [[Notes/api-test-automation/real-world-api-suites/data-setup-via-api|Data setup via API]]
- [[Notes/api-test-automation/real-world-api-suites/full-api-suite-on-buggyapi|Full API suite on BuggyAPI]]
- [[Notes/api-testing-fundamentals/postman-and-curl/postman-tests-and-variables|Postman tests & variables]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/real-world-api-suites/chaining-and-state.mdx`_
