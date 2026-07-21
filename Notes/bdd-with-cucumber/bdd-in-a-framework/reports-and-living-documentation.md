---
title: "Reports & living documentation"
tags: ["bdd-with-cucumber", "bdd-in-a-framework", "track-d"]
updated: "2026-07-16"
---

# Reports & living documentation

*Cucumber's reports show pass/fail against the actual readable Gherkin text, and tools like Allure and Serenity turn each run into current, trustworthy documentation of system behavior - 'living' because it's regenerated from really-passing scenarios, not manually maintained.*

> Every team has met the spec document that lies: written carefully eighteen months ago, referenced
> confidently in meetings, and describing at least four behaviors the system no longer has. Nobody
> updated it because nobody HAD to - nothing breaks when a Word document goes stale. Cucumber's
> reports invert that: the documentation is regenerated from scenarios that actually executed against
> the real system, minutes ago, so it physically cannot describe behavior that stopped existing.

> **In real life**
>
> The great split-flap departure board at a Paris railway station never goes stale. It doesn't need a
> diligent employee to remember to update it - it's driven directly by the live schedule, regenerated
> continuously, and every traveller under it trusts it without asking a member of staff to confirm.
> Compare that to a printed timetable glued to a pillar: accurate the day it was posted, quietly
> wrong within weeks, and misleading precisely because it still LOOKS authoritative. A living
> documentation report is the departure board; a manually-written spec doc is the printed timetable.

**Reports & living documentation**: Cucumber reporting turns a test run into readable documentation of current system behavior. Built in, Cucumber can emit an HTML report and a machine-readable JSON (or newer 'message') output showing pass/fail per scenario and per step - crucially, displayed against the actual Gherkin text, so the report reads as the specification itself with green and red marks on it. Third-party tools consume that output to go further: the hosted Cucumber Reports service publishes shareable run reports, Allure adds history, trends, and attachments like screenshots, and Serenity BDD renders full narrative documentation organized by feature and capability. The result is called living documentation because it is regenerated from scenarios that really executed on every run - if the system's behavior changes, the report changes (or fails) with it, unlike a manually-written spec document that silently goes stale the moment someone forgets to update it.

## From test run to readable documentation

- **The built-in HTML report** — run Cucumber with the `html` plugin (or `--publish` for the hosted
  Cucumber Reports service) and you get a browsable page per run: every feature, every scenario,
  every step, green or red, in the same plain language the team agreed on in the scenario-writing
  conversation.
- **The JSON / message output** — the machine-readable twin (`json:target/cucumber.json`). Nobody
  reads it directly; it exists to feed report tools, dashboards, and CI plugins - it's the wire
  format of the whole reporting ecosystem.
- **Third-party renderers** — Allure turns the output into a dashboard with run history, failure
  trends, and per-step screenshots; Serenity BDD (which coined much of this space's vocabulary)
  renders narrative, requirement-organized documentation where each feature page shows its
  scenarios and their latest results.
- **Why "living" is the honest word** — the report's claims are exactly the scenarios that passed
  minutes ago against the real system. A behavior that regresses turns red on the next run; a
  behavior that was removed fails loudly. A hand-maintained document makes the same claims but
  enforces none of them.
- **The audience loop closes here** — the same stakeholder who helped write "Given a registered
  user..." in Chapter 1 can read this run's report and see, in their own words, what the system
  verifiably does today. That's the payoff of keeping Gherkin readable all along.

> **Tip**
>
> Attach a screenshot on failure (in an `@After` hook) so it lands inside the report next to the red
> step. A stakeholder-readable scenario plus a picture of what the browser actually showed turns most
> "can you reproduce this?" conversations into a single link - the report becomes the bug report.

> **Common mistake**
>
> Treating the report as a private QA artifact - generated in CI, glanced at by the automation
> engineer, shown to nobody else. That discards the entire second half of BDD's value: the report IS
> the stakeholder-readable statement of current behavior, and if product owners never see it, the
> team is maintaining living documentation that nobody reads, which is overhead without the payoff
> (the next two notes in this chapter take that trade-off seriously).

![Travellers with luggage standing beneath the large split-flap departure board inside Paris Gare du Nord station, its header reading DEPART, DEPARTURE and ABFAHRT in three languages, with rows of yellow destination lines and a small digital clock beneath](reports-and-living-documentation.jpg)
*Travellers reading the flap display at the Paris Nord Train Station — Wikimedia Commons, CC BY 4.0 (Nicolas Kovarik / EC - Audiovisual Service). [Source](https://commons.wikimedia.org/wiki/File:Travellers_reading_the_flap_display_at_the_Paris_Nord_Train_Station_-_2014.jpg)*
- **The split-flap board — regenerated from the live schedule, never hand-updated** — Its rows change because reality changed, not because someone remembered to edit them. A living-documentation report works the same way: every run rewrites it from scenarios that actually executed.
- **DEPART / DEPARTURE / ABFAHRT — one record, readable by every audience** — The same information, deliberately legible to travellers of three languages - the way a Cucumber report shows results against the plain Gherkin every role on the team can read.
- **The clock beneath the board — you always know how current the information is** — A report is stamped with its run time. Half of trusting documentation is knowing WHEN it was last true - the printed timetable on a pillar offers no such honesty.
- **Travellers reading it directly — no intermediary needed** — Nobody asks a staff member to interpret the board. A stakeholder reading a living-doc report needs no engineer to translate it - that's the whole point of keeping scenarios in plain language.

**How one test run becomes documentation nobody had to write**

1. **CI triggers the Cucumber run** — Every scenario executes against the real system - browser and all, per the previous note.
2. **Cucumber emits JSON/message output plus an HTML report** — Pass/fail per step, recorded against the actual Gherkin text of each scenario.
3. **A report tool (Allure / Serenity / Cucumber Reports) renders it** — History, trends, screenshots on failure - organized by feature, readable by anyone.
4. **A product owner opens the report link** — They read, in the same words they helped write: this is what the system verifiably did today.
5. **Tomorrow's run regenerates everything** — A regression turns red; removed behavior fails loudly. The document cannot silently go stale - that's what 'living' means.

Regenerating a document from what actually just executed - instead of trusting someone to keep a
static file updated - is really just: derive the claims from the run results, every time. Here's
that shape as a small, generic simulation.

*Run it - a hand-maintained doc goes stale while a generated report cannot (Python)*

```python
# The system's REAL current behavior (imagine this changed last sprint)
def run_scenarios():
    return [
        ("Guest checkout completes without an account", "PASS"),
        ("Password reset link expires after 24 hours", "PASS"),
        ("Orders over $50 ship free", "FAIL"),  # threshold changed to $75 last sprint!
    ]

# A manually-written spec doc, last edited months ago - nothing forces it to change
manual_spec = [
    "Guest checkout completes without an account",
    "Password reset link never expires",        # stale: changed two sprints ago
    "Orders over $50 ship free",                # stale: changed last sprint
]

print("MANUAL SPEC (looks authoritative, enforces nothing):")
for claim in manual_spec:
    print(f"  - {claim}")

print()
print("LIVING DOCUMENTATION (regenerated from this run):")
for scenario, result in run_scenarios():
    marker = "OK " if result == "PASS" else "RED"
    print(f"  [{marker}] {scenario}")
print()
print("The stale $50 claim can't hide here - the scenario went RED the run after behavior changed.")
```

Same regenerate-from-reality shape in Java.

*Run it - a hand-maintained doc goes stale while a generated report cannot (Java)*

```java
import java.util.*;

public class Main {
    record Result(String scenario, boolean passed) {}

    static List<Result> runScenarios() {
        return List.of(
            new Result("Guest checkout completes without an account", true),
            new Result("Password reset link expires after 24 hours", true),
            new Result("Orders over $50 ship free", false) // threshold changed to $75 last sprint!
        );
    }

    public static void main(String[] args) {
        List<String> manualSpec = List.of(
            "Guest checkout completes without an account",
            "Password reset link never expires",  // stale: changed two sprints ago
            "Orders over $50 ship free"           // stale: changed last sprint
        );

        System.out.println("MANUAL SPEC (looks authoritative, enforces nothing):");
        for (String claim : manualSpec) System.out.println("  - " + claim);

        System.out.println();
        System.out.println("LIVING DOCUMENTATION (regenerated from this run):");
        for (Result r : runScenarios()) {
            System.out.println("  [" + (r.passed() ? "OK " : "RED") + "] " + r.scenario());
        }
        System.out.println();
        System.out.println("The stale $50 claim can't hide here - the scenario went RED the run after behavior changed.");
    }
}
```

### Your first time: Your mission: generate a real Cucumber report and read it as documentation

- [ ] Take any runnable Cucumber project (an example repo or your own) and run it with reporting on — Add the html plugin (html:target/report.html) or run with --publish for a hosted Cucumber Reports link.
- [ ] Open the report and find one passing scenario — Notice it reads as the specification itself - the exact Gherkin, with green marks - not as a log of technical assertions.
- [ ] Deliberately break one step (change an expected value) and re-run — Watch the same readable sentence turn red - the document changed because the system's verified behavior changed.
- [ ] Show the report to someone who has never opened the codebase — Ask them what the system does. If they can answer from the report alone, you've seen living documentation work.

You've now generated documentation nobody wrote by hand - and watched it refuse to go stale.

- **The report is technically accurate but unreadable to stakeholders - full of implementation-heavy steps.**
  The reporting layer can only display what the Gherkin says: this is the 'test script wearing Gherkin clothing' problem from Chapter 1 surfacing downstream. Fix the scenario language, not the report tool.
- **The living documentation is full of red, and everyone has learned to ignore it.**
  A report with tolerated failures documents nothing - nobody can tell real regressions from known noise. Quarantine or fix flaky scenarios ruthlessly; a living doc's entire value is that red MEANS something.
- **The JSON output exists but the fancy Allure/Serenity report shows no runs or stale runs.**
  Check the plumbing between the layers: the output path Cucumber writes (json:target/...) versus the path the report tool reads, and whether CI archives the results directory before the workspace is cleaned.
- **Stakeholders were shown the report once, never opened it again.**
  Push, don't pull: link the latest report in the sprint review, in the release notes, wherever behavior questions actually get asked. If a behavior question in a meeting can be answered by opening the report live, do that - it teaches the habit better than any announcement.

### Where to check

- **The run's report artifact in CI** (the published Cucumber Report link, or the archived
  `target/` HTML) — the canonical answer to "what did the system verifiably do on this build?"
- **The report's run timestamp and git revision** — how current the "living" claim actually is;
  a report from last month's pipeline is a printed timetable again.
- **The plugin configuration** (`@CucumberOptions(plugin = ...)`, `cucumber.properties`, or CLI
  flags) — the single place that determines which outputs exist for tools to consume.
- **The failure trend view in Allure/Serenity** — whether red scenarios are fresh regressions or
  long-tolerated noise, which decides whether the documentation is still trustworthy.

### Worked example: the meeting where the report replaced the spec document

1. A product owner asks in a release-planning meeting: "If a customer's saved card expires, do we
   retry the payment or cancel the order? The spec wiki says we retry twice."
2. Two developers give two different answers from memory. The spec wiki page was last edited
   fourteen months ago - before the payments rework.
3. A tester opens the latest Cucumber report from that morning's CI run and searches the payments
   feature: "Scenario: An expired saved card cancels the renewal after one failed retry" - green,
   executed four hours ago.
4. The answer is settled in ninety seconds, from a document nobody wrote by hand, in language the
   product owner reads directly - one retry, then cancel, verified against the real system today.
5. The team's quiet follow-up: the wiki page gets a banner linking to the living report, and the
   next "what does the system do?" question skips the archaeology entirely.

**Quiz.** A team keeps a beautifully-written behavior wiki AND a Cucumber suite with HTML reports. The wiki says bulk discounts apply at 10 units; the latest green report shows a passing scenario 'Bulk discount applies from 12 units.' Which source should the team trust about current behavior, and why?

- [ ] The wiki - prose written deliberately by a human is more authoritative than test output
- [x] The report - its claim was executed against the real system on the last run, so it cannot silently drift from actual behavior; the wiki's claim is enforced by nothing and has evidently gone stale
- [ ] Neither - documentation and reports are equally unreliable, so someone should read the source code
- [ ] The wiki, provided it was written by the product owner rather than an engineer

*The passing scenario executed against the real system - if bulk discounts didn't actually start at 12 units, that scenario would have failed, which is precisely the enforcement a manually-maintained wiki lacks; the disagreement itself is evidence the wiki went stale. Options one and four both appeal to authorship as authority, but WHO wrote a claim doesn't keep it true over time - regeneration from real runs does. Option three ignores that reading source code is exactly the expensive, non-stakeholder-readable path this reporting layer exists to replace, and a green, recently-executed scenario already IS verified evidence.*

- **What do Cucumber's built-in reports show, and in what language?** — Pass/fail per scenario and per step, displayed against the actual Gherkin text - the report reads as the specification with green and red marks on it.
- **What is the JSON/message output for?** — It's the machine-readable twin of the HTML report - the wire format that feeds Allure, Serenity, CI dashboards, and the hosted Cucumber Reports service.
- **What do Allure and Serenity add on top of Cucumber's own output?** — History and failure trends, attachments like failure screenshots, and (Serenity especially) narrative documentation organized by feature and requirement.
- **Why is it called LIVING documentation?** — Because it's regenerated from scenarios that really executed on every run - changed or removed behavior turns red immediately, so the document cannot silently go stale like a hand-maintained spec.
- **The departure-board analogy for living documentation** — A split-flap board driven by the live schedule stays current without anyone remembering to update it; a printed timetable on a pillar looks authoritative while quietly going wrong - the difference between a generated report and a manual spec doc.

### Challenge

Find one piece of manually-maintained behavior documentation in your world - a wiki page, a README
section, a spec doc. Pick three specific claims it makes and check each against the actual current
system (run it, test it, or ask). Score the document: how many of the three survived? Then write
two sentences: which of those claims would have been caught by a living-documentation report the
day it went stale, and what the stale version could have cost someone who trusted it.

### Ask the community

> My team generates Cucumber reports in CI but stakeholders never look at them. Here's how we currently share results: `[describe it]` - what actually got non-engineers reading your living documentation?

Concrete distribution tactics (where the link lives, what meeting it's opened in) transfer between
teams much better than "make stakeholders care" - ask for the mechanics, not the philosophy.

- [Cucumber — official reporting documentation](https://cucumber.io/docs/cucumber/reporting/)
- [Allure Report — Cucumber-JVM integration docs](https://allurereport.org/docs/cucumberjvm/)

🎬 [#9 - Generate Different Reports in Cucumber BDD || New Cucumber Web Report(Latest) — Naveen AutomationLabs](https://www.youtube.com/watch?v=3Sy-9m7KgZs) (21 min)

- Cucumber's reports display pass/fail against the actual Gherkin text - the report reads as the specification itself, with green and red marks on it.
- The JSON/message output is the machine-readable twin that feeds the reporting ecosystem: Allure, Serenity BDD, CI dashboards, and the hosted Cucumber Reports service.
- Documentation is 'living' when it's regenerated from scenarios that really executed every run - it cannot silently go stale, unlike a hand-maintained spec doc.
- A report full of tolerated red documents nothing - the living-doc value depends on red meaning a real, fresh regression.
- The payoff only lands if non-engineers actually read the report - readable scenario language upstream, and deliberate distribution of the report link downstream, are both required.


## Related notes

- [[Notes/bdd-with-cucumber/bdd-in-a-framework/cucumber-and-selenium|Cucumber + Selenium]]
- [[Notes/bdd-with-cucumber/bdd-in-a-framework/when-bdd-helps|When BDD helps]]
- [[Notes/bdd-with-cucumber/bdd-in-a-framework/when-it-hurts|When it hurts]]


---
_Source: `packages/curriculum/content/notes/bdd-with-cucumber/bdd-in-a-framework/reports-and-living-documentation.mdx`_
