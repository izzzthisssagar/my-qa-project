---
title: "HTTP in plain words"
tags: ["internet", "http", "api", "track-a"]
updated: "2026-07-10"
---

# HTTP in plain words

*The protocol behind every web page, in the only detail that matters: the verbs, the status codes, and the headers that decide whether your app is fast, secure, and honest.*

> HTTP has a reputation for being technical, which is odd, because it's the most
> human-readable thing in computing. It's plain text. It has **nine verbs** (you'll use
> four), a handful of **three-digit numbers** that mean exactly what they say, and some
> **notes clipped to the front**. That's it. People who "know HTTP" mostly just memorized
> what `409` means. Today, so do you.

> **In real life**
>
> HTTP is **the grammar of a very polite, very forgetful correspondent.** Each letter
> states a verb (what to do), a noun (what to do it to), and some context. The reply
> always opens with a number that tells you, before you read another word, whether it
> worked, whether it's your fault, or whether the recipient set their own house on fire.
> Nobody has to interpret tone. The number is the tone.

## The verbs (four you'll use daily)

| Verb | Means | Safe? | Idempotent? |
|---|---|---|---|
| `GET` | Give me this | Yes — changes nothing | Yes |
| `POST` | Here's something new | No | **No** — twice creates two |
| `PUT` | Replace this entirely | No | Yes — twice is same as once |
| `PATCH` | Change part of this | No | Usually |
| `DELETE` | Remove this | No | Yes |

Two words carry real weight. **Safe** means it changes nothing (only `GET`). ****Idempotent****: An operation you can repeat with the same result. DELETE is idempotent — deleting an already-deleted thing leaves it deleted. POST is not: sending it twice creates two records, which is exactly what a double-clicked Submit button does. means doing it twice is the same as
doing it once. `POST` fails that test, and that single fact is behind an entire genre of
duplicate-order bugs.

![Clients exchanging HTTP messages with a server](client-server.png)
*Diagram: client–server model — Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Client-server_model_example_(Web_browsing)_-_en.png)*
- **Every arrow carries a verb and a number** — Out: a method (GET/POST/PUT/DELETE). Back: a status code. Those two values summarize the entire exchange before you read a byte of the body — which is why experienced testers scan the Network panel's Method and Status columns and nothing else.
- **The client picks the verb — and can pick wrongly** — Nothing physically stops a front-end from using GET to delete something. HTTP is a convention, not a police force. When an app violates the convention, crawlers and caches punish it, because they trust the convention absolutely.
- **The server picks the number — and can pick wrongly too** — Returning 200 with an error message in the body is depressingly common, and it breaks every automated retry, monitor and alert that reads status codes. That's a real bug: 'endpoint returns 200 on failure'. It hides outages.
- **Headers ride on every message** — Caching rules, content type, authentication, compression. Invisible in the UI, decisive for performance and security. Half of what makes a site fast or safe is decided by text nobody ever looks at.
- **Stateless: each arrow stands alone** — The server links this request to your last one only via a cookie or token you re-attached. Nothing else connects them. Every message is complete, self-contained, and instantly forgotten.

**Reading status codes like a triage nurse — press Play**

1. **2xx — it worked** — 200 OK (here's your thing), 201 Created (I made it, here's where it lives), 204 No Content (done, nothing to say). If you see 2xx and the UI still looks wrong, stop blaming the backend: the bug is in the browser.
2. **3xx — look somewhere else** — 301 (moved permanently — update your links), 302 (temporarily over here), 304 (Not Modified: 'you already have this, use your cache'). 304s are free speed, and a page issuing zero of them is re-downloading things it already owns.
3. **4xx — YOU sent something wrong** — 400 (malformed), 401 (who are you?), 403 (I know who you are, and no), 404 (no such thing), 409 (conflict — it already exists), 429 (slow down, too many requests). The client is at fault, and the response body usually says exactly how.
4. **5xx — the SERVER broke** — 500 (unhandled crash), 502/504 (a machine behind the machine didn't answer), 503 (overloaded or down for maintenance). Never the front-end's fault. Capture the request, hand it to the backend, and file it with the response body.
5. **🎯 The triage** — First digit, three seconds, right team. 4 means the request was wrong; 5 means the server was wrong; 2 with a broken screen means the client was wrong. This is the fastest useful skill in web testing, and it fits on a business card.

*Try it — the same action, four verbs, four very different consequences*

```python
db = {1042: {"item": "keyboard", "qty": 2}}
next_id = 1043

def handle(method, path, body=None):
    global next_id
    parts = path.strip("/").split("/")           # e.g. ['orders', '1042']
    oid = int(parts[1]) if len(parts) > 1 else None

    if method == "GET":
        return (200, db[oid]) if oid in db else (404, {"error": "no such order"})
    if method == "POST":                          # NOT idempotent — creates every time
        db[next_id] = body; next_id += 1
        return (201, {"id": next_id - 1})
    if method == "PUT":                           # idempotent — same result if repeated
        db[oid] = body
        return (200, db[oid])
    if method == "DELETE":                        # idempotent — gone stays gone
        existed = db.pop(oid, None)
        return (204, None) if existed else (404, {"error": "already gone"})

print("GET  /orders/1042 ->", handle("GET", "/orders/1042"))
print("GET  /orders/9999 ->", handle("GET", "/orders/9999"))
print()

print("Double-clicking Submit (POST twice):")
print("  ", handle("POST", "/orders", {"item": "mouse", "qty": 1}))
print("  ", handle("POST", "/orders", {"item": "mouse", "qty": 1}))
print("   db now holds:", list(db.keys()), "<- TWO mice. The user clicked once, in their mind.")
print()

print("Retrying a PUT twice (safe):")
print("  ", handle("PUT", "/orders/1042", {"item": "keyboard", "qty": 5}))
print("  ", handle("PUT", "/orders/1042", {"item": "keyboard", "qty": 5}))
print("   qty is still 5. Idempotent. Retry all you like.")
print()
print("DELETE twice:", handle("DELETE", "/orders/1042"), handle("DELETE", "/orders/1042"))
print("Second one 404s — but the WORLD is in the same state. That's idempotence.")
```

## Headers: the invisible half of the web

Nobody looks at headers, and headers decide almost everything:

- **`Cache-Control`** — may the browser reuse this? For how long? Get it wrong and users see yesterday's app for a week, or your server serves the same file ten million times.
- **`Content-Type`** — is this JSON, HTML, or an image? Mislabel it and the browser will misinterpret it, occasionally dangerously.
- **`Authorization` / `Cookie`** — who you are, on every single letter.
- **`Set-Cookie`** with `HttpOnly`, `Secure`, `SameSite` — three flags that decide whether a stolen script can read your session. A session cookie without `HttpOnly` is a finding, not a preference.
- **`Content-Encoding: gzip`** — the response is compressed. Its absence on a large text response is free performance, left on the table.

> **Tip**
>
> The most valuable status code to hunt for: **200 on failure.** An API that returns
> `200 OK` with `{"success": false}` in the body has lied to every monitor, retry, alert
> and cache in the system — all of which read the number, not the prose. Outages go
> undetected because dashboards show green. When you find one, file it: *"POST /api/x
> returns 200 with an error body; should be 4xx/5xx so failures are observable."* That
> sentence, in a bug report, reads like it was written by someone with ten years of
> experience. It was written by someone who read this note.

### Your first time: Your mission: read the numbers

- [ ] Collect a 2xx, a 3xx and a 4xx — Open any big site with the Network panel open and browse. Within a minute you'll have all three, including a 404 you never noticed because the page looked fine.
- [ ] Force a 404 on purpose — Add nonsense to a URL: `site.com/this-page-does-not-exist`. Look at the status in the Network panel. Notice the pretty error page arrives WITH a 404 — the page and the number are separate things, and a pretty page with a 200 would be a bug.
- [ ] Force a 401 — Delete your session cookie (Application → Storage), then click something that needs auth. There it is. The server correctly refused an anonymous letter.
- [ ] Find a 304 — Load a page, then reload it normally (not a hard reload). Look for 304 Not Modified, or 'from disk cache' in the Size column. That's the browser being told 'you already have this'. Free speed, invisible.
- [ ] Inspect one Set-Cookie header — Log in somewhere and find the login response's headers. Does the session cookie have HttpOnly? Secure? SameSite? If not, you've found something worth reporting.

Five status codes, one cookie audit. You can now read the web's grammar at a glance.

- **Users see an old version of the app after a deploy.**
  Caching headers. The browser was told (by `Cache-Control`) that the old JavaScript file was fresh, so it never asked for the new one. Fix belongs on the server: use content-hashed filenames so a new deploy has new URLs, and set long caches only on files whose names change. Telling users to hard reload is a workaround for a deploy defect, and it does not scale to a million people.
- **Submitting a form twice creates two orders.**
  POST is not idempotent — two POSTs mean two records, and HTTP is behaving exactly as specified. The fix has two halves: disable the button after the first click (client), and accept an idempotency key so a repeated request returns the FIRST result instead of creating a second (server). Report both halves; the client fix alone fails on flaky networks where the browser retries automatically.
- **429 Too Many Requests during my test run.**
  Rate limiting, and it's the server behaving correctly. Note the `Retry-After` header — it tells you exactly how long to wait, and a well-built client reads it rather than hammering blindly. Also remember (chapter 1) that rate limits key on your public IP, so your whole office shares one budget. Your load test just throttled your colleagues.

### Where to check

Reading HTTP where it lives:

- **Network → Method + Status columns** — scan these two before anything else. They triage the whole page in seconds.
- **Response headers** — `Cache-Control`, `Content-Type`, `Content-Encoding`, `Set-Cookie`. The invisible half of performance and security.
- **Request headers** — `Authorization`, `Cookie`, `Content-Type`. What the client actually claimed.
- **`curl -i https://example.com`** — the raw response, headers and all, with no browser to interpret it. `-I` for headers only. This is how you check a server's behaviour without any front-end in the way.
- **The Retry-After / Cache-Control values** — servers frequently tell you exactly what to do, in a header nobody reads.

Tester's habit: **scan status codes before reading anything else.** A page with four
404s and a 500 hiding behind a normal-looking UI is a page with four bugs and an
incident, and none of them are visible to a user — or to a tester who only looks at
the screen.

### Worked example: the green dashboard hiding a broken checkout

An outage that lasted three weeks because of one number.

1. **The monitoring dashboard is green.** Uptime 99.99%. Error rate 0.01%. Everyone is pleased with themselves.
2. **Meanwhile, support tickets:** customers say checkout "does nothing." Not many. Enough.
3. **A tester reproduces it** with the Network panel open. `POST /api/checkout` → **200 OK**. Green. Success. And the response body reads: `{"success": false, "error": "payment gateway timeout"}`.
4. **The mechanism, now obvious.** The monitoring system counts non-2xx responses as errors. Every failed checkout returned `200`. So every failure was recorded as a success. The dashboard was not wrong about what it measured; it measured a lie.
5. **The retry logic made it worse.** The client's retry code also keys on status codes — so it never retried a "successful" failure. And the CDN happily cached some of those 200 responses, serving stored failures to new users.
6. **The report:** '`POST /api/checkout` returns 200 with `{"success": false}` on payment failure. Should return 502 (upstream gateway timeout). Impact: failures invisible to monitoring, retries never trigger, responses cacheable. Evidence: [request + response body + dashboard screenshot showing green].'
7. **One number, three broken systems.** Status codes are not decoration — they are the contract that every automated system in the stack depends on. A tester who reads them finds outages that dashboards were built to miss.

> **Common mistake**
>
> Treating status codes as cosmetic — "the body says what happened, who cares about the
> number?" Every automated system in the stack cares, and only about the number: monitors
> count non-2xx to page an engineer; retry logic re-sends on 5xx and gives up on 4xx;
> caches store 200s and skip 500s; load balancers pull a machine out of rotation on
> repeated 503s. A `200 OK` wrapping an error is not a stylistic choice, it's a
> misinformation campaign against your own infrastructure. Testers who understand this
> find outages that dashboards, by construction, cannot see.

**Quiz.** An endpoint returns `200 OK` with a body saying success is false and the error is a gateway timeout, whenever payment fails. Why is this a serious bug and not a style choice?

- [ ] It isn't — the body clearly explains the failure
- [x] Every automated system reads the status code, not the body: monitors count non-2xx to detect outages, retry logic triggers on 5xx, caches store 200s. A 200-on-failure makes real failures invisible to monitoring, unretried, and cacheable.
- [ ] Because 200 is reserved for GET requests only
- [ ] Because the error message should be in a header

*Humans read bodies; machines read numbers. Returning 200 for a failure tells every monitor that nothing is wrong, tells retry logic there's nothing to retry, and permits caches and CDNs to store and re-serve the failure. The dashboard stays green while checkout burns. That's why 'endpoint returns 200 on failure' is one of the highest-value bug reports a tester can write — it fixes not one bug but the entire system's ability to notice bugs.*

- **Status code first digits** — 2xx worked · 3xx look elsewhere · 4xx your request was wrong · 5xx the server broke. Triage in three seconds.
- **Safe vs idempotent** — Safe = changes nothing (only GET). Idempotent = twice is the same as once (GET, PUT, DELETE). POST is neither — hence duplicate orders on double-click.
- **Codes worth memorizing** — 201 created · 304 not modified (free speed) · 401 who are you · 403 no · 404 no such thing · 409 conflict · 429 slow down · 500 crash · 502/504 upstream · 503 overloaded.
- **200 on failure** — A serious bug: monitors, retries and caches all read the number, not the body. Failures become invisible, unretried and cacheable.
- **The headers that matter** — Cache-Control (stale apps after deploy), Content-Type, Authorization/Cookie, Set-Cookie flags (HttpOnly, Secure, SameSite), Content-Encoding: gzip.
- **State-changing GET** — Caches, crawlers and prefetchers fetch GETs unbidden. `GET /orders/1042/delete` will eventually be triggered by a robot. Real, reportable, famous.

### Challenge

Browse any large website with DevTools → Network open, and collect one of each: a 2xx,
a 3xx, a 4xx. (You'll find a 404 on a site that looks perfectly healthy — most do.)
Then find one login response and audit its `Set-Cookie` flags for `HttpOnly`, `Secure`
and `SameSite`. Write down what's missing. In ten minutes you've performed a status-code
survey and a cookie security audit, using a tool that has shipped in every browser for
fifteen years.

### Ask the community

> HTTP question: `[METHOD] [url]` returns `[status]`. Response body: [paste]. Response headers: [Cache-Control? Content-Type? Set-Cookie flags?]. Expected: [status you'd expect and why]. Same request via curl -i: [paste].

Including the curl output takes the browser out of the picture entirely — if curl sees
the same thing, it's the server; if only the browser fails, it's CORS, cookies or cache.
That single comparison splits the search space in half before anyone answers.

- [MDN — every status code, with when to use it](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [MDN — HTTP headers, the invisible half](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
- [HTTP verbs, codes and headers](https://www.youtube.com/watch?v=L5BlpPU_muY)

🎬 [HTTP, plainly](https://www.youtube.com/watch?v=L5BlpPU_muY) (10 min)

- Four verbs cover the daily web: GET (safe, changes nothing), POST (creates, not idempotent), PUT/PATCH (update), DELETE (idempotent).
- The status code's first digit triages any bug in three seconds: 4xx the request was wrong, 5xx the server broke, 2xx with a broken screen means the client.
- Returning 200 on failure blinds monitors, disables retries and lets caches store errors. It's one of the highest-value bugs a tester can report.
- Headers decide performance and security invisibly: Cache-Control, Content-Type, and the Set-Cookie flags HttpOnly, Secure and SameSite.
- POST is not idempotent, which is exactly why a double-clicked Submit creates two orders — and why the fix needs both a disabled button and a server-side idempotency key.


---
_Source: `packages/curriculum/content/notes/the-internet-and-the-web/client-server-and-http/http-in-plain-words.mdx`_
