import json, subprocess, re, os
src=open("work/cut.py").read()
S=eval(re.search(r"^S=(\[.*\])$",src,re.M).group(1)); END=152.5
fr=lambda t: round(round(t*30)/30,4)
keep=[];cur=None
for a,b in S:
    if b-a<0.3: continue
    if cur is None: cur=fr(b-0.12); continue
    keep.append((cur,fr(a+0.10))); cur=fr(b-0.10)
keep.append((cur,fr(END))); keep=[k for k in keep if k[1]-k[0]>0.2]
json.dump(keep,open("work/keep.json","w"))
os.makedirs("work/seg",exist_ok=True); L=[]
for i,(a,b) in enumerate(keep):
    z=",scale=1176:2092,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.35" if i%2 else ""
    f=f"work/seg/s{i:02d}.mov"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-i","work/joined.mov","-t",f"{b-a:.4f}",
      "-vf",f"setsar=1{z},setsar=1,fps=30","-af",f"afade=t=in:d=0.015,afade=t=out:st={b-a-0.02:.3f}:d=0.02",
      "-c:v","libx264","-crf","12","-preset","fast","-pix_fmt","yuv420p","-c:a","pcm_s16le","-ar","48000",f],check=True)
    L.append(f"file 's{i:02d}.mov'")
open("work/seg/list.txt","w").write("\n".join(L))
GRADE=("hqdn3d=1.5:1.5:4:4,eq=brightness=0.045:contrast=1.08:saturation=1.32:gamma=1.04,"
       "colorbalance=rm=0.02:bm=-0.01:rh=0.01,curves=master='0/0.01 0.25/0.24 0.75/0.8 1/1',unsharp=5:5:0.7:5:5:0")
VOICE=("highpass=f=90,afftdn=nf=-25,equalizer=f=3000:t=q:w=1.2:g=2.5,"
       "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=9")
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","work/seg/list.txt",
  "-vf",f"setpts=PTS/1.25,fps=30,{GRADE}","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-an","work/video.mp4",
  "-af",f"atempo=1.25,{VOICE}","-vn","-ar","48000","-ac","2","work/voice.wav"],check=True)
print(len(keep),"segments",round(sum(b-a for a,b in keep),2))
