import {
  AbsoluteFill,
  Composition,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// Smoke-test composition: confirms the render pipeline works end to end.
export const MyComposition = () => {
  return (
    <>
      <Composition
        id="TestReel"
        component={TestTitle}
        durationInFrames={90}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="TestYouTube"
        component={TestTitle}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};

const TestTitle: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 200 } });
  const opacity = interpolate(frame, [0, 12], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0b0b0c",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          color: "#f4f1ea",
          fontFamily: "Inter, system-ui, sans-serif",
          fontSize: 96,
          fontWeight: 700,
          letterSpacing: "-0.03em",
          opacity,
          transform: `translateY(${(1 - enter) * 40}px)`,
        }}
      >
        Готово к монтажу
      </div>
    </AbsoluteFill>
  );
};
