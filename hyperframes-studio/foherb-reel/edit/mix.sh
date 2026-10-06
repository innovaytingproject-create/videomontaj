#!/bin/bash
# Final mix: voice + music bed ducked under speech, swell on the end card, loudness for Reels (-14 LUFS).
set -e
cd "$(dirname "$0")/.."
LEN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/picture.mp4)
VOICE_END=$(ffprobe -v error -show_entries format=duration -of csv=p=0 assets/voice.wav)
ffmpeg -v error -y -i out/picture.mp4 -i assets/voice.wav -i assets/music-advertime.mp3 -filter_complex "
[1:a]aresample=48000,apad=whole_dur=${LEN},asplit=2[voice][key];
[2:a]aresample=48000,atrim=0:${LEN},asetpts=PTS-STARTPTS,volume=-9dB,
  volume='1+min(max(t-${VOICE_END}+0.2,0)/0.6,1)*0.5':eval=frame,
  afade=t=in:d=0.4,afade=t=out:st=$(echo "$LEN - 1.6" | bc):d=1.6[bed];
[bed][key]sidechaincompress=threshold=0.05:ratio=2.5:attack=30:release=500:makeup=1[ducked];
[voice][ducked]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.2:LRA=9[mix]" \
  -map 0:v -map "[mix]" -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart out/foherb-reel-v1.mp4
echo "out/foherb-reel-v1.mp4"
