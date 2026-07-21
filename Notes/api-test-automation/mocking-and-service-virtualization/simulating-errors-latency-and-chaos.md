---
title: "Simulating errors, latency & chaos"
tags: ["api-test-automation", "mocking-and-service-virtualization", "track-e", "resilience"]
updated: "2026-07-17"
---

# Simulating errors, latency & chaos

*A controlled virtual service can produce 500s, timeouts, malformed bodies, disconnects, and slow responses on demand so resilience behavior becomes testable instead of theoretical.*

> The production dependency will eventually respond slowly, return `503`, cut the connection halfway
> through a body, or send valid JSON containing nonsense. Waiting for the universe to schedule that
> failure during your test window is not a strategy. A virtual service lets you order the ugly response
> like lunch—specific, repeatable, and without setting production on fire for educational purposes.

> **In real life**
>
> Wind-tunnel engineers do not wait for a convenient hurricane to visit a city model. They inject
> controlled airflow and smoke, vary one condition, and observe where pressure and turbulence appear.
> Resilience tests do the same with latency and faults: controlled stress reveals behavior that a calm
> happy-path environment keeps hidden.

**fault injection**: Fault injection is the deliberate introduction of controlled failure conditions—HTTP errors, delays, malformed responses, connection faults, or state changes—to observe whether a client meets its resilience requirements. Chaos engineering is broader: it tests system-level hypotheses under controlled experiments, often in more realistic environments. One delayed stub is useful fault injection, not automatically a chaos program.

## Build a failure matrix from requirements

| Condition | What to simulate | What to assert |
|---|---|---|
| Provider rejects request | `400` or `422` with documented error | No retry; useful validation message |
| Authentication fails | `401` or `403` | Credential handling; no secret in logs |
| Temporary outage | `503`, perhaps then `200` | Bounded retry with backoff |
| Slow dependency | Fixed or random delay beyond client timeout | Timeout, cancellation, safe fallback |
| Broken transport | Reset or malformed chunk | Classified network error; no partial success |
| Bad payload | Wrong type, missing field, invalid JSON | Parser failure contained and observable |

The status code is only the stimulus. The requirement is the response: retry or do not retry,
preserve idempotency, cap total time, expose a safe message, emit useful telemetry, and avoid a retry
storm that turns a small outage into a distributed group project.

> **Tip**
>
> Use a deterministic sequence first—`503`, `503`, then `200`—to prove exact retry behavior. Add random
> delay or fault distributions later for exploration. Randomness without a seed gives you thrilling
> failures and useless bug reports.

> **Common mistake**
>
> Enabling three automatic retries in the client, two in a proxy, and four in a job runner. One failed
> request can become dozens of calls. Test the total attempt budget across layers, not one library's
> configuration in isolation.

![A researcher injecting smoke into a scale city model inside an experimental wind tunnel](simulating-errors-latency-and-chaos.jpg)
*Experimental city wind-tunnel study — U.S. EPA/NARA, public domain. [Source](https://commons.wikimedia.org/wiki/File:EXPERIMENTAL_WIND_TUNNEL_DEVICE_BUILT_AT_COLORADO_STATE_UNIVERSITY._SMOKE_IS_PIPED_INTO_THIS_MODEL_OF_THE_CITY_OF..._-_NARA_-_543741.jpg)*
- **Controlled injection** — The researcher introduces visible smoke deliberately; a test injects one known delay or fault.
- **System model** — The city model preserves important structure while avoiding harm to the real city—service virtualization follows the same bargain.
- **Stress concentration** — Tall structures change airflow; dependencies and retry layers change how a failure propagates.
- **Observable evidence** — Smoke makes flow visible. Logs, metrics, traces, and attempt counts make resilience behavior reviewable.

**Turn a resilience claim into an experiment**

1. **Write the steady state** — A ticket saves once and a notification is accepted.
2. **State the hypothesis** — Two temporary 503s are retried; success on attempt three is returned within three seconds.
3. **Inject one condition** — Serve a deterministic 503, 503, 200 sequence.
4. **Measure the whole behavior** — Count attempts, elapsed time, idempotency key, result, logs, and metrics.
5. **Restore and repeat** — Reset state so the same experiment proves the same result.

*Simulate bounded retries*

```python
responses = [503, 503, 200]
max_attempts = 3

for attempt in range(1, max_attempts + 1):
    status = responses[attempt - 1]
    print(f"attempt={attempt} status={status}")
    if status == 200:
        print("result=success")
        break
    if status < 500 or attempt == max_attempts:
        print("result=failed")
        break
```

*Run the same retry budget in Java*

```java
public class Main {
    public static void main(String[] args) {
        int[] responses = {503, 503, 200};
        int maxAttempts = 3;

        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            int status = responses[attempt - 1];
            System.out.printf("attempt=%d status=%d%n", attempt, status);
            if (status == 200) {
                System.out.println("result=success");
                break;
            }
            if (status < 500 || attempt == maxAttempts) {
                System.out.println("result=failed");
                break;
            }
        }
    }
}
```

### Your first time: Run a controlled failure experiment

- [ ] Choose one written resilience requirement — Example: timeout after one second and no retry for 400 responses.
- [ ] Configure one deterministic fault — Use a fixed delay, explicit error, scenario sequence, or transport fault—not all at once.
- [ ] Measure outcome and side effects — Assert attempts, elapsed time, stored state, user-safe result, logs, and idempotency.
- [ ] Reset and run repeatedly — A controlled experiment should reproduce without test-order dependence.

- **The timeout test takes much longer than the configured timeout.**
  Count retries, connection timeout, read timeout, backoff, and outer test-runner timeout. The total budget is the sum across layers.
- **A delayed stub never triggers a timeout.**
  Confirm the application really calls the virtual service and that the delay exceeds the client's effective read deadline, not merely a test assertion timeout.
- **Random latency makes the test flaky.**
  Replace it with a fixed value or seeded distribution for regression. Keep unseeded exploration outside the merge-blocking suite.
- **Retries create duplicate records.**
  The operation is not safely idempotent. Add and verify an idempotency key or stop retrying non-idempotent operations automatically.

### Where to check

- Client connection/read timeout, retry count, backoff, and retryable-status configuration.
- WireMock mappings, scenarios, fault/delay settings, and request journal.
- Application logs, metrics, and traces with correlation IDs and attempt counts.
- Database or downstream state for duplicate writes and partial success.

### Worked example: a timeout that must not duplicate a ticket

1. Configure the notification stub to wait two seconds while the client deadline is 500 ms.
2. Create a ticket with one idempotency key. The requirement allows two notification attempts but
   only one ticket record.
3. Assert the operation returns `notification_pending`, total elapsed time stays within the stated
   budget, the request journal contains two notification calls with the same idempotency key, and the
   database contains one ticket.
4. Replace the delay with immediate `200` and rerun to prove recovery, then reset scenario state.

**Quiz.** A deterministic stub returns 503 twice and 200 once. What evidence best proves the retry requirement?

- [ ] The final response is 200
- [x] Exactly three journaled calls, bounded elapsed time, and the expected final state
- [ ] The test runner retried the whole test
- [ ] No errors appeared in the console

*Final success alone cannot prove who retried, how many times, how long it took, or whether side effects duplicated. Measure attempts, time, and state together.*

- **Fault injection** — Deliberately introduce a controlled failure to test a specific resilience behavior.
- **Fixed delay** — A repeatable wait added before a stub response; useful for deadline and loading-state tests.
- **Retry budget** — The maximum total attempts and time allowed across all retrying layers.
- **Idempotency** — Repeating the same logical request has no additional effect; vital before retrying writes.
- **Chaos engineering** — A broader hypothesis-driven system experiment; not a fancy synonym for one mocked 500.

### Challenge

Build a table-driven resilience test for `400`, `401`, `429`, `500`, `503`, invalid JSON, and a
timeout. For each case define retry policy, attempt count, maximum elapsed time, returned error, and
allowed side effects before writing the stub.

### Ask the community

> I injected `[fault]` at `[boundary]`. Expected `[retry/timeout/fallback]`; observed `[attempts, elapsed time, state]`. Configuration: `[client and stub settings]`.

Report the whole time and attempt budget. A screenshot of `503` alone does not explain resilience.

- [WireMock — Simulating Faults](https://wiremock.org/docs/simulating-faults/)
- [WireMock — Stateful Behaviour](https://wiremock.org/docs/stateful-behaviour/)
- [Principles of Chaos Engineering](https://principlesofchaos.org/)

🎬 [Introduction to WireMock Tool — Use Cases for API Mocking — Amod Mahajan](https://www.youtube.com/watch?v=L3Pb0ciIhgI) (6 min)

- Turn resilience requirements into deterministic experiments with an explicit stimulus and measurable outcome.
- Test errors, timeouts, transport faults, and malformed payloads—not only happy status codes.
- Measure attempts, total elapsed time, idempotency, final state, logs, metrics, and traces together.
- Use seeded or fixed conditions in regression suites; uncontrolled randomness produces flaky evidence.
- Fault injection tests one boundary; chaos engineering is a broader system-level discipline.


## Related notes

- [[Notes/api-test-automation/mocking-and-service-virtualization/wiremock-hands-on|WireMock hands-on]]
- [[Notes/api-test-automation/mocking-and-service-virtualization/stubs-mocks-and-fakes|Stubs, mocks & fakes]]
- [[Notes/api-test-automation/real-world-api-suites/chaining-and-state|Chaining & state]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/mocking-and-service-virtualization/simulating-errors-latency-and-chaos.mdx`_
