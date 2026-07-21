---
title: "Subqueries & CTEs"
tags: ["relational-databases-engineer-level", "sql-mastery", "track-e"]
updated: "2026-07-17"
---

# Subqueries & CTEs

*Use subqueries for local questions and CTEs for named stages, recursive traversal, or deliberate materialization—then inspect the plan instead of assuming WITH is a performance spell.*

> A CTE can make a query readable without making it fast. Naming the mess is progress; measuring the plan is engineering.

> **In real life**
>
> Nesting dolls answer an inner question before the outer shell can use it. A CTE puts each doll on the table and gives it a name.

**subquery and CTE**: A subquery is a query nested inside another SQL expression. A common table expression (CTE) is a named query introduced by WITH for use within one statement; WITH RECURSIVE can refer to its own prior output.

## Choose the shape that exposes intent

```sql
WITH failed_runs AS (
  SELECT build_id, count(*) AS failures
  FROM test_runs
  WHERE status = 'failed'
  GROUP BY build_id
)
SELECT b.id, f.failures
FROM builds b JOIN failed_runs f ON f.build_id = b.id
WHERE f.failures >= 3;
```

In current PostgreSQL, a side-effect-free non-recursive CTE referenced once can be folded into its
parent. `MATERIALIZED` forces separate calculation; `NOT MATERIALIZED` permits folding. Verify with
`EXPLAIN`, because folklore from older versions ages like milk in a server room.

> **Tip**
>
> Use `EXISTS` when the question is “does any related row exist?” It can express intent better than counting every match.

> **Common mistake**
>
> Assuming every CTE is an optimization fence. That is version-sensitive and reference-sensitive; read the actual plan.

![A row of opened and nested Matryoshka dolls](subqueries-and-ctes.jpg)
*Matryoshka dolls — Marit and Toomas Hinnosaar, Wikimedia Commons, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Matryoshka_dolls_(6392117189).jpg)*
- **Inner query** — Produces a result the outer query consumes.
- **Named CTE** — Makes a stage readable and reusable inside one statement.
- **Outer query** — Combines and filters the staged evidence.

**Build a staged investigation**

1. **State the question** — Existence, scalar comparison, staged aggregation, or recursion?
2. **Choose subquery or CTE** — Keep a local expression local; name multi-step logic.
3. **Assert cardinality** — A scalar subquery must return at most one row.
4. **Inspect EXPLAIN** — Confirm folding, materialization, joins, and row estimates.

*Run it — staged failure aggregation (Python)*

```python
runs = [(101, "failed"), (101, "passed"), (102, "failed"), (102, "failed"), (102, "failed")]
failed = {}
for build, status in runs:
    if status == "failed": failed[build] = failed.get(build, 0) + 1
result = [(build, count) for build, count in failed.items() if count >= 3]
print(result)

# [(102, 3)]
```

*Run it — staged failure aggregation (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    String[][] runs={{"101","failed"},{"101","passed"},{"102","failed"},{"102","failed"},{"102","failed"}};
    Map<String,Integer> failed=new TreeMap<>();
    for(String[] r:runs) if(r[1].equals("failed")) failed.merge(r[0],1,Integer::sum);
    failed.entrySet().stream().filter(e->e.getValue()>=3).forEach(e->System.out.println("[("+e.getKey()+", "+e.getValue()+")]"));
  }
}

/* [(102, 3)] */
```

### Your first time: Your mission: refactor and measure

- [ ] Write the result first as one query — Capture expected rows on fixed test data.
- [ ] Extract one meaningful stage into a CTE — Name business meaning, not temp1.
- [ ] Compare EXPLAIN plans — Try default, MATERIALIZED, and NOT MATERIALIZED where legal.
- [ ] Assert result equivalence — A prettier rewrite must not change duplicates or null behavior.

- **Scalar subquery returns more than one row.**
  Fix the data relationship or use an aggregate/EXISTS; LIMIT 1 merely hides ambiguity unless ordering defines truth.
- **Recursive CTE never finishes.**
  Add a termination condition and cycle handling; test a cyclic graph deliberately.
- **CTE rewrite becomes slower.**
  Compare plans and row estimates; repeated references may benefit from materialization while selective predicates may benefit from folding.

### Where to check

- `EXPLAIN (ANALYZE, BUFFERS)` in a safe test environment.
- Row counts and duplicate behavior at every stage.
- PostgreSQL `WITH` documentation for folding and recursion rules.

### Worked example: a readable query that still scans too much

A CTE aggregates all historical failures, then the outer query selects one week. `EXPLAIN` shows a broad materialized scan. Moving the week predicate into the CTE—or allowing folding—cuts input rows while preserving the result.

**Quiz.** Does WITH always force PostgreSQL to materialize a CTE?

- [ ] Yes
- [x] No; eligible side-effect-free non-recursive CTEs can be folded
- [ ] Only on Tuesdays
- [ ] Only when named

*Current PostgreSQL can fold eligible CTEs; MATERIALIZED and NOT MATERIALIZED influence that choice.*

- **Scalar subquery** — Must produce at most one row where a single value is required.
- **EXISTS** — Tests whether any related row exists without asking for a count.
- **MATERIALIZED** — Forces separate calculation of the CTE.
- **Recursive CTE** — A non-recursive seed plus recursive term evaluated until no new rows emerge.

### Challenge

Write an `EXISTS` test for builds with failures, then a CTE for builds with at least three failures. Prove both against duplicates and empty input.

### Ask the community

> My PostgreSQL CTE changed runtime from `[before]` to `[after]`; here are sanitized EXPLAIN plans and row counts.

Include server version and whether the CTE is referenced once or repeatedly.

- [PostgreSQL — WITH queries and CTE materialization](https://www.postgresql.org/docs/current/queries-with.html)
- [PostgreSQL — subquery expressions](https://www.postgresql.org/docs/current/functions-subquery.html)

🎬 [freeCodeCamp — SQL tutorial, full database course](https://www.youtube.com/watch?v=HXV3zeQKqGY) (261 min)

- Subqueries answer local nested questions; CTEs name stages and support recursion.
- Current PostgreSQL can fold eligible CTEs into the parent query.
- MATERIALIZED and NOT MATERIALIZED are plan controls, not decorations.
- Test cardinality, duplicates, nulls, and plans after every rewrite.


## Related notes

- [[Notes/relational-databases-engineer-level/sql-mastery/window-functions|Window functions]]
- [[Notes/relational-databases-engineer-level/sql-mastery/set-operators|Set operators]]
- [[Notes/relational-databases-engineer-level/indexes-and-performance/reading-explain-and-execution-plans|Reading EXPLAIN & execution plans]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/sql-mastery/subqueries-and-ctes.mdx`_
