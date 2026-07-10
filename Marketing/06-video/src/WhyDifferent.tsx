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

// Scene durations (frames @30) sized to the why-*.mp3 clips + tail; CTA padded.
const D = [270, 337, 165, 282, 294, 259, 316, 194];
export const WHY_DURATION = D.reduce((a, b) => a + b, 0);

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

// 1 — Hook: identical "course" cards (sameness)
const S1: React.FC = () => {
  const f = useCurrentFrame();
  const e = sp(f, 70);
  return (
    <Scene glow={ZINC7}>
      <div style={kicker}>// every qa course</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div style={{ display: "flex", gap: 18, marginBottom: 56 }}>
          {[0, 1, 2, 3].map((i) => {
            const ce = sp(f, 8 + i * 8, { damping: 14 });
            return (
              <div key={i} style={{ width: 150, height: 200, borderRadius: 14, background: "#18181b", border: `1px solid ${ZINC7}`, opacity: ce, transform: `translateY(${(1 - ce) * 40}px)`, display: "flex", flexDirection: "column", gap: 10, padding: 16 }}>
                <div style={{ width: 40, height: 40, borderRadius: 999, background: ZINC7, display: "flex", alignItems: "center", justifyContent: "center", color: ZINC4 }}>▶</div>
                <div style={{ height: 8, background: ZINC7, borderRadius: 4 }} />
                <div style={{ height: 8, width: "70%", background: "#27272a", borderRadius: 4 }} />
              </div>
            );
          })}
        </div>
        <h1 style={{ ...H(120), opacity: sp(f, 90), transform: `translateY(${(1 - sp(f, 90)) * 24}px)` }}>
          EVERY QA COURSE<br />SAYS THE <span style={{ color: ZINC4 }}>SAME THING.</span>
        </h1>
      </AbsoluteFill>
    </Scene>
  );
};

// 2 — Problem: watch/quiz/cert/repeat → still froze
const S2: React.FC = () => {
  const f = useCurrentFrame();
  const froze = sp(f, 245, { damping: 12 });
  const words = ["WATCH.", "QUIZ.", "CERTIFICATE.", "REPEAT."];
  return (
    <Scene glow={AMBER}>
      <div style={kicker}>// the loop</div>
      <Audio src={staticFile("impact.mp3")} from={245} volume={0.7} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 30 }}>
        <div style={{ display: "flex", flexDirection: "column", gap: 14, opacity: interpolate(f, [205, 240], [1, 0.25], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>
          {words.map((w, i) => {
            const ie = sp(f, 16 + i * 32, { damping: 18 });
            return (
              <div key={w} style={{ fontFamily: BEBAS, fontSize: 86, color: ZINC4, letterSpacing: 1, opacity: ie, transform: `translateX(${(1 - ie) * -40}px)` }}>{w}</div>
            );
          })}
        </div>
        <h1 style={{ ...H(150), color: AMBER, opacity: froze, transform: `scale(${0.8 + froze * 0.2})` }}>STILL FROZE.</h1>
      </AbsoluteFill>
    </Scene>
  );
};

// 3 — Turn: logo
const S3: React.FC = () => {
  const f = useCurrentFrame();
  const e = sp(f, 4, { damping: 12, stiffness: 140 });
  const sub = sp(f, 30);
  return (
    <Scene glow={TEAL}>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 28 }}>
        <h1 style={{ fontFamily: BEBAS, fontSize: 190, letterSpacing: 2, margin: 0, color: FG, opacity: e, transform: `scale(${0.6 + e * 0.4})` }}>
          BUILT <span style={{ color: TEAL }}>DIFFERENT.</span>
        </h1>
        <div style={{ ...body, fontSize: 40, color: ZINC4, opacity: sub }}>Four ways. Here's how.</div>
      </AbsoluteFill>
    </Scene>
  );
};

// 4 — Diff 1: you do it (BuggyShop)
const S4: React.FC = () => {
  const f = useCurrentFrame();
  const e = sp(f, 6);
  const bugX = interpolate(f, [40, 250], [-100, 720], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Scene glow={AMBER}>
      <div style={kicker}>// difference 01</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 50 }}>
        <div style={{ width: 740, height: 420, borderRadius: 22, background: "#101013", border: `1px solid ${ZINC7}`, overflow: "hidden", opacity: e, transform: `translateY(${(1 - e) * 36}px)`, position: "relative", boxShadow: "0 30px 80px rgba(0,0,0,0.5)" }}>
          <div style={{ height: 54, background: "#18181b", display: "flex", alignItems: "center", gap: 9, padding: "0 22px", borderBottom: `1px solid ${ZINC7}` }}>
            <span style={{ width: 13, height: 13, borderRadius: 999, background: "#ef4444" }} />
            <span style={{ width: 13, height: 13, borderRadius: 999, background: AMBER }} />
            <span style={{ width: 13, height: 13, borderRadius: 999, background: TEAL }} />
            <span style={{ fontFamily: "monospace", color: ZINC4, marginLeft: 14, fontSize: 22 }}>BuggyShop</span>
          </div>
          <div style={{ padding: 28, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
            {[0, 1, 2, 3].map((i) => <div key={i} style={{ height: 110, borderRadius: 12, background: "#18181b", border: `1px solid ${ZINC7}` }} />)}
          </div>
          <div style={{ position: "absolute", left: bugX, top: 250 + Math.sin(f / 8) * 36 }}><BugMark size={84} check={0} /></div>
        </div>
        <h1 style={{ ...H(130), opacity: e }}>YOU DON'T WATCH. <span style={{ color: TEAL }}>YOU DO IT.</span></h1>
      </AbsoluteFill>
    </Scene>
  );
};

// 5 — Diff 2: graded for real
const S5: React.FC = () => {
  const f = useCurrentFrame();
  const check = interpolate(f, [70, 150], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const e = sp(f, 6);
  return (
    <Scene glow={TEAL}>
      <div style={kicker}>// difference 02</div>
      <Audio src={staticFile("chime.mp3")} from={150} volume={0.6} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 44 }}>
        <BugMark size={300} check={check} />
        <h1 style={{ ...H(130), opacity: e }}>GRADED <span style={{ color: TEAL }}>FOR REAL.</span></h1>
        <div style={{ ...body, fontSize: 36 }}>Server-side, against a real answer key. <span style={{ color: FG }}>You can't fake it.</span></div>
      </AbsoluteFill>
    </Scene>
  );
};

// 6 — Diff 3: graded portfolio
const S6: React.FC = () => {
  const f = useCurrentFrame();
  const e = sp(f, 6);
  return (
    <Scene glow={TEAL}>
      <div style={kicker}>// difference 03</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 50 }}>
        <div style={{ position: "relative", width: 620, height: 330 }}>
          {[0, 1, 2].map((i) => {
            const ie = sp(f, 12 + i * 12, { damping: 15 });
            return (
              <div key={i} style={{ position: "absolute", left: 70 + i * 34, top: 26 + i * 46, width: 440, height: 180, borderRadius: 16, background: "#101013", border: `1px solid ${ZINC7}`, opacity: ie, transform: `translateY(${(1 - ie) * 28}px)`, padding: 24, display: "flex", flexDirection: "column", gap: 12, boxShadow: "0 20px 50px rgba(0,0,0,0.4)" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}><span style={{ color: TEAL, fontSize: 28 }}>✓</span><div style={{ height: 12, width: 200, borderRadius: 6, background: ZINC7 }} /></div>
                <div style={{ height: 9, width: "80%", borderRadius: 5, background: "#27272a" }} />
                <div style={{ height: 9, width: "55%", borderRadius: 5, background: "#27272a" }} />
              </div>
            );
          })}
        </div>
        <h1 style={{ ...H(110), opacity: e }}>A <span style={{ color: TEAL }}>GRADED PORTFOLIO.</span><br />NOT A CERTIFICATE.</h1>
      </AbsoluteFill>
    </Scene>
  );
};

// 7 — Diff 4: free / real / in the open
const S7: React.FC = () => {
  const f = useCurrentFrame();
  const chips = ["FREE FIRST MODULE", "JAVA + SELENIUM", "BUILT IN PUBLIC"];
  return (
    <Scene glow={TEAL}>
      <div style={kicker}>// difference 04</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 30 }}>
        {chips.map((c, i) => {
          const ie = sp(f, 18 + i * 95, { damping: 14, stiffness: 130 });
          return (
            <div key={c} style={{ fontFamily: BEBAS, fontSize: 80, letterSpacing: 1, color: i === 0 ? TEAL : FG, opacity: ie, transform: `scale(${0.85 + ie * 0.15})` }}>{c}</div>
          );
        })}
      </AbsoluteFill>
    </Scene>
  );
};

// 8 — CTA
const S8: React.FC = () => {
  const f = useCurrentFrame();
  const e = sp(f, 4, { damping: 12 });
  const pill = sp(f, 40, { damping: 10, stiffness: 130 });
  const pulse = 1 + Math.sin(f / 9) * 0.03;
  return (
    <Scene glow={TEAL}>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 36 }}>
        <h1 style={{ ...H(150), opacity: e, transform: `translateY(${(1 - e) * 20}px)` }}>
          STOP WATCHING.<br /><span style={{ color: TEAL }}>START DOING.</span>
        </h1>
        <div style={{ fontFamily: BEBAS, fontSize: 110, letterSpacing: 2, color: FG, marginTop: 6 }}>QA <span style={{ color: TEAL }}>MASTERY</span></div>
        <div style={{ opacity: pill, transform: `scale(${pulse})`, background: TEAL, color: INK, fontFamily: BEBAS, fontSize: 52, letterSpacing: 1, padding: "20px 56px", borderRadius: 999 }}>START FREE</div>
        <div style={{ fontFamily: "monospace", fontSize: 28, color: ZINC4 }}>qa-mastery-platform.vercel.app</div>
      </AbsoluteFill>
    </Scene>
  );
};

const SCENES = [S1, S2, S3, S4, S5, S6, S7, S8];

const Wrap: React.FC<{ i: number; dur: number }> = ({ i, dur }) => {
  const f = useCurrentFrame();
  const C = SCENES[i];
  return (
    <AbsoluteFill style={{ opacity: fadeOut(f, dur) }}>
      <C />
      <Audio src={staticFile(`why-${i + 1}.mp3`)} />
      <Audio src={staticFile("whoosh.mp3")} volume={0.45} />
    </AbsoluteFill>
  );
};

export const WhyDifferent: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: INK }}>
    <Audio src={staticFile("bed.mp3")} volume={0.45} loop />
    <Series>
      {D.map((dur, i) => (
        <Series.Sequence key={i} durationInFrames={dur}>
          <Wrap i={i} dur={dur} />
        </Series.Sequence>
      ))}
    </Series>
  </AbsoluteFill>
);
