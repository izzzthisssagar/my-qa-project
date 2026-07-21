---
title: "Testing a GraphQL API"
tags: ["api-test-automation", "graphql-and-soap-testing", "track-d"]
updated: "2026-07-17"
---

# Testing a GraphQL API

*A GraphQL test must judge transport, request validation, execution, partial data, null propagation, and field authorization. Build assertions that know which layer failed.*

> A GraphQL response can say, with a straight face, "here is most of your data and also the exact place something exploded." Your assertion has to be at least as nuanced as the protocol.

> **In real life**
>
> A switchboard can connect most calls while one line fails. The useful report names the failed socket and destination; GraphQL errors use locations and paths for the same reason.

**GraphQL API testing**: GraphQL API testing validates an operation through distinct layers: HTTP transport, document parsing and validation, variable coercion, field execution, response shape, error paths, null propagation, authorization, and any observable side effects.

## Build a layered assertion

1. Assert expected transport behavior for the server's GraphQL-over-HTTP setup.
2. For request errors, expect `errors` and no `data` because execution never began.
3. For field errors, expect `data` plus `errors`, then assert the error `path` and permitted partial result.
4. Validate selected response fields and non-null propagation.
5. Test authorization at fields and nested objects, not only endpoint access.
6. Add complexity/depth limits and alias-heavy cases where the server enforces them.

> **Tip**
>
> Use named operations and retain the full response in test artifacts. Error `message` text may change; paths, codes in extensions, and response semantics are often more stable assertions.

> **Common mistake**
>
> Treating any `errors` key as identical. Request errors prevent execution and omit data; field errors happen during execution and can produce partial data.

![A historical telephone switchboard operator working among cables and sockets](testing-a-graphql-api.jpg)
*Switchboard Operator — Hennepin County Library via DPLA, Wikimedia Commons, public domain in the United States. [Source](https://commons.wikimedia.org/wiki/File:Switchboard_Operator_-_DPLA_-_8f9fd946fc77b4c3fa421d77f1464b00.jpg)*
- **The operator** — GraphQL execution resolves fields and routes their results into the response tree.
- **Individual sockets** — A field error is local and should identify its exact response path.
- **Many live lines** — Other fields may continue and return partial data even when one line fails.

**Classify before asserting**

1. **Send a named operation and variables** — Capture request and full response as one artifact.
2. **Did parsing or validation fail?** — Execution never starts; expect errors and no data entry.
3. **Did a field fail during execution?** — Expect partial data where allowed and an error path to the response position.
4. **Apply nullability rules** — A null at a non-null position propagates to the nearest nullable parent.
5. **Assert business state and authorization** — Protocol correctness is necessary, not sufficient.

*Run it — classify GraphQL responses (Python)*

```python
responses = {
    "success": {"data": {"ticket": {"id": "T-7"}}},
    "request_error": {"errors": [{"message": "Unknown field"}]},
    "field_error": {"data": {"ticket": None}, "errors": [{"message": "Denied", "path": ["ticket"]}]},
}

for name, body in responses.items():
    if "errors" not in body:
        kind = "success"
    elif "data" not in body:
        kind = "request error: execution did not begin"
    else:
        kind = f"field error with partial data at {body['errors'][0].get('path')}"
    print(f"{name}: {kind}")

# success: success
# request_error: request error: execution did not begin
# field_error: field error with partial data at ['ticket']
```

*Run it — assert a field-error path (Java)*

```java
import java.util.*;

public class Main {
  public static void main(String[] args) {
    Map<String, Object> response = new LinkedHashMap<>();
    response.put("data", Map.of("viewer", Map.of("publicName", "Asha", "email", "<null>")));
    response.put("errors", List.of(Map.of("message", "Forbidden", "path", List.of("viewer", "email"))));
    List<?> errors = (List<?>) response.get("errors");
    Map<?, ?> first = (Map<?, ?>) errors.get(0);
    boolean rightPath = Objects.equals(first.get("path"), List.of("viewer", "email"));
    System.out.println("partial data present: " + response.containsKey("data"));
    System.out.println("authorization error at viewer.email: " + rightPath);
  }
}

/* partial data present: true
   authorization error at viewer.email: true */
```

### Your first time: Your mission: test all three response classes

- [ ] Run one valid named query — Assert selected shape and absence of errors.
- [ ] Send one invalid field — Assert request error, errors present, and data absent.
- [ ] Trigger one resolver or authorization error — Assert partial data and the exact error path.
- [ ] Exercise one non-null boundary — Predict and verify how null propagates to its parent.

You now test the response model instead of reducing it to a status code.

- **Error message wording changes and tests fail.**
  Prefer stable error extension codes and paths; use exact message checks only when wording is the contract.
- **A nested authorization test leaks a forbidden field.**
  Assert both the field value/null behavior and an error path; endpoint authentication alone is not field authorization.
- **A null wipes out more data than expected.**
  Trace non-null types from the failing response position to the nearest nullable parent.

### Where to check

- Full request document, operation name, and variables.
- Top-level `data`, `errors`, and optional `extensions`.
- Error `locations` and `path` for field-level failures.
- Schema nullability and authorization directives/resolver policy.

### Worked example: the forbidden email that should not erase the profile

1. A viewer may read `publicName` but not another user's `email`.
2. The query requests both fields.
3. Execution returns `publicName`, null for `email`, and an error path `viewer.email` where schema nullability permits partial data.
4. The test asserts no email leak, the exact path, and preservation of allowed data.
5. A blanket "no errors" assertion would reject correct partial behavior; a status-only assertion would miss the authorization evidence.

**Quiz.** A GraphQL document contains an unknown field and fails validation before execution. Which response shape should the test expect?

- [ ] Data only
- [x] Errors present and no data entry
- [ ] Partial data must always exist
- [ ] An XML fault

*Request errors occur before execution; the specification requires errors and says data must not be present.*

- **Request error** — Parsing, validation, operation selection, or variable problem before execution; errors present, data absent.
- **Field error** — Execution-time failure at a response position; partial data may be returned with errors.
- **Error path** — Route through the response object to the field where execution failed.

### Challenge

Create a table of six GraphQL tests: success, syntax error, unknown field, wrong variable type, forbidden nested field, and non-null propagation. Predict data/errors presence for each before running.

### Ask the community

> Operation `[name]` returns data `[shape]` and error path `[path]` under schema nullability `[types]`. Is this correct propagation, or is the resolver/schema wrong?

Post the smallest schema slice and unedited response.

- [GraphQL Specification — Response and errors](https://spec.graphql.org/September2025/#sec-Response)
- [GraphQL Foundation — Response](https://graphql.org/learn/response/)

🎬 [Modern GraphQL Crash Course — Laiture](https://www.youtube.com/watch?v=qux4-yWeZvo) (210 min)

- GraphQL testing spans transport, validation, coercion, execution, response shape, and business state.
- Request errors omit data because execution never began.
- Field errors may return partial data and should identify their response path.
- Non-null failures propagate to the nearest nullable parent.
- Authorization tests belong at field boundaries, including nested fields.


## Related notes

- [[Notes/api-test-automation/graphql-and-soap-testing/graphql-vs-rest|How GraphQL differs from REST]]
- [[Notes/api-test-automation/graphql-and-soap-testing/queries-mutations-and-schema|Queries, mutations & the schema]]
- [[Notes/api-test-automation/contract-and-schema-testing/breaking-change-detection|Breaking-change detection]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/graphql-and-soap-testing/testing-a-graphql-api.mdx`_
