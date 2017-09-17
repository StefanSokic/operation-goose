# Operation Goose 

## Computer Vision API and Surveillance Analytics Software
Using the yolo/tiny models built on darkflow (the tensorflow translation of darknet), we created operation-gooose, a computer vision API which logs objects, motion, and anomalies in natural language. Built for Hack the North 2017.

## What It Does
Users can upload files via the operation-goose API and receive a corresponding text file and time-series analysis summarizing file meta-data:
     1. Object counts at distinct time points
     2. Time stamps of significant change to camera feed
     3. Object quantities, appearances, and exits over time

The received video summary offers a significant use case in the processing of long-term surveillance footage, highlighting solely those times in which activity is detected in the frame.

All detected instances are logged with a time stamp and annotated with natural language:

     e.g. 34.51 s:
     1 car enters the frame.
     1 truck exits the frame.
     2 people enter the frame.

     Total objects detected:
     cars: 8
     motorbikes: 2
     people: 2
     trucks: 2

## How We Built It
As mentioned above, object detection was done via yolo/tiny-yolo models, with counts and labels fed into various Python scripts designed to detect major changes and bouts of activity in frames. The server backend was built with Flask. Built for the CANSOFCOM challenge.

## Setup
First, install Anaconda3 from online.
Make sure to install ffmpeg.
Then

```
conda update conda
conda create -n goose python=3.6 anaconda
source activate goose

conda uninstall numpy # sometimes needs to be reinstalled alongside tensorflow for darkflow to work
conda install tensorflow opencv

git clone https://github.com/ninkle/operation-goose
cd operation-goose
git submodule update --init --recursive

cd darkflow

pip install -e .

mkdir bin
cd bin
wget --no-check-certificate https://pjreddie.com/media/files/tiny-yolo-voc.weights

cd ..
cd cfg
wget --no-check-certificate https://pjreddie.com/media/files/tiny-yolo-voc.weights


cd ../..
```
If you want to run the script alone, it is run by going to the `operation-goose` directory and typing 
```
bash process_video.sh <video path> 
```
Otherwise, the application is run by
```
python main.py
```
