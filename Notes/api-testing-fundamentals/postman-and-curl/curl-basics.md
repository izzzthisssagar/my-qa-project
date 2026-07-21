---
title: "curl basics"
tags: ["api-testing-fundamentals", "postman-and-curl", "track-c"]
updated: "2026-07-17"
---

# curl basics

*curl is a command-line HTTP client - four building blocks (URL, method, headers, body) cover almost every request a tester needs, and because it's just text, every request you build is copy-pasteable evidence for a bug report.*

> Every GUI API tool - Postman included - is a pretty face bolted onto the same four things: a URL, a method, some headers, maybe a body. curl **is** that skeleton, with no face at all. Learn curl first and Postman stops looking like software; it starts looking like a form for filling in the same four blanks you already understand. And unlike a GUI, curl fits in a bug report as three lines of plain text anyone can paste and rerun.

> **In real life**
>
> An old telegraph key - the photo below - sends a message with nothing but a switch, a wire, and an operator who knows the code. No screen, no menus, no autocomplete: press the key in the right pattern and the message goes out exactly as intended, character by character, with nothing hidden between the operator's hand and the wire. curl is the same idea a century later: no rendering, no click-through wizard, just a line of text that says precisely what goes out - method, address, and payload - with nothing added or interpreted on your behalf.

**curl**: curl is a command-line tool for sending HTTP (and other protocol) requests and printing the response, using flags to control every part of the request: -X sets the method (GET is the default if omitted), -H adds a header (repeatable), -d/--data sends a request body (and implies POST if no -X is given), and -i prints the response status line and headers along with the body. Because the entire request is one line of plain text, it is trivially shareable, scriptable, and rerunnable - the same request typed twice sends the same bytes twice.

## The four blocks, in curl's own vocabulary

- **URL** — the only required argument. `curl https://api.example.com/flights` sends a GET with no fuss.
- **Method** — `-X POST` (or PUT, PATCH, DELETE). Skip `-X` entirely and curl infers GET, or POST the moment you add `-d`.
- **Headers** — `-H "Header-Name: value"`, one flag per header, repeated as many times as needed. `Content-Type`, `Authorization`, and custom `X-` headers all go here.
- **Body** — `-d '{"key":"value"}'` for a raw string, or `-d @file.json` to send a file's contents without retyping it.

> **Tip**
>
> Add `-i` by reflex on every request while you're testing. It prepends the HTTP status line and every response header before the body - the difference between "I got some JSON back" and "I got a 201 back with a `Location` header pointing at the new resource." Skipping `-i` is the single most common way testers miss that a "successful-looking" response was actually a 404 with an HTML error page as its body.

> **Common mistake**
>
> Forgetting that `-d` silently switches the method to POST. A GET request built with `curl -X GET https://api.example.com/search -d '{"q":"test"}'` looks intentional, but many servers strip the body from GET entirely or ignore it - the query params never arrive. If a request needs a body, question whether GET is even the right verb; if it needs to stay GET, the data belongs in the URL's query string, not `-d`.

![A vintage brass Morse telegraph key mounted on a dark wood base, studio photograph on a black background](curl-basics.jpg)
*Morse key (CNAM 14674) — Rama, Wikimedia Commons, CC BY-SA 3.0 FR. [Source](https://commons.wikimedia.org/wiki/File:Morse_key-CNAM_14674-2-IMG_5195-black.jpg)*
- **The knob — the operator's only input** — One point of contact, pressed in a precise pattern. That's a curl command: one line, typed precisely, with nothing left to a mouse click landing in the wrong place.
- **The brass contact mechanism — where the message actually goes out** — Everything above this point is just how a human operates it; the contact itself is the real circuit. curl's flags (-X, -H, -d) are exactly this: the human-readable controls sitting directly on top of the raw HTTP request with nothing translating in between.
- **The adjustment terminals — tunable, but rarely touched** — A telegraph operator tunes contact gap and spring tension once, then just sends. curl has the same handful of flags (-i, --max-time, -s) you set once as habits and then stop thinking about - the four core blocks (URL, method, headers, body) are what change request to request.

**Building one curl command from nothing - press Play**

1. **Start with the URL alone** — curl https://postman-echo.com/get - no flags at all still sends a real GET request and prints the response body. This is the minimum viable curl command.
2. **Add -i to see the status and headers** — curl -i https://postman-echo.com/get - now the response starts with 'HTTP/2 200' and every header the server sent, before the body. This one flag turns curl from 'body only' into a real diagnostic tool.
3. **Add a header with -H** — -H 'Content-Type: application/json' tells the server how to parse the body that follows. Forget this header on a JSON body and plenty of APIs will silently treat it as a plain string instead.

Run the same request two ways - full body first, then trimmed to just the status line:

*Run it - a real GET request against Postman's public echo API*

```bash
# postman-echo.com is Postman's own free, public test API - built for exactly
# this: a real endpoint to point curl (or Postman) at with no setup required.

curl -s "https://postman-echo.com/get?flight=QA123&seat=14C"

# {"args":{"flight":"QA123","seat":"14C"},"headers":{"host":"postman-echo.com",
# "user-agent":"curl/8.7.1","accept":"*/*","x-forwarded-proto":"https",
# "accept-encoding":"gzip, br"},"url":"https://postman-echo.com/get?flight=QA123&seat=14C"}

# Now with -i - status line and headers appear BEFORE the body:
curl -s -i "https://postman-echo.com/get?flight=QA123" | head -20

# HTTP/2 200
# date: Thu, 16 Jul 2026 21:37:38 GMT
# content-type: application/json; charset=utf-8
# content-length: 213
# etag: W/"d5-D1RNOYEr4udmQvWDotIU65HqMiI"
# vary: Accept-Encoding
# x-envoy-upstream-service-time: 5
# cf-cache-status: DYNAMIC
# ...(cookie and server headers trimmed for readability)...
# server: cloudflare
#
# {"args":{"flight":"QA123"},"headers":{"host":"postman-echo.com","user-agent":
# "curl/8.7.1","accept":"*/*","x-forwarded-proto":"https","accept-encoding":
# "gzip, br"},"url":"https://postman-echo.com/get?flight=QA123"}

# Notice the response ECHOES what curl sent - postman-echo.com's whole job is
# reflecting your request back at you, which makes it perfect for learning
# curl: you can see exactly what left your machine, not just what a real
# backend chose to tell you.
```

A POST with a JSON body, plus the status-only pattern from a real script:

*Run it - POST with a body, then a status-only check*

```bash
curl -s -X POST "https://postman-echo.com/post" \\
  -H "Content-Type: application/json" \\
  -d '{"flightNumber":"QA123","seat":"14C","checkedBags":1}'

# {"args":{},"data":{"flightNumber":"QA123","seat":"14C","checkedBags":1},
# "files":{},"form":{},"headers":{"host":"postman-echo.com","user-agent":
# "curl/8.7.1","content-length":"53","content-type":"application/json",
# "accept":"*/*","x-forwarded-proto":"https","accept-encoding":"gzip, br"},
# "json":{"flightNumber":"QA123","seat":"14C","checkedBags":1},
# "url":"https://postman-echo.com/post"}

# The status-only pattern - useful when checking many endpoints in a loop,
# where reading a full JSON body every time would be noise:
curl -s -o /dev/null -w "status=%{http_code} time=%{time_total}s\\n" \\
  "https://postman-echo.com/status/404"
curl -s -o /dev/null -w "status=%{http_code} time=%{time_total}s\\n" \\
  "https://postman-echo.com/get"

# status=404 time=0.308386s
# status=200 time=0.305426s

# -o /dev/null throws the body away, -w prints exactly the fields requested.
# This is the shape a CI smoke-test script uses: dozens of curls, one line
# of output each, nobody reading a single response body by eye.
```

### Your first time: Your mission: build one curl command from scratch, four flags at a time

- [ ] Send a bare GET with no flags — curl https://postman-echo.com/get - confirm you get a JSON body back with zero setup.
- [ ] Add -i and re-run it — Read the status line and at least three response headers before you get to the body. Note the content-type - it tells you how to parse what follows.
- [ ] Break it on purpose: send the same POST without the Content-Type header — Compare the 'json' field in the response - many APIs will fail to parse the body as JSON without the header telling them to, even though the bytes sent were identical.

You built one request bottom-up instead of clicking through a GUI - which means when Postman (next note) shows you the same fields in a form, you'll recognize every one of them as something you already understand.

- **curl returns a JSON error about the body/content but you're sure you typed the JSON correctly.**
  Almost always shell quoting, not JSON syntax - your shell may be interpreting quotes, backslashes, or $ signs inside the -d string before curl ever sees it. Wrap the whole payload in single quotes on Mac/Linux (curl handles the JSON's own double quotes fine inside single quotes), and if the JSON itself contains an apostrophe, escape it as '\\'' - a genuinely ugly but standard shell trick.
- **The request hangs indefinitely with no response and no error.**
  Add --max-time 10 (or --connect-timeout 5) to every request by habit, the same rule this platform's Linux module teaches. A hung curl with no timeout is indistinguishable from 'still loading' until you kill it manually - a timeout turns silence into a clear, fast failure you can act on.
- **The response looks like a login page's HTML instead of the JSON you expected, but the request 'succeeded'.**
  Check the status code with -i first - a 200 with an HTML body is often an auth redirect the server sent instead of a real API response (the same Content-Type lie devtools work covers). curl follows no JavaScript and renders nothing, so it will show you this HTML exactly as-is rather than silently redirecting somewhere - read the body before assuming success.

### Where to check

- **`curl --help all` or `man curl`** — the full flag reference, always available locally, no browser required.
- **`https://postman-echo.com`** — Postman's free public echo API, purpose-built for exactly this kind of practice; every request you send gets reflected back so you can see precisely what left your machine.
- **[[api-testing-fundamentals/postman-and-curl/postman-requests]]** — the same four building blocks (URL, method, headers, body), now as fields in a GUI instead of flags in a terminal.
- **[[browser-devtools-mastery/network/copy-as-curl]]** — DevTools will generate a full curl command from any real browser request, which is often the fastest way to get a realistic starting point to edit.

### Worked example: turning a bug report into a curl command a developer can run in ten seconds

1. A bug report says "creating a flight booking with a past departure date doesn't return an error." Vague - no request shown, no response shown.
2. The tester reproduces it manually first, in Postman, to confirm the behavior, then translates the exact request into curl so it can be pasted into the ticket as text.
3. `curl -s -i -X POST https://api.taskflight.example/bookings -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"flightNumber":"QA123","departureDate":"2020-01-01"}'`
4. Response: `HTTP/2 201` with a body showing the booking created successfully - confirming the bug: a departure date four years in the past was silently accepted.
5. The `$TOKEN` placeholder (never a real token) keeps the command runnable in shape without leaking a live credential into the ticket - the developer supplies their own.
6. Filed with the exact command, the exact response, and one line: "expected 400 Bad Request for a past departureDate, got 201 Created - reproducible via the attached curl command in any environment." No screenshot, no "steps to reproduce" prose, no ambiguity about what request was actually sent.

**Quiz.** A tester runs `curl -X GET https://api.example.com/search -d '{ q: boots }'` (a JSON body) expecting a filtered GET request, but the server appears to ignore the search term entirely. What's the most likely explanation?

- [ ] GET requests are always cached, so the server is returning a stale cached response
- [x] The -d flag sends a request body, but many servers strip or ignore bodies on GET requests - the query term never actually reaches the server's search logic
- [ ] The JSON in -d is malformed and curl silently dropped it before sending
- [ ] curl requires --data-raw instead of -d for any request containing JSON

*This note explicitly flags this exact mistake: -d sends a request body, and while curl will happily attach a body to a GET request, plenty of real servers either strip the body from GET entirely or never look at it, because GET traditionally carries its parameters in the URL's query string, not the body. The fix is either switching to POST (if a body genuinely makes sense) or moving the search term into the URL as a query parameter (?q=boots), which is what [[api-testing-fundamentals/postman-and-curl/curl-basics]] means by 'question whether GET is even the right verb.' Caching isn't implicated here since nothing suggests a repeated identical request; the JSON is valid, so curl sends it as written; and -d vs --data-raw differ only in how they handle a leading @ or # character, not JSON validity - neither is the cause of a search term being ignored.*

- **curl's four building blocks** — URL (required), method (-X, defaults to GET or POST-if-data-present), headers (-H, repeatable), body (-d / --data). Every request is some combination of these four.
- **Why -i matters** — Prints the HTTP status line and all response headers before the body - without it you only see the body, and can easily mistake a 404-with-JSON-error-page for a successful response.
- **The -d-implies-POST trap** — Adding -d to a request with no explicit -X silently makes it a POST. Attaching -d to an explicit GET often gets the body ignored entirely by the server.
- **The reflex timeout flag** — --max-time 10 (or --connect-timeout) turns an indefinite hang into a fast, clear failure - add it by habit to every request while testing.
- **Why curl commands make good bug-report evidence** — One line of plain text, fully self-contained, pasteable and rerunnable by anyone with a terminal - no screenshot, no GUI state, no 'works on my machine' ambiguity about what was actually sent.

### Challenge

Pick any public JSON API you can call without authentication (postman-echo.com, or another free API of your choice). Build four curl commands from scratch: (1) a plain GET, (2) the same GET with -i and note which response header tells you the body format, (3) a POST with a JSON body and a Content-Type header, (4) a status-only check using -s -o /dev/null -w against an endpoint you expect to fail (try a wrong path for a 404). Paste all four commands and their real output.

### Ask the community

> I'm building a curl command for [describe the request - method, endpoint, headers, body] and getting [describe what's wrong - hang, wrong status, ignored body, quoting error]. Here's the exact command I'm running: [paste it]. What flag or quoting fix am I missing?

The most useful replies will ask to see the command exactly as typed (quoting bugs are invisible in a paraphrase) and will check whether -i was used to actually see the status/headers before diagnosing further - most "curl isn't working" reports turn out to be a 4xx/5xx the tester never looked at because -i was left off.

- [man curl — the complete, authoritative flag reference](https://curl.se/docs/manpage.html)
- [Postman — the Echo API (postman-echo.com) reference](https://learning.postman.com/docs/developer/echo-api/)

🎬 [RealClearComputing — Introduction to cURL Command: The Basics for Beginners](https://www.youtube.com/watch?v=4ByJae1MwUQ) (6 min)

- curl is the same four building blocks every HTTP tool uses under the hood: URL, method (-X), headers (-H), body (-d) - learning it makes every GUI tool, Postman included, instantly legible.
- Add -i by reflex - it shows the status line and headers, which is usually the difference between 'this looks fine' and catching a 404 or auth redirect disguised as a normal-looking body.
- -d silently implies POST, and attaching it to an explicit GET often gets the body ignored server-side entirely - if a request needs data, question whether GET is the right verb at all.
- postman-echo.com is a free, public, purpose-built endpoint for exactly this kind of practice - it reflects your request back at you so you can verify precisely what left your machine.
- A curl command is plain text: pasteable into a ticket, rerunnable by any developer with a terminal, and unambiguous about exactly what was sent - often better bug-report evidence than a screenshot.


## Related notes

- [[Notes/api-testing-fundamentals/postman-and-curl/postman-requests|Postman requests]]
- [[Notes/api-testing-fundamentals/postman-and-curl/postman-tests-and-variables|Postman tests & variables]]
- [[Notes/browser-devtools-mastery/network/copy-as-curl|copy-as-curl]]
- [[Notes/testers-toolbox/beyond-the-browser/debugging-proxies|Debugging proxies]]


---
_Source: `packages/curriculum/content/notes/api-testing-fundamentals/postman-and-curl/curl-basics.mdx`_
