---
title: "Workflow basics"
tags: ["github-actions", "ci-cd", "yaml", "track-d"]
updated: "2026-07-17"
---

# Workflow basics

*A GitHub Actions workflow is a reviewed YAML file under .github/workflows that maps repository events to jobs, runners, and ordered steps whose exit codes produce visible checks.*

> GitHub Actions is not magic attached to a repository. It is a versioned program with an event as its
> input, temporary runners as its computers, and check results as its output. Once you read those three
> layers, a 200-line workflow stops looking like a wall of YAML.

> **In real life**
>
> A flowchart gives shapes different responsibilities: a start, a decision, a process, and an end. A
> workflow file does the same with `on`, `jobs`, `runs-on`, and `steps`. Indentation is the connector
> between them; put one block at the wrong depth and you have drawn a different process.

**GitHub Actions workflow**: A GitHub Actions workflow is a YAML file committed under .github/workflows. Its on key declares triggering events; jobs define independent units of work; each job chooses a runner with runs-on; and steps execute shell commands or reusable actions in order. Jobs run in parallel by default unless needs creates a dependency. A step's non-zero exit normally fails its job and exposes a check on the commit or pull request.

## Read it from the outside inward

```yaml
name: CI
on:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: 24
          cache: npm
      - run: npm ci
      - run: npm test
```

- `name` is the human-readable workflow label.
- `on` selects events; this example reacts to pull requests.
- `permissions` narrows the repository token instead of accepting broad defaults.
- `jobs.test` is the job identifier used by status checks and dependencies.
- `runs-on` chooses the runner environment.
- `steps` are ordered inside the job. `uses` invokes an action; `run` invokes the shell.

> **Tip**
>
> Give jobs stable, risk-based names such as `unit-tests` or `browser-chromium`. Branch protection
> requires check names, so renaming a vague `build` job later can quietly break the gate configuration.

> **Common mistake**
>
> Copying marketplace actions without pinning a reviewed version or minimizing token permissions. A
> workflow executes code with repository context; treat changes to `uses` and `permissions` like
> production dependency changes, not harmless YAML formatting.

![Four glossy flowchart shapes: red and green endpoints, an orange decision diamond, and a blue process rectangle](workflow-basics.png)
*Workflow icon set — RRZEicons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:Workflow.svg)*
- **Event starts** — The workflow's on block decides which repository event creates a run.
- **Conditions decide** — Event filters and if expressions decide whether work is relevant.
- **Job processes** — A job reserves one runner and executes its steps in order.
- **Result ends** — Step exit codes roll into a job result and visible repository check.

**From committed YAML to status check**

1. **Workflow discovered** — GitHub reads a .yml or .yaml file under .github/workflows.
2. **Event matches** — The on block and branch/path filters decide whether to create a run.
3. **Jobs planned** — Independent jobs become parallel work; needs creates explicit order.
4. **Runner allocated** — Each job receives a fresh hosted or selected self-hosted runner.
5. **Steps execute** — Reusable actions and shell commands run sequentially inside the job.
6. **Check reported** — Success, failure, cancellation, or skip attaches to the revision.

*Run it — model jobs and needs (Python)*

```python
``jobs = {
    "lint": [],
    "unit-tests": [],
    "browser-tests": ["unit-tests"],
}
completed = {"lint", "unit-tests"}
for job, needs in jobs.items():
    ready = all(item in completed for item in needs)
    print(f"{job}: {'ready' if ready else 'waiting'}")``
```

*Run it — model jobs and needs (Java)*

```java
``import java.util.*;

public class Main {
    public static void main(String[] args) {
        var jobs = new LinkedHashMap<String, List<String>>();
        jobs.put("lint", List.of());
        jobs.put("unit-tests", List.of());
        jobs.put("browser-tests", List.of("unit-tests"));
        var completed = Set.of("lint", "unit-tests");
        jobs.forEach((job, needs) -> {
            boolean ready = completed.containsAll(needs);
            System.out.println(job + ": " + (ready ? "ready" : "waiting"));
        });
    }
}``
```

### Your first time: Your mission: create one truthful pull-request check

- [ ] Create .github/workflows/ci.yml on a branch — Use pull_request, read-only contents permission, one clearly named job, and a hosted runner.
- [ ] Check out the repository and prepare its runtime — Use current reviewed action versions and an explicit runtime version.
- [ ] Run the clean install and one fast test command — Do not hide its exit status or add deployment yet.
- [ ] Open a pull request and inspect the job log — Confirm the intended SHA, commands, and check name; then deliberately fail one test.

You have a useful first workflow when the same check turns green and red for honest reasons.

- **GitHub never discovers the workflow.**
  Confirm the file is committed under .github/workflows with a .yml or .yaml extension and Actions is enabled.
- **The YAML is rejected before any runner starts.**
  Use the Actions error annotation and workflow syntax reference; check indentation, key placement, and expression delimiters.
- **A job starts but cannot see repository files.**
  Add or inspect actions/checkout and confirm the subsequent working directory.
- **A later job begins before tests finish.**
  Jobs are parallel by default. Add needs only where a real data or safety dependency exists.

### Where to check

- **Actions workflow list** — discovery, syntax errors, disabled status, and run history.
- **Run summary and visualization graph** — job parallelism, dependencies, skips, and cancellations.
- **Expanded step log** — exact action version, shell command, exit code, and first causal error.
- **Workflow permissions** — effective `GITHUB_TOKEN` access for the job.
- **Pull-request checks** — the stable job name reviewers and branch protection actually consume.

### Worked example: a test job that ran without any source code

1. A learner creates a job with `runs-on` and `run: npm test` but no checkout step.
2. The runner starts in an empty workspace; npm reports that `package.json` is missing.
3. The failure is not an npm or test problem. Hosted runners do not automatically clone the repository.
4. The learner adds `actions/checkout@v6` as the first step and reruns the same commit.
5. Installation and tests now operate on the recorded revision, and the check becomes meaningful.

**Quiz.** Which GitHub Actions unit gets one runner and executes its steps sequentially?

- [ ] The repository
- [x] A job
- [ ] An event filter
- [ ] A pull-request review

*A job selects a runner with runs-on and performs its steps in order. Separate jobs are parallel by default unless needs connects them.*

- **Where must workflow files live?** — In .github/workflows with a .yml or .yaml extension.
- **on** — Declares the repository events and filters that may create workflow runs.
- **Job versus step** — A job owns a runner; its steps run in order on that runner.
- **uses versus run** — uses invokes a reusable action; run executes a shell command.
- **How are jobs ordered?** — They run in parallel by default; needs declares dependencies.

### Challenge

Review one existing workflow without running it. Draw event → jobs → runners → steps → checks, mark
every external action version and token permission, then compare your prediction with the visualization
graph of a real run.

### Ask the community

> Workflow [path] should create check [name] on [event], but [missing/failing/skipped]. The relevant YAML and first causal log line are [paste].

Include indentation and the event payload context; paraphrased YAML often removes the actual defect.

- [GitHub Docs — Actions quickstart](https://docs.github.com/en/actions/get-started/quickstart)
- [GitHub Docs — Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)

🎬 [GitHub Actions Tutorial — TechWorld with Nana](https://www.youtube.com/watch?v=R8_veQiYBjI) (32 min)

- A workflow is reviewed code under .github/workflows, not invisible provider configuration.
- Read its hierarchy as event, jobs, runners, ordered steps, and reported checks.
- Jobs are parallel unless needs creates an explicit dependency.
- Checkout is required before commands can use repository files on a fresh hosted runner.
- Pin reviewed action versions and grant the smallest practical token permissions.


## Related notes

- [[Notes/automation-in-cicd/github-actions/triggers|Triggers]]
- [[Notes/automation-in-cicd/github-actions/matrix-runs|Matrix runs]]
- [[Notes/automation-in-cicd/running-tests-in-ci/running-the-suite|Running the suite]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/github-actions/workflow-basics.mdx`_
