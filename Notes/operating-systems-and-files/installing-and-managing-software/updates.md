---
title: "Updates"
tags: ["computer-basics", "software", "security", "track-a"]
updated: "2026-07-10"
---

# Updates

*Why 'Remind me tomorrow' is a security decision, what version numbers actually promise, and why updates are simultaneously the most important and most dangerous thing your software does.*

> You have clicked "Remind me tomorrow" so many times the button has worn a groove in
> your soul. Meanwhile, every one of those postponed updates was mostly a list of holes
> someone found in your software and published on the internet. Updates are the least
> glamorous topic in computing and the one with the highest ratio of consequence to
> attention. Also — and this is the honest part — sometimes the update is the bug.

> **In real life**
>
> An update is **a locksmith replacing your lock, live, while you're in the house.**
> Usually excellent: the old lock had a flaw and burglars now know it. Occasionally
> catastrophic: the new lock doesn't fit, and you're standing outside your own house at
> midnight. Both things are true at once, and "just always update immediately" and
> "never update" are both the reasoning of someone who has only lived through one of the
> two stories.

## What a version number is actually telling you

Most software uses **semantic versioning**: Semantic Versioning: MAJOR.MINOR.PATCH. Bump PATCH for backwards-compatible bug fixes, MINOR for backwards-compatible new features, MAJOR for breaking changes. A convention, not a law — but a widely honored one.: `MAJOR.MINOR.PATCH`.

- `2.4.1 → 2.4.2` — **patch.** Bug fixes and security holes plugged. Nothing you use should change. Take it.
- `2.4.1 → 2.5.0` — **minor.** New features, nothing removed. Safe by convention.
- `2.4.1 → 3.0.0` — **major.** Something you rely on may be gone or changed. Read the release notes. Actually read them.

That single dot-shift is a promise about how much your life is about to change. It's a
promise made by humans, so it's occasionally broken — but as a first-glance risk
signal, nothing beats it.

![A package manager listing installed packages with their installed and latest available versions](package-manager.png)
*Screenshot: Synaptic Package Manager on Debian — Wikimedia Commons, CC0. [Source](https://commons.wikimedia.org/wiki/File:Synaptic_Package_Manager_on_Debian_Trixie.png)*
- **Installed version vs latest version** — Two columns, one gap. That gap is your exposure: every version between them contains fixes you don't have. This is the single most honest screen on any computer, and it's usually buried three menus deep.
- **The package list — dependencies, all of them** — Not just apps: the shared libraries apps rely on. Update one library, dozens of apps get the fix at once. That's the whole point of a package manager, and why Linux updates feel different from Windows ones.
- **Refresh / reload — check for news first** — Your machine's list of 'what's available' is a cached copy. Refresh it before believing 'no updates available'. Same shape as note-4's index problem: stale index, confident wrong answer.
- **Descriptions — the release notes' cousin** — 'Fixes CVE-2026-XXXX' is a sentence worth reading. CVE = a publicly catalogued vulnerability. If your version is listed, the hole is public knowledge and you are the last person to hear about it.
- **Apply / Mark for upgrade** — The moment of the four steps again (copy, register, permissions, shortcut) — an update is just an install of a newer version over an older one, with all the same failure modes plus one: the new version might behave differently.

**The life of a security patch — press Play**

1. **🕵️ Someone finds a hole** — A researcher (or an attacker) discovers a flaw in software you run. Right now, nobody but them knows. This is the safest your software will ever be while being fully broken.
2. **🔒 Quiet fix** — They report it privately. The vendor writes a patch. Still nobody knows. The clock starts: typically 90 days before public disclosure.
3. **📢 Patch ships + hole goes PUBLIC** — The update is released AND the vulnerability is published (as a CVE) so everyone can check whether they're affected. The moment the fix exists, the flaw becomes public knowledge. Read that sentence twice.
4. **⏰ You click 'Remind me tomorrow'** — Attackers read the same public disclosure — and now they also have the patch, which is a precise map of what was broken. Unpatched machines become the easiest targets on the internet. The window between 'patch released' and 'you installed it' is when almost all real-world compromise happens.
5. **✅ You update** — Hole closed. Total effort: 90 seconds and one restart. The asymmetry between that cost and the alternative is the entire argument, and it's why the security track will make you say this out loud.

*Try it — compare versions like a package manager does*

```python
def parse(v):
    return tuple(int(x) for x in v.split("."))

def classify(old, new):
    o, n = parse(old), parse(new)
    if n <= o:            return "no update (or a downgrade — suspicious!)"
    if n[0] > o[0]:       return "MAJOR — may break things. READ THE RELEASE NOTES."
    if n[1] > o[1]:       return "minor — new features, nothing removed. Safe."
    return "patch — bug + security fixes only. Take it now."

pairs = [("2.4.1","2.4.2"), ("2.4.1","2.5.0"), ("2.4.1","3.0.0"), ("3.0.0","2.9.9")]
for old, new in pairs:
    print(f"{old} -> {new:8} {classify(old, new)}")
print()

# Why string comparison is a REAL bug in real software:
print("'9' > '10' as strings?", "9" > "10")     # True! Alphabetical, not numeric.
print("parse('9') > parse('10')?", parse("9") > parse("10"))
print()
print("Version 1.9 vs 1.10: sorted as text, 1.9 wins and you never get the update.")
print("Testers: sort-by-version and pick-the-latest are famous bug factories.")
print("Try feeding this function '1.10.0' vs '1.9.0' and watch it get it RIGHT —")
print("then imagine the code that used string comparison instead.")
```

## The three kinds of update, ranked by "should I click now"

1. **Security patches** (OS, browser, anything touching the internet) — **immediately.** The FlowAnimation is why. There is no clever reason to wait.
2. **Bug-fix patches** — soon. Low risk, real benefit.
3. **Major versions / feature releases** — deliberately. Read the notes. On a machine you depend on for work, waiting a week while other people find the new bugs is not cowardice, it's strategy.

> **Tip**
>
> Enable automatic updates for your **OS and browser**, always. Those two are the entire
> attack surface for most people. Leave manual control over big apps whose workflows you
> depend on. That's not inconsistency — it's matching your update policy to the actual
> cost of being wrong in each direction. Being wrong about a browser patch can cost you
> your accounts; being wrong about a major version of your editor costs you an afternoon.

### Your first time: Your mission: close your update gap

- [ ] Check your OS version and its latest — Windows: Settings → Windows Update. Mac: System Settings → General → Software Update. Linux: your software center. Note the gap between what you run and what exists.
- [ ] Update your browser NOW — It's the program most exposed to hostile input on earth: every page you visit is untrusted code. Help → About usually updates it while you read. Do it before finishing this note.
- [ ] Turn on automatic OS + browser updates — This is the single highest-value security action available to a normal human, and it takes 30 seconds.
- [ ] Read one release note — Pick any app's 'What's new'. Find a line like 'fixed a crash when...' or 'security fix'. Real humans found and fixed that. Updates are other people's debugging, delivered to you free.
- [ ] Run the playground and break version comparison — See why '1.9' > '1.10' as strings. Then remember it when a test compares version strings — you now own a bug nobody else on your team is looking for.

Update gap closed, auto-updates on, and one release note actually read. You're now in the top 10% of computer users. Grim, but true.

- **The update broke my app. It worked yesterday.**
  It happens, and it's exactly why 'always update instantly' is advice with an asterisk. Fix in order: (1) restart — half of post-update weirdness is stale state; (2) check the release notes for a known issue; (3) roll back if the app supports it; (4) report it, with your version numbers, both old and new. You are now the person who found the regression, which is a genuinely valuable role — that's most of what QA IS.
- **'No updates available' — but I know a newer version exists.**
  Your machine's catalogue of available versions is a CACHED copy. Refresh/reload it first (the pin on the package-manager screenshot). Same lesson as search's index in the last chapter: the tool isn't lying, it's answering from a stale snapshot. If it's still absent, the update may not be rolled out to your region/hardware yet — staged rollouts are normal.
- **The update downloaded but won't install — 'not enough space'.**
  Updates need room for BOTH versions during the swap (the new files must exist before the old ones can go). A 2 GB update can need 5 GB free. Clear space and retry. This surprises people because they think an update replaces files in place; it mostly doesn't — it stages, verifies, then switches.
- **My machine restarted on its own and I lost work.**
  Auto-update finished and forced a reboot. Infuriating, defensible, and configurable: set 'active hours' (Windows) or schedule updates overnight (Mac). Don't disable updates to solve this — you'd be fixing a rudeness problem with a security hole. Fix the schedule, keep the patches.

### Where to check

Your update surface, in priority order:

- **OS update settings** — the biggest surface. Auto-on. Check the gap monthly anyway.
- **Browser → Help → About** — updates while you look at it. The most exposed program you run.
- **Installed apps list** — versions, side by side with latest. The gap column is the honest one.
- **Release notes / changelog** — the only place that tells you WHAT changed. Nobody reads them; everybody has opinions about updates anyway.
- **CVE databases** (later, in Track E) — public catalogues of known vulnerabilities by product and version. Terrifying and useful.

Tester's angle: **the update path is a test path nobody tests.** Install v1, use it,
create data, then upgrade to v2 and check your data survived. Migration bugs live
exclusively in that transition and are invisible to anyone who only ever tests fresh
installs. This is a well-paid specialty and almost nobody does it on purpose.

### Worked example: the upgrade that ate the settings

A migration bug, found by a tester who thought about the transition:

1. **The naive test:** install v2.0 fresh, open it, everything works. Ship it. This is what most teams check.
2. **The tester's test:** install v1.9 first. Configure it — change the theme, add three saved filters. Use it like a human for five minutes. THEN upgrade to v2.0.
3. **Result:** the app opens with default settings. The saved filters are gone. The theme is reset.
4. **Why:** v2.0 changed where settings are stored (a new folder, a new format) and the migration code that should copy the old settings across ran only when a specific file existed — a file v1.9.x stopped creating two patches ago.
5. **Nobody caught it** because fresh installs have nothing to migrate, and the developers' own machines had that legacy file lying around from years of testing. The bug is invisible from both of the two most common vantage points.
6. **The general lesson:** the upgrade path is a distinct product from the fresh-install path. Data has to survive a transition, and transitions are where software forgets things. Test the transition, not just the destination.

> **Common mistake**
>
> Postponing security updates because "nothing bad has happened yet." The patch and the
> public disclosure of the hole ship *at the same time* — so the moment a fix exists, the
> flaw is documented, and the patch itself is a map of what to attack in machines that
> haven't applied it. Delay doesn't preserve a safe status quo; it converts a private
> flaw into a public one that you specifically still have. The FlowAnimation is not a
> scare tactic, it's the actual sequence, and "Remind me tomorrow" is a decision made
> inside step 4 of it.

**Quiz.** A vendor releases a patch for a serious flaw and publishes the CVE the same day. You postpone the update for two weeks. How does your risk change over those two weeks?

- [ ] It stays the same — the flaw existed before the patch too
- [x] It goes up sharply: the disclosure tells attackers the flaw exists, and the patch itself reveals precisely what was broken. Unpatched machines go from 'nobody knows' to 'publicly documented and easy to find', which is when most real-world compromise happens.
- [ ] It goes down, because attackers move on to newer flaws
- [ ] It only matters if you use the app daily

*Before disclosure, the flaw is a secret held by few. Publication flips it into public knowledge, and the patch is a diff showing exactly which code was wrong. Attackers read both. The window between 'patch released' and 'patch applied' is the highest-risk period in a vulnerability's life — the opposite of most people's intuition that waiting is the cautious choice.*

- **MAJOR.MINOR.PATCH** — Patch = bug/security fixes, take it. Minor = new features, nothing removed. Major = may break things, read the release notes. A promise about how much your life changes.
- **Why patch immediately?** — The fix and the public disclosure of the flaw ship together. The patch is a map of what was broken. Waiting converts a private flaw into a public one that you still have.
- **Update = install** — Same four steps (copy, register, permissions, shortcut) with one extra risk: the new version may behave differently. All install failure modes apply, plus regressions.
- **Update policy that makes sense** — Auto-update OS and browser (max exposure, low breakage risk). Update big work-critical apps deliberately, after reading notes. Match policy to cost of being wrong.
- **The upgrade-path test** — Install old → configure → use → upgrade → check data survived. Migration bugs are invisible to fresh-install testing. Almost nobody does this; it's a specialty.
- **String version comparison bug** — '1.9' > '1.10' alphabetically. Compare versions as tuples of integers, never as text. A classic real-world defect.

### Challenge

Update your browser right now (Help → About, it updates as you watch). Then find any
app on your machine and open its changelog. Count how many entries say "fixed" or
"security". Every one of those was somebody's bug report — possibly from a tester who
did exactly what you're learning to do. Then, for the real exercise: install an old
version of something, configure it, upgrade it, and check whether your settings
survived. If they didn't, congratulations — you just found a migration bug on your
first attempt, which happens more often than the industry would like to admit.

### Ask the community

> Update question: [app] on [OS], upgrading [old version] → [new version]. Symptom: [what broke / what won't install]. Release notes mention: [relevant line, or 'nothing about this']. Fresh install of the new version: [works / same problem]. Rollback possible: [yes/no]

That 'fresh install: works / same problem' line splits the entire diagnosis in half:
works-fresh means it's a migration bug (your old data or settings), same-fresh means
it's a plain regression. Most people never think to run that test, and it's the single
most informative thing you can bring to an update thread.

- [Semantic Versioning — the spec behind MAJOR.MINOR.PATCH](https://semver.org/)
- [CISA — vulnerabilities actively being exploited right now](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [Why software updates matter more than you think](https://www.youtube.com/watch?v=8_SuuJ_1nAA)

🎬 [Why you should install that update](https://www.youtube.com/watch?v=8_SuuJ_1nAA) (7 min)

- MAJOR.MINOR.PATCH is a promise: patch = fixes (take it), minor = additions (safe), major = possible breakage (read the notes).
- The security patch and the public disclosure of the flaw ship together — so postponing an update raises your risk sharply rather than preserving safety.
- An update is an install of a newer version: same four steps, same failure modes, plus the risk of regressions.
- Sensible policy: auto-update OS and browser; update work-critical apps deliberately after reading release notes.
- The upgrade path (old → configure → new) is a distinct test from the fresh install, and migration bugs live only there. Almost nobody tests it.


---
_Source: `packages/curriculum/content/notes/operating-systems-and-files/installing-and-managing-software/updates.mdx`_
