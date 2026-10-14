import subprocess, json
SEG=[(0.0,6.0,1.5),(6.0,12.0,1.5),(12.0,18.0,2.0),(19.0,23.5,1.0),(31.5,42.5,1.25),(43.0,47.5,1.0),
     (60.0,72.0,2.0),(76.0,85.0,3.0),(88.0,93.5,2.0),(94.0,99.8,1.0)]
GRADE=("hqdn3d=1.5:1.5:4:4,eq=brightness=0.045:contrast=1.08:saturation=1.32:gamma=1.04,"
       "colorbalance=rm=0.02:bm=-0.01:rh=0.01,curves=master='0/0.01 0.25/0.24 0.75/0.8 1/1',unsharp=5:5:0.7:5:5:0")
fc=[];lab="";t=0;marks=[]
def atempo(s):
    out=[]
    while s>2.0: out.append("atempo=2.0"); s/=2.0
    out.append(f"atempo={s}"); return ",".join(out)
for i,(a,b,s) in enumerate(SEG):
    fc.append(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{s},fps=30,setsar=1[v{i}]")
    fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,{atempo(s)},afade=t=in:d=0.02,afade=t=out:st={(b-a)/s-0.03:.3f}:d=0.03[a{i}]")
    lab+=f"[v{i}][a{i}]"; marks.append(round(t,2)); t+=(b-a)/s
fc.append(f"{lab}concat=n={len(SEG)}:v=1:a=1[vc][ac]")
fc.append(f"[vc]{GRADE}[v]")
fc.append("[ac]highpass=f=90,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=9[a]")
subprocess.run(["ffmpeg","-v","error","-y","-i","work/joined.mov","-filter_complex",";".join(fc),
  "-map","[v]","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-an","work/video.mp4",
  "-map","[a]","-ar","48000","-ac","2","work/voice.wav"],check=True)
json.dump(marks,open("work/segment_starts.json","w")); print("starts",marks,"total",round(t,2))
