import subprocess, os, json
K=[(0.3,7.65,1),(7.85,9.1,1),(10.15,13.55,1),(13.65,14.55,1),(14.65,18.75,1),(18.9,20.35,1),(21.2,29.1,1),(30.15,31.1,1),(31.25,33.55,1),(33.75,36.5,1),
   (36.5,43.6,1),(43.85,46.2,1),(46.5,48.0,1),(48.35,49.1,1),(49.2,51.65,1),(51.8,56.25,1),(59.25,64.5,1)]
fr=lambda t: round(round(t*30)/30,4)
os.makedirs("work/seg",exist_ok=True);L=[];t=0;starts=[]
for i,(a,b,s) in enumerate(K):
    a,b=fr(a),fr(b)
    z=",scale=1176:2092,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.35" if i%2 else ""
    d=(b-a)/s
    at="" if s==1 else f",atempo={s}"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-i","work/joined.mov","-t",f"{b-a:.4f}",
      "-vf",f"setpts=(PTS-STARTPTS)/{s},setsar=1{z},setsar=1,fps=30",
      "-af",f"asetpts=PTS-STARTPTS{at},afade=t=in:d=0.015,afade=t=out:st={d-0.02:.3f}:d=0.02",
      "-c:v","libx264","-crf","12","-preset","fast","-pix_fmt","yuv420p","-c:a","pcm_s16le","-ar","48000",f"work/seg/s{i:02d}.mov"],check=True)
    L.append(f"file 's{i:02d}.mov'"); starts.append(round(t,2)); t+=d
open("work/seg/list.txt","w").write("\n".join(L))
GRADE=("hqdn3d=1.5:1.5:4:4,eq=brightness=0.045:contrast=1.08:saturation=1.32:gamma=1.04,"
       "colorbalance=rm=0.02:bm=-0.01:rh=0.01,curves=master='0/0.01 0.25/0.24 0.75/0.8 1/1',unsharp=5:5:0.7:5:5:0")
VOICE=("highpass=f=90,afftdn=nf=-25,equalizer=f=3000:t=q:w=1.2:g=2.5,"
       "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=9")
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","work/seg/list.txt",
  "-vf",GRADE,"-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-an","work/video.mp4",
  "-af",VOICE,"-vn","-ar","48000","-ac","2","work/voice.wav"],check=True)
json.dump(starts,open("work/seg_starts.json","w")); print("starts",starts,"total",round(t,2))
