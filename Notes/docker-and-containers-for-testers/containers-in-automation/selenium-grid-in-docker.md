---
title: "Selenium Grid in Docker"
tags: ["docker-and-containers-for-testers", "containers-in-automation", "selenium-grid", "docker"]
updated: "2026-07-17"
---

# Selenium Grid in Docker

*Run Selenium Grid as disposable, version-pinned containers while preserving network reachability, browser capacity, observability, and failure evidence.*

> A Grid container is not a browser vending machine on `localhost`. It is a small distributed system: the test client, Grid, browser node, and application must agree on names, ports, capacity, and cleanup.

> **In real life**
>
> A server rack holds different machines behind one cabinet, but each unit still needs power, a network address, capacity, and monitoring. A containerized Grid packages the units; it does not erase those operational contracts.

**Selenium Grid**: Selenium Grid routes WebDriver sessions from test clients to compatible browser nodes. In the official Docker images, a standalone container combines the Grid roles, while hub-and-node or distributed deployments separate them for scale and control.

## Build the smallest honest Grid

Start with an official standalone browser image for local work. Put Grid, the test runner, and any containerized application on a user-defined Docker network, then address services by container or Compose service name. Pin a complete Selenium image tag instead of `latest`; browser and driver compatibility belongs in version control.

- Publish Grid port `4444` only when the host needs it; containers on the same network use the internal port.
- Wait for `/status` to report readiness before creating a session.
- Set shared-memory capacity deliberately; browser crashes often masquerade as Selenium failures.
- Match session concurrency to CPU and memory. More nodes do not create more host capacity.
- Preserve Grid logs, browser console evidence, and video only when they help diagnose a failed run.

> **Tip**
>
> Use `http://selenium:4444/wd/hub` from a sibling container named `selenium`. Inside that test container, `localhost` means the test container itself.

> **Common mistake**
>
> Scaling browser nodes while leaving the application URL as `http://localhost:3000`. Every node then looks for the application inside itself and reports a misleading connection failure.

![A rack containing several visibly different servers, storage devices, and network appliances](selenium-grid-in-docker.jpg)
*Rack with various servers — Patrick Finnegan, Wikimedia Commons, CC BY-SA 2.0. [Source](https://commons.wikimedia.org/wiki/File:Rack_with_varoius_servers.jpg)*
- **Grid router** — One public WebDriver endpoint accepts new-session requests and routes them to suitable capacity.
- **Browser nodes** — Separate units represent browser capacity; each needs a compatible image, CPU, memory, and a reachable application URL.
- **Shared network** — The rack wiring mirrors the Docker network that lets runner, Grid, nodes, and application resolve stable service names.

**A remote WebDriver session**

1. **Grid becomes ready** — The runner polls the status endpoint rather than sleeping a guessed number of seconds.
2. **Client requests capabilities** — The test asks the Grid endpoint for a browser and platform combination.
3. **Grid reserves a slot** — A compatible node receives the session if capacity exists.
4. **Browser reaches the app** — The node resolves the application by a network-reachable host name.
5. **Evidence survives teardown** — The suite captures useful artifacts before Compose removes the disposable Grid.

*Plan Grid capacity from host limits (Python)*

```python
requests = ["chrome", "firefox", "chrome", "chrome", "firefox"]
slots = {"chrome": 2, "firefox": 1}
active = {browser: 0 for browser in slots}
waves = []

while requests:
    wave = []
    for browser in list(requests):
        if active[browser] < slots[browser]:
            active[browser] += 1
            wave.append(browser)
            requests.remove(browser)
    waves.append(wave)
    active = {browser: 0 for browser in slots}

print(waves)
# [['chrome', 'firefox', 'chrome'], ['chrome', 'firefox']]
```

*Reject an unreachable Grid topology (Java)*

```java
import java.util.*;

class Main {
  public static void main(String[] args) {
    Map<String, String> endpoints = Map.of(
      "grid", "http://selenium:4444",
      "app", "http://web:3000"
    );
    boolean usesContainerLocalhost = endpoints.values().stream()
      .anyMatch(value -> value.contains("localhost") || value.contains("127.0.0.1"));
    if (usesContainerLocalhost) throw new AssertionError("container-local endpoint");
    System.out.println("reachable service names: " + new TreeSet<>(endpoints.keySet()));
  }
}
// reachable service names: [app, grid]
```

### Your first time: Run one disposable browser session

- [ ] Pin the official image — Choose a complete selenium/standalone-* tag and record it with the suite.
- [ ] Create one named network — Give Grid, runner, and application stable service names on the same network.
- [ ] Gate on readiness — Poll Grid status until ready, then request one session.
- [ ] Capture and remove — Save failure evidence, quit the driver, and tear down containers and volumes.

- **The runner cannot connect to `localhost:4444`.**
  From another container use the Grid service name and internal port; publish a host port only for host clients.
- **Sessions queue or time out under parallel load.**
  Compare requested concurrency with node slots and host CPU/memory; cap parallelism before adding nodes.
- **Chrome exits with an unexplained renderer crash.**
  Inspect container memory and shared-memory configuration, then retain browser and Grid logs.
- **The browser opens but cannot reach the application.**
  Test DNS and HTTP reachability from the browser node's network namespace, not from the host.

### Where to check

Inspect `http://localhost:4444/status` from the host or `http://selenium:4444/status` on the Docker network, Grid logs, container health, `docker stats`, session queue, node slots, resolved application URL, and saved browser evidence.

### Worked example: Two-browser smoke suite on Compose

Define `selenium-chrome`, `selenium-firefox`, `web`, and `tests` services on one network. Pin all images. Gate the test runner on Grid and application health. Set remote URLs by service name, run only two sessions because the laptop has two reliable browser slots, export JUnit and screenshots, then tear the project down with orphan removal.

**Quiz.** Why does `http://localhost:3000` usually fail when a browser runs in a Selenium container?

- [ ] Docker blocks HTTP
- [x] Localhost identifies the browser container, not the host or application container
- [ ] Selenium supports only HTTPS
- [ ] Port 3000 is reserved

*Every container has its own network namespace. Use a reachable host gateway or, preferably, a service name on a shared Docker network.*

- **Standalone Grid** — One container combines Grid roles and one browser family; useful for small, disposable runs.
- **Service name** — Stable DNS name assigned on a Docker network and used for container-to-container traffic.
- **Session slot** — A unit of browser execution capacity; parallel demand above available slots queues.

### Challenge

Write a Compose topology for Chrome and Firefox with pinned images, health gates, explicit capacity, one shared network, and failure artifact mounts. Explain every published port.

### Ask the community

> Grid image tags: [versions]. Runner URL: [value]. Application URL as seen by node: [value]. Slots/requested concurrency: [values]. Status and logs: [evidence]. What boundary is failing?

Include the point of view—host, runner container, or browser node—because `localhost` changes meaning.

- [Selenium — Grid documentation](https://www.selenium.dev/documentation/grid/)
- [SeleniumHQ — official Docker Selenium images](https://github.com/SeleniumHQ/docker-selenium)
- [Docker — networking in Compose](https://docs.docker.com/compose/how-tos/networking/)

🎬 [Selenium Grid with Docker: Setup, Framework Integration & Live Demo (2025)](https://www.youtube.com/watch?v=5VUReeHTid8) (14 min)

- A containerized Grid remains a distributed system with explicit network and capacity contracts.
- Use pinned official images, service-name DNS, and readiness checks.
- Size session concurrency to real host resources and node slots.
- Capture evidence before disposable infrastructure is removed.


## Related notes

- [[Notes/docker-and-containers-for-testers/containers-in-automation/running-your-suite-in-a-container|Running your suite in a container]]
- [[Notes/docker-and-containers-for-testers/containers-in-automation/testcontainers-for-database-fixtures|Testcontainers for database fixtures]]
- [[Notes/docker-and-containers-for-testers/containers-in-automation/containers-in-ci|Containers in CI]]


---
_Source: `packages/curriculum/content/notes/docker-and-containers-for-testers/containers-in-automation/selenium-grid-in-docker.mdx`_
