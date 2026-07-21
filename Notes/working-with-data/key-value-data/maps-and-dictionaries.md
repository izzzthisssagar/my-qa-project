---
title: "Maps & dictionaries"
tags: ["working-with-data", "java", "python", "data-structures", "track-b"]
updated: "2026-07-11"
---

# Maps & dictionaries

*A list finds things by position; a map finds them by name. When you want the value FOR a key — a product's price, a user by id, a word's count — a dictionary gives it instantly, without scanning. It's the structure behind config, JSON, caches, and half the code you'll test.*

> You already know a list: a row of things you reach by *position* — item 0, item 1, item 2. But
> most real questions aren't "what's at position 5?" They're "what's the price *of this product*?",
> "who is the user *with this id*?", "how many times did *this word* appear?" Those are lookups by
> **name**, not position — and doing them with a list means scanning every item until you find a
> match. A **map** (Python calls it a **dictionary**) is built for exactly this: you hand it a
> **key** and it hands back the **value**, instantly, no matter how many entries it holds. It's the
> single most useful data structure after the list, and it's everywhere.

> **In real life**
>
> A dictionary is a wall of PO boxes. Each box has a **number** on the front — that's the key — and
> whatever's inside is the **value**. To get your mail you don't open every box in the building; you
> walk straight to *your* number and open that one. That's the whole magic: lookup by label, not by
> searching. Two more things the boxes get right: every number is **unique** (there's one box 2308,
> not three), and an empty or nonexistent number gives you **nothing** rather than someone else's
> mail. A dictionary is that wall, in code — go directly to the key, get the value, done.

## What a map gives you that a list doesn't

A list and a map both hold many things. The difference is *how you get to them*, and it changes
what each is good for:

**Lookup by key, not position.** `prices["apple"]` goes straight to the value for `"apple"`. No
loop, no scanning — the same speed whether the map has 10 entries or 10 million.

**Keys are unique.** Put a value at a key that already exists and you *overwrite* it — there's one
slot per key. This is why a map is perfect for "the latest value for each id" or "the count for
each word".

**Missing keys are handled, not guessed.** Ask for a key that isn't there and you get a clear
signal — a `KeyError` in Python (or `null` in Java) — not a wrong answer. Both languages give you a
safe way to say "give me the value, or this default if it's missing".

![A wall of numbered PO boxes, one open and full of mail, each box labelled with a unique number](po-boxes.jpg)
*PO boxes — Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:USPS_Post_office_boxes_1.jpg)*
- **The box NUMBER (23072) = the KEY** — Every box wears a unique number on the front. That number is the key: a label you use to find one specific box out of hundreds. In code it's `prices['apple']` or `users[42]` — the thing in the brackets is the key, and it's how you address exactly one entry without touching the others. Keys are usually strings or numbers, and each one points at a single slot.
- **The mail inside = the VALUE** — Open the box and there's the mail — that's the value stored at that key. A value can be anything: a price, a name, a list, another whole dictionary. The key is how you FIND it; the value is what you GET. `prices['apple']` returns the value `30`; the key was 'apple', the value is the number.
- **Going straight to YOUR box = instant lookup** — You don't open all 300 boxes to find yours — you walk to your number and open that one. That's the superpower over a list: a list would make you check item after item until you found a match; a map jumps straight to the key. Same speed with 10 entries or 10 million. This is why maps back caches, config, and any 'look up X by its id' code.
- **Each number appears ONCE = keys are unique** — There's exactly one box 2308 — you can't have two. Put mail in it twice and the second delivery joins (or replaces) the first in the SAME box. Maps work identically: assign to a key that already exists and you OVERWRITE the old value. That's the feature behind 'keep the latest value per id' and 'count each word' — one slot per key, updated in place.
- **A wrong or empty box = nothing, not someone else's mail** — Ask for a box number that doesn't exist and you get nothing — not a random neighbour's letters. In code, a missing key gives a clear signal (Python raises KeyError; Java returns null), and both let you ask safely for 'the value, or a default if absent'. This is why maps are safe: a missing key is an honest 'not here', never a silently wrong answer.

**List search vs map lookup — press Play**

1. **The question: what's the price of 'cherry'?** — You have product names and their prices. You want one price, for one named product. This is a lookup BY NAME — exactly the shape a map is built for, and exactly the shape a list is bad at.
2. **With a LIST, you scan** — A list of (name, price) pairs forces you to walk from the start: is item 0 'cherry'? No. Item 1? No. Item 2? ... You check each until you find a match. With three products it's fine; with three million it's slow, every single time.
3. **With a MAP, you jump** — `prices['cherry']` goes straight to the value. The map computes where 'cherry' lives and reads it directly — no walking the entries. Ten items or ten million, it's the same quick step. That's the difference between searching and looking up.
4. **Missing key? A clear signal** — Ask for `prices['durian']` when there's no durian and the map tells you plainly — KeyError (Python) or null (Java) — or hands back your chosen default with `.get('durian', 0)`. It never returns the price of some other fruit by mistake.
5. **Same key again? Overwrite** — `prices['cherry'] = 50` replaces the old value in the one 'cherry' slot. Keys are unique, so a map naturally holds 'the current value for each name' — which is why counting, grouping, and caching all fall out of it so cleanly.

Here's a dictionary in Python doing the things you'll actually use it for — lookup, safe-lookup,
update, membership, iteration, and the classic *counting* idiom:

*Run it — a Python dictionary, the everyday operations*

```python
# A dict maps keys -> values. Here: PO box number -> what's inside.
inbox = {"2308": "electric bill", "23072": "postcard", "2300": "bank letter"}

print("box 2308 holds:", inbox["2308"])          # lookup by key -- instant
inbox["2308"] = "electric bill (PAID)"           # same key overwrites the value
inbox["2400"] = "new tenant letter"              # a new key adds an entry

print("has box 9999?", "9999" in inbox)          # membership test -> False
print("safe get:", inbox.get("9999", "empty"))   # missing key -> default, no crash
# print(inbox["9999"])  # this WOULD raise KeyError -- the unsafe way

print("all boxes:")
for box, mail in inbox.items():                  # iterate keys AND values
    print(f"   box {box}: {mail}")

# The classic use: COUNT things with a dict
words = ["apple", "pear", "apple", "kiwi", "apple", "pear"]
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1             # get-or-zero, then add one
print("counts:", counts)
```

Now the same ideas in Java, using `HashMap`. Note two differences: you declare the key and value
types up front, and a missing key returns `null` instead of raising — so `getOrDefault` is your friend:

*Run it — a Java HashMap, the same operations*

```java
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        Map<String, String> inbox = new HashMap<>();
        inbox.put("2308", "electric bill");
        inbox.put("23072", "postcard");
        inbox.put("2300", "bank letter");

        System.out.println("box 2308 holds: " + inbox.get("2308"));      // lookup by key
        inbox.put("2308", "electric bill (PAID)");                       // same key overwrites
        inbox.put("2400", "new tenant letter");                          // new key adds

        System.out.println("has box 9999? " + inbox.containsKey("9999"));      // false
        System.out.println("box 9999 get: " + inbox.get("9999"));             // null, not a crash
        System.out.println("safe get: " + inbox.getOrDefault("9999", "empty"));// default instead

        System.out.println("all boxes:");
        for (Map.Entry<String, String> e : inbox.entrySet()) {           // iterate keys + values
            System.out.println("   box " + e.getKey() + ": " + e.getValue());
        }

        // The classic use: COUNT things with a map
        String[] words = {"apple", "pear", "apple", "kiwi", "apple", "pear"};
        Map<String, Integer> counts = new HashMap<>();
        for (String w : words) counts.put(w, counts.getOrDefault(w, 0) + 1);
        System.out.println("counts: " + counts);
    }
}
```

map (dictionary)

> **Tip**
>
> The moment you catch yourself writing a loop that scans a list to find "the item whose name/id
> equals X", stop — that's a map waiting to happen. Build a dictionary keyed by that name/id once,
> and every future lookup is a direct `d[key]` instead of another full scan. This one refactor turns
> slow, repetitive "search the list again" code into instant lookups, and it's one of the most
> common performance fixes there is. The tell is always the same: a loop whose only job is to find a
> match by a field. Key by that field instead.

### Your first time: Your mission: look things up by name

- [ ] Do a direct lookup — In the Python playground, `inbox['2308']` returns its value instantly — no loop. That's the whole point of a map: name in, value out. Change the key to '2300' and see a different value.
- [ ] Trip (and dodge) the missing key — Uncomment `print(inbox['9999'])` and run — a KeyError, because there's no box 9999. Comment it back and use `inbox.get('9999', 'empty')` instead. Now missing is handled, not a crash.
- [ ] Overwrite a key — Notice `inbox['2308'] = ...` replaces the value in the SAME slot — keys are unique. Add `inbox['2308'] = 'junk mail'` at the end and confirm only the latest value survives.
- [ ] See Java's null instead of KeyError — In the Java playground, `inbox.get('9999')` returns `null` (not a crash), while `getOrDefault` gives your default. Same idea, different missing-key behaviour — know which language does which.

You've now looked up, added, overwritten, safely handled a missing key, and counted with a map — the operations that cover the vast majority of real map use.

- **KeyError (Python) or a NullPointerException soon after a map lookup (Java).**
  You asked for a key that isn't in the map. Python raises KeyError immediately; Java returns null, which then blows up when you use it. Use the safe form: Python `d.get(key, default)` or `if key in d`, Java `map.getOrDefault(key, default)` or `containsKey`. Never assume a key is present — check, or supply a default.
- **I added an entry but an old one disappeared.**
  You reused a key. Keys are unique — `d['x'] = 1` then `d['x'] = 2` leaves only `2`; the first value is gone. If you genuinely need multiple values for one key, the value should be a LIST: `d.setdefault('x', []).append(...)` in Python, or a `Map` of key to `List` in Java. One key, one slot — unless the slot holds a collection.
- **My counts / groups come out wrong or crash on the first item.**
  The get-or-default is missing. `counts[w] = counts[w] + 1` fails the first time w is seen (KeyError — it's not there yet). Use `counts.get(w, 0) + 1` (Python) or `getOrDefault(w, 0) + 1` (Java) so the first sighting starts from zero. This is the single most common bug in counting code.
- **The order of my dictionary isn't what I expected.**
  Depends on language/version. Modern Python dicts keep INSERTION order (since 3.7); Java's HashMap does NOT guarantee any order — use LinkedHashMap for insertion order or TreeMap for sorted keys. If your output ordering matters, don't rely on a plain HashMap's iteration order; choose the map type that promises the order you need.
- **I tried to use a list (or another mutable thing) as a key and it failed.**
  Keys must be hashable/immutable, because the map hashes the key to decide where to store it — and a mutable key could change after storage, breaking the lookup. Use a string, number, or tuple (Python) as the key, not a list. If you need a compound key, join it into a string or use a tuple.

### Where to check

Maps are everywhere in the systems you'll test, so learn to spot and probe them:

- **A missing key** — does the code use `.get`/`getOrDefault`/`containsKey`, or does it assume the key exists? The assume-it-exists path is a crash waiting for the input that omits that key.
- **A duplicate/overwritten key** — if input can repeat a key, is the last-write-wins behaviour intended, or is data being silently lost?
- **The counting/grouping start** — is there a get-or-zero (or get-or-empty-list) so the first item doesn't crash?
- **JSON is maps** — an API response object IS a dictionary; testing "the response has field X" is a key-presence check, and "X has the right value" is a lookup. Map thinking is API thinking.
- **Order assumptions** — if a test asserts on the order of a map's keys, is that order actually guaranteed by the map type, or is the test relying on luck?

Tester's habit: **the highest-value input against map code is the missing key.** The developer wrote
for the keys they expected; you send the request without one, or with an extra, or with a duplicate.
Config missing a setting, a JSON body without an optional field, a lookup id that doesn't exist —
these are where map code cracks, because "the key is always there" is the assumption that fails.

### Worked example: the config key that wasn't always there

1. **The report:** "The app crashes on startup for some customers, fine for others. The error mentions a config value, but the config files all look complete to us."
2. **The developer opens their own config** — every key present — and can't reproduce it. They suspect file corruption, disk issues, anything but the code, because on every config THEY have, it works.
3. **A tester looks at HOW the config is read:** `timeout = config["retry_timeout"]` — a direct map lookup, no default. It assumes every config contains a `retry_timeout` key.
4. **They test with a config that OMITS that key** — an older customer's file, written before `retry_timeout` was added. Instant `KeyError: 'retry_timeout'` at startup. Reproduced in one try.
5. **Why only some customers?** Newer configs, generated by a newer installer, include the key; older ones, never migrated, don't. It was never random — it was 'old config vs new config', a split nobody had tested along.
6. **The fix is the safe lookup:** `timeout = config.get("retry_timeout", 30)` — use the configured value if present, otherwise a sensible default. One method call turns a hard crash into a graceful fallback, and every old config now starts fine.
7. **Why the developer missed it.** They only ever ran with complete configs, so the missing-key path never executed for them. The bug lived entirely in an input they didn't have — which is precisely the input a tester's job is to supply.
8. **The lesson for a tester.** Map code fails at the KEY THAT ISN'T THERE, and the person who wrote it almost never has that input, because they built the map with all its keys present. Your instinct at every map lookup should be 'what if this key is missing?' — omit it, and watch whether the code defaults gracefully or falls over. That single question finds a whole category of production crashes before they ship.

> **Common mistake**
>
> Looking up a key without handling its absence: `value = data["key"]` when `"key"` might not be
> there. It works perfectly in every test where the key is present — which is every test the author
> thought to write — and crashes the first time real input omits it. The safe form costs three extra
> characters (`data.get("key", default)` / `map.getOrDefault("key", default)`) and converts a hard
> failure into a defined fallback. Reach for the safe lookup by default, and only use the raw `[key]`
> form when a missing key genuinely *should* be a loud error — in which case, make sure that's a
> deliberate choice, not an accident.

**Quiz.** You have 10,000 products and need the price of one, looked up by product name, many times. Why is a dictionary/map far better here than a list of (name, price) pairs?

- [ ] A list can't store prices
- [x] A map looks up by KEY directly — `prices['cherry']` jumps straight to the value at the same speed whether there are 10 or 10,000,000 entries. A list forces you to SCAN from the start, checking each pair until you find the matching name, which gets slower as the list grows and repeats the whole scan every lookup.
- [ ] A map uses less memory than a list always
- [ ] There is no real difference; both are equally fast

*This is the defining advantage of a map and the instinct to build: lookup by name is a map's whole reason to exist. A list stores things by position, so to find 'the pair whose name is cherry' you have to walk the list comparing names — fine for a handful, painfully slow for thousands, and you pay that cost on EVERY lookup. A map computes where 'cherry' lives from the key itself and reads it directly, in effectively constant time regardless of size. The practical tell, which shows up constantly in real code: any loop whose only job is to find an item by matching a field is a list being used where a map belongs — key by that field once and every lookup becomes instant. Recognising 'this is a lookup by name, use a map' is one of the highest-leverage habits in programming, and spotting its ABSENCE (a scan-the-list loop) is a common performance finding for a tester.*

- **What is a map / dictionary?** — A structure of key→value pairs where you fetch the value BY KEY directly, no scanning. Python: dict. Java: HashMap. Keys are unique; lookup stays fast at any size.
- **Map vs list — the core difference** — A list finds by POSITION (item 5); a map finds by KEY/name (prices['apple']). Use a map whenever the natural question is 'the value FOR this name/id'.
- **What happens when you reuse a key?** — You OVERWRITE the old value — one slot per key. That's why maps naturally hold 'latest value per id' and power counting/grouping.
- **How do you handle a missing key safely?** — Python: `d.get(key, default)` or `if key in d`. Java: `map.getOrDefault(key, default)` or `containsKey`. Raw `d[key]` raises KeyError (Py) / returns null (Java).
- **The counting idiom** — `counts[w] = counts.get(w, 0) + 1` (Py) / `getOrDefault(w, 0) + 1` (Java). Get-or-zero then add — so the first sighting starts at 0 instead of crashing.
- **Do maps keep order?** — Python dict: insertion order (3.7+). Java HashMap: NO order guarantee — use LinkedHashMap (insertion) or TreeMap (sorted). Don't rely on HashMap iteration order.
- **The tester's instinct for map code** — Ask 'what if this key is missing?' Omit the key, send a duplicate, add an extra. The missing key is where map code — written assuming the key is present — cracks.

### Challenge

In the Python playground, build a dictionary the other way: start empty and add three boxes with
`inbox[number] = mail`. Then look up a number you didn't add and predict — KeyError or default? —
before running it both ways (`inbox[bad]` vs `inbox.get(bad, 'no such box')`). Finally, extend the
counting loop to also print WHICH word was most common (hint: `max(counts, key=counts.get)`). Write
one sentence: given an API response as a dictionary, what's the first missing-key test you'd run
against code that reads a field from it?

### Ask the community

> Map/dict question: I did `[lookup or update]` and got `[KeyError / null / wrong value / lost an entry]`. Language: `[Java/Python]`. The key involved: `[paste]`. Did I use safe access (.get / getOrDefault / containsKey)? `[yes/no]`. Could the key be missing or duplicated in my input? `[yes/no]`.

Almost every map bug is one of two things: a missing key accessed unsafely (KeyError/null), or a
duplicate key silently overwriting. Say which language, whether you used safe access, and whether
your input can miss or repeat the key — that pins it down fast.

- [Python docs — dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- [Java tutorial — the Map interface and HashMap](https://docs.oracle.com/javase/tutorial/collections/interfaces/map.html)
- [Real Python — dictionaries in depth](https://realpython.com/python-dicts/)
- [JSON — which is, structurally, just maps and lists](https://www.json.org/json-en.html)

🎬 [Dictionaries / hash maps explained](https://www.youtube.com/watch?v=daefaLgNkw0) (9 min)

- A map (Python dict, Java HashMap) fetches a value BY KEY directly — no scanning — at the same speed for 10 or 10 million entries. Use it whenever the question is 'the value FOR this name/id'.
- Keys are unique: assigning to an existing key overwrites it. That's what makes maps natural for 'latest value per id', counting, and grouping.
- Handle missing keys safely: `d.get(key, default)` / `getOrDefault` / `containsKey`. Raw `d[key]` raises KeyError (Python) or returns null (Java) — the assume-it-exists path is a crash waiting for the input that omits it.
- The counting idiom is get-or-zero-then-add: `counts.get(w, 0) + 1`. Forgetting the default is the most common counting bug.
- For a tester: JSON responses and config ARE maps, and the highest-value input is the MISSING key — omit a field, and check whether the code defaults gracefully or falls over.


---
_Source: `packages/curriculum/content/notes/working-with-data/key-value-data/maps-and-dictionaries.mdx`_
