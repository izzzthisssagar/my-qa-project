---
title: "Writing a Dockerfile"
tags: ["docker-and-containers-for-testers", "dockerfiles-and-compose", "track-e"]
updated: "2026-07-17"
---

# Writing a Dockerfile

*Turn application source into a repeatable container image. Learn build context, layer-aware instruction order, executable defaults, non-root runtime users, and the checks that expose accidental baggage.*

> A Dockerfile is a packing list with consequences. Put the wrong thing in the build context and it can enter an image layer; put a frequently changing file too early and every build repacks the warehouse.

> **In real life**
>
> A shipping manifest names the container's base, cargo, destination, and opening instructions. A Dockerfile does the same for an image, one immutable layer at a time.

**Dockerfile**: A text file whose ordered instructions tell a Docker builder how to produce a container image. Common instructions include FROM, WORKDIR, COPY, RUN, USER, EXPOSE, ENTRYPOINT, and CMD.

## Build an image deliberately

- Start with a trusted, suitably small base image and pin a version or digest according to your update policy.
- Set `WORKDIR` instead of scattering absolute paths through later instructions.
- Copy dependency manifests before application source so dependency layers can remain cached.
- Use `.dockerignore` to keep secrets, VCS metadata, test artifacts, and bulky local folders out of the context.
- Prefer JSON-array form for `CMD` or `ENTRYPOINT` so signals reach the process predictably.
- Create and select a non-root runtime user when the workload does not require root.

> **Common mistake**
>
> Treating `EXPOSE 8080` as port publishing. It documents an intended listening port; publishing still happens with `docker run -p` or a Compose `ports` mapping.

> **Tip**
>
> Inspect the result, not only the build exit code: run the container, inspect its configured user and command, scan it, and verify no credentials or host-only files entered any layer.

![Rows of multicolored shipping containers stacked at a port](writing-a-dockerfile.jpg)
*Shipping containers in a port — Chuttersnap, Wikimedia Commons, CC0. [Source](https://commons.wikimedia.org/wiki/File:Shipping_containers_in_a_port_(Unsplash).jpg)*
- **Base row** — FROM establishes the filesystem and runtime assumptions beneath every later layer.
- **Ordered layers** — Each filesystem-changing instruction adds a layer whose cache depends on earlier inputs.
- **Sealed cargo** — The final image should contain runtime necessities, not local secrets or build debris.

**From source tree to running process**

1. **Choose build context** — The final dot in docker build selects the files the builder can access.
2. **Read Dockerfile** — BuildKit resolves instructions and their dependencies.
3. **Reuse or execute layers** — Stable inputs can reuse cache; changed inputs invalidate dependent work.
4. **Export image** — The result receives a content-addressed identity and optional tag.
5. **Run and verify** — A container exercises the configured user, command, network, and filesystem.

*Run it — model cache invalidation (Python)*

```python
steps = ["base", "dependency manifest", "install dependencies", "source", "start command"]
changed = "source"
invalidated = False
for step in steps:
    if step == changed:
        invalidated = True
    print(f"{step}: {'rebuild' if invalidated else 'cached'}")

# base: cached
# dependency manifest: cached
# install dependencies: cached
# source: rebuild
# start command: rebuild
```

*Run it — model cache invalidation (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    List<String> steps = List.of("base", "dependency manifest", "install dependencies", "source", "start command");
    boolean invalidated = false;
    for (String step : steps) {
      if (step.equals("source")) invalidated = true;
      System.out.println(step + ": " + (invalidated ? "rebuild" : "cached"));
    }
  }
}
/* base: cached
   dependency manifest: cached
   install dependencies: cached
   source: rebuild
   start command: rebuild */
```

### Your first time: Your mission: build and interrogate one image

- [ ] Write Dockerfile and .dockerignore — Keep manifests before source and exclude credentials and local outputs.
- [ ] Build with a descriptive tag — Run docker build -t ticket-api:test . from the intended context.
- [ ] Run as a disposable container — Publish only the required port and pass configuration at runtime.
- [ ] Inspect identity and contents — Check docker image inspect, docker history, runtime user, logs, and a clean shutdown.

You now have evidence about the artifact, not merely a green build line.

- **COPY cannot find a file that exists locally.**
  Confirm the build-context path, .dockerignore rules, filename case, and that COPY sources are relative to the context.
- **Every small source change reinstalls dependencies.**
  Copy lockfiles first, install dependencies, then copy frequently changing source in a later layer.
- **The container ignores stop signals or takes too long to exit.**
  Use exec-form ENTRYPOINT or CMD and ensure the application handles the termination signal.

### Where to check

- `docker build --progress=plain` for the first invalidated step.
- `docker image history --no-trunc IMAGE` for unexpectedly large or revealing layers.
- `docker image inspect IMAGE` for configured user, entrypoint, command, labels, and exposed ports.
- `docker run --rm IMAGE` plus logs and exit code for runtime behavior.

### Worked example: the image that copied a developer's world

1. A team used `COPY . .` before dependency installation and had no `.dockerignore`.
2. A local dependency directory, `.git`, test reports, and a `.env` file entered the context.
3. Builds became slow, cache reuse collapsed, and the secret remained recoverable from an earlier layer even after deletion.
4. The team excluded host-only files, rotated the credential, copied manifests before source, and used a secret mount for authenticated build access.
5. CI added image-content and vulnerability checks so the mistake could not silently return.

**Quiz.** Why copy a dependency lockfile before application source in a Dockerfile?

- [ ] It publishes the container port
- [x] It lets dependency installation remain cached when only source changes
- [ ] It forces the container to run as root
- [ ] It removes the need for .dockerignore

*Layer cache reuse depends on inputs and prior layers. Stable manifests placed earlier isolate expensive dependency installation from frequent source edits.*

- **Build context** — The files made available to the builder by the path or URL passed to the build command.
- **.dockerignore** — Rules that exclude files from the build context before it is sent to the builder.
- **Exec-form CMD** — A JSON-array command form that avoids an extra shell and improves signal behavior.

### Challenge

Build once, change only an application source file, then rebuild with plain progress output. Explain exactly which step first lost cache and why.

### Ask the community

> My Dockerfile first rebuilds at `[step]` after changing `[file]`. The relevant COPY order and .dockerignore rules are `[details]`. How can I preserve correct cache reuse?

Share sanitized instructions and timings; never post secrets or private registry tokens.

- [Docker Docs — Dockerfile overview](https://docs.docker.com/build/concepts/dockerfile/)
- [Docker Docs — Building best practices](https://docs.docker.com/build/building/best-practices/)

🎬 [Docker Tutorial for Beginners [FULL COURSE in 3 Hours] — TechWorld with Nana](https://www.youtube.com/watch?v=3c-iBn73dDE) (166 min)

- A Dockerfile is an ordered, reproducible image-build specification.
- Build context and .dockerignore control what the builder can see.
- Instruction order determines cache behavior and rebuild cost.
- Runtime defaults, user identity, and signal handling deserve explicit tests.
- Inspect image contents and history; a successful build is not sufficient evidence.


## Related notes

- [[Notes/docker-and-containers-for-testers/dockerfiles-and-compose/multi-stage-builds|Multi-stage builds]]
- [[Notes/docker-and-containers-for-testers/dockerfiles-and-compose/compose-app-and-database|Compose: app + database]]
- [[Notes/docker-and-containers-for-testers/dockerfiles-and-compose/disposable-test-environment|A disposable test environment]]


---
_Source: `packages/curriculum/content/notes/docker-and-containers-for-testers/dockerfiles-and-compose/writing-a-dockerfile.mdx`_
