---
title: "REST Assured setup & first test"
tags: ["api-test-automation", "rest-assured-java", "track-d"]
updated: "2026-07-17"
---

# REST Assured setup & first test

*Add REST Assured to a Java test project, set a base URI, send one request, and make the response prove its status instead of merely printing JSON and hoping for applause.*

> Installing a library is not an API test. It is shelving a tool. Your first useful REST Assured test
> must send a known request and fail loudly when the response breaks its promise.

> **In real life**
>
> A laboratory bench can hold impressive glassware and still produce no evidence. Maven puts the
> glassware on the bench; the request, assertion, and test runner turn it into an experiment.

**REST Assured**: REST Assured is a Java DSL for testing HTTP services. In a JUnit or TestNG test it builds a request, sends it, exposes the response, and applies assertions through a fluent API.

## The smallest honest setup

Add `io.rest-assured:rest-assured` as a test-scoped dependency and use a current version from the
project's release page. Pair it with JUnit 5 or TestNG; REST Assured does not discover tests itself.

```java
import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;

@Test
void health_is_up() {
    given().baseUri("http://localhost:4000")
    .when().get("/health")
    .then().statusCode(200).body("status", equalTo("ok"));
}
```

> **Tip**
>
> Keep the base URI configurable. Hard-coding production into every test is not bravery; it is an
> incident report waiting for a timestamp.

> **Common mistake**
>
> Calling `prettyPrint()` without an assertion. Pretty JSON proves only that the printer works.

![Chemistry laboratory bench with glassware, bottles, and instruments](setup-and-first-test.jpg)
*Laboratory bench — Cjp24, Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:Laboratory_bench.jpg)*
- **Dependency** — The equipment must be present before a test can use the DSL.
- **Known request** — One controlled experiment starts with a named target and input.
- **Assertion** — The reading becomes evidence only when compared with an expected result.

**From dependency to result**

1. **Add test dependency** — Maven or Gradle places REST Assured on the test classpath.
2. **Choose base URI** — Point at a disposable local or test environment.
3. **Send request** — The HTTP method and path identify the behavior under test.
4. **Assert response** — Status and body checks decide pass or fail.

*Run it — the anatomy of a first API test (Python)*

```python
response = {"status": 200, "json": {"status": "ok"}}
checks = [
    ("status is 200", response["status"] == 200),
    ("body status is ok", response["json"]["status"] == "ok"),
]
for name, passed in checks:
    print(f"{name}: {'PASS' if passed else 'FAIL'}")
print(f"result: {sum(p for _, p in checks)}/{len(checks)} checks passed")

# status is 200: PASS
# body status is ok: PASS
# result: 2/2 checks passed
```

*Run it — the same contract (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    int status = 200;
    Map<String, String> body = Map.of("status", "ok");
    boolean statusOk = status == 200;
    boolean bodyOk = "ok".equals(body.get("status"));
    System.out.println("status is 200: " + (statusOk ? "PASS" : "FAIL"));
    System.out.println("body status is ok: " + (bodyOk ? "PASS" : "FAIL"));
    System.out.println("result: " + ((statusOk ? 1 : 0) + (bodyOk ? 1 : 0)) + "/2 checks passed");
  }
}

/* status is 200: PASS
   body status is ok: PASS
   result: 2/2 checks passed */
```

### Your first time: Your mission: make one response earn a pass

- [ ] Create a Java test project with JUnit 5 or TestNG — Confirm one empty test is discovered before adding HTTP code.
- [ ] Add REST Assured as a test dependency — Use the version shown by the official release page, not a fossil copied from a blog.
- [ ] Test a disposable health endpoint — Assert both status 200 and one stable body field.
- [ ] Break one expectation deliberately — Read the actual failure before restoring the correct value.

- **The test runner reports zero tests.**
  Check the JUnit/TestNG engine, annotation import, filename, and test task before blaming REST Assured.
- **Connection refused.**
  Verify scheme, host, port, and that the test service is listening from the same environment as the runner.
- **The body matcher cannot parse JSON.**
  Inspect Content-Type and raw body; an HTML proxy error is not JSON wearing a convincing hat.

### Where to check

- The test runner report for discovery and assertion failures.
- Request/response logging for method, URL, headers, and body.
- The service health endpoint and environment configuration.

### Worked example: a first test that catches the useful failure

The health endpoint returns `200` but its body changes from `{"status":"ok"}` to
`{"status":"degraded"}`. A status-only test smiles and waves it through. The body assertion fails
and identifies the behavioral change immediately.

**Quiz.** Why should the first test assert a stable body field as well as status 200?

- [ ] To make the test longer
- [x] Because 200 alone can accompany the wrong payload or degraded state
- [ ] Because REST Assured cannot read status codes
- [ ] To replace service monitoring

*A successful HTTP status does not prove the response body satisfies the contract.*

- **Who discovers the test?** — JUnit or TestNG; REST Assured supplies the HTTP testing DSL.
- **Why test scope?** — REST Assured is normally needed by tests, not production runtime code.
- **First two assertions** — Expected status plus one stable, meaningful response field.
- **Why break it once?** — To prove the test can fail and learn what its diagnostic output looks like.

### Challenge

Make the base URI come from an environment variable with a safe local default, then prove a bad URI and a bad body expectation produce distinguishable failures.

### Ask the community

> My first REST Assured test fails with `[exact error]` against `[method + URL]`; here is the dependency version and sanitized response log.

Include the runner, Java version, and full assertion message. Remove tokens before posting.

- [REST Assured — official getting started guide](https://github.com/rest-assured/rest-assured/wiki/GettingStarted)
- [REST Assured — official releases](https://github.com/rest-assured/rest-assured/releases)

🎬 [The TechCave — HTTP and the request-response cycle](https://www.youtube.com/watch?v=eesqK59rhGA) (9 min)

- REST Assured builds and validates HTTP interactions; JUnit or TestNG runs the test.
- A first test needs a request and assertions, not merely a printed response.
- Keep environment addresses configurable and default to a disposable target.
- Assert status and a stable body field so a polite but wrong response still fails.


## Related notes

- [[Notes/api-test-automation/rest-assured-java/given-when-then-style|Given / when / then style]]
- [[Notes/api-test-automation/rest-assured-java/validating-json-and-status|Validating JSON & status]]
- [[Notes/api-testing-fundamentals/postman-and-curl/curl-basics|curl basics]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/rest-assured-java/setup-and-first-test.mdx`_
