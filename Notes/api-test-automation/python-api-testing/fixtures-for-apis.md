---
title: "Fixtures for APIs"
tags: ["api-test-automation", "python-api-testing", "track-d"]
updated: "2026-07-17"
---

# Fixtures for APIs

*pytest fixtures provide named setup, dependency injection, scope, and teardown for API tests; use them to share clients and disposable data without turning test order into a hidden contract.*

> A fixture is not a cupboard where every test dumps state. It is a named promise: here is the setup you asked for, and here is how I will clean it up even when your assertion throws a tantrum.

> **In real life**
>
> Test tubes are prepared for specific experiments, labeled, handed to the procedure, and cleaned or discarded afterward. Fixtures do the same for clients, users, tickets, and tokens.

**fixture**: A pytest fixture is a function marked with @pytest.fixture whose returned or yielded value is injected into tests that request it by name. Scope controls reuse; code after yield performs teardown.

## Compose small, visible dependencies

```python
@pytest.fixture
def api(base_url):
    with requests.Session() as session:
        session.headers.update({"Accept": "application/json"})
        yield ApiClient(base_url, session)

@pytest.fixture
def ticket(api):
    created = api.create_ticket({"title": "Fixture ticket"})
    yield created
    api.delete_ticket(created["id"])
```

Function scope is the default and safest for mutable test data. Broader scopes reduce setup cost but
increase sharing, so use them for immutable configuration or carefully managed clients.

> **Tip**
>
> Let fixtures depend on fixtures. A `ticket` can request `api`; the test then asks only for the behavior-level object it needs.

> **Common mistake**
>
> Making every fixture `autouse=True`. Invisible setup spreads faster than gossip and is harder to debug.

![Rows of test tubes in a laboratory rack](fixtures-for-apis.jpg)
*Test tubes in a laboratory — Sarka Na kopci, Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Test_tubes_in_a_laboratory.jpg)*
- **Named fixture** — Each prepared dependency has a clear purpose.
- **Scope** — The rack determines which experiments share preparation.
- **Teardown** — Cleanup follows use even when the experiment fails.

**A yield fixture's lifecycle**

1. **Test requests fixture** — The argument name makes dependency visible.
2. **Dependencies set up** — pytest resolves the fixture graph.
3. **Fixture yields value** — The test receives client or data.
4. **Test runs** — Assertions pass or fail.
5. **Teardown executes** — Code after yield cleans up regardless of test outcome.

*Run it — setup, use, teardown order (Python)*

```python
events = []
def fixture():
    events.append("setup client")
    yield {"base_url": "http://test"}
    events.append("close client")

gen = fixture()
client = next(gen)
events.append(f"test uses {client['base_url']}")
try: next(gen)
except StopIteration: pass
print(" -> ".join(events))

# setup client -> test uses http://test -> close client
```

*Run it — setup, use, teardown order (Java)*

```java
public class Main {
  static class Client implements AutoCloseable {
    Client() { System.out.println("setup client"); }
    void use() { System.out.println("test uses http://test"); }
    public void close() { System.out.println("close client"); }
  }
  public static void main(String[] args) {
    try (Client client = new Client()) { client.use(); }
  }
}

/* setup client
   test uses http://test
   close client */
```

### Your first time: Your mission: extract setup without hiding intent

- [ ] Extract base_url as a fixture — Keep environment selection in one visible place.
- [ ] Create a function-scoped Session fixture — Use yield and close it in teardown.
- [ ] Create one disposable resource fixture — Yield the created object and delete it afterward.
- [ ] Force the test assertion to fail — Confirm teardown still executes and the resource is gone.

- **Fixture not found.**
  Check spelling and visibility: local module, conftest.py directory ancestry, or installed plugin.
- **Cleanup never runs.**
  Use yield correctly and place teardown after it; avoid returning before cleanup is registered.
- **Tests pass alone but fail together.**
  Reduce scope for mutable data and remove shared state or order dependencies.

### Where to check

- `pytest --fixtures` for available fixtures and source locations.
- `pytest --setup-show` for setup/teardown order.
- Fixture scope and mutable objects shared across tests.
- Cleanup response status and service state after forced failure.

### Worked example: cleanup survives an assertion failure

A `ticket` fixture creates `T-42`, yields it, and the test fails on title validation. pytest still resumes the fixture after `yield` and deletes `T-42`. The next test starts clean instead of inheriting yesterday's corpse.

**Quiz.** What happens to code after yield in a pytest fixture?

- [ ] It is ignored
- [x] It runs as teardown regardless of the test outcome
- [ ] It runs before the test
- [ ] It runs only on success

*pytest's fixture reference specifies that post-yield code is teardown and runs regardless of test outcome.*

- **Default fixture scope** — Function: a fresh instance for each requesting test.
- **yield fixture** — Setup before yield, injected value at yield, teardown after yield.
- **Fixture dependency** — A fixture requests another fixture by naming it as an argument.
- **Autouse risk** — Setup becomes invisible to tests and can create surprising global behavior.

### Challenge

Build fixtures for a Session and disposable ticket, then prove cleanup runs after both a pass and a deliberate failure.

### Ask the community

> My fixture `[name]` has scope `[scope]` and leaks `[state]` between tests; here is setup/teardown output.

Show the fixture dependency graph and order, with credentials removed.

- [pytest — official fixtures guide](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [pytest — official fixture reference](https://docs.pytest.org/en/stable/reference/reference.html#pytest-fixture)

🎬 [Super SQA — mastering pytest fixtures](https://www.youtube.com/watch?v=mlqlrH2p114) (18 min)

- Fixtures are explicit named dependencies injected into tests.
- Function scope is the safe default for mutable API data.
- Code after yield performs teardown even when the test fails.
- Fixture composition is useful; invisible autouse state needs restraint.


## Related notes

- [[Notes/api-test-automation/python-api-testing/requests-and-pytest|Requests + pytest]]
- [[Notes/api-test-automation/python-api-testing/parameterized-endpoint-tests|Parameterized endpoint tests]]
- [[Notes/test-frameworks/lifecycle-and-annotations/pytest-fixtures|pytest fixtures]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/python-api-testing/fixtures-for-apis.mdx`_
