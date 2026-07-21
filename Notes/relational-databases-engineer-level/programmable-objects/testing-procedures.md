---
title: "Testing Procedures"
tags: ["postgresql", "procedures", "integration-testing", "transactions"]
updated: "2026-07-17"
---

# Testing Procedures

*Turn procedure testing into a repeatable arrange-call-assert-rollback discipline with exact state diffs.*

> A procedure test without a state diff is a smoke signal, not proof. Passing means the intended rows changed, forbidden rows did not, invariants held, and failures left no debris.

> **In real life**
>
> Testing a procedure is a bridge **load test**: A controlled test that applies known demand and measures the resulting behavior.. The bridge must carry the designed load, refuse unsafe conditions, return to a known state, and leave evidence engineers can compare.

## Build a deterministic harness

Use a dedicated schema or transaction-isolated fixture, stable identifiers, and assertions that identify rows by key. Prefer `BEGIN`/`ROLLBACK` around tests when the procedure does not control transactions itself. If it does, provision disposable data and clean it by owned keys.

![Engineers performing a bridge load test](testing-procedures.jpg)
*Umgeni River Bridge load test — Wikimedia Commons, public domain. [Source](https://commons.wikimedia.org/wiki/File:Umgeni_River_Bridge_Load_Test.jpg)*
- **Known load** — Fixtures must make input quantity and starting state explicit.
- **Observed structure** — Measure outputs, table diffs, emitted events, and invariant checks—not only completion.
- **Safety margin** — Boundary, overload, retry, and failure cases prove behavior beyond the demo path.

> **Tip**
>
> Give every test run a unique key. It makes cleanup exact, exposes accidental cross-test reads, and turns logs into attributable evidence.

> **Common mistake**
>
> Asserting total table counts in a shared database. Concurrent tests make counts noisy; assert the exact keys and relationships owned by this case.

**Procedure harness**

1. **Arrange** — Insert minimal fixtures plus an unrelated sentinel.
2. **Snapshot** — Capture relevant rows, invariants, and expected error contract.
3. **CALL** — Invoke as the application role with explicit parameters.
4. **Assert + clean** — Diff exact rows, then rollback or remove only run-owned data.

*Assert an exact state diff*

```python
before = {"A": 10, "B": 20, "SENTINEL": 99}
after = {"A": 7, "B": 23, "SENTINEL": 99}

changed = {key: (before[key], after[key]) for key in before if before[key] != after[key]}
assert changed == {"A": (10, 7), "B": (20, 23)}
assert sum(before.values()) == sum(after.values())
print("exact diff:", changed)
print("invariant: total preserved")
```

*Verify transfer invariants in Java*

```java
import java.util.*;
class Main {
  public static void main(String[] args) {
    Map<String,Integer> before = Map.of("A",10,"B",20,"SENTINEL",99);
    Map<String,Integer> after = Map.of("A",7,"B",23,"SENTINEL",99);
    int beforeTotal = before.values().stream().mapToInt(Integer::intValue).sum();
    int afterTotal = after.values().stream().mapToInt(Integer::intValue).sum();
    if (beforeTotal != afterTotal || !after.get("SENTINEL").equals(99))
      throw new AssertionError("contract broken");
    System.out.println("total preserved: " + afterTotal);
  }
}
```

### Your first time: Create a procedure test

- [ ] Name the contract — List outputs, allowed row changes, invariants, errors, and retry behavior.
- [ ] Arrange owned rows — Use stable test keys and at least one untouched sentinel.
- [ ] Call as production does — Use the application role and matching transaction boundary.
- [ ] Diff then clean — Assert exact rows and rollback; prove the next run starts clean.

- **The test passes alone but fails in the suite.**
  Remove shared identifiers, wall-clock assumptions, and global counts; namespace fixtures per run.
- **A failed call leaves partial data.**
  Assert atomicity across every touched table and inspect exception handling that may swallow an error.
- **Cleanup deletes another test's rows.**
  Delete only by the unique run key or prefer rollback-based isolation.

### Where to check

Capture procedure definition, role, transaction state, SQLSTATE, exact before/after rows, sequences, audit/event tables, and server logs. A test report should reconstruct the call.

### Worked example: Testing an account transfer

Arrange accounts A=10, B=20, sentinel=99. Call transfer(A,B,3). Assert A=7, B=23, sentinel=99, total=129, and one transfer record. Then call with 30 and assert the documented SQLSTATE plus zero row changes. Roll back and repeat to prove isolation.

**Quiz.** Why add a sentinel row to a procedure fixture?

- [ ] To increase row count
- [x] To prove unrelated data remained untouched
- [ ] To avoid using transactions
- [ ] To grant permissions

*A sentinel catches an over-broad UPDATE or DELETE that correct target assertions may miss.*

- **State diff** — The exact keyed rows and values that changed between snapshots.
- **Sentinel row** — Unrelated fixture data that must remain unchanged.
- **Deterministic fixture** — Owned, repeatable data without dependence on timing or concurrent global counts.

### Challenge

Write a four-case suite for one procedure: success, boundary, refusal, and retry. For each, list exact output, exact state diff, invariant, and cleanup proof.

### Ask the community

> Procedure: [signature]. Isolation: [transaction/schema]. Input: [values]. Expected/actual keyed diff: [evidence]. SQLSTATE: [code]. What leak remains?

Include the sentinel result and whether the procedure performs transaction control.

- [PostgreSQL — CALL](https://www.postgresql.org/docs/current/sql-call.html)
- [PostgreSQL — Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)

🎬 [Learn PostgreSQL — Full Course for Beginners](https://www.youtube.com/watch?v=qw--VYLpxG4) (260 min)

- A procedure test proves exact state changes and invariants, not absence of exceptions.
- Unique run keys and sentinels make hidden coupling visible.
- Test as the application role with the production transaction boundary.
- Rollback or exact owned-key cleanup must make reruns deterministic.


## Related notes

- [[Notes/relational-databases-engineer-level/programmable-objects/stored-procedures-and-functions|Stored procedures & functions]]
- [[Notes/relational-databases-engineer-level/programmable-objects/triggers|Triggers]]
- [[Notes/relational-databases-engineer-level/data-integrity-at-scale/migrations-and-etl-verification|Migrations & ETL verification]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/programmable-objects/testing-procedures.mdx`_
