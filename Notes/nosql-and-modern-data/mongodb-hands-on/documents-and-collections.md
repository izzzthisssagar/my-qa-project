---
title: "Documents and collections"
tags: ["mongodb", "bson", "documents", "collections", "track-d"]
updated: "2026-07-17"
---

# Documents and collections

*Read MongoDB's BSON document model precisely, inspect mixed shapes safely, and test the collection contracts that flexible schemas do not enforce for you.*

> Two MongoDB documents can sit in the same collection while one has `price` as a number, another has
> `price` as text, and a third has no `price` at all. The database accepted all three. Your application
> still has to survive them—and your tests must find them before a production reader does.

> **In real life**
>
> A card catalogue groups records by purpose, but every card can carry different annotations. The
> drawer is the collection; one card is a document; its printed and handwritten fields are BSON values.

**BSON document**: A MongoDB document is an ordered set of field-value pairs encoded as BSON, a binary representation that extends JSON with types such as dates, ObjectIds, and 64-bit integers. Documents live in collections, and every standard collection document has a unique, immutable _id primary key.

## Shape is flexible; contracts are not optional

MongoDB documents can contain scalar values, arrays, embedded documents, and arrays of documents.
Collections group documents, and databases group collections. MongoDB does not require every document
in a collection to expose identical fields or types, though schema validation can enforce rules.

That flexibility supports evolution, but it moves testing attention toward:

- missing versus explicit `null`;
- numeric BSON types and driver conversions;
- old and new field names living together;
- duplicate business identifiers despite unique `_id` values;
- arrays whose element shape or size changes over time;
- the 16 MiB BSON document limit and unbounded growth.

> **Tip**
>
> Build a shape census before a migration: group by field presence and BSON type. A sample of the newest
> ten documents proves almost nothing about historical production data.

> **Common mistake**
>
> Comparing serialized JSON text. BSON types and field order can differ while business meaning remains
> the same. Assert required fields, types, values, and arrays deliberately.

![Rows of wooden card catalogue drawers with labels and metal pulls](documents-and-collections.jpg)
*Card catalogue drawers — Carolina Prysyazhnyuk, CC BY-SA 2.0. [Source](https://commons.wikimedia.org/wiki/File:Card_catalogue_drawers.jpg)*
- **Collection** — A named drawer groups documents for one application concern; it does not force every card to share one shape.
- **Document** — One card-like record contains field-value pairs, nested values, and its unique _id.
- **Index label** — Indexes create lookup paths over chosen fields; _id receives a unique index by default in standard collections.
- **Historical shapes** — Older drawers remain after application releases. Readers and migrations must handle every supported shape.

**From application object to stored document**

1. **Application builds values** — The driver receives strings, numbers, dates, arrays, objects, and an optional _id.
2. **Driver encodes BSON** — Language values map to BSON types; lossy or mismatched conversions can begin here.
3. **Validation runs** — Configured collection validators may reject shape or type violations; absent rules accept more variation.
4. **Document is stored** — The record enters one collection with a unique immutable _id.
5. **Reader decodes** — A possibly different driver and application version must interpret the stored BSON safely.
6. **Test samples history** — Checks cover old, new, missing, null, extreme, and malformed-but-existing shapes.

*Run it — census mixed document shapes (Python)*

```python
``docs = [
    {"_id": 1, "price": 12.50, "tags": ["sale"]},
    {"_id": 2, "price": "12.50"},
    {"_id": 3, "price": None},
    {"_id": 4},
]
for doc in docs:
    state = "missing" if "price" not in doc else type(doc["price"]).__name__
    print(doc["_id"], state)
assert sum(isinstance(d.get("price"), (int, float)) for d in docs) == 1``
```

*Run it — census mixed document shapes (Java)*

```java
``import java.util.*;

public class Main {
    public static void main(String[] args) {
        var docs = List.<Map<String,Object>>of(
            new HashMap<>(Map.of("_id", 1, "price", 12.50)),
            new HashMap<>(Map.of("_id", 2, "price", "12.50")),
            new HashMap<>(), new HashMap<>(Map.of("_id", 4))
        );
        docs.get(2).put("_id", 3); docs.get(2).put("price", null);
        long numbers = 0;
        for (var d : docs) {
            Object value = d.get("price");
            String state = !d.containsKey("price") ? "missing" : value == null ? "null" : value.getClass().getSimpleName();
            System.out.println(d.get("_id") + " " + state);
            if (value instanceof Number) numbers++;
        }
        if (numbers != 1) throw new AssertionError();
    }
}``
```

### Your first time: Your mission: inspect one collection's real shape

- [ ] Choose five contract fields — Include _id, one nested field, one array, and one field changed by a past release.
- [ ] Count missing, null, and BSON types — Do not collapse these states into truthy and falsy.
- [ ] Find the oldest surviving shape — Verify the current reader handles it or that a controlled migration removes it.
- [ ] Record enforcement — Separate collection validation, unique indexes, and application-only assumptions.

You now have a collection contract based on stored evidence.

- **A numeric comparison skips some documents.**
  Group the field by BSON type; strings that look numeric are still strings.
- **A new reader crashes only on old accounts.**
  Compare version-era shapes and add tolerant reading or a verified migration.
- **Duplicate users exist despite unique _id values.**
  _id uniqueness protects only _id; add and test the intended unique business index.
- **An embedded array approaches the document limit.**
  Measure BSON size and growth; bound or reference unbounded child data.

### Where to check

- **MongoDB Compass or `mongosh`** — inspect stored BSON types, not API serialization alone.
- **Collection validators** — check validation level/action and deployment drift.
- **Indexes** — confirm business uniqueness exists and is actually usable.
- **Driver codec configuration** — dates, decimals, UUIDs, and 64-bit integers can map differently.
- **Historical records** — migrations fail on the rare old shape, not the ideal fixture.

### Worked example: a price filter that lost products silently

1. An importer stores some prices as strings while the API stores numbers.
2. A sale query asks for numeric values below 20 and returns only correctly typed documents.
3. UI tests use recently created numeric fixtures, so the gap stays invisible.
4. A shape census finds both `double` and `string`; the team validates new writes and migrates old values.
5. Tests verify counts, rejected invalid writes, conversion failures, and rollback evidence.

**Quiz.** What does MongoDB's flexible document model guarantee?

- [ ] Every document in a collection has the same fields and types
- [x] A standard collection document has a unique _id, while other shape rules require validation, indexes, or application logic
- [ ] Every number is stored as the same BSON type
- [ ] Documents can grow without a size limit

*MongoDB requires a unique _id in standard collections. Other field, type, and business rules are not implied merely by collection membership.*

- **BSON** — MongoDB's binary document representation, extending JSON with additional types.
- **Collection** — A named group of documents; membership alone does not force identical shape.
- **Missing versus null** — Missing means no field; null is a stored field value. Queries and application behavior can differ.
- **_id** — A unique, immutable primary key required for documents in standard collections.
- **Maximum BSON document size** — 16 MiB; unbounded embedded arrays require design scrutiny.

### Challenge

Create eight representative documents for one entity: current, oldest, missing optional field, explicit
null, wrong historical type, empty array, maximal array, and duplicate business identifier. Predict
which layer accepts each, then verify.

### Ask the community

> Collection [name] contains [field] as BSON types [types], with [missing/null counts]. Validation enforces [rules], while the app assumes [contract]. What migration or tolerant-read risk am I missing?

Include engine/driver versions and anonymized shape counts, not production values.

- [MongoDB Manual — Documents](https://www.mongodb.com/docs/manual/core/document/)
- [MongoDB Manual — Databases and collections](https://www.mongodb.com/docs/manual/core/databases-and-collections/)
- [MongoDB Manual — Schema validation](https://www.mongodb.com/docs/manual/core/schema-validation/)

🎬 [Collections & Documents — Net Ninja](https://www.youtube.com/watch?v=ojKJqNQYaOI) (4 min)

- MongoDB stores BSON documents in collections, with nested values and typed fields.
- Flexible shape does not remove schema; it changes where schema is enforced.
- Missing, null, and wrong BSON type are distinct test cases.
- _id uniqueness does not enforce business-key uniqueness.
- Historical shape censuses reveal risks that fresh fixtures conceal.


## Related notes

- [[Notes/nosql-and-modern-data/mongodb-hands-on/crud-and-query-operators|CRUD & query operators]]
- [[Notes/nosql-and-modern-data/mongodb-hands-on/embedding-vs-referencing|Embedding vs referencing]]
- [[Notes/nosql-and-modern-data/the-nosql-landscape/document-key-value-graph-columnar|Document, key-value, graph & columnar]]


---
_Source: `packages/curriculum/content/notes/nosql-and-modern-data/mongodb-hands-on/documents-and-collections.mdx`_
