---
title: "Isolation levels and anomalies"
tags: ["relational-databases-engineer-level", "transactions-and-concurrency", "track-e"]
updated: "2026-07-17"
---

# Isolation levels and anomalies

*Isolation levels permit different concurrent histories. Learn dirty reads, nonrepeatable reads, phantoms, and serialization anomalies with PostgreSQL's exact behavior and retry contract.*

> Two transactions can each be locally sensible and still create a history no one intended. Isolation is the rulebook for which overlapping histories the database may expose.

> **In real life**
>
> A transit map can show one snapshot or update between every glance. Read Committed gives PostgreSQL statements fresh snapshots; Repeatable Read keeps a transaction snapshot; Serializable rejects histories that cannot be ordered safely.

**transaction isolation level**: A transaction isolation level specifies which effects of concurrent transactions may become visible and which anomalous histories the database must prevent. PostgreSQL implements Read Committed, Repeatable Read, and Serializable; its Read Uncommitted behaves as Read Committed.

## Map the anomaly before choosing the level

- **Dirty read:** reading another transaction's uncommitted data.
- **Nonrepeatable read:** rereading a row and seeing a committed change.
- **Phantom read:** rerunning a predicate and seeing a changed matching set.
- **Serialization anomaly:** a result impossible under any serial ordering, such as write skew.

PostgreSQL's default **Read Committed** takes a new snapshot per statement. **Repeatable Read** uses a stable transaction snapshot and, unlike the SQL minimum, prevents phantom reads in PostgreSQL, but serialization anomalies remain possible. **Serializable** detects dangerous dependencies and may abort a transaction; the application must retry the entire transaction.

> **Tip**
>
> Name the anomaly your invariant cannot tolerate. Choosing Serializable everywhere without a retry loop merely trades silent corruption for visible failures.

> **Common mistake**
>
> Copying an isolation matrix from another database. PostgreSQL maps Read Uncommitted to Read Committed and gives stronger phantom protection at Repeatable Read than the standard minimum.

![Historic London Underground map with intersecting colored railway lines](isolation-levels-and-anomalies.jpg)
*Tube map 1908 — Wikimedia Commons, public domain. [Source](https://commons.wikimedia.org/wiki/File:Tube_map_1908.jpg)*
- **Transaction A** — One route reads and writes from its own snapshot.
- **Dependency crossing** — Concurrent routes can create a cycle that has no safe serial order.
- **Retry route** — Serializable may cancel one route so it can restart on a fresh snapshot.

**How PostgreSQL Serializable resolves a dangerous history**

1. **Transactions take snapshots** — Each begins work from a coherent visible state.
2. **Reads and writes create dependencies** — The server tracks relationships relevant to serialization.
3. **A dangerous structure appears** — The combined history cannot safely remain as observed.
4. **One transaction aborts** — PostgreSQL reports a serialization failure instead of committing the anomaly.
5. **Application retries all logic** — The full transaction reruns against a new state.

*Run it — compare statement and transaction snapshots (Python)*

```python
versions = [{"alice": 100}, {"alice": 70}]

read_committed = [versions[0]["alice"], versions[1]["alice"]]
repeatable_read_snapshot = versions[0]
repeatable_read = [repeatable_read_snapshot["alice"], repeatable_read_snapshot["alice"]]

print("Read Committed:", read_committed)
print("Repeatable Read:", repeatable_read)

# Read Committed: [100, 70]
# Repeatable Read: [100, 100]
```

*Run it — classify a write-skew history (Java)*

```java
public class Main {
  public static void main(String[] args) {
    boolean aliceOnCall = true, bobOnCall = true;
    boolean txASeesCoverage = bobOnCall;
    boolean txBSeesCoverage = aliceOnCall;
    if (txASeesCoverage) aliceOnCall = false;
    if (txBSeesCoverage) bobOnCall = false;
    System.out.println("alice=" + aliceOnCall + ", bob=" + bobOnCall);
    System.out.println("invariant preserved=" + (aliceOnCall || bobOnCall));
  }
}
/* alice=false, bob=false
   invariant preserved=false */
```

### Your first time: Your mission: reproduce one anomaly

- [ ] Open two independent sessions — One connection cannot model overlapping transactions.
- [ ] Coordinate the read boundary — Use a barrier so both transactions observe the intended starting state.
- [ ] Run under two isolation levels — Record results and SQLSTATE, not only elapsed time.
- [ ] Add a full-transaction retry — Prove Serializable failure becomes a correct final result.

You have tested a concurrency contract, not merely a happy-path query.

- **A value changes between two reads at Read Committed.**
  That level uses per-statement snapshots in PostgreSQL; use a stronger level or lock when the invariant requires stability.
- **Serializable intermittently returns SQLSTATE 40001.**
  Treat it as an expected retry signal and rerun the whole transaction with bounded backoff.
- **Repeatable Read still allows write skew.**
  PostgreSQL Repeatable Read prevents phantoms but not every serialization anomaly; use Serializable or explicit coordination.

### Where to check

- `SHOW transaction_isolation` and transaction-scoped settings.
- SQLSTATE `40001` and retry telemetry.
- Exact snapshots implied by statement order.
- Invariants across all rows touched logically, not only rows updated physically.

### Worked example: two doctors leave the same shift

1. Alice and Bob are both on call; the rule requires at least one.
2. Two Repeatable Read transactions each see the other on call.
3. Each updates only its own row to off call.
4. Both changes can commit, leaving nobody on call: write skew.
5. PostgreSQL Serializable detects the unsafe dependency structure and aborts one transaction for retry.

**Quiz.** Which PostgreSQL-specific statement is true?

- [ ] Read Uncommitted exposes dirty reads
- [ ] Repeatable Read permits phantom reads
- [x] Read Uncommitted behaves as Read Committed, and Repeatable Read prevents phantoms
- [ ] Serializable transactions never need retries

*PostgreSQL implements Read Uncommitted as Read Committed and its Repeatable Read is stronger than the standard minimum for phantoms.*

- **Read Committed snapshot** — A new snapshot at the start of each command in PostgreSQL.
- **Write skew** — Transactions read overlapping facts but write different rows, jointly breaking an invariant.
- **Serialization failure** — A retryable abort used to prevent an unsafe concurrent history.

### Challenge

Design a two-session test for a seat-capacity invariant. Predict outcomes under Read Committed, Repeatable Read, and Serializable, including required retries.

### Ask the community

> At `[isolation]`, sessions A/B execute `[timeline]` and produce `[outcome/SQLSTATE]`. The invariant is `[rule]`. Which anomaly explains it?

Include the interleaving; final values alone hide the cause.

- [PostgreSQL — Transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL — SET TRANSACTION](https://www.postgresql.org/docs/current/sql-set-transaction.html)

🎬 [Transactions: myths, surprises and opportunities — Martin Kleppmann](https://www.youtube.com/watch?v=5ZjhNTM8XU8) (41 min)

- Isolation levels define permitted concurrent histories.
- PostgreSQL Read Committed uses a fresh snapshot per statement.
- PostgreSQL Repeatable Read prevents phantoms but can allow serialization anomalies.
- Serializable can abort work to preserve a serializable history.
- Correct Serializable clients retry the entire transaction.


## Related notes

- [[Notes/relational-databases-engineer-level/transactions-and-concurrency/acid-properly|ACID, properly]]
- [[Notes/relational-databases-engineer-level/transactions-and-concurrency/locks-and-deadlocks|Locks & deadlocks]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/transactions-and-concurrency/isolation-levels-and-anomalies.mdx`_
