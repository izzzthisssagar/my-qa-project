---
title: "Resource use"
tags: ["performance-testing", "metrics", "track-e"]
updated: "2026-07-20"
---

# Resource use

*Response time and error rate say a system is unhappy; resource use says why. CPU saturation and memory saturation look identical from the outside - both make requests queue - but they need opposite fixes, and only the gauges tell them apart.*

> A load test report says "the system got slow at 300 concurrent users." That sentence is true and
> almost useless. Slow HOW - because the app servers ran out of processing power and requests
> queued behind each other, or because memory filled up and the system started swapping and
> garbage-collecting itself into a stall? Both look the same on a response-time graph: a line going
> up. Only the resource-utilization gauges - CPU, memory, disk, network, connections - tell you
> which one actually happened, and the fix for one is close to useless against the other.

> **In real life**
>
> A hotel valet stand outside a casino: a fixed number of parking spots in the lot, and a fixed
> number of valets running back and forth parking and retrieving cars. On a quiet Tuesday morning,
> both have headroom - plenty of open spots, valets standing around waiting for the next car. On a
> packed Saturday night, one of two very different things can go wrong, and from the sidewalk they
> look identical: a line of cars idling by the curb, waiting. Maybe the VALETS are the bottleneck -
> only four of them, each taking three minutes per car, and cars are arriving faster than four
> people can run - that is a CPU-shaped problem, and the fix is more valets or a faster process.
> Or maybe the LOT ITSELF is full - every single spot taken - in which case it does not matter if
> you hire forty more valets, not one more car fits until something leaves. That is a memory-shaped
> problem, and hiring more valets fixes nothing. A doorman who only watches the line of idling cars
> and reports "it's backed up" has told you there is a problem. A doorman who checks how many
> valets are running versus how many spots are actually still open has told you which ONE problem,
> and which fix to reach for first.

**Resource utilization**: Resource use (or resource utilization) is how much of a system's finite capacity - CPU, memory, disk I/O, network bandwidth, connection pools, thread pools - is being consumed while it serves load, usually expressed as a percentage of a known ceiling. Saturation is what happens when a resource's utilization reaches its ceiling: requests that need that resource start queueing or failing, regardless of how healthy every other resource looks. Distinguishing WHICH resource saturated first is the difference between a load test that ends in 'it got slow' and one that ends in a specific, actionable finding, because CPU-bound and memory-bound saturation are different problems requiring different fixes - more parallel processing capacity for one, more space or less retained state for the other.

## Reading gauges, not just symptoms

- **CPU-bound saturation: the workers are the bottleneck.** Processing capacity is maxed out;
  requests queue waiting for a free worker/core. Fix: more parallel workers, faster code on the
  hot path, or fewer CPU-expensive operations per request.
- **Memory-bound saturation: the space is the bottleneck.** A fixed ceiling - RAM, a connection
  pool's max size, a cache's capacity - is full. Fix: free up space (shrink retained state, evict
  faster, fix a leak) or raise the ceiling; adding more processing workers does nothing if the
  workers have nowhere to put their work.
- **From the outside, both look like "it got slow."** Response time climbs, users queue, error
  rates may rise - the SYMPTOM is nearly identical. Only the utilization graphs, read at the same
  moment the symptom appeared, tell CPU-bound apart from memory-bound.
- **Headroom on every OTHER resource does not mean the system is healthy.** A system pegged at
  40% CPU and 45% memory can still be failing - because the bottleneck is a connection pool, disk
  I/O, or a downstream service's own rate limit, resources that a basic dashboard sometimes omits
  entirely.
- **Resource graphs need to be time-aligned with the load profile, not just averaged over the
  whole run.** A single end-of-test average CPU number hides whether saturation happened for two
  minutes at peak or was a steady state for the whole hour - very different findings.

> **Tip**
>
> Capture resource metrics on the SAME timeline as your load and response-time graphs, not as a
> separate end-of-run summary. When response time spikes at minute 14, you want to look at CPU,
> memory, and connection-pool graphs at minute 14 specifically - not a flat average for the whole
> test that dilutes the exact moment something saturated.

> **Common mistake**
>
> Reporting "the server was under load" without naming which resource actually saturated. CPU-bound
> and memory-bound problems get OPPOSITE fixes - adding application server instances helps a
> CPU-bound bottleneck and does nothing for a memory-bound one (more instances each hitting the
> same full connection pool or exhausted downstream service just fails faster, in parallel). A
> finding that does not name the saturated resource sends the fix to a coin flip between two teams,
> one of which is about to spend a sprint on the wrong problem.

![A nighttime street with a red VALET PARKING sign and arrow on a lamp post, a parking lot packed with cars beyond it, one car alone on the street nearby, and illuminated casino towers in the background](resource-use.jpg)
*Valet parking, Main Street Station, Las Vegas, Nevada by night — Pierre Andre Leclercq, Wikimedia Commons, CC BY 4.0. [Source](https://commons.wikimedia.org/wiki/File:Valet_parking,_Main_Street_Station,_Las_Vegas,_Nevada_by_night.jpg)*
- **VALET PARKING - the processing workers** — The service that turns an arriving car into a parked one, one at a time, per valet. This is CPU-shaped: a fixed number of workers, each taking a fixed amount of time per job. Add more valets and this ceiling rises - exactly like adding worker threads or application instances.
- **The packed lot - the fixed capacity ceiling** — However many valets are running, not one more car fits once every spot here is taken. This is memory-shaped: a hard ceiling that more processing power cannot talk its way past. The only fixes are freeing space or raising the ceiling itself.
- **A car alone on the street - the visible symptom** — This is what 'it got slow' looks like from outside: a car waiting. It looks IDENTICAL whether the valets are simply slow tonight (CPU-bound) or the lot is completely full (memory-bound) - the gauges behind the sign are what actually tell those two apart.
- **NO DELIVERIES - protecting capacity on purpose** — A deliberate rule keeping one class of arrivals out during a busy period, so the scarce resource (spots, valet time) stays available for the traffic that matters most. This is exactly what load shedding and rate limiting do for a saturated system - refuse some work on purpose to protect the rest.

**Reading a saturated system - press Play**

1. **Symptom appears: response time climbs, maybe errors rise** — This alone does not say why. CPU-bound and memory-bound saturation produce nearly the same visible symptom - a queue forming somewhere in the system.
2. **Check CPU utilization at that exact moment** — Pegged near 100%? Processing capacity is the bottleneck - the workers cannot keep up with arrivals. This points toward more parallel capacity or faster code on the hot path.
3. **Check memory (and pool/queue) utilization at that exact moment** — Near its ceiling while CPU has headroom? The SPACE is the bottleneck, not the workers. More processing power will not help; something needs to free up or the ceiling needs to rise.
4. **Name the saturated resource in the finding, not just the symptom** — 'CPU-bound at 340 rps' or 'memory-bound once the connection pool hit 100 at 340 rps' - each sentence sends the fix to the right team, on the right problem, immediately.

A valet lot as a load-test dashboard - watch the same rising traffic produce two completely
different verdicts depending on which resource runs out first:

*Run it - CPU-bound vs memory-bound, read from one dashboard (Python)*

```python
# Valet lot: SPOTS is memory-like capacity (a hard ceiling), VALETS is CPU-like throughput
# (workers who fetch/park cars one at a time). A load test's job is telling you WHICH one
# is the bottleneck at each traffic level, before the lot posts "LOT FULL".
SPOTS = 40           # total parking spots - fixed capacity, cannot be exceeded (like memory)
VALETS = 4           # attendants parking cars one at a time (like CPU cores/workers)
PARK_TIME_MIN = 3    # minutes for one valet to park (or retrieve) one car
CAPACITY_PER_HOUR = VALETS * (60 / PARK_TIME_MIN)  # cars/hour the valets can process flat out

def classify(cars_parked, arrivals_per_hour):
    """Return a saturation verdict from current lot state - the same shape as reading
    CPU% and memory% off a load-test dashboard."""
    cpu_utilization = min(1.0, arrivals_per_hour / CAPACITY_PER_HOUR)
    memory_utilization = cars_parked / SPOTS

    if memory_utilization >= 1.0:
        return "MEMORY-BOUND: lot is full - no more cars fit no matter how fast valets work"
    if cpu_utilization >= 0.9:
        return "CPU-BOUND: valets are the bottleneck - cars queue in the fire lane"
    if memory_utilization >= 0.8:
        return "MEMORY PRESSURE: lot nearly full - watch it, do not add more arrivals yet"
    return "HEALTHY: both valets and spots have headroom"

scenarios = [
    ("quiet Tuesday morning", 15, 6),
    ("normal Saturday dinner", 52, 22),
    ("holiday rush, valets slammed", 76, 30),
    ("holiday rush, lot nearly full", 40, 35),
    ("New Year's Eve, lot at capacity", 20, 40),
]

print(f"=== Reading a valet lot like a load-test dashboard ({VALETS} valets, {SPOTS} spots, capacity {CAPACITY_PER_HOUR:.0f} cars/hour) ===")
for label, arrivals, parked in scenarios:
    verdict = classify(parked, arrivals)
    cpu_pct = min(100.0, arrivals / CAPACITY_PER_HOUR * 100)
    mem_pct = parked / SPOTS * 100
    print(f"{label}: {arrivals} cars/hour arriving, {parked}/{SPOTS} spots full "
          f"(CPU {cpu_pct:.0f}%, memory {mem_pct:.0f}%) -> {verdict}")

print()
print("Lesson: 'the system is under load' is not a diagnosis. CPU-bound (add valets / faster")
print("service) and memory-bound (the lot itself is full) need OPPOSITE fixes - a load test that")
print("only reports 'it got slow' without naming which resource saturated sends the fix to the wrong team.")
```

The identical classifier in Java - same five scenarios, same two opposite verdicts:

*Run it - CPU-bound vs memory-bound, read from one dashboard (Java)*

```java
public class Main {
    // Valet lot: SPOTS is memory-like capacity (a hard ceiling), VALETS is CPU-like throughput
    // (workers who fetch/park cars one at a time). A load test's job is telling you WHICH one
    // is the bottleneck at each traffic level, before the lot posts "LOT FULL".
    static final int SPOTS = 40;         // total parking spots - fixed capacity (like memory)
    static final int VALETS = 4;         // attendants parking cars one at a time (like CPU cores)
    static final double PARK_TIME_MIN = 3.0; // minutes for one valet to park (or retrieve) one car
    static final double CAPACITY_PER_HOUR = VALETS * (60.0 / PARK_TIME_MIN); // cars/hour flat out

    // Return a saturation verdict from current lot state - the same shape as reading
    // CPU% and memory% off a load-test dashboard.
    static String classify(int carsParked, double arrivalsPerHour) {
        double cpuUtilization = Math.min(1.0, arrivalsPerHour / CAPACITY_PER_HOUR);
        double memoryUtilization = carsParked / (double) SPOTS;

        if (memoryUtilization >= 1.0) {
            return "MEMORY-BOUND: lot is full - no more cars fit no matter how fast valets work";
        }
        if (cpuUtilization >= 0.9) {
            return "CPU-BOUND: valets are the bottleneck - cars queue in the fire lane";
        }
        if (memoryUtilization >= 0.8) {
            return "MEMORY PRESSURE: lot nearly full - watch it, do not add more arrivals yet";
        }
        return "HEALTHY: both valets and spots have headroom";
    }

    public static void main(String[] args) {
        String[] labels = {
            "quiet Tuesday morning", "normal Saturday dinner", "holiday rush, valets slammed",
            "holiday rush, lot nearly full", "New Year's Eve, lot at capacity"
        };
        int[] arrivals = {15, 52, 76, 40, 20};
        int[] parked = {6, 22, 30, 35, 40};

        System.out.printf("=== Reading a valet lot like a load-test dashboard (%d valets, %d spots, capacity %.0f cars/hour) ===%n",
                VALETS, SPOTS, CAPACITY_PER_HOUR);
        for (int i = 0; i < labels.length; i++) {
            String verdict = classify(parked[i], arrivals[i]);
            double cpuPct = Math.min(100.0, arrivals[i] / CAPACITY_PER_HOUR * 100);
            double memPct = parked[i] / (double) SPOTS * 100;
            System.out.printf("%s: %d cars/hour arriving, %d/%d spots full (CPU %.0f%%, memory %.0f%%) -> %s%n",
                    labels[i], arrivals[i], parked[i], SPOTS, cpuPct, memPct, verdict);
        }

        System.out.println();
        System.out.println("Lesson: 'the system is under load' is not a diagnosis. CPU-bound (add valets / faster");
        System.out.println("service) and memory-bound (the lot itself is full) need OPPOSITE fixes - a load test that");
        System.out.println("only reports 'it got slow' without naming which resource saturated sends the fix to the wrong team.");
    }
}
```

### Your first time: Your mission: find which resource saturates first

- [ ] Set up CPU, memory, and connection/thread-pool graphs before running a load test — Time-aligned with the same clock as your load and response-time graphs - a single end-of-run average is not enough to find a moment-specific bottleneck.
- [ ] Ramp load until response time or error rate visibly degrades — Note the exact timestamp or load level where it happens - this is the moment you need the resource graphs to explain.
- [ ] Read the resource graphs at that exact moment, not the whole-run average — Which one was near its ceiling right then? CPU pegged, memory maxed, a pool exhausted - name the specific resource.
- [ ] Write the finding as 'X-bound at Y load', not 'it got slow' — 'CPU-bound at 340 rps' or 'memory-bound once the connection pool hit 100 at 340 rps' - specific enough that the right team can act on it immediately.

You now have a resource-utilization finding that names a cause, not just a symptom - and points
whoever picks up the ticket at the correct fix on the first try.

- **Response time degrades under load but CPU and memory both look healthy on the dashboard.**
  Check less obvious resources: connection pool size, thread pool size, file descriptor limits, disk I/O, or a downstream service's own rate limit. 'The server' has more finite resources than just CPU and memory, and a pool or limit maxing out produces the exact same queueing symptom.
- **Adding more application server instances did not fix a slowdown found under load.**
  This is the classic sign the bottleneck was memory-bound (or otherwise a shared, fixed resource) rather than CPU-bound - more instances each hitting the same full connection pool, the same exhausted downstream service, or the same disk simply fail in parallel instead of one at a time. Confirm which resource actually saturated before adding more workers again.
- **Resource graphs show healthy averages for the whole test, but users reported real slowness during the run.**
  An end-of-run average can hide a short, sharp saturation spike the same way a blended error rate can. Re-examine the resource graphs at the exact timestamp of the reported slowness, not the whole-run summary - a two-minute CPU spike to 100% averages out to something unremarkable over an hour-long test.
- **A report says 'the server was under load' with no resource named.**
  Ask which specific resource was at or near its ceiling when the symptom appeared. Without a named resource, 'under load' could mean CPU, memory, disk, network, or a pool - each pointing at a different team and a different fix, so the sentence has not actually diagnosed anything yet.

### Where to check

- **Infrastructure monitoring during the exact load-test window** — CPU, memory, disk I/O, and network graphs time-aligned with the load profile, not just an end-of-run summary.
- **Connection pool, thread pool, and queue-depth metrics specifically** — frequently the actual bottleneck when CPU and memory both look fine.
- **Downstream service dashboards, not just your own system's** — a downstream API's own rate limit or capacity can saturate before anything in your own infrastructure does.
- **[[performance-testing/metrics/latency-and-throughput]]** — once a resource is found saturating, this is where you connect it back to the throughput ceiling it is causing.

### Worked example: the fix that made things worse

1. A team's checkout API slows down sharply past 300 concurrent users. The on-call engineer's
   fix, based on past experience: add two more application server instances. Response time under
   the same load barely improves.
2. A tester pulls the resource graphs from the original test, time-aligned to the exact moment
   response time started climbing. CPU utilization at that point was a comfortable 55% - nowhere
   near saturated. The database connection pool, however, was pinned at its configured maximum of
   50 connections from just before the slowdown onward.
3. This was memory/resource-bound, not CPU-bound - the extra application instances simply gave
   more processes a chance to compete for the same 50 already-exhausted database connections,
   which is exactly why adding instances barely moved the needle.
4. The real fix: raise the connection pool's maximum (after confirming the database itself has
   headroom for more connections) and add basic connection-pool utilization to the always-on
   dashboard, not just CPU and memory.
5. Retested at 300 concurrent users: response time stays flat, connection pool utilization peaks
   around 70% instead of pinning at 100%. The team's new rule: no "it got slow" finding closes
   without naming the specific resource that saturated first.

**Quiz.** Under load, a service's response time climbs sharply. CPU sits at 40% and memory at 35% throughout - both comfortable - but a database connection pool configured for 20 connections is pinned at 20 from the moment the slowdown starts. What is the most accurate finding?

- [ ] The service is CPU-bound and needs more processing power
- [ ] The service is memory-bound and needs more RAM
- [x] The service is bound by the connection pool - a fixed-capacity resource distinct from CPU and memory - and needs the pool size (or database capacity) addressed, not more compute
- [ ] The metrics are contradictory and the test should be discarded as unreliable

*CPU and memory both having headroom rules out options A and B directly - there is no processing or memory pressure to point at. The metrics are not contradictory (option D); they are telling a complete, consistent story: a THIRD kind of finite resource, the connection pool, hit its ceiling exactly when the slowdown began. This is exactly the scenario the note warns about - resource use is not only CPU and memory, and a pool, queue, or downstream limit can saturate while the two most commonly checked gauges look perfectly healthy. The fix targets the pool (or the database capacity behind it), not compute - adding more CPU or RAM here would not free up a single additional connection.*

- **Resource use / utilization** — How much of a system's finite capacity (CPU, memory, disk, network, connection/thread pools) is consumed while serving load, usually as a percentage of a known ceiling.
- **Saturation** — When a resource's utilization hits its ceiling - requests needing that resource queue or fail, regardless of how healthy every other resource looks.
- **CPU-bound vs memory-bound** — CPU-bound: the workers/processing power are the bottleneck (fix: more parallel capacity or faster code). Memory-bound: a fixed space ceiling is full (fix: free space or raise the ceiling) - opposite fixes, identical outward symptom.
- **Why 'it got slow' is not a diagnosis** — The symptom (climbing response time, growing queues) looks nearly identical whichever resource saturated - only the utilization gauges, read at that exact moment, tell the causes apart.
- **Resources beyond CPU and memory** — Connection pools, thread pools, disk I/O, network bandwidth, file descriptors, and downstream services' own rate limits - all finite, all capable of saturating while CPU/memory look healthy.
- **Why resource graphs need time-alignment** — A whole-run average can hide a short, severe saturation spike; read the gauges at the exact timestamp the symptom appeared, not a flattened summary.

### Challenge

Take a system you have monitoring access to (or a load test you can rerun) and, the next time
response time or error rate degrades under load, name the SPECIFIC resource that was saturating at
that exact moment - not just "the server was slow." Check CPU, memory, and at least one
pool/queue/connection metric, and write one sentence in the form `X-bound at Y load` describing
what you found, plus the one fix you would try first.

### Ask the community

> Under load, my `[service/flow]` degrades once traffic passes `[N]` - CPU and memory both look `[healthy/pegged/whatever you found]`. What other resource (pool, queue, downstream limit) would you check next, and how did you confirm which one was the actual bottleneck the last time you saw this pattern?

Naming which of the obvious gauges (CPU, memory) already looked fine tends to get you straight to
the less obvious resource other testers have found behind the same pattern - connection pools and
downstream rate limits come up often enough to be worth asking about directly.

- [TestGuild — Resource Monitoring Basics: CPU and Memory in Performance Testing](https://testguild.com/performance-test-resource-utilization/)
- [BlazeMeter — Performance Testing Metrics](https://www.blazemeter.com/blog/performance-testing-metrics)
- [Load Testing for Beginners: Performance Testing & Capacity Planning](https://www.youtube.com/watch?v=u94cVdHgIcQ)

🎬 [Load Testing for Beginners: Performance Testing & Capacity Planning](https://www.youtube.com/watch?v=u94cVdHgIcQ) (6 min)

- Response time and error rate say a system is unhappy under load; resource-utilization gauges say why - and only the gauges point at the correct fix.
- CPU-bound (workers maxed) and memory-bound (space maxed) saturation produce the same outward symptom but need opposite fixes.
- Healthy CPU and memory do not mean a system is healthy - connection pools, thread pools, disk I/O, and downstream limits are all finite resources that can saturate too.
- Resource graphs need to be time-aligned with the load and response-time graphs; a whole-run average can hide a short, severe saturation spike.
- 'The system got slow' is a symptom, not a finding - a real finding names the specific resource that saturated first.


## Related notes

- [[Notes/performance-testing/metrics/latency-and-throughput|Latency & throughput]]
- [[Notes/performance-testing/metrics/error-rate|Error rate]]
- [[Notes/performance-testing/load-vs-stress-vs-soak/scalability|Scalability]]


---
_Source: `packages/curriculum/content/notes/performance-testing/metrics/resource-use.mdx`_
