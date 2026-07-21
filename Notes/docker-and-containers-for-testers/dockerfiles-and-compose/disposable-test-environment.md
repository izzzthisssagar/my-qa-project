---
title: "Disposable test environment"
tags: ["docker-and-containers-for-testers", "dockerfiles-and-compose", "track-e"]
updated: "2026-07-17"
---

# Disposable test environment

*Create a fresh containerized environment for each test run, wait for genuine readiness, preserve failure evidence, and destroy resources without leaking state into the next run.*

> A test environment that remembers yesterday is not reproducible; it is a mystery novel. Disposable does not mean careless—it means every run declares its inputs, captures its evidence, and owns its cleanup.

> **In real life**
>
> A disposable cup is created for one bounded use and then removed. A disposable test stack likewise gets a unique identity, known fixture, finite lifetime, and no authority over the next run.

**disposable test environment**: An isolated stack created from declared images and configuration for a bounded test run, then removed with its writable state after logs and reports have been captured.

## Make freshness an enforceable property

- Assign every run a unique Compose project name or let a test library own container identity.
- Pin dependency image versions so freshness does not become uncontrolled drift.
- Wait for service-specific readiness, not a fixed sleep and not merely container start.
- Apply migrations and seed the smallest deterministic fixture after readiness.
- Capture logs, inspect output, test reports, and relevant diagnostics before teardown.
- Clean up in a guaranteed finalizer path, including volumes and orphaned services where appropriate.

> **Common mistake**
>
> Using `sleep 10` as readiness. It is simultaneously too long on fast machines and too short on slow ones, producing wasted time and intermittent failures.

> **Tip**
>
> Cleanup belongs in `finally` or an equivalent always-run CI step. On failure, collect evidence first; otherwise teardown turns the most useful debugging state into silence.

![A crushed disposable plastic drink cup on pavement](disposable-test-environment.jpg)
*Smoothie King crushed plastic cup — Ser Amantio di Nicolao, Wikimedia Commons, CC0. [Source](https://commons.wikimedia.org/wiki/File:Smoothie_King_crushed_plastic_cup.jpg)*
- **One bounded run** — The environment belongs to one test execution and receives a unique identity.
- **Evidence before disposal** — Logs and reports must leave the environment before cleanup destroys it.
- **No residue** — Containers, networks, and unintended volumes must not contaminate the next run.

**Lifecycle of an ephemeral test stack**

1. **Allocate unique identity** — A project name prevents parallel runs from sharing resources.
2. **Create pinned dependencies** — Declared image versions make the environment reproducible.
3. **Wait, migrate, and seed** — Readiness precedes deterministic data setup.
4. **Run tests** — The suite talks to real isolated dependencies.
5. **Capture then destroy** — Evidence is exported before containers, networks, and state are removed.

*Run it — guarantee evidence and cleanup (Python)*

```python
events = []
try:
    events += ["create run-42", "wait healthy", "seed fixture", "run tests"]
    raise RuntimeError("assertion failed")
except RuntimeError:
    events.append("capture logs")
finally:
    events.append("remove run-42")
print(" -> ".join(events))

# create run-42 -> wait healthy -> seed fixture -> run tests -> capture logs -> remove run-42
```

*Run it — guarantee evidence and cleanup (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    List<String> events = new ArrayList<>();
    try {
      events.addAll(List.of("create run-42", "wait healthy", "seed fixture", "run tests"));
      throw new RuntimeException("assertion failed");
    } catch (RuntimeException failure) {
      events.add("capture logs");
    } finally {
      events.add("remove run-42");
    }
    System.out.println(String.join(" -> ", events));
  }
}
/* create run-42 -> wait healthy -> seed fixture -> run tests -> capture logs -> remove run-42 */
```

### Your first time: Your mission: prove two independent runs

- [ ] Create a unique project identity — Include the CI run or worker identifier so parallel suites cannot collide.
- [ ] Wait and seed deterministically — Probe the actual service, apply migrations, and load a minimal known fixture.
- [ ] Fail one assertion deliberately — Confirm logs and reports are exported while the stack still exists.
- [ ] Tear down and rerun — Remove volumes if state is meant to be ephemeral, then prove the next run starts clean.

A second identical run is stronger evidence than one clean-looking dashboard.

- **Parallel jobs connect to each other's services.**
  Use unique project names and avoid fixed container names or shared host ports.
- **The first test after startup flakes.**
  Replace sleeps with a protocol-aware readiness probe and seed only after it passes.
- **Disk usage grows after every pipeline.**
  Audit cleanup paths, named volumes, build cache policy, and abandoned resources from canceled jobs.

### Where to check

- `docker compose -p RUN_ID ps --all` for resources owned by one run.
- Timestamped service logs and health status before teardown.
- `docker volume ls` and `docker network ls` for leaked run-scoped resources.
- CI artifacts to confirm reports and logs survive after cleanup.

### Worked example: the parallel suites that shared a database

1. Four CI workers all used the default project directory name and published PostgreSQL on host port 5432.
2. Jobs collided on the port; retries sometimes connected to a surviving database with another worker's rows.
3. The team assigned a unique project name, removed the unnecessary host port, and connected through service DNS.
4. Each run applied migrations, seeded its own fixture, exported logs, and ran `down --volumes --remove-orphans` in an always-run cleanup step.
5. Cancellation tests confirmed that no run-scoped container, network, or volume remained.

**Quiz.** What should happen immediately before a failing disposable environment is destroyed?

- [ ] Pull latest images
- [x] Capture diagnostic evidence
- [ ] Reuse its volume for the next run
- [ ] Rename its container

*Logs, reports, health state, and diagnostics must be exported before teardown removes the state needed to investigate failure.*

- **Run identity** — A unique project or resource prefix that isolates one execution from parallel work.
- **Readiness probe** — A service-specific check proving the dependency can perform required work.
- **Guaranteed cleanup** — Teardown placed in finally or an always-run CI step so failures do not leak resources.

### Challenge

Terminate a test job midway, then audit containers, networks, and volumes. Strengthen cleanup until both ordinary failure and cancellation leave no run-owned resources.

### Ask the community

> My disposable stack leaks `[resource]` after `[failure mode]`. Creation identity, artifact capture, and cleanup commands are `[details]`. Which lifecycle edge is unowned?

Include sanitized CI control flow and resource labels.

- [Docker Docs — docker compose down](https://docs.docker.com/compose/reference/down/)
- [Testcontainers — Startup and wait strategies](https://java.testcontainers.org/features/startup_and_waits/)

🎬 [Realistic Tests with Testcontainers — Grafana Office Hours #20](https://www.youtube.com/watch?v=LtlRvmWzCRE) (69 min)

- A disposable environment has one run identity and a bounded lifecycle.
- Pinned images and deterministic fixtures make fresh runs comparable.
- Readiness probes outperform fixed sleeps.
- Failure evidence must be exported before teardown.
- Guaranteed cleanup prevents cross-run contamination and resource leaks.


## Related notes

- [[Notes/docker-and-containers-for-testers/dockerfiles-and-compose/writing-a-dockerfile|Writing a Dockerfile]]
- [[Notes/docker-and-containers-for-testers/dockerfiles-and-compose/multi-stage-builds|Multi-stage builds]]
- [[Notes/docker-and-containers-for-testers/dockerfiles-and-compose/compose-app-and-database|Compose: app + database]]


---
_Source: `packages/curriculum/content/notes/docker-and-containers-for-testers/dockerfiles-and-compose/disposable-test-environment.mdx`_
