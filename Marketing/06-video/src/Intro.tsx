import React from "react";
import {
  AbsoluteFill,
  Audio,
  Series,
  Sequence,
  staticFile,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { loadFont as loadBebas } from "@remotion/google-fonts/BebasNeue";
import { loadFont as loadRoboto } from "@remotion/google-fonts/Roboto";

const { fontFamily: BEBAS } = loadBebas();
const { fontFamily: ROBOTO } = loadRoboto();

// Brand tokens (match qa-mastery globals.css)
const INK = "#09090b";
const FG = "#f4f4f5";
const TEAL = "#2dd4a7";
const AMBER = "#f5b948";
const ZINC4 = "#a1a1aa";
const ZINC7 = "#3f3f46";

// Scene durations in frames @30fps (sized to each VO clip + tail)
const D = [182, 202, 165, 184, 240, 160, 200];
export const INTRO_DURATION = D.reduce((a, b) => a + b, 0); // 1419 ≈ 47s

// ── shared atmosphere ────────────────────────────────────────────────
const Grid: React.FC = () => (
  <AbsoluteFill
    style={{
      backgroundImage:
        "linear-gradient(rgba(244,244,245,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(244,244,245,0.05) 1px, transparent 1px)",
      backgroundSize: "70px 70px",
    }}
  />
);

const Glow: React.FC<{ color?: string }> = ({ color = TEAL }) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(60% 40% at 50% 0%, ${color}22, transparent 70%)`,
    }}
  />
);

const SceneBG: React.FC<{ children: React.ReactNode; glow?: string; light?: boolean }> = ({
  children,
  glow,
  light,
}) => (
  <AbsoluteFill style={{ backgroundColor: light ? "#fafafa" : INK, overflow: "hidden" }}>
    {!light && <Grid />}
    {!light && <Glow color={glow} />}
    {children}
  </AbsoluteFill>
);

const useEnter = (delay = 0, cfg = { damping: 18, stiffness: 120, mass: 0.8 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - delay, fps, config: cfg });
};

const fadeOut = (frame: number, dur: number, len = 12) =>
  interpolate(frame, [dur - len, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

// bug-caught-in-checkmark motif (teal check + amber bug)
const BugMark: React.FC<{ size?: number; check?: number; bug?: number }> = ({
  size = 240,
  check = 1,
  bug = 1,
}) => (
  <svg width={size} height={size} viewBox="0 0 100 100" fill="none">
    <path
      d="M20 55 L42 78 L84 26"
      stroke={TEAL}
      strokeWidth={10}
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeDasharray={120}
      strokeDashoffset={120 - 120 * check}
    />
    <g transform="translate(60,60)" opacity={bug}>
      <ellipse cx="0" cy="0" rx="11" ry="14" fill={AMBER} />
      <line x1="-11" y1="-6" x2="-22" y2="-12" stroke={AMBER} strokeWidth="3" strokeLinecap="round" />
      <line x1="-13" y1="2" x2="-25" y2="2" stroke={AMBER} strokeWidth="3" strokeLinecap="round" />
      <line x1="-11" y1="9" x2="-21" y2="16" stroke={AMBER} strokeWidth="3" strokeLinecap="round" />
      <line x1="0" y1="-14" x2="0" y2="-22" stroke={AMBER} strokeWidth="3" strokeLinecap="round" />
    </g>
  </svg>
);

const kicker: React.CSSProperties = {
  fontFamily: "monospace",
  fontSize: 30,
  letterSpacing: 3,
  color: TEAL,
  position: "absolute",
  top: 150,
  left: 0,
  right: 0,
  textAlign: "center",
};
const H = (size: number): React.CSSProperties => ({
  fontFamily: BEBAS,
  fontSize: size,
  lineHeight: 0.92,
  letterSpacing: 1,
  color: FG,
  textAlign: "center",
  margin: 0,
  padding: "0 80px",
});
const body: React.CSSProperties = {
  fontFamily: ROBOTO,
  fontSize: 40,
  lineHeight: 1.4,
  color: ZINC4,
  textAlign: "center",
  padding: "0 110px",
};

// ── Scene 1 — Hook ───────────────────────────────────────────────────
const S1: React.FC = () => {
  const f = useCurrentFrame();
  const e = useEnter(6);
  const cards = [0, 1, 2, 3, 4];
  return (
    <SceneBG glow={AMBER} >
      <div style={kicker}>// the problem</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div style={{ position: "relative", height: 420, width: 620, marginBottom: 40 }}>
          {cards.map((i) => {
            const ce = spring({ frame: f - 10 - i * 7, fps: 30, config: { damping: 14 } });
            return (
              <div
                key={i}
                style={{
                  position: "absolute",
                  left: 60,
                  right: 60,
                  top: 30 + i * 64,
                  height: 56,
                  borderRadius: 12,
                  background: "#18181b",
                  border: `1px solid ${ZINC7}`,
                  display: "flex",
                  alignItems: "center",
                  gap: 16,
                  padding: "0 22px",
                  opacity: ce,
                  transform: `translateY(${(1 - ce) * 40}px)`,
                }}
              >
                <div style={{ width: 30, height: 30, borderRadius: 999, background: ZINC7, color: ZINC4, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 }}>▶</div>
                <div style={{ height: 8, borderRadius: 4, background: ZINC7, flex: 1 }} />
                <div style={{ fontFamily: "monospace", fontSize: 20, color: "#52525b" }}>{`${(i + 1) * 17}:00`}</div>
              </div>
            );
          })}
        </div>
        <h1 style={{ ...H(150), opacity: e, transform: `translateY(${(1 - e) * 30}px)` }}>
          100 HOURS OF TUTORIALS.
          <br />
          <span style={{ color: AMBER }}>STILL FROZE DAY ONE.</span>
        </h1>
      </AbsoluteFill>
    </SceneBG>
  );
};

// ── Scene 2 — Problem ────────────────────────────────────────────────
const S2: React.FC = () => {
  const f = useCurrentFrame();
  const e = useEnter(4);
  const items = ["No one grades your work.", "No one tells you what to test.", "You never actually do it."];
  return (
    <SceneBG glow={AMBER}>
      <div style={kicker}>// why it fails</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 60 }}>
        <h1 style={{ ...H(160), opacity: e, transform: `scale(${0.9 + e * 0.1})` }}>
          WATCHING <span style={{ color: AMBER }}>ISN'T</span> DOING.
        </h1>
        <div style={{ display: "flex", flexDirection: "column", gap: 26 }}>
          {items.map((t, i) => {
            const ie = spring({ frame: f - 40 - i * 16, fps: 30, config: { damping: 16 } });
            return (
              <div key={i} style={{ ...body, fontSize: 42, color: FG, opacity: ie, transform: `translateX(${(1 - ie) * -30}px)`, display: "flex", alignItems: "center", gap: 18, padding: 0 }}>
                <span style={{ color: AMBER, fontSize: 44 }}>✕</span> {t}
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </SceneBG>
  );
};

// ── Scene 3 — Turn / logo ────────────────────────────────────────────
const S3: React.FC = () => {
  const e = useEnter(6, { damping: 12, stiffness: 140, mass: 0.9 });
  const sub = useEnter(34);
  return (
    <SceneBG glow={TEAL}>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 40 }}>
        <h1 style={{ fontFamily: BEBAS, fontSize: 200, letterSpacing: 2, margin: 0, color: FG, transform: `scale(${0.6 + e * 0.4})`, opacity: e }}>
          QA <span style={{ color: TEAL }}>MASTERY</span>
        </h1>
        <div style={{ ...body, fontSize: 46, color: FG, opacity: sub, transform: `translateY(${(1 - sub) * 20}px)` }}>
          You don't watch testing. <span style={{ color: TEAL }}>You do it.</span>
        </div>
      </AbsoluteFill>
    </SceneBG>
  );
};

// ── Scene 4 — BuggyShop ──────────────────────────────────────────────
const S4: React.FC = () => {
  const f = useCurrentFrame();
  const e = useEnter(6);
  const bugX = interpolate(f, [40, 150], [-120, 760], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const bugY = 250 + Math.sin(f / 8) * 40;
  return (
    <SceneBG glow={AMBER}>
      <div style={kicker}>// the practice ground</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 56 }}>
        <div style={{ width: 760, height: 460, borderRadius: 22, background: "#101013", border: `1px solid ${ZINC7}`, overflow: "hidden", opacity: e, transform: `translateY(${(1 - e) * 40}px) scale(${0.92 + e * 0.08})`, position: "relative", boxShadow: "0 30px 80px rgba(0,0,0,0.5)" }}>
          <div style={{ height: 56, background: "#18181b", display: "flex", alignItems: "center", gap: 10, padding: "0 22px", borderBottom: `1px solid ${ZINC7}` }}>
            <span style={{ width: 14, height: 14, borderRadius: 999, background: "#ef4444" }} />
            <span style={{ width: 14, height: 14, borderRadius: 999, background: AMBER }} />
            <span style={{ width: 14, height: 14, borderRadius: 999, background: TEAL }} />
            <span style={{ fontFamily: "monospace", color: ZINC4, marginLeft: 16, fontSize: 22 }}>BuggyShop</span>
          </div>
          <div style={{ padding: 30, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 22 }}>
            {[0, 1, 2, 3].map((i) => (
              <div key={i} style={{ height: 120, borderRadius: 12, background: "#18181b", border: `1px solid ${ZINC7}` }} />
            ))}
          </div>
          <div style={{ position: "absolute", left: bugX, top: bugY }}>
            <BugMark size={90} check={0} bug={1} />
          </div>
        </div>
        <h1 style={{ ...H(120), opacity: e }}>
          MEET <span style={{ color: AMBER }}>BUGGYSHOP</span>
        </h1>
      </AbsoluteFill>
    </SceneBG>
  );
};

// ── Scene 5 — Find / Report / Graded ─────────────────────────────────
const S5: React.FC = () => {
  const f = useCurrentFrame();
  const check = interpolate(f, [70, 130], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const steps = ["FIND IT", "REPORT IT", "GET GRADED"];
  return (
    <SceneBG glow={TEAL}>
      <div style={kicker}>// the loop</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 50 }}>
        <div style={{ transform: "translateY(-10px)" }}>
          <BugMark size={300} check={check} bug={1 - check * 0.15} />
        </div>
        <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
          {steps.map((s, i) => {
            const ie = spring({ frame: f - 20 - i * 18, fps: 30, config: { damping: 16 } });
            return (
              <React.Fragment key={s}>
                {i > 0 && <span style={{ color: ZINC7, fontSize: 48, opacity: ie }}>→</span>}
                <div style={{ fontFamily: BEBAS, fontSize: 64, letterSpacing: 1, color: i === 2 ? TEAL : FG, opacity: ie, transform: `translateY(${(1 - ie) * 24}px)` }}>{s}</div>
              </React.Fragment>
            );
          })}
        </div>
        <div style={{ ...body, fontSize: 36, color: ZINC4 }}>
          Server-side grading. A real answer key. <span style={{ color: FG }}>No faking it.</span>
        </div>
      </AbsoluteFill>
    </SceneBG>
  );
};

// ── Scene 6 — Portfolio / proof ──────────────────────────────────────
const S6: React.FC = () => {
  const f = useCurrentFrame();
  const e = useEnter(6);
  return (
    <SceneBG glow={TEAL}>
      <div style={kicker}>// the payoff</div>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 56 }}>
        <div style={{ position: "relative", width: 640, height: 360 }}>
          {[0, 1, 2].map((i) => {
            const ie = spring({ frame: f - 14 - i * 12, fps: 30, config: { damping: 15 } });
            return (
              <div key={i} style={{ position: "absolute", left: 80 + i * 30, top: 30 + i * 50, width: 460, height: 200, borderRadius: 16, background: "#101013", border: `1px solid ${ZINC7}`, opacity: ie, transform: `translateY(${(1 - ie) * 30}px)`, padding: 26, display: "flex", flexDirection: "column", gap: 14, boxShadow: "0 20px 50px rgba(0,0,0,0.4)" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ color: TEAL, fontSize: 30 }}>✓</span>
                  <div style={{ height: 14, width: 220, borderRadius: 6, background: ZINC7 }} />
                </div>
                <div style={{ height: 10, width: "80%", borderRadius: 5, background: "#27272a" }} />
                <div style={{ height: 10, width: "60%", borderRadius: 5, background: "#27272a" }} />
              </div>
            );
          })}
        </div>
        <h1 style={{ ...H(110), opacity: e }}>
          A <span style={{ color: TEAL }}>GRADED PORTFOLIO</span><br />THAT PROVES IT.
        </h1>
      </AbsoluteFill>
    </SceneBG>
  );
};

// ── Scene 7 — CTA ────────────────────────────────────────────────────
const S7: React.FC = () => {
  const f = useCurrentFrame();
  const e = useEnter(6, { damping: 12 });
  const pill = useEnter(36, { damping: 10, stiffness: 130 });
  const pulse = 1 + Math.sin(f / 9) * 0.03;
  return (
    <SceneBG glow={TEAL}>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 44 }}>
        <BugMark size={150} check={Math.min(1, f / 30)} bug={1} />
        <h1 style={{ fontFamily: BEBAS, fontSize: 170, letterSpacing: 2, margin: 0, color: FG, opacity: e, transform: `scale(${0.7 + e * 0.3})` }}>
          QA <span style={{ color: TEAL }}>MASTERY</span>
        </h1>
        <div style={{ ...body, fontSize: 44, color: FG }}>Learn testing by doing.</div>
        <div style={{ marginTop: 20, opacity: pill, transform: `scale(${pulse})`, background: TEAL, color: INK, fontFamily: BEBAS, fontSize: 56, letterSpacing: 1, padding: "22px 60px", borderRadius: 999 }}>
          START FREE
        </div>
        <div style={{ fontFamily: "monospace", fontSize: 30, color: ZINC4, marginTop: 10 }}>qa-mastery-platform.vercel.app</div>
      </AbsoluteFill>
    </SceneBG>
  );
};

const SCENES = [S1, S2, S3, S4, S5, S6, S7];

const SceneWrap: React.FC<{ idx: number; dur: number }> = ({ idx, dur }) => {
  const frame = useCurrentFrame();
  const Comp = SCENES[idx];
  return (
    <AbsoluteFill style={{ opacity: fadeOut(frame, dur) }}>
      <Comp />
      {/* per-scene voiceover */}
      <Audio src={staticFile(`vo-${idx + 1}.mp3`)} />
      {/* transition whoosh at scene start */}
      <Audio src={staticFile("whoosh.mp3")} volume={0.5} />
    </AbsoluteFill>
  );
};

export const Intro: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: INK }}>
      {/* ambient music bed across the whole video */}
      <Audio src={staticFile("bed.mp3")} volume={0.5} />
      <Series>
        {D.map((dur, i) => (
          <Series.Sequence key={i} durationInFrames={dur}>
            <SceneWrap idx={i} dur={dur} />
          </Series.Sequence>
        ))}
      </Series>
    </AbsoluteFill>
  );
};
