---
title: "Debugging proxies"
tags: ["testers-toolbox", "beyond-the-browser", "track-c"]
updated: "2026-07-16"
---

# Debugging proxies

*A debugging proxy sits between your app and the network, letting you inspect, modify, or fully mock any request or response - simulating a backend outage, a slow network, or a malformed API response without touching real code. mitmproxy is the free, open-source standard.*

> Some of the most important tests you'll ever run don't need a real broken backend at all — they need
> you to convincingly LIE to your own app about what the backend said. A debugging proxy sits between
> your browser/app and the real network, and lets you inspect, rewrite, delay, or fully mock any
> request or response passing through. Want to know what happens when the payment API returns a 500?
> You don't need to break payments — you need a proxy telling your app it did.

> **In real life**
>
> An old telephone switchboard didn't just pass calls straight through — an operator physically
> plugged one line into another, and could just as easily route a call somewhere else, hold it, or
> connect it to a different line entirely, all without either caller knowing the difference. A
> debugging proxy sits in exactly that operator's seat for network traffic: every request passes
> through a point where it can be inspected, rerouted, or answered differently before it ever reaches
> its real destination.

**debugging proxy**: A debugging proxy is a tool that sits between your application and the network, intercepting every HTTP/HTTPS request and response so you can inspect, modify, delay, or completely mock them before they reach their real destination (or without ever reaching it at all). mitmproxy (free, open source, MIT-licensed, terminal-based with a mitmweb browser UI) is the standard free option, alongside the lighter-weight Requestly (extension + desktop app). Both are verified alive and actively maintained in 2026.

## What sitting in the middle actually lets you do

- **Inspect real traffic in full detail** — every header, body, and status code exactly as sent and
  received, useful for confirming what an app ACTUALLY does versus what you assume it does.
- **Modify requests in flight** — rewrite a header, change a query parameter, alter a request body —
  simulating a different client version, a different auth token, or a malformed payload without
  changing any real code.
- **Mock responses entirely** — answer a request YOURSELF, on the proxy's behalf, without the real
  backend ever being contacted. This is how you simulate an outage, a timeout, or an error response
  from a service you have no ability to actually break.
- **Add artificial latency** — simulate a slow network or a struggling backend to test loading
  states, timeouts, and race conditions that only show up under real-world delay.

> **Tip**
>
> Mocking a backend response via proxy is safer and faster than asking a backend team to "please
> return a 500 for five minutes so I can test error handling" — no coordination needed, no risk to
> real users, and you can test the exact scenario as many times as you need.

> **Common mistake**
>
> Leaving proxy interception rules active after finishing a specific test and then being confused
> when unrelated features start behaving strangely. Proxy rules apply to everything matching their
> pattern — always disable or remove rules the moment you're done with the specific scenario they
> were built for.

![A vintage telephone switchboard with rows of numbered patch panels, dozens of colored plug-in cords, and toggle switches, against a red brick wall](debugging-proxies.jpg)
*Vintage telephone switchboard — Wikimedia Commons, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Vintage_telephone_switchboard_(49467795397).jpg)*
- **The plug-in cords — actively routed connections** — Each cord represents one call, physically rerouted through the operator's position - exactly like one HTTP request passing through the proxy's interception point before reaching (or not reaching) its real destination.
- **The labeled rows of jacks — every possible line, addressable** — Any connection can be picked out and worked with individually - the same way a proxy lets you target ONE specific endpoint's traffic (a pattern match) without touching everything else passing through.
- **The toggle switches — deliberate control over each connection** — A flip changes how a specific line behaves - the proxy equivalent of a rule that mocks, delays, or blocks one matched request while leaving everything else passing through untouched.
- **The full breadth of the panel, dozens of lines at once** — One operator overseeing many simultaneous connections - a proxy intercepting an entire app's network traffic simultaneously, ready to act on any single request that matches a rule.

**Simulating a backend outage without breaking anything real**

1. **Configure your device/browser to route through the proxy** — mitmproxy listens on a local port; point your app's network settings (or system proxy) at it.
2. **Confirm real traffic flows through cleanly first** — Load the app normally and see requests appear in the proxy's log - confirms interception is working before you touch anything.
3. **Write a rule matching the target endpoint** — e.g. any request to /api/payment/* - narrow enough not to affect unrelated traffic.
4. **Set the mock response (status code, body, or delay)** — A 500, a malformed JSON body, or a 10-second artificial delay - whatever the scenario needs.
5. **Trigger the real user flow and observe the app's reaction** — This is the actual test: does the UI handle the simulated failure gracefully, or does it break in a new way?

The core mechanic — intercepting a request and rewriting something about it in flight — is simple
enough to demonstrate directly:

*Run it - a proxy rule rewriting a header in flight (Python)*

```python
class InterceptedRequest:
    def __init__(self, url, headers, body=None):
        self.url = url
        self.headers = dict(headers)
        self.body = body

def apply_proxy_rules(request, rules):
    for rule in rules:
        if rule["match"] in request.url:
            if rule["action"] == "set_header":
                request.headers[rule["key"]] = rule["value"]
            elif rule["action"] == "block":
                return None
    return request

real_request = InterceptedRequest(
    "https://api.buggyshop.example/v2/checkout",
    {"Authorization": "Bearer real-prod-token", "X-Client-Version": "3.1.0"},
)

rules = [
    {"match": "/v2/checkout", "action": "set_header", "key": "X-Client-Version", "value": "1.0.0-legacy"},
    {"match": "/analytics", "action": "block"},
]

print("Real request, as the app actually sent it:")
print(f"  URL: {real_request.url}")
print(f"  Headers: {real_request.headers}")
print()

modified = apply_proxy_rules(real_request, rules)
print("After the debugging proxy's rules applied:")
print(f"  URL: {modified.url}")
print(f"  Headers: {modified.headers}")
print()
print("The client never changed - the PROXY rewrote X-Client-Version in flight,")
print("letting a tester simulate 'what happens on an old client version' without")
print("touching a single line of the app's real code.")

# Real request, as the app actually sent it:
#   URL: https://api.buggyshop.example/v2/checkout
#   Headers: {'Authorization': 'Bearer real-prod-token', 'X-Client-Version': '3.1.0'}
#
# After the debugging proxy's rules applied:
#   URL: https://api.buggyshop.example/v2/checkout
#   Headers: {'Authorization': 'Bearer real-prod-token', 'X-Client-Version': '1.0.0-legacy'}
#
# The client never changed - the PROXY rewrote X-Client-Version in flight,
# letting a tester simulate 'what happens on an old client version' without
# touching a single line of the app's real code.
```

Same idea in Java, this time fully MOCKING responses instead of just rewriting a header — the more
powerful, more commonly-used capability:

*Run it - mocking backend responses to test error handling (Java)*

```java
import java.util.*;

public class Main {
    static Map<String, Object> simulateProxyIntercept(String url, int realStatus, String mockOverrideStatus) {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("url", url);
        if (mockOverrideStatus != null) {
            result.put("status", Integer.parseInt(mockOverrideStatus));
            result.put("source", "PROXY MOCK (real backend never called)");
        } else {
            result.put("status", realStatus);
            result.put("source", "real backend");
        }
        return result;
    }

    public static void main(String[] args) {
        String[] endpoints = {"/api/payment/charge", "/api/inventory/check", "/api/shipping/rate"};
        int[] realStatuses = {200, 200, 200};
        String[] mockOverrides = {"500", null, "503"};

        System.out.println("Testing error handling by mocking backend responses via proxy:");
        System.out.println();
        for (int i = 0; i < endpoints.length; i++) {
            Map<String, Object> result = simulateProxyIntercept(endpoints[i], realStatuses[i], mockOverrides[i]);
            System.out.printf("  %-24s status=%s  (%s)%n", result.get("url"), result.get("status"), result.get("source"));
        }

        System.out.println();
        System.out.println("Two of three endpoints never touched the real backend at all -");
        System.out.println("the proxy answered on its behalf. This is how testers reproduce");
        System.out.println("a payment-service outage or inventory timeout WITHOUT needing");
        System.out.println("the real backend to actually be broken.");
    }
}

/* Testing error handling by mocking backend responses via proxy:

     /api/payment/charge      status=500  (PROXY MOCK (real backend never called))
     /api/inventory/check     status=200  (real backend)
     /api/shipping/rate       status=503  (PROXY MOCK (real backend never called))

   Two of three endpoints never touched the real backend at all -
   the proxy answered on its behalf. This is how testers reproduce
   a payment-service outage or inventory timeout WITHOUT needing
   the real backend to actually be broken. */
```

### Your first time: Your mission: mock one backend response and observe the app's reaction

- [ ] Install mitmproxy (free) and follow its setup guide to configure your browser/system to route through it — mitmweb gives you a browser-based UI if the terminal interface feels unfamiliar at first.
- [ ] Load BuggyShop normally and confirm real traffic appears in the proxy's log — This confirms interception works before you start writing any rules.
- [ ] Write one rule targeting a specific API call (e.g. the checkout endpoint) to return a 500 — Narrow the match pattern carefully - too broad, and you'll break unrelated traffic by accident.
- [ ] Trigger the real checkout flow and observe what the UI does — Does it show a clear error message? A blank screen? A stuck loading spinner forever?
- [ ] Remove the rule immediately after and confirm normal traffic resumes — The mandatory cleanup step - never leave a mock rule active once you're done with its specific test.

You've simulated a real backend failure and observed exactly how the app handles it — without ever
touching, breaking, or coordinating around the actual backend.

- **Traffic doesn't appear to flow through the proxy at all.**
  Confirm the device/browser's proxy settings actually point to the tool's listening address and port, and that the app isn't using a certificate-pinning mechanism that rejects the proxy's TLS certificate - mitmproxy's own docs cover installing its CA certificate for HTTPS interception specifically.
- **HTTPS traffic shows as encrypted/unreadable even with the proxy running.**
  You likely haven't installed the proxy's certificate authority (CA) certificate as trusted on the testing device - this is a required one-time setup step for intercepting HTTPS specifically (not needed for plain HTTP), documented in every debugging proxy's setup guide.
- **A mock rule seems to also be affecting traffic you didn't intend to touch.**
  The match pattern is broader than intended - review it carefully (a substring match on '/api/' will hit far more than a single endpoint) and narrow it to the most specific identifiable part of the target URL.
- **You forgot a mock rule was still active and spent time confused about 'broken' behavior elsewhere.**
  This is exactly the cleanup-discipline mistake this note warns about - make checking/clearing active rules a reflexive habit at the START of every new testing session, not just something you remember to do at the end.

### Where to check

- **The proxy's own traffic log/flow list** — the ground truth for exactly what was sent and received, including anything a rule modified.
- **The proxy's active rules list** — always check what's currently configured before starting a new test session, to catch any forgotten rule from a previous session.
- **The app's actual error-handling UI** — the real point of this whole exercise; a mocked failure response only matters if you observe how the app responds to it.
- **The proxy's certificate/CA installation status** — the most common setup blocker for HTTPS interception specifically.

### Worked example: finding a stuck-loading-spinner bug via a mocked timeout

1. Testing checkout's resilience: does the app handle a slow payment service gracefully, or does it
   hang forever? Real payment services rarely run slowly on demand for testing purposes.
2. Using mitmproxy, a rule adds a 15-second artificial delay to the payment endpoint's response,
   with no change to the actual payment service.
3. Triggering checkout: the loading spinner appears immediately (correct so far) — but at 15
   seconds, when the (mocked, delayed) response finally arrives, the spinner just... keeps spinning.
   No error, no success state, nothing.
4. Investigating: the frontend has a timeout mechanism set to 10 seconds that should have shown a
   "taking longer than expected" message and offered a retry — but a bug in that logic silently
   swallowed the timeout instead of displaying it.
5. Report: "Checkout hangs indefinitely with no error/retry UI when the payment endpoint takes
   longer than the frontend's own 10-second timeout threshold. Reproduced via mitmproxy artificial
   delay (15s) on /api/payment/charge - the timeout fires internally but its UI state never
   renders." A real, hard-to-otherwise-reproduce timing bug, found without waiting for a genuinely
   slow real backend.

**Quiz.** A tester wants to verify that BuggyShop shows a clear error message when the inventory-check API returns a 503 (service unavailable). What's the most efficient way to test this using a debugging proxy, compared to trying to reproduce a real 503 from the actual backend?

- [ ] Repeatedly hammer the real inventory-check endpoint with requests until it happens to fail naturally, then quickly try to reproduce the UI state before it recovers
- [x] Write a proxy rule that mocks a 503 response for the inventory-check endpoint specifically, trigger the flow, observe the UI, then remove the rule - producing the exact scenario on demand without needing the real backend to actually be unavailable
- [ ] Ask the backend team to manually take the inventory service offline for a few minutes during a scheduled window
- [ ] This scenario can only be tested in a genuine outage and should be documented as an untestable edge case

*This is precisely the core value proposition of a debugging proxy demonstrated throughout this note: mocking the exact response on demand, safely and repeatably, without needing the real backend to actually misbehave. Option one is unreliable, disruptive to a real service, and nearly impossible to time correctly to catch the UI state in the moment of failure. Option three works but requires cross-team coordination, scheduling, and real risk to a live service for something a proxy rule accomplishes in seconds, safely, and repeatably as many times as needed. Option four is simply wrong - this exact scenario is one of the most straightforward things a debugging proxy is built to make testable, not an edge case to give up on.*

- **Debugging proxy — what it does** — Sits between your app and the network, intercepting every request/response so you can inspect, modify, delay, or fully mock them - free options: mitmproxy (terminal + mitmweb UI) and Requestly (extension + desktop), both alive in 2026.
- **Why mocking a response beats waiting for a real failure** — Simulates an outage, timeout, or error response on demand, safely, and repeatably - no need to break a real backend or coordinate with another team to test error-handling paths.
- **The mandatory cleanup habit** — Always disable/remove proxy rules the moment you're done with their specific scenario - a forgotten active rule silently affects unrelated traffic and causes confusing, hard-to-diagnose 'bugs' later.
- **The HTTPS interception setup requirement** — You must install the proxy's CA certificate as trusted on the testing device to intercept HTTPS traffic specifically - a one-time setup step, distinct from plain HTTP interception which needs no certificate.
- **What artificial latency lets you test** — Loading states, timeouts, and race conditions that only manifest under real-world network delay - hard or impossible to reliably reproduce by just waiting for a real slow network.
- **Why narrow match patterns matter for proxy rules** — A too-broad pattern (like matching on '/api/' generally) can affect far more traffic than intended - always scope rules to the most specific identifiable part of the target URL.

### Challenge

Using mitmproxy or Requestly, write a rule that mocks a 500 response for one specific BuggyShop or
BuggyAPI endpoint. Trigger the real flow that calls it and document exactly how the app responds -
does it show a clear error, fail silently, or break in an unexpected way? Remove the rule when done
and confirm normal behavior resumes.

### Ask the community

> I mocked `[status code/response]` for `[endpoint]` using `[mitmproxy/Requestly]` and observed `[app behavior]`. Is this the expected/designed error-handling behavior for this endpoint, or does it look like a real gap?

Error-handling expectations vary by endpoint and team convention — the most useful answers will
confirm whether the observed behavior matches what this specific flow was actually designed to do.

- [mitmproxy — official site (free, open source)](https://www.mitmproxy.org/)
- [mitmproxy — official docs: intercepting requests](https://docs.mitmproxy.org/stable/mitmproxytutorial-interceptrequests/)
- [Capture, Analyze and Debug HTTPS Traffic with mitmproxy](https://www.youtube.com/watch?v=7BXsaU42yok)

🎬 [Learn mitmproxy #1 — Record, Replay, Intercept, and Modify HTTP Requests (QAInsights)](https://www.youtube.com/watch?v=igcsLKDfssw) (14 min)

- A debugging proxy sits between your app and the network, letting you inspect, modify, delay, or fully mock any request/response - mitmproxy (free, open source) and Requestly are both alive and maintained in 2026.
- Mocking a response lets you simulate an outage, timeout, or malformed data on demand, safely and repeatably, without needing a real backend to actually misbehave.
- HTTPS interception requires installing the proxy's CA certificate as trusted - a required one-time setup step distinct from plain HTTP.
- Always disable/remove rules the moment you're done with their specific test - a forgotten rule silently affects unrelated traffic later.
- Narrow match patterns to the most specific part of a target URL - overly broad patterns catch more traffic than intended.


## Related notes

- [[Notes/testers-toolbox/beyond-the-browser/email-testing|Email testing]]
- [[Notes/api-testing-fundamentals/finding-api-bugs/negative-api-tests|Negative API tests]]
- [[Notes/defect-management/writing-bug-reports/evidence|Evidence]]


---
_Source: `packages/curriculum/content/notes/testers-toolbox/beyond-the-browser/debugging-proxies.mdx`_
