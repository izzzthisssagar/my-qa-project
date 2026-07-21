---
title: "When to escalate"
tags: ["your-first-90-days", "working-solo-the-mentor-gap", "track-c"]
updated: "2026-07-20"
---

# When to escalate

*Judgment for when a solo QA should hand a decision upward instead of deciding alone: security-adjacent findings, legal or compliance risk, anything affecting the release date, and severity disagreements that will not resolve.*

> Being the only QA means most calls are yours to make. A few are not, and confusing the two
> categories is its own kind of risk — deciding alone on something that needed another set of eyes, or
> escalating so often that nobody takes an actual escalation seriously anymore.

> **In real life**
>
> A bank teller can approve most transactions on their own judgment. But past a certain amount, or at
> the first sign of a suspicious pattern, policy requires a manager's sign-off — not because the teller
> is probably wrong, but because some categories of decision are never a single person's call, no
> matter how confident that person is.

**Escalation trigger**: An escalation trigger is a category of finding or disagreement - security-adjacent, legal or compliance-adjacent, anything affecting the release date, or an unresolved severity disagreement - where a solo QA should hand the decision upward rather than decide alone, regardless of personal confidence in the call.

## Findings that are never a solo call

Four categories sit outside a solo QA's own authority no matter how sure the read feels: anything
security-adjacent, anything legal or compliance-adjacent, anything that could affect the release
date, and a severity disagreement with a developer that genuinely is not resolving after a real
attempt. Each of these carries consequences — data exposure, regulatory exposure, missed
commitments, unresolved risk shipping quietly — that belong to more than one person's judgment.

## Escalating is not admitting failure

Raising a finding to someone with more authority is not a sign a solo QA could not handle it. It is
the correct handling of a category of risk that was never meant to be a single person's decision in
the first place. Treating escalation as a professional norm, not a last resort, is what keeps it
from feeling like a personal failure every time it happens.

## How to escalate without creating panic

> **Tip**
>
> Escalate with the same shape as a well-prepared question: what you found, why it matters, and what
> decision you need from the recipient. "Flagging this for a decision" reads as calm and professional;
> a message with no clear ask reads as an alarm with nowhere to go.

> **Common mistake**
>
> Do not sit on a security or compliance-adjacent finding to "confirm it more" before raising it —
> escalate with what you already have, and let someone with the right authority decide what happens
> next. The opposite mistake is just as real: escalating every minor disagreement dilutes escalation
> exactly when a real one needs to be taken seriously.

![A smiling bank teller sits behind a wooden counter, with a computer keyboard and mouse visible on the desk in the foreground](when-to-escalate.jpg)
*A bank teller serves a man at National Bank of Vanuatu on Malekula island — Department of Foreign Affairs and Trade (Australia), Wikimedia Commons, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:A_bank_teller_serves_a_man_at_National_Bank_of_Vanuatu_on_Malekula_island._(10661217924).jpg)*
- **A calm expression, not the deciding factor** — How confident or calm the teller looks has no bearing on whether a transaction needs sign-off. The trigger is the category of the decision, not how sure the person handling it feels.
- **The keyboard where the transaction is entered** — The system itself enforces certain thresholds automatically. A solo QA's own escalation triggers deserve the same fixed, non-negotiable status, agreed on before a finding ever appears.
- **The mouse, where a flagged case gets routed onward** — Some transactions get approved on the spot; others get routed up regardless of how routine they look. Escalation works the same way once the trigger is met.
- **The counter's edge, just past reach** — There is a real boundary to what one person at this counter can approve alone. A solo QA has the same boundary — real, even without a visible line drawn on a desk.

**Deciding whether to escalate**

1. **Check if it is security or compliance-adjacent** — If either applies, escalate immediately regardless of how confident you feel in your own read.
2. **Check if it affects the release date** — Flag it to whoever owns that decision, even if you are not certain of the exact impact yet.
3. **Check if a severity disagreement genuinely is not resolving** — After a real attempt to align, escalate the disagreement itself, framed neutrally rather than as blame.
4. **If none apply, decide and document it** — Make the call yourself, and write down the reasoning so it is defensible without a manager's sign-off.

*An escalation-decision classifier (Python)*

```python
findings = [
    {"desc": "password reset email leaks the reset token in a logged URL", "security": True, "compliance": False, "release_date": False, "unresolved_disagreement": False},
    {"desc": "a checkout button is misaligned by four pixels on Safari", "security": False, "compliance": False, "release_date": False, "unresolved_disagreement": False},
    {"desc": "export feature includes another tenant's rows under load", "security": False, "compliance": True, "release_date": False, "unresolved_disagreement": False},
    {"desc": "dev insists a data-loss bug is Low, tester insists Critical, unresolved after two rounds", "security": False, "compliance": False, "release_date": False, "unresolved_disagreement": True},
]
def classify(f):
    if f["security"] or f["compliance"] or f["release_date"] or f["unresolved_disagreement"]:
        return "ESCALATE"
    return "DECIDE_SOLO"
escalate_count = 0
for f in findings:
    verdict = classify(f)
    print(verdict)
    if verdict == "ESCALATE":
        escalate_count += 1
print("ESCALATE_COUNT=" + str(escalate_count))
result = "MATCHES_EXPECTED" if escalate_count == 3 else "MISMATCH"
assert result == "MATCHES_EXPECTED", "expected exactly three escalation cases in this sample"
print("RESULT=" + result)
```

*An escalation-decision classifier (Java)*

```java
public class Main {
    static String classify(boolean security, boolean compliance, boolean releaseDate, boolean unresolvedDisagreement) {
        if (security || compliance || releaseDate || unresolvedDisagreement) return "ESCALATE";
        return "DECIDE_SOLO";
    }
    public static void main(String[] args) {
        boolean[][] findings = {
            {true, false, false, false},
            {false, false, false, false},
            {false, true, false, false},
            {false, false, false, true},
        };
        int escalateCount = 0;
        for (boolean[] f : findings) {
            String verdict = classify(f[0], f[1], f[2], f[3]);
            System.out.println(verdict);
            if (verdict.equals("ESCALATE")) escalateCount++;
        }
        System.out.println("ESCALATE_COUNT=" + escalateCount);
        String result = escalateCount == 3 ? "MATCHES_EXPECTED" : "MISMATCH";
        if (!result.equals("MATCHES_EXPECTED")) throw new AssertionError("expected exactly three escalation cases in this sample");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Know your escalation triggers before you need them

- [ ] Learn who owns security-adjacent findings before you find one — Confirm the actual contact or process in advance, not in the middle of an incident.
- [ ] Learn who owns legal or compliance-adjacent findings — This is often not the same person as the security contact - confirm both separately.
- [ ] Agree in advance on how release-date-affecting findings get raised — Know the channel and the expected notice period before a real one comes up.
- [ ] Set a real limit for severity disagreements — Decide in advance how many rounds of discussion happen before a disagreement gets escalated rather than left unresolved.

- **You found something security-adjacent and are tempted to confirm it further first.**
  Escalate now with what you have; further confirmation can happen once someone with the right authority is already aware.
- **A severity disagreement with a developer has gone two rounds with no resolution.**
  Escalate the disagreement itself, framed neutrally as a decision needed, rather than letting it stall silently.
- **You are escalating routine findings out of caution.**
  Reserve escalation for the four real triggers, or it loses its weight exactly when a genuine one needs to be taken seriously.

### Where to check

- Your company's actual security incident and compliance reporting contacts, confirmed in advance.
- Recent severity disagreements and how many rounds each took before resolving or getting escalated.
- Whether a release-date-affecting finding has a known, agreed channel to go through.
- [[your-first-90-days/working-solo-the-mentor-gap/being-the-only-qa]] for why having no peer to confirm a call makes these triggers matter even more.
- [[your-first-90-days/landing-well/your-first-bug-report-at-work]] for the baseline reporting habits an escalation builds on.

### Worked example: the finding that could not wait for more confirmation

1. A solo QA notices a password-reset email includes the reset token directly in a URL that also gets written to an access log.
2. Her first instinct is to spend another hour confirming exactly how exploitable it is before telling anyone.
3. She recognizes this is security-adjacent by definition, escalates immediately with what she has, and flags it as unconfirmed severity but confirmed exposure.
4. The security-aware engineer on call decides the token needs to be removed from logging that same day, a decision that was never going to be hers alone to make.

**Quiz.** Which finding should a solo QA escalate rather than decide on alone?

- [ ] A checkout button misaligned by four pixels in one browser
- [x] A password-reset token that is being written into an access log
- [ ] A typo in a tooltip on an internal admin page
- [ ] A test case that needs an extra assertion added

*A finding that is security-adjacent always crosses the escalation threshold, regardless of how confident the person who found it feels about their own read of its severity.*

- **Escalation trigger** — Security-adjacent, legal or compliance-adjacent, release-date-affecting, or an unresolved severity disagreement - categories that go up regardless of personal confidence in the call.
- **Escalation is not failure** — Raising a finding that meets a real trigger is correct handling of shared risk, not evidence a solo QA could not handle it alone.
- **Escalating without panic** — State what you found, why it matters, and what decision you need - the same shape as a well-prepared question.

### Challenge

Write down your own company's actual contact or process for security-adjacent and compliance-adjacent findings today, before you ever need it during an actual incident.

- [Indeed — When Should You Escalate an Issue at Work?](https://www.indeed.com/career-advice/career-development/escalate-the-issue)
- [Nulab — How to Escalate an Issue Without Causing Havoc](https://nulab.com/learn/project-management/escalate-the-issue/)
- [Stay Out of Trouble at Work: How to Escalate](https://www.youtube.com/watch?v=trq9f2L8BYM)

🎬 [Stay out of trouble at work | HOW TO ESCALATE](https://www.youtube.com/watch?v=trq9f2L8BYM) (16 min)

- Four categories are never a solo call: security-adjacent, legal or compliance-adjacent, release-date-affecting, and unresolved severity disagreements.
- Escalating a finding that meets a real trigger is correct handling of shared risk, not a personal failure.
- Escalate with a clear ask - what you found, why it matters, what decision you need - not just an alarm.
- Reserve escalation for real triggers, or it loses its weight exactly when a genuine one needs attention.


## Related notes

- [[Notes/your-first-90-days/working-solo-the-mentor-gap/being-the-only-qa|Being the only QA]]
- [[Notes/your-first-90-days/working-solo-the-mentor-gap/asking-good-questions|Asking good questions]]
- [[Notes/your-first-90-days/working-solo-the-mentor-gap/using-the-community|Using the community]]
- [[Notes/your-first-90-days/landing-well/your-first-bug-report-at-work|Your first bug report at work]]


---
_Source: `packages/curriculum/content/notes/your-first-90-days/working-solo-the-mentor-gap/when-to-escalate.mdx`_
