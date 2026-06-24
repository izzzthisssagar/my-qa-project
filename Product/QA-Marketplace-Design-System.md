# QA Mastery Talent — UI Design System (extension)

> Companion to the PRD / UX / Architecture / Data-Eng docs. This **extends the existing QA Mastery design system** — it does not introduce a new palette, font, or token philosophy. New tokens and components only, in the established idiom.

**Status:** v1.0 · **Base:** `apps/platform/src/app/globals.css` (Tailwind v4 `@theme inline`) + `packages/ui` · **Surface:** web-first, dark-first

---

## 0. Principle — extend, don't reinvent

The platform has a deliberate, restrained system. We **reuse it verbatim** and add only marketplace-specific semantics.

| Existing token (do NOT change) | Value | Role |
|---|---|---|
| `--background` | `#09090b` (zinc-950) | dark-first canvas |
| `--foreground` | `#f4f4f5` | primary text |
| `--accent` / `--color-accent-soft` | `#2dd4a7` / `#1f6f5c` | teal — primary action / on-light |
| `--bug` | `#f5b948` | amber — "bug hunt", used sparingly |
| `--font-display` | Bricolage Grotesque | headings |
| `--font-sans` / `--font-mono` | Geist | body / code |
| `--font-serif` (`.font-serif-accent`) | Instrument Serif *italic* | the deliberate "off" note |
| Atmosphere utils | `.bg-grid` `.bg-glow` `.bg-glow-bug` `.grain` `.text-glow-accent` | depth, never a flat fill |

**The real design language** (decoded from `badge.tsx` / `button.tsx`): the brand maps onto **Tailwind scales** — accent teal ≈ `emerald-300/400`, `--bug` ≈ `amber`, neutrals `zinc`, info `sky`, danger `red`. Dark-UI badge idiom is fixed: **`border-{c}-500/40 bg-{c}-500/10 text-{c}-300`**. Every new component below uses exactly this idiom, the `cn()` helper, variant-union props, and `focus-visible:outline-2 outline-offset-2`.

---

## 1. New semantic tokens — marketplace status

The marketplace introduces *states* the learning app never needed (availability, verification, application status, bug severity). Define them as a **documented mapping onto the existing scales** — not new hex values. Add the canonical ones to `@theme inline` so they're nameable; render with the badge idiom.

```css
/* add to globals.css @theme inline — semantic aliases, not new colors */
--color-status-open:     #34d399; /* emerald-400  — available / verified / hired (success) */
--color-status-busy:     #fcd34d; /* amber-300    — busy / pending / warning */
--color-status-off:      #a1a1aa; /* zinc-400     — not looking / neutral / closed */
--color-status-danger:   #f87171; /* red-400      — declined / critical / report */
--color-status-info:     #7dd3fc; /* sky-300      — informational / NDA-locked */
```

### Status → tone mapping (single source of truth)

| Domain | State | Tone | Tailwind classes (badge idiom) |
|---|---|---|---|
| **Availability** | Open to work | success | `border-emerald-500/40 bg-emerald-500/10 text-emerald-300` |
| | Busy | warning | `border-amber-500/40 bg-amber-500/10 text-amber-300` |
| | Not looking | neutral | `border-zinc-700 text-zinc-400` |
| **Verification** | Verified (badge from labs) | success | emerald idiom + ✓ icon |
| | Experience pending | warning | amber idiom |
| | Unverified | neutral | zinc idiom |
| **Application** | Applied | info | sky idiom |
| | Shortlisted | success | emerald idiom |
| | Declined | danger | `border-red-500/40 bg-red-500/10 text-red-300` |
| | Hired | success (filled) | emerald, solid emphasis |
| **Bug-report severity** | Critical | danger | red idiom |
| | Major | warning(bug) | amber idiom |
| | Minor | info | sky idiom |
| | Cosmetic | neutral | zinc idiom |
| **NDA / private** | Locked | info | sky idiom + lock icon |

**Accessibility (verified on `#09090b` canvas — all AA pass):**

| Text color | Contrast | Verdict |
|---|---|---|
| `foreground #f4f4f5` | 18.1:1 | AA ✓ (normal) |
| `emerald-300` | 13.05:1 | AA ✓ |
| `amber-300` | 13.8:1 | AA ✓ |
| `sky-300` | 11.93:1 | AA ✓ |
| `red-300/400` | 10.5 / 7.2:1 | AA ✓ |
| `zinc-300 / 400` | 13.5 / 7.8:1 | AA ✓ |
| `zinc-500` | 4.12:1 | **large text only** — never body |
| Button: `zinc-950` on emerald-300/400 | 13.1 / 10.4:1 | AA ✓ |

> Rule: status text uses the `-300` step on the dark canvas (always ≥10:1). `zinc-500` is permitted for ≥18px/large only.

---

## 2. Component system (atomic)

New components live in `packages/ui/src/*` (shared) or `apps/platform/src/app/(app)/talent/_components/*` (feature-local). All match `button.tsx`/`badge.tsx` conventions.

### 2.1 Atoms

**`StatusBadge`** — extend the existing `Badge` tone union rather than fork it:
```tsx
// packages/ui/src/badge.tsx — widen Tone
type Tone = "default" | "success" | "warning" | "info" | "danger";
const TONE_CLASSES: Record<Tone, string> = {
  default: "border-zinc-700 text-zinc-300",
  success: "border-emerald-500/40 bg-emerald-500/10 text-emerald-300",
  warning: "border-amber-500/40 bg-amber-500/10 text-amber-300",
  info:    "border-sky-500/40 bg-sky-500/10 text-sky-300",
  danger:  "border-red-500/40 bg-red-500/10 text-red-300",   // ← new
};
```

**`VerifiedBadge`** — the trust signal (PRD's moat). Emerald, with score:
```tsx
export function VerifiedBadge({ skill, score }: { skill: string; score: number }) {
  return (
    <Badge tone="success" className="gap-1">
      <CheckIcon className="size-3" aria-hidden /> {skill} · {score}%
    </Badge>
  );
}
```

**`AvailabilityPill`**, **`SeverityTag`**, **`ApplicationStatusTag`** — thin wrappers that pick a tone from §1's mapping. One mapping object, no ad-hoc colors.

**`DeviceChip`** — the device-matrix unit (rare-on-other-marketplaces differentiator):
```tsx
// "iPhone 13 · iOS 17"  — mono, zinc, subtle
<span className="inline-flex items-center gap-1.5 rounded-md border border-zinc-800
  bg-zinc-900/60 px-2 py-1 font-mono text-xs text-zinc-300">
  <DeviceIcon kind={kind} className="size-3 text-zinc-500" /> {device} · {os} {osVersion}
</span>
```

### 2.2 Molecules

| Component | Tokens / idiom | Notes |
|---|---|---|
| **`TesterCard`** | `card` base + emerald accent ring on hover | Directory unit. **Proof-forward** (UX §1B): avatar, headline, top 3 specialties, 1–2 `VerifiedBadge`, device count, `AvailabilityPill`. Artifact thumbnail teaser. |
| **`ProjectCard`** | `card` + amber (`.bg-glow-bug`) micro-accent | Required testing-types as chips, stack chips, engagement, NDA lock if set. |
| **`FacetChip` / `FilterGroup`** | secondary-button idiom, toggled = emerald fill | The QA-native filters (specialty, stack, device toggle, availability, verified-only). Toggle state = `bg-emerald-500/15 border-emerald-500/50 text-emerald-200`. |
| **`PortfolioArtifactCard`** | `card`, type-tinted left border | bug_report (amber) / automation (emerald) / test_case (sky). Code uses `font-mono`; NDA → locked overlay. |
| **`ProfileStrengthMeter`** | emerald progress on zinc track | Directly serves UX §2A "Valley of Death" fix — shows payoff of completing fields. |
| **`MessageBubble`** | own = emerald-tinted, other = zinc | Realtime inbox. `read_at` → subtle zinc-500 tick. Respects `prefers-reduced-motion`. |

### 2.3 Organisms / templates

- **`TesterDirectory`** — filter rail + responsive card grid (see §3) + keyset "load more".
- **`PostProjectWizard`** — guided multi-step (UX: Devon often can't self-scope); progress uses `ProfileStrengthMeter` styling.
- **`ConversationThread`** — `MessageBubble` list + composer; consent-boundary banner ("you're connected via *Project X*").
- **`EmptyState` (cold-start critical)** — never a blank grid (UX §2B). Uses `.bg-grid` + `.grain` + a teal `.bg-glow`, an explanatory line, and a CTA. **Gate launch on this existing — an empty directory kills the client journey.**

### 2.4 Variant/size discipline
Reuse `button.tsx`'s three sizes implicitly (sm/md/lg via padding) and four variants (primary=emerald, secondary=zinc, ghost, danger=red). **No new button styles** — marketplace CTAs ("Contact", "Apply", "Post a project") are `primary`; "Shortlist" is `secondary`; "Report" is `ghost`/`danger`.

---

## 3. Responsive (web-first)

Use Tailwind's default breakpoints (already in use) — don't introduce a parallel scale.

| Surface | < `sm` (mobile) | `md` (640) | `lg` (1024) | `xl`+ |
|---|---|---|---|---|
| Tester directory grid | 1 col | 2 col | 3 col + filter rail | 3–4 col |
| Filter rail | top drawer (collapsible) | top drawer | left sticky rail | left sticky rail |
| Profile page | stacked | stacked | 2-col (proof / sidebar) | 2-col |
| Inbox | list↔thread (one at a time) | split when ≥ `md` | split | split |

**Touch targets ≥ 44×44px** on mobile (filter chips, pills get min-height). Fluid headings only where the marketing-grade hero appears; in-app uses the fixed display scale already in the app. Cards never exceed ~`max-w-sm` per column to keep the proof artifact legible.

---

## 4. Developer handoff

1. **Tokens:** add the five `--color-status-*` aliases to `globals.css @theme inline`. No JSON token pipeline needed — Tailwind v4 `@theme` *is* the token source, and `@source "../../../../packages/ui/src"` already pulls UI classes into the scan. (The skill's `design_token_generator.py` is intentionally **not** used — it emits a generic Inter/blue system that would fight the established brand.)
2. **Components:** widen `Badge` tone union (shared); add `VerifiedBadge`, `DeviceChip`, `StatusBadge` wrappers to `packages/ui`; keep `TesterCard`/`ProjectCard`/wizard feature-local under `talent/_components`.
3. **One mapping module:** `talent/_components/status.ts` exports the §1 state→tone map. Every status visual reads from it — zero inline color decisions (enforces "uses only design tokens").
4. **Icons:** match whatever the app already ships (lucide-style `size-3/size-4`); never color icons outside the zinc/emerald/amber/sky/red set.
5. **Motion:** transitions ≤200ms (`transition duration-200` like `button.tsx`); all gated by the existing `prefers-reduced-motion` block.

### Handoff checklist
- [ ] `--color-status-*` added to `@theme inline`
- [ ] `Badge` tone union widened to include `danger`
- [ ] `status.ts` mapping is the only place state→color lives
- [ ] Every new component uses `cn()` + `focus-visible:outline-2 outline-offset-2`
- [ ] Contrast re-checked for any *new* color (must hit AA on `#09090b`)
- [ ] Touch targets ≥44px; `EmptyState` implemented before directory launch
- [ ] No hardcoded hex in components (only token aliases / Tailwind scale steps)

---

## 5. Why this is on-brand (vs. a generated system)

A generated palette (Inter font, blue-600 primary, fresh neutral ramp) would have been **wrong** here: it ignores the deliberate zinc/teal/amber restraint, the Bricolage/Geist/Instrument-Serif type voice, and the dark-first atmosphere utilities that make QA Mastery feel like itself. The marketplace must read as *the same product, new surface* — so the entire contribution is **semantic** (new states) and **compositional** (new components), built from the exact primitives already in `packages/ui`. That consistency is also a trust signal: a hiring surface that looks native to the learning app inherits its credibility.
