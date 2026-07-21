---
title: "Threat-modeling an API"
tags: ["api-and-modern-security", "auditing-buggyapi", "track-c"]
updated: "2026-07-21"
---

# Threat-modeling an API

*A locksmith legally allowed to test a lock still starts by asking what it protects and who might want in - not by picking it first and thinking later. Threat-modeling an API means asking that same question before a single request is sent: what's actually at stake here, and along which paths.*

> Opening an API's documentation and immediately firing requests at every endpoint feels productive, but
> it's the security-testing equivalent of trying every key on a ring before checking which door actually
> matters. Threat modeling comes first specifically because it answers a question testing alone can't:
> out of everything this API touches, what would actually hurt if it broke?

> **In real life**
>
> A locksmith legally engaged to assess a building's security doesn't start by picking the first lock he
> finds - he starts by walking the perimeter, asking what's actually stored behind each door, which
> entrances see the most traffic, and which locks look old enough to already be a known weak point. Only
> then does the actual testing begin, aimed specifically at the doors that matter most. An API deserves
> the same discipline before any request is sent: understanding what data and actions each endpoint
> actually controls, before spending testing time equally across all of them regardless of what's really
> at stake.

**Threat-modeling an API**: Threat-modeling an API means systematically identifying what data and actions each endpoint controls, who should and shouldn't be able to reach them, and which paths would cause the most damage if compromised - done before active testing begins, specifically so testing effort concentrates on what actually matters rather than spreading evenly across everything.

## Map assets and actors before touching a single endpoint

The first real question isn't "does this endpoint have a bug" - it's "what does this endpoint actually
control, and who is supposed to be able to reach it." For BuggyAPI specifically, that means walking the
documented endpoints and explicitly noting what each one touches: user account data, flight bookings,
payment-adjacent fields, admin-only operations - and which roles (anonymous, authenticated user, admin)
should legitimately be able to reach each one. This map, built before any active probing, is what turns
"test everything equally" into "test the endpoints that would actually matter if broken" first.

## Rank by impact, not by how interesting an endpoint looks

A tester's instinct often gravitates toward whatever endpoint looks most technically interesting to
poke at - a complex query parameter, an unusual header. Threat modeling deliberately overrides that
instinct with a more disciplined question: if this specific endpoint were fully compromised, what's the
actual blast radius? An endpoint controlling account password resets or payment-adjacent data ranks
above one controlling a cosmetic display preference, regardless of which one happens to look more
technically curious to test first - the ranking should come from real consequence, not from what's most
fun to poke at.

> **Tip**
>
> Write the threat model down as a real, visible document before testing starts - even a simple table of
> endpoint, data touched, and legitimate access level. A threat model that stays only in someone's head
> is easy to quietly drift away from once active testing gets underway.

> **Common mistake**
>
> Skipping straight to active testing because the target "seems simple enough to just know." Even a
> genuinely small API benefits from the explicit exercise - the value isn't just in the final list, it's
> in the deliberate act of asking the question for every endpoint rather than trusting an unexamined
> gut sense of what matters most.

![An 1877 street photograph of a locksmith working at his tool cart surrounded by hanging keys and tools](threat-modeling-an-api.jpg)
*The Street Locksmith, 1877 — LSE Library, No known restrictions, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:The_Street_Locksmith_(6899206616).jpg)*
- **The array of keys and tools hanging above the cart** — The full attack surface, laid out and visible before any single lock gets touched - the same explicit inventory a threat model builds of every endpoint before active testing begins.
- **The locksmith's hands, focused on one specific piece of work** — Deliberate, targeted effort on one thing at a time - the payoff of threat modeling: testing concentrated on what was identified as mattering most, not spread evenly across everything.
- **The uniformed figure at the frame's edge** — A visible reminder of lawful, authorized boundaries around this work - the same authorization boundary that makes testing BuggyAPI (an intentionally vulnerable, permitted target) legitimate in the first place.
- **The child watching from the side** — An observer with no role in the actual work - a reminder that a threat model should stay focused on real, in-scope assets and actors, not get distracted by everything simply visible nearby.

**Building a threat model before testing an API**

1. **List every documented endpoint** — The full, explicit inventory - nothing assumed, nothing skipped because it seems minor.
2. **Note what data or action each endpoint actually controls** — Account data, financial fields, admin operations, or something genuinely low-stakes - stated explicitly per endpoint.
3. **Note which roles should legitimately reach each one** — Anonymous, authenticated user, admin - the expected access boundary for each endpoint.
4. **Rank by real impact if compromised, not by technical interest** — Concentrate testing effort on what would actually hurt most, not on whatever looks most fun to poke at first.

*Ranking endpoints by threat-model impact before testing (Python)*

```python
endpoints = [
    {"path": "/users/{id}/password-reset", "data": "account credentials", "impact": 9},
    {"path": "/flights/search", "data": "public flight listings", "impact": 2},
    {"path": "/bookings/{id}/payment-details", "data": "payment-adjacent data", "impact": 10},
    {"path": "/users/{id}/display-preferences", "data": "cosmetic UI setting", "impact": 1},
]

ranked = sorted(endpoints, key=lambda e: e["impact"], reverse=True)

print("Testing priority (highest real impact first):")
for e in ranked:
    print("  " + e["path"] + " (" + e["data"] + ") -> impact " + str(e["impact"]))
```

*Ranking endpoints by threat-model impact before testing (Java)*

```java
import java.util.*;

public class Main {
    static class Endpoint {
        String path, data; int impact;
        Endpoint(String path, String data, int impact) {
            this.path = path; this.data = data; this.impact = impact;
        }
    }

    public static void main(String[] args) {
        List<Endpoint> endpoints = new ArrayList<>();
        endpoints.add(new Endpoint("/users/{id}/password-reset", "account credentials", 9));
        endpoints.add(new Endpoint("/flights/search", "public flight listings", 2));
        endpoints.add(new Endpoint("/bookings/{id}/payment-details", "payment-adjacent data", 10));
        endpoints.add(new Endpoint("/users/{id}/display-preferences", "cosmetic UI setting", 1));

        endpoints.sort((a, b) -> b.impact - a.impact);

        System.out.println("Testing priority (highest real impact first):");
        for (Endpoint e : endpoints) {
            System.out.println("  " + e.path + " (" + e.data + ") -> impact " + e.impact);
        }
    }
}
```

### Your first time: Build a real threat model for BuggyAPI

- [ ] List every documented BuggyAPI endpoint from its OpenAPI docs — The full set, not just the ones that seem obviously interesting.
- [ ] For each one, write one line on what data or action it actually controls — Be specific - 'user data' is weaker than 'user email and password hash.'
- [ ] Note the intended access level for each - anonymous, authenticated user, or admin — This becomes the baseline every access-control test later checks against.
- [ ] Rank the full list by real impact if fully compromised — Confirm the ranking reflects actual consequence, not which endpoint looks most technically interesting.

- **A testing pass covers every endpoint equally but still misses the highest-impact bug.**
  A sign testing effort wasn't actually weighted by a real threat model - rebuild the impact ranking explicitly and concentrate re-testing on the highest-consequence endpoints first.
- **Significant time gets spent deeply probing an endpoint that turns out to control something low-stakes.**
  Revisit the threat model before continuing - technical interest and real impact aren't the same thing, and the ranking exists specifically to catch this kind of misallocated effort.
- **A threat model exists but testing seems to have drifted away from it over time.**
  Keep the threat model as a visible, referenced document throughout testing, not a one-time exercise done once and set aside - revisit it explicitly as new endpoints or findings emerge.

### Where to check

- Any new testing effort against BuggyAPI, confirmed to start from an explicit, written endpoint-and-impact map before active probing begins.
- Testing time actually spent, checked periodically against the impact ranking to confirm effort matches real consequence.
- [[api-and-modern-security/auditing-buggyapi/a-repeatable-audit-checklist]] for the structured process a threat model feeds directly into.
- [[api-and-modern-security/owasp-api-security-top-10-2023/bola-and-bfla]] for the specific access-control risk category a threat model's role mapping is most directly checking against.
- [[api-and-modern-security/auditing-buggyapi/chaining-findings]] for how a threat model's impact ranking helps recognize when two separate findings combine into something more serious.

### Worked example: a threat model that redirected testing toward the finding that actually mattered

1. A tester begins auditing BuggyAPI by testing endpoints roughly in the order they appear in the
   documentation, starting with a complex flight-search filtering endpoint that looks technically
   interesting.
2. After building an explicit threat model instead, the `/bookings/{id}/payment-details` endpoint is
   identified as by far the highest-impact target - payment-adjacent data, intended to be accessible
   only to the booking's own owner.
3. Testing is redirected specifically toward that endpoint's access controls first, ahead of the
   originally-planned flight-search work.
4. This surfaces a real IDOR: the endpoint returns another user's payment-adjacent data when the booking
   ID in the URL is simply changed, with no ownership check performed server-side.
5. The flight-search endpoint, tested afterward per the original plan, turns out to have no meaningful
   issues - the threat model's ranking correctly predicted where the real risk actually was before any
   testing time was spent finding out the hard way.

**Quiz.** According to this note, what does threat modeling accomplish that jumping straight into active testing doesn't?

- [ ] It replaces the need for any active testing afterward
- [x] It concentrates testing effort on what would actually cause the most damage if compromised, rather than spreading effort evenly across endpoints or following technical curiosity toward whatever looks most interesting to poke at first
- [ ] It automatically finds all the bugs before testing even begins
- [ ] It's only useful for very large, complex APIs and adds no value for a small one

*Threat modeling doesn't replace active testing - it directs it. Without an explicit model, testing effort tends to either spread evenly across every endpoint regardless of real stakes, or gravitate toward whatever looks most technically interesting. Ranking endpoints by actual impact first, before testing begins, is what concentrates limited testing time on the paths that would genuinely matter if something went wrong.*

- **Threat-modeling an API** — Systematically identifying what data and actions each endpoint controls, who should reach them, and which paths matter most if compromised - done before active testing to direct effort where it counts.
- **Why rank by real impact, not technical interest** — An endpoint controlling account credentials or payment data matters more if compromised than one controlling a cosmetic setting, regardless of which one looks more technically interesting to probe.
- **Why write the threat model down explicitly** — A model that stays only in someone's head is easy to quietly drift away from once active testing gets underway - a visible document keeps testing effort anchored to the real priorities.
- **The core question a threat model answers before testing** — Out of everything this API touches, what would actually hurt if it broke - answered explicitly, per endpoint, before spending equal testing time everywhere.

### Challenge

Pick any API you have authorized access to test (BuggyAPI, or another permitted target). Build a real threat model: list every endpoint, what it controls, its intended access level, and rank the full list by real impact if compromised - before testing anything.

- [OWASP — Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [OWASP Cheat Sheet Series — Threat Modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [What is Threat Modeling and Why Is It Important? | CBT Nuggets](https://www.youtube.com/watch?v=h_BC6QMWDbA)

🎬 [What is Threat Modeling and Why Is It Important? | CBT Nuggets](https://www.youtube.com/watch?v=h_BC6QMWDbA) (6 min)

- Threat modeling comes before active testing - it directs where limited testing effort actually goes, rather than replacing the testing itself.
- Map every endpoint's real data and actions, and its intended access level, before probing anything.
- Rank endpoints by genuine impact if compromised, not by which one looks most technically interesting to test first.
- Write the threat model down as a visible document - an unwritten model is easy to drift away from once testing gets underway.
- Even a genuinely small API benefits from the explicit exercise - the discipline of asking the question matters as much as the resulting list.


## Related notes

- [[Notes/api-and-modern-security/auditing-buggyapi/a-repeatable-audit-checklist|A repeatable audit checklist]]
- [[Notes/api-and-modern-security/owasp-api-security-top-10-2023/bola-and-bfla|BOLA & BFLA]]
- [[Notes/api-and-modern-security/auditing-buggyapi/chaining-findings|Chaining findings]]


---
_Source: `packages/curriculum/content/notes/api-and-modern-security/auditing-buggyapi/threat-modeling-an-api.mdx`_
