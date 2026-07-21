---
title: "Status updates"
tags: ["test-management-and-reporting", "docs-and-communication", "track-c"]
updated: "2026-07-21"
---

# Status updates

*A relay runner hands off the baton, not a recap of the whole race so far - the receiver already knows everything up to this point. A status update that re-explains the full backstory every time is dropping the baton before the exchange even happens.*

> "We spent the week working on the checkout regression suite" describes an activity. "The checkout
> regression suite is done and running in CI as of Tuesday" describes an outcome - and only the second
> one tells a reader anything they can actually act on. A status update exists to report what changed,
> not to narrate the effort that went into changing it, and the gap between those two things is the
> entire skill this note is about.

> **In real life**
>
> A relay runner extends the baton toward a teammate who is already running, already knows exactly how
> the race has gone so far, and needs precisely one thing from this handoff: the baton itself, in a
> grip they can immediately keep moving with. Nobody stops to recap the first three legs of the race
> mid-exchange - the receiver already has that context, and repeating it would only cost both runners
> their momentum. A status update works exactly the same way: the reader already has the shared
> context, and the update's only job is handing over what changed since the last one, cleanly, without
> either party having to slow down.

**A status update**: A status update is a short, frequent communication - a standup, a written weekly note, a ticket comment - that reports what changed since the last update, current blockers, and next steps, assuming shared context with the reader rather than re-explaining the full history each time.

## The structure that survives a five-second read

State the overall status first, in one plain-language word or phrase - on track, at risk, or blocked -
so anyone can grasp the situation before reading a single further word. Follow with the classic
three-part structure: what got done (an outcome, not an activity), what's happening now, and what's
blocking progress if anything is. "Done" means a completed, verifiable outcome - "regression suite
passing in CI" - not a description of effort like "worked on the regression suite," which tells a
reader nothing about whether the work is actually finished.

## Cut anything that wouldn't change what the reader does or thinks

The single sharpest filter for a status update: if a line would not change what anyone does or thinks
after reading it, cut the line. A blocker needs to name the specific dependency or decision it's
waiting on and, ideally, a suggested next step - "blocked, waiting on API access" is more useful than
just "blocked," and "blocked on API access, need someone with admin rights to grant it by Thursday" is
more useful still. Written, asynchronous status updates (a ticket comment, a Slack message) can afford
slightly more precision than a verbal standup, since there's no chance for an instant follow-up
question - but the brevity discipline still holds. More detail belongs in a linked ticket or report,
never inline in the update itself.

> **Tip**
>
> Name the specific owner and expected date for any next step, never a vague closer like "will continue
> next week." A next step with no owner or date gives a reader nothing to act on or check back against.

> **Common mistake**
>
> Writing a status update that reads like a mini technical report - full context, background,
> methodology - defeating the entire purpose of a format meant to be skimmed in seconds. If a reader
> needs that depth, link to the full report or doc; don't inline it into every update.

![Two relay race runners exchanging a baton mid-stride on a grass field, one extending the baton and the other reaching to receive it](status-updates.jpg)
*Relay race baton pass — Patrick Bell, CC BY 2.0, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Relay_race_baton_pass.jpg)*
- **The baton, extended - status handed off, nothing more** — One clean object passed - not the entire race recapped mid-handoff. A status update carries exactly this much: current state, handed over cleanly, not a replay of everything that happened to get here.
- **The open hand, already anticipating the exchange** — The receiver doesn't need the full backstory - just the baton, right now, in a form they can immediately keep running with. A good status update assumes shared context and reports only what's new.
- **Legs still mid-stride, never fully stopping** — The exchange happens without either runner coming to a halt. A status update works best the same way - brief enough not to break anyone's actual momentum on the work itself.
- **Everything behind them, out of frame** — The earlier legs of the race don't get re-run here - already done, no need to repeat them. A status update reports what changed since the last one, not the entire history again.

**Building one skimmable status update**

1. **State overall status first: on track, at risk, or blocked** — One word or phrase, grasped in under five seconds, before any supporting detail.
2. **Report an outcome for what's done, not an activity** — "Regression suite passing in CI" tells a reader something; "worked on the regression suite" tells them nothing checkable.
3. **Name any blocker specifically, with a next step** — The exact dependency or decision waited on, and ideally what would resolve it.
4. **Cut every line that wouldn't change what the reader does or thinks** — The sharpest filter for keeping an update genuinely skimmable instead of a mini report in disguise.

*Auditing a status update against the outcome-vs-activity filter (Python)*

```python
ACTIVITY_VERBS = ["worked on", "looked into", "spent time on", "continued", "started looking at"]

updates = [
    "Worked on the checkout regression suite this week.",
    "Checkout regression suite is done, passing in CI as of Tuesday. Next: extend to the mobile flow, owner Priya, due Friday.",
]

for u in updates:
    lower = u.lower()
    is_activity = any(v in lower for v in ACTIVITY_VERBS)
    has_next_step_owner = "owner" in lower or ("due" in lower)
    print("Update: " + u)
    if is_activity:
        print("  FLAG: describes activity, not a verifiable outcome")
    if not has_next_step_owner:
        print("  FLAG: no named owner/date for next step")
    if not is_activity and has_next_step_owner:
        print("  OK: outcome-based, with an actionable next step")
    print("")
```

*Auditing a status update against the outcome-vs-activity filter (Java)*

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> activityVerbs = Arrays.asList(
                "worked on", "looked into", "spent time on", "continued", "started looking at");

        List<String> updates = Arrays.asList(
                "Worked on the checkout regression suite this week.",
                "Checkout regression suite is done, passing in CI as of Tuesday. Next: extend to the mobile flow, owner Priya, due Friday."
        );

        for (String u : updates) {
            String lower = u.toLowerCase();
            boolean isActivity = activityVerbs.stream().anyMatch(lower::contains);
            boolean hasNextStepOwner = lower.contains("owner") || lower.contains("due");

            System.out.println("Update: " + u);
            if (isActivity) {
                System.out.println("  FLAG: describes activity, not a verifiable outcome");
            }
            if (!hasNextStepOwner) {
                System.out.println("  FLAG: no named owner/date for next step");
            }
            if (!isActivity && hasNextStepOwner) {
                System.out.println("  OK: outcome-based, with an actionable next step");
            }
            System.out.println();
        }
    }
}
```

### Your first time: Rewrite one real status update

- [ ] Find a status update you wrote recently - a standup note, a ticket comment, a weekly summary — Something written quickly, in the actual flow of work.
- [ ] Check the opening line for a clear on-track/at-risk/blocked statement — If it's not there or not obvious in five seconds, add it first.
- [ ] Replace every activity description with a verifiable outcome — "Worked on X" becomes "X is done/passing/live as of [date]" or an honest "X is not yet done, currently at [specific state]."
- [ ] Add a named owner and date to any next step or blocker — Confirm a reader would know exactly who to check with and by when.

- **Stakeholders keep asking follow-up questions after every status update, even though it seemed complete.**
  Check whether it reported outcomes or just activities - 'worked on X' invites 'is it done?' every single time, while a stated outcome pre-answers that question.
- **A status update takes several minutes to read and loses the reader's attention halfway through.**
  It has likely turned into a mini report - apply the cut-test line by line, and move any detail someone might still want into a linked doc instead of inline.
- **A blocker sits unresolved for days because nobody realized it needed a specific action from them.**
  The blocker was probably stated vaguely ('blocked') rather than naming the specific dependency and who could resolve it - rewrite with both named explicitly.

### Where to check

- Any status update about to be sent, checked against the cut-test: would this specific line change what the reader does or thinks?
- Every "done" claim in a recent update, confirmed to describe a verifiable outcome rather than just effort spent.
- [[test-management-and-reporting/docs-and-communication/async-communication]] for how this same brevity discipline extends to longer-running written conversations, not just periodic updates.
- [[test-management-and-reporting/docs-and-communication/writing-for-developers]] for the precision standard a status update's technical details, if any, should meet.
- [[test-management-and-reporting/metrics-and-reporting/test-summary-reports]] for the full-depth document a status update should link to rather than try to replace.

### Worked example: a blocker that sat for a week because of one missing word

1. A tester posts a standup update: "Blocked on the payment gateway sandbox - can't run the checkout
   suite."
2. Nobody on the team knows whose job it is to unblock a sandbox access issue, so the note sits
   unanswered for six days while the tester quietly waits, assuming someone will eventually notice.
3. A manager finally asks directly what's needed, and learns the fix is a two-minute permissions grant
   that any team lead could have done immediately if they had known they were the one being asked.
4. The update is rewritten going forward with the missing piece included: "Blocked on payment gateway
   sandbox access - need a team lead to grant sandbox permissions in the admin console, blocking the
   checkout suite until resolved."
5. The same kind of blocker, reported with the specific action and an implicit call to whoever can act
   on it, gets resolved within the hour the very next time it comes up.

**Quiz.** What does this note identify as the sharpest filter for keeping a status update genuinely useful rather than a mini report in disguise?

- [ ] Keeping every update under 100 words regardless of content
- [x] Cutting any line that would not change what the reader does or thinks after reading it - the update should report outcomes and actionable blockers, not background or effort description
- [ ] Never including any technical detail in a status update
- [ ] Sending status updates only once a week instead of daily

*Length alone isn't the real test - a short update can still be useless if it's vague, and a slightly longer one can be exactly right if every line earns its place. The actual filter is whether each line changes what the reader does or thinks: an outcome, a specific blocker with an owner, a dated next step all pass; a description of effort or unnecessary background does not.*

- **A status update** — A short, frequent communication reporting what changed since the last update, current blockers, and next steps - assuming shared context rather than re-explaining the full history each time.
- **Outcome vs. activity** — "Regression suite passing in CI" is a verifiable outcome; "worked on the regression suite" is an activity description that tells a reader nothing about whether the work is actually done.
- **The cut-test for status updates** — If a line would not change what anyone does or thinks after reading it, cut it - the sharpest filter for keeping an update skimmable instead of a disguised mini report.
- **Why a blocker needs a named owner and next step** — "Blocked" alone gives a reader nothing to act on - naming the specific dependency and who could resolve it turns a stalled update into something someone can actually pick up.

### Challenge

Rewrite one recent status update you wrote: add a clear on-track/at-risk/blocked opener, replace every activity description with a verifiable outcome, and add a named owner and date to any next step or blocker.

- [Write Status Updates That Don't Waste Time](https://willowvoice.com/blog/how-to-write-internal-status-updates)
- [Atlassian — What Is a Standup Meeting & Tips to Run One](https://www.atlassian.com/agile/scrum/standups)
- [Daily Stand-up: You're Doing It Wrong!](https://www.youtube.com/watch?v=H02BlTXpcto)

🎬 [Daily Stand-up: You're Doing It Wrong!](https://www.youtube.com/watch?v=H02BlTXpcto) (7 min)

- A status update assumes shared context and reports only what changed - not a full recap of the project's history, the same way a relay handoff never re-runs the earlier legs of the race.
- State overall status first (on track, at risk, blocked) in one phrase graspable in under five seconds.
- Report outcomes, not activities - 'done and passing in CI' tells a reader something; 'worked on it' does not.
- Every blocker needs the specific dependency named and, ideally, who could resolve it - 'blocked' alone gives nobody anything to act on.
- The sharpest filter: if a line wouldn't change what the reader does or thinks, cut it - more depth belongs in a linked report, never inline in the update.


## Related notes

- [[Notes/test-management-and-reporting/docs-and-communication/async-communication|Async communication]]
- [[Notes/test-management-and-reporting/docs-and-communication/writing-for-developers|Writing for developers]]
- [[Notes/test-management-and-reporting/metrics-and-reporting/test-summary-reports|Test summary reports]]


---
_Source: `packages/curriculum/content/notes/test-management-and-reporting/docs-and-communication/status-updates.mdx`_
