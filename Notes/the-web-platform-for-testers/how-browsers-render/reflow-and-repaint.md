---
title: "Reflow & repaint, gently"
tags: ["web-platform", "rendering", "performance", "track-a"]
updated: "2026-07-10"
---

# Reflow & repaint, gently

*Change a colour and the browser repaints. Change a width and it recomputes the geometry of the entire page. Knowing which is which explains janky scrolling, dropped frames, and the layout that jumps as you reach for a button.*

> You have, at some point, gone to click a button and had the page shove it sideways at
> the exact moment your finger arrived, so you clicked an advert instead. That was a
> **reflow**, and it wasn't bad luck — it was an image loading without declared dimensions.
> The browser had to recompute where everything on the page belonged, mid-reach. This note
> is about the difference between "recolour a thing" and "recompute the world," because
> one is nearly free and the other is why your phone gets warm.

> **In real life**
>
> **Repaint is repainting a wall. Reflow is moving a wall.** Repainting is annoying but
> local: the room's shape is unchanged, nothing else in the house cares. Moving a wall
> means measuring every room again, checking the doors still open, and possibly discovering
> the staircase no longer fits. The browser does the second thing far more often than
> anyone intends, and it does it while you are trying to click something.

## Three levels of cost

| Change | What the browser must redo | Cost |
|---|---|---|
| `color`, `background`, `visibility` | **Repaint** — redraw pixels | cheap |
| `width`, `height`, `margin`, `font-size`, adding a node | ****Reflow**: Reflow (or layout): the browser recomputes the position and size of elements. Because boxes affect their neighbours and ancestors, changing one element's geometry can force the entire page to be re-measured. It is the single most expensive routine operation in a browser.** — recompute geometry, then repaint | expensive |
| `transform`, `opacity` | **Composite** — the GPU shifts an existing layer | nearly free |

That third row is why smooth animations use `transform: translateX()` instead of
`left:` — one moves a finished picture, the other re-measures the page sixty times a
second.

![A rendered browser page whose layout is computed from boxes](browser-render.png)
*Screenshot: Firefox browser — Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Firefox_Browser_Creative_Commons_screenshot.png)*
- **Every visible thing is a box with geometry** — Position, width, height — computed during layout for every node in the render tree. Change one box's size and its siblings shift, its parent resizes, and the shift climbs the tree. Nothing about a page is truly local.
- **An image with no width/height = a future reflow** — The browser reserves no space for it, lays the page out without it, then the image arrives and everything below jumps down. That's Cumulative Layout Shift, and it is entirely preventable by typing two numbers into the HTML.
- **Content below the fold pays for shifts above it** — A banner that loads late pushes down every element beneath it. The user was reading a paragraph; now they're reading a different one. The bug is felt lower on the page than where it was caused.
- **Fonts arrive late and re-measure the text** — A web font loads after the fallback font has already been laid out. Different letter widths, so every line rewraps, so the text block changes height, so everything below moves. Two seconds after you started reading.
- **Where DevTools proves it** — Performance panel → record → look for purple 'Layout' bars. Each one is a reflow. A stack of them during a scroll is why the page feels like it's stuttering, and it names the script that caused each.

**One image loads. Watch the page rearrange itself. — press Play**

1. **📐 Layout runs — no image yet** — The HTML has an `img` tag with no width or height attributes. The browser can't know how big it'll be, so it reserves ZERO space. Everything below is laid out as though the image doesn't exist.
2. **👀 The user starts reading** — Text is painted, the page looks settled, and a human begins moving their finger toward a button. Nothing on screen suggests anything is still in flight. This is the calm before the shove.
3. **🖼 The image arrives — 400px tall** — Now the browser knows. It must give the image a box, which means the box below it moves down 400px, which means its parent grows, which means everything after it moves. A reflow ripples through the tree.
4. **🤬 Everything jumps** — The button the user was reaching for is now 400px lower, and an advert occupies where it used to be. The click lands on the advert. Every human on earth has done this, and every one of them blamed themselves.
5. **✅ The one-line fix** — Put `width` and `height` on the `img` tag. The browser reserves the correct box before the bytes arrive, lays out once, and nothing ever jumps. Two attributes. This is measured as Cumulative Layout Shift, and it is a real, reportable, trivially fixable bug.

*Try it — count how many elements one change forces the browser to re-measure*

```python
# A simplified page: a stack of blocks, each with a height.
page = [
    {"name": "header",  "h": 80},
    {"name": "hero-img","h": 0},     # no dimensions declared — reserves nothing!
    {"name": "intro",   "h": 120},
    {"name": "button",  "h": 44},
    {"name": "footer",  "h": 200},
]

def layout(blocks):
    y, positions = 0, {}
    for b in blocks:
        positions[b["name"]] = y
        y += b["h"]
    return positions

before = layout(page)
print("Layout pass 1 — image has no reserved space:")
for name, y in before.items(): print(f"   {name:10} y={y}")

# The image finally loads. It is 400px tall.
page[1]["h"] = 400
after = layout(page)
print("\\nLayout pass 2 — image arrived (400px):")
moved = 0
for name, y in after.items():
    delta = y - before[name]
    if delta: moved += 1
    print(f"   {name:10} y={y:4}  {'moved down ' + str(delta) + 'px' if delta else 'unchanged'}")

print(f"\\n{moved} of {len(page)} elements moved because ONE element got a size.")
print("The user was reaching for 'button'. It is now 400px lower.")
print()
print("Now declare the size up front:")
page2 = [dict(b) for b in page]; page2[1]["h"] = 400
print("   layout runs once, nothing ever moves:", layout(page2))
print()
print("Two HTML attributes (width, height) removed an entire class of bug.")
```

## What testers actually do with this

- **Watch for jumps.** Load a page slowly (throttle to Slow 3G) and *watch it settle*. Anything that moves after first paint is layout shift, and it's a bug with a metric attached.
- **Scroll and feel.** Janky scrolling means work is happening per frame. Performance panel → record → look for long purple Layout bars.
- **Resize the window.** Reflow on purpose. Layouts that break at odd widths are found in seconds, and almost nobody looks.

> **Tip**
>
> Reflow is not a thing you eliminate — it's how the page gets built in the first place.
> It's a thing you avoid doing *repeatedly and unnecessarily.* The tester's version of this
> is simple and physical: **throttle to Slow 3G and watch the page load without touching
> anything.** Every jump you see is a shift a real user experiences on every visit. Then
> narrow the window and watch it break. Two minutes, no code, and you'll have found more
> layout bugs than a week of clicking through happy paths.

### Your first time: Your mission: cause a reflow and watch it cost

- [ ] See the paint — DevTools → three-dot menu → More tools → Rendering → tick 'Paint flashing'. Now scroll and hover around. Green flashes are repaints. Some sites flash constantly — that's real work, happening for nothing.
- [ ] Watch layout jump — Throttle to Slow 3G and reload a news site. Watch text move as images and ads arrive. Time how long until it stops moving. That interval is what a real user lives with, every visit.
- [ ] Cause a reflow yourself — Console: `document.body.style.fontSize = '20px'`. Everything re-measures and rewraps at once — every line, every block. One property, one full-page reflow.
- [ ] Cause a composite instead — Console: `document.querySelector('h1').style.transform = 'translateX(100px)'`. It moves and nothing else does. The GPU shifted a finished layer. No layout, no repaint.
- [ ] Record the difference — Performance panel → record → do both of the above → stop. Purple 'Layout' bars appear for the font-size change and not for the transform. There's your proof, drawn.

Repaint seen, reflow caused, composite compared, and the whole thing recorded.

- **The page jumps while loading and I click the wrong thing.**
  Layout shift, and it's a measured, reportable bug (Cumulative Layout Shift — next-but-one note). Causes, in order of frequency: images without width/height attributes, ads and embeds inserted late, web fonts swapping in with different metrics, and content injected above the fold after paint. Report it with a throttled screen recording and the element that moved. The fix is usually two attributes.
- **Scrolling is janky on my phone but smooth on my laptop.**
  Work is happening per frame, and the phone's CPU can't finish in the 16ms a 60fps frame allows. Performance panel with 4× CPU throttling will show long tasks and Layout bars during scroll. Usually a scroll handler that reads element geometry (forcing a reflow) on every single scroll event. Very common, very fixable, almost never reported because testers test on laptops.
- **An animation stutters.**
  Check what's being animated. `left`, `top`, `width`, `height` trigger reflow every frame — 60 full-page re-measures per second. `transform` and `opacity` are composited on the GPU and cost almost nothing. This is worth reporting precisely: 'the menu animates `left`, causing layout on every frame; `transform: translateX` would be composited.' That sentence names the fix.
- **Everything is fine until I resize the window, then the layout breaks.**
  Resizing forces a full reflow — you've just run the layout algorithm at a width nobody tested. That's not the bug; the bug is whatever fell apart. Resizing is one of the cheapest bug-finding techniques in existence, and the device toolbar (Ctrl+Shift+M) does it systematically at real device widths.

### Where to check

Rendering work, made visible:

- **Rendering panel → Paint flashing** — green flashes mark repaints. Constant flashing on a static page is wasted work.
- **Rendering panel → Layout Shift Regions** — highlights exactly what moved, as it moves. The most damning thing you can put in a bug report.
- **Performance panel → record** — purple bars are Layout (reflow), green is Paint. Look for them during scroll or animation, where they have no business being.
- **CPU throttling (4×) + Slow 3G** — the conditions your users actually have. Jank appears; on your laptop it never does.
- **Device toolbar (Ctrl+Shift+M)** — resize systematically at real widths and watch what breaks.

Tester's habit: **load every page throttled, hands off the keyboard, and just watch it
settle.** Anything that moves after the first paint is a layout shift; every one is a
real user clicking the wrong thing. It requires no code knowledge and finds bugs that
happy-path clicking never will.

### Worked example: the donate button that moved 400 pixels

A layout-shift bug with real consequences, found in ninety seconds.

1. **Report:** "Users say they're accidentally clicking the newsletter signup instead of Donate." Product assumes it's a design problem and schedules a redesign.
2. **Reproduce the way a user experiences it:** throttle to Slow 3G, reload, and watch — hands off. At about 1.4 seconds, a hero image lands and the entire page below it slams down 400 pixels.
3. **Turn on Rendering → Layout Shift Regions.** The shifted area lights up. It's not subtle: the Donate button and the newsletter form swap positions on screen at the exact moment a user's finger would be arriving.
4. **Inspect the culprit.** `<img src="hero.jpg">` — no `width`, no `height`. The browser reserved zero space, laid out the page without it, then re-laid-out everything when the bytes arrived.
5. **Measure it honestly.** Lighthouse reports a Cumulative Layout Shift of 0.31. Anything above 0.1 is a failing score. This is not an aesthetic complaint; it is a number.
6. **Confirm the fix cheaply.** In DevTools, add `width="1200" height="600"` to the img. Reload throttled. **Nothing moves.** CLS drops to near zero. You proved the fix before anyone wrote code.
7. **The report:** 'Hero image lacks width/height attributes; the browser reserves no space and reflows the page when it loads, moving the Donate button 400px at ~1.4s on Slow 3G. CLS 0.31 (fails). Users click the newsletter form instead. Fix: declare the image's intrinsic dimensions. Verified locally by adding them — CLS ≈ 0.'
8. **The redesign was cancelled.** The design was never the problem. Two missing HTML attributes were, and a tester found them by watching a page load slowly and refusing to touch anything.

> **Common mistake**
>
> Testing layout only on a fast connection with everything cached. On your machine every
> image is already in the cache, so it has its dimensions instantly, so nothing shifts, so
> you conclude the page is stable — and you have accidentally tested the one scenario your
> users never experience. Layout shift is a **first-visit, cold-cache, slow-network**
> phenomenon by construction. If you don't hard-reload with throttling on, you will not see
> the bug that is, right now, making people click the wrong button. Speed and cache don't
> prevent layout shift; they hide it from *you*, specifically.

**Quiz.** A menu animation stutters on phones. Inspecting shows it animates the `left` property. Why does changing it to `transform: translateX()` fix the stutter?

- [ ] transform is a newer property, so it's faster
- [x] Animating `left` changes the element's geometry, forcing a reflow (re-measuring the page) and a repaint on every single frame — 60 times a second. `transform` is composited: the GPU shifts an already-painted layer without recomputing layout at all.
- [ ] transform uses less memory
- [ ] The stutter is caused by the network, not the animation

*Layout is the expensive stage: changing a box's position or size can force the browser to re-measure that element, its siblings, and its ancestors. Doing that at 60fps is asking for a full geometry recalculation sixteen milliseconds apart, which a phone CPU cannot always finish in time — so frames drop and the eye reads it as stutter. `transform` and `opacity` skip layout and paint entirely; the compositor moves an existing texture. This is why 'animate transform, not left' is one of the few pieces of performance advice that is nearly always correct.*

- **Repaint vs reflow vs composite** — Repaint = redraw pixels (cheap). Reflow = recompute geometry, then repaint (expensive, can cascade across the page). Composite = GPU shifts an existing layer (nearly free).
- **What triggers reflow** — width, height, margin, padding, font-size, adding/removing nodes, reading geometry (offsetHeight) — anything that changes or queries a box.
- **Animate these two** — `transform` and `opacity`. They're composited and skip layout entirely. Animating `left`/`top`/`width` reflows every frame.
- **Layout shift's #1 cause** — Images without width/height attributes. The browser reserves no space, lays out, then re-lays-out when the image arrives. Two attributes fix it.
- **Why you never see layout shift** — It's a first-visit, cold-cache, slow-network phenomenon. Your warm cache and fast laptop hide it from you specifically.
- **The two-minute layout audit** — Throttle to Slow 3G, hard reload, hands off, and watch what moves. Then narrow the window. More bugs than a week of happy-path clicking.

### Challenge

Pick a news site — they're the worst offenders. Throttle to Slow 3G, turn on Rendering →
Layout Shift Regions, hard reload, and don't touch anything. Count how many times the
content jumps and time how long until it stops. Then find one image in the Elements panel
without `width` and `height` attributes. You have just done a Core Web Vitals audit with
no tools beyond the browser, and you can name the exact element responsible.

### Ask the community

> Rendering question: [what jumps / stutters], visible when [throttled to X / on device Y]. Performance recording shows [purple Layout bars / long tasks] during [scroll / load / animation]. The animated or shifting element is [selector], and it changes [property]. Images involved have width/height: [yes/no].

The 'which property changes' line answers it outright — `left` and `width` reflow,
`transform` and `opacity` don't. And 'images have width/height: no' is a complete
diagnosis of a layout shift on its own. You're not asking what's wrong so much as
confirming what you already found.

- [web.dev — layout thrashing and how to avoid it](https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing)
- [CSS Triggers — which property causes layout, paint, or composite](https://csstriggers.com/)
- [Reflow, repaint and the compositor](https://www.youtube.com/watch?v=ZTnIxIA5KGw)

🎬 [Reflow and repaint, visually](https://www.youtube.com/watch?v=ZTnIxIA5KGw) (9 min)

- Repaint redraws pixels (cheap). Reflow recomputes geometry and can cascade through the page (expensive). Composite shifts a finished layer on the GPU (nearly free).
- Animate `transform` and `opacity`; animating `left`, `top` or `width` forces a reflow on every frame and drops frames on real phones.
- The commonest layout shift is an image with no width/height: the browser reserves no space, then shoves the page down when it loads — often as a user reaches for a button.
- Layout shift only appears on a first visit, cold cache, slow network. Your fast, warm-cached laptop hides it from you specifically.
- Throttle, hard reload, hands off, and watch what moves. Then resize the window. Two minutes, no code, more bugs than a week of happy-path testing.


---
_Source: `packages/curriculum/content/notes/the-web-platform-for-testers/how-browsers-render/reflow-and-repaint.mdx`_
