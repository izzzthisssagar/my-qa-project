---
title: "Virtual machine vs container"
tags: ["docker-and-containers-for-testers", "containers-in-plain-words", "track-e"]
updated: "2026-07-17"
---

# Virtual machine vs container

*Separate hardware virtualization from process isolation, then choose the boundary that makes a QA environment repeatable without pretending containers are tiny virtual machines.*

> A container is not a lightweight computer. It is an isolated process whose strongest dependency—the host kernel—is easy to forget until a test behaves differently on another operating system.

> **In real life**
>
> A VM rents a furnished house with its own utilities; a container rents a locked workshop in a shared building. Both provide boundaries, but they share different layers.

**virtualization boundary**: A virtual machine emulates or virtualizes hardware and boots a guest operating system. A container isolates processes and filesystems while sharing the host kernel through namespaces, cgroups, and related controls.

## Compare the actual boundaries

| Question | Virtual machine | Container |
|---|---|---|
| Kernel | Guest kernel | Host kernel |
| Startup | Boots an OS | Starts a process |
| Image contents | OS plus application | Application and user-space dependencies |
| Isolation | Hardware-level boundary | Process-level boundary |
| QA fit | Cross-OS and kernel testing | Fast, repeatable service environments |

> **Tip**
>
> Use a VM when the kernel or operating system is part of the test target. Use a container when the goal is packaging and repeating a user-space service.

> **Common mistake**
>
> Calling containers “mini VMs” hides kernel sharing and leads to false portability claims.

![Stacks of standardized freight containers at a terminal](vm-vs-container.jpg)
*Container port — Andrew McMillan, public domain. [Source](https://commons.wikimedia.org/wiki/File:Container_port_(1).jpg)*
- **Shared terminal** — Containers share host infrastructure just as freight boxes share terminal equipment.
- **Isolated contents** — Each box carries its own payload and user-space dependencies.
- **Standard interface** — A consistent package boundary makes handling repeatable across compatible hosts.

**From host to test process**

1. **Host kernel** — Owns scheduling, networking, and device access.
2. **Runtime requests isolation** — Namespaces and resource controls define the boundary.
3. **Image filesystem is mounted** — Read-only layers supply user-space files.
4. **Application process starts** — The container lives while its main process lives.

*Run it — compare packaged layers (Python)*

```python
vm = ["guest kernel", "system services", "test app"]
container = ["user-space libraries", "test app"]
print(f"VM packages {len(vm)} layers: {', '.join(vm)}")
print(f"Container packages {len(container)} layers and shares the host kernel")

# VM packages 3 layers: guest kernel, system services, test app
# Container packages 2 layers and shares the host kernel
```

*Run it — compare packaged layers (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    List<String> vm = List.of("guest kernel", "system services", "test app");
    List<String> container = List.of("user-space libraries", "test app");
    System.out.println("VM packages " + vm.size() + " layers: " + String.join(", ", vm));
    System.out.println("Container packages " + container.size() + " layers and shares the host kernel");
  }
}
/* VM packages 3 layers: guest kernel, system services, test app
   Container packages 2 layers and shares the host kernel */
```

### Your first time: Your mission: choose the correct boundary

- [ ] Name what the test must vary — Application dependencies, OS user space, or the kernel itself?
- [ ] Record the host constraint — Linux containers require a compatible Linux kernel, directly or through a VM.
- [ ] Choose container or VM — Make the boundary an explicit test-design decision.
- [ ] Write one invalid claim — Document what the chosen boundary cannot prove.

You now have an isolation decision, not a fashionable default.

- **A Linux container behaves differently on macOS or Windows.**
  Inspect Docker Desktop's Linux VM boundary and architecture; do not assume the host kernel is identical.
- **A kernel-specific defect cannot be reproduced.**
  Test on the target kernel or a representative VM rather than relying on user-space packaging.
- **The container consumes too many resources.**
  Set and observe CPU and memory limits; isolation does not imply unlimited capacity.

### Where to check

- `docker inspect` for runtime configuration and platform.
- `docker info` for server OS, architecture, and runtime.
- `/proc/1/cgroup` inside a Linux container for process context.
- The target production kernel and architecture requirements.

### Worked example: the test that needed a VM

1. A filesystem watcher passes in a Linux container on a macOS laptop.
2. Production uses a specific Linux kernel and storage driver.
3. The container reproduces user-space packages but not the production kernel path.
4. QA reruns it in a representative VM and reproduces the missed event.
5. The test plan now distinguishes packaging coverage from kernel coverage.

**Quiz.** Which statement identifies the central VM/container difference?

- [ ] Containers have no operating-system files
- [x] A VM boots a guest kernel while a container shares the host kernel
- [ ] VMs cannot run services
- [ ] Containers always provide stronger isolation

*The kernel boundary is the key distinction; performance and security depend on configuration and workload.*

- **VM boundary** — Virtualized hardware plus a guest operating system and kernel.
- **Container boundary** — Isolated processes and user space sharing a host kernel.
- **QA decision** — Choose based on which layers the test must control or vary.

### Challenge

Take one current environment test and state precisely which defects a container can reproduce and which require a representative VM or host.

### Ask the community

> Our test needs to vary `[layer]` on `[target platform]`. We chose `[container/VM]` because `[boundary]`. What host dependency are we still missing?

Include host OS, architecture, and the behavior under test.

- [Docker Docs — What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)
- [Docker Docs — Engine security](https://docs.docker.com/engine/security/)

🎬 [Docker in 100 Seconds — Fireship](https://www.youtube.com/watch?v=Gjnup-PuquQ) (2 min)

- A VM boots a guest kernel; a container shares the host kernel.
- Containers package user-space dependencies around an isolated process.
- Kernel and cross-OS validation may require a representative VM or host.
- Isolation, portability, and security are properties to verify, not slogans.


## Related notes

- [[Notes/docker-and-containers-for-testers/containers-in-plain-words/images-containers-and-registries|Images, containers & registries]]
- [[Notes/docker-and-containers-for-testers/containers-in-plain-words/why-qa-cares|Why QA cares]]
- [[Notes/docker-and-containers-for-testers/containers-in-plain-words/install-and-first-run|Install & first run]]


---
_Source: `packages/curriculum/content/notes/docker-and-containers-for-testers/containers-in-plain-words/vm-vs-container.mdx`_
