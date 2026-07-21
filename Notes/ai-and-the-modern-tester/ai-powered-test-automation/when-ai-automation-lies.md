---
title: "When AI automation lies"
tags: ["ai-and-the-modern-tester", "ai-powered-test-automation", "track-c"]
updated: "2026-07-21"
---

# When AI automation lies

*An LLM asked why a test failed never says 'I don't know' - it names a function or race condition in the exact same confident tone whether real or invented. Open-source coding models hallucinate a nonexistent package in roughly 1 of every 5 generations.*

> Ask an AI assistant why a flaky test failed and it will answer - always. Not "I'm not certain," not
> "there isn't enough information in this stack trace to say." It names a function, a race condition, a
> config value, stated with exactly the same fluent confidence whether that explanation is real or
> entirely invented. A large 2024 academic study analyzing 576,000 code samples found open-source
> coding models hallucinate a nonexistent software package in roughly 1 of every 5 generations - and
> every one of those fabricated packages was named with total, unhedged confidence.

> **In real life**
>
> A polygraph produces a precise, scientific-looking readout - needles tracing exact lines on a moving
> chart, numbers, a specific pattern an examiner points to and interprets. It looks exactly as
> authoritative whether the reading actually correlates with truth or not, which is precisely why
> polygraph results are inadmissible as definitive proof in most courts: the confident, precise-looking
> output was never the same thing as a verified fact. An AI tool's explanation for a test failure works
> the same way - fluent, specific, confidently delivered - and just as disconnected from ground truth
> unless someone actually checks the claim against the real system, the same way a polygraph reading
> was never supposed to be trusted without independent verification.

**AI hallucination**: AI hallucination in a QA context is a confident, plausible-sounding output from an AI tool - a root-cause explanation, a generated test assertion, a cited function or package - that is not actually grounded in the real system it claims to describe, delivered with no linguistic hedge distinguishing it from a verified fact.

## Why the confidence is not a signal

An LLM is trained to predict the statistically most plausible next word, not to verify whether a
claim is true - it has no built-in mechanism to check its own output against the real codebase, the
real test environment, or the real documentation before producing an answer. That is the entire
mechanism behind package hallucination: a comprehensive 2024 study running 576,000 code-generation
samples across sixteen models found an average hallucination rate of 5.2% for commercial models and
21.7% for open-source models - some individual models exceeding 60% - every single hallucinated
package name presented as a normal, usable dependency with zero indication it does not exist. The
practical consequence for testing specifically: an AI's confidence level and its correctness are two
independent variables. Fluency is not evidence.

## Where this shows up in day-to-day QA work

A root-cause explanation for a failing test can name a specific class, method, or race condition that
sounds exactly like real domain knowledge and does not correspond to anything in the actual codebase.
A generated test's assertion can cite an expected value the model never actually computed from running
the code, only inferred from what looked plausible given the function's name. An AI-powered visual-diff
tool can report "no significant change" on a real regression sitting just outside whatever similarity
threshold it was tuned against, with the same clean, confident report it gives a genuinely unchanged
page. A chat assistant embedded in a test tool can cite a config option or API parameter that was
never real, formatted exactly like documented fact. None of these announce themselves as guesses.

> **Tip**
>
> Treat every AI-generated explanation as a hypothesis to verify, not a finding to file. Check the
> specific, checkable claim inside it - does that function actually exist, does that config option
> actually appear in the real settings file, does that package actually exist in the real registry -
> before it goes anywhere near a ticket, a report, or a commit.

> **Common mistake**
>
> Judging an AI tool's trustworthiness by how detailed or technical its explanation sounds. Package
> hallucinations in the cited study were not vague or hedged - they were specific, plausible-sounding
> names presented with total confidence, which is exactly what made them dangerous enough to enable
> real supply-chain attacks (an attacker registering the hallucinated package name and shipping malware
> under it).

![A vintage FBI polygraph examination photo, showing a seated subject wired to sensors and a polygraph machine with a pen tracing a reading on a paper chart](when-ai-automation-lies.jpg)
*Administration of Polygraph — FBI, public domain, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Administration_of_Polygraph.jpg)*
- **The readout - confident, precise-looking output** — Every needle trace looks exactly as authoritative whether or not the reading actually means what it's interpreted to mean. An AI tool's confident, specific explanation carries that identical look of precision regardless of whether it's actually correct.
- **The pen, mid-stroke** — Genuinely recording a real signal - but what that signal MEANS is an interpretation layered on top, not a direct readout of truth. The same gap sits between an AI's fluent confidence and whether its claim is actually right.
- **The subject - the actual ground truth** — The one thing in this room the machine cannot directly read. Whether an AI's root-cause explanation is correct is exactly this kind of ground truth - verified against the real system, never assumed from how confident the output sounds.
- **The dials and calibration** — A polygraph reading is only as trustworthy as its calibration and the examiner's skill - courts have never accepted it as standalone proof. An AI QA tool's output deserves the exact same standing skepticism.

**Verifying an AI explanation instead of trusting it**

1. **AI produces a confident, specific explanation** — A named function, a named race condition, a named config value - stated as fact, with no hedge.
2. **Extract the checkable claim inside it** — Does this specific function/package/parameter actually exist? Does the codebase actually behave this way?
3. **Check it directly against the real system** — Grep the codebase, run the code, check the real registry - not another AI query asking if the first answer was right.
4. **Only a verified claim becomes a finding** — An unverified one stays a hypothesis - useful as a starting point for investigation, not something to file or ship as-is.

*Verifying an AI's claimed root cause against real code (Python)*

```python
# The real codebase - what actually exists.
real_codebase = {
    "UserService": ["createUser", "deleteUser", "findByEmail"],
    "AuthService": ["login", "logout", "refreshToken"],
}

# An AI assistant's confident explanation for a test failure.
ai_explanation = {
    "claim": "The failure is caused by a missing null check in UserService.validateEmail()",
    "cited_class": "UserService",
    "cited_method": "validateEmail",
}

def verify_claim(explanation, codebase):
    cls = explanation["cited_class"]
    method = explanation["cited_method"]
    if cls not in codebase:
        return False, "Class '" + cls + "' does not exist in the codebase at all"
    if method not in codebase[cls]:
        return False, ("Class '" + cls + "' exists, but has no method '" + method +
                        "' - the AI's cited method does not exist")
    return True, "Both the class and method exist - claim is checkable, investigate further"

print("AI's claim: " + ai_explanation["claim"])
verified, reason = verify_claim(ai_explanation, real_codebase)
print("")
if verified:
    print("PLAUSIBLE: " + reason)
else:
    print("HALLUCINATED: " + reason)
    print("Do not file this root cause - the AI invented a method that isn't in the code.")
```

*Verifying an AI's claimed root cause against real code (Java)*

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, List<String>> realCodebase = new HashMap<>();
        realCodebase.put("UserService", Arrays.asList("createUser", "deleteUser", "findByEmail"));
        realCodebase.put("AuthService", Arrays.asList("login", "logout", "refreshToken"));

        String aiClaim = "The failure is caused by a missing null check in UserService.validateEmail()";
        String citedClass = "UserService";
        String citedMethod = "validateEmail";

        System.out.println("AI's claim: " + aiClaim);
        System.out.println();

        if (!realCodebase.containsKey(citedClass)) {
            System.out.println("HALLUCINATED: Class '" + citedClass + "' does not exist in the codebase at all");
            System.out.println("Do not file this root cause - the AI invented a class that isn't in the code.");
        } else if (!realCodebase.get(citedClass).contains(citedMethod)) {
            System.out.println("HALLUCINATED: Class '" + citedClass + "' exists, but has no method '" +
                    citedMethod + "' - the AI's cited method does not exist");
            System.out.println("Do not file this root cause - the AI invented a method that isn't in the code.");
        } else {
            System.out.println("PLAUSIBLE: Both the class and method exist - claim is checkable, investigate further");
        }
    }
}
```

### Your first time: Catch a hallucination in a real AI QA output

- [ ] Ask an AI assistant to explain a real test failure or generate test code for a real function — Use a genuine failure or function from a project you actually have access to.
- [ ] Pull out every specific, checkable claim in its answer — A named function, a named package, a named config value, a specific expected number.
- [ ] Check each one directly against the real source - grep, run the code, check the real package registry — Not another AI query - an independent, verifiable check.
- [ ] Note how confident the answer sounded regardless of whether it turned out true — This is the core lesson: the tone gives you no signal either way.

- **An AI-suggested dependency fails to install because the package does not exist.**
  A textbook package hallucination - check the real package registry (PyPI, npm) before ever running an install command an AI suggested, especially for less common library names.
- **A root-cause explanation sounds highly specific and technical but the fix based on it does not resolve the actual failure.**
  The specificity was never evidence of accuracy - verify the cited function, file, or condition actually exists and behaves as claimed before building a fix on top of the explanation.
- **An AI visual-diff or test-generation tool has been wrong before but a team keeps trusting its output at face value.**
  Introduce a standing spot-check habit - a fixed percentage of AI-generated findings get independently verified before use, regardless of how confident or polished any individual output looks.

### Where to check

- Any AI-suggested package or dependency name, checked against the real registry before installation - this is the exact vector real supply-chain attacks have exploited.
- Any AI-generated root-cause explanation, checked for whether the cited function, class, or config value actually exists in the real codebase.
- [[ai-and-the-modern-tester/ai-powered-test-automation/ai-test-generation-tools]] for the specific hallucination risk inside AI-generated test assertions themselves.
- [[ai-and-the-modern-tester/ai-powered-test-automation/autonomous-testing-agents]] for how the same confident-but-unverified pattern shows up in an agent's real-time decisions, not just its written explanations.
- [[ai-and-the-modern-tester/testing-ai-systems/hallucinations-bias-and-safety]] for testing an AI-powered *product* for this exact failure mode, rather than using an AI tool that exhibits it.

### Worked example: a hallucinated root cause that sent a team down the wrong path for a day

1. A flaky end-to-end test fails intermittently in CI. A tester pastes the failure log into an AI
   assistant and asks for a root cause.
2. The AI responds confidently: "This is a race condition in `PaymentGateway.confirmTransaction()` -
   the async callback resolves before the database write commits. Add an `await` before the return
   statement."
3. A developer spends most of a day adding the suggested `await`, re-running the flaky test dozens of
   times to confirm the fix - it does not resolve the flakiness, because `PaymentGateway` has no
   method called `confirmTransaction` anywhere in the actual codebase. The AI invented a plausible-
   sounding method name that fit the failure's general shape.
4. A second look at the actual stack trace, verified line by line against the real code, finds the
   true cause: a hardcoded `sleep(500)` in a completely different test helper, timing out on a slower
   CI runner under load - nothing to do with async/await at all.
5. The AI's explanation was not wrong because it was vague - it was wrong because it was specific and
   plausible while being entirely disconnected from the real code, and nobody checked the cited method
   actually existed before spending a day building a fix around it.

**Quiz.** A 2024 study found open-source coding models hallucinate nonexistent software packages in roughly what share of generations, on average?

- [ ] About 1%
- [ ] About 5%
- [x] About 21.7%
- [ ] About 90%

*5.2% was the average for commercial models in that study; open-source models averaged 21.7%, with some individual models exceeding 60%. Every one of those hallucinated packages was presented with the same confident, unhedged tone as a real one - which is exactly what makes the failure mode dangerous enough to have enabled real supply-chain attacks against developers who installed a fabricated name.*

- **AI hallucination in a QA context** — A confident, plausible-sounding AI output - a root cause, a test assertion, a cited package - not actually grounded in the real system it describes, delivered with no hedge distinguishing it from a verified fact.
- **Why an LLM's confidence is not a correctness signal** — It is trained to predict the most statistically plausible next word, with no built-in mechanism to check its own output against the real codebase or environment before producing an answer.
- **The 2024 package hallucination study's key numbers** — 576,000 code samples across 16 models: 5.2% average hallucination rate for commercial models, 21.7% for open-source models, some individual models over 60% - every hallucinated name presented with full confidence.
- **The one habit that catches most AI hallucinations** — Extract the specific, checkable claim inside any AI explanation or output and verify it directly against the real system - never accept it because it sounds detailed, technical, or confident.

### Challenge

Ask an AI assistant to explain a real test failure or suggest a fix for one, using a project you have access to. Extract every specific claim it makes (function names, config values, package names) and independently verify each one against the real source. Report what you found.

- [We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs](https://arxiv.org/abs/2406.10279)
- [The Register — AI Bots Hallucinate Software Packages and Devs Download Them](https://www.theregister.com/2024/03/28/ai_bots_hallucinate_software_packages/)
- [Why AI Hallucinates: Confident but Wrong!](https://www.youtube.com/shorts/jfsun7pxD9g)

🎬 [Why AI Hallucinates: Confident but Wrong!](https://www.youtube.com/shorts/jfsun7pxD9g) (1 min)

- An LLM always produces an answer - it has no built-in mechanism to check its own output against the real system, so confidence and correctness are independent variables.
- A 2024 study of 576,000 code samples found open-source coding models hallucinate a nonexistent package in an average of 21.7% of generations, every one stated with full confidence.
- Hallucinations show up across QA work: root-cause explanations, generated test assertions, visual-diff verdicts, and cited config or API details - none announce themselves as guesses.
- Treat every AI-generated explanation as a hypothesis: extract the specific, checkable claim and verify it directly against the real codebase or environment before it goes into a report or a fix.
- The confident, specific ones are the most dangerous, not the vague ones - specificity was never evidence of accuracy, and that gap is exactly what has enabled real supply-chain attacks.


## Related notes

- [[Notes/ai-and-the-modern-tester/ai-powered-test-automation/ai-test-generation-tools|AI test generation tools]]
- [[Notes/ai-and-the-modern-tester/ai-powered-test-automation/autonomous-testing-agents|Autonomous testing agents]]
- [[Notes/ai-and-the-modern-tester/testing-ai-systems/hallucinations-bias-and-safety|Hallucinations, bias & safety]]


---
_Source: `packages/curriculum/content/notes/ai-and-the-modern-tester/ai-powered-test-automation/when-ai-automation-lies.mdx`_
