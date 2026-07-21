---
title: "Why layouts break"
tags: ["web-platform", "css", "layout", "responsive", "track-a"]
updated: "2026-07-10"
---

# Why layouts break

*Layouts don't break because CSS is hard. They break because every layout is a private bet about the data, the screen, the font and the language — and users don't know they agreed to it.*

> Nobody ships a broken layout. They ship a layout that works for the data they had, on the
> screen they owned, in the language they wrote it in, with the font that loaded. Then a
> customer in Germany, whose surname is 22 letters, on a 320px phone, with the web font
> blocked by their corporate proxy, opens the page. **The layout didn't break. It met its
> first real user.** Every bug in this note is a bet somebody made without noticing they were
> betting.

> **In real life**
>
> A layout is a **suit tailored to a mannequin.** It fits perfectly, and the tailor is not
> lying when they say so. Then a person wears it — a person who breathes, has a wallet in one
> pocket, is having a slightly bloated Tuesday, and is three inches taller than the mannequin.
> The suit didn't change. The assumption did. QA is the job of finding the mannequin in the
> room and asking, politely, who exactly it was measured on.

## The five bets, and how to call each one

Every layout bug you will ever file is one of these. Learn them and you can find bugs on a
page you've never seen, in a language you don't read.

**1. The data bet.** "Names are short. Prices have two digits. There are three cards."
Reality: 41-character emails, `€1,234,567.89`, an empty list, a list of 900.

**2. The screen bet.** "Everyone's on a laptop." Reality: 320px phones still in use, 4K
monitors, browser zoom at 150% because the user can't read 12px type, a tablet held
sideways.

**3. The font bet.** "Our web font will load." Reality: it loads late, or is blocked, and
the fallback font is wider — so text that fit now wraps, and the button that hugged its
label now clips it.

**4. The language bet.** "The button says 'Save'." Reality: German `Speichern`, Finnish
`Tallenna`, and UI strings routinely grow 30% or more in translation. Arabic and Hebrew read
right-to-left, so the whole layout mirrors.

**5. The state bet.** "The user is logged in, verified, has a photo, has no notifications."
Reality: every combination of those, including the ones nobody drew.

![A browser rendering a page, showing layout of boxes](browser-render.png)
*Browser rendering — Wikimedia Commons, CC BY-SA. [Source](https://commons.wikimedia.org/wiki/File:Web_browser.png)*
- **The data bet — content sets the size** — Almost every box on a page sizes itself around its content. Change the content and you change the layout. Test with the longest plausible string, the empty list, and the list of 900 — not with `test@qa.com` and three rows.
- **The screen bet — drag, don't jump** — Testing only at 375/768/1024/1440 tests exactly the four widths the developer already checked. Bugs live between breakpoints and at 320px. Drag the viewport handle slowly and watch for the moment something stops fitting.
- **The font bet — FOUT and fallback metrics** — Before a web font loads, the browser paints a fallback with different metrics. Text reflows when the real font arrives — that's Cumulative Layout Shift. Simulate it: block the font file in the Network conditions panel and reload.
- **The language bet — 30% longer, or mirrored** — German and Finnish UI strings run substantially longer than English. Arabic and Hebrew flip the entire layout. A button sized to hug 'Save' has no room for 'Speichern'. Test with pseudo-localisation before you have translations.
- **The zoom bet — nobody tests this and everybody uses it** — Browser zoom at 150% is not the same as a smaller viewport: it changes CSS pixel size, so fixed-px layouts overflow while rem-based ones adapt. It's also an accessibility requirement — WCAG expects usability at 200% zoom.

**One card, five bets, five bugs — press Play**

1. **The mock: 'Jane Doe', 3 cards, 1440px, English, font loaded** — It's beautiful. It ships. Every screenshot in the ticket looks like this, because every screenshot was taken under exactly these conditions. Nobody involved was careless — they were consistent, which is worse.
2. **The data bet is called** — A user named Wolfeschlegelsteinhausenbergerdorff signs up. The name is an unbroken string, so the flex item's `min-width: auto` refuses to shrink, and the card punches through the container. Fifteen seconds to reproduce in the Elements panel; four months in the backlog.
3. **The screen bet is called** — A 320px phone. The three-column grid was `repeat(3, 1fr)` — a hard-coded count, not a responsive rule. Three columns on a 320px screen is 106px each. The Buy button now reads 'Bu…' and nobody can complete a purchase.
4. **The font bet is called** — A corporate proxy blocks Google Fonts. The fallback is wider. The button was sized to hug the word 'Checkout' in the web font, so in the fallback the word clips. The page also shifts as the font swaps in — Cumulative Layout Shift, measurable and penalised.
5. **The language bet is called** — German. 'Save' becomes 'Speichern' — nearly twice the characters. The button had a fixed width because the mock said 4 characters. Now the label overflows its own button, and this happens on every button on the site simultaneously.
6. **The state bet is called** — A brand-new user: no avatar, no orders, no notifications. The page renders an empty grid with a 400px hole in it, because nobody drew the empty state. The layout is fine. It's just full of nothing, and it looks like a bug because it is one.

*Try it — call all five bets against one card*

```python
CARD_W, BTN_W = 280, 120

def render(name, label, viewport, font_factor=1.0, cols=3):
    col_w = (viewport - (cols-1)*24) // cols
    card = min(CARD_W, col_w)
    # a name with no spaces cannot wrap: its minimum width is its full length
    name_px = int(len(name) * 8 * font_factor)
    wrappable = " " in name
    name_min = 40 if wrappable else name_px
    label_px = int(len(label) * 9 * font_factor)
    bugs = []
    if name_min > card:            bugs.append(f"name overflows card ({name_min}px in {card}px)")
    if label_px > BTN_W:           bugs.append(f"button label clips ('{label}' needs {label_px}px, has {BTN_W}px)")
    if card < 140:                 bugs.append(f"card unusably narrow ({card}px)")
    return bugs or ["ok"]

cases = [
    ("the mock",          "Jane Doe",  "Save",      1440, 1.0, 3),
    ("data bet",          "Wolfeschlegelsteinhausen", "Save", 1440, 1.0, 3),
    ("screen bet",        "Jane Doe",  "Save",       320, 1.0, 3),
    ("font bet (fallback +12%)", "Jane Doe", "Checkout", 1440, 1.12, 3),
    ("language bet (de)", "Jane Doe",  "Speichern", 1440, 1.0, 3),
    ("all at once",       "Wolfeschlegelsteinhausen", "Speichern", 320, 1.12, 3),
]
for label, name, btn, vw, ff, cols in cases:
    print(f"{label:28} @{vw}px")
    for b in render(name, btn, vw, ff, cols):
        print(f"    - {b}")
print()
print("Not one of these is a CSS bug. Every one is an ASSUMPTION bug --")
print("a bet on the data, the screen, the font, or the language. The mock")
print("passed because the mock was the only case anyone ever rendered.")
```

## Hostile fixtures: the habit that finds these before users do

`test@qa.com`. `Jane Doe`. `$9.99`. Three cards. Your fixture data is *polite*, and polite
data proves nothing. Replace it, once, everywhere:

- The **longest plausible** name, email, product title, order id — and make one of them an unbroken string.
- **Zero** items. **One** item. **Nine hundred** items.
- A price with thousands separators and a currency symbol that isn't `$`.
- A user with no avatar, no verified badge, no orders.
- Every string wrapped in pseudo-localisation: `[Ŝàvé——————]` — same meaning, 40% longer, obviously fake.

> **Tip**
>
> Pseudo-localisation is the single highest-yield layout test that almost nobody runs. You
> don't need translators: programmatically pad every UI string by 40% and add accents.
> Anything that clips, wraps badly, or overflows is a bug that *will* appear the day you
> launch in German — except you've found it before you've paid for a translation, and while
> the fix is still one CSS property instead of a hundred tickets.

Cumulative Layout Shift (CLS)

### Your first time: Your mission: call all five bets on a real page

- [ ] The data bet — Inspect a name, price or title. Double-click the text in Elements and paste in 45 unbroken characters. Does it overflow? Fifteen seconds, one bug.
- [ ] The screen bet — Device toolbar → responsive → drag from 1440px down to 320px SLOWLY. Note the exact width where something first breaks. That number goes in your bug report.
- [ ] The font bet — Network → block request URL on the font file → reload. Does anything clip or shift? Watch the page jump when a font swaps in.
- [ ] The language bet — Edit three button labels in Elements to be 40% longer with accents: `Ŝàvé—————`. Any button with a fixed width will fail immediately.
- [ ] The state bet — Delete the avatar `<img>` in Elements. Delete all but one card. Delete all cards. Does the page still make sense, or is there a hole where a design should be?

Five bets, five minutes, no code, no test framework, no backend. This is what an experienced tester does in the first five minutes on any new page.

- **It only breaks for one customer and we can't reproduce it.**
  You haven't reproduced their *conditions*, which are data, viewport, zoom, font, language and state. Get the six from the reporter — a screenshot usually reveals four of them. Then reproduce the data condition by editing the text in Elements rather than seeding a database. 'Cannot reproduce' almost always means 'our fixtures are politer than our users.'
- **There's a horizontal scrollbar on mobile and nothing looks too wide.**
  Something overflows the viewport, and it's often invisible. Run `[...document.querySelectorAll('*')].filter(e => e.getBoundingClientRect().right > document.documentElement.clientWidth)` and inspect what comes back. Usual suspects: a `nowrap` flex row, a fixed-width grid, an image without `max-width: 100%`, or an absolutely-positioned decoration nobody remembers adding.
- **The page visibly jumps around while it loads.**
  Layout shift. Images without `width`/`height` attributes reserve no space, so everything below them moves when they arrive. Web fonts swap and re-flow text. Ads and embeds inject themselves into the flow. Throttle the network to Slow 3G and watch it happen in slow motion — then check Lighthouse's CLS score, which puts a number on it that a product manager will care about.
- **It works at 100% zoom and breaks at 150%.**
  Browser zoom scales the CSS pixel, so a layout built from fixed `px` values overflows while a `rem`-based one adapts. This is not an edge case: users who zoom are usually users who need to. WCAG expects the page to remain usable at 200% zoom, so this is an accessibility failure with a standard behind it, not a cosmetic nitpick.
- **The empty state looks like a rendering bug.**
  It probably is one — the bug being that no empty state was designed. A grid with zero items renders as a hole. A list with one item renders as a lonely card in a three-column layout. These are the most-skipped and most-reported states in existence, because every mock has exactly the tasteful three items the designer felt like drawing.

### Where to check

Five bets, five places to call them:

- **Elements → double-click the text** — the data bet, tested in fifteen seconds, no database.
- **Device toolbar → drag the handle slowly** — the screen bet. Presets test what the developer already tested.
- **Network → Block request URL on the font** — the font bet, plus the layout shift it causes.
- **Elements → pad a label with accents** — the language bet, before you own a single translation.
- **Elements → delete the avatar, the cards, the badge** — the state bet.
- **Console → `scrollWidth > clientWidth`** — a one-line detector for viewport overflow.
- **Lighthouse → CLS** — the number that makes layout shift someone else's problem too.

Tester's habit: **look for the mannequin.** Ask, of any layout: what did this assume about
the data, the screen, the font, the language, the state? Then arrange for one of those
assumptions to be false. You will find a bug on almost every page, on the first try, and
you'll do it before anyone has finished setting up a test environment.

### Worked example: the launch that broke in German, and the ten minutes that would have saved it

1. **The setup:** a product launches in Germany on a Tuesday. By Wednesday, support has 340 tickets. Buttons across the entire site have clipped labels; the checkout CTA reads `Zur Kass…`.
2. **Root cause, technically:** buttons were given fixed widths — `width: 120px` — sized to hug the English labels in the mock. German UI strings run substantially longer. Every button on the site failed at once, because every button shared one component.
3. **Root cause, honestly:** nobody ever rendered the site in a language other than English before the day it launched in one. The translations existed for weeks; nobody put them on a screen.
4. **The ten-minute test that would have caught it, months earlier:** in the Elements panel, edit three button labels to `Ŝàvé—————`, `Ĉĥéĉķôût—————`, `Wéîtér—————`. Two of the three clip immediately. That's the whole test. No translator, no German, no build.
5. **Why the fix was expensive after launch and cheap before:** before, it's `min-width` instead of `width` on one shared Button component, plus `white-space: nowrap` removed. After, it's the same one-line change plus 340 support tickets, an emergency deploy, a rollback plan, a postmortem, and a country's worth of first impressions.
6. **What the team changed afterwards:** a pseudo-localisation toggle in the dev build, on by default in staging. Every UI string padded 40% and accented. It's ugly, it's obviously fake, and it makes a whole class of bug impossible to ship without seeing it first.
7. **The uncomfortable part:** the QA team had tested the German site. They tested it *functionally* — every flow, every form, every payment path. All passed. They were reading the flows and never once looked at whether the words fitted inside the boxes. The bet nobody called was the one nobody had a checklist item for.
8. **Which is the actual lesson.** Test plans are made of the things somebody once thought to write down. The five bets aren't in your test plan. Put them there.

> **Common mistake**
>
> Signing off a layout because "it matches the design." The design is one render of one data
> set at one width in one language with one font in one state. It is the *mannequin*. Matching
> it is the floor, not the ceiling, and it's the only thing most sign-offs actually check. Your
> job is the other several thousand renders — the ones nobody drew, which is exactly why nobody
> looked at them. A layout that matches the mock and breaks for a German customer at 320px with
> a long surname is not "mostly right." It is a layout that has been tested exactly once.

**Quiz.** A layout is signed off against the design mock, passes every functional test in German, and then breaks on launch day with clipped button labels across the entire site. What failed?

- [ ] The German translations were wrong
- [ ] CSS is unreliable across languages
- [x] Nobody ever rendered the layout with longer strings. Functional tests check that flows work, not that words fit inside boxes. Fixed-width buttons sized to English labels clip the moment a language runs longer — and pseudo-localisation would have shown it months earlier, without a single translator.
- [ ] The QA team should have been fluent in German

*This is the trap: every individual step was done competently. The mock was matched. The flows were tested. The translations were correct. What nobody did was render a longer string and look at it — because 'do the words fit?' wasn't on anyone's checklist, and functional tests pass happily while text overflows its container. Fluency in German (option 4) would not have helped; the tester was reading flows, not layouts. Pseudo-localisation catches this with no translator, no build, and no language knowledge: pad every string 40%, add accents, and look.*

- **The five bets every layout makes** — Data (short names, 3 items), screen (a laptop), font (it loaded), language (English), state (logged in, has an avatar, has orders).
- **Hostile fixtures** — Longest plausible string (one unbroken), zero items, one item, 900 items, a non-$ currency, no avatar. Polite fixtures prove nothing.
- **Pseudo-localisation** — Pad every UI string ~40% and add accents: `[Ŝàvé——]`. Finds the entire class of text-overflow bugs before you own a translation.
- **Why breakpoint testing misses bugs** — 375/768/1024/1440 are the four widths the developer already checked. Drag the viewport slowly; bugs live between breakpoints and at 320px.
- **Cumulative Layout Shift** — Content moving after it first paints — images with no width/height, late web fonts, injected ads. Felt as a button moving out from under a finger.
- **Zoom is not a small viewport** — Zoom scales the CSS pixel. Fixed-px layouts overflow; rem-based ones adapt. WCAG expects usability at 200%.
- **'Cannot reproduce' usually means…** — You haven't reproduced their conditions: data, viewport, zoom, font, language, state. Reproduce the data condition by editing text in Elements.
- **Why the empty state looks like a bug** — Because it is one — nobody designed it. Every mock has exactly the three tasteful items the designer drew.

### Challenge

Pick any product page you use. In ten minutes, call all five bets: paste a 45-character
unbroken string into a name, drag the viewport to 320px, block the web font in the Network
panel, pad three button labels with accents, and delete the avatar. Write down each bug with
the exact condition that triggered it. Then check the site's public bug tracker or support
forum — you will usually find that at least one of your findings has been reported by a real
customer, badly, and closed as "cannot reproduce."

### Ask the community

> Layout bug: [element] breaks under condition [data / viewport px / zoom % / font blocked / language / state]. Exact width where it first breaks: [px]. Container Computed: display=[d], grid-template-columns=[g], flex-wrap=[w]. Item Computed: width=[w], min-width=[m]. `scrollWidth > clientWidth`: [true/false]. Overlay screenshot attached.

The exact breaking width and the triggering condition are what turn 'looks broken on mobile'
into a ticket someone can act on today. And `scrollWidth > clientWidth` settles the
horizontal-scrollbar argument before anyone opens their own browser and fails to see it.

- [web.dev — Cumulative Layout Shift, and what causes it](https://web.dev/articles/cls)
- [MDN — responsive design fundamentals](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [W3C — reflow: the page must work at 400% zoom / 320px](https://www.w3.org/WAI/WCAG21/Understanding/reflow.html)
- [Microsoft — pseudo-localisation, the highest-yield layout test nobody runs](https://learn.microsoft.com/en-us/globalization/localizability/pseudolocalization)

🎬 [Responsive layout bugs, and the conditions that cause them](https://www.youtube.com/watch?v=AQqFZ5t8uNc) (11 min)

- Layouts don't break; their assumptions get called. Every layout bets on the data, the screen, the font, the language and the state.
- Polite fixtures (`test@qa.com`, `Jane Doe`, three cards) prove nothing. Use hostile ones: longest plausible strings, zero items, 900 items, no avatar.
- Pseudo-localisation — pad every string 40% and add accents — finds the entire text-overflow class of bugs with no translator and no build.
- Testing at 375/768/1024/1440 tests the four widths the developer already checked. Drag the viewport slowly; bugs live between breakpoints and at 320px.
- 'Cannot reproduce' almost always means the reporter's conditions weren't reproduced. Most of them can be recreated in the Elements panel in under a minute.


---
_Source: `packages/curriculum/content/notes/the-web-platform-for-testers/css-essentials/why-layouts-break.mdx`_
