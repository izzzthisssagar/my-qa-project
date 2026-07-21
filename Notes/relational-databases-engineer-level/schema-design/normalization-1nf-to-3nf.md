---
title: "Normalization: 1NF to 3NF"
tags: ["relational-databases-engineer-level", "schema-design", "track-e"]
updated: "2026-07-17"
---

# Normalization: 1NF to 3NF

*Normalize from atomic rows through whole-key and non-transitive dependencies to prevent insert, update, and delete anomalies—then verify decompositions preserve facts and constraints.*

> Repeating the customer's email on every order is convenient until one customer has six current email addresses depending on which row your query accidentally reads.

> **In real life**
>
> A card catalogue stores one fact in its proper drawer and references it by a stable label. Normalization stops facts from being recopied across every card that mentions them.

**normalization**: Normalization decomposes relations according to functional dependencies. In the practical 1NF-to-3NF progression: values are atomic with no repeating groups; non-key attributes depend on the whole candidate key; and non-key attributes do not depend transitively on other non-key attributes.

## Follow dependencies, not slogans

An order-line table keyed by `(order_id, product_id)` should not store `product_name` (depends only on
`product_id`) or `customer_email` (depends on `order_id` through customer). Split facts into tables
where their determinant is a key, then enforce relationships.

> **Tip**
>
> Write functional dependencies explicitly: `product_id -> product_name`. They reveal the correct owner of each fact.

> **Common mistake**
>
> Believing a surrogate primary key makes any table 3NF. Dependencies among business attributes still exist after adding `id`.

![Rows of labeled wooden card catalogue drawers](normalization-1nf-to-3nf.jpg)
*Card catalogue drawers — Carolina Prysyazhnyuk, Wikimedia Commons, CC BY-SA 2.0. [Source](https://commons.wikimedia.org/wiki/File:Card_catalogue_drawers.jpg)*
- **1NF** — One atomic value per attribute and no repeating groups.
- **2NF** — Every non-key fact depends on the whole candidate key.
- **3NF** — Non-key facts do not depend transitively on other non-key facts.

**Decompose a risky table**

1. **List candidate keys** — Normalization depends on all candidate keys, not merely one ID.
2. **Write dependencies** — State which attributes determine which facts.
3. **Remove repeating groups** — Reach atomic relational values.
4. **Remove partial dependencies** — Move facts dependent on part of a composite key.
5. **Remove transitive dependencies** — Move facts owned by another non-key determinant.

*Run it — expose an update anomaly (Python)*

```python
rows = [(1, "a@example.test"), (2, "a@example.test"), (3, "a@example.test")]
rows[0] = (1, "new@example.test")
emails = sorted({email for _, email in rows})
print("emails after one-row update:", emails)
print("anomaly:", len(emails) > 1)

# emails after one-row update: ['a@example.test', 'new@example.test']
# anomaly: True
```

*Run it — expose an update anomaly (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args){
    List<String> emails=new ArrayList<>(List.of("a@example.test","a@example.test","a@example.test"));
    emails.set(0,"new@example.test");
    Set<String> unique=new TreeSet<>(emails);
    System.out.println("emails after one-row update: "+unique);
    System.out.println("anomaly: "+(unique.size()>1));
  }
}

/* emails after one-row update: [a@example.test, new@example.test]
   anomaly: true */
```

### Your first time: Your mission: normalize one import table

- [ ] Identify all candidate keys — Do not let a synthetic ID erase business dependencies.
- [ ] Write functional dependencies — Use determinant arrows for every non-key fact.
- [ ] Decompose through 1NF, 2NF, and 3NF — Name the anomaly each split prevents.
- [ ] Test lossless reconstruction — Join fixed data and compare facts/counts with the original.

- **Join after decomposition multiplies rows.**
  A relationship key or uniqueness constraint is missing; prove cardinality before trusting reconstruction.
- **A fact still has two possible owners.**
  Revisit candidate keys and functional dependencies with concrete counterexamples.
- **Too many joins appear in one read path.**
  Measure first; normalization correctness and read optimization are separate decisions.

### Where to check

- Candidate keys and written functional dependencies.
- Insert, update, and delete anomaly examples.
- Bidirectional fact comparisons after decomposition and reconstruction.

### Worked example: customer email stops disagreeing with itself

Three order rows duplicate one customer email. Updating one creates conflicting truth. Moving email to `customer(customer_id, email)` leaves orders referencing one owner, so one update changes the fact exactly once.

**Quiz.** Does adding a surrogate id automatically put a table in 3NF?

- [ ] Yes
- [x] No; business dependencies among other attributes remain
- [ ] Only in PostgreSQL
- [ ] Only for small tables

*Normal forms concern functional dependencies across candidate keys and attributes, not the mere presence of a generated identifier.*

- **1NF** — Atomic attributes and no repeating groups within a relation.
- **2NF** — In 1NF, with no non-key fact dependent on only part of a candidate key.
- **3NF** — In 2NF, without non-key facts transitively determined by other non-key facts.
- **Update anomaly** — One logical fact has multiple copies that can disagree.

### Challenge

Normalize an order-import table to 3NF and prove no facts are lost or multiplied by reconstruction joins.

### Ask the community

> I believe `[attribute]` belongs in `[table]` because `[dependency]`; here are candidate keys and counterexample rows.

Discuss dependencies, not preferred table names.

- [PostgreSQL — constraints for normalized schemas](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL — relational table basics](https://www.postgresql.org/docs/current/ddl-basics.html)

🎬 [Decomplexify — database normalization from 1NF onward](https://www.youtube.com/watch?v=GFQaEYEc8_8) (29 min)

- Normalization follows candidate keys and functional dependencies.
- 1NF removes repeating groups; 2NF removes partial dependencies; 3NF removes transitive non-key dependencies.
- Surrogate IDs do not erase business dependencies.
- Verify decompositions for constraints, lossless reconstruction, and anomaly prevention.


## Related notes

- [[Notes/relational-databases-engineer-level/schema-design/keys-and-relationships|Keys & relationships]]
- [[Notes/relational-databases-engineer-level/schema-design/when-to-denormalize|When to denormalize]]
- [[Notes/relational-databases-engineer-level/schema-design/er-modeling-from-requirements|ER modeling from requirements]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/schema-design/normalization-1nf-to-3nf.mdx`_
