---
title: "Parallelism & sharding"
tags: ["playwright", "parallel-and-cross-browser", "track-d"]
updated: "2026-07-16"
---

# Parallelism & sharding

*Workers split a suite across CPU cores on one machine; sharding splits it across entirely separate CI machines when even every core on one machine isn't enough to keep the wait short.*

> A 500-test suite run one file at a time, in order, on a single process is a suite nobody wants to wait
> on. Playwright runs test files across multiple parallel workers by default - and when even every core
> on one machine isn't enough, sharding splits the whole suite across several separate machines running
> at the same time.

> **In real life**
>
> A 1930s bank counter didn't make every customer queue for one single teller. Several windows worked
> side by side - Accountant, Teller, others - each serving a different customer at the same moment, all
> part of the same branch. Workers are exactly that: several parallel positions within one place. When
> even a full row of windows can't keep up with demand, a bank doesn't add infinite windows to one
> counter - it opens an entirely separate branch across town, handling its own share of customers
> independently. That's sharding.

**Parallelism and sharding**: Parallelism in Playwright means running multiple test files simultaneously via worker processes on a single machine - by default, roughly half the available CPU cores, each worker running its own isolated set of browser contexts. Sharding goes a level further: splitting the entire test suite across multiple separate machines (commonly CI runners in a matrix), each running only its assigned slice via --shard=<index>/<total>. Workers parallelize within one machine's resources; sharding parallelizes across multiple machines' resources, and the two are commonly combined - each shard itself running multiple workers.

## Two different levers, for two different limits

- **Workers** (`workers: 4` in config, or `--workers=4` on the command line) — Playwright's test
  runner splits test *files* (not individual tests within a file, by default) across this many
  parallel processes on the current machine. More workers means better use of available CPU cores,
  up to the point where the machine itself runs out of cores or memory.
- **Sharding** (`--shard=2/4`) — splits the *entire suite* into `total` roughly-equal pieces and runs
  only piece number `index` on this invocation. Typically wired into a CI matrix, where each shard is
  a separate job on a separate machine, running concurrently with the others.
- **They compose** — a CI setup with 4 shards, each running 4 workers, gets up to 16-way parallelism
  total, spread across 4 separate machines.
- **A merged report** — each shard produces its own result; CI configs commonly merge them
  (`--reporter=blob` plus a merge step) into one combined report so a failure is visible in one place
  regardless of which shard it ran on.

> **Tip**
>
> Tune workers to the machine actually running them, not a number that "felt right" once - CI runners
> often have fewer cores than a developer laptop, and `workers` set too high for the actual hardware
> causes contention that can make a run slower, not faster.

> **Common mistake**
>
> Assuming sharding alone fixes a suite that's slow because of a few individually slow tests. Sharding
> distributes files across machines evenly by count, not by how long each one takes - a handful of
> disproportionately slow tests landing in the same shard can leave that shard as the long pole even
> with more shards added, until those specific slow tests are addressed directly.

![A 1937 bank banking hall interior showing a row of separate labeled service windows along one long counter, with signs reading ACCOUNTANT and TELLER above glass-partitioned stations, and two clerks working at their windows](parallelism-and-sharding.jpg)
*Tellers windows, Commonwealth Bank Hurstville (Sam Hood, 1937) — Wikimedia Commons, public domain. [Source](https://commons.wikimedia.org/wiki/File:SLNSW_11353_Tellers_windows_Commonwealth_Bank_Hurstville.jpg)*
- **The Accountant's window — one worker process** — A separate, glass-partitioned station handling its own customer independently - the same isolation a Playwright worker process has, running its own set of test files without stepping on another worker's state.
- **The Teller's window, right alongside it** — Working at the exact same moment as the neighboring window, not waiting its turn - this is what 'workers: 4' actually buys: several files genuinely running in parallel, not just queued fast.
- **A third, further window down the counter** — Still the SAME branch, same building, same shared resources (the counter itself) - all workers on one shard still share that machine's CPU and memory ceiling.
- **The customer waiting at the far left** — Even with several windows open, a customer still waits if every window is busy - the same reason workers set too high for the machine's real core count causes contention instead of speed.

**500 test files, from one process to sharded parallelism**

1. **workers: 1 — fully serial** — 500 files, one at a time, one process. The slowest possible baseline.
2. **workers: 4 — parallel on one machine** — Files split across 4 processes on the same CPU, real speedup, bounded by that machine's cores.
3. **--shard=1/4 through 4/4 — split across 4 machines** — Each CI runner gets ~125 files, running independently and concurrently.
4. **Each shard ALSO runs workers: 4** — 16-way parallelism total, spread across 4 separate machines' CPUs.
5. **Reports merge into one** — A single combined result, regardless of which shard or worker actually ran a given file.

Splitting a large batch of independent work first across parallel workers, then across entirely
separate machines when needed, is really just: divide the batch, run pieces concurrently, recombine
the results. Here's that shape as a small, generic simulation.

*Run it - split a batch across workers, then across shards, and recombine results (Python)*

```python
files = [f"test-{i}.spec.ts" for i in range(1, 13)]  # 12 files

def split(items, n):
    size = -(-len(items) // n)  # ceiling division
    return [items[i:i + size] for i in range(0, len(items), size)]

shards = split(files, 3)          # 3 CI machines
for shard_index, shard_files in enumerate(shards, start=1):
    workers = split(shard_files, 2)   # 2 workers per shard
    print(f"shard {shard_index}/3: {len(shard_files)} files across {len(workers)} workers")
    for w, w_files in enumerate(workers, start=1):
        print(f"  worker {w}: {w_files}")

total_parallelism = 3 * 2
print(f"\\nTotal parallel lanes across all shards: {total_parallelism}")
```

Same divide-run-recombine shape in Java.

*Run it - split a batch across workers, then across shards, and recombine results (Java)*

```java
import java.util.*;

public class Main {
    static List<List<String>> split(List<String> items, int n) {
        int size = (int) Math.ceil((double) items.size() / n);
        List<List<String>> chunks = new ArrayList<>();
        for (int i = 0; i < items.size(); i += size) {
            chunks.add(items.subList(i, Math.min(i + size, items.size())));
        }
        return chunks;
    }

    public static void main(String[] args) {
        List<String> files = new ArrayList<>();
        for (int i = 1; i <= 12; i++) files.add("test-" + i + ".spec.ts");

        List<List<String>> shards = split(files, 3); // 3 CI machines
        for (int s = 0; s < shards.size(); s++) {
            List<List<String>> workers = split(shards.get(s), 2); // 2 workers per shard
            System.out.println("shard " + (s + 1) + "/3: " + shards.get(s).size()
                + " files across " + workers.size() + " workers");
            for (int w = 0; w < workers.size(); w++) {
                System.out.println("  worker " + (w + 1) + ": " + workers.get(w));
            }
        }

        System.out.println("\\nTotal parallel lanes across all shards: " + (3 * 2));
    }
}
```

### Your first time: Your mission: measure the real speedup from workers on your own machine

- [ ] Run a scratch suite with npx playwright test --workers=1 and time it — Note the total wall-clock time from the report.
- [ ] Run the exact same suite with the default worker count (no flag) — Time it again and compare.
- [ ] Check how many CPU cores your machine actually has — (nproc on Linux, sysctl -n hw.ncpu on macOS) and compare against Playwright's default worker count.
- [ ] Try an intentionally too-high --workers value (e.g. 20 on a 4-core machine) — Confirm whether it's actually faster or slower than the sensible default - contention is real, not theoretical.

You've now measured, on your own hardware, exactly where parallelism helps and where it stops
helping.

- **Increasing workers made the suite slower, not faster.**
  The machine likely doesn't have enough real CPU cores (or memory) to back that many parallel browser instances - check the actual core count and bring workers back down closer to it.
- **One shard consistently finishes much later than the others.**
  Sharding splits by file COUNT, not by known duration - check whether that shard happened to get an unlucky concentration of the suite's slowest files, and consider addressing those specific tests' speed directly.
- **Tests that pass reliably with workers: 1 start failing intermittently with workers > 1.**
  This usually points to a hidden shared-state or ordering assumption between tests (see test isolation, earlier in this module) that serial execution was accidentally masking.
- **Merging shard reports in CI produces a report with missing or duplicated results.**
  Confirm every shard actually completed and uploaded its report artifact before the merge step runs - a merge step racing ahead of a slow shard is a common cause, not a bug in the merge logic itself.

### Where to check

- **`playwright.config.ts`'s `workers` setting** — the configured default; can be overridden per
  invocation with `--workers=<n>`.
- **CI's matrix/job configuration** — where `--shard=<index>/<total>` actually gets set per parallel
  job, usually driven by the CI matrix index itself.
- **The CI runner's actual core count** (varies by provider/tier) — the real ceiling worker count
  should be tuned against, not a number carried over from a different machine.
- **Per-shard timing in CI logs** — reveals directly whether shards are actually balanced or if one is
  consistently the long pole.

### Worked example: from a 62-minute suite to an 8-minute one, without changing a single test

1. A 600-test suite runs serially in CI: roughly 62 minutes wall-clock, blocking every PR.
2. Step one: enable `workers: 4` (matching the CI runner's actual core count) - the same suite, same
   machine, now finishes in about 18 minutes.
3. Step two: split into 4 shards across 4 separate CI runners in a matrix, each also running 4
   workers - each shard now handles roughly 150 tests across its own 4 workers.
4. Wall-clock time for the full suite drops to about 6-8 minutes, because the 4 shards run
   concurrently on 4 separate machines, not queued one after another.
5. No test code changed at all - the entire improvement came from correctly using two existing,
   independent levers (workers within a machine, shards across machines) instead of one.

**Quiz.** A team doubles their CI shard count from 4 to 8, expecting the suite to run roughly twice as fast, but sees almost no improvement. What's the most likely explanation, based on this note?

- [ ] Sharding doesn't actually provide any real speedup and is purely for organizational convenience
- [x] A small number of individually slow tests may be concentrated in one or two shards - sharding splits by file COUNT, not by known duration, so more shards doesn't help if the bottleneck is a few disproportionately slow files, not the total file count
- [ ] 8 shards is an invalid configuration and Playwright silently falls back to 4
- [ ] Doubling shards requires also doubling the workers config, which the team forgot to do

*The note's mistake callout addresses this exact scenario: sharding is a count-based split, not a duration-aware one, so a handful of slow tests can leave one shard as the bottleneck regardless of how many shards exist overall. Option one is false - the worked example shows a real, large speedup from sharding when it's not bottlenecked this way. Option three is a fabricated technical limitation not mentioned anywhere. Option four conflates two independent settings - workers and shard count are not required to scale together, though tuning both is often worthwhile.*

- **Workers vs sharding - the core difference** — Workers parallelize within ONE machine's CPU cores; sharding parallelizes across MULTIPLE separate machines. They compose: each shard can itself run multiple workers.
- **What does --shard=2/4 mean?** — Run only the second of four roughly-equal pieces the whole suite has been split into - typically one job in a CI matrix.
- **Why can more workers make a run SLOWER?** — If the worker count exceeds what the machine's real CPU/memory can actually support, contention outweighs the parallelism benefit.
- **Why doesn't more sharding always mean proportionally faster CI?** — Sharding splits by file count, not by known test duration - a few very slow tests concentrated in one shard become the bottleneck regardless of total shard count.
- **The bank-counter analogy for workers vs sharding** — Several teller windows working simultaneously in one branch = workers (parallel within one machine); opening an entirely separate branch across town = sharding (parallel across separate machines).

### Challenge

Take a scratch suite (or a real one) and measure wall-clock time at workers=1, then at your machine's
actual core count. Calculate the real speedup ratio (not the theoretical one). Then deliberately add
one artificially slow test (a real 10-second sleep) and re-measure with a HIGH shard count - confirm
whether adding shards alone fixes the bottleneck, or whether the slow test remains the limiting factor
regardless.

### Ask the community

> My CI suite is sharded `[N]` ways with `[M]` workers per shard, and shard `[X]` consistently takes much longer than the others. Here's the timing breakdown: `[paste it]`.

Pasting the actual per-shard timing breakdown usually reveals immediately whether one shard has an
unlucky concentration of slow files, which is fixable by addressing those specific tests rather than
by adding more shards.

- [Playwright — official Parallelism docs](https://playwright.dev/docs/test-parallel)
- [Playwright — official Sharding docs](https://playwright.dev/docs/test-sharding)

🎬 [Playwright Parallel Tests Tutorial (Workers + Sharding) — QA and Dev Tips](https://www.youtube.com/watch?v=1b80XgNmRWk) (14 min)

- Workers parallelize test files across CPU cores on ONE machine; sharding parallelizes across MULTIPLE separate machines - they compose.
- workers should be tuned to the actual machine running them, not a number carried over from different hardware - too high causes contention, not speed.
- --shard=<index>/<total> splits the suite by file COUNT, not by known duration - a few very slow tests can bottleneck one shard regardless of total shard count.
- Flaky-only-when-parallel tests usually reveal a hidden shared-state assumption that serial execution was masking, not a Playwright reliability problem.
- A large real-world speedup (62 minutes to 8) typically comes from combining both levers correctly, not from either alone.


## Related notes

- [[Notes/playwright/parallel-and-cross-browser/projects-and-browsers|Projects & browsers]]
- [[Notes/playwright/parallel-and-cross-browser/retries|Retries]]
- [[Notes/playwright/parallel-and-cross-browser/config|Config]]


---
_Source: `packages/curriculum/content/notes/playwright/parallel-and-cross-browser/parallelism-and-sharding.mdx`_
