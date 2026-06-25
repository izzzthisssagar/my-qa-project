import React from "react";
import {
  AbsoluteFill,
  Audio,
  Series,
  staticFile,
  interpolate,
  spring,
  useCurrentFrame,
} from "remotion";
import { loadFont as loadBebas } from "@remotion/google-fonts/BebasNeue";
import { loadFont as loadRoboto } from "@remotion/google-fonts/Roboto";

const { fontFamily: BEBAS } = loadBebas();
const { fontFamily: ROBOTO } = loadRoboto();

const INK = "#09090b";
const FG = "#f4f4f5";
const TEAL = "#2dd4a7";
const AMBER = "#f5b948";
const ZINC4 = "#a1a1aa";
const ZINC7 = "#3f3f46";

// "ONE PERSON" launch film — Add & Hire Testers. Motion-graphics, 9:16, 30fps.
// Scene durations (frames @30) sized to each vot-*.mp3 (edge-tts AriaNeural) + tail.
const D = [150, 132, 168, 252, 156, 210];
export const TALENT_DURATION = D.reduce((a, b) => a + b, 0);

const Grid: React.FC = () => (
  <AbsoluteFill
    style={{
      backgroundImage:
        "linear-gradient(rgba(244,244,245,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(244,244,245,0.05) 1px, transparent 1px)",
      backgroundSize: "70px 70px",
    }}
  />
);
const Glow: React.FC<{ c?: string }> = ({ c = TEAL }) => (
  <AbsoluteFill style={{ background: `radial-gradient(60% 40% at 50% 0%, ${c}22, transparent 70%)` }} />
);
const Scene: React.FC<{ children: React.ReactNode; glow?: string }> = ({ children, glow }) => (
  <AbsoluteFill style={{ backgroundColor: INK, overflow: "hidden" }}>
    <Grid />
    <Glow c={glow} />
    {children}
  </AbsoluteFill>
);
const sp = (frame: number, delay = 0, cfg = { damping: 16, stiffness: 120, mass: 0.8 }) =>
  spring({ frame: frame - delay, fps: 30, config: cfg });
const fadeOut = (frame: number, dur: number, len = 12) =>
  interpolate(frame, [dur - len, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

const kicker: React.CSSProperties = {
  fontFamily: "monospace", fontSize: 30, letterSpacing: 3, color: TEAL,
  position: "absolute", top: 150, left: 0, right: 0, textAlign: "center",
};
const H = (size: number): React.CSSProperties => ({
  fontFamily: BEBAS, fontSize: size, lineHeight: 0.92, letterSpacing: 1, color: FG,
  textAlign: "center", margin: 0, padding: "0 80px",
});
const body: React.CSSProperties = {
  fontFamily: ROBOTO, fontSize: 38, lineHeight: 1.4, color: ZINC4, textAlign: "center", padding: "0 120px",
};

const BugMark: React.FC<{ size?: number; check?: number }> = ({ size = 240, check = 1 }) => (
  <svg width={size} height={size} viewBox="0 0 100 100" fill="none">
    <path d="M20 55 L42 78 L84 26" stroke={TEAL} strokeWidth={10} strokeLinecap="round" strokeLinejoin="round"
      strokeDasharray={120} strokeDashoffset={120 - 120 * check} />
    <g transform="translate(60,60)">
      <ellipse cx="0" cy="0" rx="11" ry="14" fill={AMBER} />
      <line x1="-11" y1="-6" x2="-22" y2="-12" stroke={AMBER} strokeWidth="3" strokeLinecap="round" />
      <line x1="-13" y1="2" x2="-25" y2="2" stroke={AMBER} strokeWidth="3" strokeLinecap="round" />
      <line x1="-11" y1="9" x2="-21" y2="16" stroke={AMBER} strokeWidth="3" strokeLinecap="round" />
      <line x1="0" y1="-14" x2="0" y2="-22" stroke={AMBER} strokeWidth="3" strokeLinecap="round" />
    </g>
  </svg>
);

// 1 — SOLO: one person in the dark
const S1: React.FC = () => {
  const f = useCurrentFrame();
  const dot = sp(f, 6, { damping: 14 });
  const pulse = 0.5 + Math.sin(f / 10) * 0.18;
  return (
    <Scene glow={ZINC7}>
      <div style={{ ...kicker, color: ZINC4 }}>// 2:00 am</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 56 }}>
        <div
          style={{
            width: 120, height: 120, borderRadius: 999, background: "#18181b",
            border: `2px solid ${ZINC7}`, opacity: dot, transform: `scale(${0.6 + dot * 0.4})`,
            boxShadow: `0 0 ${40 + pulse * 60}px ${TEAL}${Math.round(pulse * 80).toString(16)}`,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontFamily: BEBAS, fontSize: 64, color: ZINC4,
          }}
        >
          1
        </div>
        <h1 style={{ ...H(110), opacity: sp(f, 40), transform: `translateY(${(1 - sp(f, 40)) * 24}px)` }}>
          IT STARTED WITH<br /><span style={{ color: TEAL }}>ONE PERSON.</span>
        </h1>
      </AbsoluteFill>
    </Scene>
  );
};

// 2 — DREAD: the bug you can't see
const S2: React.FC = () => {
  const f = useCurrentFrame();
  const e = sp(f, 6);
  const fail = sp(f, 64, { damping: 11 });
  const bugX = interpolate(f, [20, 120], [-80, 760], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Scene glow={AMBER}>
      <div style={kicker}>// launch day</div>
      <Audio src={staticFile("impact.mp3")} from={64} volume={0.7} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 50 }}>
        <div style={{ width: 740, height: 380, borderRadius: 22, background: "#101013", border: `1px solid ${ZINC7}`, overflow: "hidden", opacity: e, transform: `translateY(${(1 - e) * 36}px)`, position: "relative", boxShadow: "0 30px 80px rgba(0,0,0,0.5)" }}>
          <div style={{ height: 54, background: "#18181b", display: "flex", alignItems: "center", gap: 9, padding: "0 22px", borderBottom: `1px solid ${ZINC7}` }}>
            <span style={{ width: 13, height: 13, borderRadius: 999, background: "#ef4444" }} />
            <span style={{ width: 13, height: 13, borderRadius: 999, background: AMBER }} />
            <span style={{ width: 13, height: 13, borderRadius: 999, background: TEAL }} />
            <span style={{ fontFamily: "monospace", color: ZINC4, marginLeft: 14, fontSize: 22 }}>your-app</span>
          </div>
          <div style={{ padding: 28, display: "flex", flexDirection: "column", gap: 16 }}>
            {[0, 1, 2].map((i) => <div key={i} style={{ height: 18, width: `${90 - i * 18}%`, borderRadius: 6, background: "#1c1c20" }} />)}
          </div>
          <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(245,73,73,0.10)", opacity: fail }}>
            <span style={{ fontFamily: BEBAS, fontSize: 96, color: "#ef4444", letterSpacing: 2, transform: `scale(${0.8 + fail * 0.2})` }}>BUILD FAILED</span>
          </div>
          <div style={{ position: "absolute", left: bugX, top: 220 + Math.sin(f / 7) * 30 }}><BugMark size={70} check={0} /></div>
        </div>
        <h1 style={{ ...H(96), opacity: e }}>YOU CAN'T CATCH THE BUG<br /><span style={{ color: AMBER }}>YOU DON'T KNOW YOU WROTE.</span></h1>
      </AbsoluteFill>
    </Scene>
  );
};

// 3 — SIGNAL: you don't have to ship alone
const S3: React.FC = () => {
  const f = useCurrentFrame();
  const e = sp(f, 4, { damping: 12, stiffness: 140 });
  const sub = sp(f, 34);
  return (
    <Scene glow={TEAL}>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 28 }}>
        <div style={{ fontFamily: BEBAS, fontSize: 116, letterSpacing: 2, margin: 0, color: FG, opacity: e, transform: `scale(${0.7 + e * 0.3})` }}>
          QA MASTERY <span style={{ color: TEAL }}>TALENT</span>
        </div>
        <div style={{ ...body, fontSize: 46, color: FG, opacity: sub }}>You don&apos;t have to ship <span style={{ color: TEAL }}>alone.</span></div>
      </AbsoluteFill>
    </Scene>
  );
};

// 4 — PROOF: a tester profile card flies in
const S4: React.FC = () => {
  const f = useCurrentFrame();
  const card = sp(f, 6, { damping: 15 });
  const chip = (i: number) => sp(f, 40 + i * 9, { damping: 14 });
  const devices = ["iPhone 13", "Pixel 7", "Win · Chrome"];
  const tags = ["API", "Mobile", "Regression"];
  return (
    <Scene glow={TEAL}>
      <div style={kicker}>// proof, not promises</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 50 }}>
        <div style={{ width: 720, borderRadius: 24, background: "#101013", border: `1px solid ${ZINC7}`, padding: 34, opacity: card, transform: `translateY(${(1 - card) * 40}px) scale(${0.94 + card * 0.06})`, boxShadow: "0 30px 80px rgba(0,0,0,0.55)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 22, marginBottom: 26 }}>
            <div style={{ width: 96, height: 96, borderRadius: 999, background: `linear-gradient(135deg, ${TEAL}, ${ZINC7})`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: BEBAS, fontSize: 52, color: INK }}>S</div>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              <div style={{ fontFamily: BEBAS, fontSize: 56, color: FG, letterSpacing: 1 }}>sagar-thapa</div>
              <div style={{ display: "flex", gap: 10, opacity: chip(0) }}>
                <span style={{ fontFamily: ROBOTO, fontSize: 26, color: TEAL, border: `1px solid ${TEAL}66`, background: `${TEAL}14`, borderRadius: 999, padding: "4px 16px" }}>✓ Verified · 92%</span>
                <span style={{ fontFamily: ROBOTO, fontSize: 26, color: TEAL, border: `1px solid ${TEAL}66`, background: `${TEAL}14`, borderRadius: 999, padding: "4px 16px" }}>Open to work</span>
              </div>
            </div>
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 12, marginBottom: 18 }}>
            {tags.map((t, i) => (
              <span key={t} style={{ fontFamily: ROBOTO, fontSize: 28, color: "#7dd3fc", border: "1px solid rgba(125,211,252,0.4)", background: "rgba(125,211,252,0.10)", borderRadius: 999, padding: "6px 20px", opacity: chip(i + 1), transform: `translateY(${(1 - chip(i + 1)) * 14}px)` }}>{t}</span>
            ))}
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 12 }}>
            {devices.map((d, i) => (
              <span key={d} style={{ fontFamily: "monospace", fontSize: 26, color: ZINC4, border: `1px solid ${ZINC7}`, background: "#18181b", borderRadius: 10, padding: "6px 16px", opacity: chip(i + 4), transform: `translateY(${(1 - chip(i + 4)) * 14}px)` }}>{d}</span>
            ))}
          </div>
        </div>
        <h1 style={{ ...H(104), opacity: card }}>REAL PROOF. <span style={{ color: TEAL }}>NOT PROMISES.</span></h1>
      </AbsoluteFill>
    </Scene>
  );
};

// 5 — THE CATCH: bug found before launch
const S5: React.FC = () => {
  const f = useCurrentFrame();
  const e = sp(f, 6);
  const msg = sp(f, 30, { damping: 13 });
  const check = interpolate(f, [60, 110], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const glitch = f >= 56 && f <= 64 ? (Math.random() - 0.5) * 14 : 0;
  return (
    <Scene glow={AMBER}>
      <div style={kicker}>// caught</div>
      <Audio src={staticFile("chime.mp3")} from={60} volume={0.6} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 44 }}>
        <div style={{ width: 660, background: "#101013", border: `1px solid ${ZINC7}`, borderRadius: 20, padding: 26, opacity: msg, transform: `translateX(${(1 - msg) * -40 + glitch}px)`, boxShadow: "0 20px 50px rgba(0,0,0,0.4)" }}>
          <div style={{ fontFamily: "monospace", fontSize: 24, color: TEAL, marginBottom: 12 }}>sagar-thapa · now</div>
          <div style={{ fontFamily: ROBOTO, fontSize: 38, color: FG, lineHeight: 1.35 }}>Found it — checkout breaks on <span style={{ color: AMBER }}>Android 13.</span> Repro + fix in the report. 🐛</div>
        </div>
        <BugMark size={180} check={check} />
        <h1 style={{ ...H(100), opacity: e }}>CAUGHT — <span style={{ color: TEAL }}>BEFORE ANYONE SAW IT.</span></h1>
      </AbsoluteFill>
    </Scene>
  );
};

// 6 — SCALE + CTA
const S6: React.FC = () => {
  const f = useCurrentFrame();
  const e = sp(f, 4, { damping: 12 });
  const pill = sp(f, 46, { damping: 10, stiffness: 130 });
  const pulse = 1 + Math.sin(f / 9) * 0.03;
  const avatars = [0, 1, 2, 3, 4];
  return (
    <Scene glow={TEAL}>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 34 }}>
        <div style={{ display: "flex", marginBottom: 10 }}>
          {avatars.map((i) => {
            const ae = sp(f, 6 + i * 7, { damping: 13 });
            return (
              <div key={i} style={{ width: 84, height: 84, borderRadius: 999, marginLeft: i === 0 ? 0 : -22, background: i === 2 ? `linear-gradient(135deg, ${TEAL}, ${ZINC7})` : "#18181b", border: `2px solid ${INK}`, opacity: ae, transform: `scale(${0.5 + ae * 0.5})`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: BEBAS, fontSize: 38, color: i === 2 ? INK : ZINC4 }}>
                {i === 2 ? "S" : "+"}
              </div>
            );
          })}
        </div>
        <h1 style={{ ...H(120), opacity: e, transform: `translateY(${(1 - e) * 20}px)` }}>
          EVERY PRODUCT STARTS<br />WITH <span style={{ color: TEAL }}>ONE PERSON.</span>
        </h1>
        <div style={{ ...body, fontSize: 36, color: ZINC4 }}>The good ones don&apos;t stay that way.</div>
        <div style={{ opacity: pill, transform: `scale(${pulse})`, background: TEAL, color: INK, fontFamily: BEBAS, fontSize: 56, letterSpacing: 1, padding: "22px 60px", borderRadius: 999, marginTop: 8 }}>
          ADD YOUR FIRST TESTER — FREE
        </div>
        <div style={{ fontFamily: "monospace", fontSize: 28, color: ZINC4 }}>qa-mastery-platform.vercel.app</div>
      </AbsoluteFill>
    </Scene>
  );
};

const SCENES = [S1, S2, S3, S4, S5, S6];

const Wrap: React.FC<{ i: number; dur: number }> = ({ i, dur }) => {
  const f = useCurrentFrame();
  const C = SCENES[i];
  return (
    <AbsoluteFill style={{ opacity: fadeOut(f, dur) }}>
      <C />
      <Audio src={staticFile("whoosh.mp3")} volume={0.35} />
      <Audio src={staticFile(`vot-${i + 1}.mp3`)} volume={1} />
    </AbsoluteFill>
  );
};

export const TalentLaunch: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: INK }}>
    <Audio src={staticFile("bed.mp3")} volume={0.22} loop />
    <Series>
      {D.map((dur, i) => (
        <Series.Sequence key={i} durationInFrames={dur}>
          <Wrap i={i} dur={dur} />
        </Series.Sequence>
      ))}
    </Series>
  </AbsoluteFill>
);
