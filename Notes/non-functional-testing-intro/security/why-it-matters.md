---
title: "Why it matters"
tags: ["non-functional-testing-intro", "security", "track-c"]
updated: "2026-07-18"
---

# Why it matters

*Security is the dimension where 'it works' and 'it's safe' are different claims. A feature can pass every functional test and still hand a stranger someone else's data — correctness asks 'does the right thing happen?', security asks 'what WRONG thing can be made to happen?'*

> The invoice page works. You tested it: log in, click "My invoices", see your invoices, correct
> totals, PDF downloads. Ship it. Then a customer emails support: they changed the number at the end
> of the URL — `/invoices/4012` to `/invoices/4011` — out of idle curiosity, and they're now looking
> at a stranger's invoice. Name, address, amount, all of it. Nothing "broke": the page did exactly
> what it was built to do — fetch invoice 4011 and render it beautifully. It just never asked the one
> question functional testing never thinks to ask: *is this the person allowed to see 4011?* Every
> functional test still passes. The company now has a data breach, a disclosure obligation, and a
> very bad week. That gap — between "does the right thing happen for the right user?" and "can a wrong
> user make the right thing happen for them?" — is the entire reason security testing exists.

> **In real life**
>
> A bank vault is the clearest picture of what "secure" means and why functional testing can't see
> it. A functional test of the vault asks: does the door open for the manager with the right
> combination, and close again? Yes — flawless. But that's not what makes it a vault. What makes it a
> vault is everything designed against an ADVERSARY: 22 tons of drill-resistant steel, time locks so
> it can't be opened at gunpoint at 2am, a day-gate so the open door still isn't an open door. None of
> that shows up in "does it open for the manager?" You could build a beautiful door that opens and
> closes perfectly and is made of plywood — every functional test green, and a screwdriver defeats it.
> Security is the plywood-versus-steel question, and it is invisible to anyone only checking that the
> door opens.

**Security testing**: Security testing evaluates whether a system protects data and functionality against MISUSE — deliberate, adversarial, rule-breaking use — rather than whether it behaves correctly under honest use. The defining property: security is independent of functional correctness. A feature can be 100% functionally correct (right output, right user, happy path) and still be insecure, because insecurity lives in the paths the happy-path user never takes: requesting another user's record by changing an ID, submitting input crafted to change a query's meaning, reaching an admin action without being an admin, reading a password that should never have been stored readable. Where functional testing asks 'does the right thing happen?', security testing asks the adversary's question: 'what wrong thing can I MAKE happen?' The consequences also differ in kind — a functional bug annoys one user; a security bug can expose every user at once, carries legal and financial weight (breach disclosure, fines, lost trust), and is often exploited silently, discovered only after the damage.

## Why "it works" and "it's safe" are different questions

- **Correctness is about the honest user; security is about the dishonest one.** Functional tests
  are written from the happy path: a real user doing real things. Attackers don't use the happy
  path — they change the URL, replay the request after logging out, paste a payload where you
  expected a name. The bug lives exactly where your functional tests don't look, by design.
- **A security bug scales the way a functional bug never does.** A broken "sort by date" button
  inconveniences whoever clicks it. A broken access-control check exposes *every* record to
  *anyone* who guesses an ID. One is a support ticket; the other is a headline, a regulator's
  letter, and a mandatory breach notification to a few million people.
- **Insecurity is usually silent.** A crashing feature announces itself. A leak doesn't — the app
  keeps working perfectly while quietly serving data to the wrong people, and you find out from a
  security researcher, a customer, or a criminal, months later. "No error, no complaint" is not
  evidence of safety; it's the normal condition of an exploited system.
- **Security is a property of the whole system, not one screen.** The invoice page was fine; the
  MISSING ownership check was the bug — an absence, not a presence. Security defects are
  disproportionately things that *should be there and aren't*: the check nobody wrote, the field
  nobody escaped, the endpoint nobody protected because "the UI never calls it that way."
- **"The UI never lets you do that" is the most expensive sentence in software.** The UI is a
  suggestion, not a boundary. Anyone can send any request with tools you already know (browser
  DevTools, curl, Postman). Every protection that lives only in the front end — a hidden field, a
  disabled button, a client-side price — is already defeated the moment someone opens the network
  tab. Real security lives on the server, and the server is what has to be tested.
- **Even manual testers own a real slice of this.** You won't write exploits, but you can change an
  ID to one you don't own, resubmit a form after logging out, and ask "who's allowed to call this,
  and where is that enforced?" in refinement. Those three habits catch a startling share of the
  most common, most damaging bugs — the demo in this note is exactly one of them.

> **Tip**
>
> The single most productive security question a tester can ask about any feature: "What could a
> malicious user do here that a normal user wouldn't?" Point it at every screen — can I see data
> that isn't mine, do something I shouldn't be allowed to, reach a step out of order, put unexpected
> input somewhere it's trusted? You don't need tools or a security title to ask it; you need the
> willingness to stop being the honest user for five minutes and start being the adversary.

> **Common mistake**
>
> Treating "all functional tests pass" as evidence the feature is secure. They measure different,
> independent things: functional tests confirm the door opens for the manager; they say nothing about
> whether it's steel or plywood. The demo below is a login-and-fetch that is 100% functionally correct
> — right user sees right data, wrong password rejected — and simultaneously leaks every account's
> data to anyone who edits one number, because the ownership check was never written. Green functional
> suite, open vault. The two verdicts have to be earned separately.

![An open bank vault: a huge circular steel door with concentric locking bolts and gears on the right, a barred inner gate and safe-deposit boxes visible through the doorway on the left](why-it-matters.jpg)
*Winona Savings Bank vault door — Jonathunder, Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:WinonaSavingsBankVault.JPG)*
- **The spec plate — the promise made against an ADVERSARY** — '22 1/2 tons, 22 inches, 11 layers drill-resistant, 4 time locks.' None of this is about opening for the manager — every number is a defense against someone actively trying to get in. Security requirements read like this: not 'works for users' but 'resists attackers'. If your app has no such list, that absence is finding number one.
- **The bolt-work and gears — defense in depth** — Not one lock — dozens of bolts, multiple independent time locks, layered steel. If one fails, others hold. Secure systems are the same: auth AND access checks AND input validation AND encryption AND logging, so a single missing control isn't game over. The invoice bug was one missing bolt in a door with only one bolt.
- **The inner day-gate — the open door that still isn't open** — Even with the vault door swung wide, the barred gate means 'open' doesn't equal 'walk in and take anything'. That's authorization AFTER authentication: logging in gets you through the outer door; each thing you then try to touch still needs its own check. The leaked invoice skipped the gate — logged-in was treated as allowed-everything.
- **The safe-deposit boxes — every user's data, separately owned** — One vault, many boxes, each belonging to a different person and none openable with a neighbor's key. Your database is this: every user's rows sharing one store, each meant to be reachable only by its owner. 'Change 4012 to 4011 and read it' is opening a box that isn't yours — the exact failure this whole image argues against.
- **The threshold — where the plywood-vs-steel question gets asked** — A functional test stops at 'the door opens and closes'. Security testing steps over the threshold and asks what a thief would ask: what's it made of, what happens after hours, can I reach a box that isn't mine? Same door, a completely different set of questions — and only the second set is security.

**One feature, functionally perfect and wide open — press Play**

1. **Functional test: log in as Alice, open 'My invoice', see Alice's invoice. PASS** — Correct user, correct data, correct total, clean PDF. Every acceptance criterion met. The team ships with a green suite and a clear conscience.
2. **An attacker (or a curious user) changes the URL: /invoices/4012 → /invoices/4011** — No hacking tools — just editing a number in the address bar. The server receives a valid, logged-in request for invoice 4011 and does exactly what it was built to do: fetch and render invoice 4011.
3. **The page loads someone else's invoice. Name, address, amount — all of it** — Nothing errored. There was no ownership check between 'you are logged in' and 'here is the record', so 'logged in as anyone' became 'allowed to read everything'. The functional suite, re-run right now, is still green.
4. **Security testing exists to send request #2 before the customer does** — The whole discipline is: don't only test as the honest user. Log in as Alice, then deliberately ask for Bob's ID and confirm you're refused. Same code, two verdicts — functionally perfect, catastrophically insecure — and now you know on Tuesday, not from a breach notice.

Here's the whole idea in runnable form — a login-and-fetch that passes its functional test and
leaks every record, next to the one-line fix that closes it:

*Run it — functionally correct, and leaking every account (Python)*

```python
# A tiny "invoices" store. Two users, each owns one invoice.
INVOICES = {
    4011: {"owner": "bob",   "amount": "920", "email": "bob@example.com"},
    4012: {"owner": "alice", "amount": "140", "email": "alice@example.com"},
}

def fmt(inv):
    if inv is None:
        return "None"
    return "owner=" + inv["owner"] + " amount=" + inv["amount"] + " email=" + inv["email"]

def get_invoice_INSECURE(logged_in_user, invoice_id):
    # Looks fine. Fetches the invoice and returns it. No ownership check.
    return fmt(INVOICES.get(invoice_id))

def get_invoice_SECURE(logged_in_user, invoice_id):
    inv = INVOICES.get(invoice_id)
    if inv is None:
        return "None"
    if inv["owner"] != logged_in_user:          # the check that was missing
        return "403 Forbidden - not your invoice"
    return fmt(inv)

print("FUNCTIONAL TEST (the happy path both versions pass):")
print("  Alice opens her own invoice 4012:")
print("   insecure:", get_invoice_INSECURE("alice", 4012))
print("   secure  :", get_invoice_SECURE("alice", 4012))
print("  -> identical, correct, PASS. Ship it?")
print()
print("SECURITY TEST (the request functional tests never send):")
print("  Alice edits the URL and asks for Bob's invoice 4011:")
print("   insecure:", get_invoice_INSECURE("alice", 4011), " <- Bob's data. LEAK.")
print("   secure  :", get_invoice_SECURE("alice", 4011))
print()
print("Same feature. The functional suite cannot tell these two apart -")
print("only the adversary's request can. 'It works' and 'it's safe' are")
print("different questions, and each one has to be asked on purpose.")
```

The identical point in Java — one missing check between a green suite and a breach:

*Run it — functionally correct, and leaking every account (Java)*

```java
import java.util.*;

public class Main {
    static Map<Integer, Map<String, String>> invoices = new HashMap<>();

    static Map<String, String> inv(String owner, String amount, String email) {
        Map<String, String> m = new HashMap<>();
        m.put("owner", owner); m.put("amount", amount); m.put("email", email);
        return m;
    }

    static String fmt(Map<String, String> i) {
        if (i == null) return "None";
        return "owner=" + i.get("owner") + " amount=" + i.get("amount") + " email=" + i.get("email");
    }

    static String getInsecure(String user, int id) {
        return fmt(invoices.get(id));                 // no ownership check
    }

    static String getSecure(String user, int id) {
        Map<String, String> i = invoices.get(id);
        if (i == null) return "None";
        if (!i.get("owner").equals(user))            // the check that was missing
            return "403 Forbidden - not your invoice";
        return fmt(i);
    }

    public static void main(String[] args) {
        invoices.put(4011, inv("bob", "920", "bob@example.com"));
        invoices.put(4012, inv("alice", "140", "alice@example.com"));

        System.out.println("FUNCTIONAL TEST (the happy path both versions pass):");
        System.out.println("  Alice opens her own invoice 4012:");
        System.out.println("   insecure: " + getInsecure("alice", 4012));
        System.out.println("   secure  : " + getSecure("alice", 4012));
        System.out.println("  -> identical, correct, PASS. Ship it?");
        System.out.println();
        System.out.println("SECURITY TEST (the request functional tests never send):");
        System.out.println("  Alice edits the URL and asks for Bob's invoice 4011:");
        System.out.println("   insecure: " + getInsecure("alice", 4011) + "  <- Bob's data. LEAK.");
        System.out.println("   secure  : " + getSecure("alice", 4011));
        System.out.println();
        System.out.println("Same feature. The functional suite cannot tell these two apart -");
        System.out.println("only the adversary's request can. 'It works' and 'it's safe' are");
        System.out.println("different questions, and each one has to be asked on purpose.");
    }
}
```

### Your first time: Your mission: run one authorized access-control probe, no special tools required

- [ ] Get written authorization and prepare two tester-owned accounts with synthetic records — Use only a local, test, or training environment covered by the rules of engagement. Never use production, third-party systems, or guessed real-user identifiers; stop immediately if real data appears.
- [ ] Log in as test account A and find its seeded record identifier — An invoice, order, message, profile, or document works. Record A's ID and the known ID of test account B's synthetic record.
- [ ] While logged in as A, request B's known synthetic identifier — This tests the same ownership boundary without touching a stranger's data. Use one request as minimal proof; do not enumerate IDs.
- [ ] Look hard at what comes back — A '403 Forbidden', scoped not-found response, or redirect is evidence the ownership check exists. If test account B's synthetic record appears for A, stop after that one minimal proof and file the broken-access-control finding.
- [ ] Write it up as a security finding, not a curiosity — 'Logged in as user A, requesting resource B (owned by another user) via URL returns B's data — no ownership check.' Attach the two URLs and what you saw. That report gets a serious bug fixed before it becomes a breach.

You just did real security testing — adversarial, server-side, high-impact — using nothing but the
address bar and the decision to stop testing as the honest user for one minute.

- **Every functional test passes, but you can see another user's data by changing an ID.**
  This is broken access control (IDOR), and passing functional tests is expected — they only ever request YOUR data, so the missing ownership check is invisible to them. The fix lives on the server: every request that fetches a record by identifier must verify the logged-in user is allowed that specific record, on every endpoint, not just the ones the UI calls. Test it the only way it shows up: log in as one user and deliberately request another's identifiers.
- **'You can't do that in the UI — the button's hidden for non-admins', so no one tested it.**
  Hiding a button hides it from honest users, not from attackers, who send the request directly with DevTools or curl regardless of what the UI shows. A hidden or disabled control is a usability choice, never a security control. Test the ACTION, not the button: replay the admin request as a normal user and confirm the SERVER refuses it. If protection exists only in the front end, it doesn't exist.
- **A security issue was dismissed because 'there's no error and nothing crashes'.**
  Silence is the normal state of an insecure system, not evidence of safety — a leak serves data perfectly while leaking. Security verdicts can't be read off crash logs; they require deliberately attempting the misuse (wrong user, wrong ID, tampered request, unexpected input) and checking whether it was PREVENTED. 'It didn't error' answers a functional question; 'it refused the attack' answers the security one.
- **Security is treated as 'the security team's job', so it never enters the test plan.**
  Specialists do the deep work (pen tests, threat modeling), but the highest-frequency bugs — IDOR, missing authorization, unescaped input, client-side-only checks — surface from ordinary testing done adversarially, and testers are positioned to catch them earliest and cheapest. Add a few security probes to normal test design: 'what if a different user did this? what if I sent this without logging in? what if the input is hostile?' It doesn't replace specialists; it stops the easy bugs from ever reaching them.

### Where to check

- **The address bar and any identifier in it** — IDs in URLs, query strings, and path segments are the first place to probe access control: change one to a value you don't own and see if the server refuses. The cheapest high-value security test there is.
- **Browser DevTools → Network tab** — shows the real requests behind the UI; replay one after logging out, or as a different user, to test whether the SERVER enforces what the interface merely suggests. This is where 'the UI won't let you' gets disproven.
- **Anywhere your input is later shown or stored** — search boxes, names, comments, profile fields: input that comes back out is where injection and scripting bugs live (see [[non-functional-testing-intro/security/common-risks]]).
- **The login/logout boundary** — resubmit an action after logging out, or with an old session; a well-built app rejects it, a leaky one honors it. Session handling is quietly one of the most bug-prone areas.
- **[[non-functional-testing-intro/security/a-testers-role]]** — how to fold these probes into ordinary test design so they happen every sprint, not just when a specialist visits.

### Worked example: the profile page that passed every test and exposed 50,000 accounts

1. A team ships a user-profile page: `/account/profile?uid=8842`. Functional testing is thorough —
   the right user sees the right profile, edits save, validation works, the avatar uploads. Full
   green. Everyone signs off.
2. A tester, adding one adversarial habit to the plan, stays logged in as their own account and
   changes `uid=8842` to `uid=8841`. The page cheerfully renders a stranger's profile: full name,
   email, phone, home address. No error, no warning — the server fetched profile 8841 exactly as
   built, because nothing checked that 8842 was the caller's own uid.
3. The tester escalates the finding correctly: this isn't 'a weird URL thing', it's broken access
   control affecting every one of the ~50,000 accounts, each reachable by iterating the number. A
   short script would harvest the lot; the tester does NOT do that — one manual proof (two uids,
   two screenshots) is the finding, and going further would itself be abuse.
4. Filed as security, not curiosity: 'Authenticated user can read any other user's full profile
   (PII) by changing uid in the URL; no server-side ownership check; ~50k accounts exposed;
   proof: uid 8842 logged-in reading uid 8841.' Priority: drop-everything. The fix is one
   server-side guard — the profile query filters by the session's own uid — plus a check across
   every other by-id endpoint for the same gap.
5. What separated 'shipped clean' from 'breach averted' was zero new tooling and one changed
   assumption: test as the attacker for sixty seconds, not only as the honest user. The functional
   suite was never wrong — it was answering a different question than the one that mattered.

**Quiz.** A feature passes 100% of its functional tests: the right user sees the right data, wrong inputs are rejected, everything saves correctly. What does this tell you about its security?

- [ ] It's secure — comprehensive functional passing covers the important risks
- [x] Almost nothing — functional correctness and security are independent, and the worst bugs live in adversarial paths functional tests never exercise
- [ ] It's secure for logged-in users, only anonymous access is still a question
- [ ] Security is fine as long as there were no errors or crashes during testing

*Functional correctness and security are independent properties, so a perfect functional suite tells you almost nothing about safety. Functional tests exercise the happy path — honest user, expected input, intended flow — while the most damaging security bugs (broken access control, injection, missing authorization) live precisely in the paths that path never touches: another user's ID, a hostile input, a request sent without the UI. Option A assumes the two properties are linked; they aren't — a functionally flawless feature can leak every record via one missing ownership check. Option C is too generous: the invoice/profile leaks in this note happen TO logged-in users abusing their own valid session. Option D mistakes silence for safety — leaks don't crash, they serve data quietly. The only way to earn a security verdict is to attempt the misuse on purpose and confirm it's prevented.*

- **The core question security testing asks (vs functional)** — Functional: 'does the right thing happen for the honest user?' Security: 'what WRONG thing can an adversary make happen?' Independent properties — a 100%-correct feature can be wide open.
- **IDOR (Insecure Direct Object Reference)** — Changing an identifier (URL id, query param) to one you don't own and getting someone else's data back — because the server fetched by id without checking ownership. Extremely common, high impact, testable with one edited number.
- **Why a security bug scales worse than a functional one** — A functional bug annoys the one user who hits it. A security bug (e.g. missing access control) can expose EVERY user's data to anyone, plus legal/financial/trust fallout — one support ticket vs a breach notice.
- **'The UI won't let you do that'** — The most expensive false comfort in software. The UI is a suggestion; attackers send requests directly (DevTools, curl, Postman). Hidden buttons and client-side checks are usability, not security. Real enforcement is server-side.
- **Why silence isn't safety** — Insecure systems usually keep working perfectly while being exploited — a leak serves data without erroring. 'No crash, no complaint' is the normal state of a compromised app, not evidence it's secure.
- **Security defects are often absences** — The check nobody wrote, the field nobody escaped, the endpoint nobody protected. Unlike functional bugs (wrong thing present), security bugs are frequently a needed control that should exist and doesn't.
- **A manual tester's core security move** — Ask 'what could a malicious user do that a normal one wouldn't?' then actually try it: change an ID to one you don't own, replay after logout, put hostile input in a trusted field. No tools, no title required.

### Challenge

In a written-authorized local, test, or training environment, take one feature that shows or edits
synthetic data owned by two tester accounts and run the full adversarial pass: (1) do it normally as
account A; (2) request account B's known seeded identifier; (3) replay the action after logging out; (4) send one unexpected
input where a normal value is expected. Write down, for each, whether the server PREVENTED it. If
all four are refused, you've earned a real security verdict on that feature — not just a functional
one. If any slipped through, you've found exactly the kind of bug that becomes a headline, and you
found it first.

### Ask the community

> I found that a logged-in user can read another user's records by changing the ID in the URL (`[/thing/1052 → 1051 returns someone else's data]`) — every functional test passes. How do teams usually prioritize IDOR/access-control findings, and what's the cleanest way to prove the impact without actually harvesting real user data?

The 'passed all functional tests but leaks everything' pattern is the most common serious finding
new security-minded testers report — hearing how others sized the impact, proved it responsibly
(one manual example, not a scrape), and got it prioritized is the fastest way to handle yours well.

- [MDN — Web security (the concepts, from the browser's side)](https://developer.mozilla.org/en-US/docs/Web/Security)
- [OWASP Top 10 — the industry's map of the most critical web risks](https://owasp.org/www-project-top-ten/)
- [Computerphile — How NOT to Store Passwords! (why 'it works' isn't 'it's safe')](https://www.youtube.com/watch?v=8ZtInClXe1Q)

🎬 [Computerphile — How NOT to Store Passwords!](https://www.youtube.com/watch?v=8ZtInClXe1Q) (9 min)

- Security is the non-functional dimension where 'it works' and 'it's safe' are independent claims — a feature can pass every functional test and still hand a stranger someone else's data.
- Functional tests use the happy path; the worst security bugs live in the adversarial paths (another user's ID, hostile input, requests sent without the UI) that the happy path never touches.
- Security bugs scale and cost differently: one missing access-control check can expose every user at once, silently, with legal and trust consequences a functional bug never carries.
- 'The UI won't let you do that' is false comfort — the UI is a suggestion, attackers send requests directly, and real enforcement must live server-side.
- Many security defects are absences: the ownership check nobody wrote, the input nobody escaped — which is why they're invisible to tests that only confirm the intended thing happens.
- Within written authorization, manual testers can request one test account's synthetic record as another, replay after logout, and feed approved hostile input — minimal probes that catch serious bugs without special tools.


## Related notes

- [[Notes/non-functional-testing-intro/security/common-risks|Common risks]]
- [[Notes/non-functional-testing-intro/security/a-testers-role|A tester's role]]
- [[Notes/api-testing-fundamentals/finding-api-bugs/negative-api-tests|Negative API tests]]


---
_Source: `packages/curriculum/content/notes/non-functional-testing-intro/security/why-it-matters.mdx`_
