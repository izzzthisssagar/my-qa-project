---
title: "OpenAPI as the contract"
tags: ["api-test-automation", "contract-and-schema-testing", "track-d"]
updated: "2026-07-17"
---

# OpenAPI as the contract

*An OpenAPI document is executable agreement, not decorative Swagger wallpaper. Learn what it promises, what it does not, and how automation turns drift into a failing build.*

> Swagger UI is the shop window. The OpenAPI document behind it is the inventory ledger. Testing the
> window while ignoring the ledger is how teams ship a beautiful page describing an API that no longer exists.

> **In real life**
>
> A blueprint names every doorway before the builders arrive. OpenAPI does the same for paths, operations, parameters, request bodies, responses, and schemas; automation is the inspector with the ruler.

**OpenAPI contract**: An OpenAPI Description is a machine-readable description of an HTTP API. It records paths and operations plus their inputs, responses, security requirements, and schemas so tools can document, generate, mock, and test the same declared interface.

## Read the promise in layers

- `paths` and HTTP operations say which calls exist.
- parameters and request bodies say which inputs are accepted and required.
- responses map status codes to headers and body schemas.
- components hold reusable schemas and security schemes.
- in OpenAPI 3.1, Schema Objects use the OAS dialect based on JSON Schema Draft 2020-12.

> **Tip**
>
> Pin an exact OpenAPI version and validate the document itself before testing traffic. A malformed contract cannot reliably judge a response.

> **Common mistake**
>
> A generated OpenAPI file is not automatically truthful. If it is generated from annotations that nobody reviews, the code and its description can be wrong together.

![A historical architectural plan showing two building elevations above a detailed floor and grounds plan](openapi-as-the-contract.jpg)
*Architectural drawing, British Museum 1972,U.808 — Wikimedia Commons, public domain. [Source](https://commons.wikimedia.org/wiki/File:Drawing,_plan,_architectural_drawing_(BM_1972,U.808).jpg)*
- **Declared exterior** — The elevations publish what consumers should see from outside, like an operation's public request and response surface.
- **Detailed floor plan** — The machine-readable contract maps each defined component and connection instead of leaving clients to guess the interior.
- **Related grounds** — Referenced structures remain part of the same plan without duplicating the central building definition.

**Contract to executable check**

1. **Parse the OpenAPI document** — Fail fast if the contract itself is invalid.
2. **Choose an operation and response** — Resolve its path, method, status, and media type.
3. **Send a representative request** — Capture status, headers, and body without paraphrasing.
4. **Validate against the declaration** — Compare status and body with the documented response schema.
5. **Publish the exact mismatch** — Point to both the contract location and instance location.

*Run it — check documented operations (Python)*

```python
contract = {
    "/tickets": {"get": [200], "post": [201, 400]},
    "/tickets/{id}": {"get": [200, 404]},
}

observed = [("/tickets", "get", 200), ("/tickets", "post", 200)]
for path, method, status in observed:
    allowed = contract.get(path, {}).get(method, [])
    verdict = "PASS" if status in allowed else "CONTRACT FAIL"
    print(f"{method.upper()} {path} -> {status}: {verdict} (declared {allowed})")

# GET /tickets -> 200: PASS (declared [200])
# POST /tickets -> 200: CONTRACT FAIL (declared [201, 400])
```

*Run it — check documented operations (Java)*

```java
import java.util.*;

public class Main {
  public static void main(String[] args) {
    Map<String, Set<Integer>> contract = new LinkedHashMap<>();
    contract.put("GET /tickets", Set.of(200));
    contract.put("POST /tickets", Set.of(201, 400));
    Map<String, Integer> observed = new LinkedHashMap<>();
    observed.put("GET /tickets", 200);
    observed.put("POST /tickets", 200);
    observed.forEach((operation, status) -> {
      Set<Integer> allowed = contract.getOrDefault(operation, Set.of());
      String verdict = allowed.contains(status) ? "PASS" : "CONTRACT FAIL";
      System.out.println(operation + " -> " + status + ": " + verdict + " (declared " + allowed + ")");
    });
  }
}

/* GET /tickets -> 200: PASS (declared [200])
   POST /tickets -> 200: CONTRACT FAIL (declared [201, 400]) */
```

### Your first time: Your mission: turn one OpenAPI operation into a check

- [ ] Open the raw OpenAPI JSON or YAML — Use the machine document, not only rendered Swagger UI.
- [ ] Trace one path and method — Record parameters, request body, and declared responses.
- [ ] Call the endpoint — Capture the unmodified status and body.
- [ ] Compare the response — Report the exact contract and instance paths for any mismatch.

You have converted documentation into an executable decision.

- **A referenced schema cannot be resolved.**
  Resolve relative references from the document location and make external contracts available in CI.
- **The response status is real but absent from the contract.**
  Treat it as drift: either document the supported response intentionally or correct the provider.
- **OpenAPI 3.0 and 3.1 tools disagree.**
  Check the declared OpenAPI version and use a validator that supports that version's Schema Object dialect.

### Where to check

- The root `openapi` version and document-validation output.
- The exact `paths` operation and `responses` entry.
- Referenced schemas under `components` and their resolved URLs.
- CI artifacts containing the contract version tested.

### Worked example: the undocumented success status

1. The contract declares `POST /tickets` responses `201` and `400`.
2. A deployment starts returning `200` with a valid-looking ticket body.
3. Functional assertions pass because the body is usable.
4. The contract check fails at `paths./tickets.post.responses` because `200` is not promised.
5. The team decides whether the provider regressed or the public contract needs an intentional review.

**Quiz.** A response body matches a component schema, but its HTTP status is not declared for the operation. What is the contract verdict?

- [ ] Pass, because schema is all OpenAPI validates
- [x] Fail, because the operation's response contract includes the status code
- [ ] Pass if Swagger UI renders it
- [ ] Ignore unless a consumer complains

*OpenAPI describes the operation's responses by status as well as their content. A valid body under an undeclared status is still drift.*

- **OpenAPI Description** — Machine-readable HTTP API interface: operations, inputs, responses, security, and schemas.
- **Schema Object in OAS 3.1** — Uses the OpenAPI dialect built on JSON Schema Draft 2020-12.
- **Contract drift** — Runtime behavior and the declared interface no longer agree.

### Challenge

Choose two operations, list every declared success and error status, and make a tiny checker fail on one deliberately undeclared observation. Preserve the contract path in the failure message.

### Ask the community

> My OpenAPI contract and runtime disagree at `[operation/status/schema path]`. The producer says `[reason]`. Should the provider or contract change first, and what compatibility evidence would you require?

Include the exact contract version and response; otherwise everyone will debate a different API.

- [OpenAPI Specification 3.1 — official specification](https://spec.openapis.org/oas/v3.1.0)
- [JSON Schema Draft 2020-12 — official specification set](https://json-schema.org/draft/2020-12)

🎬 [Understand OpenAPI in 5 Minutes With Examples — florianjsx](https://www.youtube.com/watch?v=PenvYHJ9Koc) (5 min)

- OpenAPI is an executable interface contract, not merely rendered documentation.
- Validate paths, operations, statuses, media types, and schemas together.
- OpenAPI 3.1 Schema Objects use an OAS dialect based on JSON Schema Draft 2020-12.
- A generated contract can still drift or encode the same mistake as the implementation.
- Contract failures should name both the declaration path and observed instance path.


## Related notes

- [[Notes/api-testing-fundamentals/status-codes-and-rest/reading-api-docs-and-swagger|Reading API docs & Swagger]]
- [[Notes/api-testing-fundamentals/finding-api-bugs/validating-against-the-spec|Validating against the spec]]
- [[Notes/api-test-automation/contract-and-schema-testing/schema-validation|Schema validation]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/contract-and-schema-testing/openapi-as-the-contract.mdx`_
