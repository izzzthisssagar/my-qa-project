---
title: "Queries, mutations, and schema"
tags: ["api-test-automation", "graphql-and-soap-testing", "track-d"]
updated: "2026-07-17"
---

# Queries, mutations, and schema

*GraphQL's schema is the map; queries read and mutations request side effects. Learn variables, nullability, operation names, and selection-driven assertions without string-concatenation chaos.*

> An unnamed GraphQL operation assembled by string concatenation is the API-test equivalent of mailing a form written in pencil, with the answer boxes moved halfway through. It may arrive. Nobody should build a suite around that hope.

> **In real life**
>
> A questionnaire separates the printed questions from the respondent's answers. A named operation is the stable form; variables are the answers supplied separately.

**GraphQL operation and schema**: A GraphQL schema defines object, scalar, enum, interface, union, input-object, and root operation types plus their fields and arguments. Queries read through the query root; mutations request writes or side effects through the mutation root and must include a selection set for returned object fields.

## Read the type signature before writing the test

- `ID!` means a non-null ID input; `String` is nullable.
- Use named operations for tracing and diagnostics.
- Declare variables in the operation signature and send values separately.
- A query selects fields; a mutation also selects the result fields you want returned.
- Aliases rename response keys; fragments reuse selection sets; `__typename` identifies concrete union/interface results.

> **Tip**
>
> Keep operation documents static and vary the JSON variables. This lets GraphQL validate syntax and types before execution and keeps test reports readable.

> **Common mistake**
>
> Interpolating untrusted values into operation text. Variables exist specifically to separate dynamic values from the document and its type declarations.

![A photographed paper questionnaire containing printed questions and handwritten answers](queries-mutations-and-schema.jpg)
*Questionnaire — tup wanders, Wikimedia Commons, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Questionnaire.jpg)*
- **Printed structure** — The static named operation declares variables and a selection shape.
- **Supplied answers** — Variables carry changing values separately from the operation document.
- **Required boxes** — Non-null markers and input types let validation reject invalid requests before execution.

**A mutation from schema to assertion**

1. **Inspect the mutation field signature** — Read argument types, required markers, payload type, and possible errors.
2. **Write a named static operation** — Declare variable types and select only result fields the test needs.
3. **Send variables separately** — Let the server coerce and validate typed inputs.
4. **Inspect data and errors** — Distinguish request validation errors from field execution errors.
5. **Verify the side effect** — Query the changed entity or observe the externally visible outcome.

*Run it — validate operation variables (Python)*

```python
variable_spec = {"id": {"type": str, "required": True}, "status": {"type": str, "required": True}}
variables = {"id": "T-7", "status": None}

errors = []
for name, rule in variable_spec.items():
    value = variables.get(name)
    if rule["required"] and value is None:
        errors.append(f"${name}: non-null variable was null")
    elif value is not None and not isinstance(value, rule["type"]):
        errors.append(f"${name}: wrong type")

print("VALID" if not errors else "INVALID: " + "; ".join(errors))

# INVALID: $status: non-null variable was null
```

*Run it — select only requested mutation fields (Java)*

```java
import java.util.*;

public class Main {
  public static void main(String[] args) {
    Set<String> selection = new LinkedHashSet<>(List.of("id", "status"));
    Map<String, Object> resolverResult = new LinkedHashMap<>();
    resolverResult.put("id", "T-7"); resolverResult.put("status", "done"); resolverResult.put("internalNote", "hidden");
    Map<String, Object> response = new LinkedHashMap<>();
    selection.forEach(field -> response.put(field, resolverResult.get(field)));
    System.out.println(response);
    System.out.println("internalNote returned: " + response.containsKey("internalNote"));
  }
}

/* {id=T-7, status=done}
   internalNote returned: false */
```

### Your first time: Your mission: automate one named mutation

- [ ] Inspect the mutation in the schema — Write down input type, required arguments, and payload type.
- [ ] Create a named operation — Declare variables and a minimal result selection.
- [ ] Run valid and null-required cases — Observe validation before resolver execution.
- [ ] Query the entity afterward — A returned payload alone may not prove the side effect persisted.

You have tested the type boundary and the resulting state, not just the response's optimism.

- **Server says a variable was not provided.**
  Match the JSON variable key to the declared dollar-name and ensure its declared type is compatible with the argument.
- **Mutation returns data but nothing changed.**
  Add a follow-up query or observable side-effect assertion; payload shape is not persistence proof.
- **A union result lacks expected fields.**
  Select __typename and use inline fragments for fields available only on concrete types.

### Where to check

- Schema signatures and non-null markers.
- Named operation, variable definitions, and JSON variables object.
- Response `data`, `errors`, `locations`, and `path`.
- Follow-up state or external side effects after mutations.

### Worked example: the mutation that returned success but saved nothing

1. `UpdateTicket` accepts `id: ID!` and `status: Status!` and returns a ticket payload.
2. The test sends variables and receives `{id: T-7, status: DONE}` with no errors.
3. A resolver bug returns the proposed object before persistence fails.
4. A follow-up `TicketById` query still reports `OPEN`.
5. The test correctly fails on state, proving why payload validation and side-effect verification are separate.

**Quiz.** Why should dynamic GraphQL inputs be sent as variables instead of interpolated into operation text?

- [ ] Variables make HTTP unnecessary
- [x] They separate values from the static typed document and allow proper coercion and validation
- [ ] They bypass authorization
- [ ] They make every field non-null

*Variables are declared with GraphQL types and supplied separately, avoiding fragile string construction while enabling validation and coercion.*

- **Non-null marker** — An exclamation mark means null is not a valid value at that type position.
- **Operation name** — Stable name used for tracing, logs, reports, and selecting among multiple operations.
- **Mutation proof** — Validate the payload and independently verify the requested side effect.

### Challenge

Write one named query and one named mutation using the same ID variable. Add a null-variable negative case and a follow-up query proving the mutation persisted.

### Ask the community

> My operation `[name]` declares `[variables]` against schema field `[signature]`, but receives `[error]`. Is the mismatch in variable type, nullability, or selection?

Include the schema signature, operation, variables JSON, and full error path.

- [GraphQL Foundation — Queries and variables](https://graphql.org/learn/queries/)
- [GraphQL Foundation — Mutations](https://graphql.org/learn/mutations/)

🎬 [Modern GraphQL Crash Course — Laiture](https://www.youtube.com/watch?v=qux4-yWeZvo) (210 min)

- The schema defines operations, arguments, result fields, types, and nullability.
- Queries read; mutations request side effects and still require result selections.
- Named static operations plus separate variables improve validation, tracing, and safety.
- Use __typename and fragments for interface or union results.
- Verify mutation side effects independently from the returned payload.


## Related notes

- [[Notes/api-test-automation/graphql-and-soap-testing/graphql-vs-rest|How GraphQL differs from REST]]
- [[Notes/api-test-automation/graphql-and-soap-testing/testing-a-graphql-api|Testing a GraphQL API]]
- [[Notes/api-test-automation/contract-and-schema-testing/schema-validation|Schema validation]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/graphql-and-soap-testing/queries-mutations-and-schema.mdx`_
