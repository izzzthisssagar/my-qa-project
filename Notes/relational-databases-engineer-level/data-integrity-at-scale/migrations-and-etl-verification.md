---
title: "Migrations and ETL Verification"
tags: ["postgresql", "migrations", "etl", "data-reconciliation"]
updated: "2026-07-17"
---

# Migrations and ETL Verification

*Verify schema migrations and ETL movement with phased gates, reconciliation, invariants, and rollback evidence.*

> A migration that exits zero can still lose, duplicate, truncate, or mis-map data. Verification must prove structure, meaning, completeness, and operability at the same extraction boundary.

> **In real life**
>
> ETL is container shipping. Counting containers at departure and arrival helps, but seals, manifests, weights, and destination scans prove the same cargo arrived intact.

## Gate the change in layers

Separate schema change, backfill, forward-write enforcement, validation, and cleanup when risk or scale demands it. Reconcile source and target using a shared **watermark**: A stable extraction boundary that makes two data sets comparable. or consistent snapshot. Counts are necessary but weak; add key-set differences, grouped totals, null distributions, checksums, referential checks, and sampled row comparisons.

![A container ship illustrating controlled data movement](migrations-and-etl-verification.jpg)
*Photo: Syukrimsw — Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:ContainerShip.jpg)*
- **Source manifest** — Define extraction boundary, keys, counts, and aggregates before movement.
- **Transformation** — Mapping rules, defaults, type conversions, and rejected rows require explicit evidence.
- **Arrival reconciliation** — Compare key sets, distributions, totals, constraints, and samples at the same watermark.

> **Tip**
>
> Store every verification query and result with migration version, start/end timestamps, source watermark, row counts, and rejection count. A dashboard without a boundary is not reconcilable evidence.

> **Common mistake**
>
> Comparing a live source count at 10:00 with a target count at 10:20. New writes make both numbers valid and the comparison meaningless.

**Migration gates**

1. **Baseline** — Capture schema, volume, anomalies, performance, and a stable extraction boundary.
2. **Move** — Apply compatible DDL and idempotent batches with checkpoints and rejection handling.
3. **Reconcile** — Compare keys, totals, distributions, constraints, and samples at the same boundary.
4. **Cut over** — Observe application behavior, retain rollback/forward-fix evidence, then clean legacy paths.

*Reconcile an ETL batch*

```python
source = {"A": 120, "B": 80, "C": 50}
target = {"A": 120, "B": 80, "C": 50}

missing = sorted(source.keys() - target.keys())
extra = sorted(target.keys() - source.keys())
mismatched = sorted(k for k in source.keys() & target.keys() if source[k] != target[k])

assert not missing and not extra and not mismatched
assert sum(source.values()) == sum(target.values())
print({"rows": len(target), "total": sum(target.values()), "status": "reconciled"})
```

*Reconcile the batch in Java*

```java
import java.util.*;
class Main {
  public static void main(String[] args) {
    Map<String,Integer> source = Map.of("A",120,"B",80,"C",50);
    Map<String,Integer> target = Map.of("A",120,"B",80,"C",50);
    if (!source.keySet().equals(target.keySet())) throw new AssertionError("key mismatch");
    for (String key : source.keySet())
      if (!source.get(key).equals(target.get(key))) throw new AssertionError(key);
    System.out.println("reconciled keys: " + new TreeSet<>(target.keySet()));
  }
}
```

### Your first time: Verify one migration

- [ ] Freeze the comparison boundary — Use a snapshot, watermark, or immutable batch identifier.
- [ ] Verify schema and mapping — Check types, defaults, nullability, indexes, constraints, and transformation rules.
- [ ] Reconcile content — Compare key sets, grouped totals, distributions, rejects, and deterministic samples.
- [ ] Prove recovery — Rehearse retry, resume, rollback or forward-fix, and application compatibility.

- **Counts match but money totals do not.**
  Add domain aggregates and per-key comparisons; duplicates can cancel missing rows at count level.
- **A backfill rerun duplicates target rows.**
  Use deterministic source keys, upsert or checkpoint semantics, and test the same batch twice.
- **DDL is correct but deployment stalls writes.**
  Rehearse locks and duration at representative scale; split schema, backfill, validation, and cleanup phases.

### Where to check

Keep migration version/checksum, DDL state, lock waits, batch checkpoints, `COPY` row counts, rejection tables, source/target key diffs, aggregates, constraint validation, query plans, and application error rate.

### Worked example: Moving legacy orders into a typed table

At watermark W, record source keys, row count, total amount, null/status distributions, and orphan count. Load in keyed batches. Compare target at W, inspect every reject, validate constraints, rerun one batch to prove idempotency, then run old and new reads in shadow before cutover.

**Quiz.** Why can equal source and target row counts still hide corruption?

- [ ] Counts are always rounded
- [x] A missing row and a duplicate can cancel, while values may also be transformed incorrectly
- [ ] PostgreSQL cannot count
- [ ] Indexes change row counts

*Counts measure volume, not identity or meaning; use key-set and domain reconciliation.*

- **Watermark** — A stable extraction boundary that makes source and target comparisons refer to the same data.
- **Reconciliation** — Evidence that identities, values, relationships, and aggregates agree across movement.
- **Idempotent batch** — Rerunning the same batch produces no additional unintended effect.

### Challenge

Design a verification ledger for one migration: boundary, schema gates, key diff, three domain aggregates, distributions, rejects, constraint checks, retry proof, and cutover rollback signal.

### Ask the community

> Migration/version: [id]. Boundary: [watermark]. Source/target keys and aggregates: [evidence]. Rejects: [count]. Retry result: [evidence]. Which reconciliation gap remains?

Include whether writes continued during extraction; it determines whether your comparison is valid.

- [PostgreSQL — Modifying Tables](https://www.postgresql.org/docs/current/ddl-alter.html)
- [PostgreSQL — COPY](https://www.postgresql.org/docs/current/sql-copy.html)
- [PostgreSQL — ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)

🎬 [Learn PostgreSQL — Full Course for Beginners](https://www.youtube.com/watch?v=qw--VYLpxG4) (260 min)

- Compare source and target at one explicit boundary.
- Counts need key-set, aggregate, distribution, relationship, and sample checks.
- Phase risky changes and verify locks at representative scale.
- Test retry and recovery before cutover, not during an incident.


## Related notes

- [[Notes/relational-databases-engineer-level/data-integrity-at-scale/constraints-and-referential-integrity|Constraints & referential integrity]]
- [[Notes/relational-databases-engineer-level/data-integrity-at-scale/finding-orphans-and-duplicates|Finding orphans & duplicates]]
- [[Notes/relational-databases-engineer-level/data-integrity-at-scale/auditing-data-changes|Auditing data changes]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/data-integrity-at-scale/migrations-and-etl-verification.mdx`_
