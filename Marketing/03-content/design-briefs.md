# Design Briefs — Marketing Visuals

Briefs for the visual assets in [`../04-designs/`](../04-designs/). Each is built as self-contained HTML and exported to Adobe Express / Canva for final editing. Brand below; then per-asset briefs.

## Brand kit
- **Name:** QA Mastery
- **Positioning line:** "You don't watch testing — you do it."
- **Tone:** confident, practical, slightly rebellious vs passive video courses.
- **Colors (suggested — confirm against the live app):**
  - Ink / base: `#0F172A` (slate-900)
  - Primary: `#6D28D9` (violet-700) — knowledge/credibility
  - Accent / "bug": `#F43F5E` (rose-500) — the bug you hunt
  - Success / "graded": `#10B981` (emerald-500) — passing
  - Surface: `#F8FAFC`
- **Type:** a strong geometric sans for headlines (e.g., Sora / Space Grotesk), clean sans for body (Inter). Confirm via `font_recommend`.
- **Motif:** a bug icon being "caught" / a checkmark. Terminal/code texture for the automation audience.

---

## Asset 1 — Launch announcement (square 1080×1080, LinkedIn/IG)
- **Headline:** "QA Mastery is live."
- **Sub:** "Learn testing by doing — on a real buggy app. Graded like a real job."
- **Visual:** BuggyShop UI hint + a bug caught in a checkmark.
- **Footer:** free first module · [domain]

## Asset 2 — Differentiator carousel (1080×1350, 5 slides)
1. "You can watch 100 hrs of Selenium and still freeze on day one."
2. "Because watching ≠ doing."
3. "Meet BuggyShop — a shop full of real seeded bugs."
4. "Find them. File real reports. Get graded."
5. "You don't watch testing. You do it. → free module"

## Asset 3 — "You asked, we built it" template (1080×1080, reusable)
- Top: "YOU ASKED 💬" → the request.
- Bottom: "WE BUILT IT ✅" → what shipped.
- Keep it a template: swap text each time you ship from feedback.

## Asset 4 — "7 fields of a great bug report" carousel (1080×1350, 8 slides)
- Cover + 7 field slides (Title, Steps, Expected, Actual, Severity, Environment, Evidence) + CTA slide.
- Doubles as a lead magnet (highest-saved content type).

## Asset 5 — LinkedIn banner (1584×396)
- "QA Mastery — learn testing by doing." + practice/graded/portfolio keywords + domain.

---

## Build order
1. Asset 1 (launch) — needed Week 1.
2. Asset 4 (bug-report carousel) — Week 1 teach post + evergreen lead magnet.
3. Asset 2 (differentiator) — Week 2.
4. Asset 3 (you-asked template) — before Week 4.
5. Asset 5 (banner) — anytime Week 1.

Production path: HTML → `html_export_readiness_skill` → `export_html_to_express` → edit/export in Express or Canva. See `../04-designs/README.md`.
