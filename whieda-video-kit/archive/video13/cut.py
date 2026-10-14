# video13: Aktivator kletok. 4 source parts joined (work/joined.mov). Parts 3-4 are silent demo -> B-roll.
import json, subprocess, os
SPEED=1.2
fr=lambda t: round(round(t*30)/30,4)
# keep list in SOURCE time, in playback order (part 2 postscript moved before the closing lines)
K=[(6.62,9.72),(9.98,20.24),(20.47,24.10),(24.26,29.54),(29.72,31.08),(31.34,42.97),(43.13,49.82),
   (50.42,70.86),(71.06,81.02),(81.26,99.30),(100.88,104.95),(120.30,131.92),(133.56,135.28),(104.98,109.62),(109.95,118.95)]
K=[(fr(a),fr(b)) for a,b in K]
json.dump({"keep":K,"speed":SPEED},open("work/keep.json","w"))
def m(t):  # source time -> pre-speed timeline
    acc=0
    for a,b in K:
        if a<=t<=b: return acc+t-a
        acc+=b-a
    raise ValueError(t)
# B-roll: (source voice time where it starts, b-roll source start, duration) — all pre-speed seconds
BR=[(28.25,136.6,2.75),(31.40,141.7,3.1),(37.0,175.0,2.6),(54.2,149.0,2.9),(62.05,161.2,2.7),
    (65.25,144.7,2.0),(77.45,158.6,2.0),(82.3,170.6,3.9)]
os.makedirs("work/seg",exist_ok=True);L=[]
for i,(a,b) in enumerate(K):
    z=",scale=1176:2092,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.35" if i%2 else ""
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-i","work/joined.mov","-t",f"{b-a:.4f}",
      "-vf",f"setsar=1{z},setsar=1,fps=30","-af",f"afade=t=in:d=0.015,afade=t=out:st={b-a-0.02:.3f}:d=0.02",
      "-c:v","libx264","-crf","12","-preset","fast","-pix_fmt","yuv420p","-c:a","pcm_s16le","-ar","48000",f"work/seg/s{i:02d}.mov"],check=True)
    L.append(f"file 's{i:02d}.mov'")
open("work/seg/list.txt","w").write("\n".join(L))
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","work/seg/list.txt","-c","copy","work/seg/base.mov"],check=True)
fc=[];prev="0:v"
for n,(vt,bs,d) in enumerate(BR):
    o=m(vt)
    fc.append(f"[1:v]trim={bs}:{bs+d},setpts=PTS-STARTPTS+{o:.3f}/TB,setsar=1[b{n}]")
    fc.append(f"[{prev}][b{n}]overlay=0:0:enable='between(t,{o:.3f},{o+d-0.01:.3f})':eof_action=pass[o{n}]")
    prev=f"o{n}"
GRADE=("hqdn3d=1.5:1.5:4:4,eq=brightness=0.045:contrast=1.08:saturation=1.32:gamma=1.04,"
       "colorbalance=rm=0.02:bm=-0.01:rh=0.01,curves=master='0/0.01 0.25/0.24 0.75/0.8 1/1',unsharp=5:5:0.7:5:5:0")
VOICE=("highpass=f=90,afftdn=nf=-25,equalizer=f=3000:t=q:w=1.2:g=2.5,"
       "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=9")
fc.append(f"[{prev}]setpts=PTS/{SPEED},fps=30,{GRADE}[v]")
fc.append(f"[0:a]atempo={SPEED},{VOICE}[a]")
subprocess.run(["ffmpeg","-v","error","-y","-i","work/seg/base.mov","-i","work/joined.mov","-filter_complex",";".join(fc),
  "-map","[v]","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-an","work/video.mp4",
  "-map","[a]","-ar","48000","-ac","2","work/voice.wav"],check=True)
tot=sum(b-a for a,b in K)
print(len(K),"segments",round(tot,2),"->",round(tot/SPEED,2))
