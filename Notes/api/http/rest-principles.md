---
title: "REST principles"
tags: ["api", "rest", "architecture"]
updated: "Fri Jul 03 2026 05:45:00 GMT+0545 (Nepal Time)"
---

# REST principles

*What makes an API "RESTful" — resources, uniform methods, statelessness — and how each principle turns into a test.*

**REST** (Representational State Transfer) is an architectural style for APIs
built on the web's own mechanics. An API is "RESTful" to the degree it follows a
handful of constraints — each of which suggests things to test.

## The core constraints

- **Resources & URIs** — everything is a **noun** addressed by a URL:
  `/tickets`, `/tickets/42`. Not verbs (`/getTicket`). *Test:* URLs name
  resources, not actions.
- **Uniform interface via HTTP methods** — `GET` reads, `POST` creates, `PUT`/
  `PATCH` update, `DELETE` removes. *Test:* each method does what it says and
  nothing more.
- **Statelessness** — each request carries everything needed; the server keeps no
  session between calls. *Test:* the same request works in isolation, no hidden
  order dependency.
- **Representations** — a resource can be returned as JSON (usually), XML, etc.;
  `Content-Type`/`Accept` negotiate the format.
- **HATEOAS** — responses can include links to related actions. Rarely fully
  implemented, but its spirit (discoverability) is worth checking.

## Idempotency & safety

Two properties that drive real test cases:

- **Safe** methods (`GET`, `HEAD`) don't change state — calling one must never
  create or delete anything.
- **Idempotent** methods (`GET`, `PUT`, `DELETE`) give the same result if called
  repeatedly. *Test:* `DELETE` the same id twice — the second call shouldn't
  error out or double-act. `POST` is **not** idempotent (two POSTs = two rows).

## Why the model helps

REST gives you a mental checklist. When an endpoint violates a principle — a
`GET` that mutates data, a `POST` that isn't reflected in a later `GET`, an
order-dependent call — you've found a defect. See [status codes](/notes/api/http/status-codes)
for the verdicts these operations should return.


---
_Source: `packages/curriculum/content/notes/api/http/rest-principles.mdx`_
