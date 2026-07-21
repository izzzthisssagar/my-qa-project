---
title: "Cypress"
tags: ["automation-foundations", "the-tool-landscape", "track-d"]
updated: "2026-07-18"
---

# Cypress

*Cypress specializes in testing your own modern web application from inside the browser, with retry-ability, time-travel debugging, network control, and a deliberately bounded JavaScript-first model.*

> Imagine watching a failed checkout step by step: the command log freezes each moment, the DOM snapshot
> shows what existed, and a network intercept reveals the response that moved the UI. That tight feedback
> loop is Cypress's center of gravity. Its boundaries are equally important: it is specialized for your
> web app, not a universal remote for every automation problem.

> **In real life**
>
> An airport control tower sees the live runway, coordinates traffic, and records events from inside the
> operating environment. That proximity makes diagnosis fast. It also has a jurisdiction: the controller
> does not drive two aircraft from their cockpits or operate a distant seaport. Cypress's in-browser
> architecture offers privileged app/network visibility while deliberately limiting some multi-window,
> multi-browser, native-event, and general-purpose workflows.

**Cypress**: Cypress is a JavaScript-based quality platform whose App specializes in end-to-end, component, and API-oriented testing of modern web applications. Cypress commands execute with privileged access around the application under test, and linked queries/assertions retry automatically. Its architecture also creates explicit trade-offs for general-purpose automation, multiple simultaneous browsers, native mobile events, and some cross-origin or iframe workflows.

## Sweet spot and boundaries

As checked on **2026-07-18**, Cypress documentation calls the App strong at end-to-end, component,
and API testing of your own application. It supports Chrome-family browsers (including Edge and
Electron), Firefox, and experimental WebKit. Its trade-offs page says JavaScript is the supported test
language, it cannot drive two browsers simultaneously, each test is bound to one superdomain unless
`cy.origin()` is used, and native/mobile events are not supported. These are workload facts, not insults.

Queries and assertions retry; non-query commands execute once. Network interception, clock control,
screenshots/video, and the command log make frontend failures observable. Component testing can mount
UI pieces close to their framework. Teams already living in JavaScript with app-code access often gain
fast onboarding; teams needing Java bindings, two-user simultaneous browser control, or broad native
automation should prove those boundaries early.

> **Tip**
>
> Write the architectural constraint beside every demo: one browser at a time,
> origin model, iframe/payment-provider behavior, WebSocket needs, and language. A beautiful happy path
> cannot answer whether your hardest workflow fits.

> **Common mistake**
>
> Assuming every Cypress command retries. Queries and assertions retry together;
> side-effecting non-queries do not. Put the uncertain state in a retried assertion rather than repeatedly
> submitting the order.

![Interior of Seattle-Tacoma airport control tower with controllers, many screens, consoles, and runways visible through windows](cypress.jpg)
*KSEA Tower Interior — Jelson25, Wikimedia Commons, CC BY 3.0. [Source](https://commons.wikimedia.org/wiki/File:KSEA_Tower_Interior.jpg)*
- **Live runway view** — In-browser proximity gives Cypress a direct view of app state and network behavior.
- **Command consoles** — The command log and snapshots make the exact sequence inspectable after failure.
- **Single controlled airspace** — A powerful operating boundary: excellent inside its jurisdiction, not general-purpose control of every external system.

**Cypress retry-ability without duplicate side effects**

1. **Issue one action** — Submit once; a non-query command executes once.
2. **Query outcome** — Find the receipt status in the DOM.
3. **Retry query + assertion** — Cypress re-queries until the assertion passes or timeout expires.
4. **Keep evidence** — Command log, snapshot, network data, screenshot, and video explain the terminal state.

*Model linked query retries (Python)*

```python
statuses = ["processing", "processing", "paid"]
attempts = 0

def query_status():
    global attempts
    value = statuses[min(attempts, len(statuses) - 1)]
    attempts += 1
    return value

observed = ""
for _ in range(4):
    observed = query_status()
    if observed == "paid": break
assert observed == "paid" and attempts == 3, "retry oracle rejected"
print("attempts:", attempts)
print("observed:", observed)
print("verdict:", "PASS" if observed == "paid" and attempts == 3 else "FAIL")
```

*Model linked query retries (Java)*

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        var statuses = List.of("processing", "processing", "paid");
        int attempts = 0; String observed = "";
        for (int i = 0; i < 4; i++) {
            observed = statuses.get(Math.min(attempts, statuses.size() - 1));
            attempts++;
            if (observed.equals("paid")) break;
        }
        if (!observed.equals("paid") || attempts != 3) throw new AssertionError("retry oracle rejected");
        System.out.println("attempts: " + attempts);
        System.out.println("observed: " + observed);
        System.out.println("verdict: " + (observed.equals("paid") && attempts == 3 ? "PASS" : "FAIL"));
    }
}
```

### Your first time: Test Cypress's real boundary

- [ ] Automate one owned-app flow — Use a retried assertion and inspect the command log.
- [ ] Intercept one network request — Prove whether control improves determinism without hiding integration risk.
- [ ] Prototype the hardest origin/iframe/user case — Do this before writing dozens of easy specs.
- [ ] Run required browsers in CI — Label experimental WebKit honestly and date the matrix.

- **A payment iframe cannot be queried like the app DOM.**
  Identify its origin and provider boundary; use the documented cross-origin approach or test your integration contract plus a smaller provider E2E path.
- **Retries submit an order more than once.**
  Keep the action outside the retrying query/assertion chain; retry observation, not the side effect.

### Where to check

- Command Log snapshots around the first divergence.
- Network intercepts and browser console for app/server causality.
- Cypress trade-offs and launching-browsers docs before promising a matrix.

### Worked example: A React team testing its own storefront

The team is JavaScript-first, owns app code, wants component plus E2E tests, and values interactive
debugging. Cypress fits. A separate flow requires two real users in simultaneous browsers approving a
transaction; the official one-browser boundary makes that a poor Cypress-only proof. Keep the ordinary
storefront suite in Cypress and validate the dual-user workflow with a tool designed for that workload.

**Quiz.** Which Cypress statement is accurate as of 2026-07-18?

- [ ] It is a general-purpose desktop automation tool
- [ ] It natively drives two browsers simultaneously
- [x] Linked queries and assertions retry, while non-queries execute once
- [ ] It supports every backend language as a test language

*That is the documented retry model. The other options contradict Cypress's stated trade-offs.*

- **Cypress sweet spot** — Testing your own modern web app with tight JavaScript, DOM, network, and debugging integration.
- **Retry rule** — Queries and assertions retry; non-query commands execute once.
- **Boundary to prove early** — Origins, iframes, simultaneous browsers/users, native events, and language constraints.

### Challenge

Change `paid` to `declined` in both playground datasets. The assertion must fail instead of
turning the last observed value into a pass. That is the difference between retrying and forgiving.

### Ask the community

> Our app is JavaScript-first but checkout crosses a hosted payment iframe. How should we split coverage?

Good answers combine owned-app Cypress coverage, API/contract checks at the provider boundary, and a
small authorized end-to-end path that respects the documented origin/iframe model.

- [Cypress — Why Cypress?](https://docs.cypress.io/app/get-started/why-cypress)
- [Cypress — Retry-ability](https://docs.cypress.io/app/core-concepts/retry-ability)
- [Cypress — Trade-offs](https://docs.cypress.io/app/references/trade-offs)

🎬 [What is Cypress?](https://vimeo.com/237527670) (2 min)

- Cypress optimizes the feedback loop for testing your own web application.
- Its in-browser architecture provides unusual visibility and explicit workload boundaries.
- Retry observation, not side effects.
- Check origin, iframe, simultaneous-user, native-event, browser, and language needs before committing.


## Related notes

- [[Notes/automation-foundations/the-tool-landscape/selenium|Selenium]]
- [[Notes/automation-foundations/the-tool-landscape/playwright-tool|Playwright]]
- [[Notes/automation-foundations/the-tool-landscape/choosing-a-tool|Choosing a tool]]


---
_Source: `packages/curriculum/content/notes/automation-foundations/the-tool-landscape/cypress.mdx`_
