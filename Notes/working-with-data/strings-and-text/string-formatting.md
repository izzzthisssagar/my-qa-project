---
title: "String formatting"
tags: ["working-with-data", "strings", "track-b"]
updated: "2026-07-11"
---

# String formatting

*Build readable messages by dropping values into a template: Python f-strings and Java String.format/printf. Placeholders, format specs for decimals, thousands, percent and padding — and why f-strings beat messy + concatenation.*

> Almost every program has to build text out of values: "Hello, Sam! You have 5 messages," "Total: $19.50,"
> "Loaded 1,204 rows in 3.2s." You *could* glue it together with `+` — `"Hello, " + name + "! You have " +
> str(count) + " messages"` — but that's a fiddly, error-prone mess of quotes, plus signs, and `str()` calls,
> and it's where a stray missing space or a forgotten conversion sneaks in. **String formatting** is the clean
> way: write the sentence once as a template with *slots*, and drop the values into the slots. Python's
> f-strings make this beautifully readable; Java's `String.format` and `printf` do the same with `%`
> placeholders. You also get precise control over how numbers look — two decimals for money, commas for
> thousands, a percent sign, padded columns. It's a small skill with an outsized payoff in readable output and
> professional-looking results.

> **In real life**
>
> String formatting is **a 'HELLO my name is ___' badge.** The badge is printed once with fixed words and a
> blank; each person just fills the blank with their name. A template string works the same way: the fixed
> text stays put, and the *placeholder* — the blank — gets filled with a value when the string is built. An
> **f-string**: A Python string prefixed with f whose {curly braces} are placeholders filled with the value inside them, e.g. f'Hi {name}'. The modern, readable way to build text with values. Java's equivalent is String.format/printf with % placeholders.
> is that badge: `f"Hello, {name}!"` keeps 'Hello, ' and '!' fixed, and drops whatever `name` holds into the
> `{name}` slot. You can even control how neatly the value is written in the blank — two decimals, a comma
> every three digits, padded to a fixed width — which is the difference between `19.5` and a tidy `$19.50`.

## f-strings (Python) and String.format (Java)

**Python** — prefix the string with `f` and put values in `{curly braces}`:
```python
name = "Sam"
count = 5
print(f"Hello, {name}! You have {count} messages.")   # Hello, Sam! You have 5 messages.
print(f"Next year: {count + 1} messages.")            # expressions work inside {}
```

**Java** — `String.format` (or `printf`) with `%` placeholders, values listed after:
```java
String name = "Sam";
int count = 5;
System.out.println(String.format("Hello, %s! You have %d messages.", name, count));
// %s = string, %d = whole number, %f = decimal. Order matters: values fill left to right.
```

The f-string reads like the finished sentence with the variables sitting right where they belong — no
`str()` conversions, no `+` juggling, no counting spaces. Java's `%s`/`%d`/`%f` placeholders are matched to
the arguments after the string, in order. Both beat concatenation for anything longer than a word or two: the
template stays legible, and you can see the output's shape at a glance.

![A classic red HELLO my name is name badge with the printed words at the top and a large blank white area below](name-badge.png)
*Graphic: a 'HELLO my name is' badge — Wikimedia Commons, public domain. [Source](https://commons.wikimedia.org/wiki/File:Hello_my_name_is_sticker.svg)*
- **Fixed and filled stay cleanly separate** — The badge keeps the printed words and the written name visually apart — you read the sentence, then the value. f-strings do the same: the template stays a readable sentence with slots, unlike '+' concatenation where quotes, plusses, and str() calls tangle the text and the values together.

## Format specs: making numbers look right

The real power is controlling *how* a value appears. In an f-string, add a colon and a spec inside the
braces; in Java, put the spec in the `%` placeholder:

```python
price = 19.5
print(f"Total: ${price:.2f}")     # Total: $19.50   -- .2f = 2 decimal places
print(f"Rows: {1234567:,}")       # Rows: 1,234,567 -- , = thousands separator
print(f"Rate: {0.075:.1%}")       # Rate: 7.5%      -- .1% = percent, 1 decimal
print(f"[{'Sam':>8}]")            # [     Sam]      -- >8 = right-align, width 8
print(f"[{'Sam':<8}]")            # [Sam     ]      -- <8 = left-align, width 8
```

```java
double price = 19.5;
System.out.println(String.format("Total: $%.2f", price));  // $19.50
System.out.println(String.format("Rows: %,d", 1234567));   // 1,234,567
System.out.printf("[%8s]%n", "Sam");                        // right-align width 8
System.out.printf("[%-8s]%n", "Sam");                       // left-align (minus sign)
```

`:.2f` (Python) / `%.2f` (Java) is the one you'll use most — money and measurements almost always want a
fixed number of decimals so `19.5` prints as `19.50` and `19.333333` prints as `19.33`. The thousands
comma, the percent, and width/alignment (for lining up columns of output) round out the toolkit. This is
the same formatting idea from the earlier reading-and-formatting material, now in the string context.

**How a template string gets filled in. Press Play.**

1. **Python builds the final string** — At runtime the f-string evaluates each slot, applies its format, and stitches everything into one finished string: 'Total: $19.50'. It's just building a normal string — you can print it, store it, or pass it on like any other.

*Try it — f-strings and format specs in Python. Press Run.*

```python
name = "Sam"
count = 5
price = 19.5

# basic substitution -- values drop into the {slots}
print(f"Hello, {name}! You have {count} messages.")
print(f"Next year: {count + 1} messages.")     # expressions work inside {}

# format specs after a colon:
print(f"Total: \${price:.2f}")     # $19.50   -- two decimals
print(f"Rows: {1234567:,}")        # 1,234,567 -- thousands comma
print(f"Rate: {0.075:.1%}")        # 7.5%      -- percent, 1 decimal
print(f"[{name:>8}]")              # right-align in width 8
print(f"[{name:<8}]")              # left-align in width 8

# THE CLASSIC BUG: forget the f prefix -> braces print literally
print("Hello, {name}")             # Hello, {name}  <- NOT substituted!
```

Here's the **same in Java** — `String.format` and `printf`, with `%s` / `%d` / `%f` placeholders and specs
like `%.2f` and `%,d`:

*Try it — String.format and printf in Java. Press Run.*

```java
public class Main {
    public static void main(String[] args) {
        String name = "Sam";
        int count = 5;
        double price = 19.5;

        System.out.println(String.format("Hello, %s! You have %d messages.", name, count));
        System.out.println(String.format("Total: $%.2f", price));   // $19.50
        System.out.println(String.format("Rows: %,d", 1234567));    // 1,234,567

        // printf prints directly; %n is a newline, %8s pads to width 8
        System.out.printf("[%8s]%n", name);    // right-align
        System.out.printf("[%-8s]%n", name);   // left-align (minus)
    }
}
```

> **Tip**
>
> Default to f-strings (Python) or `String.format`/`printf` (Java) over `+` concatenation for any message with
> more than one value — the template stays readable and you skip the `str()` conversions and space-counting
> that concatenation demands. Learn `:.2f` first; it's the one you'll reach for constantly (money, rates,
> measurements all want fixed decimals). If placeholders print literally (`{name}` shows up in the output), you
> forgot the `f` prefix in Python; if Java throws a formatting error, your `%` type doesn't match the argument
> (`%d` needs a whole number, `%f` a decimal) or the argument count is off. And keep formatting for *display* —
> format a number into a string when you're showing it, but keep the real number for calculations.

### Your first time: First time? Fill in a template

Ten minutes and you can build clean, professional messages — readable templates instead of plus-sign spaghetti.

- **“Java throws IllegalFormatConversionException or a MissingFormatArgument error.”**
  Your % placeholder doesn't match its argument. %d needs a whole number (int/long), %f a decimal (double), %s a string — passing a double to %d, or the wrong count of arguments, throws. Count your placeholders and match each to an argument of the right type, in order. %s is the most forgiving (it stringifies anything), so use it when unsure.

### Where to check

Debugging string formatting:

- **Braces printing literally?** — missing `f` prefix in Python. Add `f"..."`. To show a real brace, double it (`{{`).
- **Java format exception?** — placeholder/argument mismatch: `%d` needs an int, `%f` a double, `%s` anything. Match type and count, in order.
- **Wrong number of decimals?** — use `:.2f` (Python) / `%.2f` (Java). Raw floats show all digits; the spec rounds for display.
- **Can't do math on a formatted value?** — formatting returns a STRING. Keep the number for calculations; format only when displaying.
- **Alignment/columns off?** — width/align specs like `{x:>8}` (right) / `{x:<8}` (left) pad to a fixed width; check the width and the direction.

### Worked example: the price that displayed as 19.5 instead of $19.50 — a formatting fix

A checkout shows prices, but they come out as `19.5`, `7`, `12.1` — inconsistent and unprofessional. Let's
format them properly:

```python
price = 19.5
print("Total: $" + str(price))     # Total: $19.5   -- looks unfinished
```

1. **The symptom:** money is showing as `19.5` (and `7` for whole amounts) instead of the expected
   `19.50` / `7.00`. It works, but looks wrong — and the concatenation with `str()` is clunky.
2. **The cause:** `str(price)` just gives the number's default text — `19.5`, with no trailing zero and no
   fixed decimals. Currency needs exactly two decimal places, which the default conversion doesn't enforce.
3. **The fix — format with two decimals in an f-string:**
   ```python
   price = 19.5
   print(f"Total: ${price:.2f}")   # Total: $19.50
   ```
   `:.2f` pads/rounds to exactly two decimal places, so `19.5` becomes `19.50` and `7` becomes `7.00`.
   The f-string also drops the `+`/`str()` clutter — the whole thing reads as the finished line.
4. **Add thousands separators for big totals:**
   ```python
   print(f"Total: ${1234.5:,.2f}")  # Total: $1,234.50   (comma + 2 decimals)
   ```
   You can combine specs — `,.2f` means 'thousands commas AND two decimals.'
5. **Keep the number for math:** crucially, format only for DISPLAY. `price` stays the number `19.5` for any
   calculation (tax, totals); you apply `:.2f` at the moment you print it. Formatting early would turn it
   into the string `'19.50'` and break later arithmetic.
6. **Tester's angle:** money display is a classic QA checklist item — testers verify prices always show two
   decimals, big numbers get separators, and rounding is correct (does 19.995 show as 19.99 or 20.00?). The
   give-away here was inconsistent decimal places across amounts, which points straight at missing/format
   specs. Consistent formatting is both a UX detail and a correctness one.

> **Common mistake**
>
> Building messages with `+` concatenation and default `str()` when a template would be cleaner and more
> correct. Concatenation forces you to juggle quotes, plus signs, spaces, and `str()` conversions — easy to
> drop a space or forget a conversion — and it can't control how a number looks, so money shows as `19.5`
> instead of `19.50`. f-strings (Python) and `String.format`/`printf` (Java) fix both: a readable template with
> slots, plus format specs (`:.2f`, `:,`, `:.1%`, width/align) for tidy output. The classic slips: forgetting
> the `f` prefix so `{name}` prints literally; mismatching Java's `%` type or argument count; and — importantly
> — formatting a number too early, turning it into a string and breaking later math. Keep the real number for
> calculations, format only when you display, and reach for a template over concatenation for anything longer
> than a word.

**Quiz.** In Python, what does print('Hello, {name}') output (note: no f prefix), and how do you fix it?

- [ ] It prints Hello, Sam — the braces are always substituted
- [x] It prints the literal 'Hello, {name}' because without the f prefix the braces are just characters; add f: print(f"Hello, {name}")
- [ ] It throws an error about an undefined placeholder
- [ ] It prints Hello, followed by a blank

*Without the f prefix, 'Hello, {name}' is an ordinary string, so the curly braces are literal characters and it prints exactly 'Hello, {name}' — no substitution happens. This is the most common f-string mistake: if placeholders show up verbatim in your output, you forgot the f. The fix is to add it: f'Hello, {name}', which tells Python to evaluate {name} and drop in its value. (It's not an error, and braces are never substituted without the f.) Bonus: to print a real curly brace inside an f-string, double it — f'{{literal}}' outputs {literal}.*

- **Why format over + concatenation** — A template stays readable (the whole sentence with slots) and skips str() conversions and space-counting. Concatenation tangles text and values with quotes and plusses, and can't control number appearance.
- **Java placeholders** — %s = string, %d = whole number, %f = decimal; values listed after the template, matched left to right. Mismatched type or count throws. %.2f / %,d apply specs. printf prints directly (%n = newline).

### Challenge

Fill the template. (1) Build `f"Hello, {name}! You have {count} messages."` with your own values. (2) Format a
price with `:.2f` so 12.5 shows as 12.50. (3) Combine specs: show 1234.5 as $1,234.50 with `:,.2f`. (4) Print
`"Hello, {name}"` WITHOUT the f and observe the literal braces, then add the f to fix it. (5) Write one
sentence: why prefer an f-string over `'Hello, ' + name + '!'`? If you can say 'the template stays readable and
I skip str() conversions and can format the values', you've got clean message-building down.

### Ask the community

> Formatting question: my [placeholders print literally / number has wrong decimals / Java format throws]. Here's the line [paste it] and its output. I'm using [Python/Java]. What's wrong?

If Python placeholders show as `{name}`, check for a missing f prefix. If a number shows too many/few decimals,
show your format spec (`:.2f` gives two). For Java format exceptions, paste the format string AND the arguments
so the %-type/argument mismatch is visible (`%d` needs an int, `%f` a double).

- [Python docs — formatted string literals (f-strings)](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals)
- [Java tutorial — formatting numbers (format/printf)](https://docs.oracle.com/javase/tutorial/java/data/numberformat.html)
- [Python f-Strings & string formatting — Dave Gray](https://www.youtube.com/watch?v=ktOOKv6XJ7U)

🎬 [f-strings & format specs — building readable messages — Dave Gray](https://www.youtube.com/watch?v=ktOOKv6XJ7U) (12 min)

- String formatting fills a template with values instead of gluing text with +. Python f-strings put values in {braces}: f"Hello, {name}!"; Java uses String.format/printf with %s/%d/%f placeholders. Both stay readable, unlike + concatenation.
- Format specs control how a value looks: :.2f (two decimals — the most-used, for money), :, (thousands comma), :.1% (percent), and width/alignment like {x:>8} for columns. Java uses %.2f, %,d, etc.
- The classic Python bug is forgetting the f prefix — then {name} prints literally. If placeholders show up verbatim, add the f. To print a real brace, double it ({{ }}).
- In Java, the % type must match the argument (%d whole number, %f decimal, %s anything) and the count must line up, or it throws — %s is the most forgiving.
- Formatting produces a STRING, not a number, so it's for DISPLAY only: keep the real numeric value for calculations and apply the format (:.2f) at the moment you show it, or later math breaks.


---
_Source: `packages/curriculum/content/notes/working-with-data/strings-and-text/string-formatting.mdx`_
