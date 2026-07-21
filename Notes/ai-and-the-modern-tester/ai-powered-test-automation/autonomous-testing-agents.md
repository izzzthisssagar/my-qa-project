---
title: "Autonomous testing agents"
tags: ["ai-and-the-modern-tester", "ai-powered-test-automation", "track-c"]
updated: "2026-07-21"
---

# Autonomous testing agents

*No script, no fixed steps - an agent like browser-use perceives the current screen, decides one action toward a goal, executes it, and perceives again. That loop finds real bugs no script anticipated - and just as easily wanders into something a script never would have risked.*

> Give a browser-use agent a goal in plain language - "complete checkout with a test card" - and it does
> not run a pre-written script. It looks at the current page, reasons about which element gets it closer
> to the goal, clicks it, looks again, and repeats. No two runs necessarily take the same path. That is
> exactly what makes it capable of finding a bug no fixed script would have stumbled into - and exactly
> what makes it capable of clicking something a careful human tester never would have.

> **In real life**
>
> A bomb disposal robot is sent in precisely because the terrain is unpredictable - nobody scripted the
> exact sequence of moves in advance, because nobody could know what the scene actually looks like until
> the robot's camera is already there. It perceives the immediate scene, its operator (or, increasingly,
> its own onboard reasoning) decides the single next move, the claw executes it, and the camera looks
> again before the next decision. That loop is what lets it handle a scene nobody scripted for. It is
> also exactly why it stays on a live link the whole time, with a human able to stop it the instant a
> decision looks wrong - autonomy was never the same thing as being left unsupervised.

**An autonomous testing agent**: An autonomous testing agent is an AI system that pursues a stated goal inside an application through a repeated perceive-decide-act loop - reading the current screen or DOM state, using an LLM to choose the next action, executing it, then perceiving the resulting state again - rather than following a pre-written, fixed sequence of steps.

## The loop, concretely

Every autonomous testing agent, whatever product wraps it, runs the same core cycle: **perceive** -
capture the current page as a screenshot, an accessibility tree, or both; **decide** - an LLM reasons
about which visible element moves the current state closer to the stated goal; **act** - execute that
one decision (click, type, scroll, navigate); then perceive again, evaluating whether the goal is now
met, closer, or the agent needs a different approach. `browser-use`, the leading open-source
implementation, wires this loop directly to a real Playwright-controlled browser and currently tops
independent long-horizon web-task benchmarks (an 87.4% average on the Odysseys leaderboard, ahead of
computer-use agents from several major labs at time of measurement) - a genuine capability jump over
scripted automation for tasks nobody wrote a script for yet.

## Real value, real risk, same mechanism

The value is exploratory: an agent given a broad goal ("try to break the signup flow") can discover a
sequence of actions - an unusual field order, an unexpected back-navigation, a race between two
async form submissions - that a fixed script never would have tried, because nobody anticipated it
worth scripting. The risk comes from the identical mechanism: an agent reasoning about "which element
gets me closer to the goal" from a screenshot or DOM snapshot can misread an ambiguous UI exactly the
way a rushed human might - confirming the wrong dialog, clicking a visually similar but functionally
different button, or, in a non-sandboxed environment, executing a genuinely destructive action (a real
delete, a real charge) because nothing in its goal statement told it that action was off-limits.

> **Tip**
>
> Run every autonomous agent against a sandboxed environment with synthetic data, never against
> anything touching real user records or real payment rails - the same non-determinism that makes an
> agent good at finding unexpected bugs makes it equally capable of taking an unexpected destructive
> action nobody explicitly forbade.

> **Common mistake**
>
> Treating an autonomous agent's run as reproducible in the way a scripted test is. Re-running the exact
> same goal against the exact same app can take a meaningfully different path - the LLM reasoning step
> is not guaranteed deterministic - which means a bug found once needs a specific, saved repro (the
> actual action sequence taken) before it can be trusted as a stable, fixable report.

![Close-up of a bomb disposal robot's camera sensor head, articulated arm, and gripper claw against a gravel background](autonomous-testing-agents.jpg)
*F6, a bomb disposal robot — Tech. Sgt. James Hodgman, U.S. Air Force, public domain, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:F6_-_a_bomb_disposal_robot_-_151027-F-YM354-303.JPG)*
- **The camera head - perceive** — Reads the current scene before anything else happens. An autonomous testing agent starts every cycle the same way: look at the current screen or DOM state before deciding what to do next.
- **The claw - act** — Executes exactly one decided action - grip, turn, pull. The agent's equivalent: one click, one keystroke, one navigation - then loop back to perceiving whatever that action just produced.
- **The antenna - a human still on the other end** — Autonomous never meant unsupervised. A live link lets an operator stop the robot the instant a decision looks wrong - an autonomous testing agent needs that exact same standing oversight, run in a sandbox, not launched and forgotten.
- **The extended arm, mid-reach** — Committed to one path toward a goal, one joint at a time - and just as capable of confidently reaching for the wrong thing as the right one, if what it perceived was misread.

**One perceive-decide-act cycle**

1. **Perceive: capture the current screen or DOM state** — A screenshot, an accessibility tree, or both - the agent's only information about where it currently is.
2. **Decide: an LLM reasons about the next best action** — Given the stated goal and the current state, which visible element most plausibly moves closer to it.
3. **Act: execute exactly one action** — Click, type, scroll, or navigate - through a real browser automation layer like Playwright.
4. **Perceive again: evaluate progress toward the goal** — Goal met, closer, or stuck - each outcome feeds directly into the next decision, with no fixed script dictating what comes next.

*A minimal perceive-decide-act loop (Python)*

```python
pages = {
    "cart": [
        {"text": "Checkout", "leads_to": "checkout"},
        {"text": "Save for later", "leads_to": "cart"},
    ],
    "checkout": [
        {"text": "Add gift wrap ($5)", "leads_to": "checkout"},
        {"text": "Confirm order", "leads_to": "confirmed"},
    ],
}

GOAL_KEYWORDS = ["checkout", "confirm", "order"]
MAX_STEPS = 6

def decide(available_actions):
    # naive scoring: how many goal keywords appear in the action's text
    scored = []
    for action in available_actions:
        score = sum(1 for kw in GOAL_KEYWORDS if kw in action["text"].lower())
        scored.append((score, action))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]

current_state = "cart"
path = [current_state]
steps = 0

while current_state != "confirmed" and steps < MAX_STEPS:
    action = decide(pages[current_state])
    print("Step " + str(steps + 1) + ": at '" + current_state + "', choosing '" + action["text"] + "'")
    current_state = action["leads_to"]
    path.append(current_state)
    steps += 1

print("")
if current_state == "confirmed":
    print("GOAL REACHED in " + str(steps) + " steps. Path: " + " -> ".join(path))
else:
    print("STOPPED at step budget (" + str(MAX_STEPS) + ") without reaching the goal. Path so far: " + " -> ".join(path))
```

*A minimal perceive-decide-act loop (Java)*

```java
import java.util.*;

public class Main {
    static class Action {
        String text, leadsTo;
        Action(String text, String leadsTo) { this.text = text; this.leadsTo = leadsTo; }
    }

    static final String[] GOAL_KEYWORDS = {"checkout", "confirm", "order"};
    static final int MAX_STEPS = 6;

    static Action decide(List<Action> availableActions) {
        Action best = null;
        int bestScore = -1;
        for (Action a : availableActions) {
            int score = 0;
            for (String kw : GOAL_KEYWORDS) {
                if (a.text.toLowerCase().contains(kw)) score++;
            }
            if (score > bestScore) { bestScore = score; best = a; }
        }
        return best;
    }

    public static void main(String[] args) {
        Map<String, List<Action>> pages = new HashMap<>();
        pages.put("cart", Arrays.asList(
                new Action("Checkout", "checkout"),
                new Action("Save for later", "cart")));
        pages.put("checkout", Arrays.asList(
                new Action("Add gift wrap ($5)", "checkout"),
                new Action("Confirm order", "confirmed")));

        String currentState = "cart";
        List<String> path = new ArrayList<>();
        path.add(currentState);
        int steps = 0;

        while (!currentState.equals("confirmed") && steps < MAX_STEPS) {
            Action action = decide(pages.get(currentState));
            System.out.println("Step " + (steps + 1) + ": at '" + currentState + "', choosing '" + action.text + "'");
            currentState = action.leadsTo;
            path.add(currentState);
            steps++;
        }

        System.out.println();
        if (currentState.equals("confirmed")) {
            System.out.println("GOAL REACHED in " + steps + " steps. Path: " + String.join(" -> ", path));
        } else {
            System.out.println("STOPPED at step budget (" + MAX_STEPS + ") without reaching the goal. Path so far: " + String.join(" -> ", path));
        }
    }
}
```

### Your first time: Run a first autonomous agent against a sandboxed app

- [ ] Set up browser-use (or a similar agent framework) against a disposable, sandboxed test environment — Never a production-adjacent one - synthetic data and a throwaway account only.
- [ ] Give it a single, narrow goal in plain language — 'Complete checkout with a test card' rather than something open-ended and unbounded, for a first run.
- [ ] Watch the actual path it takes, not just whether it succeeded — The sequence of actions is where an unexpected bug - or an unexpected risky click - actually shows up.
- [ ] Re-run the exact same goal a second time — Compare the two paths directly - confirm for yourself whether the run was deterministic or genuinely varied.

- **An autonomous agent reports a bug that nobody can reproduce from the ticket alone.**
  Save the actual action sequence (clicks, inputs, navigation) from the run that found it, not just the final state - a re-run of the same goal is not guaranteed to retrace the identical path.
- **An agent takes an unexpectedly destructive action - deleting a record, submitting a real-looking order - during a run.**
  The environment was not adequately sandboxed for the risk. Route all agent runs through synthetic data and a disposable environment, and treat this as a configuration gap to close, not a one-off surprise to shrug off.
- **The same goal produces wildly different step counts or paths run to run.**
  Expected to some degree - the LLM reasoning step is not fully deterministic. If the variance is extreme enough to make results unusable, narrow the goal statement or add more explicit constraints on what counts as progress.

### Where to check

- The sandbox boundary specifically, before every run - confirm the agent has no path to real user data, real payment processing, or any production-adjacent system.
- The actual action sequence of any bug an agent reports, saved alongside the finding, since the path itself is often not reproducible from the goal statement alone.
- [[ai-and-the-modern-tester/ai-powered-test-automation/ai-test-generation-tools]] for the related but distinct approach of generating static test code instead of executing an adaptive live run.
- [[ai-and-the-modern-tester/ai-powered-test-automation/when-ai-automation-lies]] for the broader pattern of confident, plausible-but-unverified AI output this note's misread-UI risk is one instance of.
- [[exploratory-testing/the-exploratory-mindset/exploratory-not-ad-hoc]] for how the perceive-decide-act loop compares to - and does not replace - a skilled human's exploratory testing session.

### Worked example: an agent that found a real race condition nobody scripted for

1. An autonomous agent is given the goal "complete checkout as fast as possible" against a sandboxed
   staging environment with synthetic test data.
2. Pursuing speed, the agent clicks "Confirm order" and, before the page finishes its network
   round-trip, clicks a "Back" browser action it perceives as available - a sequence no human tester's
   script ever included, because no one thought to test clicking back mid-submission.
3. The result: two order records are created from a single checkout, exposing a real race condition
   in the order-confirmation endpoint that had never surfaced in any prior scripted regression run.
4. The exact action sequence (confirm, then immediate back-navigation) is saved directly from the
   agent's run log and attached to the finding, letting the backend team reproduce it deterministically
   despite the non-deterministic path that discovered it.
5. A scripted regression test is then hand-written from this specific discovery, so the exact race
   condition is now covered permanently by a fast, reproducible check - the agent's job here was
   discovery, not the final regression suite.

**Quiz.** Why does this note say an autonomous testing agent's bug report needs the saved action sequence attached, not just the final broken state?

- [ ] Because the agent cannot describe what happened in plain language
- [x] Because re-running the same goal statement is not guaranteed to retrace the identical path - the LLM reasoning step is not fully deterministic, so the exact sequence that triggered the bug may not recur on its own
- [ ] Because autonomous agents are not allowed to file bug reports directly
- [ ] Because the final broken state is never useful information on its own

*A scripted test's steps are fixed and will retrace exactly the same way every time. An autonomous agent's path emerges from live reasoning about the current screen, which can vary between runs even with an identical goal - so the specific sequence that surfaced a bug has to be captured directly from that run's log, or the finding risks becoming unreproducible the moment someone tries to confirm it.*

- **An autonomous testing agent** — An AI system pursuing a stated goal through a repeated perceive-decide-act loop - reading the current state, choosing one action via an LLM, executing it, and perceiving again - rather than following a fixed script.
- **The perceive-decide-act loop** — Perceive (screenshot/DOM snapshot) -> Decide (LLM reasons about the next best action toward the goal) -> Act (execute one click/type/navigate) -> perceive the new state and repeat.
- **Why autonomous agents find bugs scripts miss** — They can reach action sequences nobody anticipated worth scripting - the same open-ended reasoning that scripted tests, by design, never attempt.
- **Why sandboxing is non-negotiable for these agents** — The identical mechanism that lets an agent discover an unexpected useful bug also lets it take an unexpected destructive action nobody explicitly forbade - real data and real payment rails are never an acceptable target.

### Challenge

Run an autonomous agent (browser-use or similar) against a sandboxed test app with a single narrow goal. Run the exact same goal twice and compare the two action paths directly - report whether they matched, and if not, what specifically diverged.

- [browser-use — GitHub (open-source AI browser agent)](https://github.com/browser-use/browser-use)
- [Explorbot — AI Agent for Exploratory Browser Testing](https://github.com/testomatio/explorbot)
- [BrowserUse: Open Source AI Agent Controls Your Browser! (Complete Tutorial)](https://www.youtube.com/watch?v=cPOGZApkbdk)

🎬 [BrowserUse: Open Source AI Agent Controls Your Browser! (Complete Tutorial)](https://www.youtube.com/watch?v=cPOGZApkbdk) (15 min)

- An autonomous testing agent runs a perceive-decide-act loop - reading the current state, reasoning about the next action toward a goal, executing it, and perceiving again - instead of following a fixed script.
- browser-use, the leading open-source implementation, wires this loop to a real Playwright browser and currently leads independent long-horizon web-task benchmarks over several major labs' computer-use agents.
- The same open-ended reasoning that finds bugs no script anticipated can misread an ambiguous UI and take an unexpected, even destructive, action - always run these agents against a sandboxed environment with synthetic data.
- Runs are not guaranteed reproducible - the same goal can take a different path on a re-run, so a bug finding needs its exact action sequence saved directly from the log, not reconstructed from memory.
- The right role for an autonomous agent is discovery, not the permanent regression suite - once a real bug is found, hand-write (or generate) a fixed, reproducible test to cover it going forward.


## Related notes

- [[Notes/ai-and-the-modern-tester/ai-powered-test-automation/ai-test-generation-tools|AI test generation tools]]
- [[Notes/ai-and-the-modern-tester/ai-powered-test-automation/when-ai-automation-lies|When AI automation lies]]
- [[Notes/exploratory-testing/the-exploratory-mindset/exploratory-not-ad-hoc|Not ad hoc testing]]


---
_Source: `packages/curriculum/content/notes/ai-and-the-modern-tester/ai-powered-test-automation/autonomous-testing-agents.mdx`_
