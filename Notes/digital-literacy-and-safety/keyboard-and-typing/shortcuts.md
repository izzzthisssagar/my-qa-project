---
title: "Shortcuts"
tags: ["digital-literacy", "keyboard", "productivity", "devtools", "track-a"]
updated: "2026-07-10"
---

# Shortcuts

*A shortcut isn't about saving three seconds. It's about not losing your train of thought — and about a handful of keys that turn a browser into a debugging instrument.*

> The argument against learning shortcuts is arithmetic: you save two seconds, a hundred times
> a day, which is three minutes. Three minutes! Hardly worth the trouble. **The arithmetic is
> right and the conclusion is wrong.** The cost of reaching for the mouse was never the two
> seconds. It's that you looked away from the thing you were thinking about, hunted for a menu,
> read four labels, and came back — and the thought you were holding is gone. Shortcuts don't
> buy time. They buy *continuity*, and continuity is the whole job.

> **In real life**
>
> Shortcuts are the difference between a **driver who looks at the gearstick** and one who
> doesn't. Both change gear. Both arrive. But one of them spent the corner looking at their
> hand instead of the road, and over ten thousand corners that is not a small difference —
> it's the difference between driving and operating a car. Nobody praises an experienced driver
> for knowing where third gear is. They just notice that they never look down.

## The twelve that matter, ranked by how often you'll use them

Not a reference list. The ones that pay for themselves in a week:

| Shortcut | Does | Why a tester lives here |
|---|---|---|
| `Cmd/Ctrl + Shift + C` | Inspect element (pointer mode) | Click any pixel → its markup. The single most-used key in QA. |
| `Cmd/Ctrl + Shift + J` (or `F12`) | Open DevTools console | Where errors confess |
| `Cmd/Ctrl + Shift + R` | **Hard** reload, bypassing cache | Half of all "it's still broken" is a cached file |
| `Cmd/Ctrl + F` | Find on page | Also accepts CSS selectors in the Elements panel |
| `Cmd/Ctrl + Shift + P` | DevTools command menu | Type "screenshot", "coverage", "disable JavaScript"… |
| `Cmd/Ctrl + L` | Focus the URL bar | Type a URL without leaving the keyboard |
| `Cmd/Ctrl + T` / `W` | New tab / close tab | |
| `Cmd/Ctrl + Shift + T` | **Reopen the tab you just closed** | Saves the evidence you just destroyed |
| `Cmd/Ctrl + Z` | Undo — *in the Elements panel too* | Yes: you can undo a DOM edit |
| `Alt/Option + Click` | Expand a whole DOM subtree at once | |
| `Cmd/Ctrl + K` | Clear the console | Start a clean reproduction |
| `Escape` | Toggle the DevTools drawer | Console on top of any panel |

`Cmd + Shift + P` deserves its own sentence. It is a search box over **every command
DevTools has**, including many with no menu item at all — full-page screenshot, disable
JavaScript, show coverage, emulate a slow network. Learn one shortcut and you have learned
all of them.

![A keyboard with shortcut keys highlighted](keyboard-shortcuts.jpg)
*Keyboard shortcuts — Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Keyboard-shortcuts-photoshop.jpg)*
- **The modifier keys are the grammar** — Ctrl (Cmd on Mac) = 'do the app thing'. Shift = 'do the bigger or opposite version'. Alt/Option = 'do the developer version'. Once you see the grammar, you can guess shortcuts you were never taught — and you'll be right surprisingly often.
- **Ctrl+Shift+R — the hard reload** — A normal reload happily serves you the cached JavaScript from twenty minutes ago. A hard reload bypasses the cache. An enormous share of 'the fix didn't work' reports are a developer and a tester looking at two different versions of the same file.
- **Ctrl+Shift+C — inspect by pointing** — Puts the cursor in element-picker mode: click any pixel on the page and DevTools jumps to its markup. This is how you answer 'what IS that thing?' in under a second, and it's the most-pressed key combination in professional QA.
- **Ctrl+Shift+P — the command menu** — A search box over every DevTools command, including ones with no menu entry. Type 'screenshot' for a full-page capture, 'JavaScript' to disable it, 'coverage' to find dead CSS. One shortcut that contains all the others.
- **Escape — the drawer, not just dismiss** — Inside DevTools, Escape opens a drawer with the console pinned beneath whatever panel you're in. Read a network response and its console errors at the same time, without switching tabs and losing your place.
- **Ctrl+Shift+T — undelete a tab** — Reopens the tab you just closed, with its history. You closed the tab holding the only reproduction of a bug you'd spent forty minutes finding. This key gives it back. Press it more than once to go further back.

**The same bug, two testers — press Play**

1. **The report: 'the price is wrong on the cart page'** — Both testers open the page. Both see £45.00 where £40.00 is expected. From here their paths diverge, and by the end one has a root cause and the other has a screenshot.
2. **Tester A reaches for the mouse** — Right-click → Inspect. Hunt for the Network tab. Reload with the button. Scroll the request list looking for the API call. Click it. Hunt for the Response sub-tab. Read. Four context switches, and each one is a chance to forget what they were checking.
3. **Tester B never leaves the keyboard** — Ctrl+Shift+C, click the price → markup. Ctrl+Shift+J → console, no errors. Ctrl+Shift+R → hard reload with the Network tab already recording. Ctrl+F in the request list, type 'cart'. Reads the response body.
4. **The server sent £40.00** — Both testers can now reach this fact. B reached it in about fifteen seconds and still holds the whole question in their head: server correct, screen wrong, therefore front-end bug. A got there too, having reconstructed the question twice on the way.
5. **B does the thing A won't have energy for** — Still in flow, B presses Ctrl+Shift+P → 'disable JavaScript' → reload. The price renders as £40.00. So the bug is in client-side code that mutates the price after render. That's not a bug report, that's a diagnosis — and it came from having attention left over.

*Try it — where your day actually goes*

```python
# Rough per-interaction cost. The seconds are illustrative; the RATIO is the point.
mouse = {"inspect element": 6, "open console": 5, "hard reload": 7,
         "find on page": 5, "clear console": 4, "reopen closed tab": 25}
keys  = {"inspect element": 1, "open console": 1, "hard reload": 1,
         "find on page": 1, "clear console": 1, "reopen closed tab": 1}
per_day = {"inspect element": 60, "open console": 30, "hard reload": 40,
           "find on page": 25, "clear console": 15, "reopen closed tab": 2}

t_mouse = sum(mouse[k]*n for k,n in per_day.items())
t_keys  = sum(keys[k]*n  for k,n in per_day.items())

print(f"{'action':20} {'x/day':>6} {'mouse':>8} {'keys':>7}")
print("-"*46)
for k,n in per_day.items():
    print(f"{k:20} {n:>6} {mouse[k]*n:>7}s {keys[k]*n:>6}s")
print("-"*46)
print(f"{'TOTAL':20} {'':>6} {t_mouse:>7}s {t_keys:>6}s")
print(f"\\nSaved: {(t_mouse-t_keys)/60:.0f} minutes a day. Underwhelming, isn't it?")
print()
# The part the stopwatch can't see:
switches = sum(per_day.values())
print(f"But you also avoided {switches} context switches.")
print("Each one: eyes leave the problem, hunt a menu, read labels, come back.")
print("The 2 seconds were never the cost. The DROPPED THOUGHT was the cost --")
print("and you cannot measure it, which is exactly why people dismiss it.")
```

## Shortcuts you should test, not just use

Here's the tester's inversion. Applications *define* shortcuts, and shortcuts are a feature —
so they are a surface with bugs on it, and almost nobody tests them.

- **Does the shortcut work when focus is inside a text input?** A single-key shortcut like `s` for "save" will fire while the user is typing the letter s into a search box. This bug ships constantly.
- **Does it collide with a browser or OS shortcut?** An app binding `Ctrl+W` will find that the browser closed the tab first. The browser always wins.
- **Is it discoverable?** A shortcut nobody knows about is a feature nobody has.
- **Does it work on a different layout?** A shortcut chosen for its position on QWERTY may be awkward or impossible on AZERTY.
- **Is there a way to see them all?** Almost every serious app binds `?` to a shortcut cheatsheet. Check whether yours does.

> **Tip**
>
> The fastest way to learn a new app's shortcuts is to press **`?`** on its main screen. It's an
> unwritten convention — GitHub, Gmail, Slack, Linear, Notion all do it — and it opens a
> cheatsheet. It's also the first thing you should test on any app that has shortcuts: if `?`
> does nothing, or if it fires while you're typing a question mark into a comment box, you've
> found a bug in the first ten seconds of the session.

keyboard shortcut collision

### Your first time: Your mission: retire the mouse for one hour

- [ ] Learn exactly three, today — `Cmd/Ctrl+Shift+C` (inspect), `Cmd/Ctrl+Shift+R` (hard reload), `Cmd/Ctrl+Shift+P` (command menu). Not twelve. Three. Twelve is how people learn zero.
- [ ] Put a sticky note on your monitor — Those three, written out. Remove it when you stop needing to look. This takes about four days and then it's permanent.
- [ ] Open the command menu and read — `Cmd/Ctrl+Shift+P`, then just scroll. You will find commands you didn't know existed: full-page screenshot, disable JavaScript, show coverage, emulate a slow network.
- [ ] Break a shortcut deliberately — Find an app with single-key shortcuts (GitHub, Gmail). Click into a comment box and type the shortcut letter. Does the shortcut fire while you're typing? That's a real bug in a real product.
- [ ] Press `?` on five different apps — GitHub, Gmail, Slack, YouTube, your own product. Four will show a cheatsheet. Note which one doesn't — and whether it should.

Three shortcuts, one hour, and you've also found a class of bug most testers never think to look for.

- **'I deployed the fix but it's still broken.'**
  Before anything else: `Cmd/Ctrl+Shift+R`. A normal reload will happily serve you the JavaScript and CSS it cached twenty minutes ago, so you and the developer are reading different versions of the same file and arguing about which of you is wrong. If a hard reload fixes it, the bug is real but it's a caching bug — check the Cache-Control headers, and check them in the Network panel, not in the config file.
- **The app's shortcut fires while I'm typing in a text box.**
  The handler doesn't check where focus is. A global single-key listener (`s` for save, `/` for search) must ignore the event when `document.activeElement` is an input, textarea, or contenteditable. Reproduce it in five seconds: click a comment box, type the letter. This ships in production constantly, in serious products.
- **The app's Ctrl+W shortcut closes my tab instead.**
  The browser claimed that combination first, and a web page cannot take it back. This is not a bug the developer can fix — it's a bug in the *choice* of shortcut. File it as such: 'Ctrl+W is reserved by the browser; pick another binding.' Same for Ctrl+T, Ctrl+N, and Cmd+Q.
- **DevTools is covering the page and I can't see what I'm testing.**
  `Cmd/Ctrl+Shift+P` → 'dock' → change the position, or press Escape to use the drawer, which slides the console beneath whichever panel you're in. You can also undock to a separate window entirely. Nobody teaches this and everyone suffers with a 300px page for years.
- **I closed the tab with my only reproduction in it.**
  `Cmd/Ctrl+Shift+T`. It comes back, with its history. Press it repeatedly to walk further back through closed tabs. This shortcut has saved more debugging sessions than any other, and most people find out about it after the session they needed it for.

### Where to check

Every shortcut here earns its place in an actual workflow:

- **`Cmd/Ctrl+Shift+C`** — the element picker. Click a pixel, get its markup.
- **`Cmd/Ctrl+Shift+R`** — hard reload. Rule out cache before you rule out anything else.
- **`Cmd/Ctrl+Shift+P`** — the command menu. Screenshot, disable JavaScript, coverage, throttling.
- **`Escape` inside DevTools** — the drawer: console beneath any panel, no tab switching.
- **`Cmd/Ctrl+F` in Elements** — accepts CSS selectors, highlights every match live. Develop a locator without leaving the panel.
- **`?` on any app** — the shortcut cheatsheet, by convention. Also a test.

Tester's habit: **when a fix "doesn't work", hard reload before you say so.** It costs one
keystroke, and it prevents the single most embarrassing message in software — reporting a bug
against a version of the file you never actually loaded.

### Worked example: the shortcut that deleted a customer's draft

1. **The report:** "I lost a long support reply I was writing. It just vanished." One customer, no repro, closed as user error. Twice.
2. **The third time**, someone notices the detail everyone had skimmed: the reply was about a **shipping** problem.
3. **The app's shortcuts:** `r` reply, `a` archive, `#` delete, `s` star. Single keys, no modifier — the Gmail convention, deliberate and normally good.
4. **The handler**, when someone finally reads it, listens on `document` for `keydown` and matches `event.key`. It does not ask where focus is.
5. **So it fires while you type.** Any letter you type anywhere on that page runs its shortcut *in addition* to entering the character — unless a text field swallows the event, which this one didn't, because the reply box was a `contenteditable` div rather than a `<textarea>` and the guard (such as it was) only checked for `textarea`.
6. **Reproduce it in eight seconds.** Open a reply. Type the word "shipping". The `#` isn't in it — but `s` is, and `a` is, and `r` is. The draft is starred, archived, and a reply-to-reply opens over the top of it. The customer typed a normal English word and their interface came apart.
7. **Why it was "unreproducible":** every tester who tried typed "test". No `s`, no `a`, no `r`. The polite fixture data again — `test` is a word chosen precisely because it is uninteresting, and it was uninteresting to the bug too.
8. **The fix is four lines:** ignore the event when `document.activeElement` is an `input`, a `textarea`, or has `contenteditable`. The `contenteditable` case is the one everybody forgets, because a rich-text editor doesn't look like a form field to the developer who wrote the guard.
9. **The test that should exist:** for every single-key shortcut, focus every kind of text input on the page and type that key. It's a loop. It takes a machine two seconds and it would have caught this before the first customer lost a word.

> **Common mistake**
>
> Treating shortcuts as a productivity hobby — something to get around to, like learning Vim,
> when there's time. Two of them are not productivity at all. `Cmd/Ctrl+Shift+R` is the
> difference between testing the fix and testing the cache, and it is the reason a significant
> fraction of "the fix didn't work" conversations happen. `Cmd/Ctrl+Shift+T` is the difference
> between keeping a reproduction and losing forty minutes of work. Neither saves you seconds.
> They both stop you from being *confidently wrong*, which is the expensive failure mode in
> this job.

**Quiz.** An app binds `s` to 'star this message'. A customer types a reply containing the word 'shipping' and their message gets starred, archived, and a new reply opens. What's the defect?

- [ ] The customer should not have used those letters
- [ ] Single-key shortcuts are always wrong and should be removed
- [x] The global keydown handler doesn't check where focus is. It must ignore the event when `document.activeElement` is an input, textarea, or contenteditable element — and contenteditable is the case developers forget, because a rich-text editor doesn't look like a form field.
- [ ] The browser should prevent this

*Single-key shortcuts are a good, deliberate convention — Gmail, GitHub and Linear all use them. The bug is the missing focus guard. A handler listening on `document` sees every keystroke on the page, including ones the user is typing into a text box, so it must ask `document.activeElement` where the keys are going before it acts. Note why testers missed it for months: everyone types 'test' into fixture fields, and 'test' contains none of the bound letters. The word 'shipping' contains three. Polite fixture data tests politely.*

- **The three to learn first** — `Cmd/Ctrl+Shift+C` inspect element, `Cmd/Ctrl+Shift+R` hard reload, `Cmd/Ctrl+Shift+P` command menu. Three, not twelve.
- **Why hard reload matters more than speed** — A normal reload serves cached JS/CSS. Half of 'the fix didn't work' is you and the developer reading different versions of the same file.
- **`Cmd/Ctrl+Shift+P`** — A search box over every DevTools command, including ones with no menu item: full-page screenshot, disable JavaScript, coverage, network throttling.
- **`Cmd/Ctrl+Shift+T`** — Reopens the tab you just closed, with history. Press repeatedly to go further back. Restores the reproduction you just destroyed.
- **The single-key shortcut bug** — A global keydown handler that doesn't check `document.activeElement` fires while the user types. The forgotten case is `contenteditable`, not `textarea`.
- **Shortcuts a web app can never claim** — Ctrl+W, Ctrl+T, Ctrl+N, Cmd+Q — the browser and OS take them first. Filing this as 'fix the handler' is wrong; the binding choice is the bug.
- **`?`** — By convention, opens the shortcut cheatsheet (GitHub, Gmail, Slack, Linear). Also a test: does it fire while you're typing a question mark?
- **What shortcuts actually buy** — Not seconds. Continuity — you never look away from the problem, so you still hold the question when the answer arrives.

### Challenge

Pick any app with single-key shortcuts — GitHub and Gmail both qualify. Click into a comment
box and type a sentence containing the bound letters. Watch what happens. Then do the same in
its rich-text editor if it has one, because `contenteditable` is where the focus guard is
usually missing. Report anything you find. Then go and learn exactly three DevTools shortcuts
and refuse to use the mouse for them for one week.

### Ask the community

> Shortcut bug: pressing [key] while focus is in [input/textarea/contenteditable] fires [action] instead of typing the character. `document.activeElement` at the time: [paste]. Modifier required by the app: [none/Ctrl/...]. Reproduces in a plain `<textarea>`: [y/n]. In a `contenteditable`: [y/n].

Splitting `textarea` from `contenteditable` in the report is what makes it instantly fixable.
A guard that checks for form fields but not rich-text editors is the exact shape of this bug,
and naming which one fails tells the developer precisely which line is missing.

- [Chrome DevTools — the full keyboard shortcut reference](https://developer.chrome.com/docs/devtools/shortcuts)
- [Chrome DevTools — the command menu (Cmd/Ctrl+Shift+P)](https://developer.chrome.com/docs/devtools/command-menu)
- [MDN — document.activeElement, the focus guard every shortcut needs](https://developer.mozilla.org/en-US/docs/Web/API/Document/activeElement)

🎬 [Chrome DevTools shortcuts every tester should know](https://www.youtube.com/watch?v=x4q86IjJFag) (9 min)

- Shortcuts don't buy seconds, they buy continuity — you never look away, so you still hold the question when the answer arrives.
- Learn exactly three first: inspect element, hard reload, command menu. Twelve is how people learn zero.
- `Cmd/Ctrl+Shift+R` before you report that a fix didn't work. Otherwise you and the developer are reading different files.
- `Cmd/Ctrl+Shift+P` is a search box over every DevTools command, including ones with no menu item at all.
- Shortcuts are a feature, so they have bugs. The classic: a global single-key handler that fires while you're typing, because it never asked `document.activeElement` where the keys were going.


---
_Source: `packages/curriculum/content/notes/digital-literacy-and-safety/keyboard-and-typing/shortcuts.mdx`_
