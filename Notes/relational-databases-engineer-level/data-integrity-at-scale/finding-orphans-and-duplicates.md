---
title: "Finding Orphans and Duplicates"
tags: ["sql", "data-quality", "duplicates", "referential-integrity"]
updated: "2026-07-17"
---

# Finding Orphans and Duplicates

*Detect, explain, and safely repair orphaned relationships and duplicate business identities at scale.*

> Finding bad rows is easy; proving which row is canonical and why the damage happened is the engineering work. A cleanup without a prevention step is tomorrow’s incident queue.

> **In real life**
>
> Duplicate records are look-alike buildings on one block: appearance is not identity. You need addresses, governed keys, and provenance. Orphans are records whose claimed address has no valid parent under the declared relationship.

## Detect without inventing truth

Find **orphans**: A row whose applicable child reference has no matching eligible parent. with `NOT EXISTS` or a left anti-join, respecting nullable relationships. Find duplicates by the normalized business key—not blindly by every column. Use `GROUP BY ... HAVING count(*) > 1` for groups and `row_number()` for deterministic review candidates.

![Similar brick buildings illustrating why appearance alone cannot establish record identity](finding-orphans-and-duplicates.jpg)
*Photo: Paul Sableman — Wikimedia Commons, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Identical_Twins_(30029275635).jpg)*
- **Similar appearance** — Two records may share attributes without representing the same entity, just as neighboring buildings can look alike.
- **Governed identity** — A stable key and provenance determine whether rows are duplicates or legitimate siblings.
- **Decision evidence** — Timestamps, source priority, references, and business rules choose a survivor safely.

> **Tip**
>
> Materialize candidate keys and counts before repair. Review a stratified sample: largest groups, oldest groups, newest groups, and groups spanning source systems.

> **Common mistake**
>
> Deleting every row with `row_number() > 1` before repointing children. A “duplicate” may own references, history, or distinct attributes that must be merged.

**From anomaly to prevention**

1. **Define identity** — Write the relationship or normalized business-key rule.
2. **Detect** — Produce stable candidate keys, counts, and provenance without mutating data.
3. **Reconcile** — Choose survivor, merge attributes, repoint children, and archive evidence.
4. **Prevent** — Add a constraint, ingestion rule, and recurring monitor.

*Group duplicate candidates*

```python
emails = ["A@EXAMPLE.COM ", "a@example.com", "b@example.com"]
counts = {}
for email in emails:
    key = email.strip().lower()
    counts[key] = counts.get(key, 0) + 1

duplicates = {key: count for key, count in counts.items() if count > 1}
assert duplicates == {"a@example.com": 2}
print(duplicates)
```

*Group the same candidates in Java*

```java
import java.util.*;
class Main {
  public static void main(String[] args) {
    List<String> emails = List.of("A@EXAMPLE.COM ", "a@example.com", "b@example.com");
    Map<String, Integer> counts = new TreeMap<>();
    for (String email : emails) {
      String key = email.trim().toLowerCase(Locale.ROOT);
      counts.put(key, counts.getOrDefault(key, 0) + 1);
    }
    counts.forEach((key, count) -> { if (count > 1) System.out.println(key + " -> " + count); });
  }
}
```

### Your first time: Investigate one anomaly class

- [ ] Define the rule — State nullable relationship semantics or exact normalization used for identity.
- [ ] Count and sample — Keep detection read-only and preserve candidate keys for reruns.
- [ ] Trace references — Identify children, history, and source ownership before selecting survivors.
- [ ] Repair then prevent — Repoint, merge, validate totals, and add enforceable protection.

- **An orphan query flags optional relationships.**
  Exclude null child keys when null means no relationship; do not confuse absence with a broken reference.
- **Duplicate counts change between runs.**
  Run on a consistent snapshot or staging copy and store candidate keys with the extraction boundary.
- **Cleanup loses history.**
  Repoint dependent rows and preserve an old-to-survivor mapping before deleting or archiving candidates.

### Where to check

Inspect declared keys and constraints, source-system IDs, child reference counts, created/updated timestamps, audit history, ingestion normalization, and the query plan for anti-joins or grouping.

### Worked example: Reconciling duplicate customer emails

Normalize email with the approved rule and find a two-row group. Choose the verified CRM record as survivor, merge non-conflicting attributes, repoint orders in one transaction, store loser-to-survivor mapping, assert order totals unchanged, then add a matching unique expression or generated-key constraint.

**Quiz.** What must happen before deleting a duplicate candidate?

- [ ] Sort it alphabetically
- [x] Prove the identity rule, choose a survivor, and account for references/history
- [ ] Disable all constraints
- [ ] Trust the newest row

*Similarity is only a candidate signal; reconciliation needs governed identity and dependency evidence.*

- **Orphan** — A non-null child reference with no matching eligible parent.
- **Business-key duplicate** — Multiple rows claiming one governed identity after approved normalization.
- **Survivor mapping** — Durable old-key to canonical-key evidence used to repoint and audit cleanup.

### Challenge

Write one orphan query and one duplicate-candidate query for your schema. Add null semantics, survivor policy, dependency checks, reconciliation invariants, and prevention DDL.

### Ask the community

> Identity/relationship rule: [definition]. Candidate count: [count]. References: [evidence]. Survivor policy: [rule]. Invariant after repair: [check]. What could this merge erase?

Share the normalization rule explicitly; “same email” is not precise enough.

- [PostgreSQL — Subquery Expressions and EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html)
- [PostgreSQL — Window Functions](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL — Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)

🎬 [Learn PostgreSQL — Full Course for Beginners](https://www.youtube.com/watch?v=qw--VYLpxG4) (260 min)

- Define identity and null semantics before labeling anomalies.
- Detection should be repeatable, read-only, and keyed.
- Repoint dependencies and preserve survivor mappings before deletion.
- Every repair needs invariant checks plus a prevention mechanism.


## Related notes

- [[Notes/relational-databases-engineer-level/data-integrity-at-scale/constraints-and-referential-integrity|Constraints & referential integrity]]
- [[Notes/relational-databases-engineer-level/data-integrity-at-scale/migrations-and-etl-verification|Migrations & ETL verification]]
- [[Notes/relational-databases-engineer-level/data-integrity-at-scale/auditing-data-changes|Auditing data changes]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/data-integrity-at-scale/finding-orphans-and-duplicates.mdx`_
