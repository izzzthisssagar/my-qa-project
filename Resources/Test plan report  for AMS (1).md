**Test Plan**   
**for**   
**Attendance Management System**

**![][image1]**

**Version:** 1.0  
**Date:** October 30, 2025  
**Prepared By:** Sagar Thapa  
**Project Manager/CTO:** Sandip Sharma

## **Table of Contents**

**1\. Project Overview**

**2\. Features to be Tested**

**3\. Test Levels and Types**

**4\. Test Platforms**

**5\. Test Environment**

**6\. Test Devices Requirements**

**7\. Entry and Exit Criteria**

**8\. Suspension Criteria**

**9\. Test Deliverables**

**10\. Test Estimation**

**11\. Roles and Responsibilities**

**12\. Test Schedule**

**13\. Assumptions**

**14\. Dependencies**

**15\. Risk Assessment**

**16\. Test References**

**17\. Key Testing Focus Areas**

**18\. Approval**

**19\. Revision History**

**20\. Appendix A: Test Case Template**

**21\. Appendix B: Bug Report Template**

**22\. Appendix C: Notification Test Scenarios**

**23\. Appendix D: Auto-Refresh Test Scenarios**

**24\. Appendix E: Excel Export Test Scenarios**

**25\. Appendix F: Mock Test Attendance Test Scenarios**

**26\. Appendix G: Test Data Requirements**

**27\. Appendix H: Communication Plan**

**28\. Appendix I: Success Metrics**

**29\. Appendix J: Glossary**	

## 

## **1\. Project Overview**

### **1.1 Project Description**

The Attendance Management System is an automated web-based application developed for Grace Consultancy to manage and track student attendance across different course sections (SAT, IELTS, PTE, Duolingo,). The system provides intelligent notification alerts, automated follow-up tracking, and role-based access control with real-time auto-refresh capabilities.

### **1.2 Technology Stack**

* **Frontend:** React (Developed by: Bimal, Rejina)

* **Backend:** NestJS (Developed by: Pravesh, Ganesh)

* **Database:** MySQL

* **UI/UX Design:** Nimisha, Sudha

* **Deployment:** Render (https://attendence-system-grace.onrender.com/)

### **1.3 Key Differentiators**

* **Automated Notification System:** Smart alerts based on attendance patterns

* **Real-time Auto-refresh:** Latest student updates without manual refresh

* **Automated Excel Export:** 45+ days attendance triggers automatic student data export

* **Mock Test Tracking:** Separate attendance system for SAT, IELTS, PTE mock tests

* **Fee Payment Alerts:** Automatic reminders after 3 consecutive days attendance

* **Test Booking Reminders:** Alerts after 45 consecutive days for test date booking

### **1.4 Scope of Testing**

This test plan covers functional, non-functional, automation, notification, usability, and compatibility testing for the Attendance Management System v1.0. Security testing will be handled separately by the cybersecurity intern team.

---

## **2\. Features to be Tested**

### **2.1 Core Features (Priority: High)**

#### *1\. User Authentication & Authorization*

* Login/Logout functionality

* Role-based access control (Super Admin, Ielts Admin, PTE Admin, SAT Admin, Duolingo Admin)

* Session management

* Password reset/forgot password

#### *2\. Student Management (CRUD Operations)*

* Create new student records

* View student details

* Update student information

* Delete student records


#### *3\. Basic Attendance Management*

* Mark student attendance (Present/Absent)

* View attendance records

* Edit attendance entries

* Attendance history/logs

* Date-wise attendance filtering

* Real-time attendance updates

#### *4\. **Mock Test Attendance (SAT, IELTS, PTE Only)*** 

* Separate mock test attendance marking

* Mock test attendance tracking

* Mock test performance records

* Mock test history and reports

* **Note:** Duolingo does NOT have mock test attendance

#### *5\. **Automated Notification System (Critical)***

**A. 3-Day Consecutive Attendance Alert:**

* System detects when student attends 3 consecutive days

* Automatic message sent to student via WhatsApp, Gmail/Email

* Alert message: “Payment reminder for \[Respective Section\] fees”

* Fee payment link/details included

* Notification log maintained

**B. 45-Day Consecutive Attendance Alert:**

* System detects 45 consecutive attendance days

* Automatic message sent to student via WhatsApp, Gmail/Email

* Alert message: “Time to book your \[SAT/IELTS/PTE/etc.\] test date”

* Test booking portal link included

* Reminder for test preparation completion

**C. Notification Channels:**

* SMS alerts (if integrated)

* Email notifications (already integrated)

* Whatsapp message(if integrated)

#### *6\. **Auto-Refresh Functionality (Critical)***

* Real-time data updates without manual refresh

* Live attendance status updates

* Auto-update student list

* Auto-update dashboard statistics

* WebSocket/polling mechanism

* Refresh interval configuration

* Latest student data always visible

#### *7\. **Automated Excel Export System***

* Auto-trigger when student reaches 45+ days attendance

* Student data exported to Excel file

* Export includes: Name, contact, section, total attendance, preferences

* “Future Follow-up” sheet created

* Tracks student preferences (country choices, course completion goals)

* Export stored in designated folder/cloud

* Admin notification when export is generated

* Download/view exported files

#### *8\. Role-Based Dashboards*

* Super Admin Dashboard (all sections access)

* Section Admin Dashboard (SAT, IELTS, PTE, Duolingo)

* Student Profile Section to view their details, attendance track, update and delete

* Dashboard analytics and real-time statistics

* Auto-refreshing dashboard data

#### *9\. Section/Course Management*

* SAT section management

* IELTS section management

* PTE section management

* Duolingo section management

* Section-wise student assignment

#### *10\. Reports & Analytics*

* Attendance reports (daily, weekly, monthly)

* Student-wise attendance summary

* Section-wise attendance reports

* Mock test performance reports (SAT, IELTS, PTE)

* Consecutive attendance tracking

* Auto-exported Excel reports

* Export reports (PDF/Excel)

### **2.2 Features NOT to be Tested**

* Security vulnerabilities (handled by cybersecurity team)

* SMS gateway integration (verify functionality only if implemented)

* WhatsApp API integration (verify functionality only if implemented)

* Email server configuration (verify functionality only)

* Backend API unit tests (handled by backend team)

Tracker

Account section \- paid /unpaid

---

## **3\. Test Levels and Types**

### **3.1 Test Levels**

* **System Testing:** Complete end-to-end functionality testing

* **Integration Testing:**

  * Frontend-Backend integration (React ↔ NestJS)

  * Notification system integration

  * Auto-refresh mechanism integration

  * Excel export automation integration

* **User Acceptance Testing (UAT):** Validation with actual users/stakeholders

* **Regression Testing:** After bug fixes and new feature additions

### **3.2 Testing Types**

#### *Functional Testing*

* **Functional Testing:** Verify all features work as per requirements

* **CRUD Testing:** All Create, Read, Update, Delete operations

* **Notification Testing:** All automated alerts and notifications

* **Automation Testing:** Auto-refresh, auto-export, auto-alerts

* **Positive Testing:** Valid input scenarios

* **Negative Testing:** Invalid input scenarios, boundary values

* **Smoke Testing:** Basic functionality verification after deployment

* **Sanity Testing:** Quick verification of specific functionality after bug fixes

* **Regression Testing:** Ensure existing functionality remains intact

* **Business Logic Testing:** 3-day alert, 45-day alert, Excel export triggers

#### *Non-Functional Testing*

* **Real-time Performance Testing:** Auto-refresh responsiveness

* **Responsiveness Testing:** Mobile, Tablet, Laptop, Desktop compatibility

* **Performance Testing:** Page load times, response times

* **Load Testing:** System behavior under expected user load

* **Stress Testing:** System behavior under peak load conditions

* **Notification Delivery Testing:** Alert sending speed and reliability

* **Data Synchronization Testing:** Real-time data consistency

* **Usability Testing:** UI/UX, navigation, user-friendliness

* **Compatibility Testing:** Cross-browser and cross-device testing


#### *Automation & Integration Testing*

* **Auto-refresh Mechanism Testing**

* **Notification Trigger Testing(WhatsApp, Gmail, SMS)**

* **Excel Auto-export Testing**

* **Consecutive Days Calculation Testing**

* **Background Job/Cron Job Testing** (if applicable)

* **WebSocket/Polling Testing** (for real-time updates)

#### *Other Testing Types*

* **Ad-hoc Testing:** Random exploration without test cases

* **Exploratory Testing:** Unscripted testing to discover defects

---

## **4\. Test Platforms**

### **4.1 Application Type**

* Web Application (Responsive Design with Real-time Updates)

* URL: https://attendence-system-grace.onrender.com/

### **4.2 Access Platforms**

* Desktop/Laptop

* Tablet (iPad, Android Tablets)

* Mobile (iOS, Android)

---

## **5\. Test Environment**

### **5.1 Server Environments**

| Environment | Purpose | URL | Responsible Team |
| :---- | :---- | :---- | :---- |
| Development | Developer testing | To be provided | Backend: Pravesh, Ganesh |
| QA/Testing | QA team testing | https://attendence-system-grace.onrender.com/ | QA Team |
| UAT | User acceptance testing | To be confirmed | All Teams |
| Production | Live environment | To be confirmed | DevOps/Backend |

### **5.2 Operating Systems**

* **Desktop/Laptop:**

  * Windows 10/11

  * macOS (Latest version)

  * Linux Ubuntu (if applicable)

* **Mobile:**

  * iOS 15+ (iPhone)

  * Android 11+ (Various devices)

### **5.3 Browsers**

| Browser | Versions | Priority |
| :---- | :---- | :---- |
| Google Chrome | Latest 3 versions | High |
| Mozilla Firefox | Latest 2 versions | High |
| Safari | Latest 2 versions | High |
| Microsoft Edge | Latest 2 versions | Medium |
| Mobile Safari (iOS) | Latest version | High |
| Chrome Mobile (Android) | Latest version | High |

### **5.4 Network Conditions**

* Wi-Fi (High-speed internet)

* Mobile Data (4G/5G)

* LAN (Ethernet)

* Slow network simulation (3G) for auto-refresh testing

---

## **6\. Test Devices Requirements**

### **6.1 Desktop/Laptop Devices**

| Device Type | OS | Screen Resolution | Browser |
| :---- | :---- | :---- | :---- |
| Laptop | Windows 11 | 1920x1080 | Chrome, Firefox, Edge |
| MacBook | macOS | 1440x900 | Chrome, Safari |
| Desktop | Windows 10 | 1920x1080 | Chrome, Firefox |

### **6.2 Mobile Devices**

| Device Type | Model | OS Version | Screen Size |
| :---- | :---- | :---- | :---- |
| iPhone | iPhone 12/13/14 | iOS 15+ | Various |
| Android | Samsung Galaxy S21/S22 | Android 11+ | Various |
| Android | Google Pixel 6/7 | Android 12+ | Various |

### **6.3 Tablet Devices**

| Device Type | Model | OS Version | Screen Size |
| :---- | :---- | :---- | :---- |
| iPad | iPad Air/Pro | iOS 15+ | 10.9“/12.9“ |
| Android Tablet | Samsung Galaxy Tab | Android 11+ | 10.1“/11“ |

---

## **7\. Entry and Exit Criteria**

### **7.1 Entry Criteria**

The following conditions must be met before testing begins:

* Test environment is set up and accessible

* Application is deployed on the test server

* Frontend components developed by Bimal and Rejina are integrated

* Backend APIs developed by Pravesh and Ganesh are functional

* UI/UX designs by Nimisha and Sudha are implemented

* Test data is prepared and available

* Test cases are reviewed and approved

* Required test devices are available

* Notification system is configured

* Auto-refresh mechanism is implemented

* Excel export functionality is ready

* Database is configured with test data

* Test user accounts with different roles are created

* Mock test attendance module ready for SAT, IELTS, PTE

### **7.2 Exit Criteria**

Testing will be considered complete when:

* All planned test cases have been executed

* 95% of critical and high-priority test cases pass

* **Notification system:** All alert scenarios tested and working

* **Auto-refresh:** Real-time updates verified on all pages

* **Excel export:** Automated export tested and functional

* **Mock test attendance:** Verified for SAT, IELTS, PTE sections

* All critical (P0) and high (P1) severity bugs are fixed and verified

* Medium (P2) severity bugs are evaluated and decision is made

* Low (P3) severity bugs are documented for future releases

* Regression testing is completed successfully

* Performance benchmarks are met (page load \< 3 seconds, auto-refresh \< 2 seconds)

* Responsiveness is verified across all target devices

* Notification delivery success rate \> 95%

* Consecutive attendance calculation accuracy: 100%

* Test summary report is prepared and reviewed

* UAT sign-off is obtained from stakeholders

* All test deliverables are submitted

 

---

## **8\. Suspension Criteria**

Testing will be suspended if any of the following occurs:

1. **Critical Environment Issues:**

   * Test environment/server is down or inaccessible

   * Database connectivity issues

   * Application is not loading or crashing frequently

   * Auto-refresh mechanism completely broken

2. **High Defect Density:**

   * More than 70% of test cases fail in a module

   * Multiple critical (P0) bugs are discovered that block testing

   * Notification system not sending any alerts

3. **Blockers:**

   * Critical features not implemented (notification system, auto-refresh)

   * Test data cannot be created due to application issues

   * API integration failures blocking frontend testing

   * Excel export functionality not working

4. **Resource Issues:**

   * Test devices are unavailable

   * Required test user accounts are not working

   * Build deployment delays from frontend/backend team

5. **Dependency Issues:**

   * Backend services (Pravesh, Ganesh) are not available

   * Frontend issues (Bimal, Rejina) blocking testing

   * Third-party integrations are failing (SMS/Email gateway)

   * Notification service down

**Resumption:** Testing will resume once the blocking issues are resolved and verified by respective teams.

---

## **9\. Test Deliverables**

### **9.1 Test Planning Deliverables**

* ✅ Test Plan Document (this document)

* Test Strategy Document (if required)

### **9.2 Test Design Deliverables**

* Test Scenarios Document

* Test Cases Document (Excel/Google Sheets)

* Notification Test Cases

* Auto-refresh Test Cases

* Excel Export Test Cases

* Mock Test Attendance Test Cases

* Test Data Requirements

* Traceability Matrix (Requirements to Test Cases)

### **9.3 Test Execution Deliverables**

* Test Execution Report (Daily/Weekly)

* Bug Reports (GitLab/Jira)

* Test Case Execution Status

* Screenshots/Screen recordings of defects

* Notification Testing Report

* Auto-refresh Performance Report

* Excel Export Verification Report

* Mock Test Attendance Report

### **9.4 Test Closure Deliverables**

* Test Summary Report

* Bug Metrics Report

* Test Coverage Report

* Lessons Learned Document

* Responsiveness Testing Report

* Performance/Load Testing Report

* Notification System Testing Report

* Auto-refresh Functionality Report

* Excel Export Automation Report

* UAT Sign-off Document

## **10\. Test Estimation**

### **10.1 Feature-wise Estimation**

| Module/Feature | Test Cases (Est.) | Test Design (Days) | Test Execution (Days) | Total (Days) |
| :---- | :---- | :---- | :---- | :---- |
| User Authentication | 20-30 |  |  |  |
| Student Management (CRUD) | 40-50 |  |  |  |
| Basic Attendance Management | 20-30 |  |  |  |
| Mock Test Attendance (SAT/IELTS/PTE) | 20-30 |  |  |  |
| Automatic Notification System | 30-40 |  |  |  |
| Auto-Refresh Functionality | 20-25 |  |  |  |
| Automated Excel Export (45+ days) | 20-25 |  |  |  |
| Role-Based Dashboards | 30-40 |  |  |  |
| Section Management | 30-35 |  |  |  |
| Reports & Analytics | 30-35 |  |  |  |
| Responsiveness Testing | 10-20 |  |  |  |
| Cross-Browser Testing | 10-20 |  |  |  |
| Performance Testing | 10-20 |  |  |  |
| Integration Testing | 10-20 |  |  |  |
| Regression Testing | All above |  |  |  |
| Bug Retesting | As needed |  |  |  |
| UAT Support | \- |  |  |  |
| **TOTAL** |  |  |  |  |

### **10.2 Effort Breakdown**

* **Test Planning:** 1 days

* **Test Design:** 4

* **Test Execution:**  8days

* **Defect Management:** 3 days (included in execution)

* **Reporting:** 2 days

* **Buffer (20%):** 2days

* **Total Estimated Effort:**  20 working days (2-3weeks)

**Note:** Estimation increased due to:

* Complex notification system testing

* Auto-refresh mechanism verification

* Excel automation testing

* Mock test attendance module

* Real-time data synchronization testing

* Multiple alert trigger scenarios

---

## **11\. Roles and Responsibilities**

### **11.1 Development Team**

| Role | Name | Responsibilities |
| :---- | :---- | :---- |
| **Frontend Developers** | Bimal, Rejina | \- Develop React components \- Implement UI/UX designs \- Fix frontend bugs \- Implement auto-refresh mechanism \- Integrate with backend APIs \- Support testing activities \- Fix reported frontend bugs |
| **Backend Developers** | Pravesh, Ganesh | \- Develop NestJS APIs \- Implement notification logic \- Build Excel export automation \- Configure database \- Fix backend bugs \- Provide API documentation \- Deploy builds to test environment \- Support integration testing |
| **UI/UX Designers** | Nimisha, Sudha | \- Create design mockups \- Design user flows \- Provide design specifications \- Support usability testing \- Verify design implementation \- Update designs based on feedback |
| **Project Manager/CTO** | Synthbit CTO | \- Approve test plan \- Review test progress \- Prioritize defects \- Sign-off on releases \- Stakeholder communication \- Resource allocation |
| **Security Testing** | Cybersecurity Team | \- Perform security testing \- Vulnerability assessment \- Security compliance testing |

### **11.2 QA Team**

| Role | Name | Responsibilities |
| :---- | :---- | :---- |
| **QA Lead/Manual Tester** |  | \- Create test plan and test cases \- Execute manual testing \- Test notification system \- Verify auto-refresh functionality  \- Test Excel export automation \- Test mock test attendance \- Report and track bugs \- Perform responsiveness testing \- Coordinate with development teams \- Verify consecutive days calculation \- Test real-time data updates \- Prepare test reports \- UAT coordination |

## **12\. Test Schedule**

### **12.1 Tentative Timeline**

*(To be finalized with project manager)* 

| Phase | Activities | Duration | Responsible | Status |
| :---- | :---- | :---- | :---- | :---- |
| **Phase 1: Planning** | Test plan creation, review, approval | 2 days | QA Team | Under Review |
| **Phase 2: Design** | Test scenario and test case design |  | QA Team | In Progress |
| **Phase 3: Preparation** | Test environment setup, test data creation |  | QA \+ Backend | Pending |
| **Phase 4: Execution \- Round 1** | First cycle of testing (Core features) |  | QA Team | Pending |
| **Phase 5: Notification Testing** | 3-day alert, 45-day alert, SMS/email testing |  | QA Team | Pending |
| **Phase 6: Auto-refresh Testing** | Real-time updates, data sync testing |  | QA Team | Pending |
| **Phase 7: Excel Export Testing** | Automated export verification |  | QA Team | Pending |
| **Phase 8: Bug Fixing \- Round 1** | Developer fixes bugs |  | Dev Team | Pending |
| **Phase 9: Execution \- Round 2** | Regression and retest |  | QA Team | Pending |
| **Phase 10: Performance Testing** | Load, stress, auto-refresh performance |  | QA Team | Pending |
| **Phase 11: Bug Fixing \- Round 2** | Critical bug fixes |  | Dev Team | Pending |
| **Phase 12: Final Regression** | Complete regression testing |  | QA Team | Pending |
| **Phase 13: UAT** | User acceptance testing |  | QA \+ Stakeholders | Pending |
| **Phase 14: Closure** | Final reporting and sign-off |  | QA Team | Pending |

**Total Duration:** \~

### **12.2 Milestones**

* **Milestone 1:** Test Plan Approval \- 

* **Milestone 2:** Test Cases Ready \-

* **Milestone 3:** First Test Cycle Complete \-

* **Milestone 4:** Notification System Testing Complete \- 

* **Milestone 5:** Auto-refresh & Excel Export Testing Complete \- 

* **Milestone 6:** Regression Complete \- 

* **Milestone 7:** UAT Sign-off \- 

## **13\. Assumptions**

### **13.1 Environment & Access**

* Test environment will be available throughout the testing period

* Test user accounts for all roles will be provided

* Test data can be created, modified, and deleted without restrictions

* Notification system (SMS/Email/Whatsapp) is configured and working

* Excel export folder/cloud storage is accessible

### **13.2 Resources**

* All required test devices (mobile, tablet, laptop) will be available

* Necessary browser versions will be accessible

* Internet connectivity will be stable for auto-refresh testing

* Access to notification logs/history

### **13.3 Development Team Availability**

* **Frontend Team (Bimal, Rejina):** Available for clarifications and bug fixes

* **Backend Team (Pravesh, Ganesh):** Available for API support and bug fixes

* **UI/UX Team (Nimisha, Sudha):** Available for design verification

* Bug fixes will be deployed to test environment within 2-3 days

* No major requirement changes during testing phase

### **13.4 Feature Assumptions**

* **Notification System:**

  * SMS/Email/Whatsapp gateway is integrated and functional

  * 3-day alert triggers automatically without manual intervention

  * 45-day alert triggers automatically

  * Notification templates are finalized

* **Auto-refresh:**

  * Real-time updates work via WebSocket or polling mechanism

  * Refresh interval is configurable

  * No manual page refresh needed

* **Excel Export:**

  * Export triggers automatically at 45+ days attendance

  * Export format is standardized

  * Files are stored securely and accessible

* **Mock Test Attendance:**

  * Only SAT, IELTS, PTE have mock test tracking

  * Duolingo do NOT have mock test attendance

* **Consecutive Days Calculation:**

  * System accurately calculates consecutive attendance

  * Weekends/holidays handling is defined

  * Reset logic is clear

### **13.5 Testing Assumptions**

* Security testing will be conducted separately

* Performance baseline: System should handle ( ) concurrent users

* Page load time should be under 3 seconds

* Auto-refresh latency should be under 2 seconds

* Notification delivery success rate target: 95%

* Excel export generation time: under 5 seconds

### **13.6 Communication**

* Bugs will be reported in whatsapp group

* Daily standup with dev teams

* Weekly status reports to CTO

* Critical issues communicated immediately via Slack/Teams

---

## **14\. Dependencies**

### **14.1 Internal Dependencies**

**Frontend Team (Bimal, Rejina):**

* Timely implementation of UI components

* Auto-refresh mechanism implementation

* Real-time data display

* Responsive design implementation

* Bug fixes within agreed timelines

* Integration with backend APIs

**Backend Team (Pravesh, Ganesh):**

* API development and deployment

* Notification system implementation

* Excel export automation

* Consecutive days calculation logic

* Database configuration

* Bug fixes and performance optimization

* API documentation availability

**UI/UX Team (Nimisha, Sudha):**

* Final design specifications

* Design assets and mockups

* Usability testing participation

* Design feedback and iterations

**Project Management:**

* Approval of test plan and test cases

* Prioritization of bugs

* UAT coordination with end users

* Resource allocation

* Timeline management

**Infrastructure:**

* Stable test environment

* Database accessibility

* Server uptime and performance

* Notification service availability

### **14.2 External Dependencies**

**Third-party Services:**

* Hosting service availability ()

* SMS gateway service (if integrated)

* Email service (if integrated)

* Internet connectivity

* Cloud storage for Excel exports

**Stakeholders:**

* Availability for UAT

* Timely feedback and approvals

* Requirement clarifications

* Test date booking system (if external)

---

## **15\. Risk Assessment**

| \# | Risk | Impact | Probability | Mitigation Strategy | Owner |
| :---- | :---- | :---- | :---- | :---- | :---- |
| 1 | **Notification system failure** | Critical | Medium | \- Test with mock notifications first.  \- Have fallback notification mechanism  \- Verify SMS/Email gateway configuration early | Backend Team  |
| 2 | **Auto-refresh not working** | High | Medium | \- Early prototype testing  \- Test on different browsers  \- Have manual refresh option as backup | Frontend Team |
| 3 | **Excel export automation fails** | High | Medium | \- Manual export option available \- Test with various data volumes \- Verify file permissions early | Backend Team |
| 4 | **Consecutive days calculation error** | Critical | Low | \- Thorough unit testing by backend \- Multiple test scenarios \- Edge case testing (weekends, holidays) | Backend Team |
| 5 | **Environment downtime** | High | Medium | \- Maintain backup test environment \- Coordinate deployment schedules \- Test during stable hours | Infrastructure |
| 6 | **Frontend-Backend integration issues** | High | Medium | \- Regular integration testing-  API documentation up-to-date \- Coordination between Bimal/Rejina and Pravesh/Ganesh | All Dev Teams |
| 7 | **Limited test devices** | Medium | Low | \- Prioritize critical devices \- Use browser dev tools \- Borrow devices if needed | QA Team |
| 8 | **High defect density** | High | Medium | \- Focus on critical features first \- Early smoke testing \- Continuous communication with dev teams | QA \+ Dev Teams |
| 9 | **Delayed bug fixes** | High | Medium | \- Prioritize P0/P1 bugs clearly \- Continue testing unblocked features \- Escalate to CTO | Project Manager |
| 10 | **Mock test attendance confusion** | Medium | Low | \- Clear documentation \- Only SAT, IELTS, PTE have mock tests \- Proper labeling in UI | Frontend \+ QA |
| 11 | **Performance issues with auto-refresh** | High | Medium | \- Load testing early \- Optimize refresh interval \- Monitor server resources | Backend \+ QA |
| 12 | **UI/UX design changes** | Medium | Medium | \- Freeze designs before testing \- Change control process \- Impact assessment for changes | UI/UX \+ PM |
| 13 | **Single QA resource** | High | Low | \- Detailed documentation \- Knowledge sharing \- Unplanned leave contingency | QA Team |
| 14 | **Scope creep** | Medium | Medium | \- Follow change control process \- Assess impact on timeline \- Formal approvals for changes | Project Manager |
| 15 | **Real-time data sync issues** | High | Medium | \- Test network conditions \- Verify WebSocket stability \- Fallback to polling if needed | Backend Team |

### **15.1 Risk Response Plan**

* **Critical Impact \+ High Probability:** Immediate escalation to CTO, daily monitoring

* **High Impact \+ Medium Probability:** Weekly review, mitigation plan ready

* **Medium/Low Impact:** Monitor and document

---

## **16\. Test References**

### **16.1 Documents**

* System Requirements Specification (SRS) \- *\[To be provided\]*

* API Documentation \- *\[To be provided by Pravesh, Ganesh\]*

* Database Schema \- *\[To be provided by Backend team\]*

* User Stories/Backlog \- *\[To be provided\]*

* UI/UX Designs \- *\[To be provided by Nimisha, Sudha\]*

* Wireframes/Mockups \- *\[From Nimisha, Sudha\]*

* Notification Templates \- *\[To be provided\]*

* Excel Export Format Specification \- *\[To be provided\]*

* User Manual (if available)

### **16.2 URLs**

* **Application URL:** https://attendence-system-grace.onrender.com/

* **API Documentation:** *\[To be provided by backend team\]*

* **Test Case Repository:** *\[To be provided\]*

* **Design Repository:** *\[To be provided by UI/UX team\]*

### **16.3 Standards & Guidelines**

* Web Content Accessibility Guidelines (WCAG) 2.1	

* Responsive Web Design Best Practices

* Browser Compatibility Standards

* Real-time Application Testing Standards

## **17\. Key Testing Focus Areas**

### **17.1 Critical Features Requiring Extra Attention**

**1\. Notification System (Priority: Critical)**

* 3-day consecutive attendance alert accuracy

* 45-day consecutive attendance alert accuracy

* Notification delivery success rate

* SMS/Email/Whatsapp content verification

* Notification timing and triggers

* Notification history and logs

**2\. Auto-Refresh Mechanism (Priority: Critical)**

* Real-time data updates

* Update frequency and performance

* Cross-browser compatibility

* Network interruption handling

* Data consistency during refresh

**3\. Excel Export Automation (Priority: High)**

* Trigger at exactly 45+ days

* Data accuracy in export

* File format and structure

* Admin notification

* Storage and accessibility

**4\. Mock Test Attendance (Priority: High)**

* Only for SAT, IELTS, PTE

* Separate from regular attendance

* Proper UI distinction

* Accurate tracking and reporting

**5\. Consecutive Days Calculation (Priority: Critical)**

* Accurate day counting

* Weekend/holiday handling

* Reset scenarios

* Edge cases (gaps, late attendance)

---

## **18\. Approval**

This test plan requires approval from the following stakeholders:

| Role | Name | Signature(yes/no) | Date |
| :---- | :---- | :---- | :---- |
| QA  | Sagar |  |  |
| Project Manager/CTO | Sandip |  |  |
| Frontend Lead | Bimal / Rejina |  |  |
| Backend Lead | Pravesh / Ganesh | Ganesh Thapa |  |
| UI/UX Lead | Nimisha / Sudha |  |  |

## **19\. Revision History**

| Version | Date | Author | Changes |
| :---- | :---- | :---- | :---- |
| 1.0 | October 29, 2025 | Sagar Thapa | Initial test plan created with updated requirements |
|  |  |  | \- Added 3-day notification alert feature |
|  |  |  | \- Added 45-day notification alert feature |
|  |  |  | \- Added auto-refresh functionality |
|  |  |  | \- Added automated Excel export (45+ days) |
|  |  |  | \- Added mock test attendance for SAT, IELTS, PTE |
|  |  |  | \- Updated team roles and responsibilities |
|  |  |  | \- Updated test estimation and timeline |

## **20\. Appendix A: Test Case Template**

Test Case ID: TC\_\[Module\]\_\[Priority\]\_\[Number\]  
Test Case Title: \[Brief description\]  
Module: \[Module name\]  
Priority: \[P0-Critical/P1-High/P2-Medium/P3-Low\]  
Test Type: \[Positive/Negative/Functional/etc.\]  
Prerequisites: \[Any setup needed\]  
Test Data: \[Data required\]  
Test Steps:  
1\. \[Step 1\]  
2\. \[Step 2\]  
3\. \[Step 3\]  
Expected Result: \[What should happen\]  
Actual Result: \[To be filled during execution\]  
Status: \[Pass/Fail/Blocked/Skip\]  
Executed By: \[QA Name\]  
Execution Date: \[Date\]  
Comments: \[Any notes\]

---

## **21\. Appendix B: Bug Report Template**

Bug ID: BUG\_\[Module\]\_\[Number\]  
Title: \[Brief description\]  
Module: \[Module name\]  
Severity: \[Critical/High/Medium/Low\]  
Priority: \[P0/P1/P2/P3\]  
Environment: \[Browser, OS, Device\]  
Reported By: \[Your name\]  
Assigned To: \[Developer name \- Bimal/Rejina/Pravesh/Ganesh\]  
Steps to Reproduce:  
1\. \[Step 1\]  
2\. \[Step 2\]  
3\. \[Step 3\]  
Expected Result: \[What should happen\]  
Actual Result: \[What actually happened\]  
Attachments: \[Screenshots/Videos\]  
Reported Date: \[Date\]  
Status: \[New/Open/In Progress/Fixed/Closed/Reopen\]  
Comments: \[Additional information\]

---

## **22\. Appendix C: Notification Test Scenarios**

### **Critical Test Scenarios for Notification System**

**Scenario 1: 3-Day Consecutive Attendance Alert**

Prerequisites: Student has attended 0 days  
Test Steps:  
\- Day 1: Mark student Present  
\- Day 2: Mark student Present    
\- Day 3: Mark student Present  
Expected: Notification/SMS sent immediately after Day 3 attendance  
Verify: Fee payment reminder message sent

**Scenario 2: 45-Day Consecutive Attendance Alert**

Prerequisites: Student has 44 consecutive attendance days  
Test Steps:  
\- Mark student Present on Day 45  
Expected: Notification/SMS sent for test date booking  
Verify: Test booking reminder message sent with portal link

**Scenario 3: Consecutive Attendance Break**

Prerequisites: Student has 2 consecutive days, 43 consecutive days  
Test Steps:  
\- Mark student Absent on Day 3, Day 44  
Expected: 3-day alert NOT sent, 45-day alert NOT sent  
Verify: Counter resets, consecutive days \= 0

---

## **23\. Appendix D: Auto-Refresh Test Scenarios**

### **Critical Test Scenarios for Auto-Refresh**

**Scenario 1: Real-time Attendance Update**

Setup: Two browsers \- Admin marks attendance, Student views  
Test Steps:  
1\. Admin (Browser 1): Mark student Present  
2\. Student (Browser 2): Dashboard should auto-update  
Expected: Student sees updated attendance without manual refresh  
Verify: Update appears within 2-3 seconds

**Scenario 2: Multiple Users Concurrent Updates**

Setup: Multiple admins updating different students  
Test Steps:  
1\. Admin A marks Student 1 Present  
2\. Admin B marks Student 2 Absent  
3\. Both dashboards should reflect changes  
Expected: All updates visible to all users in real-time  
Verify: No data conflicts or lost updates

**Scenario 3: Network Interruption Handling**

Test Steps:  
1\. Disconnect internet briefly  
2\. Reconnect after 10 seconds  
Expected: Auto-refresh resumes automatically  
Verify: Latest data loaded after reconnection

---

## **24\. Appendix E: Excel Export Test Scenarios**

### **Critical Test Scenarios for Excel Export**

**Scenario 1: Automatic Export at 45 Days**

Prerequisites: Student has 44 attendance days  
Test Steps:  
1\. Mark student Present (Day 45\)  
2\. Check if Excel export triggered  
Expected:   
\- Excel file auto-generated  
\- Contains student name, contact, section, preferences  
\- Admin receives notification  
\- File accessible in designated location

**Scenario 2: Export Data Accuracy**

Prerequisites: Multiple students at 45+ days  
Test Steps:  
1\. Verify all eligible students included  
2\. Check data accuracy in Excel  
Expected:  
\- All fields populated correctly  
\- "Future Follow-up" sheet created  
\- Student preferences captured  
\- No duplicate entries

**Scenario 3: Multiple Concurrent Exports**

Prerequisites: 5 students reach 45 days same day  
Test Steps:  
1\. Mark all 5 students Present  
Expected:  
\- All 5 students exported  
\- Separate records or single file with all data  
\- No data corruption  
\- Admin notified of all exports

---

## **25\. Appendix F: Mock Test Attendance Test Scenarios**

### **Critical Test Scenarios for Mock Test**

**Scenario 1: Mock Test Only for SAT, IELTS, PTE**

Test Steps:  
1\. Login as IELTS Admin \- Verify mock test option available  
2\. Login as PTE Admin \- Verify mock test option available  
3\. Login as SAT Admin \- Verify mock test option available  
4\. Login as Duolingo Admin \- Verify NO mock test option  
5\. Login as GRE Admin \- Verify NO mock test option  
Expected: Mock test attendance visible only for SAT, IELTS, PTE

**Scenario 2: Separate Mock Test Tracking**

Prerequisites: Student in IELTS section  
Test Steps:  
1\. Mark regular attendance as Present  
2\. Mark mock test attendance separately  
Expected:  
\- Both tracked independently  
\- Regular attendance ≠ mock test attendance  
\- Separate reports for each

**Scenario 3: Mock Test Performance Recording**

Test Steps:  
1\. Mark mock test attendance  
2\. Enter mock test score/performance  
3\. View mock test history  
Expected:  
\- Performance data saved  
\- Historical tracking available  
\- Reports show mock test progress

---

## **26\. Appendix G: Test Data Requirements**

### **Test User Accounts Needed**

**Super Admin:**

* Username: ( ) 

* Access: All sections, all features

**Section Admins:**

* SAT Admin: ( )

* IELTS Admin: ielts.admin@grace.com

* PTE Admin: ( )

* Duolingo Admin: ( )


**Students:**

* 5 students per section (25 total)

* Various attendance patterns for testing alerts

* Contact details for notification testing

### **Test Data Scenarios**

**For 3-Day Alert Testing:**

* Student A: 0 days → will reach 3 days

* Student B: 2 days → will reach 3 days

* Student C: 3 days → already triggered

* Student D: 2 days with 1 absence → will reset

**For 45-Day Alert Testing:**

* Student E: 43 days → will reach 45

* Student F: 44 days → will reach 45

* Student G: 45 days → already triggered

* Student H: 44 days with 1 absence → will reset

**For Excel Export Testing:**

* Student I: Exactly 45 days

* Student J: 46 days

* Student K: 50 days

* Student L: 100 days

**For Mock Test Testing:**

* SAT students: 3 students with mock test history

* IELTS students: 3 students with mock test history

* PTE students: 3 students with mock test history

---

## **27\. Appendix H: Communication Plan**

### **Daily Communication**

* **Daily Standup:** If possible 10:00 AM (15 minutes)

  * Attendees: QA, Bimal, Rejina, Pravesh, Ganesh

  * Agenda: Progress update, blockers, plan for the day

### **Weekly Communication**

* **Weekly Status Meeting:** If possible Every Monday 2:00 PM

  * Attendees: All team \+ CTO

  * Agenda: Test progress, bug status, upcoming tasks

  * 

* **Weekly Test Report:** Every Friday 5:00 PM

  * Sent to: Synthbit CTO

  * Content: Test execution summary, bug metrics, risks

### **Bug Communication**

* **Critical Bugs (P0):** Immediate notification via Slack/Teams

* **High Priority Bugs (P1):** Same day notification

* **Medium/Low Bugs (P2/P3):** Logged in Sheet, discussed in standup

### **Escalation Path**

1. **Level 1:** QA → Dev Team Lead (Bimal/Pravesh)

2. **Level 2:** Dev Team Lead → Project Manager/CTO

3. **Level 3:** Project Manager → Stakeholders

---

## **28\. Appendix I: Success Metrics**

### **Key Performance Indicators (KPIs)**

**Test Coverage:**

* Target: 95% requirement coverage

* Measure: (Tested requirements / Total requirements) × 100

**Test Execution:**

* Target: 100% test case execution

* Measure: (Executed test cases / Total test cases) × 100

**Defect Metrics:**

* Target: \< 10 critical bugs at release

* Measure: Total P0 bugs found and fixed

**Notification System:**

* Target: 95% notification delivery success

* Measure: (Successful notifications / Total triggers) × 100

**Auto-Refresh Performance:**

* Target: \< 2 seconds update latency

* Measure: Average time for data refresh

**Excel Export Accuracy:**

* Target: 100% accurate exports

* Measure: (Correct exports / Total exports) × 100

**Test Efficiency:**

* Target: 80% first-pass yield

* Measure: (Passed on first execution / Total test cases) × 100

**Bug Fix Rate:**

* Target: 90% bugs fixed within SLA

* Measure: (Bugs fixed on time / Total bugs) × 100

---

## **29\. Appendix J: Glossary**

**Terms and Definitions:**

* **Consecutive Days:** Continuous attendance without any absent/gap

* **3-Day Alert:** Automated notification after 3 consecutive attendance days

* **45-Day Alert:** Automated notification after 45 consecutive attendance days

* **Auto-Refresh:** Automatic page/data update without manual refresh

* **Mock Test:** Practice test attendance (SAT, IELTS, PTE only)

* **Excel Auto-Export:** Automated generation of Excel file at 45+ days attendance

* **Future Follow-up:** Tracking student preferences and goals after 45+ days

* **Real-time Update:** Immediate data synchronization across all users

* **Section Admin:** Administrator with access to specific section only

* **Super Admin:** Administrator with access to all sections and features

* **P0/P1/P2/P3:** Priority levels (Critical/High/Medium/Low)

* **WebSocket:** Real-time communication protocol for auto-refresh

* **Polling:** Regular server checking for data updates

---

**END OF TEST PLAN DOCUMENT**

---

## **Document Information**

##  **Total Sections:** 29 **Document Type:** Test Plan **Classification:** Internal Use **Distribution:** QA Team, Development Team, Project Management

**Prepared by:** QA Team  
**Reviewed by:**  
**Approved by:**  

**Next Review Date:**  After UAT completion  
**Document Location:** \[Project repository/shared drive\]

*This test plan is a living document and will be updated as needed throughout the project lifecycle.*

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGwAAABHCAYAAADiDaI4AAAEp0lEQVR4Xu2ZvUsjURDA/T9s/DdSWFvYW6QIXG1ho9hZBCwUQcTGj0JFDHIgCQh6CFpIgghRkIhgIsLmQCQiZA9CFhHmdpOYbGZmPyK74eaYgV/h5r2X7P72zZv3HBlNjYEihxF8Qfm3UWHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCUGHCGIqwqasqsGHsQYJpz5F5wZ17YVwlSXtKEk7ecM9elC9xezeTMHucg/xzFcymhbsCfFhgvleg9HAI6WXcN1qGIGwGzuv4DjvxeQ87c7g9j58weM3BFNOnj80LqOF+rvASltjNQbmBW3uFCfkDOkaUxC9sO+hBjdM+DL7CoArZgDd7+tbvV/DCEocFqH3iln7xHwibvfN/UKFmRypIWFBanPee5Z2gwnz6fFpgNV10pYoXtgLFpvtO7Qf7itez4NnhgIXV6uhFeDv1Fo9mufnHdP3VDiLsoAC0lQnFs3mYwOPbTKwuwFrxAjKb9LMoiVfY0Q30L9FVOMnRB2Fc+82ONkTYS4WO7SEez/KSgV8aRthlBTdpZYOwRVJcxCps7QlVVPULmE4tQh4v4q3rtL8bLMx8KEC5/xLUbmdIv1HyfRXIP+BXJqSw5g2shSyS4iI+YXN7UEIL9tcDTZMHVoPzbWYMF1TYIuwY/ddY8Ti12VsJ+v2MMNzvKxoVyO5Pkt83LGITlji7R3fqkkJSpf3p3TwZww0njP0OtIZgOaWzcXLNCSLMr+iww6rfw8kxv57FSUzCxskDdt7+2e7n66QYgUYB0mScHng8R9hoaovO4j7xqOjp7PvCCQtZ1n/UoJRfGJq4eIQt5wBnq/YD7rUh65s954pHzFgdeGFjsIG/yP1i4JlsbLWuhxXmkNg9BeMDt2aiYb8Mq7R/1MQibOoaV2HM/iRH06L1uELG+sJLGB2nl3qXHvs/Kf1qXx9EWIu5Gbtkr4AZONsqkIlZWgzCmKMou7paIu1oOmtVYaRdG09hOO11P0Np106HG52xBhbWxTlTPIVSHb9qrhjgfPQ7RC8s4CgqKL5mAcZbGJ1JrWoRzTzrab3b/vvCekzse6VKe5Yx7aMicmHcwxgoPN5QP2G0BK+ivZa9Pub8f+OgwlqsnpK1mk3/ERKxMJqeBg6PE3xfYVwJ7k63KCWHEra5DhuB+y28KXdCkjBSANjRrEH5d8UTg9wwf4LvL4weP7kDFzOhhHVmrflSgMzPH7Rsn0tCulil9yspJZISG4LPCdl/bjIn+EHCvNdOul0YRFg3PE/o+8Oytw5cSo+K6IQxR1F+B7JdmD0bd4IfKIyrTp1gKtRvCQsTksr6BHdYyp3tEfh/3eOZGSyM2//x7WIRVr+BjZhlOUQkLAnZV3wHXqfnFO5BY9lhhNHZyhcAoYTZTGyvQ/bhHsrvJli4hG+lSBOMZ3uNO0zGmgbdRCRMGRYqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBgqTBh/AX4gGyRzYVC5AAAAAElFTkSuQmCC>