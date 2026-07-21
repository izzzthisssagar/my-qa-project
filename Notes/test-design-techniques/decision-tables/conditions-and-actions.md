---
title: "Conditions & actions"
tags: ["test-design-techniques", "decision-tables", "track-a"]
updated: "2026-07-14"
---

# Conditions & actions

*Before a decision table can be built, its conditions and actions have to be identified correctly - and the single most common mistake is mixing the two up, which silently doubles the table for no real reason.*

> A decision table lives or dies on one preparatory step that happens before any row gets drawn: correctly
> telling conditions and actions apart. Get this wrong - treat an output as if it were an input, or miss a
> real condition entirely - and the table that follows is broken from its very first row, no matter how
> carefully the rest of it gets built. This note is entirely about that one step.

> **In real life**
>
> An airliner's overhead panel is a decision table built out of switches and wires. Flip the "IDG1"
> switch, and a green line on the panel traces exactly which electrical bus that decision feeds - the
> switch is the CONDITION, the bus receiving power is the ACTION, and the wiring in between is the rule
> connecting them. Nobody confuses the switch for the light it controls; the whole panel only works
> because every condition and every action has its own clearly separate identity. A decision table asks a
> tester to do the same sorting exercise in words instead of wires - and the switch-versus-light
> confusion is exactly the mistake this note is about avoiding.

**Condition vs action**: A condition is an independent input the system checks to decide what happens - something that can vary on its own, separately from every other condition (credit score: good or poor; income: stable or unstable). An action is an output the system produces as a RESULT of evaluating the conditions (loan approved; manual review required; loan rejected). The critical distinction: a condition can be set or observed BEFORE the decision is made, while an action is the OUTCOME of that decision. Treating an action as if it were a condition - or a condition as if it were an action - corrupts every rule built from that point forward, and is the single most common mistake in building a decision table.

## Conditions are inputs, chosen or observed before the decision

A condition exists independently of what the system decides to do about it - an applicant's credit
score is what it is regardless of whether the loan ultimately gets approved. Good candidate conditions
answer the question "what does the system need to KNOW before it can decide?" - and each one should be
genuinely independent: knowing one condition's value shouldn't automatically tell you another
condition's value.

## Actions are outputs, produced as a result of the conditions

An action only exists because conditions were evaluated first - "loan approved" isn't a fact about the
applicant, it's the system's RESPONSE to facts about the applicant. Good candidate actions answer "what
does the system actually DO once it knows the conditions?" - and there's often more than one action per
rule (approve the loan AND send a confirmation email are two separate actions from one rule).

## The most common mistake: an action disguised as a condition

It's surprisingly easy to accidentally list "is the loan approved?" as if it were a third condition
alongside credit score and income - especially when a related, EARLIER decision's output feeds into a
later one. The test is always: could this value exist BEFORE any decision gets made, on its own, or
does it only come into existence AS a decision's result? If it's the latter, it's an action, and listing
it as a condition doesn't just look odd - it silently doubles the size of the table for no real
information gained.

![A detailed overhead switch panel of an Airbus A320 airliner in flight, showing dozens of labeled switches organized into sections (ELEC, AIR COND, ANTI ICE, CABIN PRESS), illuminated digital voltage readouts, and a green electrical bus flow diagram connecting generator and battery switches](conditions-and-actions.jpg)
*Overhead panel of an Airbus A320 during cruise — Wikimedia Commons, CC BY-SA 3.0 (Olivier Cleynen)*
- **The green flow lines = a literal, physical decision table wired into the panel** — This diagram shows exactly which switch positions (conditions) connect to which electrical bus (the resulting action) - the same relationship a decision table's rows and columns exist to make explicit. Trace one line and you're reading conditions-to-actions logic directly off the hardware.
- **A guarded, red-collared switch = a condition worth naming precisely** — This switch isn't flipped by accident - the guard exists because its position matters enough to deserve deliberate attention. A decision table's conditions deserve the same respect: named specifically enough that nobody overlooks which one actually drives a given outcome.
- **BAT 1 / BAT 2 readouts = the actual VALUES a condition gets evaluated against** — "27.6V" isn't a label, it's live data - the same way a decision table's condition row isn't just a category name, it's evaluated against a real value every time the table gets applied.
- **A cluster of related switches under one heading = several conditions feeding one coordinated action** — MAN V/S CTL, MODE SEL, and DITCHING don't operate in isolation - together they determine how cabin pressure control behaves. This is what a decision table's COLUMN represents: one full combination of condition values, read together, producing one action.
- **ENG 1 BLEED, connected by a green line to PACK 1 = one condition, one traceable action** — Follow the line from the bleed switch to the pack it feeds, and the relationship is completely unambiguous - flip this, that happens. A decision table exists to make that same one-condition-to-one-action link just as traceable in software logic.

**Sorting a rule's raw facts into conditions and actions - press Play**

1. **Read the rule and list every fact it mentions** — "Good credit and stable income get automatic approval; poor credit is always rejected" - list every noun and outcome mentioned, without sorting yet.
2. **Ask of each one: could this exist BEFORE a decision is made?** — Credit score: yes, it's a fact about the applicant regardless of outcome. Loan approved: no, it only exists once the decision has actually been made.
3. **Everything that passes = a condition; everything that doesn't = an action** — Credit score and income are conditions. Approved, rejected, and manual-review-required are actions - the system's possible responses.
4. **Check each condition is genuinely independent** — Does knowing credit score tell you anything about income, or vice versa? If two 'conditions' always move together, they may really be one condition, not two.
5. **Confirm no action snuck into the conditions list** — Re-scan the condition list specifically for anything that's actually a RESULT rather than an input - this is the single most common error to catch before building the table.

Here's the concrete cost of that mistake, made visible - correctly identified conditions versus an
action mistakenly counted as a third one:

*Run it - the real cost of mistaking an action for a condition (Python)*

```python
def combination_count(conditions):
    total = 1
    for name, values in conditions.items():
        total *= len(values)
    return total

# Correctly identified: 2 real conditions driving the decision
real_conditions = {
    "credit_score": ["good", "poor"],
    "income": ["stable", "unstable"],
}

# A common mistake: treating the ACTION itself as an extra "condition"
mistaken_conditions = {
    "credit_score": ["good", "poor"],
    "income": ["stable", "unstable"],
    "loan_approved": ["yes", "no"],  # this is the ACTION, not a condition!
}

print(f"Correct conditions      -> {combination_count(real_conditions)} rules to define ({list(real_conditions)})")
print(f"Action miscounted as a condition -> {combination_count(mistaken_conditions)} rules ({list(mistaken_conditions)})")
print()
print("The extra 'condition' doesn't represent a real independent input -")
print("it's the OUTPUT wearing an input's clothing, and it doubles the table for no reason.")

# Correct conditions      -> 4 rules to define (['credit_score', 'income'])
# Action miscounted as a condition -> 8 rules (['credit_score', 'income', 'loan_approved'])
#
# The extra 'condition' doesn't represent a real independent input -
# it's the OUTPUT wearing an input's clothing, and it doubles the table for no reason.
```

Same demonstration in Java - the shape a rule-definition validator might use to sanity-check a table
before anyone starts filling it in:

*Run it - the condition/action miscount cost (Java)*

```java
import java.util.*;

public class Main {

    static int combinationCount(LinkedHashMap<String, List<String>> conditions) {
        int total = 1;
        for (List<String> values : conditions.values()) {
            total *= values.size();
        }
        return total;
    }

    public static void main(String[] args) {
        LinkedHashMap<String, List<String>> realConditions = new LinkedHashMap<>();
        realConditions.put("credit_score", List.of("good", "poor"));
        realConditions.put("income", List.of("stable", "unstable"));

        LinkedHashMap<String, List<String>> mistakenConditions = new LinkedHashMap<>();
        mistakenConditions.put("credit_score", List.of("good", "poor"));
        mistakenConditions.put("income", List.of("stable", "unstable"));
        mistakenConditions.put("loan_approved", List.of("yes", "no")); // this is the ACTION, not a condition!

        System.out.println("Correct conditions      -> " + combinationCount(realConditions) + " rules to define " + realConditions.keySet());
        System.out.println("Action miscounted as a condition -> " + combinationCount(mistakenConditions) + " rules " + mistakenConditions.keySet());
        System.out.println();
        System.out.println("The extra 'condition' doesn't represent a real independent input -");
        System.out.println("it's the OUTPUT wearing an input's clothing, and it doubles the table for no reason.");
    }
}

/* Output matches the Python run exactly. */
```

> **Tip**
>
> The "could this exist before any decision is made?" question is the fastest reliable test for sorting a
> raw list of facts into conditions and actions. Apply it to every single item on the list, even ones that
> feel obvious - the mistaken case in this note's playground looked entirely reasonable at a glance,
> which is exactly why it's worth checking explicitly rather than trusting a first impression.

### Your first time: Your mission: sort a real business rule into conditions and actions

- [ ] Find a real multi-factor rule — A shipping policy, a discount eligibility rule, an access-control policy - anything where an outcome depends on more than one factor at once.
- [ ] List every fact and outcome the rule mentions, unsorted — Don't categorize yet - just write down everything the rule's wording touches on.
- [ ] Apply the 'before any decision' test to each item — Could this value exist independently, before the system decides anything? If yes, it's a condition. If it only exists as a result, it's an action.
- [ ] Check every condition for independence — Does knowing one condition's value tell you anything about another's? If two 'separate' conditions always move together, reconsider whether they're really one.
- [ ] Re-scan specifically for a disguised action — This note's most common mistake - go back through your condition list one more time, hunting specifically for anything that's secretly an output.

You practiced the exact sorting exercise a decision table depends on getting right before a single row gets drawn - and checked specifically for the mistake that's easiest to make without noticing.

- **I'm not sure if something is a condition or an action - it could plausibly be read either way.**
  Ask which one comes FIRST causally, not which one sounds more like an input. 'Account is verified' sounds like a condition, but if verification itself is a decision the system makes based on other facts (submitted ID, matched name), it's actually an action of an earlier decision - and the FACTS that verification was based on are the real conditions.
- **Two of my 'conditions' always seem to have the same value together in every real example I can think of.**
  This is worth investigating before building the table, not after - if they truly always move together, they may be one condition wearing two names, and treating them as separate needlessly doubles the table. If you can construct even one plausible real case where they'd diverge, they're genuinely independent and should stay separate.
- **My rule mentions an action that itself becomes an input to a LATER decision.**
  This is a real, valid pattern - not a mistake - but it means there are two separate decision tables, not one. Model the first decision's action as that table's output; then treat it as a genuine condition of the SECOND table, since by the time the second decision runs, that value already exists as a settled fact.
- **I found a condition that seems to have no bearing on any action at all.**
  Double check it's not affecting an action indirectly through a rule you haven't looked at closely yet - but if it's genuinely never referenced by any actual outcome, it's not a real condition for this table and including it would only inflate the rule count without adding real coverage. Drop it, but note why in case a future requirement change makes it relevant again.

### Where to check

Where getting conditions and actions right matters most:

- **Any rule with more than two factors mentioned in the same sentence** — the more factors a rule's wording touches, the easier it is to accidentally list an output as if it were an input.
- **Rules describing MULTI-STEP business logic** — "verified users with a clean payment history get expedited shipping" often hides an earlier decision (verification) feeding a later one; treat these as two tables, not one inflated one.
- **Requirements or tickets that mix cause and effect in the same list** — a ticket's bullet points frequently interleave inputs and outputs without labeling which is which; the sorting has to happen explicitly, not by assuming the ticket's structure already did it.
- **Any decision table that feels unexpectedly large** — an inflated rule count is a strong signal to re-check whether an action got miscounted as a condition, before assuming the business logic itself is just genuinely that complex.
- **Handoffs from someone else's partially-built table** — a table you didn't build yourself is exactly where an inherited condition/action mixup is easiest to miss, since the sorting mistake was made before you ever saw it.

The habit: **explicitly apply the "could this exist before any decision is made" test to every item on the list - don't rely on a fact merely feeling like an input.**

### Worked example: untangling a real rule that hides a disguised action

1. **The rule, as written in a ticket:** "Orders from verified accounts with items in stock ship same-day. Verified accounts are ones where the ID check passed and the phone number was confirmed."
2. **First pass, listing everything mentioned:** account verified, items in stock, ID check passed, phone confirmed, ships same-day. Five items, not yet sorted.
3. **Apply the 'before any decision' test to 'account verified.'** Could this exist on its own, before any decision? On reflection - no. It's ITSELF a decision, made from two other facts (ID check passed, phone confirmed). It's an action of an earlier, smaller decision, not a condition of the shipping decision.
4. **Correctly identify two separate tables hiding in one ticket.** Table A (verification): conditions are "ID check passed" and "phone confirmed"; action is "account verified" (yes/no). Table B (shipping): conditions are "account verified" (now correctly an INPUT here, since by this point it's a settled fact) and "items in stock"; action is "ships same-day" (yes/no).
5. **Confirm independence within each table.** In Table A: does ID-check status tell you anything about phone-confirmation status? No - genuinely independent. In Table B: does account-verified status tell you anything about stock levels? No - also independent.
6. **Build Table A first, since Table B depends on its output.** Two conditions, four rules: (pass, confirmed) -> verified; (pass, not confirmed) -> not verified; (fail, confirmed) -> not verified; (fail, not confirmed) -> not verified.
7. **Build Table B using Table A's action as a genuine condition now.** Two conditions (verified, in stock), four rules, exactly as sized as a real two-factor decision should be - not artificially inflated by treating the ticket's five raw items as five independent conditions.
8. **The payoff:** what looked like a single, oddly five-factored decision was actually two clean, correctly-sized two-factor decisions chained together - each one easy to build, test, and reason about on its own, once the conditions and actions were sorted correctly instead of taken at face value from the ticket's wording.

> **Common mistake**
>
> Taking a requirement's wording at face value and listing every noun it mentions as a "condition"
> without checking whether some of them are actually actions, or actions of an EARLIER decision hiding
> inside the same sentence. Requirements and tickets are written in prose, not pre-sorted into inputs and
> outputs - that sorting is real analytical work a tester has to do deliberately, and skipping it produces
> either an inflated, wrong-shaped table or one that's silently missing a chained second decision
> entirely.

**Quiz.** A ticket reads: 'Premium members with an active subscription get free returns. Premium status is granted automatically once a customer's lifetime spend exceeds $500.' A tester lists three conditions: 'lifetime spend exceeds $500', 'active subscription', and 'premium status'. What's the issue?

- [x] "Premium status" is actually an ACTION (the output of a separate, earlier decision based on lifetime spend) - it should be modeled as the output of one small table, then correctly used as a genuine condition of the free-returns table, not lumped in as a third independent input to one inflated table
- [ ] There's no issue - all three items plausibly vary independently, so treating them as three conditions of one table is the correct approach
- [ ] "Active subscription" is the real action here, not "premium status", and the table should be rebuilt around that instead
- [ ] The ticket is missing a fourth condition, and no valid decision table can be built until that gap is filled by the requirements owner

*'Premium status' is explicitly described as something 'granted automatically once lifetime spend exceeds $500' - by this note's own test (could this exist before any decision is made?), it fails: it only comes into existence AS the result of evaluating lifetime spend. That makes it an action of a separate, smaller decision, exactly the pattern in this note's WorkedExample. The correct model is two chained tables: one deciding premium status from lifetime spend, and a second (free returns) that correctly treats premium status as a genuine condition once it already exists as a settled fact. Lumping it in as a third independent condition of one table inflates the rule count for no real reason and obscures the actual two-step structure of the business logic. 'Active subscription' shows no signs of being anyone's output in the ticket's wording, so there's no basis for treating it as the hidden action instead. And nothing about this scenario is actually missing information - the fix is correct MODELING of what's already there, not a request for more requirements.*

- **Condition vs action, in one line each** — Condition: an independent input, exists before any decision. Action: an output, exists only AS the result of evaluating conditions.
- **The fastest test for sorting a raw fact into condition or action** — Could this value exist BEFORE any decision is made, on its own? Yes = condition. Only exists as a result = action.
- **The single most common mistake in identifying conditions** — Treating an action - especially the output of an earlier, related decision - as if it were an independent condition. It silently doubles (or worse) the table for no real information gained.
- **What it means when an action feeds into a later decision** — Not a mistake - it means there are two separate decision tables chained together, not one. Model the first table's output, then use it as a genuine condition of the second.
- **How to check two candidate conditions are really independent** — Ask if knowing one tells you anything about the other. If they always move together in every real case you can think of, they may be one condition wearing two names.
- **Why an unexpectedly large decision table is worth double-checking** — It's a strong signal to re-verify no action got miscounted as a condition, before assuming the underlying business logic is genuinely that complex.

### Challenge

Find a real multi-factor business rule - a shipping policy, an access-control rule, a pricing rule,
anything where an outcome depends on more than one factor. List every fact and outcome it mentions,
unsorted. Apply the "could this exist before any decision is made" test to each one explicitly. Sort
the results into conditions and actions, and specifically check whether any action is secretly the
output of an earlier, smaller decision hiding inside the same rule - if you find one, describe the two
chained tables that should exist instead of one.

### Ask the community

> Condition/action sort check on this rule: `[quote the rule]`. I identified conditions `[list]` and actions `[list]`. Did I miss a disguised action hiding in the conditions list, or a chained decision I should have split into two tables?

The most useful replies name a SPECIFIC item they think is miscategorized and explain why using the
"before any decision" test - a general "looks right" doesn't actually test the sort.

- [ISTQB Glossary — decision table testing, the standard testing-certification definition](https://glossary.istqb.org/en_US/term/decision-table-testing)
- [Guru99 — Decision Table Testing, with worked examples](https://www.guru99.com/decision-table-testing.html)
- [BrowserStack — What is a Decision Table in Software Testing?](https://www.browserstack.com/guide/decision-table)
- [Software Testing Mentor — Decision Table Testing in Software Testing, tutorial #36](https://www.youtube.com/watch?v=jlbH9Wm0Z9U)

🎬 [Software Testing Tutorial #36 — Decision Table Testing in Software Testing](https://www.youtube.com/watch?v=jlbH9Wm0Z9U) (12 min)

- A condition is an independent input that exists before any decision. An action is an output that exists only as the RESULT of evaluating conditions.
- The fastest sorting test: could this value exist before any decision is made, on its own? If not, it's an action, not a condition.
- The most common mistake is treating an action - often the output of an earlier, chained decision - as an extra independent condition, which silently inflates the table for no real information gained.
- When an action feeds into a later decision, that's two separate chained tables, not one inflated table - model the first table's output, then use it as a genuine condition of the second.
- An unexpectedly large decision table is a signal to re-check the condition list for a disguised action before assuming the business logic itself is that complex.


---
_Source: `packages/curriculum/content/notes/test-design-techniques/decision-tables/conditions-and-actions.mdx`_
