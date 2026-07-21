---
title: "Feedback loops"
tags: ["interviews", "mock-practice", "track-c"]
updated: "2026-07-21"
---

# Feedback loops

*A boomerang that never came back would just be a strangely bent stick - the entire design only means something because it returns information about the throw. A single mock interview with no return signal is exactly that: effort spent with nothing coming back to actually improve on.*

> Doing five mock interviews in a row without reviewing any of them afterward feels like a lot of
> practice, but it's closer to throwing the same pitch five times with eyes closed - repetition without
> any signal about what to adjust produces very little real improvement, no matter how many reps pile up.

> **In real life**
>
> A boomerang's entire design exists around one purpose: coming back, carrying real information about
> how it was thrown - too much angle, not enough spin, thrown slightly off-line. A boomerang that never
> returned would just be an oddly bent stick, and a thrower who never adjusted based on where it landed
> would keep making the exact same mistake indefinitely, no matter how many times they threw it. A
> feedback loop in interview practice works the same way: the attempt only produces real improvement once
> some signal comes back about what actually happened, and that signal actually changes the next attempt.

**A feedback loop**: A feedback loop, in interview preparation, is the repeating cycle of attempting an answer, getting a specific signal about how it landed - self-reviewed, recorded, or from another person - and deliberately changing the next attempt based on that signal, rather than simply repeating the same attempt unchanged.

## Repetition without a real signal barely moves the needle

Practicing the same answer ten times without any specific feedback in between mostly reinforces
whatever pattern was already there, good or bad - filler words, a rushed ending, a vague structure all
get repeated right alongside whatever's already working. A feedback loop requires a distinct signal
step between attempts: a recording reviewed, specific written notes, or another person's direct
reaction - something that names what actually happened, not just a general sense that "that one felt
about the same as the last one."

## The loop has to actually close, not just generate information

Feedback that gets received but never acted on isn't a loop - it's a dead end. Writing "rushed the
ending" as a note after reviewing a recording only produces improvement if the next attempt
specifically targets that exact issue; skipping straight to a different practice question without
addressing the noted issue breaks the cycle before it closes. The loop closes specifically when the
next attempt is different, in a way that's traceable back to the previous signal - not just different
by chance, but changed on purpose because of what the feedback revealed.

> **Tip**
>
> After each practice attempt, write down exactly one specific thing to change before the next one -
> not a general "do better," but something concrete like "land the result in the final ten seconds
> instead of rushing it." One targeted change per loop closes faster than trying to fix everything at
> once.

> **Common mistake**
>
> Seeking feedback only from sources with no real signal in it - a friend who says "you did great!" to
> be supportive regardless of the actual answer. Encouragement has real value, but a feedback loop needs
> at least one source willing to name something specific and actionable, even when the answer was
> genuinely strong.

![A wooden plywood boomerang resting on green grass showing its curved shape](feedback-loops.jpg)
*Wooden boomerang — A.Savin, Free Art License (FAL), via Wikimedia Commons. [Source](https://commons.wikimedia.org/wiki/File:Wooden_boomerang_asv2021-05.jpg)*
- **One wing of the boomerang** — The outgoing attempt - the practice answer as thrown, before any information comes back about how it actually performed.
- **The other wing, angled back** — The return path - the signal coming back about the throw. A practice attempt with no equivalent return signal never actually completes a real feedback loop.
- **The curved bend where the two wings meet** — The pivot point where information about the previous attempt gets translated into a deliberate change for the next one - the moment the loop actually closes.
- **The visible layered plywood edge** — Built up in distinct, deliberate layers, not carved from a single uniform piece - the same way real skill improvement builds through distinct, deliberate loop cycles rather than one long undifferentiated practice session.

**Closing one real feedback loop**

1. **Attempt an answer under real or realistic conditions** — A genuine attempt, not a rehearsed-to-perfection read-through with no real pressure.
2. **Get a specific signal about how it landed** — A recording reviewed, written notes, or direct reaction from another person - something concrete, not a vague impression.
3. **Name exactly one thing to change** — Specific and actionable - 'land the result clearly' beats 'do better' every time.
4. **Make the next attempt different in that exact, traceable way** — The loop only closes once the next attempt is actually changed because of the signal - not just different by chance.

*Checking whether a feedback loop actually closed across two attempts (Python)*

```python
attempt_1 = {
    "noted_issue": "rushed the result in the final 10 seconds",
    "text": "...and we fixed it fast, moving on.",
}
attempt_2 = {
    "text": "...and the fix included a floor check on order totals, which has since caught two similar issues in later regression runs.",
}

# crude check: did attempt 2 give the ending noticeably more content/weight?
ending_1_words = len(attempt_1["text"].split())
ending_2_words = len(attempt_2["text"].split())

print("Noted issue: " + attempt_1["noted_issue"])
print("Attempt 1 ending length: " + str(ending_1_words) + " words")
print("Attempt 2 ending length: " + str(ending_2_words) + " words")

if ending_2_words > ending_1_words * 1.5:
    print("Loop CLOSED: the next attempt visibly addressed the noted issue")
else:
    print("Loop NOT clearly closed: attempt 2 doesn't show a clear, traceable change")
```

*Checking whether a feedback loop actually closed across two attempts (Java)*

```java
public class Main {
    public static void main(String[] args) {
        String notedIssue = "rushed the result in the final 10 seconds";
        String attempt1Text = "...and we fixed it fast, moving on.";
        String attempt2Text = "...and the fix included a floor check on order totals, " +
                "which has since caught two similar issues in later regression runs.";

        int ending1Words = attempt1Text.split("\\s+").length;
        int ending2Words = attempt2Text.split("\\s+").length;

        System.out.println("Noted issue: " + notedIssue);
        System.out.println("Attempt 1 ending length: " + ending1Words + " words");
        System.out.println("Attempt 2 ending length: " + ending2Words + " words");

        if (ending2Words > ending1Words * 1.5) {
            System.out.println("Loop CLOSED: the next attempt visibly addressed the noted issue");
        } else {
            System.out.println("Loop NOT clearly closed: attempt 2 doesn't show a clear, traceable change");
        }
    }
}
```

### Your first time: Run one complete feedback loop, start to close

- [ ] Attempt one practice answer under realistic conditions — Recorded, or in front of a real person - not silently rehearsed alone with no external signal.
- [ ] Get one specific, concrete signal about it — A recording reviewed, or direct written feedback from another person.
- [ ] Write down exactly one thing to change — Specific and actionable, not a general 'do better.'
- [ ] Make a second attempt and confirm the change is actually present — Compare the two attempts directly - the loop only closes if the change is real and traceable.

- **Many practice attempts happen but performance doesn't seem to improve over time.**
  Check whether any real signal is coming back between attempts - repetition alone, with no specific feedback closing the loop, mostly reinforces whatever pattern already exists, good or bad.
- **Feedback gets written down after every session but the same issues keep recurring.**
  The loop is generating signal but not closing - confirm the very next attempt specifically targets the noted issue, not just moves on to a different practice question.
- **All feedback comes from one consistently encouraging source with no specific critique.**
  Add at least one source willing to name something specific and actionable, even when an answer was genuinely strong - encouragement alone doesn't supply the concrete signal a loop needs to close.

### Where to check

- Any string of practice attempts, checked for whether a specific signal actually came back between them, not just repeated unchanged attempts.
- Written feedback notes, confirmed to be acted on in the very next attempt, not left unaddressed while practice moves to something else.
- [[interviews/mock-practice/mock-interview-drills]] for the realistic practice conditions a feedback loop needs to have something real to work with.
- [[interviews/mock-practice/recording-yourself]] for one of the most reliable sources of the specific signal a feedback loop depends on.
- [[interviews/mock-practice/handling-rejection]] for treating a real interview's outcome as its own kind of feedback signal, however uncomfortable.

### Worked example: a feedback loop that finally closed after several attempts that hadn't

1. A candidate runs four separate mock interviews across two weeks, each one recorded but never
   actually reviewed afterward - "I'll get to it later" each time.
2. Performance across the four sessions stays roughly flat; the same rushed ending shows up in every
   one, unnoticed because no review ever happened to surface it as a pattern.
3. Before a fifth session, the candidate finally watches all four recordings back and writes one
   specific note: "the last 10-15 seconds of every answer gets noticeably rushed."
4. The fifth mock interview is prepared with that one specific target: deliberately slowing down and
   giving the final line of each answer equal weight, timed in practice beforehand.
5. Reviewing the fifth recording shows the change clearly present and consistent - the first time in
   five sessions any specific, named issue actually got addressed and confirmed fixed, because this was
   the first time the loop actually closed rather than just generating another unreviewed recording.

**Quiz.** According to this note, what makes something an actual 'feedback loop' rather than just repeated practice?

- [ ] The total number of practice attempts completed
- [x] A specific signal coming back after each attempt, and the next attempt being deliberately changed in a traceable way because of that signal - repetition alone, without this, mostly reinforces existing patterns
- [ ] Whether the practice sessions are spaced exactly one week apart
- [ ] Whether the feedback comes from a professional coach rather than a friend

*Repetition without a specific signal in between mostly reinforces whatever pattern already exists, good or bad - like throwing a boomerang without ever noticing where it lands. A real feedback loop requires both a concrete signal about what happened and a next attempt that's deliberately, traceably different because of that signal - the loop only counts as closed once that connection is real, not just more unreviewed repetition.*

- **A feedback loop (interview prep)** — The repeating cycle of attempting an answer, getting a specific signal about how it landed, and deliberately changing the next attempt based on that signal - not simply repeating the same attempt unchanged.
- **Why repetition alone barely improves performance** — Without a specific signal between attempts, practice mostly reinforces whatever pattern already exists, good or bad - filler words and strengths both get repeated unchanged.
- **What it means for a feedback loop to 'close'** — The next attempt is actually, traceably different because of the previous signal - not just different by chance, and not skipped past without addressing what was noted.
- **Why purely encouraging feedback isn't enough on its own** — A feedback loop needs at least one source willing to name something specific and actionable - encouragement alone supplies no concrete signal to change the next attempt with.

### Challenge

Take one piece of feedback you've already received on a practice answer (or gather one now). Make a second attempt at that exact answer, specifically targeting that one piece of feedback, and confirm the change is actually present when compared side by side.

- [James Clear — Deliberate Practice: How to Build Expert Performance](https://jamesclear.com/deliberate-practice-theory)
- [MindTools — Deliberate Practice: Improving Your Skills](https://www.mindtools.com/axz1sql/deliberate-practice)
- [How to practice effectively...for just about anything | TED-Ed](https://www.youtube.com/watch?v=f2O6mQkFiiw)

🎬 [How to practice effectively...for just about anything - Annie Bosler and Don Greene | TED-Ed](https://www.youtube.com/watch?v=f2O6mQkFiiw) (5 min)

- A feedback loop needs both a specific signal and a next attempt that's deliberately, traceably changed because of it - not just more repetition.
- Repeated practice with no signal in between mostly reinforces existing patterns, good or bad, rather than improving them.
- Feedback that gets noted but never acted on in the next attempt is a broken loop, not a completed one.
- Target exactly one specific, concrete change per loop rather than trying to fix everything from a session at once.
- Encouragement alone doesn't supply the concrete signal a loop needs - at least one feedback source needs to name something specific and actionable.


## Related notes

- [[Notes/interviews/mock-practice/mock-interview-drills|Mock interview drills]]
- [[Notes/interviews/mock-practice/recording-yourself|Recording yourself]]
- [[Notes/interviews/mock-practice/handling-rejection|Handling rejection]]


---
_Source: `packages/curriculum/content/notes/interviews/mock-practice/feedback-loops.mdx`_
