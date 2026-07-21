---
title: "CAP theorem in plain words"
tags: ["cap-theorem", "distributed-systems", "consistency", "availability", "track-d"]
updated: "2026-07-17"
---

# CAP theorem in plain words

*Understand what distributed databases can promise during a network partition—and turn consistency and availability language into concrete tests.*

> CAP is not a menu where an architect circles two letters for all time. It describes a harder moment:
> replicas cannot communicate, yet clients keep asking them to read and write. Does the system reject
> some work to preserve one agreed answer, or accept work that may temporarily disagree?

> **In real life**
>
> Two ticket booths lose their radio link. If both keep selling the last seat, customers get service but
> the records can conflict. If one booth stops selling until contact returns, the seat remains singular
> but some customers are refused. The broken radio—not normal operation—creates the forced choice.

**CAP theorem**: A network partition is a failure in which parts of a distributed system remain running but cannot reliably exchange messages. Under a partition, a system cannot guarantee both linearizable consistency—every operation appears to use one current copy—and availability—every request to a non-failing node receives a non-error response. CAP does not say databases can permanently choose only two of three independent features.

## Translate the letters carefully

- **Consistency (C):** in CAP, clients observe behavior equivalent to one up-to-date copy. This is not
  the same word as constraint consistency in ACID.
- **Availability (A):** every request reaching a non-failing node eventually receives a non-error
  response. A timeout or explicit rejection sacrifices this strict property.
- **Partition tolerance (P):** the system continues with a defined behavior despite lost or delayed
  messages between groups. Real distributed systems must plan for this condition.

CAP narrows one failure trade-off. It does not settle latency, durability, isolation, read freshness,
conflict resolution, or what the system does when the network is healthy. Many databases offer
operation-level consistency choices, so testers need exact read/write settings.

> **Tip**
>
> Replace “this database is AP” with a scenario: which nodes are separated, which operation is issued,
> which consistency level is configured, what response is allowed, and how convergence is observed.

> **Common mistake**
>
> Testing CAP by killing a process. A node crash and a communication partition are different failures.
> Use a fault that drops or delays traffic while both sides remain alive and can accept requests.

![A rural road splitting around a grassy triangular junction](cap-theorem-in-plain-words.jpg)
*Road junction and grass triangle — Michael Trolove, CC BY-SA 2.0. [Source](https://commons.wikimedia.org/wiki/File:Road_junction_and_grass_triangle_-_geograph.org.uk_-_5324642.jpg)*
- **Partition begins** — At the split, two sides can no longer coordinate reliably even though both roads remain usable.
- **Preserve one answer** — One side may reject work it cannot safely coordinate, favoring consistency over strict availability.
- **Keep serving** — Both sides may accept work, favoring availability while allowing temporary divergence.
- **Reconciliation** — When communication returns, divergent writes need a documented merge, winner, or conflict workflow.

**Test behavior during a real partition**

1. **Establish one value** — Write and read a known record through all relevant client paths before fault injection.
2. **Partition replicas** — Drop communication while keeping nodes and clients alive.
3. **Issue conflicting work** — Read and write through both sides with precise timestamps and request IDs.
4. **Observe the trade** — Record accepted, rejected, timed-out, and stale operations against the promised policy.
5. **Heal communication** — Restore the link without manually repairing data.
6. **Verify convergence** — Check final value, conflict handling, durability, and user-visible compensation.

*Run it — two partition policies (Python)*

```python
``def write(policy, can_reach_quorum, value):
    if policy == "consistent" and not can_reach_quorum:
        return "REJECTED"
    return f"ACCEPTED:{value}"

for policy in ("consistent", "available"):
    left = write(policy, False, "seat=Alice")
    right = write(policy, False, "seat=Bob")
    print(policy, left, right)

assert write("consistent", False, "x") == "REJECTED"``
```

*Run it — two partition policies (Java)*

```java
``public class Main {
    static String write(String policy, boolean quorum, String value) {
        if (policy.equals("consistent") && !quorum) return "REJECTED";
        return "ACCEPTED:" + value;
    }
    public static void main(String[] args) {
        for (String policy : new String[]{"consistent", "available"}) {
            System.out.println(policy + " " + write(policy, false, "seat=Alice")
                + " " + write(policy, false, "seat=Bob"));
        }
        if (!write("consistent", false, "x").equals("REJECTED")) throw new AssertionError();
    }
}``
```

### Your first time: Your mission: specify one partition test

- [ ] Draw nodes and client routes — Mark exactly which link fails; do not use the vague phrase network issue.
- [ ] Write the promised behavior — For each side, state whether reads and writes return, reject, time out, or may be stale.
- [ ] Create a conflicting operation — Use a business invariant such as one seat, one username, or one inventory unit.
- [ ] Define recovery evidence — Name the expected winner, merge, conflict record, alert, and maximum convergence time.

You now have an executable failure contract instead of a CAP label.

- **Both sides accept a supposedly unique value.**
  Confirm whether uniqueness is globally enforceable during the configured availability policy; test compensation or conflict exposure.
- **Healthy requests stall after the partition heals.**
  Inspect leader election, quorum membership, connection pools, and retry storms.
- **Replicas converge but a client keeps seeing the old value.**
  Check read routing, session guarantees, client cache, and consistency-level configuration.
- **The test kills nodes instead of isolating them.**
  Inject directional traffic loss or latency so both sides remain alive and the partition trade-off is observable.

### Where to check

- **Consistency-level configuration** — defaults may differ per operation or client.
- **Quorum and topology logs** — confirm which side believed it could accept work.
- **Request IDs and timestamps** — reconstruct operations without trusting wall-clock order alone.
- **Conflict records or resolution metrics** — silent last-write-wins can hide lost intent.
- **Client routing and caches** — stale reads may occur above the database.

### Worked example: two successful reservations for one seat

1. Two regions lose their link while both booking APIs remain healthy.
2. Each accepts a request for seat 12A under an availability-first policy.
3. Replication later selects one write by the configured resolver.
4. Database convergence does not repair the rejected customer's payment and confirmation email.
5. The complete test therefore checks conflict detection, refund or rebooking, notification, and audit—not only the final row.

**Quiz.** During a network partition, what trade-off does CAP force?

- [ ] Choose SQL or NoSQL
- [ ] Guarantee both low latency and low cost
- [x] Either reject some operations to preserve one current view, or remain available while allowing possible divergence
- [ ] Disable all replicas permanently

*When replicas cannot coordinate, strict consistency and strict availability cannot both be guaranteed. The exact behavior depends on operation and configuration.*

- **Partition** — Running parts of a system cannot reliably exchange messages.
- **CAP consistency** — Operations behave as though there is one current copy; it is not ACID's constraint meaning.
- **CAP availability** — Every request to a non-failing node eventually receives a non-error response.
- **Why not kill a node?** — A crash removes a participant; a partition leaves separated participants alive and exposes conflicting choices.
- **What happens after healing?** — Replicas reconcile, but the product may also need compensation for user-visible conflicting actions.

### Challenge

Design a partition test for a supposedly unique username across two regions. Include the fault direction,
two concurrent requests, allowed responses, healing, convergence deadline, and user-facing resolution.

### Ask the community

> During partition [topology], our [operation] uses [consistency setting]. Side A returns [result] and side B returns [result]. After healing we observe [state]. Does this match the documented contract?

Include the engine version, replication topology, client settings, and actual fault injection.

- [IBM — CAP theorem](https://www.ibm.com/think/topics/cap-theorem)
- [Jepsen — Consistency models](https://jepsen.io/consistency)
- [MongoDB Manual — Read isolation, consistency, and recency](https://www.mongodb.com/docs/manual/core/read-isolation-consistency-recency/)

🎬 [What is CAP Theorem? — IBM Technology](https://www.youtube.com/watch?v=eWMgsk7mpFc) (9 min)

- CAP describes behavior when communication between running parts is partitioned.
- Its consistency term is not the same as ACID consistency.
- The useful test names topology, operation, configuration, and allowed response.
- A node crash is not a substitute for a partition experiment.
- Database convergence may still require product-level compensation and audit.


## Related notes

- [[Notes/nosql-and-modern-data/distributed-data-gently/eventual-consistency-bugs|Eventual-consistency bugs]]
- [[Notes/nosql-and-modern-data/distributed-data-gently/replication-and-sharding|Replication & sharding]]
- [[Notes/relational-databases-engineer-level/transactions-and-concurrency/isolation-levels-and-anomalies|Isolation levels & anomalies]]


---
_Source: `packages/curriculum/content/notes/nosql-and-modern-data/the-nosql-landscape/cap-theorem-in-plain-words.mdx`_
