# Graph Report - .  (2026-06-12)

## Corpus Check
- 17 files · ~74,539 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 142 nodes · 166 edges · 13 communities (11 shown, 2 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Defect Management & Bug Lifecycle|Defect Management & Bug Lifecycle]]
- [[_COMMUNITY_Selenium + Java Automation Stack|Selenium + Java Automation Stack]]
- [[_COMMUNITY_API Types & REST Architecture|API Types & REST Architecture]]
- [[_COMMUNITY_HTML & Semantic Markup|HTML & Semantic Markup]]
- [[_COMMUNITY_CSS Layout & Styling|CSS Layout & Styling]]
- [[_COMMUNITY_Manual Testing Foundation & AMS Project|Manual Testing Foundation & AMS Project]]
- [[_COMMUNITY_Testing Fundamentals & SDLC|Testing Fundamentals & SDLC]]
- [[_COMMUNITY_Test Planning & EntryExit Criteria|Test Planning & Entry/Exit Criteria]]
- [[_COMMUNITY_QA Learning Platform Product Plan|QA Learning Platform Product Plan]]
- [[_COMMUNITY_UIUX & Accessibility Testing|UI/UX & Accessibility Testing]]
- [[_COMMUNITY_HTTP Fundamentals|HTTP Fundamentals]]
- [[_COMMUNITY_Agile & Scrum|Agile & Scrum]]
- [[_COMMUNITY_Smoke & Sanity Testing|Smoke & Sanity Testing]]

## God Nodes (most connected - your core abstractions)
1. `API (Application Programming Interface)` - 15 edges
2. `CSS (Cascading Style Sheets)` - 13 edges
3. `Selenium + Java Automation Roadmap (65 Days)` - 12 edges
4. `HTML (HyperText Markup Language)` - 11 edges
5. `Test Plan` - 7 edges
6. `Defect / Bug` - 6 edges
7. `QA Module (90-Day Manual QA Roadmap)` - 6 edges
8. `REST Constraints` - 5 edges
9. `HTTP Methods` - 5 edges
10. `HTTP Status Codes` - 5 edges

## Surprising Connections (you probably didn't know these)
- `BuggyShop Practice App (The Moat)` --semantically_similar_to--> `Practice Sites (DemoQA, OrangeHRM, SauceDemo, The Internet)`  [INFERRED] [semantically similar]
  QA-Learning-Platform-Plan.md → Resources/SELENIUM + JAVA AUTOMATION TESTING ROADMAP.md
- `Track A — Manual Testing Foundation` --references--> `QA Module (90-Day Manual QA Roadmap)`  [INFERRED]
  QA-Learning-Platform-Plan.md → Resources/QA module.md
- `The Two Roadmaps (Project Spine)` --references--> `QA Module (90-Day Manual QA Roadmap)`  [EXTRACTED]
  CLAUDE.md → Resources/QA module.md
- `Notes Conventions (Teaching Not Shipping)` --conceptually_related_to--> `Java as Primary Teaching Language (Decision Locked)`  [INFERRED]
  CLAUDE.md → QA-Learning-Platform-Plan.md
- `Track B — Automation Foundation` --references--> `Selenium + Java Automation Roadmap (65 Days)`  [INFERRED]
  QA-Learning-Platform-Plan.md → Resources/SELENIUM + JAVA AUTOMATION TESTING ROADMAP.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **REST Architectural Constraints** — resources_api_rest, resources_api_stateless, resources_api_cacheable, resources_api_uniform_interface, resources_api_client_server [INFERRED 0.95]
- **Defect Management Flow** — phase_2_core_testing_skills_days_21_45_defect, phase_2_core_testing_skills_days_21_45_bug_life_cycle, phase_2_core_testing_skills_days_21_45_severity, phase_2_core_testing_skills_days_21_45_priority, phase_2_core_testing_skills_days_21_45_bug_report, phase_2_core_testing_skills_days_21_45_jira [INFERRED 0.85]
- **Test Planning Document Set** — phase_2_core_testing_skills_days_21_45_test_strategy, phase_2_core_testing_skills_days_21_45_test_plan, phase_2_core_testing_skills_days_21_45_entry_criteria, phase_2_core_testing_skills_days_21_45_exit_criteria, phase_2_core_testing_skills_days_21_45_rtm [INFERRED 0.85]
- **Selenium Automation Stack (Java to CI/CD)** — resources_java_essentials, resources_selenium_webdriver, resources_testng, resources_page_object_model, resources_github_actions [INFERRED 0.95]
- **V1 Platform Curriculum Sourced from Roadmaps** — qa_learning_platform_plan_v1_scope, resources_qa_module, resources_selenium_roadmap, qa_learning_platform_plan_buggyshop [INFERRED 0.85]
- **AMS Real-Time Feature Test Focus** — resources_ams_notification_system, resources_ams_auto_refresh, resources_test_plan_ams [INFERRED 0.85]
- **Semantic Document Structure and Accessibility** — resources_final_html_in_web_development_1_semantic_html, resources_final_html_in_web_development_1_semantic_elements, resources_final_html_in_web_development_1_accessibility, resources_final_html_in_web_development_1_seo [INFERRED 0.85]
- **CSS Responsive Layout Systems** — resources_final_css_in_web_development_1_flexbox, resources_final_css_in_web_development_1_css_grid, resources_final_css_in_web_development_1_media_queries, resources_final_css_in_web_development_1_container_queries [INFERRED 0.85]
- **HTML/CSS UI Foundation** — resources_final_html_in_web_development_1_html, resources_final_css_in_web_development_1_css, resources_final_css_in_web_development_1_separation_of_concerns [INFERRED 0.75]

## Communities (13 total, 2 thin omitted)

### Community 0 - "Defect Management & Bug Lifecycle"
Cohesion: 0.10
Nodes (22): Bug Life Cycle, Bug Report, Decision Table Testing, Defect / Bug, Defect Metrics & KPIs, JIRA, Priority, Regression Testing (+14 more)

### Community 1 - "Selenium + Java Automation Stack"
Cohesion: 0.16
Nodes (19): Notes Conventions (Teaching Not Shipping), My QA Project Knowledge Base, The Two Roadmaps (Project Spine), Java as Primary Teaching Language (Decision Locked), Track B — Automation Foundation, GitHub Actions CI/CD, Java Collections (List, HashMap), Phase 1 — Java Essentials for Selenium (+11 more)

### Community 2 - "API Types & REST Architecture"
Cohesion: 0.12
Nodes (19): API (Application Programming Interface), Cacheable, Client-Server Architecture, Composite API, GraphQL API, RPC / gRPC, Internal API, Overfetching & Underfetching (+11 more)

### Community 3 - "HTML & Semantic Markup"
Cohesion: 0.13
Nodes (17): Separation of Concerns (HTML/CSS), HTML Accessibility (ARIA, WCAG 2.1), Custom Data Attributes (data-*), DOCTYPE Declaration, Document Object Model (DOM), HTML5 Form Validation Attributes, HTML (HyperText Markup Language), HTML Entities (+9 more)

### Community 4 - "CSS Layout & Styling"
Cohesion: 0.18
Nodes (15): CSS Animations and Transitions, aspect-ratio Property, CSS Box Model, clamp() Fluid Typography, Container Queries, CSS (Cascading Style Sheets), CSS Architecture Methodologies (BEM, OOCSS, SMACSS), CSS Grid (+7 more)

### Community 5 - "Manual Testing Foundation & AMS Project"
Cohesion: 0.20
Nodes (11): Track A — Manual Testing Foundation, V1 Scope (Manual + Automation), AMS Auto-Refresh (WebSocket/Polling), AMS Automated Notification System (3/45-Day Alerts), Books Every Software Tester, Entry and Exit Criteria, QA Module (90-Day Manual QA Roadmap), STLC (Software Testing Life Cycle) (+3 more)

### Community 6 - "Testing Fundamentals & SDLC"
Cohesion: 0.20
Nodes (10): Risk Assessment Matrix, Risk-Based Testing, Test Strategy, Cost Multiplier of Defects, Role of QA in Modern Development, Software Development Life Cycle (SDLC), Shift-Left Testing, Shift-Right Testing (+2 more)

### Community 7 - "Test Planning & Entry/Exit Criteria"
Cohesion: 0.25
Nodes (9): Boundary Value Analysis (BVA), Entry Criteria, Equivalence Partitioning, Exit Criteria, IEEE 829 Test Plan Template, Resumption Criteria, Suspension Criteria, Test Plan (+1 more)

### Community 8 - "QA Learning Platform Product Plan"
Cohesion: 0.22
Nodes (9): QA Mastery Platform Plan, BuggyShop Practice App (The Moat), Competitors (TAU, Udemy, Guru99, BrowserStack), Core Differentiator (Visual + Hands-on + Graded), Lesson Engine (See/Try/Do/Prove/Show), Monetization (Free + Pro Subscription), Positioning (You Do It, Not Watch It), Tech Stack (Next.js, Supabase, Vercel) (+1 more)

### Community 9 - "UI/UX & Accessibility Testing"
Cohesion: 0.50
Nodes (4): Accessibility (a11y) Testing, Design System / Style Guide, Heuristic Evaluation (Nielsen's 10 Heuristics), QA Guide for Testing UI/UX Designs

### Community 10 - "HTTP Fundamentals"
Cohesion: 0.67
Nodes (3): Client-Server Model, HTTP Fundamentals for API Testing, HTTP Methods (GET, POST, PUT, DELETE)

## Knowledge Gaps
- **56 isolated node(s):** `Testing vs Debugging`, `Software Development Life Cycle (SDLC)`, `IEEE 829 Test Plan Template`, `Resumption Criteria`, `Risk Assessment Matrix` (+51 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `API (Application Programming Interface)` connect `API Types & REST Architecture` to `Defect Management & Bug Lifecycle`, `Testing Fundamentals & SDLC`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `HTTP Status Codes` connect `Defect Management & Bug Lifecycle` to `API Types & REST Architecture`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Selenium + Java Automation Roadmap (65 Days)` (e.g. with `Track B — Automation Foundation` and `Selenium Topic List`) actually correct?**
  _`Selenium + Java Automation Roadmap (65 Days)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Testing vs Debugging`, `Software Development Life Cycle (SDLC)`, `Shift-Right Testing` to the rest of the system?**
  _58 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Defect Management & Bug Lifecycle` be split into smaller, more focused modules?**
  _Cohesion score 0.1038961038961039 - nodes in this community are weakly interconnected._
- **Should `API Types & REST Architecture` be split into smaller, more focused modules?**
  _Cohesion score 0.12280701754385964 - nodes in this community are weakly interconnected._
- **Should `HTML & Semantic Markup` be split into smaller, more focused modules?**
  _Cohesion score 0.1323529411764706 - nodes in this community are weakly interconnected._