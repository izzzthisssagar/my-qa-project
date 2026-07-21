---
title: "Reuse"
tags: ["test-frameworks", "data-driven-testing", "track-d"]
updated: "2026-07-17"
---

# Reuse

*A shared @DataProvider, fixture, or external data file used across multiple test methods and classes - plus the discipline of centralizing test data so updating one shared value doesn't mean hunting through dozens of hardcoded copies.*

> Three test classes each define their own list of "valid test accounts." A fourth class copies the list
> from one of them. Then an account gets deactivated, and updating it means finding and editing four
> separate copies - if anyone remembers all four exist. Everything this chapter has covered - data
> providers, parameterized sources, external files - solves the one-test-many-rows problem. Reuse is
> what happens when you point that same machinery at MANY tests sharing the SAME rows.

> **In real life**
>
> A village well sits at the center, and every household draws from the same source rather than each
> digging its own. One well means one thing to maintain, one water quality to monitor, one place to fix
> when something goes wrong - and when the well is deepened or cleaned, every household benefits at once
> without anyone visiting four separate holes in the ground. The alternative - four households, four
> private wells, four copies of the same maintenance job - is what hardcoding the same test data into
> four different test classes actually costs.

**Reuse**: Reuse, in data-driven testing, means one data provider, one parameterized source, or one external data file is consumed by MULTIPLE test methods or test classes, rather than each test (re)defining its own copy of the same rows. In TestNG this is dataProviderClass - a static @DataProvider method living in a shared class, referenced by @Test(dataProviderClass = Shared.class, dataProvider = 'accounts') from any number of unrelated test classes. In JUnit 5, a static @MethodSource factory can live in a shared utility class and be referenced from multiple test classes via a fully-qualified method reference. In pytest, a fixture or a parametrize data list defined in conftest.py is automatically available to every test in that directory tree. An external CSV or Excel file is inherently shared the moment more than one provider or fixture reads the same path. The discipline underneath all three mechanisms is the same: centralize a piece of test data or its generation logic in exactly one place, so that updating one shared value updates every test that depends on it, instead of requiring a hunt through every hardcoded copy.

## Centralizing what many tests share

```java
public class SharedProviders {
    @DataProvider(name = "activeAccounts")
    public static Object[][] activeAccounts() {
        return new Object[][] {
            { "amina@example.com", "admin" },
            { "ben@example.com", "viewer" },
        };
    }
}

public class LoginTests {
    @Test(dataProviderClass = SharedProviders.class, dataProvider = "activeAccounts")
    public void loginSucceeds(String email, String role) { /* ... */ }
}

public class PermissionsTests {
    @Test(dataProviderClass = SharedProviders.class, dataProvider = "activeAccounts")
    public void roleIsRespected(String email, String role) { /* ... */ }
}
```

```python
# conftest.py - shared across every test file in this directory
import pytest

ACTIVE_ACCOUNTS = [
    ("amina@example.com", "admin"),
    ("ben@example.com", "viewer"),
]

@pytest.fixture
def active_accounts():
    return ACTIVE_ACCOUNTS

# test_login.py and test_permissions.py can both use active_accounts
# without importing anything - pytest discovers conftest.py automatically
```

- **TestNG's `dataProviderClass` is the direct mechanism** - the provider method must be `static`
  because TestNG calls it without constructing an instance of the shared class; any number of
  unrelated `@Test` methods, in any number of classes, can point at the same name plus class.
- **JUnit 5 leans on `@MethodSource` with a fully-qualified reference** -
  `@MethodSource("com.example.SharedData#activeAccounts")` lets a static factory method in one class
  feed parameterized tests in many others.
- **pytest's `conftest.py` is reuse by convention, not by import** - any fixture or constant defined
  there is automatically visible to every test file in that directory and its subdirectories, no
  explicit import required. This is also why an unintentionally broad `conftest.py` change can affect
  tests nobody meant to touch.
- **An external CSV or Excel file is shared the instant two providers read the same path** - no
  special syntax needed, but the file's stability (its header, its meaning) now matters to every
  consumer, not just one.
- **Reuse is a discipline question as much as a syntax question** - the mechanism (dataProviderClass,
  shared MethodSource, conftest.py, a shared file) only pays off if teams actually reach for the
  existing shared source instead of pasting a fifth private copy of "valid test accounts" into a fifth
  test class.

> **Tip**
>
> Before extracting a shared data provider, ask whether the tests reaching for it actually need the SAME
> data, or merely SIMILAR-looking data that happens to overlap today. Two tests both listing "an active
> account" and "an inactive account" might diverge the moment one needs a third state the other doesn't
> care about. Share aggressively when the underlying concept truly is one thing (the current set of
> valid discount codes); keep separate when the overlap is coincidental - a shared source that silently
> grows unrelated columns to satisfy every consumer becomes harder to reason about than four honest,
> separate copies.

> **Common mistake**
>
> Sharing a data provider or fixture across tests that then each mutate the data it returns - one test
> appends a row to a list before asserting, and because the underlying list wasn't a fresh copy per test,
> the next test consuming the "same" provider sees the mutated version. Centralizing WHERE data comes
> from is the goal; centralizing a single MUTABLE instance that tests silently corrupt for each other is
> the opposite of what reuse is supposed to buy. A shared provider should hand back fresh data (or an
> immutable structure) on every call, not a shared reference.

![A village hand-pump well in the Sahel region of Burkina Faso with several women gathered around it carrying basins and buckets, one woman operating the pump, and a cow walking past, illustrating one shared central water source multiple households draw from](reuse.jpg)
*Scene with Women at Village Well, Dori, Sahel Region, Burkina Faso — Wikimedia Commons, CC BY-SA 3.0 (Adam Jones). [Source](https://commons.wikimedia.org/wiki/File:Scene_with_Women_at_Village_Well_-_Dori_-_Sahel_Region_-_Burkina_Faso.jpg)*
- **The pump itself — the shared @DataProvider or fixture** — One mechanism, drawing from one source underneath - the static shared method or conftest.py fixture every consuming test reaches into.
- **One woman drawing water — one test class consuming the shared source** — She doesn't dig her own well; she uses the shared one, exactly like a @Test(dataProviderClass = Shared.class, ...) reaching into a class it doesn't own.
- **Another woman waiting her turn with a basin — a second, independent consumer** — The same source, a completely separate household - the way LoginTests and PermissionsTests both consume activeAccounts without knowing about each other.
- **The cow passing through — an unrelated consumer drawing from the same place** — Not every user of a shared resource is even part of the same 'team' - the same way a shared external CSV can end up read by tooling well outside the original test suite that created it.

**One shared source feeding two unrelated test classes**

1. **SharedProviders.activeAccounts() is defined once, as static** — One place holds the current list of valid test accounts - no test class owns it privately.
2. **LoginTests references it via dataProviderClass** — It never redefines the accounts - it points at the shared method by class and name.
3. **PermissionsTests references the exact same method** — A completely different test class, same shared source - zero duplication between them.
4. **An account is deactivated; the shared method is updated once** — One edit, in one file - not a search-and-replace across every test class that mentions accounts.
5. **Both LoginTests and PermissionsTests pick up the change on their next run** — Neither test file was touched - the shared source was the only thing that changed.

Underneath the framework syntax, reuse is just: put the data (or the function that makes it) in one
place, and let many callers reference that one place instead of each holding their own copy. Here's
that shape as a small, generic simulation.

*Run it - one shared source consumed by two independent test-like functions (Python)*

```python
# the ONE shared source - lives in exactly one place
def active_accounts():
    # returns a FRESH list every call - no shared mutable reference
    return [
        {"email": "amina@example.com", "role": "admin"},
        {"email": "ben@example.com", "role": "viewer"},
    ]

def login_tests():
    print("LoginTests using the shared source:")
    for account in active_accounts():
        print(f"  login({account['email']}) -> PASS")

def permissions_tests():
    print("PermissionsTests using the SAME shared source:")
    for account in active_accounts():
        print(f"  checkRole({account['email']}, {account['role']}) -> PASS")

login_tests()
permissions_tests()
print("One shared source, two unrelated consumers, zero duplicated rows.")
```

Same shared-source shape in Java.

*Run it - one shared source consumed by two independent test-like classes (Java)*

```java
import java.util.*;

public class Main {
    record Account(String email, String role) {}

    // the ONE shared source - static, lives in exactly one place
    static List<Account> activeAccounts() {
        // returns a FRESH list every call - no shared mutable reference
        return List.of(
            new Account("amina@example.com", "admin"),
            new Account("ben@example.com", "viewer")
        );
    }

    static void loginTests() {
        System.out.println("LoginTests using the shared source:");
        for (Account a : activeAccounts()) {
            System.out.println("  login(" + a.email() + ") -> PASS");
        }
    }

    static void permissionsTests() {
        System.out.println("PermissionsTests using the SAME shared source:");
        for (Account a : activeAccounts()) {
            System.out.println("  checkRole(" + a.email() + ", " + a.role() + ") -> PASS");
        }
    }

    public static void main(String[] args) {
        loginTests();
        permissionsTests();
        System.out.println("One shared source, two unrelated consumers, zero duplicated rows.");
    }
}
```

### Your first time: Your mission: extract a shared source and prove two test classes stay in sync

- [ ] Find (or write) two test classes that each hardcode their own near-identical version of the same conceptual data (test accounts, valid discount codes, sample addresses) — Copy-paste deliberately if you need to - this is the exact duplication reuse removes.
- [ ] Extract one shared, static data provider (or a conftest.py fixture) holding that data in exactly one place — TestNG: dataProviderClass. JUnit 5: a shared @MethodSource. pytest: conftest.py.
- [ ] Point both test classes at the shared source and run both — Confirm both still pass, now with zero duplicated rows between them.
- [ ] Change one value in the shared source only, then re-run both test classes — Confirm the change is reflected in BOTH without touching either test file - that's the actual payoff.

You've now built the exact thing this chapter has been building toward: data that many tests trust,
maintained in exactly one place.

- **TestNG complains a dataProviderClass method can't be found or invoked.**
  The shared provider method must be declared static - TestNG invokes it without constructing an instance of the class it lives in, and a non-static method fails at exactly that point.
- **Two test classes sharing a data provider start showing flaky, order-dependent failures.**
  The shared source is likely returning a mutable reference that one test mutates - return fresh data (a new list/array) on every call rather than a cached shared instance.
- **A conftest.py fixture change breaks tests in a directory nobody meant to touch.**
  conftest.py fixtures apply to every test file in that directory tree automatically - before editing a shared fixture, check how many test files actually consume it, not just the one you're working on.
- **A 'shared' data provider has grown five optional columns to satisfy every consumer's slightly different need.**
  This is the tip callout's warning showing up in practice - some of these consumers likely don't need the SAME data, just similar-looking data. Split the source back into what's genuinely shared versus what was forced together.

### Where to check

- **Whether a data provider method is `static`** — the first thing to check when `dataProviderClass`
  (TestNG) or a cross-class `@MethodSource` (JUnit 5) reference fails to resolve.
- **Whether a shared source returns fresh data or a cached mutable reference** — the fastest way to
  diagnose flaky, order-dependent failures across tests that share a data provider or fixture.
- **`conftest.py`'s actual scope** — which directory tree's tests it affects — before changing a
  fixture that looks locally scoped but isn't.
- **How many consumers a shared source actually has** — a quick project-wide search for the provider's
  name or fixture reference before changing its shape, so no consumer is surprised.

### Worked example: four private copies of 'valid test accounts' collapsed into one shared source

1. Four TestNG classes - `LoginTests`, `PermissionsTests`, `AuditLogTests`, `SessionTests` - each
   define their own private `@DataProvider` returning what is meant to be the same list of active test
   accounts, copy-pasted from whichever class was written first.
2. An account used in all four gets deactivated in the staging environment. Updating the data means
   finding and editing four separate `@DataProvider` methods - and `AuditLogTests`' copy is missed,
   because nobody remembered it existed.
3. `AuditLogTests` starts failing intermittently against an account that no longer works, and the team
   spends an afternoon before realizing the account list was never actually shared.
4. The four private providers are collapsed into one `SharedProviders.activeAccounts()`, marked
   `static`, referenced from all four classes via `dataProviderClass`.
5. The next account change is a single edit in one file; all four test classes pick it up on their next
   run with no risk of a missed copy, because there is no longer a copy to miss.

**Quiz.** A team extracts a shared TestNG @DataProvider so that LoginTests and PermissionsTests both consume the same activeAccounts() method. LoginTests starts appending a fake account to the list it receives before running its assertions, and afterward PermissionsTests starts seeing that fake account too. What's the actual cause, according to this note?

- [ ] TestNG runs dataProviderClass methods in a random, unpredictable order
- [ ] PermissionsTests must be caching an old version of the data provider's results
- [x] The shared provider is returning the SAME mutable list reference on every call rather than fresh data, so LoginTests' mutation leaks into what PermissionsTests later receives
- [ ] Sharing a data provider between two classes is not actually supported by dataProviderClass

*The mistake callout describes exactly this failure mode: a shared source that hands back one mutable reference instead of fresh data on every call lets one consumer's mutation leak into another's - the fix is returning new data each call, not caching or sharing an instance. Option one invents random ordering as the cause, which isn't what's described (this is a data-corruption bug, not a timing bug). Option two guesses at caching with no basis in the scenario. Option four is directly contradicted by the whole note - dataProviderClass is precisely the supported sharing mechanism.*

- **What does 'reuse' mean in data-driven testing?** — One data provider, parameterized source, or external file consumed by MULTIPLE test methods/classes, instead of each test defining its own duplicate copy of the same data.
- **TestNG's mechanism for a cross-class shared data provider** — dataProviderClass - the provider method must be static, referenced from any @Test via @Test(dataProviderClass = X.class, dataProvider = "name").
- **pytest's mechanism for automatic sharing** — conftest.py - fixtures and constants defined there are automatically available to every test file in that directory tree, with no explicit import.
- **The core mistake to avoid when sharing a data source** — Returning a shared MUTABLE reference instead of fresh data per call - one consumer's mutation silently leaks into every other consumer of the 'same' source.
- **The village-well analogy for reuse** — One well (shared source) maintained once serves every household (test class) - versus each household digging (hardcoding) its own private, separately-maintained copy.

### Challenge

Find two or more places in a real codebase (yours or an open-source one) where the same conceptual
test data appears to be hardcoded more than once - similar lists of users, addresses, or product
fixtures duplicated across test files. Extract one shared source (a static data provider, a
@MethodSource, or a conftest.py fixture) and point every duplicate at it. Then write one sentence on
what you'd have had to do, file by file, to make the same data change before the extraction - versus
after.

### Ask the community

> I'm trying to share a data provider / fixture across multiple test classes and `[describe the problem: it can't be found / the data seems to change between tests / it's not static]`. Here's how I defined it and how each class references it: `[paste both]`.

Pasting the shared source's definition next to every place that references it is usually enough for
someone to spot a missing static modifier, a name mismatch, or a mutation bug at a glance.

- [TestNG — official docs: Parameters & DataProviders (dataProviderClass)](https://testng.org/parameters.html)
- [pytest — official docs: How to use fixtures (conftest.py sharing)](https://docs.pytest.org/en/stable/how-to/fixtures.html)

🎬 [How to use DataProvider in the TestNG in Selenium | Define & use DataProvider in same or other class — AJ AUTOMATION](https://www.youtube.com/watch?v=Zm-9BrhOPL8) (26 min)

- Reuse means one data provider, parameterized source, or external file is consumed by multiple test methods or classes, instead of each test hardcoding its own duplicate copy.
- TestNG's dataProviderClass and JUnit 5's cross-class @MethodSource both require the shared provider method to be static; pytest's conftest.py shares fixtures automatically across a directory tree.
- A shared source must return fresh data on every call, not a cached mutable reference - otherwise one test's mutation silently leaks into every other consumer.
- Share aggressively when tests genuinely need the SAME data; keep sources separate when the overlap is only coincidental, or the shared source balloons with unrelated columns to satisfy everyone.
- The real payoff of reuse: updating one shared value updates every test that depends on it in one edit, instead of a search-and-replace across every hardcoded copy - and a missed copy is the exact bug this discipline eliminates.


## Related notes

- [[Notes/test-frameworks/data-driven-testing/data-providers|Data providers]]
- [[Notes/test-frameworks/data-driven-testing/parameterized-tests|Parameterized tests]]
- [[Notes/test-frameworks/data-driven-testing/external-data-csv-excel|External data (CSV/Excel)]]


---
_Source: `packages/curriculum/content/notes/test-frameworks/data-driven-testing/reuse.mdx`_
