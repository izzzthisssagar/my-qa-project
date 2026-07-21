---
title: "Parameterized endpoint tests"
tags: ["api-test-automation", "python-api-testing", "track-d"]
updated: "2026-07-17"
---

# Parameterized endpoint tests

*Use pytest.mark.parametrize to turn a table of endpoint cases into separately reported tests with readable IDs, without smuggling several unrelated failures through one loop.*

> Copy-pasted tests are a spreadsheet wearing Python syntax. Parameterization keeps the table and fires the photocopier.

> **In real life**
>
> A caliper checks many parts against their own expected dimensions. The measuring procedure stays fixed; the part and acceptable result change per row.

**parameterization**: pytest parameterization generates a distinct test invocation for each supplied parameter set. @pytest.mark.parametrize names arguments, supplies rows, and can assign IDs that appear in collection and failure reports.

## One behavior, many meaningful rows

```python
@pytest.mark.parametrize(
    "path, expected",
    [
        pytest.param("/health", 200, id="health-public"),
        pytest.param("/v1/tickets/missing", 404, id="ticket-not-found"),
    ],
)
def test_get_status(api, path, expected):
    response = api.get(path)
    assert response.status_code == expected
```

Parameterize variations of one behavior. If rows require completely different setup or assertions,
they are different tests and deserve different names.

> **Tip**
>
> Give rows semantic IDs. `ticket-not-found` is useful in CI; `case1-404` is a cry for help.

> **Common mistake**
>
> Passing mutable dictionaries and modifying them in the test. pytest passes parameter values as-is; mutations can affect later cases.

![Vernier caliper on a work surface](parameterized-endpoint-tests.jpg)
*Vernier caliper 2016 — Santeri Viinamäki, Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Vernier_caliper_2016.jpg)*
- **Test function** — One consistent measuring procedure.
- **Parameter row** — Each endpoint and expectation is a separate specimen.
- **Test ID** — The report names which exact specimen failed.

**From case table to report**

1. **Define argument names** — Columns describe the changing inputs and expectations.
2. **Add focused rows** — Each row represents the same behavior.
3. **Assign readable IDs** — Collection and CI reports identify cases semantically.
4. **pytest generates tests** — Each row passes or fails independently.

*Run it — a tiny generated endpoint matrix (Python)*

```python
cases = [
    ("health-public", "/health", 200, 200),
    ("ticket-not-found", "/v1/tickets/missing", 404, 404),
    ("private-missing-auth", "/v1/me", 401, 401),
]
for case_id, path, expected, actual in cases:
    print(f"{case_id}: {path} -> {'PASS' if actual == expected else 'FAIL'}")

# health-public: /health -> PASS
# ticket-not-found: /v1/tickets/missing -> PASS
# private-missing-auth: /v1/me -> PASS
```

*Run it — a tiny generated endpoint matrix (Java)*

```java
public class Main {
  record Case(String id, String path, int expected, int actual) {}
  public static void main(String[] args) {
    Case[] cases = {
      new Case("health-public", "/health", 200, 200),
      new Case("ticket-not-found", "/v1/tickets/missing", 404, 404),
      new Case("private-missing-auth", "/v1/me", 401, 401)
    };
    for (Case c : cases) System.out.println(c.id() + ": " + c.path() + " -> " + (c.actual() == c.expected() ? "PASS" : "FAIL"));
  }
}

/* health-public: /health -> PASS
   ticket-not-found: /v1/tickets/missing -> PASS
   private-missing-auth: /v1/me -> PASS */
```

### Your first time: Your mission: replace repetition with a case table

- [ ] Find three copied endpoint status tests — Confirm they exercise the same behavior and assertions.
- [ ] Extract only changing values into columns — Keep setup and assertion logic in the test body.
- [ ] Add a semantic id to every row — Run pytest --collect-only to inspect generated names.
- [ ] Break one row — Confirm only that parameter instance fails and is easy to select.

- **Failure name is unreadable.**
  Use explicit ids or pytest.param(..., id=...) based on behavior.
- **Later cases inherit mutated input.**
  Treat parameter objects as immutable or create fresh copies in fixtures/test setup.
- **The test body is full of if statements.**
  Split different behaviors into separately named tests instead of parameterizing unlike cases.

### Where to check

- `pytest --collect-only` for generated IDs.
- The failed node ID for the exact row.
- Parameter tables for shared mutable values.
- Whether every row truly uses the same setup and assertion logic.

### Worked example: one endpoint row fails without hiding two passes

Three GET cases run independently. `/v1/me` unexpectedly returns `403` instead of `401`; pytest reports only `test_get_status[private-missing-auth]` failed. The health and not-found cases remain visible passes, unlike a manual loop that stops at the first assertion.

**Quiz.** Why give parameter rows explicit IDs?

- [ ] They make HTTP faster
- [x] They make collection, selection, and failure reports identify behavior
- [ ] They copy input values
- [ ] pytest requires them

*IDs are optional but turn generated node names into useful diagnostic labels.*

- **Parametrized invocation** — A separately collected test instance for one parameter row.
- **Good test ID** — A short behavior label such as ticket-not-found.
- **Mutation warning** — pytest passes parameter values as-is; mutable values are not copied.
- **Split instead of parameterize** — When cases need different setup, actions, or assertions.

### Challenge

Build a five-row negative status matrix with readable IDs, then select and run one row by its node ID.

### Ask the community

> Should these endpoint cases be one parametrized test or separate tests? Here are the rows and shared assertion logic: `[sanitized table]`

Call out any row needing different setup or meaning; that is the split signal.

- [pytest — official parametrization guide](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [pytest — official parametrization examples and IDs](https://docs.pytest.org/en/stable/example/parametrize.html)

🎬 [Alexander Sergeenko — parameterized test concepts](https://www.youtube.com/watch?v=_b9LYhzzdHg) (10 min)

- Parameterization generates a separate test instance for every data row.
- Use it when setup, action, and assertion logic stay the same.
- Semantic IDs make generated failures selectable and readable.
- Treat mutable parameter values carefully because pytest does not copy them.


## Related notes

- [[Notes/api-test-automation/python-api-testing/fixtures-for-apis|Fixtures for APIs]]
- [[Notes/api-test-automation/python-api-testing/sessions-and-auth|Sessions & auth]]
- [[Notes/test-frameworks/data-driven-testing/parameterized-tests|Parameterized tests]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/python-api-testing/parameterized-endpoint-tests.mdx`_
