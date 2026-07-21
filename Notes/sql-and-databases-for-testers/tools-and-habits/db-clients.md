---
title: "DB clients (DBeaver, TablePlus)"
tags: ["sql-and-databases-for-testers", "tools-and-habits", "track-c"]
updated: "2026-07-18"
---

# DB clients (DBeaver, TablePlus)

*A DB client (DBeaver, TablePlus, pgAdmin) puts connections, a schema browser, a query editor, and one-click export in a single window - so daily QA checks take seconds instead of fighting a raw terminal.*

> You know enough SQL now to verify real data - but where do you actually type it? You could SSH into a
> server and use a bare terminal prompt, retyping every query, squinting at unaligned columns, with no
> memory of what you ran yesterday. Or you could open a database client: a desktop app where connections
> are saved, every table is browsable in a sidebar, results land in a sortable grid, and "export these
> rows for my bug report" is one click. For daily QA work, the client wins - this note shows you why.

> **In real life**
>
> An airliner cockpit. Everything the crew needs is mounted in one place: dozens of labeled gauges on
> the main panel, the throttle levers under one hand, the navigation chart clipped to the desk. Nobody
> climbs out mid-flight to read a dial bolted to the wing. A DB client is that cockpit for a database -
> the schema browser, the query editor, the results grid, and the export button are all instruments on
> one panel, so you check anything in seconds without leaving your seat. A raw terminal is the walk out
> to the wing: possible, but slow, and easy to get wrong under pressure.

**DB clients**: A database client is a desktop application that connects to a database server and gives you a visual workspace over it: saved connections (so you enter credentials once), a schema browser (a sidebar tree of every table and its columns), a query editor (with syntax highlighting, autocomplete, and query history), a results grid (sortable, scrollable, copyable), and exports (CSV, JSON) for sharing results. DBeaver (free, works with almost every database), TablePlus (fast, macOS/Windows), and pgAdmin (PostgreSQL-specific) are the common choices. The client does not replace SQL - you still write the same SELECT statements - it replaces the clumsy surface you would otherwise type them into.

## What a client gives you, piece by piece

- **Saved connections.** Enter host, port, user, and database once; reconnect forever with one click.
  Every saved connection is named, so "staging" and "prod" stop being strings you retype (and mistype).
- **A schema browser.** A sidebar tree of every table, expandable to show columns and types - the
  fastest way to answer "what is this table even called, and does it have a `status` column?" without
  writing a single query.
- **A query editor with history.** Syntax highlighting catches typos before you run them, autocomplete
  fills in table and column names, and every query you have ever run is kept in a history you can
  search and rerun.
- **A results grid and one-click export.** Results come back as a real table you can sort and copy,
  and exporting the exact rows that prove a bug into CSV for your bug report is a right-click, not a
  copy-paste cleanup job.

> **Tip**
>
> Open the schema browser BEFORE writing any query on an unfamiliar database. Two minutes of expanding
> tables and reading column names answers most "how do I even start?" questions - and the client's
> autocomplete then fills in the exact names as you type, so you never guess at spelling again.

> **Common mistake**
>
> Treating the client's editable results grid like a spreadsheet. In many clients, double-clicking a
> cell in the grid EDITS the underlying row - and some clients push that change to the database when you
> save or move away. A tester browsing data has no business editing it. Know your client's edit behavior,
> and pair it with a read-only account (next notes in this chapter) so a stray double-click cannot
> change real data.

![A vintage airliner cockpit with a gauge-covered instrument panel, center throttle levers, crew seats with harnesses, and a navigation chart on a side desk](db-clients.jpg)
*Bristol Britannia cockpit — Ian Dunster, Wikimedia Commons, CC BY-SA 2.0 UK. [Source](https://commons.wikimedia.org/wiki/File:Bristol_Britannia_Cockpit_REJS.jpg)*
- **The main instrument panel - every reading visible at a glance** — Dozens of labeled gauges, all facing the crew, no climbing around the aircraft to check one dial. That is the client's schema browser and results grid: everything the database holds, laid out and readable from one seat.
- **The throttle levers - controls under one hand** — The levers sit on the center pedestal exactly where a hand falls. That is the query editor: the one place you act from, with autocomplete and history putting every past query within reach.
- **The flight engineer's station - a specialized panel for connections and systems** — A whole wall of switches for managing the aircraft's systems. In a client, this is the connection manager: saved, named connections for each environment, configured once and reused every session.
- **The navigation chart on the desk - the map you keep in view** — The crew keeps the chart out while flying. Keep the schema browser open the same way: it is the map of tables and columns that tells you where every query should be pointed.

**One verification check, done in a client - press Play**

1. **Open the saved 'staging' connection** — Credentials were entered once, weeks ago. One click and you are connected to the right database.
2. **Browse the schema tree to find the orders table** — Expand it: id, user_id, status, total. No guessing at column names - they are right there in the sidebar.
3. **Type the query - autocomplete fills in table and column names** — SELECT email, status, total with a JOIN to users, WHERE status = 'paid'. Syntax highlighting catches a typo before you run it.
4. **Results land in a sortable grid** — Two matching rows, columns aligned, sortable by any header. Compare directly against what the app's UI claims.
5. **Export the rows as CSV and attach them to the bug report** — Right-click, export. The exact database evidence, captured in seconds - that is the whole workflow the client buys you.

The whole idea, reduced to one line: a DB client puts the schema, the query, the results, and the
export on one instrument panel - same SQL, far less friction.

*Run it - what a client's three main panels show you, in code (Python)*

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, plan TEXT)")
cur.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, status TEXT, total REAL)")
cur.executemany("INSERT INTO users VALUES (?,?,?)", [
    (1, "mina@example.com", "free"),
    (2, "leo@example.com", "pro"),
    (3, "ana@example.com", "pro"),
])
cur.executemany("INSERT INTO orders VALUES (?,?,?,?)", [
    (101, 2, "paid", 49.0),
    (102, 3, "paid", 49.0),
    (103, 1, "failed", 9.0),
])
conn.commit()

print("--- What a client's schema browser shows you (no query typed) ---")
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
for name in tables:
    cols = [c[1] for c in cur.execute("PRAGMA table_info(" + name + ")")]
    print(" ", name, "->", ", ".join(cols))

print()
print("--- The query editor: same SQL you'd type in DBeaver ---")
for row in cur.execute("SELECT email, status, total FROM orders JOIN users ON users.id = orders.user_id WHERE status = 'paid'"):
    print(" ", row)

print()
print("--- The export button: results as CSV, ready to attach to a bug report ---")
print("email,status,total")
for email, status, total in cur.execute("SELECT email, status, total FROM orders JOIN users ON users.id = orders.user_id ORDER BY orders.id"):
    print(email + "," + status + "," + str(total))

conn.close()
```

Same three panels in Java - the shared code runner here has no live JDBC/SQLite driver on its
classpath (unlike your own machine, where `sqlite-jdbc` works fine locally), so this mirrors the same
schema-browse, query, and export steps in plain Java collections, verified to match the SQLite output
above:

*Run it - the same schema browse, query, and export, without a JDBC driver (Java)*

```java
import java.util.*;

public class Main {
    record User(int id, String email, String plan) {}
    record Order(int id, int userId, String status, double total) {}

    public static void main(String[] args) {
        Map<String, List<String>> schema = new TreeMap<>();
        schema.put("users", List.of("id", "email", "plan"));
        schema.put("orders", List.of("id", "user_id", "status", "total"));

        List<User> users = List.of(
            new User(1, "mina@example.com", "free"),
            new User(2, "leo@example.com", "pro"),
            new User(3, "ana@example.com", "pro")
        );
        List<Order> orders = List.of(
            new Order(101, 2, "paid", 49.0),
            new Order(102, 3, "paid", 49.0),
            new Order(103, 1, "failed", 9.0)
        );
        Map<Integer, User> byId = new HashMap<>();
        for (User u : users) byId.put(u.id(), u);

        System.out.println("--- What a client's schema browser shows you (no query typed) ---");
        for (Map.Entry<String, List<String>> e : schema.entrySet()) {
            System.out.println("  " + e.getKey() + " -> " + String.join(", ", e.getValue()));
        }

        System.out.println();
        System.out.println("--- The query editor: same JOIN + WHERE logic as the SQL version ---");
        for (Order o : orders) {
            if (o.status().equals("paid")) {
                User u = byId.get(o.userId());
                System.out.println("  " + u.email() + " | " + o.status() + " | " + o.total());
            }
        }

        System.out.println();
        System.out.println("--- The export button: results as CSV, ready to attach to a bug report ---");
        System.out.println("email,status,total");
        for (Order o : orders) {
            User u = byId.get(o.userId());
            System.out.println(u.email() + "," + o.status() + "," + o.total());
        }
    }
}
```

### Your first time: Your mission: install a client and browse a real schema

- [ ] Install DBeaver Community Edition (free) or TablePlus — DBeaver works on every OS and talks to nearly every database - it is the safe default choice.
- [ ] Create a connection to any database you can reach - even a local SQLite file works — DBeaver can create a sample SQLite database for you if you have nothing to connect to yet.
- [ ] Expand the schema browser and read every table's columns before writing anything — Answer 'what tables exist and what shape are they?' purely by clicking - zero queries.
- [ ] Run one SELECT in the editor, sort the results grid by a column, then export the rows as CSV — That is the full daily QA loop: find the table, ask the question, capture the evidence.

You have now done the complete client workflow - connect, browse, query, export - which is the same
four moves you will use for real verification on every project from here on.

- **The client connects, but the schema browser shows no tables (or far fewer than the app clearly uses).**
  You are almost certainly looking at the wrong database or schema on that server. One server hosts many databases, and each database can hold several schemas - check which database the connection settings name, and expand other schemas in the tree before assuming the data is missing.
- **A query that worked yesterday now errors with 'table not found', even though the table is visible in the sidebar.**
  Check which connection and database the EDITOR tab is bound to - clients bind each editor tab to one connection, and a tab opened against 'local' will not see tables that live on 'staging'. Most clients show the active connection in the editor's toolbar; switch it there rather than retyping the query.

### Where to check

- **The editor tab's active connection dropdown** — every query runs against the connection that TAB is bound to, not whichever connection you clicked last in the sidebar.
- **The schema browser's column list, before you write a WHERE clause** — exact table and column names beat guessed ones, and autocomplete reads from the same list.
- **[[sql-and-databases-for-testers/tools-and-habits/connecting-safely]]** — the next note: what those host/port/user fields in the connection dialog actually mean, and how to be sure which environment you just connected to.
- **[[sql-and-databases-for-testers/tools-and-habits/read-only-discipline]]** — why the account you put into that connection dialog should not be allowed to write anything.

### Worked example: the missing-table mystery that was really a wrong-database mystery

1. A tester installs DBeaver, connects to the team's PostgreSQL server, and goes looking for the
   `orders` table to verify a checkout bug. The schema browser shows a handful of tables - none of
   them `orders`.
2. First guess: maybe the table was renamed, or the tester lacks permission to see it. A message to
   the team lead is half-typed.
3. Then the tester expands the connection tree one level higher and sees the server hosts FOUR
   databases: `postgres`, `app_dev`, `app_staging`, and `analytics`. The connection had defaulted to
   `postgres` - the server's near-empty default database.
4. Reconnecting with the database field set to `app_staging`, the full schema appears instantly,
   `orders` included, and the checkout verification takes two minutes.
5. Finding: a client faithfully shows you whatever the connection points at. "The table is missing"
   usually means "I am looking at the wrong database" - check the connection's database name before
   assuming anything about the data.

**Quiz.** A tester's SELECT works in one editor tab but fails with 'table not found' in another tab of the same client. The table is clearly visible in the sidebar. What is the most likely cause?

- [ ] The second tab has a syntax error the tester cannot see
- [ ] The database dropped the table between the two runs
- [x] Each editor tab is bound to its own connection, and the failing tab is pointed at a different connection or database than the one holding the table
- [ ] The client needs to be reinstalled because its cache is corrupted

*Clients bind every editor tab to one active connection, and tabs can point at different connections or databases at the same time - so an identical query can succeed in one tab and fail in another. That is exactly the WhenItBreaks case in this note: check the tab's active connection in its toolbar. A syntax error (option one) would produce a syntax error message, not 'table not found'. A table silently vanishing between runs (option two) is wildly unlikely and would also break the working tab. Reinstalling the client (option four) is the classic overreaction to what is actually a one-dropdown fix.*

- **A DB client, in one line** — A desktop app that wraps a database in saved connections, a schema browser, a query editor with history, a results grid, and one-click export - same SQL, better surface.
- **The cockpit analogy** — Everything on one instrument panel: schema browser and grid are the gauges, the query editor is the throttle under your hand, saved connections are the engineer's station - no climbing out to the wing (raw terminal) mid-flight.
- **Name three common DB clients** — DBeaver (free, connects to almost everything), TablePlus (fast, polished), pgAdmin (PostgreSQL-specific).
- **First move on an unfamiliar database** — Open the schema browser and read table and column names before writing any query - the sidebar answers 'what exists here?' with zero SQL.
- **The editable-grid trap** — Double-clicking a results cell can EDIT the real row in many clients - know your client's edit behavior and use a read-only account so browsing can never turn into writing.

### Challenge

Install DBeaver or TablePlus and connect it to any database you can reach (a local SQLite file
counts). Using ONLY the schema browser - no queries - write down every table name and the columns of
the two most interesting tables. Then run one SELECT with a WHERE clause, sort the results grid by
clicking a column header, and export the result as CSV. Time the whole thing: the point of this
chapter is that it should take minutes.

### Ask the community

> I'm a manual tester starting to verify data directly. The developers all use terminal tools like psql, but I find a GUI client easier. Is using DBeaver instead of the terminal considered less professional, or does it matter at all?

Useful replies usually point out that the SQL is identical either way and clients like DBeaver are
standard professional tooling on QA and data teams alike - what matters is knowing which environment
you are connected to and keeping your access read-only, not which window you type the query in.

- [DBeaver — Official Documentation](https://dbeaver.com/docs/dbeaver/)
- [TablePlus — Documentation](https://docs.tableplus.com/)
- [Database Star — DBeaver Tutorial - How to Use DBeaver (SQL Editor)](https://www.youtube.com/watch?v=LEx96-CkB1Q)

🎬 [Database Star — DBeaver Tutorial - How to Use DBeaver (SQL Editor)](https://www.youtube.com/watch?v=LEx96-CkB1Q) (16 min)

- A DB client (DBeaver, TablePlus, pgAdmin) wraps the same SQL you already know in saved connections, a schema browser, a query editor with history, and one-click export.
- For daily QA verification the client beats a raw terminal on speed and safety: no retyped credentials, no guessed column names, no hand-formatting results for bug reports.
- Browse the schema tree before writing queries on any unfamiliar database - the sidebar answers 'what exists here?' faster than any query.
- Every editor tab is bound to one connection - 'table not found' and 'no tables visible' almost always mean the tab or connection points at the wrong database.
- The results grid can edit real rows in many clients - pair the client with a read-only account so browsing can never accidentally become writing.


## Related notes

- [[Notes/sql-and-databases-for-testers/tools-and-habits/connecting-safely|Connecting safely]]
- [[Notes/sql-and-databases-for-testers/tools-and-habits/read-only-discipline|Read-only discipline]]
- [[Notes/sql-and-databases-for-testers/reading-data/select-and-where|SELECT & WHERE]]


---
_Source: `packages/curriculum/content/notes/sql-and-databases-for-testers/tools-and-habits/db-clients.mdx`_
