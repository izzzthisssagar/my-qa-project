---
title: "Posting your progress"
tags: ["a-portfolio-that-gets-interviews", "profiles", "track-e"]
updated: "2026-07-21"
---

# Posting your progress

*Regularly posting short, real progress updates on the same platforms a recruiter already searches keeps a profile surfacing in recency-weighted feeds and search - a single static resume snapshot can't do that on its own.*

> Two candidates have identical LinkedIn profiles on paper - same headline, same skills, same experience. One
> posted a two-line update about a bug they found three days ago; the other's most recent activity is from
> eight months back. A recruiter scrolling a search results page sees one of them near the top of a feed
> today, and the other only if they scroll deep enough to reach a profile that's gone quiet.

> **In real life**
>
> Fenway Park's manual scoreboard, built into the Green Monster wall, doesn't wait until the ninth inning to
> show a result. An operator sits inside the wall itself and slides a new number into place after every half
> inning, for every team on the board, not just the home team - so anyone watching can see the game actually
> building, one real update at a time. A scoreboard that only revealed the final score at the end of the game
> would technically be accurate, but it would miss the entire point of a scoreboard: letting people track real
> progress as it happens, not just receive a verdict once everything is already decided. Posting your progress
> works the same way - a recruiter's feed rewards the profile that's visibly, recently in motion, not the one
> that only updates once a year with a finished result.

**Posting your progress**: Posting your progress is the practice of publishing short, honest updates about real, specific work - a shipped feature, a fixed bug, a finished module - on the same professional platforms a recruiter already searches, so a profile keeps surfacing in recency-weighted feeds and search instead of appearing only once, as a single static resume snapshot.

## Why recency is its own signal, separate from content

A recruiter's search and a platform's feed both weight recent activity - not because an old post was wrong,
but because a profile that's been quiet for months reads as inactive or possibly no longer job-searching at
all, regardless of how strong the underlying experience is. This is a different mechanism than the content of
any single post: two profiles can say the exact same things about a candidate's skills, and the one with
activity from this week will still surface more often than the one whose last visible action was months ago.
Staying visible is partly about what gets posted, and partly just about posting recently enough to still
appear at all.

## What actually counts as a real update

A real update names something specific: "Fixed a flaky Selenium wait that was failing intermittently in CI,"
not "Learning so much this week!" A finished module, a merged pull request, a bug found and reported clearly,
a small tool built to solve a real annoyance - each of these is a genuine, checkable event worth two or three
honest sentences. This is not the same discipline as keeping a running learning changelog (see
[[resume-and-applications/certifications-honestly/learning-in-public]] for that habit specifically) - posting
your progress here is narrower and more tactical: short, frequent, specific updates on the exact platforms a
recruiter is already searching, aimed at staying visibly active while a job search is actually happening.

> **Tip**
>
> Post the moment something real finishes, not on a fixed weekly schedule. A specific two-sentence update about
> a bug just fixed reads stronger than a vaguer post written because "it's Friday and I should post something."

> **Common mistake**
>
> Don't post once, land an interview request, and go quiet for the next two months. A profile's visible
> activity resets to looking stale the moment posting stops, regardless of how much real work is happening
> privately behind it - the recruiter's feed only sees what's actually posted.

![The manual scoreboard built into Fenway Park's Green Monster wall, showing inning columns numbered 1 through 10 with empty slots, columns of other league teams' scores tracked live, an at-bat/ball/strike/out indicator light panel, and a small dark doorway in the wall where an operator climbs inside to place each number by hand](posting-your-progress.jpg)
*2017 Fenway Park manual scoreboard - Beyond My Ken, Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:2017_Fenway_Park_manual_scoreboard.jpg)*
- **A door built right into the wall** — An operator physically climbs inside to place each new number by hand, after every half-inning - nothing here updates itself. Posting your progress is the same manual, repeated act, not something a profile does on its own.
- **Innings 1 through 10, still empty** — Blank slots waiting to be filled in one at a time, as the game actually happens - a running record built incrementally, not a single result posted once at the end.
- **Every other game in the league, tracked here too** — This board doesn't only post the home team's score - it posts everyone else's inning-by-inning progress alongside it, the same way a visible update sits in a shared feed next to everyone else's, not off in isolation.
- **At bat, ball, strike, out - the finest-grained layer** — This row updates almost pitch by pitch, the clearest version of posting the smallest real update as it happens instead of waiting to announce a final result.

**How a quiet profile and an active one diverge**

1. **Two profiles start identical** — Same headline, same skills, same experience - nothing in the static content tells them apart yet.
2. **One posts a specific two-line update** — A real, checkable event - a bug fixed, a module finished - published the same week it happened.
3. **A recruiter's feed and search both weight recency** — The recently active profile surfaces more often, independent of whether the underlying experience is actually stronger.
4. **The quiet profile still exists, just less visible** — Nothing about it got worse - it simply stopped showing up as often as the one still visibly in motion.

*A posting-cadence visibility checker (Python)*

```python
from datetime import date

posts = [
    date(2026, 6, 1),
    date(2026, 6, 9),
    date(2026, 6, 22),
    date(2026, 7, 20),
]
today = date(2026, 7, 21)
STALE_AFTER_DAYS = 14

gaps = []
for i in range(1, len(posts)):
    gaps.append((posts[i] - posts[i - 1]).days)
days_since_last_post = (today - posts[-1]).days

print("GAPS_BETWEEN_POSTS=" + ",".join(str(g) for g in gaps))
print("DAYS_SINCE_LAST_POST=" + str(days_since_last_post))
longest_gap = max(gaps)
print("LONGEST_GAP=" + str(longest_gap))

status = "CURRENTLY_SURFACING" if days_since_last_post <= STALE_AFTER_DAYS else "GONE_QUIET"
print("CURRENT_STATUS=" + status)
had_a_quiet_stretch = longest_gap > STALE_AFTER_DAYS
print("HAD_A_QUIET_STRETCH=" + ("YES" if had_a_quiet_stretch else "NO"))
result = "ACTIVE_BUT_HAD_A_GAP" if (status == "CURRENTLY_SURFACING" and had_a_quiet_stretch) else "OTHER"
assert result == "ACTIVE_BUT_HAD_A_GAP", "expected a recovered profile: active now, but with a real gap earlier"
print("RESULT=" + result)
```

*A posting-cadence visibility checker (Java)*

```java
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<LocalDate> posts = Arrays.asList(
            LocalDate.of(2026, 6, 1),
            LocalDate.of(2026, 6, 9),
            LocalDate.of(2026, 6, 22),
            LocalDate.of(2026, 7, 20)
        );
        LocalDate today = LocalDate.of(2026, 7, 21);
        int staleAfterDays = 14;

        List<Long> gaps = new ArrayList<>();
        for (int i = 1; i < posts.size(); i++) {
            gaps.add(ChronoUnit.DAYS.between(posts.get(i - 1), posts.get(i)));
        }
        long daysSinceLastPost = ChronoUnit.DAYS.between(posts.get(posts.size() - 1), today);

        StringBuilder gapsStr = new StringBuilder();
        for (int i = 0; i < gaps.size(); i++) {
            if (i > 0) gapsStr.append(",");
            gapsStr.append(gaps.get(i));
        }
        System.out.println("GAPS_BETWEEN_POSTS=" + gapsStr);
        System.out.println("DAYS_SINCE_LAST_POST=" + daysSinceLastPost);
        long longestGap = Collections.max(gaps);
        System.out.println("LONGEST_GAP=" + longestGap);

        String status = daysSinceLastPost <= staleAfterDays ? "CURRENTLY_SURFACING" : "GONE_QUIET";
        System.out.println("CURRENT_STATUS=" + status);
        boolean hadAQuietStretch = longestGap > staleAfterDays;
        System.out.println("HAD_A_QUIET_STRETCH=" + (hadAQuietStretch ? "YES" : "NO"));
        String result = (status.equals("CURRENTLY_SURFACING") && hadAQuietStretch) ? "ACTIVE_BUT_HAD_A_GAP" : "OTHER";
        if (!result.equals("ACTIVE_BUT_HAD_A_GAP")) throw new AssertionError("expected a recovered profile: active now, but with a real gap earlier");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Start posting your progress this week

- [ ] Pick one real, specific thing finished recently — A fixed bug, a completed module, a small tool built - something checkable, not a vague summary of a whole week.
- [ ] Write two or three honest sentences about it — What it was, and what it actually took - specific enough that a stranger could tell it's real work.
- [ ] Post it on the platform a recruiter actually searches — LinkedIn most often, matching the searchable positioning from [[a-portfolio-that-gets-interviews/profiles/linkedin-for-qa]].
- [ ] Repeat within two weeks, not on a rigid schedule — The next real update, whenever it actually happens - consistency of cadence matters more than a fixed calendar slot.

- **A profile's last visible activity is several months old.**
  Post one real, specific update now - a recent bug fix, a finished module, anything checkable - to reset how recently active the profile appears.
- **Posts happen regularly but never mention anything specific.**
  Replace vague posts like 'learning a lot' with one named, checkable event per post - see the specificity standard in [[resume-and-applications/certifications-honestly/learning-in-public]].
- **One post got attention, then activity stopped for months afterward.**
  Treat visibility as ongoing maintenance, not a one-time event - a single strong post doesn't keep surfacing on its own once enough time passes.

### Where to check

- Your own profile's most recent activity date, checked the way a recruiter would see it, logged out.
- Whether recent posts name something specific and checkable, not just a general feeling of progress.
- The actual gap between your last few posts - a long quiet stretch matters more than any single post's quality.
- [[a-portfolio-that-gets-interviews/profiles/personal-brand-basics]] for keeping the identity behind these posts consistent across every platform they appear on.

### Worked example: the same candidate, six months apart

1. In January, a candidate posts a detailed update about finishing a Selenium test suite - genuinely strong,
   specific work.
2. No further posts happen for the next six months, even though real practice and learning continued
   privately the whole time.
3. In July, a recruiter's search for "QA tester" surfaces a dozen more recently active profiles first; this
   candidate's January post is technically still there, just buried under months of silence.
4. The candidate posts a short, specific update about a bug found that same week - within days, the profile
   starts surfacing in searches again, on the strength of recency alone, before a single new skill was added.

**Quiz.** Why can two profiles with identical skills and experience get different visibility in a recruiter's search?

- [ ] Search results are random and unrelated to any profile activity
- [x] Recency of activity is its own signal separate from content - a profile that's been quiet for months surfaces less often regardless of how strong its underlying experience is
- [ ] Only paid accounts appear in recruiter searches
- [ ] Older profiles are always ranked higher because they show more experience

*Recency is a distinct signal from content quality. Two profiles can describe identical skills and experience, but the one with recent, visible activity surfaces more often in feeds and search - staying visible requires posting recently, not just having strong material sitting static on a profile.*

- **Posting your progress, in one line** — Publishing short, specific updates about real work on the platforms a recruiter already searches, to stay visible in recency-weighted feeds and search.
- **The Fenway scoreboard analogy** — A manual scoreboard updates inning by inning as the game happens, not just once at the final score - the same way visible progress needs to post as it happens, not only once when everything is finished.
- **How this differs from a learning changelog** — Posting your progress is narrower and more tactical - short, frequent, specific updates aimed at staying visible on recruiter-searched platforms during an active job search, not a deeper process-transparency habit.

### Challenge

Post one real, specific update about something you finished this week - two or three honest sentences, on the platform a recruiter is most likely to search. Note today's date so you can check the gap before your next one.

- [Merit America - How to Write LinkedIn Posts That Land You a Job](https://meritamerica.org/blog/linkedin-posts-that-land-you-a-job/)
- [Hootsuite - How the LinkedIn Algorithm Works](https://blog.hootsuite.com/linkedin-algorithm/)
- [What to post on LinkedIn during your job search to stand out to recruiters](https://www.youtube.com/watch?v=GsjypiG1wV0)

🎬 [What to post on LinkedIn during your job search to stand out to recruiters](https://www.youtube.com/watch?v=GsjypiG1wV0) (13 min)

- Recency of activity is its own visibility signal, separate from how strong a profile's content is - a quiet profile surfaces less often regardless of the real work behind it.
- A real update names something specific and checkable - a fixed bug, a finished module - not a vague feeling of progress.
- This is narrower than a learning changelog: short, frequent, specific posts aimed at staying visible on the exact platforms a recruiter searches during an active search.
- Visibility requires ongoing posting, not a one-time strong post - a profile's activity reads as stale again once posting stops, no matter how good the last post was.


## Related notes

- [[Notes/a-portfolio-that-gets-interviews/profiles/personal-brand-basics|Personal brand basics]]
- [[Notes/a-portfolio-that-gets-interviews/profiles/linkedin-for-qa|LinkedIn for QA]]
- [[Notes/resume-and-applications/certifications-honestly/learning-in-public|Learning in public]]


---
_Source: `packages/curriculum/content/notes/a-portfolio-that-gets-interviews/profiles/posting-your-progress.mdx`_
