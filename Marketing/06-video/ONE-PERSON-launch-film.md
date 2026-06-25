# 🎬 "ONE PERSON" — QA Mastery Talent launch film

> Production package for the **Add & Hire Testers** launch. Angle #1 "One Person" — the solo-founder story. Grounded in the real product and brand. **Honesty rule:** only feature what's live (proof-forward profiles, device matrix, lab-verified badges, QA-native filters, per-project + full-time posting, consent-gated contact). **No ratings/reviews** (V1.0 backlog); match = "matched to your stack & devices" (real rule-based ranking).

**Name:** *You Built It Alone. Don't Ship It Alone.* · **Duration:** 60s · **Ratios:** 9:16 + 16:9

---

## Concept
Every product starts as one person at 2 a.m. — but none ships *ready* until someone else tries to break it. A solo dev moves through the lonely grind and the dread of launch, then opens **QA Mastery Talent** and a real tester catches the bug that would've tanked the launch. Arc: **isolation → signal → relief**, mirrored by the app's dark-to-light brand. The *Add & Hire Testers* feature is the turning point.

## Creative direction
- **Style:** cinematic realism, neon-noir → warm daylight.
- **Palette:** `#09090b` Void Black · `#2dd4a7` Signal Teal · `#f5b948` Bug Amber · `#f4f4f5` Fog. Mood: "quiet grind → signal."
- **Type:** Bricolage Grotesque (headlines), Geist (UI/captions), Instrument Serif italic (the word *"alone"*). Teal underline accents.
- **Pacing:** long holds 0–18s → accelerate → 2s cuts at the CTA.
- **Camera:** macro close-ups → slow push-ins → 2.5D parallax on card fly-ins → real-app screen recordings.
- **Arc:** SOLO (tight, one light) → SIGNAL (teal enters) → TEAM (wide, lit).
- **Refs:** Apple "The Underdogs," Linear launch films, Notion "Tools for the next generation."

## Storyboard (6 scenes / 60s)
1. **0–11s — Solo builder.** Dark room, one face lit by a monitor, cold coffee. Slow push-in. Text: *"It started with one person."* (Instrument Serif). Hard cut on a keystroke.
2. **11–20s — The dread.** Deploy bar → red error/crash. Finger hovering "Ship." Text: *"You can't catch the bug you don't know you wrote."* Glitch flash to black.
3. **20–30s — The signal.** Teal light bleeds in; real `/talent/testers` directory loads; cursor filters API · Mobile · real-device. Text: *"You don't have to ship alone."* Card lifts toward camera.
4. **30–42s — First tester.** Profile card flies in (2.5D): avatar, device matrix, green "Verified · 92%" badge, specialties. Text: *"Real proof. Not promises."* Flip to chat.
5. **42–52s — The catch.** Message: "Found it — checkout breaks on Android 13." Amber glitch flash, resolves clean; builder exhales. Text: *"Caught — before anyone else saw it."*
6. **52–60s — Scale + CTA.** One avatar → many (solo→team). UI shows "Post a project" + "Hire full-time." CTA pulses teal. Text: **"Add your first tester — free."** + URL.

## AI tool pipeline (one per task)
- Video: **Kling 1.6** · Key frames: **Flux 1.1 Pro** · UI animation: **screen-record real app + Jitter.video** · VFX: **DaVinci Resolve (Fusion)** · VO: **ElevenLabs v3 (Adam)** · Music: **Suno v4** · SFX: **ElevenLabs Sound FX** · Edit/color: **DaVinci Resolve**.

## Audio
- **Music arc:** lone felt piano + sub pad (70 BPM) → teal synth pulse + kick at 0:20 → warm resolved swell at CTA (→110 BPM). Instrumental.
- **VO script (~58s):**
  > "This started with one person. `[PAUSE]` 2 a.m. The coffee's cold. Just you, the code, and a deadline that doesn't care. `[PAUSE]` You built every screen. Every edge case `[EMPHASIS]` you could think of. `[PAUSE]` But you can't catch the bug you don't know you wrote. `[quieter]` `[PAUSE]` So you ship… and you hope. `[beat]` `[lift]` Or — you don't ship alone. **QA Mastery Talent.** Real testers. Proof, not promises — bug reports, automation, the exact devices they test on. `[PAUSE]` Find one for a project. Or hire your first full-time. `[PAUSE]` `[SFX chime]` And the bug that would've tanked your launch? `[PAUSE]` Caught. `[PAUSE]` `[warm]` Every product starts with one person. The good ones don't stay that way. `[PAUSE]` **Add your first tester — free.**"
- **SFX:** `0:02` keystrokes → `0:14` deploy hum + error stab → `0:20` signal whoosh → `0:32` card whoosh ×3 → `0:44` amber glitch + chime → `0:54` swell.
- **Mix:** VO −6 dBFS · music ducked −18 dB under VO · SFX peaks −10 dB · master −14 LUFS.

## VFX by scene
- S1–2: film grain (`.grain`), screen-glow bloom, rack-focus, amber glitch tear on error.
- S3: teal light-bleed wipe + real UI screen-record with animated cursor/chips.
- S4: 2.5D parallax card fly-in; sequential badge/chip pop; DoF.
- S5: amber "bug-found" glitch + chromatic aberration → calm teal.
- S6: avatar multiply (1→many) scale transition; CTA pulse + teal glow (`.text-glow-accent`).

## Ready-to-use prompts
**[KLING 1.6 — S1 Solo Dev]** "Cinematic close-up of a young developer alone in a dark room at 2am, face lit only by a glowing monitor, reflection of code in their glasses, cold coffee mug, exhausted but focused. Moody single-source lighting, deep blacks, subtle teal screen glow. Slow push-in. 35mm, shallow DoF, film grain. 9:16."

**[FLUX 1.1 PRO — Profile card]** "UI hero shot of a dark-mode QA marketplace profile card, near-black #09090b background, emerald-teal #2dd4a7 accents, amber #f5b948 'Verified 92%' badge, clean Geist-style type, device-matrix chips (iPhone, Pixel, Windows), floating with soft shadow + depth, premium fintech aesthetic, 4k."

**[JITTER — Card fly-in]** "Card enters with 2.5D parallax: slides up + scales 0.9→1.0 over 500ms ease-out; stagger-pop the verified badge, 3 device chips, 2 specialty tags at 80ms intervals; teal glow pulse on the badge. Dark bg."

**[SUNO v4 — Music]** "Cinematic emotional tech-launch score. Starts sparse and lonely: felt piano + soft sub pad, 70 BPM. At ~20s a warm teal synth pulse + gentle kick enter, building hope. Resolves into a full uplifting modern swell. Instrumental, 60s, Linear/Apple ad energy. BPM 70→110."

**[ELEVENLABS v3 — VO]** Voice Adam (deep, intimate). Stability 45, Style 60. Read the VO script. Reflective/quiet first half, lifting to warm at "you don't ship alone," CTA calm-confident, not salesy.

**[DAVINCI/FUSION — bug-found glitch]** S5: digital glitch + RGB chromatic-aberration for 6 frames over the phone screen, amber tint, snap-resolve to clean with teal edge-glow; 2-frame white flash on the chime.

## Timeline (solo / $0 path)
- D1 key frames (Flux free) + screen-record the real app · D2 emotional clips (Kling free credits) · D3 Jitter + Suno + ElevenLabs (free tiers) · D4 assemble + VFX + color (DaVinci free) · D5 export 9:16 + 16:9.
- **$0 swaps:** only S1/S2/S5 need AI video — if credits run out, use stock B-roll + real screen-records + bold Bricolage text cards. S3/S4/S6 are 100% free (real app + Jitter).
