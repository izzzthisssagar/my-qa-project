# Sample Lesson 1 — Boundary Value Analysis (A3.3)

**Type:** Visual concept lesson · **Time:** ~25 min · **Free-tier:** Yes (this is the shareable showpiece)
**Pattern:** See it → Try it → Do it → Prove it

---

## Hook (first screen, 15 seconds)

> **Where do bugs live?**
> Not in the middle. A field that accepts 1–99 almost never breaks at 50.
> It breaks at 0. At 1. At 99. At 100.
> **Bugs live at the edges.** This lesson teaches you to hunt there — with 6 tests instead of 99.

---

## Part 1 — SEE IT: The Boundary Slider (widget spec)

**Widget: `boundary-slider`**

- A real input field from BuggyShop: **Quantity (allowed: 1–99)** rendered above a horizontal number line 0–100.
- Learner drags a slider; at each value the field is auto-submitted and the response shows live: green tick (accepted) / red cross (rejected).
- The number line paints itself as the learner explores: green zone, red zones — making the *partition* visible.
- **The reveal:** at value 99 → green. At 100 → red. But drag to 0 → **green tick appears.** The widget freezes, zooms on the 0, and a caption appears: *"Wait. The spec said 1–99. You just found a real bug (BS-007) — by walking the boundary."*
- Sidebar updates with the formal vocabulary as the learner triggers each concept: boundary value, valid/invalid partition, off-by-one.

**Teaching beats (text blocks between interactions):**

1. **Why edges fail:** developers write `if (qty > 0)` when they meant `>= 1`, `<` when they meant `<=`. Off-by-one errors are the most common logic mistake in software — and they are invisible everywhere except the boundary.
2. **2-value BVA:** for each boundary, test the boundary itself and its nearest invalid neighbor. Range 1–99 → test {0, 1, 99, 100}.
3. **3-value BVA:** stricter variant adds the nearest valid neighbor inside: {0, 1, 2, 98, 99, 100}. When to use which: 3-value when the cost of escape is high (payments, limits, legal thresholds).
4. **BVA needs EP first:** boundaries only exist where partitions meet. (Callback link to A3.2.)

## Part 2 — TRY IT (guided)

Mini-walkthrough on a second field: **discount code length (5–10 characters)**.
- Learner is prompted: "What are the boundaries?" → picks values on a character-count line.
- Hints if stuck ("How many boundaries does a range have?" → 2; "What's the invalid neighbor of 5?" → 4).
- Expected answer: {4, 5, 10, 11} (2-value). Widget confirms with live submits.

## Part 3 — DO IT (lab, auto-graded)

**Task:** BuggyShop's product-list **price filter** accepts a max price 0–100000. Design the minimal 2-value BVA test set for the max-price input, then execute each value against the live filter and record accept/reject + filter behavior.

- Learner enters their chosen test values into a test-design grid (value, expected result, actual result).
- **Auto-grading:** expected value set {-1, 0, 100000, 100001} (order-independent; extra non-boundary values cost style points but don't fail).
- Executing 100000 correctly reveals **BS-008** (item priced exactly at max disappears — filter uses `<` instead of `<=`). The lab's final question: *"At which value did actual ≠ expected? What would you title this bug?"* (free text, rubric: identifies inclusive-boundary failure).
- **Completion reward:** "🐞 You found BS-008 — your second real bug. This exact bug class has shipped in production at companies you've heard of."

## Part 4 — PROVE IT (quiz, 6 questions)

1. A field accepts 18–60. Which is a 2-value BVA set? *(17,18,60,61)*
2. Why do bugs cluster at boundaries? *(off-by-one operator mistakes)*
3. 3-value BVA for 18–60? *(17,18,19,59,60,61)*
4. A tester tests 25, 40, 55 for the 18–60 field. What technique is missing and what's the risk?
5. True/false: BVA applies only to numbers. *(False — lengths, dates, file sizes, list counts)*
6. Scenario: signup allows age 18–100; QA tested 18 and 100 only, prod bug at 101 accepted. Which BVA rule was skipped? *(invalid neighbors)*

**Flashcards added to review queue:** 2-value BVA, 3-value BVA, partition, off-by-one.

---

## Production notes
- Widget `boundary-slider` is reused later in A3.2 (EP partitioner shares the number-line component) and B2 (assert-on-boundary demo).
- Marketing cut: 45-second screen recording of the slider hitting 0 → green tick → "you just found a bug" is the LinkedIn/reel asset for launch week.
- Standalone public version at `/play/boundary-hunter` (no signup, ends with "Want the full lesson? →") — this is the SEO link-magnet from plan §10.
