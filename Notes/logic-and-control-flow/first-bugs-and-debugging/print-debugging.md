---
title: "Print debugging"
tags: ["logic-and-control-flow", "java", "python", "debugging", "track-b"]
updated: "2026-07-11"
---

# Print debugging

*Printing a value mid-run is the oldest debugging trick and still the most-used, at every level. The skill isn't typing print — it's knowing WHAT to print (label, value, type), WHERE, and how to halve the search each time so you corner the bug in a few prints, not forty.*

> There's a myth that "real" programmers use fancy debuggers and only beginners sprinkle `print`
> statements. It's nonsense. Open the terminal of nearly any senior engineer chasing a bug and
> you'll find it full of `print("HERE 1")`, `print("x =", x)`, `console.log(">>>>", data)`. Adding
> a print to see what a program is *actually* doing — versus what you *assume* it's doing — is the
> fastest way to close the gap between those two, and that gap is where every bug lives. The trick
> is not the `print`. It's knowing what to put inside it and where to place it.

> **In real life**
>
> A print statement is a footprint in snow. When you find one, you know something *walked exactly
> here* — and the tread pattern even tells you *what*. That's precisely what a print does: it
> proves your program reached this exact line, and shows the value it carried at that instant. And
> the untouched snow matters just as much: **no footprint means nothing walked there.** When you
> add a print and it never appears in the output, that's the discovery — the line you were sure
> ran, didn't. Half of all print-debugging bugs are found not by a print that shows a wrong value,
> but by a print that never prints at all.

## The three questions a good print answers

A bare `print(x)` is a weak footprint. A *good* debug print answers three questions at once, so
you never have to guess which print produced which line:

**1. WHERE am I?** A label. `print("after the loop:", ...)` — so when six prints fire, you can
tell them apart. `print(x)` alone gives you `7` and no idea which of your prints said it.

**2. WHAT is the value?** The variable, printed with its *raw* form. In Python use `repr()` /
`!r` so a string shows its quotes and a trailing space becomes visible. The pretty value hides
bugs; the raw value reveals them.

**3. WHAT TYPE is it?** When a value surprises you, print `type(x)` too. Half of dynamic-language
bugs are a value that's secretly the wrong type — a `"3"` where you expected a `3` — and the
type is the only thing that exposes it.

Put together: `print(f"[loop] item={item!r} type={type(item).__name__} total={total}")`. That one
line tells you where, what, and what-kind — and that's a footprint you can actually follow.

![A single crisp boot print pressed into fresh snow, surrounded by untouched snow](footprint-in-snow.jpg)
*Footprint in snow — Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Footprints_in_the_snow,_Munich_2021_01.jpg)*
- **The whole print = 'execution reached HERE'** — A footprint is proof something passed this exact spot. A `print` is identical: if the line runs, its output appears, and now you KNOW the program got to that point. This is the most basic and most powerful use — not to see a value, but to confirm a line executed at all. 'Did this code even run?' is answered instantly by whether the print shows up.
- **The tread pattern = the VALUE you captured** — The detail in the print — the specific ridges — is like the value you logged: `x = 7`, `item = 'banana'`. A footprint without tread tells you someone passed; a footprint WITH tread tells you who. `print('here')` is treadless; `print('here: x =', repr(x))` records exactly what the program was carrying at that step.
- **The untouched snow = code that NEVER RAN** — This is the insight beginners miss. The blank snow around the print is every path nothing walked. When you add a print and it never appears, that blank snow is your bug: the line you were certain executed, didn't — a condition was false, a loop ran zero times, a function returned early. A MISSING footprint is often louder than a present one.
- **Crisp edges = an exact, in-the-moment record** — The print captures the value at the precise instant it ran — not before, not after. That timing is everything: a variable can be right on line 10 and wrong on line 40, and only a print placed at the right spot catches the moment it changed. Move the footprint and you sample a different point in the program's walk.
- **One clear print beats ten vague ones** — A single, well-labelled footprint tells you more than a scramble of `print(1)`, `print(2)`, `print(3)`. Resist spraying prints everywhere; place a few good ones with labels and values, read them, then move them. Debugging is aiming, not carpet-bombing — and a tidy trail is one you can actually read.

**Bisection: corner the bug in a few prints, not forty. Press Play**

1. **You know the START is right and the END is wrong** — The input is fine; the output is wrong. Somewhere between line 1 and line 100, a correct value became a wrong one. Adding a print on every line would work but is slow. There's a far faster way — the same idea as guessing a number between 1 and 100.
2. **Print ONCE, in the MIDDLE** — Put a single print at roughly the halfway point. Is the value still correct there, or already wrong? One print, one yes/no answer — and that answer just eliminated HALF the code. The bug is either before the midpoint or after it.
3. **Jump to the middle of the half that's wrong** — Say the midpoint value was already wrong — the bug is in the first half. Print at the middle of THAT half. Right or wrong? Another half gone. You're doing binary search on your own code, and each print throws away 50% of the suspects.
4. **Repeat — each print halves what's left** — 100 lines becomes 50, then 25, then 12, then 6, then 3, then 1. Around SEVEN prints, placed by halving, pin the exact line where the value goes bad — versus dozens of prints placed by guessing. This is the single biggest efficiency multiplier in print-debugging.
5. **The last print sits right on the bug** — When 'correct just before' meets 'wrong just after' on adjacent lines, the line between them is your bug. You didn't read the whole program; you asked six or seven well-placed yes/no questions and let each one delete half the haystack.

Here's print-debugging catching a real bug. This Python function adds up prices, but a string
snuck into the list — the debug print shows each item's value **and type**, so you can see the
culprit the instant before it crashes:

*Run it — a labelled debug print exposes the bad value*

```python
def total_price(items):
    total = 0
    for item in items:
        # the debug print: WHERE (loop), WHAT (item, raw), TYPE, and running total
        print(f"  [debug] item={item!r}  type={type(item).__name__}  total_before={total}")
        total += item
    return total

prices = [10, 5, "3", 2]        # oops -- a string "3" snuck in among the ints
print("adding up prices...")
print("total:", total_price(prices))
```

Read the debug lines: `item=10 type=int`, `item=5 type=int`, then `item='3' type=str` — and
right there, before the crash, you can SEE that `'3'` is a string, not a number. The `TypeError`
that follows just confirms what the print already told you. Now the same technique in Java —
where the compiler stops that exact string bug, so print-debugging instead hunts a *logic*
slip (watch the running total reveal it):

*Run it — labelled prints trace the running state in Java*

```java
public class Main {
    static int highestEven(int[] numbers) {
        int best = 0;
        for (int n : numbers) {
            boolean isEven = n % 2 == 0;
            // the debug print: which n, is it even, and the best-so-far
            System.out.println("  [debug] n=" + n + "  isEven=" + isEven + "  best_so_far=" + best);
            if (isEven && n > best) {
                best = n;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        int[] data = {3, 8, 5, 12, 7, 6};
        System.out.println("finding the highest even number...");
        System.out.println("highest even: " + highestEven(data));   // should be 12
    }
}
```

The Java debug line lets you watch `best` climb — 0, then 8, then 12 — and confirm each `n` was
tested for evenness. If the answer were ever wrong, you'd see *exactly* which step misbehaved,
without guessing. Same footprints, same idea; the only difference is Java's compiler already
swept up the type bug that bit Python.

bisection

> **Tip**
>
> Make your debug prints **findable and removable**. Prefix them with a distinctive marker you'd
> never ship — `print("XXXX total =", total)` or `>>>>`. Then before you commit, search the file
> for `XXXX` / `>>>>` and delete every one in seconds. This solves the two problems with
> print-debugging at once: during the hunt you can spot your own prints in a busy log, and
> afterwards you can guarantee none leaked into the codebase. A committed `print("XXXX")` is a
> small embarrassment; a systematic marker makes it impossible.

### Your first time: Your mission: follow the footprints to a bug

- [ ] Watch the values stream by — Run the Python playground. Each loop pass prints the item, its type, and the running total. You're seeing the program's actual state at each step — not what you assume, what IS.
- [ ] Spot the culprit before the crash — Find the line 'item='3' type=str'. There's your bug, called out by the print BEFORE the TypeError even fires. The print diagnosed it; the error just confirmed it.
- [ ] Add a footprint of your own — In the Java playground, add a print right after 'best = n;' saying 'NEW BEST:' + best. Run it — now you see the exact moments best changed (at 8, then 12), a tighter trail than before.
- [ ] Find a missing footprint — In Python, change the list to all odd numbers and add a print INSIDE an 'if item % 2 == 0' block. Run it — the print never appears. That blank output is the discovery: the block never ran.
- [ ] Try bisection — Imagine a 20-step calculation gone wrong. Instead of printing all 20, print once at step 10. Right or wrong there? You just deleted 10 steps with one print. That's the whole efficiency trick.

You've now used prints to see a value, expose a type, prove a line ran — and prove one didn't. That's the entire technique.

- **My debug print never appears in the output.**
  That's a finding, not a failure — the line didn't run. The condition around it was false, the loop ran zero times, or the function returned before reaching it. A missing footprint tells you the code path you assumed executed, didn't. Move the print earlier to find where execution actually stopped or branched away.
- **The value prints as expected but the program still behaves wrong.**
  Print in a DIFFERENT spot — the value is right where you looked but goes wrong elsewhere. Use bisection: if it's correct at the midpoint, the bug is after it. Also print the RAW value (`repr()` / `!r`) — a string that looks like `42` on screen might be `'42 '` with a trailing space, right the whole time to your eye and wrong to the code.
- **There are so many print lines I can't find mine.**
  Two fixes. Prefix every debug print with a unique marker (`XXXX`, `>>>>`) so you can eyeball or grep just yours. And print FEWER, better prints — a handful with clear labels beats fifty bare ones. If the real logs are drowning you, that's the moment to switch from print to a logging library with levels you can filter.
- **My prints show up in the wrong order, or after a crash.**
  Output buffering. Prints can sit in a buffer and flush late — so a print right before a crash may never appear, making you think the line didn't run. Force it out: Python `print(..., flush=True)`, Java `System.out.flush()`. Also, stdout and stderr can interleave oddly; if order matters, send debug prints to the same stream consistently.
- **I fixed the bug but forgot to remove my prints, and they shipped.**
  This is why the marker habit matters — grep `XXXX` before every commit and delete. Long term, prefer a logging library: `logger.debug(...)` can be left in place and switched OFF in production by config, giving you the trail when you need it and silence when you don't. Print is scratch paper; logging is the permanent, switchable record.

### Where to check

Print-debugging is a discipline, not a reflex. Aim before you fire:

- **Print WHERE, WHAT, and TYPE** — a label, the raw value (`repr`/`!r`), and `type(x)` when a value surprises you. Bare `print(x)` wastes the technique.
- **Bisect, don't carpet-bomb** — one print at the midpoint deletes half the code. Seven aimed prints beat forty scattered ones.
- **Watch for the MISSING print** — a footprint that never appears means the line never ran. That's often the whole bug.
- **Mark your prints** — a unique prefix (`XXXX`) so you can find them in a busy log and delete them all before committing.
- **Flush before a crash** — `flush=True` / `System.out.flush()` so a print right before the failure actually reaches the screen.

Tester's habit: **when you can't reproduce a bug, add prints and ask the user to run it.** A
labelled print that reports the actual value on the machine where the bug happens turns "works
on mine" into "here's the exact value that's different on theirs." Print-debugging isn't only
for your own code — it's a remote-diagnosis tool.

### Worked example: the print that wasn't there

1. **The report:** "Premium users aren't getting their discount. Regular users are billed fine. We've checked the discount math ten times and it's correct."
2. **The developer keeps re-reading the discount CALCULATION** — the multiply, the rounding, the total. All correct. Hours pass. The math was never the problem, so staring at it reveals nothing.
3. **A tester adds one print INSIDE the discount block:** `print("XXXX applying discount, rate =", rate)` — right where the discount is actually applied.
4. **They run it for a premium user. The print never appears.** Blank. The discount code isn't producing a wrong number — it's *not running at all*. The footprint that should be there, isn't.
5. **So they move the print UP**, to just before the `if user.is_premium:` that guards the block, printing `user.is_premium`. It shows `False` — for a user who is definitely premium.
6. **There's the bug, and it's nowhere near the math.** `is_premium` is being read from a field that's set later than this code runs — a timing/ordering bug. The discount block is skipped because the flag isn't `True` yet. Ten re-reads of the calculation could never have found it, because the calculation was innocent.
7. **The fix is about ORDER, not arithmetic** — set `is_premium` before the discount step runs. A one-line move, found by a print that *refused to appear*.
8. **The lesson for a tester.** The most valuable print is often the one that stays silent. A present footprint shows a wrong value; a missing footprint proves a line never executed — and 'the code you're all staring at never even ran' is a bug that re-reading the code cannot find, only running it can. When something 'should work', put a print inside it and confirm it runs at all before you trust a single line of it.

> **Common mistake**
>
> Printing without a label: `print(x)`, `print(total)`, `print(data)`. In a loop or a busy
> program you get a column of bare values — `7`, `12`, `banana`, `0` — and no idea which print
> produced which, or which iteration you're looking at. You end up adding *more* prints just to
> tell your prints apart. Spend the extra three seconds: `print("total after loop:", total)`. The
> label is what turns a pile of numbers into a readable trail, and it costs nothing but a few
> keystrokes you'll save tenfold in confusion.

**Quiz.** You add a debug print inside a function to check a value, run the program, and the print never appears in the output at all. What does that most likely mean?

- [ ] Printing is broken or the value is invalid
- [x] The line never executed — the function wasn't called, a condition around it was false, or the code returned before reaching it. A print that doesn't appear is proof that path didn't run, which is frequently the bug itself: the code you assumed ran, didn't.
- [ ] You need to add flush=True and it will definitely appear
- [ ] The value is None, so print produced nothing

*This is the most underused insight in all of print-debugging: a MISSING print is a discovery, not a dud. When your footprint never shows up, execution never reached that line — the function wasn't called, an `if` guarding it was false, a loop ran zero times, or an early `return`/exception jumped past it. Beginners assume 'the print didn't work' and move on; pros realise 'the CODE didn't run' and follow that thread, which often lands right on the bug (see the premium-discount example — the whole block was silently skipped). The move: when a print doesn't appear, walk it backwards up the code until it DOES, and the last silent spot is where execution branched away from what you expected. (Buffering can occasionally hide a final print before a crash — flush to rule that out — but 'the line didn't run' is the far more common and more useful answer.)*

- **What does a MISSING print tell you?** — The line never ran — condition false, loop ran zero times, early return, or the function wasn't called. A silent footprint is often the whole bug.
- **What is bisection?** — Binary-search your code: print ONCE at the midpoint. Correct there → bug is after; wrong there → bug is before. Each print halves the search — ~7 prints pin a bug in 100 lines.
- **Why label every debug print?** — So you can tell six prints apart. `print(x)` gives a bare `7` with no context; `print('total after loop:', x)` tells you what and where in one line.
- **How do you keep debug prints from shipping?** — Prefix with a unique marker (XXXX, >>>>), grep and delete before committing. Long term, use a logging library with levels you can switch off in production.
- **A value prints correctly but the program is still wrong — now what?** — Print somewhere else (bisect), and print the RAW value (repr) — the bug is at a different spot, or the 'correct-looking' value has a hidden trailing space / wrong type.
- **print vs logging** — print = scratch paper, delete after the hunt. logging = permanent, level-based (debug/info/warning), left in and switched off in production. Graduate from one to the other.

### Challenge

In the Python playground, remove the string `"3"` so the list is all ints and run it — the crash
vanishes and you see a clean trail ending in `total: 20`. Now add a print AFTER the loop, before
the `return`, saying `[debug] final total = ` and the value, and confirm it matches. Then delete
the `"3"` fix and instead wrap `total += item` so it converts with `int(item)` — watch the trail
continue past where it used to crash. Write one sentence: describe a bug you would find faster by
a print that NEVER appears than by any print that shows a value.

### Ask the community

> Print-debugging stuck: I expected `[X]` but a debug print shows `[Y]` (or shows NOTHING). The print I added: `[paste the print line]`. Where I placed it: `[which function/line]`. Language: `[Java/Python]`. Did the print appear at all? `[yes/no]`. Raw value via repr/!r: `[paste]`.

Whether the print APPEARED at all is the first thing to say — a missing print (line never ran)
and a present-but-wrong print (bad value) are completely different bugs. State that, paste the
print line and the raw value, and the diagnosis usually follows immediately.

- [Real Python — print-debugging done well (and when to stop)](https://realpython.com/python-debugging-print/)
- [Python docs — logging: the grown-up successor to print](https://docs.python.org/3/library/logging.html)
- [git bisect — bisection applied to finding the guilty commit](https://git-scm.com/docs/git-bisect)
- [A guide to debugging — the discipline behind the prints](https://blog.regehr.org/archives/199)

🎬 [Debugging with print statements, the right way](https://www.youtube.com/watch?v=Ioyb2iJyBI0) (10 min)

- Print-debugging is the most-used technique at every level — the skill is what to print (label + raw value + type), not typing print itself.
- A MISSING print is a discovery: the line never ran. That silent footprint is frequently the whole bug — the code you assumed executed, didn't.
- Bisect instead of carpet-bombing: one print at the midpoint deletes half the code. Around seven aimed prints pin a bug in 100 lines.
- Mark debug prints with a unique prefix (XXXX) so you can find and delete them all before committing — or graduate to a logging library you can switch off.
- For a tester: a labelled print run on the machine where a bug reproduces turns 'works on mine' into the exact value that differs on theirs — remote diagnosis in one line.


---
_Source: `packages/curriculum/content/notes/logic-and-control-flow/first-bugs-and-debugging/print-debugging.mdx`_
