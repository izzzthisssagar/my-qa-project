---
title: "JSON & XML"
tags: ["api-testing-fundamentals", "http-for-testers", "track-c"]
updated: "2026-07-17"
---

# JSON & XML

*JSON and XML are two different scripts for writing down the same underlying data - objects/arrays/values vs elements/attributes/namespaces. Most 2026 APIs are JSON-first, but XML (SOAP, legacy enterprise, some config exports) is still very much alive.*

> Two APIs can describe the exact same flight - same ID, same status, same passenger count - and
> produce bodies that look nothing alike on the wire. One wraps everything in curly braces and
> colons. The other wraps everything in angle brackets and closing tags. Neither is "the right one" -
> they're both just notation for the same underlying data, and a tester who can only read one of them
> is blind to half the APIs still running in production, especially anything enterprise, government,
> or old enough to predate JSON's dominance.

> **In real life**
>
> The Rosetta Stone: one royal decree, carved three times on the same slab, in three different
> scripts - Egyptian hieroglyphs at the top, Egyptian demotic in the middle, Greek at the bottom.
> Three completely different visual systems, one identical underlying message. Scholars used the
> Greek (which they could already read) to crack the hieroglyphs, precisely because the CONTENT was
> guaranteed identical even though the NOTATION wasn't. That's exactly the relationship between a
> JSON body and an XML body describing the same resource: different brackets, different punctuation
> rules, same data - and once you can read one fluently, the other is a notation problem, not a
> comprehension problem.

**JSON vs XML**: JSON (JavaScript Object Notation) represents data as nested objects ({ }, key-value pairs), arrays ([ ], ordered lists), and primitive values (strings, numbers, booleans, null) - no distinction between 'attributes' and 'content', no native comments, no built-in schema enforcement (though JSON Schema exists as a separate, optional layer). XML (eXtensible Markup Language) represents data as nested elements (<tag>...</tag>), each of which can carry attributes (<tag attr='value'>) in addition to child elements or text content, supports comments (<!-- -->), and supports namespaces (xmlns) to avoid tag-name collisions when combining vocabularies from different sources. Both are text-based, both are hierarchical, and both are fully capable of representing the same information - the choice between them is almost always a platform/ecosystem decision, not a technical necessity.

## The differences that actually matter for testing

- **Attributes vs elements (XML only)** — the same fact can legally live as
  `<flight id="AI202">` or `<flight><id>AI202</id></flight>`. JSON has no equivalent split - every
  field is just a key. When testing an XML API, check the actual spec for which shape a given field
  uses; guessing from "similar" fields elsewhere in the same document is a common source of wasted
  time.
- **Arrays** — JSON has a first-class array type (`[1, 2, 3]`). XML has no equivalent; a "list" is
  just multiple sibling elements with the same tag name, and a single-item list is often
  indistinguishable on the wire from "just one element" unless the schema is explicit about
  cardinality - a real source of parsing bugs when a client assumes "always a list" and gets one bare
  element instead.
- **Types** — JSON has native `true`/`false`, `null`, and numbers-without-quotes. XML has none of
  these; everything is text, and "is this `1` supposed to be a number or a string" is answered only
  by the schema/docs, never by the XML itself.
- **Comments** — legal in XML (`<!-- note -->`), not legal anywhere in standard JSON. A "commented
  out" field in a hand-edited JSON fixture file is a silent syntax error waiting to happen.
- **Namespaces (XML only)** — let two different vocabularies share one document without tag-name
  collisions (`<soap:Body>` vs a plain ``). Testing SOAP or any namespaced XML API means
  reading the `xmlns` declarations, not just the tag names, or you'll misidentify which spec a given
  element actually belongs to.

> **Tip**
>
> Never guess the format from the URL or from habit - read `Content-Type` (see
> [[api-testing-fundamentals/http-for-testers/headers-and-bodies]]). Plenty of real APIs serve
> `application/xml` from an endpoint whose path looks exactly like a "modern JSON" endpoint, and
> plenty of internal enterprise systems still speak SOAP/XML exclusively even in 2026.

> **Common mistake**
>
> Treating a single JSON field's value type as guaranteed just because it "looks like" a number.
> `"phone": "0123"` as a JSON STRING preserves the leading zero; the same value as a bare JSON number
> `0123` isn't even valid JSON in the first place, and `123` as a number silently drops it. Testers
> who assume the API "must" use numbers for numeric-looking fields miss this exact class of
> data-corruption bug - always check the actual documented/observed type, never assume from
> appearance.

![The Rosetta Stone, a large dark stone slab showing three distinct bands of carved text - Egyptian hieroglyphs at the top, Egyptian demotic script in the middle, and ancient Greek at the bottom](json-and-xml.jpg)
*The Rosetta Stone, British Museum — Wikimedia Commons, CC BY-SA 4.0 (Hans Hillewaert). [Source](https://commons.wikimedia.org/wiki/File:Rosetta_Stone.JPG)*
- **Top band — hieroglyphs** — One notation for the royal decree - dense, pictographic, unreadable to most people at a glance. Think of this as the XML of the three: verbose, tag-heavy, unmistakably its own visual style.
- **Middle band — demotic script** — A different, more cursive Egyptian script - same content again, different marks entirely. A reminder that 'different notation' doesn't mean 'different amount of information' - all three bands carry the identical decree.
- **Bottom band — Greek** — The script scholars could already read, which is what let them crack the other two - think of this as the JSON of the three for a modern tester: usually the one you're already fluent in, useful as the anchor for cross-checking an unfamiliar XML body's actual meaning.

**The same flight record, two notations - press Play**

1. **XML version arrives, same data** — <flight id="AI202"><status>ON_TIME</status><delayMinutes>0</delayMinutes></flight> - one attribute, two child elements, everything is text until the schema says otherwise.
2. **A tester checks: is delayMinutes really a number in both?** — In JSON, yes - 0 with no quotes is a genuine JSON number. In XML, delayMinutes's TEXT is '0' - whether the consuming code parses it as an integer or leaves it as a string depends entirely on that code, not on the XML itself.
3. **A tester checks: id as attribute vs element** — The XML version chose an attribute (id="AI202"). Nothing stops a different endpoint on the SAME API from choosing a child element instead - always confirm per-field, per-endpoint, from the actual spec.
4. **Verdict** — Same three facts, two totally different sets of parsing rules. A tester who can name which rules apply to which notation catches type and structure bugs neither format's syntax alone will warn you about.

Same flight, parsed both ways, to show the two notations really do carry identical information:

*Run it - the same flight record, from JSON and from XML (Python)*

```python
import json
import xml.etree.ElementTree as ET

json_body = '{"flight": "AI202", "status": "ON_TIME", "delayMinutes": 0}'
xml_body = '<flight id="AI202"><status>ON_TIME</status><delayMinutes>0</delayMinutes></flight>'

parsed_json = json.loads(json_body)
print("From JSON:")
print(f"  flight id: {parsed_json['flight']!r} (type: {type(parsed_json['flight']).__name__})")
print(f"  status: {parsed_json['status']!r}")
print(f"  delayMinutes: {parsed_json['delayMinutes']!r} (type: {type(parsed_json['delayMinutes']).__name__})")

root = ET.fromstring(xml_body)
xml_id = root.attrib["id"]
xml_status = root.find("status").text
xml_delay_text = root.find("delayMinutes").text
print("From XML:")
print(f"  flight id: {xml_id!r} (type: {type(xml_id).__name__}, came from an ATTRIBUTE)")
print(f"  status: {xml_status!r}")
print(f"  delayMinutes: {xml_delay_text!r} (type: {type(xml_delay_text).__name__} - XML has no native number type)")
print(f"  delayMinutes as int, only after explicit parsing: {int(xml_delay_text)!r}")

# From JSON:
#   flight id: 'AI202' (type: str)
#   status: 'ON_TIME'
#   delayMinutes: 0 (type: int)
# From XML:
#   flight id: 'AI202' (type: str, came from an ATTRIBUTE)
#   status: 'ON_TIME'
#   delayMinutes: '0' (type: str - XML has no native number type)
#   delayMinutes as int, only after explicit parsing: 0
```

Same comparison in Java, using the JDK's built-in XML parser and a small hand-rolled JSON reader
(no external libraries needed to make the point):

*Run it - the same flight record, from JSON and from XML (Java)*

```java
import org.w3c.dom.*;
import javax.xml.parsers.*;
import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {
        String xmlBody = "<flight id=\\"AI202\\"><status>ON_TIME</status><delayMinutes>0</delayMinutes></flight>";

        DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
        Document doc = builder.parse(new ByteArrayInputStream(xmlBody.getBytes()));
        Element root = doc.getDocumentElement();

        String xmlId = root.getAttribute("id");
        String xmlStatus = root.getElementsByTagName("status").item(0).getTextContent();
        String xmlDelayText = root.getElementsByTagName("delayMinutes").item(0).getTextContent();

        System.out.println("From XML:");
        System.out.println("  flight id: " + xmlId + " (came from an ATTRIBUTE)");
        System.out.println("  status: " + xmlStatus);
        System.out.println("  delayMinutes: \\"" + xmlDelayText + "\\" (String - XML has no native number type)");
        int delayAsInt = Integer.parseInt(xmlDelayText);
        System.out.println("  delayMinutes as int, only after explicit parsing: " + delayAsInt);
    }
}

// From XML:
//   flight id: AI202 (came from an ATTRIBUTE)
//   status: ON_TIME
//   delayMinutes: "0" (String - XML has no native number type)
//   delayMinutes as int, only after explicit parsing: 0
```

### Your first time: Your mission: convert one real record between JSON and XML by hand

- [ ] Find or invent a small JSON object (3-5 fields, at least one number and one nested list) — A flight, a user profile, anything small enough to hand-convert without a tool.
- [ ] Write out the equivalent XML by hand, choosing attributes for at least one field and child elements for the rest — This forces the exact decision real API designers make - which is which is a judgment call, not a rule.
- [ ] Parse both back and compare the extracted values field by field — Confirm every value matches, and note which XML values came out as plain text needing explicit conversion (numbers, booleans) versus JSON's native types.
- [ ] Add a list with more than one item, then a list with exactly one item, in both formats — In JSON this is trivial ([x] vs [x,y]). In XML, check whether a single-item list is structurally distinguishable from 'just one element' in your chosen schema - often it isn't without an explicit wrapper.
- [ ] Say the verdict sentence — 'This field is [type] in JSON, and in XML it's [attribute/element] holding text that needs [parsing step] before it's usable as [type].'

You've done a real, by-hand format conversion - the fastest way to internalize that JSON and XML
disagree on notation, not on what data can be represented.

- **An XML API returns a single item for a field that's supposed to be a list, and the client code crashes trying to iterate it.**
  This is the classic XML single-item-list ambiguity: without an explicit list wrapper element or a schema saying 'always an array,' one item and 'a list of one' can be structurally identical. Confirm against the schema/WSDL whether the field is defined as repeatable - if so, this is a client bug (must handle the single-element case); if the schema doesn't guarantee repeatability, it's a client assumption bug, not an API bug.
- **A JSON field that always contained integers in testing suddenly arrives as a quoted string in one response.**
  Don't assume this is a formatting glitch - it may be a deliberate type change upstream (some backends switch a field from number to string specifically to preserve values like leading zeros or numbers too large for a client's native number type). Check the API's changelog/docs before filing a type-mismatch bug; if undocumented, THAT'S the bug to file (a silent type change, not the type itself).
- **An XML response fails to parse entirely, with an error mentioning an undefined namespace prefix.**
  Look for the xmlns declaration - or its absence. A namespaced element used without its corresponding xmlns attribute (or a prefix that doesn't match any declared namespace) is invalid XML, not a parser bug. Compare against a known-good sample response from the same API to see where the xmlns should have been declared.

### Where to check

- **`Content-Type` on the response** — `application/json` vs `application/xml`/`text/xml`; see [[api-testing-fundamentals/http-for-testers/headers-and-bodies]].
- **The API's schema** — a JSON Schema, an XSD, or a WSDL (for SOAP) is the actual source of truth for field types and cardinality, not "what one example response happened to show."
- **`curl -i` or Postman's raw response view** — see the actual bracket/tag notation unmodified, before any pretty-printer reformats it into something that hides the real structure.
- **BuggyAPI (TaskFlight)** — practice parsing its JSON responses by hand, and compare against its documented OpenAPI schema for field types.

### Worked example: a silent data-loss bug found by comparing JSON and XML side by side

1. A system exposes the same order data two ways: a newer JSON API and a legacy XML export used by
   an older reporting tool, both meant to be equivalent.
2. A tester pulls one order from each. The JSON shows `"orderId": "0042"` (a string, leading zero
   intact). The XML shows `<orderId>42</orderId>` - the leading zero is gone.
3. First instinct: "XML just doesn't support leading zeros the same way." Wrong instinct - XML text
   content can hold `"0042"` just as easily as JSON can; there's nothing about XML itself that
   would drop it.
4. Root cause, found by checking the export code: the legacy XML generator reads the ID through a
   numeric field type internally before serializing it as text, silently converting `"0042"` to the
   integer `42` and losing the leading zero in that conversion step - not in XML's notation rules at
   all.
5. This matters beyond cosmetics: if `orderId` is used as a lookup key anywhere downstream, `"0042"`
   and `"42"` are different keys, and the reporting tool's exports may already be silently failing to
   match orders whose IDs have leading zeros.
6. Finding: "Legacy XML export loses leading zeros on orderId due to an internal numeric-typed
   field, not an XML notation limitation - JSON API preserves the value correctly. Recommend fixing
   the export's internal type, not the schema." Found by comparing the SAME data across both
   notations, not by inspecting either one alone.

**Quiz.** An XML response contains `<delayMinutes>0</delayMinutes>` and the equivalent JSON response contains `'delayMinutes': 0`. A tester claims 'the XML version is wrong because 0 should be a number, and XML is showing it as text.' Is this a valid bug report?

- [ ] Yes - XML should be updated to support native numbers like JSON does
- [x] No - XML has no native number type at all; every value in XML is text content by design, and whether '0' gets treated as a number is entirely up to the code consuming it, not a defect in the XML itself
- [ ] Yes, but only if the API also returns JSON - if it's XML-only, this behavior is acceptable
- [ ] No, but only because delayMinutes is allowed to be zero - a non-zero value would make this a valid bug

*This note is explicit that XML simply has no native number/boolean/null types the way JSON does - everything in XML is text content, and interpreting that text as a number, date, or anything else is entirely the consuming application's job, guided by the schema/docs, not something XML notation itself gets 'right' or 'wrong.' This isn't a bug in the API; it's a structural property of the format the tester needs to know before filing anything. Option one asks for a feature XML fundamentally doesn't have by design. Option three invents a condition (JSON also existing) that has no bearing on whether XML's OWN behavior is correct. Option four invents an unrelated condition (the specific value) that doesn't change the underlying type-system fact at all.*

- **JSON vs XML, in one line** — Two different notations for the same kind of hierarchical data - JSON uses objects/arrays/native types; XML uses elements/attributes/text, with no native number or boolean type.
- **XML attribute vs element** — The same fact can legally be an attribute (<flight id="AI202">) or a child element (<id>AI202</id>) - always check the actual spec/schema per field, never assume from a 'similar' field elsewhere.
- **The XML single-item-list trap** — Without an explicit list wrapper or schema guarantee, one XML element and 'a list containing one element' can be structurally identical - a common client-side parsing bug.
- **What XML namespaces (xmlns) are for** — Letting two different tag vocabularies share one document without name collisions - essential for reading SOAP or any multi-vocabulary XML correctly.
- **Why 'XML shows numbers as text' isn't a bug** — XML has no native number type at all - every value is text by design. Whether '0' becomes an integer is entirely the consuming code's responsibility, not something the XML format itself gets wrong.

### Challenge

Take any JSON response from BuggyAPI (or a public sandbox) and hand-convert it to XML, making an
explicit, written decision for each field: attribute or element? Then hand-convert a JSON array
field into XML twice - once with more than one item, once with exactly one - and write down whether
your XML shape would let a parser tell the two cases apart without already knowing the schema.

### Ask the community

> I'm comparing a JSON and an XML representation of what's supposed to be the same resource, and field `[name]` looks different between them (`[JSON value]` vs `[XML value]`). Is this a real data bug, or an expected notation difference (e.g. type coercion, attribute-vs-element choice) I should account for before filing anything?

The most useful replies usually ask "what does the schema/spec say this field's TYPE and structure
should be" before answering yes/no - that's the actual test, not whether the two notations happen to
render it identically at a glance.

- [MDN — Working with JSON](https://developer.mozilla.org/en-US/docs/Web/JSON)
- [MDN — Introduction to XML](https://developer.mozilla.org/en-US/docs/Web/XML/XML_introduction)
- [code with mubbi — JSON Crash Course: Learn JSON in 10 Minutes](https://www.youtube.com/watch?v=euX2r2VN94I)

🎬 [code with mubbi — JSON Crash Course: Learn JSON in 10 Minutes](https://www.youtube.com/watch?v=euX2r2VN94I) (10 min)

- JSON and XML are two different notations for the same kind of hierarchical data - neither is more 'correct,' and plenty of real 2026 APIs (SOAP, legacy enterprise) are still XML-only.
- XML can express the same fact as either an attribute or a child element - always check the actual spec per field, never assume from a similar-looking field.
- XML has no native number/boolean/null type - everything is text, and interpreting it correctly is the consuming code's job, guided by the schema.
- A single XML element and a one-item list can be structurally identical without an explicit wrapper or schema guarantee - a real, common client-parsing bug.
- When the same data is available in both formats, comparing them side by side is a genuinely effective way to catch silent type or precision loss neither format's syntax alone would reveal.


## Related notes

- [[Notes/api-testing-fundamentals/http-for-testers/headers-and-bodies|Headers & bodies]]
- [[Notes/api-testing-fundamentals/status-codes-and-rest/reading-api-docs-and-swagger|Reading API docs & Swagger]]


---
_Source: `packages/curriculum/content/notes/api-testing-fundamentals/http-for-testers/json-and-xml.mdx`_
