import React from "react";
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
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

// Scene durations (frames @30) sized to notes-vo-*.mp3 (Ava voice) + tail.
const D = [207, 222, 195, 222, 186, 138, 270];
export const NOTES_DURATION = D.reduce((a, b) => a + b, 0);

const sp = (frame: number, delay = 0, cfg = { damping: 16, stiffness: 120, mass: 0.8 }) =>
  spring({ frame: frame - delay, fps: 30, config: cfg });
const fadeOut = (frame: number, dur: number, len = 10) =>
  interpolate(frame, [dur - len, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

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

const Tag: React.FC<{ children: string; frame: number }> = ({ children, frame }) => (
  <div
    style={{
      opacity: sp(frame, 4),
      fontFamily: ROBOTO,
      fontSize: 30,
      letterSpacing: 10,
      color: TEAL,
      textTransform: "lowercase",
    }}
  >
    {"// "}
    {children}
  </div>
);

const Big: React.FC<{ lines: [string, string?]; accent?: number; frame: number; size?: number }> = ({
  lines,
  accent,
  frame,
  size = 108,
}) => (
  <div style={{ fontFamily: BEBAS, fontSize: size, lineHeight: 1.02, color: FG }}>
    {lines.map(
      (l, i) =>
        l && (
          <div
            key={i}
            style={{
              color: i === accent ? AMBER : FG,
              transform: `translateY(${(1 - sp(frame, 6 + i * 5)) * 40}px)`,
              opacity: sp(frame, 6 + i * 5),
            }}
          >
            {l}
          </div>
        ),
    )}
  </div>
);

/** Screen-recording card: rounded browser frame, spring-in, slow push-in.
 *  Clips are 2208×1436; the note column is centered, so a centered crop with a
 *  gentle scale-up keeps the interaction in frame. */
const ScreenCard: React.FC<{
  clip: string;
  frame: number;
  dur: number;
  zoom?: number;
  shiftY?: number;
}> = ({ clip, frame, dur, zoom = 1.14, shiftY = 0 }) => {
  const enter = sp(frame, 2, { damping: 18, stiffness: 90, mass: 0.9 });
  const push = interpolate(frame, [0, dur], [1, zoom]);
  return (
    <div
      style={{
        width: 1000,
        height: 1210,
        borderRadius: 28,
        overflow: "hidden",
        border: `2px solid rgba(244,244,245,0.14)`,
        boxShadow: `0 40px 120px -30px ${TEAL}44, 0 12px 40px rgba(0,0,0,0.6)`,
        transform: `translateY(${(1 - enter) * 90}px) scale(${0.96 + enter * 0.04})`,
        opacity: enter,
        background: "#0f0f12",
        position: "relative",
      }}
    >
      {/* faux browser chrome */}
      <div
        style={{
          height: 54,
          display: "flex",
          alignItems: "center",
          gap: 10,
          padding: "0 22px",
          borderBottom: "1px solid rgba(244,244,245,0.08)",
          background: "#101013",
          position: "relative",
          zIndex: 2,
        }}
      >
        {["#ff5f57", "#febc2e", "#28c840"].map((c) => (
          <div key={c} style={{ width: 14, height: 14, borderRadius: 7, background: c }} />
        ))}
        <div
          style={{
            marginLeft: 14,
            fontFamily: ROBOTO,
            fontSize: 20,
            color: ZINC4,
            background: "rgba(244,244,245,0.06)",
            borderRadius: 8,
            padding: "6px 16px",
          }}
        >
          qamastery / notes
        </div>
      </div>
      <div style={{ position: "absolute", inset: 54, overflow: "hidden" }}>
        <OffthreadVideo
          src={staticFile(clip)}
          muted
          style={{
            width: 1780,
            position: "absolute",
            left: "50%",
            top: "50%",
            transform: `translate(-50%, calc(-50% + ${shiftY}px)) scale(${push})`,
          }}
        />
      </div>
    </div>
  );
};

const Caption: React.FC<{ kicker: string; line: string; frame: number; accentColor?: string }> = ({
  kicker,
  line,
  frame,
  accentColor = TEAL,
}) => (
  <div style={{ position: "absolute", left: 60, right: 60, bottom: 96 }}>
    <div
      style={{
        fontFamily: ROBOTO,
        fontSize: 26,
        letterSpacing: 8,
        color: accentColor,
        textTransform: "uppercase",
        opacity: sp(frame, 8),
      }}
    >
      {kicker}
    </div>
    <div
      style={{
        fontFamily: BEBAS,
        fontSize: 84,
        color: FG,
        lineHeight: 1.02,
        marginTop: 8,
        transform: `translateY(${(1 - sp(frame, 12)) * 36}px)`,
        opacity: sp(frame, 12),
      }}
    >
      {line}
    </div>
  </div>
);

/* Scenes */

const S1: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Scene glow={AMBER}>
      <Audio src={staticFile("notes-vo-1.mp3")} />
      <Audio src={staticFile("impact.mp3")} volume={0.7} />
      <AbsoluteFill style={{ justifyContent: "center", padding: "0 90px", opacity: fadeOut(f, D[0]) }}>
        <Tag frame={f}>the problem</Tag>
        <div style={{ height: 28 }} />
        <Big frame={f} lines={["EVERY COURSE", "GIVES YOU NOTES."]} size={116} />
        <div style={{ height: 34 }} />
        <Big frame={f - 55} lines={["NOBODY", "READS THEM."]} accent={1} size={116} />
        <div
          style={{
            marginTop: 60,
            fontFamily: ROBOTO,
            fontSize: 40,
            color: ZINC4,
            opacity: sp(f, 130),
          }}
        >
          So we rebuilt the idea.
        </div>
      </AbsoluteFill>
    </Scene>
  );
};

const S2: React.FC = () => {
  const f = useCurrentFrame();
  const half = 111;
  return (
    <Scene>
      <Audio src={staticFile("notes-vo-2.mp3")} />
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 130, opacity: fadeOut(f, D[1]) }}>
        {f < half ? (
          <ScreenCard clip="notes-clip-hotspot1.mp4" frame={f} dur={half} zoom={1.22} shiftY={-40} />
        ) : (
          <ScreenCard clip="notes-clip-hotspot2.mp4" frame={f - half} dur={half} zoom={1.22} shiftY={-30} />
        )}
      </AbsoluteFill>
      <Caption kicker="notes you tap" line="EVERY PART EXPLAINS ITSELF." frame={f} />
    </Scene>
  );
};

const S3: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Scene>
      <Audio src={staticFile("notes-vo-3.mp3")} />
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 130, opacity: fadeOut(f, D[2]) }}>
        <ScreenCard clip="notes-clip-flow.mp4" frame={f} dur={D[2]} zoom={1.3} shiftY={-20} />
      </AbsoluteFill>
      <Caption kicker="diagrams you play" line="WATCH THE POWER FLOW." frame={f} />
    </Scene>
  );
};

const S4: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Scene glow={AMBER}>
      <Audio src={staticFile("notes-vo-4.mp3")} />
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 130, opacity: fadeOut(f, D[3]) }}>
        <ScreenCard clip="notes-clip-code.mp4" frame={f} dur={D[3]} zoom={1.32} shiftY={10} />
      </AbsoluteFill>
      <Caption kicker="a real compiler, in a note" line="EDIT. RUN. OUTPUT." frame={f} accentColor={AMBER} />
    </Scene>
  );
};

const S5: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Scene>
      <Audio src={staticFile("notes-vo-5.mp3")} />
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 130, opacity: fadeOut(f, D[4]) }}>
        <ScreenCard clip="notes-clip-quiz.mp4" frame={f} dur={D[4]} zoom={1.26} shiftY={0} />
      </AbsoluteFill>
      <Caption kicker="it checks on you" line="THE NOTE QUIZZES YOU BACK." frame={f} />
    </Scene>
  );
};

const S6: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Scene glow={AMBER}>
      <Audio src={staticFile("notes-vo-6.mp3")} />
      <Audio src={staticFile("chime.mp3")} volume={0.8} />
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 130, opacity: fadeOut(f, D[5]) }}>
        <ScreenCard clip="notes-clip-xp.mp4" frame={f} dur={D[5]} zoom={1.34} shiftY={-48} />
      </AbsoluteFill>
      <Caption kicker="finish → xp → streak" line="PROGRESS YOU CAN FEEL." frame={f} accentColor={AMBER} />
    </Scene>
  );
};

const S7: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Scene glow={TEAL}>
      <Audio src={staticFile("notes-vo-7.mp3")} />
      <Audio src={staticFile("impact.mp3")} volume={0.6} />
      <AbsoluteFill style={{ justifyContent: "center", padding: "0 90px" }}>
        <Tag frame={f}>the difference</Tag>
        <div style={{ height: 28 }} />
        <Big frame={f} lines={["READING", "IS WATCHING."]} size={120} />
        <div style={{ height: 30 }} />
        <Big frame={f - 50} lines={["THIS", "IS DOING."]} accent={1} size={120} />
        <div
          style={{
            marginTop: 70,
            opacity: sp(f, 120),
            transform: `translateY(${(1 - sp(f, 120)) * 30}px)`,
          }}
        >
          <div style={{ fontFamily: BEBAS, fontSize: 66, color: TEAL }}>QA MASTERY</div>
          <div style={{ fontFamily: ROBOTO, fontSize: 34, color: ZINC4, marginTop: 10 }}>
            First module free — link in bio.
          </div>
        </div>
      </AbsoluteFill>
    </Scene>
  );
};

export const NotesInteractive: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: INK }}>
    <Audio src={staticFile("bed.mp3")} volume={0.1} loop />
    <Series>
      <Series.Sequence durationInFrames={D[0]}><S1 /></Series.Sequence>
      <Series.Sequence durationInFrames={D[1]}><S2 /></Series.Sequence>
      <Series.Sequence durationInFrames={D[2]}><S3 /></Series.Sequence>
      <Series.Sequence durationInFrames={D[3]}><S4 /></Series.Sequence>
      <Series.Sequence durationInFrames={D[4]}><S5 /></Series.Sequence>
      <Series.Sequence durationInFrames={D[5]}><S6 /></Series.Sequence>
      <Series.Sequence durationInFrames={D[6]}><S7 /></Series.Sequence>
    </Series>
  </AbsoluteFill>
);
