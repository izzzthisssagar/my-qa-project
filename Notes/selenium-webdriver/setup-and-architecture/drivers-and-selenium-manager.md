---
title: "Drivers and Selenium Manager"
tags: ["selenium", "webdriver", "selenium-manager", "driver-management", "track-d"]
updated: "2026-07-18"
---

# Drivers and Selenium Manager

*Resolve the correct browser driver by separating browser, binding, driver executable, cache, PATH, and Selenium Manager decisions.*

> “Chrome is installed” does not prove Selenium can start Chrome. The binding still needs a compatible,
> executable driver, and the first driver found may be the wrong one. Modern Selenium automates much of
> that selection, but automation does not erase PATH, cache, network, proxy, permission, or CPU mistakes.

> **In real life**
>
> A workshop has a machine, an operator's instruction book, and a tray of adapters. Selenium Manager is
> the tool clerk: it identifies the machine version, reports a suspect adapter already sitting on the
> PATH shelf, reuses a managed one from storage, or obtains one when policy and network access allow it.
> By default the clerk does not throw away that PATH adapter for you; configuration decides whether to
> skip that shelf.

**Selenium Manager**: Selenium Manager is Selenium's bundled command-line tool for discovering, resolving, downloading, and caching compatible drivers and, in supported workflows, browsers when the bindings need automated management.

## Four pieces, four different jobs

The **browser** renders and executes the page. The browser-specific **driver executable** exposes the
WebDriver remote-end interface and communicates with that browser. The Selenium **language binding**
provides `webdriver.Chrome()` or `new ChromeDriver()` to your test. **Selenium Manager** supports the
binding when no usable driver location has already been supplied.

Current Selenium bindings invoke Selenium Manager as a fallback when a driver is unavailable through
the normal configuration path. Manager discovers the local browser version, resolves compatible
metadata, stores downloads in its cache, and reuses cached artifacts. That convenient path can need
network access on first resolution. Proxies, offline runners, firewalls, filesystem permissions, and
CPU architecture can therefore decide whether startup succeeds.

An explicit driver path or a stale executable earlier on PATH can change resolution. Treat manual
pinning as an intentional override: record why it exists, keep its browser compatibility current, and
remove obsolete entries. A managed cache and a manually pinned `Service` path are different sources
of truth; logs should say which one won. Current Selenium Manager warns when a PATH driver major does
not match the discovered browser, but returns that PATH driver by default. Set
`skip-driver-in-path = true` (or `SE_SKIP_DRIVER_IN_PATH=true`) when your policy is to ignore PATH and
use managed resolution instead.

> **Tip**
>
> Turn on Selenium Manager debug logging during diagnosis and record browser version, discovered PATH
> candidates, selected driver path, cache location, proxy settings, platform, and CPU architecture.

> **Common mistake**
>
> Downloading another driver without checking the selected path. A stale PATH entry can keep winning,
> so the new compatible file sits unused while Selenium launches the old incompatible executable.

![A white continental electrical adapter with two metal pins and several socket openings on a wooden table](drivers-and-selenium-manager.jpg)
*Continental adaptor plug original — plugwash, public domain. [Source](https://commons.wikimedia.org/wiki/File:Continental_adaptor_plug_original.jpg)*
- **Installed browser** — One metal pin represents the concrete browser version and platform already present on the machine.
- **Driver candidate** — The second pin represents an available driver executable; physical proximity does not prove that its version is compatible.
- **Compatibility check** — The central fitting is the decisive boundary: browser and driver must match the supported interface before a session can start.
- **Managed resolution** — The lower opening represents another resolution source. With skip-driver-in-path enabled, Selenium Manager can ignore the PATH shelf and reuse a compatible cached driver.

**How a driver is resolved**

1. **Read configuration** — Honor an intentional explicit driver or Service location.
2. **Inspect candidates** — Discover PATH and cached drivers with their versions and platforms.
3. **Report compatibility** — Warn when a PATH driver major does not match the installed browser; default behavior may still return that PATH driver.
4. **Resolve if needed** — Use metadata and network or proxy access when no compatible local candidate exists.
5. **Launch and report** — Start the selected driver and log the decisive source and reason.

The playgrounds model a **stricter bootstrap policy** with fixed inputs: ignore an incompatible PATH
candidate and accept a compatible cached candidate, equivalent to enabling `skip-driver-in-path` and
then validating the managed result. They are not a reimplementation of Selenium Manager's default
PATH behavior, and they never read your real PATH, cache, browser, or network.

*Run it — reject stale PATH and select cache (Python)*

```python
from dataclasses import dataclass

BROWSER_MAJOR = 126
NETWORK_AVAILABLE = False

@dataclass(frozen=True)
class Candidate:
    source: str
    major: int

@dataclass(frozen=True)
class Resolution:
    selected: Candidate | None
    rejections: tuple[str, ...]
    reason: str

def compatible(browser_major: int, driver_major: int) -> bool:
    return browser_major == driver_major

def resolve(browser_major: int, candidates: list[Candidate], network_available: bool) -> Resolution:
    rejections = []
    for candidate in candidates:
        if compatible(browser_major, candidate.major):
            return Resolution(candidate, tuple(rejections), f"{candidate.source} compatible major={candidate.major}")
        rejections.append(
            f"{candidate.source} incompatible driver={candidate.major} browser={browser_major}"
        )
    if network_available:
        downloaded = Candidate("network", browser_major)
        return Resolution(downloaded, tuple(rejections), f"network compatible major={browser_major}")
    return Resolution(None, tuple(rejections), "network unavailable")

candidates = [Candidate("path", 125), Candidate("cache", 126)]
resolution = resolve(BROWSER_MAJOR, candidates, NETWORK_AVAILABLE)

expected_rejection = "path incompatible driver=125 browser=126"
path_rejected = expected_rejection in resolution.rejections
cache_selected = resolution.selected == Candidate("cache", 126)

assert path_rejected, "the incompatible PATH driver must be rejected explicitly"
assert cache_selected, "the compatible cached driver must be selected"
assert resolution.reason == "cache compatible major=126", "the decisive reason must identify the cache"

print(f"REJECT {expected_rejection}")
print(f"SELECT {resolution.reason}")
print("RESULT path_rejected=true cache_selected=true")
```

*Run it — reject stale PATH and select cache (Java)*

```java
import java.util.Arrays;

public class Main {
    static final int BROWSER_MAJOR = 126;
    static final boolean NETWORK_AVAILABLE = false;

    record Candidate(String source, int major) {}
    record Resolution(Candidate selected, String[] rejections, String reason) {}

    static boolean compatible(int browserMajor, int driverMajor) {
        return browserMajor == driverMajor;
    }

    static Resolution resolve(int browserMajor, Candidate[] candidates, boolean networkAvailable) {
        String[] rejections = new String[candidates.length];
        int rejectionCount = 0;
        for (Candidate candidate : candidates) {
            if (compatible(browserMajor, candidate.major())) {
                return new Resolution(
                    candidate,
                    Arrays.copyOf(rejections, rejectionCount),
                    candidate.source() + " compatible major=" + candidate.major()
                );
            }
            rejections[rejectionCount++] =
                candidate.source() + " incompatible driver=" + candidate.major() + " browser=" + browserMajor;
        }
        if (networkAvailable) {
            Candidate downloaded = new Candidate("network", browserMajor);
            return new Resolution(
                downloaded,
                Arrays.copyOf(rejections, rejectionCount),
                "network compatible major=" + browserMajor
            );
        }
        return new Resolution(null, Arrays.copyOf(rejections, rejectionCount), "network unavailable");
    }

    static boolean contains(String[] values, String expected) {
        return Arrays.asList(values).contains(expected);
    }

    public static void main(String[] args) {
        Candidate[] candidates = {new Candidate("path", 125), new Candidate("cache", 126)};
        Resolution resolution = resolve(BROWSER_MAJOR, candidates, NETWORK_AVAILABLE);

        String expectedRejection = "path incompatible driver=125 browser=126";
        boolean pathRejected = contains(resolution.rejections(), expectedRejection);
        boolean cacheSelected = new Candidate("cache", 126).equals(resolution.selected());

        if (!pathRejected) {
            throw new AssertionError("the incompatible PATH driver must be rejected explicitly");
        }
        if (!cacheSelected) {
            throw new AssertionError("the compatible cached driver must be selected");
        }
        if (!resolution.reason().equals("cache compatible major=126")) {
            throw new AssertionError("the decisive reason must identify the cache");
        }

        System.out.println("REJECT " + expectedRejection);
        System.out.println("SELECT " + resolution.reason());
        System.out.println("RESULT path_rejected=true cache_selected=true");
    }
}
```

### Your first time: Your mission: prove which driver Selenium launches

- [ ] Identify the browser — Record browser version, channel, operating system, and CPU architecture.
- [ ] Inventory overrides — Check explicit Service paths, PATH entries, and whether skip-driver-in-path / SE_SKIP_DRIVER_IN_PATH is enabled.
- [ ] Inspect the cache — Locate Selenium Manager's cache and compare cached driver versions and permissions.
- [ ] Read the decision log — Enable debug output and capture the selected executable plus the reason it won.

You now know the executable actually launched, not merely the one you downloaded last.

- **The driver cannot be found or executed.**
  Check the resolved path, execute permission, quarantine or policy blocks, OS, and CPU architecture.
- **The browser rejects the driver at startup.**
  Compare browser and selected driver versions. Remove or update the stale PATH entry, or enable skip-driver-in-path so managed resolution can use a compatible cache/download.
- **The first run fails in CI but later local runs pass.**
  Check whether CI needs network and proxy access to populate an empty managed cache, or pre-provision a compatible artifact.
- **An offline run tries to download a driver.**
  Verify that a compatible cached or explicitly pinned driver exists and that configuration points to the intended source.
- **A manually pinned driver is ignored.**
  Inspect the language binding's Service configuration and debug logs rather than assuming PATH precedence.

### Where to check

- **Selenium Manager debug output** — discovered browser, metadata, cache, downloads, warnings, and selected path.
- **Language-binding logs** — whether Selenium Manager ran or an explicit Service configuration won first.
- **Shell PATH** — every driver executable, in actual search order, with version and permissions.
- **Managed cache** — cached metadata and binaries for the current user and platform.
- **Runner environment** — proxy variables, certificates, outbound access, filesystem policy, OS, and CPU architecture.

### Worked example: the compatible driver that Selenium never used

1. Chrome updates to major version 126 on a CI runner.
2. The team downloads a compatible driver into the Selenium Manager cache.
3. An older major-125 driver remains earlier on PATH and is still executable.
4. Manager warns about the major mismatch but returns the PATH driver by default; startup fails.
5. Removing the obsolete entry or setting `SE_SKIP_DRIVER_IN_PATH=true` lets managed resolution use
   the compatible cached major-126 driver without network access.

**Quiz.** A runner is offline, PATH contains driver 125, the cache contains driver 126, the browser is major 126, and skip-driver-in-path is enabled. What should managed resolution do?

- [ ] Launch the PATH driver because PATH always wins
- [ ] Download another driver despite being offline
- [x] Reject the incompatible PATH driver and select the compatible cached driver
- [ ] Replace the Selenium language binding with a browser

*The skip setting prevents the stale PATH driver from winning. Managed resolution can then reuse the fitting cached driver without network access.*

- **Browser driver** — A browser-specific WebDriver remote end that translates commands to the browser's automation interface.
- **Selenium binding** — The Java, Python, or other client library used by test code.
- **Selenium Manager** — The bundled tool used by bindings to automate driver and supported browser discovery and management.
- **Managed cache** — Selenium Manager's reusable local store for resolved metadata and downloaded artifacts.
- **Manual override** — An intentionally supplied executable path that becomes a separate source of truth to maintain.

### Challenge

Add an explicit pinned candidate before PATH, then model a machine with the wrong CPU architecture.
Require the resolver to preserve every rejection reason and select only a candidate compatible with
browser major, operating system, and architecture.

### Ask the community

> Browser [version/platform] fails to start. Selenium selected driver [path/version] from [Service/PATH/cache], Manager logged [decisive line], and network/proxy state is [state]. What resolution input should I verify next?

Share paths and versions, but remove usernames, access tokens, proxy credentials, and private hostnames.

- [Selenium documentation — Selenium Manager](https://www.selenium.dev/documentation/selenium_manager/)
- [Selenium documentation — Driver sessions and location](https://www.selenium.dev/documentation/webdriver/drivers/)
- [Selenium documentation — WebDriver troubleshooting](https://www.selenium.dev/documentation/webdriver/troubleshooting/)

🎬 [Selenium Manager: Automated Driver & Browser Management for Selenium WebDriver - Boni García](https://www.youtube.com/watch?v=7MWuXlt6BXE) (42 min)

- Browser, driver executable, Selenium binding, and Selenium Manager have distinct responsibilities.
- Manager warns about a mismatched PATH driver but returns it by default; skip-driver-in-path changes that policy.
- A compatible cache enables offline reuse; first-time resolution may need network and proxy access.
- PATH and manual Service overrides can bypass or change managed resolution.
- Debug logs should identify the selected path and the decisive reason.


## Related notes

- [[Notes/automation/frameworks/selenium-java|Selenium with Java]]
- [[Notes/selenium-webdriver/setup-and-architecture/webdriver-architecture|WebDriver architecture]]
- [[Notes/selenium-webdriver/setup-and-architecture/first-script-java|First script (Java)]]
- [[Notes/selenium-webdriver/setup-and-architecture/first-script-python|First script (Python)]]


---
_Source: `packages/curriculum/content/notes/selenium-webdriver/setup-and-architecture/drivers-and-selenium-manager.mdx`_
