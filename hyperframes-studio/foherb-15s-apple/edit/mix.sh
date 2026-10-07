#!/bin/bash
# Final mix: louder voice (-13 LUFS), quiet music bed, iOS-style SFX accents.
set -e
cd "$(dirname "$0")/.."
LEN=15.4; VE=13.2
ffmpeg -v error -y -i out/pic.mp4 -i assets/voice15.wav -i assets/music-chronos.mp3 \
  -i assets/sfx/tick.wav -i assets/sfx/pop.wav -i assets/sfx/whoosh.wav -i assets/sfx/ding.wav \
  -i assets/sfx/paydone.wav -i assets/sfx/boom.wav -i assets/sfx/riser.wav -filter_complex "
[1:a]aresample=48000,apad=whole_dur=${LEN},asplit=2[voice][key];
[2:a]aresample=48000,atrim=0:${LEN},asetpts=PTS-STARTPTS,volume=-13dB,
  volume='1+min(max(t-${VE}+0.2,0)/0.5,1)*0.55':eval=frame,
  afade=t=in:d=0.5,afade=t=out:st=13.9:d=1.5[bed];
[bed][key]sidechaincompress=threshold=0.04:ratio=3:attack=25:release=450:makeup=1[ducked];
[3:a]aresample=48000,asplit=2[t1][t2];
[t1]adelay=420:all=1[s1];[t2]adelay=950:all=1[s2];
[4:a]aresample=48000,asplit=2[p1][p2];
[p1]adelay=550:all=1[s3];[p2]adelay=14100:all=1[s4];
[5:a]aresample=48000,adelay=2280:all=1[s5];
[6:a]aresample=48000,adelay=5400:all=1,volume=-4dB[s6];
[7:a]aresample=48000,adelay=9000:all=1,volume=-3dB[s7];
[8:a]aresample=48000,adelay=11340:all=1[s8];
[9:a]aresample=48000,adelay=12350:all=1,volume=-5dB[s9];
[s1][s2][s3][s4][s5][s6][s7][s8][s9]amix=inputs=9:duration=longest:normalize=0,volume=-14dB,apad=whole_dur=${LEN}[sfx];
[voice][ducked][sfx]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-13:TP=-1.0:LRA=9[mix]" \
  -map 0:v -map "[mix]" -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p \
  -c:a aac -b:a 160k -ar 48000 -movflags +faststart out/foherb-15s-apple-v3.mp4
echo done
