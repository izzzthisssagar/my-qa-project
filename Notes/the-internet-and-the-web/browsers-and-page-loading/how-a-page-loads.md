---
title: "How a page loads"
tags: ["internet", "browsers", "performance", "track-a"]
updated: "2026-07-10"
---

# How a page loads

*One page is never one download. Learn the critical path, why a single CSS file can hold the whole screen hostage, and how to tell a slow network from a slow app in under a minute.*

> "The page is slow" is the least useful sentence in software. Slow to *appear*? Slow to
> become *usable*? Slow because the network is far away, or because a 340 KB script is
> blocking the parser, or because the server took two seconds to think? These are four
> different bugs with four different owners, and the browser will tell you which one it
> is — in about sixty seconds, for free, if you know where to look.

> **In real life**
>
> A page load is **a restaurant order, not a delivery.** The HTML is the menu — and only
> when the waiter reads the menu aloud does the kitchen discover it also needs to fetch
> the wine, the bread and the cutlery, each from a different shop. The waiter can't serve
> anything until the cutlery arrives, because someone declared cutlery essential. That
> "can't start until X arrives" chain is called the **critical path**: The chain of resources that must be downloaded and processed before the browser can paint anything. CSS is render-blocking and synchronous scripts are parser-blocking, so each one lengthens the chain — and the user watches a blank screen for its whole duration., and shortening it
> is most of web performance.

## The sequence, honestly

1. **DNS** — turn the name into an IP address. (New name? A lookup. Cached? Free.)
2. **TCP + TLS handshake** — open the connection, agree encryption. Several round trips *before any content moves*.
3. **HTML arrives** — the browser parses it top to bottom.
4. **Discovery** — every `<link>`, `<script>`, `<img>` found while parsing triggers *another* request. The browser didn't know about them a moment ago.
5. **Render-blocking work** — CSS must be downloaded and parsed before anything is painted (otherwise you'd see unstyled text flash). A synchronous `<script>` pauses parsing entirely.
6. **Paint** — first pixels. The user finally sees something.
7. **JavaScript runs** — and may rebuild the entire page.
8. **Interactive** — clicks now do things.

Between step 6 and step 8 lies the cruellest bug in web software: a page that *looks*
ready and ignores every click.

![A diagram of a browser sending a request and receiving a response from a server](request-response.png)
*Diagram: request and response — Wikimedia Commons, CC0. [Source](https://commons.wikimedia.org/wiki/File:Ajax_request_response.svg)*
- **The browser — where waiting happens** — Everything on the user's side: DNS lookup, handshake, parsing, rendering, running JavaScript. When people say 'the page is slow', roughly half the time the fault lives here, in code shipped to them by developers with fast laptops.
- **The request — one of dozens** — This single arrow happens 30 to 100 times per page. Each one costs at least one round trip (chapter 1: 12ms nearby, 187ms across an ocean). The number of arrows matters more than the size of any one of them.
- **The server — thinking time (TTFB)** — Time To First Byte: how long the server took before sending anything at all. High TTFB with a small response = the server is slow, not the network. That one distinction assigns the bug to the right team, and it's visible in DevTools as 'Waiting (TTFB)'.
- **The response — headers, then body** — Every response carries a status code (200, 404, 500) and headers, including caching instructions. The headers decide whether the NEXT visit needs this arrow at all. A well-cached asset costs zero round trips forever.
- **Repeat, for everything** — This whole diagram runs again for each stylesheet, script, font and image. Which is why 'how fast is your connection' is a much less interesting question than 'how many times does this page make the trip'.

**The critical path — why the screen stays blank — press Play**

1. **📄 HTML arrives (18 KB)** — The browser starts parsing immediately, top to bottom. It could paint text right now — but it doesn't, because it hasn't seen the styles yet, and painting unstyled text then restyling would flash horribly.
2. **🎨 It meets a stylesheet — STOP** — A `link rel=stylesheet` is render-blocking. Nothing paints until that CSS is fetched AND parsed. One 82 KB file, one round trip, and the user watches a white screen. This is the most common cause of a slow-feeling page.
3. **📜 It meets a synchronous script — STOP AGAIN** — A plain `script src=...` pauses HTML parsing entirely: the browser must fetch, then execute, before it reads the next line. Because that script might write into the document. Marking it `defer` or `async` removes it from the critical path — a one-word fix worth seconds.
4. **🖼 First paint** — Styles resolved, layout computed, pixels drawn. The user finally sees content. Everything before this moment was a blank screen, and every blocking resource extended it.
5. **🖱 Interactive — much later** — The main JavaScript bundle still has to download, parse and execute. Until it does, the page LOOKS finished and every click is discarded. Users click three times, get nothing, and leave. This gap has a name — and it's where the worst usability bugs hide, invisible to anyone testing on a fast laptop.

*Try it — compute the critical path, then fix it with one word*

```python
RTT = 180        # ms — a real user, one ocean away
BW  = 5_000      # KB/s — a decent mobile connection

def fetch(kb):
    return RTT + (kb / BW) * 1000        # one round trip + transfer time

# The page as shipped:
print("BEFORE — everything blocking:")
t = 0
t += fetch(18);   print(f"  {t:6.0f} ms  html (18 KB) parsed")
t += fetch(82);   print(f"  {t:6.0f} ms  styles.css (82 KB) — RENDER BLOCKING")
t += fetch(340);  print(f"  {t:6.0f} ms  app.js (340 KB) — PARSER BLOCKING")
print(f"  {t:6.0f} ms  <- first paint. User has seen a white screen this whole time.")
before = t
print()

# One word: defer. The script no longer blocks the parser; CSS still blocks paint.
print("AFTER — <script defer>:")
t = 0
t += fetch(18);   print(f"  {t:6.0f} ms  html parsed")
t += fetch(82);   print(f"  {t:6.0f} ms  styles.css — still render blocking")
print(f"  {t:6.0f} ms  <- first paint (app.js downloads in parallel, runs after)")
after = t
print()
print(f"first paint: {before:.0f}ms -> {after:.0f}ms   saved {before-after:.0f}ms")
print()
print("Same bytes. Same network. Same server. One attribute.")
print("This is why 'the page is slow' is never a complete bug report:")
print("slow to PAINT and slow to become INTERACTIVE have different causes.")
```

## Reading a waterfall

Open DevTools → Network, reload, and you get a **waterfall** — every request as a bar,
positioned by when it started and how long it took. Three shapes tell you almost
everything:

- **A long bar before anything else starts** → high TTFB. The *server* is slow. Not your network, not the browser.
- **Many short bars in a staircase** → requests discovered one after another (each one had to be found by parsing the previous). The *page structure* is slow.
- **One enormous bar** → a huge asset. Usually an unoptimized image or a giant JavaScript bundle. The *payload* is slow.

> **Tip**
>
> The single most valuable habit in this whole chapter: **throttle before you judge.**
> DevTools → Network → Slow 4G, and CPU 4× slowdown. Now reload. Everything you believed
> about your app's performance was measured on a fast laptop, on a fast connection, next
> to the server. Under throttling, that 340 KB bundle isn't a number in a table — it's
> four seconds of a user staring at nothing. Test the experience your users have, not the
> one your hardware grants you.

### Your first time: Your mission: watch one page load, properly

- [ ] Open the Network panel and reload — F12 → Network → Ctrl+R. Count the requests at the bottom, note the total transferred. Most pages are 40–120 requests. Sit with that number for a moment.
- [ ] Find the TTFB — Click the first request (the HTML). Look at 'Waiting (TTFB)'. Under 200ms is healthy; over a second means the server was thinking, and no front-end change will help.
- [ ] Find the biggest thing — Sort by Size. Almost always an image or a JS bundle. Ask: does the page need all of it before first paint? Usually, no.
- [ ] Throttle to Slow 4G and reload — The dropdown that says 'No throttling'. Reload and watch. How long is the screen blank? How long until a click does something? That's your app, for a large fraction of the planet.
- [ ] Compare cached vs uncached — Reload normally (fast, mostly from cache), then hard reload (Ctrl+Shift+R, everything refetched). Your users' first visit is the second number. You've only ever experienced the first.

You measured TTFB, found the payload, and experienced your own page on a real network. That's a performance audit, and it took five minutes.

- **The page takes 4 seconds to show anything, but the network looks fast.**
  Check TTFB on the first HTML request. If it's 3 of those 4 seconds, the SERVER is slow — a database query, a cold start, an unindexed lookup — and no image optimization will touch it. If TTFB is small, look for render-blocking CSS and synchronous scripts on the critical path. Two different teams, and the waterfall tells you which one to talk to.
- **The page appears instantly but clicking does nothing for a few seconds.**
  The gap between 'painted' and 'interactive'. The HTML and CSS arrived fast; the JavaScript bundle is still downloading, parsing and executing, so no event handlers exist yet. Users click, nothing happens, they click again. Fix: ship less JavaScript, split the bundle, defer non-essential code. Report it as 'page is visually complete at 0.8s but not interactive until 4.2s' — that sentence is worth ten screenshots.
- **It's fast for me and slow for everyone else.**
  Three causes, all in this module. (1) Your cache is warm and theirs isn't (hard reload to test what a first-time visitor gets). (2) You're near the server and they're not (chapter 1: latency is geography). (3) Your laptop parses that JavaScript bundle five times faster than their phone. Throttle network AND CPU before you conclude anything at all.
- **Some images load, then the layout jumps and everything moves.**
  The images arrived after layout was computed, because no width and height were declared — so the browser reserved no space and had to redo the layout. It's called layout shift, it's infuriating, it makes people click the wrong button, and it's fixable in one line of HTML. A real, reportable bug that most teams never file because it isn't a crash.

### Where to check

The Network panel, read like a professional:

- **Request count and total size** (bottom bar) — the scale of the problem, before any theorizing.
- **TTFB on the first request** — splits "slow server" from "slow everything else" in one glance. Do this first, always.
- **The waterfall shape** — staircase (structure), one long bar (payload), long first bar (server).
- **The Size column: "from cache" vs a real number** — you have been testing the warm-cache experience your users never have.
- **Throttling (Slow 4G) + CPU 4× slowdown** — the only honest test of a real user's device.
- **The Timing tab of any request** — DNS, connection, TLS, waiting, download, each measured separately. Chapter 1's whole journey, itemized in milliseconds.

Tester's angle: performance bugs are *specific*. "Slow" is not a bug report. "TTFB is
2.4s on /checkout while other pages are 180ms" is a bug report — one that names the
endpoint, the metric, and the comparison that proves it's abnormal.

### Worked example: the homepage that was slow for one reason nobody guessed

Marketing says the homepage is slow. Engineering says it's fine on their machines. Both are telling the truth.

1. **Get a number, not an adjective.** Open DevTools, throttle to Slow 4G, hard reload. First paint: **6.1 seconds**. Nobody had ever measured it under throttling.
2. **Check TTFB first** (the cheapest split). 140ms. The server is *innocent* — that eliminates the entire backend team from the investigation in one glance.
3. **So it's on the critical path.** The waterfall shows a staircase: HTML → a font stylesheet → a font file → and only then any paint. Each step waited for the one before it, because each was discovered by parsing the previous one.
4. **The culprit:** a web font loaded via a third-party stylesheet. Two extra DNS lookups, two extra TLS handshakes, two extra round trips at 180ms each — all *before the first pixel*, all to make the headline look nicer.
5. **The proof:** block that domain in DevTools, reload. First paint drops to **1.3 seconds**. That's not a theory anymore; it's an experiment with a control.
6. **The report:** 'Third-party font stylesheet adds ~4.8s to first paint on Slow 4G (2 extra DNS + TLS round trips on the critical path). Self-hosting the font, or `font-display: swap`, removes it. Evidence: waterfall before/after.' Nobody argues with that. And notice the tester needed no source access, no build system, no permission — only the Network panel and the willingness to throttle.

> **Common mistake**
>
> Testing performance on your own machine, on your office Wi-Fi, with a warm cache, next
> to the server, and concluding the app is fast. Every one of those five conditions is
> false for your users. Their cache is cold, their phone parses JavaScript several times
> slower, their packets cross an ocean, and their connection jitters (chapter 1's whole
> lesson). The performance you experience is not a sample of your users' experience — it
> is the single most favourable outcome the system can produce, and you are the only
> person on earth who will ever see it.

**Quiz.** A page shows content in 0.9 seconds but ignores clicks until 4.5 seconds. TTFB is 120ms and the CSS is small. Where's the bug?

- [ ] The server is slow — check the database
- [x] The JavaScript bundle: it's still downloading, parsing and executing after the page has painted, so no event handlers exist yet. The page looks finished and isn't. Ship less JS, split the bundle, or defer non-essential code.
- [ ] The user's internet connection
- [ ] The images are too large

*Low TTFB exonerates the server; small CSS exonerates the render-blocking styles. A fast paint with a long delay before interactivity is the signature of a heavy JavaScript bundle — the HTML and CSS drew the page, but the code that makes it respond hasn't finished executing. This is the cruellest failure mode in web software because it's invisible on a fast laptop and infuriating on a real phone: the button is right there, and it does nothing.*

- **The critical path** — The chain of resources that must arrive before the first pixel. CSS is render-blocking; a synchronous script is parser-blocking. Shortening this chain is most of web performance.
- **TTFB** — Time To First Byte — how long the server thought before sending anything. High TTFB = slow server, and no front-end fix will help. Check it first; it's the cheapest split.
- **Paint vs interactive** — A page can look finished while its JavaScript is still executing, so clicks are discarded. 'Visually complete at 0.8s, interactive at 4.2s' is a real, reportable bug.
- **One page ≠ one request** — Typically 30–100 requests, each discovered by parsing the previous resource. Request count matters more than any single file's size.
- **defer / async** — Removes a script from the parser's critical path: it downloads in parallel and runs later. A one-word change that can save seconds of blank screen.
- **Throttle before you judge** — Slow 4G + 4× CPU slowdown. Your fast laptop, warm cache and proximity to the server produce the single most favourable result the system can ever give.

### Challenge

Pick any website you use daily. Open DevTools → Network, throttle to Slow 4G, hard
reload, and time three things with a stopwatch: when you see anything, when the page
looks done, and when a click actually works. Write down the three numbers and the
biggest file in the waterfall. You have just performed a real performance audit — the
same one consultants charge for — using nothing but a panel that ships in every browser.

### Ask the community

> Page load question: [url or page]. Throttled to Slow 4G: first paint [Xs], interactive [Ys]. TTFB on the HTML: [Zms]. Request count: [N], total transferred: [KB]. Biggest asset: [name, size]. Waterfall shape: [staircase / one long bar / long first bar].

Each of those fields points at a different owner: TTFB at the backend, the waterfall
shape at page structure, the biggest asset at the build. Collect them and you'll often
name the culprit before you finish typing — which is exactly what happened in this
note's worked example.

- [web.dev — the critical path, explained by the people who built the tools](https://web.dev/learn/performance/)
- [Chrome DevTools — reading the network panel](https://developer.chrome.com/docs/devtools/network/)
- [How a web page actually loads](https://www.youtube.com/watch?v=WjDrMKZWCt0)

🎬 [Page load, the critical path, and why it's blank](https://www.youtube.com/watch?v=WjDrMKZWCt0) (10 min)

- One page is 30–100 requests, most discovered only by parsing an earlier resource. Request count matters more than any single file's size.
- CSS blocks rendering and synchronous scripts block parsing — that chain is the critical path, and shortening it is most of web performance.
- Check TTFB first: it splits 'slow server' from everything else in one glance and exonerates whole teams.
- A page can be painted but not interactive. 'Visually complete at 0.8s, interactive at 4.2s' is a real bug and invisible on a fast laptop.
- Throttle network and CPU before judging performance. Your warm cache, fast device and proximity to the server produce the best result the system will ever give anyone.


---
_Source: `packages/curriculum/content/notes/the-internet-and-the-web/browsers-and-page-loading/how-a-page-loads.mdx`_
