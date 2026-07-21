---
title: "Sessions & authentication"
tags: ["api-test-automation", "python-api-testing", "track-d"]
updated: "2026-07-17"
---

# Sessions & authentication

*Requests Sessions persist cookies and defaults and reuse connections; configure authentication deliberately, close sessions, and prove refusal paths without donating secrets to logs.*

> A Session is a reusable client, not a communal junk drawer. Persist the headers and cookies every request needs; keep the one dangerous override visible at the call site.

> **In real life**
>
> A passport carries identity evidence across checkpoints, while each entry stamp belongs to one crossing. A Session carries shared headers, auth, cookies, and connection pooling; method arguments describe one request.

**Session**: A Requests Session persists selected parameters and cookies across its requests and uses urllib3 connection pooling. Method-level dictionary values merge with session defaults and override matching keys for that request without automatically persisting the override.

## Configure shared state, then close it

```python
with requests.Session() as session:
    session.headers.update({"Accept": "application/json"})
    session.headers.update({"Authorization": f"Bearer {token}"})
    response = session.get(f"{base_url}/v1/me", timeout=5)
    assert response.status_code == 200
```

Basic auth can use `auth=(user, password)` or `HTTPBasicAuth`. Requests may also read Basic
credentials from `netrc` when no auth argument is supplied; set `session.trust_env = False` when a
hermetic test must ignore environment credentials and proxies.

> **Tip**
>
> Use a context manager or fixture teardown so the Session closes even after an assertion failure.

> **Common mistake**
>
> Assuming a method-level cookie or header update persists forever. Session dictionaries merge with request values, but request-only values do not become new Session defaults.

![Passport pages containing multiple international entry stamps](sessions-and-auth.jpg)
*Passport stamps acquired on this trip — mroach, Wikimedia Commons, CC BY-SA 2.0. [Source](https://commons.wikimedia.org/wiki/File:Passport_stamps_acquired_on_this_trip.jpg)*
- **Session identity** — Shared auth, cookies, and headers travel across requests.
- **One request** — A method-level override belongs to one checkpoint.
- **Server decision** — Each crossing still grants or refuses the requested action.

**Use a Session without leaking state**

1. **Create Session** — Connection pooling and cookie persistence begin.
2. **Apply safe defaults** — Base headers and documented auth are configured.
3. **Send scoped requests** — Method-level values override defaults for one call.
4. **Test refusal** — A separate client omits or changes credentials deliberately.
5. **Close Session** — Context manager or fixture teardown releases resources.

*Run it — session defaults and request overrides (Python)*

```python
session_headers = {"Accept": "application/json", "X-Role": "reader"}
request_headers = {**session_headers, "X-Role": "admin", "X-Trace": "case-7"}
print("request role:", request_headers["X-Role"])
print("request trace:", request_headers["X-Trace"])
print("session role after request:", session_headers["X-Role"])
print("trace persisted:", "X-Trace" in session_headers)

# request role: admin
# request trace: case-7
# session role after request: reader
# trace persisted: False
```

*Run it — session defaults and request overrides (Java)*

```java
import java.util.*;
public class Main {
  public static void main(String[] args) {
    Map<String,String> defaults = new LinkedHashMap<>();
    defaults.put("Accept", "application/json"); defaults.put("X-Role", "reader");
    Map<String,String> request = new LinkedHashMap<>(defaults);
    request.put("X-Role", "admin"); request.put("X-Trace", "case-7");
    System.out.println("request role: " + request.get("X-Role"));
    System.out.println("request trace: " + request.get("X-Trace"));
    System.out.println("session role after request: " + defaults.get("X-Role"));
    System.out.println("trace persisted: " + defaults.containsKey("X-Trace"));
  }
}

/* request role: admin
   request trace: case-7
   session role after request: reader
   trace persisted: false */
```

### Your first time: Your mission: build a scoped authenticated client

- [ ] Create a Session fixture with Accept and User-Agent defaults — Close it after yield.
- [ ] Load a test token outside source control — Fail safely if absent and never print the value.
- [ ] Prove two requests share intended defaults — Check behavior, not only internal dictionaries.
- [ ] Use a separate unauthenticated client for refusal — Avoid mutating a shared Session in a way that contaminates later tests.

- **Unexpected Basic auth appears in a hermetic test.**
  Check netrc behavior and set trust_env=False if environment credentials must be ignored.
- **A cookie leaks between tests.**
  Reduce fixture scope, clear the cookie jar, or create a fresh Session per test identity.
- **Connections are not reused during streaming.**
  Read the full response body or close it so the connection can return to the pool.

### Where to check

- `response.request.headers` after redaction for what was actually sent.
- Session headers, auth, and cookie jar before each identity-sensitive case.
- netrc and proxy environment behavior when local and CI results differ.
- Fixture scope and Session close/teardown paths.

### Worked example: an innocent cookie contaminates a negative test

A module-scoped Session logs in during the first test. The next “missing auth” case removes the Authorization header but retains the session cookie and returns `200`. A fresh unauthenticated Session correctly returns `401`, proving the shared cookie—not the endpoint—invalidated the test.

**Quiz.** Do method-level headers passed to session.get persist as new Session defaults?

- [ ] Yes, always
- [x] No; they merge for that request and matching values override only that call
- [ ] Only in pytest
- [ ] Only for Authorization

*The official Requests advanced guide distinguishes Session-level persisted defaults from method-level parameters.*

- **Session persistence** — Cookies and configured defaults persist across requests made by that Session.
- **Connection pooling** — A Session can reuse underlying connections to the same host.
- **Method-level override** — Merges for one request and does not automatically become a persisted default.
- **trust_env=False** — Stops a Session from relying on environment settings such as netrc credentials when hermetic behavior is needed.

### Challenge

Prove an unauthenticated case stays unauthenticated after a logged-in case by isolating Sessions and inspecting sanitized prepared-request headers.

### Ask the community

> My Requests Session unexpectedly sends `[cookie/header/auth]` in a later test; here are fixture scope and sanitized prepared-request headers.

Never post live cookies, passwords, bearer tokens, or netrc contents.

- [Requests — official Session objects guide](https://requests.readthedocs.io/en/stable/user/advanced/#session-objects)
- [Requests — official authentication guide](https://requests.readthedocs.io/en/stable/user/authentication/)

🎬 [OktaDev — Basic authentication in five minutes](https://www.youtube.com/watch?v=rhi1eIjSbvk) (5 min)

- Sessions persist cookies and configured defaults and reuse connections.
- Method-level dictionaries override matching Session values for one request without persisting automatically.
- Requests can use netrc credentials unless hermetic tests disable environment trust.
- Isolate identities, close Sessions, and test missing or insufficient auth without leaking secrets.


## Related notes

- [[Notes/api-test-automation/python-api-testing/parameterized-endpoint-tests|Parameterized endpoint tests]]
- [[Notes/api-test-automation/rest-assured-java/auth-in-rest-assured|Auth in REST Assured]]
- [[Notes/api-testing-fundamentals/auth-manually/basic-auth|Basic auth]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/python-api-testing/sessions-and-auth.mdx`_
