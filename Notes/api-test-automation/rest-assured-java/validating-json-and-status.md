---
title: "Validating JSON & status"
tags: ["api-test-automation", "rest-assured-java", "track-d"]
updated: "2026-07-17"
---

# Validating JSON & status

*Status checks classify the HTTP outcome; JSON path and Hamcrest checks prove the payload's shape and values. You need both unless your test goal is professionally vague.*

> A `200` containing the wrong customer's data is not a passing API. It is a security meeting with excellent uptime.

> **In real life**
>
> A vernier caliper does not announce “object exists.” It measures the exact dimension. Status is the existence check; body matchers are the measurement.

**response validation**: Response validation compares observable HTTP evidence — status, headers, and parsed body values — with an explicit contract. REST Assured commonly combines response specifications, JSON path expressions, and Hamcrest matchers.

## Assert protocol and payload separately

```java
given().baseUri(baseUri)
.when().get("/v1/tickets/{id}", ticketId)
.then()
  .statusCode(200)
  .contentType(ContentType.JSON)
  .body("id", equalTo(ticketId))
  .body("title", not(blankString()))
  .body("labels", everyItem(instanceOf(String.class)));
```

Use matchers that express intent. `equalTo`, `hasItem`, `hasSize`, `notNullValue`, and numeric
comparisons communicate more than turning the entire response into a string and searching substrings.

> **Tip**
>
> When numbers arrive from JSON, match their actual parsed type or use numeric matchers. A value can look like `1` on screen and still disagree with `1.0` in Java.

> **Common mistake**
>
> Asserting an entire volatile response snapshot when the test cares about three fields. Timestamps and generated IDs then become noise generators.

![Metal vernier caliper used for precision measurement](validating-json-and-status.jpg)
*Vernier caliper — Lgreen, Wikimedia Commons, CC BY 2.5. [Source](https://commons.wikimedia.org/wiki/File:Vernier_caliper.jpg)*
- **Status** — The broad result category: success, client error, or server error.
- **JSON path** — Select the exact response field relevant to the contract.
- **Matcher** — Compare the selected value with a precise expectation.

**Validate from outside inward**

1. **Check status** — Did the protocol operation succeed in the expected category?
2. **Check content type** — Can the body legitimately be interpreted as JSON?
3. **Select JSON path** — Target the field or collection the contract names.
4. **Apply matcher** — Compare value, type, membership, size, or boundary.

*Run it — focused response checks (Python)*

```python
response = {"status": 200, "json": {"id": "T-7", "title": "Broken filter", "labels": ["ui", "regression"]}}
checks = {
    "status": response["status"] == 200,
    "id": response["json"]["id"] == "T-7",
    "title": bool(response["json"]["title"].strip()),
    "labels": all(isinstance(x, str) for x in response["json"]["labels"]),
}
for name, ok in checks.items(): print(f"{name}: {'PASS' if ok else 'FAIL'}")

# status: PASS
# id: PASS
# title: PASS
# labels: PASS
```

*Run it — focused response checks (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    int status = 200;
    Map<String,Object> json = new LinkedHashMap<>();
    json.put("id", "T-7"); json.put("title", "Broken filter");
    json.put("labels", List.of("ui", "regression"));
    System.out.println("status: " + (status == 200 ? "PASS" : "FAIL"));
    System.out.println("id: " + ("T-7".equals(json.get("id")) ? "PASS" : "FAIL"));
    System.out.println("title: " + (!((String)json.get("title")).isBlank() ? "PASS" : "FAIL"));
    boolean labels = ((List<?>)json.get("labels")).stream().allMatch(String.class::isInstance);
    System.out.println("labels: " + (labels ? "PASS" : "FAIL"));
  }
}

/* status: PASS
   id: PASS
   title: PASS
   labels: PASS */
```

### Your first time: Your mission: validate one useful payload

- [ ] Choose a stable GET response — Record its documented status, content type, and required fields.
- [ ] Assert status and JSON content type — Do this before detailed body checks.
- [ ] Add three focused body matchers — Cover identity, a required value, and one collection or type rule.
- [ ] Mutate each expectation once — Confirm the failure names the path and mismatched value.

- **A matcher says Integer was not equal to Float.**
  Inspect the parsed numeric type and use the corresponding literal or a numeric comparison matcher.
- **JSON path returns null.**
  Print the sanitized body and verify nesting, array indexes, and field spelling before weakening the assertion.
- **One body failure hides later checks.**
  Use a deliberate validation strategy; do not assume every chained assertion is reported together.

### Where to check

- The OpenAPI response schema for required fields and types.
- The raw sanitized response for actual nesting and content type.
- REST Assured's JSON path and matcher documentation for selection semantics.

### Worked example: the status passes while identity fails

A ticket request returns `200` with a valid-looking object, but `id` is `T-8` instead of requested `T-7`. The status and content type pass; the identity matcher fails. That focused failure exposes routing or authorization leakage that a status-only test would bless.

**Quiz.** What should you verify before applying JSON path body matchers?

- [ ] Only response time
- [x] Expected status and a JSON content type
- [ ] The entire response as one string
- [ ] Nothing; JSON path accepts HTML

*Status and content type establish that the response is the expected kind before fields are parsed.*

- **Status assertion** — Checks the protocol outcome, not the correctness of every body field.
- **JSON path** — Selects a nested field or collection from a parsed JSON response.
- **Focused matcher** — Checks only the stable behavior the test intends to prove.
- **Why avoid full snapshots?** — Volatile IDs and timestamps create failures unrelated to the test's intent.

### Challenge

Write one response test that detects wrong identity, empty required text, and a non-string element inside a labels array without asserting volatile timestamps.

### Ask the community

> This REST Assured body matcher fails at JSON path `[path]` with expected `[type/value]` and actual `[type/value]`. Which contract assumption is wrong?

Post the schema fragment and sanitized response, not the entire production payload.

- [REST Assured — official JSON path usage](https://github.com/rest-assured/rest-assured/wiki/Usage#json-using-jsonpath)
- [Hamcrest — official Java tutorial](https://hamcrest.org/JavaHamcrest/tutorial)

🎬 [FixITKalia — why use Hamcrest matchers](https://www.youtube.com/watch?v=OxFXIbvbaqI) (4 min)

- Status verifies the broad HTTP outcome; body checks verify the returned behavior.
- Check content type before treating a response as JSON.
- Use focused JSON path and Hamcrest assertions that express the contract.
- Watch numeric types and volatile fields instead of weakening every matcher to strings.


## Related notes

- [[Notes/api-test-automation/rest-assured-java/given-when-then-style|Given / when / then style]]
- [[Notes/api-test-automation/rest-assured-java/auth-in-rest-assured|Auth in REST Assured]]
- [[Notes/api-testing-fundamentals/status-codes-and-rest/status-code-families|2xx / 4xx / 5xx families]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/rest-assured-java/validating-json-and-status.mdx`_
