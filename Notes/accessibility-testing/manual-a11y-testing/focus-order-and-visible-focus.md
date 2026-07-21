---
title: "Focus order & visible focus"
tags: ["accessibility-testing", "manual-a11y-testing", "track-c"]
updated: "2026-07-20"
---

# Focus order & visible focus

*Two separate checks: does Tab move through elements in the same order a sighted reader would follow (focus order), and is it actually visible where focus currently sits (visible focus) - both must hold.*

> A control can be perfectly reachable by Tab and still fail this pass twice over: once if Tab arrives in
> an order that makes no visual sense, and again if, once it arrives, nobody watching the screen can tell
> where focus actually went. Reachable is necessary. It is not the same as ordered, and it is not the
> same as visible.

> **In real life**
>
> A bakery counter's "now serving" display shows whichever numbered ticket the register has marked
> next - but that number only means anything if the physical line of waiting customers is actually
> standing in the same order the tickets were handed out in. Hand out ticket 42 to someone who then
> wanders to the back of a completely differently-ordered line, and the number on the board stops
> matching who is genuinely next for anyone watching the room. And the internal system marking a ticket
> "now serving" does nothing on its own - the number has to actually light up on a display people can
> see, not just get logged quietly in the till. One problem is order; the other is visibility. A counter
> can fail at either independently, and both have to hold for the system to actually work.

**Focus order and visible focus**: Focus order is whether the sequence Tab visits elements in matches the sequence a sighted reader would naturally follow through the page. Visible focus is whether, once an element receives focus, there is an actual visible indicator - typically an outline or highlight - showing where it currently sits. An element can be focusable (focus is present) without a visible indicator (focus is not visible), and both failures are independent of each other.

## Present is not the same as visible

An element receiving focus - present, in the DOM-and-accessibility-tree sense - is a completely separate
fact from whether a sighted keyboard user can actually see it happened. A very common, very quiet bug:
a global CSS reset includes `outline: none` to strip the default browser focus ring for visual polish,
with no replacement style added anywhere. Every single control on the page is still perfectly focusable
and still perfectly operable with Enter or Space - but a sighted keyboard user has absolutely no visual
signal for where they currently are on the page. Focus is present. Focus is not visible. Both statements
are true at once, and only one of them is a passing result.

## Order is a separate question from visibility

Focus order is about sequence, not appearance: does Tab move left-to-right, top-to-bottom in roughly
the way a sighted reader's eye would naturally travel, or does a CSS layout technique visually
reposition an element far from where it sits in the underlying markup, so Tab jumps somewhere that
looks completely unrelated to where focus just was. This is exactly what happens when visual and DOM
order quietly diverge - CSS `order`, `float`, or absolute positioning can rearrange what a page looks
like without touching the markup order Tab actually follows underneath.

> **Tip**
>
> Test visible focus and focus order as two separate passes with two separate checklists. Confirming
> "Tab reaches everything in a sensible order" tells you nothing about whether any of those stops are
> actually visible, and confirming "I can see a focus ring" tells you nothing about whether the order
> those rings appear in makes sense.

> **Common mistake**
>
> Removing a default focus outline for aesthetic reasons without adding any replacement indicator at all.
> This is one of the single most common real-world violations of the Focus Visible requirement, and it
> usually starts as an innocent global style reset nobody connected back to keyboard accessibility.

![A large digital advertisement screen mounted above a train station departure board listing departures in ordered columns, under a glass station roof, with travelers standing below](focus-order-and-visible-focus.jpg)
*Train departure board in the concourse of Brighton railway station — Wikimedia Commons, CC0. [Source](https://commons.wikimedia.org/wiki/File:Train_departure_board_in_the_concourse_of_Brighton_railway_station_2026-05-16.jpg)*
- **The bright advertisement screen** — Visually dominant - the first thing an eye is drawn to - but not part of the functional sequence a traveler actually needs, the same way visual prominence has nothing to do with true focus order.
- **The leftmost information column** — A fixed starting point in a documented left-to-right order, the same way a page's markup order should start somewhere a reader can predict.
- **Later columns, read in the same fixed direction** — The order keeps going predictably rightward - exactly what a mismatched CSS layout can quietly break for Tab order.
- **The physical platform the order points to** — An order only matters if it correctly leads somewhere real and operable - the same standard a focus order has to meet.

**Checking order and visibility as two passes**

1. **Tab through the whole page once, watching only sequence** — Does the order roughly match how a sighted reader's eye would travel through the same content?
2. **Tab through again, watching only the indicator** — At every single stop, is there something visibly different about that element right now?
3. **Compare visual layout to markup order directly** — CSS positioning can make something look like it belongs in one place while the markup places it somewhere else entirely.
4. **Record each failure under the correct one of the two** — 'Order is wrong' and 'nothing is visible' are different bugs with different fixes - do not conflate them in a report.

*A visible-focus-indicator and order checker (Python)*

```python
elements = [
    {"name": "Skip to content", "dom": 0, "row": 0, "col": 0, "outline_removed": False, "alt_indicator": False},
    {"name": "Nav: Home", "dom": 1, "row": 0, "col": 1, "outline_removed": False, "alt_indicator": False},
    {"name": "Search input", "dom": 2, "row": 1, "col": 2, "outline_removed": True, "alt_indicator": True},
    {"name": "Search button", "dom": 3, "row": 1, "col": 1, "outline_removed": True, "alt_indicator": False},
    {"name": "Main CTA", "dom": 4, "row": 2, "col": 0, "outline_removed": False, "alt_indicator": False},
]

dom_sequence = [e["name"] for e in elements]
visual_sequence = [e["name"] for e in sorted(elements, key=lambda e: (e["row"], e["col"]))]

print("DOM / Tab order:")
for i, name in enumerate(dom_sequence):
    print("  " + str(i) + ": " + name)

print("")
print("Visual reading order (by row, then column):")
for i, name in enumerate(visual_sequence):
    print("  " + str(i) + ": " + name)

print("")
order_matches = dom_sequence == visual_sequence
if order_matches:
    print("DOM order matches visual order: no mismatch")
else:
    print("DOM order does NOT match visual order:")
    for i in range(len(dom_sequence)):
        if dom_sequence[i] != visual_sequence[i]:
            print("  Position " + str(i) + ": DOM has '" + dom_sequence[i] + "' but visually it reads '" + visual_sequence[i] + "'")

print("")
print("Focus-visible check (WCAG 2.4.7):")
violations = []
for e in elements:
    focus_visible = (not e["outline_removed"]) or e["alt_indicator"]
    status = "VISIBLE" if focus_visible else "NOT VISIBLE"
    print("  " + e["name"] + ": " + status)
    if not focus_visible:
        violations.append(e["name"])

print("")
if violations:
    print("Focus-visible violations: " + ", ".join(violations))
else:
    print("Focus-visible violations: none")

print("")
print("Total elements: " + str(len(elements)))
print("Order mismatches: " + ("0" if order_matches else str(sum(1 for i in range(len(dom_sequence)) if dom_sequence[i] != visual_sequence[i]))))
print("Focus-visible violations: " + str(len(violations)))
```

*A visible-focus-indicator and order checker (Java)*

```java
import java.util.*;

public class Main {
    static class Elem {
        String name;
        int dom, row, col;
        boolean outlineRemoved, altIndicator;
        Elem(String name, int dom, int row, int col, boolean outlineRemoved, boolean altIndicator) {
            this.name = name;
            this.dom = dom;
            this.row = row;
            this.col = col;
            this.outlineRemoved = outlineRemoved;
            this.altIndicator = altIndicator;
        }
    }

    public static void main(String[] args) {
        List<Elem> elements = new ArrayList<>();
        elements.add(new Elem("Skip to content", 0, 0, 0, false, false));
        elements.add(new Elem("Nav: Home", 1, 0, 1, false, false));
        elements.add(new Elem("Search input", 2, 1, 2, true, true));
        elements.add(new Elem("Search button", 3, 1, 1, true, false));
        elements.add(new Elem("Main CTA", 4, 2, 0, false, false));

        List<String> domSequence = new ArrayList<>();
        for (Elem e : elements) domSequence.add(e.name);

        List<Elem> sortedForVisual = new ArrayList<>(elements);
        sortedForVisual.sort((a, b) -> a.row != b.row ? Integer.compare(a.row, b.row) : Integer.compare(a.col, b.col));
        List<String> visualSequence = new ArrayList<>();
        for (Elem e : sortedForVisual) visualSequence.add(e.name);

        System.out.println("DOM / Tab order:");
        for (int i = 0; i < domSequence.size(); i++) {
            System.out.println("  " + i + ": " + domSequence.get(i));
        }

        System.out.println();
        System.out.println("Visual reading order (by row, then column):");
        for (int i = 0; i < visualSequence.size(); i++) {
            System.out.println("  " + i + ": " + visualSequence.get(i));
        }

        System.out.println();
        boolean orderMatches = domSequence.equals(visualSequence);
        int mismatches = 0;
        if (orderMatches) {
            System.out.println("DOM order matches visual order: no mismatch");
        } else {
            System.out.println("DOM order does NOT match visual order:");
            for (int i = 0; i < domSequence.size(); i++) {
                if (!domSequence.get(i).equals(visualSequence.get(i))) {
                    mismatches++;
                    System.out.println("  Position " + i + ": DOM has '" + domSequence.get(i) + "' but visually it reads '" + visualSequence.get(i) + "'");
                }
            }
        }

        System.out.println();
        System.out.println("Focus-visible check (WCAG 2.4.7):");
        List<String> violations = new ArrayList<>();
        for (Elem e : elements) {
            boolean focusVisible = (!e.outlineRemoved) || e.altIndicator;
            String status = focusVisible ? "VISIBLE" : "NOT VISIBLE";
            System.out.println("  " + e.name + ": " + status);
            if (!focusVisible) violations.add(e.name);
        }

        System.out.println();
        if (!violations.isEmpty()) {
            System.out.println("Focus-visible violations: " + String.join(", ", violations));
        } else {
            System.out.println("Focus-visible violations: none");
        }

        System.out.println();
        System.out.println("Total elements: " + elements.size());
        System.out.println("Order mismatches: " + mismatches);
        System.out.println("Focus-visible violations: " + violations.size());
    }
}
```

### Your first time: Run order and visibility as two separate checks

- [ ] Tab through the whole page once, tracking sequence only — Note every point where the next stop feels visually unrelated to where you just were.
- [ ] Tab through again, tracking the indicator only — At every stop, confirm you can actually see - not infer - exactly which element currently has focus.
- [ ] Compare against the visual, sighted reading order — Read the page top to bottom, left to right, the way a sighted user would, and compare that path to Tab's actual path.
- [ ] File order bugs and visibility bugs separately — They have different root causes and different fixes; combining them into one vague report slows down the fix.

- **Every control is reachable and operable, but nothing visibly changes when Tab moves.**
  Check for a global outline: none reset with no replacement style - this is the single most common Focus Visible violation in real codebases.
- **Tab order jumps to a spot that looks completely unrelated to the previous stop.**
  Compare the visual layout to the underlying markup order - CSS order, float, or absolute positioning is very likely rearranging appearance without touching Tab's actual path.
- **A focus indicator is visible but barely - a one-pixel color shift most people would miss.**
  This still counts as a Focus Visible failure in practice even if it technically exists; test with real, varied lighting and vision conditions, not just a controlled monitor in a quiet room.

### Where to check

- Every focusable element, checked for both a sensible sequence and an actually visible indicator - not just one of the two.
- Places where CSS positioning could plausibly separate visual order from markup order - grids, flexbox with `order`, absolutely positioned elements.
- Any global stylesheet reset touching `outline` or `:focus`, since that is where visibility regressions usually start.
- [[accessibility-testing/manual-a11y-testing/keyboard-only-navigation]] for the reachability and operability checks that should happen before this one.
- [[accessibility-testing/why-accessibility-matters/wcag-2-2-a-aa-aaa]] for where Focus Visible sits among WCAG's AA-level requirements.

### Worked example: a redesign that passed every functional test and failed this one completely

1. A visual redesign ships. Every button still works with a mouse click, and a keyboard-only pass
   confirms every control is still reachable with Tab and still operable with Enter.
2. A focus-order-and-visible-focus pass begins separately, watching only the indicator this time.
3. Tab moves through the entire page correctly, in a sensible order - but at no point does anything on
   screen visibly change. The default outline was stripped in the redesign's new global stylesheet.
4. Every control silently passes reachability and operability while failing Focus Visible completely.
5. Report: "No visible focus indicator anywhere on the page after the redesign - outline: none was
   added globally with no replacement. Sighted keyboard users cannot tell where they are at any point."
   The fix (a visible focus style reintroduced globally) is exact because the missing piece was named
   exactly, separate from the reachability checks that had already passed.

**Quiz.** Every control on a page is reachable by Tab and operable with Enter, but no visible change appears anywhere on screen as Tab moves. What does this note say about that result?

- [ ] It passes, since reachability and operability are the only things that matter
- [x] It fails Focus Visible specifically - focus being present is a separate fact from focus being visible, and both are required
- [ ] It only matters for screen reader users, not sighted keyboard users
- [ ] It is acceptable as long as the page still looks visually polished

*The note treats focus order and visible focus as two independent checks. An element can be fully focusable and operable - focus present - while providing no visible indicator at all, which is a genuine, common Focus Visible failure regardless of how well reachability passed.*

- **Focus order** — Whether the sequence Tab visits elements in matches the sequence a sighted reader would naturally follow through the page.
- **Visible focus** — Whether, once an element receives focus, there is an actual visible indicator showing where it currently sits.
- **Present vs visible** — An element can be focusable (present) with no visible indicator at all (not visible) - these are independent facts, and both must hold.
- **Most common Focus Visible violation** — A global CSS reset that strips the default outline for visual polish with no replacement indicator ever added.

### Challenge

Pick one real page. Run a Tab-only pass twice: once tracking only whether the sequence makes visual sense, once tracking only whether you can see the indicator at every stop. Report each failure under the correct one of the two categories, with the specific element involved.

- [W3C — Understanding SC 2.4.3: Focus Order](https://www.w3.org/WAI/WCAG21/Understanding/focus-order.html)
- [W3C — Understanding SC 2.4.7: Focus Visible](https://www.w3.org/WAI/WCAG21/Understanding/focus-visible.html)
- [WCAG 2.4.7 Focus Visible](https://www.youtube.com/watch?v=rgBfNXKH3nE)

🎬 [WCAG 2.4.7 Focus Visible](https://www.youtube.com/watch?v=rgBfNXKH3nE) (5 min)

- Focus order (does Tab's sequence make visual sense) and visible focus (can you see where focus is) are two independent checks.
- An element can be fully focusable and operable while providing zero visible indicator - present is not the same as visible.
- CSS layout techniques like order, float, or absolute positioning can separate visual order from the markup order Tab actually follows.
- The single most common real-world Focus Visible violation is a global outline: none reset with no replacement style.
- File order bugs and visibility bugs as separate findings - they have different causes and different fixes.


## Related notes

- [[Notes/accessibility-testing/manual-a11y-testing/keyboard-only-navigation|Keyboard-only navigation]]
- [[Notes/accessibility-testing/manual-a11y-testing/screen-readers-nvda-voiceover|Screen readers (NVDA / VoiceOver)]]
- [[Notes/accessibility-testing/why-accessibility-matters/wcag-2-2-a-aa-aaa|WCAG 2.2 A / AA / AAA]]


---
_Source: `packages/curriculum/content/notes/accessibility-testing/manual-a11y-testing/focus-order-and-visible-focus.mdx`_
