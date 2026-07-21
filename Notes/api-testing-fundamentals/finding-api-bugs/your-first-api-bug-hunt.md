---
title: "Your first API bug hunt (BuggyAPI)"
tags: ["api-testing-fundamentals", "finding-api-bugs", "track-c"]
updated: "2026-07-17"
---

# Your first API bug hunt (BuggyAPI)

*BuggyAPI ('TaskFlight') is this platform's own practice REST API - real auth, real projects and tickets, a real OpenAPI spec, and seeded bugs behind a flag. This is where the last four notes stop being theory.*

> An entomologist doesn't wander a field hoping to bump into something interesting - they work a grid,
> methodically, so they can say afterward exactly which patches of ground they covered and which they
> didn't. A bug hunt against a real API works the same way. Poking at random endpoints until something
> looks wrong finds SOME bugs. Working through auth, then every resource, then every negative case,
> systematically, is what finds the ones random poking misses entirely.

> **In real life**
>
> A specimen drawer full of neatly pinned, individually labeled insects didn't happen by luck - each
> one was caught, identified, and recorded as part of a deliberate collecting method, with the gaps in
> the drawer just as informative as the specimens in it. A systematic API bug hunt produces the same
> kind of record: not a vague sense that "I poked around and it seemed mostly fine," but a specific
> list of what was tested, what wasn't yet, and exactly what was found where.

**Bug hunt**: A bug hunt is a deliberate, systematic session of exercising an API's real surface area - every endpoint, every method that applies to it, the happy path and the negative cases - to find genuine defects, as opposed to casually poking at whatever's convenient. The output isn't just a list of bugs; it's also a coverage record of what was actually checked, so 'nothing found yet' in an unchecked area is honestly reported as untested, not as clean.

## What you're actually working with in BuggyAPI

- **BuggyAPI ("TaskFlight") is a real, spec-first REST API** — auth (`/api/v1/auth/login`,
  `/api/v1/me`), projects (`/api/v1/projects`, `/api/v1/projects/{id}`), and tickets
  (`/api/v1/tickets`, `/api/v1/tickets/{id}`), each with GET/POST/PATCH/DELETE where it makes sense.
- **The OpenAPI spec is generated from the same schema code the server validates against**, served
  at `/api/docs` (Swagger UI) and `/api/v1/openapi.json` — this is your ground truth for what
  "correct" means, from [[api-testing-fundamentals/finding-api-bugs/validating-against-the-spec]].
- **Every response you get is scoped to your own practice sandbox** — the data you create and see is
  yours alone, which matters for one specific category of test: does the API actually enforce that
  boundary, or does it just assume you'll stay inside it.
- **Bugs here are seeded behind a mode flag** — clean mode serves a correct reference API; switching
  to bug-hunt mode is what turns on the deliberate defects this note exists to help you find. Which
  specific defects are seeded is intentionally not something this note tells you — that's the actual
  exercise.

> **Tip**
>
> Before hunting for exotic bugs, run the boring pass first: every endpoint, every applicable method,
> once each, with valid input. A surprising number of real findings turn up in this pass alone —
> because "the happy path definitely works" is an assumption, not a fact, until it's actually been
> exercised end to end.

> **Common mistake**
>
> Testing until you get bored or something breaks, then stopping. Without a record of what you
> actually covered, "I didn't find anything else" is indistinguishable from "I didn't check anything
> else" — and those are very different claims to make in a report.

![An entomology specimen drawer with dozens of pinned insects, each with a small handwritten label recording location, date, and collector](your-first-api-bug-hunt.jpg)
*Insect collection (Diptera), photo by Notafly — Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:InsectCollectionDiptera.jpg)*
- **A dense, methodically organized cluster of specimens** — Rows, not scatter — each pin placed deliberately as part of working the whole drawer systematically. This is what a bug hunt's coverage matrix looks like once you're partway through: organized by area, not by whatever you happened to try first.
- **One specimen with its own handwritten label card** — Location, date, collector — every detail someone else would need to trust and reuse this finding without re-doing the work. A bug report needs the exact same level of specific, individually-attached evidence, not a general note pinned to the whole session.
- **A sparser corner of the drawer** — Less populated doesn't mean nothing's there to find — it may just mean this area hasn't been worked as thoroughly yet. The same is true of whichever endpoint or method combination you haven't gotten to yet in a hunt session.

**Structuring a bug hunt session instead of just poking around**

1. **Get the lay of the land** — Open the OpenAPI docs — list every endpoint and every method that applies to each one before touching anything.
2. **Authenticate and confirm the happy path once** — Log in, call a simple GET, confirm the basic shape matches the spec — your working baseline before anything gets deliberately weird.
3. **Work through each resource systematically** — Every method, on every endpoint, with valid input first — this is the boring pass, and it's the one most likely to be skipped by accident.
4. **Layer in negative and boundary cases per endpoint** — Using the categories from [[api-testing-fundamentals/finding-api-bugs/negative-api-tests]] — not just once overall, but per endpoint, since validation quality can vary between them.
5. **Record coverage and findings as you go, not from memory after** — What was tested, what wasn't yet, and exactly what broke where — the record IS the deliverable, not just the bugs.

The coverage-tracking habit is simple to model — mark off what's actually been exercised, and let
the gaps stay visibly gaps instead of quietly disappearing:

*Run it — tracking real coverage during a hunt session (Python)*

```python
def build_coverage_matrix(endpoints, methods):
    return {endpoint: {method: False for method in methods} for endpoint in endpoints}

def mark_tested(matrix, endpoint, method):
    matrix[endpoint][method] = True

endpoints = ["/v1/projects", "/v1/projects/{id}", "/v1/tickets", "/v1/tickets/{id}"]
methods = ["GET", "POST", "PATCH", "DELETE"]

matrix = build_coverage_matrix(endpoints, methods)

# Only methods that actually exist per the API's own OpenAPI spec get marked
# 'applicable' -- testing a method the spec never declares isn't coverage,
# it's noise.
applicable = {
    "/v1/projects": ["GET", "POST"],
    "/v1/projects/{id}": ["GET", "PATCH", "DELETE"],
    "/v1/tickets": ["GET", "POST"],
    "/v1/tickets/{id}": ["GET", "PATCH", "DELETE"],
}

session_log = [
    ("/v1/projects", "GET"),
    ("/v1/projects", "POST"),
    ("/v1/tickets", "GET"),
    ("/v1/tickets", "POST"),
    ("/v1/tickets/{id}", "GET"),
]

for endpoint, method in session_log:
    mark_tested(matrix, endpoint, method)

print("=== Coverage after one exploration session ===")
for endpoint in endpoints:
    for method in applicable[endpoint]:
        mark = "hit" if matrix[endpoint][method] else "NOT YET TESTED"
        print(f"{method:6} {endpoint:20} {mark}")

applicable_total = sum(len(v) for v in applicable.values())
applicable_done = sum(
    1 for endpoint in endpoints for method in applicable[endpoint] if matrix[endpoint][method]
)
pct = round(applicable_done / applicable_total * 100)
print()
print(f"{applicable_done}/{applicable_total} applicable method+endpoint combos exercised ({pct}%)")
print("A real hunt session isn't 'done' just because nothing has broken yet --")
print("it's done when this matrix is full, or every gap is a deliberate choice.")

# === Coverage after one exploration session ===
# GET    /v1/projects         hit
# POST   /v1/projects         hit
# GET    /v1/projects/{id}    NOT YET TESTED
# PATCH  /v1/projects/{id}    NOT YET TESTED
# DELETE /v1/projects/{id}    NOT YET TESTED
# GET    /v1/tickets          hit
# POST   /v1/tickets          hit
# GET    /v1/tickets/{id}     hit
# PATCH  /v1/tickets/{id}     NOT YET TESTED
# DELETE /v1/tickets/{id}     NOT YET TESTED
#
# 5/10 applicable method+endpoint combos exercised (50%)
# A real hunt session isn't 'done' just because nothing has broken yet --
# it's done when this matrix is full, or every gap is a deliberate choice.
```

Coverage tells you where to look. Once you've actually found a few things, the next skill is
deciding what to write up first — a different, equally real part of a hunt session:

*Run it — triaging a session's findings before writing any of them up (Java)*

```java
import java.util.*;

public class Main {
    record Finding(String description, int severity, int confidence) {}
    // severity 1(low)-4(critical); confidence 1-3 (how sure it's real yet)

    public static void main(String[] args) {
        List<Finding> findings = new ArrayList<>();
        findings.add(new Finding("List endpoint returns fewer items per page than 'per_page' asked for near the last page", 2, 3));
        findings.add(new Finding("A field is a string on the list view but a number on the detail view for the same resource", 3, 2));
        findings.add(new Finding("An update call accepts a field the docs never mention", 2, 1));
        findings.add(new Finding("Deleting a resource twice returns different status codes the second time", 2, 3));

        // Sort by severity desc, then confidence desc -- report the scariest,
        // best-evidenced findings first; a scary but low-confidence hunch
        // needs more repro work before it's worth writing up.
        findings.sort((a, b) -> {
            if (a.severity() != b.severity()) return b.severity() - a.severity();
            return b.confidence() - a.confidence();
        });

        System.out.println("=== Triage order for this session's findings ===");
        int rank = 1;
        for (Finding f : findings) {
            System.out.printf("%d. [sev %d, confidence %d/3] %s%n", rank++, f.severity(), f.confidence(), f.description());
        }

        System.out.println();
        System.out.println("Severity says how bad it is if true; confidence says how sure you are");
        System.out.println("it's actually true yet. Writing up #1 first, with its repro steps, beats");
        System.out.println("writing up all four in the order you happened to notice them.");
    }
}

/* === Triage order for this session's findings ===
   1. [sev 3, confidence 2/3] A field is a string on the list view but a number on the detail view for the same resource
   2. [sev 2, confidence 3/3] List endpoint returns fewer items per page than 'per_page' asked for near the last page
   3. [sev 2, confidence 3/3] Deleting a resource twice returns different status codes the second time
   4. [sev 2, confidence 1/3] An update call accepts a field the docs never mention

   Severity says how bad it is if true; confidence says how sure you are
   it's actually true yet. Writing up #1 first, with its repro steps, beats
   writing up all four in the order you happened to notice them. */
```

### Your first time: Your mission: run a real, structured hunt session against BuggyAPI

- [ ] Open BuggyAPI's OpenAPI docs and list every endpoint and applicable method — Your coverage matrix, before you send a single request.
- [ ] Authenticate and confirm the happy path on each resource once, with valid input — The boring pass — projects and tickets, GET/POST/PATCH/DELETE where each applies.
- [ ] Layer in negative cases per endpoint using this chapter's categories — Missing fields, wrong types, bad enums, missing auth — see [[api-testing-fundamentals/finding-api-bugs/negative-api-tests]].
- [ ] Spot-check at least one response against the OpenAPI spec field by field — See [[api-testing-fundamentals/finding-api-bugs/validating-against-the-spec]] for exactly what to check.
- [ ] Write down every finding immediately, with the exact request and response — don't rely on memory later — Triage by severity and confidence once you have more than one.

This is the whole chapter in one session: reading raw responses with no UI, deliberately sending
invalid input, measuring real responses against the documented spec, and doing all of it
systematically enough to know honestly what you covered.

- **You've tested for twenty minutes and found nothing yet — starting to wonder if you're doing something wrong.**
  Check your coverage matrix, not your confidence. A clean run through the happy path with no findings is a normal, honest result for well-tested surface area — it means move to the negative cases and the spec-validation pass, not that something about your approach is broken.
- **You found something that might be a bug, but you're not fully sure it's not just how the API is intentionally designed.**
  Check the OpenAPI spec before deciding either way — if the observed behavior matches the documented contract, it's not a finding, however odd it feels. If the spec is silent or contradicts what you saw, that itself is reportable, per [[api-testing-fundamentals/finding-api-bugs/validating-against-the-spec]].
- **You have several findings from one session and aren't sure which to write up first, or whether to write up all of them.**
  Triage by severity and confidence before writing anything — write up the highest-severity, highest-confidence finding completely and well rather than four findings sketched thinly. A complete, well-evidenced report beats a longer list of vague ones.

### Where to check

- **BuggyAPI's docs at `/api/docs`** — your coverage checklist and your spec-validation reference in
  one place; start every session here, not from memory of what the endpoints probably do.
- **The BuggyAPI home page's seeded sandbox credentials** — the fastest path to a working
  authenticated session, so time goes into testing, not into guessing valid login details.
- **[[api-testing-fundamentals/finding-api-bugs/testing-without-a-ui]]** — the raw-response reading
  discipline this whole session runs on, from the very first request you send.
- **[[defect-management/writing-bug-reports/anatomy-of-a-report]]** — once you have a finding worth
  keeping, this is the shape a report needs to take for someone else to act on it without redoing
  your work.

### Worked example: a finding that comes from testing a boundary, not a field

1. During a systematic pass, a tester notices that every resource in BuggyAPI is described as
   "scoped to your own sandbox" — so they deliberately test that boundary itself, not just each
   endpoint's normal behavior.
2. Using a ticket ID that belongs to a different sandbox (not one they created), they call
   `GET /v1/tickets/{id}` with their own valid auth token.
3. If the API is enforcing sandbox scoping correctly, this should fail — a `404` (treating another
   sandbox's data as if it doesn't exist to you) is the expected, spec-honest result.
4. Whatever actually comes back, this is exactly the kind of test that's easy to skip because it
   requires deliberately constructing a cross-boundary request instead of just exercising the normal
   surface — which is precisely why a systematic hunt makes time for it instead of leaving it to
   chance.
5. Reported either way is useful: a correct `404` confirms the boundary holds (worth noting as
   covered), and anything else is a serious finding — data isolation is a core guarantee, not a nice-
   to-have.

**Quiz.** After 20 minutes of testing BuggyAPI's happy-path endpoints with valid input, a tester has found zero bugs. What should they conclude?

- [ ] That BuggyAPI likely has no seeded bugs active and the session can end here
- [ ] That they're testing it wrong, since a bug-hunting exercise should always turn up something quickly
- [x] That the happy-path pass came back clean (a normal, honest result), and the next step is to move on to negative cases and spec validation, since a hunt isn't done until those are covered too
- [ ] That they should keep repeating the exact same happy-path requests until something eventually breaks

*This note's coverage-matrix framing is explicit: a hunt session isn't judged as 'done' by whether something has broken yet, it's judged by how much of the matrix (methods x endpoints x positive AND negative cases) has actually been exercised. A clean happy-path pass is a normal, legitimate outcome that simply means it's time to move to the next category — negative cases and spec validation — not a sign of failure or a reason to stop. Option one wrongly treats an early clean result as proof of a global absence of bugs, which the note explicitly warns against ('nothing found yet' in an unchecked area is untested, not clean). Option two assumes hunting must be fast, which isn't how the systematic approach this note teaches actually works. Option four mistakes repetition for the missing categories of testing that are actually needed next.*

- **What separates a 'bug hunt' from casually poking at an API** — Deliberate, systematic coverage of every endpoint and method, plus negative cases and spec checks — and an honest record of what was and wasn't actually tested.
- **BuggyAPI's real resource surface** — Auth (login, me), projects, and tickets — each with the HTTP methods documented in its own OpenAPI spec at /api/docs and /api/v1/openapi.json.
- **Why 'nothing found yet' needs a coverage record to mean anything** — Without one, 'I didn't find anything else' is indistinguishable from 'I didn't check anything else' — two very different claims.
- **The order to run a session in** — Map the surface via the spec, confirm the happy path once per resource, layer in negative cases per endpoint, spot-check against the spec, record findings as you go.
- **How to decide what to write up first when you have multiple findings** — Triage by severity (how bad if true) and confidence (how sure you are it's real) — write up the top one completely rather than several thinly.

### Challenge

Run one real, timed 30-minute hunt session against BuggyAPI. Before starting, list every endpoint
and applicable method from its OpenAPI docs as your coverage matrix. Work the happy path first, then
layer in negative cases, then spot-check one response against the spec. At the end, report your
coverage percentage honestly alongside anything you found — an accurate "60% covered, one finding"
is more useful than an inflated claim of having tested everything.

### Ask the community

> I ran a hunt session against BuggyAPI and found `[a short description of what looked wrong]` on `[endpoint/method]`. Here's the exact request and response I got. Does this look like a genuine finding, and if so, roughly what severity would you call it?

The most useful replies will ask for the exact request and response before weighing in on severity —
a vague description of "something looked off" is much harder to triage than the actual evidence.

- [OWASP API Security Top 10 — categories worth knowing even for non-security bug hunting](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [Martin Fowler — contract testing (the idea validating-against-the-spec builds toward)](https://martinfowler.com/articles/microservice-testing/#testing-contract-introduction)
- [Postman Learning Center — running a whole collection systematically](https://learning.postman.com/docs/collections/running-collections/intro-to-collection-runs/)

🎬 [EvilTester — API Challenges: a practice API application for testing tutorials](https://www.youtube.com/watch?v=rxEwPMM_Qyc) (8 min)

- A bug hunt is systematic coverage of a real API's surface area, not casual poking — the record of what was tested matters as much as what was found.
- BuggyAPI ('TaskFlight') is a real, spec-first API — auth, projects, tickets, an OpenAPI spec generated from the same schema the server validates against, and seeded bugs behind a mode flag.
- Run the boring happy-path pass first, on every endpoint and applicable method, before hunting for anything exotic.
- Layer in this chapter's other skills per endpoint: reading raw responses, negative test categories, and spec validation.
- Triage multiple findings by severity and confidence, and write up the strongest one completely rather than several thinly.


## Related notes

- [[Notes/api-testing-fundamentals/finding-api-bugs/testing-without-a-ui|Testing without a UI]]
- [[Notes/api-testing-fundamentals/finding-api-bugs/negative-api-tests|Negative API tests]]
- [[Notes/api-testing-fundamentals/finding-api-bugs/validating-against-the-spec|Validating against the spec]]
- [[Notes/defect-management/writing-bug-reports/anatomy-of-a-report|Anatomy of a report]]


---
_Source: `packages/curriculum/content/notes/api-testing-fundamentals/finding-api-bugs/your-first-api-bug-hunt.mdx`_
