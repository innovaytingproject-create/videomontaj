import { Composition } from "remotion";
import { MyComposition } from "./Composition";
import { Edit, WhiedaReel } from "./WhiedaReel";
import video16 from "./edits/video16.json";
import video16full from "./edits/video16-full.json";
import video12 from "./edits/video12.json";
import video17 from "./edits/video17.json";
import video18 from "./edits/video18.json";

const reel = (id: string, edit: Edit) => (
  <Composition
    id={id}
    component={WhiedaReel}
    durationInFrames={Math.round(edit.duration * 30)}
    fps={30}
    width={1080}
    height={1920}
    defaultProps={{ edit }}
  />
);

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <MyComposition />
      {reel("Video16-Maqsad-15s", video16 as Edit)}
      {reel("Video16-Maqsad-Full", video16full as Edit)}
      {reel("Video12-Ishonchlar", video12 as Edit)}
      {reel("Video17-Orzu", video17 as Edit)}
      {reel("Video18-Odamlar", video18 as Edit)}
    </>
  );
};
