---
title: "Pseudo-localization tricks"
tags: ["non-functional-testing-intro", "localization-and-i18n", "track-c"]
updated: "2026-07-20"
---

# Pseudo-localization tricks

*Generate pseudo-localized strings - accented characters, bracket markers, and deliberate expansion - to reveal internationalization defects like hard-coded text, truncation, and encoding gaps before real translation exists.*

> Real translations arrive late, cost money, and depend on people outside engineering. A team that waits
> for them to test internationalization finds every layout, encoding, and hard-coded-string defect during
> the least convenient week of the release. There is a cheaper way to fail early.

> **In real life**
>
> A broadcast engineer does not wait for the evening program to test a signal chain. A synthetic color-bar
> test card runs through the same pipeline first: it is not real content, but its known bars, edges, and
> near-black patches expose sync, color, and clipping problems immediately. Pseudo-localization plays a
> synthetic "test card" string through the product before a single real translation exists.

**Pseudo-localization**: Pseudo-localization is an automated pseudo-translation of source strings - adding accented characters, wrapping text in bracket markers, and expanding length - applied before real translation exists so that hard-coded text, truncation, and encoding defects surface early and cheaply, without depending on a translator.

## Engineer the defect, do not wait for the translator

A pseudo-localization tool walks every extracted string and returns an altered but still-readable
version: vowels gain diacritics, the whole string grows by roughly 30-50 percent, and bracket markers
wrap the start and end so a tester can spot truncation at a glance. Run the product against this
generated pseudo-locale exactly like a real locale switch. Anything that still renders in plain English
was never extracted into a translatable resource. Anything whose brackets get clipped will truncate
again under a real, longer translation.

> **Tip**
>
> Treat a visible, unaccented word as the highest-priority finding. It means the string was never
> externalized, so no translator will ever see it - the localization vendor cannot fix what engineering
> still owns.

> **Common mistake**
>
> Do not treat a passing pseudo-localization pass as proof the product is translation-ready. It proves the
> mechanism - extraction, encoding, and flexible layout - works. Terminology accuracy, tone, and cultural
> fit still require a native-speaker review pass with real content.

![The SMPTE color bar test pattern with a full-height bar row, a castellated calibration row, and a bottom row of black, white, and near-black reference patches](pseudo-localization-tricks.jpg)
*SMPTE Color Bars — Denelson83, Wikimedia Commons, Public domain. [Source](https://commons.wikimedia.org/wiki/File:SMPTE_Color_Bars.svg)*
- **A synthetic full-range signal** — Like a pseudo-locale string, this pattern is not real content - it is engineered to make every value visible at once, before a real broadcast or translation exists.
- **High-contrast calibration block** — Alternating blocks pinpoint an exact boundary, the same job bracket markers do around a pseudo-localized string.
- **Near-black registration patches** — Fine reference patches catch subtle errors a casual glance would miss - just as accented characters catch silent encoding or font-fallback defects.
- **Full white clipping block** — An extreme reference value exposes clipping, the same way a deliberately expanded pseudo-localized string exposes truncation and layout overflow.

**A pseudo-localization pass**

1. **Generate a pseudo-locale from source strings** — Automated tooling accents characters, adds bracket markers, and expands length without waiting on translators.
2. **Run the product against the pseudo-locale** — Every screen, dialog, error, and notification the source locale reaches should also render pseudo-localized text.
3. **Inspect layout, encoding, and hard-coded text** — Clipped bracket markers, mangled accents, and unchanged English reveal defects immediately.
4. **Fix engineering gaps before real translation arrives** — Real localization then adapts content instead of also fighting rigid containers and missing extraction.

*A pseudo-localization string transformer (Python)*

```python
def pseudo_localize(text):
    accents = {
        "a": "å", "e": "é", "i": "î", "o": "ö", "u": "ü",
        "A": "Å", "E": "É", "I": "Î", "O": "Ö", "U": "Ü",
    }
    accented = "".join(accents.get(ch, ch) for ch in text)
    padded = accented + " " + accented[: max(1, len(accented) // 3)]
    return "[!! " + padded + " !!]"

samples = ["Save", "Checkout complete", "Add to cart"]
checks = {}
for s in samples:
    out = pseudo_localize(s)
    checks[s + "_has_brackets"] = out.startswith("[!!") and out.endswith("!!]")
    checks[s + "_is_longer"] = len(out) > len(s)
    checks[s + "_has_accent"] = any(ord(c) > 127 for c in out)
    print(s + " -> " + out)

result = "PASS" if all(checks.values()) else "FAIL"
assert result == "PASS", "pseudo-localization transform rejected"
print("RESULT=" + result)
```

*A pseudo-localization string transformer (Java)*

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class Main {
    static String pseudoLocalize(String text) {
        String src = "aeiouAEIOU";
        String dst = "åéîöüÅÉÎÖÜ";
        StringBuilder accented = new StringBuilder();
        for (char ch : text.toCharArray()) {
            int idx = src.indexOf(ch);
            accented.append(idx >= 0 ? dst.charAt(idx) : ch);
        }
        String accentedStr = accented.toString();
        String extra = accentedStr.substring(0, Math.max(1, accentedStr.length() / 3));
        String padded = accentedStr + " " + extra;
        return "[!! " + padded + " !!]";
    }

    static boolean hasNonAscii(String s) {
        for (char c : s.toCharArray()) if (c > 127) return true;
        return false;
    }

    public static void main(String[] args) {
        String[] samples = { "Save", "Checkout complete", "Add to cart" };
        Map<String, Boolean> checks = new LinkedHashMap<>();
        for (String s : samples) {
            String out = pseudoLocalize(s);
            checks.put(s + "_has_brackets", out.startsWith("[!!") && out.endsWith("!!]"));
            checks.put(s + "_is_longer", out.length() > s.length());
            checks.put(s + "_has_accent", hasNonAscii(out));
            System.out.println(s + " -> " + out);
        }
        boolean ok = true;
        for (var e : checks.entrySet()) ok &= e.getValue();
        String result = ok ? "PASS" : "FAIL";
        if (!result.equals("PASS")) throw new AssertionError("pseudo-localization transform rejected");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Run a first pseudo-localization pass

- [ ] Generate or enable a pseudo-locale — Use a build tool, resource-bundle generator, or the sample transformer to accent, expand, and bracket every extracted string.
- [ ] Switch the running product to that pseudo-locale — Visit navigation, forms, empty states, errors, toasts, and emails - not only the happy path.
- [ ] Flag unaccented, unbracketed text — Plain English inside a pseudo-localized screen is a hard-coded string that no translator will ever reach.
- [ ] Flag clipped brackets and broken accents — A missing closing marker or mangled character is a truncation or encoding defect, independent of any real translation.

- **A button still reads plain English under the pseudo-locale.**
  Trace the string to its source; it was never externalized into a translatable resource, so route it to engineering, not the localization vendor.
- **The trailing `!!]` marker is clipped off a pseudo-localized label.**
  The container is fixed-width; remove the constraint or use an approved flexible layout pattern, then rerun the pseudo-locale pass.
- **Accented characters render as boxes or question marks.**
  Check encoding end to end - source files, database columns, HTTP headers, and fonts - since pseudo-localization only surfaces the defect, it does not explain which layer caused it.

### Where to check

- Extracted message catalogs versus every string actually rendered under the pseudo-locale.
- Fixed-width containers, truncation, and ellipsis behavior on expanded pseudo-localized text.
- Encoding at the source file, database, transport, and font-rendering layers.
- [[non-functional-testing-intro/localization-and-i18n/text-expansion-truncation-and-rtl]] for the deeper layout and direction checks a pseudo-locale pass first flags.

### Worked example: the vanishing bracket marker

1. QA enables an English-based pseudo-locale before any real translation is ready.
2. A settings dialog title renders "Preferen" - the expansion and trailing "!!]" marker are missing.
3. The tester records the string key, the expected pseudo-localized form, and the clipped rendered result.
4. Engineering removes a fixed-width container; the same key is retested and every other dialog title is swept for the identical pattern.

**Quiz.** What is the main purpose of pseudo-localization?

- [ ] Provide accurate translations ready for release
- [x] Reveal internationalization defects before real translations exist
- [ ] Replace native-speaker linguistic review
- [ ] Measure server response time under load

*Pseudo-localization is engineered, not accurate, text. It stresses extraction, encoding, and flexible layout early so real translation work does not also have to fight engineering gaps.*

- **Pseudo-localization** — Automated accenting, bracketing, and expansion of source strings to test internationalization before real translation exists.
- **Unaccented text under a pseudo-locale** — A hard-coded string that was never externalized - an engineering defect, not a translation gap.
- **Clipped bracket marker** — Evidence of a fixed-width container that will also truncate a real, longer translation.

### Challenge

Generate a pseudo-localized version of five strings from one screen, run the screen, and classify every finding as extraction, layout, or encoding.

- [Microsoft — Pseudo-Localization](https://learn.microsoft.com/en-us/globalization/methodology/pseudolocalization)
- [Android Developers — Pseudolocales](https://developer.android.com/guide/topics/resources/pseudolocales)
- [Android Testing Tip: Pseudo-Localization Explained](https://www.youtube.com/watch?v=Wvx89P-rguQ)

🎬 [Android Testing Tip: Pseudo-Localization Explained](https://www.youtube.com/watch?v=Wvx89P-rguQ) (3 min)

- Pseudo-localization generates engineered, readable-but-altered strings before real translation exists.
- An unaccented string under a pseudo-locale is a hard-coded-text defect, not a translation gap.
- A clipped bracket marker predicts truncation that a real, longer translation will also hit.
- A clean pseudo-localization pass proves the mechanism works; it does not replace native-speaker review.


## Related notes

- [[Notes/non-functional-testing-intro/localization-and-i18n/i18n-vs-l10n-in-plain-words|i18n vs l10n in plain words]]
- [[Notes/non-functional-testing-intro/localization-and-i18n/text-expansion-truncation-and-rtl|Text expansion, truncation & RTL]]
- [[Notes/non-functional-testing-intro/localization-and-i18n/dates-currencies-and-formats|Dates, currencies & formats]]


---
_Source: `packages/curriculum/content/notes/non-functional-testing-intro/localization-and-i18n/pseudo-localization-tricks.mdx`_
