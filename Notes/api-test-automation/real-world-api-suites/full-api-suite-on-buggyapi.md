---
title: "Full API suite on BuggyAPI"
tags: ["api-test-automation", "real-world-api-suites", "track-d"]
updated: "2026-07-17"
---

# Full API suite on BuggyAPI

*Assemble a risk-based, isolated suite across BuggyAPI health, authentication, projects, tickets, contracts, and cleanup—without encoding hidden bug answers.*

> A “full suite” is not every endpoint hit once. It is a deliberate system of contracts, lifecycles, negative boundaries, isolation, and evidence that still tells the truth on run fifty.

> **In real life**
>
> Mission control does not watch one light and declare the spacecraft healthy. Separate consoles watch separate risks, then combine signals into one operational picture.

**Full BuggyAPI suite**: A full BuggyAPI suite is a layered, sandbox-scoped collection of independent scenarios covering public health and OpenAPI surfaces, authentication, project and ticket lifecycles, filtering and pagination, negative permissions and validation, plus reliable cleanup. It tests documented behavior without embedding private seeded-bug manifests or answers.

## Build from public behavior and risk

Start with `/api/health`, `/api/v1/openapi.json`, and the interactive docs at `/api/docs`. Authenticated REST routes include `/api/v1/me`, projects, tickets, and ticket attachments; the host also exposes GraphQL and SOAP practice surfaces. Use only credentials provisioned for your own sandbox. Derive assertions from the public contract and observed requirements, never from internal seeded-bug files.

> **Tip**
>
> Tag scenarios `smoke`, `contract`, `lifecycle`, `negative`, and `regression`. A suite becomes operable when CI can select risk, not just “run everything.”

> **Common mistake**
>
> Do not assert one enormous response snapshot. It couples the suite to irrelevant values and hides which contract actually broke.

![NASA mission control room during a Space Shuttle simulation with rows of consoles and large status screens](full-api-suite-on-buggyapi.jpg)
*Mission Control Center during STS-114 simulation — NASA, public domain, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Mission_control_center.jpg)*
- **Auth and readiness console** — Fast smoke proves the target and credentials before deeper scenarios begin.
- **Lifecycle consoles** — Projects and tickets are independent domains with owned setup and cleanup.
- **Shared status screens** — Reports combine domain signals while keeping each failing assertion identifiable.

**BuggyAPI suite architecture**

1. **Health + public contract** — Confirm target identity and load the OpenAPI source.
2. **Authenticate own sandbox** — Verify principal through /api/v1/me.
3. **Independent domain scenarios** — Projects, tickets, filters, pagination, and negatives arrange their own data.
4. **Contract + behavior assertions** — Check focused status, headers, shape, and business invariants.
5. **Scoped cleanup + report** — Delete owned resources and retain actionable evidence.

*Run it - build a risk-based BuggyAPI execution plan (Python)*

```python
suites = {"smoke": 4, "contract": 7, "lifecycle": 9, "negative": 6}
total = 0
for name, count in suites.items():
    total += count
    print(f"{name}: {count} scenarios")
print(f"total={total}")
print("order=smoke -> contract -> lifecycle -> negative -> cleanup")
```

*Run it - build the same execution plan (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    Map<String,Integer> suites = new LinkedHashMap<>();
    suites.put("smoke",4); suites.put("contract",7); suites.put("lifecycle",9); suites.put("negative",6);
    int total = 0;
    for (var entry : suites.entrySet()) { total += entry.getValue(); System.out.println(entry.getKey() + ": " + entry.getValue() + " scenarios"); }
    System.out.println("total=" + total);
    System.out.println("order=smoke -> contract -> lifecycle -> negative -> cleanup");
  }
}
```

### Your first time: Your mission: assemble the capstone suite

- [ ] Prove /api/health and load /api/v1/openapi.json — Use the public contract as the source, not internal code comments.
- [ ] Authenticate and verify /api/v1/me — Use only your provisioned sandbox credentials.
- [ ] Cover isolated project and ticket lifecycles — Each scenario captures ids and owns cleanup.
- [ ] Add focused negative and contract checks — Assert documented invariants without revealing seeded bug answers.
- [ ] Run headlessly with reports — Make smoke selectable for PRs and broader coverage schedulable.

- **Every scenario fails with 401.**
  Stop after auth smoke; inspect header scheme, credential source, expiry, and sandbox identity before running domain tests.
- **Runs interfere with another learner.**
  Verify every request uses your sandbox credentials and every created name has your unique run id.
- **One create failure causes twenty red requests.**
  Gate dependent steps on validated setup and report the first causal failure; skip unsafe consumers.
- **Suite passes while cleanup fails.**
  Report cleanup as a distinct failure because leaked state will corrupt future runs.

### Where to check

- `/api/health`, `/api/docs`, and `/api/v1/openapi.json` for public runtime truth.
- The authenticated principal from `/api/v1/me` and sandbox-scoped credentials.
- Run-id names, captured ids, first causal failure, and cleanup ledger.
- CLI/JUnit/JSON results grouped by smoke, contract, lifecycle, and negative tags.

### Worked example: one full run that remains diagnosable

Smoke verifies health, OpenAPI availability, auth, and `/me`. Contract checks validate focused response shapes. Project and ticket scenarios each create uniquely named data, capture server ids, test read/update/delete behavior and documented filters, then clean their own records. Negative cases use fresh setup and explicit invalid inputs. Reports identify the domain and first failed invariant—never a hidden bug label.

**Quiz.** What is the correct source for BuggyAPI assertions in this learner suite?

- [ ] Private seeded-bug files
- [x] The public OpenAPI/docs and stated behavior
- [ ] Another learner's captured responses
- [ ] Whatever makes the test pass

*The exercise is to discover and test public behavior. Encoding hidden manifests leaks answers and makes the suite dishonest.*

- **BuggyAPI public starting points** — /api/health, /api/docs, and /api/v1/openapi.json.
- **Core suite domains** — Auth identity, projects, tickets, filtering/pagination, contracts, negatives, and cleanup.
- **Capstone isolation rule** — Use only your sandbox and delete only ids created by your run.
- **What never belongs in the notes?** — Private seeded-bug manifests, labels, or answer-revealing assertions.

### Challenge

Create a collection plan with at least four smoke, six contract, eight lifecycle, and six negative scenarios. For each, state its public requirement, setup ownership, first assertion, and cleanup rule—without naming any seeded defect.

### Ask the community

> My BuggyAPI suite first fails at `[public route/assertion]`; run tag, redacted response shape, and owned setup ids are `[details]`.

Do not share sandbox keys, passwords, tokens, internal manifests, or discovered answer lists.

- [Postman Docs — Test script examples](https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-examples/)
- [Postman Docs — Run and test collections](https://learning.postman.com/docs/collections/running-collections/running-collections-overview)

🎬 [API Challenges: a practice API application for testing tutorials — EvilTester](https://www.youtube.com/watch?v=rxEwPMM_Qyc) (8 min)

- Build the suite from public contracts and risk, never hidden seeded-bug answers.
- Separate smoke, contract, lifecycle, negative, and regression coverage so CI can select intent.
- Use only your sandbox, unique run data, captured ids, and scoped cleanup.
- Stop cascades at failed setup and report the first causal invariant with actionable evidence.
- A full suite is operable, repeatable, and diagnosable—not merely large.


## Related notes

- [[Notes/api-test-automation/real-world-api-suites/test-pyramids-for-apis|Test pyramids for APIs]]
- [[Notes/api-test-automation/real-world-api-suites/data-setup-via-api|Data setup via API]]
- [[Notes/api-test-automation/real-world-api-suites/chaining-and-state|Chaining & state]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/real-world-api-suites/full-api-suite-on-buggyapi.mdx`_
