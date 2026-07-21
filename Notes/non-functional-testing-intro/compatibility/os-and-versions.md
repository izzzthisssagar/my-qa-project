---
title: "OS / versions"
tags: ["non-functional-testing-intro", "compatibility", "track-c"]
updated: "2026-07-18"
---

# OS / versions

*Test operating-system and version boundaries with a dated support policy, upgrade paths, platform changes, and lifecycle evidence.*

> An application may work on a phone model today and fail after the same phone installs tomorrow's OS.
> Permissions, storage, background work, certificates, keyboards, and system controls evolve underneath
> the product. Compatibility is a moving boundary, not a sticker on the device.

> **In real life**
>
> OS versions are editions of a rulebook. The field looks familiar, but a new edition can change how play
> restarts, which equipment is permitted, or when a warning appears. Test the supported editions and the
> moment teams move between them.

**OS-version compatibility**: OS-version compatibility testing evaluates supported operating-system releases and transitions, including clean install, update, upgrade, permissions, lifecycle, platform behavior changes, and minimum-version boundaries. Support claims must be dated because vendor releases and policies change.

## Test boundaries and transitions

State a minimum supported version and a current range using product policy, audience data, store or
vendor requirements, and platform documentation. High-value rows are the minimum supported version,
latest stable version, upcoming beta when appropriate, and versions where a relevant behavior changed.
Test fresh install, app update, OS upgrade with existing data, permission changes, background/foreground,
notifications, links, files, and uninstall/reinstall behavior.

> **Tip**
>
> Subscribe to official Android, Apple, Microsoft, and browser platform change notes relevant to the
> product. Convert each breaking or privacy-related change into an explicit scenario before release.

> **Common mistake**
>
> "Supports Android" or "supports iOS" is not testable. Name version ranges and dates, and do not assume a
> successful clean install covers upgrades with old databases, cached credentials, or previously granted
> permissions.

![Three smartphones displaying different Android Jelly Bean Easter egg screens](os-and-versions.jpg)
*Android Jelly Bean — Galaxy Note 10 and Google, Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Android_Jelly_Bean.jpg)*
- **Older platform presentation** — Minimum supported releases deserve explicit journey and performance coverage.
- **Same family, different behavior** — Point releases and vendor builds can alter system UI, permissions, and lifecycle details.
- **Newer platform state** — Latest releases expose behavior changes early; upcoming betas are risk signals, not production guarantees.
- **Upgrade path between versions** — Preserved user data, permissions, sessions, and migrations are often riskier than a clean install.

**A version boundary test**

1. **Publish a dated supported-version range** — Make the claim precise enough to test and retire.
2. **Read official behavior-change notes** — Target permission, storage, lifecycle, privacy, and API changes relevant to the product.
3. **Test clean install and upgrade paths** — Preserve real prior state, data, permissions, and cached credentials.
4. **Reassess on every platform release** — Update the matrix and communicate deprecation before dropping support.

*An OS-version boundary oracle (Python)*

```python
checks = {
    "minimum_version": True,
    "latest_stable": True,
    "upgrade_preserves_data": True,
    "permission_change_handled": True,
}
for name, passed in checks.items(): print(name + "=" + ("PASS" if passed else "FAIL"))
result = "PASS" if all(checks.values()) else "FAIL"
assert result == "PASS", "OS version boundary rejected"
print("RESULT=" + result)
```

*An OS-version boundary oracle (Java)*

```java
import java.util.LinkedHashMap;
import java.util.Map;
public class Main {
    public static void main(String[] args) {
        Map<String, Boolean> checks = new LinkedHashMap<>();
        checks.put("minimum_version", true);
        checks.put("latest_stable", true);
        checks.put("upgrade_preserves_data", true);
        checks.put("permission_change_handled", true);
        boolean ok = true;
        for (var e : checks.entrySet()) { System.out.println(e.getKey() + "=" + (e.getValue() ? "PASS" : "FAIL")); ok &= e.getValue(); }
        String result = ok ? "PASS" : "FAIL";
        if (!result.equals("PASS")) throw new AssertionError("OS version boundary rejected");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Test one version transition

- [ ] Record the dated support range — Identify the minimum, latest stable, and the platform change that threatens the feature.
- [ ] Create meaningful prior state — Install the previous release, sign in, create data, set permissions, and background the app.
- [ ] Upgrade the OS or app — Preserve state and observe migrations, permissions, notifications, links, and lifecycle.
- [ ] Run the critical journey and recovery — Verify data integrity, error handling, and behavior after restart.

- **A clean install passes but upgraded users crash.**
  Reproduce with the old schema and cached state, inspect migrations, and retain upgrade fixtures in regression coverage.
- **Permissions silently reset after an OS update.**
  Test denied, granted, one-time, and changed permission states; explain recovery instead of assuming prior grants persist.
- **Nobody knows whether an old version is supported.**
  Create an owner-approved, dated version policy and map each promised row to evidence and deprecation communication.

### Where to check

- Official platform release notes and behavior-change documentation.
- App/store minimum requirements and internal supported-version policy.
- Install, update, OS-upgrade, migration, permission, lifecycle, notification, and deep-link paths.
- Crash and analytics segmentation by exact OS and app version.

### Worked example: photos permission changed under the app

1. A photo uploader passed on the team's current OS with broad library access.
2. The next platform version introduces a more limited permission state; upgraded users select a photo
   but the app assumes the entire library remains readable.
3. The tester reproduces with preserved permissions and existing draft data, then records exact versions.
4. The app handles limited access and offers a clear recovery path; clean and upgrade flows are retested.

**Quiz.** Which scenario adds the most version-specific evidence?

- [ ] Only a clean install on the newest OS
- [x] An upgrade from a supported old version with data and permissions preserved
- [ ] A screenshot of the home page
- [ ] A generic claim that Android works

*Transitions carry schemas, sessions, permissions, caches, and user data across changing platform rules, exposing risks a clean install cannot.*

- **Version claim** — A dated range with minimum and current releases, not a platform name alone.
- **Boundary rows** — Minimum supported, latest stable, relevant behavior-change versions, and beta when justified.
- **Upgrade evidence** — Prior app data, sessions, permissions, caches, migrations, and post-upgrade critical journeys.

### Challenge

Take one official platform behavior change and design clean-install, upgrade, denied-permission, and recovery scenarios.

- [Android Developers — Platform releases](https://developer.android.com/about/versions)
- [Apple Developer — iOS and iPadOS release notes](https://developer.apple.com/documentation/ios-ipados-release-notes)
- [Android Developers — Testing platform changes in Android 11](https://www.youtube.com/watch?v=82einkyFns4)

🎬 [Testing platform changes in Android 11](https://www.youtube.com/watch?v=82einkyFns4) (4 min)

- Make OS support precise and dated because the boundary moves.
- Target minimum, latest, and behavior-change versions rather than every release uniformly.
- Upgrade paths with preserved state reveal risks clean installs miss.
- Turn official platform changes into explicit permission, lifecycle, storage, and recovery scenarios.


## Related notes

- [[Notes/non-functional-testing-intro/compatibility/cross-device|Cross-device]]
- [[Notes/non-functional-testing-intro/compatibility/cross-browser|Cross-browser]]
- [[Notes/operating-systems-and-files/installing-and-managing-software/updates|Updates]]


---
_Source: `packages/curriculum/content/notes/non-functional-testing-intro/compatibility/os-and-versions.mdx`_
