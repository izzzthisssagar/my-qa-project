---
title: ".gitlab-ci.yml"
tags: ["gitlab-ci", "yaml", "pipeline-as-code", "track-d"]
updated: "2026-07-17"
---

# .gitlab-ci.yml

*The repository-root .gitlab-ci.yml defines pipeline creation, defaults, jobs, rules, variables, artifacts, caches, and includes; the merged configuration—not one visible file—is what GitLab executes.*

> A valid YAML file can still describe the wrong pipeline. GitLab merges includes, defaults, hidden
> templates, extensions, variables, workflow rules, and job rules before scheduling anything. Debugging
> only the 30 lines in the root file can mean debugging a recipe GitLab never actually cooked.

> **In real life**
>
> A recipe names ingredients, order, conditions, and outputs. Reusable templates are useful recipe
> cards, but substitutions and included pages change the final dish. The only honest review examines
> the fully assembled recipe and the exact ingredients available to that run.

**.gitlab-ci.yml**: The .gitlab-ci.yml file is the default repository-root configuration for GitLab CI/CD. It can declare workflow rules, stages, default settings, variables, jobs, job rules, images, services, caches, artifacts, and included configuration. GitLab fetches and merges includes before applying the root file; hashes can deep-merge while arrays such as script and rules are replaced rather than appended. The compiled or merged configuration is the execution truth.

## Build from global decision to job detail

```yaml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

default:
  image: node:24
  before_script:
    - npm ci

stages: [test]

unit_tests:
  stage: test
  script:
    - npm test
  artifacts:
    when: always
    reports:
      junit: reports/junit.xml
```

`workflow:rules` controls whether a pipeline exists at all. Job `rules` then decide whether a job
exists inside it. Sensitive variables belong in protected/masked CI settings or external secrets,
not committed YAML.

> **Tip**
>
> Use the Pipeline Editor or CI Lint and inspect the merged configuration before merging include or
> extends changes. Syntax validity alone does not reveal overridden arrays or unexpected defaults.

> **Common mistake**
>
> Defining a new `script` in a job and expecting it to append to an included template. Arrays do not
> deep-merge; the job's array replaces the inherited one, possibly deleting install or security steps.

![An illustrated vintage recipe-book page showing many labelled puddings, tarts, and pastries](gitlab-ci-yml.jpg)
*The Everyday Cook and Recipe Book illustration — Internet Archive, public domain. [Source](https://commons.wikimedia.org/wiki/File:The_everyday_cook_and_recipe_book_-_containing_more_than_two_thousand_practical_recipes_for_cooking_every_kind_of_meat,_fish,_poultry,_game,_soups,_broths,_vegetables_and_salads_-_also_for_making_all_(14801749053).jpg)*
- **workflow rules** — The top-level recipe first decides whether a pipeline exists.
- **defaults and variables** — Shared ingredients apply broadly unless jobs override them.
- **jobs and scripts** — Each named result comes from its own commands, rules, and environment.
- **merged includes** — External recipe pages and templates change the final configuration GitLab executes.

**How GitLab compiles CI configuration**

1. **Root file loaded** — GitLab reads .gitlab-ci.yml from the selected revision.
2. **Includes fetched** — Local, project, template, or remote configuration is resolved.
3. **Configuration merged** — Hashes deep-merge; later scalar/array values override earlier ones.
4. **workflow evaluated** — Rules decide whether to create the pipeline.
5. **Jobs expanded** — Defaults, extends, variables, and job rules form runnable jobs.
6. **Graph validated** — Stages, needs, tags, artifacts, and scripts become the scheduled pipeline.

*Run it — see map merge versus list replacement (Python)*

```python
``template = {"variables": {"A": "1", "B": "2"}, "script": ["install", "test"]}
job = {"variables": {"B": "3"}, "script": ["test --fast"]}
merged = {
    "variables": {**template["variables"], **job["variables"]},
    "script": job["script"],
}
print("variables:", merged["variables"])
print("script:", merged["script"])``
```

*Run it — see map merge versus list replacement (Java)*

```java
``import java.util.*;

public class Main {
    public static void main(String[] args) {
        var variables = new LinkedHashMap<String, String>();
        variables.put("A", "1"); variables.put("B", "2");
        variables.put("B", "3");
        var script = List.of("test --fast");
        System.out.println("variables: " + variables);
        System.out.println("script: " + script);
    }
}``
```

### Your first time: Your mission: inspect the configuration GitLab actually runs

- [ ] Create one merge-request-only pipeline — Use workflow rules, one job, an explicit image, and a truthful test command.
- [ ] Validate with CI Lint/Pipeline Editor — Fix syntax and semantic errors before pushing repeated experiments.
- [ ] Extract one hidden template — Use a dot-prefixed job and extends, then inspect the merged result.
- [ ] Override one hash and one array intentionally — Confirm the hash merges while the array replaces inherited content.

You understand reuse only after predicting the compiled configuration correctly.

- **No pipeline is created.**
  Inspect workflow rules first; job rules cannot run inside a pipeline that was never created.
- **A job lost inherited commands.**
  Inspect merged YAML. script and rules arrays are replaced, not item-by-item merged.
- **The YAML parses but a variable has the wrong value.**
  Quote values and inspect precedence across project/group variables, defaults, job values, and includes.
- **An include changed without a repository diff.**
  Pin project/template refs or use integrity controls where available; mutable remote includes are supply-chain inputs.

### Where to check

- **CI Lint/Pipeline Editor** — syntax, schema, and simulated pipeline creation.
- **Merged/compiled configuration** — final includes, extends, defaults, and overrides.
- **Pipeline source and variables** — rule inputs and precedence.
- **Job details** — image, tags, script, services, artifacts, and effective environment.
- **Include ref/version** — the external configuration revision actually consumed.

### Worked example: the security scan deleted by a harmless override

1. A shared template defines `script: [install-scanner, run-scan]`.
2. A project extends it and adds `script: [run-project-tests]`, expecting an append.
3. Arrays replace, so the scan commands disappear from the merged job.
4. The reviewer inspects merged YAML, spots the loss, and refactors template work into reusable commands/jobs.
5. The pipeline now runs both checks with explicit ownership rather than accidental merge semantics.

**Quiz.** When a job overrides an inherited script array, what happens?

- [ ] Commands automatically append
- [ ] GitLab randomly chooses commands
- [x] The new array replaces the inherited script array
- [ ] The pipeline always fails syntax validation

*GitLab deep-merges mapping values, but arrays are not merged item-by-item. The later script array replaces the earlier one.*

- **workflow:rules** — Controls whether the pipeline is created before job rules are evaluated.
- **Job rules** — Controls whether and how one job appears inside an existing pipeline.
- **Hidden job** — A dot-prefixed non-runnable configuration template commonly reused with extends.
- **Merged configuration** — The fully resolved includes/defaults/extends result that GitLab executes.
- **GitLab merge rule** — Mappings deep-merge; conflicting scalars and arrays use the later value.

### Challenge

Choose the most included pipeline in your group. Compile it, annotate every inherited job, default,
variable, rule, and array override, then pin one mutable dependency and remove one surprising behavior.

### Ask the community

> Our root .gitlab-ci.yml includes [sources/refs]. The merged job [name] has [unexpected value]; root/template values are [paste], and CI Lint reports [result].

Share the compiled fragment, not secrets or only the root file.

- [GitLab Docs — CI/CD YAML syntax reference](https://docs.gitlab.com/ci/yaml/)
- [GitLab Docs — Use configuration from other files](https://docs.gitlab.com/ci/yaml/includes/)

🎬 [GitLab CI/CD Pipeline Tutorial for Beginners — Valentin Despa](https://www.youtube.com/watch?v=z7nLsJvEyMY) (20 min)

- .gitlab-ci.yml is pipeline code, but the merged configuration is execution truth.
- workflow rules decide pipeline creation; job rules decide job inclusion.
- Validate syntax and inspect compiled includes/defaults/extends before merging.
- Mappings can deep-merge while arrays such as script and rules replace inherited arrays.
- Keep secrets out of YAML and pin/govern external configuration inputs.


## Related notes

- [[Notes/automation-in-cicd/gitlab-ci-and-quality-gates/stages-jobs-and-runners|Stages, jobs & runners]]
- [[Notes/automation-in-cicd/gitlab-ci-and-quality-gates/quality-gates-coverage-and-sonar|Quality gates (coverage, Sonar)]]
- [[Notes/automation-in-cicd/github-actions/workflow-basics|Workflow basics]]


---
_Source: `packages/curriculum/content/notes/automation-in-cicd/gitlab-ci-and-quality-gates/gitlab-ci-yml.mdx`_
