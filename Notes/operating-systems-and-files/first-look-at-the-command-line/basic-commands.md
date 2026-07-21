---
title: "Basic commands"
tags: ["computer-basics", "command-line", "track-a"]
updated: "2026-07-10"
---

# Basic commands

*Twelve commands cover ninety percent of a working day. Learn the grammar they all share, the flags that change their meaning, and the two that can ruin your afternoon.*

> You do not need to memorize four hundred commands. You need twelve, plus one grammar
> rule, plus the humility to run `--help` before running something with `-rf` in it.
> That's the entire syllabus. People who look fluent in a terminal aren't recalling more
> commands than you — they're recalling the *same twelve*, faster, and they read the
> error messages.

> **In real life**
>
> Commands are **verbs, and flags are adverbs.** `copy` is a verb. `copy --recursively`
> is copy, but *thoroughly, into every subfolder*. `remove --force` is remove, but
> *without asking*. Learn the verbs and you can speak; learn what the adverbs do and you
> stop accidentally shouting. The disasters in this note are all adverbs: the verb was
> fine, the adverb was `--force`, and nothing asked whether you were sure.

## The grammar (one rule, then you can read any command)

```
command  -flags  targets
   ls      -la    Documents
   │        │        └── what to act on
   │        └── how to do it (options)
   └── the verb
```

Flags come in two shapes: **short** (`-l`, one dash, one letter, stackable as `-la`)
and **long** (`--long`, two dashes, a whole word, self-documenting). `-h` and `--help`
are the same idea, and `--help` is the most underused key on your keyboard.

Everything after the command name — flags and targets alike — is an **argument**: The words you pass to a command after its name. Flags (starting with - or --) change HOW it behaves; the rest are targets, the things it acts on. The shell splits them on spaces, which is why filenames with spaces need quotes., and the shell hands the whole list to the program to interpret.

![A terminal showing typed commands with flags and their text output](terminal.png)
*Screenshot: GNOME Terminal running bash — Wikimedia Commons, GPL. [Source](https://commons.wikimedia.org/wiki/File:Linux_command-line._Bash._GNOME_Terminal._screenshot.png)*
- **The verb — always the first word** — `ls`, `cd`, `cat`, `cp`. Short because you type them a thousand times a day. Unix names are terse for the same reason your friends have nicknames — frequency compresses language.
- **The flags — how, not what** — `-l` = long listing, `-a` = all (including hidden). `-la` stacks them. Every flag is documented in `man ls` or `ls --help`. Nobody memorizes flags; everybody looks them up. Looking things up IS the skill.
- **The output — text you can capture** — This isn't a picture of your files, it's TEXT. Which means it can be searched, saved to a file, piped into another command, or diffed against yesterday's. That capability is why the terminal outlives every GUI.
- **Exit code — the invisible answer** — Every command returns a number you don't see: 0 = success, anything else = a specific failure. `echo $?` prints it. Your entire CI pipeline is built on this one number, and it's the reason a test suite can 'fail the build'.
- **Errors go to a SEPARATE stream** — Normal output (stdout) and errors (stderr) are two different pipes that both land on your screen. That's why you can save output to a file and STILL see errors printed. Confusing until you know; obvious after.

## The twelve

**Looking around**
- `pwd` — where am I?
- `ls` (`dir` on PowerShell) — what's here? Try `ls -la`.
- `cat file` — print a file's contents. `less file` for long ones (`q` to quit).

**Moving and changing**
- `cd folder` — go there. `cd ..` up one. `cd` alone → Home.
- `mkdir name` — make a folder.
- `cp a b` — copy. `cp -r` for folders.
- `mv a b` — move **and** rename (same operation — the folders note explained why).
- `rm file` — delete. **No trash. No undo.** See the mistake callout, seriously.

**Finding and understanding**
- `grep pattern file` — find lines matching a pattern. The tester's crowbar.
- `find . -name "*.log"` — find files by name, walking down from here.
- `man command` / `command --help` — the manual. Read it *before* you need it.
- `history` — everything you've typed. Your own lab notebook.

**Anatomy of `rm -rf old-logs/` — press Play (and pay attention)**

1. **🔤 The shell splits the line** — Words: `rm`, `-rf`, `old-logs/`. Verb, flags, target. Nothing has happened yet — this is just parsing.
2. **🚩 `-r` = recursive** — 'Descend into folders and act on everything inside, all the way down.' Without it, `rm` refuses to delete a folder at all. That refusal is a safety feature you are now switching off.
3. **🚩 `-f` = force** — 'Do not ask me anything. Do not warn me. Do not stop on errors.' Combined with `-r`, you have asked for: delete everything below this point, silently, without confirmation.
4. **🎯 The target decides your fate** — `old-logs/` — fine, that's the job. `/` — you have just asked the machine to delete every file it can reach. Same verb, same adverbs. The only difference is one character in the target.
5. **💀 It obeys instantly** — No trash, no undo, no 'are you sure'. The terminal's obedience is exactly what makes it automatable, and exactly what makes this command famous. Read the TARGET before you press Enter. Check `pwd` first. Every engineer who skipped that has a story.

*Try it — build `grep`, the tester's most-used command*

```python
log = """2026-07-10 09:12:03 INFO  user 41 logged in
2026-07-10 09:12:44 INFO  cart updated
2026-07-10 09:13:01 ERROR checkout failed: payment gateway timeout
2026-07-10 09:13:02 INFO  retry scheduled
2026-07-10 09:13:59 ERROR checkout failed: payment gateway timeout
2026-07-10 09:15:10 WARN  slow query: 1400ms
"""

def grep(pattern, text, invert=False, count=False, ignore_case=False):
    lines = text.strip().split("\\n")
    def match(l):
        hay, needle = (l.lower(), pattern.lower()) if ignore_case else (l, pattern)
        return (needle in hay) != invert          # -v inverts the test
    hits = [l for l in lines if match(l)]
    return len(hits) if count else hits

print("$ grep ERROR app.log")
for l in grep("ERROR", log): print("   ", l)
print()
print("$ grep -c ERROR app.log        ->", grep("ERROR", log, count=True), "matching lines")
print("$ grep -v INFO app.log         (everything that is NOT routine chatter)")
for l in grep("INFO", log, invert=True): print("   ", l)
print()
print("$ grep -i error app.log        ->", grep("error", log, ignore_case=True, count=True), "(case-insensitive)")
print()
print("Three flags, three different questions, one verb. That's the whole")
print("command line: a small vocabulary of verbs, sharpened by adverbs.")
print("Real testers run exactly this against real logs, all day.")
```

> **Tip**
>
> `--help` before `-rf`. Every single time. `rm --help`, `cp --help`, `find --help` —
> they print in under a second and they are written by the people who wrote the command.
> Fluency is not memorizing flags; it's the reflex of checking one *before* the
> irreversible command, not after. Also: `history` is your lab notebook. Ran something
> clever three days ago? `history | grep pytest` finds it. You've been keeping a log of
> your own work without noticing.

### Your first time: Your mission: run all twelve, break nothing

- [ ] Make a safe playground — `mkdir ~/cli-practice && cd ~/cli-practice`. Everything you do next happens here. Check `pwd` to confirm you're standing in it — that habit is the whole safety story.
- [ ] Create and inspect — `echo hello > note.txt` then `cat note.txt` then `ls -la`. You've created a file, read it, and listed the folder including hidden entries.
- [ ] Copy, move, rename — `cp note.txt copy.txt`, then `mv copy.txt renamed.txt`. Notice mv did both jobs. `ls` to confirm. This is the folders chapter, in text.
- [ ] Grep something real — `ls -la | grep txt` — the `|` pipes ls's output INTO grep. Two verbs, one sentence. This is the moment the terminal beats the GUI and you can feel it.
- [ ] Read a manual before deleting — `rm --help` (or `man rm`). Find what `-i` does. Then delete your practice files with `rm -i *.txt` — it asks before each one. Interactive delete is the flag nobody teaches beginners, and it should be the first one they learn.

Twelve verbs, a pipe, and a delete that asked permission. Nothing exploded.

- **`rm: cannot remove 'folder': Is a directory`**
  `rm` refuses folders by default — a deliberate safety rail. It wants `-r` (recursive) to descend into it. Before you add that flag, run `ls folder` and look at what's inside. The refusal is the OS giving you one free chance to check the target. Take it.
- **I deleted the wrong thing with `rm`. Where's the Trash?**
  There isn't one. `rm` unlinks the file immediately — no Trash, no undo, no confirmation. This is the single most important fact in this note. Recovery means backups (or expensive forensics). Prevention: `rm -i` to be asked each time, `ls` the target first, and check `pwd` before anything destructive. Learn this from the paragraph rather than from the experience.
- **`cd Documents` — 'no such file or directory' — but I can SEE Documents!**
  Three candidates. (1) Case: Linux is case-sensitive, `documents` ≠ `Documents`. (2) You're not standing where you think — run `pwd`. (3) A space in the name: `cd My Documents` passes two arguments; quote it. Same relative-path lesson from chapter 3, now with a shell splitting on spaces.
- **The command printed a wall of text and scrolled past everything.**
  Pipe it into a pager or a filter: `command | less` (q to quit), `command | head -20` (first 20 lines), or `command | grep error` (only the lines that matter). Piping is the terminal's superpower: every command's output can become another command's input. That's why text-only turned out to be a feature.

### Where to check

Before any command you can't undo:

- **`pwd`** — am I standing where I think? Most `rm` disasters are correct commands in the wrong directory.
- **`ls <target>`** — what am I actually about to act on? Look before you leap, one command.
- **`--help` / `man`** — what does this flag really do? Written by the authors, prints instantly.
- **`echo $?`** — the exit code of the last command. `0` = success. Non-zero = failure, and the number often means something specific. Your entire CI pipeline is built on this.
- **`history`** — what did I actually run? Not what you *think* you ran. Essential when reproducing your own bug.

Tester's habit: build the destructive command with `echo` in front of it first (`echo
rm -rf old-logs/`). The shell expands everything — wildcards, variables, the lot — and
*prints* what it would run without running it. See the real target list, then remove
`echo` and press up-arrow. Zero cost, total protection.

### Worked example: finding the failing test in a 40,000-line log

CI failed. The log is 40,000 lines. This is a daily task, and it takes four commands:

1. **`grep -c FAIL results.log`** → `3`. Three failures. Now you know the scale before you read anything. Never open a huge log blind.
2. **`grep FAIL results.log`** → the three lines, with test names. Ten seconds in, you know *what* failed.
3. **`grep -B5 -A10 "test_checkout" results.log`** → the failing test's line plus 5 lines before and 10 after: setup, the assertion, the stack trace. `-B` and `-A` mean before and after. This is the flag pair that turns grep from a search into an investigation.
4. **`grep FAIL results.log > failures.txt`** → save just the failures to a file. `>` redirects output. Attach it to the bug ticket. Reproducible, small, exactly the evidence a developer needs.
5. **What a GUI user did instead:** opened the log in an editor, scrolled, used Ctrl+F, lost their place, screenshotted a fragment, and pasted the picture into Slack — a picture no one can search, grep, or diff.
6. Same log, same failures, four commands versus twenty minutes. **The command line isn't faster because it's arcane. It's faster because text composes and pictures don't.**

> **Common mistake**
>
> Running `sudo` because a command failed with 'permission denied', without reading why.
> `sudo` doesn't fix the command — it removes the guardrail that stopped it. Combine that
> with `rm -rf` and a mistyped path and there is no force on the machine that will
> protect you: you have explicitly told it not to ask, not to stop on errors, to descend
> into everything, and to do so as the administrator. Every element of that sentence was
> requested. The terminal will do precisely what you say, which is the deal you accepted
> when you opened it. Read the target. Check `pwd`. Prefix with `echo` if unsure.

**Quiz.** You want to delete a folder of old logs. Which is the safest first move?

- [ ] `sudo rm -rf old-logs/` — get it over with
- [x] `pwd` to confirm where you're standing, then `ls old-logs/` to see what's actually in it, then `echo rm -rf old-logs/` to see the exact expanded command — and only then run it for real.
- [ ] `rm old-logs/` and add flags until it stops complaining
- [ ] Delete it in the file manager instead; the terminal is too dangerous

*Option 3 is how disasters happen — 'add flags until the error stops' means switching off safety rails you haven't read. Option 1 adds sudo, removing the last one. Option 4 is fine but doesn't teach you anything and doesn't scale to a server with no screen. The habit that survives contact with real work: know where you are, know what you're about to touch, preview the expanded command, then run it. Ten seconds, every time, forever.*

- **Command grammar** — command -flags targets. Short flags (-l) stack (-la); long flags (--help) are self-documenting. Verbs and adverbs.
- **The twelve** — pwd, ls, cat/less, cd, mkdir, cp, mv, rm, grep, find, man/--help, history. Ninety percent of a working day.
- **`rm` has no Trash** — It unlinks immediately: no trash, no undo, no confirmation. `rm -i` asks first. `-r` descends into folders, `-f` silences all questions. Read the TARGET before Enter.
- **The pipe `|`** — Sends one command's output into another's input: `ls -la | grep txt`. Composing small verbs into sentences is why text-only is a feature, not a limitation.
- **Exit code `$?`** — 0 = success, non-zero = failure. Invisible, returned by every command. Your whole CI pipeline — 'this build failed' — is built on this number.
- **The echo-preview trick** — Put `echo` in front of a destructive command. The shell expands wildcards and variables and PRINTS what it would run, without running it. Free, total protection.

### Challenge

Make `~/cli-practice`, fill it with a few files, and answer these with commands only:
how many files contain the word 'test'? (`grep -c`) Which files were changed most
recently? (`ls -lt`) What did I run in this session? (`history`) Then delete the folder
using `rm -ri` so it asks about every single item — and notice that being asked feels
*good*, not slow. That feeling is the one to keep when you eventually stop using `-i`.

### Ask the community

> Command question: I ran `[exact command, copy-pasted]` in `[output of pwd]` and got `[exact error]`. `ls` of the target shows: [paste]. Expected: [what you thought would happen].

Paste the command exactly — including flags, quotes, and slashes. Nine out of ten
terminal questions are answered by someone spotting a missing quote or a `-r` that
should have been `-i`, and a paraphrased command hides precisely the character that
matters.

- [LinuxCommand.org — learning the shell, from zero](https://linuxcommand.org/lc3_learning_the_shell.php)
- [explainshell — paste any command, see what every flag does](https://explainshell.com/)
- [Essential commands, demonstrated](https://www.youtube.com/watch?v=oxuRxtrO2Ag)

🎬 [The commands you'll actually use](https://www.youtube.com/watch?v=oxuRxtrO2Ag) (10 min)

- Every command is `verb -adverbs targets`. Short flags stack (-la), long flags document themselves (--help). Twelve verbs cover most days.
- `rm` deletes immediately: no trash, no undo, no confirmation. `-r` descends, `-f` silences. Check `pwd`, `ls` the target, and preview with `echo` before pressing Enter.
- The pipe `|` feeds one command's output into another. Text composes; screenshots don't. That's the terminal's real advantage.
- `grep -c`, `grep -B5 -A10`, and `>` turn a 40,000-line log into a small attachable piece of evidence in four commands.
- Every command returns an invisible exit code: 0 = success. CI pipelines are built entirely on that number.


---
_Source: `packages/curriculum/content/notes/operating-systems-and-files/first-look-at-the-command-line/basic-commands.mdx`_
