---
title: "Stubs, mocks & fakes"
tags: ["api-test-automation", "mocking-and-service-virtualization", "track-e"]
updated: "2026-07-17"
---

# Stubs, mocks & fakes

*Test doubles replace a dependency for a specific reason: stubs return controlled answers, mocks verify conversations, and fakes provide a working but simplified implementation.*

> Your checkout test calls a payment sandbox that is slow, rate-limited, and closed for maintenance
> exactly when CI starts. Re-running until it turns green is not resilience; it is asking a stranger's
> server for permission to merge your code. A test double replaces that dependency long enough to test
> one claim under conditions you control.

> **In real life**
>
> Crash-test dummies are not counterfeit passengers. They are deliberately limited substitutes built
> to produce repeatable measurements in conditions where using a real passenger would be dangerous and
> absurd. A good test double is the same: less realistic than production on purpose, but instrumented
> for a precise experiment.

**test double**: A test double is any controlled substitute for a real collaborator used during a test. A stub returns prearranged data, a mock additionally verifies expected interactions, and a fake is a lightweight working implementation such as an in-memory repository. The labels describe behavior and purpose, not three competing libraries.

## Three doubles, three questions

| Double | What it does | Best question | Main risk |
|---|---|---|---|
| Stub | Returns a canned response for a matching request | How does our code handle this response? | The canned contract drifts |
| Mock | Records or verifies calls as well as responding | Did our code make the required interaction? | Tests become coupled to implementation |
| Fake | Implements useful behavior with shortcuts | Does a realistic workflow work without the real infrastructure? | Simplifications hide production behavior |

A stub can make `/rates/NPR` return `200` with a fixed exchange rate. A mock can also verify that the
client sent `X-Correlation-Id` exactly once. A fake repository may accept creates and queries in
memory, but skip PostgreSQL transactions, locks, and indexes. Calling every one of these things a
"mock" is common conversation; choosing them as if they were identical is common test debt.

> **Tip**
>
> Start with the smallest double that proves the claim. If the outcome is what matters, stub the
> response and assert the outcome. Verify interactions only when the interaction itself is the
> requirement, such as publishing an audit event or attaching an idempotency key.

> **Common mistake**
>
> Building a beautiful fake that reproduces the real service's every validation rule. Congratulations:
> you now maintain two production systems, except the second one lies whenever the first changes.

![A laboratory with several instrumented crash-test dummies positioned around an impact rig](stubs-mocks-and-fakes.jpg)
*Crash test dummies — NIST Digital Collections, public domain. [Source](https://commons.wikimedia.org/wiki/File:Crash_test_dummies.jpg)*
- **Controlled substitute** — The dummy stands in for a real collaborator so the dangerous or unreliable condition can be repeated safely.
- **Different doubles** — Different body sizes and instruments serve different measurements; stub, mock, and fake are selected by the question.
- **The system under test** — The rig remains real. Replace the dependency at the boundary, not every piece of the behavior you mean to test.
- **Measurement equipment** — A mock's interaction log is useful instrumentation, but measuring every internal movement makes the experiment brittle.

**Choose a double from the claim**

1. **State the claim** — Example: a 503 from the rates service shows a retryable message.
2. **Find the boundary** — The rates HTTP call is external to the behavior under test.
3. **Choose the minimum double** — A stubbed 503 is enough; no interaction verification is required.
4. **Assert the observable outcome** — Check the returned error and user-safe message, not private method calls.
5. **Keep one real contract check** — Separately verify the stub still matches the provider's documented schema.

*Classify the smallest useful test double*

```python
cases = [
    ("return a fixed 503", False, False),
    ("verify one audit POST", True, False),
    ("store and query tickets", False, True),
]

def choose(needs_verification, needs_behavior):
    if needs_behavior:
        return "fake"
    if needs_verification:
        return "mock"
    return "stub"

for claim, verify, behavior in cases:
    print(f"{choose(verify, behavior):4} | {claim}")
```

*Run the same selection rule in Java*

```java
import java.util.*;

public class Main {
    record Case(String claim, boolean verify, boolean behavior) {}

    static String choose(Case c) {
        if (c.behavior()) return "fake";
        if (c.verify()) return "mock";
        return "stub";
    }

    public static void main(String[] args) {
        var cases = List.of(
            new Case("return a fixed 503", false, false),
            new Case("verify one audit POST", true, false),
            new Case("store and query tickets", false, true)
        );
        for (Case c : cases) {
            System.out.printf("%-4s | %s%n", choose(c), c.claim());
        }
    }
}
```

### Your first time: Replace one dependency without replacing reality

- [ ] Pick one API test that depends on a remote service — Write the exact behavior the test is meant to prove.
- [ ] Identify the request boundary — Method, path, required headers, request body, and expected response contract.
- [ ] Choose stub, mock, or fake — Record why the smaller option would not prove the claim.
- [ ] Add one drift check — Validate the double's sample response against the real OpenAPI or JSON Schema contract.

- **Every refactor breaks mock-verification tests although behavior is unchanged.**
  The test is checking implementation choreography. Assert the public outcome and verify only interactions that are contractual requirements.
- **All isolated tests pass but integration fails on a renamed field.**
  The stub drifted. Validate fixtures against the provider contract and keep a smaller set of real integration or contract tests.
- **The fake database passes concurrency tests that production fails.**
  An in-memory fake does not reproduce isolation, locks, constraints, or query plans. Run those claims against the real database engine.
- **A test unexpectedly calls the real payment API.**
  Make unmatched mock requests fail closed and assert the configured base URL before the suite starts.

### Where to check

- The application's dependency-injection or base-URL configuration: prove it points at the double.
- The double's request journal: inspect method, path, headers, body, and unmatched requests.
- The provider's OpenAPI, JSON Schema, or contract tests: detect fixture drift.
- A focused integration suite: cover behavior the double deliberately cannot reproduce.

### Worked example: a retry test that stops worshipping the network

1. A ticket service calls a notification provider. The requirement says a provider `503` is retried
   twice, then the ticket still saves with notification status `pending`.
2. A stub returns `503` three times. The test asserts the ticket result and pending status.
3. Because the retry count is itself required, the stub server's journal is checked for exactly
   three calls. That narrow interaction check is justified; verifying every private method is not.
4. A separate contract test validates the canned error body against the provider schema. The suite is
   fast and deterministic without pretending the provider no longer matters.

**Quiz.** A test needs a lightweight repository that supports create, update, and query behavior in memory, but does not reproduce PostgreSQL locking. Which double fits best?

- [ ] A stub
- [ ] A mock
- [x] A fake
- [ ] A production clone

*A fake is a working but simplified implementation. A stub mainly returns prearranged answers, while a mock is chosen when verifying interactions matters. The fake remains unsuitable for claims about PostgreSQL-specific locking or isolation.*

- **Stub** — Returns controlled data for matching input so the consumer's outcome can be tested.
- **Mock** — A configurable double that also records or verifies expected interactions.
- **Fake** — A lightweight working implementation with shortcuts, such as an in-memory repository.
- **Contract drift** — The double keeps serving an old shape after the real provider changes.
- **Fail closed** — Reject unmatched requests so a test cannot silently reach the real service or accept the wrong call.

### Challenge

Take one API client test and write two versions: one that verifies every internal call, and one that
stubs the boundary and asserts only the public result. Perform a harmless refactor and record which
test fails. Keep interaction verification only where you can name the external requirement it proves.

### Ask the community

> I need to replace `[dependency]` while proving `[claim]`. I chose a `[stub/mock/fake]` because `[reason]`, but it cannot reproduce `[limitation]`. Is that boundary honest?

Include the claim and limitation. Tool names alone cannot tell reviewers whether the double is useful.

- [Martin Fowler — Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- [WireMock — Stubbing](https://wiremock.org/docs/stubbing/)
- [WireMock — Service virtualization](https://wiremock.org/docs/solutions/service-virtualization/)

🎬 [Unit Tests and Test Doubles like Mocks, Stubs & Fakes — The Theory Of Code](https://www.youtube.com/watch?v=NPp2pvhGbkM) (18 min)

- Choose a double from the claim: stub an answer, mock a required conversation, or fake useful behavior.
- Prefer outcome assertions; interaction verification is justified only when the interaction is part of the contract.
- A deterministic double improves isolation but cannot prove the real integration works.
- Validate fixtures against current schemas and retain focused integration tests to catch drift.
- Make unmatched requests fail closed so tests never leak into real services silently.


## Related notes

- [[Notes/api-test-automation/mocking-and-service-virtualization/wiremock-hands-on|WireMock hands-on]]
- [[Notes/api-test-automation/mocking-and-service-virtualization/simulating-errors-latency-and-chaos|Simulating errors, latency & chaos]]
- [[Notes/api-test-automation/real-world-api-suites/test-pyramids-for-apis|Test pyramids for APIs]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/mocking-and-service-virtualization/stubs-mocks-and-fakes.mdx`_
