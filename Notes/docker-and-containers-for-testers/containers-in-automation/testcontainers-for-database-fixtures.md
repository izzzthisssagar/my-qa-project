---
title: "Testcontainers for Database Fixtures"
tags: ["docker-and-containers-for-testers", "containers-in-automation", "testcontainers", "database-testing"]
updated: "2026-07-17"
---

# Testcontainers for Database Fixtures

*Give integration tests real, disposable database instances with pinned images, readiness-aware startup, isolated state, and explicit lifecycle ownership.*

> A fake database can confirm that your mock returns a row. A disposable real database can expose a broken migration, collation surprise, transaction bug, extension mismatch, or query the production engine rejects.

> **In real life**
>
> A scientist prepares a labeled sample, waits until the instrument is ready, records conditions, runs the experiment, and disposes of contamination safely. Testcontainers applies that lifecycle to infrastructure fixtures.

**Testcontainers**: Testcontainers is a family of libraries that starts Docker-compatible containers from test code, exposes mapped connection details, waits for readiness, and removes resources after the test lifecycle. Database modules add engine-specific convenience around that core lifecycle.

## Own a production-like database boundary

Pin the same database major version and required extensions used by production. Start the container before the tests that own it, obtain its mapped JDBC or network URL from the library, apply real migrations, seed the smallest scenario-specific data, and stop it at the declared lifecycle boundary.

Container startup is not database readiness. Use the module's wait strategy or a meaningful log/SQL check, not a blind sleep. Reuse can accelerate local feedback, but fresh state is the safer default for isolation and CI reproducibility.

> **Tip**
>
> Test behavior through the application repository or API. Use direct SQL for setup and diagnostic evidence only when that bypass is an explicit part of the fixture contract.

> **Common mistake**
>
> Starting one shared PostgreSQL container for the entire developer team. Tests now depend on order, stale rows, local manual fixes, and whoever last changed the schema.

![A laboratory researcher handling labeled sample tools beside a row of small white containers](testcontainers-for-database-fixtures.jpg)
*Sample preparation laboratory — Sofiia Baletska, Wikimedia Commons, CC BY 4.0. [Source](https://commons.wikimedia.org/wiki/File:Sample_preparation_laboratory.jpg)*
- **Pinned fixture** — A labeled database image and migration version define the infrastructure sample under test.
- **Isolated state** — Separate containers or schemas prevent one scenario's rows from contaminating another.
- **Lifecycle controls** — Startup, readiness, seeding, observation, and cleanup belong to the test harness.

**A database integration fixture**

1. **Start pinned image** — The test requests the production-relevant database version and configuration.
2. **Wait for readiness** — The library observes the engine-specific condition instead of sleeping blindly.
3. **Apply migrations** — The same schema evolution path used by deployment creates the database.
4. **Seed one scenario** — Deterministic, minimal data makes failures local and repeatable.
5. **Assert and dispose** — The application is exercised, evidence captured, and owned infrastructure removed.

*Prove fixture isolation with unique databases (Python)*

```python
runs = ["run-41", "run-42", "run-43"]
databases = {run: f"qa_{run.replace('-', '_')}" for run in runs}

assert len(set(databases.values())) == len(runs)
for run, database in databases.items():
    print(f"{run} -> {database}")
# run-41 -> qa_run_41
# run-42 -> qa_run_42
# run-43 -> qa_run_43
```

*Gate tests on migration and readiness (Java)*

```java
import java.util.*;

class Main {
  public static void main(String[] args) {
    Map<String, Boolean> gates = new LinkedHashMap<>();
    gates.put("container-running", true);
    gates.put("database-ready", true);
    gates.put("migrations-applied", true);
    gates.put("seed-loaded", true);
    if (gates.containsValue(false)) throw new AssertionError(gates);
    System.out.println("fixture ready: " + String.join(" -> ", gates.keySet()));
  }
}
// fixture ready: container-running -> database-ready -> migrations-applied -> seed-loaded
```

### Your first time: Test one repository against PostgreSQL

- [ ] Pin the engine image — Match the production major version and declare required extensions and settings.
- [ ] Let the library expose connection data — Use the mapped host, port, database, and credentials returned at runtime.
- [ ] Migrate and seed — Apply real migrations, then insert the minimum deterministic scenario.
- [ ] Assert lifecycle cleanup — Close clients and verify the harness removes owned resources after pass and fail.

- **The first query fails although the container is running.**
  Use an engine-aware readiness strategy; process start and database acceptance are different events.
- **Tests pass locally but CI cannot reach Docker.**
  Verify the runner exposes a supported Docker environment or Testcontainers-compatible provider and inspect provider discovery logs.
- **Parallel tests see each other's rows.**
  Use per-test containers, databases, or schemas and unique resource names; never rely on test order.
- **The test schema differs from deployment.**
  Apply the same migration artifact in the fixture and assert the resulting version before seeding.

### Where to check

Inspect the selected image and digest, Testcontainers provider discovery logs, mapped port and connection URL, wait strategy, container logs, migration version, seed identity, active connections, resource reuse settings, and cleanup/reaper behavior.

### Worked example: A repository test that catches a real SQL defect

Start pinned PostgreSQL, wait for its module readiness, run Flyway migrations, insert two accounts, then call the repository transfer operation. Assert balances and one audit row inside a transaction-visible boundary. A query using a vendor-incompatible function now fails before merge instead of passing against an in-memory substitute.

**Quiz.** Why should the test read the connection URL from Testcontainers instead of assuming port 5432?

- [ ] PostgreSQL changes its internal port
- [x] The host port is dynamically mapped to avoid collisions and must be discovered at runtime
- [ ] JDBC forbids fixed ports
- [ ] Containers do not use TCP

*The database can still listen on its normal internal port while Testcontainers assigns a free host port for isolated concurrent runs.*

- **Mapped port** — A dynamically assigned host port connected to the container's fixed internal service port.
- **Wait strategy** — An observable condition that declares the service ready for tests, not merely started.
- **Fixture ownership** — The test scope responsible for startup, migration, data, clients, and cleanup.

### Challenge

Replace one mocked repository integration test with a pinned database container. Make it apply production migrations, survive parallel execution, and fail if the expected cleanup or schema version is missing.

### Ask the community

> Library/language: [value]. Database image: [tag]. Docker provider: [value]. Wait strategy: [value]. Migration and container logs: [evidence]. Lifecycle scope: [value]. Where does startup fail?

Mask credentials but keep image, provider, mapped-port, and readiness evidence.

- [Testcontainers for Java — database modules](https://java.testcontainers.org/modules/databases/)
- [Testcontainers for Java — JDBC support](https://java.testcontainers.org/modules/databases/jdbc/)
- [Testcontainers for Java — startup and wait strategies](https://java.testcontainers.org/features/startup_and_waits/)

🎬 [Stop Mocking Your Database! Use Testcontainers in .NET](https://www.youtube.com/watch?v=ssRE0pBNvpE) (16 min)

- Use a real production-relevant engine when database behavior is part of the risk.
- Discover mapped connection details and wait for meaningful readiness.
- Apply real migrations and isolate deterministic data per lifecycle.
- Treat Docker provider access and cleanup evidence as part of test reliability.


## Related notes

- [[Notes/docker-and-containers-for-testers/containers-in-automation/selenium-grid-in-docker|Selenium Grid in Docker]]
- [[Notes/docker-and-containers-for-testers/containers-in-automation/running-your-suite-in-a-container|Running your suite in a container]]
- [[Notes/docker-and-containers-for-testers/containers-in-automation/containers-in-ci|Containers in CI]]


---
_Source: `packages/curriculum/content/notes/docker-and-containers-for-testers/containers-in-automation/testcontainers-for-database-fixtures.mdx`_
