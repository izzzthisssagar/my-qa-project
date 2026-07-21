---
title: "Environment variables and networks"
tags: ["docker-and-containers-for-testers", "docker-hands-on", "track-e"]
updated: "2026-07-17"
---

# Environment variables and networks

*Inject non-secret configuration deliberately and connect containers through user-defined networks using service names instead of brittle container IP addresses.*

> A container should call `db:5432`, not yesterday's `172.18.0.4`. Names express service identity; container IPs are disposable implementation details.

> **In real life**
>
> A user-defined Docker network is an office directory: colleagues find “db” by name even when desks move. Environment variables are the day's configuration sheet, not a secure vault.

**runtime configuration plane**: A user-defined bridge network gives attached containers isolated connectivity and Docker-managed DNS by container name or network alias. Environment variables provide runtime process configuration but can be exposed through inspection and process context.

## Configure without coupling

- Create a user-defined network and attach only services that need to communicate.
- Address peers by container name or explicit network alias.
- Use `-e NAME=value` or `--env-file` for non-secret runtime configuration.
- Do not commit env files containing credentials or print them in diagnostics.
- Use the platform's secret mechanism for sensitive values and rotate exposed credentials.

> **Tip**
>
> Assert configuration names and safe values at startup, then redact secrets. A missing variable should fail clearly before tests time out.

> **Common mistake**
>
> Using `localhost` from one container to reach another. Inside the container, localhost means that same container.

![A container crane beside stacked freight containers at Oakland Seaport](environment-variables-and-networks.jpg)
*Container crane at Oakland Seaport — Cullen328, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Container_crane_at_the_Oakland_Seaport.jpg)*
- **Named services** — Stable names identify peers while individual container addresses change.
- **Shared network** — Only attached containers participate in this communication boundary.
- **Runtime settings** — Each workload receives configuration appropriate to the test run.

**A service-to-database connection**

1. **Read DB_HOST=db** — Runtime configuration supplies the logical service name.
2. **Docker DNS resolves db** — The user-defined network returns a current container address.
3. **Connect to container port** — Peer traffic uses the database's internal listening port.
4. **Emit redacted diagnostics** — Logs report endpoint and outcome without credentials.

*Run it — validate safe runtime configuration (Python)*

```python
env = {"DB_HOST": "db", "DB_PORT": "5432", "DB_PASSWORD": "secret"}
required = ["DB_HOST", "DB_PORT"]
print("missing=" + str([key for key in required if not env.get(key)]))
print(f'endpoint={env["DB_HOST"]}:{env["DB_PORT"]}, password=REDACTED')

# missing=[]
# endpoint=db:5432, password=REDACTED
```

*Run it — validate safe runtime configuration (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    Map<String,String> env = Map.of("DB_HOST", "db", "DB_PORT", "5432", "DB_PASSWORD", "secret");
    List<String> missing = new ArrayList<>();
    for (String key : List.of("DB_HOST", "DB_PORT")) if (!env.containsKey(key)) missing.add(key);
    System.out.println("missing=" + missing);
    System.out.println("endpoint=" + env.get("DB_HOST") + ":" + env.get("DB_PORT") + ", password=REDACTED");
  }
}
/* missing=[]
   endpoint=db:5432, password=REDACTED */
```

### Your first time: Your mission: connect two named services

- [ ] Create a user-defined bridge network — Give the test run a unique network name.
- [ ] Run a dependency named db — Do not publish its port unless the host needs access.
- [ ] Run a client with DB_HOST=db — Attach it to the same network and resolve by name.
- [ ] Inspect and remove the network — Prove membership and cleanup after capturing evidence.

You have replaced a disposable IP with a declared service relationship.

- **The service cannot resolve its peer name.**
  Confirm both containers share the same user-defined network and the expected name or alias exists.
- **The app connects to itself.**
  Replace localhost with the peer's network name and internal port.
- **A secret appears in logs or inspect output.**
  Rotate it, remove logging, and use an appropriate secrets mechanism rather than plain environment injection.

### Where to check

- `docker network inspect NETWORK` for members and aliases.
- Container inspect output for attached networks and safe configuration names.
- `getent hosts NAME` or application DNS diagnostics inside the client.
- Application bind address and the peer's internal port.

### Worked example: the hard-coded IP failure

1. A test stores a database container IP from yesterday's run.
2. Recreation assigns the database a different address.
3. The application times out against the stale IP.
4. QA creates a user-defined network and configures `DB_HOST=db`.
5. Docker DNS resolves the current peer on every recreation.

**Quiz.** From an app container, what does `localhost` identify?

- [ ] The Docker host
- [ ] Every container on the network
- [x] That same app container
- [ ] The first database container

*Each container has its own network namespace; use the peer's network name to reach another container.*

- **Network alias** — A DNS name for a container on a specific Docker network.
- **Internal port** — The port where the peer process listens inside its network namespace.
- **Environment variable** — Runtime process configuration, not inherently secret storage.

### Challenge

Prove a service can be removed and recreated at a new IP while its peer continues to reach it by network name.

### Ask the community

> Containers `[names]` share networks `[networks]`; lookup of `[name]` returns `[result]`; target listens on `[address:port]`. Where is the break?

Redact credentials and tokens.

- [Docker Docs — Bridge network driver](https://docs.docker.com/engine/network/drivers/bridge/)
- [Docker Docs — Set environment variables](https://docs.docker.com/reference/cli/docker/container/run/#env)

🎬 [Docker Tutorial for Beginners [FULL COURSE in 3 Hours] — TechWorld with Nana](https://www.youtube.com/watch?v=3c-iBn73dDE) (166 min)

- User-defined networks provide scoped connectivity and DNS.
- Use service names, not disposable container IP addresses.
- Localhost refers to the current container.
- Environment variables are visible configuration and require secret discipline.


## Related notes

- [[Notes/docker-and-containers-for-testers/docker-hands-on/ports-and-volumes|Ports & volumes]]
- [[Notes/docker-and-containers-for-testers/docker-hands-on/debugging-a-container|Debugging a container]]
- [[Notes/docker-and-containers-for-testers/containers-in-plain-words/why-qa-cares|Why QA cares]]


---
_Source: `packages/curriculum/content/notes/docker-and-containers-for-testers/docker-hands-on/environment-variables-and-networks.mdx`_
