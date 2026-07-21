---
title: "Postman requests"
tags: ["api-testing-fundamentals", "postman-and-curl", "track-c"]
updated: "2026-07-17"
---

# Postman requests

*Postman's request builder is curl's four building blocks - URL, method, headers, body - rearranged into tabs and a Send button, plus a response viewer and a Code button that proves the two tools speak the exact same underlying request.*

> The previous note built a request out of curl flags, one at a time. Postman builds the *exact same request* out of form fields, one tab at a time - a URL bar, a method dropdown, a Headers tab, a Body tab, and a Send button where curl had Enter. Nothing about HTTP changed; only the interface did. Prove it to yourself and Postman stops being "the tool with the intimidating UI" and becomes "curl with a response viewer attached."

> **In real life**
>
> A postal worker heading out on a round, satchel over the shoulder, checking the paperwork before setting off - the photo below. Every letter already has an address, a class of service, sometimes special handling instructions; the postal worker's job is arranging and dispatching, not reinventing what a letter is. Postman is the same relationship to a request: the URL, method, headers and body are the letter's contents, already fully specified by HTTP - Postman is the organized, repeatable dispatch system built around sending (and re-sending, and organizing into rounds) exactly that same letter.

**Postman request builder**: Postman's request builder maps directly onto curl's flags: the URL bar is the URL, a Method dropdown replaces -X, the Headers tab replaces repeated -H flags, and the Body tab (with a Raw/JSON option) replaces -d. Clicking Send performs the request and opens a Response panel showing status code, response time, size, headers, and a syntax-highlighted, auto-formatted body - the GUI equivalent of curl -i piped through a JSON formatter. A '</>' Code button on every request generates the equivalent curl command (or Python, JavaScript, and other languages) for that exact request, which is the fastest way to confirm the two tools are doing identical work.

## The same four fields, now as UI

- **URL bar** — paste or type the endpoint. Postman auto-detects `{{variables}}` inside it (next note's whole subject) and highlights them.
- **Method dropdown** — GET, POST, PUT, PATCH, DELETE and more, no `-X` typo possible since it's a fixed list.
- **Headers tab** — a key/value table. Postman auto-adds a few sensible defaults (like `Accept: */*`) that you can override or delete, mirroring what curl adds silently too.
- **Body tab** — `none`, `form-data`, `x-www-form-urlencoded`, `raw` (with a JSON/XML/Text sub-picker), or `binary`. Selecting `raw` → `JSON` is the GUI equivalent of `-d` plus a `Content-Type: application/json` header - and Postman sets that header for you automatically, a detail curl leaves entirely manual.

> **Tip**
>
> The **Code** button (the `</>` icon, usually top-right of the request panel) is the fastest way to sanity-check a Postman request: generate the cURL snippet and read it. If something in the response is confusing you, reading the equivalent curl command often reveals a header or body detail the UI's tabs made easy to miss - the same request, described more explicitly.

> **Common mistake**
>
> Assuming Postman's auto-added headers (like a default `User-Agent: PostmanRuntime/x.x.x`) are invisible or don't matter. They're real headers sent with every request, and some APIs behave differently based on `User-Agent` or reject unfamiliar ones outright. If a request works in Postman but an equivalent-looking curl command fails (or vice versa), compare headers via the Code button first - the "equivalent" requests are rarely byte-identical unless you make them so.

![A postal worker in uniform standing beside a bicycle fitted with a mail satchel, checking papers before setting off on a delivery round](postman-requests.jpg)
*Postman with bicycle — ThePoeticFrame, Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Postman_with_bicycle.jpg)*
- **Checking the paperwork before departing** — Confirming the details before dispatch - exactly what reading a request's Headers and Body tabs before hitting Send is. The letter (request) is already fully specified; this is verification, not composition from scratch.
- **The satchel on the bicycle — the vehicle for many letters, organized** — Not one letter loose in a pocket - a whole round, carried together. This is the direct preview of the next note: a Postman Collection is exactly this, many requests grouped and carried together instead of pasted one at a time.
- **Other bicycles parked, waiting for their own rounds** — Different rounds, different routes, same basic vehicle. Postman Environments (also next note) are this: the same collection of requests, run against a different base address depending on which 'round' - dev, staging, prod - is currently active.

**From curl flag to Postman tab - press Play**

1. **-X becomes the Method dropdown** — No typo risk - GET, POST, PUT, PATCH, DELETE are a fixed list instead of a string you type. The HTTP semantics underneath are unchanged.
2. **-H becomes the Headers tab** — Each -H 'Name: value' flag becomes one row in a key/value table. Postman shows you its own auto-added headers here too, greyed out but real and sent.
3. **-d becomes the Body tab** — Raw > JSON in the Body tab is -d plus an automatic Content-Type: application/json header - one less thing to remember to set by hand versus curl.
4. **Send becomes Enter, and the Response panel becomes -i piped through a formatter** — Status, time, size, headers, and an auto-indented body - everything curl -i gives you as raw text, now laid out and color-coded.

Prove the equivalence by sending literally the same request both ways:

*Run it - the raw request, exactly what Postman's Send button would fire*

```bash
curl -s -X POST "https://postman-echo.com/post" \\
  -H "Content-Type: application/json" \\
  -H "X-Client: qa-mastery-notes" \\
  -d '{"flightNumber":"QA123","seat":"14C","checkedBags":1}' | python3 -m json.tool

# {
#     "args": {},
#     "data": {
#         "flightNumber": "QA123",
#         "seat": "14C",
#         "checkedBags": 1
#     },
#     "files": {},
#     "form": {},
#     "headers": {
#         "host": "postman-echo.com",
#         "content-length": "53",
#         "user-agent": "curl/8.7.1",
#         "x-client": "qa-mastery-notes",
#         "content-type": "application/json",
#         "accept": "*/*",
#         "x-forwarded-proto": "https",
#         "accept-encoding": "gzip, br"
#     },
#     "json": {
#         "flightNumber": "QA123",
#         "seat": "14C",
#         "checkedBags": 1
#     },
#     "url": "https://postman-echo.com/post"
# }

# This is literally what fills in when you set Method=POST, add a
# Content-Type and X-Client row in Headers, and paste the JSON into
# Body > raw > JSON, then click Send. Same bytes, different interface.
```

The Python this note's playground actually runs is what Postman's **Code** button would hand you for this exact request (`</>` → Python - Requests):

*Run it - the same request as Postman's generated Python snippet*

```python

```
 icon) would generate for Python - Requests
# after you build this request in the UI: method POST, URL, a header, a JSON body.
url = "https://postman-echo.com/post"
headers = {
    "Content-Type": "application/json",
    "X-Client": "qa-mastery-notes",  # a custom header, same as a "Headers" tab row
}
payload = {
    "flightNumber": "QA123",
    "seat": "14C",
    "checkedBags": 1,
}

response = requests.post(url, headers=headers, json=payload, timeout=10)

print(f"Status: {response.status_code} {response.reason}")
print(f"Content-Type: {response.headers.get('content-type')}")
print()
body = response.json()
print("Echoed request body Postman/curl actually sent (from postman-echo's echo):")
print(json.dumps(body["json"], indent=2))
print()
print("Echoed headers the server received (trimmed to the ones we set):")
sent_headers = body["headers"]
print(f"  content-type: {sent_headers.get('content-type')}")
print(f"  x-client:     {sent_headers.get('x-client')}")

# Status: 200 OK
# Content-Type: application/json; charset=utf-8
#
# Echoed request body Postman/curl actually sent (from postman-echo's echo):
# {
#   "flightNumber": "QA123",
#   "seat": "14C",
#   "checkedBags": 1
# }
#
# Echoed headers the server received (trimmed to the ones we set):
#   content-type: application/json
#   x-client:     qa-mastery-notes`}
/>

### Your first time: Your mission: build one request in Postman, then prove it against curl

) and select cURL", detail: "Read the generated command line by line against what you built in the UI - every field you filled in should appear somewhere in that command." },
    { text: "Switch the Code button's language to Python - Requests", detail: "Compare it against this note's second playground - the shape should be nearly identical: a headers dict, a payload, one requests call." },
    { text: "Build the same request as a raw curl command from scratch, without the Code button", detail: "Run it in a terminal and diff the response body against what Postman showed you - they should match exactly, proving the two tools performed the same HTTP transaction." },
  ]}
/>
You've now built the identical request three ways - Postman's UI, its generated code, and raw curl - and confirmed HTTP doesn't care which one sent it.

- **A request works when pasted as curl in a terminal, but fails (or behaves differently) from inside Postman.**
  Compare headers via the Code button first - Postman auto-adds its own User-Agent, Accept, and sometimes Postman Console-visible headers that a bare curl command won't have unless you add them explicitly. Some APIs allow/deny based on User-Agent; check the Postman Console (View > Show Postman Console) to see the exact outgoing request Postman actually sent, not just what the tabs implied.
- **The Body tab shows valid JSON, but the server responds as if it received no body or a malformed one.**
  Check that Body > raw has JSON selected in the dropdown next to 'raw' (it defaults to Text) - Text mode sends the exact same bytes but WITHOUT the Content-Type: application/json header, and plenty of servers refuse to parse a JSON-shaped body sent as text/plain. This is the GUI version of forgetting -H 'Content-Type: application/json' in curl.
- **Query params typed into the URL bar don't match what shows in the Params tab, or vice versa.**
  Postman keeps the URL bar and the Params tab in sync in both directions, but paste-based edits (pasting a whole new URL with different params) can occasionally desync from a stray encoded character. Retype the differing param manually in the Params tab, confirm the URL bar updates, and if it still disagrees, delete the request and rebuild it - a corrupted param row is rare but not worth debugging further than one retry.

### Where to check

- **The `</>` Code button** — on every request, generates curl (and 20+ other languages) for exactly what Postman would send; the single fastest equivalence check between this note and the last one.
- **View → Show Postman Console** — the real outgoing request and incoming response, unfiltered by the tabs' summarized view; the GUI's answer to `curl -v`.
- **The Response panel's header bar** — status, time, size, at a glance, before opening any tab.
- **[[api-testing-fundamentals/postman-and-curl/curl-basics]]** — every field in this note's request builder maps onto a flag covered there; when a Postman behavior is confusing, translating it back to curl is often the fastest way to understand it.

### Worked example: chasing a header mismatch between curl and Postman

1. A tester reports: "This endpoint returns 401 when I call it with curl, but 200 in Postman - same URL, same body. Which one is 'right'?"
2. First move: Postman's Code button, set to cURL, on the working Postman request - not writing curl from memory, generating it from the exact request that's succeeding.
3. Diffing the generated command against the tester's original curl command line by line surfaces it: the generated one has an extra `-H "Authorization: Bearer eyJ..."` header the tester's hand-written version never included.
4. Root cause: the tester was testing the request logic in isolation and genuinely forgot the endpoint needs auth - Postman had it saved from an earlier request and carried it forward, curl had no memory of anything.
5. Neither tool was "wrong" - the requests were never actually identical, and the Code button proved it in under a minute instead of a longer manual header-by-header audit.
6. Lesson banked: "requests behave differently" is a testable claim, not a mystery - generate the exact command for the WORKING case and diff it against the FAILING one; the difference is the finding.

**Quiz.** A Postman request's Body tab has 'raw' selected with valid JSON typed in, but the type dropdown next to 'raw' is set to Text instead of JSON. What's the most likely consequence?

- [ ] Postman will refuse to send the request until JSON is selected
- [x] The exact same bytes are sent, but WITHOUT a Content-Type: application/json header, so some servers will fail to parse a body that is actually valid JSON
- [ ] The request will send as XML instead of JSON
- [ ] Nothing changes - the raw/Text vs raw/JSON dropdown only affects Postman's own syntax highlighting

*This note's WhenItBreaks entry covers this directly: the raw/Text vs raw/JSON dropdown controls which Content-Type header Postman attaches, not whether Postman will send the request - it sends fine either way. Text mode sends valid-looking JSON bytes without the header telling the server how to interpret them, which is the GUI equivalent of forgetting -H 'Content-Type: application/json' in [[api-testing-fundamentals/postman-and-curl/curl-basics]]. Many servers require that header to parse the body as JSON at all and will error or silently ignore fields without it. XML isn't involved unless explicitly selected, and the dropdown's effect is a real behavioral difference (a missing header), not merely cosmetic highlighting.*

 Code button, set to cURL - generates the exact equivalent command for the current request, which is also useful for pasting into a bug report as plain text." },
    { front: "raw/Text vs raw/JSON in the Body tab", back: "Same bytes sent either way, but JSON mode adds a Content-Type: application/json header that Text mode omits - many servers need that header to parse the body correctly." },
    { front: "Where to see the truly raw outgoing request", back: "View → Show Postman Console - the unfiltered request and response, Postman's equivalent of curl -v, useful when the tabs' summary view hides something." },
    { front: "Why Postman auto-added headers matter", back: "They're real and sent with every request (e.g. a default User-Agent) - if a curl command and a Postman request 'look the same' but behave differently, compare headers via the Code button before assuming a bug." },
  ]}
/>

### Challenge

Build the same POST request two ways: once in Postman's UI (URL, one custom header, a JSON body), once as a hand-typed curl command with no help from the Code button. Run both against postman-echo.com/post, and diff the two response bodies field by field. Then use the Code button on the Postman version to generate its curl equivalent and diff THAT against your hand-typed command - note every difference (headers Postman added that you didn't type) and explain each one.

### Ask the community

> A request behaves differently in Postman vs curl even though I believe I built them identically: [describe the difference in status/body/behavior]. Here's my curl command: [paste it]. Here's what the Postman Code button generates for the same request: [paste it]. What's the actual difference?

The most useful replies will ask for the Code-button-generated curl specifically, not a re-typed approximation - most "Postman vs curl" mysteries turn out to be one extra or missing header (often auth, sometimes User-Agent) that's invisible until the two commands are diffed side by side.

- [Postman Docs — Sending your first request](https://learning.postman.com/docs/getting-started/first-steps/sending-the-first-request/)
- [Postman — the Echo API (postman-echo.com) reference](https://learning.postman.com/docs/developer/echo-api/)

🎬 [Postman — How to Send Your First API Request in Postman](https://www.youtube.com/watch?v=YKalL1rVDOE) (4 min)

 Code button generates the exact equivalent curl (or Python, or 20+ languages) for any Postman request - the fastest way to verify what a request actually sends, and useful for pasting into bug reports as text.",
    "Body tab raw/Text vs raw/JSON sends identical bytes but a different Content-Type header - the GUI version of remembering (or forgetting) curl's -H 'Content-Type: application/json'.",
    "Postman auto-adds real headers (like User-Agent) you didn't type - when 'equivalent' curl and Postman requests behave differently, compare headers via the Code button before assuming a bug.",
    "View → Show Postman Console is the unfiltered ground truth of what was actually sent and received, Postman's answer to curl -v.",
  ]}
/>


## Related notes

- [[Notes/api-testing-fundamentals/postman-and-curl/curl-basics|curl basics]]
- [[Notes/api-testing-fundamentals/postman-and-curl/collections-and-environments|Collections & environments]]
- [[Notes/testers-toolbox/cookies-json-sessions/json-formatters|JSON formatters]]
- [[Notes/browser-devtools-mastery/network/copy-as-curl|copy-as-curl]]


---
_Source: `packages/curriculum/content/notes/api-testing-fundamentals/postman-and-curl/postman-requests.mdx`_
