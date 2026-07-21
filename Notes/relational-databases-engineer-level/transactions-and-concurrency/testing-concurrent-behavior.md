---
title: "Testing concurrent behavior"
tags: ["relational-databases-engineer-level", "transactions-and-concurrency", "track-e"]
updated: "2026-07-17"
---

# Testing concurrent behavior

*Concurrency tests need controlled interleavings, independent transactions, bounded waits, and invariant assertions. Build deterministic two-session tests that reveal races without sleep-driven flakiness.*

> A concurrency bug lives in an interleaving. If a test does not control that interleaving, one green run proves almost nothing and one red run may be impossible to reproduce.

> **In real life**
>
> A rowing crew tests coordination by aligning strokes to a coxswain's calls. Barriers play that role for transactions: both sessions reach a precise phase before either proceeds.

**concurrency test**: A deterministic concurrency test runs work on independent sessions, coordinates exact phase boundaries with barriers or latches, bounds every wait, and asserts both permitted outcomes and durable invariants across the final database state.

## Control the schedule, then assert the contract

Use separate connections because one connection serializes commands. Start from known fixtures, coordinate reads and writes at named barriers, and capture values, errors, SQLSTATEs, and commit outcomes. Assert the invariant after every transaction finishes. Repeat enough to detect unsupported assumptions, but never substitute repetition for controlled timing.

> **Tip**
>
> Build a tiny schedule DSL—`A.read`, `B.read`, `A.write`, `B.write`, `commit`—or explicit barriers. The failure report should print the exact interleaving.

> **Common mistake**
>
> Using `sleep(1)` as synchronization. Scheduler load changes the timing; barriers express causality while sleeps only express hope.

![Rowing crew and coxswain coordinating in a racing shell on the water](testing-concurrent-behavior.jpg)
*Rowing crew with coxswain — Columbus Metropolitan Library via DPLA and Wikimedia Commons, public domain in the United States. [Source](https://commons.wikimedia.org/wiki/File:Rowing_crew_with_coxswain_-_DPLA_-_fb2618e96316b77bb9ec12f87c861a00.jpg)*
- **Independent workers** — Each rower represents a separate database session and transaction.
- **Shared barrier** — A named phase aligns both workers before the next operation.
- **Final invariant** — The whole crew's outcome matters, not the apparent success of one worker.

**A deterministic two-session race test**

1. **Reset fixture** — Create one known durable starting state.
2. **Open A and B** — Use independent connections and explicit transactions.
3. **Meet at read barrier** — Both sessions capture the intended snapshot or value.
4. **Release ordered actions** — Latches control writes, commits, and expected waits.
5. **Assert outcomes and invariant** — Check results, SQLSTATEs, final rows, and retry behavior.

*Run it — force a stale-read lost update (Python)*

```python
from threading import Barrier, Event, Lock, Thread

balance = {"value": 100}
read_barrier = Barrier(2)
write_lock = Lock()
first_write_done = Event()

def withdraw(amount, wait_for_first):
    observed = balance["value"]
    read_barrier.wait()
    if wait_for_first:
        first_write_done.wait()
    with write_lock:
        balance["value"] = observed - amount
    if not wait_for_first:
        first_write_done.set()

threads = [Thread(target=withdraw, args=(10, False)), Thread(target=withdraw, args=(20, True))]
for thread in threads: thread.start()
for thread in threads: thread.join()
print("final balance:", balance["value"])
print("correct serial result: 70")

# final balance: 80
# correct serial result: 70
```

*Run it — coordinate the same race (Java)*

```java
import java.util.concurrent.*;
public class Main {
  static int balance = 100;
  static final CyclicBarrier readBarrier = new CyclicBarrier(2);
  static final CountDownLatch firstWriteDone = new CountDownLatch(1);
  static synchronized void publish(int value) { balance = value; }
  static Runnable withdraw(int amount, boolean waitForFirst) {
    return () -> {
      int observed = balance;
      try { readBarrier.await(); } catch (Exception error) { throw new RuntimeException(error); }
      if (waitForFirst) {
        try { firstWriteDone.await(); } catch (InterruptedException error) { throw new RuntimeException(error); }
      }
      publish(observed - amount);
      if (!waitForFirst) firstWriteDone.countDown();
    };
  }
  public static void main(String[] args) throws Exception {
    Thread a = new Thread(withdraw(10, false));
    Thread b = new Thread(withdraw(20, true));
    a.start(); b.start(); a.join(); b.join();
    System.out.println("final balance: " + balance);
    System.out.println("correct serial result: 70");
  }
}
/* final balance: 80
   correct serial result: 70 */
```

### Your first time: Your mission: make a race reproducible

- [ ] Create one minimal fixture — Keep the invariant and expected serial result obvious.
- [ ] Open independent transactions — Give each worker its own connection and explicit boundary.
- [ ] Place barriers around the vulnerable read — Force both sessions to observe the state before either writes.
- [ ] Bound and report every wait — Timeouts should print the phase, session, query, and lock state.

You now own the schedule that exposes the race.

- **The test passes locally but flakes in CI.**
  Replace sleeps with barriers/latches and log the exact phase reached by each worker.
- **No overlap occurs.**
  Verify separate connections, explicit transactions, and a barrier before the contested operation.
- **The test hangs forever.**
  Set transaction, lock, statement, and harness timeouts; dump blockers before cleanup.

### Where to check

- Per-worker connection identity, transaction boundary, and isolation level.
- Barrier/latch phase logs and bounded timeout failures.
- SQLSTATE, commit/rollback result, and retry count.
- Final invariant queried from a fresh connection after workers finish.

### Worked example: a deterministic lost update

1. Balance begins at 100; A withdraws 10 and B withdraws 20.
2. A and B read 100, then wait at the same barrier.
3. Each computes from its stale copy; writes are released one after another.
4. The last write leaves 80 or 90 instead of the serial result 70.
5. A conditional update, row lock, or suitable serializable transaction changes the allowed outcome; the test verifies that contract.

**Quiz.** Why is a barrier stronger than a sleep in a concurrency test?

- [ ] It makes the database faster
- [ ] It guarantees all threads use one connection
- [x] It expresses that participants reached a named phase before release
- [ ] It eliminates the need for timeouts

*A barrier coordinates causality at a specific phase; a sleep only guesses how far another worker has progressed.*

- **Barrier** — A synchronization point that releases participants only after all expected workers arrive.
- **Invariant assertion** — A check of the durable business rule after all concurrent work completes.
- **Allowed outcome** — A result or retry/error explicitly permitted by the selected concurrency contract.

### Challenge

Implement a two-session test for double booking. Force both reads before either reservation, then verify the invariant under the current isolation and after adding the chosen fix.

### Ask the community

> Workers A/B follow `[schedule]` at `[isolation]`; outcomes are `[values/SQLSTATEs]`, while invariant `[rule]` becomes `[state]`. Is the test schedule or product control wrong?

Include connection boundaries, barriers, and timeout diagnostics.

- [PostgreSQL — Transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL — Explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html)

🎬 [Transactions: myths, surprises and opportunities — Martin Kleppmann](https://www.youtube.com/watch?v=5ZjhNTM8XU8) (41 min)

- Concurrency tests need independent sessions and explicit transaction boundaries.
- Barriers and latches control interleavings more reliably than sleeps.
- Assert SQLSTATEs and commit outcomes as well as returned values.
- Check the durable invariant from a fresh connection after workers finish.
- Bound every wait and report the exact phase when a test times out.


## Related notes

- [[Notes/relational-databases-engineer-level/transactions-and-concurrency/isolation-levels-and-anomalies|Isolation levels & anomalies]]
- [[Notes/relational-databases-engineer-level/transactions-and-concurrency/locks-and-deadlocks|Locks & deadlocks]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/transactions-and-concurrency/testing-concurrent-behavior.mdx`_
