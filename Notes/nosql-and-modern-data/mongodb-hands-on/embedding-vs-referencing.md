---
title: "Embedding vs referencing"
tags: ["mongodb", "embedding", "references", "data-modeling", "track-d"]
updated: "2026-07-17"
---

# Embedding vs referencing

*Choose MongoDB document boundaries from read/write behavior, growth, and consistency—and test the duplication and orphan risks each choice creates.*

> Embedding an address inside every order makes order reads beautifully simple—and address corrections
> deliberately do not rewrite history. Embedding that same customer status may create stale duplicates.
> The syntax looks identical; the business meaning decides whether duplication is a feature or a bug.

> **In real life**
>
> Nesting dolls travel as one object and open together. Separate dolls connected by catalogue numbers can
> change independently, but someone must follow the references and handle a missing piece.

**embedding and referencing**: Embedding stores related data inside one parent document, usually enabling one read and one-document atomic updates. Referencing stores related entities in separate documents and records identifiers that applications or $lookup stages resolve, reducing duplication while introducing additional reads and dangling-reference risk.

## Model what changes together

Embedding is usually attractive when data is read together, updated together, bounded in size, and
owned by the parent. Referencing becomes attractive when children grow without bound, exist
independently, change frequently, are shared by many parents, or form complex many-to-many relations.

Neither choice removes consistency work:

- embedded snapshots may intentionally preserve historical truth;
- duplicated live facts need update propagation and reconciliation;
- references need missing-target, deletion, permission, and multi-read handling;
- `$lookup` can join collections, but does not erase model or performance trade-offs.

> **Tip**
>
> Write the lifecycle sentence: “When X changes, should every existing Y show the new value?” The answer
> often reveals whether duplicated embedded data is a snapshot or a stale-data defect.

> **Common mistake**
>
> Embedding an unbounded activity stream because the first fixture has three items. Test projected growth,
> document size, update contention, and whether the array must be paginated independently.

![Opened wooden nesting dolls with smaller dolls visible beside larger shells](embedding-vs-referencing.jpg)
*Matryoshka dolls — Wikimedia Commons contributor, public domain. [Source](https://commons.wikimedia.org/wiki/File:Matryoshka_dolls.jpg)*
- **Embedded child** — The smaller value travels inside the parent and can be updated atomically with it.
- **Aggregate boundary** — One parent document should contain a bounded set of facts commonly read and changed together.
- **Independent reference** — A separate child can live and change alone, but its identifier may become dangling or unauthorized.
- **Shared target** — Many parents may point to one authoritative entity rather than duplicate a frequently changing fact.

**Decide embed or reference**

1. **Name the relationship** — Describe ownership, cardinality, and whether the child can exist alone.
2. **Map reads and writes** — Identify which facts load and change together, including historical behavior.
3. **Bound growth** — Estimate worst-case count, BSON size, contention, and pagination need.
4. **Choose a source of truth** — For duplicated fields, state whether each copy is a snapshot or must remain current.
5. **Test lifecycle edges** — Exercise update, deletion, missing target, migration, and reconciliation.

*Run it — snapshot versus live reference (Python)*

```python
``customer = {"id": "c1", "name": "Asha"}
order_embedded = {"id": "o1", "customer": {"id": "c1", "name": customer["name"]}}
order_referenced = {"id": "o2", "customer_id": customer["id"]}

customer["name"] = "Asha Thapa"
print("historical snapshot:", order_embedded["customer"]["name"])
print("live reference:", customer["name"] if order_referenced["customer_id"] == customer["id"] else "missing")
assert order_embedded["customer"]["name"] == "Asha"``
```

*Run it — snapshot versus live reference (Java)*

```java
``import java.util.*;

public class Main {
    public static void main(String[] args) {
        var customer = new HashMap<String,String>(Map.of("id","c1", "name","Asha"));
        var embedded = new HashMap<String,String>(Map.of("customerId","c1", "customerName",customer.get("name")));
        var referenced = new HashMap<String,String>(Map.of("customerId",customer.get("id")));
        customer.put("name", "Asha Thapa");
        System.out.println("historical snapshot: " + embedded.get("customerName"));
        System.out.println("live reference: " + (referenced.get("customerId").equals(customer.get("id")) ? customer.get("name") : "missing"));
        if (!embedded.get("customerName").equals("Asha")) throw new AssertionError();
    }
}``
```

### Your first time: Your mission: classify one duplicated field

- [ ] Choose one parent-child pair — Examples: order/customer, post/comments, product/category, or room/messages.
- [ ] State ownership and maximum cardinality — Bound the child count using a credible worst case, not today's average.
- [ ] Classify duplicated fields — Mark each as immutable fact, historical snapshot, or live value requiring propagation.
- [ ] Write deletion behavior — Specify cascade, preserve snapshot, reject deletion, or tolerate a missing reference.

You now have a lifecycle model, not merely nested JSON.

- **A customer rename appears in some orders but not others.**
  Decide snapshot versus live semantics; reconcile only fields meant to remain current.
- **A parent document grows and updates become slow.**
  Measure BSON size and array cardinality; move independently paginated or unbounded children to references.
- **An API returns null for a referenced entity.**
  Check deletion order, tenant filters, permissions, replication lag, and dangling identifiers.
- **Concurrent child additions overwrite each other.**
  Use atomic array operators where embedding is bounded, or independent child documents when write contention is high.

### Where to check

- **BSON document size and array length** — observe high percentiles, not averages.
- **Source-of-truth documentation** — every duplicated live field needs an owner.
- **Orphan-reference queries** — compare stored identifiers with target existence and tenant.
- **Update fan-out metrics** — one logical change touching thousands of parents is a warning.
- **Historical requirements** — snapshots may be legally or operationally correct.

### Worked example: why an order should keep an old shipping address

1. An order embeds the shipping address used at checkout.
2. The customer later updates the account address.
3. A generic stale-data test expects every embedded address to change and flags the order.
4. The business contract says shipped orders preserve the original destination for audit.
5. Tests therefore treat the embedded address as an immutable snapshot while new orders use the live customer reference.

**Quiz.** Which relationship most strongly favors referencing?

- [ ] A small bounded value object always read and changed with its parent
- [ ] A historical snapshot that must never follow later edits
- [x] A high-cardinality child set that grows without bound and is paginated independently
- [ ] Two fields updated atomically in one aggregate

*Unbounded, independently accessed children risk oversized, contentious parent documents. References allow separate lifecycle and pagination.*

- **Embed when** — Data is bounded, owned, read together, and changed together.
- **Reference when** — Children are unbounded, shared, independent, frequently changing, or many-to-many.
- **Snapshot duplication** — A copy intentionally preserves historical value and should not follow later source edits.
- **Dangling reference** — A stored identifier points to no accessible target document.
- **Key growth test** — Measure worst-case BSON size, array count, write contention, and pagination needs.

### Challenge

Model product reviews once embedded and once referenced. For each design, write tests for create,
moderation, user deletion, 100,000 reviews, pagination, product deletion, and restore.

### Ask the community

> For [parent/child], reads are [pattern], child count reaches [bound], and [field] should [snapshot/stay live]. We plan to [embed/reference]. Which lifecycle test would challenge this model most?

Include growth and update frequency; a tiny example cannot expose the main trade-off.

- [MongoDB Manual — Data-modeling best practices](https://www.mongodb.com/docs/manual/data-modeling/best-practices/)
- [MongoDB Manual — Reference data](https://www.mongodb.com/docs/manual/data-modeling/referencing/)
- [MongoDB Manual — Enforce consistency with embedding](https://www.mongodb.com/docs/manual/data-modeling/enforce-consistency/embed-data/)

🎬 [Embedding vs. Referencing Explained — MongoDB](https://www.youtube.com/watch?v=TKlSyI_diZI) (2 min)

- Embed bounded data owned, read, and changed with its parent.
- Reference independent, shared, high-cardinality, or unbounded data.
- Classify duplicated fields as snapshots or live facts before testing staleness.
- Embedding trades join work for growth, duplication, and contention risks.
- References add missing-target, authorization, and multi-read failure modes.


## Related notes

- [[Notes/nosql-and-modern-data/mongodb-hands-on/documents-and-collections|Documents & collections]]
- [[Notes/nosql-and-modern-data/mongodb-hands-on/aggregation-pipeline-gently|Aggregation pipeline, gently]]
- [[Notes/relational-databases-engineer-level/schema-design/when-to-denormalize|When to denormalize]]


---
_Source: `packages/curriculum/content/notes/nosql-and-modern-data/mongodb-hands-on/embedding-vs-referencing.mdx`_
