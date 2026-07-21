---
title: "Stale-data bugs and cache invalidation"
tags: ["redis", "cache-invalidation", "stale-data", "race-conditions", "track-d"]
updated: "2026-07-18"
---

# Stale-data bugs and cache invalidation

*Reproduce stale reads, test invalidation ordering and failure paths, and verify that cached copies stop winning after authoritative data changes.*

> The database says the sale price is 80. The API says 100. Redis says 100 in under a millisecond, so
> the wrong answer arrives before the correct system has time to object. Staleness is not “Redis being
> slow.” It is a copy outliving the event that made it wrong.

> **In real life**
>
> Mouldy bread can remain exactly where fresh bread used to be. Location and appearance are not proof of
> freshness. A cached value can have the expected key and valid serialization while its meaning has
> already expired.

**cache invalidation**: Cache invalidation is the act of removing or marking a cached copy unusable when the authoritative value changes, so later reads cannot serve data that is no longer valid.

## Every write needs a freshness story

A TTL limits how long staleness can survive, but it does not make a cached value fresh between the
source update and the deadline. Systems use several patterns:

- invalidate after changing the source, so the next read refills;
- update the source and cached copy through one application path;
- use versioned keys so a new version cannot collide with an old copy;
- accept bounded staleness for data whose product contract allows it;
- send invalidation messages to clients that keep local copies.

Each pattern has a failure window. Invalidate-before-write can remove the old copy, then allow another
reader to refill it before the source update completes. Write-then-invalidate can leave stale data if
invalidation fails. Two concurrent refills can complete out of order. Delete, rename, bulk update, and
rollback paths can skip the invalidation used by ordinary edits.

Redis client-side caching can notify tracking clients when keys change, expire, or are evicted. Clients
must remove their local copies. If the invalidation connection is lost, the safe action is to clear the
local cache; otherwise the client cannot know which messages it missed.

> **Tip**
>
> Give stale-data tests a value history: v1 in source, v1 cached, source moves to v2, then prove exactly
> which read returns v1 or v2. “Response is 200” cannot expose freshness.

> **Common mistake**
>
> Testing invalidation by deleting a key manually. That proves Redis can delete. It does not prove every
> real application write, delete, rename, retry, or rollback emits the right invalidation at the right time.

![Close-up of white mould colonies spreading across brown bread](stale-data-bugs-and-cache-invalidation.jpg)
*Moldy bread — Thomas Bresson, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Moldy_bread_(35065875813).jpg)*
- **Expected location** — The bread remains where a valid item belongs, just as a stale value remains under the expected key.
- **Stale copy** — The copy still exists but no longer meets the freshness contract.
- **Spread** — One missed invalidation can affect many requests, replicas, or client-local caches before detection.
- **Replace, do not relabel** — A new timestamp on old data is not a refresh. Remove or replace the copy from the authoritative source.

**A missed invalidation becomes a stale read**

1. **Cache fills v1** — A read copies the current authoritative value into the cache.
2. **Source changes to v2** — A write succeeds in the database or upstream service.
3. **Invalidation is lost** — A timeout, retry bug, skipped code path, or disconnected tracker leaves v1 cached.
4. **Reader gets v1** — The cache hit is fast and well-formed but wrong for the current source state.
5. **Cache is cleared** — Delete, version change, or tracking recovery prevents v1 from winning again.
6. **Next read refills v2** — The authoritative value returns and becomes the new reusable copy.

*Run it — reproduce then fix a stale read (Python)*

```python
``source = {"product:42": 100}
cache = {}
stale_reads = 0

def read_price(key):
    if key not in cache:
        cache[key] = source[key]
    return cache[key]

first = read_price("product:42")
source["product:42"] = 80
second = read_price("product:42")
if second != source["product:42"]:
    stale_reads += 1
    print("STALE cached", second, "source", source["product:42"])

cache.pop("product:42", None)
third = read_price("product:42")
print("REFRESHED", third)

assert first == 100
assert second == 100
assert third == 80
assert stale_reads == 1``
```

*Run it — reproduce then fix a stale read (Java)*

```java
``import java.util.*;

public class Main {
    static final Map<String, Integer> source = new HashMap<>();
    static final Map<String, Integer> cache = new HashMap<>();
    static int staleReads;

    static int readPrice(String key) {
        return cache.computeIfAbsent(key, source::get);
    }

    public static void main(String[] args) {
        source.put("product:42", 100);
        int first = readPrice("product:42");
        source.put("product:42", 80);
        int second = readPrice("product:42");
        if (second != source.get("product:42")) {
            staleReads++;
            System.out.println("STALE cached " + second + " source " + source.get("product:42"));
        }

        cache.remove("product:42");
        int third = readPrice("product:42");
        System.out.println("REFRESHED " + third);

        if (first != 100 || second != 100 || third != 80) throw new AssertionError();
        if (staleReads != 1) throw new AssertionError();
    }
}``
```

### Your first time: Your mission: make freshness observable

- [ ] Seed version one — Read the source and prove the cache contains a known old value.
- [ ] Change through the real write path — Use the same API, job, or event path production uses—not a manual database edit unless that path is itself supported.
- [ ] Read during the risk window — Coordinate the write, invalidation, and refill so ordering is controlled and reproducible.
- [ ] Break invalidation — Inject a timeout, disconnect, duplicate event, or reordered completion and assert the documented freshness bound.

You can now describe staleness with versions and events, not feelings.

- **Only bulk edits stay stale.**
  Trace whether bulk, import, admin, and migration paths publish the same invalidation as ordinary writes.
- **Stale data returns after a reconnect.**
  Flush client-local cache when the tracking connection is lost; missed invalidations cannot be reconstructed safely.
- **Older data overwrites a newer refill.**
  Control concurrent loaders with versions, compare-and-set logic, locks, or a single-flight mechanism.
- **Deletes reappear as cached objects.**
  Test tombstones, negative caching, delete invalidation, and readers racing with deletion.

### Where to check

- **Write trace** — source commit, event publication, cache delete/update, and acknowledgements.
- **Cache value version** — compare timestamp, entity version, ETag, or revision with the source.
- **Retry and dead-letter paths** — an invalidation retry must be idempotent and observable.
- **Client tracking connection** — disconnection should clear local cached copies.
- **Key fan-out** — one source change may invalidate detail, list, count, search, and permission keys.

### Worked example: a sale price that depended on which page you opened

1. An admin changes a product from 100 to 80 and invalidates the product-detail key.
2. The category-list key still contains the old embedded price.
3. Detail tests pass because they check the one invalidated key.
4. A journey test opens the category, detail, cart, and checkout and finds three prices.
5. The team maps every derived key, versions the product payload, and tests invalidation fan-out plus failure retries.

**Quiz.** What should a client using Redis tracking do after it loses the invalidation connection?

- [ ] Keep serving local values until their process restarts
- [ ] Assume no keys changed during the disconnect
- [x] Flush the local cache because invalidation messages may have been missed
- [ ] Add one hour to every local TTL

*Without the invalidation channel, the client cannot know which tracked keys changed. Clearing local copies prevents unknowingly serving stale data.*

- **Invalidation** — Remove or mark a cached copy unusable after authoritative state changes.
- **Stale read** — A read returns an older value that no longer satisfies the freshness contract.
- **Bounded staleness** — The product explicitly allows data to lag the source by a defined maximum interval.
- **Versioned key** — A cache key includes a version so new state cannot collide with an older copy.
- **Invalidation fan-out** — One source change affects every cached representation derived from that data.

### Challenge

List every cache representation derived from one product update: detail, category, search, price,
availability, cart, permissions, and client-local copies. Inject failure after the source commits but
before each invalidation completes. State the accepted freshness bound and recovery evidence.

### Ask the community

> Source entity [name] moved from version [v1] to [v2]. Cached representations are [key groups]. Write committed at [step]; invalidation [failed/reordered/disconnected] at [step]; observed stale window was [duration]. Which race or missing fan-out should I test next?

Use synthetic versions and sanitized key shapes, never customer data.

- [Redis docs — Client-side caching and invalidation](https://redis.io/docs/latest/develop/reference/client-side-caching/)
- [Redis command docs — CLIENT TRACKING](https://redis.io/docs/latest/commands/client-tracking/)
- [Redis docs — Keyspace notifications](https://redis.io/docs/latest/develop/pubsub/keyspace-notifications/)

🎬 [Caching Pitfalls Every Developer Should Know — ByteByteGo](https://www.youtube.com/watch?v=wh98s0XhMmQ) (7 min)

- A valid key and valid payload can still contain stale data.
- Every supported write path needs an invalidation or refresh contract.
- TTL bounds staleness; it does not prevent it.
- Concurrent refill and message ordering create testable race windows.
- Lost invalidation tracking requires clearing client-local copies.


## Related notes

- [[Notes/nosql-and-modern-data/redis-and-caching-bugs/what-caching-solves|What caching solves]]
- [[Notes/nosql-and-modern-data/redis-and-caching-bugs/ttls-and-eviction|TTLs & eviction]]
- [[Notes/nosql-and-modern-data/redis-and-caching-bugs/testing-around-a-cache|Testing around a cache]]
- [[Notes/nosql-and-modern-data/mongodb-hands-on/crud-and-query-operators|CRUD & query operators]]


---
_Source: `packages/curriculum/content/notes/nosql-and-modern-data/redis-and-caching-bugs/stale-data-bugs-and-cache-invalidation.mdx`_
