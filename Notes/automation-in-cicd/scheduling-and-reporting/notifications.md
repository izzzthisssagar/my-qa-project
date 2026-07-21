---
title: "Notifications"
tags: ["ci", "notifications", "alerting", "ownership", "track-d"]
updated: "2026-07-17"
---

# Notifications

*Useful CI notifications route actionable state changes to the right owner with revision, environment, failure fingerprint, evidence links, and recovery status—without training teams to ignore noise.*

> A channel receives 400 green pipeline messages a day. The first production-blocking regression lands
> between them and nobody opens it. The integration worked perfectly; the notification system failed.

> **In real life**
>
> A bell is valuable because its sound has agreed meaning: fire, class change, door, or alarm. If it
> rings for everything, people stop translating sound into action. CI notifications need the same
> contract between signal, audience, urgency, and response.

**Actionable CI notification**: A CI notification is a routed message about a pipeline state change that asks a defined audience to take or acknowledge an action. A complete notification identifies repository/workflow, branch and SHA, trigger and actor, environment, failed stage/job/test fingerprint, first occurrence or duration, evidence link, ownership, and current recovery state.

## Notify on decisions and transitions

```text
[BLOCKED] checkout-e2e · main · 8d21f4a · staging
3 failures · first seen 14:32 UTC · owner: payments-qa
fingerprint: timeout waiting for POST /orders
run: .../actions/runs/1842 · trace: .../artifacts/checkout-trace
```

This is better than “Build failed.” Deduplicate repeats, update a thread, and send a recovery message
when the same condition clears. Failure without recovery leaves stale operational truth.

> **Tip**
>
> Start with notifications for main/release failures, protected quality gates, scheduled-run absence,
> and prolonged queueing. Let personal subscriptions cover ordinary author-owned pull-request results.

> **Common mistake**
>
> Sending secrets, raw request bodies, or full logs into chat. Notifications should link to access-
> controlled evidence and redact tokens, credentials, customer data, and sensitive test fixtures.

![An opened electromechanical telephone ringer showing two brass bells, a striker, coils, and wiring](notifications.jpg)
*Bell of the 1900 — Gregory F. Maxwell, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Bell_of_the_1900.jpg)*
- **Signal** — A meaningful state transition should cause the bell to ring.
- **Routing mechanism** — Rules decide channel, owner, severity, deduplication, and escalation.
- **Inputs** — Pipeline status and metadata feed the notifier; sanitize them before delivery.
- **Recovery** — The second bell represents closure: notify when the incident is healthy again.

**From CI state to owned response**

1. **State changes** — A required job fails, schedule disappears, or release becomes blocked.
2. **Policy classifies** — Severity, branch, environment, recurrence, and owner are evaluated.
3. **Message is enriched** — Add SHA, actor, fingerprint, timestamps, and evidence links.
4. **Noise is controlled** — Deduplicate, thread repeats, suppress expected states, and rate-limit.
5. **Owner acknowledges** — A named team accepts, investigates, or escalates.
6. **Recovery closes** — A green rerun or fix updates the same incident context.

*Run it — deduplicate failure fingerprints (Python)*

```python
``failures = ["checkout|timeout|main", "checkout|timeout|main", "login|500|release"]
seen = set()
for fingerprint in failures:
    if fingerprint in seen:
        print("thread repeat:", fingerprint)
    else:
        seen.add(fingerprint)
        print("new alert:", fingerprint)``
```

*Run it — deduplicate failure fingerprints (Java)*

```java
``import java.util.*;

public class Main {
    public static void main(String[] args) {
        var failures = List.of("checkout|timeout|main", "checkout|timeout|main", "login|500|release");
        var seen = new HashSet<String>();
        for (String f : failures)
            System.out.println((seen.add(f) ? "new alert: " : "thread repeat: ") + f);
    }
}``
```

### Your first time: Your mission: design one owned CI alert

- [ ] Choose an actionable transition — State who must do what and by when.
- [ ] Enrich the message — Include run/SHA/environment, fingerprint, owner, and evidence links.
- [ ] Test duplicate and secret handling — Repeat the failure and inject a fake token to prove threading and redaction.
- [ ] Prove recovery — Fix or rerun the condition and confirm the incident closes visibly.

You now have a response loop, not a chat webhook.

- **The channel is noisy and failures are ignored.**
  Remove routine success spam, filter by decision significance, deduplicate fingerprints, and assign owners.
- **A message says only 'pipeline failed'.**
  Add workflow, branch/SHA, environment, failed job/test, first error, evidence link, and responsible team.
- **Every rerun creates a new incident.**
  Use a stable fingerprint and update a thread or incident until recovery.
- **Secrets appear in notification text.**
  Redact at the source, minimize payloads, restrict links, rotate exposed credentials, and audit message history.

### Where to check

- **Notifier condition** — branch, environment, status transition, and severity.
- **Payload template** — identity, owner, evidence, redaction, and timestamps.
- **Delivery/integration logs** — rejected webhook, permissions, quotas, and retries.
- **Fingerprint/thread state** — duplicate or stale incidents.
- **Acknowledgement and recovery** — whether anyone owns and closes the signal.

### Worked example: turning 400 messages into four useful alerts

1. A team posts every started, passed, skipped, and failed job into one channel.
2. A required release security test fails five retries, producing six disconnected messages.
3. The team limits shared alerts to protected-branch blockers, missing nightlies, and releases.
4. A fingerprint groups repeats; the message links the latest run and preserves first-seen time.
5. The owner acknowledges once, and a recovery update closes the thread after the fix.

**Quiz.** Which CI message is most actionable?

- [ ] Build failed
- [ ] Tests: red
- [x] Release checkout gate failed on SHA 8d21f4a in staging; fingerprint timeout-orders; owner payments-qa; trace and run linked
- [ ] Pipeline #1842 completed

*It identifies the decision, revision, environment, failure class, owner, and evidence needed to respond.*

- **Alert fingerprint** — Stable key used to group repeated instances of the same operational condition.
- **Signal-to-noise** — The proportion of messages that genuinely require the audience's attention.
- **Recovery notification** — Update showing the previously alerted condition is healthy again.
- **Actionable payload** — Identity, impact, owner, evidence, and requested response—not merely status.
- **Redaction** — Removal or masking of secrets and sensitive data before delivery.

### Challenge

Inventory one CI channel for a day. Classify every message by required action, owner, duplicate
fingerprint, and security risk. Redesign the policy and demonstrate failure, repeat, and recovery.

### Ask the community

> CI notification for [workflow] is [missing/noisy/duplicated]. Trigger policy, branch/environment, fingerprint, owner, payload fields, delivery log, and recovery behavior are [values].

Those details expose policy, transport, routing, and lifecycle problems.

- [GitHub Docs — workflow run notifications](https://docs.github.com/en/actions/concepts/workflows-and-actions/notifications-for-workflow-runs)
- [GitLab Docs — Slack integration reference](https://docs.gitlab.com/user/project/integrations/slack_slash_commands/)

🎬 [DevOps CI/CD Explained in 100 Seconds — Fireship](https://www.youtube.com/watch?v=scEDHsr3APg) (2 min)

- Notify on actionable decisions and transitions, not every job event.
- Include revision, environment, failure fingerprint, owner, timestamps, and evidence.
- Deduplicate repeats and close the loop with recovery state.
- Test delivery failure, redaction, acknowledgement, and escalation.
- Noise is a reliability defect because it trains the audience to ignore real blockers.


## Related notes

- [[Notes/automation-in-cicd/scheduling-and-reporting/publishing-reports|Publishing reports]]
- [[Notes/automation-in-cicd/scheduling-and-reporting/dashboards|Dashboards]]
- [[Notes/automation-in-cicd/flake-management/quarantine|Quarantine]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/scheduling-and-reporting/notifications.mdx`_
