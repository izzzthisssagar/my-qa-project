---
title: "Test pyramids for APIs"
tags: ["api-test-automation", "real-world-api-suites", "track-d"]
updated: "2026-07-17"
---

# Test pyramids for APIs

*Build most confidence below the browser, keep a focused API layer for service behavior, and reserve full end-to-end journeys for risks only the whole system can reveal.*

> If every rule needs a browser, the test suite has hired a chauffeur to cross the kitchen. API checks sit where rich behavior is observable without paying the full UI tax.

> **In real life**
>
> A pyramid carries most weight in its broad base. Tests work similarly: many focused checks below, fewer service integrations, and a thin cap of expensive whole-system journeys.

**API test pyramid**: An API test pyramid is a portfolio heuristic: many fast unit/component tests support a substantial but smaller service/API layer, with few full end-to-end checks. It is not a mandated percentage; architecture, risk, feedback time, and maintenance cost determine the useful shape.

## Put each risk at the cheapest revealing layer

Pure validation rules belong in unit tests. HTTP serialization, authentication, persistence boundaries, and endpoint contracts earn API tests. A handful of browser or cross-service journeys prove wiring the API layer cannot see. Duplication across every layer adds runtime without automatically adding information.

> **Tip**
>
> Ask “what is the lowest layer that can fail for the right reason?” before adding another end-to-end test.

> **Common mistake**
>
> Do not turn the pyramid into a quota. Ten fragile API checks are not improved by inventing ninety trivial unit tests to reach a slide-deck ratio.

![The Great Pyramid of Giza rising above a modern city street in a black-and-white photograph](test-pyramids-for-apis.jpg)
*Great Pyramid Giza — Ireneusz Jerzy Borysiewicz, CC BY-SA 4.0, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Great_Pyramid_Giza.jpg)*
- **Broad stone base** — Like fast focused checks, the widest layer carries most of the structure's weight.
- **Narrower middle** — The API layer is substantial but more selective: contracts, auth, HTTP behavior, and persistence wiring.
- **Tiny apex** — Only critical end-to-end journeys pay the highest setup and diagnosis cost.

**Place a risk at the right layer**

1. **Name the risk** — Example: unauthorized users must not create tickets.
2. **Find the lowest revealing layer** — Middleware unit test may cover branching; HTTP test proves wiring.
3. **Add only missing evidence** — Avoid repeating identical assertions at every layer.
4. **Measure feedback** — Runtime, flake rate, and diagnostic value reshape the portfolio.

*Run it - allocate risks by cheapest revealing layer (Python)*

```python
risks = {"title validation": "unit", "auth header wiring": "api", "browser login journey": "e2e", "pagination contract": "api"}
for layer in ("unit", "api", "e2e"):
    names = [risk for risk, owner in risks.items() if owner == layer]
    print(f"{layer}: {len(names)} -> {', '.join(names)}")
```

*Run it - allocate the same risks (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    Map<String,String> risks = new LinkedHashMap<>();
    risks.put("title validation","unit"); risks.put("auth header wiring","api");
    risks.put("browser login journey","e2e"); risks.put("pagination contract","api");
    for (String layer : List.of("unit","api","e2e")) {
      List<String> names = risks.entrySet().stream().filter(e -> e.getValue().equals(layer)).map(Map.Entry::getKey).toList();
      System.out.println(layer + ": " + names.size() + " -> " + String.join(", ", names));
    }
  }
}
```

### Your first time: Your mission: map twelve API risks

- [ ] List business, protocol, contract, and journey risks — Start from failure impact, not existing test folders.
- [ ] Assign the lowest revealing layer — Unit, component, API integration, contract, or end-to-end.
- [ ] Mark intentional overlap — Overlap needs a reason such as contract plus runtime wiring.
- [ ] Set a feedback budget — Decide what must finish on a pull request versus nightly.

- **The API suite takes longer than the UI suite.**
  Audit repeated setup, broad data resets, network dependencies, and scenarios that belong below HTTP.
- **Unit tests pass but deployed API is broken.**
  Add focused integration checks for routing, serialization, middleware, and persistence wiring.
- **The same defect fails dozens of tests.**
  Remove redundant journeys and keep one strong assertion at each layer that adds distinct evidence.

### Where to check

- Risk-to-layer map and intentional overlaps.
- Runtime, flake rate, setup cost, and first-failure diagnostic clarity by layer.
- Gaps around auth, schema, persistence, and critical journeys.

### Worked example: ticket creation at three useful depths

A unit test covers title-length rules. An API test posts an authenticated ticket and verifies status, response shape, and persisted retrieval. One browser journey proves the UI sends a valid request. The three checks overlap on the feature but fail for different reasons and answer different questions.

**Quiz.** Which claim best describes a test pyramid?

- [ ] A fixed 70/20/10 quota
- [x] A heuristic for placing risk at cheaper, faster layers while retaining necessary integration evidence
- [ ] A ban on API tests
- [ ] A CI report format

*The pyramid guides portfolio economics; it is not a universal percentage or a reason to skip real integration risks.*

- **API layer earns its place by testing?** — HTTP contracts, auth, serialization, persistence wiring, and service behavior.
- **Why few end-to-end tests?** — They cost more to set up, run, and diagnose, so reserve them for risks only the full system reveals.
- **Is the pyramid a quota?** — No. It is a risk and feedback heuristic.

### Challenge

Take one feature with ten current end-to-end cases. Reassign each assertion to the lowest revealing layer and keep only journeys that prove unique wiring.

### Ask the community

> Our API portfolio is slow around `[domain]`; current layers, runtimes, and duplicate assertions are `[details]`.

Bring measurements before proposing a prettier triangle.

- [Google Testing Blog — Just Say No to More End-to-End Tests](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html)
- [Martin Fowler — The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

🎬 [Building Quality Gates in DevOps CI/CD Pipelines — DheerajTechInsight](https://www.youtube.com/watch?v=90auAVyZswc) (31 min)

- Place each risk at the lowest layer that can fail for the right reason.
- Use API tests for protocol and service wiring, not every pure rule.
- Keep only a thin set of whole-system journeys with unique evidence.
- Reshape the portfolio using runtime, flake, maintenance, and diagnosis data—not quotas.


## Related notes

- [[Notes/api-test-automation/real-world-api-suites/data-setup-via-api|Data setup via API]]
- [[Notes/api-test-automation/real-world-api-suites/full-api-suite-on-buggyapi|Full API suite on BuggyAPI]]
- [[Notes/levels-and-types-of-testing/test-levels/integration|Integration]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/real-world-api-suites/test-pyramids-for-apis.mdx`_
