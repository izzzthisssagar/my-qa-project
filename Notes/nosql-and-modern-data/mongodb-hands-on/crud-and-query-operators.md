---
title: "CRUD and query operators"
tags: ["mongodb", "crud", "queries", "operators", "track-d"]
updated: "2026-07-17"
---

# CRUD and query operators

*Test MongoDB create, read, update, and delete operations with precise filters, safe update operators, and evidence about how many documents actually matched and changed.*

> An update command can succeed while changing zero documents. It can also succeed while changing ten
> thousand because the filter was too broad. “No exception” is not CRUD correctness; matched count,
> modified count, final state, and unintended neighbors are the evidence.

> **In real life**
>
> A magnifying glass defines what you act on. If the lens frames the wrong records, even a perfectly
> executed update or delete damages the wrong data. Inspect the filter before admiring the operation.

**query filter**: A MongoDB query filter is a BSON document whose field conditions and operators select documents for reads, updates, or deletes. Update operators such as $set, $inc, $push, and $unset change selected fields without replacing the entire document.

## CRUD is filter plus effect

- **Create:** `insertOne` or `insertMany`; verify generated `_id`, validation, duplicates, and partial bulk behavior.
- **Read:** `find`; combine equality and operators such as `$gt`, `$in`, `$exists`, `$elemMatch`, `$and`, and `$or`.
- **Update:** choose `updateOne`, `updateMany`, or `replaceOne`; verify matched and modified counts.
- **Delete:** choose `deleteOne` or `deleteMany`; preview the exact filter before destructive work.

Single-document writes are atomic. That does not make a multi-document business operation atomic, and
it does not make a broad filter correct. Also distinguish a no-op update—matched but same value—from a
miss—nothing matched.

> **Tip**
>
> For risky updates, run the same filter as a read first, inspect identifiers and count, then update with
> an expected version field. Verify both the target and a nearby non-target document.

> **Common mistake**
>
> Using replacement syntax when you intend `$set`. Replacing a document omits every field not supplied;
> a small profile edit can silently erase unrelated data.

![A large blue magnifying-glass icon](crud-and-query-operators.png)
*Magnifying glass CC0 — Igel B TyMaHe, CC0 1.0. [Source](https://commons.wikimedia.org/wiki/File:Magnifying_glass_CC0.svg)*
- **Filter field** — Name the field precisely, including nested dot notation and expected BSON type.
- **Operator** — Equality, ranges, membership, existence, and array semantics select different populations.
- **Effect** — After selection, verify matched, modified, deleted, upserted, and final-state evidence.

**A safe update test**

1. **Seed target and neighbor** — Create one document that should change and one similar document that must not.
2. **Preview the filter** — Read identifiers and count using exactly the update filter.
3. **Apply one operator** — Use $set, $inc, or another intentional operator instead of accidental replacement.
4. **Read the result object** — Assert acknowledged, matched, modified, and upserted counts as applicable.
5. **Verify stored state** — Check the changed fields, preserved fields, and BSON types.
6. **Verify the neighbor** — Prove the broadest near-match remained untouched.

*Run it — filter then update safely (Python)*

```python
``docs = [
    {"id": 1, "tenant": "A", "status": "open", "attempts": 0},
    {"id": 2, "tenant": "B", "status": "open", "attempts": 0},
]
targets = [d for d in docs if d["tenant"] == "A" and d["status"] == "open"]
assert [d["id"] for d in targets] == [1]
for d in targets:
    d["attempts"] += 1  # like $inc
print(docs)
assert docs[0]["attempts"] == 1 and docs[1]["attempts"] == 0``
```

*Run it — filter then update safely (Java)*

```java
``import java.util.*;

public class Main {
    record Doc(int id, String tenant, String status, int attempts) {}
    public static void main(String[] args) {
        var docs = new ArrayList<>(List.of(new Doc(1,"A","open",0), new Doc(2,"B","open",0)));
        long matches = docs.stream().filter(d -> d.tenant().equals("A") && d.status().equals("open")).count();
        if (matches != 1) throw new AssertionError("unsafe filter");
        docs.replaceAll(d -> d.tenant().equals("A") && d.status().equals("open")
            ? new Doc(d.id(), d.tenant(), d.status(), d.attempts()+1) : d);
        System.out.println(docs);
        if (docs.get(1).attempts() != 0) throw new AssertionError("neighbor changed");
    }
}``
```

### Your first time: Your mission: prove one update is scoped

- [ ] Create a target and near-match — Differ them by the tenant, state, or owner condition most likely to be omitted.
- [ ] Preview exact identifiers — Use the production filter and assert the expected count before changing data.
- [ ] Assert result counts — Distinguish matched zero, matched but unchanged, modified, and upserted.
- [ ] Verify preservation — Confirm unrelated fields and the near-match retain their original values and types.

You now test both intended effect and blast radius.

- **Update returns success but the record does not change.**
  Compare matchedCount and modifiedCount; inspect filter type, field path, current value, and write concern.
- **An update removes unrelated fields.**
  Check for replacement semantics; use update operators for partial changes.
- **A nested-array query matches unexpected documents.**
  Use $elemMatch when multiple conditions must apply to the same array element.
- **Two clients overwrite each other's changes.**
  Add an expected version or previous-value condition and assert a zero-match conflict response.

### Where to check

- **Command result counts** — acknowledged alone is weak evidence.
- **Explain plan and indexes** — correct filters can still scan too much data.
- **BSON types in filter and storage** — string `"5"` and numeric `5` are different.
- **Write concern** — accepted locally is not the same as durably replicated.
- **Audit or change stream** — reconstruct unintended multi-document effects.

### Worked example: an array query that matched two different elements

1. Product documents contain an `offers` array with seller and price fields.
2. A filter asks for `offers.seller = A` and `offers.price < 10` as separate dotted conditions.
3. One element has seller A at 50; another has seller B at 5, and the document still matches.
4. `$elemMatch` binds both conditions to one array element.
5. Tests include split-condition and same-element fixtures so this semantic difference stays visible.

**Quiz.** An update reports matchedCount=1 and modifiedCount=0. What can you conclude?

- [ ] The server failed
- [x] One document matched, but the operation produced no stored change—for example the value was already equal
- [ ] Exactly one document was deleted
- [ ] The filter matched nothing

*Matched and modified counts answer different questions. A matching document may already contain the requested value, producing a legitimate no-op.*

- **Single-document atomicity** — A write to one document is atomic; a multi-document workflow needs separate guarantees.
- **matchedCount vs modifiedCount** — MatchedCount selects documents; modifiedCount reports stored changes.
- **$set vs replacement** — $set changes named fields; replacement substitutes the document and can remove omitted fields.
- **$elemMatch** — Requires multiple conditions to hold on the same array element.
- **Safe delete habit** — Preview exact filter identifiers and count, then verify target removal and neighbor survival.

### Challenge

Write fixtures that distinguish `$in`, `$exists`, `null`, and `$elemMatch`. Predict every match before
running the filters, then add an update and prove its non-target blast radius is zero.

### Ask the community

> MongoDB [operation] uses filter [anonymized filter]. Result is matched=[n], modified/deleted=[n], but expected [state]. Stored BSON types are [types]. Which query semantic should I isolate?

Include a minimal target and near-match document without production secrets.

- [MongoDB Manual — CRUD operations](https://www.mongodb.com/docs/manual/crud/)
- [MongoDB Manual — Query documents](https://www.mongodb.com/docs/manual/tutorial/query-documents/)
- [MongoDB Manual — Update operators](https://www.mongodb.com/docs/manual/reference/operator/update/)

🎬 [Complete CRUD Operations in MongoDB — ProgrammingKnowledge](https://www.youtube.com/watch?v=H5sDjNfl3xA) (10 min)

- MongoDB CRUD operations combine a selection filter with an effect.
- Assert matched, modified, deleted, and upserted counts—not only absence of exceptions.
- Update operators preserve unrelated fields; replacement can remove them.
- Array and BSON-type semantics deserve adversarial fixtures.
- Every mutation test needs a near-match that must remain unchanged.


## Related notes

- [[Notes/nosql-and-modern-data/mongodb-hands-on/documents-and-collections|Documents & collections]]
- [[Notes/nosql-and-modern-data/mongodb-hands-on/aggregation-pipeline-gently|Aggregation pipeline, gently]]
- [[Notes/relational-databases-engineer-level/data-integrity-at-scale/auditing-data-changes|Auditing data changes]]


---
_Source: `packages/curriculum/content/notes/nosql-and-modern-data/mongodb-hands-on/crud-and-query-operators.mdx`_
