---
title: "ACID, properly"
tags: ["relational-databases-engineer-level", "transactions-and-concurrency", "track-e"]
updated: "2026-07-17"
---

# ACID, properly

*ACID is a set of transaction guarantees, not a claim that every business rule is automatic. Learn what each letter promises, what it does not, and how to test a transfer safely.*

> A bank transfer is not two unrelated balance edits. It is one promise: debit and credit happen together, valid rules still hold, concurrent work cannot produce forbidden histories, and a reported commit survives.

> **In real life**
>
> ACID resembles a sealed delivery. Atomicity keeps the package together, consistency checks what is allowed inside, isolation controls simultaneous couriers, and durability keeps the signed delivery from vanishing.

**ACID**: ACID names four transaction properties: atomicity, consistency, isolation, and durability. Together they describe all-or-nothing changes, preservation of declared invariants, controlled concurrent histories, and committed results that persist after successful completion.

## Read each guarantee precisely

- **Atomicity:** every statement in the transaction commits, or none of its transactional changes do.
- **Consistency:** a successful transaction preserves constraints and application invariants that were actually defined and enforced.
- **Isolation:** concurrent transactions behave according to the selected isolation level; weaker levels permit more histories.
- **Durability:** after the database reports a successful commit, its configured recovery machinery preserves that result across failure.

> **Tip**
>
> Write each business invariant as a constraint, serialized decision, or explicit test. The word consistency cannot enforce a rule the database was never told.

> **Common mistake**
>
> Treating ACID as a magic correctness badge. A transaction can atomically and durably commit the wrong price, an invalid workflow transition, or a race allowed by its isolation level.

![Tall black bank vault door set into an interior wall](acid-properly.jpg)
*Inside the Bank, Vault Door — Ratinsley, Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:Inside_the_Bank,_Vault_Door.jpg)*
- **Atomic boundary** — The vault boundary represents one unit that opens or closes as a whole.
- **Enforced mechanism** — The handle is a concrete control, like constraints and recovery records—not a hopeful label.
- **Durable enclosure** — A successful commit depends on configured persistence and recovery guarantees.

**A transfer transaction**

1. **BEGIN** — Open one transaction boundary.
2. **Validate invariant** — Confirm the debit is permitted under a concurrency-safe rule.
3. **Debit and credit** — Apply both related changes inside the same transaction.
4. **COMMIT or ROLLBACK** — Publish all changes or discard them together.
5. **Recover if needed** — Durability machinery re-establishes committed state after failure.

*Run it — roll back a failed transfer (Python)*

```python
accounts = {"checking": 120, "savings": 80}

def transfer(state, amount, fail=False):
    working = state.copy()
    working["checking"] -= amount
    if working["checking"] < 0:
        raise ValueError("insufficient funds")
    if fail:
        raise RuntimeError("credit service failed")
    working["savings"] += amount
    state.clear()
    state.update(working)

try:
    transfer(accounts, 30, fail=True)
except RuntimeError as error:
    print(error)
print(accounts, "total=", sum(accounts.values()))

# credit service failed
# {'checking': 120, 'savings': 80} total= 200
```

*Run it — publish only a valid transfer (Java)*

```java
import java.util.*;
public class Main {
  static Map<String,Integer> transfer(Map<String,Integer> state, int amount) {
    Map<String,Integer> working = new LinkedHashMap<>(state);
    working.put("checking", working.get("checking") - amount);
    if (working.get("checking") < 0) throw new IllegalArgumentException("insufficient funds");
    working.put("savings", working.get("savings") + amount);
    return working;
  }
  public static void main(String[] args) {
    Map<String,Integer> accounts = new LinkedHashMap<>();
    accounts.put("checking", 120); accounts.put("savings", 80);
    Map<String,Integer> committed = transfer(accounts, 30);
    System.out.println(committed + " total=" + committed.values().stream().mapToInt(Integer::intValue).sum());
  }
}
/* {checking=90, savings=110} total=200 */
```

### Your first time: Your mission: specify one transactional promise

- [ ] Name the transaction boundary — List every statement that must succeed or fail together.
- [ ] Write the invariant — Express totals, uniqueness, ranges, or state transitions precisely.
- [ ] Choose concurrency control — Select isolation, locking, or a conditional update for the race.
- [ ] Inject failure before commit — Verify rollback leaves no partial effect.

You now have a falsifiable guarantee instead of an ACID label.

- **The debit remains but the credit is missing.**
  Place both writes on the same connection and transaction; reject hidden auto-commit boundaries.
- **Two valid transactions jointly violate a rule.**
  Test the concurrent history and strengthen isolation, locking, constraints, or conditional writes.
- **A retry duplicates an external effect.**
  Make retries idempotent and coordinate database state with an outbox or equivalent protocol.

### Where to check

- Transaction boundaries and auto-commit settings in the client library.
- Database constraints that encode invariants.
- PostgreSQL server and storage durability configuration.
- Logs for rollback, serialization failure, connection loss, and retry behavior.

### Worked example: the transfer that was atomic but still wrong

1. A transaction debits one account and credits another together.
2. Both updates commit atomically and durably.
3. The code forgot to reject a negative source balance.
4. No database constraint or serialized check expresses that rule.
5. ACID worked; the missing invariant made the result incorrect.

**Quiz.** What does ACID consistency guarantee?

- [ ] Every business rule is inferred automatically
- [x] A successful transaction preserves the invariants that the system actually defines and enforces
- [ ] Every transaction runs serially
- [ ] Committed data can never be lost under any imaginable hardware failure

*Consistency depends on real constraints and correct transaction logic; ACID is not an oracle for unstated business rules.*

- **Atomicity** — All transactional changes commit together or roll back together.
- **Isolation** — The permitted interactions among concurrent transactions at a chosen level.
- **Durability** — A successfully committed result persists according to configured recovery guarantees.

### Challenge

Model an order placement transaction. Identify one invariant, one partial-failure point, one concurrent race, and one external side effect that needs idempotency.

### Ask the community

> Our transaction promises `[invariant]`, uses `[isolation/locks]`, and fails at `[point]`. The observed state is `[state]`. Which ACID property or application contract is missing?

Show boundaries and constraints; the acronym alone is not a diagnosis.

- [PostgreSQL — Transactions tutorial](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [PostgreSQL — Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

🎬 [Relational Database ACID Transactions (Explained by Example) — Hussein Nasser](https://www.youtube.com/watch?v=pomxJOFVcQs) (43 min)

- Atomicity prevents partial transactional publication.
- Consistency requires explicitly defined and enforced invariants.
- Isolation is a selectable concurrency contract, not always serial execution.
- Durability begins after a successful commit acknowledgement.
- External side effects need protocols beyond a local database transaction.


## Related notes

- [[Notes/relational-databases-engineer-level/transactions-and-concurrency/isolation-levels-and-anomalies|Isolation levels & anomalies]]
- [[Notes/relational-databases-engineer-level/transactions-and-concurrency/testing-concurrent-behavior|Testing concurrent behavior]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/transactions-and-concurrency/acid-properly.mdx`_
