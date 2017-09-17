#!/bin/bash

VIDEO=$1
FRAMERATE=1
OUTDIR=ffmpeg-out
MODEL=tiny-yolo-voc

mkdir -p $OUTDIR
ffmpeg -i $VIDEO -vf fps=$FRAMERATE $OUTDIR/out%d.png

cd darkflow
flow --imgdir ../$OUTDIR \
     --model cfg/$MODEL.cfg \
     --load bin/$MODEL.weights --json

cd ..
FRAMECOUNT=$(ls -1q $OUTDIR/out/out* | wc -l)
python generate_report.py $OUTDIR $FRAMECOUNT $FRAMERATE
