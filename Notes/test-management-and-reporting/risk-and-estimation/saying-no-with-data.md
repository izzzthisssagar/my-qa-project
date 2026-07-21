---
title: "Saying no with data"
tags: ["test-management-and-reporting", "risk-and-estimation", "track-c"]
updated: "2026-07-21"
---

# Saying no with data

*A doctor doesn't refuse a patient's request - they hold up the x-ray, name the specific finding, and let the patient choose with full information. Saying no with data means the same: present the real tradeoff, backed by risk score and estimate, and let the stakeholder decide with the risk on record.*

> "We can't test all of that in two days" is technically a refusal and offers nobody anything to act
> on. "Full coverage needs five days; with two, here's exactly what gets tested and what gets skipped,
> and here's the specific risk of skipping the payment retry logic" is the same underlying constraint,
> turned into a real choice a stakeholder can actually make. The goal was never to say no - it was
> always to make sure whoever decides to accept a risk is doing it knowingly, not by accident.

> **In real life**
>
> A doctor holding up a patient's x-ray does not simply tell them what to do - they point at the actual
> finding, name it specifically, and lay out the real options with their real risks, so the patient
> makes the final call with full information in front of them. Nobody walks away from that conversation
> confused about what was decided or why, and if the chosen option doesn't go perfectly, nobody can say
> they were never told. Saying no with data works from the identical structure: bring the actual
> evidence - a risk score, an estimate - name the specific tradeoff, and let the stakeholder choose,
> on the record, rather than either silently absorbing an impossible ask or refusing with nothing to
> show for it.

**Saying no with data**: Saying no with data means responding to an unrealistic testing scope or timeline by presenting the specific tradeoff - backed by real risk scores and estimates - as an explicit choice for the stakeholder to make, rather than either silently accepting the impossible ask and quietly cutting corners, or flatly refusing with no evidence or alternative offered.

## The two failure modes this note exists to prevent

**Silent acceptance**: agreeing to an impossible timeline and quietly cutting corners to survive it -
this hides the real risk from everyone who should know about it, and when the cut corner eventually
surfaces as a real defect, the decision to accept that risk was never actually made by anyone with the
authority to make it. **Flat refusal**: "that's not possible" with no evidence or alternative offered
- technically honest, but it gives a stakeholder nothing to actually decide with, and reads as
obstructive rather than as the kind of partner who helps the business make an informed call. The
productive middle uses exactly the risk and estimation work already built: name the real number, name
the specific tradeoff, and hand the decision to whoever is actually accountable for it.

## The Iron Triangle makes the tradeoff explicit

Time, scope, and cost form what project management calls the Iron Triangle - change one and at least
one of the others has to move, because all three are tightly linked. Presented honestly, this becomes
three concrete options rather than one refusal: cut scope and hit the deadline with a defined,
reduced coverage; add resources (more testers, overtime) and hit the deadline with full scope; or
keep scope and resources fixed and accept a later, safer delivery date. Presenting all three,
explicitly, with the specific risk named for whichever scope gets cut, shifts the conversation from
"no" to "which of these tradeoffs does the business actually want" - and shifts the accountability for
that choice to the person who is supposed to be making it.

> **Tip**
>
> Always lead with the option that represents doing the work right, not the bad news first. "Full scope
> and quality needs five days - here's that plan" stated as the anchor, before presenting the reduced-
> scope alternative, keeps the conversation from starting on the back foot.

> **Common mistake**
>
> Presenting the tradeoff verbally in a hallway conversation with nothing written down. A decision to
> accept a specific, named risk needs to be documented - not to create a paper trail for blame, but so
> nobody has to rely on memory later about what was actually agreed to and why.

![A doctor holding up an x-ray and pointing at a finding while explaining it to two seated patients, one of whom is asking a question, with paperwork on the table](saying-no-with-data.jpg)
*Doctor explains x-ray to patient — Rhoda Baer, National Cancer Institute, public domain, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Doctor_explains_x-ray_to_patient.jpg)*
- **The x-ray - the actual evidence** — Not a verbal assurance - a real, checkable artifact everyone in the room can see for themselves. Saying no with data means bringing the actual risk score or estimate, not just an opinion about the timeline.
- **Pointing at the specific finding** — Not a vague warning - an exact, named thing on the image. A data-backed pushback names the specific risk being accepted, not a general sense that something might go wrong.
- **The patient, asking back - not just told** — A real conversation, not a pronouncement. Saying no with data means presenting the tradeoff and letting the stakeholder make an informed call, not refusing on the tester's own authority.
- **The paperwork - the decision, on record** — Whatever gets decided here gets written down. A documented tradeoff protects everyone later: nobody has to remember what was agreed to, and nobody gets blamed for a risk that was actually accepted knowingly.

**Turning a refusal into an informed decision**

1. **Bring the real data: risk scores and estimates already built** — Not a fresh opinion - the actual numbers from risk-based testing and estimation work already done.
2. **Present the Iron Triangle tradeoff explicitly** — Cut scope, add resources, or extend timeline - three real options, not one refusal.
3. **Name the specific risk for whichever scope gets cut** — Not "we might miss something" - the exact area, and why it's the one being left untested.
4. **Let the stakeholder choose, and document the decision** — The accountability for the accepted risk moves to whoever actually made the call, on the record.

*Presenting a scope tradeoff with named risk (Python)*

```python
full_scope_days = 5
available_days = 2

risk_ranked_items = [
    {"name": "Checkout flow", "risk_score": 20, "test_days": 1.0},
    {"name": "Payment retry logic", "risk_score": 18, "test_days": 0.7},
    {"name": "Profile settings", "risk_score": 6, "test_days": 1.3},
    {"name": "Footer links", "risk_score": 2, "test_days": 2.0},
]

ranked = sorted(risk_ranked_items, key=lambda i: i["risk_score"], reverse=True)

covered = []
remaining_days = available_days
for item in ranked:
    if item["test_days"] <= remaining_days:
        covered.append(item)
        remaining_days -= item["test_days"]

skipped = [i for i in ranked if i not in covered]

print("Full scope requires " + str(full_scope_days) + " days. Available: " + str(available_days) + " days.")
print("")
print("With " + str(available_days) + " days, this gets covered:")
for c in covered:
    print("  " + c["name"] + " (risk score " + str(c["risk_score"]) + ")")

print("")
print("This gets skipped, with the specific risk accepted:")
for s in skipped:
    print("  " + s["name"] + " (risk score " + str(s["risk_score"]) + ") - UNTESTED if this scope is chosen")
```

*Presenting a scope tradeoff with named risk (Java)*

```java
import java.util.*;

public class Main {
    static class Item {
        String name; int riskScore; double testDays;
        Item(String name, int riskScore, double testDays) {
            this.name = name; this.riskScore = riskScore; this.testDays = testDays;
        }
    }

    public static void main(String[] args) {
        int fullScopeDays = 5;
        double availableDays = 2;

        List<Item> items = new ArrayList<>();
        items.add(new Item("Checkout flow", 20, 1.0));
        items.add(new Item("Payment retry logic", 18, 0.7));
        items.add(new Item("Profile settings", 6, 1.3));
        items.add(new Item("Footer links", 2, 2.0));

        items.sort((a, b) -> Integer.compare(b.riskScore, a.riskScore));

        List<Item> covered = new ArrayList<>();
        double remainingDays = availableDays;
        for (Item item : items) {
            if (item.testDays <= remainingDays) {
                covered.add(item);
                remainingDays -= item.testDays;
            }
        }

        List<Item> skipped = new ArrayList<>();
        for (Item item : items) if (!covered.contains(item)) skipped.add(item);

        System.out.println("Full scope requires " + fullScopeDays + " days. Available: " + availableDays + " days.");
        System.out.println();
        System.out.println("With " + availableDays + " days, this gets covered:");
        for (Item c : covered) System.out.println("  " + c.name + " (risk score " + c.riskScore + ")");

        System.out.println();
        System.out.println("This gets skipped, with the specific risk accepted:");
        for (Item s : skipped) {
            System.out.println("  " + s.name + " (risk score " + s.riskScore + ") - UNTESTED if this scope is chosen");
        }
    }
}
```

### Your first time: Reframe one real timeline pressure as an explicit choice

- [ ] Take one real situation where a testing timeline feels unrealistic — A current or recent example, not a hypothetical.
- [ ] Pull the risk ranking and effort estimates already available for that scope — From risk-based testing and estimation work - the actual data, not a fresh guess.
- [ ] Write the three Iron Triangle options explicitly: cut scope, add resources, or extend time — For the cut-scope option specifically, name exactly what gets tested and what doesn't.
- [ ] Present it as a written decision for the stakeholder, not a verbal refusal — Confirm the choice and its accepted risk get documented once a decision is made.

- **A team silently cuts testing scope to meet a deadline, and nobody outside the team knows it happened.**
  The tradeoff was absorbed silently instead of surfaced - reconstruct what was actually skipped and present it retroactively as the explicit, named risk it always should have been.
- **A tester's pushback on a timeline is dismissed as unhelpful or obstructive.**
  Check whether the pushback included real data (risk scores, estimates) and concrete options, or was a flat refusal with nothing to act on - the Iron Triangle framing turns the same concern into something a stakeholder can actually work with.
- **A risk that was 'accepted' during a rushed conversation later gets blamed entirely on the testing team.**
  The decision was never documented - going forward, any accepted risk needs to be written down at the time it's agreed to, specifically to prevent this exact dispute.

### Where to check

- Any current timeline or scope pressure, checked for whether the response so far has been silent absorption, flat refusal, or an actual data-backed tradeoff conversation.
- Past decisions to skip testing scope, checked for whether they were ever documented as an explicit, named, accepted risk.
- [[test-management-and-reporting/risk-and-estimation/risk-based-testing]] for the risk scores this note's tradeoff conversation is built directly on.
- [[test-management-and-reporting/risk-and-estimation/test-estimation-techniques]] for the defensible time estimates that make the Iron Triangle conversation possible in the first place.
- [[test-management-and-reporting/risk-and-estimation/prioritizing-what-to-test-first]] for deciding exactly what gets covered within whatever reduced scope a stakeholder ultimately chooses.

### Worked example: a documented tradeoff that protected the team when the accepted risk materialized

1. A release deadline leaves two days for testing against a risk-ranked scope that would normally take
   five, based on real estimates the team has tracked historically.
2. Instead of silently testing whatever fits or flatly saying it's impossible, the tester presents
   three options in writing: extend the deadline by three days for full coverage, add a second tester
   temporarily to compress the timeline, or accept reduced scope covering only the two highest-risk
   areas (checkout and payment retry) with named, explicit gaps in the rest.
3. The product manager, with full information, chooses reduced scope - explicitly accepting, in
   writing, that profile settings and less-critical areas will ship untested this cycle.
4. A minor bug does surface in profile settings after release - exactly the kind of gap the documented
   tradeoff named in advance.
5. Because the decision was on record, the conversation afterward is "yes, we knew and accepted this
   risk deliberately, here's why" rather than an unproductive dispute about who is at fault - the
   documentation did exactly the job it was written for.

**Quiz.** According to this note, what is the actual goal of 'saying no with data' - is it really about saying no?

- [ ] The goal is to refuse unrealistic requests as firmly and clearly as possible
- [x] The goal is not really to say no at all - it's to present the real tradeoff explicitly, backed by data, so whoever is accountable for the decision makes it knowingly rather than a risk being silently absorbed or a flat refusal offering nothing to act on
- [ ] The goal is to always find a way to say yes regardless of the real constraints
- [ ] The goal is to document disagreements for later blame assignment

*The note frames both silent acceptance and flat refusal as failure modes - neither actually serves the stakeholder or the project. The real goal is surfacing the true tradeoff with real data (risk scores, estimates) so an informed decision gets made by the person actually accountable for it, and documented so nobody has to rely on memory about what was agreed to and why.*

- **Saying no with data** — Presenting an unrealistic scope or timeline as an explicit, data-backed tradeoff for the stakeholder to decide - not silently absorbing the risk, and not flatly refusing with no evidence or alternative.
- **The two failure modes this note warns against** — Silent acceptance (quietly cutting corners, hiding the real risk) and flat refusal (technically honest, but offers no evidence or alternative to actually decide with).
- **The Iron Triangle, applied to a testing tradeoff** — Time, scope, and cost are linked - cut scope to hit a deadline, add resources to keep scope, or extend the timeline to keep both. Presenting all three shifts a refusal into a real choice.
- **Why the decision needs to be documented** — Not for blame, but so nobody has to rely on memory later about what was actually agreed to - it protects both the stakeholder's informed choice and the tester who flagged the risk honestly.

### Challenge

Take one real timeline or scope pressure you're facing (or have faced). Pull the relevant risk scores and estimates, write out the three Iron Triangle options explicitly, and name the specific risk for the reduced-scope option. Present it as a written choice rather than a verbal refusal.

- [Atlassian — Project Trade-Off Analysis](https://www.atlassian.com/team-playbook/plays/trade-offs)
- [When to Push Back on Unrealistic Testing Deadlines](https://blog.magicpod.com/when-to-push-back-on-unrealistic-testing-deadlines)
- [How to Master the Iron Triangle in Project Management: Balancing Time, Cost, and Scope](https://www.youtube.com/watch?v=nUjc7lut7CE)

🎬 [How to Master the Iron Triangle in Project Management: Balancing Time, Cost, and Scope](https://www.youtube.com/watch?v=nUjc7lut7CE) (9 min)

- Saying no with data means presenting a real tradeoff backed by risk scores and estimates, not silently absorbing an impossible ask or flatly refusing with no evidence.
- The Iron Triangle (time, scope, cost) turns a refusal into three explicit options: cut scope, add resources, or extend the timeline - each with a real, named consequence.
- Name the specific risk being accepted for whichever scope gets cut - not a vague warning, but the exact area and why it's the one left untested.
- The goal is shifting an informed decision to whoever is actually accountable for it, not winning an argument or avoiding all risk entirely.
- Document the decision once made - it protects the stakeholder's informed choice and the tester who flagged the risk honestly, and prevents a later dispute about who agreed to what.


## Related notes

- [[Notes/test-management-and-reporting/risk-and-estimation/risk-based-testing|Risk-based testing]]
- [[Notes/test-management-and-reporting/risk-and-estimation/prioritizing-what-to-test-first|Prioritizing what to test first]]
- [[Notes/test-management-and-reporting/risk-and-estimation/test-estimation-techniques|Test estimation techniques]]


---
_Source: `packages/curriculum/content/notes/test-management-and-reporting/risk-and-estimation/saying-no-with-data.mdx`_
