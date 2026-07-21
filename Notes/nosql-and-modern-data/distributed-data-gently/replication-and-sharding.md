---
title: "Replication and sharding"
tags: ["replication", "sharding", "replica-lag", "data-distribution", "distributed-systems", "track-d"]
updated: "2026-07-18"
---

# Replication and sharding

*Separate copy health from data distribution, then test routing, lag, failover, rebalancing, and hot-shard risk with evidence.*

> Three servers can hold three healthy copies of the same overloaded dataset, or three well-balanced
> parts with no surviving copy when one server fails. Both diagrams contain three boxes. They solve
> different problems, so their tests need different evidence.

> **In real life**
>
> Replication is photocopying the warehouse inventory into backup ledgers: each ledger describes the
> same stock. Sharding is assigning different aisles to different warehouses: aisle A stores chairs,
> aisle B stores tables, and a directory routes each request. Copies improve survival; partitions
> divide the load.

**replication and sharding**: Replication keeps copies of the same logical data on multiple members, while sharding partitions different key ranges or hashed keys across shards. A production shard is often itself a replica set, combining distribution with redundancy.

## Ask whether the failure is about copies or placement

A replica set accepts writes through a primary or leader and propagates them to secondaries. If the
primary fails, an eligible secondary may be elected. That failover is useful only when the candidate
has applied sufficiently fresh data and clients discover the new primary. Asynchronous replication
means a secondary read can trail the primary even while every process reports healthy.

A sharded collection chooses a shard key. A router uses that key and cluster metadata to target one
or more shards. A good key spreads storage and traffic; a low-cardinality, skewed, or monotonically
growing key can create one hot shard. Rebalancing moves ranges after growth or topology changes, so
test both final placement and the latency, bandwidth, and routing behavior during migration.

> **Tip**
>
> Keep two dashboards and two test oracles: replica freshness and election readiness for copy health;
> per-shard records, bytes, operations, latency, and routed-query fan-out for distribution health.

> **Common mistake**
>
> Declaring sharding healthy because every replica is caught up. Perfect copies of one hot shard do not
> prove even distribution, correct routing, or capacity on the other shards.

![A wide warehouse aisle with tall pallet racks, boxed goods, aisle signs, and shoppers](replication-and-sharding.jpg)
*Ikea Brooklyn warehouse aisles — Evan-Amos, public domain. [Source](https://commons.wikimedia.org/wiki/File:Ikea-Brooklyn-Warehouse-Aisles.jpg)*
- **Left-side partition** — These racks hold one portion of the goods, like keys assigned to one shard rather than a full copy of every item.
- **Right-side partition** — A second rack section represents different keys. Compare its stored volume and request rate with the left side.
- **Aisle 1 marker** — The red aisle sign is routing metadata: a request needs a reliable directory to find the responsible partition.
- **Shopping cart route** — The cart in the central aisle represents a client following the route to the selected shard.
- **Uneven stock** — Dense boxes on the near-right rack make distribution visible; a hot shard is a traffic imbalance, not merely a record-count difference.

**Prove distribution and copy health separately**

1. **Choose shard key** — Use production-shaped key frequencies and record the expected deterministic route.
2. **Measure placement** — Count records, bytes, and operations per shard; also verify zone or residency rules.
3. **Create skew** — Send a concentrated tenant or sequential-key workload and observe the hottest shard.
4. **Trigger movement** — Add capacity or cross a balancing threshold, then observe range migration and router metadata.
5. **Lag one replica** — Pause or slow apply work while primary writes continue.
6. **Exercise failover** — Verify election, client rerouting, acknowledged-write durability, and post-failover freshness.

*Run it — routing, imbalance, and replica lag (Python)*

```python
``customer_ids = [100, 103, 106, 109, 101, 102]
expected_routes = [(100, 1), (103, 1), (106, 1), (109, 1), (101, 2), (102, 0)]
counts = [0, 0, 0]
routes = []

for customer_id in customer_ids:
    shard = customer_id % 3
    counts[shard] += 1
    routes.append((customer_id, shard))
    print(f"ROUTE customer-{customer_id} shard-{shard}")

placement_ok = routes == expected_routes
imbalance_detected = max(counts) - min(counts) >= 2
primary_version = 7
replica_version = 6
lagging_detected = replica_version < primary_version

print(f"DISTRIBUTION shard-0={counts[0]} shard-1={counts[1]} shard-2={counts[2]}")
print(f"PLACEMENT {'PASS' if placement_ok else 'FAIL'} deterministic-modulo")
print(f"IMBALANCE {'DETECTED' if imbalance_detected else 'MISSED'} spread={max(counts) - min(counts)}")
print(f"REPLICA_FRESHNESS {'LAGGING' if lagging_detected else 'FRESH'} primary=7 replica=6")
print(f"RESULT placement={str(placement_ok).lower()} imbalance={str(imbalance_detected).lower()} lagging={str(lagging_detected).lower()}")

assert placement_ok and imbalance_detected and lagging_detected``
```

*Run it — routing, imbalance, and replica lag (Java)*

```java
``public class Main {
    public static void main(String[] args) {
        int[] customerIds = {100, 103, 106, 109, 101, 102};
        int[] expectedShards = {1, 1, 1, 1, 2, 0};
        int[] counts = new int[3];
        boolean placementOk = true;

        for (int index = 0; index < customerIds.length; index++) {
            int customerId = customerIds[index];
            int shard = customerId % 3;
            counts[shard]++;
            placementOk = placementOk && shard == expectedShards[index];
            System.out.println("ROUTE customer-" + customerId + " shard-" + shard);
        }

        int spread = Math.max(counts[0], Math.max(counts[1], counts[2]))
            - Math.min(counts[0], Math.min(counts[1], counts[2]));
        boolean imbalanceDetected = spread >= 2;
        int primaryVersion = 7;
        int replicaVersion = 6;
        boolean laggingDetected = replicaVersion < primaryVersion;

        System.out.println("DISTRIBUTION shard-0=" + counts[0] + " shard-1=" + counts[1] + " shard-2=" + counts[2]);
        System.out.println("PLACEMENT " + (placementOk ? "PASS" : "FAIL") + " deterministic-modulo");
        System.out.println("IMBALANCE " + (imbalanceDetected ? "DETECTED" : "MISSED") + " spread=" + spread);
        System.out.println("REPLICA_FRESHNESS " + (laggingDetected ? "LAGGING" : "FRESH") + " primary=7 replica=6");
        System.out.println("RESULT placement=" + placementOk + " imbalance=" + imbalanceDetected + " lagging=" + laggingDetected);

        if (!(placementOk && imbalanceDetected && laggingDetected)) throw new AssertionError();
    }
}``
```

### Your first time: Your mission: separate two health checks

- [ ] Map copies and partitions — Draw each shard and every replica inside it; label primary, secondary, router, and config metadata.
- [ ] Record expected routes — Use known shard keys and state the exact target shard or expected fan-out before running queries.
- [ ] Measure freshness — Write a version marker and compare applied versions or optimes, not process liveness alone.
- [ ] Disturb one dimension — Create skew, migration, lag, or failover and prove the other dimension is still observed independently.

You now have separate evidence for “the right keys are here” and “the copies are current.”

- **One shard owns most writes while record counts look even.**
  Measure operations and latency per shard; inspect shard-key frequency, monotonic growth, and targeted versus scatter-gather queries.
- **A secondary is healthy but returns an old order state.**
  Compare its applied version or optime with the primary and verify read preference, read concern, and lag thresholds.
- **Queries fail during or after rebalancing.**
  Inspect range-migration state, router metadata refresh, stale-config retries, and orphan cleanup.
- **Failover succeeds but acknowledged writes disappear.**
  Check write concern, majority commit point, election candidate freshness, rollback logs, and retry semantics.

### Where to check

- **Router plans and profiler** — targeted shard list, scatter-gather fan-out, stale metadata, and retry.
- **Per-shard telemetry** — documents, bytes, reads, writes, CPU, disk, queue depth, and latency.
- **Balancer and migration state** — active ranges, thresholds, bandwidth, failures, and cleanup.
- **Replica status** — primary identity, applied optime or version, lag, majority commit point, and elections.
- **Client configuration** — seed list, topology discovery, read preference, read concern, and write concern.

### Worked example: a balanced customer count that hid a hot tenant

1. Customer records are evenly divided across three shards by tenant ID.
2. One enterprise tenant generates 70 percent of writes, so its shard saturates while counts remain balanced.
3. Its secondary falls behind, making reporting reads stale and weakening its failover readiness.
4. Adding a shard starts rebalancing, but the tenant's indivisible key value cannot be spread by record movement alone.
5. The useful test checks request frequency, key cardinality, migration behavior, replica lag, and a revised key—not just totals.

**Quiz.** Which evidence distinguishes distribution health from replica health?

- [ ] All database processes answer a ping
- [x] Per-shard workload and placement are balanced, and each replica's applied version is within its freshness objective
- [ ] Every shard has the same number of replica members
- [ ] The router can connect to one primary

*Distribution health concerns where keys and traffic land; replica health concerns whether copies are current and ready. One does not prove the other.*

- **Replication** — Maintains copies of the same logical data for availability, durability, or read capacity.
- **Sharding** — Partitions different keys across shards to divide storage and workload.
- **Replica lag** — The gap between a source operation and its application on a replica.
- **Hot shard** — A shard receiving disproportionate traffic or resource pressure, even if record counts look balanced.
- **Rebalancing** — Moving data ranges to restore intended distribution after growth, skew, or topology change.

### Challenge

Replace the playground's modulo route with your real shard-key rule. Feed it production-shaped synthetic
frequencies, add one shard, and assert placement, fan-out, workload distribution, migration completion,
replica freshness, and successful client rediscovery after failover.

### Ask the community

> Our collection uses shard key [fields] and [range/hash/zone] routing. Workload [shape] makes shard [id] hot while replica [id] lags by [measure]. Which placement, migration, or failover check should we add?

Share sanitized key distributions, topology, consistency settings, and per-shard measurements—not customer values.

- [MongoDB Manual — Sharding](https://www.mongodb.com/docs/manual/sharding/)
- [MongoDB Manual — Choose a shard key](https://www.mongodb.com/docs/manual/core/sharding-choose-a-shard-key/)
- [MongoDB Manual — Replication](https://www.mongodb.com/docs/manual/replication/)
- [MongoDB Manual — Troubleshoot replication lag](https://www.mongodb.com/docs/manual/troubleshooting/replication-lag/)

🎬 [What is Database Sharding? — Anton Putra](https://www.youtube.com/watch?v=XP98YCr-iXQ) (9 min)

- Replication copies the same data; sharding partitions different keys.
- A router and shard key determine placement and query fan-out.
- Record balance does not prove workload balance, and replica liveness does not prove freshness.
- Rebalancing and failover are transitions that need correctness and latency checks.
- CAP partition behavior and eventual-consistency read behavior become concrete in lag and failover tests.


## Related notes

- [[Notes/nosql-and-modern-data/the-nosql-landscape/cap-theorem-in-plain-words|CAP theorem in plain words]]
- [[Notes/nosql-and-modern-data/distributed-data-gently/eventual-consistency-bugs|Eventual-consistency bugs]]


---
_Source: `packages/curriculum/content/notes/nosql-and-modern-data/distributed-data-gently/replication-and-sharding.mdx`_
