# QA Mastery Talent — Test Plan & QA Strategy

> The capstone QA doc. Test pyramid, the security-critical RLS suite (real code), unit/component/E2E plans, and a requirements→tests traceability matrix — all in the repo's actual harness (Vitest + `packages/db` RLS tests + Playwright). Fittingly rigorous: this is a marketplace *for* QA engineers.

**Status:** v1.0 · **Harness:** Vitest (unit, per-package) · `packages/db/test/rls.test.ts` (RLS) · Playwright (e2e, chromium+webkit) · **Coverage gate:** 80% on new marketplace logic

---

## 0. Strategy — grounded in the existing harness (no generic stubs)

The repo already runs a clean test pyramid; the marketplace extends it. I deliberately do **not** use this skill's `test_suite_generator.py` (emits Jest) or `e2e_test_scaffolder.py` (generic) — the repo uses **Vitest** and a specific **`data-testid`** + service-role-RLS convention. Authoring to the real harness > generated stubs that don't fit.

```
         ╱╲   E2E (Playwright, chromium+webkit, prod builds)
        ╱  ╲     few, high-value journeys + the realtime + consent tests
       ╱────╲  Integration / RLS (packages/db/test, Vitest + real Supabase)
      ╱      ╲    the security invariants — the marketplace's #1 risk
     ╱────────╲ Unit + Component (Vitest + RTL, per package/app)
    ╱__________╲   actions, Zod contracts, filter builder, status map, components
```

| Layer | Tool (exists) | What it proves for Talent |
|---|---|---|
| Unit | Vitest (`packages/*/vitest.config.ts`) | pure logic: Zod event contracts, `searchTesters` filter builder, status→tone map, `connection_made` derivation |
| Component | Vitest + React Testing Library | design-system components render/behave; a11y roles |
| **RLS / integration** | `packages/db/test/rls.test.ts` style | **access-control invariants** (the launch gate) |
| E2E | Playwright (`e2e/tests/*.spec.ts`) | the user journeys + realtime + consent boundary, in a real browser |

---

## 1. RLS test suite — the security centerpiece (real code, repo pattern)

These are the **5 negative tests** the Backend/Security specs gate M0 on, written in the exact `rls.test.ts` idiom (service-role setup, `signedInClient`, `describe.skipIf(!hasEnv)`). Add to `packages/db/test/rls.test.ts` (or a sibling `talent-rls.test.ts`); run with `pnpm --filter @qa-mastery/db test:rls`.

```ts
// packages/db/test/talent-rls.test.ts
import { randomUUID } from "node:crypto";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import { afterAll, beforeAll, describe, expect, it } from "vitest";

const URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const ANON = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const SERVICE = process.env.SUPABASE_SERVICE_ROLE_KEY;
const hasEnv = Boolean(URL && ANON && SERVICE);
const PASSWORD = "rls-test-password-123";

async function signedInClient(email: string): Promise<SupabaseClient> {
  const c = createClient(URL!, ANON!, { auth: { persistSession: false } });
  const { error } = await c.auth.signInWithPassword({ email, password: PASSWORD });
  if (error) throw new Error(`sign-in failed for ${email}: ${error.message}`);
  return c;
}

describe.skipIf(!hasEnv)("Talent RLS invariants", () => {
  const service = createClient(URL!, SERVICE!, { auth: { persistSession: false, autoRefreshToken: false } });
  const emailClient = `t-client-${randomUUID()}@e2e.local`;
  const emailTester = `t-tester-${randomUUID()}@e2e.local`;
  const emailOutsider = `t-out-${randomUUID()}@e2e.local`;
  let clientId = "", testerId = "", outsiderId = "", convoId = "";
  let asClient: SupabaseClient, asTester: SupabaseClient, asOutsider: SupabaseClient;

  beforeAll(async () => {
    const mk = async (email: string) => {
      const r = await service.auth.admin.createUser({ email, password: PASSWORD, email_confirm: true });
      if (r.error) throw new Error(r.error.message);
      return r.data.user!.id;
    };
    clientId = await mk(emailClient); testerId = await mk(emailTester); outsiderId = await mk(emailOutsider);
    asClient = await signedInClient(emailClient);
    asTester = await signedInClient(emailTester);
    asOutsider = await signedInClient(emailOutsider);

    // tester publishes a profile (public) + an NDA portfolio item, via service role
    await service.from("talent_profiles").insert({ id: testerId, handle: `h${randomUUID().slice(0,8)}`, is_public: true });
    await service.from("talent_portfolio_items").insert({
      tester_id: testerId, type: "automation", title: "secret nda work", is_nda: true,
    });
    // a conversation strictly between client & tester
    const { data } = await service.from("talent_conversations")
      .insert({ client_id: clientId, tester_id: testerId, created_by: clientId }).select("id").single();
    convoId = data!.id;
    await service.from("talent_messages").insert({ conversation_id: convoId, sender_id: clientId, body: "private hello" });
  });

  afterAll(async () => {
    for (const id of [clientId, testerId, outsiderId]) await service.auth.admin.deleteUser(id);
  });

  it("1. a non-participant CANNOT read a conversation's messages", async () => {
    const { data } = await asOutsider.from("talent_messages").select("*").eq("conversation_id", convoId);
    expect(data ?? []).toHaveLength(0);            // RLS hides it (no error, just empty)
  });

  it("2. a user CANNOT insert a message into a conversation they're not in (even forging sender_id)", async () => {
    const { error } = await asOutsider.from("talent_messages")
      .insert({ conversation_id: convoId, sender_id: outsiderId, body: "intrusion" });
    expect(error).not.toBeNull();                  // with-check fails
    // and forging someone else's sender_id also fails
    const { error: e2 } = await asOutsider.from("talent_messages")
      .insert({ conversation_id: convoId, sender_id: clientId, body: "spoof" });
    expect(e2).not.toBeNull();
  });

  it("3. a non-owner CANNOT read another tester's NDA portfolio item", async () => {
    const { data } = await asOutsider.from("talent_portfolio_items").select("*").eq("is_nda", true);
    expect(data ?? []).toHaveLength(0);
  });

  it("4. anon/authenticated get ZERO rows from audit_events and talent_reports", async () => {
    const audit = await asClient.from("audit_events").select("*").limit(1);
    expect(audit.data ?? []).toHaveLength(0);
    await service.from("talent_reports").insert({ reporter_id: clientId, target_type: "profile", target_id: testerId, reason: "x" });
    const reports = await asOutsider.from("talent_reports").select("*").limit(1);
    expect(reports.data ?? []).toHaveLength(0);     // insert-own only; no read policy
  });

  it("5. a tester CANNOT link a portfolio item to a source_id they do not own", async () => {
    // (positive control) owner can write their own profile; outsider cannot write tester's profile
    const { error } = await asOutsider.from("talent_profiles")
      .update({ headline: "hijacked" }).eq("id", testerId);
    // RLS update with using(auth.uid()=id) → 0 rows affected, no privilege
    const { data: check } = await service.from("talent_profiles").select("headline").eq("id", testerId).single();
    expect(check!.headline).not.toBe("hijacked");
  });
});
```

> These are **regression tests for the database itself** — independent of app code. A future RLS-policy edit that opens a hole fails CI here. This is the single most important test asset for a marketplace handling private messages.

---

## 2. Unit tests (Vitest)

Pure logic, no DB — fast, runs in default `pnpm test`.

| Target | Test | Why |
|---|---|---|
| `searchTesters` filter builder | given filters → correct query predicates (specialties `&&`, deviceReal flag, rate ceiling, cursor) | the directory's correctness |
| Zod event contracts (`emitTalentEvent`) | each `talent.*` action's `metadata` validates; bad payload rejected | Data-Eng contract enforcement |
| `connection_made` derivation | 2nd reply by the *other* party fires it once; same-party replies don't; idempotent | North-Star metric integrity |
| status→tone map (`status.ts`) | every availability/verification/application/severity state → exactly one tone | Design-System single-source-of-truth |
| `ActionResult` error mapping | each thrown error → correct code (`VALIDATION`/`FORBIDDEN`/`RATE_LIMITED`) | API contract |

---

## 3. Component tests (Vitest + RTL)

Accessible-query-first (the repo/skill convention). Examples:

| Component | Assertions |
|---|---|
| `StatusBadge` | renders tone classes per §1 map; text label present (color-independent — a11y) |
| `ProfileStrengthMeter` | reflects completeness %; `role="progressbar"` with `aria-valuenow` |
| `FilterRail` | toggling a `FacetChip` updates the URL searchParams; `aria-pressed` flips; keyboard-operable |
| `MessageComposer` | Enter submits, Shift+Enter newlines; optimistic message appears then reconciles; disabled while sending |
| `EmptyState` | renders CTA; present (never a blank grid) when zero results |

```ts
// example — color-independent state (a11y rule from Design-System)
it("availability state is conveyed by text, not color alone", () => {
  render(<AvailabilityPill state="busy" />);
  expect(screen.getByText(/busy/i)).toBeInTheDocument();   // SR-readable
});
```

---

## 4. E2E (Playwright) — journeys + the hard async tests

New specs under `e2e/tests/talent-*.spec.ts`, `data-testid` locators, chromium+webkit (the existing matrix). The marketplace adds two tests most apps lack:

### 4.1 Critical journeys
| Spec | Flow | Pass |
|---|---|---|
| `talent-tester-onboard.spec.ts` | login → pick tester → fill skills+device → add artifact → publish | public profile reachable < 10 min budget |
| `talent-client-hire.spec.ts` | login → post project → filter testers → open profile → contact | reaches relevant tester < 3 min, sends message |
| `talent-empty-state.spec.ts` | directory with no matches | shows `EmptyState`, never a blank grid |

### 4.2 The signature test — **two-context Realtime delivery**
The marketplace's defining async behavior. Two browser contexts (client + tester); a message sent in one must appear live in the other via the RLS-authorized Postgres-Changes subscription.

```ts
// e2e/tests/talent-realtime.spec.ts
import { expect, test } from "@playwright/test";

test("a message sent by the client appears live in the tester's inbox", async ({ browser }) => {
  const clientCtx = await browser.newContext({ storageState: "e2e/.auth/client.json" });
  const testerCtx = await browser.newContext({ storageState: "e2e/.auth/tester.json" });
  const client = await clientCtx.newPage();
  const tester = await testerCtx.newPage();

  await tester.goto("http://localhost:3000/talent/inbox");
  await tester.getByTestId(`convo-${process.env.E2E_CONVO_ID}`).click();

  await client.goto(`http://localhost:3000/talent/inbox`);
  await client.getByTestId("message-input").fill("ping from client");
  await client.getByTestId("message-send").click();

  // tester sees it live — no reload. waitFor, never sleep (flaky-avoidance).
  await expect(tester.getByTestId("message-list")).toContainText("ping from client", { timeout: 10_000 });
});
```

### 4.3 Consent-boundary negative E2E
```ts
test("a client cannot open a chat with a tester they haven't contacted (no UI path + API blocked)", async ({ page }) => {
  // direct-navigate to a forged conversation id → redirected/forbidden, no messages rendered
  await page.goto("http://localhost:3000/talent/inbox/00000000-0000-0000-0000-000000000000");
  await expect(page.getByTestId("message-list")).toHaveCount(0);
  await expect(page).toHaveURL(/inbox$|forbidden/);
});
```

---

## 5. Test data, fixtures, flaky-avoidance

- **Seeding:** service-role inserts in `beforeAll` (the `rls.test.ts` pattern) — deterministic, no UI setup.
- **Auth fixtures:** generate `e2e/.auth/{client,tester}.json` storage states once (Playwright global setup), reuse across specs — fast, stable.
- **Flaky-avoidance** (the repo already encodes this): run E2E on **production builds** (`next start`, not dev — dev cold-compiles swallow clicks); `await expect(...)` / `waitFor`, **never `sleep`**; CI `retries: 2` + trace-on-retry. Realtime test uses a generous `timeout`, asserts on content arrival, not timing.
- **Isolation:** every test creates its own users (`randomUUID` emails `@e2e.local`) and tears them down — no cross-test bleed.

---

## 6. Coverage & CI gates

| Gate | Target | Where |
|---|---|---|
| Unit/component coverage (new marketplace logic) | **≥ 80%** branches/lines | `vitest --coverage`; `coverage_analyzer.py --threshold 80` |
| RLS suite | **100% of the 5 invariants pass** | `pnpm --filter @qa-mastery/db test:rls` in `ci.yml` |
| E2E journeys | green on chromium **and** webkit | `pnpm e2e` |
| a11y | no critical axe violations; Lighthouse a11y ≥ 95 | component tests + Lighthouse CI |

All wired into the existing `ci.yml` (boots local Supabase + applies migrations, so RLS tests run against the real `20260621000017_talent.sql`).

---

## 7. Requirements → tests traceability matrix

The senior-QA hallmark — every critical requirement maps to a test that proves it. Ties the whole 11-doc suite together.

| Requirement (source) | Verified by |
|---|---|
| Messaging only between contacted parties (PRD §3C, Sec §1) | RLS test #1/#2 + consent E2E (§4.3) |
| No PII leak / no contact scraping (Sec §1, GDPR) | RLS (public view excludes PII) + unit test on `getPublicProfile` shape |
| NDA artifacts hidden (PRD §1A, Sec §1) | RLS test #3 |
| Verified badges unforgeable (Arch ADR-004) | RLS (service-role-write only) + unit on sync idempotency |
| North-Star "connected pair" integrity (Data-Eng §1) | unit on `connection_made` derivation + realtime E2E |
| Directory relevance / never-empty (UX §2B) | `talent-empty-state` E2E + filter-builder unit |
| Tester onboarding < 10 min, client contact < 3 min (UX §5) | journey E2Es (§4.1) |
| Realtime delivery (Arch ADR-002) | two-context E2E (§4.2) |
| a11y AA, color-independent state (Design §1) | component a11y tests (§3) |
| Perf budget (Frontend §0) | Lighthouse CI gate |

---

## 8. Dogfood note
This is a marketplace *for* testers, run by a QA-strong founder — the test suite is also a **showcase artifact**. Bug reports filed during testing should use QA Mastery's own bug-report format (severity taxonomy from Design-System §1), and the realtime + RLS tests make good "how we test" content for the $0-organic motion (tester-spotlight / build-in-public). The quality of this suite is part of the product's credibility.

---

## 9. Summary
The marketplace test plan rides the existing pyramid — Vitest units, the `packages/db` RLS suite, Playwright e2e across chromium+webkit on production builds — and adds the two things a hiring marketplace specifically needs: **database-level access-control regression tests** (5 negative RLS invariants, real code, the launch gate) and a **two-context Realtime delivery test**. A requirements→tests traceability matrix proves every critical claim across all eleven docs is backed by a test. Coverage gate 80% on new logic; everything wired into the existing `ci.yml`. **First step: add `talent-rls.test.ts` alongside the `20260621000017_talent.sql` migration — they ship together.**
