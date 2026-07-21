---
title: "Async & loading, gently"
tags: ["web-platform", "javascript", "async", "track-a"]
updated: "2026-07-10"
---

# Async & loading, gently

*JavaScript does one thing at a time, yet somehow waits for a server without freezing. Understanding that trick explains every flaky test, every race condition, and every spinner that never stops.*

> Here is the fact that breaks everyone's mental model: **JavaScript runs on one thread.**
> One thing at a time. No parallelism. And yet a page can wait three seconds for a server
> while you keep scrolling, typing and clicking. That's not a contradiction — it's the
> most important trick in the language, and misunderstanding it is the direct cause of
> every flaky test you will ever write. So let's not misunderstand it.

> **In real life**
>
> JavaScript is **one waiter in a restaurant, not one waiter per table.** The waiter takes
> your order and walks it to the kitchen. He does *not* stand there watching the food
> cook — that would freeze the whole restaurant. He goes and serves other tables. When
> your food is ready, the kitchen rings a bell, and the waiter comes back **when he
> finishes what he's currently doing.** One waiter. Never idle. Never two things at once.
> That last sentence is where the bugs live.

## Sync, async, and the queue

**Synchronous** code runs immediately, top to bottom, blocking everything. **Asynchronous**
code says "start this, tell me when it's done, and meanwhile carry on."

When you call `fetch('/api/orders')`, the browser hands the request to the network and
JavaScript **keeps going**. Later, when the response arrives, the callback is put on a
queue, and the **event loop**: The loop that runs JavaScript: finish the current job completely, then take the next finished callback off the queue and run that to completion. It is why a slow function freezes the whole page, and why an arriving response can never interrupt code that is already running. only picks it up once the
currently-executing code finishes. Never during.

That's the whole model:

1. Run the current code to completion. Nothing can interrupt it.
2. Then take the next finished thing off the queue and run *that* to completion.
3. Repeat forever.

![JavaScript source code showing function calls](javascript-code.png)
*JavaScript source code — Wikimedia Commons, CC0. [Source](https://commons.wikimedia.org/wiki/File:SampleJavaScriptCode.png)*
- **A function runs to completion. Always.** — Nothing interrupts a running function — no timer, no arriving response, no click. They all wait in a queue. This is why a slow loop freezes the entire page: the waiter is stuck at one table and every bell in the kitchen is ringing unanswered.
- **`await` — pause here, let others go** — The magic word. It means 'suspend this function, hand control back, and resume when the result arrives'. The page stays responsive because the waiter walked away rather than standing at the kitchen door. Everything after an `await` runs LATER, at a time you did not choose.
- **A callback is a note left for later** — 'When this finishes, run that.' The `that` doesn't run now. It goes on the queue. Half of async confusion is expecting the next line to have the answer, when the answer arrives a thousand lines of unrelated work later.
- **Timers are the same shape** — `setTimeout(f, 0)` does NOT run f immediately. It queues f to run after the current code finishes — even with a zero delay. That surprises everyone once, and then explains a hundred things.
- **Race conditions are born here** — Two async operations, no guaranteed order. Whichever finishes first wins. Run the same code twice and you may get two different outcomes. If a test depends on the order, it will be flaky forever, and no amount of retrying will fix the cause.

**Why your test failed, and passed when you ran it again — press Play**

1. **🖱 The test clicks 'Load orders'** — JavaScript calls `fetch('/api/orders')`, hands the request off to the network layer, and immediately continues. It does not wait. The DOM is untouched. The order list is still empty.
2. **🔎 The test immediately looks for a row** — Milliseconds have passed. The server is one ocean away (Module 3: 187ms). The response has not arrived, the callback has not queued, the DOM has no rows. The test asserts, finds nothing, and fails.
3. **📥 The response arrives — too late** — 180ms after the click, the network layer finishes and queues the callback. JavaScript picks it up, builds the rows, inserts them into the DOM. The page is now correct. The test failed 170ms ago and has already moved on.
4. **🎲 Run it again on a fast day** — This time the API responds in 30ms (warm cache, closer server, quieter network). The rows exist before the test looks. The test PASSES. Nothing about the code changed — only the timing did. Congratulations: you own a flaky test.
5. **✅ The fix is not `sleep(2)`** — Waiting a fixed time makes the suite slow AND still flaky (some days take 3 seconds). Instead, WAIT FOR THE CONDITION: 'wait until a row exists'. Playwright's `expect(locator).toBeVisible()` does exactly this, retrying until it's true or the timeout expires. State, not stopwatch.

*Try it — one thread, one queue, and the order that surprises everyone*

```python
# JavaScript's event loop, modelled. Sync code runs now; async goes on a queue.
queue = []
output = []

def log(msg):          output.append(msg)
def set_timeout(fn, _ms):  queue.append(fn)      # timers ALWAYS queue, even at 0ms
def fetch(url, on_done):   queue.append(lambda: on_done(f"data from {url}"))

# ---- the code, read top to bottom ----
log("1. script starts")
set_timeout(lambda: log("4. timer callback (queued, ran later)"), 0)
fetch("/api/orders", lambda data: log(f"5. fetch callback: {data}"))
log("2. script ends")
# --------------------------------------

log("3. --- current code finished; NOW the queue drains ---")
while queue:
    queue.pop(0)()          # each queued job runs to completion, one at a time

for line in output: print(line)
print()
print("Read the numbers. The timer had a 0ms delay and STILL ran after")
print("'script ends'. Nothing on the queue can interrupt running code.")
print()
print("Now the test bug, in one line:")
print("  click() -> fetch starts -> assert(row exists)   <- row is queued, not built")
print("The assert ran while the callback was still sitting in that queue.")
```

## Promises, `async`/`await`, and the three states

A **promise** is an IOU for a value that doesn't exist yet. It has exactly three states:

- **pending** — still waiting (your spinner is spinning)
- **fulfilled** — the value arrived
- **rejected** — it failed

`await` unwraps the IOU: "pause this function until the promise settles." A rejected
promise with nothing to catch it produces `Uncaught (in promise)` in the console — one
of the most-ignored red messages in the browser, and frequently the reason a spinner
spins forever.

> **Tip**
>
> The single most valuable testing habit from this note: **never wait for time, always wait
> for state.** `sleep(2000)` is a bet that the server will be fast today. It makes your
> suite slow on good days and flaky on bad ones — the worst of both. `await
> expect(page.getByRole('row')).toBeVisible()` asks the actual question, retries until the
> answer is yes, and fails fast with a useful message when it never becomes yes. Every
> serious automation framework is built around this idea, and Track C will assume you
> already believe it.

### Your first time: Your mission: feel the single thread

- [ ] Prove setTimeout(0) is not immediate — Run: `setTimeout(() => console.log('B'), 0); console.log('A')`. It prints A then B. The zero-delay timer still waited for the current code to finish.
- [ ] Watch a promise settle — `const p = fetch('/'); console.log(p)` — you'll see a Promise in state 'pending'. Log it again a moment later: fulfilled. You just watched an IOU get honoured.
- [ ] Cause a race — Open a page with a search box, type fast, and watch the Network panel. Multiple requests fire; whichever returns LAST wins the display — even if it's for an older query. That's a real bug class (stale response overwrites fresh), and you can trigger it by typing.
- [ ] Find an unhandled rejection — Browse a few apps with the console open, looking for `Uncaught (in promise)`. It means an async operation failed and nobody caught it. Somewhere, a spinner is spinning forever because of that line.

You froze a thread, queued a timer, watched a promise settle, and caused a race with your own typing.

- **My test passes locally and fails in CI, or passes on retry.**
  A race between your assertion and an async operation. Locally your API answers in 12ms; on CI it's slower and the DOM isn't ready. Fix: replace every fixed wait with a condition-based wait (`toBeVisible`, `toHaveText`). If a test only passes on retry, it is not a passing test — it's an unfixed race that will fail in front of a customer eventually.
- **The spinner spins forever.**
  A promise that never settled, or one that rejected with nobody listening. Console first: `Uncaught (in promise)` names the failure. Network panel second: is the request pending forever (server never answered) or did it return a 500 the code didn't handle? The spinner is a symptom of a promise stuck in 'pending' — find which one, and you've found the bug.
- **Typing quickly in a search box shows results for an earlier query.**
  A classic race. Request A (for 'ca') and request B (for 'cat') both in flight; A returns last and overwrites B's results. The code assumed responses arrive in the order they were sent. They don't, ever. Fix is server-agnostic: cancel stale requests, or ignore any response that isn't for the current query. Report it — it's a real defect, and you can reproduce it by typing fast.
- **The page freezes for a second when I click something.**
  Synchronous work is hogging the single thread — a big loop, a huge JSON parse, an expensive re-render. Nothing else can run, including your scroll and your clicks. DevTools → Performance → record and look for a long task. This is not a network problem, so no amount of caching will help. It's the waiter standing at one table.

### Where to check

Async behaviour, made visible:

- **Console** — `Uncaught (in promise)` is the loudest async smell there is. Never scroll past it.
- **Network → pending requests** — a request with no status has not come back. That's your stuck spinner, named.
- **Network → the order responses arrive** — not the order they were sent. Watch a fast-typed search and see it for yourself.
- **Performance panel → long tasks** — synchronous work blocking the thread. Anything over ~50ms is felt by a human.
- **Playwright's auto-waiting** — `expect(locator).toBeVisible()` retries until true. Learn what it does and you'll never write `sleep()` again.

Tester's habit: whenever behaviour depends on *timing*, run it three times fast and
three times slow (DevTools → Network → Slow 4G). Bugs that only appear at one speed are
races, and races are the most under-reported defect class in web software — because
they're invisible on a fast laptop.

### Worked example: the search box that lied about what you typed

A race condition, found by typing quickly. Cost: four minutes.

1. **Symptom:** occasionally, searching for `cat` shows results for `ca`. Users report it as "the search is wrong sometimes." Nobody can reproduce it on demand.
2. **Reproduce deliberately.** Throttle the network to Slow 3G (this widens the window the race needs) and type `cat` quickly. The bug appears every time. **Slowness didn't cause the bug; it revealed it.**
3. **Network panel.** Two requests: `?q=ca` then `?q=cat`. Look at the *response* times: `?q=cat` returns in 400ms, `?q=ca` in 700ms. The older query answered last.
4. **The mechanism, straight from this note.** Both callbacks were queued. The one that arrived last ran last, and its handler wrote its results into the DOM — overwriting the correct, newer results. The code assumed responses come back in the order they were sent. Nothing guarantees that. Nothing ever has.
5. **Confirm it's not the server.** Both responses are correct for their own query — check the response bodies. The API is blameless; the client's assumption is the defect.
6. **The report:** 'Search results race: responses are applied in arrival order, not request order. A slower earlier request overwrites a faster later one. Repro: throttle to Slow 3G, type "cat" quickly — results for "ca" display. Fix: ignore responses whose query no longer matches the input, or cancel in-flight requests on each keystroke.'
7. **Why this is a senior-looking find:** you reproduced an intermittent bug *on demand* by widening the race window with throttling. That single technique — make the machine slower so the bug becomes reliable — is worth more than any framework you'll learn this year.

> **Common mistake**
>
> Fixing a flaky test with `sleep()`. It feels like it works, and it is the most expensive
> mistake in test automation. A fixed wait is a bet on the server's mood: too short and
> the test still fails sometimes; too long and every run wastes those seconds forever,
> across thousands of runs. Worse, it *hides* the race rather than proving it's absent —
> so the underlying bug ships to users, who experience it as "the app is weird sometimes."
> Wait for the condition you actually care about, not for a number of milliseconds. A test
> that says "wait until this row appears" is both faster and more honest than one that
> says "wait two seconds and hope."

**Quiz.** A test clicks a button that triggers `fetch()`, then immediately asserts a table row exists. It passes locally and fails on CI. What is happening, and what is the correct fix?

- [ ] CI is broken — add a retry to the test suite
- [x] A race: the fetch callback is queued and only runs after the current code finishes, so the row doesn't exist when the assertion runs. Locally the API is fast enough to win; on CI it isn't. The fix is a condition-based wait (retry until the row is visible), not a fixed sleep.
- [ ] The CI server has less memory
- [ ] Add sleep(2000) before the assertion

*JavaScript is single-threaded: `fetch` hands off the request and execution continues immediately. The callback that builds the row waits on a queue and runs only after the current code completes — by which time your assertion has already failed. Local speed masks it; CI's slower network exposes it. `sleep(2000)` makes the suite slow and still flaky on a bad day; waiting for the condition ('until the row is visible') asks the real question, passes as soon as it's true, and fails with a useful message when it never is.*

- **JavaScript's thread model** — One thread, one thing at a time. Async work is handed off; its callback waits on a queue and runs only after the current code finishes. Nothing interrupts running code.
- **setTimeout(f, 0)** — Does not run f now. It queues f to run after the current code completes. Zero delay still means 'later'.
- **Promise states** — Pending (spinner spinning), fulfilled (value arrived), rejected (it failed). An unhandled rejection prints `Uncaught (in promise)` and often means a spinner never stops.
- **Why tests go flaky** — The assertion runs before the queued callback has built the DOM. Fast locally, slow on CI. The code never changed — only the timing did.
- **Wait for state, not time** — `sleep(2000)` is a bet on the server's mood: slow always, flaky sometimes, and it hides the race. Retry until the condition holds instead.
- **Response order ≠ request order** — Two in-flight requests can return in either order. Code that applies whichever arrives last overwrites fresh data with stale. Reproduce it by throttling and typing fast.

### Challenge

Open any app with a search box, throttle to Slow 3G, and type a word quickly. Watch the
Network panel: do responses return in the order they were sent? Does the UI ever show
results for a query you've already moved past? If yes, you've found a race condition in
production software using nothing but a dropdown and your fingers. Write it up with the
two request URLs and their response times — that's a complete bug report.

### Ask the community

> Async question: [what happens]. Network panel shows requests [list, with the order they were SENT and the order they RETURNED]. Console: [any `Uncaught (in promise)`]. Reproduces when throttled to Slow 3G: [yes/no]. Test does [fixed sleep / condition wait].

That 'reproduces when throttled' line is the tell. If slowing the network makes an
intermittent bug reliable, you have a race, and you can say so with confidence rather
than calling it flaky. Widening the window is how you turn 'sometimes' into 'always',
and 'always' is what gets fixed.

- [MDN — asynchronous JavaScript, from callbacks to await](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous)
- [Playwright — auto-waiting, and why you never need sleep()](https://playwright.dev/docs/actionability)
- [The event loop, visually (the talk everyone recommends)](https://www.youtube.com/watch?v=8aGhZQkoFbQ)

🎬 [What the heck is the event loop?](https://www.youtube.com/watch?v=8aGhZQkoFbQ) (26 min)

- JavaScript runs one thing at a time. Async work is handed off and its callback waits on a queue — it can never interrupt code that's currently running.
- `setTimeout(f, 0)` still runs after the current code. `await` suspends a function and resumes it later, at a moment you didn't choose.
- Flaky tests are races: the assertion runs before the queued callback built the DOM. Fast locally, slow on CI, code unchanged.
- Wait for state, never for time. A fixed sleep is slow on good days, flaky on bad ones, and hides the race from users.
- Responses do not arrive in the order they were sent. Throttling the network widens the race window and turns an intermittent bug into a reproducible one — the most valuable trick in this note.


---
_Source: `packages/curriculum/content/notes/the-web-platform-for-testers/javascript-for-readers/async-and-loading.mdx`_
