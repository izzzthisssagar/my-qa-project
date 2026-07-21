---
title: "Reviewing AI output critically"
tags: ["ai-and-the-modern-tester", "ai-as-your-testing-copilot", "track-c"]
updated: "2026-07-20"
---

# Reviewing AI output critically

*The core skill for working with AI test suggestions: checking whether a case maps to a real requirement, whether it duplicates existing coverage, and whether it would actually catch the bug it claims to.*

> Every technique in this chapter - brainstorming ideas, prompting well, generating data - produces
> output that reads as confident and finished. None of it is finished. An LLM cannot tell you which
> of its own suggestions actually matters to this product, because it does not know what this
> product's users have already been burned by. That judgment call is still entirely the tester's,
> every single time.

> **In real life**
>
> A car's GPS states the route, the speed limit, and the arrival time with total confidence - "50,"
> turn here, fourteen minutes - and it is usually right. What it cannot see is the rain starting on
> the windshield, the lane that closed an hour ago, or the fact that this particular turn floods
> every spring. A good driver treats the confident readout as a strong first draft of the trip, not
> the trip itself, and still looks up through the glass before committing to the turn. Reviewing AI
> output works the same way: the suggestion is confident and usually a reasonable starting point.
> Whether it is actually correct for the road you are really on is still your call.

**Reviewing AI output critically**: Reviewing AI output critically is the habit of checking any AI-suggested test case, test data, or claim against three questions before trusting it: does it map to a real, stated requirement; does it duplicate coverage that already exists; and would it actually fail if the bug it claims to catch were really present.

## Confident is not the same as correct

A suggested test case can be grammatically clean, plausibly worded, and completely disconnected
from anything this product actually promises. Fluent, well-structured output is not evidence of
correctness - it is evidence that the model is good at producing fluent, well-structured text. The
only way to know whether a suggestion is actually right is to check it against something real: the
spec, the existing suite, or the behavior of the running application.

## Does this map to a real requirement?

For every suggested case, find the exact sentence in the spec, ticket, or acceptance criteria it
is supposed to be testing. If there isn't one, the suggestion isn't wrong exactly - it's
unverified. It might be pointing at a genuine gap the spec never covered, which is worth raising
with whoever owns the spec. What it is not, yet, is a test case ready to add to the suite.

## Does this duplicate something already covered?

AI-generated lists restate the same underlying check in different wording more often than a
tester expects. "Verify login fails with an empty password" and "check that submitting the form
with no password shows an error" are the same test wearing two outfits. Counting them as separate
coverage inflates a suite's apparent size without adding anything real. Reduce each suggestion to
what it actually checks - which field, which condition, which expected outcome - before deciding
whether it's new.

## Would this actually catch the bug it claims to?

The final, easiest-to-skip check: read the suggested assertion and ask what would happen if the
bug it names were really there. A case that "verifies the error message appears" but only checks
that some element became visible would pass even if the error message said the wrong thing
entirely. A suggestion is only worth keeping once its actual assertion would genuinely fail against
the exact failure it claims to guard against.

> **Tip**
>
> Ask the three questions in order and stop as soon as one fails: no matching requirement means it
> doesn't graduate yet regardless of how clever it sounds; a duplicate gets merged regardless of how
> well-written it is; only a survivor of both needs the final, more careful assertion check.

> **Common mistake**
>
> Grading an AI-suggested list by its length or its prose quality. A list of twenty well-written
> suggestions that all restate the happy path, or all carry assertions too weak to fail against the
> bug they name, is worth less than three suggestions that are genuinely distinct, requirement-backed,
> and verified to actually catch something.

![A GPS navigation device mounted on a car dashboard, displaying a detailed street map with a navigation arrow, a red speed-limit circle showing 50, and rain visible on the windshield behind it](reviewing-ai-output-critically.jpg)
*Mio DigiWalker on Zhongshan North Road, Taipei - Tianmu peter, Wikimedia Commons, CC BY 3.0. [Source](https://commons.wikimedia.org/wiki/File:Mio_DigiWalker_on_Zhongshan_North_Road,_Taipei_20080912.jpg)*
- **A precise speed-limit reading** — Presented as plain fact - '50' - with nothing about it inviting a second look, the same way a well-worded AI suggestion invites you to accept it without checking the actual rule it claims to reflect.
- **The confident route arrow** — It states exactly where you are and where to turn next - useful, but only as good as the map data behind it, which cannot see anything the sensors and stored data didn't already capture.
- **Rain on the windshield the device can't see** — A real-world condition invisible to the system generating the confident readout - exactly like the business context and real user history an LLM was never given and cannot infer on its own.
- **'Start navigation' - one tap to just follow it** — The easy path is accepting the confident output and going; the safer habit is glancing at what's actually outside the windshield first.

**A three-question review pass**

1. **Read the suggestion at face value** — Note what it claims to test and what it claims would happen.
2. **Check it against the real requirement** — Find the exact spec sentence it maps to - if there isn't one, it isn't ready yet.
3. **Check it against existing coverage** — Reduce it to field, condition, and outcome - is this actually new, or a duplicate in different words?
4. **Check whether the assertion would really fail** — Would this case actually catch the bug it claims to, or does it only check that something happened at all?

*A duplicate/redundant test-case detector (Python)*

```python
# A duplicate/redundant test-case detector: an AI brainstorm often restates
# the same case in different words. Reduce each case to what it actually
# checks (subject, condition, expected outcome) before trusting the count.

AI_SUGGESTED = [
    "Verify login fails when the password is left blank",
    "Check that submitting the login form with an empty password shows an error",
    "Verify login succeeds with a valid email and password",
    "Test that an empty password field on login is rejected",
    "Verify login fails when the email has no @ symbol",
    "Check login with a correct email and correct password logs the user in",
]

def signature(text):
    t = text.lower()
    if "email" in t and ("no @" in t or "invalid" in t):
        subject = "email"
    elif "password" in t and "email" in t:
        subject = "credentials"
    elif "password" in t:
        subject = "password"
    elif "email" in t:
        subject = "email"
    else:
        subject = "unknown"

    if "blank" in t or "empty" in t:
        condition = "empty"
    elif "valid" in t or "correct" in t:
        condition = "valid"
    elif "no @" in t or "invalid" in t:
        condition = "invalid"
    else:
        condition = "unspecified"

    if "fails" in t or "error" in t or "rejected" in t:
        expected = "reject"
    elif "succeeds" in t or "logs the user in" in t or "logs in" in t:
        expected = "accept"
    else:
        expected = "unspecified"

    return (subject, condition, expected)

def find_duplicates(cases):
    seen = {}       # signature -> original case text
    kept = []
    duplicates = []
    for case in cases:
        sig = signature(case)
        if sig in seen:
            duplicates.append((case, seen[sig]))
        else:
            seen[sig] = case
            kept.append(case)
    return kept, duplicates

def main():
    kept, duplicates = find_duplicates(AI_SUGGESTED)

    print("AI suggested " + str(len(AI_SUGGESTED)) + " test cases.")
    print()
    print("Kept as distinct (" + str(len(kept)) + "):")
    for c in kept:
        print("  - " + c)

    print()
    print("Flagged as redundant (" + str(len(duplicates)) + "):")
    for case, original in duplicates:
        print("  - \\"" + case + "\\"")
        print("    same (subject, condition, outcome) as: \\"" + original + "\\"")

main()

# AI suggested 6 test cases.
#
# Kept as distinct (3):
#   - Verify login fails when the password is left blank
#   - Verify login succeeds with a valid email and password
#   - Verify login fails when the email has no @ symbol
#
# Flagged as redundant (3):
#   - "Check that submitting the login form with an empty password shows an error"
#     same (subject, condition, outcome) as: "Verify login fails when the password is left blank"
#   - "Test that an empty password field on login is rejected"
#     same (subject, condition, outcome) as: "Verify login fails when the password is left blank"
#   - "Check login with a correct email and correct password logs the user in"
#     same (subject, condition, outcome) as: "Verify login succeeds with a valid email and password"
```

*A duplicate/redundant test-case detector (Java)*

```java
import java.util.*;

public class Main {
    static final String[] AI_SUGGESTED = {
        "Verify login fails when the password is left blank",
        "Check that submitting the login form with an empty password shows an error",
        "Verify login succeeds with a valid email and password",
        "Test that an empty password field on login is rejected",
        "Verify login fails when the email has no @ symbol",
        "Check login with a correct email and correct password logs the user in",
    };

    static String[] signature(String text) {
        String t = text.toLowerCase();
        String subject;
        if (t.contains("email") && (t.contains("no @") || t.contains("invalid"))) subject = "email";
        else if (t.contains("password") && t.contains("email")) subject = "credentials";
        else if (t.contains("password")) subject = "password";
        else if (t.contains("email")) subject = "email";
        else subject = "unknown";

        String condition;
        if (t.contains("blank") || t.contains("empty")) condition = "empty";
        else if (t.contains("valid") || t.contains("correct")) condition = "valid";
        else if (t.contains("no @") || t.contains("invalid")) condition = "invalid";
        else condition = "unspecified";

        String expected;
        if (t.contains("fails") || t.contains("error") || t.contains("rejected")) expected = "reject";
        else if (t.contains("succeeds") || t.contains("logs the user in") || t.contains("logs in")) expected = "accept";
        else expected = "unspecified";

        return new String[] {subject, condition, expected};
    }

    public static void main(String[] args) {
        Map<String, String> seen = new LinkedHashMap<>();
        List<String> kept = new ArrayList<>();
        List<String[]> duplicates = new ArrayList<>(); // {case, original}

        for (String c : AI_SUGGESTED) {
            String[] sig = signature(c);
            String key = String.join("|", sig);
            if (seen.containsKey(key)) {
                duplicates.add(new String[] {c, seen.get(key)});
            } else {
                seen.put(key, c);
                kept.add(c);
            }
        }

        System.out.println("AI suggested " + AI_SUGGESTED.length + " test cases.");
        System.out.println();
        System.out.println("Kept as distinct (" + kept.size() + "):");
        for (String c : kept) System.out.println("  - " + c);

        System.out.println();
        System.out.println("Flagged as redundant (" + duplicates.size() + "):");
        for (String[] d : duplicates) {
            System.out.println("  - \\"" + d[0] + "\\"");
            System.out.println("    same (subject, condition, outcome) as: \\"" + d[1] + "\\"");
        }
    }
}

// AI suggested 6 test cases.
//
// Kept as distinct (3):
//   - Verify login fails when the password is left blank
//   - Verify login succeeds with a valid email and password
//   - Verify login fails when the email has no @ symbol
//
// Flagged as redundant (3):
//   - "Check that submitting the login form with an empty password shows an error"
//     same (subject, condition, outcome) as: "Verify login fails when the password is left blank"
//   - "Test that an empty password field on login is rejected"
//     same (subject, condition, outcome) as: "Verify login fails when the password is left blank"
//   - "Check login with a correct email and correct password logs the user in"
//     same (subject, condition, outcome) as: "Verify login succeeds with a valid email and password"
```

### Your first time: Run one AI-suggested list through a real review pass

- [ ] Get a raw list of AI-suggested cases for one real feature — Use the prompting habits from earlier in this chapter to get a decent starting list.
- [ ] Find the exact requirement each one claims to test — No matching sentence in the spec means it isn't ready to add yet.
- [ ] Group cases that test the same condition and keep one — Reduce each to subject, condition, and expected outcome before comparing.
- [ ] Check the assertion on each survivor — Would it actually fail if the exact bug it names were present, or does it only check that something happened?
- [ ] Only then add the survivors to the suite — With a clear expected result and a note on which requirement it covers.

- **A suggested case sounds specific but you can't point to what it's testing in the spec.**
  Treat it as an open question, not a finding - either it's pointing at a real gap worth raising, or it's a plausible-sounding guess that doesn't apply here.
- **Two suggested cases turn out to be the same test in different words.**
  Reduce both to subject, condition, and expected outcome; keep whichever is worded more clearly and drop the other.
- **A case passes today but wouldn't actually catch the bug it claims to prevent.**
  Check what the assertion really verifies - a check that only confirms something rendered, without checking its actual content or value, will pass even when the real bug is present.

### Where to check

- The actual spec or acceptance criteria, read side by side with every suggestion before it's accepted.
- The existing test suite or test management tool, to confirm a suggestion is genuinely new coverage.
- [[ai-and-the-modern-tester/ai-as-your-testing-copilot/llms-for-test-ideas-and-cases]] for where these raw suggestions come from in the first place.
- [[ai-and-the-modern-tester/ai-as-your-testing-copilot/generating-test-data-with-ai]] for applying this same review discipline to generated data, not just generated cases.

### Worked example: reviewing a suggested list for a checkout discount-code field

1. An LLM suggests six cases for the discount-code rule from an earlier note in this chapter,
   including "verify an expired code is rejected" and "check that a code past its expiry date
   shows an error."
2. Both map to the same spec sentence and reduce to the same signature - expired code, rejected -
   so one is kept and the other dropped as a duplicate.
3. A third suggestion, "verify the discount field validates the code," has an assertion that only
   checks a message appeared - not which message, or whether checkout still completed. Tightened to
   assert the exact text "Code not valid" and that checkout remains usable, it would now actually
   fail if that specific behavior broke.
4. A fourth suggestion, about codes containing emoji, matches nothing in the spec. It gets raised
   as a question for the spec owner rather than silently added as an assumed requirement.

**Quiz.** An AI tool suggests a test case: 'Verify an error message appears when the discount code is invalid.' The current implementation shows a generic 'Something went wrong' message instead of the spec's required 'Code not valid.' What happens if this suggestion is added to the suite exactly as worded?

- [ ] The test correctly fails, catching the wrong-message bug
- [x] The test passes, because it only checks that some error message appeared - not which one - so the actual spec violation goes uncaught
- [ ] The test cannot run at all
- [ ] The test fails regardless of what message appears, since AI-suggested tests are always stricter than needed

*This is exactly the failure mode the third review question is built to catch: an assertion that checks 'something happened' rather than the specific, spec-required outcome will pass even when the real requirement is violated. The fix is tightening the suggestion to assert the exact expected text before adding it to the suite - not assuming a plausible-sounding case is automatically a rigorous one.*

- **The three-question review pass** — Does it map to a real requirement? Does it duplicate existing coverage? Would its assertion actually fail against the exact bug it claims to catch?
- **Why fluent output isn't proof of correctness** — A model that writes clearly is demonstrating fluency, not accuracy - the only way to know a suggestion is right is to check it against the spec, the suite, or the running app.
- **How to spot a duplicate suggestion** — Reduce it to subject, condition, and expected outcome - two cases with the same signature in different wording are one test, not two.
- **The AI-as-copilot throughline** — Across every technique in this chapter, the model accelerates a tester's own work - brainstorming, prompting, generating data - but selecting, verifying, and deciding what actually matters stays the tester's job, every time.

### Challenge

Take a list of AI-suggested test cases for a feature you know well (your own from earlier in this chapter, or a fresh one). Run all three review questions on each: requirement match, duplicate check, and assertion strength. Report how many survived all three unchanged.

### Ask the community

> An AI tool suggested `[test case]` for `[feature]`, and I can't tell if its assertion would actually catch `[the specific bug it claims to guard against]`. How would you strengthen or verify it before adding it to a real suite?

The most useful answers point at a concrete way to tighten the assertion or verify it against a known-bad state, not just general advice to "test more thoroughly."

- [Katalon — How to review and validate AI-generated test cases](https://katalon.com/resources-center/blog/reviewing-ai-generated-test-cases)
- [Applause — Human Testing vs. AI Testing: what each can (and can't) catch](https://www.applause.com/blog/human-testing-vs-ai-testing-what-each-can-and-cant-catch/)
- [Automation Testing with Joe Colantonio — The AI Illusion: Why Testing Still Needs Humans](https://www.youtube.com/watch?v=D6BiFEu7D8s)

🎬 [The AI Illusion: Why Testing Still Needs Humans](https://www.youtube.com/watch?v=D6BiFEu7D8s) (16 min)

- Confident, fluent AI output is not the same thing as correct output - check it against something real before trusting it.
- Every suggestion earns its place by mapping to a real requirement, not duplicating existing coverage, and having an assertion that would actually fail against the bug it names.
- A long, well-written list is not proof of good coverage - three verified, distinct cases beat twenty unverified ones.
- Across this whole chapter, AI accelerates a tester's own brainstorming, prompting, and data generation - it never replaces the judgment that decides what actually matters and whether the output can be trusted.


## Related notes

- [[Notes/ai-and-the-modern-tester/ai-as-your-testing-copilot/llms-for-test-ideas-and-cases|LLMs for test ideas & cases]]
- [[Notes/ai-and-the-modern-tester/ai-as-your-testing-copilot/prompting-for-qa-work|Prompting for QA work]]
- [[Notes/ai-and-the-modern-tester/ai-as-your-testing-copilot/generating-test-data-with-ai|Generating test data with AI]]


---
_Source: `packages/curriculum/content/notes/ai-and-the-modern-tester/ai-as-your-testing-copilot/reviewing-ai-output-critically.mdx`_
