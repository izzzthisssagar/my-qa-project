---
title: "Repro steps"
tags: ["defect-management", "writing-bug-reports", "track-c"]
updated: "2026-07-16"
---

# Repro steps

*Exact, numbered, one-action-per-line instructions from a known starting point - the single field most responsible for whether a bug gets fixed on the first read or bounces back unreproduced.*

> "I tried logging in and it didn't work" and "1. Go to /login. 2. Enter a valid email with a password
> containing an apostrophe. 3. Click Sign in." describe the exact same discovered bug. Only one of them
> lets a developer reproduce it without messaging you first. Repro steps are the single field most
> responsible for whether a valid bug gets fixed today or bounces back marked Cannot Reproduce a week
> from now — and the skill of writing them well is almost entirely about precision, not length.

> **In real life**
>
> A three-dial combination padlock only opens when every dial lands on the EXACT right digit, aligned
> against the same fixed reference line, in whatever order you set them. "Turn it to roughly 9, then
> somewhere around 0, then near 1" opens nothing — the lock doesn't reward a close guess, it requires
> an exact value on every single dial. Vague repro steps fail the same way: "click around the settings
> area" is the equivalent of spinning a dial to "somewhere around 9." A bug only reproduces reliably
> when every step lands on the exact action, in the exact order, same as every dial has to land exactly
> on its digit before the shackle releases.

**repro steps**: Repro steps (steps to reproduce) are the numbered sequence of exact actions, taken from a known, stated starting point, that reliably triggers a reported defect. Each step describes ONE discrete action - not a group of actions - using the same words the interface itself uses (the actual button label, not a paraphrase). Complete repro steps let someone who has never seen the bug attempt the same reproduction using only the written steps, without needing to ask the original reporter anything.

## What makes a step exact instead of vague

- **One action per step.** "Log in and go to settings and change the email" is three steps
  compressed into one line, and compression is exactly where the detail that actually matters tends
  to hide. If the bug depends on the ORDER of those three actions, a single combined line can't show
  that order was significant.
- **Specific values, not categories.** "Enter a password" is a category; "enter `Passw0rd!'` (a
  password containing an apostrophe)" is a specific value. If any value in the bug (which browser,
  which account type, which exact input) matters to reproducing it, name the specific one used —
  not a general description of the kind of thing it was.
- **The interface's own words.** If the button says "Sign in," write "Click Sign in" — not "log in"
  or "authenticate." A developer scanning the actual screen for the exact label you named finds it
  in one glance; a paraphrase forces them to guess which real control you meant.
- **A stated starting point.** "Starting from a logged-out state, on the homepage" tells a developer
  exactly where to begin. Steps that assume unstated prior context (an account in some specific state,
  a particular prior action) will reproduce for the reporter and mysteriously fail for everyone else.

> **Common mistake**
>
> Writing steps from memory, after the fact, instead of literally re-performing them while writing.
> Memory smooths over exactly the details that turn out to matter — the specific value typed, the
> precise click order, a step taken without noticing it was even a step. The safest habit: reproduce
> the bug ONE MORE TIME while writing the numbered list down in real time, not from recollection
> afterward.

![A close-up photograph of a classic 3-dial combination padlock with brushed metal body, each of the three dials showing a row of engraved numbers, and a fixed reference line running vertically down the front of the lock body](repro-steps.jpg)
*3-combination Master padlock — Wikimedia Commons, public domain (ZooFari). [Source](https://commons.wikimedia.org/wiki/File:3-combination_Master_padlock.jpg)*
- **Dial one — step one, an exact value** — Not 'somewhere near the top' - one specific digit. A repro step's first action needs the same exactness: the actual value typed or clicked, not a category of value.
- **Dial two — step two, independent and exact** — A separate action with its own exact requirement, unaffected by whether dial one was set correctly. Each repro step should be independently checkable - a reader should be able to verify step 2 was followed correctly without re-deriving step 1.
- **Dial three — the last step, still exact** — Precision doesn't relax on the final step just because the first two are done - the lock needs all three exact, and a bug's repro steps need every single one exact, not just the first couple.
- **The fixed reference line — the shared standard every dial is checked against** — Every dial is read against the SAME fixed line, not eyeballed independently - a shared, unambiguous reference point. Naming the interface's own exact label ('Click Sign in') plays the same role: a shared reference anyone reading the steps can check against, instead of a paraphrase that means something slightly different to each reader.
- **The shackle — stays locked until every step is exact** — One approximately-right dial keeps the whole lock closed. One vague or skipped repro step can be the entire reason a real, valid bug fails to reproduce for someone else - the failure doesn't announce which dial was off, it just doesn't open.

**Compressed steps, unpacked into exact ones**

1. **Compressed: 'logged in and changed my email, it broke'** — Three or more actions hidden in one sentence. If order or a specific value mattered, it's invisible here.
2. **Unpacked, starting point stated** — 'Starting from a logged-out state on the homepage:' - now anyone knows exactly where to begin, not assuming unstated prior context.
3. **One action per numbered step** — 1. Click Sign in. 2. Enter [email] / [password]. 3. Click the account icon. 4. Click Edit email.
4. **Specific values named** — Not 'a valid email' - the actual value used, or a realistic placeholder that preserves whatever made it trigger the bug (e.g. an email already in use by another account).
5. **Interface's own words used throughout** — 'Click Edit email' matches the real button label exactly - a developer finds the exact control on the first glance at the screen.

A quick, mechanical check for whether steps are actually atomic: does any single step contain more
than one verb joined by 'and'? Here's a small script that flags exactly that — a real, if blunt,
first-pass signal that a step might be hiding a compressed sequence.

*Run it - flag repro steps that hide more than one action (Python)*

```python
step_sets = [
    [
        "Starting from a logged-out state on the homepage",
        "Click Sign in",
        "Enter demo@example.com / Passw0rd!",
        "Click the account icon",
        "Click Edit email",
    ],
    [
        "Log in and go to settings and change the email",
        "See the error",
    ],
]

MULTI_ACTION_MARKERS = [" and ", " then "]

def flag_compressed_steps(steps):
    flagged = []
    for i, step in enumerate(steps, start=1):
        lowered = step.lower()
        if any(marker in lowered for marker in MULTI_ACTION_MARKERS):
            flagged.append((i, step))
    return flagged

for i, steps in enumerate(step_sets, start=1):
    print(f"Step set {i}:")
    flagged = flag_compressed_steps(steps)
    if not flagged:
        print("  All steps look atomic (no 'and'/'then' joining multiple actions).")
    else:
        for step_num, text in flagged:
            print(f"  Step {step_num} may hide multiple actions: \\"{text}\\"")
    print()

# Step set 1:
#   All steps look atomic (no 'and'/'then' joining multiple actions).
#
# Step set 2:
#   Step 1 may hide multiple actions: "Log in and go to settings and change the email"
```

Same check in Java, for teams whose ticket-linting tooling already runs on the JVM:

*Run it - flag repro steps that hide more than one action (Java)*

```java
import java.util.*;

public class Main {
    static final List<String> MULTI_ACTION_MARKERS = List.of(" and ", " then ");

    public static void main(String[] args) {
        List<List<String>> stepSets = List.of(
            List.of(
                "Starting from a logged-out state on the homepage",
                "Click Sign in",
                "Enter demo@example.com / Passw0rd!",
                "Click the account icon",
                "Click Edit email"
            ),
            List.of(
                "Log in and go to settings and change the email",
                "See the error"
            )
        );

        int setNum = 1;
        for (List<String> steps : stepSets) {
            System.out.println("Step set " + setNum + ":");
            List<String> flagged = new ArrayList<>();
            for (int i = 0; i < steps.size(); i++) {
                String lowered = steps.get(i).toLowerCase();
                for (String marker : MULTI_ACTION_MARKERS) {
                    if (lowered.contains(marker)) {
                        flagged.add("  Step " + (i + 1) + " may hide multiple actions: \\"" + steps.get(i) + "\\"");
                        break;
                    }
                }
            }
            if (flagged.isEmpty()) {
                System.out.println("  All steps look atomic (no 'and'/'then' joining multiple actions).");
            } else {
                flagged.forEach(System.out::println);
            }
            System.out.println();
            setNum++;
        }
    }
}

/* Step set 1:
     All steps look atomic (no 'and'/'then' joining multiple actions).

   Step set 2:
     Step 1 may hide multiple actions: "Log in and go to settings and change the email" */
```

### Your first time: Your mission: turn one vague, compressed bug description into exact repro steps

- [ ] Find or reproduce one real bug — Reuse the one from the previous note's exercise if you still have access to it, or find a fresh small one.
- [ ] Write the compressed, one-sentence version first, on purpose — 'I clicked around and it broke' - the honest, lazy version most real bad reports actually look like.
- [ ] Re-perform the bug one more time, writing each action down AS you do it — Not from memory afterward - live, one numbered line per single action, in the interface's own words.
- [ ] Check every step against the atomic-action test — Does any step contain 'and' or 'then' joining two actions? If so, split it into two numbered steps.
- [ ] Run the Python playground with your own step list — Confirm the script finds zero compressed steps in your final version - and if it flags one, decide honestly whether it's really two actions or a legitimate exception.

You now have a real set of exact, atomic repro steps, written the way you'll want every future bug
report you file to read on the first try.

- **A developer follows your numbered steps exactly and still can't reproduce the bug.**
  Check for an unstated starting point first - a specific account state, a prior action, a particular piece of existing data that wasn't mentioned. The most common reason 'exact-looking' steps still fail for someone else is a real precondition the original reporter didn't realize was load-bearing because it was already true when they started.
- **You wrote detailed steps, but a step like 'navigate to the relevant settings page' still isn't specific enough for someone new to the product.**
  Name the ACTUAL path or the exact label/breadcrumb, not a description of the destination's purpose. 'Navigate to the relevant settings page' assumes the reader already knows where that is; 'Go to Account > Privacy > Data export' doesn't.
- **A bug only reproduces sometimes, even when you follow your own written steps exactly.**
  This is a real, different problem from vague steps - some defects are genuinely intermittent (race conditions, timing-dependent, data-state-dependent). Note the reproduction RATE honestly ('reproduces about 1 in 5 attempts') rather than either pretending it's 100% or giving up on writing steps at all - a rate is still useful information.
- **Someone reads your repro steps and reproduces a DIFFERENT bug than the one you meant.**
  Check whether a step used a vague interface reference that resolves to more than one real control (e.g. two different buttons both roughly describable as 'the save button'). Naming the exact, unambiguous label - or a screenshot pin if the interface genuinely has two similarly-named controls - resolves this.

### Where to check

- **Screen recording tools**, if available — a short recording alongside written steps resolves nearly all remaining ambiguity about exact clicks and timing, and is worth attaching even when the written steps feel solid.
- **Your own re-performance of the bug**, live, immediately before finalizing the report — not memory. If you can't currently reproduce it yourself right now while writing, that's worth noting explicitly rather than writing steps from an earlier session's recollection.
- **The browser's or app's own network/console panel** (see the browser-devtools-mastery module) — for confirming an exact request, an exact error, or an exact timestamp that belongs in a step, rather than describing it approximately.
- **A second person attempting your steps before you file**, when time allows — the single fastest way to catch an unstated assumption is watching someone else get stuck on a step you thought was obvious.

### Worked example: an intermittent bug's honestly-stated repro steps, rate included

1. A tester notices a "save" button occasionally doesn't persist a change, but it doesn't happen
   every time — a bug that resists a clean, deterministic repro.
2. Resisting the urge to either give up on steps or falsely claim 100% reproduction, the tester
   performs the same sequence ten times, counting: 3 out of 10 attempts show the failure.
3. Filed steps: "1. Starting from a freshly loaded settings page. 2. Change the display name field.
   3. Click Save immediately (within ~1 second of finishing typing). 4. Reload the page and check
   whether the new name persisted. Reproduces approximately 3/10 attempts when Save is clicked within
   1 second of the last keystroke; did not reproduce in 5/5 attempts when waiting 3+ seconds before
   clicking Save."
4. That last sentence — the deliberate comparison between fast-click and slow-click attempts — is
   the tester doing real investigative work, not just reporting a vague flake. It hands the developer
   a genuinely useful lead: likely a race between a debounced input handler and the click handler.
5. The developer confirms exactly that root cause in under an hour, specifically because the repro
   steps included the timing detail and the honest, measured reproduction rate — a report that had
   simply said "sometimes save doesn't work" would have taken far longer to narrow down to the same
   root cause.

**Quiz.** A bug report's repro steps read: '1. Log in. 2. Go to the dashboard and click the export button and select CSV. 3. Observe the error.' What's the most accurate assessment of step 2?

- [ ] It's fine - all three actions happen on the same page, so grouping them into one step is reasonable
- [x] It should be split into three separate numbered steps, since it's currently one step containing three distinct actions joined by 'and'
- [ ] It's fine as long as step 3 clearly describes the error
- [ ] It only needs to be split if the bug turns out to depend on the exact order of those three actions

*This note's atomic-step rule is explicit: one action per step, regardless of whether the actions happen on the same page or in quick succession. Step 2 as written joins THREE actions (navigate, click export, select CSV) with 'and' twice - exactly the compression pattern the Python playground's check is built to catch. Option one wrongly excuses compression just because the actions are visually close together on one page - proximity doesn't make three actions into one. Option three is a distractor: a clear step 3 doesn't fix an ambiguous step 2, and a developer still can't tell which of the three sub-actions in step 2 was pivotal. Option four has the reasoning backwards - you often don't KNOW whether order matters until you've isolated each action, which is exactly why atomic steps are the safe default rather than something to add only after order is confirmed to matter.*

- **Repro steps — definition** — The numbered sequence of exact actions, from a stated starting point, that reliably triggers a reported defect - written so a stranger can reproduce it using only the written steps.
- **The atomic-step rule** — One discrete action per numbered step. A step joining two actions with 'and' or 'then' is a compression that can hide exactly the detail (order, an intermediate state) that turns out to matter.
- **Why specific values beat categories in a repro step** — 'A valid email' is a category; 'demo@example.com' is a value. If the specific value used affected whether the bug triggered, naming the category instead of the value throws away the information that made it reproduce.
- **Why steps should use the interface's OWN words** — 'Click Sign in' (the real button label) lets a developer find the exact control at a glance. A paraphrase like 'log in' or 'authenticate' forces them to guess which actual control was meant.
- **The safest habit for writing accurate steps** — Re-perform the bug ONE MORE TIME while writing the numbered list in real time, rather than reconstructing steps from memory afterward - memory smooths over exactly the details that matter.
- **How to handle a genuinely intermittent bug's repro steps** — State an honest reproduction RATE (e.g. '3/10 attempts') rather than either claiming false 100% reproducibility or giving up on steps entirely - a measured rate, especially compared across a varied condition, is real, useful investigative information.

### Challenge

Take the compressed, one-sentence bug description you wrote in the FirstTime exercise above. Rewrite
it as fully atomic, numbered steps with a stated starting point and specific values throughout. Then
deliberately try to reproduce your OWN bug using only the numbered steps you wrote, in a fresh session
if possible - if you get stuck or have to guess at any point, that's the exact step to sharpen. Run
the Python playground with your final steps and confirm it reports zero compressed steps.

### Ask the community

> I wrote these repro steps for a bug: `[paste your numbered steps]`. It reproduces for me but I'm not fully confident someone else could follow them without asking a question. Is there a step here that's still ambiguous or assumes something I haven't stated?

Asking someone to literally attempt your steps and narrate where they get stuck is far more useful
than asking "does this look clear?" - clarity is easy to assume and hard to self-assess honestly.

- [Marker.io — How to Write Steps to Reproduce a Bug (With Examples)](https://marker.io/blog/steps-to-reproduce-a-bug)
- [TestingXperts — Steps to Reproduce Bugs Accurately in QA Testing](https://www.testingxperts.com/technical-hub/steps-to-reproduce-bugs-accurately-in-qa-testing/)
- [Learn To Troubleshoot — How To Write Steps To Reproduce (STR) For Bugs?](https://www.youtube.com/watch?v=KbDLtLoVL7k)

🎬 [How To Write Steps To Reproduce (STR) For Bugs? — Learn To Troubleshoot](https://www.youtube.com/watch?v=KbDLtLoVL7k) (3 min)

- Repro steps are numbered, exact actions from a stated starting point - the single field most responsible for whether a valid bug gets fixed fast or bounces back Cannot Reproduce.
- One discrete action per step - a step joining actions with 'and' or 'then' is a compression that can hide exactly the detail (order, an intermediate state) that turns out to matter.
- Specific values, not categories, and the interface's own exact words, not a paraphrase - both let a stranger reproduce the bug without guessing what you meant.
- Write steps by re-performing the bug live, not from memory afterward - memory smooths over the details that turn out to be load-bearing.
- A genuinely intermittent bug still deserves honest, measured repro steps - a stated reproduction rate, especially compared across a varied condition, is real investigative information, not a shrug.


## Related notes

- [[Notes/defect-management/writing-bug-reports/anatomy-of-a-report|Anatomy of a report]]
- [[Notes/defect-management/writing-bug-reports/evidence|Evidence]]
- [[Notes/defect-management/writing-bug-reports/clarity|Clarity]]


---
_Source: `packages/curriculum/content/notes/defect-management/writing-bug-reports/repro-steps.mdx`_
