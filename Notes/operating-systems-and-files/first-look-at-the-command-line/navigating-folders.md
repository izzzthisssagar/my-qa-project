---
title: "Navigating folders"
tags: ["computer-basics", "command-line", "paths", "track-a"]
updated: "2026-07-10"
---

# Navigating folders

*Walking the tree with `cd`, `ls` and tab-completion. The same folders you clicked through in chapter 3 — but now you can move through them faster than a mouse, and describe exactly where you are.*

> Everything you learned about paths in chapter 3 was secretly preparation for this. The
> tree, the absolute versus relative distinction, the `..` that means "up one" — that was
> theory. Here it becomes movement. And the single key that makes it painless is one
> almost nobody teaches beginners: **Tab**. Press it constantly. It types for you, and
> it refuses to type a path that doesn't exist.

> **In real life**
>
> The GUI is **teleporting between rooms by clicking on doors you can see.** The terminal
> is **walking a building you know the floor plan of.** Walking sounds slower — until you
> realise the walker can say "go to the third floor, east wing, room 12" in one breath
> and be there, while the clicker is still opening the second door. The floor plan is the
> path. You already have it.

## The three commands, and the shortcuts that make them fly

- `pwd` — where am I? (Prints the absolute path of your **working directory**: The folder a program considers 'here'. Every process has one, inherited from whatever launched it. Relative paths resolve against it — which is why the same script finds a file on your laptop and not on CI..)
- `ls` — what's here? `ls -la` shows hidden files and details.
- `cd <path>` — go there.

And the shorthand the shell understands, which *is* chapter 3's vocabulary:

| You type | It means |
|---|---|
| `cd Documents` | relative: into `Documents`, from where I stand |
| `cd /home/sajan/QA` | absolute: from the root, exactly there |
| `cd ..` | up one level |
| `cd ../..` | up two |
| `cd ~` or just `cd` | Home |
| `cd -` | back to the previous directory (the browser Back button) |

![A terminal prompt showing the current directory, with ls output listing files](terminal.png)
*Screenshot: GNOME Terminal running bash — Wikimedia Commons, GPL. [Source](https://commons.wikimedia.org/wiki/File:Linux_command-line._Bash._GNOME_Terminal._screenshot.png)*
- **The prompt shows your location — always** — That `~/Documents` in the prompt IS your working directory, printed for free before every command. The file manager needed a path bar for this; the shell just tells you, constantly, without being asked.
- **`cd` — the whole navigation vocabulary** — One verb, and chapter 3's grammar as its argument: relative names, absolute paths, `..` for up, `~` for Home, `-` for back. You learned the grammar before you learned the verb. That was on purpose.
- **`ls` output — the room you're standing in** — Files and folders, plain text. Add `-l` for sizes and dates, `-a` for hidden entries (the dotfiles the uninstalling note said were hiding your app configs). The GUI shows you a room; `ls` tells you about it in a form you can pipe into grep.
- **Trailing slash = it's a folder** — Many `ls` configs append `/` to directory names, or colour them. Learn to read the shape of a listing at a glance — folders, files, executables. Your eye gets fast at this within a week.
- **Prompt returned = you've arrived** — `cd` prints nothing when it succeeds — Unix's rule is 'no news is good news'. Silence means it worked. An error means it didn't. There is no third state, and nothing to read when things go right.

**Tab-completion: the key that types for you — press Play**

1. **⌨️ You type `cd Doc` and press Tab** — You have typed three characters. The shell now looks at your current folder and asks: what starts with 'Doc'?
2. **🔎 One match → it completes** — `Documents/` appears, fully typed, correctly spelled, with the slash. You cannot typo a name you didn't type. Tab completion is a spellchecker that runs before the error instead of after it.
3. **🔀 Several matches → it pauses** — Type `cd D` + Tab with `Documents/` and `Downloads/` both present: the shell completes as far as it can (`Do`) and stops. Press Tab AGAIN and it lists both. It's not stuck — it's asking you to disambiguate.
4. **🚫 No match → silence (or a beep)** — Nothing completes. That's information: no file or folder here starts with what you typed. You just discovered the path is wrong BEFORE running the command. Tab is a free existence check.
5. **🚀 Now chain it** — `cd D`Tab`Tab`→`cd Documents/`Tab→`QA/`Tab→`bug-reports/`. Four keystrokes and three Tabs walk you three levels deep, with zero typos, faster than three double-clicks. This is why terminal users look fast: they aren't typing full paths. Almost nobody does.

*Try it — resolve `cd` paths the way the shell does*

```python
from pathlib import PurePosixPath

def cd(cwd, arg, home="/home/sajan", prev=None):
    if arg in ("", "~"):     return home
    if arg == "-":           return prev or cwd
    if arg.startswith("~/"): arg = f"{home}/{arg[2:]}"
    p = PurePosixPath(arg) if arg.startswith("/") else PurePosixPath(cwd) / arg
    # resolve '..' and '.' by hand — exactly what the shell does:
    parts = []
    for seg in p.parts:
        if seg == "..":
            if len(parts) > 1: parts.pop()      # never go above root
        elif seg not in (".",):
            parts.append(seg)
    return str(PurePosixPath(*parts))

cwd, prev = "/home/sajan/Documents/QA/bug-reports", None
for arg in ["..", "../test-plans", "/var/log", "~", "~/Documents", "-", "../../../.."]:
    new = cd(cwd, arg, prev=prev)
    print(f"cwd={cwd:38} $ cd {arg:16} -> {new}")
    prev, cwd = cwd, new
print()
print("Note the last one: four '..' from /home/sajan/Documents can't climb past /.")
print("The root has no parent. 'cd ..' there is a no-op, not an error.")
```

## Tab is not optional

Say it once more, because it's the difference between "the terminal is slow" and "the
terminal is fast": **you do not type paths. You type two or three letters and press
Tab.** It completes filenames, folder names, command names, and (in modern shells) even
flags. It cannot complete something that doesn't exist — so a completion that refuses
to fire is telling you your path is wrong, before you've run anything.

> **Tip**
>
> Three more that feel like cheating: **↑ (up-arrow)** re-runs your last command — edit
> it instead of retyping. **Ctrl+R** searches your history: press it, type `pytest`, and
> the last pytest command you ran appears, ready to run. **`cd -`** bounces you back to
> the folder you were just in, like a browser Back button. Between Tab, ↑, and Ctrl+R,
> an experienced user retypes almost nothing. That's the actual secret — not memory,
> just refusing to type twice.

### Your first time: Your mission: walk the tree without a mouse

- [ ] Start at Home — Type `cd` alone and press Enter. You're Home. Confirm with `pwd`. That's the absolute path of your Home folder — the one chapter 3 taught you to recognize.
- [ ] Walk down using Tab only — Type `cd Doc` then Tab (it completes), Enter. Then `ls`. Then descend again with Tab. Rule for this exercise: you may not type a full folder name. Only fragments plus Tab.
- [ ] Walk back up — `cd ..` then `pwd`. Then `cd ../..` and `pwd` again. Watch your absolute path shorten by one segment each time. The tree from chapter 3, moving under your hands.
- [ ] Use `cd -` twice — Jump somewhere far away, then `cd -` to bounce back, then `cd -` again to bounce forward. Two folders, one key. This is the shortcut people who've used a terminal for years still smile about.
- [ ] Break it on purpose — `cd doesnotexist`. Read the error: 'no such file or directory'. Then type `cd doesnot` + Tab — nothing completes. Tab told you the same thing, for free, before you ran anything.

You navigated three levels down, back up, bounced between two folders, and never typed a full path.

- **`cd: no such file or directory` — but I can see the folder in Finder!**
  In order: (1) `pwd` — you're not standing where you think, so your relative path resolves somewhere else entirely (chapter 3's central lesson, now in the terminal). (2) Case — Linux distinguishes `documents` from `Documents`; macOS usually doesn't. (3) A space in the name — `cd My Documents` passes two arguments. Quote it, or just press Tab and let the shell escape it for you.
- **Tab-completion isn't completing anything.**
  It's telling you nothing here matches what you typed. That's a real answer, not a broken key. `ls` to see what's actually in this folder, or check `pwd`. Completion failing IS the diagnosis — the shell just refused to help you type a path that doesn't exist. Treat it as an early error, not a malfunction.
- **I `cd`'d into a folder in the terminal, but my file manager didn't move.**
  Working as designed: each program has its OWN working directory (the FlowAnimation in chapter 3's `file-paths` note). The shell moving doesn't move anything else. Two programs, two 'heres'. Which, incidentally, is the exact reason your script found a file when you ran it and CI didn't.
- **I'm completely lost. Which folder am I even in?**
  `pwd`. That's it. Then `cd` alone to teleport Home and start over. You cannot be lost in a terminal for more than one command — a claim no file manager can make. Being lost is a five-character problem here.

### Where to check

Orientation, in the terminal:

- **The prompt** — usually shows your current folder already. Configure it to show the full path if you want (`PS1` in bash, `PROMPT` in zsh).
- **`pwd`** — the absolute truth about where you stand.
- **`ls -la`** — what's here, including hidden dotfiles: `.git`, `.env`, `.config`. The GUI hides these; the terminal shows them on request, and testers need them.
- **`cd -`** — where was I before? Bounce back and check.
- **`history`** — how did I get here? Your own trail of commands.
- **Tab** — does this path exist? Ask before you run.

Tester's habit: **`pwd` before any destructive command, `ls` before any wildcard.**
`rm *.log` in the wrong folder is a bad afternoon, and both commands that would have
prevented it take under a second. The professionals aren't more careful people — they
just have two reflexes you can install this week.

### Worked example: finding a config file in an unfamiliar project

Your first day on a new codebase. Someone says "the test config is somewhere in there."

1. **`cd project && ls`** — you see `src/`, `tests/`, `package.json`, and not much else. Fine. Ten files, not four hundred.
2. **`ls -la`** — now you see the hidden ones too: `.git/`, `.env`, `.github/`. The dotfiles were always there; `ls` just doesn't show them without `-a`. Half a project's configuration hides here.
3. **`ls tests/`** — `playwright.config.ts`. Found it, three commands in, without opening an editor.
4. **But is it the only one?** `find . -name "*.config.*"` — walks the whole tree from here down and prints every match, including one in a subfolder you'd never have clicked into.
5. **Two configs.** Which one runs? `cat playwright.config.ts` — and there's the answer, plus a `testDir: './tests'` line: **a relative path**, resolved against wherever the command is run from. You know exactly what that means now, and exactly how it breaks on CI.
6. **Total time: under a minute**, no editor, no clicking, and you finished holding a real insight about the project rather than a vague memory of its folder icons. This is what "navigating" actually buys.

> **Common mistake**
>
> Typing full paths by hand. It's slow, it's typo-prone, and it makes people conclude the
> terminal is user-hostile when in fact they're refusing the help it's offering. `cd
> /Users/sajan/Documents/Projects/qa-mastery/apps/platform` is 52 keystrokes of risk;
> `cd ~/D`Tab`P`Tab`q`Tab`a`Tab`p`Tab is nine keystrokes that cannot be misspelled. If
> your terminal feels like a typing test, you have not yet made Tab a reflex — and that
> single habit, more than any command in this chapter, is what separates fluent from
> frustrated.

**Quiz.** You're in /home/sajan/Documents/QA/bug-reports and you run `cd ../test-plans`. Where do you end up, and why?

- [ ] /home/sajan/test-plans
- [x] /home/sajan/Documents/QA/test-plans — `..` climbs one level to QA/, then `test-plans` descends into its sibling folder. It's a relative path: up one, then down one.
- [ ] It fails, because you can't combine .. with a folder name
- [ ] /test-plans, since .. resets to the root

*`..` means 'the parent of where I stand' — from bug-reports that's QA/. The rest of the path continues from there, descending into test-plans. Combining `..` with names is not just legal, it's the standard way to move sideways between sibling folders in one command. This is chapter 3's path grammar, executed rather than described — which is why that chapter came first.*

- **The navigation trio** — `pwd` (where am I), `ls` (what's here), `cd` (go there). Everything else is shortcuts on top.
- **cd shorthand** — `cd ..` up one · `cd ../..` up two · `cd ~` or `cd` Home · `cd -` back to the previous directory · relative names from here, absolute paths from root.
- **Tab completion** — Type a fragment, press Tab. One match completes it; several completes as far as possible and lists on second Tab; none means the path doesn't exist. A free existence check before you run anything.
- **↑ and Ctrl+R** — Up-arrow re-runs the last command (edit instead of retyping). Ctrl+R searches history by fragment. Fluent users retype almost nothing.
- **`cd` prints nothing on success** — Unix rule: no news is good news. Silence means it worked. There's nothing to read when things go right.
- **Two programs, two 'heres'** — Each process has its own working directory. `cd` in the shell doesn't move your file manager — and that's exactly why relative paths behave differently on CI.

### Challenge

Navigate from Home to a folder three levels deep using only fragments plus Tab — no
full folder names, no mouse. Then `cd -` back, and `cd -` forward again. Finally run
`ls -la` somewhere real and find one dotfile you've never noticed (`.gitconfig`,
`.zshrc`, `.env`). Open it with `cat`. You've just read a configuration file that has
been quietly shaping your machine's behaviour for months, and the GUI never once
mentioned it existed.

### Ask the community

> Navigation question: `pwd` says [paste]. I ran `cd [exact argument]` and got [exact error]. `ls` here shows: [paste]. I expected to land in [path].

Including `pwd` and `ls` output makes this a ten-second answer — the mismatch between
where you're standing and what your relative path assumes is visible in the paste
itself. That's the same diagnosis chapter 3 taught for CI failures, which is not a
coincidence: it's one bug wearing two hats.

- [Ubuntu — moving around the filesystem](https://ubuntu.com/tutorials/command-line-for-beginners#3-opening-a-terminal)
- [MIT Missing Semester — navigating the shell](https://missing.csail.mit.edu/2020/course-shell/)
- [cd, ls, pwd and tab-completion in practice](https://www.youtube.com/watch?v=oxuRxtrO2Ag)

🎬 [Navigating the filesystem from the terminal](https://www.youtube.com/watch?v=oxuRxtrO2Ag) (9 min)

- `pwd`, `ls`, `cd` are the whole navigation vocabulary; chapter 3's path grammar (relative, absolute, `..`, `~`) is what you pass to `cd`.
- Tab-completion is not optional: type a fragment, press Tab. It cannot complete a path that doesn't exist, so it catches wrong paths before you run anything.
- ↑ re-runs the last command, Ctrl+R searches history, `cd -` bounces to the previous folder. Fluent users retype almost nothing.
- `cd` prints nothing on success — silence means it worked. `pwd` means you can never be lost for more than one command.
- Each program has its own working directory, so moving in the shell moves nothing else — the same fact that makes relative paths behave differently on CI.


---
_Source: `packages/curriculum/content/notes/operating-systems-and-files/first-look-at-the-command-line/navigating-folders.mdx`_
