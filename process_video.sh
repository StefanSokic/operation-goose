#!/bin/bash

VIDEO=$1
FRAMERATE=1
IMDIR=ffmpeg-out
MODEL=tiny-yolo-voc
DOWNLOAD=downloads

mkdir -p $IMDIR
ffmpeg -i $VIDEO -vf fps=$FRAMERATE $IMDIR/out%d.png

cd darkflow
flow --imgdir ../$IMDIR \
     --model cfg/$MODEL.cfg \
     --load bin/$MODEL.weights --json

cd ..
FRAMECOUNT=$(ls -1q $IMDIR/out/out* | wc -l)
python generate_report.py $IMDIR $FRAMECOUNT $FRAMERATE \
       | echo > log.txt
