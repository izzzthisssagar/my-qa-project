---
title: "What test data is"
tags: ["test-artifacts", "test-data", "track-a"]
updated: "2026-07-14"
---

# What test data is

*A test case says WHAT to check. Test data is the actual values you feed it to check it - and a test case without real, specific data attached is just an untested idea.*

> "Verify signup rejects users under 18" is a test case - a description of a check. It doesn't test
> anything by itself. The moment you actually run it, you need a real number: 17? 12? -5? "twenty"? Each
> of those is a different piece of test data, and each one exercises a genuinely different path through
> the code. The case tells you what to check; the data is what actually does the checking.

> **In real life**
>
> A pile of fresh ingredients gathered on a counter - mushrooms, a red pepper, greens, a lemon, a bag of
> shrimp - isn't a meal yet, and it isn't a recipe either. It's the raw material a recipe needs before
> anything can actually be cooked. A recipe that says "add protein and vegetables" is still just an idea
> until real ingredients are in front of you: this specific pepper, this specific bag of shrimp, not a
> protein and a vegetable in the abstract. Test data plays the exact same role for a test case - the case
> describes the dish, the data is what actually goes in the pot.

**Test data**: Test data is the concrete set of input values used when a test case is actually executed - specific numbers, strings, files, or records, as opposed to the test case's abstract description of what behavior to verify. The same test case can be run against many different test data sets, each exercising a different path: valid/typical data (the expected everyday case), boundary data (values at the edge of a valid range), invalid data (values that should be rejected), and malformed data (values in the wrong shape entirely, like a string where a number belongs). A test case with no data attached hasn't actually been run yet - it's still just a plan.

## The case describes; the data executes

"Rejects users under 18" is untestable on its own - it has no specific value to check against actual
system behavior. The moment you pick 17, or 18, or "twenty," you've moved from planning a check to
actually running one. This distinction matters because a test suite can look complete at the case level
while still being thin on the data actually feeding those cases.

## One case, many data sets, many different outcomes

The same signup-age test case can be run against five completely different data values, and each one
tells you something the others don't: does 25 (a typical valid value) work, does 18 (the exact boundary)
work, does 17 (just under the boundary) get correctly rejected, does "twenty" (the wrong data type
entirely) get handled without crashing, does -5 (an impossible but technically-numeric value) get
caught.

## Different categories of data test different failure modes

Valid data confirms the happy path works. Boundary data confirms the edges are drawn in the right place.
Invalid data confirms bad input gets rejected instead of silently accepted. Malformed data confirms the
system doesn't crash on genuinely wrong-shaped input. Each category earns its place - none of them is
optional if the goal is real confidence, not just a passing test count.

![A collection of fresh raw ingredients gathered on a granite countertop - mushrooms, a red bell pepper, leafy greens, green onions, a lemon, and a packaged bag of shrimp - assembled together before cooking begins](what-test-data-is.jpg)
*Tom Yum Ingredients (4297200768).jpg — Wikimedia Commons, CC BY 2.0 (Vegan Feast Catering)*
- **The whole red pepper = one complete, realistic data value** — A single, specific, usable input - exactly what a test case needs to actually execute, not an abstract description of 'a vegetable.'
- **The cluster of mushrooms = a batch of related but distinct data points** — Multiple similar values, each slightly different - the same idea as running one test case against several data points in the same category (several 'valid' ages, for instance).
- **The green onions, oddly shaped and irregular = an edge-case-shaped input** — Not every real input is tidy - some data naturally sits at an awkward shape or extreme, which is exactly where boundary and edge-case data earns its value.
- **The lemon among the vegetables = a different data TYPE mixed into the set** — A fruit standing out among vegetables mirrors malformed data - a value of the wrong shape or type entirely, which is exactly what tests that type-handling.
- **The packaged, labeled bag of shrimp = a sourced, pre-prepared data component** — Not gathered loose like the produce - already packaged and ready, the same role seeded or fixture data plays: prepared once, ready to use directly in a test run.

**From abstract case to concrete, executable check - press Play**

1. **Start with the test case's description** — "Rejects users under 18" - a plan, not yet something you can run.
2. **Pick a valid, typical data value** — Age 25 - confirms the ordinary, expected path actually works.
3. **Pick a boundary value** — Age 18 (should pass) and age 17 (should fail) - confirms the edge is drawn exactly where it should be.
4. **Pick invalid and malformed values** — A negative age, a non-numeric string - confirms bad input is rejected, not silently accepted or crashed on.
5. **Run the SAME case against every data set** — The case stays fixed; only the data changes - each run is a genuinely different check of the same behavior.

*Run it - one test case, five different test data sets (Python)*

```python
# A test CASE describes what to check. Test DATA is the concrete values fed into it.
test_case = "Verify signup rejects an age under 18 and accepts an age of 18 or older"

test_data_sets = [
    {"label": "valid, typical", "age": 25},
    {"label": "valid, boundary", "age": 18},
    {"label": "invalid, boundary", "age": 17},
    {"label": "invalid, malformed", "age": "twenty"},
    {"label": "invalid, negative", "age": -5},
]

def check_signup_age(age):
    if not isinstance(age, int):
        return "REJECTED - not a number"
    if age < 0:
        return "REJECTED - negative age"
    if age < 18:
        return "REJECTED - under 18"
    return "ACCEPTED"

print(f"Test case: {test_case}\\n")
print(f"{'Data set':20} {'Value':10} Result")
for data in test_data_sets:
    result = check_signup_age(data["age"])
    print(f"{data['label']:20} {str(data['age']):10} {result}")

# Test case: Verify signup rejects an age under 18 and accepts an age of 18 or older
#
# Data set             Value      Result
# valid, typical       25         ACCEPTED
# valid, boundary      18         ACCEPTED
# invalid, boundary    17         REJECTED - under 18
# invalid, malformed   twenty     REJECTED - not a number
# invalid, negative    -5         REJECTED - negative age
```

Same case, same five data sets, in Java - the shape a parameterized JUnit test might take:

*Run it - the same case against five data sets (Java)*

```java
import java.util.*;

public class Main {

    static String checkSignupAge(Object age) {
        if (!(age instanceof Integer)) return "REJECTED - not a number";
        int a = (Integer) age;
        if (a < 0) return "REJECTED - negative age";
        if (a < 18) return "REJECTED - under 18";
        return "ACCEPTED";
    }

    public static void main(String[] args) {
        String testCase = "Verify signup rejects an age under 18 and accepts an age of 18 or older";

        LinkedHashMap<String, Object> dataSets = new LinkedHashMap<>();
        dataSets.put("valid, typical", 25);
        dataSets.put("valid, boundary", 18);
        dataSets.put("invalid, boundary", 17);
        dataSets.put("invalid, malformed", "twenty");
        dataSets.put("invalid, negative", -5);

        System.out.println("Test case: " + testCase + "\\n");
        System.out.printf("%-20s %-10s %s%n", "Data set", "Value", "Result");
        for (Map.Entry<String, Object> entry : dataSets.entrySet()) {
            String result = checkSignupAge(entry.getValue());
            System.out.printf("%-20s %-10s %s%n", entry.getKey(), String.valueOf(entry.getValue()), result);
        }
    }
}

/* Test case: Verify signup rejects an age under 18 and accepts an age of 18 or older

   Data set             Value      Result
   valid, typical       25         ACCEPTED
   valid, boundary      18         ACCEPTED
   invalid, boundary    17         REJECTED - under 18
   invalid, malformed   twenty     REJECTED - not a number
   invalid, negative    -5         REJECTED - negative age */
```

> **Tip**
>
> Notice this is ONE test case run against FIVE data sets, not five separate test cases. That distinction
> matters for how you organize a suite - the case describes the behavior once; the data sets are what you
> actually vary to exercise different paths through it (this is exactly what boundary-value-analysis and
> equivalence-partitioning, from an earlier module, are systematic techniques for choosing well).

### Your first time: Your mission: separate a test case from its data, on purpose

- [ ] Pick a real test case you or someone else has written — Something with a clear pass/fail condition - a form validation rule works well.
- [ ] Write down the case's description alone, with no specific values — Confirm it's genuinely abstract - it shouldn't be executable as written.
- [ ] List at least one data value from each category: valid, boundary, invalid, malformed — Four distinct values minimum, each testing something the others don't.
- [ ] Run (or trace through) the case against each data value separately — Confirm each one produces a genuinely different, informative result.
- [ ] Note which category, if any, was missing from the original test before you did this — Most real-world gaps show up here - a case that only ever got run against valid data, for instance.

You practiced the core distinction this whole chapter of notes builds on - a test case is a plan, and test data is what actually makes it real.

- **Our test suite has hundreds of passing cases but bugs keep slipping through on unusual inputs.**
  Check whether those cases are actually being run against a genuinely varied set of data, or just against one comfortable 'happy path' value repeatedly. A high case count with thin, repetitive data behind it gives false confidence.
- **I wrote a test case but I'm not sure what specific values to actually use for it.**
  Work through the four categories from this note explicitly: what's a typical valid value, what's right at the boundary, what's clearly invalid, and what's the wrong shape entirely (malformed). That's usually enough to get a solid starting set.
- **A bug reached production with an input type nobody thought to test - like a decimal age instead of a whole number.**
  This is a malformed-data gap specifically - the case existed, but the data set behind it never included a wrong-shaped value. Add it now, and consider it a standing category to check for on future cases too.
- **My test data all looks realistic, but it's not actually testing anything interesting - just typical, unremarkable values.**
  Typical valid data alone only proves the happy path works - deliberately add boundary and invalid values, which is usually where the genuinely interesting bugs live.

### Where to check

Where the case/data distinction actually matters:

- **Reviewing test coverage claims** — a high case count says little without knowing what data actually ran behind each one.
- **Debugging a slipped-through bug** — often the case existed but the specific data value that broke things was never tried.
- **Writing a new test case from scratch** — deliberately picking data from all four categories (valid, boundary, invalid, malformed) up front, not as an afterthought.
- **Parameterized/data-driven test frameworks** — these exist specifically to run one case against many data sets efficiently; recognizing the case/data split is what makes them make sense.
- **NOT a reason to write a separate test case per data value by default** — often one well-designed case run against several data sets is more maintainable than duplicating the case's logic repeatedly.

The habit: **whenever you write or review a test case, ask what specific data it actually runs against - a case is only as good as the data behind it.**

### Worked example: a case that looked solid until its data was actually examined

1. **The test case**: "Verify the discount-code field rejects codes that have expired."
2. **On paper, this looks like a complete, well-scoped test.** It's in the suite, it's passing, nobody's worried about it.
3. **Looking at the actual data behind it**: the only data value ever used is a single code that expired exactly one year ago.
4. **That data value never actually tests the interesting boundary** - a code that expired YESTERDAY, or one expiring in the next hour, would exercise the real edge of the expiration logic far more precisely.
5. **A tester adds two new data values to the same case**: a code expiring in 1 minute (should still work) and a code that expired 1 minute ago (should be rejected).
6. **Running the case against the new boundary data reveals a real bug**: the expiration check compares dates, not full timestamps, so a code technically expired 30 seconds ago is still being accepted for the rest of that calendar day.
7. **The test CASE never needed to change.** Its description - "rejects expired codes" - was correct all along. The DATA behind it was too thin to actually catch the bug.
8. **This is the core lesson**: a passing test case tells you almost nothing about real coverage without knowing what data actually executed it.

> **Common mistake**
>
> Judging test coverage by counting test cases instead of examining the data behind them. The worked
> example above shows exactly how this goes wrong - a correctly-worded, passing test case that never
> actually exercised the boundary where the real bug lived, because its data was too thin (one comfortable
> value, reused indefinitely). A case is only as strong as the data actually run against it.

**Quiz.** A team says their signup form has '100% test coverage' because every field has at least one passing test case. What does this note say is the real, remaining question worth asking?

- [x] What DATA actually ran behind each of those cases - a passing case tells you almost nothing about real coverage without knowing whether it was run against typical, boundary, invalid, and malformed values
- [ ] Nothing further needs to be asked - if every field has at least one passing test case, that IS complete coverage by definition, regardless of what specific values were used
- [ ] Whether the test cases were written by a senior or junior tester, since case QUALITY is really about who authored it rather than what data values were actually exercised
- [ ] Whether the tests run fast enough in CI - execution speed is the deciding factor for whether test coverage claims should be trusted, not the values used

*This note's entire argument, reinforced directly by its worked example, is that a case count or a 'passing' status says very little on its own - the real substance is in the DATA actually run behind each case (typical, boundary, invalid, malformed). The worked example shows a correctly-worded, passing case that still missed a real bug because its data was too thin, which is precisely the scenario this quiz describes at suite scale. Coverage isn't complete 'by definition' just because every field has one passing case - that's the exact false confidence this note warns against. Who authored a case and how fast it runs are both irrelevant to the specific question this note raises, which is about the substance of the data behind the case, not authorship or performance.*

- **The core distinction this note teaches** — A test case describes WHAT to check (abstract); test data is the actual VALUES used to check it (concrete).
- **The four data categories worth deliberately covering** — Valid/typical, boundary, invalid, and malformed - each tests a genuinely different failure mode.
- **Why a high passing test-case count can still hide real gaps** — A case can be correctly worded and passing while its underlying data never exercised the boundary where a real bug actually lives.
- **What 'malformed' data specifically tests** — Input of the wrong TYPE or shape entirely (a string where a number belongs) - confirms the system doesn't crash on genuinely wrong-shaped input.
- **The relationship between one test case and multiple data sets** — One well-designed case can run against many data sets - the case stays fixed, the data varies to exercise different paths.
- **The habit this note is really teaching** — Whenever reviewing a test case, ask what specific data actually ran behind it - a case is only as strong as its data.

### Challenge

Take a real test case from a suite you have access to (or write a new one for a BuggyShop field). List
the actual data value(s) currently run against it, categorize each as valid/boundary/invalid/malformed,
and identify which category is missing. Add at least one data value from the missing category and report
whether it changes the result.

### Ask the community

> Test data audit on `[a test case]`: currently runs against `[N]` data value(s), covering `[categories]`. What's missing, and is it worth adding given the risk?

The most useful replies point at a SPECIFIC missing category and a plausible real bug it could catch,
rather than a general "always test more" comment.

- [Guru99 — What is Test Data in Software Testing?](https://www.guru99.com/software-testing-test-data.html)
- [BrowserStack — What is Test Data: Techniques, Challenges & Solutions](https://www.browserstack.com/guide/what-is-test-data)
- [Enov8 — Types of Test Data You Should Use for Your Software Tests](https://www.enov8.com/blog/types-of-test-data-you-should-use-for-your-software-tests/)
- [Software and Testing Training — Test Data in Software Testing](https://www.youtube.com/watch?v=XNZ2Pm2TAUs)

🎬 [Test Data in Software Testing — Test Data Generation](https://www.youtube.com/watch?v=XNZ2Pm2TAUs) (18 min)

- A test case describes what to check; test data is the concrete values that actually check it - a case with no data attached hasn't really been run.
- The four data categories worth deliberately covering: valid/typical, boundary, invalid, and malformed.
- One well-designed test case can run against many data sets - the case stays fixed, the data varies.
- A high passing test-case count says little on its own - the substance is in what data actually ran behind each case.
- The recurring habit: whenever reviewing a case, ask what data actually exercised it, not just whether it passed.


---
_Source: `packages/curriculum/content/notes/test-artifacts/test-data/what-test-data-is.mdx`_
