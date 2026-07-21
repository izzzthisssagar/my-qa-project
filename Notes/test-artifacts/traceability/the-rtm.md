---
title: "The RTM"
tags: ["test-artifacts", "traceability", "track-a"]
updated: "2026-07-14"
---

# The RTM

*A requirements traceability matrix is the one document whose entire job is answering a single question fast: for any requirement, exactly which test cases prove it works - and which requirements have no test case at all.*

> Picture a stakeholder in a release-readiness meeting asking: "Are we sure the password-reset requirement
> is actually tested?" Without a traceability matrix, the honest answer is "let me go check the test
> suite and get back to you." With one, the answer is a five-second lookup: find the requirement's row,
> read across, see the linked test case IDs and their pass/fail status. That's the entire reason this
> document exists - not process for its own sake, but a real answer to a real question, on demand.

> **In real life**
>
> A broadcast video patch bay wires an entire studio together - dozens of labeled rows, each one a named
> signal (camera outputs, color-corrector inputs, switcher outputs), each with its own numbered jacks, all
> cross-connected by physical cables a technician can trace by hand from any single jack back to its
> source. A laptop running port-configuration software sits right beside it, showing the same
> cross-connections as a literal on-screen grid. Neither the physical patch bay nor the software grid
> exists to look impressive - they exist so that when something's wrong with the "COLOR CORRECTOR
> OUTPUTS" signal, someone can trace that exact row to its exact source in seconds instead of guessing. A
> traceability matrix is the QA equivalent: one row per requirement, cross-connected to the test cases
> that verify it, so any single thread can be traced in seconds.

**Requirements Traceability Matrix (RTM)**: A Requirements Traceability Matrix (RTM) is a table that maps each requirement to the test case(s) that verify it - typically requirement ID, requirement description, linked test case ID(s), and execution status (pass/fail/not-run) per requirement. Its core purpose is proving test coverage: every requirement has at least one linked case, and every case traces back to a real requirement. A requirement with zero linked cases is a coverage gap - a real, spec'd behavior nobody has actually verified. An RTM is not a test plan (which covers process and scope) and not a test case (which covers HOW to test) - it's the cross-reference connecting the two.

## Why this table exists and what it isn't

An RTM answers exactly one question well: for a given requirement, what test cases verify it, and did
they pass? It is deliberately NOT trying to be a test plan (this chapter's earlier notes cover that
document's job) and it is NOT trying to hold the actual test steps (a test case's job, from the
scenarios-and-cases chapter). Confusing an RTM for either of those, or trying to make it do their job
too, is how RTMs balloon into unmaintained spreadsheets nobody trusts.

## The minimum viable RTM

A working RTM needs exactly four columns to answer its one question: requirement ID, requirement
description (short - full detail lives in the requirements doc), linked test case ID(s), and status per
case. Anything beyond that (owner, priority, module, release) is optional enrichment, not the core job.

## The single fact an RTM makes undeniable

A requirement row with an empty test-case column is not ambiguous or arguable - it's a fact, visible at
a glance, that nobody has verified that specific requirement yet. This is the RTM's real value: it turns
"I think we've tested everything" into a checkable claim instead of a guess.

![A broadcast video patch bay with rows labeled by signal name (CCU inputs, color corrector outputs, switcher outputs) and numbered jacks, a blue patch cable running down the panel, and a laptop displaying port-configuration software with a grid-style matrix layout](the-rtm.jpg)
*Patchpanel2.JPG — Wikimedia Commons, public domain (Pcpeggs)*
- **One labeled row = one requirement** — Each row on the patch bay is a distinct, named signal - exactly like one row of an RTM is one distinct, named requirement. The label is the identity; everything else hangs off it.
- **The numbered jacks in a row = the linked test cases** — A row's individual numbered ports are the specific connections proving that signal actually reaches somewhere real - the same role a requirement's linked test-case IDs play in an RTM.
- **The laptop's grid software = the matrix itself** — The software on screen is a literal cross-reference grid, mapping keypoints to ports. An RTM is this same idea in spreadsheet form - one axis requirements, one axis test cases, the intersection showing the link.
- **One traced cable = one verified requirement-to-case link** — A single cable, followed by hand from jack to jack, is proof of one specific connection - just like one row's status column is proof (pass/fail) of one specific requirement-to-case link.
- **Multiple parallel labeled rows = the full set of requirements being tracked** — The panel doesn't track one signal - it tracks dozens, each independently traceable. An RTM does the same for a whole requirements set, not just the one a stakeholder happens to ask about.

**How an RTM gets built and read - press Play**

1. **List every requirement with a stable ID** — REQ-01, REQ-02... - IDs that won't change even if the requirement's wording does, so links don't silently break.
2. **Write test cases, each tagged with the requirement(s) it verifies** — The link is created at case-authoring time, not bolted on afterward - a case without a requirement tag can't be traced at all.
3. **Build the matrix: one row per requirement, linked case IDs alongside** — Some tools generate this automatically from tags; a spreadsheet works fine for a small project.
4. **Scan for empty case columns - these are your coverage gaps** — A requirement row with nothing linked to it is the single most useful thing this document ever tells you.
5. **Update statuses as cases run - pass, fail, not yet run** — The RTM becomes a live coverage dashboard, not just a one-time planning artifact.

*Run it - building an RTM and finding coverage gaps (Python)*

```python
requirements = {
    "REQ-01": "User can log in with valid credentials",
    "REQ-02": "User sees an error on invalid credentials",
    "REQ-03": "User can reset a forgotten password",
    "REQ-04": "Session expires after 30 minutes idle",
}

test_cases = {
    "TC-101": {"requirement": "REQ-01", "status": "pass"},
    "TC-102": {"requirement": "REQ-01", "status": "pass"},
    "TC-103": {"requirement": "REQ-02", "status": "fail"},
    "TC-104": {"requirement": "REQ-03", "status": "pass"},
}

def build_rtm(requirements, test_cases):
    rtm = {req_id: [] for req_id in requirements}
    for tc_id, tc in test_cases.items():
        rtm[tc["requirement"]].append((tc_id, tc["status"]))
    return rtm

rtm = build_rtm(requirements, test_cases)

print(f"{'Requirement':10} {'Cases':22} Coverage")
covered = 0
for req_id, desc in requirements.items():
    cases = rtm[req_id]
    case_summary = ", ".join(f"{tc}({status})" for tc, status in cases) if cases else "NONE"
    coverage = "covered" if cases else "GAP"
    if cases:
        covered += 1
    print(f"{req_id:10} {case_summary:22} {coverage}")

print(f"\\n{covered}/{len(requirements)} requirements have at least one linked test case.")
gaps = [req_id for req_id, cases in rtm.items() if not cases]
print(f"Coverage gaps: {gaps}")

# Requirement Cases                  Coverage
# REQ-01     TC-101(pass), TC-102(pass) covered
# REQ-02     TC-103(fail)           covered
# REQ-03     TC-104(pass)           covered
# REQ-04     NONE                   GAP
#
# 3/4 requirements have at least one linked test case.
# Coverage gaps: ['REQ-04']
```

Same matrix-building logic in Java, the shape a real test-management tool's traceability report might take:

*Run it - the RTM builder (Java)*

```java
import java.util.*;

public class Main {

    static class TestCase {
        String requirement;
        String status;
        TestCase(String requirement, String status) {
            this.requirement = requirement;
            this.status = status;
        }
    }

    public static void main(String[] args) {
        LinkedHashMap<String, String> requirements = new LinkedHashMap<>();
        requirements.put("REQ-01", "User can log in with valid credentials");
        requirements.put("REQ-02", "User sees an error on invalid credentials");
        requirements.put("REQ-03", "User can reset a forgotten password");
        requirements.put("REQ-04", "Session expires after 30 minutes idle");

        LinkedHashMap<String, TestCase> testCases = new LinkedHashMap<>();
        testCases.put("TC-101", new TestCase("REQ-01", "pass"));
        testCases.put("TC-102", new TestCase("REQ-01", "pass"));
        testCases.put("TC-103", new TestCase("REQ-02", "fail"));
        testCases.put("TC-104", new TestCase("REQ-03", "pass"));

        LinkedHashMap<String, List<String>> rtm = new LinkedHashMap<>();
        for (String reqId : requirements.keySet()) {
            rtm.put(reqId, new ArrayList<>());
        }
        for (Map.Entry<String, TestCase> entry : testCases.entrySet()) {
            String tcId = entry.getKey();
            TestCase tc = entry.getValue();
            rtm.get(tc.requirement).add(tcId + "(" + tc.status + ")");
        }

        System.out.printf("%-11s %-23s %s%n", "Requirement", "Cases", "Coverage");
        int covered = 0;
        List<String> gaps = new ArrayList<>();
        for (String reqId : requirements.keySet()) {
            List<String> cases = rtm.get(reqId);
            String caseSummary = cases.isEmpty() ? "NONE" : String.join(", ", cases);
            String coverage = cases.isEmpty() ? "GAP" : "covered";
            if (!cases.isEmpty()) covered++;
            else gaps.add(reqId);
            System.out.printf("%-11s %-23s %s%n", reqId, caseSummary, coverage);
        }

        System.out.println();
        System.out.println(covered + "/" + requirements.size() + " requirements have at least one linked test case.");
        System.out.println("Coverage gaps: " + gaps);
    }
}

/* Requirement Cases                   Coverage
   REQ-01      TC-101(pass), TC-102(pass) covered
   REQ-02      TC-103(fail)            covered
   REQ-03      TC-104(pass)            covered
   REQ-04      NONE                    GAP

   3/4 requirements have at least one linked test case.
   Coverage gaps: [REQ-04] */
```

> **Tip**
>
> Notice REQ-02 shows "covered" even though its one linked test case has status "fail." Coverage and
> passing are two different facts - a failed test case still counts as proof the requirement was actually
> tested. Don't let a red status column trick you into treating a requirement as a coverage gap; only an
> EMPTY case column is a real gap.

### Your first time: Your mission: build a real RTM from a small requirements set

- [ ] Pick 5-6 real requirements for a small feature — BuggyShop's checkout flow works well - has enough distinct behaviors to be a real exercise.
- [ ] Give each requirement a stable ID — REQ-01 style - something that won't change even if the wording gets revised later.
- [ ] Write or list the test cases that verify each one, tagging each with its requirement ID — If a case doesn't obviously map to one of your requirements, that's worth noticing on its own.
- [ ] Build the matrix: requirement rows, linked case IDs, status column — A spreadsheet is completely fine for this - the format matters far less than the discipline of filling it in honestly.
- [ ] Circle any requirement row with an empty case column — This is the actual output of the exercise - a real, current list of what's genuinely untested.

You built a document that turns "I think we've tested everything" into a checkable claim - and probably found at least one requirement nobody had actually written a case for.

- **My RTM has a requirement with two test cases, one passing and one failing - what status do I mark the row?**
  Track status per test case, not one blended status per requirement - REQ-02 in this note's playground example shows exactly this pattern (covered, with a failing case). Collapsing multiple case statuses into one number per requirement hides the actual detail an RTM exists to preserve.
- **A requirement changed wording during development and now I'm not sure if the old test cases still apply.**
  This is exactly why requirement IDs should be stable and separate from requirement wording - the ID (REQ-04) doesn't change even when the description does, so the RTM link survives the edit. If the requirement's actual BEHAVIOR changed (not just wording), review the linked cases specifically for that row.
- **My RTM is huge and nobody on the team actually looks at it before release.**
  An unused RTM is usually one that tries to do too much (extra columns, extra process) rather than answering its one core question fast. Strip it back to the four essential columns from this note and re-check whether it becomes useful again.
- **I have test cases that don't map cleanly to any single requirement - like a general exploratory session.**
  Not every test activity needs to appear in the RTM - it exists specifically to trace REQUIREMENTS to CASES. Exploratory testing and other requirement-agnostic activities are valuable but belong in a different record, not forced into a matrix they don't fit.

### Where to check

Where an RTM earns its keep:

- **Release-readiness reviews** — "is X actually tested" needs a five-second lookup, not a live investigation.
- **Regulated or audited projects** — traceability from requirement to verification is often a literal compliance requirement, not just good practice.
- **Requirement changes mid-project** — the RTM shows exactly which existing cases need re-review when a requirement's behavior changes.
- **Post-release defect triage** — a bug tied to a requirement with no linked case is a coverage gap that just became visible the hard way.
- **NOT for tracking exploratory or requirement-agnostic testing** — that activity is real and valuable, but it isn't what this document is for.

The habit: **before calling a release ready, scan the RTM for empty case columns - that scan is the actual value of the whole document.**

### Worked example: finding a real gap before it becomes a real incident

1. **The project**: a checkout flow redesign with six written requirements, including REQ-04: "Session expires after 30 minutes of inactivity, prompting re-login before payment submission."
2. **The team builds an RTM** mapping all six requirements to their test cases, as part of pre-release review.
3. **REQ-01 through REQ-03 and REQ-05, REQ-06 each show two to three linked, passing test cases.** Confidence is high.
4. **REQ-04's row comes up empty.** No test case anywhere in the suite is tagged against it.
5. **Someone assumes it must be covered indirectly** - "surely the general session tests catch this" - and almost moves on.
6. **The RTM's whole point is refusing to accept that assumption**: an empty case column means untested, full stop, regardless of what anyone assumes might be covered incidentally.
7. **A tester writes a dedicated case**: log in, sit idle 31 minutes, attempt to submit payment, confirm re-login is required. It fails - the session timeout was never actually wired up for the payment step specifically, only for general page navigation.
8. **The gap the RTM surfaced was a real, shippable bug** - caught during review because the matrix made "REQ-04: untested" a visible fact instead of a buried assumption.

> **Common mistake**
>
> Assuming a requirement is "probably covered" by some other test that doesn't specifically link to it. The
> worked example above is the exact failure mode: REQ-04 looked like it might be covered by general
> session tests, and that assumption was wrong in a way that mattered. An RTM's entire value comes from
> refusing assumptions - an empty case column means untested, and the only fix is writing the missing case,
> never reasoning your way around the gap.

**Quiz.** A requirement's RTM row shows one linked test case with status 'fail.' A teammate says this requirement is a coverage gap and needs a new test case written. Are they right?

- [x] No - the requirement IS covered (it has a linked test case); the fail status means the requirement's actual behavior is broken and needs a bug fix, not a new test case
- [ ] Yes - any requirement without a fully passing test suite should be treated as an uncovered gap until every linked case passes
- [ ] No - RTM status only matters at the very end of a release cycle, so a failing case earlier in testing can be safely ignored for now
- [ ] Yes - a failing test case should be deleted and rewritten from scratch, since its current form clearly doesn't reflect the real requirement

*This note explicitly distinguishes two different facts an RTM row can show: whether a requirement has ANY linked test case (coverage) versus whether that case currently passes (correctness). A linked case with a fail status proves the requirement WAS tested - and found broken - which is a completely different, and arguably more urgent, situation than an empty case column. The fix for a failing case is fixing the underlying bug (or confirming the test itself is wrong), not writing a redundant new case. Ignoring a failing case until 'the end of the release cycle' has nothing to do with what the RTM is telling you, and deleting a failing case just because it fails would erase real, valid evidence of a bug rather than addressing it.*

- **What an RTM's four essential columns are** — Requirement ID, requirement description, linked test case ID(s), status per case - everything beyond this is optional enrichment.
- **The one fact an RTM makes undeniable** — A requirement row with an empty test-case column - a real, spec'd behavior nobody has actually verified yet.
- **Coverage vs. passing - the key distinction** — A linked-but-failing test case still counts as coverage; only an EMPTY case column is a real coverage gap.
- **What an RTM is NOT** — Not a test plan (process/scope) and not a test case (test steps) - it's the cross-reference connecting requirements to the cases that verify them.
- **Why requirement IDs need to be stable** — So RTM links survive requirement wording changes - the ID persists even when the description text is edited.
- **The habit an RTM exists to support** — Scanning for empty case columns before calling a release ready - refusing to accept 'probably covered' assumptions.

### Challenge

Build a real RTM (requirement ID, description, linked case IDs, status) for 5-6 requirements from a
feature you have access to. Deliberately write it honestly rather than retrofitting it to look complete
- if a requirement genuinely has no test case yet, leave that row empty. Then answer: which requirement
row surprised you, and would you have caught that gap without building the matrix?

### Ask the community

> RTM review for `[feature]`: `[N]` requirements, `[N]` covered, `[N]` gaps found. Is a spreadsheet still the right tool at this scale, or is it time for RTM-generation features in a real test-management tool?

Useful replies name a SPECIFIC tool or workflow and explain what problem it solves at scale (auto-linking
via tags, live status updates) rather than a general "spreadsheets don't scale" comment.

- [Guru99 — What is Requirements Traceability Matrix (RTM) in Testing?](https://www.guru99.com/traceability-matrix.html)
- [Software Testing Help — Requirements Traceability Matrix with Example Template](https://www.softwaretestinghelp.com/requirements-traceability-matrix/)
- [TestRail — Requirements Traceability Matrix: A How-To Guide](https://www.testrail.com/blog/requirements-traceability-matrix/)
- [S3CloudHub — Requirements Traceability Matrix | RTM Tutorial](https://www.youtube.com/watch?v=GTHk3acE1Sk)

🎬 [Requirements Traceability Matrix — RTM Tutorial](https://www.youtube.com/watch?v=GTHk3acE1Sk) (7 min)

- An RTM maps each requirement to the test case(s) that verify it - its whole job is answering coverage questions in seconds, not minutes of investigation.
- The minimum viable RTM needs four columns: requirement ID, description, linked case ID(s), status - extra columns are optional, not core.
- An empty case column is a real coverage gap; a linked-but-failing case is NOT a gap - it's proof the requirement was tested and found broken.
- Requirement IDs should stay stable even when wording changes, so RTM links don't silently break on an edit.
- The core habit: scan for empty case columns before calling a release ready - that scan is the entire point of maintaining the document.


---
_Source: `packages/curriculum/content/notes/test-artifacts/traceability/the-rtm.mdx`_
