---
title: "Clear Cache"
tags: ["testers-toolbox", "cookies-json-sessions", "track-c"]
updated: "2026-07-16"
---

# Clear Cache

*A one-click extension that clears cached files, cookies, and browsing data instantly - the fix for the most common false bug report a tester can accidentally file: re-testing yesterday's deploy because the browser quietly kept serving it.*

> A developer fixes a bug, deploys it, and you reload the page to verify — except the browser, trying
> to be helpful, quietly serves you yesterday's JavaScript file from its local cache instead of
> fetching today's. You conclude the fix didn't work. It did. Your browser just didn't tell you. A
> one-click "Clear Cache" extension exists to remove exactly this doubt, instantly, before every
> verification that matters.

> **In real life**
>
> A garden left untended accumulates leaves, twigs, and debris that make it harder to tell what's
> actually growing underneath. Sweeping it clear doesn't change what's planted — it removes the
> buildup so you can see the garden's TRUE current state instead of a state buried under yesterday's
> mess. Clearing browser cache does the same thing to a webpage: it doesn't change the server, it just
> removes the local buildup so you're seeing what's ACTUALLY there right now.

**cache-clearing extension**: A cache-clearing extension gives one-click access to deleting a browser's stored data - cached files (JS/CSS/images), cookies, and browsing history - without navigating through browser settings menus each time. Clear Cache and Clear Browsing Data (the latter open-source, by developer dessant) are both free and verified alive in 2026, with fine-grained control over exactly what gets cleared and for which sites.

## Why this matters more than it sounds like it should

- **Caching is invisible by design** — browsers cache aggressively for performance, and there's
  usually no visual indicator that you're looking at a cached file instead of a fresh one. The bug
  is silent until you specifically suspect and rule it out.
- **The most common false "still broken" report** — a developer fixes something, deploys, a tester
  reloads without clearing cache, sees the old broken behavior (because they're running old code),
  and reports the fix didn't work. It did. The report was wrong, and everyone's time got wasted
  tracking down a non-issue.
- **Fine-grained control matters** — clearing EVERYTHING (all sites, all history) every time is
  overkill and disruptive; a good extension lets you clear just the current site, or just cache
  without wiping saved logins elsewhere.

> **Tip**
>
> Before verifying ANY fix, deploy, or "it should be different now" claim, clear cache for that site
> first, as a reflexive habit — not just when something looks wrong. It costs one click and eliminates
> an entire category of false reports before they're ever written.

> **Common mistake**
>
> Clearing cache AFTER already writing a bug report that turns out to have been stale-cache all along.
> Always rule out cache as step one of investigating something that seems "unfixed" — before spending
> time writing repro steps, screenshots, and a severity assessment for a bug that may not actually exist.

![A red-handled garden broom with orange bristles leaning against a wall covered in green and red-tinged autumn leaves, standing on a dark wooden deck scattered with fallen leaves](clear-cache.jpg)
*Broom in fall — Wikimedia Commons, CC BY-SA 3.0 (Demeester). [Source](https://commons.wikimedia.org/wiki/File:Broom_in_fall.JPG)*
- **The broom's bristles — the clearing action itself** — One deliberate tool, one clear purpose: remove what's accumulated. The extension's single click does exactly this to cached files - sweep away what's built up, revealing what's actually current underneath.
- **Leaves covering the wall behind — buildup obscuring the real surface** — You can't tell what the wall really looks like until the leaves are cleared - the same way cached files obscure what the server is ACTUALLY serving right now, until you clear them.
- **Scattered leaves already on the deck — data that's already stale** — Debris that's fallen and settled, no longer connected to anything currently growing - stale cached files are exactly this: leftover from a PAST state, no longer reflecting the current one.
- **The broom ready and leaning, not yet used** — The tool exists and is available the whole time - the habit this note argues for is USING it reflexively before verification, not leaving it leaning unused until something already looks suspicious.

**Why 'it's still broken' sometimes means 'you're running yesterday's code'**

1. **A bug gets fixed and deployed** — The SERVER now has the corrected JS/CSS/HTML - the fix genuinely exists.
2. **Tester reloads the page, cache NOT cleared** — The browser checks its local cache first - if it thinks the cached copy is still valid, it serves that instead of fetching fresh.
3. **The old, broken behavior appears again** — Not because the fix failed - because the tester is looking at YESTERDAY'S file, cached locally.
4. **Cache cleared, page reloaded again** — Now the browser has nothing stale to fall back on - it fetches the current, fixed version from the server.
5. **The fix is confirmed working** — The 'bug' was never really still there - it was a caching artifact, ruled out in one click.

The mechanism underneath this whole note is simple: a cache either holds a stale copy, or it
doesn't. Here's exactly what changes when you clear it:

*Run it - simulating a stale-cache false-negative bug report (Python)*

```python
browser_cache = {
    "/static/app.js": {"version": "v3", "cached_at_deploy": "v3"},
    "/static/styles.css": {"version": "v3", "cached_at_deploy": "v3"},
    "/api/user/profile": {"version": None, "cached_at_deploy": None},
}

def deploy_new_version(cache, new_version):
    server_state = {path: new_version for path in cache}
    return server_state

def simulate_request(cache, cleared):
    results = {}
    for path, entry in cache.items():
        if cleared:
            results[path] = "FETCHED FRESH (cache cleared)"
        elif entry["cached_at_deploy"] is None:
            results[path] = "FETCHED FRESH (never cached, e.g. API call)"
        else:
            results[path] = f"SERVED FROM CACHE (stale, still {entry['cached_at_deploy']})"
    return results

print("Server deploys v4, but the browser's local cache still holds v3:")
server_now = deploy_new_version(browser_cache, "v4")
for path, version in server_now.items():
    print(f"  server has: {path} = {version}")

print()
print("What the BROWSER actually serves, cache NOT cleared:")
for path, result in simulate_request(browser_cache, cleared=False).items():
    print(f"  {path:<24} -> {result}")

print()
print("What the BROWSER actually serves, cache CLEARED first:")
for path, result in simulate_request(browser_cache, cleared=True).items():
    print(f"  {path:<24} -> {result}")

print()
print("Without clearing cache, a 'bug' report about a fixed-in-v4 issue")
print("might just be v3's JS/CSS still running - the most common false")
print("bug report a tester can accidentally file.")

# Server deploys v4, but the browser's local cache still holds v3:
#   server has: /static/app.js = v4
#   server has: /static/styles.css = v4
#   server has: /api/user/profile = v4
#
# What the BROWSER actually serves, cache NOT cleared:
#   /static/app.js           -> SERVED FROM CACHE (stale, still v3)
#   /static/styles.css       -> SERVED FROM CACHE (stale, still v3)
#   /api/user/profile        -> FETCHED FRESH (never cached, e.g. API call)
#
# What the BROWSER actually serves, cache CLEARED first:
#   /static/app.js           -> FETCHED FRESH (cache cleared)
#   /static/styles.css       -> FETCHED FRESH (cache cleared)
#   /api/user/profile        -> FETCHED FRESH (cache cleared)
#
# Without clearing cache, a 'bug' report about a fixed-in-v4 issue
# might just be v3's JS/CSS still running - the most common false
# bug report a tester can accidentally file.
```

Same lesson in Java, framed as a direct before/after regression check:

*Run it - regression testing with and without a cleared cache (Java)*

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, String> deployedVersion = new LinkedHashMap<>();
        deployedVersion.put("/static/app.js", "v4");
        deployedVersion.put("/static/styles.css", "v4");

        Map<String, String> browserCache = new LinkedHashMap<>();
        browserCache.put("/static/app.js", "v3");
        browserCache.put("/static/styles.css", "v3");

        System.out.println("Server has deployed v4. Browser's local cache still holds v3.");
        System.out.println();

        System.out.println("Testing WITHOUT clearing cache first:");
        for (String path : deployedVersion.keySet()) {
            String served = browserCache.get(path);
            String verdict = served.equals(deployedVersion.get(path)) ? "matches deploy" : "STALE - testing old code";
            System.out.printf("  %-22s served=%-4s deployed=%-4s (%s)%n", path, served, deployedVersion.get(path), verdict);
        }

        System.out.println();
        System.out.println("Testing WITH cache cleared first:");
        for (String path : deployedVersion.keySet()) {
            String served = deployedVersion.get(path);
            System.out.printf("  %-22s served=%-4s deployed=%-4s (matches deploy)%n", path, served, deployedVersion.get(path));
        }

        System.out.println();
        System.out.println("A regression test run against stale cached files isn't testing");
        System.out.println("today's deploy at all - it is silently re-testing yesterday's.");
    }
}

/* Server has deployed v4. Browser's local cache still holds v3.

   Testing WITHOUT clearing cache first:
     /static/app.js         served=v3   deployed=v4   (STALE - testing old code)
     /static/styles.css     served=v3   deployed=v4   (STALE - testing old code)

   Testing WITH cache cleared first:
     /static/app.js         served=v4   deployed=v4   (matches deploy)
     /static/styles.css     served=v4   deployed=v4   (matches deploy)

   A regression test run against stale cached files isn't testing
   today's deploy at all - it is silently re-testing yesterday's. */
```

### Your first time: Your mission: build the reflexive clear-before-verify habit

- [ ] Install Clear Cache or Clear Browsing Data (both free, one-click) — The open-source Clear Browsing Data (dessant) is a solid, auditable choice if you want to confirm exactly what it does.
- [ ] Configure it to clear cache for the CURRENT SITE only by default — Wiping all sites' data every time is disruptive (logs you out everywhere) - scope it to what you actually need cleared.
- [ ] Pick a page in BuggyShop, load it once, then have a fix or change 'deployed' (or just note the current state) — Reload WITHOUT clearing cache first and observe whether anything looks unchanged that you expected to change.
- [ ] Clear cache with one click, then reload the same page — Compare - did anything actually look different once cache was ruled out as a factor?
- [ ] Make this the FIRST step whenever you're about to verify a fix — Not a step you reach for only when confused - a reflexive habit before every verification, so the false-report class from this note never gets a chance to happen.

You've built the single habit most likely to prevent you from ever filing (or chasing down someone
else's) a bug report that was actually just a stale cache.

- **You cleared cache and the page still shows old behavior.**
  Cache isn't the only source of staleness - check for a service worker (which can serve its own cached responses independent of normal browser cache, visible in DevTools' Application panel), a CDN edge cache serving a stale copy, or confirm the fix was ACTUALLY deployed to the environment you're testing, not just merged to a branch.
- **Clearing cache also logged you out of the site unexpectedly.**
  Your extension's scope likely included cookies, not just cached files - reconfigure it to clear cache/cached-images-and-files specifically, leaving cookies untouched, if you need to stay logged in across cache clears.
- **A hard refresh (Ctrl/Cmd+Shift+R) seems to work sometimes but not always, so you stopped trusting it.**
  A hard refresh bypasses cache for the MAIN document request, but doesn't always force-refresh every sub-resource (some fonts, some third-party scripts) - a dedicated cache-clearing extension is more thorough and consistent than relying on the hard-refresh shortcut alone.
- **You need to compare 'with cache' vs 'without cache' behavior deliberately, not just clear it every time.**
  That's a legitimate test case in its own right (does the app behave correctly for a returning visitor with stale assets, e.g. showing an update-available prompt?) - use the extension's toggle deliberately for that specific check, rather than treating clearing as always mandatory.

### Where to check

- **DevTools' Application panel, Service Workers section** — a service worker can serve cached responses independent of normal browser cache; if clearing cache doesn't fix stale behavior, check here next.
- **The network tab's "Disable cache" checkbox** (while DevTools is open) — a quick alternative that bypasses cache for the current session without a separate extension, useful for active debugging sessions.
- **The deploy/build timestamp of the environment you're testing** — confirm the fix you're trying to verify was actually deployed THERE, before assuming a still-broken result is a caching issue.
- **Response headers (`Cache-Control`, `ETag`)** — explain WHY a resource was or wasn't cached, useful when cache-clearing behavior seems inconsistent across different files on the same page.

### Worked example: a near-miss false bug report, caught just in time

1. A developer fixes a checkout button's disabled-state bug and deploys to staging. A tester reloads
   the checkout page to verify — the button is STILL clickable when it shouldn't be.
2. Before writing up "fix didn't work," the tester runs the reflexive habit: clear cache for the
   site, reload again.
3. This time the button correctly shows disabled. The fix was real; the first reload was serving a
   cached copy of the JS bundle from before the fix landed.
4. Cross-check via DevTools' network tab confirms it: the first load showed `(from disk cache)` next
   to the JS bundle request; after clearing, it showed a real 200 response with today's deploy
   timestamp in a custom header.
5. No bug report gets filed. No developer time gets spent investigating a fix that already worked.
   One click, thirty seconds, an entire wasted investigation avoided — the exact value this tool
   family exists to provide, made concrete.

**Quiz.** A tester verifies a deployed fix, sees the old broken behavior, and is about to file 'fix does not work' when a colleague suggests clearing cache first. After clearing, the fix works correctly. What should the tester conclude and do differently going forward?

- [ ] Nothing needs to change - this was a one-time fluke, and the normal verification process is fine as-is
- [x] Clearing cache should become a standing FIRST STEP before verifying any fix or deploy, not a troubleshooting step reached for only after something looks wrong - since this exact false-negative pattern is common and cheap to rule out upfront
- [ ] The developer's fix must have been flaky, since it worked after a cache clear but not before
- [ ] This proves browser caching is inherently unreliable and should be disabled entirely during all testing

*The core lesson of this note is that stale-cache false negatives are common enough, and cheap enough to rule out (one click), that clearing should be a REFLEXIVE first step before verification - not a troubleshooting step you only reach for once something already seems wrong, by which point time may already have been spent investigating a non-bug. Option one dismisses a real, recurring pattern as a fluke, missing the whole point. Option three misattributes the cause - the fix worked correctly the entire time; the browser's cache, not the fix, was the variable that changed between the two checks. Option four proposes an extreme, impractical response (caching exists for good performance reasons across the entire web) to a problem whose actual fix is simple and targeted: clear cache before verifying, not eliminate caching everywhere.*

- **What a cache-clearing extension does** — One-click deletion of cached files, cookies, and browsing data - fine-grained control lets you clear just the current site's cache without logging out of other sites or losing all history.
- **The most common false bug report cache-clearing prevents** — 'This fix doesn't work' when actually the browser is still serving a CACHED pre-fix version of JS/CSS - the fix is real, the report is wrong, and clearing cache first prevents ever filing it.
- **The recommended habit from this note** — Clear cache REFLEXIVELY before verifying any fix or deploy - not just as a troubleshooting step reached for after something already looks broken.
- **What to check if clearing cache doesn't fix stale-looking behavior** — A service worker (DevTools' Application panel) can cache independently of normal browser cache; also confirm the fix was actually deployed to the environment being tested, not just merged to a branch.
- **Why a hard refresh (Ctrl/Cmd+Shift+R) isn't always fully reliable** — It bypasses cache for the main document but doesn't always force-refresh every sub-resource (some fonts/third-party scripts) - a dedicated cache-clearing tool is more thorough and consistent.
- **A legitimate reason NOT to always clear cache** — Deliberately testing a returning visitor's stale-cache experience (e.g. an 'update available, refresh' prompt) is a real test case - use the clear toggle intentionally for that check, rather than treating clearing as universally mandatory.

### Challenge

The next time you verify any change in BuggyShop (a fix, a new feature, anything), make clearing
cache your literal first action before reloading — even if nothing looks currently broken. Do this
for at least three separate verifications and note whether cache-clearing ever changed what you saw,
even once. Write a one-line note on whether this habit felt worth adopting permanently.

### Ask the community

> I verified `[fix/change]` on `[app]`, saw `[old/unexpected behavior]` before clearing cache, and `[what changed / didn't change]` after clearing. Is there a standard team habit here for ruling out caching before filing a 'not fixed' report?

Stale-cache false reports are common enough that most teams have an informal habit around this — the
most useful answers will share what convention (if any) this team already uses.

- [GitHub — Clear Browsing Data (dessant), open-source](https://github.com/dessant/clear-browsing-data)
- [Clear Cache — Chrome Web Store listing](https://chromewebstore.google.com/detail/clear-cache/cppjkneekbjaeellbfkmgnhonkkjfpdn)
- [Awais Mirza — Clear Cache Extension for Web Developers](https://www.youtube.com/watch?v=R_81Se9iQcg)

🎬 [Clear Cache Chrome Browser Extension for Developers (Tech Pulse Labs)](https://www.youtube.com/watch?v=uIQCZt5-rBw) (6 min)

- A cache-clearing extension gives one-click access to deleting cached files, cookies, and history - free, verified alive in 2026 (Clear Cache, and the open-source Clear Browsing Data).
- Caching is invisible by design - the most common false 'still broken' report comes from a browser silently serving a stale, pre-fix version of a file.
- Make clearing cache a REFLEXIVE first step before verifying any fix or deploy, not a troubleshooting step reached for only after confusion sets in.
- If clearing cache doesn't fix stale behavior, check for a service worker (DevTools Application panel) and confirm the fix was actually deployed to the environment you're testing.
- A hard refresh isn't always fully reliable across every sub-resource - a dedicated extension is more thorough and consistent.


## Related notes

- [[Notes/testers-toolbox/cookies-json-sessions/cookie-editors|Cookie editors]]
- [[Notes/testers-toolbox/cookies-json-sessions/multi-account-testing|Managing multi-account testing]]
- [[Notes/defect-management/writing-bug-reports/repro-steps|Repro steps]]


---
_Source: `packages/curriculum/content/notes/testers-toolbox/cookies-json-sessions/clear-cache.mdx`_
