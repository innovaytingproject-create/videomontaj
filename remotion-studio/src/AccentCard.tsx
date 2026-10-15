import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  random,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// Full-screen accent card: animated background, a thin line + big words that
// rise in line by line, the *accent* words marked (yellow marker on white,
// glowing yellow on black), an icon popping in. The voice keeps playing under it.

export type Card = {
  start: number;
  end: number;
  thin: string;
  big: string; // "|" = new line, *word* = accent
  theme: "white" | "black";
  icon?: string; // assets/icons/<icon>-blue.png (white) | -white.png (black)
  numeric?: boolean; // first line extra large (numbers like 100+)
  enter?: "circle" | "wipe" | "zoom";
  exit?: "slide" | "zoom";
};

const INK = "#1D1D1F";
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const WhiteBg: React.FC<{ frame: number }> = ({ frame }) => {
  const blob = (x: number, y: number, r: number, color: string, sx: number, sy: number) => (
    <div
      style={{
        position: "absolute",
        left: x + Math.sin(frame / sx) * 120 - r,
        top: y + Math.cos(frame / sy) * 140 - r,
        width: r * 2,
        height: r * 2,
        borderRadius: "50%",
        background: `radial-gradient(circle, ${color} 0%, rgba(255,255,255,0) 70%)`,
      }}
    />
  );
  return (
    <AbsoluteFill style={{ background: "linear-gradient(180deg, #FFFFFF 0%, #F5F5F7 45%, #EAF3FF 100%)" }}>
      {blob(220, 380, 520, "rgba(191,217,255,.95)", 23, 31)}
      {blob(880, 1500, 560, "rgba(255,230,128,.75)", 27, 21)}
      {blob(820, 520, 380, "rgba(234,243,255,1)", 19, 25)}
      <Sparkles frame={frame} color="#FFC800" count={16} seed="w" />
    </AbsoluteFill>
  );
};

const BlackBg: React.FC<{ frame: number }> = ({ frame }) => (
  <AbsoluteFill style={{ background: "#0B0B0D", overflow: "hidden" }}>
    <div
      style={{
        position: "absolute",
        left: -660,
        top: -260,
        width: 2400,
        height: 2400,
        background:
          "repeating-conic-gradient(from 0deg, rgba(255,214,10,.11) 0deg 6deg, rgba(255,214,10,0) 6deg 22deg)",
        transform: `rotate(${frame * 0.6}deg)`,
        WebkitMaskImage: "radial-gradient(circle, #000 0%, rgba(0,0,0,0) 55%)",
        maskImage: "radial-gradient(circle, #000 0%, rgba(0,0,0,0) 55%)",
      }}
    />
    <AbsoluteFill
      style={{ background: "radial-gradient(700px 700px at 50% 44%, rgba(255,214,10,.16) 0%, rgba(11,11,13,0) 70%)" }}
    />
    <Sparkles frame={frame} color="#FFD60A" count={22} seed="b" />
  </AbsoluteFill>
);

// Deterministic twinkling particles drifting upwards.
const Sparkles: React.FC<{ frame: number; color: string; count: number; seed: string }> = ({ frame, color, count, seed }) => (
  <>
    {Array.from({ length: count }, (_, i) => {
      const x = random(`${seed}x${i}`) * 1080;
      const y0 = random(`${seed}y${i}`) * 1920;
      const sp = 1.2 + random(`${seed}s${i}`) * 2.2;
      const size = 6 + random(`${seed}r${i}`) * 14;
      const tw = 0.35 + 0.65 * Math.abs(Math.sin(frame / (6 + i % 5) + i));
      const y = ((y0 - frame * sp) % 1920 + 1920) % 1920;
      return (
        <div
          key={i}
          style={{
            position: "absolute",
            left: x,
            top: y,
            width: size,
            height: size,
            background: color,
            opacity: tw * 0.8,
            transform: `rotate(45deg) scale(${tw})`,
            borderRadius: i % 3 === 0 ? "50%" : 2,
            boxShadow: `0 0 ${size * 1.5}px ${color}`,
          }}
        />
      );
    })}
  </>
);

const Line: React.FC<{ text: string; delay: number; dark: boolean; size: number; accent: string }> = ({
  text,
  delay,
  dark,
  size,
  accent,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const k = spring({ frame: frame - delay, fps, config: { damping: 16, stiffness: 150 } });
  const mark = interpolate(frame, [delay + 8, delay + 16], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const parts = text.split(/(\*[^*]+\*)/).filter(Boolean);
  return (
    <div style={{ overflow: "hidden", padding: "6px 30px 14px" }}>
      <div
        style={{
          transform: `translateY(${(1 - k) * 115}%)`,
          fontFamily: "Gilroy, Montserrat, sans-serif",
          fontWeight: 800,
          fontSize: size,
          lineHeight: 1.04,
          letterSpacing: "-0.03em",
          textAlign: "center",
          color: dark ? "#FFFFFF" : INK,
          whiteSpace: "nowrap",
        }}
      >
        {parts.map((p, i) => {
          const hot = p.startsWith("*");
          const word = hot ? p.slice(1, -1) : p;
          if (!hot) return <span key={i}>{word}</span>;
          return dark ? (
            <span key={i} style={{ color: accent, textShadow: `0 0 ${36 * mark}px rgba(255,214,10,.65)` }}>
              {word}
            </span>
          ) : (
            <span key={i} style={{ position: "relative", display: "inline-block", isolation: "isolate" }}>
              <span
                style={{
                  position: "absolute",
                  // full-height highlight box behind the whole word
                  left: "-0.12em",
                  right: "-0.12em",
                  top: "0.04em",
                  bottom: "0.02em",
                  background: accent,
                  borderRadius: "0.16em",
                  transform: `scaleX(${mark}) skewX(-6deg)`,
                  transformOrigin: "left center",
                  zIndex: -1,
                }}
              />
              {word}
            </span>
          );
        })}
      </div>
    </div>
  );
};

export const AccentCard: React.FC<{ card: Card; accent: string }> = ({ card, accent }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const len = Math.round((card.end - card.start) * fps);
  const dark = card.theme === "black";
  const ein = interpolate(frame, [0, 10], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const eout = interpolate(frame, [len - 9, len], [0, 1], { ...clamp, easing: Easing.in(Easing.cubic) });

  const enter = card.enter ?? "circle";
  let clipPath: string | undefined;
  let inScale = 1;
  let inOpacity = 1;
  if (enter === "circle") clipPath = `circle(${ein * 120}% at 50% 46%)`;
  else if (enter === "wipe") {
    const x = ein * 170;
    clipPath = `polygon(0 0, ${x}% 0, ${x - 40}% 100%, 0 100%)`;
  } else {
    inScale = 1.25 - 0.25 * ein;
    inOpacity = ein;
  }
  const exit = card.exit ?? "slide";
  const outY = exit === "slide" ? -1920 * eout : 0;
  const outScale = exit === "zoom" ? 1 - 0.18 * eout : 1;
  const outOpacity = exit === "zoom" ? 1 - eout : 1;

  const thinK = spring({ frame: frame - 3, fps, config: { damping: 200 } });
  const icoK = spring({ frame: frame - 13, fps, config: { damping: 10, stiffness: 170 } });
  const drift = interpolate(frame, [0, len], [1, 1.05]);
  const lines = card.big.split("|");

  return (
    <AbsoluteFill
      style={{
        clipPath,
        opacity: inOpacity * outOpacity,
        transform: `translateY(${outY}px) scale(${inScale * outScale})`,
      }}
    >
      {dark ? <BlackBg frame={frame} /> : <WhiteBg frame={frame} />}
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          paddingBottom: 140,
          transform: `scale(${drift})`,
        }}
      >
        <div
          style={{
            fontFamily: "Montserrat",
            fontWeight: 700,
            fontSize: 46,
            color: dark ? "#B8BCC4" : "#5D6066",
            opacity: thinK,
            transform: `translateY(${(1 - thinK) * 30}px)`,
            marginBottom: 10,
          }}
        >
          {card.thin}
        </div>
        {lines.map((l, i) => (
          <Line
            key={i}
            text={l}
            delay={5 + i * 4}
            dark={dark}
            size={card.numeric && i === 0 ? 230 : 132}
            accent={accent}
          />
        ))}
        {card.icon ? (
          <Img
            src={staticFile(`assets/icons/${card.icon}-${dark ? "white" : "blue"}.png`)}
            style={{
              marginTop: 34,
              height: 240,
              width: "auto",
              transform: `scale(${icoK}) translateY(${Math.sin(frame / 8) * 6}px)`,
            }}
          />
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
