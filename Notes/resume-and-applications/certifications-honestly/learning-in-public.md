---
title: "Learning in public"
tags: ["resume-and-applications", "certifications-honestly", "track-c"]
updated: "2026-07-20"
---

# Learning in public

*Documenting your learning journey publicly - a blog post, a LinkedIn update, a running changelog - can outweigh a static certificate by showing the actual process, not just a claimed outcome.*

> A static certificate freezes one moment in time - pass this exam, on this date. A public learning log shows
> the whole arc that came before and after it, and more hiring managers are reading the arc than the single
> freeze-frame.

> **In real life**
>
> A ship's captain keeps a daily log - position, weather, storms weathered, decisions made along the way. At
> the end of the voyage, a single certificate might say only "arrived safely." Anyone reading just the
> certificate learns nothing about how the captain actually handled the storm on day twelve; anyone reading the
> log learns exactly how they think under pressure.

**Changelog**: A running, dated public record of what you learned, built, or fixed - published as you go rather than compiled once at the end, so the process itself becomes visible evidence.

## What learning in public actually means

Learning in public means regularly publishing short, honest updates about what you tried, what broke, and
what you figured out - a blog post, a LinkedIn update, a running changelog or notes repository. It doesn't
need to be polished or tutorial-quality; a few honest sentences about a specific problem and how you solved it
carries more real signal than a single, heavily edited post written once and never followed up. The habit
matters more than any individual entry.

## Why visible process can outweigh a static credential

A hiring manager skimming a few months of public posts sees real problem-solving, communication, and
consistency over time - a certificate proves none of that on its own. Writing about a specific bug also forces
clearer thinking about what actually happened, which reinforces the learning itself, not just the audience
reading it. And unlike an exam taken once, a visible habit compounds: each new post adds to a running,
dated body of evidence that keeps growing for as long as you keep the habit, at no cost beyond the time spent
writing.

> **Tip**
>
> Write about one specific bug or problem and exactly how you diagnosed it - specificity beats a vague "learned
> something today" post every time, and it's easier to write besides.

> **Common mistake**
>
> Don't wait until something feels "impressive enough" to post. A habit of small, consistent, honest updates
> beats a handful of polished posts that never actually get published because they're always not quite ready.

![An overhead view of hands writing in an open notebook on a desk, with a laptop keyboard visible nearby and a small plant in the background](learning-in-public.jpg)
*Person writing in notebook while using laptop at a modern workspace.jpg — Shixart1985, Wikimedia Commons, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Person_writing_in_notebook_while_using_laptop_at_a_modern_workspace.jpg)*
- **An open page, not yet public** — The first draft of a learning entry starts here, before it ever reaches a blog or a feed.
- **The act of writing it down** — Capturing what just happened while it's fresh is what makes an entry specific instead of a vague memory later.
- **The same entry, about to go public** — A private note like this becomes public signal only once it's typed up and actually published somewhere.
- **A timestamp on the habit** — Learning in public works as a running, dated record - a single post proves far less than a visible pattern of them over time.

**Turning a day's work into a public entry**

1. **Hit a real problem or learn something** — During practice, a lab, or a bug hunt - something specific, not a vague topic.
2. **Write 3-5 honest sentences the same day** — What happened, what you tried, and what actually fixed it.
3. **Publish it somewhere public** — A blog, LinkedIn, or a public changelog - not a private notes file only you can see.
4. **Link the running collection from your profile** — So a reviewer can see the pattern across entries, not just one post in isolation.

*Scoring a learning log for public signal (Python)*

```python
from datetime import date

entries = [
    {"date": date(2026, 7, 14), "topic": "Debugging a flaky Selenium wait", "url": "https://example.com/post1"},
    {"date": date(2026, 7, 15), "topic": "Reading job posts for exact keywords", "url": "https://example.com/post2"},
    {"date": date(2026, 7, 16), "topic": "Private notes, not published", "url": None},
    {"date": date(2026, 7, 17), "topic": "Writing a short cover letter", "url": "https://example.com/post3"},
    {"date": date(2026, 7, 20), "topic": "ISTQB tradeoffs", "url": "https://example.com/post4"},
]

published = [e for e in entries if e["url"] is not None]
print("TOTAL_ENTRIES=" + str(len(entries)))
print("PUBLISHED_ENTRIES=" + str(len(published)))

dates = sorted(e["date"] for e in published)
longest_streak = 1
current_streak = 1
for i in range(1, len(dates)):
    gap_days = (dates[i] - dates[i - 1]).days
    if gap_days <= 2:
        current_streak += 1
    else:
        current_streak = 1
    longest_streak = max(longest_streak, current_streak)

print("LONGEST_STREAK=" + str(longest_streak))
signal = "STRONG_PUBLIC_SIGNAL" if len(published) >= 4 else "BUILD_MORE_PUBLIC_ENTRIES"
print("VERDICT=" + signal)
```

*Scoring a learning log for public signal (Java)*

```java
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.*;

public class Main {
    static class Entry {
        LocalDate date;
        String topic;
        String url;
        Entry(LocalDate d, String t, String u) { date = d; topic = t; url = u; }
    }

    public static void main(String[] args) {
        List<Entry> entries = Arrays.asList(
            new Entry(LocalDate.of(2026, 7, 14), "Debugging a flaky Selenium wait", "https://example.com/post1"),
            new Entry(LocalDate.of(2026, 7, 15), "Reading job posts for exact keywords", "https://example.com/post2"),
            new Entry(LocalDate.of(2026, 7, 16), "Private notes, not published", null),
            new Entry(LocalDate.of(2026, 7, 17), "Writing a short cover letter", "https://example.com/post3"),
            new Entry(LocalDate.of(2026, 7, 20), "ISTQB tradeoffs", "https://example.com/post4")
        );

        List<LocalDate> dates = new ArrayList<>();
        for (Entry e : entries) if (e.url != null) dates.add(e.date);
        System.out.println("TOTAL_ENTRIES=" + entries.size());
        System.out.println("PUBLISHED_ENTRIES=" + dates.size());

        Collections.sort(dates);
        int longestStreak = 1;
        int currentStreak = 1;
        for (int i = 1; i < dates.size(); i++) {
            long gapDays = ChronoUnit.DAYS.between(dates.get(i - 1), dates.get(i));
            if (gapDays <= 2) currentStreak++;
            else currentStreak = 1;
            longestStreak = Math.max(longestStreak, currentStreak);
        }
        System.out.println("LONGEST_STREAK=" + longestStreak);
        String signal = dates.size() >= 4 ? "STRONG_PUBLIC_SIGNAL" : "BUILD_MORE_PUBLIC_ENTRIES";
        System.out.println("VERDICT=" + signal);
    }
}
```

### Your first time: Start a public learning log this week

- [ ] Pick one small thing you learned or fixed today — Specific beats general - a single bug, a single concept, a single mistake caught.
- [ ] Write 3-5 honest sentences about it the same day — What happened, what you tried, and what actually worked - while it's still fresh.
- [ ] Publish it somewhere public — A blog, LinkedIn, or a public notes repository - not a private file only you can see.
- [ ] Link the running collection from your resume or profile — So a reviewer sees the pattern across entries, not just one post in isolation.

- **You have plenty of private notes but nothing public to show.**
  Pick your best three private entries and republish them as-is, honestly labeled with their original dates - a late start still builds a real record.
- **You posted once and then stopped.**
  Lower the bar back down to 3-5 sentences and same-day publishing - a maintainable small habit beats an ambitious one you abandon.
- **You're not sure anyone reads it, so it feels pointless.**
  Treat it as a portfolio artifact first and an audience-builder second - link it directly in applications where it can be reviewed on its own.

### Where to check

- Whether your public entries are actually dated and public, not sitting in a private drafts folder.
- Whether recent entries are specific about one real problem, not vague summaries of a whole week.
- The gap between your entries - a long gap undercuts the "running record" case more than any single weak post.
- [[resume-and-applications/certifications-honestly/free-alternatives]] for pairing a learning log with the actual project work it documents.

### Worked example: a week of entries becoming a linkable record

1. A candidate fixes a flaky Selenium wait on Monday and publishes four honest sentences about it the same day.
2. On Tuesday, they publish a short post about reading job postings for exact keyword matches.
3. Wednesday's private notes stay private - no post that day, and that's fine.
4. By Sunday, four dated public posts exist, and the candidate links the whole collection directly from their resume, in place of a line about a certification they don't have.

**Quiz.** Why does a running public learning log carry weight a single certificate doesn't?

- [ ] Because certificates are never checked by employers
- [x] Because it shows a dated pattern of real problem-solving and communication over time, not one static claim
- [ ] Because it's technically required for every QA job
- [ ] Because it replaces the need for any hands-on practice

*A certificate proves a single passed exam on a single date. A dated, public log shows the actual thinking behind real problems solved over time - a pattern, not a freeze-frame.*

- **Learning in public** — Regularly publishing honest, specific updates about what you learned, tried, or fixed - not polished, just visible.
- **Why it can outweigh a static credential** — It shows a dated pattern of real problem-solving and communication over time, which a single certificate can't demonstrate.
- **The most common failure mode** — Waiting until an update feels 'impressive enough' to publish - consistency matters more than polish.

### Challenge

Write and publish one honest, specific entry today about something you actually learned or fixed this week - 3-5 sentences, dated, somewhere public. Link it from your profile in the space a certification line would otherwise sit.

- [swyx — Learn In Public](https://www.swyx.io/learn-in-public)
- [Rizèl Scarlett — How to Learn in Public](https://blackgirlbytes.dev/how-to-learn-in-public)
- [Anaïs Urlichs — Learning in Public: How to Get Started](https://anaisurl.com/learning-in-public/)

🎬 [Developer Love - Ep. #15, Learning in Public with Shawn “Swyx” Wang of Temporal](https://www.youtube.com/watch?v=SBbWVYBKzXE) (44 min)

- Learning in public means regularly publishing short, honest, dated updates about real problems and what you learned from them.
- A visible pattern of posts over time shows problem-solving and communication a single static certificate can't prove.
- Specificity beats polish - one real bug described honestly outbeats a vague 'learned something today' post.
- Consistency matters more than any individual entry - a small, maintainable habit beats an ambitious one you abandon.


## Related notes

- [[Notes/resume-and-applications/certifications-honestly/free-alternatives|Free alternatives]]
- [[Notes/resume-and-applications/certifications-honestly/when-certs-matter|When certs matter]]
- [[Notes/resume-and-applications/the-qa-resume/structure-that-works|Structure that works]]


---
_Source: `packages/curriculum/content/notes/resume-and-applications/certifications-honestly/learning-in-public.mdx`_
