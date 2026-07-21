---
title: "How an index works"
tags: ["relational-databases-engineer-level", "indexes-and-performance", "track-e"]
updated: "2026-07-17"
---

# How an index works

*A database index trades extra storage and write work for a faster route to selected rows. Learn PostgreSQL B-tree navigation, heap lookups, selectivity, and why the planner can correctly ignore your index.*

> A card catalogue is useful because it is smaller and ordered, not because the librarian glued every book into a drawer. An index points toward rows; it is not usually the table wearing a tiny hat.

> **In real life**
>
> A catalogue key leads to a shelf location. PostgreSQL's B-tree stores ordered keys with tuple identifiers; an index scan follows those references to heap tuples unless an index-only scan can answer from the index and visibility map.

**database index**: A database index is a separate access structure that maps indexed key values to table rows. PostgreSQL's default index method is B-tree, suited to equality and range comparisons on sortable data; other methods include Hash, GiST, SP-GiST, GIN, and BRIN for different operator and data patterns.

## The route from predicate to row

- B-tree internal pages narrow the key range; leaf entries identify candidate heap tuples.
- Equality and range predicates can use B-tree; only B-tree can directly provide ordered output in PostgreSQL.
- An index scan may still visit heap pages to check visibility and fetch unindexed columns.
- An index-only scan requires all requested columns in the index and enough all-visible heap pages.
- For a large fraction of a table, sequential access can be cheaper than scattered heap visits.

> **Tip**
>
> Design from real predicates and ordering, then verify with `EXPLAIN (ANALYZE, BUFFERS)`. "Indexed" is a physical fact; "faster" is a measured result.

> **Common mistake**
>
> Forcing an index because a sequential scan looks primitive. On a tiny table or low-selectivity predicate, sequential scanning can be the rational plan.

![Rows of wooden library card catalogue drawers with label holders and handles](how-an-index-works.jpg)
*Sterling Memorial Library card catalogue — Henry Trotter, Wikimedia Commons, public domain. [Source](https://commons.wikimedia.org/wiki/File:SML-Card-Catalog.jpg)*
- **Ordered labels** — Indexed keys narrow the search to a small region instead of inspecting every row.
- **Drawer entries** — Leaf entries point to row locations; they are not normally the whole row.
- **Many maintained copies** — Every relevant insert, update, and delete must maintain the catalogue too.

**What an index scan actually does**

1. **Planner estimates selectivity** — Statistics predict how many rows the predicate will match.
2. **B-tree narrows the key range** — Internal pages guide the scan toward matching leaf entries.
3. **Leaf entries yield tuple locations** — Candidates point to physical heap tuples.
4. **Heap visibility and columns are checked** — MVCC visibility and non-indexed values may require table-page visits.
5. **Rows flow to remaining plan nodes** — Sorts, joins, filters, and aggregates continue above the scan.

*Run it — compare linear and indexed lookup work (Python)*

```python
rows = [(i, f"ticket-{i}") for i in range(1, 1001)]
target = 901

linear_checks = 0
for key, value in rows:
    linear_checks += 1
    if key == target:
        linear_value = value
        break

index = {key: position for position, (key, _) in enumerate(rows)}
position = index[target]
print(f"linear scan: {linear_checks} row checks -> {linear_value}")
print(f"index lookup: 1 key lookup + 1 row fetch -> {rows[position][1]}")

# linear scan: 901 row checks -> ticket-901
# index lookup: 1 key lookup + 1 row fetch -> ticket-901
```

*Run it — compare linear and indexed lookup work (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    List<Integer> rows = new ArrayList<>();
    Map<Integer, Integer> index = new HashMap<>();
    for (int i = 1; i <= 1000; i++) { index.put(i, rows.size()); rows.add(i); }
    int checks = 0, target = 901;
    for (int key : rows) { checks++; if (key == target) break; }
    System.out.println("linear scan: " + checks + " row checks -> ticket-" + target);
    System.out.println("index lookup: 1 key lookup + 1 row fetch -> ticket-" + rows.get(index.get(target)));
  }
}
/* linear scan: 901 row checks -> ticket-901
   index lookup: 1 key lookup + 1 row fetch -> ticket-901 */
```

### Your first time: Your mission: observe a real index decision

- [ ] Create a table with enough representative rows — Tiny toy tables make sequential scans look unbeatable.
- [ ] Run a selective query before indexing — Capture EXPLAIN ANALYZE BUFFERS.
- [ ] Create one B-tree index and ANALYZE — Refresh statistics before comparing.
- [ ] Compare plan, rows, time, and buffers — Explain every changed node rather than celebrating the word Index.

You have evidence of a route change, not an index superstition.

- **The planner still uses Seq Scan.**
  Check table size, selectivity, statistics, predicate/operator compatibility, and the fraction of heap pages needed.
- **Index Only Scan still reports heap fetches.**
  The visibility map cannot prove every tuple visible; vacuum activity and recent writes affect heap visits.
- **A function-wrapped column misses the index.**
  Rewrite to an indexable predicate or create a matching expression index deliberately.

### Where to check

- `pg_indexes` and the exact index definition.
- `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` for chosen access path and I/O.
- Table statistics after `ANALYZE`.
- Predicate operators against the chosen index method/operator class.

### Worked example: the index the planner correctly ignored

1. A million tickets have only two status values, and 92 percent are `open`.
2. An index exists on `status`; a query asks for every open ticket and all columns.
3. Following hundreds of thousands of index entries into the heap would touch most pages randomly.
4. PostgreSQL chooses a sequential scan and reads the table once.
5. A selective `WHERE id = ...` query uses its B-tree, proving the planner is cost-based, not index-phobic.

**Quiz.** Why might PostgreSQL ignore a valid B-tree index for a predicate?

- [ ] Indexes work only after restart
- [x] The estimated cost of reading a large share through index and heap can exceed a sequential scan
- [ ] B-trees cannot test equality
- [ ] PostgreSQL never uses indexes automatically

*The planner compares estimated costs. Low selectivity and many heap visits can make sequential access cheaper.*

- **B-tree strength** — Equality, range, and ordered retrieval on sortable values.
- **Heap fetch** — Table-page visit for visibility or columns not available from the index.
- **Selectivity** — Fraction of rows expected to match; a central input to plan cost.

### Challenge

Benchmark one high-selectivity and one low-selectivity predicate on the same indexed column. Explain why the access paths differ using rows and buffers, not elapsed time alone.

### Ask the community

> PostgreSQL chooses `[scan]` for `[query]` with index `[definition]`. Estimated/actual rows and buffers are `[values]`. Is the plan rational, or are statistics/index design wrong?

Include the full plan and table scale; one node line is not a diagnosis.

- [PostgreSQL — Index types](https://www.postgresql.org/docs/current/indexes-types.html)
- [PostgreSQL — Index-only scans and covering indexes](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)

🎬 [Database Indexing Explained with PostgreSQL — Hussein Nasser](https://www.youtube.com/watch?v=-qNSXK7s7_w) (18 min)

- An index is a separate access structure maintained alongside the table.
- PostgreSQL B-tree supports common equality, range, and ordering work.
- Index scans often still fetch heap tuples for visibility or extra columns.
- Low-selectivity predicates can rationally favor sequential scans.
- Measure plan nodes, row estimates, and buffers before calling an index useful.


## Related notes

- [[Notes/relational-databases-engineer-level/indexes-and-performance/reading-explain-and-execution-plans|Reading EXPLAIN & execution plans]]
- [[Notes/relational-databases-engineer-level/indexes-and-performance/query-tuning-and-over-indexing-writes|Query tuning & over-indexing writes]]
- [[Notes/database/sql/select-basics|SELECT, JOIN & aggregate basics]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/indexes-and-performance/how-an-index-works.mdx`_
