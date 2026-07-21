---
title: "Request & response anatomy"
tags: ["api-testing-fundamentals", "http-for-testers", "track-c"]
updated: "2026-07-17"
---

# Request & response anatomy

*Every API call is one request and one response, each built from three parts - a start line, headers, and an optional body. Learn to read both halves cold, straight off a curl invocation, before touching Postman or a framework.*

> 2026 QA hiring finally caught up to reality: manual API testing - reading raw requests and
> responses, driving them by hand with curl and Postman - now shows up in the first few months of
> every serious QA roadmap, not as an "automation prerequisite" bolted on at the end. And it starts
> here, with the single most useful skill in this whole module: looking at a request or a response
> and reading it like a sentence instead of a wall of symbols. Every HTTP message ever sent, no
> matter how fancy the framework wrapping it, breaks down into exactly three parts. Once you can
> name those three parts on sight, "the API is broken" stops being a vibe and starts being a specific,
> pointable-at line.

> **In real life**
>
> Two people with matching handheld radios. One keys the mic and speaks: a specific message, spoken
> in a specific way, into a specific channel - that's the **request**. The other releases their own
> key and speaks back - the **response**. Neither radio does anything useful alone; the exchange only
> works because both units are built to the same standard, understand the same button layout, and
> take turns. HTTP is the same deal at the software layer: a client keys up with a request, a server
> replies with a response, and the entire "conversation" is just that one request/response pair,
> repeated as many times as the app needs.

**Request/response anatomy**: An HTTP request/response pair is the fundamental unit of exchange on the web: a request sent by a client (start line + headers + optional body) and the response sent back by a server (status line + headers + optional body). The start line differs by direction - a request's start line is METHOD, target (path + query string), and HTTP version, e.g. 'GET /flights?from=DEL&to=BOM HTTP/1.1'; a response's start line (often called the status line) is HTTP version, status code, and reason phrase, e.g. 'HTTP/1.1 200 OK'. Everything below the start line, up to a blank line, is headers - metadata about the message. Everything after that blank line, if anything, is the body - the actual payload.

## The three parts, in order, every single time

- **Start line** — first line only. For a request: method + target + version. For a response:
  version + status code + reason phrase. This is the one line you should be able to read in under
  a second: what was asked for, or what happened.
- **Headers** — every line after the start line, one `Name: value` pair per line, until a blank
  line. Metadata *about* the message: what format the body is in, who's asking, how big the body
  is, when this was sent. The headers-and-bodies note in this chapter goes deep on these.
- **Body** — everything after that blank line. Optional - a `GET` almost never has one, a `POST`
  creating a new record usually does. When present, its shape (JSON, XML, plain text) is announced
  by the `Content-Type` header, not guessed.
- **The blank line is not decoration.** It's the one character sequence (`\r\n\r\n`) that formally
  separates "metadata about this message" from "the message's actual content." A tool that gets
  this boundary wrong is a tool worth filing a bug against.

> **Tip**
>
> When a request looks broken and you can't tell why, name the three parts out loud first: "start
> line says GET to this URL. Headers say Accept: JSON, Authorization: Bearer something. Body: empty."
> Half of "this API call is weird" bugs turn out to be one specific part being wrong - a body sent on
> a GET, a missing Content-Type, a status line that doesn't match the body it's attached to - and you
> only spot the mismatch once you're checking the three parts individually instead of squinting at
> the whole thing.

> **Common mistake**
>
> Treating "the request" and "the response" as one blob you either "worked" or "didn't." A tester who
> says "the API call failed" without saying which of the six pieces (request start line, request
> headers, request body, response start line, response headers, response body) actually shows the
> problem hasn't finished investigating yet - they've just noticed something's wrong.

![Two identical black handheld two-way radios standing side by side on a wooden table, both with antennas raised and matching keypads and small screens](request-and-response-anatomy.jpg)
*Retevis RT87 handheld radios — Wikimedia Commons, CC BY-SA 4.0 (FederalElection). [Source](https://commons.wikimedia.org/wiki/File:Retevis_RT87_handheld_radios.jpg)*
- **The left radio, keying up — the request** — One specific message, sent once: a method, a target, headers, maybe a body. In HTTP terms, this is the client sending exactly one request and then waiting.
- **The right radio, replying — the response** — Same three-part shape as the request (start line, headers, optional body), just travelling the other direction: a status line instead of a request line, and the actual payload the client asked for.
- **Matching antennas, matching keypads — the shared protocol** — Neither radio is special; they work because both sides speak the identical format. That shared format is HTTP itself - the same three-part shape on both legs is exactly what lets any client talk to any compliant server.

**One request/response pair, start to finish - press Play**

1. **Client builds a request** — Method (GET), target (/flights?from=DEL&to=BOM), version (HTTP/1.1) on the start line; headers describing the client and what it wants back; body only if the method needs one.
2. **Request travels to the server** — The exact bytes above, sent over a TCP connection (usually wrapped in TLS for https). Nothing is added or reinterpreted in transit - what the client wrote is what the server reads.
3. **Server reads the start line first** — Method + target tell the server WHAT is being asked before it even looks at headers - this is why a wrong method on an otherwise-perfect request still fails immediately.
4. **Server builds a response** — Status line (version + code + reason) summarizing the outcome, headers describing the reply, body carrying the actual data - or nothing, for a 204 No Content.
5. **Client reads the response the same way** — Start line first (did it work?), then headers (what format is the body in?), then the body itself - the identical three-part reading habit, just applied to the other half of the exchange.

A real request and response, byte for byte, is worth seeing before anything gets abstracted away -
here's one live round trip, captured with `-i` so both the status line and every header print:

*Run it - one real request/response pair, unabridged (curl)*

```bash
curl -i -m 10 "https://httpbin.org/get?tester=qa-mastery"

# HTTP/2 200
# date: Thu, 17 Jul 2026 09:00:00 GMT
# content-type: application/json
# content-length: 303
# server: gunicorn/19.9.0
# access-control-allow-origin: *
# access-control-allow-credentials: true
#
# {
#   "args": {
#     "tester": "qa-mastery"
#   },
#   "headers": {
#     "Accept": "*/*",
#     "Host": "httpbin.org",
#     "User-Agent": "curl/8.7.1",
#     "X-Amzn-Trace-Id": "Root=1-6a595063-4e9e54e4735ed3f0220c7bd9"
#   },
#   "origin": "103.98.129.204",
#   "url": "https://httpbin.org/get?tester=qa-mastery"
# }
#
# Read the REQUEST half first, from what curl sent (not printed above, but it's
# "GET /get?tester=qa-mastery HTTP/2" plus the Accept/Host/User-Agent headers
# httpbin echoes back under "headers" - the server is literally showing you
# your own request back). Now the RESPONSE half: start line is "HTTP/2 200" -
# version + status, no separate reason phrase under HTTP/2. Everything from
# "date:" to "access-control-allow-credentials:" is response headers. The
# blank line. Then the body: a JSON object, exactly matching what
# content-type: application/json promised.
```

Same three-part reading, done in code instead of by eye - split a raw request on the blank line and
name each piece:

*Run it - parsing a raw HTTP request into its three parts (Python)*

```python
raw_request = (
    "GET /flights?from=DEL&to=BOM HTTP/1.1\\r\\n"
    "Host: api.taskflight.example\\r\\n"
    "Accept: application/json\\r\\n"
    "Authorization: Bearer demo-token-123\\r\\n"
    "\\r\\n"
)

def parse_request(raw):
    head, _, body = raw.partition("\\r\\n\\r\\n")
    lines = head.split("\\r\\n")
    request_line = lines[0]
    method, target, version = request_line.split(" ")
    headers = {}
    for line in lines[1:]:
        if not line:
            continue
        name, _, value = line.partition(": ")
        headers[name] = value
    return {
        "method": method,
        "target": target,
        "version": version,
        "headers": headers,
        "body": body,
    }

parsed = parse_request(raw_request)
print("=== Request line ===")
print(f"  method:  {parsed['method']}")
print(f"  target:  {parsed['target']}")
print(f"  version: {parsed['version']}")
print("=== Headers ===")
for name, value in parsed["headers"].items():
    print(f"  {name}: {value}")
print("=== Body ===")
print(f"  {parsed['body'] or '(empty - GET requests usually carry no body)'}")

# === Request line ===
#   method:  GET
#   target:  /flights?from=DEL&to=BOM
#   version: HTTP/1.1
# === Headers ===
#   Host: api.taskflight.example
#   Accept: application/json
#   Authorization: Bearer demo-token-123
# === Body ===
#   (empty - GET requests usually carry no body)
```

Same idea, the other direction - parsing a raw response into status line, headers, and body:

*Run it - parsing a raw HTTP response into its three parts (Java)*

```java
import java.util.*;

public class Main {
    static String rawResponse =
        "HTTP/1.1 200 OK\\r\\n" +
        "Content-Type: application/json\\r\\n" +
        "Content-Length: 41\\r\\n" +
        "Date: Fri, 17 Jul 2026 09:00:00 GMT\\r\\n" +
        "\\r\\n" +
        "{\\"flightId\\":\\"AI202\\",\\"status\\":\\"ON_TIME\\"}";

    record ParsedResponse(String version, int statusCode, String reason, Map<String, String> headers, String body) {}

    static ParsedResponse parseResponse(String raw) {
        String[] parts = raw.split("\\r\\n\\r\\n", 2);
        String head = parts[0];
        String body = parts.length > 1 ? parts[1] : "";
        String[] lines = head.split("\\r\\n");
        String[] statusLine = lines[0].split(" ", 3);
        String version = statusLine[0];
        int statusCode = Integer.parseInt(statusLine[1]);
        String reason = statusLine[2];

        Map<String, String> headers = new LinkedHashMap<>();
        for (int i = 1; i < lines.length; i++) {
            String[] kv = lines[i].split(": ", 2);
            headers.put(kv[0], kv[1]);
        }
        return new ParsedResponse(version, statusCode, reason, headers, body);
    }

    public static void main(String[] args) {
        ParsedResponse parsed = parseResponse(rawResponse);
        System.out.println("=== Status line ===");
        System.out.println("  version: " + parsed.version());
        System.out.println("  status:  " + parsed.statusCode());
        System.out.println("  reason:  " + parsed.reason());
        System.out.println("=== Headers ===");
        for (Map.Entry<String, String> e : parsed.headers().entrySet()) {
            System.out.println("  " + e.getKey() + ": " + e.getValue());
        }
        System.out.println("=== Body ===");
        System.out.println("  " + parsed.body());
    }
}

// === Status line ===
//   version: HTTP/1.1
//   status:  200
//   reason:  OK
// === Headers ===
//   Content-Type: application/json
//   Content-Length: 41
//   Date: Fri, 17 Jul 2026 09:00:00 GMT
// === Body ===
//   {"flightId":"AI202","status":"ON_TIME"}
```

### Your first time: Your mission: read a real request/response pair cold

- [ ] Run the curl playground above yourself (or any GET against a public API) — Add -i so the response's start line and headers print, not just the body.
- [ ] Before reading further, write down the response's three parts from memory — Status line (version + code), the header names (not values yet), then where the body starts.
- [ ] Now do the same for the request you sent — curl -v shows what it actually sent, prefixed with '>' - find the request's own start line and headers in that output.
- [ ] Find one header that only makes sense on the response, and one that only makes sense on the request — E.g. content-length describes the message it's attached to either way, but Host only ever appears on a request, and Date's authorship is the server's, not the client's.
- [ ] Say the verdict sentence out loud — 'Request: GET to [target], asking for [Accept type]. Response: [status], body is [format], [size] bytes.' That sentence is the whole skill, compressed.

You've read a live request/response pair by naming its parts instead of eyeballing the whole thing -
the exact habit every other note in this module builds on.

- **A response has a status line, headers, and what looks like a body - but the body is empty even though Content-Length says 41.**
  Check for truncation in transit (a proxy, a tool's buffer, a copy-paste that lost trailing bytes) or a genuine server bug writing the wrong Content-Length. Re-run with curl -i directly against the server (bypassing any intermediary) to see the untouched bytes - if curl also shows a mismatch, it's server-side; if curl looks fine, something between you and curl's output is the culprit.
- **A tool (Postman, a browser extension) shows headers in a different order than curl did for the identical request.**
  Header ORDER is rarely meaningful in HTTP (unlike header VALUES) - most clients and intermediaries are free to reorder them, and most servers don't care. Don't file a bug on order alone; check whether any specific header's presence or value actually differs, which is the thing that can legitimately break something.
- **You're staring at a raw request/response dump and can't find the blank line that's supposed to separate headers from body.**
  Some tools render the blank line invisibly, or collapse it entirely in a pretty-printed view. Switch to a raw/source view (curl -i, a Network panel's 'raw' toggle, or a text export) - the blank line (an empty line, not just short) is structurally required by HTTP, so if you truly can't find one, you're looking at a tool's summary, not the actual message.

### Where to check

- **`curl -i` (or `-v` for the request side too)** — the least-abstracted view of both halves; nothing between you and the actual bytes.
- **Your browser's Network panel** — see [[browser-devtools-mastery/network/anatomy-of-a-request]] for the panel-specific reading skill this note's raw-text version feeds into.
- **Postman's response viewer's "Raw" tab** — most tools default to a pretty/formatted view that hides exactly where headers end and body begins; the raw tab restores it.
- **BuggyAPI (TaskFlight)** — this platform's own practice REST API is the natural place to run every curl command in this note against a real, live target instead of a public sandbox.

### Worked example: diagnosing a 'the API returns nothing' report using just the three parts

1. A report says: "calling the flight-status endpoint returns nothing." Vague - "nothing" could mean
   an empty body, an error, or a request that never even left the client.
2. Run it with `curl -i` against the real endpoint. First check: did a response come back at all, or
   did the connection just hang? A response arrived - good, narrows it to something in the three parts.
3. Read the start line: `HTTP/1.1 200 OK`. Not an error - so "nothing" isn't a status-code problem.
4. Read the headers: `Content-Length: 0`. There it is - the server itself is reporting a zero-length
   body. This isn't a tool failing to display something; the body genuinely is empty.
5. Compare against the request that was sent: the `Accept` header was missing entirely. Re-run with
   `Accept: application/json` added.
6. New response: `Content-Length: 187`, body full of flight data. Root cause found by walking the
   three parts in order (start line, then headers, then body) on BOTH the request and the response,
   rather than guessing from the vague "returns nothing" description.

**Quiz.** A tester runs `curl -i` against an endpoint and sees a response start with `HTTP/1.1 204 No Content`, followed by a few headers, followed immediately by the next shell prompt - no blank-line-then-body section visible at all. What's the correct read of this?

- [ ] The response is broken - every HTTP response must include a body, so this is a bug
- [x] This is expected: a body is optional, and a 204 status specifically means 'succeeded, and there is no body' - the missing body IS the correct behavior, not evidence of a tool problem
- [ ] The tool (curl) failed to display the body, and a different tool should be used
- [ ] The blank line separating headers from body is missing, which is itself the bug

*This note is explicit that the body is the one optional part of the three - present when there's a payload to carry, absent when there isn't. 204 No Content is HTTP's own way of saying 'this succeeded, and there is intentionally nothing to send back' (a DELETE that removed a resource is a classic case) - so a 204 response having no body is correct, expected behavior, not a defect. Option one is simply wrong about HTTP's rules. Option three misdiagnoses a display issue where there isn't one - curl shows exactly what came over the wire. Option four confuses 'no body' with 'malformed message' - the blank line still exists structurally in a 204 response (it just precedes zero bytes of body), and its presence or absence isn't what a tester would actually be able to distinguish from curl's rendering in this scenario anyway. The status-code-families note ([[api-testing-fundamentals/status-codes-and-rest/status-code-families]]) covers 204 and its 2xx siblings in more depth.*

- **The three parts of every HTTP message** — Start line (first line only), headers (Name: value pairs until a blank line), and an optional body (everything after the blank line).
- **Request start line vs response start line** — Request: METHOD + target + version (e.g. 'GET /flights HTTP/1.1'). Response: version + status code + reason phrase (e.g. 'HTTP/1.1 200 OK') - often called the status line.
- **What formally separates headers from body** — A single blank line (the byte sequence \\r\
\\r\
) - structurally required, not optional formatting.
- **Which part is genuinely optional** — The body. GET requests almost never have one; many responses (204 No Content, some redirects) don't either. Start line and headers are always present.
- **The fastest debugging habit this note teaches** — Say the three parts out loud for both halves: 'Request: [method] to [target], headers say [X]. Response: [status], body is [format].' Most 'the API is weird' reports resolve once you name which specific part is actually wrong.

### Challenge

Pick any public GET endpoint (httpbin.org/get is a safe default, or BuggyAPI if you have access).
Run it with `curl -i -v` so both the request and response print. Write out, in your own words, the
three parts of EACH half - six labeled pieces total (request start line, request headers, request
body; response start line, response headers, response body). Then deliberately change one header in
your request (try removing `Accept` or adding a bogus `Content-Type` to a GET) and note which of the
six pieces changes as a result on the response side.

### Ask the community

> I ran `[method]` against `[endpoint]` and got a response starting with `[status line]`. Walking through the three parts, here's what I found: headers = `[list]`, body = `[shape/empty]`. Does this response's structure look correct for what I asked for, or is something in the three parts off?

The most useful replies will point at ONE specific part (not "looks fine" or "looks broken" as a
whole) - e.g. "that Content-Type doesn't match what's actually in the body" is far more actionable
than a general reaction to the whole response.

- [MDN — HTTP Messages (request/response structure)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages)
- [httpbin.org — a free, public sandbox for practicing exactly this note's exercises](https://httpbin.org/)
- [The TechCave — The Http and the Web | Http Explained | Request-Response Cycle](https://www.youtube.com/watch?v=eesqK59rhGA)

🎬 [The TechCave — The Http and the Web | Http Explained | Request-Response Cycle](https://www.youtube.com/watch?v=eesqK59rhGA) (9 min)

- Every HTTP message, request or response, breaks down into exactly three parts: a start line, headers, and an optional body.
- A request's start line is method + target + version; a response's start line (the status line) is version + status code + reason phrase.
- A single blank line formally separates headers from body - it's structural, not visual formatting, and a tool that mishandles it is buggy.
- The body is the one truly optional part - many valid responses (204 No Content especially) have none, and that's correct, not broken.
- The fastest debugging habit in this whole module: name the three parts out loud for both the request and the response before deciding anything is actually wrong.


## Related notes

- [[Notes/browser-devtools-mastery/network/anatomy-of-a-request|anatomy-of-a-request]]
- [[Notes/browser-devtools-mastery/network/copy-as-curl|copy-as-curl]]
- [[Notes/api-testing-fundamentals/http-for-testers/headers-and-bodies|Headers & bodies]]


---
_Source: `packages/curriculum/content/notes/api-testing-fundamentals/http-for-testers/request-and-response-anatomy.mdx`_
