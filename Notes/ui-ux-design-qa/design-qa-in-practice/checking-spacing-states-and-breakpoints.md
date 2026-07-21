---
title: "Checking spacing, states & breakpoints"
tags: ["ui-ux-design-qa", "design-qa-in-practice", "track-c"]
updated: "2026-07-17"
---

# Checking spacing, states & breakpoints

*The three-part pass a design-QA tester runs on a real build: measure spacing at its actual on-screen values, deliberately trigger every interactive state since none render by default, and resize through every documented breakpoint plus the undesigned widths in between.*

> Load a page once, glance at it, and you've checked exactly one state at exactly one width: default,
> whatever the browser happened to be sized to. Nothing about hover, focus, disabled, or how the layout
> holds up at 600px instead of 1440px is visible from that single glance - and that's precisely the
> territory where design bugs live undetected the longest, because they only show up when someone
> deliberately goes looking for them.

> **In real life**
>
> A set of matryoshka dolls is the same design rendered at six different sizes, nested inside each
> other - open the biggest one and there's a smaller, complete version underneath, then a smaller one
> still. Nobody assumes checking only the largest and smallest dolls tells you what the middle four
> look like; each one has to be opened and inspected on its own. A responsive component works the same
> way: passing at your two habitual breakpoints says nothing about the sizes nested in between that
> nobody happened to check.

**Checking spacing, states & breakpoints**: Checking spacing, states & breakpoints is the disciplined, three-part pass a design-QA tester runs on a REAL build (not the design file) before considering a component checked. Spacing means measuring gaps, padding, and margins at their actual on-screen values - not assuming visual similarity means a numeric match. States means deliberately triggering every interactive state a component can have (hover, focus, active, disabled, error, loading, empty), since none of them render by simply loading the page. Breakpoints means resizing the viewport through every documented breakpoint - and the undesigned widths between them - not just the two or three sizes a tester happens to habitually check.

## Spacing: measure it, don't eyeball it

- Pull the exact spacing values from the spec first (see
  [[ui-ux-design-qa/design-qa-in-practice/reading-a-figma-spec]]), then measure the live build's real
  on-screen gaps against them - "looks about the same" and "measures the same" are different claims.
- Check spacing at the DEFAULT state and breakpoint first, as a baseline, before checking whether it
  holds up once states and sizes start changing.
- Spacing is frequently NOT constant across breakpoints on purpose - tighter mobile padding is common
  and correct. Confirm the spec has a per-breakpoint value before assuming a difference is a bug.

## States: nothing renders by default except default

- A component has as many states as its spec defines - typically default, hover, focus, active,
  disabled, and often error, loading, and empty. Loading the page shows exactly one of them.
- Each state has to be deliberately TRIGGERED, not assumed: hover the element, tab to it for focus,
  click-and-hold for active, check what a disabled prop actually renders, submit invalid data for
  error.
- Keyboard focus specifically needs a keyboard pass. Clicking with a mouse does not reliably trigger
  the same `:focus-visible` state most browsers show on keyboard navigation.

## Breakpoints: every documented one, not just your two habitual sizes

- Resize to the EXACT documented breakpoint widths, not just until the layout "looks like it
  changed" - dragging finds where something accidentally breaks, not whether it matches spec.
- Watch for the "squishy middle" - a width between two named breakpoints where nothing was
  explicitly designed, and layout, spacing, or states can regress silently.
- Re-check spacing and states AGAIN at each breakpoint. A focus ring that's fine on desktop and a
  spacing value that's correct on desktop can both independently regress on mobile.

> **Tip**
>
> Use DevTools' responsive mode with the exact documented breakpoint widths typed in as fixed values,
> rather than freehand dragging. Dragging is good for exploring where something happens to break;
> typing in the documented width is what actually confirms the build matches spec AT that breakpoint.

> **Common mistake**
>
> Checking states only with mouse hover and skipping keyboard focus entirely. An interactive element
> that's never been tabbed to can look completely "done" and still have no visible focus indicator at
> all - a WCAG 2.4.7 (Focus Visible) problem that's fully invisible to a mouse-only pass, however
> thorough that pass otherwise is.

![A row of six Russian matryoshka nesting dolls of decreasing size, lined up left to right, each hand-painted with a similar folk-costume design](checking-spacing-states-and-breakpoints.jpg)
*Early matryoshka — All-Russian Decorative Art Museum, Wikimedia Commons, CC0. [Source](https://commons.wikimedia.org/wiki/File:Early_matryoshka_-_All-Russian_Decorative_Art_Museum.jpg)*
- **The largest doll — the biggest breakpoint (desktop)** — The size most designs get checked at first, since it's usually the frame everyone builds and reviews from - complete and correct on its own, but not proof of anything about the smaller sizes nested inside.
- **A middle-sized doll — a mid-range breakpoint, easy to skip** — The one most likely to get skipped when a tester checks only 'mobile and desktop' - exactly the kind of in-between size (tablet, or a width between two documented breakpoints) where layout regressions hide undetected.
- **The smallest doll — the tightest breakpoint (mobile)** — Where spacing has the least room to be wrong and every state (focus rings, error text, disabled styling) has the least space to render cleanly - the size where issues are most visible once someone actually checks it.

**Running a full spacing / states / breakpoints pass**

1. **Get the spec's exact spacing values and full breakpoint list** — Including any per-breakpoint spacing differences that are intentional, not bugs.
2. **Measure real on-screen spacing at the default state and breakpoint** — A clean baseline before anything else changes.
3. **Deliberately trigger every state** — Hover, keyboard focus, active, disabled, error, loading, empty - each one, on purpose.
4. **Resize to every documented breakpoint, plus the squishy middle** — Not just the two or three sizes a tester habitually checks.
5. **Re-check spacing and states again at each breakpoint** — Either can regress independently of the other, and independently of desktop passing.

Checking whether the measured column count matches the spec at every documented breakpoint is a
simple lookup-and-compare - and it catches exactly the kind of single missed breakpoint that's easy
to overlook when a layout "looks responsive" at a glance:

*Run it - checking measured column count against spec at each breakpoint (Python)*

```python
breakpoints = [
    ("mobile", 375, 1),
    ("tablet", 768, 2),
    ("desktop", 1280, 3),
    ("wide", 1440, 4),
]

# Simulated measured column counts at each breakpoint width (what a real
# resize-and-count check would produce)
measured_columns = {
    "mobile": 1,
    "tablet": 2,
    "desktop": 2,
    "wide": 4,
}

print("Checking measured column count against spec at each breakpoint:")
print()
mismatches = []
for name, width, expected in breakpoints:
    actual = measured_columns[name]
    verdict = "OK" if actual == expected else "MISMATCH"
    print(f"  {name:<8} {width:>5}px   expected={expected}  measured={actual}   {verdict}")
    if actual != expected:
        mismatches.append((name, width, expected, actual))

print()
print(f"{len(mismatches)} breakpoint(s) mismatched:")
for name, width, expected, actual in mismatches:
    print(f"  - {name} ({width}px): expected {expected} columns, measured {actual}")
print()
print("mobile, tablet and wide all match spec exactly. desktop is the one that")
print("didn't get its column count bumped when the breakpoint was implemented -")
print("the layout still LOOKS fine at 1280px, it's just one column short of spec,")
print("which is exactly the kind of gap that only shows up by actually resizing")
print("to each breakpoint and counting, not by eyeballing a couple of familiar sizes.")

# Checking measured column count against spec at each breakpoint:
#
#   mobile     375px   expected=1  measured=1   OK
#   tablet     768px   expected=2  measured=2   OK
#   desktop   1280px   expected=3  measured=2   MISMATCH
#   wide      1440px   expected=4  measured=4   OK
#
# 1 breakpoint(s) mismatched:
#   - desktop (1280px): expected 3 columns, measured 2
#
# mobile, tablet and wide all match spec exactly. desktop is the one that
# didn't get its column count bumped when the breakpoint was implemented -
# the layout still LOOKS fine at 1280px, it's just one column short of spec,
# which is exactly the kind of gap that only shows up by actually resizing
# to each breakpoint and counting, not by eyeballing a couple of familiar sizes.
```

The same "check every required item, don't assume" discipline applies to states - comparing what's
required against what's actually implemented is a simple completeness check:

*Run it - checking which required interactive states are actually implemented (Java)*

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> requiredStates = Arrays.asList("default", "hover", "focus", "active", "disabled", "error");
        List<String> implementedStates = Arrays.asList("default", "hover", "active", "disabled");

        System.out.println("Required interactive states: " + requiredStates);
        System.out.println("Implemented in the build:    " + implementedStates);
        System.out.println();

        List<String> missing = new ArrayList<>();
        for (String state : requiredStates) {
            boolean present = implementedStates.contains(state);
            System.out.printf("  %-10s %s%n", state, present ? "present" : "MISSING");
            if (!present) missing.add(state);
        }

        System.out.println();
        System.out.println(missing.size() + " of " + requiredStates.size() + " required states missing: " + missing);
        System.out.println();
        if (missing.contains("focus")) {
            System.out.println("Missing focus is the one worth escalating fastest - no visible focus");
            System.out.println("ring is a keyboard-navigation and WCAG 2.4.7 problem, not just a");
            System.out.println("cosmetic gap. error is the second-most likely to actually get hit");
            System.out.println("by a real user and should not ship without a defined state either.");
        }
    }
}

/* Required interactive states: [default, hover, focus, active, disabled, error]
   Implemented in the build:    [default, hover, active, disabled]

     default    present
     hover      present
     focus      MISSING
     active     present
     disabled   present
     error      MISSING

   2 of 6 required states missing: [focus, error]

   Missing focus is the one worth escalating fastest - no visible focus
   ring is a keyboard-navigation and WCAG 2.4.7 problem, not just a
   cosmetic gap. error is the second-most likely to actually get hit
   by a real user and should not ship without a defined state either. */
```

### Your first time: Your mission: run a full pass on one real component

- [ ] Pick one interactive component with a known spec (a button, card, or dropdown) — Something with more than one documented state is ideal.
- [ ] Measure its default-state spacing precisely against spec — A clean baseline before anything else changes.
- [ ] Trigger every state it supports — Hover, keyboard focus (Tab), active/pressed, disabled, and error if applicable - note or screenshot each one.
- [ ] Resize the viewport through every documented breakpoint — Don't stop at two familiar sizes - check every width the spec actually lists.
- [ ] Re-check spacing and states at each breakpoint — Either can regress independently, and a desktop pass tells you nothing about mobile.

You've practiced the full three-part pass - not a glance at the default state on one familiar screen
size, but a deliberate check of every state at every documented width.

- **A component looks identical at the two breakpoints you checked, so you assume every size in between is also fine.**
  That's the 'squishy middle' - widths between documented breakpoints are exactly where nothing was explicitly designed. Check at least one width between each pair of documented breakpoints, not just the documented values themselves.
- **You can't find a focus state no matter how much you click around the element.**
  Focus is triggered by keyboard navigation (Tab), not a mouse click, in most browsers by default. Clicking doesn't reliably show `:focus-visible` - tab to the element instead before concluding a focus state is missing.
- **A spacing check passes cleanly on desktop but the same component looks different at mobile.**
  Spacing values are frequently NOT constant across breakpoints on purpose - tighter mobile padding is common and correct. Confirm the spec has a per-breakpoint spacing value before flagging the difference as a bug; the actual bug might be checking against the wrong number.

### Where to check

- **[[ui-ux-design-qa/design-qa-in-practice/reading-a-figma-spec]]** — get the exact spacing value AND the full breakpoint list before starting; per-breakpoint values often differ intentionally.
- **[[testers-toolbox/link-page-ui-checks/window-resizer-responsive-checks]]** — for jumping to exact documented breakpoint widths rather than dragging until something looks off.
- **Browser DevTools' keyboard/accessibility tab-order check** — the fastest way to actually trigger every focus state in sequence.
- **[[ui-ux-design-qa/design-qa-in-practice/pixel-perfect-vs-pragmatic]]** — once you've found a real spacing delta at a specific breakpoint, this is how to decide if it's worth filing.

### Worked example: one component, two very different findings

1. A tester checks an "Add to cart" button: spec says 12px/24px (vertical/horizontal) padding, with
   default, hover, focus, and disabled states documented.
2. Default state at desktop (1440px) measures exactly to spec - clean baseline confirmed.
3. Tabbing to the button with the keyboard: no visible focus ring at all, not just a wrong color -
   completely absent.
4. Resizing to the documented tablet breakpoint (768px): the button renders correctly, and the
   missing focus state is confirmed absent there too - a consistent bug, not resolution-specific.
5. Resizing to 600px - a squishy-middle width between the documented 375px and 768px breakpoints -
   the button's horizontal padding collapses to 8px, well outside tolerance and not a documented
   per-breakpoint value anywhere in the spec.
6. Two separate findings filed: "Add to cart button has no visible `:focus` state at any breakpoint
   (WCAG 2.4.7)" and "Add to cart button horizontal padding drops to 8px (spec: 24px) at a 600px
   viewport width, between the documented 375px and 768px breakpoints." Two different categories of
   finding - a missing state and an undocumented-width spacing regression - both traced to exact
   widths and states rather than "the button seems a bit off sometimes."

**Quiz.** A tester checks a component at the two documented breakpoints listed in the spec (375px and 1280px) and finds no issues at either. They conclude the component is fully responsive. What did they most likely miss?

- [ ] Nothing - checking both documented breakpoints and finding no issues is sufficient to conclude the component is fully responsive
- [x] The 'squishy middle' - viewport widths BETWEEN documented breakpoints are exactly where nothing was explicitly designed, and a component passing at both named breakpoints can still break at an undesigned width in between
- [ ] They should have used PerfectPixel instead of resizing the browser, since resizing cannot reveal breakpoint issues
- [ ] Breakpoints only ever affect font size, never spacing or layout, so checking anything besides text at each breakpoint was unnecessary

*This note's core point about breakpoints is that passing at the documented widths says nothing about the undesigned widths in between - the 'squishy middle.' A responsive check that stops at the named breakpoints, exactly like checking only the largest and smallest matryoshka doll and assuming the middle ones must be fine, misses the sizes where nothing was explicitly designed and layout is most likely to regress silently. [[testers-toolbox/link-page-ui-checks/window-resizer-responsive-checks]] covers the tooling for jumping to and between exact widths efficiently. Option one is the exact mistake this note warns against. Option three misrepresents PerfectPixel, which overlays a design comp for visual comparison and has nothing to do with revealing breakpoint gaps. Option four is factually wrong - breakpoints commonly change layout, column count, and spacing, not just font size, as this note's own Python playground demonstrates with column-count drift.*

- **The three-part pass this note covers** — Spacing (measure real on-screen values), states (deliberately trigger every interactive state), and breakpoints (resize through every documented width, not just two habitual sizes).
- **Why states don't render by default** — Loading a page only shows the DEFAULT state - hover, focus, active, disabled, error, loading, and empty all have to be deliberately triggered, none can be assumed correct from a static screenshot.
- **How to reliably trigger a focus state** — Tab to the element with the keyboard, not click it with a mouse - most browsers don't show `:focus-visible` reliably on mouse click, only on keyboard navigation.
- **What the 'squishy middle' is** — A viewport width BETWEEN two documented breakpoints, where nothing was explicitly designed - a component can pass at both named breakpoints and still break at an undesigned width in between.
- **Why a spacing difference between breakpoints isn't automatically a bug** — Spacing is frequently NOT constant across breakpoints on purpose (tighter mobile padding is common and correct) - confirm the spec has a per-breakpoint value before flagging a difference as a regression.

### Challenge

Pick one interactive component in BuggyShop. Check its spacing at the default state and breakpoint
against spec, trigger every state via keyboard AND mouse, then resize through every documented
breakpoint plus one width in the squishy middle between two of them. File any real finding using an
exact width, state, and measured value.

### Ask the community

> I checked `[component]` at `[breakpoints checked]` and found `[what you found]` in the `[state]` state. Is this within the documented breakpoint list, or is it a squishy-middle case I should widen my check to cover?

The most useful replies will ask for the exact viewport width and state before answering - a finding
at an undocumented in-between width needs a different conversation with the designer than one at a
breakpoint that's explicitly in the spec.

- [MDN — Using Media Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries)
- [MDN — :focus-visible](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible)
- [Tisfoulla Academy — Hover, Focus, Active, Disabled and States Variants](https://www.youtube.com/watch?v=lVPc4bH-dxY)

🎬 [Jesse Showalter — Responsive Web Design Has Never Been This Easy (Figma Breakpoints)](https://www.youtube.com/watch?v=gsVwThzYwv8) (4 min)

- Checking a component means three separate passes: spacing (measured, not eyeballed), states (deliberately triggered), and breakpoints (every documented width, not just two habitual ones).
- No interactive state besides default renders just from loading a page - hover, focus, active, disabled, error, loading, and empty all have to be triggered on purpose.
- Focus states need a keyboard pass specifically - mouse clicks don't reliably trigger the same :focus-visible state as Tab navigation.
- The 'squishy middle' between documented breakpoints is undesigned territory - passing at both named breakpoints doesn't guarantee anything about the widths in between.
- A spacing difference between breakpoints isn't automatically a bug - confirm the spec has a per-breakpoint value before flagging it as a regression.


## Related notes

- [[Notes/ui-ux-design-qa/design-qa-in-practice/reading-a-figma-spec|Reading a Figma spec]]
- [[Notes/ui-ux-design-qa/design-qa-in-practice/pixel-perfect-vs-pragmatic|Pixel-perfect vs pragmatic]]
- [[Notes/ui-ux-design-qa/design-qa-in-practice/design-bugs-devs-respect|Design bugs devs respect]]
- [[Notes/testers-toolbox/link-page-ui-checks/window-resizer-responsive-checks|Window Resizer & responsive checks]]


---
_Source: `packages/curriculum/content/notes/ui-ux-design-qa/design-qa-in-practice/checking-spacing-states-and-breakpoints.mdx`_
