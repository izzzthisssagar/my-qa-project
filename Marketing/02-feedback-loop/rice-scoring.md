# RICE Scoring — How to Decide What to Build Next

RICE stops you from building by gut or by whoever shouted loudest. Score each feature/UX/content request, rank by score, build top-down.

## The formula

```
RICE score = (Reach × Impact × Confidence) ÷ Effort
```

| Factor | What it means | How to fill it |
|---|---|---|
| **Reach** | How many users affected per quarter | A number. Estimate from your user base / signups (e.g., 500). |
| **Impact** | How much it moves the needle per user | massive=3, high=2, medium=1, low=0.5, minimal=0.25 |
| **Confidence** | How sure are you about the above | high=100%, medium=80%, low=50% |
| **Effort** | Person-months of work | t-shirt size → number: xs=0.25, s=0.5, m=1, l=2, xl=3 |

> In the CSV you write words (`high`, `m`, etc.) for Impact / Confidence / Effort. The [`feedback_triage.py`](../05-automation/scripts/feedback_triage.py) script converts them to numbers and computes the score. Reach is a raw number.

## Worked example

> "Add an API testing track" — Reach 800, Impact high (2), Confidence medium (0.8), Effort l (2)
>
> RICE = (800 × 2 × 0.8) ÷ 2 = **640**

> "Loosen lab 3 grading" — Reach 400, Impact high (2), Confidence high (1.0), Effort s (0.5)
>
> RICE = (400 × 2 × 1.0) ÷ 0.5 = **1600** ← higher score, build first (small effort, real pain)

The small fix beats the big track — that's RICE doing its job. Quick wins that remove real pain usually rank high. Mix those with the occasional big bet.

## Rules of thumb

- **Bugs don't use RICE.** Triage by severity; Critical/High fixed before any feature.
- **A theme with 3+ requests** gets a Confidence bump — multiple users asking is evidence.
- **Re-score quarterly.** Reach and confidence change as you learn.
- **Don't over-precision.** RICE is for *ranking*, not exact truth. Rough numbers, consistent method.

## After scoring

The ranked list is your backlog. Take the top item that fits next week's capacity. Mark it `planned` in `feedback-intake.csv`, ship it, then `announced`. Publish the ranked list as your **public roadmap** so users see their requests in line.

See also `references/frameworks.md` in the product-manager-toolkit skill for MoSCoW / Kano alternatives, and the toolkit's `rice_prioritizer.py` for a heavier portfolio-analysis version.
