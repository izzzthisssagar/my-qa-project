---
title: "Auditing Data Changes"
tags: ["postgresql", "auditing", "triggers", "data-integrity"]
updated: "2026-07-17"
---

# Auditing Data Changes

*Design and test append-only database audit evidence that answers who changed what, when, and in which transaction.*

> An `updated_at` column says something changed. An audit trail must answer who, what, when, from where, and under which transaction—without becoming a second ungoverned copy of sensitive data.

> **In real life**
>
> An audit table is a general ledger. Entries are appended, attributable, ordered, and reconcilable. Erasing a line to make the balance prettier defeats the reason the ledger exists.

## Capture evidence, not noise

Define the threat and investigation model first. An **audit event**: Attributable, correlated evidence of a governed data operation and its relevant delta. often includes event ID, occurred time, actor, transaction/request correlation, operation, table, row key, and old/new or changed fields. Database users may be pooled service accounts, so application actor identity often needs trusted session context.

![A general ledger illustrating append-only change history](auditing-data-changes.jpg)
*Image: Bgibbs, Wikimedia Foundation — Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:General_ledger_example.jpg)*
- **Attribution** — Actor, request, transaction, and source connect the change to a responsible execution context.
- **Before and after** — Operation plus row key and changed values explain what actually happened.
- **Append-only evidence** — Restricted writes, retention, export, and monitoring protect the history from casual alteration.

> **Tip**
>
> Test audit behavior inside the same transaction as the business change. A rolled-back update should not leave an audit row claiming a change that never committed.

> **Common mistake**
>
> Copying every row as JSON forever. Secrets, personal data, storage cost, and access scope multiply. Capture the minimum investigation evidence and apply explicit retention.

**Audit event lifecycle**

1. **Context** — Set trusted actor and request correlation before the write.
2. **Change** — The business statement inserts, updates, or deletes governed data.
3. **Record** — An audit trigger or service appends operation, identity, key, and delta in the transaction.
4. **Protect + review** — Restrict mutation, retain appropriately, export if required, and monitor gaps.

*Build a minimal audit event*

```python
event = {
    "event_id": "evt-1042",
    "actor": "user-17",
    "operation": "UPDATE",
    "row_key": "order-42",
    "changed": "status:PENDING->PAID",
    "occurred_at": "2026-07-17T10:15:30Z",
}
required = {"event_id", "actor", "operation", "row_key", "changed", "occurred_at"}
assert required <= event.keys()
print(event)
```

*Build the same event in Java*

```java
import java.time.*;
import java.util.*;
class Main {
  public static void main(String[] args) {
    Map<String, String> event = new LinkedHashMap<>();
    event.put("event_id", "evt-1042");
    event.put("actor", "user-17");
    event.put("operation", "UPDATE");
    event.put("row_key", "order-42");
    event.put("changed", "status:PENDING->PAID");
    event.put("occurred_at", Instant.parse("2026-07-17T10:15:30Z").toString());
    event.forEach((key, value) -> System.out.println(key + "=" + value));
  }
}
```

### Your first time: Test an audit trail

- [ ] Define required evidence — Map investigation questions to fields, sensitivity, and retention.
- [ ] Exercise every operation — Insert, meaningful update, no-op update, delete, bulk statement, and privileged path.
- [ ] Assert transaction behavior — Commit produces one attributable event per contract; rollback produces none.
- [ ] Test protection — The application role can read only as intended and cannot rewrite or delete history.

- **Every event actor is the same service account.**
  Propagate authenticated actor through trusted transaction-local context and record both application and database identities.
- **No-op updates flood the trail.**
  Define meaningful-change semantics and compare OLD with NEW in a narrow WHEN condition or function.
- **Audit rows exist for rolled-back changes.**
  Keep audit writes transactional; external emission needs an outbox or commit-aware design.

### Where to check

Inspect trigger definitions, audit-table grants, actor context setup, row-event correlation, transaction IDs, timestamps/time zone, retention jobs, export monitoring, and gaps between business changes and audit events.

### Worked example: Auditing an order status change

As application actor `user-17`, update order 42 from PENDING to PAID. Assert one event with actor, request ID, UPDATE, row key, old/new status, and transaction correlation. Roll back a second update and assert no durable event. Attempt audit DELETE as the app role and assert denial.

**Quiz.** Why should a rolled-back business update usually leave no audit row?

- [ ] Audit tables cannot store text
- [x] The claimed durable change never happened, so transactional evidence must roll back with it
- [ ] Timestamps are optional
- [ ] Triggers only run on commit

*An audit trail should describe committed state transitions unless it explicitly models attempted actions separately.*

- **Audit event** — Attributable evidence of a governed operation, row identity, timing, correlation, and relevant delta.
- **Application actor** — The end-user or system principal behind a pooled database connection.
- **Append-only** — Normal writers may add governed events but cannot rewrite or erase prior history.

### Challenge

Create an audit contract for one sensitive table: required fields, actor propagation, no-op policy, bulk behavior, rollback result, access controls, retention, and gap monitor.

### Ask the community

> Audited operation: [table/action]. Expected event: [fields/count]. Actual event and transaction result: [evidence]. Actor propagation: [method]. Which trust gap remains?

Redact sensitive values; share field presence, correlation, roles, and transaction sequence.

- [PostgreSQL — Trigger Functions and Audit Example](https://www.postgresql.org/docs/current/plpgsql-trigger.html)
- [PostgreSQL — Privileges](https://www.postgresql.org/docs/current/ddl-priv.html)

🎬 [Learn PostgreSQL — Full Course for Beginners](https://www.youtube.com/watch?v=qw--VYLpxG4) (260 min)

- Audit evidence must be attributable, correlated, minimal, and protected.
- Test insert, update, delete, bulk, no-op, rollback, and privileged paths.
- Pooled connections require explicit trusted application-actor context.
- Retention and sensitive-data policy are part of audit correctness.


## Related notes

- [[Notes/relational-databases-engineer-level/programmable-objects/triggers|Triggers]]
- [[Notes/relational-databases-engineer-level/data-integrity-at-scale/migrations-and-etl-verification|Migrations & ETL verification]]
- [[Notes/relational-databases-engineer-level/data-integrity-at-scale/finding-orphans-and-duplicates|Finding orphans & duplicates]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/data-integrity-at-scale/auditing-data-changes.mdx`_
