---
title: "Fragmentation"
tags: ["mobile-testing", "device-and-os-matrix", "track-c"]
updated: "2026-07-20"
---

# Fragmentation

*Why Android and iOS each spread a real user base across many device models, screen sizes, and OS versions, and why that shape of the problem matters more than any single stat.*

> A build that passes every check on one phone can still crash, misrender, or silently drop a permission
> prompt the moment it reaches a different manufacturer's skin, a smaller screen, or an OS release from two
> years ago. The app never changed. The population running it did.

> **In real life**
>
> Picture a cobbler asked to fit an entire stadium crowd for a big event. There is no single standard foot:
> some fans arrive in shoes fresh off this season's line, others are still wearing a pair from a decade ago
> that has been resoled twice, and every batch came out of a different factory with its own last and
> sizing quirks. Fitting "a shoe" is meaningless. The cobbler has to fit the actual feet in the building,
> grouped into sizes and widths that cover the most people with the fewest pairs.

**Fragmentation**: Device and OS fragmentation is the spread of a real mobile audience across many combinations of hardware, screen size and density, manufacturer skin, and operating-system version, rather than one uniform platform. It exists on Android and iOS alike, though the shape of the spread differs between them.

## Two ecosystems, two shapes of the same problem

Android fragmentation comes from an open licensing model: many OEMs (Samsung, Google, Xiaomi, OnePlus,
and others) each ship their own hardware, screen sizes and densities, and a manufacturer skin layered over
stock Android. Two phones on the "same" Android version can behave differently because the OEM changed
keyboard height, notification handling, background-process limits, or default font scaling. OS version
adoption is also uneven — a flagship released this year and a budget phone still running an OS release
from several years back can both be active in the same audience at once.

iOS fragmentation is narrower but still real. Apple controls a much smaller hardware lineup and pushes
OS updates directly to devices, so version adoption climbs faster than on Android. The fragmentation that
remains is generational: older iPhone models drop support for the newest OS release, some features are
gated to newer chips, and a portion of any real user base is always a version or two behind the latest
release rather than instantly current. Treating "iOS" as one monolithic target is as much a mistake as
treating "Android" as one.

> **Tip**
>
> Describe a fragmentation gap in concrete terms: manufacturer, model, OS version, screen density, and the
> exact behavior observed. "Broken on Android" is not a finding; "notification action buttons missing on a
> OneUI 6 device running Android 14 at 3x density" is one a developer can act on.

> **Common mistake**
>
> Do not treat the newest flagship as a stand-in for the whole platform. The newest device usually has the
> most RAM, the fastest chip, and the latest OS — it hides exactly the low-memory, older-OS, small-screen
> failures fragmentation is warning you about.

![Four smartphones lying face down in a row: an LG phone, a OnePlus One running CyanogenMod, a Samsung Galaxy Note 4, and an Apple iPhone 6](fragmentation.jpg)
*OnePlus One vs LG G3 vs Apple iPhone 6 Plus vs Samsung Galaxy Note 4 — Maurizio Pesce, Wikimedia Commons, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Smartphones_back.jpg)*
- **One manufacturer, one skin** — LG's camera module, materials, and firmware are unique to LG; a bug here says nothing about the other three.
- **Community firmware** — This OnePlus One shipped running CyanogenMod, a modified Android build — a reminder that even the OS layer itself can vary underneath the same version number.
- **A different OEM skin again** — Samsung's own Android skin changes defaults for keyboard height, notifications, and battery behavior versus stock Android.
- **A separate platform entirely** — The iPhone runs iOS, not Android — its own hardware lineup, its own version-adoption curve, its own fragmentation shape.

**Naming the fragmentation you actually have**

1. **Pull real device and OS-version analytics** — Your actual audience, not a generic industry chart, defines which combinations exist.
2. **Group by manufacturer, screen, and OS version** — Cluster similar hardware instead of listing every individual model.
3. **Flag the outliers on purpose** — Smallest screen, oldest supported OS, most customized skin — these are where fragmentation bugs concentrate.
4. **Re-check the shape periodically** — OS adoption and device mix shift over time; a fragmentation picture from a year ago is already stale.

*A fragmentation-coverage calculator (Python)*

```python
devices = {
    "pixel8_android15": 0.22,
    "galaxyS23_android14": 0.18,
    "galaxyA14_android13": 0.15,
    "iphone15_ios18": 0.20,
    "iphone12_ios17": 0.12,
    "redmiNote12_android13": 0.13,
}
covered = {
    "pixel8_android15": True,
    "galaxyS23_android14": True,
    "galaxyA14_android13": True,
    "iphone15_ios18": True,
    "iphone12_ios17": False,
    "redmiNote12_android13": False,
}
total_share = sum(devices.values())
covered_share = sum(share for name, share in devices.items() if covered[name])
for name, share in devices.items():
    status = "COVERED" if covered[name] else "GAP"
    print(name + "=" + status + " (" + str(round(share * 100)) + "%)")
coverage_pct = round(covered_share / total_share * 100)
print("COVERAGE=" + str(coverage_pct) + "%")
result = "PASS" if coverage_pct >= 70 else "FAIL"
assert result == "PASS", "fragmentation coverage below threshold"
print("RESULT=" + result)
```

*A fragmentation-coverage calculator (Java)*

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        Map<String, Double> devices = new LinkedHashMap<>();
        devices.put("pixel8_android15", 0.22);
        devices.put("galaxyS23_android14", 0.18);
        devices.put("galaxyA14_android13", 0.15);
        devices.put("iphone15_ios18", 0.20);
        devices.put("iphone12_ios17", 0.12);
        devices.put("redmiNote12_android13", 0.13);

        Map<String, Boolean> covered = new LinkedHashMap<>();
        covered.put("pixel8_android15", true);
        covered.put("galaxyS23_android14", true);
        covered.put("galaxyA14_android13", true);
        covered.put("iphone15_ios18", true);
        covered.put("iphone12_ios17", false);
        covered.put("redmiNote12_android13", false);

        double totalShare = 0;
        double coveredShare = 0;
        for (Map.Entry<String, Double> e : devices.entrySet()) {
            totalShare += e.getValue();
            if (covered.get(e.getKey())) coveredShare += e.getValue();
        }
        for (Map.Entry<String, Double> e : devices.entrySet()) {
            String status = covered.get(e.getKey()) ? "COVERED" : "GAP";
            long pct = Math.round(e.getValue() * 100);
            System.out.println(e.getKey() + "=" + status + " (" + pct + "%)");
        }
        long coveragePct = Math.round(coveredShare / totalShare * 100);
        System.out.println("COVERAGE=" + coveragePct + "%");
        String result = coveragePct >= 70 ? "PASS" : "FAIL";
        if (!result.equals("PASS")) throw new AssertionError("fragmentation coverage below threshold");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Map your own fragmentation shape

- [ ] Pull device and OS-version analytics — Use your own product analytics, not a generic industry chart, as the source of truth.
- [ ] Group into manufacturer/screen/OS clusters — Collapse near-identical rows so the list stays a decision tool, not a spreadsheet nobody reads.
- [ ] Name your two outliers — The smallest screen and the oldest supported OS version in your real audience — write down what they are.
- [ ] Date the snapshot — Fragmentation shifts as OS adoption climbs and new hardware ships; note when this picture was taken.

- **A bug only reproduces on one manufacturer's phones.**
  Check for OEM-specific skin behavior — keyboard height, notification channels, background-process limits, and default font scale are common culprits.
- **A feature works on the newest OS but not an older supported one.**
  Confirm the minimum supported OS version and test against it directly instead of assuming forward compatibility.
- **Layout looks fine on your team's phones but breaks for users.**
  Compare screen size and density against real analytics; a team's devices are rarely representative of the smallest or most dense screens in the field.

### Where to check

- Your own product analytics for device model, OS version, and screen-density distribution.
- Android's per-OEM release notes and iOS's published version-adoption data.
- Crash and ANR/exception reports segmented by device and OS version.
- [[mobile-testing/device-and-os-matrix/building-a-matrix]] for turning this shape into a concrete, risk-based device list.

### Worked example: a notification bug that only one OEM skin exposes

1. A release adds an action button to a notification and passes on the team's own devices.
2. Analytics show a meaningful slice of the audience is on an OEM skin the team does not own.
3. On that skin, the notification channel default suppresses action buttons unless the user has opted in.
4. The finding names the exact OEM, skin version, and OS version, and the team adds a fallback path that
   does not depend on the action button being visible.

**Quiz.** Which statement best describes fragmentation on Android versus iOS?

- [ ] Android has fragmentation and iOS does not
- [ ] iOS has fragmentation and Android does not
- [x] Both have fragmentation, but it comes from different sources — many OEMs and skins on Android, a narrower device lineup with an uneven version-adoption curve on iOS
- [ ] Fragmentation only matters for automated tests, not manual testing

*Both platforms spread a real audience across meaningfully different combinations; the shape of the spread differs because of how each ecosystem is built.*

- **Android fragmentation source** — Many OEMs, each with their own hardware, skin, and defaults, plus uneven OS-version adoption across devices.
- **iOS fragmentation source** — A narrower device lineup, but real generational and OS-version-adoption spread — never one monolithic target.
- **Fragmentation finding format** — Manufacturer, model, OS version, screen density, and the exact observed behavior — not a vague platform name.

### Challenge

Pull your product's real device and OS-version analytics, group them into clusters, and name the two combinations most likely to be under-tested right now.

- [Android Developers — Support Different Pixel Densities](https://developer.android.com/training/multiscreen/screendensities)
- [BrowserStack — What Is Android Fragmentation](https://www.browserstack.com/guide/what-is-android-fragmentation)
- [All About Operating Systems — How Does Android Fragmentation Differ From iOS?](https://www.youtube.com/watch?v=3HG_Ol4BeYw)

🎬 [How Does Android Fragmentation Differ From iOS?](https://www.youtube.com/watch?v=3HG_Ol4BeYw) (4 min)

- Fragmentation is the real spread of hardware, screen, and OS-version combinations behind any mobile audience.
- Android's fragmentation comes from many OEMs and skins; iOS's comes from a narrower lineup with an uneven version-adoption curve.
- The newest flagship in the office hides the exact low-memory, older-OS, small-screen failures fragmentation causes.
- A useful fragmentation finding names manufacturer, model, OS version, density, and the exact behavior observed.


## Related notes

- [[Notes/mobile-testing/device-and-os-matrix/building-a-matrix|Building a matrix]]
- [[Notes/mobile-testing/device-and-os-matrix/real-vs-emulated|Real vs emulated]]
- [[Notes/mobile-testing/device-and-os-matrix/device-farms|Device farms]]


---
_Source: `packages/curriculum/content/notes/mobile-testing/device-and-os-matrix/fragmentation.mdx`_
