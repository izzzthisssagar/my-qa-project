---
title: "Document, key-value, graph, and columnar databases"
tags: ["nosql", "data-modeling", "databases", "testing", "track-d"]
updated: "2026-07-17"
---

# Document, key-value, graph, and columnar databases

*Learn the four NoSQL families by the questions they answer, the shapes they preserve, and the bugs testers should expect when data stops looking like rows.*

> “NoSQL” tells you what a database is not. It does not tell you whether a value lives behind one key,
> inside a JSON-like document, along an edge, or across a wide sparse row. Treating those designs as
> interchangeable is how teams test the API response and miss the data-model failure underneath it.

> **In real life**
>
> A filing cabinet, a coat-check ticket, a route map, and a laboratory spreadsheet all store facts, but
> they retrieve them differently. Documents keep related papers together; key-value stores exchange one
> ticket for one item; graphs follow connections; wide-column stores scan selected measurements at scale.

**NoSQL database**: NoSQL is an umbrella term for non-relational database models designed around access patterns such as retrieving a whole aggregate, looking up a value by key, traversing relationships, or scanning sparse columns. The label does not imply one query language, one consistency model, or an absence of schema.

## Four families, four native questions

| Family | Native shape | Natural question | Typical tester risk |
|---|---|---|---|
| Document | nested fields and arrays in a document | “Give me this order with its lines” | old and new document shapes coexist |
| Key-value | opaque value addressed by a unique key | “What value belongs to this session key?” | expiry, collision, or stale replacement |
| Graph | nodes connected by typed relationships | “How is A connected to B?” | missing, duplicated, or wrongly directed edge |
| Wide-column | rows with flexible, grouped columns | “Read these measurements for this partition” | poor partition key or incomplete range |

These are dominant abstractions, not prison walls. A product may add indexes, JSON support, search,
transactions, or graph-like features. Test the guarantees of the selected engine and configuration—not
the stereotype attached to its category.

> **Tip**
>
> Start data tests from access paths. Write the three most important reads and writes, then ask which
> model makes them direct. The shape of the API alone can hide fan-out queries, duplicated facts, and
> expensive traversals.

> **Common mistake**
>
> Saying “NoSQL has no schema.” The schema still exists in producers, validators, indexes, consumers,
> and migration logic. Flexible enforcement means testers must discover mixed shapes deliberately.

![Four metal filing-cabinet drawers with different handles and label slots](document-key-value-graph-columnar.jpg)
*Filing Cabinets — MarkBuckawicki, CC0 1.0. [Source](https://commons.wikimedia.org/wiki/File:Filing_Cabinets.jpg)*
- **Document drawer** — One drawer can hold a complete aggregate with nested fields, but older drawers may use a different internal layout.
- **Key-value handle** — A precise key retrieves a value quickly; without the key, discovery may be intentionally limited.
- **Graph label** — A label is useful only with links to other labels—the relationships are first-class data.
- **Wide-column slots** — Rows may expose different columns, optimized around partitions and ordered scans rather than joins.

**Classify a storage problem by its dominant access path**

1. **Name the decision** — Describe the read or write the product must perform, including latency and scale.
2. **Expose the data shape** — Identify aggregates, independent values, relationships, and sparse time-ordered facts.
3. **Choose a native model** — Prefer the model that answers the dominant question without repeated joins or duplication gymnastics.
4. **Record sacrificed queries** — List queries that become awkward, slower, or application-managed.
5. **Test real guarantees** — Verify validation, atomicity, ordering, expiry, indexes, and consistency in the actual engine.

*Run it — classify access patterns (Python)*

```python
``cases = {
    "load one shopping cart": "key-value",
    "load product with variable attributes": "document",
    "find friends-of-friends": "graph",
    "scan sensor values by device and hour": "wide-column",
}
for question, family in cases.items():
    print(f"{question:42} -> {family}")

assert cases["find friends-of-friends"] == "graph"``
```

*Run it — classify access patterns (Java)*

```java
``import java.util.*;

public class Main {
    public static void main(String[] args) {
        var cases = new LinkedHashMap<String, String>();
        cases.put("load one shopping cart", "key-value");
        cases.put("load product with variable attributes", "document");
        cases.put("find friends-of-friends", "graph");
        cases.put("scan sensor values by device and hour", "wide-column");
        cases.forEach((question, family) ->
            System.out.printf("%-42s -> %s%n", question, family));
        if (!cases.get("find friends-of-friends").equals("graph")) throw new AssertionError();
    }
}``
```

### Your first time: Your mission: classify one feature without naming a product

- [ ] Write its two dominant reads — Use concrete questions such as load cart by customer ID or traverse dependencies three levels deep.
- [ ] Write its most dangerous update — Mark which facts must change atomically and which can lag.
- [ ] Sketch the native shape — Draw a document, key/value pair, graph, or partitioned row before discussing vendors.
- [ ] Name one awkward query — A credible choice includes what the model makes harder, not only what it accelerates.

You now have a model decision a tester can challenge instead of a product-name preference.

- **New records work, but records created before a release fail.**
  Sample historical shapes and verify readers tolerate or migrate every supported version.
- **A graph traversal returns duplicates or cycles forever.**
  Check edge direction, uniqueness, depth limits, and visited-node handling.
- **A key lookup intermittently returns nothing.**
  Inspect key construction, namespace collisions, TTL, eviction, and replica consistency.
- **A range query slows sharply as volume grows.**
  Inspect partition-key distribution and whether the query crosses many partitions.

### Where to check

- **Stored records, not only DTOs** — sample missing, extra, null, and old-version fields.
- **Key construction** — include tenant, environment, case normalization, and separators.
- **Relationship direction and type** — `OWNS` and `OWNED_BY` are not automatically equivalent.
- **Partition distribution** — one hot customer or date can defeat horizontal scale.
- **Documented guarantees** — atomicity and consistency scope differ by engine and operation.

### Worked example: a recommendation test that passed while the graph was wrong

1. The API returns three recommended accounts, and the UI test checks only the count.
2. An import creates `FOLLOWS` edges in the opposite direction for one tenant.
3. The traversal still finds three nodes, but they are followers rather than followed accounts.
4. A graph-aware test asserts edge direction, path depth, tenant boundary, and uniqueness.
5. The defect becomes a data relationship failure instead of a vague recommendation complaint.

**Quiz.** Which statement is safest?

- [ ] Every NoSQL database stores JSON documents
- [ ] NoSQL databases do not have schemas
- [x] The database family suggests a native access pattern, but the engine's documented guarantees still decide the tests
- [ ] Graph databases make every query faster

*A family is a useful model, not a universal contract. Features and guarantees vary by engine, version, and configuration, so tests must target the deployed behavior.*

- **Document database** — Stores an aggregate as a nested document; test mixed shapes, validation, and atomic update scope.
- **Key-value database** — Retrieves a value by key; test key construction, expiry, collision, and replacement.
- **Graph database** — Stores nodes and relationships as first-class data; test direction, type, depth, cycles, and boundaries.
- **Wide-column database** — Organizes sparse columns around partitioned rows; test partition distribution and range access.
- **Does flexible schema mean no schema?** — No. The contract moves into validators, code, indexes, consumers, and migrations.

### Challenge

Take one feature currently backed by a relational table. Model its dominant read in all four NoSQL
families. For each, state one test that becomes easier and one new failure mode you introduce.

### Ask the community

> Our feature reads [question] and atomically updates [facts]. We are considering [family] because [reason]. The awkward query is [query]. Which failure mode should we prototype first?

Include access frequency, data volume, consistency need, and expected partition key. “It scales” is not
enough information to evaluate a model.

- [MongoDB Manual — Data modeling](https://www.mongodb.com/docs/manual/data-modeling/)
- [Redis Docs — Data types](https://redis.io/docs/latest/develop/data-types/)
- [Neo4j — What is a graph database?](https://neo4j.com/docs/getting-started/graph-database/)

🎬 [MongoDB Explained in 10 Minutes — MongoDB](https://www.youtube.com/watch?v=GV9VBwH_h1U) (9 min)

- NoSQL names a landscape, not one database behavior.
- Document, key-value, graph, and wide-column models optimize different native questions.
- Flexible enforcement increases the need to test mixed historical shapes.
- Access patterns and atomicity needs should lead the model decision.
- Category knowledge never replaces the deployed engine's documented guarantees.


## Related notes

- [[Notes/nosql-and-modern-data/the-nosql-landscape/sql-vs-nosql-choosing-honestly|SQL vs NoSQL: choosing honestly]]
- [[Notes/nosql-and-modern-data/the-nosql-landscape/where-each-shines|Where each shines]]
- [[Notes/relational-databases-engineer-level/schema-design/when-to-denormalize|When to denormalize]]


---
_Source: `packages/curriculum/content/notes/nosql-and-modern-data/the-nosql-landscape/document-key-value-graph-columnar.mdx`_
