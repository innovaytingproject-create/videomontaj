import { loadFont } from "@remotion/fonts";
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// Vertical reel in the approved WHIEDA style, driven entirely by an edit JSON
// (src/edits/<name>.json). Media lives in public/<name>/ (prepare_reel.py),
// shared kit assets in public/assets/.

export type CaptionWord = { t: number; text: string; hot?: boolean };
export type Caption = { start: number; end: number; words: CaptionWord[] };
export type Pill = { start: number; end: number; text: string; icon?: string };
export type Sticker = {
  file: string;
  start: number;
  end: number;
  x: number; // centre, px in the 1080x1920 frame
  y: number;
  w: number;
  rot?: number;
};
export type Edit = {
  name: string;
  duration: number; // seconds
  accent: string; // highlighted words
  // Reframe: zoom around the face and lift it to the viewer's eye level.
  framing: { originX: number; originY: number; scale: number; shiftY: number };
  cuts: number[]; // "camera" transitions: punch + blur + soft flash
  captions: Caption[];
  pills: Pill[];
  stickers: Sticker[];
  music: string;
  musicDb: number;
  sfx?: [string, number, number][]; // extra [sound, time, dB]
};

loadFont({ family: "Gilroy", url: staticFile("assets/fonts/Gilroy-ExtraBold.otf"), weight: "800" });
loadFont({ family: "Montserrat", url: staticFile("assets/fonts/Montserrat-Bold.ttf"), weight: "700" });

const INK = "#1D1D1F";
const BLUE = "#0A84FF";
const db = (d: number) => Math.pow(10, d / 20);

// Alternating push-in / pull-out between cuts, plus a punch at each cut.
const useCamera = (edit: Edit) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const bounds = [0, ...edit.cuts, edit.duration];
  const seg = Math.max(0, bounds.findIndex((b, i) => t >= b && t < (bounds[i + 1] ?? Infinity)));
  const a = bounds[seg];
  const b = bounds[seg + 1] ?? edit.duration;
  const p = interpolate(t, [a, b], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.sin),
  });
  let zoom = seg % 2 === 0 ? 1 + 0.12 * p : 1.16 - 0.12 * p;
  let rot = 0;
  let blur = 0;
  let flash = 0;
  for (const [i, c] of edit.cuts.entries()) {
    const d = t - c;
    if (d > -0.18 && d < 0.3) {
      const k = d < 0 ? interpolate(d, [-0.18, 0], [0, 1]) : interpolate(d, [0, 0.3], [1, 0], { easing: Easing.out(Easing.cubic) });
      zoom *= 1 + 0.07 * k;
      rot += (i % 2 ? -1.5 : 1.5) * k;
      blur += 7 * k;
      flash = Math.max(flash, 0.22 * k);
    }
  }
  return { zoom, rot, blur, flash };
};

const Footage: React.FC<{ edit: Edit }> = ({ edit }) => {
  const { zoom, rot, blur, flash } = useCamera(edit);
  const f = edit.framing;
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#000" }}>
      <AbsoluteFill
        style={{
          transformOrigin: `${f.originX}px ${f.originY}px`,
          transform: `translateY(${f.shiftY}px) scale(${f.scale * zoom}) rotate(${rot}deg)`,
          filter: blur > 0.2 ? `blur(${blur}px)` : undefined,
        }}
      >
        <OffthreadVideo src={staticFile(`${edit.name}/clip.mp4`)} muted style={{ width: 1080, height: 1920 }} />
      </AbsoluteFill>
      <AbsoluteFill style={{ backgroundColor: "#fff", opacity: flash }} />
    </AbsoluteFill>
  );
};

const CaptionView: React.FC<{ cap: Caption; accent: string }> = ({ cap, accent }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps + cap.start;
  const out = interpolate(t, [cap.end - 0.12, cap.end], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 70, right: 70, bottom: 860, display: "flex", justifyContent: "center", opacity: out }}>
      <div
        style={{
          maxWidth: 920,
          textAlign: "center",
          fontFamily: "Gilroy, Montserrat, sans-serif",
          fontWeight: 800,
          fontSize: 62,
          lineHeight: 1.16,
          color: "#fff",
          textShadow:
            "0 2px 2px rgba(5,12,28,.9), 0 0 8px rgba(5,12,28,.75), 0 3px 14px rgba(5,12,28,.7), 0 0 34px rgba(5,12,28,.6), 0 12px 44px rgba(5,12,28,.5)",
        }}
      >
        {cap.words.map((w, i) => {
          const k = spring({ frame: frame - Math.round((w.t - cap.start) * fps), fps, config: { damping: 14, stiffness: 220 } });
          return (
            <span
              key={i}
              style={{
                display: "inline-block",
                marginRight: "0.24em",
                color: w.hot ? accent : "#fff",
                opacity: Math.min(1, k * 1.6),
                transform: `translateY(${(1 - k) * 22}px) scale(${0.7 + 0.3 * k})`,
              }}
            >
              {w.text}
            </span>
          );
        })}
      </div>
    </div>
  );
};

const PillView: React.FC<{ pill: Pill }> = ({ pill }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const len = (pill.end - pill.start) * fps;
  const k = spring({ frame, fps, config: { damping: 13, stiffness: 180 } });
  const out = interpolate(frame, [len - 8, len], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", top: 170, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: out }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 18,
          background: "rgba(255,255,255,.97)",
          borderRadius: 60,
          padding: "14px 34px 14px 16px",
          boxShadow: "0 14px 40px rgba(10,20,40,.28)",
          transform: `translateY(${(1 - k) * -60}px) scale(${0.6 + 0.4 * k})`,
          opacity: Math.min(1, k * 2),
        }}
      >
        <div
          style={{
            width: 64,
            height: 64,
            borderRadius: "50%",
            background: BLUE,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#fff",
            fontFamily: "Gilroy",
            fontSize: 34,
          }}
        >
          {pill.icon ? <Img src={staticFile(`assets/icons/${pill.icon}-white.png`)} style={{ height: 46 }} /> : "✓"}
        </div>
        <span style={{ fontFamily: "Montserrat", fontWeight: 700, fontSize: 34, color: INK }}>{pill.text}</span>
      </div>
    </div>
  );
};

const StickerView: React.FC<{ s: Sticker }> = ({ s }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const len = (s.end - s.start) * fps;
  const k = spring({ frame, fps, config: { damping: 9, stiffness: 160 } });
  const out = spring({ frame: frame - (len - 9), fps, config: { damping: 200 } });
  const scale = k * (1 - out);
  const wobble = Math.sin(frame / 9) * 2.5;
  const float = Math.sin(frame / 14) * 6;
  return (
    <Img
      src={staticFile(`assets/stickers/${s.file}.png`)}
      style={{
        position: "absolute",
        left: s.x - s.w / 2,
        top: s.y - s.w / 2 + float,
        width: s.w,
        transform: `scale(${scale}) rotate(${(s.rot ?? 0) + wobble}deg)`,
        filter: "drop-shadow(0 12px 22px rgba(10,20,40,.35))",
      }}
    />
  );
};

const Sfx: React.FC<{ name: string; at: number; gainDb: number }> = ({ name, at, gainDb }) => {
  const { fps } = useVideoConfig();
  return (
    <Sequence from={Math.max(0, Math.round(at * fps))} layout="none">
      <Audio src={staticFile(`assets/sfx/${name}.wav`)} volume={db(gainDb - 8)} />
    </Sequence>
  );
};

export const WhiedaReel: React.FC<{ edit: Edit }> = ({ edit }) => {
  const { fps } = useVideoConfig();
  const sec = (s: number) => Math.round(s * fps);
  const speaking = (t: number) => edit.captions.some((c) => t >= c.start - 0.15 && t <= c.end + 0.15);
  const events: [string, number, number][] = [
    ...edit.cuts.flatMap((c): [string, number, number][] => [["whoosh", c - 0.32, 0], ["boom", c, -6]]),
    ...edit.stickers.map((s): [string, number, number] => ["pop", s.start, -1]),
    ...edit.pills.map((p): [string, number, number] => ["tick", p.start, 0]),
    ...(edit.sfx ?? []),
  ];
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Footage edit={edit} />
      {edit.stickers.map((s, i) => (
        <Sequence key={`s${i}`} from={sec(s.start)} durationInFrames={sec(s.end - s.start)} layout="none">
          <StickerView s={s} />
        </Sequence>
      ))}
      {edit.pills.map((p, i) => (
        <Sequence key={`p${i}`} from={sec(p.start)} durationInFrames={sec(p.end - p.start)} layout="none">
          <PillView pill={p} />
        </Sequence>
      ))}
      {edit.captions.map((c, i) => (
        <Sequence key={`c${i}`} from={sec(c.start)} durationInFrames={sec(c.end - c.start)} layout="none">
          <CaptionView cap={c} accent={edit.accent} />
        </Sequence>
      ))}
      <Audio src={staticFile(`${edit.name}/voice.wav`)} />
      <Audio
        src={staticFile(`assets/music/${edit.music}.mp3`)}
        volume={(f) => {
          const t = f / fps;
          const fade = interpolate(t, [0, 0.5, edit.duration - 1.2, edit.duration], [0, 1, 1, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          // ducking: music sits ~20 dB under the voice while she speaks
          return db(edit.musicDb + (speaking(t) ? -9 : 0)) * fade;
        }}
      />
      {events
        .filter(([, at]) => at >= 0 && at < edit.duration - 0.1)
        .map(([n, at, g], i) => (
          <Sfx key={`x${i}`} name={n} at={at} gainDb={g} />
        ))}
    </AbsoluteFill>
  );
};
