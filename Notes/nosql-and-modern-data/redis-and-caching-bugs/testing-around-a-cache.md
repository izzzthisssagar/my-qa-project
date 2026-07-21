---
title: "Testing around a cache"
tags: ["redis", "cache-testing", "resilience", "observability", "test-design", "track-d"]
updated: "2026-07-18"
---

# Testing around a cache

*Build a cache test matrix that proves cold, warm, degraded, corrupt-value, double-failure, observability, isolation, and recovery behavior.*

> The warm-path test is green. Redis is running, the key exists, and the response is fast. Production
> Redis then times out, the fallback floods the database, malformed values crash deserialization, and
> your green test explains none of it. A cache is a branch in the system, so test the branches.

> **In real life**
>
> A road closure does not test whether the main road was pleasant yesterday. It tests whether drivers
> can detect the barrier, take a safe alternate route, and still reach the right destination. Cache
> failure testing blocks the fast path on purpose.

**cache-path testing**: Cache-path testing verifies the result, work, state transitions, failure behavior, and observability of cold, warm, expired, evicted, stale, unavailable, malformed, and recovering cache scenarios.

## Test the matrix, not the logo

“Redis is up” is infrastructure evidence, not feature evidence. A useful scenario matrix records:

- starting cache state: empty, warm, expired, evicted, stale, or malformed;
- cache behavior: available, slow, timing out, disconnected, or recovering;
- source behavior: available, slow, changed, or unavailable;
- returned result or explicit error;
- source and cache call counts;
- cache repair, deletion, or fill after the response;
- metrics, logs, traces, and alerts produced.

Unit tests should drive cache and source adapters deterministically. Integration tests should prove
serialization, TTL, policy, and client behavior against an isolated Redis instance. End-to-end tests
should cover a small set of product-critical journeys where stale or unavailable data changes the
business outcome.

> **Tip**
>
> Use dependency-controlled fakes for races and failures, then a real Redis container for protocol
> contracts. Mock-only tests miss serialization and configuration; live-only tests make rare timing
> states expensive and flaky.

> **Common mistake**
>
> Flushing the shared developer or CI cache before every test. That hides warm-state bugs, creates
> cross-test races, and can destroy another test's evidence. Give each test unique key prefixes and
> delete only what it owns.

![Rural road blocked by striped barriers and a sign reading ROAD CLOSED TO THRU TRAFFIC](testing-around-a-cache.jpg)
*Road closed, Champaign County — Daniel Schwen, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Road_closed.jpg)*
- **Normal fast path** — The road leads straight to the destination when the cache is healthy and the value is valid.
- **Detected failure** — The sign makes failure explicit. Cache clients need bounded timeouts and observable errors.
- **Barrier** — Block the cache deliberately in tests; do not wait for an accidental outage to discover fallback behavior.
- **Alternate route** — Fallback must preserve correctness without silently overloading or bypassing the authoritative source.

**A cache resilience test**

1. **Seed scenario** — Choose cold, warm, malformed, stale, or unavailable cache state.
2. **Control source** — Set the authoritative value and whether the source succeeds, slows, or fails.
3. **Call feature** — Exercise the real application branch rather than manipulating Redis alone.
4. **Assert result** — Check exact value or explicit error; never accept fabricated fallback data.
5. **Assert work and repair** — Count cache/source calls and inspect fill, delete, or replacement state.
6. **Assert signals** — Verify hit, miss, fallback, corruption, timeout, and failure metrics or traces.

*Run it — five cache-path scenarios (Python)*

```python
``class Source:
    def __init__(self):
        self.value = 80
        self.available = True
        self.calls = 0

    def read(self):
        self.calls += 1
        if not self.available:
            raise RuntimeError("source unavailable")
        return self.value

class Cache:
    def __init__(self):
        self.data = {}
        self.available = True
        self.calls = 0

    def get(self, key):
        self.calls += 1
        if not self.available:
            raise RuntimeError("cache unavailable")
        return self.data.get(key)

source = Source()
cache = Cache()
fallbacks = 0

def read_price():
    global fallbacks
    try:
        cached = cache.get("product:42")
        if isinstance(cached, int):
            return cached
        if cached is not None:
            fallbacks += 1
    except RuntimeError:
        fallbacks += 1
    value = source.read()
    if cache.available:
        cache.data["product:42"] = value
    return value

assert read_price() == 80
assert source.calls == 1
assert read_price() == 80
assert source.calls == 1

cache.available = False
assert read_price() == 80
assert source.calls == 2 and fallbacks == 1

cache.available = True
cache.data["product:42"] = "broken"
assert read_price() == 80
assert cache.data["product:42"] == 80
assert source.calls == 3 and fallbacks == 2

cache.data.clear()
source.available = False
try:
    read_price()
    raise AssertionError("expected source failure")
except RuntimeError as error:
    assert str(error) == "source unavailable"

print("PASS cold warm cache_down malformed source_down")
print("source_calls", source.calls, "cache_calls", cache.calls, "fallbacks", fallbacks)``
```

*Run it — five cache-path scenarios (Java)*

```java
``import java.util.*;

public class Main {
    static class Source {
        int value = 80;
        boolean available = true;
        int calls;
        int read() {
            calls++;
            if (!available) throw new IllegalStateException("source unavailable");
            return value;
        }
    }

    static class Cache {
        final Map<String, Object> data = new HashMap<>();
        boolean available = true;
        int calls;
        Object get(String key) {
            calls++;
            if (!available) throw new IllegalStateException("cache unavailable");
            return data.get(key);
        }
    }

    static final Source source = new Source();
    static final Cache cache = new Cache();
    static int fallbacks;

    static int readPrice() {
        try {
            Object cached = cache.get("product:42");
            if (cached instanceof Integer value) return value;
            if (cached != null) fallbacks++;
        } catch (IllegalStateException error) {
            fallbacks++;
        }
        int value = source.read();
        if (cache.available) cache.data.put("product:42", value);
        return value;
    }

    public static void main(String[] args) {
        if (readPrice() != 80 || source.calls != 1) throw new AssertionError();
        if (readPrice() != 80 || source.calls != 1) throw new AssertionError();

        cache.available = false;
        if (readPrice() != 80 || source.calls != 2 || fallbacks != 1) throw new AssertionError();

        cache.available = true;
        cache.data.put("product:42", "broken");
        if (readPrice() != 80 || !cache.data.get("product:42").equals(80)) throw new AssertionError();
        if (source.calls != 3 || fallbacks != 2) throw new AssertionError();

        cache.data.clear();
        source.available = false;
        try {
            readPrice();
            throw new AssertionError("expected source failure");
        } catch (IllegalStateException error) {
            if (!error.getMessage().equals("source unavailable")) throw error;
        }

        System.out.println("PASS cold warm cache_down malformed source_down");
        System.out.println("source_calls " + source.calls + " cache_calls " + cache.calls + " fallbacks " + fallbacks);
    }
}``
```

### Your first time: Your mission: build one cache scenario table

- [ ] Choose one business read — Use price, permission, inventory, or another answer where wrong data has a visible consequence.
- [ ] List cache states — Include empty, warm, expired, stale, malformed, unavailable, and recovered.
- [ ] Control the source — Set a known value, then add changed, slow, and unavailable cases.
- [ ] Assert signals and cleanup — Check calls and metrics; use unique keys and delete only this test's data.

You now have a test model for behavior, work, and evidence.

- **Cache-down fallback passes locally but overloads production.**
  Load-test miss and outage paths; assert source protection, backoff, concurrency limits, and circuit-breaker behavior.
- **Tests pass alone and fail together.**
  Use unique key prefixes, isolated instances, controlled clocks, and ownership-scoped cleanup.
- **Malformed cache data causes a 500.**
  Validate deserialization, delete or repair bad values, and fall back only to authoritative data.
- **Metrics say hit while the database was called.**
  Define hit at the application decision point and correlate cache, source, and trace spans.

### Where to check

- **Application adapter tests** — deterministic branch, race, retry, and repair behavior.
- **Isolated Redis integration** — commands, serialization, expiry, policy, and connection behavior.
- **Traces** — cache span, source span, fallback reason, and total latency.
- **INFO stats and app metrics** — hits, misses, expirations, evictions, timeouts, corruption, and fallbacks.
- **Cleanup logs** — prove a test deletes only its unique key namespace.

### Worked example: a checkout that failed when the fast road closed

1. Checkout reads tax rules from cache and normally completes in 30 ms.
2. During a Redis timeout, each request waits five seconds, then queries the database.
3. Retries multiply database traffic and exhaust its connection pool.
4. A functional test with Redis either fully healthy or fully stopped misses the slow-timeout state.
5. Fault injection adds latency, concurrent load, bounded timeouts, single fallback, and an alert on fallback rate.

**Quiz.** Which test best proves safe cache degradation?

- [ ] Ping Redis and assert PONG
- [ ] Delete every key in the shared test environment
- [x] Inject a bounded cache failure, assert authoritative fallback and call limits, then verify fallback signals
- [ ] Assert the warm response is faster than the cold response

*Safe degradation requires correct fallback, protected source work, bounded delay, and observable evidence. Infrastructure reachability or speed alone proves less.*

- **Cold-path test** — Starts without a reusable cached value and proves source read plus fill or explicit failure.
- **Warm-path test** — Starts with a valid cached value and proves correct response without unintended source work.
- **Fault injection** — Deliberately introduces timeout, disconnect, corruption, latency, or failure to exercise rare branches.
- **Cache stampede** — Many misses trigger concurrent source work for the same value.
- **Test isolation** — Each test owns unique keys, clock, state, and cleanup so parallel runs cannot interfere.

### Challenge

Run the five-case playground model against your application's cache adapter, then add expired, evicted,
stale, slow-cache, and concurrent-miss cases. For every row, record exact response, cache calls, source
calls, post-state, latency budget, and metric changes.

### Ask the community

> Cached feature [name] has scenarios [list]. For [scenario], expected result is [value/error], cache calls [n], source calls [n], repair [state], and signals [metrics]. Which failure state or isolation risk is missing?

Share synthetic values, test-only key prefixes, and sanitized traces.

- [Redis docs — Eviction policies and cache metrics](https://redis.io/docs/latest/develop/reference/eviction/)
- [Redis command docs — INFO](https://redis.io/docs/latest/commands/info/)
- [Redis docs — Transactions and pipelines with redis-py](https://redis.io/docs/latest/develop/clients/redis-py/transpipe/)

🎬 [What is Caching? Cache Eviction and Invalidation Explained — Tech With Aman](https://www.youtube.com/watch?v=6IHE4d-l7Y0) (19 min)

- Model cache tests by state, source behavior, result, work, repair, and signals.
- Use controlled fakes for rare branches and real Redis for protocol contracts.
- A degraded path must preserve truth and protect the source.
- Malformed cached data needs validation and repair.
- Unique keys and scoped cleanup prevent cross-test collisions.


## Related notes

- [[Notes/nosql-and-modern-data/redis-and-caching-bugs/what-caching-solves|What caching solves]]
- [[Notes/nosql-and-modern-data/redis-and-caching-bugs/ttls-and-eviction|TTLs & eviction]]
- [[Notes/nosql-and-modern-data/redis-and-caching-bugs/stale-data-bugs-and-cache-invalidation|Stale-data bugs & cache invalidation]]
- [[Notes/nosql-and-modern-data/the-nosql-landscape/where-each-shines|Where each shines]]


---
_Source: `packages/curriculum/content/notes/nosql-and-modern-data/redis-and-caching-bugs/testing-around-a-cache.mdx`_
