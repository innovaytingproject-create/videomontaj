import json, subprocess
S=[(0.0,0.75),(3.2,3.65),(5.9,6.35),(8.4,8.75),(15.45,15.8),(19.6,19.95),(23.4,23.75),(27.05,27.55),(27.95,28.8),(32.15,32.5),(36.85,37.3),(41.65,41.95),(45.5,45.85),(51.4,51.75),(53.45,53.9),(56.65,56.95),(59.25,59.6),(63.95,64.3),(65.55,65.85),(69.85,70.25),(75.2,75.5),(79.45,79.85),(81.7,82.1),(87.15,87.5),(91.1,91.4),(93.65,94.05),(94.35,94.8),(98.25,98.55),(100.8,101.2),(107.6,107.9)]
END=110.25
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
fc.append(f"[vc]{GRADE}[v]")
fc.append(f"[ac]{VOICE}[a]")
subprocess.run(["ffmpeg","-v","error","-y","-i","work/joined.mov","-filter_complex",";".join(fc),
  "-map","[v]","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-an","work/video.mp4",
  "-map","[a]","-ar","48000","-ac","2","work/voice.wav"],check=True)
