---
title: "What caching solves"
tags: ["redis", "caching", "cache-aside", "performance", "track-d"]
updated: "2026-07-18"
---

# What caching solves

*Understand cache-aside behavior, distinguish fast copies from the source of truth, and test hits, misses, fills, fallbacks, latency, and correctness.*

> Your product page drops from 420 ms to 18 ms after Redis goes live. Everyone celebrates. Then a price
> changes in the database, the page keeps showing the old number, and the fast response becomes a fast
> lie. A cache solves repeated-read cost; it does not solve truth.

> **In real life**
>
> A pantry keeps ingredients close to the kitchen. It saves a trip to the shop, but it is a small,
> temporary copy of wider stock. Empty jars, wrong labels, and stale contents are pantry problems—not
> proof that the shop changed.

**cache**: A cache is a faster storage layer that keeps reusable copies of data or computed results so repeated requests avoid slower work. The authoritative source remains the system of record unless the architecture explicitly says otherwise.

## Fast path, slow path, same answer

In cache-aside, the application asks the cache first. A **hit** returns a stored value. A **miss**
causes the application to read the source, return the result, and usually fill the cache for later
requests. Redis is useful here because in-memory access is fast and its data structures are simple to
address by key.

That design creates two paths that must agree:

- cold path: cache miss, source read, cache fill, response;
- warm path: cache hit, no source read, response;
- degraded path: cache unavailable, source still returns correct data;
- double failure: cache misses or fails while the source is also unavailable;
- refresh path: authoritative data changes and cached copies must stop winning.

> **Tip**
>
> Assert both value and work. A warm-read test that checks only the response can pass even when the app
> quietly calls the database every time and the cache provides zero benefit.

> **Common mistake**
>
> Using Redis as a magic speed switch. Cache keys, fill rules, invalidation, fallback, observability, and
> data ownership are application contracts. Redis cannot infer them from your product requirements.

![Labelled and unlabelled glass jars arranged on wooden pantry shelves](what-caching-solves.jpg)
*Kitchen pantry containers — Shixart1985, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Container_storage_at_a_kitchen_pantry_with_different_types_of_food_items_in_jars_and_bottles_at_home.jpg)*
- **Nearby copy** — The labelled coconut-flour jar is quick to reach, like a cached value addressed by a known key.
- **Key and meaning** — A label connects a name to contents. Cache-key design must encode the entity, version, tenant, locale, or other dimensions that change the answer.
- **Empty cache** — An empty jar is a miss. The application must fetch from its source, then decide whether and how long to refill.
- **Source stock** — More supplies sit behind the front row. The cache is a convenient subset, not the complete system of record.

**Cache-aside read**

1. **Request arrives** — The application derives a stable cache key from the requested data and context.
2. **Read cache** — A present, valid value is a hit; an absent value is a miss.
3. **Hit: return copy** — The fast path returns without repeating the slower source lookup.
4. **Miss: read source** — The system of record provides the authoritative value or an explicit error.
5. **Fill cache** — The application stores a reusable copy with the intended expiry and serialization.
6. **Observe both paths** — Metrics distinguish hits, misses, source calls, errors, and latency.

*Run it — prove cache-aside work (Python)*

```python
``source = {"product:42": "keyboard:80"}
cache = {}
hits = misses = source_reads = 0

def read_product(key):
    global hits, misses, source_reads
    if key in cache:
        hits += 1
        print("HIT", key)
        return cache[key]
    misses += 1
    print("MISS", key)
    source_reads += 1
    value = source[key]
    cache[key] = value
    return value

first = read_product("product:42")
second = read_product("product:42")
print("values", first, second)
print("source_reads", source_reads, "hits", hits, "misses", misses)

assert first == second == "keyboard:80"
assert source_reads == 1
assert hits == 1 and misses == 1``
```

*Run it — prove cache-aside work (Java)*

```java
``import java.util.*;

public class Main {
    static final Map<String, String> source = Map.of("product:42", "keyboard:80");
    static final Map<String, String> cache = new HashMap<>();
    static int hits, misses, sourceReads;

    static String readProduct(String key) {
        if (cache.containsKey(key)) {
            hits++;
            System.out.println("HIT " + key);
            return cache.get(key);
        }
        misses++;
        System.out.println("MISS " + key);
        sourceReads++;
        String value = source.get(key);
        cache.put(key, value);
        return value;
    }

    public static void main(String[] args) {
        String first = readProduct("product:42");
        String second = readProduct("product:42");
        System.out.println("values " + first + " " + second);
        System.out.println("source_reads " + sourceReads + " hits " + hits + " misses " + misses);

        if (!first.equals(second) || !first.equals("keyboard:80")) throw new AssertionError();
        if (sourceReads != 1 || hits != 1 || misses != 1) throw new AssertionError();
    }
}``
```

### Your first time: Your mission: prove a cache earns its keep

- [ ] Name the source of truth — Write down which database, API, or computation owns the authoritative answer.
- [ ] Exercise a cold read — Clear the key, call the feature, and assert one source read plus a correct response.
- [ ] Exercise a warm read — Call again and assert the same response without another source read.
- [ ] Block the cache — Verify the documented fallback or explicit failure instead of assuming Redis is always reachable.

You now have the value, saved-work, and fallback evidence.

- **Warm responses are correct but still slow.**
  Measure source-call count and cache hit metrics; the key may drift or the fill may fail.
- **One user sees another user's data.**
  Audit key dimensions such as tenant, user, locale, permissions, and API version.
- **A cache outage takes down an otherwise healthy database.**
  Verify timeout, fallback, circuit-breaker, and connection-pool behavior under cache failure.
- **The app returns an empty object after a miss.**
  Distinguish absent cached value from a cached empty result and from a source error.

### Where to check

- **Application trace** — cache lookup, source read, fill, serialization, and returned response.
- **Redis INFO stats** — keyspace hits, misses, evictions, and expirations.
- **Database query metrics** — warm traffic should reduce the intended repeated query.
- **Key schema** — confirm tenant, locale, version, and authorization dimensions.
- **Timeout configuration** — cache fallback must not wait longer than the source it protects.

### Worked example: a product page that became fast but cross-tenant

1. The app caches product 42 under the key product:42.
2. Tenant A and Tenant B both have a product 42 with different prices.
3. Tenant A fills the shared key; Tenant B receives A's cached response.
4. Happy-path tests use one tenant and report excellent latency.
5. A two-tenant test exposes the collision; the key includes tenant and product IDs, then both paths are retested.

**Quiz.** What should a cache-aside warm-read test prove?

- [ ] Only that the response is faster than one second
- [ ] That Redis contains at least one key
- [x] That the response stays correct and the intended slower source work is avoided
- [ ] That cached data becomes the permanent source of truth

*The warm path must preserve correctness and avoid the repeated work the cache was introduced to remove. Speed alone can hide wrong data or unnecessary source calls.*

- **Cache hit** — The requested valid value is found in the cache and can use the fast path.
- **Cache miss** — The value is absent, so the application follows its source or failure path.
- **Cache fill** — A value read or computed elsewhere is stored for later reuse.
- **Source of truth** — The authoritative system whose state wins when copies disagree.
- **Cache-aside** — The application reads the cache first, loads misses from the source, then fills the cache.

### Challenge

Design a five-case test table for one cached endpoint: cold read, warm read, wrong-tenant key, cache
timeout, and source failure after a miss. Record expected value, source calls, cache calls, and metric
changes for each.

### Ask the community

> Feature [name] caches [data] under key shape [shape]. Source of truth is [system]. Cold path does [calls]; warm path does [calls]; cache outage behavior is [fallback/error]. Which correctness dimension could still be missing?

Include sanitized key structure and counts, never production values or credentials.

- [Redis docs — Client-side caching reference](https://redis.io/docs/latest/develop/reference/client-side-caching/)
- [Redis docs — Key eviction and cache metrics](https://redis.io/docs/latest/develop/reference/eviction/)
- [Redis command docs — INFO](https://redis.io/docs/latest/commands/info/)

🎬 [Redis and MongoDB: Cache-Aside Pattern — Redis](https://www.youtube.com/watch?v=AJhTduDOVCs) (6 min)

- A cache is a faster copy; identify the source of truth explicitly.
- Cache-aside creates cold, warm, degraded, and double-failure paths.
- Assert source-call counts and metrics, not response values alone.
- Cache keys are data-isolation contracts.
- A fast wrong answer is still a production defect.


## Related notes

- [[Notes/nosql-and-modern-data/redis-and-caching-bugs/ttls-and-eviction|TTLs & eviction]]
- [[Notes/nosql-and-modern-data/redis-and-caching-bugs/stale-data-bugs-and-cache-invalidation|Stale-data bugs & cache invalidation]]
- [[Notes/nosql-and-modern-data/redis-and-caching-bugs/testing-around-a-cache|Testing around a cache]]
- [[Notes/nosql-and-modern-data/mongodb-hands-on/documents-and-collections|Documents & collections]]


---
_Source: `packages/curriculum/content/notes/nosql-and-modern-data/redis-and-caching-bugs/what-caching-solves.mdx`_
