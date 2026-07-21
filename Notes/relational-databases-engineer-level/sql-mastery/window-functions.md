---
title: "Window functions"
tags: ["relational-databases-engineer-level", "sql-mastery", "track-e"]
updated: "2026-07-17"
---

# Window functions

*Window functions calculate ranks, running totals, lagged comparisons, and partition metrics while preserving each source row—provided ordering and frames are explicit.*

> A running total without deterministic ordering is not analytics. It is a number generator with office clothes.

> **In real life**
>
> Each building window keeps its identity while sharing a façade and floor. Window functions keep every row while calculating across its partition and frame.

**window function**: A window function calculates across rows related to the current row without collapsing them into one aggregate row. The OVER clause defines partitioning, ordering, and optionally the window frame.

## Partition, order, frame

```sql
SELECT suite, finished_at, duration_ms,
       row_number() OVER (PARTITION BY suite ORDER BY finished_at, id) AS run_no,
       avg(duration_ms) OVER (
         PARTITION BY suite ORDER BY finished_at, id
         ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS moving_avg
FROM test_runs;
```

Window functions run after `WHERE`, grouping, and `HAVING`, so filter their results in an outer query
or CTE. Add a unique tie-breaker to ordering when row sequence matters.

> **Tip**
>
> Spell out `ROWS` frames for running aggregates. The default frame with ordering can include peer rows and surprise anyone who assumed “current physical row.”

> **Common mistake**
>
> Using `last_value` with the default frame and expecting the last row of the partition. The default usually ends at the current row's last peer.

![Repeating windows across a building facade](window-functions.jpg)
*Windows on building facade — Philip Halling, Wikimedia Commons, CC BY-SA 2.0. [Source](https://commons.wikimedia.org/wiki/File:Windows_on_building_facade_-_geograph.org.uk_-_6854299.jpg)*
- **Partition** — A floor-like group calculated independently.
- **Current row** — One window remains one output row.
- **Frame** — The neighboring rows visible to this calculation.

**Make a window deterministic**

1. **Choose partition** — Define independent business groups.
2. **Choose ordering** — Add a unique tie-breaker when sequence matters.
3. **Choose frame** — ROWS, RANGE, or GROUPS determines visible peers.
4. **Filter outside** — Use a CTE/subquery for top-N or rank filters.

*Run it — row numbers within suites (Python)*

```python
runs = [("api", 12, 102), ("ui", 8, 201), ("api", 12, 101), ("ui", 9, 202)]
for suite in sorted({r[0] for r in runs}):
    ordered = sorted((r for r in runs if r[0] == suite), key=lambda r: (r[1], r[2]))
    for rank, row in enumerate(ordered, 1): print(suite, row[2], rank)

# api 101 1
# api 102 2
# ui 201 1
# ui 202 2
```

*Run it — row numbers within suites (Java)*

```java
import java.util.*;
public class Main {
  record Run(String suite,int time,int id){}
  public static void main(String[] args){
    List<Run> runs=new ArrayList<>(List.of(new Run("api",12,102),new Run("ui",8,201),new Run("api",12,101),new Run("ui",9,202)));
    runs.sort(Comparator.comparing(Run::suite).thenComparingInt(Run::time).thenComparingInt(Run::id));
    String last=""; int rank=0;
    for(Run r:runs){ if(!r.suite().equals(last)){last=r.suite();rank=0;} System.out.println(r.suite()+" "+r.id()+" "+(++rank)); }
  }
}

/* api 101 1
   api 102 2
   ui 201 1
   ui 202 2 */
```

### Your first time: Your mission: rank without collapsing

- [ ] Create tied timestamps — Include unique IDs so deterministic order can be tested.
- [ ] Add row_number per suite — Order by timestamp and ID.
- [ ] Add a three-row moving average — Declare ROWS BETWEEN 2 PRECEDING AND CURRENT ROW.
- [ ] Filter top two in an outer query — Window outputs are not available to WHERE in the same SELECT level.

- **Rank changes between runs.**
  Add a stable unique tie-breaker to the window ORDER BY.
- **Running total jumps across tied rows.**
  Inspect the frame; use explicit ROWS if physical row progression is intended.
- **Window function is rejected in WHERE.**
  Calculate it in a CTE or subquery, then filter outside.

### Where to check

- The full `OVER` clause: partition, order, and frame.
- Tied ordering values in test data.
- Outer query filters and execution plan sort nodes.

### Worked example: a flaky top-two query

Two runs share `finished_at`. Ordering only by time lets their row numbers swap. Adding `id` makes rank stable, and a regression test repeats the query to prove deterministic output.

**Quiz.** Why can a window function not be referenced in WHERE at the same SELECT level?

- [ ] It is text
- [x] Window functions are logically evaluated after WHERE
- [ ] PostgreSQL lacks WHERE
- [ ] Only ranks are forbidden

*PostgreSQL documents window functions as executing after WHERE, grouping, and HAVING.*

- **PARTITION BY** — Splits rows into independent calculation groups.
- **ORDER BY in OVER** — Defines sequence and peers inside the partition.
- **Window frame** — The subset of the partition visible to a frame-sensitive calculation.
- **row_number vs rank** — row_number is unique sequence; rank gives peers the same rank and leaves gaps.

### Challenge

Return the slowest two tests per suite and a three-run moving average, including ties and deterministic ordering.

### Ask the community

> My window result changes around tied values; here is the OVER clause and minimal rows.

Show the unique key and expected peer behavior.

- [PostgreSQL — window functions tutorial](https://www.postgresql.org/docs/current/tutorial-window.html)
- [PostgreSQL — window function reference](https://www.postgresql.org/docs/current/functions-window.html)

🎬 [freeCodeCamp — SQL tutorial, full database course](https://www.youtube.com/watch?v=HXV3zeQKqGY) (261 min)

- Window functions preserve rows while calculating across related rows.
- Deterministic ordering needs a unique tie-breaker.
- Explicit frames prevent peer-related surprises.
- Filter window outputs in an outer query or CTE.


## Related notes

- [[Notes/relational-databases-engineer-level/sql-mastery/subqueries-and-ctes|Subqueries & CTEs]]
- [[Notes/relational-databases-engineer-level/sql-mastery/date-time-and-timezone-handling|Date, time & timezone handling]]
- [[Notes/relational-databases-engineer-level/sql-mastery/set-operators|Set operators]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/sql-mastery/window-functions.mdx`_
