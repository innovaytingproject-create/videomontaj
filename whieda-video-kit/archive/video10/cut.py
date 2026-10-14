import json, subprocess
S=[(0.0,0.3),(1.95,2.3),(4.85,5.25),(10.0,10.3),(12.4,12.75),(14.6,14.9),(16.15,16.5),(21.5,21.9),(25.1,25.55),(28.65,29.15),(31.3,31.6),(33.9,34.25),(37.6,38.0),(41.95,42.35),(45.75,46.05),(47.35,47.65),(52.5,52.9),(57.4,57.7),(60.75,61.05),(63.0,63.35),(67.95,68.3),(70.4,70.75),(72.85,73.3),(76.7,77.0),(80.5,80.85),(84.05,84.35),(87.1,87.45),(88.0,88.3),(94.5,95.0),(96.55,96.95),(98.25,98.55),(107.95,108.25),(110.15,110.6),(113.2,113.5),(114.75,115.05),(116.75,117.15),(118.45,118.75),(121.65,122.05),(122.9,123.2),(124.05,124.4),(125.65,126.6),(131.15,131.6),(133.05,133.4),(137.4,137.85),(142.15,142.6),(143.95,144.3),(145.15,145.5),(148.8,149.15),(149.45,149.8),(151.15,151.5)]
END=152.5
fr=lambda t: round(round(t*30)/30,4)
keep=[];cur=None
for a,b in S:
    if b-a<0.3: continue
    pa,pb=(0.10,0.10)
    if cur is None:  # leading silence
        cur=fr(b-0.12); continue
    keep.append((cur,fr(a+pa))); cur=fr(b-pb)
keep.append((cur,fr(END)))
keep=[k for k in keep if k[1]-k[0]>0.2]
json.dump(keep,open('work/keep.json','w'))
tot=sum(b-a for a,b in keep); print(len(keep),'segments, total',round(tot,2))
GRADE=("hqdn3d=1.5:1.5:4:4,eq=brightness=0.045:contrast=1.08:saturation=1.32:gamma=1.04,"
       "colorbalance=rm=0.02:bm=-0.01:rh=0.01,curves=master='0/0.01 0.25/0.24 0.75/0.8 1/1',unsharp=5:5:0.7:5:5:0")
VOICE=("highpass=f=90,afftdn=nf=-25,equalizer=f=3000:t=q:w=1.2:g=2.5,"
       "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=9")
fc=[];lab=""
for i,(a,b) in enumerate(keep):
    z=1.0 if i%2==0 else 1.09   # alternate framing hides jump cuts
    zf=f",scale={int(1080*z)//2*2}:{int(1920*z)//2*2},crop=1080:1920:(iw-1080)/2:(ih-1920)*0.35,setsar=1" if z>1 else ""
    fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,setsar=1{zf}[v{i}]")
    fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={b-a-0.02:.3f}:d=0.02[a{i}]")
    lab+=f"[v{i}][a{i}]"
fc.append(f"{lab}concat=n={len(keep)}:v=1:a=1[vc][ac]")
fc.append(f"[vc]setpts=PTS/1.25,fps=30,{GRADE}[v]")
fc.append(f"[ac]atempo=1.25,{VOICE}[a]")
subprocess.run(["ffmpeg","-v","error","-y","-i","work/joined.mov","-filter_complex",";".join(fc),
  "-map","[v]","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-an","work/video.mp4",
  "-map","[a]","-ar","48000","-ac","2","work/voice.wav"],check=True)
