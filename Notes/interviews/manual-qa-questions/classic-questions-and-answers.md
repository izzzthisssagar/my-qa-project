---
title: "Classic questions & answers"
tags: ["interviews", "manual-qa-questions", "track-c"]
updated: "2026-07-20"
---

# Classic questions & answers

*The manual QA interview's recurring core - QA vs QC, verification vs validation, severity vs priority, and what makes a bug report good - answered with reasoning an interviewer can actually follow.*

> Almost every manual QA interview, regardless of company size or seniority, circles back to the same
> handful of questions: what is the difference between QA and QC, verification and validation, severity
> and priority, and what actually makes a bug report good. These are not trick questions and they are not
> trivia - they are the interviewer's fastest way to check whether you understand the job or only
> memorized its vocabulary. A candidate who recites a textbook definition sounds identical to a candidate
> who understands it, right up until the interviewer asks one small follow-up. This note is about
> surviving that follow-up.

> **In real life**
>
> A driving test never worries that you memorized the manual's page on parallel parking - it puts you in
> an actual car, on an actual street, and watches whether you can execute the maneuver when a real curb,
> a real mirror check, and a real pedestrian are all happening at once. The examiner already knows you
> can recite "check your mirrors, signal, reverse slowly" - reciting it proves nothing. What proves
> something is doing it, then answering "why did you check your mirror twice there?" with a real reason
> instead of "because that's what you're supposed to do." Classic QA interview questions work the same
> way: the interviewer has heard the textbook definition of QA vs QC a thousand times, so the definition
> itself has almost no signal left in it. The signal is entirely in whether you can apply it to a
> scenario they invent on the spot.

**classic question**: A classic question is a small set of foundational QA distinctions - QA vs QC vs testing, verification vs validation, severity vs priority, and the anatomy of a good bug report - that recur across nearly every manual QA interview because they reveal whether a candidate understands the underlying reasoning or only memorized a definition. The tell is always the same: a memorized answer collapses on a follow-up scenario; an understood answer extends to one naturally.

## The four questions, and the reasoning behind each answer

**"What's the difference between QA and QC?"** QA is process-oriented prevention - coding standards,
requirement reviews, a definition of done, root-cause analysis after a bug escapes. QC is
product-oriented detection - examining the actual build against its requirements, and testing is the
core activity inside QC. The fast way to sound like you understand this rather than recite it: give an
example of each from a real day. "QA is us adding a rule that error messages get reviewed by design to our
definition of done last sprint. QC is me running the regression suite against last night's release
candidate." One sentence, two concrete examples, done.

**"What's the difference between verification and validation?"** Verification asks "did we build the
thing right?" - does it match the spec, the wireframe, the API contract. Validation asks "did we build
the right thing?" - does it actually solve the user's real problem when they use it live. A login page
can pass verification (it matches the wireframe exactly) and still fail validation (real users cannot
figure out where to click, because the wireframe itself was wrong). The interview-ready line: "Verification
checks against the spec; validation checks against the real need. You can pass one and fail the other,
and that gap is usually where the interesting bugs live."

**"What's the difference between severity and priority?"** Severity is the defect's own technical
impact - crash vs cosmetic, data loss vs display-only - judged independent of anyone's calendar. Priority
is a scheduling decision - how soon it gets worked, driven by business context. They are independent
axes: a rare crash can be low priority (workaround exists, tiny affected population), and a cosmetic typo
can be high priority (it is on the homepage during a funded ad campaign). Naming a real example where
they diverged is worth more than any definition.

**"What makes a bug report good?"** A stranger with zero context should be able to reproduce the bug,
understand its impact, and know it is already fixed once it is, without ever messaging you. That means:
a clear title stating the actual problem (not "login broken" but "login rejects valid password
containing an ampersand"), exact numbered repro steps, expected vs actual result, environment, and
evidence - a screenshot, a log line, a network trace. Missing any one of those five and the report
becomes a conversation instead of a document.

> **Tip**
>
> For every classic question, prepare one real example from your own experience, not a textbook case.
> Interviewers can tell the difference instantly, and a real example survives follow-up questions that a
> memorized one cannot. "Tell me about a time severity and priority disagreed" is a near-certain follow-up
> to the severity/priority question - have your answer ready before you walk in.

> **Common mistake**
>
> Answering with the definition and stopping there. "QA is prevention, QC is detection" is a correct
> sentence and a weak answer, because it is indistinguishable from something read off a flashcard ten
> minutes before the interview. The definition is the ticket to enter the conversation, not the answer
> itself - the answer is the definition plus one concrete example that shows you have actually lived the
> distinction, not just read about it.

![A young woman in a job interview sits at a glass conference table mid-answer, holding a pen and papers, facing an interviewer whose hand and pen are visible in the foreground taking notes](classic-questions-and-answers.jpg)
*Woman on a Job Interview - amtec_photos, Wikimedia Commons, CC BY-SA 2.0. [Source](https://commons.wikimedia.org/wiki/File:Woman_on_a_Job_Interview_-_38826218972.jpg)*
- **Mid-answer, not mid-recital** — Her expression is mid-thought, not mid-recitation. The best answers to classic questions sound like this - reasoned in the moment, not read off an internal script.
- **The paper on the table** — Notes and a resume are fine to glance at, but classic questions should not need them. If you must read a definition to answer 'QA vs QC', that is the tell an interviewer is listening for.
- **The pen mid-gesture** — A pen used to gesture while explaining a real example, not to point at a written answer. Explaining out loud, hands moving, is what a genuinely understood answer looks like from the outside.
- **The interviewer's pen, actively writing** — Interviewers write down specifics, not restated definitions. A concrete example ('last sprint we added X to our definition of done') is the sentence that actually gets written in the notes.

**How one classic question gets asked, answered, and probed**

1. **The question lands** — "What's the difference between severity and priority?" - a question the interviewer has heard answered a hundred times before.
2. **The definition, stated fast** — Severity is technical impact, priority is scheduling urgency - said in one breath, because the definition itself carries little signal.
3. **The concrete example, which carries the real signal** — "A Critical crash affecting three enterprise accounts got P2'd because a manual workaround existed and fixing it properly needed a week we didn't have before a launch."
4. **The follow-up** — "Who decided that, and would you have decided differently?" - the question that separates memorization from judgment.
5. **The judgment call, stated honestly** — A real opinion, with reasoning, beats a safe non-answer - interviewers are evaluating how you think, not whether you agree with them.

Here is the shape of a classic-question mock interview turned into a runnable quiz-style checker - six
scenarios across the three binary distinctions, graded against a candidate's labels:

*Run it - grade classic-question scenario labels (Python)*

```python
scenarios = [
    {"id": "S1", "statement": "A checklist added to the definition of done so a missed edge case cannot recur", "answer": "QA"},
    {"id": "S2", "statement": "Running the regression suite against tonight's release candidate build", "answer": "QC"},
    {"id": "S3", "statement": "Confirming the login page matches the approved wireframe and API contract", "answer": "verification"},
    {"id": "S4", "statement": "Confirming the login page actually lets a real user sign in and reach the dashboard", "answer": "validation"},
    {"id": "S5", "statement": "A checkout bug that crashes the app for every user, no workaround exists", "answer": "severity"},
    {"id": "S6", "statement": "A cosmetic bug the CEO wants fixed before tomorrow's live demo", "answer": "priority"},
]

candidate_answers = {
    "S1": "QA",
    "S2": "QC",
    "S3": "verification",
    "S4": "validation",
    "S5": "severity",
    "S6": "priority",
}

def grade(items, answers):
    results = []
    for s in items:
        given = answers.get(s["id"])
        correct = given == s["answer"]
        results.append((s["id"], given, s["answer"], correct))
    return results

results = grade(scenarios, candidate_answers)
score = sum(1 for r in results if r[3])
for sid, given, answer, correct in results:
    print(f"{sid}: you said {given}, correct is {answer} -> {'PASS' if correct else 'FAIL'}")

print(f"SCORE={score}/{len(scenarios)}")
print("ADVANCE" if score == len(scenarios) else "REVIEW")
```

Same grader in Java, the kind of quick self-check you can run the night before an interview to confirm
the four classic distinctions actually stuck:

*Run it - grade classic-question scenario labels (Java)*

```java
import java.util.*;

public class Main {
    record Scenario(String id, String statement, String answer) {}

    public static void main(String[] args) {
        List<Scenario> scenarios = List.of(
            new Scenario("S1", "A checklist added to the definition of done so a missed edge case cannot recur", "QA"),
            new Scenario("S2", "Running the regression suite against tonight's release candidate build", "QC"),
            new Scenario("S3", "Confirming the login page matches the approved wireframe and API contract", "verification"),
            new Scenario("S4", "Confirming the login page actually lets a real user sign in and reach the dashboard", "validation"),
            new Scenario("S5", "A checkout bug that crashes the app for every user, no workaround exists", "severity"),
            new Scenario("S6", "A cosmetic bug the CEO wants fixed before tomorrow's live demo", "priority")
        );

        Map<String, String> candidateAnswers = new LinkedHashMap<>();
        candidateAnswers.put("S1", "QA");
        candidateAnswers.put("S2", "QC");
        candidateAnswers.put("S3", "verification");
        candidateAnswers.put("S4", "validation");
        candidateAnswers.put("S5", "severity");
        candidateAnswers.put("S6", "priority");

        int score = 0;
        for (Scenario s : scenarios) {
            String given = candidateAnswers.get(s.id());
            boolean correct = given.equals(s.answer());
            if (correct) score++;
            System.out.println(s.id() + ": you said " + given + ", correct is " + s.answer() + " -> " + (correct ? "PASS" : "FAIL"));
        }

        System.out.println("SCORE=" + score + "/" + scenarios.size());
        System.out.println(score == scenarios.size() ? "ADVANCE" : "REVIEW");
    }
}
```

### Your first time: Your mission: build a one-page answer sheet for the four classic questions

- [ ] Write the one-sentence definition for each of the four questions — QA vs QC, verification vs validation, severity vs priority, and the five elements of a good bug report - short enough to say without pausing.
- [ ] Attach one real example to each definition — Pull from your own testing experience, a practice project, or a bug you genuinely filed - not an invented textbook case.
- [ ] Say each answer out loud, unscripted, three times — The goal is sounding like reasoning, not recitation. If you stumble on the third try, the example is not yet natural to you.
- [ ] Run the Python playground and get every scenario right — Then swap two answer keys deliberately and confirm the checker catches the mistake - understanding what FAIL looks like matters too.
- [ ] Invent one follow-up question per answer and answer it out loud — "Tell me about a time severity and priority disagreed" for the third question is a near-guaranteed follow-up - do not let it surprise you in the real interview.

You now have a one-page answer sheet built from your own reasoning and your own examples, not someone
else's flashcards - which is exactly what survives a live follow-up question.

- **You give the correct definition but freeze when asked for an example.**
  This means the concept is memorized, not internalized. Go back through your own testing work - practice projects count - and find one real instance of each distinction before the next interview, even a small one.
- **Your QA vs QC answer keeps drifting into just describing your daily tasks.**
  Ground it back in the definition first (process vs product, prevention vs detection), then use the daily task as the example, not as a replacement for the distinction itself.
- **An interviewer's follow-up question catches you completely off guard.**
  That is the exact purpose of the follow-up - it is not personal and it is not a failure. Answer honestly with your reasoning in the moment rather than reaching for another memorized line; genuine reasoning under a surprise question is what the question is actually testing.

### Where to check

- The ISTQB Glossary for the precise, citable wording of each classic distinction, in case an interviewer asks for the textbook phrasing specifically.
- Your own past bug reports and test sessions - real examples you can describe in one or two sentences without hesitation.
- Mock interview recordings of yourself, even made on a phone alone in a room - listening back reveals which answers still sound memorized.
- [[interviews/manual-qa-questions/talking-through-bugs]] for the deeper version of the "good bug report" question, where you narrate a full real bug end to end.
- [[interviews/manual-qa-questions/test-design-exercises]] for the live-application version of this same understand-it-versus-recite-it distinction, applied to a form field instead of a definition.

### Worked example: a follow-up question that separates a memorized answer from a real one

1. The interviewer asks the standard question: "What's the difference between severity and priority?"
2. The candidate answers correctly: "Severity is the technical impact, priority is business urgency,
   and they're independent axes."
3. The interviewer follows up immediately: "Give me a real bug where they didn't match."
4. A memorized answer stalls here, because no example was ever prepared - only the definition was.
5. A prepared candidate answers: "A checkout bug corrupted export files for about a dozen enterprise
   accounts - Critical severity, real damage, no workaround. But those accounts had already been
   individually notified with a manual fix, and a proper repair needed a full week that would have
   delayed an unrelated launch. We set it P2. A cosmetic logo misalignment on the signup page, meanwhile,
   got P0'd the same week because a national ad campaign was actively driving traffic to that exact page."
6. That single answer proves the definition was understood, not recited - it shows the reasoning behind
   a real, defensible business decision, which is precisely what "independent axes" means in practice.
7. The lesson generalizes: every classic question has a near-certain follow-up, and the follow-up is
   always "now show me," never "say it again."

**Quiz.** An interviewer asks 'What's the difference between QA and QC?' and you answer correctly with the textbook definition. What should you do next, unprompted?

- [ ] Wait for the next question, since you answered correctly
- [ ] Repeat the definition in different words to show you really understand it
- [x] Add one concrete, real example from your own experience that shows the distinction in action
- [ ] Ask the interviewer to clarify what they meant by the question

*A correct definition is the entry ticket, not the answer itself - interviewers have heard the textbook phrasing constantly, so it carries little signal on its own. Volunteering one real, concrete example unprompted is what demonstrates understanding rather than memorization, and it also preempts the almost-certain follow-up question asking for exactly that example. Repeating the definition in different words (option two) is still just definition, not evidence of understanding. Waiting silently (option one) wastes the strongest moment you have to differentiate your answer. Asking for clarification (option four) is reasonable only if the question was genuinely ambiguous, which this one is not.*

- **QA vs QC - the one-line answer plus example** — QA is process-oriented prevention, QC is product-oriented detection. Example: 'QA is adding a review rule to our definition of done; QC is running the regression suite against the release candidate.'
- **Verification vs validation - the one-line answer plus example** — Verification checks against the spec ('did we build it right'); validation checks against the real need ('did we build the right thing'). A page can pass one and fail the other.
- **Severity vs priority - the one-line answer plus example** — Severity is the defect's own technical impact, judged independent of anyone's calendar. Priority is a scheduling decision driven by business context. They are independent axes and can point in opposite directions, legitimately.
- **The five elements of a good bug report** — A specific title, exact numbered repro steps, expected vs actual result, environment, and evidence (screenshot, log, or trace) - missing any one turns the report into a conversation instead of a document.
- **Why a correct definition alone is a weak interview answer** — It is indistinguishable from a flashcard read minutes before the interview. The real signal is a concrete example attached to the definition, which a memorized answer usually lacks.
- **The near-universal follow-up to any classic question** — "Give me a real example" or "tell me about a time this happened to you." Prepare one real example per classic question before the interview, not during it.

### Challenge

Write out full answers to all four classic questions from this note, each with a genuine example from
your own experience (a practice project counts). Then write one plausible follow-up question per
answer and answer that too, out loud, unscripted. Finally, open the Python playground, deliberately
swap two entries in `candidate_answers` so they are wrong, run it, and read the FAIL lines - notice
exactly which information they give you that a bare score would not.

### Ask the community

> I'm prepping the classic QA interview questions and my weakest one is `[QA vs QC / verification vs validation / severity vs priority / good bug reports]`. Here's my current one-line answer: `[your answer]`. What follow-up would you ask if you were interviewing me, and what's missing?

Naming your actual current answer, not just the topic, gets far more useful feedback than "how do I
answer this question" - the community can tell you specifically whether it sounds memorized or reasoned.

- [Guru99 - 150+ manual and software testing interview questions and answers](https://www.guru99.com/software-testing-interview-questions.html)
- [GeeksforGeeks - manual testing interview questions](https://www.geeksforgeeks.org/software-testing/manual-testing-interview-questions/)
- [Manual Testing: QA Interview Preparation Questions and Answers](https://www.youtube.com/watch?v=t4OeuVi1jQQ)

🎬 [Manual Testing: QA Interview Preparation Questions and Answers](https://www.youtube.com/watch?v=t4OeuVi1jQQ) (11 min)

- The four classic questions - QA vs QC, verification vs validation, severity vs priority, and what makes a bug report good - recur because they reveal understanding, not vocabulary.
- A correct definition is the entry ticket; a real, concrete example is the actual answer an interviewer is listening for.
- Every classic question has a near-certain follow-up asking for a specific instance - prepare that example before the interview, not during it.
- The tell an interviewer is watching for is whether an answer extends naturally to a new scenario, or collapses back to the same memorized sentence.


## Related notes

- [[Notes/interviews/manual-qa-questions/test-design-exercises|Test-design exercises]]
- [[Notes/interviews/manual-qa-questions/test-this-pen-scenarios|Test this pen scenarios]]
- [[Notes/interviews/manual-qa-questions/talking-through-bugs|Talking through bugs]]


---
_Source: `packages/curriculum/content/notes/interviews/manual-qa-questions/classic-questions-and-answers.mdx`_
