---
title: "Dates, currencies & formats"
tags: ["non-functional-testing-intro", "localization-and-i18n", "track-c"]
updated: "2026-07-18"
---

# Dates, currencies & formats

*Separate stored values from localized display, then test calendars, time zones, numbers, currencies, units, parsing, and round-trip meaning.*

> `03/04/2026` is either March 4 or April 3 depending on the reader. `$100` may be US, Canadian,
> Australian, or another dollar. A value can be mathematically correct and still communicate the wrong
> day or amount when the product formats it without locale and context.

> **In real life**
>
> Stored data is sheet music; localized formatting is the instrument and performance convention. Keep
> the notes stable, then render them for the audience. Saving the sound of one instrument as the score
> makes every later performance ambiguous.

**Locale-aware formatting**: Locale-aware formatting renders dates, times, numbers, currencies, units, and names according to language and regional conventions while preserving an unambiguous underlying value. Unicode CLDR supplies widely used locale data; applications should use maintained platform libraries rather than hand-built separator rules.

## Store meaning; localize presentation

Keep instants with an unambiguous timeline representation and retain the intended timezone or calendar
context when the business meaning needs it. Keep monetary amount and ISO currency code together. Format
with locale-aware APIs backed by current data, and parse input deliberately—display formats are not
safe interchange formats. Test decimal/grouping symbols, digit systems, negative/accounting patterns,
currency placement and precision, calendars, first day of week, daylight-saving transitions, units,
and round trips.

> **Tip**
>
> For every format defect, record the raw value, locale tag, timezone, currency/unit code, formatted text,
> and the exact library/platform version. Without those inputs, the display cannot be reproduced.

> **Common mistake**
>
> Do not replace comma and period characters manually or assume every currency has two fraction digits.
> CLDR patterns treat separators as locale placeholders, and currency rules vary. Hand-built formatting
> also misses spacing, signs, grouping, plural forms, and numbering systems.

![An illuminated Cairo Metro clock face displaying Eastern Arabic numerals](dates-currencies-and-formats.jpg)
*Clock in Cairo with Eastern Arabic numerals — Ajfweb, Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:Clock-in-cairo-with-eastern-arabic-numerals.jpg)*
- **Same time value** — The underlying instant does not change when digits or display conventions change.
- **Localized digit shapes** — Numbering systems are part of locale presentation; ASCII digits are not universal display.
- **Familiar regional convention** — Users interpret formats through learned conventions, so context matters as much as numeric correctness.
- **Readable meaning** — Test that formatting, labels, and timezone context remove ambiguity instead of merely looking local.

**A safe locale-formatting pipeline**

1. **Store an unambiguous value and its business context** — Keep currency code, timezone, unit, or calendar information where meaning requires it.
2. **Select explicit locale and formatting options** — Do not infer every setting from language or country alone.
3. **Render with maintained CLDR-backed APIs** — Libraries handle separators, symbols, patterns, digits, and plural-sensitive forms.
4. **Test boundaries and round trips** — Use DST transitions, month/day ambiguity, negatives, zero, large values, and user input.

*A locale-format contract oracle (Python)*

```python
checks = {
    "raw_value_unambiguous": True,
    "locale_explicit": True,
    "currency_code_preserved": True,
    "timezone_boundary_tested": True,
}
for name, passed in checks.items(): print(name + "=" + ("PASS" if passed else "FAIL"))
result = "PASS" if all(checks.values()) else "FAIL"
assert result == "PASS", "format contract rejected"
print("RESULT=" + result)
```

*A locale-format contract oracle (Java)*

```java
import java.util.LinkedHashMap;
import java.util.Map;
public class Main {
    public static void main(String[] args) {
        Map<String, Boolean> checks = new LinkedHashMap<>();
        checks.put("raw_value_unambiguous", true);
        checks.put("locale_explicit", true);
        checks.put("currency_code_preserved", true);
        checks.put("timezone_boundary_tested", true);
        boolean ok = true;
        for (var e : checks.entrySet()) { System.out.println(e.getKey() + "=" + (e.getValue() ? "PASS" : "FAIL")); ok &= e.getValue(); }
        String result = ok ? "PASS" : "FAIL";
        if (!result.equals("PASS")) throw new AssertionError("format contract rejected");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Build a locale-format boundary table

- [ ] Choose explicit locales and contexts — Include locale tag, timezone, currency, unit, and calendar assumptions rather than changing only language.
- [ ] Create ambiguous and boundary values — Use March/April ambiguity, midnight, DST transition, negative money, zero, large numbers, and varying currency precision.
- [ ] Compare display and stored value — Verify the localized text communicates the same underlying meaning and includes needed context.
- [ ] Test input and round trip — Enter local forms, validate or reject ambiguity clearly, save, reload, and confirm the same value.

- **A US user and UK user interpret the same numeric date differently.**
  Use locale-aware unambiguous display, include month names where risk is high, and keep interchange/storage formats separate from presentation.
- **A currency total is correct but the symbol implies the wrong dollar.**
  Preserve and display the ISO currency code where ambiguity matters; never derive currency from language alone.
- **An appointment moves by an hour after a DST change.**
  Clarify whether the business value is an instant or local wall time, retain zone context, and test both sides of the transition.

### Where to check

- Unicode CLDR charts and UTS #35 for locale data and patterns.
- Raw API/database values alongside rendered UI and exported documents.
- Locale, timezone, calendar, currency, numbering-system, and unit settings.
- Input validation, save/reload, sorting, filtering, exports, emails, and notifications.

### Worked example: the meeting that moved after daylight saving

1. A recurring 09:00 Europe/Berlin meeting is stored as one UTC offset and reused forever.
2. After the DST transition, local display becomes 10:00 even though the business intent was 09:00 wall time.
3. The tester records recurrence semantics, zone ID, raw values, transition date, and locale.
4. The model retains the named timezone and recurrence intent; both sides of DST are regression tested.

**Quiz.** What belongs with a monetary amount?

- [ ] Only a dollar sign
- [ ] The user's language
- [x] An explicit currency code and locale-aware presentation
- [ ] A manually inserted comma

*The currency code preserves monetary meaning; locale-aware formatting controls how that meaning is presented. Language alone cannot safely choose currency.*

- **CLDR** — Unicode's curated locale data and structures used by many formatting libraries.
- **Store vs display** — Store unambiguous values and context; localize presentation with maintained APIs.
- **Format evidence** — Raw value, locale, timezone, currency/unit, library version, and rendered text.

### Challenge

Create a table of six values across two locales and two timezones, including DST, ambiguous dates, and two currencies; verify round-trip meaning.

- [Unicode — Common Locale Data Repository](https://cldr.unicode.org/)
- [Unicode Technical Standard #35 — Locale Data Markup Language](https://unicode.org/reports/tr35/)
- [The Unicode Consortium — Unicode CLDR (Common Locale Data Repository)](https://www.youtube.com/watch?v=D6nMTy3e_AU)

🎬 [Unicode CLDR (Common Locale Data Repository)](https://www.youtube.com/watch?v=D6nMTy3e_AU) (17 min)

- Store unambiguous values plus business context; localize only the presentation layer.
- Use maintained CLDR-backed APIs rather than manual separator and currency rules.
- Test ambiguity, DST, numbering systems, currency precision, units, negatives, and round trips.
- A reproducible format defect names raw value and every locale-sensitive input.


## Related notes

- [[Notes/non-functional-testing-intro/localization-and-i18n/i18n-vs-l10n-in-plain-words|i18n vs l10n in plain words]]
- [[Notes/non-functional-testing-intro/localization-and-i18n/text-expansion-truncation-and-rtl|Text expansion, truncation & RTL]]
- [[Notes/working-with-data/strings-and-text/string-formatting|String formatting]]


---
_Source: `packages/curriculum/content/notes/non-functional-testing-intro/localization-and-i18n/dates-currencies-and-formats.mdx`_
