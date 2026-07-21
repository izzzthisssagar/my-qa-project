---
title: "The CI/CD pipeline"
tags: ["agile-and-devops-for-testers", "shift-left-and-cicd", "the-cicd-pipeline"]
updated: "2026-07-20"
---

# The CI/CD pipeline

*Where automated tests actually run in a CI/CD pipeline - build, unit, integration, e2e, then deploy - what a tester owns versus what a platform engineer owns, and the basics of pipeline-as-code.*

> A developer pushes a commit and, ten minutes later, sees a red X next to it - no human ran a single test by
> hand. Somewhere between that push and the red X, code got compiled, a battery of automated tests ran in a
> specific order, and the whole thing stopped before it ever reached anything a user could touch. That ordered,
> automatic sequence is the CI/CD pipeline, and knowing exactly which stage failed - and whose job that stage
> is - is one of the most practical skills a tester on a modern team can have.

> **In real life**
>
> Think of an actual factory assembly line building a car, not a metaphorical one. Nothing gets painted before
> the frame is welded, nothing gets wired before the panels are on, and a car with a cracked weld gets pulled
> off the line at the welding station - it never reaches the paint booth, let alone the customer lot. Every
> station does one job, checks its own work before waving the car forward, and a failure at any station stops
> that specific car right there instead of quietly riding the line to the end. A CI/CD pipeline runs on the
> identical logic: build, then a sequence of increasingly realistic tests, then deploy - each stage gating the
> next, so a broken commit gets caught at the earliest station capable of catching it, not at the loading dock.

**CI/CD pipeline**: A CI/CD pipeline is an automated, ordered sequence of stages - typically build, then automated tests of increasing scope, then deployment - defined as code in a configuration file, that runs every time code changes and must complete successfully before that change is considered ready to ship.

## The stages, in the order they actually run

A typical pipeline runs five kinds of stages, each one gating the next. **Build** comes first: the code
compiles or bundles into a runnable artifact, and if this fails, nothing else even starts - there's no
application yet to test. **Unit tests** run next, fast and isolated, checking individual functions or classes
in complete isolation from databases, networks, or other services; they're cheap enough to run on every
single commit. **Integration tests** come after, checking that components actually work together - a service
talking to a real (or realistic) database, two internal services calling each other over the network.
**End-to-end tests** run against something close to the full system, usually in a staging environment,
driving real user flows through a real (or close-to-real) UI or API surface. Only after all of that survives
does **deploy** run, pushing the build to production or to the next environment in line. The further right a
stage sits, the slower and more expensive it is to run - which is exactly why fast, cheap unit tests run
first and catch what they can before anything spends time on a full end-to-end run.

## Who owns which part

On most teams, ownership splits cleanly, even if the split isn't always written down anywhere. A **tester**
typically owns the test code itself: writing and maintaining the unit, integration, and end-to-end tests,
deciding what "passing" actually means for a given stage, and maintaining the test data and fixtures those
tests depend on. A **platform or DevOps engineer** typically owns the pipeline's plumbing: the CI/CD tooling
itself, the runners or agents that execute each stage, how secrets and credentials get injected safely,
provisioning the environments tests run against, and how a deployment actually gets rolled out or rolled
back. Neither role can do the other's job well without talking to the other - a tester who doesn't know how
staging environments get provisioned can't debug a flaky integration-stage failure, and a platform engineer
who doesn't know what a test stage is actually checking can't safely change how or when it runs.

> **Tip**
>
> When a pipeline stage fails, read the stage name before reading the error. "unit-tests" failing usually
> means a tester's problem (a real regression, or a test that needs updating); "provision-staging-env" failing
> usually means a platform problem (infrastructure, not application logic). Knowing which owner to loop in
> first turns a shared Slack channel scramble into a two-minute fix.

> **Common mistake**
>
> Writing end-to-end tests for everything a unit test could have covered instead. End-to-end stages are slow
> and run against real, shared infrastructure - loading them up with checks a unit test could catch in
> milliseconds makes every pipeline run slower for everyone, and a slow pipeline is one people start skipping
> or running less often, which quietly undoes the whole point of catching problems early.

![A car factory assembly line with several cars at different stages of completion - one in the foreground with its hood open being worked on, others further down the line with doors and trunks open or fully closed, overhead tooling suspended above the line](the-cicd-pipeline.jpg)
*Car assembly line, General Motors Manufacturing Poland, Gliwice - Marek Slusarczyk, Wikimedia Commons, CC BY 3.0. [Source](https://commons.wikimedia.org/wiki/File:002_Production_line_-_car_assembly_line_in_General_Motors_Manufacturing_Poland_-_Gliwice,_Poland.jpg)*
- **Hood open, protective covers on - still being built** — This is the build stage made physical: raw components going together, nowhere near ready for anyone to evaluate it as a finished thing yet.
- **Trunk and doors still open, mid-line** — Further along than the first car, but still open for inspection at this point - the equivalent of an integration or end-to-end stage, where the system is assembled enough to test but not yet sealed up and shipped.
- **Overhead tooling fixed above the line** — This station runs the identical check on every single car that passes underneath it, the same way an automated pipeline stage runs the same tests against every commit, not a custom check per build.
- **Doors and hood closed, further down the line** — This car already survived every station behind it - the pipeline only lets a car this far if it passed what came before, exactly like a build that only reaches deploy after every earlier stage passed.

**One commit's trip through the pipeline - press Play**

1. **Build** — The code compiles or bundles into a runnable artifact. Nothing downstream can start until this succeeds - there's no application yet to run a single test against.
2. **Unit tests** — Fast, isolated checks run against that artifact. Cheap enough to run on every commit, and they fail the pipeline before anything slower even starts.
3. **Integration and end-to-end tests** — The artifact runs against real or realistic dependencies, then against full user flows in something close to production.
4. **Deploy** — Only a build that survived every earlier stage reaches this one - a pipeline that deploys after a failed test stage isn't actually gating anything.

Here is a small pipeline runner: it executes each stage in order and stops at the first failure, which is
the fail-fast behavior a real CI/CD pipeline relies on - notice deploy never even attempts to run once an
earlier stage fails.

*A fail-fast pipeline runner (Python)*

```python
stages = [
    ("build", True),
    ("unit_tests", True),
    ("integration_tests", True),
    ("e2e_tests", False),
    ("deploy", True),
]

def run_stage(name, passed):
    print(name.upper() + "=" + ("PASS" if passed else "FAIL"))
    return passed

stopped_at = None
for name, passed in stages:
    ok = run_stage(name, passed)
    if not ok:
        stopped_at = name
        break

result = "PASS" if stopped_at is None else "FAIL"
assert result == "FAIL", "expected the pipeline to stop before deploy"
print("RESULT=" + result)
```

*A fail-fast pipeline runner (Java)*

```java
import java.util.*;

public class Main {
    static class Stage {
        String name;
        boolean passed;
        Stage(String name, boolean passed) { this.name = name; this.passed = passed; }
    }

    static boolean runStage(Stage s) {
        System.out.println(s.name.toUpperCase() + "=" + (s.passed ? "PASS" : "FAIL"));
        return s.passed;
    }

    public static void main(String[] args) {
        List<Stage> stages = new ArrayList<>();
        stages.add(new Stage("build", true));
        stages.add(new Stage("unit_tests", true));
        stages.add(new Stage("integration_tests", true));
        stages.add(new Stage("e2e_tests", false));
        stages.add(new Stage("deploy", true));

        String stoppedAt = null;
        for (Stage s : stages) {
            boolean ok = runStage(s);
            if (!ok) {
                stoppedAt = s.name;
                break;
            }
        }

        String result = stoppedAt == null ? "PASS" : "FAIL";
        if (!result.equals("FAIL")) throw new AssertionError("expected the pipeline to stop before deploy");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Reading a pipeline configuration for the first time

- [ ] Find the pipeline-as-code file — Look for .github/workflows/*.yml, .gitlab-ci.yml, or a Jenkinsfile in the repo root - the pipeline's actual definition lives in version control, not in a UI someone configured by hand.
- [ ] List the stages in the order they run — Read the file top to bottom (or trace the 'needs'/'stage' dependencies) to find the real order - build, tests of increasing scope, then deploy.
- [ ] Find which stages are tests you'd recognize — Match unit, integration, and end-to-end test commands to stage names - the labels vary by team, but the shape rarely does.
- [ ] Ask who owns the file itself — Confirm whether changes to the pipeline definition go through a platform team, the whole team, or whoever touched it last - that tells you where to route a pipeline-infrastructure problem versus a test-code problem.

- **A pipeline stage named 'e2e-tests' takes twenty minutes and fails constantly for reasons unrelated to the code change.**
  This usually means checks that belong in a fast unit or integration stage got pushed into the slow, flaky end-to-end stage instead. Audit what's actually being checked there and move anything that doesn't need a full running system to an earlier, cheaper stage.
- **Deploy runs even though an earlier test stage failed.**
  The pipeline isn't actually gating - stages either aren't configured to depend on each other, or a failure is being swallowed somewhere. This is a pipeline-as-code configuration problem, worth routing to whoever owns the pipeline file, not a test problem.
- **A tester can't tell whether a failing stage is a real regression or a broken test environment.**
  Check the stage name and what it depends on: a test-code failure usually reproduces locally with the same test command, while an environment failure (provisioning, secrets, network) usually doesn't. When it's unclear, loop in whoever owns the pipeline plumbing rather than guessing.

### Where to check

- The pipeline-as-code file itself (.github/workflows, .gitlab-ci.yml, Jenkinsfile) for the real, current stage order - not a diagram someone drew a year ago.
- The last five pipeline runs on the main branch, to see which stage actually fails most often and how long each stage takes.
- Whether unit test stages run before integration and end-to-end stages, or whether slow stages run first and waste time on commits that would have failed a cheap check anyway.
- [[agile-and-devops-for-testers/shift-left-and-cicd/quality-gates]] for what actually decides pass or fail inside each of these stages.
- [[agile-and-devops-for-testers/shift-left-and-cicd/continuous-testing]] for how testing spreads across every one of these stages instead of living in just one of them.

### Worked example: the twenty-minute pipeline that used to take four

1. **The setup:** A team's pipeline used to finish in four minutes. Over six months of adding features, it
   now takes twenty, and developers have started skipping local test runs because "the pipeline will catch
   it anyway, eventually."
2. **The tester investigates stage by stage:** Ninety percent of the added time sits in the end-to-end stage
   - most of the new checks added there are testing individual validation rules that never touch a database
   or a second service.
3. **The root cause:** New tests kept getting added to whichever stage was already running, not to the
   cheapest stage that could actually catch that specific kind of problem - end-to-end became a dumping
   ground instead of a stage reserved for full user-flow checks.
4. **The fix:** The tester moves roughly two-thirds of the end-to-end checks into the unit and integration
   stages, where they run in milliseconds instead of minutes, and end-to-end shrinks back to genuine
   full-flow scenarios only.
5. **The lesson:** A stage's speed is a direct function of what's actually assigned to run there - a pipeline
   doesn't get slow on its own, it gets slow one misplaced test at a time.

**Quiz.** A commit fails the unit-tests stage. What happens to the later stages in a correctly configured pipeline?

- [ ] Integration and end-to-end tests still run, but deploy is skipped
- [x] All later stages - integration tests, end-to-end tests, and deploy - are skipped, because the pipeline stops at the first failed stage
- [ ] Only deploy runs, to confirm whether the failure matters in production
- [ ] The pipeline reruns the unit tests automatically until they pass

*A correctly configured pipeline is fail-fast: each stage gates the next, so a failure at any stage stops everything after it. Integration tests, end-to-end tests, and deploy all depend on the stages before them succeeding, so none of them run once unit tests fail.*

- **The typical CI/CD stage order** — Build, then unit tests, then integration tests, then end-to-end tests, then deploy - each stage gating the next, cheapest and fastest checks first.
- **Tester ownership vs platform/DevOps ownership** — A tester typically owns test code, what 'passing' means, and test data. A platform engineer typically owns the pipeline tooling, runners, secrets, and environment provisioning.
- **Pipeline-as-code, in one line** — The pipeline's definition lives in a version-controlled file in the repo (a workflow YAML or a Jenkinsfile) rather than in a UI someone configured by hand - so it's reviewable, versioned, and reproducible like any other code.

### Challenge

Open your team's actual pipeline-as-code file and list every stage in the order it runs. For each stage, write down in one sentence who owns fixing a failure there - a tester, a platform engineer, or genuinely both - and flag any stage where you're not sure.

- [GitLab Docs - CI/CD pipelines](https://docs.gitlab.com/ci/pipelines/)
- [GitHub Docs - Understanding GitHub Actions](https://docs.github.com/en/actions/get-started/understanding-github-actions)
- [The CI/CD Pipeline, Explained](https://www.youtube.com/watch?v=w6Y19RWawc0)

🎬 [The CI/CD Pipeline, Explained](https://www.youtube.com/watch?v=w6Y19RWawc0) (5 min)

- A CI/CD pipeline runs build, then unit tests, then integration tests, then end-to-end tests, then deploy - each stage gating the next, cheapest checks first.
- A tester typically owns test code and what 'passing' means for a stage; a platform or DevOps engineer typically owns the pipeline tooling, runners, and environments.
- Pipeline-as-code means the pipeline's definition lives in a version-controlled file in the repo, reviewable and reproducible like any other code.
- A pipeline is fail-fast by design - a failure at any stage stops everything after it, including deploy.


## Related notes

- [[Notes/agile-and-devops-for-testers/shift-left-and-cicd/shift-left|Shift-left]]
- [[Notes/agile-and-devops-for-testers/shift-left-and-cicd/quality-gates|Quality gates]]
- [[Notes/agile-and-devops-for-testers/shift-left-and-cicd/continuous-testing|Continuous testing]]


---
_Source: `packages/curriculum/content/notes/agile-and-devops-for-testers/shift-left-and-cicd/the-cicd-pipeline.mdx`_
