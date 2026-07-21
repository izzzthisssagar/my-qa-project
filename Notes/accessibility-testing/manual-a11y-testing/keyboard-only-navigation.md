---
title: "Keyboard-only navigation"
tags: ["accessibility-testing", "manual-a11y-testing", "track-c"]
updated: "2026-07-20"
---

# Keyboard-only navigation

*Unplug the mouse and drive the whole product with Tab, Shift+Tab, Enter, Space, and arrow keys - confirming every control is reachable, operable, and never trapped.*

> Unplug the mouse. Set it on the far side of the desk. Now reach every link, button, menu, and form
> field using only the keyboard - and never let a single control swallow focus and refuse to give it
> back. If that sentence made you nervous, that is exactly the test a huge number of shipped products
> would fail today.

> **In real life**
>
> A flat-pack furniture box ships with exactly one tool: a small hex key, tucked in a plastic bag with
> the screws. That hex key is deliberately the only tool assumed - no power drill, no separate wrench -
> because the whole point is that anyone who opens the box can finish the build with what came inside.
> A real quality check on the instructions is trying to assemble the entire piece using only that one
> key, start to finish, never once reaching for a power tool sitting right there on the bench. Keyboard-
> only navigation testing is the same discipline: the keyboard is the one tool guaranteed to be present,
> and the test is whether the whole product can actually be finished with it alone.

**Keyboard-only navigation testing**: Keyboard-only navigation testing verifies that every interactive element in a product - links, buttons, form fields, menus, custom widgets - can be reached, operated, and left again using only keyboard input (Tab, Shift+Tab, Enter, Space, and arrow keys), with no reliance on a mouse and no point where focus becomes trapped.

## What the pass actually checks

Three separate questions, checked for every single interactive element on the page: can Tab (and
Shift+Tab going backward) actually reach it, does pressing Enter or Space actually operate it the way
a click would, and once focus lands somewhere, can it always move on to the next element - never stuck.
Arrow keys matter for composite widgets like menus, tabs, and radio groups, where the expected behavior
is arrow-key movement between options rather than pure Tab-per-option. A control that a mouse user
never notices anything wrong with can still be completely unusable this way if it was only ever wired
up for `onclick`.

## Reachable, operable, and never trapped - all three, every time

A single missing piece breaks the whole pass. A custom dropdown might be perfectly reachable by Tab
and open correctly on Enter, but if Escape does not close it and Tab does not move past it afterward,
that is a keyboard trap - focus is stuck circling inside one component while the rest of the page
becomes permanently unreachable. Equally common: a `div` styled to look exactly like a button, with a
click handler attached, that Tab skips over entirely because a plain `div` was never in the keyboard
navigation sequence to begin with. It looks identical to a real button and does nothing for a keyboard
user.

> **Tip**
>
> Do the entire pass with your hands off the mouse and the mouse physically unplugged or moved out of
> reach for the first run. It is far too easy to unconsciously reach for it to "just fix" a stuck moment,
> which quietly erases the exact evidence you were testing for.

> **Common mistake**
>
> Assuming a control is keyboard-operable because it visually resembles a standard button or link.
> Visual styling tells you nothing about the underlying element or its event bindings - only pressing
> Tab to it and then Enter or Space actually proves it.

![Overhead view of a MacBook keyboard and trackpad, with the tab key, shift key, arrow key cluster, and trackpad all clearly visible](keyboard-only-navigation.jpg)
*Minimal laptop keyboard — Unsplash via Wikimedia Commons, CC0. [Source](https://commons.wikimedia.org/wiki/File:Minimal_laptop_keyboard_(Unsplash).jpg)*
- **Tab** — Moves focus forward to the next reachable element - the single most-used key in this entire pass.
- **Shift** — Held with Tab, moves focus backward. If Shift+Tab never returns you to where you just were, that is its own bug.
- **Arrow key cluster** — Composite widgets - menus, tabs, radio groups - are expected to respond to arrow keys for moving between their own options.
- **The trackpad, deliberately unused** — A keyboard-only pass means this surface stays untouched for the entire run - every result has to come from the keys alone.

**One keyboard-only pass**

1. **Start at the top of the page with Tab** — Press Tab repeatedly and track exactly which elements receive focus, in what order.
2. **Operate each one with Enter or Space** — Confirm the action actually fires - a link, button, or control that focuses but does nothing has failed.
3. **Test arrow keys inside composite widgets** — Menus, tabs, and radio groups should respond to arrow keys for moving between their own options.
4. **Confirm Tab always moves on afterward** — Every component - especially modals and custom dropdowns - must release focus rather than trap it.

*A tab-order-vs-DOM-order comparator (Python)*

```python
elements = [
    {"name": "Skip link", "dom": 0, "tabindex": 0},
    {"name": "Logo link", "dom": 1, "tabindex": 0},
    {"name": "Search input", "dom": 2, "tabindex": 3},
    {"name": "Search button", "dom": 3, "tabindex": 2},
    {"name": "Nav: Home", "dom": 4, "tabindex": 0},
    {"name": "Nav: Pricing", "dom": 5, "tabindex": 0},
    {"name": "Promo banner close (X)", "dom": 6, "tabindex": -1},
    {"name": "Main CTA button", "dom": 7, "tabindex": 0},
]

print("DOM order:")
for e in elements:
    print("  " + str(e["dom"]) + ": " + e["name"] + " (tabindex=" + str(e["tabindex"]) + ")")

reachable = [e for e in elements if e["tabindex"] >= 0]
positive = sorted([e for e in reachable if e["tabindex"] > 0], key=lambda e: (e["tabindex"], e["dom"]))
zero = [e for e in reachable if e["tabindex"] == 0]
tab_order = positive + zero
unreachable = [e for e in elements if e["tabindex"] < 0]

print("")
print("Computed Tab order:")
for i, e in enumerate(tab_order, start=1):
    print("  " + str(i) + ": " + e["name"] + " (tabindex=" + str(e["tabindex"]) + ")")

print("")
if unreachable:
    for e in unreachable:
        print("UNREACHABLE BY TAB (tabindex=-1): " + e["name"])
else:
    print("No unreachable elements found")

print("")
dom_sequence = [e["name"] for e in elements if e["tabindex"] >= 0]
tab_sequence = [e["name"] for e in tab_order]
mismatch_found = False
for name in tab_sequence:
    dom_pos = dom_sequence.index(name)
    tab_pos = tab_sequence.index(name)
    if dom_pos != tab_pos:
        mismatch_found = True
        print("DOM-vs-tab-order mismatch: '" + name + "' sits at DOM position " + str(dom_pos) + " but Tab position " + str(tab_pos))

if not mismatch_found:
    print("DOM order and Tab order match exactly")

print("")
print("Total interactive elements: " + str(len(elements)))
print("Reachable by Tab: " + str(len(reachable)))
print("Unreachable: " + str(len(unreachable)))
```

*A tab-order-vs-DOM-order comparator (Java)*

```java
import java.util.*;

public class Main {
    static class Elem {
        String name;
        int dom;
        int tabindex;
        Elem(String name, int dom, int tabindex) {
            this.name = name;
            this.dom = dom;
            this.tabindex = tabindex;
        }
    }

    public static void main(String[] args) {
        List<Elem> elements = new ArrayList<>();
        elements.add(new Elem("Skip link", 0, 0));
        elements.add(new Elem("Logo link", 1, 0));
        elements.add(new Elem("Search input", 2, 3));
        elements.add(new Elem("Search button", 3, 2));
        elements.add(new Elem("Nav: Home", 4, 0));
        elements.add(new Elem("Nav: Pricing", 5, 0));
        elements.add(new Elem("Promo banner close (X)", 6, -1));
        elements.add(new Elem("Main CTA button", 7, 0));

        System.out.println("DOM order:");
        for (Elem e : elements) {
            System.out.println("  " + e.dom + ": " + e.name + " (tabindex=" + e.tabindex + ")");
        }

        List<Elem> reachable = new ArrayList<>();
        for (Elem e : elements) if (e.tabindex >= 0) reachable.add(e);

        List<Elem> positive = new ArrayList<>();
        for (Elem e : reachable) if (e.tabindex > 0) positive.add(e);
        positive.sort((a, b) -> a.tabindex != b.tabindex ? Integer.compare(a.tabindex, b.tabindex) : Integer.compare(a.dom, b.dom));

        List<Elem> zero = new ArrayList<>();
        for (Elem e : reachable) if (e.tabindex == 0) zero.add(e);

        List<Elem> tabOrder = new ArrayList<>();
        tabOrder.addAll(positive);
        tabOrder.addAll(zero);

        List<Elem> unreachable = new ArrayList<>();
        for (Elem e : elements) if (e.tabindex < 0) unreachable.add(e);

        System.out.println();
        System.out.println("Computed Tab order:");
        for (int i = 0; i < tabOrder.size(); i++) {
            Elem e = tabOrder.get(i);
            System.out.println("  " + (i + 1) + ": " + e.name + " (tabindex=" + e.tabindex + ")");
        }

        System.out.println();
        if (!unreachable.isEmpty()) {
            for (Elem e : unreachable) {
                System.out.println("UNREACHABLE BY TAB (tabindex=-1): " + e.name);
            }
        } else {
            System.out.println("No unreachable elements found");
        }

        System.out.println();
        List<String> domSequence = new ArrayList<>();
        for (Elem e : elements) if (e.tabindex >= 0) domSequence.add(e.name);
        List<String> tabSequence = new ArrayList<>();
        for (Elem e : tabOrder) tabSequence.add(e.name);

        boolean mismatchFound = false;
        for (String name : tabSequence) {
            int domPos = domSequence.indexOf(name);
            int tabPos = tabSequence.indexOf(name);
            if (domPos != tabPos) {
                mismatchFound = true;
                System.out.println("DOM-vs-tab-order mismatch: '" + name + "' sits at DOM position " + domPos + " but Tab position " + tabPos);
            }
        }
        if (!mismatchFound) {
            System.out.println("DOM order and Tab order match exactly");
        }

        System.out.println();
        System.out.println("Total interactive elements: " + elements.size());
        System.out.println("Reachable by Tab: " + reachable.size());
        System.out.println("Unreachable: " + unreachable.size());
    }
}
```

### Your first time: Run a first keyboard-only pass on one real page

- [ ] Move the mouse out of reach — Physically, not just figuratively - the temptation to grab it mid-test is strong.
- [ ] Tab from the very top of the page to the very bottom — Write down every element that receives focus, in order, as it happens.
- [ ] Operate every focused control with Enter or Space — A focus ring with no resulting action is a failure just as real as no focus ring at all.
- [ ] Deliberately try to get stuck — Open every modal, dropdown, and custom widget and confirm Escape or Tab always gets you back out.

- **Tab skips a control entirely that a mouse user can click just fine.**
  Check the underlying element - a `div` or `span` with a click handler is invisible to Tab unless it is a real interactive element or has an explicit `tabindex`.
- **Focus enters a modal or custom dropdown and Tab never leaves it.**
  That is a keyboard trap. Confirm Escape closes the component and that focus then returns to a sensible, visible location on the page behind it.
- **Enter operates a button but Space does not, or vice versa.**
  Native buttons respond to both by default; a custom-built control likely has an incomplete key handler and needs both keys wired up explicitly.

### Where to check

- Every interactive element on the page, checked individually - links, buttons, inputs, custom widgets, not just the obvious ones.
- Modals, dropdowns, and any component that can visually cover other content, specifically for keyboard traps.
- Whether Tab order and visual reading order actually agree, since a working tab stop in the wrong place is still confusing.
- [[accessibility-testing/manual-a11y-testing/focus-order-and-visible-focus]] for exactly how to evaluate that order and the focus indicator itself once reachability is confirmed.
- [[accessibility-testing/why-accessibility-matters/pour-principles]] for why this entire pass falls under the Operable principle specifically.

### Worked example: a checkout that looked perfectly fine until the mouse came unplugged

1. A "Apply promo code" button on checkout works perfectly with a mouse click in every manual test so far.
2. A keyboard-only pass begins at the top of the page and tabs downward through the form.
3. Tab reaches the promo code text input, but the very next Tab press jumps straight past the "Apply"
   button to the "Place order" button beneath it - the button itself never receives focus.
4. Inspection shows the "Apply" control is a styled `span` with an `onclick` handler, not a real
   `button` element, and it was never given a `tabindex`.
5. Report: "Promo code 'Apply' control is unreachable by keyboard - it is a `span`, not a real button,
   and has no tabindex. Keyboard-only users cannot apply a promo code at all." The fix is exact because
   the missing element type was named exactly.

**Quiz.** A custom dropdown can be reached with Tab and opens correctly with Enter, but pressing Escape does nothing and Tab does not move past it while it is open. What does this note call that specific problem?

- [ ] A missing accessible name
- [x] A keyboard trap
- [ ] A contrast failure
- [ ] An acceptable trade-off since the dropdown is reachable at all

*Reachable and initially operable is not the same as fully passing. A component that focus enters but cannot leave - blocking Tab from moving the rest of the page - is a keyboard trap, and it is a severe, independent failure regardless of how well the component's opening behavior works.*

- **Keyboard-only navigation testing** — Verifying every interactive element can be reached, operated, and left again using only Tab, Shift+Tab, Enter, Space, and arrow keys - no mouse.
- **Keyboard trap** — A component that focus can enter but never leave using standard keys, blocking the rest of the page from being reached at all.
- **Why a div with onclick fails this test** — Tab only visits real interactive elements or elements with an explicit tabindex - a styled div is invisible to keyboard navigation by default.
- **Arrow keys in this test** — Expected for moving between options inside composite widgets like menus, tabs, and radio groups - not a substitute for Tab between separate controls.

### Challenge

Pick one real page with a modal or custom dropdown. Unplug the mouse and Tab through the entire page, operating every control with Enter or Space. Report every element Tab skips and every place focus gets stuck, naming the exact element type behind each failure.

- [WebAIM — Keyboard Accessibility](https://webaim.org/techniques/keyboard/)
- [W3C — Understanding SC 2.1.1: Keyboard](https://www.w3.org/WAI/WCAG21/Understanding/keyboard.html)
- [Practical Web Accessibility — Keyboard-only Navigation, Part 1](https://www.youtube.com/watch?v=vJwv9K7xkkc)

🎬 [Practical Web Accessibility — Keyboard-only Navigation, Part 1](https://www.youtube.com/watch?v=vJwv9K7xkkc) (7 min)

- Keyboard-only navigation testing checks three things for every interactive element: reachable by Tab, operable with Enter or Space, and never trapped.
- Composite widgets like menus and tabs are expected to also respond to arrow keys between their own options.
- A styled div or span with a click handler is invisible to Tab unless it is a real interactive element or has an explicit tabindex.
- A keyboard trap - focus that enters a component and cannot leave - is a severe, independent failure even if the component otherwise works.
- Doing the whole pass with the mouse physically out of reach prevents unconsciously erasing the evidence you are testing for.


## Related notes

- [[Notes/accessibility-testing/manual-a11y-testing/focus-order-and-visible-focus|Focus order & visible focus]]
- [[Notes/accessibility-testing/manual-a11y-testing/screen-readers-nvda-voiceover|Screen readers (NVDA / VoiceOver)]]
- [[Notes/accessibility-testing/why-accessibility-matters/pour-principles|POUR principles]]


---
_Source: `packages/curriculum/content/notes/accessibility-testing/manual-a11y-testing/keyboard-only-navigation.mdx`_
