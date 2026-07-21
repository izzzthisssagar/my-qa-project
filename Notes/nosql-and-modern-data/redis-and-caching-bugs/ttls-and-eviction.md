---
title: "TTLs and eviction"
tags: ["redis", "ttl", "expiration", "eviction", "cache-testing", "track-d"]
updated: "2026-07-18"
---

# TTLs and eviction

*Separate time-driven expiration from memory-driven eviction, read Redis TTL states correctly, and test boundary, policy, and pressure behavior deterministically.*

> A session disappears at exactly 10:00 and everyone blames the TTL. A product key vanishes at 09:43
> because Redis ran out of allowed cache memory and everyone still blames the TTL. Same symptom, two
> different mechanisms, two different fixes.

> **In real life**
>
> An hourglass removes time from every key with an expiry. A crowded coat rack removes something because
> space ran out. Expiration asks, “Has this key's time ended?” Eviction asks, “Which key leaves so a new
> one can fit?”

**TTL and eviction**: A time to live (TTL) is the remaining lifetime attached to a key before automatic expiration. Eviction is a separate memory-management action that removes keys according to the configured maxmemory policy when the allowed memory limit is exceeded.

## Two removal clocks

Redis can remove a key because its expiration deadline passed. The TTL command reports remaining
seconds: a nonnegative number while the key exists with an expiry, -1 when the key exists without an
expiry, and -2 when the key does not exist. Millisecond variants provide finer precision.

Redis can also remove keys when writes push memory above maxmemory. The selected maxmemory policy
decides what can leave:

- noeviction rejects data-adding commands instead of evicting keys;
- allkeys-lru approximates least-recently-used selection across all keys;
- allkeys-lfu approximates least-frequently-used selection;
- allkeys-random chooses across all keys;
- volatile policies choose only among keys that have an expiry;
- volatile-ttl favors keys with the shortest remaining TTL.

If a volatile policy has no expiring candidates, it behaves like noeviction for new data. Policy names
describe eligibility and selection—not a guarantee that a particular business-important key survives.

> **Tip**
>
> Test the exact boundary with a fake clock: just before expiry, exactly at expiry, and just after. Sleeping
> in a test makes time nondeterministic and turns a contract check into a flake generator.

> **Common mistake**
>
> Treating eviction as data loss from the source of truth. Cache entries should usually be reconstructible.
> If evicting a key destroys the only copy, the architecture is using a cache label for authoritative data.

![Ornate hourglass with white sand falling from the upper bulb to the lower bulb](ttls-and-eviction.jpg)
*Hourglass with sand — John Morgan, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Hourglass_with_sand.jpg)*
- **Remaining TTL** — Sand in the upper bulb represents lifetime still available before expiration.
- **Exact boundary** — The narrow neck is the deadline. Tests must define whether a value is available exactly when time reaches the expiry.
- **Expired state** — Sand already below cannot be read as remaining time. After expiry Redis treats the key as absent.
- **Capacity frame** — The physical frame is finite, like maxmemory. Capacity pressure can remove a key before its TTL ends.

**Why a cache key disappears**

1. **Write key** — The application stores a value and may attach an expiration.
2. **Time and traffic move** — The TTL counts down while other writes consume cache memory.
3. **Expiry check** — At or after the deadline, the key is logically absent and can be deleted.
4. **Memory check** — A data-adding command above maxmemory triggers the selected policy.
5. **Expire, evict, or reject** — Cause depends on deadline, policy eligibility, and available memory.
6. **Observe and refill** — Expired and evicted counters explain the miss; source data reconstructs the copy.

*Run it — fake TTL and capacity pressure (Python)*

```python
``class Cache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = {}
        self.expirations = 0
        self.evictions = 0

    def put(self, key, value, expires_at=None):
        if key not in self.data and len(self.data) >= self.capacity:
            oldest = next(iter(self.data))
            del self.data[oldest]
            self.evictions += 1
        self.data[key] = (value, expires_at)

    def get(self, key, now):
        entry = self.data.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if expires_at is not None and now >= expires_at:
            del self.data[key]
            self.expirations += 1
            return None
        return value

cache = Cache(capacity=1)
cache.put("session", "active", expires_at=10)
assert cache.get("session", 9) == "active"
assert cache.get("session", 10) is None

cache.put("A", "alpha")
cache.put("B", "beta")
assert cache.get("A", 10) is None
assert cache.get("B", 10) == "beta"
print("expirations", cache.expirations, "evictions", cache.evictions)
assert cache.expirations == 1
assert cache.evictions == 1``
```

*Run it — fake TTL and capacity pressure (Java)*

```java
``import java.util.*;

public class Main {
    record Entry(String value, Integer expiresAt) {}

    static class Cache {
        final int capacity;
        final Map<String, Entry> data = new LinkedHashMap<>();
        int expirations;
        int evictions;

        Cache(int capacity) { this.capacity = capacity; }

        void put(String key, String value, Integer expiresAt) {
            if (!data.containsKey(key) && data.size() >= capacity) {
                String oldest = data.keySet().iterator().next();
                data.remove(oldest);
                evictions++;
            }
            data.put(key, new Entry(value, expiresAt));
        }

        String get(String key, int now) {
            Entry entry = data.get(key);
            if (entry == null) return null;
            if (entry.expiresAt() != null && now >= entry.expiresAt()) {
                data.remove(key);
                expirations++;
                return null;
            }
            return entry.value();
        }
    }

    public static void main(String[] args) {
        Cache cache = new Cache(1);
        cache.put("session", "active", 10);
        if (!"active".equals(cache.get("session", 9))) throw new AssertionError();
        if (cache.get("session", 10) != null) throw new AssertionError();

        cache.put("A", "alpha", null);
        cache.put("B", "beta", null);
        if (cache.get("A", 10) != null) throw new AssertionError();
        if (!"beta".equals(cache.get("B", 10))) throw new AssertionError();
        System.out.println("expirations " + cache.expirations + " evictions " + cache.evictions);
        if (cache.expirations != 1 || cache.evictions != 1) throw new AssertionError();
    }
}``
```

### Your first time: Your mission: classify every disappearance

- [ ] Read the TTL state — Record remaining seconds, no-expiry state, or missing-key state without collapsing -1 and -2.
- [ ] Cross the deadline — Check immediately before, exactly at, and after expiry with a controlled clock.
- [ ] Create pressure — Use a safe test instance with a known memory limit and policy; observe which key leaves or which write fails.
- [ ] Read the counters — Compare expired keys, evicted keys, misses, and rejected commands with the expected cause.

You can now separate the clock from the capacity policy.

- **A supposedly permanent key disappears under load.**
  Check the maxmemory policy and evicted-key counter; no TTL does not protect a key from allkeys policies.
- **Writes fail while plenty of expiring keys exist.**
  Confirm noeviction or a volatile policy with no eligible keys is not rejecting the write.
- **A TTL test fails only in CI.**
  Replace sleep and wall-clock assumptions with an injected clock and explicit boundary values.
- **Sessions survive longer after an update.**
  Verify whether the write preserved, cleared, or replaced the previous expiry.

### Where to check

- **TTL and PTTL commands** — remaining lifetime and sentinel values.
- **Redis configuration** — maxmemory and maxmemory-policy.
- **INFO stats** — expired_keys, evicted_keys, keyspace hits/misses, and rejected calls.
- **Application writes** — confirm every path attaches or preserves the intended expiry.
- **Test clock** — prove timezone and scheduling noise cannot move the boundary.

### Worked example: a session test that blamed the wrong clock

1. A session receives a 30-minute TTL and disappears after 12 minutes during a load test.
2. The team increases the TTL to two hours; the defect remains.
3. INFO shows evicted keys rising while expired keys stay flat.
4. The instance uses allkeys-lru under a small maxmemory limit, so the session was evicted.
5. Tests now cover both deadline expiry and memory pressure; architecture separates disposable cache data from session requirements.

**Quiz.** What does Redis TTL return when a key exists but has no associated expiry?

- [ ] 0
- [x] -1
- [ ] -2
- [ ] The maxmemory policy name

*TTL returns -1 for an existing key without expiry. It returns -2 when the key itself does not exist.*

- **Expiration** — Time-driven removal after a key's configured deadline.
- **Eviction** — Memory-pressure removal selected by maxmemory-policy.
- **TTL -1** — The key exists but has no associated expiry.
- **TTL -2** — The key does not exist.
- **noeviction** — Do not evict dataset keys; reject data-adding commands when memory is over the limit.

### Challenge

Build a matrix for one session key under noeviction, allkeys-lru, volatile-lru, and volatile-ttl.
Predict the outcome when its deadline passes, memory fills, the key lacks an expiry, and no volatile
candidate exists. Then verify on an isolated Redis instance.

### Ask the community

> Key [shape] vanished at [observed age]. TTL before failure was [value]. Redis policy is [policy]; expired_keys changed by [n], evicted_keys by [n], rejected calls by [n]. Which removal path best fits this evidence?

Share configuration and counters from a non-production reproduction, not credentials or live values.

- [Redis command docs — TTL](https://redis.io/docs/latest/commands/ttl/)
- [Redis command docs — EXPIRE](https://redis.io/docs/latest/commands/expire/)
- [Redis docs — Key eviction](https://redis.io/docs/latest/develop/reference/eviction/)

🎬 [Redis Expiration & Eviction Policies — Kartikeya Sharma](https://www.youtube.com/watch?v=I4TXUbQoaNg) (7 min)

- Expiration follows time; eviction follows memory pressure.
- TTL distinguishes remaining time, no expiry, and missing keys.
- Eviction policy defines eligibility and selection, not business importance.
- Use fake clocks for exact expiry boundaries.
- Counters reveal whether a miss came from expiry, eviction, or rejection.


## Related notes

- [[Notes/nosql-and-modern-data/redis-and-caching-bugs/what-caching-solves|What caching solves]]
- [[Notes/nosql-and-modern-data/redis-and-caching-bugs/stale-data-bugs-and-cache-invalidation|Stale-data bugs & cache invalidation]]
- [[Notes/nosql-and-modern-data/redis-and-caching-bugs/testing-around-a-cache|Testing around a cache]]
- [[Notes/nosql-and-modern-data/the-nosql-landscape/cap-theorem-in-plain-words|CAP theorem in plain words]]


---
_Source: `packages/curriculum/content/notes/nosql-and-modern-data/redis-and-caching-bugs/ttls-and-eviction.mdx`_
