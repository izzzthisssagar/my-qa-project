---
title: "Use-case testing"
tags: ["test-design-techniques", "error-guessing-and-use-cases", "track-a"]
updated: "2026-07-14"
---

# Use-case testing

*Every other technique in this module tests one field or one decision in isolation. Use case testing zooms out to test an entire multi-step journey toward a user's goal - and the exception flows are where it earns its keep.*

> Equivalence partitioning tests one field. Boundary value analysis tests one threshold. A decision table
> tests one combination of conditions. None of them test the thing a real user actually experiences: a
> multi-step journey toward a goal, where step three's success depends on step two having gone a specific
> way. Use case testing is the technique built for that shape - and it explicitly plans for the journey
> going sideways, not just for it going right.

> **In real life**
>
> A TSA checkpoint has a documented main path - join Lane 1, show ID, wait for clearance, proceed - and
> it also has a real, signposted alternate path (TSA PreCheck) that reaches the exact same destination
> through a different sequence of steps. Both are legitimate, both are worth walking through deliberately.
> But the checkpoint also has to handle what happens when someone's ID doesn't scan, or they step past the
> "Please Wait Here" sign before being called - genuine deviations from either documented path, and the
> system has to recover gracefully from those too, not just from the two paths that go according to plan.
> A use case works exactly the same way: one main flow, one or more real alternate flows, and exception
> flows for when something goes wrong along any of them - all three deserve deliberate testing.

**Use case / main flow / alternate flow / exception flow**: A use case is a sequence of steps a user takes to accomplish a specific goal. The MAIN SUCCESS SCENARIO (or 'happy path') is the most common, complete sequence that achieves the goal without any deviation. An ALTERNATE FLOW is a different sequence that still successfully achieves the same goal - not an error, just a different valid route (applying a promo code before payment, for instance). An EXCEPTION FLOW is what happens when something goes wrong along the way (a declined payment, an expired session) - the system should still respond usefully, ideally recovering back into a workable state rather than leaving the user stuck. Use case testing writes and runs test cases for all three categories, not just the main scenario.

## The main success scenario is the easy, obvious part

Every use case starts here: the single, most complete, straight-line sequence of steps from goal to
completion. It's the version everyone naturally thinks of first when describing a feature, and the
version most likely to already be tested even without deliberate use-case-testing discipline.

## Alternate flows are valid detours, not mistakes

An alternate flow still reaches the goal successfully - it just gets there differently. Applying a
promo code before entering payment, choosing express shipping instead of standard, logging in via a
third-party provider instead of a password: none of these are errors, and each deserves its own
end-to-end test confirming the DIFFERENT sequence still reaches the same successful outcome.

## Exception flows are where use case testing earns its keep

This is the category most likely to get skipped under time pressure, and the one with the highest
payoff: what happens when a step in the sequence fails partway through? A declined payment, a session
timeout mid-form, a network failure between two steps - the system's job isn't just to detect the
failure, it's to leave the user in a coherent, recoverable state, not a broken or inconsistent one.

![A TSA airport security checkpoint with a 'LANE 1' sign, a TSA officer checking a traveler's ID at a podium, a 'TSA PreCheck' sign visible in the background marking an alternate lane, a black 'Please Wait Here' sign in the foreground, and a Travel Advisory information screen to the right](use-case-testing-technique.jpg)
*Transportation Security Administration Checkpoint at John Glenn Columbus International Airport — Wikimedia Commons, CC0 (Public Domain)*
- **LANE 1 = the entry point into the MAIN success scenario** — This is where the primary, most common path through security begins - the sequence of steps a typical traveler follows start to finish, exactly what a use case's main success scenario documents first.
- **The officer checking ID = one necessary, well-defined step within that main flow** — This step has to happen, in this position, before the traveler can proceed - a use case's main scenario is a specific ORDERED sequence of steps like this one, not just a list of things that eventually need to occur.
- **TSA PreCheck signage = a documented ALTERNATE flow to the identical goal** — A different, faster sequence of steps - but ending at the exact same destination as the main lane: through security, to the gate. A use case's alternate flows are exactly this: different valid paths to the same goal, each deserving its own test.
- **'Please Wait Here' = an explicit required step, easy to accidentally skip when only imagining the happy path** — A traveler who steps around this sign has deviated from the documented flow - whether that's harmless or a real problem is exactly the kind of exception case a thorough use case analysis has to consider on purpose.
- **The Travel Advisory screen = context alongside the journey, not a step within it** — This information is available, but skipping it entirely doesn't stop anyone from reaching the gate. Not everything visible in a flow is actually part of the use case's real sequence of required steps - telling the two apart matters.

**Testing all three flow types for one use case - press Play**

1. **Write the main success scenario as an ordered step list** — The single, complete, straight-line sequence from goal to completion - the version everyone thinks of first.
2. **Identify every REAL alternate route to the same goal** — Not errors - valid detours. A promo code applied early, a different shipping choice, a different login method, all still reaching success.
3. **Identify every point in the main flow where something could go wrong** — Not just 'the payment step' broadly - the SPECIFIC step (entering payment details) and the SPECIFIC failure (declined) at that exact point.
4. **Test each flow type as its own complete run, not just individual steps** — Run the whole sequence end to end for the main flow, then again for each alternate flow, then again for each exception flow.
5. **For every exception flow, check the RECOVERY state specifically** — Not just 'did it show an error' - is the user left somewhere they can actually continue from, or stuck in a broken, inconsistent state?

Here's a checkout use case tested across all three flow types - main, alternate, and exception - with
the exception flow exposing a real recovery-state bug the other two flows never touch:

*Run it - testing main, alternate, and exception flows for one use case (Python)*

```python
class Checkout:
    def __init__(self):
        self.cart_items = 2
        self.status = "cart"

    def run_flow(self, steps):
        log = []
        for step in steps:
            result = getattr(self, step)()
            log.append(f"{step}: {result} (status={self.status}, cart_items={self.cart_items})")
        return log

    def review_cart(self):
        self.status = "reviewing"
        return "OK"

    def enter_payment(self):
        self.status = "payment_entered"
        return "OK"

    def confirm_order(self):
        self.status = "confirmed"
        self.cart_items = 0
        return "OK"

    def apply_promo_code(self):
        self.status = "promo_applied"
        return "OK"

    def payment_declined(self):
        # BUG: should reset status back to "payment_entered" so the user can retry,
        # but leaves status as "confirmed" from a stale previous attempt
        self.status = "confirmed"
        return "DECLINED"

print("MAIN SUCCESS SCENARIO: review -> pay -> confirm")
c1 = Checkout()
for line in c1.run_flow(["review_cart", "enter_payment", "confirm_order"]):
    print(" ", line)

print()
print("ALTERNATE FLOW: review -> apply promo -> pay -> confirm")
c2 = Checkout()
for line in c2.run_flow(["review_cart", "apply_promo_code", "enter_payment", "confirm_order"]):
    print(" ", line)

print()
print("EXCEPTION FLOW: review -> pay -> payment declined")
c3 = Checkout()
for line in c3.run_flow(["review_cart", "enter_payment", "payment_declined"]):
    print(" ", line)
print(f"  Final status after decline: {c3.status} (BUG: should be 'payment_entered' so user can retry, not 'confirmed')")

# MAIN SUCCESS SCENARIO: review -> pay -> confirm
#   review_cart: OK (status=reviewing, cart_items=2)
#   enter_payment: OK (status=payment_entered, cart_items=2)
#   confirm_order: OK (status=confirmed, cart_items=0)
#
# ALTERNATE FLOW: review -> apply promo -> pay -> confirm
#   review_cart: OK (status=reviewing, cart_items=2)
#   apply_promo_code: OK (status=promo_applied, cart_items=2)
#   enter_payment: OK (status=payment_entered, cart_items=2)
#   confirm_order: OK (status=confirmed, cart_items=0)
#
# EXCEPTION FLOW: review -> pay -> payment declined
#   review_cart: OK (status=reviewing, cart_items=2)
#   enter_payment: OK (status=payment_entered, cart_items=2)
#   payment_declined: DECLINED (status=confirmed, cart_items=2)
#   Final status after decline: confirmed (BUG: should be 'payment_entered' so user can retry, not 'confirmed')
```

Same three flows, same caught defect, in Java - the shape a real checkout service's flow orchestration
might take:

*Run it - main, alternate, and exception flow testing (Java)*

```java
import java.util.*;
import java.util.function.*;

public class Main {

    static class Checkout {
        int cartItems = 2;
        String status = "cart";
        Map<String, Supplier<String>> steps = new LinkedHashMap<>();

        Checkout() {
            steps.put("review_cart", this::reviewCart);
            steps.put("enter_payment", this::enterPayment);
            steps.put("confirm_order", this::confirmOrder);
            steps.put("apply_promo_code", this::applyPromoCode);
            steps.put("payment_declined", this::paymentDeclined);
        }

        String reviewCart() { status = "reviewing"; return "OK"; }
        String enterPayment() { status = "payment_entered"; return "OK"; }
        String confirmOrder() { status = "confirmed"; cartItems = 0; return "OK"; }
        String applyPromoCode() { status = "promo_applied"; return "OK"; }

        String paymentDeclined() {
            // BUG: should reset status back to "payment_entered" so the user can retry,
            // but leaves status as "confirmed" from a stale previous attempt
            status = "confirmed";
            return "DECLINED";
        }

        void runFlow(String[] flowSteps) {
            for (String step : flowSteps) {
                String result = steps.get(step).get();
                System.out.printf("  %s: %s (status=%s, cart_items=%d)%n", step, result, status, cartItems);
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("MAIN SUCCESS SCENARIO: review -> pay -> confirm");
        Checkout c1 = new Checkout();
        c1.runFlow(new String[]{"review_cart", "enter_payment", "confirm_order"});

        System.out.println();
        System.out.println("ALTERNATE FLOW: review -> apply promo -> pay -> confirm");
        Checkout c2 = new Checkout();
        c2.runFlow(new String[]{"review_cart", "apply_promo_code", "enter_payment", "confirm_order"});

        System.out.println();
        System.out.println("EXCEPTION FLOW: review -> pay -> payment declined");
        Checkout c3 = new Checkout();
        c3.runFlow(new String[]{"review_cart", "enter_payment", "payment_declined"});
        System.out.printf("  Final status after decline: %s (BUG: should be 'payment_entered' so user can retry, not 'confirmed')%n", c3.status);
    }
}

/* Output matches the Python run exactly. */
```

> **Tip**
>
> Look closely at the exception flow's final state: `status=confirmed` with `cart_items=2` still sitting
> in the cart. That combination is internally CONTRADICTORY - "confirmed" implies a completed purchase,
> but the cart still has unpurchased items and no charge went through. This is exactly the kind of
> inconsistent recovery state exception-flow testing is built to catch - not just "did an error appear,"
> but "is the resulting state actually coherent."

### Your first time: Your mission: test all three flow types for one real use case

- [ ] Pick a real multi-step user goal — Checkout, signup, password reset, booking a reservation - anything with a clear start, a clear goal, and more than one step in between.
- [ ] Write and run the main success scenario — The complete, straight-line sequence, step by step, confirming each one and the final successful outcome.
- [ ] Identify and run at least one real alternate flow — A different valid sequence reaching the same goal - not an error, a legitimate detour.
- [ ] Identify and run at least one exception flow — Deliberately break something partway through (a declined payment, an invalid entry mid-flow) and follow what happens next.
- [ ] Check the exception flow's FINAL state for internal consistency — Not just whether an error appeared - does the resulting state actually make sense, or does it contradict itself the way this note's example did?

You tested a complete user journey across all three flow types, not just the happy path - and specifically checked whether the system's exception recovery leaves a coherent state behind.

- **My exception flow test showed an error message, and I assumed that meant it was handled correctly.**
  An error message appearing is necessary but not sufficient - always check the resulting STATE too, the way this note's worked example does. A clean error message sitting on top of an internally contradictory state (like 'confirmed' with items still in the cart) is still a real defect, just a subtler one than a crash.
- **I can't tell if a deviation from the main flow is a legitimate alternate flow or actually an exception flow.**
  Ask whether it still reaches the SAME successful goal through a different valid path (alternate), or whether something has actually gone wrong and needs recovery (exception). Applying a promo code early is alternate; a declined payment is exception - the distinction is whether the outcome is still success, just achieved differently.
- **My use case has many possible alternate and exception flows, and testing all of them feels like too much.**
  Prioritize by real-world frequency and consequence, the same way earlier notes in this module suggested scaling effort - a payment decline is common and consequential, worth full testing; an extremely rare combination of simultaneous failures can reasonably be deprioritized, but should still be named and consciously deferred, not silently skipped.
- **I found an exception flow that leaves the system in a genuinely broken state, not just an inconsistent one.**
  Escalate this with real urgency and full reproduction steps - a broken (not just inconsistent) state after an exception flow often means data corruption or a stuck user with no path forward, which tends to generate real support burden until it's fixed.

### Where to check

Where use case testing matters most:

- **Any multi-step process with real business consequence** — checkout, signup, booking, onboarding: exactly where main, alternate, and exception flows all carry real weight.
- **Payment and financial transaction flows** — the exception flows here (declined cards, timeouts, partial failures) are both the most likely to occur in practice and the most costly to get wrong.
- **Flows with more than one legitimate path to success** — anywhere a user can reasonably choose between options (shipping methods, login providers, payment types) and expect all of them to work.
- **Any feature where support tickets mention being "stuck"** — a strong signal an exception flow's recovery state is leaving users somewhere they can't proceed from.
- **Newly built or recently redesigned multi-step flows** — fresh flows are exactly where exception handling gets the least attention relative to the main path, mirroring the same asymmetry this module's state-transition chapter described for invalid transitions.

The habit: **test the main flow, at least one real alternate flow, and at least one exception flow for every meaningful multi-step user journey - and check the exception flow's resulting state for genuine consistency, not just the presence of an error message.**

### Worked example: use case testing a password-reset flow, all three types

1. **The use case:** "A user resets a forgotten password." Goal: the user ends up able to log in with a new password.
2. **Main success scenario**: request reset -> receive email -> click link -> enter new password -> confirmation -> can log in with new password. Test this fully, end to end, confirming each step and the final login.
3. **An alternate flow**: the user requests a reset from the mobile app instead of the website - a different starting point, same underlying goal. Test this as its own complete run, not assumed identical just because the destination matches.
4. **An exception flow**: the user clicks the reset link after it's expired (a common, realistic failure). Trigger this deliberately and follow what happens.
5. **The main flow and alternate flow both pass cleanly** - new password set, login works in both cases. Confidence in the happy paths is earned.
6. **The exception flow reveals a problem.** The expired-link page shows a generic "something went wrong" message, but the ORIGINAL reset token is still marked as unused in the database - meaning if the user's email client somehow re-triggers the link (a browser prefetch, for instance), it could still silently succeed with a token the UI already told the user was expired.
7. **This is exactly the kind of internally-inconsistent recovery state this note is about hunting for** - the visible error message looked fine, but the underlying state didn't actually match what the error claimed.
8. **File the exact finding**: "expired reset-link page shows an error but doesn't invalidate the underlying token server-side - a stale request against the same token can still succeed. Reproduced by [specific steps]. Recommend invalidating the token the moment expiry is detected, not just showing a client-side message." A precise, exception-flow-specific defect that neither the main nor the alternate flow testing would ever have surfaced.

> **Common mistake**
>
> Testing only the main success scenario and calling a multi-step feature "tested." A use case with a
> real, well-tested happy path can still ship with a broken alternate flow or a recovery-breaking
> exception flow - this note's checkout example passed its main and alternate flows perfectly while its
> exception flow left the system in a contradictory state. The main flow being solid says nothing about
> the other two categories; each needs its own deliberate test.

**Quiz.** A tester writes and passes a test for a hotel booking flow's main success scenario (search dates, select room, pay, receive confirmation). They report the feature as fully tested. What does this note say is likely still missing?

- [x] Alternate flows (a different valid path to a successful booking, like applying a loyalty discount before payment) and exception flows (a declined payment, a room becoming unavailable mid-booking) - both categories test genuinely different scenarios the main flow alone never exercises
- [ ] Nothing is missing - once the main success scenario passes cleanly, a multi-step use case is considered fully tested by definition
- [ ] Only exception flows are missing; alternate flows are optional and rarely worth testing since they still reach the same successful outcome as the main flow
- [ ] The main success scenario needs to be re-run multiple times with different data before the use case can be considered even partially tested

*This note's core argument, demonstrated in its checkout worked example, is that a use case has three genuinely distinct categories - main, alternate, exception - and passing one says nothing about the other two. A loyalty-discount alternate path and a declined-payment exception path are both real, common scenarios completely untouched by a main-flow-only test, the same way this note's own checkout example passed its main and alternate flows cleanly while its exception flow revealed a genuine defect. Calling alternate flows 'optional' contradicts the note's explicit framing of them as valid, deserving-of-testing routes to the same goal, not corner cases to skip. And re-running the same main scenario repeatedly with different data doesn't address the actual gap here - it's still only exercising the ONE flow type, never touching the alternate or exception categories this note is specifically about.*

- **The three flow types in use case testing** — Main success scenario (the complete happy path), alternate flow (a different valid route to the same goal), exception flow (something goes wrong, system must recover usefully).
- **Alternate flow vs exception flow, the key distinction** — Alternate: still reaches SUCCESS, just via a different valid sequence. Exception: something has genuinely gone wrong and the system needs to recover gracefully, not just detect the failure.
- **Why check an exception flow's resulting STATE, not just its error message** — A clean-looking error can sit on top of an internally contradictory state (this note's 'confirmed' order with items still in cart) - the message alone doesn't prove the recovery was actually correct.
- **What makes use case testing different from EP, BVA, or decision tables** — It tests an entire multi-step JOURNEY toward a goal, not one field or one decision in isolation - the other techniques test components, use case testing tests the sequence connecting them.
- **Why exception flows are the highest-payoff category to test** — They're the most likely to get skipped under time pressure and the most likely to hide a real, consequential defect - the same asymmetry this module's state-transition chapter described for invalid transitions.
- **How to prioritize among many possible alternate/exception flows** — By real-world frequency and consequence - common, high-stakes ones (a declined payment) get full testing; rare, low-stakes ones can be consciously deferred, but named explicitly, not silently skipped.

### Challenge

Pick a real multi-step user goal you can test (checkout, signup, booking, password reset - anything with
a clear start and end and more than one step). Write and run the main success scenario fully. Identify
and run at least one genuine alternate flow. Identify and run at least one exception flow, deliberately
triggering a failure partway through. For the exception flow specifically, check the resulting state for
internal consistency, not just whether an error message appeared - report anything that looks
contradictory, the way this note's checkout and password-reset examples both did.

### Ask the community

> Use-case flow check on `[feature/goal]`: main flow `[steps]` passed. Alternate flow `[steps]` result: `[outcome]`. Exception flow `[steps + failure point]` result: `[outcome + resulting state]`. Does the exception flow's final state look internally consistent to you, or does anything about it look contradictory?

The most useful replies examine the SPECIFIC resulting state after the exception flow, not just
whether an error appeared - "looks handled" without checking the state doesn't test what this note is
asking about.

- [Study.com — Exception & Alternate Flow in Use Case](https://study.com/academy/lesson/exception-alternate-flow-in-use-case.html)
- [Visual Paradigm — Understanding Use Case Scenarios: Normal, Exception, and Alternative Paths](https://guides.visual-paradigm.com/understanding-use-case-scenarios-modeling-system-behavior-with-normal-exception-and-alternative-paths/)
- [aiotests — Testing Use Case Guide: Improve QA Efficiency](https://www.aiotests.com/blog/testing-use-case-guide)
- [Testing Shala — Use Case Testing With Example in Software Testing](https://www.youtube.com/watch?v=k8JOkRDrgCM)

🎬 [Use Case Testing With Example in Software Testing](https://www.youtube.com/watch?v=k8JOkRDrgCM) (6 min)

- Use case testing tests an entire multi-step journey toward a goal - main success scenario, alternate flows, and exception flows - not one field or decision in isolation.
- An alternate flow still reaches success through a different valid sequence; an exception flow means something genuinely went wrong and the system must recover usefully.
- A passing main success scenario says nothing about alternate or exception flows - each is a genuinely distinct category requiring its own deliberate test.
- For exception flows specifically, check the resulting STATE for internal consistency, not just whether an error message appeared.
- Exception flows are the highest-payoff category to test deliberately, precisely because they're the most likely to be skipped under time pressure and the most likely to hide a real defect.


---
_Source: `packages/curriculum/content/notes/test-design-techniques/error-guessing-and-use-cases/use-case-testing-technique.mdx`_
