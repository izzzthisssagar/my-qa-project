---
title: "GraphQL vs REST"
tags: ["api-test-automation", "graphql-and-soap-testing", "track-d"]
updated: "2026-07-17"
---

# GraphQL vs REST

*GraphQL is not REST with curly braces. Learn how one typed field-selection endpoint changes test design, error assertions, caching assumptions, and coverage.*

> REST gives you a menu of resource endpoints. GraphQL gives you one kitchen door and lets every customer write a precise order. Reusing the same test checklist for both is how you verify the door and miss the meal.

> **In real life**
>
> A fixed menu item arrives with the chef's chosen sides; a custom order names only what you want. REST commonly returns a server-shaped representation, while a GraphQL selection set shapes the response field by field.

**GraphQL API**: GraphQL is a typed query language and execution specification for APIs. Clients send operations against a schema and select fields down to scalar or enum leaves; the response data mirrors the selection shape, with errors represented separately.

## The test surface moves

- REST commonly spreads behavior across resource URLs and HTTP methods; GraphQL commonly exposes operations through one HTTP endpoint.
- GraphQL selection sets let clients request nested related fields in one operation.
- The schema defines types, fields, arguments, nullability, and root operation types.
- A GraphQL response may contain both partial `data` and `errors`; HTTP 200 alone is not a pass.
- Test operation complexity, authorization at field boundaries, aliases, variables, and null propagation.

> **Tip**
>
> Compare architectures by contract, not slogans. GraphQL can reduce round trips for a particular screen, but a deliberately designed REST endpoint can also return the needed representation.

> **Common mistake**
>
> Asserting only HTTP status against GraphQL. Execution errors can coexist with partial data, so inspect both top-level `data` and `errors`.

![An open restaurant menu with many individually listed choices](graphql-vs-rest.jpg)
*A restaurant menu — Sergiy Galyonkin, Wikimedia Commons, CC BY-SA 2.0. [Source](https://commons.wikimedia.org/wiki/File:A_restaurant_menu_(52369791551).jpg)*
- **Fixed offerings** — REST resources commonly expose server-designed representations at distinct routes.
- **Selected details** — A GraphQL client names exactly the fields required for this operation.
- **One order, many choices** — Related objects can be traversed in one selection tree, with cost and authorization still needing tests.

**How the same screen drives different tests**

1. **List the screen's data needs** — Ticket identity, reporter, and project name.
2. **REST follows resource representations** — Call one or more documented URLs and assert each response contract.
3. **GraphQL follows a selection tree** — Send one named operation selecting nested fields.
4. **Validate protocol-specific failure signals** — REST status/body rules differ from GraphQL data/errors and null propagation.
5. **Assert the same business outcome** — Architecture changes transport evidence, not the user's expectation.

*Run it — compare response shape to a selection (Python)*

```python
selection = {"ticket": {"id": None, "status": None, "project": {"name": None}}}
response = {"ticket": {"id": "T-7", "status": "open", "project": {"name": "Apollo"}}}

def shape_matches(selected, actual, path="data"):
    errors = []
    for field, nested in selected.items():
        if field not in actual:
            errors.append(f"{path}.{field}: selected field missing")
        elif nested is not None:
            errors += shape_matches(nested, actual[field], f"{path}.{field}")
    return errors

errors = shape_matches(selection, response)
print("PASS: response mirrors selection" if not errors else "FAIL: " + str(errors))

# PASS: response mirrors selection
```

*Run it — distinguish transport and GraphQL verdicts (Java)*

```java
import java.util.*;

public class Main {
  public static void main(String[] args) {
    int httpStatus = 200;
    Map<String, Object> graphql = new LinkedHashMap<>();
    Map<String, Object> partialData = new LinkedHashMap<>();
    partialData.put("ticket", null);
    graphql.put("data", partialData);
    graphql.put("errors", List.of(Map.of("message", "Not authorized", "path", List.of("ticket"))));
    System.out.println("HTTP check: " + (httpStatus == 200 ? "PASS" : "FAIL"));
    boolean executionPass = !graphql.containsKey("errors");
    System.out.println("GraphQL execution check: " + (executionPass ? "PASS" : "FAIL"));
  }
}

/* HTTP check: PASS
   GraphQL execution check: FAIL */
```

### Your first time: Your mission: translate one REST check into GraphQL

- [ ] Choose one REST-backed screen — List the exact fields the UI consumes.
- [ ] Write a named GraphQL query — Select the same data, including nested fields.
- [ ] Assert response shape and errors — Do not stop at HTTP 200.
- [ ] Test one forbidden nested field — Field-level authorization is part of the new surface.

You now compare equivalent user evidence without pretending the protocols are identical.

- **A GraphQL test passes on HTTP 200 despite a blank widget.**
  Inspect errors, its path, and null propagation in data.
- **One query becomes slow as fields are added.**
  Measure resolver behavior and operation complexity; one HTTP request is not one backend operation.
- **REST cache assumptions fail.**
  GraphQL over HTTP often posts operations to one URL; verify the actual caching layer and persisted-query strategy.

### Where to check

- GraphQL schema root types, fields, arguments, and nullability.
- Named operation, variables, selection set, and top-level response keys.
- Resolver traces and authorization at nested fields.
- GraphQL-over-HTTP configuration rather than generic REST assumptions.

### Worked example: the HTTP 200 that still broke the ticket card

1. A ticket query selects `id`, `status`, and nested `project.name`.
2. The server returns HTTP 200 and `data.ticket.project: null` plus an `errors` entry at that path.
3. A REST-style status-only test passes.
4. A GraphQL-aware assertion fails on the error path and unexpected null propagation.
5. The defect points to the project resolver or field authorization, not the transport.

**Quiz.** Why is HTTP 200 insufficient as a GraphQL success assertion?

- [ ] GraphQL never uses HTTP
- [x] A response can include partial data and execution errors
- [ ] Every GraphQL response is XML
- [ ] Status codes are random

*The GraphQL response contract permits partial data alongside field errors, so the response body carries essential execution status.*

- **Selection set** — Fields the client requests, nested down to scalar or enum leaves.
- **Response shape** — The data result mirrors the requested field structure.
- **Protocol-aware assertion** — Checks GraphQL data/errors semantics in addition to HTTP transport.

### Challenge

Take one REST test and design an equivalent GraphQL operation. Identify three new cases caused by selection flexibility: omitted field, forbidden nested field, and partial error.

### Ask the community

> For feature `[screen]`, REST needs `[calls]` while GraphQL operation `[name]` selects `[fields]`. Which GraphQL-specific failure paths should the automation add?

Include schema nullability and authorization boundaries, not just query text.

- [GraphQL Foundation — Queries](https://graphql.org/learn/queries/)
- [GraphQL Specification — Response](https://spec.graphql.org/September2025/#sec-Response)

🎬 [GraphQL Explained in 100 Seconds — Fireship](https://www.youtube.com/watch?v=eIQh02xuVw4) (2 min)

- GraphQL clients select response fields through a typed schema; REST commonly exposes server-shaped resources.
- One GraphQL request can traverse nested data, but one request is not automatically cheap.
- GraphQL tests must inspect data, errors, paths, and null propagation in addition to HTTP status.
- Selection flexibility adds field authorization and complexity cases.
- Compare equivalent business outcomes while respecting each protocol's contract.


## Related notes

- [[Notes/api-testing-fundamentals/status-codes-and-rest/rest-in-plain-words|REST in plain words]]
- [[Notes/api-test-automation/graphql-and-soap-testing/queries-mutations-and-schema|Queries, mutations & the schema]]
- [[Notes/api-test-automation/graphql-and-soap-testing/testing-a-graphql-api|Testing a GraphQL API]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/graphql-and-soap-testing/graphql-vs-rest.mdx`_
