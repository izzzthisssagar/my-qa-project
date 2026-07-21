---
title: "Constraints and Referential Integrity"
tags: ["postgresql", "constraints", "foreign-keys", "data-integrity"]
updated: "2026-07-17"
---

# Constraints and Referential Integrity

*Design and verify PostgreSQL constraints as executable invariants, including safe validation on large tables.*

> Application validation is a polite request; a database constraint is a boundary every writer must cross. At scale, correctness includes both the invariant and a rollout that does not freeze the system.

> **In real life**
>
> Constraints are a perimeter fence. Primary and unique keys control identity, checks define allowed shapes, and foreign keys keep children inside a valid parent boundary. A gate nobody inspects is only decoration.

## Make invariants executable

Use `NOT NULL`, `CHECK`, `UNIQUE`, `PRIMARY KEY`, and **`FOREIGN KEY`**: A constraint requiring each applicable child key to match an eligible parent key. for facts the database must defend. PostgreSQL does not automatically create an index on the referencing side of a foreign key, so parent updates or deletes may need an explicit child-column index.

![A chain-link fence representing database integrity boundaries](constraints-and-referential-integrity.jpg)
*Photo: Evan-Amos — Wikimedia Commons, CC0. [Source](https://commons.wikimedia.org/wiki/File:Chain-link-Fence.jpg)*
- **Identity** — Primary and unique constraints prevent two rows from claiming the same governed key.
- **Allowed shape** — NOT NULL and CHECK reject incomplete or invalid row states.
- **Relationship** — A foreign key requires each non-null child key to match an eligible parent key.

> **Tip**
>
> For large existing tables, add a CHECK or FOREIGN KEY as `NOT VALID`, repair historical rows, then run `VALIDATE CONSTRAINT`. New and updated rows are still checked while validation is pending.

> **Common mistake**
>
> Assuming a foreign key creates the child-side index. It does not; inspect the query workload and index the referencing columns when parent changes or joins require it.

**Safe constraint rollout**

1. **Define invariant** — Name the precise row or relationship rule and its null semantics.
2. **Detect violations** — Measure historical bad rows before changing production behavior.
3. **Enforce forward** — Add a supported CHECK or FOREIGN KEY as NOT VALID so new writes comply.
4. **Repair + validate** — Backfill violations, validate the named constraint, and monitor lock impact.

*Model relationship validation*

```python
customers = {10, 20}
orders = [
    {"id": 1, "customer_id": 10, "total": 8},
    {"id": 2, "customer_id": 99, "total": 4},
    {"id": 3, "customer_id": 20, "total": -1},
]

violations = []
for order in orders:
    if order["customer_id"] not in customers:
        violations.append((order["id"], "foreign key"))
    if order["total"] < 0:
        violations.append((order["id"], "check total >= 0"))
print(violations)
assert len(violations) == 2
```

*Validate parent references in Java*

```java
import java.util.*;
class Main {
  public static void main(String[] args) {
    Set<Integer> customers = Set.of(10, 20);
    Map<Integer,Integer> orders = Map.of(1, 10, 2, 99, 3, 20);
    List<Integer> orphans = new ArrayList<>();
    orders.forEach((id, customer) -> { if (!customers.contains(customer)) orphans.add(id); });
    if (!orphans.equals(List.of(2))) throw new AssertionError(orphans);
    System.out.println("orphan order ids: " + orphans);
  }
}
```

### Your first time: Audit one relationship

- [ ] State the invariant — Define identity, null behavior, and delete/update policy in plain language.
- [ ] Query current violations — Count and sample invalid rows before adding enforcement.
- [ ] Inspect indexes — Verify parent uniqueness and decide whether child columns need an index.
- [ ] Roll out and validate — Enforce future writes, repair history, then confirm validation state.

- **Adding the constraint blocks a busy table.**
  Rehearse lock behavior; use NOT VALID plus later VALIDATE where PostgreSQL supports it.
- **Parent deletes become unexpectedly slow.**
  Inspect an index beginning with the referencing foreign-key columns and verify with EXPLAIN.
- **A CHECK allows null unexpectedly.**
  CHECK succeeds for true or null; add NOT NULL when absence itself is forbidden.

### Where to check

Inspect `pg_constraint`, `information_schema.table_constraints`, `referential_constraints`, `pg_indexes`, constraint validation state, SQLSTATE, and lock waits during rehearsal.

### Worked example: Adding an order-customer foreign key

Count orders whose non-null customer_id has no customer. Add `orders_customer_fk` as NOT VALID, verify a new orphan is rejected, repair historical orphans, then `VALIDATE CONSTRAINT`. Confirm `convalidated` and benchmark parent update/delete with the child index.

**Quiz.** What does a PostgreSQL NOT VALID foreign key allow?

- [ ] New invalid rows
- [x] Skipping the initial historical scan while checking new or updated rows
- [ ] Disabling the constraint permanently
- [ ] Dropping parent uniqueness

*It separates forward enforcement from validation of preexisting data.*

- **Referential integrity** — Every applicable child key matches an eligible parent key under the declared policy.
- **NOT VALID** — Adds supported constraints without first scanning all historical rows; new writes are enforced.
- **CHECK and null** — A CHECK rejects false, but null passes; pair with NOT NULL when required.

### Challenge

Pick one high-volume relationship. Produce the violation query, null policy, action policy, index check, NOT VALID rollout, repair rule, and VALIDATE gate.

### Ask the community

> Invariant: [rule]. PostgreSQL version: [version]. Current violations: [count]. Proposed constraint/index: [DDL]. Rehearsed locks/timing: [evidence]. Is rollout safe?

Include table size and write rate; safe DDL is workload-specific.

- [PostgreSQL — Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL — ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)

🎬 [Learn PostgreSQL — Full Course for Beginners](https://www.youtube.com/watch?v=qw--VYLpxG4) (260 min)

- Constraints defend invariants against every writer.
- CHECK does not imply NOT NULL, and foreign keys do not create child-side indexes.
- NOT VALID can separate forward enforcement from historical validation.
- Measure violations and rehearse locks before production DDL.


## Related notes

- [[Notes/relational-databases-engineer-level/data-integrity-at-scale/finding-orphans-and-duplicates|Finding orphans & duplicates]]
- [[Notes/relational-databases-engineer-level/data-integrity-at-scale/migrations-and-etl-verification|Migrations & ETL verification]]
- [[Notes/relational-databases-engineer-level/programmable-objects/error-handling-in-sql|Error handling in SQL]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/data-integrity-at-scale/constraints-and-referential-integrity.mdx`_
