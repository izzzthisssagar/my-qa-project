---
title: "Chaining findings"
tags: ["api-and-modern-security", "auditing-buggyapi", "track-c"]
updated: "2026-07-21"
---

# Chaining findings

*One domino falling barely moves the air. The same domino, lined up with nine others, topples the entire row. Two 'low severity' API findings, each harmless read in isolation, can tip into something genuinely serious the moment they're read together instead of one at a time.*

> A findings list with "IDOR on GET /users/{id} - exposes email address (low)" and "no rate limit on
> /password-reset (low)" filed as two separate, individually minor issues can hide the fact that
> combined, they enable an attacker to enumerate real email addresses and then hammer password resets
> against every single one - a genuinely serious attack that neither finding alone comes close to
> suggesting.

> **In real life**
>
> One domino tipped over on its own barely disturbs the air around it - a small, contained, almost
> uninteresting event. The exact same domino, positioned at the start of a carefully lined-up row, sets
> off a chain that ends somewhere far more dramatic than any single tile falling alone could ever produce.
> Security findings behave the same way: a minor information leak here, a missing rate limit there, each
> genuinely low-severity when judged in complete isolation - but positioned next to each other in the
> right order, they can tip into an attack path with real, serious consequence that reading each finding
> separately would never reveal.

**Chaining findings**: Chaining findings means deliberately examining multiple individually low- or medium-severity security findings together, specifically to check whether they combine into a more serious attack path than any single finding represents on its own - since the true severity of a vulnerability often depends on what else is reachable alongside it, not just its isolated technical description.

## The real severity question is "combined with what else," not just "how bad alone"

A finding judged purely in isolation answers an incomplete question. The more useful question, asked
deliberately after an audit surfaces multiple findings: does this finding, combined with any other
finding already on the list, unlock something worse than either one alone? An information disclosure
that reveals internal user IDs is mildly interesting alone; combined with a separate authorization
bypass that trusts a client-supplied user ID with no ownership check, the two together produce a
genuinely serious full account-data exposure path that neither finding's individual severity rating
would suggest on its own.

## Chaining requires deliberately revisiting the full findings list, not just moving forward

The natural flow of testing is linear - find something, note it, move to the next endpoint. Chaining
requires an explicit, separate pass: after a testing session produces multiple findings, deliberately
lay them out together and ask, for each pair or small group, whether one enables or amplifies another.
This doesn't happen automatically as a side effect of finding things one at a time - it requires
setting aside dedicated time specifically to look backward across everything found so far, not just
forward to the next untested endpoint.

> **Tip**
>
> When two findings look like they might chain, write out the actual attacker's step-by-step path
> explicitly - "attacker does X using finding A, which enables Y using finding B, resulting in Z." A
> chain that can't be stated as a concrete sequence of real steps probably isn't a genuine chain yet.

> **Common mistake**
>
> Filing every finding at its technically-correct isolated severity without ever explicitly checking for
> combinations, then being surprised when a "low + low" pair turns out to represent a real, exploitable
> critical path. The chaining check is a distinct, deliberate step - it doesn't happen by accident just
> from finding enough issues.

![A row of dominoes captured mid-fall, toppling in sequence](chaining-findings.jpg)
*Dominoes falling — Kurt:S, CC BY 2.0, via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Dominoes_falling.jpg)*
- **The first domino, already fallen** — One finding, judged alone - genuinely minor on its own, the same way a single fallen tile barely disturbs anything by itself.
- **The domino mid-tip, caught in the act of toppling the next** — The exact moment one finding enables the next - the deliberate chaining question: does this specific finding unlock or amplify another one already on the list?
- **The still-standing dominoes further down the row** — The full consequence not yet realized - the serious combined impact a chain can produce, invisible if only the first tile is ever examined in isolation.
- **The straight, deliberately arranged line connecting every tile** — Not a coincidence - a specific, deliberate arrangement. The same deliberate work chaining findings actually requires: explicitly laying results out together, not just noting each one and moving on.

**Checking a findings list for real chains**

1. **Lay out every finding from the session together** — A dedicated, separate pass - not a side effect of moving linearly from endpoint to endpoint.
2. **For each pair, ask what one finding gives access to that the other needs** — Does an information leak supply exactly the missing piece another finding's exploit path requires?
3. **Write the combined attack as a concrete, real step-by-step sequence** — If it can't be stated as real, ordered actor steps, it's probably not a genuine chain yet.
4. **Re-rate the combined chain's severity separately from each individual finding** — The chain's severity can be, and often is, meaningfully higher than any single link in it.

*Checking whether two findings' data flow actually chains (Python)*

```python
finding_a = {
    "id": "F-01",
    "desc": "GET /users/{id} leaks internal numeric user IDs to any authenticated user",
    "provides": {"internal_user_id"},
}
finding_b = {
    "id": "F-02",
    "desc": "GET /bookings?userId={id} returns any user's bookings with no ownership check",
    "requires": {"internal_user_id"},
}

def check_chain(a, b):
    overlap = a["provides"] & b["requires"]
    return overlap

overlap = check_chain(finding_a, finding_b)
if overlap:
    print("CHAIN CONFIRMED: " + finding_a["id"] + " supplies " + str(overlap) +
          " which " + finding_b["id"] + " requires to exploit")
    print("Combined impact: any authenticated user can enumerate and read every user's bookings")
else:
    print("No confirmed chain between these two findings")
```

*Checking whether two findings' data flow actually chains (Java)*

```java
import java.util.*;

public class Main {
    static class Finding {
        String id, desc;
        Set<String> provides = new HashSet<>();
        Set<String> requires = new HashSet<>();
    }

    public static void main(String[] args) {
        Finding a = new Finding();
        a.id = "F-01";
        a.desc = "GET /users/{id} leaks internal numeric user IDs to any authenticated user";
        a.provides.add("internal_user_id");

        Finding b = new Finding();
        b.id = "F-02";
        b.desc = "GET /bookings?userId={id} returns any user's bookings with no ownership check";
        b.requires.add("internal_user_id");

        Set<String> overlap = new HashSet<>(a.provides);
        overlap.retainAll(b.requires);

        if (!overlap.isEmpty()) {
            System.out.println("CHAIN CONFIRMED: " + a.id + " supplies " + overlap +
                    " which " + b.id + " requires to exploit");
            System.out.println("Combined impact: any authenticated user can enumerate and read every user's bookings");
        } else {
            System.out.println("No confirmed chain between these two findings");
        }
    }
}
```

### Your first time: Run a real chaining pass on an existing findings list

- [ ] Gather at least two or three real findings from a prior BuggyAPI testing session — Even individually minor ones - those are exactly the candidates worth checking.
- [ ] For each pair, write what the first finding reveals or provides — Data, an identifier, an access path - stated concretely.
- [ ] Write what the second finding would need to actually be exploited — Check explicitly whether the first finding happens to supply it.
- [ ] If a real chain exists, write the full attacker path as concrete numbered steps — Confirm each step is a real, specific action, not a vague gesture at 'combining' the two.

- **A findings report lists several low-severity issues with no mention of whether any combine into something worse.**
  Run an explicit chaining pass as a distinct step after the initial testing session - it doesn't happen automatically just from finding multiple issues, it requires deliberately laying them out together.
- **Two findings seem like they might chain but the actual combined attack is hard to state concretely.**
  Write out the literal attacker steps in order - if a real, specific sequence can't be constructed, the chain may not be genuine yet, or a missing piece hasn't been found.
- **A chain is identified but reported at the same severity as its weakest individual link.**
  Re-rate the combined chain's severity on its own merits - a chain's real-world impact is often meaningfully higher than any single finding in it, and should be reported that way explicitly.

### Where to check

- Any findings list with more than one entry, checked with a dedicated, explicit chaining pass before finalizing severity ratings.
- Findings that individually reveal identifiers, tokens, or access paths, checked specifically against other findings that might consume exactly that information.
- [[api-and-modern-security/auditing-buggyapi/a-repeatable-audit-checklist]] for the systematic process that reliably surfaces the individual findings a chaining pass then examines together.
- [[api-and-modern-security/auditing-buggyapi/the-write-up-like-a-real-report]] for how a confirmed chain gets communicated clearly and convincingly in a real report.
- [[api-and-modern-security/jwt-and-token-attacks/scope-and-audience-abuse]] for a specific token-related finding type that frequently chains with an authorization-bypass finding elsewhere.

### Worked example: two low-severity findings that chained into a real account-takeover path

1. A BuggyAPI audit produces two separate findings, each initially filed as low severity: an endpoint
   that leaks a user's internal numeric ID in a public-facing response, and a separate password-reset
   endpoint with no rate limiting.
2. Filed independently, neither finding looks especially serious - an internal ID leak alone isn't
   directly exploitable, and a missing rate limit alone just means reset requests could theoretically be
   sent repeatedly.
3. A deliberate chaining pass asks the explicit question: does the leaked ID provide anything the
   rate-limit finding's exploit path needs? It does - the password-reset endpoint, it turns out, accepts
   the same internal user ID directly rather than an email address.
4. The combined, concretely stated attack: enumerate internal user IDs via the first finding, then
   hammer unrate-limited password-reset requests against each one via the second - a real, viable path
   toward account takeover at scale.
5. The write-up reports this explicitly as a chained critical finding, referencing both original low
   findings as its components, rather than leaving two separately-filed low-severity issues that
   understate the real combined risk.

**Quiz.** According to this note, why doesn't chaining happen automatically just from finding multiple individual issues during testing?

- [ ] It does happen automatically - no additional step is needed once enough findings exist
- [x] Testing naturally moves forward linearly from endpoint to endpoint, so recognizing that two separate findings combine requires a deliberate, dedicated pass that explicitly looks backward across the full findings list together, not just forward to the next untested endpoint
- [ ] Chaining only applies to findings discovered on the exact same endpoint
- [ ] Automated scanning tools always catch chains, making a manual pass unnecessary

*The natural flow of testing is linear - find something, note it, move to the next endpoint - which means recognizing that two separate findings combine into something worse requires an explicit, separate step: deliberately laying the full findings list out together and asking, for each pair, whether one enables or amplifies another. This doesn't happen as an automatic side effect of simply finding enough individual issues.*

- **Chaining findings** — Deliberately examining multiple individually low- or medium-severity findings together to check whether they combine into a more serious attack path than any single finding represents alone.
- **The real severity question chaining asks** — Not just 'how bad is this finding alone' but 'combined with what else on this list' - since true severity often depends on what else is reachable alongside a given finding.
- **Why a chaining pass has to be deliberate and separate** — Testing naturally flows forward, endpoint to endpoint - recognizing a chain requires explicitly looking backward across the full findings list together, which doesn't happen automatically.
- **How to confirm a chain is real, not just plausible** — Write out the full attacker path as concrete, ordered steps - if a specific real sequence can't be constructed, the chain likely isn't confirmed yet.

### Challenge

Gather two or three real findings from a past BuggyAPI testing session, even minor ones. For each pair, check explicitly whether one supplies something the other needs, and write out any real chain as a concrete step-by-step attacker path.

- [PortSwigger Web Security Academy — Business Logic Vulnerabilities](https://portswigger.net/web-security/logic-flaws)
- [HackerOne — Knowledge Center](https://www.hackerone.com/knowledge-center)
- [This 'Low' Vulnerability Became CRITICAL | Vux06](https://www.youtube.com/watch?v=4AXBn-LuXJA)

🎬 [This 'Low' Vulnerability Became CRITICAL | Vux06](https://www.youtube.com/watch?v=4AXBn-LuXJA) (5 min)

- Two individually low-severity findings can combine into a genuinely serious attack path - true severity often depends on what else is reachable alongside a finding.
- Chaining requires a deliberate, separate pass looking backward across the full findings list - it doesn't happen automatically from testing forward.
- A real chain can be stated as a concrete, ordered sequence of actual attacker steps - if it can't, it may not be confirmed yet.
- Rate a confirmed chain's severity on its own merits, separately from any single finding within it - the combined impact is often meaningfully higher.
- Ask explicitly, for every finding: what does this provide, and does anything else on the list need exactly that?


## Related notes

- [[Notes/api-and-modern-security/auditing-buggyapi/a-repeatable-audit-checklist|A repeatable audit checklist]]
- [[Notes/api-and-modern-security/auditing-buggyapi/the-write-up-like-a-real-report|The write-up (like a real report)]]
- [[Notes/api-and-modern-security/jwt-and-token-attacks/scope-and-audience-abuse|Scope & audience abuse]]


---
_Source: `packages/curriculum/content/notes/api-and-modern-security/auditing-buggyapi/chaining-findings.mdx`_
