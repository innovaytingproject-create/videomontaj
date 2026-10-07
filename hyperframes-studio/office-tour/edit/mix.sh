#!/bin/bash
set -e
cd "$(dirname "$0")/.."
LEN=90.5; VE=88.0
ffmpeg -v error -y -i out/pic.mp4 -i assets/voice2.wav -i assets/music-chronos.mp3 \
  -i assets/sfx/tick.wav -i assets/sfx/pop.wav -i assets/sfx/whoosh.wav -i assets/sfx/ding.wav \
  -i assets/sfx/paydone.wav -i assets/sfx/boom.wav -i assets/sfx/riser.wav -filter_complex "
[1:a]aresample=48000,apad=whole_dur=${LEN},asplit=2[voice][key];
[2:a]aresample=48000,atrim=0:${LEN},asetpts=PTS-STARTPTS,volume=-13dB,
  volume='1+min(max(t-${VE}+0.2,0)/0.5,1)*0.55':eval=frame,
  afade=t=in:d=0.5,afade=t=out:st=88.9:d=1.6[bed];
[bed][key]sidechaincompress=threshold=0.04:ratio=3:attack=25:release=450:makeup=1[ducked];
[3:a]aresample=48000,asplit=7[t1][t2][t3][t4][t5][t6][t7];
[t1]adelay=420:all=1[s1];[t2]adelay=950:all=1[s2];[t3]adelay=15300:all=1[s3];
[t4]adelay=30600:all=1[s4];[t5]adelay=47900:all=1[s5];[t6]adelay=57900:all=1[s6];[t7]adelay=64100:all=1[s7];
[4:a]aresample=48000,asplit=6[p1][p2][p3][p4][p5][p6];
[p1]adelay=550:all=1[s8];[p2]adelay=59500:all=1[s9];[p3]adelay=61000:all=1[s10];
[p4]adelay=62500:all=1[s11];[p5]adelay=78350:all=1[s12];[p6]adelay=89150:all=1[s13];
[5:a]aresample=48000,adelay=2280:all=1[s14];
[6:a]aresample=48000,adelay=9950:all=1,volume=-4dB[s15];
[7:a]aresample=48000,adelay=17200:all=1,volume=-3dB[s16];
[8:a]aresample=48000,adelay=78300:all=1[s17];
[9:a]aresample=48000,adelay=86900:all=1,volume=-5dB[s18];
[s1][s2][s3][s4][s5][s6][s7][s8][s9][s10][s11][s12][s13][s14][s15][s16][s17][s18]amix=inputs=18:duration=longest:normalize=0,volume=-14dB,apad=whole_dur=${LEN}[sfx];
[voice][ducked][sfx]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-13:TP=-1.0:LRA=9[mix]" \
  -map 0:v -map "[mix]" -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p \
  -c:a aac -b:a 160k -ar 48000 -movflags +faststart out/meda-office-tour.mp4
echo done
