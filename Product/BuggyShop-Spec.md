# BuggyShop — Practice App Specification

**Status:** Draft v1 · Week 1 deliverable · Owner: Sagar
**Purpose:** The deliberately flawed e-commerce app every Track A/B lab runs against. Seeded bugs are versioned and machine-checkable → auto-graded bug hunts and test runs.

---

## 1. Product Overview

A small but realistic e-commerce site ("BuggyShop — everything for testers who shop"). Built as a standalone Next.js app + Supabase, deployed separately from the learning platform, embedded via iframe or opened in a new tab. Each learner gets an isolated data sandbox (their own user rows; products are shared read-only).

### Releases
| Release | Used by | Contents |
|---|---|---|
| **v1.0** | A1.4 → A4.6, all of Track B | Core app + seeded bugs BS-001…BS-020 |
| **v1.1** | A5.1–A5.5 | Wishlist feature + regressions BS-021…BS-023 (+ fixes some v1.0 bugs to teach retest) |
| **v2.0** | A5.6 Capstone | Coupon system + fresh bugs BS-026…BS-037 (capstone-only manifest, kept private) |

Learners can switch release from a version picker (platform controls which versions are unlocked).

---

## 2. Pages & Features (v1.0)

1. **Home** — hero, featured products, nav, search bar, footer.
2. **Signup** — name, email, password (+ confirm), age (18–100), terms checkbox.
3. **Login** — email/password, "remember me," forgot-password (stub: sends nothing, shows confirmation).
4. **Product list** — grid, category filter, price filter (0–100000), sort (price/name), search results.
5. **Product detail** — images, price, quantity selector (1–99), add to cart, stock indicator, reviews (read-only seed data).
6. **Cart** — line items, quantity edit, remove, subtotal, shipping rule (free > ₹999), proceed to checkout.
7. **Checkout** — address form, payment method selection (COD / card mock / UPI mock), order summary, place order.
8. **Order confirmation + Orders list** — order status (Placed → Paid → Shipped → Delivered / Cancelled), cancel button.
9. **Profile** — edit name/email/password, order history link.
10. **Intentionally messy area (for Track B):** the "Deals" page — auto-generated divs, dynamic IDs, nested tables, delayed loading — exists to teach locator strategy and waits. Bugs are NOT seeded here in v1.0; it's a locator gym.

### Non-functional requirements (these matter unusually much)
- **Deterministic:** same actions → same results, always. No random failures except where a bug is explicitly seeded as intermittent (only BS-018).
- **Stable selectors everywhere except the Deals page:** every interactive element gets `data-testid`. Track B depends on this.
- **Resettable:** "Reset my sandbox" button restores the learner's data to seed state in <5 s.
- **Fast:** no real payments, no emails, no external APIs. Everything mocked in-app.
- **Bug flags:** every seeded bug is behind a feature flag keyed to release version → one codebase, three releases, and you can hotfix a broken bug without redeploying content.

---

## 3. The Bug Manifest (how grading works)

Each seeded bug is a JSON record. The grading service matches learner bug reports against this manifest (page + trigger + observed-behavior keywords, with AI-assisted fuzzy matching as a Phase 1.5 upgrade; v1 can use structured report fields — learner selects page and category from dropdowns, describes the rest).

```json
{
  "id": "BS-008",
  "release": "1.0",
  "page": "product-list",
  "feature": "price-filter",
  "category": "boundary",
  "severity": "major",
  "priority_hint": "high",
  "title_internal": "Price filter excludes items priced exactly at the max boundary",
  "trigger": "Set max price = X; product priced exactly X disappears",
  "repro_steps_internal": ["Open product list", "Set max price to 500", "Item 'Tester Mug' (₹500) not shown"],
  "expected": "Filter range is inclusive: items priced exactly at max appear",
  "teaches": ["A3.3 BVA"],
  "detection": { "type": "structured-match", "required_fields": ["page", "boundary_value"] },
  "points": 10
}
```

---

## 4. Seeded Bugs v1.0 — BS-001…BS-020

Severity scale: blocker / critical / major / minor / trivial.

| ID | Page / Feature | Bug | Category | Sev | Teaches |
|---|---|---|---|---|---|
| BS-001 | Signup / email | Accepts `user@@domain..com` (broken email regex) | Validation | major | A3.2 EP |
| BS-002 | Signup / password | Error message reveals password rule only AFTER failed submit, and message says "username invalid" (wrong field) | Usability/Validation | minor | A4.4 (guided first report) |
| BS-003 | Signup / confirm-password | Paste into confirm field bypasses match check | Validation | major | A3.6 error guessing |
| BS-004 | Signup / terms | Can submit with unchecked terms via double-click on Submit | Functional | major | A3.6 |
| BS-005 | Login / remember me | "Remember me" never persists session | Functional | minor | A2 levels lab |
| BS-006 | Login / error | Wrong password error: "User does not exist" (information + wrong message) | Security-ish/Usability | minor | A2.3 types |
| BS-007 | Product detail / quantity | Quantity field accepts 0 and adds a ₹0 line item | Boundary/Validation | major | A3.2 EP |
| BS-008 | Product list / price filter | Max-boundary item excluded (filter uses `<` not `<=`) | Boundary | major | A3.3 BVA |
| BS-009 | Product list / sort | Sort by price sorts as text: 1000 < 200 < 30 | Functional | major | A1.4 observations |
| BS-010 | Search | Leading/trailing spaces → zero results (no trim) | Functional | minor | A3.6 |
| BS-011 | Checkout / payment rules | Card option shown for orders < ₹100 but errors on submit (decision-table rule conflict) | Logic | major | A3.4 decision tables |
| BS-012 | Cart / shipping | Free shipping applies at exactly ₹999 (rule says > ₹999) | Boundary/Logic | minor | A3.3, A3.4 |
| BS-013 | Cart / quantity edit | Setting quantity to 99 then +1 wraps the line total negative | Boundary/Calc | critical | A3.3 |
| BS-014 | Orders / cancel | Cancel button works on already-Shipped orders (invalid state transition) | State | critical | A3.5 |
| BS-015 | Orders / status | Order shows "Delivered" while payment status still "Pending" (state mismatch) | State | major | A3.5 |
| BS-016 | Checkout / address | PIN/ZIP accepts letters; order then unroutable (garbage-in accepted) | Validation | major | A3.6 mini-capstone |
| BS-017 | Checkout / summary | Discount line shows but isn't subtracted from total | Calc | critical | A4.6 hunt |
| BS-018 | Cart (intermittent, only seeded intermittent bug) | Removing the last item sometimes (1 in 3, deterministic counter) leaves subtotal unchanged until refresh | Functional | major | A4.4 repro discipline |
| BS-019 | Profile / edit email | Changing email doesn't re-validate format (accepts empty) | Validation | major | A5.1 exploratory |
| BS-020 | Profile / order history | Shows orders from a different (seed) user — data leak | Data/Security-ish | critical | A5.1 exploratory |

**Reachability note:** A4.6 Bug Hunt I scope = signup→checkout flows; reachable set there is 18 bugs (BS-001…BS-018); pass bar = 10. BS-019/020 are reserved for the A5.1 exploratory charter so that area still has fresh finds.

## 5. v1.1 — Wishlist Feature + Regressions (BS-021…BS-025)

New: heart icon on product cards/detail → wishlist page; move-to-cart.

| ID | Page | Bug | Category | Sev | Teaches |
|---|---|---|---|---|---|
| BS-021 | Cart (regression) | Move-to-cart from wishlist ignores the BS-007 fix — quantity 0 returns | Regression | major | A5.2 |
| BS-022 | Product list (regression) | Heart icon overlaps and blocks the Add-to-Cart button | Regression/UI | major | A5.2 |
| BS-023 | Mobile viewport | Checkout "Place order" button hidden under footer at ≤ 390 px width | Responsive | critical | A5.3 |
| BS-024 | Wishlist | Wishlist count badge caps at 9 (shows "9" for 10+) | Boundary | trivial | extra credit |
| BS-025 | Wishlist | Removing item from wishlist on detail page doesn't sync list page until refresh | Functional | minor | extra credit |

Also in v1.1: BS-002, BS-008, BS-009 are FIXED → retest lessons get genuine "verify the fix" work.

## 6. v2.0 — Coupon System + Capstone Bugs (BS-026…BS-037)

New: coupon entry at cart (percent / flat / free-shipping codes, expiry, min-order, one-per-order, stacking forbidden).
Twelve fresh bugs across validation/boundary/logic/state/calc/UI — **manifest kept out of this file deliberately** (capstone integrity; learners will find this doc if it ships in a public repo). Maintain `BuggyShop-Manifest-v2-PRIVATE.json` separately. Design rule: ≥2 bugs per A3 technique so the capstone forces technique use, e.g. expiry boundary (BVA), stacking rules (decision table), coupon state after order-cancel (state transition).

---

## 7. Build Notes

- **Stack:** Next.js + Tailwind + Supabase (same as platform — one mental model). Seed data: ~30 products, 3 categories, 1 seed "other user" with orders (needed for BS-020).
- **Bug implementation pattern:** each bug = small conditional behind `bugFlag('BS-008', release)`. Never sprinkle bug logic inline without the flag wrapper — unmaintainable otherwise.
- **Grading API:** `GET /api/manifest/:release` (auth: platform service key) returns the manifest; platform's grading service does the matching. Manifest JSON lives in the BuggyShop repo, never shipped to the client bundle.
- **Track B reuse:** all `data-testid` attributes documented in a selector inventory (auto-generated page → testids table) so automation lessons can reference them precisely.
- **Estimated build:** core app 2–3 weeks AI-assisted part-time; bug seeding + manifest +1 week; v1.1/v2.0 increments ~1 week each, needed months later.

---

## 8. Open Questions (decide before build)

1. One shared BuggyShop with per-learner data rows vs per-learner ephemeral instance? → **Start shared + sandboxed rows; revisit if learners collide.**
2. Structured bug-report form (dropdown page/category → easy exact matching) vs free-text + AI matching? → **Structured in v1; AI matching Phase 1.5.**
3. Currency ₹ vs $ — follows the Phase 0 geography decision (plan §9).
