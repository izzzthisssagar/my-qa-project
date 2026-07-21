---
title: "Problem-solving steps"
tags: ["working-with-data", "java", "python", "algorithms", "track-b"]
updated: "2026-07-11"
---

# Problem-solving steps

*The hardest part of coding isn't the syntax — it's staring at a big problem with no idea where to start. The fix is a repeatable recipe: understand it, work an example by hand, break it into small steps, solve one step at a time, and test as you go. You cross the river one stone at a time.*

> Here's the moment every beginner dreads: you're handed a problem — "find the average of the even
> numbers", "check if a word is a palindrome" — and your mind goes blank. You don't know where to
> *start*. That blankness isn't a sign you can't code; it's a sign you're trying to swallow the whole
> problem in one gulp. The people who look fast at this aren't smarter — they have a **recipe**: a
> fixed sequence of small moves that turns any vague problem into a list of tiny, obvious steps. Learn
> the recipe and the blank-mind moment disappears, because you always know the next move: not "solve
> the whole thing", just "take the next step."

> **In real life**
>
> Solving a problem is crossing a river on stepping stones. You can't leap the whole river in one
> jump — you'd fall in. But you don't have to: you step to the first stone, get your balance, then the
> next, then the next, and somehow you're across. The far bank is your goal (the working solution); the
> river is the gap between not-knowing and knowing; each stone is one small step you *can* actually
> take. Beginners freeze because they're staring at the far bank trying to jump it. The trick is to
> stop looking at the whole crossing and just find the nearest stone you can reach — then repeat.

## The recipe — five steps, every time

Whatever the problem, run it through these five steps in order. They're the difference between
staring blankly and always having a next move:

**1. Understand it.** What exactly goes IN, and what should come OUT? Write it down in one sentence.
"Input: a list of numbers. Output: one number, the average of the even ones." You cannot solve what
you can't state.

**2. Work an example by hand.** Take a concrete input — `[4, 7, 10]` — and solve it on paper. Evens
are 4 and 10, sum 14, count 2, average 7. Now you *know* the answer, so you can check your code.

**3. Break it into steps.** How did your hand solve it? "Keep the evens → add them up → divide by
how many." Those three phrases are your plan — the stepping stones — before you write any code.

**4. Solve one step at a time.** Write and run ONE step. Get "keep the evens" working and printing,
alone, before touching the sum. Small, verified steps beat one big leap you can't debug.

**5. Test as you go, and handle the edges.** Does it match your hand-worked answer? What about the
empty list, one item, all-odd? The edges are where the bugs live.

![A line of stepping stones crossing a river to a path on the far bank](stepping-stones.jpg)
*Stepping stones over the River Dove — Wikimedia Commons, CC BY 3.0. [Source](https://commons.wikimedia.org/wiki/File:Stepping_stones_over_the_River_Dove.JPG)*
- **The far bank = the SOLVED problem** — The path up the far hill is your goal — the working solution, the correct output. It's where you're trying to get, and it can look impossibly far when you're standing on this side with wet feet and no plan. Keep it in view (know what 'done' looks like: the output for a sample input), but don't try to LEAP to it.
- **The river = the gap you can't jump** — Between you and the answer is the gap: everything you don't yet know how to do. Beginners freeze because they try to cross it in one jump — to write the whole solution at once — and fall in. The river is only crossable in steps, and pretending otherwise is the single most common reason people get stuck.
- **The first stone = start where you CAN** — The nearest stone is the first small step you can definitely take: understand the input/output, or solve one tiny example by hand. You don't need to see every stone to take the first one. Starting — anywhere solid — is what breaks the freeze; the path reveals itself once you're moving.
- **Each stone = one small, solvable step** — Every stone is a step small enough to actually make: 'keep the evens', 'add them up', 'divide'. Break the crossing into stones this size and each one is easy, even when the whole river looked impossible. The skill isn't big leaps — it's choosing stones close enough together that every step is boring.
- **Cross in ORDER, landing each one = test as you go** — You put weight on each stone and make sure it holds before trusting the next. Solving is the same: get one step working and CHECK it (print it, compare to your hand-worked answer) before building the next on top. Skip the checking and you find out three stones later that you slipped — with no idea which stone was wet.

**Solving 'average of the even numbers' — press Play**

1. **Understand: what in, what out?** — Input: a list of numbers. Output: ONE number — the average of just the even ones. One sentence, written down. Already the fog lifts: you know the shape of the answer even though you can't yet code it.
2. **Work an example by hand** — Take [4, 7, 10, 3, 6]. By hand: evens are 4, 10, 6; sum is 20; count is 3; average is 20/3 ≈ 6.67. Now you have a known-correct answer to check your code against — and you noticed the steps your own hand took.
3. **Break it into steps** — Your hand did three things: keep the evens, add them up, divide by how many. Three phrases, in order — that's your plan, your stepping stones, written before a line of code. The hard thinking is done; what's left is translation.
4. **Solve one step, run it** — Write just 'keep the evens' and print the result: [4, 10, 6]. Correct? Good — that stone holds. Only now add 'sum them', run, check 20. Then 'divide', run, check 6.67. One stone at a time, each verified before the next.
5. **Test the edges** — Match the hand answer — yes. Now the edges: empty list (divide by zero!), all odds (no evens — same problem), one even. Handle them. The happy path was three easy stones; the edges are where the real bugs — and the real testing — live.

Here's that exact recipe carried out in Python — each step written and printed separately, the way
you'd actually build it, ending with the edge-case guard:

*Run it — one problem, solved one step at a time (Python)*

```python
numbers = [4, 7, 10, 3, 6, 9]

# Step 1 (understand): input = list of ints; output = one number, the mean of the evens.
# Step 2 (example by hand): evens 4,10,6 -> sum 20 -> count 3 -> 20/3 = 6.67

# Step 3 + 4: solve ONE step at a time, printing each so you can check it
evens = [n for n in numbers if n % 2 == 0]     # step: keep the evens
print("evens:", evens)

total = sum(evens)                              # step: add them up
print("total:", total)

count = len(evens)                              # step: how many
print("count:", count)

# Step 5: divide -- but GUARD the edge (empty -> divide by zero)
average = total / count if count > 0 else 0
print("average of evens:", round(average, 2))

# Test an edge by hand: all-odd input should give 0, not a crash
odds_only = [1, 3, 5]
ev = [n for n in odds_only if n % 2 == 0]
print("all-odd edge:", (sum(ev) / len(ev)) if ev else 0)
```

Now the same problem in Java — same five steps, same edge guard, just a counting loop instead of a
comprehension:

*Run it — the same problem, same steps (Java)*

```java
public class Main {
    public static void main(String[] args) {
        int[] numbers = {4, 7, 10, 3, 6, 9};

        // Steps 3 + 4: keep evens, summing and counting as we go
        int total = 0;
        int count = 0;
        for (int n : numbers) {
            if (n % 2 == 0) {          // step: is it even?
                total += n;             // step: add it up
                count++;                // step: count it
            }
        }
        System.out.println("evens total: " + total + ", count: " + count);

        // Step 5: divide, GUARDING the empty edge (no evens -> would divide by zero)
        double average = (count > 0) ? (double) total / count : 0;
        System.out.printf("average of evens: %.2f%n", average);
    }
}
```

algorithm

> **Tip**
>
> When you're stuck, the fastest unstick is almost always **solve a smaller example by hand and watch
> what your hand does.** Your brain already knows how to find the average of `[4, 10]` — it just did
> it. The steps it took (spot the evens, add, divide) ARE the algorithm; you only have to notice them
> and write them down. Coding a solution you can't perform by hand is coding blind. So before you type,
> do it on paper for a tiny input, narrate each move out loud, and those moves become your plan. If you
> can't do it by hand, you don't understand the problem yet — and that's the real blocker, not the code.

### Your first time: Your mission: cross one river

- [ ] State it in one sentence — In the Python playground, read the 'understand' comment: input = list of ints, output = mean of evens. Practice this on any problem — if you can't write the one-sentence in/out, you don't understand it yet.
- [ ] Do a tiny example by hand — Before running, work [4, 7, 10] on paper: evens 4,10, sum 14, count 2, average 7. Now you have a known answer to check the code against. This step feels slow and saves the most time.
- [ ] Watch each step print — The playground prints evens, then total, then count, then average — one step at a time. That's the recipe: build and verify each stone before the next, not the whole thing at once.
- [ ] Break the guard — Change `numbers` to all odd values `[1, 3, 5]` and run — the guard returns 0 instead of crashing on divide-by-zero. Remove the `if count > 0` guard and watch it break. The edge is the real test.
- [ ] Apply the recipe to a new problem — Try 'count the vowels in a word' in your head: understand (in: a word, out: a number), hand-example ('hello' -> 2), steps (look at each letter, is it a vowel, add one). You just planned an algorithm.

You've run a problem through all five steps — understand, example, break down, solve-one-step, test — which is the entire method, reusable on any problem you'll ever face.

- **I'm staring at the problem with no idea where to start.**
  You're trying to leap the whole river. Drop to step 1: write the input and output in one sentence. Then step 2: solve ONE tiny concrete example by hand. Ninety percent of 'I don't know where to start' dissolves the moment you stop trying to solve the whole thing and just do a small example by hand — the steps reveal themselves.
- **I wrote the whole solution at once and it doesn't work — no idea why.**
  You leapt instead of stepping. Break it back into steps and run them ONE at a time, printing each result, until you find the step whose output is wrong. Building the whole thing then debugging the whole thing is far harder than verifying each small step as you go. Comment out everything past the first step, get that right, then uncomment the next.
- **My code works on my example but fails on the real data.**
  Your example wasn't hostile enough. Step 2 is only useful if the example covers the tricky cases: the empty input, one item, all-same, the extremes, the wrong type. Re-do the hand-example with a nasty input and you'll usually find the step that doesn't handle it. Happy-path examples hide the exact bugs the real data exposes.
- **I can't tell if my algorithm is even correct.**
  Compare it against the answer you worked by hand in step 2 — that's what that step is FOR. If you skipped it, you have no reference to check against, so you can't tell right from plausible-looking-wrong. Work at least one input by hand, then assert your code produces exactly that. No hand answer means no way to know.
- **My steps are still too big — each one is its own puzzle.**
  Break them smaller. If 'process the data' is a step, it's not a stone, it's another river — split it until each step is something you could write in a line or two without thinking hard. The right step size is 'boring to implement'. Steps that are still puzzles mean the decomposition isn't finished.

### Where to check

The problem-solving process is also a testing process — decomposition tells you exactly what to test:

- **The one-sentence spec** — 'input X, output Y'. That sentence IS the top-level test: given X, do you get Y? A vague spec you can't write in one sentence is an untestable one.
- **The hand-worked example** — becomes your first assertion: this exact input must produce this exact output.
- **Each step's output** — testable on its own. If 'keep the evens' is a step, test it in isolation before trusting the steps built on it.
- **The edges of step 5** — empty, one item, all-same, the max, the wrong type. The happy path is a few easy stones; the edges are where you earn your keep.
- **The efficiency at scale** — a correct algorithm can still be too slow. If a step scans a list inside a loop, test with a big input (see [[when-to-use-which]]).

Tester's habit: **a clear spec is a testable spec, and decomposition writes your test list for you.** When
a developer breaks a feature into steps, each step and each edge is a test you can name in advance —
which is why 'help me understand exactly what this should do, in and out' is often a tester's most
valuable question. You can't test 'make it work'; you can test 'given an empty list, return 0'.

### Worked example: the feature nobody could test because nobody could state it

1. **The situation:** a team keeps arguing about whether a 'loyalty discount' feature is done. Every build, someone finds it 'wrong'. Bug reports contradict each other. It's been three sprints.
2. **The real problem isn't the code — it's step 1.** Nobody has written, in one sentence, what the feature should DO: exactly which input produces exactly which discount. Everyone has a slightly different picture in their head, so every build is 'wrong' by someone's private definition.
3. **A tester forces step 1:** "Let's write the input and output. Input: a customer's total and their years-as-member. Output: a discount percentage. What's the rule?" Silence — because the rule was never actually pinned down. The arguing was a symptom of an unstated spec.
4. **Working examples by hand (step 2) exposes the gaps.** '£100, 2 years → ?' Nobody agrees. '£100, 0 years → ?' — is a brand-new member eligible? Unspecified. 'What about exactly at a tier boundary, 5 years?' — the boundary was never defined. Each hand-example surfaces a decision nobody had made.
5. **Once the examples are agreed, the algorithm falls out.** With the rule stated and a table of input→output examples, breaking it into steps (find the tier from years → look up the tier's rate → apply to total → round) is straightforward, and every one of those examples becomes a test.
6. **The feature was never hard; the SPEC was missing.** Three sprints of thrashing weren't a coding problem — they were a step-1 problem. The code kept getting rewritten to match whichever mental model complained loudest, because there was no single written definition to build and test against.
7. **The tester's move that fixed it** wasn't finding a bug — it was refusing to accept 'make the discount work' and insisting on the one-sentence spec and a table of worked examples. That table simultaneously defined 'done' and wrote the entire test suite.
8. **The lesson for a tester.** The most valuable question is often the least technical: 'what exactly goes in, and what exactly should come out — for these specific examples, including the edges?' A problem you can't state you can't build and can't test. Decomposition isn't just how developers solve problems; it's how testers turn a vague feature into a concrete, checkable list of cases — and forcing step 1 is sometimes the whole fix.

> **Common mistake**
>
> Jumping straight to code before understanding the problem. It feels productive — you're typing! — but
> you're writing a solution to a problem you haven't defined, which is how you end up with clever code
> that solves the wrong thing. The tell is that you can't say, in one sentence, what your code should
> output for a given input. When that happens, stop typing: go back to step 1, state the in and out,
> work an example by hand. Five minutes on paper routinely saves an hour at the keyboard, because the
> hard part of most problems is understanding them, not coding them — and code written on a
> misunderstanding has to be thrown away, not fixed.

**Quiz.** You're handed a problem and your mind goes blank — you have no idea how to start writing the code. What's the most reliable FIRST move?

- [ ] Start typing code and see what happens
- [x] Don't write code yet — first state the input and output in one sentence, then solve one small concrete example BY HAND. Watching how your own hand solves it reveals the steps (the algorithm), and gives you a known-correct answer to check your code against. You break the freeze by taking the nearest small step, not by leaping to the whole solution.
- [ ] Search for someone else's complete solution to copy
- [ ] Give up on this problem and try an easier one

*The blank-mind freeze comes from trying to swallow the whole problem at once — leaping the river. The reliable cure is to shrink the first move until it's trivially doable: state the input and output in one sentence (you can't solve what you can't state), then work ONE tiny example by hand. That second step does double duty — the moves your hand makes ARE the algorithm (you just write them down), and the answer you get becomes the assertion your code must match. Typing code first feels productive but skips the understanding, so you often build a clever solution to the wrong problem. Copying a full solution robs you of the decomposition skill that's the whole point. For a tester this generalises directly: 'what exactly goes in and comes out, for these examples?' is the question that turns a vague feature into a testable spec — a problem you can't state, you can't test, and decomposition is how you make it statable.*

- **The five problem-solving steps** — 1) Understand (input/output in one sentence). 2) Work an example by hand. 3) Break into small steps. 4) Solve one step at a time, running each. 5) Test, including the edges.
- **Why solve an example by hand first?** — The moves your hand makes ARE the algorithm — write them down. And the answer becomes a known-correct value to check your code against. Can't do it by hand = don't understand it yet.
- **What is an algorithm?** — A finite, ordered list of clear steps that turns input into the desired output — a recipe. Good ones are correct (handle all inputs incl. edges) and efficient enough (not too slow at scale).
- **The stepping-stones principle** — Don't leap the whole problem — cross one small, solvable step at a time, verifying each before the next. Freezing comes from staring at the far bank instead of the nearest stone.
- **Why solve one step at a time (not all at once)?** — You can verify each small step's output before building on it, so a bug is localised to the step you just added. One big leap then debugging the whole thing is far harder.
- **Where do the bugs live?** — In the edges: empty input, one item, all-same, the extremes, the wrong type. The happy path is a few easy stones; the edges are what step 5 (test) and a tester target.
- **The tester's most valuable question** — 'What exactly goes in, and what exactly should come out — for these specific examples, including the edges?' A problem you can't state, you can't test. Decomposition writes the test list.

### Challenge

Pick a small problem — 'is a word a palindrome?' — and run it through all five steps WITHOUT coding
first: write the one-sentence in/out, solve 'racecar' and 'hello' by hand, list the steps your hand
took, then and only then translate to code in the playground. Next, break the average example by
feeding it an empty list with the guard removed, and watch the divide-by-zero. Finally, write one
sentence: for a feature described only as 'make the search work', what's the first question you'd ask
before you could test it?

### Ask the community

> Stuck on a problem: what it should do (input -> output, one sentence): `[fill in — if you can't, that's the blocker]`. A worked example by hand: `[input -> the answer you got by hand]`. The steps I think it takes: `[list them]`. Which step I'm stuck on: `[which]`. Language: `[Java/Python]`.

If you can fill in the one-sentence input→output and a hand-worked example, you're usually 80% unstuck
already — and if you CAN'T fill them in, that's the real blocker, not the code. Post those two things
and the step you're stuck on; the answer is almost always in a step that's still too big — break it smaller.

- [Polya's 'How to Solve It' — the classic problem-solving method](https://en.wikipedia.org/wiki/How_to_Solve_It)
- [How to think like a programmer — problem-solving, step by step](https://www.freecodecamp.org/news/how-to-think-like-a-programmer-lessons-in-problem-solving-d1d8bf1de7d2/)
- [Python docs — the control flow you'll build steps from](https://docs.python.org/3/tutorial/controlflow.html)
- [CS50 — problem sets that drill decomposition](https://cs50.harvard.edu/x/)

🎬 [How to think like a programmer — problem solving](https://www.youtube.com/watch?v=azcrPFhaY9k) (13 min)

- The blank-mind freeze comes from trying to solve the whole problem at once. The cure is a recipe: understand → example by hand → break into steps → solve one step → test.
- Solve a small example BY HAND first: the moves your hand makes are the algorithm, and the answer becomes a known-correct value to check your code against.
- Cross the river one stone at a time — write and verify each small step's output before building the next, instead of one big leap you then can't debug.
- The edges (empty, one item, all-same, extremes, wrong type) are where the bugs live, so step 5 is testing them — not just re-checking the happy path.
- For a tester: a clear spec is a testable spec. 'What exactly goes in and comes out, for these examples?' turns a vague feature into a concrete list of cases, and decomposition writes that list.


---
_Source: `packages/curriculum/content/notes/working-with-data/simple-algorithms/problem-solving-steps.mdx`_
