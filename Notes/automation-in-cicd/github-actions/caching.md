---
title: "Caching"
tags: ["github-actions", "caching", "dependencies", "track-d"]
updated: "2026-07-17"
---

# Caching

*Dependency caching speeds GitHub Actions by restoring reusable inputs under content-derived keys, but a cache hit must never replace lockfile installation, test evidence, or correctness.*

> A fast wrong build is still wrong. Caching earns its place only when removing the cache changes speed,
> not the dependency set, test result, or evidence. The cache is a pantry: useful ingredients close at
> hand, never permission to skip the recipe and trust an unlabelled jar.

> **In real life**
>
> A labelled pantry avoids buying the same staples for every meal. The label and expiry matter: restore
> the wrong jar and speed becomes contamination. Cache keys are those labels; lockfile hashes and runner
> details describe which stored inputs are safe to reuse.

**dependency cache**: A GitHub Actions dependency cache stores reusable files from one workflow run and restores them in later runs when a cache key matches. Keys should include the operating system, relevant tool or runtime identity, and a hash of dependency lockfiles. A cache miss is normal and must fall back to a correct clean install. Caches are immutable for an exact key and can be evicted; they are not build artifacts or durable test evidence.

## Cache downloads, preserve installation

```yaml
- uses: actions/setup-node@v6
  with:
    node-version: 24
    cache: npm
- run: npm ci
```

The setup action can cache npm's package download data. `npm ci` still constructs `node_modules` from
the reviewed lockfile. Caching the package manager's store is usually safer than restoring a fully
materialized dependency tree whose native binaries and install scripts may depend on the runner.

> **Tip**
>
> Measure before and after. Record restore time, install time, hit rate, archive size, and total job
> duration. A huge cache can take longer to transfer than the clean download it replaces.

> **Common mistake**
>
> Using a broad static key such as `dependencies`. Lockfile changes then restore stale inputs across
> branches and runtimes, making failures depend on cache history instead of committed code.

![A crowded pantry shelf with labelled jars, bottles, fruit, and preserved food](caching.jpg)
*Pantry shelf — Chris Lawton, CC0. [Source](https://commons.wikimedia.org/wiki/File:Pantry_shelf_(Unsplash).jpg)*
- **Cache key labels** — A useful key identifies OS, tool/runtime, and lockfile content.
- **Reusable inputs** — Package downloads and tool stores are ingredients reused across clean jobs.
- **Restore keys** — Broader fallback keys can seed work, but the lockfile install must still verify the exact result.
- **Eviction** — A pantry can be cleared. A correct pipeline treats cache misses as ordinary, not failures.

**Safe dependency cache lifecycle**

1. **Compute key** — Combine OS, tool identity, and lockfile hash.
2. **Search exact match** — An exact key restores the known reusable input set.
3. **Try fallback** — Optional restore keys provide a starting point, not final correctness.
4. **Run clean install** — The package manager enforces the committed lockfile.
5. **Build and test** — Correctness checks remain identical on hit and miss.
6. **Save on miss** — A successful job may store reusable files under the new immutable key.

*Run it — derive content-sensitive cache keys (Python)*

```python
``import hashlib

os_name, runtime = "linux", "node-24"
lockfile = b'{"lockfileVersion": 3, "packages": {}}'
digest = hashlib.sha256(lockfile).hexdigest()[:12]
print(f"{os_name}-{runtime}-npm-{digest}")
print("same content gives same key:", digest == hashlib.sha256(lockfile).hexdigest()[:12])``
```

*Run it — derive content-sensitive cache keys (Java)*

```java
``import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.HexFormat;

public class Main {
    public static void main(String[] args) throws Exception {
        byte[] lockfile = "{\"lockfileVersion\": 3, \"packages\": {}}".getBytes(StandardCharsets.UTF_8);
        String digest = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(lockfile)).substring(0, 12);
        System.out.println("linux-node-24-npm-" + digest);
        System.out.println("key includes OS, runtime, tool, and content");
    }
}``
```

### Your first time: Your mission: prove cache independence

- [ ] Time one clean job with caching disabled — Record dependency-install and total duration.
- [ ] Enable the package-manager cache with a lockfile-derived key — Do not remove the clean install command.
- [ ] Run twice and inspect hit metadata — The second equivalent run should restore; compare transfer and install time.
- [ ] Change the lockfile and run again — Confirm a new key or safe fallback, then prove tests and installed versions remain correct.

A trustworthy pipeline passes on a cold cache and merely finishes sooner on a warm one.

- **Every run reports a cache miss.**
  Compare key components and save conditions; volatile values such as commit SHA make every key unique.
- **A cache hit still saves no time.**
  Measure archive transfer versus clean download and confirm the cached path is what the package manager actually uses.
- **Dependency behavior changes after a lockfile update.**
  Ensure the lockfile hash is in the key and the clean install still runs; clear misleading broad fallbacks.
- **Forked code can read sensitive cached files.**
  Never cache credentials or generated secret-bearing configuration. Anyone able to open a pull request may influence or access cache behavior under documented scopes.

### Where to check

- **Resolved cache key and hit status** — exact match, fallback match, or miss.
- **Cached path** — package-manager store versus an unrelated directory.
- **Lockfile hash and runtime axis** — key invalidation inputs.
- **Restore/save timings and archive size** — whether optimization is net positive.
- **Cold-cache result** — correctness must survive eviction.

### Worked example: the cache that never hit

1. A key includes `github.sha`, so every commit produces a unique exact key.
2. Runs save hundreds of megabytes but never restore them on the next commit.
3. The team replaces SHA with a lockfile hash and includes OS and runtime.
4. Commits that do not change dependencies now share a cache; lockfile changes create a new key.
5. `npm ci` remains in place, so both hits and misses produce the reviewed dependency tree.

**Quiz.** Which cache key is safest for a Node dependency cache?

- [ ] dependencies
- [ ] the full commit SHA only
- [x] runner OS + Node version + package manager + lockfile hash
- [ ] the current minute

*OS and runtime prevent incompatible reuse, the package-manager label clarifies the path, and the lockfile hash invalidates the cache when dependencies change.*

- **Cache hit** — A matching reusable input archive was restored; it is not proof the build or tests pass.
- **Cache miss** — Normal operation. The pipeline must install correctly and may save a new cache afterward.
- **Why hash the lockfile?** — Dependency changes produce a new key while equivalent commits can reuse downloads.
- **Cache versus artifact** — Cache accelerates later runs; artifact preserves outputs or evidence from this run.
- **Cold-cache invariant** — Removing every cache may slow the job but must not change its correctness.

### Challenge

Audit one cache key and path. Predict five changes that should invalidate it and five that should not,
then test a cold run, exact hit, lockfile change, and runtime change while measuring total job time.

### Ask the community

> Cache [name] uses key [components] and path [path]. Logs show [hit/miss], restore [seconds], install [seconds], archive [size]. Which key or path is wrong?

Include measurements; a green "cache restored" line alone does not prove the cache is useful.

- [GitHub Docs — Dependency caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)
- [actions/cache — official repository](https://github.com/actions/cache)

🎬 [Caching Dependencies to Speed Up Workflows in GitHub Actions — CoderDave](https://www.youtube.com/watch?v=BDQivAobxKA) (6 min)

- Caching is a performance optimization; correctness must survive a cache miss or eviction.
- Keys should reflect compatibility and dependency content, not every commit.
- Keep the lockfile-driven install even after reusable downloads are restored.
- Measure transfer, installation, hit rate, size, and total duration before claiming a win.
- Caches are not artifacts and must never contain credentials or indispensable evidence.


## Related notes

- [[Notes/automation-in-cicd/github-actions/workflow-basics|Workflow basics]]
- [[Notes/automation-in-cicd/github-actions/matrix-runs|Matrix runs]]
- [[Notes/automation-in-cicd/running-tests-in-ci/artifacts|Artifacts]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/github-actions/caching.mdx`_
