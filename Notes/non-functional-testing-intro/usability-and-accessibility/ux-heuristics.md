---
title: "UX heuristics"
tags: ["non-functional-testing-intro", "usability-and-accessibility", "track-c"]
updated: "2026-07-18"
---

# UX heuristics

*Use established usability heuristics as inspection lenses, support findings with evidence, and avoid treating a checklist as a substitute for users.*

> A control panel can expose every possible function and still make the urgent one impossible to find.
> Heuristics give a tester names for that friction: visibility, match with the real world, control,
> consistency, error prevention, recognition, flexibility, minimalism, recovery, and help.

> **In real life**
>
> Heuristics are a mechanic's inspection lights. Each illuminates a different surface, but the light does
> not decide whether the car is safe. A finding still needs a concrete task, observation, impact, and
> context; [[non-functional-testing-intro/usability-and-accessibility/usability-testing]] adds real users.

**Usability heuristic**: A usability heuristic is a broad, evidence-informed rule of thumb used to inspect an interface for likely usability problems. It is a diagnostic lens rather than a binary standard, legal requirement, or guarantee of user success.

## Turn labels into test questions

For **visibility of system status**, ask what the interface communicates after an action and whether it
arrives soon enough. For **user control and freedom**, try cancel, undo, back, and escape routes. For
**error prevention and recovery**, trigger a realistic mistake and inspect both the guardrail and the
message. For **recognition rather than recall**, check whether choices and prior context remain visible.

> **Tip**
>
> Write findings as "During task X, condition Y violates heuristic Z because the user cannot recover,
> causing impact Q." The heuristic supplies shared vocabulary; the task and impact make it actionable.

> **Common mistake**
>
> Do not award a page "9/10 heuristics passed." The heuristics overlap, are not equally important, and are
> not designed as a conformance score. One irreversible data-loss path matters more than several cosmetic
> consistency nits.

![A Japanese toilet control panel with many labeled buttons, icons, a display, and an open cover](ux-heuristics.jpg)
*Wireless toilet control panel with open lid — Chris 73, Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:Wireless_toilet_control_panel_w._open_lid.jpg)*
- **Status display** — Visibility asks whether the system clearly confirms its current state and the result of an action.
- **Prominent stop control** — User control asks whether a person can stop, cancel, undo, or safely leave an unwanted state.
- **Icons plus labels** — Recognition improves when meaning is visible, but testers must confirm that symbols and language match the intended audience.
- **Covered advanced controls** — Minimalism can hide secondary complexity while keeping frequent actions available; hiding must not remove essential access.

**A heuristic inspection that produces evidence**

1. **Choose a critical user task** — Inspect a journey, not a screenshot floating outside context.
2. **Apply several relevant heuristic lenses** — Check feedback, language, control, prevention, recognition, consistency, and recovery.
3. **Reproduce a concrete breakdown** — Capture the action, state, expected signal, actual behavior, and affected user goal.
4. **Prioritize by impact and validate** — Use severity and user research, analytics, or support evidence; never prioritize by checklist count alone.

*A heuristic finding oracle (Python)*

```python
checks = {
    "task_named": True,
    "heuristic_named": True,
    "observable_breakdown": True,
    "impact_explained": True,
}
for name, passed in checks.items():
    print(name + "=" + ("PASS" if passed else "FAIL"))
result = "PASS" if all(checks.values()) else "FAIL"
assert result == "PASS", "heuristic oracle rejected vague finding"
print("RESULT=" + result)
```

*A heuristic finding oracle (Java)*

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        Map<String, Boolean> checks = new LinkedHashMap<>();
        checks.put("task_named", true);
        checks.put("heuristic_named", true);
        checks.put("observable_breakdown", true);
        checks.put("impact_explained", true);
        boolean ok = true;
        for (var entry : checks.entrySet()) {
            System.out.println(entry.getKey() + "=" + (entry.getValue() ? "PASS" : "FAIL"));
            ok &= entry.getValue();
        }
        String result = ok ? "PASS" : "FAIL";
        if (!result.equals("PASS")) throw new AssertionError("heuristic oracle rejected vague finding");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Inspect one risky journey with four lenses

- [ ] Name the journey and intended user — Choose a consequential path such as deleting, paying, publishing, or changing permissions.
- [ ] Probe feedback, control, prevention, and recovery — For every action, ask what the person sees, how they escape, what prevents a mistake, and how they recover.
- [ ] Capture one concrete breakdown — Record the exact state, action, observed result, expected signal, and user impact.
- [ ] Validate priority — Compare with participant behavior, analytics, support evidence, and product risk rather than counting heuristic labels.

- **Reviewers produce dozens of subjective comments.**
  Anchor each comment to a task, observable breakdown, named heuristic, and impact. Remove preference-only claims.
- **Two heuristics appear to describe the same defect.**
  Choose the label that best explains the mechanism, note a secondary lens only if useful, and file one finding rather than duplicates.
- **The checklist is green but users still fail.**
  Run representative usability sessions. Heuristics predict likely friction; they do not replace observed human behavior.

### Where to check

- Loading, saving, and background operations for visible system status.
- Destructive flows for cancel, undo, confirmation, and recovery.
- Labels, icons, ordering, and platform conventions for consistency and real-world match.
- Error messages for plain language, preserved input, and a next action.

### Worked example: delete with no way back

1. A tester deletes a saved report and receives only a brief "Done" toast.
2. The task is consequential, there is no confirmation, and no undo or recovery path is visible.
3. The finding uses error prevention plus user control: one mistaken click permanently removes work.
4. The team adds a specific confirmation and a timed undo, then tests keyboard and screen-reader paths.

**Quiz.** What makes a heuristic finding actionable?

- [ ] A numeric score for all ten heuristics
- [x] A concrete task, observable breakdown, relevant heuristic, and user impact
- [ ] The reviewer's visual preference
- [ ] Using as many heuristic labels as possible

*A heuristic is useful vocabulary, but the reproducible task and user impact are what let a team understand and prioritize the defect.*

- **Heuristic** — A diagnostic rule of thumb, not a binary conformance standard.
- **Visibility** — The system communicates current state and action results in time to guide the user.
- **Control and recovery** — People can cancel, undo, escape, and recover from realistic mistakes.

### Challenge

Inspect a destructive action with visibility, control, prevention, and recovery lenses. File only the
highest-impact evidence-based issue, and explain why it outranks cosmetic inconsistencies.

- [Nielsen Norman Group — 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [W3C WAI — Evaluating Web Accessibility Overview](https://www.w3.org/WAI/test-evaluate/)
- [Nehmat Gereige — 📊 10 Usability Heuristics Explained with Real UX Examples (Nielsen Norman Group)](https://www.youtube.com/watch?v=6_e1AiOZHC0)

🎬 [📊 10 Usability Heuristics Explained with Real UX Examples (Nielsen Norman Group)](https://www.youtube.com/watch?v=6_e1AiOZHC0) (13 min)

- Heuristics are inspection lenses, not scores or guarantees.
- Start with a user task and turn each label into a test question.
- A strong finding combines a reproducible breakdown, heuristic mechanism, and user impact.
- Prioritize by severity and validate with user or product evidence, not checklist totals.


## Related notes

- [[Notes/non-functional-testing-intro/usability-and-accessibility/usability-testing|Usability testing]]
- [[Notes/non-functional-testing-intro/usability-and-accessibility/accessibility-wcag|Accessibility (WCAG)]]
- [[Notes/ui-ux-design-qa/design-principles-and-the-laws-of-ux/nielsens-10-usability-heuristics|Nielsen's 10 usability heuristics]]


---
_Source: `packages/curriculum/content/notes/non-functional-testing-intro/usability-and-accessibility/ux-heuristics.mdx`_
