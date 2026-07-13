# Generates notes-curriculum-preview.html (v3) from structured data.
# Unchanged modules reproduce v2 verbatim; NEW/UPGRADED modules carry badges.

T = lambda title, topics: (title, topics, False)      # chapter
TN = lambda title, topics: (title, topics, True)      # NEW chapter

def M(title, level, chapters, new=False, upgraded=False, note=None):
    return dict(title=title, level=level, chapters=chapters, new=new, upgraded=upgraded, note=note)

tracks = [
dict(id="A", title="Computer & Digital Foundations", tag=None,
     desc="Absolute zero — what a computer is, how to drive it, and how the internet works.",
     modules=[
    M("How a computer works", "Beginner", [
        T("The parts of a computer", ["tower & laptop anatomy","monitor, keyboard, mouse","ports & cables","turning it on safely"]),
        T("CPU, memory & storage", ["what the CPU does","RAM vs storage","GHz, GB, TB","why computers slow down"]),
        T("Input & output devices", ["input devices","output devices","peripherals","connecting a device"]),
        T("How software runs", ["hardware vs software","programs & processes","booting up","apps vs the OS"]),
        T("Types of computers", ["desktops & laptops","phones & tablets","servers","smart devices"]),
    ]),
    M("Operating systems & files", "Beginner", [
        T("What an OS does", ["role of the OS","the desktop & UI","managing hardware","common OS tasks"]),
        T("Windows, macOS & Linux", ["Windows tour","macOS tour","Linux & open source","choosing one"]),
        T("Files, folders & paths", ["files & file types","folders & organizing","file paths","search & shortcuts"]),
        T("Installing & managing software", ["installing apps","updates","uninstalling","app stores vs downloads"]),
        T("First look at the command line", ["what a terminal is","basic commands","navigating folders","why testers use it"]),
    ]),
    M("The internet & the web", "Beginner", [
        T("How the internet works", ["networks & the internet","ISPs & connections","IP addresses","Wi-Fi vs wired"]),
        T("Browsers & page loading", ["what a browser is","how a page loads","tabs, history, bookmarks","a peek at dev tools"]),
        T("Client, server & HTTP", ["client vs server","request & response","HTTP in plain words","what a site is made of"]),
        T("What “the cloud” is", ["the cloud explained","cloud storage","web apps","SaaS"]),
        T("Domains, URLs & hosting", ["anatomy of a URL","domains & DNS","hosting","HTTPS & the padlock"]),
    ]),
    M("Digital literacy & safety", "Beginner", [
        T("Accounts, passwords & 2FA", ["accounts & sign-in","strong passwords","password managers","two-factor auth"]),
        T("Staying safe online", ["phishing & scams","safe downloads","privacy basics","updates & antivirus"]),
        T("Keyboard & typing", ["keyboard layout","shortcuts","touch typing","efficiency tips"]),
        T("Everyday tools", ["documents","spreadsheets","email","collaboration tools"]),
    ]),
], checkpoint=dict(title="Checkpoint · Set up your QA workstation",
     desc="Create your accounts (GitHub, QA Mastery), install a browser + dev tools, organize a study folder, learn the shortcuts you’ll use every day.")),

dict(id="B", title="Thinking Like a Programmer", tag="Java & Python",
     desc="The logic and coding foundation a tester needs before automating — taught in Java and Python side by side.",
     modules=[
    M("Programming basics", "Beginner", [
        T("What is code & a program", ["what code is","languages overview","Java vs Python for beginners","your first program"]),
        T("Variables & data types", ["variables","numbers, text, booleans","types in Java & Python","naming"]),
        T("Operators & expressions", ["arithmetic","comparison","logical operators","expressions"]),
        T("Input & output", ["printing output","reading input","comments","formatting"]),
    ]),
    M("Logic & control flow", "Beginner", [
        T("Conditions", ["if / else","comparison & logic","nested conditions","switch / match"]),
        T("Loops", ["for loops","while loops","break & continue","iterating collections"]),
        T("Functions", ["defining functions","parameters & return","scope","reuse & DRY"]),
        T("First bugs & debugging", ["reading errors","print debugging","using a debugger","common mistakes"]),
    ]),
    M("Working with data", "Beginner", [
        T("Strings & text", ["string basics","common methods","formatting","parsing"]),
        T("Lists / arrays", ["creating lists","add / remove","iterating","sort & search"]),
        T("Key–value data", ["maps / dictionaries","objects","nesting","when to use which"]),
        T("Simple algorithms", ["problem-solving steps","looping over data","basic sort / search","practice katas"]),
    ]),
    M("A first language, deeper", "Core QA", [
        T("Setup & IDE", ["installing the JDK","installing Python","IntelliJ / VS Code","running programs"]),
        T("Syntax essentials", ["Java syntax tour","Python syntax tour","key differences","style conventions"]),
        T("Object-oriented basics", ["classes & objects","methods & fields","inheritance","encapsulation"]),
        T("Collections & exceptions", ["lists / maps / sets","exceptions & try-catch","file I/O","packages & modules"]),
    ]),
    M("Version control with Git", "Core QA", [
        T("Why version control", ["the problem it solves","what Git is","repositories","local vs remote"]),
        T("Git basics", ["init / clone","add & commit","status & log",".gitignore"]),
        T("Branches & merging", ["branches","switching","merging","resolving conflicts"]),
        T("GitHub & pull requests", ["pushing to GitHub","pull requests","code review","collaboration flow"]),
    ]),
    M("Linux for testers", "Core QA", new=True, note="Added in v3.1 — servers, CI runners and Docker images are all Linux; log-digging over SSH is week-one QA work.", chapters=[
        TN("Linux essentials", ["why servers run Linux","distros & the filesystem layout","the shell, properly","man pages & getting help"]),
        TN("Everyday commands", ["navigating & managing files","find & wildcards","viewing files (cat/less/head/tail)","pipes & redirection"]),
        TN("Logs & investigation", ["tail -f a live log","grep + basic regex","cut / sort / uniq / wc","from log line to bug report"]),
        TN("Remote servers", ["SSH & keys","scp / rsync","tmux basics","collecting evidence remotely"]),
        TN("Permissions & processes", ["chmod & chown in plain words","ps / top / kill","disk & memory (df/du/free)","environment variables"]),
        TN("Bash scripting for QA", ["variables, ifs & loops","your first useful script","cron scheduling","automating repetitive checks"]),
    ]),
], checkpoint=dict(title="Checkpoint · Code kata + your first repo",
     desc="Solve small katas in Java and Python, put them in a clean GitHub repo with a real README — your very first public artifact.")),

dict(id="C", title="QA & Manual Testing", tag=None,
     desc="The heart of the path — how professional testing thinks and works. API and SQL now live here, early, where the market says they belong.",
     modules=[
    M("QA foundations", "Core QA", [
        T("What is QA", ["QA vs QC vs testing","the tester’s mindset","quality defined","roles on a team"]),
        T("Why testing matters", ["cost of defects","famous failures","risk & value","when to stop"]),
        T("The seven principles", ["the 7 principles","applying them","testing myths","defect clustering"]),
        T("SDLC & STLC", ["SDLC phases","STLC phases","where testing fits","entry / exit criteria"]),
        T("Models", ["waterfall","agile","V-model","choosing a model"]),
    ]),
    M("Test design techniques", "Core QA", [
        T("Equivalence partitioning", ["valid & invalid classes","picking representatives","worked example","pitfalls"]),
        T("Boundary value analysis", ["why edges fail","2- & 3-value","worked example","combining with EP"]),
        T("Decision tables", ["conditions & actions","building a table","collapsing rules","worked example"]),
        T("State transition", ["states & events","diagrams & tables","valid vs invalid","worked example"]),
        T("Error guessing & use cases", ["error guessing","experience-based","use-case testing","exploratory link"]),
    ]),
    M("Test artifacts", "Core QA", [
        T("Scenarios & cases", ["scenarios vs cases","anatomy of a case","writing good cases","positive & negative"]),
        T("Test plans & strategy", ["what’s in a plan","test strategy","entry / exit criteria","lightweight plans"]),
        T("Traceability", ["the RTM","coverage","linking to requirements","finding gaps"]),
        T("Test data", ["what test data is","preparing data","data-driven thinking","managing data"]),
    ]),
    M("Levels & types of testing", "Core QA", [
        T("Test levels", ["unit","integration","system","acceptance (UAT)"]),
        T("Functional & regression", ["functional testing","regression","retest vs regression","impact analysis"]),
        T("Smoke & sanity", ["smoke testing","sanity testing","when to run each","build acceptance"]),
        T("Exploratory & ad-hoc", ["exploratory testing","session-based","ad-hoc","heuristics & tours"]),
        T("Box & approach", ["black vs white box","gray box","static vs dynamic","positive / negative"]),
    ]),
    M("Defect management", "Core QA", [
        T("The bug life cycle", ["states of a bug","the workflow","reopen & duplicate","triage"]),
        T("Writing bug reports", ["anatomy of a report","repro steps","evidence","clarity"]),
        T("Severity vs priority", ["severity","priority","combinations","who sets what"]),
        T("Tools", ["JIRA basics","Bugzilla","test management tools","dashboards"]),
    ]),
    M("Browser DevTools mastery", "Core QA", new=True, note="Added in v3.1 — the tester's microscope, taught panel by panel as how / what / when / why.", chapters=[
        TN("Elements & styles", ["inspecting the DOM","editing HTML/CSS live","finding locators","debugging layout & spacing"]),
        TN("Console", ["reading JS errors","warnings vs errors","filtering the noise","what to paste into a bug report"]),
        TN("Network", ["anatomy of a request","status, timing & headers","copy as cURL","HAR export as bug evidence"]),
        TN("Throttling & emulation", ["slow 3G & offline mode","device emulation","geolocation & sensors","testing what users really feel"]),
        TN("Application & storage", ["cookies & local storage","session & cache","clearing state properly","service workers, gently"]),
        TN("Audits & performance", ["Lighthouse reports","accessibility signals","performance recording, gently","when to escalate to devs"]),
    ]),
    M("The tester’s toolbox", "Core QA", new=True, note="Added in v3.1 — organized by tool family (specific tools rotate, the families don’t); every topic teaches how / what / when / why + the current best free pick.", chapters=[
        TN("Edge-case & form data", ["Bug Magnet (tricky inputs)","form fillers","test credit cards & emails","generating data: Mockaroo & Faker"]),
        TN("Link, page & UI checks", ["Check My Links","GoFullPage & screenshot tools","Window Resizer / responsive checks","WhatFont, PerfectPixel, Page Ruler"]),
        TN("Cookies, JSON & sessions", ["cookie editors","JSON formatters","Clear Cache","managing multi-account testing"]),
        TN("Locator & recorder helpers", ["SelectorsHub","CSS selector helpers","recorder extensions","from recorder to real script"]),
        TN("Accessibility & quality", ["WAVE","axe DevTools","contrast & screen-reader checks","Lighthouse as an extension of QA"]),
        TN("Beyond the browser", ["debugging proxies (Requestly / Charles / mitmproxy)","email testing (Mailinator / Mailpit)","tunnels (ngrok) & sharing localhost","screen recorders for bug repro"]),
        TN("Choosing tools wisely", ["how / what / when / why framework","free vs paid honestly","tool sprawl & when to stop","keeping your kit current"]),
    ]),
    M("API testing fundamentals", "Core QA", new=True, note="Moved early from Track E — every 2026 roadmap teaches Postman in the first months, and manual API testing is now a core manual-tester skill.", chapters=[
        TN("HTTP for testers", ["request & response anatomy","methods (GET/POST/PUT/DELETE)","headers & bodies","JSON & XML"]),
        TN("Status codes & REST", ["2xx / 4xx / 5xx families","REST in plain words","idempotency & safety","reading API docs & Swagger"]),
        TN("Postman & curl", ["curl basics","Postman requests","collections & environments","Postman tests & variables"]),
        TN("Auth, manually", ["API keys","Basic auth","Bearer / JWT","OAuth2, what a tester needs"]),
        TN("Finding API bugs", ["testing without a UI","negative API tests","validating against the spec","your first API bug hunt (BuggyAPI)"]),
    ]),
    M("SQL & databases for testers", "Core QA", new=True, note="Moved early from Track E — the market is unanimous: SQL comes before automation, because verifying data is daily manual-QA work.", chapters=[
        TN("Databases in plain words", ["what a database is","tables, rows, columns","relational vs NoSQL","where your app’s data lives"]),
        TN("Reading data", ["SELECT & WHERE","sorting & limits","JOINs, gently","aggregates & GROUP BY"]),
        TN("Verifying the app against the DB", ["UI action → DB check","CRUD verification","finding data bugs","test data setup & cleanup"]),
        TN("Tools & habits", ["DB clients (DBeaver, TablePlus)","connecting safely","read-only discipline","query snippets library"]),
    ]),
    M("Non-functional testing (intro)", "Core QA", [
        T("Performance", ["what it measures","load vs stress","key metrics","tools overview"]),
        T("Security", ["why it matters","common risks","a tester’s role","OWASP preview"]),
        T("Usability & accessibility", ["usability testing","UX heuristics","accessibility (WCAG)","assistive tech"]),
        T("Compatibility", ["cross-browser","cross-device","OS / versions","responsive checks"]),
    ]),
], checkpoint=dict(title="Checkpoint · Manual test cycle on BuggyShop + BuggyAPI",
     desc="Write a real test plan, 50 test cases, and graded bug reports on BuggyShop — then hunt the 5 seeded API bugs in BuggyAPI with Postman. This becomes portfolio repo #1: your documented manual project.")),

dict(id="D", title="Test Automation", tag="Selenium · Playwright · Cucumber",
     desc="Turning manual know-how into code — Selenium in Java & Python, Playwright in JS/TS, and BDD the way teams actually use it.",
     modules=[
    M("Automation foundations", "Advanced", [
        T("Why & when to automate", ["benefits","what to automate","what NOT to","manual vs automated"]),
        T("The automation pyramid", ["unit / integration / E2E","ice-cream-cone anti-pattern","balancing the suite","ROI"]),
        T("The tool landscape", ["Selenium","Playwright","Cypress","choosing a tool"]),
        T("Pitfalls", ["flaky tests","maintenance cost","over-automation","false confidence"]),
    ]),
    M("Selenium WebDriver", "Advanced", [
        T("Setup & architecture", ["WebDriver architecture","drivers & Selenium Manager","first script (Java)","first script (Python)"]),
        T("Locators", ["id / name / css / xpath","locator strategy","relative locators","robust selectors"]),
        T("Waits & sync", ["implicit vs explicit","fluent waits","avoiding sleeps","handling async"]),
        T("Actions & navigation", ["clicks & input","dropdowns & alerts","frames & windows","Actions API"]),
    ]),
    M("Test frameworks", "Advanced", [
        T("Lifecycle & annotations", ["setup / teardown hooks","@Test","TestNG vs JUnit","pytest fixtures"]),
        T("Assertions", ["assertions","soft assertions","custom messages","matchers"]),
        T("Groups & parameters", ["grouping tests","parameters","ordering","suites"]),
        T("Data-driven testing", ["data providers","parameterized tests","external data (CSV/Excel)","reuse"]),
    ]),
    M("Framework design", "Advanced", [
        T("Page Object Model", ["the POM pattern","page classes","returning pages","component objects"]),
        T("Reusable components", ["base classes","utilities","waits wrapper","driver factory"]),
        T("Config & data", ["config files","environments","test data","secrets"]),
        T("Logging & reporting", ["logging (Log4j)","ExtentReports","Allure","screenshots on failure"]),
    ]),
    M("BDD with Cucumber", "Advanced", new=True, note="Every best-selling QA course ships Cucumber — and job posts ask for it. Gherkin in Java (Cucumber) and Python (behave / pytest-bdd).", chapters=[
        TN("BDD in plain words", ["what BDD solves","Given / When / Then","BDD vs test scripts","the three amigos"]),
        TN("Gherkin & feature files", ["writing scenarios","scenario outlines & examples","backgrounds & tags","good vs bad Gherkin"]),
        TN("Step definitions", ["glue code (Java)","behave / pytest-bdd (Python)","data tables","hooks & context"]),
        TN("BDD in a framework", ["Cucumber + Selenium","reports & living documentation","when BDD helps","when it hurts"]),
    ]),
    M("Playwright", "Advanced", [
        T("Setup & auto-waiting", ["install Playwright","TypeScript setup","first test","auto-waiting explained"]),
        T("Locators & fixtures", ["user-facing locators","getByRole / Label / TestId","fixtures","test isolation"]),
        T("Tracing & debugging", ["trace viewer","codegen","debugging","screenshots & video"]),
        T("Parallel & cross-browser", ["projects & browsers","parallelism & sharding","retries","config"]),
    ]),
    M("Automation in CI/CD", "Advanced", upgraded=True, note="Upgraded in v3.1 — Jenkins and GitLab CI + quality gates added so all three major CI systems are covered.", chapters=[
        T("Running tests in CI", ["what CI is","running the suite","headless mode","artifacts"]),
        T("GitHub Actions", ["workflow basics","triggers","matrix runs","caching"]),
        TN("Jenkins", ["jobs & the classic UI","Jenkinsfile — pipeline as code","agents & plugins","when teams still pick Jenkins"]),
        TN("GitLab CI & quality gates", ["stages, jobs & runners",".gitlab-ci.yml","quality gates (coverage, Sonar)","blocking a merge on failure"]),
        T("Scheduling & reporting", ["scheduled runs","publishing reports","notifications","dashboards"]),
        T("Flake management", ["detecting flakes","quarantine","retries","stability practices"]),
    ]),
], checkpoint=dict(title="Checkpoint · Automate BuggyShop, end to end",
     desc="Build a Selenium + Java POM framework AND a Playwright TS suite against BuggyShop, running green in GitHub Actions. Portfolio repos #2 (UI automation) and the CI pipeline employers screen for.")),

dict(id="E", title="Specialized Testing", tag=None,
     desc="The high-value niches employers ask for — now with real API automation, since the fundamentals moved early.",
     modules=[
    M("API test automation", "Advanced", upgraded=True, note="Upgraded — was “API testing”. Manual API skills moved to Track C; this is the automation layer: REST Assured, pytest + requests, and contract testing.", chapters=[
        TN("REST Assured (Java)", ["setup & first test","given / when / then style","validating JSON & status","auth in REST Assured"]),
        TN("Python API testing", ["requests + pytest","fixtures for APIs","parameterized endpoint tests","sessions & auth"]),
        TN("Contract & schema testing", ["OpenAPI as the contract","schema validation","consumer-driven contracts","breaking-change detection"]),
        TN("Real-world API suites", ["test pyramids for APIs","data setup via API","chaining & state","API suite on BuggyAPI (OAuth2, GraphQL, SOAP)"]),
    ]),
    M("Relational databases, engineer-level", "Advanced", upgraded=True, note="Rebuilt in v3.1 (was “Database testing, deeper”) — reaches real backend-developer depth, verified hands-on against the BuggyAPI Postgres schema.", chapters=[
        TN("SQL mastery", ["subqueries & CTEs","window functions","set operators (UNION/EXCEPT)","date, time & timezone handling"]),
        TN("Schema design", ["ER modeling from requirements","keys & relationships","normalization 1NF→3NF","when to denormalize (and why)"]),
        TN("Indexes & performance", ["how an index actually works","clustered vs non-clustered","reading EXPLAIN / execution plans","query tuning & over-indexing writes"]),
        TN("Transactions & concurrency", ["ACID, properly","isolation levels & anomalies","locks & deadlocks","testing concurrent behavior"]),
        TN("Programmable objects", ["stored procedures & functions","triggers","testing procs (inputs, outputs, side effects)","error handling in SQL"]),
        TN("Data integrity at scale", ["constraints & referential integrity","finding orphans & duplicates","migrations & ETL verification","auditing data changes"]),
    ]),
    M("NoSQL & modern data", "Advanced", new=True, note="Added in v3.1 — the other half of real-world data work: document stores, caching, and the consistency bugs they breed.", chapters=[
        TN("The NoSQL landscape", ["document / key-value / graph / columnar","SQL vs NoSQL — choosing honestly","CAP theorem in plain words","where each shines"]),
        TN("MongoDB hands-on", ["documents & collections","CRUD & query operators","embedding vs referencing","aggregation pipeline, gently"]),
        TN("Redis & caching bugs", ["what caching solves","TTLs & eviction","stale-data bugs & cache invalidation","testing around a cache"]),
        TN("Distributed data, gently", ["replication & sharding","eventual consistency bugs","backups & recovery checks","testing data pipelines"]),
    ]),
    M("Docker & containers for testers", "Advanced", new=True, note="Added in v3.1 — kills “works on my machine” and unlocks disposable test environments.", chapters=[
        TN("Containers in plain words", ["VM vs container","images, containers & registries","why QA cares","install & first run"]),
        TN("Docker hands-on", ["run / exec / logs / stop","ports & volumes","env vars & networks","debugging a container"]),
        TN("Dockerfiles & Compose", ["writing a Dockerfile","multi-stage builds","docker-compose: app + DB together","a disposable test environment"]),
        TN("Containers in automation", ["Selenium Grid in Docker","running your suite in a container","Testcontainers for DB fixtures","containers in CI"]),
    ]),
    M("Kubernetes & test infrastructure", "Advanced", new=True, note="Added in v3.1 — intro-level on purpose: enough to work with real deployments and stand out in interviews, not to become a cluster admin.", chapters=[
        TN("Kubernetes in plain words", ["what K8s solves","pods, deployments, services","kubectl survival kit","namespaces & contexts"]),
        TN("Test workloads on K8s", ["running tests as Jobs","Selenium Grid on K8s (dynamic grid)","reading pod logs","port-forward to debug"]),
        TN("Releases & environments", ["how teams deploy","staging vs production","config & secrets","what QA verifies after a deploy"]),
    ]),
    M("Performance testing", "Advanced", [
        T("Load vs stress vs soak", ["types of perf testing","goals","recovery","scalability"]),
        T("Metrics", ["latency & throughput","percentiles vs averages","error rate","resource use"]),
        T("Tools intro", ["JMeter","k6","designing a test","reading results"]),
    ]),
    M("Security testing", "Advanced", [
        T("OWASP Top 10", ["the list","access control","misconfiguration","using OWASP"]),
        T("Injection & XSS", ["SQL injection","XSS types","testing for them","fixes"]),
        T("Broken auth & access", ["auth weaknesses","session issues","IDOR","privilege checks"]),
        T("Security checklist", ["a tester’s checklist","tools (ZAP)","reporting","secure mindset"]),
    ]),
    M("Mobile testing", "Advanced", [
        T("Device & OS matrix", ["fragmentation","building a matrix","real vs emulated","device farms"]),
        T("Gestures, interrupts, networks", ["touch gestures","interrupts","network conditions","orientation"]),
        T("Appium intro", ["what Appium is","setup","first mobile test","mobile locators"]),
        T("Mobile specifics", ["permissions","battery & performance","app lifecycle","store testing"]),
    ]),
], checkpoint=dict(title="Checkpoint · Specialist audit of BuggyAPI",
     desc="Ship an API automation suite (REST Assured or pytest) against BuggyAPI — REST, OAuth2, GraphQL — plus a DB integrity pass and a security checklist run. Portfolio repo #3: the API suite.")),

dict(id="F", title="Process & Team", tag=None,
     desc="How testing fits a real team — agile ceremonies, pipelines, and the tools you’ll live in.",
     modules=[
    M("Agile & DevOps for testers", "Core QA", [
        T("Scrum & Kanban", ["Scrum roles & ceremonies","Kanban","backlog & stories","estimation"]),
        T("Tester in a sprint", ["definition of done","in-sprint testing","acceptance criteria","collaboration"]),
        T("Shift-left & CI/CD", ["shift-left","the CI/CD pipeline","quality gates","continuous testing"]),
    ]),
    M("Test management & reporting", "Core QA", new=True, note="Split out of the old career module — job posts ask for TestRail/Xray experience and stakeholder reporting by name.", chapters=[
        TN("Test management tools", ["JIRA & boards, deeper","TestRail / Xray / Zephyr","organizing suites & runs","linking bugs to cases"]),
        TN("Metrics & reporting", ["test summary reports","coverage & pass-rate metrics","dashboards","reporting to stakeholders"]),
        TN("Docs & communication", ["Confluence / wikis","writing for developers","status updates","async communication"]),
    ]),
], checkpoint=None),

dict(id="G", title="Your First Job", tag="NEW TRACK",
     desc="The last mile almost nobody teaches — turning the work you just did into interviews, offers, and a strong first 90 days.",
     modules=[
    M("A portfolio that gets interviews", "Core QA", new=True, chapters=[
        TN("The 3-repo portfolio", ["repo 1: documented manual project","repo 2: UI automation suite","repo 3: API suite + CI","READMEs that sell"]),
        TN("Show your work", ["packaging BuggyShop / BuggyAPI work","architecture diagrams","demo GIFs & reports","what recruiters actually open"]),
        TN("Profiles", ["GitHub profile polish","LinkedIn for QA","personal brand basics","posting your progress"]),
    ]),
    M("Résumé & applications", "Core QA", new=True, chapters=[
        TN("The QA résumé", ["structure that works","skills & keywords (ATS)","numbers & impact","common mistakes"]),
        TN("Applying smart", ["reading job posts","tailoring per role","cover letters, short","tracking applications"]),
        TN("Certifications, honestly", ["ISTQB — worth it or not","when certs matter","free alternatives","learning in public"]),
    ]),
    M("Interviews", "Core QA", new=True, chapters=[
        TN("Manual QA questions", ["classic questions & answers","test-design exercises","“test this pen” scenarios","talking through bugs"]),
        TN("Technical rounds", ["automation & coding questions","SQL questions","API questions","take-home assignments"]),
        TN("Behavioral & scenarios", ["STAR stories","conflict & priority scenarios","questions to ask them","salary conversations"]),
        TN("Mock practice", ["mock interview drills","recording yourself","feedback loops","handling rejection"]),
    ]),
    M("Your first 90 days", "Core QA", new=True, chapters=[
        TN("Landing well", ["onboarding as a QA","learning the product fast","your first bug report at work","building trust"]),
        TN("Working solo (the mentor gap)", ["being the only QA","asking good questions","using the community","when to escalate"]),
        TN("Growing from here", ["junior → mid roadmap","specializing","keeping a brag doc","continued learning"]),
    ]),
], checkpoint=dict(title="Checkpoint · Ship it",
     desc="Portfolio public, résumé tailored, three mock interviews done — start applying. The community is your senior QA while you do.")),
]

anatomy = [
    ("\U0001F3A3", "Hook", "a curiosity opener that makes you need the answer"),
    ("\U0001F3D9", "Real-life analogy", "the concept in everyday terms first"),
    ("\U0001F4CA", "Animated figure", "a diagram you can play, not a static image"),
    ("\U0001F527", "First time? Do this", "exact setup steps, nothing assumed"),
    ("⚠️", "When it breaks", "the errors you’ll actually hit + fixes"),
    ("\U0001F50E", "Where & how to check", "logs, network tab, DB — concrete verification"),
    ("\U0001F64B", "How & whom to ask", "frame a good question → posts to the Community"),
    ("\U0001F39B", "Try it", "an interactive tool or runnable code (Wandbox)"),
    ("\U0001F4CB", "Worked example", "a real case walked through"),
    ("\U0001F4D6", "Glossary terms", "hover any jargon for plain English"),
    ("\U0001F9E0", "Quiz + challenge", "instant-feedback quiz mid-note, challenge at the end"),
    ("\U0001F0CF", "Flashcards", "key terms, wired to spaced repetition"),
    ("⚡", "Common mistakes", "what beginners get wrong, preempted"),
    ("✅", "Takeaways + XP", "mark complete, earn XP, keep the streak"),
]

changes = [
    ("Mentor anatomy in every note", "Every topic is written as “the senior QA you don’t have to ask”: setup steps, troubleshooting, where to verify, and how to ask the community. This is the approved sample-note format plus your “add more” extras."),
    ("API testing moved early", "New Track C module — HTTP, Postman, auth, and a first API bug hunt during manual testing. 2026 roadmaps put Postman in months 1–3; it’s “the highest-use skill most QAs underinvest in”."),
    ("SQL moved early", "New Track C module — SELECT/JOIN and verifying the app against the DB, before any automation. Every roadmap we validated sequences SQL pre-code."),
    ("BDD / Cucumber added", "New Track D module (Gherkin, Cucumber + Java, behave/pytest-bdd). Every best-selling course ships it and job posts list it."),
    ("API automation upgraded", "Track E module rebuilt around REST Assured, pytest + requests, and contract/schema testing against OpenAPI."),
    ("NEW Track G — Your First Job", "Four modules: the 3-repo portfolio employers screen for, résumé/ATS, interview rounds (manual + SQL + API + behavioral), and your first 90 days — including working solo without a senior."),
    ("Project spine checkpoints", "After each track, a guided checkpoint on the real BuggyShop + BuggyAPI apps builds the portfolio piece by piece — manual → UI automation → API → DB → security."),
    ("Setup + resources per module", "Every module opens with a \U0001F527 setup guide and closes with 3–5 curated free resources — the fragmentation pain, solved in place."),
]

sources = [
    ("QA Engineer Roadmap 2026 (BirJob)", "12-month zero→SDET path: Postman + SQL in months 1–3, Playwright default, 3-repo portfolio, contract testing"),
    ("Rahul Shetty — Udemy best-seller (100k+ 5★)", "wins on framework-building end-to-end + Cucumber + interview prep + résumé section — not on topic count"),
    ("Test Automation University (free)", "short course per tool, Java/Python/JS parallel tracks, API paths, career courses — validates our track model"),
    ("StarAgile / Guru99 / roadmap.sh (Jul 2 research)", "manual → programming → Selenium → API → CI sequencing; beginner tracks start at computer basics"),
]

# ---- counts ----
n_modules = sum(len(t["modules"]) for t in tracks)
n_chapters = sum(len(m["chapters"]) for t in tracks for m in t["modules"])
n_topics = sum(len(ch[1]) for t in tracks for m in t["modules"] for ch in m["chapters"])

esc = lambda s: s  # content is authored, entities already escaped where needed

parts = []
add = parts.append

add("""<title>Notes Wiki — Curriculum v3 (Validated)</title>
<style>
  :root {
    --ground:#f4f7f6; --surface:#ffffff; --ink:#141a18; --muted:#5b6663;
    --faint:#87928e; --border:#dfe6e3; --accent:#0f9b78; --accent-ink:#0b7a5f;
    --accent-soft:#e3f4ee; --new:#b4540a; --new-soft:#fcefe2;
    --beginner:#b06d12; --beginner-soft:#fbf0dd;
    --core:#0f9b78; --core-soft:#e3f4ee;
    --advanced:#6d5bd0; --advanced-soft:#edeafb;
    --spine:#0f9b78; --chip:#eef2f0;
  }
  @media (prefers-color-scheme: dark) { :root {
    --ground:#0c1110; --surface:#131a18; --ink:#e6edea; --muted:#9aa8a3;
    --faint:#6e7b76; --border:#243029; --accent:#2dd4a7; --accent-ink:#2dd4a7;
    --accent-soft:#12352b; --new:#f0954a; --new-soft:#3a2413;
    --beginner:#e8b04e; --beginner-soft:#33270f;
    --core:#2dd4a7; --core-soft:#12352b;
    --advanced:#a78bfa; --advanced-soft:#251d45;
    --spine:#2dd4a7; --chip:#1b2420;
  } }
  :root[data-theme="dark"] {
    --ground:#0c1110; --surface:#131a18; --ink:#e6edea; --muted:#9aa8a3;
    --faint:#6e7b76; --border:#243029; --accent:#2dd4a7; --accent-ink:#2dd4a7;
    --accent-soft:#12352b; --new:#f0954a; --new-soft:#3a2413;
    --beginner:#e8b04e; --beginner-soft:#33270f;
    --core:#2dd4a7; --core-soft:#12352b;
    --advanced:#a78bfa; --advanced-soft:#251d45;
    --spine:#2dd4a7; --chip:#1b2420;
  }
  :root[data-theme="light"] {
    --ground:#f4f7f6; --surface:#ffffff; --ink:#141a18; --muted:#5b6663;
    --faint:#87928e; --border:#dfe6e3; --accent:#0f9b78; --accent-ink:#0b7a5f;
    --accent-soft:#e3f4ee; --new:#b4540a; --new-soft:#fcefe2;
    --beginner:#b06d12; --beginner-soft:#fbf0dd;
    --core:#0f9b78; --core-soft:#e3f4ee;
    --advanced:#6d5bd0; --advanced-soft:#edeafb;
    --spine:#0f9b78; --chip:#eef2f0;
  }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--ground); color:var(--ink);
    font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; line-height:1.55; }
  .wrap { max-width:1060px; margin:0 auto; padding:40px 24px 80px; }
  h1,h2,h3 { text-wrap:balance; margin:0; }
  .eyebrow { font-size:12px; letter-spacing:.14em; text-transform:uppercase; color:var(--accent-ink); font-weight:700; }
  header.top h1 { font-size:30px; letter-spacing:-.01em; margin:6px 0 10px; }
  header.top p.lede { color:var(--muted); max-width:68ch; margin:0 0 22px; }
  .stats { display:flex; flex-wrap:wrap; gap:12px; }
  .stat { background:var(--surface); border:1px solid var(--border); border-radius:10px;
    padding:12px 18px; min-width:110px; }
  .stat b { display:block; font-size:24px; font-variant-numeric:tabular-nums; color:var(--accent-ink); }
  .stat span { font-size:12.5px; color:var(--muted); }
  .stat.delta b { color:var(--new); }
  section { margin-top:44px; }
  .panel { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:22px 24px; }
  .panel h2 { font-size:19px; margin-bottom:4px; }
  .panel p.sub { color:var(--muted); font-size:14px; margin:0 0 16px; max-width:75ch; }
  .choices { display:flex; flex-wrap:wrap; gap:8px 22px; font-size:14px; }
  .choices b { color:var(--accent-ink); font-weight:600; }
  .changes { display:grid; grid-template-columns:repeat(auto-fit,minmax(290px,1fr)); gap:12px; margin-top:14px; }
  .change { border:1px solid var(--border); border-radius:10px; padding:14px 16px; background:var(--ground); }
  .change h3 { font-size:14.5px; margin-bottom:4px; }
  .change p { font-size:13px; color:var(--muted); margin:0; }
  .anatomy { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:8px; margin-top:14px; }
  .an { display:flex; gap:10px; align-items:flex-start; border:1px solid var(--border);
    border-radius:10px; padding:10px 12px; background:var(--ground); }
  .an .em { font-size:17px; line-height:1.3; }
  .an b { font-size:13.5px; display:block; }
  .an span { font-size:12.5px; color:var(--muted); }
  .legend { display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin:26px 0 6px; font-size:12.5px; color:var(--muted); }
  .lv { padding:2px 10px; border-radius:99px; font-weight:600; font-size:12px; }
  .lv.Beginner { color:var(--beginner); background:var(--beginner-soft); }
  .lv.CoreQA { color:var(--core); background:var(--core-soft); }
  .lv.Advanced { color:var(--advanced); background:var(--advanced-soft); }
  .badge-new { color:var(--new); background:var(--new-soft); padding:2px 10px; border-radius:99px; font-weight:700; font-size:11.5px; letter-spacing:.06em; }
  .track { margin-top:34px; }
  .track-head { display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; padding-bottom:10px; }
  .track-id { font-size:13px; font-weight:800; letter-spacing:.1em; color:var(--accent-ink);
    background:var(--accent-soft); padding:3px 12px; border-radius:99px; }
  .track-head h2 { font-size:21px; }
  .track-head .tag { color:var(--faint); font-size:13.5px; }
  .track > p.desc { color:var(--muted); font-size:14px; margin:2px 0 16px; max-width:78ch; }
  .module { background:var(--surface); border:1px solid var(--border); border-radius:12px;
    padding:18px 20px; margin-bottom:14px; }
  .module.is-new { border-color:var(--new); }
  .mod-head { display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:4px; }
  .mod-num { font-size:12px; font-weight:700; color:var(--faint); font-variant-numeric:tabular-nums; }
  .mod-head h3 { font-size:16.5px; }
  .mod-note { font-size:13px; color:var(--muted); background:var(--new-soft); border-radius:8px;
    padding:8px 12px; margin:8px 0 4px; }
  .mod-meta { font-size:12px; color:var(--faint); margin-top:10px; }
  table.chapters { width:100%; border-collapse:collapse; margin-top:10px; }
  .chapters td { padding:7px 0; vertical-align:top; border-top:1px solid var(--border); font-size:13.5px; }
  .chapters td.ch { width:230px; font-weight:600; padding-right:14px; }
  .chapters td.ch .nb { color:var(--new); font-size:10.5px; font-weight:800; letter-spacing:.08em; margin-left:6px; }
  .topics { display:flex; flex-wrap:wrap; gap:6px; }
  .topic { background:var(--chip); border-radius:6px; padding:2px 9px; font-size:12.5px; color:var(--muted); }
  .checkpoint { border-left:3px solid var(--spine); background:var(--surface); border-radius:0 12px 12px 0;
    padding:14px 18px; margin:4px 0 10px; }
  .checkpoint b { color:var(--accent-ink); font-size:14px; }
  .checkpoint p { margin:4px 0 0; font-size:13.5px; color:var(--muted); max-width:82ch; }
  .sources li { font-size:13.5px; color:var(--muted); margin-bottom:8px; }
  .sources b { color:var(--ink); }
  .cta { margin-top:40px; border:1px solid var(--accent); }
  .cta p { margin:0; font-size:14.5px; }
  @media (max-width:640px){ .chapters td.ch { width:135px; } }
</style>
""")

add(f"""<div class="wrap">
<header class="top">
  <div class="eyebrow">Notes Wiki · Curriculum v3.1 · APPROVED MASTER MAP</div>
  <h1>From zero to your first QA job — the full note map</h1>
  <p class="lede">The locked curriculum: v3 (market-validated, approved) + the v3.1 deep-dive additions you approved —
  engineer-level databases + NoSQL, Linux, Docker &amp; Kubernetes, all three CI systems, DevTools mastery, and the tester’s toolbox.
  Every topic gets the full mentor-note format. Build order: taxonomy first, then Track A · Module 1 for review, then onward.</p>
  <div class="stats">
    <div class="stat"><b>7</b><span>tracks (+1)</span></div>
    <div class="stat"><b>{n_modules}</b><span>modules (was 28 in v2)</span></div>
    <div class="stat"><b>{n_chapters}</b><span>chapters</span></div>
    <div class="stat"><b>~{n_topics}</b><span>topics (notes)</span></div>
    <div class="stat delta"><b>6</b><span>project checkpoints</span></div>
  </div>
</header>

<section class="panel">
  <h2>Your locked choices</h2>
  <div class="choices" style="margin-top:8px">
    <span>Start: <b>true zero (Track A kept)</b></span>
    <span>Languages: <b>Java + Python</b>, <b>JS/TS for Playwright</b></span>
    <span>Depth: <b>full lessons, 3–5 topics/chapter</b></span>
    <span>Format: <b>approved sample note + your “add more” extras</b></span>
  </div>
</section>

<section class="panel">
  <h2>What changed in v3</h2>
  <p class="sub">Each change traces to the validation research — nothing moved on taste alone.</p>
  <div class="changes">""")
for title, body in changes:
    add(f'<div class="change"><h3>{title}</h3><p>{body}</p></div>')
add("""</div>
</section>

<section class="panel">
  <h2>Anatomy of every note — “the senior QA you don’t have to ask”</h2>
  <p class="sub">The approved sample-note format, extended with your requested additions. Every one of the topics below is authored on this skeleton.</p>
  <div class="anatomy">""")
for em, name, desc in anatomy:
    add(f'<div class="an"><span class="em">{em}</span><div><b>{name}</b><span>{desc}</span></div></div>')
add("""</div>
</section>

<div class="legend">Level:
  <span class="lv Beginner">Beginner</span>
  <span class="lv CoreQA">Core QA</span>
  <span class="lv Advanced">Advanced</span>
  <span style="margin-left:10px" class="badge-new">NEW / UPGRADED since v2</span>
</div>
""")

mod_no = 0
for t in tracks:
    tag = f'<span class="tag">· {t["tag"]}</span>' if t["tag"] else ""
    add(f"""<section class="track">
  <div class="track-head"><span class="track-id">Track {t["id"]}</span><h2>{t["title"]}</h2>{tag}</div>
  <p class="desc">{t["desc"]}</p>""")
    for m in t["modules"]:
        mod_no += 1
        cls = "module is-new" if (m["new"] or m["upgraded"]) else "module"
        badge = ""
        if m["new"]: badge = '<span class="badge-new">NEW</span>'
        elif m["upgraded"]: badge = '<span class="badge-new">UPGRADED</span>'
        lv = m["level"].replace(" ", "")
        add(f"""<div class="{cls}">
    <div class="mod-head"><span class="mod-num">M{mod_no}</span><h3>{m["title"]}</h3>
      <span class="lv {lv}">{m["level"]}</span>{badge}</div>""")
        if m.get("note"):
            add(f'<div class="mod-note">{m["note"]}</div>')
        add('<table class="chapters">')
        for ch_title, topics, ch_new in m["chapters"]:
            nb = '<span class="nb">NEW</span>' if ch_new and not (m["new"] or m["upgraded"]) else ""
            chips = "".join(f'<span class="topic">{tp}</span>' for tp in topics)
            add(f'<tr><td class="ch">{ch_title}{nb}</td><td><div class="topics">{chips}</div></td></tr>')
        add("</table>")
        add('<div class="mod-meta">\U0001F527 opens with a setup guide · \U0001F517 closes with 3–5 curated free resources</div>')
        add("</div>")
    if t.get("checkpoint"):
        cp = t["checkpoint"]
        add(f'<div class="checkpoint"><b>\U0001F680 {cp["title"]}</b><p>{cp["desc"]}</p></div>')
    add("</section>")

add("""<section class="panel">
  <h2>Validated against</h2>
  <ul class="sources" style="margin:12px 0 0; padding-left:20px">""")
for name, what in sources:
    add(f"<li><b>{name}</b> — {what}</li>")
add(f"""</ul>
</section>

<section class="panel cta">
  <p><b>This map is approved and locked (v3 on 2026-07-09, v3.1 additions same day).</b> Next: the wiki taxonomy is rebuilt to this map, and <b>Track A · Module 1</b> is written first,
  live in the platform with the full mentor format, for your review — then M2→M4, then B→G, checkpoint by checkpoint.</p>
</section>
</div>""")

html = "\n".join(parts)
out = "/private/tmp/claude-501/-Users-sajanathapa-Desktop-1/9298bb44-e37b-469c-a23d-cefc71ba064d/scratchpad/notes-curriculum-preview.html"
open(out, "w").write(html)
print(f"tracks=7 modules={n_modules} chapters={n_chapters} topics={n_topics} bytes={len(html)}")
