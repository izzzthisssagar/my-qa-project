---
title: "ER modeling from requirements"
tags: ["relational-databases-engineer-level", "schema-design", "track-e"]
updated: "2026-07-17"
---

# ER modeling from requirements

*Turn requirement nouns, business events, cardinalities, optionality, and lifecycle rules into a conceptual entity-relationship model before choosing tables and datatypes.*

> If the requirement says “a user can belong to many teams” and your diagram has one `team_id` on users, the schema is already arguing with the product before either exists.

> **In real life**
>
> An architectural drawing turns activities and constraints into rooms and connections before anyone pours concrete. ER modeling does that for information.

**ER modeling**: Entity-relationship (ER) modeling is conceptual design that identifies entity types, their attributes, relationships, cardinalities, optionality, and business rules before mapping them to relational tables and constraints.

## Mine rules, not just nouns

For “projects contain tickets; users may watch many tickets; every ticket has exactly one project,”
model `Project`, `Ticket`, `User`, and a many-to-many `Watch` relationship. Ask lifecycle questions:
can a ticket exist before its project, can a user watch twice, and what happens when either is deleted?

> **Tip**
>
> Write every relationship in both directions: “one project has zero-or-many tickets; each ticket belongs to exactly one project.” Ambiguity hates symmetry.

> **Common mistake**
>
> Treating every noun as an entity. “Status” may be an attribute, constrained value, or entity depending on behavior and ownership.

![Architectural perspective drawing of a public building](er-modeling-from-requirements.jpg)
*Public building architectural drawing — Cusack5239, Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:Public_building.jpg)*
- **Entities** — Stable things the requirements need to identify.
- **Relationships** — Business connections and events between entities.
- **Constraints** — Cardinality, optionality, uniqueness, and lifecycle rules.

**Requirements to conceptual model**

1. **Collect scenarios** — Happy paths, refusal paths, lifecycle, and history.
2. **Identify entities** — Things with identity and independent meaning.
3. **Name relationships** — Use verbs and describe both directions.
4. **Set cardinality** — One, optional one, many, and mandatory many.
5. **Validate examples** — Walk real and adversarial scenarios through the model.

*Run it — validate requirement cardinalities (Python)*

```python
requirements = {"ticket_project": (1, 1), "project_tickets": (0, None), "ticket_watchers": (0, None)}
examples = {"ticket_project": 1, "project_tickets": 3, "ticket_watchers": 0}
for name, (minimum, maximum) in requirements.items():
    count = examples[name]
    valid = count >= minimum and (maximum is None or count <= maximum)
    print(f"{name}: {count} -> {'VALID' if valid else 'INVALID'}")

# ticket_project: 1 -> VALID
# project_tickets: 3 -> VALID
# ticket_watchers: 0 -> VALID
```

*Run it — validate requirement cardinalities (Java)*

```java
import java.util.*;
public class Main {
  record Rule(int min,Integer max){}
  public static void main(String[] args){
    Map<String,Rule> rules=new LinkedHashMap<>(); rules.put("ticket_project",new Rule(1,1)); rules.put("project_tickets",new Rule(0,null)); rules.put("ticket_watchers",new Rule(0,null));
    Map<String,Integer> counts=Map.of("ticket_project",1,"project_tickets",3,"ticket_watchers",0);
    rules.forEach((n,r)->{int c=counts.get(n); boolean ok=c>=r.min()&&(r.max()==null||c<=r.max()); System.out.println(n+": "+c+" -> "+(ok?"VALID":"INVALID"));});
  }
}

/* ticket_project: 1 -> VALID
   project_tickets: 3 -> VALID
   ticket_watchers: 0 -> VALID */
```

### Your first time: Your mission: model one workflow

- [ ] Collect five concrete scenarios — Include creation, reassignment, deletion, duplicates, and history.
- [ ] Underline candidate entities and relationship verbs — Reject nouns with no independent identity or behavior.
- [ ] State cardinality and optionality both ways — Use exact minimum and maximum language.
- [ ] Walk counterexamples through the diagram — Ask what invalid states the model must prevent.

- **Stakeholders disagree on cardinality.**
  Use concrete examples and lifecycle events; the disagreement is a requirement gap, not a diagram formatting issue.
- **A relationship needs its own attributes.**
  Promote it to an associative entity, such as Watch with created_at and notification_mode.
- **The model cannot represent history.**
  Separate current state from temporal events or validity periods according to reporting requirements.

### Where to check

- User stories, API contracts, event payloads, and audit requirements.
- Cardinality in both directions and delete/reassignment behavior.
- Examples of invalid states the future schema must reject.

### Worked example: watchers reveal the missing entity

A simple user-ticket line models many-to-many membership. Requirements later demand `watched_at` and notification mode. The relationship becomes a `Watch` entity keyed by user and ticket, with its own attributes and uniqueness rule.

**Quiz.** When should a relationship become an associative entity?

- [ ] Whenever the diagram is large
- [x] When the relationship has attributes or identity of its own
- [ ] Only for one-to-one
- [ ] Never

*A relationship carrying facts such as timestamps or roles needs a place to store and constrain them.*

- **Entity** — A distinguishable thing with independent meaning and identity.
- **Cardinality** — Minimum and maximum relationship participation.
- **Optionality** — Whether zero related instances are allowed.
- **Associative entity** — A modeled relationship with its own attributes or identity.

### Challenge

Model projects, tickets, users, assignees, and watchers from ten written rules, including deletion and duplicate behavior.

### Ask the community

> My ER model assumes `[cardinality]` for `[relationship]`; these two scenarios conflict.

Ask for the missing business rule, not opinions about crow's-foot notation.

- [PostgreSQL — table basics](https://www.postgresql.org/docs/current/ddl-basics.html)
- [PostgreSQL — constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)

🎬 [freeCodeCamp — database design course](https://www.youtube.com/watch?v=ztHopE5Wnpc) (487 min)

- Start with scenarios and business rules, not column types.
- Describe every relationship in both directions with minimum and maximum cardinality.
- Associative entities model many-to-many facts with their own attributes.
- Counterexamples expose missing lifecycle and integrity rules before implementation.


## Related notes

- [[Notes/relational-databases-engineer-level/schema-design/keys-and-relationships|Keys & relationships]]
- [[Notes/relational-databases-engineer-level/schema-design/normalization-1nf-to-3nf|Normalization: 1NF to 3NF]]
- [[Notes/relational-databases-engineer-level/sql-mastery/date-time-and-timezone-handling|Date, time & timezone handling]]


---
_Source: `packages/curriculum/content/notes/relational-databases-engineer-level/schema-design/er-modeling-from-requirements.mdx`_
