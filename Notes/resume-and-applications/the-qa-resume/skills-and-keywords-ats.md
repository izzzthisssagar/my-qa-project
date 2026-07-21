---
title: "Skills & keywords (ATS)"
tags: ["resume-and-applications", "the-qa-resume", "track-c"]
updated: "2026-07-20"
---

# Skills & keywords (ATS)

*Applicant tracking systems match resumes against a job description's exact wording before a human ever opens the file - plain formatting and honest, precise phrasing both matter.*

> Many resumes never reach a human reader first. An applicant tracking system (ATS) parses the file, extracts
> text, and ranks or filters candidates against the job description before anyone on the hiring side sees a
> name. A resume that reads perfectly to a person can still fail this first, mechanical pass.

> **In real life**
>
> An ATS behaves like a literal-minded translation engine, not a bilingual colleague. Feed it the exact
> phrase it expects and the meaning passes through cleanly. Feed it a synonym, an idiom, or your own
> inventive way of describing the same skill, and the meaning can get lost in translation entirely - even
> though a person fluent in both phrasings would have understood you instantly.

**Applicant tracking system (ATS)**: Software that scans, parses, and ranks resumes against a job description's keywords and requirements before a human recruiter reviews them, often rejecting or down-ranking resumes whose formatting cannot be parsed or whose wording does not match expected terms.

## What the system is actually matching

Most ATS platforms extract plain text from the uploaded file and search it for terms pulled from the job
description - tool names, methodologies, certifications, years of experience. A resume that says "test
automation" scores differently than one that says only "automation," even to a human those read as the
same skill. The fix is not padding the page with every buzzword; it is mirroring the job description's
exact phrasing for skills you genuinely have, in the summary, skills list, and experience bullets.

## Format so a machine can read it

Tables, text boxes, multi-column layouts, headers/footers, and skills embedded in images frequently parse
as garbled text or get dropped entirely. Use a single column, standard section headings ("Experience,"
"Skills," "Education"), and plain bullet points. Save as a standard PDF or .docx unless the job posting
says otherwise. None of this changes what a human sees when they open a well-formatted file - it only
protects the machine's ability to read the same content.

> **Tip**
>
> Read the job description and note its exact terms for your tools and methods. If it says "API testing"
> and your resume says "backend testing," a keyword match may fail even though the skill is identical.

> **Common mistake**
>
> Do not list a skill or tool you cannot discuss in an interview just to pass a keyword scan. Getting past
> the ATS only to fail the first technical question wastes everyone's time, including yours.

![A hand marking a green checkmark over one silhouette figure and red X marks over five others in a row, representing an automatic first-pass filter](skills-and-keywords-ats.jpg)
*Choosing A Job Applicant.jpg — CIPHR Connect, Wikimedia Commons, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Choosing_A_Job_Applicant.jpg)*
- **One mechanical match** — Only the figure whose profile matched the expected terms gets marked through - a pass, not a judgment of overall quality.
- **Rejected before being read** — Most of the row is marked out at this stage; a qualified candidate phrased differently can land on this side of the line.
- **The mark is automatic** — The hand stands in for a rule, not a considered read - real ATS scoring runs the same way, without judgment or context.
- **Every applicant looks identical to the filter** — The silhouettes are interchangeable; a parser reads extracted text fields the same way, blind to anything a table or image hid from it.

**What happens before a human opens the file**

1. **Resume uploaded** — The file is parsed into plain text, stripping layout, images, and any content the parser cannot read.
2. **Text matched against the job description** — Required skills, tools, and years of experience are searched for as terms in the extracted text.
3. **Resume ranked or filtered** — Low-matching resumes may be down-ranked or excluded before a recruiter's queue ever shows them.
4. **A human reviews the survivors** — Only resumes that passed the mechanical stage typically reach a person's attention next.

*An ATS keyword-match scorer (Python)*

```python
job_keywords = ["selenium", "test automation", "api testing", "jira", "regression testing", "sql", "agile"]
resume_text = ("Automated regression testing with Selenium and integrated API testing suites. "
               "Tracked defects in Jira within an Agile team. Wrote SQL queries for data validation.")

resume_lower = resume_text.lower()
matched = [k for k in job_keywords if k in resume_lower]

for k in job_keywords:
    status = "MATCHED" if k in matched else "MISSING"
    print(k + "=" + status)

score = round(100 * len(matched) / len(job_keywords))
print("SCORE=" + str(score))
result = "PASS" if score >= 70 else "FAIL"
assert result == "PASS", "ATS keyword match below threshold"
print("RESULT=" + result)
```

*An ATS keyword-match scorer (Java)*

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> jobKeywords = Arrays.asList("selenium", "test automation", "api testing", "jira", "regression testing", "sql", "agile");
        String resumeText = "Automated regression testing with Selenium and integrated API testing suites. "
                + "Tracked defects in Jira within an Agile team. Wrote SQL queries for data validation.";
        String resumeLower = resumeText.toLowerCase();

        List<String> matched = new ArrayList<>();
        for (String k : jobKeywords) if (resumeLower.contains(k)) matched.add(k);

        for (String k : jobKeywords) {
            String status = matched.contains(k) ? "MATCHED" : "MISSING";
            System.out.println(k + "=" + status);
        }

        long score = Math.round(100.0 * matched.size() / jobKeywords.size());
        System.out.println("SCORE=" + score);
        String result = score >= 70 ? "PASS" : "FAIL";
        if (!result.equals("PASS")) throw new AssertionError("ATS keyword match below threshold");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Run your resume through a keyword check before applying

- [ ] Paste the job description into a plain-text file — Highlight tool names, methodologies, and required years of experience mentioned explicitly.
- [ ] Compare that list against your resume's exact wording — Note any skill you have but phrased differently than the posting.
- [ ] Rewrite matching terms in, honestly — Only where the skill is real - do not add tools you cannot back up in an interview.
- [ ] Strip risky formatting — Remove tables, text boxes, and multi-column layouts; confirm the file opens as clean plain text when copied out.

- **You never hear back despite matching qualifications.**
  Copy your resume's text into a plain text editor - if sections are jumbled or missing, the ATS likely saw the same garbled version.
- **A skill you have is never recognized.**
  Check the job description's exact phrase and mirror it once in your resume, in addition to any synonym you already used.
- **The resume feels like a keyword list, not a story.**
  Keep keywords inside real sentences describing what you did and the outcome, not a bare comma-separated dump.

### Where to check

- Copy the resume file's text into a plain editor and confirm every section still reads in order.
- Cross-reference the job description's required tools and methods against your skills and experience wording.
- Confirm every listed skill is one you could discuss for several minutes in an interview.
- [[resume-and-applications/the-qa-resume/common-mistakes]] for why keyword-stuffing a skill you cannot back up creates a worse problem later.

### Worked example: matching a job description's exact terms

1. A job posting requires "API testing" and "regression testing" experience.
2. A candidate's resume says "backend testing" and "re-running test suites" - true to the work, but different wording.
3. The candidate rewrites one bullet to state "API testing" and one to state "regression testing," describing the same real work.
4. The resume now matches both required terms while still being an accurate description of what was done.

**Quiz.** What is the most reliable way to pass an ATS keyword check honestly?

- [ ] List every tool you have ever heard of
- [x] Mirror the job description's exact terms for skills you genuinely have
- [ ] Use a scanned image of your resume for a unique look
- [ ] Put all skills in a decorative sidebar table

*Matching exact phrasing for real skills gets past the parser without misrepresenting anything; buzzword stuffing and risky formatting both tend to backfire.*

- **What an ATS scores** — Extracted plain text matched against job-description keywords - tools, methods, certifications, and phrasing.
- **Formatting risk** — Tables, columns, text boxes, and image-embedded text often parse as garbled or missing content.
- **Honest keyword use** — Mirror the job posting's exact wording only for skills you can discuss in an interview.

### Challenge

Take one job posting you want to apply to. List its required keywords, then check your resume's exact wording against each one and rewrite any mismatches honestly.

- [Indeed — Get Your Resume Seen With ATS Keywords](https://www.indeed.com/career-advice/resumes-cover-letters/ats-resume-keywords)
- [Coursera — Resume Keywords: How to Find the Right Words to Beat the ATS](https://www.coursera.org/articles/resume-keywords)
- [ATS Friendly Resume In 6 Minutes](https://www.youtube.com/watch?v=mZb_nkXOLRs)

🎬 [ATS Friendly Resume In 6 Minutes](https://www.youtube.com/watch?v=mZb_nkXOLRs) (6 min)

- Most resumes are parsed by software before a human ever opens them.
- Mirror the job description's exact wording for skills you genuinely have; do not invent them.
- Avoid tables, columns, and image-embedded text that can break plain-text parsing.
- Passing the ATS is only the first gate - never list a skill you cannot discuss afterward.


## Related notes

- [[Notes/resume-and-applications/the-qa-resume/structure-that-works|Structure that works]]
- [[Notes/resume-and-applications/the-qa-resume/numbers-and-impact|Numbers & impact]]
- [[Notes/resume-and-applications/the-qa-resume/common-mistakes|Common mistakes]]


---
_Source: `packages/curriculum/content/notes/resume-and-applications/the-qa-resume/skills-and-keywords-ats.mdx`_
