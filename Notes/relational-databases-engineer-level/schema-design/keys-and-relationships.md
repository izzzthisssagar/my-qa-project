---
title: "Keys & relationships"
tags: ["relational-databases-engineer-level", "schema-design", "track-e"]
updated: "2026-07-17"
---

# Keys & relationships

*Choose stable candidate and primary keys, enforce alternate identities with UNIQUE, represent relationships with foreign keys, and test updates/deletes as integrity behavior.*

> A UUID does not make a relationship correct. It merely gives the wrong row a very professional-looking identifier.

> **In real life**
>
> A key identifies one lock; a key ring organizes several roles. Database keys identify rows, alternate identities, and references—each with a different job.

**key and relationship**: A candidate key is a minimal set of columns that uniquely identifies a row. One candidate is chosen as the primary key; other business identities can be UNIQUE. A foreign key requires referencing values to match a referenced primary/unique key, subject to declared action rules.

## Encode the rules in DDL

```sql
CREATE TABLE ticket (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  project_id bigint NOT NULL REFERENCES project(id) ON DELETE RESTRICT,
  external_key text NOT NULL,
  UNIQUE (project_id, external_key)
);
```

PostgreSQL primary keys imply uniqueness and `NOT NULL`. A foreign key must reference a primary key,
unique constraint, or eligible non-partial unique index. Index referencing columns separately when
workloads need efficient parent updates/deletes or child lookups; PostgreSQL does not create that
referencing-side index automatically.

> **Tip**
>
> Name constraints when failure diagnostics matter. `ticket_project_fk` says more than an auto-generated suffix during a migration incident.

> **Common mistake**
>
> Using `ON DELETE CASCADE` because cleanup tests become easy. Cascade encodes ownership semantics and can widen blast radius dramatically.

![A ring holding several distinct metal keys](keys-and-relationships.jpg)
*Key ring — Basile Morin, Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Key_ring.jpg)*
- **Primary key** — The chosen row identity.
- **Alternate key** — Another business identity protected by UNIQUE.
- **Foreign key** — A reference whose target and lifecycle action are enforced.

**Design and test a relationship**

1. **List candidate identities** — Find minimal stable unique sets.
2. **Choose primary key** — Prefer stable, non-null identity.
3. **Add foreign key** — Match types and referenced uniqueness.
4. **Choose actions** — RESTRICT, CASCADE, SET NULL, or defaults from ownership rules.
5. **Test invalid states** — Orphans, duplicate alternates, updates, and deletes.

*Run it — enforce a composite alternate key (Python)*

```python
tickets = [(10, "QA-1"), (10, "QA-2"), (11, "QA-1"), (10, "QA-1")]
seen = set()
for key in tickets:
    result = "ACCEPT" if key not in seen else "REJECT duplicate"
    print(key, result)
    seen.add(key)

# (10, 'QA-1') ACCEPT
# (10, 'QA-2') ACCEPT
# (11, 'QA-1') ACCEPT
# (10, 'QA-1') REJECT duplicate
```

*Run it — enforce a composite alternate key (Java)*

```java
import java.util.*;
public class Main {
  record Key(int project,String external){}
  public static void main(String[] args){
    List<Key> keys=List.of(new Key(10,"QA-1"),new Key(10,"QA-2"),new Key(11,"QA-1"),new Key(10,"QA-1"));
    Set<Key> seen=new HashSet<>();
    for(Key k:keys) System.out.println("("+k.project()+", '"+k.external()+"') "+(seen.add(k)?"ACCEPT":"REJECT duplicate"));
  }
}

/* (10, 'QA-1') ACCEPT
   (10, 'QA-2') ACCEPT
   (11, 'QA-1') ACCEPT
   (10, 'QA-1') REJECT duplicate */
```

### Your first time: Your mission: prove referential integrity

- [ ] List primary and alternate candidate keys — Justify stability and minimality.
- [ ] Add one named foreign key — Choose delete/update actions from lifecycle rules.
- [ ] Attempt orphan and duplicate inserts — Assert exact constraint failures.
- [ ] Test parent update and delete — Verify restrict, cascade, or null behavior plus row counts.

- **Foreign key cannot be created.**
  Check matching types and that referenced columns have primary/unique eligibility.
- **Parent delete is unexpectedly slow.**
  Inspect referencing-side indexes and child volume; PostgreSQL does not auto-index foreign-key columns.
- **Cascade removes too much.**
  Revisit ownership semantics and test the entire descendant row-count blast radius.

### Where to check

- `information_schema` or `\d` for actual constraints.
- Duplicate and orphan probes in a rollback-safe test transaction.
- Query plans for parent delete/update checks.

### Worked example: the business key the surrogate missed

Tickets use surrogate IDs, but imports create two `QA-1` tickets in the same project. Adding `UNIQUE(project_id, external_key)` captures the real business identity while allowing `QA-1` in another project.

**Quiz.** Does PostgreSQL automatically index the referencing columns of a foreign key?

- [ ] Always
- [x] No; add an index when access and parent-change workloads need it
- [ ] Only for text
- [ ] Foreign keys cannot be indexed

*The referenced key is unique/indexed, but PostgreSQL does not automatically create an index on the referencing columns.*

- **Candidate key** — A minimal column set that uniquely identifies a row.
- **Primary key** — The chosen candidate key; unique and not null.
- **Alternate key** — Another candidate identity usually enforced with UNIQUE.
- **Foreign key action** — Declared behavior when referenced rows update or delete.

### Challenge

Model project-ticket identity with surrogate and business keys, then test orphan, duplicate, restrict, and cascade cases.

### Ask the community

> My foreign key `[name]` rejects/allows `[operation]`; here are DDL and expected ownership rules.

Include both table definitions and sanitized constraint error.

- [PostgreSQL — primary, unique, and foreign-key constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL — identity columns](https://www.postgresql.org/docs/current/ddl-identity-columns.html)

🎬 [freeCodeCamp — database design course](https://www.youtube.com/watch?v=ztHopE5Wnpc) (487 min)

- Candidate keys capture minimal row identities; one becomes primary and alternates remain constrained.
- Foreign keys enforce references only to eligible unique targets.
- Delete/update actions encode ownership and must be tested for blast radius.
- Index referencing columns according to workload; PostgreSQL does not add that index automatically.


## Related notes

- [[Notes/relational-databases-engineer-level/schema-design/er-modeling-from-requirements|ER modeling from requirements]]
- [[Notes/relational-databases-engineer-level/schema-design/normalization-1nf-to-3nf|Normalization: 1NF to 3NF]]
- [[Notes/relational-databases-engineer-level/sql-mastery/set-operators|Set operators]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/schema-design/keys-and-relationships.mdx`_
