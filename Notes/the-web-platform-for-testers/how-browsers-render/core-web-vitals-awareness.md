---
title: "Core Web Vitals awareness"
tags: ["web-platform", "performance", "metrics", "track-a"]
updated: "2026-07-10"
---

# Core Web Vitals awareness

*Google turned 'the page feels slow' into three numbers with thresholds. Learn what LCP, INP and CLS actually measure, why your laptop always passes, and how to file a performance bug nobody can argue with.*

> "The page feels slow" is an opinion. "LCP is 4.2 seconds; the threshold is 2.5" is a
> fact with a threshold attached, and it ends the argument before it starts. Someone did
> the enormous work of turning three human frustrations — *it takes forever to appear*,
> *it ignores my clicks*, *it moves while I'm reading* — into three measurable numbers.
> This note is the last one of Module 4, and it hands you those numbers.

> **In real life**
>
> Core Web Vitals are **a blood test, not a diagnosis.** Three numbers, each with a normal
> range. A bad result doesn't tell you what's wrong — it tells you *where to look*, and it
> removes any argument about whether something is wrong at all. You still need everything
> from this module to find the cause. But you no longer have to persuade anyone that the
> patient is unwell.

## The three numbers

| Metric | The human complaint | Good | Poor |
|---|---|---|---|
| **LCP** — Largest Contentful Paint | "It takes forever to show up" | ≤ 2.5s | > 4.0s |
| **INP** — Interaction to Next Paint | "It ignores my clicks" | ≤ 200ms | > 500ms |
| **CLS** — Cumulative Layout Shift | "It moves while I'm reading" | ≤ 0.1 | > 0.25 |

- ****LCP**: Largest Contentful Paint — the moment the biggest element in the viewport (usually the hero image or headline) finishes rendering. Good is 2.5 seconds or less, measured on a throttled mid-range phone with a cold cache.** times the biggest thing on screen — usually a hero image or headline. It's your six stages from the last note, summed up to the moment the page looks like *something*.
- **INP** times the gap between a click and the next painted frame. It measures the mannequin window: the page is drawn and unresponsive.
- **CLS** measures how much content jumped. Images without dimensions, late ads, font swaps — the last note's whole subject, scored.

Each maps to something you already understand. That's not a coincidence; the metrics were
chosen to be caused by things you can fix.

![A loaded web page, whose load quality can be scored by three metrics](browser-render.png)
*Screenshot: Firefox browser — Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Firefox_Browser_Creative_Commons_screenshot.png)*
- **LCP — the biggest element to appear** — Usually the hero image or the headline. LCP is the moment IT finishes rendering, not the moment the page finishes loading. Optimizing a footer image cannot help; optimizing this one can. Lighthouse literally tells you which element it timed.
- **INP — the click that goes nowhere** — Time from your click to the next painted frame. If JavaScript is busy parsing (Module 4 ch3's single thread), the browser cannot paint, and your click sits in a queue. Over 500ms and the user clicks again — which is how double submissions are born.
- **CLS — anything that moves after paint** — Every shift is scored by how much area moved and how far. An image with no width/height is the classic. Score above 0.1 fails, and the user experiences it as clicking the wrong button.
- **Hard reload is the only honest measurement** — Warm cache means the image is already sized and present: LCP fast, CLS zero. You measured yourself, not a visitor. Ctrl+Shift+R with throttling on, always.
- **Lighthouse lives one panel away** — DevTools → Lighthouse → Analyze. It applies mobile throttling for you, scores all three, and names the exact element responsible for LCP and each layout shift. Two minutes, a report you can paste.

**What a real user experiences, scored — press Play**

1. **⚪ 0.0s — a white screen** — The request is out; DNS, TLS and TTFB are burning time (last note's stages 1–2). No metric has fired yet because nothing has been painted. The user is already forming an opinion.
2. **🖼 2.8s — the hero image lands: LCP** — The biggest element finally paints. LCP = 2.8s, which fails the 2.5s threshold. Not because the site is badly built, but because the image was 900 KB and sat behind a render-blocking stylesheet.
3. **📉 3.1s — the ad loads and shoves: CLS** — A banner is inserted above the content, pushing everything down 120px. CLS climbs to 0.19 — a failing score. The user was reaching for a link and now they aren't.
4. **🖱 3.4s — they click. Nothing: INP** — The JavaScript bundle is still executing, and JavaScript is single-threaded (ch3). The click waits in the queue; the browser cannot paint a response. INP = 780ms. The user clicks again, and later two orders appear.
5. **🚪 4.0s — they leave** — Three failing numbers, one human, no bug report — because nothing 'broke'. This is what the metrics exist to make visible: an experience that is bad in ways no functional test would ever catch.

*Try it — score a page the way Lighthouse does*

```python
THRESHOLDS = {           # (good, poor) — anything between is "needs improvement"
    "LCP": (2.5, 4.0),    # seconds
    "INP": (200, 500),    # milliseconds
    "CLS": (0.1, 0.25),   # unitless
}

def rate(metric, value):
    good, poor = THRESHOLDS[metric]
    return "GOOD" if value <= good else ("POOR" if value > poor else "NEEDS WORK")

# The same page, measured two ways.
runs = {
    "your laptop (warm cache, fast wifi, near server)": {"LCP": 0.9, "INP": 60,  "CLS": 0.00},
    "a real phone (cold cache, Slow 4G, 4x CPU)":       {"LCP": 2.8, "INP": 780, "CLS": 0.19},
}

for label, metrics in runs.items():
    print(label)
    for m, v in metrics.items():
        unit = {"LCP": "s", "INP": "ms", "CLS": ""}[m]
        print(f"   {m}: {v}{unit:3}  -> {rate(m, v)}")
    print()

print("Identical code. Identical server. Identical everything.")
print("You would have shipped this and called it fast.")
print()
# CLS is an area x distance score, not a pixel count:
shifts = [(0.30, 0.25), (0.10, 0.20)]   # (fraction of viewport moved, fraction of distance)
cls = sum(a * d for a, d in shifts)
print(f"CLS = sum(impact x distance) = {cls:.2f}  -> {rate('CLS', cls)}")
print("Two shifts, neither of which felt dramatic, and the page fails.")
```

## How to file a performance bug that gets fixed

Bad: *"the dashboard is slow."* Ignored, or scheduled for a redesign nobody funds.

Good: *"LCP 4.2s on Slow 4G + 4× CPU (threshold 2.5s). Lighthouse names the LCP element
as the hero image: 900 KB, unoptimized, loaded after a render-blocking stylesheet.
Screenshot and trace attached."*

The second one names the metric, the threshold, the conditions, the element, and the
cause. It cannot be argued with, only fixed or deprioritized *explicitly* — which is all
a tester can ever ask for.

> **Tip**
>
> **Lighthouse already applies mobile throttling for you.** That's why its numbers look
> "wrong" compared to what you feel — it is simulating a mid-range Android on a slow
> connection, which is a far more typical user than you are. Before you dispute a
> Lighthouse score, reproduce its conditions: hard reload, Slow 4G, 4× CPU. Nearly every
> time, the score is right and your machine was lying. Learning to trust the number over
> the feeling is most of what makes a performance tester useful.

### Your first time: Your mission: score three real pages

- [ ] Run Lighthouse on a site you love — DevTools → Lighthouse → Mobile → Analyze. Wait a minute. Read the three vitals. Many beloved, well-funded sites fail at least one, and seeing that recalibrates your standards permanently.
- [ ] Find the LCP element — Lighthouse names it: 'Largest Contentful Paint element'. Click it — DevTools highlights it on the page. Now you know exactly which image or heading to argue about.
- [ ] Find every layout shift — In the Lighthouse report, 'Avoid large layout shifts' lists the exact elements that moved. Combine with Rendering → Layout Shift Regions to watch it happen live.
- [ ] Measure INP by hand — Throttle CPU 4×, load a heavy app, and click something the instant the content appears. Count the delay. That's the mannequin window from the last note, felt in your own fingers.
- [ ] Compare warm vs cold — Run Lighthouse twice: once normally, once after a hard reload with cache disabled. The gap between the two scores is the gap between your experience and your users'.

Three sites scored, one LCP element identified, one layout shift caught, one INP felt.

- **Lighthouse says LCP is 4s but the page feels instant to me.**
  It does feel instant — to you. Lighthouse simulates a mid-range phone on a throttled network with an empty cache. You have a fast laptop, a warm cache, and you're sitting near the server. Both observations are true and only one describes a customer. Reproduce its conditions before disputing it; you'll almost always find the number was honest.
- **CLS is bad but I can't see anything jump.**
  Your cache has the images sized already, so nothing shifts for you. Hard reload with cache disabled and throttle to Slow 3G, then turn on Rendering → Layout Shift Regions. Now watch. Layout shift is by definition a first-visit, cold-cache phenomenon, which is exactly why it survives so long in production.
- **INP is terrible but the page loads fast.**
  Load speed and responsiveness are different problems (last note's paint-vs-interactive gap, scored). A fast-painting page with a heavy JavaScript bundle blocks the single thread, so clicks queue and no frame paints. Look for long tasks in the Performance panel. Report it as INP with the number: 'INP 780ms, threshold 200ms.'
- **The score changes every time I run it.**
  Normal — Lighthouse simulates and there's variance, plus your machine has other things running. Run it three times and take the median, close other tabs, and prefer field data (real users) over lab data (your machine) when a product has it. Never argue a two-point difference; do argue a category difference.

### Where to check

Where the numbers live:

- **DevTools → Lighthouse** — all three vitals, mobile throttling applied, the LCP element named, every layout shift listed. Start here, always.
- **Performance panel** — the timeline behind the numbers: which stage ate the seconds.
- **Rendering → Layout Shift Regions** — watch CLS happen, live, highlighted.
- **Network → hard reload with cache disabled** — the only measurement that describes a first-time visitor.
- **The thresholds themselves** — LCP 2.5s, INP 200ms, CLS 0.1. Memorize these three numbers; they turn every performance conversation from taste into arithmetic.

Tester's habit: **quote the metric, the threshold, and the conditions.** "LCP 4.2s
against a 2.5s threshold, on Slow 4G + 4× CPU, hero image 900 KB" is not a complaint.
It's a measurement, and it survives contact with a sceptical engineer — which is the only
test a bug report ever really has to pass.

### Worked example: the redesign that was cancelled by three numbers

The last worked example of the module, and it uses every note in it.

1. **The situation:** conversion is down on mobile. Leadership assumes the design is stale and approves a costly redesign. A tester asks for two days first.
2. **Run Lighthouse on mobile.** LCP **4.2s** (poor), INP **610ms** (poor), CLS **0.24** (poor). Three failures. Nobody in the company had run it.
3. **LCP: Lighthouse names the element** — the hero image. Network panel: **900 KB**, uncompressed, and it sits behind a render-blocking stylesheet (Module 3, ch2). Two fixes, both boring: compress it, and preload it.
4. **CLS: the report lists the shifting elements** — the hero image (no `width`/`height`, last note's exact bug) and an ad slot inserted after paint. Rendering → Layout Shift Regions confirms it live, at 1.4s.
5. **INP: Performance panel** shows a 480ms long task on the main thread during load — a bundle parsing while JavaScript's single thread (ch3) can't paint anything. Clicks queue. Users click twice.
6. **Now interpret it as a human story.** A mobile user waits four seconds, watches the page shove itself around, taps a button, gets nothing, taps again, and leaves. That is the conversion drop, and it has nothing whatsoever to do with the design.
7. **The report:** all three metrics, their thresholds, the exact elements, and the conditions. Plus one honest sentence: *the design was never measured; the delivery was never tested.*
8. **The redesign was cancelled.** Compressing one image, adding two HTML attributes, and code-splitting one bundle moved all three metrics into the green — and conversion followed. A tester with a browser and two days beat a redesign budget, because they had numbers and everyone else had feelings.

> **Common mistake**
>
> Measuring performance on your own machine and believing the result. Your laptop's CPU
> parses JavaScript several times faster than a mid-range phone's. Your cache already holds
> every image, correctly sized, so nothing shifts. Your connection is fast and your server
> is close. Under those four conditions, *every site on earth passes Core Web Vitals* —
> which is precisely why they are measured with throttling and a cold cache. If your
> performance testing has never made you uncomfortable, you have not yet tested your
> product; you have tested your hardware, and it passed with flying colours.

**Quiz.** Lighthouse reports LCP 4.2s, INP 610ms, CLS 0.24 on mobile. The page feels instant on your laptop. What is the correct conclusion?

- [ ] Lighthouse is unreliable — trust the real experience
- [x] All three fail their thresholds (2.5s / 200ms / 0.1) under simulated mid-range-phone conditions with a cold cache. Your laptop's fast CPU, warm cache and proximity to the server hide all three problems. The numbers describe your users; your feeling describes your hardware.
- [ ] Only CLS matters, since users notice movement most
- [ ] The design needs to be modernized

*Every one of these metrics is a first-visit, cold-cache, throttled measurement precisely because that's what a real visitor experiences. A fast laptop parses the JavaScript bundle in a fraction of the time (hiding INP), holds pre-sized images in cache (hiding CLS), and sits close to the server (hiding LCP). Under those conditions any site passes. The discomfort of a bad Lighthouse score is the sensation of finally testing your product rather than your machine.*

- **The three vitals** — LCP — biggest element paints (≤2.5s). INP — click to next painted frame (≤200ms). CLS — how much content jumped (≤0.1).
- **What each maps to** — LCP = the six load stages. INP = the paint-to-interactive gap and JS's single thread. CLS = reflow from images without dimensions, late ads, font swaps.
- **Why your laptop always passes** — Fast CPU (hides INP), warm cache with sized images (hides CLS), proximity to the server (hides LCP). Throttle and hard-reload or you're testing hardware.
- **How to file it** — Metric + threshold + conditions + the named element. 'LCP 4.2s vs 2.5s on Slow 4G + 4x CPU; LCP element is a 900 KB hero image.' Unarguable.
- **Lighthouse throttles for you** — It simulates a mid-range phone on a slow network. Its numbers look wrong because you are not a typical user. Reproduce before disputing.
- **Lab vs field data** — Lab = your machine, simulated. Field = real users, aggregated. Prefer field data when it exists; never argue a two-point lab difference.

### Challenge

Run Lighthouse (mobile) on three sites: one you love, one you hate, and your own project
if you have one. Write down LCP, INP and CLS for each, and for the worst offender, name
the exact element Lighthouse blames. Then predict which one users complain about most —
and check whether the numbers agree with your prediction. That's the last exercise of
Module 4, and it uses every note in it.

### Ask the community

> Vitals question: Lighthouse (mobile) reports LCP [x]s, INP [y]ms, CLS [z]. LCP element: [what Lighthouse names]. Shifting elements: [list]. Conditions: hard reload, Slow 4G, 4x CPU. On my laptop it feels [fine/slow]. Where should I look first?

Including 'on my laptop it feels fine' is not an admission of weakness — it's the most
diagnostic line in the template. That contrast is exactly what Core Web Vitals exist to
surface, and naming it up front stops the conversation from becoming an argument about
whose experience is real. Both are. Only one belongs to a customer.

- [web.dev — Core Web Vitals: LCP, INP and CLS defined](https://web.dev/articles/vitals)
- [Lighthouse — running an audit and reading the report](https://developer.chrome.com/docs/lighthouse/overview/)
- [Core Web Vitals, explained with real pages](https://www.youtube.com/watch?v=AQqFZ5t8uNc)

🎬 [LCP, INP and CLS in practice](https://www.youtube.com/watch?v=AQqFZ5t8uNc) (11 min)

- Three metrics turn feelings into facts: LCP (≤2.5s, it appears), INP (≤200ms, it responds), CLS (≤0.1, it stays still).
- Each maps onto something this module already taught: the six load stages, JavaScript's single thread, and reflow from undeclared image dimensions.
- Your laptop passes every one of them — fast CPU, warm cache, nearby server. Throttle and hard-reload, or you are testing your hardware.
- File performance bugs as metric + threshold + conditions + the named element. That report cannot be argued with, only fixed or explicitly deprioritized.
- Lighthouse applies mobile throttling for you. When its number disagrees with your feeling, the number is describing your users.


---
_Source: `packages/curriculum/content/notes/the-web-platform-for-testers/how-browsers-render/core-web-vitals-awareness.mdx`_
