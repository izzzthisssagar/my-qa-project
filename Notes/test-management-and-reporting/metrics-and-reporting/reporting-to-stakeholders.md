---
title: "Reporting to stakeholders"
tags: ["test-management-and-reporting", "metrics-and-reporting", "track-c"]
updated: "2026-07-21"
---

# Reporting to stakeholders

*'Ysgol 140 llath' and 'School 140 yds' are the exact same warning, translated - not softened, not summarized differently. A finding reported to an executive and the same finding filed for a developer need that identical discipline: same fact, different language, zero drift in substance.*

> "P1 defect blocking the checkout flow, root cause in the payment gateway's timeout handling" is a
> perfectly clear sentence to a developer and nearly meaningless to an executive who has thirty seconds
> to decide whether to delay a launch. "Customers currently cannot complete a purchase - this is
> revenue-impacting until fixed" is the same fact, translated for a reader who needs to act on it in a
> completely different way. Neither version is more true than the other. Reporting to stakeholders is
> entirely the discipline of knowing which version a given reader actually needs.

> **In real life**
>
> A bilingual road sign in Wales reads "Ysgol 140 llath" above "School 140 yds" - the identical warning,
> at the identical distance, rendered once for a Welsh-speaking reader and once for an English-speaking
> one. Nothing about the fact changes between the two lines: same distance, same hazard, same urgency.
> Only the language changes, because the sign's entire job is getting one true warning into the head of
> whoever happens to be reading it, in whatever form actually lands. Reporting the same finding to an
> executive, a product manager, and a developer needs that exact discipline - the underlying fact stays
> completely fixed, and only the vocabulary, depth, and framing shift to match the reader in front of it.

**Reporting to stakeholders**: Reporting to stakeholders means translating the same underlying finding into the specific vocabulary, depth, and framing each distinct audience needs to act on it - business-impact language for executives, feature-and-blocker status for product managers, full technical detail for developers - while keeping the substance of the finding itself completely unchanged across every version.

## Three audiences, one fact, three different reports

An **executive** needs business impact in the time it takes to read a sentence: what breaks, for
whom, and what it costs if unfixed - "our mean time to recover improved from 4.2 hours to 1.8 hours
over 90 days, cutting per-incident cost from $22K to $9K" tells a complete, compelling story in two
sentences, with zero implementation detail. A **product manager** needs feature-level status and
exactly what they're blocked on or need to decide - which epic is at risk, what tradeoff needs their
call, by when. A **developer** needs the opposite of a summary: the full technical detail - exact
repro steps, the stack trace, the specific failing assertion - because summarizing away the technical
substance is exactly what makes a report useless to the one audience whose job is fixing the
underlying code.

## The structure that works for every version: pyramid, not maze

Every one of these three versions should lead with the conclusion and let supporting detail follow -
a pyramid, not a maze a reader has to walk through to find the point. For a non-technical audience
specifically, that means starting at the business outcome and only then, if at all, touching the
technical cause; a maze-shaped report that opens with methodology and buries the actual impact
several paragraphs in loses a busy executive before the sentence that mattered ever arrives.

> **Tip**
>
> Before sending any stakeholder-facing report, ask one question: what does this specific reader need
> to decide or do differently after reading it? If the answer isn't obvious from the first sentence,
> restructure until it is - the detail can come after, never instead of, the point.

> **Common mistake**
>
> Sending the exact same report, unedited, to every audience. A developer-detail report overwhelms an
> executive who has no use for a stack trace; an executive-summary report starves a developer of the
> one thing they actually need to fix anything. One finding, multiple translations - never one document
> trying to serve every reader equally.

![A bilingual Welsh and English road warning sign reading Ysgol 140 llath and School 140 yds with a red triangular warning icon, on a quiet street with colorful houses](reporting-to-stakeholders.jpg)
*Bilingual warning sign — Ysgol/School, Greenfield Road, Tenby — Jaggery, CC BY-SA 2.0, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Bilingual_warning_sign_-_Ysgol-School,_Greenfield_Road,_Tenby_-_geograph.org.uk_-_5259470.jpg)*
- **Ysgol 140 llath - one translation** — Same fact, same distance, phrased for a Welsh-speaking reader. An executive's version of a finding states the same underlying truth in the language they actually process quickly.
- **School 140 yds - the other translation** — Not a different fact - the identical warning, translated. A developer's version of the same finding (stack trace, exact repro) and an executive's version (business risk, cost) have to stay this consistent underneath the different wording.
- **The warning triangle - the one universal signal** — No translation needed for the shape itself - danger ahead, understood instantly by anyone. Every stakeholder report needs one universal signal too: a clear severity or ship/hold status that registers without reading the detail.
- **The actual street the sign describes** — The sign isn't the reality - it's a warning about the reality just ahead. A report is the same: never a substitute for the underlying system, just a translated pointer toward exactly where the real risk sits.

**Translating one finding for three readers**

1. **Start from the single, unchanged underlying fact** — Checkout is broken for a specific class of users under a specific condition - this does not change across any version.
2. **For the executive: business impact, in one or two sentences** — What breaks, for whom, what it costs - no implementation detail, no jargon.
3. **For the product manager: status, blocker, and the decision they own** — Which feature is at risk, what tradeoff needs a call, by when.
4. **For the developer: full technical detail, unabridged** — Exact repro steps, stack trace, failing assertion - the version that gets the actual fix built.

*Generating three audience-specific versions from one finding (Python)*

```python
finding = {
    "summary": "Checkout fails for users with expired session tokens during payment confirmation",
    "affected_users_percent": 8,
    "revenue_impact_daily": 14000,
    "epic": "Checkout Redesign Q3",
    "blocking_decision": "Delay launch by 2 days, or ship with this known issue and a hotfix planned",
    "root_cause": "PaymentController.confirmPayment() does not refresh an expired session token before calling the gateway API",
    "repro_steps": "1) Start checkout 2) Leave session idle 31+ min 3) Complete payment - fails with 401",
}

def for_executive(f):
    daily_cost = "$" + str(f["revenue_impact_daily"])
    return ("Checkout is currently failing for about " + str(f["affected_users_percent"]) +
            "% of customers, costing roughly " + daily_cost + "/day until fixed.")

def for_product_manager(f):
    return ("'" + f["epic"] + "' is blocked. Decision needed: " + f["blocking_decision"])

def for_developer(f):
    return "Root cause: " + f["root_cause"] + "\\nRepro: " + f["repro_steps"]

print("=== For the executive ===")
print(for_executive(finding))
print("")
print("=== For the product manager ===")
print(for_product_manager(finding))
print("")
print("=== For the developer ===")
print(for_developer(finding))
```

*Generating three audience-specific versions from one finding (Java)*

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, Object> finding = new HashMap<>();
        finding.put("summary", "Checkout fails for users with expired session tokens during payment confirmation");
        finding.put("affectedUsersPercent", 8);
        finding.put("revenueImpactDaily", 14000);
        finding.put("epic", "Checkout Redesign Q3");
        finding.put("blockingDecision", "Delay launch by 2 days, or ship with this known issue and a hotfix planned");
        finding.put("rootCause", "PaymentController.confirmPayment() does not refresh an expired session token before calling the gateway API");
        finding.put("reproSteps", "1) Start checkout 2) Leave session idle 31+ min 3) Complete payment - fails with 401");

        System.out.println("=== For the executive ===");
        System.out.println("Checkout is currently failing for about " + finding.get("affectedUsersPercent") +
                "% of customers, costing roughly $" + finding.get("revenueImpactDaily") + "/day until fixed.");

        System.out.println();
        System.out.println("=== For the product manager ===");
        System.out.println("'" + finding.get("epic") + "' is blocked. Decision needed: " + finding.get("blockingDecision"));

        System.out.println();
        System.out.println("=== For the developer ===");
        System.out.println("Root cause: " + finding.get("rootCause"));
        System.out.println("Repro: " + finding.get("reproSteps"));
    }
}
```

### Your first time: Translate one real finding three ways

- [ ] Pick one real defect or test finding you have full detail on — Something with a clear technical root cause and a real business consequence.
- [ ] Write the executive version first: one or two sentences, business impact only — No implementation detail, no jargon - what breaks, for whom, what it costs.
- [ ] Write the product manager version: status and the specific decision they own — What's blocked, what tradeoff needs their call, by when.
- [ ] Write the developer version last: full technical detail, unabridged — Exact repro, stack trace, root cause - nothing summarized away.

- **An executive reads a status update and still can't say whether a launch should be delayed.**
  The report likely led with technical framing instead of business impact - rewrite the opening sentence around cost, scope, and urgency, with technical detail moved after or removed entirely.
- **A developer gets a bug assigned with only an executive-style summary and no reproduction detail.**
  The wrong translation reached the wrong audience - developers need the full technical version, not the business-impact summary meant for a different reader.
- **Two stakeholders who read different versions of the same finding come away with contradictory understandings of severity.**
  Check that both versions actually describe the same underlying fact - translation should never let the substance drift, only the framing and depth.

### Where to check

- Any report or update about to go to a non-technical audience, checked specifically for whether the first sentence states business impact or opens with technical framing instead.
- Whether a developer-facing bug report actually contains full reproduction detail, not an executive-style summary that got copy-pasted into the wrong channel.
- [[test-management-and-reporting/metrics-and-reporting/test-summary-reports]] for the document-level version of this same audience-awareness discipline.
- [[test-management-and-reporting/docs-and-communication/writing-for-developers]] for the specific standard the technical-audience version of a finding needs to meet.
- [[test-management-and-reporting/docs-and-communication/status-updates]] for the ongoing, shorter-form version of stakeholder reporting this note's principles apply to just as directly.

### Worked example: one finding, two versions, two very different outcomes

1. A tester finds a defect: 8% of users hit a checkout failure caused by an unrefreshed session token,
   costing an estimated $14,000/day while unfixed.
2. Version one, sent to the executive sponsor unedited from the bug tracker: "PaymentController.
   confirmPayment() throws a 401 due to expired session token not being refreshed before the gateway
   call" - technically complete, and the executive has no way to judge urgency or cost from it.
3. Version two, rewritten specifically for that audience: "Checkout is currently failing for about 8%
   of customers, costing roughly $14,000/day until fixed. Recommend delaying launch by two days for a
   fix, or shipping with a same-day hotfix planned" - same underlying fact, immediately actionable.
4. The executive reading version one asks three clarifying questions before making any decision; the
   executive reading version two makes the call in the same message thread within minutes.
5. The developer assigned the fix still gets the full technical version - repro steps, root cause,
   exact failing line - because that translation was never the one that needed to change.

**Quiz.** According to this note, what should stay identical across the executive, product manager, and developer versions of the same finding?

- [ ] The exact wording and technical vocabulary used in each version
- [x] The underlying fact and substance of the finding - only the vocabulary, depth, and framing change to match what each specific reader needs to act on it
- [ ] Nothing - each audience should receive completely independent, unrelated summaries
- [ ] The length of the report, which should be identical for every audience

*The analogy is a bilingual road sign: 'Ysgol 140 llath' and 'School 140 yds' are the same distance, the same hazard, the same urgency - only the language differs. A finding translated for different stakeholders has to hold that same discipline: the fact itself never drifts, even though the words, depth, and framing change completely to fit what each reader actually needs.*

- **Reporting to stakeholders** — Translating the same underlying finding into the vocabulary, depth, and framing each distinct audience needs to act on it - while keeping the substance of the finding itself completely unchanged.
- **What each of the three audiences actually needs** — Executives: business impact in one or two sentences. Product managers: feature status and the specific decision they own. Developers: full, unabridged technical detail.
- **Pyramid, not maze** — Lead with the conclusion and let supporting detail follow, for every audience - a report that opens with methodology and buries the point loses a busy reader before it matters.
- **The core stakeholder-reporting mistake** — Sending the same unedited report to every audience - overwhelming a non-technical reader with implementation detail, or starving a developer of the technical substance they actually need.

### Challenge

Take one real finding you have full technical detail on and write three versions: an executive summary (business impact, two sentences max), a product manager update (status and decision needed), and a developer report (full technical detail). Confirm all three describe the exact same underlying fact.

- [Statsig — From Data to Decisions: Communicating Findings to Non-Technical Teams](https://www.statsig.com/perspectives/from-data-to-decisions-how-to-communicate-findings-to-non-technical-teams)
- [Built In SF — How Data Scientists Communicate Effectively With Non-Technical Stakeholders](https://www.builtinsf.com/articles/how-2-data-scientists-communicate-effectively-non-technical-stakeholders)
- [How to Communicate with Non-Technical Stakeholders](https://www.youtube.com/watch?v=7oaxAZH40uU)

🎬 [How to Communicate with Non-Technical Stakeholders](https://www.youtube.com/watch?v=7oaxAZH40uU) (10 min)

- The same finding needs different translations for different stakeholders - business impact for executives, status and decisions for product managers, full technical detail for developers.
- The underlying fact must stay identical across every version - only vocabulary, depth, and framing change, never the substance.
- Structure every version like a pyramid, not a maze: lead with the conclusion, let supporting detail follow, especially for non-technical audiences.
- Sending one unedited report to every audience fails both ends - it overwhelms a non-technical reader and starves a developer of what they actually need to fix anything.
- Before sending any stakeholder report, confirm the first sentence answers what that specific reader needs to decide or do next.


## Related notes

- [[Notes/test-management-and-reporting/metrics-and-reporting/test-summary-reports|Test summary reports]]
- [[Notes/test-management-and-reporting/docs-and-communication/writing-for-developers|Writing for developers]]
- [[Notes/test-management-and-reporting/docs-and-communication/status-updates|Status updates]]


---
_Source: `packages/curriculum/content/notes/test-management-and-reporting/metrics-and-reporting/reporting-to-stakeholders.mdx`_
