---
title: "Stored Procedures and Functions"
tags: ["postgresql", "stored-procedures", "functions", "database-testing"]
updated: "2026-07-17"
---

# Stored Procedures and Functions

*Choose the right PostgreSQL routine, test its contract, and catch side effects that a happy-path CALL can hide.*

> A routine can pass its demo and still be dangerous. The useful question is not “did it run?” but “did its return value, data changes, errors, and transaction behavior match the contract?”

> **In real life**
>
> A **routine**: Named database code with a declared interface and behavior. is a recipe. A function plates a value you can use in an expression; a procedure runs a kitchen operation through `CALL`. Test ingredients, result, and the state of the kitchen afterward.

## Two tools, two contracts

PostgreSQL functions can be used by queries and may return scalar, row, or set values. Procedures are invoked with `CALL`. That syntax difference is only the first test: inspect parameters, privileges, volatility or side effects, failure behavior, and rows changed.

![An open cookbook representing reusable database routines](stored-procedures-and-functions.jpg)
*General Foods Kitchen cookbook — Wikimedia Commons, public domain. [Source](https://commons.wikimedia.org/wiki/File:Generalfoods_kitchen_cookbook.jpg)*
- **Inputs** — Parameters are the ingredient list: types, nullability, defaults, and boundary values belong in the contract.
- **Instructions** — The body may read data, mutate it, raise errors, or call other routines; tests observe all promised effects.
- **Outcome** — A return value alone is not enough when tables, notices, or transaction state also change.

> **Tip**
>
> Start from `pg_proc` or `\df+` in `psql`, then test the public contract. Catalog inspection catches a wrong signature before test data muddies the diagnosis.

> **Common mistake**
>
> Calling a routine once with typical data and declaring it tested. Duplicate calls, nulls, boundaries, missing rows, permissions, and concurrent use are where contracts fracture.

**Routine test loop**

1. **Read contract** — Record invocation, parameter types, output, allowed state changes, and expected SQLSTATEs.
2. **Arrange** — Create the smallest isolated fixture, including rows the routine must not touch.
3. **Invoke** — Use SELECT for a function or CALL for a procedure with explicit test values.
4. **Assert** — Check result, changed-row set, invariants, and durable state after commit or rollback.

*Model a routine contract*

```python
def reserve(stock, requested):
    if requested <= 0:
        raise ValueError("requested must be positive")
    if requested > stock:
        return {"accepted": False, "remaining": stock}
    return {"accepted": True, "remaining": stock - requested}

cases = [(5, 2), (5, 5), (5, 6)]
for stock, requested in cases:
    result = reserve(stock, requested)
    assert result["remaining"] >= 0
    print(stock, requested, result)
```

*Check the same routine contract in Java*

```java
class Main {
  static int remaining(int stock, int requested) {
    if (requested <= 0) throw new IllegalArgumentException("requested must be positive");
    return requested > stock ? stock : stock - requested;
  }
  public static void main(String[] args) {
    for (int requested : new int[]{2, 5, 6}) {
      int left = remaining(5, requested);
      if (left < 0) throw new AssertionError("negative stock");
      System.out.println(requested + " -> " + left);
    }
  }
}
```

### Your first time: Test one routine deliberately

- [ ] Capture the signature — Record parameter modes, types, defaults, return shape, and invocation syntax.
- [ ] Create a disposable fixture — Include a normal row, boundary row, and unrelated sentinel row.
- [ ] Exercise success and refusal — Assert both outputs and exact rows changed.
- [ ] Repeat the call — Determine whether retry is idempotent, additive, or explicitly rejected.

- **CALL succeeds but the application sees no expected value.**
  Confirm this is a procedure rather than a function and verify OUT parameters or result handling.
- **A retry doubles balances or inventory movement.**
  Treat idempotency as part of the contract; use a request key or assert that retries are rejected safely.
- **It works as owner but fails in production.**
  Execute as the application role and inspect EXECUTE privilege plus object privileges used by invoker-rights code.

### Where to check

`pg_proc`, `information_schema.routines`, the routine definition, application-role privileges, affected tables, and the captured SQLSTATE. Compare pre/post rows by primary key—not just counts.

### Worked example: A reservation procedure that protects stock

Arrange stock `5` and an unrelated product. Call `reserve_item` for `2`; assert stock `3` and one reservation. Call with `6`; assert a documented rejection and no change. Retry the first request key; assert no second reservation. The contract now covers value, side effect, refusal, and retry.

**Quiz.** What is the strongest assertion after a state-changing procedure?

- [ ] It returned without an exception
- [x] The expected rows changed and unrelated rows plus invariants did not
- [ ] The table row count increased
- [ ] The owner role could execute it

*A precise changed-row set plus invariant checks detects both missing and excessive side effects.*

- **Function invocation** — Use it in a query or expression, commonly with SELECT.
- **Procedure invocation** — Use CALL; test its state changes and OUT values if declared.
- **Idempotency** — Repeating the same request has no additional effect, when the contract promises it.

### Challenge

Choose one production routine and write a six-column contract: inputs, invocation, output, allowed mutations, SQLSTATEs, and retry behavior. Add one sentinel row assertion.

### Ask the community

> Routine: [signature]. Expected contract: [result and side effects]. Case: [input]. Observed SQLSTATE/state diff: [evidence]. What assumption should I test next?

Include the exact database version and application role; routine behavior without execution context is incomplete evidence.

- [PostgreSQL 18 — SQL Functions](https://www.postgresql.org/docs/18/xfunc-sql.html)
- [PostgreSQL — CREATE PROCEDURE](https://www.postgresql.org/docs/current/sql-createprocedure.html)
- [PostgreSQL — CALL](https://www.postgresql.org/docs/current/sql-call.html)

🎬 [Learn PostgreSQL — Full Course for Beginners](https://www.youtube.com/watch?v=qw--VYLpxG4) (260 min)

- Functions participate in queries; procedures are invoked with CALL.
- A routine contract includes outputs, mutations, errors, privileges, and retry behavior.
- Assert exact changed rows and untouched sentinels, not success alone.
- Run tests as the real application role inside isolated fixtures.


## Related notes

- [[Notes/relational-databases-engineer-level/programmable-objects/triggers|Triggers]]
- [[Notes/relational-databases-engineer-level/programmable-objects/testing-procedures|Testing procedures]]
- [[Notes/relational-databases-engineer-level/programmable-objects/error-handling-in-sql|Error handling in SQL]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/programmable-objects/stored-procedures-and-functions.mdx`_
