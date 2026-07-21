---
title: "REST in plain words"
tags: ["api-testing-fundamentals", "status-codes-and-rest", "track-c"]
updated: "2026-07-17"
---

# REST in plain words

*REST is a small set of conventions for naming and addressing things: resources are nouns with their own URL, and the HTTP method (already covered) is the verb applied to that noun. No new technology - just an agreement on shape.*

> "RESTful API" gets thrown around like it's a specific technology - a library to install, a protocol
> to speak. It isn't. REST (REpresentational State Transfer) is a STYLE, a set of conventions for how
> to name and organize things over HTTP. Once you see the pattern, you'll recognize it (or its
> absence) in every API you're handed, and you'll be able to say precisely WHY an endpoint feels
> "off" instead of just vaguely sensing it.

> **In real life**
>
> A wall-mounted candy machine with three separate chutes: milk chocolate, caramel, peanut. Each
> chute is its own addressable slot - insert tokens into the CARAMEL chute and only caramel comes out,
> no matter what else is in the machine. Notice the caramel chute has a hand-written "OUT" label taped
> over it: the SLOT still exists and is still addressable (you can still try it), it's just currently
> empty. That's the essence of REST: every kind of thing gets its own consistently-named, independently
> addressable slot (`/chocolate`, `/caramel`, `/peanut` - or in API terms, `/flights`, `/bookings`,
> `/passengers`), and the method you apply (insert tokens = "give me one") is the same regardless of
> which slot you're pointed at.

**REST**: REST (REpresentational State Transfer) is an architectural STYLE for HTTP APIs, not a protocol or library. Its core conventions: (1) RESOURCES are nouns, each with its own URL (/flights, /flights/42, /flights/42/passengers) - never verbs in the path (not /getFlight or /createBooking); (2) the HTTP METHOD supplies the verb (GET/POST/PUT/DELETE - see the http-methods note) rather than the URL encoding the action; (3) resources can be nested to express relationships (/flights/42/passengers means 'passengers belonging to flight 42'); (4) representations are typically JSON (occasionally XML), and the same resource can often be requested in different representations via the Accept header. An API that puts verbs in URLs (/api/getUserData?id=5) or encodes every action as a POST to one fixed endpoint is NOT REST-style, even if it runs over HTTP and returns JSON - REST is specifically about resource-oriented URLs plus method-as-verb.

## The conventions, one at a time

- **Resources are nouns, in the URL.** `/flights`, not `/getFlights` or `/flightList`. The noun
  names the THING; the method (already covered in this module) supplies the verb.
- **Collections vs individual items.** `/flights` (the whole collection - GET lists them, POST
  creates a new one) versus `/flights/42` (one specific item - GET reads it, PUT replaces it, DELETE
  removes it). The trailing ID is what turns "the whole aisle" into "this one specific slot."
- **Nesting expresses relationships.** `/flights/42/passengers` reads naturally as "the passengers
  belonging to flight 42" - a sub-resource scoped to its parent, not a separate, unrelated endpoint
  that happens to share a URL prefix.
- **Query strings filter/sort/paginate; they don't name new resources.** `/flights?from=DEL&to=BOM`
  is still the `/flights` resource, filtered - not a different kind of thing. If a query parameter
  starts fundamentally changing WHAT the response represents (not just narrowing it), that's usually
  a sign the API should have used a different URL/resource entirely.
- **Verbs occasionally sneak back in for actions with no clean noun** — `/bookings/42/cancel` (a
  `POST`) is a common, pragmatic exception for actions that don't map cleanly onto plain
  CRUD-on-a-noun. Not "wrong" REST, just the honest edge case every real API eventually has.

> **Tip**
>
> When an API's URLs read like a sentence of ACTIONS (`/processOrder`, `/getUserInfo`,
> `/updateStatus`), that's the fastest tell that you're looking at something more RPC-flavored than
> REST-style - worth confirming with the docs rather than assuming, since plenty of real production
> APIs are a deliberate, documented mix of both styles.

> **Common mistake**
>
> Assuming "uses JSON over HTTP" automatically means "RESTful." Plenty of APIs are JSON-over-HTTP but
> verb-in-URL, single-endpoint RPC-style underneath (a lot of internal/legacy APIs look exactly like
> this). REST is specifically about the resource-oriented URL + method-as-verb conventions above, not
> about the wire format.

![A wall-mounted candy vending machine with three vertical glass chutes labeled milk chocolate, a middle one with a hand-written OUT label, and peanut, each above its own coin-operated dispensing mechanism](rest-in-plain-words.jpg)
*Candy vending machine — Wikimedia Commons, CC0 / public domain. [Source](https://commons.wikimedia.org/wiki/Category:Vending_machines)*
- **The 'OUT' chute — still addressable, just empty** — This is exactly a 404-worthy resource: the SLOT (URL) still legitimately exists and can be asked about, it's just currently got nothing in it. An empty collection isn't a broken endpoint - it's a valid, addressable resource with zero items right now.
- **Peanut chute — same shape, different resource, different price** — Same interaction pattern (insert tokens, get one out) as the other two chutes, but its own separate resource with its own separate state (3 tokens instead of 2) - nesting/parallel resources share a pattern without sharing state.

**Reading a REST-style URL, piece by piece - press Play**

1. **GET /flights** — Noun: flights (the collection). Method: GET (read). Meaning: give me the list of flights. No verb anywhere in the URL itself.
2. **GET /flights/42** — Same noun, now with an ID - one specific item instead of the whole collection. Still just GET; the URL alone tells you WHICH thing, the method tells you WHAT to do with it.
3. **GET /flights/42/passengers** — Nesting: passengers that belong to flight 42 specifically - not the entire passengers table, not an unrelated endpoint. The URL path itself encodes the relationship.
4. **POST /bookings/42/cancel** — The pragmatic exception: 'cancel' is a verb sitting right in the URL, because there's no clean noun-and-method combination for this specific action. Common, not a REST violation in practice.
5. **Verdict** — Nouns in the path, methods as verbs, nesting for relationships, query strings for filtering - and the occasional honest action-verb exception. That's the whole style.

A small in-memory REST-style router - matching noun + ID patterns the way a real framework would,
to show the convention isn't magic, just consistent string matching:

*Run it - a minimal REST-style router (Python)*

```python
import re

routes = [
    (r"^/flights$", "list all flights"),
    (r"^/flights/(\\d+)$", "get one flight by id"),
    (r"^/flights/(\\d+)/passengers$", "list passengers for a flight"),
    (r"^/bookings/(\\d+)/cancel$", "cancel a specific booking (pragmatic verb exception)"),
]

def route(path):
    for pattern, meaning in routes:
        match = re.match(pattern, path)
        if match:
            ids = match.groups()
            return f"{meaning}" + (f" (id={ids[0]})" if ids else "")
    return "404 - no matching resource"

test_paths = [
    "/flights",
    "/flights/42",
    "/flights/42/passengers",
    "/bookings/7/cancel",
    "/getFlights",
]

for path in test_paths:
    print(f"{path:28} -> {route(path)}")

# /flights                     -> list all flights
# /flights/42                  -> get one flight by id (id=42)
# /flights/42/passengers       -> list passengers for a flight (id=42)
# /bookings/7/cancel           -> cancel a specific booking (pragmatic verb exception) (id=7)
# /getFlights                  -> 404 - no matching resource
```

The same routing idea in Java, using regex patterns the same way a real router matches paths under
the hood:

*Run it - a minimal REST-style router (Java)*

```java
import java.util.*;
import java.util.regex.*;

public class Main {
    record Route(Pattern pattern, String meaning) {}

    public static void main(String[] args) {
        List<Route> routes = List.of(
            new Route(Pattern.compile("^/flights$"), "list all flights"),
            new Route(Pattern.compile("^/flights/(\\\\d+)$"), "get one flight by id"),
            new Route(Pattern.compile("^/flights/(\\\\d+)/passengers$"), "list passengers for a flight"),
            new Route(Pattern.compile("^/bookings/(\\\\d+)/cancel$"), "cancel a specific booking (pragmatic verb exception)")
        );

        String[] testPaths = {"/flights", "/flights/42", "/flights/42/passengers", "/bookings/7/cancel", "/getFlights"};

        for (String path : testPaths) {
            System.out.printf("%-28s -> %s%n", path, route(routes, path));
        }
    }

    static String route(List<Route> routes, String path) {
        for (Route r : routes) {
            Matcher m = r.pattern().matcher(path);
            if (m.matches()) {
                String result = r.meaning();
                if (m.groupCount() > 0) {
                    result += " (id=" + m.group(1) + ")";
                }
                return result;
            }
        }
        return "404 - no matching resource";
    }
}

// /flights                     -> list all flights
// /flights/42                  -> get one flight by id (id=42)
// /flights/42/passengers       -> list passengers for a flight (id=42)
// /bookings/7/cancel           -> cancel a specific booking (pragmatic verb exception) (id=7)
// /getFlights                  -> 404 - no matching resource
```

### Your first time: Your mission: map five real URLs to nouns and verbs

- [ ] Open any API's docs (BuggyAPI's OpenAPI docs or a public API's reference) — Pick five endpoints across at least two different HTTP methods.
- [ ] For each, write down the noun (resource) and the verb (HTTP method) separately — e.g. 'flights' + GET, 'bookings' + POST - resist reading the path as one blob.
- [ ] Find at least one nested resource (a path with two nouns in it) — Confirm it reads as 'the [child] belonging to [parent]', not something unrelated sharing a URL prefix.
- [ ] Find at least one query-string parameter and confirm it filters rather than changes the resource type — e.g. ?status=delayed on /flights should still return flights, just a subset.
- [ ] Look for any pragmatic verb-in-URL exceptions (like a /cancel or /activate action endpoint) — Note whether the docs call this out as an exception or if the whole API is actually verb-in-URL throughout.

You've read a real API's URL design the way its authors intended - by separating noun from verb
instead of treating each path as an opaque string to memorize.

- **An API's paths all look like /api/action?type=getFlights, with every real endpoint funneling through one URL and a type parameter choosing the actual operation.**
  This isn't a bug exactly, but it IS worth flagging as a design/testability observation: this is RPC-style, not REST-style. It changes how you test it (you can't rely on REST conventions like 'GET is always safe here' - check what each type value actually does, since the URL/method alone won't tell you).
- **GET /flights/42/passengers returns passengers that don't actually belong to flight 42.**
  This is a real, filable bug - nesting in a REST-style URL is a documented CONTRACT ('passengers scoped to this parent'), not just a naming convention. Returning unscoped or wrongly-scoped data breaks that contract regardless of what the response's status code says.
- **A query-string filter like ?status=delayed on /flights returns a completely different SHAPE of object than an unfiltered GET /flights does.**
  Worth flagging: query strings are supposed to filter/sort/paginate the SAME resource, not change what kind of thing is being returned. A shape change based on a filter parameter is a design inconsistency clients won't expect, even if each individual response is internally well-formed.

### Where to check

- **The API's OpenAPI/Swagger spec or route list** — the definitive list of which nouns and nesting actually exist; see [[api-testing-fundamentals/status-codes-and-rest/reading-api-docs-and-swagger]].
- **The URL path itself, read noun-first** — before touching headers or body, name the resource and any nesting out loud.
- **Whether GET requests are actually safe (never mutate state)** — a REST-style API's GET should never change data; see [[api-testing-fundamentals/status-codes-and-rest/idempotency-and-safety]] for the deeper property this touches.
- **BuggyAPI (TaskFlight)** — read its actual route list (`/api/v1/flights`, `/api/v1/bookings`, etc.) and confirm which parts follow REST conventions and where, if anywhere, it takes the pragmatic verb-exception route.

### Worked example: a scoping bug found by taking REST's nesting contract literally

1. An API exposes `GET /projects/{projectId}/tickets` - the URL's nesting implies "tickets that
   belong to this specific project."
2. A tester, taking that contract literally, creates two projects (A and B), adds tickets to each,
   then calls `GET /projects/A/tickets`.
3. Expected: only Project A's tickets. Actual: the response includes several tickets that were
   created under Project B.
4. This isn't a "which status code" question at all - the response is a `200 OK`, correctly
   formatted JSON. The bug is purely in whether the nesting's implied scoping is actually enforced
   server-side.
5. Root cause, once reported: the tickets endpoint filters by the caller's account but forgot to
   also filter by the `projectId` path parameter - a classic case of the URL PROMISING scoping that
   the handler code never actually implements.
6. Finding: "`GET /projects/{projectId}/tickets` returns tickets from other projects under the same
   account - the path's nesting isn't enforced, it's decorative." Found entirely by treating REST's
   naming convention as a literal, testable contract rather than just a URL-styling choice.

**Quiz.** An API has two endpoints: `POST /flights` (creates a flight) and `POST /api/createFlight` (also creates a flight, functionally identical, older). From a REST-style perspective, what's the key difference between them worth noting in a test report?

- [ ] There's no meaningful difference - both use POST and both create a flight, so they're equally RESTful
- [ ] /api/createFlight is more explicit and therefore the better-designed endpoint, since its name states exactly what it does
- [x] POST /flights follows REST convention (noun in the URL, POST supplies the 'create' verb); /api/createFlight repeats the verb IN the URL on top of the HTTP method already supplying one - a naming inconsistency worth flagging even though both may work correctly, since it signals the API mixes two different design styles
- [ ] Neither endpoint can be RESTful because true REST APIs never use POST for creation

*This note is explicit that REST-style URLs use nouns, with the HTTP method supplying the verb - /flights (noun) + POST (verb: create) is exactly that pattern. /api/createFlight puts a verb ('create') directly in the path ON TOP of POST already being the verb, which is the RPC-style pattern this note calls out as the fastest tell of a non-REST endpoint. This isn't necessarily a functional BUG (option one's 'no difference' undersells it, but it isn't broken either) - it's a design-consistency finding worth noting, since an API mixing both styles is harder to predict behavior for. Option two is backwards - the explicit verb-in-URL is the RPC-style tell, not a design win. Option four is factually wrong: POST is exactly the correct REST verb for creation.*

- **REST, in one sentence** — An architectural style: resources are nouns with their own URL, the HTTP method supplies the verb - not a protocol or library.
- **Collection vs item URL** — /flights (the whole collection: GET lists, POST creates) vs /flights/42 (one item: GET reads, PUT replaces, DELETE removes).
- **What nesting (/flights/42/passengers) is supposed to mean** — The child resource SCOPED to its parent - a testable contract, not just a naming convention. If it returns unscoped data, that's a real bug.
- **The fastest RPC-vs-REST tell** — Verbs living in the URL path itself (/getFlights, /processOrder) instead of the HTTP method supplying the verb - common in legacy/internal APIs, worth confirming against docs rather than assuming.
- **What query strings are for in REST style** — Filtering/sorting/pagination of the SAME resource - not changing what kind of thing is being returned.

### Challenge

Pick any API you have access to (BuggyAPI or a public one) and find one endpoint with path
nesting (two or more nouns in the URL, like /parent/{id}/child). Deliberately test whether the
nesting's implied scoping is actually enforced: create two parent resources with different children
under each, then request the nested child list for ONE parent and check whether any of the other
parent's children leak into the response.

### Ask the community

> This endpoint's URL is `[path]` using method `[method]`. Reading it noun-first, I'd expect it to mean `[your plain-words read]`. Does the actual documented/observed behavior match that reading, or is this API using a different convention I should know about before testing more of it?

Useful replies often point out whether the WHOLE API is consistently REST-style or a deliberate mix
(many real production APIs are) - that context changes what conventions you can safely assume hold
for the rest of your testing.

- [MDN — REST, glossary definition](https://developer.mozilla.org/en-US/docs/Glossary/REST)
- [restfulapi.net — REST API conventions and best practices reference](https://restfulapi.net/)
- [Marco Lenzo — REST APIs Explained in 5 MINUTES | What is a REST API?](https://www.youtube.com/watch?v=RrsRkXR5qaQ)

🎬 [Marco Lenzo — REST APIs Explained in 5 MINUTES | What is a REST API?](https://www.youtube.com/watch?v=RrsRkXR5qaQ) (5 min)

- REST is a style, not a technology - resources are nouns with their own URL, and the HTTP method supplies the verb.
- Collections (/flights) vs items (/flights/42): same noun, GET/POST/PUT/DELETE behave differently depending on which one you're addressing.
- Nesting (/flights/42/passengers) is a testable CONTRACT - scoping that isn't actually enforced server-side is a real, filable bug.
- Verbs living directly in the URL path (/getFlights, /processOrder) are the fastest tell of RPC-style rather than REST-style - common, and worth confirming against docs rather than assuming.
- Query strings filter/sort/paginate the same resource; if a parameter changes the fundamental SHAPE of what's returned, that's a design inconsistency worth flagging.


## Related notes

- [[Notes/api-testing-fundamentals/http-for-testers/http-methods|Methods (GET/POST/PUT/DELETE)]]
- [[Notes/api-testing-fundamentals/status-codes-and-rest/idempotency-and-safety|Idempotency & safety]]
- [[Notes/api-testing-fundamentals/status-codes-and-rest/reading-api-docs-and-swagger|Reading API docs & Swagger]]


---
_Source: `packages/curriculum/content/notes/api-testing-fundamentals/status-codes-and-rest/rest-in-plain-words.mdx`_
