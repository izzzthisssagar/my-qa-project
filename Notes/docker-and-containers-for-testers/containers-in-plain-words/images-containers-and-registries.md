---
title: "Images, containers, and registries"
tags: ["docker-and-containers-for-testers", "containers-in-plain-words", "track-e"]
updated: "2026-07-17"
---

# Images, containers, and registries

*Trace an immutable image reference from a registry into a running container, and learn why tags alone are weak evidence for reproducible testing.*

> “We tested `latest`” is not a build identity. A mutable tag can point at different image content between two runs while every command in the test report looks identical.

> **In real life**
>
> An image is a sealed blueprint, a container is one building created from it, and a registry is the catalogue that distributes blueprints. A tag is a movable label; a digest is the blueprint's content address.

**image lifecycle**: A container image is an immutable, layered package of filesystem content and configuration. A container is a runnable instance of an image. A registry stores and distributes image manifests and layers by repository, tag, or digest.

## Follow identity, not just names

- `docker pull repo/app:1.4` resolves a tag to a manifest and downloads missing layers.
- `docker run` creates a writable container layer above the image layers and starts its configured process.
- Several containers can run independently from the same image.
- Tags can move; a digest such as `sha256:...` identifies exact manifest content.
- Private registries require authentication and deliberate credential handling.

> **Tip**
>
> Record the pulled digest in test evidence and deployment metadata. Keep a friendly version tag too, but do not confuse it with immutable identity.

> **Common mistake**
>
> Debugging by editing a running container and then assuming the image changed. The writable container layer disappears when that container is removed.

![Freight containers stacked in rows at a port](images-containers-and-registries.jpg)
*Container at Mongla port — Nahian shuvo, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Container_at_mongla_port.jpg)*
- **Repository** — A named collection groups related image versions.
- **Layer reuse** — Shared layers reduce repeated transfer and storage.
- **Exact unit** — A digest identifies content more reliably than a movable tag.

**From registry reference to process**

1. **Resolve tag or digest** — The registry returns an image manifest.
2. **Fetch missing layers** — The local content store reuses layers already present.
3. **Create writable layer** — Container-specific filesystem changes stay above image layers.
4. **Start configured process** — Entrypoint, command, environment, and mounts form the runtime.

*Run it — expose mutable tag risk (Python)*

```python
registry = {"app:latest": "sha256:aaa", "app:1.4": "sha256:aaa"}
first = registry["app:latest"]
registry["app:latest"] = "sha256:bbb"
second = registry["app:latest"]
print(f"same tag: {first == second}")
print(f"first={first}, second={second}")

# same tag: False
# first=sha256:aaa, second=sha256:bbb
```

*Run it — expose mutable tag risk (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    Map<String,String> registry = new HashMap<>();
    registry.put("app:latest", "sha256:aaa");
    String first = registry.get("app:latest");
    registry.put("app:latest", "sha256:bbb");
    String second = registry.get("app:latest");
    System.out.println("same tag: " + first.equals(second));
    System.out.println("first=" + first + ", second=" + second);
  }
}
/* same tag: false
   first=sha256:aaa, second=sha256:bbb */
```

### Your first time: Your mission: preserve image identity

- [ ] Pull a versioned image — Use a small trusted image and a deliberate tag.
- [ ] Inspect its repo digest — Capture the resolved content identity.
- [ ] Run two named containers — Observe independent writable state from one image.
- [ ] Remove containers, keep image — Separate runtime lifecycle from image storage.

You can now say exactly what artifact produced a test environment.

- **A rerun with the same tag behaves differently.**
  Compare resolved digests and pin the intended image by digest in controlled runs.
- **Pull returns an authentication error.**
  Confirm registry hostname, repository permission, and credential-helper state without printing secrets.
- **A local edit vanishes after replacement.**
  Rebuild the image or mount deliberate persistent data; do not use container mutation as configuration management.

### Where to check

- `docker image inspect IMAGE` for IDs, digests, layers, and config.
- `docker container inspect NAME` for the image reference actually used.
- Registry repository history and immutable-tag policy.
- CI logs for pull output and promoted digest.

### Worked example: the tag that moved overnight

1. CI tests `registry.example/app:qa` and records only the tag.
2. A second pipeline pushes a new manifest to that tag.
3. The rerun pulls new content and fails despite identical test code.
4. The team compares digests and finds the environment changed.
5. Promotion now records and reuses the tested digest.

**Quiz.** Which reference best identifies exact image content?

- [ ] Container name
- [ ] A mutable tag
- [x] A registry digest
- [ ] Dockerfile directory

*A digest is content-addressed; tags are human-friendly pointers that can move.*

- **Image** — Immutable layered package and runtime configuration.
- **Container** — A runnable image instance with its own writable layer.
- **Registry digest** — Content identity returned for an image manifest.

### Challenge

Update one CI report so it records repository, tag, and resolved digest, then prove the deployment uses the tested digest.

### Ask the community

> Tag `[tag]` resolved to `[digest A]` during test and `[digest B]` later. Which registry or pipeline action moved it?

Include timestamps and repository history, never credentials.

- [Docker Docs — What is an image?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/)
- [Docker Docs — Docker Hub](https://docs.docker.com/docker-hub/)

🎬 [Docker in 100 Seconds — Fireship](https://www.youtube.com/watch?v=Gjnup-PuquQ) (2 min)

- Images are immutable packages; containers are their runnable instances.
- Registries distribute manifests and layers.
- Tags can move while digests identify exact content.
- Test evidence should preserve the resolved image digest.


## Related notes

- [[Notes/docker-and-containers-for-testers/containers-in-plain-words/vm-vs-container|VM vs container]]
- [[Notes/docker-and-containers-for-testers/containers-in-plain-words/install-and-first-run|Install & first run]]
- [[Notes/docker-and-containers-for-testers/docker-hands-on/run-exec-logs-and-stop|Run / exec / logs / stop]]


---
_Source: `packages/curriculum/content/notes/docker-and-containers-for-testers/containers-in-plain-words/images-containers-and-registries.mdx`_
