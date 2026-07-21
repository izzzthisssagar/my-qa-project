---
title: "Building a matrix"
tags: ["mobile-testing", "device-and-os-matrix", "track-c"]
updated: "2026-07-20"
---

# Building a matrix

*Turn fragmentation into a short, defensible list of devices and OS versions to test, chosen from real usage and risk data instead of guesswork or brand loyalty.*

> Nobody can test every device and OS-version combination in the world, and pretending otherwise just
> produces a spreadsheet nobody trusts. The teams who catch real device bugs are not the ones with the
> longest device list — they are the ones whose short list was chosen on purpose.

> **In real life**
>
> A city traffic engineer cannot put a camera on every intersection in town. Instead, the decision is
> built from data: which intersections carry the most traffic, and which ones have the worst accident
> history. A handful of intersections chosen that way catch far more real problems than a much longer list
> picked at random or based on which ones look important from the highway. A device matrix works the same
> way — a small, evidence-backed selection beats a long, arbitrary one.

**A device matrix**: A device and OS matrix is a documented, risk-based selection of device models and OS-version rows, built from real usage analytics and known failure risk, so that a bounded amount of testing effort covers the combinations most likely to matter and most likely to fail.

## Choose rows from evidence, not habit

Start from real product analytics: which device models, screen sizes, and OS versions your actual users
run today. Layer in supported-OS policy (the oldest version you still claim to support) and known risk —
older OS versions with fewer platform safety nets, budget hardware with less memory, and any device class
that has caused problems before. A good matrix deliberately mixes low-end and high-end hardware, common
mid-range screen sizes, and both the newest and oldest OS versions still inside your support window,
rather than clustering around whatever device the team happens to own.

> **Tip**
>
> Score candidate rows on two axes — how many real users a combination represents, and how likely it is to
> fail or to have failed before — then take the highest-scoring rows first. A device with modest usage but a
> history of OEM-specific bugs can outrank a more popular device with a clean track record.

> **Common mistake**
>
> Do not build the matrix around the QA team's personal phones or the newest flagship in the office. Those
> devices have the most RAM, the newest OS, and the fewest quirks — they are the least representative rows
> you could pick, even though they are the easiest ones to reach for.

![A speech-bubble-shaped illustration densely filled with dozens of small, distinct human silhouette icons representing a large and varied population of people](building-a-matrix.jpg)
*Crowdtesting, Crowdsourcing — Testbirds GmbH, Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:Crowdtesting.jpg)*
- **The full population you cannot cover** — Every distinct silhouette stands in for a device and OS-version combination that theoretically exists in your audience.
- **No two rows are identical** — Just as no two silhouettes are drawn the same, no two devices behave identically — selection has to be deliberate, not a single representative stand-in.
- **You still can't test everyone** — The crowd is the reason a matrix exists at all: the population is too large to cover exhaustively, so the selection itself is the skill.
- **Where the outline points** — The bubble's tail aims the whole crowd toward one destination — the same way a risk-based matrix points a huge population toward a short, chosen list of test rows.

**Building a matrix from data**

1. **Pull usage analytics and support policy** — Real device/OS-version share and the oldest OS version you still commit to supporting.
2. **Score each candidate row for usage and risk** — Weight both how common a combination is and how likely it is to expose a defect.
3. **Select rows above a deliberate threshold** — Take the highest-scoring combinations first instead of an arbitrary fixed count.
4. **Re-score on a schedule** — Usage share and risk both drift; an unreviewed matrix silently goes stale.

*A risk-based matrix-builder (Python)*

```python
rows = [
    {"device": "pixel8_android15", "usage": 0.22, "risk": 0.30},
    {"device": "galaxyS23_android14", "usage": 0.18, "risk": 0.20},
    {"device": "galaxyA14_android13", "usage": 0.15, "risk": 0.60},
    {"device": "iphone15_ios18", "usage": 0.20, "risk": 0.20},
    {"device": "iphone12_ios17", "usage": 0.12, "risk": 0.50},
    {"device": "redmiNote12_android13", "usage": 0.13, "risk": 0.70},
]
threshold = 0.25
selected = []
for row in rows:
    score = round(row["usage"] * 0.6 + row["risk"] * 0.4, 2)
    status = "SELECTED" if score >= threshold else "SKIPPED"
    if score >= threshold:
        selected.append(row["device"])
    print(row["device"] + "=" + str(score) + "=" + status)
print("SELECTED_COUNT=" + str(len(selected)))
result = "PASS" if len(selected) >= 4 else "FAIL"
assert result == "PASS", "matrix too small for risk-based coverage"
print("RESULT=" + result)
```

*A risk-based matrix-builder (Java)*

```java
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        String[] names = {
            "pixel8_android15", "galaxyS23_android14", "galaxyA14_android13",
            "iphone15_ios18", "iphone12_ios17", "redmiNote12_android13"
        };
        double[] usage = {0.22, 0.18, 0.15, 0.20, 0.12, 0.13};
        double[] risk  = {0.30, 0.20, 0.60, 0.20, 0.50, 0.70};
        double threshold = 0.25;

        List<String> selected = new ArrayList<>();
        for (int i = 0; i < names.length; i++) {
            double raw = usage[i] * 0.6 + risk[i] * 0.4;
            double score = Math.round(raw * 100) / 100.0;
            String status = score >= threshold ? "SELECTED" : "SKIPPED";
            if (score >= threshold) selected.add(names[i]);
            System.out.println(names[i] + "=" + score + "=" + status);
        }
        System.out.println("SELECTED_COUNT=" + selected.size());
        String result = selected.size() >= 4 ? "PASS" : "FAIL";
        if (!result.equals("PASS")) throw new AssertionError("matrix too small for risk-based coverage");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Build a first risk-based matrix

- [ ] Gather usage analytics and support policy — List real device/OS-version share and the oldest OS version still officially supported.
- [ ] Score usage and risk per candidate row — Combine how common a combination is with how likely it is to expose a defect.
- [ ] Select rows above a stated threshold — Pick by score, not by a round number of devices someone guessed at a meeting.
- [ ] Write down why each row is in — A one-line justification per row keeps the matrix defensible when someone asks why a device is missing.

- **The matrix keeps growing every sprint.**
  Re-score against the threshold instead of only adding rows; retire low-scoring rows on purpose so the list stays a decision tool.
- **A widely-reported bug wasn't caught by the matrix.**
  Check whether the failing combination scored below threshold by mistake — usage or risk data may be stale and need refreshing.
- **Stakeholders keep asking for one more device.**
  Ask for the usage or risk evidence behind the request; add it to the scoring model instead of the list directly.

### Where to check

- Product analytics for device model, OS version, and screen-size share.
- Written supported-OS policy and its oldest still-supported version.
- Prior defect history segmented by device and OS version.
- [[mobile-testing/device-and-os-matrix/fragmentation]] for the underlying spread a matrix is built to cover.

### Worked example: a mid-tier device that outranked a flagship

1. A budget Android device has lower usage share than the team's flagship test phone.
2. Its risk score is higher: it has a history of memory-related crashes and an OEM skin the team doesn't
   own a unit of.
3. Its combined score clears the threshold while a higher-usage but low-risk device does not.
4. The budget device earns a matrix row, and testing on it catches a low-memory crash the flagship never
   would have reproduced.

**Quiz.** What should primarily drive which rows enter a device matrix?

- [ ] Whichever devices the QA team already owns
- [ ] The newest flagship device on each platform
- [x] Real usage analytics combined with known or likely risk
- [ ] An arbitrary fixed number of devices picked in a meeting

*A defensible matrix scores rows on real usage and risk evidence and takes the highest-scoring combinations, rather than relying on convenience or habit.*

- **Matrix selection basis** — Real usage analytics combined with known or likely risk, scored per candidate row.
- **Common matrix mistake** — Building the list around the team's own devices or the newest flagship, which hides low-memory and older-OS failures.
- **Matrix maintenance** — Re-score on a schedule; usage share and risk both drift, so an unreviewed matrix goes stale.

### Challenge

Score five real devices from your product's analytics on usage and risk, apply a threshold, and justify in one line each why the selected rows made the cut.

- [BrowserStack — Building an Effective Device Matrix for Mobile App Testing](https://www.browserstack.com/guide/device-matrix-for-mobile-app-testing)
- [BrowserStack — How to Select Mobile Devices for Testing](https://www.browserstack.com/guide/how-to-select-mobile-devices-for-testing)
- [Manual QA: Testing for Beginners — Mobile Testing Specifics (Part 25)](https://www.youtube.com/watch?v=JfUqZr6jLSE)

🎬 [Manual QA: Testing for Beginners — Mobile Testing Specifics (Part 25)](https://www.youtube.com/watch?v=JfUqZr6jLSE) (13 min)

- A device matrix is a deliberate, risk-based selection, not an exhaustive or arbitrary device list.
- Score candidate rows on real usage share and known or likely risk, then take the highest scorers.
- Deliberately mix low-end and high-end hardware and both new and old still-supported OS versions.
- Re-score the matrix on a schedule; usage and risk both drift as the real audience changes.


## Related notes

- [[Notes/mobile-testing/device-and-os-matrix/fragmentation|Fragmentation]]
- [[Notes/mobile-testing/device-and-os-matrix/real-vs-emulated|Real vs emulated]]
- [[Notes/mobile-testing/device-and-os-matrix/device-farms|Device farms]]


---
_Source: `packages/curriculum/content/notes/mobile-testing/device-and-os-matrix/building-a-matrix.mdx`_
