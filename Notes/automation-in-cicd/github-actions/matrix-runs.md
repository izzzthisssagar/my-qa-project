---
title: "Matrix runs"
tags: ["github-actions", "matrix", "cross-browser", "track-d"]
updated: "2026-07-17"
---

# Matrix runs

*A GitHub Actions matrix expands one job definition into explicit environment combinations, making compatibility coverage visible while include, exclude, fail-fast, and parallel limits control cost.*

> Copy-pasting the same test job for three operating systems and four runtime versions creates twelve
> places to drift. A matrix makes the combinations data and keeps the job procedure singular — but it
> also makes twelve runners, so every axis must represent a compatibility question worth paying for.

> **In real life**
>
> A multiplication table turns two input axes into a grid of results. A job matrix does the same: every
> operating system crosses every runtime version unless you deliberately include or exclude cells.
> Adding one innocent-looking axis can multiply the bill.

**job matrix**: A GitHub Actions job matrix is a strategy that declares one or more variables whose values expand a single job into multiple job combinations. Each generated job reads values through the matrix context. include can add values or special combinations; exclude removes unwanted combinations; fail-fast controls whether one failure cancels siblings; and max-parallel limits how many generated jobs run simultaneously.

## Make coverage a table, not duplicated YAML

```yaml
strategy:
  fail-fast: false
  max-parallel: 4
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [22, 24]

runs-on: ${{ matrix.os }}
steps:
  - uses: actions/checkout@v6
  - uses: actions/setup-node@v6
    with:
      node-version: ${{ matrix.node }}
  - run: npm ci
  - run: npm test
```

This is four jobs, not one job that loops. Each gets an isolated runner, log, status, and cost.

> **Tip**
>
> Start from supported production combinations. Put exotic or expensive combinations in a scheduled
> workflow rather than multiplying every pull-request run.

> **Common mistake**
>
> Adding axes for browser, OS, runtime, database, and locale all at once. A 3 × 3 × 3 × 2 × 4 grid is
> 216 jobs before a single test has run.

![A multiplication table written as many equations across a rough outdoor surface](matrix-runs.jpg)
*Multiplication table — Denis Mihailov, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Multiplication_table_(4643804213).jpg)*
- **First axis** — Operating systems or browser engines form one set of values.
- **Second axis** — Runtime versions cross the first set to create combinations.
- **Expanded cell** — Each combination becomes an independently visible job and runner.
- **Multiplication cost** — Every new axis multiplies combinations; count them before committing.

**How a matrix becomes jobs**

1. **Declare axes** — Choose compatibility dimensions and supported values.
2. **Cartesian expansion** — GitHub creates every default combination.
3. **Apply exclude** — Unsupported or redundant cells are removed.
4. **Apply include** — Special cells or per-cell metadata are added.
5. **Schedule runners** — max-parallel limits simultaneous generated jobs.
6. **Collect statuses** — Each cell reports separately; fail-fast may cancel siblings.

*Run it — expand and exclude a matrix (Python)*

```python
``oses = ["ubuntu", "windows"]
versions = [22, 24]
excluded = {("windows", 22)}
jobs = [(os, version) for os in oses for version in versions if (os, version) not in excluded]
for os, version in jobs:
    print(f"{os} / node-{version}")
print("job count:", len(jobs))``
```

*Run it — expand and exclude a matrix (Java)*

```java
``import java.util.*;

public class Main {
    public static void main(String[] args) {
        var oses = List.of("ubuntu", "windows");
        var versions = List.of(22, 24);
        var jobs = new ArrayList<String>();
        for (String os : oses) for (int version : versions)
            if (!(os.equals("windows") && version == 22))
                jobs.add(os + " / node-" + version);
        jobs.forEach(System.out::println);
        System.out.println("job count: " + jobs.size());
    }
}``
```

### Your first time: Your mission: prove two compatibility dimensions

- [ ] Choose two supported values on one axis — For example the current and previous runtime, or two browser engines.
- [ ] Reference the matrix value in runner or setup — Print it in the log so the job identity is undeniable.
- [ ] Introduce one combination-specific failure — Confirm its cell is red while the other remains independently visible.
- [ ] Set fail-fast intentionally — Use false for full compatibility evidence; use true only when sibling results add no value.

The matrix is useful when each cell answers a named support question.

- **All generated jobs use the same version.**
  Check that setup inputs reference matrix.variable rather than a hard-coded value.
- **One failure cancels combinations you wanted to inspect.**
  Set strategy.fail-fast to false for diagnostic compatibility runs.
- **The matrix creates far more jobs than expected.**
  Multiply axis lengths, then inspect include entries. Remove axes that do not protect supported behavior.
- **A special include cell lacks expected values.**
  Remember include can add or augment combinations; inspect the generated job list and pass explicit metadata.

### Where to check

- **Visualization graph and generated job names** — actual expansion and cancelled cells.
- **Printed matrix context** — values each job received.
- **include/exclude blocks** — special combinations and omissions.
- **fail-fast and max-parallel** — cancellation and concurrency behavior.
- **Billing/runtime metrics** — whether coverage value justifies multiplied runner time.

### Worked example: the accidental 36-job pull request

1. A team adds three OS values, three Node versions, and four browsers: 3 × 3 × 4 = 36 jobs.
2. Most browser/OS pairs duplicate engine behavior; pull requests slow dramatically.
3. They keep two Node versions on Linux for every pull request and three OS smoke jobs on main.
4. A scheduled workflow runs the broader compatibility matrix nightly.
5. Coverage now matches decisions: fast merge feedback plus periodic breadth.

**Quiz.** A matrix has 3 OS values, 2 runtimes, and 4 browsers with no exclusions. How many jobs are generated?

- [ ] 9
- [ ] 12
- [x] 24
- [ ] 48

*Matrix axes form a Cartesian product: 3 × 2 × 4 = 24 independently generated jobs.*

- **Matrix expansion** — The Cartesian product of declared axis values, adjusted by include and exclude.
- **fail-fast false** — Keeps sibling combinations running after one cell fails, producing full compatibility evidence.
- **max-parallel** — Caps how many matrix jobs execute simultaneously without removing combinations.
- **include** — Adds special combinations or augments matching combinations with extra values.
- **Matrix design test** — Every cell should answer a supported compatibility question worth its runner time.

### Challenge

Calculate the current job count and runner-minutes for one matrix. Redesign it into pull-request,
post-merge, and scheduled layers while preserving every explicitly supported compatibility claim.

### Ask the community

> Our matrix axes are [values], producing [count] jobs and [minutes]. We support [environments], and failures differ by [evidence]. Which combinations are redundant?

State the support promise before optimizing; otherwise job reduction is only guesswork.

- [GitHub Docs — Run job variations](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [Playwright — Sharding tests](https://playwright.dev/docs/test-sharding)

🎬 [GitHub Actions Matrix Strategy: Run Jobs Faster & Smarter — Techi Nik](https://www.youtube.com/watch?v=FSQDtRMtSHo) (7 min)

- A matrix turns compatibility values into independently visible jobs from one definition.
- Job count is the product of axes, so calculate cost before adding dimensions.
- Use include and exclude to express real support combinations, not arbitrary grids.
- Choose fail-fast based on whether sibling results remain diagnostically valuable.
- Keep pull-request coverage focused and move expensive breadth to post-merge or scheduled runs.


## Related notes

- [[Notes/automation-in-cicd/github-actions/workflow-basics|Workflow basics]]
- [[Notes/automation-in-cicd/github-actions/caching|Caching]]
- [[Notes/playwright/parallel-and-cross-browser/projects-and-browsers|Projects & browsers]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/github-actions/matrix-runs.mdx`_
