# My QA Project — Knowledge Base

Personal QA learning knowledge base. **Not a code repo** — a corpus of study
notes, roadmaps, and reference material for becoming a QA / automation tester.
No build, no tests, no git (yet).

## What this is

Owner is learning Quality Assurance: manual testing first, then Selenium + Java
automation. This folder is the single source of truth for notes, roadmaps, test
artifacts, and reference docs gathered during that journey.

## Structure

```
My Qa Projecct/
├── CLAUDE.md            ← this file
└── Resources/           ← all notes + reference material
    ├── QA module.md                          90-day manual QA roadmap (16 modules, 4 phases)
    ├── SELENIUM + JAVA AUTOMATION ... .md     65-day automation roadmap (Java→Selenium→TestNG→POM→CI/CD)
    ├── Selenium Topic List.md                 Selenium topic checklist
    ├── PHASE 1 — JAVA ESSENTIALS ... .md       Java fundamentals notes
    ├── PHASE 2_ CORE TESTING SKILLS ... .md    Days 21–45 detailed notes
    ├── FULL MODULES NOTES FOR QA.md            master notes dump (~22k words, largest)
    ├── API.md                                  API testing notes
    ├── HTTP Fundamentals for API Testing.md    HTTP reference
    ├── Test plan report  for AMS (1).md        sample test plan (AMS project)
    ├── What is Test Environment ... .md         QA/Stage/Preprod/Prod notes
    ├── _QA Guide for Testing UI_UX Designs.md   UI/UX testing guide
    ├── Books Every Software Tester.md           book list / notes
    ├── final HTML in Web Development (1).pdf     web-dev reference
    └── final CSS in Web Development (1)(2).pdf   web-dev reference (2 = duplicate)
```

## The two roadmaps (the spine of this project)

1. **Manual QA** — 90 days, 16 modules, 4 phases: Foundation → Core QA Skills →
   Specialized Testing → Real Projects & Job Prep. Ends at interview readiness.
2. **Selenium + Java automation** — 65 days: Java essentials → WebDriver core →
   TestNG + Page Object Model → Maven/reporting/CI-CD → end-to-end project +
   interview prep. Stack: Java 17, IntelliJ, Maven, TestNG, ChromeDriver,
   ExtentReports/Allure, Log4j2, Git + GitHub Actions. Practice sites: DemoQA,
   OrangeHRM, SauceDemo, The Internet (Heroku).

## How to help (conventions)

- **Notes are Markdown.** Match existing heading style: `# **Title**`, day-by-day
  `### **Day N — Topic**`. Keep the day/module numbering intact.
- **Teaching, not shipping.** Default to clear explanations, worked examples, and
  practice exercises over terse answers. The owner is learning — show the why.
- When asked for Selenium/Java code, use the project stack above (Java + Maven +
  TestNG + POM). Prefer realistic, runnable examples against the named practice
  sites.
- When filling roadmap days, write actual study content under the existing
  `### **Day N**` stubs rather than creating parallel files.
- Cite which note a fact came from when answering across files.
- For library/framework specifics (Selenium, TestNG, Maven), verify current API
  via Context7 docs rather than memory — versions move.

## Housekeeping (flag, don't auto-delete)

- `Resources/Unconfirmed 172025.crdownload` — 9.4MB partial/aborted Chrome
  download. Likely junk; confirm before removing.
- `final CSS in Web Development (2).pdf` — byte-identical duplicate of `(1)`.
- `.DS_Store` files — macOS cruft.
- No git repo. If versioning is wanted: `git init` + a `.gitignore` for
  `.DS_Store` / `*.crdownload`.

## Knowledge graph

`graphify-out/` holds a graphify knowledge graph of the notes (open
`graph.html`, read `GRAPH_REPORT.md`). Ask graph questions with
`/graphify query "..."`.
