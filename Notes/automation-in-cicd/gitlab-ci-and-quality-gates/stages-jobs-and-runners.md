---
title: "Stages, jobs & runners"
tags: ["gitlab-ci", "pipelines", "runners", "track-d"]
updated: "2026-07-17"
---

# Stages, jobs & runners

*GitLab pipelines group independent jobs into ordered stages while runners execute each job in an isolated environment; needs can replace unnecessary stage waiting with explicit dependencies.*

> A GitLab pipeline is not one long script. It is a graph of jobs competing for runners and exchanging
> evidence. If you confuse a stage with a machine, or a runner with a pipeline, queue delays and missing
> artifacts become impossible to explain.

> **In real life**
>
> In a relay, each runner performs a leg and the baton is the handoff. Stages describe broad order;
> jobs are the runners; runners are the available lanes and people; artifacts carry what later work
> needs. A bad handoff can fail even when both runners are fast.

**GitLab stages, jobs, and runners**: A GitLab pipeline is a collection of jobs created for a source event. A job is an independent command unit with its own log and result, executed by a matching GitLab Runner. Stages group jobs into sequential phases; jobs in the same stage can run in parallel when runners are available. The needs keyword declares direct job dependencies and can let a job start before an entire earlier stage finishes.

## Model work at the correct level

```yaml
stages: [build, test]

build_app:
  stage: build
  script: ./build.sh
  artifacts:
    paths: [dist/]

unit_tests:
  stage: test
  needs: [build_app]
  script: ./test.sh
```

The job name is `build_app`. Its stage is `build`. A compatible runner executes it. `dist/` is the
handoff. `needs` states that unit tests require this job rather than every possible build-stage job.

> **Tip**
>
> Name jobs by the risk or output they own, not `test1`. A failed `contract-tests` check tells a reviewer
> what decision is blocked before opening the log.

> **Common mistake**
>
> Adding stages merely to force visual order. Stage barriers make every later job wait for every earlier
> job. Use `needs` for real dependencies and let independent feedback run early.

![Two runners reaching toward each other during a relay baton handoff](stages-jobs-and-runners.jpg)
*Relay race baton pass — Patrick Bell, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Relay_race_baton_pass.jpg)*
- **Upstream job** — One job produces a result and optional artifact.
- **Artifact handoff** — Files needed downstream must be declared, not assumed to remain on another runner.
- **Downstream job** — needs states the direct dependency and can start it without waiting for unrelated work.
- **Runner capacity** — Parallel-ready jobs still wait when no matching runner slot is available.

**From pipeline creation to job result**

1. **Pipeline created** — workflow/rules decide the event belongs.
2. **Jobs evaluated** — Job rules, stages, needs, tags, and variables form the graph.
3. **Jobs enter queue** — Ready work waits for matching runner capacity.
4. **Runner executes** — A runner obtains source, variables, and an isolated job environment.
5. **Artifacts pass** — Declared outputs become available to dependent jobs.
6. **Pipeline resolves** — Required job results roll into the pipeline and merge decision.

*Run it — find ready jobs in a DAG (Python)*

```python
``needs = {"build": [], "lint": [], "unit": ["build"], "e2e": ["build"]}
completed = {"build"}
ready = [job for job, deps in needs.items() if job not in completed and all(d in completed for d in deps)]
print("completed:", ", ".join(sorted(completed)))
print("ready:", ", ".join(ready))``
```

*Run it — find ready jobs in a DAG (Java)*

```java
``import java.util.*;

public class Main {
    public static void main(String[] args) {
        var needs = new LinkedHashMap<String, List<String>>();
        needs.put("build", List.of()); needs.put("lint", List.of());
        needs.put("unit", List.of("build")); needs.put("e2e", List.of("build"));
        var completed = Set.of("build");
        var ready = needs.entrySet().stream()
            .filter(e -> !completed.contains(e.getKey()) && completed.containsAll(e.getValue()))
            .map(Map.Entry::getKey).toList();
        System.out.println("completed: build");
        System.out.println("ready: " + String.join(", ", ready));
    }
}``
```

### Your first time: Your mission: explain one pipeline graph

- [ ] Open a pipeline and list every job by stage — Mark jobs running in parallel, skipped by rules, manual, failed, or waiting.
- [ ] Pick one queued job and inspect runner tags — Distinguish dependency waiting from missing compatible capacity.
- [ ] Trace one artifact handoff — Find producer path, retention, consumer needs/dependencies, and downloaded file.
- [ ] Replace one false stage barrier with needs — Measure feedback time while preserving the real dependency.

You now have an execution graph, not a colored row of boxes.

- **A job is stuck pending.**
  Read its pending reason; compare job tags, protected status, runner scope, online state, and available concurrency.
- **A downstream job cannot find build output.**
  Declare the producer artifact path and dependency with needs; runner workspaces are not shared implicitly.
- **A fast job waits behind an unrelated slow one.**
  Inspect stage barriers and add a direct needs relationship if the jobs are independent.
- **A failed job does not fail the pipeline.**
  Check allow_failure, rules, manual behavior, and whether the failing job belongs to the merge-request pipeline.

### Where to check

- **Pipeline graph** — stage barriers, needs edges, skips, manuals, and failures.
- **Job pending reason and runner tags** — dependency versus capacity/eligibility.
- **Job log and runner identity** — environment and first causal error.
- **Artifact browser/download** — exact producer output and expiry.
- **Pipeline source and SHA** — which event and revision the graph represents.

### Worked example: tests waiting for an unrelated image build

1. Stage `build` contains a 3-minute application build and a 20-minute container image build.
2. Unit tests need only the application bundle but wait for the whole stage.
3. The team declares `needs: [build_app]` on unit tests.
4. Tests start after three minutes while image work continues.
5. Deployment still needs both outputs, preserving safety while cutting feedback latency.

**Quiz.** When do jobs in the same GitLab stage run?

- [ ] Always sequentially in YAML order
- [x] In parallel when matching runner capacity is available
- [ ] Only after deployment
- [ ] On the same runner workspace

*Stages are sequential groups, but jobs inside one stage are independent and can run in parallel. Each job may use a separate runner environment.*

- **Pipeline** — The job graph created for one event/revision.
- **Job** — Independent command unit with its own runner execution, log, and result.
- **Stage** — Sequential phase grouping; all ordinary jobs in an earlier stage finish before the next.
- **Runner** — The agent application/environment that executes a compatible job.
- **needs** — Direct job dependency that creates DAG execution and artifact relationships.

### Challenge

Draw one GitLab pipeline as a DAG. Annotate each job's stage, tags, duration, needs, artifacts, and
merge significance. Remove one unnecessary barrier and prove the same failure still blocks safely.

### Ask the community

> GitLab job [name] in stage [stage] is [pending/waiting/failing]. Its needs, tags, runner status, artifact producer, and pipeline source/SHA are [values].

Those fields separate graph, capacity, handoff, and test failures.

- [GitLab Docs — CI/CD pipelines](https://docs.gitlab.com/ci/pipelines/)
- [GitLab Docs — CI/CD jobs](https://docs.gitlab.com/ci/jobs/)

🎬 [GitLab CI/CD Tutorial for Beginners — TechWorld with Nana](https://www.youtube.com/watch?v=qP8kir2GUgo) (69 min)

- Pipelines contain independent jobs; runners execute jobs; stages group broad order.
- Jobs in one stage can run in parallel only when compatible runner capacity exists.
- Artifacts are explicit handoffs because job workspaces are not implicitly shared.
- needs expresses true dependencies and removes unnecessary stage waiting.
- Diagnose pending, failed, skipped, and allowed-to-fail states separately.


## Related notes

- [[Notes/automation-in-cicd/gitlab-ci-and-quality-gates/gitlab-ci-yml|.gitlab-ci.yml]]
- [[Notes/automation-in-cicd/github-actions/workflow-basics|Workflow basics]]
- [[Notes/automation-in-cicd/jenkins/agents-and-plugins|Agents & plugins]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/gitlab-ci-and-quality-gates/stages-jobs-and-runners.mdx`_
