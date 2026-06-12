

# **⭐ DAY 1 — Introduction to APIs, Client–Server & Industry Relevance**

---

## **🎯 Learning Objectives**

By the end of Day-1, students will clearly understand:

* What an API is (simple → professional → industry level)

* How **client–server architecture** works

* How an **API request → response** actually flows

* Types of APIs (REST, SOAP, GraphQL, WebSocket, Third-Party) with **Nepal examples**

* API URL structure with **proper labels/designations**

* What a QA tests in an API (status, body, headers, logic, errors, time, security)

  * where to **see it in Postman**

* First hands-on GET request using Postman

---

## **0\. Client–Server Architecture (Foundation Before APIs)**

Before talking about APIs, students must first understand **how apps talk to servers**.

### **⭐ 0.1 What is a Client?**

A **client** is anything that sends a request to a server.

**Examples:**

* Web browser (Chrome, Firefox)

* Mobile apps (Android / iOS)

* Desktop apps

* Frontend frameworks (React / Angular)

**Nepal Examples:**

* **Nagarik App** → client

* **Daraz App** → client

* **NIC Asia Mobile Banking** → client

* **LEC Student App / Web Portal** → client

---

### **⭐ 0.2 What is a Server?**

A **server** is a powerful machine (or service) that:

* Stores data

* Runs backend code

* Processes requests from clients

**Examples:**

* Node.js / Django / Laravel / Spring Boot backend

* MySQL / PostgreSQL / MongoDB database

**Nepal Examples:**

* **LEC backend** hosted on Render

* **E-Sewa transaction server**

* **Nepal Telecom recharge server**

* **Government education / exam portals**

---

### **⭐ 0.3 Client → Server → Client (Big Picture)**

          🧑‍💻 CLIENT (Frontend)  
  Mobile App / Web App / Desktop App  
                  |  
                  | 1️⃣ Sends Request (API)  
                  v  
          🌐 INTERNET / NETWORK  
                  |  
                  | 2️⃣ Request reaches backend  
                  v  
       🖥 SERVER (Backend \+ Database)  
   Node / Laravel / Spring Boot \+ MySQL

                  ^  
                  | 3️⃣ Sends Response (API)  
                  |  
           🧑‍💻 CLIENT shows result to user

**Nepal Scenario – NIC Asia Mobile Banking**

1. User opens **NIC Asia app** → this is the **client**.

2. User taps **“View Balance”**.

3. App sends API request to **NIC Asia backend server**.

4. Backend checks **core banking database**.

5. Server responds with JSON: current balance.

6. Client app shows “Your balance is रू X”.

---

## **1\. How API Request–Response Works (Step by Step)**

Once client–server is clear, now zoom into the **API level**.

STEP 1: Client prepares API request  
  \- Method (GET / POST / PUT / DELETE)  
  \- URL (endpoint)  
  \- Headers (Content-Type, Authorization, etc.)  
  \- Body (for POST/PUT/PATCH)

STEP 2: Server receives & processes  
  \- Validates input (required fields, formats)  
  \- Applies business logic (OTP valid? marks enough?)  
  \- Reads/writes database

STEP 3: Server sends response back  
  \- Status Code (200/201/400/401/500…)  
  \- Response Body (JSON / XML)  
  \- Response Headers

### **🔎 Where can students SEE this in Postman?**

* Top-left: **Method \+ URL**

* Tabs under URL:

  * **Params** → query parameters

  * **Headers** → request headers

  * **Body** → JSON body (for POST/PUT)

* After clicking **Send**:

  * Top-right of response → **Status code \+ Time**

  * Response **Body** tab → JSON/XML data

  * Response **Headers** tab → response headers

---

## **2\. What is an API?**

### **✔ Simple Definition**

API \= A **bridge** that allows two software systems to talk to each other.

### **✔ Professional Definition**

API (**Application Programming Interface**) is a set of rules that allows one application to interact with another using defined requests and responses.

### **✔ 2025 QA Standard Definition**

“API is a communication interface that transfers data between client and server in a structured, secure, and predictable way.”

---

## **3\. Why APIs Are Important (Real-World Uses)**

APIs power almost everything we use:

* Login systems (email/password → server validation)

* Payment gateways (Khalti, eSewa, Fonepay)

* E-commerce (Daraz search, add-to-cart, checkout)

* Banking integration (balance, statements, transfers)

* Attendance systems (QR scan → backend attendance)

* OTP verification (LEC login/registration)

* CMS document upload and verification

👉 **90%+ of modern applications depend on APIs.**

---

## **4\. API URL Structure (With Proper Designations)**

Example from your **LEC** project:

https://lec-backend-gva9.onrender.com/api/auth/verify-otp

Breakdown like a teacher:

| Part | Designation / Name | Meaning / How to Explain |
| ----- | ----- | ----- |
| `https://` | Protocol | Communication rule. `https` \= secure (encrypted). |
| `lec-backend-gva9.onrender.com` | Domain / Host | Address of backend server (like house address). |
| `/api` | Base Path | Says “this is API section”, not a normal web page. |
| `/auth` | Module / Resource | Group of APIs dealing with **authentication**. |
| `/verify-otp` | Endpoint / Action | Exact function → “verify user’s OTP”. |

💡 **Teaching trick**:  
 “URL is like an address:

* Country \= `https`

* City \= `lec-backend…`

* Building \= `/api`

* Floor \= `/auth`

* Room \= `/verify-otp`”

🔍 **QA angle when API fails (404/500)**:

* Check **domain** → is backend URL correct?

* Check **path/endpoint** → any typo?

* Check **method** → using POST instead of GET (or vice versa)?

---

## **5\. Types of APIs (With Nepal-Based Scenarios)**

# **⭐ TYPES OF API** 

**Types of API by Technology / Architecture**  
---

# **🔵 1\. REST API (Representational State Transfer)**

---

## **⭐ 1.1 Definition (Deep Explanation)**

Feature is the term used in manual testing to functionality  

Resource is the term used in api automation testing refers What data/entity exists on the server.

REST is a **software architectural style** where the server exposes “resources,” and the client interacts with these resources using **standard HTTP methods** (GET, POST, PUT, DELETE).

In REST:

* **Everything is treated as a resource**  
   Example: user, product, route, bus schedule, bank account, ticket, etc.

* Each resource is identified by a **URI** (Uniform Resource Identifier).  
   Example:  
   `/api/buses`, `/api/news/latest`, `/api/hospitals/nearby`

* The client interacts using HTTP **verbs**:

  * GET → retrieve resource

  * POST → create new resource

  * PUT/PATCH → update resource

  * DELETE → remove resource

* REST returns a “representation” of the resource, usually **JSON** in 2025\.

**Why “representational”?**  
 Because client doesn’t get the actual database record — it gets a **representation** of it (JSON).

---

## **⭐ 1.2 Why REST Exists (The Problem It Solves)**

Before REST became standard, APIs were inconsistent:

* Some used custom formats

* Some used SOAP

* Some used XML everywhere

* Some used custom verbs

* No universal rule

REST brought:

* **Predictable structure**

* **Uniform way of calling APIs**

* **Scalable and stateless model**

* **Easy debugging (curl, Postman)**

* **Frontend-friendly (React, Android, iOS)**

---

## **⭐ 1.3 REST Characteristics (Deep)**

Proxy \= **Middleman between client and server**

**Cache \= Temporary stored response**

### **CDN:**

**A CDN delivers cached content from the nearest edge server to reduce latency and server load.**

### **Load Balancer:**

**A load balancer distributes incoming traffic across multiple servers to ensure high availability.**

| Principle | Meaning | Why Important |
| ----- | ----- | ----- |
| **Client–Server** | Client UI separate from backend logic | Enables Android/React/web to share same backend |
| **Stateless** | Server doesn’t remember previous request | Scales massively; each request must include auth token |
| **Cacheable** | Responses can be cached if allowed | Speed boost for news, bus routes, weather |
| **Uniform Interface** | Consistent rules for accessing resources | Reduces complexity |
| **Layered System** | Client doesn’t know if request goes to server or proxy | Load balancers/CDNs work |

---

## **⭐ 1.4 Nepal Use Cases (Non–Your Project)**

### **1\. Nepal News Portals (REST)**

E.g., OnlineKhabar mobile app:

GET https://api.onlinekhabar.com/v1/top-news

* Client asks for latest news

* Server returns list in JSON

* Stateless, fast, cacheable

---

### **2\. Bus Route Finder App (REST)**

Imagine a real Nepali startup:

GET /api/buses/route?from=Lagankhel\&to=Kalanki

Returns:

* List of buses

* Ticket price

* Estimated arrival time

Perfect REST use-case.

---

### **3\. Cinema Ticket Booking (REST)**

POST /api/tickets/book

Client sends:

* MovieId

* ShowTime

* SeatNumber

Server returns booking confirmation.

## **⭐ 1.5 Pros**

* Best for **mobile/web applications**

* Very easy for QA to test (Postman)

* JSON is lightweight

* Scales to millions of users

## **⭐ 1.6 Cons**

* REST can be inefficient:

  * **Overfetching:** client gets more data than needed

  * **Underfetching:** client needs multiple API calls

Example:  
 To show restaurant \+ menu \+ rating on one screen, client might need **3 different APIs**.

---

# **🔵 2\. SOAP API (Simple Object Access Protocol)**

---

## **⭐ 2.1 Deep Definition**

SOAP is a **protocol** (not just style) that uses **XML** as the message format, following very strict rules.

SOAP has:

* Envelope

* Header

* Body

* Fault (for errors)

SOAP APIs are defined using **WSDL (Web Services Description Language)**, (WSDL defines the contract of a SOAP service by describing the available operations, how to invoke them, the structure of request and response messages, and the data types used.)which describes:

* available operations

* how to call them

* message structure

* data types

SOAP is used where **strict security and reliability** are required.

---

## **⭐ 2.2 Why SOAP Exists (Problems It Solves)**

SOAP was designed for:

* **Banking & financial transactions**

* **Telecom charging systems**

* **Government secure systems**

* **Enterprise business integration**

It ensures:

* Guaranteed message delivery

* Built-in security rules

* Built-in error codes

* Strong typing

* Contract-based communication

REST does **not** have these enterprise features built-in.

---

## **⭐ 2.3 Nepal Examples (Realistic)**

### **1\. Telecom Recharge Systems (SOAP)**

Telecom operators like NTC/Ncell often use SOAP for:

* Recharge request

* Balance inquiry

* Notification delivery

Example SOAP body:

\<Envelope\>  
    \<Body\>  
        \<CheckBalance\>  
            \<MobileNumber\>9841xxxxxx\</MobileNumber\>  
        \</CheckBalance\>  
    \</Body\>  
\</Envelope\>

---

### **2\. Inter-Bank Transactions (SOAP)**

Older banking systems use SOAP for:

* Fund transfers

* Card-to-card payments

* ATM host systems

Because SOAP ensures:

* Confirmed delivery

* High reliability

## **⭐ 2.4 Pros & Cons**

**Pros:**

* Very strict → safe for money-related systems

* Secure

* Reliable delivery

* Standardized contract (WSDL)

**Cons:**

* Slow compared to REST

* XML is heavy

* Not beginner-friendly

* Postman/Browser debugging is harder

---

# **🔵 3\. GraphQL API**

---

## **⭐ 3.1 Detailed Definition**

GraphQL is a **query language and runtime** for APIs where the client specifies **exactly what data it wants**, and the server returns **only that**.

GraphQL has:

* Single endpoint (usually `/graphql`)

* Client writes a “query” similar to SQL

* Server resolves the request using “resolvers”

---

## **⭐ 3.2 Why GraphQL Exists (Problems It Solves)**

REST issues:

* Underfetching → need multiple APIs to build a screen

* Overfetching → server sends more than needed

* Too many round trips → slow mobile performance

GraphQL solves this by:

* returning exactly what is needed

* combining multiple resources into a single request

---

## **⭐ 3.3 Nepal Use Cases (Realistic)**

### **1\. Real Estate Portal (Large Data)**

Imagine a Nepali property website:

UI needs:

* property details

* owner details

* nearby public facilities

* price history

REST would require **4 different APIs**.  
 GraphQL does it in **one**.

{  
  property(id:123) {  
    title  
    description  
    owner {  
      name  
      phone  
    }  
    nearbyFacilities {  
      school  
      hospital  
    }  
  }  
}

---

### **2\. Large E-commerce (Nepal Scale)**

Listing a product page needs:

* Product details

* Seller info

* Ratings

* Variants

* Delivery options

REST → multiple APIs  
 GraphQL → one structured query

---

### **3\. Education Portals / Coaching Tech**

For screens showing:

* Student info

* Classes

* Assignments

* Attendance

GraphQL is ideal.

---

## **⭐ 3.4 Pros**

* No underfetching

* No overfetching

* Fast for mobile

* Flexible

* Great for dashboards

## **⭐ 3.5 Cons**

* Harder server implementation

* Caching is complex

* Requires deeper QA understanding

---

# **🔵 4\. WebSocket (Real-Time API)**

---

## **⭐ 4.1 Deep Definition**

WebSocket is a communication protocol that creates a **full-duplex**, **persistent** connection between client and server.

### **🔹 “Full-duplex”**

👉 Communication happens **both ways at the same time**

| Protocol | Direction |
| ----- | ----- |
| HTTP | Client → Server only |
| WebSocket | Client ⇄ Server |

Server can send data **without waiting** for client request.

---

### **🔹 “Persistent connection”**

👉 Connection stays **open**

* No reconnect for every message

* One handshake, many messages

HTTP:

`Request → Response → Close`

WebSocket:

`Connect → Open → Message ⇄ Message ⇄ Message → Close`

Meaning:

* Connection stays open

* Client ↔ Server can both send data anytime

* Used for live updates

REST \= one request → one response  
 WebSocket \= continuous communication stream

---

## **⭐ 4.2 Why WebSocket Exists (Problems It Solves)**

Without WebSockets, apps had to:

* keep sending GET requests every second

* waste bandwidth(Bandwidth is the amount of data that can be transferred over a network in a given time.)

* overload server  
  

WebSocket solves:

* Real-time updates

* High-frequency data

* Live events

---

## **⭐ 4.3 Nepal Use Cases**

### **1\. Ride Tracking (Pathao, InDrive, Tootle)**

* Rider location updates every second

* Map marker moves in real time

* WebSocket pushes new coordinates instantly

---

### **2\. NEPSE Live Stock Updates**

* Price changes every 2–3 seconds

* Web app updates instantly

* No refresh required

---

### **3\. Live Chat Support Systems**

ISPs, banks, telecom sites use WebSockets for:

* Instant messaging

* Agent typing indicators

* Message delivery confirmations

---

### **4\. Live Attendance / Real-Time Monitoring Dashboards**

For Nepal corporate or educational systems where:

* Student checks in

* Dashboards update instantly for teachers/admin

---

## **⭐ 4.4 Pros**

* Extremely fast (no request repeating)

* Best for real-time apps

* Efficient network usage

## **⭐ 4.5 Cons**

* Harder for QA (you need special tools)

* More code complexity

* Connection-drop handling is tricky

---

# **🔵 5\. RPC / gRPC (Remote Procedure Call)**

---

## **⭐ 5.1 Full Definition**

RPC is a method where the client calls a **function on another machine** as if it were a local function.

Example (conceptually):

getWeather(city)  
transferMoney(account1, account2)  
calculateRoute(start, end)

gRPC (Google’s RPC):

* Uses Protocol Buffers (binary format)

* Extremely fast

* Used for backend-to-backend communication in microservices

---

## **⭐ 5.2 Why RPC Exists**

REST and GraphQL are great for apps → but too slow for:

* Internal service to service communication

* High-performance backend systems

* Millions of requests per second

RPC solves this by:

* Extremely compact binary messages

* Faster serialization/deserialization

* Long-lived connections

---

## **⭐ 5.3 Nepal Examples (Real Context)**

### **1\. Logistics & Delivery Platforms**

Companies like:

* Delivery services

* Local “courier tech”

* Warehouse management platforms

They often use internal microservices that talk via RPC.

---

### **2\. Digital TV/ISP Backends**

ISPs in Nepal often have:

* Billing microservice

* CRM microservice

* Network device controller microservice

These talk to each other using fast protocols (like RPC), not REST.

---

### **3\. Banking Internal Services**

Modern banks in Nepal:

* Card services

* Customer info system

* Risk scoring engine

* Notification engine

All need super-fast internal communication → RPC fits perfectly.

---

## **⭐ 5.4 Pros**

* Very fast

* Lightweight

* Ideal for microservices

## **⭐ 5.5 Cons**

* Not easy for mobile/web

* Harder to test manually

* Specialized tools required

---

# **🟣 FINAL SUMMARY TABLE (MASTER LEVEL)**

| API Type | Format | Best For | Nepal Example | QA Difficulty |
| ----- | ----- | ----- | ----- | ----- |
| **REST** | JSON | Apps, CRUD systems, websites | News apps, food delivery, bus route apps | ⭐ Easy |
| **SOAP** | XML | Secure/legacy/financial | Telecom recharge, interbank | ⭐⭐ Medium |
| **GraphQL** | JSON | Complex UIs, dashboards | Real estate, e-commerce data-heavy screens | ⭐⭐⭐ Hard |
| **WebSocket** | Stream | Live updates | Ride tracking, NEPSE, chat | ⭐⭐⭐ Hard |
| **RPC/gRPC** | Binary | Microservices, high-performance systems | ISP internal, banking microservices | ⭐⭐⭐⭐ Advanced |

---

# **🟧 TYPES OF API — BY ACCESS**

**(WHO CAN USE THE API? HOW OPEN OR RESTRICTED IS IT?)**

**APIs can also be classified based on who is allowed to access them and how they are shared.**

**This is extremely important in interviews and real-world projects because:**

* **It decides authentication**

* **It decides rate limits**

* **It decides security level**

* **It decides documentation structure**

* **It decides how QA should test the API**

**Below are the 4 industry-standard categories, with deep explanations.**

---

# **🔵 1\. PUBLIC API (Open API)**

---

## **⭐ 1.1 Definition**

**A Public API is an API that is open for external developers, meaning anyone can use it (usually after getting an API key).**  
 **These APIs are designed for integration, innovation, and community usage.**

---

## **⭐ 1.2 Purpose (Why It Exists)**

**Companies provide Public APIs to:**

* **Let developers build apps on top of their platform**

* **Encourage integrations**

* **Expand ecosystem**

* **Promote open data**

* **Increase usage of their services**

**Public APIs often become big developer communities.**

---

## **⭐ 1.3 Characteristics**

* **Available over the internet**

* **Requires API key but no special access**

* **Rate-limited (e.g., 100 requests/min)**

* **Strong documentation**

* **Used in tutorials, research, student projects**

---

## **⭐ 1.4 Nepal Context Examples**

**(No mention of your projects)**

### **1\. Weather API for Nepali Apps**

**Many Nepali weather apps use:**

**GET https://api.open-meteo.com/v1/forecast**

**Or global weather APIs like OpenWeatherMap.**

### **2\. News Aggregator Apps**

**Apps that show Nepali news in one place call public RSS/REST sources.**

### **3\. Nepali Travel / Tourism Apps**

**May use:**

* **Public currency conversion APIs**

* **Public timezone APIs**

* **Public holiday APIs**

### **4\. Cinema & Event Portals**

**Some provide public APIs for:**

* **list of shows**

* **event info**

* **upcoming movies**

### **5\. Crypto Price Trackers in Nepal**

**Use public APIs:**

**https://api.coingecko.com/api/v3/coins/bitcoin**

---

## **⭐ 1.5 QA Focus for Public APIs**

* **Check rate limits (429 Too Many Requests)**

* **Key-based authentication (API key required?)**

* **Documentation accuracy**

* **Response format consistency**

* **No sensitive data exposed publicly**

* **CORS policies(CORS controls which websites can call the API from a browser)**

---

# **🟣 2\. PARTNER API**

---

## **⭐ 2.1 Definition**

**A Partner API is shared only between two or more business partners.**  
 **It is not public but not totally internal either.**

**Both companies sign:**

* **Contracts**

* **Security agreements**

* **Data usage policies**

---

## **⭐ 2.2 Purpose (Why It Exists)**

**Partner APIs exist when two companies need to:**

* **Share business data**

* **Do transactions**

* **Integrate payment systems**

* **Sync inventory or logistics**

* **Verify identity or credentials**

**This is more secure than public API and more open than internal API.**

---

## **⭐ 2.3 Characteristics**

* **Authentication tokens/keys are stricter**

* **IP whitelisting often applied**

* **Rate limits negotiated in contract**

* **Error logs are shared cross-company**

* **Data privacy agreements needed**

---

## **⭐ 2.4 Nepal Context Examples**

### **1\. Banks ↔ Payment Providers**

**(Realistic & common scenario)**

* **Banks integrate with Khalti**

* **Fonepay ↔ financial institutions**

* **NIC Asia ↔ airline ticketing companies**

**Example:**

**POST https://partnerapi.fonepay.com.np/v1/payment/verify**

**Requires:**

* **Secret key**

* **Merchant code**

* **IP whitelisting**

---

### **2\. Ride-Sharing Companies ↔ Map Providers**

**Pathao or InDrive may integrate with:**

* **Google Maps Directions API**

* **Location providers**

### **3\. E-commerce ↔ Delivery/Logistics**

**Daraz partnering with:**

* **Delivery companies**

* **Warehouse management systems**

**They exchange:**

* **order details**

* **package tracking**

* **delivery status**

---

### **4\. Telecom Companies ↔ ISPs**

**For verifying user identity or sending notifications.**

---

## **⭐ 2.5 QA Focus for Partner APIs**

* **Validate required partner headers/signatures**

* **End-to-end integration scenarios**

* **Contract-based test cases (from SLA)**

* **Error handling for partner failures**

* **Retry logic**

* **Partial failure scenarios (partner down)**

* **Security (IP whitelisting, HMAC signatures)**

---

# **🔴 3\. INTERNAL API (Private API)**

---

## **⭐ 3.1 Definition**

**Internal APIs are used only within the same organization.**  
 **Not exposed to outside world.**

**Examples:**

* **Backend → Backend**

* **Backend → Frontend**

* **Microservice → Microservice**

**These APIs power internal systems and operations.**

---

## **⭐ 3.2 Purpose (Why It Exists)**

**Organizations need many internal services that must communicate efficiently:**

* **User service**

* **Payment service**

* **Notification service**

* **Inventory service**

* **HR service**

* **Billing service**

**Internal APIs allow clean separation of systems.**

---

## **⭐ 3.3 Characteristics**

* **No public access**

* **No external documentation**

* **May not need heavy auth (but usually has token)**

* **Data is more raw**

* **Performance optimized**

* **More version changes**

* **Fast-breaking updates (rapid development)**

---

## **⭐ 3.4 Nepal Context Examples**

### **1\. E-commerce Internal APIs**

**A Nepali e-commerce platform may have:**

**/internal/inventory/update**

**/internal/order/assign-delivery**

**/internal/payment/verify**

**These aren’t visible to customers — only internal dashboards, warehouse apps, delivery apps use them.**

---

### **2\. ISP Internal Systems**

**ISPs in Nepal (Vianet, ClassicTech, WorldLink) have:**

* **Internal CRM API**

* **Billing API**

* **Router configuration API**

* **Fiber connection status API**

**These are never public.**

---

### **3\. Digital Wallet Internal APIs**

**eSewa or Khalti internal services:**

* **Fraud detection**

* **Transaction risk scoring**

* **Notification engine**

* **Cashback engine**

---

### **4\. Hospital Management Systems**

**Internal modules:**

* **Lab API**

* **Pharmacy API**

* **Patient tracking API**

* **Billing and invoice API**

---

## **⭐ 3.5 QA Focus for Internal APIs**

* **Strict functional validation**

* **Database validation**

* **Performance tests (high load)**

* **Microservice communication flow**

* **Failover testing**

* **Logging / monitoring validation**

* **Versioning issues**

**Internal APIs need much more deep QA.**

---

# **🟡 4\. COMPOSITE API (Orchestration API)**

---

## **⭐ 4.1 Definition**

**A Composite API is where one API internally calls multiple other APIs and returns combined data to the client.**

**This is like:**

**“One API to fetch everything needed for a page.”**

**It is also used for workflows where many steps are combined:**

* **Step A: create user**

* **Step B: create address**

* **Step C: send welcome email**

**One Composite API does all steps internally.**

---

## **⭐ 4.2 Purpose (Why It Exists)**

**Composite APIs exist because:**

* **Mobile apps need less network calls**

* **Dashboards need multi-section data**

* **Slow networks (Nepal mobile data) require fewer requests**

* **Business workflows need automation**

---

## **⭐ 4.3 Characteristics**

* **One endpoint**

* **Multiple internal microservice calls**

* **Combined response**

* **Can include caching**

* **More complex backend logic**

* **Client sees simple result**

---

## **⭐ 4.4 Nepal Context Examples**

### **1\. Dashboards (Any Nepal App)**

**Banking Dashboard:**  
 **Shows:**

* **Account balance**

* **Last transactions**

* **Cards**

* **Loans**

* **Notifications**

**All fetched by one composite endpoint like:**

**GET /api/dashboard/overview**

**Internally calls 4–6 microservices.**

---

### **2\. Ride-Sharing Driver App**

**Driver dashboard shows:**

* **Today’s earnings**

* **Completed rides**

* **Pending payouts**

* **Rating**

* **Onboarding status**

**All combined internally.**

---

### **3\. Education Portal Dashboard**

**A Nepali LMS dashboard might combine:**

* **Student profile**

* **Notices**

* **Assignments**

* **Attendance**

* **Exam schedule**

---

### **4\. Healthcare System Dashboard**

**Doctor dashboard shows:**

* **Pending patients**

* **Lab results**

* **Prescriptions**

* **Appointments**

**Composite APIs handle this seamlessly.**

---

## **⭐ 4.5 QA Focus for Composite API**

* **Validate combined structure**

* **Partial failure scenarios**

* **Timeouts between microservices**

* **Slow microservice → does composite API respond?**

* **Whole workflow (E2E testing)**

* **Error propagation rules**

* **Data correctness from multiple sources**

**Composite APIs are the hardest to test after gRPC.**

---

# **🟩 FINAL SUMMARY (ACCESS-BASED)**

| API Type | Who Uses It? | Real Nepal Example | Security Level | QA Difficulty |
| ----- | ----- | ----- | ----- | ----- |
| **Public API** | **Anyone with key** | **Weather data, currency, news APIs** | **Low–Medium** | **⭐ Easy** |
| **Partner API** | **Business partners** | **Bank ↔ Fonepay/Khalti** | **High** | **⭐⭐⭐ Medium** |
| **Internal API** | **Inside organization** | **ISP CRM, internal payment engine** | **Medium–High** | **⭐⭐⭐⭐⭐ Hard** |
| **Composite API** | **Apps needing multi-data** | **Banking dashboard, LMS dashboard** | **Medium** | **⭐⭐⭐⭐ Hard** |

## **6\. What QA Tests in an API (Detailed \+ Where in Postman)**

💡 For each item:  
 **What it is → Where to see in Postman → How to test → Nepal example**

---

### **⭐ 6.1 Status Codes**

* **What:** Number indicating success or error.

* **Where:** Postman response top-right → `Status: 200 OK`.

**How to test:**

1. Valid request → expect `200` or `201`.

2. Invalid data → expect `400` or `422`.

3. Wrong URL → expect `404`.

4. No/invalid token → `401` or `403`.

**Examples:**

| Code | Meaning | Example (Nepal) |
| ----- | ----- | ----- |
| 200 | OK | LEC login success |
| 201 | Created | New CMS document created |
| 400 | Bad Request | Missing required signup field |
| 401 | Unauthorized | Token expired in NIC Asia app |
| 403 | Forbidden | Student calling admin-only endpoint |
| 404 | Not Found | Wrong `/verify-otpp` URL |
| 500 | Server Error | AMS backend crash |

---

### **⭐ 6.2 Response Body**

* **What:** JSON/XML data returned by server.

* **Where:** Response **Body** tab in Postman.

**How to test:**

* All required keys present?

* Data type correct? (`id` as number, `name` as string, etc.)

* Values follow business logic?

**Example – CMS Profile API:**

{  
  "id": 12,  
  "name": "Suraksha",  
  "email": "user@example.com",  
  "documents": 5  
}

QA checks:

* `id` is a number

* `documents` count increases after upload

* `email` format is valid

---

### **⭐ 6.3 Headers**

* **What:** Meta-data about request/response.

* **Where:**

  * Request headers → **Headers** tab (top section)

  * Response headers → **Headers** tab (bottom/response section)

**Important headers:**

| Header | Meaning |
| ----- | ----- |
| Content-Type | Format of body (JSON/XML) |
| Authorization | Token for secure access |
| Accept | What format client accepts |
| User-Agent | Who is making request |

**Example – LEC Profile API:**

Authorization: Bearer \<token\>  
Content-Type: application/json

QA ensures:

* Protected APIs **fail** without proper Authorization header.

---

### **⭐ 6.4 Business Logic**

* **What:** System rules, not just data.

* **Where:** By comparing **input → rule → output**.

**Example – Scholarship Eligibility API (Nepal scenario):**

Rule:

* If marks ≥ 80 ⇒ `scholarship = true`.

Tests:

* Send marks: 79 → expect `scholarship = false`.

* Send marks: 80 → expect `scholarship = true`.

* Send marks: 95 → expect `scholarship = true`.

Similar logic in:

* AMS: No attendance allowed for **future dates**.

* CMS: Country-specific required documents.

* LEC: OTP valid only for **2 minutes**.

---

### **⭐ 6.5 Error Handling**

* **What:** How API responds to bad input or internal errors.

* **Where:** Status code \+ response body.

**Good example:**

{  
  "error": "Invalid OTP. Please try again."  
}

**Bad example:**

Something went wrong

QA sends:

* Missing field

* Wrong data type

* Extra unexpected field

…and checks:

* Clear, user-friendly error

* No internal stack trace leakage

---

### **⭐ 6.6 Response Time (Basic Performance Check)**

* **What:** Time taken to respond.

* **Where:** Top-right in Postman → `Time: 320 ms`.

**High-level rule of thumb:**

| Time | Meaning |
| ----- | ----- |
| \< 800 ms | Good |
| 800–1500 ms | Okay |
| \> 1500 ms | Slow |

QA doesn’t do full performance testing here, but flags **consistently slow APIs**.

---

### **⭐ 6.7 Security (Basic From QA POV)**

Basic checks:

* Try **SQL injection** in input: `" OR 1=1 --"`

* Try calling **admin API with student token**

* Try calling **protected API without token**

Expected:

* Proper `401`/`403` responses

* No sensitive error messages

* No access to other user’s data

Example:  
 Student **must not** get success on:

GET /api/admin/all-users

---

## **7\. Practical Assignments (Hands-on)**

### **✅ Task 1 — Install & Setup Postman**

* Download Postman

* Create workspace

* Create a new request tab

---

### **✅ Task 2 — First GET Request**

Send:

GET https://jsonplaceholder.typicode.com/posts/1

Check in Postman:

* Status code \= `200 OK`

* Time (response time)

* Response body (JSON)

---

### **✅ Task 3 — Invalid Endpoint Test**

Use:

GET https://jsonplaceholder.typicode.com/postss/1

Expected: `404 Not Found`.  
 Ask students: why?

---

### **✅ Task 4 — Real Project Mapping**

From **AMS / CMS / LEC** (or any known system), identify:

* Base URL

* Endpoint path

* HTTP method

* Auth type (No Auth / API Key / Bearer Token)

---

## **8\. Bonus Practice (For Fast Learners)**

* Remove `Content-Type` from a POST → see what happens

* Miss a required field → observe error

* Use wrong method (GET instead of POST) → note status & message

* Open **Postman Console** and watch full request/response details

---

## **9\. Teacher Notes (How to Teach Day-1)**

* Start with **client–server diagram** on board.

* Use **Nepal-based examples** (Daraz, eSewa, LEC, AMS).

* Live demo: show a simple GET in Postman.

* Make students **read URL \+ method \+ status out loud**.

* Encourage them to explain:

  * “What is this API doing?”

  * “What is this status code telling you?”

---

## **🔁 Day-1 Summary Checklist (Quick Oral Test)**

Students should be able to answer:

* What is a **client**? What is a **server**?

* What is an **API** (in simple words)?

* What is the difference between **REST, SOAP, GraphQL**?

* How is an API URL structured (protocol, domain, base path, module, endpoint)?

* What is a **status code**? Give examples.

* What are **headers** and **response body**?

* Name at least **5 things a QA checks** in API testing.

---

## **🎯 Day-1 Revision Tasks (Homework)**

1. Write your own definition of **API** (≤ 2 lines).

2. Draw the **client–server–database** diagram.

3. Take any API URL and clearly label:

   * Protocol

   * Domain

   * Base path

   * Module

   * Endpoint

4. Perform a GET in Postman and note down:

   * URL

   * Method

   * Status code

   * Time

5. List **5 real apps in Nepal** that must use APIs and describe **1 example API** for each.  
---

# **⭐ DAY 2 — HTTP Methods, API Components, REST & API Documentation** 

---

## **🎯 Learning Objectives**

**By the end of Day-2, students must clearly understand:**

* **Difference between HTTP vs HTTPS (with SSL/TLS)**

* **What REST is and what RESTful constraints mean**

* **All HTTP Methods (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)**

* **Real runnable examples they can test in Postman**

* **Difference between request parameters (path, query, header, body)**

* **Structure of an HTTP request and HTTP response**

* **How to read API documentation (Swagger / Postman / public API docs)**

* **How QA analyzes and tests each method**

---

# **🔵 1\. HTTP Protocol & REST Concepts (Core Foundation)**

---

## **⭐ 1.1 HTTP vs HTTPS (With SSL/TLS Details)**

### **📘 What is HTTP?**

* **HTTP \= HyperText Transfer Protocol**

* **It defines how messages are sent between client (browser/app) and server.**

* **In plain HTTP, data is sent as plain text → can be read if intercepted.**

**Example:**

**http://example.com/api/users**

---

### **📘 What is HTTPS?**

* **HTTPS \= HyperText Transfer Protocol Secure**

* **It is HTTP \+ encryption using SSL/TLS.**

* **Data is encrypted before sending, and decrypted on the other end.**

**Example:**

**https://example.com/api/users**

**Used for:**

* **Banking apps (eSewa, Khalti, bank apps)**

* **Login systems**

* **Payment gateways**

* **Government portals**

---

### **🔐 What are SSL and TLS?**

#### **✅ SSL**

* **SSL \= Secure Sockets Layer**

* **It was the older protocol used to secure data between client and server.**

* **SSL versions are now outdated and considered insecure.**

#### **✅ TLS**

* **TLS \= Transport Layer Security**

* **This is the modern, secure version used today instead of SSL.**

* **When we say "SSL certificate" in real life, actually it is TLS under the hood.**

**📌 In simple terms:**

***“HTTPS uses TLS (modern SSL) to encrypt data.”***

**So what TLS does:**

* **Encrypts: password, OTP, tokens, personal data**

* **Verifies: server identity via certificate**

* **Protects: against man-in-the-middle attacks**

**You can tell students:**

**“HTTP \= talking loudly in a public place.**  
 **HTTPS \= talking in a locked room with code language (encryption).”**

---

## **⭐ 1.2 What is REST?**

### **📘 REST (Definition)**

* **REST \= Representational State Transfer**

* **It’s an architectural style for designing APIs.**

* **In REST:**

  * **Data is treated as resources (users, orders, products)**

  * **Each resource has a URI (unique path)**

  * **Client uses HTTP methods (GET, POST, PUT, etc.) to interact with resources.**

**Example resource URIs:**

**GET  /api/users**

**GET  /api/users/5**

**POST /api/users**

**PUT  /api/users/5**

**DELETE /api/users/5**

---

## **⭐ 1.3 What are “REST Constraints”?**

**Word meaning:**  
**👉 Reminder:**  
 **“Constraint” \= rule / restriction that REST architecture *must follow* to get benefits like scalability, simplicity, performance.**

**If an API follows these constraints well → we call it RESTful.**

**There are 6 main REST constraints:**

1. **Client–Server**

2. **Stateless**

3. **Cacheable**

4. **Uniform Interface**

5. **Layered System**

6. **Code-On-Demand (optional)**

**Let’s go one by one.**

---

### **🔹 1\. Client–Server**

#### **📘 Definition**

**Client and server must be separate concerns:**

* **Client → UI/UX, presentation layer (web app, mobile app, desktop app)**

* **Server → data storage, business logic, security, rules**

**The client should not care how data is stored, only how to request it.**

#### **🧠 Why this constraint exists**

* **Makes system modular means breaking a big system into small, independent parts (modules) that can work and change separately.**

* **Backend can be reused with many clients (Web, Android, iOS)**

* **Teams can work separately (frontend team, backend team, QA team, DevOps)**

  #### **🇳🇵 Example (Nepal context)**

**Think of a bus ticketing system:**

* **Android app used by passengers → client**

* **Web-based admin panel → another client**

* **Common backend API (Node/Laravel/Spring) → server**

**Both mobile app and admin panel talk to same REST API.**

#### **🔍 QA View**

* **You test APIs independent of UI using Postman.**

* **If UI changes (new theme, new design), your API test cases remain valid.**

* **You check if all clients (mobile/web) get consistent behavior from same APIs.**

  ---

  ### **🔹 2\. Stateless**

  #### **📘 Definition**

**Each request from client to server must contain all the information needed to understand and process it.**

* **Server does not store any session about client between requests.**

* **Server doesn’t “remember” what you did in previous request.**

**In REST:**

* **Authentication is usually done via tokens in each request (e.g., JWT in `Authorization` header).**

  #### **🚫 What “not stateless” would look like**

* **Server keeps user login state in memory:**  
   **“Ah this user logged in 2 mins ago, I’ll remember them without token” → NOT stateless.**

  #### **🧠 Why this constraint exists**

* **Makes horizontal scaling easier means adding more servers instead of making one server bigger:**

  * **Any server in a cluster can handle any request.**

* **If one server goes down, others can continue.**

  #### **🇳🇵 Example**

**A Nepali online learning platform:**

* **Student calls `GET /api/my-courses`**

* **Each request sends:**

* **Authorization: Bearer \<JWT\_TOKEN\>**


**Backend doesn’t remember “this user is logged in already” — it only trusts the token on each request.**

#### **🔍 QA View**

* **Always test with and without `Authorization` header.**

* **Verify:**

  * **No token → `401 Unauthorized`**

  * **Wrong token → `401`**

  * **Expired token → `401`**

* **Even if you call the same API 10 times, without token it should never “remember” you.**

  ---

  ### **🔹 3\. Cacheable**

  #### **📘 Definition**

**Server responses must indicate whether they are cacheable or not (via headers like `Cache-Control`, `Expires`, etc.).**

* **If a response is marked as cacheable, client or intermediate proxies can store it and reuse it.**

  #### **🧠 Why this constraint exists**

* **Performance boost (fewer trips to server)**

* **Less latency, better user experience**

* **Reduces load on backend server**

  #### **🇳🇵 Examples**

1. **News Portal API**

   * **`GET /api/top-news` → can be cached for 1–5 minutes.**

2. **Bus route list**

   * **`GET /api/routes` → doesn’t change often → good candidate for caching.**

3. **Public holiday list**

   * **`GET /api/holidays/2025` → can be cached for days/weeks.**

**These can be served faster using caching.**

#### **🔍 QA View**

**You don’t always need to go very deep into HTTP caching, but as a QA you should:**

* **Inspect `Cache-Control`, `Expires`, `ETag` headers when given in docs.**

* **Ensure sensitive data is NOT cached (e.g., user info, tokens, bank balance).**

* **Verify that public data can be cached appropriately, as per requirement.**

  ---

  ### **🔹 4\. Uniform Interface**

**This is one of the most important constraints and has its own sub-rules.**

**Definition (simple):**

**Client and server must communicate in a consistent, standardized way so that different clients can talk to the same server without special changes.**

**Uniform Interface means: “All APIs should follow the same common rules, so clients don’t need special instructions for each endpoint.”**

**It means:**

* **Standard HTTP methods used properly**

* **Resource-based endpoints**

* **Standard response forms**

* **Self-descriptive messages**

**Let’s break it into key ideas.**

---

#### **4.1 Resource-Based URIs**

* **Resources are nouns, not actions:**

  * **✅ `/users/10`**

  * **❌ `/getUserById?userId=10`**

* **Collections & items:**

  * **`/users` (collection)**

  * **`/users/10` (single resource)**

  * **`/users/10/orders` (related resources)**

**✅ Good REST style → answers “what resource?” not “what function?”.**

---

#### **4.2 Standard Use of HTTP Methods**

* **`GET /users/10` → read user**

* **`POST /users` → create new user**

* **`PUT /users/10` → full update**

* **`PATCH /users/10` → partial update**

* **`DELETE /users/10` → delete user**

**You shouldn’t see:**

* **`POST /getUsers`**

* **`GET /deleteUser?id=10`**

**That breaks uniform interface.**

---

#### **4.3 Self-Descriptive Messages**

**Each request/response contains enough information that anyone can understand it:**

* **Proper status codes**

* **Clear error messages**

* **Content-Type header**

* **Consistent JSON keys**

**Example error:**

* **{**  
*   **"error": "EMAIL\_ALREADY\_EXISTS",**  
*   **"message": "This email is already registered."**  
* **}**


**Much better than:**

* **{**  
*   **"error": "Error occurred"**  
* **}**  
    
  ---

  #### **4.4 HATEOAS (Advanced / Optional in practice)**

**HATEOAS \= Hypermedia As The Engine Of Application State.**  
 **Means response contains links to actions you can take next.**

**Example:**

* **{**  
*   **"id": 10,**  
*   **"name": "Aastha",**  
*   **"links": \[**  
*     **{ "rel": "self", "href": "/users/10" },**  
*     **{ "rel": "orders", "href": "/users/10/orders" }**  
*   **\]**  
* **}**


**Not many APIs fully use HATEOAS in real life, but it’s part of original REST definition.**

---

#### **🔍 QA View**

**As QA, when checking uniform interface:**

* **URLs should be clean, resource-based**

* **Methods must follow correct semantics**

* **Status codes must be meaningful**

* **JSON structures must be consistent across endpoints**

**Develop test cases like:**

* **Does `POST /users` really create new user?**

* **Does `GET /users` never modify anything?**

* **Does `DELETE /users/10` remove the user permanently or soft-delete?**

  ---

  ### **🔹 5\. Layered System**

  #### **📘 Definition**

**Client doesn’t know if it’s talking to:**

* **The actual origin server, or**

* **An API gateway, or**

* **A cache layer, or**

* **A load balancer.**

**System is built in layers, each layer having its own responsibility.**

#### **🇳🇵 Example**

**A Nepali banking API setup might look like:**

* **Mobile App**  
*     **↓**  
* **API Gateway  (validation, rate limiting)**  
*     **↓**  
* **Backend Service (business logic)**  
*     **↓**  
* **Database**


**Or for a big e-commerce platform:**

* **Client → CDN/Reverse Proxy → API Gateway → Microservices → DB**


  #### **🧠 Why this constraint exists**

* **Makes the system more scalable**

* **Load can be spread across many servers**

* **Security layers can be added**

* **Backend can be refactored without impacting clients**

  #### **🔍 QA View**

* **You normally test the API gateway endpoint (e.g., `https://api.example.com/...`)**

* **You may be unaware of internal microservices.**

* **For performance or reliability testing, understanding there are layers helps you report:**

  * **Where the slowdown might be (gateway vs service vs DB)**

  ---

  ### **🔹 6\. Code-On-Demand (Optional)**

  #### **📘 Definition**

**Servers can send code to clients (e.g., JavaScript) to extend their functionality.**

**Example:**

* **Webpage loads JS from the server that adds dynamic behavior.**

* **This is more about web apps rather than pure JSON APIs.**

**It’s one constraint which is optional — most REST APIs you test will not rely heavily on this concept.**

#### **🔍 QA View**

**For REST API testing, you mostly don’t need to worry about this constraint.**  
 **It’s more relevant in full web-app behavior testing (front-end testing).**

---

### **🧠 How to Explain Constraints to Students in Class**

**You can summarize like this:**

* **Client–Server → Separate UI and backend.**

* **Stateless → Server doesn’t remember; every request is complete.**

* **Cacheable → Some responses can be reused for speed.**

* **Uniform Interface → Consistent URLs, methods, status codes.**

* **Layered System → There can be gateways and proxies in between, not only one server.**

* **Code-on-Demand → Optional; server can send executable code.**

**Then ask them:**

**“If an API uses GET to delete, or keeps state on server memory only, is it truly RESTful?”**

**(Answer: it’s breaking constraints.)**

---

# **🔵 2\. HTTP Methods (Deep \+ Runnable Examples)**

**For each HTTP method:**

* **Concept explanation**

* **Real Nepal-like scenario (for imagination)**

* **Runnable public API example (so you can actually do it in Postman)**

**We’ll mainly use:**

* **JSONPlaceholder → [https://jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com/)**

* **ReqRes → [https://reqres.in](https://reqres.in/)**

---

## **⭐ 2.1 GET Method**

### **📘 Definition**

**GET is used to retrieve data from the server**  
 **and does not modify anything.**

### **📌 Key Rules**

* **No body (in most cases)**

* **Safe & idempotent (repeat \= same effect)**

---

### **🇳🇵 Nepal Scenario (Concept)**

* **A tourism app shows a list of hotels in Pokhara.**

* **A bus app shows routes from Kalanki → Chitwan.**

---

### **🧪 Real Runnable Example (JSONPlaceholder)**

**Request:**

**GET https://jsonplaceholder.typicode.com/posts/1**

**Steps in Postman:**

1. **Set method \= `GET`**

2. **URL \= `https://jsonplaceholder.typicode.com/posts/1`**

3. **Click Send**

**You get JSON for single post.**

### **🔍 QA Tests**

* **Valid ID → returns 200 \+ valid JSON**

* **Invalid ID (e.g., 999999\) → see behavior**

* **Measure response time**

* **Verify response keys & data types**

---

## **⭐ 2.2 POST Method**

### **📘 Definition**

**POST is used to create new data on server.**

---

### **🇳🇵 Nepal Scenario (Concept)**

* **User registers in a Nepali online exam portal.**

* **Customer books a movie ticket.**

---

### **🧪 Real Runnable Example (ReqRes)**

**Request:**

**POST https://reqres.in/api/users**

**Body (raw JSON):**

**{**

  **"name": "Sagar",**

  **"job": "QA Student"**

**}**

**Steps:**

1. **Method: `POST`**

2. **URL: `https://reqres.in/api/users`**

3. **Body → raw → JSON**

4. **Paste above JSON**

5. **Click Send**

**You’ll get:**

**{**

  **"name": "Sagar",**

  **"job": "QA Student",**

  **"id": "123",**

  **"createdAt": "2025-11-28T..."**

**}**

### **🔍 QA Tests**

* **Missing `name` → what happens?**

* **Unsupported fields → ignored or error?**

* **Status code should be `201 Created` or `200 OK` depending on API**

* **Response has new `id` and `createdAt`**

---

## **⭐ 2.3 PUT Method**

### **📘 Definition**

**PUT is used to completely replace an existing resource.**

---

### **🇳🇵 Nepal Scenario (Concept)**

* **User updates full profile information in local banking portal.**

---

### **🧪 Real Runnable Example (ReqRes)**

**Request:**

**PUT https://reqres.in/api/users/2**

**Body:**

**{**

  **"name": "Rohan",**

  **"job": "Engineer"**

**}**

**Steps:**

1. **`PUT https://reqres.in/api/users/2`**

2. **Body → raw → JSON**

3. **Paste above JSON**

4. **Send**

**The API returns updated resource.**

### **🔍 QA Tests**

* **All fields updated as per request**

* **If a field missing → does API remove or ignore it?**

* **Response structure correct**

---

## **⭐ 2.4 PATCH Method**

### **📘 Definition**

**PATCH is used to partially update a resource**  
 **(only some fields).**

---

### **🇳🇵 Nepal Scenario (Concept)**

* **User changes only email or only phone number in profile.**

---

### **🧪 Real Runnable Example (ReqRes)**

**Request:**

**PATCH https://reqres.in/api/users/2**

**Body:**

**{**

  **"job": "Senior QA"**

**}**

**Steps:**

1. **`PATCH https://reqres.in/api/users/2`**

2. **Body → JSON**

3. **Paste above body**

4. **Send**

### **🔍 QA Tests**

* **Only `job` field changes**

* **Other fields remain unchanged**

* **Response status \= 200**

* **Validation rules still apply**

---

## **⭐ 2.5 DELETE Method**

### **📘 Definition**

**DELETE is used to remove a resource from server.**

---

### **🇳🇵 Nepal Scenario (Concept)**

* **User deletes a saved address from Food Delivery app.**

* **Admin deletes a fake account.**

---

### **🧪 Real Runnable Example (ReqRes)**

**Request:**

**DELETE https://reqres.in/api/users/2**

**Steps:**

1. **`DELETE https://reqres.in/api/users/2`**

2. **No body**

3. **Click Send**

**ReqRes returns `204 No Content` (nothing in body).**

### **🔍 QA Tests**

* **Status code `204` or `200`**

* **Second DELETE → should be `404` or same `204` depending on design**

* **Try deleting non-existing ID**

---

## **⭐ 2.6 HEAD Method (Runnable Example)**

### **📘 Definition**

**HEAD returns only headers, no body.**

### **🧪 Example (use JSONPlaceholder):**

**HEAD https://jsonplaceholder.typicode.com/posts/1**

**In Postman:**

* **Method: HEAD**

* **URL: above**

* **Send → you’ll see headers, but no body.**

---

## **⭐ 2.7 OPTIONS Method (Runnable Example)**

**Some public APIs may not return full OPTIONS, but you can still try:**

**OPTIONS https://jsonplaceholder.typicode.com/posts**

**You’ll see allowed methods in headers if configured.**

---

# **🔵 3\. API REQUEST COMPONENTS (More Detail \+ Definitions)**

**An API request is made of several parts working together.**

---

## **⭐ 3.1 What is a “Parameter” in General?**

**Definition:**

**A parameter is an input value you send to the API to tell the server:**

* **What resource you want**

* **How to filter results**

* **What data you’re sending**

**Parameters can be in:**

* **URL path**

* **Query string**

* **Headers**

* **Body**

---

## **⭐ 3.2 Types of Parameters (Deep Explanation)**

---

### **🔹 3.2.1 Path Parameters**

**Definition:**

**Path parameters are part of the URL path itself and usually identify a specific resource.**

**They are placed in the URL like:**

**GET /users/{id}**

**Example:**

**GET https://jsonplaceholder.typicode.com/posts/1**

* **`1` here is a path parameter (post ID).**

**In Swagger docs, path params show with `{}` (curly braces).**

**As QA, you test:**

* **Valid ID**

* **Non-existent ID**

* **Wrong type (string instead of number)**

---

### **🔹 3.2.2 Query Parameters**

**Definition:**

**Query parameters are key–value pairs after `?` in the URL used for filtering, sorting, searching, pagination, etc.**

**Syntax:**

**?key1=value1\&key2=value2**

**Example:**

**GET /api/hotels?city=Pokhara\&rating=4\&priceMax=3000**

**Here:**

* **`city`, `rating`, `priceMax` are query parameters.**

**In Postman, they go in the Params tab.**

**As QA, you test:**

* **Missing query param**

* **Invalid value type**

* **Multiple filters**

* **Combination of filters**

---

### **🔹 3.2.3 Header Parameters**

**Definition:**

**Header parameters are values sent in the HTTP headers to give meta-information about request or client.**

**They are not visible in URL.**

**Examples:**

* **`Authorization: Bearer <token>`**

* **`Content-Type: application/json`**

* **`Accept-Language: ne-NP`**

**In Postman:**

* **Use Headers tab (key–value table).**

**As QA, you test:**

* **Missing `Authorization` header**

* **Invalid token**

* **Wrong `Content-Type`**

* **Language impact on response**

---

### **🔹 3.2.4 Body Parameters**

**Definition:**

**Body parameters are fields inside the body of POST/PUT/PATCH requests.**

**They represent actual data you send to server to create or update resources.**

**Example (ReqRes):**

**{**

  **"name": "Sagar",**

  **"job": "QA Engineer"**

**}**

**Type: JSON fields.**

**In Postman:**

* **Body → raw → JSON**

**As QA, you test:**

* **Required vs optional fields**

* **Data type (string, number, boolean)**

* **Length restrictions**

* **Business rules (age \> 18, salary \> 0\)**

---

### **⭐ 3.3 Recap: Request Components**

**API Request \=**

* **Method → What to do (GET, POST, PUT, PATCH, DELETE)**

* **URL → Where to do it (endpoint)**

* **Headers → Extra info (auth, type, language)**

* **Parameters → Inputs (path, query, header, body)**

* **Body → Main data (for create/update)**

---

# **🔵 4\. API RESPONSE COMPONENTS**

**An API Response is what server sends back.**

**Response \=**  
 **Status Code \+ Headers \+ Body \+ Time \+ Size**

---

## **⭐ 4.1 STATUS CODE – Result meaning**

**Examples:**

* **`200 OK` → success**

* **`201 Created` → new resource is created**

* **`400 Bad Request` → client sent invalid data**

* **`401 Unauthorized` → invalid/missing auth**

* **`404 Not Found` → resource doesn’t exist**

* **`500 Internal Server Error` → server crashed**

**Example with ReqRes:**

**`GET https://reqres.in/api/users/2`**

**`Status: 200 OK`**

---

## **⭐ 4.2 RESPONSE HEADERS**

**Examples:**

| Header | Meaning |
| ----- | ----- |
| **`Content-Type`** | **Format of response (e.g. JSON)** |
| **`Server`** | **Server software (nginx, cloudflare)** |
| **`Date`** | **Time when response generated** |
| **`Content-Length`** | **Size of payload** |
| **`RateLimit-Remaining`** | **Requests left (for public APIs)** |

**Example (Dog API):**

**`GET https://dog.ceo/api/breeds/list/all`**

**`Response headers:`**

  **`Content-Type: application/json`**

  **`Server: cloudflare`**

  **`Date: Tue, 12 Nov 2025`**

---

## **⭐ 4.3 RESPONSE BODY – Actual data**

**Example (OpenWeather):**

**`{`**

  **`"weather": "cloudy",`**

  **`"temp": 21`**

**`}`**

**QA validates:**

* **Keys**

* **Data types**

* **Business rules**

* **Error formats**  
  **\`2q**

---

## **⭐ 4.4 RESPONSE TIME**

* **Time taken to respond (in ms)**

* **Seen in Postman as `Time: 320 ms`**

**QA checks:**

* **Consistency**

* **Very slow endpoints**

* **Spikes under load**

---

## **⭐ 4.5 RESPONSE SIZE**

* **Size in bytes/kB**

* **Larger size \= slower on weak networks**

**QA must watch big responses for optimization.**

---

# **🔵 5\. HOW TO READ API DOCUMENTATION**

## **⭐ 5.1 Swagger (OpenAPI) Documentation — Real Example**

**Open:**

**`https://petstore.swagger.io/`**

**You’ll see:**

* **Title: Swagger Petstore**

* **Modules/tags: pet, store, user**

* **Each with endpoints like `GET /pet/{petId}`, `POST /pet`, etc.**

**Pick: GET `/pet/{petId}`**

**Swagger shows:**

* **Method & Path: `GET /pet/{petId}`**

* **Summary & Description: explains purpose**

* **Parameters:**

  * **`petId` (path, integer, required)**

* **Responses:**

  * **200 → success schema \+ example JSON**

  * **400, 404 → error conditions**

* **Try It Out button to call live from browser**

### **How QA Reads Swagger:**

* **Inputs:**

  * **Path params**

  * **Query params**

  * **Body (for POST/PUT)**

* **Validation rules:**

  * **Required/optional**

  * **Data types**

  * **Allowed values (enums)**

* **Outputs:**

  * **Response structure**

  * **Error codes & messages**

**From this, QA writes:**

* **Positive test cases**

* **Negative test cases (missing, invalid, null)**

* **Edge cases (max length, boundary IDs)**

---

## **⭐ 5.2 Reading Postman Echo Docs – Real Example**

**Open:**

**`https://documenter.getpostman.com/view/5025623/SWTG5aqV`**

**You’ll see:**

* **Title: Postman Echo Documentation**

* **Description: API for testing REST clients**

* **Requests list: GET, POST (raw, form-data), PUT, PATCH, DELETE**

**Pick: GET Request**

**Inside you’ll see:**

* **Request URL: `https://postman-echo.com/get`**

* **Query params: `foo1`, `foo2`**

* **Explanation: what GET does and echo behavior**

* **Example Response JSON (args, headers, url)**

**QA extracts:**

* **Method: GET**

* **Endpoint: `/get`**

* **Params: foo1, foo2 (optional)**

* **Behavior: echoes back what you send**

* **Status: `200 OK`**

* **Response structure: `args`, `headers`, `url`**

**Test cases:**

* **Without params**

* **With one param**

* **With multiple params**

* **With long/special characters**

---

## **⭐ 5.3 Reading Third-Party Public API Docs**

### **🔸 OpenWeatherMap**

**`https://openweathermap.org/api`**

**QA checks:**

* **API key requirement**

* **Rate limits**

* **Query params (q, lat, lon, units)**

* **Error codes (`401` for invalid key, `404` for city not found)**

---

### **🔸 News API**

**`https://newsapi.org/`**

**Used to fetch global & possibly Nepali news articles.**

**QA checks:**

* **Endpoint list**

* **API key usage**

* **Filter options (country, category, q)**

* **Error response patterns**

---

### **🔸 TMDB (Movie DB API)**

**`https://developer.themoviedb.org/reference`**

**QA checks:**

* **Authentication (API key / Bearer)**

* **Required vs optional fields**

* **Rate limits**

* **Pagination behavior**

---

## **🔵 6\. Practical Assignments for Day-2**

---

### **🔹 Assignment 1 — Methods in Postman**

**Using a public API (e.g., JSONPlaceholder: `https://jsonplaceholder.typicode.com`):**

* **Send `GET /posts/1` → view post**

* **Send `POST /posts` → create dummy post**

* **Send `PUT /posts/1` → full update**

* **Send `PATCH /posts/1` → partial update**

* **Send `DELETE /posts/1` → delete**

---

### **🔹 Assignment 2 — Identify Components in Docs**

**Pick any of:**

* **Postman Echo docs**

* **Swagger Petstore**

* **OpenWeatherMap**

**Students must list:**

* **Request type (GET/POST…)**

* **Headers**

* **Path params**

* **Query params**

* **Body (if any)**

* **Expected success response**

* **Expected error responses**

---

### **🔹 Assignment 3 — Design Test Scenarios**

**For imaginary APIs:**

1. **Search movies**

2. **Book a hotel**

3. **Update user profile**

4. **Delete saved address**

**Ask students to create:**

* **3 positive cases**

* **5 negative cases**

---

# **🔵 7\. Teacher Notes (How to Teach Day-2)**

* **Start with HTTP vs HTTPS → why security matters**

* **Draw request–response diagram**

* **Explain GET/POST/PUT/PATCH/DELETE with Nepal daily life examples**

* **Live Postman demo (at least 2 methods)**

* **Show Swagger \+ Postman docs to connect theory & practice**

* **Make students identify parameters & build test cases**

* **End with quick oral quiz:**

  * **“What is idempotent?”**

  * **“Difference between query & path param?”**

  * **“What is in headers?”**

---

# **🔵 8\. Day-2 Summary Checklist (Student Must Understand)**

**✔ HTTP vs HTTPS**  
 **✔ What is REST & RESTful constraints**  
 **✔ GET vs POST vs PUT vs PATCH vs DELETE**  
 **✔ HEAD & OPTIONS basic purpose**  
 **✔ Required vs optional parameters**  
 **✔ Path vs query vs header vs body**  
 **✔ Request & response structure**  
 **✔ Reading Swagger & Postman docs**  
 **✔ How to run and analyze API calls in Postman**

# **⭐ DAY 3 — HTTP Status Codes, Debugging & Real-World Scenarios (FINAL VERSION)**

---

## **🎯 Learning Objectives**

**By the end of Day-3, students will clearly understand:**

**✔ What status codes are and why they exist**  
 **✔ Status code classes (1xx–5xx)**  
 **✔ Detailed explanation of each important status code**  
 **✔ Real Nepal-based examples for every code**  
 **✔ How to trigger each status code intentionally in Postman**  
 **✔ How to read response bodies, headers, and errors**  
 **✔ How rate-limiting (429) works**  
 **✔ QA debugging workflow for common issues**

**Time required → 3 hours**  
 **(1 hour theory \+ 2 hours hands-on debugging)**

---

# **🔵 1\. What Are HTTP Status Codes?**

**A status code is a 3-digit number returned by the server that tells the result of a request.**

**Think of it as:**

* **200 → “Yes, done.”**

* **400 → “Your request is wrong.”**

* **500 → “Our server failed.”**

---

# **🔵 2\. Status Code Classes**

**HTTP status codes are grouped into 5 categories:**

| Class | Meaning | Example Codes |
| ----- | ----- | ----- |
| **1xx** | **Informational** | **100 Continue** |
| **2xx** | **Success** | **200, 201, 202, 204** |
| **3xx** | **Redirection** | **301, 302** |
| **4xx** | **Client Errors** | **400, 401, 403, 404, 422** |
| **5xx** | **Server Errors** | **500, 502, 503** |

**Most APIs deal heavily with 2xx, 4xx, 5xx.**

---

# **🔵 3\. SUCCESS CODES (2xx)**

---

## **⭐ 3.1 200 OK — Request Successful**

### **Meaning:**

**Server processed the request successfully.**

### **🇳🇵 Nepal Real Scenario:**

**Nepali bus schedule API returns available buses:**

**GET /api/buses?from=Butwal\&to=Kathmandu**

**Server returns 200 \+ JSON list.**

### **QA Must Verify:**

**✔ Correct data returned**  
 **✔ Proper JSON structure**  
 **✔ Pagination (if any)**  
 **✔ Response time reasonable**

### **How to trigger in Postman:**

**Send a valid GET request:**

**GET https://jsonplaceholder.typicode.com/posts/1**

---

## **⭐ 3.2 201 Created — Resource Successfully Created**

### **Meaning:**

**A new resource has been created.**

### **🇳🇵 Scenario:**

**Nepali cinema ticket booking API:**

**POST /api/tickets**

**Body:**

**{**

  **"movieId": 101,**

  **"seat": "G10"**

**}**

**Response:**

**201 Created**

### **QA Must Verify:**

**✔ Resource created**  
 **✔ New ID returned**  
 **✔ Success message**

### **Trigger in Postman:**

**POST https://reqres.in/api/users**

---

## **⭐ 3.3 204 No Content — Successful but no response body**

**Used in DELETE or logout.**

### **🇳🇵 Scenario:**

**Delete a saved delivery address:**

**DELETE /api/address/34**

**Response: `204`**

### **QA Checks:**

**✔ No body returned**  
 **✔ Resource actually deleted**  
 **✔ 404 for next call**

---

# **🔵 4\. CLIENT ERROR CODES (4xx)**

---

## **⭐ 4.1 400 Bad Request — Invalid Input**

### **Meaning:**

**Client sent incorrect or incomplete data.**

### **🇳🇵 Example:**

**Signup with missing password:**

**POST /api/signup**

**{**

  **"email": "user@test.com"**

**}**

**Response:**

**{**

  **"error": "Password is required"**

**}**

### **How QA Triggers:**

* **Missing required fields**

* **Invalid data type**

* **Wrong JSON format**

### **Try in Postman:**

**POST https://reqres.in/api/register**

**Send wrong fields → get 400\.**

---

## **⭐ 4.2 401 Unauthorized — Missing or Wrong Token**

### **Meaning:**

**No valid authentication provided.**

### **🇳🇵 Example:**

**Accessing user profile without login:**

**GET /api/user/me**

**Response: 401 → "Token missing"**

### **QA Tests:**

**✔ No token → 401**  
 **✔ Wrong token → 401**  
 **✔ Expired token → 401**

---

## **⭐ 4.3 403 Forbidden — You are not allowed**

### **Meaning:**

**You have a token, but you don’t have permission.**

### **🇳🇵 Example:**

**Normal user tries admin-only API:**

**GET /api/admin/customers**

**Response: 403\.**

### **QA Tests:**

* **User role enforcement**

* **Access control list (ACL)**

---

## **⭐ 4.4 404 Not Found — Wrong URL / Endpoint**

### **Meaning:**

**Endpoint or resource doesn’t exist.**

### **🇳🇵 Example:**

**Wrong cinema ID:**

**GET /api/cinemas/99999**

**Cinema not found → 404\.**

### **Trigger:**

**In Postman type wrong URL like:**

**GET https://jsonplaceholder.typicode.com/postssss**

---

## **⭐ 4.5 422 Unprocessable Entity — Validation Error**

### **Meaning:**

**Data submitted is correct format but logically invalid.**

### **🇳🇵 Example:**

**Hotel booking:**

**Date "Checkout \< Checkin" → invalid.**

### **QA Tests:**

**✔ Boundary checks**  
 **✔ Logical checks**  
 **✔ Validation messages**

---

# **🔵 5\. SERVER ERROR CODES (5xx)**

---

## **⭐ 5.1 500 Internal Server Error**

### **Meaning:**

**Server crashed or failed due to bug.**

### **🇳🇵 Example:**

**Nepal payment gateway returns 500 if server is down.**

### **QA Tests:**

**✔ Try invalid inputs**  
 **✔ Check if API gracefully handles crash**

---

## **⭐ 5.2 502 Bad Gateway**

**Occurs when API gateway cannot reach backend.**

### **🇳🇵 Scenario:**

**High load on server during Dashain offer → gateway fails.**

---

## **⭐ 5.3 503 Service Unavailable**

**Server temporarily offline or under maintenance.**

---

# **🔵 6\. Rate Limiting & Throttling (429 Too Many Requests)**

---

## **⭐ 429 Too Many Requests**

### **Meaning:**

**You have exceeded API request limit per minute/hour.**

### **How APIs in Nepal Use It:**

* **SMS providers (Sparrow, EasySMS)**

* **Payment gateways**

* **Banking OTP providers**

* **Live score APIs**

### **Trigger in Postman (Manual Simulation):**

**Send GET request 20–30 times quickly.**

**Some public APIs like GitHub, TMDB will return:**

**429 Rate Limit Exceeded**

### **QA Must Check:**

**✔ Useful error message**  
 **✔ Retry-After header present**  
 **✔ Application handles retry logic correctly**

---

# **🔵 7\. Debugging API Errors — QA Workflow**

### **When you get an error, follow this EXACT flow:**

**1\. Check HTTP method (GET/POST/PUT…)**

**2\. Check URL/path parameters**

**3\. Check query params format**

**4\. Check headers (Content-Type, Authorization)**

**5\. Check request body schema**

**6\. Check response body for hints**

**7\. Check if server logs provided (rare)**

### **Debugging Example in Postman**

**Error:**  
 **`400 Bad Request`**

**Steps:**

1. **Click Body tab → verify JSON structure**

2. **Click Headers → check Content-Type**

3. **Click Console (bottom-left) → see request logs**

4. **Fix error → resend request**

---

# **🔵 8\. Practical Assignments (Hands-On)**

---

## **⭐ Assignment 1 — Trigger 5 Status Codes**

**Use:**

**👉 [https://jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com/)**  
 **👉 [https://reqres.in](https://reqres.in/)**  
 **👉 [https://httpstat.us/](https://httpstat.us/)**

### **Examples to Perform:**

#### **✔ 200**

**GET https://jsonplaceholder.typicode.com/posts/1**

#### **✔ 201**

**POST https://reqres.in/api/users**

#### **✔ 204**

**DELETE https://jsonplaceholder.typicode.com/posts/1**

#### **✔ 400**

**Send empty body to:**

**POST https://reqres.in/api/register**

#### **✔ 404**

**Wrong endpoint.**

**GET https://jsonplaceholder.typicode.com/abcxyz**

---

## **⭐ Assignment 2 — Identify Status Codes from Docs**

**Visit Swagger:**  
 **👉 [https://petstore.swagger.io](https://petstore.swagger.io/)**

**Pick 3 endpoints and write:**

* **Expected 200**

* **Expected 400**

* **Expected 404**

* **Expected 500**

---

## **⭐ Assignment 3 — Create Status Code Cheat Sheet**

**For these actions:**

**✔Logging into an app**  
 **✔Sending wrong credentials**  
 **✔Viewing profile**  
 **✔Accessing admin panel without permission**  
 **✔Deleting something twice**

**Students must produce:**

* **Status code**

* **Nepal scenario**

* **Explanation**

---

# **🔵 9\. Teacher Notes**

* **Ask students: “Tell me difference between 401 & 403”**

* **Make them manually break APIs on purpose**

* **Use live Postman demo for each code**

* **Let them check headers & body in errors**

* **Give bonus marks for real debugging approach**

---

# **🔵 10\. Day-3 Summary Checklist**

**✔ 2xx, 4xx, 5xx groups**  
 **✔ Meaning of each important code**  
 **✔ 200 vs 201 vs 204**  
 **✔ 400 vs 401 vs 403 vs 404 vs 422**  
 **✔ 500 vs 502 vs 503**  
 **✔ 429 and rate limit**  
 **✔ How to trigger each code in Postman**  
 **✔ How QA debugs failures**

---

## **⭐ DAY 4 — API Headers & Authentication Basics (DAY 4 NOTES — FINAL VERSION)**

---

## **🎯 Learning Objective**

**By the end of Day-4, students should understand essential HTTP headers and the introduction to API authentication methods.**

**Students must be able to:**

* **Explain why headers exist and what they carry (meta-information).**  
* **Identify and use these headers confidently in Postman: Content-Type, Accept, Authorization, User-Agent.**  
* **Explain the difference between No Auth vs API Key vs Bearer Token (intro).**  
* **Use Postman Console to debug outgoing request headers.**

---

## **3\) ⏱ Time Estimate**

**Total: 2.5 hours**

* **1 hour → learn headers \+ auth types**  
* **1.5 hours → Postman testing \+ experimentation**

---

## **4\) 📚 Theory (Simple explanation \+ where to see in Postman \+ real-life scenario examples)**

### **4.1 What are Headers (simple meaning)**

**Headers are values sent in HTTP headers to give meta-information about the request or client. They are not visible in the URL.**

**Think of headers like the envelope details on a courier package:**

* **Who is sending? (User-Agent)**  
* **What type of item is inside? (Content-Type)**  
* **What kind of response do you want? (Accept)**  
* **Are you allowed to receive it? (Authorization)**

### **4.2 Where to see Headers in Postman (must know)**

**In Postman you can see headers in two places:**

* **Request headers → Headers tab (key–value table) in the request area**  
* **Response headers → Headers tab inside the response section**

### **4.3 Real-life Nepal scenarios (concept examples, like in your notes)**

**Your notes already use Nepal-based teaching examples like Daraz, eSewa, LEC, AMS.**  
**So use the same style for Day-4:**

* **Daraz-like e-commerce: mobile app sends headers to tell the backend “I’m Android app v3.1” (User-Agent) and expects JSON back (Accept).**  
* **eSewa/Khalti-like payment: payment verification endpoints must block unknown users → needs Authorization.**  
* **LEC / school portal: student’s profile API must fail if token is missing. (Authorization)**

---

## **5\) 🔑 Key Concepts (Each header explained in detail \+ QA checks \+ where to see in Postman \+ Nepal scenario examples)**

**Important note (from your notes): Headers are a key QA check area and you must verify them for both request and response.**

---

### **5.1 ✅ Header: Content-Type**

**Meaning (in your notes):**

* **Content-Type \= format of body (JSON/XML)**  
* **Example in notes: `Content-Type: application/json`**

**When it matters most:**

* **Mainly for POST/PUT/PATCH (requests that send a body).**  
* **If Content-Type is wrong, server may not parse body properly → leads to 400/415-like behavior (you observe via status \+ body). (Teach as observation, not memorization.)**

**Where to see / set in Postman:**

* **Request → Headers tab (key–value table)**

**QA checks (from your notes):**

* **Wrong Content-Type → check how API reacts**  
* **Bonus practice already recommended in your notes: Remove Content-Type from a POST and see what happens**

**Nepal scenario (teaching example):**

* **“Online form submission” for a Nepali education portal (LEC/CMS style) sends JSON profile update.**  
  * **If Content-Type is missing/wrong, backend may treat it as empty → returns validation error (“missing field”).**

**Teacher Tip (how to explain to students):**

* **Say: “Content-Type is what language your body is speaking. If you speak JSON but don’t tell the server, server gets confused.”**

---

### **5.2 ✅ Header: Accept**

**Meaning (in your notes):**

* **Accept \= what format client accepts**

**Why this matters:**

* **Client is telling server: “Please reply in JSON (or another format) so I can read it.”**  
* **QA uses Accept when API supports multiple formats (or to ensure response is consistent).**

**Where to see / set in Postman:**

* **Request → Headers tab (key–value table)**  
* **Response → Headers tab → check response `Content-Type` matches expected format**

**QA checks (practical):**

* **Send request with Accept set (ex: JSON expectation), then confirm response header shows correct content-type.**

**Nepal scenario (teaching example):**

* **A “Bus route finder app” in Nepal expects JSON so it can render routes quickly on mobile.**  
  * **If API returns HTML or unexpected response type, app breaks (blank screen / parsing error).**

**Teacher Tip:**

* **Say: “Accept is what you want to receive; Content-Type is what you are sending.”**

---

### **5.3 ✅ Header: Authorization**

**Meaning (in your notes):**

* **Authorization \= token for secure access**  
* **Example in notes: `Authorization: Bearer <token>`**

**Why it exists (QA mindset):**

* **Without Authorization, protected endpoints must block access. Your notes clearly say QA ensures protected APIs fail without proper Authorization.**

**Where to see / set in Postman:**

* **Request → Headers tab (key–value)**

**QA checks (directly from notes):**

* **Missing Authorization header**  
* **Invalid token**  
* **Expected result: 401 Unauthorized when missing/invalid auth (shown in your status code examples too).**

**Nepal scenario (teaching example):**

* **Bank app / wallet app token expired → user gets 401 Unauthorized (your notes even give a Nepal example: “Token expired in NIC Asia app”).**  
* **LEC student tries admin-only endpoint → 403 Forbidden (another Nepal example in your notes).**

**Teacher Tip:**

* **Say: “Authorization is your entry pass. No pass → security guard stops you.”**

---

### **5.4 ✅ Header: User-Agent**

**Meaning (in your notes):**

* **User-Agent \= who is making request**

**Why QA cares:**

* **Sometimes backend behaves differently for different clients (web vs mobile).**  
* **Even if your API *should* behave same, QA checks if client identity affects response or error patterns (debugging point).**

**Where to see / set in Postman:**

* **Request → Headers tab (key–value)**  
* **Debug in Postman Console to confirm it actually got sent (Day-4 bonus).**

**Nepal scenario (teaching example):**

* **A Nepali mobile banking app might send a specific User-Agent to help backend logging: “AndroidApp/…”**  
* **If backend blocks unknown automated clients, different User-Agent may change behavior (e.g., stricter security rules).**

**Teacher Tip:**

* **Say: “User-Agent is like your identity card that says what device/app you are.”**

---

## **6\) 🔐 Authentication Basics to Advanced**

**Below is every authentication/authorization option Postman documents in the Auth (Authorization) dropdown \+ certificate-based auth in Settings, explained teacher-style with what it is, when to use, how to set in Postman, where it gets added (headers/URL/body), and QA checks.**

---

# **How Postman “Auth” works (must understand first)**

### **Where you configure it**

**Open any request → Authorization tab → choose Auth Type. Postman then auto-populates the correct part of the request (Header / URL / Body / Params) based on that auth type. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/specifying-authorization-details/))**

### **Where you confirm it actually got applied**

* **Request → Headers tab (some auth appears as hidden headers) and you can preview what Postman added. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/specifying-authorization-details/))**  
* **After sending → Postman Console shows a raw dump including auth data. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/specifying-authorization-details/))**

### **Two critical Postman rules (students always get stuck here)**

1. **You can’t override auth headers in the Headers tab if they were generated from Authorization settings—change it from Authorization tab instead. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/specifying-authorization-details/))**  
2. **Postman recommends storing secrets in variables / Postman Vault; it avoids saving header/query auth data to reduce accidental exposure. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/specifying-authorization-details/))**

---

# **A) Auth options inside Postman    Authorization tab (Auth Type dropdown)**

## **1\) No Auth**				

**What it is: Postman sends no authorization details. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/authorization-types/))**  
**When used: Public APIs (open data, health-check endpoints).**  
**Where it appears: Nothing is added.**

**QA checks (Nepal scenario):**

* **For a “public notice” API of a municipality website: it should work without auth.**  
* **Negative: confirm it doesn’t accidentally require auth (unexpected 401).**

---

## **2\) Inherit auth from parent**

**What it is: Request inherits auth from Folder/Collection so you set it once and reuse everywhere. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/specifying-authorization-details/))**  
**When used: Real projects where 20–200 endpoints share the same token/key.**

**How to set:**

* **Set auth at Collection or Folder level.**  
* **Inside a request choose Inherit auth from parent. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/specifying-authorization-details/))**

**QA benefit (Nepal scenario):**

* **If you’re testing an “eSewa-like wallet API,” you can store token at collection level and every endpoint uses it consistently.**

---

## **3\) API Key**

**What it is: Sends a key-value pair (like `x-api-key: <value>`) either in Headers or Query Params. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/authorization-types/))**  
**When used: Public/partner APIs that want usage tracking \+ rate limiting (weather/news/maps).**

**How to set in Postman (Authorization tab):**

* **Type: API Key**  
* **Enter Key name \+ Value**  
* **Choose Add to: Header or Query Params ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/authorization-types/))**

**Where it appears:**

* **If Header → appears in Headers**  
* **If Query Params → appended to URL query string ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/authorization-types/))**

**QA checks:**

* **Missing key → should fail (commonly 401/403 depending on API design)**  
* **Wrong key → should fail**  
* **Key leak risk → confirm you used variables/vault, not hardcoded values ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/specifying-authorization-details/))**

**Nepal example:**

* **“Weather alert dashboard for Baglung municipality” using an API key. If key is missing → dashboard must show a friendly error instead of crashing.**

---

## **4\) Bearer Token**

**What it is: Adds `Authorization: Bearer <token>` (often JWT access token). ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/authorization-types/))**  
**When used: Most modern apps (login → get token → call protected endpoints).**

**How to set:**

* **Type: Bearer Token**  
* **Paste token in Token field ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/authorization-types/))**

**Where it appears:**

* **Postman appends it to the Authorization header in the required `Bearer ...` format ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/authorization-types/))**

**QA checks (very important):**

* **Missing token → 401**  
* **Expired token → 401**  
* **Valid token, wrong role → often 403 (authorization failure)**  
* **Token should not change response structure (still JSON etc.)**

**Nepal example:**

* **“Student portal (LEC)”: student token must not access admin endpoints.**

---

## **5\) JWT Bearer (Postman generates JWT for you)**

**What it is: Postman can generate a JWT bearer token by taking payload \+ signing method, then adds it to the request. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/authorization-types/))**  
**When used: When your API expects a self-signed JWT (service-to-service, internal tools).**

**How to set (Authorization tab → JWT Bearer):**

* **Choose where JWT goes: Request Header or Query Param**  
* **Choose Algorithm (HS/RS/ES/PS families)**  
* **Provide Secret (HMAC) or Private key (RSA/ECDSA)**  
* **Provide Payload JSON**  
* **Optional advanced: header prefix, custom JWT headers ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/authorization-types/))**

**QA checks:**

* **Wrong algorithm → should fail**  
* **Wrong key/secret → should fail**  
* **Payload fields (`iss`, `aud`, `exp` etc.) behavior must match API rules (if your API enforces them)**

---

## **6\) Basic Auth**

**What it is: Sends username \+ password encoded and put into `Authorization: Basic <base64...>`. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/authorization-types/))**  
**When used: Legacy systems, internal tools, quick prototyping, some vendor APIs.**

**How to set:**

* **Type: Basic Auth**  
* **Fill Username \+ Password ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/authorization-types/))**

**Where it appears:**

* **Authorization header as `Basic <Base64...>` ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/authorization-types/))**

**QA checks:**

* **Wrong password → 401**  
* **Verify HTTPS is used (Basic Auth over HTTP is risky)**  
* **Confirm credentials stored as variables/vault ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/specifying-authorization-details/))**

**Nepal example:**

* **A small local ISP’s internal admin API might still use Basic Auth for simplicity.**

---

## **7\) Digest Auth**

**What it is: Challenge-response style auth (more secure than Basic in how it avoids sending raw password). Postman can automate the multi-step handshake. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/digest-auth/))**

**How to set:**

* **Type: Digest Auth**  
* **Enter Username \+ Password**  
* **Postman shows two-stage fields and auto-updates advanced fields using server response ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/digest-auth/))**

**Important Postman behavior:**

* **By default it can retry automatically after extracting server data; you can disable retry and do it manually. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/digest-auth/))**

**QA checks:**

* **Wrong password → 401**  
* **If automation disabled → confirm advanced values are set correctly**  
* **Confirm server nonce/realm changes are handled**

---

## **8\) OAuth 1.0**

**What it is: Older OAuth standard (still used in some APIs). Postman supports OAuth 1.0 core revision A. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/oauth-10/))**

**How to set (high level):**

* **Type: OAuth 1.0**  
* **Choose where to add auth: Headers OR Body/URL**  
* **Choose signature method and fill required fields; Postman can auto-generate advanced values ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/oauth-10/))**

**Where it appears:**

* **If header → Authorization header starting with `OAuth ...`**  
* **If body/URL → params go into Body (x-www-form-urlencoded) or URL query params depending on request method ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/oauth-10/))**

**QA checks:**

* **Signature mismatch errors (common)**  
* **Timestamp/nonce replay issues**  
* **Wrong consumer key/secret**

---

## **9\) OAuth 2.0**

**What it is: Modern standard using access tokens (and sometimes ID tokens). Postman can request tokens and attach them automatically. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/oauth-20/))**

**How to set (Authorization tab):**

* **Type: OAuth 2.0**  
* **Choose to pass auth in URL or Headers**  
* **Use Get New Access Token → Proceed → Use Token ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/oauth-20/))**

**Where it appears:**

* **By default Postman appends token as `Authorization: Bearer <token>` (prefix editable). ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/oauth-20/))**

**Team sharing note:**

* **Postman has options for sharing tokens (controls syncing) ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/oauth-20/))**

**QA checks (very practical):**

* **Wrong redirect URL / wrong client secret → token fetch fails**  
* **Access token works for some endpoints but not admin endpoints (scope/role issue)**  
* **Token refresh flow (if used) behaves correctly**

**Nepal example:**

* **Government SSO / enterprise identity provider for a big system could use OAuth2; QA validates scopes (citizen vs officer).**

---

## **10\) Hawk Authentication**

**What it is: Uses partial cryptographic verification; Postman collects Hawk ID, key, algorithm, and builds required headers. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/hawk-authentication/))**

**How to set:**

* **Type: Hawk Authentication**  
* **Fill Hawk Auth ID, Hawk Auth Key, Algorithm**  
* **Postman adds the final auth to Headers when required details are complete ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/hawk-authentication/))**

**QA checks:**

* **Wrong algorithm or key → signature fail**  
* **Nonce replay handling (server should reject repeats)**

---

## **11\) AWS Signature**

**What it is: AWS custom scheme based on keyed-HMAC for AWS requests. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/aws-signature/))**

**How to set:**

* **Type: AWS Signature**  
* **Choose Add authorization data to: Request Headers or Request URL**  
* **If headers → Postman adds `Authorization` \+ `X-Amz-...` headers**  
* **If URL → adds `X-Amz-...` params in URL ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/aws-signature/))**

**QA checks:**

* **Wrong region/service name causes signature mismatch**  
* **Time skew issues**  
* **Missing required headers**

---

## **12\) NTLM Authentication (Windows NTLM)**

**What it is: Windows challenge-response auth, common in on-prem enterprise systems. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/ntlm-authentication/))**

**How to set:**

* **Type: NTLM Authentication**  
* **Username \+ Password**  
* **Optional advanced: Domain, Workstation ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/ntlm-authentication/))**

**Postman behavior:**

* **Can run request a second time after extracting data; you can disable retry. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/ntlm-authentication/))**

**QA checks:**

* **Domain/workstation mismatches**  
* **Correct user permissions**

---

## **13\) Akamai EdgeGrid**

**What it is: Akamai-specific auth (for Akamai APIs).**  
**How to set:**

* **Type: Akamai EdgeGrid**  
* **Provide Access Token, Client Token, Client Secret**  
* **Postman adds required details to headers after completion ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/akamai-edgegrid/))**

**QA checks:**

* **Invalid tokens → unauthorized**  
* **Ensure secrets stored in variables ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/akamai-edgegrid/))**

---

## **14\) ASAP (Atlassian)**

**What it is: Atlassian Service-to-Service auth using JWT bearer token. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/atlassian/))**  
**How to set:**

* **Type: ASAP (Atlassian)**  
* **Fill required details; Postman can generate optional values ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/atlassian/))**

**QA checks:**

* **Wrong JWT claims or key signing → fail**  
* **Ensure server validates audience/issuer properly**

---

# **B) Certificate-based authentication in Postman (not in Auth dropdown)**

## **15\) Mutual TLS (mTLS) Client Certificates \+ Custom CA Certificates**

**Some APIs require certificates (common in banking/enterprise gateways).**

**What it is: mTLS requires both client and server to verify identity via certificates before encrypted connection is established. ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/certificates/))**

**Where to set in Postman:**  
**Settings (gear icon) → Certificates tab ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/certificates/))**

### **Add CA certificate (fix “self signed certificate” errors)**

* **Turn on CA certificates toggle**  
* **Upload PEM file ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/certificates/))**

### **Add Client certificate (mTLS)**

* **Add Certificate**  
* **Host (domain only, no protocol; supports wildcard patterns)**  
* **Optional port (default 443\)**  
* **CRT \+ Key OR PFX**  
* **Optional passphrase ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/certificates/))**

**QA checks:**

* **Wrong host mapping → certificate not applied**  
* **Expired cert → handshake failure**  
* **If multiple certs for same domain, Postman uses last one (avoid duplicates). ([Postman Docs](https://learning.postman.com/docs/sending-requests/authorization/certificates/))**

**Nepal context example (training story):**

* **Bank/Payment gateway sandbox may require mTLS. QA confirms handshake success and that requests fail when cert removed.**

## **7\) 🛠 Step-by-step Postman Practical (Tasks \+ Steps)**

### **7.1 Setup (before requests)**

1. **Create a Collection: Day 4 — Headers & Auth**  
2. **For every request you send, always check:**  
   * **Status code (top right)**  
   * **Response Headers (response → Headers tab)**  
   * **Request Headers (request → Headers tab)**  
3. **Turn on Postman Console (Bonus required today):**  
   * **Open console and watch full request/response details**  
   * **Routine Day-4 specifically asks this: analyze outgoing request headers.**

---

### **7.2 Task A — Hit 5 public APIs and inspect headers (No Auth)**

**Use these 5 public APIs (all referenced in your notes/doc examples):**

**1\) JSONPlaceholder**

   **GET https://jsonplaceholder.typicode.com/posts/1**

**2\) ReqRes**

   **GET https://reqres.in/api/users/2**

**3\) Postman Echo (echoes back what you send)**

   **GET https://postman-echo.com/get?foo1=bar1\&foo2=bar2**

**4\) Swagger Petstore**

   **GET https://petstore.swagger.io/v2/pet/1**

**5\) CoinGecko**

   **GET https://api.coingecko.com/api/v3/coins/bitcoin**

* **JSONPlaceholder and ReqRes are the main runnable examples in your notes.**  
* **Postman Echo’s /get endpoint and that it returns request details (including headers) is described in your notes.**  
* **Swagger Petstore is explicitly mentioned as a docs source students can pick.**  
* **CoinGecko is listed as a public API example for practice in your notes.**  
  **(And you can also verify Postman Echo & Petstore from their official docs.) ([Postman Docs](https://learning.postman.com/docs/developer/echo-api/?utm_source=chatgpt.com))**

**For EACH request, do this mini-checklist:**

1. **Send request (No special headers first).**  
2. **Open Response Headers → note down:**  
   * **`Content-Type` (response format)**  
3. **Open Request Headers → add these two manually and resend:**  
   * **`Accept: application/json` (client expects JSON)**  
   * **`User-Agent: QA-Student-Postman` (identify client)**  
4. **Use Postman Echo request to confirm your headers were actually sent (because it echoes “headers” back).**  
5. **Open Postman Console → confirm outgoing headers exist (Day-4 bonus).**

---

### **7.3 Task B — API Key Authentication with 1 API**

**Routine says: use one API with API key (example: NewsAPI or OpenWeather).**  
**Your notes show QA checks for OpenWeatherMap/NewsAPI include API key requirement and typical errors like 401 invalid key.**

**Steps (safe & aligned to your PDFs):**

1. **Pick ONE: OpenWeatherMap or News API (teacher can provide a class key or each student uses their own).**  
2. **First send request without key → observe likely 401 (invalid/missing auth).**  
3. **Then send with key as per that API’s documentation (some accept it in headers or query params).**  
4. **Verify:**  
   * **Success response OR a different error (example: OpenWeather can also give 404 city not found, which is still useful QA feedback).**  
5. **Record evidence: status code \+ response body \+ response headers.**

---

### **7.4 Mini Experiment (10 minutes) — Content-Type behavior (Header focus)**

**Your notes recommend experiments like removing Content-Type from a POST.**

**Do this with a safe dummy POST from your earlier runnable examples (ReqRes POST exists in your notes).**

1. **Create a POST request (ReqRes user creation example).**  
2. **Send with proper Content-Type (JSON).**  
3. **Remove Content-Type header and send again.**  
4. **Compare status \+ message → learn why Content-Type matters.**

---

## **8\) 🧾 QA Test Case Template (Table)**

| TC\_ID | Title | API/Endpoint | Method | Headers to Set/Change | Auth Type | Steps (short) | Expected Result | Actual Result | Status (Pass/Fail) | Evidence (Screenshot/Notes) |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **TC-01** | **Verify response content type** | **(paste endpoint)** | **GET** | **Accept=application/json** | **No Auth** | **Send request → open Response Headers** | **Response Content-Type is JSON-like** |  |  |  |
| **TC-02** | **Missing Authorization should fail** | **(protected endpoint)** | **GET** | **Remove Authorization** | **Bearer** | **Send request** | **401 Unauthorized** |  |  |  |
| **TC-03** | **Invalid token should fail** | **(protected endpoint)** | **GET** | **Authorization=Bearer invalid** | **Bearer** | **Send request** | **401 Unauthorized** |  |  |  |
| **TC-04** | **API key missing should fail** | **(News/Weather endpoint)** | **GET** | **Remove key** | **API Key** | **Send request** | **401 invalid/missing key** |  |  |  |
| **TC-05** | **User-Agent logged/echoed** | **Postman Echo /get** | **GET** | **User-Agent=QA-Student-Postman** | **No Auth** | **Send → check echoed headers** | **User-Agent appears in echoed headers** |  |  |  |

---

## **9\) ✅ Day Summary Checklist (Quick Oral Test)**

**Students should be able to answer (Day-4 oral checklist style like Day-1):**

* **What are headers (simple meaning)?**  
* **Where do you set request headers in Postman?**  
* **Where do you see response headers in Postman?**  
* **Difference: Content-Type vs Accept?**  
* **What does Authorization header do?**  
* **Difference: No Auth vs API Key vs Bearer Token?**  
* **What does Postman Console help you debug today?**

---

## **10\) 📝 Revision Tasks (Homework)**

1. **Write 2 lines each (simple definition):**  
   * **Content-Type, Accept, Authorization, User-Agent**  
2. **Take screenshots of:**  
   * **Request headers tab and Response headers tab from one request**  
3. **Create 5 test cases using the template:**  
   * **At least 2 negative cases must be about missing/invalid auth.**  
4. **Make a “Nepal scenario mapping” like your notes style:**  
   * **Choose any 3: (Daraz / eSewa / Khalti / LEC / AMS)**  
   * **For each, write one endpoint idea and specify: which header(s) are critical and why.**  
5. **Console practice:**  
   * **Open Postman Console and write what you observed for “outgoing request headers”.**

## 

## **⭐ DAY 5 — JSON Structure & Data Formats (JSON \+ XML Basics)**

### **1\) 🎯 Learning Objective**

Master how data is structured in **JSON format** and explore **XML basics**, including how XML differs from JSON (commonly seen in legacy systems).

---

### **2\) ⏱ Time Estimate**

**Total: 2.5 hours**

* **1 hour** → JSON concepts  
* **1.5 hours** → build/convert/validate data samples

---

## **3\) 📚 Theory (Simple explanation \+ where to see in Postman \+ real-life Nepal scenarios)**

### **3.1 What is JSON (in simple words)?**

**JSON (JavaScript Object Notation)** is a **text format** used to exchange structured data between systems (client ↔ server). It mainly represents:

* **Objects** (key/value pairs)  
* **Arrays** (ordered lists)  
* Primitive values like **string, number, boolean, null** ([RFC Editor](https://www.rfc-editor.org/rfc/rfc8259?utm_source=chatgpt.com))

✅ Why QA must understand JSON?  
Because most REST APIs return data in JSON. In Postman, your “Response Body” is very commonly JSON.

### **3.2 Where to see JSON in Postman**

When you hit an API in Postman:

* **Response Body** → you see the actual JSON/XML response returned by server  
* **Pretty View** → Postman formats JSON/XML for easier reading and collapsing large blocks ([docs.devnet-academy.com](https://docs.devnet-academy.com/docs/postman/sending-requests/response-data/responses/index.html?utm_source=chatgpt.com))  
* **Headers tab** → you’ll often see `Content-Type: application/json` which indicates JSON format

### **3.3 Real-life Nepal scenarios (why JSON matters)**

Think like this (very common in Nepal apps too):

* **Wallet / Fintech (eSewa/Khalti-type systems)**: API returns JSON like `{ "status": "success", "txnId": "...", "amount": 500 }`  
* **College / Exam portal**: API returns student profile JSON like `{ "name": "Sagar", "semester": 5, "roll": 12 }`  
* **Municipality system** (attendance / billing / citizen record): API returns nested JSON (citizen \+ documents \+ ward info)

As QA, if you don’t understand JSON structure, you can’t verify **keys, types, and business logic** properly.

---

## **4\) 🔑 Key Concepts (Structure \+ data types \+ QA checks \+ where in Postman \+ Nepal examples)**

### **4.1 JSON Structure: Object (Key–Value)**

**JSON Object** is inside `{ }` and contains **key:value pairs**.

Example (Nepal exam portal “student profile”):

{

  "id": 12,

  "name": "Suraksha",

  "email": "user@example.com",

  "documents": 5

}

This same kind of example appears in API notes as response body sample, and QA checks include verifying data types.

**Where in Postman?**

* Response → **Body → Pretty**  
* Confirm header: **Response Headers** contain Content-Type (JSON/XML)

✅ QA Checks (Object level)

* Are **all required keys present**?  
* Are keys spelled correctly (`documents` vs `document`)?  
* Do keys follow stable naming (avoid random renames)?

---

### **4.2 Arrays (Lists) in JSON**

**Array** is inside `[ ]` and contains an ordered list of values/objects.

Example (Pokhara hotel list):

{

  "city": "Pokhara",

  "hotels": \[

    { "name": "Hotel A", "rating": 4 },

    { "name": "Hotel B", "rating": 5 }

  \]

}

✅ QA Checks (Array level)

* Array should be an array (not object), and not a string like `"hotels": "Hotel A"`  
* Validate **array length** when logic expects it (e.g., pagination page size)  
* Check each item structure: does every hotel have `name` and `rating`?

**Where in Postman?**

* Body → Pretty → you can expand/collapse arrays easily ([docs.devnet-academy.com](https://docs.devnet-academy.com/docs/postman/sending-requests/response-data/responses/index.html?utm_source=chatgpt.com))

---

### **4.3 Nested JSON (Object inside Object)**

Nested JSON is common in real apps.

Example (Municipality citizen record — ward \+ documents):

{

  "citizen": {

    "name": "Ramesh",

    "ward": { "number": 6, "name": "Ward-6" }

  },

  "documents": \[

    { "type": "Citizenship", "verified": true }

  \]

}

✅ QA Checks (Nested structure)

* Ensure nested keys exist: `citizen.ward.number`  
* Validate business rule: if `verified=true`, then status must show verified  
* Negative case: missing nested object should return proper error message (not crash)

**Important QA focus from notes:** verify response keys and **data types** properly.

---

### **4.4 JSON Data Types (must know for QA)**

JSON supports:

* **string** `"Sagar"`  
* **number** `12` (JSON does not separate int/float in the spec; it’s “number”) ([RFC Editor](https://www.rfc-editor.org/rfc/rfc8259?utm_source=chatgpt.com))  
* **boolean** `true/false`  
* **null** `null`  
* **object** `{ }`  
* **array** `[ ]` ([RFC Editor](https://www.rfc-editor.org/rfc/rfc8259?utm_source=chatgpt.com))

✅ QA Checks (Type validation — very important)  
From the notes:

* `id` should be a **number**, `name` should be a **string**  
* If API returns `id: "12"` (string) instead of `12` (number), that can break mobile/web code.

Nepal scenario:

* **Khalti-like payment verification**: `amount` must be number; if string `"500"`, your fee calculation might fail in client app.

---

### **4.5 Common JSON mistakes QA should catch (very practical)**

These are real errors that cause API parsing failures:

* Missing comma  
* Trailing comma (not allowed in strict JSON)  
* Single quotes instead of double quotes  
* Unbalanced `{ }` or `[ ]`  
  (Validators like jsonlint are used to catch these quickly.) ([npm](https://www.npmjs.com/package/jsonlint?utm_source=chatgpt.com))

---

## **5\) 🧾 XML Basics \+ “How XML differs from JSON (legacy systems)”**

Day-5 requires exploring **XML basics** and the difference from JSON.

### **5.1 XML in simple terms**

XML is also a text-based structured format, but it is tag-based like:

\<student\>

  \<name\>Suraksha\</name\>

  \<id\>12\</id\>

\</student\>

### **5.2 Why XML is still seen (legacy systems)**

Your API notes explain SOAP uses **XML message format** and is used where strict rules/security are needed (banking/telecom/government).

Nepal examples mentioned in notes:

* Telecom recharge/balance inquiry systems (NTC/Ncell-type) using SOAP/XML style  
* Older banking integrations using SOAP/XML for reliability

### **5.3 Key difference (QA view)**

* JSON is usually **lighter \+ easier** for REST apps (mobile/web)  
* XML is **more verbose** and often appears in **legacy/enterprise SOAP** integrations

---

## **6\) 🛠 Step-by-step Practical (Tasks \+ Steps)**

### **Practical A — Validate sample JSON using jsonlint.com**

(Required in routine)

**Steps**

1. Take a JSON sample (from your API response or from the sample below).  
2. Paste into **jsonlint** (online validator).  
3. Fix errors until it validates.  
4. Copy the formatted JSON back.

**Sample JSON (intentionally broken — for practice)**

{

  "name": "Sagar"

  "phone": 9841,

}

Expected: validator should show error (missing comma \+ trailing comma).

---

### **Practical B — Convert JSON to XML using online tools**

(Required in routine)

**Steps**

1. Use a correct JSON object.  
2. Paste into an online JSON→XML converter.  
3. Observe:  
   * keys become tags  
   * arrays become repeated tags/items  
4. Discuss in class: Which looks easier to read/debug? (JSON usually)

---

### **Practical C — Create and parse 3 complex JSON samples manually**

(Required in routine)

You will **write**, then **explain** each JSON:

1. Nested object \+ array  
2. Array of objects \+ boolean flags  
3. Null \+ optional fields

**Template for your 3 samples**

* What is the main object?  
* Which keys are nested?  
* Which keys are arrays?  
* Which keys are boolean/null?

---

### **🧠 Bonus Practice — Write JSON payload for sign-up form**

(Required in routine)

**Sign-up payload (Nepal context: college portal / municipality service / wallet signup)**

{

  "name": "Sagar Thapa",

  "email": "sagar@example.com",

  "phone": "98XXXXXXXX",

  "roles": \["student", "tester"\]

}

✅ QA checks for this payload:

* Email format valid (contains @)  
* phone stored as string (so it doesn’t lose leading zeros or formatting)  
* roles is an array (not a single string)

---

## **7\) 🧪 QA Test Case Template (Table — for JSON/Data Format Validation)**

| Test Case ID | Title | Input / Response Sample | Where to Check (Postman) | Steps | Expected Result |
| ----- | ----- | ----- | ----- | ----- | ----- |
| JSON-01 | Validate required keys exist | `{ "id": 1, "name": "X" }` | Body → Pretty | Send request, inspect JSON | All required keys present |
| JSON-02 | Validate data types | `id` should be number | Body \+ compare types | Check each key type | Types match contract (id=number, name=string) |
| JSON-03 | Validate array structure | `roles: ["student"]` | Body → Pretty | Inspect roles | roles is array, not string |
| JSON-04 | Negative: invalid JSON should fail parsing | broken JSON | jsonlint validation | Paste to validator | Validator shows exact error |
| XML-01 | Convert JSON to XML and verify structure preserved | JSON→XML | Converter output | Convert and compare | Fields map correctly; arrays become repeated elements |

---

## **8\) ✅ Day Summary Checklist (What you must be able to do today)**

* Explain JSON object vs array clearly (with `{}` and `[]`) ([RFC Editor](https://www.rfc-editor.org/rfc/rfc8259?utm_source=chatgpt.com))  
* Identify JSON data types (string/number/boolean/null/object/array) ([RFC Editor](https://www.rfc-editor.org/rfc/rfc8259?utm_source=chatgpt.com))  
* In Postman, locate JSON response in **Body** and check `Content-Type` header  
* Validate JSON using jsonlint (find and fix syntax issues)  
* Convert JSON to XML and explain why XML is common in legacy/SOAP systems  
* Create one clean signup JSON payload (name/email/phone/roles)

---

## **9\) 📝 Revision Tasks (Homework)**

1. Write **3 JSON samples**:  
   * one nested  
   * one with arrays  
   * one with `null` optional field  
2. Break each JSON intentionally (missing comma / quotes) → validate in jsonlint → fix it.  
3. Convert one JSON sample to XML and write 5 lines explaining “how XML differs from JSON” (QA perspective).  
4. Create your own **Nepal-based signup payload**:  
   * include realistic phone format `"98XXXXXXXX"`  
   * include roles array  
5. In Postman, open any API response you already tested earlier and list:  
   * 3 keys  
   * their types  
   * which one is nested (if any)

## **1\) ⭐ DAY 6 — Postman Environment Setup & GET Requests**

(From routine: “Postman UI overview (requests, collections, environments) \+ Anatomy of GET request & endpoints \+ Query parameters” )

---

## **2\) 🎯 Learning Objective**

By the end of Day 6, you will be able to:

1. Navigate Postman UI confidently (Request tab, Collections, Environments, History).  
2. Create and send **GET** requests correctly and understand “endpoint” meaning.  
3. Use **query parameters** in Postman (Params tab \+ URL) and know what to test as QA.  
4. Save your practice requests into a **new Collection** for reuse.  
5. Use **History tab \+ Postman Console** for repeating and debugging requests.

---

## **3\) ⏱ Time Estimate (Total: 3 hours)**

* **1 hour** → UI \+ Theory  
* **2 hours** → Hands-on practice & repetition (5 GET calls \+ query params \+ save to collection \+ history \+ console)

---

## **4\) 📚 Theory (simple explanation \+ where to see in Postman \+ Nepal real-life scenarios)**

### **4.1 What is Postman (in QA testing)?**

Postman is your **API testing lab**. Instead of clicking a mobile app or website, you directly send HTTP requests (like GET) to an API and inspect response.

* **Where to see in Postman:** You work mainly in the **Request Builder** tab (top work area) and inspect results in the **Response area** (bottom).  
* **Nepal scenario (simple):**  
  * A “Municipality Citizen Service” app has a “Notices” screen. That screen is basically doing a GET request like: “Give me latest notices.”

---

### **4.2 What is a GET request?**

**GET \= retrieve data** from server (read-only, should not change data).

* **Where to see in Postman:** Method dropdown → choose **GET**, enter URL, click **Send**.  
* **Nepal scenarios:**  
  * Tourism app: “List hotels in Pokhara” (GET hotels)  
  * Bus app: “Show routes Kalanki → Chitwan” (GET routes)

**QA mindset for GET (basic checks):**

* Valid request returns **200** and correct JSON keys.  
* Invalid ID or missing resource should give meaningful behavior (often 404).

---

### **4.3 What is an Endpoint?**

Endpoint \= the “address” you call. Typically:

* **Base URL** \+ **Path** (+ optional query parameters)  
  Example idea:  
* Base: `https://api.mycity.gov.np`  
* Path: `/notices`  
* Full endpoint: `https://api.mycity.gov.np/notices`

In today’s practice we use public dummy APIs (JSONPlaceholder / ReqRes) because they are safe for learning. ([jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com/?utm_source=chatgpt.com))

---

### **4.4 What are Query Parameters?**

Query parameters are key-value pairs after `?` used for filtering/search/pagination etc.

* Example format: `?key1=value1&key2=value2`  
* **Where to see in Postman:** **Params tab** (below URL) OR type directly in URL — Postman syncs both. ([Postman Docs](https://learning.postman.com/docs/sending-requests/create-requests/parameters/?utm_source=chatgpt.com))

**Nepal scenario examples (very practical):**

* **Pagination:** “Show page 2 of notices” → `?page=2` (common in listing screens)  
* **Filtering:** “Show scholarships for Grade 12 only” → `?grade=12`  
* **Searching:** “Search citizen by name” → `?q=Sagar`

---

## **5\) 🧠 Key Concepts (detailed \+ QA checks \+ where to see in Postman \+ Nepal examples)**

### **5.1 Postman UI overview (Requests, Collections, Environments)**

**A) Request (tab)**

* **Meaning:** A single API call setup (method \+ URL \+ params \+ headers).  
* **Where in Postman:** New HTTP request tab (Request Builder). ([Postman Docs](https://learning.postman.com/docs/postman/launching-postman/creating-the-first-collection/?utm_source=chatgpt.com))  
* **QA checks:**  
  * Method chosen correctly (GET for read-only)  
  * URL correct (no extra slash, correct base)  
  * Params are correct and encoded properly  
* **Nepal scenario:** “GET list of schools in ward 5” request tab can be saved and reused.

**B) Collections**

* **Meaning:** A folder to store and organize requests (like “Project file”). ([Postman Docs](https://learning.postman.com/docs/collections/use-collections/use-collections-overview/?utm_source=chatgpt.com))  
* **Where in Postman:** Sidebar → **Collections**.  
* **How to save:** Click **Save** in request, name it, select collection. ([Postman Docs](https://learning.postman.com/docs/collections/use-collections/add-requests-to-collections/?utm_source=chatgpt.com))  
* **QA checks:**  
  * Naming standard: `GET_ListUsers_Page2` (clear for team)  
  * Group by module: `User`, `Posts`, `Comments`, etc.  
* **Nepal scenario:** For a Municipality project: Collection \= `Tarakhola API`, folders \= `Citizen`, `Tax`, `Notice`.

**C) Environments**

* **Meaning:** A switchable set of variables (DEV/STAGING/PROD). Routine mentions environments as Day 6 UI scope.  
* **Where in Postman:** Environment selector (top area) \+ Variables/Environments section.  
* **Why QA uses it:** Same request, different base URL (dev vs prod).  
* **Variables in environment (basic):** Postman supports storing and reusing values using variables and scopes. ([Postman Docs](https://learning.postman.com/docs/postman/environments_and_globals/variables/?utm_source=chatgpt.com))  
* **Nepal scenario:**  
  * DEV API for local school demo: `https://dev.api.school.edu.np`  
  * PROD API for live system: `https://api.school.edu.np`  
    QA switches environment instead of rewriting 50 URLs.

---

### **5.2 Anatomy of a GET request (what parts QA must look at)**

A GET request normally includes:

1. **Method:** GET  
2. **URL/Endpoint** (base \+ path)  
3. **Query Params** (optional)  
4. **Headers** (today: only observe; deep header testing was Day 4\)

**Where to see results in Postman (Response):**

* **Status Code** (top of response)  
* **Response Body** tab (JSON)  
* **Response Headers** tab (metadata)  
* **Time** shown near response (basic performance clue)

**Nepal QA scenario:**  
A “Result Publishing API” for a college:

* GET `/results?symbol=12345`  
  QA checks:  
* 200 for valid symbol, 404/400 for invalid symbol  
* Response has fields: name, marks, grade, pass/fail  
* Time is not too slow (students will complain)

---

### **5.3 Query Parameters in Postman (how \+ QA checks)**

**How to add query params:**

* Type directly in URL: `...?page=2`  
* OR use **Params tab** and fill key-value; Postman syncs both. ([Postman Docs](https://learning.postman.com/docs/sending-requests/create-requests/parameters/?utm_source=chatgpt.com))

**QA checks for query params (from API.pdf guidance):**

* Missing param  
* Invalid value type  
* Multiple filters and combinations

**Nepal examples to teach students:**

* `?page=2` → “Second page of notices” (pagination)  
* `?city=Pokhara` → “Hotels only in Pokhara” (filter)  
* `?priceMax=3000` → “Budget hotels under NPR 3000” (filter)

---

### **5.4 History tab (repeat \+ learn from past calls)**

Routine bonus says use History tab for repeating and analyzing calls.

* **Where to see:** Sidebar → **History** ([Postman Docs](https://learning.postman.com/docs/postman/sending-api-requests/working-with-tabs/?utm_source=chatgpt.com))  
* You can click an older request to reopen it in a new tab. ([Postman Docs](https://learning.postman.com/docs/postman/sending-api-requests/working-with-tabs/?utm_source=chatgpt.com))  
* You can also save a request from History to a Collection. ([Postman Docs](https://learning.postman.com/docs/collections/use-collections/add-requests-to-collections/?utm_source=chatgpt.com))

**Nepal scenario:**  
Yesterday you tested “School attendance list API”. Today you forgot URL/params. History helps you reopen instantly.

---

### **5.5 Postman Console (debugging visibility)**

Routine bonus says use console logs.

* **What it shows:** Every network call \+ headers \+ payloads \+ script logs. ([Postman](https://www.postman.com/postman/postman-team-collections/collection/c8w949c/how-to-use-the-postman-console?utm_source=chatgpt.com))  
* **How to open:** View → Show Postman Console OR shortcut `CMD/CTRL + ALT + C`. ([Postman](https://www.postman.com/postman/postman-team-collections/collection/c8w949c/how-to-use-the-postman-console?utm_source=chatgpt.com))

**When QA uses Console (real):**

* “I sent request but server says param missing” → Console shows the exact URL sent and outgoing headers. ([Postman](https://www.postman.com/postman/postman-team-collections/collection/c8w949c/how-to-use-the-postman-console?utm_source=chatgpt.com))  
* “Why is my query param not included?” → Console helps confirm the final request.

---

## **6\) 🔐 Authentication Basics to Advanced**

**Not in Day 6 scope.** (Day 6 routine is Environment \+ GET \+ query params \+ save \+ history/console.)

---

## **7\) 🛠 Step-by-step Postman Practical (tasks \+ steps)**

### **✅ Task Set (must complete today)**

1. Create **1 Collection**: `Day6_GET_Practice`  
2. Create **1 Environment**: `PublicAPIs_DEV` (basic setup)  
3. Make **5 GET calls** (mix JSONPlaceholder \+ ReqRes)  
4. Use **Query Params** at least in 2 calls (one must be `?page=2`)  
5. Use **History tab** to repeat 2 old calls  
6. Open **Postman Console** and inspect 1 request’s outgoing details

---

### **7.1 Create Environment (basic)**

1. Create environment: `PublicAPIs_DEV`  
2. Add variable (basic):  
   * `json_base` \= `https://jsonplaceholder.typicode.com` ([jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com/?utm_source=chatgpt.com))  
   * `reqres_base` \= `https://reqres.in/api` ([openpublicapis.com](https://openpublicapis.com/api/reqres?utm_source=chatgpt.com))  
3. Select this environment in the environment selector (environment must be active to use it). ([Postman Docs](https://learning.postman.com/docs/postman/environments_and_globals/variables/?utm_source=chatgpt.com))

**Why this matters (teacher talk):**  
Tomorrow when you practice again, you only change one variable, not every request URL.

---

### **7.2 Make 5 GET calls (copy-paste safe practice URLs)**

Use variables (recommended):

{{json\_base}}/posts/1

{{json\_base}}/posts

{{json\_base}}/comments?postId=1

{{reqres\_base}}/users/2

{{reqres\_base}}/users?page=2

These endpoints are publicly documented for learning and support GET routes (including `comments?postId=1` and pagination examples). ([jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com/?utm_source=chatgpt.com))

#### **For each request, do this same checklist (very important habit):**

1. Method \= **GET**  
2. Paste URL  
3. If query param needed, use **Params tab** (key/value) OR URL (both sync). ([Postman Docs](https://learning.postman.com/docs/sending-requests/create-requests/parameters/?utm_source=chatgpt.com))  
4. Click **Send**  
5. Observe and write down:  
   * Status code (expect 200 mostly)  
   * Response time (ms)  
   * Body (JSON)  
   * Headers (Content-Type etc.)

---

### **7.3 Use Query Params properly (must do today)**

**Example A (ReqRes pagination):**

* `GET {{reqres_base}}/users?page=2` ([openpublicapis.com](https://openpublicapis.com/api/reqres?utm_source=chatgpt.com))  
  In Params tab:  
* Key: `page`  
* Value: `2` ([Postman Docs](https://learning.postman.com/docs/sending-requests/create-requests/parameters/?utm_source=chatgpt.com))

**Example B (JSONPlaceholder filter by postId):**

* `GET {{json_base}}/comments?postId=1` ([jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com/?utm_source=chatgpt.com))

**QA checks to try (2 negative tests):**

* Remove query param → compare response  
* Change value type (e.g., `page=abc`) → observe behavior (some public APIs still respond, but you must note it)

---

### **7.4 Save requests to Collection (required)**

After each request works:

1. Click **Save**  
2. Name it clearly (examples):  
   * `GET_Post_1`  
   * `GET_Comments_By_postId_1`  
   * `GET_ReqRes_Users_Page2`  
3. Choose your collection `Day6_GET_Practice` and Save ([Postman Docs](https://learning.postman.com/docs/collections/use-collections/add-requests-to-collections/?utm_source=chatgpt.com))

---

### **7.5 Use History tab (repeat \+ analyze)**

1. Open **History** from sidebar ([Postman Docs](https://learning.postman.com/docs/postman/sending-api-requests/working-with-tabs/?utm_source=chatgpt.com))  
2. Click any previous request → it opens in a new tab ([Postman Docs](https://learning.postman.com/docs/postman/sending-api-requests/working-with-tabs/?utm_source=chatgpt.com))  
3. Repeat 2 requests and compare:  
   * Are status \+ body same?  
   * Any time difference?

---

### **7.6 Use Postman Console (debug proof)**

1. Open Console (`CMD/CTRL + ALT + C`) ([Postman](https://www.postman.com/postman/postman-team-collections/collection/c8w949c/how-to-use-the-postman-console?utm_source=chatgpt.com))  
2. Send `GET {{reqres_base}}/users?page=2` again  
3. In console, find the network entry and observe:  
   * Final URL (does it include `?page=2`?)  
   * Request/response headers logged ([Postman](https://www.postman.com/postman/postman-team-collections/collection/c8w949c/how-to-use-the-postman-console?utm_source=chatgpt.com))

---

## **8\) 🧾 QA Test Case Template (table)**

| TC ID | Title | Precondition | Method | Endpoint / URL | Query Params | Steps | Expected Result | What to Capture in Evidence |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| TC-GET-01 | Fetch single post | Postman opened | GET | `{{json_base}}/posts/1` | N/A | Send request | Status 200 \+ JSON body returned | Status \+ Time \+ Body screenshot/text |
| TC-GET-02 | Fetch all posts | Environment selected | GET | `{{json_base}}/posts` | N/A | Send request | Status 200 \+ list/array of posts | Status \+ first 3 items proof |
| TC-QP-01 | Filter comments by postId | Environment selected | GET | `{{json_base}}/comments` | `postId=1` | Add in Params tab → Send | Status 200 \+ comments for that post | URL proof \+ Params tab proof |
| TC-QP-02 | Pagination page 2 users | Environment selected | GET | `{{reqres_base}}/users` | `page=2` | Add in Params tab → Send | Status 200 \+ users page 2 | Console proof shows final URL |
| TC-HIS-01 | Repeat call from History | At least 3 requests sent | GET | From History | N/A | Open History → open request → Send | Same response structure, reusability | History entry \+ response compare |
| TC-CON-01 | Validate query param sent | Console opened | GET | `{{reqres_base}}/users` | `page=2` | Send request → check Console | Console shows correct final URL and headers | Console screenshot/log snippet |

(These tests align with the Day 6 routine: 5 GET calls \+ query parameters \+ collection saving \+ history/console use.)

---

## **9\) ✅ Day Summary Checklist (tick before ending class)**

* I can create a new GET request and send it successfully  
* I understand endpoint \= base URL \+ path (and optional query params)  
* I can add query params via **Params tab** and confirm it updates URL ([Postman Docs](https://learning.postman.com/docs/sending-requests/create-requests/parameters/?utm_source=chatgpt.com))  
* I completed 5 GET calls and saved them into a collection ([Postman Docs](https://learning.postman.com/docs/collections/use-collections/add-requests-to-collections/?utm_source=chatgpt.com))  
* I used History to reopen a request ([Postman Docs](https://learning.postman.com/docs/postman/sending-api-requests/working-with-tabs/?utm_source=chatgpt.com))  
* I opened Postman Console and verified final URL/params ([Postman](https://www.postman.com/postman/postman-team-collections/collection/c8w949c/how-to-use-the-postman-console?utm_source=chatgpt.com))

---

## **10\) 📝 Revision Tasks (homework)**

1. Redo the same 5 GET calls tomorrow **without looking** at today’s notes (use your Collection).  
2. For 2 requests, change query param values and write observations:  
   * What changed in response body?  
   * What stayed same?  
3. Use History: find one request from yesterday and save it into your Collection from History. ([Postman Docs](https://learning.postman.com/docs/postman/sending-api-requests/working-with-tabs/?utm_source=chatgpt.com))  
4. Open Postman Console and answer in 3 lines (teacher-style):  
   * “What did Console show that normal response area didn’t?” ([Postman](https://www.postman.com/postman/postman-team-collections/collection/c8w949c/how-to-use-the-postman-console?utm_source=chatgpt.com))  
5. Nepal scenario writing (short):  
   * Write 2 imaginary endpoints for a Nepali municipality app and add one query param each (pagination/filter).

