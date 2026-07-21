---
title: "Pushing to GitHub"
tags: ["version-control-with-git", "github", "track-b"]
updated: "2026-07-11"
---

# Pushing to GitHub

*GitHub is a remote home for your repository — a shared copy in the cloud. Create a repo, connect it with git remote add origin, upload commits with git push, and fetch teammates' work with git pull. Push and pull are just sync between your machine's history and GitHub's copy.*

> Everything you've done with Git so far lives on one machine: yours. Your commits, your branches, your
> whole history — safe, but invisible. If your laptop died tonight, the repo dies with it, and no teammate
> has ever seen a line of it. **GitHub** fixes both problems at once: it's a website that hosts a copy of
> your repository — a *remote* — so your work is backed up off your machine and shared with your team.
> The mechanics are two commands you'll run every working day for the rest of your career: `git push`
> uploads your commits to GitHub, `git pull` downloads everyone else's. That's it — push and pull are just
> *sync*. For a tester this is day-one stuff: the test framework you'll work in lives on GitHub, and the
> first thing a new job asks of you is to clone it, commit to it, and push. This note gets you fluent.

> **In real life**
>
> GitHub is **a shared warehouse, and pushing is mailing a parcel to it.** Your local repo is your home
> workshop: you build things (commits) there, and only you can see them. The warehouse — the
> **remote**: A copy of your repository hosted somewhere else, usually on GitHub. Your local repo remembers the remote's address under a nickname (conventionally 'origin'). git push uploads your commits to it; git pull downloads new commits from it. It exists for backup and sharing.
> — is the copy everyone on the team can reach. `git remote add origin ...` writes the warehouse's address
> into your address book under the nickname `origin`. `git push` loads your finished parcels (commits) into
> the van and delivers them; `git pull` is the return trip, collecting parcels your teammates dropped off.
> Nothing teleports on its own: until you push, your commits sit in your workshop, and until you pull,
> theirs sit in the warehouse. Two copies, two commands to keep them in sync.

## GitHub hosts a copy of your repo, called a remote

You already know a repo can live in two places — your machine and somewhere shared — from the
[local vs remote](/notes/version-control-with-git/why-version-control/local-vs-remote) note. GitHub is
the somewhere shared: a website (github.com) that stores Git repositories, shows their history in a
browser, and lets a whole team read and write the same project. To put an existing local repo there,
you do two things. First, create an **empty** repository on GitHub: log in, click **New repository**,
give it a name like `qa-notes`, and skip the 'add a README' checkbox (your repo already has files —
starting empty avoids a clash). GitHub then shows you its address. Second, tell your local repo that
address:

```bash
git remote add origin https://github.com/<your-username>/qa-notes.git
git remote -v
# origin  https://github.com/<your-username>/qa-notes.git (fetch)
# origin  https://github.com/<your-username>/qa-notes.git (push)
```

`remote add` doesn't copy anything yet — it just saves the URL under a nickname. That nickname is
`origin` by convention, the way 'home' is the first entry in your GPS. Every push and pull from now on
uses the nickname, so you never type the URL again.

![A long wharf-side transit shed with eighteen identical loading-bay doors stretching down the waterfront, dock cranes at both ends and a ship moored at the right, the city skyline behind](pushing-to-github.jpg)
*Transit shed with eighteen loading bays, Oakland Army Base — HAER, Library of Congress via Wikimedia Commons, Public domain. [Source](https://commons.wikimedia.org/wiki/File:GENERAL_VIEW_OF_SOUTHEAST_SIDE_OF_SHED,_SHOWING_ALL_EIGHTEEN_LOADING_BAYS,_LOOKING_WEST_FROM_ACROSS_TURNING_BASIN_-_Oakland_Army_Base,_Transit_Shed,_East_of_Dunkirk_Street_and_HAER_CAL,1-OAK,12-A-7.tif)*
- **The shared shed = the remote (origin)** — The shared building is the GitHub copy of your repo. Everyone on the team can reach it; nobody works IN it. It exists for two jobs: backup (your history survives your laptop) and sharing (teammates fetch your work from here, not from your machine).
- **Each crate behind a bay door = a commit** — What travels between your machine and GitHub is commits — whole save-points, with their messages and history. git push never sends 'your latest keystrokes'; it sends committed snapshots. Uncommitted changes stay home. If it isn't committed, it can't be pushed.
- **The ship unloading at the dock = git push** — Push is the delivery run: it uploads every local commit the remote doesn't have yet. After a successful push, GitHub's copy of the branch matches yours. Until you push, your commits are invisible to the team — the number-one beginner surprise.
- **The crane loading outbound = git pull** — Pull is the return trip: it downloads commits your teammates pushed and merges them into your local branch. Pulling before you start work keeps you building on the latest version instead of on stale history — and avoids most push rejections.
- **The bay numbers = the remote URL and branch refs** — https://github.com/you/qa-notes.git is the warehouse's street address. git remote add origin saves it once under the nickname 'origin'; git remote -v reads your address book back. Wrong address = every push and pull fails with 'repository not found'.

## Push uploads your commits, pull downloads everyone else's

With the remote saved, the very first upload is:

```bash
git push -u origin main
# To https://github.com/<your-username>/qa-notes.git
#  * [new branch]      main -> main
# branch 'main' set up to track 'origin/main'.
```

Read it as 'push my `main` branch to `origin`'. The one-time `-u` flag links your local `main` to the
remote's `main` (called *tracking*), so from then on a plain `git push` and `git pull` know exactly
where to go. And that's the whole model: **commits are local until you push.** `git commit` saves to
*your* repo only — nothing leaves your machine. `git push` is the moment your work becomes visible,
backed up, and shareable. The mirror image is `git pull`: your local repo doesn't magically learn about
teammates' pushes; you fetch them on request. So the everyday rhythm is a sync loop — *pull before you
start, push when you're done* — keeping two copies of the same history close enough that nobody trips
over the gap.

**From local-only to synced with GitHub. Press Play.**

1. **Your repo lives on your machine** — You've been committing locally: full history, but one copy, visible to one person. If the laptop dies, the project dies. Git is doing its job — GitHub's job (backup + sharing) hasn't started yet.
2. **Create an empty repo on GitHub** — On github.com: New repository, name it, skip the README (your local repo already has files). GitHub now has an empty shell waiting for history, and shows you its URL — the address you'll connect to.
3. **Connect them: git remote add origin URL** — This saves GitHub's address in your local repo under the nickname 'origin'. Nothing is uploaded yet — it's writing an entry in your address book so future pushes and pulls know where to go.
4. **git push -u origin main uploads your commits** — Push sends every commit on main up to GitHub; -u links the two branches so plain 'git push' works afterwards. Refresh the GitHub page: your files and full commit history are there. Backed up. Visible.
5. **git pull keeps you in sync from now on** — Teammates push their commits to the same remote; git pull downloads and merges them into your copy. The loop for life: pull before you start, commit as you work, push when you're done.

*Try it — connect a local repo to GitHub and push. Press Run.*

```bash
# One-time setup: you have a local repo with commits,
# and you've created an EMPTY repo named qa-notes on github.com

git remote add origin https://github.com/sajan-qa/qa-notes.git

git remote -v
# origin  https://github.com/sajan-qa/qa-notes.git (fetch)
# origin  https://github.com/sajan-qa/qa-notes.git (push)

# First push: -u links local main to origin/main (tracking)
git push -u origin main
# Enumerating objects: 6, done.
# Writing objects: 100% (6/6), 542 bytes | 542.00 KiB/s, done.
# To https://github.com/sajan-qa/qa-notes.git
#  * [new branch]      main -> main
# branch 'main' set up to track 'origin/main'.

# Refresh github.com/sajan-qa/qa-notes in the browser:
# your files AND your whole commit history are now there.
```

That's the one-time setup. Here's the **everyday rhythm** — the pull/commit/push loop you'll run every
single working day:

*Try it — the daily sync loop: pull, commit, push. Press Run.*

```bash
# Morning: pull first, so you build on the latest version
git pull
# Already up to date.

# ...you edit login-tests.md, then save the work LOCALLY:
git add login-tests.md
git commit -m "Add negative login test cases"
# [main 4f2a9c1] Add negative login test cases
#  1 file changed, 12 insertions(+)

# Right now the commit exists ONLY on your machine.
git status
# On branch main
# Your branch is ahead of 'origin/main' by 1 commit.
#   (use "git push" to publish your local commits)

# Publish it:
git push
# To https://github.com/sajan-qa/qa-notes.git
#    8d3e2b7..4f2a9c1  main -> main

git status
# On branch main
# Your branch is up to date with 'origin/main'.
```

> **Tip**
>
> Burn in the rhythm: **pull before you start, push when you're done.** Pulling first means you build on
> the team's latest work instead of on yesterday's, and it prevents the classic 'push rejected' message
> (which just means the remote has commits you don't). And keep the two-step firmly separate in your head:
> `git commit` = saved *locally*, `git push` = published to GitHub. If a teammate 'can't see your fix,'
> run `git status` — 'ahead of origin/main by 1 commit' is Git telling you the work is sitting in your
> workshop, still waiting for the delivery van.

### Your first time: First time? Put a repo on GitHub

- [ ] Create an empty repo on github.com — Log in, click New repository, name it (say, qa-notes), and leave 'Add a README' unchecked — your local repo already has files, and starting empty avoids a first-push clash. GitHub then shows the exact commands for 'push an existing repository'.
- [ ] Connect your local repo to it — In your project folder: git remote add origin https://github.com/YOURNAME/qa-notes.git — then git remote -v to confirm. Nothing uploads yet; you've just saved the address under the nickname 'origin'. Typos here cause 'repository not found' later, so verify.
- [ ] Push for the first time with -u — git push -u origin main uploads all your commits and links local main to origin/main. Watch the output: '[new branch] main -> main' is the success line. From now on plain 'git push' is enough — the -u was a one-time introduction.
- [ ] Verify on the website — Refresh the repo page on github.com. Your files are there — and click the commits count: your full history, every message you wrote, is browsable. This is the payoff: backup plus a team-readable history, for free.
- [ ] Run one full sync loop — Edit a file, git add, git commit, then git status — note 'ahead of origin/main by 1 commit' (saved locally, not published). git push, refresh the browser, see the change land. Then git pull once: 'Already up to date.' You've now done the loop you'll run daily forever.

Fifteen minutes, and your repo is backed up, shareable, and synced — and push/pull have stopped being magic.

- **“! [rejected] main -> main (fetch first / non-fast-forward) when I push.”**
  The remote has commits you don't have — a teammate pushed since your last sync (or you edited on the GitHub website). Git refuses to overwrite them. Run git pull first: it downloads and merges their commits into yours, then git push succeeds. This is normal teamwork friction, not an error in your work — and it's exactly why the habit is 'pull before you push.'
- **“remote: Repository not found — but I can see it in my browser.”**
  Your saved remote URL is wrong (typo, wrong username, wrong repo name), or you don't have access with the account Git is using. Check git remote -v and compare character-by-character with the URL on GitHub. Fix it with: git remote set-url origin https://github.com/YOU/correct-name.git — then push again. If the URL is right, it's an authentication/account mismatch.
- **“Authentication failed — it won't accept my GitHub password.”**
  GitHub removed password authentication for Git operations years ago. You need either a personal access token (used in place of the password) or, far easier, the GitHub CLI: run gh auth login once and follow the prompts — it wires up credentials for you. On a fresh machine this is almost always the first wall you hit; it's setup, not something you broke.
- **“error: src refspec main does not match any.”**
  Git can't find a branch named main to push. Two usual causes: you haven't made any commits yet (an empty repo has no branch to push — commit first), or your branch has a different name, like master (check with git branch). Either commit and retry, or push the branch you actually have — or rename it first: git branch -M main.

### Where to check

Debugging a push or pull:

- **`git remote -v`** — is the URL exactly right? Wrong address = 'repository not found' on every push and pull.
- **`git status`** — 'ahead of origin/main by N commits' = you have unpushed work; 'behind' = you need to pull; 'up to date' = synced.
- **`git log --oneline -5`** — is the commit you expect actually committed? You can't push what you never committed.
- **The GitHub page itself** — refresh the repo in the browser and check the latest commit message. That's the truth about what the team can see.
- **Rejected push?** — pull first, then push. The remote having newer commits is the normal cause, and pull is the normal cure.

### Worked example: the fix nobody could see — a commit that never left the laptop

A tester fixes a broken test script, tells the team 'done — it's fixed,' and an hour later the teammate
running the suite says the test still fails and the fix is nowhere on GitHub. Trace it:

1. **The symptom:** on the tester's machine the fix is plainly there — the file is correct, and `git log`
   shows the commit `a91c3f2 Fix locator in login test` at the top. On GitHub, the file is unchanged and
   that commit doesn't exist. Same repo, two different stories.
2. **The tell-tale status:** `git status` says `Your branch is ahead of 'origin/main' by 1 commit.`
   That line is Git saying it out loud: the commit was saved *locally* and never published. `git commit`
   ran; `git push` never did.
3. **Why this happens so easily:** commit feels like 'saving to the system,' so it *feels* done. But
   commit writes only to the repo on your machine. Until push, teammates, GitHub, and the CI pipeline are
   all looking at history that doesn't include your work.
4. **The fix — publish it:** `git push`. Output: `8d3e2b7..a91c3f2  main -> main`. Refresh GitHub — the
   commit and the corrected file appear. The teammate pulls (`git pull`) and the suite goes green.
5. **The habit that prevents it:** end every work session with `git status`. If it says 'ahead by N
   commits,' decide deliberately: push it, or know you're leaving work unpublished. 'Done' means pushed,
   not committed.
6. **Tester's angle:** this bug has a famous cousin — 'works on my machine.' When a developer says a fix
   is done but your retest still fails, check *what you're actually testing*: is the fix pushed, and is
   it in the build you're running? A tester who asks 'is that pushed? which commit is this build from?'
   saves hours of arguing about a fix that simply hasn't shipped yet.

> **Common mistake**
>
> Believing `git commit` uploads your work. It doesn't — commit saves a snapshot to the repo *on your
> machine*, and nothing more. Your teammates, GitHub, and the CI pipeline see exactly nothing until you
> `git push`. The classic shape: someone announces a fix, the team can't find it, tempers rise — and
> `git status` was quietly saying 'ahead of origin/main by 1 commit' the whole time. The sibling mistake
> is pushing without ever pulling: work for days without syncing and your first push gets rejected because
> the remote moved on without you — then the merge is bigger and messier than it needed to be. Both have
> the same cure: treat push/pull as a *daily rhythm*, not an occasional event. Pull before you start, push
> when you're done, and read what `git status` tells you about ahead/behind.

**Quiz.** You run git commit -m 'Fix login test', then your teammate refreshes GitHub and sees nothing new. What happened?

- [ ] GitHub is slow — the commit will appear on the website within a few minutes
- [x] Commits are local until published: git commit saved the snapshot to YOUR repo only, and it reaches GitHub when you run git push
- [ ] The commit failed silently — you must run git commit twice for remote repos
- [ ] The teammate needs to run git commit on their machine to receive it

*git commit writes to the repository on your machine — full stop. Nothing is transmitted anywhere. The remote copy on GitHub only changes when you explicitly upload with git push (and your teammate then sees it in the browser immediately, or gets it locally with git pull). There's no delay to wait out, no double-commit, and receiving work is done by pulling, not committing. The two-step model — commit = save locally, push = publish — is the single most important fact about working with GitHub.*

- **Remote** — A hosted copy of your repository, usually on GitHub. Exists for backup (history survives your laptop) and sharing (the team syncs through it). Your local repo stores its URL under a nickname.
- **origin** — The conventional nickname for your main remote. Saved with git remote add origin URL; inspected with git remote -v. Commands like push/pull use the nickname so you never retype the URL.
- **git push** — Uploads your local commits to the remote. Until you push, commits exist only on your machine. First push of a branch: git push -u origin main (the -u sets up tracking so plain git push works after).
- **git pull** — Downloads new commits from the remote and merges them into your current branch. It's how teammates' pushed work reaches you. Habit: pull before you start working, so you build on the latest version.
- **Ahead / behind (git status)** — 'Ahead of origin/main by 2' = you have 2 unpushed local commits. 'Behind by 3' = the remote has 3 commits you haven't pulled. Both at once can happen — pull first, then push. git status is the sync dashboard.
- **git clone** — The other direction of setup: copies an EXISTING remote repo to your machine, with full history, and wires up origin automatically. Joining a team = clone once, then live in the pull/commit/push loop.

### Challenge

Put a real repo on GitHub, end to end. (1) Take any local repo with a few commits (or make one: a folder
with two small text files, committed). (2) Create an empty repo on github.com and connect it with
git remote add origin, then prove the address stuck with git remote -v. (3) Push with
git push -u origin main and verify in the browser that both the files AND the commit history arrived.
(4) Make one more local commit, run git status, and write down the exact 'ahead of origin/main' line
before you push it. (5) In one sentence, explain to an imaginary teammate why 'I committed it' and 'I
pushed it' are different claims — if your sentence contains 'commit saves locally, push publishes to the
remote,' you've got the model.

### Ask the community

> Push/pull question: I'm trying to [push my repo to GitHub / pull my teammate's changes], I ran [exact commands] and got [exact message]. git remote -v shows [output] and git status says [output]. What's going on?

Paste the *exact* error line — 'rejected (fetch first)', 'repository not found', 'authentication failed',
and 'src refspec' all have different one-line fixes. Include your git remote -v output (with the URL) and
what git status says about ahead/behind: those two commands answer most push/pull mysteries before anyone
even replies.

- [GitHub Docs — Hello World (your first repository)](https://docs.github.com/en/get-started/start-your-journey/hello-world)
- [Pro Git — Working with Remotes (free book chapter)](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)
- [Learn GitHub in 20 minutes — remotes and pushing — Colt Steele](https://www.youtube.com/watch?v=nhNq2kIvi9s)

🎬 [Learn GitHub in 20 minutes — remotes and pushing — Colt Steele](https://www.youtube.com/watch?v=nhNq2kIvi9s) (20 min)

- GitHub hosts a remote — a copy of your repo that lives off your machine. It exists for two reasons: backup (your history survives the laptop) and sharing (the whole team syncs through one place).
- Connect once with git remote add origin URL. 'origin' is just a nickname for the saved address; git remote -v reads it back. After that, commands use the nickname, never the raw URL.
- git push uploads your commits to the remote; the first push of a branch uses -u (git push -u origin main) to set up tracking so plain git push works from then on.
- Commits are LOCAL until you push. git commit saves to your machine only — teammates and GitHub see nothing until git push. 'Ahead of origin/main by N commits' in git status = unpublished work.
- Push and pull are just sync, and the rhythm is daily: pull before you start (build on the latest), push when you're done (publish and back up). Most push rejections are cured by pulling first.


---
_Source: `packages/curriculum/content/notes/version-control-with-git/github-and-pull-requests/pushing-to-github.mdx`_
