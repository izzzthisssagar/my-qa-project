---
title: "Clustered vs non-clustered"
tags: ["relational-databases-engineer-level", "indexes-and-performance", "track-e"]
updated: "2026-07-17"
---

# Clustered vs non-clustered

*Clustered-index vocabulary is vendor-specific. Learn the general physical-order idea, PostgreSQL's one-time CLUSTER operation, and how to test locality without importing SQL Server rules.*

> "The primary key is always clustered" is not database knowledge; it is one vendor's accent spoken loudly in the wrong airport.

> **In real life**
>
> Books physically shelved by call number have locality; a separate author catalogue points into those shelves. Some engines maintain table organization through one clustered index. PostgreSQL instead keeps heap tables and can reorder one with `CLUSTER`, but later writes do not preserve that ordering.

**table clustering**: Clustering describes physical locality of table rows according to an index key, but implementation and terminology vary by database. PostgreSQL's CLUSTER command physically rewrites a heap table using an existing index as a one-time operation; it remembers the index but does not automatically keep subsequent inserts or updates clustered.

## Separate the portable idea from vendor behavior

- Physical locality can reduce page reads for range queries returning nearby keys.
- A conventional secondary/non-clustered index is a separate structure pointing toward table rows.
- Some vendors organize table storage by one clustered index and maintain it with writes.
- PostgreSQL heap tables can have many indexes; none automatically becomes a maintained clustered index.
- PostgreSQL `CLUSTER table USING index` takes a strong table lock and must be rerun to restore order after drift.

> **Tip**
>
> Name the engine and version whenever teaching clustered indexes. Then verify physical locality with workload evidence rather than inferring it from a primary-key declaration.

> **Common mistake**
>
> Porting SQL Server's "one clustered index whose leaf level is the table" model directly into PostgreSQL. PostgreSQL's `CLUSTER` command is a rewrite, not a continuously maintained storage identity.

![Tall library shelves arranged in physical aisles full of ordered books](clustered-vs-non-clustered.jpg)
*Bookshelves at the library — Westcott Phillip, Wikimedia Commons, public domain. [Source](https://commons.wikimedia.org/wiki/File:Bookshelves_at_the_library.jpg)*
- **Physical shelf order** — Nearby call numbers occupy nearby shelves, the locality benefit clustering seeks.
- **Aisle route** — A range read can continue through nearby pages instead of jumping across storage.
- **Order drifts with returns** — PostgreSQL does not automatically recluster new and updated rows after CLUSTER.

**PostgreSQL clustering lifecycle**

1. **Choose an existing index** — The index defines the requested physical row order.
2. **CLUSTER rewrites the heap** — PostgreSQL physically reorders the table under an ACCESS EXCLUSIVE lock.
3. **Range locality improves** — Rows with nearby indexed values are likely on nearby pages.
4. **Normal writes resume** — New and updated tuples are not automatically placed in perfect index order.
5. **Measure drift and recluster if justified** — Operational cost and workload benefit decide whether to repeat it.

*Run it — count page jumps before and after clustering (Python)*

```python
physical_rows = [30, 80, 10, 40, 90, 50, 100, 60, 20, 70]
page_of_position = lambda position: position // 2

def page_jumps(rows, low, high):
    pages = [page_of_position(i) for i, key in enumerate(rows) if low <= key <= high]
    return pages, sum(a != b for a, b in zip(pages, pages[1:]))

before_pages, before_jumps = page_jumps(physical_rows, 30, 70)
clustered = sorted(physical_rows)
after_pages, after_jumps = page_jumps(clustered, 30, 70)
print(f"before: pages {before_pages}, jumps {before_jumps}")
print(f"after:  pages {after_pages}, jumps {after_jumps}")

# before: pages [0, 1, 2, 3, 4], jumps 4
# after:  pages [1, 1, 2, 2, 3], jumps 2
```

*Run it — show clustering drift after inserts (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    List<Integer> heap = new ArrayList<>(List.of(10, 20, 30, 40, 50));
    System.out.println("after CLUSTER: " + heap);
    heap.add(15); heap.add(35);
    System.out.println("after later inserts: " + heap);
    List<Integer> reclustered = new ArrayList<>(heap); Collections.sort(reclustered);
    System.out.println("after recluster: " + reclustered);
  }
}
/* after CLUSTER: [10, 20, 30, 40, 50]
   after later inserts: [10, 20, 30, 40, 50, 15, 35]
   after recluster: [10, 15, 20, 30, 35, 40, 50] */
```

### Your first time: Your mission: test locality, not vocabulary

- [ ] Choose a range-heavy table and index — Document why nearby keys should be read together.
- [ ] Capture EXPLAIN ANALYZE BUFFERS before CLUSTER — Use a representative range and returned columns.
- [ ] Run CLUSTER in a safe test environment — Record lock and rewrite cost.
- [ ] Repeat after writes — Demonstrate benefit and later physical-order drift.

You have separated locality evidence from vendor folklore.

- **CLUSTER blocks application traffic.**
  It takes ACCESS EXCLUSIVE on the table; schedule maintenance or choose a different operational approach.
- **Performance benefit fades after heavy writes.**
  PostgreSQL does not maintain clustering; measure correlation/drift and recluster only when benefit exceeds rewrite cost.
- **A primary key table is assumed physically ordered.**
  Inspect engine behavior and physical correlation; a PostgreSQL primary key creates uniqueness/indexing, not maintained heap order.

### Where to check

- PostgreSQL `CLUSTER` documentation and lock requirements.
- `pg_stats.correlation` as one clue about physical order.
- Range-query buffers before and after clustering.
- Vendor documentation before transferring clustered-index rules.

### Worked example: the SQL Server rule that broke a PostgreSQL capacity plan

1. A team assumes PostgreSQL's primary key physically organizes a 500 GB event table.
2. Range scans grow increasingly random as inserts arrive by a different key.
3. The primary-key index is healthy; the heap was never maintained in that order.
4. A controlled `CLUSTER ... USING ...` improves locality temporarily but requires a large rewrite and exclusive lock.
5. The team redesigns partitioning/maintenance around PostgreSQL reality instead of a borrowed term.

**Quiz.** What does PostgreSQL guarantee after CLUSTER table USING index?

- [ ] All future writes remain in index order
- [x] The table is physically reordered once; later writes are not automatically clustered
- [ ] The index leaf pages become the table
- [ ] Every query must use that index

*The official command documentation explicitly calls clustering a one-time operation and says later changes are not clustered.*

- **Portable clustering idea** — Physical locality by a key can reduce page reads for range access.
- **PostgreSQL CLUSTER** — One-time heap rewrite based on an index, not maintained on later writes.
- **Vendor warning** — Clustered-index storage semantics differ; always name the engine.

### Challenge

Write a three-column comparison for PostgreSQL, SQL Server, and one other engine: table organization, maintained ordering, and operational rebuild/recluster behavior. Cite each vendor's docs.

### Ask the community

> On PostgreSQL `[version]`, range query `[plan]` changed after CLUSTER by `[buffers/time]` and drifted after `[writes]`. Is periodic reclustering justified?

Include rewrite size, lock budget, and workload frequency—not just the fastest run.

- [PostgreSQL — CLUSTER](https://www.postgresql.org/docs/current/sql-cluster.html)
- [PostgreSQL — Indexes and ORDER BY](https://www.postgresql.org/docs/current/indexes-ordering.html)

🎬 [Database Indexing Explained with PostgreSQL — Hussein Nasser](https://www.youtube.com/watch?v=-qNSXK7s7_w) (18 min)

- Clustered-index terminology and storage behavior are vendor-specific.
- PostgreSQL stores ordinary tables as heaps with separate indexes.
- PostgreSQL CLUSTER is a one-time physical rewrite and later writes drift.
- Locality can improve range I/O but must justify rewrite and locking cost.
- Never infer PostgreSQL physical order from a primary-key declaration.


## Related notes

- [[Notes/relational-databases-engineer-level/indexes-and-performance/how-an-index-works|How an index works]]
- [[Notes/relational-databases-engineer-level/indexes-and-performance/reading-explain-and-execution-plans|Reading EXPLAIN & execution plans]]
- [[Notes/relational-databases-engineer-level/schema-design/keys-and-relationships|Keys & relationships]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/indexes-and-performance/clustered-vs-non-clustered.mdx`_
