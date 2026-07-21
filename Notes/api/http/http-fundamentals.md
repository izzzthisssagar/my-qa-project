---
title: "HTTP fundamentals"
tags: ["api", "http", "fundamentals"]
updated: "Thu Jul 02 2026 05:45:00 GMT+0545 (Nepal Time)"
---

# HTTP fundamentals

*The request/response model, methods, status codes, and headers — the vocabulary every API tester speaks.*

HTTP is a **stateless request/response** protocol. A client sends a request; the
server returns a response. Each exchange stands alone — any state (who you are,
what's in your cart) must be carried explicitly, usually in headers or tokens.

## Anatomy of a request

- **Method** — the intent: `GET` (read), `POST` (create), `PUT`/`PATCH`
  (update), `DELETE` (remove).
- **URL** — the resource, often with a query string (`/tickets?status=open`).
- **Headers** — metadata: `Authorization`, `Content-Type`, `Accept`.
- **Body** — the payload (JSON, form data) for writes.

## Anatomy of a response

- **Status code** — a three-digit verdict (see below).
- **Headers** — `Content-Type`, `Location`, rate-limit headers, caching.
- **Body** — the representation of the resource or an error envelope.

## Status code families

| Range | Meaning | Examples |
|-------|---------|----------|
| `2xx` | Success | `200 OK`, `201 Created`, `204 No Content` |
| `3xx` | Redirection | `301 Moved`, `304 Not Modified` |
| `4xx` | Client error | `400 Bad Request`, `401 Unauthorized`, `404 Not Found`, `429 Too Many Requests` |
| `5xx` | Server error | `500 Internal Server Error`, `503 Unavailable` |

## Why testers care

Most API bugs are **contract violations**: the wrong status code (a `200` where
the spec says `201`), a missing header, or a body shape that doesn't match the
schema. Knowing the correct HTTP semantics is what lets you spot them — practise
against the BuggyAPI bug-hunt to see these exact deviations live.


---
_Source: `packages/curriculum/content/notes/api/http/http-fundamentals.mdx`_
