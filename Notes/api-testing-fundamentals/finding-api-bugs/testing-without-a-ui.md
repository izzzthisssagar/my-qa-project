---
title: "Testing without a UI"
tags: ["api-testing-fundamentals", "finding-api-bugs", "track-c"]
updated: "2026-07-17"
---

# Testing without a UI

*No screen, no button to click, no visual 'that looks wrong' - when you're testing an API directly, the status code, headers, and raw JSON body ARE the interface, and reading them correctly is the whole skill.*

> A pilot flying through thick cloud can't look out the windscreen and eyeball the horizon - there's
> nothing to see. Every decision comes from the instrument panel: airspeed, altitude, heading,
> attitude, all read off dials with no visual confirmation from the world outside. Testing an API
> directly is the same situation - there's no page to look at, no button to click, no red border
> around the bad field. There's a status code, some headers, and a body. That's the entire panel.

> **In real life**
>
> A Cessna's instrument panel exists because flying by "it looks fine outside" stops working the
> moment visibility drops to zero - pilots train specifically on instrument-only flight because it's
> a genuinely different skill from flying VFR (visual flight rules) on a clear day. Testing an API
> without a UI is the same shift: you can't glance at a screen and think "that looks off." You read
> the status code the way a pilot reads the altimeter - deliberately, every time, because it's the
> only source of truth you've got.

**Testing without a UI**: Testing without a UI means exercising an API directly - via curl, Postman, or code - and judging correctness from the raw HTTP response (status code, headers, body) instead of from rendered pixels. It's also called API-level or headless testing. The skill isn't a new tool, it's a shift in what counts as evidence: nothing is 'obviously wrong' until you've actually read the response.

## Why this is a different skill, not just a different tool

- **A UI does interpretation for you, for free.** A broken save shows a red toast. A missing field
  shows a blank box. Testing the API directly means YOU are the interpretation layer - the status
  code and body are neutral facts until you decide what they mean against what should have happened.
- **Nothing fails loudly by default.** A UI bug is often visually obvious. An API bug can be a
  `200 OK` with subtly wrong data inside it - the request "succeeded" and looks calm from a distance,
  which is exactly why reading the body matters as much as reading the status line.
- **You lose incidental context a UI gives away for free** - which button was clicked, what the form
  looked like before submit. Testing without a UI means the request you send is the ENTIRE story;
  if you don't log what you sent, you can't explain what you found.
- **The response has more parts than a screen shows.** Headers (`Content-Type`, `Cache-Control`,
  rate-limit headers) rarely have any UI equivalent at all - they're invisible unless you go looking,
  which most manual UI testing never does.

> **Tip**
>
> Read a response in a fixed order every time: status code first, then the headers that matter
> (`Content-Type` at minimum), then the body. Skipping straight to "does the body look right" is how
> a `200` that should have been a `201`, or a missing `Content-Type`, slides past unnoticed.

> **Common mistake**
>
> Treating "the request didn't error" as "the test passed." A request that returns `200` with a body
> that's silently wrong (a stale field, a dropped filter, the wrong resource) LOOKS like a pass if you
> only glance at the status code. Without a UI to flash red, the only thing standing between you and
> that bug is actually reading the body against what you expected.

![Close-up of a Cessna 172 aircraft cockpit instrument panel, showing rows of analog gauges and a radio stack, with no view outside the aircraft](testing-without-a-ui.jpg)
*Cessna 172 Instrument Panel (left), photo by Theo, 2006 — Wikimedia Commons, CC BY-SA 2.5. [Source](https://commons.wikimedia.org/wiki/File:Cessna_172_Instrument_Panel_(left)_(Photo_by_Theo,_2006).jpg)*
- **The altimeter and airspeed dials — your status code** — The two numbers a pilot checks first, every time, no matter how the flight feels. The HTTP status code is the same: the first fact you read, before you form any opinion about whether the response is 'right'.
- **The compass and heading indicators — your response headers** — Easy to ignore because nothing forces you to look at them, but they carry real information (Content-Type, rate-limit headers, caching directives) that a UI would almost never surface to a tester at all.
- **The radio stack — the raw body you actually read** — Dense, text-heavy, and the thing a pilot spends the most active attention on mid-flight. The JSON body is where most of your actual verification time goes — it's also where a subtly-wrong value hides best.

**Reading a response with no UI to interpret it for you**

1. **Send the request** — curl, Postman, or a script — capture exactly what you sent (method, URL, headers, body) so the result is reproducible.
2. **Read the status code first** — Before anything else. Does the code even belong to the right family for what you asked (2xx for a clean write, 4xx for a bad request)?
3. **Check the headers that matter** — Content-Type at minimum — a body that looks like JSON served as text/plain is still a bug, even though the body reads fine.
4. **Read the body against what you expected** — Field by field, not 'skim and it looks plausible.' A wrong value that's still valid JSON produces zero visual signal on its own.
5. **Write down what you sent AND what came back** — There's no screenshot to fall back on later — the request/response pair IS your evidence.

The check itself is nothing exotic — it's the discipline of actually looking at every part of the
response instead of skimming for a vibe:

*Run it — reading a raw API response with no screen to glance at (Python)*

```python
def check_api_response(status_code, headers, body):
    print("=== Reading the raw response (no UI, no screen -- just this) ===")
    print(f"HTTP status: {status_code}")
    print(f"Content-Type header: {headers.get('Content-Type')}")
    print(f"Body: {body}")
    print()

    checks = []
    checks.append(("Status code is 200", status_code == 200))
    checks.append(("Content-Type is JSON", "application/json" in headers.get("Content-Type", "")))
    checks.append(("Body has 'id' field", "id" in body))
    checks.append(("Body 'status' field is 'active'", body.get("status") == "active"))

    print("=== Assertions -- this IS the test, there's no screen to eyeball ===")
    passed = 0
    for name, ok in checks:
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {name}")
        if ok:
            passed += 1
    print()
    print(f"{passed}/{len(checks)} checks passed")
    return passed == len(checks)

# Standing in for what curl -i or Postman's response pane would show you --
# this IS the interface when there's no UI to look at.
response_status = 200
response_headers = {"Content-Type": "application/json; charset=utf-8"}
response_body = {"id": "6fa1c07e-2f34-4b1e-9c3a-5d2f8a91b0aa", "status": "active", "name": "Ground Ops"}

all_ok = check_api_response(response_status, response_headers, response_body)
print()
print("Overall:", "ALL CHECKS PASSED" if all_ok else "SOMETHING FAILED")

# === Reading the raw response (no UI, no screen -- just this) ===
# HTTP status: 200
# Content-Type header: application/json; charset=utf-8
# Body: {'id': '6fa1c07e-2f34-4b1e-9c3a-5d2f8a91b0aa', 'status': 'active', 'name': 'Ground Ops'}
#
# === Assertions -- this IS the test, there's no screen to eyeball ===
# [PASS] Status code is 200
# [PASS] Content-Type is JSON
# [PASS] Body has 'id' field
# [PASS] Body 'status' field is 'active'
#
# 4/4 checks passed
#
# Overall: ALL CHECKS PASSED
```

The same discipline in Java — deliberately reading every part before deciding anything passed:

*Run it — the same read-everything discipline (Java)*

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class Main {
    static boolean check(String name, boolean ok, int[] tally) {
        System.out.println("[" + (ok ? "PASS" : "FAIL") + "] " + name);
        if (ok) tally[0]++;
        tally[1]++;
        return ok;
    }

    public static void main(String[] args) {
        // Standing in for what curl -i or Postman's response pane would show
        // you -- this IS the interface when there is no UI to look at.
        int status = 200;
        Map<String, String> headers = new LinkedHashMap<>();
        headers.put("Content-Type", "application/json; charset=utf-8");
        Map<String, String> body = new LinkedHashMap<>();
        body.put("id", "6fa1c07e-2f34-4b1e-9c3a-5d2f8a91b0aa");
        body.put("status", "active");
        body.put("name", "Ground Ops");

        System.out.println("=== Reading the raw response (no UI, no screen -- just this) ===");
        System.out.println("HTTP status: " + status);
        System.out.println("Content-Type header: " + headers.get("Content-Type"));
        System.out.println("Body: " + body);
        System.out.println();

        System.out.println("=== Assertions -- this IS the test, there's no screen to eyeball ===");
        int[] tally = new int[2]; // {passed, total}
        check("Status code is 200", status == 200, tally);
        check("Content-Type is JSON", headers.get("Content-Type").contains("application/json"), tally);
        check("Body has 'id' field", body.containsKey("id"), tally);
        check("Body 'status' field is 'active'", "active".equals(body.get("status")), tally);

        System.out.println();
        System.out.println(tally[0] + "/" + tally[1] + " checks passed");
        System.out.println();
        System.out.println("Overall: " + (tally[0] == tally[1] ? "ALL CHECKS PASSED" : "SOMETHING FAILED"));
    }
}

/* === Reading the raw response (no UI, no screen -- just this) ===
   HTTP status: 200
   Content-Type header: application/json; charset=utf-8
   Body: {id=6fa1c07e-2f34-4b1e-9c3a-5d2f8a91b0aa, status=active, name=Ground Ops}

   === Assertions -- this IS the test, there's no screen to eyeball ===
   [PASS] Status code is 200
   [PASS] Content-Type is JSON
   [PASS] Body has 'id' field
   [PASS] Body 'status' field is 'active'

   4/4 checks passed

   Overall: ALL CHECKS PASSED */
```

### Your first time: Your mission: test one real endpoint with nothing but the raw response

- [ ] Pick one GET endpoint you can call without a UI (BuggyAPI, a public API, or curl against something local) — curl -i shows you the status line and headers as well as the body — the -i flag is what makes them visible at all.
- [ ] Write down what you expect BEFORE you send the request — Expected status code, expected shape of the body — commit to it first, so you can't unconsciously rationalize the actual response afterward.
- [ ] Send it, then read the status code out loud (or write it down) before looking at anything else — Building the habit of not skipping straight to the body.
- [ ] Check the Content-Type header specifically — It's the header most UI-first testers have never once looked at.
- [ ] Compare the body field-by-field against what you wrote down — Not 'does it look plausible' — does each field match what you predicted, exactly.

You've practiced the core discipline this whole chapter builds on: deciding correctness from the
raw response alone, in a fixed order, instead of from a vibe.

- **You keep re-reading the same response and still aren't sure if it's 'right' — nothing visually flags a problem.**
  That uncertainty is the actual signal that you don't have a written expectation yet. Go back and write down, in words, exactly what a correct response looks like BEFORE sending the request again — the ambiguity usually turns out to be in your own expectation, not the response.
- **A request 'worked' (200, sensible-looking JSON) but something about it still feels off days later.**
  Recheck against the documented contract field-by-field rather than trusting the earlier gut check — this is exactly the gap [[api-testing-fundamentals/finding-api-bugs/validating-against-the-spec]] covers, and 'felt fine at a glance' is precisely the failure mode that check exists to catch.
- **You want to test something a UI would never let you send at all (a malformed body, a missing header) and aren't sure that counts as a real test.**
  It's not just a real test, it's a category of test a UI usually can't reach — see [[api-testing-fundamentals/finding-api-bugs/negative-api-tests]] for how to run it and what a correct rejection looks like.

### Where to check

- **`curl -i` (or `-v` for full verbosity)** — the `-i` flag alone is the single habit that turns a response from invisible into readable; without it you only see the body.
- **Postman's response pane** — status code and time sit above the body by default, and headers get their own tab, which nudges you toward reading them instead of skipping straight to JSON.
- **The API's own OpenAPI docs (BuggyAPI serves them at `/api/docs`)** — the fastest way to know what "expected" looks like before you send anything, instead of guessing after the fact.
- **[[defect-management/writing-bug-reports/anatomy-of-a-report]]** — once you've read a response and found something wrong, this is how that finding becomes a report someone else can act on.

### Worked example: a response that 'looks fine' and isn't

1. Testing `GET /v1/projects/{id}` against BuggyAPI, a tester sends a request for a project they
   just created and gets back `200 OK` with a JSON body. Glancing at it, it has an `id`, a `name`,
   a `status` — looks like a project. Tempting to call it a pass and move on.
2. Reading it properly against the documented `Project` schema instead: `status` is supposed to be
   one of `"active"` or `"archived"`. This response has `"status": "Active"` — capitalized.
3. That's easy to miss on a glance because the body still LOOKS like a normal project object. Only
   reading each field against what the spec actually promises catches the casing mismatch.
4. This is a real finding: any client code written against the documented enum values (lowercase)
   will fail to match this response, silently, the first time it checks `status === "active"`.
5. Nothing about the status code, the overall shape, or a casual read flagged this. Only the
   discipline of checking the actual field value against the actual documented contract did.

**Quiz.** You send a request to an API with no UI in front of it and get back a 200 status code with a JSON body that contains all the fields you expected. Is the test done?

- [ ] Yes — a 200 status code with the right fields present means the response is correct
- [x] No — the status code and field presence are a start, but each field's actual VALUE still needs to be checked against what was expected, since nothing will visually flag a wrong value
- [ ] No, because a manual API test always requires re-running the request at least three times
- [ ] Yes, but only if the response also included a Content-Type header

*This note's whole point is that a UI does interpretation work you have to do yourself when there's no UI: a 200 with the right fields PRESENT still says nothing about whether those fields' VALUES are correct. Option one stops at 'looks structurally fine,' which is exactly the trap the note warns about — a silently wrong value inside a 200 produces zero visual signal. Option three invents an unrelated rule. Option four correctly names something worth checking (Content-Type matters), but wrongly treats it as sufficient on its own — headers are one part of the response, not a substitute for reading the body's actual values.*

- **What replaces a UI's visual feedback when testing an API directly?** — The raw HTTP response — status code, headers, and body — read deliberately, since nothing fails loudly by default the way a red UI error does.
- **The fixed order to read a response in** — Status code first, then the headers that matter (Content-Type at minimum), then the body field-by-field against a written expectation.
- **Why '200 and it looks plausible' isn't enough** — A 200 can still contain a subtly wrong value — a UI would often flash an error for this, but a raw response gives zero visual signal unless you actually check each field.
- **What you lose by skipping curl's -i flag (or Postman's headers tab)** — The headers entirely — Content-Type, caching, rate-limit headers rarely have any UI equivalent, so most manual UI testers have never once had a reason to look at them.
- **Why writing down your expectation BEFORE sending the request matters** — It stops you from unconsciously rationalizing whatever comes back as 'probably fine' — without a screen to compare against, your own written expectation is the only fixed reference point.

### Challenge

Pick any GET endpoint you can call without a UI (BuggyAPI, a public API, or something local). Write
down your expected status code and expected body shape BEFORE sending the request. Send it with
`curl -i` (or Postman), then check the status code, the `Content-Type` header, and every field in
the body against what you wrote down. Note anywhere your actual expectation turned out to be vague —
that vagueness is usually the real finding.

### Ask the community

> I'm testing `[endpoint]` with no UI in front of it and got back `[status code + a short description of the body]`. I expected `[what you expected]`. Is this a real finding, or am I missing something about what the response is actually supposed to look like?

The most useful replies will ask what the documented contract actually says before agreeing
anything is wrong — a lot of "that looks off" reactions to raw JSON turn out to be an
undocumented-but-intentional shape, not a bug.

- [curl docs — reading HTTP responses (status line, headers, body)](https://everything.curl.dev/http/responses.html)
- [Postman Learning Center — working with responses](https://learning.postman.com/docs/sending-requests/response-data/response-data/)
- [MDN — HTTP headers reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

🎬 [Joshua Morony — How to test like a 'real' API dev](https://www.youtube.com/watch?v=vcJhW1fL7a4) (5 min)

- With no UI, the status code, headers, and body ARE the interface — nothing fails loudly by default the way a red UI error would.
- Read a response in a fixed order every time: status code, then relevant headers (Content-Type at minimum), then the body field-by-field.
- A 200 with all the right fields present still isn't 'done' — each field's VALUE needs checking against a written expectation, not a glance.
- Write your expectation down before sending the request, so there's a fixed reference point instead of an after-the-fact rationalization.
- The request/response pair is your entire evidence trail — there's no screenshot to fall back on later.


## Related notes

- [[Notes/api-testing-fundamentals/finding-api-bugs/negative-api-tests|Negative API tests]]
- [[Notes/api-testing-fundamentals/finding-api-bugs/validating-against-the-spec|Validating against the spec]]
- [[Notes/defect-management/writing-bug-reports/anatomy-of-a-report|Anatomy of a report]]


---
_Source: `packages/curriculum/content/notes/api-testing-fundamentals/finding-api-bugs/testing-without-a-ui.mdx`_
