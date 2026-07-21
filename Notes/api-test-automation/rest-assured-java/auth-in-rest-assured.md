---
title: "Authentication in REST Assured"
tags: ["api-test-automation", "rest-assured-java", "track-d"]
updated: "2026-07-17"
---

# Authentication in REST Assured

*Apply Basic, bearer, OAuth2, or other supported authentication at request or specification scope, keep secrets out of code and logs, and test both access and refusal.*

> A test suite that proves valid tokens work but never proves invalid tokens fail has tested the welcome mat and skipped the lock.

> **In real life**
>
> A clear padlock shows the mechanism: the correct key aligns every pin, while a near-match must still be refused. Auth tests need the same positive and negative evidence.

**authentication**: Authentication supplies evidence of identity with a request. REST Assured supports request-scoped and reusable authentication for schemes including Basic, digest, OAuth, certificates, and form auth; bearer tokens can be sent through OAuth2 support or an Authorization header.

## Scope credentials deliberately

```java
given()
  .baseUri(baseUri)
  .auth().oauth2(System.getenv("API_TOKEN"))
.when()
  .get("/v1/me")
.then()
  .statusCode(200);
```

For Basic auth, know which behavior you are testing. Preemptive Basic sends credentials immediately;
challenged Basic waits for the server's challenge and may require an additional request.

> **Tip**
>
> Build an authenticated `RequestSpecification` from environment-provided secrets, then override or omit auth in dedicated negative tests.

> **Common mistake**
>
> Turning on full request logging and shipping `Authorization: Bearer ...` into CI artifacts. Debug output is still data exfiltration when the secret wears monospace.

![Transparent practice padlock with two metal keys](auth-in-rest-assured.jpg)
*Clear padlock and keys — zaphad1, Wikimedia Commons, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Clear_padlock_and_keys.jpg)*
- **Credential** — The presented key: password, token, or certificate.
- **Auth scheme** — The mechanism determines how the credential travels and is challenged.
- **Authorization result** — The server must grant the right identity and reject missing or invalid evidence.

**Prove the lock, not just the key**

1. **Load secret safely** — Read it from environment or a secret manager.
2. **Apply correct scheme** — Basic, bearer/OAuth2, certificate, or the API's documented mechanism.
3. **Assert authorized behavior** — The intended identity receives the intended resource.
4. **Assert refusal paths** — Missing, malformed, expired, and wrong-scope credentials fail correctly.

*Run it — a tiny authorization matrix (Python)*

```python
def authorize(token, required_scope):
    tokens = {"good": {"read:tickets"}, "wrong-scope": {"read:profile"}}
    if token not in tokens: return 401
    return 200 if required_scope in tokens[token] else 403

for name, token in [("valid", "good"), ("missing", None), ("bad", "nope"), ("scope", "wrong-scope")]:
    print(f"{name}: HTTP {authorize(token, 'read:tickets')}")

# valid: HTTP 200
# missing: HTTP 401
# bad: HTTP 401
# scope: HTTP 403
```

*Run it — a tiny authorization matrix (Java)*

```java
import java.util.*;
public class Main {
  static int authorize(String token, String scope) {
    Map<String, Set<String>> tokens = Map.of("good", Set.of("read:tickets"), "wrong-scope", Set.of("read:profile"));
    if (token == null || !tokens.containsKey(token)) return 401;
    return tokens.get(token).contains(scope) ? 200 : 403;
  }
  public static void main(String[] args) {
    String[][] cases = {{"valid","good"},{"missing",null},{"bad","nope"},{"scope","wrong-scope"}};
    for (String[] c : cases) System.out.println(c[0] + ": HTTP " + authorize(c[1], "read:tickets"));
  }
}

/* valid: HTTP 200
   missing: HTTP 401
   bad: HTTP 401
   scope: HTTP 403 */
```

### Your first time: Your mission: test an auth matrix

- [ ] Load a test credential outside source control — Fail clearly when it is absent without printing its value.
- [ ] Prove the valid credential reaches the right identity — Assert an identity or scope field, not only 200.
- [ ] Test missing and malformed credentials — Expect the documented authentication failure, commonly 401.
- [ ] Test valid identity with insufficient permission — Expect the documented authorization failure, commonly 403.

- **Basic auth causes two requests.**
  Use preemptive Basic if the goal is ordinary authenticated access; keep challenged mode when testing the challenge itself.
- **A bearer token works locally but not in CI.**
  Check secret availability, whitespace/newlines, environment scope, and expiration without logging the token.
- **A redirect loses Authorization.**
  Inspect redirect hosts and policy; credentials should not casually cross hosts.

### Where to check

- The API's documented authentication scheme and required scopes.
- Sanitized request logs showing the scheme, never the secret value.
- CI secret scope and expiration metadata.
- Separate 401 authentication and 403 authorization expectations.

### Worked example: a token that opens too much

A read-only token successfully calls `GET /v1/tickets`, then unexpectedly receives `204` from `DELETE /v1/tickets/T-7`. The negative scope test fails, revealing excess authorization. A happy-path-only suite would advertise the token as healthy.

**Quiz.** What is the key behavioral difference between preemptive and challenged Basic auth?

- [x] Preemptive sends credentials before a challenge; challenged waits and may make another request
- [ ] Challenged encrypts the password
- [ ] Preemptive uses bearer tokens
- [ ] There is no difference

*The official REST Assured usage guide documents the request-timing difference; neither mode makes plain HTTP safe, so use TLS.*

- **401 vs 403** — 401 commonly means missing/invalid authentication; 403 means the identity is known but not allowed.
- **Preemptive Basic** — Sends credentials immediately instead of waiting for a server challenge.
- **Safe secret source** — Environment or secret manager, never committed code or fixtures.
- **Complete auth coverage** — Valid identity plus missing, invalid, expired, and insufficient-scope cases.

### Challenge

Create a reusable authenticated request specification and four isolated auth tests while ensuring failure logs redact the Authorization value.

### Ask the community

> My auth test gets `[401/403/redirect]` using `[scheme]`; here is the sanitized request flow and documented scope.

Never paste a live token, cookie, password, private key, or raw CI artifact.

- [REST Assured — official authentication usage](https://github.com/rest-assured/rest-assured/wiki/Usage#authentication)
- [REST Assured — official Basic authentication behavior](https://github.com/rest-assured/rest-assured/wiki/Usage#basic-authentication)

🎬 [JayPMedia — JWT explained visually](https://www.youtube.com/watch?v=0WH9oiYMS3M) (4 min)

- Apply the API's documented scheme at request or reusable specification scope.
- Keep credentials outside source and redact them from logs and artifacts.
- Preemptive Basic sends immediately; challenged Basic waits for a challenge.
- Test valid access and refusal for missing, bad, expired, and under-scoped credentials.


## Related notes

- [[Notes/api-test-automation/rest-assured-java/validating-json-and-status|Validating JSON & status]]
- [[Notes/api-test-automation/python-api-testing/sessions-and-auth|Sessions & auth]]
- [[Notes/api-testing-fundamentals/auth-manually/bearer-and-jwt|Bearer / JWT]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/rest-assured-java/auth-in-rest-assured.mdx`_
