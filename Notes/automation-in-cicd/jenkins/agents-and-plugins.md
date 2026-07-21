---
title: "Agents & plugins"
tags: ["jenkins", "agents", "plugins", "track-d"]
updated: "2026-07-17"
---

# Agents & plugins

*Jenkins controllers schedule work; agents supply isolated executors and tools; plugins add capabilities but also create versioned security, compatibility, availability, and maintenance dependencies.*

> When a Jenkins test fails, the application is only one suspect. The controller may have scheduled it
> onto the wrong capability, two executors may be fighting over one machine, or a plugin update may have
> changed the step that interprets the Jenkinsfile. Architecture is part of test evidence.

> **In real life**
>
> A workshop foreman assigns work but should not weld every part at the office desk. Skilled workers,
> stations, and tools execute the plan. Jenkins' controller schedules; agents and executors do the work;
> plugins add specialized tools — each with capacity and maintenance limits.

**Jenkins agents and plugins**: A Jenkins controller manages configuration, authentication, scheduling, queues, and orchestration. An agent is a process on a node that performs assigned work through one or more executors; an executor is one concurrent work slot. Labels describe capabilities used by Pipeline agent selection. Plugins extend the controller and Pipeline with integrations and steps, but every plugin is executable supply-chain state that must be inventoried, updated, secured, tested, and minimized.

## Separate orchestration from execution

Avoid running builds on the built-in controller node; Jenkins documentation discourages it for
security, performance, and scalability. Prefer agents with explicit capability labels such as
`linux`, `windows`, `browser`, or `jdk21`. Keep labels meaningful and provision the matching tools
reproducibly.

Plugins are not free features. Each adds code, dependencies, configuration, update work, and possible
security advisories. Use the smallest maintained set and record versions outside a hand-built controller.

> **Tip**
>
> Start with one executor per agent for resource-heavy browser suites. Add executors only after CPU,
> memory, I/O, ports, workspaces, accounts, and test data are proven safe under concurrency.

> **Common mistake**
>
> Installing a plugin during an incident because a blog post uses its step. Check health, maintenance,
> security advisories, dependencies, compatibility, and whether shell or built-in Pipeline features
> already solve the need.

![Four factory workers in protective clothing holding welding tools in a workshop](agents-and-plugins.jpg)
*Factory workers, circa 1945 — Howard Clifford / University of Washington, no known copyright restrictions. [Source](https://commons.wikimedia.org/wiki/File:Factory_workers_(4951753946).jpg)*
- **Controller coordinates** — Scheduling and governance decide which capable worker receives the task.
- **Agent capability** — Labels describe OS, browser, hardware, or tool capabilities required by the job.
- **Executor slot** — Each active slot consumes real CPU, memory, I/O, ports, and shared state.
- **Plugin tool** — Specialized capabilities help, but each tool needs compatible versions and maintenance.

**How Jenkins places work**

1. **Build queued** — A job declares an agent label and resource need.
2. **Controller matches** — Online nodes and labels are evaluated.
3. **Executor reserved** — One concurrency slot and workspace are assigned.
4. **Agent executes** — Installed tools or containers run Pipeline steps.
5. **Plugin participates** — Plugin-provided steps may transform, publish, or integrate.
6. **Result returns** — Logs and evidence return while workspace cleanup and capacity release occur.

*Run it — match a job to an agent (Python)*

```python
``agents = {
    "a1": {"linux", "browser", "jdk21"},
    "a2": {"windows", "browser"},
}
required = {"linux", "browser"}
eligible = [name for name, labels in agents.items() if required <= labels]
print("required:", ", ".join(sorted(required)))
print("eligible:", ", ".join(eligible) if eligible else "none")``
```

*Run it — match a job to an agent (Java)*

```java
``import java.util.*;

public class Main {
    public static void main(String[] args) {
        var agents = new LinkedHashMap<String, Set<String>>();
        agents.put("a1", Set.of("linux", "browser", "jdk21"));
        agents.put("a2", Set.of("windows", "browser"));
        var required = Set.of("linux", "browser");
        var eligible = agents.entrySet().stream().filter(e -> e.getValue().containsAll(required)).map(Map.Entry::getKey).toList();
        System.out.println("required: browser, linux");
        System.out.println("eligible: " + (eligible.isEmpty() ? "none" : String.join(", ", eligible)));
    }
}``
```

### Your first time: Your mission: audit one execution path

- [ ] Choose a build and record controller, node, agent, and executor — Use queue and build pages; do not call all four things 'the Jenkins server'.
- [ ] Verify every required label and tool — Compare Pipeline request with node labels, tool versions, containers, and environment.
- [ ] Measure concurrency resources — Observe CPU, memory, I/O, workspace, ports, and shared test data with current executors.
- [ ] Inventory plugin-provided steps — Record plugin name/version, health, advisories, dependencies, and owner.

You now know which infrastructure facts belong in a failed test's diagnosis.

- **A build waits indefinitely in the queue.**
  Read the queue reason; verify label expression, online agents, executor availability, and clouds/provisioning.
- **Two builds corrupt each other's output.**
  Reduce executors and find shared workspaces, ports, files, accounts, or data before increasing parallelism.
- **A Pipeline step suddenly becomes unknown.**
  Map the step to its plugin and inspect installation, version, failed dependencies, and recent updates/restarts.
- **The controller becomes slow during builds.**
  Confirm work is not running on the built-in node; move execution to agents and inspect queue/controller health separately.

### Where to check

- **Queue reason and node labels** — placement mismatch versus capacity shortage.
- **Node monitor data** — disk, temp, swap, clock, response, CPU, memory, and I/O.
- **Executor count and running builds** — actual resource contention.
- **Plugin Manager and security advisories** — versions, dependencies, health, disabled/failed plugins.
- **Build node/workspace metadata** — exact environment behind the result.

### Worked example: the browser suite that failed only in pairs

1. One agent has two executors; both browser jobs use the same test account and download directory.
2. Alone each passes. Together one logs out the other and overwrites a screenshot.
3. Retries hide some collisions but increase runtime.
4. The team temporarily uses one executor, then gives each job unique accounts and directories.
5. Two executors return only after parallel isolation tests pass.

**Quiz.** What does an executor represent in Jenkins?

- [ ] A plugin update site
- [x] One concurrent task slot on a node/agent
- [ ] The controller database
- [ ] A Git branch

*Agents perform work; executors determine how many tasks an agent can run concurrently. More executors increase resource and shared-state pressure.*

- **Controller** — Orchestrates configuration, authentication, queueing, scheduling, and results.
- **Agent** — Worker process on a node that executes assigned Pipeline work.
- **Executor** — One concurrent task slot on a node.
- **Label** — Capability metadata used to match a job's agent requirement.
- **Plugin governance** — Minimize, inventory, pin/provision, monitor advisories, test upgrades, and assign ownership.

### Challenge

Build a table of agents, labels, executors, tools, resource limits, and suites. Then build a plugin
inventory with version, purpose, health, advisory status, dependency, and owner. Remove one unjustified risk.

### Ask the community

> Build [number] requested labels [expression], queued on [reason], and ran on [node/executor] with resources [values]. Plugin step [name/version] produced [error].

Separate placement, capacity, tool, and plugin evidence so the next experiment changes one layer.

- [Jenkins Handbook — Managing Nodes](https://www.jenkins.io/doc/book/managing/nodes/)
- [Jenkins Handbook — Managing Plugins](https://www.jenkins.io/doc/book/managing/plugins/)

🎬 [How to Create an Agent Node in Jenkins — CloudBeesTV](https://www.youtube.com/watch?v=99DddJiH7lM) (24 min)

- Controllers orchestrate; agents execute; executors set concurrency; labels express capabilities.
- Do not run ordinary builds on the built-in controller node.
- Begin resource-heavy test agents conservatively and prove isolation before adding executors.
- Plugins are executable dependencies with security, compatibility, and ownership costs.
- A test result is incomplete without the node, tools, executor pressure, and plugin versions behind it.


## Related notes

- [[Notes/automation-in-cicd/jenkins/jobs-and-the-classic-ui|Jobs & the classic UI]]
- [[Notes/automation-in-cicd/jenkins/jenkinsfile-pipeline-as-code|Jenkinsfile — pipeline as code]]
- [[Notes/automation-in-cicd/jenkins/when-teams-still-pick-jenkins|When teams still pick Jenkins]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/jenkins/agents-and-plugins.mdx`_
