---
title: "Debugging a container"
tags: ["docker-and-containers-for-testers", "docker-hands-on", "track-e"]
updated: "2026-07-17"
---

# Debugging a container

*Triage container failures from state, logs, inspect data, resource signals, networking, and image identity before changing the environment.*

> The fastest way to destroy a container failure is to restart it before recording its exit code, error, logs, mounts, network, and image digest.

> **In real life**
>
> Debugging is an incident scene: photograph state before moving objects. A restart may restore service while erasing the sequence that explains the defect.

**evidence-first triage**: Evidence-first container triage captures immutable identity, runtime configuration, state transition, process output, resource use, and connectivity before any mutation or replacement.

## A bounded triage order

1. `docker ps -a` — locate the object and current state.
2. `docker inspect` — capture image, command, environment names, mounts, networks, health, error, OOM flag, and exit code.
3. `docker logs --timestamps` — align application output with the failure.
4. `docker stats --no-stream` and daemon events — check resource and lifecycle signals.
5. If running, use `docker exec` for read-only process, DNS, filesystem, and socket probes.

> **Tip**
>
> Save raw inspect JSON and logs as artifacts, then derive a human summary. Summaries alone omit the field you need next time.

> **Common mistake**
>
> Installing tools or editing config inside the failed container. You change the evidence and create a state that nobody can reproduce.

![Aerial view of a container terminal with organized rows of freight containers](debugging-a-container.jpg)
*Container terminal from above — chuttersnap, CC0 1.0. [Source](https://commons.wikimedia.org/wiki/File:Container_terminal_from_above_(Unsplash).jpg)*
- **Preserve identity** — Record the exact artifact and runtime configuration before repair.
- **Inspect the failure** — Exit, health, logs, resources, mounts, and network narrow the cause.
- **Reproduce cleanly** — The fix belongs in the image or declared runtime, not in a patched instance.

**From symptom to reproducible cause**

1. **Freeze observations** — Avoid restart, removal, or in-container edits.
2. **Capture state and identity** — Inspect exit, error, image digest, command, and attachments.
3. **Correlate logs and resources** — Align timestamps with health, OOM, and daemon events.
4. **Probe the failing boundary** — Check process, DNS, socket, files, or permission with read-only commands.
5. **Recreate from declarations** — Validate the hypothesis on a clean container.

*Run it — classify exit evidence (Python)*

```python
cases = [(0, False), (1, False), (137, True)]
for code, oom in cases:
    cause = "success" if code == 0 else ("memory kill" if oom else "application failure")
    print(f"exit={code}, oom={str(oom).lower()} -> {cause}")

# exit=0, oom=false -> success
# exit=1, oom=false -> application failure
# exit=137, oom=true -> memory kill
```

*Run it — classify exit evidence (Java)*

```java
public class Main {
  public static void main(String[] args) {
    int[] codes = {0, 1, 137}; boolean[] oom = {false, false, true};
    for (int i = 0; i < codes.length; i++) {
      String cause = codes[i] == 0 ? "success" : (oom[i] ? "memory kill" : "application failure");
      System.out.println("exit=" + codes[i] + ", oom=" + oom[i] + " -> " + cause);
    }
  }
}
/* exit=0, oom=false -> success
   exit=1, oom=false -> application failure
   exit=137, oom=true -> memory kill */
```

### Your first time: Your mission: diagnose without patching

- [ ] Create one intentional failure — Use a missing safe configuration variable or invalid command.
- [ ] Capture inspect JSON and logs — Do this before restart or removal.
- [ ] State one evidence-backed hypothesis — Name the failing boundary and supporting fields.
- [ ] Fix declarations and recreate — A clean rerun proves the correction is repeatable.

You have a diagnosis that survives container replacement.

- **The container exits immediately.**
  Inspect configured command, state error, exit code, and earliest logs; the main process may have completed or failed.
- **Health is unhealthy while the process runs.**
  Inspect health-check output, timing, dependencies, and whether the probe tests the correct endpoint.
- **Exit code 137 appears.**
  Check `OOMKilled`, resource limits, host memory pressure, and daemon events before assuming an application exception.

### Where to check

- `State.ExitCode`, `State.Error`, `State.OOMKilled`, and `State.Health`.
- Configured image, command, entrypoint, user, working directory, and environment names.
- Mount and network inspect data.
- Timestamped app logs, daemon logs, and events.

### Worked example: the restart loop misdiagnosed as networking

1. A test reports connection refused and the team inspects port mappings.
2. `docker ps -a` shows the service repeatedly restarting.
3. Inspect reports exit code 1, and logs show an unreadable config file.
4. Mount metadata reveals the file was bind-mounted with wrong permissions.
5. QA fixes host permissions in setup and recreates the container cleanly.

**Quiz.** What should happen before restarting a failed container?

- [ ] Install an editor inside it
- [x] Capture state, identity, configuration, and logs
- [ ] Delete all volumes
- [ ] Change several settings together

*Evidence-first triage preserves the failure and supports a testable hypothesis.*

- **OOMKilled** — Inspect state flag indicating the container process was killed for memory pressure.
- **Health status** — Result of the configured health check, separate from process running state.
- **Clean reproduction** — Recreate from corrected declarations rather than a patched instance.

### Challenge

Build a one-command evidence bundle that captures inspect JSON, timestamped logs, and resource state without printing secrets.

### Ask the community

> Container `[name]` has exit `[code]`, OOM `[flag]`, health `[status]`, image `[digest]`, and last logs `[lines]`. Which hypothesis best fits?

Redact values, tokens, and private paths.

- [Docker Docs — docker container inspect](https://docs.docker.com/reference/cli/docker/container/inspect/)
- [Docker Docs — docker container stats](https://docs.docker.com/reference/cli/docker/container/stats/)
- [Docker Docs — docker system events](https://docs.docker.com/reference/cli/docker/system/events/)

🎬 [Docker Tutorial for Beginners [FULL COURSE in 3 Hours] — TechWorld with Nana](https://www.youtube.com/watch?v=3c-iBn73dDE) (166 min)

- Preserve evidence before restart, edit, or removal.
- State, logs, resources, mounts, networks, and image identity narrow failures.
- Running and healthy are different states.
- Fix declarations and validate on a clean recreation.


## Related notes

- [[Notes/docker-and-containers-for-testers/docker-hands-on/run-exec-logs-and-stop|Run / exec / logs / stop]]
- [[Notes/docker-and-containers-for-testers/docker-hands-on/ports-and-volumes|Ports & volumes]]
- [[Notes/docker-and-containers-for-testers/docker-hands-on/environment-variables-and-networks|Environment variables & networks]]


---
_Source: `packages/curriculum/content/notes/docker-and-containers-for-testers/docker-hands-on/debugging-a-container.mdx`_
