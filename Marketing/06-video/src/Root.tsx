import { Composition } from "remotion";
import { Intro, INTRO_DURATION } from "./Intro";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Intro"
      component={Intro}
      durationInFrames={INTRO_DURATION}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
