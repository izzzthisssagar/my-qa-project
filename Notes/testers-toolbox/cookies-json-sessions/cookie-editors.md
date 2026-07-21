---
title: "Cookie editors"
tags: ["testers-toolbox", "cookies-json-sessions", "track-c"]
updated: "2026-07-16"
---

# Cookie editors

*Cookie editors let you view, edit, and delete a site's cookies directly - essential for testing session handling, role checks, and client-trust bugs. Includes a real 2024-2026 cautionary tale: the original EditThisCookie was pulled, and a malicious copycat with the same name still circulates.*

> A cookie editor lets you open the hood on exactly what a site stored in your browser and change it —
> which sounds niche until you realize it's how you test one of the most common real-world bug
> classes: a server that TRUSTS a client-side value it should be re-checking. This chapter also
> carries a genuine cautionary tale from 2024-2026: the most famous cookie editor of all got pulled
> from the Chrome Web Store, and a malicious impersonator wearing its name is still out there.

> **In real life**
>
> Three identical-looking glass jars on a counter — you can't tell from a glance whether one holds
> fresh cookies, one holds stale ones, and one is a decoy planted by someone hoping you'll grab it
> without checking. Opening each jar and looking inside is the only way to know for certain. A cookie
> editor is you opening the jar: it shows you exactly what's really stored, instead of trusting the
> label.

**cookie editor**: A cookie editor is a browser extension that lists every cookie set for the current site and lets you view, add, edit, or delete values directly - session IDs, role flags, cart data, feature flags, anything a site stores client-side. Cookie-Editor (free, open-source, Chrome/Firefox/Safari/Edge/Opera) is the maintained, safe standard as of 2026. The older EditThisCookie was removed from the Chrome Web Store in December 2024 for running on the deprecated Manifest V2 platform, and a malicious extension using the same name (with 50,000+ installs) has circulated since - always verify the developer name before installing any cookie editor.

## Why editing cookies is a real testing technique, not a party trick

- **Session and role testing** — many apps store a role or permission flag client-side for
  convenience. Editing it (e.g. `user_role: customer` → `admin`) and reloading tests whether the
  SERVER re-validates permissions on every request, or blindly trusts what the client sends back.
  If editing the cookie actually grants access, that's a serious, reportable vulnerability.
- **Session expiry and edge-state testing** — manually deleting a session cookie, corrupting its
  value, or setting an already-expired one lets you test logout behavior and expired-session
  handling without waiting for a real timeout.
- **Feature-flag and A/B testing** — some apps gate features behind a cookie value; editing it lets
  you access and test variant behavior directly, without waiting to be randomly assigned.

> **Tip**
>
> Any value stored in a cookie and later trusted by the server is a candidate for this exact test:
> edit it to something it "shouldn't" be, and see if the server catches the discrepancy. Prices,
> roles, discount flags, quantity limits — if it's client-visible, assume someone (attacker or
> careless script) could edit it, and verify the server doesn't just believe it.

> **Common mistake**
>
> Installing the first "cookie editor" result you find without checking the developer name. The real
> EditThisCookie's Chrome listing was removed in Dec 2024, and a copycat using the identical name and
> icon (over 50,000 installs, actively stealing cookies and even posting phishing content through
> victims' social accounts) has occupied that name space since. Use Cookie-Editor by cookie-editor.com
> (the maintained, safe, actively supported alternative) or verify any extension's actual developer
> before granting it access to every cookie on every site you visit.

![Three glass cookie jars in a row, each with a metal lid, illuminated from behind by warm lights - the leftmost holds dark cookies, the middle pale cookies, the rightmost chocolate-striped macarons](cookie-editors.jpg)
*Glass cookie jars, December 2007 — Wikimedia Commons, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Glass_cookie_jars,_December_2007.jpg)*
- **The sealed jar — a cookie's value, unopened** — From outside, you only know a jar EXISTS - not what's really inside. A browser cookie is the same: you know it's set, but its true value stays hidden until something opens and reads it.
- **Lifting the lid — what a cookie editor does** — The extension's whole job: open the jar, show you the real contents (name, value, expiry, flags), and let you change what's inside directly.
- **The visibly different contents in each jar** — Session ID, role flag, cart data, feature flag - each cookie holds something different, and only opening it (reading its actual value) tells you which is which.
- **The identical lids across all three jars** — From the outside, a legitimate cookie editor and a malicious copycat with the same name look identical too - the EditThisCookie lesson: verify what's actually inside (the real developer) before trusting the label.

**Testing a role-based permission with a cookie editor**

1. **Log in as a normal user** — Confirm baseline access - what pages/actions are correctly available at this role.
2. **Open the cookie editor, find the role/permission cookie** — Look for anything resembling role, permission level, or tier - not always obviously named.
3. **Edit the value to a higher-privilege role** — e.g. customer -> admin, or free -> premium - a deliberate, controlled probe, not guesswork.
4. **Reload and attempt the higher-privilege action** — Does the server actually check, or does it trust the edited cookie and grant access?
5. **Report precisely what happened** — If access was granted: a serious severity finding. If correctly denied: confirms the server-side check works as intended - also worth recording.

The core risk this whole note is about — a server trusting a client-editable value — is simple to
demonstrate directly:

*Run it - simulating a role-cookie edit (Python)*

```python
session_cookies = {
    "session_id": "a1b2c3d4-real-session",
    "user_role": "customer",
    "cart_id": "cart-9981",
    "theme": "dark",
}

def simulate_edit(cookies, key, new_value):
    edited = dict(cookies)
    edited[key] = new_value
    return edited

print("Original session cookies:")
for k, v in session_cookies.items():
    print(f"  {k:<12} = {v}")

tampered = simulate_edit(session_cookies, "user_role", "admin")

print()
print("After editing 'user_role' to 'admin' via a cookie editor:")
for k, v in tampered.items():
    marker = " <-- CHANGED" if session_cookies[k] != v else ""
    print(f"  {k:<12} = {v}{marker}")

print()
print("If the SERVER trusts this client-side value without re-checking")
print("permissions on every request, this one edit just became a privilege-")
print("escalation bug - exactly why cookie editors are core pentesting/QA")
print("tools, and exactly why 'trust but verify server-side' matters.")

# Original session cookies:
#   session_id   = a1b2c3d4-real-session
#   user_role    = customer
#   cart_id      = cart-9981
#   theme        = dark
#
# After editing 'user_role' to 'admin' via a cookie editor:
#   session_id   = a1b2c3d4-real-session
#   user_role    = admin <-- CHANGED
#   cart_id      = cart-9981
#   theme        = dark
#
# If the SERVER trusts this client-side value without re-checking
# permissions on every request, this one edit just became a privilege-
# escalation bug - exactly why cookie editors are core pentesting/QA
# tools, and exactly why 'trust but verify server-side' matters.
```

Same idea against a price/discount field — a classic e-commerce finding, tested the exact same way:

*Run it - simulating a cart-price cookie edit (Java)*

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, String> cookies = new LinkedHashMap<>();
        cookies.put("session_id", "a1b2c3d4-real-session");
        cookies.put("cart_total_cents", "4999");
        cookies.put("discount_applied", "false");
        cookies.put("locale", "en-US");

        System.out.println("Original cookies:");
        for (Map.Entry<String, String> e : cookies.entrySet()) {
            System.out.printf("  %-18s = %s%n", e.getKey(), e.getValue());
        }

        Map<String, String> tampered = new LinkedHashMap<>(cookies);
        tampered.put("cart_total_cents", "1");
        tampered.put("discount_applied", "true");

        System.out.println();
        System.out.println("After editing cart_total_cents and discount_applied client-side:");
        for (Map.Entry<String, String> e : tampered.entrySet()) {
            boolean changed = !cookies.get(e.getKey()).equals(e.getValue());
            System.out.printf("  %-18s = %s%s%n", e.getKey(), e.getValue(), changed ? " <-- CHANGED" : "");
        }

        System.out.println();
        System.out.println("A price stored client-side and trusted on checkout is a textbook");
        System.out.println("finding: this exact test (edit the cookie, see if checkout accepts");
        System.out.println("the new price) is standard practice, not an exotic attack.");
    }
}

/* Original cookies:
     session_id         = a1b2c3d4-real-session
     cart_total_cents   = 4999
     discount_applied   = false
     locale             = en-US

   After editing cart_total_cents and discount_applied client-side:
     session_id         = a1b2c3d4-real-session
     cart_total_cents   = 1 <-- CHANGED
     discount_applied   = true <-- CHANGED
     locale             = en-US

   A price stored client-side and trusted on checkout is a textbook
   finding: this exact test (edit the cookie, see if checkout accepts
   the new price) is standard practice, not an exotic attack. */
```

### Your first time: Your mission: safely test one client-trust boundary

- [ ] Install Cookie-Editor from cookie-editor.com or your browser's official store — Confirm the developer/publisher matches cookie-editor.com before installing - never install a 'cookie editor' whose developer name you haven't checked.
- [ ] Log into BuggyShop as a normal user and open the extension — List every cookie set for the site - note any that look like they might carry role, price, or permission information.
- [ ] Pick one cookie value and change it to something 'higher privilege' or 'better deal' — A role flag, a discount flag, a quantity limit - anything plausible. Note the EXACT original and edited values.
- [ ] Reload the page and attempt the corresponding privileged action — Did the app grant something it shouldn't have, based purely on the edited cookie?
- [ ] Record the result either way — A correctly-rejected edit confirms the server-side check works (still worth noting as a passed check); a granted one is a real, reportable finding with exact repro steps.

You've run a genuine client-trust security test — the same category of check professional testers
and pentesters run routinely, done safely on a practice application.

- **You installed a 'cookie editor' extension and now suspicious things are happening (unexpected posts, odd account activity).**
  Uninstall it immediately and check its developer name against cookie-editor.com's official listing. If it doesn't match, assume compromise: change passwords for accounts you were logged into while it was active, and report the extension to your browser's web store.
- **Editing a cookie value has no visible effect at all.**
  Check whether the app is actually reading that cookie, or storing the real state server-side and only using the cookie for display/convenience - many apps store the meaningful state in a database keyed by session ID, making the visible cookie value cosmetic. Confirm by checking the network tab for what's actually sent and how the server responds.
- **An edited cookie gets silently overwritten back to its original value on the next request.**
  This usually means the server is regenerating that cookie on every response, based on server-side state - actually a GOOD sign (the server isn't trusting the client value), worth noting as evidence the boundary is handled correctly.
- **You need to test cookie behavior across HTTPS/HttpOnly-flagged cookies the editor can't see.**
  HttpOnly cookies are deliberately inaccessible to JavaScript (including most browser extensions) as a security measure - that's working as intended, not a tool limitation to work around. Test those via a network proxy tool instead (covered in the beyond-the-browser chapter) if you specifically need to inspect them.

### Where to check

- **cookie-editor.com's official page** — confirm you have the genuine extension before installing, matching developer name and listing exactly.
- **The network tab, after any cookie edit** — confirms what the server actually received and how it responded, the real evidence for whether a trust boundary held or broke.
- **Server-side logs or an admin view**, if available — the definitive answer to whether an edited-cookie privilege escalation actually took effect on the backend, not just in the UI.
- **HttpOnly and Secure flags on sensitive cookies** (via DevTools' Application/Storage panel) — their PRESENCE is itself a positive finding (harder to tamper with or steal via script); their ABSENCE on a session cookie is worth flagging.

### Worked example: a discount-cookie edit that should have been rejected — and wasn't

1. A tester notices BuggyShop sets a cookie `promo_discount_pct: 0` after a failed promo-code
   attempt. Curious whether this value is trusted anywhere.
2. Using Cookie-Editor, they change `promo_discount_pct` from `0` to `100` and proceed to checkout
   without ever entering a valid promo code.
3. Checkout total drops to $0.00. The server applied the discount based purely on the cookie value,
   with no re-validation that a real promo code was ever actually redeemed.
4. Confirmed via network tab: the checkout request includes `promo_discount_pct=100` and the
   server's response total reflects it directly — no server-side lookup of an actual promo record.
5. Report: "Editing the `promo_discount_pct` cookie to 100 (via browser extension, no code required)
   results in a $0.00 checkout total with no promo code ever validated server-side. Repro: [exact
   steps]. Severity: Critical — direct, trivial-to-execute revenue-loss vulnerability, not a cosmetic
   bug." A finding measured in real dollars, found by editing one cookie value.

**Quiz.** A tester edits a role cookie from 'customer' to 'admin', reloads the page, and the admin dashboard link now appears in the navigation menu — but clicking it still redirects to an 'access denied' page. What's the correct conclusion?

- [ ] This is a full privilege-escalation bug - the role cookie edit worked, so report it as Critical severity
- [x] This is a partial finding worth reporting at lower severity: the UI incorrectly trusts the client-side role cookie to decide what to DISPLAY, even though the actual protected action still correctly re-validates permission server-side
- [ ] This is not a bug at all, since the actual admin functionality remains protected
- [ ] The cookie editor must be malfunctioning, since editing the cookie should have either changed everything or nothing

*The two checks (what to SHOW vs what to ALLOW) are separate, and this scenario shows exactly one of them failing while the other holds: the nav menu trusted the client-editable cookie for display logic (a real bug - showing privileged UI to non-privileged users is an information/UX leak and often a stepping stone to worse findings), while the actual admin action correctly re-validated server-side and blocked access (the important boundary held). Option one overstates the severity - full privilege escalation would require reaching the actual protected functionality, which didn't happen here. Option three misses a real, reportable issue by requiring 'total failure' as the bar. Option four is a category error: a cookie editor CAN affect one client-side check (menu visibility) while a separate, independent server-side check remains unaffected - that's not tool malfunction, that's exactly what layered validation looks like when only one layer is broken.*

- **What a cookie editor is used for in testing** — Viewing, adding, editing, or deleting a site's cookies directly - core technique for testing whether the SERVER properly re-validates client-editable values (roles, prices, discount flags) instead of blindly trusting them.
- **The EditThisCookie cautionary tale (2024-2026)** — Google removed the original (3M+ users) in Dec 2024 for running on deprecated Manifest V2. A malicious copycat using the identical name (50k+ installs) has circulated since, stealing cookies and posting phishing content. Verify developer name before installing ANY cookie editor.
- **The safe, maintained alternative in 2026** — Cookie-Editor by cookie-editor.com - free, open source, works across Chrome/Firefox/Safari/Edge/Opera. Confirm the developer/publisher matches the official site before installing.
- **The general client-trust test pattern** — Any value visible/editable client-side (role, price, discount, quantity limit) should be tested by editing it to an implausible/privileged value and checking whether the SERVER catches the discrepancy - if it doesn't, that's the bug.
- **Why HttpOnly cookies can't be edited by most extensions** — HttpOnly is a deliberate security flag blocking JavaScript (including extensions) from reading/writing that cookie - working as intended, not a tool limitation. Test those via a network proxy instead.
- **The two-layer finding pattern (display vs. actual access)** — A cookie edit can affect what the UI SHOWS (a real, lower-severity bug if wrong) independently of what the server actually ALLOWS (the more serious boundary) - always test both, and report them at their true, separate severities.

### Challenge

Find one cookie in BuggyShop that appears to store role, discount, or limit-related state. Edit it
with Cookie-Editor and test both the DISPLAY layer (does the UI change what it shows?) and the
ACTUAL ACCESS layer (does a protected action actually succeed?) separately. Write up your finding
using this note's worked-example structure — exact cookie name, original value, edited value, and
which layer(s) failed.

### Ask the community

> I edited `[cookie name]` from `[original value]` to `[edited value]` on `[app]` and observed `[what happened]`. Is this the kind of client-trust issue worth reporting as a security finding, or is there a legitimate reason this cookie is meant to be client-editable?

Not every editable cookie is a bug — the most useful answers will help you distinguish a genuine
trust-boundary failure from an intentionally client-controlled preference (like theme or locale).

- [Cookie-Editor — official site (the safe, maintained standard)](https://cookie-editor.com/)
- [gHacks — the EditThisCookie removal and copycat story (Dec 2024)](https://www.ghacks.net/2024/12/31/google-chrome-legit-editthiscookie-extension-removed-instead-of-malicious-copycat/)
- [Rafsan The Developer — Cookies Editor Extension for Chrome, how to use it](https://www.youtube.com/watch?v=PGWW3I-Izpw)

🎬 [Cookie Editor — Browser Extension Review (eccorem project)](https://www.youtube.com/watch?v=23cys7FQzbw) (5 min)

- Cookie editors let you view/edit/delete a site's cookies directly - core technique for testing whether the server properly re-validates client-editable values instead of trusting them.
- The EditThisCookie story is a real 2024-2026 security lesson: the original was pulled (Manifest V2), and a malicious copycat with the same name still circulates with 50k+ installs.
- Cookie-Editor (cookie-editor.com) is the safe, maintained 2026 standard - always verify developer name before installing any cookie editor.
- The general pattern: edit any client-visible value to something implausible and check whether the server catches it - roles, prices, discounts, and limits are the classic targets.
- Test the DISPLAY layer (what the UI shows) and the ACCESS layer (what the server actually allows) separately - a cookie edit can break one without the other.


## Related notes

- [[Notes/testers-toolbox/cookies-json-sessions/json-formatters|JSON formatters]]
- [[Notes/testers-toolbox/cookies-json-sessions/multi-account-testing|Managing multi-account testing]]
- [[Notes/defect-management/severity-vs-priority/severity|Severity]]


---
_Source: `packages/curriculum/content/notes/testers-toolbox/cookies-json-sessions/cookie-editors.mdx`_
