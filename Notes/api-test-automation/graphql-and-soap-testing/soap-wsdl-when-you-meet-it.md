---
title: "SOAP & WSDL — when you meet it"
tags: ["api-test-automation", "graphql-and-soap-testing", "track-d"]
updated: "2026-07-17"
---

# SOAP & WSDL — when you meet it

*SOAP is an XML messaging framework; WSDL describes service operations and concrete bindings. Learn envelopes, namespaces, faults, and contract-first tests without calling all XML SOAP.*

> SOAP is not "the old API with angle brackets." XML is the paper; SOAP is the envelope rules; WSDL is the service directory and wiring diagram. Mixing those up makes every failure look like "XML weirdness."

> **In real life**
>
> A mailed letter has an outer envelope, optional routing marks, a body, and a known destination. SOAP defines that message envelope; WSDL says which letters the service accepts, where, and through which binding.

**SOAP and WSDL**: SOAP 1.2 is an XML-based messaging framework whose message has one Envelope, an optional Header, and a mandatory Body that may contain application content or a Fault. WSDL describes service interfaces, operations, messages, bindings, and concrete endpoints.

## Read the layers in order

- Confirm SOAP version by its envelope namespace; SOAP 1.1 and 1.2 differ.
- Inspect optional headers, including role and `mustUnderstand` behavior.
- Validate body XML namespaces and element qualification, not just local names.
- Use WSDL operation/message definitions plus the binding to derive wire details.
- Assert SOAP Fault structure as well as HTTP transport behavior.
- SOAP 1.2 XML over HTTP uses `application/soap+xml`; do not blindly copy SOAP 1.1 headers.

> **Tip**
>
> Generate a sample request from the exact WSDL version, then reduce it carefully. Namespaces that look decorative are part of element identity.

> **Common mistake**
>
> Validating only that XML parses. Well-formed XML can have the wrong SOAP namespace, wrong body element, wrong operation, or a perfectly structured Fault.

![A white envelope icon with a letter visibly emerging from it](soap-wsdl-when-you-meet-it.jpg)
*Envelope-letter icon — paomedia, Wikimedia Commons, CC0 1.0. [Source](https://commons.wikimedia.org/wiki/File:Envelope-letter-icon.png)*
- **Header area** — SOAP headers carry processing instructions and intermediaries' metadata when present.
- **The envelope** — Its namespace identifies the SOAP version and frames the message.
- **Body payload** — The body carries application content or a SOAP Fault, constrained by the service contract.

**From WSDL to a verified SOAP exchange**

1. **Locate service and endpoint** — Read the concrete address associated with the binding.
2. **Choose an operation** — Trace its input, output, and declared faults.
3. **Inspect the binding** — Determine protocol, message format, action, and style details.
4. **Build the SOAP envelope** — Use the correct version namespace, headers, body, and application namespaces.
5. **Validate response or Fault** — Check transport, envelope structure, body schema, and business result.

*Run it — inspect a SOAP envelope (Python)*

```python
import xml.etree.ElementTree as ET

xml = '''<env:Envelope xmlns:env="http://www.w3.org/2003/05/soap-envelope"
 xmlns:t="urn:tickets"><env:Body><t:GetTicket><t:id>T-7</t:id></t:GetTicket></env:Body></env:Envelope>'''
root = ET.fromstring(xml)
soap = "{http://www.w3.org/2003/05/soap-envelope}"
body = root.find(soap + "Body")
operation = list(body)[0]
print("SOAP 1.2 envelope:", root.tag == soap + "Envelope")
print("Body operation:", operation.tag)
print("Ticket id:", list(operation)[0].text)

# SOAP 1.2 envelope: True
# Body operation: {urn:tickets}GetTicket
# Ticket id: T-7
```

*Run it — classify a SOAP body or fault (Java)*

```java
import javax.xml.parsers.*;
import org.w3c.dom.*;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class Main {
  public static void main(String[] args) throws Exception {
    String xml = "<e:Envelope xmlns:e='http://www.w3.org/2003/05/soap-envelope'><e:Body><e:Fault><e:Code><e:Value>e:Sender</e:Value></e:Code><e:Reason><e:Text xml:lang='en'>Bad id</e:Text></e:Reason></e:Fault></e:Body></e:Envelope>";
    var factory = DocumentBuilderFactory.newInstance(); factory.setNamespaceAware(true);
    Document doc = factory.newDocumentBuilder().parse(new ByteArrayInputStream(xml.getBytes(StandardCharsets.UTF_8)));
    NodeList faults = doc.getElementsByTagNameNS("http://www.w3.org/2003/05/soap-envelope", "Fault");
    System.out.println("SOAP fault present: " + (faults.getLength() == 1));
    System.out.println("Reason: " + doc.getElementsByTagNameNS("http://www.w3.org/2003/05/soap-envelope", "Text").item(0).getTextContent());
  }
}

/* SOAP fault present: true
   Reason: Bad id */
```

### Your first time: Your mission: test one WSDL operation

- [ ] Find the service endpoint and binding — Do not infer wire details from operation names alone.
- [ ] Generate one valid envelope — Preserve SOAP and application namespaces.
- [ ] Send valid and invalid requests — Capture both normal body and SOAP Fault.
- [ ] Validate at four layers — Transport, envelope, body schema, and business result.

You have turned a wall of XML into four ordinary, diagnosable checks.

- **Server reports version mismatch.**
  Check the Envelope namespace and media type; SOAP 1.1 and SOAP 1.2 are not interchangeable labels.
- **Operation is not recognized.**
  Inspect binding details, action, body namespace, and qualified operation element from the exact WSDL.
- **XML assertion finds no element that visibly exists.**
  Use namespace-aware parsing; a local name without its namespace is not the same expanded name.

### Where to check

- WSDL service/port endpoint, interface or portType operation, and binding.
- SOAP Envelope namespace, Header, Body, and Fault.
- XML Schema imports and target namespaces.
- HTTP media type and action rules for the SOAP version in use.

### Worked example: the request that looked identical but used the wrong namespace

1. A generated request uses SOAP 1.2's envelope namespace.
2. A copied test replaces it with the SOAP 1.1 namespace but keeps identical local element names.
3. The XML remains well formed, so a parse-only test passes.
4. The service rejects the message as a version mismatch.
5. A namespace-aware assertion catches the wrong expanded Envelope name before transmission.

**Quiz.** Why must a SOAP test parse XML with namespace awareness?

- [ ] Namespaces only change indentation
- [x] Namespace URI plus local name defines element identity
- [ ] SOAP forbids prefixes
- [ ] WSDL is JSON

*Two elements with the same local name but different namespace URIs are different elements, including the version-defining SOAP Envelope.*

- **SOAP Envelope** — Versioned XML wrapper containing optional Header and mandatory Body.
- **WSDL binding** — Concrete protocol and message-format details for abstract operations.
- **SOAP Fault** — Structured SOAP error carried in the Body; inspect it rather than relying only on HTTP.

### Challenge

Take one SOAP response and write four assertions: expected media type/status, SOAP version namespace, expected body operation or Fault, and one business value. Break each layer independently.

### Ask the community

> WSDL operation `[name]` through binding `[binding]` rejects this envelope with `[fault]`. SOAP version/media type/action are `[values]`. Which contract layer is inconsistent?

Include namespace URIs and exact Fault; pretty-printed XML without them hides the bug.

- [W3C SOAP 1.2 Part 1 — Messaging Framework](https://www.w3.org/TR/soap12-part1/)
- [W3C WSDL 2.0 Core Language](https://www.w3.org/TR/wsdl)

🎬 [SOAP Web Services 01 — Introduction To Web Services, Java Brains](https://www.youtube.com/watch?v=mKjvKPlb1rA) (11 min)

- SOAP defines a versioned XML message envelope; WSDL describes operations, messages, bindings, and endpoints.
- Envelope namespaces distinguish SOAP versions and are not decorative.
- Inspect WSDL bindings for concrete wire details rather than guessing from abstract operations.
- Validate SOAP Fault structure as well as HTTP behavior.
- Layer assertions across transport, envelope, body schema, and business outcome.


## Related notes

- [[Notes/api-testing-fundamentals/http-for-testers/json-and-xml|JSON & XML]]
- [[Notes/api-test-automation/contract-and-schema-testing/schema-validation|Schema validation]]
- [[Notes/api-test-automation/contract-and-schema-testing/openapi-as-the-contract|OpenAPI as the contract]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/graphql-and-soap-testing/soap-wsdl-when-you-meet-it.mdx`_
