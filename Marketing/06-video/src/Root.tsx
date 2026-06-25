import { Composition } from "remotion";
import { Intro, INTRO_DURATION } from "./Intro";
import { WhyDifferent, WHY_DURATION } from "./WhyDifferent";
import { TalentLaunch, TALENT_DURATION } from "./TalentLaunch";
import { TalentShort, SHORT_DURATION } from "./TalentShort";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Intro"
        component={Intro}
        durationInFrames={INTRO_DURATION}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="WhyDifferent"
        component={WhyDifferent}
        durationInFrames={WHY_DURATION}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="TalentLaunch"
        component={TalentLaunch}
        durationInFrames={TALENT_DURATION}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="TalentLaunchWide"
        component={TalentLaunch}
        durationInFrames={TALENT_DURATION}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="TalentShort"
        component={TalentShort}
        durationInFrames={SHORT_DURATION}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
