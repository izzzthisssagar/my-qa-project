---
title: "Data-driven thinking"
tags: ["test-artifacts", "test-data", "track-a"]
updated: "2026-07-14"
---

# Data-driven thinking

*The previous notes treated one test case and its data as a pair. Data-driven thinking is what happens when you stop writing a new test for every new scenario and instead add a new row to a table - the same logic, run against many rows at once.*

> Five nearly-identical test functions, each hardcoding one slightly different input and expected result,
> is a maintenance trap waiting to happen - change the underlying logic once, and now five copies need
> updating instead of one. Data-driven thinking is the fix: write the check ONCE, put the five scenarios in
> a table, and let the same logic run against every row. Adding a sixth scenario becomes adding a row, not
> writing new code.

> **In real life**
>
> A tray of identical star-shaped cookie cutters, pressed into rolled-out dough in row after row, uses the
> exact same cutting shape every single time - the shape itself never changes from cut to cut. What
> changes is which patch of dough each cutter lands on. Nobody re-designs the star shape for the third
> cookie or the fortieth; the shape is fixed, reused, and applied repeatedly across different material.
> That's data-driven thinking in physical form: one fixed "logic" (the cutter shape), run repeatedly
> against many different "data" inputs (the dough underneath each one).

**Data-driven thinking**: Data-driven thinking is the practice of separating a test's LOGIC (the steps and the assertion) from its DATA (the specific inputs and expected outputs), so the same logic runs once against a table, list, or spreadsheet of many data rows instead of being duplicated once per scenario. Adding a new test scenario becomes adding a new row of data, not writing new test code. Most test frameworks support this directly - JUnit's @ParameterizedTest, pytest's @pytest.mark.parametrize - but the mindset matters even without a framework feature: whenever you notice several near-identical test functions differing only in their input values, that's a signal the logic and the data should be separated.

## One function, many rows, not many functions

The signal that a set of tests wants to become data-driven is duplication: several test functions that
are byte-for-byte identical except for the specific numbers or strings plugged in. Once you notice that
pattern, the fix is almost always the same - extract the shared logic into one function, and turn the
varying values into a table the function is run against.

## A new scenario is a new row, not new code

This is the actual payoff. Once the logic/data split exists, covering a newly-discovered edge case is as
cheap as adding one line to a table - no new function, no risk of accidentally writing the assertion
slightly differently the sixth time than the first.

## The table itself becomes documentation

A well-organized data table, with a clear label column, reads almost like a spec: every row states a
scenario and its expected outcome in one glance. This is a real, additional benefit beyond just reducing
duplicated code - the table is often the clearest, most complete description of the behavior that exists
anywhere in the codebase.

![A close-up view of many identical star-shaped metal cookie cutters pressed into rolled-out dough, arranged in repeated rows extending into a blurred background, with a light dusting of flour visible on some of the metal edges](data-driven-thinking.jpg)
*Cutting ginger snaps.jpg — Wikimedia Commons, CC BY-SA (BenFrantzDale)*
- **One cutter, closest in frame = the single, fixed test LOGIC** — Written once - the same shape (the same assertion) applied identically every time, never redesigned per use.
- **The full grid extending into the background = the same logic applied to every data row** — Dozens of identical shapes, not dozens of different tools - the visual equivalent of one test function running against a whole table of scenarios.
- **The dough visible inside one cutter = the specific data for that one row** — Different patch of dough under each identical shape - exactly like different input values feeding the same fixed test logic.
- **The consistent star shape repeated everywhere = the assertion staying identical across rows** — The check being performed never varies row to row - only the values being checked do.
- **Flour dusting on some cutters, not others = natural variation between runs that doesn't affect the shape itself** — Small real-world differences between cuts don't change the underlying tool - just like incidental differences in test output formatting don't change the core logic being tested.

**Turning duplicated tests into one data-driven test - press Play**

1. **Notice several near-identical test functions** — Same steps, same assertion shape, different hardcoded input values - the signal to look for.
2. **Extract the shared logic into one function** — Parameters in, a result out - no scenario-specific values baked into the function itself.
3. **Move each scenario's values into a data table** — A label, the inputs, and the expected result - one row per scenario.
4. **Run the one function against every row** — Automatically, via a framework feature (@ParameterizedTest, @pytest.mark.parametrize), or manually in a loop.
5. **Add a new scenario as a new row, going forward** — The payoff - covering a new edge case never requires touching the test logic again.

*Run it - one shipping-cost function, five data rows (Python)*

```python
# The LOGIC is written once. Adding a scenario means adding a row, not new code.
def calculate_shipping(subtotal, is_member):
    if is_member:
        return 0.0
    if subtotal >= 50:
        return 0.0
    return 5.99

test_data_table = [
    {"case": "member, small order",    "subtotal": 12.00, "is_member": True,  "expected": 0.0},
    {"case": "non-member, under $50",  "subtotal": 30.00, "is_member": False, "expected": 5.99},
    {"case": "non-member, exactly $50","subtotal": 50.00, "is_member": False, "expected": 0.0},
    {"case": "non-member, over $50",   "subtotal": 75.00, "is_member": False, "expected": 0.0},
    {"case": "member, large order",    "subtotal": 200.00,"is_member": True,  "expected": 0.0},
]

print(f"{'Case':28} {'Subtotal':10} {'Member':8} {'Expected':10} Result")
failures = 0
for row in test_data_table:
    actual = calculate_shipping(row["subtotal"], row["is_member"])
    passed = actual == row["expected"]
    if not passed:
        failures += 1
    status = "PASS" if passed else "FAIL"
    print(f"{row['case']:28} {row['subtotal']:<10} {str(row['is_member']):8} {row['expected']:<10} {status}")

print(f"\\n{len(test_data_table) - failures}/{len(test_data_table)} rows passed, using ONE test function.")

# Case                         Subtotal   Member   Expected   Result
# member, small order          12.0       True     0.0        PASS
# non-member, under $50        30.0       False    5.99       PASS
# non-member, exactly $50      50.0       False    0.0        PASS
# non-member, over $50         75.0       False    0.0        PASS
# member, large order          200.0      True     0.0        PASS
#
# 5/5 rows passed, using ONE test function.
```

Same table-driven pattern in Java - the shape a JUnit `@ParameterizedTest` conceptually mirrors:

*Run it - the same shipping-cost check, one function, five rows (Java)*

```java
import java.util.*;

public class Main {

    static double calculateShipping(double subtotal, boolean isMember) {
        if (isMember) return 0.0;
        if (subtotal >= 50) return 0.0;
        return 5.99;
    }

    static class Row {
        String label;
        double subtotal, expected;
        boolean isMember;
        Row(String label, double subtotal, boolean isMember, double expected) {
            this.label = label;
            this.subtotal = subtotal;
            this.isMember = isMember;
            this.expected = expected;
        }
    }

    public static void main(String[] args) {
        List<Row> testDataTable = Arrays.asList(
            new Row("member, small order", 12.00, true, 0.0),
            new Row("non-member, under $50", 30.00, false, 5.99),
            new Row("non-member, exactly $50", 50.00, false, 0.0),
            new Row("non-member, over $50", 75.00, false, 0.0),
            new Row("member, large order", 200.00, true, 0.0)
        );

        System.out.printf("%-28s %-10s %-8s %-10s %s%n", "Case", "Subtotal", "Member", "Expected", "Result");
        int failures = 0;
        for (Row row : testDataTable) {
            double actual = calculateShipping(row.subtotal, row.isMember);
            boolean passed = actual == row.expected;
            if (!passed) failures++;
            System.out.printf("%-28s %-10s %-8s %-10s %s%n", row.label, row.subtotal, row.isMember, row.expected, passed ? "PASS" : "FAIL");
        }

        System.out.println();
        System.out.println((testDataTable.size() - failures) + "/" + testDataTable.size() + " rows passed, using ONE test function.");
    }
}

/* Case                         Subtotal   Member   Expected   Result
   member, small order          12.0       true     0.0        PASS
   non-member, under $50        30.0       false    5.99       PASS
   non-member, exactly $50      50.0       false    0.0        PASS
   non-member, over $50         75.0       false    0.0        PASS
   member, large order          200.0      true     0.0        PASS

   5/5 rows passed, using ONE test function. */
```

> **Tip**
>
> Notice `calculate_shipping` never mentions "member" or "small order" anywhere in its own code - all of
> that scenario-specific meaning lives in the table, in the `case` label and the row's values. That
> separation is the entire point: the function stays generic and reusable, and the table carries all the
> scenario-specific knowledge.

### Your first time: Your mission: turn duplicated tests into one data-driven test

- [ ] Find (or write) 3+ test functions that are nearly identical except for hardcoded values — A validation rule tested with several different inputs is a common, easy example.
- [ ] Extract the shared logic into a single function, with the varying values as parameters — Nothing scenario-specific should remain hardcoded inside the function body.
- [ ] Build a data table: one row per scenario, with a clear label, inputs, and expected result — Mirror this note's playground structure - it doesn't need to be fancy, just complete.
- [ ] Run the one function against every row and confirm all original scenarios still pass — This proves the refactor didn't quietly lose any of the original coverage.
- [ ] Add one brand-new scenario as a new row only - no new function — This is the actual payoff - confirm it really is just a one-line addition.

You converted duplicated, hard-to-maintain tests into one reusable check driven by a table - and proved that covering a new scenario going forward is now a one-line change, not a new function.

- **We have a dozen test functions that are almost identical, and every time the underlying logic changes, someone forgets to update one of them.**
  This is the exact signal this note describes - extract the shared logic into one function and move the dozen scenarios into a data table. A future logic change then only needs updating in one place.
- **I'm not sure a scenario is different enough to deserve its own table row versus being folded into an existing one.**
  If it produces a genuinely different expected result, or exercises a different branch of the logic, it earns its own row - rows should represent meaningfully distinct behavior, not just superficially different-looking inputs that all hit the same path.
- **Our data table has grown to 40+ rows and it's getting hard to see what each one is actually testing.**
  This is where the label column earns its keep - make sure every row has a clear, specific description, not just raw values. If groups of rows share a theme, consider splitting into multiple smaller tables by theme rather than one giant undifferentiated list.
- **A data-driven test failed, but the failure message just shows a row index, not what scenario it was.**
  This is a sign the table's label column isn't being surfaced in the failure output - most parameterized-test frameworks support naming each run from the row's label field specifically to avoid this exact problem.

### Where to check

Where data-driven thinking pays off the most:

- **Validation logic with many input classes** — exactly the equivalence-partitioning and boundary-value scenarios from an earlier module, naturally expressed as table rows.
- **Business rules with several distinct cases** — a shipping-cost rule, a discount calculation, a pricing tier - anywhere "if X then Y" branches multiply.
- **Any set of near-duplicate test functions you find during review** — the strongest, most concrete signal that a refactor to data-driven form is worth the effort.
- **Regression suites that need to grow over time** — new scenarios arriving as new rows keeps the suite's growth cheap and low-risk.
- **NOT every single test in a suite** — a one-off test with a single meaningful scenario doesn't need a table; forcing data-driven structure onto genuinely unique tests adds ceremony without benefit.

The habit: **whenever you notice several test functions differing only in their hardcoded values, that's the signal to separate logic from data.**

### Worked example: collapsing five duplicated tests into one, and catching a real inconsistency in the process

1. **A codebase has five separate test functions** for a discount-code validator: `test_valid_code`, `test_expired_code`, `test_wrong_format_code`, `test_empty_code`, `test_case_sensitivity`.
2. **Reading all five**, they share the exact same three steps (submit a code, check the result, check the message) and differ only in the specific code string and expected outcome.
3. **A developer extracts the shared steps into one function**, `check_discount_code(code, expected_valid, expected_message)`, and builds a table with the five original scenarios as rows.
4. **Running the new data-driven version against all five rows** reproduces the original five test results exactly - no regression, same coverage.
5. **While filling in the table's expected-message column**, the developer notices `test_wrong_format_code` and `test_empty_code` were using DIFFERENT error message text for what's actually the same underlying validation failure - a real inconsistency in the application's own error messaging, invisible while the tests were five separate, rarely-compared functions.
6. **This inconsistency was always there** - it just wasn't visible until the scenarios were side by side in one table, where a mismatched pattern is obvious at a glance.
7. **The team fixes the application to use one consistent message for both cases**, and the table's expected column gets updated to match - a real product improvement that came directly from the refactor, not just a maintenance cleanup.
8. **A sixth scenario (a code with leading/trailing whitespace) is discovered a week later** and added as a single new row - no new function, no risk of copying the assertion pattern incorrectly a sixth time.

> **Common mistake**
>
> Treating data-driven refactoring as pure mechanical cleanup with no side benefit. The worked example
> above shows the real, additional value: putting scenarios side by side in one table surfaced a genuine
> inconsistency in the application's own error messages that five separate, rarely-compared test functions
> had been quietly hiding. The table isn't just less code - it's often a clearer view of the actual
> behavior than the original scattered tests ever provided.

**Quiz.** A team has 8 near-identical test functions differing only in hardcoded input values. What does this note say is the first, most direct signal to look for, and what's the concrete first step?

- [x] The signal is functions differing only in hardcoded values; the first step is extracting the shared logic into ONE function and moving the varying values into a data table with one row per original scenario
- [ ] The signal is having more than 5 test functions in a single file; the first step is splitting them across multiple files regardless of whether their logic is actually duplicated
- [ ] The signal is slow test execution time; the first step is deleting the slowest-running functions to speed up the suite, regardless of what unique scenarios they cover
- [ ] There is no reliable signal to look for; whether to use data-driven testing is purely a stylistic preference with no real technical trade-off either way

*This note is explicit and consistent throughout: the signal is 'several near-identical test functions differing only in their input values' (stated directly in the Term definition, the WhereToCheck section, and demonstrated in the worked example's five near-duplicate functions), and the concrete first step is extracting shared logic into one function with scenarios moved into a data table - exactly what both code playgrounds demonstrate. File count has nothing to do with the actual signal this note describes - splitting files without addressing genuine logic duplication wouldn't solve anything this note is concerned with. Deleting slow-running tests to fix duplication is both unrelated to the note's actual topic and would destroy real coverage rather than consolidating it safely. And the note explicitly frames this as a real technical trade-off with concrete benefits (single point of maintenance, cheaper new-scenario coverage, the table itself as documentation) - not a matter of pure style with no substance behind it.*

- **The core idea of data-driven thinking** — Separate a test's LOGIC (written once) from its DATA (many rows) - one function run against a table instead of many near-duplicate functions.
- **The clearest signal it's time to refactor toward data-driven testing** — Several test functions that are nearly identical except for their hardcoded input/expected values.
- **The concrete payoff of the logic/data split** — A new test scenario becomes adding one row to a table, not writing a new function.
- **An unexpected benefit of building the data table** — Putting scenarios side by side can surface real inconsistencies (like mismatched error messages) that were invisible across separate, rarely-compared test functions.
- **When NOT to force data-driven structure** — On a one-off test with a single genuinely unique scenario - forcing a table adds ceremony without real benefit there.
- **Framework features that implement this pattern directly** — JUnit's @ParameterizedTest and pytest's @pytest.mark.parametrize - though the mindset applies even without a framework feature.

### Challenge

Find (or deliberately write) 3 near-identical test functions differing only in hardcoded values. Refactor
them into one function driven by a data table, following this note's pattern. Confirm all original
scenarios still pass, then add one brand-new scenario as a single new row and confirm it required no
changes to the function itself.

### Ask the community

> Data-driven refactor report: collapsed `[N]` near-duplicate tests into 1 function + a `[N]`-row table for `[feature]`. Did building the table surface anything - an inconsistency, a missing scenario - that wasn't obvious before?

The most useful replies describe a SPECIFIC thing the table surfaced (a mismatched expected value, a
missing edge case) rather than a general "yes, tables are clearer" comment.

- [QA Skills — Data-Driven Testing: Complete Guide with Frameworks](https://qaskills.sh/blog/data-driven-testing-complete-guide)
- [Automation Rhapsody — Data Driven Testing with JUnit Parameterized Tests](https://automationrhapsody.com/data-driven-testing-junit-parameterized-tests/)
- [Pytest with Eric — Pytest Parameterized Tests](https://pytest-with-eric.com/introduction/pytest-parameterized-tests/)
- [EvilTester — How to Write a Data Driven Test in JUnit 4](https://www.youtube.com/watch?v=9KLtQdBSqJo)

🎬 [How to Write a Data Driven Test in JUnit 4 — Parameterized Unit Test](https://www.youtube.com/watch?v=9KLtQdBSqJo) (11 min)

- Data-driven thinking separates test LOGIC (written once) from test DATA (many rows) - one function run against a table.
- The signal to look for: several near-identical test functions differing only in hardcoded input/expected values.
- The real payoff: a new scenario becomes a new table row, not new test code.
- An unexpected bonus: a well-built data table can surface real inconsistencies that were invisible across separate, rarely-compared tests.
- Not every test needs this - genuinely one-off scenarios don't benefit from forced table structure.


---
_Source: `packages/curriculum/content/notes/test-artifacts/test-data/data-driven-thinking.mdx`_
