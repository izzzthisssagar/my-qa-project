---
title: "IDs, classes & attributes"
tags: ["web-platform", "html", "automation", "locators", "track-a"]
updated: "2026-07-10"
---

# IDs, classes & attributes

*Attributes are the handles your tests grab. Pick the wrong handle and your suite breaks every time a designer changes a colour — pick the right one and it survives a full redesign.*

> A tester writes `page.locator('.btn.btn-primary.mt-4.rounded-lg')`. It works. Six weeks
> later a designer changes `mt-4` to `mt-6` — a four-pixel margin — and forty tests go red
> overnight. Nothing about the product broke. **The tests were pinned to how the button
> looked, and looks are the most volatile thing on any web page.** The button's *purpose*
> never changed. Neither did its `id`.

> **In real life**
>
> Attributes are the difference between finding your friend by **name badge** and finding
> them by **outfit**. The badge (`id`, `data-testid`) is issued once and doesn't change.
> The outfit (`class`) changes whenever they feel like it — and half the room is wearing
> the same jacket. A test that identifies people by jacket is not a test of who's in the
> room. It's a test of this season's fashion.

## The four kinds of attribute, ranked by how much you should trust them

| Attribute | What it's for | Trust as a locator |
|---|---|---|
| `id` | A unique name for one element on the page | High — if it's genuinely stable and not generated |
| `data-testid` | A hook that exists *only* for tests | Highest — nothing else can move it |
| `class` | Styling, and grouping many elements | Low — designers change these freely |
| `role`, `aria-label`, `name` | Meaning, for assistive tech | Highest, and audits accessibility for free |

- **`id` must be unique** on the page. Two elements with the same `id` is invalid HTML. The browser won't complain; `document.getElementById` just returns the first, and your test picks a different one than you meant.
- **`class` is many-to-many.** One element can have ten classes; one class can be on a hundred elements. That's the point — it's for styling groups.
- **`data-*`** is a free-for-all namespace. `data-testid`, `data-state`, `data-user-id`. The browser ignores them entirely; they exist for your code and your tests.

![HTML source showing elements with id, class and data attributes](html-source.png)
*Diagram: HTML source code example — Wikimedia Commons, Public domain. [Source](https://commons.wikimedia.org/wiki/File:HTML_source_code_example.svg)*
- **`id` — one per page, or the rules break** — Duplicated ids are invalid HTML that renders perfectly. `getElementById` silently returns the first match, `label for=` binds to the first, and your locator resolves to whichever the engine met first. Detect it: run a Set over all ids and compare lengths.
- **`class` — the volatile one** — `class="btn btn-primary mt-4"` is three independent groups. A designer changing `mt-4` to `mt-6` has changed nothing about behaviour and broken every locator that named it. This is why CSS-class locators rot.
- **`data-testid` — a handle nobody else touches** — The browser ignores `data-*` entirely. That's the feature: a designer restyling, a developer renaming classes, and a framework regenerating hashes all leave it untouched. It's a contract between the app and its tests, written down in the markup.
- **Generated class names are a trap** — `css-1x2y3z`, `sc-fzXfMB`, `_button_1a2b3` — emitted by CSS-in-JS and hashed from file contents. They change when unrelated code changes. A test pinned to one passes today and fails on a commit that touched nothing it tests.
- **`aria-label` and `role` do double duty** — Locating by role and accessible name finds the element the way a screen reader finds it. When that locator breaks, you haven't got a flaky test — you've got an accessibility regression, reported for free by your suite (Module 4, ch1).

**The same button, five locators, six weeks later — press Play**

1. **Week 2 — a designer bumps the margin** — `mt-4` becomes `mt-6`. Zero behaviour change. The `.mt-4` locator dies. Nobody can explain why the payment test failed, so someone reruns CI and it fails again, and now the team distrusts the suite.
2. **Week 4 — a redesign renames the classes** — `btn-primary` becomes `button--cta`. `.btn-primary` dies too. Still no behaviour change. Two locators down, and both failures said 'element not found' rather than 'the button was restyled'.
3. **Week 6 — only two survive** — `#checkout-submit` and `[data-testid=checkout-submit]` never wavered, because nothing a designer does touches them. The role locator broke once, meaningfully. The class locators broke twice, meaninglessly. That's the whole ranking, learned the expensive way.

*Try it — score your locators against six weeks of change*

```python
# A button, as it exists on day 1
button = {
    "id": "checkout-submit",
    "data-testid": "checkout-submit",
    "class": ["btn", "btn-primary", "mt-4"],
    "role": "button",
    "text": "Pay now",
}

# Changes that ship over six weeks. None of them change what the button DOES.
changes = [
    ("designer bumps margin",   lambda b: b["class"].__setitem__(2, "mt-6")),
    ("redesign renames classes",lambda b: b["class"].__setitem__(1, "button--cta")),
    ("copywriter edits label",  lambda b: b.__setitem__("text", "Complete purchase")),
]

locators = {
    ".mt-4":                         lambda b: "mt-4" in b["class"],
    ".btn-primary":                  lambda b: "btn-primary" in b["class"],
    "#checkout-submit":              lambda b: b["id"] == "checkout-submit",
    "[data-testid=checkout-submit]": lambda b: b["data-testid"] == "checkout-submit",
    "getByRole(button, 'Pay now')":  lambda b: b["role"] == "button" and b["text"] == "Pay now",
}

alive = {k: True for k in locators}
for label, apply in changes:
    apply(button)
    broke = [k for k, fn in locators.items() if alive[k] and not fn(button)]
    for k in broke: alive[k] = False
    print(f"{label:26} broke: {broke or 'nothing'}")

print()
for k, ok in alive.items():
    print(f"  {'SURVIVED' if ok else 'DEAD    '}  {k}")
print()
print("The role locator died for a REAL reason: the words the user reads changed.")
print("The class locators died for no reason at all. That is the difference between")
print("a test that tells you something and a test that tells you a designer exists.")
```

## So which locator do you actually use?

In order of preference:

1. **Role + accessible name** — `getByRole('button', { name: 'Pay now' })`. Finds it the way a user does, and audits accessibility every run (Module 4, ch1). Breaks when the visible label changes, which is a change worth noticing.
2. **`data-testid`** — when the role locator is ambiguous or the element genuinely has no accessible identity. It's a contract: the developer promises not to move it.
3. **`id`** — good, if it's hand-written. React and friends often generate ids like `:r3:` which change per render. Look before you trust.
4. **CSS classes** — last resort, and write a comment explaining why you had no choice.
5. **XPath through the DOM structure** — `/html/body/div[2]/div[3]/button` is a locator that breaks when someone adds a wrapper div. Never do this.

> **Tip**
>
> Before you write `[data-testid=…]`, try the role locator. Half the time it works, and it
> gives you an accessibility check for free. If the role locator *can't* find the element,
> you've just discovered that a screen-reader user can't find it either — which is a bug
> report, not an inconvenience. Only reach for `data-testid` once you're satisfied the
> element's accessible identity is correct and simply isn't unique enough to locate by.

data-testid

### Your first time: Your mission: grade the handles on a real page

- [ ] Count duplicate ids — Console: `const ids=[...document.querySelectorAll('[id]')].map(e=>e.id); ids.length - new Set(ids).size`. Anything above 0 is invalid HTML that renders fine and breaks locators.
- [ ] Look for generated classes — Console: `[...document.querySelectorAll('*')].flatMap(e=>[...e.classList]).filter(c=>/^(css|sc)-|_\\w+_/.test(c)).length`. If it's high, CSS-class locators on this site will rot.
- [ ] Find the test hooks — `document.querySelectorAll('[data-testid], [data-test], [data-cy]').length`. Zero means nobody planned for testability — worth raising before you write the suite, not after.
- [ ] Try a role locator on the main CTA — Console: `document.querySelector('button')` then read its `aria-label` and text. Could you find it by role and name alone? If not, why not?
- [ ] Pick the handle and justify it — Write down which locator you'd use for the primary action and one sentence on what would have to change for it to break. If the answer is 'a margin', pick another.

You've now audited a page for locator stability before writing a single test. This is the ten minutes that saves the forty red builds.

- **A test that passed yesterday fails today, and nobody changed the feature.**
  Read what the locator names. If it's a class, `git log` the stylesheet or component — a rename or a margin tweak almost certainly landed. The test isn't flaky; it was pinned to something with no reason to stay still. Rewrite it against role or `data-testid` instead of re-running CI and hoping.
- **`getElementById` returns the wrong element.**
  There are two elements with that id. Invalid HTML, renders perfectly, no warning anywhere. `getElementById` returns the first in document order, and so does `<label for>` — meaning a duplicated id also breaks form labelling. Check with the Set trick above; file it as a real bug.
- **A locator like `.css-1x2y3z` breaks on a commit that touched an unrelated file.**
  That's a CSS-in-JS generated class, hashed from content. It changes when the build changes, not when the component changes. It was never a locator; it was a hash of a hash. Nothing to fix in the test — the strategy is what's broken.
- **The element has no id, no data-testid, and getByRole can't find it.**
  This is a design smell, not a locator puzzle. No role means no accessible identity, so a screen-reader user cannot find it either. Don't reach for XPath — go ask for a `data-testid` and, more importantly, for a real element with a real role. Your inability to write a clean locator is the most concrete accessibility bug report you will ever file.

### Where to check

Locator archaeology lives entirely in Elements and the Console:

- **Elements → the element** — read every attribute. Which of them describe *what it is* versus *how it looks*?
- **Console → the duplicate-id one-liner** — invalid markup that never announces itself.
- **Console → `document.querySelectorAll('[data-testid]').length`** — does this codebase take testing seriously?
- **The Accessibility pane** — computed role and accessible name. This is what `getByRole` queries.
- **`git log` on the component** — when a locator breaks, the answer is in the diff, not in a rerun.

Tester's habit: **when a locator breaks, ask whether a user would have noticed.** If the
button moved four pixels and the test failed, the test was wrong. If the button's label
changed from "Pay now" to "Complete purchase" and the test failed, the test was right and
is now telling you something true.

### Worked example: forty red builds and a four-pixel margin

1. **Monday morning:** 40 of 260 e2e tests fail. Deploy is blocked. Everyone assumes the checkout service.
2. **Read one failure, not forty.** `TimeoutError: locator('.btn.btn-primary.mt-4') resolved to 0 elements`. Not a payment error. Not a 500. The element was never found.
3. **Open the app.** The checkout button is right there, working, clickable. So the feature is fine and the *test* is broken. That reframe takes ten seconds and saves an afternoon.
4. **Inspect it.** `class="btn btn-primary mt-6"`. One character.
5. **`git log -p` the component.** "chore: bump CTA spacing for the new hero." A designer, doing their job.
6. **Count the damage.** All 40 failures name a class. `grep -r "locator('\." e2e/` returns 112 more waiting to break the same way.
7. **The real fix isn't the 40.** Replacing `.mt-4` with `.mt-6` buys you until the next redesign. The fix is a rule: locators go role-first, `data-testid` second, and CSS classes require a comment justifying them. Then a codemod for the 112.
8. **The cost of not doing this:** the team learns that red CI means "rerun it," and the day a real payment bug turns the build red, nobody looks. That's the actual damage — the four pixels only cost an afternoon.

> **Common mistake**
>
> Copying the selector out of DevTools' "Copy → Copy selector" menu. It hands you something
> like `#root > div:nth-child(2) > div.sc-fzXfMB > button`, which encodes the entire
> ancestry of the element and its generated class names. It works this minute. It will break
> the first time anyone wraps that section in a div — a change that affects nothing, that no
> reviewer will question, and that no error message will connect to your test. That menu
> item is a trap wearing the costume of a convenience.

**Quiz.** Forty e2e tests fail after a commit that only changed `mt-4` to `mt-6` on a button. What is the correct conclusion?

- [ ] The tests are flaky and should be rerun
- [ ] The button is broken and the deploy should be blocked
- [x] The tests were pinned to a styling class, which has no reason to stay stable. The failures are real (the locator genuinely found nothing) but meaningless (nothing a user cares about changed). Move the locators to role or data-testid.
- [ ] The designer should not have changed the margin without telling QA

*The failure is real — the locator resolved to zero elements — but it carries no information about the product. Classes exist to be changed; that's their job. Option 1 is how teams train themselves to ignore red CI, which is the expensive part. Option 4 makes a designer ask permission to do their job, which never survives contact with reality. The only durable fix is locators pinned to what the element IS (role, name, data-testid) rather than how it looks.*

- **id vs class** — `id` is unique to one element; `class` groups many and is styling-owned. Duplicated ids are invalid HTML that renders fine and silently breaks getElementById and `<label for>`.
- **Why data-testid is stable** — The browser ignores `data-*` entirely, so no restyle, class rename, or CSS-in-JS hash can move it. It's a written contract between app and tests.
- **Locator preference order** — role + accessible name → data-testid → hand-written id → CSS class (with a comment) → never structural XPath.
- **Why role locators are best** — They find the element the way a user does, and every run doubles as an accessibility audit. When they break, something a user perceives actually changed.
- **css-1x2y3z / sc-fzXfMB** — Generated CSS-in-JS class names, hashed from content. They change on unrelated commits. Never a locator.
- **'Copy selector' in DevTools** — Emits a full ancestry chain with nth-child and generated classes. Breaks when anyone adds a wrapper div. A trap dressed as a convenience.
- **The test that broke: was it right?** — Ask whether a user would have noticed the change. Label changed → good failure. Margin changed → bad locator.

### Challenge

Open your own project's e2e suite (or any public one on GitHub) and grep for locators
that name a CSS class. For each one, look at the element and ask: what would have to
change for this to break, and would a user notice that change? Then rewrite three of them
against role and accessible name. If a role locator can't find the element, you've found
an accessibility bug — file it. That's two deliverables from one grep.

### Ask the community

> Locator question: `[paste locator]` resolves to 0 elements after commit [sha]. The element still renders and works. Its current attributes: [paste the opening tag]. Accessibility pane role=[r], name=[n]. What changed in the diff: [paste]

Including the element's current attributes and its computed role is what turns 'my test
is flaky' into 'my test was pinned to a class.' The answer is usually visible the moment
someone else sees the opening tag — and the fix is usually a role locator you could have
written on day one.

- [Playwright — locators, and why role comes first](https://playwright.dev/docs/locators#locate-by-test-id)
- [Testing Library — the query priority list (the canonical ranking)](https://testing-library.com/docs/queries/about/#priority)
- [MDN — using data attributes](https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes)

🎬 [Writing locators that survive a redesign](https://www.youtube.com/watch?v=uJyeSAOJs-U) (11 min)

- `id` is unique, `class` is a styling group, `data-*` is yours. Duplicated ids are invalid HTML the browser renders without complaint.
- Locator order: role + accessible name, then data-testid, then a hand-written id, then a CSS class with an apology. Never structural XPath.
- Role locators break only when something a user perceives changes — that's an honest failure. Class locators break when a designer breathes.
- Generated class names (`css-1x2y3z`) are hashes of file contents. They change on commits that touch nothing you test.
- If no role locator can find the element, a screen-reader user can't either. Your locator problem is an accessibility bug report.


---
_Source: `packages/curriculum/content/notes/the-web-platform-for-testers/html-essentials/ids-classes-and-attributes.mdx`_
