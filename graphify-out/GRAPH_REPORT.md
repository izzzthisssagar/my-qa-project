# Graph Report - .  (2026-06-13)

## Corpus Check
- 25 files · ~84,525 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 244 nodes · 309 edges · 13 communities (11 shown, 2 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 34 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_BuggyShop Bug Catalog|BuggyShop Bug Catalog]]
- [[_COMMUNITY_QA Knowledge Base Meta|QA Knowledge Base Meta]]
- [[_COMMUNITY_CSS Fundamentals|CSS Fundamentals]]
- [[_COMMUNITY_API & Web Protocols|API & Web Protocols]]
- [[_COMMUNITY_Track A Test Design|Track A Test Design]]
- [[_COMMUNITY_Validation Landing Site|Validation Landing Site]]
- [[_COMMUNITY_Test Planning & Criteria|Test Planning & Criteria]]
- [[_COMMUNITY_Selenium Java Automation|Selenium Java Automation]]
- [[_COMMUNITY_HTTP Methods|HTTP Methods]]
- [[_COMMUNITY_Defect Lifecycle & Tracking|Defect Lifecycle & Tracking]]
- [[_COMMUNITY_STLC & AMS Test Plan|STLC & AMS Test Plan]]
- [[_COMMUNITY_Agile & Scrum|Agile & Scrum]]
- [[_COMMUNITY_Smoke & Sanity Testing|Smoke & Sanity Testing]]

## God Nodes (most connected - your core abstractions)
1. `Resources/ folder (all notes + reference material)` - 16 edges
2. `BuggyShop v1.0 Release` - 15 edges
3. `API (Application Programming Interface)` - 15 edges
4. `CSS (Cascading Style Sheets)` - 13 edges
5. `BuggyShop Practice App` - 11 edges
6. `HTML (HyperText Markup Language)` - 11 edges
7. `Selenium + Java Automation Roadmap (65 Days)` - 10 edges
8. `Lesson 1 — BVA Visual Concept (A3.3)` - 9 edges
9. `Lesson 2 — First Real Bug Report (A4.4)` - 9 edges
10. `QA Mastery Validation Landing Site` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Sample Test Plan for AMS (Attendance Management System)` --part_of--> `Manual QA 4 phases: Foundation → Core QA Skills → Specialized Testing → Real Projects & Job Prep`  [AMBIGUOUS]
  Resources/Test plan report  for AMS (1).md → CLAUDE.md
- `Housekeeping items (crdownload junk, duplicate CSS PDF, .DS_Store, gitignored cruft)` --references--> `CSS in Web Development (PDF reference, has duplicate copy)`  [EXTRACTED]
  CLAUDE.md → Resources/final CSS in Web Development (1)(2).pdf
- `Find-the-Bug Public Challenge` --semantically_similar_to--> `Lesson 2 — First Real Bug Report (A4.4)`  [INFERRED] [semantically similar]
  /Users/sajanathapa/Desktop/My Qa Projecct/Product/Week4-Promotion-Kit.md → /Users/sajanathapa/Desktop/My Qa Projecct/Product/Sample-Lessons/Lesson-2-Bug-Hunt-Manual-Lab.md
- `Severity` --semantically_similar_to--> `HTTP Status Codes`  [INFERRED] [semantically similar]
  /Users/sajanathapa/Desktop/My Qa Projecct/Resources/PHASE 2_ CORE TESTING SKILLS (Days 21-45).md → /Users/sajanathapa/Desktop/My Qa Projecct/Resources/API.md
- `Selenium + Java automation roadmap (65 days)` --requires--> `Automation tech stack (Java 17, IntelliJ, Maven, TestNG, ChromeDriver, ExtentReports/Allure, Log4j2, Git + GitHub Actions)`  [EXTRACTED]
  Resources/SELENIUM + JAVA AUTOMATION TESTING ROADMAP.md → CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **BVA lesson teaches BVA via BuggyShop price filter and BS-008** — sample_lessons_lesson_1_bva_visual_concept_lesson, sample_lessons_lesson_1_bva_visual_concept_boundary_value_analysis, product_buggyshop_spec_bs_008 [INFERRED 0.85]
- **A3 design techniques each surface a seeded BuggyShop bug** — product_track_a_manual_testing_outline_module_a3, product_buggyshop_spec_seeded_bug, product_buggyshop_spec_buggyshop [INFERRED 0.75]
- **Landing-site validation loop (markets plan, drives waitlist, feeds kill/continue gate)** — landing_site_index_landing_page, qa_learning_platform_plan_positioning, qa_learning_platform_plan_validation_gate [INFERRED 0.85]
- **Interactive lesson pattern (visual widget -> BuggyShop lab -> graded)** — qa_learning_platform_plan_differentiator, landing_site_index_boundary_hunter, landing_site_index_find_the_bug [INFERRED 0.85]
- **REST Architectural Constraints** — resources_api_rest, resources_api_stateless, resources_api_cacheable, resources_api_uniform_interface, resources_api_client_server [INFERRED 0.95]
- **HTTP request-response cycle (methods over client-server yielding status codes)** — resources_http_fundamentals_for_api_testing_http_methods, resources_http_fundamentals_for_api_testing_client_server_model, resources_http_fundamentals_for_api_testing_status_codes [INFERRED 0.85]
- **Defect Management Flow** — phase_2_core_testing_skills_days_21_45_defect, phase_2_core_testing_skills_days_21_45_bug_life_cycle, phase_2_core_testing_skills_days_21_45_severity, phase_2_core_testing_skills_days_21_45_priority, phase_2_core_testing_skills_days_21_45_bug_report, phase_2_core_testing_skills_days_21_45_jira [INFERRED 0.85]
- **Test Planning Document Set** — phase_2_core_testing_skills_days_21_45_test_strategy, phase_2_core_testing_skills_days_21_45_test_plan, phase_2_core_testing_skills_days_21_45_entry_criteria, phase_2_core_testing_skills_days_21_45_exit_criteria, phase_2_core_testing_skills_days_21_45_rtm [INFERRED 0.85]
- **Selenium Automation Stack (Java to CI/CD)** — resources_java_essentials, resources_selenium_webdriver, resources_testng, resources_page_object_model, resources_github_actions [INFERRED 0.95]
- **AMS Real-Time Feature Test Focus** — resources_ams_notification_system, resources_ams_auto_refresh, resources_test_plan_ams [INFERRED 0.85]
- **CSS Responsive Layout Systems** — resources_final_css_in_web_development_1_flexbox, resources_final_css_in_web_development_1_css_grid, resources_final_css_in_web_development_1_media_queries, resources_final_css_in_web_development_1_container_queries [INFERRED 0.85]
- **HTML/CSS UI Foundation** — resources_final_html_in_web_development_1_html, resources_final_css_in_web_development_1_css, resources_final_css_in_web_development_1_separation_of_concerns [INFERRED 0.75]
- **Semantic Document Structure and Accessibility** — resources_final_html_in_web_development_1_semantic_html, resources_final_html_in_web_development_1_semantic_elements, resources_final_html_in_web_development_1_accessibility, resources_final_html_in_web_development_1_seo [INFERRED 0.85]
- **Manual QA learning progression through 4 phases ending interview-ready** — manual_qa_roadmap, manual_qa_phases, phase2_core_testing_skills, full_modules_notes [INFERRED 0.85]
- **Selenium + Java automation progression: Java → WebDriver → TestNG + POM → Maven/CI-CD → end-to-end project** — selenium_java_roadmap, selenium_java_phases, phase1_java_essentials, selenium_topic_list, automation_stack, practice_sites [INFERRED 0.85]
- **Notes corpus feeds the QA Learning Platform plan and curriculum** — claude_md_resources_folder, qa_learning_platform_plan, product_folder, qa_learning_platform [INFERRED 0.85]
- **Resources notes indexed into the graphify knowledge graph for querying** — claude_md_resources_folder, graphify_out, claude_md_project_knowledge_base [EXTRACTED 1.00]

## Communities (13 total, 2 thin omitted)

### Community 0 - "BuggyShop Bug Catalog"
Cohesion: 0.08
Nodes (34): BS-001 Broken Email Regex, BS-002 Wrong-Field Password Error Message, BS-003 Paste Bypasses Confirm-Password Match, BS-004 Double-Click Bypasses Terms Checkbox, BS-012 Free Shipping Off-By-One at Boundary, BS-016 PIN/ZIP Accepts Letters, BS-018 Intermittent Subtotal Bug, BS-019 Profile Email Re-validation Missing (+26 more)

### Community 1 - "QA Knowledge Base Meta"
Cohesion: 0.08
Nodes (33): API testing notes, Automation tech stack (Java 17, IntelliJ, Maven, TestNG, ChromeDriver, ExtentReports/Allure, Log4j2, Git + GitHub Actions), Books Every Software Tester (book list / notes), Public GitHub repo izzzthisssagar/my-qa-project, Not a code repo (notes corpus, no build/no tests), Owner — QA / automation tester learner, My QA Project Knowledge Base (personal QA study corpus), Resources/ folder (all notes + reference material) (+25 more)

### Community 2 - "CSS Fundamentals"
Cohesion: 0.08
Nodes (32): CSS Animations and Transitions, aspect-ratio Property, CSS Box Model, clamp() Fluid Typography, Container Queries, CSS (Cascading Style Sheets), CSS Architecture Methodologies (BEM, OOCSS, SMACSS), CSS Grid (+24 more)

### Community 3 - "API & Web Protocols"
Cohesion: 0.08
Nodes (30): API (Application Programming Interface), API Security Testing, Cacheable, Client-Server Architecture, Composite API, GraphQL API, RPC / gRPC, HTTP Methods (+22 more)

### Community 4 - "Track A Test Design"
Cohesion: 0.11
Nodes (23): BS-007 Quantity Field Accepts 0, BS-008 Price Filter Excludes Max Boundary, BS-011 Payment Decision-Table Rule Conflict, BS-014 Cancel After Shipped (Invalid State Transition), A4.6 Bug Hunt I (Graded Milestone), Decision Tables (A3.4), Equivalence Partitioning (A3.2), Error Guessing (A3.6) (+15 more)

### Community 5 - "Validation Landing Site"
Cohesion: 0.13
Nodes (22): Boundary Hunter Widget (Lesson A3.3), Curriculum Preview — Tracks A & B, Find the Bug Widget (Lesson A4.4), Hero Section — Don't watch testing. Do it., Hero CTA — Join the early-access waitlist, QA Mastery Validation Landing Site, Waitlist Form (Formspree), Landing Site README — Formspree/Netlify setup & QA checklist (+14 more)

### Community 6 - "Test Planning & Criteria"
Cohesion: 0.10
Nodes (21): Boundary Value Analysis (BVA), Decision Table Testing, Entry Criteria, Equivalence Partitioning, Exit Criteria, IEEE 829 Test Plan Template, Requirements (BRS, FRS, SRS), Resumption Criteria (+13 more)

### Community 7 - "Selenium Java Automation"
Cohesion: 0.20
Nodes (15): GitHub Actions CI/CD, Java Collections (List, HashMap), Phase 1 — Java Essentials for Selenium, Java Exception Handling, Java OOP (Classes, Objects, Inheritance, Interfaces), Locators (XPath, CSS Selectors), Maven, Page Object Model (POM) (+7 more)

### Community 8 - "HTTP Methods"
Cohesion: 0.20
Nodes (12): HTTP Authentication (Basic/Digest/Bearer), Client-Server Model, DELETE Method, GET Method, HTTP (Hypertext Transfer Protocol), HTTP Methods (GET/POST/PUT/DELETE/PATCH/HEAD/OPTIONS), PATCH Method, POST Method (+4 more)

### Community 9 - "Defect Lifecycle & Tracking"
Cohesion: 0.25
Nodes (9): Bug Life Cycle, Bug Report, Defect / Bug, Defect Metrics & KPIs, JIRA, Priority, Regression Testing, Retesting (+1 more)

### Community 10 - "STLC & AMS Test Plan"
Cohesion: 0.25
Nodes (9): AMS Auto-Refresh (WebSocket/Polling), AMS Automated Notification System (3/45-Day Alerts), Books Every Software Tester, Entry and Exit Criteria, QA Module (90-Day Manual QA Roadmap), STLC (Software Testing Life Cycle), Test Design Techniques (EP, BVA, Decision Table), Test Environment (QA, Stage, Preprod, Production) (+1 more)

## Ambiguous Edges - Review These
- `Manual QA 4 phases: Foundation → Core QA Skills → Specialized Testing → Real Projects & Job Prep` → `Sample Test Plan for AMS (Attendance Management System)`  [AMBIGUOUS]
  CLAUDE.md · relation: part_of

## Knowledge Gaps
- **92 isolated node(s):** `BS-012 Free Shipping Off-By-One at Boundary`, `BS-016 PIN/ZIP Accepts Letters`, `BS-018 Intermittent Subtotal Bug`, `BS-023 Mobile Place-Order Button Hidden`, `Coupon System (v2.0)` (+87 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Manual QA 4 phases: Foundation → Core QA Skills → Specialized Testing → Real Projects & Job Prep` and `Sample Test Plan for AMS (Attendance Management System)`?**
  _Edge tagged AMBIGUOUS (relation: part_of) - confidence is low._
- **Why does `BuggyShop Practice App` connect `BuggyShop Bug Catalog` to `Track A Test Design`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `HTTP Status Codes` connect `API & Web Protocols` to `Defect Lifecycle & Tracking`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **What connects `BS-012 Free Shipping Off-By-One at Boundary`, `BS-016 PIN/ZIP Accepts Letters`, `BS-018 Intermittent Subtotal Bug` to the rest of the system?**
  _93 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `BuggyShop Bug Catalog` be split into smaller, more focused modules?**
  _Cohesion score 0.08021390374331551 - nodes in this community are weakly interconnected._
- **Should `QA Knowledge Base Meta` be split into smaller, more focused modules?**
  _Cohesion score 0.07954545454545454 - nodes in this community are weakly interconnected._
- **Should `CSS Fundamentals` be split into smaller, more focused modules?**
  _Cohesion score 0.08064516129032258 - nodes in this community are weakly interconnected._