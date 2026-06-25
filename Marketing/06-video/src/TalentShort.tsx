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

// "Scale Without the Overhead" — 15s ad cutdown. No VO: text + music + SFX.
// Demand-side: post → match → contact. Fast, 3 beats × 5s.
const D = [150, 150, 150];
export const SHORT_DURATION = D.reduce((a, b) => a + b, 0);

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
const fadeOut = (frame: number, dur: number, len = 10) =>
  interpolate(frame, [dur - len, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

const kicker: React.CSSProperties = {
  fontFamily: "monospace", fontSize: 30, letterSpacing: 3, color: TEAL,
  position: "absolute", top: 150, left: 0, right: 0, textAlign: "center",
};
const H = (size: number): React.CSSProperties => ({
  fontFamily: BEBAS, fontSize: size, lineHeight: 0.92, letterSpacing: 1, color: FG,
  textAlign: "center", margin: 0, padding: "0 80px",
});
const field = (e: number): React.CSSProperties => ({
  height: 60, borderRadius: 12, background: "#18181b", border: `1px solid ${ZINC7}`,
  opacity: e, transform: `translateX(${(1 - e) * -30}px)`, display: "flex", alignItems: "center",
  padding: "0 22px", fontFamily: ROBOTO, fontSize: 30, color: ZINC4, gap: 12,
});

// 1 — Post a project
const S1: React.FC = () => {
  const f = useCurrentFrame();
  const card = sp(f, 4, { damping: 14 });
  const rows = ["Project type — Mobile app", "Testing — API · Regression · Real-device", "Engagement — Per-project"];
  return (
    <Scene glow={TEAL}>
      <div style={kicker}>// need QA?</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 44 }}>
        <div style={{ width: 760, borderRadius: 22, background: "#101013", border: `1px solid ${ZINC7}`, padding: 30, opacity: card, transform: `translateY(${(1 - card) * 36}px)`, display: "flex", flexDirection: "column", gap: 16, boxShadow: "0 30px 80px rgba(0,0,0,0.55)" }}>
          <div style={{ fontFamily: BEBAS, fontSize: 44, color: FG, letterSpacing: 1 }}>POST A PROJECT</div>
          {rows.map((r, i) => {
            const re = sp(f, 18 + i * 12, { damping: 16 });
            return <div key={r} style={field(re)}><span style={{ color: TEAL }}>✓</span> {r}</div>;
          })}
        </div>
        <h1 style={{ ...H(120), opacity: card }}>NEED QA? <span style={{ color: TEAL }}>POST IT.</span></h1>
      </AbsoluteFill>
    </Scene>
  );
};

// 2 — Matched testers
const S2: React.FC = () => {
  const f = useCurrentFrame();
  const chips = ["API", "Mobile", "iPhone 13", "Pixel 7"];
  return (
    <Scene glow={TEAL}>
      <div style={kicker}>// matched to your stack</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 40 }}>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 12, width: 760, justifyContent: "center" }}>
          {chips.map((c, i) => {
            const ce = sp(f, 6 + i * 7, { damping: 13 });
            return <span key={c} style={{ fontFamily: ROBOTO, fontSize: 30, color: TEAL, border: `1px solid ${TEAL}66`, background: `${TEAL}14`, borderRadius: 999, padding: "8px 24px", opacity: ce, transform: `scale(${0.8 + ce * 0.2})` }}>{c}</span>;
          })}
        </div>
        <div style={{ display: "flex", gap: 16 }}>
          {[0, 1, 2].map((i) => {
            const ce = sp(f, 40 + i * 12, { damping: 14 });
            return (
              <div key={i} style={{ width: 200, borderRadius: 16, background: "#101013", border: `1px solid ${ZINC7}`, padding: 18, opacity: ce, transform: `translateY(${(1 - ce) * 30}px)`, display: "flex", flexDirection: "column", gap: 10 }}>
                <div style={{ width: 56, height: 56, borderRadius: 999, background: `linear-gradient(135deg, ${TEAL}, ${ZINC7})` }} />
                <div style={{ height: 10, width: "70%", borderRadius: 5, background: ZINC7 }} />
                <div style={{ height: 22, width: 110, borderRadius: 999, background: `${TEAL}22`, border: `1px solid ${TEAL}55` }} />
              </div>
            );
          })}
        </div>
        <h1 style={{ ...H(96), opacity: sp(f, 30) }}>MATCHED TO YOUR<br /><span style={{ color: TEAL }}>STACK & DEVICES.</span></h1>
      </AbsoluteFill>
    </Scene>
  );
};

// 3 — Contact + CTA
const S3: React.FC = () => {
  const f = useCurrentFrame();
  const e = sp(f, 4, { damping: 12 });
  const pill = sp(f, 34, { damping: 10, stiffness: 130 });
  const pulse = 1 + Math.sin(f / 9) * 0.03;
  return (
    <Scene glow={TEAL}>
      <Audio src={staticFile("chime.mp3")} from={30} volume={0.6} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 34 }}>
        <h1 style={{ ...H(130), opacity: e, transform: `translateY(${(1 - e) * 20}px)` }}>
          TESTING STARTS <span style={{ color: TEAL }}>TODAY.</span>
        </h1>
        <div style={{ fontFamily: BEBAS, fontSize: 88, letterSpacing: 2, color: FG }}>QA MASTERY <span style={{ color: TEAL }}>TALENT</span></div>
        <div style={{ opacity: pill, transform: `scale(${pulse})`, background: TEAL, color: INK, fontFamily: BEBAS, fontSize: 54, letterSpacing: 1, padding: "20px 56px", borderRadius: 999 }}>
          ADD YOUR FIRST TESTER — FREE
        </div>
        <div style={{ fontFamily: "monospace", fontSize: 28, color: ZINC4 }}>qa-mastery-platform.vercel.app</div>
      </AbsoluteFill>
    </Scene>
  );
};

const SCENES = [S1, S2, S3];

const Wrap: React.FC<{ i: number; dur: number }> = ({ i, dur }) => {
  const f = useCurrentFrame();
  const C = SCENES[i];
  return (
    <AbsoluteFill style={{ opacity: fadeOut(f, dur) }}>
      <C />
      <Audio src={staticFile("whoosh.mp3")} volume={0.35} />
    </AbsoluteFill>
  );
};

export const TalentShort: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: INK }}>
    <Audio src={staticFile("bed.mp3")} volume={0.5} loop />
    <Series>
      {D.map((dur, i) => (
        <Series.Sequence key={i} durationInFrames={dur}>
          <Wrap i={i} dur={dur} />
        </Series.Sequence>
      ))}
    </Series>
  </AbsoluteFill>
);
