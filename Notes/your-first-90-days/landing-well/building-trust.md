---
title: "Building trust"
tags: ["your-first-90-days", "landing-well", "track-c"]
updated: "2026-07-20"
---

# Building trust

*Concrete trust-building behaviors for a new QA: following through on small commitments, asking good questions instead of pretending to know, giving credit, and staying consistent about severity and priority calls.*

> Nobody hands a new QA a document that says "the team trusts you now." It accumulates quietly, one
> small kept promise and one calibrated severity call at a time, and it can just as quietly drain away
> the first time someone catches an inconsistency they were not expecting.

> **In real life**
>
> A beach lifeguard does not earn the head guard's trust with one dramatic rescue. It comes from weeks
> of correct, boring calls: scanning the same water the same careful way, calling a swimmer back at the
> same distance every time, never once needing someone else to check behind them. The dramatic save, if
> it ever comes, only works because the boring calls were already trusted.

**Trust capital**: Trust capital is the accumulated confidence a team places in a person's judgment, built through small, consistent, verifiable actions over time rather than through any single impressive act. It determines how much a person's calls get double-checked, and it can be spent down quickly by even one visible inconsistency.

## Small commitments, kept consistently

Trust is built less by grand gestures and more by whether the small things you said you would do
actually happened. If you tell someone you will retest a fix by Thursday, retest it by Thursday. If
you cannot, say so before the deadline, not after someone asks. Each kept commitment is a small,
specific data point a colleague uses to decide how much to rely on you next time.

## Ask rather than pretend, and calibrate rather than guess

Nobody expects a new QA to already know everything. What erodes trust fast is pretending to know
something you do not, because it is eventually discovered and it recasts every previous confident
statement in doubt. The same goes for severity and priority: a QA whose "Critical" reliably means
critical becomes someone whose calls people stop re-checking. A QA whose "Critical" is unpredictable
becomes someone whose calls people always re-check.

> **Tip**
>
> When a fix or investigation was a team effort, say so explicitly in your own update: "confirmed with
> help from [name]'s earlier root-cause work." Giving credit costs you nothing and is one of the fastest,
> most visible ways a new person demonstrates they are trustworthy about facts, not just about code.

> **Common mistake**
>
> Do not chase trust by inflating your own certainty. Saying "I am confident this is fixed" when you
> only spot-checked one path is a bigger long-term cost than saying "I checked the main path; the edge
> cases still need another pass" and being right about the limits of what you actually verified.

![A lifeguard sitting in an elevated chair overlooking a busy Barcelona beach, with a red rescue float strapped to his side and a tall skyscraper in the background](building-trust.jpg)
*Lifeguard in Barcelona, Spain — Maria Moreno, Wikimedia Commons, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Barcelona%27s_lifeguard.jpg)*
- **Attentive, not busy-looking** — Trust is built by consistently watching the right things over time, not by visibly looking busy. A new QA earns the same way: steady, correct judgment noticed over weeks, not a single loud effort.
- **Equipment kept exactly where it belongs** — The rescue float is always strapped in the same place, ready without being asked. Following through on small commitments reliably, in the same way every time, is what colleagues quietly come to count on.
- **People below who rarely look up** — The swimmers below trust the chair is watched without checking constantly. That is what earned trust looks like from the outside — nobody feels the need to double-check your calls anymore.
- **A reputation built slowly in the background** — The skyline did not appear overnight, and neither does trust. It compounds slowly from many small correct calls, not from one dramatic rescue.

**Building trust deliberately**

1. **Follow through on small commitments** — A kept deadline or a proactive heads-up when you cannot meet one, every time, builds specific evidence of reliability.
2. **Ask instead of pretending to know** — A good question costs nothing; a confident wrong answer costs the trust in every answer that follows it.
3. **Give credit explicitly** — Naming who helped is free, visible, and one of the fastest signals of trustworthy reporting.
4. **Stay consistent on severity and priority** — A predictable, defensible judgment call is what lets people stop re-checking your calls over time.

*A trust-building habit tracker over four weeks (Python)*

```python
weeks = [
    {"followed_through": True, "asked_instead_of_guessing": True, "gave_credit": False, "consistent_calls": True},
    {"followed_through": True, "asked_instead_of_guessing": True, "gave_credit": True, "consistent_calls": True},
    {"followed_through": True, "asked_instead_of_guessing": True, "gave_credit": True, "consistent_calls": True},
    {"followed_through": True, "asked_instead_of_guessing": True, "gave_credit": True, "consistent_calls": True},
]
scores = []
prev = -1
trend_ok = True
for i, week in enumerate(weeks, start=1):
    score = sum(25 for done in week.values() if done)
    print("week" + str(i) + "=" + str(score))
    if score < prev:
        trend_ok = False
    prev = score
    scores.append(score)
average = round(sum(scores) / len(scores))
print("AVERAGE=" + str(average))
trend = "RISING" if trend_ok else "UNSTABLE"
print("TREND=" + trend)
result = "TRUSTED" if average >= 80 and trend_ok else "NOT_YET"
assert result == "TRUSTED", "trust score not yet earned"
print("RESULT=" + result)
```

*A trust-building habit tracker over four weeks (Java)*

```java
import java.util.LinkedHashMap;
import java.util.Map;
public class Main {
    public static void main(String[] args) {
        @SuppressWarnings("unchecked")
        Map<String, Boolean>[] weeks = new Map[] {
            mapOf(true, true, false, true),
            mapOf(true, true, true, true),
            mapOf(true, true, true, true),
            mapOf(true, true, true, true),
        };
        int[] scores = new int[weeks.length];
        int prev = -1;
        boolean trendOk = true;
        for (int i = 0; i < weeks.length; i++) {
            int score = 0;
            for (boolean done : weeks[i].values()) if (done) score += 25;
            System.out.println("week" + (i + 1) + "=" + score);
            if (score < prev) trendOk = false;
            prev = score;
            scores[i] = score;
        }
        int sum = 0;
        for (int s : scores) sum += s;
        int average = Math.round(sum / (float) scores.length);
        System.out.println("AVERAGE=" + average);
        String trend = trendOk ? "RISING" : "UNSTABLE";
        System.out.println("TREND=" + trend);
        String result = (average >= 80 && trendOk) ? "TRUSTED" : "NOT_YET";
        if (!result.equals("TRUSTED")) throw new AssertionError("trust score not yet earned");
        System.out.println("RESULT=" + result);
    }
    static Map<String, Boolean> mapOf(boolean a, boolean b, boolean c, boolean d) {
        Map<String, Boolean> m = new LinkedHashMap<>();
        m.put("followed_through", a);
        m.put("asked_instead_of_guessing", b);
        m.put("gave_credit", c);
        m.put("consistent_calls", d);
        return m;
    }
}
```

### Your first time: Start building trust deliberately in your first month

- [ ] Make small commitments you can actually keep — Promise specific, checkable things — 'retested by Thursday' — and follow through visibly.
- [ ] Ask a genuine question at least once a week — Pick something you are unsure of rather than guessing quietly and risking a confident wrong answer.
- [ ] Give credit by name in your written updates — Make collaboration visible instead of letting your update read as solo work.
- [ ] Check your severity calls against team precedent — Before filing, compare your rating to how similar issues were rated recently, and stay consistent.

- **A teammate double-checks your work even after weeks on the team.**
  Ask directly what would make them comfortable relying on your call without a recheck, and treat the answer as specific, actionable feedback.
- **You missed a small deadline you committed to.**
  Say so before anyone asks, with a revised estimate. A proactive heads-up preserves far more trust than a silent miss followed by an excuse.
- **Your severity ratings get overridden more often than a peer's.**
  Review the last several cases where it happened and look for a pattern in your calibration, rather than treating each override as an isolated disagreement.

### Where to check

- Your own recent commitments and whether each one was actually kept or proactively renegotiated.
- Past severity or priority calls you made, compared against how similar issues were eventually resolved.
- Direct feedback from a manager or buddy about what would increase their confidence in your calls.
- [[your-first-90-days/landing-well/your-first-bug-report-at-work]] for how a single early report already starts this same trust process.

### Worked example: the missed deadline handled two different ways

1. A new QA commits to retesting a fix by Thursday but discovers Wednesday evening she will not finish in time.
2. In one version of the story, she stays quiet and delivers Friday morning with no explanation.
3. In the other, she messages Wednesday night: "won't make Thursday, one edge case needs another environment; expect it by Friday noon."
4. Both versions deliver the same result a day late, but only one of them preserves trust in her next commitment.

**Quiz.** Which behavior builds a new QA's trust with their team fastest over time?

- [ ] Making bold predictions to sound confident
- [x] Consistently following through on small commitments and calibrating severity against precedent
- [ ] Avoiding questions so as not to look inexperienced
- [ ] Taking full individual credit for team debugging efforts

*Trust compounds from small, verifiable, consistent behavior — kept commitments and predictable judgment calls — not from confidence, silence, or claiming more credit than is accurate.*

- **Trust capital** — Accumulated confidence built from many small, consistent, verifiable actions rather than one impressive act, and it can be spent quickly by a single visible inconsistency.
- **Ask versus pretend** — A genuine question costs nothing; a confidently wrong answer costs trust in every answer that follows it.
- **Consistent severity calls** — A rating that predictably matches team precedent is what eventually lets colleagues stop double-checking your judgment.

### Challenge

Track your own commitments for one week: write down each one you make, then mark whether you kept it, renegotiated it proactively, or missed it silently. Notice which column is longest.

- [Atlassian — How to Build and Maintain Trust When You Start a New Job](https://www.atlassian.com/blog/productivity/build-trust-when-you-start-a-job)
- [Indeed — 14 Tips for Building Trust at Work](https://www.indeed.com/career-advice/career-development/building-trust)
- [How to Build Trust in the Workplace](https://www.youtube.com/watch?v=0-N1g9uL6Bk)

🎬 [How to Build Trust in the Workplace](https://www.youtube.com/watch?v=0-N1g9uL6Bk) (4 min)

- Trust accumulates from small, consistent, verifiable actions, not from one impressive gesture.
- Follow through on commitments, or renegotiate them proactively before the deadline passes.
- Ask genuine questions instead of pretending to know, and give credit explicitly.
- Consistent, defensible severity and priority calls are what let colleagues stop double-checking your judgment.


## Related notes

- [[Notes/your-first-90-days/landing-well/onboarding-as-a-qa|Onboarding as a QA]]
- [[Notes/your-first-90-days/landing-well/learning-the-product-fast|Learning the product fast]]
- [[Notes/your-first-90-days/landing-well/your-first-bug-report-at-work|Your first bug report at work]]


---
_Source: `packages/curriculum/content/notes/your-first-90-days/landing-well/building-trust.mdx`_
