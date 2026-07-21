---
title: "Compose: app and database"
tags: ["docker-and-containers-for-testers", "dockerfiles-and-compose", "track-e"]
updated: "2026-07-17"
---

# Compose: app and database

*Define an application and database as one testable Compose project. Learn service DNS, readiness checks, configuration, data lifetime, and reliable startup and teardown with the current docker compose CLI.*

> Two containers can be running and still fail as a system. The application may call `localhost`, the database may still be replaying recovery logs, or yesterday's volume may quietly preserve today's test data.

> **In real life**
>
> Compose is an orchestra score: it names each service and how they coordinate. `depends_on` cues entry order; a healthcheck tells the conductor whether the database is actually ready to play.

**Compose file**: A YAML configuration, commonly compose.yaml, that declares a multi-container application's services, networks, volumes, configuration, and relationships for the docker compose CLI.

## Model the system, not just two processes

- Give the application and database separate services in `compose.yaml`.
- Inside the default network, connect to the database by service name such as `db`, not `localhost`.
- Keep credentials out of the image and inject test configuration at runtime.
- Add a database healthcheck and require `service_healthy` when startup readiness matters.
- Decide whether a named volume is intentional persistence or a source of test contamination.
- Use the integrated `docker compose` command; the hyphenated `docker-compose` name refers to the legacy standalone tool.

> **Common mistake**
>
> Assuming `depends_on` alone means ready. Basic dependency ordering waits for a container to start, not for PostgreSQL or MySQL to accept the application's real workload.

> **Tip**
>
> Run `docker compose config` before startup. It renders the merged, interpolated model and catches many YAML, environment, and profile surprises without launching a container.

![A conductor leading a seated orchestra](compose-app-and-database.jpg)
*Conducting the Orchestra — Jonjobaker, Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Conducting_the_Orchestra.jpg)*
- **Compose model** — One declared project coordinates service configuration and lifecycle.
- **Application service** — The app reaches dependencies through service DNS names on the project network.
- **Database service** — A healthcheck establishes readiness beyond the mere running state.

**Reliable Compose startup**

1. **Render configuration** — docker compose config resolves variables and validates the model.
2. **Create project network** — Services receive DNS names matching their service keys.
3. **Start database** — The database container enters running state.
4. **Pass healthcheck** — A readiness command proves that the database accepts connections.
5. **Start app and test** — The application uses db as hostname and the suite exercises the stack.

*Run it — evaluate dependency readiness (Python)*

```python
states = {"db": "healthy", "app": "created"}
dependency = "db"
if states[dependency] == "healthy":
    states["app"] = "started"
print("db:", states["db"])
print("app:", states["app"])
print("connection: postgres://db:5432/testdb")

# db: healthy
# app: started
# connection: postgres://db:5432/testdb
```

*Run it — evaluate dependency readiness (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    Map<String, String> states = new LinkedHashMap<>();
    states.put("db", "healthy");
    states.put("app", "created");
    if (states.get("db").equals("healthy")) states.put("app", "started");
    System.out.println("db: " + states.get("db"));
    System.out.println("app: " + states.get("app"));
    System.out.println("connection: postgres://db:5432/testdb");
  }
}
/* db: healthy
   app: started
   connection: postgres://db:5432/testdb */
```

### Your first time: Your mission: launch a clean app-plus-database project

- [ ] Write compose.yaml — Declare app and db services, test-only configuration, and a database healthcheck.
- [ ] Render the model — Run docker compose config and inspect resolved image, build, ports, and variables.
- [ ] Start and observe — Run docker compose up --build --wait, then inspect ps and service logs.
- [ ] Tear down intentionally — Use docker compose down --volumes when the test requires fresh database state.

Repeat the run to prove the setup is deterministic, not lucky.

- **The app gets connection refused while db is running.**
  Use the db service name, add a meaningful healthcheck, require service_healthy, and keep application retry logic.
- **Tests pass locally but see old rows in CI retries.**
  Identify named volumes and tear them down with --volumes or use a unique project name per run.
- **A host port is already allocated.**
  Do not publish internal-only database ports, or choose a dynamic or non-conflicting host mapping.

### Where to check

- `docker compose config` for the effective project model.
- `docker compose ps --all` for service state, health, exit code, and ports.
- `docker compose logs --timestamps app db` for startup chronology.
- `docker compose exec db ...` for database-local readiness and schema checks.

### Worked example: localhost was the wrong computer

1. An API container used `DB_HOST=localhost`, while PostgreSQL ran in the `db` service.
2. Inside the API container, localhost referred to the API container itself, so every connection failed.
3. The team changed the hostname to `db`, added `pg_isready` as a healthcheck, and required `service_healthy`.
4. They removed the database's unnecessary published host port and added application retries for transient reconnects.
5. Two clean `up --wait` and `down --volumes` cycles produced the same passing result.

**Quiz.** What hostname should the app normally use for a Compose database service named db?

- [ ] localhost
- [ ] host.docker.internal in every environment
- [x] db
- [ ] The container's changing IP address

*Compose service discovery makes a service reachable by its service name on the project network.*

- **Service name** — The stable DNS hostname other services use on a Compose network.
- **service_healthy** — A depends_on condition that waits for a dependency's healthcheck to pass.
- **docker compose config** — Renders and validates the effective Compose application model.

### Challenge

Break the database healthcheck deliberately and prove the application does not start as healthy. Restore it and capture the startup sequence from timestamped logs.

### Ask the community

> My Compose app cannot reach `[service]`. The effective hostname, health state, and relevant config are `[details]`. Where is the lifecycle or network mismatch?

Share docker compose config and sanitized logs, not secret values.

- [Docker Docs — Compose quickstart](https://docs.docker.com/compose/gettingstarted/)
- [Docker Docs — Control startup order](https://docs.docker.com/compose/how-tos/startup-order/)

🎬 [Docker Tutorial for Beginners [FULL COURSE in 3 Hours] — TechWorld with Nana](https://www.youtube.com/watch?v=3c-iBn73dDE) (166 min)

- Compose defines the lifecycle and relationships of a multi-container application.
- Service names provide stable container-to-container DNS.
- Running is not ready; healthchecks establish a stronger dependency condition.
- Named volumes preserve data until deliberately removed.
- Use docker compose config, ps, and logs as your first evidence sources.


## Related notes

- [[Notes/docker-and-containers-for-testers/dockerfiles-and-compose/writing-a-dockerfile|Writing a Dockerfile]]
- [[Notes/docker-and-containers-for-testers/dockerfiles-and-compose/multi-stage-builds|Multi-stage builds]]
- [[Notes/docker-and-containers-for-testers/dockerfiles-and-compose/disposable-test-environment|A disposable test environment]]


---
_Source: `packages/curriculum/content/notes/docker-and-containers-for-testers/dockerfiles-and-compose/compose-app-and-database.mdx`_
