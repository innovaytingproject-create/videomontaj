import subprocess, os, json
S=[(0.0,0.9),(5.9,6.2),(7.95,8.4),(10.6,10.9),(13.45,13.75),(18.1,18.75),(19.55,20.0),(26.05,26.45),(29.6,30.05),(34.6,35.1),(37.85,38.25),(39.25,39.65),(41.35,41.75),(49.1,49.6),(52.1,52.45),(54.5,54.85),(56.2,56.55),(60.55,61.5),(63.55,63.9),(65.45,65.75),(67.25,67.7),(69.1,69.45),(72.1,73.05),(74.6,74.95),(76.1,76.4),(77.95,78.25),(79.0,79.3)]
END=83.75
fr=lambda t: round(round(t*30)/30,4)
K=[];cur=None
for a,b in S:
    if cur is None: cur=fr(b-0.12); continue
    K.append((cur,fr(a+0.10))); cur=fr(b-0.10)
K.append((cur,fr(END)))
json.dump(K,open("work/keep.json","w"))
os.makedirs("work/seg",exist_ok=True);L=[]
for i,(a,b) in enumerate(K):
    z=",scale=1176:2092,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.35" if i%2 else ""
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-i","work/joined.mov","-t",f"{b-a:.4f}",
      "-vf",f"setsar=1{z},setsar=1,fps=30","-af",f"afade=t=in:d=0.015,afade=t=out:st={b-a-0.02:.3f}:d=0.02",
      "-c:v","libx264","-crf","12","-preset","fast","-pix_fmt","yuv420p","-c:a","pcm_s16le","-ar","48000",f"work/seg/s{i:02d}.mov"],check=True)
    L.append(f"file 's{i:02d}.mov'")
open("work/seg/list.txt","w").write("\n".join(L))
GRADE=("hqdn3d=1.5:1.5:4:4,eq=brightness=0.045:contrast=1.08:saturation=1.32:gamma=1.04,"
       "colorbalance=rm=0.02:bm=-0.01:rh=0.01,curves=master='0/0.01 0.25/0.24 0.75/0.8 1/1',unsharp=5:5:0.7:5:5:0")
VOICE=("highpass=f=90,afftdn=nf=-25,equalizer=f=3000:t=q:w=1.2:g=2.5,"
       "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=9")
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","work/seg/list.txt",
  "-vf",GRADE,"-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-an","work/video.mp4",
  "-af",VOICE,"-vn","-ar","48000","-ac","2","work/voice.wav"],check=True)
print(len(K),round(sum(b-a for a,b in K),2))
