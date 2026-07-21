---
title: "Set operators"
tags: ["relational-databases-engineer-level", "sql-mastery", "track-e"]
updated: "2026-07-17"
---

# Set operators

*UNION, INTERSECT, and EXCEPT combine compatible query results; DISTINCT semantics, ALL variants, precedence, and final ordering decide whether your comparison is evidence or accidental data loss.*

> `UNION` is not “append.” It quietly removes duplicates, which is charming until duplicates are the bug you were hired to find.

> **In real life**
>
> Two fruit baskets can be poured together, compared for shared fruit, or subtracted. Whether identical apples remain repeated is the difference between default operators and `ALL`.

**set operator**: SQL set operators combine union-compatible query outputs: UNION returns rows from either input, INTERSECT rows in both, and EXCEPT rows in the left input but not the right. Without ALL, duplicates are eliminated.

## Compatibility, duplicates, precedence

```sql
SELECT id FROM source_a
EXCEPT
SELECT id FROM source_b;
```

Inputs need the same column count and compatible corresponding types. `INTERSECT` binds more tightly
than `UNION` and `EXCEPT`; the latter associate left-to-right. Parenthesize mixed operators so a
reviewer need not remember a precedence table during an outage.

> **Tip**
>
> Use `EXCEPT` in migration verification in both directions: old-minus-new and new-minus-old.

> **Common mistake**
>
> Applying `ORDER BY` to an unparenthesized branch and believing it sorts that branch. A trailing order normally applies to the combined result.

![Several baskets containing overlapping varieties of fruit](set-operators.jpg)
*Fruit baskets — Pixel.la Free Stock Photos, Wikimedia Commons, CC0. [Source](https://commons.wikimedia.org/wiki/File:Fruit_baskets.jpg)*
- **Left set** — Rows produced by the first compatible query.
- **Overlap** — Rows visible to INTERSECT.
- **Right set** — Rows added by UNION or removed by EXCEPT.

**Compare two data populations**

1. **Align columns** — Same count, order, and compatible types.
2. **Choose relationship** — Either, both, or left-only.
3. **Choose duplicate policy** — Default distinct or explicit ALL.
4. **Parenthesize and order** — Make evaluation and final presentation explicit.

*Run it — union, intersection, difference (Python)*

```python
left = [1, 1, 2, 3]
right = [2, 3, 4]
print("UNION", sorted(set(left) | set(right)))
print("INTERSECT", sorted(set(left) & set(right)))
print("EXCEPT", sorted(set(left) - set(right)))
print("UNION ALL", left + right)

# UNION [1, 2, 3, 4]
# INTERSECT [2, 3]
# EXCEPT [1]
# UNION ALL [1, 1, 2, 3, 2, 3, 4]
```

*Run it — union, intersection, difference (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args){
    List<Integer> left=List.of(1,1,2,3), right=List.of(2,3,4);
    Set<Integer> union=new TreeSet<>(left); union.addAll(right);
    Set<Integer> both=new TreeSet<>(left); both.retainAll(right);
    Set<Integer> diff=new TreeSet<>(left); diff.removeAll(right);
    List<Integer> all=new ArrayList<>(left); all.addAll(right);
    System.out.println("UNION "+union); System.out.println("INTERSECT "+both); System.out.println("EXCEPT "+diff); System.out.println("UNION ALL "+all);
  }
}

/* UNION [1, 2, 3, 4]
   INTERSECT [2, 3]
   EXCEPT [1]
   UNION ALL [1, 1, 2, 3, 2, 3, 4] */
```

### Your first time: Your mission: reconcile two sources

- [ ] Select the same key shape from old and new tables — Cast deliberately where types differ.
- [ ] Run EXCEPT in both directions — One direction cannot detect unexpected additions.
- [ ] Compare UNION with UNION ALL counts — Expose duplicate assumptions.
- [ ] Parenthesize mixed operators — Then add one final ORDER BY for deterministic evidence.

- **Queries are not union compatible.**
  Align column count/order and cast corresponding types intentionally.
- **Duplicate bug disappears.**
  Use ALL or separate GROUP BY/HAVING duplicate checks instead of default distinct semantics.
- **Mixed operator result is surprising.**
  Remember INTERSECT binds tighter; add parentheses that encode the intended logic.

### Where to check

- Column order and types on both branches.
- Counts before and after distinct elimination.
- Parentheses, final ordering, and NULL-containing rows.

### Worked example: a migration that only looked equal

`old EXCEPT new` returns nothing, so the tester declares victory. `new EXCEPT old` reveals 17 unexpected rows. Equivalence requires both directions—or a symmetric comparison—not optimism in one direction.

**Quiz.** What does UNION do with duplicate rows by default?

- [ ] Keeps all
- [x] Eliminates duplicates
- [ ] Throws an error
- [ ] Keeps only duplicates

*UNION uses distinct semantics unless UNION ALL is specified.*

- **UNION** — Rows from either input, duplicates removed by default.
- **INTERSECT** — Rows present in both inputs.
- **EXCEPT** — Rows in the left input but not the right.
- **Union compatible** — Same column count with compatible corresponding types.

### Challenge

Verify two migrated key/value projections with bidirectional EXCEPT, explicit duplicate checks, and deterministic output.

### Ask the community

> My set comparison lost `[duplicates/rows]`; here are branch schemas, counts, and operators.

Include whether ALL was used and how NULLs should be treated.

- [PostgreSQL — combining queries](https://www.postgresql.org/docs/current/queries-union.html)
- [PostgreSQL — UNION type resolution](https://www.postgresql.org/docs/current/typeconv-union-case.html)

🎬 [freeCodeCamp — SQL tutorial, full database course](https://www.youtube.com/watch?v=HXV3zeQKqGY) (261 min)

- UNION, INTERSECT, and EXCEPT express either, both, and left-only relationships.
- Default set operators remove duplicates; ALL preserves multiplicity.
- Inputs must be union compatible.
- Parenthesize mixed operators and compare migrations in both directions.


## Related notes

- [[Notes/relational-databases-engineer-level/sql-mastery/subqueries-and-ctes|Subqueries & CTEs]]
- [[Notes/relational-databases-engineer-level/schema-design/keys-and-relationships|Keys & relationships]]
- [[Notes/relational-databases-engineer-level/sql-mastery/window-functions|Window functions]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/sql-mastery/set-operators.mdx`_
