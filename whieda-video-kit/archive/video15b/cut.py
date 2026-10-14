# video15b: standalone edit of part 6 (masterclass invitation), taken from ../video15/work/joined.mov
import subprocess, json
K=[(69.80,99.37)]
json.dump(K,open("work/keep.json","w"))
A,B=K[0]
GRADE=("hqdn3d=1.5:1.5:4:4,eq=brightness=0.045:contrast=1.08:saturation=1.32:gamma=1.04,"
       "colorbalance=rm=0.02:bm=-0.01:rh=0.01,curves=master='0/0.01 0.25/0.24 0.75/0.8 1/1',unsharp=5:5:0.7:5:5:0")
VOICE=("highpass=f=90,afftdn=nf=-25,equalizer=f=3000:t=q:w=1.2:g=2.5,"
       "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=9")
subprocess.run(["ffmpeg","-v","error","-y","-ss",str(A),"-t",f"{B-A:.3f}","-i","../video15/work/joined.mov",
  "-vf",GRADE,"-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-an","work/video.mp4",
  "-af",f"afade=t=in:d=0.03,afade=t=out:st={B-A-0.1:.3f}:d=0.1,{VOICE}","-vn","-ar","48000","-ac","2","work/voice.wav"],check=True)
