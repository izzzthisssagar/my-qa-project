---
title: "Screen recorders for bug repro"
tags: ["testers-toolbox", "beyond-the-browser", "track-c"]
updated: "2026-07-16"
---

# Screen recorders for bug repro

*Loom's free tier was gutted in the 2026 Atlassian integration (25 videos lifetime, 5-minute cap, 720p, no MP4 download) - impractical for regular bug work. Built-in OS recorders (free, unlimited) and OBS Studio (free, open source, unlimited) are the sustainable 2026 defaults.*

> A screen recording turns "it doesn't work when I click submit" into a developer watching exactly
> what you clicked, exactly what happened, exactly what the console showed at that moment. It's the
> single highest-leverage piece of evidence in a bug report. But the tool most people default to,
> Loom, changed dramatically in 2026 — its free tier is now genuinely too small for regular testing
> work, and the sustainable free options are ones already sitting on your computer.

> **In real life**
>
> An old mechanical film camera doesn't need a subscription, doesn't cap how many reels you shoot, and
> the film it produces is yours outright — you load it, you shoot, you own the result. That's exactly
> the deal with your operating system's built-in screen recorder or OBS Studio: no account, no video
> limit, no quality cap, the file is a real local file the moment you stop recording.

**screen recorder**: A screen recorder captures video of what happens on screen, essential for bug reports where static screenshots can't show a sequence of interactions, a transient error message, or timing-dependent behavior. Built-in OS recorders (macOS: Cmd+Shift+5; Windows: Win+G / Xbox Game Bar) are free and unlimited. OBS Studio is free, open-source, and unlimited with more advanced capture options. Loom's free tier was significantly reduced after its 2026 Atlassian integration: 25 videos total (lifetime cap, not monthly), a 5-minute length limit, 720p max quality, and no MP4 download without paying.

## Why the tool choice actually matters here

- **Loom's 2026 reality**: since Atlassian's integration completed, the free "Starter" tier caps at
  25 recordings TOTAL (not per month — for the lifetime of the account), 5 minutes each, 720p
  maximum, and you cannot download the raw MP4 file without a paid plan. For a tester filing several
  bug recordings a week, this runs out fast.
- **Built-in OS recorders**: completely free, no account, no length or quality cap, and you own the
  resulting file outright as a local video — the simplest sustainable option for most bug-repro needs.
- **OBS Studio**: free, open source, more powerful (multiple sources, scene switching, higher
  quality control) — worth the extra setup when you need more than a basic screen capture.
- **What actually makes a recording USEFUL for a bug report**: not just capturing the screen, but
  capturing the RIGHT context alongside it — most critically, the browser's own DevTools console
  and network tab, visible in the same recording.

> **Tip**
>
> Before recording a bug, open DevTools and position it so the Console and/or Network tab is visible
> in the SAME frame as the bug itself. A recording of just the UI proves something happened; a
> recording that also shows the console error at the exact moment tells a developer WHY.

> **Common mistake**
>
> Relying on Loom's free tier for ongoing, regular bug-repro work without checking your remaining
> video count first. Discovering you've hit the 25-video lifetime cap mid-testing-session, with no
> warning, disrupts exactly the workflow a screen recorder is supposed to make smoother.

![A vintage black 8mm film movie camera with a triple lens turret resting on a white surface next to its open instruction manual and lens cap](screen-recorders-for-bug-repro.jpg)
*Ekran-4 8mm film camera — Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:Ekran-4_8mm_film_camera.jpg)*
- **The triple lens turret — multiple ways to capture the same scene** — Different lenses for different framing needs, all built into one owned device - like choosing between a built-in OS recorder and OBS Studio depending on how much control a specific bug capture needs.
- **The open instruction manual — full documentation, no paywall** — Complete technical specs available upfront, nothing locked behind a subscription - the same transparency OBS Studio's open-source nature and a built-in OS recorder's simplicity both offer.
- **The small black lens cap, sitting separately** — A simple, complete accessory - nothing about using this camera requires anything beyond what's already in the box. No recurring account, no video-count meter running in the background.
- **The camera body itself, self-contained and ready** — Everything needed to shoot is already there, owned outright - the film it produces is yours the moment you stop recording, exactly like a local screen-recording file with no download paywall.

**Recording a bug the way that actually helps a developer**

1. **Open DevTools and position it visibly** — Console and/or Network tab in view, alongside the app - this is the single biggest quality upgrade to any bug recording.
2. **Start recording (OS built-in, or OBS)** — No account needed, no length cap to worry about mid-repro.
3. **Reproduce the bug exactly, narrating if helpful** — Perform the EXACT steps that trigger it - a recording of a DIFFERENT path than the real bug helps nobody.
4. **Stop recording once the bug/error is clearly visible** — No need to keep going past the point that matters - shorter, focused recordings are easier for a developer to review.

The value of showing console/network context alongside the UI is measurable — here's that gap made
explicit as a simple scoring model:

*Run it - scoring bug-report evidence quality by what's actually included (Python)*

```python
def repro_quality_score(steps_written, has_video, video_shows_console, has_exact_url):
    score = 0
    if steps_written:
        score += 30
    if has_video:
        score += 30
    if video_shows_console:
        score += 25
    if has_exact_url:
        score += 15
    return score

reports = [
    {"name": "Text-only, vague steps", "steps": True, "video": False, "console": False, "url": False},
    {"name": "Text + screen recording (no console)", "steps": True, "video": True, "console": False, "url": True},
    {"name": "Text + screen recording WITH console/network visible", "steps": True, "video": True, "console": True, "url": True},
]

print("Bug report quality, scored by what evidence is actually included:")
print()
for r in reports:
    score = repro_quality_score(r["steps"], r["video"], r["console"], r["url"])
    print(f"  {r['name']:<52} score={score}/100")

print()
print("The jump from 'has a video' to 'video SHOWS the console/network tab'")
print("is the single biggest quality gap - a recording of just the UI proves")
print("something happened, but a developer still can't see WHY without the")
print("browser's own error output visible in the same recording.")

# Bug report quality, scored by what evidence is actually included:
#
#   Text-only, vague steps                               score=30/100
#   Text + screen recording (no console)                 score=75/100
#   Text + screen recording WITH console/network visible score=100/100
#
# The jump from 'has a video' to 'video SHOWS the console/network tab'
# is the single biggest quality gap - a recording of just the UI proves
# something happened, but a developer still can't see WHY without the
# browser's own error output visible in the same recording.
```

Same lesson in Java — the concrete numbers behind why Loom's 2026 free tier is a poor fit for
regular testing work:

*Run it - Loom's gutted 2026 free tier vs OBS Studio, side by side (Java)*

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, String> loom2026 = new LinkedHashMap<>();
        loom2026.put("total_free_videos", "25 (lifetime, not monthly)");
        loom2026.put("max_length", "5 minutes");
        loom2026.put("max_quality", "720p");
        loom2026.put("mp4_download", "NOT available on free tier");

        Map<String, String> obsStudio = new LinkedHashMap<>();
        obsStudio.put("total_free_videos", "unlimited");
        obsStudio.put("max_length", "unlimited");
        obsStudio.put("max_quality", "up to your monitor's native resolution");
        obsStudio.put("mp4_download", "yes - it's a local file, always");

        System.out.println("Loom's 2026 gutted free tier vs OBS Studio (free, open source):");
        System.out.println();
        System.out.println("Loom (post-Atlassian 2026 free tier):");
        for (Map.Entry<String, String> e : loom2026.entrySet()) {
            System.out.printf("  %-18s %s%n", e.getKey(), e.getValue());
        }

        System.out.println();
        System.out.println("OBS Studio (free, open source):");
        for (Map.Entry<String, String> e : obsStudio.entrySet()) {
            System.out.printf("  %-18s %s%n", e.getKey(), e.getValue());
        }

        System.out.println();
        System.out.println("A 25-video LIFETIME cap makes Loom's free tier impractical for");
        System.out.println("regular bug-repro work - a tester filing several recordings a week");
        System.out.println("burns through that in under a month. OBS (or an OS built-in recorder)");
        System.out.println("is the sustainable free choice for repeated real work.");
    }
}

/* Loom's 2026 gutted free tier vs OBS Studio (free, open source):

   Loom (post-Atlassian 2026 free tier):
     total_free_videos  25 (lifetime, not monthly)
     max_length         5 minutes
     max_quality        720p
     mp4_download       NOT available on free tier

   OBS Studio (free, open source):
     total_free_videos  unlimited
     max_length         unlimited
     max_quality        up to your monitor's native resolution
     mp4_download       yes - it's a local file, always

   A 25-video LIFETIME cap makes Loom's free tier impractical for
   regular bug-repro work - a tester filing several recordings a week
   burns through that in under a month. OBS (or an OS built-in recorder)
   is the sustainable free choice for repeated real work. */
```

### Your first time: Your mission: record one bug the way that actually helps a developer

- [ ] Open your OS's built-in recorder (macOS: Cmd+Shift+5; Windows: Win+G) — No install needed - confirm you know where the resulting file is saved before you need it under pressure.
- [ ] Open DevTools and position it so the Console tab is visible alongside the app — This is the single change that makes a recording actually diagnostic instead of just illustrative.
- [ ] Find or reproduce a real bug in BuggyShop — A console error, a failed network request, a visual glitch - anything with a repeatable trigger.
- [ ] Record the EXACT repro steps, keeping the console/network tab in frame — Perform the precise sequence that triggers it - not an approximation.
- [ ] Save the file and confirm you can open/replay it before considering the task done — A corrupted or unreadable recording helps nobody - always verify the output.

You've produced the kind of bug-report evidence that answers not just "what happened" but "why" -
using a tool with no video-count meter running in the background.

- **Your OS's built-in recorder isn't capturing system audio, or a specific window won't record.**
  Check OS-level screen-recording permissions first (macOS System Settings > Privacy & Security > Screen Recording is a common blocker) - a permission not yet granted is the most frequent cause, not a tool malfunction.
- **OBS Studio's output looks blurry or lower quality than expected.**
  Confirm your OBS output resolution matches your actual display resolution - a common misconfiguration downscales the capture, producing exactly this blurriness; check Settings > Video for both base and output resolution.
- **You're not sure whether you've used up Loom's free-tier video count.**
  Check your account's video count directly in Loom's dashboard before starting a recording you're relying on - discovering the cap mid-session is disruptive; checking first avoids the surprise entirely.
- **A recording is too long and unfocused, making it hard for a developer to find the actual bug moment.**
  Re-record with a tighter script: reproduce ONLY the exact steps that trigger the bug, stop recording shortly after the failure is visible - a focused 30-second recording is more useful than an unfocused 5-minute one.

### Where to check

- **OS-level screen-recording permissions** (System Settings on macOS, Privacy settings on Windows) — the most common recording-failure cause, checked before assuming a tool problem.
- **OBS Studio's Settings > Video panel** — confirms base/output resolution match your actual display for a sharp, undistorted capture.
- **The saved file itself, replayed once** — always verify a recording is actually usable before considering the bug-repro task complete.
- **DevTools' own visibility within the recorded frame** — confirms the console/network context was actually captured, not just the app UI.

### Worked example: a recording that showed the actual root cause, not just the symptom

1. A tester notices a "loading" spinner never resolves on a specific product page. Text description
   alone: "product page spinner never stops."
2. Recording the bug with DevTools' Console AND Network tab visible alongside the page: the spinner
   appears, and simultaneously, a network request to `/api/products/8842/reviews` shows a red 404
   in the Network tab, followed by a console error: `Cannot read property 'map' of undefined`.
3. This single recording shows the COMPLETE causal chain: a missing reviews endpoint (404) causes
   the frontend to receive no data, which then crashes trying to render a list from undefined data —
   visible in one continuous capture, not three separate investigations.
4. Report: "Product page 8842's reviews section fails to load - /api/products/8842/reviews returns
   404, causing a client-side crash (Cannot read property 'map' of undefined) that leaves the
   loading spinner stuck indefinitely. See attached recording (0:08-0:15) showing both the network
   failure and the resulting console error." Attached as a local file, not an expiring share link.
5. A developer watching this recording needs zero additional investigation to identify both the
   missing backend endpoint AND the frontend's missing null-check - both visible in eight seconds
   of footage.

**Quiz.** A tester records a bug using their OS's built-in screen recorder, capturing only the visible UI (no DevTools console/network tab in frame), and attaches it to a bug report. The developer replies asking for the console output. What could the tester have done differently to avoid this back-and-forth?

- [ ] Nothing - console output can never be captured in a screen recording and always requires a separate manual step from the developer
- [x] Position DevTools' Console and/or Network tab to be visible in the SAME recorded frame as the bug before recording - this single change turns a recording that only shows WHAT happened into one that also shows WHY, eliminating exactly this kind of follow-up request
- [ ] Use Loom instead of the OS built-in recorder, since only Loom's paid tier can capture console output
- [ ] Record two separate videos - one of the UI and one of the console - since the two cannot be shown in one continuous recording

*This note's central practical lesson is precisely this: positioning DevTools so its Console/Network tab is visible in the same frame as the bug being reproduced is what separates a merely illustrative recording from a genuinely diagnostic one - and it costs nothing extra to do, regardless of which recording tool is used. Option one is factually wrong; any screen recorder captures whatever is visible on screen, DevTools included, with zero special capability required. Option three is an invented and false claim - no recording tool's console-capture ability depends on that tool specifically, since it's just capturing whatever is on screen. Option four is unnecessary and worse - the whole point (as this note's worked example shows) is that seeing the network failure and the resulting console error IN THE SAME continuous timeline is what reveals the causal chain; splitting them into two separate videos would make that connection harder to see, not easier.*

- **Loom's 2026 free-tier reality** — Post-Atlassian integration: 25 videos TOTAL (lifetime cap, not monthly), 5-minute length limit, 720p max quality, no MP4 download without paying - impractical for regular bug-repro work.
- **The sustainable 2026 free defaults** — Built-in OS recorders (macOS Cmd+Shift+5, Windows Win+G) - free, unlimited, no account. OBS Studio - free, open source, unlimited, more advanced capture options.
- **The single biggest quality upgrade to any bug recording** — Position DevTools' Console and/or Network tab visible in the SAME frame as the bug before recording - turns 'proves it happened' into 'shows why it happened,' with zero extra tooling cost.
- **Why 'record only what's visibly broken' isn't enough** — A recording of just the UI shows the symptom; the console/network context alongside it reveals the actual root cause - as this note's worked example shows, both together can eliminate an entire investigation cycle.
- **The main OS-level troubleshooting step for a failed recording** — Check screen-recording permissions first (macOS System Settings > Privacy & Security; Windows equivalent) - the most common cause of a recording failing to capture, not a tool malfunction.
- **Why attaching the actual file beats an expiring share link** — A locally-owned recording (OS recorder/OBS output) stays permanently accessible in the bug tracker - no risk of a hosted link expiring or requiring a viewer account later.

### Challenge

Reproduce and record one real bug in BuggyShop using your OS's built-in recorder, with DevTools'
Console and Network tab visible in the same frame throughout. Write the accompanying bug report
following this note's worked-example structure - describing both what the recording shows AND the
root cause it reveals, with a specific timestamp reference into the recording.

### Ask the community

> I recorded `[bug]` showing `[what the console/network revealed]`. Should I trim/edit this recording before attaching it to the ticket, or is the full unedited capture preferred for this team's review process?

Recording length and editing conventions vary by team — the most useful answers will tell you
whether this specific team prefers tight, trimmed clips or full unedited context.

- [OBS Studio — official site (free, open source)](https://obsproject.com/)
- [ScreenKite — Loom's 2026 free-plan changes explained](https://www.screenkite.com/blog/loom-free-plan-changes-2026)
- [How to Use OBS Studio for Screen Recording — 2025 Tutorial for Beginners (Emmanuel Adanu)](https://www.youtube.com/watch?v=yyU9-3Hblvo)

🎬 [How to Use OBS Studio to Record Screen — Beginner Tutorial (Kevin Stratvert)](https://www.youtube.com/watch?v=xoe9ZOzlfnQ) (12 min)

- Loom's 2026 free tier was gutted after Atlassian's integration - 25 videos total (lifetime), 5-minute cap, 720p, no MP4 download - impractical for regular testing work.
- Built-in OS recorders (free, unlimited) and OBS Studio (free, open source, unlimited) are the sustainable 2026 defaults for bug-repro recording.
- Position DevTools' Console/Network tab visible in the SAME recorded frame as the bug - the single biggest quality upgrade, showing WHY not just WHAT happened.
- A focused, short recording of the exact repro steps beats a long, unfocused one - stop recording once the failure is clearly visible.
- Always attach the actual local file rather than relying on an expiring hosted share link.


## Related notes

- [[Notes/testers-toolbox/link-page-ui-checks/gofullpage-and-screenshots|GoFullPage & screenshot tools]]
- [[Notes/defect-management/writing-bug-reports/evidence|Evidence]]
- [[Notes/defect-management/writing-bug-reports/repro-steps|Repro steps]]


---
_Source: `packages/curriculum/content/notes/testers-toolbox/beyond-the-browser/screen-recorders-for-bug-repro.mdx`_
