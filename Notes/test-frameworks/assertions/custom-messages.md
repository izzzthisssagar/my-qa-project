---
title: "Custom messages"
tags: ["test-frameworks", "assertions", "track-d"]
updated: "2026-07-17"
---

# Custom messages

*An assertion's optional message argument should explain WHY a value was expected - the business reason - not restate the expected and actual values the framework already prints automatically.*

> `assertEquals(expected, actual)` fails and JUnit already prints both values in the report - so a
> message that just says "values don't match" adds nothing. A message that says "discount should only
> apply to orders over $50" tells the next person, at 2am, exactly what business rule they just broke.

> **In real life**
>
> A pharmacy's auxiliary warning labels don't just print a generic hazard icon on a pill bottle. One
> reads "you should avoid prolonged exposure to direct and/or artificial sunlight while taking this
> medicine" - it states the actual reason, not just a fact the label's own color or shape already
> implies. A patient doesn't need a sun icon translated; they need to know why it matters for this
> specific medicine. A good assertion message does the same job for a test failure.

**Custom message**: A custom message is an optional argument passed to an assertion call - the last parameter in JUnit's assertEquals(expected, actual, message) and TestNG's assertEquals(actual, expected, message), or the text after the comma in Python's assert condition, message - that gets shown alongside the automatic expected/actual diff when the assertion fails. Its purpose is not to repeat what the framework already reports (the compared values), but to state the intent or business reason behind the check: why that value was expected, what rule or requirement it enforces, so a failure report answers 'why does this matter' as well as 'what differed.'

## Writing a message that earns its place in the report

```java
// Restates what the framework already shows - adds nothing
assertEquals(50.00, cart.getTotal(), "totals should be equal");

// Explains the actual business reason - this is what a message is for
assertEquals(50.00, cart.getTotal(),
    "orders under $50 should not receive free shipping discount");
```

```python
# Restates the comparison - pytest already shows expected vs actual on failure
assert cart.get_total() == 50.00, "total is wrong"

# Explains why this specific value matters
assert cart.get_total() == 50.00, (
    "free-shipping threshold is $50; a discount must not apply below it"
)
```

- **The framework already shows the diff** — `assertEquals` failures print the expected and actual
  values automatically; a message that repeats "expected X but got Y" is pure duplication.
- **A good message states intent** — the rule, requirement, or reason the check exists, in language
  a teammate unfamiliar with this specific test could understand without reading the code around it.
- **JUnit 5 also supports lazy messages** — passing a `Supplier` (a lambda) instead of a
  plain string means the message string is only built if the assertion actually fails, avoiding
  wasted work on the common case where it passes.
- **TestNG's argument order is reversed from JUnit's** — `Assert.assertEquals(actual, expected,
  message)` in TestNG vs `assertEquals(expected, actual, message)` in JUnit; the message is always
  last in both, but mixing up the first two arguments between frameworks is a common source of
  confusing "expected X but was X" failure reports.

> **Tip**
>
> Write the message as if explaining the failure to someone paging in at 2am who has never seen this
> test before. "Discount should only apply to orders over $50" orients them immediately; "totals do
> not match" sends them straight back to reading the whole test from scratch.

> **Common mistake**
>
> Writing a message that just restates the comparison in words - `assertEquals(actual, expected,
> "actual should equal expected")` or `assertTrue(isValid, "isValid should be true")`. This is pure
> noise: it repeats information the assertion framework already prints in its own failure output, and
> tells a future reader nothing about why the value was expected in the first place.

![Rows of pharmacy auxiliary warning label dispenser rolls holding colorful printed stickers with specific written instructions including a sunlight exposure warning, shake well, do not refrigerate, and for eyes](custom-messages.jpg)
*Auxiliary Labels — Wikimedia Commons, Public domain (U.S. Air Force photo by Staff Sgt. Ciara Wymbs). [Source](https://commons.wikimedia.org/wiki/File:Auxiliary_Labels.jpg)*
- **The orange sunlight-exposure label** — Spells out the actual reason - avoid direct and artificial sunlight while taking this medicine - not just a generic sun icon. This is what a good assertion message does: state the specific WHY.
- **"SHAKE WELL" — a plain restatement** — A short instruction with no reason attached - useful, but compare it to the sunlight label's fuller explanation. A message that only restates the check ("should be true") is this, without even the instruction's usefulness.
- **"DO NOT REFRIGERATE" — specific to this medicine** — Not a generic warning - a fact that matters for THIS item's specific handling requirement, the same way a good assertion message states the specific business rule that specific check enforces.
- **Rows of different labels for different reasons** — Each label exists because a specific, different fact needed stating - not one generic warning reused everywhere. Assertion messages should be this specific, not a copy-pasted generic string.

**A failure report with (and without) a useful message**

1. **assertEquals(50.00, cart.getTotal())** — No message. On failure: just 'expected 50.00 but was 45.00'.
2. **Reader sees the diff, not the reason** — They know WHAT differed, but not WHY 50.00 was expected in the first place.
3. **assertEquals(50.00, cart.getTotal(), "free-shipping threshold is $50")** — Same comparison, now with an intent-carrying message.
4. **Failure report: diff AND reason together** — "expected 50.00 but was 45.00" plus "free-shipping threshold is $50" - both facts, no extra investigation needed.
5. **Reader fixes the actual bug faster** — They immediately know which business rule broke, not just which numbers disagreed.

A custom message is really just: attach the reason a check exists to the check itself, so the
reason survives into the failure report. Here's that shape as a small, generic simulation - not
real JUnit or pytest internals, just the pattern underneath them.

*Run it - attach a reason to a check, not just a comparison (Python)*

```python
def assert_equals(actual, expected, message=None):
    if actual != expected:
        diff = f"expected {expected!r} but was {actual!r}"
        if message:
            raise AssertionError(f"{diff}\\n  reason: {message}")
        raise AssertionError(diff)
    print("  PASSED")

def check_no_message():
    cart_total = 45.00
    try:
        assert_equals(cart_total, 50.00)
    except AssertionError as e:
        print(f"FAILED\\n{e}")

def check_with_reason():
    cart_total = 45.00
    try:
        assert_equals(
            cart_total, 50.00,
            "free-shipping threshold is $50; a discount must not apply below it"
        )
    except AssertionError as e:
        print(f"FAILED\\n{e}")

print("-- no message --")
check_no_message()
print()
print("-- with reason --")
check_with_reason()
```

Same attach-a-reason shape in Java.

*Run it - attach a reason to a check, not just a comparison (Java)*

```java
public class Main {
    static void assertEqualsSim(double actual, double expected, String message) {
        if (actual != expected) {
            String diff = "expected " + expected + " but was " + actual;
            if (message != null) {
                throw new AssertionError(diff + "\\n  reason: " + message);
            }
            throw new AssertionError(diff);
        }
        System.out.println("  PASSED");
    }

    public static void main(String[] args) {
        double cartTotal = 45.00;

        System.out.println("-- no message --");
        try {
            assertEqualsSim(cartTotal, 50.00, null);
        } catch (AssertionError e) {
            System.out.println("FAILED");
            System.out.println(e.getMessage());
        }

        System.out.println();
        System.out.println("-- with reason --");
        try {
            assertEqualsSim(cartTotal, 50.00,
                "free-shipping threshold is $50; a discount must not apply below it");
        } catch (AssertionError e) {
            System.out.println("FAILED");
            System.out.println(e.getMessage());
        }
    }
}
```

### Your first time: Your mission: rewrite three assertions so their messages actually earn their place

- [ ] Find three assertions in a real test (yours or a project you can read) that have no message, or a message that just restates the comparison — Look for phrases like "should be equal" or "values should match."
- [ ] For each one, write down the actual business rule or reason the check exists, in one sentence — Ask: why THIS expected value, specifically, and not some other one?
- [ ] Rewrite each assertion with that sentence as its message argument — assertEquals(expected, actual, "<your sentence>") in JUnit, or assert cond, "<your sentence>" in Python.
- [ ] Deliberately break one of the checks and read the new failure report — Confirm it now tells you both what differed AND why that value mattered, without opening the test file.

You've now practiced the actual skill: distinguishing a message that repeats the diff from one that
explains the reason the check exists at all.

- **A failure message is technically present but just restates "expected X, got Y" - no new information beyond what the framework already prints.**
  Rewrite it to state the business rule or intent behind the check instead - ask why that specific expected value was chosen, not what it was.
- **In TestNG, a message shows up attached to the wrong value, or a failure report reads oddly like "expected: 45.00 but was 50.00" backwards from what's expected.**
  Check TestNG's argument order - Assert.assertEquals(actual, expected, message) - it's reversed from JUnit's assertEquals(expected, actual, message), and mixing the two up is a common, confusing mistake.
- **Building an assertion message is measurably slowing down a large, mostly-passing test suite.**
  In JUnit 5, switch from a plain String message to a Supplier lambda - it's only evaluated if the assertion actually fails, so expensive string-building work never runs on the passing path.
- **A message explains what the code does, not why the expected value is what it is.**
  That's a description, not a reason - rewrite it to name the requirement or business rule the check enforces ("orders under $50 don't get free shipping"), not a restatement of the code's mechanics.

### Where to check

- **The message argument itself, read in isolation from the code around it** — would it make sense
  to someone who has never seen this test file?
- **Whether the message repeats information the assertion already prints** — expected/actual values
  are automatic; a message repeating them is wasted words.
- **JUnit 5's Assertions API docs** — confirms which overloads accept a `String` vs a
  `Supplier` for lazy message evaluation.
- **TestNG's Assert Javadoc** — the definitive reference for exact argument order per overload,
  since it differs from JUnit's.

### Worked example: a message that turned a 20-minute investigation into a 20-second fix

1. A nightly test fails: `assertEquals(true, order.isEligibleForDiscount())` with no custom message -
   the report just says "expected true but was false."
2. A tester spends twenty minutes reading the discount-eligibility code, the order's field values, and
   the surrounding test setup to reconstruct why `true` was expected here at all.
3. They discover the actual rule: discounts only apply to orders placed by accounts older than 90
   days, and the test's seed data had an account created only 10 days ago - a seed-data bug, not a
   real feature bug.
4. They rewrite the assertion: `assertTrue(order.isEligibleForDiscount(), "accounts older than 90
   days should be discount-eligible; check seed data account age")`.
5. Three weeks later the same test fails again. This time the message alone identifies the seed-data
   suspect immediately - the fix takes twenty seconds, not twenty minutes, because the reason survived
   into the report.

**Quiz.** Which of these is the strongest custom assertion message for `assertEquals(50.00, cart.getTotal(), ???)`?

- [ ] "totals should match"
- [ ] "expected value was not equal to actual value"
- [x] "free-shipping threshold is $50; a discount must not apply to orders below it"
- [ ] "assertEquals failed"

*The note is explicit that a good message states the business reason or intent behind the check - option three is the only one that explains WHY 50.00 specifically was expected. Options one, two, and four all just restate that a comparison failed, which the framework's automatic expected/actual diff already communicates - they add no information a reader couldn't get from the bare assertion failure itself.*

- **What should a custom assertion message state?** — The intent or business reason behind the check - why that value was expected - not a restatement of the expected/actual values, which the framework already prints automatically.
- **JUnit's assertEquals argument order vs TestNG's** — JUnit: assertEquals(expected, actual, message). TestNG: Assert.assertEquals(actual, expected, message) - reversed first two arguments; the message is last in both.
- **What is a lazy message in JUnit 5, and why use one?** — Passing a Supplier lambda instead of a plain String - it's only evaluated if the assertion actually fails, avoiding wasted string-building work on the passing path.
- **The pharmacy auxiliary-label analogy for custom messages** — A sunlight-warning label states the specific reason (avoid sun exposure while on this medicine), not just a generic hazard icon - a good assertion message states the specific business rule, not just that values differed.
- **Example of a message that adds nothing** — "expected value was not equal to actual value" or "totals should be equal" - both just repeat what the framework's own expected/actual diff already shows.

### Challenge

Pick five assertions from a real test suite you can access. For each, rate its message (or lack of
one) as either "restates the diff" or "explains the reason." Rewrite every one rated "restates the
diff" so it states the actual business rule or intent instead, and confirm with a teammate (or by
rereading it cold a day later) that the new message would actually help someone unfamiliar with the
test understand a real failure.

### Ask the community

> I'm not sure how to phrase a custom message for this assertion so it explains the reason, not just the comparison: `[paste the assertion and what business rule it's meant to enforce]`.

Stating the actual business rule or requirement you're trying to check (not just the code) usually
gets a fast suggestion - the hard part is naming the reason, not the assertion syntax itself.

- [JUnit 5 — User Guide: Assertions](https://docs.junit.org/current/user-guide/#writing-tests-assertions)
- [Python — The assert statement (language reference)](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)

🎬 [JUnit 5 Basics 23 - Using supplier for assert messages — Java Brains](https://www.youtube.com/watch?v=S-hk1jFdZfA) (4 min)

- A custom assertion message should explain WHY a value was expected - the business reason - not restate the expected and actual values the framework already prints.
- JUnit's assertEquals(expected, actual, message) and TestNG's assertEquals(actual, expected, message) reverse the first two arguments - the message is always last.
- JUnit 5 supports lazy messages via Supplier, only building the string if the assertion actually fails.
- A message like "totals should be equal" adds nothing; a message like "free-shipping threshold is $50" tells a future reader exactly what rule broke.
- Writing a message as if explaining the failure to someone unfamiliar with the test is a reliable way to check whether it's actually useful.


## Related notes

- [[Notes/test-frameworks/assertions/assertions-basics|Assertions]]
- [[Notes/test-frameworks/assertions/soft-assertions|Soft assertions]]
- [[Notes/test-frameworks/assertions/matchers|Matchers]]


---
_Source: `packages/curriculum/content/notes/test-frameworks/assertions/custom-messages.mdx`_
