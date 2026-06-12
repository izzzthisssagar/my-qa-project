# Graph Report - .  (2026-06-12)

## Corpus Check
- 11 files · ~84,506 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 227 nodes · 293 edges · 15 communities (13 shown, 2 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 35 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_CSS Layout & Styling|CSS Layout & Styling]]
- [[_COMMUNITY_Landing Site & Product Validation|Landing Site & Product Validation]]
- [[_COMMUNITY_API Types & REST Architecture|API Types & REST Architecture]]
- [[_COMMUNITY_BuggyShop Seeded Bugs (AuthCart)|BuggyShop Seeded Bugs (Auth/Cart)]]
- [[_COMMUNITY_Test Design Modules & BuggyShop Bugs|Test Design Modules & BuggyShop Bugs]]
- [[_COMMUNITY_Selenium + Java Automation Stack|Selenium + Java Automation Stack]]
- [[_COMMUNITY_Test Planning & EntryExit Criteria|Test Planning & Entry/Exit Criteria]]
- [[_COMMUNITY_HTTP Fundamentals|HTTP Fundamentals]]
- [[_COMMUNITY_Testing Fundamentals & SDLC|Testing Fundamentals & SDLC]]
- [[_COMMUNITY_Defect Management & Bug Lifecycle|Defect Management & Bug Lifecycle]]
- [[_COMMUNITY_BuggyShop Releases & Capstone|BuggyShop Releases & Capstone]]
- [[_COMMUNITY_Manual QA Roadmap & AMS Project|Manual QA Roadmap & AMS Project]]
- [[_COMMUNITY_UIUX & Accessibility Testing|UI/UX & Accessibility Testing]]
- [[_COMMUNITY_Agile & Scrum|Agile & Scrum]]
- [[_COMMUNITY_Smoke & Sanity Testing|Smoke & Sanity Testing]]

## God Nodes (most connected - your core abstractions)
1. `API (Application Programming Interface)` - 15 edges
2. `BuggyShop v1.0 Release` - 15 edges
3. `CSS (Cascading Style Sheets)` - 13 edges
4. `Selenium + Java Automation Roadmap (65 Days)` - 12 edges
5. `HTML (HyperText Markup Language)` - 11 edges
6. `BuggyShop Practice App` - 11 edges
7. `QA Mastery Validation Landing Site` - 10 edges
8. `Positioning (You Do It, Not Watch It)` - 9 edges
9. `Lesson 1 — BVA Visual Concept (A3.3)` - 9 edges
10. `Lesson 2 — First Real Bug Report (A4.4)` - 9 edges

## Surprising Connections (you probably didn't know these)
- `BuggyShop Practice App (The Moat)` --semantically_similar_to--> `Practice Sites (DemoQA, OrangeHRM, SauceDemo, The Internet)`  [INFERRED] [semantically similar]
  QA-Learning-Platform-Plan.md → Resources/SELENIUM + JAVA AUTOMATION TESTING ROADMAP.md
- `Track A — Manual Testing Foundation` --references--> `QA Module (90-Day Manual QA Roadmap)`  [INFERRED]
  QA-Learning-Platform-Plan.md → Resources/QA module.md
- `My QA Project Knowledge Base README` --references--> `QA Mastery Validation Landing Site`  [INFERRED]
  README.md → Product/landing-site/index.html
- `Severity` --semantically_similar_to--> `HTTP Status Codes`  [INFERRED] [semantically similar]
  Resources/PHASE 2_ CORE TESTING SKILLS (Days 21-45).md → Resources/API.md
- `The Two Roadmaps (Project Spine)` --references--> `QA Module (90-Day Manual QA Roadmap)`  [EXTRACTED]
  CLAUDE.md → Resources/QA module.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **BVA lesson teaches BVA via BuggyShop price filter and BS-008** — sample_lessons_lesson_1_bva_visual_concept_lesson, sample_lessons_lesson_1_bva_visual_concept_boundary_value_analysis, product_buggyshop_spec_bs_008 [INFERRED 0.85]
- **A3 design techniques each surface a seeded BuggyShop bug** — product_track_a_manual_testing_outline_module_a3, product_buggyshop_spec_seeded_bug, product_buggyshop_spec_buggyshop [INFERRED 0.75]
- **Landing-site validation loop (markets plan, drives waitlist, feeds kill/continue gate)** — landing_site_index_landing_page, qa_learning_platform_plan_positioning, qa_learning_platform_plan_validation_gate [INFERRED 0.85]
- **HTTP request-response cycle (methods over client-server yielding status codes)** — resources_http_fundamentals_for_api_testing_http_methods, resources_http_fundamentals_for_api_testing_client_server_model, resources_http_fundamentals_for_api_testing_status_codes [INFERRED 0.85]
- **Interactive lesson pattern (visual widget -> BuggyShop lab -> graded)** — qa_learning_platform_plan_differentiator, landing_site_index_boundary_hunter, landing_site_index_find_the_bug [INFERRED 0.85]

## Communities (15 total, 2 thin omitted)

### Community 0 - "CSS Layout & Styling"
Cohesion: 0.08
Nodes (32): CSS Animations and Transitions, aspect-ratio Property, CSS Box Model, clamp() Fluid Typography, Container Queries, CSS (Cascading Style Sheets), CSS Architecture Methodologies (BEM, OOCSS, SMACSS), CSS Grid (+24 more)

### Community 1 - "Landing Site & Product Validation"
Cohesion: 0.11
Nodes (27): Boundary Hunter Widget (Lesson A3.3), Curriculum Preview — Tracks A & B, Find the Bug Widget (Lesson A4.4), Hero Section — Don't watch testing. Do it., Hero CTA — Join the early-access waitlist, QA Mastery Validation Landing Site, Waitlist Form (Formspree), Landing Site README — Formspree/Netlify setup & QA checklist (+19 more)

### Community 2 - "API Types & REST Architecture"
Cohesion: 0.10
Nodes (26): API (Application Programming Interface), API Security Testing, Cacheable, Client-Server Architecture, Composite API, GraphQL API, RPC / gRPC, HTTP Methods (+18 more)

### Community 3 - "BuggyShop Seeded Bugs (Auth/Cart)"
Cohesion: 0.11
Nodes (25): BS-001 Broken Email Regex, BS-002 Wrong-Field Password Error Message, BS-003 Paste Bypasses Confirm-Password Match, BS-004 Double-Click Bypasses Terms Checkbox, BS-012 Free Shipping Off-By-One at Boundary, BS-016 PIN/ZIP Accepts Letters, BS-018 Intermittent Subtotal Bug, BS-019 Profile Email Re-validation Missing (+17 more)

### Community 4 - "Test Design Modules & BuggyShop Bugs"
Cohesion: 0.11
Nodes (23): BS-007 Quantity Field Accepts 0, BS-008 Price Filter Excludes Max Boundary, BS-011 Payment Decision-Table Rule Conflict, BS-014 Cancel After Shipped (Invalid State Transition), A4.6 Bug Hunt I (Graded Milestone), Decision Tables (A3.4), Equivalence Partitioning (A3.2), Error Guessing (A3.6) (+15 more)

### Community 5 - "Selenium + Java Automation Stack"
Cohesion: 0.16
Nodes (19): Notes Conventions (Teaching Not Shipping), My QA Project Knowledge Base, The Two Roadmaps (Project Spine), Java as Primary Teaching Language (Decision Locked), Track B — Automation Foundation, GitHub Actions CI/CD, Java Collections (List, HashMap), Phase 1 — Java Essentials for Selenium (+11 more)

### Community 6 - "Test Planning & Entry/Exit Criteria"
Cohesion: 0.14
Nodes (15): Boundary Value Analysis (BVA), Decision Table Testing, Entry Criteria, Equivalence Partitioning, Exit Criteria, IEEE 829 Test Plan Template, Requirements (BRS, FRS, SRS), Resumption Criteria (+7 more)

### Community 7 - "HTTP Fundamentals"
Cohesion: 0.15
Nodes (15): My QA Project Knowledge Base README, Client-Server Model, HTTP Fundamentals for API Testing, HTTP Authentication (Basic/Digest/Bearer), DELETE Method, GET Method, HTTP (Hypertext Transfer Protocol), HTTP Methods (GET/POST/PUT/DELETE/PATCH/HEAD/OPTIONS) (+7 more)

### Community 8 - "Testing Fundamentals & SDLC"
Cohesion: 0.20
Nodes (10): Risk Assessment Matrix, Risk-Based Testing, Test Strategy, Cost Multiplier of Defects, Role of QA in Modern Development, Software Development Life Cycle (SDLC), Shift-Left Testing, Shift-Right Testing (+2 more)

### Community 9 - "Defect Management & Bug Lifecycle"
Cohesion: 0.25
Nodes (9): Bug Life Cycle, Bug Report, Defect / Bug, Defect Metrics & KPIs, JIRA, Priority, Regression Testing, Retesting (+1 more)

### Community 10 - "BuggyShop Releases & Capstone"
Cohesion: 0.25
Nodes (9): BS-021 Wishlist Move-to-Cart Regression, BS-022 Heart Icon Blocks Add-to-Cart Regression, BS-023 Mobile Place-Order Button Hidden, Coupon System (v2.0), BuggyShop v1.1 Release (Wishlist + Regressions), BuggyShop v2.0 Release (Coupon + Capstone Bugs), A5.6 Capstone — Full Test Cycle on v2.0, Module A5 — Real-World Manual QA (+1 more)

### Community 11 - "Manual QA Roadmap & AMS Project"
Cohesion: 0.25
Nodes (9): AMS Auto-Refresh (WebSocket/Polling), AMS Automated Notification System (3/45-Day Alerts), Books Every Software Tester, Entry and Exit Criteria, QA Module (90-Day Manual QA Roadmap), STLC (Software Testing Life Cycle), Test Design Techniques (EP, BVA, Decision Table), Test Environment (QA, Stage, Preprod, Production) (+1 more)

### Community 12 - "UI/UX & Accessibility Testing"
Cohesion: 0.50
Nodes (4): Accessibility (a11y) Testing, Design System / Style Guide, Heuristic Evaluation (Nielsen's 10 Heuristics), QA Guide for Testing UI/UX Designs

## Knowledge Gaps
- **84 isolated node(s):** `Testing vs Debugging`, `Software Development Life Cycle (SDLC)`, `IEEE 829 Test Plan Template`, `Resumption Criteria`, `Risk Assessment Matrix` (+79 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `QA Mastery Validation Landing Site` connect `Landing Site & Product Validation` to `HTTP Fundamentals`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `API (Application Programming Interface)` connect `API Types & REST Architecture` to `Testing Fundamentals & SDLC`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `BuggyShop Practice App` connect `BuggyShop Seeded Bugs (Auth/Cart)` to `BuggyShop Releases & Capstone`, `Test Design Modules & BuggyShop Bugs`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Selenium + Java Automation Roadmap (65 Days)` (e.g. with `Track B — Automation Foundation` and `Selenium Topic List`) actually correct?**
  _`Selenium + Java Automation Roadmap (65 Days)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Testing vs Debugging`, `Software Development Life Cycle (SDLC)`, `Shift-Right Testing` to the rest of the system?**
  _85 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CSS Layout & Styling` be split into smaller, more focused modules?**
  _Cohesion score 0.08064516129032258 - nodes in this community are weakly interconnected._
- **Should `Landing Site & Product Validation` be split into smaller, more focused modules?**
  _Cohesion score 0.10826210826210826 - nodes in this community are weakly interconnected._