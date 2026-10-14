# video15: Biznes Xitoy bilan — 6 parts joined, silences removed, nothing said is cut.
import subprocess, os, json
K=[(0.66,5.41),(5.58,6.33),(8.69,14.53),(15.21,15.92),(16.97,18.21),(18.45,33.65),(35.98,55.48),(57.58,63.46),(63.61,67.84),(69.80,99.37)]
fr=lambda t: round(round(t*30)/30,4)
K=[(fr(a),fr(b)) for a,b in K]
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
