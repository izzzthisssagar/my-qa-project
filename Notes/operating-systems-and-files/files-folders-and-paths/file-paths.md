---
title: "File paths"
tags: ["computer-basics", "files", "paths", "track-a"]
updated: "2026-07-10"
---

# File paths

*A path is a file's full address. Learn to read one, write one, tell absolute from relative, and survive the Windows-vs-everyone slash war — the single most reused skill in all of testing.*

> `C:\Users\Sajan\Documents\report.pdf` and `/home/sajan/Documents/report.pdf` are the
> same idea wearing different punctuation, and roughly 40% of all beginner automation
> failures are one of these two strings being slightly wrong. Not conceptually wrong.
> One-character wrong. Today you learn to read addresses so that when a test screams
> `FileNotFoundError`, you already know which character betrayed you.

> **In real life**
>
> A path is **a postal address for a file.** `Nepal → Kathmandu → Thamel → House 12`
> narrows the whole planet to one door, reading left to right, each step a smaller
> world. A path does exactly that: `/home/sajan/Documents/report.pdf` — from the root
> of everything, down through branches, to one file. Same as an address, a path is
> useless if you get one level wrong, and there's no postal worker to guess your intent.

## Reading an address

Take the tree from the last note and write a walk through it as text. That's a path.
Every path has three ingredients:

- **A starting point** — either the very top (`/` or `C:\`), or "wherever I am right now."
- **Separators** — the slashes between folder names. `/` on Mac/Linux, `\` on Windows.
- **The steps** — folder names, then finally the filename.

```
/home/sajan/Documents/QA/bug-reports/2026-07-10-login.md
│    │     │         │  │           └── the file
│    │     │         │  └── folder
│    │     │         └── folder
│    │     └── folder
│    └── your Home folder
└── the ROOT — the top of everything
```

![A file manager window with the path bar showing the current location as a trail of folder names](file-manager.png)
*Screenshot: GNOME Files — Wikimedia Commons, CC BY-SA 4.0. [Source](https://commons.wikimedia.org/wiki/File:GNOME_Files_47.png)*
- **The path bar IS a path, drawn as buttons** — Home › Documents › Projects. Press Ctrl+L (or click an empty part of the bar) and it flips into editable TEXT: /home/you/Documents/Projects. Same address, two costumes. Do this once and paths stop being scary forever.
- **Home — the shortcut that hides a path** — 'Home' is really /home/yourname (Linux), /Users/yourname (Mac), or C:\\Users\\yourname (Windows). The tilde ~ is shorthand for exactly this. Every 'Home' button is a path in disguise.
- **Each folder = one segment** — Double-clicking a folder appends one segment to your path. Going 'up' removes one. Browsing IS path editing — you've been writing paths with a mouse your whole life.
- **Search results have paths too** — Find a file by search, then check its Properties/Get Info: there's the full absolute path. That's how you answer 'where did that thing actually live?' — the question the next note automates.

## Absolute vs relative — the distinction that breaks tests

An **absolute path**: A path that starts at the root of the file system (/ on Mac/Linux, C:\ on Windows). It means the same file no matter where you're standing. Example: /home/sajan/report.pdf starts at the root and means one exact
file, always, from anywhere. A **relative path**: A path interpreted relative to the current working directory — where the program is 'standing'. Example: reports/july.pdf means 'a folder named reports, inside wherever I am now'. starts wherever the program
happens to be standing (its **working directory**) and means something different
depending on where that is.

- `/home/sajan/QA/tests/login.spec.ts` — absolute. Unambiguous. Long.
- `tests/login.spec.ts` — relative. Short. Depends entirely on where you run it from.
- `../screenshots/fail.png` — relative, with `..` meaning **"go up one folder."** (`.` means "right here.")

Relative paths are why a script works in your terminal and dies in CI: same command,
different working directory, so the same relative path resolves to a different place —
or to nothing.

**How a path gets resolved — press Play**

1. **📝 A program asks for `reports/july.pdf`** — No leading slash → it's RELATIVE. The OS cannot answer yet. It needs one more fact: where is this program standing?
2. **📍 Find the working directory** — Every running program has a 'current working directory' — the folder it considers HERE. Say it's /home/sajan/QA. Nothing about the path text told you this. It's context, not content.
3. **🔗 Join them** — /home/sajan/QA + reports/july.pdf → /home/sajan/QA/reports/july.pdf. The relative path just became absolute. This join happens millions of times a second and nobody thinks about it — until it goes wrong.
4. **🌲 Walk the tree** — Root → home → sajan → QA → reports → july.pdf. Each step: 'does this folder list that name?' One missing step = FileNotFoundError, naming the WHOLE path — which is why the error is actually a gift.
5. **💥 Now run it from Home instead** — Working directory changes to /home/sajan. Same text, now resolves to /home/sajan/reports/july.pdf — a file that doesn't exist. Script unchanged, result broken. THIS is the CI failure you'll debug a hundred times.

*Try it — take paths apart and put them back together*

```python
import os
from pathlib import PurePosixPath, PureWindowsPath

p = PurePosixPath("/home/sajan/Documents/QA/2026-07-10-login.md")
print("full:      ", p)
print("parent:    ", p.parent)       # the folder holding it
print("name:      ", p.name)         # filename with extension
print("stem:      ", p.stem)         # filename without extension
print("suffix:    ", p.suffix)       # the costume from note 1
print("parts:     ", p.parts)        # every segment of the walk
print()

# Absolute vs relative — the distinction that breaks CI:
for candidate in ["/home/sajan/report.pdf", "reports/july.pdf", "../shared/logo.png"]:
    kind = "ABSOLUTE" if candidate.startswith(("/", "C:")) else "relative"
    print(f"{candidate:26} -> {kind}")
print()

# Resolve a relative path against two different working directories:
rel = "reports/july.pdf"
for cwd in ["/home/sajan/QA", "/home/sajan"]:
    print(f"cwd={cwd:18} '{rel}' means -> {PurePosixPath(cwd) / rel}")
print("^ same text, two files. That is the whole bug, in two lines.")
print()

# Windows vs POSIX — never build paths with string concatenation:
print("Windows:", PureWindowsPath("C:/Users/Sajan") / "Documents" / "report.pdf")
print("POSIX:  ", PurePosixPath("/home/sajan") / "Documents" / "report.pdf")
print("os.sep on this machine:", repr(os.sep))
```

## The slash war (and how professionals dodge it)

- **Mac / Linux:** `/` separates, and there's ONE root: `/`. Everything, including USB sticks, hangs off it.
- **Windows:** `\` separates, and each drive has its own root: `C:\`, `D:\`. Also — Windows quietly accepts `/` in most places, which is why so much software gets away with it.

The backslash has a second job in most programming languages: it *escapes* characters
(`\n` = newline). So `"C:\new\table.txt"` in code contains a newline and a tab, not
folders. This is a genuinely famous bug.

> **Tip**
>
> The professional dodge: **never build a path by gluing strings together.** Use your
> language's path tools — `pathlib` / `os.path.join` in Python, `path.join` in Node,
> `Path` in Java. They pick the right separator for the machine they're running on. Your
> Playwright test then works on your Mac AND on the Linux CI runner, unchanged. This one
> habit prevents an entire genre of "works on my machine."

### Your first time: Your mission: say your own address out loud

- [ ] Reveal a real path — Open any folder. Windows: click the empty space in the address bar → it turns into text. Mac: View → Show Path Bar, or drag the folder into Terminal. Linux: Ctrl+L. Read your own address.
- [ ] Copy a file's absolute path — Windows: Shift+Right-click → 'Copy as path'. Mac: right-click → hold Option → 'Copy as Pathname'. Paste it somewhere. That string is the file's true name.
- [ ] Spot your Home path — Find where 'Home' really lives: /home/you, /Users/you, or C:\\Users\\you. Everything you own is a branch of that one address.
- [ ] Run the playground above — Watch 'reports/july.pdf' resolve to two different files under two working directories. That's the CI bug, seen before you ever meet it.
- [ ] Find a `..` in the wild — Look at any project's config or import statements. `../` means 'up one'. Once you see it, you can read any relative path anywhere.

You can now read, copy, and resolve an address. Paths are no longer a wall of punctuation.

- **FileNotFoundError: 'data/users.csv' — but the file is RIGHT THERE.**
  It's right there relative to YOU; the program is standing somewhere else. Print the working directory first (`os.getcwd()` / `pwd` / `process.cwd()`) — nine times out of ten it's the repo root, not the folder holding your script. Fix: use a path anchored to the script's own location, or run from the directory the tool expects. Read the error's full path: it TELLS you where it looked.
- **My script works locally and fails on CI with a path error.**
  Same relative path, different working directory (and often different OS). Two-part fix: build paths with pathlib/path.join instead of string concatenation, and anchor to a known root rather than to 'wherever I happen to be'. This is the single most common CI-vs-local difference in test automation, and now it's not mysterious.
- **My Windows path in code produces garbage: 'C:\
ew\\table.txt' behaves weirdly.**
  `\
` and `\\t` are escape sequences (newline, tab) in most languages — your path literally contains control characters. Fix: use a raw string (r"C:\
ew") , double the backslashes, or just use forward slashes (Windows accepts them). Better: don't hand-write it at all — join with a path library.
- **A path with spaces breaks in the terminal: 'No such file: My'**
  The shell split your path at the space and thought 'My' was the whole filename. Quote it: "My Documents/file.pdf", or escape the space (My\\ Documents). This is exactly why the last note said 'name files with hyphens, no spaces' — chapter 5's command line will make you grateful.

### Where to check

Where paths surface in a tester's day, constantly:

- **The path bar / address bar** — press Ctrl+L (or the Mac/Windows equivalents) to flip it to text. Instant absolute path.
- **Properties / Get Info** — the 'Location' field is the parent folder's absolute path.
- **Any error message with a filename in it** — it usually prints the FULL path it tried. Read it against the tree: which segment doesn't exist? That's your bug, located for free.
- **Terminal `pwd`** (print working directory) — the answer to "where is this program standing," which is half of every relative-path mystery.
- **Test config files** — `testDir: './tests'`, `screenshot: 'test-results/'`. Relative paths, all of them, resolved against the config file or the working directory. Knowing which is knowing why your screenshots landed somewhere odd.

The habit: when anything says "not found," don't re-check that the file exists. Check
**which path it actually used.** The file is fine. The address was wrong.

### Worked example: the screenshot that landed in the wrong universe

A real, unremarkable, extremely common debugging session:

1. **Symptom:** a Playwright test saves `screenshot('results/fail.png')`. Locally the file appears. On CI, the "upload artifacts" step finds nothing.
2. **First instinct (wrong):** "CI deleted my file." Nothing was deleted.
3. **The check:** print the working directory in both places. Locally: `/Users/sajan/qa/e2e`. On CI: `/home/runner/work/repo/repo`. The relative path `results/fail.png` resolved to two totally different absolute addresses.
4. **The evidence:** the artifact step was told to look in `e2e/results/` — which exists locally and never existed on CI, because CI stood one level higher.
5. **The fix:** anchor the path to the config's directory instead of the working directory, and the artifact step points at the same anchor. Passing on both.
6. **The moral:** the file was created successfully every single time. Nothing was ever missing. Two different answers to "where is here?" produced two different files, and only one place looked. Absolute vs relative isn't trivia — it's a debugging superpower.

> **Common mistake**
>
> Assuming "the file isn't there" when a program says it can't find it. The program
> almost never lies about *looking* — it tells you the exact path it tried, and beginners
> skim past that line to go check the folder with their eyes. Read the path in the error,
> character by character, against the tree. Wrong separator? Missing segment? Relative
> when you meant absolute? A typo'd folder name? The error already did the investigation
> and handed you the report. Actually read it.

**Quiz.** A script contains `open('data/input.csv')`. It works when run from /home/sajan/project, but fails from /home/sajan. Why, and what's the professional fix?

- [ ] The file got deleted; restore from Trash
- [x] 'data/input.csv' is RELATIVE — it resolves against the working directory. From /home/sajan it means /home/sajan/data/input.csv, which doesn't exist. Fix: anchor the path to a known root (e.g. the script's own location) or build it with a path library instead of assuming where you're standing.
- [ ] CSV files can only be opened from their own folder
- [ ] The slash direction is wrong for this OS

*No leading slash = relative = 'join me to the current working directory.' Change where you stand, change which file that text names. The fix is never 'cd to the right place and hope' — it's anchoring the path to something stable (the script's location, a config-relative root) so the same code resolves identically on your laptop and on the CI runner.*

- **What is a path?** — A file's full address: a walk through the folder tree written as text, separated by / (Mac/Linux) or \\ (Windows).
- **Absolute vs relative** — Absolute starts at the root (/ or C:\\) and means one file from anywhere. Relative starts at the working directory — same text, different file depending on where you stand.
- **. and ..** — `.` = the current folder. `..` = go up one level. `../screenshots/a.png` = up one, then into screenshots.
- **The #1 CI path bug** — A relative path resolving against a different working directory on CI than locally. Fix: build paths with pathlib/path.join, anchored to a stable root.
- **Why \\ hurts in code** — Backslash escapes characters (\
 = newline). "C:\
ew" contains a newline, not a folder. Use raw strings, forward slashes, or a path library.
- **Debugging 'file not found'** — Don't check the folder — read the FULL path in the error. It tells you exactly where the program looked. The file is fine; the address was wrong.

### Challenge

Copy the absolute path of any file on your machine (Shift+Right-click → Copy as path,
or Option+right-click → Copy as Pathname). Paste it somewhere and annotate every
segment: which is the root, which is Home, which are folders, which is the name, which
is the extension. Then write the same file's path *relative to your Home folder*. If
you can do both, you can debug 40% of automation failures you'll ever meet, and you
haven't written a line of test code yet.

### Ask the community

> Path question: my program says [exact error, WITH the full path it printed]. My working directory is [output of pwd/cwd]. The file actually lives at [absolute path]. I expected the relative path [x] to resolve to [y].

Notice this template forces you to gather the three facts that solve it: the path it
tried, where it was standing, and where the file really is. Half the time you'll spot
the mismatch while typing the question and never hit send. That's not wasted effort —
that's the method working.

- [Wikipedia — paths, absolute and relative, across OSes](https://en.wikipedia.org/wiki/Path_(computing))
- [Python pathlib — the right way to build paths in code](https://docs.python.org/3/library/pathlib.html)
- [Absolute vs relative paths, explained visually](https://www.youtube.com/watch?v=ephId3mYu9o)

🎬 [Absolute vs relative paths](https://www.youtube.com/watch?v=ephId3mYu9o) (7 min)

- A path is a file's address: a walk down the folder tree, written as text with separators (/ on Mac+Linux, \\ on Windows).
- Absolute paths start at the root and mean one file from anywhere; relative paths resolve against the working directory — same text, different file.
- `.` = here, `..` = up one level. Relative paths + a changed working directory = the most common CI-vs-local test failure there is.
- Never build paths by gluing strings; use pathlib / path.join so the separator and root are correct on every OS.
- When something is 'not found', read the full path in the error rather than checking the folder. The program tells you exactly where it looked.


---
_Source: `packages/curriculum/content/notes/operating-systems-and-files/files-folders-and-paths/file-paths.mdx`_
