# Generates notes-v3-2-final-check.html — the final gap report + resource library, for approval.

C = lambda t, topics: (t, topics)

# ---------- gaps: additions that slot into EXISTING modules ----------
slot_ins = [
 dict(module="QA foundations", track="C", chapter="Where QA came from",
   topics=["the 1947 moth story (and the myth)","five eras: debugging → prevention","the pioneers & their big ideas","how agile, DevOps & AI reshaped QA"],
   why="You asked for the full background — who/when/why/how QA started and developed. Gelperin & Hetzel's five eras (debugging-oriented pre-1956 → demonstration → destruction (Myers 1979: a good test FINDS bugs) → evaluation → prevention from 1988) is the standard frame; pioneers covered: Grace Hopper, Glenford Myers, Cem Kaner (context-driven), James Bach & Michael Bolton (testing vs checking), Lisa Crispin & Janet Gregory (Agile Testing)."),
 dict(module="QA foundations", track="C", chapter="The tester’s mind",
   topics=["critical thinking for testers","cognitive biases (confirmation, overconfidence…)","curiosity & questioning","psychology of tester–developer relations"],
   why="Recurring in every 2026 skills survey and a Ministry of Testing course subject — testers prize critical thinking but fall for the same biases as everyone; naming them makes better testers."),
 dict(module="Levels & types of testing", track="C", chapter="Static testing & reviews",
   topics=["static vs dynamic, properly","reviews: informal → walkthrough → inspection","static analysis tools","review checklists that work"],
   why="A whole ISTQB Foundation chapter (Ch. 3) that the map only brushed — reviews find defects cheaper than any test execution."),
 dict(module="Non-functional testing (intro)", track="C", chapter="Localization & i18n",
   topics=["i18n vs l10n in plain words","text expansion, truncation & RTL","dates, currencies & formats","pseudo-localization tricks"],
   why="Standard specialization missing from the map; Applitools/localization guides show the classic bug families (overflow, hard-coded strings) every tester meets on global products."),
 dict(module="Playwright", track="D", chapter="Visual regression testing",
   topics=["pixel vs AI diffing","Playwright snapshots","Percy / Applitools / BackstopJS","taming false positives"],
   why="2026 tooling reviews show visual testing split into AI-diffing platforms vs framework snapshot libraries — a distinct skill job posts now name."),
 dict(module="API test automation", track="E", chapter="Mocking & service virtualization",
   topics=["stubs, mocks & fakes","WireMock hands-on","record & playback","simulating errors, latency & chaos"],
   why="Testing without waiting on real dependencies (third-party APIs, payment gateways) — WireMock-style virtualization is how teams unblock QA and test failure scenarios safely."),
 dict(module="Test management & reporting", track="F", chapter="Environments & test data",
   topics=["dev / QA / staging / prod","environment parity & config","test data management & anonymization","GDPR & sensitive data in tests"],
   why="Test-data management and environment strategy surfaced as the classic “nobody teaches this” gap — and it's daily friction in real teams."),
 dict(module="Test management & reporting", track="F", chapter="Risk & estimation",
   topics=["risk-based testing","prioritizing what to test first","test estimation techniques","saying no with data"],
   why="ISTQB Ch. 5 territory the map under-covered; estimation and risk-ranking are the skills that separate seniors from juniors."),
 dict(module="Your first 90 days", track="G", chapter="Domains & specializations",
   topics=["payments & fintech testing","ERP / CRM & enterprise","games, IoT & embedded","picking a niche deliberately"],
   why="Domain knowledge is a hiring multiplier — payment-domain interview banks and IoT/ERP testing guides show each domain has its own bug families worth a taster tour."),
]

# ---------- gaps: NEW modules ----------
sysdesign_module = dict(
 title="How systems are built — system design for testers", track="C", level="Core QA",
 place="Track C · new module after “API testing fundamentals”",
 why="Your call: testers must know the system they test, not just its screens. System-design guides (ByteByteGo, System Design Handbook, web-architecture 2026 references) show the request lifecycle — load balancer → server → cache → DB → queue — and each hop is a bug family a tester should recognize. It also doubles as developer knowledge and interview material.",
 chapters=[
  C("The big picture", ["frontend, backend & the database","life of a request, end to end","client-side vs server-side rendering","reading an architecture diagram"]),
  C("Architecture styles", ["monolith vs microservices","layers & MVC, gently","APIs as the glue","third-party services & webhooks"]),
  C("Scaling building blocks", ["load balancers","caching (Redis) & its bugs","message queues & async work","CDNs & static assets"]),
  C("Where bugs live, layer by layer", ["UI-layer bug families","API & integration bug families","data-layer bug families","infra & config bug families"]),
  C("From architecture to test strategy", ["what to test at which layer","integration points = risk","asking devs the right questions","drawing the system before testing it"]),
 ])

ai_module = dict(
 title="AI & the modern tester", track="F", level="Core QA",
 place="Track F · new module after “Test management & reporting”",
 why="The biggest 2026 shift the map didn't cover. Two sides: using AI to test better, and testing systems that contain AI. Sources: qaskills.sh 2026 guides, awesome-ai-testing list, DeepEval/RAGAS docs — self-healing and LLM test generation are already mainstream (~9× faster authoring, ~88% less maintenance claimed).",
 chapters=[
  C("AI as your testing copilot", ["LLMs for test ideas & cases","prompting for QA work","generating test data with AI","reviewing AI output critically"]),
  C("AI-powered test automation", ["self-healing tests","AI test generation tools","autonomous testing agents","when AI automation lies"]),
  C("Testing AI systems", ["why AI apps break differently","evaluating LLM outputs (DeepEval / RAGAS ideas)","hallucinations, bias & safety","regression for prompts & models"]),
  C("Staying employable in the AI era", ["what AI won't replace","the tester's judgment premium","learning loop for new tools","AI on your resume, honestly"]),
 ])

# ---------- resource library ----------
library = [
 ("\U0001F3AF Practice apps (beyond BuggyShop & BuggyAPI)", [
   ("the-internet (Heroku)", "https://the-internet.herokuapp.com", "every tricky UI element in one place"),
   ("DemoQA", "https://demoqa.com", "forms, alerts, frames, widgets to automate"),
   ("SauceDemo", "https://www.saucedemo.com", "the classic practice shop for UI suites"),
   ("Restful-Booker", "https://restful-booker.herokuapp.com", "CRUD API with auth — API testing playground"),
   ("ParaBank", "https://parabank.parasoft.com", "demo bank — fintech-flavored practice"),
   ("OWASP Juice Shop", "https://owasp.org/www-project-juice-shop/", "deliberately insecure shop — security practice"),
   ("OrangeHRM demo", "https://opensource-demo.orangehrmlive.com", "realistic HR system for E2E flows"),
   ("awesome-sites-to-test-on", "https://github.com/BMayhew/awesome-sites-to-test-on", "curated GitHub list of practice targets"),
 ]),
 ("\U0001F4DA Books that shaped the craft", [
   ("The Art of Software Testing — Glenford Myers", "https://en.wikipedia.org/wiki/Glenford_Myers", "1979 classic: a good test finds bugs"),
   ("Lessons Learned in Software Testing — Kaner, Bach, Pettichord", "https://www.wiley.com/en-us/Lessons+Learned+in+Software+Testing-p-9780471081128", "293 lessons from the context-driven school"),
   ("Agile Testing — Lisa Crispin & Janet Gregory", "https://agiletester.ca", "the agile-team testing bible"),
   ("Explore It! — Elisabeth Hendrickson", "https://pragprog.com/titles/ehxta/explore-it/", "the exploratory testing playbook"),
   ("How Google Tests Software — Whittaker et al.", "https://www.pearson.com/en-us/subject-catalog/p/how-google-tests-software/P200000009424", "engineering-culture view of QA at scale"),
   ("Perfect Software & Other Illusions — Gerald Weinberg", "https://leanpub.com/perfectsoftware", "why testing exists, by a field pioneer"),
   ("MoT book collection", "https://www.ministryoftesting.com/collections/software-testing-books", "community-curated reading list"),
 ]),
 ("\U0001F393 Free courses & structured learning", [
   ("Test Automation University", "https://testautomationu.applitools.com", "free, per-tool courses in Java/Python/JS"),
   ("ISTQB CTFL v4.0 syllabus (free PDF)", "https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/", "the certification skeleton — free to study"),
   ("Ministry of Testing", "https://www.ministryoftesting.com", "courses, articles, The Club forum, MoTaverse"),
   ("FreeLearningResourcesForSoftwareTesters", "https://github.com/PaulWaltersDev/FreeLearningResourcesForSoftwareTesters", "huge GitHub link collection"),
   ("MoT: 99 essential resources", "https://www.ministryoftesting.com/insights/99-essential-resources-to-help-software-testers", "one-stop meta-list"),
 ]),
 ("\U0001F4DD Blogs & people to follow", [
   ("DevelopSense — Michael Bolton", "https://developsense.com", "testing vs checking; deep craft thinking"),
   ("Satisfice — James Bach", "https://www.satisfice.com/blog", "context-driven testing's home"),
   ("Automation Panda — Andy Knight", "https://automationpanda.com", "clear automation & BDD writing"),
   ("TestGuild — Joe Colantonio", "https://testguild.com", "blog + the biggest automation podcast"),
   ("Software Testing Help", "https://www.softwaretestinghelp.com", "encyclopedic tutorials"),
   ("Guru99 testing", "https://www.guru99.com/software-testing.html", "beginner-friendly tutorials"),
   ("Angie Jones", "https://angiejones.tech", "automation & career inspiration"),
 ]),
 ("\U0001F399 Podcasts & channels", [
   ("TestGuild podcast", "https://testguild.com/podcasts/", "weekly automation interviews"),
   ("MoTaverse podcast", "https://www.ministryoftesting.com", "people & systems shaping quality"),
   ("AB Testing — Bach/Bolton adjacent", "https://www.angryweasel.com/ABTesting/", "modern testing philosophy"),
   ("Rahul Shetty Academy (YouTube)", "https://www.youtube.com/@RahulShettyAcademy", "hands-on Selenium/API walkthroughs"),
   ("Naveen AutomationLabs (YouTube)", "https://www.youtube.com/@naveenautomationlabs", "Java + Selenium deep dives"),
 ]),
 ("\U0001F916 AI-era tool lists", [
   ("awesome-ai-testing", "https://github.com/tugkanboz/awesome-ai-testing", "curated AI testing tools & resources"),
   ("DeepEval", "https://github.com/confident-ai/deepeval", "open-source LLM evaluation framework"),
   ("Promptfoo", "https://promptfoo.dev", "test your prompts like code"),
 ]),
 ("\U0001F310 Communities", [
   ("r/QualityAssurance", "https://reddit.com/r/QualityAssurance", "career threads & honest advice"),
   ("r/softwaretesting", "https://reddit.com/r/softwaretesting", "practitioner Q&A"),
   ("MoT The Club", "https://club.ministryoftesting.com", "the friendliest testing forum"),
   ("uTest community", "https://www.utest.com", "crowdtesting — real paid practice"),
 ]),
]

checked_covered = [
 "ISTQB CTFL v4.0 cross-check: Ch1 fundamentals ✓, Ch2 SDLC/levels ✓, Ch4 techniques ✓, Ch6 tools ✓ — Ch3 static testing & Ch5 risk/estimation were the only gaps (now added above)",
 "Exploratory & session-based testing ✓ (Track C) · Accessibility ✓ (non-functional + toolbox) · Compatibility/cross-browser ✓",
 "Performance, security (OWASP), mobile/Appium ✓ (Track E) · BDD/Cucumber ✓ · contract testing ✓",
 "Microservices & resilience: contract testing already in Track E; chaos engineering + observability & shift-right folded into the new AI/modern-era additions and Docker/K8s modules’ CI chapters",
 "Agile/Scrum/Kanban, shift-left, test management tools, metrics & reporting ✓ (Track F)",
 "Portfolio, résumé, interviews, first 90 days, working solo ✓ (Track G)",
]

new_modules = [sysdesign_module, ai_module]
n_ch = len(slot_ins) + sum(len(m["chapters"]) for m in new_modules)
n_topics = sum(len(s["topics"]) for s in slot_ins) + sum(len(c[1]) for m in new_modules for c in m["chapters"])
n_links = sum(len(items) for _, items in library)

parts = []
add = parts.append
add("""<title>Notes Curriculum — Final Gap Check (v3.2)</title>
<style>
  :root {
    --ground:#f4f7f6; --surface:#ffffff; --ink:#141a18; --muted:#5b6663;
    --faint:#87928e; --border:#dfe6e3; --accent:#0f9b78; --accent-ink:#0b7a5f;
    --accent-soft:#e3f4ee; --new:#b4540a; --new-soft:#fcefe2; --chip:#eef2f0;
    --core:#0f9b78; --core-soft:#e3f4ee;
  }
  @media (prefers-color-scheme: dark) { :root {
    --ground:#0c1110; --surface:#131a18; --ink:#e6edea; --muted:#9aa8a3;
    --faint:#6e7b76; --border:#243029; --accent:#2dd4a7; --accent-ink:#2dd4a7;
    --accent-soft:#12352b; --new:#f0954a; --new-soft:#3a2413; --chip:#1b2420;
    --core:#2dd4a7; --core-soft:#12352b;
  } }
  :root[data-theme="dark"] {
    --ground:#0c1110; --surface:#131a18; --ink:#e6edea; --muted:#9aa8a3;
    --faint:#6e7b76; --border:#243029; --accent:#2dd4a7; --accent-ink:#2dd4a7;
    --accent-soft:#12352b; --new:#f0954a; --new-soft:#3a2413; --chip:#1b2420;
    --core:#2dd4a7; --core-soft:#12352b;
  }
  :root[data-theme="light"] {
    --ground:#f4f7f6; --surface:#ffffff; --ink:#141a18; --muted:#5b6663;
    --faint:#87928e; --border:#dfe6e3; --accent:#0f9b78; --accent-ink:#0b7a5f;
    --accent-soft:#e3f4ee; --new:#b4540a; --new-soft:#fcefe2; --chip:#eef2f0;
    --core:#0f9b78; --core-soft:#e3f4ee;
  }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--ground); color:var(--ink);
    font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; line-height:1.55; }
  .wrap { max-width:960px; margin:0 auto; padding:40px 24px 80px; }
  h1,h2,h3 { text-wrap:balance; margin:0; }
  a { color:var(--accent-ink); text-decoration:none; }
  a:hover { text-decoration:underline; }
  a:focus-visible { outline:2px solid var(--accent-ink); outline-offset:2px; border-radius:2px; }
  .eyebrow { font-size:12px; letter-spacing:.14em; text-transform:uppercase; color:var(--new); font-weight:700; }
  header.top h1 { font-size:28px; letter-spacing:-.01em; margin:6px 0 10px; }
  header.top p { color:var(--muted); max-width:72ch; margin:0 0 20px; }
  .stats { display:flex; flex-wrap:wrap; gap:12px; }
  .stat { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:11px 18px; }
  .stat b { display:block; font-size:22px; font-variant-numeric:tabular-nums; color:var(--new); }
  .stat span { font-size:12.5px; color:var(--muted); }
  section { margin-top:42px; }
  section > h2 { font-size:20px; margin-bottom:6px; }
  section > p.sub { color:var(--muted); font-size:14px; margin:0 0 16px; max-width:80ch; }
  .gap { background:var(--surface); border:1px solid var(--new); border-radius:12px; padding:16px 18px; margin-bottom:12px; }
  .gap-head { display:flex; gap:10px; align-items:baseline; flex-wrap:wrap; }
  .gap-head h3 { font-size:15.5px; }
  .where { font-size:12px; color:var(--faint); }
  .where b { color:var(--accent-ink); font-weight:600; }
  .topics { display:flex; flex-wrap:wrap; gap:6px; margin:9px 0; }
  .topic { background:var(--chip); border-radius:6px; padding:2px 9px; font-size:12.5px; color:var(--muted); }
  .why { font-size:13px; color:var(--muted); margin:0; max-width:84ch; }
  .module-card { background:var(--surface); border:2px solid var(--new); border-radius:12px; padding:18px 20px; }
  .module-card .kind { color:var(--new); background:var(--new-soft); padding:2px 10px; border-radius:99px; font-weight:700; font-size:11.5px; letter-spacing:.06em; }
  table.chapters { width:100%; border-collapse:collapse; margin-top:10px; }
  .chapters td { padding:7px 0; vertical-align:top; border-top:1px solid var(--border); font-size:13.5px; }
  .chapters td.ch { width:230px; font-weight:600; padding-right:14px; }
  .lib { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px 18px; margin-bottom:12px; }
  .lib h3 { font-size:15px; margin-bottom:8px; }
  .lib ul { margin:0; padding-left:18px; }
  .lib li { font-size:13.5px; margin-bottom:5px; color:var(--muted); }
  .lib li b { color:var(--ink); font-weight:600; }
  .covered { background:var(--accent-soft); border-radius:12px; padding:16px 20px; }
  .covered h2 { color:var(--accent-ink); font-size:17px; margin-bottom:8px; }
  .covered li { font-size:13.5px; color:var(--muted); margin-bottom:6px; }
  .cta { background:var(--surface); border:1px solid var(--accent); border-radius:12px; padding:18px 22px; margin-top:40px; }
  .cta p { margin:0; font-size:14.5px; }
</style>
""")

add(f"""<div class="wrap">
<header class="top">
  <div class="eyebrow">Final gap check · v3.2 proposal · the last additions before writing begins</div>
  <h1>The exhaustive sweep: what was still missing — and the resource library</h1>
  <p>Cross-checked the whole map against the ISTQB v4.0 syllabus, testing-history sources, 2026 skills surveys,
  AI-testing guides, and the community’s big resource lists. Result: <b>2 new modules, {len(slot_ins)} new chapters</b>
  slotted into existing modules, the QA-history background you asked for, and a <b>{n_links}-link resource library</b>
  that becomes a permanent page in the wiki.</p>
  <div class="stats">
    <div class="stat"><b>2</b><span>new modules (system design · AI)</span></div>
    <div class="stat"><b>+{n_ch}</b><span>chapters</span></div>
    <div class="stat"><b>+{n_topics}</b><span>topics</span></div>
    <div class="stat"><b>{n_links}</b><span>curated links</span></div>
  </div>
</header>

<section>
  <h2>\U0001F4DC The background you asked for — where QA came from</h2>
  <p class="sub">Becomes a full chapter early in QA foundations, written as a story: the 1947 Mark II moth
  Grace Hopper’s team taped into the logbook (“first actual case of bug being found” — and why the story is
  half-myth: “bug” predates it, even Edison used it) · Gelperin &amp; Hetzel’s five eras — debugging-oriented
  (pre-1956) → demonstration (prove it works) → destruction (Myers 1979: a good test <i>finds</i> bugs) →
  evaluation → prevention (1988→) · the pioneers: Myers, Weinberg, Kaner’s context-driven school, Bach &amp;
  Bolton’s testing-vs-checking, Crispin &amp; Gregory’s agile testing · then how agile (2001), DevOps, and now
  AI keep reshaping the tester’s job.</p>
</section>

<section>
  <h2>\U0001F9E9 Gaps found — new chapters slotted into existing modules</h2>
  <p class="sub">Each card names the exact module it joins. Nothing else in the approved map moves.</p>""")
for g in slot_ins:
    chips = "".join(f'<span class="topic">{t}</span>' for t in g["topics"])
    add(f"""<div class="gap">
    <div class="gap-head"><h3>{g["chapter"]}</h3>
      <span class="where">→ Track <b>{g["track"]}</b> · module “<b>{g["module"]}</b>”</span></div>
    <div class="topics">{chips}</div>
    <p class="why">{g["why"]}</p>
  </div>""")
add("</section>")

add("""<section>
  <h2>\U0001F195 Two genuinely new modules</h2>""")
for nm in new_modules:
    add(f"""<div class="module-card" style="margin-bottom:14px">
    <div class="gap-head"><h3>{nm["title"]}</h3><span class="kind">NEW MODULE</span>
      <span class="where">{nm["place"]}</span></div>
    <p class="why" style="margin-top:8px">{nm["why"]}</p>
    <table class="chapters">""")
    for ch, topics in nm["chapters"]:
        chips = "".join(f'<span class="topic">{t}</span>' for t in topics)
        add(f'<tr><td class="ch">{ch}</td><td><div class="topics" style="margin:0">{chips}</div></td></tr>')
    add("</table></div>")
add("""</section>

<section>
  <h2>\U0001F517 The resource library — a permanent wiki page</h2>
  <p class="sub">Beyond per-topic links, the wiki gets one living “Library” page. Starting stock, all free:</p>""")
for group, items in library:
    add(f'<div class="lib"><h3>{group}</h3><ul>')
    for name, url, note in items:
        add(f'<li><b><a href="{url}" target="_blank" rel="noopener">{name}</a></b> — {note}</li>')
    add("</ul></div>")
add("</section>")

add("""<section class="covered">
  <h2>✅ Checked and already covered (no action needed)</h2>
  <ul style="margin:0; padding-left:18px">""")
for c in checked_covered:
    add(f"<li>{c}</li>")
add(f"""</ul>
</section>

<section class="cta">
  <p><b>This is the completeness ceiling</b> — the map has now been checked against the certification syllabus,
  the history, the 2026 tool landscape, and the community’s own resource lists. Approve and the master map
  becomes final at roughly <b>43 modules / ~194 chapters / ~770 topics</b> — and the next step is writing
  Track A · Module 1.</p>
</section>
</div>""")

html = "\n".join(parts)
out = "/private/tmp/claude-501/-Users-sajanathapa-Desktop-1/9298bb44-e37b-469c-a23d-cefc71ba064d/scratchpad/notes-v3-2-final-check.html"
open(out, "w").write(html)
print(f"chapters=+{n_ch} topics=+{n_topics} links={n_links} bytes={len(html)}")
