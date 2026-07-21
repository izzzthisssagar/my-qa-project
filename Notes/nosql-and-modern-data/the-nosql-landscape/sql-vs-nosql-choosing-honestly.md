---
title: "SQL vs NoSQL: choosing honestly"
tags: ["sql", "nosql", "architecture", "tradeoffs", "track-d"]
updated: "2026-07-17"
---

# SQL vs NoSQL: choosing honestly

*Replace database tribalism with a testable decision built from invariants, access patterns, operational limits, and the cost of change.*

> “SQL or NoSQL?” is usually asked one level too early. The product does not care which camp wins. It
> cares whether a payment is charged once, a catalog loads quickly, an audit survives, and an operator
> can recover the system at 3 a.m. A useful choice turns those needs into evidence.

> **In real life**
>
> Choosing a database from a feature checklist is like choosing transport from the number of buttons on
> the dashboard. First ask what must be carried, over what terrain, under which rules, and who repairs it.

**polyglot persistence**: Polyglot persistence is the deliberate use of more than one data-store model in a system, assigning each bounded workload to a suitable store while accepting the extra synchronization, operations, security, and testing cost.

## Begin with invariants, not labels

Relational databases are strong defaults when relationships, constraints, multi-row transactions, and
ad hoc querying matter. NoSQL models can be strong when one aggregate dominates, relationships are
traversed as data, keys drive every lookup, or partitions must scale predictably. Neither sentence is a
verdict. Modern products overlap, and operational maturity can outweigh a theoretical advantage.

Ask five questions:

1. Which facts must remain true after every accepted write?
2. What are the top reads and their latency budgets?
3. Which queries are unknown today but likely tomorrow?
4. What volume, distribution, and failure modes are credible—not imaginary?
5. Can the team operate, secure, back up, restore, and migrate this engine?

> **Tip**
>
> Write a decision record with measurable assumptions: peak writes, record size, required consistency,
> recovery objectives, and expected query shapes. Add a date to revisit them.

> **Common mistake**
>
> Choosing NoSQL “for scale” before measuring the workload, or choosing SQL “for safety” while keeping
> critical invariants only in application code. A label does not implement the property you need.

![A simple network graph with a central node connected to surrounding nodes](sql-vs-nosql-choosing-honestly.png)
*Network Graph — Graphpedia, CC0 1.0. [Source](https://commons.wikimedia.org/wiki/File:Network-Graph.svg)*
- **The workload** — Keep the product's invariants and dominant access patterns at the center of the decision.
- **Data model** — Relationships, aggregates, keys, and partitions determine which operations are natural.
- **Operations** — Backup, restore, observability, upgrades, and team skill are part of correctness.
- **Failure behavior** — Decide what reads and writes may do during partitions, lag, and partial outages.
- **Change cost** — Migration and synchronization costs can dominate a small performance advantage.

**An honest database decision**

1. **State invariants** — Write the business truths that no accepted operation may violate.
2. **Measure access** — Capture read/write shapes, latency targets, data size, and credible growth.
3. **Shortlist models** — Compare relational and relevant NoSQL families against the same workload.
4. **Prototype the hardest path** — Exercise the risky transaction, traversal, partition, migration, or query.
5. **Test failure and recovery** — Include replica lag, unavailable nodes, backup restore, and operator response.
6. **Record the trade** — Document why the winner fits and which weakness the design must contain.

*Run it — score a decision transparently (Python)*

```python
``weights = {"transactions": 5, "ad_hoc_queries": 3, "key_lookup_scale": 2, "team_skill": 4}
sql = {"transactions": 5, "ad_hoc_queries": 5, "key_lookup_scale": 3, "team_skill": 5}
nosql = {"transactions": 3, "ad_hoc_queries": 2, "key_lookup_scale": 5, "team_skill": 2}

def score(candidate):
    return sum(weights[k] * candidate[k] for k in weights)

print("SQL:", score(sql))
print("NoSQL:", score(nosql))
assert score(sql) > score(nosql)  # true for this workload, not universally``
```

*Run it — score a decision transparently (Java)*

```java
``import java.util.*;

public class Main {
    static int score(Map<String,Integer> weights, Map<String,Integer> values) {
        return weights.entrySet().stream().mapToInt(e -> e.getValue() * values.get(e.getKey())).sum();
    }
    public static void main(String[] args) {
        var w = Map.of("transactions",5, "queries",3, "keyScale",2, "team",4);
        var sql = Map.of("transactions",5, "queries",5, "keyScale",3, "team",5);
        var nosql = Map.of("transactions",3, "queries",2, "keyScale",5, "team",2);
        System.out.println("SQL: " + score(w, sql));
        System.out.println("NoSQL: " + score(w, nosql));
        if (score(w, sql) <= score(w, nosql)) throw new AssertionError();
    }
}``
```

### Your first time: Your mission: write a one-page database decision

- [ ] List three invariants — Use testable language: an order total equals its lines; a payment reference is unique.
- [ ] Rank five access patterns — Include frequency, latency target, result size, and whether the query is known in advance.
- [ ] Compare two candidates — Score the same criteria and attach evidence or a prototype result to every important score.
- [ ] Name the exit plan — Record export format, migration boundary, and the signal that would force reconsideration.

You now have an auditable hypothesis rather than a technology allegiance.

- **The chosen store is fast, but reporting needs become painful.**
  Revisit the ad hoc query requirement; add a governed analytical copy rather than forcing every workload into one model.
- **Two databases disagree about the same entity.**
  Declare one system of record, trace the change event, and test replay, duplication, ordering, and repair.
- **A managed service outage reveals no tested restore path.**
  Treat backup and restore as product behavior; run recovery drills against measured objectives.
- **The prototype passed but production hotspots appear.**
  Compare real key distribution and query mix with the prototype assumptions; averages hide skew.

### Where to check

- **Decision record assumptions** — compare forecasts with production telemetry.
- **Constraint location** — database, application, event consumer, or nowhere.
- **System-of-record ownership** — one fact should have an explicit authority.
- **Restore evidence** — a backup that has never restored is an untested artifact.
- **Operational ownership** — on-call skill and vendor limits affect the real design.

### Worked example: a catalog that did not need a fashionable rewrite

1. A team proposes moving a modest catalog from PostgreSQL to a document store “for scale.”
2. Measurements show 40 reads per second, frequent support queries, and strong team SQL skill.
3. The real latency problem is an unindexed filter plus repeated image calls.
4. An index and CDN fix the target without migration, dual writes, or a new recovery procedure.
5. The decision record keeps the document option open if product attributes later demand aggregate reads.

**Quiz.** What is the strongest reason to choose a database model?

- [ ] It appears most often in job advertisements
- [ ] It wins a synthetic benchmark unrelated to the product
- [x] Evidence shows it meets the workload's invariants, access patterns, failure needs, and operating constraints with acceptable trade-offs
- [ ] The team has not used it before

*A defensible choice binds evidence to the actual workload and includes operations and failure behavior. Popularity and isolated benchmarks do not establish fitness.*

- **Best first database question** — Which facts must remain true after every accepted write?
- **Polyglot persistence** — Using multiple store models deliberately, while accepting synchronization and operational cost.
- **Why prototype the hardest path?** — Easy CRUD hides the transaction, traversal, partition, or migration that may invalidate the design.
- **What should a decision record contain?** — Measured assumptions, alternatives, evidence, trade-offs, owner, and revisit trigger.
- **Why is team skill architectural?** — Correct operation, recovery, security, and diagnosis depend on people, not only engine features.

### Challenge

Find a database claim in your project that contains “always,” “never,” or “scales.” Replace it with a
measurement, a guarantee from documentation, and a failure test. Record what remains uncertain.

### Ask the community

> We need to preserve [invariants] while serving [access patterns] at [measured load]. Candidate A trades [cost] for [benefit]; candidate B trades [cost] for [benefit]. Which assumption would you test first?

Share the decision constraints, not only the product names. Useful answers require the workload.

- [MongoDB — NoSQL vs SQL](https://www.mongodb.com/resources/basics/databases/nosql-explained/nosql-vs-sql)
- [PostgreSQL — Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [Redis Docs — Data types](https://redis.io/docs/latest/develop/data-types/)

🎬 [SQL vs. NoSQL: What's the difference? — IBM Technology](https://www.youtube.com/watch?v=Q5aTUc7c4jg) (6 min)

- Start with business invariants and access patterns, not SQL-versus-NoSQL identity.
- Operational maturity, recovery, and team skill are part of database correctness.
- Prototype the path most likely to invalidate the choice.
- Multiple stores add synchronization and ownership bugs; use them deliberately.
- Record assumptions and revisit triggers so a good decision can change when evidence changes.


## Related notes

- [[Notes/nosql-and-modern-data/the-nosql-landscape/document-key-value-graph-columnar|Document, key-value, graph & columnar]]
- [[Notes/nosql-and-modern-data/the-nosql-landscape/where-each-shines|Where each shines]]
- [[Notes/relational-databases-engineer-level/transactions-and-concurrency/acid-properly|ACID, properly]]


---
_Source: `packages/curriculum/content/notes/nosql-and-modern-data/the-nosql-landscape/sql-vs-nosql-choosing-honestly.mdx`_
