---
title: "The write-up, like a real report"
tags: ["api-and-modern-security", "auditing-buggyapi", "track-c"]
updated: "2026-07-21"
---

# The write-up, like a real report

*Two hands poised over a typewriter, mid-thought, capture the exact moment a finding stops being something only the finder understands and starts becoming something a stranger can act on. A security finding nobody else can reproduce from the write-up alone might as well not have been found.*

> "Found an IDOR on the bookings endpoint, pretty bad" tells a developer almost nothing they can act on -
> which endpoint, which parameter, what request actually triggers it, what the impact concretely looks
> like. A finding this vague forces the reader to rediscover the entire bug themselves before they can
> even start fixing it, which defeats most of the value of having found it in the first place.

> **In real life**
>
> Two hands poised over an old typewriter, mid-thought, capture the exact moment a finding stops living
> only in one person's head and starts becoming something a stranger could pick up and act on without
> ever having been in the room. Whatever was actually discovered - the exact request, the exact response,
> the exact consequence - has to survive the translation from "I found something" into words precise
> enough that someone who wasn't there can reproduce it, understand why it matters, and fix it. A real
> report is that translation done properly, not an afterthought tacked onto the actual finding.

**Writing the report**: Writing a finding up like a real report means documenting a security discovery with enough specific, reproducible detail - exact request, exact response, concrete impact, and a clear fix direction - that someone who wasn't present for the discovery can independently verify it and act on it, rather than a vague summary that only makes sense to the person who found it.

## Reproduction steps are the report's actual load-bearing wall

Everything else in a good write-up - severity, impact narrative, suggested fix - depends on the reader
being able to reproduce the finding themselves. A report missing an exact, step-by-step reproduction
(the specific request, headers, and body used; the specific response received) forces every reader to
either trust the claim on faith or spend real time rediscovering the bug from scratch before they can
even evaluate it, let alone fix it. For BuggyAPI specifically, that means the literal request made -
method, path, headers, body - and the literal response received, not a paraphrased description of
either.

## Impact has to be stated in concrete consequence, not just a technical label

"IDOR vulnerability" is a correct technical classification that tells a non-security reader almost
nothing about why it matters. "Any authenticated user can read any other user's full booking history,
including passenger names and travel dates, by changing a single number in the URL" states the same
finding in terms that make the actual real-world consequence immediately clear to a developer, a
manager, or anyone else reading the report without deep security background. A strong write-up states
both: the technical classification, for a security-literate reader, and the concrete consequence, for
everyone else who needs to understand why it's worth fixing now.

> **Tip**
>
> Write the report as if the reader will never get to ask a single clarifying question. Every detail
> needed to reproduce, understand, and prioritize the fix has to be in the document itself - a report
> that depends on a follow-up conversation to actually be usable hasn't fully done its job yet.

> **Common mistake**
>
> Leading a write-up with the fix suggestion before establishing the reproduction and impact clearly.
> A reader needs to understand exactly what's wrong and why it matters before a suggested fix makes real
> sense - reversing that order makes the fix feel arbitrary rather than clearly justified by what
> actually came before it.

![A close-up of two hands poised over the keys of an old black typewriter](the-write-up-like-a-real-report.jpg)
*Hands on an old typewriter closeup — Shixart1985, CC BY 2.0, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Hands_on_an_old_typewriter_closeup.jpg)*
- **The fingers poised directly over the keys** — The precise moment of translating what's known into words someone else can read - the exact work a good write-up does with a raw finding before it's shared.
- **The wristwatch, visible on one hand** — A reminder that a write-up happens under real time constraints too - but rushing it undermines the exact reproducibility the whole report depends on.
- **The worn, well-used typewriter keys** — A tool built for exactly this purpose, used repeatedly - the same way a good write-up follows a consistent, repeatable structure every time, not reinvented from scratch per finding.
- **The dark, focused space immediately around the machine** — Deliberate concentration on getting this one document right - the same focused effort a report needs, since a vague version forces every future reader to redo the work of understanding it.

**Writing a finding up like a real report**

1. **State the exact reproduction steps first** — The literal request and literal response - specific enough that a stranger can reproduce it without any follow-up questions.
2. **State the concrete, real-world impact** — Not just a technical classification - what this actually lets an attacker do, in plain terms anyone can understand.
3. **Note severity with explicit reasoning, not just a label** — Why this rating specifically - what scope of data or users, what ease of exploitation.
4. **Suggest a fix direction last, once the problem is fully established** — A concrete starting point for the developer, offered after reproduction and impact make the fix's necessity clear.

*Checking a report draft for the required sections before submitting (Python)*

```python
report = {
    "title": "IDOR on GET /bookings/{id} exposes any user's booking data",
    "reproduction_steps": "1. Authenticate as user A. 2. GET /bookings/1002 (belongs to user B). 3. Response returns user B's full booking data with no ownership check.",
    "impact": "Any authenticated user can read any other user's booking history, including passenger names and travel dates, by changing one number in the URL.",
    "severity_reasoning": "",
    "suggested_fix": "Add a server-side check that the authenticated user owns the requested booking ID before returning data.",
}

REQUIRED_SECTIONS = ["title", "reproduction_steps", "impact", "severity_reasoning", "suggested_fix"]

missing = [s for s in REQUIRED_SECTIONS if not report.get(s)]
if missing:
    print("NOT READY TO SUBMIT - missing: " + ", ".join(missing))
else:
    print("All required sections present - ready to submit")
```

*Checking a report draft for the required sections before submitting (Java)*

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, String> report = new LinkedHashMap<>();
        report.put("title", "IDOR on GET /bookings/{id} exposes any user's booking data");
        report.put("reproduction_steps",
                "1. Authenticate as user A. 2. GET /bookings/1002 (belongs to user B). " +
                "3. Response returns user B's full booking data with no ownership check.");
        report.put("impact",
                "Any authenticated user can read any other user's booking history, including " +
                "passenger names and travel dates, by changing one number in the URL.");
        report.put("severity_reasoning", "");
        report.put("suggested_fix",
                "Add a server-side check that the authenticated user owns the requested booking ID before returning data.");

        List<String> requiredSections = Arrays.asList(
                "title", "reproduction_steps", "impact", "severity_reasoning", "suggested_fix");

        List<String> missing = new ArrayList<>();
        for (String s : requiredSections) {
            if (report.get(s) == null || report.get(s).isEmpty()) missing.add(s);
        }

        if (!missing.isEmpty()) {
            System.out.println("NOT READY TO SUBMIT - missing: " + String.join(", ", missing));
        } else {
            System.out.println("All required sections present - ready to submit");
        }
    }
}
```

### Your first time: Write one real finding up as a full report

- [ ] Pick one real finding from a BuggyAPI testing session — Any confirmed issue, even a minor one - the structure matters more than the severity for this exercise.
- [ ] Write the exact reproduction steps: literal request and literal response — Specific enough that someone who wasn't there could follow them exactly.
- [ ] Write the impact in plain, concrete consequence, not just a technical label — What can an attacker actually do, stated so a non-security reader understands why it matters.
- [ ] Add severity reasoning and a suggested fix, in that order, after the above — Confirm a stranger reading only this document would have everything needed to act on it.

- **A developer responds to a filed finding asking for clarification on how to reproduce it.**
  The reproduction steps weren't specific enough - rewrite with the literal request and response, not a paraphrased summary, so no follow-up question should be needed.
- **A finding gets deprioritized despite being genuinely serious.**
  Check whether the impact was stated only as a technical classification - rewrite it in concrete, real-world consequence terms a non-security reader can immediately grasp the seriousness of.
- **A report reads well but a developer implements a fix that doesn't actually address the root cause.**
  The suggested fix may have been offered without the reproduction and impact being fully clear first - reorder the report so the problem is unambiguous before the fix direction is suggested.

### Where to check

- Any finding about to be filed, checked against whether a stranger could reproduce it from the write-up alone with no follow-up questions.
- The impact section specifically, checked for concrete real-world consequence, not just a technical vulnerability classification.
- [[api-and-modern-security/auditing-buggyapi/chaining-findings]] for how a confirmed chain gets documented clearly as its own combined finding, not just two separate reports.
- [[api-and-modern-security/auditing-buggyapi/threat-modeling-an-api]] for the earlier context that helps frame why a given finding's impact matters relative to what that endpoint actually controls.
- [[test-management-and-reporting/docs-and-communication/writing-for-developers]] for the underlying precision-writing discipline a strong security report draws on directly.

### Worked example: a vague finding rewritten into a report a developer could act on immediately

1. A tester's first draft of a finding reads: "IDOR issue on bookings endpoint, can see other people's
   data, should probably fix soon."
2. A developer picking this up would need to ask which endpoint, which parameter, what a real request
   looks like, and what data specifically is exposed - none of it is in the report as written.
3. The write-up is rewritten with the exact reproduction: the literal endpoint
   (`GET /bookings/{id}`), the literal steps (authenticate as one user, request another user's booking
   ID), and the literal response confirming the exposed fields.
4. The impact is rewritten from "can see other people's data" to the concrete version: "any
   authenticated user can read any other user's full booking history, including passenger names and
   travel dates, by changing one number in the URL."
5. The developer picking up the rewritten version fixes it the same day, with zero follow-up questions
   needed - every piece of information required to reproduce, understand, and act on the finding was
   already in the document.

**Quiz.** According to this note, what is the actual load-bearing element of a good security write-up?

- [ ] The severity label assigned to the finding
- [x] The reproduction steps - since everything else in the report, including the impact narrative and suggested fix, depends on the reader being able to independently reproduce and verify the finding themselves
- [ ] How quickly the report is written after the finding is discovered
- [ ] Whether the report uses the correct official vulnerability classification terminology

*A report's severity rating, impact narrative, and suggested fix all depend on the reader first being able to reproduce the finding themselves. Without exact, specific reproduction steps - the literal request and response - a reader has to either trust the claim on faith or spend real time rediscovering the bug from scratch, which undermines the report's entire purpose regardless of how well the rest of it is written.*

- **Writing a finding up like a real report** — Documenting a security discovery with enough specific, reproducible detail - exact request, exact response, concrete impact, clear fix direction - that a stranger can act on it independently.
- **Why reproduction steps are the report's load-bearing element** — Everything else - severity, impact, fix - depends on the reader being able to reproduce the finding themselves; vague steps force them to rediscover the bug from scratch first.
- **Why impact needs concrete consequence, not just a technical label** — 'IDOR vulnerability' tells a non-security reader little - stating exactly what an attacker can actually do makes the real seriousness immediately clear to any reader, not just security specialists.
- **Why the suggested fix belongs last in the report** — A fix suggested before the reproduction and impact are fully established feels arbitrary - establishing the problem clearly first is what makes the fix direction make real sense.

### Challenge

Pick one real finding from a BuggyAPI testing session. Write it up as a full report: exact reproduction steps, concrete impact in plain language, severity reasoning, and a suggested fix - in that order.

- [OWASP Cheat Sheet Series — Vulnerability Disclosure Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html)
- [GoGetSecure — How to Write a Bug Bounty Report](https://gogetsecure.com/how-to-write-a-bug-bounty-report/)
- [Hacker101 - Writing Good Reports | HackerOne](https://www.youtube.com/watch?v=z60CFFFyZWE)

🎬 [Hacker101 - Writing Good Reports | HackerOne](https://www.youtube.com/watch?v=z60CFFFyZWE) (6 min)

- A finding nobody else can reproduce from the write-up alone might as well not have been found - reproduction steps are the report's load-bearing element.
- State exact requests and responses, not paraphrased summaries - specific enough that a stranger needs no follow-up questions.
- State impact in concrete, real-world consequence, not just a technical classification - so any reader immediately understands why it matters.
- Order matters: reproduction and impact established clearly first, suggested fix offered last, once the problem is unambiguous.
- Write as if the reader will never get to ask a clarifying question - everything needed has to already be in the document.


## Related notes

- [[Notes/api-and-modern-security/auditing-buggyapi/chaining-findings|Chaining findings]]
- [[Notes/api-and-modern-security/auditing-buggyapi/threat-modeling-an-api|Threat-modeling an API]]
- [[Notes/test-management-and-reporting/docs-and-communication/writing-for-developers|Writing for developers]]


---
_Source: `packages/curriculum/content/notes/api-and-modern-security/auditing-buggyapi/the-write-up-like-a-real-report.mdx`_
