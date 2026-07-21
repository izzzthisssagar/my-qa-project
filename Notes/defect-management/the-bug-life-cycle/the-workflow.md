---
title: "The workflow"
tags: ["defect-management", "the-bug-life-cycle", "track-c"]
updated: "2026-07-16"
---

# The workflow

*The bug life cycle as a directed graph: which role can move a defect from which state to which next state, why almost every arrow points forward, and why Reopened is the one deliberate arrow that points back.*

> The previous note named the states. This one answers the question that actually matters day to day:
> who is *allowed* to move a bug from one state to the next, and in which direction? A tracker isn't
> just a list of labels — it's a small rulebook. A tester can move New to Confirmed but usually can't
> move Assigned to Fixed (that's not their claim to make). A developer can mark something Fixed but
> can't mark it Verified (that would mean grading their own work). The workflow is the *shape* those
> rules draw — and once you can see the shape, "whose move is it" stops being a mystery.

> **In real life**
>
> Watch a real letter-sorting facility for five minutes: a single conveyor carries every piece of mail
> past a barcode scanner, which routes each one — automatically, based on a rule, not a guess — into
> exactly one of dozens of destination bins. Almost everything that enters keeps moving *forward*
> toward a bin and stays there. Only a small, deliberate fraction gets pulled back onto the belt for a
> second pass, because a human noticed something the automated read got wrong. A bug workflow is that
> same conveyor: most tickets move forward through a small number of stations, routed by a rule (who
> owns this step), and only a specific, named event — Reopened — deliberately sends one back for
> another pass.

**workflow**: A workflow, in defect management, is the directed graph of a tracker's states plus the specific transitions allowed between them and the role permitted to make each move. Nodes are the states from the previous note (New, Confirmed, Assigned, In Progress, Fixed, Retest, Verified/Closed, plus the exit ramps); edges are the allowed moves (e.g. Fixed to Retest, but never Fixed directly to Closed). Most real trackers enforce this graph in software - a status dropdown only shows the states reachable from the current one, for the roles allowed to move it.

## Who owns each move

- **New → Confirmed**: a lead or triager, not the original reporter. Letting the reporter confirm
  their own bug removes the independent second look that makes "Confirmed" mean anything.
- **Confirmed → Assigned**: usually a lead, sometimes automatic (round-robin, or ownership by
  component). Either way, this move names one accountable person.
- **Assigned → In Progress → Fixed**: the assigned developer, and only that developer. This is their
  claim, and their claim alone — nobody else can honestly assert the code changed.
- **Fixed → Pending Retest**: often automatic, triggered by the fix landing in a build the tester can
  reach — a system event, not a person's judgment call.
- **Pending Retest → Retest → Verified/Closed**: the tester, and specifically *not* the developer who
  fixed it. This is the independent check the whole cycle exists to guarantee.
- **Reopened**: the tester, from Verified/Closed (or sometimes directly from Fixed) back to Assigned
  or In Progress. This is the one transition that legitimately points backward.

> **Common mistake**
>
> Letting the same person make two moves that are supposed to check each other — most commonly, a
> developer marking their own fix Verified because "I tested it before I pushed." That's not a
> workflow violation most trackers block technically (many tools don't enforce role-per-transition),
> but it defeats the entire *purpose* of having a Retest step: an independent party checking a claim.
> If your tracker allows it and your team does it, the workflow diagram is decorative — say so out
> loud before a release, not after one ships with a bug the developer "definitely tested."

![Overhead view of a long automated letter-sorting conveyor in an industrial mail center, with rows of numbered destination compartments along both sides, blue control-panel displays, overhead cable bundles, and a worker standing at a monitoring station partway down the line](the-workflow.jpg)
*Briefzentrum Härkingen automated sorting — Wikimedia Commons, CC0 (Hadi). [Source](https://commons.wikimedia.org/wiki/File:Briefzentrum_H%C3%A4rkingen_11.jpg)*
- **One entry point — every bug starts as New** — Every piece of mail enters this system from the same single point at the top of the line, no matter its final destination. Every bug, regardless of how it ends up, starts at exactly one state: New.
- **The barcode read — an automatic routing decision** — A scanner reads each piece and routes it by RULE, not by guessing - the same way a Confirmed-to-Assigned move should follow a rule (component ownership, round robin) rather than whoever happens to be free.
- **The worker at the monitoring station — the one manual override point** — Almost the whole line runs unattended; a person stands at just one control point to catch and correct the rare misroute. This is the workflow's Reopened move: the one place a human deliberately pulls something back onto the belt for another pass.
- **Rows of destination bins — the states a bug can land in** — Dozens of separate compartments, each one a specific destination reachable only via the routing decision upstream - exactly like a bug reaching Fixed, Duplicate, or Deferred only via its own specific, named transition, never by skipping straight there.
- **Bins filling at different rates** — Some compartments fill fast, others stay nearly empty during this stretch - the same uneven picture a workflow dashboard shows: most tickets clustered in a couple of active states, a few rare paths barely used.

**The workflow graph — who moves what, and the one backward edge**

1. **New → Confirmed** — Lead's move. Independent of the reporter — confirms the bug is real without trusting the reporter's own judgment of that.
2. **Confirmed → Assigned** — Lead's move (or automatic by rule). Names exactly one accountable developer.
3. **Assigned → Fixed** — Developer's move, and only the developer's. Their claim that the code changed.
4. **Fixed → Retest → Verified/Closed** — Tester's move. The independent check — never the same person who claimed Fixed.
5. **Verified/Closed → Reopened** — Tester's move, backward. The one deliberate exception: verification caught something the Fixed claim missed.

A workflow is really just a set of allowed `(from_state, role) → to_state` rules. Here's a tiny
checker that enforces exactly that — given a transition someone is trying to make, it says whether
that role is allowed to make that specific move right now, the same logic a real tracker runs before
it lets you change a status dropdown.

*Run it - check whether a role can make a given workflow transition (Python)*

```python
# (from_state, role) -> set of allowed next states
WORKFLOW = {
    ("New", "lead"): {"Confirmed", "Rejected", "Duplicate"},
    ("Confirmed", "lead"): {"Assigned"},
    ("Assigned", "developer"): {"In Progress"},
    ("In Progress", "developer"): {"Fixed", "Deferred"},
    ("Fixed", "system"): {"Pending Retest"},
    ("Pending Retest", "tester"): {"Retest"},
    ("Retest", "tester"): {"Verified", "Reopened"},
    ("Verified", "tester"): {"Closed", "Reopened"},
}

def try_transition(current_state, role, target_state):
    allowed = WORKFLOW.get((current_state, role), set())
    if target_state in allowed:
        return True, f"OK: {role} may move {current_state} -> {target_state}"
    return False, f"BLOCKED: {role} may NOT move {current_state} -> {target_state}"

attempts = [
    ("New", "lead", "Confirmed"),
    ("Assigned", "developer", "Fixed"),          # skips In Progress - should block
    ("Fixed", "developer", "Verified"),           # developer verifying own fix - should block
    ("Verified", "tester", "Reopened"),
    ("Retest", "tester", "Closed"),                # must go through Verified first - should block
]

for current, role, target in attempts:
    ok, message = try_transition(current, role, target)
    print(message)

# OK: lead may move New -> Confirmed
# BLOCKED: developer may NOT move Assigned -> Fixed
# BLOCKED: developer may NOT move Fixed -> Verified
# OK: tester may move Verified -> Reopened
# BLOCKED: tester may NOT move Retest -> Closed
```

Same rule table in Java, as a real tracker's backend might enforce it before accepting a status change:

*Run it - check whether a role can make a given workflow transition (Java)*

```java
import java.util.*;

public class Main {
    record Move(String state, String role) {}

    public static void main(String[] args) {
        Map<Move, Set<String>> workflow = new HashMap<>();
        workflow.put(new Move("New", "lead"), Set.of("Confirmed", "Rejected", "Duplicate"));
        workflow.put(new Move("Confirmed", "lead"), Set.of("Assigned"));
        workflow.put(new Move("Assigned", "developer"), Set.of("In Progress"));
        workflow.put(new Move("In Progress", "developer"), Set.of("Fixed", "Deferred"));
        workflow.put(new Move("Fixed", "system"), Set.of("Pending Retest"));
        workflow.put(new Move("Pending Retest", "tester"), Set.of("Retest"));
        workflow.put(new Move("Retest", "tester"), Set.of("Verified", "Reopened"));
        workflow.put(new Move("Verified", "tester"), Set.of("Closed", "Reopened"));

        List<Object[]> attempts = List.of(
            new Object[]{"New", "lead", "Confirmed"},
            new Object[]{"Assigned", "developer", "Fixed"},
            new Object[]{"Fixed", "developer", "Verified"},
            new Object[]{"Verified", "tester", "Reopened"},
            new Object[]{"Retest", "tester", "Closed"}
        );

        for (Object[] attempt : attempts) {
            String current = (String) attempt[0];
            String role = (String) attempt[1];
            String target = (String) attempt[2];
            Set<String> allowed = workflow.getOrDefault(new Move(current, role), Set.of());
            if (allowed.contains(target)) {
                System.out.println("OK: " + role + " may move " + current + " -> " + target);
            } else {
                System.out.println("BLOCKED: " + role + " may NOT move " + current + " -> " + target);
            }
        }
    }
}

/* OK: lead may move New -> Confirmed
   BLOCKED: developer may NOT move Assigned -> Fixed
   BLOCKED: developer may NOT move Fixed -> Verified
   OK: tester may move Verified -> Reopened
   BLOCKED: tester may NOT move Retest -> Closed */
```

### Your first time: Your mission: draw your own team's workflow, then break it on purpose

- [ ] List every status your tracker allows, and for five real tickets, note who made each transition — Look at the history log from the previous note's exercise. Write down: from state, to state, who (role, not name).
- [ ] Try to find one transition your tracker technically ALLOWS but your team treats as against the rules — The most common one: a developer closing their own bug without a separate tester verification step. If you find one, that's a real workflow gap worth raising, not a personal failing of whoever did it.
- [ ] Run the Python playground and add one new rule for a transition your team actually uses that isn't in the table — Maybe your team allows a lead to reopen directly, or has an extra 'Code Review' state between In Progress and Fixed. Add it and confirm the checker still blocks the moves it should.
- [ ] Ask a teammate: 'who is allowed to verify a fix?' — If the honest answer is 'whoever's free,' that's worth raising - verification only means something if it's independent of whoever claimed Fixed.

You now have your own team's actual rulebook written down, including the one gap most teams have
somewhere and rarely name out loud.

- **A ticket jumps straight from Assigned to Closed with no Fixed or Retest in between.**
  Check the history log for who made the move and what the comment says. This usually means either the tracker's workflow enforcement is missing (anyone can set any status) or the ticket was closed as a mistake/duplicate rather than actually fixed - the jump itself is the tell that something skipped the independent-check step, whatever the reason turns out to be.
- **Two different tickets show the exact same transition made by two different roles - once by a lead, once by a developer - and you're not sure which is 'correct.'**
  Check whether your tracker has an explicit written workflow policy (many teams document this in a wiki page or the tool's own workflow configuration screen). If it's undocumented, that's the actual problem to raise - an inconsistently enforced workflow is worse than a strict one, because two people can both be following 'the rules' and land on different results.
- **You're blocked from making a status change the tracker's UI simply doesn't offer as an option.**
  That's the workflow graph enforcing itself - the tool is telling you that transition isn't a valid edge from the current state for your role. Before working around it (some tools allow admins to force a status), ask why the edge doesn't exist; it's very often protecting the exact independent-check separation this note is about.
- **A bug gets reopened repeatedly by different testers, and nobody can tell if it's the SAME failure recurring or a new one each time.**
  Read each reopening comment specifically for the repro steps used, not just the fact that it was reopened. If the steps differ each time, you may actually have multiple distinct bugs sharing one ticket, which should probably be split - the workflow's Reopened edge assumes it's the same defect coming back, not a new one wearing the old ticket's ID.

### Where to check

The workflow itself usually isn't hidden — most trackers let you inspect it directly:

- **The tracker's workflow/scheme configuration screen** — Jira calls it a "workflow scheme," Azure DevOps a "process template." Admin access usually isn't required just to *view* it, only to edit it.
- **A ticket's available status dropdown, at its current state** — the options shown ARE the graph's outgoing edges from wherever it sits right now. If "Closed" isn't in the dropdown from "Assigned," that edge doesn't exist.
- **The activity/history log** (same place as the previous note) — cross-reference who made each move against the role rules to spot workflow violations after the fact.
- **A team wiki or onboarding doc**, if one exists — teams that have been burned by workflow confusion before often write the role rules down explicitly, separate from the tool's own configuration.

### Worked example: a workflow-role violation almost slips through a release

1. A developer fixes a checkout bug late Friday, marks it Fixed, and — because the tester is out —
   also clicks through Pending Retest and Verified themselves "just to keep things moving," closing
   the ticket.
2. Monday, the QA lead reviews the release's closed-ticket list before sign-off and notices the
   history log: the same person made the Fixed AND Verified moves, with a four-minute gap between
   them.
3. The lead doesn't assume malice — flags it as a workflow gap: "this ticket has no independent
   verification," and reopens it for a real retest, citing the workflow rule directly rather than
   distrust of the developer's work.
4. The actual tester runs the original repro steps Monday morning and finds the fix only handled the
   common case — a specific discount-code combination still triggers the original bug.
5. Reopened again, fixed properly, verified by the tester this time, closed for real — caught not by
   distrusting the developer, but by the workflow's own rule (independent verification) doing exactly
   the job it exists to do.

**Quiz.** A tracker's workflow configuration technically allows a developer to move a ticket directly from 'In Progress' to 'Verified,' skipping the tester entirely. What's the most accurate way to describe this situation?

- [ ] It's fine, since the tracker software allows it - if it were a real problem, the tool would block it
- [x] A configuration gap - the tool ALLOWS a transition that removes the independent check the workflow exists to guarantee, and it's worth fixing the configuration or the team's practice explicitly
- [ ] It only matters if the developer actually makes that exact move - as long as nobody does it, the allowed transition is harmless
- [ ] This is a sign the whole tracker is misconfigured and should be replaced

*A tool ALLOWING a transition is a technical fact about its configuration, not a judgment about whether that transition is a good idea - trackers are frequently configured more permissively than a team's actual practice, and this note's whole point is that the workflow's VALUE comes from the independent-check separation, not from the software enforcing it. Option one wrongly assumes the tool's permissiveness is evidence of safety. Option three is the most tempting wrong answer - it's true that an unused allowed transition causes no immediate harm, but 'as long as nobody does it' is not a plan; the option existing means it eventually WILL get used under deadline pressure, which is exactly when the independent check matters most. Option four overreacts - a single missing constraint doesn't mean the whole tool is broken, just that this one part of its configuration doesn't match the team's actual intended workflow yet.*

- **Workflow (defect management)** — The directed graph of a tracker's states plus the specific transitions allowed between them and the role permitted to make each move.
- **Why New→Confirmed isn't the reporter's own move** — Letting the reporter confirm their own bug removes the independent second look that makes 'Confirmed' mean anything distinct from 'reported.'
- **Why Fixed→Verified isn't the developer's own move** — It would mean grading your own work - the entire value of a Retest/Verified step is that it's an independent check by someone with no stake in the fix already being correct.
- **The one backward edge in a healthy workflow** — Reopened - moved by the tester, from Verified/Closed (or Fixed) back to Assigned/In Progress, when verification catches something the Fixed claim missed. Every other edge points forward.
- **How to check if your tracker enforces role-per-transition** — Look at the status dropdown available from a ticket's CURRENT state - the options shown are the graph's actual outgoing edges. If a transition that should require a different role is still offered, that's a configuration gap, not a safe unused option.
- **A workflow-role violation that 'seems fine because nothing broke yet'** — Still a real gap. An unused permissive transition tends to get used exactly once, under deadline pressure - which is precisely when the independent check it removes matters most.

### Challenge

Pull up your own tracker's workflow configuration screen (or ask an admin to show you, if you don't
have access). Draw it as a simple diagram: one box per state, one arrow per allowed transition,
labeled with which role can make it. Circle any arrow that lets the SAME role make two moves that are
supposed to check each other (e.g. the same person marking Fixed and Verified). Then open the Python
playground above and add your tracker's real rules to the WORKFLOW dictionary, replacing the example
ones, and confirm the checker correctly blocks the same gap you circled by hand.

### Ask the community

> I looked at our tracker's workflow configuration and found `[describe the transition]` is technically allowed for `[role]`, which seems to skip the independent check that `[the other role]` is supposed to provide. Is this a real gap worth raising, or is there a reason teams sometimes configure it this way on purpose?

Some teams DO intentionally relax this for very low-risk changes (a typo fix, a copy change with no
logic) - the useful follow-up question is whether the relaxed rule is scoped narrowly to genuinely
low-risk tickets, or just left wide open for everything out of convenience.

- [Guru99 — Defect/Bug Life Cycle (workflow diagram and states)](https://www.guru99.com/defect-life-cycle.html)
- [Atlassian — Jira workflow guide (how a real tool models this exact graph)](https://www.atlassian.com/software/jira/guides/issues/workflows)
- [The Testing Academy — Bug Life Cycle / Defect Life Cycle (LIVE example in Jira)](https://www.youtube.com/watch?v=j7cty0x9518)

🎬 [Bug Life Cycle / Defect Life Cycle In Software Testing — LIVE Example in Jira — The Testing Academy](https://www.youtube.com/watch?v=j7cty0x9518) (6 min)

- A workflow is the directed graph of allowed (state, role) -> next-state moves - not just the list of state names from the previous note.
- Each forward move exists to separate claims from checks: a lead confirms independently of the reporter, a developer claims Fixed, a tester independently verifies - the same person should never make both halves of a check.
- Reopened is the one legitimate backward edge - it means verification worked, not that someone made a mistake.
- A tracker ALLOWING a transition is not the same as a team's practice endorsing it - an unused permissive edge tends to get used exactly once, under deadline pressure.
- You can inspect your own team's real workflow directly: the status dropdown at a ticket's current state shows its actual outgoing edges, and the history log shows who has actually been using them.


## Related notes

- [[Notes/defect-management/the-bug-life-cycle/states-of-a-bug|States of a bug]]
- [[Notes/defect-management/the-bug-life-cycle/triage|Triage]]
- [[Notes/defect-management/severity-vs-priority/who-sets-what|Who sets what]]


---
_Source: `packages/curriculum/content/notes/defect-management/the-bug-life-cycle/the-workflow.mdx`_
