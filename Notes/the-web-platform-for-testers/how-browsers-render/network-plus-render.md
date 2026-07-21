---
title: "Network + render = page load"
tags: ["web-platform", "rendering", "performance", "track-a"]
updated: "2026-07-10"
---

# Network + render = page load

*Everything from Modules 3 and 4 in one picture: the request, the critical path, the two trees, the paint. Learn to read a page load end to end and you can locate any performance bug in one recording.*

> You now know how a request crosses an ocean, how a browser parses HTML, how CSS blocks
> paint, how JavaScript rewrites the DOM, and what a reflow costs. This note is where all
> of it becomes **one timeline** — the thing you record, read, and hand to a developer with
> a fault already circled. Page load isn't one thing that's slow. It's six things in a row,
> and only one of them is ever the culprit.

> **In real life**
>
> A page load is **a relay race, not a sprint.** The baton passes from DNS to the network,
> to the parser, to the stylesheet, to the layout engine, to JavaScript. The team's time
> is the sum of six runners, and shouting "run faster" at the whole team is useless. You
> need to know **which runner is slow**, and every one of them is separately timed, in a
> panel you already have open.

## The six stages, in order, with their tell-tale symptom

1. **DNS + connect + TLS** — before any content moves. Slow here means a cold DNS lookup or a distant server (Module 3, ch1).
2. ****TTFB**: Time To First Byte — how long the server took before sending anything at all. Under 200ms is healthy. It is the cheapest split in performance testing: a low TTFB exonerates the entire backend in one glance.** — the server thinking. High TTFB means a slow backend; nothing on the front-end will help.
3. **Download HTML** — usually fast; it's small.
4. **Critical path** — CSS must arrive and parse before paint; synchronous scripts block the parser (Module 3, ch2).
5. **First paint** — pixels. The user finally sees something.
6. **JavaScript → interactive** — the bundle downloads, parses, executes, attaches handlers. Until then the page is a mannequin.

Slow at stage 2 and slow at stage 6 are *different bugs owned by different people*, and
they feel identical to a user. That's the whole reason this note exists.

![A browser displaying a fully loaded page — the end of a six-stage pipeline](browser-render.png)
*Screenshot: Firefox browser — Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Firefox_Browser_Creative_Commons_screenshot.png)*
- **One URL. Then thirty to a hundred more requests.** — The HTML is the only thing you asked for. Everything else — stylesheets, scripts, fonts, images — was discovered by parsing it, and each costs at least one round trip. Request COUNT usually matters more than any single file's size.
- **What you see = first paint** — Reached only after the CSS arrived and parsed. Everything before this moment was a blank white screen, and every render-blocking resource made it longer. This is the number users describe as 'how fast the site is'.
- **What responds = interactive, much later** — The JavaScript bundle still has to download, parse and execute before a single click does anything. The gap between paint and interactive is invisible on your laptop and brutal on a phone.
- **Hard reload = what a first-time visitor gets** — Ctrl+Shift+R bypasses the cache. Your normal reload measures the experience of someone who has already visited. Those are two different products, and you have only ever tested one.
- **Performance panel: the whole race, drawn** — Record a load and every stage is a bar with a duration. Purple layout, green paint, yellow scripting, blue loading. One recording, six answers, and the slow runner is obvious on sight.

**Six stages, one timeline, one culprit — press Play**

1. **🔎 DNS + TCP + TLS (0–300ms)** — The name becomes an IP, a connection opens, encryption is agreed. Several round trips before a single byte of content moves. On a distant server at 187ms RTT, this alone can cost half a second — and no code change touches it. Only a CDN does.
2. **⏳ TTFB — the server thinks** — Time To First Byte. Under 200ms is healthy. Two seconds means a database query, a cold serverless start, an unindexed lookup. Check this FIRST: it exonerates or convicts the entire backend in one glance.
3. **📄 HTML parses → the DOM grows** — Top to bottom. Every stylesheet and script the parser meets triggers another request. A synchronous script STOPS parsing entirely until it has downloaded and run.
4. **🎨 CSS arrives → render tree → layout → PAINT** — Now the two trees combine, every box gets geometry, and pixels appear. This is first paint. Everything before it was a white screen. Render-blocking CSS sets its floor.
5. **⚙️ JS executes → handlers attach → INTERACTIVE** — The bundle downloads, parses, runs. Only now do clicks work. On a mid-range phone, parsing 340 KB of JavaScript can take longer than downloading it — and the page has looked ready this whole time.

*Try it — find the slow runner in a real-looking load*

```python
# A page load, itemized. Which stage would you attack?
stages = [
    ("DNS + connect + TLS", 280),
    ("TTFB (server thinking)", 1900),
    ("Download HTML", 60),
    ("CSS (render blocking)", 340),
    ("First paint", 0),
    ("JS download + parse + execute", 2200),
]
total = sum(ms for _, ms in stages)
paint = sum(ms for n, ms in stages[:5])

print(f"{'stage':32} {'ms':>6}  {'share':>6}")
print("-" * 50)
for name, ms in stages:
    bar = "█" * max(1, round(ms / 100))
    print(f"{name:32} {ms:6}  {ms/total*100:5.1f}%  {bar}")
print("-" * 50)
print(f"{'first paint at':32} {paint:6} ms")
print(f"{'interactive at':32} {total:6} ms")
print()

worst = max(stages, key=lambda s: s[1])
print(f"Biggest single cost: {worst[0]} ({worst[1]}ms)")
print()
print("Two stages own 79% of this load: the SERVER (1900ms TTFB) and the")
print("JS BUNDLE (2200ms). Optimizing images here would save nothing.")
print()
print("Note the trap: the user SEES the page at", paint, "ms and cannot USE it")
print("until", total, "ms. They will click during that", total - paint, "ms gap")
print("and nothing will happen. That is the bug nobody files.")
```

## Reading one recording

Open **Performance → record → reload → stop.** You get colours:

- **Blue** — loading (network).
- **Yellow** — scripting (JavaScript executing).
- **Purple** — rendering (layout/reflow).
- **Green** — painting.

A wall of yellow before anything appears? Too much JavaScript. A long blue bar first?
TTFB or a slow asset. Purple bars during scroll? Reflow on every frame (last note).

> **Tip**
>
> The single most honest performance test, and it takes ninety seconds: **hard reload
> (Ctrl+Shift+R) with Slow 4G and 4× CPU throttling on, then time three moments with a
> stopwatch** — when you first see anything, when it looks finished, and when a click
> actually works. Three numbers. They map exactly onto the stages above, and any one of
> them being bad points at exactly one owner. This is what expensive consultants do, and
> the tooling ships free in your browser.

### Your first time: Your mission: record the whole race

- [ ] Record a cold load — Performance panel → the reload-and-record icon (not just record). Throttle to Slow 4G, CPU 4×. You now have the whole timeline of a first-time visitor on a phone.
- [ ] Find TTFB — Network panel → click the first HTML request → Timing → 'Waiting (TTFB)'. Under 200ms means the backend is fine and you can stop suspecting it.
- [ ] Find the render-blocking resources — In the timeline, look at what completes just before first paint. That stylesheet is your paint's floor. Nothing appears until it lands.
- [ ] Measure the paint→interactive gap — Note when content appears and when the yellow scripting finally stops. That gap is the mannequin window. Click a button inside it and watch nothing happen.
- [ ] Compare warm and cold — Reload normally (warm cache), then hard reload. Two very different timelines. Your users mostly get the second one, and you have mostly tested the first.

One recording, six stages, three stopwatch numbers. You can audit any page on earth now.

- **The page takes 5 seconds and I don't know who to blame.**
  Split it. TTFB over 1s → backend. Long gap between HTML arriving and first paint → render-blocking CSS or a synchronous script. Long gap between paint and interactive → the JavaScript bundle. Three checks, three owners, and each has an entirely different fix. Never file 'the page is slow' — file the stage.
- **Lighthouse gives a bad score but the site feels fine to me.**
  Lighthouse simulates a mid-range phone on a slow network with a cold cache. You are on a fast laptop, on office Wi-Fi, with everything cached, sitting near the server. Lighthouse is not wrong — it is describing a user you have never been. Reproduce its conditions (throttle + hard reload) before disputing its number.
- **First paint is fast but the page is unusable for 4 seconds.**
  Classic paint/interactive gap. HTML and CSS arrived quickly; the JavaScript bundle is still parsing and executing, so no handlers exist. Users click, nothing happens, they click again — and then two things fire at once. Report it with both numbers: 'visually complete at 0.8s, interactive at 4.6s'. That sentence names a real and often-ignored bug.
- **It's fast in production but slow in my local dev environment.**
  Almost always the opposite direction of the usual bug, and almost always meaningless: dev builds are unminified, unbundled, source-mapped and hot-reloading. Never benchmark a dev server. Build for production and serve it, or measure the real deployment. Performance conclusions from `pnpm dev` are noise.

### Where to check

The whole load, one panel at a time:

- **Network → the first request → Timing tab** — DNS, connect, TLS, waiting (TTFB), download. Stage 1 and 2, itemized in milliseconds.
- **Network → bottom bar** — request count and total transferred. Scale before theory.
- **Performance → record with reload** — the whole race, colour-coded, with a filmstrip of what the user actually saw at each moment.
- **Lighthouse** — the same audit, scored, with the throttling already applied. Run it before disputing it.
- **Throttling: Slow 4G + CPU 4×, and hard reload** — the only honest configuration. Everything else is testing yourself.

Tester's habit: **three stopwatch numbers on every page you audit** — first paint,
visually complete, interactive. They cost ninety seconds, they map onto the six stages,
and they turn "slow" into a stage, an owner, and a fix.

### Worked example: the five-second page with three innocent suspects

Everyone blames a different thing. The recording settles it in one pass.

1. **The complaint:** the dashboard takes about five seconds. Backend says their APIs are fast. Front-end says the bundle is fine. Design blames the images.
2. **Record it properly:** Performance panel, reload-and-record, Slow 4G, CPU 4×. One recording, everyone watching.
3. **Stage 2 — TTFB: 180ms.** The backend is innocent, provably, in the first ten seconds of the meeting. (Note how much heat this removes from the room.)
4. **Stage 4 — first paint at 1.1s.** So CSS wasn't the problem either. The page appeared quickly.
5. **Stage 6 — interactive at 4.9s.** A wall of yellow: **2.2 seconds downloading and 1.6 seconds *parsing and executing* a 340 KB JavaScript bundle** on a throttled CPU. The images finished long before, and contributed nothing to the delay.
6. **The insight the whole room missed:** the page was *visually complete at 1.1s*. Everyone testing on a laptop saw it appear instantly and concluded it was fast. Every user on a phone saw the same thing and then clicked a button that ignored them for nearly four seconds.
7. **The report:** 'Dashboard is visually complete at 1.1s and interactive at 4.9s on Slow 4G + 4× CPU. Cause: 340 KB JS bundle, 1.6s of parse+execute. TTFB 180ms (backend fine), images not on the critical path. Suggest code-splitting the dashboard route.'
8. **Nobody argued.** Not because the tester was persuasive, but because a recording is not an opinion. Three suspects, one timeline, one culprit — and the fix was assigned in the same meeting.

> **Common mistake**
>
> Optimizing the stage that isn't slow. Teams compress images for a week while a 340 KB
> JavaScript bundle spends 1.6 seconds parsing on every phone that visits. Images are
> visible, familiar and easy to blame; parse time is invisible and lives in a panel nobody
> opens. The stages are separately measured *precisely so you don't have to guess* — and
> guessing is exactly what happens when nobody records the load. Measure first, and let the
> timeline choose the target. The satisfaction of a week of image compression that saved
> forty milliseconds is not worth the four seconds you left on the table.

**Quiz.** A page has TTFB 180ms, first paint at 1.1s, and becomes interactive at 4.9s under Slow 4G + 4× CPU. Where is the time going and who owns it?

- [ ] The backend — 180ms TTFB is too slow
- [x] The JavaScript bundle. TTFB exonerates the server and the fast first paint exonerates the CSS. The 3.8s between paint and interactive is the bundle downloading, parsing and executing — so the page looks finished while ignoring every click. Front-end owns it; code-splitting is the fix.
- [ ] The images — they always dominate page weight
- [ ] The network — the user should get faster internet

*Each stage is separately measured so you don't have to guess. 180ms TTFB is healthy, and a 1.1s first paint means CSS and HTML did their jobs. The entire remaining 3.8 seconds sits between paint and interactive, which is exactly the window in which a JavaScript bundle downloads, parses and executes. Images cannot cause this — they don't block interactivity. This is also the cruellest failure mode in web software: on a laptop it's invisible, because parse time scales with CPU, and yours is four times faster than your user's.*

- **The six stages** — DNS+connect+TLS → TTFB → download HTML → critical path (CSS/blocking JS) → first paint → JS executes → interactive.
- **TTFB** — Time To First Byte: how long the server thought. Under 200ms is healthy. Check it first — it convicts or exonerates the entire backend in one glance.
- **Paint vs interactive** — Two different moments. A page can be visually complete at 1.1s and ignore clicks until 4.9s. Report both numbers.
- **Performance panel colours** — Blue = loading, yellow = scripting, purple = rendering/layout, green = paint. A wall of yellow before content means too much JavaScript.
- **The only honest config** — Hard reload + Slow 4G + 4× CPU. Anything else measures you, not your users.
- **The three stopwatch numbers** — When you first see anything, when it looks finished, when a click works. Ninety seconds, and each maps to one stage and one owner.

### Challenge

Record a cold, throttled load of any site you use daily (Performance → reload-and-record,
Slow 4G, CPU 4×). Write down three numbers: first paint, visually complete, interactive.
Then look at which colour dominates the timeline. In under two minutes you'll know
whether that site's problem is its server, its stylesheets, or its JavaScript — and you'll
know it more precisely than most of the people who work on it.

### Ask the community

> Page-load question: on Slow 4G + 4x CPU, first paint [Xs], visually complete [Ys], interactive [Zs]. TTFB on the HTML: [ms]. Request count: [N], transferred: [KB]. Biggest asset: [name, size]. Timeline is mostly [blue/yellow/purple].

Those six facts assign the bug before anyone answers: TTFB names the backend, the
paint-to-interactive gap names the bundle, purple names reflow. It's the same
stage-splitting from this note, compressed into a paste — and half the time you'll spot
the slow runner while typing.

- [web.dev — page load performance, stage by stage](https://web.dev/learn/performance/)
- [Chrome DevTools — recording and reading a performance profile](https://developer.chrome.com/docs/devtools/performance/)
- [Network and render, together](https://www.youtube.com/watch?v=ZTnIxIA5KGw)

🎬 [A page load, end to end](https://www.youtube.com/watch?v=ZTnIxIA5KGw) (12 min)

- A page load is six stages in a row: DNS/TLS, TTFB, HTML, critical path, first paint, JS to interactive. Only one is ever the culprit.
- Check TTFB first — under 200ms exonerates the backend instantly and stops the whole team suspecting it.
- First paint and interactive are different moments. 'Visually complete at 1.1s, interactive at 4.9s' is a real bug, invisible on a fast laptop.
- Record with Performance (reload-and-record, Slow 4G, 4× CPU). Blue is network, yellow is JavaScript, purple is layout. The dominant colour names the owner.
- Measure before optimizing. Teams compress images for a week while a JS bundle spends 1.6 seconds parsing on every phone that visits.


---
_Source: `packages/curriculum/content/notes/the-web-platform-for-testers/how-browsers-render/network-plus-render.mdx`_
