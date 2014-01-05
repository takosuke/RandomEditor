#!/usr/bin/env bash
ffprobe -show_frames -of compact=p=0 -f lavfi "movie=$1,select=gt(scene\,0.4)" | sed  -E 's/.*pkt_pts_time=([0-9.]{8,})\|.*/\1/' | tee /dev/stderr | python cutter.py $1