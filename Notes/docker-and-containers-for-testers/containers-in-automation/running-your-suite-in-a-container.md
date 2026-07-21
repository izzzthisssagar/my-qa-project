---
title: "Running Your Suite in a Container"
tags: ["docker-and-containers-for-testers", "containers-in-automation", "test-runner", "reproducibility"]
updated: "2026-07-17"
---

# Running Your Suite in a Container

*Package the test runtime as a reproducible image, inject environment-specific configuration at execution, and make reports and exit status survive the container.*

> The useful artifact is not “tests in Docker.” It is an immutable test runtime that behaves the same on a laptop and a CI runner while inputs, secrets, reports, and exit status remain explicit.

> **In real life**
>
> The Svalbard Seed Vault stores labeled containers under controlled conditions. The box supplies a repeatable boundary; the label and inventory still say what is inside. A test image fixes tools and dependencies, while runtime configuration says which environment to test.

**test runner image**: A test runner image contains the language runtime, system libraries, dependency lock state, test code or a declared code mount, and one predictable entrypoint. It should not bake environment secrets or mutable test results into image layers.

## Separate build inputs from run inputs

The Dockerfile should make expensive dependency layers cacheable and application-specific changes cheap. Copy lock files first, install with frozen or reproducible options, then copy tests. Use a non-root user where practical and a `.dockerignore` so local reports, secrets, and dependency directories do not enter the build context.

At run time, pass the target base URL, browser choice, shard, and credentials through a secret-aware mechanism. Mount or copy reports to a host/CI-visible location. The container's process must return the suite's exit code; `docker run` then becomes a trustworthy gate.

> **Tip**
>
> Make the image entrypoint run exactly one suite command. Extra arguments should select a tag, shard, or browser—not replace a hidden chain of shell behavior.

> **Common mistake**
>
> Baking `TEST_PASSWORD`, a staging URL, and last run's screenshots into the image. The image becomes both a secret leak and an environment-specific snowflake.

![A worker placing a gray storage box among labeled containers on blue and orange shelves inside the Svalbard Global Seed Vault](running-your-suite-in-a-container.jpg)
*Storage containers in Svalbard Global Seed Vault — Dag Endresen, Wikimedia Commons, public domain. [Source](https://commons.wikimedia.org/wiki/File:Storage_containers_in_Svalbard_Global_Seed_Vault_01.jpg)*
- **Versioned image** — A labeled box identifies one immutable runtime built from a Dockerfile and dependency lock files.
- **Repeatable inventory** — Pinned runtimes and system libraries make the test environment inspectable and reproducible.
- **Runtime placement** — The same image can run in different environments when endpoints and credentials arrive at execution time.

**Build once, run with evidence**

1. **Define the runtime** — Pin the base image and install locked system and language dependencies.
2. **Copy the suite** — Add tests and a single predictable entrypoint after dependency layers.
3. **Inject run inputs** — Provide target URL, browser, shard, and secrets without rebuilding.
4. **Execute as PID 1** — The test process receives signals and determines the container exit code.
5. **Export artifacts** — Reports, screenshots, traces, and logs leave the ephemeral filesystem.

*Build a deterministic container command (Python)*

```python
config = {"base_url": "https://staging.example.test", "browser": "chromium", "shard": "2/4"}
required = ("base_url", "browser", "shard")
missing = [key for key in required if not config.get(key)]
if missing:
    raise SystemExit(f"missing: {missing}")

command = ["pytest", "-m", "smoke", f"--base-url={config['base_url']}", f"--browser={config['browser']}"]
print(" ".join(command))
print("shard=" + config["shard"])
# pytest -m smoke --base-url=https://staging.example.test --browser=chromium
# shard=2/4
```

*Preserve the suite verdict as an exit code (Java)*

```java
import java.util.*;

class Main {
  public static void main(String[] args) {
    List<Boolean> tests = List.of(true, true, false, true);
    long failed = tests.stream().filter(passed -> !passed).count();
    int exitCode = failed == 0 ? 0 : 1;
    System.out.println("tests=" + tests.size() + " failed=" + failed);
    System.out.println("container exit=" + exitCode);
  }
}
// tests=4 failed=1
// container exit=1
```

### Your first time: Containerize one smoke suite

- [ ] Pin and minimize — Choose a specific base image, locked dependencies, `.dockerignore`, and a non-root runtime.
- [ ] Define one entrypoint — Run the test process directly so signals and exit status remain accurate.
- [ ] Inject configuration — Supply environment URL and secret references only at execution time.
- [ ] Export evidence — Mount a report directory and verify it is populated on both pass and fail.

- **The image rebuilds every dependency after a test edit.**
  Copy lock files and install dependencies before copying frequently changed suite sources.
- **CI is green although tests failed.**
  Remove wrappers that swallow status; make the test process or an `exec`-replacing entrypoint determine the container exit code.
- **Reports disappear after the run.**
  Write to a mounted workspace or copy artifacts before container removal, including on failure.
- **The suite passes locally but fonts or browsers differ in CI.**
  Inspect image digests, architecture, runtime variables, and browser/system packages; avoid mutable tags.

### Where to check

Inspect the image digest and history, Dockerfile layer order, `.dockerignore`, effective environment variable names without exposing values, container user, entrypoint and command, exit code, mounted report permissions, and CI artifact upload conditions.

### Worked example: A Playwright smoke image

Pin a Playwright base image compatible with the project version, copy package manager metadata, install with a frozen lockfile, then copy the suite. Run as a non-root user with `BASE_URL` and shard inputs. Mount `/work/test-results`, execute the test process directly, and confirm a failing assertion returns container status 1 while the HTML report remains available.

**Quiz.** Which item belongs at image build time rather than container run time?

- [ ] Staging password
- [ ] Current test target URL
- [x] Pinned language and browser dependencies
- [ ] CI job identifier

*The image owns the reproducible runtime. Environment targets, run identity, and secrets are runtime inputs.*

- **Build context** — Files sent to the Docker builder; restrict it with `.dockerignore`.
- **Immutable image** — A content-addressed runtime artifact that should not change between laptop and CI execution.
- **Artifact mount** — A host- or runner-visible path where ephemeral containers write durable reports.

### Challenge

Containerize one suite so a deliberate failing test produces status 1 and a readable report outside the container. Re-run from a clean checkout using only the documented image build and run commands.

### Ask the community

> Image digest/base: [values]. Entrypoint: [value]. Runtime inputs: [names only]. Container exit: [code]. Artifact mount and permissions: [evidence]. What differs between local and CI?

Do not post secret values; configuration shape and image identity are enough.

- [Docker — building best practices](https://docs.docker.com/build/building/best-practices/)
- [Docker — optimize build cache](https://docs.docker.com/build/cache/optimize/)
- [Docker — run tests in a container](https://docs.docker.com/guides/java/run-tests/)

🎬 [How to Run Automated Tests in Docker Container](https://www.youtube.com/watch?v=CEBbOFqTPnk) (4 min)

- The image fixes the test runtime; execution injects targets, shards, and secrets.
- Layer order and `.dockerignore` control build speed and leakage risk.
- The suite process must own the container exit status.
- Export reports before the ephemeral filesystem disappears.


## Related notes

- [[Notes/docker-and-containers-for-testers/containers-in-automation/selenium-grid-in-docker|Selenium Grid in Docker]]
- [[Notes/docker-and-containers-for-testers/containers-in-automation/testcontainers-for-database-fixtures|Testcontainers for database fixtures]]
- [[Notes/docker-and-containers-for-testers/containers-in-automation/containers-in-ci|Containers in CI]]


---
_Source: `packages/curriculum/content/notes/docker-and-containers-for-testers/containers-in-automation/running-your-suite-in-a-container.mdx`_
