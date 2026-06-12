# QA Mastery — Validation Landing Site

One self-contained `index.html`. No build step, no dependencies, no backend.

## What's on the page
1. **Hero** + waitlist CTA
2. **Boundary Hunter** (working widget) — quantity field 1–99 with a seeded off-by-one bug at 0
3. **Find the Bug** (working widget) — signup form with 3 seeded bugs: broken email regex, paste-bypasses-confirm-check, double-click-bypasses-terms (+ a wrong-field error message as a free extra for sharp eyes)
4. **Curriculum preview** — Tracks A & B
5. **Waitlist form** — needs Formspree connected (below)

## Setup step 1 — Connect the waitlist form (5 min)
1. Go to formspree.io → sign up free → **New form** → name it "QA Mastery waitlist".
2. Copy your form ID (looks like `xqkrgwyz`).
3. In `index.html`, find `YOUR_FORM_ID` and replace it: `action="https://formspree.io/f/xqkrgwyz"`.
4. The "form not connected" notice disappears automatically once the ID is real.

Free tier = 50 submissions/month. Enough for validation; upgrade only if you're winning.

## Setup step 2 — Deploy free (5 min)
**Netlify (easiest):** app.netlify.com → "Add new site" → "Deploy manually" → drag the `landing-site` folder onto the page. Done — you get a live URL like `qa-mastery.netlify.app`.
**Custom domain (optional):** buy the domain, add it in Netlify → Domain settings.

## Setup step 3 — Measure (before you share anything)
- Add a free analytics snippet (Netlify Analytics, or paste a PostHog/Plausible script tag before `</head>`).
- The metrics that matter for the kill/continue gate (plan §12): visitors → widget interaction rate → waitlist signups. Target from the plan: **50–100 genuine signups in ~2 weeks of community promotion.**

## Testing checklist (do this yourself — you're the QA)
- [ ] Slider: drag to 0 → green "Accepted" + bug banner appears
- [ ] Slider: 100 rejected, 99 accepted, 1 accepted
- [ ] Form bug 1: submit with email `a@@b..com` (everything else valid) → account created → Bug #1 marked
- [ ] Form bug 2: password `Pass@123`, PASTE a different value into Confirm → submits → Bug #2 marked
- [ ] Form bug 3: leave terms unchecked, double-click Create account fast → Bug #3 marked
- [ ] All 3 found → trophy banner with waitlist link
- [ ] Hints button cycles 3 hints
- [ ] Waitlist form submits to Formspree after setup (test with your own email)
- [ ] Check on a phone (responsive)

## Known intentional behaviors
- Short password shows "Username is invalid." — that's the BS-002 easter egg, intentional.
- The whole signup form is a demo; no data is stored anywhere.
