---
title: "Store testing"
tags: ["mobile-testing", "mobile-specifics", "track-c"]
updated: "2026-07-21"
---

# Store testing

*What QA verifies before an App Store or Play Store submission -- metadata accuracy, screenshot rules, crash-free rate thresholds, semantic versioning, and how staged rollouts and phased releases limit the blast radius of a bad build.*

> A build passes every test the team has, gets submitted, and comes back rejected two days later for a
> screenshot showing a login screen instead of the app in actual use. The code was never the problem. Nobody
> on the team had checked the listing itself against the store's own rules before hitting submit.

> **In real life**
>
> Think of an old apothecary shop window: every bottle on display carries its own label naming exactly what's
> inside, arranged in a consistent, curated row behind the glass. A shopper decides whether to walk in based on
> that window alone, long before they ever touch a bottle. An app's store listing is that window — the icon,
> title, screenshots, and version notes are what a user judges before they ever open the app, and a shop that
> lets a mislabeled or inconsistent bottle into the display risks the whole window's credibility, not just that
> one item.

**Store testing**: Store testing is the QA pass that verifies an app build and its listing meet a store's submission requirements -- accurate metadata, compliant screenshots, a correctly incremented version number, and acceptable crash and stability metrics -- before the build is submitted for review or rolled out to users.

## The listing is reviewed as strictly as the code

App Store review checks far more than whether the binary runs. Apple's guidelines explicitly require
screenshots to "show the app in use, and not merely the title art, login page, or splash screen," and reject
apps for incomplete or inaccurate metadata — hidden or undocumented features, marketing claims the app
doesn't actually deliver on, or generic reviewer notes for a non-obvious feature. Guideline 2.1 covers the
build itself: it must be tested on-device for bugs and stability before submission, with no placeholder
content and no crashes on first launch. Google Play runs its own, separate policy review, but adds an
ongoing production signal Apple's one-time review doesn't have in the same form: Android vitals tracks a
user-perceived crash rate in production, and Play Console currently treats 1.09% or more of daily active
users hitting a crash — across all devices — as a "bad behavior" threshold that can make an app less
discoverable in the store.

Versioning ties directly into what a store submission actually is. Android's `versionCode` is an internal
integer that must strictly increase with every submitted build, while `versionName` is the human-readable
string (commonly semantic — major.minor.patch) a user sees; iOS splits the same idea into
`CFBundleVersion` (build number) and `CFBundleShortVersionString` (the user-facing version). A QA pass before
submission confirms both numbers actually moved, not just one, since a store will reject a build with a
build number it has already seen even if the marketing version string changed.

Neither platform releases a new version to everyone instantly by default if the team chooses otherwise. Play
Console's staged rollout lets a release reach a percentage of users first, with no automatic increase — a
team must manually raise the percentage or halt the rollout entirely if problems appear, and halting stops
new users from getting the build without pulling it from existing ones. Apple's phased release for automatic
updates follows a fixed seven-day schedule instead: 1%, 2%, 5%, 10%, 20%, 50%, then 100%, though a user can
always manually download the update early from the store regardless of what percentage the phased schedule
has reached. Both exist for the same reason: to limit how many users a bad build reaches before something
goes wrong publicly.

> **Tip**
>
> Before submitting, walk the listing exactly as a reviewer would: read every screenshot for whether it shows
> the app in actual use, confirm both the build number and the user-facing version string incremented, and
> check that anything the description claims — including in-app purchases and any non-obvious feature — is
> something a reviewer can actually find and use in the build being submitted.

> **Common mistake**
>
> Do not treat "the build works" as equivalent to "the submission is ready." A perfectly functional build can
> still be rejected outright for stale screenshots, an unincremented version number, or metadata that no
> longer matches what the app actually does — none of which a functional test suite will ever catch.

![A Kiehl's storefront window reading 'KIEHL'S ESTABLISHED 1851' with two shelves of labeled apothecary bottles arranged behind the glass](store-testing.jpg)
*Kiehl's Storefront Window — Plot Spoiler, Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:Kiehl%27s_Storefront_Window.jpg)*
- **The listing itself** — The shop's own name and founding date painted right on the glass is the first thing a passerby reads, before ever touching a bottle -- the same role an app's title, icon, and short description play before a user ever installs it.
- **One product, its own label** — Each bottle carries its own name and contents label, checked individually -- the shelf-level equivalent of confirming an app's screenshots, version number, and metadata are accurate for this specific submission, not just accurate in general.
- **A curated, consistent row** — The bottom shelf presents a consistent style across many items at once -- the same discipline a staged rollout or phased release applies, presenting one verified build to a steadily growing audience instead of everyone at once.
- **An item at the edge of the display** — The bottle tucked at the far edge of the window still has to meet the same labeling standard as the ones in the center -- an edge-case feature or a rarely-opened screen in an app still has to pass the same review bar as the core flow.

**From a finished build to users actually seeing it**

1. **QA verifies the build and the listing together** — Screenshots show the app in use, version numbers incremented, metadata matches current behavior -- not just 'the app works.'
2. **The build is submitted for platform review** — Apple's App Store review and Google Play's policy review each check the build and metadata against their own guidelines.
3. **The release goes out gradually, not to everyone at once** — A staged rollout (Play) or phased release (App Store) exposes a small percentage of users first.
4. **The team watches production signals during the rollout** — Crash-free rate, ANR rate, and user reports at the current percentage decide whether to keep expanding.
5. **The rollout either completes or gets halted** — A clean signal lets the percentage climb to 100%; a bad one lets the team stop the bleeding before most users are affected.

*Deciding whether to advance or halt a staged rollout (Python)*

```python
release = {
    "version_name": "4.3.0",
    "version_code": 87,
    "previous_version_code": 86,
    "rollout_pct": 10,
    "crash_free_rate_pct": 99.5,   # 100 - user-perceived crash rate
    "bad_behavior_threshold_pct": 1.09,  # Android vitals "bad behavior" crash-rate line
}

def metadata_ready(screenshots_show_app_in_use, version_code, previous_version_code):
    return screenshots_show_app_in_use and version_code > previous_version_code

def crash_rate_pct(crash_free_rate_pct):
    return round(100 - crash_free_rate_pct, 2)

def rollout_decision(release):
    crash_pct = crash_rate_pct(release["crash_free_rate_pct"])
    if crash_pct >= release["bad_behavior_threshold_pct"]:
        return "HALT"
    if release["rollout_pct"] >= 100:
        return "COMPLETE"
    return "ADVANCE"

meta_ok = metadata_ready(True, release["version_code"], release["previous_version_code"])
print("metadata_ready=" + str(meta_ok))
print("crash_rate_pct=" + str(crash_rate_pct(release["crash_free_rate_pct"])) + " threshold=" + str(release["bad_behavior_threshold_pct"]))

decision = rollout_decision(release)
print("rollout_pct=" + str(release["rollout_pct"]) + " decision=" + decision)

assert meta_ok is True, "version code must strictly increase and screenshots must show the app in use before submission"
assert decision == "ADVANCE", "a crash rate under the bad-behavior threshold at a partial rollout should advance, not halt"
print("RESULT=PASS")
```

*Deciding whether to advance or halt a staged rollout (Java)*

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class Main {
    static boolean metadataReady(boolean screenshotsShowAppInUse, int versionCode, int previousVersionCode) {
        return screenshotsShowAppInUse && versionCode > previousVersionCode;
    }

    static double crashRatePct(double crashFreeRatePct) {
        return Math.round((100 - crashFreeRatePct) * 100.0) / 100.0;
    }

    static String rolloutDecision(Map<String, Double> release) {
        double crashPct = crashRatePct(release.get("crash_free_rate_pct"));
        if (crashPct >= release.get("bad_behavior_threshold_pct")) return "HALT";
        if (release.get("rollout_pct") >= 100) return "COMPLETE";
        return "ADVANCE";
    }

    public static void main(String[] args) {
        Map<String, Double> release = new LinkedHashMap<>();
        release.put("rollout_pct", 10.0);
        release.put("crash_free_rate_pct", 99.5);           // 100 - user-perceived crash rate
        release.put("bad_behavior_threshold_pct", 1.09);   // Android vitals "bad behavior" crash-rate line

        int versionCode = 87;
        int previousVersionCode = 86;

        boolean metaOk = metadataReady(true, versionCode, previousVersionCode);
        System.out.println("metadata_ready=" + metaOk);
        System.out.println("crash_rate_pct=" + crashRatePct(release.get("crash_free_rate_pct")) + " threshold=" + release.get("bad_behavior_threshold_pct"));

        String decision = rolloutDecision(release);
        System.out.println("rollout_pct=" + release.get("rollout_pct") + " decision=" + decision);

        if (!metaOk) throw new AssertionError("version code must strictly increase and screenshots must show the app in use before submission");
        if (!decision.equals("ADVANCE")) throw new AssertionError("a crash rate under the bad-behavior threshold at a partial rollout should advance, not halt");
        System.out.println("RESULT=PASS");
    }
}
```

### Your first time: Run a pre-submission store-testing pass

- [ ] Review every screenshot as if you were the reviewer — Each one must show the app in actual use -- not a login screen, splash screen, or pure title art.
- [ ] Confirm both version identifiers moved — Android's versionCode and versionName, or iOS's CFBundleVersion and CFBundleShortVersionString -- a stale build number gets rejected even if the marketing version looks new.
- [ ] Match the description against current behavior — Any claimed feature, including in-app purchases, must be something a reviewer can actually find and use in this exact build.
- [ ] Confirm the rollout mechanism is configured, not defaulted — Decide the staged rollout or phased release percentage deliberately instead of accepting whatever the console defaults to.

- **A submission is rejected for screenshots even though the app itself works fine.**
  Check that every screenshot shows the app in actual use, not a login page, splash screen, or promotional art -- this is one of the most common rejection reasons and has nothing to do with app functionality.
- **A build is rejected for a version number even though the changelog is correct.**
  Confirm the internal build identifier (versionCode / CFBundleVersion) actually increased, not just the human-readable version string -- stores reject a resubmission with a build number they've already seen.
- **A staged rollout or phased release isn't reaching more users days after launch.**
  Google Play's staged rollout percentage does not increase automatically -- someone has to manually raise it or the release stalls at whatever percentage it started at.

### Where to check

- Apple's App Store Review Guidelines for the exact metadata, screenshot, and stability rules a submission is judged against.
- Google Play Console Help's staged rollout documentation for how percentage steps and halting actually work.
- Apple's phased release documentation for the fixed seven-day rollout schedule and how pausing works.
- Android Developers' crash vitals documentation for the current user-perceived crash rate bad-behavior threshold.
- [[mobile-testing/device-and-os-matrix/fragmentation]] for why a crash-free rate that looks fine in aggregate can hide a real problem concentrated on one device or OS-version slice.
- [[mobile-testing/mobile-specifics/app-lifecycle]] for the on-device stability testing (real kills, not just backgrounding) that should happen before a build is ever submitted.

### Worked example: a rejected submission traced back to stale screenshots

1. A team submits a redesigned app, confident because every automated test passes and the build has been
   stable in internal testing for weeks.
2. The submission is rejected two days later citing Guideline 2.3.3 -- one screenshot still shows the old
   login screen from before the redesign, not the app in actual use.
3. QA had verified the build extensively but never walked the store listing itself against the current
   guidelines before submission.
4. The team adds a listing review step to their pre-submission checklist -- screenshots, version numbers, and
   description all checked against the current build, not just the build itself.

**Quiz.** What does Google Play's staged rollout percentage do on its own, with no developer action, after a release goes out at 10%?

- [ ] It automatically climbs toward 100% over the following days
- [x] It stays at 10% indefinitely -- a developer must manually increase it or halt the rollout
- [ ] It resets to 0% after 24 hours if not confirmed
- [ ] It matches whatever percentage Apple's phased release is using for the same app

*Google Play's staged rollout percentage does not increase automatically. A team has to manually raise it through the console, or halt it if problems appear -- unlike Apple's fixed seven-day phased-release schedule.*

- **Most common App Store rejection categories from this note** — Inaccurate or incomplete metadata, screenshots not showing the app in actual use, and crashes or obvious technical problems found during review.
- **Android versionCode vs versionName** — versionCode is an internal integer that must strictly increase every submission; versionName is the human-readable string users see.
- **Google Play staged rollout vs Apple phased release** — Play's percentage is fully manual with no auto-increase; Apple's phased release follows a fixed 1/2/5/10/20/50/100 percent schedule over seven days.
- **Android vitals crash bad-behavior threshold** — 1.09% or more of daily active users hitting a user-perceived crash, across all devices, is currently treated as bad behavior that can reduce store discoverability.

### Challenge

Pick an app you know well. Open its store listing and review every screenshot as if you were a reviewer: does each one show the app in actual use? Then check its version history -- can you tell whether the internal build number and the marketing version both moved on the last update?

- [Apple Developer — App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Google Play Console Help — Release Apps with Staged Rollouts](https://support.google.com/googleplay/android-developer/answer/6346149)
- [Apple Developer — Release a Version Update in Phases](https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/)
- [Android Developers — Crash Rate (Android Vitals)](https://developer.android.com/topic/performance/vitals/crash)
- [Tutorial: Prepare and Roll Out a Release on Google Play Console](https://www.youtube.com/watch?v=JmfbD6RmZn0)

🎬 [Tutorial: Prepare and Roll Out a Release on Google Play Console](https://www.youtube.com/watch?v=JmfbD6RmZn0) (4 min)

- Store review checks the listing as strictly as the code -- screenshots must show the app in actual use, and metadata must match real behavior.
- Version identifiers have an internal build number and a human-readable string on both platforms; a submission needs both to actually move.
- Google Play's staged rollout is fully manual with no auto-increase; Apple's phased release follows a fixed seven-day percentage schedule.
- Crash-free rate is a real, currently-enforced production signal (Android vitals' 1.09% bad-behavior line), not just a nice-to-have metric.


## Related notes

- [[Notes/mobile-testing/mobile-specifics/app-lifecycle|App lifecycle]]
- [[Notes/mobile-testing/mobile-specifics/battery-and-performance|Battery & performance]]
- [[Notes/mobile-testing/device-and-os-matrix/fragmentation|Fragmentation]]


---
_Source: `packages/curriculum/content/notes/mobile-testing/mobile-specifics/store-testing.mdx`_
