---
title: "Consumer-driven contracts"
tags: ["api-test-automation", "contract-and-schema-testing", "track-d"]
updated: "2026-07-17"
---

# Consumer-driven contracts

*Consumer-driven contracts capture the interactions clients actually depend on, then replay them against the real provider. Learn Pact's workflow without mistaking mocks for evidence.*

> Two teams can each have 100 percent green tests and still fail the first time their services meet. Separate green dashboards are not a relationship counsellor; the shared interaction is what needs proof.

> **In real life**
>
> A handshake works only because both parties perform compatible halves. The consumer records the hand it expects; provider verification proves the real provider can meet it.

**Consumer-driven contract**: A consumer-driven contract captures concrete requests a consumer makes and the responses it relies on. Consumer tests generate the contract against a mock provider; provider verification replays those interactions against the real provider in controlled states.

## The Pact loop, with no magic smoke

1. The consumer test declares a provider state, request, and expected response.
2. Pact's mock provider checks the consumer really makes that request.
3. The interaction is written to a pact contract and published or shared.
4. Provider verification prepares the named state and replays the request.
5. Deployment checks use verified contract results to decide compatibility.

> **Tip**
>
> Match only what the consumer genuinely relies on. Requiring every provider field freezes harmless evolution and turns contracts into distributed snapshots.

> **Common mistake**
>
> A consumer test passing against its own mock proves only that the consumer agrees with its declared expectation. Provider verification is the missing half that makes the contract evidence.

![Two people shaking hands outdoors](consumer-driven-contracts.jpg)
*Handshake — Cpl. Paula M. Fitzgerald, Wikimedia Commons, public domain US Government work. [Source](https://commons.wikimedia.org/wiki/File:Handshake.jpg)*
- **Consumer side** — One side initiates with a concrete need: the exact interaction its code uses.
- **Provider side** — The other side must verify that its real behavior can satisfy that need.
- **The pact** — Compatibility exists at the shared interaction, not inside either team's isolated dashboard.

**From consumer expectation to deployable evidence**

1. **Consumer test runs against Pact mock** — The client makes a real request to the controlled double.
2. **Pact writes the interaction** — Request, expected response, matching rules, and provider state become a contract.
3. **Contract is shared** — A broker or artifact store makes the consumer's current expectations available.
4. **Provider verification replays it** — The real provider runs in a deterministic state with dependencies stubbed where appropriate.
5. **Compatibility gates deployment** — A version deploys only when its relevant consumer contracts are verified.

*Run it — match only what the consumer needs (Python)*

```python
expected = {"id": "T-7", "status": "open"}
actual = {"id": "T-7", "status": "open", "priority": "high", "internal_note": "new"}

errors = []
for field, expected_value in expected.items():
    if actual.get(field) != expected_value:
        errors.append(f"{field}: expected {expected_value!r}, got {actual.get(field)!r}")

print("PASS: provider satisfies consumer contract" if not errors else "FAIL: " + "; ".join(errors))
print("Provider may add fields the consumer never promised to use.")

# PASS: provider satisfies consumer contract
# Provider may add fields the consumer never promised to use.
```

*Run it — match only what the consumer needs (Java)*

```java
import java.util.*;

public class Main {
  public static void main(String[] args) {
    Map<String, Object> expected = Map.of("id", "T-7", "status", "open");
    Map<String, Object> actual = Map.of("id", "T-7", "status", "open", "priority", "high");
    List<String> errors = new ArrayList<>();
    expected.forEach((field, value) -> {
      if (!Objects.equals(value, actual.get(field)))
        errors.add(field + ": expected " + value + ", got " + actual.get(field));
    });
    System.out.println(errors.isEmpty() ? "PASS: provider satisfies consumer contract" : "FAIL: " + errors);
    System.out.println("Provider may add fields the consumer never promised to use.");
  }
}

/* PASS: provider satisfies consumer contract
   Provider may add fields the consumer never promised to use. */
```

### Your first time: Your mission: model one consumer interaction

- [ ] Choose one real client call — Use a request the consumer actually makes.
- [ ] Declare the minimum expected response — Include only fields and constraints the client reads.
- [ ] Name the provider state — Make preconditions explicit and repeatable.
- [ ] Run both halves — Generate the pact from the consumer, then verify it against the provider.

You now have compatibility evidence instead of two unrelated unit-test trophies.

- **Provider verification cannot recreate data.**
  Implement deterministic provider-state setup; do not depend on whatever staging happens to contain.
- **Adding an optional response field breaks contracts.**
  The consumer over-specified the response. Match only fields and constraints it consumes.
- **The mock test passes but production integration fails.**
  Confirm the pact was published and verified against the exact provider version being deployed.

### Where to check

- Consumer test logs proving the expected request was sent.
- Pact files and matching rules, not screenshots of mock responses.
- Provider-state setup and verification output.
- Broker version tags, branches, environments, and deploy checks.

### Worked example: the harmless provider field that a brittle contract rejected

1. A mobile client reads only `id` and `status`.
2. Its contract snapshots the entire response, including five unused fields.
3. The provider adds optional `priority`; snapshot equality fails.
4. The contract is narrowed to the fields the consumer reads, with type matchers where values vary.
5. The addition passes, while removing `status` still blocks deployment.

**Quiz.** A Pact consumer test passes against the generated mock. What must still happen before claiming provider compatibility?

- [ ] Nothing
- [x] Replay and verify the contract against the real provider in controlled states
- [ ] Run only the UI suite
- [ ] Compare OpenAPI file sizes

*The consumer test creates and exercises its expectation. Provider verification proves the real provider can satisfy it.*

- **Consumer** — The application that makes a request or receives a message and declares what it relies on.
- **Provider verification** — Replay consumer interactions against the real provider in prepared states.
- **Provider state** — Named precondition needed to make an interaction deterministic.

### Challenge

Take one response assertion and delete every field the consumer does not read. Add a harmless provider field and prove the focused contract passes; remove a consumed field and prove it fails.

### Ask the community

> Our Pact interaction for `[consumer -> provider]` currently matches `[fields/rules]`. Which expectations are genuine consumer needs, and which are accidental over-specification?

Share consumer code that reads the response; intent beats a giant pact excerpt.

- [Pact official introduction](https://docs.pact.io/)
- [Pact provider verification — official guide](https://docs.pact.io/implementation_guides/javascript/docs/provider)

🎬 [Contract testing Ask Me Anything — PactFlow](https://www.youtube.com/watch?v=FxrFj7xvQ24) (33 min)

- Consumer tests generate contracts from concrete interactions the client actually uses.
- Provider verification is essential; a mock passing alone is not compatibility proof.
- Provider states make replay deterministic without a fully deployed world.
- Match only consumer needs so harmless provider additions remain compatible.
- Track contract and application versions together before making deployment decisions.


## Related notes

- [[Notes/api-test-automation/contract-and-schema-testing/openapi-as-the-contract|OpenAPI as the contract]]
- [[Notes/api-test-automation/contract-and-schema-testing/breaking-change-detection|Breaking-change detection]]
- [[Notes/api-test-automation/mocking-and-service-virtualization/stubs-mocks-and-fakes|Stubs, mocks & fakes]]


---
_Source: `packages/curriculum/content/notes/api-test-automation/contract-and-schema-testing/consumer-driven-contracts.mdx`_
