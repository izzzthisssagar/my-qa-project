---
title: "Requests & pytest"
tags: ["api-test-automation", "python-api-testing", "track-d"]
updated: "2026-07-17"
---

# Requests & pytest

*Requests performs the HTTP exchange; pytest discovers cases, injects fixtures, and reports assertions. Together they make small API tests readable without pretending a response object is self-validating.*

> `requests.get()` is an HTTP call, not a test. The test begins when pytest compares the response with a contract and is willing to ruin your green checkmark over it.

> **In real life**
>
> A lab technician operates instruments and records evidence; the laboratory procedure decides whether the evidence passes. Requests is the instrument, pytest is the procedure and report.

**Requests + pytest test**: An API test with Requests and pytest calls an HTTP method through Requests, inspects the returned Response, and uses plain Python assertions inside pytest-discovered test functions to decide pass or fail.

## One request, explicit timeout, useful assertions

```python
import requests

def test_health(base_url):
    response = requests.get(f"{base_url}/health", timeout=5)
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    assert response.json()["status"] == "ok"
```

Requests does not time out unless you set a timeout. In a test suite, an unlimited wait is not
patience; it is a runner occupying a machine while teaching nobody what failed.

> **Tip**
>
> Use `response.raise_for_status()` in client code when any error status should raise. In tests, explicit status assertions often produce expectations that better match the endpoint's intended behavior.

> **Common mistake**
>
> Calling `response.json()` before checking that the response is actually JSON. An HTML gateway error then becomes a distracting decoder exception.

![Biochemistry laboratory bench with equipment and containers](requests-and-pytest.jpg)
*Lab bench — Magnus Manske, Wikimedia Commons, CC BY 1.0. [Source](https://commons.wikimedia.org/wiki/File:Lab_bench.jpg)*
- **Requests** — The instrument sends HTTP and returns a Response.
- **Assertion** — The procedure compares evidence with the contract.
- **pytest report** — Discovery and failure output make the result actionable.

**A Python API test's real lifecycle**

1. **pytest discovers test** — A test_ function is collected.
2. **Requests sends HTTP** — Method, URL, headers, body, and timeout define the exchange.
3. **Response is classified** — Status and content type are checked before parsing.
4. **Assertions report** — Business fields decide the final result.

*Run it — response evidence under pytest-style assertions (Python)*

```python
response = {"status_code": 200, "content_type": "application/json", "json": {"status": "ok"}}
assert response["status_code"] == 200
assert response["content_type"].startswith("application/json")
assert response["json"]["status"] == "ok"
print("3 assertions passed")

# 3 assertions passed
```

*Run it — the same evidence, language changed (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    int status = 200; String contentType = "application/json";
    Map<String,String> json = Map.of("status", "ok");
    if (status != 200) throw new AssertionError("status");
    if (!contentType.startsWith("application/json")) throw new AssertionError("content type");
    if (!"ok".equals(json.get("status"))) throw new AssertionError("body status");
    System.out.println("3 assertions passed");
  }
}

/* 3 assertions passed */
```

### Your first time: Your mission: build one pytest API check

- [ ] Install Requests and pytest in an isolated environment — Record dependencies in the project's chosen lock or requirements file.
- [ ] Put one test_health function in a test_*.py file — First confirm pytest collects it.
- [ ] Send a GET with an explicit timeout — Use a disposable local or test environment.
- [ ] Assert status, content type, and one body field — Break each expectation once and read pytest's introspected failure.

- **pytest collects zero tests.**
  Check test file/function naming and run pytest --collect-only before debugging HTTP.
- **The run hangs on a dead service.**
  Add an explicit connect/read timeout; Requests has no default timeout.
- **response.json() raises a decode error.**
  Inspect status, Content-Type, and a sanitized body preview for HTML or empty content.

### Where to check

- `pytest --collect-only` for discovery.
- `response.status_code`, headers, elapsed time, and sanitized body.
- The prepared request URL and headers when parameters look wrong.
- Service logs only after the client-side evidence is preserved.

### Worked example: the gateway page disguised as an API failure

The endpoint returns `502` with `text/html`. A test that immediately calls `.json()` fails with a decoder traceback. Checking status and content type first reports the real condition: an upstream gateway error, not malformed application JSON.

**Quiz.** What happens when no timeout is supplied to Requests?

- [ ] It defaults to five seconds
- [x] It does not time out by default
- [ ] pytest supplies one
- [ ] Only POST requests wait

*The official Requests advanced guide states that requests do not time out unless a timeout is set explicitly.*

- **Requests' job** — Build and send HTTP requests and return Response objects.
- **pytest's job** — Discover tests, provide fixtures/parametrization, evaluate assertions, and report failures.
- **Why explicit timeout?** — Requests has no default timeout; an unavailable service can otherwise stall a run.
- **Safe parse order** — Check expected status and JSON content type, then parse and assert fields.

### Challenge

Add a tuple timeout for connect/read behavior and make a failure message include method and sanitized URL without leaking query secrets.

### Ask the community

> My Requests + pytest case fails at `[status/content type/JSON assertion]`; here is the sanitized response and exact pytest traceback.

Include the timeout and environment, but remove auth headers and cookies.

- [Requests — official quickstart](https://requests.readthedocs.io/en/stable/user/quickstart/)
- [pytest — official getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [Requests — official timeout guidance](https://requests.readthedocs.io/en/stable/user/advanced/#timeouts)

🎬 [Joshua Morony — how to test like an API developer](https://www.youtube.com/watch?v=vcJhW1fL7a4) (5 min)

- Requests performs HTTP; pytest supplies collection, fixtures, assertions, and reporting.
- Set timeouts explicitly because Requests has no default timeout.
- Check status and content type before parsing JSON.
- A useful first test verifies protocol evidence and one stable business field.


## Related notes

- [[Notes/api-test-automation/python-api-testing/fixtures-for-apis|Fixtures for APIs]]
- [[Notes/api-test-automation/python-api-testing/parameterized-endpoint-tests|Parameterized endpoint tests]]
- [[Notes/api-test-automation/rest-assured-java/setup-and-first-test|Setup & first test]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/python-api-testing/requests-and-pytest.mdx`_
