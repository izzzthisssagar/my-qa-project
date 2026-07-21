---
title: "Given / when / then style"
tags: ["api-test-automation", "rest-assured-java", "track-d"]
updated: "2026-07-17"
---

# Given / when / then style

*REST Assured's recommended given-when-then syntax separates request setup, the HTTP action, and response evidence so failures can be read without archaeology.*

> A fluent chain is useful only when its grammar tells the truth. If `given` secretly performs the request, your test reads like a recipe that bakes the cake while listing ingredients.

> **In real life**
>
> A kitchen recipe stages ingredients, performs the cooking step, then checks the result. REST Assured's phases are the same: arrange the request, act once, assert the response.

**given / when / then**: Given-when-then is REST Assured's recommended BDD-like syntax: given configures request data, when invokes an HTTP operation, and then validates the response.

## Keep each phase honest

```java
given()
  .baseUri(baseUri)
  .header("Accept", "application/json")
  .queryParam("limit", 2)
.when()
  .get("/v1/tickets")
.then()
  .statusCode(200)
  .body("items.size()", lessThanOrEqualTo(2));
```

- `given`: headers, cookies, query/form parameters, auth, and body.
- `when`: exactly the request action — method and path.
- `then`: status, headers, timing where appropriate, and body matchers.

> **Tip**
>
> Use request and response specifications for genuinely repeated setup. Do not hide the one field that makes a test special inside a giant global specification.

> **Common mistake**
>
> Using the legacy `given/expect/when` order copied from REST Assured 1.x material. It still exists, but the official usage guide recommends given/when/then for readability.

![Historic laboratory equipment arranged across a work bench](given-when-then-style.jpg)
*Laboratory equipment on a bench — History Trust of South Australia, Wikimedia Commons, CC0. [Source](https://commons.wikimedia.org/wiki/File:Laboratory_equipment_on_a_bench(GN11961).jpg)*
- **Given** — Inputs and instruments are arranged before the operation.
- **When** — One action transforms the prepared input.
- **Then** — A reading is compared with the expected outcome.

**Read the chain as behavior**

1. **Given request data** — Make prerequisites explicit.
2. **When one method runs** — Send exactly one request.
3. **Then status matches** — Check the protocol outcome.
4. **And body matches** — Check the business result.

*Run it — phase labels expose responsibility (Python)*

```python
request = {"headers": {"Accept": "application/json"}, "limit": 2}
response = {"status": 200, "items": ["T-1", "T-2"]}
print("GIVEN limit =", request["limit"])
print("WHEN  GET /v1/tickets")
print("THEN  status 200 =", response["status"] == 200)
print("AND   item limit =", len(response["items"]) <= request["limit"])

# GIVEN limit = 2
# WHEN  GET /v1/tickets
# THEN  status 200 = True
# AND   item limit = True
```

*Run it — phase labels expose responsibility (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    int limit = 2;
    int status = 200;
    List<String> items = List.of("T-1", "T-2");
    System.out.println("GIVEN limit = " + limit);
    System.out.println("WHEN  GET /v1/tickets");
    System.out.println("THEN  status 200 = " + (status == 200));
    System.out.println("AND   item limit = " + (items.size() <= limit));
  }
}

/* GIVEN limit = 2
   WHEN  GET /v1/tickets
   THEN  status 200 = true
   AND   item limit = true */
```

### Your first time: Your mission: refactor a muddy test

- [ ] Choose a request with headers or query data — You need enough setup to make the phase boundary visible.
- [ ] Move all request preparation under given — No assertion belongs here.
- [ ] Keep only method and path under when — One test should normally have one central HTTP action.
- [ ] Put protocol and body evidence under then — Run once passing and once deliberately failing.

- **The chain will not compile after a line break.**
  Check the preceding dot, parentheses, and static imports; Java formatting is flexible, syntax is not.
- **A query parameter became form data.**
  Use queryParam or formParam explicitly instead of relying on method-sensitive param inference.
- **The failure reveals no request details.**
  Add conditional logging such as log().ifValidationFails(), while redacting credentials.

### Where to check

- `given` for the exact request inputs.
- `when` for the one method/path pair.
- `then` for protocol and business assertions.
- Official usage documentation when old examples disagree with current style.

### Worked example: a pagination test that says what it means

A test sets `limit=2` under `given`, calls `GET /v1/tickets` under `when`, and verifies both `200` and at most two items under `then`. When three items arrive, the failure points at the contract rather than burying the limit inside helper code.

**Quiz.** Which phase should contain the query parameter named limit?

- [x] given
- [ ] when
- [ ] then
- [ ] after the test

*A query parameter prepares request data, so it belongs in given.*

- **given** — Request prerequisites: URI, headers, parameters, auth, and body.
- **when** — The HTTP action: method and path.
- **then** — Response validation: status, headers, and body.
- **Why explicit queryParam?** — It avoids method-dependent inference and tells the reader exactly where data goes.

### Challenge

Rewrite one existing REST Assured test so a reviewer can identify request input, action, and every assertion in under ten seconds.

### Ask the community

> Does this REST Assured chain keep request setup, action, and evidence in the right phases? `[sanitized test]`

Explain which line feels hidden or surprising, not merely whether it compiles.

- [REST Assured — official usage guide](https://github.com/rest-assured/rest-assured/wiki/Usage)
- [REST Assured — official syntax note](https://github.com/rest-assured/rest-assured/wiki/Usage#note-on-syntax)

🎬 [Marco Lenzo — REST APIs explained](https://www.youtube.com/watch?v=RrsRkXR5qaQ) (6 min)

- Given prepares, when sends, then verifies.
- The official guide recommends given/when/then over the legacy ordering in most cases.
- Explicit parameter methods make request placement unambiguous.
- Reusable specifications should remove repetition without hiding the behavior under test.


## Related notes

- [[Notes/api-test-automation/rest-assured-java/setup-and-first-test|Setup & first test]]
- [[Notes/api-test-automation/rest-assured-java/validating-json-and-status|Validating JSON & status]]
- [[Notes/bdd-with-cucumber/bdd-in-plain-words/given-when-then|Given / When / Then]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/rest-assured-java/given-when-then-style.mdx`_
