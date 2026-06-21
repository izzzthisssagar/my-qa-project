# External Feedback Form — Spec (Tally or Google Forms)

Build this once in **Tally** (free, prettier, no Google login needed) or **Google Forms** (free, exports to Sheets). Drop the link in your LinkedIn bio, post CTAs, Reddit comments, and the in-app "send feedback" fallback.

**Goal:** Capture feedback from *anyone* — including people who haven't signed up. Keep it under 60 seconds or people bounce.

---

## Questions

1. **What's your situation?** (single choice → maps to `user_segment`)
   - Trying to get my first QA job (career switcher)
   - Manual tester wanting automation
   - Experienced / aiming for lead
   - Just curious / other

2. **What kind of feedback is this?** (single choice → maps to `type`)
   - I found a bug
   - I want a feature
   - Something was confusing (UX)
   - I want different/more content
   - About pricing
   - Just praise / something I loved

3. **Tell us — what do you want or what went wrong?** (long text → `raw_text`) *(required)*

4. **If we could fix/build ONE thing for you, what would it be?** (long text)
   - This single question surfaces your highest-RICE items. Gold.

5. **How did you hear about QA Mastery?** (single choice → feeds signup-source log)
   - LinkedIn / Reddit / Google search / Friend / Community / Other

6. **Email (optional — only if you want a reply when we ship it)** (email → `email`)
   - Permission to close the loop = future testimonial + retention.

---

## Settings
- Turn ON: "allow multiple responses" (people give feedback more than once).
- Turn OFF: required login (kills cold feedback).
- Tally → connect to a Google Sheet, OR export CSV weekly.
- Map the export columns to `feedback-intake.csv` headers before running the triage script (the script expects: `source,user_segment,type,raw_text,theme,reach,impact,confidence,effort,status` — fill reach/impact/confidence/effort during Friday triage, not in the form).

## Where the link goes
- LinkedIn bio + every "what's missing for you?" post
- Reddit/MoT comments where relevant (not spammy)
- In-app feedback widget "having trouble? tell us here" fallback
- Email signature
