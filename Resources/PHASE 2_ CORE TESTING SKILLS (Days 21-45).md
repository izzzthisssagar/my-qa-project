# **PHASE 2: CORE TESTING SKILLS (Days 21-45)**

## **Complete Detailed Course Content with Tasks, Notes & Assignments**

---

## **📚 TABLE OF CONTENTS \- PHASE 2**

### **MODULE 5: Test Planning & Documentation (Days 21-25)**

* Day 21: Test Plan Document \- Structure & Components  
* Day 22: Test Strategy vs Test Plan  
* Day 23: Entry & Exit Criteria  
* Day 24: Risk-Based Testing Approach  
* Day 25: Creating Your First Test Plan Document

### **MODULE 6: Requirements Analysis (Days 26-30)**

* Day 26: Understanding Requirements (BRS, FRS, SRS)  
* Day 27: Requirements Traceability Matrix (RTM)  
* Day 28: How to Review Requirements  
* Day 29: Identifying Testable vs Non-Testable Requirements  
* Day 30: PROJECT 2 \- Create RTM for E-commerce Module

### **MODULE 7: Defect/Bug Management (Days 31-36)**

* Day 31: What is a Defect? Bug Life Cycle  
* Day 32: Severity vs Priority with Examples  
* Day 33: Writing Effective Bug Reports  
* Day 34: Introduction to JIRA (Bug Tracking Tool)  
* Day 35: Defect Metrics & KPIs  
* Day 36: PROJECT 3 \- Log 20 Bugs in JIRA for Sample App

### **MODULE 8: Test Execution & Reporting (Days 37-42)**

* Day 37: Test Environment Setup & Test Data  
* Day 38: Executing Test Cases \- Step by Step  
* Day 39: Test Execution Report & Status  
* Day 40: Smoke Testing vs Sanity Testing  
* Day 41: Regression Testing \- When & How  
* Day 42: Retesting vs Regression Testing

### **MODULE 9: Agile Testing Methodology (Days 43-45)**

* Day 43: Agile & Scrum Basics for Testers  
* Day 44: Sprint Planning, Daily Standup, Retrospective  
* Day 45: User Stories & Acceptance Criteria Testing

---

# **MODULE 5: TEST PLANNING & DOCUMENTATION**

---

## **📅 DAY 21: Test Plan Document \- Structure & Components**

### **📖 THEORY NOTES**

**What is a Test Plan?**

A Test Plan is a detailed document that outlines the strategy, approach, resources, and schedule for testing activities. It serves as a blueprint for the entire testing process.

**Why Test Plan is Important:**

1. **Provides Direction**: Clear roadmap for testing  
2. **Sets Expectations**: What will be tested and how  
3. **Resource Planning**: Team, tools, environment needs  
4. **Risk Management**: Identifies potential issues early  
5. **Communication Tool**: Aligns stakeholders  
6. **Baseline Document**: Reference throughout testing

**Who Creates Test Plan:**

* Test Manager  
* Test Lead  
* Senior QA Engineer

**When Created:**

* After requirement analysis  
* Before test case development  
* During test planning phase of STLC

---

### **IEEE 829 TEST PLAN TEMPLATE STRUCTURE:**

**1\. TEST PLAN IDENTIFIER**

* Unique ID for the test plan  
* Version number  
* Example: TP\_ECOMMERCE\_V1.0

**2\. INTRODUCTION**

* Brief overview of the project  
* Purpose of the test plan  
* Document scope

**Example:**

This test plan document outlines the testing strategy for the   
E-Commerce Shopping Cart Module version 2.5. The purpose is to   
ensure all functionalities meet business requirements and quality   
standards before production release.

**3\. TEST ITEMS / FEATURES TO BE TESTED**

* List all features/modules to be tested  
* Version/build numbers  
* Component details

**Example:**

Features to be Tested:  
\- User Registration & Login (v2.5)  
\- Product Search & Filter (v2.5)  
\- Shopping Cart Management (v2.5)  
\- Checkout Process (v2.5)  
\- Payment Gateway Integration (v2.5)  
\- Order Management (v2.5)

**4\. FEATURES NOT TO BE TESTED (OUT OF SCOPE)**

* Explicitly state what won't be tested  
* Reasons for exclusion

**Example:**

Out of Scope:  
\- Admin panel (will be tested separately)  
\- Mobile app (separate test plan)  
\- Third-party payment gateway internals  
\- Backend database performance (separate test plan)

**5\. APPROACH / TEST STRATEGY**

* Testing methodology  
* Types of testing to be performed  
* Test levels  
* Test design techniques to be used

**Example:**

Testing Approach:  
\- Manual testing for functional scenarios  
\- Exploratory testing for new features  
\- Regression testing for existing features  
\- Black-box testing techniques (EP, BVA, Decision Tables)  
\- Agile methodology with 2-week sprints

**6\. ITEM PASS/FAIL CRITERIA**

* Criteria to determine if testing passed or failed  
* Quality gates  
* Acceptance criteria

**Example:**

Pass Criteria:  
\- 100% of P0 test cases executed and passed  
\- 95% of P1 test cases passed  
\- No open critical/high severity defects  
\- All planned test scenarios executed  
\- Performance benchmarks met

Fail Criteria:  
\- Any critical defect open  
\- \<90% test case pass rate  
\- Environment not stable  
\- Key functionality not working

**7\. SUSPENSION CRITERIA & RESUMPTION REQUIREMENTS**

**Suspension Criteria** (When to stop testing):

* Critical defects blocking testing  
* Test environment unavailable  
* Build unstable (crashes frequently)  
* Major changes in requirements  
* Insufficient resources

**Resumption Requirements** (When to resume):

* Critical defects fixed  
* Stable environment available  
* New build deployed  
* Requirements clarified  
* Resources available

**8\. TEST DELIVERABLES**

**Before Testing:**

* Test Plan document  
* Test scenarios  
* Test cases  
* Test data  
* RTM

**During Testing:**

* Test execution reports  
* Defect reports  
* Test logs  
* Status reports

**After Testing:**

* Test summary report  
* Test metrics  
* Lessons learned document  
* Test closure report

**9\. TEST ENVIRONMENT**

Specify:

* Hardware requirements  
* Software requirements  
* Network configuration  
* Test data requirements  
* Tools needed

**Example:**

Hardware:  
\- Server: 16GB RAM, 500GB Storage  
\- Client: Windows 10, 8GB RAM

Software:  
\- OS: Windows Server 2019  
\- Database: MySQL 8.0  
\- Browser: Chrome (latest), Firefox (latest), Edge  
\- Test Management: TestRail  
\- Bug Tracking: JIRA

Network:  
\- Internet connection: 100 Mbps  
\- VPN access for remote testers

Test Data:  
\- 100 user accounts  
\- 500 product records  
\- Sample payment test cards

**10\. STAFFING & TRAINING NEEDS**

**Team Structure:**

* Test Manager: 1  
* Test Lead: 1  
* Senior QA Engineers: 2  
* Junior QA Engineers: 3  
* Total: 7 team members

**Training Required:**

* JIRA training for new members  
* Domain knowledge training (e-commerce)  
* Payment gateway testing training  
* Automation tool training (if applicable)

**11\. RESPONSIBILITIES**

| Role | Responsibilities |
| ----- | ----- |
| Test Manager | Overall test planning, resource allocation, stakeholder communication |
| Test Lead | Test case review, execution monitoring, defect triage |
| Senior QA | Test design, complex scenario testing, mentoring juniors |
| Junior QA | Test execution, defect logging, test data preparation |
| Developer | Unit testing, defect fixing, test environment support |
| Business Analyst | Requirement clarification, UAT support |

**12\. SCHEDULE**

| Phase | Start Date | End Date | Duration |
| ----- | ----- | ----- | ----- |
| Test Planning | Jan 1 | Jan 5 | 5 days |
| Test Design | Jan 6 | Jan 15 | 10 days |
| Environment Setup | Jan 10 | Jan 12 | 3 days |
| Test Execution | Jan 16 | Feb 5 | 21 days |
| Regression Testing | Feb 6 | Feb 10 | 5 days |
| UAT | Feb 11 | Feb 15 | 5 days |
| Test Closure | Feb 16 | Feb 17 | 2 days |

**13\. RISKS & MITIGATION**

| Risk | Impact | Probability | Mitigation |
| ----- | ----- | ----- | ----- |
| Resource unavailability | High | Medium | Cross-train team members |
| Environment instability | High | High | Have backup environment |
| Requirement changes | Medium | High | Follow change management process |
| Third-party API issues | High | Medium | Mock services for testing |
| Tight timeline | Medium | High | Prioritize critical test cases |

**14\. APPROVALS**

| Name | Role | Signature | Date |
| ----- | ----- | ----- | ----- |
| John Doe | Test Manager |  |  |
| Jane Smith | Project Manager |  |  |
| Mike Johnson | Development Lead |  |  |
| Sarah Williams | Business Analyst |  |  |

---

### **TEST PLAN BEST PRACTICES:**

**DO:** ✅ Keep it clear and concise ✅ Make it specific and measurable ✅ Get stakeholder buy-in ✅ Update regularly ✅ Make it realistic ✅ Include all necessary details ✅ Use templates for consistency

**DON'T:** ❌ Make it too lengthy (20+ pages) ❌ Be vague or ambiguous ❌ Over-promise on timelines ❌ Ignore risks ❌ Create and forget (must be living document) ❌ Skip stakeholder approval

---

### **SAMPLE TEST PLAN EXCERPT:**

TEST PLAN DOCUMENT  
Project: E-Commerce Shopping Cart  
Version: 1.0  
Date: January 1, 2025

1\. INTRODUCTION  
This document outlines the comprehensive testing strategy for the   
Shopping Cart module of the E-Commerce platform. The testing will   
ensure the module meets all functional requirements and quality standards.

2\. SCOPE  
In Scope:  
\- Add/Remove items from cart  
\- Update quantity  
\- Apply discount coupons  
\- Calculate total with tax  
\- Save cart for later  
\- Guest checkout  
\- Registered user checkout

Out of Scope:  
\- Payment processing (separate test plan)  
\- Product catalog management  
\- User profile management

3\. TEST APPROACH  
We will follow a manual testing approach using:  
\- Functional testing for all features  
\- Equivalence Partitioning and BVA for input validation  
\- Decision tables for discount calculations  
\- Exploratory testing for usability  
\- Regression testing after each bug fix

4\. PASS/FAIL CRITERIA  
Pass:   
\- All P0 test cases passed (100%)  
\- P1 test cases passed (≥95%)  
\- No critical/high defects open  
\- Performance: Page load \<3 seconds

Fail:  
\- Any critical defect open  
\- P0 test case failure  
\- Major functionality broken

5\. SCHEDULE  
\- Test Planning: 5 days  
\- Test Design: 10 days  
\- Test Execution: 15 days  
\- Regression: 5 days  
Total: 35 days

6\. TEAM  
\- Test Lead: 1  
\- QA Engineers: 4  
Total: 5 members

7\. RISKS  
\- Third-party API instability (Mitigation: Use mock services)  
\- Resource shortage (Mitigation: Cross-training)  
\- Environment issues (Mitigation: Backup environment)

APPROVED BY:  
Test Manager: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_

---

### **✍️ PRACTICAL TASK (3 hours)**

**Task 21.1: Analyze Test Plans**

Review 2 sample test plans (search online for "sample test plan document PDF") and:

* Identify all sections  
* Note what's good  
* Note what's missing  
* List improvements you'd make

**Task 21.2: Identify Components**

You're given a project: "Online Banking System \- Fund Transfer Module"

For each test plan section, write what you would include:

1. Features to be tested (list at least 5\)  
2. Features not to be tested (list 3\)  
3. Test approach (describe in 2-3 paragraphs)  
4. Pass/Fail criteria (at least 3 each)  
5. Test deliverables (list 10\)  
6. Risks (identify 5 with mitigation)

**Task 21.3: Schedule Creation**

Create a detailed test schedule for a project with:

* Test Planning: 1 week  
* Test Case Development: 2 weeks  
* Environment Setup: 3 days (parallel to test case development)  
* Test Execution: 3 weeks  
* Regression: 1 week  
* UAT: 1 week

Create a Gantt chart or timeline showing all phases.

**Task 21.4: Risk Assessment**

For "Healthcare Patient Management System", identify:

* 10 potential risks  
* Impact (High/Medium/Low)  
* Probability (High/Medium/Low)  
* Mitigation strategy for each

**Task 21.5: Real Project Analysis**

Choose any software you use (e.g., Gmail, Amazon, Netflix):

* Imagine you're testing one feature  
* Write the "Features to be tested" section  
* Write the "Test Approach" section  
* Define Pass/Fail criteria

### **📝 ASSIGNMENT (2.5 hours)**

**1\. Complete Test Plan Template:**

Create a blank test plan template in Word/Google Docs with:

* All sections from IEEE 829  
* Proper formatting and structure  
* Instructions/examples in each section  
* Make it reusable

**2\. Mini Test Plan:**

Write a 3-4 page test plan for:

**Project**: "Social Media \- Post Creation Feature"

Include:

* Introduction  
* Scope (In/Out)  
* Test Approach  
* Pass/Fail Criteria  
* Test Deliverables  
* Schedule  
* Risks & Mitigation

**3\. Comparison Document:**

Create a comparison table:

| Section | Purpose | Importance (H/M/L) | Common Mistakes |
| ----- | ----- | ----- | ----- |
| Test Items |  |  |  |
| Approach |  |  |  |
| Pass/Fail |  |  |  |
| ... |  |  |  |

**4\. Research Assignment:**

Research and document:

* Differences between IEEE 829 and Agile test plans  
* When to use which format  
* Industry trends in test planning

### **📚 RESOURCES**

* Download: IEEE 829 Test Plan Template  
* Article: "How to Write Test Plan" \- Guru99  
* Video: "Test Planning Tutorial"  
* Sample: Search "Test Plan Sample Document PDF"

---

## **📅 DAY 22: Test Strategy vs Test Plan**

### **📖 THEORY NOTES**

**Understanding the Difference:**

Many people confuse Test Strategy with Test Plan. They are related but serve different purposes.

---

### **TEST STRATEGY**

**Definition**: High-level document defining the overall approach to testing for an organization or project.

**Characteristics:**

* Strategic, high-level  
* Long-term, reusable  
* Created once per organization/product line  
* Rarely changes  
* Defines "HOW" testing will be done in general  
* Usually 5-10 pages

**Created By:**

* Test Manager  
* QA Manager  
* Testing Architect

**When Created:**

* At organizational level (once)  
* At project inception  
* Before test plan

**Contains:**

* Testing objectives  
* Testing approach and methodology  
* Test levels to be performed  
* Types of testing  
* Roles and responsibilities  
* Test environment strategy  
* Tools and technologies  
* Defect management approach  
* Risk analysis approach

**Example Test Strategy Content:**

TESTING STRATEGY  
Organization: TechCorp Solutions

1\. TESTING OBJECTIVES  
\- Ensure product quality meets industry standards  
\- Reduce production defects by 90%  
\- Achieve 95% test coverage  
\- Deliver defect-free releases

2\. TESTING APPROACH  
\- Follow Agile methodology  
\- Continuous testing in sprints  
\- Automated regression testing  
\- Risk-based testing prioritization

3\. TEST LEVELS  
All projects will perform:  
\- Unit Testing (by developers)  
\- Integration Testing (by QA \+ developers)  
\- System Testing (by QA team)  
\- UAT (by business users)

4\. TYPES OF TESTING  
Mandatory:  
\- Functional Testing  
\- Regression Testing  
\- Smoke Testing

Conditional (based on project):  
\- Performance Testing  
\- Security Testing  
\- Compatibility Testing

5\. TOOLS STANDARD  
\- Test Management: TestRail  
\- Bug Tracking: JIRA  
\- Automation: Selenium (for web)  
\- API Testing: Postman  
\- Performance: JMeter

6\. DEFECT MANAGEMENT  
\- All defects logged in JIRA  
\- Priority and Severity mandatory fields  
\- Defect triage meeting twice weekly  
\- Critical defects fixed within 24 hours

---

### **TEST PLAN**

**Definition**: Detailed document describing the testing activities for a specific project or release.

**Characteristics:**

* Tactical, detailed  
* Project-specific  
* Created for each project/release  
* Updated frequently  
* Defines "WHAT" will be tested specifically  
* Usually 10-20 pages

**Created By:**

* Test Lead  
* Senior QA Engineer

**When Created:**

* For each project  
* During test planning phase  
* After requirements are clear

**Contains:**

* Specific features to be tested  
* Specific test scope  
* Detailed schedule  
* Specific resources assigned  
* Specific test cases  
* Specific risks for this project  
* Entry/Exit criteria  
* Deliverables

---

### **KEY DIFFERENCES:**

| Aspect | Test Strategy | Test Plan |
| ----- | ----- | ----- |
| **Level** | High-level | Detailed |
| **Scope** | Organization/Product line | Specific project |
| **Created By** | Test Manager/Architect | Test Lead |
| **Frequency** | Once (rarely updated) | Every project |
| **Purpose** | Define approach | Define activities |
| **Focus** | HOW to test | WHAT to test |
| **Reusability** | High | Low |
| **Changes** | Rare | Frequent |
| **Pages** | 5-10 pages | 10-20 pages |
| **Timeline** | Long-term | Short-term |
| **Content** | General guidelines | Specific details |
| **Audience** | Management, all projects | Project team |

---

### **RELATIONSHIP:**

Test Strategy (Organization Level)  
        ↓  
    Defines overall approach  
        ↓  
Test Plan (Project Level)  
        ↓  
    Implements strategy for specific project  
        ↓  
Test Cases (Execution Level)

**Example:**

**Test Strategy says:** "All web applications must undergo cross-browser testing on Chrome, Firefox, and Safari."

**Test Plan says:** "For E-Commerce project v2.5, cross-browser testing will be performed on:

* Chrome v120  
* Firefox v119  
* Safari v17 Schedule: Feb 1-3, 2025 Assigned to: QA Engineer John Doe Test cases: TC\_BROWSER\_001 to TC\_BROWSER\_050"

---

### **TEST STRATEGY EXAMPLE:**

ABC COMPANY \- SOFTWARE TESTING STRATEGY  
Version 1.0

1\. INTRODUCTION  
This document defines the overall testing strategy for all software   
projects at ABC Company.

2\. TESTING APPROACH  
\- Agile methodology with 2-week sprints  
\- Test-driven development encouraged  
\- Continuous integration and testing  
\- Shift-left approach (early testing)

3\. TEST LEVELS (All projects must perform)  
\- Unit Testing: Developers (JUnit, NUnit)  
\- Integration Testing: Developers \+ QA  
\- System Testing: QA Team  
\- UAT: Business Users

4\. MANDATORY TESTING TYPES  
\- Functional Testing (all features)  
\- Regression Testing (after each change)  
\- Smoke Testing (each build)

5\. CONDITIONAL TESTING (based on project type)  
\- Performance Testing (for high-traffic apps)  
\- Security Testing (for apps handling sensitive data)  
\- Compatibility Testing (for multi-platform apps)

6\. TOOLS AND TECHNOLOGIES  
\- Bug Tracking: JIRA (standard for all projects)  
\- Test Management: TestRail or Zephyr  
\- Automation: Selenium (web), Appium (mobile)  
\- API Testing: Postman, REST Assured  
\- Performance: JMeter, LoadRunner

7\. DEFECT MANAGEMENT PROCESS  
\- All defects must be logged within 24 hours of discovery  
\- Priority: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)  
\- Severity: S1 (Critical), S2 (Major), S3 (Minor), S4 (Trivial)  
\- P0 defects: Fix within 24 hours  
\- Defect triage: Daily for active projects

8\. TEST ENVIRONMENT STRATEGY  
\- Dedicated QA environment (mirrors production)  
\- Automated deployment to test environment  
\- Test data refresh weekly  
\- Environment available 24/7

9\. ENTRY/EXIT CRITERIA (Standard)  
Entry:  
\- Requirements signed off  
\- Test environment ready  
\- Test cases reviewed and approved

Exit:  
\- All test cases executed  
\- No P0/P1 defects open  
\- 95% pass rate achieved

10\. REPORTING  
\- Daily: Test execution status  
\- Weekly: Test summary report  
\- End of project: Test closure report

11\. ROLES & RESPONSIBILITIES  
Test Manager:  
\- Overall testing strategy  
\- Resource planning  
\- Stakeholder communication

Test Lead:  
\- Test planning for projects  
\- Team coordination  
\- Test execution monitoring

QA Engineers:  
\- Test case creation and execution  
\- Defect logging and tracking  
\- Test reporting

12\. RISK MANAGEMENT  
All projects must identify and document:  
\- Technical risks  
\- Schedule risks  
\- Resource risks  
\- Mitigation plans

13\. CONTINUOUS IMPROVEMENT  
\- Monthly retrospectives  
\- Lessons learned documentation  
\- Process improvements quarterly

APPROVED BY:  
CTO: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_  
VP Engineering: \_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_

---

### **TEST PLAN EXAMPLE:**

TEST PLAN \- E-COMMERCE SHOPPING CART  
Project: E-Commerce Platform v2.5  
Module: Shopping Cart  
Version: 1.0  
Date: January 15, 2025

1\. INTRODUCTION  
This test plan covers testing of Shopping Cart module version 2.5,   
following ABC Company's testing strategy.

2\. FEATURES TO BE TESTED  
\- Add item to cart  
\- Remove item from cart  
\- Update quantity (1-99)  
\- Apply discount coupon  
\- Calculate subtotal, tax, total  
\- Save cart for later  
\- Clear cart  
\- Guest checkout  
\- Registered user checkout

3\. FEATURES NOT TO BE TESTED  
\- Payment processing (separate test plan)  
\- Product recommendations  
\- User reviews  
\- Wishlist feature

4\. TEST APPROACH (per company strategy)  
\- Manual functional testing  
\- Exploratory testing for usability  
\- Regression testing (automated)  
\- Cross-browser testing (Chrome, Firefox, Safari)  
\- Test design: EP, BVA, Decision Tables

5\. TEST SCHEDULE  
\- Test Planning: Jan 15-17 (3 days)  
\- Test Design: Jan 18-25 (8 days)  
\- Environment Setup: Jan 22-24 (3 days)  
\- Test Execution: Jan 26-Feb 10 (16 days)  
\- Regression: Feb 11-13 (3 days)  
\- UAT: Feb 14-18 (5 days)

6\. TEAM  
\- Test Lead: John Doe  
\- Senior QA: Jane Smith  
\- QA Engineers: 3 (Mike, Sarah, Tom)  
Total: 5 members

7\. TEST ENVIRONMENT  
\- QA Environment: qa.ecommerce.com  
\- OS: Windows 10, macOS  
\- Browsers: Chrome 120, Firefox 119, Safari 17  
\- Database: MySQL 8.0 (test data refreshed Jan 20\)  
\- Test Users: 50 accounts (test user 1-50)

8\. TEST DELIVERABLES  
\- Test cases: \~150 test cases  
\- RTM: Linking requirements to test cases  
\- Test execution report: Daily  
\- Defect report: As found  
\- Test summary: Feb 19

9\. PASS/FAIL CRITERIA  
Pass:  
\- 100% P0 test cases passed  
\- 95% overall pass rate  
\- No P0/P1 open defects  
\- Performance: Page load \<3 seconds  
\- UAT sign-off received

Fail:  
\- Any P0 test case failure  
\- \<90% pass rate  
\- Critical defect open

10\. RISKS SPECIFIC TO THIS PROJECT  
Risk: Third-party coupon API may be unstable  
Impact: High | Probability: Medium  
Mitigation: Create mock coupon service for testing

Risk: Limited test data for edge cases  
Impact: Medium | Probability: High  
Mitigation: Generate synthetic test data

11\. DEPENDENCIES  
\- Product Catalog module must be stable  
\- User Authentication module must be working  
\- Payment Gateway stub must be ready

APPROVED BY:  
Test Lead: John Doe \_\_\_\_\_\_\_\_\_ Date: Jan 17, 2025  
Project Manager: \_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_\_\_\_

---

### **WHEN TO CREATE EACH:**

**Create Test Strategy:**

* When starting a new organization's QA process  
* When launching a new product line  
* When QA process needs standardization  
* Update: Annually or when major process changes

**Create Test Plan:**

* For every new project  
* For every major release  
* For every sprint (in Agile \- lightweight version)  
* Update: As project progresses

---

### **✍️ PRACTICAL TASK (3 hours)**

**Task 22.1: Identify Documents**

Read these statements and identify if they belong in Test Strategy (TS) or Test Plan (TP):

1. "All web applications must be tested on Chrome, Firefox, and Safari" \- \_\_\_  
2. "Shopping cart testing will be performed Jan 15-30 by John and Sarah" \- \_\_\_  
3. "Company standard: All defects logged in JIRA with mandatory priority field" \- \_\_\_  
4. "This project has 150 test cases covering 15 features" \- \_\_\_  
5. "Organization follows Agile methodology with 2-week sprints" \- \_\_\_  
6. "Pass criteria: No P0 defects, 95% test cases passed" \- \_\_\_  
7. "Test Manager role: Overall strategy and resource planning" \- \_\_\_  
8. "Risk: API may be unstable. Mitigation: Use mock service" \- \_\_\_  
9. "Standard tools: JIRA for bugs, TestRail for test management" \- \_\_\_  
10. "Test environment: qa.myapp.com, available Jan 10-Feb 20" \- \_\_\_

**Task 22.2: Create Test Strategy**

Write a 2-3 page Test Strategy for:

**Organization**: "FinTech Solutions Inc." (Financial Technology Company)

Include:

* Testing objectives  
* Testing approach and methodology  
* Test levels (mandatory)  
* Types of testing (mandatory and conditional)  
* Tools standard  
* Defect management approach  
* Roles and responsibilities  
* Entry/Exit criteria (standard)

**Task 22.3: Create Test Plan from Strategy**

Using your Test Strategy from Task 22.2, create a specific Test Plan for:

**Project**: "Mobile Banking App \- Money Transfer Feature"

Include:

* Specific features to test  
* Specific schedule  
* Specific team members  
* Specific test environment  
* Project-specific risks  
* Pass/Fail criteria for this project

**Task 22.4: Comparison Analysis**

Create a side-by-side comparison showing:

| Topic | What Test Strategy Says | What Test Plan Says |
| ----- | ----- | ----- |
| Testing approach | General methodology | Specific application |
| Team structure | Roles definition | Actual names assigned |
| Tools | Standard tools list | Tools used in this project |
| Schedule | Not included | Detailed timeline |
| Risks | General risk management | Project-specific risks |

**Task 22.5: Real-World Research**

Search online for:

* 2 Test Strategy documents  
* 2 Test Plan documents

Analyze and document:

* How do they differ?  
* What's common?  
* What's unique?  
* Quality assessment

### **📝 ASSIGNMENT (3 hours)**

**1\. Complete Strategy \+ Plan Set:**

Create both documents for:

**Company**: "HealthCare Systems Corp" **Project**: "Patient Appointment Scheduling Module"

Deliverables:

* Test Strategy document (3-4 pages)  
* Test Plan document (5-6 pages)  
* Document showing how Test Plan implements Test Strategy

**2\. Gap Analysis:**

You're given a Test Strategy that says: "All projects must perform security testing including SQL injection and XSS testing"

You review a Test Plan for "User Registration Module" and find:

* No mention of security testing  
* No SQL injection test cases  
* No XSS test cases

Write:

* Gap analysis report  
* What's missing?  
* Impact of gaps  
* Recommendations

**3\. Conversion Exercise:**

Convert these Test Strategy statements into specific Test Plan items:

**Strategy**: "Cross-browser testing mandatory for all web apps" **Plan**: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Strategy**: "P0 defects must be fixed within 24 hours" **Plan**: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Strategy**: "Use Selenium for automation" **Plan**: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**4\. Best Practices Document:**

Create a document: **Title**: "Test Strategy vs Test Plan \- Complete Guide"

Include:

* Definitions  
* Detailed differences  
* When to create each  
* How they relate  
* Best practices  
* Common mistakes  
* Templates for both  
* Real examples

(6-8 pages)

### **📚 RESOURCES**

* Article: "Test Strategy vs Test Plan" \- Software Testing Help  
* Video: "Difference between Test Strategy and Test Plan"  
* Download: Sample Test Strategy Template  
* Download: Sample Test Plan Template

---

## **📅 DAY 23: Entry & Exit Criteria**

### **📖 THEORY NOTES**

**What are Entry and Exit Criteria?**

Entry and Exit Criteria are pre-defined conditions that must be met before starting or completing a testing phase.

**Purpose:**

* Ensure readiness before starting  
* Ensure completeness before finishing  
* Avoid premature starts  
* Avoid incomplete closures  
* Set clear expectations  
* Improve quality

---

### **ENTRY CRITERIA**

**Definition**: Conditions that must be satisfied before testing can begin.

**Why Important:**

* Prevents starting testing prematurely  
* Ensures all prerequisites are met  
* Reduces wasted effort  
* Avoids test environment issues  
* Ensures test team readiness

**Who Defines:**

* Test Manager  
* Test Lead  
* In collaboration with Project Manager

**When Defined:**

* During test planning phase  
* Before test execution starts

---

### **ENTRY CRITERIA FOR DIFFERENT PHASES:**

**1\. ENTRY CRITERIA FOR TEST PLANNING**

✅ Requirements document available and approved ✅ Project scope defined ✅ Project timeline established ✅ Budget allocated ✅ Test team identified ✅ Stakeholder buy-in received

**Example:**

Test Planning Phase \- Entry Criteria:  
☐ Requirements Specification Document (version 2.0) approved  
☐ Project kickoff meeting completed  
☐ Testing budget approved ($50,000)  
☐ Test Manager assigned (John Doe)  
☐ Project timeline approved (3 months)

---

**2\. ENTRY CRITERIA FOR TEST CASE DEVELOPMENT**

✅ Test Plan document approved ✅ Requirements clearly defined and stable ✅ RTM (Requirements Traceability Matrix) created ✅ Test design technique selected ✅ Test case template available ✅ Domain knowledge training completed

**Example:**

Test Case Development \- Entry Criteria:  
☐ Test Plan v1.0 approved by Test Manager and PM  
☐ Requirements stable (no major changes expected)  
☐ RTM created with all requirements listed  
☐ Test case template shared with team  
☐ Team trained on application domain  
☐ Sample test cases reviewed and approved

---

**3\. ENTRY CRITERIA FOR TEST ENVIRONMENT SETUP**

✅ Test environment requirements documented ✅ Hardware/Software requirements approved ✅ Budget for environment approved ✅ Network connectivity available ✅ System admin support available ✅ Access permissions granted

**Example:**

Test Environment Setup \- Entry Criteria:  
☐ Environment spec document approved  
☐ Server: 16GB RAM, 500GB storage procured  
☐ Software licenses purchased  
☐ Network setup completed  
☐ VPN access provided to testers  
☐ Admin credentials received

---

**4\. ENTRY CRITERIA FOR TEST EXECUTION**

✅ Test environment ready and stable ✅ Test cases reviewed and approved ✅ Test data prepared and loaded ✅ Build deployed to test environment ✅ Smoke test passed ✅ Test team trained and ready ✅ Defect tracking tool configured ✅ Entry criteria checklist signed off

**Example:**

Test Execution \- Entry Criteria:  
☐ Test environment: qa.myapp.com is accessible  
☐ All test cases (150) reviewed and approved  
☐ Test data: 100 user accounts created  
☐ Build: v2.5.1 deployed to QA environment  
☐ Smoke test: 25/25 test cases passed  
☐ Test team: 5 members trained and available  
☐ JIRA configured with project and workflows  
☐ Test Lead sign-off received

---

**5\. ENTRY CRITERIA FOR REGRESSION TESTING**

✅ All new feature testing completed ✅ All critical defects fixed ✅ Regression test suite updated ✅ Stable build available ✅ Regression test cases prioritized ✅ Test environment stable

**Example:**

Regression Testing \- Entry Criteria:  
☐ New feature testing: 100% completed  
☐ Critical defects: 0 open  
☐ High priority defects: ≤2 open  
☐ Regression suite updated with new test cases  
☐ Build: v2.5.2 deployed (includes all fixes)  
☐ Environment: No issues in last 48 hours

---

**6\. ENTRY CRITERIA FOR UAT (User Acceptance Testing)**

✅ System testing completed ✅ No critical or high severity defects open ✅ UAT test cases prepared ✅ UAT environment setup ✅ UAT users identified and trained ✅ Production-like data available ✅ UAT schedule defined

**Example:**

UAT Phase \- Entry Criteria:  
☐ System testing: Complete with 95% pass rate  
☐ Open defects: 0 critical, 0 high, ≤5 medium  
☐ UAT test cases: 50 scenarios prepared  
☐ UAT environment: uat.myapp.com ready  
☐ Business users: 10 users trained  
☐ UAT data: Production copy loaded  
☐ UAT schedule: Feb 10-20 confirmed

---

### **EXIT CRITERIA**

**Definition**: Conditions that must be satisfied before testing can be considered complete.

**Why Important:**

* Ensures testing completeness  
* Prevents premature closure  
* Defines quality standards  
* Manages stakeholder expectations  
* Provides clear completion signal

---

### **EXIT CRITERIA FOR DIFFERENT PHASES:**

**1\. EXIT CRITERIA FOR TEST PLANNING**

✅ Test Plan document completed ✅ Test Plan reviewed by stakeholders ✅ Test Plan approved and signed off ✅ Test strategy defined ✅ Resources allocated ✅ Budget approved ✅ Schedule finalized

**Example:**

Test Planning Phase \- Exit Criteria:  
☐ Test Plan document completed (v1.0)  
☐ Reviewed by: PM, Dev Lead, Test Manager  
☐ Approved and signed by all stakeholders  
☐ Test approach defined and agreed  
☐ Team of 5 QA engineers allocated  
☐ Testing budget confirmed  
☐ Schedule baseline created

---

**2\. EXIT CRITERIA FOR TEST CASE DEVELOPMENT**

✅ All test cases written ✅ Test cases reviewed and approved ✅ RTM updated with test case IDs ✅ Test case coverage ≥95% ✅ Peer review completed ✅ Test Lead sign-off received

**Example:**

Test Case Development \- Exit Criteria:  
☐ Test cases: 150 test cases completed  
☐ Peer review: 100% test cases reviewed  
☐ Defects in test cases: All fixed  
☐ RTM: 100% requirements traced  
☐ Coverage: 98% requirements covered  
☐ Test Lead approval: Received  
☐ Test cases uploaded to TestRail

---

**3\. EXIT CRITERIA FOR TEST ENVIRONMENT SETUP**

✅ All components installed and configured ✅ Environment stable for 48 hours ✅ Smoke test passed ✅ All users have access ✅ Test data loaded successfully ✅ Backup and restore tested ✅ Environment documentation completed

**Example:**

Test Environment Setup \- Exit Criteria:  
☐ Application deployed successfully  
☐ Database configured and accessible  
☐ Network connectivity verified  
☐ Stability: No crashes/issues for 48 hours  
☐ Smoke test: 25/25 passed  
☐ All 5 testers have access  
☐ Test data: 100 users, 500 products loaded  
☐ Environment doc: Updated and shared

---

**4\. EXIT CRITERIA FOR TEST EXECUTION**

✅ All planned test cases executed ✅ Test execution rate ≥95% ✅ Test pass rate ≥90% ✅ No critical or high severity defects open ✅ All medium defects reviewed and accepted/fixed ✅ Regression testing completed ✅ Traceability matrix updated ✅ Test execution report completed

**Example:**

Test Execution \- Exit Criteria:  
☐ Test cases executed: 148/150 (98.7%)  
☐ Test cases passed: 140/148 (94.6%)  
☐ Critical defects open: 0  
☐ High defects open: 0  
☐ Medium defects open: 3 (all accepted by business)  
☐ Regression: 100 test cases, 98 passed  
☐ RTM: Updated with execution status  
☐ Test summary report: Completed

---

**5\. EXIT CRITERIA FOR REGRESSION TESTING**

✅ All regression test cases executed ✅ Pass rate ≥95% ✅ No new defects found ✅ Previously fixed defects verified ✅ No critical/high defects open ✅ Build stability confirmed

**Example:**

Regression Testing \- Exit Criteria:  
☐ Regression suite: 100/100 executed (100%)  
☐ Pass rate: 97/100 passed (97%)  
☐ New defects: 0 found  
☐ Retesting: 15/15 defect fixes verified  
☐ Critical defects: 0 open  
☐ High defects: 0 open  
☐ Build stability: Confirmed stable

---

**6\. EXIT CRITERIA FOR UAT**

✅ All UAT scenarios executed ✅ UAT pass rate ≥90% ✅ No critical defects open ✅ Business users satisfied ✅ UAT sign-off received ✅ All critical business processes validated ✅ UAT report submitted

**Example:**

UAT Phase \- Exit Criteria:  
☐ UAT scenarios: 50/50 executed (100%)  
☐ Pass rate: 46/50 passed (92%)  
☐ Critical defects: 0  
☐ High defects: 1 (deferred to next release)  
☐ User satisfaction: Positive feedback received  
☐ Sign-off: Received from business sponsor  
☐ Critical processes: All validated  
☐ UAT report: Submitted to stakeholders

---

### **SUSPENSION CRITERIA**

**Definition**: Conditions under which testing should be suspended (stopped temporarily).

**Common Suspension Criteria:**

❌ Build is unstable (crashes frequently) ❌ Critical defects blocking testing ❌ Test environment unavailable ❌ Major functionality not working ❌ More than 50% test cases blocked ❌ Key resources unavailable ❌ Major changes in requirements ❌ Security breach in test environment

**Example:**

Testing should be SUSPENDED if:  
☐ Application crashes more than 10 times per day  
☐ Any P0 defect is found  
☐ Test environment down for \>4 hours  
☐ Login functionality completely broken  
☐ More than 75 test cases blocked  
☐ Test Lead unavailable and no backup  
☐ Requirements change affecting \>30% features

---

### **RESUMPTION CRITERIA**

**Definition**: Conditions that must be met before testing can resume after suspension.

**Common Resumption Criteria:**

✅ Critical defects fixed and verified ✅ Stable build deployed ✅ Test environment restored and stable ✅ Blocked test cases unblocked ✅ Requirements clarified ✅ Resources available ✅ Test Lead approval to resume

**Example:**

Testing can RESUME when:  
☐ P0 defect fixed and verified  
☐ New stable build deployed (v2.5.3)  
☐ Environment stable for 24 hours  
☐ Previously blocked test cases now executable  
☐ Requirements meeting held and clarifications received  
☐ Backup Test Lead assigned  
☐ Test Manager approves resumption

---

### **PRACTICAL EXAMPLES:**

**Example 1: E-commerce Shopping Cart Testing**

**Entry Criteria:**

Before starting Shopping Cart testing:  
1\. ✓ Product Catalog module working (dependency)  
2\. ✓ User Login module working (dependency)  
3\. ✓ Test cases: 75 test cases reviewed  
4\. ✓ Test data: 50 products loaded  
5\. ✓ Test users: 20 user accounts created  
6\. ✓ Build v2.5 deployed to QA  
7\. ✓ Smoke test passed (15/15)

**Exit Criteria:**

Shopping Cart testing complete when:  
1\. ✓ All 75 test cases executed  
2\. ✓ Pass rate: 70/75 \= 93.3%  
3\. ✓ Critical defects: 0 open  
4\. ✓ High defects: 0 open  
5\. ✓ Medium defects: 3 (accepted by business)  
6\. ✓ Add to cart functionality: 100% working  
7\. ✓ Checkout flow: End-to-end successful

---

**Example 2: Mobile App Payment Testing**

**Entry Criteria:**

1\. ✓ Payment gateway sandbox environment ready  
2\. ✓ Test payment cards received from vendor  
3\. ✓ Payment test cases: 40 test cases approved  
4\. ✓ SSL certificates installed  
5\. ✓ Network security clearance obtained  
6\. ✓ Payment module deployed (v3.1)  
7\. ✓ Integration with payment API verified

**Exit Criteria:**

1\. ✓ All payment methods tested (Card, UPI, Wallet)  
2\. ✓ Transaction success rate: 95%  
3\. ✓ Payment security tests passed  
4\. ✓ Error handling tested and working  
5\. ✓ No P0/P1 defects  
6\. ✓ Payment audit log verified  
7\. ✓ Refund testing completed

---

### **ENTRY/EXIT CRITERIA CHECKLIST TEMPLATE:**

PROJECT: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
PHASE: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
DATE: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

ENTRY CRITERIA CHECKLIST:  
☐ Criterion 1: \[Description\]  
   Status: Met / Not Met  
   Comments: \_\_\_\_\_\_\_\_\_\_\_

☐ Criterion 2: \[Description\]  
   Status: Met / Not Met  
   Comments: \_\_\_\_\_\_\_\_\_\_\_

☐ Criterion 3: \[Description\]  
   Status: Met / Not Met  
   Comments: \_\_\_\_\_\_\_\_\_\_\_

OVERALL ENTRY STATUS: Ready / Not Ready

SIGN-OFF:  
Test Lead: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_  
Project Manager: \_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_

\---

EXIT CRITERIA CHECKLIST:  
☐ Criterion 1: \[Description\]  
   Status: Met / Not Met  
   Evidence: \_\_\_\_\_\_\_\_\_\_\_

☐ Criterion 2: \[Description\]  
   Status: Met / Not Met  
   Evidence: \_\_\_\_\_\_\_\_\_\_\_

☐ Criterion 3: \[Description\]  
   Status: Met / Not Met  
   Evidence: \_\_\_\_\_\_\_\_\_\_\_

OVERALL EXIT STATUS: Complete / Incomplete

SIGN-OFF:  
Test Lead: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_  
Project Manager: \_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_

---

### **BEST PRACTICES:**

**For Entry Criteria:**

✅ **DO:**

* Make them specific and measurable  
* Get stakeholder agreement  
* Document clearly  
* Check before starting  
* Have sign-off process  
* Be realistic

❌ **DON'T:**

* Make them too strict (no one can start)  
* Be vague ("requirements should be good")  
* Skip checking them  
* Start without meeting them  
* Change them without approval

**For Exit Criteria:**

✅ **DO:**

* Align with business goals  
* Make them measurable (percentages, numbers)  
* Include quality gates  
* Get stakeholder buy-in  
* Document evidence  
* Be consistent

❌ **DON'T:**

* Set unrealistic goals (100% pass rate)  
* Be subjective ("good enough")  
* Ignore them to meet deadlines  
* Change at the last minute  
* Accept without evidence

---

### **COMMON MISTAKES:**

**Mistake 1: Too Many Criteria** ❌ Bad: 30 entry criteria (impossible to meet all) ✅ Good: 8-10 critical entry criteria

**Mistake 2: Vague Criteria** ❌ Bad: "Environment should be stable" ✅ Good: "Environment stable with no crashes for 48 hours"

**Mistake 3: No Measurements** ❌ Bad: "Most test cases passed" ✅ Good: "95% of test cases passed (142/150)"

**Mistake 4: Ignoring Criteria** ❌ Bad: Start testing even when criteria not met ✅ Good: Wait until all criteria met, or get waiver

**Mistake 5: No Documentation** ❌ Bad: Verbal agreement only ✅ Good: Written checklist with sign-offs

---

### **✍️ PRACTICAL TASK (3 hours)**

**Task 23.1: Create Entry/Exit Criteria**

For "Online Banking \- Fund Transfer Feature", define:

**Entry Criteria for Test Execution** (at least 8):

1. ---

2. ---

...

**Exit Criteria for Test Execution** (at least 8):

1. ---

2. ---

...

**Suspension Criteria** (at least 5):

1. ---

2. ---

...

**Resumption Criteria** (at least 5):

1. ---

2. ---

...

**Task 23.2: Evaluate Criteria**

You're given these entry criteria for test execution:

1\. Build deployed  
2\. Some test cases ready  
3\. Environment is good  
4\. Team is ready  
5\. Requirements are okay

Problems with these criteria:

* Identify what's wrong with each  
* Rewrite them properly  
* Make them specific and measurable

**Task 23.3: Checklist Creation**

Create a complete entry/exit criteria checklist for:

**Project**: Healthcare Patient Management System **Module**: Appointment Scheduling **Phase**: System Testing

Include:

* 10 entry criteria with status checkboxes  
* 10 exit criteria with status checkboxes  
* Sign-off section  
* Date and version

**Task 23.4: Decision Making**

**Scenario:** You're a Test Lead. Test execution is scheduled to start tomorrow.

**Current Status:**

* Build deployed: ✓  
* Test cases ready: ✓ (140/150, 10 still being reviewed)  
* Test environment: ✓  
* Test data: ✓  
* Smoke test: ✗ (failed 3/20 test cases)  
* Team trained: ✓

**Entry Criteria Required:**

* All test cases ready and reviewed  
* Smoke test 100% passed

**Question:** Should you start test execution tomorrow?

* Your decision: Yes / No / Partial  
* Justification: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
* What needs to be done: \_\_\_\_\_\_\_\_\_\_  
* Communication to stakeholders: \_\_\_

**Task 23.5: Real Project Analysis**

Choose any completed project (yours or research online):

* Identify what entry criteria were likely used  
* Identify what exit criteria were likely used  
* Find gaps (what should have been included)  
* Document lessons learned

**Task 23.6: Metrics Exercise**

Convert these vague exit criteria into measurable ones:

1. "Most test cases should pass" → Measurable: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

2. "Not too many defects" → Measurable: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

3. "Good test coverage" → Measurable: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

4. "Environment stable enough" → Measurable: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

5. "Users satisfied" → Measurable: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### **📝 ASSIGNMENT (3 hours)**

**1\. Complete Criteria Document:**

Create a comprehensive Entry/Exit Criteria document for:

**Project**: Social Media Platform **Module**: Post Creation & Sharing **Testing Phases**: Unit, Integration, System, UAT

For EACH phase, define:

* Entry Criteria (minimum 6\)  
* Exit Criteria (minimum 6\)  
* Suspension Criteria (minimum 4\)  
* Resumption Criteria (minimum 4\)

Format professionally with:

* Checklist format  
* Specific and measurable criteria  
* Sign-off sections  
* Version control

**2\. Case Study Analysis:**

**Scenario:** A team started test execution without meeting entry criteria:

* Only 70% test cases ready  
* Test environment unstable (crashes daily)  
* No smoke test performed  
* Test data incomplete

**Results:**

* 50% of testing time wasted  
* Many blocked test cases  
* Environment issues caused delays  
* Project delayed by 2 weeks

Write:

* Root cause analysis (why this happened)  
* Impact assessment  
* What should have been done  
* Lessons learned  
* Prevention measures for future

(2-3 pages)

**3\. Template Creation:**

Create reusable templates:

**Template 1:** Entry Criteria Checklist **Template 2:** Exit Criteria Checklist **Template 3:** Entry/Exit Criteria Sign-off Form **Template 4:** Suspension/Resumption Request Form

Make them professional and reusable for any project.

**4\. Best Practices Guide:**

Write a guide document:

**Title**: "Entry & Exit Criteria \- Complete Guide"

Include:

* What they are and why important  
* How to define them  
* How to make them measurable  
* Examples (good vs bad)  
* Different phases criteria  
* Common mistakes  
* Best practices  
* Templates  
* Real-world examples

(5-6 pages)

### **📚 RESOURCES**

* Article: "Entry and Exit Criteria in Testing" \- Guru99  
* Video: "How to Define Entry/Exit Criteria"  
* Template: Entry/Exit Criteria Checklist Template  
* Read: IEEE standards for entry/exit criteria

---

## **📅 DAY 24: Risk-Based Testing Approach**

### **📖 THEORY NOTES**

**What is Risk-Based Testing?**

Risk-Based Testing (RBT) is an approach where testing efforts are prioritized based on the risk of failure and its potential impact on the business.

**Key Principle:** "Test what matters most first"

**Why Risk-Based Testing?**

1. **Limited Time**: Never enough time to test everything  
2. **Limited Resources**: Limited team, budget, tools  
3. **Maximize ROI**: Get maximum value from testing efforts  
4. **Focus on Critical Areas**: Test high-risk areas thoroughly  
5. **Business Alignment**: Testing aligned with business priorities

**Quote:**

"If you don't have time to test everything, test what's most important." \- James Bach

---

### **UNDERSTANDING RISK:**

**Risk** \= Probability × Impact

**Risk**: The possibility of a negative outcome

**Components:**

1. **Probability/Likelihood**: How likely is the failure to occur?

   * High, Medium, Low  
   * Percentage (e.g., 80% chance)  
2. **Impact/Severity**: What's the consequence if it fails?

   * High, Medium, Low  
   * Business impact, financial loss, reputation damage

---

### **RISK CATEGORIES:**

**1\. TECHNICAL RISKS:**

* Complex algorithms  
* New technology used  
* Integration with third-party systems  
* Performance requirements  
* Security vulnerabilities  
* Data migration issues

**2\. BUSINESS RISKS:**

* Revenue-generating features  
* Customer-facing features  
* Compliance/regulatory requirements  
* Brand reputation  
* Market competition  
* Customer satisfaction

**3\. PROJECT RISKS:**

* Tight deadlines  
* Resource constraints  
* Unclear requirements  
* Dependencies on other teams  
* Frequent changes  
* Inexperienced team

---

### **RISK ANALYSIS PROCESS:**

**Step 1: IDENTIFY RISKS**

Methods to identify risks:

* Brainstorming sessions with team  
* Historical data analysis (past projects)  
* Requirement reviews  
* Architecture reviews  
* Stakeholder interviews  
* Industry experience  
* Competitor analysis

**Example Risks for E-commerce:**

* Payment gateway failure  
* Inventory sync issues  
* Cart abandonment  
* Slow page load times  
* Security breaches  
* Product search not working  
* Order processing errors

---

**Step 2: ASSESS RISKS**

For each risk, assess:

**Probability (Likelihood):**

* **High (H)**: Very likely to occur (\>70% chance)  
* **Medium (M)**: Moderate chance (30-70%)  
* **Low (L)**: Unlikely (\<30%)

**Impact (Severity):**

* **High (H)**: Severe impact on business  
* **Medium (M)**: Moderate impact  
* **Low (L)**: Minor impact

---

**Step 3: CALCULATE RISK LEVEL**

| Probability | Impact | Risk Level |
| ----- | ----- | ----- |
| High | High | **CRITICAL** |
| High | Medium | **HIGH** |
| High | Low | MEDIUM |
| Medium | High | **HIGH** |
| Medium | Medium | MEDIUM |
| Medium | Low | LOW |
| Low | High | MEDIUM |
| Low | Medium | LOW |
| Low | Low | **VERY LOW** |

---

**Step 4: PRIORITIZE TESTING**

**Priority Order:**

1. **CRITICAL** risks → Test first, most thoroughly  
2. **HIGH** risks → Test early, thoroughly  
3. **MEDIUM** risks → Test after high risks  
4. **LOW** risks → Test if time permits  
5. **VERY LOW** risks → May skip or minimal testing

---

### **RISK ASSESSMENT MATRIX:**

                   IMPACT  
                Low    Medium   High  
           ┌────────┬─────────┬─────────┐  
      High │ MEDIUM │  HIGH   │CRITICAL │  
PROB.      ├────────┼─────────┼─────────┤  
    Medium │  LOW   │ MEDIUM  │  HIGH   │  
           ├────────┼─────────┼─────────┤  
      Low  │VERY LOW│  LOW    │ MEDIUM  │  
           └────────┴─────────┴─────────┘

---

### **EXAMPLE: E-COMMERCE APPLICATION**

**Risk Analysis Table:**

| Feature | Probability | Impact | Risk Level | Testing Priority |
| ----- | ----- | ----- | ----- | ----- |
| Payment Processing | High | High | CRITICAL | 1 \- Test First |
| Checkout Flow | High | High | CRITICAL | 1 \- Test First |
| Product Search | Medium | High | HIGH | 2 \- Test Early |
| User Login | Medium | High | HIGH | 2 \- Test Early |
| Shopping Cart | High | Medium | HIGH | 2 \- Test Early |
| Order History | Medium | Medium | MEDIUM | 3 \- Test After High |
| Product Reviews | Low | Medium | LOW | 4 \- Test If Time |
| Wishlist | Low | Low | VERY LOW | 5 \- May Skip |

**Rationale:**

* **Payment Processing**: High probability (complex integration) \+ High impact (revenue loss) \= CRITICAL  
* **Product Search**: Medium probability \+ High impact (users can't find products) \= HIGH  
* **Wishlist**: Low probability (simple feature) \+ Low impact (nice-to-have) \= VERY LOW

---

### **RISK-BASED TEST STRATEGY:**

**For CRITICAL Risks:**

* Allocate maximum testing time (30-40% of effort)  
* Multiple test approaches (functional, security, performance)  
* Detailed test cases  
* Experienced testers assigned  
* Exploratory testing included  
* Automation priority  
* Thorough regression testing

**For HIGH Risks:**

* Allocate significant time (25-30% of effort)  
* Comprehensive test cases  
* Senior testers assigned  
* Good test coverage  
* Include in regression suite

**For MEDIUM Risks:**

* Allocate moderate time (20-25% of effort)  
* Standard test cases  
* Mid-level testers assigned  
* Adequate coverage  
* Selective regression

**For LOW Risks:**

* Allocate minimal time (10-15% of effort)  
* Basic test cases  
* Junior testers assigned  
* Smoke/Sanity testing  
* Optional regression

**For VERY LOW Risks:**

* Allocate minimal time or skip (0-5% of effort)  
* Ad-hoc testing only  
* May skip if time constrained  
* No regression (unless bugs found)

---

### **FACTORS INFLUENCING RISK:**

**1\. Complexity:**

* More complex \= Higher risk  
* Example: Payment integration vs. Static content display

**2\. Frequency of Use:**

* More used \= Higher impact if fails  
* Example: Login (daily use) vs. Delete Account (rare)

**3\. Visibility:**

* Customer-facing \= Higher impact  
* Example: Product page vs. Admin logs

**4\. Change Frequency:**

* Frequently changed \= Higher probability of defects  
* Example: New feature vs. Unchanged for 2 years

**5\. Technology Maturity:**

* New/untested technology \= Higher risk  
* Example: New AI feature vs. Standard CRUD

**6\. Dependencies:**

* More dependencies \= Higher risk  
* Example: Feature depending on 5 systems vs. Standalone

**7\. Historical Defects:**

* More past bugs \= Higher probability  
* Example: Module with 50 bugs vs. Module with 2 bugs

---

### **RISK MITIGATION STRATEGIES:**

**1\. Intensive Testing:**

* More test cases  
* Different testing types  
* Multiple testers

**2\. Early Testing:**

* Test high-risk areas first  
* Shift-left approach  
* Test during development

**3\. Expert Assignment:**

* Senior testers for high-risk  
* Domain experts involved  
* Pair testing

**4\. Multiple Techniques:**

* Functional \+ Security \+ Performance  
* Exploratory testing  
* Monkey testing

**5\. Automation:**

* Automate high-risk regression tests  
* Frequent execution  
* Quick feedback

**6\. Monitoring:**

* Close monitoring in production  
* Analytics and logging  
* Quick rollback plan

**7\. Contingency Planning:**

* Backup plans  
* Rollback procedures  
* Communication plans

---

### **PRACTICAL EXAMPLE:**

**Project**: Banking Application \- Fund Transfer Module

**Risk Identification & Assessment:**

**1\. Risk: Incorrect Amount Transfer**

* Probability: Medium (calculation logic is complex)  
* Impact: High (financial loss, legal issues)  
* Risk Level: HIGH  
* Testing Strategy:  
  * 50 test cases covering all scenarios  
  * Boundary value analysis  
  * Decision table testing  
  * Senior tester assigned  
  * Automated regression tests

**2\. Risk: Transaction Timeout**

* Probability: High (network dependencies)  
* Impact: High (frustrated users, lost transactions)  
* Risk Level: CRITICAL  
* Testing Strategy:  
  * Network simulation testing  
  * Timeout scenarios  
  * Recovery testing  
  * Performance testing  
  * 24/7 monitoring plan

**3\. Risk: Transaction History Display Error**

* Probability: Low (simple display logic)  
* Impact: Low (non-critical feature)  
* Risk Level: VERY LOW  
* Testing Strategy:  
  * 10 basic test cases  
  * Junior tester assigned  
  * Smoke testing only

---

### **RISK-BASED TEST PLAN SECTION:**

RISK ANALYSIS AND MITIGATION

High-Risk Features:  
1\. Payment Processing (P=High, I=High, Risk=CRITICAL)  
   \- Testing Effort: 35% of total time  
   \- Test Cases: 80 detailed test cases  
   \- Testers: 2 senior QA engineers  
   \- Additional Testing: Security, Performance, Error handling  
   \- Automation: High priority

2\. User Authentication (P=Medium, I=High, Risk=HIGH)  
   \- Testing Effort: 25% of total time  
   \- Test Cases: 50 test cases  
   \- Testers: 1 senior QA engineer  
   \- Additional Testing: Security, Session management  
   \- Automation: Medium priority

Medium-Risk Features:  
3\. Product Catalog (P=Medium, I=Medium, Risk=MEDIUM)  
   \- Testing Effort: 20% of total time  
   \- Test Cases: 40 test cases  
   \- Testers: 2 mid-level QA engineers

Low-Risk Features:  
4\. User Profile (P=Low, I=Medium, Risk=LOW)  
   \- Testing Effort: 10% of total time  
   \- Test Cases: 20 test cases  
   \- Testers: 1 junior QA engineer

5\. Help/FAQ Section (P=Low, I=Low, Risk=VERY LOW)  
   \- Testing Effort: 5% of total time  
   \- Test Cases: 10 basic test cases  
   \- Testers: 1 junior QA engineer

Total Testing Effort Allocation:  
\- Critical/High Risk: 60%  
\- Medium Risk: 20%  
\- Low/Very Low Risk: 20%

---

### **BENEFITS OF RISK-BASED TESTING:**

✅ **Optimized Resources**: Focus where it matters ✅ **Better ROI**: Maximum value from testing ✅ **Stakeholder Confidence**: Testing aligned with business ✅ **Early Defect Detection**: High-risk areas tested first ✅ **Informed Decisions**: Clear prioritization rationale ✅ **Flexibility**: Adapt to time/resource constraints ✅ **Clear Communication**: Everyone understands priorities

---

### **CHALLENGES:**

❌ **Subjective Assessment**: Risk assessment can be subjective ❌ **Requires Experience**: Needs experienced team for assessment ❌ **Time for Analysis**: Initial risk analysis takes time ❌ **Changing Risks**: Risks may change during project ❌ **Stakeholder Disagreement**: Different views on risk levels ❌ **Documentation Overhead**: Needs proper documentation

---

### **✍️ PRACTICAL TASK (4 hours)**

**Task 24.1: Risk Identification**

For "Healthcare Patient Management System", identify:

* 10 technical risks  
* 10 business risks  
* 5 project risks

**Task 24.2: Risk Assessment**

For each risk from Task 24.1:

* Assess Probability (H/M/L)  
* Assess Impact (H/M/L)  
* Calculate Risk Level  
* Justify your assessment

Create table:

| Risk | Probability | Impact | Risk Level | Justification |
| ----- | ----- | ----- | ----- | ----- |
|  |  |  |  |  |

**Task 24.3: Test Prioritization**

Given these features for an e-learning platform:

1. Video Streaming  
2. User Registration  
3. Course Purchase & Payment  
4. Progress Tracking  
5. Certificate Download  
6. Discussion Forum  
7. User Profile  
8. Course Search  
9. Instructor Dashboard  
10. Student Feedback

Assess each feature:

* Assign Probability (H/M/L)  
* Assign Impact (H/M/L)  
* Calculate Risk Level  
* Prioritize testing order (1-10)  
* Allocate testing effort %

**Task 24.4: Testing Strategy**

For the TOP 3 high-risk features from Task 24.3:

For each feature, define:

* Number of test cases  
* Testing types to be performed  
* Team member level (Senior/Mid/Junior)  
* Additional testing needed  
* Automation priority  
* Monitoring plan

**Task 24.5: Risk Mitigation**

For these identified risks, define mitigation strategies:

**Risk 1:** Third-party payment gateway may fail during peak hours

* Mitigation: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Risk 2:** New machine learning algorithm may produce inaccurate results

* Mitigation: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Risk 3:** Database may not handle 10,000 concurrent users

* Mitigation: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Task 24.6: Real Application Analysis**

Choose your favorite app (Netflix/Amazon/Uber):

* Identify 5 features  
* Assess risk for each  
* Prioritize testing  
* Justify your assessment

### **📝 ASSIGNMENT (3 hours)**

**1\. Complete Risk Analysis Document:**

Create a comprehensive Risk-Based Testing document for:

**Project**: Online Food Delivery Application

Include:

* Risk identification (20 risks minimum)  
* Risk assessment matrix  
* Risk levels with justification  
* Test prioritization  
* Testing strategy for each risk level  
* Effort allocation  
* Mitigation strategies  
* Monitoring plan

(6-8 pages)

**2\. Case Study:**

**Scenario:** A team tested all features equally (20% effort each for 5 features) without risk analysis.

**Results:**

* Low-risk "Help Section" thoroughly tested (found 2 minor bugs)  
* High-risk "Payment Module" insufficiently tested (missed critical bug in production causing $50,000 loss)

Write:

* What went wrong?  
* How would risk-based testing have helped?  
* Calculate optimal effort distribution using RBT  
* Lessons learned  
* Recommendations

(3-4 pages)

**3\. Risk Assessment Template:**

Create reusable templates:

* Risk Identification Worksheet  
* Risk Assessment Matrix  
* Risk-Based Test Strategy Template

# **PHASE 2: CORE TESTING SKILLS \- COMPLETION**

## **(Days 24-45 \- Remaining Content)**

---

## **📅 DAY 25: Creating Your First Test Plan Document**

### **📖 THEORY NOTES**

**Recap: What You've Learned About Test Plans**

* Day 21: Structure & Components  
* Day 22: Strategy vs Plan  
* Day 23: Entry & Exit Criteria  
* Day 24: Risk-Based Testing  
* **Today: Put it all together\!**

**Step-by-Step Process to Create Test Plan:**

**STEP 1: Gather Information** Before writing, collect:

* ✅ Project requirements document  
* ✅ Stakeholder expectations  
* ✅ Resource availability  
* ✅ Timeline constraints  
* ✅ Budget information  
* ✅ Risk inputs from team  
* ✅ Previous project lessons learned

**STEP 2: Choose Template**

* Use IEEE 829 for traditional projects  
* Use simplified template for Agile  
* Customize based on organization needs

**STEP 3: Fill Sections Systematically**

**Section-by-Section Guide:**

**1\. HEADER INFORMATION**

Document Title: TEST PLAN \- \[Project Name\]

Version: 1.0

Date: \[Creation Date\]

Author: \[Your Name\]

Status: Draft / Under Review / Approved

**2\. INTRODUCTION (Who, What, Why)** Write 2-3 paragraphs covering:

* What project/module is being tested  
* Purpose of this test plan  
* Who is the audience

**Example:**

This test plan outlines the testing approach for the XYZ E-commerce 

Shopping Cart module version 3.0. The purpose is to ensure all 

functionalities meet the specified requirements and quality standards 

before the production release scheduled for March 2025\.

This document is intended for the QA team, development team, project 

managers, and stakeholders involved in the project.

**3\. SCOPE \- Be Specific**

**In Scope \- List exactly what WILL be tested:**

Features to be Tested:

✓ Add product to cart (single & multiple items)

✓ Remove product from cart

✓ Update product quantity (1-99 items)

✓ Apply discount coupons (percentage & fixed amount)

✓ Calculate totals (subtotal, tax, discount, grand total)

✓ Save cart for later

✓ Clear entire cart

✓ Guest user checkout flow

✓ Registered user checkout flow

✓ Cart persistence (across sessions)

**Out of Scope \- Be clear about exclusions:**

Features NOT to be Tested:

✗ Payment gateway processing (separate test plan)

✗ Product catalog management (already tested)

✗ User registration/login (separate module)

✗ Order fulfillment process (future release)

✗ Mobile app version (separate test plan)

Reasons for Exclusion:

\- Separate ownership/teams

\- Already tested in previous cycle

\- Third-party managed components

\- Not in current release scope

**4\. TEST APPROACH \- Explain HOW**

**Template to follow:**

Testing Methodology: \[Agile/Waterfall/Hybrid\]

Testing Types to be Performed:

1\. Functional Testing

   \- Verify all features work as per requirements

   \- Test all user workflows end-to-end

   

2\. Regression Testing

   \- Ensure existing features still work

   \- Execute after each bug fix

   

3\. Exploratory Testing

   \- Unscripted testing to find edge cases

   \- 20% of testing time allocated

4\. Cross-browser Testing

   \- Chrome (latest version)

   \- Firefox (latest version)

   \- Safari (latest version)

   \- Edge (latest version)

Test Design Techniques:

\- Equivalence Partitioning for input fields

\- Boundary Value Analysis for quantity, amounts

\- Decision Tables for discount calculations

\- State Transition for cart states

\- Error Guessing for negative scenarios

Test Levels:

\- Integration Testing: Cart \+ Product Catalog

\- System Testing: Complete checkout flow

\- UAT: Business users validate

**5\. PASS/FAIL CRITERIA \- Use Numbers**

**Good Criteria (Measurable):**

PASS CRITERIA:

✓ 100% of P0 (Critical) test cases executed and passed

✓ ≥95% of P1 (High) test cases passed

✓ ≥90% of P2 (Medium) test cases passed

✓ Zero open Critical (S1) defects

✓ Zero open High (S2) defects

✓ ≤3 open Medium (S3) defects (with business acceptance)

✓ All planned test scenarios executed

✓ 95% requirements coverage achieved

✓ Performance: Page load time \<3 seconds

✓ UAT sign-off received

FAIL CRITERIA:

✗ Any P0 test case failure

✗ \<90% overall test case pass rate

✗ Any Critical/High severity defect open

✗ Key functionality (add to cart, checkout) not working

✗ Test environment unstable for \>4 hours

✗ \>20% test cases blocked

**6\. TEST DELIVERABLES \- Complete List**

BEFORE TESTING STARTS:

□ Test Plan document (this document)

□ Test scenarios document

□ Test cases (detailed)

□ Requirements Traceability Matrix (RTM)

□ Test data preparation sheet

□ Test environment setup checklist

DURING TESTING:

□ Daily test execution status report

□ Defect reports (logged in JIRA)

□ Test logs

□ Weekly status report to stakeholders

□ Blocked test cases report

□ Risk updates

AFTER TESTING:

□ Test summary report

□ Test metrics dashboard

□ Defect metrics and analysis

□ Test coverage report

□ Lessons learned document

□ Test closure report

□ Sign-off document

**7\. TEST ENVIRONMENT \- Exact Specifications**

HARDWARE:

\- Server: AWS EC2 (t3.large instance, 8GB RAM, 100GB storage)

\- Client: Windows 10/11, macOS 12+

\- Minimum: 8GB RAM, 256GB storage

\- Internet: Minimum 10 Mbps

SOFTWARE:

\- Operating System: Windows Server 2019

\- Database: PostgreSQL 14.2

\- Web Server: Apache 2.4

\- Application Server: Node.js 18.x

\- Browsers: 

  \* Chrome 120+ (primary)

  \* Firefox 119+

  \* Safari 17+

  \* Edge 120+

TEST TOOLS:

\- Test Management: TestRail v7.5

\- Bug Tracking: JIRA v9.4

\- API Testing: Postman v10.x

\- Screenshot Tool: Snagit

\- Screen Recording: Loom

TEST DATA:

\- User accounts: 100 (test\_user\_001 to test\_user\_100)

\- Products: 500 items across 20 categories

\- Discount coupons: 50 valid, 20 expired

\- Payment cards: Test cards from payment gateway provider

NETWORK:

\- VPN access required for remote testers

\- Network speed: 100 Mbps

\- Firewall rules: Port 443, 80, 8080 open

ENVIRONMENT URL:

\- QA Environment: https://qa.myecommerce.com

\- Admin Panel: https://qa.myecommerce.com/admin

\- Database: qa-db.myecommerce.com:5432

ENVIRONMENT AVAILABILITY:

\- 24/7 available during testing phase

\- Maintenance window: Saturday 2 AM \- 4 AM

\- Backup environment: https://qa2.myecommerce.com

**8\. SCHEDULE \- Realistic Timeline**

PHASE                   START DATE    END DATE     DURATION   OWNER

─────────────────────────────────────────────────────────────────────

Test Planning           Jan 15       Jan 19       5 days     Test Lead

Test Case Development   Jan 20       Jan 31       12 days    QA Team

Test Case Review        Feb 01       Feb 02       2 days     Test Lead

Environment Setup       Jan 27       Jan 30       4 days     DevOps \+ QA

Test Data Preparation   Jan 30       Feb 01       2 days     QA Team

Smoke Testing           Feb 03       Feb 03       1 day      Sr. QA

Test Execution Cycle 1  Feb 04       Feb 15       12 days    QA Team

Bug Fixing              Feb 16       Feb 18       3 days     Dev Team

Regression Testing      Feb 19       Feb 22       4 days     QA Team

Test Execution Cycle 2  Feb 23       Feb 26       4 days     QA Team

UAT                     Feb 27       Mar 05       7 days     Business

Test Closure            Mar 06       Mar 07       2 days     Test Lead

─────────────────────────────────────────────────────────────────────

TOTAL DURATION: 52 days (7.5 weeks)

MILESTONES:

✓ Test Plan Approval: Jan 19

✓ Test Cases Ready: Jan 31

✓ Environment Ready: Jan 30

✓ Smoke Test Pass: Feb 03

✓ Cycle 1 Complete: Feb 15

✓ Regression Complete: Feb 22

✓ UAT Sign-off: Mar 05

✓ Go-Live: Mar 10

**9\. TEAM & RESPONSIBILITIES**

ROLE              NAME            RESPONSIBILITY                      ALLOCATION

──────────────────────────────────────────────────────────────────────────────

Test Manager      Sarah Williams  \- Overall test strategy              20%

                                  \- Resource management

                                  \- Stakeholder communication

                                  \- Risk management

Test Lead         John Doe        \- Test plan creation                 100%

                                  \- Test case review

                                  \- Daily execution monitoring

                                  \- Defect triage meetings

                                  \- Status reporting

Senior QA         Jane Smith      \- Complex scenario testing           100%

                                  \- Payment flow testing

                                  \- Mentoring juniors

                                  \- Automation support

QA Engineer       Mike Johnson    \- Test case execution                100%

                                  \- Defect logging

                                  \- Regression testing

                                  \- Browser compatibility testing

QA Engineer       Tom Brown       \- Test case execution                100%

                                  \- Exploratory testing

                                  \- Test data creation

                                  \- Documentation

Junior QA         Lisa Anderson   \- Test execution support             100%

                                  \- Basic test case execution

                                  \- Defect verification

                                  \- Learning/training

Developer         Dev Team        \- Unit testing                       20%

                                  \- Bug fixing

                                  \- Environment support

                                  \- Build deployment

Business Analyst  Emily Davis     \- Requirement clarification          10%

                                  \- UAT coordination

                                  \- Test case validation

DevOps Engineer   Robert Lee      \- Environment setup                  30%

                                  \- Build deployment

                                  \- Infrastructure support

                                  \- Monitoring setup

TOTAL TEAM SIZE: 9 members

FULL-TIME QA: 5 members

PART-TIME SUPPORT: 4 members

**10\. ENTRY & EXIT CRITERIA**

ENTRY CRITERIA FOR TEST EXECUTION:

☐ Test plan approved by Test Manager and PM

☐ Test cases: 100% written, reviewed, and approved (minimum 120 test cases)

☐ Test environment stable and accessible (https://qa.myecommerce.com)

☐ Test data loaded successfully (100 users, 500 products)

☐ Build deployed to QA: Version 3.0.1 or higher

☐ Smoke test: 100% passed (minimum 20 smoke test cases)

☐ All testers have access (JIRA, TestRail, QA environment)

☐ Defect tracking configured in JIRA

☐ No open P0 defects from previous release

☐ Test team trained on new features

☐ Entry criteria checklist signed off

EXIT CRITERIA FOR TEST EXECUTION:

☐ Test case execution: ≥95% completed (114/120 minimum)

☐ Test pass rate: ≥90% (108/120 minimum passed)

☐ Critical defects: 0 open

☐ High defects: 0 open

☐ Medium defects: ≤3 open (with business acceptance)

☐ All P0 test cases: 100% passed

☐ All P1 test cases: ≥95% passed

☐ Regression testing: Complete (100 test cases executed, ≥95% passed)

☐ Requirements traceability: 100% requirements traced and tested

☐ UAT: Completed with business sign-off

☐ Test summary report: Completed and reviewed

☐ Go/No-Go decision: Made by steering committee

☐ Exit criteria checklist signed off

SUSPENSION CRITERIA (Stop Testing):

☐ Application crashes \>10 times per day

☐ Any P0 (Critical) defect found

☐ Test environment down for \>4 hours

☐ Login/Authentication completely broken

☐ \>50% of test cases blocked

☐ Major requirement changes affecting \>30% scope

☐ Build instability (repeated failures)

RESUMPTION CRITERIA (Resume Testing):

☐ Critical defect fixed and verified

☐ Stable build deployed (crash-free for 24 hours)

☐ Test environment restored and stable

☐ Blocked test cases unblocked

☐ Requirements clarified and documented

☐ Test Manager/Test Lead approval to resume

**11\. RISKS & MITIGATION**

RISK ASSESSMENT MATRIX:

RISK                          PROBABILITY  IMPACT  RISK LEVEL  MITIGATION STRATEGY

─────────────────────────────────────────────────────────────────────────────────

Third-party payment API       High         High    CRITICAL    \- Use mock payment service

unstable/unavailable                                           \- Early integration testing

                                                               \- Backup test environment

                                                               \- Daily API health checks

Resource unavailability       Medium       High    HIGH        \- Cross-train team members

(team members on leave)                                        \- Identify backup resources

                                                               \- Maintain knowledge docs

                                                               \- Buffer in schedule

Requirement changes           Medium       High    HIGH        \- Freeze requirements early

mid-testing                                                    \- Change control process

                                                               \- Impact analysis for changes

                                                               \- Re-prioritize testing

Test environment              High         Medium  HIGH        \- Backup environment ready

instability                                                    \- Daily environment checks

                                                               \- DevOps on-call support

                                                               \- Auto-recovery scripts

Tight timeline/schedule       High         Medium  HIGH        \- Risk-based testing

pressure                                                       \- Prioritize critical features

                                                               \- Daily progress tracking

                                                               \- Early escalation

Insufficient test data        Medium       Medium  MEDIUM      \- Automated data generation

                                                               \- Production data copy (masked)

                                                               \- Test data creation scripts

Browser compatibility         Low          High    MEDIUM      \- BrowserStack subscription

issues                                                         \- Parallel browser testing

                                                               \- Early browser testing

Team inexperience with        Medium       Low     LOW         \- Training sessions

new features                                                   \- Pair testing approach

                                                               \- Senior QA mentoring

                                                               \- Documentation review

RISK MONITORING:

\- Weekly risk review meeting

\- Risk register maintained in Confluence

\- Risk escalation to Test Manager/PM

\- Mitigation effectiveness tracking

**12\. ASSUMPTIONS & DEPENDENCIES**

ASSUMPTIONS:

✓ Requirements will be stable after Jan 15

✓ Test team will be available full-time for testing period

✓ Development will be complete by Feb 02

✓ Test environment will be available 24/7

✓ Testers have basic e-commerce domain knowledge

✓ JIRA and TestRail licenses available

✓ Internet connectivity stable (minimum 10 Mbps)

✓ No major production issues requiring team support

DEPENDENCIES:

→ Product Catalog module must be stable and tested

→ User Authentication module must be functional

→ Payment gateway sandbox/test environment must be ready

→ DevOps team to set up test environment by Jan 30

→ Business Analyst to clarify requirements by Jan 18

→ Developers to complete development by Feb 02

→ Third-party API documentation must be available

→ Test data scripts must be ready by Jan 31

→ UAT users must be identified and available Feb 27-Mar 05

EXTERNAL DEPENDENCIES:

⚠ Payment Gateway Provider: Test credentials by Jan 25

⚠ Email Service: Test SMTP credentials by Jan 28

⚠ SMS Gateway: Test API access by Jan 28

⚠ Cloud Provider (AWS): Environment provisioning by Jan 27

**13\. COMMUNICATION PLAN**

MEETING                  FREQUENCY    DAY/TIME           ATTENDEES

────────────────────────────────────────────────────────────────────────

Daily Standup           Daily        9:00 AM (15 min)   QA Team, Test Lead

Test Status Meeting     Daily        5:00 PM (30 min)   Test Lead, PM, Dev Lead

Defect Triage          Tue, Thu     11:00 AM (45 min)  Test Lead, Developers,

                                                        BA, PM

Weekly Status Review    Weekly       Fri 3:00 PM (1hr)  All stakeholders

Risk Review            Weekly       Mon 2:00 PM (30min) Test Manager, PM,

                                                        Test Lead

UAT Coordination       As needed    TBD                 Test Lead, BA, UAT Users

REPORTS:

\- Daily: Test execution status (via email to PM, Dev Lead)

\- Daily: Defect summary dashboard (JIRA)

\- Weekly: Detailed test status report (Friday EOD)

\- Weekly: Metrics dashboard (test coverage, pass%, defect trends)

\- End of cycle: Test summary report

COMMUNICATION CHANNELS:

\- Email: For formal communication, reports

\- Slack: For quick questions, updates (\#qa-testing channel)

\- JIRA: For defect communication

\- Confluence: For documentation

\- Video Call (Zoom): For meetings

ESCALATION PATH:

Level 1: Test Lead (for blocking issues, resource needs)

Level 2: Test Manager (for high-risk issues, conflicts)

Level 3: Project Manager (for schedule, budget, scope issues)

Level 4: Steering Committee (for Go/No-Go decisions)

**14\. TEST METRICS**

METRICS TO BE TRACKED:

EXECUTION METRICS:

1\. Test Case Execution Progress

   \- Total test cases: X

   \- Executed: Y (Y/X %)

   \- Pending: Z

   \- Blocked: A

2\. Test Pass/Fail Rate

   \- Passed: X (X/Total %)

   \- Failed: Y (Y/Total %)

   \- Blocked: Z (Z/Total %)

3\. Requirements Coverage

   \- Total requirements: X

   \- Covered: Y (Y/X %)

   \- Not covered: Z

DEFECT METRICS:

4\. Defect Density

   \- Total defects found

   \- Defects per test case

   \- Defects per requirement

5\. Defect Distribution

   \- By Severity: S1, S2, S3, S4

   \- By Priority: P0, P1, P2, P3

   \- By Module: Cart, Checkout, etc.

   \- By Type: Functional, UI, Performance

6\. Defect Status

   \- Open: X

   \- In Progress: Y

   \- Fixed: Z

   \- Retest: A

   \- Closed: B

   \- Reopened: C

7\. Defect Aging

   \- Age 0-2 days: X

   \- Age 3-5 days: Y

   \- Age \>5 days: Z

QUALITY METRICS:

8\. Defect Rejection Rate

   \- Invalid/Duplicate/Cannot Reproduce

9\. Test Effectiveness

   \- % defects found in testing vs production

10\. Test Efficiency

    \- Test cases executed per day

    \- Defects found per day

REPORTING:

\- Daily dashboard update

\- Weekly trends analysis

\- End-of-cycle comprehensive metrics report

**15\. APPROVALS**

DOCUMENT APPROVAL:

NAME                 ROLE                  SIGNATURE    DATE      STATUS

─────────────────────────────────────────────────────────────────────────

John Doe            Test Lead             \_\_\_\_\_\_\_\_\_    \_\_\_\_\_\_    □ Pending

                                                                 □ Approved

                                                                 □ Rejected

Sarah Williams      Test Manager          \_\_\_\_\_\_\_\_\_    \_\_\_\_\_\_    □ Pending

                                                                 □ Approved

                                                                 □ Rejected

Michael Chen        Project Manager       \_\_\_\_\_\_\_\_\_    \_\_\_\_\_\_    □ Pending

                                                                 □ Approved

                                                                 □ Rejected

David Brown         Development Lead      \_\_\_\_\_\_\_\_\_    \_\_\_\_\_\_    □ Pending

                                                                 □ Approved

                                                                 □ Rejected

Emily Davis         Business Analyst      \_\_\_\_\_\_\_\_\_    \_\_\_\_\_\_    □ Pending

                                                                 □ Approved

                                                                 □ Rejected

COMMENTS/FEEDBACK:

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

REVISION HISTORY:

VERSION   DATE        AUTHOR        CHANGES MADE

─────────────────────────────────────────────────────────────────

1.0       Jan 15      John Doe      Initial draft

1.1       Jan 17      John Doe      Added risk mitigation strategies

1.2       Jan 18      John Doe      Updated schedule based on PM feedback

2.0       Jan 19      John Doe      Final version \- Ready for approval

---

### **✍ PRACTICAL TASK (4 hours)**

**Task 25.1: Create Complete Test Plan**

**Scenario:** You're the Test Lead for a "Food Delivery Mobile App" project.

**Requirements:**

* App allows users to browse restaurants, order food, track delivery  
* Must support iOS and Android  
* Payment integration required  
* First release (MVP)  
* Timeline: 6 weeks for testing  
* Team: 1 Test Lead (you), 3 QA Engineers, 1 Junior QA

**Your Task:** Create a COMPLETE Test Plan (10-15 pages) including ALL sections:

1. Introduction  
2. Test Items/Features to be tested  
3. Features NOT to be tested  
4. Test Approach  
5. Pass/Fail Criteria  
6. Test Deliverables  
7. Test Environment  
8. Schedule (detailed with Gantt chart)  
9. Team & Responsibilities  
10. Entry & Exit Criteria  
11. Risks & Mitigation (minimum 8 risks)  
12. Assumptions & Dependencies  
13. Communication Plan  
14. Test Metrics  
15. Approvals

**Deliverable:** Professional Word/PDF document

---

**Task 25.2: Test Plan Review Exercise**

Download 2 sample test plans from the internet (search "test plan PDF sample").

**For each test plan, analyze:**

1. **Completeness:** What sections are included? What's missing?  
2. **Quality:** Are criteria measurable? Is schedule realistic?  
3. **Clarity:** Is it easy to understand?  
4. **Issues:** Identify 5 problems or gaps  
5. **Improvements:** How would you improve it?

**Create a comparison table:**

| Section | Test Plan 1 | Test Plan 2 | Your Rating | Comments |
| ----- | ----- | ----- | ----- | ----- |
| Introduction | Yes/No | Yes/No | Good/Average/Poor | ... |
| Scope | Yes/No | Yes/No | Good/Average/Poor | ... |
| ... | ... | ... | ... | ... |

---

**Task 25.3: Gap Analysis**

**Given Scenario:** You receive a test plan for review that has these issues:

* No specific numbers in pass/fail criteria ("most test cases should pass")  
* Schedule shows "Testing: 2 weeks" with no breakdown  
* Only 3 risks identified  
* No entry/exit criteria  
* Team section just says "QA Team" with no names or roles

**Your Task:**

1. **Identify all gaps** (minimum 10\)  
2. **Assess impact** of each gap (High/Medium/Low)  
3. **Provide specific corrections** for each gap  
4. **Rewrite the problematic sections** properly

**Format:**

GAP \#1: Vague pass criteria

Impact: HIGH

Issue: Says "most test cases should pass" \- not measurable

Correction: "≥95% test cases must pass (114/120 minimum)"

Rewritten Section: \[Provide complete rewrite\]

---

**Task 25.4: Stakeholder Presentation**

Create a **PowerPoint presentation (10-12 slides)** to present your test plan to stakeholders.

**Required Slides:**

1. Title & Overview  
2. Project Scope \- In/Out  
3. Testing Approach  
4. Timeline & Milestones  
5. Team Structure  
6. Key Risks & Mitigation  
7. Success Criteria  
8. Resource Requirements  
9. Communication Plan  
10. Q\&A

**Focus on:** Business value, risk mitigation, confidence building

---

**Task 25.5: Template Customization**

Create 3 different test plan templates for different project types:

1. **Agile Project Template** (Lightweight, Sprint-focused)  
2. **Waterfall Project Template** (Comprehensive, Detailed)  
3. **Small Project Template** (Simplified, 3-5 pages)

Each template should:

* Have appropriate sections  
* Include instructions/examples in each section  
* Be ready to use (just fill in the blanks)  
* Have proper formatting and structure

---

### **📝 ASSIGNMENT (4 hours)**

**1\. Real Project Test Plan (Main Assignment)**

**Scenario:** You've been hired as QA Lead for "SmartHome IoT Control App"

**Project Details:**

* Mobile app (iOS & Android) to control smart home devices  
* Features: Device pairing, room management, automation rules, voice control  
* Integration with: Alexa, Google Home, 50+ device brands  
* Security critical (home access control)  
* Performance critical (real-time device control)  
* Timeline: 8 weeks testing  
* Team: You (Test Lead), 2 Senior QA, 3 QA Engineers, 2 Junior QA  
* Budget: $80,000  
* High-profile launch planned

**Deliverables:**

**A) Complete Test Plan Document (15-20 pages)** Include all 15 sections with realistic, specific details

**B) Risk Register Spreadsheet**

* Identify minimum 15 risks  
* Assess Probability, Impact, Risk Level  
* Detailed mitigation strategies  
* Risk ownership assignment  
* Monitoring plan

**C) Test Schedule Gantt Chart**

* All testing phases  
* Dependencies  
* Milestones  
* Resource allocation  
* Create in Excel or Project tool

**D) Test Metrics Dashboard**

* Design dashboard layout (mock-up)  
* Identify 10 KPIs to track  
* Show sample metrics visualization  
* Include daily, weekly, end-of-cycle reports

**E) Stakeholder Communication Plan**

* Meeting schedule  
* Report templates  
* Escalation matrix  
* Communication channels

---

**2\. Test Plan Improvement Exercise**

**Given:** A poorly written test plan (create one or use a sample with intentional errors)

**Bad Test Plan includes:**

* Vague objectives  
* No measurable criteria  
* Unrealistic schedule  
* Missing sections  
* Ambiguous language  
* No risk analysis

**Your Task:**

1. **Mark-up the document** with all issues identified (use comments)  
2. **Create improvement report** (what's wrong, why it's wrong, impact)  
3. **Rewrite 5 sections completely** with best practices applied  
4. **Add missing sections** (create from scratch)  
5. **Final review checklist** (for future test plans)

---

**3\. Test Plan Defense**

Write a document as if you're presenting to a tough stakeholder who questions everything:

**Stakeholder Questions:**

1. "Why do we need 8 weeks for testing? Can we do it in 4?"  
2. "Why do we need 8 testers? Can 3 people handle it?"  
3. "Why are you spending 40% time on payment testing? Other features are important too."  
4. "What if requirements change during testing?"  
5. "How do you know 95% pass rate is good enough?"  
6. "What guarantees do you give that production will be bug-free?"

**For each question, provide:**

* Clear, logical answer  
* Data/evidence to support your answer  
* Alternatives if needed  
* Risk explanation if their suggestion is followed

---

**4\. Industry Research Assignment**

**Research and document:**

**A) Compare Test Plans across industries:**

* Banking/Finance  
* Healthcare  
* E-commerce  
* Gaming  
* IoT/Embedded systems

**Find:** What's different? What's common? Special considerations?

**B) Test Plan Standards:**

* IEEE 829 details  
* ISO/IEC 29119 standards  
* Agile test plan approaches  
* Modern trends (AI in testing, shift-left, continuous testing)

**C) Tool Comparison:**

* Compare 5 test management tools  
* How do they handle test planning?  
* Pros and cons  
* Recommendations

**Deliverable:** Comprehensive research report (8-10 pages)

---

### **📚 RESOURCES**

**Templates:**

* IEEE 829 Test Plan Template (download)  
* Agile Test Plan Template  
* Test Plan Checklist  
* Risk Register Template  
* Communication Plan Template

**Reading:**

* "Software Test Plan \- IEEE 829" \- Full specification  
* "How to Write a Test Plan" \- Guru99 article  
* "Test Planning in Agile" \- Atlassian guide

**Videos:**

* "Test Plan Tutorial" \- YouTube (search recommended channels)  
* "Creating Effective Test Plans" webinars

**Tools:**

* Microsoft Project (for Gantt charts)  
* Excel (for schedules, matrices)  
* Draw.io (for diagrams)  
* Confluence (for documentation)

**Sample Test Plans:**

* Search: "Sample Test Plan PDF" (analyze 3-5 examples)  
* GitHub repositories with test plan samples

---

## **🎯 DAY 25 SUCCESS CRITERIA**

By end of today, you should be able to: ✅ Create a complete, professional test plan from scratch ✅ Fill in all sections with realistic, specific details ✅ Make all criteria measurable and specific ✅ Identify and document risks comprehensively ✅ Create realistic schedules with dependencies ✅ Present test plan to stakeholders confidently ✅ Review and critique other test plans ✅ Customize templates for different project types

**Next:** Day 26 \- Requirements Analysis begins\!

---

# **MODULE 6: REQUIREMENTS ANALYSIS**

## **(Days 26-30)**

---

## **📅 DAY 26: Understanding Requirements (BRS, FRS, SRS)**

### **📖 THEORY NOTES**

**What are Requirements?**

Requirements are documented needs and expectations of what a system should do and how it should perform.

**Quote:** *"If you don't understand the requirements, you don't know what to test."*

---

### **WHY REQUIREMENTS MATTER IN TESTING**

1. **Foundation of Testing:** Can't write test cases without requirements  
2. **Scope Definition:** Defines what to test and what not to test  
3. **Acceptance Criteria:** Defines when testing is complete  
4. **Defect Identification:** Deviation from requirements \= defect  
5. **Communication:** Common understanding for all teams  
6. **Traceability:** Link requirements → test cases → defects

**Testing Reality:**

* 40-50% of defects originate from poor requirements  
* Clear requirements \= 30-40% fewer bugs in production  
* Time spent understanding requirements \= Time saved in testing

---

### **TYPES OF REQUIREMENT DOCUMENTS**

### **1\. BRS \- Business Requirements Specification**

**What:** High-level business needs and objectives

**Created By:** Business Analysts, Product Managers, Business Owners

**Audience:** Executives, stakeholders, business users

**Purpose:** WHY the system is needed

**Content:**

* Business objectives  
* Business needs  
* Problem statement  
* Expected business benefits  
* High-level scope  
* Business rules  
* Success criteria (business perspective)

**Example \- E-commerce BRS:**

BUSINESS REQUIREMENT: Increase Online Sales

Business Objective:

\- Increase online revenue by 25% in next quarter

\- Reduce cart abandonment rate from 70% to 50%

\- Improve customer satisfaction score from 3.5 to 4.5

Business Need:

Currently, customers are abandoning carts due to complex checkout process.

We need a streamlined, one-click checkout option to compete with Amazon.

Expected Benefits:

\- Additional $500K revenue per quarter

\- Higher customer retention (65% to 80%)

\- Reduced customer support calls (30% reduction)

Business Rules:

\- Only registered users eligible for one-click checkout

\- Minimum order value: $25

\- Limited to domestic shipping addresses

\- Payment method must be pre-saved

Success Criteria:

\- 40% of registered users adopt one-click checkout

\- Cart abandonment rate drops to \<50%

\- Average checkout time reduces from 5 minutes to 1 minute

**Tester's Role with BRS:**

* Understand business context  
* Identify testable business rules  
* Validate business success criteria  
* Participate in BRS review meetings

---

### **2\. FRS \- Functional Requirements Specification**

**What:** Detailed description of WHAT the system should do

**Created By:** Business Analysts, Product Managers

**Audience:** Development team, QA team, technical teams

**Purpose:** WHAT features and functions are needed

**Content:**

* Detailed functional requirements  
* User interactions  
* System behaviors  
* Input/Output specifications  
* Business logic  
* User roles and permissions  
* Workflows and processes  
* Data requirements  
* Validation rules  
* Error handling

**Example \- E-commerce FRS:**

FUNCTIONAL REQUIREMENT: One-Click Checkout Feature

FR-001: One-Click Checkout Button

Description: System shall display "Buy Now with 1-Click" button on product 

detail page for registered users with saved payment method.

Preconditions:

\- User must be logged in

\- User must have at least one saved payment method

\- User must have at least one saved shipping address

\- Product must be in stock

Main Flow:

1\. User clicks "Buy Now with 1-Click" button

2\. System validates user eligibility

3\. System creates order using default payment and shipping

4\. System processes payment

5\. System confirms order and displays order number

6\. System sends confirmation email

Business Rules:

\- Default payment method used (last used or marked as default)

\- Default shipping address used (marked as primary)

\- Order total must be ≥$25

\- Only available for items sold by our company (not marketplace sellers)

\- Limited to 5 orders per day per user (fraud prevention)

Input:

\- User click on "Buy Now with 1-Click" button

\- Product ID

\- Quantity (default: 1\)

Output:

\- Order confirmation page with order number

\- Confirmation email sent to registered email

\- SMS notification (if opted in)

Validation Rules:

\- Product must be in stock (quantity available ≥ requested quantity)

\- Payment method must be valid (not expired)

\- Shipping address must be complete

\- User account must be active (not suspended)

Error Conditions:

\- If payment fails → Display error "Payment could not be processed. Please 

  try again or use standard checkout"

\- If product out of stock → Display "Sorry, this item is currently out of 

  stock. Add to cart for later"

\- If no saved payment → Display "Please add a payment method to use 

  1-Click checkout"

\- If order limit reached → Display "You've reached the daily order limit. 

  Please try again tomorrow"

Non-Functional Requirements:

\- Page load time: \<2 seconds

\- Payment processing time: \<5 seconds

\- 99.9% uptime during business hours

\- Support 1000 concurrent users

**Tester's Role with FRS:**

* PRIMARY document for test case writing  
* Identify all test scenarios  
* Understand workflows and edge cases  
* Verify all validations and error conditions  
* Ask clarifying questions on ambiguities

---

### **3\. SRS \- Software Requirements Specification**

**What:** Comprehensive technical document combining business, functional, and non-functional requirements

**Created By:** System Architects, Senior Business Analysts, Technical Leads

**Audience:** Entire project team (Business, Development, QA, Infrastructure)

**Purpose:** Complete specification \- WHAT and HOW (at high level)

**Content:**

* Introduction and scope  
* Overall description  
* Functional requirements (detailed)  
* Non-functional requirements (performance, security, usability)  
* System features  
* External interface requirements  
* System constraints  
* Assumptions and dependencies

**SRS Structure (IEEE 830 Standard):**

1\. INTRODUCTION

   1.1 Purpose

   1.2 Scope

   1.3 Definitions, Acronyms, Abbreviations

   1.4 References

   1.5 Overview

2\. OVERALL DESCRIPTION

   2.1 Product Perspective

   2.2 Product Functions

   2.3 User Characteristics

   2.4 Constraints

   2.5 Assumptions and Dependencies

3\. SPECIFIC REQUIREMENTS

   3.1 Functional Requirements

       3.1.1 Feature 1

       3.1.2 Feature 2

       ...

   3.2 Non-Functional Requirements

       3.2.1 Performance Requirements

       3.2.2 Security Requirements

       3.2.3 Usability Requirements

       3.2.4 Reliability Requirements

   3.3 External Interface Requirements

       3.3.1 User Interfaces

       3.3.2 Hardware Interfaces

       3.3.3 Software Interfaces

       3.3.4 Communication Interfaces

4\. APPENDICES

**Example \- E-commerce SRS Section:**

3.1.5 One-Click Checkout Feature

3.1.5.1 Description

The system shall provide registered users with a one-click checkout option 

that allows immediate purchase without navigating through standard checkout 

process.

3.1.5.2 Functional Requirements

FR-1C-001: Button Display

The system shall display "Buy Now with 1-Click" button on product detail 

page when ALL conditions are met:

\- User is authenticated (logged in)

\- User has ≥1 saved payment method (card not expired)

\- User has ≥1 saved shipping address (complete and valid)

\- Product is in stock (available quantity \> 0\)

\- Product is eligible (not marketplace seller product)

FR-1C-002: Order Creation

When user clicks "Buy Now with 1-Click", system shall:

\- Create order record with unique order ID

\- Use default payment method (user's last used or marked default)

\- Use primary shipping address

\- Set quantity to 1 (default)

\- Calculate order total (item price \+ tax \+ shipping)

\- Apply current promotions if eligible

FR-1C-003: Payment Processing

System shall process payment immediately:

\- Charge default payment method

\- If successful: proceed to FR-1C-004

\- If failed: display error (FR-1C-008) and do NOT create order

FR-1C-004: Order Confirmation

Upon successful payment, system shall:

\- Display order confirmation page with order number

\- Show estimated delivery date

\- Provide tracking link (when available)

\- Send confirmation email within 2 minutes

\- Send SMS if user opted in

FR-1C-005: Order Limits (Fraud Prevention)

System shall enforce limits:

\- Maximum 5 one-click orders per user per day

\- Maximum $2000 total value per day via one-click

\- If limit exceeded: display error and redirect to standard checkout

3.1.5.3 Non-Functional Requirements

NFR-1C-001: Performance

\- Button load time: \<500ms

\- Order processing time: \<3 seconds (end-to-end)

\- Page response time: \<2 seconds

NFR-1C-002: Security

\- Payment data encrypted using TLS 1.3

\- PCI-DSS compliant payment processing

\- Tokenized payment storage (no plain card numbers)

\- Session timeout: 30 minutes

NFR-1C-003: Usability

\- Button clearly visible (minimum 44x44 pixels touch target)

\- Confirmation message displayed prominently

\- Error messages clear and actionable

\- Mobile responsive design

NFR-1C-004: Reliability

\- 99.9% uptime during business hours

\- Graceful degradation (if feature fails, standard checkout available)

\- Transaction rollback on payment failure

3.1.5.4 Business Rules

BR-1C-001: Minimum order value: $25

BR-1C-002: Only domestic shipping addresses supported

BR-1C-003: User account must be in good standing (no fraud flags)

BR-1C-004: Feature available 24/7 except maintenance windows

BR-1C-005: Automatic refund if order cancelled within 1 hour

3.1.5.5 Data Requirements

\- Order ID: Auto-generated, 10-digit numeric

\- User ID: FK to Users table

\- Product ID: FK to Products table

\- Payment Method ID: FK to PaymentMethods table

\- Shipping Address ID: FK to Addresses table

\- Order Date/Time: Timestamp (UTC)

\- Order Status: Enum (Pending, Confirmed, Shipped, Delivered, Cancelled)

\- Order Total: Decimal(10,2)

3.1.5.6 Interface Requirements

UI-1C-001: Button Design

\- Text: "Buy Now with 1-Click"

\- Color: Primary brand color (\#FF9900)

\- Position: Below "Add to Cart" button

\- Icon: Lightning bolt symbol

\- Disabled state: Gray with tooltip explaining why

3.1.5.7 Error Handling

ERR-1C-001: Payment Failure

\- Error Code: PAYMENT\_FAILED

\- Message: "Payment could not be processed. Please try again or use 

  standard checkout."

\- Action: Log error, send alert to ops team, do NOT create order

ERR-1C-002: Out of Stock

\- Error Code: OUT\_OF\_STOCK

\- Message: "Sorry, this item is currently out of stock."

\- Action: Update button to "Notify Me" option

ERR-1C-003: Daily Limit Reached

\- Error Code: LIMIT\_EXCEEDED

\- Message: "You've reached the daily one-click order limit. Please use 

  standard checkout or try again tomorrow."

\- Action: Hide 1-click button for 24 hours

3.1.5.8 Dependencies

\- User Management Module (authentication)

\- Payment Gateway Integration (payment processing)

\- Inventory Management System (stock verification)

\- Email Service (notifications)

\- SMS Gateway (optional notifications)

3.1.5.9 Assumptions

\- Users have valid email addresses

\- Payment gateway uptime: 99.95%

\- Network latency: \<100ms average

\- Users understand one-click concept

**Tester's Role with SRS:**

* Comprehensive test planning  
* Test case writing for all requirements  
* Non-functional testing planning  
* Interface testing planning  
* Review and validate completeness

---

### **COMPARISON: BRS vs FRS vs SRS**

| Aspect | BRS | FRS | SRS |
| ----- | ----- | ----- | ----- |
| **Focus** | WHY | WHAT | WHAT \+ HOW (overview) |
| **Level** | High-level, Business | Detailed, Functional | Comprehensive, Technical |
| **Language** | Business terminology | Mixed (business \+ technical) | Technical terminology |
| **Audience** | Business stakeholders | Developers, QA | Entire team |
| **Detail** | Objectives, benefits | Features, workflows | Complete specification |
| **Created By** | Business Analyst/PM | Business Analyst | System Architect/Lead BA |
| **When** | Project initiation | After BRS approval | After FRS approval |
| **Page Count** | 5-15 pages | 20-50 pages | 50-200+ pages |
| **Testing Use** | Understand context | Write test cases | Complete test planning |
| **Example** | "Increase sales by 25%" | "One-click checkout button with validation rules" | "Complete feature spec with NFRs, interfaces, data model" |

---

### **REQUIREMENT QUALITY CHARACTERISTICS**

**Good Requirements are:**

**1\. CLEAR** ❌ Bad: "System should be fast" ✅ Good: "Page load time shall be \<2 seconds for 95% of requests"

**2\. COMPLETE** ❌ Bad: "User can add items to cart" ✅ Good: "User can add items to cart (quantity 1-99). System validates stock. If out of stock, display error. If in stock, add to cart and show confirmation."

**3\. CONSISTENT** ❌ Bad: One place says "max 10 items per cart", another says "max 20 items" ✅ Good: Same rule stated consistently everywhere

**4\. VERIFIABLE/TESTABLE** ❌ Bad: "System should be user-friendly" ✅ Good: "80% of users shall complete checkout in ≤3 minutes without help"

**5\. UNAMBIGUOUS** ❌ Bad: "System may send notification" ✅ Good: "System shall send email notification within 5 minutes of order confirmation"

**6\. FEASIBLE** ❌ Bad: "System shall have zero defects" ✅ Good: "System shall have \<5 critical defects per 1000 test cases"

**7\. TRACEABLE**

* Each requirement has unique ID  
* Can trace from BRS → FRS → SRS → Design → Code → Test Cases

**8\. PRIORITIZED**

* Must Have (P0) \- Critical  
* Should Have (P1) \- Important  
* Could Have (P2) \- Nice to have  
* Won't Have (P3) \- Future release

---

### **REQUIREMENT ANALYSIS FOR TESTERS**

**Step 1: READ Thoroughly**

* Read multiple times  
* Read slowly  
* Take notes  
* Highlight unclear parts

**Step 2: UNDERSTAND Context**

* Why is this feature needed?  
* Who will use it?  
* How often will it be used?  
* What's the business value?

**Step 3: IDENTIFY Testable Requirements**

* What can be tested?  
* What are the acceptance criteria?  
* What are the validation rules?  
* What are the error conditions?

**Step 4: FIND Gaps and Ambiguities**

* Missing information  
* Unclear statements  
* Contradictions  
* Incomplete flows

**Step 5: ASK Questions** Create a questions list:

REQUIREMENT CLARIFICATION QUESTIONS

Requirement ID: FR-1C-001

Questions:

1\. What happens if user has multiple default payment methods?

2\. Is there a maximum order value limit for one-click?

3\. Should we show loading indicator during processing?

4\. What if user's address is international format?

5\. Can user change quantity before clicking one-click button?

6\. What happens if item goes out of stock between page load and click?

7\. Should we log all one-click attempts for analytics?

8\. What's the retry logic if payment gateway times out?

**Step 6: DOCUMENT Assumptions** If requirements are unclear, document your assumptions:

ASSUMPTIONS FOR TESTING

Assumption 1: If not specified, we assume default quantity \= 1

Assumption 2: One-click button hidden if any prerequisite not met

Assumption 3: Payment processing timeout \= 30 seconds

Assumption 4: User can cancel order within 1 hour

Status: Pending BA confirmation

---

### **COMMON REQUIREMENT ISSUES**

**1\. Ambiguous Language**

* "User-friendly", "Fast", "Secure", "Efficient"  
* "May", "Should", "Might"  
* "As soon as possible", "Shortly"

**2\. Missing Information**

* No error conditions specified  
* No boundary values mentioned  
* No performance criteria  
* No security requirements

**3\. Conflicting Requirements**

* Different documents say different things  
* Requirements contradict each other  
* Business rules inconsistent

**4\. Non-Testable Requirements**

* Subjective statements  
* No measurable criteria  
* Vague descriptions

**5\. Gold Plating**

* Unnecessary features  
* Over-complicated requirements  
* Features nobody asked for

**6\. Scope Creep**

* Requirements keep changing  
* New features added mid-project  
* No change control

---

### **TESTER'S REQUIREMENT REVIEW CHECKLIST**

REQUIREMENT REVIEW CHECKLIST

Requirement ID: \_\_\_\_\_\_\_\_\_\_

Reviewer: \_\_\_\_\_\_\_\_\_\_

Date: \_\_\_\_\_\_\_\_\_\_

CLARITY:

☐ Requirement is clearly stated

☐ No ambiguous terms used

☐ Technical terms defined

☐ Examples provided where needed

COMPLETENESS:

☐ All scenarios covered (positive, negative, edge cases)

☐ Input specifications complete

☐ Output specifications complete

☐ Error conditions specified

☐ Validation rules defined

☐ Business rules included

TESTABILITY:

☐ Can be tested (has measurable criteria)

☐ Acceptance criteria clear

☐ Expected behavior defined

☐ Can write test cases from this

CONSISTENCY:

☐ Consistent with other requirements

☐ No contradictions found

☐ Terminology consistent

☐ Aligns with business rules

FEASIBILITY:

☐ Technically feasible

☐ Realistic timelines

☐ Resources available

TRACEABILITY:

☐ Has unique ID

☐ Linked to business requirement

☐ Priority assigned

☐ Owner identified

QUESTIONS/ISSUES IDENTIFIED:

1\. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

2\. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

3\. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

OVERALL ASSESSMENT:

☐ Approved \- Ready for test case development

☐ Approved with minor clarifications

☐ Need major clarifications \- Not ready

Signature: \_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_\_\_\_

---

### **✍ PRACTICAL TASK (3 hours)**

**Task 26.1: Identify Requirement Type**

Read these requirement statements and identify if they belong to BRS, FRS, or SRS:

1. "The company wants to reduce customer support calls by 40% through self-service options"

   * Type: \_\_\_\_\_\_\_  
2. "System shall display error message 'Invalid email format' when user enters email without @ symbol"

   * Type: \_\_\_\_\_\_\_  
3. "The login button shall be 120x40 pixels, use brand color \#336699, and have 5px border radius"

   * Type: \_\_\_\_\_\_\_  
4. "Increase market share from 15% to 25% in the next fiscal year"

   * Type: \_\_\_\_\_\_\_  
5. "User can search products by name, category, price range, and brand. Search results displayed in grid view with 20 items per page"

   * Type: \_\_\_\_\_\_\_  
6. "System response time shall be \<1 second for 99% of API calls under normal load"

   * Type: \_\_\_\_\_\_\_

---

**Task 26.2: Analyze Requirements Quality**

Evaluate these requirements. Identify problems and rewrite them properly:

**Requirement 1:** "The system should be fast and user-friendly"

Problems:

* ---

* ---

Rewritten:

* ---

**Requirement 2:** "User may be able to add products to wishlist if they want"

Problems:

* ---

Rewritten:

* ---

**Requirement 3:** "Password should be strong"

Problems:

* ---

Rewritten:

* ---

**Requirement 4:** "System will send notification"

Problems:

* ---

Rewritten:

* ---

**Requirement 5:** "Search should return relevant results quickly"

Problems:

* ---

Rewritten:

* ---

---

**Task 26.3: Create Clarification Questions**

For this requirement, create 10 clarification questions:

**Requirement:** "Users can upload profile pictures. System shall validate the image and display error if invalid."

**Your Questions:**

1. ---

2. ---

3. ---

4. ---

5. ---

6. ---

7. ---

8. ---

9. ---

10. ---

---

**Task 26.4: Write Different Requirement Types**

For a "Password Reset" feature, write:

**A) Business Requirement (BRS style):**

* Business objective  
* Business need  
* Expected benefit  
* Success criteria

**B) Functional Requirement (FRS style):**

* Detailed description  
* Preconditions  
* Main flow (steps)  
* Business rules  
* Validation rules  
* Error conditions

**C) System Requirement (SRS style):**

* Complete specification  
* Functional requirements  
* Non-functional requirements  
* Interface requirements  
* Data requirements  
* Error handling

---

**Task 26.5: Requirement Review Exercise**

You're given this requirement to review:

FR-2.3: User Registration

User can register on the website. They need to provide information. 

System will validate and create account. Confirmation will be sent.

**Your Tasks:**

1. **Identify all problems** (minimum 10\)  
2. **Ask clarification questions** (minimum 15\)  
3. **List missing information**  
4. **Rewrite the requirement properly** (detailed, complete, testable)  
5. **Create test scenarios** based on your rewritten requirement

---

### **📝 ASSIGNMENT (4 hours)**

**1\. Complete Requirement Analysis Document**

**Scenario:** You receive this requirement for a "Hotel Booking System":

REQUIREMENT: Online Hotel Booking

Users should be able to search for hotels, view details, and book rooms 

online. Payment can be made online or at hotel. Users will get confirmation.

**Your Deliverables:**

**A) Requirement Analysis Report (5-6 pages)** Include:

* Problems identified in given requirement  
* Ambiguities and gaps  
* Assumptions documented  
* Clarification questions (minimum 30 questions)  
* Risks from unclear requirements

**B) Rewritten Requirements:**

* BRS version (1 page)  
* FRS version (3-4 pages with all details)  
* SRS snippet (2 pages showing how it should look)

**C) Testability Analysis:**

* What's testable in current requirement  
* What's NOT testable  
* How to make it testable  
* Acceptance criteria for each requirement

---

**2\. Requirement Quality Assessment**

Analyze these 10 requirements and create assessment report:

1. "System should be secure"  
2. "User can login with username and password. If credentials invalid, show error. If valid, redirect to dashboard."  
3. "Page load time: \<2 seconds"  
4. "Shopping cart may hold up to certain number of items"  
5. "Email notifications sent promptly"  
6. "Password must be strong with special characters"  
7. "System shall process payment using Payment Gateway API v2.0, handle success/failure responses, update order status accordingly, send confirmation email within 2 minutes, and log transaction"  
8. "Users like the interface"  
9. "Search functionality should return results"  
10. "System available 24/7"

**For each requirement, provide:**

* Quality rating (Poor/Average/Good/Excellent)  
* Problems identified  
* Rewritten version  
* Test scenarios possible

---

**3\. Create Requirement Review Template**

Create a comprehensive requirement review template that can be used for any project.

**Include sections:**

* Requirement information  
* Quality checklist (20+ checkpoints)  
* Testability assessment  
* Questions/clarifications  
* Gap analysis  
* Risk assessment  
* Approval section

**Make it:** Professional, reusable, easy to fill

---

**4\. Real-World Analysis**

Choose a real application you use (Amazon, Netflix, Uber, etc.):

**Pick one feature** (e.g., Amazon's "Add to Cart")

**Write:**

* What the business requirement might have been (BRS)  
* What the functional requirement would look like (FRS)  
* What system requirements would include (SRS excerpt)  
* Test scenarios based on your written requirements  
* Questions you would ask as a tester

**Deliverable:** Complete requirement documentation (8-10 pages)

---

### **📚 RESOURCES**

**Standards:**

* IEEE 830: SRS Recommended Practice  
* IEEE 829: Test Documentation Standard

**Reading:**

* "Writing Effective Use Cases" \- Alistair Cockburn  
* "Software Requirements" \- Karl Wiegers  
* "Requirements Engineering" articles

**Templates:**

* BRS Template  
* FRS Template  
* SRS Template (IEEE 830\)  
* Requirement Review Checklist

**Tools:**

* Confluence (documentation)  
* JIRA (requirement tracking)  
* Requirements management tools (Jama, Doors)

---

## **🎯 DAY 26 SUCCESS CRITERIA**

By end of today, you should be able to: ✅ Differentiate between BRS, FRS, and SRS ✅ Understand what each document contains ✅ Identify good vs bad requirements ✅ Ask relevant clarification questions ✅ Analyze requirements from testing perspective ✅ Identify gaps and ambiguities ✅ Rewrite poor requirements properly ✅ Understand your role in requirement reviews

## **📅 DAY 27: Requirements Traceability Matrix (RTM)**

### **📖 THEORY NOTES**

**What is RTM?**

Requirements Traceability Matrix (RTM) is a document that maps and traces user requirements with test cases. It ensures that all requirements are covered by test cases and tested.

**Other Names:**

* Traceability Matrix  
* Requirements Coverage Matrix  
* Test Coverage Matrix

**Quote:** *"If you can't trace it, you can't prove you tested it."*

---

### **WHY RTM IS IMPORTANT**

**1\. Complete Coverage**

* Ensures NO requirement is missed  
* Proves every requirement has test cases  
* Identifies gaps in testing

**2\. Traceability**

* Forward Traceability: Requirement → Test Cases → Defects  
* Backward Traceability: Test Cases → Requirements  
* Bi-directional visibility

**3\. Impact Analysis**

* If requirement changes, know which test cases affected  
* If defect found, trace back to requirement  
* If test fails, know which requirement impacted

**4\. Progress Tracking**

* How many requirements tested?  
* Testing completion percentage  
* Which requirements pending?

**5\. Audit & Compliance**

* Proof of testing for regulatory requirements  
* Quality assurance documentation  
* Client deliverable

**6\. Stakeholder Communication**

* Clear visibility of testing coverage  
* Evidence of thoroughness  
* Confidence building

---

### **RTM STRUCTURE**

**Basic RTM Columns:**

| Req ID | Requirement Description | Test Case ID | Test Case Description | Status | Comments |

**Comprehensive RTM Columns:**

| Req ID | Requirement | Priority | Test Case ID(s) | Test Scenario | Execution Status | Pass/Fail | Defect ID | Tested By | Test Date | Comments |

---

### **RTM COLUMN DESCRIPTIONS**

**1\. Requirement ID**

* Unique identifier from requirement document  
* Example: FR-001, BR-REG-01, REQ-LOGIN-03

**2\. Requirement Description**

* Brief description of the requirement  
* Or full requirement text  
* Example: "User shall be able to login with email and password"

**3\. Requirement Type** (Optional)

* Functional / Non-Functional  
* Feature / Enhancement / Bug Fix

**4\. Priority**

* P0 (Critical), P1 (High), P2 (Medium), P3 (Low)  
* Must Have / Should Have / Could Have / Won't Have

**5\. Test Scenario**

* High-level test scenario  
* Example: "Verify user login functionality"

**6\. Test Case ID(s)**

* One or more test case IDs  
* Example: TC-LOGIN-001, TC-LOGIN-002, TC-LOGIN-003

**7\. Test Case Description**

* Brief description of test case  
* Example: "Login with valid credentials"

**8\. Execution Status**

* Not Executed / In Progress / Executed / Blocked

**9\. Test Result**

* Pass / Fail / Blocked / Skipped

**10\. Defect ID(s)**

* Link to defects if test failed  
* Example: BUG-123, DEF-456

**11\. Tested By**

* Name of tester who executed  
* Example: John Doe

**12\. Test Date**

* Date of execution  
* Example: 2025-02-15

**13\. Comments/Remarks**

* Additional notes  
* Blockers, dependencies, etc.

---

### **TYPES OF RTM**

**1\. Forward Traceability**

* From Requirements → Test Cases  
* Ensures all requirements have test coverage

Requirement FR-001   
    ↓  
Test Scenarios  
    ↓  
Test Cases (TC-001, TC-002, TC-003)  
    ↓  
Test Execution  
    ↓  
Defects (if any)

**2\. Backward Traceability**

* From Test Cases → Requirements  
* Ensures no test cases without requirements (orphan tests)  
* Removes unnecessary test cases

Test Case TC-001  
    ↑  
Linked to Requirement FR-001

**3\. Bi-directional Traceability**

* Both forward and backward  
* Complete visibility  
* Industry best practice

---

### **RTM EXAMPLE: E-COMMERCE LOGIN FEATURE**

**Simple RTM:**

| Req ID | Requirement Description | Test Case ID | Test Case Description | Status | Result |
| ----- | ----- | ----- | ----- | ----- | ----- |
| FR-LOGIN-001 | User can login with valid email and password | TC-LOGIN-001 | Login with valid credentials | Executed | Pass |
| FR-LOGIN-001 | User can login with valid email and password | TC-LOGIN-002 | Login with invalid email | Executed | Pass |
| FR-LOGIN-001 | User can login with valid email and password | TC-LOGIN-003 | Login with invalid password | Executed | Pass |
| FR-LOGIN-002 | System shall show error for invalid credentials | TC-LOGIN-004 | Verify error message for wrong password | Executed | Pass |
| FR-LOGIN-002 | System shall show error for invalid credentials | TC-LOGIN-005 | Verify error message for non-existent email | Executed | Fail |
| FR-LOGIN-003 | User shall be redirected to dashboard after successful login | TC-LOGIN-006 | Verify redirect to dashboard | Executed | Pass |
| FR-LOGIN-004 | Password shall be masked during entry | TC-LOGIN-007 | Verify password masking | Not Executed | \- |
| FR-LOGIN-005 | Login session shall timeout after 30 minutes | TC-LOGIN-008 | Verify session timeout | Executed | Pass |

**Analysis from above RTM:**

* Total Requirements: 5  
* Total Test Cases: 8  
* Executed: 7 (87.5%)  
* Not Executed: 1 (12.5%)  
* Pass: 6 (85.7% of executed)  
* Fail: 1 (14.3% of executed)  
* **Gap:** FR-LOGIN-004 not fully tested yet

---

**Comprehensive RTM:**

| Req ID | Requirement | Priority | Test Scenario | Test Case IDs | Total TCs | Executed | Pass | Fail | Coverage | Defect IDs | Comments |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| FR-LOGIN-001 | Login with valid credentials | P0 | Verify login functionality | TC-001, TC-002, TC-003 | 3 | 3 | 3 | 0 | 100% | \- | Complete |
| FR-LOGIN-002 | Error for invalid credentials | P0 | Verify error handling | TC-004, TC-005 | 2 | 2 | 1 | 1 | 100% | BUG-123 | Bug found |
| FR-LOGIN-003 | Redirect after login | P1 | Verify redirect | TC-006 | 1 | 1 | 1 | 0 | 100% | \- | Complete |
| FR-LOGIN-004 | Password masking | P2 | Verify security | TC-007 | 1 | 0 | 0 | 0 | 0% | \- | Pending |
| FR-LOGIN-005 | Session timeout | P1 | Verify timeout | TC-008, TC-009 | 2 | 1 | 1 | 0 | 50% | \- | In progress |

**Metrics from above RTM:**

* Total Requirements: 5  
* Requirements Fully Covered: 3 (60%)  
* Requirements Partially Covered: 1 (20%)  
* Requirements Not Covered: 1 (20%)  
* Overall Test Coverage: 77.8%

---

### **HOW TO CREATE RTM**

**STEP 1: Gather Requirements**

* Collect all requirement documents (BRS, FRS, SRS)  
* Extract all requirements  
* Assign unique IDs if not already assigned

**STEP 2: Create RTM Structure**

* Choose tool (Excel, Google Sheets, TestRail, JIRA)  
* Set up columns  
* Create tabs if multiple modules

**STEP 3: List All Requirements**

* Enter Requirement ID  
* Enter Requirement Description  
* Add Priority  
* Group by module/feature

**STEP 4: Map Test Scenarios**

* For each requirement, identify test scenarios  
* One requirement may have multiple scenarios

**STEP 5: Link Test Cases**

* Write test cases (or reference existing ones)  
* Link test case IDs to requirements  
* One requirement may have multiple test cases

**STEP 6: Update During Execution**

* Update execution status  
* Update pass/fail results  
* Link defects  
* Add comments

**STEP 7: Track Coverage**

* Calculate coverage percentages  
* Identify gaps  
* Report to stakeholders

**STEP 8: Maintain Throughout Project**

* Update when requirements change  
* Update when test cases added/removed  
* Keep it current

---

### **RTM BEST PRACTICES**

**DO: ✅**

* ✅ Create RTM early (during test planning)  
* ✅ Update regularly (daily during execution)  
* ✅ Use unique IDs for traceability  
* ✅ Include all requirement types  
* ✅ Review with stakeholders  
* ✅ Use tool for automation (not just Excel)  
* ✅ Calculate and track metrics  
* ✅ Color code for visual clarity  
* ✅ Version control the RTM  
* ✅ Include in test deliverables

**DON'T: ❌**

* ❌ Create at end of project (too late)  
* ❌ Create once and forget  
* ❌ Skip requirements (even "obvious" ones)  
* ❌ Use vague descriptions  
* ❌ Ignore orphan test cases  
* ❌ Make it too complex (keep simple)  
* ❌ Duplicate requirement entries unnecessarily  
* ❌ Leave blank cells without explanation

---

### **RTM TEMPLATES**

**Template 1: Basic RTM**

PROJECT: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
MODULE: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
VERSION: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
DATE: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

| Req ID | Requirement Description | Test Case ID | Test Status | Result | Defect ID | Tester | Date |  
|--------|------------------------|--------------|-------------|---------|-----------|---------|------|  
|        |                        |              |             |         |           |         |      |

SUMMARY:  
Total Requirements: \_\_\_  
Total Test Cases: \_\_\_  
Coverage: \_\_\_%  
Pass Rate: \_\_\_%

**Template 2: Detailed RTM**

| Req ID | Module | Requirement | Type | Priority | Test Scenario | TC IDs | TC Count | Executed | Pass | Fail | Coverage | Defects | Status | Comments |

**Template 3: Requirements Coverage Summary**

MODULE: Login Feature  
Total Requirements: 10

Coverage Status:  
\- Fully Covered: 7 (70%)  
\- Partially Covered: 2 (20%)  
\- Not Covered: 1 (10%)

Execution Status:  
\- Executed: 25/30 test cases (83%)  
\- Pending: 5/30 test cases (17%)

Quality Metrics:  
\- Pass: 22/25 (88%)  
\- Fail: 3/25 (12%)

Risk Assessment:  
\- High Risk (Not Covered): REQ-LOGIN-010  
\- Medium Risk (Failing): REQ-LOGIN-005

---

### **RTM IN DIFFERENT TOOLS**

**1\. Excel/Google Sheets**

* Pros: Easy, flexible, no cost  
* Cons: Manual updates, limited collaboration  
* Best for: Small projects

**2\. TestRail**

* Built-in RTM features  
* Automatic coverage calculation  
* Test case to requirement linking

**3\. JIRA/Zephyr**

* Requirements as User Stories  
* Test cases linked to stories  
* Traceability reports built-in

**4\. HP ALM / Quality Center**

* Comprehensive traceability  
* Enterprise-grade  
* Complex setup

**5\. TestLink**

* Open source  
* Good traceability features  
* Free option

---

### **RTM METRICS & REPORTING**

**Key Metrics to Track:**

**1\. Requirements Coverage**

Coverage % \= (Requirements with Test Cases / Total Requirements) × 100

Example: (45/50) × 100 \= 90% coverage

**2\. Test Execution Progress**

Execution % \= (Executed Test Cases / Total Test Cases) × 100

Example: (120/150) × 100 \= 80% executed

**3\. Test Pass Rate**

Pass Rate % \= (Passed Test Cases / Executed Test Cases) × 100

Example: (100/120) × 100 \= 83.3% pass rate

**4\. Defect Density**

Defect Density \= Total Defects / Total Requirements

Example: 15 defects / 50 requirements \= 0.3 defects per requirement

**5\. Requirements Status**

* Fully Tested: All test cases executed and passed  
* Partially Tested: Some test cases pending  
* Not Tested: No test cases executed  
* Failed: Test cases executed but failed

---

### **SAMPLE RTM REPORT**

REQUIREMENTS TRACEABILITY MATRIX REPORT

Project: E-Commerce Platform  
Module: Shopping Cart  
Date: February 15, 2025  
Prepared By: John Doe, Test Lead

EXECUTIVE SUMMARY:  
─────────────────────────────────────────────────────────  
Total Requirements: 25  
Requirements Covered: 24 (96%)  
Requirements Not Covered: 1 (4%)  
Total Test Cases: 95  
Test Cases Executed: 88 (93%)  
Test Cases Passed: 79 (90% of executed)  
Test Cases Failed: 9 (10% of executed)  
Defects Found: 12

COVERAGE ANALYSIS:  
─────────────────────────────────────────────────────────  
High Priority Requirements (P0): 8  
  \- Fully Tested: 7 (87.5%)  
  \- Not Tested: 1 (12.5%) ⚠ REQ-CART-003

Medium Priority Requirements (P1): 12  
  \- Fully Tested: 11 (91.7%)  
  \- Partially Tested: 1 (8.3%)

Low Priority Requirements (P2): 5  
  \- Fully Tested: 5 (100%)

GAPS IDENTIFIED:  
─────────────────────────────────────────────────────────  
1\. REQ-CART-003 (P0): Payment integration not tested  
   \- Reason: Payment gateway not available  
   \- Mitigation: Testing scheduled for Feb 18

2\. REQ-CART-015 (P1): Discount calculation partial testing  
   \- Reason: 2 of 5 test cases pending  
   \- Action: Scheduled for Feb 16

DEFECT SUMMARY:  
─────────────────────────────────────────────────────────  
Critical: 1 (BUG-301 \- Payment processing fails)  
High: 3  
Medium: 6  
Low: 2

RECOMMENDATION:  
─────────────────────────────────────────────────────────  
• Complete testing of REQ-CART-003 before release  
• Fix BUG-301 (Critical defect)  
• Overall coverage is good at 96%  
• Pass rate acceptable at 90%

NEXT STEPS:  
─────────────────────────────────────────────────────────  
1\. Complete pending test cases by Feb 18  
2\. Retest 9 failed test cases after bug fixes  
3\. Final RTM review on Feb 20  
4\. Sign-off target: Feb 22

Prepared by: \_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_  
Reviewed by: \_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_  
Approved by: \_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_

---

### **✍ PRACTICAL TASK (4 hours)**

**Task 27.1: Create Basic RTM**

**Scenario:** ATM Machine \- Withdrawal Feature

**Requirements:**

1. REQ-ATM-001: User can withdraw cash using valid card and PIN  
2. REQ-ATM-002: System shall dispense exact amount requested  
3. REQ-ATM-003: System shall update account balance after withdrawal  
4. REQ-ATM-004: System shall print receipt if requested  
5. REQ-ATM-005: System shall show error if insufficient balance  
6. REQ-ATM-006: Daily withdrawal limit: $1000  
7. REQ-ATM-007: System shall capture card if wrong PIN entered 3 times

**Your Task:**

1. Create test scenarios for each requirement  
2. Write test case IDs (at least 3 test cases per requirement)  
3. Create RTM in Excel/Google Sheets  
4. Include all necessary columns  
5. Add sample execution status and results

---

**Task 27.2: RTM Analysis**

You're given this RTM data:

| Req ID | Priority | Test Cases | Executed | Pass | Fail |
| ----- | ----- | ----- | ----- | ----- | ----- |
| REQ-001 | P0 | 5 | 5 | 5 | 0 |
| REQ-002 | P0 | 4 | 4 | 3 | 1 |
| REQ-003 | P1 | 6 | 4 | 4 | 0 |
| REQ-004 | P1 | 3 | 0 | 0 | 0 |
| REQ-005 | P2 | 2 | 2 | 2 | 0 |

**Calculate:**

1. Total test cases: \_\_\_  
2. Execution percentage: \_\_\_%  
3. Pass rate: \_\_\_%  
4. Coverage for P0 requirements: \_\_\_%  
5. Which requirement has highest risk? Why?  
6. What's your recommendation?

---

**Task 27.3: Create Comprehensive RTM**

**Scenario:** Online Banking \- Fund Transfer Module

**Requirements:**

* FR-TXN-001: Transfer money between own accounts  
* FR-TXN-002: Transfer money to other bank accounts  
* FR-TXN-003: Schedule future transfers  
* FR-TXN-004: Verify beneficiary details before transfer  
* FR-TXN-005: Send SMS and email confirmation  
* NFR-TXN-001: Transaction completion time \<5 seconds  
* NFR-TXN-002: Support 1000 concurrent transactions

**Your Task:** Create comprehensive RTM with:

* All columns (minimum 12 columns)  
* Test scenarios  
* Multiple test cases per requirement (total 25+ test cases)  
* Sample execution data  
* Linked defects (create sample defect IDs)  
* Coverage calculations  
* Summary section

---

**Task 27.4: Gap Identification**

Given RTM shows:

* 30 total requirements  
* 25 requirements have test cases  
* 5 requirements have no test cases

**Your Tasks:**

1. Calculate coverage percentage  
2. Identify why requirements might be missing test cases  
3. What questions would you ask?  
4. What's the risk?  
5. Create action plan to close gaps

---

**Task 27.5: RTM Report Creation**

Using your RTM from Task 27.3, create:

**A) Executive Summary Report** (1 page)

* Key metrics  
* Coverage status  
* Issues/risks  
* Recommendations

**B) Detailed RTM Report** (2-3 pages)

* Complete traceability  
* Test execution status  
* Defect summary  
* Gap analysis

**C) Visual Dashboard** (1 page)

* Charts/graphs showing coverage  
* Pie chart for execution status  
* Bar chart for pass/fail  
* Traffic light indicators

---

### **📝 ASSIGNMENT (4 hours)**

**1\. Complete RTM Project**

**Scenario:** E-commerce Checkout Process

**Requirements Provided:**

1\. FR-CHK-001 (P0): User can proceed to checkout from cart  
2\. FR-CHK-002 (P0): User can select shipping address  
3\. FR-CHK-003 (P0): User can add new shipping address  
4\. FR-CHK-004 (P0): User can select payment method  
5\. FR-CHK-005 (P0): User can add new payment method  
6\. FR-CHK-006 (P1): User can apply discount coupon  
7\. FR-CHK-007 (P1): System calculates total (items \+ tax \+ shipping \- discount)  
8\. FR-CHK-008 (P0): User can review order before confirming  
9\. FR-CHK-009 (P0): System processes payment  
10\. FR-CHK-010 (P0): System confirms order and sends email  
11\. FR-CHK-011 (P2): User can save order as draft  
12\. FR-CHK-012 (P1): System validates inventory before confirming  
13\. NFR-CHK-001 (P0): Checkout process completes in \<30 seconds  
14\. NFR-CHK-002 (P1): Payment data encrypted (PCI-DSS compliant)  
15\. NFR-CHK-003 (P2): Mobile responsive design

**Your Deliverables:**

**A) Complete RTM Spreadsheet**

* Professional formatting  
* All 15 requirements  
* Minimum 50 test cases total  
* All necessary columns  
* Sample execution data (80% executed)  
* Sample results (90% pass rate for executed)  
* 5-8 linked defects  
* Color coding  
* Formulas for automatic calculations

**B) RTM Analysis Report** (4-5 pages) Include:

* Coverage analysis  
* Execution progress  
* Quality metrics  
* Gap identification  
* Risk assessment  
* Defect analysis  
* Recommendations  
* Next steps

**C) Requirements Coverage Chart** Create visual representations:

* Coverage by priority  
* Execution status pie chart  
* Pass/fail trend  
* Module-wise coverage

**D) Traceability Diagram** Show:

* Requirements → Scenarios → Test Cases → Defects  
* Forward and backward traceability  
* Visual representation

---

**2\. RTM for Real Application**

Choose a real application (Amazon, Netflix, Gmail, etc.)

**Pick one feature** (e.g., Amazon Shopping Cart)

**Your Tasks:**

**A) Reverse Engineer Requirements** (10-15 requirements)

* Identify what requirements likely existed  
* Write them in proper format with IDs  
* Prioritize them

**B) Create Test Scenarios**

* 3-5 scenarios per requirement

**C) Write Test Case IDs**

* Minimum 40 test cases total  
* Descriptive naming convention

**D) Build Complete RTM**

* Professional spreadsheet  
* All columns  
* Simulated execution data

**E) Analysis Report**

* What coverage would be ideal?  
* What risks exist?  
* What additional test cases needed?

---

**3\. RTM Template Creation**

Create 3 professional RTM templates:

**Template 1: Agile Project RTM**

* User story based  
* Sprint-focused  
* Lightweight but complete

**Template 2: Waterfall Project RTM**

* Comprehensive  
* Detailed traceability  
* All columns

**Template 3: Regulatory/Compliance RTM**

* Audit-ready  
* Regulatory requirement tracking  
* Sign-off columns  
* Evidence columns

Each template must:

* Be professional and polished  
* Include instructions  
* Have sample data  
* Include formulas  
* Be immediately usable

---

**4\. RTM Best Practices Guide**

Write a comprehensive guide (8-10 pages):

**Title: "Requirements Traceability Matrix \- Complete Guide"**

**Include:**

1. What is RTM and why it matters  
2. When to create RTM  
3. How to create RTM (step-by-step)  
4. RTM structure and columns  
5. Best practices (20+ tips)  
6. Common mistakes (10+ mistakes to avoid)  
7. Tools comparison  
8. Metrics to track  
9. Reporting techniques  
10. Real-world examples (3-4 examples)  
11. Templates (include 2-3 templates)  
12. Interview questions on RTM

Make it comprehensive enough to be used as training material.

---

### **📚 RESOURCES**

**Templates:**

* RTM Excel Template (download)  
* RTM Google Sheets Template  
* Requirements Coverage Report Template

**Reading:**

* "Requirements Traceability Matrix" \- Software Testing Help  
* "How to Create RTM" \- Guru99  
* IEEE 830 Standard (Requirements Traceability section)

**Tools:**

* Excel/Google Sheets (basic RTM)  
* TestRail (Test management with RTM)  
* JIRA \+ Zephyr (Traceability)  
* HP ALM (Enterprise RTM)  
* TestLink (Open source)

**Videos:**

* "RTM Tutorial" \- Search on YouTube  
* "Creating Traceability Matrix in Excel"  
* "Test Management Tools Demo"

**Practice:**

* Create RTM for sample projects  
* Analyze RTMs from real projects (search online)  
* Practice calculating coverage metrics

