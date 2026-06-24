# QA Mastery Talent — Frontend Spec

> Companion to the Backend Spec and Design System. Rendering strategy, the Server/Client component boundary map, data-fetching, performance budget, and accessibility for the marketplace frontend.

**Status:** v1.0 · **Profile:** `next-app-router` (mixed-rendering) · **Surface:** web-first, dark-first, mobile-4G as the design constraint

---

## 0. Assumptions + engine validation (skill discipline)

| Assumption | Value | Why |
|---|---|---|
| Primary device + network | **mobile-4G** (global QA audience, mid-range Android) as the constraint; clients often desktop | design for the worst case |
| LCP target (p75) | **2000 ms** public pages · INP **< 200 ms** · CLS **< 0.1** | Build-Plan SLO |
| SEO vs auth-walled | **MIXED** — public profiles SEO-critical; app shell auth-walled | the central frontend decision |
| WCAG + a11y owner | **AA**, owner = founder | Design-System contrast already verified AA |

### Engine result — and the honest correction
`frontend_decision_engine.py` returned **`astro-or-static` (90%)** as top, but **explicitly flagged a violated constraint: `read_write_ratio >= 100`**. A static-site profile assumes near-zero writes; our marketplace is **write-heavy** (messages, posts, applications, shortlists). So the top pick is an artifact of flattening "mixed" into `seo=true/auth=false`. **The correct profile is the runner-up `next-app-router` (89%, within 15%)** — a dynamic, mostly-auth-walled app with a *thin* SEO-critical public surface. This matches the live stack (no change) and Architecture ADR-001. *(Lesson: read the engine's violations, don't parrot the top score.)*

### Verifiable criteria (CWV + bundle budget + Lighthouse floors)
| | Target |
|---|---|
| Core Web Vitals (mobile-4G p75) | LCP < **2000 ms** (public) / < 2500 ms (app), INP < **200 ms**, CLS < **0.1** |
| Per-route JS budget | **≤ 150 KB-gzip** / route (next-app-router profile) |
| Lighthouse floors (CI gate) | **Perf ≥ 90** (public profile), **a11y ≥ 95** all routes |

Bundle baseline today: analyzer scored the platform **100/100 (A)** — start from a clean budget; protect it.

---

## 1. Rendering strategy — the mixed model

The single most important frontend decision: **split rendering by route purpose.**

| Route | Purpose | Rendering | Why |
|---|---|---|---|
| `(app)/talent/u/[handle]` | **public profile** | **RSC + ISR** (cache, revalidate on profile update via tag) | SEO + shareable on LinkedIn = the $0-organic motion; mostly static between edits |
| `(app)/talent/testers` | directory | **RSC** list + **client filter island** | server-rendered cards (fast LCP, indexable), interactivity via a small island |
| `(app)/talent/post`, `/profile`, `/onboarding` | editors | **RSC shell + client form islands** | forms need state; shell stays server |
| `(app)/talent/projects/[id]` | project + applicants | **RSC** + client action buttons | mostly read |
| `(app)/talent/inbox` | messaging | **RSC shell + client Realtime island** | live subscription is inherently client |

**Default to Server Components.** Add `'use client'` only for: filters, forms, the message composer, the Realtime subscription, and action buttons (the existing app's exact discipline — `button.tsx` is `'use client'`, pages are RSC).

**Public-profile SEO essentials:** `generateMetadata()` (title/description/OG image per tester), JSON-LD `Person`/`ProfilePage`, canonical URL, OG image for LinkedIn cards. These pages must render meaningful HTML without JS.

---

## 2. Server/Client component boundary map (core architecture)

```
(app)/talent/testers/page.tsx                         ← RSC: await searchTesters(searchParams)
  ├─ <FilterRail/>                  'use client'       ← reads/writes URL searchParams (shareable state)
  ├─ <TesterGrid/>                   RSC               ← maps rows → <TesterCard/> (server)
  │    └─ <TesterCard/>              RSC               ← <VerifiedBadge/> <DeviceChip/> <AvailabilityPill/> (all server)
  ├─ <Suspense fallback=<TesterGridSkeleton/>>         ← stream results; instant shell
  └─ <ShortlistButton/>             'use client'       ← optimistic toggle

(app)/talent/u/[handle]/page.tsx                       ← RSC + ISR: getPublicProfile(handle)
  ├─ generateMetadata + JSON-LD     RSC               ← SEO
  ├─ <PortfolioArtifactCard/>       RSC               ← code rendered server-side (syntax highlight at build/RSC)
  └─ <ContactButton/>               'use client'       ← opens conversation (client-only since gated)

(app)/talent/profile/page.tsx                          ← RSC shell: load own profile
  └─ <ProfileEditor/>               'use client'       ← form (useState/useActionState) → upsertTesterProfile
        ├─ <SkillTaxonomyPicker/>   'use client'
        ├─ <DeviceMatrixEditor/>    'use client'
        ├─ <PortfolioReusePicker/>  'use client'       ← pick existing bug_reports/test_cases (ADR-003)
        └─ <ProfileStrengthMeter/>  client (derived)   ← UX "Valley of Death" fix

(app)/talent/inbox/page.tsx                            ← RSC shell: list conversations
  ├─ <ConversationList/>            RSC
  └─ <ConversationThread/>          'use client'       ← Realtime subscription (dynamic import)
        ├─ <MessageBubble/>         (pure, rendered by client list)
        └─ <MessageComposer/>       'use client'       ← optimistic send via useOptimistic
```

**Rule:** the `'use client'` boundary is pushed as *deep* as possible — page stays RSC, only the interactive leaf is a client island. This keeps per-route JS under budget.

---

## 3. Data fetching & state

| Concern | Pattern |
|---|---|
| **Reads** | RSC `await` the Server-Action data functions (`searchTesters`, `getPublicProfile`) — no client fetch, no waterfall. **Parallel** with `Promise.all` (profile + badges + devices + portfolio). |
| **Streaming** | `<Suspense>` around the directory grid → instant filter shell + skeleton, results stream in (good INP/LCP). |
| **Filter state** | **URL `searchParams` is the source of truth** (`?specialty=api&device=real&avail=open`). Shareable, back-button-correct, SSR-readable. `<FilterRail>` updates via `router.replace` (shallow). `useDebounce(300ms)` on the text query. |
| **Mutations** | Server Actions via `useActionState`/`<form action>`; `useOptimistic` for sending a message and toggling shortlist (instant UI, reconcile on server response). |
| **Realtime** | Inbox subscribes to `talent_messages` Postgres Changes (RLS-authorized) filtered to the open conversation; Broadcast for typing. The Supabase Realtime client is **dynamically imported** so it never ships to non-inbox routes. |
| **Global client state** | **None.** No Redux/Zustand needed — URL + RSC + Realtime cover it. (Engine anti-pattern: don't add a client store for server state.) |

---

## 4. Performance budget — how each route hits target

| Route | Budget | Techniques |
|---|---|---|
| `/talent/u/[handle]` (public) | LCP < 2000ms, ≤120 KB | ISR/cache; RSC (zero form JS); `next/image` avatar with `priority`; JSON-LD; minimal client (only ContactButton) |
| `/talent/testers` | LCP < 2.5s, ≤150 KB | RSC cards; client only in FilterRail; `next/image` avatars `fill`+`sizes`; keyset "load more" (no giant list); virtualize only if a page > ~60 cards |
| `/talent/inbox` | INP < 200ms | dynamic-import Realtime client; windowed message list; optimistic send |
| `/talent/profile` | ≤150 KB | code-split heavy editor sub-parts; lazy-load the reuse picker |

**Config (from the bundle analyzer's two findings — both apply):**
```js
// next.config.js
images: { remotePatterns: [{ protocol: 'https', hostname: '<supabase-project>.supabase.co' }],
          formats: ['image/avif','image/webp'] },          // avatars/artifact thumbs
experimental: { optimizePackageImports: ['lucide-react'] }, // icon tree-shaking
```
- **No heavy deps:** dates via `Intl`/`date-fns` (not moment); native `fetch` (not axios); reuse `packages/ui` (no MUI). Protect the 100/100 score.
- **Avatars/thumbnails:** always `next/image` (AVIF/WebP, sized) — never raw `<img>`; prevents CLS.

---

## 5. Accessibility (WCAG AA)

- **Semantic HTML:** `<nav>` filter rail, `<main>` directory, `<article>` tester card, `<button>` for actions (never a div), `<form>` editors. Cards are a link-wrapped article with an accessible name.
- **Keyboard:** filter chips are real toggle `<button aria-pressed>`; directory is tab-navigable; inbox thread has a logical focus order; composer submits on Enter (Shift+Enter = newline). Skip-link to `#talent-main`.
- **Focus:** the existing `focus-visible:outline-2 outline-offset-2` idiom on every interactive element; move focus to the new message / to the thread on open; trap focus in any modal.
- **Screen reader:** icon-only buttons (`Contact`, `Report`) get `aria-label`; status pills convey state in text, not color alone (color + label — Design-System rule); live region (`aria-live="polite"`) announces new messages in the inbox.
- **Contrast:** already AA-verified on `#09090b` (Design-System §1) — body text uses the `-300` step (≥10:1).
- **Motion:** all transitions gated by the existing `prefers-reduced-motion` block in `globals.css`.

---

## 6. Component → rendering reference (ties to Design-System §2)

| Component | Server/Client | Notes |
|---|---|---|
| `TesterCard`, `ProjectCard`, `PortfolioArtifactCard`, `VerifiedBadge`, `DeviceChip`, `AvailabilityPill`, `SeverityTag`, status badges | **Server** | pure presentational; no JS shipped |
| `FilterRail`/`FacetChip`, `ShortlistButton`, `ContactButton`, `ProfileEditor` (+ pickers), `MessageComposer`, `ConversationThread`, `ProfileStrengthMeter`, `PostProjectWizard` | **Client** | interactivity / state / realtime |
| `EmptyState` | **Server** | cold-start; pure markup + atmosphere utils |

---

## 7. Testing & CI gates

| Layer | Tool | Marketplace specifics |
|---|---|---|
| Component | RTL + Vitest (`turbo test`) | filter toggles update URL; `useOptimistic` send rolls back on error; status→tone map |
| a11y | Lighthouse CI + jest-axe | a11y ≥ 95 gate; keyboard path through directory + inbox; no color-only state |
| E2E | Playwright (`e2e/tests`) | onboarding→publish; post→filter→contact; **realtime delivery across two browser contexts** |
| Perf | Lighthouse CI / Vercel Speed Insights | LCP/INP/CLS budget on `/talent/u/[handle]` and `/talent/testers`; fail CI on regression |
| Bundle | `bundle_analyzer.py` in CI | keep ≥ 90; alert on any new heavy dep |

---

## 8. Summary
The marketplace frontend is **`next-app-router` mixed-rendering**: public tester profiles are RSC+ISR (SEO + LinkedIn-shareable — the growth engine), the app shell is RSC with deep client islands (filters, editors, realtime inbox). State lives in the **URL** (filters) and **Realtime** (inbox) — no client store. The performance budget (LCP < 2s public, ≤150 KB-gzip/route, a11y ≥ 95) is enforced in CI, starting from the existing 100/100 bundle. The honest engine read mattered here: the top-scored static profile *violated* the write-heavy reality, so we took the correct runner-up. Frontend work begins alongside Backend M1 (tester profile) and follows the same milestone order.
