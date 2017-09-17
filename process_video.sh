#!/bin/bash

VIDEO=$1
FRAMERATE=1
OUTDIR=ffmpeg-out

mkdir -p $OUTDIR
ffmpeg -i $VIDEO -vf fps=$FRAMERATE $OUTDIR/out%d.png

cd darkflow
flow --imgdir ../$OUTDIR \
     --model cfg/yolo.cfg \
     --load bin/yolo.weights --json

cd ..
FRAMECOUNT=$(ls -1q $OUTDIR/out/out* | wc -l)
python generate_report.py $OUTDIR $FRAMECOUNT $FRAMERATE
