---
title: "Command & template injection"
tags: ["security-testing-web", "injection-and-client-side", "track-c"]
updated: "2026-07-20"
---

# Command & template injection

*Command injection reaches a real OS shell through metacharacters like a semicolon or backtick; server-side template injection reaches a template engine's own expression syntax instead. Different interpreters, different root causes, different fixes.*

> An admin panel has a "network diagnostics" tool: type a hostname, it pings it and shows the result. Type
> a report name into a completely different, unrelated feature, and it renders a PDF with that name on the
> cover. Two harmless-looking text fields - and two entirely different ways they can go wrong. One reaches
> the operating system's own shell underneath the app. The other reaches a template-rendering engine that
> never touches a shell at all. Same symptom on the surface (your input did something it should not have),
> two different interpreters, two different fixes - and confusing the two leads straight to a
> recommendation that fixes nothing.

> **In real life**
>
> Picture an old telephone exchange. Sit at the switchboard and speak a connection request, and the
> operator patches your literal words straight into the real, physical phone network sitting behind the
> panel - whatever you say is trusted as a routing instruction, reaching the actual underlying system. That
> is OS command injection: input reaching a real shell on the real server, exactly as spoken, no separate
> validation in between. Now walk to the telegram counter next door, where a clerk fills your dictated
> message into the blanks of a preprinted form and a printing press later renders that filled-in form. The
> press never touches the phone exchange at all - but if your dictated words happen to contain the press's
> own formatting codes instead of plain text, the press executes those codes the moment it renders the
> template. That is server-side template injection: a completely different machine (the template engine,
> not the operating system), with a completely different root cause - unescaped input reaching template
> syntax, not a shell.

**Command injection and server-side template injection (SSTI)**: Command and template injection are two different mechanisms that both begin the same way - unescaped input reaching a place that interprets syntax as instructions rather than as inert data - but they reach two entirely different interpreters. OS command injection happens when user input reaches a shell or command-line invocation (a ping utility, a file-conversion helper, an image-processing pipeline that shells out) and shell metacharacters in that input - semicolons, pipes, ampersands, backticks, dollar-parenthesis command substitution - are interpreted by the operating system's shell rather than passed as one literal argument. The root cause is unsanitized input reaching the OS itself, and the fix is avoiding shell invocation entirely (calling the underlying library or API directly, or passing arguments as an array with no shell interpretation), plus strict allowlisting for any value that genuinely must reach a command. Server-side template injection (SSTI) happens when user input reaches a template-rendering engine (a report generator, an email-templating system, a page-templating framework) and that input contains the engine's own expression syntax, which the engine then evaluates as code during rendering instead of treating as literal text. The root cause is unescaped input reaching the template engine's own execution path - a completely different component from the operating system - and the fix is never concatenating raw user input into a template's own text; pass it in only as bound template data/context, never as parsed template markup. Confirming either is done with a benign, uniquely-identifiable, non-destructive probe, and only on systems the tester owns or is explicitly, in writing, authorized to test - this platform's own BuggyShop/BuggyAPI sandbox or a named local target - using tester-owned accounts and synthetic data, never a real third-party site.

## Distinguishing the two, by hand

- **Find the candidates for each, separately.** Command injection candidates are features that plausibly
  shell out: network diagnostics (ping, traceroute, DNS lookup), file/image conversion, archive
  extraction. SSTI candidates are features that plausibly render a template: report or document
  generation, email previews, custom page or notification templates.
- **Probe command injection with a harmless, observable marker.** Append a shell metacharacter (a
  semicolon, a pipe) followed by a benign, uniquely-named marker command, in a sandbox only, and check
  whether the marker's distinct output appears alongside the expected result - evidence the shell ran a
  second instruction, not just accepted a value.
- **Probe SSTI with pure arithmetic, never a real payload.** Enter the target engine's expression syntax
  around simple math - the classic minimal probe multiplies two small numbers - and check whether the
  rendered output shows the computed result instead of the literal characters you typed. A computed
  result proves the engine evaluated your input as code.
- **Match the fix to the interpreter that actually evaluated the input.** Command injection is fixed by
  avoiding the shell (or strict allowlisting); SSTI is fixed by keeping input out of parsed template text
  entirely. Recommending shell-metacharacter escaping for an SSTI finding, or template-syntax stripping
  for a command-injection finding, fixes neither.
- **Never use a real destructive command or a real code-execution SSTI payload.** A benign marker or an
  arithmetic probe is sufficient proof. Reading files, spawning shells, or modifying the sandbox beyond
  the test itself is out of scope for a minimal proof of concept.

> **Tip**
>
> The safest, most portable SSTI probe is pure arithmetic wrapped in the target engine's expression
> delimiters - it proves code evaluation with zero side effects. If the rendered output shows the computed
> number instead of your literal characters, the engine evaluated your input as an expression; if it shows
> your literal characters unchanged, it did not. This single check, run once per suspected template field,
> usually settles the question without needing anything more elaborate.

> **Common mistake**
>
> Treating command injection and template injection as the same bug with the same fix. A tester confirms a
> report-naming field evaluates a simple arithmetic expression, proving SSTI, and writes up the finding
> recommending "sanitize shell metacharacters like semicolons and pipes" - but the report generator never
> invokes a shell at all; the vulnerable component is the template engine's own expression evaluator, which
> does not care about semicolons. The correct fix is keeping user input out of the template's parsed text
> entirely (passed in only as bound data), not stripping shell syntax that was never the problem. Match the
> recommended fix to the interpreter the evidence actually points to.

![A telephone exchange operator seated at a large control panel with round analog meters and rows of patch-cord jack fields, viewed from the side](command-and-template-injection.jpg)
*Wisconsin Bell Telephone Company Switchboard - Gary Langebartels/FortepanIowa, Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Wisconsin_Bell_Telephone_Company_Switchboard.jpg)*
- **A spoken instruction, patched through directly** — Whatever the operator's hand does at this panel connects straight into the real exchange behind it. OS command injection is the same directness: input reaching a real shell, executed exactly as given, with nothing validating it in between.
- **The meter reads the real system, not the request** — The gauge reflects actual electrical state of the exchange - the true underlying system - regardless of what was said into the handset. A tester confirms command injection the same way: by observing a real side effect at the system level, not by trusting the app's own displayed response.
- **Every connection, the identical jack field** — Every call is patched through the same physical jack field no matter its content. A template engine works the same way: one rendering path handles every value - and if that path evaluates code-like syntax in the value, that is template injection, a property of the rendering path itself, not of any one field.
- **Two systems, one relay interface** — The operator's panel talks to the phone exchange; a separate apparatus - the telegram counter's printing press - renders text elsewhere entirely. Command injection and template injection are exactly this: two distinct systems that happen to sit behind what looks like one simple 'just relay my input' feature.

**Telling command injection from SSTI - press Play**

1. **Identify which interpreter the field plausibly reaches** — A diagnostics/conversion feature likely shells out (command injection risk). A report/email/template feature likely renders a template (SSTI risk).
2. **Probe the shell candidate with a benign, observable marker** — A shell metacharacter plus a uniquely-named marker, in a sandbox only. A distinct side effect in the output is evidence the OS shell ran a second instruction.
3. **Probe the template candidate with pure arithmetic** — The engine's expression syntax around simple math. A computed result instead of literal characters proves the engine evaluated your input as code.
4. **Recommend the fix that matches the interpreter** — Avoid shell invocation (or allowlist) for command injection. Keep input out of parsed template text for SSTI. Never swap the two fixes.

Here is the same distinction in runnable form - a static detector that flags shell metacharacters
separately from template-engine syntax in a handful of sample field values, plus an allowlist validator
showing the actual fix for the command-injection candidates.

*Run it - a command/template injection marker detector (Python)*

```python
# A command-injection vs template-injection marker detector, plus an
# allowlist validator. Static string analysis only - no subprocess call, no
# template engine invoked, nothing executed. Illustrative inputs are fake,
# local strings; this never touches a real shell or a real server.

# Characters/sequences a shell would treat as control syntax if a raw string
# reached an OS command (os command injection reaches the OPERATING SYSTEM).
SHELL_METACHARS = [";", "|", "&", "$(", "\`", "&&", "||", "\\n"]

# Sequences a template engine would treat as executable expression syntax if
# a raw string reached template rendering (SSTI reaches the TEMPLATE ENGINE,
# a completely different component with a completely different root cause).
TEMPLATE_MARKERS = ["{{", "}}", "\${", "<%", "%>"]

SAMPLES = [
    ("ping-target-field", "8.8.8.8"),
    ("ping-target-field-attempted", "8.8.8.8; whoami"),
    ("report-name-field", "Q3 Summary"),
    ("report-name-field-attempted", "{{7*7}}"),
    ("filename-field-attempted", "report.pdf\`id\`"),
]

def classify(value):
    hits_shell = [m for m in SHELL_METACHARS if m in value]
    hits_template = [m for m in TEMPLATE_MARKERS if m in value]
    if hits_shell and hits_template:
        return "both", hits_shell, hits_template
    if hits_shell:
        return "command-injection-risk", hits_shell, []
    if hits_template:
        return "template-injection-risk", [], hits_template
    return "clean", [], []

# An allowlist validator - the actual fix for command injection: never build
# a shell string from input at all, restrict to a known-safe shape instead.
import re
SAFE_HOSTNAME_OR_IP = re.compile(r"^[A-Za-z0-9.\\-]{1,253}$")

def allowlist_validate(value):
    return bool(SAFE_HOSTNAME_OR_IP.match(value))

def run():
    print("Static marker scan (detection signal, not a substitute for allowlisting):")
    for name, value in SAMPLES:
        verdict, shell_hits, template_hits = classify(value)
        print("  [" + name + "] " + repr(value) + " -> " + verdict.upper())
        if shell_hits:
            print("           shell metacharacters found: " + str(shell_hits) + " (risk: reaches the OS if passed to a command)")
        if template_hits:
            print("           template syntax found: " + str(template_hits) + " (risk: reaches the template engine if rendered)")
    print()

    print("Allowlist validation of the same ping-target values (the actual fix):")
    for name, value in SAMPLES[:2]:
        ok = allowlist_validate(value)
        print("  [" + name + "] " + repr(value) + " -> " + ("ACCEPT" if ok else "REJECT - does not match hostname/IP shape"))

run()
```

The identical detector and validator in Java - same samples, same verdicts:

*Run it - a command/template injection marker detector (Java)*

```java
import java.util.*;
import java.util.regex.Pattern;

public class Main {
    // A command-injection vs template-injection marker detector, plus an
    // allowlist validator. Static string analysis only - nothing executed,
    // no shell, no template engine invoked. Illustrative inputs are fake,
    // local strings; this never touches a real shell or a real server.

    static final String[] SHELL_METACHARS = {";", "|", "&", "$(", "\`", "&&", "||", "\\n"};
    static final String[] TEMPLATE_MARKERS = {"{{", "}}", "\${", "<%", "%>"};

    static final String[][] SAMPLES = {
        {"ping-target-field", "8.8.8.8"},
        {"ping-target-field-attempted", "8.8.8.8; whoami"},
        {"report-name-field", "Q3 Summary"},
        {"report-name-field-attempted", "{{7*7}}"},
        {"filename-field-attempted", "report.pdf\`id\`"},
    };

    static final Pattern SAFE_HOSTNAME_OR_IP = Pattern.compile("^[A-Za-z0-9.\\\\-]{1,253}$");

    static class Verdict {
        String label;
        List<String> shellHits, templateHits;
        Verdict(String l, List<String> s, List<String> t) { label = l; shellHits = s; templateHits = t; }
    }

    static Verdict classify(String value) {
        List<String> shellHits = new ArrayList<>();
        for (String m : SHELL_METACHARS) if (value.contains(m)) shellHits.add(m);
        List<String> templateHits = new ArrayList<>();
        for (String m : TEMPLATE_MARKERS) if (value.contains(m)) templateHits.add(m);

        if (!shellHits.isEmpty() && !templateHits.isEmpty()) return new Verdict("both", shellHits, templateHits);
        if (!shellHits.isEmpty()) return new Verdict("command-injection-risk", shellHits, Collections.emptyList());
        if (!templateHits.isEmpty()) return new Verdict("template-injection-risk", Collections.emptyList(), templateHits);
        return new Verdict("clean", Collections.emptyList(), Collections.emptyList());
    }

    static boolean allowlistValidate(String value) {
        return SAFE_HOSTNAME_OR_IP.matcher(value).matches();
    }

    public static void main(String[] args) {
        System.out.println("Static marker scan (detection signal, not a substitute for allowlisting):");
        for (String[] sample : SAMPLES) {
            String name = sample[0], value = sample[1];
            Verdict v = classify(value);
            System.out.println("  [" + name + "] '" + value + "' -> " + v.label.toUpperCase());
            if (!v.shellHits.isEmpty())
                System.out.println("           shell metacharacters found: " + v.shellHits + " (risk: reaches the OS if passed to a command)");
            if (!v.templateHits.isEmpty())
                System.out.println("           template syntax found: " + v.templateHits + " (risk: reaches the template engine if rendered)");
        }
        System.out.println();

        System.out.println("Allowlist validation of the same ping-target values (the actual fix):");
        for (int i = 0; i < 2; i++) {
            String name = SAMPLES[i][0], value = SAMPLES[i][1];
            boolean ok = allowlistValidate(value);
            System.out.println("  [" + name + "] '" + value + "' -> " + (ok ? "ACCEPT" : "REJECT - does not match hostname/IP shape"));
        }
    }
}
```

### Your first time: Your mission: probe one field of each kind, in an authorized sandbox

- [ ] Get written authorization and use a tester-owned account — This platform's own BuggyShop/BuggyAPI sandbox or a named local target, with a test account you own and fake data only.
- [ ] Find one diagnostics/conversion field and one report/template field — The first is a command-injection candidate; the second is an SSTI candidate. Note the normal expected response for each first.
- [ ] Probe each with the matching minimal, non-destructive test — A shell metacharacter plus a benign marker for the first; the engine's expression syntax around simple arithmetic for the second.
- [ ] Write the finding naming the correct interpreter and fix — Command injection names the shell as the reached component; SSTI names the template engine. Recommend the matching fix, never the other one's.

You can now tell, from evidence rather than a guess, whether a field reaches an operating system shell or
a template engine - and recommend the fix that actually addresses the component the evidence points to.

- **A shell-metacharacter probe on a diagnostics field produces no visible difference at all.**
  The field may not shell out, may already allowlist input, or the marker may need to be more distinctive. Try a different benign marker and check for output timing or side effects, not just visible text - but never escalate to a real destructive command to force a result.
- **An arithmetic SSTI probe renders as literal text instead of a computed number.**
  That is evidence against SSTI on that specific field and syntax - it does not clear the whole feature. Try the delimiter syntax the actual engine in use expects; different templating engines use different expression syntax, and a probe shaped for the wrong one will always look negative.
- **A finding recommends 'escape shell metacharacters' for a confirmed SSTI bug.**
  That fix does not address the actual interpreter - the template engine never invokes a shell. Rewrite the recommendation to keep user input out of the template's parsed text entirely, passing it only as bound data.
- **You suspect command or template injection while browsing a real, live, third-party site.**
  Stop probing immediately. You do not have authorization to test that system. Do not send a confirming second request. Report only through an explicit responsible-disclosure channel if one exists, never by continuing to test without written permission.

### Where to check

- **The exact probe and exact observed side effect, saved verbatim** - a marker string and where its
  effect appeared, or the arithmetic input and the rendered output, not a paraphrase.
- **Which component actually evaluated the input** - a shell (command injection) or a template engine
  (SSTI) - before writing a fix recommendation; the two require genuinely different remediation.
- **Every field that plausibly reaches either interpreter, not just the first one that responds** - a
  single confirmed field does not clear a diagnostics tool's other parameters or a template's other
  variables.
- **[[security-testing-web/injection-and-client-side/sql-injection-by-hand]]** - the sibling injection
  category where the reached interpreter is a database query engine; same data-versus-instruction
  mechanism, a third distinct interpreter.
- **[[security-testing-web/owasp-top-10-properly/mapping-findings-to-the-list]]** - for how both of these
  map to A03:2021 Injection, and how to report their severity separately from that category.

### Worked example: confirming SSTI, not command injection, on a report-naming field

1. A tester, authorized to test the platform's own BuggyAPI sandbox with a tester-owned account, notices
   an invoice-export feature lets the user supply a custom report name that appears on the generated PDF.
2. They first try a shell-metacharacter probe (a semicolon plus a benign marker) on the field, in case it
   shells out to a PDF tool - no distinct side effect appears in the output at all.
3. They then try a minimal arithmetic probe using the templating engine's expression delimiters. The
   generated PDF shows the computed number instead of the literal characters typed - proof the report
   name is being rendered as template code, not displayed as literal text.
4. The finding is written up as server-side template injection, naming the template engine (not a shell)
   as the reached component, with the fix recommended as passing the report name in only as bound
   template data, never concatenated into the template's own parsed text.

**Quiz.** A tester confirms that a report-naming field evaluates a simple arithmetic expression written in a templating engine's syntax. What is the correct fix to recommend?

- [ ] Strip shell metacharacters like semicolons and pipes from the field
- [x] Keep user input out of the template's parsed text entirely, passing it only as bound template data
- [ ] Block the specific arithmetic expression that was used as the proof-of-concept probe
- [ ] No fix is needed, since arithmetic evaluation causes no real harm

*The evidence points to the template engine, not a shell - so the fix must address how input reaches the template's parsed text, not shell metacharacters (option A), which were never the reached interpreter. Blocking one specific probe string (option C) does not address the underlying mechanism, and dismissing the finding (option D) ignores that the same evaluation path can run far more than arithmetic once an engine executes attacker-influenced expressions.*

- **OS command injection** — User input reaches a real shell invocation, and shell metacharacters in it are interpreted as instructions by the operating system rather than passed as one literal argument.
- **Server-side template injection (SSTI)** — User input reaches a template-rendering engine and contains that engine's own expression syntax, which gets evaluated as code during rendering instead of shown as literal text.
- **Why they need different fixes** — Command injection is fixed by avoiding shell invocation (or strict allowlisting); SSTI is fixed by keeping input out of parsed template text. Swapping the two fixes addresses the wrong interpreter.
- **The minimal SSTI probe** — Simple arithmetic wrapped in the target engine's expression delimiters. A computed result instead of literal characters proves code evaluation, with zero side effects.
- **The minimal command-injection probe** — A shell metacharacter plus a benign, uniquely-named marker, in a sandbox only - a distinct side effect in the output proves the shell ran a second instruction.
- **The actual command-injection fix** — Avoid shell invocation entirely (call the underlying library/API directly, or pass arguments as an array with no shell interpretation), plus allowlisting any value that must reach a command.
- **A common mistake** — Recommending shell-metacharacter escaping for a confirmed SSTI finding, or template-syntax stripping for a confirmed command-injection finding - fixing neither because the fix targets the wrong interpreter.

### Challenge

In this platform's own BuggyAPI or BuggyShop sandbox, using a tester-owned account, find one candidate
field for each mechanism (a diagnostics/conversion feature and a report/template feature) - or construct
plausible ones if the sandbox does not currently expose both. For each, run the matching minimal,
non-destructive probe, write the exact input and exact observed evidence, name the interpreter it
actually reached, and recommend the fix that matches that interpreter. Deliberately write one incorrect
fix recommendation (the command-injection fix applied to the SSTI finding, or vice versa) and explain in
one sentence why it would not actually work.

### Ask the community

> I've started keeping command injection and template injection separate in my own head by asking which interpreter actually evaluated the input - a real OS shell, or a template engine - before I ever write a fix recommendation, and I confirm each with the smallest possible non-destructive probe (a benign marker for the shell, plain arithmetic for the template). For people who test these regularly: what field types have surprised you by shelling out or rendering a template when it was not obvious from the feature's name, and how do you keep an SSTI proof-of-concept minimal once you have confirmed evaluation?

Hearing which field types turned out to secretly shell out or secretly render a template - when nothing
in the feature's name suggested it - and how other testers keep an SSTI proof-of-concept to the smallest
possible non-destructive step once evaluation is confirmed, would sharpen exactly the judgment call this
note is trying to teach.

- [OWASP - Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- [PortSwigger Web Security Academy - Server-side template injection](https://portswigger.net/web-security/server-side-template-injection)

🎬 [PortSwigger Web Security Academy - What is command injection?](https://www.youtube.com/watch?v=8PDDjCW5XWw) (8 min)

- Command injection reaches a real OS shell; server-side template injection reaches a template engine's own expression evaluator - two different interpreters, two different root causes.
- Probe command injection with a shell metacharacter plus a benign, observable marker; probe SSTI with pure arithmetic in the engine's expression syntax - both minimal and non-destructive.
- A computed arithmetic result instead of literal characters proves template code evaluation; a distinct side effect from a marker proves shell execution.
- Match the fix to the interpreter the evidence points to: avoid shell invocation (or allowlist) for command injection, keep input out of parsed template text for SSTI - never swap the two.
- Never use a real destructive command or a real code-execution payload; a benign marker or arithmetic probe is sufficient proof.
- Test only systems you own or are explicitly, in writing, authorized to test, with tester-owned accounts and synthetic data.


## Related notes

- [[Notes/security-testing-web/injection-and-client-side/sql-injection-by-hand|SQL injection by hand]]
- [[Notes/security-testing-web/injection-and-client-side/xss-reflected-stored-dom|XSS: reflected / stored / DOM]]
- [[Notes/security-testing-web/owasp-top-10-properly/mapping-findings-to-the-list|Mapping findings to the list]]


---
_Source: `packages/curriculum/content/notes/security-testing-web/injection-and-client-side/command-and-template-injection.mdx`_
