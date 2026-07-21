---
title: "Asking good questions"
tags: ["your-first-90-days", "working-solo-the-mentor-gap", "track-c"]
updated: "2026-07-20"
---

# Asking good questions

*How to ask questions that build credibility instead of eroding it: do the basic research first, lead with what you found, and batch questions instead of interrupting repeatedly.*

> With no in-house QA mentor, every question has to go to a developer, a manager, or a stranger in a
> community thread who is doing you a favor by answering at all. The same question can read as sharp
> or as a burden depending only on how much work happened before it was asked.

> **In real life**
>
> A second-year resident does not walk into an attending's office and ask "what's wrong with this
> patient?" She checks the vitals herself, forms a working guess, and says: "I found this, my read is
> X — does that match yours?" The attending's time gets spent confirming or correcting a real
> assessment, not doing the resident's first pass for her.

**Research-first question**: A research-first question is one that arrives with the asker's own findings and best guess already attached, framed as a request to confirm or correct rather than a request to be handed the answer from nothing.

## Do the basic research before you ask

Checking the docs, the existing tickets, the README, or the last similar bug report costs a few
minutes and often answers the question outright. When it does not, it still gives you something
concrete to bring: "I checked X and Y, here is what I found" is a different opening than "how do I
do this?" asked cold, and colleagues can tell the difference immediately.

## Lead with what you found, not with what you want handed to you

"Here's what I found, is this right?" invites a quick confirm-or-correct. "How do I do X?" invites a
full explanation from zero, which costs far more of someone else's time and teaches you less about
how to get there yourself next time.

## Batch questions instead of interrupting repeatedly

Five separate interruptions across a day cost a colleague five context switches. The same five
questions, held and sent as one message before lunch or at day's end, cost one. Genuinely urgent
questions are the exception, not the default.

> **Tip**
>
> Keep a running note of questions as they come up during the day. Before sending any of them, do a
> five-minute check against docs or existing tickets — several will answer themselves, and the rest
> go out already stronger for having a first attempt attached.

> **Common mistake**
>
> Do not let "I don't want to look like I don't know" turn into silently guessing and shipping the
> guess. A confidently wrong guess costs more credibility to fix later than a well-prepared question
> ever costs to ask. The goal is not fewer questions — it is questions that show real work behind them.

![A female doctor in a white coat points a pen at one chest x-ray on a lightboard while two other physicians listen, with several chest x-ray images visible on the board above her](asking-good-questions.jpg)
*Radiologist Discusses Chest X-rays — National Cancer Institute, Wikimedia Commons, Public domain. [Source](https://commons.wikimedia.org/wiki/File:Radiologist_discusses_chest_x-rays.jpg)*
- **A full board, scanned before narrowing down** — Eight images sit on the lightboard, but the discussion is about specific findings. Research comes first; the question narrows only after the wider check has already happened.
- **One pen, pointed at one finding** — She is not asking a vague, open-ended question about the whole board. A good question names the exact thing being checked, not everything that could possibly be wrong.
- **A colleague listening, not lecturing** — The two physicians in front are there to confirm or correct a specific read, not to walk her through the basics from zero. That is what a prepared question buys you.
- **A second colleague, present for the same brief exchange** — One well-prepared exchange serves two listeners at once. Batching a real finding into one clear presentation respects everyone's time in the room, not just one person's.

**Turning a question into evidence**

1. **Check the obvious sources first** — Docs, past tickets, the README, and recent commit history often already contain the answer.
2. **Form a specific, checkable guess** — A concrete guess gives the other person something to confirm or correct instead of building an answer from nothing.
3. **Lead with what you found** — "Here's what I found, is this right?" signals real work already done, not a request to be handed the answer.
4. **Batch non-urgent questions** — Hold what can wait and send it as one message instead of several separate interruptions across the day.

*A question-quality scorer (Python)*

```python
questions = [
    {"text": "How do I write a test plan?", "did_research": False, "showed_attempt": False, "specific": False},
    {"text": "Checked the API docs, tried POST with this JSON body, got a 422 - is this the right shape?", "did_research": True, "showed_attempt": True, "specific": True},
    {"text": "Compared this to spec section 4.2 and the behavior looks off - is this a bug or intended?", "did_research": True, "showed_attempt": True, "specific": True},
    {"text": "What do I do about this ticket?", "did_research": False, "showed_attempt": False, "specific": False},
]
def score(q):
    points = 0
    if q["did_research"]:
        points += 40
    if q["showed_attempt"]:
        points += 30
    if q["specific"]:
        points += 30
    return points
scores = []
for q in questions:
    s = score(q)
    label = "CREDIBILITY_BUILDING" if s >= 70 else "NEEDS_WORK"
    print(label + "=" + str(s))
    scores.append(s)
average = round(sum(scores) / len(scores))
print("AVERAGE=" + str(average))
result = "READY_TO_ASK" if average >= 50 else "KEEP_PRACTICING"
assert result == "READY_TO_ASK", "average question quality below threshold"
print("RESULT=" + result)
```

*A question-quality scorer (Java)*

```java
public class Main {
    static int score(boolean didResearch, boolean showedAttempt, boolean specific) {
        int points = 0;
        if (didResearch) points += 40;
        if (showedAttempt) points += 30;
        if (specific) points += 30;
        return points;
    }
    public static void main(String[] args) {
        boolean[][] questions = {
            {false, false, false},
            {true, true, true},
            {true, true, true},
            {false, false, false},
        };
        int total = 0;
        for (boolean[] q : questions) {
            int s = score(q[0], q[1], q[2]);
            String label = s >= 70 ? "CREDIBILITY_BUILDING" : "NEEDS_WORK";
            System.out.println(label + "=" + s);
            total += s;
        }
        int average = Math.round(total / (float) questions.length);
        System.out.println("AVERAGE=" + average);
        String result = average >= 50 ? "READY_TO_ASK" : "KEEP_PRACTICING";
        if (!result.equals("READY_TO_ASK")) throw new AssertionError("average question quality below threshold");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Build the habit before your next question

- [ ] Check the obvious sources first — Docs, the README, past tickets, and recent commits before anything else.
- [ ] Write your best guess before asking — Form a specific, checkable answer of your own, even if you are not confident in it.
- [ ] Lead with what you found, not \\"how do I\\" — State your research and your guess, then ask for confirmation or correction.
- [ ] Hold non-urgent questions in one running note — Send them as a single batched message instead of separate interruptions across the day.

- **Colleagues seem to sigh before answering your questions.**
  Check whether you did a five-minute research pass first, and start leading with what you already found.
- **You keep asking the same category of question repeatedly.**
  Write the answer down somewhere durable — your own notes — so the same thing does not need re-asking next month.
- **You are interrupting the same person multiple times a day.**
  Hold non-urgent questions in a running note and send them as one batch instead of several separate pings.

### Where to check

- Your last five questions — whether each led with your own research or asked cold from zero.
- Whether you interrupted the same person more than once today for something that could have waited.
- A running note where you can check if a question was already answered before asking it again.
- [[your-first-90-days/working-solo-the-mentor-gap/using-the-community]] for where a question goes when there is genuinely no one in-house left to ask.
- [[your-first-90-days/landing-well/your-first-bug-report-at-work]] for the same research-first instinct applied to writing up a bug report.

### Worked example: the same question, asked two different ways

1. Version one: "Hey, the checkout API isn't working, how do I fix it?" sent the moment something looks wrong.
2. Version two, same problem: "Checkout API returns 422 on a repeat card save. I checked the docs — the payload looks like it matches the spec. Logs show a null customer_id upstream of my request. Is that a known issue, or am I missing something on my side?"
3. The first version asks someone to reconstruct the entire investigation from nothing.
4. The second version asks for one specific confirmation, and it is answerable in under a minute.

**Quiz.** Which question is most likely to build a solo QA's credibility?

- [ ] "How do I test this feature?" sent the moment a new ticket appears
- [x] "I checked the spec and tried X, got Y instead of Z - is this a bug or expected?"
- [ ] A question sent, then re-sent five more times across the day as new thoughts arrive
- [ ] No question at all, followed by a best-effort guess shipped silently

*Leading with research already done and a specific, checkable result respects the other person's time and shows real work, which is what actually builds trust in a solo QA's questions over time.*

- **Research-first question** — A question that arrives with the asker's own findings and best guess attached, framed as a request to confirm or correct rather than to be handed an answer from nothing.
- **Batching questions** — Holding non-urgent questions in a running note and sending them as one message instead of several separate interruptions across a day.
- **Credibility-building versus credibility-eroding** — "Here's what I found, is this right?" builds credibility; a confidently shipped silent guess erodes it far more than a well-prepared question ever costs.

### Challenge

For one full day, write down every question before you ask it, along with the five-minute research check you did first. At the end of the day, count how many questions your own check already answered.

- [Atlassian — How to Ask (The Right) Questions At Work](https://www.atlassian.com/blog/loom/ask-questions-at-work)
- [The Muse — How to Ask Good Questions at Work, and Actually Get the Info You Need](https://www.themuse.com/advice/how-to-ask-good-questions)
- [How to Ask Good Questions for Deeper Workplace Conversations](https://www.youtube.com/watch?v=Dtm7nA9IgAY)

🎬 [How to Ask Good Questions for Deeper Workplace Conversations: Communicate and Connect](https://www.youtube.com/watch?v=Dtm7nA9IgAY) (6 min)

- A few minutes of research before asking often answers the question outright, and strengthens it when it does not.
- Lead with what you found and your best guess, not with a cold request to be handed the answer.
- Batch non-urgent questions into one message instead of interrupting repeatedly across the day.
- A confidently shipped silent guess costs more credibility than a well-prepared question ever costs to ask.


## Related notes

- [[Notes/your-first-90-days/working-solo-the-mentor-gap/being-the-only-qa|Being the only QA]]
- [[Notes/your-first-90-days/working-solo-the-mentor-gap/using-the-community|Using the community]]
- [[Notes/your-first-90-days/working-solo-the-mentor-gap/when-to-escalate|When to escalate]]
- [[Notes/your-first-90-days/landing-well/your-first-bug-report-at-work|Your first bug report at work]]


---
_Source: `packages/curriculum/content/notes/your-first-90-days/working-solo-the-mentor-gap/asking-good-questions.mdx`_
