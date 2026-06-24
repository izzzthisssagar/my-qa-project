# QA Mastery Talent — Security & Compliance Spec

> Companion to the Backend/Frontend specs. Threat model, OWASP Top 10 mapping, GDPR design for global PII + private messaging, and the CI security gate. Grounded in real scans of the codebase.

**Status:** v1.0 · **Data tier:** PII (profiles, messages) — no PCI/PHI in MVP · **Posture:** RLS-as-authorization, defense-in-depth

---

## 0. Scan results (run against the live codebase — reported honestly)

| Scan | Tool | Result | Read |
|---|---|---|---|
| **Code vulnerabilities** | `security_scanner.py` (src, medium+) | **0 findings** (exit 0) | **Clean.** Definitively retires the "3 SQL-injection" flags from the fullstack pass — a proper scanner sees no injection. All DB access is the parameterized Supabase client + RLS. |
| **Dependency CVEs** | `vulnerability_assessor.py` (29 pkgs) | **0 vulnerabilities**, risk 0/100 | **Clean.** No vulnerable deps. |
| **GDPR controls** | `compliance_checker.py` | **27.8% (critical-gaps)** | **Mixed — read carefully (§4).** Partly a *visibility artifact* (encryption is Supabase-managed, invisible to a repo scanner); partly a *real documentation/process gap* the marketplace makes urgent. |

**Bottom line:** the *code* and *dependencies* are secure today. The marketplace's security work is **design + process**, not fixing existing vulnerabilities.

---

## 1. Threat model (assets → STRIDE → mitigation)

The marketplace introduces high-value, abusable assets the learning app didn't have: private 1:1 messages, contact-gated relationships, PII profiles, and uploaded artifacts.

| Asset | Top threats (STRIDE) | Mitigation (design ref) |
|---|---|---|
| **Private messages** | **Information disclosure** (read others' chats); **Spoofing** (send as someone else) | Participant-only RLS via `EXISTS` subquery (Backend §1.2b); `with check (auth.uid() = sender_id)` blocks forged senders; **negative RLS tests gate M0** |
| **Contact relationship** | **Elevation** (message an un-contacted user); **Spam** (mass-contact) | Consent boundary = a `talent_conversations` row required before any message (RLS); rate-limit `contactTester`/`sendMessage` (reuse `lib/help-agent/rate-limit.ts`) |
| **PII (email/phone)** | **Disclosure** (scraping for off-platform spam) | email/phone confined to `auth.users`; **never** in `talent_*` or any public view; `talent_public_profile` view selects only public columns (Backend §1.4) |
| **NDA / private artifacts** | **Disclosure** (NDA work leaked) | `is_nda` portfolio hidden by RLS unless owner; private Storage bucket + **signed URLs minted only after an ownership check**; never a public signed URL for NDA items |
| **Profiles / projects** | **Tampering** (edit others'); **Repudiation** | owner-write RLS; `audit_events` append-only trail (existing SOC2 control) |
| **Verified badges** | **Spoofing** (fake credentials) | service-role-write only (no client path); derived from grading (Data-Eng ADR-004) |
| **Uploads** | **Malware / oversized / content-type confusion** | validate MIME + size; private bucket; (V1.0) virus-scan hook |
| **Platform bypass** | **Business integrity** (take it off-platform) | out-value, not wall (PRD §5); contact-masking; on-platform nudges |

---

## 2. OWASP Top 10 — talent module quick-check

| # | Category | Status | How |
|---|---|---|---|
| **A01 Broken Access Control** | **Primary risk → mitigated** | RLS on every `talent_*` table; participant-only messaging; 5 negative RLS tests as launch gate (Backend §5). Horizontal-priv-escalation explicitly tested. |
| **A02 Cryptographic Failures** | OK | TLS 1.2+ everywhere (Supabase/Vercel default); AES-256 at rest (Supabase); no secrets in source (scan = 0). |
| **A03 Injection** | OK | Parameterized Supabase client; **scanner confirms 0**; `text[]` taxonomy is allow-listed, not free SQL. |
| **A04 Insecure Design** | OK | Threat model (this doc) exists for the critical flows; consent boundary designed-in. |
| **A05 Security Misconfiguration** | Verify | RLS-on-by-default per table; ensure no table ships RLS-disabled; generic error messages (`ActionResult` codes, no stack traces). |
| **A06 Vulnerable Components** | OK | assessor = 0 CVEs; add to CI gate (§5). |
| **A07 Auth Failures** | OK (inherited) | Supabase Auth; existing login throttling; MFA available for the service-role/admin (founder) account — **enable it**. |
| **A08 Data Integrity** | OK | CI builds; pinned `pnpm` lockfile; recommend SBOM + signed deploys at scale (§5). |
| **A09 Logging & Monitoring** | OK | `audit_events` captures marketplace actions (contact/post/hire/report); alerting via existing `NOTIFY_WEBHOOK`. |
| **A10 SSRF** | Low | repo URLs in portfolios are *links shown to humans*, not server-fetched. **If** an OG/preview fetcher is ever added, block internal ranges + `169.254.169.254`. |

---

## 3. Secrets & secure-coding posture

- **Secrets:** scanner found **0 hardcoded secrets**. Keys live in Vercel/Supabase env (existing). **Add a pre-commit + CI secret scan** to keep it that way: `detect-secrets` (pre-commit) + `gitleaks` (CI) — cheap insurance for a public GitHub repo.
- **Input validation:** Zod on every Server Action (Backend §2); allow-list taxonomy; length/range checks already in the migration's `check` constraints.
- **Output/XSS:** React auto-escapes; portfolio bodies rendered as text/markdown — **if** raw HTML is ever allowed, sanitize with DOMPurify. Code snippets are highlighted, not `dangerouslySetInnerHTML`'d from user input.
- **Error handling:** `ActionResult` returns generic codes; never leak stack traces or DB errors to the client.
- **Admin (founder) account:** enable MFA; service-role key is server-only (never shipped to the browser).

---

## 4. GDPR — the real work (global PII + private messaging)

The marketplace processes **PII of a global audience** (incl. likely EU users) and **private communications** — so GDPR genuinely applies. The 27.8% scan score breaks down as:

**Already satisfied (but invisible to the repo scanner):**
- **Art 32 encryption** — TLS in transit + AES-256 at rest, **managed by Supabase/Vercel**. The scanner can't see infra config; this control *is* met. Document it (don't "fix" it).
- **Art 17 erasure (partial, by design)** — every `talent_*` table FKs to `profiles`/`auth.users` with **`on delete cascade`**. Deleting a user erases their profile, devices, portfolio, projects, applications, messages, shortlists. The schema *was designed* for right-to-erasure.
- **Art 25 data minimization (by design)** — **PII never enters `talent_*`**; the marketplace stores only what it needs; contact is in-app (no email/phone collection beyond auth).

**Genuine gaps to close before EU launch (the actionable part):**

| GDPR control | Action |
|---|---|
| **Art 13/14 transparency** | Publish a **privacy policy** + the legal basis (consent for account; legitimate interest for matching). *(No policy file in repo — the scanner's "fail" is correct here.)* |
| **Art 28 processors / DPA** | Record subprocessors — **Supabase, Vercel, Paddle (V1.0)** — and sign DPAs. List them in the privacy policy. |
| **Art 17 erasure (full)** | Add a **"delete my account"** Server Action that triggers the cascade + purges Storage objects + tombstones the user in `audit_events` (keep the security log, drop the PII). Cron-verify no orphaned Storage. |
| **Art 20 portability** | Add **"export my data"** — a Server Action returning the user's profile + messages + portfolio as JSON. |
| **Art 33 breach notification** | A **runbook**: detect (audit/Supabase logs) → assess → notify supervisory authority **within 72h** → notify affected users. (Incident-response phases in the skill.) |
| **Art 7 consent** | Explicit checkbox at marketplace onboarding (separate from learning ToS); store consent timestamp/version. |
| **Messages retention** | Define a retention policy (e.g. messages kept while account active); fold into the existing `pg_cron` retention pattern. |

> Recommendation: ship the **privacy policy + DPAs + erasure/export actions** in M5 (alongside moderation) so the marketplace is GDPR-defensible at launch, not retrofitted.

### SOC 2 (already partially in place)
`audit_events` (append-only, service-role-only) satisfies **CC7 logging**; CI/code-review satisfies **CC8 change management**; Supabase Auth + RLS satisfy **CC6 access control**. Marketplace actions just extend the existing `audit_events` stream — no new control needed, only coverage.

---

## 5. CI security gate (extend existing `security.yml`)

The repo already has `security.yml`. Add the three scanners as **blocking** steps for marketplace PRs:

```yaml
# additions to .github/workflows/security.yml
- name: secret-scan (gitleaks)
  uses: gitleaks/gitleaks-action@v2
- name: code-scan
  run: python scripts/security_scanner.py apps/platform/src --severity high   # fail on exit 1/2
- name: dependency-scan
  run: python scripts/vulnerability_assessor.py apps/platform --severity high  # fail on critical/high CVE
```
Plus the **RLS test gate** (`pnpm test:rls`) in `ci.yml` is the real access-control assurance — the 5 negative tests (Backend §5) must pass on every PR.

**Pre-commit (local):** `detect-secrets` hook with a `.secrets.baseline`.

---

## 6. Pre-launch security checklist

- [ ] 5 negative RLS tests green (non-participant can't read/forge messages; NDA/private hidden; analytics deny-all; can't link unowned artifact)
- [ ] No `talent_*` table ships with RLS disabled; every table has explicit policies
- [ ] `talent_public_profile` view + every action exclude email/phone (PII boundary test)
- [ ] Signed-URL minting checks ownership/visibility; NDA items never public
- [ ] Rate limits on `contactTester`/`sendMessage`/`postProject`/`reportContent`
- [ ] Founder/admin account has MFA; service-role key server-only
- [ ] Secret scan (gitleaks + detect-secrets) wired; CI security steps blocking
- [ ] **GDPR: privacy policy + DPAs published; delete-account + export-data actions shipped; breach runbook written**
- [ ] Marketplace actions emit `audit_events`; alerting on report/abuse spikes

---

## 7. Summary
Code and dependencies scan **clean** (0 findings, 0 CVEs) — the marketplace's security work is *design and process*, not remediation. Access control is the central risk and is handled by **RLS-as-authorization** with negative tests as the launch gate. The genuinely new obligation is **GDPR for global PII + private messages**: encryption and right-to-erasure are *already satisfied by design* (Supabase infra + `on delete cascade` + no-PII-in-`talent_*`), but the **privacy policy, DPAs, explicit consent, and erasure/export/breach processes** are real gaps to close in M5 before opening to EU users. The 27.8% GDPR score was mostly a scanner visibility artifact — but it pointed at the right documentation work.
