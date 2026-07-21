---
title: "Containers in CI"
tags: ["docker-and-containers-for-testers", "containers-in-automation", "continuous-integration", "service-containers"]
updated: "2026-07-17"
---

# Containers in CI

*Use job containers and service containers as explicit, pinned CI dependencies with health gates, bounded resources, durable evidence, and guaranteed cleanup.*

> CI containers are disposable, but failures are not self-explanatory. A useful pipeline pins what ran, waits for dependencies honestly, preserves evidence on failure, and removes resources even when the test command exits early.

> **In real life**
>
> An assembly line gives every unit the same ordered stations, tools, and quality gates. CI containers standardize those stations, while the workflow still controls sequencing, capacity, evidence, and stop conditions.

**job and service containers**: A CI job container supplies the environment in which workflow steps execute. A service container supplies a network dependency such as PostgreSQL or Redis beside that job. Exact network and port behavior depends on whether the job itself runs in a container or directly on the runner.

## Make infrastructure part of the job contract

Pin image tags or digests, declare only required services, and attach health checks that represent usability. In GitHub Actions, a job running in a container can address service containers by their service labels on the shared Docker network; a job running directly on the runner normally reaches published host ports.

Use caches for immutable dependency material, not mutable database state. Give services bounded resources and unique project names. Always upload reports and diagnostic logs with a condition that runs after failure, then clean containers, networks, and volumes.

> **Tip**
>
> Record the workflow revision, image digests, suite command, shard, and service health with the report. “It ran in CI” is not enough to reproduce the environment.

> **Common mistake**
>
> Using `sleep 20` before tests. A fast runner wastes time; a slow database still fails. Poll the protocol or configure a real container health check with a bounded timeout.

![Several cars at different assembly stages on a factory production line with overhead tools and work stations](containers-in-ci.jpg)
*Opel Astra assembly line, General Motors Manufacturing Poland — Marek Ślusarczyk, Wikimedia Commons, CC BY 3.0. [Source](https://commons.wikimedia.org/wiki/File:002_Production_line_-_car_assembly_line_in_General_Motors_Manufacturing_Poland_-_Gliwice,_Poland.jpg)*
- **Pinned inputs** — Each car enters a known station just as a job begins from versioned workflow code and immutable image identity.
- **Ordered gates** — Build, service readiness, migration, test, and report steps run in a visible dependency order.
- **Evidence at exit** — The finished unit leaves with inspection results; CI must publish reports and logs even when the gate fails.

**A container-backed CI job**

1. **Resolve immutable inputs** — Checkout revision, lock files, and pinned image identities define the run.
2. **Start job and services** — The runner creates isolated containers, network, and any declared volumes.
3. **Pass health gates** — Protocol-aware checks prove the application and dependencies are usable.
4. **Run the suite** — The test command returns a trustworthy status and writes durable artifacts.
5. **Publish then clean** — Reports and diagnostics upload regardless of verdict before infrastructure disappears.

*Gate a CI job from explicit stages (Python)*

```python
stages = {
    "images_pinned": True,
    "services_healthy": True,
    "migrations_applied": True,
    "tests_passed": False,
    "artifacts_uploaded": True,
}
blocking = [name for name, passed in stages.items() if not passed and name != "artifacts_uploaded"]
print("verdict=" + ("pass" if not blocking else "fail"))
print("blocking=" + ",".join(blocking))
# verdict=fail
# blocking=tests_passed
```

*Assign collision-free service names (Java)*

```java
import java.util.*;

class Main {
  public static void main(String[] args) {
    List<String> shards = List.of("1", "2", "3");
    Set<String> projects = new LinkedHashSet<>();
    for (String shard : shards) projects.add("ci-842-shard-" + shard);
    if (projects.size() != shards.size()) throw new AssertionError("name collision");
    System.out.println(String.join(",", projects));
  }
}
// ci-842-shard-1,ci-842-shard-2,ci-842-shard-3
```

### Your first time: Add one database service to CI

- [ ] Pin the service image — Use the production-relevant major version and record the resolved identity.
- [ ] Declare networking and health — Use the provider's documented service label or host-port path and a protocol-aware health check.
- [ ] Run migrations and tests — Gate the suite on successful readiness and schema setup; preserve the test exit status.
- [ ] Upload and clean — Publish reports and service logs after pass or fail, then remove owned resources.

- **The service name works locally but not in CI.**
  Check whether steps run inside a job container or on the host runner; the documented network address differs.
- **Parallel jobs attach to the same resources.**
  Namespace Compose projects, container names, networks, volumes, databases, and test data with the run and shard identity.
- **The workflow times out with no useful report.**
  Bound health and test timeouts separately, capture container logs, and upload diagnostics under an always-run condition.
- **A mutable image update changes results without a code change.**
  Pin a version or digest, record the resolved image, and update it through reviewed dependency maintenance.

### Where to check

Inspect workflow revision, runner type and architecture, job-container status, service labels, published ports, health output, image digests, `docker ps`/service logs when available, migration status, test exit code, artifact upload conditions, disk usage, and cleanup steps.

### Worked example: GitHub Actions job with PostgreSQL

Run the job in a pinned test-runner image and declare a pinned PostgreSQL service with `pg_isready` health options. Connect to host `postgres` on internal port `5432`, apply migrations, run tests, and upload JUnit plus service diagnostics under `if: always()`. A host-runner job would instead publish and use a host port, so document which topology the workflow uses.

**Quiz.** In GitHub Actions, how does a step inside a job container normally reach a PostgreSQL service labeled `postgres`?

- [ ] Through `localhost` only
- [x] By the service label `postgres` on the shared job network
- [ ] Through a public internet address
- [ ] By reading the container ID from logs

*Container jobs and their services share a Docker network where service labels provide host names. Host-runner jobs use published ports instead.*

- **Job container** — The container environment in which CI workflow steps execute.
- **Service container** — An ephemeral network dependency created beside a CI job.
- **Always-run artifact step** — Report and diagnostic publication that executes after success or failure.

### Challenge

Build a two-shard CI matrix whose runner and database images are pinned, service names cannot collide, health and test timeouts differ, and each failed shard uploads its own reports and service logs.

### Ask the community

> Provider/runner topology: [value]. Job and service images: [identities]. Address/port: [values]. Health output: [evidence]. Test exit and artifact step: [evidence]. Which contract failed?

Include whether the steps run on the host or inside a job container.

- [GitHub Actions — create PostgreSQL service containers](https://docs.github.com/en/actions/tutorials/use-containerized-services/create-postgresql-service-containers)
- [GitHub Actions — run jobs in a container](https://docs.github.com/en/actions/writing-workflows/choosing-where-your-workflow-runs/running-jobs-in-a-container)
- [Docker Compose — service healthcheck](https://docs.docker.com/reference/compose-file/services/#healthcheck)

🎬 [How to use Container Environment in GitHub Actions | Tutorial](https://www.youtube.com/watch?v=kmBu27D1InU) (4 min)

- CI container topology determines service names and port access.
- Pin and record images, then gate on protocol-aware readiness.
- Namespace resources for parallel jobs and bound their capacity.
- Publish reports and diagnostics before guaranteed cleanup.


## Related notes

- [[Notes/docker-and-containers-for-testers/containers-in-automation/selenium-grid-in-docker|Selenium Grid in Docker]]
- [[Notes/docker-and-containers-for-testers/containers-in-automation/running-your-suite-in-a-container|Running your suite in a container]]
- [[Notes/docker-and-containers-for-testers/containers-in-automation/testcontainers-for-database-fixtures|Testcontainers for database fixtures]]


---
_Source: `packages/curriculum/content/notes/docker-and-containers-for-testers/containers-in-automation/containers-in-ci.mdx`_
